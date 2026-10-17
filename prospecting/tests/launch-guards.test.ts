import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import { beforeEach, describe, expect, it } from "vitest";
import { POST } from "@/app/api/mcp/route";
import { setCampaignStatus } from "@/server/services/campaigns";
import { UserError } from "@/server/services/errors";
import { createToken } from "@/server/services/tokens";
import { createCampaign, createWorkspace, db, resetDb } from "./helpers";

beforeEach(resetDb);

async function mcpClient(workspaceId: string) {
  const user = await db.user.create({ data: { email: "owner@example.com", name: "Alex", passwordHash: "x", memberships: { create: { workspaceId } } } });
  const { token } = await createToken(workspaceId, user.id, "Claude Code");
  const transport = new StreamableHTTPClientTransport(new URL("http://vela.test/api/mcp"), {
    requestInit: { headers: { Authorization: `Bearer ${token}` } },
    fetch: (url, init) => POST(new Request(url, init)),
  });
  const client = new Client({ name: "test", version: "1.0.0" });
  await client.connect(transport);
  return client;
}

describe("launch guards", () => {
  it("refuse on the server what the campaign page refuses: a setter with no booking link", async () => {
    const { workspace, account } = await createWorkspace();
    await db.workspace.update({ where: { id: workspace.id }, data: { bookingUrl: "" } });
    const campaign = await createCampaign(workspace.id, account.id, { status: "DRAFT", bookingUrl: "", setterMode: "APPROVAL" });

    const error = await setCampaignStatus(workspace.id, campaign.id, "ACTIVE").catch((e: unknown) => e);
    expect(error).toBeInstanceOf(UserError);
    expect((error as Error).message).toMatch(/Aucun lien de réservation/);
    expect((await db.campaign.findUniqueOrThrow({ where: { id: campaign.id } })).status).toBe("DRAFT");

    await db.workspace.update({ where: { id: workspace.id }, data: { bookingUrl: "https://cal.example.com/demo" } });
    await setCampaignStatus(workspace.id, campaign.id, "ACTIVE");
    expect((await db.campaign.findUniqueOrThrow({ where: { id: campaign.id } })).status).toBe("ACTIVE");
  });

  it("explain over MCP that a search campaign needs targeting, and keep workspace defaults otherwise", async () => {
    const { workspace } = await createWorkspace();
    const client = await mcpClient(workspace.id);

    const refused = await client.callTool({ name: "create_campaign", arguments: { name: "Sans ciblage" } });
    expect(refused.isError).toBe(true);
    expect(JSON.stringify(refused.content)).toContain("Ajoutez au moins un poste ou un mot-clé");

    const created = await client.callTool({ name: "create_campaign", arguments: { name: "DAF", titles: ["CFO"] } });
    expect(created.isError).toBeFalsy();
    const campaign = await db.campaign.findFirstOrThrow({ where: { workspaceId: workspace.id, name: "DAF" } });
    // Empty means "use the workspace's", so a later change in Réglages applies to this campaign too.
    expect(campaign).toMatchObject({ offer: "", persona: "", status: "DRAFT" });
  });
});
