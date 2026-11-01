// S02 — a messy pile of papers becomes one clean sheet: the « Productivity » folder opens into the dock; each AI rises,
// points a cyan beam at the pile, pulls out one clean object (total, source, table, contract, reminder) that lands as
// a line of « Ma fiche ». Claude first. End: the pile is gone, the one-page sheet remains.
import React from 'react';
import {Hard, Icon, roundRect, Txt} from '../../story/draw';
import {back, Burst, C, CheckBadge, CX, DOCK, dockSlot, eInOut, elStart, eOut, fr, lerp, Panel, seg, Sheet, Svg, thump, Tile} from '../kit';
import type {DeviceSpec, ShortProps} from '../types';

const PILE_HOOK = {x: CX, y: 740, s: 1.15};
const PILE = {x: 228, y: 478, s: 0.8};
const FICHE = {x: 430, y: 258, w: 474, h: 444};
const ROW_Y = (k: number) => FICHE.y + 128 + k * 64;
const FICHE_ROWS = [
  {label: 'Frais repérés', icon: 'euro'},
  {label: 'Règle vérifiée', icon: 'check'},
  {label: 'Budget 3 mois', icon: 'bars'},
  {label: 'Contrat retrouvé', icon: 'mail'},
  {label: 'Point dimanche', icon: 'cal'},
];
const AI = {x: 182, y: 868, s: 150};
const OBJ = {x: 628, y: 885, w: 540, h: 300};

// Papers of the pile, bottom to top; the top one leaves first (element 0 takes paper 4).
const PAPERS = [
  {dx: 20, dy: 30, rot: 9, label: ''},
  {dx: -26, dy: 12, rot: -11, label: 'Facture'},
  {dx: 30, dy: -6, rot: 6, label: ''},
  {dx: -14, dy: -18, rot: -5, label: 'Contrat'},
  {dx: 8, dy: -30, rot: 3, label: 'Relevé'},
];

const colorOf = (s: ShortProps, k: number) => s.elements[k]?.couleur ?? C.cyan;

// ---------- the five clean objects (centred on (0, 0), card 540 x 300) ----------
const Card: React.FC<{children: React.ReactNode; title: string}> = ({children, title}) => (
  <g>
    <Hard off={6} render={(sh) => <path d={roundRect(-OBJ.w / 2, -OBJ.h / 2, OBJ.w, OBJ.h, 26)} fill={sh ? C.ink : C.paper} stroke={C.ink} strokeWidth={4} />} />
    <Txt x={-OBJ.w / 2 + 30} y={-OBJ.h / 2 + 40} size={36} weight={800} color={C.deep}>
      {fr(title)}
    </Txt>
    {children}
  </g>
);

const Fees: React.FC<{u: number}> = ({u}) => {
  const rows = [
    ['Frais de tenue', '2,00 €'],
    ['Commission', '8,50 €'],
    ['Frais carte', '4,00 €'],
  ];
  return (
    <Card title="Relevé">
      {rows.map(([a, b], k) => {
        const y = -40 + k * 68;
        const hl = eOut(seg(u, 24 + 6 * k, 30 + 6 * k));
        return (
          <g key={k}>
            {hl > 0 ? <rect x={-250} y={y - 28} width={500 * hl} height={56} rx={12} fill={C.cyan} opacity={0.55} /> : null}
            <Txt x={-236} y={y} size={36} weight={700}>
              {fr(a)}
            </Txt>
            <Txt x={236} y={y} size={36} weight={800} anchor="end" tabular>
              {fr(b)}
            </Txt>
          </g>
        );
      })}
    </Card>
  );
};

const Source: React.FC<{u: number}> = ({u}) => {
  const tick = back(seg(u, 32, 38));
  return (
    <Card title="Règle">
      <g opacity={seg(u, 20, 26)}>
        <Txt x={-236} y={-30} size={40} weight={800}>
          {fr('Plafond PEA : 150 000 €')}
        </Txt>
      </g>
      <g transform={`translate(-60 70) scale(${back(seg(u, 24, 30))})`}>
        <Hard off={4} render={(sh) => <path d={roundRect(-150, -36, 300, 72, 36)} fill={sh ? C.ink : C.light} stroke={C.ink} strokeWidth={4} />} />
        <g transform="translate(-104 0)">
          <Icon name="arrow" s={34} color={C.deep} sw={4} />
        </g>
        <Txt x={18} y={0} size={38} weight={800} anchor="middle" color={C.deep}>
          source
        </Txt>
      </g>
      <g transform={`translate(160 70)`}>
        <path d={roundRect(-34, -34, 68, 68, 14)} fill={C.paper} stroke={C.ink} strokeWidth={4} />
        {tick > 0.01 ? (
          <g transform={`scale(${tick})`}>
            <Icon name="check" s={64} color={C.deep} sw={9} />
          </g>
        ) : null}
      </g>
    </Card>
  );
};

const Table: React.FC<{u: number}> = ({u}) => {
  const cols = [
    ['Janv.', 120, '+120 €'],
    ['Févr.', 80, '+80 €'],
    ['Mars', 150, '+150 €'],
  ] as const;
  return (
    <Card title="Budget">
      {cols.map(([m, v, t], k) => {
        const x = -150 + k * 170;
        const g = eOut(seg(u, 22 + 6 * k, 30 + 6 * k));
        const hgt = (v / 150) * 120 * g;
        return (
          <g key={k}>
            <Txt x={x} y={-62} size={36} weight={700} anchor="middle">
              {m}
            </Txt>
            <line x1={x - 60} y1={128} x2={x + 60} y2={128} stroke={C.ink} strokeWidth={3} />
            {hgt > 1 ? <rect x={x - 38} y={128 - hgt} width={76} height={hgt} rx={8} fill={k === 2 ? C.deep : C.cyan} stroke={C.ink} strokeWidth={3} /> : null}
            <g opacity={seg(u, 28 + 6 * k, 32 + 6 * k)}>
              <Txt x={x} y={128 - hgt - 28} size={36} weight={800} anchor="middle" tabular>
                {fr(t)}
              </Txt>
            </g>
          </g>
        );
      })}
    </Card>
  );
};

const Mail: React.FC<{u: number}> = ({u}) => {
  const open = eInOut(seg(u, 20, 27));
  const out = eOut(seg(u, 27, 40));
  return (
    <Card title="Mails">
      <g transform="translate(-110 0)">
        <g transform={`translate(${out * 230} ${-out * 30}) rotate(${out * 6})`} opacity={seg(u, 25, 28)}>
          <Hard off={5} render={(sh) => <path d={roundRect(-80, -100 + (1 - out) * 60, 160, 190, 12)} fill={sh ? C.ink : C.paper} stroke={C.ink} strokeWidth={4} />} />
          <rect x={-56} y={-86 + (1 - out) * 60} width={112} height={50} rx={10} fill={C.cyan} stroke={C.ink} strokeWidth={3} />
          <Txt x={0} y={-61 + (1 - out) * 60} size={36} weight={800} anchor="middle">
            PDF
          </Txt>
          <Txt x={0} y={20 + (1 - out) * 60} size={36} weight={800} anchor="middle">
            Contrat
          </Txt>
        </g>
        <Hard off={5} render={(sh) => <path d={roundRect(-120, -10, 240, 150, 14)} fill={sh ? C.ink : C.light} stroke={C.ink} strokeWidth={4} />} />
        <path d={`M-120,-10 L0,${lerp(70, -90, open)} L120,-10`} fill={open > 0.5 ? C.light : C.paper} stroke={C.ink} strokeWidth={4} strokeLinejoin="round" />
        <path d="M-120,140 L-20,60 M120,140 L20,60" stroke={C.ink} strokeWidth={3} opacity={0.5} />
      </g>
    </Card>
  );
};

const Bell: React.FC<{u: number}> = ({u}) => {
  const days = ['L', 'M', 'M', 'J', 'V', 'S', 'D'];
  const circle = eInOut(seg(u, 26, 36));
  const swing = u > 20 && u < 46 ? Math.sin((u - 20) * 0.9) * 16 * (1 - seg(u, 36, 46)) : 0;
  const dx = -207 + 6 * 69;
  return (
    <Card title="Rappel">
      <g transform={`translate(196 -88) rotate(${swing})`}>
        <path d="M-30,18 C-30,-14 -22,-36 0,-36 C22,-36 30,-14 30,18 L38,28 H-38 Z" fill={C.cyan} stroke={C.ink} strokeWidth={4} strokeLinejoin="round" />
        <circle cx={0} cy={36} r={9} fill={C.ink} />
      </g>
      {swing !== 0
        ? [1, -1].map((sg) => <path key={sg} d={`M${196 + sg * 52},-118 q${sg * 14},26 0,52`} fill="none" stroke={C.ink} strokeWidth={4} strokeLinecap="round" opacity={0.7} />)
        : null}
      {days.map((d, k) => (
        <g key={k}>
          <path d={roundRect(-207 + k * 69 - 30, 10, 60, 92, 12)} fill={k === 6 ? C.light : C.slot} stroke={C.ink} strokeWidth={3} />
          <Txt x={-207 + k * 69} y={56} size={36} weight={800} anchor="middle">
            {d}
          </Txt>
        </g>
      ))}
      {circle > 0 ? (
        <circle cx={dx} cy={56} r={50} fill="none" stroke={C.deep} strokeWidth={7} strokeDasharray={`${circle * 315} 400`} transform={`rotate(-90 ${dx} 56)`} strokeLinecap="round" />
      ) : null}
    </Card>
  );
};

const OBJECTS = [Fees, Source, Table, Mail, Bell];

const Fiche: React.FC<{f: number; on: number}> = ({f, on}) => (
  <g opacity={on} transform={`translate(0 ${(1 - on) * -40})`}>
    <Hard off={6} render={(sh) => <path d={roundRect(FICHE.x, FICHE.y, FICHE.w, FICHE.h, 26)} fill={sh ? C.ink : C.paper} stroke={C.ink} strokeWidth={4} />} />
    <Txt x={FICHE.x + 30} y={FICHE.y + 50} size={40} weight={800}>
      Ma fiche
    </Txt>
    <line x1={FICHE.x + 30} y1={FICHE.y + 86} x2={FICHE.x + FICHE.w - 30} y2={FICHE.y + 86} stroke={C.ink} strokeWidth={3} />
    {FICHE_ROWS.map((r, k) => {
      const t0 = elStart(k) + 48;
      const k1 = eOut(seg(f, t0, t0 + 8));
      const y = ROW_Y(k);
      return (
        <g key={k}>
          {k1 < 1 ? <rect x={FICHE.x + 30} y={y - 6} width={FICHE.w - 60} height={12} rx={6} fill={C.rule} /> : null}
          {k1 > 0 ? (
            <g opacity={k1}>
              <g transform={`translate(${FICHE.x + 52} ${y}) scale(${back(seg(f, t0, t0 + 6))})`}>
                <Hard off={3} render={(sh) => <circle r={21} fill={sh ? C.ink : C.cyan} stroke={C.ink} strokeWidth={3} />} />
                <Icon name={r.icon} s={26} color={C.ink} sw={3} />
              </g>
              <Txt x={FICHE.x + 88 + (1 - k1) * 20} y={y} size={36} weight={700}>
                {fr(r.label)}
              </Txt>
            </g>
          ) : null}
        </g>
      );
    })}
  </g>
);

const Stage: React.FC<{s: ShortProps; f: number}> = ({s, f}) => {
  const move = eInOut(seg(f, 46, 60));
  const px = lerp(PILE_HOOK.x, PILE.x, move);
  const py = lerp(PILE_HOOK.y, PILE.y, move);
  const ps = lerp(PILE_HOOK.s, PILE.s, move) * back(seg(f, 2, 14), 1.2);
  const shake = f < 46 ? Math.sin(f * 1.3) * 2 * seg(f, 10, 20) * (1 - seg(f, 36, 46)) : 0;
  const ko = eInOut(seg(f, 22, 40));
  const dockOn = seg(f, 18, 26);
  const active = f >= elStart(0) && f < elStart(5) ? Math.floor((f - elStart(0)) / 60) : -1;
  return (
    <Svg>
      {/* Productivity dock (folder opening upward from a small folder) */}
      <g opacity={dockOn} transform={`translate(${CX} ${DOCK.y + DOCK.h / 2}) scale(${lerp(0.3, 1, ko)} ${lerp(0.6, 1, ko)}) translate(${-CX} ${-(DOCK.y + DOCK.h / 2)})`}>
        <Panel x={DOCK.x} y={DOCK.y} w={DOCK.w} h={DOCK.h} r={DOCK.r} />
      </g>
      <g opacity={seg(f, 34, 42)}>
        <Txt x={DOCK.x + 34} y={DOCK.y + 44} size={38} weight={800}>
          Productivity
        </Txt>
      </g>
      {s.elements.slice(0, 5).map((el, k) => {
        const [sx, sy] = dockSlot(k);
        const inK = back(seg(f, 30 + 3 * k, 38 + 3 * k));
        const u = f - elStart(k);
        if (k === active) {
          return u > 1 && u < 58 ? <Tile key={k} x={sx} y={sy} s={DOCK.tile} color={C.cyan} dashed /> : null;
        }
        if (inK <= 0.01) return null;
        return <Tile key={k} x={sx} y={sy} s={DOCK.tile * inK} color={colorOf(s, k)} name={el.nom} badge={f >= elStart(k) + 54 ? 1 : 0} />;
      })}
      <Fiche f={f} on={eOut(seg(f, 52, 62))} />
      {/* the pile: papers still there */}
      <g transform={`translate(${px + shake} ${py}) scale(${ps})`}>
        {PAPERS.map((p, j) => {
          const owner = 4 - j; // element that takes this paper
          const t0 = elStart(owner) + 16;
          if (f >= t0) return null;
          return (
            <Sheet key={j} x={p.dx} y={p.dy} w={210} h={270} rot={p.rot} lines={p.label ? 3 : 5}>
              {p.label ? (
                <Txt x={0} y={-82} size={46} weight={800} anchor="middle">
                  {p.label}
                </Txt>
              ) : null}
            </Sheet>
          );
        })}
      </g>
      {active >= 0
        ? (() => {
            const k = active;
            const u = f - elStart(k);
            const el = s.elements[k];
            const [sx, sy] = dockSlot(k);
            const a = seg(u, 0, 11);
            const r = eInOut(seg(u, 46, 58));
            const ox = lerp(sx, AI.x, eOut(a));
            const oy = lerp(sy, AI.y, eOut(a)) - Math.sin(Math.PI * a) * 90;
            const os = lerp(DOCK.tile, AI.s, back(a, 1.4));
            const tx = lerp(ox, sx, r);
            const ty = lerp(oy, sy, r) - Math.sin(Math.PI * r) * 60;
            const ts = lerp(os, DOCK.tile, r);
            const beam = seg(u, 9, 14) * (1 - seg(u, 24, 30));
            const flick = 0.75 + 0.25 * Math.sin(u * 1.7);
            const Obj = OBJECTS[k];
            // object: out of the pile (u 16-26), shows its gesture, then shrinks into the sheet row (u 44-54)
            const go = eOut(seg(u, 16, 26));
            const back2 = eInOut(seg(u, 44, 54));
            const bx = lerp(lerp(PILE.x, OBJ.x, go), FICHE.x + 260, back2);
            const by = lerp(lerp(PILE.y, OBJ.y, go), ROW_Y(k), back2);
            const bs = lerp(lerp(0.3, 1, go), 0.12, back2);
            const objOn = u >= 16 && u < 54;
            return (
              <>
                {beam > 0.01 ? (
                  <g opacity={beam * flick}>
                    <polygon points={`${tx - 40},${ty - ts / 2 + 6} ${tx + 40},${ty - ts / 2 + 6} ${PILE.x + 120},${PILE.y + 70} ${PILE.x - 110},${PILE.y + 70}`} fill={C.cyan} opacity={0.4} />
                    <line x1={tx - 40} y1={ty - ts / 2 + 6} x2={PILE.x - 110} y2={PILE.y + 70} stroke={C.deep} strokeWidth={4} />
                    <line x1={tx + 40} y1={ty - ts / 2 + 6} x2={PILE.x + 120} y2={PILE.y + 70} stroke={C.deep} strokeWidth={4} />
                  </g>
                ) : null}
                <Burst x={PILE.x} y={PILE.y} t={seg(u, 15, 25)} r0={90} r1={150} color={C.deep} />
                {objOn ? (
                  <g transform={`translate(${bx} ${by}) scale(${bs})`} opacity={1 - seg(u, 50, 54)}>
                    <Obj u={u} />
                  </g>
                ) : null}
                <g opacity={seg(u, 5, 11) * (1 - seg(u, 44, 50))}>
                  <Txt x={AI.x} y={AI.y + AI.s / 2 + 40} size={42} weight={800} anchor="middle">
                    {fr(el.nom)}
                  </Txt>
                </g>
                <g transform={`translate(${tx} ${ty}) scale(${thump(u, 12, 0.08)}) translate(${-tx} ${-ty})`}>
                  <Tile x={tx} y={ty} s={ts} color={colorOf(s, k)} name={el.nom} badge={u >= 54 ? back(seg(u, 54, 60)) : 0} />
                </g>
              </>
            );
          })()
        : null}
      {/* end of the series: the empty spot where the pile was gets a check */}
      <CheckBadge x={PILE.x} y={PILE.y} r={40} k={back(seg(f, elStart(4) + 30, elStart(4) + 38)) * (1 - seg(f, elStart(4) + 54, elStart(4) + 60))} />
    </Svg>
  );
};

const Emblem: React.FC<{s: ShortProps; k: number; u: number}> = ({k}) => (
  <g transform="translate(0 -10)">
    <Sheet x={0} y={0} w={170} h={230} lines={0} />
    {[0, 1, 2, 3, 4].map((j) => {
      const kk = eOut(seg(k, 0.1 + j * 0.12, 0.4 + j * 0.12));
      const y = -60 + j * 36;
      return (
        <g key={j} opacity={kk}>
          <circle cx={-52} cy={y} r={11} fill={C.cyan} stroke={C.ink} strokeWidth={2.5} />
          <rect x={-32} y={y - 5} width={90 * kk} height={10} rx={5} fill={C.ink} opacity={0.75} />
        </g>
      );
    })}
    <Txt x={0} y={150} size={36} weight={800} anchor="middle">
      1 fiche
    </Txt>
    <CheckBadge x={74} y={-104} r={26} k={back(seg(k, 0.7, 1))} />
  </g>
);

export const beams: DeviceSpec = {
  Stage,
  Emblem,
  roleTop: 1075,
  hookCard: true,
  recap: (s) => s.elements.map((e) => ({label: e.nom, mark: 'tile', color: e.couleur})),
};
