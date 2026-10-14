import React from 'react';
import {clignote, easeIn, easeInOut, easeOut, prog} from '../anim';
import {BADGES_TRAVAUX, CAPTURES, PANNEAU} from '../data';
import {TRAVAUX} from '../timeline';
import {intensitePiece} from './Immeuble';
import {Jaune, PanneauCapture} from './PanneauCapture';

// Scène 4 : le panneau "Ce qui est en travaux" (capture 08), badges qui clignotent en jaune.
export const PanneauTravaux: React.FC<{f: number}> = ({f}) => {
  const entree = prog(f, TRAVAUX.panneau, 28, easeOut);
  const sortie = prog(f, TRAVAUX.sortie, 20, easeIn);
  if (entree <= 0 || sortie >= 1) return null;
  const dy = (1 - entree) * 1000 + sortie * 1000;
  const defile = 772 * prog(f, TRAVAUX.defile, 32, easeInOut);
  const marqueur = prog(f, TRAVAUX.marqueur, 14, easeOut);
  const b = BADGES_TRAVAUX;
  const ensemble = clignote(f, TRAVAUX.tous[1], 2, 14);
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
    >
      {/* "9 pièces en travaux" passé au surligneur */}
      <Jaune x={36} y={138} w={232} h={34} rayon={6} intensite={0.55} etire={marqueur} />
      <Jaune {...b.cuisine} intensite={clignote(f, TRAVAUX.cuisine, 1, 16)} />
      <Jaune {...b.architect} intensite={intensitePiece(f, 0)} />
      <Jaune {...b.build} intensite={intensitePiece(f, 1)} />
      <Jaune {...b.run} intensite={intensitePiece(f, 2)} />
      <Jaune {...b.studio} intensite={ensemble} />
      <Jaune {...b.finance} intensite={ensemble} />
    </PanneauCapture>
  );
};
