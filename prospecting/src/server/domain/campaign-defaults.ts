import type { FollowUpStep } from "./followups";

export const DEFAULT_INVITE_NOTE = "{Bonjour|Hello} {{firstName}}, je vois que vous êtes {{title}} chez {{company}}. Je serais ravi d'échanger avec vous !";

export const DEFAULT_FIRST_MESSAGE =
  "Merci pour la connexion {{firstName}} !\n\n{Je travaille avec|J'accompagne} des équipes comme {{company}} sur un sujet précis. {Comment gérez-vous ça aujourd'hui|Est-ce un sujet chez vous en ce moment} ?";

export const DEFAULT_FOLLOW_UPS: FollowUpStep[] = [
  { delayDays: 3, template: "{{firstName}}, je me permets de remonter mon message. {Une idée de la réponse|Qu'en pensez-vous} ?" },
  { delayDays: 5, template: "{Dernier message de ma part|Je ne veux pas insister} {{firstName}} : si le sujet devient d'actualité chez {{company}}, je reste disponible." },
];
