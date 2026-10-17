import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { CampaignForm, type CampaignFormValues } from "@/app/(app)/campaigns/campaign-form";
import { DEFAULT_FIRST_MESSAGE, DEFAULT_FOLLOW_UPS } from "@/server/domain/campaign-defaults";
import { VARIABLE_LABELS_FR, malformedVariables, suggestVariable } from "@/server/domain/templates";
import { parseCampaignForm } from "@/server/services/campaigns";

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

const many = (n: number, make: (i: number) => string) => JSON.stringify(Array.from({ length: n }, (_, i) => make(i)));

describe("tag list limits", () => {
  it("explains too many or too long tags in French", () => {
    const errors = fieldErrors({
      ...form,
      postUrls: many(11, (i) => `https://www.linkedin.com/posts/post-${i}`),
      exclusions: JSON.stringify(["x".repeat(201)]),
      titles: many(51, (i) => `Poste ${i}`),
      locations: JSON.stringify(["  "]),
    });
    expect(errors.postUrls).toBe("10 posts maximum");
    expect(errors.exclusions).toBe("200 caractères maximum par élément");
    expect(errors.titles).toBe("50 éléments maximum");
    expect(errors.locations).toBe("Élément vide");
    expect(fieldErrors({ ...form, exclusions: many(101, (i) => `terme ${i}`) }).exclusions).toBe("100 éléments maximum");
  });

  it("keeps tampered values in French too", () => {
    const errors = fieldErrors({ ...form, sources: ["XX"], signals: ["YY"], minScore: "abc", setterMode: "Z", titles: "[pas du JSON" });
    expect(errors).toMatchObject({ sources: "Source inconnue", signals: "Signal inconnu", minScore: "Score entre 0 et 100", setterMode: "Choisissez un mode du setter", titles: "Liste invalide" });
    for (const message of Object.values(errors)) expect(message).not.toMatch(/Invalid|expected|Too (big|small)/);
  });
});

describe("single-brace variables", () => {
  it("finds variables written with one brace, and leaves spintax and other text alone", () => {
    expect(malformedVariables("Bonjour {prenom} {firstName}, chez {{company}}")).toEqual(["prenom", "firstName"]);
    expect(malformedVariables("{{title} et { lien }")).toEqual(["title", "lien"]);
    expect(malformedVariables("{Bonjour|Salut} {{firstName}}, {{{firstName}}|vous} {Bonjour}")).toEqual([]);
    expect(malformedVariables(DEFAULT_FIRST_MESSAGE)).toEqual([]);
    for (const step of DEFAULT_FOLLOW_UPS) expect(malformedVariables(step.template)).toEqual([]);
  });

  it("refuses them on save, keyed to the field or the step", () => {
    const followUps = JSON.stringify([{ delayDays: 3, template: "{firstName}, alors ?" }]);
    const errors = fieldErrors({ ...form, firstMessage: "Bonjour {prenom}", followUps });
    expect(errors.firstMessage).toBe("Premier message : variable mal écrite {prenom} : utilisez {{firstName}}.");
    expect(errors["followUps.0"]).toBe("Relance 1 : variable mal écrite {firstName} : utilisez {{firstName}}.");
  });
});

describe("variable suggestions", () => {
  it("understand the chip labels and common English names", () => {
    for (const [variable, label] of Object.entries(VARIABLE_LABELS_FR)) expect(suggestVariable(label)).toBe(variable);
    expect(suggestVariable("Votre lien de réservation")).toBe("bookingUrl");
    expect(suggestVariable("lien_reservation")).toBe("bookingUrl");
    expect(suggestVariable("url")).toBe("bookingUrl");
    expect(suggestVariable("company_name")).toBe("company");
  });
});

describe("campaign builder markup after review", () => {
  const values: CampaignFormValues = {
    name: "",
    accountId: "sim",
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
    inviteNote: "",
    firstMessage: DEFAULT_FIRST_MESSAGE,
    followUps: DEFAULT_FOLLOW_UPS,
    setterMode: "APPROVAL",
    bookingUrl: "",
  };
  const render = (overrides: Partial<CampaignFormValues> = {}) =>
    renderToStaticMarkup(
      createElement(CampaignForm, {
        aiEnabled: false,
        campaignId: null,
        accounts: [{ id: "sim", fullName: "Alex Test", provider: "simulator", accountType: "PREMIUM", status: "ACTIVE" }],
        workspace: { offer: "", persona: "", bookingUrl: "" },
        values: { ...values, ...overrides },
      }),
    );

  it("titles the criteria by what they are used for", () => {
    expect(render()).toContain("Critères de recherche et de note");
    expect(render({ searchUrl: "https://www.linkedin.com/search/results/people/?keywords=cfo" })).toContain("Critères de note (la recherche utilise votre URL)");
    const withoutSearch = render({ sources: ["POST_ENGAGERS", "PROFILE_VISITORS"] });
    expect(withoutSearch).not.toContain("Critères de recherche");
    expect(withoutSearch).toMatch(/<legend[^>]*>Critères de note<\/legend>/);
  });

  it("gives the invitation note toggle a full touch target", () => {
    const toggle = /<label class="([^"]*)"><input type="checkbox"[^>]*aria-describedby="inviteNote-toggle-desc"/.exec(render())?.[1] ?? "";
    expect(toggle.split(" ")).toEqual(expect.arrayContaining(["min-h-9", "max-sm:min-h-11", "pointer-coarse:min-h-11"]));
  });

  it("flags a single-brace variable while typing", () => {
    expect(render({ firstMessage: "Bonjour {prenom}" })).toContain("Variable mal écrite {prenom} : utilisez {{firstName}}.");
  });
});
