/** Vocabulary for generated people. Plain, fictional data. */

export const FIRST_NAMES = [
  "Camille", "Julien", "Sarah", "Thomas", "Léa", "Nicolas", "Inès", "Hugo", "Manon", "Antoine",
  "Chloé", "Maxime", "Emma", "Lucas", "Clara", "Mehdi", "Amina", "Karim", "Sofia", "Paul",
  "Laura", "Romain", "Yasmine", "Alexandre", "Pauline", "Benoît", "Nora", "Samuel", "Julie", "Olivier",
  "Fatou", "Adrien", "Mathilde", "Rayan", "Élodie", "David", "Aïcha", "Victor", "Margaux", "Ibrahim",
];

export const LAST_NAMES = [
  "Martin", "Bernard", "Dubois", "Durand", "Lefebvre", "Moreau", "Laurent", "Simon", "Michel", "Garcia",
  "Roux", "Fontaine", "Chevalier", "Robin", "Benali", "Diallo", "Nguyen", "Morel", "Girard", "Mercier",
  "Bonnet", "Lambert", "Faure", "Rousseau", "Blanc", "Guerin", "Haddad", "Perrin", "Masson", "Traoré",
];

export const TITLES = [
  "CEO", "Fondateur", "Co-fondatrice", "Directeur Général", "CFO", "Directeur Administratif et Financier",
  "Head of Sales", "Directeur Commercial", "VP Marketing", "Head of Growth", "CTO", "DRH",
  "Responsable Comptable", "Expert-comptable", "Contrôleur de gestion", "Office Manager",
  "Business Developer", "Consultant", "Product Manager", "Responsable Achats",
];

export const INDUSTRIES = [
  "Logiciels (SaaS)", "Conseil", "Expertise comptable", "E-commerce", "Industrie", "Immobilier",
  "Santé", "Services financiers", "Agence marketing", "Formation", "Logistique", "Recrutement",
];

export const LOCATIONS = [
  "Paris", "Lyon", "Bordeaux", "Lille", "Nantes", "Marseille", "Toulouse", "Rennes",
  "Bruxelles", "Genève", "Montréal", "Casablanca",
];

export const COMPANY_SIZES = ["1-10", "11-50", "51-200", "201-500", "501-1000", "1000+"];

export const COMPANY_PREFIXES = [
  "Nova", "Atlas", "Orion", "Lumen", "Kairos", "Helio", "Vertex", "Altura", "Sirius", "Opale",
  "Cobalt", "Azur", "Nexo", "Pragma", "Solis", "Iris", "Tandem", "Mosaïk", "Boréal", "Quartz",
];

export const COMPANY_SUFFIXES = [
  "Conseil", "Labs", "Group", "Digital", "Finance", "Partners", "Tech", "Solutions", "& Associés", "Studio",
];

export const SIGNAL_DETAILS: Record<string, string[]> = {
  NEW_ROLE: ["A pris ses fonctions il y a 3 semaines", "Nouveau poste depuis le mois dernier"],
  HIRING: ["Recrute 3 commerciaux", "Offre d'emploi publiée cette semaine", "Recrute un(e) DAF"],
  FUNDRAISING: ["Levée de fonds de 2 M€ annoncée", "Série A bouclée récemment"],
  POST_ENGAGEMENT: ["A commenté votre post", "A aimé un post ciblé"],
  PROFILE_VISIT: ["A visité votre profil"],
};

/** What simulated people answer, by intent. */
export const REPLIES: Record<string, string[]> = {
  INTERESTED: [
    "Bonjour, oui ça m'intéresse, on peut en parler ?",
    "Pourquoi pas, vous avez un créneau la semaine prochaine ?",
    "Ça tombe bien, c'est un sujet en ce moment chez nous. On s'appelle ?",
    "Yes, happy to chat. When are you available?",
  ],
  QUESTION: [
    "Merci pour le message. Concrètement, comment ça marche ?",
    "C'est quoi le prix ?",
    "Vous travaillez déjà avec des entreprises de notre taille ?",
    "Intéressant. Combien de temps faut-il pour la mise en place ?",
  ],
  OBJECTION: [
    "On a déjà une solution en interne pour ça.",
    "Pas le bon moment, on est en plein budget.",
    "Je ne suis pas sûr que ce soit une priorité pour nous.",
  ],
  NOT_INTERESTED: [
    "Merci mais ça ne m'intéresse pas.",
    "Non merci, pas pour nous.",
    "Not interested, thanks.",
  ],
  OUT_OF_OFFICE: [
    "Je suis en congés jusqu'au 25, je reviens vers vous à mon retour.",
    "Absent cette semaine, recontactez-moi la semaine prochaine.",
  ],
  SENSITIVE: [
    "Où avez-vous eu mes coordonnées ? Merci de supprimer mes données (RGPD).",
    "Arrêtez de m'envoyer des messages s'il vous plaît.",
    "Je suis avocat de la société, merci de passer par notre service juridique.",
  ],
};
