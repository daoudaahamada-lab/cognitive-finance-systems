// "Short" composition: 14 s silent vertical shorts (wth-videos/shorts/shorts.json, one short object per render).
// 0-2 s hook (big title + the device's opening action + the hook line), 2-12 s five elements of 2 s (entrance,
// gesture, role line, settle: they accumulate; progress bar 1/5 .. 5/5), 12-14 s end card (title, recap of the 5,
// « fin » line, brand + « S’abonner » pill). One visual device per short (devices/*), same identity as the series.
import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Icon} from '../story/draw';
import {beams} from './devices/beams';
import {chat} from './devices/chat';
import {folder} from './devices/folder';
import {line} from './devices/line';
import {locks} from './devices/locks';
import {back, C, CX, Digits, eOut, END, fr, FONT, initials, onColor, Progress, seg, Svg, TextBox, elStart} from './kit';
import type {DeviceName, DeviceSpec, ShortProps} from './types';

export const DEVICES: Record<DeviceName, DeviceSpec> = {folder, beams, line, locks, chat};
const DEVICE_BY_ID: Record<string, DeviceName> = {S01: 'folder', S02: 'beams', S03: 'line', S04: 'locks', S05: 'chat'};

const HookTitle: React.FC<{s: ShortProps; f: number}> = ({s, f}) => {
  const op = seg(f, 0, 7) * (1 - seg(f, 46, 55));
  const dy = (1 - eOut(seg(f, 0, 10))) * -30 - seg(f, 46, 55) * 40;
  return (
    <TextBox x={80} y={228} w={830} size={76} weight={800} lh={1.06} opacity={op} dy={dy} scale={0.94 + 0.06 * eOut(seg(f, 0, 10))}>
      <Digits text={fr(s.titre)} />
    </TextBox>
  );
};

const RoleCards: React.FC<{s: ShortProps; f: number; dev: DeviceSpec}> = ({s, f, dev}) => {
  if (dev.roleTop === null) return null;
  const top = dev.roleTop;
  const cards: React.ReactNode[] = [];
  if (dev.hookCard && f < 62) {
    const op = seg(f, 8, 15) * (1 - seg(f, 50, 58));
    cards.push(
      <TextBox key="hook" x={80} y={top} w={830} size={52} weight={800} card={C.light} opacity={op} dy={(1 - eOut(seg(f, 8, 16))) * 30}>
        {fr(s.accroche)}
      </TextBox>,
    );
  }
  s.elements.slice(0, 5).forEach((el, i) => {
    const u = f - elStart(i);
    if (u < 0 || u > 60) return;
    const op = seg(u, 6, 13) * (1 - seg(u, 52, 59));
    cards.push(
      <TextBox key={i} x={80} y={top} w={830} size={50} weight={700} card={C.paper} opacity={op} dy={(1 - eOut(seg(u, 6, 14))) * 30}>
        {fr(el.role)}
      </TextBox>,
    );
  });
  return <>{cards}</>;
};

const MiniMark: React.FC<{row: ReturnType<DeviceSpec['recap']>[number]; n: number}> = ({row, n}) => {
  const s = 58;
  return (
    <svg width={s + 6} height={s + 6} viewBox={`-3 -3 ${s + 6} ${s + 6}`} style={{flex: 'none', overflow: 'visible'}}>
      {row.mark === 'tile' ? (
        <>
          <rect x={4} y={4} width={s - 4} height={s - 4} rx={14} fill={C.ink} />
          <rect x={0} y={0} width={s - 4} height={s - 4} rx={14} fill={row.color ?? C.cyan} stroke={C.ink} strokeWidth={3} />
          <text x={(s - 4) / 2} y={(s - 4) / 2 + 8} textAnchor="middle" fill={onColor(row.color ?? C.cyan)} style={{fontFamily: FONT, fontWeight: 800, fontSize: 22}}>
            {initials(row.label)}
          </text>
        </>
      ) : (
        <>
          <circle cx={(s - 4) / 2 + 3} cy={(s - 4) / 2 + 3} r={(s - 4) / 2} fill={C.ink} />
          <circle cx={(s - 4) / 2} cy={(s - 4) / 2} r={(s - 4) / 2} fill={C.cyan} stroke={C.ink} strokeWidth={3} />
          {row.mark === 'num' ? (
            <text x={(s - 4) / 2} y={(s - 4) / 2 + 11} textAnchor="middle" fill={C.ink} style={{fontFamily: FONT, fontWeight: 800, fontSize: 30}}>
              {n}
            </text>
          ) : (
            <g transform={`translate(${(s - 4) / 2} ${(s - 4) / 2})`}>
              <Icon name="check" s={34} color={C.ink} sw={5} />
            </g>
          )}
        </>
      )}
    </svg>
  );
};

const EndCard: React.FC<{s: ShortProps; f: number; dev: DeviceSpec}> = ({s, f, dev}) => {
  const u = f - END;
  if (u < -2) return null;
  const rows = dev.recap(s).slice(0, 5);
  const Emblem = dev.Emblem;
  const kCard = back(seg(u, 0, 12), 1.2);
  const fin = eOut(seg(u, 12, 20));
  const brand = eOut(seg(u, 18, 26));
  const pill = back(seg(u, 22, 32), 2.2);
  const press = seg(u, 38, 42) * (1 - seg(u, 44, 50));
  const pulse = 1 + 0.025 * Math.sin(Math.max(0, u - 50) * 0.5);
  return (
    <div style={{position: 'absolute', left: 80, top: 214, width: 830, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 34, fontFamily: FONT}}>
      <div
        style={{
          width: 830,
          boxSizing: 'border-box',
          padding: '26px 30px 30px',
          background: C.paper,
          border: `4px solid ${C.ink}`,
          borderRadius: 36,
          boxShadow: `8px 8px 0 0 ${C.ink}`,
          opacity: Math.min(1, seg(u, 0, 6)),
          transform: `scale(${0.9 + 0.1 * kCard})`,
          transformOrigin: 'center top',
        }}
      >
        <div style={{fontWeight: 800, fontSize: 44, lineHeight: 1.08, textAlign: 'center', color: C.ink, textWrap: 'balance'}}>
          <Digits text={fr(s.titre)} />
        </div>
        <div style={{display: 'flex', alignItems: 'center', marginTop: 22, gap: 22}}>
          <svg width={200} height={300} viewBox="-100 -150 200 300" style={{flex: 'none', overflow: 'visible'}}>
            <Emblem s={s} k={eOut(seg(u, 2, 14))} u={u} />
          </svg>
          <div style={{display: 'flex', flexDirection: 'column', gap: 6}}>
            {rows.map((row, j) => {
              const k = eOut(seg(u, 5 + 2.5 * j, 11 + 2.5 * j));
              return (
                <div key={j} style={{display: 'flex', alignItems: 'center', gap: 16, opacity: k, transform: `translateX(${(1 - k) * 40}px)`}}>
                  <MiniMark row={row} n={j + 1} />
                  <span style={{fontWeight: 700, fontSize: 36, color: C.ink, whiteSpace: 'nowrap'}}>{fr(row.label)}</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
      <div
        style={{
          width: 830,
          boxSizing: 'border-box',
          padding: '20px 30px',
          background: dev.finAlert ? C.paper : C.light,
          border: `4px solid ${C.ink}`,
          borderRadius: 28,
          boxShadow: `6px 6px 0 0 ${C.ink}`,
          display: 'flex',
          alignItems: 'center',
          gap: 20,
          opacity: fin,
          transform: `translateY(${(1 - fin) * 30}px)`,
        }}
      >
        {dev.finAlert ? (
          <svg width={64} height={64} viewBox="-32 -32 64 64" style={{flex: 'none'}}>
            <Icon name="warning" s={60} color={C.red} sw={5} />
          </svg>
        ) : null}
        <div style={{flex: 1, fontWeight: 700, fontSize: 40, lineHeight: 1.18, textAlign: dev.finAlert ? 'left' : 'center', color: C.ink, textWrap: 'balance'}}>{fr(s.fin)}</div>
      </div>
      <div style={{marginTop: 18, fontWeight: 800, fontSize: 58, color: C.ink, opacity: brand, transform: `translateY(${(1 - brand) * 24}px)`, whiteSpace: 'nowrap'}}>
        WealthTech <span style={{color: C.deep}}>Horizon</span>
      </div>
      <div
        style={{
          width: 420,
          height: 116,
          boxSizing: 'border-box',
          borderRadius: 58,
          background: C.cyan,
          border: `4px solid ${C.ink}`,
          boxShadow: `${8 * (1 - press)}px ${8 * (1 - press)}px 0 0 ${C.ink}`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 16,
          fontWeight: 800,
          fontSize: 52,
          color: C.ink,
          transform: `translate(${8 * press}px, ${8 * press}px) scale(${Math.max(0, pill) * pulse})`,
          opacity: pill > 0.01 ? 1 : 0,
        }}
      >
        <svg width={44} height={44} viewBox="-22 -22 44 44">
          <Icon name="plus" s={40} color={C.ink} sw={6} />
        </svg>
        {fr("S'abonner")}
      </div>
    </div>
  );
};

export const Short: React.FC<ShortProps> = (s) => {
  const f = useCurrentFrame();
  const dev = DEVICES[s.device ?? DEVICE_BY_ID[s.id] ?? 'folder'];
  const Stage = dev.Stage;
  const stageOp = 1 - seg(f, END - 2, END + 8);
  return (
    <AbsoluteFill
      style={{
        backgroundColor: C.bg,
        backgroundImage: `linear-gradient(to right, ${C.gridLine} 2px, transparent 2px), linear-gradient(to bottom, ${C.gridLine} 2px, transparent 2px)`,
        backgroundSize: '36px 36px',
        backgroundPosition: '-1px -1px',
        overflow: 'hidden',
      }}
    >
      {stageOp > 0.01 ? (
        <div style={{position: 'absolute', inset: 0, opacity: stageOp < 0.999 ? stageOp : undefined, transform: stageOp < 0.999 ? `scale(${0.96 + 0.04 * stageOp})` : undefined, transformOrigin: `${CX}px 900px`}}>
          <Stage s={s} f={f} />
        </div>
      ) : null}
      <Svg>
        <Progress f={f} />
      </Svg>
      <HookTitle s={s} f={f} />
      <RoleCards s={s} f={f} dev={dev} />
      <EndCard s={s} f={f} dev={dev} />
    </AbsoluteFill>
  );
};
