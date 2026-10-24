import {useCurrentFrame} from 'remotion';
import type {CaptionGroup, Style} from './types';

/**
 * Karaoke captions: one centred line, baseline fixed, the word being spoken in the accent colour.
 * Hard cuts only: a group appears on its first word's onset and stays through the following pause;
 * the accent jumps to each word on its onset frame (no fade, no scale, nothing moves).
 * SVG text puts the baseline exactly at style.caption.baseline.
 */
export const Captions: React.FC<{groups: CaptionGroup[]; style: Style; width: number; height: number}> = ({
  groups,
  style,
  width,
  height,
}) => {
  const frame = useCurrentFrame();
  const group = groups.find((g) => frame >= g.from && frame < g.to);
  if (!group) return null;
  // The first group is on screen from frame 0; its first word only turns red on its own onset.
  let active = -1;
  group.words.forEach((w, i) => {
    if (frame >= w.from) active = i;
  });
  const c = style.caption;
  return (
    <svg width={width} height={height} style={{position: 'absolute', inset: 0}}>
      <text
        x={width / 2}
        y={c.baseline}
        textAnchor="middle"
        style={{
          fontFamily: `'${style.font_family}'`,
          fontWeight: c.weight,
          fontSize: c.size,
          letterSpacing: `${c.tracking_em}em`,
          whiteSpace: 'pre',
          fontKerning: 'normal',
        }}
      >
        {group.words.map((w, i) => (
          <tspan key={w.i} fill={i === active ? style.accent : style.cream}>
            {(i > 0 ? ' ' : '') + w.text}
          </tspan>
        ))}
      </text>
    </svg>
  );
};
