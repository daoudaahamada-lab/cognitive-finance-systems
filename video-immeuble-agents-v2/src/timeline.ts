// Chorégraphie de la v2, entièrement dérivée des phrases de la voix off (voir src/voix.ts).
// R.Lxx.debut = premier mot, R.Lxx.finVoix = dernier mot, a('Lxx', 0.5) = milieu de la phrase.
import type {Cle} from './anim';
import {a, DUREE_TOTALE, FPS, R} from './voix';

export {a, DUREE_TOTALE, FPS, R};

// --- Étape 1 : le problème (pastilles des salles dispersées) ---
export const CARTES = {
  apparition: R.L01.debut - 22, // une pastille toutes les 5 images
  domaines: [a('L02', 0.12), a('L02', 0.33), a('L02', 0.5), a('L02', 0.7)], // santé, patrimoine, business, idées
  desordre: [R.L03.debut, R.L03.fin],
};

// --- Étape 2 : l'idée (les pastilles rejoignent leur étage, l'immeuble se construit étage par étage) ---
const debutTour = a('L04', 0.72);
export const TOUR = {debut: debutTour, decalage: Math.round((a('L05', 0.55) - debutTour) / 4), chute: 20};
export const chuteEtage = (i: number) => TOUR.debut + (4 - i) * TOUR.decalage; // S1 d'abord, Health en dernier

// --- Étape 3 : l'organisation ---
export const ETIQUETTES_TOUR = {entree: R.L06.debut + 4, sortie: R.L06.finVoix + 2};
export const PLONGEE = {debut: R.L07.debut + 2, fin: R.L07.debut + 30};
export const AGENTS = a('L07', 0.5); // « agent IA » : chaque étage reçoit son agent dans l'ascenseur
const d8 = R.L08.debut;
export const TRAJETS = [
  [d8 + 2, d8 + 20], // Health -> Wealth
  [d8 + 26, d8 + 44], // Wealth -> Business
] as const;
const anneau = Math.max(a('L08', 0.42), d8 + 70);
export const SALLE = {
  anneau, // sur « sous-agent »
  zoom: [anneau - 24, anneau + 6],
  panneau: a('L08', 0.6),
  mission: a('L08', 0.74), // « avec une mission précise »
  // --- Étape 4 : la mécanique ---
  objectif: a('L09', 0.5),
  taches: a('L10', 0.55),
  defile: R.L10.debut + 2,
  hud: R.L11.debut - 6,
  coche: a('L11', 0.42),
  sortie: R.L11.finVoix + 10,
  compteurSales: R.L12.debut + 2,
  recul: [R.L12.debut + 26, R.L12.debut + 56],
  niveau: R.L12.debut + 58,
  hudSortie: R.L12.fin - 6,
};
export const CREDITS = {avant: 330, gain: 30, envol: SALLE.coche + 6, arrivee: SALLE.coche + 30};

// --- Étape 5 : le suivi quotidien ---
const d13 = R.L13.debut;
export const COCKPIT = {
  entree: d13 - 12,
  invitations: [d13 + 10, d13 + 16, d13 + 22],
  relances: [d13 + 28],
  serie: [d13 + 34],
  commentaires: [d13 + 36, d13 + 40, d13 + 44, d13 + 48, d13 + 52],
  post: [d13 + 60],
  sortie: R.L14.debut - 10, // fondu enchaîné vers l'étage Wealth de sortie - 12 à sortie + 2
};
export const TRAVAUX = {
  retour: COCKPIT.sortie - 12, // l'étage Wealth apparaît pendant que le cockpit s'efface
  clignotes: [a('L14', 0.02), a('L14', 0.02) + 14, a('L14', 0.02) + 28],
  tous: a('L14', 0.95),
  attention: R.L15.debut - 6, // la carte Ascenseur revient, domaines à surveiller en jaune
  alerte: a('L15', 0.45),
};

// --- Étape 6 : le sens, puis le plan final sur l'avatar ---
export const RECUL = {debut: R.L16.debut - 6, fin: R.L16.debut + 34};
export const POURCENTAGES = {entree: R.L17.debut + 2, sortie: R.L18.debut + 6};
export const FINAL = {
  approche: R.L18.debut + 2, // la caméra part de l'immeuble vers l'avatar, d'un seul mouvement
  bascule: a('L19', 0.28), // l'avatar 3D prend le relais de la capture
  arrivee: R.L19.finVoix, // fin du mouvement sur « construire »
  fin: DUREE_TOTALE,
};

// Étage visé par la caméra du monde (0 = Health ... 4 = Life), valeur continue (avant le plan final).
export const clesEtage: Cle[] = [
  [0, 2],
  [PLONGEE.debut, 2],
  [PLONGEE.fin, 0],
  [TRAJETS[0][0], 0],
  [TRAJETS[0][1], 1],
  [TRAJETS[1][0], 1],
  [TRAJETS[1][1], 2],
  [COCKPIT.sortie - 14, 2],
  [COCKPIT.sortie - 13, 1],
  [RECUL.debut, 1],
  [RECUL.fin, 2],
];
