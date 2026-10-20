// Flat vector drawing kit of the Story composition: ink outlines, hard shadows (+6/+6, no blur), Inter text,
// pictograms. Everything is drawn in an entity's local coordinates, centred on its origin.
//
// Colours come from props.style (pipeline/story.py STYLE) through PaletteContext: the composition is data-driven,
// changing STYLE recolours entities, background and captions alike. DEFAULT_PALETTE only serves the studio preview.
import React, {createContext, useContext} from 'react';
import {FONT_FAMILY} from '../fonts';
import {mixHex, type Mat} from './timeline';
import type {StoryStyle} from './types';

export type Palette = {
  ink: string;
  cyan: string;
  deep: string;
  light: string;
  paper: string;
  grey: string;
  slot: string;
  rule: string;
  red: string;
  aiTick: string;
};

export const DEFAULT_PALETTE: Palette = {
  ink: '#1E1416',
  cyan: '#19B3C7',
  deep: '#0A7487',
  light: '#D3F0F6',
  paper: '#FFFDF8',
  grey: '#DDD5C6',
  slot: '#F4EEE3',
  rule: '#E6DECF',
  red: '#C8102E',
  aiTick: '#9C9496',
};

export const paletteFromStyle = (s: StoryStyle): Palette => ({
  ink: s.ink,
  cyan: s.cyan,
  deep: s.deep,
  light: s.light,
  paper: s.paper,
  grey: s.grey,
  slot: s.slot ?? DEFAULT_PALETTE.slot,
  rule: s.rule ?? DEFAULT_PALETTE.rule,
  red: s.red,
  aiTick: s.ai_tick ?? DEFAULT_PALETTE.aiTick,
});

export const PaletteContext = createContext<Palette>(DEFAULT_PALETTE);
export const usePalette = (): Palette => useContext(PaletteContext);

/** Shape drawn twice: a flat ink copy offset by (dx, dy) under the shape itself (reference hard shadow). */
export const Hard: React.FC<{off?: number | [number, number]; render: (shadow: boolean) => React.ReactNode}> = ({off = 6, render}) => {
  const [dx, dy] = Array.isArray(off) ? off : [off, off];
  return (
    <>
      {dx !== 0 || dy !== 0 ? <g transform={`translate(${dx} ${dy})`}>{render(true)}</g> : null}
      {render(false)}
    </>
  );
};

/**
 * Local offset that lands as (+off, +off) px on screen whatever the entity's rotation and scale: the hard shadow
 * of a rotated tool (pen, stamp) still falls down-right, like every other shadow of the frame.
 */
export const worldShadow = (m: Mat, off: number): [number, number] => {
  const det = m[0] * m[3] - m[1] * m[2];
  if (Math.abs(det) < 1e-9) return [0, 0];
  const ia = m[3] / det;
  const ib = -m[1] / det;
  const ic = -m[2] / det;
  const id = m[0] / det;
  return [ia * off + ic * off, ib * off + id * off];
};

type TxtProps = {
  x: number;
  y: number;
  size: number;
  weight?: number;
  color?: string;
  anchor?: 'start' | 'middle' | 'end';
  children: React.ReactNode;
  opacity?: number;
  spacing?: number;
};

/** Text vertically centred on y (cap height of Inter = 0.727 em). */
export const Txt: React.FC<TxtProps> = ({x, y, size, weight = 600, color, anchor = 'start', children, opacity, spacing}) => {
  const C = usePalette();
  return (
    <text
      x={x}
      y={y + 0.3635 * size}
      textAnchor={anchor}
      fill={color ?? C.ink}
      opacity={opacity}
      style={{
        fontFamily: `'${FONT_FAMILY}'`,
        fontWeight: weight,
        fontSize: size,
        whiteSpace: 'pre',
        fontKerning: 'normal',
        letterSpacing: spacing ? `${spacing}px` : undefined,
      }}
    >
      {children}
    </text>
  );
};

export const roundRect = (x: number, y: number, w: number, h: number, r: number): string => {
  const rr = Math.max(0, Math.min(r, w / 2, h / 2));
  return (
    `M${x + rr},${y} H${x + w - rr} A${rr},${rr} 0 0 1 ${x + w},${y + rr} V${y + h - rr} ` +
    `A${rr},${rr} 0 0 1 ${x + w - rr},${y + h} H${x + rr} A${rr},${rr} 0 0 1 ${x},${y + h - rr} V${y + rr} ` +
    `A${rr},${rr} 0 0 1 ${x + rr},${y} Z`
  );
};

/** Rounded rectangle whose top-right corner is folded (document silhouette). */
export const foldedRect = (x: number, y: number, w: number, h: number, r: number, fold: number): string => {
  const rr = Math.max(0, Math.min(r, w / 2, h / 2));
  const f = Math.max(0, Math.min(fold, w / 2, h / 2));
  return (
    `M${x + rr},${y} H${x + w - f} L${x + w},${y + f} V${y + h - rr} A${rr},${rr} 0 0 1 ${x + w - rr},${y + h} ` +
    `H${x + rr} A${rr},${rr} 0 0 1 ${x},${y + h - rr} V${y + rr} A${rr},${rr} 0 0 1 ${x + rr},${y} Z`
  );
};

/** Perimeter of a rounded rectangle path (for draw-on dash arrays). */
export const roundRectLength = (w: number, h: number, r: number): number => {
  const rr = Math.max(0, Math.min(r, w / 2, h / 2));
  return 2 * (w - 2 * rr) + 2 * (h - 2 * rr) + 2 * Math.PI * rr;
};

export type IconName = 'euro' | 'bars' | 'mail' | 'shield' | 'cal' | 'building' | 'check' | 'person' | 'none';

/** Pictogram in a box of side s centred on the origin, stroked/filled with `color`. */
export const Icon: React.FC<{name: IconName | string; s: number; color?: string; sw?: number; fill?: string}> = ({name, s, color, sw, fill}) => {
  const C = usePalette();
  const col = color ?? C.ink;
  const k = s / 24;
  const w = sw ?? Math.max(2, 2.4 * k);
  const common = {fill: 'none', stroke: col, strokeWidth: w / k, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const};
  switch (name) {
    case 'euro':
      return (
        <g transform={`scale(${k})`}>
          <path d="M6.4 -5.8 A7.6 7.6 0 1 0 6.4 5.8" {...common} />
          <path d="M-8.6 -1.9 H2.2 M-8.6 2.1 H1.4" {...common} />
        </g>
      );
    case 'bars':
      return (
        <g transform={`scale(${k})`} fill={col}>
          <rect x={-9} y={1} width={5} height={8} rx={1} />
          <rect x={-2.5} y={-4} width={5} height={13} rx={1} />
          <rect x={4} y={-9} width={5} height={18} rx={1} />
        </g>
      );
    case 'mail':
      return (
        <g transform={`scale(${k})`}>
          <rect x={-10} y={-7} width={20} height={14} rx={2} {...common} />
          <path d="M-9 -5.5 L0 1.5 L9 -5.5" {...common} />
        </g>
      );
    case 'shield':
      return (
        <g transform={`scale(${k})`}>
          <path d="M0 -10 L8.5 -6.8 V0 C8.5 5.5 4.8 8.6 0 10.4 C-4.8 8.6 -8.5 5.5 -8.5 0 V-6.8 Z" {...common} />
          <path d="M-3.6 0.2 L-0.8 3 L4 -2.6" {...common} />
        </g>
      );
    case 'cal':
      return (
        <g transform={`scale(${k})`}>
          <rect x={-9.5} y={-7.5} width={19} height={17} rx={2.5} {...common} />
          <path d="M-9.5 -2 H9.5 M-4.5 -10.5 V-5 M4.5 -10.5 V-5" {...common} />
          <circle cx={-4} cy={3.5} r={1.4} fill={col} />
          <circle cx={0.5} cy={3.5} r={1.4} fill={col} />
          <circle cx={5} cy={3.5} r={1.4} fill={col} />
        </g>
      );
    case 'building':
      return (
        <g transform={`scale(${k})`} fill={col}>
          <path d="M0 -10.5 L10.5 -4.5 H-10.5 Z" />
          <rect x={-8.5} y={-2.6} width={3} height={9.5} />
          <rect x={-1.5} y={-2.6} width={3} height={9.5} />
          <rect x={5.5} y={-2.6} width={3} height={9.5} />
          <rect x={-10.5} y={8} width={21} height={2.6} />
        </g>
      );
    case 'check':
      return <path d={`M${-9 * k} ${0.5 * k} L${-3 * k} ${6.5 * k} L${9.5 * k} ${-6.5 * k}`} {...common} strokeWidth={w} />;
    case 'person':
      // The client's mini-silhouette (same figurine: round head + rounded trapezoid bust), paper inside.
      return (
        <g transform={`scale(${k})`} strokeLinejoin="round">
          <path d="M-4.6 1 H4.6 Q6.6 1 7 3 L8.6 10.4 Q8.9 12 7.3 12 H-7.3 Q-8.9 12 -8.6 10.4 L-7 3 Q-6.6 1 -4.6 1 Z" fill={fill ?? C.paper} stroke={col} strokeWidth={w / k} />
          <circle cx={0} cy={-5.6} r={5} fill={fill ?? C.paper} stroke={col} strokeWidth={w / k} />
        </g>
      );
    default:
      return null;
  }
};

/** The figurine of the cast (client / advisor): round head + rounded trapezoid bust, base at y = 95. */
export const BUST = 'M-27 -26 H27 Q39 -26 41 -14 L57 80 Q59 95 45 95 H-45 Q-59 95 -57 80 L-41 -14 Q-39 -26 -27 -26 Z';
export const FIGURE_H = 191; // head top (-96) to base (95)

/**
 * Mini copy of the client figurine (paper inside, ink outline), `h` px tall, centred on the origin. Used inside the
 * advisor's bubble and on the « ? » sticker: the question is for THIS person (not a generic « profile » icon).
 */
export const ClientGlyph: React.FC<{h: number; sw: number; fill?: string}> = ({h, sw, fill}) => {
  const C = usePalette();
  const k = h / FIGURE_H;
  return (
    <g transform={`scale(${k}) translate(0 0.5)`}>
      <path d={BUST} fill={fill ?? C.paper} stroke={C.ink} strokeWidth={sw / k} strokeLinejoin="round" />
      <circle cx={0} cy={-64} r={32} fill={fill ?? C.paper} stroke={C.ink} strokeWidth={sw / k} />
    </g>
  );
};

/**
 * Diagonal sheen band of a page (« fluide »), in PAGE coordinates (origin = page centre), as polygon points shifted
 * by (dx, dy) = the drawing entity's origin in page coordinates. s: 0 -> 1, the band enters top-left, leaves
 * bottom-right. Drawn UNDER texts (rows, pill, page body): it never bleaches letters.
 */
export const SHEEN_HALF = 55;
export const sheenPoints = (s: number, W: number, H: number, dx: number, dy: number): string => {
  const slant = H * 0.45;
  const cx = -W / 2 - 70 + (W + slant + 200) * s;
  const pts: [number, number][] = [
    [cx - SHEEN_HALF, -H / 2 - 4],
    [cx + SHEEN_HALF, -H / 2 - 4],
    [cx + SHEEN_HALF - slant, H / 2 + 4],
    [cx - SHEEN_HALF - slant, H / 2 + 4],
  ];
  return pts.map(([x, y]) => `${x - dx},${y - dy}`).join(' ');
};

/**
 * Information bullet: cyan disc + ink outline + document pictogram. `none` = the AI's empty bullet: a white
 * disc with a dashed outline; `alarm` turns that outline red. It never fills: emptiness is the message.
 */
export const Bullet: React.FC<{icon: string; r?: number; alarm?: number}> = ({icon, r = 22, alarm = 0}) => {
  const C = usePalette();
  if (icon === 'none') {
    const a = Math.max(0, Math.min(1, alarm));
    return <circle cx={0} cy={0} r={r} fill={C.paper} stroke={a > 0 ? mixHex(C.deep, C.red, a) : C.deep} strokeWidth={4.5} strokeDasharray="6.2 5" />;
  }
  return (
    <>
      <Hard off={3} render={(sh) => <circle cx={0} cy={0} r={r} fill={sh ? C.ink : C.cyan} stroke={C.ink} strokeWidth={3} />} />
      <Icon name={icon} s={r * 1.2} color={C.ink} sw={2.6} />
    </>
  );
};
