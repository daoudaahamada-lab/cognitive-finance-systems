import React from 'react';
import {Img, staticFile} from 'remotion';
import {easeIn, easeInOut, easeOut, piste, prog} from '../anim';
import {CAPTURES, TEXTES} from '../data';
import {C, MARGE, SANS} from '../theme';
import {FIN} from '../timeline';
import {LigneMasquee} from './Legende';

const ECRAN_L = 540;
const ECRAN_H = Math.round((540 * 2532) / 1170); // 1169
const CADRE = 12;

// Scène 6 : la version mobile (capture 12), puis la phrase de chute.
export const Fin: React.FC<{f: number}> = ({f}) => {
  const entree = prog(f, FIN.telephone, 32, easeOut);
  const sortie = prog(f, FIN.recentrage, 24, easeIn);
  const zoom = 1 + 0.06 * prog(f, FIN.telephone, 120, easeInOut);
  const topTexte = piste(f, [
    [FIN.recentrage, 150],
    [FIN.recentrage + 30, 790],
  ]);
  const largeur = ECRAN_L + CADRE * 2;
  return (
    <>
      {sortie < 1 ? (
        <div
          style={{
            position: 'absolute',
            left: (1080 - largeur) / 2,
            top: 560 + (1 - entree) * 1400 + sortie * 260,
            width: largeur,
            height: ECRAN_H + CADRE * 2,
            borderRadius: 78,
            background: '#15161a',
            padding: CADRE,
            boxShadow: '0 50px 100px rgba(30, 24, 14, 0.25), 0 10px 24px rgba(30, 24, 14, 0.12)',
            opacity: 1 - sortie,
          }}
        >
          <div style={{width: ECRAN_L, height: ECRAN_H, borderRadius: 66, overflow: 'hidden', background: C.fond}}>
            <Img
              src={staticFile(CAPTURES.mobileQG)}
              style={{width: ECRAN_L, height: ECRAN_H, transform: `scale(${zoom})`, transformOrigin: '50% 55%'}}
            />
          </div>
        </div>
      ) : null}
      <div
        style={{
          position: 'absolute',
          left: MARGE,
          right: MARGE,
          top: topTexte,
          fontFamily: SANS,
          fontSize: 88,
          lineHeight: 1.08,
          fontWeight: 800,
          letterSpacing: '-0.035em',
          color: C.encre,
        }}
      >
        <LigneMasquee f={f} entree={FIN.ligne1}>
          {TEXTES.chute[0]}
        </LigneMasquee>
        <LigneMasquee f={f} entree={FIN.ligne2}>
          <span style={{color: C.accent}}>{TEXTES.chute[1]}</span>
        </LigneMasquee>
      </div>
    </>
  );
};
