// Reusable, data-driven "Story" composition: a scene graph of persistent entities whose keyframed tracks
// carry the whole film (pipeline/story.py writes the props). Ivory background with the static 36 px grid,
// flat vector entities, karaoke captions (toggle: showCaptions).
import React, {useMemo} from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {FONT_FAMILY} from '../fonts';
import {PaletteContext, paletteFromStyle} from './draw';
import {COMPONENTS, HTML_TYPES} from './entities';
import {SceneFrame, type Resolved} from './timeline';
import type {CaptionGroup, StoryProps, StoryStyle} from './types';

const EntityView: React.FC<{r: Resolved; scene: SceneFrame}> = ({r, scene}) => {
  if (r.opacity <= 0.002) return null;
  const m = r.world;
  if (Math.abs(m[0] * m[3] - m[1] * m[2]) < 1e-6) return null; // scaled to a point: gone
  const Comp = COMPONENTS[r.e.type];
  if (!Comp) throw new Error(`Story: no component for entity type "${r.e.type}" (${r.e.id})`);
  return (
    <div
      style={{
        position: 'absolute',
        left: 0,
        top: 0,
        width: 0,
        height: 0,
        transformOrigin: '0 0',
        transform: `matrix(${m.map((x) => x.toFixed(5)).join(',')})`,
        opacity: r.opacity < 0.999 ? r.opacity : undefined,
      }}
    >
      {HTML_TYPES.has(r.e.type) ? (
        <Comp r={r} scene={scene} />
      ) : (
        <svg width={1} height={1} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
          <Comp r={r} scene={scene} />
        </svg>
      )}
    </div>
  );
};

/** Karaoke: one centred line, baseline fixed; the spoken word in deep cyan (alert words in red); hard cuts. */
const Captions: React.FC<{groups: CaptionGroup[]; n: number; style: StoryStyle; width: number; height: number}> = ({groups, n, style, width, height}) => {
  const group = groups.find((g) => n >= g.from && n < g.to);
  if (!group) return null;
  let active = -1;
  group.words.forEach((w, i) => {
    if (n >= w.from) active = i;
  });
  const c = style.caption;
  return (
    <svg width={width} height={height} style={{position: 'absolute', inset: 0}}>
      <text
        x={width / 2}
        y={c.baseline}
        textAnchor="middle"
        style={{fontFamily: `'${FONT_FAMILY}'`, fontWeight: c.weight, fontSize: c.size, whiteSpace: 'pre', fontKerning: 'normal'}}
      >
        {group.words.map((w, i) => (
          <tspan key={w.i} fill={i === active ? (w.tone === 'alert' ? c.alert : c.active) : c.color}>
            {(i > 0 ? ' ' : '') + w.text}
          </tspan>
        ))}
      </text>
    </svg>
  );
};

export const Story: React.FC<StoryProps> = (props) => {
  const frame = useCurrentFrame();
  const n = frame + props.frameOffset;
  const {style, width, height} = props;
  const scene = new SceneFrame(props.entities, n);
  // Paint order: z (static, or a `z` track when an entity changes layer), then declaration order (stable sort).
  const indexed = useMemo(() => props.entities.map((e, i) => ({e, i})), [props.entities]);
  const order = indexed
    .map(({e, i}) => ({e, i, z: e.t.z ? scene.resolve(e.id).get('z', e.z) : e.z}))
    .sort((a, b) => a.z - b.z || a.i - b.i)
    .map((x) => x.e);
  const palette = useMemo(() => paletteFromStyle(style), [style]);
  const g = style.grid;
  const off = -Math.floor(g.line / 2);
  return (
    <AbsoluteFill
      style={{
        backgroundColor: style.bg,
        // Static grid anchored top-left: 2 px lines covering pixels 36k-1 and 36k (same as the reference).
        backgroundImage: `linear-gradient(to right, ${g.color} ${g.line}px, transparent ${g.line}px), linear-gradient(to bottom, ${g.color} ${g.line}px, transparent ${g.line}px)`,
        backgroundSize: `${g.pitch}px ${g.pitch}px`,
        backgroundPosition: `${off}px ${off}px`,
      }}
    >
      <PaletteContext.Provider value={palette}>
        {order.map((e) => (
          <EntityView key={e.id} r={scene.resolve(e.id)} scene={scene} />
        ))}
      </PaletteContext.Provider>
      {props.showCaptions ? <Captions groups={props.captions} n={n} style={style} width={width} height={height} /> : null}
    </AbsoluteFill>
  );
};

export const defaultStoryProps: StoryProps = {
  id: 'demo',
  fps: 30,
  width: 1080,
  height: 1920,
  durationInFrames: 60,
  frameOffset: 0,
  style: {
    bg: '#F6F0E4',
    grid: {pitch: 36, line: 2, color: '#ECE4D4'},
    ink: '#1E1416',
    cyan: '#19B3C7',
    deep: '#0A7487',
    light: '#D3F0F6',
    paper: '#FFFDF8',
    grey: '#DDD5C6',
    red: '#C8102E',
    slot: '#F4EEE3',
    rule: '#E6DECF',
    ai_tick: '#9C9496',
    font_family: 'WTH Inter',
    caption: {size: 64, weight: 700, baseline: 1350, color: '#1E1416', active: '#0A7487', alert: '#C8102E'},
  },
  entities: [
    {id: 'pastille', type: 'pill', z: 1, p: {text: 'Client · 9 h', w: 230}, t: {pos: [{f: 0, v: [540, 760]}], scale: [{f: 0, v: 0}, {f: 0, v: 1, d: 9, e: 'out'}]}},
  ],
  captions: [],
  showCaptions: true,
};
