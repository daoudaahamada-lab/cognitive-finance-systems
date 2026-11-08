/* Étage 8 — La Promesse à 99,9 % : un ballon-vendeur gonflé de certitudes, contrat à la main. */
BOSSES[8] = {
  palette: { main: "#f3d27a", dark: "#1f2a4f", accent: "#fff6d8", eye: "#1b1405", rage: "#ff6b4a" },
  hit: { rx: 104, ry: 142, coreR: 24 },
  top: 158,
  attackFrom: { x: -176, y: -40 },
  castLean: -0.1,
  weakSpot: () => ({ x: -4, y: 40 }),
  critLabel: "PROMESSE PERCÉE",
  lines: {
    hit: ["Ce n’est qu’une petite marge d’erreur…", "Mon annexe !", "Aïe, un chiffre mesuré."],
    crit: ["Mon badge 99,9 % !", "Tu as lu les petites lignes ?!"],
    wrong: ["Signé ! Merci pour la confiance.", "Promis, ça tiendra en production.", "Le client adore ce chiffre."],
    timeout: ["Le client n’attend pas, signe !", "Trop tard, j’ai déjà promis."],
    rage: "Très bien : 100 % garanti, sans évaluation !",
    special: {
      shieldUp: ["Mon bouclier SLA est regonflé !", "Une erreur ? Encore plus de promesses !"],
      shieldBreak: ["Trois preuves d’affilée ?! Mon SLA éclate !", "Non… pas des mesures !"]
    }
  },
  intro: {
    title: "Bouclier SLA",
    text: "Son bouclier « 99,9 % » divise tes dégâts par deux tant que tu n’enchaînes pas 3 bonnes réponses. Une erreur le regonfle : seules des preuves répétées font tomber une promesse."
  },
  mechanics: ["shield"],
  init(b) { b.own.sweat = []; b.own.sweatT = 0; },
  update(b, dt) {
    const o = b.own;
    const shieldDown = b.mech && b.mech.shield && b.mech.shield.up === false;
    o.sweatT -= dt;
    if ((shieldDown || b.rage || b.hpFrac < 0.3) && o.sweatT <= 0) {
      o.sweatT = rand(0.35, 0.8);
      o.sweat.push({ x: rand(-36, 26), y: rand(-34, -22), vy: rand(10, 25), life: 0 });
    }
    for (const s of o.sweat) { s.vy += 160 * dt; s.y += s.vy * dt; s.life += dt; }
    o.sweat = o.sweat.filter((s) => s.life < 1.1);
  },
  draw(c, b) {
    const fl = b.flash, rt = b.rageT, t = b.t;
    const castK = b.cast >= 0 ? Math.sin(Math.min(1, b.cast / 0.9) * Math.PI) : 0;
    const breathe = 1 + Math.sin(t * 2.4) * 0.025 + castK * 0.08;
    const deflate = 0.84 + 0.16 * clamp(b.hpFrac, 0, 1);
    const gold = mixv(mixv("#f3d27a", "#ff7a52", rt * 0.6), C.white, fl * 0.7);
    const goldDark = mixv(mixv("#c4922f", "#b8402c", rt * 0.6), C.white, fl * 0.5);
    const suit = mixv(mixv("#22305a", "#4a1f33", rt * 0.55), C.white, fl * 0.45);
    const suitLight = mixv(suit, C.white, 0.18);
    const shirt = mixv("#f4f1e8", C.white, fl);
    const ink = "#1b1405";

    // halo doré
    const ag = c.createRadialGradient(0, 0, 30, 0, 0, 240);
    ag.addColorStop(0, col(gold, 0.2)); ag.addColorStop(1, col(gold, 0));
    c.fillStyle = ag; c.fillRect(-250, -240, 500, 480);

    const bodyY = 30, bodyRx = 86 * breathe, bodyRy = 84 * deflate * breathe;
    const knotY = bodyY + bodyRy;

    // ficelle du ballon
    const sway = Math.sin(t * 1.7) * 12;
    c.strokeStyle = "rgba(232,236,246,0.55)"; c.lineWidth = 1.5; c.beginPath();
    c.moveTo(0, knotY + 6);
    c.bezierCurveTo(14 + sway, knotY + 40, -16 - sway, knotY + 70, 6 + sway * 0.6, 196);
    c.stroke();
    c.fillStyle = col(goldDark); c.beginPath(); c.moveTo(-7, knotY - 2); c.lineTo(7, knotY - 2); c.lineTo(3, knotY + 8); c.lineTo(-3, knotY + 8); c.closePath(); c.fill();

    // bras arrière (main sur la hanche)
    c.lineCap = "round"; c.lineJoin = "round";
    c.strokeStyle = col(suit); c.lineWidth = 22;
    c.beginPath(); c.moveTo(70, bodyY - 30); c.quadraticCurveTo(122, bodyY + 4, 84, bodyY + 40); c.stroke();
    c.fillStyle = col(gold); c.beginPath(); c.arc(84, bodyY + 40, 11, 0, Math.PI * 2); c.fill();

    // ventre ballon
    const bg = c.createRadialGradient(-30, bodyY - 40, 10, 0, bodyY, bodyRx * 1.2);
    bg.addColorStop(0, col(mixv(gold, C.white, 0.45))); bg.addColorStop(0.55, col(gold)); bg.addColorStop(1, col(goldDark));
    c.fillStyle = bg; c.beginPath(); c.ellipse(0, bodyY, bodyRx, bodyRy, 0, 0, Math.PI * 2); c.fill();

    // veste ouverte sur le ventre
    c.save(); c.beginPath(); c.ellipse(0, bodyY, bodyRx, bodyRy, 0, 0, Math.PI * 2); c.clip();
    c.fillStyle = col(suit);
    c.beginPath(); c.moveTo(-110, bodyY - 120); c.lineTo(-24, bodyY - 92); c.quadraticCurveTo(-58, bodyY + 10, -40, bodyY + 130); c.lineTo(-110, bodyY + 130); c.closePath(); c.fill();
    c.beginPath(); c.moveTo(110, bodyY - 120); c.lineTo(24, bodyY - 92); c.quadraticCurveTo(58, bodyY + 10, 40, bodyY + 130); c.lineTo(110, bodyY + 130); c.closePath(); c.fill();
    c.fillStyle = col(suitLight);
    c.beginPath(); c.moveTo(-24, bodyY - 92); c.lineTo(-48, bodyY - 30); c.lineTo(-36, bodyY - 80); c.closePath(); c.fill();
    c.beginPath(); c.moveTo(24, bodyY - 92); c.lineTo(48, bodyY - 30); c.lineTo(36, bodyY - 80); c.closePath(); c.fill();
    c.fillStyle = col(mixv(gold, C.white, 0.5));
    for (const y of [bodyY - 10, bodyY + 30]) { c.beginPath(); c.arc(-50, y, 3.5, 0, Math.PI * 2); c.fill(); }
    c.restore();
    // reflet du ballon
    c.fillStyle = "rgba(255,255,255,0.32)"; c.beginPath(); c.ellipse(-44, bodyY - 30, 10, 22, 0.5, 0, Math.PI * 2); c.fill();

    // cravate
    c.fillStyle = col(mixv("#d8443a", C.white, fl * 0.5));
    c.beginPath(); c.moveTo(-7, bodyY - 84); c.lineTo(7, bodyY - 84); c.lineTo(4, bodyY - 74); c.lineTo(-4, bodyY - 74); c.closePath(); c.fill();
    c.beginPath(); c.moveTo(-4, bodyY - 74); c.lineTo(4, bodyY - 74); c.lineTo(10, bodyY - 20); c.lineTo(0, bodyY - 8); c.lineTo(-10, bodyY - 20); c.closePath(); c.fill();

    // badge 99,9 % (point faible)
    const ws = { x: -4, y: 40 };
    const pulse = 1 + Math.sin(b.time * 4) * 0.05;
    const shieldDown = b.mech && b.mech.shield && b.mech.shield.up === false;
    c.save(); c.translate(ws.x, ws.y); c.scale(pulse, pulse);
    c.shadowColor = col(gold); c.shadowBlur = 12;
    c.fillStyle = col(mixv("#fff3c4", C.white, fl)); c.beginPath(); c.arc(0, 0, 25, 0, Math.PI * 2); c.fill();
    c.shadowBlur = 0;
    c.strokeStyle = col(goldDark); c.lineWidth = 3; c.stroke();
    c.strokeStyle = col(gold); c.lineWidth = 1.5; c.beginPath(); c.arc(0, 0, 19, 0, Math.PI * 2); c.stroke();
    c.fillStyle = shieldDown ? "rgba(27,20,5,0.45)" : ink;
    c.font = "800 15px " + F_DISPLAY; c.textAlign = "center"; c.textBaseline = "middle";
    c.fillText("99,9 %", 0, 1);
    if (shieldDown) { c.strokeStyle = "rgba(184,64,44,0.85)"; c.lineWidth = 2; c.beginPath(); c.moveTo(-14, -12); c.lineTo(-2, 0); c.lineTo(-8, 6); c.lineTo(12, 14); c.stroke(); }
    c.restore();

    drawCracks(c, b, "rgba(110,50,20,0.7)", 1.8);

    // col de chemise et cou
    c.fillStyle = col(shirt);
    c.beginPath(); c.moveTo(-26, bodyY - 96); c.lineTo(0, bodyY - 82); c.lineTo(-10, bodyY - 70); c.closePath(); c.fill();
    c.beginPath(); c.moveTo(26, bodyY - 96); c.lineTo(0, bodyY - 82); c.lineTo(10, bodyY - 70); c.closePath(); c.fill();

    // tête ballon
    const hx = -6, hy = -96, hr = 48 * breathe;
    const hg = c.createRadialGradient(hx - 18, hy - 18, 6, hx, hy, hr * 1.1);
    hg.addColorStop(0, col(mixv(gold, C.white, 0.5))); hg.addColorStop(0.6, col(gold)); hg.addColorStop(1, col(goldDark));
    c.fillStyle = hg; c.beginPath(); c.arc(hx, hy, hr, 0, Math.PI * 2); c.fill();
    c.fillStyle = "rgba(255,255,255,0.35)"; c.beginPath(); c.ellipse(hx - 22, hy - 24, 7, 13, 0.6, 0, Math.PI * 2); c.fill();
    // coiffure gominée
    c.fillStyle = col(mixv("#141a33", "#3a1424", rt * 0.6));
    c.beginPath(); c.moveTo(hx + 40, hy - 18); c.quadraticCurveTo(hx + 30, hy - 58, hx - 10, hy - 54); c.quadraticCurveTo(hx - 44, hy - 52, hx - 52, hy - 30);
    c.quadraticCurveTo(hx - 26, hy - 44, hx - 4, hy - 36); c.quadraticCurveTo(hx + 22, hy - 34, hx + 40, hy - 18); c.closePath(); c.fill();
    c.fillStyle = "rgba(255,255,255,0.25)"; c.beginPath(); c.ellipse(hx - 10, hy - 48, 14, 3, -0.2, 0, Math.PI * 2); c.fill();

    // visage (tourné vers la gauche)
    const fx = hx - 10;
    c.strokeStyle = ink; c.fillStyle = ink; c.lineCap = "round";
    const angry = rt > 0.3;
    // sourcils
    c.lineWidth = 3.2; c.beginPath();
    if (angry) { c.moveTo(fx - 30, hy - 26); c.lineTo(fx - 12, hy - 20); c.moveTo(fx + 4, hy - 20); c.lineTo(fx + 22, hy - 26); }
    else { c.moveTo(fx - 30, hy - 22); c.quadraticCurveTo(fx - 21, hy - 30, fx - 12, hy - 24); c.moveTo(fx + 4, hy - 26); c.quadraticCurveTo(fx + 13, hy - 32, fx + 22, hy - 26); }
    c.stroke();
    // yeux : un ouvert qui fixe le joueur, un clin d'œil assuré
    const sq = b.squint;
    if (b.stun > 0) {
      c.lineWidth = 2.4; c.beginPath();
      for (const ex of [fx - 21, fx + 13]) { c.moveTo(ex - 5, hy - 15); c.lineTo(ex + 5, hy - 7); c.moveTo(ex + 5, hy - 15); c.lineTo(ex - 5, hy - 7); }
      c.stroke();
    } else {
      c.fillStyle = "#ffffff"; c.beginPath(); c.ellipse(fx - 21, hy - 11, 8, 8 * (1 - sq * 0.8), 0, 0, Math.PI * 2); c.fill();
      c.fillStyle = angry ? "#b8402c" : ink; c.beginPath(); c.arc(fx - 24, hy - 11, 3.6 * (1 - sq * 0.6), 0, Math.PI * 2); c.fill();
      c.lineWidth = 2.8; c.beginPath();
      if (angry) { c.ellipse(fx + 13, hy - 11, 7, 6 * (1 - sq * 0.8), 0, 0, Math.PI * 2); }
      else { c.moveTo(fx + 6, hy - 10); c.quadraticCurveTo(fx + 13, hy - 16, fx + 20, hy - 10); }
      c.stroke();
    }
    // grand sourire commercial
    const open = b.atk >= 0 ? (b.atk < 0.22 ? b.atk / 0.22 : b.atk < 0.34 ? 1 : Math.max(0, 1 - (b.atk - 0.34) / 0.41)) : 0;
    const mY = hy + 10, mW = 46, mH = 16 + open * 12;
    if (b.stun > 0) {
      c.lineWidth = 2.6; c.beginPath(); c.moveTo(fx - 26, mY + 4);
      for (let k = 1; k <= 6; k++) c.lineTo(fx - 26 + k * 7.5, mY + 4 + (k % 2 ? -4 : 4));
      c.stroke();
    } else {
      c.fillStyle = "#3a1414"; c.beginPath(); c.moveTo(fx - mW / 2 - 6, mY); c.quadraticCurveTo(fx - 4, mY - 4, fx + mW / 2, mY - 2); c.quadraticCurveTo(fx + 2, mY + mH * 1.6, fx - mW / 2 - 6, mY); c.closePath(); c.fill();
      c.save(); c.clip();
      c.fillStyle = "#ffffff"; c.fillRect(fx - mW / 2 - 8, mY - 6, mW + 12, 7 + open * 2);
      c.strokeStyle = "rgba(27,20,5,0.25)"; c.lineWidth = 1;
      for (let k = -2; k <= 3; k++) { c.beginPath(); c.moveTo(fx + k * 8 - 4, mY - 6); c.lineTo(fx + k * 8 - 4, mY + 2); c.stroke(); }
      c.restore();
    }
    // joues roses
    c.fillStyle = col(mixv("#ff9a8a", C.rage, rt), 0.35);
    c.beginPath(); c.ellipse(fx - 34, hy + 4, 7, 4, 0, 0, Math.PI * 2); c.ellipse(fx + 26, hy + 4, 6, 4, 0, 0, Math.PI * 2); c.fill();

    // gouttes de sueur quand le bouclier tombe
    c.fillStyle = "rgba(170,215,255,0.85)";
    for (const s of b.own.sweat || []) { const sx = hx + s.x, sy = hy + s.y; c.beginPath(); c.moveTo(sx, sy - 5); c.quadraticCurveTo(sx + 4, sy + 1, sx, sy + 4); c.quadraticCurveTo(sx - 4, sy + 1, sx, sy - 5); c.fill(); }

    // étourdi : étoiles
    if (b.stun > 0) {
      c.fillStyle = col(C.lamp); c.font = "700 14px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle";
      for (let k = 0; k < 3; k++) { const a = b.time * 4 + k * 2.1; c.fillText("★", hx + Math.cos(a) * 40, hy - 62 + Math.sin(a) * 8); }
    }

    // bras avant + contrat brillant (riposte : il armé puis tend le contrat)
    let hand;
    const idle = { x: -132, y: -26 + Math.sin(t * 2) * 5 };
    if (b.atk >= 0) {
      const a = b.atk;
      if (a < 0.22) { const k = a / 0.22; hand = { x: lerp(idle.x, -96, k), y: lerp(idle.y, -96, k) }; }
      else if (a < 0.34) { const k = (a - 0.22) / 0.12; hand = { x: lerp(-96, -176, k), y: lerp(-96, -34, k) }; }
      else { const k = Math.min(1, (a - 0.34) / 0.41); hand = { x: lerp(-176, idle.x, k), y: lerp(-34, idle.y, k) }; }
    } else hand = idle;
    c.strokeStyle = col(suit); c.lineWidth = 22; c.lineCap = "round";
    c.beginPath(); c.moveTo(-64, bodyY - 56); c.quadraticCurveTo((hand.x - 64) / 2 - 10, (hand.y + bodyY - 56) / 2 + 18, hand.x + 10, hand.y + 6); c.stroke();
    c.strokeStyle = col(shirt); c.lineWidth = 8; c.beginPath(); c.moveTo(hand.x + 16, hand.y + 8); c.lineTo(hand.x + 8, hand.y + 4); c.stroke();
    // contrat
    c.save(); c.translate(hand.x - 8, hand.y - 18); c.rotate(-0.22 + (b.atk >= 0 && b.atk > 0.22 && b.atk < 0.4 ? -0.3 : 0));
    c.fillStyle = col(mixv("#fbf7ec", C.white, fl)); rr(c, -24, -32, 48, 62, 4); c.fill();
    c.strokeStyle = col(goldDark, 0.8); c.lineWidth = 1.5; rr(c, -24, -32, 48, 62, 4); c.stroke();
    c.fillStyle = ink; c.font = "800 10px " + F_DISPLAY; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText("SLA 99,9 %", 0, -22);
    c.strokeStyle = "rgba(27,20,5,0.35)"; c.lineWidth = 1;
    for (let k = 0; k < 4; k++) { c.beginPath(); c.moveTo(-17, -10 + k * 7); c.lineTo(17 - (k === 3 ? 12 : 0), -10 + k * 7); c.stroke(); }
    c.fillStyle = "rgba(27,20,5,0.3)"; c.font = "600 4px " + F_MONO; c.fillText("*sauf annexe", 4, 22);
    c.fillStyle = col(mixv("#d8443a", C.white, fl * 0.5)); c.beginPath(); c.arc(-12, 20, 6, 0, Math.PI * 2); c.fill();
    c.fillStyle = "rgba(255,255,255,0.45)"; c.beginPath(); c.moveTo(-24, -32); c.lineTo(-10, -32); c.lineTo(-24, -12); c.closePath(); c.fill();
    c.restore();
    c.fillStyle = col(gold); c.beginPath(); c.arc(hand.x + 4, hand.y + 2, 11, 0, Math.PI * 2); c.fill();
  }
};
