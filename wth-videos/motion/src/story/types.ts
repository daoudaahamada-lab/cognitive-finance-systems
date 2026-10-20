// Props of the "Story" composition (scene graph). Written by pipeline/story.py (build/Vxx/story/*.json).
//
// A story is a cast of persistent ENTITIES (stable ids) whose TRACKS are keyframed over the frames of the
// whole film. The composition renders the window [frameOffset, frameOffset + durationInFrames): an excerpt
// is the same timeline seen through a shorter window, so its first frame shows the evaluated state of the
// film at that frame (no intro animation).

export type Vec2 = [number, number];
export type Value = number | string | boolean | number[];

/** Easing of a keyframe segment. No overshoot anywhere (reference grammar). */
export type Ease = 'linear' | 'out' | 'in' | 'inOut' | 'outQuad' | 'inOutSine';

/**
 * One segment: from frame `f` the track goes from its current value (the value it had on frame f - 1, so an
 * interrupted move continues smoothly) to `v` in `d` frames with easing `e`. Frame `f` already shows the first
 * step (LEAD = 1): an event drawn on a word-onset frame is visible on that very frame.
 * `arc` (px, 2-vectors only): the path bulges upward by `arc` at mid-course (parabola on the eased progress).
 */
export type Key = {f: number; v: Value; d?: number; e?: Ease; arc?: number};

/** First key = initial value (its `f` is ignored); the following keys are segments in frame order. */
export type Track = Key[];

/** A point given in the LOCAL coordinates of another entity (follows it through every transform). */
export type Anchor = {id: string; at: Vec2};

export type Entity = {
  id: string;
  /** Component: pill, figure, png, window, doc, fiche, sheen, line, tick, label, case, wire, qmark, bubble, pen, limb,
   *  stamp, marker, bullet, burst (entities.tsx). */
  type: string;
  /** Scene-graph parent: local tracks are expressed in the parent's coordinates (translate, rotate, scale). */
  parent?: string;
  /** Paint order (flat list sorted by z, then declaration order); a `z` track overrides it over time. */
  z: number;
  /** Static parameters of the component (texts, sizes measured by the builder, colours, anchors...). */
  p: Record<string, unknown>;
  /**
   * Keyframed tracks. Common to every entity: pos [x, y], scale, sx, sy, rot (deg), opacity.
   * Component tracks: see entities.tsx (draw, chars, red, crack, compact, lit, w, h, seal, active...).
   */
  t: Record<string, Track>;
};

export type CaptionWord = {text: string; i: number; from: number; tone?: 'alert'};
export type CaptionGroup = {from: number; to: number; width: number; words: CaptionWord[]};

export type StoryStyle = {
  bg: string;
  grid: {pitch: number; line: number; color: string};
  ink: string;
  cyan: string;
  deep: string;
  light: string;
  paper: string;
  grey: string;
  red: string;
  /** Row background, rules and the AI's tick (ink at ~45 % on paper); optional for older props. */
  slot?: string;
  rule?: string;
  ai_tick?: string;
  font_family: string;
  caption: {size: number; weight: number; baseline: number; color: string; active: string; alert: string};
};

export type StoryProps = {
  id: string;
  fps: number;
  width: number;
  height: number;
  /** Frames rendered. */
  durationInFrames: number;
  /** Film frame shown on the composition's frame 0 (excerpt = window on the film timeline). */
  frameOffset: number;
  style: StoryStyle;
  entities: Entity[];
  /** Karaoke groups, in film frames. */
  captions: CaptionGroup[];
  showCaptions: boolean;
  meta?: Record<string, unknown>;
};
