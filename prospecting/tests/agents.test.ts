import { describe, expect, it } from "vitest";
import { RuleBasedScorer } from "@/server/agents/scorer";
import { RuleBasedSetter, classifyIntent } from "@/server/agents/setter";
import { REPLIES } from "@/server/linkedin/simulator/data";
import type { TemplateVars } from "@/server/domain/templates";

const scorer = new RuleBasedScorer();
const targeting = {
  titles: ["CFO"], keywords: ["reporting"], industries: ["SaaS"], locations: ["Paris"], companySizes: ["11-50"], exclusions: ["Stagiaire"],
};
const prospect = {
  title: "Directeur Administratif et Financier", headline: "DAF chez Nova | reporting", company: "Nova",
  companySize: "11-50", industry: "Logiciels (SaaS)", location: "Paris", signal: "HIRING",
};

describe("RuleBasedScorer", () => {
  it("gives a perfect score to a perfect fit, using title synonyms", () => {
    const r = scorer.score({ prospect, targeting });
    expect(r.score).toBe(100);
    expect(r.reasons.map((x) => x.label)).toContain("Poste ciblé : CFO");
  });

  it("drops points for each missed criterion and explains them", () => {
    const r = scorer.score({ prospect: { ...prospect, location: "Lyon", signal: null }, targeting });
    expect(r.score).toBe(75);
    expect(r.reasons.find((x) => x.label === "Zone hors cible")?.points).toBe(0);
  });

  it("excludes on exclusion keywords", () => {
    const r = scorer.score({ prospect: { ...prospect, title: "Stagiaire finance" }, targeting });
    expect(r.excludedBy).toBe("Stagiaire");
    expect(r.score).toBe(0);
  });

  it("matches short acronyms as whole words only", () => {
    const r = scorer.score({ prospect: { ...prospect, title: "Directory manager", headline: "" }, targeting: { ...targeting, titles: ["CTO"] } });
    expect(r.reasons.find((x) => x.label.startsWith("Poste"))?.points).toBe(0);
  });

  it("is neutral without targeting", () => {
    const empty = { titles: [], keywords: [], industries: [], locations: [], companySizes: [], exclusions: [] };
    expect(scorer.score({ prospect: { ...prospect, signal: null }, targeting: empty }).score).toBe(60);
  });
});

describe("setter intent classification", () => {
  it("recognizes every reply the simulator can produce", () => {
    for (const [intent, samples] of Object.entries(REPLIES)) {
      for (const sample of samples) {
        expect({ sample, intent: classifyIntent(sample) }).toEqual({ sample, intent });
      }
    }
  });

  it("does not read a refusal as interest", () => {
    expect(classifyIntent("Merci mais ça ne m’intéresse pas")).toBe("NOT_INTERESTED");
  });
});

describe("RuleBasedSetter", () => {
  const setter = new RuleBasedSetter();
  const vars: TemplateVars = {
    firstName: "Léa", lastName: "M", company: "Nova", title: "CFO", industry: "SaaS", location: "Paris",
    senderFirstName: "Alex", bookingUrl: "https://cal.example.com/demo",
  };
  const ask = (body: string, extra: Partial<Parameters<typeof setter.decide>[0]> = {}) =>
    setter.decide({
      history: [
        { direction: "OUTBOUND", author: "SEQUENCE", body: "Bonjour Léa" },
        { direction: "INBOUND", author: "PROSPECT", body },
      ],
      vars, offer: "Nous automatisons le reporting financier. En 2 semaines.", prospectStage: "REPLIED", ...extra,
    });

  it("sends the booking link to interested prospects", async () => {
    const d = await ask("Oui avec plaisir, vous avez un créneau ?");
    expect(d.action).toBe("reply");
    if (d.action === "reply") expect(d.message).toContain("https://cal.example.com/demo");
  });

  it("escalates pricing questions and sensitive requests", async () => {
    expect((await ask("C'est quoi le prix ?")).action).toBe("escalate");
    expect((await ask("Supprimez mes données svp (RGPD)")).action).toBe("escalate");
  });

  it("answers general questions with the offer and a link", async () => {
    const d = await ask("Comment ça marche concrètement ?");
    expect(d.action).toBe("reply");
    if (d.action === "reply") {
      expect(d.message).toContain("Nous automatisons le reporting financier.");
      expect(d.message).not.toContain("En 2 semaines");
    }
  });

  it("closes politely on refusal and waits on out-of-office", async () => {
    const no = await ask("Non merci");
    expect(no.action === "reply" && no.closeAfter).toBe(true);
    expect((await ask("Je suis en congés jusqu'au 3")).action).toBe("wait");
  });

  it("escalates when no booking link exists", async () => {
    const d = await setter.decide({
      history: [{ direction: "INBOUND", author: "PROSPECT", body: "Oui, on s'appelle ?" }],
      vars: { ...vars, bookingUrl: "" }, offer: "x", prospectStage: "REPLIED",
    });
    expect(d.action).toBe("escalate");
  });

  it("hands over after too many AI replies", async () => {
    const history = [
      ...Array.from({ length: 4 }, () => ({ direction: "OUTBOUND" as const, author: "AI", body: "..." })),
      { direction: "INBOUND" as const, author: "PROSPECT", body: "Comment ça marche ?" },
    ];
    expect((await setter.decide({ history, vars, offer: "x", prospectStage: "REPLIED" })).action).toBe("escalate");
  });
});
