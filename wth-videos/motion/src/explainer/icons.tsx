// Small line icons in a 24x24 box, drawn with a stroke so they can "draw on" via strokeDashoffset.

export const ICON_PATHS = {
  tick: 'M5.5 12.5 L10 17 L18.5 7.5',
  cross: 'M7 7 L17 17 M17 7 L7 17',
  doc: 'M7 3.5 H14 L18 7.5 V20.5 H7 Z M14 3.5 V7.5 H18 M9.5 12 H15.5 M9.5 15.5 H15.5',
  cal: 'M5 6.5 H19 V19.5 H5 Z M5 10.5 H19 M9 4 V8 M15 4 V8',
} as const;

// Lengths (in the 24 px box) used for draw-on animations.
export const ICON_LENGTH = {tick: 20, cross: 29, doc: 60, cal: 64} as const;

export type IconName = keyof typeof ICON_PATHS;

// Icons made of separate strokes draw them in parallel. The cross grows outward from its centre: drawn
// stroke after stroke, or both strokes from the top, its partial frames look like a "v", i.e. a tick.
const STROKES: Partial<Record<IconName, {d: string; len: number}[]>> = {
  cross: [
    {d: 'M12 12 L7 7', len: 7.1},
    {d: 'M12 12 L17 7', len: 7.1},
    {d: 'M12 12 L17 17', len: 7.1},
    {d: 'M12 12 L7 17', len: 7.1},
  ],
};

export const Icon: React.FC<{
  name: IconName;
  size: number;
  color: string;
  stroke?: number;
  /** 0..1 portion drawn. */
  drawn?: number;
}> = ({name, size, color, stroke = 3, drawn = 1}) => {
  const parts = STROKES[name] ?? [{d: ICON_PATHS[name], len: ICON_LENGTH[name]}];
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" style={{display: 'block', overflow: 'visible'}}>
      {parts.map((p, i) => (
        <path
          key={i}
          d={p.d}
          fill="none"
          stroke={color}
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeDasharray={drawn < 1 ? `${p.len} ${p.len}` : undefined}
          strokeDashoffset={drawn < 1 ? p.len * (1 - drawn) : undefined}
        />
      ))}
    </svg>
  );
};

/** Arrow pointer, tip at (0, 0), 30x46 box. */
export const Cursor: React.FC<{color: string; outline: string}> = ({color, outline}) => (
  <svg width={34} height={50} viewBox="-2 -2 34 50" style={{display: 'block', overflow: 'visible'}}>
    <path
      d="M0 0 L0 38 L9.5 29.5 L16 44 L22.5 41 L16 27 L29 27 Z"
      fill={color}
      stroke={outline}
      strokeWidth={2.6}
      strokeLinejoin="round"
    />
  </svg>
);
