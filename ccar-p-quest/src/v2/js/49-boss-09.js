/* Étage 9 — Le Chaos Ops : une baie de serveurs en panique, gyrophare allumé et câbles en bataille. */
BOSSES[9] = {
  palette: { main: "#ef4b4b", dark: "#2a3350", accent: "#f3b841", eye: "#f3b841", rage: "#ff2d55" },
  hit: { rx: 96, ry: 148, coreR: 22 },
  top: 176,
  attackFrom: { x: -150, y: 10 },
  castLean: -0.14,
  weakSpot: () => ({ x: 0, y: 44 }),
  critLabel: "HEALTH CHECK",
  lines: {
    hit: ["Qui a touché à la prod ?!", "Ma config locale !", "Un rollback, vite !"],
    crit: ["Mon health check !", "Tout est rouge !"],
    wrong: ["Copie ça depuis le wiki, ça marchera.", "Encore un réglage à la main !", "Chez moi, ça marche."],
    timeout: ["Incident ouvert, personne d’astreinte.", "Trop tard, le pager sonne."],
    rage: "Alerte générale ! Tout le monde en prod !",
    special: {
      incident: ["Nouvel incident ! Personne n’a de procédure ?", "Le pager hurle, à toi de jouer !", "Encore une alerte non triée !"],
      hook: ["Un hook ?! Mes incidents rebondissent…", "Un contrôle déterministe… c’est déloyal !"]
    }
  },
  intro: {
    title: "Incidents en rafale",
    text: "Il lance des incidents qui foncent vers toi : touche-les pour les acquitter, sinon sa barre d’attaque avance. Installe un hook pour les bloquer tous : un contrôle déterministe vaut mieux que l’urgence permanente."
  },
  mechanics: ["incidents"],
  init(b) {
    const o = b.own;
    const r = seeded(9);
    o.leds = [];
    for (let row = 0; row < 7; row++) for (let k = 0; k < 4; k++) o.leds.push({ x: -48 + k * 11, y: -38 + row * 18 + (row > 2 ? 34 : 0), p: r() * 6, s: 1.5 + r() * 5, hue: r() });
    o.smoke = []; o.smokeT = 0;
  },
  update(b, dt) {
    const o = b.own;
    o.smokeT -= dt;
    const rate = b.rage ? 0.12 : 0.35 + 0.5 * b.hpFrac;
    if (o.smokeT <= 0) { o.smokeT = rate; o.smoke.push({ x: rand(38, 58), y: -122, r: rand(6, 11), vx: rand(4, 18), vy: rand(-36, -22), life: 0, max: rand(1.4, 2.4) }); }
    for (const s of o.smoke) { s.life += dt; s.x += s.vx * dt; s.y += s.vy * dt; s.r += 9 * dt; }
    o.smoke = o.smoke.filter((s) => s.life < s.max);
  },
  draw(c, b) {
    const fl = b.flash, rt = b.rageT, t = b.t, o = b.own;
    const metal = mixv(mixv("#2b3456", "#3d1f2c", rt * 0.55), C.white, fl * 0.6);
    const metalLight = mixv(mixv("#4b5680", "#6a2f40", rt * 0.55), C.white, fl * 0.6);
    const red = mixv(mixv("#ef4b4b", "#ff2d55", rt), C.white, fl * 0.4);
    const amber = mixv("#f3b841", C.white, fl * 0.4);
    const beaconSpeed = b.rage ? 9 : 4;
    const beacon = (Math.sin(b.time * beaconSpeed) + 1) / 2;

    // halo rouge qui pulse avec le gyrophare
    const ag = c.createRadialGradient(0, -20, 30, 0, -20, 250);
    ag.addColorStop(0, col(red, 0.12 + 0.12 * beacon)); ag.addColorStop(1, col(red, 0));
    c.fillStyle = ag; c.fillRect(-250, -260, 500, 500);

    // fumée
    for (const s of o.smoke || []) { const a = 1 - s.life / s.max; c.fillStyle = "rgba(150,160,185," + (0.35 * a) + ")"; c.beginPath(); c.arc(s.x, s.y, s.r, 0, Math.PI * 2); c.fill(); }

    // câbles-tentacules (arrière)
    c.lineCap = "round";
    const cables = [
      { sx: 70, sy: -70, ex: 150, ey: -110, cl: "#3d7bd9", ph: 0 },
      { sx: 72, sy: 10, ex: 165, ey: 30, cl: "#e0b13a", ph: 1.4 },
      { sx: 66, sy: 80, ex: 140, ey: 140, cl: "#57c48f", ph: 2.6 },
      { sx: -66, sy: 86, ex: -130, ey: 150, cl: "#b06ad9", ph: 3.3 }
    ];
    const wig = b.rage ? 2.2 : 1;
    for (const k of cables) {
      const w1 = Math.sin(t * 2.4 * wig + k.ph) * 22, w2 = Math.cos(t * 1.9 * wig + k.ph) * 18;
      c.strokeStyle = col(mixv(k.cl, C.white, fl * 0.5)); c.lineWidth = 7;
      c.beginPath(); c.moveTo(k.sx, k.sy);
      c.bezierCurveTo(k.sx + (k.ex - k.sx) * 0.4, k.sy + w1, k.sx + (k.ex - k.sx) * 0.7, k.ey + w2, k.ex + w2 * 0.4, k.ey + w1 * 0.4);
      c.stroke();
      c.fillStyle = "#c9d1e4"; c.save(); c.translate(k.ex + w2 * 0.4, k.ey + w1 * 0.4); c.rotate(Math.atan2(k.ey - k.sy, k.ex - k.sx)); rr(c, -2, -6, 14, 12, 2); c.fill(); c.fillStyle = "#7d879f"; c.fillRect(12, -4, 5, 2); c.fillRect(12, 2, 5, 2); c.restore();
    }

    // roulettes
    c.fillStyle = "#11172a";
    for (const x of [-48, 48]) { c.fillRect(x - 3, 112, 6, 10); c.beginPath(); c.arc(x, 126, 9, 0, Math.PI * 2); c.fill(); c.strokeStyle = "#4b5680"; c.lineWidth = 2; c.stroke(); }

    // baie
    const rg = c.createLinearGradient(-72, 0, 72, 0);
    rg.addColorStop(0, col(metalLight)); rg.addColorStop(0.18, col(metal)); rg.addColorStop(0.82, col(metal)); rg.addColorStop(1, col(mixv(metal, "#000000", 0.3)));
    c.fillStyle = rg; rr(c, -72, -126, 144, 240, 10); c.fill();
    c.strokeStyle = col(metalLight); c.lineWidth = 2; rr(c, -72, -126, 144, 240, 10); c.stroke();
    // rails et vis
    c.fillStyle = col(mixv(metal, "#000000", 0.25)); c.fillRect(-66, -40, 6, 148); c.fillRect(60, -40, 6, 148);
    c.fillStyle = col(metalLight);
    for (let y = -34; y < 110; y += 18) { c.beginPath(); c.arc(-63, y, 1.6, 0, Math.PI * 2); c.arc(63, y, 1.6, 0, Math.PI * 2); c.fill(); }
    // unités de rack
    for (let row = 0; row < 7; row++) {
      const y = -46 + row * 18 + (row > 2 ? 34 : 0);
      c.fillStyle = col(mixv(metal, "#000000", 0.35)); rr(c, -56, y, 112, 15, 3); c.fill();
      c.strokeStyle = "rgba(255,255,255,0.07)"; c.lineWidth = 1;
      for (let vx = 8; vx < 50; vx += 5) { c.beginPath(); c.moveTo(vx, y + 3); c.lineTo(vx, y + 12); c.stroke(); }
    }
    // LEDs
    for (const led of o.leds || []) {
      const on = Math.sin(b.time * led.s + led.p) > (b.rage ? -0.3 : 0.1);
      const hue = b.rage ? (led.hue < 0.75 ? "#ff2d55" : "#f3b841") : (led.hue < 0.55 ? "#57c48f" : led.hue < 0.85 ? "#f3b841" : "#ef4b4b");
      c.fillStyle = on ? hue : "rgba(255,255,255,0.08)";
      c.beginPath(); c.arc(led.x, led.y + 7.5, 2.4, 0, Math.PI * 2); c.fill();
    }

    // panneau d'état (point faible)
    const ws = { x: 0, y: 44 };
    c.fillStyle = "#0b1220"; rr(c, -46, ws.y - 18, 92, 36, 6); c.fill();
    c.strokeStyle = col(metalLight); c.lineWidth = 1.5; rr(c, -46, ws.y - 18, 92, 36, 6); c.stroke();
    const health = clamp(b.hpFrac, 0, 1);
    const hcol = health > 0.6 ? "#57c48f" : health > 0.3 ? "#f3b841" : "#ef4b4b";
    c.strokeStyle = col(hcol, 0.9); c.lineWidth = 1.6; c.beginPath();
    for (let x = -42; x <= 42; x += 2) {
      if (Math.abs(x) < 16) continue;
      const ph = (x + b.time * 60) % 40;
      const y = ph > 18 && ph < 22 ? -9 : ph > 22 && ph < 25 ? 7 : 0;
      if (x === -42 || x === 16) c.moveTo(x, ws.y + y); else c.lineTo(x, ws.y + y);
    }
    c.stroke();
    const pulse = 1 + Math.sin(b.time * (b.rage ? 10 : 5)) * 0.12;
    c.save(); c.shadowColor = hcol; c.shadowBlur = 14;
    const lg = c.createRadialGradient(ws.x - 3, ws.y - 3, 1, ws.x, ws.y, 13 * pulse);
    lg.addColorStop(0, "#ffffff"); lg.addColorStop(0.45, hcol); lg.addColorStop(1, col(hcol, 0.2));
    c.fillStyle = lg; c.beginPath(); c.arc(ws.x, ws.y, 13 * pulse, 0, Math.PI * 2); c.fill();
    c.restore();
    c.fillStyle = "rgba(232,236,246,0.75)"; c.font = "600 7px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle";
    c.fillText("HEALTH", ws.x, ws.y + 26);

    // écran-visage
    c.fillStyle = "#0b1220"; rr(c, -58, -116, 116, 62, 7); c.fill();
    c.strokeStyle = col(metalLight); c.lineWidth = 2; rr(c, -58, -116, 116, 62, 7); c.stroke();
    const scr = b.rage ? mixv("#ff2d55", C.white, fl) : mixv("#f3b841", C.white, fl);
    c.save(); c.globalAlpha = b.stun > 0 ? 0.45 : 1;
    c.fillStyle = col(scr);
    const ex = -8; // regard vers la gauche
    if (b.stun > 0) {
      c.font = "700 18px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText("x  x", ex, -94);
    } else {
      const sq = 1 - b.squint * 0.75;
      for (const s of [-1, 1]) {
        const cx = ex + s * 22;
        c.beginPath(); c.moveTo(cx - 12, -100 + (s < 0 ? -4 : 4) * 1); c.lineTo(cx + 12, -100 + (s < 0 ? 4 : -4)); c.lineTo(cx + 12, -100 + (s < 0 ? 4 : -4) + 9 * sq); c.lineTo(cx - 12, -100 + (s < 0 ? -4 : 4) + 9 * sq); c.closePath(); c.fill();
      }
    }
    // bouche pixel
    const open = b.atk >= 0 ? (b.atk < 0.22 ? b.atk / 0.22 : b.atk < 0.34 ? 1 : Math.max(0, 1 - (b.atk - 0.34) / 0.41)) : 0;
    if (open > 0.05) { c.fillRect(ex - 16, -78, 32, 4 + open * 10); }
    else { c.fillRect(ex - 18, -74, 6, 3); c.fillRect(ex - 12, -77, 6, 3); c.fillRect(ex - 6, -74, 6, 3); c.fillRect(ex, -77, 6, 3); c.fillRect(ex + 6, -74, 6, 3); c.fillRect(ex + 12, -77, 6, 3); }
    c.restore();
    c.fillStyle = "rgba(255,255,255,0.05)";
    for (let y = -114; y < -56; y += 3) c.fillRect(-56, y, 112, 1);

    drawCracks(c, b, "rgba(255,210,190,0.7)", 1.6);

    // gyrophare
    c.save(); c.translate(0, -140);
    const ang = b.time * beaconSpeed;
    for (const s of [0, Math.PI]) {
      const a = ang + s;
      const gr = c.createRadialGradient(0, 0, 4, 0, 0, 150);
      gr.addColorStop(0, col(red, 0.4)); gr.addColorStop(1, col(red, 0));
      c.fillStyle = gr; c.beginPath(); c.moveTo(0, 0); c.arc(0, 0, 150, a - 0.22, a + 0.22); c.closePath(); c.fill();
    }
    c.fillStyle = "#1a2033"; rr(c, -20, 2, 40, 12, 3); c.fill();
    c.fillStyle = col(mixv(red, C.white, beacon * 0.4)); c.beginPath(); c.arc(0, 2, 17, Math.PI, 0); c.closePath(); c.fill();
    c.fillStyle = "rgba(255,255,255,0.45)"; c.beginPath(); c.ellipse(-6, -6, 4, 7, 0.4, 0, Math.PI * 2); c.fill();
    c.restore();

    // tentacule avant avec le pager (riposte : il recule puis fouette)
    let tip;
    const idle = { x: -150, y: 10 + Math.sin(t * 2.6) * 8 };
    if (b.atk >= 0) {
      const a = b.atk;
      if (a < 0.22) { const k = a / 0.22; tip = { x: lerp(idle.x, -104, k), y: lerp(idle.y, -76, k) }; }
      else if (a < 0.34) { const k = (a - 0.22) / 0.12; tip = { x: lerp(-104, -190, k), y: lerp(-76, -6, k) }; }
      else { const k = Math.min(1, (a - 0.34) / 0.41); tip = { x: lerp(-190, idle.x, k), y: lerp(-6, idle.y, k) }; }
    } else tip = idle;
    c.strokeStyle = col(mixv("#d9534f", C.white, fl * 0.5)); c.lineWidth = 8;
    c.beginPath(); c.moveTo(-68, -10);
    c.bezierCurveTo(-96, -40 + Math.sin(t * 3) * 10, (tip.x - 68) / 2 - 20, tip.y + 30, tip.x + 14, tip.y);
    c.stroke();
    c.save(); c.translate(tip.x, tip.y); c.rotate(Math.sin(t * 9) * (b.atk >= 0 ? 0.25 : 0.08));
    c.fillStyle = "#1a2033"; rr(c, -18, -13, 36, 26, 5); c.fill();
    c.strokeStyle = "#4b5680"; c.lineWidth = 1.5; rr(c, -18, -13, 36, 26, 5); c.stroke();
    const blink = Math.sin(b.time * 12) > 0;
    c.fillStyle = blink ? col(amber) : "#3a2a12"; rr(c, -13, -8, 26, 12, 2); c.fill();
    c.fillStyle = "#0b1220"; c.font = "800 10px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText("!", 0, -2);
    c.fillStyle = "#4b5680"; c.fillRect(-10, 7, 6, 3); c.fillRect(4, 7, 6, 3);
    c.restore();
  }
};
