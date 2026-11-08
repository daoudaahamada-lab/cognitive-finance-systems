/* Étage 2 — Le Sur-Ingénieur : un robot fait de trop de modules, avec un gros bouton DEPLOY sur le torse. */
BOSSES[2] = {
  palette: { main: "#6f86b8", dark: "#26304f", accent: "#f39a3b", eye: "#7fe3ff", rage: "#ff4f9a" },
  hit: { rx: 114, ry: 118, coreR: 20 },
  top: 162,
  attackFrom: { x: -204, y: -14 },
  castLean: -0.08,
  weakSpot: () => ({ x: 0, y: 14 }),
  critLabel: "DEPLOY ANNULÉ",
  lines: {
    hit: ["Ma couche d’abstraction !", "Il me faut un agent de plus.", "Rien de grave, j’ai douze replis."],
    crit: ["Pas le bouton DEPLOY !", "Tu as visé la mise en prod ?!"],
    wrong: ["Ajoutons un orchestrateur.", "Trop simple pour être vrai.", "Un agent de plus et ça passe."],
    timeout: ["Mes agents débattent encore…", "Réunion de synchro, désolé."],
    rage: "Plan B : vingt agents et un méta-orchestrateur !",
    special: {
      build: ["Je construis un agent de plus.", "Une tourelle de plus, par précaution.", "Il manque une couche, non ?"],
      collapse: ["Mes tourelles… inutiles ?", "Ta solution simple les a rasées !"]
    }
  },
  intro: {
    title: "Tourelles multi-agents",
    text: "À chaque question, il construit une tourelle « multi-agents » entre toi et lui, qui arrête tes pierres. Une bonne réponse les fait toutes s’effondrer : la solution simple gagne."
  },
  mechanics: ["turrets"],
  draw(c, b) {
    const t = b.t, fl = b.flash, rg = b.rageT;
    const steel = mixv(mixv("#6f86b8", "#a2477a", rg * 0.6), C.white, fl * 0.7);
    const steelD = mixv(mixv("#3d4b78", "#5a2346", rg * 0.6), C.white, fl * 0.5);
    const orange = mixv("#f39a3b", C.white, fl * 0.5);
    const eye = mixv(mixv("#7fe3ff", C.bad, rg), C.white, fl);
    const spin = t * (b.rage ? 5 : 2);
    const hammer = b.cast >= 0 ? Math.sin(t * 22) : Math.sin(t * 3);
    const box = (x, y, w, h, fill, r) => { rr(c, x, y, w, h, r || 6); c.fillStyle = col(fill); c.fill(); c.strokeStyle = col(steelD); c.lineWidth = 2; c.stroke(); };
    const label = (txt, x, y, size) => { c.font = "600 " + (size || 9) + "px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle"; c.fillStyle = col(mixv("#dfe7ff", C.white, fl), 0.85); c.fillText(txt, x, y); };

    // poing à ressort (riposte) : armement vers l'arrière, puis frappe vers la gauche
    let reach = 0;
    if (b.atk >= 0) {
      const a = b.atk;
      reach = a < 0.22 ? -10 * (a / 0.22) : a < 0.34 ? -10 + 100 * ((a - 0.22) / 0.12) : 90 * Math.max(0, 1 - (a - 0.34) / 0.41);
    }

    const halo = c.createRadialGradient(0, -10, 20, 0, -10, 240);
    halo.addColorStop(0, col(mixv(orange, C.rage, rg), 0.14)); halo.addColorStop(1, col(orange, 0));
    c.fillStyle = halo; c.fillRect(-250, -230, 500, 460);

    // propulseur
    const fh = 18 + Math.sin(t * 30) * 5 + rg * 8;
    c.fillStyle = col(mixv("#ffd27a", C.rage, rg * 0.5), 0.85);
    c.beginPath(); c.moveTo(-16, 82); c.quadraticCurveTo(0, 82 + fh * 1.6, 16, 82); c.fill();
    c.fillStyle = col("#fff4d6", 0.9); c.beginPath(); c.moveTo(-7, 82); c.quadraticCurveTo(0, 82 + fh * 0.8, 7, 82); c.fill();
    c.fillStyle = col(steelD); c.beginPath(); c.moveTo(-26, 60); c.lineTo(26, 60); c.lineTo(18, 84); c.lineTo(-18, 84); c.closePath(); c.fill();

    // câbles emmêlés (derrière)
    c.lineCap = "round"; c.lineWidth = 3;
    const cables = [["#f39a3b", -88, -10, -40, 120, 30, 60, 10, 62], ["#7fe3ff", 90, -10, 140, 90, -60, 110, -14, 64], ["#57c48f", -30, -96, -140, -60, -110, 40, -76, 30], ["#ef6b5c", 40, -96, 130, -150, 150, -30, 104, 10]];
    for (const cb of cables) {
      c.strokeStyle = col(mixv(cb[0], C.white, fl * 0.5), 0.8);
      c.beginPath(); c.moveTo(cb[1], cb[2]); c.bezierCurveTo(cb[3], cb[4] + Math.sin(t * 2 + cb[1]) * 6, cb[5], cb[6], cb[7], cb[8]); c.stroke();
    }

    // modules d'épaule
    box(-106, -36, 34, 44, steel); label("A1", -89, -14, 10);
    box(72, -32, 36, 50, steel); label("A7", 90, -7, 10);
    // engrenage
    c.save(); c.translate(98, 42); c.rotate(spin);
    c.fillStyle = col(mixv("#9aa5c3", C.white, fl));
    c.beginPath();
    for (let k = 0; k < 16; k++) { const a = (k / 16) * Math.PI * 2, r = k % 2 ? 13 : 18; c.lineTo(Math.cos(a) * r, Math.sin(a) * r); }
    c.closePath(); c.fill();
    c.fillStyle = col(steelD); c.beginPath(); c.arc(0, 0, 5, 0, Math.PI * 2); c.fill();
    c.restore();

    // torse
    const tg = c.createLinearGradient(0, -38, 0, 62); tg.addColorStop(0, col(mixv(steel, C.white, 0.15))); tg.addColorStop(1, col(steelD));
    rr(c, -72, -38, 144, 100, 10); c.fillStyle = tg; c.fill(); c.strokeStyle = col(steelD); c.lineWidth = 2.5; c.stroke();
    c.strokeStyle = col(steelD, 0.8); c.lineWidth = 1.5;
    for (let y = 44; y <= 54; y += 5) { c.beginPath(); c.moveTo(34, y); c.lineTo(62, y); c.stroke(); c.beginPath(); c.moveTo(-62, y); c.lineTo(-34, y); c.stroke(); }
    label("agent-07", 42, -26, 8);
    // voyants qui clignotent
    for (let k = 0; k < 5; k++) {
      const on = Math.sin(t * (3 + k * 1.7) + k * 2) > 0;
      const lc = b.rage ? C.bad : [C.ok, C.lamp, C.ok, "#7fe3ff", C.bad][k];
      c.fillStyle = col(lc, on ? 1 : 0.25); c.beginPath(); c.arc(-56 + k * 10, -26, 3, 0, Math.PI * 2); c.fill();
    }
    drawCracks(c, b, "rgba(230,236,250,0.75)", 1.8);

    // bouton DEPLOY (point faible)
    const pulse = 1 + Math.sin(t * 5) * 0.07;
    const bg = c.createRadialGradient(0, 14, 4, 0, 14, 40 * pulse); bg.addColorStop(0, "rgba(239,107,92,0.55)"); bg.addColorStop(1, "rgba(239,107,92,0)");
    c.fillStyle = bg; c.beginPath(); c.arc(0, 14, 40 * pulse, 0, Math.PI * 2); c.fill();
    c.fillStyle = col(steelD); c.beginPath(); c.arc(0, 14, 23, 0, Math.PI * 2); c.fill();
    c.fillStyle = "#f2c14e"; c.beginPath(); c.arc(0, 14, 21, 0, Math.PI * 2); c.fill();
    const dg = c.createRadialGradient(-5, 8, 2, 0, 14, 18); dg.addColorStop(0, col(mixv("#ff9a8c", C.white, fl))); dg.addColorStop(1, col(mixv("#c63b2f", C.white, fl * 0.5)));
    c.fillStyle = dg; c.beginPath(); c.arc(0, 14, 17, 0, Math.PI * 2); c.fill();
    c.font = "700 8px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle"; c.fillStyle = "#fff4f0"; c.fillText("DEPLOY", 0, 15);

    // petits bras porte-outils
    const arm = (sx, sy, ang, len, tool, ph) => {
      const a = ang + hammer * 0.35 * (ph % 2 ? 1 : -1);
      const ex = sx + Math.cos(a) * len, ey = sy + Math.sin(a) * len;
      const tx = ex + Math.cos(a + 0.6) * len * 0.8, ty = ey + Math.sin(a + 0.6) * len * 0.8;
      c.strokeStyle = col(mixv("#9aa5c3", C.white, fl)); c.lineWidth = 4;
      c.beginPath(); c.moveTo(sx, sy); c.lineTo(ex, ey); c.lineTo(tx, ty); c.stroke();
      c.fillStyle = col(orange); c.strokeStyle = col(orange); c.lineWidth = 3;
      if (tool === "wrench") { c.beginPath(); c.arc(tx, ty, 6, 0.6, Math.PI * 2 - 0.6); c.stroke(); }
      else if (tool === "hammer") { c.fillRect(tx - 7, ty - 4, 14, 8); }
      else if (tool === "driver") { c.beginPath(); c.moveTo(tx, ty); c.lineTo(tx + Math.cos(a + 0.6) * 12, ty + Math.sin(a + 0.6) * 12); c.stroke(); }
      else { c.fillStyle = col("#dfe7ff"); c.fillRect(tx - 6, ty - 8, 12, 15); c.fillStyle = col(steelD); c.fillRect(tx - 4, ty - 4, 8, 1.5); c.fillRect(tx - 4, ty, 8, 1.5); }
    };
    arm(-72, 24, Math.PI * 0.85, 18, "wrench", 0);
    arm(-72, 46, Math.PI * 0.7, 16, "driver", 1);
    arm(72, 26, Math.PI * 0.15, 18, "hammer", 2);
    arm(72, 50, Math.PI * 0.3, 14, "board", 3);

    // extenseur à ciseaux + gant de boxe
    const sx0 = -106, sy0 = -14, gx = -116 - reach;
    c.strokeStyle = col(mixv("#9aa5c3", C.white, fl)); c.lineWidth = 2.5;
    const seg = 5, span = (sx0 - gx);
    c.beginPath(); c.moveTo(sx0, sy0);
    for (let k = 1; k <= seg; k++) c.lineTo(sx0 - (span * k) / seg, sy0 + (k % 2 ? -7 : 7));
    c.stroke();
    c.fillStyle = col(mixv("#d8443a", C.white, fl)); c.beginPath(); c.arc(gx - 6, sy0, 13, 0, Math.PI * 2); c.fill();
    c.beginPath(); c.arc(gx - 2, sy0 - 11, 6, 0, Math.PI * 2); c.fill();
    c.fillStyle = "#f2ead7"; c.fillRect(gx + 4, sy0 - 6, 6, 12);

    // tête
    c.fillStyle = col(steelD); c.fillRect(-14, -44, 28, 8);
    box(-48, -98, 96, 58, steel, 10);
    rr(c, -44, -84, 84, 28, 8); c.fillStyle = col("#0e1426"); c.fill();
    c.save(); c.globalAlpha = b.stun > 0 ? 0.4 : 1;
    angryEyes(c, 6, -73, 16, 7, eye, b.squint, 10);
    c.restore();
    const mouthOpen = b.atk >= 0.2 && b.atk < 0.5 ? 1 : 0;
    c.fillStyle = col(eye, 0.8);
    for (let k = 0; k < 5; k++) c.fillRect(-24 + k * 8, -50 - mouthOpen * 2, 5, 3 + mouthOpen * 4);

    // pile de modules sur la tête : elle se simplifie quand il perd de la vie
    const stack = Math.max(0, Math.ceil(clamp(b.hpFrac, 0, 1) * 3));
    const names = ["orch", "router", "meta"];
    for (let k = 0; k < stack; k++) {
      c.save(); c.translate(4 + k * 6, -98 - 18 * k - 9); c.rotate(Math.sin(t * 2 + k) * 0.05 + k * 0.04);
      box(-(22 - k * 3), -9, 44 - k * 6, 18, steel, 4); label(names[k], 0, 0, 8);
      c.restore();
    }
    // antennes
    const antTop = -98 - 18 * stack;
    c.strokeStyle = col(mixv("#9aa5c3", C.white, fl)); c.lineWidth = 2;
    c.beginPath(); c.moveTo(-36, -98); c.lineTo(-48, -138); c.moveTo(14 + stack * 6, antTop); c.lineTo(22 + stack * 6, antTop - 26); c.stroke();
    const blink = Math.sin(t * 6) > 0 || b.rage;
    c.fillStyle = col(b.rage ? C.bad : C.ok, blink ? 1 : 0.3); c.beginPath(); c.arc(-48, -140, 4, 0, Math.PI * 2); c.fill();
    c.fillStyle = col(C.lamp, Math.sin(t * 4 + 1) > 0 ? 1 : 0.3); c.beginPath(); c.arc(22 + stack * 6, antTop - 28, 4, 0, Math.PI * 2); c.fill();

    // barre de construction pendant une action spéciale
    if (b.cast >= 0) {
      const k = clamp(b.cast / 0.9, 0, 1);
      rr(c, 66, -132, 96, 12, 4); c.fillStyle = "rgba(12,17,30,0.85)"; c.fill(); c.strokeStyle = col(orange); c.lineWidth = 1.5; c.stroke();
      rr(c, 68, -130, 92 * k, 8, 3); c.fillStyle = col(orange); c.fill();
      label("BUILD agent-" + (8 + Math.floor(k * 4)), 114, -142, 9);
    }
  }
};
