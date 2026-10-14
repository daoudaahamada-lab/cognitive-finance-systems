import React from 'react';
import {interpolateColors} from 'remotion';
import {clamp01, easeIn, easeOut, piste, prog} from '../anim';
import {ETAGES} from '../data';
import {C, MONO, SANS} from '../theme';
import {clesEtage, PLONGEE, SALLE} from '../timeline';

const HAUT = 1236;
const ENTETE = 76;
const RANG = 98;

// Carte "Ascenseur" reprise de l'application : la sélection suit la caméra.
export const Ascenseur: React.FC<{f: number}> = ({f}) => {
  const position = piste(f, clesEtage);
  const entree = prog(f, PLONGEE.debut + 6, 26, easeOut);
  const sortie = prog(f, SALLE.zoom[0], 22, easeIn);
  const dy = (1 - entree) * 760 + sortie * 760;
  if (entree <= 0 || sortie >= 1) return null;
  return (
    <div
      style={{
        position: 'absolute',
        left: 60,
        width: 960,
        top: HAUT,
        height: ENTETE + RANG * ETAGES.length + 22,
        transform: `translateY(${dy}px)`,
        background: C.carte,
        borderRadius: 34,
        boxShadow: C.ombre,
        border: '1px solid rgba(17,18,20,0.05)',
        fontFamily: SANS,
        overflow: 'hidden',
      }}
    >
      <div
        style={{
          position: 'absolute',
          left: 36,
          top: 30,
          fontSize: 22,
          fontWeight: 700,
          letterSpacing: '0.2em',
          color: C.grisClair,
        }}
      >
        ASCENSEUR
      </div>
      {/* sélection */}
      <div
        style={{
          position: 'absolute',
          left: 14,
          right: 14,
          top: ENTETE + position * RANG + 4,
          height: RANG - 8,
          borderRadius: 22,
          background: C.accentDoux,
          border: `2.5px solid ${C.accent}`,
        }}
      />
      {ETAGES.map((e, i) => {
        const proche = clamp01(1 - Math.abs(position - i));
        const couleurNumero = interpolateColors(proche, [0, 1], [C.grisClair, C.accent]);
        return (
          <div
            key={e.nom}
            style={{
              position: 'absolute',
              left: 0,
              right: 0,
              top: ENTETE + i * RANG,
              height: RANG,
              display: 'flex',
              alignItems: 'center',
              padding: '0 40px 0 36px',
            }}
          >
            <div style={{width: 104, fontFamily: MONO, fontSize: 28, fontWeight: 700, color: couleurNumero}}>{e.numero}</div>
            <div style={{flex: 1, minWidth: 0}}>
              <div style={{fontSize: 36, fontWeight: 800, letterSpacing: '-0.02em', color: C.encre, lineHeight: 1.1}}>{e.nom}</div>
              <div
                style={{
                  fontSize: 23,
                  fontWeight: 500,
                  color: C.gris,
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  marginTop: 3,
                }}
              >
                {e.description}
              </div>
            </div>
            <div style={{display: 'flex', alignItems: 'center', gap: 16}}>
              <span style={{fontFamily: MONO, fontSize: 24, fontWeight: 500, color: C.gris}}>{e.pourcentage}%</span>
              <span
                style={{
                  width: 14,
                  height: 14,
                  borderRadius: 7,
                  background: e.statut === 'travaux' ? C.travaux : C.accent,
                }}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
};
