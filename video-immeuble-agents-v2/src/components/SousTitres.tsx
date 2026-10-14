import React from 'react';
import {ETAPES, SOUS_TITRES} from '../data';
import {C, MARGE, SANS} from '../theme';
import {a, FINAL, R} from '../timeline';
import {LIGNES} from '../voix';
import {LigneMasquee} from './Legende';

// Sous-titres de la voix off, dans le style typographique de la vidéo (gras, noir, en haut d'écran),
// avec le surtitre bleu de l'étape du récit.
type Item = {texte: string; rang: number; entree: number; sortie: number};

const etapeDe = (id: string) => LIGNES.find((l) => l.id === id)!.etape;

const construire = () => {
  const cartons = SOUS_TITRES.map((c) => ({...c, debut: a(c.id, c.a)}));
  const items: Item[] = [];
  const actifs: (Item | undefined)[] = [];
  const surtitres: {etape: number; entree: number; sortie: number}[] = [];
  cartons.forEach((c, i) => {
    const suivant = cartons[i + 1];
    const fin = suivant ? Math.min(suivant.debut - 11, R[c.id].fin + 12) : FINAL.arrivee + 14;
    c.lignes.forEach((texte, rang) => {
      const precedent = actifs[rang];
      if (precedent && precedent.texte === texte && precedent.sortie >= c.debut - 11) {
        precedent.sortie = fin; // la ligne reste en place
      } else {
        const item = {texte, rang, entree: c.debut + rang * 4, sortie: fin + rang * 2};
        items.push(item);
        actifs[rang] = item;
      }
    });
    for (let r = c.lignes.length; r < actifs.length; r++) actifs[r] = undefined;
    const e = etapeDe(c.id);
    const dernier = surtitres[surtitres.length - 1];
    if (dernier && dernier.etape === e) dernier.sortie = fin;
    else surtitres.push({etape: e, entree: c.debut - 2, sortie: fin});
  });
  return {items, surtitres};
};

const {items: ITEMS, surtitres: SURTITRES} = construire();

export const SousTitres: React.FC<{f: number; texte: boolean}> = ({f, texte}) => (
  <div style={{position: 'absolute', left: MARGE, right: MARGE, top: 112, fontFamily: SANS}}>
    {SURTITRES.filter((s) => f >= s.entree - 1 && f <= s.sortie + 20).map((s) => (
      <div key={s.etape} style={{position: 'absolute', left: 0, top: 0, width: '100%'}}>
        <LigneMasquee f={f} entree={s.entree} sortie={s.sortie} dureeSortie={8}>
          <div style={{fontSize: 24, fontWeight: 700, letterSpacing: '0.18em', textTransform: 'uppercase', color: C.accent, display: 'flex', alignItems: 'center', gap: 12}}>
            <span style={{width: 11, height: 11, borderRadius: 6, background: C.accent}} />
            {s.etape}/6 · {ETAPES[s.etape]}
          </div>
        </LigneMasquee>
      </div>
    ))}
    {texte
      ? ITEMS.filter((it) => f >= it.entree - 1 && f <= it.sortie + 20).map((it) => (
          <div key={`${it.texte}-${it.entree}`} style={{position: 'absolute', left: 0, top: 46 + it.rang * 66, width: '100%'}}>
            <LigneMasquee f={f} entree={it.entree} sortie={it.sortie} dureeSortie={8}>
              <div style={{fontSize: 58, lineHeight: 1.1, fontWeight: 800, letterSpacing: '-0.03em', color: C.encre}}>{it.texte}</div>
            </LigneMasquee>
          </div>
        ))
      : null}
  </div>
);
