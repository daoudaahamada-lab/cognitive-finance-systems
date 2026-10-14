import React from 'react';
import {Composition} from 'remotion';
import './fonts';
import {DUREE_TOTALE, FPS} from './timeline';
import {ImmeubleAgentsV2, type VideoProps} from './Video';

const defaut: VideoProps = {voix: true, sousTitres: true, musique: ''};

export const RemotionRoot: React.FC = () => (
  <Composition
    id="ImmeubleAgentsV2"
    component={ImmeubleAgentsV2}
    durationInFrames={DUREE_TOTALE}
    fps={FPS}
    width={1080}
    height={1920}
    defaultProps={defaut}
  />
);
