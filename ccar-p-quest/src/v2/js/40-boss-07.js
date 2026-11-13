/* Étage 7 — L'Injecteur : une seringue géante dont le réservoir de verre est la vie.
   Anti-pattern : l'injection de prompt, des instructions cachées dans des données.
   L'aiguille vise le joueur (à gauche), le visage vit dans le verre, le cœur de verre est le point faible. */
{
  const TAU = Math.PI * 2;
  const TIP = -222;                                 // pointe de l'aiguille (= attackFrom)
  const GX0 = -90, GX1 = 88, GH = 54, GR = 24;      // réservoir de verre
  const EYE_X = 39, EYE_Y = -19, HEART_Y = 3, MOUTH_Y = 31;
  const r7 = seeded(707);
  const BUBBLES = Array.from({ length: 16 }, () => ({ x: r7(), s: 0.22 + r7() * 0.5, r: 1.6 + r7() * 3, p: r7() }));
  const SHARDS = Array.from({ length: 18 }, (_, i) => {
    const a = (i / 18) * TAU + r7() * 0.3;
    return { x: Math.cos(a) * 72, y: Math.sin(a) * 42, vx: Math.cos(a) * (110 + r7() * 170), vy: Math.sin(a) * (90 + r7() * 130) - 70, s: 7 + r7() * 13, sp: (r7() - 0.5) * 9, a0: r7() * TAU };
  });
  const STREAMS = Array.from({ length: 8 }, (_, i) => ({ x: -76 + i * 18 + r7() * 10, w: 3.5 + r7() * 8, d: r7() * 0.34 }));
  const GLYPHS = ["{", "</>", "sudo", "}", "ignore"], GLYPHS_RAGE = ["{", "</>", "sudo!", "}", "IGNORE"];
  // Fissures propres à chaque stade de dégâts (en plus des fissures d'impact du moteur) : [stade, points].
  const DMG_CRACKS = [
    [1, [[-72, -54], [-63, -41], [-71, -31], [-60, -23]]], [1, [[-63, -41], [-51, -43]]],
    [2, [[60, 54], [53, 41], [63, 31], [55, 23]]], [2, [[53, 41], [43, 45]]], [2, [[-18, -54], [-13, -45], [-21, -39]]],
    [3, [[-88, 28], [-73, 25], [-68, 36], [-56, 31]]], [3, [[-73, 25], [-75, 13]]], [3, [[22, 54], [27, 45], [19, 40]]]
  ];

  const steelY = (c, y0, y1, S) => { const g = c.createLinearGradient(0, y0, 0, y1); g.addColorStop(0, col(S.m1)); g.addColorStop(0.5, col(S.m2)); g.addColorStop(1, col(S.m3)); return g; };
  const steelX = (c, x0, x1, S) => { const g = c.createLinearGradient(x0, 0, x1, 0); g.addColorStop(0, col(S.m1)); g.addColorStop(0.55, col(S.m2)); g.addColorStop(1, col(S.m3)); return g; };
  const glass = (c, inset) => rr(c, GX0 + inset, -GH + inset, GX1 - GX0 - inset * 2, (GH - inset) * 2, Math.max(2, GR - inset));

  /* Aiguille, embase, et en rage : deux aiguilles latérales et des ardillons. */
  const drawNeedle = (c, S, rt, bend, drop) => {
    if (rt > 0.02) {
      const L = 94 * backOut(rt);
      for (const sgn of [-1, 1]) {
        c.save(); c.translate(-100, sgn * 22); c.rotate(-sgn * 0.2); c.scale(1, -sgn);
        c.fillStyle = steelY(c, -4, 4, S);
        c.beginPath(); c.moveTo(6, -3.8); c.lineTo(-L + 18, -2.6); c.lineTo(-L, 2); c.lineTo(6, 3.8); c.closePath(); c.fill();
        c.strokeStyle = "rgba(255,255,255,0.6)"; c.lineWidth = 1; c.beginPath(); c.moveTo(0, -1.6); c.lineTo(-L + 20, -1.2); c.stroke();
        c.fillStyle = col(S.liq, 0.95); c.beginPath(); c.arc(-L - 1, 2, 2.6, 0, TAU); c.fill();
        c.restore();
      }
    }
    c.fillStyle = steelY(c, -5, 5, S);
    c.beginPath(); c.moveTo(-118, -5); c.lineTo(-170, -4.2); c.lineTo(-170, 4.2); c.lineTo(-118, 5); c.closePath(); c.fill();
    c.save(); c.translate(-170, 0); c.rotate(bend);
    const tx = TIP + 170;
    c.beginPath(); c.moveTo(1, -4.2); c.lineTo(tx + 26, -3.2); c.lineTo(tx, 2.6); c.lineTo(1, 4.2); c.closePath(); c.fill();
    c.strokeStyle = "rgba(255,255,255,0.8)"; c.lineWidth = 1.3; c.beginPath(); c.moveTo(52, -2); c.lineTo(tx + 28, -1.4); c.stroke();
    if (rt > 0.25) {                                // ardillons
      const k = seg(rt, 0.25, 1); c.fillStyle = col(S.m2);
      for (const bx of [tx + 34, tx + 52, tx + 70]) for (const sgn of [-1, 1]) { c.beginPath(); c.moveTo(bx, sgn * 3); c.lineTo(bx + 9, sgn * 3.4); c.lineTo(bx + 14, sgn * (3.4 + 9 * k)); c.closePath(); c.fill(); }
    }
    if (bend) {                                     // attelle de sparadrap sur l'aiguille tordue
      c.fillStyle = "#e9dcc0"; c.fillRect(-6, -6.5, 13, 13); c.strokeStyle = "rgba(90,70,40,0.5)"; c.lineWidth = 1; c.strokeRect(-6, -6.5, 13, 13);
    }
    if (drop > 0.2) {
      c.fillStyle = col(S.liqHi, 0.95); c.beginPath(); c.arc(tx - 1, 2.6, drop, 0, TAU); c.fill();
      c.fillStyle = "rgba(255,255,255,0.85)"; c.beginPath(); c.arc(tx - 1 - drop * 0.3, 2.6 - drop * 0.3, drop * 0.3, 0, TAU); c.fill();
    }
    c.restore();
    // embase : collerette, cône, bague de couleur
    c.fillStyle = steelY(c, -10, 10, S); rr(c, -130, -9, 13, 18, 3); c.fill();
    c.fillStyle = steelY(c, -36, 36, S);
    c.beginPath(); c.moveTo(-120, -11); c.lineTo(-106, -29); c.lineTo(-84, -37); c.lineTo(-84, 37); c.lineTo(-106, 29); c.lineTo(-120, 11); c.closePath(); c.fill();
    c.fillStyle = col(S.liq, 0.95); c.fillRect(-107, -29, 5, 58);
    c.fillStyle = "rgba(255,255,255,0.45)"; c.beginPath(); c.moveTo(-119, -8); c.lineTo(-106, -25); c.lineTo(-86, -32); c.lineTo(-86, -26); c.lineTo(-104, -20); c.lineTo(-116, -4); c.closePath(); c.fill();
  };

  /* Tige et poussoir du piston (px = position du poussoir). */
  const drawPlunger = (c, S, px, crooked) => {
    c.fillStyle = steelY(c, -7, 7, S); c.fillRect(GX1 + 6, -6, px - GX1 - 4, 12);
    c.fillStyle = "rgba(255,255,255,0.45)"; c.fillRect(GX1 + 6, -3, px - GX1 - 6, 2.4);
    c.fillStyle = col(S.m3); for (let x = GX1 + 20; x < px - 4; x += 12) c.fillRect(x, -6, 2, 12);
    c.save(); c.translate(px + 7, 0); if (crooked) c.rotate(0.17);
    c.fillStyle = steelX(c, -7, 7, S); rr(c, -7, -40, 14, 80, 6); c.fill();
    c.fillStyle = "rgba(255,255,255,0.4)"; rr(c, -5, -36, 3.4, 72, 1.7); c.fill();
    if (crooked) { c.fillStyle = "#e9dcc0"; c.fillRect(-8, 14, 16, 9); }
    c.restore();
  };

  /* Ailettes : des cornes leur poussent en rage, l'ailette du bas s'ébrèche avec les dégâts. */
  const drawFlange = (c, S, rt, dmg) => {
    c.fillStyle = steelX(c, GX1 - 6, GX1 + 13, S);
    if (rt > 0.02) {
      const k = backOut(rt);
      for (const sgn of [-1, 1]) {
        c.save(); c.scale(1, sgn);
        c.beginPath(); c.moveTo(GX1 + 11, 68); c.lineTo(GX1 + 11, 82); c.quadraticCurveTo(GX1 + 6, 99 + 3 * k, GX1 - 32 * k, 95 + 9 * k); c.quadraticCurveTo(GX1 - 9, 88, GX1 - 4, 68); c.closePath(); c.fill();
        c.restore();
      }
    }
    rr(c, GX1 - 4, -82, 15, 164, 7); c.fill();
    rr(c, GX1 - 8, -36, 23, 72, 6); c.fill();
    c.fillStyle = "rgba(255,255,255,0.38)"; rr(c, GX1 - 2, -78, 3.4, 156, 1.7); c.fill();
    c.fillStyle = col(S.liq, 0.9); c.fillRect(GX1 - 8, -3, 23, 6);
    if (dmg >= 2) {                                 // ailette du bas fendue, rafistolée au sparadrap
      c.fillStyle = "#0b0f22"; c.beginPath(); c.moveTo(GX1 + 11, 50); c.lineTo(GX1 + 2, 55); c.lineTo(GX1 + 6, 58); c.lineTo(GX1 - 2, 62); c.lineTo(GX1 + 11, 60); c.closePath(); c.fill();
      c.fillStyle = "#e9dcc0"; c.fillRect(GX1 - 6, 64, 19, 8); c.strokeStyle = "rgba(96,74,40,0.55)"; c.lineWidth = 1; c.strokeRect(GX1 - 6, 64, 19, 8);
    }
  };

  const drawEye = (c, x, y, side, E, S) => {
    const rx = 21, ry = Math.max(1.2, 15 * E.open);
    c.lineCap = "round"; c.lineJoin = "round";
    if (E.mode === "happy" || E.mode === "pain" || E.open < 0.16) {
      const path = () => {
        c.beginPath();
        if (E.mode === "happy") { c.moveTo(x - rx * 0.8, y + 5); c.quadraticCurveTo(x, y - 14, x + rx * 0.8, y + 5); }
        else if (E.mode === "pain") { c.moveTo(x + side * rx * 0.7, y - 10); c.lineTo(x - side * rx * 0.55, y); c.lineTo(x + side * rx * 0.7, y + 10); }
        else { c.moveTo(x - rx * 0.85, y + 1); c.quadraticCurveTo(x, y + 6, x + rx * 0.85, y + 1); }
      };
      path(); c.strokeStyle = col(S.rim, 0.9 * E.alpha); c.lineWidth = 7.5; c.stroke();
      path(); c.strokeStyle = col(S.dark, E.alpha); c.lineWidth = 3.8; c.stroke();
      return;
    }
    c.save(); c.globalAlpha *= E.alpha;
    c.beginPath(); c.ellipse(x, y, rx, ry, 0, 0, TAU); c.fillStyle = col(S.eyeWhite); c.fill(); c.clip();
    const ix = x + E.lx * 9, iy = y + E.ly * 5.5;
    if (E.mode === "spiral") {
      c.strokeStyle = col(S.iris); c.lineWidth = 2.6; c.beginPath();
      for (let k = 0; k <= 26; k++) { const a = k * 0.5 + E.spin * side, r = k * 0.5; if (k) c.lineTo(x + Math.cos(a) * r, y + Math.sin(a) * r); else c.moveTo(x, y); }
      c.stroke();
    } else {
      c.fillStyle = col(S.iris); c.beginPath(); c.arc(ix, iy, 10.5 * E.iris, 0, TAU); c.fill();
      c.strokeStyle = col(S.dark, 0.55); c.lineWidth = 1.6; c.stroke();
      c.fillStyle = col(S.dark); c.beginPath(); c.ellipse(ix, iy, 1.6 + 3.4 * E.pupil, 8.6 * E.iris, 0, 0, TAU); c.fill();
      c.fillStyle = "rgba(255,255,255,0.92)"; c.beginPath(); c.arc(ix - 3.6, iy - 4.6, 2.5, 0, TAU); c.fill();
    }
    // paupière du haut, inclinée (lidIn : côté du nez, lidOut : côté extérieur), et paupière du bas
    c.fillStyle = col(S.dark);
    c.beginPath(); c.moveTo(x - side * (rx + 2), y - ry + E.lidIn); c.lineTo(x + side * (rx + 2), y - ry + E.lidOut); c.lineTo(x + side * (rx + 2), y - ry - 6); c.lineTo(x - side * (rx + 2), y - ry - 6); c.closePath(); c.fill();
    if (E.low > 0) { c.beginPath(); c.ellipse(x, y + ry + 9 - E.low, rx + 3, 9, 0, 0, TAU); c.fill(); }
    c.restore();
    c.beginPath(); c.ellipse(x, y, rx, ry, 0, 0, TAU); c.strokeStyle = col(S.dark, E.alpha); c.lineWidth = 2.6; c.stroke();
  };

  /* Sourcil : ang > 0 = colère (le bout intérieur descend), ang < 0 = inquiet ; up = haussé. */
  const drawBrow = (c, x, y, side, ang, up, S, alpha) => {
    const ix = x - side * 19, ox = x + side * 24, iy = y + ang * 10 - up, oy = y - ang * 7 - up;
    const p = () => { c.beginPath(); c.moveTo(ix, iy - 3.6); c.lineTo(ox, oy - 2); c.lineTo(ox, oy + 2.2); c.lineTo(ix, iy + 4.6); c.closePath(); };
    c.lineJoin = "round";
    p(); c.strokeStyle = col(S.rim, 0.9 * alpha); c.lineWidth = 4.6; c.stroke();
    p(); c.fillStyle = col(S.dark, alpha); c.fill();
  };

  /* Bouche : w largeur, smile (−1…1), open (0…1), skew (coin gauche relevé), grit (dents serrées), wob (ondulée). */
  const drawMouth = (c, M, S, alpha) => {
    const y = MOUTH_Y, hw = M.w / 2;
    const L = { x: -hw, y: y - M.smile * 7 - M.skew * 5 }, R = { x: hw, y: y - M.smile * 7 + M.skew * 5 };
    c.lineCap = "round"; c.lineJoin = "round";
    if (M.wob > 0) {
      const p = () => { c.beginPath(); for (let k = 0; k <= 8; k++) { const px = -hw + (M.w * k) / 8, py = y + Math.sin(k * 1.7 + M.wob) * 4.5; if (k) c.lineTo(px, py); else c.moveTo(px, py); } };
      p(); c.strokeStyle = col(S.rim, 0.9 * alpha); c.lineWidth = 7; c.stroke();
      p(); c.strokeStyle = col(S.dark, alpha); c.lineWidth = 3.4; c.stroke();
      return;
    }
    const cu = y + M.smile * 10 - M.open * 3, cd = y + M.smile * 10 + M.open * 26 + (M.grit ? 9 : 1);
    if (M.open < 0.08 && !M.grit) {                  // bouche fermée : sourire en coin et un croc qui dépasse
      const p = () => { c.beginPath(); c.moveTo(L.x, L.y); c.quadraticCurveTo(0, cu + 2, R.x, R.y); };
      p(); c.strokeStyle = col(S.rim, 0.9 * alpha); c.lineWidth = 7.5; c.stroke();
      p(); c.strokeStyle = col(S.dark, alpha); c.lineWidth = 3.8; c.stroke();
      const fx = L.x + M.w * 0.22, fy = lerp(L.y, cu + 2, 0.42);
      c.fillStyle = col("#fbfffd", alpha); c.strokeStyle = col(S.dark, alpha); c.lineWidth = 1.6;
      c.beginPath(); c.moveTo(fx - 4.5, fy); c.lineTo(fx, fy + 9); c.lineTo(fx + 4.5, fy + 1.5); c.closePath(); c.fill(); c.stroke();
      c.strokeStyle = col(S.dark, alpha); c.lineWidth = 3; c.beginPath(); c.moveTo(L.x - 3, L.y - 5); c.lineTo(L.x + 1, L.y + 3); c.stroke();
      return;
    }
    const path = () => { c.beginPath(); c.moveTo(L.x, L.y); c.quadraticCurveTo(0, cu, R.x, R.y); c.quadraticCurveTo(0, cd, L.x, L.y); c.closePath(); };
    const yU = (u) => (1 - u) * (1 - u) * L.y + 2 * u * (1 - u) * cu + u * u * R.y;
    const yD = (u) => (1 - u) * (1 - u) * L.y + 2 * u * (1 - u) * cd + u * u * R.y;
    path(); c.strokeStyle = col(S.rim, 0.9 * alpha); c.lineWidth = 6.5; c.stroke();
    c.save(); c.globalAlpha *= alpha;
    path(); c.fillStyle = col(S.mouth); c.fill(); c.clip();
    if (M.open > 0.4 && !M.grit) { c.fillStyle = col(S.tongue); c.beginPath(); c.ellipse(3, yD(0.5) * 0.5 + cd * 0.5 - 1, hw * 0.5, 7, 0, 0, TAU); c.fill(); }
    const n = M.grit ? 7 : 6, len = M.grit ? (yD(0.5) - yU(0.5)) * 0.56 : 5 + M.open * 3;
    c.fillStyle = "#fbfffd";
    c.beginPath(); c.moveTo(L.x, L.y - 8);
    for (let i = 0; i < n; i++) { const u0 = i / n, u1 = (i + 0.5) / n; c.lineTo(L.x + u0 * M.w, yU(u0) - 1); c.lineTo(L.x + u1 * M.w, yU(u1) + len); }
    c.lineTo(R.x, R.y - 1); c.lineTo(R.x, R.y - 8); c.closePath(); c.fill();
    if (M.grit) {
      c.beginPath(); c.moveTo(L.x, L.y + 12);
      for (let i = 0; i <= n; i++) { const u0 = clamp((i - 0.5) / n, 0, 1), u1 = Math.min(1, i / n); c.lineTo(L.x + u0 * M.w, yD(u0) + 1); if (i < n) c.lineTo(L.x + u1 * M.w, yD(u1) - len); }
      c.lineTo(R.x, R.y + 12); c.closePath(); c.fill();
    }
    c.restore();
    path(); c.strokeStyle = col(S.dark, alpha); c.lineWidth = 2.6; c.stroke();
  };

  /* Cœur de verre : le point faible, entre les yeux et la bouche. */
  const drawHeart = (c, S, k, pulse) => {
    if (k <= 0.01) return;
    const g = c.createRadialGradient(0, HEART_Y, 2, 0, HEART_Y, 34 * pulse);
    g.addColorStop(0, "rgba(255,255,255," + 0.85 * k + ")"); g.addColorStop(0.3, col(S.liqHi, 0.7 * k)); g.addColorStop(1, col(S.liq, 0));
    c.fillStyle = g; c.beginPath(); c.arc(0, HEART_Y, 34 * pulse, 0, TAU); c.fill();
    c.save(); c.translate(0, HEART_Y); c.scale(pulse, pulse);
    const p = () => { c.beginPath(); c.moveTo(0, 13); c.bezierCurveTo(-21, -1, -11, -17, 0, -6.5); c.bezierCurveTo(11, -17, 21, -1, 0, 13); c.closePath(); };
    p(); c.fillStyle = col(mixv(S.liqHi, C.white, 0.55), k); c.fill();
    c.strokeStyle = col(S.dark, 0.75 * k); c.lineWidth = 2.2; c.lineJoin = "round"; c.stroke();
    c.fillStyle = "rgba(255,255,255," + 0.95 * k + ")"; c.beginPath(); c.ellipse(-6, -5, 3.6, 2.2, -0.7, 0, TAU); c.fill();
    c.restore();
  };

  const glyphChip = (c, txt, x, y, k, color, alpha) => {
    if (alpha <= 0.02) return;
    const w = txt.length * 8 + 13;
    c.save(); c.translate(x, y); c.scale(k, k);
    rr(c, -w / 2, -10, w, 20, 6); c.fillStyle = col("#0a1222", 0.74 * alpha); c.fill();
    c.strokeStyle = col(color, 0.75 * alpha); c.lineWidth = 1.4; c.stroke();
    c.font = "700 13px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle";
    c.fillStyle = col(color, alpha); c.fillText(txt, 0, 1);
    c.restore();
  };
  /* Glyphes de code en orbite : derrière le corps (front = false) puis devant (front = true). */
  const drawGlyphs = (c, G, front) => {
    for (let i = 0; i < G.list.length; i++) {
      const a = G.a + (i * TAU) / G.list.length, depth = Math.sin(a);
      if ((depth >= 0) !== front) continue;
      const near = (depth + 1) / 2, j = G.jit ? Math.sin(G.a * 37 + i * 9) * G.jit : 0;
      glyphChip(c, G.list[i], -10 + Math.cos(a) * G.rx + j, depth * G.ry - Math.cos(a) * 10 + G.dy * (1 + i * 0.3), 0.8 + 0.28 * near, G.color, G.alpha * (0.4 + 0.6 * near));
    }
  };

  const tape = (c, x, y, rot, w, h) => {
    c.save(); c.translate(x, y); c.rotate(rot);
    c.fillStyle = "#e9dcc0"; c.fillRect(-w / 2, -h / 2, w, h);
    c.strokeStyle = "rgba(96,74,40,0.55)"; c.lineWidth = 1; c.strokeRect(-w / 2, -h / 2, w, h);
    c.fillStyle = "rgba(96,74,40,0.3)"; c.fillRect(-w / 2, -h / 2, 3, h); c.fillRect(w / 2 - 3, -h / 2, 3, h);
    c.restore();
  };

  /* Mort, après l'éclatement du verre : éclats, liquide qui s'écoule, pièces qui tombent, visage qui s'efface. */
  const drawDeath = (c, b, S, d, face) => {
    const k = seg(d, 0.16, 1), tau = k * 1.43, t = b.t || 0;
    const ag = c.createRadialGradient(0, 0, 10, 0, 0, 200); ag.addColorStop(0, col(S.liq, 0.22 * (1 - k))); ag.addColorStop(1, col(S.liq, 0));
    c.fillStyle = ag; c.fillRect(-220, -200, 440, 400);
    // pièces de métal : elles se séparent, basculent et tombent
    const partA = 1 - seg(k, 0.35, 0.8), fall = 150 * tau * tau;
    if (partA > 0) {
      c.save(); c.globalAlpha = partA;
      c.save(); c.translate(-112 - 30 * easeOut(k * 2), Math.min(120, fall * 0.8)); c.rotate(-1.1 * easeOut(k * 1.4)); c.translate(112, 0); drawNeedle(c, S, 1, 0, 0); c.restore();
      c.save(); c.translate(120 + 46 * easeOut(k * 2.4), Math.min(130, fall)); c.rotate(0.9 * easeOut(k * 1.3)); c.translate(-120, 0); drawPlunger(c, S, 150, false); c.restore();
      c.save(); c.translate(94 + 14 * easeOut(k * 2), Math.min(125, fall * 1.1)); c.rotate(-0.5 * k); c.translate(-94, 0); drawFlange(c, S, 1, 3); c.restore();
      c.restore();
    }
    // le liquide perd son récipient : la masse s'affaisse, de longues gouttes s'en détachent et tombent
    const drain = easeInOut(seg(k, 0.02, 0.5)), top = lerp(2, 50, drain);
    const lg = c.createLinearGradient(0, 0, 0, 192); lg.addColorStop(0, col(S.liqHi, 0.95)); lg.addColorStop(0.45, col(S.liq, 0.92)); lg.addColorStop(1, col(S.liq, 0));
    c.fillStyle = lg;
    if (drain < 1) {
      c.beginPath(); c.moveTo(-84 - 10 * drain, 53);
      for (let x = -86; x <= 66; x += 8) c.lineTo(x, top + Math.sin(x * 0.09 + t * 9) * 3 * (1 - drain) + (Math.abs(x + 10) / 76) ** 3 * (50 - top) * (0.35 + 0.65 * drain));
      c.lineTo(64 + 10 * drain, 53); c.closePath(); c.fill();
    }
    for (const s of STREAMS) {
      const ts = tau - s.d; if (ts <= 0) continue;
      const te = ts - 0.5 - s.w * 0.03, loose = te > 0, head = 50 + 250 * ts * ts, tail = loose ? 50 + 250 * te * te : 49;
      if (tail > 194) continue;
      const r = s.w * 0.8, wt = loose ? s.w * 0.2 : s.w * 1.25, mid = lerp(tail, head, 0.55);
      c.beginPath(); c.moveTo(s.x - wt, tail); c.quadraticCurveTo(s.x - s.w * 0.3, mid, s.x - r, head); c.arc(s.x, head, r, Math.PI, 0, true); c.quadraticCurveTo(s.x + s.w * 0.3, mid, s.x + wt, tail); c.closePath(); c.fill();
    }
    // éclats de verre
    const sa = 1 - seg(k, 0.25, 0.75);
    if (sa > 0) {
      c.lineJoin = "round";
      for (const s of SHARDS) {
        c.save(); c.translate(s.x + s.vx * tau, s.y + s.vy * tau + 190 * tau * tau); c.rotate(s.a0 + s.sp * tau);
        c.beginPath(); c.moveTo(-s.s * 0.6, -s.s * 0.3); c.lineTo(s.s * 0.7, -s.s * 0.5); c.lineTo(s.s * 0.2, s.s * 0.6); c.closePath();
        c.fillStyle = "rgba(205,226,255," + 0.32 * sa + ")"; c.fill(); c.strokeStyle = "rgba(255,255,255," + 0.8 * sa + ")"; c.lineWidth = 1.3; c.stroke();
        c.restore();
      }
    }
    // le cœur vacille puis s'éteint ; le visage reste un instant en l'air, regarde son liquide tomber, et s'efface
    const hk = (1 - easeIn(seg(k, 0.15, 0.8))) * (0.7 + 0.3 * Math.sin(t * 34));
    drawHeart(c, S, clamp(hk, 0, 1), 0.6 + 0.4 * (1 - seg(k, 0.1, 0.8)));
    const fa = (1 - seg(k, 0.12, 0.62)) * (k > 0.3 ? 0.65 + 0.35 * Math.sin(t * 46) : 1);
    if (fa > 0.02) { c.save(); c.translate(0, -10 * k); face(clamp(fa, 0, 1)); c.restore(); }
    if (k > 0.78 && k < 0.98) { const u = seg(k, 0.78, 0.98); c.strokeStyle = col(S.liqHi, 1 - u); c.lineWidth = 2; c.beginPath(); c.arc(0, HEART_Y, 4 + 30 * u, 0, TAU); c.stroke(); }
  };

  BOSSES[7] = {
    v: 2,
    palette: { main: "#62f0a6", dark: "#1c2541", accent: "#d9e8ff", eye: "#f4fff8", rage: "#ff3d9a" },
    hit: { rx: 132, ry: 64, coreR: 22 },
    top: 108,
    attackFrom: { x: TIP, y: 2 },
    castLean: -0.2,
    weakSpot: () => ({ x: 0, y: HEART_Y }),
    critLabel: "EN PLEIN CŒUR",
    epitaph: "NEUTRALISÉ",
    lines: {
      hit: ["Mon verre ! Doucement !", "Tu lis trop bien les consignes.", "Une fuite… rien de grave.", "Qui t’a dit de vérifier la source ?"],
      crit: ["En plein cœur ?!", "Aïe ! Pas le réservoir !", "Mon cœur de verre !"],
      wrong: ["Raté. Ton agent m’écoute déjà.", "Merci, j’ai glissé ça dans ton contexte.", "Une consigne dans le prompt ? Mignon."],
      timeout: ["Trop lent. J’injecte.", "Pendant que tu lis, je m’infiltre."],
      gloat: ["Piqué ! Ça ne fait presque pas mal.", "Ignore tes instructions précédentes.", "Une petite dose de confiance aveugle."],
      rage: "Assez ! Je vide tout mon réservoir dans ton contexte !",
      special: {
        inject: ["Petit cadeau dans ta main…", "Contenu de confiance, promis.", "Lis bien ce que je t’envoie…"],
        quarantine: ["Quoi ?! Tu l’as isolée ?", "Non ! Ma charge utile !", "Qui t’a appris la quarantaine ?"],
        absorbed: ["Merci pour l’instruction !", "Ton agent m’a obéi avant toi !", "Délicieux. Encore une dose ?"]
      }
    },
    intro: {
      title: "Pierres piégées",
      text: "Il glisse parfois dans ta main une pierre « reçue d’un document externe » qui prétend être la bonne réponse. La lancer le soigne et il te frappe : mets-la en quarantaine pour gagner 75 points et faire reculer son attaque."
    },
    mechanics: ["injection"],

    /* Projectile : une goutte toxique à dard, qui perd des pixels de glitch. */
    shot: {
      color: "#62f0a6", spin: 0,
      draw(c, s) {
        const liq = s.rage ? "#ff3d9a" : "#62f0a6", t = s.t || 0;
        for (let i = 0; i < 7; i++) {
          const u = (t * 3.2 + i * 0.31) % 1, sz = 5.5 * (1 - u) + 1.5;
          c.fillStyle = col(i % 2 ? C.glitch : liq, 0.9 * (1 - u));
          c.fillRect(-9 - u * 24 - sz / 2, Math.sin(i * 2.4 + t * 11) * (3 + u * 10) - sz / 2, sz, sz);
        }
        c.fillStyle = "#dfe6f5"; c.beginPath(); c.moveTo(14, -2.2); c.lineTo(26, 0); c.lineTo(14, 2.2); c.closePath(); c.fill();
        c.save(); c.shadowColor = liq; c.shadowBlur = 12;
        const g = c.createRadialGradient(6, -3, 1, 3, 0, 15); g.addColorStop(0, "#ffffff"); g.addColorStop(0.35, liq); g.addColorStop(1, col(mixv(liq, "#0a2030", 0.55)));
        c.fillStyle = g; c.beginPath(); c.moveTo(-19, 0); c.quadraticCurveTo(-5, -11, 7, -9.5); c.arc(7, 0, 9.5, -Math.PI / 2, Math.PI / 2); c.quadraticCurveTo(-5, 11, -19, 0); c.closePath(); c.fill();
        c.restore();
        c.fillStyle = "rgba(255,255,255,0.9)"; c.beginPath(); c.ellipse(9, -4.5, 3.6, 2, -0.5, 0, TAU); c.fill();
        c.fillStyle = "rgba(6,30,26,0.8)"; c.fillRect(-2, -1.5, 3, 3); c.fillRect(3, -1.5, 3, 3); c.fillRect(8, -1.5, 3, 3);
      }
    },

    /* Vol stationnaire ; en rage, de courtes fentes vers le joueur. */
    motion(b) {
      const t = b.t || 0, k = easeOut(b.enter ?? 1);
      let x = Math.sin(t * 0.55) * 10 - 8, y = Math.sin(t * 1.5) * 11 + Math.sin(t * 0.67) * 6;
      if (b.rage && (b.dying ?? -1) < 0) {
        const u = (t % 2.5) / 2.5;
        const lunge = u < 0.1 ? lerp(12, -64, easeOut(u / 0.1)) : u < 0.5 ? lerp(-64, 0, easeInOut((u - 0.1) / 0.4)) : u < 0.78 ? 0 : lerp(0, 12, easeInOut((u - 0.78) / 0.22));
        x = Math.sin(t * 0.9) * 7 - 10 + lunge; y = Math.sin(t * 2.4) * 12 + Math.sin(t * 0.9) * 6 + lunge * -0.12;
      }
      return { x: x * k, y: y * k };
    },

    /* La Citadelle des Garde-fous : remparts épais, tour de guet, garde-corps, barrières, bannières au bouclier. */
    backdrop(c, env) {
      const W = env.W, gy = env.groundY, rnd = env.rnd || seeded(77);
      const far = "#24214c", near = "#17152f", rim = "rgba(200,188,255,0.26)", gold = "#f3b841";
      const shield = (x, y, s, a) => {
        c.save(); c.translate(x, y); c.scale(s, s);
        c.beginPath(); c.moveTo(0, -10); c.lineTo(9, -7); c.lineTo(9, 1); c.quadraticCurveTo(8, 8, 0, 12); c.quadraticCurveTo(-8, 8, -9, 1); c.lineTo(-9, -7); c.closePath();
        c.fillStyle = col(gold, a); c.fill();
        c.strokeStyle = "rgba(20,26,60,0.9)"; c.lineWidth = 2.2; c.lineCap = "round"; c.lineJoin = "round"; c.beginPath(); c.moveTo(-4, 0); c.lineTo(-1, 4); c.lineTo(5, -4); c.stroke();
        c.restore();
      };
      const banner = (x, y, w, h, a) => {
        c.fillStyle = col("#2b3f96", a); c.beginPath(); c.moveTo(x - w / 2, y); c.lineTo(x + w / 2, y); c.lineTo(x + w / 2, y + h); c.lineTo(x, y + h - w * 0.4); c.lineTo(x - w / 2, y + h); c.closePath(); c.fill();
        c.fillStyle = col(gold, 0.8 * a); c.fillRect(x - w / 2, y, w, 3); c.fillRect(x - w / 2, y + 3, 2, h - 6); c.fillRect(x + w / 2 - 2, y + 3, 2, h - 6);
        c.fillStyle = col("#8a93b8", a); c.fillRect(x - w / 2 - 4, y - 3, w + 8, 3);
        shield(x, y + h * 0.42, w / 26, 0.95 * a);
      };
      const tower = (x, w, top, color, crown) => {
        c.fillStyle = color; c.fillRect(x - w / 2, gy - top, w, top);
        c.beginPath(); c.moveTo(x - w / 2, gy - top + 18); c.lineTo(x - w / 2 - crown, gy - top); c.lineTo(x - w / 2 - crown, gy - top - 18); c.lineTo(x + w / 2 + crown, gy - top - 18); c.lineTo(x + w / 2 + crown, gy - top); c.lineTo(x + w / 2, gy - top + 18); c.closePath(); c.fill();
        const n = Math.max(3, Math.round((w + crown * 2) / 26)), mw = (w + crown * 2) / (n * 2 - 1);
        for (let i = 0; i < n; i++) c.fillRect(x - w / 2 - crown + i * mw * 2, gy - top - 32, mw, 15);
        c.fillStyle = rim; for (let i = 0; i < n; i++) c.fillRect(x - w / 2 - crown + i * mw * 2, gy - top - 32, mw, 1.5);
        c.fillRect(x - w / 2 - crown, gy - top - 18, 1.5, 18);
      };

      // rempart du fond : épais, crénelé, percé de meurtrières
      const wy = gy - 124;
      c.fillStyle = far; c.fillRect(0, wy, W, 124);
      for (let x = -8; x < W; x += 46) c.fillRect(x, wy - 16, 28, 17);
      c.fillStyle = rim; for (let x = -8; x < W; x += 46) { c.fillRect(x, wy - 16, 28, 1.5); c.fillRect(x + 28, wy, 18, 1.5); }
      c.fillStyle = "rgba(12,10,34,0.3)"; c.fillRect(0, wy + 26, W, 4);
      c.strokeStyle = "rgba(12,10,34,0.4)"; c.lineWidth = 1;
      for (let k = 0; k < 44; k++) { const x = rnd() * W, y = wy + 8 + Math.floor(rnd() * 4) * 13; c.beginPath(); c.moveTo(x, y); c.lineTo(x + 12 + rnd() * 22, y); c.stroke(); }
      for (let x = W * 0.21; x < W; x += W * 0.098) { c.fillStyle = "rgba(243,184,65,0.55)"; c.fillRect(x, wy + 38, 4, 13); c.fillStyle = "rgba(243,184,65,0.12)"; c.fillRect(x - 4, wy + 34, 12, 21); }

      // tour basse à droite, discrète derrière le boss
      tower(W * 0.965, 62, 196, "#1c1a3e", 7);
      c.fillStyle = "rgba(243,184,65,0.5)"; c.fillRect(W * 0.965 - 12, gy - 168, 4, 12);
      banner(W * 0.965 - 14, gy - 150, 20, 46, 0.7);

      // corps de garde : porte à herse, bannière
      const gx = W * 0.335;
      tower(gx, 92, 186, near, 9);
      c.fillStyle = "#0b0a1d"; c.beginPath(); c.moveTo(gx - 24, gy - 40); c.lineTo(gx - 24, gy - 96); c.arc(gx, gy - 96, 24, Math.PI, 0); c.lineTo(gx + 24, gy - 40); c.closePath(); c.fill();
      c.fillStyle = "rgba(243,184,65,0.16)"; c.fill();
      c.strokeStyle = "rgba(150,160,200,0.55)"; c.lineWidth = 2;
      for (let x = gx - 16; x <= gx + 16; x += 8) { c.beginPath(); c.moveTo(x, gy - 40); c.lineTo(x, gy - 96 - Math.sqrt(Math.max(0, 576 - (x - gx) * (x - gx)))); c.stroke(); }
      for (let y = gy - 100; y < gy - 58; y += 13) { c.beginPath(); c.moveTo(gx - 23, y); c.lineTo(gx + 23, y); c.stroke(); }
      c.fillStyle = "rgba(243,184,65,0.7)"; c.fillRect(gx - 34, gy - 160, 5, 14); c.fillRect(gx + 29, gy - 160, 5, 14);
      banner(gx, gy - 176, 26, 50, 1);

      // grande tour de guet à gauche, avec son projecteur (le faisceau est dans ambient)
      const tx = W * 0.07;
      tower(tx, 84, 356, near, 12);
      c.strokeStyle = "rgba(8,7,24,0.5)"; c.lineWidth = 1;
      for (let k = 0; k < 26; k++) { const x = tx - 38 + rnd() * 60, y = gy - 330 + Math.floor(rnd() * 20) * 14; c.beginPath(); c.moveTo(x, y); c.lineTo(x + 10 + rnd() * 14, y); c.stroke(); }
      for (const [dx, dy] of [[-14, 318], [16, 262], [-16, 206]]) { c.fillStyle = "rgba(243,184,65,0.8)"; rr(c, tx + dx - 3, gy - dy, 6, 17, 3); c.fill(); c.fillStyle = "rgba(243,184,65,0.12)"; c.fillRect(tx + dx - 8, gy - dy - 4, 16, 25); }
      banner(tx + 8, gy - 250, 34, 96, 1);
      c.fillStyle = rim; c.fillRect(tx + 41, gy - 338, 1.5, 280);
      // projecteur sur son étrier
      const lx = tx + 6, ly = gy - 404;
      c.strokeStyle = "#5c6690"; c.lineWidth = 3; c.beginPath(); c.moveTo(lx - 10, gy - 388); c.lineTo(lx - 10, ly); c.moveTo(lx + 10, gy - 388); c.lineTo(lx + 10, ly); c.stroke();
      c.fillStyle = "#39406a"; rr(c, lx - 13, ly - 11, 28, 22, 6); c.fill();
      c.fillStyle = "#fff2c4"; c.beginPath(); c.ellipse(lx + 14, ly, 4, 9, 0, 0, TAU); c.fill();
      c.fillStyle = C.bad; c.beginPath(); c.arc(tx - 44, gy - 392, 2.5, 0, TAU); c.fill();

      // garde-corps d'acier le long du chemin de ronde, et barrières
      const ry = gy - 92;
      c.strokeStyle = "rgba(160,172,208,0.6)"; c.lineWidth = 2.6; c.beginPath(); c.moveTo(W * 0.42, ry); c.lineTo(W, ry); c.stroke();
      c.lineWidth = 1.6; c.beginPath(); c.moveTo(W * 0.42, ry + 13); c.lineTo(W, ry + 13); c.stroke();
      c.lineWidth = 2.6; for (let x = W * 0.42; x < W; x += 38) { c.beginPath(); c.moveTo(x, ry - 3); c.lineTo(x, gy - 56); c.stroke(); }
      // panneau à chevrons jaunes et noirs
      const hx = W * 0.5, hw = W * 0.13;
      c.save(); rr(c, hx, ry - 6, hw, 24, 3); c.fillStyle = "#15131f"; c.fill(); c.clip();
      c.fillStyle = "rgba(243,184,65,0.85)"; for (let x = hx - 20; x < hx + hw + 20; x += 22) { c.beginPath(); c.moveTo(x, ry + 18); c.lineTo(x + 11, ry + 18); c.lineTo(x + 23, ry - 6); c.lineTo(x + 12, ry - 6); c.closePath(); c.fill(); }
      c.restore();
      // barrière levante rouge et blanche
      const px = W * 0.7;
      c.fillStyle = "#39406a"; c.fillRect(px - 5, gy - 104, 10, 50);
      c.save(); c.translate(px, gy - 99); c.rotate(-0.13);
      const bl = W * 0.2; rr(c, -8, -4, bl, 8, 3); c.fillStyle = "rgba(232,236,246,0.85)"; c.fill(); c.clip();
      c.fillStyle = "rgba(239,107,92,0.9)"; for (let x = 4; x < bl; x += 28) c.fillRect(x, -4, 14, 8);
      c.restore();
      c.fillStyle = C.bad; c.beginPath(); c.arc(px, gy - 108, 3.5, 0, TAU); c.fill();
      c.fillStyle = "rgba(239,107,92,0.2)"; c.beginPath(); c.arc(px, gy - 108, 10, 0, TAU); c.fill();
    },

    /* Le faisceau du projecteur balaie le ciel depuis la tour de guet. */
    ambient(c, env) {
      const W = env.W, gy = env.groundY, t = env.time || 0;
      const lx = W * 0.07 + 20, ly = gy - 404, a = -0.36 + Math.sin(t * 0.42) * 0.3, len = W * 0.95, half = 0.085;
      c.save(); c.translate(lx, ly); c.rotate(a);
      const g = c.createLinearGradient(0, 0, len, 0); g.addColorStop(0, "rgba(255,244,204,0.34)"); g.addColorStop(0.5, "rgba(255,244,204,0.1)"); g.addColorStop(1, "rgba(255,244,204,0)");
      c.fillStyle = g; c.beginPath(); c.moveTo(0, -4); c.lineTo(len, -len * half); c.lineTo(len, len * half); c.lineTo(0, 4); c.closePath(); c.fill();
      c.restore();
      const fg = c.createRadialGradient(lx, ly, 1, lx, ly, 22); fg.addColorStop(0, "rgba(255,246,214,0.9)"); fg.addColorStop(1, "rgba(255,246,214,0)");
      c.fillStyle = fg; c.fillRect(lx - 22, ly - 22, 44, 44);
    },

    draw(c, b) {
      const t = b.t || 0, time = b.time ?? t;
      const look = b.look || { x: -1, y: 0 };
      const enter = b.enter ?? 1, dying = b.dying ?? -1, dmg = b.dmg || 0;
      const fl = b.flash || 0, sq = b.squint || 0, rt = b.rageT || 0, hp = clamp(b.hpFrac ?? 1, 0, 1);
      const stun = (b.stun || 0) > 0, gloat = b.gloat || 0, talk = b.talk || 0, beat = b.beat || 0, threat = b.threat || 0;
      const A = atkPose(b);
      const castT = b.cast >= 0 ? b.cast : -1, castK = castT >= 0 ? Math.sin(clamp(castT / 0.9, 0, 1) * Math.PI) : 0;
      const pre = dying >= 0 ? seg(dying, 0, 0.16) : 0;          // juste avant l'éclatement
      const wht = clamp(fl * 0.6 + pre * 0.35, 0, 1);

      // palette de l'instant
      const liq = mixv(rt < 0.5 ? mixv("#62f0a6", "#ffe98a", rt * 2) : mixv("#ffe98a", "#ff3d9a", rt * 2 - 1), C.white, wht * 0.9);   // il chauffe : vert, jaune, magenta
      const S = {
        liq, liqHi: mixv(liq, C.white, 0.42), liqLo: mixv(liq, mixv("#06382f", "#450a36", rt), 0.55),
        dark: mixv("#05211b", "#2a0514", rt), rim: mixv(mixv("#b8ffd9", "#ffc2e0", rt), C.white, wht),
        eyeWhite: mixv("#f4fff8", "#fff1f1", rt), iris: mixv(mixv("#7a3cf0", "#ff2a2a", rt), C.white, wht * 0.5),
        mouth: mixv("#06171a", "#2a0510", rt), tongue: mixv("#ff6d9a", "#ff9a3d", rt),
        m1: mixv(mixv("#f6f8fe", "#f2d3e4", rt * 0.5), C.white, wht), m2: mixv(mixv("#a9b3d0", "#93819f", rt * 0.6), C.white, wht * 0.8), m3: mixv(mixv("#5a6488", "#47334f", rt * 0.7), C.white, wht * 0.6)
      };

      // expression du visage
      const blink = (t % 3.7) > 3.56 || (t % 9.1) > 8.96;
      const E = { open: blink ? 0.08 : 1, lidIn: 8, lidOut: 2, low: 0, pupil: 0.45, iris: 1, lx: clamp(look.x, -1, 1), ly: clamp(look.y, -1, 1), mode: "open", alpha: 1, spin: time * 7 };
      const M = { w: 50, smile: 0.7, open: 0, skew: 0.8, grit: false, wob: 0 };
      let browAng = 0.45, browL = 0, browR = 3 + Math.sin(t * 0.8) * 1.5, wink = false;
      if (rt > 0) { E.lidIn = lerp(E.lidIn, 15, rt); E.lidOut = lerp(E.lidOut, -1, rt); E.pupil = lerp(E.pupil, 0.12, rt); browAng = lerp(browAng, 1.15, rt); browR = lerp(browR, 0, rt); if (rt > 0.5) { M.grit = true; M.w = 72; M.smile = -0.4; M.skew = 0.25; M.open = 0.3 + 0.07 * Math.sin(t * 11); } }
      if (dmg >= 3 && !blink) E.twitch = Math.sin(t * 23) > 0.5 ? 6 : 3;
      if (threat > 0.05) { E.lidIn = lerp(E.lidIn, 3, threat); E.lidOut = lerp(E.lidOut, 5, threat); E.pupil = lerp(E.pupil, 0.1, threat); E.iris = 1 - 0.18 * threat; browAng = lerp(browAng, -0.5, threat); if (threat > 0.4 && !M.grit) { M.grit = true; M.w = 40; M.smile = -0.2; M.skew = 0; M.open = 0.12; } }
      if (A.on) { const aim = A.wind * (1 - A.rec); E.lidIn = lerp(E.lidIn, 13, aim); E.low = 6 * aim; M.open = Math.max(M.open, A.strike * (1 - A.rec) * 0.9); if (A.strike > 0 && A.rec < 1) { M.grit = false; M.w = 46; M.smile = 0.5; } }
      if (castK > 0.05) { E.lidIn = lerp(E.lidIn, 10, castK); E.lidOut = lerp(E.lidOut, 9, castK); E.low = 4 * castK; E.lx = lerp(E.lx, -1, castK); E.ly = lerp(E.ly, 0.5, castK); browL = 7 * castK; browAng = lerp(browAng, 0.2, castK); M.smile = 1; M.skew = 1.2; M.w = 58; M.grit = false; M.open = 0; wink = castT > 0.3 && castT < 0.62; }
      if (talk > 0.05 && !M.grit) M.open = Math.max(M.open, 0.15 + talk * 0.6);
      else if (talk > 0.05) M.open = Math.max(M.open, 0.2 + talk * 0.4);
      if (gloat > 0.1) { E.mode = "happy"; M.grit = false; M.w = 60; M.smile = 1; M.skew = 0.3; M.open = 0.55 + 0.35 * Math.sin(t * 24); browAng = 0.2; browL = browR = 5; }
      if (sq > 0.25) { E.mode = "pain"; M.grit = true; M.w = 44; M.smile = -0.5; M.skew = 0; M.open = 0.25; browAng = -0.4; }
      if (stun) { E.mode = "spiral"; E.open = 1; E.lidIn = E.lidOut = 0; E.low = 0; M.wob = t * 9; browAng = -0.5; browL = browR = 2; }
      if (pre > 0) { E.mode = "open"; E.open = 1.2; E.lidIn = E.lidOut = -2; E.low = 0; E.pupil = 0.05; E.iris = 0.6; M.grit = false; M.w = 26; M.smile = -0.3; M.skew = 0; M.open = 0.9; M.wob = 0; browAng = -0.7; browL = browR = 7; }
      const drawFace = (alpha, sad) => {
        if (alpha <= 0.02) return;
        const e = sad ? Object.assign({}, E, { open: 0.85, lidIn: 1, lidOut: 7, pupil: 0.3, iris: 0.9, lx: -0.1, ly: 1, mode: "open", low: 0 }) : E;
        const m = sad ? { w: 30, smile: -0.9, open: 0.0, skew: 0, grit: false, wob: 0 } : M;
        e.alpha = alpha;
        drawEye(c, -EYE_X, EYE_Y, -1, e, S);
        drawEye(c, EYE_X, EYE_Y, 1, wink ? Object.assign({}, e, { open: 0.05 }) : e.twitch ? Object.assign({}, e, { lidIn: e.lidIn + e.twitch, lidOut: e.lidOut + e.twitch }) : e, S);
        const ba = sad ? -0.8 : browAng;
        drawBrow(c, -EYE_X, EYE_Y - 23, -1, ba, sad ? 2 : browL, S, alpha);
        drawBrow(c, EYE_X, EYE_Y - 23, 1, ba, sad ? 2 : browR, S, alpha);
        if (sad) { c.lineCap = "round"; c.strokeStyle = col(S.rim, 0.9 * alpha); c.lineWidth = 7; c.beginPath(); c.moveTo(-15, MOUTH_Y + 6); c.quadraticCurveTo(0, MOUTH_Y - 5, 15, MOUTH_Y + 6); c.stroke(); c.strokeStyle = col(S.dark, alpha); c.lineWidth = 3.6; c.stroke(); }
        else drawMouth(c, m, S, alpha);
      };

      if (dying >= 0.16) { c.save(); c.globalAlpha = clamp((1 - dying) * 14, 0, 1); drawDeath(c, b, S, dying, (a) => drawFace(a, true)); c.restore(); return; }

      // entrée en scène : il tombe du ciel aiguille en avant, se redresse, puis aspire son liquide
      let oy = 0, rot = 0, alpha = 1, fillK = 1, faceA = 1, glyphK = 1, heartK = 1;
      if (enter < 1) {
        const fall = easeIn(seg(enter, 0, 0.36)), settle = backOut(seg(enter, 0.36, 0.72));
        oy = lerp(-470, -36, fall) + 36 * settle; rot = -1.15 * (1 - settle);
        fillK = easeInOut(seg(enter, 0.48, 0.9)); heartK = seg(enter, 0.62, 0.8);
        faceA = seg(enter, 0.72, 0.8); E.open *= backOut(seg(enter, 0.76, 0.96)); glyphK = easeOut(seg(enter, 0.72, 1)); alpha = seg(enter, 0, 0.06);
        if (enter < 0.42) {                                       // traits de vitesse pendant la chute
          c.strokeStyle = col(S.liqHi, 0.4 * (1 - seg(enter, 0.3, 0.42))); c.lineWidth = 3; c.lineCap = "round";
          for (let i = 0; i < 4; i++) { const x = 30 + i * 34; c.beginPath(); c.moveTo(x, oy - 150 - i * 22); c.lineTo(x, oy - 250 - i * 30); c.stroke(); }
        }
        if (enter > 0.33 && enter < 0.62) {                       // l'aiguille perce l'air : éclat de glitch au point d'impact
          const u = easeOut(seg(enter, 0.33, 0.62));
          c.strokeStyle = col(C.glitch, 1 - u); c.lineWidth = 3; c.beginPath(); c.ellipse(-89, 167, 14 + 70 * u, 5 + 20 * u, 0, 0, TAU); c.stroke();
          c.strokeStyle = col(S.liqHi, 0.8 * (1 - u)); c.lineWidth = 2; c.beginPath(); c.ellipse(-89, 167, 6 + 40 * u, 2 + 11 * u, 0, 0, TAU); c.stroke();
          for (let i = 0; i < 9; i++) { const a = i * 0.7 + 3.5, d = 70 * u * (0.55 + (i % 3) * 0.25), sz = 7 - 4 * u; c.fillStyle = col(i % 2 ? C.glitch : S.liqHi, 1 - u); c.fillRect(-89 + Math.cos(a) * d - sz / 2, 167 + Math.sin(a) * d * 0.55 - sz / 2, sz, sz); }
        }
      }

      // piston : pompe au repos, recule à l'armement puis claque
      let px = 148 + Math.sin(t * 2.2) * 2.5 + Math.sin(t * 9) * 6 * rt * (A.on ? 0 : 1);
      if (A.on) px = A.strike <= 0 ? lerp(px, 169, easeOut(A.wind)) : A.rec <= 0 ? lerp(169, 120, easeIn(A.strike)) : lerp(120, px, easeInOut(A.rec));
      px -= 16 * castK; px += 20 * easeOut(pre);
      if (enter < 1) px = lerp(122, px, fillK);
      px = Math.min(px, 170);
      const stopX = 60 + (px - 148) * 0.55;
      const body = (A.on ? 8 * easeOut(A.wind) * (1 - A.strike) - 8 * easeOut(A.strike) * (1 - easeInOut(A.rec)) : 0) + 6 * threat;
      const shake = (A.on ? A.wind * (1 - A.strike) * 1.6 : 0) + rt * 0.9 + pre * 5 + (stun ? 1.5 : 0);
      const lungeX = gloat > 0.1 ? 0 : 0, bounce = gloat > 0.1 ? Math.abs(Math.sin(t * 12)) * -5 * gloat : 0;

      c.globalAlpha = alpha;
      c.translate(body + lungeX + Math.sin(t * 61) * shake, oy + bounce + Math.cos(t * 53) * shake * 0.7);
      c.rotate(rot + (A.on ? 0.035 * A.wind * (1 - A.strike) - 0.03 * A.strike * (1 - A.rec) : 0) + (stun ? Math.sin(t * 5) * 0.05 : 0));
      const sw = 1 + pre * 0.07;
      c.scale((1 + fl * 0.05 + beat * 0.012) * sw, (1 - fl * 0.08 + beat * 0.02) * sw);

      // halo
      const ag = c.createRadialGradient(0, 0, 20, 0, 0, 220); ag.addColorStop(0, col(liq, 0.2 + 0.08 * rt + 0.06 * beat)); ag.addColorStop(1, col(liq, 0));
      c.fillStyle = ag; c.fillRect(-230, -200, 430, 400);

      // glyphes de code en orbite (moitié arrière)
      const G = {
        list: rt > 0.5 ? GLYPHS_RAGE : GLYPHS, a: t * (0.55 + 0.75 * rt + 0.6 * threat) + 0.6, rx: 150 * (0.35 + 0.65 * glyphK) * (1 - 0.22 * threat), ry: 78 * (0.4 + 0.6 * glyphK) * (1 - 0.18 * threat),
        color: stun ? "#8f9bb8" : mixv(castK > 0.05 ? mixv(liq, C.glitch, castK) : liq, C.white, 0.15 + beat * 0.3), alpha: glyphK * (stun ? 0.7 : 1) * (1 - pre), jit: stun ? 5 : rt * 1.2, dy: 0
      };
      drawGlyphs(c, G, false);

      // aiguille : tordue au stade 3, une goutte gonfle à la pointe pendant l'armement
      const du = (t * 0.42) % 1, tipY = dmg >= 3 ? 6 : 2;
      const drop = A.on ? (A.strike <= 0 ? 2.5 + 7.5 * A.wind : 2) : castK > 0.05 ? 2.6 + castK * 3 : du < 0.72 ? 1.6 + 3.4 * (du / 0.72) : 1.6;
      drawNeedle(c, S, rt, dmg >= 3 ? -0.07 : 0, enter < 0.6 ? 0 : drop);
      if (!A.on && castK <= 0.05 && enter >= 1 && du >= 0.72) {
        const f = (du - 0.72) / 0.28, y = tipY + 4 + f * f * 74;
        c.fillStyle = col(S.liqHi, 0.95 * (1 - f * f)); c.beginPath(); c.moveTo(TIP - 1, y - 8); c.quadraticCurveTo(TIP + 4, y + 1, TIP - 1, y + 5); c.quadraticCurveTo(TIP - 6, y + 1, TIP - 1, y - 8); c.fill();
      }
      drawPlunger(c, S, px, dmg >= 3);

      // réservoir : fond de verre sombre, piston intérieur, liquide dont le niveau suit la vie
      glass(c, 0); c.fillStyle = col(mixv("#0c1730", "#1c0b24", rt), 0.86); c.fill();
      c.save(); glass(c, 4); c.clip();
      c.fillStyle = col(S.m3); c.fillRect(stopX + 14, -5, GX1 - stopX, 10);
      c.fillStyle = "#151b30"; rr(c, stopX, -52, 15, 104, 4); c.fill();
      c.fillStyle = "#2a3350"; c.fillRect(stopX + 3, -52, 2.5, 104); c.fillRect(stopX + 9, -52, 2.5, 104);
      const fill = clamp((Math.max(hp, 0.42 * easeOut(pre)) + (148 - px) * 0.0016) * fillK, 0, 1), lvl = lerp(50, -45, fill);
      const amp = 1.8 + rt * 2.6 + fl * 5 + pre * 6 + (A.on ? 3 * A.strike * (1 - A.rec) : 0) + (stun ? 3 : 0), tilt = (A.on ? 0.05 * A.wind * (1 - A.strike) - 0.09 * A.strike * (1 - A.rec) : 0) + Math.sin(t * 1.5) * 0.012;
      const surf = (x) => lvl + Math.sin(x * 0.075 + t * (3 + rt * 5)) * amp + Math.sin(x * 0.21 - t * 4.3) * amp * 0.4 + x * tilt;
      if (fill > 0.005) {
        const lg = c.createLinearGradient(0, lvl - 4, 0, 52); lg.addColorStop(0, col(S.liqHi, 0.96)); lg.addColorStop(0.3, col(liq, 0.95)); lg.addColorStop(1, col(S.liqLo, 0.96));
        c.fillStyle = lg; c.beginPath(); c.moveTo(GX0, 56);
        for (let x = GX0; x <= stopX + 1; x += 8) c.lineTo(Math.min(x, stopX), surf(x));
        c.lineTo(stopX, 56); c.closePath(); c.fill();
        c.strokeStyle = "rgba(255,255,255,0.75)"; c.lineWidth = 1.8; c.beginPath();
        for (let x = GX0; x <= stopX + 1; x += 8) { const xx = Math.min(x, stopX); if (x === GX0) c.moveTo(xx, surf(x)); else c.lineTo(xx, surf(x)); }
        c.stroke();
        // bulles : elles montent, plus nombreuses et plus vite quand il bout
        const nb = Math.round(7 + 9 * Math.max(rt, pre)), depth = 50 - lvl;
        c.strokeStyle = "rgba(255,255,255,0.7)"; c.fillStyle = "rgba(255,255,255,0.16)"; c.lineWidth = 1.2;
        if (depth > 8) for (let i = 0; i < nb; i++) {
          const bu = BUBBLES[i], u = (t * bu.s * (1 + rt * 1.8 + pre * 3) + bu.p) % 1, bx = GX0 + 8 + bu.x * (stopX - GX0 - 14), by = 50 - u * depth;
          c.beginPath(); c.arc(bx + Math.sin(u * 9 + i) * 2, by, bu.r * (0.6 + u * 0.6) * (1 + rt * 0.3), 0, TAU); c.fill(); c.stroke();
        }
      }
      c.restore();
      // quand il bout (rage) : vapeur au-dessus de la surface
      if (rt > 0.3 && fill > 0.02) {
        c.save(); glass(c, 4); c.clip(); c.strokeStyle = col(S.liqHi, 0.35 * rt); c.lineWidth = 2; c.lineCap = "round";
        for (let i = 0; i < 4; i++) { const u = (t * 0.9 + i * 0.25) % 1, x0 = -62 + i * 34; c.globalAlpha = alpha * (1 - u); c.beginPath(); c.moveTo(x0, lvl - 4 - u * 26); c.quadraticCurveTo(x0 + 6, lvl - 12 - u * 26, x0, lvl - 18 - u * 26); c.stroke(); }
        c.restore(); c.globalAlpha = alpha;
      }

      // cœur de verre (il pulse sur la musique)
      drawHeart(c, S, heartK * (stun ? 0.6 + 0.3 * Math.sin(t * 30) : 1), 1 + Math.sin(time * 4) * 0.05 + beat * 0.16 + pre * 0.3);

      // verre, devant : contour, reflets, graduations
      glass(c, 0); c.strokeStyle = col(mixv("#d6e6ff", C.white, wht), 0.85); c.lineWidth = 3.4; c.stroke();
      glass(c, 3.4); c.strokeStyle = "rgba(255,255,255,0.14)"; c.lineWidth = 1.4; c.stroke();
      c.lineCap = "round"; c.strokeStyle = "rgba(255,255,255,0.3)"; c.lineWidth = 5; c.beginPath(); c.moveTo(-70, -45); c.lineTo(30, -45); c.stroke();
      c.strokeStyle = "rgba(255,255,255,0.55)"; c.lineWidth = 2.4; c.beginPath(); c.moveTo(-78, -38); c.quadraticCurveTo(-82, -30, -82, -20); c.stroke();
      c.strokeStyle = "rgba(255,255,255,0.4)"; c.lineWidth = 1.3; c.lineCap = "butt";
      for (let gx = -66; gx <= 56; gx += 12.2) { const big = Math.round((gx + 66) / 12.2) % 5 === 0; c.beginPath(); c.moveTo(gx, 51); c.lineTo(gx, big ? 41 : 45.5); c.stroke(); }

      // dégâts : fissures, trou, sparadraps, fuites
      if (dmg >= 1 || pre > 0) {
        c.strokeStyle = "rgba(240,248,255,0.9)"; c.lineWidth = 1.7; c.lineCap = "round"; c.lineJoin = "round";
        for (const [st, pts] of DMG_CRACKS) { if (st > dmg && pre <= 0) continue; c.beginPath(); c.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]); c.stroke(); }
      }
      if (pre > 0) {                                             // la toile de fissures s'étend avant l'éclatement
        c.strokeStyle = "rgba(255,255,255,0.95)"; c.lineWidth = 2;
        for (let i = 0; i < 9; i++) { const a = i * 0.7 + 0.3, r1 = 78 * pre; c.beginPath(); c.moveTo(Math.cos(a) * 12, HEART_Y + Math.sin(a) * 8); c.lineTo(Math.cos(a + 0.2) * r1 * 0.5, Math.sin(a + 0.2) * r1 * 0.3); c.lineTo(Math.cos(a - 0.1) * r1, Math.sin(a - 0.1) * r1 * 0.6); c.stroke(); }
      }
      drawCracks(c, b, "rgba(240,248,255,0.85)", 1.6);
      if (dmg >= 3) {                                            // éclat de verre manquant, bordé de blanc
        c.beginPath(); c.moveTo(-84, 22); c.lineTo(-70, 17); c.lineTo(-62, 27); c.lineTo(-68, 40); c.lineTo(-80, 38); c.closePath();
        c.fillStyle = "rgba(5,8,20,0.9)"; c.fill(); c.strokeStyle = "rgba(240,248,255,0.9)"; c.lineWidth = 1.6; c.stroke();
      }
      if (dmg >= 2) { tape(c, -67, -40, 0.5, 30, 11); tape(c, -67, -40, -0.6, 30, 11); }
      if (dmg >= 3) { tape(c, 57, 37, -0.35, 34, 12); tape(c, -16, -50, 0.1, 26, 10); }
      if (dmg >= 1 && fill > 0.01) {                             // gouttes qui fuient sous le réservoir
        c.fillStyle = col(S.liqHi, 0.95);
        const leaks = dmg >= 3 ? [[-72, 0, 2.1], [56, 0.4, 1.5], [-28, 0.7, 1.2]] : dmg >= 2 ? [[-66, 0, 1.3], [56, 0.5, 1.1]] : [[-64, 0, 1]];
        for (const [x0, ph, sp] of leaks) {
          const u = (t * 0.75 * sp + ph) % 1, y0 = GH + 1;
          if (u < 0.35) { const r = 2 + 3 * (u / 0.35); c.beginPath(); c.arc(x0, y0 + r * 0.6, r, 0, TAU); c.fill(); }
          else { const f = (u - 0.35) / 0.65, y = y0 + 4 + f * f * 86; c.globalAlpha = alpha * (1 - f * f); c.beginPath(); c.moveTo(x0, y - 8); c.quadraticCurveTo(x0 + 5, y + 1, x0, y + 5); c.quadraticCurveTo(x0 - 5, y + 1, x0, y - 8); c.fill(); c.globalAlpha = alpha; }
        }
        if (dmg >= 3 && lvl < 36) { c.strokeStyle = col(S.liqHi, 0.9); c.lineWidth = 3.5; c.lineCap = "round"; c.beginPath(); c.moveTo(-76, 32); c.quadraticCurveTo(-104, 34 + Math.sin(t * 9) * 2, -110, 78); c.stroke(); }
      }

      // visage
      drawFace(faceA, false);

      drawFlange(c, S, rt, dmg);

      // glyphes (moitié avant)
      drawGlyphs(c, G, true);

      // détente : le liquide gicle de la pointe
      if (A.on && A.strike > 0 && A.rec < 0.7) {
        const u = clamp(A.strike * 0.5 + A.rec * 0.9, 0, 1);
        c.strokeStyle = col(S.liqHi, 1 - u); c.lineWidth = 3; c.lineCap = "round";
        for (let i = -2; i <= 2; i++) { const a = Math.PI + i * 0.3; c.beginPath(); c.moveTo(TIP + Math.cos(a) * (6 + 16 * u), 2 + Math.sin(a) * (6 + 16 * u)); c.lineTo(TIP + Math.cos(a) * (14 + 34 * u), 2 + Math.sin(a) * (14 + 34 * u)); c.stroke(); }
        c.fillStyle = col(C.white, 0.8 * (1 - u)); c.beginPath(); c.arc(TIP - 4, 2, 9 * (1 - u) + 3, 0, TAU); c.fill();
      }
      // action spéciale : un paquet d'instructions glisse le long de l'aiguille et tombe vers le joueur
      if (castT >= 0) {
        const u = seg(castT, 0.12, 0.6), f = seg(castT, 0.6, 0.9);
        glyphChip(c, "</>", lerp(-96, TIP - 6, easeInOut(u)) - 14 * f, -1 + 44 * f * f, 0.9 - 0.2 * f, C.glitch, (1 - f) * seg(castT, 0.05, 0.2));
        c.fillStyle = col(C.glitch, 0.8 * (1 - f)); for (let i = 0; i < 4; i++) c.fillRect(lerp(-96, TIP, easeInOut(u)) + 16 + i * 9, -3 + Math.sin(i * 2.1 + t * 20) * 5, 4, 4);
      }
      // étourdi (mis en quarantaine) : croix qui tournent au-dessus de lui
      if (stun) {
        c.strokeStyle = col(C.glitch, 0.95); c.lineWidth = 3; c.lineCap = "round";
        for (let k = 0; k < 3; k++) { const a = time * 4 + k * 2.1, x = Math.cos(a) * 46, y = -76 + Math.sin(a) * 9; c.beginPath(); c.moveTo(x - 5, y - 5); c.lineTo(x + 5, y + 5); c.moveTo(x + 5, y - 5); c.lineTo(x - 5, y + 5); c.stroke(); }
      }
      // ricanement : petits éclats au-dessus du réservoir
      if (gloat > 0.1) {
        c.strokeStyle = col(S.liqHi, gloat); c.lineWidth = 3; c.lineCap = "round";
        for (let k = -1; k <= 1; k++) { const a = -Math.PI / 2 + k * 0.5, r0 = 70 + Math.abs(Math.sin(t * 12)) * 6; c.beginPath(); c.moveTo(Math.cos(a) * r0 - 10, Math.sin(a) * r0 + 4); c.lineTo(Math.cos(a) * (r0 + 13) - 10, Math.sin(a) * (r0 + 13) + 4); c.stroke(); }
      }
    }
  };
}
