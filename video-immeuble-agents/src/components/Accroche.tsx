import React from 'react';
import {easeOut, prog} from '../anim';
import {TEXTES} from '../data';
import {C, MARGE, SANS} from '../theme';
import {ACCROCHE} from '../timeline';
import {LigneMasquee} from './Legende';

// 0 à 3 s : titre très gros, noir sur fond clair.
export const Accroche: React.FC<{f: number}> = ({f}) => {
  const lignes = TEXTES.accroche;
  const trait = prog(f, 30, 20, easeOut);
  return (
    <div
      style={{
        position: 'absolute',
        left: MARGE,
        right: MARGE,
        top: 0,
        bottom: 0,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        fontFamily: SANS,
        fontSize: 140,
        lineHeight: 1.0,
        fontWeight: 800,
        letterSpacing: '-0.045em',
        color: C.encre,
        paddingBottom: 60,
      }}
    >
      {lignes.map((l, i) => {
        const derniere = i === lignes.length - 1;
        return (
          <LigneMasquee key={l} f={f} entree={-10 + i * 5} sortie={ACCROCHE.sortie + i * 3} style={{paddingBottom: '0.2em', marginBottom: '-0.2em'}}>
            <span style={{position: 'relative', display: 'inline-block'}}>
              {l}
              {derniere ? (
                <span
                  style={{
                    position: 'absolute',
                    left: 4,
                    right: 18,
                    bottom: '-0.06em',
                    height: '0.085em',
                    borderRadius: 8,
                    background: C.accent,
                    transform: `scaleX(${trait})`,
                    transformOrigin: 'left center',
                  }}
                />
              ) : null}
            </span>
          </LigneMasquee>
        );
      })}
    </div>
  );
};
