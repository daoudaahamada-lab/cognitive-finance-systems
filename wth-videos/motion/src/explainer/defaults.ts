import type {ExplainerProps} from './types';

// Placeholder props for `remotion studio`; real renders always pass --props=build/Vxx/motion.json.
export const defaultExplainerProps: ExplainerProps = {
  id: 'demo',
  fps: 30,
  width: 1080,
  height: 1920,
  durationInFrames: 60,
  style: {
    bg: '#0A0A0B',
    cream: '#F6F0E4',
    accent: '#FF4A5C',
    fill: '#DC1835',
    fill_shadow: '#7A0E14',
    font_family: 'WTH Inter',
    stage: {cx: 540, cy: 800, box: [720, 600]},
    hero_mask: {top0: 130, top1: 230, bottom0: 1150, bottom1: 1262},
    caption: {size: 66, weight: 800, tracking_em: -0.015, baseline: 1350, max_width: 760},
    motion: {enter: 11, enter_fade: 1, enter_from: 0.7, exit: 8, exit_fade: 4.5, exit_ease: 'in-out', exit_to: 0.8, move: 16, tilt: 14, pop: 9, tone: 12, fade: 6},
    steps: {
      small: {d: 26, red: 34, gap: 64, stroke: 3, opacity: 0.6},
      big: {d: 112, red: 250, gap: 270, stroke: 7, opacity: 1},
      enter: 11,
      leave: 3,
      slide: 16,
    },
  },
  background: '',
  assets: {},
  shots: [],
  overlays: [],
  steps: null,
  endCard: null,
  captions: [
    {
      from: 0,
      to: 60,
      width: 0,
      words: [
        {text: 'Props', i: 0, from: 0},
        {text: 'par', i: 1, from: 20},
        {text: 'défaut', i: 2, from: 40},
      ],
    },
  ],
};
