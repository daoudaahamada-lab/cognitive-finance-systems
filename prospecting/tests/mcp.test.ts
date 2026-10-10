import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import { beforeEach, describe, expect, it } from "vitest";
import { POST } from "@/app/api/mcp/route";
import { HOUR } from "@/server/domain/time";
import { runTick } from "@/server/engine/tick";
import { createToken, revokeToken } from "@/server/services/tokens";
import { createCampaign, createWorkspace, db, deps, resetDb } from "./helpers";

beforeEach(resetDb);

/** An MCP client whose HTTP requests go straight to the route handler (no network). */
async function connect(token: string) {
  const transport = new StreamableHTTPClientTransport(new URL("http://vela.test/api/mcp"), {
    requestInit: { headers: { Authorization: `Bearer ${token}` } },
    fetch: (url, init) => POST(new Request(url, init)),
  });
  const client = new Client({ name: "test", version: "1.0.0" });
  await client.connect(transport);
  return client;
}

async function setup() {
  const { workspace, account } = await createWorkspace();
  const user = await db.user.create({ data: { email: `u${Date.now()}@example.com`, name: "Alex", passwordHash: "x", memberships: { create: { workspaceId: workspace.id } } } });
  const { token, record } = await createToken(workspace.id, user.id, "Claude Code");
  return { workspace, account, user, token, tokenId: record.id };
}

function data(result: Awaited<ReturnType<Client["callTool"]>>) {
  const content = result.content as { type: string; text: string }[];
  return JSON.parse(content[0]!.text);
}

describe("MCP server", () => {
  it("rejects missing, unknown and revoked tokens", async () => {
    const { workspace, token, tokenId } = await setup();
    const call = (auth?: string) =>
      POST(new Request("http://vela.test/api/mcp", {
        method: "POST",
        headers: { "content-type": "application/json", accept: "application/json, text/event-stream", ...(auth ? { authorization: auth } : {}) },
        body: JSON.stringify({ jsonrpc: "2.0", id: 1, method: "tools/list" }),
      }));
    expect((await call()).status).toBe(401);
    expect((await call("Bearer vela_nope")).status).toBe(401);
    await revokeToken(workspace.id, tokenId);
    expect((await call(`Bearer ${token}`)).status).toBe(401);
  });

  it("lists its tools with safety annotations", async () => {
    const { token } = await setup();
    const client = await connect(token);
    const { tools } = await client.listTools();
    expect(tools.map((t) => t.name).sort()).toEqual([
      "approve_draft", "create_campaign", "get_campaign", "get_conversation", "get_overview", "get_prospect", "hand_back_to_setter",
      "import_prospects", "list_accounts", "list_campaigns", "list_conversations", "list_meetings", "list_prospects", "log_meeting",
      "mark_conversation_handled", "reject_draft", "run_engine", "save_prospect_notes", "send_reply", "set_campaign_status",
      "set_meeting_status", "set_prospect_status", "snooze_prospect", "take_over_conversation", "update_campaign",
    ]);
    const byName = Object.fromEntries(tools.map((t) => [t.name, t]));
    expect(byName.get_overview!.annotations?.readOnlyHint).toBe(true);
    expect(byName.approve_draft!.annotations?.openWorldHint).toBe(true);
    expect(byName.approve_draft!.description).toContain("accord");
    await client.close();
  });

  it("creates, updates and launches a campaign, then reports on it", async () => {
    const { token, account } = await setup();
    const client = await connect(token);

    const created = data(await client.callTool({ name: "create_campaign", arguments: { name: "DAF Lyon", titles: ["CFO"], locations: ["Lyon"] } }));
    expect(created.status).toBe("DRAFT");
    const updated = data(await client.callTool({ name: "update_campaign", arguments: { campaignId: created.id, minScore: 40, exclusions: ["Stagiaire"] } }));
    expect(updated.updated.sort()).toEqual(["exclusions", "minScore"]);
    const campaign = data(await client.callTool({ name: "get_campaign", arguments: { campaignId: created.id } }));
    expect(campaign).toMatchObject({ accountId: account.id, targeting: { titles: ["CFO"], locations: ["Lyon"], minScore: 40, exclusions: ["Stagiaire"] }, setter: { mode: "APPROVAL" } });
    expect(campaign.sequence.followUps.length).toBeGreaterThan(0);

    await client.callTool({ name: "set_campaign_status", arguments: { campaignId: created.id, status: "ACTIVE" } });
    const engine = data(await client.callTool({ name: "run_engine", arguments: {} }));
    expect(engine[0].sourced).toBeGreaterThan(0);
    const overview = data(await client.callTool({ name: "get_overview", arguments: { days: 7 } }));
    expect(overview.kpis.found).toBeGreaterThan(0);
    expect(overview.agents).toBe("règles");

    const invalid = await client.callTool({ name: "update_campaign", arguments: { campaignId: created.id, firstMessage: "Bonjour {{prenom}}" } });
    expect(invalid.isError).toBe(true);
    await client.close();
  });

  it("lets the assistant review and approve setter drafts", async () => {
    const { workspace, account, token } = await setup();
    await createCampaign(workspace.id, account.id, { setterMode: "APPROVAL" });
    let now = new Date("2026-10-05T07:00:00Z");
    for (let i = 0; i < 120 && (await db.draft.count({ where: { status: "PENDING" } })) === 0; i++) {
      await runTick(deps(now), { workspaceId: workspace.id });
      now = new Date(now.getTime() + 2 * HOUR);
    }
    const client = await connect(token);
    const drafts = data(await client.callTool({ name: "list_conversations", arguments: { tab: "drafts" } }));
    expect(drafts.length).toBeGreaterThan(0);
    const thread = data(await client.callTool({ name: "get_conversation", arguments: { conversationId: drafts[0].id } }));
    expect(thread.pendingDraft.id).toBe(drafts[0].pendingDraftId);

    await client.callTool({ name: "approve_draft", arguments: { draftId: thread.pendingDraft.id, editedMessage: "Merci, voici mon agenda." } });
    const after = data(await client.callTool({ name: "get_conversation", arguments: { conversationId: drafts[0].id } }));
    expect(after.messages.at(-1)).toMatchObject({ from: "AI", text: "Merci, voici mon agenda." });
    expect(after.pendingDraft).toBeNull();
    await client.close();
  });

  it("only sees the token's own workspace", async () => {
    const a = await setup();
    const b = await setup();
    const campaign = await createCampaign(b.workspace.id, b.account.id);
    const client = await connect(a.token);
    const result = await client.callTool({ name: "get_campaign", arguments: { campaignId: campaign.id } });
    expect(result.isError).toBe(true);
    expect(data(await client.callTool({ name: "list_campaigns", arguments: {} }))).toEqual([]);
    await client.close();
  });
});
