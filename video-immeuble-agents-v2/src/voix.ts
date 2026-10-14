// Voix off : le montage se cale sur la durée réelle de chaque phrase (public/voix/durees.json).
// Pour enregistrer votre propre voix : déposez L01.wav ... L19.wav dans public/voix/,
// lancez `bash outils/mesurer-voix.sh`, puis relancez le rendu. Tout se recale seul.
import script from '../voix-off/script.json';
import durees from '../public/voix/durees.json';

export const FPS = 30;

export type LigneVO = {id: string; etape: number; texte: string; prononciation: string};
export const LIGNES = script as LigneVO[];
const DUREES = durees as Record<string, number>;

// Durée minimale (s) qu'il faut à l'image pour illustrer chaque phrase (les fichiers audio sont rognés, sans silence).
const MINIMUM: Record<string, number> = {
  L01: 2.0, L02: 3.0, L03: 4.6, L04: 2.4, L05: 2.8, L06: 2.2, L07: 2.7, L08: 4.1, L09: 2.0, L10: 2.5,
  L11: 2.6, L12: 2.8, L13: 2.9, L14: 1.6, L15: 2.3, L16: 1.8, L17: 2.9, L18: 1.3, L19: 0,
};
const DEBUT = 0.4; // les cartes projets apparaissent avant la première phrase
const PAUSE = 0.12; // entre deux phrases d'une même étape
const PAUSE_ETAPE = 0.35; // entre deux étapes du récit
const TENUE_FINALE = 1.9; // plan final sur l'avatar, sans texte

export type Repere = {debut: number; finVoix: number; fin: number; duree: number};

export const R: Record<string, Repere> = (() => {
  const r: Record<string, Repere> = {};
  let t = DEBUT;
  let etape = LIGNES[0].etape;
  for (const l of LIGNES) {
    if (l.etape !== etape) {
      t += PAUSE_ETAPE - PAUSE;
      etape = l.etape;
    }
    const d = DUREES[l.id] ?? 3;
    const creneau = Math.max(d, MINIMUM[l.id] ?? 0);
    r[l.id] = {
      debut: Math.round(t * FPS),
      finVoix: Math.round((t + d) * FPS),
      fin: Math.round((t + creneau) * FPS),
      duree: Math.round(d * FPS),
    };
    t += creneau + PAUSE;
  }
  return r;
})();

// Image située à une fraction de la phrase (0 = premier mot, 1 = dernier mot).
export const a = (id: string, fraction: number) => Math.round(R[id].debut + fraction * R[id].duree);

export const DUREE_TOTALE = R.L19.finVoix + Math.round(TENUE_FINALE * FPS);
