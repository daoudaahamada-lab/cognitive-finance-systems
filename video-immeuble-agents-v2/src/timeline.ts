// Chorégraphie de la v2, entièrement dérivée des phrases de la voix off (voir src/voix.ts).
// R.Lxx.debut = premier mot, R.Lxx.finVoix = dernier mot, a('Lxx', 0.5) = milieu de la phrase.
import type {Cle} from './anim';
import {a, DUREE_TOTALE, FPS, R} from './voix';

export {a, DUREE_TOTALE, FPS, R};

// --- Étape 1 : le problème (cartes projets dispersées) ---
export const CARTES = {
  apparition: R.L01.debut - 22, // une carte toutes les 5 images
  domaines: [a('L02', 0.0), a('L02', 0.26), a('L02', 0.52), a('L02', 0.76)], // santé, argent, business, idées
  desordre: [R.L03.debut, R.L03.fin],
};

// --- Étape 2 : l'idée (les cartes rejoignent leur étage, l'immeuble se construit) ---
export const TOUR = {debut: a('L04', 0.35), decalage: 10, chute: 20};
export const chuteEtage = (i: number) => TOUR.debut + (4 - i) * TOUR.decalage; // S1 d'abord, Health en dernier

// --- Étape 3 : l'organisation ---
export const ETIQUETTES_TOUR = {entree: R.L06.debut + 4, sortie: R.L07.debut + 2};
export const PLONGEE = {debut: R.L07.debut + 2, fin: R.L07.debut + 30};
export const TRAJETS = [
  [R.L08.debut + 4, R.L08.debut + 24], // Health -> Wealth
  [R.L08.debut + 38, R.L08.debut + 58], // Wealth -> Business
] as const;
export const SALLE = {
  zoom: [R.L08.debut + 70, R.L08.debut + 102],
  anneau: R.L08.debut + 98,
  // --- Étape 4 : la mécanique ---
  panneau: R.L09.debut - 8,
  objectif: a('L09', 0.5),
  taches: a('L10', 0.55),
  defile: R.L10.debut + 2,
  hud: R.L11.debut - 6,
  coche: a('L11', 0.42),
  sortie: R.L12.debut,
  compteurSales: R.L12.debut + 8,
  recul: [R.L12.debut + 18, R.L12.debut + 50],
  niveau: a('L12', 0.62),
  hudSortie: R.L12.fin - 6,
};
export const CREDITS = {avant: 330, gain: 30, envol: SALLE.coche + 6, arrivee: SALLE.coche + 30};

// --- Étape 5 : le suivi quotidien ---
const d13 = R.L13.debut;
export const COCKPIT = {
  entree: d13 - 12,
  invitations: [d13 + 16, d13 + 24, d13 + 32],
  relances: [d13 + 40],
  commentaires: [d13 + 50, d13 + 55, d13 + 60, d13 + 65, d13 + 70],
  post: [d13 + 82],
  serie: [d13 + 46],
  sortie: R.L14.debut - 10,
};
export const TRAVAUX = {
  retour: R.L14.debut - 6, // l'étage Wealth remonte à l'image
  clignotes: [a('L14', 0.02), a('L14', 0.02) + 14, a('L14', 0.02) + 28],
  tous: a('L14', 0.95),
  attention: R.L15.debut - 6, // la carte Ascenseur revient, domaines à surveiller en jaune
  alerte: a('L15', 0.45),
};

// --- Étape 6 : le sens, puis le plan final sur l'avatar ---
export const RECUL = {debut: R.L16.debut - 6, fin: R.L16.debut + 34};
export const POURCENTAGES = {entree: R.L17.debut + 2, sortie: R.L18.debut + 6};
export const FINAL = {
  approche: R.L18.debut + 2, // la caméra part de l'immeuble vers l'avatar
  bascule: a('L19', 0.28), // l'avatar 3D prend le relais de la capture
  arrivee: R.L19.finVoix, // fin du mouvement sur « construire »
  fin: DUREE_TOTALE,
};

// Étage visé par la caméra du monde (0 = Health ... 4 = Life), valeur continue.
export const clesEtage: Cle[] = [
  [0, 2],
  [PLONGEE.debut, 2],
  [PLONGEE.fin, 0],
  [TRAJETS[0][0], 0],
  [TRAJETS[0][1], 1],
  [TRAJETS[1][0], 1],
  [TRAJETS[1][1], 2],
  [COCKPIT.sortie, 2],
  [COCKPIT.sortie + 1, 1],
  [RECUL.debut, 1],
  [RECUL.fin, 2],
  [FINAL.approche, 2],
  [FINAL.bascule, 3],
  [FINAL.arrivee, 2],
];
