import './fonts';
import {Composition} from 'remotion';
import {Explainer} from './explainer/Explainer';
import {defaultExplainerProps} from './explainer/defaults';
import type {ExplainerProps} from './explainer/types';
import {defaultShortProps} from './shorts/defaults';
import {Short} from './shorts/Short';
import {TOTAL as SHORT_FRAMES} from './shorts/kit';
import type {ShortProps} from './shorts/types';
import {defaultStoryProps, Story} from './story/Story';
import type {StoryProps} from './story/types';
import {Test, type TestProps} from './Test';

const FPS = 30;

const defaultTestProps: TestProps = {
  illustration: 'fixtures/test-illustration.png',
  words: ['Props', 'par', 'défaut'],
  accentIndex: 1,
  accentColor: '#C8102E',
  durationInSeconds: 3,
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* Production composition: one explainer video per props file (pipeline/motion.py). */}
      <Composition
        id="Explainer"
        component={Explainer}
        width={1080}
        height={1920}
        fps={FPS}
        durationInFrames={60}
        defaultProps={defaultExplainerProps}
        calculateMetadata={({props}: {props: ExplainerProps}) => ({
          durationInFrames: props.durationInFrames,
          fps: props.fps,
          width: props.width,
          height: props.height,
        })}
      />
      {/* Scene-graph composition (persistent entities + keyframed tracks), one props file per film or excerpt
          (pipeline/story.py). */}
      <Composition
        id="Story"
        component={Story}
        width={1080}
        height={1920}
        fps={FPS}
        durationInFrames={60}
        defaultProps={defaultStoryProps}
        calculateMetadata={({props}: {props: StoryProps}) => ({
          durationInFrames: props.durationInFrames,
          fps: props.fps,
          width: props.width,
          height: props.height,
        })}
      />
      {/* Silent 14 s shorts (wth-videos/shorts/shorts.json, one short object as props; pipeline/shorts.py). */}
      <Composition
        id="Short"
        component={Short}
        width={1080}
        height={1920}
        fps={FPS}
        durationInFrames={SHORT_FRAMES}
        defaultProps={defaultShortProps satisfies ShortProps}
      />
      {/* Spike from the setup phase, kept as a smoke test (npm run render:test). */}
      <Composition
        id="Test"
        component={Test}
        width={1080}
        height={1920}
        fps={FPS}
        durationInFrames={3 * FPS}
        defaultProps={defaultTestProps}
        calculateMetadata={({props}) => ({
          durationInFrames: Math.ceil(props.durationInSeconds * FPS),
        })}
      />
    </>
  );
};
