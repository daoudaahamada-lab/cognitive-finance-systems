// Track evaluation and scene-graph transforms of the Story composition.
// pipeline/story.py mirrors this file exactly (same easings, same LEAD, same matrices): the builder computes
// world positions (re-parenting, anchors, paths along wires) with the very numbers the renderer will use.
import type {Anchor, Ease, Entity, Key, Track, Value, Vec2} from './types';

/** Frame `f` of a segment already shows step 1/d (events appear on their word-onset frame). */
export const LEAD = 1;

const cubeOut = (t: number) => 1 - (1 - t) ** 3;
export const EASES: Record<Ease, (t: number) => number> = {
  linear: (t) => t,
  out: cubeOut,
  in: (t) => t ** 3,
  inOut: (t) => (t < 0.5 ? 4 * t ** 3 : 1 - ((1 - t) * 2) ** 3 / 2),
  outQuad: (t) => 1 - (1 - t) ** 2,
  inOutSine: (t) => (1 - Math.cos(Math.PI * t)) / 2,
};

const clamp01 = (x: number) => (x < 0 ? 0 : x > 1 ? 1 : x);

export const progressOf = (key: Key, n: number): number => {
  const d = key.d ?? 0;
  if (d <= 0) return n >= key.f ? 1 : 0;
  return EASES[key.e ?? 'out'](clamp01((n - key.f + LEAD) / d));
};

const hex = (c: string): number[] => [1, 3, 5].map((i) => parseInt(c.slice(i, i + 2), 16));
export const mixHex = (a: string, b: string, p: number): string => {
  const A = hex(a);
  const B = hex(b);
  return '#' + A.map((x, i) => Math.round(x + (B[i] - x) * p).toString(16).padStart(2, '0')).join('');
};

const mix = (a: Value, b: Value, p: number, arc?: number): Value => {
  if (typeof a === 'number' && typeof b === 'number') return a + (b - a) * p;
  if (Array.isArray(a) && Array.isArray(b)) {
    const out = a.map((x, i) => x + ((b[i] as number) - x) * p);
    if (arc && out.length === 2) out[1] -= arc * 4 * p * (1 - p);
    return out;
  }
  if (typeof a === 'string' && typeof b === 'string' && a.startsWith('#') && b.startsWith('#') && a.length === 7 && b.length === 7) {
    return mixHex(a, b, p);
  }
  // Text, booleans: switch on the first frame of the segment.
  return p > 0 ? b : a;
};

export function evalTrack(track: Track | undefined, n: number, fallback: Value): Value {
  if (!track || track.length === 0) return fallback;
  let seg: Key | null = null;
  let start: Value = track[0].v;
  for (let k = 1; k < track.length; k++) {
    const key = track[k];
    if (n < key.f) break;
    // Start value of this segment: the value on frame f - 1 under the previous segment.
    start = seg ? mix(start, seg.v, progressOf(seg, key.f - 1), seg.arc) : track[0].v;
    seg = key;
  }
  return seg ? mix(start, seg.v, progressOf(seg, n), seg.arc) : track[0].v;
}

// ---------- 2D affine matrices [a, b, c, d, e, f]: x' = a x + c y + e, y' = b x + d y + f ----------
export type Mat = [number, number, number, number, number, number];
export const IDENTITY: Mat = [1, 0, 0, 1, 0, 0];

export const mul = (m: Mat, n: Mat): Mat => [
  m[0] * n[0] + m[2] * n[1],
  m[1] * n[0] + m[3] * n[1],
  m[0] * n[2] + m[2] * n[3],
  m[1] * n[2] + m[3] * n[3],
  m[0] * n[4] + m[2] * n[5] + m[4],
  m[1] * n[4] + m[3] * n[5] + m[5],
];

export const apply = (m: Mat, p: Vec2): Vec2 => [m[0] * p[0] + m[2] * p[1] + m[4], m[1] * p[0] + m[3] * p[1] + m[5]];

/** T(pos) . R(rot) . S(scale * sx, scale * sy) */
export const localMatrix = (pos: Vec2, rot: number, sx: number, sy: number): Mat => {
  const r = (rot * Math.PI) / 180;
  const c = Math.cos(r);
  const s = Math.sin(r);
  return [c * sx, s * sx, -s * sy, c * sy, pos[0], pos[1]];
};

export type Resolved = {
  e: Entity;
  world: Mat;
  opacity: number;
  /** Value of one of the entity's tracks at the current frame. */
  get: <T extends Value>(name: string, fallback: T) => T;
};

/** Evaluates every entity at film frame n: world matrices (parents first) and cumulated opacity. */
export class SceneFrame {
  readonly n: number;
  private byId = new Map<string, Entity>();
  private cache = new Map<string, Resolved>();

  constructor(entities: Entity[], n: number) {
    this.n = n;
    for (const e of entities) this.byId.set(e.id, e);
  }

  resolve(id: string): Resolved {
    const hit = this.cache.get(id);
    if (hit) return hit;
    const e = this.byId.get(id);
    if (!e) throw new Error(`Story: unknown entity "${id}"`);
    const get = <T extends Value>(name: string, fallback: T): T => evalTrack(e.t[name], this.n, fallback) as T;
    const pos = get<number[]>('pos', [0, 0]) as Vec2;
    const scale = get('scale', 1);
    const local = localMatrix(pos, get('rot', 0), scale * get('sx', 1), scale * get('sy', 1));
    let world = local;
    let opacity = get('opacity', 1);
    if (e.parent) {
      const p = this.resolve(e.parent);
      world = mul(p.world, local);
      opacity *= p.opacity;
    }
    const r: Resolved = {e, world, opacity, get};
    this.cache.set(id, r);
    return r;
  }

  /** World position of a point given in an entity's local coordinates. */
  anchor(a: Anchor): Vec2 {
    return apply(this.resolve(a.id).world, a.at);
  }
}

/** Cubic of a wire: horizontal tangents (S-curve), `sag` px pulls both handles down (droop). */
export const wireCubic = (a: Vec2, b: Vec2, sag: number, tension = 0.45): [Vec2, Vec2, Vec2, Vec2] => {
  const dx = (b[0] - a[0]) * tension;
  return [a, [a[0] + dx, a[1] + sag], [b[0] - dx, b[1] + sag], b];
};

export const cubicAt = (c: [Vec2, Vec2, Vec2, Vec2], t: number): Vec2 => {
  const u = 1 - t;
  const w = [u * u * u, 3 * u * u * t, 3 * u * t * t, t * t * t];
  return [
    w[0] * c[0][0] + w[1] * c[1][0] + w[2] * c[2][0] + w[3] * c[3][0],
    w[0] * c[0][1] + w[1] * c[1][1] + w[2] * c[2][1] + w[3] * c[3][1],
  ];
};

export const cubicLength = (c: [Vec2, Vec2, Vec2, Vec2], steps = 32): number => {
  let len = 0;
  let prev = c[0];
  for (let i = 1; i <= steps; i++) {
    const p = cubicAt(c, i / steps);
    len += Math.hypot(p[0] - prev[0], p[1] - prev[1]);
    prev = p;
  }
  return len;
};

/**
 * Path of a wire or beam: the S-cubic of wireCubic from A to `via` (or to B), then, with a via point, a straight
 * segment via -> B. A beam routed through a via point enters its target row horizontally from outside the bullet
 * column instead of cutting across it.
 */
export type WirePath = {d: string; len: number; pointAt: (frac: number) => Vec2};
export const wirePath = (a: Vec2, b: Vec2, sag: number, tension = 0.45, via?: Vec2 | null): WirePath => {
  const end = via ?? b;
  const cub = wireCubic(a, end, sag, tension);
  const n = 32;
  const pts: Vec2[] = [];
  for (let i = 0; i <= n; i++) pts.push(cubicAt(cub, i / n));
  if (via) pts.push(b);
  const acc: number[] = [0];
  for (let i = 1; i < pts.length; i++) acc.push(acc[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
  const len = acc[acc.length - 1];
  let d = `M${cub[0][0]},${cub[0][1]} C${cub[1][0]},${cub[1][1]} ${cub[2][0]},${cub[2][1]} ${cub[3][0]},${cub[3][1]}`;
  if (via) d += ` L${b[0]},${b[1]}`;
  const pointAt = (frac: number): Vec2 => {
    const target = Math.max(0, Math.min(1, frac)) * len;
    for (let i = 1; i < pts.length; i++) {
      if (acc[i] >= target) {
        const t = (target - acc[i - 1]) / Math.max(1e-6, acc[i] - acc[i - 1]);
        return [pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * t, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * t];
      }
    }
    return pts[pts.length - 1];
  };
  return {d, len, pointAt};
};

/**
 * stroke-dasharray that shows the first `p` of a path of length `len`, optionally with a dash pattern
 * (dashes then gaps; [0, gap] with round caps = dots). Lets a dashed / dotted outline be "drawn on".
 */
export const drawDash = (len: number, p: number, pattern?: number[]): string | undefined => {
  if (p >= 0.999 && !pattern) return undefined;
  const shown = Math.max(0, Math.min(1, p)) * len;
  if (!pattern || pattern.length === 0) return `${shown} ${len + 10}`;
  const out: number[] = [];
  let acc = 0;
  let k = 0;
  while (acc < shown) {
    const seg = pattern[k % pattern.length];
    const on = k % 2 === 0;
    const take = Math.min(seg, shown - acc);
    if (on) out.push(take);
    else out.push(take);
    acc += take;
    k++;
  }
  if (out.length % 2 === 1) out.push(len + 10);
  else out.push(0, len + 10);
  return out.join(' ');
};
