/* Étage 9 — Le Chaos Ops : une baie de serveurs sur roulettes, gyrophare hurlant, câbles en bataille et pager au poing. */
{
  const TAU = Math.PI * 2;
  const INK = "#0b1020";
  const frac = (v) => v - Math.floor(v);
  const hsh = (n) => frac(Math.sin(n * 127.1 + 31.7) * 43758.5453);
  /* Balancement de roulage : sert au déplacement, à l'inclinaison de la baie et à la rotation des roulettes. */
  const swayX = (t, rt) => Math.sin(t * 0.8) * 30 + Math.sin(t * 1.9) * 6 + rt * (Math.sin(t * 3.7) * 11 + Math.sin(t * 6.3) * 5);
  const swayV = (t, rt) => Math.cos(t * 0.8) * 0.8 + Math.cos(t * 1.9) * 0.2 + rt * Math.cos(t * 3.7) * 0.6;

  /* Câbles arrière : ancre sur la baie, pointe au repos, couleur, déphasage, type de fiche. `rage` : n'apparaît qu'en phase 2. */
  const REAR = [
    { ax: 68, ay: -88, px: 146, py: -132, cl: "#3d7bd9", ph: 0.0, plug: 0 },
    { ax: 80, ay: -22, px: 160, py: -16, cl: "#e0b13a", ph: 1.7, plug: 1 },
    { ax: 76, ay: 58, px: 152, py: 100, cl: "#57c48f", ph: 3.1, plug: 0 },
    { ax: -62, ay: 104, px: -136, py: 148, cl: "#b06ad9", ph: 4.4, plug: 1 },
    { ax: 34, ay: -128, px: 104, py: -170, cl: "#e8743b", ph: 5.6, plug: 1, rage: true },
    { ax: -74, ay: 62, px: -152, py: 92, cl: "#38c6d9", ph: 2.3, plug: 0, rage: true }
  ];
  /* Unités de la baie, de haut en bas (le voyant HEALTH s'intercale entre la 2e et la 3e). */
  const UNITS = [
    { y: -38, kind: "drives", deadAt: 3, row: 0 },
    { y: -19, kind: "drives", deadAt: 2, row: 1, plateAt: 2, pivot: -1 },
    { y: 52, kind: "vent", deadAt: 9, row: 3 },
    { y: 71, kind: "drives", deadAt: 1, row: 4, plateAt: 1, pivot: 1 },
    { y: 90, kind: "ports", deadAt: 9, row: 5 }
  ];

  /* Fiche au bout d'un câble, dessinée vers +x. */
  const plug = (c, kind, color) => {
    c.fillStyle = INK; rr(c, -5, -7.5, 13, 15, 4); c.fill();
    c.fillStyle = color; rr(c, -3.5, -6, 10, 12, 3); c.fill();
    c.fillStyle = "#d7ddec"; rr(c, 5, -7, 13, 14, 3); c.fill();
    c.strokeStyle = INK; c.lineWidth = 1.2; c.stroke();
    if (kind === 0) { c.fillStyle = "#98a2bd"; c.fillRect(18, -5, 7, 2.6); c.fillRect(18, 2.4, 7, 2.6); }
    else { c.fillStyle = "#98a2bd"; c.fillRect(18, -5, 6, 10); c.fillStyle = "#f4f6fb"; c.fillRect(19.5, -3, 4.5, 2.6); c.fillStyle = INK; c.fillRect(19.5, 1.2, 1.8, 1.8); c.fillRect(22.2, 1.2, 1.8, 1.8); }
  };
  /* Câble-tentacule : Bézier épaisse (contour, gaine, reflet) terminée par une fiche. */
  const cable = (c, ax, ay, x1, y1, x2, y2, tx, ty, color, withPlug, kind, w) => {
    c.lineCap = "round";
    c.beginPath(); c.moveTo(ax, ay); c.bezierCurveTo(x1, y1, x2, y2, tx, ty);
    c.strokeStyle = INK; c.lineWidth = (w || 7) + 3.5; c.stroke();
    c.strokeStyle = color; c.lineWidth = w || 7; c.stroke();
    c.beginPath(); c.moveTo(ax - 1, ay - 2); c.bezierCurveTo(x1 - 1, y1 - 2, x2 - 1, y2 - 2, tx - 1, ty - 2);
    c.strokeStyle = "rgba(255,255,255,0.3)"; c.lineWidth = 1.6; c.stroke();
    if (withPlug) { c.save(); c.translate(tx, ty); c.rotate(Math.atan2(ty - y2, tx - x2)); plug(c, kind, color); c.restore(); }
  };
  /* Petite flamme (rage, pannes). */
  const flame = (c, x, y, w, h, T, seed) => {
    const wob = Math.sin(T * 13 + seed * 5) * w * 0.35, hh = h * (0.8 + 0.3 * Math.sin(T * 17 + seed * 3));
    c.fillStyle = "#ef5a2a"; c.beginPath(); c.moveTo(x - w, y); c.quadraticCurveTo(x - w * 1.1, y - hh * 0.5, x + wob, y - hh); c.quadraticCurveTo(x + w * 1.1, y - hh * 0.45, x + w, y); c.closePath(); c.fill();
    c.fillStyle = "#ffd76a"; c.beginPath(); c.moveTo(x - w * 0.5, y); c.quadraticCurveTo(x - w * 0.55, y - hh * 0.3, x + wob * 0.5, y - hh * 0.58); c.quadraticCurveTo(x + w * 0.55, y - hh * 0.28, x + w * 0.5, y); c.closePath(); c.fill();
  };
  /* Roulette pivotante. */
  const caster = (c, x, y, r, ang, S) => {
    c.fillStyle = S.cLo; c.fillRect(x - 9, y, 18, 4);
    c.strokeStyle = S.cHi; c.lineWidth = 3; c.lineCap = "round"; c.beginPath(); c.moveTo(x - 2, y + 4); c.lineTo(x + 3, y + 4 + r + 2); c.stroke();
    const wx = x + 3, wy = y + 6 + r;
    c.fillStyle = "#080b16"; c.beginPath(); c.arc(wx, wy, r, 0, TAU); c.fill();
    c.strokeStyle = S.cHi; c.lineWidth = 2; c.beginPath(); c.arc(wx, wy, r - 3.2, 0, TAU); c.stroke();
    c.lineWidth = 1.6; c.beginPath();
    for (let k = 0; k < 3; k++) { const a = ang + k * TAU / 3; c.moveTo(wx, wy); c.lineTo(wx + Math.cos(a) * (r - 3.5), wy + Math.sin(a) * (r - 3.5)); }
    c.stroke();
  };

  /* Écran LCD : le visage en gros pixels, l'écran de démarrage et le message de clôture. */
  const face = (c, S) => {
    const { T, look, rt, fl } = S, X0 = -66, Y0 = -110, SW = 116, SH = 64, pw = S.power;
    c.fillStyle = "#0a0e1b"; rr(c, X0 - 5, Y0 - 5, SW + 10, SH + 10, 9); c.fill();
    c.strokeStyle = S.cHi; c.lineWidth = 1.6; c.stroke();
    c.save(); rr(c, X0, Y0, SW, SH, 5); c.clip();
    const bg = pw > 0.04 ? col(mixv(mixv("#0a1424", S.dead && S.d > 0.1 ? "#2fbf7c" : S.hotRaw, 0.10 + rt * 0.10), C.white, fl * 0.35)) : "#04060b";
    c.fillStyle = bg; c.fillRect(X0, Y0, SW, SH);
    const hot = col(S.hot);
    if (S.e < 1 && S.boot < 0.72) {
      // démarrage : barre de progression et journal
      if (S.boot > 0.08) {
        const k = seg(S.boot, 0.1, 0.68);
        c.textAlign = "left"; c.textBaseline = "alphabetic"; c.font = "700 9px " + F_MONO; c.fillStyle = C.ok; c.fillText("BOOT prod-01", X0 + 8, Y0 + 15);
        c.strokeStyle = C.ok; c.lineWidth = 1.4; c.strokeRect(X0 + 8.5, Y0 + 21.5, SW - 17, 9); c.fillRect(X0 + 11, Y0 + 24, (SW - 22) * k, 4);
        c.font = "600 7px " + F_MONO;
        if (k > 0.3) c.fillText("[ OK ] ventilos", X0 + 8, Y0 + 42);
        if (k > 0.6) { c.fillStyle = C.bad; c.fillText("[FAIL] runbook", X0 + 8, Y0 + 52); }
        if (k > 0.85) { c.fillStyle = C.lamp; c.fillText("on verra en prod…", X0 + 8, Y0 + 61); }
      }
    } else if (S.dead && S.d > 0.1) {
      // clôture : « incident clos ✓ », puis extinction en une ligne
      const a = pw * seg(S.d, 0.1, 0.18);
      if (a > 0.02) {
        c.fillStyle = col("#7dffb8", a); c.strokeStyle = col("#7dffb8", a); c.font = "700 15px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle";
        c.fillText("incident", -8, -89); c.fillText("clos", -22, -68);
        c.lineWidth = 4; c.lineCap = "round"; c.lineJoin = "round"; c.beginPath(); c.moveTo(6, -69); c.lineTo(13, -61); c.lineTo(27, -79); c.stroke();
      } else { const l = 1 - seg(S.d, 0.68, 0.8); if (l > 0) { c.fillStyle = "rgba(220,255,235," + l + ")"; c.fillRect(-8 - 50 * l, -79, 100 * l, 2); } }
    } else {
      const cx = -8 + look.x * 5.5, cy = -87 + look.y * 3;
      c.fillStyle = hot;
      if (S.stun) {
        // yeux en croix
        for (const s of [-1, 1]) for (let k = 0; k < 5; k++) { const x = cx + s * 27 - 12.5 + k * 5; c.fillRect(x, cy - 12 + k * 5, 5, 5); c.fillRect(x, cy + 8 - k * 5, 5, 5); }
      } else if (S.gloat > 0.3) {
        // yeux rieurs en accent circonflexe
        for (const s of [-1, 1]) for (let k = 0; k < 6; k++) c.fillRect(cx + s * 27 - 15 + k * 5, cy - 9 + Math.round(Math.abs(k - 2.5) * 4), 5, 8);
      } else {
        const blink = frac(T * 0.31) > 0.96 || frac(T * 0.23 + 0.4) > 0.985 ? 0.14 : 1;
        const open = blink * (1 - S.sq * 0.72), anger = clamp(0.62 + rt * 0.45 + S.threat * 0.2, 0, 1.1), tall = 24 + S.threat * 4 + rt * 2;
        for (const s of [-1, 1]) {
          const ex = cx + s * 27;
          for (let k = 0; k < 6; k++) {
            const cut = S.hk > 0.5 ? 13 : Math.round(k * anger * 1.15) * 2, h = Math.max(3, (tall - cut) * open);
            c.fillRect(s < 0 ? ex - 15 + k * 5 : ex + 10 - k * 5, cy + 12 - h, 5, h);
          }
          if (open > 0.5) {
            const ps = S.threat > 0.5 ? 6 : 10, lk = S.hk > 0.5 ? 0.9 : look.x, px = ex - ps / 2 + lk * 6.5, py = cy + 5 - ps / 2 + look.y * 3;
            c.fillStyle = bg; c.fillRect(px, py, ps, ps);
            c.fillStyle = "rgba(255,255,255,0.9)"; c.fillRect(px, py, 3, 3);
            c.fillStyle = hot;
          }
        }
      }
      // bouche en pixels
      const mx = cx - 2, my = cy + 25, P = S.P;
      const mo = Math.max(S.talk * 0.9, P.on ? (P.rec > 0 ? 1 - P.rec : Math.max(P.wind * 0.6, P.strike)) : 0, S.cast * 0.7, S.sq * 0.55);
      if (S.stun) { for (let k = 0; k < 9; k++) c.fillRect(mx - 22 + k * 5, my + Math.round(Math.sin(k * 1.7 + T * 11) * 2.4), 5, 3); }
      else if (mo > 0.12) {
        const w = 44, h = 6 + mo * 9;
        c.fillRect(mx - w / 2, my - 3, w, h); c.fillStyle = bg; c.fillRect(mx - w / 2 + 3, my, w - 6, h - 6); c.fillStyle = hot;
        for (let k = 0; k < 4; k++) { c.fillRect(mx - w / 2 + 6 + k * 9, my, 5, 2.5); if (h > 11) c.fillRect(mx - w / 2 + 10.5 + k * 9, my + h - 8.5, 5, 2.5); }
      } else if (S.gloat > 0.3) {
        for (let k = 0; k < 10; k++) c.fillRect(mx - 25 + k * 5, my + 4 - Math.round((k - 4.5) ** 2 * 0.3), 5, 4);
        c.fillRect(mx - 15, my, 30, 2);
      } else if (S.hk > 0.5) { c.fillRect(mx - 16, my + 1, 24, 3); c.fillRect(mx + 8, my + 4, 9, 3); }
      else { const fang = 3 + rt * 3; for (let k = 0; k < 9; k++) c.fillRect(mx - 22 + k * 5, my + (k % 2 ? 3 : 0) + Math.round(Math.abs(k - 4) * rt * 0.6), 5, k % 2 ? 3 : fang); }
      // goutte de sueur quand le joueur vise
      if (S.threat > 0.4) { c.fillStyle = "rgba(160,215,255," + (S.threat * 0.9) + ")"; c.fillRect(X0 + SW - 16, Y0 + 12 + frac(T * 1.4) * 10, 4, 6); }
      // bandeau d'état
      c.font = "700 7px " + F_MONO; c.textBaseline = "alphabetic"; c.textAlign = "left";
      const tick = Math.sin(T * 9) > 0;
      if (S.dmg >= 2 || rt > 0.5) { c.fillStyle = tick ? "#ff5a6e" : "rgba(255,90,110,0.45)"; c.fillText(S.dmg >= 3 ? "KERNEL PANIC" : "ERR 500", X0 + 5, Y0 + 9); }
      else { c.fillStyle = tick ? C.bad : "rgba(239,107,92,0.3)"; c.fillRect(X0 + 5, Y0 + 4, 4, 4); c.fillStyle = col(S.hot, 0.7); c.fillText("PROD", X0 + 12, Y0 + 9); }
      if (rt > 0.4) {
        // triangles d'alerte qui clignotent dans les coins
        c.fillStyle = col("#ff2d55", tick ? 0.95 : 0.25); c.beginPath(); c.moveTo(X0 + SW - 13, Y0 + 4); c.lineTo(X0 + SW - 5, Y0 + 16); c.lineTo(X0 + SW - 21, Y0 + 16); c.closePath(); c.fill();
        c.fillStyle = bg; c.fillRect(X0 + SW - 14, Y0 + 8, 2, 4); c.fillRect(X0 + SW - 14, Y0 + 13, 2, 1.6);
      }
      // parasites des écrans abîmés
      if (S.dmg >= 2) {
        for (let k = 0; k < 3; k++) { const gy = Y0 + hsh(Math.floor(T * 9) + k * 7) * SH, gw = 20 + hsh(Math.floor(T * 9) + k) * 60; c.fillStyle = k % 2 ? "rgba(90,230,255,0.28)" : "rgba(255,80,150,0.28)"; c.fillRect(X0 + hsh(k + Math.floor(T * 7)) * (SW - gw), gy, gw, 2.5); }
      }
      if (S.dmg >= 3) { c.fillStyle = "#03050a"; c.beginPath(); c.moveTo(X0 + SW, Y0 + SH); c.lineTo(X0 + SW - 34, Y0 + SH); c.lineTo(X0 + SW - 24, Y0 + SH - 9); c.lineTo(X0 + SW - 14, Y0 + SH - 7); c.lineTo(X0 + SW - 9, Y0 + SH - 22); c.lineTo(X0 + SW, Y0 + SH - 26); c.closePath(); c.fill(); }
      if (S.e < 1) { const a = 1 - seg(S.boot, 0.72, 0.9); if (a > 0) { c.fillStyle = "rgba(255,255,255," + a * 0.8 + ")"; c.fillRect(X0, Y0, SW, SH); } }
    }
    // trame LCD et reflet
    c.fillStyle = "rgba(0,0,0,0.16)"; for (let y = Y0 + 3; y < Y0 + SH; y += 6) c.fillRect(X0, y, SW, 1.2);
    c.fillStyle = "rgba(255,255,255,0.05)"; c.beginPath(); c.moveTo(X0, Y0); c.lineTo(X0 + 46, Y0); c.lineTo(X0 + 14, Y0 + SH); c.lineTo(X0, Y0 + SH); c.closePath(); c.fill();
    if (S.dmg >= 1) {
      c.strokeStyle = "rgba(225,240,255,0.7)"; c.lineWidth = 1.2; c.lineJoin = "round"; c.beginPath();
      c.moveTo(X0 + SW, Y0 + 20); c.lineTo(X0 + SW - 14, Y0 + 26); c.lineTo(X0 + SW - 19, Y0 + 38); c.moveTo(X0 + SW - 14, Y0 + 26); c.lineTo(X0 + SW - 27, Y0 + 22);
      if (S.dmg >= 3) { c.moveTo(X0, Y0 + 44); c.lineTo(X0 + 16, Y0 + 38); c.lineTo(X0 + 24, Y0 + 50); c.lineTo(X0 + 40, Y0 + SH); c.moveTo(X0 + 16, Y0 + 38); c.lineTo(X0 + 22, Y0 + 24); }
      c.stroke();
    }
    c.restore();
  };

  /* Une unité de la baie : tiroirs de disques, grille d'aération ou panneau de brassage. */
  const unit = (c, u, S) => {
    const { T, rt } = S, y = u.y, deadU = S.dmg >= u.deadAt;
    const lit = S.power > 0 && (S.e >= 1 || S.boot > 0.16 + u.row * 0.1) && !(S.dead && S.ledsOut * 6.4 > u.row + 0.5);
    const open = u.plateAt && S.dmg >= u.plateAt;
    const ledCol = (i) => (S.stun ? "#f3b841" : rt > 0.5 ? (hsh(i) < 0.75 ? "#ff2d55" : "#f3b841") : hsh(i) < 0.6 ? "#57c48f" : hsh(i) < 0.85 ? "#f3b841" : "#5aa9ff");
    const blink = (i) => (S.stun ? Math.sin(T * 22) > 0 : Math.sin(T * (2 + hsh(i) * 7) * (1 + rt) + hsh(i + 9) * 6) > (rt > 0.5 ? -0.3 : 0.15));
    c.fillStyle = S.cUnit; rr(c, -64, y, 112, 16, 3); c.fill();
    if (open) {
      // capot arraché : cavité noire, fils à nu
      c.fillStyle = "#05070e"; rr(c, -62, y + 2, 108, 12, 2); c.fill();
      c.lineWidth = 2; c.lineCap = "round";
      for (let k = 0; k < 3; k++) { c.strokeStyle = ["#e0b13a", "#3d7bd9", "#ef4b4b"][k]; c.beginPath(); c.moveTo(-50 + k * 34, y + 3); c.quadraticCurveTo(-40 + k * 34 + Math.sin(T * 3 + k) * 3, y + 16, -26 + k * 34, y + 5); c.stroke(); }
      if (lit && Math.sin(T * 23 + u.row) > 0.55) { c.fillStyle = "#fff6c8"; c.fillRect(-20 + hsh(Math.floor(T * 12)) * 40, y + 5, 3, 3); }
      return;
    }
    const i0 = u.row * 10;
    for (let k = 0; k < 3; k++) { c.fillStyle = lit && (deadU ? k === 0 : blink(i0 + k)) ? (deadU ? "#ef4b4b" : ledCol(i0 + k)) : "rgba(255,255,255,0.09)"; c.fillRect(-60 + k * 6, y + 6, 3.5, 3.5); }
    if (u.kind === "drives") {
      for (let k = 0; k < 3; k++) {
        const sx = -38 + k * 28, out = S.dmg >= 3 && u.row === 0 && k === 1 ? 3 : 0;
        if (out) { c.fillStyle = "#05070e"; c.fillRect(sx, y + 2, 26, 12); }
        c.fillStyle = deadU ? S.cDead : S.cSled; rr(c, sx - out * 1.5, y + 2 + out, 26, 12, 2); c.fill();
        c.fillStyle = S.cLo; c.fillRect(sx + 18 - out * 1.5, y + 4 + out, 4, 8);
        c.fillStyle = lit && !deadU && blink(i0 + 4 + k) ? ledCol(i0 + 4 + k) : "rgba(255,255,255,0.08)"; c.fillRect(sx + 3 - out * 1.5, y + 6.5 + out, 8, 3);
      }
    } else if (u.kind === "vent") {
      c.fillStyle = "#070a14"; for (let x = -36; x < 44; x += 7) c.fillRect(x, y + 3, 3.4, 10);
    } else {
      for (let k = 0; k < 7; k++) { c.fillStyle = "#070a14"; c.fillRect(-38 + k * 12, y + 5, 8.5, 8); c.fillStyle = lit && blink(i0 + 4 + k) ? ledCol(i0 + 4 + k) : "rgba(255,255,255,0.08)"; c.fillRect(-36 + k * 12, y + 2, 4, 2); }
    }
  };
  /* Capot d'unité arraché qui pend à une vis. */
  const plate = (c, u, S) => {
    const sw = Math.sin(S.t * 2.3 + u.row) * 0.07 + S.fl * 0.18;
    c.save(); c.translate(u.pivot > 0 ? 46 : -62, u.y + 3);
    c.rotate(u.pivot > 0 ? -0.5 - sw : 0.21 + sw);
    c.fillStyle = S.cSled; rr(c, u.pivot > 0 ? -108 : -2, -3, 110, 15, 3); c.fill();
    c.strokeStyle = INK; c.lineWidth = 1.4; c.stroke();
    c.fillStyle = S.cLo; for (let k = 0; k < 3; k++) c.fillRect((u.pivot > 0 ? -100 : 8) + k * 34, 1, 22, 7);
    c.fillStyle = "#c9d1e4"; c.beginPath(); c.arc(0, 4, 2.4, 0, TAU); c.fill();
    c.restore();
  };

  /* Disposition du décor, partagée par backdrop et ambient. */
  const layout = (env) => {
    const W = env.W, gy = env.groundY;
    const wx = W * 0.035, ww = Math.min(W * 0.4, 330), wy = gy - 372, wh = 196;
    const cw = (ww - 16) / 3, ch = (wh - 14) / 2;
    const cell = (i, j) => ({ x: wx + 5 + i * (cw + 3), y: wy + 5 + j * (ch + 4), w: cw, h: ch });
    return { W, gy, wx, wy, ww, wh, cell, mastX: W * 0.955, mastTop: gy - 430, dishX: W * 0.455, dishY: gy - 150 };
  };

  BOSSES[9] = {
    v: 2,
    palette: { main: "#ef4b4b", dark: "#2a3350", accent: "#f3b841", eye: "#f3b841", rage: "#ff2d55" },
    hit: { rx: 98, ry: 152, coreR: 21 },
    top: 176,
    attackFrom: { x: -176, y: -30 },
    castLean: -0.12,
    weakSpot: () => ({ x: -8, y: 24 }),
    critLabel: "HEALTH CHECK",
    epitaph: "INCIDENT CLOS",
    lines: {
      hit: ["Qui a touché à la prod ?!", "Ma config locale !", "Rollback ! ROLLBACK !", "C’était dans quel runbook, ça ?"],
      crit: ["Mon health check !", "Tout est rouge !", "502… 503… 504…"],
      wrong: ["Copie ça depuis le wiki, ça marchera.", "Encore un réglage à la main !", "Chez moi, ça marche."],
      timeout: ["Incident ouvert, personne d’astreinte.", "Trop tard, le pager sonne."],
      gloat: ["Bip bip ! C’est toi d’astreinte ce soir.", "On corrigera en prod, comme toujours.", "Encore un incident sans post-mortem !"],
      rage: "Alerte générale ! Tout le monde en prod !",
      special: {
        incident: ["Nouvel incident ! Personne n’a de procédure ?", "Le pager hurle, à toi de jouer !", "Encore une alerte non triée !"],
        hook: ["Un hook ?! Mes incidents rebondissent…", "Un contrôle déterministe… c’est déloyal !", "Cadenassé par un PreToolUse. Quelle honte."]
      }
    },
    intro: {
      title: "Incidents en rafale",
      text: "Il lance des incidents qui foncent vers toi : touche-les pour les acquitter, sinon sa barre d’attaque avance. Installe un hook pour les bloquer tous : un contrôle déterministe vaut mieux que l’urgence permanente."
    },
    mechanics: ["incidents"],

    /* Triangle d'alerte qui tournoie. */
    shot: {
      color: "#f3b841", spin: 8,
      draw(c, s) {
        const rage = !!s.rage, p = 1 + Math.sin((s.t || 0) * 34) * 0.07;
        c.scale(p, p);
        c.lineJoin = "round";
        c.strokeStyle = rage ? "rgba(255,45,85,0.45)" : "rgba(243,184,65,0.4)"; c.lineWidth = 2;
        c.beginPath(); c.arc(0, 2, 22, 0, TAU); c.stroke();
        c.beginPath(); c.moveTo(0, -17); c.lineTo(17, 12); c.lineTo(-17, 12); c.closePath();
        c.strokeStyle = INK; c.lineWidth = 8; c.stroke();
        c.strokeStyle = rage ? "#ff2d55" : "#f3b841"; c.lineWidth = 4.5; c.stroke();
        c.fillStyle = rage ? "#ff2d55" : "#f3b841"; c.fill();
        c.fillStyle = rage ? "#ffffff" : INK; rr(c, -2.4, -9, 4.8, 11, 2); c.fill(); c.beginPath(); c.arc(0, 7, 2.6, 0, TAU); c.fill();
      }
    },

    /* Roulis : il glisse de gauche à droite sur ses roulettes, par à-coups nerveux en rage. */
    motion(b) {
      const t = b.t || 0, rt = b.rageT || 0;
      return { x: swayX(t, rt) - 13, y: Math.sin(t * 0.6) * 7 - Math.abs(Math.sin(t * 3.2)) * 3 + rt * Math.sin(t * 9.4) * 3 };
    },

    backdrop(c, env) {
      const L = layout(env), { W, gy } = L, rnd = env.rnd || seeded(909);
      const dark = "#0d1326", steel = "#222c4c", edge = "#34416a";
      // chemin de câbles au plafond, du mur d'écrans au mât
      c.strokeStyle = "rgba(13,19,38,0.9)"; c.lineWidth = 2.5; c.lineCap = "round";
      for (let k = 0; k < 3; k++) { c.beginPath(); c.moveTo(L.wx + L.ww - 10, L.wy + 4 + k * 3); c.quadraticCurveTo(W * 0.66, L.wy + 80 + k * 22, L.mastX, L.mastTop + 70 + k * 46); c.stroke(); }
      // mât d'antenne en treillis (à droite, fin : il ne gêne pas le boss)
      const mx = L.mastX, mt = L.mastTop, mb = gy - 20;
      c.strokeStyle = "#1b2440"; c.lineWidth = 3; c.beginPath(); c.moveTo(mx - 13, mb); c.lineTo(mx - 3, mt); c.moveTo(mx + 13, mb); c.lineTo(mx + 3, mt); c.stroke();
      c.lineWidth = 1.5; c.beginPath();
      for (let k = 0; k < 11; k++) { const y0 = lerp(mb, mt, k / 11), y1 = lerp(mb, mt, (k + 1) / 11), w0 = lerp(13, 3, k / 11), w1 = lerp(13, 3, (k + 1) / 11); c.moveTo(mx - w0, y0); c.lineTo(mx + w1, y1); c.moveTo(mx + w0, y0); c.lineTo(mx - w1, y1); c.moveTo(mx - w1, y1); c.lineTo(mx + w1, y1); }
      c.stroke();
      c.strokeStyle = "#1b2440"; c.lineWidth = 2; c.beginPath(); c.moveTo(mx, mt); c.lineTo(mx, mt - 34); c.stroke();
      c.fillStyle = "#1b2440"; for (const [dy, s] of [[90, -1], [150, 1]]) { c.beginPath(); c.ellipse(mx + s * 14, mt + dy, 6, 11, 0, 0, TAU); c.fill(); c.fillRect(mx + (s > 0 ? 0 : -14), mt + dy - 1.5, 14, 3); }
      c.fillStyle = "#5a1d28"; c.beginPath(); c.arc(mx, mt - 36, 4, 0, TAU); c.fill();
      // pupitres de contrôle au pied du mur, bande de signalisation jaune et noire
      const dx0 = W * 0.2, dx1 = W * 0.6, dy = gy - 104;
      c.fillStyle = dark; c.beginPath(); c.moveTo(dx0, gy - 30); c.lineTo(dx0 + 12, dy); c.lineTo(dx1 - 12, dy); c.lineTo(dx1, gy - 30); c.closePath(); c.fill();
      c.fillStyle = steel; c.beginPath(); c.moveTo(dx0 + 12, dy); c.lineTo(dx0 + 24, dy - 12); c.lineTo(dx1 - 24, dy - 12); c.lineTo(dx1 - 12, dy); c.closePath(); c.fill();
      for (let x = dx0 + 30; x < dx1 - 30; x += 9) { const r = rnd(); if (r < 0.55) { c.fillStyle = r < 0.12 ? "rgba(239,75,75,0.8)" : r < 0.3 ? "rgba(243,184,65,0.7)" : "rgba(87,196,143,0.6)"; c.fillRect(x, dy - 8 + (r * 40 % 4), 4, 2.5); } }
      c.fillStyle = "#151a26"; c.fillRect(dx0 + 14, dy + 6, dx1 - dx0 - 28, 9);
      c.fillStyle = "rgba(243,184,65,0.55)"; c.beginPath();
      for (let x = dx0 + 14; x < dx1 - 26; x += 14) { c.moveTo(x, dy + 15); c.lineTo(x + 6, dy + 6); c.lineTo(x + 13, dy + 6); c.lineTo(x + 7, dy + 15); c.closePath(); }
      c.fill();
      // antenne parabolique sur son pied
      const px = L.dishX, py = L.dishY;
      c.strokeStyle = steel; c.lineWidth = 6; c.beginPath(); c.moveTo(px, dy - 10); c.lineTo(px, py + 6); c.stroke();
      c.save(); c.translate(px, py); c.rotate(-0.55);
      c.fillStyle = steel; c.beginPath(); c.ellipse(0, 0, 44, 15, 0, 0, Math.PI); c.fill();
      c.fillStyle = edge; c.beginPath(); c.ellipse(0, 0, 44, 6, 0, 0, TAU); c.fill();
      c.fillStyle = dark; c.beginPath(); c.ellipse(0, 0, 38, 4, 0, 0, TAU); c.fill();
      c.strokeStyle = edge; c.lineWidth = 2; c.beginPath(); c.moveTo(-30, 0); c.lineTo(0, -32); c.lineTo(30, 0); c.moveTo(0, 0); c.lineTo(0, -32); c.stroke();
      c.fillStyle = "#c9d1e4"; c.beginPath(); c.arc(0, -33, 3.5, 0, TAU); c.fill();
      c.restore();
      // mur d'écrans : portique, six moniteurs, courbes et alertes
      c.fillStyle = dark; c.fillRect(L.wx + 26, L.wy + L.wh, 9, gy - L.wy - L.wh); c.fillRect(L.wx + L.ww - 36, L.wy + L.wh, 9, gy - L.wy - L.wh);
      c.fillStyle = "#0a0f20"; rr(c, L.wx - 3, L.wy - 3, L.ww + 6, L.wh + 6, 8); c.fill();
      c.strokeStyle = edge; c.lineWidth = 2; c.stroke();
      const scr = (i, j, tint) => { const q = L.cell(i, j); c.fillStyle = tint; rr(c, q.x, q.y, q.w, q.h, 4); c.fill(); return q; };
      c.lineJoin = "round"; c.lineCap = "round";
      // 1. courbe de latence qui s'emballe
      let q = scr(0, 0, "#0e1a2c");
      c.strokeStyle = "rgba(120,150,200,0.25)"; c.lineWidth = 1; c.beginPath(); for (let k = 1; k < 4; k++) { c.moveTo(q.x + 4, q.y + q.h * k / 4); c.lineTo(q.x + q.w - 4, q.y + q.h * k / 4); } c.stroke();
      c.strokeStyle = "#57c48f"; c.lineWidth = 2; c.beginPath();
      for (let k = 0; k <= 12; k++) { const u = k / 12, yy = q.y + q.h * (0.78 - 0.1 * rnd() - (u > 0.6 ? (u - 0.6) * 1.5 : 0)); if (k) c.lineTo(q.x + 6 + u * (q.w - 12), yy); else c.moveTo(q.x + 6, yy); }
      c.stroke();
      c.fillStyle = "#ef4b4b"; c.beginPath(); c.arc(q.x + q.w - 6, q.y + q.h * 0.2, 3, 0, TAU); c.fill();
      // 2. écran radar (le balayage est animé par ambient)
      q = scr(1, 0, "#0a1c1a");
      const rc = { x: q.x + q.w / 2, y: q.y + q.h / 2, r: Math.min(q.w, q.h) / 2 - 6 };
      c.strokeStyle = "rgba(98,240,166,0.4)"; c.lineWidth = 1.2; for (const k of [1, 0.66, 0.33]) { c.beginPath(); c.arc(rc.x, rc.y, rc.r * k, 0, TAU); c.stroke(); }
      c.beginPath(); c.moveTo(rc.x - rc.r, rc.y); c.lineTo(rc.x + rc.r, rc.y); c.moveTo(rc.x, rc.y - rc.r); c.lineTo(rc.x, rc.y + rc.r); c.stroke();
      // 3. histogramme d'erreurs
      q = scr(2, 0, "#1a1420");
      for (let k = 0; k < 8; k++) { const bh = q.h * (0.15 + 0.09 * k * rnd() + (k > 5 ? 0.25 : 0)); c.fillStyle = k > 5 ? "#ef4b4b" : "#f3b841"; c.fillRect(q.x + 7 + k * (q.w - 14) / 8, q.y + q.h - 6 - bh, (q.w - 14) / 8 - 3, bh); }
      // 4. journal qui défile
      q = scr(0, 1, "#0e1626");
      for (let k = 0; k < 9; k++) { const r = rnd(); c.fillStyle = r < 0.25 ? "rgba(239,75,75,0.85)" : r < 0.5 ? "rgba(243,184,65,0.7)" : "rgba(154,165,195,0.45)"; c.fillRect(q.x + 6, q.y + 7 + k * (q.h - 12) / 9, (q.w - 14) * (0.35 + r * 0.6), 2.5); }
      // 5. grande alerte (clignote dans ambient)
      q = scr(1, 1, "#2a0f18");
      c.fillStyle = "#ef4b4b"; c.beginPath(); c.moveTo(q.x + q.w / 2, q.y + 10); c.lineTo(q.x + q.w / 2 + 26, q.y + q.h - 22); c.lineTo(q.x + q.w / 2 - 26, q.y + q.h - 22); c.closePath(); c.fill();
      c.fillStyle = "#2a0f18"; c.fillRect(q.x + q.w / 2 - 2.5, q.y + 26, 5, 18); c.fillRect(q.x + q.w / 2 - 2.5, q.y + q.h - 33, 5, 5);
      c.fillStyle = "#ef4b4b"; c.font = "800 13px " + F_DISPLAY; c.textAlign = "center"; c.textBaseline = "alphabetic"; c.fillText("INCIDENT", q.x + q.w / 2, q.y + q.h - 6);
      // 6. carte des services : nœuds verts, orange, rouges
      q = scr(2, 1, "#0e1a2c");
      const nodes = []; for (let k = 0; k < 7; k++) nodes.push([q.x + 10 + rnd() * (q.w - 20), q.y + 10 + rnd() * (q.h - 20)]);
      c.strokeStyle = "rgba(120,150,200,0.4)"; c.lineWidth = 1; c.beginPath(); for (let k = 1; k < 7; k++) { c.moveTo(nodes[k][0], nodes[k][1]); c.lineTo(nodes[(k * 3) % k][0], nodes[(k * 3) % k][1]); c.moveTo(nodes[k][0], nodes[k][1]); c.lineTo(nodes[0][0], nodes[0][1]); } c.stroke();
      nodes.forEach((p, k) => { c.fillStyle = k % 3 === 0 ? "#ef4b4b" : k % 3 === 1 ? "#57c48f" : "#f3b841"; c.beginPath(); c.arc(p[0], p[1], 3.5, 0, TAU); c.fill(); });
      // reflets et lueur du mur
      c.fillStyle = "rgba(255,255,255,0.04)"; for (let i = 0; i < 3; i++) for (let j = 0; j < 2; j++) { const z = L.cell(i, j); c.beginPath(); c.moveTo(z.x, z.y); c.lineTo(z.x + z.w * 0.5, z.y); c.lineTo(z.x + z.w * 0.2, z.y + z.h); c.lineTo(z.x, z.y + z.h); c.closePath(); c.fill(); }
      // panneau d'avertissement accroché au portique
      const sx = L.wx + L.ww + 26, sy = L.wy + L.wh - 30;
      c.strokeStyle = dark; c.lineWidth = 4; c.beginPath(); c.moveTo(L.wx + L.ww, sy - 30); c.lineTo(sx, sy - 30); c.lineTo(sx, sy - 22); c.stroke();
      c.fillStyle = "#f3b841"; c.beginPath(); c.moveTo(sx, sy - 24); c.lineTo(sx + 22, sy + 14); c.lineTo(sx - 22, sy + 14); c.closePath(); c.fill();
      c.strokeStyle = "#151a26"; c.lineWidth = 3; c.stroke();
      c.fillStyle = "#151a26"; c.fillRect(sx - 2.2, sy - 10, 4.4, 13); c.fillRect(sx - 2.2, sy + 6, 4.4, 4.4);
      c.fillStyle = "rgba(232,236,246,0.5)"; c.font = "700 9px " + F_MONO; c.textAlign = "center"; c.fillText("PROD", sx, sy + 27);
    },
    /* Balayage du radar, alerte et feu du mât qui clignotent. */
    ambient(c, env) {
      const L = layout(env), T = env.time || 0;
      const q = L.cell(1, 0), cx = q.x + q.w / 2, cy = q.y + q.h / 2, r = Math.min(q.w, q.h) / 2 - 6, a = T * 1.6;
      for (let k = 0; k < 4; k++) { c.fillStyle = "rgba(98,240,166," + (0.26 - k * 0.06) + ")"; c.beginPath(); c.moveTo(cx, cy); c.arc(cx, cy, r, a - 0.22 * (k + 1), a - 0.22 * k); c.closePath(); c.fill(); }
      c.strokeStyle = "rgba(170,255,210,0.9)"; c.lineWidth = 1.5; c.beginPath(); c.moveTo(cx, cy); c.lineTo(cx + Math.cos(a) * r, cy + Math.sin(a) * r); c.stroke();
      for (let k = 0; k < 3; k++) { const ba = 0.9 + k * 2.2, br = r * (0.45 + 0.2 * k), age = frac((a - ba) / TAU); c.fillStyle = "rgba(170,255,210," + Math.max(0, 0.9 - age * 1.4) + ")"; c.beginPath(); c.arc(cx + Math.cos(ba) * br, cy + Math.sin(ba) * br, 2.2, 0, TAU); c.fill(); }
      const z = L.cell(1, 1); c.fillStyle = "rgba(239,75,75," + (0.1 + 0.16 * (Math.sin(T * 5) > 0 ? 1 : 0)) + ")"; rr(c, z.x, z.y, z.w, z.h, 4); c.fill();
      const on = frac(T * 0.8) < 0.5 ? 1 : 0.15, mx = L.mastX, my = L.mastTop - 36;
      c.fillStyle = "rgba(255,70,90," + 0.28 * on + ")"; c.beginPath(); c.arc(mx, my, 15, 0, TAU); c.fill();
      c.fillStyle = "rgba(255,120,130," + on + ")"; c.beginPath(); c.arc(mx, my, 4, 0, TAU); c.fill();
    },

    update(b, dt) {
      const o = b.own || (b.own = {}), hook = !!(b.mech && b.mech.incidents && b.mech.incidents.hook);
      o.hk = lerp(o.hk || 0, hook ? 1 : 0, 1 - Math.exp(-dt * 8));
      o.ba = (o.ba || 0) + dt * (b.stun > 0 ? 1.5 : lerp(3.4, 10.5, b.rageT || 0) * (hook ? 0.45 : 1));
    },

    draw(c, b) {
      const t = b.t || 0, T = b.time == null ? t : b.time, own = b.own || {};
      const e = b.enter == null ? 1 : b.enter, dying = b.dying == null ? -1 : b.dying, dead = dying >= 0, d = dead ? dying : 0;
      const dmg = b.dmg || 0, fl = b.flash || 0, sq = b.squint || 0, rt = (b.rageT || 0) * (dead ? 1 - seg(d, 0.04, 0.3) : 1), hp = b.hpFrac == null ? 1 : b.hpFrac;
      const look = b.look || { x: -1, y: 0 }, P = atkPose(b);
      const cast = b.cast >= 0 ? Math.sin(clamp(b.cast / 0.9, 0, 1) * Math.PI) : 0;
      const stun = (b.stun || 0) > 0, gloat = b.gloat || 0, talk = b.talk || 0, threat = b.threat || 0, beat = b.beat || 0;
      const hookOn = !!(b.mech && b.mech.incidents && b.mech.incidents.hook), hk = own.hk == null ? (hookOn ? 1 : 0) : own.hk;

      // entrée : il arrive en roulant de la droite, freine, puis démarre ; mort : extinction, affaissement, écran qui se replie
      const roll = easeOut(seg(e, 0, 0.5)), speed = e < 1 ? (1 - seg(e, 0, 0.5)) ** 1.5 : 0, brake = e < 1 ? Math.sin(seg(e, 0.34, 0.66) * Math.PI) : 0;
      const boot = e < 1 ? seg(e, 0.58, 1) : 1, unf = e < 1 ? backOut(seg(boot, 0.35, 1)) : 1;
      const ledsOut = seg(d, 0.02, 0.5), slump = dead ? easeInOut(seg(d, 0.36, 0.76)) : 0, crt = dead ? seg(d, 0.8, 1) : 0;
      const power = dead ? 1 - seg(d, 0.56, 0.66) : boot > 0.05 ? 1 : 0;
      const live = (1 - slump) * (stun ? 0.4 : 1);

      const hotRaw = mixv("#f3b841", "#ff2d55", rt);
      const S = {
        t, T, e, d, dead, dmg, fl, sq, rt, look, P, cast, stun, gloat, talk, threat, hk, boot, power, ledsOut,
        hotRaw, hot: mixv(hotRaw, C.white, fl * 0.6),
        cHi: col(mixv(mixv("#5c6a99", "#93405a", rt * 0.6), C.white, fl * 0.6)),
        cLo: col(mixv(mixv("#141a30", "#1f0c16", rt * 0.6), C.white, fl * 0.4)),
        cUnit: col(mixv(mixv("#161d35", "#260f1a", rt * 0.6), C.white, fl * 0.5)),
        cSled: col(mixv(mixv("#3a466d", "#5a2a3c", rt * 0.6), C.white, fl * 0.6)),
        cDead: col(mixv(mixv("#232a44", "#2e141e", rt * 0.6), C.white, fl * 0.5))
      };
      const metal = mixv(mixv("#2d3757", "#43202f", rt * 0.6), C.white, fl * 0.6);
      const metalHi = mixv(mixv("#5c6a99", "#93405a", rt * 0.6), C.white, fl * 0.6);
      const sideC = mixv(mixv("#1b2340", "#2a111c", rt * 0.6), C.white, fl * 0.5);
      const wcol = (h, k) => col(mixv(h, C.white, fl * (k == null ? 0.5 : k)));

      // gyrophare : rouge, frénétique en rage, vert puis éteint à la mort
      const ang = own.ba == null ? T * lerp(3.4, 10.5, rt) : own.ba, ca = Math.cos(ang), sa = Math.sin(ang);
      const lampOn = dead ? 1 - seg(d, 0.5, 0.62) : stun ? 0.35 + 0.3 * Math.sin(T * 30) : seg(boot, 0.45, 0.6);
      const lampC = dead ? mixv(mixv("#ef4b4b", "#ff2d55", rt), "#3fe08f", seg(d, 0.05, 0.16)) : mixv(mixv("#ef4b4b", "#ff2d55", rt), "#ffffff", fl * 0.5);

      const sw = swayX(t, rt), sv = swayV(t, rt);
      const jit = rt * live * Math.sin(T * 47) * 1.3 + (stun ? Math.sin(T * 38) * 1.5 : 0);
      const hop = gloat * Math.abs(Math.sin(T * 13)) * 7;
      const rot = -sv * 0.03 * live + (1 - roll) * 0.11 - brake * 0.17 + slump * 0.11 + (dmg >= 3 ? 0.035 : 0) - rt * 0.03 * live + threat * 0.03;
      const pulse = 1 + beat * 0.014 + rt * 0.03;
      let sx = pulse * (1 + fl * 0.07), sy = pulse * (1 - fl * 0.07 - brake * 0.03);
      if (crt > 0) { sy *= 1 - easeIn(seg(crt, 0, 0.55)) * 0.985; sx *= 1 - easeIn(seg(crt, 0.5, 1)) * 0.96; }

      c.save();
      c.translate((1 - roll) * 440 + jit, slump * 18 - hop);
      c.translate(0, 138); c.rotate(rot); c.translate(0, -138);

      // halo d'alarme
      const glowA = (0.13 + 0.09 * Math.max(0, sa) + rt * 0.08) * lampOn * (1 - crt);
      if (glowA > 0.01) {
        const ag = c.createRadialGradient(0, -20, 30, 0, -20, 215);
        ag.addColorStop(0, col(lampC, glowA)); ag.addColorStop(1, col(lampC, 0));
        c.fillStyle = ag; c.fillRect(-215, -235, 430, 430);
      }
      // étincelles, poussière de freinage et traînées de l'arrivée
      if (e < 1 && (speed > 0.02 || brake > 0.02)) {
        const pow = Math.min(1, speed * 1.4 + brake);
        c.lineCap = "round";
        for (let k = 0; k < 14; k++) {
          const u = frac(T * 4.6 + k * 0.37), wx = k % 2 ? 41 : -53, vx = 50 + hsh(k) * 110, vy = -(20 + hsh(k + 5) * 90);
          const x = wx + vx * u, y = 143 + vy * u + 70 * u * u;
          c.strokeStyle = col(mixv("#ffffff", "#f3b841", u), (1 - u) * pow); c.lineWidth = 3.2 - u * 2;
          c.beginPath(); c.moveTo(x, y); c.lineTo(x + vx * 0.09, y + (vy + 140 * u) * 0.09); c.stroke();
        }
        for (let k = 0; k < 4; k++) { const u = frac(T * 1.9 + k * 0.25); c.fillStyle = "rgba(190,198,220," + 0.3 * brake * (1 - u) + ")"; c.beginPath(); c.arc((k % 2 ? 50 : -44) + u * 46, 140 - u * 16, 6 + u * 12, 0, TAU); c.fill(); }
        c.strokeStyle = "rgba(232,236,246," + 0.45 * speed + ")"; c.lineWidth = 2.5;
        for (let k = 0; k < 5; k++) { const y = -100 + k * 52 + hsh(k + Math.floor(T * 10)) * 20; c.beginPath(); c.moveTo(96, y); c.lineTo(190 + hsh(k) * 80, y); c.stroke(); }
      }

      c.translate(0, -5); c.scale(sx, sy); c.translate(0, 5);
      if (crt > 0.6) c.globalAlpha = 1 - seg(crt, 0.6, 1) * 0.9;

      // faisceaux du gyrophare (derrière la baie)
      if (lampOn > 0.05) {
        const beams = rt > 0.5 ? [ca, -ca, sa * 0.8, -sa * 0.8] : [ca, -ca];
        for (const dir of beams) {
          const len = 185 * Math.abs(dir); if (len < 14) continue;
          const sgn = dir > 0 ? 1 : -1, g = c.createLinearGradient(0, 0, sgn * len, 0);
          g.addColorStop(0, col(lampC, 0.55 * lampOn)); g.addColorStop(1, col(lampC, 0));
          c.fillStyle = g; c.beginPath(); c.moveTo(0, -146); c.lineTo(sgn * len, -146 - len * 0.2); c.lineTo(sgn * len, -146 + len * 0.2); c.closePath(); c.fill();
        }
      }

      // câbles arrière : ils ondulent, fouettent en rage, pendent à la mort, sont ficelés par le hook
      const tie = { x: 128, y: 34 };
      for (let i = 0; i < REAR.length; i++) {
        const k = REAR[i], ext = k.rage ? backOut(rt) * unf : unf; if (ext < 0.05) continue;
        const right = k.ax > 0, ph = k.ph;
        let tx = k.px + (Math.sin(t * 2.1 + ph) * 9 + rt * Math.sin(t * 7.3 + ph * 2) * 15) * live;
        let ty = k.py + (Math.cos(t * 1.7 + ph) * 11 + rt * Math.cos(t * 8.1 + ph) * 15) * live - gloat * 24 * (right ? 1 : 0.4);
        tx = lerp(tx, k.ax + (right ? 30 : -24), slump); ty = lerp(ty, Math.min(168, k.ay + 96), slump);
        if (right) { tx = lerp(tx, tie.x + 26 + i * 3, hk); ty = lerp(ty, tie.y + 34 + i * 9, hk); } else { tx = lerp(tx, k.ax - 34, hk); ty = lerp(ty, k.ay + 44, hk); }
        tx = k.ax + (tx - k.ax) * ext * (1 - threat * 0.12); ty = k.ay + (ty - k.ay) * ext * (1 - threat * 0.12);
        tx = Math.min(tx, 180); ty = clamp(ty, -182, 170);
        const dx = tx - k.ax, dy = ty - k.ay, len = Math.max(1, Math.hypot(dx, dy)), nx = -dy / len, ny = dx / len;
        const amp = (1 - hk * 0.7) * live * ext, w1 = (Math.sin(t * 2.4 + ph) * 20 + rt * Math.sin(t * 9.1 + ph) * 16) * amp, w2 = (Math.cos(t * 1.9 + ph) * 16 + rt * Math.cos(t * 7.7 + ph) * 14) * amp;
        const sag = slump * 34;
        let x1 = k.ax + dx * 0.35 + nx * w1, y1 = k.ay + dy * 0.35 + ny * w1 + sag, x2 = k.ax + dx * 0.72 - nx * w2, y2 = k.ay + dy * 0.72 - ny * w2 + sag;
        if (right && hk > 0.01) { x1 = lerp(x1, tie.x - 24, hk); y1 = lerp(y1, tie.y - 12 + (k.ay - tie.y) * 0.3, hk); x2 = lerp(x2, tie.x, hk); y2 = lerp(y2, tie.y - 4, hk); }
        cable(c, k.ax, k.ay, x1, y1, x2, y2, tx, ty, wcol(k.cl), true, k.plug);
        if (rt > 0.5 && !dead && hsh(Math.floor(T * 13) + i * 3) > 0.62) {
          // étincelle au bout de la fiche
          c.strokeStyle = "#fff6c8"; c.lineWidth = 1.6; c.beginPath();
          for (let q = 0; q < 4; q++) { const a = q * 1.57 + T * 9; c.moveTo(tx + Math.cos(a) * 3, ty + Math.sin(a) * 3); c.lineTo(tx + Math.cos(a) * 9, ty + Math.sin(a) * 9); }
          c.stroke();
        }
      }
      if (hk > 0.03) {
        // collier de serrage vert autour des câbles ficelés
        c.save(); c.translate(tie.x, tie.y + 4); c.rotate(0.35); c.globalAlpha *= Math.min(1, hk * 1.5);
        c.fillStyle = "#1f7a52"; rr(c, -17, -8, 34, 16, 5); c.fill(); c.fillStyle = "#57c48f"; rr(c, -15, -6, 30, 9, 4); c.fill(); c.fillStyle = "#c8f5de"; c.fillRect(9, -9, 6, 5);
        c.restore();
      }

      // roulettes
      const wa = sw / 9.5 - (1 - roll) * 46;
      caster(c, 74, 108, 8, wa, S);
      caster(c, -56, 116, 10, wa, S);
      caster(c, 38, 116, 10, wa + 1, S);

      // flanc droit : ouïes d'aération, porte de service
      c.fillStyle = col(sideC); c.beginPath(); c.moveTo(62, -122); c.lineTo(84, -132); c.lineTo(84, 108); c.lineTo(62, 118); c.closePath(); c.fill();
      c.strokeStyle = INK; c.lineWidth = 2.5; c.lineCap = "round"; c.beginPath();
      for (let k = 0; k < 6; k++) { const y = -110 + k * 8; c.moveTo(66, y - 1.8); c.lineTo(80, y - 8.2); }
      c.stroke();
      if (dmg >= 2) {
        // porte de service arrachée : cavité, fils qui pendent, battant ouvert
        c.fillStyle = "#05070e"; c.beginPath(); c.moveTo(65, 20); c.lineTo(82, 12); c.lineTo(82, 92); c.lineTo(65, 100); c.closePath(); c.fill();
        c.lineWidth = 2.2;
        for (let k = 0; k < 3; k++) { c.strokeStyle = ["#ef4b4b", "#e0b13a", "#38c6d9"][k]; c.beginPath(); c.moveTo(70 + k * 4, 40 + k * 12); c.quadraticCurveTo(84 + k * 5 + Math.sin(t * 2.6 + k) * 4, 96 + k * 8, 78 + k * 9 + Math.sin(t * 2.1 + k) * 5, 112 + k * 10); c.stroke(); }
        const o = 22 + Math.sin(t * 1.8) * 4 + fl * 6;
        c.fillStyle = col(mixv(sideC, "#000000", 0.25)); c.beginPath(); c.moveTo(84, 10); c.lineTo(84 + o, 22); c.lineTo(84 + o, 106); c.lineTo(84, 92); c.closePath(); c.fill();
        c.strokeStyle = col(metalHi); c.lineWidth = 1.5; c.stroke();
      } else {
        c.strokeStyle = "rgba(0,0,0,0.35)"; c.lineWidth = 1.5; c.beginPath(); c.moveTo(66, 21); c.lineTo(81, 14); c.lineTo(81, 92); c.lineTo(66, 99); c.closePath(); c.stroke();
      }
      // dessus
      c.fillStyle = col(mixv(metalHi, metal, 0.45)); c.beginPath(); c.moveTo(-78, -122); c.lineTo(-56, -132); c.lineTo(84, -132); c.lineTo(62, -122); c.closePath(); c.fill();
      // façade
      const fg = c.createLinearGradient(-78, 0, 62, 0);
      fg.addColorStop(0, col(metalHi)); fg.addColorStop(0.1, col(metal)); fg.addColorStop(0.85, col(metal)); fg.addColorStop(1, col(mixv(metal, "#000000", 0.28)));
      c.fillStyle = fg; rr(c, -78, -122, 140, 240, 7); c.fill();
      c.strokeStyle = INK; c.lineWidth = 2; c.stroke();
      c.strokeStyle = col(metalHi, 0.8); c.lineWidth = 1.4; c.beginPath(); c.moveTo(-76, -114); c.lineTo(-76, 110); c.stroke();
      // montants et vis
      c.fillStyle = S.cLo; c.fillRect(-73, -42, 6, 150); c.fillRect(51, -42, 6, 150);
      c.fillStyle = S.cHi; for (let y = -36; y < 106; y += 19) { c.fillRect(-71, y, 2.4, 2.4); c.fillRect(52.8, y, 2.4, 2.4); }
      // plinthe de signalisation
      c.fillStyle = "#12141d"; c.fillRect(-72, 107, 128, 9);
      c.fillStyle = wcol(hotRaw, 0.5); c.beginPath();
      for (let x = -72; x < 44; x += 13) { c.moveTo(x, 116); c.lineTo(x + 6, 107); c.lineTo(x + 12.5, 107); c.lineTo(x + 6.5, 116); c.closePath(); }
      c.fill();

      // unités, voyants et tiroirs
      for (const u of UNITS) unit(c, u, S);

      // panneau HEALTH : le voyant est sa cible critique
      const wsx = -8, wsy = 24;
      c.fillStyle = "#080d1a"; rr(c, -64, 2, 112, 44, 5); c.fill();
      c.strokeStyle = S.cHi; c.lineWidth = 1.4; c.stroke();
      const hOn = dead ? 1 - seg(d, 0.42, 0.52) : seg(boot, 0.5, 0.6);
      const hcol = hOn < 0.5 ? "#3a425c" : hp > 0.6 ? "#57c48f" : hp > 0.3 ? "#f3b841" : "#ef4b4b";
      c.strokeStyle = col(hcol, 0.9); c.lineWidth = 1.6; c.lineJoin = "round"; c.beginPath();
      for (const [xa, xb] of [[-60, -27], [11, 44]]) {
        for (let x = xa; x <= xb; x += 3) {
          const p = (x + T * (hp > 0.3 ? 46 : 80) + 400) % 34, yy = hOn < 0.5 ? 0 : p > 12 && p < 15 ? -9 : p >= 15 && p < 18 ? 7 : 0;
          if (x === xa) c.moveTo(x, wsy + 4 + yy); else c.lineTo(x, wsy + 4 + yy);
        }
      }
      c.stroke();
      c.fillStyle = "rgba(232,236,246,0.75)"; c.font = "700 7px " + F_MONO; c.textAlign = "left"; c.textBaseline = "alphabetic"; c.fillText("HEALTH", -60, 12);
      const hpulse = 1 + Math.sin(T * (hp < 0.3 ? 11 : 5)) * 0.07 * hOn + beat * 0.05;
      c.fillStyle = "#05070e"; c.beginPath(); c.arc(wsx, wsy, 17, 0, TAU); c.fill();
      c.strokeStyle = S.cHi; c.lineWidth = 2.5; c.stroke();
      c.save(); if (hOn > 0.5) { c.shadowColor = hcol; c.shadowBlur = 16; }
      const lg = c.createRadialGradient(wsx - 4, wsy - 4, 1, wsx, wsy, 13 * hpulse);
      lg.addColorStop(0, hOn > 0.5 ? "#ffffff" : "#8089a6"); lg.addColorStop(0.42, col(mixv(hcol, C.white, fl * 0.6))); lg.addColorStop(1, col(mixv(hcol, "#000000", 0.45)));
      c.fillStyle = lg; c.beginPath(); c.arc(wsx, wsy, 13 * hpulse, 0, TAU); c.fill();
      c.restore();
      c.fillStyle = "rgba(255,255,255,0.55)"; c.beginPath(); c.ellipse(wsx - 5, wsy - 6, 4, 2.4, -0.6, 0, TAU); c.fill();

      // câbles de brassage en spaghetti sur la façade
      c.lineWidth = 2.6; c.lineCap = "round";
      const sp = Math.sin(t * 2.2) * 2 * live;
      c.strokeStyle = wcol("#38c6d9"); c.beginPath(); c.moveTo(-34, 99); c.quadraticCurveTo(-48 + sp, 86, -56, 60); c.stroke();
      c.strokeStyle = wcol("#e8743b"); c.beginPath(); c.moveTo(-10, 99); c.quadraticCurveTo(10 - sp, 124 + sp, 26, 99); c.stroke();
      c.strokeStyle = wcol("#d95fb0"); c.beginPath(); c.moveTo(38, 99); c.quadraticCurveTo(46 + sp, 80, 30, 62); c.stroke();

      for (const u of UNITS) if (u.plateAt && dmg >= u.plateAt) plate(c, u, S);
      if (dmg >= 3 && !dead) flame(c, -20, 86, 7, 20, T, 3);

      face(c, S);
      drawCracks(c, b, "rgba(255,214,196,0.75)", 1.6);

      // hook installé : sangle verte et cadenas, la machine est bridée
      if (hk > 0.03) {
        const k = backOut(hk);
        c.save(); c.globalAlpha *= Math.min(1, hk * 1.6);
        c.fillStyle = "#1f7a52"; c.fillRect(-79, -46, 142 * k, 11);
        c.beginPath(); c.moveTo(62, -46); c.lineTo(84, -56); c.lineTo(84, -45); c.lineTo(62, -35); c.closePath(); c.fill();
        c.fillStyle = "#57c48f"; c.fillRect(-79, -44, 142 * k, 5);
        c.translate(-8, -40 + (1 - k) * -30); c.rotate(Math.sin(t * 2.4) * 0.08);
        c.strokeStyle = "#c8f5de"; c.lineWidth = 4; c.beginPath(); c.arc(0, -3, 8, Math.PI, 0); c.stroke();
        c.fillStyle = "#1f7a52"; rr(c, -14, -4, 28, 22, 5); c.fill(); c.fillStyle = "#57c48f"; rr(c, -12, -2, 24, 16, 4); c.fill();
        c.fillStyle = "#0e3a27"; c.beginPath(); c.arc(0, 5, 3.2, 0, TAU); c.fill(); c.fillRect(-1.3, 5, 2.6, 6);
        c.restore();
      }

      // gyrophare
      c.fillStyle = INK; rr(c, -22, -140, 44, 13, 4); c.fill();
      c.fillStyle = S.cHi; c.fillRect(-19, -137, 38, 3);
      const domeC = lampOn > 0.05 ? mixv(mixv(lampC, "#000000", 0.25), "#ffffff", Math.max(0, sa) * 0.55 * lampOn) : mixv("#3a425c", C.white, fl * 0.4);
      c.save(); if (lampOn > 0.3) { c.shadowColor = col(lampC); c.shadowBlur = 18; }
      c.fillStyle = col(domeC); c.beginPath(); c.ellipse(0, -139, 17, 20, 0, Math.PI, 0); c.closePath(); c.fill();
      c.restore();
      if (lampOn > 0.05) { c.fillStyle = col(mixv(lampC, "#ffffff", 0.7), 0.85 * lampOn); c.beginPath(); c.ellipse(ca * 8, -147, 3 + 5 * Math.abs(sa), 8, 0, 0, TAU); c.fill(); }
      c.fillStyle = "rgba(255,255,255,0.4)"; c.beginPath(); c.ellipse(-8, -150, 2.6, 6, 0.5, 0, TAU); c.fill();
      c.strokeStyle = INK; c.lineWidth = 1.6; c.beginPath(); c.ellipse(0, -139, 17, 20, 0, Math.PI, 0); c.stroke();
      if (dmg >= 3) { c.strokeStyle = "rgba(255,255,255,0.7)"; c.lineWidth = 1.2; c.beginPath(); c.moveTo(4, -158); c.lineTo(8, -150); c.lineTo(4, -146); c.lineTo(11, -141); c.stroke(); }
      if (rt > 0.3 && lampOn > 0.5) {
        // ondes de sirène
        c.lineWidth = 2.2;
        for (let k = 0; k < 2; k++) { const u = frac(T * 2.6 + k * 0.5), r = 22 + u * 20; c.strokeStyle = col(lampC, 0.7 * rt * (1 - u)); c.beginPath(); c.arc(0, -146, r, -0.6, 0.6); c.stroke(); c.beginPath(); c.arc(0, -146, r, Math.PI - 0.6, Math.PI + 0.6); c.stroke(); }
      }

      // fumée des ouïes (de plus en plus épaisse) et flammes de la rage
      const nS = dead ? Math.round(6 * (1 - slump)) : e < 1 ? Math.round(3 * boot) + (brake > 0.2 ? 3 : 0) : 2 + dmg * 2 + (rt > 0.5 ? 2 : 0);
      for (let k = 0; k < nS; k++) {
        const u = frac(T * (0.34 + 0.06 * (k % 3)) + k * 0.37), front = k % 3 === 2;
        const vx = front ? 30 + (k % 2) * 14 : 76, vy = front ? -130 : -116 + (k % 2) * 10;
        const x = vx + u * (20 + 14 * Math.sin(k * 2.1)) + Math.sin(T * 1.3 + k) * 5 * u, y = vy - u * (52 + 8 * (k % 3)), r = 5 + u * (12 + dmg * 2);
        const g = rt > 0.5 ? 70 : 150;
        c.fillStyle = "rgba(" + g + "," + (g + 8) + "," + (g + 30) + "," + (0.16 + dmg * 0.05 + rt * 0.08) * Math.sin(u * Math.PI) + ")";
        c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill();
      }
      if (rt > 0.1 && !dead) {
        const fs = backOut(rt);
        c.strokeStyle = col("#ff8a3c", 0.55 * rt + 0.25 * rt * Math.sin(T * 12)); c.lineWidth = 3; c.lineCap = "round"; c.beginPath(); c.moveTo(-70, -123); c.lineTo(56, -123); c.stroke();
        flame(c, 40, -131, 10 * fs, 36 * fs, T, 0); flame(c, 60, -130, 7 * fs, 23 * fs, T, 1); flame(c, -48, -128, 7 * fs, 21 * fs, T, 2); flame(c, 80, -108, 5 * fs, 15 * fs, T, 4);
      }

      // tentacule avant : il tient le pager, l'arme en arrière puis fouette vers le joueur
      const ax = -76, ay = -6;
      let tx = -150, ty = 12 + Math.sin(t * 2.6) * 7 * live, pa = -0.12 + Math.sin(t * 2.1) * 0.1 * live, taut = 0;
      tx = lerp(tx, -142, gloat); ty = lerp(ty, -72 + Math.sin(T * 26) * 4, gloat);
      tx = lerp(tx, -166, cast); ty = lerp(ty, -58, cast);
      tx = lerp(tx, -120, threat * 0.8); ty = lerp(ty, -10, threat * 0.8);
      tx = lerp(tx, -112, hk); ty = lerp(ty, 56, hk); pa = lerp(pa, 0.5, hk);
      if (P.on) {
        const Wd = { x: -100, y: -150 }, R = { x: -176, y: -30 }, Sx = { x: -206, y: 30 };
        if (P.rec > 0) { const k = easeInOut(P.rec); tx = lerp(Sx.x, tx, k); ty = lerp(Sx.y, ty, k); pa = lerp(-0.25, pa, k); taut = 1 - k; }
        else if (P.strike > 0) { const k = easeOut(P.strike); tx = lerp(R.x, Sx.x, k); ty = lerp(R.y, Sx.y, k); pa = lerp(-0.6, -0.25, k); taut = 1; }
        else if (P.wind < 0.72) { const k = easeOut(P.wind / 0.72); tx = lerp(tx, Wd.x, k); ty = lerp(ty, Wd.y, k); pa = lerp(pa, 1.0, k); }
        else { const k = ((P.wind - 0.72) / 0.28) ** 2; tx = lerp(Wd.x, R.x, k); ty = lerp(Wd.y, R.y, k); pa = lerp(1.0, -0.6, k); taut = k; }
      }
      tx = lerp(tx, -104, slump); ty = lerp(ty, 128, slump); pa = lerp(pa, 1.25, slump);
      tx = ax + (tx - ax) * unf; ty = ay + (ty - ay) * unf;
      const ex = tx + 15, ey = ty + 2;
      const x1 = lerp(ax - 26, lerp(ax, ex, 0.33), taut), y1 = lerp(ay - 34 + Math.sin(t * 3) * 8 * live + slump * 60, lerp(ay, ey, 0.33), taut);
      const x2 = lerp(ex + 34, lerp(ax, ex, 0.66), taut), y2 = lerp(ey + 36, lerp(ay, ey, 0.66), taut);
      if (P.on && P.strike > 0 && P.rec < 0.6) {
        // sillage du coup de fouet et ondes du pager
        const a = 1 - P.rec / 0.6;
        c.strokeStyle = "rgba(255,255,255," + 0.5 * a + ")"; c.lineWidth = 3; c.lineCap = "round"; c.beginPath(); c.moveTo(-104, -146); c.quadraticCurveTo(-176, -110, -184, -34); c.stroke();
        c.strokeStyle = col(hotRaw, 0.8 * a); c.lineWidth = 2.4;
        for (let k = 0; k < 2; k++) { const r = 14 + (P.strike + P.rec) * 12 + k * 8; c.beginPath(); c.arc(tx - 8, ty, r, Math.PI * 0.72, Math.PI * 1.28); c.stroke(); }
      }
      if (unf > 0.04) cable(c, ax, ay, x1, y1, x2, y2, ex, ey, wcol("#d9534f"), false, 0, 8);
      const ps = clamp(unf * 1.6, 0, 1);
      c.save(); c.translate(tx, ty); c.rotate(pa + (P.on || gloat > 0.2 || cast > 0.2 ? Math.sin(T * 44) * 0.07 : 0)); c.scale(ps, ps);
      const ring = !dead && power > 0 && (P.on || cast > 0.1 || gloat > 0.2 || Math.sin(T * (rt > 0.5 ? 14 : 7)) > 0.2);
      c.fillStyle = INK; rr(c, -22, -16, 44, 32, 7); c.fill();
      c.fillStyle = wcol("#2a3350"); rr(c, -20, -14, 40, 28, 6); c.fill();
      c.fillStyle = hk > 0.5 ? (ring ? "#57c48f" : "#1d5a3f") : ring ? wcol("#f3b841") : "#4a3a16"; rr(c, -15, -9, 22, 14, 2.5); c.fill();
      if (power > 0 && !dead) {
        c.fillStyle = INK;
        if (hk > 0.5) { c.fillRect(-9, -3, 10, 7); c.strokeStyle = INK; c.lineWidth = 1.8; c.beginPath(); c.arc(-4, -3, 3, Math.PI, 0); c.stroke(); }
        else { c.fillRect(-5.5, -7, 3, 6.5); c.fillRect(-5.5, 1, 3, 2.6); }
      }
      c.fillStyle = "#ef4b4b"; c.beginPath(); c.arc(13, -5, 2.6, 0, TAU); c.fill(); c.fillStyle = "#5c6a99"; c.fillRect(10.5, 1, 5, 3.4); c.fillRect(-14, 8, 12, 2.6);
      c.strokeStyle = "#5c6a99"; c.lineWidth = 2; c.beginPath(); c.moveTo(-14, -15); c.lineTo(-17, -24); c.stroke(); c.fillStyle = "#ef4b4b"; c.beginPath(); c.arc(-17, -25, 2.4, 0, TAU); c.fill();
      // l'extrémité du câble s'enroule autour du pager
      c.strokeStyle = INK; c.lineWidth = 8.5; c.lineCap = "round"; c.beginPath(); c.moveTo(19, -15); c.quadraticCurveTo(12, 0, 19, 15); c.stroke();
      c.strokeStyle = wcol("#d9534f"); c.lineWidth = 5.5; c.stroke();
      if (ring && hk < 0.5) {
        c.strokeStyle = col(hotRaw, 0.85); c.lineWidth = 2;
        c.beginPath(); c.arc(-22, 0, 7, Math.PI * 0.75, Math.PI * 1.25); c.stroke(); c.beginPath(); c.arc(-22, 0, 12, Math.PI * 0.78, Math.PI * 1.22); c.stroke();
      }
      c.restore();

      // étoiles de l'étourdissement
      if (stun && !dead) {
        c.fillStyle = "#ffe08a";
        for (let k = 0; k < 3; k++) {
          const a = T * 5 + k * 2.09, px = Math.cos(a) * 34, py = -166 + Math.sin(a) * 7, r = 5 + Math.sin(a) * 1.5;
          c.beginPath(); for (let q = 0; q < 8; q++) { const rr2 = q % 2 ? r * 0.4 : r, aa = q * 0.785 + T * 3; c.lineTo(px + Math.cos(aa) * rr2, py + Math.sin(aa) * rr2); } c.closePath(); c.fill();
        }
      }
      c.restore();

      // dernière image : l'écran se replie en une ligne, puis un point
      if (crt > 0.25) {
        const w = 100 * (1 - easeIn(seg(crt, 0.5, 1))) + 3, a = seg(crt, 0.25, 0.5) * (1 - seg(crt, 0.88, 1));
        c.save(); c.translate(0, slump * 18 - 5); c.fillStyle = "rgba(225,255,238," + a + ")"; c.shadowColor = "#57c48f"; c.shadowBlur = 14;
        c.beginPath(); c.ellipse(0, 0, w, 2.2, 0, 0, TAU); c.fill(); c.restore();
      }
    }
  };
}
