// S03 — a horizontal assembly line: an idea bulb rides in on the belt; at each station a tool drops from the gantry,
// stamps the item and transforms it (script -> storyboard, voice waves, animated frame, cloud, calendar at 17:00); the
// tools line up in the « Ma chaîne » dock. End: a vertical phone playing a WealthTech Horizon video.
import React from 'react';
import {Hard, Icon, roundRect, Txt} from '../../story/draw';
import {back, Burst, C, CX, DOCK, dockSlot, eIn, eInOut, elStart, eOut, fr, lerp, Panel, seg, Sheet, Svg, thump, Tile} from '../kit';
import type {DeviceSpec, ShortProps} from '../types';

const IX = CX; // item centre
const IY = 790;
const BELT_Y = 958;
const RAIL_Y = 298;
const TOOL_Y = 412;
const TOOL_S = 150;
const STAMP_Y = 560;

const colorOf = (s: ShortProps, k: number) => s.elements[k]?.couleur ?? C.cyan;

// ---------- item states (centred on (0, 0), resting on y = +140) ----------
const Bulb: React.FC<{lit: number}> = ({lit}) => (
  <g>
    {lit > 0
      ? [0, 1, 2, 3, 4, 5, 6].map((j) => {
          const a = Math.PI + (j * Math.PI) / 6;
          return <line key={j} x1={Math.cos(a) * 100} y1={-40 + Math.sin(a) * 100} x2={Math.cos(a) * (100 + 30 * lit)} y2={-40 + Math.sin(a) * (100 + 30 * lit)} stroke={C.ink} strokeWidth={6} strokeLinecap="round" />;
        })
      : null}
    <Hard off={5} render={(sh) => <path d="M-40,40 C-40,10 -78,-6 -78,-42 A78,78 0 1 1 78,-42 C78,-6 40,10 40,40 Z" fill={sh ? C.ink : lit > 0.5 ? C.cyan : C.paper} stroke={C.ink} strokeWidth={4} strokeLinejoin="round" />} />
    <path d="M-16,30 V-10 L0,8 L16,-10 V30" fill="none" stroke={C.ink} strokeWidth={4} strokeLinejoin="round" />
    <path d={roundRect(-42, 40, 84, 30, 8)} fill={C.grey} stroke={C.ink} strokeWidth={4} />
    <path d={roundRect(-34, 70, 68, 26, 8)} fill={C.grey} stroke={C.ink} strokeWidth={4} />
    <path d="M-16,96 H16 L8,112 H-8 Z" fill={C.ink} />
  </g>
);

const Board: React.FC<{k: number}> = ({k}) => (
  <g>
    <Hard off={5} render={(sh) => <path d={roundRect(-140, -100, 280, 220, 18)} fill={sh ? C.ink : C.paper} stroke={C.ink} strokeWidth={4} />} />
    {[0, 1, 2, 3, 4, 5].map((j) => {
      const x = -95 + (j % 3) * 95;
      const y = -45 + Math.floor(j / 3) * 105;
      const kk = eOut(seg(k, j * 0.12, j * 0.12 + 0.4));
      return (
        <g key={j} transform={`translate(${x} ${y}) scale(${kk})`}>
          <path d={roundRect(-38, -40, 76, 80, 8)} fill={j % 2 ? C.light : C.slot} stroke={C.ink} strokeWidth={3} />
          {j % 3 === 0 ? <circle cx={0} cy={0} r={16} fill={C.cyan} stroke={C.ink} strokeWidth={2.5} /> : j % 3 === 1 ? <rect x={-16} y={-16} width={32} height={32} rx={4} fill={C.deep} /> : <path d="M-18,16 L0,-16 L18,16 Z" fill={C.cyan} stroke={C.ink} strokeWidth={2.5} />}
        </g>
      );
    })}
  </g>
);

const Waves: React.FC<{u: number}> = ({u}) => (
  <g>
    {[0, 1, 2].map((j) => {
      const t = ((u - 14 + j * 7) % 21) / 21;
      if (u < 14 + 0) return null;
      const r = 150 + t * 120;
      return [1, -1].map((sg) => (
        <path key={`${j}${sg}`} d={`M${sg * r * 0.72},${-r * 0.55} A${r},${r} 0 0 ${sg > 0 ? 1 : 0} ${sg * r * 0.72},${r * 0.55}`} fill="none" stroke={C.deep} strokeWidth={8} strokeLinecap="round" opacity={(1 - t) * seg(u, 14, 18)} transform="translate(0 10)" />
      ));
    })}
  </g>
);

const Frame916: React.FC<{u: number}> = ({u}) => {
  const t = u * 0.22;
  return (
    <g>
      <Hard off={5} render={(sh) => <path d={roundRect(-82, -130, 164, 266, 18)} fill={sh ? C.ink : C.bg} stroke={C.ink} strokeWidth={5} />} />
      <circle cx={-30} cy={-60 + Math.sin(t) * 30} r={22} fill={C.cyan} stroke={C.ink} strokeWidth={3} />
      <g transform={`translate(32 -40) rotate(${u * 9})`}>
        <rect x={-20} y={-20} width={40} height={40} rx={5} fill={C.deep} stroke={C.ink} strokeWidth={3} />
      </g>
      <rect x={-56} y={60} width={112 * (0.4 + 0.6 * Math.abs(Math.sin(t * 0.7)))} height={18} rx={9} fill={C.cyan} stroke={C.ink} strokeWidth={3} />
      <rect x={-56} y={92} width={80} height={14} rx={7} fill={C.grey} />
    </g>
  );
};

const Cloud: React.FC<{s?: number}> = ({s = 1}) => (
  <g transform={`scale(${s})`}>
    <Hard off={5} render={(sh) => <path d="M-120,40 A50,50 0 0 1 -90,-38 A70,70 0 0 1 40,-62 A56,56 0 0 1 128,-10 A46,46 0 0 1 112,64 H-96 A40,40 0 0 1 -120,40 Z" fill={sh ? C.ink : C.light} stroke={C.ink} strokeWidth={5} strokeLinejoin="round" />} />
    <path d="M-10,40 V-14 M-30,6 L-10,-16 L10,6" fill="none" stroke={C.deep} strokeWidth={7} strokeLinecap="round" strokeLinejoin="round" />
  </g>
);

const Calendar: React.FC<{u: number}> = ({u}) => (
  <g>
    <Hard off={5} render={(sh) => <path d={roundRect(-150, -90, 300, 220, 20)} fill={sh ? C.ink : C.paper} stroke={C.ink} strokeWidth={4} />} />
    <path d={roundRect(-150, -90, 300, 56, 20)} fill={C.deep} stroke={C.ink} strokeWidth={4} />
    {[0, 1, 2, 3, 4, 5, 6, 7].map((j) => (
      <rect key={j} x={-122 + (j % 4) * 64} y={-16 + Math.floor(j / 4) * 64} width={52} height={50} rx={8} fill={j === 5 ? C.light : C.slot} stroke={C.ink} strokeWidth={2.5} />
    ))}
    <g transform={`translate(42 74) scale(${back(seg(u, 32, 38))})`}>
      <Hard off={4} render={(sh) => <path d={roundRect(-84, -34, 168, 68, 34)} fill={sh ? C.ink : C.cyan} stroke={C.ink} strokeWidth={4} />} />
      <Txt x={0} y={0} size={40} weight={800} anchor="middle" tabular>
        17:00
      </Txt>
    </g>
  </g>
);

/** Item on the belt at element frame f (state machine of the transformations). */
const Item: React.FC<{f: number}> = ({f}) => {
  const ph = (k: number) => f - elStart(k);
  // hook: the bulb rides in from the left and lights up
  if (f < elStart(0) + 14) {
    const lit = eOut(seg(f, 32, 40));
    return <Bulb lit={lit} />;
  }
  const u1 = ph(0);
  if (f < elStart(0) + 28) {
    // Claude, first stamp: the bulb becomes a script page
    return (
      <g transform={`scale(${back(seg(u1, 14, 20))})`}>
        <Sheet x={0} y={0} w={180} h={230} lines={5} />
      </g>
    );
  }
  if (f < elStart(1) + 14) {
    // second stamp: the page becomes a 6-panel storyboard (+ voice waves from u 14 of ElevenLabs)
    return (
      <g transform={`scale(${back(seg(u1, 28, 34))})`}>
        <Board k={seg(u1, 28, 44)} />
      </g>
    );
  }
  if (f < elStart(2) + 14) {
    const u = ph(1);
    return (
      <g>
        <Waves u={u} />
        <g transform={`scale(${thump(u, 14, 0.06)})`}>
          <Board k={1} />
        </g>
        <g transform="translate(0 150)">
          {Array.from({length: 11}, (_, j) => {
            const h = 10 + 26 * Math.abs(Math.sin(u * 0.5 + j * 1.1)) * seg(u, 14, 20);
            return <rect key={j} x={-110 + j * 20} y={-h / 2 - 22} width={10} height={h} rx={5} fill={C.deep} />;
          })}
        </g>
      </g>
    );
  }
  if (f < elStart(3) + 14) {
    const u = ph(2);
    return (
      <g transform={`translate(0 -10) scale(${back(seg(u, 14, 20))})`}>
        <Frame916 u={u} />
      </g>
    );
  }
  if (f < elStart(4) + 14) {
    // Cloudinary: a cloud appears above and the frame rises into it; then the cloud rests on the belt
    const u = ph(3);
    const rise = eInOut(seg(u, 18, 32));
    if (u < 60) {
      return (
        <g>
          <g transform={`translate(0 ${lerp(-10, -170, rise)}) scale(${lerp(1, 0.35, rise)})`} opacity={1 - seg(u, 30, 34)}>
            <Frame916 u={u} />
          </g>
          <g transform={`translate(0 ${lerp(-200, 0, eInOut(seg(u, 34, 46)))}) scale(${back(seg(u, 12, 20)) * thump(u, 32, 0.08)})`}>
            <Cloud />
          </g>
        </g>
      );
    }
    return <Cloud />;
  }
  // Metricool: the cloud lifts, a calendar arrives, the cloud drops the video onto 17:00
  const u = ph(4);
  const lift = eInOut(seg(u, 10, 18));
  const drop = eIn(seg(u, 22, 32));
  return (
    <g>
      <g transform={`translate(0 30) scale(${back(seg(u, 14, 22))})`}>
        <Calendar u={u} />
      </g>
      {u < 34 ? (
        <g transform={`translate(${lerp(0, -38, drop)} ${lerp(-175, 55, drop)}) scale(${lerp(0.3, 0.2, drop)})`} opacity={seg(u, 18, 22)}>
          <Frame916 u={u} />
        </g>
      ) : null}
      <g transform={`translate(0 ${lerp(0, -240, lift)}) scale(${lerp(1, 0.7, lift)})`} opacity={1 - seg(u, 36, 44)}>
        <Cloud />
      </g>
      <Burst x={-38} y={60} t={seg(u, 32, 42)} r0={50} r1={95} color={C.deep} />
    </g>
  );
};

const Belt: React.FC<{phase: number}> = ({phase}) => (
  <g>
    <Hard off={6} render={(sh) => <path d={roundRect(70, BELT_Y - 26, 848, 52, 26)} fill={sh ? C.ink : C.grey} stroke={C.ink} strokeWidth={4} />} />
    <defs>
      <clipPath id="beltclip">
        <path d={roundRect(74, BELT_Y - 22, 840, 44, 22)} />
      </clipPath>
    </defs>
    <g clipPath="url(#beltclip)">
      {Array.from({length: 17}, (_, j) => {
        const x = 40 + j * 60 + (phase % 60);
        return <line key={j} x1={x} y1={BELT_Y - 22} x2={x - 16} y2={BELT_Y + 22} stroke={C.ink} strokeWidth={4} opacity={0.4} />;
      })}
    </g>
    {[100, 300, 495, 690, 888].map((x) => (
      <g key={x}>
        <circle cx={x} cy={BELT_Y} r={15} fill={C.paper} stroke={C.ink} strokeWidth={4} />
        <circle cx={x} cy={BELT_Y} r={4} fill={C.ink} />
      </g>
    ))}
  </g>
);

const beltPhase = (f: number) => {
  let p = 380 * eOut(seg(f, 8, 32));
  for (let k = 0; k < 5; k++) p += 120 * eInOut(seg(f, elStart(k) + 46, elStart(k) + 60));
  return p;
};

const Stage: React.FC<{s: ShortProps; f: number}> = ({s, f}) => {
  const ko = eOut(seg(f, 26, 40));
  const gantry = eOut(seg(f, 46, 60));
  const active = f >= elStart(0) && f < elStart(5) ? Math.floor((f - elStart(0)) / 60) : -1;
  // item position: rides in from the left during the hook, then hops a little at each belt move
  const enter = eOut(seg(f, 8, 32));
  let ix = lerp(150, IX, enter);
  let iy = IY;
  if (active >= 0) {
    const u = f - elStart(active);
    iy -= Math.sin(Math.PI * seg(u, 46, 60)) * 14;
    ix += Math.sin(Math.PI * seg(u, 46, 60)) * 10;
  }
  return (
    <Svg>
      {/* gantry (after the hook title) */}
      {gantry > 0.01 ? (
        <g opacity={gantry}>
          <rect x={98} y={lerp(BELT_Y, RAIL_Y, gantry)} width={14} height={BELT_Y - lerp(BELT_Y, RAIL_Y, gantry)} fill={C.ink} />
          <rect x={878} y={lerp(BELT_Y, RAIL_Y, gantry)} width={14} height={BELT_Y - lerp(BELT_Y, RAIL_Y, gantry)} fill={C.ink} />
          <path d={roundRect(86, lerp(BELT_Y, RAIL_Y, gantry) - 12, 818, 24, 12)} fill={C.deep} stroke={C.ink} strokeWidth={4} />
        </g>
      ) : null}
      <Belt phase={beltPhase(f)} />
      <g opacity={seg(f, 8, 12)} transform={`translate(${ix} ${iy})`}>
        <Item f={f} />
      </g>
      {/* dock: « Ma chaîne », 5 tool tiles joined by arrows */}
      <g opacity={seg(f, 24, 32)} transform={`translate(${CX} ${DOCK.y + DOCK.h / 2}) scale(${lerp(0.85, 1, ko)}) translate(${-CX} ${-(DOCK.y + DOCK.h / 2)})`}>
        <Panel x={DOCK.x} y={DOCK.y} w={DOCK.w} h={DOCK.h} r={DOCK.r} />
        <Txt x={DOCK.x + 34} y={DOCK.y + 44} size={38} weight={800}>
          {fr('Ma chaîne')}
        </Txt>
        {[0, 1, 2, 3].map((k) => (
          <g key={k} transform={`translate(${(dockSlot(k)[0] + dockSlot(k + 1)[0]) / 2} ${dockSlot(k)[1]})`}>
            <Icon name="arrow" s={34} color={C.ink} sw={4} />
          </g>
        ))}
        {s.elements.slice(0, 5).map((el, k) => {
          const [sx, sy] = dockSlot(k);
          const u = f - elStart(k);
          const home = f >= elStart(k) + 58 || f < elStart(0) || active < k;
          if (!home || (active === k && u < 58)) return <Tile key={k} x={sx} y={sy} s={DOCK.tile - 8} color={C.cyan} dashed />;
          return <Tile key={k} x={sx} y={sy} s={(DOCK.tile - 8) * back(seg(f, 28 + 3 * k, 36 + 3 * k))} color={colorOf(s, k)} name={el.nom} badge={f >= elStart(k) + 54 ? 1 : 0} />;
        })}
      </g>
      {active >= 0
        ? (() => {
            const k = active;
            const u = f - elStart(k);
            const el = s.elements[k];
            const [sx, sy] = dockSlot(k);
            // tool: rises from its dock slot to the gantry (u 0-10), stamps (u 10-16), Claude stamps twice (u 24-30)
            const a = eOut(seg(u, 0, 10));
            const r = eInOut(seg(u, 46, 58));
            const stamp1 = eIn(seg(u, 10, 14)) * (1 - eOut(seg(u, 16, 24)));
            const stamp2 = k === 0 ? eIn(seg(u, 24, 28)) * (1 - eOut(seg(u, 30, 38))) : 0;
            const sy2 = TOOL_Y + (STAMP_Y - TOOL_Y) * Math.max(stamp1, stamp2);
            const tx = lerp(lerp(sx, CX, a), sx, r);
            const ty = lerp(lerp(sy, sy2, a), sy, r) - Math.sin(Math.PI * r) * 60;
            const ts = lerp(lerp(DOCK.tile - 8, TOOL_S, a), DOCK.tile - 8, r);
            const rod = a * (1 - r);
            return (
              <>
                {rod > 0.05 ? <rect x={CX - 7} y={RAIL_Y} width={14} height={Math.max(0, ty - ts / 2 - RAIL_Y)} fill={C.ink} opacity={rod} /> : null}
                <g opacity={seg(u, 5, 11) * (1 - seg(u, 44, 50))}>
                  <Txt x={CX + TOOL_S / 2 + 26} y={TOOL_Y} size={48} weight={800}>
                    {fr(el.nom)}
                  </Txt>
                </g>
                <Burst x={CX} y={STAMP_Y + 70} t={seg(u, 14, 24)} r0={110} r1={170} />
                {k === 0 ? <Burst x={CX} y={STAMP_Y + 70} t={seg(u, 28, 38)} r0={110} r1={170} /> : null}
                <Tile x={tx} y={ty} s={ts} color={colorOf(s, k)} name={el.nom} badge={u >= 54 ? back(seg(u, 54, 60)) : 0} />
              </>
            );
          })()
        : null}
    </Svg>
  );
};

/** The final product: a vertical phone playing a WealthTech Horizon video. */
const Emblem: React.FC<{s: ShortProps; k: number; u: number}> = ({k, u}) => {
  const prog = seg(u, 0, 60);
  return (
    <g transform={`translate(${(1 - eOut(k)) * -60} -20)`} opacity={Math.min(1, k * 2)}>
      <Hard off={6} render={(sh) => <path d={roundRect(-82, -140, 164, 280, 30)} fill={sh ? C.ink : C.ink} stroke={C.ink} strokeWidth={4} />} />
      <path d={roundRect(-70, -122, 140, 244, 18)} fill={C.bg} />
      <Txt x={0} y={-90} size={22} weight={800} anchor="middle" color={C.deep}>
        WTH
      </Txt>
      <circle cx={0} cy={-10} r={38} fill={C.cyan} stroke={C.ink} strokeWidth={4} />
      <path d="M-11,-28 L19,-10 L-11,8 Z" fill={C.ink} />
      {[0, 1, 2].map((j) => (
        <rect key={j} x={-50 + j * 36} y={60 - 26 * Math.abs(Math.sin(u * 0.4 + j))} width={26} height={26 * Math.abs(Math.sin(u * 0.4 + j)) + 4} rx={4} fill={C.deep} />
      ))}
      <rect x={-56} y={92} width={112} height={8} rx={4} fill={C.grey} />
      <rect x={-56} y={92} width={112 * prog} height={8} rx={4} fill={C.deep} />
      <Txt x={0} y={176} size={36} weight={800} anchor="middle">
        1 vidéo
      </Txt>
    </g>
  );
};

export const line: DeviceSpec = {
  Stage,
  Emblem,
  roleTop: 1075,
  hookCard: true,
  recap: (s) => s.elements.map((e) => ({label: e.nom, mark: 'tile', color: e.couleur})),
};
