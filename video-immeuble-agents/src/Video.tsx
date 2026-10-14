import React from 'react';
import {AbsoluteFill, Html5Audio, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {Accroche} from './components/Accroche';
import {Ascenseur} from './components/Ascenseur';
import {PanneauTravaux} from './components/Chantier';
import {Cockpit} from './components/Cockpit';
import {Fin} from './components/Fin';
import {EtiquettesTour, Immeuble} from './components/Immeuble';
import {Legende} from './components/Legende';
import {PanneauSales} from './components/Salle';
import {TEXTES} from './data';
import {C} from './theme';
import {DUREE_TOTALE, LEGENDES} from './timeline';

export type VideoProps = {
  // Chemin d'un fichier audio dans public/ (ex. "musique.mp3"). Vide = vidéo muette.
  musique: string;
};

export const ImmeubleAgents: React.FC<VideoProps> = ({musique}) => {
  const f = useCurrentFrame();
  const L = LEGENDES;
  return (
    <AbsoluteFill style={{background: C.fond}}>
      {f < 104 ? <Accroche f={f} /> : null}

      {f >= 88 && f < 790 ? <Immeuble f={f} /> : null}
      {f >= 100 && f < 196 ? <EtiquettesTour f={f} /> : null}
      {f >= 180 && f < 430 ? <Ascenseur f={f} /> : null}
      {f >= 440 && f < 580 ? <PanneauSales f={f} /> : null}
      {f >= 645 && f < 780 ? <PanneauTravaux f={f} /> : null}
      {f >= 750 && f < 1062 ? <Cockpit f={f} /> : null}
      {f >= 1036 ? <Fin f={f} /> : null}

      <Legende f={f} entree={L.etages[0]} sortie={L.etages[1]} {...TEXTES.etages} />
      <Legende f={f} entree={L.salles[0]} sortie={L.salles[1]} {...TEXTES.salles} />
      <Legende f={f} entree={L.bureaux[0]} sortie={L.bureaux[1]} {...TEXTES.bureaux} />
      <Legende f={f} entree={L.travaux[0]} sortie={L.travaux[1]} {...TEXTES.travaux} />
      <Legende f={f} entree={L.cockpit[0]} sortie={L.cockpit[1]} {...TEXTES.cockpit} />

      {musique ? (
        <Html5Audio
          src={staticFile(musique)}
          volume={(t) =>
            interpolate(t, [0, 15, DUREE_TOTALE - 45, DUREE_TOTALE], [0, 0.8, 0.8, 0], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            })
          }
        />
      ) : null}
    </AbsoluteFill>
  );
};
