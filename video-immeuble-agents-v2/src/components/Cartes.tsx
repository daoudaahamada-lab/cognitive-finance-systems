import React from 'react';
import {interpolateColors} from 'remotion';
import {clamp01, easeInOut, easeOut, prog} from '../anim';
import {CARTES_PROJETS, CENTRE_ETAGE, type CarteProjet} from '../data';
import {C, MONO, SANS} from '../theme';
import {CARTES, chuteEtage} from '../timeline';
import {camera, versEcran} from './Immeuble';

// Pastille de salle, dans le style des étiquettes de l'application.
export const Pastille: React.FC<{carte: CarteProjet; point: string; echelle?: number}> = ({carte, point, echelle = 1}) => (
  <div
    style={{
      display: 'inline-flex',
      alignItems: 'center',
      gap: 14 * echelle,
      padding: `${13 * echelle}px ${22 * echelle}px ${13 * echelle}px ${18 * echelle}px`,
      borderRadius: 999,
      background: '#fdfdfc',
      boxShadow: '0 10px 28px rgba(40, 32, 20, 0.12), 0 2px 6px rgba(40, 32, 20, 0.06)',
      fontFamily: SANS,
      whiteSpace: 'nowrap',
    }}
  >
    <span style={{width: 13 * echelle, height: 13 * echelle, borderRadius: 99, background: point}} />
    <span style={{fontSize: 29 * echelle, fontWeight: 700, letterSpacing: '-0.015em', color: C.encre}}>{carte.nom}</span>
    <span style={{fontFamily: MONO, fontSize: 22 * echelle, fontWeight: 700, color: '#8b8b8b'}}>
      {carte.projets} proj. · {carte.faites}/{carte.total}
    </span>
    {carte.travaux ? (
      <span
        style={{
          fontSize: 17 * echelle,
          fontWeight: 800,
          letterSpacing: '0.06em',
          padding: `${4 * echelle}px ${11 * echelle}px`,
          borderRadius: 999,
          background: C.travaux,
          color: '#1a1712',
        }}
      >
        TRAVAUX
      </span>
    ) : null}
  </div>
);

// Étapes 1 et 2 : les projets en vrac, puis chacun rejoint son étage quand l'immeuble se construit.
export const CartesProjets: React.FC<{f: number}> = ({f}) => {
  const desordre = prog(f, CARTES.desordre[0], CARTES.desordre[1] - CARTES.desordre[0], easeInOut);
  const cam = camera(f);
  return (
    <>
      {CARTES_PROJETS.map((carte, k) => {
        const apparition = prog(f, CARTES.apparition + k * 5, 14, easeOut);
        if (apparition <= 0) return null;
        // domaine nommé par la voix : le point passe au bleu, petite impulsion
        const tDomaine = carte.etage < 4 ? CARTES.domaines[carte.etage] : 1e9;
        const nomme = prog(f, tDomaine, 8, easeOut);
        const impulsion = Math.sin(Math.PI * clamp01((f - tDomaine) / 14)) * (f >= tDomaine ? 1 : 0);
        // flottement, qui s'emballe pendant « je ne savais jamais où j'en étais »
        const amp = 6 + 34 * desordre;
        const vit = 1 + 1.6 * desordre;
        const fx = Math.sin((f * vit) / 37 + k * 1.7) * amp;
        const fy = Math.cos((f * vit) / 45 + k * 2.3) * amp * 0.8;
        const rot = carte.r + Math.sin((f * vit) / 29 + k) * (1.5 + 5 * desordre);
        // envol vers son étage pendant la construction de l'immeuble
        const t0 = chuteEtage(carte.etage) - 16 + (k % 3) * 2;
        const envol = prog(f, t0, 24, easeInOut);
        if (envol >= 1) return null;
        const cible = versEcran(cam, carte.etage, CENTRE_ETAGE.x + ((k % 3) - 1) * 260, CENTRE_ETAGE.y - 120);
        const x0 = carte.x + fx;
        const y0 = carte.y + fy;
        const x = x0 + (cible.x - x0) * envol;
        const y = y0 + (cible.y - y0) * envol - Math.sin(Math.PI * envol) * 120;
        const echelle = (0.85 + 0.15 * apparition) * (1 - 0.07 * desordre) * (1 + 0.08 * impulsion) * (1 - 0.75 * envol);
        const point = interpolateColors(nomme, [0, 1], ['#b9b4ab', C.accent]);
        return (
          <div
            key={carte.nom}
            style={{
              position: 'absolute',
              left: x,
              top: y,
              transform: `translate(-50%, -50%) rotate(${rot * (1 - envol)}deg) scale(${echelle})`,
              opacity: Math.min(apparition, 1 - prog(f, t0 + 12, 12)) * (1 - 0.25 * desordre * ((k % 4) / 3)),
              filter: desordre > 0.05 && k % 4 === 3 ? `blur(${2.5 * desordre}px)` : undefined,
              zIndex: 20 + k,
            }}
          >
            <Pastille carte={carte} point={point} />
          </div>
        );
      })}
    </>
  );
};

