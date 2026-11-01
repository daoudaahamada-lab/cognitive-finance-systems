import {useCurrentFrame} from 'remotion';
import {easeInOut, easeOut, lerp, pop, progress} from './anim';
import type {Chapter, StepLayout, Steps, Style} from './types';

/**
 * Step indicator, after the reference's « Numéro N » card.
 *
 * Chapter card (on the ordinal word: « Première », « Ensuite », « Dernière »): in the same frame the previous hero
 * starts shrinking toward the protagonist's slot (pose.ts, shot.exit), the reminder row at the top leaves in place,
 * and the big row grows in at centre stage with the entrance grammar (0.7 -> 1, ease-out, rings 1 frame apart).
 * The red protagonist pops on the first ordinal, and on the next ones re-appears where it was and slides to the
 * new step (ease-in-out). Drawn in front of the outgoing hero, so the disc visibly replaces it.
 *
 * Handover to the step's hero (in-place swap, never a glide through the hero): on the hero's first frame the big
 * row shrinks toward its own centres and fades in `leave` frames, drawn BEHIND the incoming hero, while the small
 * reminder row pops in near the top (pop, 2-frame stagger). The row leaves with the chute's first handover (hide).
 * Every filled shape uses the brand red (style.fill); outlines are cream.
 */
export const StepIndicator: React.FC<{steps: Steps; style: Style; width: number; layer: 'front' | 'behind'}> = ({
  steps,
  style,
  width,
  layer,
}) => {
  const frame = useCurrentFrame();
  const chapters = steps.chapters;
  const tok = style.steps;
  if (!chapters.length || frame < chapters[0].from - 1 || frame >= steps.hide + tok.leave + 2) return null;

  const xs = (lay: StepLayout) => (i: number) => width / 2 + (i - (steps.count - 1) / 2) * lay.gap;
  const ring = (key: string, x: number, y: number, lay: StepLayout, scale: number, opacity: number) =>
    opacity <= 0.001 || scale <= 0.001 ? null : (
      <div
        key={key}
        style={{
          position: 'absolute',
          left: x - lay.d / 2,
          top: y - lay.d / 2,
          width: lay.d,
          height: lay.d,
          borderRadius: '50%',
          boxSizing: 'border-box',
          border: `${lay.stroke}px solid ${style.cream}`,
          opacity: lay.opacity * opacity,
          transform: `scale(${scale})`,
        }}
      />
    );
  const disc = (key: string, x: number, y: number, lay: StepLayout, scale: number, opacity: number) =>
    opacity <= 0.001 || scale <= 0.001 ? null : (
      <div
        key={key}
        style={{
          position: 'absolute',
          left: x - lay.red / 2,
          top: y - lay.red / 2,
          width: lay.red,
          height: lay.red,
          borderRadius: '50%',
          background: style.fill,
          opacity,
          transform: `scale(${scale})`,
        }}
      />
    );

  const out: React.ReactNode[] = [];

  // Big row at centre stage, one per chapter: front while it holds the stage, behind the hero once it leaves.
  chapters.forEach((ch: Chapter, k) => {
    if (frame < ch.from - 1 || frame >= ch.to + tok.leave + 1) return;
    if ((layer === 'behind') !== frame >= ch.to) return;
    const lay = tok.big;
    const x = xs(lay);
    const leaveP = progress(frame, ch.to, tok.leave, easeOut);
    const keep = 1 - leaveP;
    const shrink = lerp(1, 0.6, leaveP);
    for (let i = 0; i < steps.count; i++) {
      const g = progress(frame, ch.from + i, tok.enter, easeOut);
      const f = progress(frame, ch.from + i, 3, easeOut);
      out.push(ring(`b${k}-${i}`, x(i), steps.cy, lay, lerp(0.7, 1, g) * shrink, f * keep));
    }
    const prev = k > 0 ? chapters[k - 1].index : ch.index;
    const slot = lerp(prev, ch.index, progress(frame, ch.go, tok.slide, easeInOut));
    // First chapter: the protagonist pops (0 -> 1) on the ordinal; later: it re-appears with the row, then slides.
    const grow = k === 0 ? pop(frame, ch.go) : lerp(0.7, 1, progress(frame, ch.from, tok.enter, easeOut));
    const fade = k === 0 ? 1 : progress(frame, ch.from, 3, easeOut);
    out.push(disc(`bred${k}`, x(slot), steps.cy, lay, grow * shrink, fade * keep));
  });

  // Small reminder row near the top: pops in on each step's hero, leaves in place on the next chapter (or hide).
  if (layer === 'front') {
    chapters.forEach((ch: Chapter, k) => {
      const end = k + 1 < chapters.length ? chapters[k + 1].from : steps.hide;
      if (frame < ch.to - 1 || frame >= end + tok.leave + 1) return;
      const lay = tok.small;
      const x = xs(lay);
      const leaveP = progress(frame, end, tok.leave, easeOut);
      const keep = 1 - leaveP;
      const shrink = lerp(1, 0.6, leaveP);
      for (let i = 0; i < steps.count; i++) {
        const s = pop(frame, ch.to + i * 2);
        out.push(ring(`s${k}-${i}`, x(i), steps.y, lay, s * shrink, keep));
      }
      out.push(disc(`sred${k}`, x(ch.index), steps.y, lay, pop(frame, ch.to + ch.index * 2) * shrink, keep));
    });
  }

  return out.length ? <div style={{position: 'absolute', inset: 0}}>{out}</div> : null;
};
