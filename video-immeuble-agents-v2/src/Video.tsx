import React from 'react';
import {AbsoluteFill, Html5Audio, interpolate, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {Ascenseur} from './components/Ascenseur';
import {CartesProjets} from './components/Cartes';
import {CarteCockpit} from './components/Cockpit';
import {Hud} from './components/Hud';
import {EtiquetteSousAgent, EtiquettesTour, EtiquettesTravaux, Immeuble, ProgressionEtage} from './components/Immeuble';
import {LumiereFinale, PlanFinal} from './components/PlanFinal';
import {JetonCredits, PanneauSales} from './components/Salle';
import {SousTitres} from './components/SousTitres';
import {C} from './theme';
import {chuteEtage, COCKPIT, CREDITS, DUREE_TOTALE, ETIQUETTES_TOUR, FINAL, PLONGEE, POURCENTAGES, R, RECUL, SALLE, TOUR, TRAVAUX} from './timeline';
import {LIGNES} from './voix';

export type VideoProps = {
  // Voix off phrase par phrase (public/voix/Lxx.wav). false = version muette, à doubler soi-même.
  voix: boolean;
  // Sous-titres de la voix off en haut d'écran (recommandé : la plupart des vidéos sont lues sans le son).
  sousTitres: boolean;
  // Musique facultative dans public/ (ex. "musique.mp3"), mixée sous la voix.
  musique: string;
};

export const ImmeubleAgentsV2: React.FC<VideoProps> = ({voix, sousTitres, musique}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: C.fond}}>
      {f >= FINAL.bascule ? <LumiereFinale f={f} /> : null}
      {f >= TOUR.debut - 2 ? <Immeuble f={f} /> : null}

      {/* 3. L'organisation */}
      {f >= ETIQUETTES_TOUR.entree && f < ETIQUETTES_TOUR.sortie + 14 ? (
        <EtiquettesTour f={f} entree={ETIQUETTES_TOUR.entree} sortie={ETIQUETTES_TOUR.sortie} />
      ) : null}
      {f >= SALLE.anneau && f < SALLE.panneau + 20 ? <EtiquetteSousAgent f={f} /> : null}

      {/* 5. Le suivi : pièces en travaux */}
      {f >= R.L14.debut - 6 && f < RECUL.debut + 12 ? <EtiquettesTravaux f={f} /> : null}

      {/* 6. Le sens : avancement de chaque domaine */}
      {f >= POURCENTAGES.entree && f < POURCENTAGES.sortie + 14 ? (
        <EtiquettesTour f={f} entree={POURCENTAGES.entree} sortie={POURCENTAGES.sortie} pourcentage />
      ) : null}

      {/* 1-2. Le point de départ : les projets en vrac rejoignent l'immeuble */}
      {f < chuteEtage(0) + 40 ? <CartesProjets f={f} /> : null}

      {(f >= PLONGEE.debut && f < SALLE.zoom[1] + 4) || (f >= TRAVAUX.attention && f < RECUL.debut + 16) ? <Ascenseur f={f} /> : null}

      {/* 4. La mécanique */}
      {f >= SALLE.panneau && f < SALLE.sortie + 22 ? <PanneauSales f={f} /> : null}
      {f >= SALLE.hud && f < SALLE.hudSortie + 16 ? <Hud f={f} /> : null}
      {f >= CREDITS.envol && f < CREDITS.arrivee + 2 ? <JetonCredits f={f} /> : null}
      {f >= SALLE.recul[0] && f < COCKPIT.entree + 4 ? <ProgressionEtage f={f} /> : null}

      {/* 5. Le suivi : objectifs du jour */}
      {f >= COCKPIT.entree && f < COCKPIT.sortie + 4 ? <CarteCockpit f={f} /> : null}

      {/* 6. Plan final sur l'avatar */}
      {f >= FINAL.bascule - 1 ? <PlanFinal f={f} /> : null}

      <SousTitres f={f} texte={sousTitres} />

      {voix
        ? LIGNES.map((l) => (
            <Sequence key={l.id} from={R[l.id].debut} durationInFrames={R[l.id].duree + 15} layout="none">
              <Html5Audio src={staticFile(`voix/${l.id}.wav`)} />
            </Sequence>
          ))
        : null}
      {musique ? (
        <Html5Audio
          src={staticFile(musique)}
          volume={(t) =>
            interpolate(t, [0, 30, DUREE_TOTALE - 60, DUREE_TOTALE], [0, voix ? 0.22 : 0.7, voix ? 0.22 : 0.7, 0], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            })
          }
        />
      ) : null}
    </AbsoluteFill>
  );
};
