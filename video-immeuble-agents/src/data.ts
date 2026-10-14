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
  mobileCockpit: 'captures/13-mobile-cockpit.png',
} as const;

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
export const CENTRE_SALES = {x: 1990, y: 790};

// Panneau "Sales" (capture 07) : découpe et zones à surligner (coordonnées locales au panneau).
export const PANNEAU = {x: 2320, y: 170, w: 851, h: 1603};
export const SURLIGNAGES_SALES = [
  {x: 20, y: 22, w: 790, h: 165, label: 'Sous-agent'},
  {x: 22, y: 392, w: 812, h: 138, label: 'Projet'},
  {x: 22, y: 562, w: 812, h: 868, label: 'Tâches'},
] as const;

// --- Étage Wealth : pièces en travaux ---
export const PIECES_WEALTH = [
  {nom: 'Architect', zone: zoneUV(0.05, 0.5, 0.05, 0.44), pillule: {x: 1783, y: 473, w: 125, h: 27}},
  {nom: 'Build', zone: zoneUV(0.55, 0.95, 0.05, 0.44), pillule: {x: 2353, y: 780, w: 124, h: 27}},
  {nom: 'Run', zone: zoneUV(0.05, 0.95, 0.5, 0.95), pillule: {x: 1627, y: 847, w: 123, h: 26}},
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
