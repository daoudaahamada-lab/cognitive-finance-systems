import { containsTerm, normalize } from "./text";

export type ScoreInput = {
  /** Echoed back so batched results can be matched to their prospect. */
  id?: string;
  prospect: {
    title: string;
    headline: string;
    company: string;
    companySize: string;
    industry: string;
    location: string;
    signal: string | null;
  };
  targeting: {
    titles: string[];
    keywords: string[];
    industries: string[];
    locations: string[];
    companySizes: string[];
    exclusions: string[];
  };
  /** What the campaign sells and to whom: lets an AI scorer judge fit beyond keywords. */
  context?: { offer: string; persona: string };
};

/** `max` is 0 for qualitative reasons (AI scorer): `points` > 0 then means "in favour". */
export type ScoreReason = { label: string; points: number; max: number };

export type ScoreResult = {
  score: number;
  reasons: ScoreReason[];
  /** Set when an exclusion matched: the prospect must not be contacted. */
  excludedBy: string | null;
  /** One-sentence rationale (AI scorer only). */
  summary?: string | null;
  scoredBy: "rules" | "claude";
};

/** Scores how well profiles fit a campaign; results come back in input order. */
export interface ProspectScorer {
  scoreBatch(inputs: ScoreInput[]): Promise<ScoreResult[]>;
}

const WEIGHTS = { title: 35, keywords: 15, industry: 15, location: 10, companySize: 10, intent: 15 };

/** Common equivalents between French and English job titles. */
const TITLE_SYNONYMS: string[][] = [
  ["cfo", "daf", "directeur administratif et financier", "directrice administrative et financiere", "directeur financier", "directrice financiere", "chief financial officer"],
  ["ceo", "dg", "directeur general", "directrice generale", "chief executive officer", "pdg"],
  ["fondateur", "fondatrice", "co-fondateur", "co-fondatrice", "founder", "co-founder"],
  ["head of sales", "directeur commercial", "directrice commerciale", "vp sales", "sales director"],
  ["drh", "directeur des ressources humaines", "chro", "head of people"],
  ["cto", "directeur technique", "chief technology officer"],
];

function titleVariants(title: string): string[] {
  const wanted = normalize(title);
  const group = TITLE_SYNONYMS.find((g) => g.includes(wanted));
  return group ?? [title];
}

const INTENT_LABELS: Record<string, string> = {
  NEW_ROLE: "Signal : nouveau poste",
  HIRING: "Signal : recrute",
  FUNDRAISING: "Signal : levée de fonds",
  POST_ENGAGEMENT: "A interagi avec un post",
  PROFILE_VISIT: "A visité votre profil",
};

/** Transparent, rule-based scorer: every point comes with a reason shown in the UI. */
export class RuleBasedScorer implements ProspectScorer {
  async scoreBatch(inputs: ScoreInput[]): Promise<ScoreResult[]> {
    return inputs.map((input) => this.score(input));
  }

  /** Exclusion check alone: shared with the AI scorer, which must never override it. */
  exclusion({ prospect, targeting }: ScoreInput): string | null {
    const profileText = [prospect.title, prospect.headline, prospect.company, prospect.industry].join(" | ");
    return targeting.exclusions.find((term) => containsTerm(profileText, term)) ?? null;
  }

  score(input: ScoreInput): ScoreResult {
    const { prospect, targeting } = input;
    const profileText = [prospect.title, prospect.headline, prospect.company, prospect.industry].join(" | ");

    const exclusion = this.exclusion(input);
    if (exclusion) {
      return { score: 0, reasons: [{ label: `Exclu : « ${exclusion} »`, points: 0, max: 0 }], excludedBy: exclusion, scoredBy: "rules" };
    }

    const reasons: ScoreReason[] = [];
    let earned = 0;
    let possible = 0;

    const criterion = (terms: string[], weight: number, matches: (term: string) => boolean, hit: (t: string) => string, miss: string) => {
      if (terms.length === 0) return;
      possible += weight;
      const match = terms.find(matches);
      if (match) {
        earned += weight;
        reasons.push({ label: hit(match), points: weight, max: weight });
      } else {
        reasons.push({ label: miss, points: 0, max: weight });
      }
    };

    criterion(
      targeting.titles, WEIGHTS.title,
      (t) => titleVariants(t).some((v) => containsTerm(`${prospect.title} | ${prospect.headline}`, v)),
      (t) => `Poste ciblé : ${t}`, "Poste hors cible",
    );
    criterion(targeting.keywords, WEIGHTS.keywords, (k) => containsTerm(profileText, k), (k) => `Mot-clé : ${k}`, "Aucun mot-clé");
    criterion(targeting.industries, WEIGHTS.industry, (i) => containsTerm(prospect.industry, i), (i) => `Secteur : ${i}`, "Secteur hors cible");
    criterion(targeting.locations, WEIGHTS.location, (l) => containsTerm(prospect.location, l), (l) => `Zone : ${l}`, "Zone hors cible");
    criterion(targeting.companySizes, WEIGHTS.companySize, (s) => prospect.companySize === s, (s) => `Taille : ${s} salariés`, "Taille hors cible");

    const intentPoints = prospect.signal ? WEIGHTS.intent : 0;
    if (prospect.signal) {
      reasons.push({ label: INTENT_LABELS[prospect.signal] ?? `Signal : ${prospect.signal}`, points: intentPoints, max: WEIGHTS.intent });
    }

    if (possible === 0) {
      // No targeting at all: neutral score, intent still counts.
      return { score: 60 + intentPoints, reasons, excludedBy: null, scoredBy: "rules" };
    }
    possible += WEIGHTS.intent;
    earned += intentPoints;
    return { score: Math.round((100 * earned) / possible), reasons, excludedBy: null, scoredBy: "rules" };
  }
}
