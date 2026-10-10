import { renderTemplate, type TemplateVars } from "@/server/domain/templates";
import { normalize } from "./text";

export type Intent =
  | "INTERESTED"
  | "QUESTION"
  | "OBJECTION"
  | "NOT_INTERESTED"
  | "OUT_OF_OFFICE"
  | "SENSITIVE"
  | "UNKNOWN";

export type ConversationTurn = { direction: "OUTBOUND" | "INBOUND"; author: string; body: string };

export type SetterInput = {
  /** Oldest first; the last turn is the prospect message to answer. */
  history: ConversationTurn[];
  vars: TemplateVars;
  offer: string;
  /** Ideal customer description, for context. */
  persona?: string;
  prospectStage: string;
};

export type AgentName = "rules" | "claude";

export type SetterDecision = { agent: AgentName } & (
  | { action: "reply"; intent: Intent; message: string; rationale: string; closeAfter: boolean }
  | { action: "escalate"; intent: Intent; reason: string }
  | { action: "wait"; intent: Intent; rationale: string }
);

export const INTENTS = ["INTERESTED", "QUESTION", "OBJECTION", "NOT_INTERESTED", "OUT_OF_OFFICE", "SENSITIVE", "UNKNOWN"] as const;

/** Decides what to do with a prospect reply. */
export interface ReplyAgent {
  decide(input: SetterInput): Promise<SetterDecision>;
}

/** After this many setter replies without a booking, a human should look. */
export const MAX_AI_REPLIES = 4;

const PATTERNS: [Exclude<Intent, "UNKNOWN">, RegExp][] = [
  ["SENSITIVE", /\b(rgpd|gdpr|mes donnees|supprimer|suppression|arretez|stop|spam|harcel|avocat|juridique|plainte|unsubscribe|remove me|ne plus me contacter|ne me contactez plus)/],
  ["OUT_OF_OFFICE", /\b(conges|vacances|absent|absente|out of office|de retour le|je reviens vers vous a mon retour|en deplacement|recontactez-moi (la semaine|plus tard|dans))/],
  ["NOT_INTERESTED", /(ne m'interesse pas|pas interesse|non merci|not interested|pas pour nous|no thanks|pas besoin|aucun besoin|pas concerne)/],
  ["INTERESTED", /(un creneau|des creneaux|on s'appelle|s'appeler|en parler|on peut echanger|un appel|un call|rdv|rendez-vous|disponible|dispos?\b|when are you available|happy to chat|let's talk|book a call)/],
  ["QUESTION", /(\?|combien|comment|quel |quelle|quels|prix|tarif|cout|how much|how does|what is|pricing)/],
  ["OBJECTION", /(deja (une|un|des)|pas le (bon )?moment|budget|pas (une|la) priorite|trop cher|pas sur que|already have|not a priority|en interne)/],
  ["INTERESTED", /\b(oui|yes|interesse|interessant|pourquoi pas|volontiers|avec plaisir|carrement|top|go)\b/],
];

export function classifyIntent(text: string): Intent {
  const t = normalize(text);
  for (const [intent, pattern] of PATTERNS) {
    if (pattern.test(t)) return intent;
  }
  return "UNKNOWN";
}

function isPricingQuestion(text: string): boolean {
  return /(prix|tarif|cout|combien ca coute|how much|pricing|devis)/.test(normalize(text));
}

/** First sentence of the offer, for short answers. */
function offerPitch(offer: string): string {
  const sentence = offer.split(/(?<=[.!?])\s/)[0]?.trim() ?? "";
  return sentence.length > 220 ? `${sentence.slice(0, 217)}...` : sentence;
}

/**
 * Deterministic setter: classifies the reply with keyword rules and answers with
 * vetted templates. Anything it cannot handle safely goes to a human.
 */
export class RuleBasedSetter implements ReplyAgent {
  async decide({ history, vars, offer, prospectStage }: SetterInput): Promise<SetterDecision> {
    const last = history[history.length - 1];
    if (!last || last.direction !== "INBOUND") {
      return { agent: "rules", action: "wait", intent: "UNKNOWN", rationale: "Aucun message prospect à traiter." };
    }
    const intent = classifyIntent(last.body);
    const seed = `${vars.firstName}:${history.length}`;
    const render = (template: string) => renderTemplate(template, vars, seed);

    if (prospectStage === "MEETING_BOOKED") {
      return { agent: "rules", action: "escalate", intent, reason: "Le prospect a déjà un rendez-vous : réponse humaine recommandée." };
    }
    const aiReplies = history.filter((t) => t.direction === "OUTBOUND" && t.author === "AI").length;
    if (aiReplies >= MAX_AI_REPLIES && intent !== "NOT_INTERESTED" && intent !== "OUT_OF_OFFICE") {
      return { agent: "rules", action: "escalate", intent, reason: `${aiReplies} réponses IA sans rendez-vous : à reprendre en main.` };
    }

    switch (intent) {
      case "SENSITIVE":
        return { agent: "rules", action: "escalate", intent, reason: "Demande sensible (données personnelles, opposition ou juridique)." };
      case "UNKNOWN":
        return { agent: "rules", action: "escalate", intent, reason: "Réponse non reconnue : le setter préfère ne pas improviser." };
      case "OUT_OF_OFFICE":
        return { agent: "rules", action: "wait", intent, rationale: "Absence : la séquence reprendra dans une semaine." };
      case "NOT_INTERESTED":
        return {
          agent: "rules",
          action: "reply",
          intent,
          closeAfter: true,
          rationale: "Refus clair : on remercie et on n'insiste pas.",
          message: render("{Merci|Merci beaucoup} pour votre retour {{firstName}}, je n'insiste pas. {Belle journée|Bonne continuation} !"),
        };
      case "INTERESTED":
        if (!vars.bookingUrl) {
          return { agent: "rules", action: "escalate", intent, reason: "Prospect intéressé mais aucun lien de réservation n'est configuré." };
        }
        return {
          agent: "rules",
          action: "reply",
          intent,
          closeAfter: false,
          rationale: "Intérêt exprimé : on propose directement un créneau.",
          message: render(
            "{Avec plaisir|Super|Génial} {{firstName}} ! {Voici mon agenda|Je vous laisse choisir un créneau} pour {caler|prévoir} 20 minutes quand ça vous arrange : {{bookingUrl}}",
          ),
        };
      case "QUESTION": {
        if (isPricingQuestion(last.body)) {
          return { agent: "rules", action: "escalate", intent, reason: "Question tarifaire : à traiter par un humain." };
        }
        const pitch = offerPitch(offer);
        if (!pitch || !vars.bookingUrl) {
          return { agent: "rules", action: "escalate", intent, reason: "Question du prospect : pas assez de contexte (offre ou lien) pour répondre." };
        }
        return {
          agent: "rules",
          action: "reply",
          intent,
          closeAfter: false,
          rationale: "Question générale : réponse courte avec l'offre, puis proposition d'appel.",
          message: `${render("{Bonne question|Merci pour la question} {{firstName}}.")} ${pitch} ${render(
            "{Le plus simple|Le plus efficace} est d'en parler 20 minutes, je vous montre concrètement : {{bookingUrl}}",
          )}`,
        };
      }
      case "OBJECTION":
        return {
          agent: "rules",
          action: "reply",
          intent,
          closeAfter: false,
          rationale: "Objection : on reconnaît, on recadre, on propose un échange sans pression.",
          message: render(
            "Je comprends tout à fait {{firstName}}. {Beaucoup|La plupart} des {équipes|dirigeants} avec qui je travaille {avaient la même réserve au départ|étaient dans le même cas}. {Est-ce que 15 minutes pour comparer vous paraîtraient utiles|Ça vaudrait le coup d'en parler 15 minutes} ? Sinon, aucun souci.",
          ),
        };
    }
  }
}
