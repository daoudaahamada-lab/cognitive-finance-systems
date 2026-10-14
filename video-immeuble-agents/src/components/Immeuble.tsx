import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {clamp01, clignote, easeIn, easeOut, piste, prog} from '../anim';
import {
  CAPTURE_H,
  CAPTURE_W,
  CENTRE_ETAGE,
  CENTRE_SALES,
  COIN_DROIT,
  ETAGES,
  IDX_BUSINESS,
  IDX_WEALTH,
  PIECES_WEALTH,
  PILLULE_SALES,
  POLY_ETAGE,
} from '../data';
import {C, MONO, SANS} from '../theme';
import {chuteEtage, clesEtage, PLONGEE, SALLE, TOUR, TRAVAUX} from '../timeline';

// --- Caméra -------------------------------------------------------------
// Monde = pixels des captures. L'étage i est posé à y = i * écart.
// La caméra vise un point (lx, ly) de l'étage `etage` et le place à l'écran en (ax, ay).

export type Camera = {
  s: number;
  etage: number;
  lx: number;
  ly: number;
  ax: number;
  ay: number;
  ecart: number;
  voisins: number;
  opacite: number;
};

export const camera = (f: number): Camera => ({
  s: piste(f, [
    [TOUR.debut, 0.3],
    [PLONGEE.debut, 0.315],
    [PLONGEE.fin, 0.47],
    [SALLE.zoom[0], 0.47],
    [SALLE.zoom[1], 1.25],
    [TRAVAUX.transition[0], 1.25],
    [TRAVAUX.transition[1], 0.42],
    [TRAVAUX.sortie, 0.42],
    [TRAVAUX.sortie + 32, 0.36],
  ]),
  etage: piste(f, clesEtage),
  lx: piste(f, [
    [SALLE.zoom[0], CENTRE_ETAGE.x],
    [SALLE.zoom[1], CENTRE_SALES.x],
    [TRAVAUX.transition[0], CENTRE_SALES.x],
    [TRAVAUX.transition[1], CENTRE_ETAGE.x],
  ]),
  ly: piste(f, [
    [SALLE.zoom[0], CENTRE_ETAGE.y],
    [SALLE.zoom[1], CENTRE_SALES.y],
    [TRAVAUX.transition[0], CENTRE_SALES.y],
    [TRAVAUX.transition[1], CENTRE_ETAGE.y],
  ]),
  ax: piste(f, [
    [PLONGEE.debut, 430],
    [PLONGEE.fin, 540],
  ]),
  ay: piste(f, [
    [PLONGEE.debut, 1130],
    [PLONGEE.fin, 830],
    [SALLE.zoom[0], 830],
    [SALLE.zoom[1], 860],
    [SALLE.panneau - 6, 860],
    [SALLE.panneau + 24, 600],
    [TRAVAUX.transition[0], 600],
    [TRAVAUX.transition[1], 660],
    [TRAVAUX.sortie, 660],
    [TRAVAUX.sortie + 32, 540],
  ]),
  ecart: piste(f, [
    [PLONGEE.debut, 780],
    [PLONGEE.fin, 1650],
  ]),
  voisins: piste(f, [
    [PLONGEE.debut, 1],
    [PLONGEE.fin, 0.2],
    [SALLE.remontee[1], 0.2],
    [SALLE.zoom[0] + 16, 0],
  ]),
  opacite: piste(f, [
    [TRAVAUX.sortie, 1],
    [TRAVAUX.sortie + 28, 0],
  ]),
});

export const versEcran = (c: Camera, i: number, x: number, y: number) => ({
  x: c.ax + (x - c.lx) * c.s,
  y: c.ay + (i * c.ecart + y - (c.etage * c.ecart + c.ly)) * c.s,
});

const chute = (f: number, i: number) => prog(f, chuteEtage(i), TOUR.chute, easeOut);

const POLYGONE = `polygon(${POLY_ETAGE.map(([x, y]) => `${x}px ${y}px`).join(', ')})`;

// --- Surcouches dans le repère d'un étage ------------------------------

const AnneauSales: React.FC<{f: number}> = ({f}) => {
  const a = prog(f, SALLE.anneau, 14, easeOut);
  const ping = prog(f, SALLE.anneau + 6, 30, easeOut);
  const p = PILLULE_SALES;
  const cadre = (pad: number): React.CSSProperties => ({
    position: 'absolute',
    left: p.x - pad,
    top: p.y - pad,
    width: p.w + pad * 2,
    height: p.h + pad * 2,
    borderRadius: 60,
  });
  return (
    <>
      <div style={{...cadre(10), border: `6px solid ${C.accent}`, opacity: a, transform: `scale(${0.92 + 0.08 * a})`}} />
      <div
        style={{
          ...cadre(10),
          border: `4px solid ${C.accent}`,
          opacity: 0.55 * (1 - ping) * (ping > 0 ? 1 : 0),
          transform: `scale(${1 + 0.45 * ping})`,
        }}
      />
    </>
  );
};

export const intensitePiece = (f: number, k: number) => {
  const seule = clignote(f, TRAVAUX.clignotes[k], 2, 14);
  const ensemble = Math.max(clignote(f, TRAVAUX.tous[0], 2, 16), clignote(f, TRAVAUX.tous[1], 2, 14));
  return Math.max(seule, ensemble);
};

const PiecesEnTravaux: React.FC<{f: number}> = ({f}) => (
  <>
    <svg
      width={CAPTURE_W}
      height={CAPTURE_H}
      style={{position: 'absolute', left: 0, top: 0}}
    >
      <defs>
        <filter id="flou-travaux" x="-10%" y="-10%" width="120%" height="120%">
          <feGaussianBlur stdDeviation="10" />
        </filter>
      </defs>
      {PIECES_WEALTH.map((piece, k) => {
        const v = intensitePiece(f, k);
        return (
          <polygon
            key={piece.nom}
            points={piece.zone}
            fill="#ffc81e"
            stroke={C.travaux}
            strokeWidth={16}
            strokeLinejoin="round"
            opacity={0.5 * v}
            filter="url(#flou-travaux)"
          />
        );
      })}
    </svg>
    {PIECES_WEALTH.map((piece, k) => {
      const v = intensitePiece(f, k);
      const p = piece.pillule;
      return (
        <div
          key={piece.nom}
          style={{
            position: 'absolute',
            left: p.x,
            top: p.y,
            width: p.w,
            height: p.h,
            borderRadius: 999,
            boxShadow: `0 0 0 ${6 + 16 * v}px rgba(242, 180, 0, ${0.55 * v})`,
          }}
        />
      );
    })}
  </>
);

// --- L'immeuble --------------------------------------------------------

export const Immeuble: React.FC<{f: number}> = ({f}) => {
  const c = camera(f);
  const tx = c.ax - c.lx * c.s;
  const ty = c.ay - (c.etage * c.ecart + c.ly) * c.s;
  return (
    <AbsoluteFill
      style={{
        opacity: c.opacite,
        // la zone des légendes reste propre
        maskImage: 'linear-gradient(to bottom, transparent 0px, transparent 330px, #000 410px)',
        WebkitMaskImage: 'linear-gradient(to bottom, transparent 0px, transparent 330px, #000 410px)',
      }}
    >
      <div style={{position: 'absolute', left: 0, top: 0, transformOrigin: '0 0', transform: `translate(${tx}px, ${ty}px) scale(${c.s})`}}>
        {ETAGES.map((e, i) => {
          const p = chute(f, i);
          const distance = Math.min(1, Math.abs(i - c.etage));
          const visible = clamp01(p * 2.5) * (1 - distance * (1 - c.voisins));
          if (visible <= 0.001) return null;
          return (
            <div
              key={e.nom}
              style={{
                position: 'absolute',
                left: 0,
                top: i * c.ecart - (1 - p) * 700,
                width: CAPTURE_W,
                height: CAPTURE_H,
                clipPath: POLYGONE,
                opacity: visible,
                zIndex: 10 - i,
              }}
            >
              <Img src={staticFile(e.capture)} style={{position: 'absolute', left: 0, top: 0, width: CAPTURE_W, height: CAPTURE_H}} />
              {i === IDX_BUSINESS && f >= SALLE.anneau ? <AnneauSales f={f} /> : null}
              {i === IDX_WEALTH && f >= TRAVAUX.clignotes[0] ? <PiecesEnTravaux f={f} /> : null}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// Étiquettes à droite de la tour (vue d'ensemble).
export const EtiquettesTour: React.FC<{f: number}> = ({f}) => {
  const c = camera(f);
  const sortie = prog(f, PLONGEE.debut - 4, 12, easeIn);
  return (
    <AbsoluteFill style={{fontFamily: SANS}}>
      {ETAGES.map((e, i) => {
        const pose = chuteEtage(i) + TOUR.chute - 6;
        const a = prog(f, pose, 14, easeOut) * (1 - sortie);
        if (a <= 0) return null;
        const pos = versEcran(c, i, COIN_DROIT.x, COIN_DROIT.y);
        return (
          <div
            key={e.nom}
            style={{
              position: 'absolute',
              left: pos.x + 26 + (1 - a) * 30,
              top: pos.y - 26,
              opacity: a,
              display: 'flex',
              alignItems: 'center',
              gap: 14,
            }}
          >
            <span
              style={{
                fontFamily: MONO,
                fontSize: 22,
                fontWeight: 700,
                color: C.gris,
                border: `2px solid rgba(17,18,20,0.14)`,
                borderRadius: 10,
                padding: '4px 9px',
                minWidth: 30,
                textAlign: 'center',
              }}
            >
              {e.numero}
            </span>
            <span style={{fontSize: 40, fontWeight: 800, letterSpacing: '-0.02em', color: C.encre}}>{e.nom}</span>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
