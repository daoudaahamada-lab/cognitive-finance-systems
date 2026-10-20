// End card, after the reference outro, staged as one deliberate gesture: the red S’ABONNER key pops on
// "Abonne-toi", the arrow cursor comes in a few frames later, glides to the key's lower-right padding (never over
// the label) and presses it: the key dips into its shadow and comes back up, still red, and the bell hero rings on
// the same frame (the shot's `shake`). The wordmark fades in on "comprendre". Like the reference, the key stays a
// red S’ABONNER to the last frame (the loop point). An optional `flip_at` swaps the label hard on one frame
// (never two labels cross-fading on top of each other).
import {useCurrentFrame} from 'remotion';
import {easeInOut, easeOut, lerp, pop, progress, swap} from './anim';
import {Cursor, Icon} from './icons';
import type {EndCard as EndCardProps, Style} from './types';

const KEY_DEPTH = 8;

/** Press curve: 0 -> 1 in 2 frames, held 3 frames, back to 0 in 4 frames. */
const pressAmount = (frame: number, at: number | undefined): number => {
  if (at === undefined || frame < at) return 0;
  const t = frame - at;
  if (t < 2) return progress(frame, at, 2, easeOut);
  if (t < 5) return 1;
  return 1 - progress(frame, at + 5, 4, easeOut);
};

const Key: React.FC<{
  text: string;
  style: Style;
  press: number;
  filled: boolean;
  tick?: number;
}> = ({text, style, press, filled, tick}) => (
  <div
    style={{
      position: 'relative',
      height: 84,
      padding: '0 46px',
      boxSizing: 'border-box',
      borderRadius: 42,
      background: filled ? style.fill : 'rgba(10, 10, 11, 0.62)',
      border: filled ? 'none' : `4px solid ${style.cream}`,
      boxShadow: filled ? `0 ${KEY_DEPTH * (1 - press)}px 0 ${style.fill_shadow}` : undefined,
      transform: `translateY(${KEY_DEPTH * press}px)`,
      display: 'flex',
      alignItems: 'center',
      gap: 18,
      color: style.cream,
      fontFamily: `'${style.font_family}'`,
      fontWeight: 800,
      fontSize: 38,
      lineHeight: 1,
      letterSpacing: '0.06em',
      whiteSpace: 'nowrap',
    }}
  >
    <span style={{marginRight: '-0.06em'}}>{text}</span>
    {tick !== undefined ? <Icon name="tick" size={40} color={style.cream} stroke={3.4} drawn={tick} /> : null}
  </div>
);

export const EndCard: React.FC<{card: EndCardProps; style: Style}> = ({card, style}) => {
  const frame = useCurrentFrame();
  const {button, cursor, wordmark} = card;
  const press = pressAmount(frame, button?.press_at);
  const font = `'${style.font_family}'`;

  return (
    <div style={{position: 'absolute', inset: 0}}>
      {wordmark && frame >= wordmark.from - 1 ? (
        <div
          style={{
            position: 'absolute',
            left: 0,
            right: 0,
            top: wordmark.pos[1] - 60,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 24,
            opacity: progress(frame, wordmark.from, style.motion.fade, easeOut),
          }}
        >
          <div style={{width: 64, height: 6, borderRadius: 3, background: style.accent}} />
          <div
            style={{
              fontFamily: font,
              fontWeight: 800,
              fontSize: wordmark.size ?? 42,
              lineHeight: 1,
              letterSpacing: '-0.01em',
              color: style.cream,
              whiteSpace: 'nowrap',
            }}
          >
            {wordmark.text}
          </div>
        </div>
      ) : null}

      {button && frame >= button.from - 1
        ? (() => {
            const sw = swap(frame, button.flip_at);
            const flipped = sw.on;
            const s = pop(frame, button.from);
            const place = (scale: number, opacity: number, key: string, children: React.ReactNode) => (
              <div
                key={key}
                style={{
                  position: 'absolute',
                  left: button.pos[0],
                  top: button.pos[1],
                  opacity,
                  transform: `translate(-50%, -50%) scale(${s * scale})`,
                }}
              >
                {children}
              </div>
            );
            return (
              <>
                {!flipped ? place(1, 1, 'a', <Key text={button.text} style={style} press={press} filled />) : null}
                {flipped
                  ? place(
                      sw.neuScale,
                      1,
                      'b',
                      <Key
                        text={button.flip_text ?? button.text}
                        style={style}
                        press={0}
                        filled={false}
                        tick={progress(frame, button.flip_at! + 3, 8)}
                      />,
                    )
                  : null}
              </>
            );
          })()
        : null}

      {cursor && button?.press_at !== undefined && frame >= button.press_at ? (
        // Tap ripple from the cursor tip.
        <div style={{position: 'absolute', left: cursor.to[0], top: cursor.to[1], width: 0, height: 0}}>
          {(() => {
            const p = progress(frame, button.press_at, 12, easeOut);
            const r = lerp(10, 74, p);
            return (
              <div
                style={{
                  position: 'absolute',
                  left: -r,
                  top: -r,
                  width: 2 * r,
                  height: 2 * r,
                  borderRadius: '50%',
                  border: `3px solid ${style.cream}`,
                  boxSizing: 'border-box',
                  opacity: 0.75 * (1 - p),
                }}
              />
            );
          })()}
        </div>
      ) : null}

      {cursor && frame >= cursor.from - 1
        ? (() => {
            const g = progress(frame, cursor.from, cursor.glide ?? 10, easeInOut);
            const x = lerp(cursor.start[0], cursor.to[0], g);
            const y = lerp(cursor.start[1], cursor.to[1], g);
            // Leaves once the key has turned into ABONNÉ: the final frame holds only the result.
            const gone = button?.flip_at !== undefined ? 1 - progress(frame, button.flip_at, 5, easeOut) : 1;
            return (
              <div
                style={{
                  position: 'absolute',
                  left: x,
                  top: y,
                  opacity: pop(frame, cursor.from, 4) * gone,
                  transformOrigin: '0 0',
                  transform: `scale(${1 - 0.14 * press})`,
                  filter: 'drop-shadow(0 4px 10px rgba(0,0,0,0.55))',
                }}
              >
                <Cursor color={style.cream} outline={style.bg} />
              </div>
            );
          })()
        : null}
    </div>
  );
};
