import type { Server } from "node:http";
import type { AddressInfo } from "node:net";
import { afterAll, afterEach, beforeAll, beforeEach, describe, expect, it } from "vitest";
import { startBridge } from "@/server/linkedin/bridge";
import { ProviderAuthError, type AccountRef, type LinkedInProvider } from "@/server/linkedin/types";
import {
  SESSION_TO_OPEN_REASON,
  connectAccount,
  diagnoseAccount,
  needsSession,
  setAccountStatus,
  updateAccountSession,
} from "@/server/services/accounts";
import { UserError } from "@/server/services/errors";
import { createWorkspace, db, resetDb } from "./helpers";

const SECRET = "p6-bridge-secret";
const NOW = new Date("2026-10-16T08:42:00Z");
const FAILED_AT = new Date("2026-10-15T07:00:00Z");

/** Stands in for Vela's browser (the worker side of the bridge). */
const worker = {
  name: "browser",
  async updateSession(account: AccountRef) {
    return { externalId: account.externalId, fullName: "Alex Martin", headline: "CFO", accountType: "FREE" };
  },
  async diagnose(account: AccountRef) {
    if (account.externalId === "br-expired") throw new ProviderAuthError("Session LinkedIn expirée ou vérification de sécurité demandée.");
    return [
      { check: "Session", ok: true, detail: "connecté en tant que Alex Martin" },
      { check: "Recherche", ok: account.externalId !== "br-changed", detail: "10 profils lus" },
    ];
  },
} as unknown as LinkedInProvider;

let server: Server;
const previousEnv = { port: process.env.LINKEDIN_BRIDGE_PORT, secret: process.env.LINKEDIN_BRIDGE_SECRET };

beforeAll(async () => {
  server = await startBridge(worker, { port: 0, secret: SECRET });
  process.env.LINKEDIN_BRIDGE_SECRET = SECRET;
});

afterAll(async () => {
  await new Promise<void>((resolve) => server.close(() => resolve()));
  for (const [key, value] of [["LINKEDIN_BRIDGE_PORT", previousEnv.port], ["LINKEDIN_BRIDGE_SECRET", previousEnv.secret]] as const) {
    if (value === undefined) delete process.env[key];
    else process.env[key] = value;
  }
});

beforeEach(async () => {
  await resetDb();
  process.env.LINKEDIN_BRIDGE_PORT = String((server.address() as AddressInfo).port);
});

afterEach(() => {
  process.env.LINKEDIN_BRIDGE_PORT = String((server.address() as AddressInfo).port);
});

async function browserAccount(externalId: string, data: Record<string, unknown> = {}) {
  const { workspace } = await createWorkspace();
  const account = await db.linkedInAccount.create({
    data: { workspaceId: workspace.id, provider: "browser", externalId, fullName: "Alex Martin", ...data },
  });
  return { workspace, account };
}

describe("account repair clears old failure alerts", () => {
  it("clears lastError when 'Réactiver' sets the account back to ACTIVE", async () => {
    const { workspace, account } = await createWorkspace();
    await db.linkedInAccount.update({
      where: { id: account.id },
      data: { status: "PAUSED", statusReason: "Mis en pause", lastError: "LinkedIn : page inattendue", lastErrorAt: FAILED_AT },
    });

    await setAccountStatus(workspace.id, account.id, "ACTIVE");

    expect(await db.linkedInAccount.findUniqueOrThrow({ where: { id: account.id } })).toMatchObject({
      status: "ACTIVE",
      statusReason: null,
      lastError: null,
      lastErrorAt: null,
    });
  });

  it("keeps lastError when the account is only paused", async () => {
    const { workspace, account } = await createWorkspace();
    await db.linkedInAccount.update({ where: { id: account.id }, data: { lastError: "LinkedIn : page inattendue", lastErrorAt: FAILED_AT } });

    await setAccountStatus(workspace.id, account.id, "PAUSED");

    expect(await db.linkedInAccount.findUniqueOrThrow({ where: { id: account.id } })).toMatchObject({ status: "PAUSED", lastErrorAt: FAILED_AT });
  });

  it("clears lastError when a new LinkedIn session reactivates the account", async () => {
    const { workspace, account } = await browserAccount("br-renewed", {
      status: "PAUSED",
      statusReason: "Session LinkedIn expirée ou vérification de sécurité demandée : mettez à jour le cookie du compte.",
      lastError: "LinkedIn : page inattendue",
      lastErrorAt: FAILED_AT,
    });

    await updateAccountSession(workspace.id, account.id, "AQEDAR-a-fresh-li-at-cookie-value");

    expect(await db.linkedInAccount.findUniqueOrThrow({ where: { id: account.id } })).toMatchObject({
      status: "ACTIVE",
      statusReason: null,
      lastError: null,
      lastErrorAt: null,
      headline: "CFO",
    });
  });
});

describe("a new LinkedIn session needs a new check", () => {
  it("forgets the previous check result when the session is replaced", async () => {
    const { workspace, account } = await browserAccount("br-new-session", {
      status: "PAUSED",
      statusReason: "Session LinkedIn expirée ou vérification de sécurité demandée : mettez à jour le cookie du compte.",
      lastDiagnosedAt: FAILED_AT,
      lastDiagnosisOk: true,
    });

    await updateAccountSession(workspace.id, account.id, "AQEDAR-a-fresh-li-at-cookie-value");

    expect(await db.linkedInAccount.findUniqueOrThrow({ where: { id: account.id } })).toMatchObject({
      status: "ACTIVE",
      lastDiagnosedAt: null,
      lastDiagnosisOk: null,
    });
  });

  it("keeps it when the same session is only resumed", async () => {
    const { workspace, account } = await browserAccount("br-resumed", { status: "PAUSED", statusReason: null, lastDiagnosedAt: FAILED_AT, lastDiagnosisOk: true });

    await setAccountStatus(workspace.id, account.id, "ACTIVE");

    expect(await db.linkedInAccount.findUniqueOrThrow({ where: { id: account.id } })).toMatchObject({
      status: "ACTIVE",
      lastDiagnosedAt: FAILED_AT,
      lastDiagnosisOk: true,
    });
  });
});

describe("a LinkedIn session to open", () => {
  it("creates a browser account without a cookie as paused, with plain instructions", async () => {
    const { workspace } = await createWorkspace();

    const account = await connectAccount(workspace.id, { provider: "browser", fullName: "Léa Martin", headline: "", accountType: "FREE", sessionCookie: "" });

    expect(account).toMatchObject({ status: "PAUSED", statusReason: SESSION_TO_OPEN_REASON });
    expect(SESSION_TO_OPEN_REASON).toMatch(/^Session LinkedIn à ouvrir/);
    expect(SESSION_TO_OPEN_REASON).not.toMatch(/worker/i);
    // Also read in the header banner, the dashboard and the campaigns, where nothing is "below".
    expect(SESSION_TO_OPEN_REASON).not.toMatch(/ci-dessous/);
    expect(needsSession(account)).toBe(true);
  });

  it("refuses 'Réactiver' until the session is open, and keeps the instructions", async () => {
    const { workspace } = await createWorkspace();
    const account = await connectAccount(workspace.id, { provider: "browser", fullName: "Léa Martin", headline: "", accountType: "FREE", sessionCookie: "" });

    const refused = await setAccountStatus(workspace.id, account.id, "ACTIVE").catch((e: unknown) => e);

    expect(refused).toBeInstanceOf(UserError);
    expect((refused as UserError).message).toMatch(/^Ouvrez d'abord la session LinkedIn/);
    expect(await db.linkedInAccount.findUniqueOrThrow({ where: { id: account.id } })).toMatchObject({ status: "PAUSED", statusReason: SESSION_TO_OPEN_REASON });
  });

  it("also refuses it after an expired session, but still allows pausing or disconnecting", async () => {
    const { workspace, account } = await browserAccount("br-expired-session", { status: "PAUSED", statusReason: "Session LinkedIn expirée" });

    await expect(setAccountStatus(workspace.id, account.id, "ACTIVE")).rejects.toThrow(/Ouvrez d'abord la session LinkedIn/);
    await setAccountStatus(workspace.id, account.id, "DISCONNECTED");
    expect((await db.linkedInAccount.findUniqueOrThrow({ where: { id: account.id } })).status).toBe("DISCONNECTED");
  });

  it("lets other paused accounts be reactivated", async () => {
    const { workspace, account: simulated } = await createWorkspace();
    await db.linkedInAccount.update({ where: { id: simulated.id }, data: { status: "PAUSED", statusReason: "Session LinkedIn expirée" } });
    const { account: real } = await browserAccount("br-paused-by-hand", { workspaceId: workspace.id, status: "PAUSED", statusReason: null });

    expect(needsSession(simulated)).toBe(false);
    await setAccountStatus(workspace.id, simulated.id, "ACTIVE");
    await setAccountStatus(workspace.id, real.id, "ACTIVE");

    expect((await db.linkedInAccount.findUniqueOrThrow({ where: { id: simulated.id } })).status).toBe("ACTIVE");
    expect((await db.linkedInAccount.findUniqueOrThrow({ where: { id: real.id } })).status).toBe("ACTIVE");
  });
});

describe("'Vérifier la connexion LinkedIn' is remembered", () => {
  it("stores a successful check", async () => {
    const { workspace, account } = await browserAccount("br-ok");

    const lines = await diagnoseAccount(workspace.id, account.id, NOW);

    expect(lines.every((line) => line.ok)).toBe(true);
    expect(await db.linkedInAccount.findUniqueOrThrow({ where: { id: account.id } })).toMatchObject({ lastDiagnosedAt: NOW, lastDiagnosisOk: true });
  });

  it("stores a check with unrecognised points as failed", async () => {
    const { workspace, account } = await browserAccount("br-changed", { lastDiagnosedAt: FAILED_AT, lastDiagnosisOk: true });

    const lines = await diagnoseAccount(workspace.id, account.id, NOW);

    expect(lines.filter((line) => !line.ok)).toHaveLength(1);
    expect(await db.linkedInAccount.findUniqueOrThrow({ where: { id: account.id } })).toMatchObject({ lastDiagnosedAt: NOW, lastDiagnosisOk: false });
  });

  it("stores a refused session as a failed check", async () => {
    const { workspace, account } = await browserAccount("br-expired");

    await expect(diagnoseAccount(workspace.id, account.id, NOW)).rejects.toThrow(/LinkedIn a refusé la session/);

    expect(await db.linkedInAccount.findUniqueOrThrow({ where: { id: account.id } })).toMatchObject({ lastDiagnosedAt: NOW, lastDiagnosisOk: false });
  });

  it("keeps the previous result when Vela's browser cannot be reached, and says so without jargon", async () => {
    const { workspace, account } = await browserAccount("br-ok", { lastDiagnosedAt: FAILED_AT, lastDiagnosisOk: true });
    const closed = await startBridge(worker, { port: 0, secret: SECRET });
    const closedPort = (closed.address() as AddressInfo).port;
    await new Promise<void>((resolve) => closed.close(() => resolve()));
    process.env.LINKEDIN_BRIDGE_PORT = String(closedPort);

    const error = await diagnoseAccount(workspace.id, account.id, NOW).catch((e: unknown) => e);

    expect(error).toBeInstanceOf(UserError);
    expect((error as UserError).message).toBe("Vela ne parvient pas à joindre son navigateur LinkedIn. Fermez puis relancez Vela (« npm run local »).");
    expect(await db.linkedInAccount.findUniqueOrThrow({ where: { id: account.id } })).toMatchObject({ lastDiagnosedAt: FAILED_AT, lastDiagnosisOk: true });
  });
});
