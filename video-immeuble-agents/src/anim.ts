import {Easing, interpolate} from 'remotion';

export const easeInOut = Easing.bezier(0.65, 0, 0.35, 1);
export const easeOut = Easing.bezier(0.22, 1, 0.36, 1);
export const easeIn = Easing.bezier(0.55, 0, 1, 0.45);
// Courbe plus douce pour les grands déplacements (trajets d'ascenseur, glissements).
export const easeDouce = Easing.bezier(0.45, 0, 0.55, 1);

export type Cle = readonly [frame: number, valeur: number];

// Interpolation par images cles, avec un easing sur chaque segment.
export const piste = (f: number, cles: readonly Cle[], easing = easeInOut): number => {
  if (f <= cles[0][0]) return cles[0][1];
  for (let k = 0; k < cles.length - 1; k++) {
    const [f0, v0] = cles[k];
    const [f1, v1] = cles[k + 1];
    if (f <= f1) {
      if (f1 === f0) return v1;
      return v0 + (v1 - v0) * easing((f - f0) / (f1 - f0));
    }
  }
  return cles[cles.length - 1][1];
};

// Progression 0 -> 1 entre debut et debut + duree.
export const prog = (f: number, debut: number, duree: number, easing = easeOut): number =>
  interpolate(f, [debut, debut + duree], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing,
  });

// Entree puis sortie : 0 -> 1 -> 0.
export const fenetre = (f: number, entree: number, sortie: number, duree = 14): number =>
  Math.min(prog(f, entree, duree), 1 - prog(f, sortie, duree, easeIn));

// Clignotement doux : `nombre` impulsions de `periode` images a partir de `debut`.
export const clignote = (f: number, debut: number, nombre: number, periode: number): number => {
  const phase = (f - debut) / periode;
  if (phase < 0 || phase > nombre) return 0;
  return Math.pow(Math.sin(Math.PI * phase), 2);
};

export const clamp01 = (x: number) => Math.max(0, Math.min(1, x));
