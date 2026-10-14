// Tout le contenu modifiable de la vidéo : textes, étages, captures, zones à surligner.
// Les coordonnées sont en pixels des captures d'origine (3200 x 1800 pour le QG desktop).

export const TEXTES = {
  accroche: ['J’ai mis', 'ma vie dans', 'un immeuble', 'd’agents.'],
  etages: {kicker: 'L’immeuble', lignes: ['Chaque étage', 'est un agent.']},
  salles: {kicker: 'Les salles', lignes: ['Chaque salle est', 'un sous-agent.']},
  bureaux: {kicker: 'Les bureaux', lignes: ['Chaque bureau', 'est un projet.']},
  travaux: {kicker: 'Le chantier', lignes: ['Je vois ce qui n’est', 'pas encore branché.']},
  cockpit: {kicker: 'Le cockpit', lignes: ['Chaque action', 'compte.']},
  chute: ['Mon système tourne.', 'Moi, je prospecte.'],
} as const;

export type Etage = {
  numero: string;
  nom: string;
  description: string;
  pourcentage: number;
  statut: 'service' | 'travaux';
  capture: string;
};

// De haut en bas : l'ascenseur descend dans cet ordre.
export const ETAGES: Etage[] = [
  {numero: '3', nom: 'Health', description: 'Entraînement, nutrition, sommeil', pourcentage: 44, statut: 'service', capture: 'captures/02-etage-health.png'},
  {numero: '2', nom: 'Wealth', description: 'En travaux', pourcentage: 0, statut: 'travaux', capture: 'captures/03-etage-wealth.png'},
  {numero: '1', nom: 'Business', description: 'Marketing, Sales, Ops, Follow-up, Finance', pourcentage: 1, statut: 'service', capture: 'captures/04-etage-business.png'},
  {numero: 'RDC', nom: 'SMART', description: 'Inbox, système, carrière, labo', pourcentage: 29, statut: 'service', capture: 'captures/05-etage-rdc.png'},
  {numero: 'S1', nom: 'Life', description: 'En travaux', pourcentage: 0, statut: 'travaux', capture: 'captures/06-etage-life.png'},
];

export const IDX_BUSINESS = 2;
export const IDX_WEALTH = 1;

export const CAPTURES = {
  salleSales: 'captures/07-salle-sales.png',
  travaux: 'captures/08-travaux.png',
  cockpitAujourdhui: 'captures/09-cockpit-aujourdhui.png',
  cockpitProjets: 'captures/10-cockpit-projets.png',
  cockpitAtelier: 'captures/11-cockpit-atelier.png',
  mobileQG: 'captures/12-mobile-qg.png',
  mobileCockpit: 'captures/13-mobile-cockpit.png', // référence du cockpit recréé, non affichée
} as const;

// Capture mobile 12 : l'onglet du rez-de-chaussée s'appelle encore "Main" dans l'app.
// On le renomme comme le brief ("SMART"). Mettre `actif: false` pour garder la capture telle quelle.
export const MOBILE = {w: 1170, h: 2532};
export const ONGLET_RDC_MOBILE = {actif: true, texte: 'SMART', x: 735, y: 2410, w: 133, h: 44, fond: 'rgb(233, 232, 230)', encre: 'rgb(27, 29, 34)', taille: 33};

export const CAPTURE_W = 3200;
export const CAPTURE_H = 1800;

// --- Géométrie de l'immeuble (identique sur les 5 captures d'étage) ---

// Silhouette d'un étage : murs + dalle, avec une marge au-dessus des murs
// pour garder les étiquettes des salles.
export const POLY_ETAGE: ReadonlyArray<readonly [number, number]> = [
  [532, 642],
  [1432, 170],
  [2668, 816],
  [2668, 1095],
  [1767, 1562],
  [545, 925],
];
export const CENTRE_ETAGE = {x: 1600, y: 866};
export const COIN_DROIT = {x: 2700, y: 1000};

// Repère isométrique du sol : (u, v) dans [0, 1]².
const FOND = [1432, 442];
const AXE_U = [1228, 643];
const AXE_V = [-882, 468];
export const uv = (u: number, v: number): [number, number] => [
  FOND[0] + u * AXE_U[0] + v * AXE_V[0],
  FOND[1] + u * AXE_U[1] + v * AXE_V[1],
];
export const zoneUV = (u0: number, u1: number, v0: number, v1: number) =>
  [uv(u0, v0), uv(u1, v0), uv(u1, v1), uv(u0, v1)].map((p) => p.join(',')).join(' ');

// --- Étage Business : salle Sales ---
export const PILLULE_SALES = {x: 1860, y: 638, w: 320, h: 47};
export const CENTRE_SALES = {x: 2045, y: 790};

// Panneau "Sales" (capture 07) : découpe et zones à surligner (coordonnées locales au panneau).
export const PANNEAU = {x: 2320, y: 170, w: 851, h: 1603};
export const SURLIGNAGES_SALES = [
  {x: 22, y: 30, w: 812, h: 160, label: 'Sous-agent'},
  {x: 22, y: 392, w: 812, h: 142, label: 'Projet'},
  {x: 22, y: 566, w: 812, h: 644, label: 'Tâches'},
] as const;
// Bouton "×" de la capture 07, masqué sous le cadre "Sous-agent".
export const BOUTON_FERMER_SALES = {x: 760, y: 22, w: 72, h: 72};

// --- Étage Wealth : pièces en travaux ---
// `etiquette` : centre de l'étiquette d'origine, recouverte par une étiquette lisible sur téléphone.
export const PIECES_WEALTH = [
  {nom: 'Architect', zone: zoneUV(0.05, 0.5, 0.05, 0.44), pillule: {x: 1783, y: 473, w: 125, h: 27}, etiquette: {x: 1687, y: 485, w: 480}},
  {nom: 'Build', zone: zoneUV(0.55, 0.95, 0.05, 0.44), pillule: {x: 2353, y: 780, w: 124, h: 27}, etiquette: {x: 2271, y: 791, w: 443}},
  {nom: 'Run', zone: zoneUV(0.05, 0.95, 0.5, 0.95), pillule: {x: 1627, y: 847, w: 123, h: 26}, etiquette: {x: 1558, y: 858, w: 433}},
] as const;

// Badges "EN TRAVAUX" du panneau (capture 08), coordonnées locales au panneau.
export const BADGES_TRAVAUX = {
  cuisine: {x: 627, y: 359, w: 174, h: 32},
  architect: {x: 627, y: 866, w: 174, h: 31},
  build: {x: 627, y: 1006, w: 174, h: 31},
  run: {x: 627, y: 1147, w: 174, h: 32},
  studio: {x: 627, y: 1373, w: 174, h: 31},
  finance: {x: 627, y: 1480, w: 174, h: 31},
} as const;

// ============================== v2 ==============================

// Étape 1 : les "salles" réelles de l'application, dispersées comme des projets en vrac.
// Données reprises des captures (nombre de projets, tâches faites / total, statut).
export type CarteProjet = {nom: string; etage: number; projets: number; faites: number; total: number; travaux?: boolean; x: number; y: number; r: number};
export const CARTES_PROJETS: CarteProjet[] = [
  {nom: 'Salle de sport', etage: 0, projets: 1, faites: 0, total: 1, x: 300, y: 520, r: -6},
  {nom: 'Cuisine', etage: 0, projets: 1, faites: 0, total: 1, travaux: true, x: 770, y: 600, r: 5},
  {nom: 'Chambre', etage: 0, projets: 1, faites: 2, total: 4, x: 420, y: 760, r: 3},
  {nom: 'Architect', etage: 1, projets: 1, faites: 0, total: 1, travaux: true, x: 790, y: 870, r: -4},
  {nom: 'Build', etage: 1, projets: 1, faites: 0, total: 6, travaux: true, x: 290, y: 970, r: 7},
  {nom: 'Studio Marketing', etage: 2, projets: 4, faites: 1, total: 36, travaux: true, x: 600, y: 1100, r: -3},
  {nom: 'Sales', etage: 2, projets: 1, faites: 0, total: 17, x: 300, y: 1235, r: -8},
  {nom: 'Finance', etage: 2, projets: 2, faites: 0, total: 13, travaux: true, x: 760, y: 1320, r: 6},
  {nom: 'Hall Inbox', etage: 3, projets: 1, faites: 1, total: 11, x: 470, y: 1440, r: 4},
  {nom: 'Labo d’apps', etage: 3, projets: 3, faites: 0, total: 12, x: 280, y: 1580, r: -5},
  {nom: 'Bureau carrière', etage: 3, projets: 1, faites: 1, total: 8, x: 770, y: 1600, r: -2},
  {nom: 'Archives', etage: 4, projets: 1, faites: 0, total: 2, travaux: true, x: 520, y: 1735, r: 6},
];

// Sous-titres de la voix off, découpés pour l'écran. `a` = moment d'apparition (fraction de la phrase).
// Une ligne déjà affichée au même rang dans le carton précédent reste en place.
export type Carton = {id: string; a: number; lignes: string[]};
export const SOUS_TITRES: Carton[] = [
  {id: 'L01', a: 0, lignes: ['J’ai toujours plusieurs', 'projets en même temps.']},
  {id: 'L02', a: 0, lignes: ['Ma santé, mon argent,', 'mon business, mes idées.']},
  {id: 'L03', a: 0, lignes: ['Tout avance en parallèle…']},
  {id: 'L03', a: 0.3, lignes: ['mais je ne savais jamais', 'vraiment où j’en étais,']},
  {id: 'L03', a: 0.7, lignes: ['ni où mettre', 'mon énergie.']},
  {id: 'L04', a: 0, lignes: ['Alors j’ai imaginé ma vie', 'comme un immeuble.']},
  {id: 'L05', a: 0, lignes: ['Un immeuble que je', 'construis, étage par étage.']},
  {id: 'L06', a: 0, lignes: ['Chaque étage, c’est', 'un domaine de ma vie.']},
  {id: 'L07', a: 0, lignes: ['Et chacun est piloté par', 'son propre agent IA.']},
  {id: 'L08', a: 0, lignes: ['À l’intérieur, chaque salle', 'abrite un sous-agent,']},
  {id: 'L08', a: 0.62, lignes: ['avec une mission précise.']},
  {id: 'L09', a: 0, lignes: ['Mes projets ont', 'un objectif.']},
  {id: 'L10', a: 0, lignes: ['Et chaque objectif se', 'découpe en tâches concrètes.']},
  {id: 'L11', a: 0, lignes: ['Chaque fois que j’en valide', 'une, je gagne des crédits.']},
  {id: 'L12', a: 0, lignes: ['Et ces crédits font avancer', 'la construction.']},
  {id: 'L13', a: 0, lignes: ['Chaque jour, je suis', 'mes objectifs.']},
  {id: 'L14', a: 0, lignes: ['Je vois les chantiers', 'en cours…']},
  {id: 'L15', a: 0, lignes: ['…et les domaines qui ont', 'besoin de plus d’attention.']},
  {id: 'L16', a: 0, lignes: ['Je ne gère plus', 'seulement des tâches.']},
  {id: 'L17', a: 0, lignes: ['Je vois ce que je construis.']},
  {id: 'L17', a: 0.5, lignes: ['Je vois ce que je construis.', 'Et je sais où j’en suis.']},
  {id: 'L18', a: 0, lignes: ['Je joue au jeu de la vie.']},
  {id: 'L19', a: 0, lignes: ['Je joue au jeu de la vie.', 'Et chaque action me rapproche', 'de l’immeuble que je veux', 'construire.']},
];

// Surtitre de chaque étape du récit.
export const ETAPES: Record<number, string> = {
  1: 'Le point de départ',
  2: 'L’idée',
  3: 'L’organisation',
  4: 'La mécanique',
  5: 'Le suivi',
  6: 'Le sens',
};

// L'avatar du joueur sur la capture du rez-de-chaussée (05) : centre, silhouette, étiquette.
export const DAOUDA = {
  centre: {x: 1472, y: 640},
  masque: [
    {x: 1432, y: 556, w: 100, h: 164},
    {x: 1412, y: 508, w: 124, h: 44},
    {x: 1500, y: 640, w: 80, h: 80},
  ],
  sol: '#dfe0e4',
};

// Panneau Sales (capture 07) en v2 : zones en coordonnées locales au panneau.
export const SALES_V2 = {
  objectif: {x: 22, y: 392, w: 812, h: 142},
  taches: {x: 22, y: 566, w: 812, h: 490},
  case: {x: 73, y: 720, w: 36, h: 36}, // case à cocher de la première tâche
  ligne: {x: 110, y: 708, w: 720, h: 128}, // texte de la première tâche
  credits: {x: 516, y: 801, w: 103, h: 26}, // « +30 crédits » de la première tâche
};
// Compteur de la pastille « Sales 1 proj. · 0/17 » sur la capture de l'étage Business.
export const COMPTEUR_SALES = {x: 2104, y: 647, w: 62, h: 32};
