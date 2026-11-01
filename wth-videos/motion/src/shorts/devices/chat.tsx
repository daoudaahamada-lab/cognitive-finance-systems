// S05 — a scrolling chat: each prompt is typed in the input bubble, sent, and its answer arrives as a visual object
// (3-slice pie, subscriptions with a yearly total, income − expenses = rest, a 3-line KID sheet, 3 numbered questions).
import React from 'react';
import {Hard, Icon, roundRect, Txt} from '../../story/draw';
import {back, C, clamp01, CX, eInOut, elStart, eOut, FONT, fr, lerp, seg, Svg, Tile} from '../kit';
import type {DeviceSpec, ShortProps} from '../types';

const CLAUDE = '#D97757';
const PANEL = {x: 70, w: 840, bottom: 1500};
const panelTop = (f: number) => lerp(560, 250, eInOut(seg(f, 44, 60)));
const INPUT = {x: 96, y: 1338, w: 788, h: 140};
const MSG_BOTTOM = 1322;
const ANSWER = {x: 96, y: 590, w: 788, h: 712};
const RECAP = ['Classer mes dépenses', 'Lister mes abonnements', 'Mon reste à vivre', 'Résumer un DIC', '3 questions au banquier'];

const ACx = ANSWER.x + ANSWER.w / 2;

// ---------- answer objects (global coordinates inside the answer card) ----------
const Pie: React.FC<{u: number}> = ({u}) => {
  const parts = [
    {label: 'Fixes', pct: 50, color: C.deep},
    {label: 'Variables', pct: 30, color: C.cyan},
    {label: 'Plaisir', pct: 20, color: C.light},
  ];
  const cx = ACx;
  const cy = 830;
  const r = 165;
  let a0 = -90;
  return (
    <g>
      <circle cx={cx + 6} cy={cy + 6} r={r} fill={C.ink} opacity={seg(u, 26, 30)} />
      <circle cx={cx} cy={cy} r={r} fill={C.paper} stroke={C.ink} strokeWidth={4} opacity={seg(u, 26, 30)} />
      {parts.map((p, j) => {
        const g = eInOut(seg(u, 28 + 6 * j, 34 + 6 * j));
        const sweep = (p.pct / 100) * 360 * g;
        const start = a0;
        a0 += (p.pct / 100) * 360;
        if (g <= 0) return null;
        const s = (start * Math.PI) / 180;
        const e = ((start + sweep) * Math.PI) / 180;
        const d = `M${cx},${cy} L${cx + r * Math.cos(s)},${cy + r * Math.sin(s)} A${r},${r} 0 ${sweep > 180 ? 1 : 0} 1 ${cx + r * Math.cos(e)},${cy + r * Math.sin(e)} Z`;
        return <path key={j} d={d} fill={p.color} stroke={C.ink} strokeWidth={4} strokeLinejoin="round" />;
      })}
      {parts.map((p, j) => (
        <g key={`l${j}`} opacity={seg(u, 30 + 6 * j, 34 + 6 * j)} transform={`translate(${cx - 200} ${1068 + j * 72})`}>
          <rect x={-22} y={-22} width={44} height={44} rx={10} fill={p.color} stroke={C.ink} strokeWidth={3} />
          <Txt x={40} y={0} size={42} weight={700}>
            {p.label}
          </Txt>
          <Txt x={420} y={0} size={42} weight={800} anchor="end" tabular>
            {fr(`${p.pct} %`)}
          </Txt>
        </g>
      ))}
    </g>
  );
};

const Subs: React.FC<{u: number}> = ({u}) => {
  const rows = [
    ['Streaming', 13],
    ['Musique', 11],
    ['Cloud', 3],
    ['Salle de sport', 30],
  ] as const;
  const total = Math.round(684 * eOut(seg(u, 40, 48)));
  return (
    <g>
      {rows.map(([n, v], j) => {
        const k = eOut(seg(u, 26 + 3 * j, 31 + 3 * j));
        const y = 672 + j * 84;
        return (
          <g key={j} opacity={k} transform={`translate(${(1 - k) * 30} 0)`}>
            <g transform={`translate(${ANSWER.x + 62} ${y})`}>
              <circle r={24} fill={C.light} stroke={C.ink} strokeWidth={3} />
              <Icon name="repeat" s={30} color={C.ink} sw={3} />
            </g>
            <Txt x={ANSWER.x + 104} y={y} size={42} weight={700}>
              {n}
            </Txt>
            <Txt x={ANSWER.x + ANSWER.w - 40} y={y} size={42} weight={800} anchor="end" tabular>
              {fr(`${v} € / mois`)}
            </Txt>
          </g>
        );
      })}
      <line x1={ANSWER.x + 36} y1={1022} x2={ANSWER.x + ANSWER.w - 36} y2={1022} stroke={C.ink} strokeWidth={4} opacity={seg(u, 36, 40)} />
      <g opacity={seg(u, 38, 42)} transform={`translate(0 ${1132}) scale(1)`}>
        <Hard off={6} render={(sh) => <path d={roundRect(ANSWER.x + 36, -64, ANSWER.w - 72, 128, 30)} fill={sh ? C.ink : C.light} stroke={C.ink} strokeWidth={4} />} />
        <Txt x={ANSWER.x + 70} y={0} size={44} weight={800}>
          Total
        </Txt>
        <Txt x={ANSWER.x + ANSWER.w - 70} y={0} size={62} weight={800} anchor="end" tabular>
          {fr(`${total} € / an`)}
        </Txt>
      </g>
    </g>
  );
};

const Rest: React.FC<{u: number}> = ({u}) => {
  const rows = [
    {op: '', label: 'Revenus', v: '2 100 €', w: 1, color: C.cyan},
    {op: '−', label: 'Charges', v: '1 350 €', w: 1350 / 2100, color: C.grey},
    {op: '=', label: 'Reste à vivre', v: '750 €', w: 750 / 2100, color: C.deep},
  ];
  const bw = ANSWER.w - 120;
  return (
    <g>
      {rows.map((r, j) => {
        const k = eOut(seg(u, 26 + 7 * j, 32 + 7 * j));
        const y = 680 + j * 200;
        const last = j === 2;
        return (
          <g key={j} opacity={k}>
            {last ? <Hard off={6} render={(sh) => <path d={roundRect(ANSWER.x + 24, y - 52, ANSWER.w - 48, 172, 26)} fill={sh ? C.ink : C.light} stroke={C.ink} strokeWidth={4} />} /> : null}
            <Txt x={ANSWER.x + 60} y={y} size={last ? 48 : 44} weight={800} color={C.deep}>
              {r.op}
            </Txt>
            <Txt x={ANSWER.x + 104} y={y} size={last ? 48 : 44} weight={last ? 800 : 700}>
              {fr(r.label)}
            </Txt>
            <Txt x={ANSWER.x + ANSWER.w - 60} y={y} size={last ? 56 : 46} weight={800} anchor="end" tabular>
              {fr(r.v)}
            </Txt>
            <rect x={ANSWER.x + 60} y={y + 44} width={bw * r.w * eOut(seg(u, 28 + 7 * j, 36 + 7 * j))} height={30} rx={15} fill={r.color} stroke={C.ink} strokeWidth={3} />
          </g>
        );
      })}
    </g>
  );
};

const Kid: React.FC<{u: number}> = ({u}) => {
  const rows = ['Frais : 1,2 % / an', 'Risque : 4 / 7', 'Durée : 5 ans'];
  return (
    <g>
      <g opacity={seg(u, 24, 28)}>
        <g transform={`translate(${ANSWER.x + 74} 668)`}>
          <Icon name="sign" s={56} color={C.deep} sw={5} />
        </g>
        <Txt x={ANSWER.x + 118} y={668} size={50} weight={800}>
          DIC
        </Txt>
        <line x1={ANSWER.x + 36} y1={726} x2={ANSWER.x + ANSWER.w - 36} y2={726} stroke={C.ink} strokeWidth={4} />
      </g>
      {rows.map((r, j) => {
        const k = eOut(seg(u, 28 + 6 * j, 34 + 6 * j));
        const y = 812 + j * 170;
        return (
          <g key={j} opacity={k} transform={`translate(${(1 - k) * 30} 0)`}>
            <g transform={`translate(${ANSWER.x + 66} ${y}) scale(${back(seg(u, 30 + 6 * j, 36 + 6 * j))})`}>
              <circle r={26} fill={C.cyan} stroke={C.ink} strokeWidth={3} />
              <Icon name="check" s={30} color={C.ink} sw={4.5} />
            </g>
            <Txt x={ANSWER.x + 112} y={y} size={46} weight={800} tabular>
              {fr(r)}
            </Txt>
            {j === 1
              ? [1, 2, 3, 4, 5, 6, 7].map((n) => (
                  <g key={n}>
                    <path d={roundRect(ANSWER.x + 112 + (n - 1) * 72, y + 40, 62, 56, 12)} fill={n === 4 ? C.deep : n < 4 ? C.light : C.slot} stroke={C.ink} strokeWidth={3} />
                    <Txt x={ANSWER.x + 143 + (n - 1) * 72} y={y + 68} size={36} weight={800} anchor="middle" color={n === 4 ? C.paper : C.ink}>
                      {String(n)}
                    </Txt>
                  </g>
                ))
              : null}
          </g>
        );
      })}
    </g>
  );
};

const Questions: React.FC<{u: number}> = ({u}) => {
  const qs = ['Quels frais, au total ?', 'Puis-je sortir sans frais ?', 'Quel risque, en clair ?'];
  return (
    <g>
      {qs.map((q, j) => {
        const k = back(seg(u, 26 + 6 * j, 32 + 6 * j), 1.2);
        const y = 720 + j * 196;
        return (
          <g key={j} opacity={clamp01(k)} transform={`translate(${ACx} ${y}) scale(${0.85 + 0.15 * k}) translate(${-ACx} ${-y})`}>
            <Hard off={5} render={(sh) => <path d={roundRect(ANSWER.x + 30, y - 66, ANSWER.w - 60, 132, 26)} fill={sh ? C.ink : C.light} stroke={C.ink} strokeWidth={4} />} />
            <circle cx={ANSWER.x + 92} cy={y} r={36} fill={C.cyan} stroke={C.ink} strokeWidth={4} />
            <Txt x={ANSWER.x + 92} y={y} size={40} weight={800} anchor="middle">
              {String(j + 1)}
            </Txt>
            <Txt x={ANSWER.x + 148} y={y} size={42} weight={800}>
              {fr(q)}
            </Txt>
          </g>
        );
      })}
    </g>
  );
};

const ANSWERS = [Pie, Subs, Rest, Kid, Questions];

/** Text of a prompt without its quotes (it is typed as a message). */
const promptText = (role: string) => fr(role.replace(/^«\s*/, '').replace(/\s*»$/, ''));

const Stage: React.FC<{s: ShortProps; f: number}> = ({s, f}) => {
  const top = panelTop(f);
  const msgTop = top + 92;
  const panelIn = eOut(seg(f, 4, 18));
  const active = f >= elStart(0) && f < elStart(5) ? Math.floor((f - elStart(0)) / 60) : -1;
  // what the input field holds now
  let typed = '';
  let caret = Math.floor(f / 8) % 2 === 0;
  let placeholder = true;
  if (active >= 0) {
    const u = f - elStart(active);
    const full = promptText(s.elements[active].role);
    if (u < 18) {
      const n = Math.ceil(full.length * seg(u, 0, 15));
      typed = full.slice(0, n);
      placeholder = n === 0;
      caret = true;
    }
  }
  const sendPulse = active >= 0 ? seg(f - elStart(active), 15, 19) * (1 - seg(f - elStart(active), 19, 24)) : 0;
  return (
    <div style={{position: 'absolute', inset: 0, opacity: Math.min(1, panelIn * 1.5), transform: `scale(${0.88 + 0.12 * panelIn})`, transformOrigin: `${CX}px ${PANEL.bottom}px`}}>
      <Svg>
        <Hard off={7} render={(sh) => <path d={roundRect(PANEL.x, top, PANEL.w, PANEL.bottom - top, 40)} fill={sh ? C.ink : C.paper} stroke={C.ink} strokeWidth={4} />} />
        <Tile x={PANEL.x + 56} y={top + 48} s={60} color={CLAUDE} name="Claude" />
        <Txt x={PANEL.x + 104} y={top + 48} size={40} weight={800}>
          Claude
        </Txt>
        <line x1={PANEL.x} y1={top + 92} x2={PANEL.x + PANEL.w} y2={top + 92} stroke={C.ink} strokeWidth={3} />
        <path d={roundRect(INPUT.x, INPUT.y, INPUT.w, INPUT.h, 30)} fill={C.slot} stroke={C.ink} strokeWidth={4} />
        <g transform={`translate(${INPUT.x + INPUT.w - 52} ${INPUT.y + INPUT.h / 2}) scale(${1 + 0.18 * sendPulse})`}>
          <circle r={36} fill={typed && !placeholder ? C.cyan : C.grey} stroke={C.ink} strokeWidth={4} />
          <g transform="rotate(-90)">
            <Icon name="arrow" s={40} color={C.ink} sw={5} />
          </g>
        </g>
      </Svg>
      <div
        style={{
          position: 'absolute',
          left: INPUT.x + 28,
          top: INPUT.y,
          width: INPUT.w - 130,
          height: INPUT.h,
          display: 'flex',
          alignItems: 'center',
          fontFamily: FONT,
          fontWeight: 700,
          fontSize: 44,
          lineHeight: 1.12,
          color: placeholder ? C.aiTick : C.ink,
        }}
      >
        <span>
          {placeholder ? (active < 0 ? fr('Écris ton prompt…') : '') : typed}
          <span style={{color: C.deep, opacity: caret ? 1 : 0}}>|</span>
        </span>
      </div>
      {/* messages, clipped under the header */}
      <div style={{position: 'absolute', left: PANEL.x + 4, top: msgTop, width: PANEL.w - 8, height: MSG_BOTTOM - msgTop, overflow: 'hidden'}}>
        <div style={{position: 'absolute', left: -(PANEL.x + 4), top: -msgTop, width: 1080, height: 1920}}>
          {/* hook line as Claude's first message */}
          {f < 62 ? (
            <div
              style={{
                position: 'absolute',
                left: 100,
                top: 690 - seg(f, 46, 58) * 500,
                width: 700,
                boxSizing: 'border-box',
                padding: '22px 30px',
                background: C.light,
                border: `4px solid ${C.ink}`,
                borderRadius: '30px 30px 30px 8px',
                boxShadow: `6px 6px 0 0 ${C.ink}`,
                fontFamily: FONT,
                fontWeight: 800,
                fontSize: 54,
                lineHeight: 1.1,
                color: C.ink,
                opacity: seg(f, 10, 16),
                transform: `scale(${0.9 + 0.1 * back(seg(f, 10, 18))})`,
                transformOrigin: 'left bottom',
                textWrap: 'balance',
              }}
            >
              {fr(s.accroche)}
            </div>
          ) : null}
          {s.elements.slice(0, 5).map((el, k) => {
            const u = f - elStart(k);
            if (u < 16 || u > 62) return null;
            const send = eOut(seg(u, 16, 24));
            const scroll = eInOut(seg(u, 50, 60)) * -1000;
            const by = lerp(INPUT.y, 412, send) + scroll;
            const ans = eOut(seg(u, 22, 30));
            const A = ANSWERS[k];
            return (
              <React.Fragment key={k}>
                <div style={{position: 'absolute', right: 1080 - 884, top: 352 + scroll, fontFamily: FONT, fontWeight: 800, fontSize: 36, color: C.deep, opacity: send}}>
                  {fr(el.nom)}
                </div>
                <div
                  style={{
                    position: 'absolute',
                    right: 1080 - 884,
                    top: by,
                    maxWidth: 720,
                    boxSizing: 'border-box',
                    padding: '18px 28px',
                    background: C.light,
                    border: `4px solid ${C.ink}`,
                    borderRadius: '30px 30px 8px 30px',
                    boxShadow: `6px 6px 0 0 ${C.ink}`,
                    fontFamily: FONT,
                    fontWeight: 700,
                    fontSize: 44,
                    lineHeight: 1.12,
                    color: C.ink,
                    textAlign: 'left',
                    transform: `scale(${0.92 + 0.08 * send})`,
                    transformOrigin: 'right top',
                  }}
                >
                  {promptText(el.role)}
                </div>
                {ans > 0.01 ? (
                  <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible', opacity: ans}}>
                    <g transform={`translate(0 ${(1 - ans) * 40 + scroll})`}>
                      <Hard off={6} render={(sh) => <path d={roundRect(ANSWER.x, ANSWER.y, ANSWER.w, ANSWER.h, 30)} fill={sh ? C.ink : C.paper} stroke={C.ink} strokeWidth={4} />} />
                      <Tile x={ANSWER.x - 2} y={ANSWER.y - 2} s={44} color={CLAUDE} name="Claude" />
                      <A u={u} />
                    </g>
                  </svg>
                ) : null}
              </React.Fragment>
            );
          })}
        </div>
      </div>
    </div>
  );
};

const Emblem: React.FC<{s: ShortProps; k: number; u: number}> = ({k}) => (
  <g transform="translate(0 -20)">
    <g transform={`translate(${(1 - eOut(k)) * 40} 0)`} opacity={Math.min(1, k * 2)}>
      <path d={roundRect(-30, -110, 120, 64, 22)} fill={C.ink} transform="translate(5 5)" />
      <path d={roundRect(-30, -110, 120, 64, 22)} fill={C.light} stroke={C.ink} strokeWidth={4} />
      <rect x={-12} y={-84} width={80} height={12} rx={6} fill={C.ink} opacity={0.7} />
    </g>
    <g opacity={seg(k, 0.3, 0.7)}>
      <path d={roundRect(-92, -24, 150, 120, 22)} fill={C.ink} transform="translate(5 5)" />
      <path d={roundRect(-92, -24, 150, 120, 22)} fill={C.paper} stroke={C.ink} strokeWidth={4} />
      <circle cx={-34} cy={36} r={38} fill={C.light} stroke={C.ink} strokeWidth={3} />
      <path d="M-34,36 L-34,-2 A38,38 0 0 1 4,36 Z" fill={C.deep} stroke={C.ink} strokeWidth={3} />
      <rect x={14} y={20} width={30} height={10} rx={5} fill={C.ink} opacity={0.6} />
      <rect x={14} y={42} width={22} height={10} rx={5} fill={C.ink} opacity={0.6} />
    </g>
    <Tile x={-70} y={-96} s={50} color={CLAUDE} name="Claude" />
    <Txt x={0} y={150} size={36} weight={800} anchor="middle">
      5 prompts
    </Txt>
  </g>
);

export const chat: DeviceSpec = {
  Stage,
  Emblem,
  roleTop: null,
  hookCard: false,
  recap: () => RECAP.map((label) => ({label, mark: 'num'})),
};

