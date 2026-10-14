import React from 'react';
import {interpolateColors} from 'remotion';
import {clamp01, clignote, easeDouce, easeIn, easeOut, piste, prog} from '../anim';
import {ETAGES} from '../data';
import {C, MONO, SANS} from '../theme';
import {a, clesEtage, PLONGEE, RECUL, SALLE, TRAVAUX} from '../timeline';

const HAUT = 1236;
const ENTETE = 76;
const RANG = 98;

// Carte "Ascenseur" reprise de l'application.
// Étape 3 : la sélection suit la caméra. Étape 5 : les domaines en travaux ressortent en jaune.
export const Ascenseur: React.FC<{f: number}> = ({f}) => {
  const attention = f >= SALLE.zoom[1] + 30;
  const entree = attention ? prog(f, TRAVAUX.attention, 24, easeOut) : prog(f, PLONGEE.debut + 6, 26, easeOut);
  const sortie = attention ? prog(f, RECUL.debut - 4, 18, easeIn) : prog(f, SALLE.zoom[0], 22, easeIn);
  if (entree <= 0 || sortie >= 1) return null;
  const dy = (1 - entree) * 760 + sortie * 760;
  const position = f < PLONGEE.fin ? 0 : piste(f, clesEtage, easeDouce);
  const impulsionAgents = clignote(f, a('L07', 0.55), 1, 16);
  const alerte = Math.max(0.35, clignote(f, TRAVAUX.alerte, 2, 14));
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
      <div style={{position: 'absolute', left: 36, top: 30, fontSize: 22, fontWeight: 700, letterSpacing: '0.2em', color: C.grisClair}}>ASCENSEUR</div>
      {/* légende des statuts, reprise de l'application */}
      <div style={{position: 'absolute', right: 40, top: 26, display: 'flex', alignItems: 'center', gap: 10, fontSize: 22, color: C.gris}}>
        <span style={{width: 12, height: 12, borderRadius: 6, background: attention ? C.travaux : C.accent}} />
        {attention ? 'En travaux' : 'Agent en service'}
      </div>
      {!attention ? (
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
      ) : null}
      {ETAGES.map((e, i) => {
        const proche = attention ? 0 : clamp01(1 - Math.abs(position - i));
        const couleurNumero = interpolateColors(proche, [0, 1], [C.grisClair, C.accent]);
        const enTravaux = e.statut === 'travaux';
        return (
          <div key={e.nom} style={{position: 'absolute', left: 0, right: 0, top: ENTETE + i * RANG, height: RANG}}>
            {attention && enTravaux ? (
              <div
                style={{
                  position: 'absolute',
                  left: 14,
                  right: 14,
                  top: 4,
                  bottom: 4,
                  borderRadius: 22,
                  background: `rgba(242, 180, 0, ${0.1 + 0.12 * alerte})`,
                  border: `2.5px solid rgba(242, 180, 0, ${0.5 + 0.5 * alerte})`,
                }}
              />
            ) : null}
            <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', padding: '0 40px 0 36px'}}>
              <div style={{width: 104, fontFamily: MONO, fontSize: 28, fontWeight: 700, color: couleurNumero}}>{e.numero}</div>
              <div style={{flex: 1, minWidth: 0}}>
                <div style={{fontSize: 36, fontWeight: 800, letterSpacing: '-0.02em', color: C.encre, lineHeight: 1.1}}>{e.nom}</div>
                <div style={{fontSize: 23, fontWeight: 500, color: C.gris, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', marginTop: 3}}>
                  {e.description}
                </div>
              </div>
              <div style={{display: 'flex', alignItems: 'center', gap: 16}}>
                <span
                  style={{
                    fontFamily: MONO,
                    fontSize: attention ? 28 : 24,
                    fontWeight: attention ? 700 : 500,
                    color: attention ? (enTravaux ? '#b98a00' : C.encre) : C.gris,
                  }}
                >
                  {e.pourcentage}%
                </span>
                <span
                  style={{
                    width: 14,
                    height: 14,
                    borderRadius: 7,
                    background: enTravaux ? C.travaux : C.accent,
                    transform: `scale(${1 + (enTravaux ? 0 : 0.6 * impulsionAgents)})`,
                  }}
                />
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
