import React from 'react';
import {interpolateColors} from 'remotion';
import {clamp01, clignote, easeDouce, easeIn, easeOut, piste, prog} from '../anim';
import {ETAGES} from '../data';
import {C, MONO, SANS} from '../theme';
import {AGENTS, clesEtage, PLONGEE, RECUL, SALLE, TRAVAUX} from '../timeline';
import {pourcentageAffiche} from './Immeuble';

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
  const legende = prog(f, AGENTS - 4, 10, easeOut);
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
      {attention ? (
        <div style={{position: 'absolute', right: 40, top: 26, display: 'flex', alignItems: 'center', gap: 10, fontSize: 22, color: C.gris}}>
          <span style={{width: 12, height: 12, borderRadius: 6, background: C.travaux}} />
          En travaux
        </div>
      ) : (
        <div
          style={{
            position: 'absolute',
            right: 30,
            top: 20,
            display: 'flex',
            alignItems: 'center',
            gap: 10,
            fontSize: 22,
            padding: '6px 14px',
            borderRadius: 999,
            background: `rgba(47, 107, 255, ${0.1 * legende})`,
            color: interpolateColors(legende, [0, 1], [C.gris, C.accent]),
            fontWeight: legende > 0.5 ? 700 : 500,
          }}
        >
          <span style={{width: 12, height: 12, borderRadius: 6, background: C.accent}} />
          Un agent IA par étage
        </div>
      )}
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
              {attention ? (
                <div style={{display: 'flex', alignItems: 'center', gap: 16}}>
                  <span style={{fontFamily: MONO, fontSize: 28, fontWeight: 700, color: enTravaux ? '#b98a00' : C.encre}}>{pourcentageAffiche(i, f)}%</span>
                  <span style={{width: 14, height: 14, borderRadius: 7, background: enTravaux ? C.travaux : C.accent}} />
                </div>
              ) : (
                (() => {
                  // « Agent IA » : une pastille par étage, l'une après l'autre
                  const p = prog(f, AGENTS + i * 4, 10, easeOut);
                  return (
                    <div
                      style={{
                        opacity: p,
                        transform: `translateX(${(1 - p) * 24}px) scale(${0.9 + 0.1 * p})`,
                        display: 'flex',
                        alignItems: 'center',
                        gap: 8,
                        padding: '7px 14px',
                        borderRadius: 999,
                        background: C.accent,
                        color: '#fff',
                        fontSize: 21,
                        fontWeight: 700,
                        whiteSpace: 'nowrap',
                      }}
                    >
                      <span style={{width: 9, height: 9, borderRadius: 5, background: '#fff'}} />
                      Agent IA
                    </div>
                  );
                })()
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};
