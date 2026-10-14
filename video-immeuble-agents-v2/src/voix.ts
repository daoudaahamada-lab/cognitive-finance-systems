// Voix off : le montage se cale sur la durée réelle de chaque phrase (public/voix/durees.json).
// Pour enregistrer votre propre voix : déposez L01.wav ... L19.wav dans public/voix/,
// lancez `bash outils/mesurer-voix.sh`, puis relancez le rendu. Tout se recale seul.
import script from '../voix-off/script.json';
import durees from '../public/voix/durees.json';

export const FPS = 30;

export type LigneVO = {id: string; etape: number; texte: string; prononciation: string};
export const LIGNES = script as LigneVO[];
const DUREES = durees as Record<string, number>;

// Durée minimale (s) qu'il faut à l'image pour illustrer chaque phrase.
const MINIMUM: Record<string, number> = {
  L01: 2.9, L02: 4.2, L03: 6.6, L04: 4.2, L05: 3.6, L06: 3.2, L07: 3.9, L08: 6.2, L09: 2.9, L10: 3.4,
  L11: 4.6, L12: 3.9, L13: 5.0, L14: 3.0, L15: 3.4, L16: 2.8, L17: 4.0, L18: 2.0, L19: 4.6,
};
const DEBUT = 1.0; // les cartes projets apparaissent avant la première phrase
const PAUSE = 0.3; // entre deux phrases d'une même étape
const PAUSE_ETAPE = 0.8; // entre deux étapes du récit
const TENUE_FINALE = 3.0; // plan final sur l'avatar, sans texte

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
