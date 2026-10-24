import {AbsoluteFill, Img, staticFile} from 'remotion';

/**
 * Flat near-black with a static 36 px grid anchored top-left and a faint dithered lift behind the hero.
 * Pre-rendered by pipeline/motion.py (exact pixels, dither included), so it never moves or bands.
 */
export const Background: React.FC<{src: string; color: string}> = ({src, color}) => (
  <AbsoluteFill style={{backgroundColor: color}}>
    {src ? <Img src={staticFile(src)} style={{width: '100%', height: '100%'}} /> : null}
  </AbsoluteFill>
);
