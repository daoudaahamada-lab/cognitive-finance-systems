import React from 'react';
import {easeIn, easeInOut, easeOut, prog} from '../anim';
import {BADGES_TRAVAUX, CAPTURES, PANNEAU} from '../data';
import {TRAVAUX} from '../timeline';
import {intensitePiece} from './Immeuble';
import {Jaune, PanneauCapture} from './PanneauCapture';

// Scène 4 : le panneau "Ce qui est en travaux" (capture 08).
// Chaque badge clignote en même temps que sa pièce sur l'étage Wealth.
export const PanneauTravaux: React.FC<{f: number}> = ({f}) => {
  const entree = prog(f, TRAVAUX.panneau, 28, easeOut);
  const sortie = prog(f, TRAVAUX.sortiePanneau, 18, easeIn);
  if (entree <= 0 || sortie >= 1) return null;
  const dy = (1 - entree) * 1000 + sortie * 1000;
  const defile = 772 * prog(f, TRAVAUX.defile, 32, easeInOut);
  const marqueur = prog(f, TRAVAUX.marqueur, 14, easeOut);
  const b = BADGES_TRAVAUX;
  return (
    <PanneauCapture
      src={CAPTURES.travaux}
      decoupe={PANNEAU}
      left={114}
      top={975}
      largeur={852}
      hauteur={828}
      defile={defile}
      dy={dy}
      filtre="contrast(1.12) brightness(1.015)"
    >
      {/* "9 pièces en travaux" passé au surligneur */}
      <Jaune x={36} y={138} w={232} h={34} rayon={6} intensite={0.55} etire={marqueur} />
      <Jaune {...b.architect} intensite={intensitePiece(f, 0)} />
      <Jaune {...b.build} intensite={intensitePiece(f, 1)} />
      <Jaune {...b.run} intensite={intensitePiece(f, 2)} />
    </PanneauCapture>
  );
};
