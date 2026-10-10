/**
 * Every LinkedIn-specific label and CSS hook in one place (French and English UI).
 * When LinkedIn changes its interface, this is the file to update; run
 * `npm run linkedin:check` to see what still matches.
 */
export const LABELS = {
  connect: /^(se connecter|connect)$/i,
  connectAria: /(invitez?|invite) .+(rejoindre votre réseau|to connect)/i,
  pending: /^(en attente|pending)$/i,
  pendingAria: /(en attente|pending)/i,
  message: /^(message|envoyer un message)$/i,
  messageAria: /^(envoyer un message à|message) .+/i,
  more: /^(plus|more|plus d.actions|more actions)$/i,
  addNote: /(ajouter une note|add a note)/i,
  sendWithoutNote: /(envoyer sans note|send without a note)/i,
  sendInvitation: /^(envoyer|send|envoyer l.invitation|send invitation)$/i,
  send: /^(envoyer|send)$/i,
  closeConversation: /(fermer votre conversation|close your conversation)/i,
  reactions: /(réactions?|reactions?)/i,
  /** Degree badge of a first-level connection ("· 1er", "1st"), matched on its own element. */
  firstDegree: /^[·•\s]*(1er|1st)\s*$/i,
};

/** Text that means LinkedIn refused or limited an action. */
export const WARNINGS = {
  weeklyLimit: /(limite hebdomadaire|weekly invitation limit|weekly limit|trop d.invitations|too many invitations)/i,
  emailRequired: /(adresse e-mail|email address)/i,
  notFound: /(cette page n.existe pas|page doesn.t exist|profil n.est pas disponible|profile is not available)/i,
};

/** URL fragments of pages that mean the session is not usable. */
export const AUTH_WALLS = ["/login", "/uas/login", "/checkpoint", "/authwall", "/signup"];

export const CSS = {
  headline: ".text-body-medium",
  location: ".text-body-small.inline",
  composer: 'div[role="textbox"][contenteditable="true"]',
  threadEvent: ".msg-s-message-list__event",
  messageBody: ".msg-s-event-listitem__body",
};
