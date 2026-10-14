import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {clamp01, clignote, easeDouce, easeIn, easeInOut, easeOut, piste, prog} from '../anim';
import {
  CAPTURE_H,
  CAPTURE_W,
  CENTRE_ETAGE,
  CENTRE_SALES,
  COIN_DROIT,
  COMPTEUR_SALES,
  DAOUDA,
  ETAGES,
  IDX_BUSINESS,
  IDX_WEALTH,
  PIECES_WEALTH,
  PILLULE_SALES,
  POLY_ETAGE,
} from '../data';
import {C, MONO, SANS} from '../theme';
import {
  chuteEtage,
  clesEtage,
  COCKPIT,
  ETIQUETTES_TOUR,
  FINAL,
  PLONGEE,
  RECUL,
  SALLE,
  TOUR,
  TRAVAUX,
} from '../timeline';

const IDX_RDC = 3;

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
  flou: number;
};

export const camera = (f: number): Camera => ({
  s: piste(f, [
    [TOUR.debut, 0.3],
    [PLONGEE.debut, 0.33],
    [PLONGEE.fin, 0.47],
    [SALLE.zoom[0], 0.47],
    [SALLE.zoom[1], 1.25],
    [SALLE.recul[0], 1.25],
    [SALLE.recul[1], 0.5],
    [TRAVAUX.attention, 0.5],
    [TRAVAUX.attention + 24, 0.42],
    [RECUL.debut, 0.42],
    [RECUL.fin, 0.3],
    [FINAL.approche, 0.3],
    [FINAL.approche + 26, 0.36],
    [FINAL.bascule, 1.7],
    [FINAL.arrivee, 0.4],
    [FINAL.fin, 0.39],
  ]),
  etage: piste(f, clesEtage, easeDouce),
  lx: piste(f, [
    [SALLE.zoom[0], CENTRE_ETAGE.x],
    [SALLE.zoom[1], CENTRE_SALES.x],
    [SALLE.recul[0], CENTRE_SALES.x],
    [SALLE.recul[1], CENTRE_ETAGE.x],
    [FINAL.approche + 26, CENTRE_ETAGE.x],
    [FINAL.bascule, DAOUDA.centre.x],
    [FINAL.arrivee, CENTRE_ETAGE.x],
  ]),
  ly: piste(f, [
    [SALLE.zoom[0], CENTRE_ETAGE.y],
    [SALLE.zoom[1], CENTRE_SALES.y],
    [SALLE.recul[0], CENTRE_SALES.y],
    [SALLE.recul[1], CENTRE_ETAGE.y],
    [FINAL.approche + 26, CENTRE_ETAGE.y],
    [FINAL.bascule, DAOUDA.centre.y],
    [FINAL.arrivee, CENTRE_ETAGE.y],
  ]),
  ax: piste(f, [
    [ETIQUETTES_TOUR.entree - 8, 540],
    [ETIQUETTES_TOUR.entree + 10, 430],
    [PLONGEE.debut, 430],
    [PLONGEE.fin, 540],
    [RECUL.debut, 540],
    [RECUL.fin, 430],
    [FINAL.approche, 430],
    [FINAL.approche + 26, 540],
  ]),
  ay: piste(f, [
    [PLONGEE.debut, 1130],
    [PLONGEE.fin, 830],
    [SALLE.zoom[0], 830],
    [SALLE.zoom[1], 860],
    [SALLE.panneau, 860],
    [SALLE.panneau + 28, 640],
    [SALLE.recul[0], 640],
    [SALLE.recul[1], 960],
    [COCKPIT.entree - 2, 960],
    [COCKPIT.entree + 16, 760],
    [COCKPIT.sortie, 760],
    [COCKPIT.sortie + 1, 1200],
    [TRAVAUX.retour, 1200],
    [TRAVAUX.retour + 22, 900],
    [TRAVAUX.attention, 900],
    [TRAVAUX.attention + 24, 660],
    [RECUL.debut, 660],
    [RECUL.fin, 1130],
    [FINAL.approche, 1130],
    [FINAL.approche + 26, 1000],
    [FINAL.bascule, 1150],
    [FINAL.arrivee, 1000],
  ]),
  ecart: piste(f, [
    [PLONGEE.debut, 780],
    [PLONGEE.fin, 1650],
    [RECUL.debut, 1650],
    [RECUL.fin, 780],
    [FINAL.approche + 26, 780],
    [FINAL.bascule, 1650],
    [FINAL.arrivee, 780],
  ]),
  voisins: piste(f, [
    [PLONGEE.debut, 1],
    [PLONGEE.fin, 0],
    [RECUL.debut, 0],
    [RECUL.fin, 1],
    [FINAL.approche + 26, 1],
    [FINAL.bascule - 12, 0],
    [FINAL.arrivee, 1],
  ]),
  opacite: piste(f, [
    [COCKPIT.entree - 2, 1],
    [COCKPIT.entree + 14, 0],
    [TRAVAUX.retour, 0],
    [TRAVAUX.retour + 14, 1],
    [FINAL.bascule, 1],
    [FINAL.arrivee, 0.82],
  ]),
  flou: piste(f, [
    [FINAL.bascule, 0],
    [FINAL.bascule + 18, 7],
    [FINAL.arrivee, 10],
  ]),
});

export const versEcran = (c: Camera, i: number, x: number, y: number) => ({
  x: c.ax + (x - c.lx) * c.s,
  y: c.ay + (i * c.ecart + y - (c.etage * c.ecart + c.ly)) * c.s,
});

const chute = (f: number, i: number) => prog(f, chuteEtage(i), TOUR.chute, easeOut);

const POLYGONE = `polygon(${POLY_ETAGE.map(([x, y]) => `${x}px ${y}px`).join(', ')})`;

// --- Surcouches dans le repère d'un étage ------------------------------

const cadre = (p: {x: number; y: number; w: number; h: number}, pad: number): React.CSSProperties => ({
  position: 'absolute',
  left: p.x - pad,
  top: p.y - pad,
  width: p.w + pad * 2,
  height: p.h + pad * 2,
  borderRadius: 60,
});

const AnneauSales: React.FC<{f: number}> = ({f}) => {
  const a = prog(f, SALLE.anneau, 14, easeOut);
  const ping = prog(f, SALLE.anneau + 6, 30, easeOut);
  const ping2 = prog(f, SALLE.compteurSales, 26, easeOut);
  const p = PILLULE_SALES;
  return (
    <>
      <div style={{...cadre(p, 10), border: `6px solid ${C.accent}`, opacity: a, transform: `scale(${0.92 + 0.08 * a})`}} />
      {[ping, ping2].map((q, k) =>
        q > 0 && q < 1 ? (
          <div key={k} style={{...cadre(p, 10), border: `4px solid ${C.accent}`, opacity: 0.55 * (1 - q), transform: `scale(${1 + 0.45 * q})`}} />
        ) : null,
      )}
    </>
  );
};

// La tâche validée fait passer la salle Sales de 0/17 à 1/17.
const CompteurSales: React.FC<{f: number}> = ({f}) => {
  const p = prog(f, SALLE.compteurSales, 10, easeOut);
  if (p <= 0) return null;
  const k = COMPTEUR_SALES;
  return (
    <div
      style={{
        position: 'absolute',
        left: k.x,
        top: k.y,
        width: k.w,
        height: k.h,
        background: '#fdfdfc',
        overflow: 'hidden',
        fontFamily: MONO,
        fontSize: 24,
        fontWeight: 700,
        lineHeight: `${k.h}px`,
        color: '#8b8b8b',
      }}
    >
      <div style={{transform: `translateY(${(1 - p) * 100}%)`, color: p < 1 ? C.accent : '#8b8b8b'}}>1/17</div>
      <div style={{position: 'absolute', left: 0, top: 0, transform: `translateY(${-p * 100}%)`}}>0/17</div>
    </div>
  );
};

// Une impulsion par pièce, puis toutes ensemble.
export const intensitePiece = (f: number, k: number) =>
  Math.max(clignote(f, TRAVAUX.clignotes[k], 1, 18), clignote(f, TRAVAUX.tous, 2, 11));

const PiecesEnTravaux: React.FC<{f: number}> = ({f}) => (
  <>
    <svg width={CAPTURE_W} height={CAPTURE_H} style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <filter id="flou-travaux" x="-10%" y="-10%" width="120%" height="120%">
          <feGaussianBlur stdDeviation="10" />
        </filter>
      </defs>
      {PIECES_WEALTH.map((piece, k) => (
        <polygon
          key={piece.nom}
          points={piece.zone}
          fill="#ffc81e"
          stroke={C.travaux}
          strokeWidth={16}
          strokeLinejoin="round"
          opacity={0.5 * intensitePiece(f, k)}
          filter="url(#flou-travaux)"
        />
      ))}
    </svg>
  </>
);

// L'avatar de la capture est effacé quand l'avatar 3D prend le relais.
const EffaceDaouda: React.FC = () => (
  <>
    {DAOUDA.masque.map((m, k) => (
      <div
        key={k}
        style={{position: 'absolute', left: m.x, top: m.y, width: m.w, height: m.h, borderRadius: 30, background: DAOUDA.sol, filter: 'blur(6px)'}}
      />
    ))}
  </>
);

// --- L'immeuble --------------------------------------------------------

export const Immeuble: React.FC<{f: number}> = ({f}) => {
  const c = camera(f);
  if (c.opacite <= 0.001) return null;
  const tx = c.ax - c.lx * c.s;
  const ty = c.ay - (c.etage * c.ecart + c.ly) * c.s;
  return (
    <AbsoluteFill
      style={{
        opacity: c.opacite,
        filter: c.flou > 0.05 ? `blur(${c.flou}px)` : undefined,
        // la zone des sous-titres reste propre
        maskImage: 'linear-gradient(to bottom, transparent 0px, transparent 330px, #000 410px)',
        WebkitMaskImage: 'linear-gradient(to bottom, transparent 0px, transparent 330px, #000 410px)',
      }}
    >
      <div style={{position: 'absolute', left: 0, top: 0, transformOrigin: '0 0', transform: `translate(${tx}px, ${ty}px) scale(${c.s})`}}>
        {ETAGES.map((e, i) => {
          const p = chute(f, i);
          const d = Math.abs(i - c.etage);
          const visible = clamp01(p * 2.5) * (1 - clamp01((Math.min(1, d) - 0.6) / 0.4) * (1 - c.voisins));
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
              {i === IDX_BUSINESS && f >= SALLE.anneau && f < COCKPIT.entree + 20 ? (
                <>
                  <CompteurSales f={f} />
                  <AnneauSales f={f} />
                </>
              ) : null}
              {i === IDX_WEALTH && f >= TRAVAUX.clignotes[0] - 1 && f < RECUL.fin ? <PiecesEnTravaux f={f} /> : null}
              {i === IDX_RDC && f >= FINAL.bascule + 8 ? <EffaceDaouda /> : null}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// Étiquettes à droite de la tour : noms des domaines (étape 3), puis avancement (étape 6).
export const EtiquettesTour: React.FC<{f: number; entree: number; sortie: number; pourcentage?: boolean}> = ({f, entree, sortie, pourcentage}) => {
  const c = camera(f);
  const out = prog(f, sortie, 12, easeIn);
  return (
    <AbsoluteFill style={{fontFamily: SANS}}>
      {ETAGES.map((e, i) => {
        const a = prog(f, entree + i * 5, 14, easeOut) * (1 - out);
        if (a <= 0) return null;
        const pos = versEcran(c, i, COIN_DROIT.x, COIN_DROIT.y);
        return (
          <div
            key={e.nom}
            style={{position: 'absolute', left: pos.x + 26 + (1 - a) * 30, top: pos.y - 26, opacity: a, display: 'flex', alignItems: 'center', gap: 14}}
          >
            <span
              style={{
                fontFamily: MONO,
                fontSize: 22,
                fontWeight: 700,
                color: C.gris,
                border: '2px solid rgba(17,18,20,0.14)',
                borderRadius: 10,
                padding: '4px 9px',
                minWidth: 30,
                textAlign: 'center',
              }}
            >
              {e.numero}
            </span>
            <span style={{fontSize: 40, fontWeight: 800, letterSpacing: '-0.02em', color: C.encre}}>{e.nom}</span>
            {pourcentage ? (
              <span style={{fontFamily: MONO, fontSize: 26, fontWeight: 700, color: e.statut === 'travaux' ? '#b98a00' : C.accent}}>
                {e.pourcentage}%
              </span>
            ) : null}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// Pastille « Sous-agent » accrochée à la salle Sales.
export const EtiquetteSousAgent: React.FC<{f: number}> = ({f}) => {
  const c = camera(f);
  const a = prog(f, SALLE.anneau + 4, 12, easeOut) * (1 - prog(f, SALLE.panneau + 6, 10, easeIn));
  if (a <= 0) return null;
  const pos = versEcran(c, IDX_BUSINESS, PILLULE_SALES.x + PILLULE_SALES.w + 24, PILLULE_SALES.y + PILLULE_SALES.h / 2);
  return (
    <div
      style={{
        position: 'absolute',
        left: pos.x,
        top: pos.y,
        transform: `translate(0, -50%) scale(${0.8 + 0.2 * a})`,
        transformOrigin: 'left center',
        opacity: a,
        background: C.accent,
        color: '#fff',
        fontFamily: SANS,
        fontSize: 28,
        fontWeight: 700,
        padding: '9px 20px',
        borderRadius: 999,
        whiteSpace: 'nowrap',
      }}
    >
      Sous-agent
    </div>
  );
};

// Noms des pièces en travaux, lisibles sur téléphone (posés sur les étiquettes d'origine).
export const EtiquettesTravaux: React.FC<{f: number}> = ({f}) => {
  const c = camera(f);
  const entree = prog(f, TRAVAUX.retour + 6, 10, easeOut);
  const sortie = prog(f, RECUL.debut, 10, easeIn);
  const opacite = Math.min(1, entree * 3) * (1 - sortie);
  if (opacite <= 0) return null;
  return (
    <AbsoluteFill style={{fontFamily: SANS, opacity: opacite}}>
      {PIECES_WEALTH.map((piece, k) => {
        const v = intensitePiece(f, k);
        const pos = versEcran(c, IDX_WEALTH, piece.etiquette.x, piece.etiquette.y);
        return (
          <div
            key={piece.nom}
            style={{
              position: 'absolute',
              left: pos.x,
              top: pos.y,
              transform: `translate(-50%, -50%) scale(${(0.7 + 0.3 * entree) * (1 + 0.08 * v)})`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: 12,
              minWidth: (piece.etiquette.w + 24) * c.s,
              boxSizing: 'border-box',
              padding: '10px 20px 10px 16px',
              borderRadius: 999,
              background: C.carte,
              border: `3px solid ${v > 0.02 ? `rgba(242, 180, 0, ${0.35 + 0.65 * v})` : 'rgba(17,18,20,0.06)'}`,
              boxShadow: `0 8px 22px rgba(40, 32, 20, 0.14), 0 0 0 ${10 * v}px rgba(242, 180, 0, ${0.25 * v})`,
              whiteSpace: 'nowrap',
            }}
          >
            <span style={{width: 14, height: 14, borderRadius: 7, background: C.travaux}} />
            <span style={{fontSize: 32, fontWeight: 800, letterSpacing: '-0.02em', color: C.encre}}>{piece.nom}</span>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};


// Étape 4 : la tâche validée fait avancer l'étage Business (carte reprise de l'Ascenseur).
export const ProgressionEtage: React.FC<{f: number}> = ({f}) => {
  const entree = prog(f, SALLE.recul[1] - 14, 16, easeOut);
  const sortie = prog(f, COCKPIT.entree - 10, 12, easeIn);
  if (entree <= 0 || sortie >= 1) return null;
  const avance = prog(f, SALLE.niveau, 22, easeInOut);
  const e = ETAGES[IDX_BUSINESS];
  const pct = e.pourcentage + avance;
  return (
    <div
      style={{
        position: 'absolute',
        left: 90,
        width: 900,
        top: 1400 + (1 - entree) * 80,
        opacity: entree * (1 - sortie),
        background: C.carte,
        borderRadius: 30,
        boxShadow: C.ombre,
        border: '1px solid rgba(17,18,20,0.05)',
        padding: '26px 34px 30px',
        fontFamily: SANS,
      }}
    >
      <div style={{display: 'flex', alignItems: 'center'}}>
        <span style={{width: 90, fontFamily: MONO, fontSize: 28, fontWeight: 700, color: C.accent}}>{e.numero}</span>
        <span style={{flex: 1, fontSize: 40, fontWeight: 800, letterSpacing: '-0.02em', color: C.encre}}>{e.nom}</span>
        <span style={{fontFamily: MONO, fontSize: 40, fontWeight: 700, color: avance > 0.5 ? C.accent : C.encre}}>{Math.round(pct)}%</span>
      </div>
      <div style={{marginTop: 18, height: 14, borderRadius: 99, background: '#e9e5de', overflow: 'hidden'}}>
        <div style={{width: `${Math.max(1.2, pct) * 3}%`, height: '100%', borderRadius: 99, background: C.accent}} />
      </div>
      <div style={{marginTop: 14, fontSize: 24, color: C.gris}}>Sales : 1 tâche faite sur 17</div>
    </div>
  );
};
