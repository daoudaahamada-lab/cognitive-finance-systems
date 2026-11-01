// Code-drawn accents in the flat premium style of direction A: cream outlines, red fills, Inter ExtraBold.
// Each overlay belongs to a shot: anchored ones (content-box fractions) follow the object's pose, and every
// overlay leaves with its shot unless it has its own `until` frame.
import React from 'react';
import {useCurrentFrame} from 'remotion';
import {easeInOut, easeOut, leave, lerp, pop, progress, swap} from './anim';
import {Icon} from './icons';
import {heroPose, toScreen, type Pose} from './pose';
import type {
  Asset,
  BadgeOverlay,
  BarOverlay,
  BracketsOverlay,
  ChipsOverlay,
  DotOverlay,
  DotsOverlay,
  LeaderOverlay,
  Overlay,
  PillOverlay,
  QMarkOverlay,
  RingOverlay,
  ScanOverlay,
  SectorOverlay,
  Shot,
  Style,
  TicksOverlay,
  TypingOverlay,
  Vec2,
} from './types';

const SCRIM = 'rgba(10, 10, 11, 0.62)';

type Ctx = {
  frame: number;
  style: Style;
  pose: Pose;
  asset: Asset;
  /** Opacity / scale factors of the overlay's own exit (or its shot's exit). */
  out: number;
  outScale: number;
  /** Geometric size factor for anchored overlays (camera zoom x entrance/exit). */
  geo: number;
  at: Vec2;
  width: number;
  height: number;
};

const center = (x: number, y: number, w: number, h: number): React.CSSProperties => ({
  position: 'absolute',
  left: x - w / 2,
  top: y - h / 2,
  width: w,
  height: h,
});

const FullSvg: React.FC<{c: Ctx; children: React.ReactNode; opacity?: number}> = ({c, children, opacity = 1}) => (
  <svg width={c.width} height={c.height} style={{position: 'absolute', inset: 0, opacity: c.out * opacity}}>
    {children}
  </svg>
);

// ---------- small accents ----------

const Dot: React.FC<{o: DotOverlay; c: Ctx}> = ({o, c}) => {
  const d = (o.d ?? 30) * c.geo * pop(c.frame, o.from);
  return (
    <div
      style={{
        ...center(c.at[0], c.at[1], d, d),
        borderRadius: '50%',
        background: c.style.fill,
        opacity: c.out,
      }}
    />
  );
};

const Dots: React.FC<{o: DotsOverlay; c: Ctx}> = ({o, c}) => (
  <>
    {o.anchors.map((uv, i) => {
      const [x, y] = toScreen(c.pose, c.asset, uv);
      const at = o.from + i * (o.stagger ?? 3);
      const d = (o.d ?? 22) * c.geo * pop(c.frame, at);
      if (o.icon === 'tick') {
        // Restyle (no move): the filled tick turns into an outline tick, rows 1 frame apart.
        const f = o.flip_at !== undefined ? progress(c.frame, o.flip_at + i, 6, easeOut) : 0;
        return (
          <div
            key={i}
            style={{
              ...center(x, y, d, d),
              borderRadius: '50%',
              boxSizing: 'border-box',
              background: f > 0 ? `color-mix(in srgb, ${c.style.fill} ${(1 - f) * 100}%, ${SCRIM})` : c.style.fill,
              border: f > 0 ? `${2.5 * f}px solid ${c.style.cream}` : undefined,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              opacity: c.out,
            }}
          >
            <Icon name="tick" size={d * 0.62} color={c.style.cream} stroke={3.6} drawn={progress(c.frame, at + 2, 7)} />
          </div>
        );
      }
      return (
        <div
          key={i}
          style={{
            ...center(x, y, d, d),
            borderRadius: '50%',
            background: c.style.fill,
            opacity: c.out,
          }}
        />
      );
    })}
  </>
);

const Ring: React.FC<{o: RingOverlay; c: Ctx}> = ({o, c}) => {
  const color = o.color === 'cream' ? c.style.cream : c.style.accent;
  const stroke = o.stroke ?? 6;
  if (o.draw) {
    const r = o.r * c.geo;
    const len = 2 * Math.PI * r;
    const p = progress(c.frame, o.from, o.draw, easeOut);
    return (
      <FullSvg c={c} opacity={o.opacity ?? 1}>
        <circle
          cx={c.at[0]}
          cy={c.at[1]}
          r={r}
          fill="none"
          stroke={color}
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={`${len} ${len}`}
          strokeDashoffset={len * (1 - p)}
          transform={`rotate(-90 ${c.at[0]} ${c.at[1]})`}
        />
      </FullSvg>
    );
  }
  const p = pop(c.frame, o.from);
  const r = o.r * c.geo * lerp(0.6, 1, p);
  return (
    <FullSvg c={c} opacity={(o.opacity ?? 1) * p}>
      <circle cx={c.at[0]} cy={c.at[1]} r={r} fill="none" stroke={color} strokeWidth={stroke} />
    </FullSvg>
  );
};

const Bar: React.FC<{o: BarOverlay; c: Ctx}> = ({o, c}) => {
  const stroke = o.stroke ?? 14;
  const r = o.r * c.geo - stroke / 2;
  const a = ((o.angle ?? 45) * Math.PI) / 180;
  const [dx, dy] = [Math.cos(a) * r, Math.sin(a) * r];
  const p = progress(c.frame, o.from, o.draw ?? 10, easeOut);
  const [x0, y0] = [c.at[0] - dx, c.at[1] - dy];
  return (
    <FullSvg c={c}>
      <line
        x1={x0}
        y1={y0}
        x2={lerp(x0, c.at[0] + dx, p)}
        y2={lerp(y0, c.at[1] + dy, p)}
        stroke={c.style.accent}
        strokeWidth={stroke}
      />
    </FullSvg>
  );
};

/** Thin accent leader from a point of the object to a fixed screen point (where labels will land), drawn on. */
const Leader: React.FC<{o: LeaderOverlay; c: Ctx}> = ({o, c}) => {
  const p = progress(c.frame, o.from, o.draw ?? 10, easeOut);
  const [x0, y0] = c.at;
  const x1 = lerp(x0, o.to[0], p);
  const y1 = lerp(y0, o.to[1], p);
  const stroke = o.stroke ?? 3;
  return (
    <FullSvg c={c}>
      <circle cx={x0} cy={y0} r={stroke * 2.4 * pop(c.frame, o.from, 6)} fill={c.style.accent} />
      <line x1={x0} y1={y0} x2={x1} y2={y1} stroke={c.style.accent} strokeWidth={stroke} strokeLinecap="round" />
      <circle cx={x1} cy={y1} r={stroke * 2.4 * progress(c.frame, o.from + (o.draw ?? 10) - 3, 6, easeOut)} fill={c.style.accent} />
    </FullSvg>
  );
};

const Sector: React.FC<{o: SectorOverlay; c: Ctx}> = ({o, c}) => {
  const [bx0, by0, bx1, by1] = c.asset.box;
  const rx = o.rx * (bx1 - bx0) * c.pose.k;
  const ry = o.ry * (by1 - by0) * c.pose.k;
  const a = lerp(o.a0, o.a1, progress(c.frame, o.from, o.draw ?? 14, easeOut));
  // Nothing (not even the radius stroke) until the sweep has really started.
  if (Math.abs(a - o.a0) < 0.5) return null;
  const pt = (deg: number) => {
    const t = (deg * Math.PI) / 180;
    return `${c.at[0] + rx * Math.cos(t)} ${c.at[1] + ry * Math.sin(t)}`;
  };
  const large = Math.abs(a - o.a0) > 180 ? 1 : 0;
  // Opaque brand-red wedge (same red as the pills next to it), with a cream leading edge that sweeps
  // clockwise into the minute hand and fades as the sweep lands, so the wedge closes flush on the hand.
  const edge = 1 - progress(c.frame, o.from + (o.draw ?? 14) - 4, 4, easeOut);
  return (
    <FullSvg c={c}>
      <path
        d={`M ${c.at[0]} ${c.at[1]} L ${pt(o.a0)} A ${rx} ${ry} 0 ${large} 1 ${pt(a)} Z`}
        fill={c.style.fill}
        stroke={c.style.fill}
        strokeWidth={2}
        strokeLinejoin="round"
      />
      {edge > 0.001 ? (
        <path d={`M ${c.at[0]} ${c.at[1]} L ${pt(a)}`} stroke={c.style.cream} strokeWidth={3} strokeLinecap="round" opacity={edge} />
      ) : null}
    </FullSvg>
  );
};

const Brackets: React.FC<{o: BracketsOverlay; c: Ctx}> = ({o, c}) => {
  const [u0, v0, u1, v1] = o.rect;
  const pts = [toScreen(c.pose, c.asset, [u0, v0]), toScreen(c.pose, c.asset, [u1, v1])];
  const p = pop(c.frame, o.from);
  const cx = (pts[0][0] + pts[1][0]) / 2;
  const cy = (pts[0][1] + pts[1][1]) / 2;
  const s = lerp(1.14, 1, p);
  const hw = ((pts[1][0] - pts[0][0]) / 2) * s;
  const hh = ((pts[1][1] - pts[0][1]) / 2) * s;
  const L = Math.min(Math.max(72, 0.18 * Math.min(hw, hh)), 0.45 * Math.min(hw, hh));
  const corners: [number, number, number, number][] = [
    [-1, -1, 1, 1],
    [1, -1, -1, 1],
    [1, 1, -1, -1],
    [-1, 1, 1, -1],
  ];
  return (
    <FullSvg c={c} opacity={p}>
      {corners.map(([sx, sy, ix, iy], i) => {
        const x = cx + sx * hw;
        const y = cy + sy * hh;
        return (
          <path
            key={i}
            d={`M ${x + ix * L} ${y} L ${x} ${y} L ${x} ${y + iy * L}`}
            fill="none"
            stroke={c.style.accent}
            strokeWidth={10}
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        );
      })}
    </FullSvg>
  );
};

const Scan: React.FC<{o: ScanOverlay; c: Ctx}> = ({o, c}) => {
  const [u0, v0, u1, v1] = o.rect;
  const [x0, y0] = toScreen(c.pose, c.asset, [u0, v0]);
  const [x1, y1] = toScreen(c.pose, c.asset, [u1, v1]);
  // Linear narrative sweep (the AI reads at a constant pace), from `from` to `end`.
  const t = Math.min(1, Math.max(0, (c.frame - o.from) / Math.max(1, o.end - o.from)));
  const x = lerp(x0, x1, t);
  const lineOpacity = leave(c.frame, o.end, 6) * pop(c.frame, o.from, 4);
  return (
    <FullSvg c={c}>
      <defs>
        <linearGradient id={`scan-${o.id}`} x1="0" x2="1" y1="0" y2="0">
          <stop offset="0" stopColor={c.style.accent} stopOpacity={0.02} />
          <stop offset="1" stopColor={c.style.accent} stopOpacity={0.16} />
        </linearGradient>
        <filter id={`glow-${o.id}`} x="-200%" y="-10%" width="500%" height="120%">
          <feGaussianBlur stdDeviation="7" />
        </filter>
      </defs>
      <rect x={x0} y={y0} width={Math.max(0, x - x0)} height={y1 - y0} fill={`url(#scan-${o.id})`} />
      <g opacity={lineOpacity}>
        <rect x={x - 8} y={y0 - 14} width={16} height={y1 - y0 + 28} fill={c.style.accent} filter={`url(#glow-${o.id})`} />
        <rect x={x - 2.5} y={y0 - 14} width={5} height={y1 - y0 + 28} rx={2.5} fill={c.style.accent} />
      </g>
    </FullSvg>
  );
};

// ---------- labels and badges ----------

const pillBox = (size: number) => ({h: Math.round(size * 1.9), pad: Math.round(size * 0.78)});

const PillFace: React.FC<{
  text: string;
  size: number;
  upper: boolean;
  filled: number;
  glyph?: 'doc' | 'cal' | 'cross';
  style: Style;
}> = ({text, size, upper, filled, glyph, style}) => {
  const {h, pad} = pillBox(size);
  const border = filled >= 1 ? style.fill : style.cream;
  return (
    <div
      style={{
        height: h,
        padding: `0 ${pad}px`,
        boxSizing: 'border-box',
        borderRadius: h / 2,
        border: `3px solid ${border}`,
        background: filled > 0 ? `color-mix(in srgb, ${style.fill} ${filled * 100}%, ${SCRIM})` : SCRIM,
        display: 'flex',
        alignItems: 'center',
        gap: Math.round(size * 0.4),
        whiteSpace: 'nowrap',
        color: style.cream,
        fontFamily: `'${style.font_family}'`,
        fontWeight: 800,
        fontSize: size,
        lineHeight: 1,
        letterSpacing: upper ? '0.06em' : '0',
      }}
    >
      {glyph ? (
        <Icon
          name={glyph}
          size={Math.round(size * 1.05)}
          color={glyph === 'cross' ? style.accent : style.cream}
          stroke={glyph === 'cross' ? 3.4 : 2.4}
        />
      ) : null}
      <span style={{marginRight: upper ? '-0.06em' : 0, transform: 'translateY(0.02em)'}}>
        {upper ? text.toLocaleUpperCase('fr-FR') : text}
      </span>
    </div>
  );
};

export const PILL_SIZE = 36;

const Pill: React.FC<{o: PillOverlay; c: Ctx}> = ({o, c}) => {
  const size = o.size ?? PILL_SIZE;
  const upper = o.case !== 'keep';
  const s = (o.pop === false ? 1 : pop(c.frame, o.from)) * c.outScale;
  let filled = o.style === 'fill' ? 1 : 0;
  if (o.fill_at !== undefined) filled = Math.max(filled, progress(c.frame, o.fill_at, 9, easeOut));
  const sw = swap(c.frame, o.flip_at);
  const {h} = pillBox(size);
  const tickAt = o.tick_at ?? (o.fill_at !== undefined ? o.fill_at + 3 : undefined);
  const tick = tickAt !== undefined ? pop(c.frame, tickAt) : 0;
  // Collapse: glide to go_to (ease-in-out), shrink, and fade out over the last frames.
  let at = c.at;
  let go = 1;
  let goOpacity = 1;
  if (o.go_at !== undefined && o.go_to) {
    const p = progress(c.frame, o.go_at, 14, easeInOut);
    at = [lerp(c.at[0], o.go_to[0], p), lerp(c.at[1], o.go_to[1], p)];
    go = lerp(1, 0.5, p);
    goOpacity = 1 - progress(c.frame, o.go_at + 8, 6, easeOut);
    if (goOpacity <= 0.001) return null;
  }
  const face = (text: string, f: number, opacity: number, scale: number, key: string) => (
    <div
      key={key}
      style={{
        position: 'absolute',
        left: at[0],
        top: at[1],
        opacity: c.out * goOpacity * opacity,
        transform: `translate(-50%, -50%) scale(${s * go * scale})`,
      }}
    >
      <PillFace text={text} size={size} upper={upper} filled={f} glyph={o.glyph} style={c.style} />
      {tick > 0 && key === 'a' ? (
        <div
          style={{
            position: 'absolute',
            right: -h * 0.32,
            top: -h * 0.32,
            width: h * 0.72,
            height: h * 0.72,
            borderRadius: '50%',
            background: c.style.cream,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            transform: `scale(${tick})`,
          }}
        >
          <Icon name="tick" size={h * 0.5} color={c.style.fill} stroke={3.6} drawn={progress(c.frame, tickAt! + 2, 8)} />
        </div>
      ) : null}
    </div>
  );
  if (!sw.on) return face(o.text, filled, 1, 1, 'a');
  const newFilled = o.flip_style ? (o.flip_style === 'fill' ? 1 : 0) : filled;
  return (
    <>
      {sw.old > 0.001 ? face(o.text, filled, sw.old, sw.oldScale, 'a') : null}
      {face(o.flip_text ?? o.text, newFilled, sw.neu, sw.neuScale, 'b')}
    </>
  );
};

/**
 * Row of word chips (« RELIS · CORRIGE · DÉCIDE »): each pops in on its word as a cream outline and stays, a running
 * checklist. No red: the caption alone carries the red « now » accent (no second red copy of the spoken word).
 */
const Chips: React.FC<{o: ChipsOverlay; c: Ctx}> = ({o, c}) => {
  const size = o.size ?? PILL_SIZE;
  const gap = o.gap ?? 22;
  return (
    <div
      style={{
        position: 'absolute',
        left: c.at[0],
        top: c.at[1],
        transform: 'translate(-50%, -50%)',
        display: 'flex',
        gap,
        opacity: c.out,
      }}
    >
      {o.texts.map((t, i) => {
        const at = o.fill_at[i];
        const s = pop(c.frame, at) * c.outScale;
        return (
          <div key={i} style={{transform: `scale(${s})`}}>
            <PillFace text={t} size={size} upper filled={0} style={c.style} />
          </div>
        );
      })}
    </div>
  );
};

const Badge: React.FC<{o: BadgeOverlay; c: Ctx}> = ({o, c}) => {
  const d = o.d ?? 96;
  const s = pop(c.frame, o.from) * c.outScale;
  const sw = swap(c.frame, o.flip_at);
  const face = (icon: BadgeOverlay['icon'], fill: boolean, drawn: number, opacity: number, scale: number, key: string) => (
    <div
      key={key}
      style={{
        ...center(c.at[0], c.at[1], d, d),
        borderRadius: '50%',
        boxSizing: 'border-box',
        background: fill ? c.style.fill : SCRIM,
        border: `4px solid ${fill ? c.style.fill : c.style.cream}`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        opacity: c.out * opacity,
        transform: `scale(${s * scale})`,
      }}
    >
      <Icon name={icon} size={d * 0.6} color={c.style.cream} stroke={3.2} drawn={drawn} />
    </div>
  );
  const fill = o.style !== 'outline';
  const first = face(o.icon, fill, progress(c.frame, o.from + 3, 8), sw.on ? sw.old : 1, sw.on ? sw.oldScale : 1, 'a');
  if (!sw.on) return first;
  const nfill = o.flip_style ? o.flip_style === 'fill' : fill;
  return (
    <>
      {sw.old > 0.001 ? first : null}
      {face(o.flip_icon ?? o.icon, nfill, progress(c.frame, o.flip_at! + 2, 7), sw.neu, sw.neuScale, 'b')}
    </>
  );
};

const QMark: React.FC<{o: QMarkOverlay; c: Ctx}> = ({o, c}) => {
  const size = (o.size ?? 180) * c.geo;
  const s = pop(c.frame, o.from);
  const rot = o.tilt_at !== undefined ? (o.tilt ?? 12) * progress(c.frame, o.tilt_at, 14, easeOut) : 0;
  return (
    <div
      style={{
        position: 'absolute',
        left: c.at[0],
        top: c.at[1],
        opacity: c.out,
        transform: `translate(-50%, -50%) rotate(${rot}deg) scale(${s})`,
        color: c.style.fill,
        fontFamily: `'${c.style.font_family}'`,
        fontWeight: 800,
        fontSize: size,
        lineHeight: 1,
        // Optical centring of the glyph box.
        paddingTop: size * 0.04,
      }}
    >
      ?
    </div>
  );
};

const Ticks: React.FC<{o: TicksOverlay; c: Ctx}> = ({o, c}) => {
  const d = o.d ?? 76;
  const gap = o.gap ?? 112;
  const x0 = c.at[0] - ((o.n - 1) * gap) / 2;
  return (
    <>
      {Array.from({length: o.n}, (_, i) => {
        const at = o.fill_at[i];
        const f = at !== undefined ? progress(c.frame, at, 9, easeOut) : 0;
        const s = pop(c.frame, o.from + i * 2) * c.outScale;
        return (
          <div
            key={i}
            style={{
              ...center(x0 + i * gap, c.at[1], d, d),
              borderRadius: '50%',
              boxSizing: 'border-box',
              border: `3px solid ${f > 0.5 ? c.style.fill : c.style.cream}`,
              background: f > 0 ? `color-mix(in srgb, ${c.style.fill} ${f * 100}%, ${SCRIM})` : SCRIM,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              opacity: c.out * (0.55 + 0.45 * Math.max(f, at !== undefined && c.frame >= at ? 1 : 0)),
              transform: `scale(${s})`,
            }}
          >
            {at !== undefined && c.frame >= at ? (
              <Icon name="tick" size={d * 0.6} color={c.style.cream} stroke={3.4} drawn={progress(c.frame, at + 2, 8)} />
            ) : null}
          </div>
        );
      })}
    </>
  );
};

const Typing: React.FC<{o: TypingOverlay; c: Ctx}> = ({o, c}) => {
  const w = 138;
  const h = 64;
  const s = pop(c.frame, o.from) * c.outScale;
  return (
    <div
      style={{
        ...center(c.at[0], c.at[1], w, h),
        borderRadius: h / 2,
        boxSizing: 'border-box',
        border: `3px solid ${c.style.cream}`,
        background: SCRIM,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 14,
        opacity: c.out,
        transform: `scale(${s})`,
      }}
    >
      {[0, 1, 2].map((i) => {
        const p = pop(c.frame, o.from + 3 + i * 3, 7);
        return (
          <div
            key={i}
            style={{
              width: 14,
              height: 14,
              borderRadius: '50%',
              background: i === 2 ? c.style.fill : c.style.cream,
              transform: `scale(${p})`,
            }}
          />
        );
      })}
    </div>
  );
};

const RENDERERS: Record<Overlay['type'], React.FC<{o: never; c: Ctx}>> = {
  dot: Dot as React.FC<{o: never; c: Ctx}>,
  dots: Dots as React.FC<{o: never; c: Ctx}>,
  ring: Ring as React.FC<{o: never; c: Ctx}>,
  bar: Bar as React.FC<{o: never; c: Ctx}>,
  sector: Sector as React.FC<{o: never; c: Ctx}>,
  brackets: Brackets as React.FC<{o: never; c: Ctx}>,
  scan: Scan as React.FC<{o: never; c: Ctx}>,
  pill: Pill as React.FC<{o: never; c: Ctx}>,
  badge: Badge as React.FC<{o: never; c: Ctx}>,
  qmark: QMark as React.FC<{o: never; c: Ctx}>,
  ticks: Ticks as React.FC<{o: never; c: Ctx}>,
  typing: Typing as React.FC<{o: never; c: Ctx}>,
  chips: Chips as React.FC<{o: never; c: Ctx}>,
  leader: Leader as React.FC<{o: never; c: Ctx}>,
};

export const OverlayLayer: React.FC<{
  overlays: Overlay[];
  shots: Shot[];
  assets: Record<string, Asset>;
  style: Style;
  layer: 'front' | 'behind';
  width: number;
  height: number;
}> = ({overlays, shots, assets, style, layer, width, height}) => {
  const frame = useCurrentFrame();
  const mo = style.motion;
  return (
    <>
      {overlays
        .filter((o) => (o.layer ?? 'front') === layer && frame >= o.from)
        .map((o) => {
          const si = shots.findIndex((s) => s.id === o.shot);
          const shot = shots[si];
          const isLast = si === shots.length - 1;
          const asset = assets[shot.asset];
          // Overlays leave fast, on their own `until` frame or with their shot (scale 1 -> 0.8). With their shot (next
          // hero or chapter card) or on a hero handover they are gone in 3 frames (0.30, 0.04, 0), so no label of the
          // outgoing shot lingers over what comes next; a mid-shot exit takes 5 (0.49, 0.22, 0.06).
          const exitAt = o.until !== undefined ? o.until : isLast ? undefined : shot.to;
          const fast = o.until === undefined || shots.some((s) => s.from === exitAt);
          let out = leave(frame, exitAt, fast ? 3 : 5);
          const outScale = exitAt === undefined ? 1 : lerp(1, mo.exit_to, progress(frame, exitAt, mo.exit));
          if (out <= 0.001) return null;
          const pose = heroPose(shot, asset, style, frame, isLast);
          // Anchored overlays belong to the object: they can never be more visible than the hero's entrance,
          // so an accent that starts on a handover frame never lands on the outgoing object.
          if (o.anchor) out *= pose.enterOpacity;
          const at: Vec2 = o.anchor ? toScreen(pose, asset, o.anchor) : (o.pos ?? [width / 2, height / 2]);
          const geo = o.anchor ? pose.zoom * pose.anim : outScale;
          const R = RENDERERS[o.type];
          if (!R) throw new Error(`Overlay ${o.id}: unknown type "${o.type}"`);
          const c: Ctx = {frame, style, pose, asset, out, outScale, geo, at, width, height};
          return <R key={o.id} o={o as never} c={c} />;
        })}
    </>
  );
};
