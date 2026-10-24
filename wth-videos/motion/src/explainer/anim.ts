// Frame-based motion grammar of the reference: hold still, then burst.
// Entrances / pops / tilts ease out (cubic, no overshoot); moves of an element already on screen ease in-out.
import {Easing, interpolate} from 'remotion';

export const easeOut = Easing.out(Easing.cubic);
export const easeInOut = Easing.inOut(Easing.cubic);
export const easeIn = Easing.in(Easing.cubic);

const clampOpts = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

/**
 * Every animation shows its first step ON its start frame (the word-onset frame, where the karaoke accent also
 * switches), like the reference (83 of 107 motion onsets in the word-switch frame). Without this lead, an
 * eased curve is 0 on its start frame and visuals trailed the voice by one frame (33 ms).
 */
export const LEAD = 1;

/** 0 up to `start - 1`, eased to 1 at `start - 1 + dur` (so frame `start` already shows step 1/dur). */
export const progress = (frame: number, start: number, dur: number, easing = easeOut): number =>
  dur <= 0
    ? frame >= start
      ? 1
      : 0
    : interpolate(frame, [start - LEAD, start - LEAD + dur], [0, 1], {...clampOpts, easing});

export const lerp = (a: number, b: number, t: number): number => a + (b - a) * t;

/** Pop 0 -> 1 (small accents), ~300 ms ease-out cubic: 0.30, 0.54, 0.70 ... on frames start, +1, +2. */
export const pop = (frame: number, start: number, dur = 9): number => progress(frame, start, dur, easeOut);

/** Leaving: 1 -> 0 over `dur` frames from `start` (eased out, fast start). */
export const leave = (frame: number, start: number | undefined, dur = 5): number =>
  start === undefined ? 1 : 1 - progress(frame, start, dur, easeOut);

/**
 * Same-frame state swap (replaces the old 2D card flip): the old face shrinks 1 -> 0.6 and fades out in 4 frames
 * while the new face pops 0.7 -> 1 in 9 frames (ease-out) and is opaque after 3.
 */
export const swap = (frame: number, at: number | undefined) => {
  if (at === undefined || frame < at - LEAD + 1) return {old: 1, oldScale: 1, neu: 0, neuScale: 0.7, on: false};
  const o = progress(frame, at, 4, easeOut);
  return {
    old: 1 - o,
    oldScale: lerp(1, 0.6, o),
    neu: progress(frame, at, 3, easeOut),
    neuScale: lerp(0.7, 1, progress(frame, at, 9, easeOut)),
    on: true,
  };
};

/** Point on an ellipse arc path (degrees, 0 = 3 o'clock, clockwise in screen space). */
export const polar = (cx: number, cy: number, rx: number, ry: number, deg: number): [number, number] => {
  const a = (deg * Math.PI) / 180;
  return [cx + rx * Math.cos(a), cy + ry * Math.sin(a)];
};
