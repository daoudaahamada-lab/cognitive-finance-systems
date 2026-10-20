import './fonts';
import {Composition} from 'remotion';
import {Test, type TestProps} from './Test';

const FPS = 30;

const defaultTestProps: TestProps = {
  illustration: 'illustrations/WTH-003-04.png',
  words: ['Props', 'par', 'défaut'],
  accentIndex: 1,
  accentColor: '#C8102E',
  durationInSeconds: 3,
};

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="Test"
      component={Test}
      width={1080}
      height={1920}
      fps={FPS}
      durationInFrames={3 * FPS}
      defaultProps={defaultTestProps}
      // Props (from --props=file.json) can drive the duration, e.g. the voice length.
      calculateMetadata={({props}) => ({
        durationInFrames: Math.round(props.durationInSeconds * FPS),
      })}
    />
  );
};
