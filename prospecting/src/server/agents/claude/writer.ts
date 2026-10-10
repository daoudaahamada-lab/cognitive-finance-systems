import * as z from "zod/v4";
import { INVITE_NOTE_MAX } from "@/server/domain/templates";
import { SIGNAL_DESCRIPTIONS } from "../signals";
import { renderStep, type MessageWriter, type WriteInput } from "../writer";
import { AgentUnavailable, claudeClient, logFallback, structuredCall, type ClaudeClient } from "./client";

const MESSAGE_MAX = 2000;

const SYSTEM = `Tu rédiges des messages LinkedIn de prospection B2B au nom d'un commercial. Il a écrit un message de base ; tu l'adaptes à un destinataire précis à partir de son profil.

Règles :
- Garde l'intention, la structure, le ton, la langue, le tutoiement ou vouvoiement et à peu près la longueur du message de base. C'est son message, pas le tien.
- Ajoute au plus un ou deux éléments personnels tirés du profil fourni (poste, entreprise, secteur, signal récent), seulement s'ils rendent le message plus pertinent.
- N'invente jamais de fait, de chiffre, de client, de résultat, d'événement ou de point commun qui ne figure pas dans les informations fournies.
- Si le message de base contient un lien, recopie-le à l'identique. N'ajoute aucun autre lien.
- Pas de flatterie, pas de formule creuse, pas de signature, pas d'emoji sauf si le message de base en contient.
- Rends du texte brut, sans guillemets autour, sans balises ni variables entre accolades. Les retours à la ligne sont permis.
- Une note d'invitation fait au maximum ${INVITE_NOTE_MAX} caractères, espaces compris.`;

const OUTPUT = z.object({ message: z.string() });

const STEP_LABELS: Record<WriteInput["step"]["kind"], string> = {
  invite_note: `note d'invitation (${INVITE_NOTE_MAX} caractères maximum)`,
  first_message: "premier message, envoyé juste après l'acceptation de l'invitation",
  follow_up: "relance, envoyée faute de réponse aux messages précédents",
};

function urls(text: string): string[] {
  return text.match(/https?:\/\/[^\s)>\]]+/gi) ?? [];
}

/** Why a personalized message is unsafe to send, or null when it is fine. */
export function rejectMessage(message: string, base: string, step: WriteInput["step"]): string | null {
  if (!message) return "message vide";
  if (/\{\{|\}\}/.test(message)) return "variable non remplacée";
  const max = step.kind === "invite_note" ? INVITE_NOTE_MAX : MESSAGE_MAX;
  if (message.length > max) return `trop long (${message.length} > ${max})`;
  const allowed = new Set(urls(base));
  const foreign = urls(message).filter((u) => !allowed.has(u));
  if (foreign.length > 0) return `lien ajouté (${foreign[0]})`;
  return null;
}

/**
 * Personalizes the rendered template for one prospect. Anything unusable
 * (error, refusal, invented link, over-long note) sends the rendered template instead.
 */
export class ClaudeWriter implements MessageWriter {
  constructor(private readonly client: ClaudeClient = claudeClient()) {}

  async write(input: WriteInput): Promise<string> {
    const base = renderStep(input);
    if (!input.personalize || !base) return base;

    const p = input.profile;
    const signal = p.signal ? `${SIGNAL_DESCRIPTIONS[p.signal] ?? p.signal}${p.signalDetail ? ` (${p.signalDetail})` : ""}` : "aucun";
    const prompt = [
      `<etape>${STEP_LABELS[input.step.kind]}</etape>`,
      `<offre>\n${input.offer || "(non précisée)"}\n</offre>`,
      `<destinataire>\nPrénom : ${input.vars.firstName}\nPoste : ${p.title}\nTitre du profil : ${p.headline}\nEntreprise : ${p.company}\nSecteur : ${p.industry}\nZone : ${p.location}\nSignal récent : ${signal}\n</destinataire>`,
      `<message_de_base>\n${base}\n</message_de_base>`,
    ].join("\n\n");

    try {
      const { message } = await structuredCall(this.client, { system: SYSTEM, input: prompt, schema: OUTPUT, effort: "medium" });
      const text = message.replace(/\r\n?/g, "\n").trim();
      const problem = rejectMessage(text, base, input.step);
      if (problem) throw new AgentUnavailable(`message refusé par les garde-fous : ${problem}`);
      return text;
    } catch (error) {
      logFallback("writer", error);
      return base;
    }
  }
}
