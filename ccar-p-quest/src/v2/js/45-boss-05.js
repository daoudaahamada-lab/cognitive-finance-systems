/* Étage 5 — Le Vibe-Checker : une boule à facettes suffisante, lunettes noires et casque sur les oreilles.
   Sa cible critique est la petite jauge de métrique qui tremble sur son visage : la vraie mesure qu'il refuse de regarder. */
BOSSES[5] = {
  palette: { main: "#ff9ad5", dark: "#2a1d3a", accent: "#7fe3ff", eye: "#ff9ad5", rage: "#ff5a36" },
  hit: { rx: 105, ry: 105, coreR: 18 },
  top: 128,
  attackFrom: { x: -92, y: 60 },
  castLean: 0.1,
  critLabel: "MESURÉ !",
  lines: {
    hit: ["Hé, ça avait l’air bien pourtant.", "Mes vibes… ébranlées.", "Tu as… une rubrique ?"],
    crit: ["Une métrique ?! Pile dedans !", "Ma jauge ! Ne la regarde pas !"],
    wrong: ["Tu vois ? Au feeling, ça passe.", "Trois réponses lues, ça me suffit.", "Ça sent bon, je valide."],
    timeout: ["Je sens que t’as perdu.", "Pas besoin d’attendre les chiffres."],
    rage: "Mes vibes sont formelles : tu vas tomber !",
    special: {
      shuffle: ["Je mélange tout, l’ordre c’est une vibe.", "Tiens, relis tout ça au feeling.", "La position A, c’était une impression."]
    }
  },
  intro: {
    title: "Pierres mélangées",
    text: "Il mélange tes pierres toutes les 25 secondes et après chaque tir raté : les lettres changent, seule la réponse compte. Sa jauge de métrique tremble sur son visage, vise-la pour un critique."
  },
  mechanics: ["shuffle"],

  weakSpot(b) {
    const r = b.rage ? 1.6 : 1, a = b.rage ? 1.25 : 1, t = b.t;
    return {
      x: (Math.sin(t * 2.3 * r) * 34 + Math.sin(t * 5.7 * r + 1) * 16) * a - 8,
      y: (Math.sin(t * 1.9 * r + 2) * 26 + Math.cos(t * 6.1 * r) * 10) * a + 6
    };
  },
  /* -1 → 1 : recul à l'armement, puis détente vers la gauche, puis retour. */
  atkK(b) {
    if (b.atk < 0) return 0;
    const a = b.atk;
    return a < 0.22 ? a / 0.22 : a < 0.34 ? 1 - ((a - 0.22) / 0.12) * 2 : -(1 - Math.min(1, (a - 0.34) / 0.41));
  },
  init(b) {
    b.own.sparkles = [];
    for (let i = 0; i < 7; i++) b.own.sparkles.push({ a: (i / 7) * Math.PI * 2, r: rand(112, 138), s: rand(4, 8), ph: rand(0, 6) });
    b.own.spin = 0;
  },
  update(b, dt) {
    const sp = (b.rage ? 2.2 : 1) * (b.cast >= 0 ? 7 : 1) * (b.stun > 0 ? 0.3 : 1);
    b.own.spin = (b.own.spin + dt * 16 * sp) % 1000;
    for (const s of b.own.sparkles) s.a += dt * 0.5 * (b.rage ? 1.8 : 1);
  },

  draw(c, b) {
    const B = BOSSES[5], P = B.palette, fl = b.flash, rage = b.rageT, t = b.time;
    const tint = mixv(mixv(P.main, P.rage, rage), C.white, fl * 0.6);
    const tint2 = mixv(mixv(P.accent, P.rage, rage * 0.6), C.white, fl * 0.6);
    const k = B.atkK(b), castK = b.cast >= 0 ? Math.sin(Math.min(1, b.cast / 0.9) * Math.PI) : 0;
    const bob = Math.sin(b.t * 1.4) * 4;
    c.save(); c.translate(0, bob);

    // halo
    const ag = c.createRadialGradient(0, 0, 30, 0, 0, 230); ag.addColorStop(0, col(tint, 0.22)); ag.addColorStop(0.6, col(tint2, 0.06)); ag.addColorStop(1, col(tint2, 0));
    c.fillStyle = ag; c.fillRect(-240, -230, 480, 460);

    // étincelles en orbite
    for (const s of b.own.sparkles || []) {
      const rr2 = s.r + castK * 40, tw = 0.5 + 0.5 * Math.abs(Math.sin(t * 3 + s.ph));
      B.sparkle(c, Math.cos(s.a) * rr2, Math.sin(s.a) * rr2 * 0.8, s.s * (0.6 + tw * 0.6), col(b.rage ? P.rage : (s.ph > 3 ? P.accent : P.main), 0.5 + tw * 0.5));
    }

    // arceau du casque
    c.lineCap = "round"; c.strokeStyle = col(mixv("#2a2f48", C.white, fl * 0.5)); c.lineWidth = 11;
    c.beginPath(); c.arc(0, -6, 96, Math.PI * 1.08, Math.PI * 1.92); c.stroke();
    c.strokeStyle = col(tint, 0.6); c.lineWidth = 3;
    c.beginPath(); c.arc(0, -6, 96, Math.PI * 1.12, Math.PI * 1.88); c.stroke();

    // boule à facettes
    c.save();
    c.beginPath(); c.arc(0, 0, 86, 0, Math.PI * 2); c.closePath();
    const base = c.createRadialGradient(-26, -30, 10, 0, 0, 90); base.addColorStop(0, col(mixv("#e9eefb", C.white, fl))); base.addColorStop(1, col(mixv("#58607e", C.white, fl * 0.6)));
    c.fillStyle = base; c.fill();
    c.clip();
    const tile = 14, off = b.own.spin % tile;
    for (let gx = -98; gx < 98; gx += tile) {
      for (let gy = -88; gy < 88; gy += tile) {
        const ix = Math.floor((gx - off + 1000) / tile), iy = Math.floor((gy + 1000) / tile);
        const h = Math.sin(ix * 12.9898 + iy * 78.233) * 43758.5453, n = h - Math.floor(h);
        const shimmer = 0.5 + 0.5 * Math.sin(t * 4 + n * 12);
        const cTile = n < 0.33 ? tint : n < 0.6 ? tint2 : mixv("#c9d2e6", C.white, fl);
        c.fillStyle = col(cTile, 0.18 + 0.5 * shimmer * n);
        c.fillRect(gx + off + 1, gy + 1, tile - 2, tile - 2);
      }
    }
    // volume de la sphère
    const shade = c.createRadialGradient(-30, -34, 20, 0, 0, 92); shade.addColorStop(0, "rgba(255,255,255,0.18)"); shade.addColorStop(0.7, "rgba(10,12,30,0)"); shade.addColorStop(1, "rgba(10,12,30,0.55)");
    c.fillStyle = shade; c.fillRect(-90, -90, 180, 180);
    drawCracks(c, b, "rgba(255,255,255,0.9)", 1.8);
    c.restore();
    c.strokeStyle = col(tint, 0.7); c.lineWidth = 2.5; c.beginPath(); c.arc(0, 0, 86, 0, Math.PI * 2); c.stroke();

    // oreillettes
    for (const sx of [-1, 1]) {
      rr(c, sx < 0 ? -104 : 82, -34, 22, 50, 10); c.fillStyle = col(mixv("#2a2f48", C.white, fl * 0.5)); c.fill();
      rr(c, sx < 0 ? -100 : 86, -28, 14, 38, 7); c.fillStyle = col(tint, 0.8); c.fill();
    }

    // lunettes noires (glissent à l'armement et laissent voir des yeux furieux)
    const slide = Math.max(0, k) * 12 + castK * 4;
    c.save(); c.globalAlpha = b.stun > 0 ? 0.6 : 1;
    if (slide > 2) angryEyes(c, 14, -30, 26, 8, mixv(C.bad, C.white, fl), b.squint, 12);
    c.restore();
    c.save(); c.translate(-10, slide);
    const lens = (x0) => {
      rr(c, x0, -38, 44, 28, 12);
      const lg = c.createLinearGradient(x0, -38, x0 + 44, -10); lg.addColorStop(0, "#0b0f22"); lg.addColorStop(0.55, "#1d2142"); lg.addColorStop(0.62, col(tint2, 0.85)); lg.addColorStop(0.7, col(tint, 0.7)); lg.addColorStop(0.78, "#1d2142"); lg.addColorStop(1, "#0b0f22");
      c.fillStyle = lg; c.fill(); c.strokeStyle = col(mixv("#0b0f22", C.white, fl)); c.lineWidth = 3; c.stroke();
    };
    lens(-54); lens(4);
    c.strokeStyle = "#0b0f22"; c.lineWidth = 4; c.beginPath(); c.moveTo(-10, -28); c.quadraticCurveTo(-3, -34, 4, -28); c.stroke();
    c.beginPath(); c.moveTo(-54, -30); c.lineTo(-84, -20); c.moveTo(48, -30); c.lineTo(84, -20); c.stroke();
    if (b.squint > 0.3) { c.strokeStyle = "rgba(255,255,255,0.8)"; c.lineWidth = 1.4; c.beginPath(); c.moveTo(-40, -36); c.lineTo(-30, -24); c.lineTo(-22, -30); c.stroke(); }
    c.restore();
    // sourcil sceptique
    c.strokeStyle = col(mixv("#0b0f22", C.white, fl)); c.lineWidth = 4; c.lineCap = "round";
    c.beginPath(); c.moveTo(0, -50 - slide * 0.3); c.quadraticCurveTo(18, -60 - slide * 0.5, 38, -52); c.stroke();

    // bouche : sourire en coin, ouverte pendant la frappe
    c.strokeStyle = col(mixv("#0b0f22", C.white, fl)); c.lineWidth = 4;
    if (k < -0.2 || castK > 0.4) {
      c.fillStyle = "#0b0f22"; c.beginPath(); c.ellipse(-12, 38, 18, 10 + Math.abs(k) * 4, 0, 0, Math.PI * 2); c.fill();
      c.fillStyle = col(tint, 0.9); c.beginPath(); c.ellipse(-12, 43, 10, 4, 0, 0, Math.PI * 2); c.fill();
    } else {
      c.beginPath(); c.moveTo(-40, 34); c.quadraticCurveTo(-14, 50, 14, 30); c.stroke();
      c.beginPath(); c.moveTo(14, 30); c.lineTo(20, 26); c.stroke();
    }

    // main au pouce levé (pouce baissé quand il frappe)
    const hx = -84 + k * 22 + Math.sin(b.t * 2) * 3, hy = 64 + Math.cos(b.t * 2) * 3;
    c.save(); c.translate(hx, hy); c.rotate(k < -0.1 ? Math.PI : -0.15 + castK * 0.5);
    rr(c, -15, -12, 30, 26, 9); c.fillStyle = col(mixv("#f1e8ff", C.white, fl)); c.fill();
    c.strokeStyle = col(tint, 0.9); c.lineWidth = 2; c.stroke();
    rr(c, -13, -30, 10, 22, 5); c.fillStyle = col(mixv("#f1e8ff", C.white, fl)); c.fill(); c.stroke();
    c.strokeStyle = "rgba(42,29,58,0.5)"; c.lineWidth = 1.5;
    for (let j = 0; j < 3; j++) { c.beginPath(); c.moveTo(-2, -5 + j * 6); c.lineTo(13, -5 + j * 6); c.stroke(); }
    c.restore();

    // étourdi : étoiles au-dessus de la tête
    if (b.stun > 0) for (let j = 0; j < 3; j++) { const a = t * 4 + (j * Math.PI * 2) / 3; B.sparkle(c, Math.cos(a) * 34, -104 + Math.sin(a) * 8, 6, col(C.lamp, 0.95)); }

    c.restore();

    // jauge de métrique (cible critique) : dessinée par-dessus tout, au même endroit que weakSpot
    const ws = B.weakSpot(b);
    c.save(); c.translate(ws.x, ws.y);
    const g = c.createRadialGradient(0, 0, 2, 0, 0, 26); g.addColorStop(0, col(C.lamp, 0.55)); g.addColorStop(1, col(C.lamp, 0));
    c.fillStyle = g; c.beginPath(); c.arc(0, 0, 26, 0, Math.PI * 2); c.fill();
    c.fillStyle = col(mixv("#fdf7e3", C.white, fl)); c.beginPath(); c.arc(0, 0, 13, 0, Math.PI * 2); c.fill();
    c.strokeStyle = col(C.lamp); c.lineWidth = 2; c.stroke();
    c.lineWidth = 2.5; c.strokeStyle = C.ok; c.beginPath(); c.arc(0, 3, 8, Math.PI * 1.1, Math.PI * 1.45); c.stroke();
    c.strokeStyle = C.lamp; c.beginPath(); c.arc(0, 3, 8, Math.PI * 1.5, Math.PI * 1.7); c.stroke();
    c.strokeStyle = C.bad; c.beginPath(); c.arc(0, 3, 8, Math.PI * 1.75, Math.PI * 1.95); c.stroke();
    const na = Math.PI * 1.5 + Math.sin(t * 9) * 0.6 + Math.sin(t * 23) * 0.15;
    c.strokeStyle = "#0b0f22"; c.lineWidth = 1.8; c.beginPath(); c.moveTo(0, 3); c.lineTo(Math.cos(na) * 9, 3 + Math.sin(na) * 9); c.stroke();
    c.fillStyle = "#0b0f22"; c.beginPath(); c.arc(0, 3, 2, 0, Math.PI * 2); c.fill();
    c.restore();
  },

  sparkle(c, x, y, r, color) {
    c.fillStyle = color; c.beginPath();
    for (let k = 0; k < 8; k++) { const a = (k * Math.PI) / 4, rr2 = k % 2 ? r * 0.28 : r; c.lineTo(x + Math.cos(a) * rr2, y + Math.sin(a) * rr2); }
    c.closePath(); c.fill();
  }
};
