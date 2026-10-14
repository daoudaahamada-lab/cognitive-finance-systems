import React from 'react';
import {easeIn, easeOut, prog} from '../anim';
import {C, MARGE, SANS} from '../theme';

// Ligne de texte révélée derrière un masque (glisse de bas en haut).
export const LigneMasquee: React.FC<{
  entree: number;
  sortie?: number;
  dureeSortie?: number;
  f: number;
  style?: React.CSSProperties;
  children: React.ReactNode;
}> = ({entree, sortie, dureeSortie = 12, f, style, children}) => {
  const p = prog(f, entree, 18, easeOut);
  const q = sortie === undefined ? 0 : prog(f, sortie, dureeSortie, easeIn);
  const y = (1 - p) * 130 - q * 130;
  return (
    <div style={{overflow: 'hidden', paddingBottom: '0.12em', marginBottom: '-0.12em', ...style}}>
      <div style={{transform: `translateY(${y}%)`, whiteSpace: 'nowrap'}}>{children}</div>
    </div>
  );
};

// Légende du haut d'écran : petit surtitre bleu + phrase en gras.
export const Legende: React.FC<{
  f: number;
  entree: number;
  sortie: number;
  kicker: string;
  lignes: readonly string[];
}> = ({f, entree, sortie, kicker, lignes}) => {
  if (f < entree - 1 || f > sortie + 30) return null;
  return (
    <div style={{position: 'absolute', left: MARGE, right: MARGE, top: 118, fontFamily: SANS}}>
      <LigneMasquee f={f} entree={entree} sortie={sortie}>
        <div
          style={{
            fontSize: 26,
            fontWeight: 700,
            letterSpacing: '0.18em',
            textTransform: 'uppercase',
            color: C.accent,
            display: 'flex',
            alignItems: 'center',
            gap: 14,
          }}
        >
          <span style={{width: 12, height: 12, borderRadius: 6, background: C.accent, flexShrink: 0}} />
          {kicker}
        </div>
      </LigneMasquee>
      <div style={{height: 16}} />
      {lignes.map((l, i) => (
        <LigneMasquee key={l} f={f} entree={entree + 4 + i * 4} sortie={sortie + 2 + i * 3}>
          <div
            style={{
              fontSize: 84,
              lineHeight: 1.06,
              fontWeight: 800,
              letterSpacing: '-0.035em',
              color: C.encre,
            }}
          >
            {l}
          </div>
        </LigneMasquee>
      ))}
    </div>
  );
};
