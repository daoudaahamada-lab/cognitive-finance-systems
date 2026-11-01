// S01 — the phone's « Finances » folder: it opens into the bottom dock; each app jumps out, grows in the centre, shows
// what it does in one gesture, then goes back to its slot with a check. End: the folder closed with the 5 inside.
import React from 'react';
import {Hard, Icon, roundRect, Txt} from '../../story/draw';
import {back, Burst, C, CheckBadge, Coin, CX, DOCK, dockSlot, eIn, eInOut, elStart, eOut, fr, lerp, Panel, seg, Svg, thump, Tile} from '../kit';
import type {DeviceSpec, ShortProps} from '../types';

const CLOSED = {x: CX - 160, y: 600, w: 320, h: 320, r: 76};
const gridPos = (k: number): [number, number] => [CX - 98 + (k % 3) * 98, CLOSED.y + 112 + Math.floor(k / 3) * 96];
const STAGE_Y = 440; // centre of the big tile
const BIG = 200;

const colorOf = (s: ShortProps, k: number) => s.elements[k]?.couleur ?? C.cyan;

/** Partial polyline (fraction t of its length). */
const partial = (pts: [number, number][], t: number): [number, number][] => {
  const lens = pts.slice(1).map((p, k) => Math.hypot(p[0] - pts[k][0], p[1] - pts[k][1]));
  const total = lens.reduce((a, b) => a + b, 0);
  let left = total * t;
  const out: [number, number][] = [pts[0]];
  for (let k = 0; k < lens.length; k++) {
    if (left >= lens[k]) {
      out.push(pts[k + 1]);
      left -= lens[k];
    } else {
      const r = lens[k] > 0 ? left / lens[k] : 0;
      out.push([lerp(pts[k][0], pts[k + 1][0], r), lerp(pts[k][1], pts[k + 1][1], r)]);
      break;
    }
  }
  return out;
};
const toD = (pts: [number, number][]) => pts.map((p, k) => `${k ? 'L' : 'M'}${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(' ');

// ---------- the five gestures (local frame u of the element) ----------
const Basket: React.FC<{u: number}> = ({u}) => {
  const sq = thump(u, 24, 0.07);
  const coinT = seg(u, 12, 24);
  const coinY = lerp(690, 905, eIn(coinT));
  return (
    <g>
      {[-100, 0, 100].map((dx, k) => {
        const rise = eOut(seg(u, 24 + 2 * k, 34 + 2 * k)) * -34;
        return (
          <g key={k} transform={`translate(${CX + dx} ${840 + rise})`}>
            <Hard off={4} render={(sh) => <path d={roundRect(-48, -55, 96, 110, 16)} fill={sh ? C.ink : C.paper} stroke={C.ink} strokeWidth={3.5} />} />
            <path d="M-32,22 L-12,4 L6,12 L32,-30" fill="none" stroke={k === 1 ? C.deep : C.cyan} strokeWidth={7} strokeLinecap="round" strokeLinejoin="round" />
          </g>
        );
      })}
      {coinT > 0 && u < 26 ? <Coin x={CX + 10} y={coinY} r={40} /> : null}
      <g transform={`translate(${CX} 950) scale(${2 - sq} ${sq}) translate(${-CX} -950)`}>
        <Hard off={6} render={(sh) => <path d={`M${CX - 160},880 L${CX + 160},880 L${CX + 125},1022 L${CX - 125},1022 Z`} fill={sh ? C.ink : C.paper} stroke={C.ink} strokeWidth={4} strokeLinejoin="round" />} />
        {[918, 954, 990].map((y) => (
          <line key={y} x1={CX - 150 + (y - 880) * 0.25} y1={y} x2={CX + 150 - (y - 880) * 0.25} y2={y} stroke={C.ink} strokeWidth={2.5} opacity={0.35} />
        ))}
        {[-90, -30, 30, 90].map((dx) => (
          <line key={dx} x1={CX + dx} y1={892} x2={CX + dx * 0.8} y2={1018} stroke={C.ink} strokeWidth={2.5} opacity={0.35} />
        ))}
        <path d={roundRect(CX - 172, 866, 344, 26, 13)} fill={C.deep} stroke={C.ink} strokeWidth={4} />
      </g>
      <Burst x={CX} y={872} t={seg(u, 24, 36)} r0={70} r1={130} />
    </g>
  );
};

const PriceCard: React.FC<{x: number; y: number; text: string; k: number; fill: string}> = ({x, y, text, k, fill}) =>
  k <= 0.01 ? null : (
    <g transform={`translate(${x} ${y}) scale(${k})`}>
      <Hard off={5} render={(sh) => <path d={roundRect(-120, -48, 240, 96, 26)} fill={sh ? C.ink : fill} stroke={C.ink} strokeWidth={4} />} />
      <Txt x={0} y={0} size={48} weight={800} anchor="middle" tabular>
        {fr(text)}
      </Txt>
    </g>
  );

const RoundUp: React.FC<{u: number}> = ({u}) => {
  const fly = eInOut(seg(u, 24, 36));
  const chipOn = u >= 21 && u < 37;
  const cx = lerp(CX + 190, CX, fly);
  const cy = lerp(880, 975, fly) - Math.sin(Math.PI * fly) * 40;
  const cs = lerp(1, 0.35, eIn(fly)) * back(seg(u, 20, 25));
  const coinK = back(seg(u, 16, 24)) * thump(u, 36, 0.12);
  return (
    <g>
      <PriceCard x={CX - 190} y={790} text="4,60 €" k={back(seg(u, 8, 14))} fill={C.paper} />
      <g opacity={seg(u, 12, 16)} transform={`translate(${CX} 790)`}>
        <Icon name="arrow" s={56} color={C.ink} sw={6} />
      </g>
      <PriceCard x={CX + 190} y={790} text="5,00 €" k={back(seg(u, 15, 21))} fill={C.light} />
      <g transform={`translate(${CX} 975) scale(${coinK})`}>{coinK > 0.01 ? <Coin x={0} y={0} r={62} letter="B" /> : null}</g>
      {chipOn ? (
        <g transform={`translate(${cx} ${cy}) scale(${cs})`}>
          <Hard off={4} render={(sh) => <path d={roundRect(-100, -36, 200, 72, 36)} fill={sh ? C.ink : C.cyan} stroke={C.ink} strokeWidth={4} />} />
          <Txt x={0} y={0} size={40} weight={800} anchor="middle" tabular>
            {fr('0,40 €')}
          </Txt>
        </g>
      ) : null}
      <Burst x={CX} y={975} t={seg(u, 36, 46)} r0={74} r1={124} />
    </g>
  );
};

const Safe: React.FC<{u: number}> = ({u}) => {
  const sx = CX + 80;
  const sy = 875;
  const close = eInOut(seg(u, 24, 32));
  const doorScale = lerp(-0.55, 1, close);
  const keyT = eOut(seg(u, 8, 22));
  const kx = lerp(CX - 300, sx - 40, keyT);
  const sq = thump(u, 32, 0.06);
  const dial = eInOut(seg(u, 32, 42)) * 140;
  return (
    <g>
      <g transform={`translate(${sx} ${sy}) scale(${2 - sq} ${sq})`}>
        <Hard off={6} render={(sh) => <path d={roundRect(-140, -122, 280, 244, 26)} fill={sh ? C.ink : C.grey} stroke={C.ink} strokeWidth={4} />} />
        <path d={roundRect(-115, -100, 230, 200, 16)} fill={C.ink} />
        <rect x={-100} y={80} width={36} height={52} rx={6} fill={C.ink} />
        <rect x={64} y={80} width={36} height={52} rx={6} fill={C.ink} />
      </g>
      {u < 33 ? (
        <g transform={`translate(${kx} ${sy})`}>
          <Hard
            off={4}
            render={(sh) => (
              <g fill={sh ? C.ink : C.cyan} stroke={C.ink} strokeWidth={4} strokeLinejoin="round">
                <circle cx={-80} cy={0} r={32} />
                <path d="M-50,-10 H60 V10 H40 V30 H24 V10 H8 V24 H-8 V10 H-50 Z" />
              </g>
            )}
          />
          <circle cx={-80} cy={0} r={11} fill={C.bg} stroke={C.ink} strokeWidth={3} />
        </g>
      ) : null}
      <g transform={`translate(${sx + 115} ${sy}) scale(${doorScale * (2 - sq)} ${sq}) translate(-115 0)`}>
        <Hard off={doorScale > 0 ? 5 : 0} render={(sh) => <path d={roundRect(-115, -100, 230, 200, 16)} fill={sh ? C.ink : doorScale > 0 ? C.light : C.paper} stroke={C.ink} strokeWidth={4} />} />
        {doorScale > 0.2 ? (
          <g transform={`rotate(${dial})`}>
            <circle r={50} fill={C.paper} stroke={C.ink} strokeWidth={4} />
            {[0, 60, 120, 180, 240, 300].map((a) => (
              <line key={a} x1={0} y1={0} x2={0} y2={-38} stroke={C.ink} strokeWidth={4} strokeLinecap="round" transform={`rotate(${a})`} />
            ))}
            <circle r={12} fill={C.deep} stroke={C.ink} strokeWidth={3} />
          </g>
        ) : null}
      </g>
      <CheckBadge x={sx + 128} y={sy - 112} r={30} k={back(seg(u, 36, 42))} />
    </g>
  );
};

const NETS: [number, number][] = [
  [CX - 285, 960],
  [CX, 712],
  [CX + 285, 960],
];
const Net: React.FC<{x: number; y: number; k: number}> = ({x, y, k}) =>
  k <= 0.01 ? null : (
    <g transform={`translate(${x} ${y}) scale(${k})`}>
      <circle r={50} fill={C.paper} stroke={C.ink} strokeWidth={3} strokeDasharray="8 7" />
      {[0, 1, 2].map((j) => {
        const a = -Math.PI / 2 + (j * 2 * Math.PI) / 3;
        const b = -Math.PI / 2 + (((j + 1) % 3) * 2 * Math.PI) / 3;
        return <line key={`l${j}`} x1={Math.cos(a) * 28} y1={Math.sin(a) * 28} x2={Math.cos(b) * 28} y2={Math.sin(b) * 28} stroke={C.ink} strokeWidth={4} />;
      })}
      {[0, 1, 2].map((j) => {
        const a = -Math.PI / 2 + (j * 2 * Math.PI) / 3;
        return <circle key={j} cx={Math.cos(a) * 28} cy={Math.sin(a) * 28} r={13} fill={C.cyan} stroke={C.ink} strokeWidth={3.5} />;
      })}
    </g>
  );

const Wallet: React.FC<{u: number}> = ({u}) => {
  const sq = thump(u, 20, 0.05) * thump(u, 26, 0.05) * thump(u, 32, 0.05);
  return (
    <g>
      {NETS.map(([nx, ny], j) => {
        const t = eInOut(seg(u, 12 + 6 * j, 20 + 6 * j));
        const ax = CX + Math.sign(nx - CX) * 110;
        const ay = ny < 860 ? 790 : 900;
        const bx = lerp(ax, nx, t);
        const by = lerp(ay, ny, t);
        return t > 0 ? <line key={j} x1={ax} y1={ay} x2={bx} y2={by} stroke={C.deep} strokeWidth={7} strokeLinecap="round" strokeDasharray="2 14" /> : null;
      })}
      {NETS.map(([nx, ny], j) => (
        <Net key={j} x={nx} y={ny} k={back(seg(u, 19 + 6 * j, 25 + 6 * j))} />
      ))}
      <g transform={`translate(${CX} 860) scale(${sq})`}>
        <Hard off={6} render={(sh) => <path d={roundRect(-115, -75, 230, 150, 24)} fill={sh ? C.ink : C.paper} stroke={C.ink} strokeWidth={4} />} />
        <path d={roundRect(-115, -75, 230, 40, 20)} fill={C.grey} stroke={C.ink} strokeWidth={4} />
        <Hard off={3} render={(sh) => <path d={roundRect(30, -22, 100, 64, 18)} fill={sh ? C.ink : C.cyan} stroke={C.ink} strokeWidth={4} />} />
        <circle cx={62} cy={10} r={10} fill={C.paper} stroke={C.ink} strokeWidth={3} />
      </g>
    </g>
  );
};

const CURVE: [number, number][] = [
  [-260, 70],
  [-200, 40],
  [-140, 55],
  [-80, 5],
  [-20, 25],
  [40, -25],
  [100, -5],
  [160, -55],
  [220, -40],
  [262, -85],
];
const Watch: React.FC<{u: number}> = ({u}) => {
  const t = eInOut(seg(u, 10, 40));
  const pts = partial(CURVE, t);
  const tip = pts[pts.length - 1];
  return (
    <g transform={`translate(${CX} 865)`}>
      <Hard off={6} render={(sh) => <path d={roundRect(-310, -150, 620, 300, 26)} fill={sh ? C.ink : C.paper} stroke={C.ink} strokeWidth={4} />} />
      {[-80, -10, 60].map((y) => (
        <line key={y} x1={-280} y1={y} x2={280} y2={y} stroke={C.rule} strokeWidth={3} />
      ))}
      <path d={toD(pts)} fill="none" stroke={C.deep} strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" />
      <circle cx={tip[0]} cy={tip[1]} r={10} fill={C.cyan} stroke={C.ink} strokeWidth={3} />
      <g transform={`translate(${tip[0] + 6} ${tip[1] + 4})`}>
        <line x1={38} y1={38} x2={84} y2={84} stroke={C.ink} strokeWidth={14} strokeLinecap="round" />
        <circle r={56} fill={C.light} fillOpacity={0.45} stroke={C.ink} strokeWidth={7} />
      </g>
    </g>
  );
};

const GESTURES = [Basket, RoundUp, Safe, Wallet, Watch];

const Stage: React.FC<{s: ShortProps; f: number}> = ({s, f}) => {
  // Hook: the closed folder pops in, is tapped (squish + ring), then opens into the dock.
  const pop = back(seg(f, 2, 14));
  const tap = thump(f, 16, 0.08, 10);
  const ko = eInOut(seg(f, 24, 44));
  const rect = {
    x: lerp(CLOSED.x, DOCK.x, ko),
    y: lerp(CLOSED.y, DOCK.y, ko),
    w: lerp(CLOSED.w, DOCK.w, ko),
    h: lerp(CLOSED.h, DOCK.h, ko),
    r: lerp(CLOSED.r, DOCK.r, ko),
  };
  const fcx = rect.x + rect.w / 2;
  const fcy = rect.y + rect.h / 2;
  const sc = (ko > 0 ? 1 : pop) * tap;
  const ring = seg(f, 16, 32);
  const active = f >= elStart(0) && f < elStart(5) ? Math.floor((f - elStart(0)) / 60) : -1;
  const tiles = s.elements.slice(0, 5).map((el, k) => {
    const [gx, gy] = gridPos(k);
    const [dx, dy] = dockSlot(k);
    const hx = lerp(gx, dx, ko);
    const hy = lerp(gy, dy, ko);
    const hs = lerp(78, DOCK.tile, ko);
    const u = f - elStart(k);
    let x = hx;
    let y = hy;
    let size = hs;
    if (k === active) {
      const a = seg(u, 0, 11);
      const r = eInOut(seg(u, 46, 58));
      const ox = lerp(hx, CX, eOut(a));
      const oy = lerp(hy, STAGE_Y, eOut(a)) - Math.sin(Math.PI * a) * 120;
      const os = lerp(hs, BIG, back(a, 1.4));
      x = lerp(ox, hx, r);
      y = lerp(oy, hy, r) - Math.sin(Math.PI * r) * 80;
      size = lerp(os, hs, r);
    }
    const badge = f >= elStart(k) + 54 ? back(seg(u, 54, 60)) : 0;
    return {el, k, x, y, size, badge, color: colorOf(s, k), u};
  });
  return (
    <Svg>
      {ring > 0 && ring < 1 ? <circle cx={CX} cy={CLOSED.y + CLOSED.h / 2} r={lerp(175, 250, eOut(ring))} fill="none" stroke={C.cyan} strokeWidth={8} opacity={1 - ring} /> : null}
      <g transform={`translate(${fcx} ${fcy}) scale(${sc}) translate(${-fcx} ${-fcy})`}>
        <Panel x={rect.x} y={rect.y} w={rect.w} h={rect.h} r={rect.r} fill={C.slot} />
        <g opacity={1 - seg(f, 22, 30)}>
          <Txt x={CX} y={CLOSED.y + CLOSED.h + 52} size={46} weight={800} anchor="middle">
            Finances
          </Txt>
        </g>
        <g opacity={seg(f, 40, 48)}>
          <Txt x={DOCK.x + 34} y={DOCK.y + 44} size={38} weight={800}>
            Finances
          </Txt>
        </g>
        {tiles.map((t) =>
          t.k === active && t.u > 1 && t.u < 58 ? <Tile key={`d${t.k}`} x={dockSlot(t.k)[0]} y={dockSlot(t.k)[1]} s={DOCK.tile} color={C.cyan} dashed /> : null,
        )}
        {tiles.map((t) => (t.k === active ? null : <Tile key={t.k} x={t.x} y={t.y} s={t.size} color={t.color} name={t.el.nom} badge={t.k < active || active < 0 ? (f >= elStart(t.k) + 54 ? 1 : 0) : t.badge} />))}
      </g>
      {active >= 0
        ? (() => {
            const t = tiles[active];
            const G = GESTURES[active];
            const gOp = seg(t.u, 8, 14) * (1 - seg(t.u, 44, 52));
            const nameOp = seg(t.u, 5, 11) * (1 - seg(t.u, 44, 50));
            return (
              <>
                {gOp > 0.01 ? (
                  <g opacity={gOp}>
                    <G u={t.u} />
                  </g>
                ) : null}
                <g opacity={nameOp}>
                  <Txt x={CX} y={STAGE_Y + BIG / 2 + 46} size={50} weight={800} anchor="middle">
                    {fr(t.el.nom)}
                  </Txt>
                </g>
                <Tile x={t.x} y={t.y} s={t.size} color={t.color} name={t.el.nom} badge={t.badge} />
              </>
            );
          })()
        : null}
    </Svg>
  );
};

const Emblem: React.FC<{s: ShortProps; k: number; u: number}> = ({s, k}) => {
  const close = eInOut(k);
  return (
    <g transform="translate(0 -20)">
      <Hard off={6} render={(sh) => <path d={roundRect(-90, -90, 180, 180, 44)} fill={sh ? C.ink : C.slot} stroke={C.ink} strokeWidth={4} />} />
      {s.elements.slice(0, 5).map((el, j) => {
        const tx = -50 + (j % 3) * 50;
        const ty = -26 + Math.floor(j / 3) * 52;
        const fx = (j - 2) * 40;
        return <Tile key={j} x={lerp(fx, tx, close)} y={lerp(-180, ty, close)} s={lerp(70, 42, close)} color={el.couleur ?? C.cyan} name={el.nom} label="" opacity={Math.min(1, k * 3)} />;
      })}
      <Txt x={0} y={130} size={36} weight={800} anchor="middle">
        Finances
      </Txt>
      <CheckBadge x={84} y={-84} r={26} k={back(seg(k, 0.7, 1))} />
    </g>
  );
};

export const folder: DeviceSpec = {
  Stage,
  Emblem,
  roleTop: 1075,
  hookCard: true,
  finAlert: true,
  recap: (s) => s.elements.map((e) => ({label: e.nom, mark: 'tile', color: e.couleur})),
};
