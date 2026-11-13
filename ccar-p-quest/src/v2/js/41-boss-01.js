/* Étage 1 — L'Ambigu : un nuage-fantôme de consignes floues qui étouffe une lanterne, la consigne claire qu'il cache. */
{
  const TAU = Math.PI * 2;
  const LX = 10, LY = 44;                                     // la lanterne (cible critique)
  const rgba = (v, a) => col(v, a <= 0 ? 0 : a >= 1 ? 1 : Math.round(a * 1000) / 1000);
  const hash = (k) => { const s = Math.sin(k * 127.1 + 31.7) * 43758.5453; return s - Math.floor(s); };

  /* Bouffées du nuage : [x, y, rayon, phase, stade de dégâts où elle se détache (0 = jamais), 1 = ne pousse qu'en rage]. */
  const PUFFS = [
    [0, -6, 62, 0.0, 0, 0], [-72, 4, 46, 1.3, 0, 0], [-40, -44, 46, 2.1, 0, 0], [14, -58, 50, 0.7, 0, 0],
    [62, -32, 44, 3.4, 0, 0], [92, 8, 34, 4.2, 2, 0], [50, 36, 42, 5.0, 0, 0], [-6, 42, 46, 2.7, 0, 0],
    [-60, 38, 36, 1.9, 3, 0], [-104, -32, 40, 0.4, 0, 1], [108, -44, 36, 3.0, 0, 1], [-16, -84, 40, 5.6, 0, 1]
  ];
  /* Traînes sous le nuage : [x, y, largeur, longueur, phase, 1 = ne pousse qu'en rage]. */
  const WISPS = [[-58, 62, 22, 44, 0.3, 0], [-18, 78, 24, 56, 1.7, 0], [26, 74, 22, 48, 3.1, 0], [64, 60, 20, 38, 4.4, 0], [-92, 36, 18, 66, 0.9, 1], [4, 80, 20, 78, 2.4, 1], [90, 30, 18, 62, 5.2, 1]];
  /* Déchirures : [x, y, rx, ry, stade d'apparition]. La deuxième s'ouvre autour de la lanterne. */
  const HOLES = [[70, -26, 13, 10, 1], [LX, LY + 2, 24, 27, 2], [-93, 27, 9, 11, 2], [-12, -88, 12, 9, 3], [66, 46, 11, 11, 3]];
  const WORDS = ["TBD", "etc.", "au mieux", "vite", "à voir", "…", "bref", "~"];
  const WORDS_RAGE = ["TBD !", "ASAP", "N’IMPORTE", "VITE !", "ON VERRA", "???", "BREF !", "…"];

  const X = [], Y = [], R = [], BX = [], BY = [];             // tampons de l'image en cours
  /** Contour du nuage : l'union des bouffées (un seul tracé). */
  const trace = (c, grow) => { c.beginPath(); for (let i = 0; i < X.length; i++) if (R[i] > 1.5) { c.moveTo(X[i] + R[i] + grow, Y[i]); c.arc(X[i], Y[i], R[i] + grow, 0, TAU); } };
  /** Ajoute au tracé une boucle bosselée (déchirure, brûlure) autour de (x, y). */
  const blob = (c, x, y, rx, ry, ph) => {
    const n = 10;
    for (let i = 0; i < n; i++) { const a = (i / n) * TAU, w = 1 + 0.15 * Math.sin(i * 2.3 + ph) + 0.09 * Math.sin(i * 4.7 - ph * 1.6); BX[i] = x + Math.cos(a) * rx * w; BY[i] = y + Math.sin(a) * ry * w; }
    c.moveTo((BX[n - 1] + BX[0]) / 2, (BY[n - 1] + BY[0]) / 2);
    for (let i = 0; i < n; i++) { const j = (i + 1) % n; c.quadraticCurveTo(BX[i], BY[i], (BX[i] + BX[j]) / 2, (BY[i] + BY[j]) / 2); }
    c.closePath();
  };
  /** Boucle en « ? » tracée pas à pas ; `straight` la déroule en « ! ». Utilise les styles courants. */
  const curl = (c, x, y, s, straight, wig) => {
    let a = -Math.PI / 2, px = x, py = y;
    const step = 6 * s * (1 - 0.3 * straight), bend = 1 - straight;
    c.beginPath(); c.moveTo(px, py);
    for (let i = 0; i < 13; i++) { a += ((i < 3 ? 0.3 : i < 12 ? -0.45 : -0.25) + wig * Math.sin(i * 0.7)) * bend; px += Math.cos(a) * step; py += Math.sin(a) * step; c.lineTo(px, py); }
    c.stroke();
    c.beginPath(); c.arc(x, y + 15 * s, 6.4 * s, 0, TAU); c.fill();
  };
  /** Un œil : copie fantôme décalée (double exposition), blanc, iris, pupille qui suit le regard, paupières. */
  const eye = (c, x, y, rx, ry, s) => {
    if (s.k <= 0.02) return;
    c.save(); c.translate(x, y); c.scale(s.k, s.k);
    c.fillStyle = s.ghost; c.beginPath(); c.ellipse(s.gx, s.gy, rx, ry, 0, 0, TAU); c.fill();
    c.fillStyle = s.ghostInk; c.beginPath(); c.arc(s.gx + s.lx * rx * 0.4, s.gy + s.ly * ry * 0.36, rx * 0.36, 0, TAU); c.fill();
    c.fillStyle = s.socket; c.beginPath(); c.ellipse(0, 1.5, rx + 3.2, ry + 3.2, 0, 0, TAU); c.fill();
    if (s.arc) {                                               // œil rieur : un arc
      c.beginPath(); c.ellipse(0, 0, rx, ry, 0, 0, TAU); c.fillStyle = s.lid; c.fill();
      c.strokeStyle = s.ink; c.lineWidth = 3.4; c.beginPath(); c.arc(0, ry * 0.5, rx * 0.72, Math.PI * 1.14, Math.PI * 1.86); c.stroke();
      c.restore(); return;
    }
    c.beginPath(); c.ellipse(0, 0, rx, ry, 0, 0, TAU); c.fillStyle = s.white; c.fill();
    c.save(); c.clip();
    const px = s.lx * rx * 0.4, py = s.ly * ry * 0.36;
    if (s.spiral) {
      c.strokeStyle = s.ink; c.lineWidth = 2.2; c.beginPath();
      for (let i = 0; i <= 26; i++) { const a = i * 0.48 + s.t * 7, r = i * rx * 0.034; if (i) c.lineTo(Math.cos(a) * r, Math.sin(a) * r); else c.moveTo(0, 0); }
      c.stroke();
    } else {
      c.fillStyle = s.iris; c.beginPath(); c.arc(px, py, rx * 0.64, 0, TAU); c.fill();
      const pr = rx * 0.33 * s.pupil;
      c.fillStyle = s.ink; c.beginPath(); c.ellipse(px * 1.15, py * 1.15, pr * (s.slit ? 0.42 : 1), pr * (s.slit ? 1.7 : 1), 0, 0, TAU); c.fill();
      c.fillStyle = "rgba(255,255,255,0.92)"; c.beginPath(); c.arc(px - rx * 0.24, py - rx * 0.27, rx * 0.16, 0, TAU); c.fill();
    }
    c.fillStyle = s.lid;
    if (s.top > 0.01 || s.tilt) {
      const yo = -ry - 2, hIn = 2 * ry * clamp(s.top + s.tilt, 0, 1.05), hOut = 2 * ry * clamp(s.top - s.tilt, 0, 1.05), xi = s.inner * (rx + 3);
      c.beginPath(); c.moveTo(-xi, yo); c.lineTo(xi, yo); c.lineTo(xi, yo + hIn + 2); c.lineTo(-xi, yo + hOut + 2); c.closePath(); c.fill();
    }
    if (s.bot > 0.01) { c.beginPath(); c.ellipse(0, ry + ry * 1.7 * (1 - s.bot), rx * 1.6, ry * 1.7, 0, 0, TAU); c.fill(); }
    c.restore();
    c.lineWidth = 1.8; c.strokeStyle = s.rim; c.beginPath(); c.ellipse(0, 0, rx, ry, 0, 0, TAU); c.stroke();
    c.restore();
  };
  /** La lanterne : `on` l'allume (0→1), `flare` la fait flamboyer (mort), `w` la blanchit (coup reçu). */
  const lantern = (c, t, on, flare, w) => {
    const flick = 0.86 + 0.1 * Math.sin(t * 9.3) + 0.06 * Math.sin(t * 23.1);
    const iron = rgba(mixv("#3a3466", C.white, w), on), edge = rgba(mixv("#9a93cf", C.white, w), on), warm = mixv("#f6d38a", C.white, w * 0.6);
    c.save(); c.translate(LX, LY - 24); c.rotate(Math.sin(t * 1.9) * 0.07); c.translate(0, 24);
    const gr = (40 + 62 * flare) * flick, g = c.createRadialGradient(0, 3, 1, 0, 3, gr);
    g.addColorStop(0, rgba("#fff8e0", 0.95 * on)); g.addColorStop(0.28, rgba(warm, (0.5 - 0.14 * flare) * on)); g.addColorStop(1, rgba(warm, 0));
    c.fillStyle = g; c.beginPath(); c.arc(0, 3, gr, 0, TAU); c.fill();
    if (flare > 0.02) {                                        // rayons : la consigne claire éclate au grand jour
      c.fillStyle = rgba("#fff3c8", 0.34 * flare);
      for (let i = 0; i < 8; i++) { const a = i * (TAU / 8) + t * 0.9, l = (60 + 52 * (i % 2)) * flare; c.beginPath(); c.moveTo(Math.cos(a + 0.5) * 5, 3 + Math.sin(a + 0.5) * 5); c.lineTo(Math.cos(a) * l, 3 + Math.sin(a) * l); c.lineTo(Math.cos(a - 0.5) * 5, 3 + Math.sin(a - 0.5) * 5); c.fill(); }
    }
    c.strokeStyle = edge; c.lineWidth = 2; c.beginPath(); c.arc(0, -21, 4.6, 0, TAU); c.stroke();
    c.fillStyle = iron; c.beginPath(); c.moveTo(-10, -11); c.lineTo(-5.5, -17.5); c.lineTo(5.5, -17.5); c.lineTo(10, -11); c.closePath(); c.fill();
    rr(c, -8.5, -11, 17, 25, 3); c.fillStyle = rgba(warm, 0.62 * on); c.fill(); c.strokeStyle = edge; c.lineWidth = 1.6; c.stroke();
    c.fillStyle = rgba(mixv("#fffbe8", C.white, w), on);
    c.beginPath(); c.moveTo(0, -6.5 - 3 * flick); c.quadraticCurveTo(6, 3, 0, 9.5); c.quadraticCurveTo(-6, 3, 0, -6.5 - 3 * flick); c.fill();
    c.fillStyle = iron; rr(c, -10.5, 13, 21, 5.5, 2); c.fill(); c.fillRect(-0.8, -11, 1.6, 4);
    c.restore();
  };

  BOSSES[1] = {
    v: 2,
    palette: { main: "#b9b2e0", dark: "#2a2850", accent: "#f6d38a", eye: "#f3f0ff", rage: "#ff4f9a" },
    hit: { rx: 128, ry: 98, coreR: 22 },
    top: 150,
    attackFrom: { x: -132, y: 6 },
    castLean: -0.1,
    weakSpot: (b) => ({ x: LX, y: LY + 4 * ((b && b.rageT) || 0) }),
    critLabel: "ÉCLAIRÉ",
    epitaph: "CLARIFIÉ",
    lines: {
      hit: ["Hé, c’était presque clair…", "Tu précises trop !", "Mes contours s’effacent…", "Aïe. Enfin… plus ou moins aïe."],
      crit: ["Ma lanterne ! Tu vois à travers moi ?", "Trop précis, ça brûle !", "Qui t’a soufflé le format attendu ?!"],
      wrong: ["Hmm… ça dépend, non ?", "Fais-le bien, c’est tout.", "Personne ne sait ce qu’on veut.", "Voilà. Enfin, à peu près."],
      timeout: ["Prends ton temps… ou pas.", "Trop lent. C’était flou, de toute façon.", "On avait dit « vite ». Ou « bien » ? Bref."],
      gloat: ["Tu vois ? Enfin… tu vois flou.", "C’était pourtant « évident ».", "Devine ce que je voulais dire !", "Raté. Raté comment ? Mystère."],
      rage: "Assez de précision ! Que tout redevienne vague !",
      special: {
        fog: ["Non… tout devient limpide !", "Arrête de préciser le format !", "Des exemples ? Qui t’a permis ?", "Remets-moi un peu de flou…"],
        mirage: ["Lequel de nous deux est le vrai ?", "Je suis ici. Ou là. À voir.", "Un double : devine lequel éclaire."]
      }
    },
    intro: {
      title: "Brouillard d’instructions",
      text: "L’Ambigu noie sa lanterne dans un brouillard qui cache sa cible critique et raccourcit ta visée ; chaque bonne réponse le dissipe, chaque erreur l’épaissit. Par moments un mirage sans lanterne te barre la route : contourne-le."
    },
    mechanics: ["fog"],

    init(b) { b.own.dmgSeen = b.dmg || 0; b.own.dmgAt = []; },
    update(b) {
      const o = b.own, dmg = b.dmg || 0;
      if (!o.dmgAt) { o.dmgAt = []; o.dmgSeen = dmg; }
      while (o.dmgSeen < dmg) o.dmgAt[++o.dmgSeen] = b.t;      // l'instant où chaque stade de dégâts commence
      if (dmg < o.dmgSeen) o.dmgSeen = dmg;
    },

    /* Dérive lente, avec de temps en temps une glissade de côté ; en orage il zigzague sans prévenir. */
    motion(b) {
      const t = b.t || 0, rg = b.rageT || 0;
      const slide = (period, hold, seed) => { const u = t / period, k = Math.floor(u); return lerp(hash(k + seed), hash(k + 1 + seed), easeInOut(seg(u - k, hold, 1))) * 2 - 1; };
      const cx = slide(4.4, 0.74, 3) * 30 - 16 + Math.sin(t * 0.5) * 7, cy = Math.sin(t * 0.8) * 11 + Math.sin(t * 0.33 + 1) * 8;
      const sx = slide(1.25, 0.45, 11) * 52 - 28 + Math.sin(t * 19) * 1.8, sy = slide(1.6, 0.4, 23) * 42 + Math.sin(t * 2.6) * 8;
      return { x: lerp(cx, sx, rg), y: lerp(cy, sy, rg) };
    },

    /* Projectile : une volute en « ? » qui reste droite quel que soit le sens du vol. */
    shot: {
      color: "#cfc8f5", spin: 0,
      draw(c, s) {
        const t = s.t || 0, hot = s.rage ? 1 : 0;
        for (let i = 3; i >= 1; i--) { c.fillStyle = rgba(hot ? "#ff9ad5" : "#b9b2e0", 0.14 * (4 - i)); c.beginPath(); c.arc(-10 * i + Math.sin(t * 20 + i) * 2, Math.cos(t * 16 + i * 2) * 3, 12 - i * 2.4, 0, TAU); c.fill(); }
        const m = c.getTransform ? c.getTransform() : null;
        if (m) c.rotate(-Math.atan2(m.b, m.a));
        c.rotate(Math.sin(t * 13) * 0.22);
        c.fillStyle = rgba(hot ? "#ff4f9a" : "#8f86d6", 0.3); c.beginPath(); c.arc(0, -3, 19, 0, TAU); c.fill();
        c.lineCap = "round"; c.lineJoin = "round"; c.lineWidth = 6.2;
        const dx = 1.6 + Math.sin(t * 17) * 0.8;
        c.strokeStyle = c.fillStyle = "rgba(127,233,255,0.6)"; curl(c, -1 - dx, 7, 0.5, 0, 0);
        c.strokeStyle = c.fillStyle = "rgba(255,143,208,0.6)"; curl(c, -1 + dx, 7.6, 0.5, 0, 0);
        c.strokeStyle = c.fillStyle = hot ? "#ffe6f3" : "#f6f3ff"; curl(c, -1, 7.3, 0.5, 0, 0);
      }
    },

    /* La Forge des Prompts : fourneau, cheminée, enclume, râtelier, lanternes à la poutre, parchemins de prompts épinglés. */
    backdrop(c, env) {
      const W = env.W, g = env.groundY, fx = W * 0.355;
      const glow = (x, y, r, a, hue) => { const q = c.createRadialGradient(x, y, 2, x, y, r); q.addColorStop(0, "rgba(" + hue + "," + a + ")"); q.addColorStop(1, "rgba(" + hue + ",0)"); c.fillStyle = q; c.fillRect(x - r, y - r, r * 2, r * 2); };
      const lamp = (x, y) => {                                  // lanterne suspendue (y = point d'accroche)
        c.strokeStyle = "#1d1a2b"; c.lineWidth = 1.5; c.beginPath(); c.moveTo(x, y); c.lineTo(x, y + 26); c.stroke();
        glow(x, y + 40, 58, 0.3, "243,184,65");
        c.fillStyle = "#1d1a2b"; c.beginPath(); c.moveTo(x - 9, y + 31); c.lineTo(x - 5, y + 25); c.lineTo(x + 5, y + 25); c.lineTo(x + 9, y + 31); c.closePath(); c.fill(); c.fillRect(x - 9, y + 50, 18, 4);
        c.fillStyle = "#f3b841"; c.fillRect(x - 7, y + 31, 14, 19); c.fillStyle = "#fff3c4"; c.beginPath(); c.ellipse(x, y + 42, 3, 6, 0, 0, TAU); c.fill();
        c.strokeStyle = "#1d1a2b"; c.lineWidth = 1.2; c.strokeRect(x - 7, y + 31, 14, 19); c.beginPath(); c.moveTo(x, y + 31); c.lineTo(x, y + 36); c.stroke();
      };
      glow(fx, g - 100, 320, 0.26, "246,130,60");

      // charpente : poteau, poutre, jambe de force
      const px = W * 0.035, by = g - 318;
      c.fillStyle = "#2a2230"; c.fillRect(px - 7, by, 14, 318); c.fillRect(-10, by, fx + 10, 13);
      c.fillStyle = "#463840"; c.fillRect(-10, by, fx + 10, 2.5); c.fillRect(px - 7, by, 2.5, 318);
      c.strokeStyle = "#2a2230"; c.lineWidth = 9; c.beginPath(); c.moveTo(px + 4, by + 62); c.lineTo(px + 58, by + 10); c.stroke();
      c.fillStyle = "rgba(246,150,70,0.35)"; c.fillRect(px + 5, by + 70, 2, 248); c.fillRect(px + 20, by + 11, fx - px - 60, 2);
      lamp(W * 0.092, by + 13);

      // parchemins de prompts pendus à une corde
      const sx0 = W * 0.142, sx1 = W * 0.292;
      c.strokeStyle = "#57463f"; c.lineWidth = 1.4; c.beginPath(); c.moveTo(sx0 - 6, by + 13); c.quadraticCurveTo((sx0 + sx1) / 2, by + 36, sx1, by + 13); c.stroke();
      for (let i = 0; i < 3; i++) {
        const x = lerp(sx0 + 14, sx1 - 20, i / 2), y = by + 24 + (i === 1 ? 6 : 2);
        c.save(); c.translate(x, y); c.rotate([-0.07, 0.04, 0.09][i]);
        c.fillStyle = "#8a6a4a"; c.fillRect(-2, -5, 4, 9);                                         // pince
        c.fillStyle = "#c9b68c"; c.fillRect(-15, 2, 30, 46); c.fillStyle = "#e0cfa5"; c.fillRect(-15, 2, 30, 3);
        c.fillStyle = "#a08c66"; rr(c, -17, 45, 34, 7, 3.5); c.fill();                             // bas enroulé
        c.fillStyle = "rgba(60,44,40,0.75)";
        if (i === 0) for (let k = 0; k < 5; k++) { c.fillRect(-11, 10 + k * 7, 3, 2); c.fillRect(-6, 10 + k * 7, 12 + ((k * 7) % 6), 2); }       // étapes numérotées
        else if (i === 1) { c.font = "700 9px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText("<ex>", 0, 12); c.fillRect(-9, 19, 18, 2); c.fillRect(-9, 24, 14, 2); c.fillRect(-9, 29, 17, 2); c.fillText("</ex>", 0, 38); }
        else { c.fillRect(-11, 9, 22, 2); c.fillRect(-11, 14, 16, 2); c.strokeStyle = "rgba(60,44,40,0.75)"; c.lineWidth = 1.2; c.strokeRect(-11, 20, 22, 13); c.fillRect(-8, 24, 14, 1.6); c.fillRect(-8, 28, 10, 1.6); c.fillStyle = "#b5482f"; c.beginPath(); c.arc(8, 40, 3.4, 0, TAU); c.fill(); }
        c.restore();
      }

      // cheminée et hotte
      const cg = c.createLinearGradient(fx - 24, 0, fx + 24, 0); cg.addColorStop(0, "#211e31"); cg.addColorStop(0.45, "#373250"); cg.addColorStop(1, "#262338");
      c.fillStyle = cg; c.fillRect(fx - 23, g - 448, 46, 190);
      c.strokeStyle = "rgba(15,14,26,0.5)"; c.lineWidth = 1;
      for (let y = g - 436; y < g - 262; y += 13) { c.beginPath(); c.moveTo(fx - 23, y); c.lineTo(fx + 23, y); c.stroke(); const o = (((y - g) / 13) | 0) % 2 ? 0 : 11; for (let x = fx - 23 + o; x < fx + 23; x += 22) { c.beginPath(); c.moveTo(x, y); c.lineTo(x, y + 13); c.stroke(); } }
      c.fillStyle = "#191727"; c.fillRect(fx - 26, g - 392, 52, 6); c.fillRect(fx - 26, g - 312, 52, 6);
      c.fillStyle = "#2c283f"; rr(c, fx - 30, g - 460, 60, 13, 3); c.fill(); c.fillStyle = "#3d3856"; c.fillRect(fx - 30, g - 460, 60, 3);
      c.fillStyle = "rgba(205,215,245,0.16)"; c.fillRect(fx + 20, g - 448, 2, 190);
      const hg = c.createLinearGradient(fx - 62, 0, fx + 62, 0); hg.addColorStop(0, "#252136"); hg.addColorStop(0.5, "#3b3654"); hg.addColorStop(1, "#28243a");
      c.fillStyle = hg; c.beginPath(); c.moveTo(fx - 62, g - 184); c.lineTo(fx - 23, g - 262); c.lineTo(fx + 23, g - 262); c.lineTo(fx + 62, g - 184); c.closePath(); c.fill();
      c.fillStyle = "#191727"; c.fillRect(fx - 64, g - 192, 128, 9);
      c.fillStyle = "#6a6488"; for (let k = 0; k < 6; k++) { c.beginPath(); c.arc(fx - 55 + k * 22, g - 187.5, 1.6, 0, TAU); c.fill(); }

      // fourneau : massif de pierre, gueule ardente
      const fg = c.createLinearGradient(0, g - 184, 0, g - 40); fg.addColorStop(0, "#3d374f"); fg.addColorStop(1, "#272336");
      c.fillStyle = fg; c.fillRect(fx - 68, g - 184, 136, 184);
      c.strokeStyle = "rgba(15,14,26,0.45)"; c.lineWidth = 1.2;
      for (let r = 0; r < 8; r++) { const y = g - 184 + r * 17; c.beginPath(); c.moveTo(fx - 68, y); c.lineTo(fx + 68, y); c.stroke(); for (let x = fx - 68 + (r % 2 ? 17 : 0); x < fx + 68; x += 34) { c.beginPath(); c.moveTo(x, y); c.lineTo(x, y + 17); c.stroke(); } }
      glow(fx, g - 92, 86, 0.5, "255,150,70");
      const arch = () => { c.beginPath(); c.moveTo(fx - 31, g - 56); c.lineTo(fx - 31, g - 104); c.arc(fx, g - 104, 31, Math.PI, 0); c.lineTo(fx + 31, g - 56); c.closePath(); };
      c.lineWidth = 9; c.strokeStyle = "#1a1828"; arch(); c.stroke();
      const mg = c.createRadialGradient(fx, g - 74, 4, fx, g - 86, 52); mg.addColorStop(0, "#fff6cf"); mg.addColorStop(0.35, "#ffbe55"); mg.addColorStop(0.75, "#e9642a"); mg.addColorStop(1, "#8a2a16");
      c.fillStyle = mg; arch(); c.fill();
      c.fillStyle = "rgba(255,246,200,0.85)";
      for (const [dx, h] of [[-14, 30], [2, 42], [15, 26]]) { c.beginPath(); c.moveTo(fx + dx - 8, g - 60); c.quadraticCurveTo(fx + dx - 6, g - 60 - h * 0.6, fx + dx, g - 60 - h); c.quadraticCurveTo(fx + dx + 7, g - 60 - h * 0.5, fx + dx + 8, g - 60); c.fill(); }
      c.strokeStyle = "rgba(255,190,110,0.5)"; c.lineWidth = 1.5; c.beginPath(); c.arc(fx, g - 104, 36, Math.PI * 1.08, Math.PI * 1.92); c.stroke();

      // potence et seconde lanterne, côté arène
      c.strokeStyle = "#1d1a2b"; c.lineWidth = 3.5; c.beginPath(); c.moveTo(fx + 23, g - 332); c.lineTo(fx + 76, g - 332); c.moveTo(fx + 23, g - 306); c.lineTo(fx + 50, g - 332); c.stroke();
      lamp(fx + 68, g - 332);

      // enclume sur son billot, lame de prompt encore rouge, marteau
      const ax = W * 0.505;
      c.fillStyle = "#3a2b2c"; c.fillRect(ax - 21, g - 96, 42, 40); c.fillStyle = "#4d3a38"; c.fillRect(ax - 21, g - 96, 42, 4);
      c.fillStyle = "#3f4663"; c.beginPath(); c.moveTo(ax - 56, g - 121); c.lineTo(ax + 28, g - 124); c.lineTo(ax + 28, g - 115); c.quadraticCurveTo(ax + 10, g - 112, ax + 12, g - 102); c.lineTo(ax + 22, g - 96); c.lineTo(ax - 22, g - 96); c.lineTo(ax - 12, g - 102); c.quadraticCurveTo(ax - 12, g - 113, ax - 30, g - 115); c.closePath(); c.fill();
      c.fillStyle = "rgba(255,176,96,0.75)"; c.fillRect(ax - 50, g - 123.5, 76, 2);
      glow(ax - 6, g - 128, 34, 0.5, "255,160,70");
      c.fillStyle = "#ffd98a"; c.fillRect(ax - 26, g - 129.5, 38, 5); c.fillStyle = "#ff8a3c"; c.fillRect(ax + 6, g - 129.5, 10, 5);
      c.strokeStyle = "#6b5140"; c.lineWidth = 3.5; c.beginPath(); c.moveTo(ax + 20, g - 127); c.lineTo(ax + 50, g - 144); c.stroke();
      c.fillStyle = "#59617f"; c.save(); c.translate(ax + 20, g - 128); c.rotate(-0.5); c.fillRect(-7, -11, 14, 19); c.restore();

      // râtelier bas, bac de trempe, tas de charbon (discrets, sous le boss)
      const rx = W * 0.6;
      c.fillStyle = "#2a2230"; c.fillRect(rx, g - 112, 4, 56); c.fillRect(rx + 66, g - 112, 4, 56); c.fillRect(rx - 4, g - 108, 78, 4);
      c.strokeStyle = "#4b5374"; c.lineWidth = 2.6; c.lineCap = "round";
      c.beginPath(); c.moveTo(rx + 12, g - 104); c.lineTo(rx + 12, g - 70); c.moveTo(rx + 28, g - 104); c.lineTo(rx + 24, g - 66); c.moveTo(rx + 28, g - 104); c.lineTo(rx + 32, g - 66); c.moveTo(rx + 44, g - 104); c.lineTo(rx + 44, g - 74); c.moveTo(rx + 58, g - 104); c.lineTo(rx + 58, g - 68); c.stroke();
      c.fillStyle = "#4b5374"; c.fillRect(rx + 6, g - 78, 12, 9); c.fillRect(rx + 40, g - 76, 8, 12);
      const qx = W * 0.815;
      c.fillStyle = "#3a2b2c"; c.beginPath(); c.moveTo(qx - 24, g - 102); c.lineTo(qx + 24, g - 102); c.lineTo(qx + 20, g - 56); c.lineTo(qx - 20, g - 56); c.closePath(); c.fill();
      c.fillStyle = "#59617f"; c.fillRect(qx - 24, g - 96, 48, 3); c.fillRect(qx - 22, g - 74, 44, 3);
      c.fillStyle = "#2c4a66"; c.beginPath(); c.ellipse(qx, g - 102, 24, 5, 0, 0, TAU); c.fill();
      c.strokeStyle = "#59617f"; c.lineWidth = 2.2; c.beginPath(); c.moveTo(qx - 8, g - 102); c.lineTo(qx - 16, g - 132); c.moveTo(qx + 6, g - 102); c.lineTo(qx + 12, g - 126); c.stroke();
      const kx = W * 0.925;
      c.fillStyle = "#1c1a29"; for (const [dx, dy, r] of [[-22, 0, 13], [-6, -8, 15], [12, -2, 14], [26, 4, 11], [2, 4, 16]]) { c.beginPath(); c.arc(kx + dx, g - 62 + dy, r, 0, TAU); c.fill(); }
      c.fillStyle = "rgba(255,140,70,0.8)"; for (const [dx, dy] of [[-10, -16], [8, -12], [-2, -20]]) c.fillRect(kx + dx, g - 62 + dy, 3, 2);
    },

    /* Décor animé : le foyer respire, des braises montent, la cheminée fume. */
    ambient(c, env) {
      const W = env.W, g = env.groundY, t = env.time || 0, fx = W * 0.355;
      const fl = 0.5 + 0.3 * Math.sin(t * 7.3) + 0.2 * Math.sin(t * 13.1);
      const gr = c.createRadialGradient(fx, g - 84, 4, fx, g - 84, 76); gr.addColorStop(0, rgba("#ffd98a", 0.16 + 0.16 * fl)); gr.addColorStop(1, "rgba(255,150,60,0)");
      c.fillStyle = gr; c.fillRect(fx - 76, g - 160, 152, 102);
      for (let i = 0; i < 9; i++) {
        const p = (t * (0.15 + (i % 3) * 0.04) + i * 0.231) % 1, x = fx + Math.sin(i * 12.9 + p * 6 + t * 0.4) * (10 + p * 44) + p * 26, y = g - 100 - p * 240 * (0.7 + (i % 4) * 0.1), s = 2.6 - p * 1.4;
        c.fillStyle = "rgba(255," + ((200 - p * 90) | 0) + ",90," + ((1 - p) * 0.9).toFixed(3) + ")"; c.fillRect(x, y, s, s);
      }
      for (let i = 0; i < 4; i++) {
        const p = (t * 0.1 + i / 4) % 1, x = fx + 4 + p * 50 + Math.sin(t * 0.6 + i * 2) * 7 * p, y = g - 466 - p * 84;
        c.fillStyle = rgba("#9a98b8", 0.2 * (1 - p) * Math.min(1, p * 6)); c.beginPath(); c.arc(x, y, 9 + p * 26, 0, TAU); c.fill();
      }
    },

    draw(c, b) {
      const t = b.t || 0, fl = b.flash || 0, rg = b.rageT || 0, dmg = b.dmg || 0, o = b.own || {};
      const e = b.enter ?? 1, dying = b.dying ?? -1, dead = dying >= 0, d = dead ? dying : 0;
      const look = b.look || { x: -1, y: 0 }, beat = b.beat || 0, threat = b.threat || 0, gloat = b.gloat || 0, talk = b.talk || 0;
      const stun = (b.stun || 0) > 0, sq = b.squint || 0, mirage = !!b.isMirage;
      const fog = (b.mech && b.mech.fog && b.mech.fog.shown) || 0;
      const castK = b.cast >= 0 ? Math.sin(clamp(b.cast / 0.9, 0, 1) * Math.PI) : 0;
      const ap = atkPose(b);
      const inh = !ap.on ? 0 : ap.strike > 0 ? 1 - easeOut(ap.strike) : easeOut(ap.wind);          // il aspire…
      const blow = !ap.on ? 0 : ap.rec > 0 ? 1 - easeInOut(ap.rec) : easeOut(ap.strike);           // …puis crache
      const since = (k) => (o.dmgAt && o.dmgAt[k] != null ? t - o.dmgAt[k] : 99);
      const rgB = backOut(rg), burnR = dead ? seg(d, 0.14, 0.84) ** 1.25 * 300 : 0;
      const wash = mirage ? 0.5 : 0, wfl = fl * 0.75;
      const tone = (calm, storm, a) => rgba(mixv(mixv(mixv(calm, storm, rg), "#e6e8f8", wash), C.white, wfl), a == null ? 1 : a);
      const ink = mixv(mixv("#2a2850", "#120f2a", rg), "#8d8ab5", wash);
      const vis = seg(e, 0.2, 0.75) * (1 - seg(d, 0.45, 0.9));
      if (mirage) c.globalAlpha *= 0.82;

      // halo
      const hg = c.createRadialGradient(-4, 0, 30, -4, 0, 185);
      hg.addColorStop(0, tone("#b9b2e0", "#ff4f9a", 0.2 * vis)); hg.addColorStop(1, tone("#b9b2e0", "#ff4f9a", 0));
      c.fillStyle = hg; c.fillRect(-189, -185, 370, 370);

      // mots vagues qui dérivent autour de lui, en double exposition
      const wordsA = seg(e, 0.78, 1) * (1 - seg(d, 0.04, 0.4));
      if (wordsA > 0.01) {
        c.font = "600 14px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle";
        const list = rg > 0.5 ? WORDS_RAGE : WORDS, n = list.length, wr = 1 - 0.26 * inh + 0.1 * blow + 0.3 * d;
        for (let i = 0; i < n; i++) {
          const a = t * (0.15 + 0.32 * rg) + (i * TAU) / n + Math.sin(t * 0.5 + i * 2.1) * 0.12;
          const x = -14 + Math.cos(a) * 163 * wr, y = -6 + Math.sin(a) * (128 + 20 * rg) * wr + Math.sin(t * 1.3 + i) * 5 - 40 * d;
          const al = wordsA * (0.5 + 0.25 * Math.sin(t * 0.9 + i * 1.7)), dx = 1.8 + Math.sin(t * 1.1 + i) * 1.3;
          c.fillStyle = rgba("#7fe9ff", al * 0.5); c.fillText(list[i], x - dx, y - 0.8);
          c.fillStyle = rgba("#ff8fd0", al * 0.5); c.fillText(list[i], x + dx, y + 0.8);
          c.fillStyle = tone("#e4e0ff", "#ffd3e8", al); c.fillText(list[i], x, y);
        }
      }

      // bouffées de l'image : respiration, entrée (elles convergent), dégâts (elles se détachent), rage (elles poussent)
      X.length = Y.length = R.length = 0;
      for (let i = 0; i < PUFFS.length; i++) {
        const p = PUFFS[i];
        let x = p[0] + Math.sin(t * 0.9 + p[3]) * 3.2, y = p[1] + Math.cos(t * 0.75 + p[3] * 1.7) * 2.6, r = p[2] * (1 + 0.035 * Math.sin(t * 1.3 + p[3] * 2));
        if (p[5]) r *= rgB;
        if (p[4] && dmg >= p[4]) { const k = easeOut(since(p[4]) / 0.9); x += Math.sign(p[0]) * 46 * k; y -= 30 * k; r *= 1 - k; }
        if (e < 1) { const gk = easeOut(seg(e, i * 0.02, 0.5 + i * 0.02)), a = Math.atan2(p[1] + 6, p[0] + 0.01) + (1 - gk) * 1.5; x += Math.cos(a) * 150 * (1 - gk); y += Math.sin(a) * 120 * (1 - gk); r *= 0.35 + 0.65 * gk; }
        X.push(x); Y.push(y); R.push(Math.max(0, r));
      }

      c.save();
      const shudder = dead ? Math.sin(t * 71) * 3 * seg(d, 0, 0.1) * (1 - seg(d, 0.3, 0.6)) : 0;
      c.translate(16 * inh - 34 * blow + 5 * threat + shudder, -Math.abs(Math.sin(t * 13)) * 9 * gloat + (stun ? 6 : 0));
      c.rotate((stun ? Math.sin(t * 2.6) * 0.06 : 0) + 0.07 * inh - 0.08 * blow);
      const S = (1 + 0.1 * rgB) * (1 + 0.14 * inh) * (1 - 0.04 * threat) * (1 + 0.05 * castK) * (1 + 0.025 * beat), br = Math.sin(t * 1.7) * 0.018;
      c.scale(S * (1 + br + 0.07 * fl + 0.13 * blow - 0.03 * inh), S * (1 - br - 0.07 * fl - 0.1 * blow + 0.03 * inh));
      c.lineCap = "round"; c.lineJoin = "round";

      // déchirures (dégâts) puis brûlure (mort) : ce qui est dessiné ensuite est rogné
      const tears = () => { for (const h of HOLES) if (dmg >= h[4]) { const k = backOut(clamp(since(h[4]) / 0.5, 0, 1)) * (1 + 0.32 * (dmg - h[4])); blob(c, h[0], h[1], h[2] * k, h[3] * k, h[0] + t * 0.8); } };
      const cut = () => {
        if (dmg > 0) { c.beginPath(); c.rect(-400, -400, 800, 800); tears(); c.clip("evenodd"); }
        if (burnR > 0) { c.beginPath(); c.rect(-400, -400, 800, 800); blob(c, LX, LY, burnR, burnR, t * 5); c.clip("evenodd"); }
      };

      const bodyA = seg(e, 0.25, 0.62) * (1 - 0.06 * dmg);
      c.save(); cut();
      // traînes
      const wa = seg(e, 0.55, 0.9);
      if (wa > 0.01) {
        const wg = c.createLinearGradient(0, 44, 0, 150 + 20 * rg); wg.addColorStop(0, tone("#8a80cc", "#3a3470", 0.95 * wa)); wg.addColorStop(1, tone("#8a80cc", "#ff4f9a", 0));
        c.fillStyle = wg;
        for (const w of WISPS) {
          const k = w[5] ? rgB : 1; if (k < 0.05) continue;
          const L = w[3] * k * wa * (1 + 0.12 * Math.sin(t * 1.1 + w[4])) * (1 - 0.3 * threat), sp = 1.5 + 1.6 * rg + 3 * castK, s1 = Math.sin(t * sp + w[4]) * (7 + 8 * rg), s2 = Math.sin(t * sp + w[4] - 1) * (12 + 14 * rg) + 26 * blow - 14 * inh, hw = w[2] / 2;
          c.beginPath(); c.moveTo(w[0] - hw, w[1]);
          c.bezierCurveTo(w[0] - hw + s1 * 0.4, w[1] + L * 0.45, w[0] + s1 - 3, w[1] + L * 0.7, w[0] + s2, w[1] + L);
          c.bezierCurveTo(w[0] + s1 + 4, w[1] + L * 0.7, w[0] + hw + s1 * 0.4, w[1] + L * 0.45, w[0] + hw, w[1]); c.fill();
        }
      }
      // volutes d'entrée : elles se condensent
      if (e < 0.8) {
        const sa = (1 - seg(e, 0.4, 0.8)) * seg(e, 0.02, 0.2);
        for (let i = 0; i < X.length; i++) if (R[i] > 1.5) { const rad = R[i] * 1.7, q = c.createRadialGradient(X[i], Y[i], 0, X[i], Y[i], rad); q.addColorStop(0, tone("#d9d4f5", "#8b82c4", 0.5 * sa)); q.addColorStop(1, tone("#d9d4f5", "#8b82c4", 0)); c.fillStyle = q; c.beginPath(); c.arc(X[i], Y[i], rad, 0, TAU); c.fill(); }
      }
      if (bodyA > 0.01) {
        // double exposition : deux copies décalées qui ne se superposent jamais
        const gx = 5 + 2 * Math.sin(t * 0.7) + 1.5 * dmg + 3 * rg + 6 * castK, gy = 3 * Math.cos(t * 0.9);
        trace(c, 9); c.fillStyle = tone("#b9b2e0", "#ff4f9a", 0.16 * bodyA); c.fill();                    // frange de brume
        c.translate(gx, gy); trace(c, 2.5); c.fillStyle = rgba("#7fe9ff", 0.24 * bodyA); c.fill();
        c.translate(-2 * gx, -2 * gy); trace(c, 2.5); c.fillStyle = rgba("#ff8fd0", 0.24 * bodyA); c.fill();
        c.translate(gx, gy);
        if (rg > 0.02) { trace(c, 3); c.fillStyle = rgba("#ff6fb0", 0.7 * rg * bodyA); c.fill(); }             // liseré d'orage
        const bg = c.createLinearGradient(0, -112, 0, 92);
        bg.addColorStop(0, tone("#f3f0ff", "#9d94d6", bodyA)); bg.addColorStop(0.52, tone("#b9b2e0", "#544b92", bodyA)); bg.addColorStop(1, tone("#7a70c4", "#2b2556", bodyA * 0.94));
        trace(c, 0); c.fillStyle = bg; c.fill();
        for (let i = 0; i < X.length; i++) if (R[i] > 8) {                                           // volume : chaque bouffée prend la lumière
          const hx = X[i] - R[i] * 0.28, hy = Y[i] - R[i] * 0.36, q = c.createRadialGradient(hx, hy, 0, hx, hy, R[i] * 0.98);
          q.addColorStop(0, rgba(C.white, (0.36 - 0.2 * rg) * bodyA)); q.addColorStop(1, rgba(C.white, 0));
          c.fillStyle = q; c.beginPath(); c.arc(X[i], Y[i], R[i], 0, TAU); c.fill();
        }
        if (rg > 0.02) { const ug = c.createLinearGradient(0, 10, 0, 96); ug.addColorStop(0, rgba("#ff4f9a", 0)); ug.addColorStop(1, rgba("#ff4f9a", 0.34 * rg * bodyA)); trace(c, 0); c.fillStyle = ug; c.fill(); }
        if (dmg > 0) { c.save(); trace(c, 0); c.clip(); c.beginPath(); tears(); c.lineWidth = 6; c.strokeStyle = tone("#5a5199", "#15122e", 0.6); c.stroke(); c.restore(); }
      }
      c.restore();

      // la lanterne, puis le voile qui la cache (il s'amincit avec les dégâts)
      const end = 1 - easeIn(seg(d, 0.88, 1));
      if (!mirage && end > 0.01) {
        const flare = dead ? easeOut(seg(d, 0, 0.3)) : 0;
        c.save(); c.translate(LX, LY); c.scale(end * (1 + 0.3 * flare), end * (1 + 0.3 * flare)); c.translate(-LX, -LY);
        lantern(c, t, seg(e, 0, 0.14) * (0.8 + 0.07 * dmg + 0.13 * beat), flare, fl);
        c.restore();
      }

      c.save(); cut();
      if (bodyA > 0.01) {
        const va = clamp(0.5 - 0.2 * dmg + 0.26 * fog, 0, 0.8) * bodyA * seg(e, 0.3, 0.7);
        if (va > 0.01) { const q = c.createRadialGradient(LX, LY, 4, LX, LY, 46); q.addColorStop(0, tone("#aaa2dc", "#463e80", va)); q.addColorStop(0.6, tone("#aaa2dc", "#463e80", va * 0.8)); q.addColorStop(1, tone("#aaa2dc", "#463e80", 0)); c.fillStyle = q; c.beginPath(); c.arc(LX, LY, 46, 0, TAU); c.fill(); }
        if (!mirage && !dead) { const wr = 30 + 3 * Math.sin(t * 9.3) + 6 * beat, q = c.createRadialGradient(LX, LY + 3, 2, LX, LY + 3, wr); q.addColorStop(0, rgba("#ffe9b0", 0.5 * bodyA)); q.addColorStop(1, rgba("#f6d38a", 0)); c.fillStyle = q; c.beginPath(); c.arc(LX, LY + 3, wr, 0, TAU); c.fill(); }   // sa lueur perce le voile : le mirage n'en a pas
        if (threat > 0.03) {                                                                         // il se crispe : deux bouffées se referment sur la lanterne
          const th = easeOut(threat);
          for (const sd of [-1, 1]) {
            const hx = LX + sd * (50 - 33 * th), hy = LY + 16 - 9 * th + sd * 3, hr = 21;
            c.fillStyle = tone("#b4acdf", "#51488e"); c.beginPath(); c.arc(hx, hy, hr, 0, TAU); c.fill();
            const q = c.createRadialGradient(hx - 6, hy - 8, 0, hx - 6, hy - 8, hr); q.addColorStop(0, rgba(C.white, 0.42 - 0.2 * rg)); q.addColorStop(1, rgba(C.white, 0)); c.fillStyle = q; c.fill();
            c.strokeStyle = tone("#7a70c4", "#2b2556", 0.45); c.lineWidth = 1.6; c.stroke();
          }
        }
        drawCracks(c, b, tone("#4b4785", "#0f0c24", 0.34), 2.2);
      }

      // visage : deux yeux dépareillés qui ne s'alignent jamais, un troisième en rage
      const k1 = backOut(seg(e, 0.72, 0.86)), k2 = backOut(seg(e, 0.8, 0.94));
      if (k1 > 0.02) {
        const panic = dead ? 1 : 0, wide = Math.max(threat, panic, inh * 0.8);
        let top1 = (t * 0.31 + 0.13) % 1 < 0.035 ? 1 : lerp(0.2, 0.02, wide), top2 = (t * 0.23 + 0.61) % 1 < 0.04 ? 1 : lerp(0.36, 0.04, wide);
        let bot = Math.max(0.55 * sq, 0.72 * gloat, 0.6 * blow), tilt = dead ? -0.14 : 0.24 * rg - 0.12 * threat;
        if (sq > 0.05 || blow > 0.3) { top1 = Math.max(top1, 0.42 * Math.max(sq, blow)); top2 = Math.max(top2, 0.42 * Math.max(sq, blow)); }
        if (gloat > 0.3) { top1 = Math.min(top1, 0.04); top2 = Math.min(top2, 0.04); tilt *= 0.4; }
        if (stun) { top1 = 0.24; top2 = 0.4; tilt = 0; }
        const lx = dead ? 0.55 : clamp(look.x, -1, 1), ly = dead ? 0.9 : clamp(look.y, -1, 1), dr = Math.sin(t * 0.6) * 0.5 + 0.3 * dmg;     // strabisme qui se promène
        const gx1 = (4 + 1.5 * dmg + 2 * rg) * Math.sin(t * 1.3) + 3, gy1 = 3 * Math.cos(t * 1.7), pup = 1 - 0.3 * threat - 0.45 * panic + 0.15 * rg;
        const lid = tone("#a199d6", "#3f3878"), white = tone("#fbfaff", "#fff0c2"), rim = rgba(ink, 0.75), socket = tone("#6f66b5", "#1d1940", 0.5);
        const ghost = rgba(C.white, 0.3), ghostInk = rgba(ink, 0.28), inkC = rgba(ink, 1);
        eye(c, -54, -30, 19, 22, { k: k1, gx: gx1, gy: gy1, lx, ly, top: top1, tilt, bot, inner: 1, iris: tone("#6d5bd0", "#ff4f9a"), ink: inkC, lid, white, rim, socket, ghost, ghostInk, pupil: pup, slit: rg > 0.6, spiral: stun, arc: gloat > 0.45 && !stun, t });
        eye(c, 8, -38, 13, 15, { k: k2, gx: -gx1 * 0.9, gy: -gy1, lx: clamp(lx * Math.cos(dr) - ly * Math.sin(dr), -1, 1), ly: clamp(lx * Math.sin(dr) + ly * Math.cos(dr), -1, 1), top: top2, tilt, bot, inner: -1, iris: tone("#22a99a", "#ffb000"), ink: inkC, lid, white, rim, socket, ghost, ghostInk, pupil: pup * 1.1, slit: rg > 0.6, spiral: stun, arc: gloat > 0.45 && !stun, t: -t });
        if (rg > 0.35) eye(c, -22, -76, 9, 12, { k: backOut(seg(rg, 0.35, 1)) * k1, gx: 2.5 * Math.cos(t * 1.9), gy: 2, lx, ly, top: (t * 0.4) % 1 < 0.05 ? 1 : 0.06, tilt: 0, bot: 0.5 * sq, inner: 1, iris: tone("#ff4f9a", "#ff4f9a"), ink: inkC, lid, white, rim, socket, ghost, ghostInk, pupil: 1, slit: true, spiral: stun, t });
        // sourcils : l'un haussé, l'autre bas (perplexe) ; froncés en rage
        const ba = seg(e, 0.86, 1), rise = 7 * threat + 5 * inh + 4 * sq + (dead ? 8 : 0), rb = dead ? 0 : rg;
        c.strokeStyle = rgba(ink, 0.82 * ba); c.lineWidth = 4.6;
        c.beginPath(); c.moveTo(-78, -56 - rise - 6 * rb); c.quadraticCurveTo(-58, -70 - rise + 4 * rb, -36, -60 - rise + 13 * rb); c.stroke();
        c.beginPath(); c.moveTo(-5, -55 - rise * 0.6 + 11 * rb); c.quadraticCurveTo(10, -60 - rise * 0.6 + 2 * rb, 25, -56 - rise * 0.6 - 5 * rb); c.stroke();
        // bouche : un tilde hésitant ; elle s'arrondit pour aspirer, s'ouvre en grand pour cracher
        const ma = seg(e, 0.86, 1), mx = -30, my = 7, open = Math.max(talk * 0.9, sq * 0.6);
        c.fillStyle = rgba(ink, 0.92 * ma); c.strokeStyle = rgba(mixv(ink, "#ff9ad5", rg * 0.75), 0.92 * ma); c.lineWidth = 3.4;
        if (inh > 0.08 || blow > 0.08) { c.beginPath(); c.ellipse(mx - 6 - 16 * blow, my, 4 + 2 * inh + 8 * blow, 4 + 3 * inh + 10 * blow, 0, 0, TAU); c.fill(); }
        else if (dead) { c.beginPath(); c.ellipse(mx, my + 3, 7, 9 + Math.sin(t * 30) * 1.5, 0, 0, TAU); c.fill(); }
        else if (gloat > 0.15) { c.beginPath(); c.moveTo(mx - 22, my - 5); c.quadraticCurveTo(mx, my + 20 * gloat, mx + 22, my - 5); c.quadraticCurveTo(mx, my + 4 * gloat, mx - 22, my - 5); c.fill(); }
        else if (open > 0.1) { c.beginPath(); c.ellipse(mx, my + 2, 10 - 2 * open, 2 + 8 * open, 0, 0, TAU); c.fill(); }
        else if (rg > 0.5) { c.beginPath(); for (let i = 0; i <= 6; i++) { const x = mx - 20 + i * 6.7, y = my + (i % 2 ? -4 : 4) + Math.sin(t * 9 + i) * 1; if (i) c.lineTo(x, y); else c.moveTo(x, y); } c.stroke(); }
        else { c.beginPath(); for (let i = 0; i <= 12; i++) { const x = mx - 19 + i * 3.2, y = my + Math.sin(i * 0.95 + t * 3.2) * 3.2 * (1 + stun); if (i) c.lineTo(x, y); else c.moveTo(x, y); } c.stroke(); }
      }

      // la boucle en « ? » (en rage, un « ! » lui répond ; à sa mort, elle se déroule : tout est clair)
      const ck = backOut(seg(e, 0.86, 1));
      if (ck > 0.02) {
        const straight = dead ? easeInOut(seg(d, 0.04, 0.36)) : 0, wig = 0.05 * Math.sin(t * 2.3) + 0.08 * threat * Math.sin(t * 40) + (stun ? 0.07 : 0);
        const qx = 78 + Math.sin(t * 1.1) * 2, qy = -98 + Math.sin(t * 1.9) * 2.5 - 3 * beat, dx = 3 + 1.5 * Math.sin(t * 0.8) + rg * 2;
        const mark = (x, y, s, st, rot, wg) => {
          c.save(); c.translate(x, y); c.rotate(rot); c.lineWidth = 11.5 * s;
          c.strokeStyle = c.fillStyle = rgba("#7fe9ff", 0.4); curl(c, dx, -1.5, s, st, wg);
          c.strokeStyle = c.fillStyle = rgba("#ff8fd0", 0.4); curl(c, -dx, 1.5, s, st, wg);
          c.strokeStyle = c.fillStyle = tone("#f3f0ff", "#ffd3e8"); curl(c, 0, 0, s, st, wg);
          c.restore();
        };
        mark(qx, qy, ck, straight, 0.2 + Math.sin(t * 1.4) * 0.07 - 0.2 * straight, wig);
        if (rg > 0.3) mark(-86 + Math.sin(t * 1.3) * 2, -96 + Math.cos(t * 1.7) * 2.5, backOut(seg(rg, 0.3, 0.9)) * 0.9 * ck, 1, -0.16 + Math.sin(t * 9) * 0.03, 0);
      }
      // éclair intérieur (rage)
      const lt = t * 1.25, li = Math.floor(lt), lf = lt - li, bolt = rg > 0.6 && !dead && lf < 0.2 && hash(li) > 0.22;
      if (bolt && bodyA > 0.01) { trace(c, 0); c.fillStyle = rgba(C.white, lf < 0.07 ? 0.3 : 0.12); c.fill(); }
      c.restore();

      // la brûlure mord le nuage de l'intérieur vers l'extérieur
      if (burnR > 2 && burnR < 280) {
        c.save(); trace(c, 0); c.clip();
        c.beginPath(); blob(c, LX, LY, burnR, burnR, t * 5);
        c.lineWidth = 16; c.strokeStyle = "rgba(255,138,60,0.5)"; c.stroke(); c.lineWidth = 7; c.strokeStyle = "rgba(255,214,130,0.9)"; c.stroke(); c.lineWidth = 2.2; c.strokeStyle = "#fffbe8"; c.stroke();
        c.restore();
        for (let i = 0; i < 14; i++) { const a = i * 2.4 + 0.3, p = (d * 3.2 + i * 0.37) % 1, r = burnR * (0.92 - p * 0.1), x = LX + Math.cos(a) * r, y = LY + Math.sin(a) * r * 0.9 - p * 46; if (Math.abs(x) < 170 && y > -170 && y < 150) { c.fillStyle = rgba("#ffd98a", (1 - p) * 0.9); c.fillRect(x, y, 3 - p * 1.6, 3 - p * 1.6); } }
      }

      // riposte : il aspire l'air, puis crache une volute
      if (inh > 0.05 && blow < 0.05) {
        c.strokeStyle = tone("#e4e0ff", "#ffd3e8", 0.7 * inh); c.lineWidth = 2.6;
        for (let i = 0; i < 7; i++) { const a = Math.PI + (i - 3) * 0.24, p = (t * 3.4 + i * 0.29) % 1, r0 = 158 - p * 96, r1 = r0 - 26 * (1 - p * 0.5); c.beginPath(); c.moveTo(-36 + Math.cos(a) * r0, 7 + Math.sin(a) * r0 * 0.8); c.lineTo(-36 + Math.cos(a) * r1, 7 + Math.sin(a) * r1 * 0.8); c.stroke(); }
      }
      if (blow > 0.05 && ap.rec < 0.7) {
        const p = ap.rec > 0 ? ap.rec / 0.7 : 0;
        c.strokeStyle = tone("#f3f0ff", "#ffd3e8", 0.7 * (1 - p)); c.lineWidth = 3;
        for (let i = 0; i < 3; i++) { c.beginPath(); c.arc(-70 - i * 16 - p * 36, 7, 12 + i * 7 + p * 10, Math.PI * 0.72, Math.PI * 1.28); c.stroke(); }
      }
      // action spéciale : il se dédouble dans une gerbe de signes vagues
      if (castK > 0.02) {
        const k = clamp(b.cast / 0.9, 0, 1), ko = easeOut(k);
        c.save(); c.translate(-86 * ko, 4 * ko); trace(c, 2); c.fillStyle = tone("#d9d4f5", "#8b82c4", 0.42 * (1 - k)); c.fill(); c.lineWidth = 2.5; c.strokeStyle = rgba("#7fe9ff", 0.5 * (1 - k)); c.stroke(); c.restore();
        c.lineWidth = 9 * (1 - k); c.strokeStyle = tone("#e4e0ff", "#ffd3e8", 0.4 * (1 - k)); c.beginPath(); c.ellipse(-6, 0, 96 + 70 * ko, 72 + 50 * ko, 0, 0, TAU); c.stroke();
        c.font = "800 26px " + F_DISPLAY; c.textAlign = "center"; c.textBaseline = "middle"; c.fillStyle = tone("#f3f0ff", "#ffd3e8", 0.95 * (1 - k * k));
        for (let i = 0; i < 6; i++) { const a = i * 1.05 + 0.3 + k * 0.5, r = 118 + ko * 46; c.fillText(i % 2 ? "…" : "?", -6 + Math.cos(a) * r, Math.sin(a) * r * 0.74); }
      }
      // étourdi : de petits « ? » tournent au-dessus de sa tête
      if (stun) {
        c.font = "800 20px " + F_DISPLAY; c.textAlign = "center"; c.textBaseline = "middle";
        for (let i = 0; i < 3; i++) { const a = t * 3.4 + i * 2.09; c.fillStyle = rgba(C.lamp, 0.55 + 0.4 * Math.sin(a)); c.fillText("?", -24 + Math.cos(a) * 46, -112 + Math.sin(a) * 10); }
      }
      // éclair (rage)
      if (bolt) {
        const r = seeded(li * 13 + 5); let x = -66 + r() * 132, y = 56;
        c.beginPath(); c.moveTo(x, y);
        for (let i = 0; i < 4; i++) { x += (r() - 0.5) * 36; y += 15 + r() * 8; c.lineTo(x, y); }
        c.save(); c.shadowColor = "#ff4f9a"; c.shadowBlur = 14; c.lineWidth = lf < 0.07 ? 3.4 : 2; c.strokeStyle = rgba("#fff6c8", lf < 0.07 || lf > 0.12 ? 1 : 0.45); c.stroke(); c.restore();
      }
      c.restore();
    }
  };
}
