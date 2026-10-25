// Shared kit of the "Short" composition (14 s silent vertical shorts, wth-videos/shorts/shorts.json): timing, easing,
// French typography, app tiles, the bottom "dock" panel, the 1/5 progress bar, HTML text blocks with the series' hard
// ink shadow. Drawing primitives (Hard, Txt, Icon, roundRect, palette) come from the Story kit (../story/draw).
import React from 'react';
import {FONT_FAMILY} from '../fonts';
import {DEFAULT_PALETTE, Hard, Icon, roundRect, Txt} from '../story/draw';

export const C = {...DEFAULT_PALETTE, bg: '#F6F0E4', gridLine: '#ECE4D4'};
export const FONT = `'${FONT_FAMILY}'`;

// ---------- frame & timing ----------
export const W = 1080;
export const H = 1920;
export const FPS = 30;
/** Horizontal centre of the safe area (x 60 .. 930): everything is centred here, not on 540. */
export const CX = 495;
export const SAFE = {top: 160, bottom: 1540, left: 60, right: 930};
export const HOOK = 60; // 0-2 s
export const EL = 60; // 5 x 2 s
export const END = HOOK + 5 * EL; // 12 s
export const TOTAL = END + 60; // 14 s
export const elStart = (i: number) => HOOK + i * EL;

export const clamp01 = (x: number) => (x < 0 ? 0 : x > 1 ? 1 : x);
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
/** 0 -> 1 between frames a and b (linear, clamped). */
export const seg = (f: number, a: number, b: number) => clamp01((f - a) / (b - a));
export const eOut = (t: number) => 1 - Math.pow(1 - clamp01(t), 3);
export const eIn = (t: number) => Math.pow(clamp01(t), 3);
export const eInOut = (t: number) => {
  const x = clamp01(t);
  return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
};
/** Overshoot (pop). */
export const back = (t: number, s = 1.7) => {
  const x = clamp01(t) - 1;
  return 1 + (s + 1) * x * x * x + s * x * x;
};
/** Damped bounce around 1 after an impact at frame a (squash & settle). */
export const thump = (f: number, a: number, amp = 0.08, len = 12) => {
  if (f < a || f > a + len) return 1;
  const t = (f - a) / len;
  return 1 - amp * Math.sin(t * Math.PI * 2) * (1 - t);
};

/** Where we are: hook, element i (local frame u), or end card (local frame u). */
export type Phase = {kind: 'hook' | 'el' | 'end'; i: number; u: number};
export const phaseOf = (f: number): Phase => {
  if (f < HOOK) return {kind: 'hook', i: -1, u: f};
  if (f >= END) return {kind: 'end', i: 5, u: f - END};
  const i = Math.floor((f - HOOK) / EL);
  return {kind: 'el', i, u: f - elStart(i)};
};

// ---------- French typography ----------
/** Typographic apostrophe, non-breaking spaces before : ; ? ! % € and inside « », thin non-breaking space in 22 950. */
export const fr = (s: string): string =>
  s
    .replace(/'/g, '’')
    .replace(/ ([:;?!%€»])/g, ' $1')
    .replace(/« /g, '« ')
    .replace(/(\d) (\d{3})(?!\d)/g, '$1 $2');

/** Up to 2 letters for a tile: first letters of the first two words (« Trust Wallet » -> TW), else the first letter. */
export const initials = (name: string): string => {
  const words = name.split(/\s+/).filter(Boolean);
  if (words.length >= 2) return (words[0][0] + words[1][0]).toUpperCase();
  return name.slice(0, 1).toUpperCase();
};

const lum = (hex: string): number => {
  const h = hex.replace('#', '');
  const v = [0, 2, 4].map((k) => parseInt(h.slice(k, k + 2), 16) / 255).map((c) => (c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4)));
  return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2];
};
/** Ink on light tiles, paper on dark ones. */
export const onColor = (hex: string): string => (lum(hex) > 0.36 ? C.ink : C.paper);

// ---------- SVG pieces ----------
export const Svg: React.FC<{children: React.ReactNode; opacity?: number}> = ({children, opacity}) => (
  <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{position: 'absolute', inset: 0, overflow: 'visible', opacity}}>
    {children}
  </svg>
);

/** Check badge: cyan disc, ink outline, ink tick. */
export const CheckBadge: React.FC<{x: number; y: number; r: number; k?: number}> = ({x, y, r, k = 1}) =>
  k <= 0.01 ? null : (
    <g transform={`translate(${x} ${y}) scale(${k})`}>
      <Hard off={3} render={(sh) => <circle r={r} fill={sh ? C.ink : C.cyan} stroke={C.ink} strokeWidth={3} />} />
      <Icon name="check" s={r * 1.3} color={C.ink} sw={Math.max(3, r * 0.22)} />
    </g>
  );

/**
 * App tile: rounded square in the app's colour, ink outline, hard shadow, the initial(s) (or a generic pictogram)
 * inside and the app NAME under it. No logo is reproduced.
 */
export const Tile: React.FC<{
  x: number;
  y: number;
  s: number;
  color: string;
  name?: string;
  label?: string;
  glyph?: string;
  showName?: boolean;
  nameSize?: number;
  badge?: number;
  rot?: number;
  opacity?: number;
  dashed?: boolean;
}> = ({x, y, s, color, name = '', label, glyph, showName = false, nameSize = 44, badge = 0, rot = 0, opacity, dashed}) => {
  const r = s * 0.24;
  const sw = Math.max(3, s * 0.02);
  const fg = onColor(color);
  const text = label ?? initials(name);
  const ts = text.length >= 3 ? s * 0.3 : text.length === 2 ? s * 0.38 : s * 0.5;
  return (
    <g transform={`translate(${x} ${y}) rotate(${rot})`} opacity={opacity}>
      {dashed ? (
        <path d={roundRect(-s / 2, -s / 2, s, s, r)} fill="none" stroke={C.aiTick} strokeWidth={3} strokeDasharray="10 8" />
      ) : (
        <>
          <Hard off={Math.max(3, Math.min(8, s * 0.04))} render={(sh) => <path d={roundRect(-s / 2, -s / 2, s, s, r)} fill={sh ? C.ink : color} stroke={C.ink} strokeWidth={sw} />} />
          {glyph ? (
            <Icon name={glyph} s={s * 0.5} color={fg} sw={Math.max(2.5, s * 0.04)} />
          ) : (
            <Txt x={0} y={0} size={ts} weight={800} color={fg} anchor="middle">
              {text}
            </Txt>
          )}
          {showName && name ? (
            <Txt x={0} y={s / 2 + 14 + nameSize / 2} size={nameSize} weight={800} anchor="middle">
              {fr(name)}
            </Txt>
          ) : null}
          <CheckBadge x={s / 2 - s * 0.06} y={-s / 2 + s * 0.06} r={Math.max(14, s * 0.16)} k={badge} />
        </>
      )}
    </g>
  );
};

/** Bottom dock: the open folder panel (label + 5 slots). Slot centres: dockSlot(k). */
export const DOCK = {x: 80, y: 1285, w: 830, h: 230, r: 40, tile: 104};
export const dockSlot = (k: number): [number, number] => [DOCK.x + (DOCK.w * (k + 0.5)) / 5, DOCK.y + 150];

export const Panel: React.FC<{x: number; y: number; w: number; h: number; r: number; fill?: string; off?: number}> = ({x, y, w, h, r, fill, off = 6}) => (
  <Hard off={off} render={(sh) => <path d={roundRect(x, y, w, h, r)} fill={sh ? C.ink : (fill ?? C.slot)} stroke={C.ink} strokeWidth={4} />} />
);

/** Progress bar at the top of the safe area: « 2/5 » + 5 segments filling with time. */
export const Progress: React.FC<{f: number}> = ({f}) => {
  const show = seg(f, HOOK - 8, HOOK + 2) * (1 - seg(f, END - 2, END + 8));
  if (show <= 0.01) return null;
  const p = Math.max(0, Math.min(5, (f - HOOK) / EL));
  const n = Math.min(5, Math.floor(p) + 1);
  const x0 = 176;
  const x1 = 904;
  const gap = 14;
  const sw = (x1 - x0 - 4 * gap) / 5;
  const y = 205;
  const h = 24;
  return (
    <g opacity={show} transform={`translate(0 ${(1 - show) * -16})`}>
      <Txt x={60} y={y} size={46} weight={800} tabular>
        {`${n}/5`}
      </Txt>
      {[0, 1, 2, 3, 4].map((k) => {
        const x = x0 + k * (sw + gap);
        const fill = clamp01(p - k);
        return (
          <g key={k}>
            <defs>
              <clipPath id={`seg${k}`}>
                <path d={roundRect(x, y - h / 2, sw, h, h / 2)} />
              </clipPath>
            </defs>
            <Hard off={4} render={(sh) => <path d={roundRect(x, y - h / 2, sw, h, h / 2)} fill={sh ? C.ink : C.paper} stroke={C.ink} strokeWidth={3} />} />
            {fill > 0 ? <rect x={x} y={y - h / 2} width={sw * fill} height={h} fill={k < n - 1 ? C.deep : C.cyan} clipPath={`url(#seg${k})`} /> : null}
            <path d={roundRect(x, y - h / 2, sw, h, h / 2)} fill="none" stroke={C.ink} strokeWidth={3} />
          </g>
        );
      })}
    </g>
  );
};

/** Burst of short rays (impact beat). */
export const Burst: React.FC<{x: number; y: number; t: number; r0?: number; r1?: number; n?: number; color?: string}> = ({x, y, t, r0 = 60, r1 = 110, n = 8, color = C.ink}) => {
  if (t <= 0 || t >= 1) return null;
  const a = eOut(t);
  const op = 1 - t;
  return (
    <g transform={`translate(${x} ${y})`} opacity={op}>
      {Array.from({length: n}, (_, k) => {
        const ang = (k / n) * Math.PI * 2 - Math.PI / 2;
        const ra = lerp(r0, r1, a) - 26;
        const rb = lerp(r0, r1, a);
        return <line key={k} x1={Math.cos(ang) * ra} y1={Math.sin(ang) * ra} x2={Math.cos(ang) * rb} y2={Math.sin(ang) * rb} stroke={color} strokeWidth={6} strokeLinecap="round" />;
      })}
    </g>
  );
};

/** Coin: cyan disc + euro sign (or a custom letter). */
export const Coin: React.FC<{x: number; y: number; r: number; letter?: string; fill?: string}> = ({x, y, r, letter, fill}) => (
  <g transform={`translate(${x} ${y})`}>
    <Hard off={4} render={(sh) => <circle r={r} fill={sh ? C.ink : (fill ?? C.cyan)} stroke={C.ink} strokeWidth={4} />} />
    <circle r={r * 0.74} fill="none" stroke={C.ink} strokeWidth={2.5} opacity={0.5} />
    {letter === 'B' ? (
      <g>
        <line x1={-r * 0.12} y1={-r * 0.72} x2={-r * 0.12} y2={r * 0.72} stroke={C.ink} strokeWidth={Math.max(3, r * 0.09)} />
        <line x1={r * 0.14} y1={-r * 0.72} x2={r * 0.14} y2={r * 0.72} stroke={C.ink} strokeWidth={Math.max(3, r * 0.09)} />
        <Txt x={0} y={0} size={r * 1.05} weight={800} anchor="middle">
          B
        </Txt>
      </g>
    ) : letter ? (
      <Txt x={0} y={0} size={r * 1.0} weight={800} anchor="middle">
        {letter}
      </Txt>
    ) : (
      <Icon name="euro" s={r * 1.15} color={C.ink} sw={Math.max(3, r * 0.1)} />
    )}
  </g>
);

/** Folded-corner document (paper) with grey text lines; centred on (x, y). */
export const Sheet: React.FC<{x: number; y: number; w: number; h: number; rot?: number; lines?: number; fill?: string; children?: React.ReactNode}> = ({x, y, w, h, rot = 0, lines = 4, fill, children}) => {
  const f = Math.min(w, h) * 0.18;
  const x0 = -w / 2;
  const y0 = -h / 2;
  const body = `M${x0 + 12},${y0} H${x0 + w - f} L${x0 + w},${y0 + f} V${y0 + h - 12} Q${x0 + w},${y0 + h} ${x0 + w - 12},${y0 + h} H${x0 + 12} Q${x0},${y0 + h} ${x0},${y0 + h - 12} V${y0 + 12} Q${x0},${y0} ${x0 + 12},${y0} Z`;
  return (
    <g transform={`translate(${x} ${y}) rotate(${rot})`}>
      <Hard off={5} render={(sh) => <path d={body} fill={sh ? C.ink : (fill ?? C.paper)} stroke={C.ink} strokeWidth={3.5} strokeLinejoin="round" />} />
      <path d={`M${x0 + w - f},${y0} V${y0 + f} H${x0 + w} Z`} fill={C.grey} stroke={C.ink} strokeWidth={3} strokeLinejoin="round" />
      {Array.from({length: lines}, (_, k) => (
        <rect key={k} x={x0 + w * 0.14} y={y0 + h * 0.3 + k * h * 0.15} width={w * (k % 2 ? 0.55 : 0.72)} height={Math.max(5, h * 0.045)} rx={3} fill={C.grey} />
      ))}
      {children}
    </g>
  );
};

// ---------- HTML text blocks ----------
/** HTML text box (wraps, balanced lines), optionally a card with the series' hard ink shadow. */
export const TextBox: React.FC<{
  x: number;
  y: number;
  w: number;
  size: number;
  weight?: number;
  color?: string;
  align?: 'left' | 'center' | 'right';
  card?: string | null;
  pad?: [number, number];
  opacity?: number;
  dy?: number;
  scale?: number;
  lh?: number;
  radius?: number;
  shadow?: number;
  children: React.ReactNode;
}> = ({x, y, w, size, weight = 700, color, align = 'center', card = null, pad = [22, 32], opacity = 1, dy = 0, scale = 1, lh = 1.16, radius = 28, shadow = 6, children}) =>
  opacity <= 0.01 ? null : (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y,
        width: w,
        boxSizing: 'border-box',
        padding: card ? `${pad[0]}px ${pad[1]}px` : 0,
        background: card ?? undefined,
        border: card ? `4px solid ${C.ink}` : undefined,
        borderRadius: card ? radius : undefined,
        boxShadow: card && shadow ? `${shadow}px ${shadow}px 0 0 ${C.ink}` : undefined,
        fontFamily: FONT,
        fontWeight: weight,
        fontSize: size,
        lineHeight: lh,
        color: color ?? C.ink,
        textAlign: align,
        textWrap: 'balance',
        fontKerning: 'normal',
        opacity: opacity < 0.999 ? opacity : undefined,
        transform: dy || scale !== 1 ? `translateY(${dy}px) scale(${scale})` : undefined,
        transformOrigin: 'center top',
      }}
    >
      {children}
    </div>
  );

/** Digits of a title in deep cyan (the « 5 » of « Mes 5 applis »). */
export const Digits: React.FC<{text: string; color?: string}> = ({text, color = C.deep}) => (
  <>
    {text.split(/(\d+)/).map((part, k) =>
      /^\d+$/.test(part) ? (
        <span key={k} style={{color}}>
          {part}
        </span>
      ) : (
        <React.Fragment key={k}>{part}</React.Fragment>
      ),
    )}
  </>
);
