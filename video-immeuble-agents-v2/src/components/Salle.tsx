import React from 'react';
import {clamp01, easeIn, easeInOut, easeOut, prog} from '../anim';
import {BOUTON_FERMER_SALES, CAPTURES, PANNEAU, SALES_V2} from '../data';
import {C, MONO, SANS} from '../theme';
import {CREDITS, SALLE} from '../timeline';
import {POSITION_CREDITS} from './Hud';
import {PanneauCapture, Surlignage} from './PanneauCapture';

// Fenêtre du panneau Sales à l'écran (capture 07).
const P = {left: 40, top: 770, largeur: 1000, hauteur: 1090};
const K = P.largeur / PANNEAU.w;
const defileA = (f: number) => 200 * prog(f, SALLE.defile, 24, easeInOut);
const dyA = (f: number) => (1 - prog(f, SALLE.panneau, 28, easeOut)) * 1200 + prog(f, SALLE.sortie, 20, easeIn) * 1200;
const versEcranPanneau = (f: number, x: number, y: number) => ({x: P.left + x * K, y: P.top + (y - defileA(f)) * K + dyA(f)});

// « Arsenal de prospection » passe de 0/6 à 1/6 quand la tâche est cochée.
const CompteurGroupe: React.FC<{f: number}> = ({f}) => {
  const p = prog(f, SALLE.coche + 4, 10, easeOut);
  if (p <= 0) return null;
  const k = SALES_V2.compteur;
  return (
    <div
      style={{
        position: 'absolute',
        left: k.x,
        top: k.y,
        width: k.w,
        height: k.h,
        background: k.fond,
        overflow: 'hidden',
        fontFamily: MONO,
        fontSize: 25,
        fontWeight: 500,
        lineHeight: `${k.h}px`,
        textAlign: 'right',
        color: '#55565a',
      }}
    >
      <div style={{transform: `translateY(${(1 - p) * 100}%)`, color: p < 1 ? C.accent : '#55565a'}}>1/6</div>
      <div style={{position: 'absolute', right: 0, top: 0, transform: `translateY(${-p * 100}%)`}}>0/6</div>
    </div>
  );
};

// Coche animée sur la première tâche.
const Coche: React.FC<{f: number}> = ({f}) => {
  const p = prog(f, SALLE.coche, 10, easeOut);
  if (p <= 0) return null;
  const c = SALES_V2.case;
  const trace = prog(f, SALLE.coche + 3, 10, easeInOut);
  return (
    <div
      style={{
        position: 'absolute',
        left: c.x - 2,
        top: c.y - 2,
        width: c.w + 4,
        height: c.h + 4,
        borderRadius: 9,
        background: C.accent,
        transform: `scale(${0.6 + 0.4 * p + 0.12 * Math.sin(Math.PI * p)})`,
      }}
    >
      <svg viewBox="0 0 40 40" width="100%" height="100%">
        <path d="M10 21 L17 28 L30 13" fill="none" stroke="#fff" strokeWidth={4.5} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - trace} />
      </svg>
    </div>
  );
};

export const PanneauSales: React.FC<{f: number}> = ({f}) => {
  const dy = dyA(f);
  if (dy >= 1199) return null;
  const b = BOUTON_FERMER_SALES;
  const l = SALES_V2.ligne;
  const cr = SALES_V2.credits;
  const fait = prog(f, SALLE.coche + 6, 12, easeOut);
  const repere = prog(f, SALLE.coche + 2, 10, easeOut) * (1 - prog(f, CREDITS.envol + 4, 8));
  return (
    <PanneauCapture src={CAPTURES.salleSales} decoupe={PANNEAU} left={P.left} top={P.top} largeur={P.largeur} hauteur={P.hauteur} defile={defileA(f)} dy={dy}>
      <div style={{position: 'absolute', left: b.x, top: b.y, width: b.w, height: b.h, background: C.carte}} />
      <Surlignage f={f} debut={SALLE.mission} fin={SALLE.objectif - 10} {...SALES_V2.mission} label="Sa mission" />
      <Surlignage f={f} debut={SALLE.objectif} {...SALES_V2.objectif} label="Objectif" />
      <Surlignage f={f} debut={SALLE.taches} hautEtiquette={-4} {...SALES_V2.taches} label="Tâches" />
      <CompteurGroupe f={f} />
      {/* la tâche validée passe en retrait */}
      <div style={{position: 'absolute', left: l.x, top: l.y, width: l.w, height: l.h, background: C.carte, opacity: 0.45 * fait}} />
      <Coche f={f} />
      {repere > 0 ? (
        <div style={{position: 'absolute', left: cr.x - 8, top: cr.y - 6, width: cr.w + 16, height: cr.h + 12, borderRadius: 10, border: `3px solid ${C.accent}`, opacity: repere}} />
      ) : null}
    </PanneauCapture>
  );
};

// Le gain « +30 crédits » quitte la tâche et rejoint le compteur de crédits.
export const JetonCredits: React.FC<{f: number}> = ({f}) => {
  const t = prog(f, CREDITS.envol, CREDITS.arrivee - CREDITS.envol, easeInOut);
  if (f < CREDITS.envol || t >= 1) return null;
  const cr = SALES_V2.credits;
  const depart = versEcranPanneau(f, cr.x + cr.w / 2, cr.y + cr.h / 2);
  const arrivee = POSITION_CREDITS;
  const x = depart.x + (arrivee.x - depart.x) * t;
  const y = depart.y + (arrivee.y - depart.y) * t - Math.sin(Math.PI * t) * 140;
  const apparition = clamp01((f - CREDITS.envol) / 5);
  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y,
        transform: `translate(-50%, -50%) scale(${(0.8 + 0.2 * apparition) * (1 - 0.35 * t)})`,
        opacity: apparition * (1 - prog(f, CREDITS.arrivee - 4, 4)),
        background: C.accent,
        color: '#fff',
        fontFamily: SANS,
        fontSize: 30,
        fontWeight: 800,
        padding: '10px 22px',
        borderRadius: 999,
        whiteSpace: 'nowrap',
        boxShadow: '0 10px 24px rgba(20, 30, 60, 0.18)',
        zIndex: 50,
      }}
    >
      +{CREDITS.gain} crédits
    </div>
  );
};
