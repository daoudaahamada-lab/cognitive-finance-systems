import React from 'react';
import {Img, staticFile} from 'remotion';
import {CAPTURES, MOBILE, ONGLET_RDC_MOBILE} from '../data';
import {SANS} from '../theme';

// Capture mobile 12 en "cover" calée en haut, avec l'onglet du rez-de-chaussée renommé.
export const EcranMobile: React.FC<{largeur: number; hauteur: number}> = ({largeur, hauteur}) => {
  const s = Math.max(largeur / MOBILE.w, hauteur / MOBILE.h);
  const w = MOBILE.w * s;
  const h = MOBILE.h * s;
  const o = ONGLET_RDC_MOBILE;
  return (
    <div style={{position: 'absolute', left: (largeur - w) / 2, top: 0, width: w, height: h}}>
      <Img src={staticFile(CAPTURES.mobileQG)} style={{position: 'absolute', left: 0, top: 0, width: w, height: h}} />
      {o.actif ? (
        <div
          style={{
            position: 'absolute',
            left: o.x * s,
            top: o.y * s,
            width: o.w * s,
            height: o.h * s,
            background: o.fond,
            color: o.encre,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontFamily: SANS,
            fontWeight: 700,
            fontSize: o.taille * s,
            letterSpacing: '-0.01em',
          }}
        >
          {o.texte}
        </div>
      ) : null}
    </div>
  );
};
