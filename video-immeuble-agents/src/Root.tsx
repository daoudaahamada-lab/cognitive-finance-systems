import React from 'react';
import {Composition} from 'remotion';
import './fonts';
import {DUREE_TOTALE, FPS} from './timeline';
import {ImmeubleAgents, type VideoProps} from './Video';

const defaut: VideoProps = {musique: ''};

export const RemotionRoot: React.FC = () => (
  <Composition
    id="ImmeubleAgents"
    component={ImmeubleAgents}
    durationInFrames={DUREE_TOTALE}
    fps={FPS}
    width={1080}
    height={1920}
    defaultProps={defaut}
  />
);
