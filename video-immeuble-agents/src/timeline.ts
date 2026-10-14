// Repères temporels (en images, 30 i/s). Toute la chorégraphie part d'ici.
import type {Cle} from './anim';

export const FPS = 30;
export const DUREE_TOTALE = 1215; // 40,5 s

// 1. Accroche
export const ACCROCHE = {sortie: 78};

// 2. L'immeuble se construit, puis la caméra descend avec l'ascenseur
export const TOUR = {debut: 92, decalage: 9, chute: 20};
export const chuteEtage = (i: number) => TOUR.debut + (4 - i) * TOUR.decalage; // S1 d'abord, Health en dernier
export const PLONGEE = {debut: 180, fin: 205};
export const ARRETS = [205, 240, 277, 314, 351]; // arrivée de la caméra sur chaque étage
export const TRAJET = 12; // durée d'un trajet d'ascenseur

// 3. Une salle s'ouvre
export const SALLE = {remontee: [375, 398], zoom: [400, 432], anneau: 428, panneau: 446, surlignages: [480, 500, 520], defile: 520, sortie: 552};

// 4. Les pièces en travaux
export const TRAVAUX = {transition: [556, 594], clignotes: [600, 616, 632], tous: [664, 722], panneau: 650, marqueur: 670, cuisine: 680, defile: 690, sortie: 752};

// 5. Tableau de bord
export const COCKPIT = {
  entree: 752,
  bascules: [806, 834], // Projets -> Atelier -> Aujourd'hui
  zoom: 850,
  morphose: 868,
  vecteur: 886,
  invitations: [916, 928, 940],
  relances: [952],
  commentaires: [966, 972, 978, 984, 990],
  post: [1004],
  serie: [954],
  sortie: 1035,
};

// 6. Fin
export const FIN = {telephone: 1042, ligne1: 1066, ligne2: 1088, recentrage: 1150};

// Légendes du haut d'écran
export const LEGENDES = {
  etages: [100, 370],
  salles: [380, 462],
  bureaux: [472, 552],
  travaux: [562, 744],
  cockpit: [758, 1030],
} as const;

// Étage visé par la caméra (0 = Health ... 4 = Life), valeur continue.
export const clesEtage: Cle[] = (() => {
  const cles: [number, number][] = [
    [0, 2],
    [PLONGEE.debut, 2],
    [PLONGEE.fin, 0],
  ];
  for (let k = 1; k < ARRETS.length; k++) cles.push([ARRETS[k] - TRAJET, k - 1], [ARRETS[k], k]);
  cles.push([SALLE.remontee[0], 4], [SALLE.remontee[1], 2], [TRAVAUX.transition[0], 2], [TRAVAUX.transition[1], 1]);
  return cles;
})();
