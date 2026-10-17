import { readFileSync } from "node:fs";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { beforeEach, describe, expect, it } from "vitest";
import { CampaignForm, type CampaignFormAccount, type CampaignFormValues } from "@/app/(app)/campaigns/campaign-form";
import { DEFAULT_FIRST_MESSAGE, DEFAULT_FOLLOW_UPS, DEFAULT_INVITE_NOTE } from "@/server/domain/campaign-defaults";
import { sequenceTimeline } from "@/server/domain/followups";
import { TEMPLATE_VARIABLES, VARIABLE_LABELS_FR, countVariants, suggestVariable, unknownVariables } from "@/server/domain/templates";
import {
  CampaignFieldError,
  SEARCH_TARGETING_MESSAGE,
  campaignSchema,
  createCampaign,
  parseCampaignForm,
  setCampaignStatus,
} from "@/server/services/campaigns";
import { createCampaign as createTestCampaign, createWorkspace, db, resetDb } from "./helpers";

beforeEach(resetDb);

/** What the builder submits (FormData entries), with a valid targeting. */
const form = {
  name: "DAF Lyon",
  accountId: "acc",
  sources: ["SEARCH"],
  titles: '["CFO"]',
  keywords: "[]",
  industries: "[]",
  locations: "[]",
  companySizes: [],
  signals: [],
  postUrls: "[]",
  searchUrl: "",
  exclusions: "[]",
  minScore: "60",
  weeklyProspectTarget: "100",
  offer: "",
  persona: "",
  inviteNote: "",
  firstMessage: DEFAULT_FIRST_MESSAGE,
  followUps: JSON.stringify(DEFAULT_FOLLOW_UPS),
  setterMode: "APPROVAL",
  bookingUrl: "",
};

function fieldErrors(data: Record<string, unknown>) {
  const result = parseCampaignForm(data);
  if (!("state" in result)) throw new Error("expected the form to be rejected");
  return result.state?.fieldErrors ?? {};
}

describe("templates", () => {
  it("catches variables a French speaker would type, accents included", () => {
    expect(unknownVariables("Bonjour {{prénom}} de {{ entreprise }} {{firstName}}")).toEqual(["prénom", "entreprise"]);
    expect(unknownVariables("{{{firstName}}|Bonjour}")).toEqual([]);
  });

  it("suggests the variable that was meant", () => {
    expect(suggestVariable("prenom")).toBe("firstName");
    expect(suggestVariable("Prénom")).toBe("firstName");
    expect(suggestVariable("FirstName")).toBe("firstName");
    expect(suggestVariable("entreprise")).toBe("company");
    expect(suggestVariable("lien_rdv")).toBe("bookingUrl");
    expect(suggestVariable("xyz")).toBeNull();
  });

  it("labels every variable in French", () => {
    expect(Object.keys(VARIABLE_LABELS_FR).sort()).toEqual([...TEMPLATE_VARIABLES].sort());
    expect(VARIABLE_LABELS_FR.firstName).toBe("Prénom");
  });

  it("counts spintax variants, nested groups included", () => {
    expect(countVariants("Bonjour {{firstName}}")).toBe(1);
    expect(countVariants("{Bonjour|Salut} {{firstName}}, {a|b|c}")).toBe(6);
    expect(countVariants("{Bonjour {{firstName}}|{Hello|Hi} {{firstName}}}")).toBe(3);
    expect(countVariants(DEFAULT_FIRST_MESSAGE)).toBe(4);
  });
});

describe("default and demo templates", () => {
  it("send no invitation note by default and use French, gender-neutral wording", () => {
    expect(DEFAULT_INVITE_NOTE).toBe("");
    const seed = readFileSync("prisma/seed.ts", "utf8");
    for (const text of [DEFAULT_FIRST_MESSAGE, ...DEFAULT_FOLLOW_UPS.map((f) => f.template), seed]) {
      expect(text).not.toMatch(/Merci pour la connexion|Hello|\bravie?\b/);
    }
    expect(DEFAULT_FIRST_MESSAGE.startsWith("Merci d'avoir accepté mon invitation, {{firstName}} !")).toBe(true);
    expect(unknownVariables(DEFAULT_FIRST_MESSAGE)).toEqual([]);
  });

  it("follow-up delays add up: the default 3/5 cadence reaches J+3 and J+8", () => {
    expect(sequenceTimeline(DEFAULT_FOLLOW_UPS).map((t) => t.dayFromFirst)).toEqual([3, 8]);
  });
});

describe("campaign form validation", () => {
  it("names the unknown variable, keyed to its field", () => {
    const errors = fieldErrors({ ...form, firstMessage: "Bonjour {{prenom}}" });
    expect(errors.firstMessage).toBe("Premier message : variable inconnue {{prenom}}. Utilisez une des variables listées.");
  });

  it("keys follow-up errors by step so they show under the matching Relance", () => {
    const followUps = JSON.stringify([
      { delayDays: 3, template: "" },
      { delayDays: 5, template: "Chez {{entreprise}} ?" },
    ]);
    const errors = fieldErrors({ ...form, followUps });
    expect(errors["followUps.0"]).toBe("Relance 1 : texte requis");
    expect(errors["followUps.1"]).toBe("Relance 2 : variable inconnue {{entreprise}}. Utilisez une des variables listées.");
    expect(errors.followUps).toBeUndefined();
  });

  it("refuses a search with nothing to search for, alongside the other errors", () => {
    const errors = fieldErrors({ ...form, name: "", titles: "[]" });
    expect(errors.titles).toBe(SEARCH_TARGETING_MESSAGE);
    expect(errors.name).toBe("Nom requis");
  });

  it("accepts a search URL, a keyword or a source that is not a search instead of titles", () => {
    const searchUrl = "https://www.linkedin.com/search/results/people/?keywords=cfo";
    expect(campaignSchema.safeParse({ ...form, titles: "[]", searchUrl }).success).toBe(true);
    expect(campaignSchema.safeParse({ ...form, titles: "[]", keywords: '["reporting"]' }).success).toBe(true);
    expect(campaignSchema.safeParse({ ...form, titles: "[]", sources: ["PROFILE_VISITORS"] }).success).toBe(true);
  });

  it("still rejects a search URL that is not a LinkedIn people search, on the URL field only", () => {
    const errors = fieldErrors({ ...form, searchUrl: "https://example.com/x", titles: "[]" });
    expect(errors.searchUrl).toMatch(/linkedin\.com\/search\/results\/people/);
    expect(errors.titles).toBeUndefined();
  });
});

describe("campaign service", () => {
  it("keeps offer, persona and booking link empty so the settings apply", async () => {
    const { workspace, account } = await createWorkspace();
    const parsed = campaignSchema.parse({ ...form, accountId: account.id });
    const created = await createCampaign(workspace.id, parsed);
    expect(created).toMatchObject({ offer: "", persona: "", bookingUrl: "", inviteNote: null, status: "DRAFT" });
  });

  it("reports a disconnected account on the account field", async () => {
    const { workspace, account } = await createWorkspace();
    await db.linkedInAccount.update({ where: { id: account.id }, data: { status: "DISCONNECTED" } });
    const parsed = campaignSchema.parse({ ...form, accountId: account.id });
    const error = await createCampaign(workspace.id, parsed).catch((e: unknown) => e);
    expect(error).toBeInstanceOf(CampaignFieldError);
    expect(error).toMatchObject({ field: "accountId" });
  });

  it("refuses to launch on an inactive account or without search targeting", async () => {
    const { workspace, account } = await createWorkspace();
    const campaign = await createTestCampaign(workspace.id, account.id, { status: "DRAFT", sources: ["SEARCH"], titles: [], keywords: [], searchUrl: "" });

    await expect(setCampaignStatus(workspace.id, campaign.id, "ACTIVE")).rejects.toThrow(SEARCH_TARGETING_MESSAGE);

    await db.campaign.update({ where: { id: campaign.id }, data: { keywords: ["reporting"] } });
    await db.linkedInAccount.update({ where: { id: account.id }, data: { status: "PAUSED" } });
    await expect(setCampaignStatus(workspace.id, campaign.id, "ACTIVE")).rejects.toThrow(
      "Le compte LinkedIn de cette campagne n'est pas actif : réparez-le dans Comptes LinkedIn.",
    );

    await db.linkedInAccount.update({ where: { id: account.id }, data: { status: "ACTIVE" } });
    await setCampaignStatus(workspace.id, campaign.id, "ACTIVE");
    expect((await db.campaign.findUniqueOrThrow({ where: { id: campaign.id } })).status).toBe("ACTIVE");
  });
});

describe("campaign builder markup", () => {
  const values: CampaignFormValues = {
    name: "",
    accountId: "real",
    sources: ["SEARCH"],
    titles: [],
    keywords: [],
    industries: [],
    locations: [],
    companySizes: [],
    signals: [],
    postUrls: [],
    searchUrl: "",
    exclusions: [],
    aiPersonalization: true,
    minScore: 60,
    weeklyProspectTarget: 100,
    offer: "",
    persona: "",
    inviteNote: DEFAULT_INVITE_NOTE,
    firstMessage: DEFAULT_FIRST_MESSAGE,
    followUps: DEFAULT_FOLLOW_UPS,
    setterMode: "APPROVAL",
    bookingUrl: "",
  };
  const accounts: CampaignFormAccount[] = [
    { id: "real", fullName: "Léa Martin", provider: "browser", accountType: "FREE", status: "ACTIVE" },
    { id: "sim", fullName: "Alex Test", provider: "simulator", accountType: "PREMIUM", status: "ACTIVE" },
  ];
  const workspace = { offer: "Nous automatisons le reporting.", persona: "DAF de PME", bookingUrl: "https://cal.example.com/lea" };
  const render = (overrides: Partial<CampaignFormValues> = {}, campaignId: string | null = null) =>
    renderToStaticMarkup(createElement(CampaignForm, { aiEnabled: false, campaignId, accounts, workspace, values: { ...values, ...overrides } }));

  it("disables buying signals for a real account and explains why", () => {
    const html = render();
    expect(html).toContain("Pas encore disponible avec un vrai compte LinkedIn");
    const signals = /<input[^>]*value="SIGNALS"[^>]*>/.exec(html)?.[0] ?? "";
    expect(signals).toContain('disabled=""');
    expect(signals).not.toContain("checked");
    expect(html).toContain("Utilisés pour la note, pas pour la recherche LinkedIn");
  });

  it("shows the real cadence, French variable chips and an opt-in invitation note", () => {
    const html = render();
    expect(html).toContain("J+3 relance 1");
    expect(html).toContain("J+8 relance 2");
    expect(html).toContain("J+15 sans réponse");
    expect(html).toContain("Relance 2 · J+8");
    expect(html).toContain("2 sur 8 possibles · elles s&#x27;arrêtent dès que le prospect répond");
    expect(html).toContain(">Prénom</button>");
    expect(html).toContain("Ajouter une note à l&#x27;invitation");
    expect(html).toContain('<input type="hidden" name="inviteNote" value=""/>');
    expect(html).not.toContain('id="inviteNote"');
  });

  it("puts settings in placeholders, previews the settings booking link and the chosen account's name", () => {
    const html = render({ firstMessage: "{{senderFirstName}} · {{bookingUrl}}" });
    expect(html).toContain('placeholder="Nous automatisons le reporting."');
    expect(html).toContain("Laissez vide pour utiliser celle des Réglages");
    expect(html).toContain("Léa · https://cal.example.com/lea");
  });

  it("links the sections and keeps the save button in a sticky bar with a way out", () => {
    const html = render({}, "c1");
    for (const id of ["general", "ciblage", "offre", "sequence", "setter"]) {
      expect(html).toContain(`id="${id}"`);
      expect(html).toContain(`href="#${id}"`);
    }
    expect(html).toContain('href="/campaigns/c1"');
    expect(html).toContain("sticky bottom-(--mobile-nav-h)");
    expect(html).not.toMatch(/<form[^>]*action=/);
  });

  it("asks for another account instead of silently picking one", () => {
    const html = render({ accountId: "" });
    expect(html).toContain('<option value="" disabled="" selected="">Choisissez un compte</option>');
  });
});
