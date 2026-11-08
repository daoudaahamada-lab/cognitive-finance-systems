/* Étage 6 — Le Gouffre à Tokens : un vortex vorace bordé d'un anneau de tokens qui tombent dans sa gueule.
   Sa cible critique est l'œil de la singularité, au fond de la gueule. Moins il a de vie, moins il reste de tokens à avaler. */
BOSSES[6] = {
  palette: { main: "#9b6bff", dark: "#140f2a", accent: "#f3b841", eye: "#f3b841", rage: "#ff4f6d" },
  hit: { rx: 112, ry: 104, coreR: 22 },
  top: 118,
  attackFrom: { x: -30, y: 8 },
  castLean: 0,
  critLabel: "SINGULARITÉ",
  lines: {
    hit: ["Ma facture… elle baisse ?!", "Hé ! Je n’ai rien avalé !", "Tu as réduit mes sorties ?"],
    crit: ["En plein dans la singularité !", "Ma gueule ! Mon budget !"],
    wrong: ["Miam, 80 000 tokens de plus.", "Pas de cache ? Délicieux.", "Renvoie tout le contexte, encore !"],
    timeout: ["Le temps aussi, je l’avale.", "Chaque seconde te coûte."],
    rage: "J’ai faim ! Envoie-moi tout, sans cache !",
    special: {
      cache: ["Un cache hit ?! Je n’ai rien eu à manger !", "Préfixe en cache… je meurs de faim.", "Trop rapide, trop économique !"]
    }
  },
  intro: {
    title: "Cache hit",
    text: "Il aspire ton temps : sa barre d’attaque se remplit plus vite qu’ailleurs. Une bonne réponse dans les premiers 40 % de la barre est un « cache hit » qui frappe deux fois plus fort."
  },
  mechanics: ["tokens"],

  weakSpot: () => ({ x: 0, y: 8 }),
  atkK(b) {
    if (b.atk < 0) return 0;
    const a = b.atk;
    return a < 0.22 ? a / 0.22 : a < 0.34 ? 1 - ((a - 0.22) / 0.12) * 2 : -(1 - Math.min(1, (a - 0.34) / 0.41));
  },
  init(b) {
    const glyphs = ["T", "¤", "$", "1k", "T", "¤"];
    b.own.tokens = [];
    for (let i = 0; i < 24; i++) b.own.tokens.push({ a: rand(0, Math.PI * 2), r: rand(40, 165), s: rand(0.5, 1.2), sz: rand(7, 12), g: glyphs[i % glyphs.length] });
    b.own.spin = 0;
  },
  update(b, dt) {
    const sp = (b.rage ? 1.8 : 1) * (b.cast >= 0 ? 2.6 : 1) * (b.stun > 0 ? 0.3 : 1) * (b.atk >= 0 ? 1.6 : 1);
    b.own.spin += dt * 0.9 * sp;
    for (const tk of b.own.tokens) {
      tk.a += dt * sp * (0.6 + 40 / tk.r);
      tk.r -= dt * sp * 14 * tk.s;
      if (tk.r < 28) { tk.r = rand(140, 168); tk.a = rand(0, Math.PI * 2); }
    }
  },

  draw(c, b) {
    const B = BOSSES[6], P = B.palette, fl = b.flash, rage = b.rageT, t = b.time;
    const main = mixv(mixv(P.main, P.rage, rage), C.white, fl * 0.6);
    const gold = mixv(P.accent, C.white, fl * 0.6);
    const eye = mixv(mixv(P.eye, C.bad, rage), C.white, fl);
    const k = B.atkK(b), castK = b.cast >= 0 ? Math.sin(Math.min(1, b.cast / 0.9) * Math.PI) : 0;
    const cy = 8, scale = 1 + (k > 0 ? -0.08 * k : 0.07 * -k) + castK * 0.04;
    const toks = b.own.tokens || [];
    const visible = Math.ceil(toks.length * (0.35 + 0.65 * clamp(b.hpFrac, 0, 1)));

    // halo
    const ag = c.createRadialGradient(0, cy, 30, 0, cy, 240); ag.addColorStop(0, col(main, 0.25)); ag.addColorStop(1, col(main, 0));
    c.fillStyle = ag; c.fillRect(-250, -230, 500, 470);

    const drawToken = (tk, front) => {
      const x = Math.cos(tk.a) * tk.r, y = cy + Math.sin(tk.a) * tk.r * 0.36;
      if ((Math.sin(tk.a) >= 0) !== front) return;
      const sz = tk.sz * (0.45 + 0.55 * clamp(tk.r / 160, 0, 1)) * (1 + castK * 0.3);
      c.save(); c.translate(x, y); c.rotate(tk.a * 2);
      c.fillStyle = col(gold, front ? 0.95 : 0.55); rr(c, -sz / 2, -sz / 2, sz, sz, 2); c.fill();
      c.strokeStyle = col(mixv(P.dark, C.white, fl), 0.6); c.lineWidth = 1; c.stroke();
      if (sz > 8) { c.rotate(-tk.a * 2); c.fillStyle = col(P.dark, 0.85); c.font = "700 " + Math.round(sz * 0.7) + "px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText(tk.g, 0, 0.5); }
      c.restore();
    };
    // anneau d'accrétion (arrière)
    c.strokeStyle = col(gold, 0.25); c.lineWidth = 2; c.beginPath(); c.ellipse(0, cy, 158, 57, 0, Math.PI, Math.PI * 2); c.stroke();
    for (let i = 0; i < visible; i++) drawToken(toks[i], false);

    c.save(); c.translate(0, cy); c.scale(scale, scale);
    // disque du vortex
    const dg = c.createRadialGradient(0, 0, 8, 0, 0, 102);
    dg.addColorStop(0, col(mixv(gold, C.white, 0.4))); dg.addColorStop(0.25, col(main, 0.95)); dg.addColorStop(0.75, col(mixv(main, P.dark, 0.55))); dg.addColorStop(1, col(mixv(P.dark, C.white, fl * 0.4)));
    c.fillStyle = dg; c.beginPath(); c.arc(0, 0, 100, 0, Math.PI * 2); c.fill();
    // bras de la spirale
    c.lineCap = "round";
    for (let arm = 0; arm < 5; arm++) {
      c.beginPath();
      for (let r = 20; r <= 98; r += 4) {
        const a = -b.own.spin * 1.4 + (arm * Math.PI * 2) / 5 + r * 0.045;
        const x = Math.cos(a) * r, y = Math.sin(a) * r;
        if (r === 20) c.moveTo(x, y); else c.lineTo(x, y);
      }
      c.strokeStyle = col(mixv(main, C.white, 0.35), 0.45); c.lineWidth = 5; c.stroke();
      c.strokeStyle = col(gold, 0.25); c.lineWidth = 1.5; c.stroke();
    }
    c.strokeStyle = col(gold, 0.55); c.lineWidth = 2.5; c.beginPath(); c.arc(0, 0, 100, 0, Math.PI * 2); c.stroke();
    c.restore();

    drawCracks(c, b, "rgba(255,232,190,0.85)", 1.8);

    // yeux au-dessus de la gueule
    c.save(); c.globalAlpha = b.stun > 0 ? 0.45 : 1;
    for (const [ex, tilt] of [[-36, 0.34], [36, -0.34]]) {
      c.save(); c.translate(ex, -44 * scale); c.rotate(tilt);
      const eh = 10 * (1 - b.squint * 0.75) + (k > 0 ? k * 3 : 0);
      c.beginPath(); c.moveTo(-18, 0); c.quadraticCurveTo(0, -eh * 1.5, 18, 0); c.quadraticCurveTo(0, eh, -18, 0); c.closePath();
      c.shadowColor = col(eye); c.shadowBlur = 12; c.fillStyle = col(eye); c.fill(); c.shadowBlur = 0;
      c.fillStyle = "#05030c"; c.beginPath(); c.ellipse(-5, -2, 2.4, Math.max(1, eh * 0.7), 0, 0, Math.PI * 2); c.fill();
      c.strokeStyle = col(mixv(P.dark, C.white, fl * 0.5)); c.lineWidth = 5; c.lineCap = "round";
      c.beginPath(); c.moveTo(-20, -eh * 1.2 - 6); c.lineTo(18, -eh * 0.5 - 8); c.stroke();
      c.restore();
    }
    c.restore();

    // gueule dentée et œil de la singularité
    const mawR = 34 + (k < 0 ? -k * 12 : 0) + castK * 4;
    c.save(); c.translate(0, cy);
    c.fillStyle = "#05030c"; c.beginPath(); c.arc(0, 0, mawR, 0, Math.PI * 2); c.fill();
    c.strokeStyle = col(main, 0.9); c.lineWidth = 3; c.stroke();
    const teeth = 12, retract = k < 0 ? -k * 0.6 : 0;
    c.fillStyle = col(mixv("#f2ead7", C.white, fl));
    for (let i = 0; i < teeth; i++) {
      const a = (i / teeth) * Math.PI * 2 + b.own.spin * 0.3, a1 = a - 0.16, a2 = a + 0.16, tip = mawR - 13 * (1 - retract);
      c.beginPath(); c.moveTo(Math.cos(a1) * mawR, Math.sin(a1) * mawR); c.lineTo(Math.cos(a) * tip, Math.sin(a) * tip); c.lineTo(Math.cos(a2) * mawR, Math.sin(a2) * mawR); c.closePath(); c.fill();
    }
    const pulse = 1 + Math.sin(t * 5) * 0.1;
    const eg = c.createRadialGradient(0, 0, 1, 0, 0, 18 * pulse); eg.addColorStop(0, "rgba(255,255,255,0.98)"); eg.addColorStop(0.45, col(eye, 0.95)); eg.addColorStop(1, col(eye, 0));
    c.fillStyle = eg; c.beginPath(); c.arc(0, 0, 18 * pulse, 0, Math.PI * 2); c.fill();
    c.fillStyle = "#05030c"; c.beginPath(); c.ellipse(-3, 0, 2.6 * (1 - b.squint * 0.6), 9, 0, 0, Math.PI * 2); c.fill();
    c.restore();

    // anneau d'accrétion (avant)
    c.strokeStyle = col(gold, 0.45); c.lineWidth = 2; c.beginPath(); c.ellipse(0, cy, 158, 57, 0, 0, Math.PI); c.stroke();
    for (let i = 0; i < visible; i++) drawToken(toks[i], true);

    // étourdi : étoiles qui tournent au-dessus
    if (b.stun > 0) {
      c.fillStyle = col(C.lamp, 0.95);
      for (let j = 0; j < 3; j++) {
        const a = t * 4 + (j * Math.PI * 2) / 3, x = Math.cos(a) * 36, y = -104 + Math.sin(a) * 8;
        c.beginPath(); for (let q = 0; q < 8; q++) { const aa = (q * Math.PI) / 4, r = q % 2 ? 2 : 6; c.lineTo(x + Math.cos(aa) * r, y + Math.sin(aa) * r); } c.closePath(); c.fill();
      }
    }
  }
};
