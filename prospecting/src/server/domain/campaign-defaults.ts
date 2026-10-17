import type { FollowUpStep } from "./followups";

/** No note by default: invitations without one are often accepted more readily. The note is opt-in in the builder. */
export const DEFAULT_INVITE_NOTE = "";

export const DEFAULT_FIRST_MESSAGE =
  "Merci d'avoir accepté mon invitation, {{firstName}} !\n\n{Je travaille avec|J'accompagne} des équipes comme {{company}} sur un sujet précis. {Comment le gérez-vous aujourd'hui|Est-ce un sujet chez vous en ce moment} ?";

export const DEFAULT_FOLLOW_UPS: FollowUpStep[] = [
  { delayDays: 3, template: "{{firstName}}, je me permets de remonter mon message. {Une idée de la réponse|Qu'en pensez-vous} ?" },
  { delayDays: 5, template: "{Dernier message de ma part|Je ne veux pas insister} {{firstName}} : si le sujet devient d'actualité chez {{company}}, je reste disponible." },
];
