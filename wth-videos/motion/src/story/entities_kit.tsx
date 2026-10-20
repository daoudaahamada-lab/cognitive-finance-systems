// Kit d'entités génériques de la composition Story (méthode validée sur V01) : formes, texte, pictogramme, secteur,
// jauge, compteur, courbe, bascule, curseur, carte de fin, foule. Même style plat que entities.tsx : contours encre
// 4-5 px, ombre dure +6/+6 sans flou (orientée bas-droite quelle que soit la rotation), couleurs de props.style.
//
// Couleurs : un nom de la palette (ink, cyan, deep, light, paper, grey, slot, rule, red, aiTick / ai_tick, none) ou un
// hex « #RRGGBB ». Une piste de couleur ne s'interpole qu'entre deux hex (sinon elle bascule sur la 1re image).
// Paramètres et pistes de chaque type : .claude/skills/wth-story-build/references/entities.md (racine du dépôt).
import React from 'react';
import {ClientGlyph, Hard, Icon, roundRect, roundRectLength, Txt, usePalette, worldShadow, type Palette} from './draw';
import type {EntityProps} from './entities';
import type {Mat} from './timeline';
import type {Vec2} from './types';

const clamp01 = (x: number) => (x < 0 ? 0 : x > 1 ? 1 : x);
const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

/** Couleur : nom de la palette ou hex ; `none` = pas de remplissage. */
export const paint = (C: Palette, v: string | undefined, fallback: string): string => {
  const c = v ?? fallback;
  if (c.startsWith('#') || c === 'none') return c;
  const k = (c === 'ai_tick' ? 'aiTick' : c) as keyof Palette;
  return C[k] ?? fallback;
};

/** Ombre dure à `off` px écran vers le bas-droite (rotation annulée, échelle conservée comme les autres entités). */
const shadowOf = (m: Mat, off: number): [number, number] => worldShadow(m, off * Math.sqrt(Math.abs(m[0] * m[3] - m[1] * m[2])));

/** Polyligne échantillonnée : longueurs cumulées, sous-chemin jusqu'à une fraction, point courant. */
type Poly = {pts: Vec2[]; acc: number[]; len: number};
const poly = (pts: Vec2[]): Poly => {
  const acc = [0];
  for (let i = 1; i < pts.length; i++) acc.push(acc[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
  return {pts, acc, len: acc[acc.length - 1]};
};
const polyUpTo = (P: Poly, frac: number): Vec2[] => {
  const target = clamp01(frac) * P.len;
  const out: Vec2[] = [P.pts[0]];
  for (let i = 1; i < P.pts.length; i++) {
    if (P.acc[i] <= target) {
      out.push(P.pts[i]);
      continue;
    }
    const t = (target - P.acc[i - 1]) / Math.max(1e-6, P.acc[i] - P.acc[i - 1]);
    out.push([lerp(P.pts[i - 1][0], P.pts[i][0], t), lerp(P.pts[i - 1][1], P.pts[i][1], t)]);
    break;
  }
  return out;
};
const pathOf = (pts: Vec2[], closed = false) =>
  pts.map(([x, y], i) => `${i ? 'L' : 'M'}${x.toFixed(2)},${y.toFixed(2)}`).join(' ') + (closed ? ' Z' : '');

/** Catmull-Rom uniforme -> polyligne (`n` pas par segment) : courbe lisse qui passe par chaque point. */
const smoothPts = (P: Vec2[], n = 16): Vec2[] => {
  if (P.length < 3) return P;
  const out: Vec2[] = [P[0]];
  for (let i = 0; i < P.length - 1; i++) {
    const p0 = P[Math.max(0, i - 1)];
    const p1 = P[i];
    const p2 = P[i + 1];
    const p3 = P[Math.min(P.length - 1, i + 2)];
    for (let s = 1; s <= n; s++) {
      const t = s / n;
      const t2 = t * t;
      const t3 = t2 * t;
      const f = (a: number, b: number, c: number, d: number) =>
        0.5 * (2 * b + (-a + c) * t + (2 * a - 5 * b + 4 * c - d) * t2 + (-a + 3 * b - 3 * c + d) * t3);
      out.push([f(p0[0], p1[0], p2[0], p3[0]), f(p0[1], p1[1], p2[1], p3[1])]);
    }
  }
  return out;
};

const ellipseLength = (a: number, b: number) => Math.PI * (3 * (a + b) - Math.sqrt((3 * a + b) * (a + 3 * b)));

// ---------- shape : rect, round (rectangle arrondi), circle, ellipse, poly ----------
// Pistes : w, h, r (rayon des coins), fill, stroke, draw (contour tracé 0 -> 1, depuis le haut / le 1er point),
// fillOp (opacité de l'aplat et de l'ombre ; par défaut 1 dès que le contour est fermé, 0 avant).
type ShapeP = {kind?: 'rect' | 'round' | 'circle' | 'ellipse' | 'poly'; w?: number; h?: number; r?: number; pts?: Vec2[];
  closed?: boolean; fill?: string; stroke?: string; sw?: number; shadow?: number; dash?: number[]};
const shapeGeom = (p: ShapeP, w: number, h: number, rr: number): {d: string; len: number; closed: boolean} => {
  const kind = p.kind ?? 'round';
  if (kind === 'circle' || kind === 'ellipse') {
    const a = w / 2;
    const b = kind === 'circle' ? w / 2 : h / 2;
    return {d: `M0,${-b} A${a},${b} 0 1 1 0,${b} A${a},${b} 0 1 1 0,${-b} Z`, len: ellipseLength(a, b), closed: true};
  }
  if (kind === 'poly') {
    const pts = p.pts ?? [];
    const closed = p.closed !== false;
    const P = poly(closed ? [...pts, pts[0]] : pts);
    return {d: pathOf(pts, closed), len: P.len, closed};
  }
  const k = kind === 'rect' ? 0 : rr;
  return {d: roundRect(-w / 2, -h / 2, w, h, k), len: roundRectLength(w, h, k), closed: true};
};
const Shape: React.FC<EntityProps> = ({r}) => {
  const C = usePalette();
  const p = r.e.p as ShapeP;
  const w = r.get('w', p.w ?? 200);
  const h = r.get('h', p.h ?? p.w ?? 200);
  const rr = r.get('r', p.r ?? 18);
  const draw = clamp01(r.get('draw', 1));
  if (draw <= 0) return null;
  const g = shapeGeom(p, w, h, rr);
  const fill = paint(C, r.get('fill', p.fill ?? 'paper'), C.paper);
  const stroke = paint(C, r.get('stroke', p.stroke ?? 'ink'), C.ink);
  const sw = p.sw ?? 4;
  const fillOp = g.closed ? clamp01(r.get('fillOp', draw >= 0.999 ? 1 : 0)) : 0;
  const dash = draw < 0.999 || p.dash ? (draw < 0.999 ? `${draw * g.len} ${g.len + 10}` : p.dash!.join(' ')) : undefined;
  const sh = p.shadow ?? 6;
  return (
    <>
      {fillOp > 0.001 && fill !== 'none' ? (
        <g opacity={fillOp < 0.999 ? fillOp : undefined}>
          <Hard off={sh ? shadowOf(r.world, sh) : 0} render={(s) => <path d={g.d} fill={s ? C.ink : fill} stroke={s ? C.ink : 'none'} strokeWidth={sw} strokeLinejoin="round" />} />
        </g>
      ) : null}
      <path d={g.d} fill="none" stroke={stroke} strokeWidth={sw} strokeLinejoin="round" strokeLinecap="round" strokeDasharray={dash} />
    </>
  );
};

// ---------- text : texte libre (1 ou plusieurs lignes « \n »), machine à écrire, surligneur, soulignement ----------
// Pistes : chars (caractères visibles, sauts de ligne non comptés ; la suite est posée mais transparente : un texte
// centré ne glisse pas pendant la frappe), text (bascule de texte), color, mark (surligneur cyan clair tiré de gauche
// à droite derrière le texte, 0 -> 1 ; il faut `w`), under (trait souligné tracé, 0 -> 1 ; il faut `w`).
type TextP = {text: string; size?: number; weight?: number; color?: string; anchor?: 'start' | 'middle' | 'end';
  spacing?: number; lh?: number; w?: number; markColor?: string; underColor?: string};
const Text: React.FC<EntityProps> = ({r}) => {
  const C = usePalette();
  const p = r.e.p as TextP;
  const text = r.get('text', p.text);
  const size = p.size ?? 40;
  const anchor = p.anchor ?? 'middle';
  const chars = Math.floor(r.get('chars', 1e6) + 1e-6);
  const color = paint(C, r.get('color', p.color ?? 'ink'), C.ink);
  const mark = clamp01(r.get('mark', 0));
  const under = clamp01(r.get('under', 0));
  const lines = text.split('\n');
  const lh = size * (p.lh ?? 1.18);
  let left = chars;
  const shown = lines.map((l) => {
    const n = Math.max(0, Math.min(l.length, left));
    left -= l.length;
    return [l.slice(0, n), l.slice(n)];
  });
  const w = p.w ?? 0;
  const x0 = anchor === 'middle' ? -w / 2 : anchor === 'end' ? -w : 0;
  const top = -((lines.length - 1) * lh) / 2;
  const bottom = top + (lines.length - 1) * lh + size * 0.62;
  return (
    <>
      {mark > 0 && w > 0 ? (
        <rect x={x0 - size * 0.18} y={top - size * 0.56} width={(w + size * 0.36) * mark} height={(lines.length - 1) * lh + size * 1.12} rx={size * 0.16} fill={paint(C, p.markColor, C.light)} />
      ) : null}
      {shown.map(([s, rest], i) =>
        s ? (
          <Txt key={i} x={0} y={top + i * lh} size={size} weight={p.weight ?? 700} color={color} anchor={anchor} spacing={p.spacing}>
            {rest ? (
              <>
                <tspan>{s}</tspan>
                <tspan fillOpacity={0}>{rest}</tspan>
              </>
            ) : (
              s
            )}
          </Txt>
        ) : null,
      )}
      {under > 0 && w > 0 ? (
        <path d={`M${x0},${bottom} H${x0 + w * under}`} stroke={paint(C, p.underColor, C.deep)} strokeWidth={Math.max(4, size * 0.1)} strokeLinecap="round" />
      ) : null}
    </>
  );
};

// ---------- icon : pictogramme seul (trait encre) ou posé sur un disque (aplat + contour + ombre dure) ----------
// Pistes : color (pictogramme), fill (disque), ring (anneau deep autour du disque, 0 -> 1 tracé : « coché »).
type IconP = {name: string; s?: number; color?: string; sw?: number; disc?: number; fill?: string; shadow?: number; ringColor?: string};
const IconEnt: React.FC<EntityProps> = ({r}) => {
  const C = usePalette();
  const p = r.e.p as IconP;
  const color = paint(C, r.get('color', p.color ?? 'ink'), C.ink);
  const ring = clamp01(r.get('ring', 0));
  if (!p.disc) return <Icon name={p.name} s={p.s ?? 64} color={color} sw={p.sw} />;
  const R = p.disc;
  const fill = paint(C, r.get('fill', p.fill ?? 'cyan'), C.cyan);
  const rl = 2 * Math.PI * (R + 10);
  return (
    <>
      <Hard off={shadowOf(r.world, p.shadow ?? (R < 25 ? 3 : 6))} render={(sh) => <circle cx={0} cy={0} r={R} fill={sh ? C.ink : fill} stroke={C.ink} strokeWidth={R < 25 ? 3 : 4} />} />
      <Icon name={p.name} s={p.s ?? R * 1.15} color={color} sw={p.sw ?? Math.max(2.6, R * 0.11)} />
      {ring > 0 ? (
        <circle cx={0} cy={0} r={R + 10} fill="none" stroke={paint(C, p.ringColor, C.deep)} strokeWidth={4} transform="rotate(-90)" strokeDasharray={`${ring * rl} ${rl + 10}`} strokeLinecap="round" />
      ) : null}
    </>
  );
};

// ---------- sector : cadran et secteur de temps (le « secteur de 10 minutes ») ----------
// unit = unités par tour (60 : minutes), 0 = midi. Pistes : start (début du secteur, unités), value (taille du
// secteur, unités ; >= unit = disque plein), fill. `face: 'none'` = secteur seul, à poser sur le cadran d'un PNG.
type SectorP = {r?: number; unit?: number; face?: string; fill?: string; alpha?: number; ticks?: number; hand?: boolean;
  edge?: number; sw?: number; shadow?: number};
const polar = (R: number, u: number, unit: number): Vec2 => {
  const a = ((-90 + (360 * u) / unit) * Math.PI) / 180;
  return [R * Math.cos(a), R * Math.sin(a)];
};
const Sector: React.FC<EntityProps> = ({r}) => {
  const C = usePalette();
  const p = r.e.p as SectorP;
  const R = p.r ?? 120;
  const unit = p.unit ?? 60;
  const face = p.face ?? 'paper';
  const start = r.get('start', 0);
  const v = Math.max(0, r.get('value', 0));
  const fill = paint(C, r.get('fill', p.fill ?? 'deep'), C.deep);
  const ticks = p.ticks ?? (face === 'none' ? 0 : 12);
  const edge = p.edge ?? (face === 'none' ? 0 : 3);
  const Rw = face === 'none' ? R : R - 2;
  let wedge: string | null = null;
  if (v >= unit - 1e-6) wedge = `M0,${-Rw} A${Rw},${Rw} 0 1 1 0,${Rw} A${Rw},${Rw} 0 1 1 0,${-Rw} Z`;
  else if (v > 1e-3) {
    const a = polar(Rw, start, unit);
    const b = polar(Rw, start + v, unit);
    wedge = `M0,0 L${a[0].toFixed(2)},${a[1].toFixed(2)} A${Rw},${Rw} 0 ${v > unit / 2 ? 1 : 0} 1 ${b[0].toFixed(2)},${b[1].toFixed(2)} Z`;
  }
  const end = polar(R * 0.72, start + v, unit);
  const sw = p.sw ?? 5;
  return (
    <>
      {face !== 'none' ? (
        <Hard off={shadowOf(r.world, p.shadow ?? 6)} render={(sh) => <circle cx={0} cy={0} r={R} fill={sh ? C.ink : paint(C, face, C.paper)} stroke={C.ink} strokeWidth={sw} />} />
      ) : null}
      {wedge ? <path d={wedge} fill={fill} fillOpacity={p.alpha ?? (face === 'none' ? 0.6 : 1)} stroke={edge ? C.ink : 'none'} strokeWidth={edge} strokeLinejoin="round" /> : null}
      {Array.from({length: ticks}, (_, i) => {
        const a = polar(R - 10, (unit * i) / ticks, unit);
        const b = polar(R - (i % 3 === 0 ? 26 : 19), (unit * i) / ticks, unit);
        return <line key={i} x1={a[0]} y1={a[1]} x2={b[0]} y2={b[1]} stroke={C.ink} strokeWidth={i % 3 === 0 ? 5 : 3.5} strokeLinecap="round" />;
      })}
      {p.hand !== false && face !== 'none' ? (
        <>
          <line x1={0} y1={0} x2={end[0]} y2={end[1]} stroke={C.ink} strokeWidth={7} strokeLinecap="round" />
          <circle cx={0} cy={0} r={9} fill={C.ink} />
        </>
      ) : null}
    </>
  );
};

// ---------- gauge : barre de temps / de budget, remplie de `value` (0 -> 1) depuis le côté `dir` ----------
// dir : right (remplit de gauche à droite), left (le reste est collé à droite : la barre « fond » vers la droite),
// up, down. segments : séparateurs (blocs, jetons) ; marks : repères (fractions comptées depuis l'origine du
// remplissage, ex. 0,8 = budget). Pistes : value, fill (couleur ; ex. cyan -> rouge au dépassement), w, h.
type GaugeP = {w?: number; h?: number; r?: number; fill?: string; empty?: string; sw?: number; shadow?: number;
  dir?: 'right' | 'left' | 'up' | 'down'; segments?: number; marks?: number[]};
const Gauge: React.FC<EntityProps> = ({r}) => {
  const C = usePalette();
  const p = r.e.p as GaugeP;
  const w = r.get('w', p.w ?? 600);
  const h = r.get('h', p.h ?? 48);
  const rr = p.r ?? Math.min(14, Math.min(w, h) / 2);
  const v = clamp01(r.get('value', 1));
  const fill = paint(C, r.get('fill', p.fill ?? 'cyan'), C.cyan);
  const dir = p.dir ?? 'right';
  const sw = p.sw ?? 4;
  const x0 = -w / 2;
  const y0 = -h / 2;
  const fr: [number, number, number, number] =
    dir === 'right' ? [x0, y0, w * v, h] : dir === 'left' ? [x0 + w * (1 - v), y0, w * v, h] : dir === 'up' ? [x0, y0 + h * (1 - v), w, h * v] : [x0, y0, w, h * v];
  const id = `${r.e.id}-gauge`;
  const body = roundRect(x0, y0, w, h, rr);
  const n = p.segments ?? 0;
  const vertical = dir === 'up' || dir === 'down';
  return (
    <>
      <Hard off={shadowOf(r.world, p.shadow ?? 6)} render={(sh) => <path d={body} fill={sh ? C.ink : paint(C, p.empty, C.paper)} />} />
      <defs>
        <clipPath id={id}>
          <path d={body} />
        </clipPath>
      </defs>
      {v > 0.001 ? <rect x={fr[0]} y={fr[1]} width={fr[2]} height={fr[3]} fill={fill} clipPath={`url(#${id})`} /> : null}
      {Array.from({length: Math.max(0, n - 1)}, (_, i) => {
        const t = (i + 1) / n;
        return vertical ? (
          <line key={i} x1={x0} x2={x0 + w} y1={y0 + h * t} y2={y0 + h * t} stroke={C.ink} strokeWidth={3} />
        ) : (
          <line key={i} x1={x0 + w * t} x2={x0 + w * t} y1={y0} y2={y0 + h} stroke={C.ink} strokeWidth={3} />
        );
      })}
      {(p.marks ?? []).map((t, i) => {
        const u = dir === 'left' || dir === 'up' ? 1 - t : t;
        return vertical ? (
          <line key={`m${i}`} x1={x0 - 10} x2={x0 + w + 10} y1={y0 + h * u} y2={y0 + h * u} stroke={C.ink} strokeWidth={4} strokeLinecap="round" />
        ) : (
          <line key={`m${i}`} x1={x0 + w * u} x2={x0 + w * u} y1={y0 - 10} y2={y0 + h + 10} stroke={C.ink} strokeWidth={4} strokeLinecap="round" />
        );
      })}
      <path d={body} fill="none" stroke={C.ink} strokeWidth={sw} strokeLinejoin="round" />
    </>
  );
};

// ---------- counter : nombre interpolé, typographie française (12 500 €, 3,5 %, −40 €) ----------
// Pistes : value (nombre, interpolé image par image), color. Chiffres à chasse fixe : la largeur ne tremble pas.
type CounterP = {size?: number; weight?: number; color?: string; decimals?: number; prefix?: string; suffix?: string;
  anchor?: 'start' | 'middle' | 'end'; sign?: boolean};
/** Format français : espace fine insécable (U+202F) entre milliers, virgule décimale, vrai signe moins (U+2212). */
export const formatFr = (v: number, decimals = 0, sign = false): string => {
  const k = 10 ** decimals;
  const x = Math.round(Math.abs(v) * k) / k;
  const [ent, dec] = x.toFixed(decimals).split('.');
  const grouped = ent.replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
  const s = x === 0 ? '' : v < 0 ? '−' : sign ? '+' : '';
  return s + grouped + (dec ? ',' + dec : '');
};
const Counter: React.FC<EntityProps> = ({r}) => {
  const C = usePalette();
  const p = r.e.p as CounterP;
  const v = r.get('value', 0);
  // espace collée à l'unité : insécable (« 500 € » ne se coupe pas, « 3,5 % »)
  const pre = (p.prefix ?? '').replace(/ $/, ' ');
  const suf = (p.suffix ?? '').replace(/^ /, ' ');
  return (
    <Txt x={0} y={0} size={p.size ?? 96} weight={p.weight ?? 800} color={paint(C, r.get('color', p.color ?? 'ink'), C.ink)} anchor={p.anchor ?? 'middle'} tabular>
      {pre + formatFr(v, p.decimals ?? 0, p.sign) + suf}
    </Txt>
  );
};

// ---------- curve : courbe tracée (frais, inflation), aire sous la courbe, axes, point de tête ----------
// pts en coordonnées locales (y vers le bas). Pistes : draw (0 -> 1, longueur tracée), color.
type CurveP = {pts: Vec2[]; smooth?: boolean; color?: string; sw?: number; area?: string; base?: number; axes?: boolean | {pad?: number};
  dot?: boolean; dash?: number[]};
const Curve: React.FC<EntityProps> = ({r}) => {
  const C = usePalette();
  const p = r.e.p as CurveP;
  const draw = clamp01(r.get('draw', 1));
  const color = paint(C, r.get('color', p.color ?? 'deep'), C.deep);
  const sw = p.sw ?? 7;
  const P = poly(p.smooth === false ? p.pts : smoothPts(p.pts));
  const shown = draw > 0 ? polyUpTo(P, draw) : [];
  const xs = p.pts.map((q) => q[0]);
  const ys = p.pts.map((q) => q[1]);
  const base = p.base ?? Math.max(...ys);
  const pad = typeof p.axes === 'object' ? (p.axes.pad ?? 24) : 24;
  const ax0 = Math.min(...xs) - pad;
  const ax1 = Math.max(...xs) + pad;
  const ayTop = Math.min(...ys) - pad;
  const head = shown[shown.length - 1];
  return (
    <>
      {p.axes ? (
        <path
          d={`M${ax0},${ayTop} V${base} H${ax1} M${ax0 - 9},${ayTop + 14} L${ax0},${ayTop} L${ax0 + 9},${ayTop + 14} M${ax1 - 14},${base - 9} L${ax1},${base} L${ax1 - 14},${base + 9}`}
          fill="none"
          stroke={C.ink}
          strokeWidth={4}
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      ) : null}
      {p.area && shown.length > 1 ? (
        <path d={`${pathOf(shown)} L${head[0].toFixed(2)},${base} L${shown[0][0].toFixed(2)},${base} Z`} fill={paint(C, p.area, C.light)} />
      ) : null}
      {shown.length > 1 ? (
        <path d={pathOf(shown)} fill="none" stroke={color} strokeWidth={sw} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={p.dash?.join(' ')} />
      ) : null}
      {p.dot !== false && head && draw > 0 ? (
        <Hard off={shadowOf(r.world, 3)} render={(sh) => <circle cx={head[0]} cy={head[1]} r={sw * 1.5} fill={sh ? C.ink : color} stroke={C.ink} strokeWidth={3} />} />
      ) : null}
    </>
  );
};

// ---------- seesaw : planche à bascule. Origine = sommet du pivot (milieu du dessous de la planche) ----------
// La bascule = piste `rot` de l'entité (degrés, > 0 : le côté droit descend) : les entités posées sur la planche
// (parent = la bascule, y < -h) basculent avec elle ; le pivot, contre-tourné, reste droit sur le sol.
type SeesawP = {w?: number; h?: number; fill?: string; base?: string; baseW?: number; baseH?: number; ground?: number; sw?: number; shadow?: number};
const Seesaw: React.FC<EntityProps> = ({r}) => {
  const C = usePalette();
  const p = r.e.p as SeesawP;
  const w = p.w ?? 640;
  const h = p.h ?? 24;
  const bw = p.baseW ?? 120;
  const bh = p.baseH ?? 90;
  const sw = p.sw ?? 5;
  const rot = r.get('rot', 0);
  const off = p.shadow ?? 6;
  const rad = (-rot * Math.PI) / 180;
  const c = Math.cos(rad);
  const s = Math.sin(rad);
  const m = r.world;
  // matrice du pivot (planche contre-tournée) : son ombre tombe aussi en bas à droite
  const mb: Mat = [m[0] * c + m[2] * s, m[1] * c + m[3] * s, -m[0] * s + m[2] * c, -m[1] * s + m[3] * c, m[4], m[5]];
  const ground = p.ground ?? bw + 120;
  // posé sur un sol, le pivot ne projette son ombre que vers la droite (elle ne passe pas sous la ligne de sol)
  const baseOff: [number, number] = ground > 0 ? [off, 0] : shadowOf(mb, off);
  return (
    <>
      <g transform={`rotate(${-rot})`}>
        {ground > 0 ? <line x1={-ground / 2} x2={ground / 2} y1={bh} y2={bh} stroke={C.ink} strokeWidth={sw} strokeLinecap="round" /> : null}
        <Hard
          off={baseOff}
          render={(sh) => (
            <path d={`M0,0 L${bw / 2},${bh} H${-bw / 2} Z`} fill={sh ? C.ink : paint(C, p.base, C.paper)} stroke={C.ink} strokeWidth={sw} strokeLinejoin="round" />
          )}
        />
      </g>
      <Hard off={shadowOf(m, off)} render={(sh) => <path d={roundRect(-w / 2, -h, w, h, h / 2)} fill={sh ? C.ink : paint(C, p.fill, C.ink)} stroke={C.ink} strokeWidth={sw} />} />
    </>
  );
};

// ---------- cursor : pointeur (la main du conseiller à l'écran). Origine = pointe de la flèche ----------
// Pistes : press (0 -> 1 : la flèche s'enfonce, x0,85), ring (0 -> 1 : deux ondes deep partent de la pointe, le clic).
type CursorP = {fill?: string; edge?: string; size?: number; shadow?: number};
const CURSOR = 'M0,0 L0,44 L10.5,34 L18,51 L26.5,47.5 L19,31 L33,31 Z';
const Cursor: React.FC<EntityProps> = ({r}) => {
  const C = usePalette();
  const p = r.e.p as CursorP;
  const k = (p.size ?? 64) / 51;
  const press = clamp01(r.get('press', 0));
  const ring = clamp01(r.get('ring', 0));
  const sc = k * (1 - 0.15 * press);
  return (
    <>
      {ring > 0 && ring < 1
        ? [0, 0.35].map((dl) => {
            const t = clamp01((ring - dl) / (1 - dl));
            return t > 0 && t < 1 ? <circle key={dl} cx={0} cy={0} r={12 + 52 * t} fill="none" stroke={C.deep} strokeWidth={6 * (1 - t) + 2} opacity={1 - 0.8 * t} /> : null;
          })
        : null}
      <g transform={`scale(${sc})`}>
        <Hard
          off={shadowOf(r.world, (p.shadow ?? 5) * (1 - 0.8 * press)).map((x) => x / sc) as [number, number]}
          render={(sh) => <path d={CURSOR} fill={sh ? C.ink : paint(C, p.fill, C.ink)} stroke={sh ? C.ink : paint(C, p.edge, C.paper)} strokeWidth={3.2} strokeLinejoin="round" />}
        />
      </g>
    </>
  );
};

// ---------- endcard : carte de fin (titre + bouton pilule « S’abonner ») ----------
// Pistes : w, h (la carte naît d'une autre forme), btn (échelle du bouton, 0 -> 1), press (0 -> 1 : le bouton
// s'enfonce dans son ombre), title (opacité du titre). `text` = libellé du bouton, sans bouton si absent.
type EndcardP = {w?: number; h?: number; r?: number; title?: string; titleSize?: number; titleY?: number; text?: string;
  labels?: string[]; labelSize?: number; bw?: number; bh?: number; by?: number; bsize?: number; fill?: string; bfill?: string;
  icon?: string; shadow?: number};
const Endcard: React.FC<EntityProps> = ({r}) => {
  const C = usePalette();
  const p = r.e.p as EndcardP;
  const w = r.get('w', p.w ?? 620);
  const h = r.get('h', p.h ?? 560);
  const rr = p.r ?? 32;
  const btn = Math.max(0, r.get('btn', 1));
  const press = clamp01(r.get('press', 0));
  const title = clamp01(r.get('title', 1));
  const bw = p.bw ?? 380;
  const bh = p.bh ?? 112;
  const by = p.by ?? h / 2 - bh / 2 - 56;
  const off = p.shadow ?? 8;
  const boff = 8 * (1 - press);
  const push = 8 * press;
  const bsize = p.bsize ?? 46;
  const ty = p.titleY ?? -h / 2 + (p.icon ? 214 : 150);
  const ls = p.labelSize ?? 30;
  return (
    <>
      <Hard off={shadowOf(r.world, off)} render={(sh) => <path d={roundRect(-w / 2, -h / 2, w, h, rr)} fill={sh ? C.ink : paint(C, p.fill, C.paper)} stroke={C.ink} strokeWidth={4} />} />
      {p.title && title > 0.01 ? (
        <g opacity={title < 0.99 ? title : undefined}>
          {p.icon ? (
            <g transform={`translate(0 ${ty - 100})`}>
              <Hard off={5} render={(sh) => <circle cx={0} cy={0} r={46} fill={sh ? C.ink : C.cyan} stroke={C.ink} strokeWidth={4} />} />
              <Icon name={p.icon} s={52} color={C.ink} sw={5} />
            </g>
          ) : null}
          <Txt x={0} y={ty} size={p.titleSize ?? 44} weight={700} anchor="middle">
            {p.title}
          </Txt>
          {(p.labels ?? []).map((t, i) => (
            <Txt key={i} x={0} y={ty + 70 + i * ls * 1.3} size={ls} weight={600} color={C.deep} anchor="middle">
              {t}
            </Txt>
          ))}
        </g>
      ) : null}
      {p.text && btn > 0.001 ? (
        <g transform={`translate(${push} ${by + push}) scale(${btn})`}>
          {boff > 0.05 ? <rect x={-bw / 2 + boff} y={-bh / 2 + boff} width={bw} height={bh} rx={bh / 2} fill={C.ink} stroke={C.ink} strokeWidth={4} /> : null}
          <rect x={-bw / 2} y={-bh / 2} width={bw} height={bh} rx={bh / 2} fill={paint(C, p.bfill, C.cyan)} stroke={C.ink} strokeWidth={4} />
          <Txt x={0} y={0} size={bsize} weight={800} anchor="middle">
            {p.text}
          </Txt>
        </g>
      ) : null}
    </>
  );
};

// ---------- crowd : n petites figurines (ClientGlyph), en anneau, en arc ou en rang, reliées ou non à l'origine ----------
// layout : ring (anneau de rayon r, de a0 sur span degrés), row (rang centré, pas `gap`), pts (positions données).
// Pistes : show (0 -> n : la figurine i apparaît pendant show de i à i + 1), link (0 -> 1 : traits fins tirés de
// l'origine, la tête de l'IA grand public, vers chaque figurine), tone (couleur du contour : hex pour un fondu).
type CrowdP = {n?: number; h?: number; layout?: 'ring' | 'row'; r?: number; a0?: number; span?: number; gap?: number; pts?: Vec2[];
  fill?: string; tone?: string; sw?: number; link?: boolean; linkColor?: string; linkSw?: number};
export const crowdPoints = (p: CrowdP): Vec2[] => {
  if (p.pts) return p.pts;
  const n = p.n ?? 6;
  if (p.layout === 'row') {
    const gap = p.gap ?? 56;
    return Array.from({length: n}, (_, i) => [(i - (n - 1) / 2) * gap, 0] as Vec2);
  }
  const R = p.r ?? 130;
  const span = p.span ?? 360;
  const a0 = p.a0 ?? -90;
  const step = span >= 360 ? span / n : span / Math.max(1, n - 1);
  return Array.from({length: n}, (_, i) => {
    const a = ((a0 + step * i) * Math.PI) / 180;
    return [R * Math.cos(a), R * Math.sin(a)] as Vec2;
  });
};
const Crowd: React.FC<EntityProps> = ({r}) => {
  const C = usePalette();
  const p = r.e.p as CrowdP;
  const pts = crowdPoints(p);
  const show = r.get('show', pts.length);
  const link = clamp01(r.get('link', p.link ? 1 : 0));
  const tone = paint(C, r.get('tone', p.tone ?? 'aiTick'), C.aiTick);
  const gh = p.h ?? 48;
  return (
    <>
      {link > 0
        ? pts.map(([x, y], i) => {
            const vis = clamp01(show - i);
            return vis > 0 ? (
              <line key={`l${i}`} x1={0} y1={0} x2={x * link} y2={y * link} stroke={paint(C, p.linkColor, C.aiTick)} strokeWidth={p.linkSw ?? 3} strokeLinecap="round" />
            ) : null;
          })
        : null}
      {pts.map(([x, y], i) => {
        const vis = clamp01(show - i);
        if (vis <= 0.001) return null;
        const s = 1 - (1 - vis) ** 3;
        return (
          <g key={i} transform={`translate(${x} ${y}) scale(${s})`}>
            <ClientGlyph h={gh} sw={p.sw ?? 3} fill={paint(C, p.fill, C.paper)} stroke={tone} />
          </g>
        );
      })}
    </>
  );
};

/** Composants du kit, fusionnés dans COMPONENTS (entities.tsx). */
export const KIT: Record<string, React.FC<EntityProps>> = {
  shape: Shape,
  text: Text,
  icon: IconEnt,
  sector: Sector,
  gauge: Gauge,
  counter: Counter,
  curve: Curve,
  seesaw: Seesaw,
  cursor: Cursor,
  endcard: Endcard,
  crowd: Crowd,
};

