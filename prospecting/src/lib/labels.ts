/** French labels and badge tones for enums, shared by server and client components. */

import type { ActivityType } from "@prisma/client";

/** Semantic badge tones, drawn only from the theme tokens (see components/ui/badge.tsx). */
export type SemanticTone = "neutral" | "strong" | "brand" | "ai" | "success" | "warning" | "danger" | "info";

/** Former colour names, kept as aliases of the semantic tones while pages migrate. */
export type LegacyTone = "gray" | "blue" | "indigo" | "green" | "amber" | "red" | "violet";

export type Tone = SemanticTone | LegacyTone;

export const LEGACY_TONES: Record<LegacyTone, SemanticTone> = {
  gray: "neutral",
  blue: "info",
  indigo: "brand",
  violet: "ai",
  green: "success",
  amber: "warning",
  red: "danger",
};

export function semanticTone(tone: Tone): SemanticTone {
  return tone in LEGACY_TONES ? LEGACY_TONES[tone as LegacyTone] : (tone as SemanticTone);
}

export const STAGE_LABELS: Record<string, { label: string; tone: Tone }> = {
  NEW: { label: "À évaluer", tone: "neutral" },
  QUALIFIED: { label: "Qualifié", tone: "strong" },
  DISQUALIFIED: { label: "Écarté", tone: "neutral" },
  INVITED: { label: "Invité", tone: "brand" },
  CONNECTED: { label: "En relation", tone: "brand" },
  MESSAGED: { label: "En séquence", tone: "brand" },
  REPLIED: { label: "A répondu", tone: "ai" },
  MEETING_BOOKED: { label: "Rendez-vous pris", tone: "success" },
  NOT_INTERESTED: { label: "Pas intéressé", tone: "neutral" },
  UNRESPONSIVE: { label: "Sans réponse", tone: "neutral" },
};

export const CAMPAIGN_STATUS: Record<string, { label: string; tone: Tone }> = {
  DRAFT: { label: "Brouillon", tone: "neutral" },
  ACTIVE: { label: "Active", tone: "success" },
  PAUSED: { label: "En pause", tone: "warning" },
  ARCHIVED: { label: "Archivée", tone: "neutral" },
};

export const ACCOUNT_STATUS: Record<string, { label: string; tone: Tone }> = {
  ACTIVE: { label: "Actif", tone: "success" },
  PAUSED: { label: "En pause", tone: "warning" },
  DISCONNECTED: { label: "Déconnecté", tone: "neutral" },
};

export const ACCOUNT_TYPES: Record<string, string> = {
  FREE: "Gratuit",
  PREMIUM: "Premium",
  SALES_NAVIGATOR: "Sales Navigator",
  RECRUITER: "Recruiter",
};

export const CONVERSATION_STATUS: Record<string, { label: string; tone: Tone }> = {
  AI_ACTIVE: { label: "Setter", tone: "ai" },
  NEEDS_HUMAN: { label: "À traiter", tone: "brand" },
  HUMAN: { label: "Vous avez la main", tone: "strong" },
  CLOSED: { label: "Terminée", tone: "neutral" },
};

export const SETTER_MODES: Record<string, { label: string; description: string }> = {
  AUTO: { label: "Automatique", description: "Le setter répond seul et vous passe la main sur les cas sensibles." },
  APPROVAL: { label: "Validation", description: "Le setter rédige, vous validez chaque réponse avant envoi." },
  OFF: { label: "Désactivé", description: "Toutes les réponses arrivent dans votre boîte, vous répondez." },
};

export const SOURCES: Record<string, { label: string; description: string }> = {
  SEARCH: { label: "Recherche", description: "Profils correspondant à vos critères." },
  SIGNALS: { label: "Signaux d'achat", description: "Nouveau poste, recrutement, levée de fonds. Simulateur uniquement pour l'instant." },
  POST_ENGAGERS: { label: "Engagement sur des posts", description: "Personnes qui likent ou commentent des posts choisis." },
  PROFILE_VISITORS: { label: "Visiteurs de profil", description: "Personnes qui ont visité votre profil." },
  IMPORT: { label: "Import", description: "Liste importée." },
};

export const SIGNALS: Record<string, string> = {
  NEW_ROLE: "Nouveau poste",
  HIRING: "Recrute",
  FUNDRAISING: "Levée de fonds",
  POST_ENGAGEMENT: "Engagement post",
  PROFILE_VISIT: "Visite de profil",
};

export const INTENTS: Record<string, string> = {
  INTERESTED: "Intéressé",
  QUESTION: "Question",
  OBJECTION: "Objection",
  NOT_INTERESTED: "Pas intéressé",
  OUT_OF_OFFICE: "Message d'absence",
  SENSITIVE: "Sensible",
  UNKNOWN: "Non reconnu",
};

export const INTENT_TONES: Record<string, SemanticTone> = {
  INTERESTED: "success",
  QUESTION: "warning",
  OBJECTION: "warning",
  SENSITIVE: "danger",
  NOT_INTERESTED: "neutral",
  OUT_OF_OFFICE: "neutral",
  UNKNOWN: "neutral",
};

export const MEETING_STATUS: Record<string, { label: string; tone: Tone }> = {
  SCHEDULED: { label: "Planifié", tone: "info" },
  COMPLETED: { label: "Effectué", tone: "success" },
  NO_SHOW: { label: "Non honoré", tone: "warning" },
  CANCELED: { label: "Annulé", tone: "neutral" },
};

export const ACTIVITY_LABELS: Record<string, string> = {
  PROSPECT_FOUND: "Prospect trouvé",
  PROSPECT_QUALIFIED: "Qualifié (note suffisante)",
  PROSPECT_DISQUALIFIED: "Écarté (note trop basse)",
  INVITE_SENT: "Invitation envoyée",
  INVITE_ACCEPTED: "Invitation acceptée",
  MESSAGE_SENT: "Premier message envoyé",
  FOLLOW_UP_SENT: "Relance envoyée",
  REPLY_RECEIVED: "Réponse reçue",
  AI_REPLY_SENT: "Réponse du setter envoyée",
  HUMAN_REPLY_SENT: "Réponse manuelle envoyée",
  DRAFT_CREATED: "Réponse proposée par le setter",
  DRAFT_REJECTED: "Réponse proposée refusée",
  ESCALATED: "Passé à un humain",
  MEETING_BOOKED: "Rendez-vous pris",
  MARKED_NOT_INTERESTED: "Marqué pas intéressé",
  MARKED_UNRESPONSIVE: "Séquence terminée sans réponse",
  ACTION_FAILED: "Action LinkedIn impossible",
};

/** Lucide icon names for the activity timeline; components/ui/timeline.tsx maps them to icons. */
export type ActivityIconName =
  | "search" | "star" | "ban" | "user-plus" | "user-check" | "send" | "repeat" | "message-circle"
  | "sparkles" | "reply" | "pen-line" | "x" | "hand" | "calendar-check" | "thumbs-down" | "clock" | "alert";

export type ActivityVisual = { icon: ActivityIconName; tone: SemanticTone };

export const ACTIVITY_VISUALS: Record<string, ActivityVisual> = {
  PROSPECT_FOUND: { icon: "search", tone: "neutral" },
  PROSPECT_QUALIFIED: { icon: "star", tone: "strong" },
  PROSPECT_DISQUALIFIED: { icon: "ban", tone: "neutral" },
  INVITE_SENT: { icon: "user-plus", tone: "brand" },
  INVITE_ACCEPTED: { icon: "user-check", tone: "brand" },
  MESSAGE_SENT: { icon: "send", tone: "brand" },
  FOLLOW_UP_SENT: { icon: "repeat", tone: "brand" },
  REPLY_RECEIVED: { icon: "message-circle", tone: "info" },
  AI_REPLY_SENT: { icon: "sparkles", tone: "ai" },
  HUMAN_REPLY_SENT: { icon: "reply", tone: "brand" },
  DRAFT_CREATED: { icon: "pen-line", tone: "ai" },
  DRAFT_REJECTED: { icon: "x", tone: "neutral" },
  ESCALATED: { icon: "hand", tone: "warning" },
  MEETING_BOOKED: { icon: "calendar-check", tone: "success" },
  MARKED_NOT_INTERESTED: { icon: "thumbs-down", tone: "neutral" },
  MARKED_UNRESPONSIVE: { icon: "clock", tone: "neutral" },
  ACTION_FAILED: { icon: "alert", tone: "danger" },
} satisfies Record<ActivityType, ActivityVisual>;

export const PROVIDER_LABELS: Record<string, string> = {
  browser: "Navigateur",
  simulator: "Simulateur",
};

export const COMPANY_SIZES = ["1-10", "11-50", "51-200", "201-500", "501-1000", "1000+"];

export const WEEKDAYS = [
  { value: 1, label: "Lun" },
  { value: 2, label: "Mar" },
  { value: 3, label: "Mer" },
  { value: 4, label: "Jeu" },
  { value: 5, label: "Ven" },
  { value: 6, label: "Sam" },
  { value: 7, label: "Dim" },
];
