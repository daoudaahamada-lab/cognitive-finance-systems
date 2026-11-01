// S04 — an unknown crypto app arrives locked behind 5 padlocks (chained in a ring). Each check is played in the card
// below; when it passes, its padlock pops open (cyan, check) and its chain falls. All open: the app is verified.
import React from 'react';
import {Hard, Icon, roundRect, Txt} from '../../story/draw';
import {back, Burst, C, CheckBadge, clamp01, CX, eIn, eInOut, elStart, eOut, fr, lerp, seg, Svg, thump} from '../kit';
import type {DeviceSpec, ShortProps} from '../types';

const RING_HOOK = 760;
const RING_Y = 630;
const R = 200;
const CARD_Y = 1010; // centre of the check card (890 .. 1130)
const NAME_Y = 262;
const OPEN_U = 38; // the padlock opens on this beat of its element

const lockPos = (k: number, cy: number): [number, number] => {
  const a = ((-90 + 72 * k) * Math.PI) / 180;
  return [CX + Math.cos(a) * R, cy + Math.sin(a) * R];
};

const Padlock: React.FC<{x: number; y: number; s: number; open: number; n: number}> = ({x, y, s, open, n}) => {
  const lift = eOut(clamp01(open * 1.6));
  const swing = eOut(clamp01(open * 1.6 - 0.4));
  return (
    <g transform={`translate(${x} ${y}) scale(${s})`}>
      <g transform={`translate(0 ${-24 * lift}) rotate(${-38 * swing} 30 -10)`}>
        <path d="M-30,-6 V-40 A30,30 0 0 1 30,-40 V-6" fill="none" stroke={C.ink} strokeWidth={16} strokeLinecap="round" />
        <path d="M-30,-6 V-40 A30,30 0 0 1 30,-40 V-6" fill="none" stroke={C.grey} strokeWidth={7} strokeLinecap="round" />
      </g>
      <Hard off={5} render={(sh) => <path d={roundRect(-50, -12, 100, 84, 16)} fill={sh ? C.ink : open > 0.5 ? C.cyan : C.paper} stroke={C.ink} strokeWidth={4} />} />
      {open > 0.5 ? (
        <g transform={`translate(0 30) scale(${back(clamp01((open - 0.5) * 2))})`}>
          <Icon name="check" s={50} color={C.ink} sw={7} />
        </g>
      ) : (
        <Txt x={0} y={30} size={42} weight={800} anchor="middle">
          {String(n)}
        </Txt>
      )}
    </g>
  );
};

// ---------- the five checks (card centred on (0, 0), 830 x 240) ----------
const WhiteList: React.FC<{u: number}> = ({u}) => {
  const scan = eInOut(seg(u, 8, 28));
  const lx = lerp(-260, 60, scan);
  const ly = lerp(-62, 0, eInOut(seg(u, 14, 26)));
  const hl = eOut(seg(u, 26, 32));
  return (
    <g>
      <path d={roundRect(-360, -100, 500, 200, 18)} fill={C.slot} stroke={C.ink} strokeWidth={3} />
      {[-62, 0, 62].map((y, j) => (
        <g key={j}>
          {j === 1 && hl > 0 ? <rect x={-348} y={y - 26} width={476 * hl} height={52} rx={10} fill={C.cyan} opacity={0.5} /> : null}
          {j === 1 ? (
            <Txt x={-330} y={y} size={36} weight={800}>
              Ton appli
            </Txt>
          ) : (
            <rect x={-330} y={y - 7} width={j ? 260 : 320} height={14} rx={7} fill={C.grey} />
          )}
        </g>
      ))}
      <g transform={`translate(${lx} ${ly})`}>
        <line x1={34} y1={34} x2={72} y2={72} stroke={C.ink} strokeWidth={12} strokeLinecap="round" />
        <circle r={46} fill={C.light} fillOpacity={0.4} stroke={C.ink} strokeWidth={6} />
      </g>
      <g transform="translate(270 0)">
        <Hard off={4} render={(sh) => <path d={roundRect(-48, -48, 96, 96, 18)} fill={sh ? C.ink : C.paper} stroke={C.ink} strokeWidth={4} />} />
        <g transform={`scale(${back(seg(u, 30, 36))})`}>
          <Icon name="check" s={88} color={C.deep} sw={10} />
        </g>
      </g>
    </g>
  );
};

const BlackList: React.FC<{u: number}> = ({u}) => {
  const scroll = eInOut(seg(u, 6, 30)) * 300;
  return (
    <g>
      <defs>
        <clipPath id="blackwin">
          <path d={roundRect(-380, -100, 440, 200, 18)} />
        </clipPath>
      </defs>
      <path d={roundRect(-380, -100, 440, 200, 18)} fill={C.paper} stroke={C.red} strokeWidth={4} />
      <g clipPath="url(#blackwin)">
        {Array.from({length: 10}, (_, j) => {
          const y = -40 + j * 54 - scroll;
          return (
            <g key={j}>
              <circle cx={-346} cy={y} r={9} fill={C.red} />
              <rect x={-326} y={y - 8} width={[300, 240, 330, 210, 280][j % 5]} height={16} rx={8} fill={C.red} opacity={0.35} />
            </g>
          );
        })}
        <rect x={-380} y={-100} width={440} height={50} fill={C.paper} />
        <Txt x={-356} y={-74} size={36} weight={800} color={C.red}>
          Liste noire
        </Txt>
        <line x1={-380} y1={-50} x2={60} y2={-50} stroke={C.red} strokeWidth={3} />
      </g>
      <g transform="translate(240 -48)">
        <Hard off={4} render={(sh) => <path d={roundRect(-140, -36, 280, 72, 36)} fill={sh ? C.ink : C.paper} stroke={C.ink} strokeWidth={4} />} />
        <Txt x={0} y={0} size={36} weight={800} anchor="middle">
          Ton appli
        </Txt>
      </g>
      <g transform={`translate(240 50) scale(${back(seg(u, 30, 36))})`}>
        <Hard off={4} render={(sh) => <path d={roundRect(-140, -36, 280, 72, 36)} fill={sh ? C.ink : C.cyan} stroke={C.ink} strokeWidth={4} />} />
        <g transform="translate(-92 0)">
          <Icon name="check" s={40} color={C.ink} sw={6} />
        </g>
        <Txt x={22} y={0} size={36} weight={800} anchor="middle">
          Absente
        </Txt>
      </g>
    </g>
  );
};

const TwoFA: React.FC<{u: number}> = ({u}) => {
  const code = '482913';
  const shown = Math.floor(clamp01((u - 10) / 18) * 6 + 1e-6);
  return (
    <g>
      <g transform="translate(-290 0)">
        <Hard off={5} render={(sh) => <path d={roundRect(-62, -104, 124, 208, 22)} fill={sh ? C.ink : C.ink} stroke={C.ink} strokeWidth={4} />} />
        <path d={roundRect(-52, -88, 104, 170, 12)} fill={C.light} />
        <g transform={`translate(0 -4) scale(${thump(u, 30, 0.15)})`}>
          <Icon name="shield" s={70} color={C.deep} sw={6} />
        </g>
      </g>
      <g transform="translate(-160 0)">
        {[0, 1, 2].map((j) => (
          <circle key={j} cx={j * 24} cy={0} r={6} fill={C.deep} opacity={seg(u, 6 + j * 3, 9 + j * 3)} />
        ))}
      </g>
      <g transform="translate(120 0)">
        <Hard off={6} render={(sh) => <path d={roundRect(-200, -62, 400, 124, 30)} fill={sh ? C.ink : C.paper} stroke={C.ink} strokeWidth={4} />} />
        {code.split('').map((d, j) => {
          const on = j < shown;
          const x = -150 + j * 56 + (j >= 3 ? 24 : 0);
          return on ? (
            <Txt key={j} x={x} y={0} size={66} weight={800} anchor="middle" tabular>
              {d}
            </Txt>
          ) : (
            <rect key={j} x={x - 18} y={22} width={36} height={8} rx={4} fill={C.grey} />
          );
        })}
        <CheckBadge x={196} y={-58} r={30} k={back(seg(u, 30, 36))} />
      </g>
    </g>
  );
};

const Phrase: React.FC<{u: number}> = ({u}) => {
  const slash = eOut(seg(u, 10, 18));
  const fold = eInOut(seg(u, 20, 28));
  const down = eIn(seg(u, 28, 38));
  return (
    <g>
      <g transform="translate(-200 0)">
        <Hard off={5} render={(sh) => <path d={roundRect(-100, -62, 200, 132, 22)} fill={sh ? C.ink : C.paper} stroke={C.ink} strokeWidth={4} />} />
        <path d={roundRect(-40, -84, 80, 28, 8)} fill={C.grey} stroke={C.ink} strokeWidth={4} />
        <circle cx={0} cy={4} r={42} fill={C.light} stroke={C.ink} strokeWidth={5} />
        <circle cx={0} cy={4} r={18} fill={C.ink} />
        {slash > 0 ? <line x1={-110} y1={-90} x2={-110 + 220 * slash} y2={-90 + 190 * slash} stroke={C.red} strokeWidth={14} strokeLinecap="round" /> : null}
      </g>
      <g transform="translate(210 0)">
        <defs>
          <clipPath id="drawer">
            <rect x={-200} y={-200} width={400} height={262} />
          </clipPath>
        </defs>
        <g clipPath="url(#drawer)">
          <g transform={`translate(0 ${-30 + down * 170}) scale(1 ${lerp(1, 0.5, fold)})`}>
            <Hard off={4} render={(sh) => <path d={roundRect(-74, -80, 148, 160, 12)} fill={sh ? C.ink : C.paper} stroke={C.ink} strokeWidth={4} />} />
            {[0, 1, 2, 3].map((j) => (
              <rect key={j} x={-54 + (j % 2) * 58} y={-56 + Math.floor(j / 2) * 52} width={50} height={30} rx={8} fill={C.grey} stroke={C.ink} strokeWidth={2} />
            ))}
            <line x1={-74} y1={0} x2={74} y2={0} stroke={C.ink} strokeWidth={3} strokeDasharray="8 6" opacity={0.6 * (1 - fold)} />
          </g>
        </g>
        <Hard off={5} render={(sh) => <path d={roundRect(-110, 62, 220, 52, 12)} fill={sh ? C.ink : C.deep} stroke={C.ink} strokeWidth={4} />} />
        <rect x={-30} y={80} width={60} height={14} rx={7} fill={C.paper} />
        <CheckBadge x={112} y={56} r={28} k={back(seg(u, 36, 42))} />
      </g>
    </g>
  );
};

const Tag: React.FC<{x: number; flip: number; label: string; value: string}> = ({x, flip, label, value}) => {
  const sx = Math.cos(Math.PI * flip);
  const backSide = flip > 0.5;
  const body = 'M-110,-66 H150 Q160,-66 160,-56 V56 Q160,66 150,66 H-110 L-160,0 Z';
  return (
    <g transform={`translate(${x} 0) scale(${Math.max(0.02, Math.abs(sx))} 1)`}>
      <Hard off={5} render={(sh) => <path d={body} fill={sh ? C.ink : backSide ? C.light : C.paper} stroke={C.ink} strokeWidth={4} strokeLinejoin="round" />} />
      <circle cx={-118} cy={0} r={11} fill={C.bg} stroke={C.ink} strokeWidth={3} />
      {backSide ? (
        <>
          <Txt x={20} y={-26} size={36} weight={700} anchor="middle" color={C.deep}>
            {label}
          </Txt>
          <Txt x={20} y={26} size={48} weight={800} anchor="middle" tabular>
            {fr(value)}
          </Txt>
        </>
      ) : (
        <Txt x={20} y={0} size={46} weight={800} anchor="middle">
          {label}
        </Txt>
      )}
    </g>
  );
};

const Fees: React.FC<{u: number}> = ({u}) => (
  <g>
    <Tag x={-200} flip={eInOut(seg(u, 14, 24))} label="achat" value="1,5 %" />
    <Tag x={208} flip={eInOut(seg(u, 22, 32))} label="retrait" value="2,50 €" />
  </g>
);

const CHECKS = [WhiteList, BlackList, TwoFA, Phrase, Fees];

const Stage: React.FC<{s: ShortProps; f: number}> = ({s, f}) => {
  const up = eInOut(seg(f, 46, 60));
  const cy = lerp(RING_HOOK, RING_Y, up);
  const tileIn = eOut(seg(f, 3, 15));
  const tileY = lerp(cy - 500, cy, tileIn);
  const active = f >= elStart(0) && f < elStart(5) ? Math.floor((f - elStart(0)) / 60) : -1;
  const allOpen = seg(f, elStart(4) + OPEN_U, elStart(4) + OPEN_U + 8);
  const shake = f >= 16 && f < 40 ? Math.sin(f * 2.1) * 3 * (1 - seg(f, 30, 40)) : 0;
  const locks = [0, 1, 2, 3, 4].map((k) => {
    const [x, y] = lockPos(k, cy);
    const clamp = back(seg(f, 16 + 4 * k, 22 + 4 * k));
    const u = f - elStart(k);
    const open = seg(u, OPEN_U, OPEN_U + 8);
    const act = k === active ? eOut(seg(u, 0, 8)) * (1 - eInOut(seg(u, 46, 56))) : 0;
    return {k, x, y, clamp, open, act, u};
  });
  return (
    <Svg>
      {/* chains: tile -> padlock, they fall when the padlock opens */}
      {locks.map((l) =>
        l.clamp > 0.05 && l.open < 1 ? (
          <line
            key={l.k}
            x1={CX}
            y1={cy}
            x2={lerp(CX, l.x, Math.min(1, l.clamp))}
            y2={lerp(cy, l.y, Math.min(1, l.clamp)) + l.open * 60}
            stroke={C.ink}
            strokeWidth={9}
            strokeLinecap="round"
            strokeDasharray="16 10"
            opacity={1 - l.open}
          />
        ) : null,
      )}
      {/* the unknown app */}
      <g transform={`translate(${CX + shake} ${tileY}) scale(${thump(f, 15, 0.08) * thump(f, elStart(4) + OPEN_U + 4, 0.08)})`}>
        <Hard off={7} render={(sh) => <path d={roundRect(-95, -95, 190, 190, 46)} fill={sh ? C.ink : allOpen > 0.5 ? C.light : C.grey} stroke={C.ink} strokeWidth={4} />} />
        <Txt x={0} y={-6} size={118} weight={800} anchor="middle">
          ?
        </Txt>
        <g transform="translate(46 50)">
          <circle r={24} fill={C.cyan} stroke={C.ink} strokeWidth={3} />
          <Txt x={0} y={0} size={26} weight={800} anchor="middle">
            B
          </Txt>
        </g>
        <CheckBadge x={86} y={-86} r={34} k={back(seg(f, elStart(4) + OPEN_U + 6, elStart(4) + OPEN_U + 12))} />
      </g>
      {locks.map((l) =>
        l.act > 0.01 ? (
          <circle key={`p${l.k}`} cx={l.x} cy={l.y + 20} r={78 + 10 * Math.sin(l.u * 0.45)} fill={C.light} stroke={C.cyan} strokeWidth={6} opacity={l.act * (1 - l.open * 0.6)} />
        ) : null,
      )}
      {locks.map((l) => (l.clamp > 0.01 ? <Padlock key={l.k} x={l.x} y={l.y} s={l.clamp * (1 + 0.22 * l.act) * thump(l.u, OPEN_U, 0.12)} open={l.open} n={l.k + 1} /> : null))}
      {locks.map((l) => (
        <Burst key={`b${l.k}`} x={l.x} y={l.y} t={seg(l.u, OPEN_U, OPEN_U + 10)} r0={70} r1={115} color={C.deep} />
      ))}
      {active >= 0
        ? (() => {
            const u = f - elStart(active);
            const Ch = CHECKS[active];
            const on = eOut(seg(u, 4, 12)) * (1 - seg(u, 50, 58));
            return (
              <>
                <g opacity={seg(u, 3, 9) * (1 - seg(u, 50, 56))}>
                  <Txt x={CX} y={NAME_Y} size={50} weight={800} anchor="middle">
                    {fr(s.elements[active].nom)}
                  </Txt>
                </g>
                {on > 0.01 ? (
                  <g opacity={on} transform={`translate(${CX} ${CARD_Y + (1 - on) * 40})`}>
                    <Hard off={6} render={(sh) => <path d={roundRect(-415, -120, 830, 240, 28)} fill={sh ? C.ink : C.paper} stroke={C.ink} strokeWidth={4} />} />
                    <Ch u={u} />
                  </g>
                ) : null}
              </>
            );
          })()
        : null}
    </Svg>
  );
};

const Emblem: React.FC<{s: ShortProps; k: number; u: number}> = ({k}) => {
  const drop = eInOut(k);
  return (
    <g transform="translate(0 -10)">
      <path d="M-92,-30 V-62 Q-92,-76 -78,-76 H-24 L-8,-60 H78 Q92,-60 92,-46 V-30 Z" fill={C.grey} stroke={C.ink} strokeWidth={4} strokeLinejoin="round" />
      <g transform={`translate(0 ${lerp(-170, -46, drop)})`}>
        <Hard off={4} render={(sh) => <path d={roundRect(-56, -56, 112, 112, 28)} fill={sh ? C.ink : C.light} stroke={C.ink} strokeWidth={4} />} />
        <Txt x={0} y={-4} size={66} weight={800} anchor="middle">
          ?
        </Txt>
      </g>
      <Hard off={6} render={(sh) => <path d={roundRect(-92, -24, 184, 130, 26)} fill={sh ? C.ink : C.slot} stroke={C.ink} strokeWidth={4} />} />
      <g transform="translate(0 42) scale(0.55)">
        <Padlock x={0} y={-18} s={1} open={1} n={5} />
      </g>
      <Txt x={0} y={150} size={36} weight={800} anchor="middle">
        5/5
      </Txt>
      <CheckBadge x={88} y={-20} r={26} k={back(seg(k, 0.7, 1))} />
    </g>
  );
};

export const locks: DeviceSpec = {
  Stage,
  Emblem,
  roleTop: 1160,
  hookCard: true,
  finAlert: true,
  recap: (s) => s.elements.map((e) => ({label: e.nom, mark: 'check'})),
};
