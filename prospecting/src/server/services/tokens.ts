import { createHash, randomBytes } from "node:crypto";
import { z } from "zod";
import { db } from "@/server/db";
import { MINUTE } from "@/server/domain/time";
import { UserError } from "./errors";

const TOKEN_PREFIX = "vela_";
/** lastUsedAt is refreshed at most this often, to avoid a write per MCP call. */
const LAST_USED_RESOLUTION = 5 * MINUTE;

function digest(token: string): string {
  return createHash("sha256").update(token).digest("hex");
}

export const tokenNameSchema = z.object({ name: z.string().trim().min(1, "Donnez un nom au jeton").max(60) });

/** Returns the token in clear once; only its hash is stored. */
export async function createToken(workspaceId: string, userId: string, name: string) {
  const token = `${TOKEN_PREFIX}${randomBytes(32).toString("base64url")}`;
  const record = await db.apiToken.create({
    data: { workspaceId, userId, name, tokenHash: digest(token), prefix: token.slice(0, TOKEN_PREFIX.length + 6) },
  });
  return { token, record };
}

export async function listTokens(workspaceId: string) {
  return db.apiToken.findMany({
    where: { workspaceId, revokedAt: null },
    orderBy: { createdAt: "desc" },
    select: { id: true, name: true, prefix: true, lastUsedAt: true, createdAt: true },
  });
}

export async function revokeToken(workspaceId: string, tokenId: string) {
  const { count } = await db.apiToken.updateMany({ where: { id: tokenId, workspaceId, revokedAt: null }, data: { revokedAt: new Date() } });
  if (count === 0) throw new UserError("Jeton introuvable.");
}

export type TokenIdentity = { workspaceId: string; userId: string; tokenId: string };

/** Resolves a bearer token to its workspace, or null when unknown or revoked. */
export async function authenticateToken(token: string, now = new Date()): Promise<TokenIdentity | null> {
  if (!token.startsWith(TOKEN_PREFIX)) return null;
  const record = await db.apiToken.findUnique({ where: { tokenHash: digest(token) } });
  if (!record || record.revokedAt) return null;
  if (!record.lastUsedAt || now.getTime() - record.lastUsedAt.getTime() > LAST_USED_RESOLUTION) {
    await db.apiToken.update({ where: { id: record.id }, data: { lastUsedAt: now } });
  }
  return { workspaceId: record.workspaceId, userId: record.userId, tokenId: record.id };
}
