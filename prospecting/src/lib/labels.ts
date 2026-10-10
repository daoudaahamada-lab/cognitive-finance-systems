/** French labels and badge tones for enums, shared by server and client components. */

export type Tone = "gray" | "blue" | "indigo" | "green" | "amber" | "red" | "violet";

export const STAGE_LABELS: Record<string, { label: string; tone: Tone }> = {
  NEW: { label: "À évaluer", tone: "gray" },
  QUALIFIED: { label: "Qualifié", tone: "blue" },
  DISQUALIFIED: { label: "Écarté", tone: "gray" },
  INVITED: { label: "Invité", tone: "indigo" },
  CONNECTED: { label: "Connecté", tone: "violet" },
  MESSAGED: { label: "En séquence", tone: "violet" },
  REPLIED: { label: "A répondu", tone: "amber" },
  MEETING_BOOKED: { label: "RDV réservé", tone: "green" },
  NOT_INTERESTED: { label: "Pas intéressé", tone: "red" },
  UNRESPONSIVE: { label: "Sans réponse", tone: "gray" },
};

export const CAMPAIGN_STATUS: Record<string, { label: string; tone: Tone }> = {
  DRAFT: { label: "Brouillon", tone: "gray" },
  ACTIVE: { label: "Active", tone: "green" },
  PAUSED: { label: "En pause", tone: "amber" },
  ARCHIVED: { label: "Archivée", tone: "gray" },
};

export const ACCOUNT_STATUS: Record<string, { label: string; tone: Tone }> = {
  ACTIVE: { label: "Actif", tone: "green" },
  PAUSED: { label: "En pause", tone: "amber" },
  DISCONNECTED: { label: "Déconnecté", tone: "gray" },
};

export const ACCOUNT_TYPES: Record<string, string> = {
  FREE: "Gratuit",
  PREMIUM: "Premium",
  SALES_NAVIGATOR: "Sales Navigator",
  RECRUITER: "Recruiter",
};

export const CONVERSATION_STATUS: Record<string, { label: string; tone: Tone }> = {
  AI_ACTIVE: { label: "Setter IA", tone: "indigo" },
  NEEDS_HUMAN: { label: "À traiter", tone: "red" },
  HUMAN: { label: "Vous", tone: "blue" },
  CLOSED: { label: "Close", tone: "gray" },
};

export const SETTER_MODES: Record<string, { label: string; description: string }> = {
  AUTO: { label: "Automatique", description: "Le setter répond seul et vous passe la main sur les cas sensibles." },
  APPROVAL: { label: "Validation", description: "Le setter rédige, vous validez chaque réponse avant envoi." },
  OFF: { label: "Désactivé", description: "Toutes les réponses arrivent dans votre boîte, vous répondez." },
};

export const SOURCES: Record<string, { label: string; description: string }> = {
  SEARCH: { label: "Recherche", description: "Profils correspondant à vos critères." },
  SIGNALS: { label: "Signaux d'achat", description: "Nouveau poste, recrutement, levée de fonds." },
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
  OUT_OF_OFFICE: "Absent",
  SENSITIVE: "Sensible",
  UNKNOWN: "Non reconnu",
};

export const MEETING_STATUS: Record<string, { label: string; tone: Tone }> = {
  SCHEDULED: { label: "Planifié", tone: "blue" },
  COMPLETED: { label: "Effectué", tone: "green" },
  NO_SHOW: { label: "Absent", tone: "amber" },
  CANCELED: { label: "Annulé", tone: "gray" },
};

export const ACTIVITY_LABELS: Record<string, string> = {
  PROSPECT_FOUND: "Prospect trouvé",
  PROSPECT_QUALIFIED: "Qualifié par le scoring",
  PROSPECT_DISQUALIFIED: "Écarté par le scoring",
  INVITE_SENT: "Invitation envoyée",
  INVITE_ACCEPTED: "Invitation acceptée",
  MESSAGE_SENT: "Premier message envoyé",
  FOLLOW_UP_SENT: "Relance envoyée",
  REPLY_RECEIVED: "Réponse reçue",
  AI_REPLY_SENT: "Réponse du setter envoyée",
  HUMAN_REPLY_SENT: "Réponse manuelle envoyée",
  DRAFT_CREATED: "Brouillon proposé par le setter",
  DRAFT_REJECTED: "Brouillon refusé",
  ESCALATED: "Passé à un humain",
  MEETING_BOOKED: "Rendez-vous réservé",
  MARKED_NOT_INTERESTED: "Marqué pas intéressé",
  MARKED_UNRESPONSIVE: "Séquence terminée sans réponse",
  ACTION_FAILED: "Action LinkedIn impossible",
};

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
