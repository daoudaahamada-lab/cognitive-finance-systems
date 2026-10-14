import React from 'react';
import {interpolateColors} from 'remotion';
import {easeIn, easeInOut, easeOut, prog} from '../anim';
import {C, MONO, SANS} from '../theme';
import {CREDITS, SALLE} from '../timeline';

// Barre du haut du QG (capture 01) : niveau, XP, crédits, objectif, jours.
const TOP = 322;
export const POSITION_CREDITS = {x: 565, y: TOP + 40};

const Stat: React.FC<{valeur: React.ReactNode; label: string; couleur?: string; largeur: number}> = ({valeur, label, couleur, largeur}) => (
  <div style={{width: largeur}}>
    <div style={{fontFamily: MONO, fontSize: 34, fontWeight: 700, color: couleur ?? C.encre, lineHeight: 1.1}}>{valeur}</div>
    <div style={{fontSize: 15, fontWeight: 600, letterSpacing: '0.14em', color: C.grisClair, marginTop: 6}}>{label}</div>
  </div>
);

export const Hud: React.FC<{f: number}> = ({f}) => {
  const entree = prog(f, SALLE.hud, 16, easeOut);
  const sortie = prog(f, SALLE.hudSortie, 14, easeIn);
  if (entree <= 0 || sortie >= 1) return null;
  const dy = -(1 - entree) * 20 - sortie * 20;
  const gagne = prog(f, CREDITS.arrivee, 10, easeOut);
  const pulse = Math.sin(Math.PI * Math.min(1, Math.max(0, (f - CREDITS.arrivee) / 14))) * (f >= CREDITS.arrivee ? 1 : 0);
  const niveau = 0.62 + 0.1 * prog(f, SALLE.niveau, 20, easeInOut);
  const montee = Math.sin(Math.PI * Math.min(1, Math.max(0, (f - SALLE.niveau) / 26))) * (f >= SALLE.niveau ? 1 : 0);
  const carte: React.CSSProperties = {
    background: C.carte,
    borderRadius: 26,
    boxShadow: C.ombre,
    border: '1px solid rgba(17,18,20,0.05)',
    height: 100,
    boxSizing: 'border-box',
  };
  return (
    <div style={{position: 'absolute', left: 40, top: TOP, width: 1000, display: 'flex', gap: 16, transform: `translateY(${dy}px)`, opacity: entree * (1 - sortie), fontFamily: SANS}}>
      <div style={{...carte, width: 316, display: 'flex', alignItems: 'center', gap: 16, padding: '0 22px'}}>
        <div
          style={{
            width: 56,
            height: 56,
            borderRadius: 16,
            background: 'linear-gradient(160deg, #6fb6ff, #2f6bff)',
            color: '#0b1020',
            fontSize: 28,
            fontWeight: 800,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          D
        </div>
        <div style={{flex: 1}}>
          <div style={{display: 'flex', alignItems: 'baseline', gap: 10}}>
            <span style={{fontSize: 26, fontWeight: 800, color: C.encre}}>Niveau 3</span>
          </div>
          <div style={{fontSize: 16, color: C.gris, marginTop: 2}}>2 chantiers terminés</div>
          <div style={{height: 10, borderRadius: 9, background: '#e7e3dc', marginTop: 8, overflow: 'hidden', boxShadow: `0 0 0 ${3 * montee}px rgba(47, 107, 255, ${0.25 * montee})`}}>
            <div style={{width: `${niveau * 100}%`, height: '100%', borderRadius: 9, background: 'linear-gradient(90deg, #2f6bff, #2bb673)'}} />
          </div>
        </div>
      </div>
      <div style={{...carte, flex: 1, display: 'flex', alignItems: 'center', padding: '0 28px'}}>
        <Stat largeur={130} valeur="110" label="XP" />
        <div style={{width: 170, position: 'relative'}}>
          <div
            style={{
              position: 'absolute',
              left: -14,
              top: -12,
              width: 150,
              height: 82,
              borderRadius: 18,
              background: `rgba(47, 107, 255, ${0.12 * pulse})`,
            }}
          />
          <div style={{transform: `scale(${1 + 0.12 * pulse})`, transformOrigin: 'left center'}}>
            <Stat
              largeur={170}
              label="CRÉDITS"
              couleur={interpolateColors(pulse, [0, 1], [C.encre, C.accent])}
              valeur={
                <span style={{display: 'inline-block', position: 'relative', height: 38, overflow: 'hidden', verticalAlign: 'bottom'}}>
                  <span style={{display: 'block', transform: `translateY(${(1 - gagne) * 100}%)`, opacity: gagne > 0 ? 1 : 0}}>
                    {CREDITS.avant + CREDITS.gain}
                  </span>
                  <span style={{position: 'absolute', left: 0, top: 0, transform: `translateY(${-gagne * 100}%)`}}>{CREDITS.avant}</span>
                </span>
              }
            />
          </div>
        </div>
        <Stat largeur={190} valeur="8%" label="OBJECTIF 2026" />
        <Stat largeur={110} valeur="79" label="JOURS" />
      </div>
    </div>
  );
};
