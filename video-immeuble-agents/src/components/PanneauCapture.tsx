import React from 'react';
import {Img, staticFile} from 'remotion';
import {easeOut, prog} from '../anim';
import {CAPTURE_H, CAPTURE_W} from '../data';
import {C, SANS} from '../theme';

type Decoupe = {x: number; y: number; w: number; h: number};

// Un panneau découpé dans une capture, affiché dans une fenêtre arrondie,
// avec défilement vertical. Les enfants sont placés en coordonnées locales au panneau.
export const PanneauCapture: React.FC<{
  src: string;
  decoupe: Decoupe;
  left: number;
  top: number;
  largeur: number;
  hauteur: number;
  defile: number;
  dy: number;
  // filtre CSS appliqué à la capture (ex. pour blanchir les reflets d'un panneau translucide)
  filtre?: string;
  // fond dégradé en bas de fenêtre : la liste se fond dans la carte au lieu d'être coupée net
  fonduBas?: boolean;
  children?: React.ReactNode;
}> = ({src, decoupe, left, top, largeur, hauteur, defile, dy, filtre, fonduBas = true, children}) => {
  const k = largeur / decoupe.w;
  return (
    <div
      style={{
        position: 'absolute',
        left,
        top,
        width: largeur,
        height: hauteur,
        borderRadius: 36,
        overflow: 'hidden',
        background: C.carte,
        boxShadow: C.ombre,
        transform: `translateY(${dy}px)`,
      }}
    >
      <div
        style={{
          position: 'absolute',
          left: 0,
          top: 0,
          width: decoupe.w,
          height: decoupe.h,
          transformOrigin: '0 0',
          transform: `scale(${k}) translateY(${-defile}px)`,
        }}
      >
        <Img
          src={staticFile(src)}
          style={{position: 'absolute', left: -decoupe.x, top: -decoupe.y, width: CAPTURE_W, height: CAPTURE_H, filter: filtre}}
        />
        {children}
      </div>
      {fonduBas ? (
        <div
          style={{
            position: 'absolute',
            left: 0,
            right: 0,
            bottom: 0,
            height: 90,
            background: `linear-gradient(to bottom, rgba(250, 249, 246, 0), ${C.carte})`,
          }}
        />
      ) : null}
    </div>
  );
};

// Cadre bleu + étiquette, en coordonnées locales au panneau.
export const Surlignage: React.FC<{
  f: number;
  debut: number;
  x: number;
  y: number;
  w: number;
  h: number;
  label: string;
}> = ({f, debut, x, y, w, h, label}) => {
  const a = prog(f, debut, 14, easeOut);
  if (a <= 0) return null;
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, height: h, opacity: a}}>
      <div
        style={{
          position: 'absolute',
          inset: 0,
          borderRadius: 24,
          border: `5px solid ${C.accent}`,
          background: 'rgba(47, 107, 255, 0.04)',
          transform: `scale(${0.97 + 0.03 * a})`,
        }}
      />
      <div
        style={{
          position: 'absolute',
          right: 22,
          top: -22,
          background: C.accent,
          color: '#fff',
          fontFamily: SANS,
          fontSize: 25,
          fontWeight: 700,
          letterSpacing: '-0.01em',
          padding: '7px 18px',
          borderRadius: 999,
          transform: `translateY(${(1 - a) * 10}px)`,
        }}
      >
        {label}
      </div>
    </div>
  );
};

// Surligneur jaune (statut "en travaux"), en coordonnées locales au panneau.
export const Jaune: React.FC<{x: number; y: number; w: number; h: number; intensite: number; rayon?: number; etire?: number}> = ({
  x,
  y,
  w,
  h,
  intensite,
  rayon = 999,
  etire = 1,
}) => (
  <div
    style={{
      position: 'absolute',
      left: x,
      top: y,
      width: w,
      height: h,
      borderRadius: rayon,
      background: C.travaux,
      mixBlendMode: 'multiply',
      opacity: 0.75 * intensite,
      transform: `scaleX(${etire})`,
      transformOrigin: 'left center',
    }}
  />
);
