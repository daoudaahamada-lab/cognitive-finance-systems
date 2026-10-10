import * as z from "zod/v4";
import { SIGNAL_DESCRIPTIONS } from "../signals";
import { RuleBasedScorer, type ProspectScorer, type ScoreInput, type ScoreResult } from "../scorer";
import { claudeClient, logFallback, structuredCall, type ClaudeClient } from "./client";

/** Profiles per request: enough to amortize the instructions, small enough to stay precise. */
export const SCORING_BATCH = 20;

const SYSTEM = `Tu es l'analyste de prospection d'une équipe commerciale B2B. Pour chaque profil LinkedIn reçu, tu estimes à quel point la personne correspond au client idéal décrit, c'est-à-dire si elle mérite d'être contactée pour l'offre présentée.

Barème de 0 à 100 :
- 80 à 100 : correspond clairement au client idéal (rôle qui décide ou influence l'achat, type d'entreprise visé).
- 60 à 79 : correspondance probable, un point reste incertain.
- 40 à 59 : correspondance partielle ; à contacter seulement si la cible est large.
- 0 à 39 : hors cible.

Comment juger :
- Appuie-toi uniquement sur les informations fournies. N'invente rien sur la personne ni sur son entreprise.
- Le poste et son pouvoir de décision sur l'offre comptent le plus, puis le type et la taille d'entreprise, puis la zone.
- Les critères de ciblage sont des repères, pas des filtres stricts : un intitulé équivalent (« Directeur financier » pour « CFO », « Founder » pour « Fondateur ») compte comme une correspondance.
- Un signal d'intention (nouveau poste, recrutement, levée de fonds, interaction avec un post, visite de profil) rend le contact plus opportun : il augmente la note d'un profil pertinent, il ne rend pas pertinent un profil hors cible.
- Les exclusions ont déjà été appliquées avant toi : ne les mentionne pas.

Pour chaque profil, renvoie son identifiant, sa note, une synthèse d'une phrase en français, et 2 à 4 raisons courtes (moins de 60 caractères chacune), chacune marquée favorable ou défavorable. Évalue chaque identifiant reçu, sans en omettre ni en ajouter.`;

const OUTPUT = z.object({
  evaluations: z.array(
    z.object({
      id: z.string(),
      score: z.number(),
      summary: z.string(),
      reasons: z.array(z.object({ label: z.string(), favorable: z.boolean() })),
    }),
  ),
});

function list(values: string[]): string {
  return values.length > 0 ? values.join(", ") : "(non précisé)";
}

export function scoringInput(batch: ScoreInput[]): string {
  const first = batch[0]!;
  const t = first.targeting;
  const profiles = batch.map((input, i) =>
    JSON.stringify({
      id: `p${i + 1}`,
      poste: input.prospect.title,
      titre: input.prospect.headline,
      entreprise: input.prospect.company,
      taille: input.prospect.companySize,
      secteur: input.prospect.industry,
      zone: input.prospect.location,
      signal: input.prospect.signal ? (SIGNAL_DESCRIPTIONS[input.prospect.signal] ?? input.prospect.signal) : null,
    }),
  );
  return [
    `<offre>\n${first.context?.offer || "(non précisée)"}\n</offre>`,
    `<client_ideal>\n${first.context?.persona || "(non précisé)"}\n</client_ideal>`,
    `<criteres>\nPostes : ${list(t.titles)}\nSecteurs : ${list(t.industries)}\nZones : ${list(t.locations)}\nTailles d'entreprise : ${list(t.companySizes)}\nMots-clés : ${list(t.keywords)}\n</criteres>`,
    `<profils>\n${profiles.join("\n")}\n</profils>`,
  ].join("\n\n");
}

/**
 * Claude judges fit against the offer and ideal customer, which keyword rules cannot.
 * Exclusions stay deterministic and are applied before Claude sees anything;
 * any profile Claude does not score falls back to the rule-based score.
 */
export class ClaudeScorer implements ProspectScorer {
  private readonly rules = new RuleBasedScorer();

  constructor(private readonly client: ClaudeClient = claudeClient()) {}

  async scoreBatch(inputs: ScoreInput[]): Promise<ScoreResult[]> {
    const results: (ScoreResult | null)[] = inputs.map((input) => {
      const excludedBy = this.rules.exclusion(input);
      return excludedBy ? this.rules.score(input) : null;
    });
    const pending = inputs.map((input, index) => ({ input, index })).filter(({ index }) => results[index] === null);

    for (let start = 0; start < pending.length; start += SCORING_BATCH) {
      const batch = pending.slice(start, start + SCORING_BATCH);
      let evaluations: z.infer<typeof OUTPUT>["evaluations"] = [];
      try {
        ({ evaluations } = await structuredCall(this.client, {
          system: SYSTEM,
          input: scoringInput(batch.map((b) => b.input)),
          schema: OUTPUT,
          effort: "low",
        }));
      } catch (error) {
        logFallback("scorer", error);
      }
      batch.forEach(({ input, index }, i) => {
        const evaluation = evaluations.find((e) => e.id === `p${i + 1}`);
        results[index] = evaluation
          ? {
              score: Math.max(0, Math.min(100, Math.round(evaluation.score))),
              summary: evaluation.summary.trim() || null,
              reasons: evaluation.reasons.slice(0, 4).map((r) => ({ label: r.label.slice(0, 80), points: r.favorable ? 1 : 0, max: 0 })),
              excludedBy: null,
              scoredBy: "claude",
            }
          : this.rules.score(input);
      });
    }
    return results as ScoreResult[];
  }
}
