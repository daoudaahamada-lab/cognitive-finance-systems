import React from 'react';
import {easeIn, easeInOut, piste, prog} from '../anim';
import {TEXTES} from '../data';
import {C, MARGE, SANS} from '../theme';
import {FIN} from '../timeline';
import {TELEPHONE} from './Cockpit';
import {EcranMobile} from './EcranMobile';
import {LigneMasquee} from './Legende';

// Scène 6 : la version mobile (capture 12), puis la phrase de chute.
// Le téléphone naît du repli de la carte du cockpit (voir Cockpit.tsx) : il est déjà en place ici.
export const Fin: React.FC<{f: number}> = ({f}) => {
  const sortie = prog(f, FIN.recentrage, 14, easeIn);
  // lente poussée sur tout le téléphone (l'écran garde son cadrage)
  const zoom = 1 + 0.04 * prog(f, FIN.telephone, FIN.recentrage - FIN.telephone, easeInOut);
  const topTexte = piste(f, [
    [FIN.recentrage + 8, 150],
    [FIN.recentrage + 38, 790],
  ]);
  const T = TELEPHONE;
  return (
    <>
      {f >= FIN.telephone && sortie < 1 ? (
        <div
          style={{
            position: 'absolute',
            left: T.left,
            top: T.top + sortie * 260,
            width: T.largeur,
            height: T.hauteur,
            boxSizing: 'border-box',
            borderRadius: T.rayon,
            background: T.fond,
            boxShadow: '0 40px 90px rgba(20, 16, 10, 0.26), 0 8px 20px rgba(20, 16, 10, 0.12)',
            opacity: 1 - sortie,
            transform: `scale(${zoom})`,
            transformOrigin: '50% 50%',
          }}
        >
          <div style={{position: 'absolute', inset: T.cadre, borderRadius: T.rayonEcran, overflow: 'hidden', background: C.fond}}>
            <EcranMobile largeur={T.largeur - T.cadre * 2} hauteur={T.hauteur - T.cadre * 2} />
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
