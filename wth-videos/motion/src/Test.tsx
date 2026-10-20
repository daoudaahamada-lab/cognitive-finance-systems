import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {FONT_FAMILY} from './fonts';

export type TestProps = {
  /** Path relative to motion/public, e.g. "illustrations/WTH-003-04.png" */
  illustration: string;
  /** Caption words (2 to 4) */
  words: string[];
  /** Index in `words` of the word drawn in the accent colour */
  accentIndex: number;
  accentColor: string;
  durationInSeconds: number;
};

export const Test: React.FC<TestProps> = ({illustration, words, accentIndex, accentColor}) => {
  const frame = useCurrentFrame();
  const {fps, width} = useVideoConfig();

  // Scale-in with a spring, then a gentle continuous float.
  const pop = spring({frame, fps, config: {damping: 14, stiffness: 120, mass: 0.9}});
  const scale = interpolate(pop, [0, 1], [0.6, 1]);
  const opacity = interpolate(frame, [0, 8], [0, 1], {extrapolateRight: 'clamp'});
  const floatY = Math.sin((frame / fps) * Math.PI * 0.8) * 18;
  const floatRot = Math.sin((frame / fps) * Math.PI * 0.5) * 1.5;

  // Caption: words rise in one after another.
  const captionStart = 10;
  const perWord = 4;

  const imgWidth = width * 0.92; // 1536x1024 source -> ~994x662

  return (
    <AbsoluteFill style={{backgroundColor: '#000'}}>
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
        <Img
          src={staticFile(illustration)}
          style={{
            width: imgWidth,
            height: (imgWidth * 1024) / 1536,
            marginTop: -220,
            opacity,
            transform: `translateY(${floatY}px) rotate(${floatRot}deg) scale(${scale})`,
          }}
        />
      </AbsoluteFill>
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'flex-start', top: 1240}}>
        <div
          style={{
            fontFamily: `'${FONT_FAMILY}', sans-serif`,
            fontWeight: 800,
            fontSize: 92,
            letterSpacing: '-0.02em',
            color: '#F6F0E4',
            display: 'flex',
            gap: 26,
            maxWidth: 1080 - 2 * 140,
            flexWrap: 'wrap',
            justifyContent: 'center',
          }}
        >
          {words.map((w, i) => {
            const t = spring({frame: frame - captionStart - i * perWord, fps, config: {damping: 200}});
            return (
              <span
                key={i}
                style={{
                  color: i === accentIndex ? accentColor : undefined,
                  opacity: t,
                  transform: `translateY(${interpolate(t, [0, 1], [40, 0], {easing: Easing.out(Easing.quad)})}px)`,
                  display: 'inline-block',
                }}
              >
                {w}
              </span>
            );
          })}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
