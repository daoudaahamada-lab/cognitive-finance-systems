import React from 'react';
import {easeIn, easeInOut, easeOut, prog} from '../anim';
import {BOUTON_FERMER_SALES, CAPTURES, PANNEAU, SURLIGNAGES_SALES} from '../data';
import {C} from '../theme';
import {SALLE} from '../timeline';
import {PanneauCapture, Surlignage} from './PanneauCapture';

// Scène 3 : la salle Sales s'ouvre sur ses projets et ses tâches (capture 07).
export const PanneauSales: React.FC<{f: number}> = ({f}) => {
  const entree = prog(f, SALLE.panneau, 28, easeOut);
  const sortie = prog(f, SALLE.sortie, 20, easeIn);
  if (entree <= 0 || sortie >= 1) return null;
  const dy = (1 - entree) * 1200 + sortie * 1200;
  const defile = 370 * prog(f, SALLE.defile, 28, easeInOut);
  const b = BOUTON_FERMER_SALES;
  return (
    <PanneauCapture
      src={CAPTURES.salleSales}
      decoupe={PANNEAU}
      left={114}
      top={780}
      largeur={852}
      hauteur={1060}
      defile={defile}
      dy={dy}
    >
      <div style={{position: 'absolute', left: b.x, top: b.y, width: b.w, height: b.h, background: C.carte}} />
      {SURLIGNAGES_SALES.map((s, i) => (
        <Surlignage key={s.label} f={f} debut={SALLE.surlignages[i]} {...s} />
      ))}
    </PanneauCapture>
  );
};
