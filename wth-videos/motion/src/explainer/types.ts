// Props of the "Explainer" composition. Written by pipeline/motion.py (build/Vxx/motion.json):
// every time is already a frame number, every visual event starts on a word onset.

export type Vec2 = [number, number];

export type Style = {
  bg: string;
  cream: string;
  /** Spoken word, dots, rings, red protagonist. */
  accent: string;
  /** Brand red for fills that carry cream text or icons. */
  fill: string;
  fill_shadow: string;
  font_family: string;
  stage: {cx: number; cy: number; box: [number, number]};
  hero_mask: {top0: number; top1: number; bottom0: number; bottom1: number};
  caption: {size: number; weight: number; tracking_em: number; baseline: number; max_width: number};
  motion: {
    enter: number;
    /** Incoming hero opacity 0 -> 1 (frames, ease-out); scale keeps `enter`. */
    enter_fade: number;
    enter_from: number;
    exit: number;
    /** Outgoing hero opacity 1 -> 0 (frames, ease-out: gone while the incoming covers it); scale keeps `exit`. */
    exit_fade: number;
    /** Easing of the outgoing fade: 'in-out' holds it a little then drops it, 'out' drops it at once. */
    exit_ease?: 'out' | 'in-out';
    exit_to: number;
    move: number;
    tilt: number;
    pop: number;
    tone: number;
    fade: number;
  };
  /** Step indicator layouts: the chapter card at centre stage (big) and the reminder row near the top (small). */
  steps: {
    small: StepLayout;
    big: StepLayout;
    /** Frames: rings grow in, the big row leaves in place, the protagonist slides. */
    enter: number;
    leave: number;
    slide: number;
  };
};

export type StepLayout = {d: number; red: number; gap: number; stroke: number; opacity: number};

export type Asset = {src: string; w: number; h: number; box: [number, number, number, number]};

export type Move = {frame: number; dur: number; scale: number; focus: Vec2};
export type Tilt = {frame: number; dur: number; deg: number};
export type Tone = {frame: number; dur: number; brightness: number; saturate: number};
export type Shake = {frame: number; dur: number; deg: number};

export type Shot = {
  id: string;
  asset: string;
  from: number;
  to: number;
  /** Screen px per asset px at scale 1 (content box fitted into the stage box). */
  fit: number;
  /** Screen point where the focus point sits. */
  anchor: Vec2;
  enter: 'grow' | 'cut';
  /** Entrance starts displaced by this (px) and settles with the scale (lateral push, drop from above). */
  enter_offset?: Vec2;
  /** Exit drifts by this (px) while shrinking. */
  exit_offset?: Vec2;
  /**
   * Exit override, set on a hero that hands over to a chapter card: it shrinks to `to` while its focus point
   * glides to `target` (the red protagonist's slot), so the protagonist visibly replaces it.
   */
  exit?: {to: number; dur: number; fade: number; target?: Vec2} | null;
  scale: number;
  focus: Vec2;
  moves: Move[];
  tilts: Tilt[];
  tones: Tone[];
  shakes?: Shake[];
  tone?: {brightness: number; saturate: number} | null;
};

type OverlayBase = {
  id: string;
  shot: string;
  from: number;
  /** Own exit frame; otherwise the overlay leaves with its shot. */
  until?: number;
  /** Content-box fraction of the shot's illustration (follows the object). */
  anchor?: Vec2;
  /** Fixed screen position (px). */
  pos?: Vec2;
  layer?: 'front' | 'behind';
};

export type DotOverlay = OverlayBase & {type: 'dot'; d?: number};
export type DotsOverlay = OverlayBase & {
  type: 'dots';
  anchors: Vec2[];
  d?: number;
  stagger?: number;
  /** 'tick': brand-red discs with a cream tick (one per line) instead of plain accent dots. */
  icon?: 'tick';
  /** From this frame the filled ticks turn into outline ticks (« ça a l'air vérifié »), 1-frame ripple. */
  flip_at?: number;
};
/** Thin accent leader line from a point of the object (anchor) to a fixed screen point, drawn on. */
export type LeaderOverlay = OverlayBase & {type: 'leader'; to: Vec2; draw?: number; stroke?: number};
export type RingOverlay = OverlayBase & {
  type: 'ring';
  r: number;
  stroke?: number;
  color?: 'accent' | 'cream';
  opacity?: number;
  /** Frames to draw the stroke clockwise from 12 o'clock; otherwise it pops. */
  draw?: number;
  pop?: boolean;
};
export type BarOverlay = OverlayBase & {type: 'bar'; r: number; stroke?: number; angle?: number; draw?: number};
export type PillOverlay = OverlayBase & {
  type: 'pill';
  text: string;
  style?: 'outline' | 'fill';
  size?: number;
  /** Leading icon: doc / cal in cream, cross in the accent red. */
  glyph?: 'doc' | 'cal' | 'cross';
  case?: 'upper' | 'keep';
  /** false: fully shown from its first frame (cover frame), no pop. */
  pop?: boolean;
  fill_at?: number;
  /** Frame a cream tick badge pops on the pill's corner (default: fill_at + 3 when fill_at is set). */
  tick_at?: number;
  flip_at?: number;
  flip_text?: string;
  flip_style?: 'outline' | 'fill';
  /** Collapse: from go_at the pill glides (ease-in-out) to go_to, shrinking and fading out. */
  go_at?: number;
  go_to?: Vec2;
};
export type ChipsOverlay = OverlayBase & {
  type: 'chips';
  texts: string[];
  /** Frame each chip pops in (cream outline: the caption alone carries the red « now » accent). */
  fill_at: number[];
  size?: number;
  gap?: number;
};
export type BadgeOverlay = OverlayBase & {
  type: 'badge';
  d?: number;
  icon: 'tick' | 'cross';
  style?: 'outline' | 'fill';
  flip_at?: number;
  flip_icon?: 'tick' | 'cross';
  flip_style?: 'outline' | 'fill';
};
export type QMarkOverlay = OverlayBase & {type: 'qmark'; size?: number; tilt_at?: number; tilt?: number};
export type ScanOverlay = OverlayBase & {type: 'scan'; rect: [number, number, number, number]; end: number};
export type BracketsOverlay = OverlayBase & {type: 'brackets'; rect: [number, number, number, number]};
export type SectorOverlay = OverlayBase & {
  type: 'sector';
  rx: number;
  ry: number;
  a0: number;
  a1: number;
  draw?: number;
};
export type TicksOverlay = OverlayBase & {type: 'ticks'; n: number; d?: number; gap?: number; fill_at: number[]};
export type TypingOverlay = OverlayBase & {type: 'typing'};

export type Overlay =
  | DotOverlay
  | DotsOverlay
  | RingOverlay
  | BarOverlay
  | PillOverlay
  | BadgeOverlay
  | QMarkOverlay
  | ScanOverlay
  | BracketsOverlay
  | SectorOverlay
  | TicksOverlay
  | TypingOverlay
  | ChipsOverlay
  | LeaderOverlay;

/** Chapter beat: from `from` to `to` the row sits big at centre stage (y = cy); the red protagonist pops or
 * slides to `index` on `go`. Between chapters the row rests small at y until `hide`. */
export type Chapter = {from: number; to: number; go: number; index: number};
export type Steps = {count: number; y: number; cy: number; chapters: Chapter[]; hide: number};

export type EndCard = {
  button?: {from: number; text: string; pos: Vec2; press_at?: number; flip_at?: number; flip_text?: string};
  cursor?: {from: number; start: Vec2; to: Vec2; glide?: number};
  wordmark?: {from: number; text: string; pos: Vec2; size?: number};
};

export type CaptionWord = {text: string; i: number; from: number};
export type CaptionGroup = {from: number; to: number; width: number; words: CaptionWord[]};

export type ExplainerProps = {
  id: string;
  fps: number;
  width: number;
  height: number;
  durationInFrames: number;
  style: Style;
  background: string;
  assets: Record<string, Asset>;
  shots: Shot[];
  overlays: Overlay[];
  steps: Steps | null;
  endCard: EndCard | null;
  captions: CaptionGroup[];
  beats?: {frame: number; word: string; what: string}[];
  meta?: Record<string, unknown>;
};
