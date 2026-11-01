// Where a shot's illustration is on screen at a given frame. Overlays anchored to the object use the same
// pose, so they follow every move, tilt, entrance and exit of the hero.
import {easeInOut, easeOut, lerp, progress} from './anim';
import type {Asset, Shot, Style, Vec2} from './types';

export type Pose = {
  /** False outside [from, to + exit]. */
  visible: boolean;
  /** Screen px per asset px, including the entrance / exit scale. */
  k: number;
  /** k without the entrance / exit scale, relative to the shot's opening framing (camera zoom). */
  zoom: number;
  /** Entrance / exit scale factor (0.7 -> 1 -> 0.8). */
  anim: number;
  opacity: number;
  /** Entrance opacity alone (0 -> 1 in style.motion.enter_fade frames): gates overlays anchored to the hero. */
  enterOpacity: number;
  /** Exit progress (0 -> 1, eased) once the next shot has started; 0 for the last shot. */
  exitP: number;
  /** Image top-left on screen. */
  x: number;
  y: number;
  /** Rotation (deg) around the stage anchor. */
  rot: number;
  /** Focus point in asset px (also the rotation / scale pivot). */
  fx: number;
  fy: number;
  anchor: Vec2;
  brightness: number;
  saturate: number;
};

const framing = (shot: Shot, frame: number): {scale: number; focus: Vec2} => {
  let scale = shot.scale;
  let focus: Vec2 = shot.focus;
  for (const m of shot.moves) {
    if (frame < m.frame) break;
    const p = progress(frame, m.frame, m.dur, easeInOut);
    // Zoom in log space so the move feels even; focus moves with the same ease.
    scale = Math.exp(lerp(Math.log(scale), Math.log(m.scale), p));
    focus = [lerp(focus[0], m.focus[0], p), lerp(focus[1], m.focus[1], p)];
  }
  return {scale, focus};
};

/**
 * Handover grammar (reference: outgoing shapes shrink toward their own centre while opaque incoming shapes grow
 * over them, frame change peaking in the first 1-3 frames). Scale and opacity are separate curves:
 *   incoming  scale 0.7 -> 1 over `enter` (11) frames ease-out, opaque from its first frame (`enter_fade` 1) and
 *             drawn above the outgoing hero, so the outgoing one is never seen THROUGH it (no cross-dissolve);
 *   outgoing  scale 1 -> 0.8 over `exit` (8) frames ease-out, opacity 1 -> 0 over `exit_fade` (4.5) frames
 *             (`exit_ease` in-out: 0.96, 0.65, 0.15, 0): only its parts outside the incoming silhouette show while
 *             it shrinks away, then it is gone; the hero band keeps >= 0.8 of its luminance (no dip).
 * Both start on the same (word-onset) frame. Optional offsets turn a handover into a lateral push or a drop.
 * A hero handing over to a chapter card uses `shot.exit`: it shrinks further (0.4) toward the red protagonist's
 * slot and fades more slowly (ease-in-out) while the protagonist grows over it.
 */
export const exitSpan = (shot: Shot, style: Style): number =>
  Math.max(shot.exit?.dur ?? style.motion.exit, shot.exit?.fade ?? style.motion.exit_fade);

export const heroPose = (shot: Shot, asset: Asset, style: Style, frame: number, isLast: boolean): Pose => {
  const mo = style.motion;
  const exitStart = isLast ? undefined : shot.to;
  const visible = frame >= shot.from && (exitStart === undefined || frame < exitStart + exitSpan(shot, style));
  const ex = shot.exit ?? undefined;

  const cut = shot.enter === 'cut';
  const enterP = cut ? 1 : progress(frame, shot.from, mo.enter, easeOut);
  const enterOpacity = cut ? 1 : progress(frame, shot.from, mo.enter_fade, easeOut);
  const exitP = exitStart === undefined ? 0 : progress(frame, exitStart, ex?.dur ?? mo.exit, easeOut);
  const exitFade =
    exitStart === undefined
      ? 0
      : progress(frame, exitStart, ex?.fade ?? mo.exit_fade, ex || mo.exit_ease === 'in-out' ? easeInOut : easeOut);
  const anim = lerp(mo.enter_from, 1, enterP) * lerp(1, ex?.to ?? mo.exit_to, exitP);
  const opacity = enterOpacity * (1 - exitFade);

  const [eox, eoy] = shot.enter_offset ?? [0, 0];
  const [xox, xoy] = shot.exit_offset ?? [0, 0];
  const offX = eox * (1 - enterP) + xox * exitP;
  const offY = eoy * (1 - enterP) + xoy * exitP;
  let anchor: Vec2 = [shot.anchor[0] + offX, shot.anchor[1] + offY];
  if (ex?.target) anchor = [lerp(anchor[0], ex.target[0], exitP), lerp(anchor[1], ex.target[1], exitP)];

  const {scale, focus} = framing(shot, frame);
  const k = shot.fit * scale * anim;
  const [bx0, by0, bx1, by1] = asset.box;
  const fx = bx0 + focus[0] * (bx1 - bx0);
  const fy = by0 + focus[1] * (by1 - by0);

  let rot = 0;
  for (const t of shot.tilts) rot = lerp(rot, t.deg, progress(frame, t.frame, t.dur, easeOut));
  // A bell "ring": damped sway, the only oscillation in the piece (semantic, on the subscribe press).
  for (const s of shot.shakes ?? []) {
    const p = progress(frame, s.frame, s.dur, (t) => t);
    if (p > 0 && p < 1) rot += s.deg * Math.sin(3 * Math.PI * p) * (1 - p) * (1 - p);
  }

  let brightness = shot.tone?.brightness ?? 1;
  let saturate = shot.tone?.saturate ?? 1;
  for (const t of shot.tones) {
    const p = progress(frame, t.frame, t.dur, easeOut);
    brightness = lerp(brightness, t.brightness, p);
    saturate = lerp(saturate, t.saturate, p);
  }

  return {
    visible,
    k,
    zoom: scale / shot.scale,
    anim,
    opacity,
    enterOpacity,
    exitP,
    x: anchor[0] - fx * k,
    y: anchor[1] - fy * k,
    rot,
    fx,
    fy,
    anchor,
    brightness,
    saturate,
  };
};

/** Content-box fraction -> screen point, through the hero pose (scale, focus, tilt). */
export const toScreen = (pose: Pose, asset: Asset, uv: Vec2): Vec2 => {
  const [bx0, by0, bx1, by1] = asset.box;
  const px = (bx0 + uv[0] * (bx1 - bx0) - pose.fx) * pose.k;
  const py = (by0 + uv[1] * (by1 - by0) - pose.fy) * pose.k;
  const a = (pose.rot * Math.PI) / 180;
  return [
    pose.anchor[0] + px * Math.cos(a) - py * Math.sin(a),
    pose.anchor[1] + px * Math.sin(a) + py * Math.cos(a),
  ];
};
