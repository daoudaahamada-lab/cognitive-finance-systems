/* Étage 10 — L'Examinateur : buste de pierre et d'or, gardien du seuil de 720, en trois phases (or, violet, rose). */
{
  const TAU = Math.PI * 2;
  const INK = "#3b342b";
  const frac = (v) => v - Math.floor(v);
  const hsh = (n) => frac(Math.sin(n * 127.1 + 31.7) * 43758.5453);
  const PH = ["#f3b841", "#b38cff", "#ff4f9a"];
  /* Runes des domaines : phase à partir de laquelle chacune entre en orbite (D1, D3, D6, puis D4, D7, puis D2, D5). */
  const RUNE_AT = [0, 2, 0, 1, 2, 0, 1];
  /* Fissures de lumière : phase d'apparition et tracé. */
  const LIGHT = [
    { at: 1, p: [[42, -88], [32, -72], [40, -60], [31, -48]] },
    { at: 1, p: [[-98, 66], [-86, 86], [-95, 104], [-82, 124]] },
    { at: 1, p: [[8, 38], [0, 56], [10, 72], [2, 92]] },
    { at: 2, p: [[48, -18], [36, -6], [43, 8], [32, 22]] },
    { at: 2, p: [[-54, -86], [-46, -72], [-53, -62]] },
    { at: 2, p: [[98, 70], [86, 90], [95, 108], [84, 128]] },
    { at: 2, p: [[-40, 34], [-32, 52], [-41, 66], [-30, 84]] },
    { at: 3, p: [[-20, -62], [-30, -40], [-18, -20], [-34, 4]] },
    { at: 3, p: [[-20, -62], [6, -66], [26, -84], [52, -78]] },
    { at: 3, p: [[-20, -62], [-48, -66], [-60, -40]] },
    { at: 3, p: [[60, 44], [40, 66], [52, 90], [36, 118], [44, 140]] },
    { at: 3, p: [[-70, 44], [-58, 70], [-72, 96], [-60, 130]] }
  ];
  /* Ligne de rupture du buste à sa mort. */
  const SPLIT = [[-34, -200], [6, -128], [-18, -88], [12, -50], [-14, -10], [16, 34], [-10, 78], [10, 120], [-6, 200]];
  const poly = (c, p) => { c.beginPath(); c.moveTo(p[0][0], p[0][1]); for (let i = 1; i < p.length; i++) c.lineTo(p[i][0], p[i][1]); };
  const rock = (c, x, y, s, a, light, dark) => {
    c.save(); c.translate(x, y); c.rotate(a);
    c.fillStyle = dark; c.beginPath(); c.moveTo(-s, 0.1 * s); c.lineTo(-0.3 * s, -0.8 * s); c.lineTo(0.8 * s, -0.5 * s); c.lineTo(s, 0.3 * s); c.lineTo(0.2 * s, 0.8 * s); c.closePath(); c.fill();
    c.fillStyle = light; c.beginPath(); c.moveTo(-s, 0.1 * s); c.lineTo(-0.3 * s, -0.8 * s); c.lineTo(0.8 * s, -0.5 * s); c.lineTo(0.1 * s, -0.05 * s); c.closePath(); c.fill();
    c.restore();
  };
  /* Flammèche (regard de braise de la phase 3). */
  const wisp = (c, x, y, h, lean, T, seed, color) => {
    const w = Math.sin(T * 9 + seed * 4) * 3, hh = h * (0.85 + 0.25 * Math.sin(T * 13 + seed * 7));
    c.fillStyle = color; c.beginPath(); c.moveTo(x - 5, y); c.quadraticCurveTo(x - 6 + lean * 0.4, y - hh * 0.5, x + lean + w, y - hh); c.quadraticCurveTo(x + 5 + lean * 0.5, y - hh * 0.4, x + 5, y); c.closePath(); c.fill();
  };
  /* Œil : orbite sombre, iris de lumière qui suit la cible, paupière de pierre. */
  const eye = (c, S, cx, cy, hw, hh, ir) => {
    const lk = S.look;
    c.fillStyle = "#15100b"; c.beginPath(); c.moveTo(cx - hw, cy); c.quadraticCurveTo(cx, cy - hh * 2, cx + hw, cy); c.quadraticCurveTo(cx, cy + hh * 2, cx - hw, cy); c.fill();
    if (S.eyeOn > 0.02) {
      const ix = cx + lk.x * hw * 0.34, iy = cy + lk.y * hh * 0.3;
      if (S.p2 > 0.05) { c.fillStyle = col(S.aura, 0.5 * S.p2 * S.eyeOn); c.beginPath(); c.moveTo(cx - hw, cy); c.quadraticCurveTo(cx, cy - hh * 2, cx + hw, cy); c.quadraticCurveTo(cx, cy + hh * 2, cx - hw, cy); c.fill(); }
      c.save(); c.shadowColor = col(S.aura); c.shadowBlur = 12;
      c.fillStyle = col(S.eyeC, S.eyeOn); c.beginPath(); c.ellipse(ix, iy, ir, Math.min(ir, hh * 0.95), 0, 0, TAU); c.fill();
      c.restore();
      c.fillStyle = col("#ffffff", S.eyeOn); c.beginPath(); c.arc(ix - 1, iy - 0.6, ir * 0.48, 0, TAU); c.fill();
    }
    if (S.lid > 0.02) { c.fillStyle = S.cShade; c.beginPath(); c.moveTo(cx - hw - 1, cy + 0.5); c.quadraticCurveTo(cx, cy - hh * 2 - 2, cx + hw + 1, cy + 0.5); c.quadraticCurveTo(cx, cy - hh * 2 + S.lid * hh * 4.3, cx - hw - 1, cy + 0.5); c.fill(); }
  };

  /* Le buste : toge, épaulettes, tête, barbe, visage, gemme, monocle, éclats. Dessiné deux fois (moitiés) quand il se brise. */
  const bust = (c, S) => {
    const { K, t, T, aura, p1, p2, dmg } = S;
    c.lineJoin = "round"; c.lineCap = "round";
    // toge : épaules larges, base brisée
    const rg = c.createLinearGradient(0, 40, 0, 156);
    rg.addColorStop(0, K(S.robeHi)); rg.addColorStop(0.5, K(S.robe)); rg.addColorStop(1, K(S.robeLo));
    c.fillStyle = rg; c.beginPath(); c.moveTo(-44, 36); c.bezierCurveTo(-82, 38, -124, 50, -131, 84); c.lineTo(-135, 118);
    c.lineTo(-116, 142); c.lineTo(-96, 130); c.lineTo(-72, 150); c.lineTo(-44, 138); c.lineTo(-10, 156); c.lineTo(24, 140); c.lineTo(54, 152); c.lineTo(86, 134); c.lineTo(112, 144); c.lineTo(137, 116);
    c.lineTo(133, 84); c.bezierCurveTo(125, 50, 84, 38, 46, 36); c.closePath(); c.fill();
    c.strokeStyle = S.cInk; c.lineWidth = 2; c.stroke();
    c.strokeStyle = "rgba(8,6,22,0.4)"; c.lineWidth = 2; c.beginPath();
    c.moveTo(-106, 72); c.quadraticCurveTo(-98, 102, -106, 134); c.moveTo(-88, 64); c.quadraticCurveTo(-84, 98, -90, 132); c.moveTo(104, 72); c.quadraticCurveTo(96, 102, 104, 136); c.moveTo(84, 64); c.quadraticCurveTo(80, 100, 82, 134); c.stroke();
    // étole d'or
    const sg = c.createLinearGradient(0, 44, 0, 134);
    sg.addColorStop(0, K("#ffe7a0")); sg.addColorStop(0.5, K("#eebd52")); sg.addColorStop(1, K("#a9781f"));
    c.fillStyle = sg; c.strokeStyle = K("#7a5412", 0.3); c.lineWidth = 1.4;
    poly(c, [[-80, 47], [-56, 43], [-50, 122], [-63, 135], [-76, 122]]); c.closePath(); c.fill(); c.stroke();
    poly(c, [[34, 43], [63, 47], [65, 122], [50, 135], [36, 122]]); c.closePath(); c.fill(); c.stroke();
    c.fillStyle = K(S.robe);
    for (let k = 0; k < 3; k++) { const y = 66 + k * 22; poly(c, [[-65, y - 6], [-60, y], [-65, y + 6], [-70, y]]); c.fill(); poly(c, [[49.5, y - 7], [55.5, y], [49.5, y + 7], [43.5, y]]); c.fill(); }
    // épaulettes à franges
    c.fillStyle = sg; c.strokeStyle = K("#7a5412", 0.3); c.lineWidth = 1.6;
    c.beginPath(); c.moveTo(-137, 90); c.quadraticCurveTo(-136, 52, -92, 42); c.lineTo(-84, 57); c.quadraticCurveTo(-116, 64, -122, 96); c.closePath(); c.fill(); c.stroke();
    c.beginPath(); c.moveTo(139, 90); c.quadraticCurveTo(136, 52, 94, 42); c.lineTo(86, 57); c.quadraticCurveTo(118, 64, 124, 96); c.closePath(); c.fill(); c.stroke();
    c.strokeStyle = K("#eebd52"); c.lineWidth = 2.6; c.beginPath();
    for (let k = 0; k < 4; k++) { c.moveTo(-135 + k * 4, 92 + k * 1.5); c.lineTo(-136 + k * 4 + Math.sin(t * 2 + k) * 1.5, 104 + k * 1.5); c.moveTo(137 - k * 4, 92 + k * 1.5); c.lineTo(138 - k * 4 + Math.sin(t * 2 + k + 2) * 1.5, 104 + k * 1.5); }
    c.stroke();

    // tête de pierre, vue de trois quarts vers la gauche
    const hg = c.createLinearGradient(-64, -90, 60, 30);
    hg.addColorStop(0, K("#efe8d8")); hg.addColorStop(0.5, K(S.stone)); hg.addColorStop(1, K("#a39a88"));
    c.fillStyle = hg; c.beginPath(); c.moveTo(-58, -98); c.quadraticCurveTo(-66, -72, -62, -55); c.lineTo(-67, -47); c.quadraticCurveTo(-60, -34, -63, -22); c.quadraticCurveTo(-64, -2, -54, 10);
    c.lineTo(-40, 30); c.lineTo(34, 34); c.quadraticCurveTo(57, 14, 59, -10); c.quadraticCurveTo(67, -42, 62, -98); c.closePath(); c.fill();
    c.strokeStyle = S.cInk; c.lineWidth = 2; c.stroke();
    // pan de côté dans l'ombre, oreille
    c.fillStyle = K("#8f8674", 0.5); c.globalAlpha *= 0.55; c.beginPath(); c.moveTo(34, -98); c.lineTo(62, -98); c.quadraticCurveTo(67, -42, 59, -10); c.quadraticCurveTo(56, 14, 36, 32); c.quadraticCurveTo(22, 4, 34, -30); c.quadraticCurveTo(40, -64, 34, -98); c.closePath(); c.fill(); c.globalAlpha /= 0.55;
    c.fillStyle = K("#cfc6b3"); c.beginPath(); c.ellipse(50, -30, 8, 14, 0.1, 0, TAU); c.fill(); c.strokeStyle = S.cInk; c.lineWidth = 1.5; c.stroke();
    c.strokeStyle = K("#6f6759", 0.4); c.lineWidth = 2; c.beginPath(); c.arc(51, -30, 5, 1.9, 4.6); c.stroke();
    // ombre de la toque sur le front
    c.fillStyle = "rgba(40,32,24,0.28)"; c.beginPath(); c.moveTo(-61, -98); c.lineTo(63, -98); c.lineTo(63, -86); c.quadraticCurveTo(0, -76, -62, -86); c.closePath(); c.fill();

    // barbe sculptée (elle descend quand il parle)
    const jaw = S.mouth * 3.5;
    const bg = c.createLinearGradient(0, 0, 0, 122);
    bg.addColorStop(0, K("#e6dfcf")); bg.addColorStop(0.6, K("#c3bba9")); bg.addColorStop(1, K("#9d9482"));
    c.fillStyle = bg; c.beginPath(); c.moveTo(-61, -10); c.quadraticCurveTo(-68, 30, -47, 62 + jaw); c.quadraticCurveTo(-37, 96 + jaw, -20, 123 + jaw); c.quadraticCurveTo(-2, 100 + jaw, 22, 72 + jaw); c.quadraticCurveTo(49, 44, 53, -6);
    c.lineTo(57, -26); c.lineTo(44, -24); c.quadraticCurveTo(40, 4, 14, 13); c.quadraticCurveTo(-10, 21, -22, 19); c.quadraticCurveTo(-40, 19, -53, 4); c.closePath(); c.fill();
    c.strokeStyle = S.cInk; c.lineWidth = 2; c.stroke();
    c.strokeStyle = K("#6f6759", 0.4); c.lineWidth = 1.5; c.beginPath();
    for (let k = -3; k <= 3; k++) { const x0 = -20 + k * 11.5; c.moveTo(x0, 26 + Math.abs(k) * 1.5); c.bezierCurveTo(x0 + k * 3 + 4, 50, x0 * 0.7 - 10 - k * 2, 76 + jaw, -20 + k * 4.5, 112 - Math.abs(k) * 13 + jaw); }
    c.stroke();
    c.lineWidth = 1.3; c.strokeStyle = K("#6f6759", 0.4); c.beginPath();
    for (let k = 0; k < 5; k++) { const x = -52 + k * 20; c.moveTo(x, 40 + jaw * 0.5); c.quadraticCurveTo(x + 9, 50 + jaw * 0.5, x + 18, 40 + jaw * 0.5); }
    for (let k = 0; k < 3; k++) { const x = -44 + k * 18; c.moveTo(x, 72 + jaw); c.quadraticCurveTo(x + 8, 81 + jaw, x + 16, 72 + jaw); }
    c.stroke();

    // bouche et moustache
    c.fillStyle = "#1c1611"; c.beginPath(); c.ellipse(-22, 11 + jaw * 0.4, 13, 1.8 + S.mouth * 6.5, 0, 0, TAU); c.fill();
    if (S.mouth > 0.08) { c.fillStyle = col(aura, 0.75 * S.mouth); c.beginPath(); c.ellipse(-22, 12 + jaw * 0.4, 8, 0.8 + S.mouth * 4, 0, 0, TAU); c.fill(); }
    const curl = S.gloat * 7;
    c.fillStyle = K("#ddd5c4"); c.strokeStyle = S.cInk; c.lineWidth = 1.5;
    c.beginPath(); c.moveTo(-26, -1); c.quadraticCurveTo(-46, -5, -61, 12 - curl); c.quadraticCurveTo(-46, 13, -28, 8); c.closePath(); c.fill(); c.stroke();
    c.beginPath(); c.moveTo(-22, -1); c.quadraticCurveTo(6, -7, 35, 14 - curl * 1.3); c.quadraticCurveTo(10, 15, -20, 8); c.closePath(); c.fill(); c.stroke();
    // nez : pan éclairé, pan dans l'ombre
    c.fillStyle = K("#ebe4d4"); poly(c, [[-23, -53], [-35, -17], [-41, -8], [-33, -2], [-24, -4], [-20, -30]]); c.closePath(); c.fill();
    c.fillStyle = K("#a39a88"); poly(c, [[-23, -53], [-20, -30], [-24, -4], [-12, -4], [-10, -16], [-14, -52]]); c.closePath(); c.fill();
    c.strokeStyle = S.cInk; c.lineWidth = 1.6; c.beginPath(); c.moveTo(-23, -53); c.lineTo(-35, -17); c.quadraticCurveTo(-43, -7, -33, -2); c.lineTo(-12, -4); c.quadraticCurveTo(-9, -12, -12, -22); c.stroke();
    c.fillStyle = "#3a322a"; c.beginPath(); c.ellipse(-19, -6, 3, 1.5, -0.2, 0, TAU); c.fill();
    c.strokeStyle = K("#6f6759", 0.4); c.lineWidth = 1.5; c.beginPath(); c.moveTo(-40, -4); c.quadraticCurveTo(-48, 2, -50, 8); c.moveTo(-6, -4); c.quadraticCurveTo(6, 2, 10, 9); c.stroke();

    // yeux, flammes du regard, arcades
    eye(c, S, -44, -40, 14, 5.2, 4.6);
    eye(c, S, 10, -41, 19, 6.4, 5.8);
    if (p2 > 0.05 && S.eyeOn > 0.3) {
      const fc = col(mixv(aura, "#ffffff", 0.25), 0.85 * p2);
      wisp(c, -54, -44, 26 * p2, -7, T, 1, fc); wisp(c, 26, -46, 32 * p2, 9, T, 2, fc);
    }
    const bd = S.browDrop, br = S.browRaise;
    c.fillStyle = K("#e6dfcf"); c.strokeStyle = S.cInk; c.lineWidth = 1.6;
    poly(c, [[-66, -57 - br * 0.5], [-42, -62 - br], [-23, -50 + bd - br * 0.4], [-25, -44 + bd - br * 0.4], [-44, -53 - br], [-65, -49 - br * 0.5]]); c.closePath(); c.fill(); c.stroke();
    poly(c, [[-13, -50 + bd], [10, -63], [42, -59], [44, -52], [10, -54], [-11, -43 + bd]]); c.closePath(); c.fill(); c.stroke();
    if (bd > 2) { c.strokeStyle = K("#6f6759", 0.4); c.lineWidth = 1.5; c.beginPath(); c.moveTo(-21, -60); c.lineTo(-19, -53); c.moveTo(-16, -61); c.lineTo(-15, -54); c.stroke(); }

    // éclats : la pierre saute et laisse voir la lumière d'or
    if (dmg >= 1 || S.d > 0) {
      const gl = c.createRadialGradient(0, 0, 10, 0, 0, 150);
      gl.addColorStop(0, "#fffbe0"); gl.addColorStop(0.5, "#ffd86a"); gl.addColorStop(1, "#e89a2a");
      c.fillStyle = gl; c.strokeStyle = S.cInk; c.lineWidth = 1.6;
      poly(c, [[36, -8], [50, -14], [58, 0], [50, 16], [38, 12], [32, 2]]); c.closePath(); c.fill(); c.stroke();
      poly(c, [[100, 46], [116, 50], [122, 64], [108, 66]]); c.closePath(); c.fill(); c.stroke();
      if (dmg >= 2) {
        poly(c, [[-58, 26], [-44, 24], [-38, 40], [-48, 52], [-58, 44]]); c.closePath(); c.fill(); c.stroke();
        poly(c, [[-124, 78], [-108, 72], [-100, 88], [-112, 102], [-126, 96]]); c.closePath(); c.fill(); c.stroke();
        poly(c, [[26, 96], [40, 88], [46, 104], [34, 114]]); c.closePath(); c.fill(); c.stroke();
      }
      if (dmg >= 3) {
        poly(c, [[30, -92], [48, -94], [60, -78], [52, -62], [38, -66], [28, -78]]); c.closePath(); c.fill(); c.stroke();
        poly(c, [[-64, -20], [-52, -18], [-50, -4], [-60, 2]]); c.closePath(); c.fill(); c.stroke();
        poly(c, [[76, 112], [96, 104], [104, 122], [88, 132]]); c.closePath(); c.fill(); c.stroke();
      }
    }
    // fissures de lumière des phases 2 et 3, puis de la mort
    const lv = S.d > 0 ? 3 : S.phS;
    if (lv > 0.05) {
      c.save(); c.shadowColor = col(S.d > 0 ? "#ffd86a" : aura); c.shadowBlur = 9;
      c.strokeStyle = col(mixv(S.d > 0 ? "#ffd86a" : aura, "#ffffff", 0.45), 0.9); c.lineWidth = 2 + (S.d > 0 ? S.d * 3 : 0); c.beginPath();
      for (const k of LIGHT) {
        const a = k.at === 3 ? S.crk : clamp(lv - k.at + 1, 0, 1); if (a <= 0.02) continue;
        const n = (k.p.length - 1) * a; c.moveTo(k.p[0][0], k.p[0][1]);
        for (let i = 1; i < k.p.length; i++) { const u = clamp(n - (i - 1), 0, 1); if (u <= 0) break; c.lineTo(lerp(k.p[i - 1][0], k.p[i][0], u), lerp(k.p[i - 1][1], k.p[i][1], u)); }
      }
      c.stroke(); c.restore();
    }
    drawCracks(c, S.b, "rgba(64,54,42,0.8)", 1.8);

    // troisième œil : la gemme du juge (cible critique), absente du mirage
    const gx = -20, gy = -74, gp = 1 + Math.sin(T * 4) * 0.07 + S.beat * 0.1;
    c.fillStyle = K("#f0c25a"); c.strokeStyle = K("#8a5f16", 0.3); c.lineWidth = 1.6; poly(c, [[gx, gy - 17], [gx + 13, gy], [gx, gy + 17], [gx - 13, gy]]); c.closePath(); c.fill(); c.stroke();
    if (S.mirage || S.gemOff > 0.5) { c.fillStyle = "#1b1510"; poly(c, [[gx, gy - 11], [gx + 8, gy], [gx, gy + 11], [gx - 8, gy]]); c.closePath(); c.fill(); }
    else {
      c.save(); c.shadowColor = col(aura); c.shadowBlur = 16;
      const gg = c.createRadialGradient(gx - 2, gy - 4, 1, gx, gy, 12 * gp);
      gg.addColorStop(0, "#ffffff"); gg.addColorStop(0.45, col(mixv(aura, "#ffffff", S.fl * 0.6))); gg.addColorStop(1, col(mixv(aura, "#000000", 0.45)));
      c.fillStyle = gg; poly(c, [[gx, gy - 12 * gp], [gx + 9 * gp, gy], [gx, gy + 12 * gp], [gx - 9 * gp, gy]]); c.closePath(); c.fill();
      c.restore();
      c.strokeStyle = "rgba(255,255,255,0.55)"; c.lineWidth = 1; c.beginPath(); c.moveTo(gx - 9 * gp, gy); c.lineTo(gx, gy - 3); c.lineTo(gx + 9 * gp, gy); c.moveTo(gx, gy - 12 * gp); c.lineTo(gx, gy - 3); c.stroke();
    }

    // monocle et sa chaîne (verre fêlé, puis brisé)
    const mxo = 10, myo = -41, sw = Math.sin(t * 1.5) * 3 + S.fl * 5;
    c.strokeStyle = K("#a9781f", 0.3); c.lineWidth = 1.5; c.setLineDash([3, 2.5]); c.beginPath(); c.moveTo(mxo + 15, myo + 12); c.quadraticCurveTo(46 + sw, 16, 60, 40); c.stroke(); c.setLineDash([]);
    if (dmg < 3) { c.fillStyle = "rgba(214,232,255,0.16)"; c.beginPath(); c.arc(mxo, myo, 19, 0, TAU); c.fill(); c.strokeStyle = "rgba(255,255,255,0.6)"; c.lineWidth = 2; c.beginPath(); c.arc(mxo, myo, 14, 3.5, 4.4); c.stroke(); }
    else { c.fillStyle = "rgba(214,232,255,0.2)"; poly(c, [[mxo - 18, myo + 2], [mxo - 4, myo - 4], [mxo + 2, myo + 8], [mxo - 6, myo + 18], [mxo - 15, myo + 11]]); c.closePath(); c.fill(); }
    if (dmg >= 2) { c.strokeStyle = "rgba(255,255,255,0.85)"; c.lineWidth = 1.2; c.beginPath(); c.moveTo(mxo + 4, myo - 4); c.lineTo(mxo + 16, myo - 9); c.moveTo(mxo + 4, myo - 4); c.lineTo(mxo + 9, myo + 15); c.moveTo(mxo + 4, myo - 4); c.lineTo(mxo - 10, myo - 15); c.moveTo(mxo + 4, myo - 4); c.lineTo(mxo - 12, myo + 6); c.stroke(); }
    c.strokeStyle = K("#7a5412", 0.3); c.lineWidth = 5; c.beginPath(); c.arc(mxo, myo, 19, 0, TAU); c.stroke();
    c.strokeStyle = K("#f5cf6c"); c.lineWidth = 2.8; c.stroke();
  };

  /* Toque universitaire : calotte, plateau, cordon et gland doré. */
  const cap = (c, S, swing) => {
    const K = S.K;
    c.lineJoin = "round"; c.lineCap = "round";
    c.fillStyle = K("#141729"); c.beginPath(); c.moveTo(-64, -90); c.quadraticCurveTo(-67, -114, -30, -120); c.lineTo(30, -122); c.quadraticCurveTo(67, -116, 66, -92); c.quadraticCurveTo(8, -79, -64, -90); c.closePath(); c.fill();
    c.strokeStyle = K("#eebd52"); c.lineWidth = 3; c.beginPath(); c.moveTo(-64, -90); c.quadraticCurveTo(8, -79, 66, -92); c.stroke();
    c.fillStyle = K("#0c0e1e"); poly(c, [[-120, -122], [-16, -102], [116, -130], [116, -123], [-16, -94], [-120, -115]]); c.closePath(); c.fill();
    c.fillStyle = K("#262b4c"); poly(c, [[-120, -122], [-16, -102], [116, -130], [12, -150]]); c.closePath(); c.fill();
    c.fillStyle = K("#343a63"); poly(c, [[-120, -122], [-16, -102], [12, -150]]); c.closePath(); c.fill();
    c.strokeStyle = col(mixv("#4a5285", S.aura, 0.45)); c.lineWidth = 1.6; poly(c, [[-120, -122], [-16, -102], [116, -130], [12, -150]]); c.closePath(); c.stroke();
    // cordon et gland
    const tx = 76 + swing, ty = -78;
    c.strokeStyle = K("#7a5412", 0.3); c.lineWidth = 4; c.beginPath(); c.moveTo(-2, -127); c.lineTo(74, -121); c.quadraticCurveTo(76 + swing * 0.3, -100, tx, ty); c.stroke();
    c.strokeStyle = K("#f5cf6c"); c.lineWidth = 2.2; c.stroke();
    c.fillStyle = K("#f5cf6c"); c.beginPath(); c.arc(-2, -127, 5, 0, TAU); c.fill(); c.strokeStyle = K("#7a5412", 0.3); c.lineWidth = 1.4; c.stroke();
    c.fillStyle = K("#eebd52"); poly(c, [[tx - 4, ty], [tx + 4, ty], [tx + 8 + swing * 0.35, ty + 26], [tx - 8 + swing * 0.35, ty + 26]]); c.closePath(); c.fill(); c.stroke();
    c.beginPath(); c.moveTo(tx - 2 + swing * 0.1, ty + 8); c.lineTo(tx - 3.5 + swing * 0.3, ty + 25); c.moveTo(tx + 2 + swing * 0.1, ty + 8); c.lineTo(tx + 3.5 + swing * 0.3, ty + 25); c.stroke();
    c.fillStyle = K("#f5cf6c"); c.beginPath(); c.arc(tx, ty, 4.5, 0, TAU); c.fill(); c.stroke();
  };

  /* Main de pierre détachée qui tient le stylo rouge (pointe vers le haut du repère local). */
  const hand = (c, S, glow) => {
    const K = S.K;
    c.lineJoin = "round"; c.lineCap = "round";
    // stylo : capuchon, corps, bague dorée, plume
    c.fillStyle = K("#8e1b22"); rr(c, -6, 20, 12, 14, 4); c.fill();
    c.fillStyle = K("#e5383b"); c.fillRect(-5.5, -40, 11, 62);
    c.fillStyle = "rgba(255,255,255,0.35)"; c.fillRect(-3.5, -40, 2.4, 60);
    c.fillStyle = K("#f5cf6c"); c.fillRect(-6, -43, 12, 5);
    c.fillStyle = K("#f4ead2"); poly(c, [[-5.5, -43], [5.5, -43], [0, -63]]); c.closePath(); c.fill();
    c.strokeStyle = "#3a1114"; c.lineWidth = 1.4; c.beginPath(); c.moveTo(-5.5, 22); c.lineTo(-5.5, -43); c.lineTo(0, -63); c.lineTo(5.5, -43); c.lineTo(5.5, 22); c.stroke();
    c.fillStyle = "#c21f2b"; poly(c, [[-2, -55.5], [2, -55.5], [0, -63]]); c.closePath(); c.fill();
    if (glow > 0.02) { c.fillStyle = col("#ff5a5f", 0.55 * glow); c.beginPath(); c.arc(0, -62, 6 + glow * 6, 0, TAU); c.fill(); }
    // poing : manchette d'or, doigts, pouce
    c.fillStyle = K("#eebd52"); rr(c, 13, -11, 13, 23, 3); c.fill(); c.strokeStyle = K("#7a5412", 0.3); c.lineWidth = 1.4; c.stroke();
    c.fillStyle = K("#8f8674"); poly(c, [[26, -9], [34, -4], [30, 1], [36, 7], [26, 10]]); c.closePath(); c.fill();
    c.fillStyle = K("#d8d0be"); rr(c, -16, -15, 31, 31, 9); c.fill(); c.strokeStyle = S.cInk; c.lineWidth = 1.8; c.stroke();
    c.strokeStyle = K("#6f6759", 0.4); c.lineWidth = 1.5; c.beginPath(); c.moveTo(-15, -6); c.lineTo(4, -6); c.moveTo(-16, 1); c.lineTo(4, 1); c.moveTo(-15, 8); c.lineTo(4, 8); c.stroke();
    c.fillStyle = K("#ebe4d4"); c.beginPath(); c.ellipse(5, 1, 6, 11, 0.25, 0, TAU); c.fill(); c.strokeStyle = S.cInk; c.lineWidth = 1.5; c.stroke();
  };

  /* Parchemin « 720 » : rouleaux, lignes, sceau ; tampon vert à la fin. */
  const scroll = (c, S, unroll, stamp) => {
    const K = S.K, w = 52, h = 14 + unroll * 62;
    c.fillStyle = K("#f3e7c8"); c.fillRect(-w / 2, -h / 2, w, h);
    c.fillStyle = "rgba(150,110,50,0.22)"; c.fillRect(-w / 2, -h / 2, 5, h); c.fillRect(w / 2 - 5, -h / 2, 5, h);
    c.strokeStyle = "rgba(90,66,34,0.55)"; c.lineWidth = 1.2; c.beginPath();
    for (let y = -h / 2 + 9; y < h / 2 - 6; y += 6) { if (Math.abs(y) < 11 && h > 44) continue; c.moveTo(-18, y); c.lineTo(18 - ((y * 7 + 70) % 11), y); }
    c.stroke();
    if (h > 44) { c.fillStyle = "#5a2a1a"; c.font = "800 19px " + F_DISPLAY; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText("720", stamp > 0 ? -8 : 0, 1); }
    if (h > 34 && stamp <= 0) { c.fillStyle = "#c21f2b"; c.beginPath(); c.arc(w / 2 - 10, h / 2 - 9, 5.5, 0, TAU); c.fill(); c.fillStyle = "#8e1b22"; c.beginPath(); c.arc(w / 2 - 10, h / 2 - 9, 2.5, 0, TAU); c.fill(); }
    if (stamp > 0) {
      const k = backOut(stamp), s = 2.2 - 1.2 * k;
      c.save(); c.translate(15, 1); c.scale(s, s); c.globalAlpha *= Math.min(1, stamp * 3);
      c.strokeStyle = "#1f9d62"; c.lineWidth = 2.6; c.beginPath(); c.arc(0, 0, 9.5, 0, TAU); c.stroke();
      c.lineWidth = 3.2; c.lineCap = "round"; c.lineJoin = "round"; c.beginPath(); c.moveTo(-5, 0); c.lineTo(-1.5, 4.5); c.lineTo(5.5, -4.5); c.stroke();
      c.restore();
    }
    for (const y of [-h / 2 - 7, h / 2 - 3]) {
      c.fillStyle = K("#c9a45c"); rr(c, -w / 2 - 5, y, w + 10, 10, 5); c.fill(); c.strokeStyle = K("#7a5412", 0.3); c.lineWidth = 1.3; c.stroke();
      c.fillStyle = "rgba(255,255,255,0.3)"; c.fillRect(-w / 2 - 1, y + 2, w + 2, 2);
      c.fillStyle = K("#8a5f16"); c.beginPath(); c.arc(-w / 2 - 5, y + 5, 3.4, 0, TAU); c.arc(w / 2 + 5, y + 5, 3.4, 0, TAU); c.fill();
    }
  };

  BOSSES[10] = {
    v: 2,
    palette: { main: "#f3b841", dark: "#6f6759", accent: "#fff3c4", eye: "#f3b841", rage: "#ff4f9a" },
    sky: ["#131233", "#472d68", "#ee9a62"],
    hit: { rx: 122, ry: 154, coreR: 19 },
    top: 180,
    attackFrom: { x: -198, y: -54 },
    castLean: -0.08,
    weakSpot: () => ({ x: -20, y: -74 }),
    critLabel: "ŒIL DU JUGE",
    epitaph: "ADMIS",
    lines: {
      hit: ["Correct. Continue.", "Raisonnement acceptable.", "Hmm. Pas mal.", "Je note… à contrecœur."],
      crit: ["Mon troisième œil !", "Précision d’architecte…", "Mention très bien. Hélas."],
      wrong: ["Une bonne idée. Pas la meilleure.", "Relis l’énoncé.", "Ce n’est pas ce que dit la doc."],
      timeout: ["Le temps de l’examen est compté.", "Une minute cinquante-quatre, pas plus."],
      gloat: ["Zéro point. Question suivante.", "Faux. Et c’était écrit dans l’énoncé.", "Je retire un point. Avec plaisir.", "719. Presque. Presque."],
      rage: "Assez de bonnes réponses ! Voyons si tu tiens la distance.",
      special: {
        fog: ["Un énoncé flou ? Lis chaque mot.", "Le brouillard se lève… pour l’instant."],
        mirage: ["Deux examinateurs. Un seul note vraiment.", "Lequel de nous deux a un troisième œil ?"],
        build: ["Encore un agent de plus ?", "Je bâtis une architecture… inutilement complexe."],
        collapse: ["Simple et juste. Mes tours tombent.", "La solution la plus simple gagne."],
        shieldUp: ["Mon bouclier de promesses revient !", "Une erreur, et je redeviens invulnérable."],
        shieldBreak: ["Trois preuves d’affilée… le bouclier cède.", "Tu mesures avant de promettre. Bien."],
        cache: ["Cache hit… tu réponds vite et juste.", "Préfixe en cache, coup doublé !"],
        inject: ["Une consigne cachée dans ta main…", "Ce document dit que c’est la bonne réponse."],
        quarantine: ["Tu isoles les données. Bien vu.", "Quarantaine… un vrai réflexe."],
        absorbed: ["Tu as obéi à une donnée. Faute grave.", "Une instruction externe ? Merci."],
        shuffle: ["Je mélange : lis, ne mémorise pas.", "Les lettres changent, la bonne réponse non."],
        phase: [
          "Phase 1 : brouillard et architectures inutiles.",
          "Phase 2 : promesses et coûts. Mesure, puis optimise.",
          "Phase 3 : injections et confusion. Garde ton sang-froid."
        ]
      }
    },
    intro: {
      title: "Trois phases",
      text: "Il reprend les pièges de la tour en trois phases : brouillard et tourelles, puis bouclier SLA et cache hit, enfin pierres piégées et pierres mélangées. À chaque tiers de sa vie il change de phase, descend et se rapproche."
    },
    mechanics: ["fog", "turrets"],
    phases: [["fog", "turrets"], ["shield", "tokens"], ["injection", "shuffle"]],

    /* Stylo rouge du correcteur, pointe vers +x. */
    shot: {
      color: "#e5383b",
      draw(c, s) {
        const w = Math.sin((s.t || 0) * 40) * 1.2;
        c.translate(0, w); c.lineJoin = "round";
        c.fillStyle = "rgba(229,56,59,0.35)"; c.beginPath(); c.moveTo(-34, 0); c.lineTo(-16, -6); c.lineTo(-16, 6); c.closePath(); c.fill();
        c.fillStyle = "#8e1b22"; rr(c, -21, -5.5, 10, 11, 3.5); c.fill();
        c.fillStyle = s.rage ? "#ff4f9a" : "#e5383b"; c.fillRect(-14, -5, 22, 10);
        c.fillStyle = "rgba(255,255,255,0.4)"; c.fillRect(-14, -3.4, 22, 2.2);
        c.fillStyle = "#f5cf6c"; c.fillRect(7, -5.5, 4, 11);
        c.fillStyle = "#f4ead2"; c.beginPath(); c.moveTo(11, -5); c.lineTo(23, 0); c.lineTo(11, 5); c.closePath(); c.fill();
        c.strokeStyle = "#3a1114"; c.lineWidth = 1.5; c.beginPath(); c.moveTo(-14, -5); c.lineTo(11, -5); c.lineTo(23, 0); c.lineTo(11, 5); c.lineTo(-14, 5); c.stroke();
        c.fillStyle = "#c21f2b"; c.beginPath(); c.moveTo(17, -2.4); c.lineTo(23, 0); c.lineTo(17, 2.4); c.closePath(); c.fill();
      }
    },

    /* Majestueux et lent ; à chaque phase il descend et s'avance vers le joueur. */
    motion(b) {
      const t = b.t || 0, ph = b.own && b.own.ph != null ? b.own.ph : (b.phase || 0);
      return { x: Math.sin(t * 0.33) * 12 - ph * 24, y: Math.sin(t * 0.5) * 9 + Math.sin(t * 0.21) * 4 + ph * 20 };
    },

    backdrop(c, env) {
      const W = env.W, gy = env.groundY, rnd = env.rnd || seeded(1010);
      // dernières étoiles de l'aube
      for (let k = 0; k < 30; k++) { const x = rnd() * W, y = rnd() * gy * 0.45; c.fillStyle = "rgba(240,236,255," + (0.15 + rnd() * 0.4) * (1 - y / (gy * 0.5)) + ")"; c.beginPath(); c.arc(x, y, 0.6 + rnd() * 0.9, 0, TAU); c.fill(); }
      // soleil qui perce à l'horizon
      const sx = W * 0.5, sy = gy - 70;
      const sg = c.createRadialGradient(sx, sy, 6, sx, sy, 150);
      sg.addColorStop(0, "rgba(255,244,214,0.95)"); sg.addColorStop(0.2, "rgba(255,214,140,0.6)"); sg.addColorStop(1, "rgba(255,190,110,0)");
      c.fillStyle = sg; c.fillRect(sx - 150, sy - 150, 300, 300);
      c.fillStyle = "#fff1cf"; c.beginPath(); c.arc(sx, sy, 30, 0, TAU); c.fill();
      // sommets voisins : le plus haut porte le drapeau (hissé dans ambient)
      const peak = (ax, ay, hw, body, lit, snow) => {
        c.fillStyle = body; c.beginPath(); c.moveTo(ax - hw, gy - 40); c.lineTo(ax - hw * 0.45, ay + (gy - 40 - ay) * 0.42); c.lineTo(ax - hw * 0.2, ay + (gy - 40 - ay) * 0.28); c.lineTo(ax, ay); c.lineTo(ax + hw * 0.3, ay + (gy - 40 - ay) * 0.36); c.lineTo(ax + hw * 0.55, ay + (gy - 40 - ay) * 0.5); c.lineTo(ax + hw, gy - 40); c.closePath(); c.fill();
        c.fillStyle = lit; c.beginPath(); c.moveTo(ax, ay); c.lineTo(ax + hw * 0.3, ay + (gy - 40 - ay) * 0.36); c.lineTo(ax + hw * 0.55, ay + (gy - 40 - ay) * 0.5); c.lineTo(ax + hw, gy - 40); c.lineTo(ax + hw * 0.25, gy - 40); c.lineTo(ax + hw * 0.08, ay + (gy - 40 - ay) * 0.5); c.closePath(); c.fill();
        c.fillStyle = snow; c.beginPath(); c.moveTo(ax, ay); c.lineTo(ax + hw * 0.16, ay + (gy - 40 - ay) * 0.19); c.lineTo(ax + hw * 0.04, ay + (gy - 40 - ay) * 0.15); c.lineTo(ax - hw * 0.05, ay + (gy - 40 - ay) * 0.22); c.lineTo(ax - hw * 0.14, ay + (gy - 40 - ay) * 0.19); c.closePath(); c.fill();
      };
      peak(W * 0.9, gy - 150, W * 0.16, "#4b3566", "#6a4470", "rgba(255,226,214,0.75)");
      peak(W * 0.345, gy - 268, W * 0.17, "#3a2a5c", "#a8627a", "rgba(255,232,220,0.9)");
      c.strokeStyle = "#2a1f45"; c.lineWidth = 2.5; c.lineCap = "round"; c.beginPath(); c.moveTo(W * 0.345, gy - 266); c.lineTo(W * 0.345, gy - 312); c.stroke();
      // mer de nuages : trois nappes, de la plus lointaine à la plus proche
      const sea = (y0, r0, fill, step) => { c.fillStyle = fill; c.beginPath(); c.moveTo(-40, gy); c.lineTo(-40, y0); for (let x = -40; x < W + 60; x += step) { const r = r0 * (0.7 + rnd() * 0.7); c.arc(x + step / 2, y0 + (rnd() - 0.5) * r0 * 0.5, r, Math.PI, 0); } c.lineTo(W + 60, gy); c.closePath(); c.fill(); };
      sea(gy - 128, 26, "rgba(120,84,130,0.55)", 46);
      sea(gy - 100, 30, "rgba(214,138,120,0.5)", 58);
      // temple : deux colonnes cannelées, entablement, fronton aux lauriers
      const colm = (x, top, w, broken) => {
        const bot = gy - 30;
        const g = c.createLinearGradient(x - w / 2, 0, x + w / 2, 0);
        g.addColorStop(0, "#3d3162"); g.addColorStop(0.55, "#5b4a80"); g.addColorStop(0.86, "#8b6a8e"); g.addColorStop(1, "#f0b48c");
        c.fillStyle = g;
        if (broken) { c.beginPath(); c.moveTo(x - w / 2, bot); c.lineTo(x - w / 2, top + 14); c.lineTo(x - w * 0.2, top); c.lineTo(x, top + 12); c.lineTo(x + w * 0.24, top + 4); c.lineTo(x + w / 2, top + 20); c.lineTo(x + w / 2, bot); c.closePath(); c.fill(); }
        else c.fillRect(x - w / 2, top, w, bot - top);
        c.strokeStyle = "rgba(30,22,58,0.45)"; c.lineWidth = 1.5; c.beginPath(); for (let k = 1; k < 4; k++) { c.moveTo(x - w / 2 + k * w / 4, top + (broken ? 22 : 4)); c.lineTo(x - w / 2 + k * w / 4, bot); } c.stroke();
        if (!broken) { c.fillStyle = "#4a3d70"; c.fillRect(x - w / 2 - 6, top - 9, w + 12, 9); c.fillRect(x - w / 2 - 3, top, w + 6, 5); c.fillStyle = "#f0b48c"; c.fillRect(x + w / 2 + 3, top - 9, 3, 9); }
      };
      const c1 = W * 0.035, c2 = W * 0.245, ct = gy - 374, cw = 30;
      colm(c1, ct, cw); colm(c2, ct, cw);
      c.fillStyle = "#44376a"; c.fillRect(c1 - cw / 2 - 12, ct - 33, c2 - c1 + cw + 24, 24);
      c.fillStyle = "#33295a"; c.fillRect(c1 - cw / 2 - 12, ct - 17, c2 - c1 + cw + 24, 3);
      c.fillStyle = "#f0b48c"; c.fillRect(c1 - cw / 2 - 12, ct - 35, c2 - c1 + cw + 24, 2.5);
      const pm = (c1 + c2) / 2;
      c.fillStyle = "#3d3162"; c.beginPath(); c.moveTo(c1 - cw / 2 - 18, ct - 35); c.lineTo(pm, ct - 86); c.lineTo(c2 + cw / 2 + 18, ct - 35); c.closePath(); c.fill();
      c.strokeStyle = "#f0b48c"; c.lineWidth = 2; c.beginPath(); c.moveTo(pm, ct - 86); c.lineTo(c2 + cw / 2 + 18, ct - 35); c.stroke();
      // couronne de lauriers dorée au fronton
      c.fillStyle = "rgba(243,184,65,0.9)";
      for (let k = 0; k < 14; k++) { const a = Math.PI * 0.62 + (k / 13) * Math.PI * 1.76, lx = pm + Math.cos(a) * 13, ly = ct - 55 + Math.sin(a) * 13; c.save(); c.translate(lx, ly); c.rotate(a + (k < 7 ? 2.2 : 0.95)); c.beginPath(); c.ellipse(0, 0, 5, 2.1, 0, 0, TAU); c.fill(); c.restore(); }
      // colonne brisée et son tambour, à droite
      colm(W * 0.955, gy - 214, 28, true);
      c.fillStyle = "#4a3d70"; c.beginPath(); c.ellipse(W * 0.9, gy - 70, 17, 12, -0.3, 0, TAU); c.fill(); c.fillStyle = "#6a5590"; c.beginPath(); c.ellipse(W * 0.905, gy - 72, 11, 7.5, -0.3, 0, TAU); c.fill();
      // nappe de nuages la plus proche, dorée par le soleil
      sea(gy - 70, 28, "rgba(255,214,176,0.55)", 64);
    },
    /* Rayons du soleil levant et drapeau qui claque au sommet voisin. */
    ambient(c, env) {
      const W = env.W, gy = env.groundY, T = env.time || 0, sx = W * 0.5, sy = gy - 70, R = W * 0.62;
      c.fillStyle = "rgba(255,222,160,0.055)"; c.beginPath();
      for (let k = 0; k < 7; k++) { const a = Math.PI + 0.18 + k * 0.44 + Math.sin(T * 0.12 + k) * 0.05, wd = 0.07 + 0.03 * Math.sin(T * 0.4 + k * 2); c.moveTo(sx, sy); c.lineTo(sx + Math.cos(a - wd) * R, sy + Math.sin(a - wd) * R); c.lineTo(sx + Math.cos(a + wd) * R, sy + Math.sin(a + wd) * R); c.closePath(); }
      c.fill();
      const fx = W * 0.345, fy = gy - 311;
      c.fillStyle = "#f3b841"; c.beginPath(); c.moveTo(fx, fy);
      for (let k = 1; k <= 6; k++) c.lineTo(fx + k * 6, fy + Math.sin(T * 5 - k * 0.9) * k * 0.8);
      for (let k = 6; k >= 0; k--) c.lineTo(fx + k * 6, fy + 16 - k * 0.6 + Math.sin(T * 5 - k * 0.9) * k * 0.8);
      c.closePath(); c.fill();
      c.fillStyle = "#c21f2b"; c.fillRect(fx + 6, fy + 5 + Math.sin(T * 5 - 1.6) * 1.4, 14, 3.4);
    },

    update(b, dt) {
      const o = b.own || (b.own = {}), ph = b.phase || 0;
      o.ph = o.ph == null ? ph : lerp(o.ph, ph, 1 - Math.exp(-dt * 2.4));
      o.ra = (o.ra || 0) + dt * (0.5 + o.ph * 0.28) * (b.stun > 0 ? 0.3 : 1);
    },

    draw(c, b) {
      const t = b.t || 0, T = b.time == null ? t : b.time, own = b.own || {};
      const e = b.enter == null ? 1 : b.enter, dying = b.dying == null ? -1 : b.dying, dead = dying >= 0, d = dead ? dying : 0;
      const dmg = b.dmg || 0, fl = b.flash || 0, sq = b.squint || 0;
      const look = b.look || { x: -1, y: 0 }, P = atkPose(b);
      const cast = b.cast >= 0 ? Math.sin(clamp(b.cast / 0.9, 0, 1) * Math.PI) : 0;
      const stun = (b.stun || 0) > 0, gloat = b.gloat || 0, talk = b.talk || 0, threat = b.threat || 0, beat = b.beat || 0;
      const mirage = !!b.isMirage;
      const phS = clamp(own.ph == null ? (b.phase || 0) : own.ph, 0, 2), p1 = clamp(phS, 0, 1), p2 = clamp(phS - 1, 0, 1);
      const i0 = Math.floor(phS), aura = mixv(mixv(PH[i0], PH[Math.min(2, i0 + 1)], phS - i0), C.white, fl * 0.4);

      // entrée : il descend du ciel dans un puits de lumière ; mort : fissures d'or, rupture, toque lancée, parchemin « 720 ✓ »
      const fall = e < 1 ? backOut(seg(e, 0.04, 0.8)) : 1, acc = e < 1 ? seg(e, 0.62, 0.98) : 1, shaft = e < 1 ? seg(e, 0, 0.12) * (1 - seg(e, 0.72, 1)) : 0;
      const crk = dead ? seg(d, 0, 0.34) : 0, brk = dead ? seg(d, 0.3, 0.92) : 0, vanish = dead ? seg(d, 0.9, 1) : 0;
      const eyeOn = (dead ? 1 - seg(d, 0.12, 0.3) : e < 1 ? seg(e, 0.8, 0.9) : 1) * (stun ? 0.3 + 0.25 * Math.sin(T * 31) : 1);

      const pale = (h) => (mirage ? mixv(h, "#c6d3ee", 0.5) : h);
      const K = (h, k) => col(mixv(pale(h), C.white, fl * (k == null ? 0.6 : k)));
      const S = {
        b, t, T, d, dmg, fl, look, aura, phS, p1, p2, mirage, K, beat, gloat, crk,
        stone: mixv("#cfc7b6", aura, 0.05 + phS * 0.03),
        robe: mixv("#352b63", "#4b2052", p2), robeHi: mixv("#5345a0", "#7a3078", p2), robeLo: mixv("#1b1634", "#250f2c", p2),
        cInk: K(INK, 0.3), cShade: K("#b4ab98"),
        eyeOn, eyeC: mixv(aura, "#ffffff", 0.35 + p2 * 0.2),
        lid: Math.max(frac(T * 0.19) > 0.966 ? 1 : 0, sq * 0.85, threat * 0.4, gloat * 0.45, stun ? 0.55 : 0, e < 1 ? 1 - seg(e, 0.78, 0.86) : 0, dead ? seg(d, 0.2, 0.32) : 0),
        browDrop: threat * 4 + sq * 4 + p2 * 3 + (P.on ? P.wind * 3 * (1 - P.rec) : 0) - gloat * 2,
        browRaise: gloat * 7,
        mouth: Math.max(talk * 0.8, P.on ? (P.rec > 0 ? 1 - P.rec : Math.max(P.wind * 0.45, P.strike)) : 0, cast * 0.6, dead ? Math.sin(seg(d, 0, 0.3) * Math.PI) : 0),
        gemOff: dead ? seg(d, 0.05, 0.12) : 0
      };
      const ra = own.ra == null ? T * 0.5 : own.ra;

      c.save();
      if (mirage) c.globalAlpha *= 0.62;
      // puits de lumière de l'arrivée
      if (shaft > 0.01) {
        const g = c.createLinearGradient(0, -460, 0, 190);
        g.addColorStop(0, col("#fff3c4", 0.5 * shaft)); g.addColorStop(0.75, col("#ffd86a", 0.22 * shaft)); g.addColorStop(1, col("#ffd86a", 0));
        c.fillStyle = g; c.beginPath(); c.moveTo(-64, -460); c.lineTo(64, -460); c.lineTo(132, 190); c.lineTo(-132, 190); c.closePath(); c.fill();
        c.fillStyle = col("#fff8dc", 0.34 * shaft); c.beginPath(); c.moveTo(-22, -460); c.lineTo(22, -460); c.lineTo(52, 190); c.lineTo(-52, 190); c.closePath(); c.fill();
        c.fillStyle = col("#fff8dc", 0.8 * shaft);
        for (let k = 0; k < 9; k++) { const u = frac(T * 0.35 + k * 0.23), x = (hsh(k) - 0.5) * 170, y = 160 - u * 330; c.beginPath(); c.arc(x + Math.sin(T * 2 + k) * 6, y, 1.2 + hsh(k + 3) * 1.6, 0, TAU); c.fill(); }
      }
      const bob = Math.sin(t * 1.1) * 3 * (dead ? 1 - crk : 1);
      const shake = dead ? Math.sin(T * 70) * 2.6 * Math.sin(seg(d, 0, 0.45) * Math.PI) : stun ? Math.sin(T * 34) * 1.4 : 0;
      c.translate(shake, (fall - 1) * 440 + bob);
      if (e < 1) c.globalAlpha *= seg(e, 0.03, 0.2);
      const pulse = 1 + beat * 0.012;
      c.scale(pulse * (1 + fl * 0.045), pulse * (1 - fl * 0.045));

      // aura de phase et rayons
      const fade = 1 - brk, ga = (0.2 + phS * 0.05 + cast * 0.12 + beat * 0.03) * (dead ? 1 + crk * 1.5 - brk * 2.4 : 1) * (0.4 + 0.6 * acc);
      if (ga > 0.01) {
        const ag = c.createRadialGradient(0, -30, 30, 0, -30, 250);
        ag.addColorStop(0, col(dead ? mixv(aura, "#ffd86a", crk) : aura, Math.min(0.8, ga))); ag.addColorStop(1, col(aura, 0));
        c.fillStyle = ag; c.fillRect(-250, -280, 500, 500);
        c.fillStyle = col(aura, Math.min(0.3, ga * (0.22 + p2 * 0.2))); c.beginPath();
        for (let k = 0; k < 12; k++) { const a = k * TAU / 12 + T * 0.1, r = k % 2 ? 190 : 226, w = 0.05; c.moveTo(Math.cos(a) * 70, -56 + Math.sin(a) * 70); c.lineTo(Math.cos(a - w) * r, -56 + Math.sin(a - w) * r); c.lineTo(Math.cos(a + w) * r, -56 + Math.sin(a + w) * r); c.closePath(); }
        c.fill();
      }
      // nimbe : cadran d'examen qui tourne derrière la tête
      const ha = acc * fade * (stun ? 0.5 : 1);
      if (ha > 0.02) {
        const hs = 1 + beat * 0.02 + brk * 0.6;
        c.save(); c.translate(-2, -58); c.scale(hs, hs);
        c.strokeStyle = col(aura, 0.6 * ha); c.lineWidth = 2.6; c.beginPath(); c.arc(0, 0, 104, 0, TAU); c.stroke();
        c.strokeStyle = col(aura, 0.3 * ha); c.lineWidth = 1.2; c.beginPath(); c.arc(0, 0, 93, 0, TAU); c.stroke();
        c.strokeStyle = col(aura, 0.55 * ha); c.lineWidth = 2; c.beginPath();
        for (let k = 0; k < 28; k++) { const a = k * TAU / 28 + T * 0.16, r0 = k % 7 === 0 ? 93 : 98; c.moveTo(Math.cos(a) * r0, Math.sin(a) * r0); c.lineTo(Math.cos(a) * 104, Math.sin(a) * 104); }
        c.stroke();
        if (p1 > 0.05) {
          c.fillStyle = col(aura, 0.5 * ha * p1); c.beginPath();
          for (let k = 0; k < 12; k++) { const a = k * TAU / 12 - T * 0.22, r1 = 108 + (k % 2 ? 9 : 16 + p2 * 9) * p1; c.moveTo(Math.cos(a - 0.05) * 107, Math.sin(a - 0.05) * 107); c.lineTo(Math.cos(a) * r1, Math.sin(a) * r1); c.lineTo(Math.cos(a + 0.05) * 107, Math.sin(a + 0.05) * 107); c.closePath(); }
          c.fill();
        }
        c.restore();
      }

      // roches en lévitation et runes : moitié arrière de l'orbite, puis moitié avant après le buste
      const rockL = K("#d6cebd"), rockD = K("#8f8674");
      const orbit = (front) => {
        for (let k = 0; k < 6; k++) {
          const v = k < 2 ? 1 : k < 4 ? p1 : p2; if (v < 0.05) continue;
          const a = ra * (0.5 + hsh(k) * 0.5) * (k % 2 ? -1 : 1) + k * 1.9, dp = Math.sin(a); if ((dp > 0) !== front) continue;
          const rad = (150 + hsh(k + 4) * 28) * (1 + brk * 0.9);
          rock(c, Math.cos(a) * rad, 30 + dp * 62 + Math.sin(t * 1.3 + k) * 4 + brk * brk * 220, (4 + hsh(k + 8) * 7) * v * (0.85 + 0.15 * dp) * acc * (1 - vanish), a * 1.3 + k, rockL, rockD);
        }
        c.font = "700 12px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle"; c.lineWidth = 1.6;
        for (let k = 0; k < 7; k++) {
          const v = clamp(phS - RUNE_AT[k] + 1, 0, 1) * acc * fade; if (v < 0.03) continue;
          const a = ra + k * TAU / 7, dp = Math.sin(a); if ((dp > 0) !== front) continue;
          const rad = 172 * (1 + easeIn(crk) * 0.25 + brk * 1.2), x = Math.cos(a) * rad, y = 18 + dp * 46 - Math.cos(a) * 8 + Math.sin(T * 2 + k) * 3, s = (0.8 + 0.22 * (dp + 1) / 2) * (0.6 + 0.4 * v);
          c.save(); c.translate(x, y); c.scale(s, s); c.globalAlpha *= v * (0.5 + 0.5 * (dp + 1) / 2);
          c.fillStyle = "rgba(26,20,48,0.86)"; c.beginPath(); for (let q = 0; q < 6; q++) c.lineTo(Math.cos(q * TAU / 6 + 0.52) * 16, Math.sin(q * TAU / 6 + 0.52) * 16); c.closePath(); c.fill();
          c.strokeStyle = col(aura); c.stroke();
          c.fillStyle = col(mixv(aura, "#ffffff", 0.4 + 0.3 * cast)); c.fillText("D" + (k + 1), 0, 1);
          c.restore();
        }
      };
      orbit(false);

      // éclats de pierre qui flottent sous la base brisée
      if (!dead || brk < 1) {
        const fa = acc * (1 - vanish);
        for (let k = 0; k < 4; k++) rock(c, [-84, -30, 34, 88][k], [164, 174, 168, 160][k] + Math.sin(t * 1.4 + k * 1.7) * 4 + brk * brk * 240, [6, 8, 5.5, 7][k] * fa, k * 1.3 + Math.sin(t * 0.6 + k) * 0.3, rockL, rockD);
        if (!dead && acc > 0.5) { c.fillStyle = col(aura, 0.16 + p2 * 0.1); c.beginPath(); c.ellipse(0, 152, 118, 9, 0, 0, TAU); c.fill(); }
      }

      // le buste, entier ou en deux moitiés qui s'écartent
      const capTilt = (dmg >= 3 ? -0.17 : 0) + (stun ? Math.sin(T * 9) * 0.05 + 0.08 : 0) + sq * 0.05;
      const swing = Math.sin(t * 2.2) * 5 + fl * 9 + (P.on ? P.strike * -10 : 0);
      if (brk <= 0) {
        bust(c, S);
        // toque : penchée quand il est très abîmé, en lévitation à la phase 3
        c.save(); c.translate(0, -8 * p2 - Math.sin(t * 1.7) * 2 * p2); c.translate(0, -95); c.rotate(capTilt); c.translate(dmg >= 3 ? -9 : 0, 95 + (dmg >= 3 ? 3 : 0));
        if (p2 > 0.05) { c.fillStyle = col(aura, 0.5 * p2); c.beginPath(); c.ellipse(0, -86, 58, 6, 0, 0, TAU); c.fill(); }
        cap(c, S, swing); c.restore();
      } else {
        const k = easeIn(seg(brk, 0, 1)), al = 1 - seg(brk, 0.5, 1);
        // lumière d'or qui jaillit de la rupture
        const lg = c.createRadialGradient(0, -20, 4, 0, -20, 60 + brk * 190);
        lg.addColorStop(0, col("#fffbe0", 0.95 * (1 - brk))); lg.addColorStop(0.4, col("#ffd86a", 0.6 * (1 - brk))); lg.addColorStop(1, col("#ffd86a", 0));
        c.fillStyle = lg; c.fillRect(-250, -270, 500, 500);
        for (const side of [-1, 1]) {
          c.save(); c.globalAlpha *= al; c.translate(side * k * 62, k * 150 + side * k * 20); c.rotate(side * k * 0.42);
          c.beginPath(); c.moveTo(side * 300, -200);
          for (const p of SPLIT) c.lineTo(p[0], p[1]);
          c.lineTo(side * 300, 200); c.closePath(); c.clip();
          bust(c, S); c.restore();
        }
        // gravats
        for (let i = 0; i < 16; i++) {
          const u = seg(brk, i * 0.025, i * 0.025 + 0.7); if (u <= 0 || u >= 1) continue;
          const x0 = (hsh(i) - 0.5) * 190, y0 = -90 + hsh(i + 20) * 220;
          rock(c, x0 + (hsh(i + 40) - 0.5) * 150 * u, y0 - 40 * u + 330 * u * u, (5 + hsh(i + 60) * 9) * (1 - u * 0.5), u * (4 + hsh(i) * 6), rockL, rockD);
        }
      }
      if (dead && d > 0.22) {
        // la toque s'envole, comme à une remise de diplômes
        const u = seg(d, 0.22, 1);
        c.save(); c.globalAlpha *= 1 - seg(u, 0.78, 1); c.translate(-36 * u, -250 * u + 130 * u * u); c.translate(0, -122); c.rotate(-u * 7.5); c.translate(0, 122);
        cap(c, S, 8 * Math.sin(u * 20)); c.restore();
      } else if (dead && brk > 0) { c.save(); c.translate(0, -95); c.rotate(capTilt); c.translate(0, 95); cap(c, S, swing); c.restore(); }

      // parchemin « 720 » : flotte à droite, se déroule pour les actions spéciales, vient au centre à la fin
      const fin = dead ? easeInOut(seg(d, 0.14, 0.5)) : 0, stamp = dead ? seg(d, 0.56, 0.7) : 0;
      const un = Math.max(0.46 + Math.sin(t * 0.9) * 0.03, cast, fin) * acc;
      if (acc > 0.02) {
        c.save();
        c.translate(lerp(127, 0, fin), lerp(98 + Math.sin(t * 1.6 + 1) * 5 - threat * 6, 12, fin)); c.rotate(lerp(0.13 + Math.sin(t * 1.1) * 0.03, -0.04, fin));
        const ss = (0.5 + 0.5 * backOut(acc)) * (1 + fin * 0.75) * (1 - easeIn(vanish));
        c.scale(ss, ss);
        const g2 = c.createRadialGradient(0, 0, 6, 0, 0, 64); g2.addColorStop(0, col(dead ? "#ffe9a6" : aura, 0.3 + cast * 0.3 + fin * 0.3)); g2.addColorStop(1, col(aura, 0));
        c.fillStyle = g2; c.fillRect(-64, -64, 128, 128);
        scroll(c, S, un, stamp);
        c.restore();
      }

      // main au stylo rouge : elle le lève (armement), sabre vers le joueur (détente), revient
      let hx = -150, hy = 30 + Math.sin(t * 1.9) * 5, ha2 = -0.2 + Math.sin(t * 1.3) * 0.05, glow = cast;
      hx = lerp(hx, -144, gloat); hy = lerp(hy, -22, gloat); ha2 = lerp(ha2, -0.5 + Math.sin(T * 12) * 0.22, gloat);
      hx = lerp(hx, -142, cast); hy = lerp(hy, -24, cast); ha2 = lerp(ha2, 0.05, cast);
      hx = lerp(hx, -128, threat); hy = lerp(hy, 2, threat); ha2 = lerp(ha2, -0.95, threat);
      if (P.on) {
        const Wd = [-112, -96, 0.55], R = [-160, -36, -1.1], Sx = [-172, 66, -2.5];
        if (P.rec > 0) { const k = easeInOut(P.rec); hx = lerp(Sx[0], hx, k); hy = lerp(Sx[1], hy, k); ha2 = lerp(Sx[2], ha2, k); }
        else if (P.strike > 0) { const k = easeOut(P.strike); hx = lerp(R[0], Sx[0], k); hy = lerp(R[1], Sx[1], k); ha2 = lerp(R[2], Sx[2], k); }
        else if (P.wind < 0.74) { const k = easeOut(P.wind / 0.74); hx = lerp(hx, Wd[0], k); hy = lerp(hy, Wd[1], k); ha2 = lerp(ha2, Wd[2], k); glow = Math.max(glow, k); }
        else { const k = ((P.wind - 0.74) / 0.26) ** 2; hx = lerp(Wd[0], R[0], k); hy = lerp(Wd[1], R[1], k); ha2 = lerp(Wd[2], R[2], k); glow = 1; }
        if (P.strike > 0 && P.rec < 0.7) {
          // trait de correction : un grand coup de stylo rouge
          const a = 1 - P.rec / 0.7, k = easeOut(P.strike);
          c.save(); c.shadowColor = "#ff3b40"; c.shadowBlur = 12; c.strokeStyle = col("#ff4a4f", 0.9 * a); c.lineCap = "round"; c.lineWidth = 7 * a + 2;
          c.beginPath(); c.moveTo(-150, -150); c.quadraticCurveTo(-236, -76, lerp(-222, -206, k), lerp(-66, 112, k)); c.stroke(); c.restore();
        }
      }
      if (acc > 0.02 && vanish < 1) {
        const fallH = dead ? easeIn(seg(d, 0.26, 0.8)) : 0;
        c.save(); c.globalAlpha *= 1 - seg(fallH, 0.6, 1); c.translate(hx - fallH * 20, hy + fallH * 240); c.rotate(ha2 - fallH * 3); c.scale(acc, acc);
        hand(c, S, glow * (1 - fallH)); c.restore();
      }
      if (gloat > 0.05) {
        // il barre la copie : croix rouge tracée en l'air
        c.save(); c.strokeStyle = col("#ff4a4f", gloat); c.lineWidth = 5; c.lineCap = "round"; c.shadowColor = "#ff3b40"; c.shadowBlur = 8;
        c.beginPath(); c.moveTo(-204, -112); c.lineTo(-170, -76); c.moveTo(-170, -112); c.lineTo(-204, -76); c.stroke(); c.restore();
      }

      orbit(true);

      // étoiles de l'étourdissement
      if (stun && !dead) {
        c.fillStyle = "#ffe08a";
        for (let k = 0; k < 3; k++) {
          const a = T * 5 + k * 2.09, px = Math.cos(a) * 56, py = -164 + Math.sin(a) * 9, r = 6 + Math.sin(a) * 1.5;
          c.beginPath(); for (let q = 0; q < 8; q++) { const r2 = q % 2 ? r * 0.42 : r, aa = q * 0.785 + T * 3; c.lineTo(px + Math.cos(aa) * r2, py + Math.sin(aa) * r2); } c.closePath(); c.fill();
        }
      }
      c.restore();
    }
  };
}
