/* Étage 1 — L'Ambigu : un nuage-fantôme fait de consignes floues, une lanterne cachée en son cœur. */
BOSSES[1] = {
  palette: { main: "#b9b2e0", dark: "#2a2850", accent: "#f6d38a", eye: "#e4e0ff", rage: "#ff4f9a" },
  hit: { rx: 130, ry: 92, coreR: 22 },
  top: 122,
  attackFrom: { x: -122, y: -12 },
  castLean: -0.12,
  weakSpot: () => ({ x: 0, y: 22 }),
  critLabel: "ÉCLAIRÉ",
  lines: {
    hit: ["Hé, c’était presque clair…", "Tu précises trop !", "Mes contours s’effacent…"],
    crit: ["Ma lanterne ! Tu vois à travers moi ?", "Trop précis, ça brûle !"],
    wrong: ["Hmm… ça dépend, non ?", "Fais-le bien, c’est tout.", "Personne ne sait ce qu’on veut."],
    timeout: ["Prends ton temps… ou pas.", "Trop lent. C’était flou, de toute façon."],
    rage: "Assez de précision ! Que tout redevienne vague !",
    special: {
      fog: ["Un peu plus de brouillard ?", "Sans contexte, tu vises à l’aveugle.", "Qui a besoin d’exemples ?"],
      fogClear: ["Non… tout devient limpide !", "Arrête de préciser le format !"]
    }
  },
  intro: {
    title: "Brouillard d’instructions",
    text: "L’Ambigu se cache dans un brouillard qui masque son cœur et raccourcit ta visée. Chaque bonne réponse le dissipe, chaque erreur l’épaissit : la clarté rend tes tirs précis."
  },
  mechanics: ["fog"],
  init(b) {
    const rnd = seeded(101);
    const blobs = [];
    for (let i = 0; i < 12; i++) {
      const a = (i / 12) * Math.PI * 2 + rnd() * 0.4, d = 0.45 + rnd() * 0.55;
      blobs.push({ x: Math.cos(a) * 96 * d, y: Math.sin(a) * 58 * d - 4, r: 44 + rnd() * 26, ph: rnd() * 6.28, sp: 0.6 + rnd() * 0.7 });
    }
    b.own.blobs = blobs;
  },
  draw(c, b) {
    const t = b.t, fl = b.flash, rg = b.rageT;
    const churn = 1 + rg * 1.4;
    const base = mixv(mixv("#b9b2e0", C.rage, rg * 0.85), C.white, fl * 0.7);
    const deep = mixv(mixv("#4b4785", "#7a2152", rg), C.white, fl * 0.45);
    const eye = mixv(mixv("#e4e0ff", C.bad, rg), C.white, fl);
    const warm = mixv("#f6d38a", C.white, fl * 0.6);
    const fade = 0.55 + 0.45 * clamp(b.hpFrac, 0, 1);

    // souffle d'attaque : il se contracte, puis crache vers la gauche
    let ox = 0, sx = 1;
    if (b.atk >= 0) {
      const a = b.atk;
      if (a < 0.22) { const k = a / 0.22; ox = 14 * k; sx = 1 - 0.08 * k; }
      else if (a < 0.34) { const k = (a - 0.22) / 0.12; ox = 14 - 42 * k; sx = 0.92 + 0.24 * k; }
      else { const k = Math.min(1, (a - 0.34) / 0.41); ox = -28 * (1 - k); sx = 1.16 - 0.16 * k; }
    }

    const halo = c.createRadialGradient(0, 0, 20, 0, 0, 230);
    halo.addColorStop(0, col(base, 0.16 * fade)); halo.addColorStop(1, col(base, 0));
    c.fillStyle = halo; c.fillRect(-240, -220, 480, 440);

    c.save();
    c.translate(ox, 0); c.scale(sx, 2 - sx);

    // filaments sous le nuage
    c.lineCap = "round";
    for (let k = 0; k < 5; k++) {
      const x0 = -60 + k * 30;
      c.strokeStyle = col(base, 0.22 * fade); c.lineWidth = 12 - k;
      c.beginPath(); c.moveTo(x0, 36);
      for (let s = 1; s <= 4; s++) c.lineTo(x0 + Math.sin(t * 1.6 * churn + k + s) * 10 - s * 3, 36 + s * 18);
      c.stroke();
    }

    // corps : bulles translucides qui dérivent
    for (const bl of b.own.blobs || []) {
      const x = bl.x + Math.sin(t * bl.sp * churn + bl.ph) * 9;
      const y = bl.y + Math.cos(t * bl.sp * 0.8 * churn + bl.ph) * 7;
      const r = bl.r * (1 + 0.06 * Math.sin(t * 1.3 + bl.ph));
      const g = c.createRadialGradient(x, y, r * 0.15, x, y, r);
      g.addColorStop(0, col(base, 0.42 * fade)); g.addColorStop(0.6, col(base, 0.2 * fade)); g.addColorStop(1, col(base, 0));
      c.fillStyle = g; c.beginPath(); c.arc(x, y, r, 0, Math.PI * 2); c.fill();
    }
    const core = c.createRadialGradient(0, 0, 10, 0, 0, 92);
    core.addColorStop(0, col(deep, 0.75 * fade)); core.addColorStop(1, col(deep, 0));
    c.fillStyle = core; c.beginPath(); c.ellipse(0, 0, 112, 78, 0, 0, Math.PI * 2); c.fill();

    // boucle en point d'interrogation, en double exposition
    for (let e = 0; e < 2; e++) {
      const dx = e ? Math.sin(t * 1.9) * 4 : -Math.cos(t * 1.4) * 3, dy = e ? -2 : 2;
      c.save(); c.translate(dx, dy);
      c.strokeStyle = col(base, 0.5 * fade); c.lineWidth = 11;
      c.beginPath(); c.arc(86, -74, 20, Math.PI * 0.95, Math.PI * 0.45, false); c.lineTo(86, -38); c.stroke();
      c.fillStyle = col(base, 0.5 * fade); c.beginPath(); c.arc(86, -22, 6.5, 0, Math.PI * 2); c.fill();
      c.restore();
    }

    // lanterne (point faible)
    c.save(); c.translate(0, 8);
    const flick = 0.85 + 0.15 * Math.sin(t * 9) + 0.08 * Math.sin(t * 23);
    const lg = c.createRadialGradient(0, 16, 2, 0, 16, 40 * flick);
    lg.addColorStop(0, col(warm, 0.9)); lg.addColorStop(0.4, col(warm, 0.35)); lg.addColorStop(1, col(warm, 0));
    c.fillStyle = lg; c.beginPath(); c.arc(0, 16, 40 * flick, 0, Math.PI * 2); c.fill();
    c.strokeStyle = col(mixv("#8a84b8", C.white, fl)); c.lineWidth = 2.2;
    c.beginPath(); c.arc(0, -4, 8, Math.PI, 0); c.stroke();
    c.fillStyle = col(mixv("#5d5890", C.white, fl)); c.fillRect(-11, -4, 22, 5); c.fillRect(-9, 28, 18, 4);
    rr(c, -9, 1, 18, 27, 4); c.fillStyle = col(warm, 0.55); c.fill();
    c.strokeStyle = col(mixv("#8a84b8", C.white, fl), 0.9); c.lineWidth = 1.5; c.stroke();
    c.fillStyle = col(mixv("#fff6dc", C.white, fl), 0.95);
    c.beginPath(); c.moveTo(0, 6 - 3 * flick); c.quadraticCurveTo(5, 16, 0, 22); c.quadraticCurveTo(-5, 16, 0, 6 - 3 * flick); c.fill();
    c.restore();

    // visage : yeux en double exposition qui ne s'alignent jamais
    c.save(); c.globalAlpha = b.stun > 0 ? 0.4 : 1;
    const sq = 1 - b.squint * 0.8;
    const exposures = [
      { dx: Math.sin(t * 1.7 * churn) * 5, dy: Math.cos(t * 1.3) * 3 },
      { dx: -Math.sin(t * 1.1 + 1) * 6, dy: Math.sin(t * 2.1) * 4 }
    ];
    for (const ex of exposures) {
      c.fillStyle = col(eye, 0.55);
      c.beginPath(); c.ellipse(-36 + ex.dx, -36 + ex.dy, 9, 13 * sq, -0.15, 0, Math.PI * 2); c.fill();
      c.beginPath(); c.ellipse(20 + ex.dx, -38 + ex.dy, 9, 13 * sq, 0.15, 0, Math.PI * 2); c.fill();
      c.fillStyle = col(deep, 0.6);
      c.beginPath(); c.arc(-39 + ex.dx * 1.4, -35 + ex.dy, 3.2 * sq, 0, Math.PI * 2); c.moveTo(17 + ex.dx * 1.4 + 3.2 * sq, -37 + ex.dy); c.arc(17 + ex.dx * 1.4, -37 + ex.dy, 3.2 * sq, 0, Math.PI * 2); c.fill();
    }
    // bouche : un tilde hésitant, qui s'ouvre en O pour souffler
    const open = b.atk >= 0.22 && b.atk < 0.6 ? 1 : b.atk >= 0 && b.atk < 0.22 ? b.atk / 0.22 * 0.4 : 0;
    c.strokeStyle = col(eye, 0.75); c.lineWidth = 2.6;
    if (open > 0.05) {
      c.beginPath(); c.ellipse(-14, -12, 7 + 5 * open, 4 + 7 * open, 0, 0, Math.PI * 2); c.stroke();
    } else {
      c.beginPath(); c.moveTo(-32, -14);
      for (let x = -32; x <= 4; x += 3) c.lineTo(x, -14 + Math.sin(x * 0.28 + t * 4) * 3);
      c.stroke();
    }
    c.restore();

    drawCracks(c, b, col(mixv(base, C.white, 0.5), 0.55), 2);

    // points d'interrogation qui jaillissent pendant une action spéciale
    if (b.cast >= 0) {
      const k = clamp(b.cast / 0.9, 0, 1);
      c.font = "800 24px " + F_DISPLAY; c.textAlign = "center"; c.textBaseline = "middle";
      for (let q = 0; q < 6; q++) {
        const a = q * 1.05 + 0.3, r = 50 + k * 140;
        c.fillStyle = col(base, 0.9 * (1 - k));
        c.fillText("?", Math.cos(a) * r, Math.sin(a) * r * 0.7);
      }
    }
    c.restore();

    // mots flous en orbite
    c.font = "600 15px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle";
    const gl = ["?", "…", "etc.", "TBD", "~", "bien", "vite"];
    for (let k = 0; k < gl.length; k++) {
      const a = t * 0.5 * churn + (k * Math.PI * 2) / gl.length, depth = Math.sin(a);
      c.fillStyle = col(base, (0.2 + 0.32 * (depth + 1) / 2) * fade);
      c.fillText(gl[k], Math.cos(a) * 190, depth * 100);
    }
  }
};
