import { beforeEach, describe, expect, it, vi } from "vitest";

// The server actions run outside Next here: stub the request context, the cache and the redirect.
vi.mock("@/server/auth/context", () => ({ requireContext: vi.fn() }));
vi.mock("next/cache", () => ({ revalidatePath: vi.fn() }));
vi.mock("next/navigation", () => ({
  redirect: vi.fn((url: string) => {
    throw Object.assign(new Error("NEXT_REDIRECT"), { url });
  }),
}));

import { conversationAction } from "@/app/(app)/inbox/actions";
import { proposalChange } from "@/app/(app)/inbox/compose";
import { idlePane, remainingSummary } from "@/app/(app)/inbox/navigation";
import { requireContext } from "@/server/auth/context";
import { createCampaign, createWorkspace, db, resetDb } from "./helpers";

describe("reply box when the proposal changes underneath", () => {
  const old = { body: "Voici mon lien." };
  const fresh = { body: "Merci, voici un créneau." };

  it("adopts the new proposal while the box still holds the old one, or nothing", () => {
    expect(proposalChange({ body: old.body, previous: old, next: fresh, refused: false })).toEqual({ mode: "proposal", body: fresh.body, newProposal: false, adopted: true });
    expect(proposalChange({ body: "  ", previous: null, next: fresh, refused: false })).toMatchObject({ mode: "proposal", body: fresh.body });
  });

  it("keeps what the user typed, as their own reply, and flags the newer proposal", () => {
    // Writing their own reply when the setter drafts.
    expect(proposalChange({ body: "Bonjour Léa, je vous appelle demain.", previous: null, next: fresh, refused: false })).toEqual({
      mode: "reply",
      body: "Bonjour Léa, je vous appelle demain.",
      newProposal: true,
      adopted: false,
    });
    // Editing a proposal that gets superseded.
    expect(proposalChange({ body: "Voici mon lien, à bientôt.", previous: old, next: fresh, refused: false })).toMatchObject({ mode: "reply", body: "Voici mon lien, à bientôt.", newProposal: true });
    // The proposal disappears for another reason: the text stays, nothing to offer.
    expect(proposalChange({ body: "Mon texte", previous: old, next: null, refused: false })).toMatchObject({ mode: "reply", body: "Mon texte", newProposal: false });
  });

  it("empties the box after « Refuser », even an edited proposal", () => {
    expect(proposalChange({ body: "Voici mon lien, modifié.", previous: old, next: null, refused: true })).toEqual({ mode: "reply", body: "", newProposal: false, adopted: true });
  });
});

describe("inbox right pane with no thread open", () => {
  const counts = { todo: 12, drafts: 0, ai: 3, all: 20 };

  it("nests the proposals inside the to-do count instead of adding them", () => {
    expect(remainingSummary({ todo: 60, drafts: 40 })).toBe("60 à traiter, dont 40 réponses proposées à valider.");
    expect(remainingSummary({ todo: 1, drafts: 1 })).toBe("1 à traiter, dont 1 réponse proposée à valider.");
    expect(remainingSummary({ todo: 12, drafts: 0 })).toBe("12 à traiter.");
    expect(idlePane({ listEmpty: false, q: "", counts: { ...counts, drafts: 4 }, tabEmptyTitle: "" }).description).toBe(
      "12 à traiter, dont 4 réponses proposées à valider.",
    );
  });

  it("says « Tout est traité » only when nothing is left to do", () => {
    // The last proposal of À valider was just approved, but 12 conversations still wait.
    const emptied = idlePane({ listEmpty: true, q: "", counts, tabEmptyTitle: "Aucune réponse à valider" });
    expect(emptied).toEqual({ title: "Aucune réponse à valider", description: "12 conversations restent à traiter.", allDone: false });
    expect(idlePane({ listEmpty: true, q: "", counts: { ...counts, todo: 1 }, tabEmptyTitle: "x" }).description).toBe("1 conversation reste à traiter.");

    const done = idlePane({ listEmpty: true, q: "", counts: { ...counts, todo: 0 }, tabEmptyTitle: "Rien à traiter" });
    expect(done).toMatchObject({ title: "Tout est traité", allDone: true });
    expect(idlePane({ listEmpty: true, q: "Dupont", counts: { ...counts, todo: 0 }, tabEmptyTitle: "" })).toMatchObject({ title: "Aucun résultat", allDone: false });
    expect(idlePane({ listEmpty: true, q: "", counts: { todo: 0, drafts: 0, ai: 0, all: 0 }, tabEmptyTitle: "" })).toEqual({ title: "Aucune conversation pour l'instant", allDone: false });
  });
});

describe("thread actions", () => {
  beforeEach(resetDb);

  async function twoThreads() {
    const { workspace, account } = await createWorkspace();
    vi.mocked(requireContext).mockResolvedValue({ workspace } as never);
    const campaign = await createCampaign(workspace.id, account.id);
    const threads = [];
    for (const n of [1, 2]) {
      const prospect = await db.prospect.create({
        data: {
          workspaceId: workspace.id, campaignId: campaign.id, accountId: account.id,
          externalId: `p${n}`, profileUrl: `https://www.linkedin.com/in/p${n}`, firstName: `Prénom${n}`, lastName: "Test", source: "SEARCH", stage: "REPLIED",
        },
      });
      const conversation = await db.conversation.create({
        data: {
          workspaceId: workspace.id, prospectId: prospect.id, accountId: account.id, status: "AI_ACTIVE", unread: true, lastMessageAt: new Date(),
          messages: { create: [{ direction: "INBOUND", author: "PROSPECT", body: "Dites-m'en plus.", sentAt: new Date() }] },
        },
      });
      threads.push({ prospect, conversation });
    }
    return threads;
  }

  function navForm(next: string) {
    const form = new FormData();
    form.set("tab", "ai");
    form.set("q", "");
    form.set("next", next);
    form.set("name", "Prénom1");
    return form;
  }

  it("« Prendre la main » stays on the thread", async () => {
    const [a, b] = await twoThreads();
    const state = await conversationAction(a!.conversation.id, a!.prospect.id, "take_over", null, navForm(b!.conversation.id));
    expect(state).toMatchObject({ ok: true });
    expect((await db.conversation.findUniqueOrThrow({ where: { id: a!.conversation.id } })).status).toBe("HUMAN");
  });

  it("« Marquer comme traité » still moves on to the next thread of the tab", async () => {
    const [a, b] = await twoThreads();
    await expect(conversationAction(a!.conversation.id, a!.prospect.id, "handled", null, navForm(b!.conversation.id))).rejects.toMatchObject({
      url: `/inbox?tab=ai&c=${b!.conversation.id}&done=Pr%C3%A9nom1&did=handled`,
    });
  });
});
