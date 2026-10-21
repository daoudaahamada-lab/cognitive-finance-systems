// One React component per entity type. Each draws itself in LOCAL coordinates centred on its origin; the
// Story composition places it with the entity's world matrix (scene graph) and cumulated opacity.
// Flat vector style of the storyboard: ink outlines 3-6 px, hard ink shadows (+6, +3 under 50 px, no blur), Inter.
// Colours come from props.style through usePalette() (draw.tsx).
import React from 'react';
import {Img, staticFile} from 'remotion';
import {BUST, Bullet, ClientGlyph, foldedRect, Hard, HEAD, Icon, roundRect, roundRectLength, sheenPoints, Txt, usePalette, worldShadow, type Palette} from './draw';
import {KIT} from './entities_kit';
import GEOM from './geometry.json';
import {apply, drawDash, mixHex, type Resolved, type SceneFrame, wirePath} from './timeline';
import type {Anchor, Vec2} from './types';

export type EntityProps = {r: Resolved; scene: SceneFrame};

const clamp01 = (x: number) => (x < 0 ? 0 : x > 1 ? 1 : x);
const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

/** Sheen source: the carrier entity (track p, 0 -> 1) and this entity's origin in page coordinates. */
type SheenRef = {id: string; dx: number; dy: number; w: number; h: number; color?: string; opacity?: number};
/** The sheen band of the page, clipped to `clipD` (this entity's local coordinates), drawn under its texts. */
const SheenUnder: React.FC<{sheen?: SheenRef; scene: SceneFrame; clipD: string; uid: string}> = ({sheen, scene, clipD, uid}) => {
  const C = usePalette();
  if (!sheen) return null;
  const s = scene.resolve(sheen.id).get('p', 0);
  if (s <= 0 || s >= 1) return null;
  const id = `${uid}-sheen`;
  return (
    <>
      <defs>
        <clipPath id={id}>
          <path d={clipD} />
        </clipPath>
      </defs>
      <polygon points={sheenPoints(s, sheen.w, sheen.h, sheen.dx, sheen.dy)} clipPath={`url(#${id})`} fill={sheen.color ?? C.light} opacity={sheen.opacity ?? 0.75} />
    </>
  );
};

// ---------- pill: « Client · 9 h », « IA », ... ----------
type PillP = {text: string; w: number; h?: number; size?: number; weight?: number; fill?: string; color?: string;
  stroke?: string; sw?: number; shadow?: number; icon?: string; iconColor?: string; sheen?: SheenRef};
const Pill: React.FC<EntityProps> = ({r, scene}) => {
  const C = usePalette();
  const p = r.e.p as PillP;
  const h = p.h ?? 56;
  const w = r.get('w', p.w);
  const fill = r.get('fill', p.fill ?? C.cyan);
  const text = r.get('text', p.text);
  const size = p.size ?? 28;
  const iconW = p.icon ? 30 : 0;
  return (
    <>
      <Hard
        off={p.shadow ?? 6}
        render={(sh) => (
          <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={h / 2} fill={sh ? C.ink : fill} stroke={p.stroke ?? C.ink} strokeWidth={p.sw ?? 4} />
        )}
      />
      <SheenUnder sheen={p.sheen} scene={scene} clipD={roundRect(-w / 2 + 2, -h / 2 + 2, w - 4, h - 4, h / 2 - 2)} uid={r.e.id} />
      {p.icon ? (
        <g transform={`translate(${-w / 2 + 18 + 12} 0)`}>
          <Icon name={p.icon} s={24} color={p.iconColor ?? C.ink} />
        </g>
      ) : null}
      <Txt x={iconW / 2} y={0} size={size} weight={p.weight ?? 700} color={p.color ?? C.ink} anchor="middle">
        {text}
      </Txt>
    </>
  );
};

// ---------- figure: advisor (full ink) / client (paper) ----------
/** Lean pivot of the figure (its base), shared with the arm anchor (limb). */
export const FIGURE_PIVOT = GEOM.FIGURE.pivot as Vec2;
// Opt-in (absent = today's figure, pixel for pixel): variant 'societe' = paper figure standing under a building
// portico (gable + entablature + two columns on its shoulders) so it reads as a company, not a person; track `look` (-1 .. 1, absent = 0): a small
// nose on the side of the head, the figure seen in profile looking left (< 0) or right (> 0), e.g. turning its back.
const SOC_ROOF = GEOM.FIGURE.societe as {gable: string; beam: number[]; cols: number[][]};
const Figure: React.FC<EntityProps> = ({r}) => {
  const C = usePalette();
  const variant = (r.e.p as {variant?: string}).variant;
  const ink = variant === 'ink';
  const lean = r.get('lean', 0);
  const look = r.get('look', 0);
  const lk = Math.abs(look);
  const sgn = look < 0 ? -1 : 1;
  const nose = lk > 0.01
    ? `M${sgn * (HEAD.r - 4)} ${HEAD.cy - 9} L${sgn * (HEAD.r + 11 * lk)} ${HEAD.cy + 2} L${sgn * (HEAD.r - 4)} ${HEAD.cy + 10} Z`
    : null;
  return (
    <g transform={`rotate(${lean} ${FIGURE_PIVOT[0]} ${FIGURE_PIVOT[1]})`}>
      <Hard
        off={6}
        render={(sh) => (
          <>
            <path d={BUST} fill={sh || ink ? C.ink : C.paper} stroke={C.ink} strokeWidth={GEOM.FIGURE.sw} strokeLinejoin="round" />
            {nose ? <path d={nose} fill={sh || ink ? C.ink : C.paper} stroke={C.ink} strokeWidth={GEOM.FIGURE.sw} strokeLinejoin="round" /> : null}
            <circle cx={0} cy={HEAD.cy} r={HEAD.r} fill={sh || ink ? C.ink : C.paper} stroke={C.ink} strokeWidth={GEOM.FIGURE.sw} />
            {variant === 'societe' ? (
              <>
                <path d={SOC_ROOF.gable} fill={sh ? C.ink : C.paper} stroke={C.ink} strokeWidth={GEOM.FIGURE.sw} strokeLinejoin="round" />
                <rect x={SOC_ROOF.beam[0]} y={SOC_ROOF.beam[1]} width={SOC_ROOF.beam[2]} height={SOC_ROOF.beam[3]} rx={3} fill={C.ink} stroke={C.ink} strokeWidth={2} />
                {SOC_ROOF.cols.map((c, i) => (
                  <rect key={`col${i}`} x={c[0]} y={c[1]} width={c[2]} height={c[3]} rx={2} fill={C.ink} stroke={C.ink} strokeWidth={2} />
                ))}
              </>
            ) : null}
          </>
        )}
      />
    </g>
  );
};

// ---------- png: glass object, strict alpha + soft contact shadow ----------
/**
 * `contact` (optional): soft contact shadow ONLY under the object (blurred ellipse of w x h px, centred `dy` px below
 * the PNG's bottom edge), instead of a drop-shadow halo around the whole silhouette. `saturate` < 1 calms a PNG whose
 * colours would compete with the cyan accent.
 */
// Opt-in (absent = today's drawing, pixel for pixel): tint 'mono' (grey glass: grayscale, slightly lighter), outline
// (px: hard ink contour drawn around the silhouette by 4 zero-blur drop-shadows), flip (mirrored left-right; the
// contact shadow and the children are not mirrored).
type PngP = {src: string; w: number; h: number; shadow?: number; blur?: number; dy?: number; saturate?: number;
  contact?: {w: number; h: number; dy: number; blur: number; alpha: number}; tint?: 'mono'; outline?: number;
  flip?: boolean};
const pngExtra = (p: PngP, ink: string): string => {
  const parts: string[] = [];
  if (p.tint === 'mono') parts.push('grayscale(1) brightness(1.06) contrast(1.04)');
  const o = p.outline ?? 0;
  if (o > 0) parts.push(`drop-shadow(${o}px 0 0 ${ink}) drop-shadow(-${o}px 0 0 ${ink}) drop-shadow(0 ${o}px 0 ${ink}) drop-shadow(0 -${o}px 0 ${ink})`);
  return parts.join(' ');
};
const Png: React.FC<EntityProps> = ({r}) => {
  const p = r.e.p as PngP;
  const C = usePalette();
  const extra = pngExtra(p, C.ink);
  const sat = (p.saturate != null && p.saturate !== 1 ? `saturate(${p.saturate})` : '') + (extra ? ` ${extra}` : '');
  const c = p.contact;
  return (
    <>
      {c ? (
        <div
          style={{
            position: 'absolute',
            left: -c.w / 2,
            top: p.h / 2 + c.dy - c.h / 2,
            width: c.w,
            height: c.h,
            borderRadius: '50%',
            background: `rgba(30, 20, 22, ${c.alpha})`,
            filter: `blur(${c.blur}px)`,
          }}
        />
      ) : null}
      <Img
        src={staticFile(p.src)}
        style={{
          position: 'absolute',
          left: -p.w / 2,
          top: -p.h / 2,
          width: p.w,
          height: p.h,
          filter: c ? sat.trim() || undefined : `drop-shadow(0px ${p.dy ?? 16}px ${p.blur ?? 24}px rgba(30, 20, 22, ${p.shadow ?? 0.16})) ${sat}`.trim(),
          transform: p.flip ? 'scaleX(-1)' : undefined,
        }}
      />
    </>
  );
};

// ---------- window: validated tool (title bar, seal « ✓ Cabinet », padlock); shrinks into a badge ----------
// Opt-in tracks (absent = today's drawing, pixel for pixel): bar (title bar + its 3 dots, drawn -40·(1 - bar) px
// higher at opacity bar), sealOn / sealDy (opacity and vertical offset of the seal: it can fall into place),
// lockOn / lockDy (same for the padlock). bar = sealOn = lockOn = 0 leaves the bare deep-cyan 6 px frame.
// Opt-in sealK (absent = 1, today's drawing): the seal (disc, building, check, « Cabinet ») drawn k times larger;
// give sealW for the open pill at that scale (68k + text_width(sealText, 26k, 700) + 16k).
type WindowP = {titleH?: number; r?: number; sealW: number; sealText: string; sealK?: number};
/** A part of the window shown at opacity `on`, shifted down by `dy` px; untouched (no wrapper) at its defaults. */
const winLayer = (on: number, dy: number, node: React.ReactNode): React.ReactNode => {
  if (on <= 0.001) return null;
  if (on >= 0.999 && dy === 0) return node;
  return (
    <g transform={dy !== 0 ? `translate(0 ${dy})` : undefined} opacity={on < 0.999 ? on : undefined}>
      {node}
    </g>
  );
};
const Window: React.FC<EntityProps> = ({r}) => {
  const C = usePalette();
  const p = r.e.p as WindowP;
  const w = r.get('w', 820);
  const h = r.get('h', 640);
  const seal = r.get('seal', 1);
  const lock = r.get('lock', 1);
  const barOn = clamp01(r.get('bar', 1));
  const sealOn = clamp01(r.get('sealOn', 1));
  const sealDy = r.get('sealDy', 0);
  const lockOn = clamp01(r.get('lockOn', 1));
  const lockDy = r.get('lockDy', 0);
  const lockK = r.get('lockK', 1); // opt-in: padlock scaled about its own centre (default 1: unchanged)
  const lockDx = r.get('lockDx', 0); // opt-in: padlock shifted right by lockDx px (default 0: unchanged)
  const tb = p.titleH ?? 56;
  const rr = p.r ?? 24;
  const x0 = -w / 2;
  const y0 = -h / 2;
  const cy = y0 + tb / 2;
  const bar = `M${x0},${y0 + tb} V${y0 + rr} A${rr},${rr} 0 0 1 ${x0 + rr},${y0} H${x0 + w - rr} A${rr},${rr} 0 0 1 ${x0 + w},${y0 + rr} V${y0 + tb} Z`;
  const k = p.sealK ?? 1;
  const pw = 46 * k + (p.sealW - 46 * k) * seal;
  const sx1 = x0 + w - 12;
  const sx0 = sx1 - pw;
  const px = sx0 - 30;
  const textOp = clamp01((seal - 0.55) / 0.45);
  return (
    <>
      <path d={roundRect(x0, y0, w, h, rr)} fill="none" stroke={C.deep} strokeWidth={6} />
      {winLayer(
        barOn,
        -40 * (1 - barOn),
        <>
          <Hard off={6} render={(sh) => <path d={bar} fill={sh ? C.ink : C.light} stroke={C.ink} strokeWidth={4} strokeLinejoin="round" />} />
          {[24, 46, 68].map((dx) => (
            <circle key={dx} cx={x0 + dx} cy={cy} r={6} fill={C.ink} />
          ))}
        </>,
      )}
      {/* padlock: ink body, deep-cyan shackle (closed when lock = 1) */}
      {((node: React.ReactNode) => (lockDx !== 0 && node ? <g transform={`translate(${lockDx} 0)`}>{node}</g> : node))(winLayer(
        lockOn,
        lockDy,
        ((node: React.ReactNode) =>
          lockK !== 1 ? <g transform={`translate(${px} ${cy}) scale(${lockK}) translate(${-px} ${-cy})`}>{node}</g> : node)(
          <>
            <path
              d={`M${px - 8},${cy - 3} V${cy - 10 - 4 * (1 - lock)} A8,8 0 0 1 ${px + 8},${cy - 10 - 4 * (1 - lock)} V${cy - 3 - 6 * (1 - lock)}`}
              fill="none"
              stroke={C.deep}
              strokeWidth={4}
              strokeLinecap="round"
            />
            <rect x={px - 13} y={cy - 4} width={26} height={20} rx={4} fill={C.ink} />
          </>,
        ),
      ))}
      {/* seal: cyan disc with the firm's building, opens into the pill « ✓ Cabinet » */}
      {winLayer(
        sealOn,
        sealDy,
        <>
          <Hard off={4} render={(sh) => <rect x={sx0} y={cy - 22 * k} width={pw} height={44 * k} rx={22 * k} fill={sh ? C.ink : C.cyan} stroke={C.ink} strokeWidth={3} />} />
          <g transform={`translate(${sx0 + 23 * k} ${cy})`}>
            <Icon name="building" s={24 * k} color={C.ink} />
          </g>
          {textOp > 0 ? (
            <g opacity={textOp}>
              <g transform={`translate(${sx0 + 54 * k} ${cy})`}>
                <Icon name="check" s={18 * k} color={C.ink} sw={3.4} />
              </g>
              <Txt x={sx0 + 68 * k} y={cy} size={26 * k} weight={700}>
                {p.sealText}
              </Txt>
            </g>
          ) : null}
        </>,
      )}
    </>
  );
};

// ---------- card: shared body of the compact document, the date chip and the source tag ----------
// One drawing for the three looks, so that a document can shrink INTO its source tag (same frames, no fade) and the
// tag entity of the page can take over on the frame of arrival with a pixel-identical picture.
type CardSpec = {
  w: number;
  h: number;
  r: number;
  fold: number;
  shadow: number;
  fill: string;
  stroke: string;
  sw?: number;
  /** cyan disc with the ink pictogram (document identity) */
  disc?: {x: number; r: number; icon: string; scale?: number};
  /** optional second disc right after the first (tag icon2) */
  disc2?: {x: number; r: number; icon: string; scale?: number};
  /** bare pictogram (calendar of the date chip) */
  glyph?: {x: number; icon: string; s: number; color: string; scale?: number};
  texts: {text: string; x: number; size: number; opacity: number; weight?: number}[];
};
const Card: React.FC<{c: CardSpec; C: Palette}> = ({c, C}) => {
  const x0 = -c.w / 2;
  const y0 = -c.h / 2;
  const f = c.fold;
  const body = f > 0.5 ? foldedRect(x0, y0, c.w, c.h, c.r, f) : roundRect(x0, y0, c.w, c.h, c.r);
  return (
    <>
      <Hard off={c.shadow} render={(sh) => <path d={body} fill={sh ? C.ink : c.fill} stroke={c.stroke} strokeWidth={c.sw ?? 3} strokeLinejoin="round" />} />
      {f > 0.5 ? (
        <path d={`M${x0 + c.w - f},${y0} V${y0 + f} H${x0 + c.w} Z`} fill={C.grey} stroke={c.stroke} strokeWidth={Math.min(3, c.sw ?? 3)} strokeLinejoin="round" />
      ) : null}
      {c.disc ? (
        <g transform={`translate(${c.disc.x} 0) scale(${c.disc.scale ?? 1})`}>
          <Bullet icon={c.disc.icon} r={c.disc.r} />
        </g>
      ) : null}
      {c.disc2 ? (
        <g transform={`translate(${c.disc2.x} 0) scale(${c.disc2.scale ?? 1})`}>
          <Bullet icon={c.disc2.icon} r={c.disc2.r} />
        </g>
      ) : null}
      {c.glyph ? (
        <g transform={`translate(${c.glyph.x} 0) scale(${c.glyph.scale ?? 1})`}>
          <Icon name={c.glyph.icon} s={c.glyph.s} color={c.glyph.color} sw={2.8} />
        </g>
      ) : null}
      {c.texts.map((t, i) =>
        t.opacity > 0.01 ? (
          <Txt key={i} x={t.x} y={0} size={t.size} weight={t.weight ?? 600} opacity={t.opacity < 0.99 ? t.opacity : undefined}>
            {t.text}
          </Txt>
        ) : null,
      )}
    </>
  );
};

/** Source tag of a line (document pictogram + date, folded corner) and its date-chip state (calendar + date). */
// Opt-in icon2 (absent = today's tag): a second pictogram disc right after the first (tagged state only), the date
// shifted right by one disc (2 discR + 4 px) : give w accordingly.
type TagGeom = {w: number; h: number; date: string; size: number; icon2?: string};
const TAG = GEOM.TAG;
const tagSpec = (g: TagGeom, C: Palette, icon: string, tagged: boolean, lit: number, iconScale = 1): CardSpec => {
  const x0 = -g.w / 2;
  const two = tagged && !!g.icon2;
  const shift = two ? 2 * TAG.discR + 4 : 0;
  return {
    w: g.w,
    h: g.h,
    r: TAG.r,
    fold: tagged ? TAG.fold : 0,
    shadow: TAG.shadow,
    fill: mixHex(C.paper, C.light, lit),
    stroke: mixHex(C.ink, C.deep, lit),
    disc: tagged ? {x: x0 + TAG.iconX, r: TAG.discR, icon, scale: iconScale} : undefined,
    disc2: two ? {x: x0 + TAG.iconX + shift, r: TAG.discR, icon: g.icon2 as string, scale: iconScale} : undefined,
    glyph: tagged ? undefined : {x: x0 + TAG.iconX, icon: 'cal', s: 24, color: C.deep, scale: iconScale},
    texts: [{text: g.date, x: x0 + TAG.textX + shift, size: g.size, opacity: 1}],
  };
};

// ---------- doc: client document (full card -> compact card -> pictogram disc landing on its source tag) ----------
// Compact card (S11-S12): no title (the row label and the tag already say it), a blank date strip on the left (the
// date chip, a `label` entity, sits there until « date. » peels it off along the wire) and the pictogram disc on the
// right. Track `tag` (S13): the card shrinks INTO its disc, which lands on the tag's calendar and becomes its pictogram.
// Opt-in variant (absent = today's 160 x 200 card, pixel for pixel): fw x fh (full card size, the `compact` track
// contracts from it), fts (title size of the full card), fdate (the date written out in deep cyan on the bottom strip,
// in place of the second grey rule); track `read` (0 -> 1: the grey rules turn deep cyan, left to right, one after
// the other: the AI reads the document).
type DocP = {title: string; icon: string; date: string; cw: number; ch: number; titleSize: number; tag: TagGeom;
  fw?: number; fh?: number; fts?: number; fdate?: boolean; fdateSize?: number};
export const DOC_DISC = GEOM.DOC_DISC;
const Doc: React.FC<EntityProps> = ({r}) => {
  const C = usePalette();
  const p = r.e.p as DocP;
  const c = clamp01(r.get('compact', 0));
  const t = clamp01(r.get('tag', 0));
  const txt = clamp01(r.get('txt', 1));
  const sh = r.get('sh', 5);
  const read = clamp01(r.get('read', 0));
  const lit = clamp01(r.get('lit', 0)); // opt-in: card fill paper -> light cyan (the source « lights up »)
  const d = 2 * TAG.discR;
  const cw = lerp(p.cw, d, t);
  const chh = lerp(p.ch, d, t);
  const w = lerp(p.fw ?? 160, cw, c);
  const h = lerp(p.fh ?? 200, chh, c);
  const x0 = -w / 2;
  const y0 = -h / 2;
  const spec: CardSpec = {
    w,
    h,
    r: lerp(10, lerp(12, TAG.discR, t), c),
    fold: lerp(20, lerp(16, 0, t), c),
    shadow: lerp(sh, 0, t),
    fill: lit > 0 ? mixHex(C.paper, C.light, lit) : C.paper,
    stroke: C.ink,
    sw: lerp(4, 3, t),
    disc: c > 0 ? {x: lerp(p.cw / 2 - DOC_DISC.inset, 0, t) * c, r: lerp(DOC_DISC.r, TAG.discR, t), icon: p.icon} : undefined,
    texts: [],
  };
  // grey rules of the full card [x from, x to, y]; with fdate, the date replaces the second one
  const rules: [number, number, number][] = [[x0 + 16, x0 + w - 30, y0 + h - 56]];
  if (!p.fdate) rules.push([x0 + 16, x0 + w - 60, y0 + h - 34]);
  return (
    <>
      <Card c={spec} C={C} />
      {c < 1 ? (
        // full card content (vertical layout), cross-faded while the card contracts
        <g opacity={(1 - c) * txt}>
          <g transform={`translate(${x0 + 36} ${y0 + 40})`}>
            <Bullet icon={p.icon} r={22} />
          </g>
          <Txt x={x0 + 16} y={y0 + 96} size={p.fts ?? 26}>
            {p.title}
          </Txt>
          <path d={rules.map(([a, b, y]) => `M${a},${y} H${b}`).join(' ')} stroke={C.grey} strokeWidth={6} strokeLinecap="round" />
          {read > 0.001
            ? rules.map(([a, b, y], i) => {
                const k = clamp01(read * rules.length - i);
                return k > 0.001 ? <path key={i} d={`M${a},${y} H${a + (b - a) * k}`} stroke={C.deep} strokeWidth={6} strokeLinecap="round" /> : null;
              })
            : null}
          {p.fdate ? (
            <Txt x={x0 + 16} y={y0 + h - 34} size={p.fdateSize ?? 24} weight={600} color={C.deep}>
              {p.date}
            </Txt>
          ) : null}
        </g>
      ) : null}
    </>
  );
};

// ---------- fiche: the one-page brief (card, header « Brief », tabs) ----------
type FicheP = {w: number; h: number; title: string; headerH: number; tabs: number[]; tabX: number; sheen?: SheenRef};
const Fiche: React.FC<EntityProps> = ({r, scene}) => {
  const C = usePalette();
  const p = r.e.p as FicheP;
  const {w, h} = p;
  return (
    <>
      <Hard off={8} render={(sh) => <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={16} fill={sh ? C.ink : C.paper} stroke={C.ink} strokeWidth={4} />} />
      <SheenUnder sheen={p.sheen} scene={scene} clipD={roundRect(-w / 2 + 2, -h / 2 + 2, w - 4, h - 4, 14)} uid={r.e.id} />
      {r.get('lite', 0) < 0.999 ? (
        <Txt x={w / 2 - 26} y={-h / 2 + p.headerH / 2 + 2} size={36} weight={800} anchor="end" opacity={r.get('lite', 0) > 0.001 ? 1 - clamp01(r.get('lite', 0)) : undefined}>
          {p.title}
        </Txt>
      ) : null}
      {r.get('lite', 0) > 0.001 ? (
        // opt-in `lite` (absent / 0 = today's page): the title becomes a plain ink bar
        <rect x={w / 2 - 26 - 96} y={-h / 2 + p.headerH / 2 - 11} width={96} height={22} rx={11} fill={C.ink} opacity={r.get('lite', 0) < 0.999 ? clamp01(r.get('lite', 0)) : undefined} />
      ) : null}
      <line x1={-w / 2 + 20} x2={w / 2 - 20} y1={-h / 2 + p.headerH} y2={-h / 2 + p.headerH} stroke={C.rule} strokeWidth={3} />
      {/* empty tabs of the order (S10): each disappears when its bullet lands (track tab<i>) */}
      {p.tabs.map((y, i) => {
        const o = clamp01(r.get(`tab${i}`, 1));
        return o > 0.01 ? (
          <rect key={y} x={p.tabX - 14} y={y - 14} width={28} height={28} rx={6} fill={C.cyan} stroke={C.ink} strokeWidth={3} opacity={o < 0.99 ? o : undefined} />
        ) : null;
      })}
    </>
  );
};

// ---------- sheen: white reflection sweeping across the page (« fluide ») ----------
const Sheen: React.FC<EntityProps> = ({r}) => {
  const p = r.e.p as {w: number; h: number; under?: boolean};
  const s = r.get('p', 0);
  // `under`: this entity only carries the progress; page, rows and pill draw the band under their texts (SheenUnder).
  if (p.under || s <= 0 || s >= 1) return null;
  const id = `${r.e.id}-clip`;
  const slant = p.h * 0.45;
  // The band is already ON the page at the first frame (top-left corner) and leaves it by the bottom-right.
  const cx = -p.w / 2 + 10 + (p.w + slant + 60) * s;
  return (
    <>
      <defs>
        <clipPath id={id}>
          <rect x={-p.w / 2 + 2} y={-p.h / 2 + 2} width={p.w - 4} height={p.h - 4} rx={14} />
        </clipPath>
      </defs>
      <g clipPath={`url(#${id})`}>
        <polygon
          points={`${cx - 34},${-p.h / 2 - 4} ${cx + 46},${-p.h / 2 - 4} ${cx + 46 - slant},${p.h / 2 + 4} ${cx - 34 - slant},${p.h / 2 + 4}`}
          fill="#FFFFFF"
          opacity={0.62}
        />
        <polygon
          points={`${cx + 62},${-p.h / 2 - 4} ${cx + 76},${-p.h / 2 - 4} ${cx + 76 - slant},${p.h / 2 + 4} ${cx + 62 - slant},${p.h / 2 + 4}`}
          fill="#FFFFFF"
          opacity={0.62}
        />
      </g>
    </>
  );
};

// ---------- line: one row of the brief (bullet, key, value; typewriter, red, crack, strike, fall) ----------
type LineP = {key: string; value: string; icon: string; x0: number; x1: number; h: number; hStrip: number; ty: number;
  bulletX: number; textX: number; valueX: number; valueW: number; crackX: number; tilt: number; drop: number;
  gap?: number; fallPx?: number; strikeW?: number; sheen?: SheenRef; keyW?: number};
/**
 * Tracks: chars (typewriter), grow (row height: text strip -> full row when its source arrives), slotFill (opacity
 * of the beige capsule: rows lighten once written), flash (bullet pulse when the AI beam reaches it), pulse (bullet
 * x1.6 blink: « nothing holds this line »), bulletOn (0: no bullet yet), alarm (hollow bullet outline -> red), red
 * (text + capsule outline), crack (the row SPLITS between key and value: a zigzag gap opens at crackX and the right
 * piece, the value, drops `drop` px and tilts `tilt` deg about the gap's top edge; pipeline.story.line_crack_point),
 * strike (ink line drawn across the value, right to left), fall (the struck value detaches and falls off the card,
 * fading at the end), dimValue (legacy: struck value at 60 % ink).
 */
const Line: React.FC<EntityProps> = ({r, scene}) => {
  const C = usePalette();
  const p = r.e.p as LineP;
  const chars = Math.floor(r.get('chars', 999) + 1e-6);
  const red = clamp01(r.get('red', 0));
  const crack = clamp01(r.get('crack', 0));
  const strike = clamp01(r.get('strike', 0));
  const dimValue = clamp01(r.get('dimValue', 0));
  const grow = clamp01(r.get('grow', 1));
  const fill = clamp01(r.get('slotFill', 1));
  const fall = clamp01(r.get('fall', 0));
  const flash = r.get('flash', 0);
  const pulse = r.get('pulse', 0);
  const bulletOn = r.get('bulletOn', 1) >= 0.5;
  const alarm = clamp01(r.get('alarm', 0));
  const key = p.key.slice(0, Math.max(0, Math.min(p.key.length, chars)));
  const value = p.value.slice(0, Math.max(0, chars - p.key.length));
  const col = mixHex(C.ink, C.red, red);
  const valCol = mixHex(col, C.paper, 0.4 * dimValue);
  const top = -p.h / 2;
  const sh = lerp(p.hStrip, p.h, grow);
  const slotD = roundRect(p.x0, top, p.x1 - p.x0, sh, 12);
  const slot = (
    <path d={slotD} fill={C.slot} fillOpacity={fill < 0.999 ? fill : undefined} stroke={C.red} strokeWidth={red > 0 ? 4 : 0} strokeOpacity={red} />
  );
  // Opt-in `lite` (absent / 0 = today's row): key and value cross-fade into plain bars (ink, deep cyan), for a
  // reduced page (V01 S15-S17) ; bullet, capsule and ticks stay. keyW = measured key width (else 17 px a character).
  const lite = clamp01(r.get('lite', 0));
  const keyBar =
    lite > 0.001 && key.length > 0 ? (
      <rect x={p.textX} y={p.ty - 10} width={(p.keyW ?? 17 * p.key.length) * (key.length / Math.max(1, p.key.length))} height={20} rx={10} fill={col} opacity={lite < 0.999 ? lite : undefined} />
    ) : null;
  const keyT = (
    <>
      {lite < 0.999 ? (
        <Txt x={p.textX} y={p.ty} size={32} color={col} opacity={lite > 0.001 ? 1 - lite : undefined}>
          {key}
        </Txt>
      ) : null}
      {keyBar}
    </>
  );
  const sx0 = p.valueX + 8;
  const sx1 = p.valueX - p.valueW - 8;
  const vcx = p.valueX - p.valueW / 2;
  const fallPx = p.fallPx ?? 240;
  const valOp = 1 - clamp01((fall - 0.6) / 0.4);
  const valT =
    valOp > 0.001 ? (
      <g transform={fall > 0 ? `translate(0 ${fall * fallPx}) rotate(${16 * fall} ${vcx} ${p.ty})` : undefined} opacity={valOp < 0.999 ? valOp : undefined}>
        {lite < 0.999 ? (
          <Txt x={p.valueX} y={p.ty} size={32} color={valCol} anchor="end" opacity={lite > 0.001 ? 1 - lite : undefined}>
            {value}
          </Txt>
        ) : null}
        {lite > 0.001 && value.length > 0 ? (
          <rect x={p.valueX - p.valueW * (value.length / Math.max(1, p.value.length))} y={p.ty - 10} width={p.valueW * (value.length / Math.max(1, p.value.length))} height={20} rx={10} fill={mixHex(C.deep, C.red, red)} opacity={lite < 0.999 ? lite : undefined} />
        ) : null}
        {strike > 0 ? (
          <path d={`M${sx0},${p.ty} H${sx1}`} stroke={C.ink} strokeWidth={p.strikeW ?? 7} strokeLinecap="round" strokeDasharray={drawDash(sx0 - sx1, strike)} />
        ) : null}
      </g>
    ) : null;
  const bullet = bulletOn ? (
    <g transform={`translate(${p.bulletX} ${p.ty}) scale(${(1 + 0.35 * flash) * (1 + 0.6 * pulse)})`}>
      <Bullet icon={p.icon} r={22} alarm={alarm} />
    </g>
  ) : null;
  if (crack <= 0.001) {
    return (
      <>
        {slot}
        <SheenUnder sheen={p.sheen} scene={scene} clipD={slotD} uid={r.e.id} />
        {keyT}
        {valT}
        {bullet}
      </>
    );
  }
  // The row splits between key and value: zigzag cut at crackX, the gap opens to `gap` px (the page shows through),
  // the right piece (capsule end + value) hangs from the gap's top edge. Both cut edges are inked.
  const cx = p.crackX;
  const g = ((p.gap ?? 12) / 2) * crack;
  const n = 6;
  const zz: Vec2[] = [[cx, top - 2]];
  for (let i = 1; i < n; i++) zz.push([cx + (i % 2 ? 7 : -7), top + (sh * i) / n]);
  zz.push([cx, top + sh + 2]);
  const zl = zz.map(([x, y]) => `${x - g},${y}`).join(' ');
  const zr = zz.map(([x, y]) => `${x + g},${y}`).join(' ');
  const idL = `${r.e.id}-cl`;
  const idR = `${r.e.id}-cr`;
  const W = 2000;
  const edge = mixHex(C.ink, C.red, red);
  return (
    <>
      <defs>
        <clipPath id={idL}>
          <polygon points={`${-W},${top - 40} ${zl} ${-W},${top + sh + 40}`} />
        </clipPath>
        <clipPath id={idR}>
          <polygon points={`${W},${top - 40} ${zr} ${W},${top + sh + 40}`} />
        </clipPath>
      </defs>
      <g clipPath={`url(#${idL})`}>{slot}</g>
      <polyline points={zl} fill="none" stroke={edge} strokeWidth={4} strokeLinejoin="round" opacity={crack} />
      <g transform={`translate(0 ${p.drop * crack}) rotate(${p.tilt * crack} ${cx + (p.gap ?? 12) / 2} ${top})`}>
        <g clipPath={`url(#${idR})`}>{slot}</g>
        <polyline points={zr} fill="none" stroke={edge} strokeWidth={4} strokeLinejoin="round" opacity={crack} />
        {valT}
      </g>
      {keyT}
      {bullet}
    </>
  );
};

// ---------- tick: AI tick (grey, ink ~50 %) / advisor tick (deep cyan), single stroke, drawn on ----------
// `size` (px, default 31): width of the tick; the stroke width stays `sw` px whatever the size. `dots` (optional):
// dotted stroke. Knock-off (S14) = the entity's own pos / rot / opacity tracks.
// Variante `variant: 'ai'` : coche fine en pointillés dans un carré tireté (côté GEOM.TICK.aiBox x size) ; l'IA et le
// conseiller se distinguent par la forme, pas seulement par la couleur. `draw` trace le carré puis la coche.
const TICK_PTS = GEOM.TICK.pts as Vec2[];
const tickPath = (size: number) => {
  const k = size / GEOM.TICK.size;
  const pts = TICK_PTS.map(([x, y]) => [x * k, y * k] as Vec2);
  const len = Math.hypot(pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]) + Math.hypot(pts[2][0] - pts[1][0], pts[2][1] - pts[1][1]);
  return {len, d: `M${pts[0].join(',')} L${pts[1].join(',')} L${pts[2].join(',')}`};
};
type TickP = {color: string; sw: number; dots?: number; size?: number; variant?: 'ai'; boxSw?: number; thin?: number; boxFill?: string};
const Tick: React.FC<EntityProps> = ({r}) => {
  const p = r.e.p as TickP;
  const d = r.get('draw', 1);
  if (d <= 0) return null;
  if (p.variant === 'ai') return <AiTick p={p} d={d} />;
  const {len, d: path} = tickPath(p.size ?? GEOM.TICK.size);
  const dash = p.dots ? drawDash(len, d, [0.01, p.dots]) : drawDash(len, d);
  return <path d={path} fill="none" stroke={p.color} strokeWidth={p.sw} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={dash} />;
};
const AiTick: React.FC<{p: TickP; d: number}> = ({p, d}) => {
  const size = p.size ?? GEOM.TICK.size;
  const B = GEOM.TICK.aiBox * size;
  const rr = B * 0.14;
  const box = clamp01(d / 0.5);
  const tk = clamp01((d - 0.45) / 0.55);
  // coche intérieure à 78 %, en points ronds posés un à un (les 3 sommets compris : la forme reste lisible) ;
  // thin = diamètre des points (défaut 0,7 x sw), dots = pas visé entre deux points (défaut 1,5 x thin)
  const thin = p.thin ?? Math.max(4, p.sw * 0.7);
  const k = (size * 0.78) / GEOM.TICK.size;
  const pts = TICK_PTS.map(([x, y]) => [x * k + 0.5, y * k + 0.5] as Vec2);
  const dots: {x: number; y: number; at: number}[] = [];
  let acc = 0;
  for (let i = 1; i < pts.length; i++) {
    const L = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
    const n = Math.max(1, Math.round(L / (p.dots ?? thin * 1.5)));
    for (let j = i === 1 ? 0 : 1; j <= n; j++) {
      const t = j / n;
      dots.push({x: lerp(pts[i - 1][0], pts[i][0], t), y: lerp(pts[i - 1][1], pts[i][1], t), at: acc + L * t});
    }
    acc += L;
  }
  const boxLen = roundRectLength(B, B, rr);
  const boxSw = p.boxSw ?? Math.max(2.5, p.sw * 0.4);
  return (
    <>
      {box > 0 ? (
        <path d={roundRect(-B / 2, -B / 2, B, B, rr)} fill={p.boxFill ?? 'none'} stroke={p.color} strokeWidth={boxSw} strokeLinecap="round" strokeDasharray={drawDash(boxLen, box, [B * 0.16, B * 0.11])} />
      ) : null}
      {tk > 0 ? dots.filter((q) => q.at <= tk * acc + 1e-6).map((q, i) => <circle key={i} cx={q.x} cy={q.y} r={thin / 2} fill={p.color} />) : null}
    </>
  );
};

// ---------- label: date chip (calendar + date) -> source tag (document pictogram + date, folded corner) ----------
const Label: React.FC<EntityProps> = ({r}) => {
  const C = usePalette();
  const p = r.e.p as {icon: string; tag: TagGeom};
  const tagged = r.get('tagged', 0) >= 0.5;
  const pop = clamp01(r.get('pop', 1));
  const lit = clamp01(r.get('lit', 0));
  const flash = r.get('flash', 0);
  const s = tagged ? 1 + 0.35 * flash : 0.4 + 0.6 * pop;
  // Opt-in `lite` (absent / 0 = today's tag): the written date cross-fades into a plain deep-cyan bar.
  const lite = clamp01(r.get('lite', 0));
  const spec = tagSpec(p.tag, C, p.icon, tagged, lit, s);
  if (lite <= 0.001) return <Card c={spec} C={C} />;
  const t0 = spec.texts[0];
  const bx = t0.x;
  const bw = Math.max(10, p.tag.w / 2 - 12 - bx);
  return (
    <>
      <Card c={{...spec, texts: spec.texts.map((t) => ({...t, opacity: t.opacity * (1 - lite)}))}} C={C} />
      <rect x={bx} y={-8} width={bw} height={16} rx={8} fill={C.deep} opacity={lite < 0.999 ? lite : undefined} />
    </>
  );
};

// ---------- case: dashed source box traced by the advisor's pen ----------
const Case: React.FC<EntityProps> = ({r}) => {
  const C = usePalette();
  const p = r.e.p as {w: number; h: number};
  const d = r.get('draw', 1);
  if (d <= 0) return null;
  const len = roundRectLength(p.w, p.h, 14);
  return (
    <path d={roundRect(-p.w / 2, -p.h / 2, p.w, p.h, 14)} fill="none" stroke={C.deep} strokeWidth={4} strokeDasharray={drawDash(len, d, [14, 10])} />
  );
};

// ---------- wire: proof thread (solid) / AI beam (dotted) between two anchors, optionally through a via point ----------
type WireP = {a?: Anchor; b?: Anchor; color: string; sw: number; dash?: number[]; dashAlt?: number[]; dots?: boolean;
  tension?: number; endDot?: boolean};
const Wire: React.FC<EntityProps> = ({r, scene}) => {
  const p = r.e.p as WireP;
  const draw = clamp01(r.get('draw', 1));
  const from = clamp01(r.get('from', 0));
  if (draw <= from + 0.001) return null;
  // aAt / bAt (optional tracks): the anchor point slides inside its entity (ex. from the value to the date chip).
  const A = p.a ? scene.anchor({id: p.a.id, at: r.get<number[]>('aAt', p.a.at) as Vec2}) : (r.get<number[]>('pa', [0, 0]) as Vec2);
  const B = p.b ? scene.anchor({id: p.b.id, at: r.get<number[]>('bAt', p.b.at) as Vec2}) : (r.get<number[]>('pb', [0, 0]) as Vec2);
  const viaV = r.get<number[]>('via', []);
  const via = viaV.length === 2 ? (viaV as Vec2) : null;
  const color = r.get('color', p.color);
  const path = wirePath(A, B, r.get('sag', 0), p.tension ?? 0.45, via);
  const len = path.len;
  // « dashed » >= 0.5: a solid thread breaks into dashes (proof that found nothing).
  const pattern = r.get('dashed', 0) >= 0.5 && p.dashAlt ? p.dashAlt : p.dash;
  const shown = (draw - from) * len;
  let dash: string | undefined;
  if (pattern) {
    const parts: number[] = [];
    if (from > 0) parts.push(0, from * len);
    // trailing gap = whole path: a partly drawn dotted beam must not repeat further along the path
    const pat = drawDash(len, draw - from, pattern) ?? '';
    parts.push(...pat.split(' ').map(Number));
    dash = parts.join(' ');
  } else {
    dash = from > 0 || draw < 0.999 ? `0 ${from * len} ${shown} ${len + 10}` : undefined;
  }
  const end = path.pointAt(draw);
  const start = path.pointAt(from);
  return (
    <>
      <path d={path.d} fill="none" stroke={color} strokeWidth={p.sw} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={dash} />
      {p.dots ? (
        <>
          <circle cx={start[0]} cy={start[1]} r={p.sw * 1.3} fill={color} />
          {p.endDot !== false ? <circle cx={end[0]} cy={end[1]} r={p.sw * 1.3} fill={color} /> : null}
        </>
      ) : null}
    </>
  );
};

// ---------- qmark: big ink « ? » (born from the value without a source, under the advisor's pen) ----------
const QMark: React.FC<EntityProps> = ({r}) => {
  const gs = r.get('gs', 100);
  return (
    <Txt x={0} y={0} size={gs} weight={800} anchor="middle">
      ?
    </Txt>
  );
};

// ---------- bubble: the advisor's flat speech bubble « ? » + mini copy of the client <-> the « ? » sticker ----------
// q: size of the « ? » (ExtraBold), qx its x; px / ps: x and height (px) of the client's mini figurine; gs: its stroke.
type BubbleShape = {w: number; h: number; r: number; q: number; qx: number; px: number; ps: number; sw: number; shadow: number; gs?: number};
type BubbleP = {big: BubbleShape; small: BubbleShape; tail: Vec2; tailBase: [number, number]};
/** Tracks: s (0 speech bubble -> 1 sticker: smaller pill, cyan, tail retracted), q (own « ? » shown), pulse. */
const Bubble: React.FC<EntityProps> = ({r}) => {
  const C = usePalette();
  const p = r.e.p as BubbleP;
  const s = clamp01(r.get('s', 0));
  const q = r.get('q', 1);
  const pulse = r.get('pulse', 0);
  const B = p.big;
  const S = p.small;
  const w = lerp(B.w, S.w, s);
  const h = lerp(B.h, S.h, s);
  const rr = lerp(B.r, S.r, s);
  const x = -w / 2;
  const y = -h / 2;
  // tail: from the bottom edge (base, left part of the body) to the tip on the advisor's head; retracts as s -> 1
  const k = w / B.w;
  const bx0 = p.tailBase[0] * k;
  const bx1 = p.tailBase[1] * k;
  const bm = (bx0 + bx1) / 2;
  const ts = clamp01(1 - 1.6 * s);
  const tip: Vec2 = [lerp(bm, p.tail[0], ts), lerp(y + h, p.tail[1], ts)];
  const tb0 = lerp(bm, bx0, ts);
  const tb1 = lerp(bm, bx1, ts);
  const d =
    `M${x + rr},${y} H${x + w - rr} A${rr},${rr} 0 0 1 ${x + w},${y + rr} V${y + h - rr} A${rr},${rr} 0 0 1 ${x + w - rr},${y + h} ` +
    `H${tb1} L${tip[0]},${tip[1]} L${tb0},${y + h} H${x + rr} A${rr},${rr} 0 0 1 ${x},${y + h - rr} V${y + rr} A${rr},${rr} 0 0 1 ${x + rr},${y} Z`;
  const fill = mixHex(C.paper, C.cyan, s);
  const sc = 1 + 0.25 * pulse;
  return (
    <g transform={`scale(${sc})`}>
      <Hard off={lerp(B.shadow, S.shadow, s)} render={(sh) => <path d={d} fill={sh ? C.ink : fill} stroke={C.ink} strokeWidth={lerp(B.sw, S.sw, s)} strokeLinejoin="round" />} />
      {q >= 0.5 ? (
        <Txt x={lerp(B.qx, S.qx, s)} y={0} size={lerp(B.q, S.q, s)} weight={800} anchor="middle">
          ?
        </Txt>
      ) : null}
      {r.get('glyph', 1) >= 0.5 ? (
        <g transform={`translate(${lerp(B.px, S.px, s)} 0)`}>
          <ClientGlyph h={lerp(B.ps, S.ps, s)} sw={lerp(B.gs ?? 4, S.gs ?? 3, s)} />
        </g>
      ) : null}
    </g>
  );
};

// ---------- pen: the advisor's tool. Origin = his grip (where the arm holds it), tip at (len, 0) ----------
const Pen: React.FC<EntityProps> = ({r}) => {
  const C = usePalette();
  const L = (r.e.p as {len?: number}).len ?? GEOM.PEN.len;
  const {r: pr, tip} = GEOM.PEN;
  const body = `M0,${-pr} H${L - tip} V${pr} H0 A${pr},${pr} 0 0 1 0,${-pr} Z`;
  return (
    <Hard
      off={worldShadow(r.world, 4)}
      render={(sh) => (
        <>
          <path d={body} fill={C.ink} stroke={C.ink} strokeWidth={3} />
          <path d={`M${L - tip - 1},${-(pr - 1)} L${L - 1},0 L${L - tip - 1},${pr - 1} Z`} fill={sh ? C.ink : C.cyan} stroke={C.ink} strokeWidth={3} strokeLinejoin="round" />
          {sh ? null : <rect x={L - tip - 12} y={-pr} width={8} height={2 * pr} fill={C.cyan} />}
        </>
      )}
    />
  );
};

// ---------- limb: the advisor's arm, a thick ink stroke from his shoulder to the grip of the tool he holds ----------
type LimbP = {a: Anchor; b: Anchor; sw?: number; pivot?: Vec2; pivotTrack?: string};
/** Tracks: bend (0 straight .. 1 through the elbow), elbow (world point). */
const rotateAbout = (pt: Vec2, deg: number, c: Vec2): Vec2 => {
  const t = (deg * Math.PI) / 180;
  const dx = pt[0] - c[0];
  const dy = pt[1] - c[1];
  return [c[0] + dx * Math.cos(t) - dy * Math.sin(t), c[1] + dx * Math.sin(t) + dy * Math.cos(t)];
};
const Limb: React.FC<EntityProps> = ({r, scene}) => {
  const C = usePalette();
  const p = r.e.p as LimbP;
  const fig = scene.resolve(p.a.id);
  const lean = p.pivotTrack ? fig.get(p.pivotTrack, 0) : 0;
  const A = apply(fig.world, lean ? rotateAbout(p.a.at, lean, p.pivot ?? [0, 0]) : p.a.at);
  const B = scene.anchor(p.b);
  const sw = p.sw ?? GEOM.FIGURE.arm.sw;
  // bend (0..1) + elbow (world point): the arm goes shoulder -> elbow -> grip, to reach round what it must not cover.
  const bend = clamp01(r.get('bend', 0));
  const el = r.get<number[]>('elbow', [0, 0]);
  const E: Vec2 = [lerp((A[0] + B[0]) / 2, el[0], bend), lerp((A[1] + B[1]) / 2, el[1], bend)];
  const line = () =>
    bend > 0.001 ? (
      <polyline points={`${A[0]},${A[1]} ${E[0]},${E[1]} ${B[0]},${B[1]}`} fill="none" stroke={C.ink} strokeWidth={sw} strokeLinecap="round" strokeLinejoin="round" />
    ) : (
      <line x1={A[0]} y1={A[1]} x2={B[0]} y2={B[1]} stroke={C.ink} strokeWidth={sw} strokeLinecap="round" />
    );
  // Opt-in track `rim` (absent / 0 = today's arm): a paper outline of 3 px round the arm, so that an arm crossing the
  // ink bust stays readable (drawn over the plain arm at opacity rim).
  const rim = clamp01(r.get('rim', 0));
  if (rim <= 0.001) return <Hard off={5} render={line} />;
  const pts = bend > 0.001 ? `${A[0]},${A[1]} ${E[0]},${E[1]} ${B[0]},${B[1]}` : `${A[0]},${A[1]} ${B[0]},${B[1]}`;
  return (
    <>
      <Hard off={5} render={line} />
      <g opacity={rim < 0.999 ? rim : undefined}>
        <polyline points={pts} fill="none" stroke={C.paper} strokeWidth={sw + 6} strokeLinecap="round" strokeLinejoin="round" />
        <polyline points={pts} fill="none" stroke={C.ink} strokeWidth={sw} strokeLinecap="round" strokeLinejoin="round" />
      </g>
    </>
  );
};

// ---------- stamp: « VALIDÉ », ink on paper (no fill: the page shows through) ----------
/** Track `handle` (0..1): the ink handle on top, held by the advisor's arm during the slam. Grip at STAMP_GRIP.
 *  Opt-in `sub` (absent = today's one-line stamp, same pixels): a second line under the text, a small « ? » in a
 *  deep circle then `sub` (SemiBold, GEOM.STAMP_SUB), the first line lifted by `lift`; `subW` = measured width of
 *  `sub` (Kit.stamp; else 0.5 em a character). Track `subOn` (0..1, default 1): opacity of the second line. */
export const STAMP_HANDLE = GEOM.STAMP_HANDLE;
const STAMP_SUB = GEOM.STAMP_SUB;
const Stamp: React.FC<EntityProps> = ({r}) => {
  const C = usePalette();
  const p = r.e.p as {text: string; w: number; h: number; size?: number; sub?: string; subW?: number};
  const handle = clamp01(r.get('handle', 0));
  const Q = STAMP_SUB;
  const sub = p.sub ? p.sub : null;
  const ty = sub ? 1 - Q.lift : 1;
  const lite = clamp01(r.get('lite', 0));
  const subOn = sub ? clamp01(r.get('subOn', 1)) : 0;
  const qD = 2 * Q.qR + Q.qSw;
  const subW = sub ? p.subW ?? 0.5 * Q.size * sub.length : 0;
  const gx = -(qD + Q.gap + subW) / 2;
  const ny = -p.h / 2;
  const H = STAMP_HANDLE;
  return (
    <>
      {handle > 0.01 ? (
        <g opacity={handle < 0.99 ? handle : undefined}>
          <Hard
            off={worldShadow(r.world, 5)}
            render={(sh) => (
              <>
                <rect x={-H.neckW / 2} y={ny - H.neck} width={H.neckW} height={H.neck} fill={C.ink} />
                <rect x={-H.knobW / 2} y={ny - H.neck - H.knobH} width={H.knobW} height={H.knobH} rx={H.knobH / 2} fill={C.ink} />
              </>
            )}
          />
        </g>
      ) : null}
      <rect x={-p.w / 2} y={-p.h / 2} width={p.w} height={p.h} rx={12} fill="none" stroke={C.deep} strokeWidth={6} />
      <rect x={-p.w / 2 + 9} y={-p.h / 2 + 9} width={p.w - 18} height={p.h - 18} rx={7} fill="none" stroke={C.deep} strokeWidth={2.5} />
      {r.get('lite', 0) < 0.999 ? (
        <Txt x={0} y={ty} size={p.size ?? 40} weight={800} color={C.deep} anchor="middle" spacing={3} opacity={r.get('lite', 0) > 0.001 ? 1 - clamp01(r.get('lite', 0)) : undefined}>
          {p.text}
        </Txt>
      ) : null}
      {r.get('lite', 0) > 0.001 ? (
        // opt-in `lite` (absent / 0 = today's stamp): the text becomes a plain deep-cyan bar
        <rect x={-p.w / 2 + 30} y={sub ? ty - 12 : -11} width={p.w - 60} height={22} rx={11} fill={C.deep} opacity={r.get('lite', 0) < 0.999 ? clamp01(r.get('lite', 0)) : undefined} />
      ) : null}
      {sub && subOn > 0.001 && lite < 0.999 ? (
        // opt-in `sub`: second line « (?) + 1 question », faded in by `subOn` (the slam's contact)
        <g opacity={subOn * (1 - lite) < 0.999 ? subOn * (1 - lite) : undefined}>
          <circle cx={gx + qD / 2} cy={Q.dy} r={Q.qR} fill="none" stroke={C.deep} strokeWidth={Q.qSw} />
          <Txt x={gx + qD / 2} y={Q.dy} size={Q.qSize} weight={800} color={C.deep} anchor="middle">
            ?
          </Txt>
          <Txt x={gx + qD + Q.gap} y={Q.dy} size={Q.size} weight={600} color={C.deep}>
            {sub}
          </Txt>
        </g>
      ) : null}
      {sub && subOn > 0.001 && lite > 0.001 ? (
        // with `lite`, the second line becomes a bar too
        <rect x={gx} y={Q.dy - Q.bar / 2} width={qD + Q.gap + subW} height={Q.bar} rx={Q.bar / 2} fill={C.deep} opacity={subOn * lite < 0.999 ? subOn * lite : undefined} />
      ) : null}
    </>
  );
};

// ---------- bullet: a loose information pastille (ex. the AI's empty one), same drawing as a row's bullet ----------
const LooseBullet: React.FC<EntityProps> = ({r}) => {
  const p = r.e.p as {icon: string; r?: number};
  return <Bullet icon={p.icon} r={p.r ?? GEOM.BULLET.r} alarm={clamp01(r.get('alarm', 0))} />;
};

// ---------- burst: short rays flashing out of a point (the AI's glass brain « produces » something) ----------
const Burst: React.FC<EntityProps> = ({r}) => {
  const C = usePalette();
  const p = r.e.p as {r0: number; r1: number; n?: number; sw?: number; color?: string; a0?: number};
  const t = r.get('p', 0);
  if (t <= 0 || t >= 1) return null;
  const n = p.n ?? 8;
  const out = 1 - (1 - t) ** 2;
  const inner = p.r0 + (p.r1 - p.r0) * Math.max(0, out - 0.45);
  const outer = p.r0 + (p.r1 - p.r0) * out;
  return (
    <g opacity={t > 0.6 ? (1 - t) / 0.4 : 1}>
      {Array.from({length: n}, (_, k) => {
        const a = ((p.a0 ?? 0) + (360 * k) / n) * (Math.PI / 180);
        return (
          <line key={k} x1={inner * Math.cos(a)} y1={inner * Math.sin(a)} x2={outer * Math.cos(a)} y2={outer * Math.sin(a)} stroke={p.color ?? C.deep} strokeWidth={p.sw ?? 6} strokeLinecap="round" />
        );
      })}
    </g>
  );
};

// ---------- marker: numbered steps 1-2-3, the active disc slides ----------
// `labels` (optionnel) : légende sous chaque disque (ex. Limiter / Exiger / Relire), encre pour l'étape active, gris
// (ai_tick) pour les autres, en fondu selon la piste `active` ; `labelDy` / `labelSize` : GEOM.MARKER par défaut.
type MarkerP = {xs: number[]; y: number; labels?: string[]; labelDy?: number; labelSize?: number; moveBlank?: boolean};
const Marker: React.FC<EntityProps> = ({r}) => {
  const C = usePalette();
  const p = r.e.p as MarkerP;
  const M = GEOM.MARKER;
  const a = Math.max(0, Math.min(p.xs.length - 1, r.get('active', 0)));
  const i0 = Math.min(p.xs.length - 2, Math.floor(a));
  const cx = p.xs[i0] + (p.xs[i0 + 1] - p.xs[i0]) * (a - i0);
  const digit = Math.round(a) + 1;
  // opt-in track `on` (absent = 1 = today's marker): 0 = no active step yet, the active disc is drawn exactly as an
  // inactive one (r, paper, no shadow, small digit) and every label stays grey; 0 -> 1 grows it into the cyan disc.
  const on = r.get('on', 1);
  const lit = on === 1 ? 1 : clamp01(on);
  return (
    <>
      <line x1={p.xs[0]} x2={p.xs[p.xs.length - 1]} y1={p.y} y2={p.y} stroke={C.ink} strokeWidth={4} />
      {p.labels
        ? p.labels.map((t, i) => (
            <Txt key={`l${i}`} x={p.xs[i]} y={p.y + (p.labelDy ?? M.labelDy)} size={p.labelSize ?? M.labelSize} weight={700} color={mixHex(C.aiTick, C.ink, Math.max(clamp01(r.get(`done${i}`, 0)), on === 1 ? clamp01(1 - Math.abs(a - i)) : clamp01(1 - Math.abs(a - i)) * lit))} anchor="middle">
              {t}
            </Txt>
          ))
        : null}
      {p.xs.map((x, i) => {
        // opt-in tracks done0..doneN (absent = 0 = today's disc): the step is DONE, its label stays ink and a deep
        // tick replaces the digit in the disc (drawn 0 -> 1).
        const dn = clamp01(r.get(`done${i}`, 0));
        const tk = tickPath(26);
        return (
          <g key={x}>
            <circle cx={x} cy={p.y} r={M.r} fill={C.paper} stroke={C.ink} strokeWidth={4} />
            {dn < 1 ? (
              <g opacity={1 - dn}>
                <Txt x={x} y={p.y} size={22} weight={800} anchor="middle">
                  {String(i + 1)}
                </Txt>
              </g>
            ) : null}
            {dn > 0 ? (
              <path d={tk.d} transform={`translate(${x} ${p.y + 1})`} fill="none" stroke={C.deep} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={drawDash(tk.len, dn)} />
            ) : null}
          </g>
        );
      })}
      {on === 1 ? (
        <Hard off={6} render={(sh) => <circle cx={cx} cy={p.y} r={M.activeR} fill={sh ? C.ink : C.cyan} stroke={C.ink} strokeWidth={4} />} />
      ) : (
        <Hard
          off={6 * lit}
          render={(sh) => <circle cx={cx} cy={p.y} r={M.r + (M.activeR - M.r) * Math.max(0, on)} fill={sh ? C.ink : mixHex(C.paper, C.cyan, lit)} stroke={C.ink} strokeWidth={4} />}
        />
      )}
      {/* opt-in moveBlank (absent = today's marker): the sliding disc carries no digit until it lands */}
      {!p.moveBlank || Math.abs(a - Math.round(a)) < 0.02 ? (
        <Txt x={cx} y={p.y} size={on === 1 ? 34 : 22 + 12 * Math.max(0, on)} weight={800} anchor="middle">
          {String(digit)}
        </Txt>
      ) : null}
    </>
  );
};

export const COMPONENTS: Record<string, React.FC<EntityProps>> = {
  pill: Pill,
  figure: Figure,
  png: Png,
  window: Window,
  doc: Doc,
  fiche: Fiche,
  sheen: Sheen,
  line: Line,
  tick: Tick,
  label: Label,
  case: Case,
  wire: Wire,
  qmark: QMark,
  bubble: Bubble,
  pen: Pen,
  limb: Limb,
  stamp: Stamp,
  marker: Marker,
  bullet: LooseBullet,
  burst: Burst,
  // kit générique (entities_kit.tsx) : shape, text, icon, sector, gauge, counter, curve, seesaw, cursor, endcard, crowd
  ...KIT,
};

/** Types drawn as HTML (not inside the entity's SVG). */
export const HTML_TYPES = new Set(['png']);
