// Flat vector drawing kit of the Story composition: ink outlines, hard shadows (+6/+6, no blur), Inter text,
// pictograms. Everything is drawn in an entity's local coordinates, centred on its origin.
//
// Colours come from props.style (pipeline/story.py STYLE) through PaletteContext: the composition is data-driven,
// changing STYLE recolours entities, background and captions alike. DEFAULT_PALETTE only serves the studio preview.
import React, {createContext, useContext} from 'react';
import {FONT_FAMILY} from '../fonts';
import GEOM from './geometry.json';
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
  /** Chiffres à chasse fixe (compteur : la largeur ne tremble pas pendant l'interpolation). */
  tabular?: boolean;
};

/** Text vertically centred on y (cap height of Inter = 0.727 em). */
export const Txt: React.FC<TxtProps> = ({x, y, size, weight = 600, color, anchor = 'start', children, opacity, spacing, tabular}) => {
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
        fontVariantNumeric: tabular ? 'tabular-nums' : undefined,
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

export type IconName = 'euro' | 'bars' | 'mail' | 'shield' | 'cal' | 'building' | 'check' | 'person' | 'rewind' | 'clock' |
  'house' | 'bank' | 'coin' | 'percent' | 'lock' | 'cart' | 'moon' | 'pause' | 'warning' | 'phone' | 'plus' | 'minus' |
  'arrow' | 'hourglass' | 'clock9' | 'chat' | 'target' | 'sign' | 'none';

/** Pictogrammes disponibles (catalogue du kit, planches de contrôle). */
export const ICON_NAMES: IconName[] = ['euro', 'bars', 'mail', 'shield', 'cal', 'building', 'check', 'person', 'rewind',
  'clock', 'house', 'bank', 'coin', 'percent', 'lock', 'cart', 'moon', 'pause', 'warning', 'phone', 'plus', 'minus', 'arrow',
  'hourglass', 'clock9', 'chat', 'target', 'sign'];

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
    // ----- pictogrammes du kit (même boîte 24 x 24, traits arrondis) -----
    case 'rewind':
      // « ◀◀ » : retour en arrière
      return (
        <g transform={`scale(${k})`} fill={col} stroke={col} strokeWidth={w / k} strokeLinejoin="round">
          <path d="M-0.5 -7 L-9 0 L-0.5 7 Z" />
          <path d="M8.5 -7 L0 0 L8.5 7 Z" />
        </g>
      );
    case 'clock':
      return (
        <g transform={`scale(${k})`}>
          <circle cx={0} cy={0} r={10} {...common} />
          <path d="M0 -6 V0 L4.2 2.6" {...common} />
        </g>
      );
    case 'house':
      return (
        <g transform={`scale(${k})`}>
          <path d="M-10.5 -0.5 L0 -9.5 L10.5 -0.5" {...common} />
          <path d="M-7.5 -2.8 V9.5 H7.5 V-2.8" {...common} />
          <path d="M-2.6 9.5 V3.6 H2.6 V9.5" {...common} />
        </g>
      );
    case 'bank':
      // temple au trait (le « building » plein reste le sceau du cabinet)
      return (
        <g transform={`scale(${k})`}>
          <path d="M-10.5 -4.2 L0 -10 L10.5 -4.2 Z" {...common} />
          <path d="M-6.8 -1 V6 M-2.3 -1 V6 M2.3 -1 V6 M6.8 -1 V6 M-10.5 9.4 H10.5" {...common} />
        </g>
      );
    case 'coin':
      return (
        <g transform={`scale(${k})`}>
          <circle cx={0} cy={0} r={10} {...common} />
          <g transform="translate(0.6 0) scale(0.56)">
            <path d="M6.4 -5.8 A7.6 7.6 0 1 0 6.4 5.8" {...common} strokeWidth={w / k / 0.7} />
            <path d="M-8.6 -1.9 H2.2 M-8.6 2.1 H1.4" {...common} strokeWidth={w / k / 0.7} />
          </g>
        </g>
      );
    case 'percent':
      return (
        <g transform={`scale(${k})`}>
          <path d="M7.5 -8.5 L-7.5 8.5" {...common} />
          <circle cx={-5.4} cy={-5.6} r={2.9} {...common} />
          <circle cx={5.4} cy={5.6} r={2.9} {...common} />
        </g>
      );
    case 'lock':
      return (
        <g transform={`scale(${k})`}>
          <path d="M-5.2 -1.5 V-5 A5.2 5.2 0 0 1 5.2 -5 V-1.5" {...common} />
          <rect x={-8.5} y={-1.5} width={17} height={12} rx={2.5} {...common} />
          <circle cx={0} cy={4.4} r={1.7} fill={col} />
        </g>
      );
    case 'cart':
      return (
        <g transform={`scale(${k})`}>
          <path d="M-11 -8.5 H-7.4 L-4.4 4.6 H7.2 L9.8 -4.4 H-6.2" {...common} />
          <circle cx={-2.8} cy={8.8} r={1.9} fill={col} />
          <circle cx={5.8} cy={8.8} r={1.9} fill={col} />
        </g>
      );
    case 'moon':
      return (
        <g transform={`scale(${k})`}>
          <path d="M3.6 -9.6 A9.8 9.8 0 1 0 9.8 3.2 A7.6 7.6 0 0 1 3.6 -9.6 Z" {...common} />
        </g>
      );
    case 'pause':
      return (
        <g transform={`scale(${k})`} fill={col}>
          <rect x={-7.5} y={-9} width={5.4} height={18} rx={1.6} />
          <rect x={2.1} y={-9} width={5.4} height={18} rx={1.6} />
        </g>
      );
    case 'warning':
      return (
        <g transform={`scale(${k})`}>
          <path d="M0 -10 L10.6 8.6 H-10.6 Z" {...common} />
          <path d="M0 -3.4 V2.2" {...common} />
          <circle cx={0} cy={5.4} r={1.5} fill={col} />
        </g>
      );
    case 'phone':
      return (
        <g transform={`scale(${k})`}>
          <rect x={-6.5} y={-10.5} width={13} height={21} rx={2.6} {...common} />
          <path d="M-2.2 -7.4 H2.2" {...common} />
          <circle cx={0} cy={7} r={1.3} fill={col} />
        </g>
      );
    case 'plus':
      return <path d={`M${-8 * k} 0 H${8 * k} M0 ${-8 * k} V${8 * k}`} {...common} strokeWidth={w} />;
    case 'minus':
      return <path d={`M${-8 * k} 0 H${8 * k}`} {...common} strokeWidth={w} />;
    case 'arrow':
      return (
        <g transform={`scale(${k})`}>
          <path d="M-9 0 H8.5 M2.5 -6 L8.5 0 L2.5 6" {...common} />
        </g>
      );
    // ----- ajoutés pour V01 v3 (même boîte 24 x 24, traits arrondis) -----
    case 'hourglass':
      // sablier (« retraite ») : deux triangles pointe contre pointe entre deux barres, un tas de sable en bas
      return (
        <g transform={`scale(${k})`}>
          <path d="M-6.2 -8.6 H6.2 L0.9 -0.4 Q0 0.6 -0.9 -0.4 Z M-6.2 8.6 H6.2 L0.9 0.4 Q0 -0.6 -0.9 0.4 Z" {...common} />
          <path d="M-4.4 8.6 Q0 3.4 4.4 8.6 Z" fill={col} stroke={col} strokeWidth={w / k / 2} strokeLinejoin="round" />
          <path d="M-9 -10.2 H9 M-9 10.2 H9" {...common} />
        </g>
      );
    case 'clock9':
      // horloge sur 9 h : petite aiguille vers la gauche, grande aiguille vers le haut
      return (
        <g transform={`scale(${k})`}>
          <circle cx={0} cy={0} r={10} {...common} />
          <path d="M0 -6.6 V0 H-4.8" {...common} />
        </g>
      );
    case 'chat':
      // bulle de dialogue arrondie, petite queue en bas à gauche
      return (
        <g transform={`scale(${k})`}>
          <path d="M-5.8 -8.6 H5.8 A4.4 4.4 0 0 1 10.2 -4.2 V1.4 A4.4 4.4 0 0 1 5.8 5.8 H-1.4 L-6.6 10 V5.8 A4.4 4.4 0 0 1 -10.2 1.4 V-4.2 A4.4 4.4 0 0 1 -5.8 -8.6 Z" {...common} />
        </g>
      );
    case 'target':
      // cible : deux cercles concentriques et un point plein
      return (
        <g transform={`scale(${k})`}>
          <circle cx={0} cy={0} r={10} {...common} />
          <circle cx={0} cy={0} r={5.4} {...common} />
          <circle cx={0} cy={0} r={2} fill={col} />
        </g>
      );
    case 'sign':
      // signature : trait ondulé, souligné, qui finit sous une pointe de stylo
      return (
        <g transform={`scale(${k})`}>
          <path d="M-10.6 3.2 C-9.8 -4.6 -6.4 -5.2 -6.2 -0.4 C-6 3.6 -3.4 3.8 -2.6 0.4 C-2 -2 -0.4 -1.6 0.6 2.4" {...common} />
          <path d="M-10.6 8.6 H9.8" {...common} />
          <path d="M4.4 -2.4 L9.6 -9.4" {...common} strokeWidth={(w / k) * 1.9} />
          <path d="M0.8 2.6 L2.1 -3.2 L6 -0.4 Z" fill={col} stroke={col} strokeWidth={w / k / 2} strokeLinejoin="round" />
        </g>
      );
    default:
      return null;
  }
};

/** The figurine of the cast (client / advisor): round head + rounded trapezoid bust, base at y = 95 (geometry.json). */
export const BUST = GEOM.FIGURE.bust;
export const FIGURE_H = GEOM.FIGURE.h; // head top (-96) to base (95)
export const HEAD = GEOM.FIGURE.head;

/**
 * Mini copy of the client figurine (paper inside, ink outline), `h` px tall, centred on the origin. Used inside the
 * advisor's bubble and on the « ? » sticker: the question is for THIS person (not a generic « profile » icon).
 */
export const ClientGlyph: React.FC<{h: number; sw: number; fill?: string; stroke?: string}> = ({h, sw, fill, stroke}) => {
  const C = usePalette();
  const k = h / FIGURE_H;
  return (
    <g transform={`scale(${k}) translate(0 0.5)`}>
      <path d={BUST} fill={fill ?? C.paper} stroke={stroke ?? C.ink} strokeWidth={sw / k} strokeLinejoin="round" />
      <circle cx={0} cy={HEAD.cy} r={HEAD.r} fill={fill ?? C.paper} stroke={stroke ?? C.ink} strokeWidth={sw / k} />
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
export const Bullet: React.FC<{icon: string; r?: number; alarm?: number}> = ({icon, r = GEOM.BULLET.r, alarm = 0}) => {
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
