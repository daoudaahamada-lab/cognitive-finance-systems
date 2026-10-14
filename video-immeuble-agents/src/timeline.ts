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
export const TRAJET = 20; // durée d'un trajet d'ascenseur

// 3. Une salle s'ouvre
export const SALLE = {
  remontee: [368, 400], // S1 -> étage 1
  zoom: [400, 432],
  anneau: 428,
  panneau: 446,
  surlignages: [462, 490, 504], // Sous-agent, Projet, Tâches
  defile: 510,
  sortie: 552,
};

// 4. Les pièces en travaux : chaque pièce clignote avec son badge dans le panneau
export const TRAVAUX = {
  transition: [556, 594],
  panneau: 596,
  marqueur: 604, // "9 pièces en travaux" passé au surligneur
  defile: 624, // le panneau descend jusqu'à la section Wealth
  clignotes: [658, 678, 698], // Architect, Build, Run
  tous: 718,
  sortiePanneau: 742,
  sortie: 752,
};

// 5. Tableau de bord : captures 10 (Projets) puis 09 (Aujourd'hui), puis compteurs
export const COCKPIT = {
  entree: 754,
  bascule: 822, // Projets -> Aujourd'hui
  zoom: 846,
  morphose: 872,
  vecteur: 880,
  invitations: [916, 928, 940],
  relances: [952],
  commentaires: [966, 972, 978, 984, 990],
  post: [1004],
  serie: [962],
  sortie: 1035, // la carte se replie en téléphone jusqu'à FIN.telephone
};

// 6. Fin
export const FIN = {telephone: 1062, ligne1: 1066, ligne2: 1088, recentrage: 1140};

// Légendes du haut d'écran : la suivante entre au moins 14 images après la sortie de la précédente.
export const LEGENDES = {
  etages: [100, 366],
  salles: [380, 472],
  bureaux: [486, 552],
  travaux: [566, 744],
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
