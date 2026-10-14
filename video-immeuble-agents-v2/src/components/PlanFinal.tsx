import React from 'react';
import {AbsoluteFill} from 'remotion';
import {clamp01, easeInOut, easeOut, prog} from '../anim';
import {SANS} from '../theme';
import {FINAL} from '../timeline';
import {projeter, SceneAvatar, type PlanCamera} from './Avatar3D';

// Plan de départ : même cadrage que la capture du jeu (vue isométrique, avatar d'environ 245 px).
const ISO: PlanCamera = {azimut: 55, elevation: 31.6, champ: 10, cible: [0, 1, 0], echelle: (2 * 1920) / 245, ecranY: 1150};
// Plan d'arrivée : plan rapproché de trois quarts, légèrement en contre-plongée.
const PROCHE: PlanCamera = {azimut: 36, elevation: 7, champ: 30, cible: [0, 1.5, 0], echelle: 2.75, ecranY: 1250};
// Tenue finale : la caméra continue de glisser très lentement.
const DERIVE: PlanCamera = {azimut: 40, elevation: 7.5, champ: 30, cible: [0, 1.52, 0], echelle: 2.62, ecranY: 1250};

const melange = (p: PlanCamera, q: PlanCamera, t: number): PlanCamera => ({
  azimut: p.azimut + (q.azimut - p.azimut) * t,
  elevation: p.elevation + (q.elevation - p.elevation) * t,
  champ: p.champ + (q.champ - p.champ) * t,
  cible: [0, 1, 2].map((k) => p.cible[k] + (q.cible[k] - p.cible[k]) * t) as [number, number, number],
  echelle: Math.exp(Math.log(p.echelle) + (Math.log(q.echelle) - Math.log(p.echelle)) * t),
  ecranY: p.ecranY + (q.ecranY - p.ecranY) * t,
});

export const planAvatar = (f: number) => {
  const t = prog(f, FINAL.bascule, FINAL.arrivee - FINAL.bascule, easeInOut);
  const tenue = clamp01((f - FINAL.arrivee) / Math.max(1, FINAL.fin - FINAL.arrivee));
  return melange(melange(ISO, PROCHE, t), DERIVE, tenue);
};

// Lumière douce derrière le personnage + léger vignettage (profondeur, sans effet néon).
export const LumiereFinale: React.FC<{f: number}> = ({f}) => {
  const a = prog(f, FINAL.bascule + 6, 40, easeInOut);
  if (a <= 0) return null;
  return (
    <AbsoluteFill
      style={{
        opacity: a,
        background: 'radial-gradient(ellipse 620px 760px at 540px 1020px, rgba(255, 251, 243, 0.85), rgba(255, 251, 243, 0) 70%)',
      }}
    />
  );
};

export const PlanFinal: React.FC<{f: number}> = ({f}) => {
  if (f < FINAL.bascule - 1) return null;
  const plan = planAvatar(f);
  const opacite = prog(f, FINAL.bascule, 12, easeOut);
  const t = prog(f, FINAL.bascule, FINAL.arrivee - FINAL.bascule, easeInOut);
  const respiration = Math.sin(f / 22);
  const tete = Math.sin(f / 47) * 0.5 * clamp01((f - FINAL.arrivee + 30) / 40);
  // étiquette du joueur, comme dans le jeu, au-dessus de la tête
  const nom = prog(f, FINAL.arrivee - 14, 16, easeOut);
  const pos = projeter(plan, [0, 2.3, 0]);
  const vignette = prog(f, FINAL.bascule + 10, 40, easeInOut);
  return (
    <>
      <SceneAvatar plan={plan} respiration={respiration} tete={tete} ombre={1 - t} opacite={opacite} />
      <AbsoluteFill
        style={{
          opacity: vignette,
          background: 'radial-gradient(ellipse 760px 1150px at 540px 1000px, rgba(0,0,0,0) 62%, rgba(40, 30, 18, 0.16) 100%)',
        }}
      />
      {nom > 0 ? (
        <div
          style={{
            position: 'absolute',
            left: pos.x,
            top: pos.y,
            transform: `translate(-50%, -100%) translateY(${(1 - nom) * 14}px)`,
            opacity: nom,
            background: '#1c1d22',
            color: '#fff',
            fontFamily: SANS,
            fontSize: 34,
            fontWeight: 700,
            padding: '10px 28px',
            borderRadius: 999,
            boxShadow: '0 10px 24px rgba(20, 16, 10, 0.2)',
          }}
        >
          Daouda
        </div>
      ) : null}
    </>
  );
};

