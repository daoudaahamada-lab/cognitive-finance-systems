/* Étage 5 — Le Vibe-Checker : une boule à facettes suffisante, lunettes noires, casque sur les oreilles, pouce levé.
   Il juge « au feeling » et vit sur le temps de la musique. Sous les facettes qui tombent, un tableau de bord tout simple ;
   sa cible critique est la petite jauge de métrique qui sautille sur son visage : la vraie mesure qu'il refuse de regarder. */
BOSSES[5] = {
  v: 2,
  palette: { main: "#ff8fd0", dark: "#241a3a", accent: "#7fe3ff", eye: "#ffe27a", rage: "#ff5a36" },
  hit: { rx: 104, ry: 96, coreR: 17 },
  top: 110,
  attackFrom: { x: -152, y: -40 },
  castLean: 0.05,
  critLabel: "MESURÉ !",
  epitaph: "MESURÉ",
  lines: {
    hit: ["Hé, ça avait l’air bien pourtant.", "Mes vibes… ébranlées.", "Tu as… une rubrique ?", "Aïe. Statistiquement significatif."],
    crit: ["Une métrique ?! Pile dedans !", "Ma jauge ! Ne la regarde pas !", "Pas le chiffre ! Tout sauf le chiffre !"],
    wrong: ["Tu vois ? Au feeling, ça passe.", "Trois réponses lues, ça me suffit.", "Ça sent bon, je valide."],
    timeout: ["Je sens que t’as perdu.", "Pas besoin d’attendre les chiffres."],
    gloat: ["Pouce en bas. C’est mon ressenti.", "Zéro mesure, cent pour cent style.", "Noté au feeling : recalé.", "Ça, c’était une bonne vibe."],
    rage: "Mes vibes sont formelles : tu vas tomber !",
    special: {
      shuffle: ["Je mélange tout, l’ordre c’est une vibe.", "Tiens, relis tout ça au feeling.", "La position A, c’était une impression.", "Scratch ! Nouvel ordre, même flair."]
    }
  },
  intro: {
    title: "Pierres mélangées",
    text: "Il mélange tes pierres toutes les 25 secondes et après chaque tir raté : les lettres changent, seule la réponse compte. Sa jauge de métrique sautille sur son visage, vise-la pour un critique."
  },
  mechanics: ["shuffle"],

  /* La jauge s'attarde, puis file ailleurs sur le visage : des sauts pseudo-aléatoires tirés de b.t, plus nerveux en rage. */
  weakSpot(b) {
    const t = b.t || 0, rg = b.rage ? 1 : 0, u = t * (rg ? 2.2 : 1.3), i = Math.floor(u);
    const h = (n, s) => { const v = Math.sin(n * 127.1 + s * 311.7) * 43758.5453; return v - Math.floor(v); };
    const at = (n) => { const a = h(n, 1) * Math.PI * 2, r = Math.sqrt(h(n, 2)) * (rg ? 56 : 48); return [Math.cos(a) * r, Math.sin(a) * r * 0.9]; };
    const p = at(i), q = at(i + 1), k = easeInOut(seg(u - i, rg ? 0.4 : 0.55, 1)), j = rg ? 2.6 : 1.2;
    return { x: lerp(p[0], q[0], k) - 5 + Math.sin(t * 19) * j, y: lerp(p[1], q[1], k) + 7 + Math.cos(t * 23) * j };
  },

  /* Projectile : un vinyle au macaron « pouce baissé », lancé comme un frisbee. */
  shot: {
    color: "#ff8fd0", spin: 13,
    draw(c, s) { BOSSES[5].vinyl(c, 19, s && s.rage ? "#ff5a36" : "#ff8fd0"); }
  },

  /* Pas de côté en rythme (un aller-retour toutes les 8 pulsations, 4 en rage) : il glisse, se pose, repart ; le creux du balancier est au milieu. */
  motion(b) {
    const t = b.t || 0, r = b.rageT || 0, w = 1.545;
    const f = (u) => { const s = Math.sin(u); return [s * (1.5 - 0.5 * s * s), 1 - s * s]; }, p = f(t * w), q = f(t * w * 2);
    return { x: -24 + lerp(p[0] * 44, q[0] * 58, r), y: lerp(p[1] * 12, q[1] * 16, r) - 6 - (b.beat || 0) * 5 };
  },

  init(b) { if (b.own) b.own.spin = 0; },
  update(b, dt) {
    const o = b.own; if (!o) return;
    const sp = (0.55 + (b.rageT || 0) * 0.9) * ((b.cast ?? -1) >= 0 ? 6 : 1) * ((b.stun || 0) > 0 ? 0.15 : 1) * (1 + (b.flash || 0) * 2);
    o.spin = ((o.spin || 0) + dt * sp) % 6283.1853;
  },

  /* ------------------------------------------------------------ Décor : le Banc d'Essai ------------------------------------------------------------ */
  /* Repères partagés par backdrop et ambient. */
  lay(env) {
    const W = env.W, bench = env.groundY - 82, sx = Math.round(W * 0.235), sy = bench - 106;
    return { W, bench, scope: { x: sx, y: sy, w: 134, h: 100 }, screen: { x: sx + 12, y: sy + 14, w: 80, h: 60 }, lampL: { x: W * 0.36, y: 30 }, lampR: { x: W * 0.94, y: 30 } };
  },
  backdrop(c, env) {
    const B = BOSSES[5], L = B.lay(env), W = L.W, G = env.groundY, bench = L.bench, rnd = env.rnd || seeded(5);
    const iron = "#161c36", iron2 = "#1f2747", edge = "rgba(120,140,200,0.35)";
    c.lineCap = "round"; c.lineJoin = "round";

    // papier millimétré, à peine visible : ici, tout se mesure
    c.strokeStyle = "rgba(160,180,255,0.035)"; c.lineWidth = 1; c.beginPath();
    for (let x = W * 0.04; x < W; x += 38) { c.moveTo(x, 44); c.lineTo(x, bench); }
    for (let y = bench - 38; y > 44; y -= 38) { c.moveTo(0, y); c.lineTo(W, y); }
    c.stroke();
    // règle graduée le long du bord droit
    c.strokeStyle = "rgba(243,184,65,0.2)"; c.lineWidth = 1.5; c.beginPath();
    for (let y = bench - 10, k = 0; y > 70; y -= 19, k++) { c.moveTo(W - 4, y); c.lineTo(W - (k % 5 ? 12 : 22), y); }
    c.stroke();

    // rampe de projecteurs (la boîte de nuit s'est installée dans le labo)
    c.fillStyle = iron; c.fillRect(W * 0.28, 12, W, 5); c.fillRect(W * 0.28, 24, W, 4);
    c.strokeStyle = iron; c.lineWidth = 2; c.beginPath();
    for (let x = W * 0.28; x < W + 20; x += 22) { c.moveTo(x, 26); c.lineTo(x + 11, 14); c.lineTo(x + 22, 26); }
    c.stroke();
    for (const [lp, tint] of [[L.lampL, "#ff8fd0"], [L.lampR, "#7fe3ff"]]) {
      c.fillStyle = iron2; c.beginPath(); c.moveTo(lp.x - 9, lp.y - 6); c.lineTo(lp.x + 9, lp.y - 6); c.lineTo(lp.x + 14, lp.y + 12); c.lineTo(lp.x - 14, lp.y + 12); c.closePath(); c.fill();
      c.fillStyle = col(tint, 0.75); c.fillRect(lp.x - 13, lp.y + 11, 26, 3);
    }

    // portique de gauche : une toise graduée, une traverse, la check-list suspendue
    const px = W * 0.03, top = bench - 268;
    c.fillStyle = iron2; c.fillRect(px + 116, top, 7, 268); c.fillRect(px - 4, top - 6, 134, 8);
    c.fillStyle = "rgba(120,140,200,0.3)"; c.fillRect(px + 116, top, 1.5, 268); c.fillRect(px - 4, top - 6, 134, 1.5);
    c.strokeStyle = iron2; c.lineWidth = 4; c.beginPath(); c.moveTo(px + 119, top + 40); c.lineTo(px + 84, top); c.stroke();
    c.fillStyle = "#2a2440"; c.fillRect(px, top, 13, 268);
    c.strokeStyle = "rgba(243,184,65,0.6)"; c.lineWidth = 1.4; c.beginPath();
    for (let y = bench - 6, k = 0; y > top + 4; y -= 9, k++) { c.moveTo(px + 13, y); c.lineTo(px + (k % 5 ? 7 : 2), y); }
    c.stroke();
    // check-list : trois cases cochées, la dernière attend toujours sa mesure
    c.save(); c.translate(px + 62, top + 16); c.rotate(-0.045);
    c.strokeStyle = "rgba(160,170,200,0.5)"; c.lineWidth = 1.2; c.beginPath(); c.moveTo(-22, -16); c.lineTo(-16, 0); c.moveTo(22, -16); c.lineTo(16, 0); c.stroke();
    rr(c, -36, 0, 72, 98, 5); c.fillStyle = "#3b2c33"; c.fill();
    rr(c, -30, 9, 60, 83, 2); c.fillStyle = "rgba(205,211,230,0.82)"; c.fill();
    rr(c, -14, -5, 28, 11, 3); c.fillStyle = "#8b96b3"; c.fill();
    const marks = [C.ok, C.ok, C.ok, C.bad];
    for (let i = 0; i < 4; i++) {
      const y = 24 + i * 18;
      c.strokeStyle = "rgba(40,48,80,0.75)"; c.lineWidth = 1.4; c.strokeRect(-24, y - 5, 10, 10);
      c.lineWidth = 2.6; c.beginPath(); c.moveTo(-8, y - 2); c.lineTo(20 - (i % 2) * 8, y - 2); c.moveTo(-8, y + 4); c.lineTo(10 + (i % 3) * 4, y + 4); c.stroke();
      c.strokeStyle = marks[i]; c.lineWidth = 2.4; c.beginPath();
      if (i < 3) { c.moveTo(-23, y); c.lineTo(-20, y + 4); c.lineTo(-13, y - 6); } else { c.moveTo(-23, y - 4); c.lineTo(-15, y + 4); c.moveTo(-15, y - 4); c.lineTo(-23, y + 4); }
      c.stroke();
    }
    c.restore();

    // oscilloscope (sa trace est animée par ambient) et galvanomètre posé dessus
    const S = L.scope, Sc = L.screen;
    c.fillStyle = iron; c.fillRect(S.x + 10, S.y + S.h - 2, 12, 8); c.fillRect(S.x + S.w - 22, S.y + S.h - 2, 12, 8);
    rr(c, S.x, S.y, S.w, S.h, 9); c.fillStyle = iron2; c.fill(); c.strokeStyle = edge; c.lineWidth = 1.5; c.stroke();
    rr(c, Sc.x - 4, Sc.y - 4, Sc.w + 8, Sc.h + 8, 8); c.fillStyle = "#0d1226"; c.fill();
    rr(c, Sc.x, Sc.y, Sc.w, Sc.h, 6); c.fillStyle = "#06150f"; c.fill();
    c.strokeStyle = "rgba(98,240,166,0.16)"; c.lineWidth = 1; c.beginPath();
    for (let i = 1; i < 5; i++) { c.moveTo(Sc.x + (Sc.w * i) / 5, Sc.y + 2); c.lineTo(Sc.x + (Sc.w * i) / 5, Sc.y + Sc.h - 2); }
    for (let i = 1; i < 4; i++) { c.moveTo(Sc.x + 2, Sc.y + (Sc.h * i) / 4); c.lineTo(Sc.x + Sc.w - 2, Sc.y + (Sc.h * i) / 4); }
    c.stroke();
    const kx = S.x + S.w - 22;
    for (let i = 0; i < 2; i++) {
      c.fillStyle = "#0d1226"; c.beginPath(); c.arc(kx, S.y + 24 + i * 26, 9, 0, 6.2832); c.fill();
      c.strokeStyle = "rgba(200,210,240,0.6)"; c.lineWidth = 2; c.beginPath(); c.moveTo(kx, S.y + 24 + i * 26); c.lineTo(kx + (i ? 6 : -4), S.y + 18 + i * 26); c.stroke();
    }
    [C.ok, C.lamp, C.bad].forEach((k, i) => { c.fillStyle = col(k, 0.85); c.beginPath(); c.arc(kx - 9 + i * 9, S.y + 76, 2.6, 0, 6.2832); c.fill(); });
    c.strokeStyle = "#0d1226"; c.lineWidth = 3; c.beginPath(); c.moveTo(S.x + 30, S.y + S.h - 12); c.bezierCurveTo(S.x + 20, S.y + S.h + 30, S.x - 26, S.y + S.h - 40, S.x - 34, S.y + S.h + 2); c.stroke();
    const mx = S.x + 14, my = S.y - 44;
    rr(c, mx, my, 74, 44, 6); c.fillStyle = iron2; c.fill(); c.strokeStyle = edge; c.lineWidth = 1.5; c.stroke();
    rr(c, mx + 7, my + 7, 60, 26, 4); c.fillStyle = "rgba(240,232,205,0.8)"; c.fill();
    c.lineWidth = 3; c.lineCap = "butt";
    [[C.bad, 1.12, 1.36], [C.lamp, 1.38, 1.6], [C.ok, 1.62, 1.88]].forEach(([k, a, e]) => { c.strokeStyle = col(k, 0.9); c.beginPath(); c.arc(mx + 37, my + 40, 26, Math.PI * a, Math.PI * e); c.stroke(); });
    c.lineCap = "round"; c.strokeStyle = "#141230"; c.lineWidth = 2; c.beginPath(); c.moveTo(mx + 37, my + 34); c.lineTo(mx + 22, my + 13); c.stroke();

    // paillasse et règle plate sur son chant
    c.fillStyle = iron; c.fillRect(-10, bench, W + 20, 40);
    c.fillStyle = "#2b3560"; c.fillRect(-10, bench, W + 20, 3);
    c.fillStyle = "rgba(243,184,65,0.14)"; c.fillRect(-10, bench + 9, W + 20, 13);
    c.strokeStyle = "rgba(243,184,65,0.5)"; c.lineWidth = 1.2; c.beginPath();
    for (let x = 4, k = 0; x < W; x += 8, k++) { c.moveTo(x, bench + 9); c.lineTo(x, bench + (k % 5 ? 14 : 19)); }
    c.stroke();

    // portoirs de tubes à essai, erlenmeyer, petits cadrans : tout reste bas sous le boss
    const tubes = (x0, n, tints) => {
      c.fillStyle = "#4a3a34"; c.fillRect(x0 - 6, bench - 30, n * 14 + 8, 4); c.fillRect(x0 - 6, bench - 9, n * 14 + 8, 5);
      c.fillRect(x0 - 5, bench - 30, 4, 30); c.fillRect(x0 + n * 14 - 3, bench - 30, 4, 30);
      for (let i = 0; i < n; i++) {
        const x = x0 + i * 14, lv = 12 + rnd() * 20, tint = tints[i % tints.length];
        const gl = c.createRadialGradient(x + 4, bench - 14, 1, x + 4, bench - 14, 24); gl.addColorStop(0, col(tint, 0.22)); gl.addColorStop(1, col(tint, 0));
        c.fillStyle = gl; c.fillRect(x - 20, bench - 40, 48, 48);
        rr(c, x, bench - 4 - lv, 8, lv, 4); c.fillStyle = col(tint, 0.85); c.fill();
        rr(c, x, bench - 44, 8, 40, 4); c.strokeStyle = "rgba(210,225,255,0.55)"; c.lineWidth = 1.3; c.stroke();
      }
    };
    tubes(W * 0.425, 5, ["#ff8fd0", "#7fe3ff", C.toxic, C.lamp]);
    tubes(W * 0.9, 4, ["#7fe3ff", C.lamp, "#ff8fd0"]);
    const fx = W * 0.6;
    c.beginPath(); c.moveTo(fx - 5, bench - 38); c.lineTo(fx + 5, bench - 38); c.lineTo(fx + 5, bench - 24); c.lineTo(fx + 17, bench - 2); c.lineTo(fx - 17, bench - 2); c.lineTo(fx - 5, bench - 24); c.closePath();
    c.fillStyle = "rgba(190,215,255,0.08)"; c.fill(); c.strokeStyle = "rgba(210,225,255,0.5)"; c.lineWidth = 1.4; c.stroke();
    c.beginPath(); c.moveTo(fx - 9, bench - 16); c.lineTo(fx + 9, bench - 16); c.lineTo(fx + 16, bench - 3); c.lineTo(fx - 16, bench - 3); c.closePath(); c.fillStyle = col("#ff8fd0", 0.8); c.fill();
    const gx = W * 0.71;
    rr(c, gx, bench - 36, 104, 36, 5); c.fillStyle = iron2; c.fill(); c.strokeStyle = edge; c.lineWidth = 1.3; c.stroke();
    for (let i = 0; i < 3; i++) {
      const cx = gx + 20 + i * 32, cy = bench - 17, a = Math.PI * (1.15 + rnd() * 0.7);
      c.fillStyle = "rgba(240,232,205,0.82)"; c.beginPath(); c.arc(cx, cy, 11, 0, 6.2832); c.fill();
      c.strokeStyle = col([C.bad, C.lamp, C.ok][i], 0.9); c.lineWidth = 2.5; c.beginPath(); c.arc(cx, cy, 8, Math.PI * 1.1, Math.PI * 1.9); c.stroke();
      c.strokeStyle = "#141230"; c.lineWidth = 1.8; c.beginPath(); c.moveTo(cx, cy + 2); c.lineTo(cx + Math.cos(a) * 9, cy + 2 + Math.sin(a) * 9); c.stroke();
    }
  },
  /* Décor animé : la trace de l'oscilloscope (elle suit le temps de la musique) et deux cônes de projecteur. */
  ambient(c, env, b) {
    const B = BOSSES[5], L = B.lay(env), Sc = L.screen, time = env.time || 0, beat = (b && b.beat) || 0, rg = (b && b.rageT) || 0, G = env.groundY;
    for (const [lp, tint, tx] of [[L.lampL, "#ff8fd0", L.W * (0.52 + Math.sin(time * 0.6) * 0.2)], [L.lampR, "#7fe3ff", L.W * (0.7 + Math.sin(time * 0.47 + 2) * 0.17)]]) {
      const k = mixv(tint, "#ff5a36", rg * 0.8), g = c.createLinearGradient(lp.x, lp.y, tx, G - 60);
      g.addColorStop(0, col(k, 0.2 + beat * 0.05)); g.addColorStop(1, col(k, 0));
      c.fillStyle = g; c.beginPath(); c.moveTo(lp.x - 10, lp.y + 12); c.lineTo(lp.x + 10, lp.y + 12); c.lineTo(tx + 74, G - 60); c.lineTo(tx - 74, G - 60); c.closePath(); c.fill();
    }
    const amp = Sc.h * (0.16 + beat * 0.2), mid = Sc.y + Sc.h / 2;
    c.lineJoin = "round"; c.lineCap = "round"; c.beginPath();
    for (let i = 0; i <= 26; i++) {
      const u = i / 26, x = Sc.x + 4 + u * (Sc.w - 8), env2 = Math.sin(u * Math.PI);
      const y = mid + (Math.sin(u * 10 - time * 5) * amp + Math.sin(u * 33 + time * 12) * amp * 0.3) * env2;
      if (i) c.lineTo(x, y); else c.moveTo(x, y);
    }
    c.strokeStyle = col(C.toxic, 0.22); c.lineWidth = 5; c.stroke();
    c.strokeStyle = col(mixv(C.toxic, C.white, 0.35), 0.95); c.lineWidth = 1.6; c.stroke();
  },

  /* ------------------------------------------------------------ Pièces du personnage ------------------------------------------------------------ */
  /** Étoile à quatre branches. */
  star(c, x, y, r, rot) {
    c.beginPath();
    for (let k = 0; k < 8; k++) { const a = (rot || 0) + (k * Math.PI) / 4, q = k % 2 ? r * 0.26 : r; c.lineTo(x + Math.cos(a) * q, y + Math.sin(a) * q); }
    c.closePath(); c.fill();
  },
  /** Vinyle centré sur l'origine : sillons, reflets, macaron « pouce baissé ». */
  vinyl(c, r, tint) {
    c.fillStyle = "#0d0b1a"; c.beginPath(); c.arc(0, 0, r, 0, 6.2832); c.fill();
    c.strokeStyle = col(tint, 0.95); c.lineWidth = 1.8; c.stroke();
    c.strokeStyle = "rgba(255,255,255,0.17)"; c.lineWidth = 1;
    for (const q of [0.82, 0.68, 0.54]) { c.beginPath(); c.arc(0, 0, r * q, 0, 6.2832); c.stroke(); }
    c.fillStyle = "rgba(255,255,255,0.3)";
    for (const a of [0.35, 3.49]) { c.beginPath(); c.moveTo(0, 0); c.arc(0, 0, r * 0.9, a, a + 0.5); c.closePath(); c.fill(); }
    c.fillStyle = col(tint); c.beginPath(); c.arc(0, 0, r * 0.4, 0, 6.2832); c.fill();
    c.fillStyle = "#0d0b1a"; c.fillRect(-r * 0.2, -r * 0.2, r * 0.4, r * 0.24); c.fillRect(-r * 0.2, 0, r * 0.15, r * 0.26);
  },
  /** Gant blanc au pouce levé (rot = π : pouce baissé). */
  glove(c, x, y, rot, s, fl, tint) {
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s);
    const white = col(mixv("#fff6fc", C.white, fl));
    c.lineJoin = "round"; c.lineWidth = 2.4; c.strokeStyle = "#2a1d3a";
    rr(c, -12, 10, 24, 10, 4); c.fillStyle = col(tint); c.fill(); c.stroke();
    rr(c, -15, -32, 13, 30, 6.5); c.fillStyle = white; c.fill(); c.stroke();
    rr(c, -16, -11, 32, 23, 9); c.fillStyle = white; c.fill(); c.stroke();
    c.lineWidth = 1.6; c.strokeStyle = "rgba(42,29,58,0.5)"; c.beginPath();
    for (let j = 0; j < 3; j++) { c.moveTo(1, -5 + j * 5.5); c.lineTo(13, -5 + j * 5.5); }
    c.stroke(); c.restore();
  },
  /** Cadran de mesure : rouge à gauche, vert à droite, aiguille sur val (0 → 1). */
  gauge(c, x, y, r, val, o) {
    const a0 = Math.PI * 0.85, a1 = Math.PI * 2.15, at = (v) => lerp(a0, a1, v), hy = r * 0.14;
    c.save(); c.translate(x, y);
    if (o.glow) { const g = c.createRadialGradient(0, 0, r * 0.6, 0, 0, r * 2.1); g.addColorStop(0, col(C.lamp, 0.55 * o.glow)); g.addColorStop(1, col(C.lamp, 0)); c.fillStyle = g; c.beginPath(); c.arc(0, 0, r * 2.1, 0, 6.2832); c.fill(); }
    c.fillStyle = "#141230"; c.beginPath(); c.arc(0, 0, r * 1.13, 0, 6.2832); c.fill();
    c.fillStyle = col(mixv("#fdf6e0", C.white, o.fl || 0)); c.beginPath(); c.arc(0, 0, r, 0, 6.2832); c.fill();
    c.lineCap = "butt"; c.lineWidth = r * 0.2;
    for (const [u, v, k] of [[0, 0.4, C.bad], [0.4, 0.7, C.lamp], [0.7, 1, C.ok]]) { c.strokeStyle = k; c.beginPath(); c.arc(0, hy, r * 0.7, at(u), at(v)); c.stroke(); }
    if (o.big) {
      c.strokeStyle = "rgba(20,18,48,0.6)"; c.lineWidth = 1.6; c.beginPath();
      for (let i = 0; i <= 10; i++) { const a = at(i / 10), q = i % 5 ? 0.9 : 0.84; c.moveTo(Math.cos(a) * r * 0.96, hy + Math.sin(a) * r * 0.96); c.lineTo(Math.cos(a) * r * q, hy + Math.sin(a) * r * q); }
      c.stroke();
    }
    const na = at(clamp(val, -0.04, 1.04));
    c.strokeStyle = "#141230"; c.lineWidth = Math.max(1.8, r * 0.085); c.lineCap = "round";
    c.beginPath(); c.moveTo(-Math.cos(na) * r * 0.14, hy - Math.sin(na) * r * 0.14); c.lineTo(Math.cos(na) * r * 0.78, hy + Math.sin(na) * r * 0.78); c.stroke();
    c.fillStyle = "#141230"; c.beginPath(); c.arc(0, hy, Math.max(2, r * 0.13), 0, 6.2832); c.fill();
    if (o.text) {
      rr(c, -r * 0.46, r * 0.42, r * 0.92, r * 0.36, r * 0.08); c.fillStyle = "#141230"; c.fill();
      c.fillStyle = col(C.ok, o.textA == null ? 1 : o.textA); c.font = "700 " + Math.round(r * 0.3) + "px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText(o.text, 0, r * 0.61);
    }
    c.restore();
  },
  /** Boule à facettes : le tableau de bord en dessous, les facettes en bandes de latitude qui tournent, le volume. miss = part de facettes tombées. */
  ball(c, b, R, spin, miss, o) {
    const TAU = Math.PI * 2, H = Math.PI / 2;
    c.save(); c.beginPath(); c.arc(0, 0, R, 0, TAU); c.clip();
    c.fillStyle = col(mixv("#222a50", C.white, o.fl * 0.35)); c.fillRect(-R, -R, R * 2, R * 2);
    if (miss > 0) {
      c.strokeStyle = "rgba(165,185,240,0.2)"; c.lineWidth = 1; c.beginPath();
      for (let g = -R + 10; g < R; g += 18) { c.moveTo(-R, g); c.lineTo(R, g); c.moveTo(g, -R); c.lineTo(g, R); }
      c.stroke();
      c.strokeStyle = col(C.ok, 0.9); c.lineWidth = 2.4; c.lineJoin = "round"; c.beginPath();
      [[-74, 20], [-52, 4], [-34, 12], [-14, -14], [6, -4], [26, -30], [46, -20], [74, -46]].forEach((p, i) => (i ? c.lineTo(p[0], p[1]) : c.moveTo(p[0], p[1])));
      c.stroke();
      c.fillStyle = col(C.lamp, 0.85);
      for (let i = 0; i < 6; i++) { const h = 9 + ((i * 37) % 23); c.fillRect(-52 + i * 18, 66 - h, 11, h); }
    }
    if (miss < 1) {
      const bands = 8, p0 = -1.32, dp = 2.64 / bands;
      c.lineWidth = 1.3; c.strokeStyle = o.grout;
      for (let i = 0; i < bands; i++) {
        const pa = p0 + i * dp, pm = pa + dp / 2, ya = R * Math.sin(pa), yb = R * Math.sin(pa + dp), ra = R * Math.cos(pa), rb = R * Math.cos(pa + dp);
        const n = Math.max(6, Math.round(19 * Math.cos(pm))), step = TAU / n;
        for (let k = 0; k < n; k++) {
          const l1 = ((((k * step + spin + Math.PI) % TAU) + TAU) % TAU) - Math.PI, l2 = l1 + step;
          if (l2 < -H + 0.04 || l1 > H - 0.04) continue;
          const hv = Math.sin(i * 12.9898 + k * 78.233) * 43758.5453, h = hv - Math.floor(hv);
          if ((0.5 + 0.5 * Math.sin(k * step * 2 + i * 0.9 + 0.7)) * 0.65 + h * 0.35 < miss) continue;
          const s1 = Math.sin(Math.max(l1, -H)), s2 = Math.sin(Math.min(l2, H)), lm = (l1 + l2) / 2;
          let gl = Math.pow(0.5 + 0.5 * Math.sin(lm * 2.4 + pm * 2.1 + h * 6.283 + o.time * 0.7), 3);
          if (h > 0.7) gl = Math.min(1, gl + o.beat * 0.8);
          const base = h < 0.22 ? o.pink : h < 0.38 ? o.cyan : o.silver, h2 = (h * 7.13) % 1;
          c.fillStyle = col(mixv(mixv(mixv(o.deep, base, 0.3 + 0.7 * Math.max(h2 * 0.85, gl)), C.white, gl * 0.78 + o.fl * 0.5), "#171a30", (1 - o.lit) * 0.84));
          c.beginPath(); c.moveTo(ra * s1, ya); c.lineTo(ra * s2, ya); c.lineTo(rb * s2, yb); c.lineTo(rb * s1, yb); c.closePath(); c.fill(); c.stroke();
        }
      }
    }
    const sh = c.createRadialGradient(-R * 0.36, -R * 0.42, R * 0.1, 0, 0, R * 1.05);
    sh.addColorStop(0, "rgba(255,255,255," + 0.3 * o.lit + ")"); sh.addColorStop(0.45, "rgba(255,255,255,0)"); sh.addColorStop(0.75, "rgba(16,12,40,0.12)"); sh.addColorStop(1, "rgba(16,12,40,0.62)");
    c.fillStyle = sh; c.fillRect(-R, -R, R * 2, R * 2);
    drawCracks(c, b, "rgba(24,18,52,0.6)", 1.5);
    c.restore();
    c.strokeStyle = o.rim; c.lineWidth = 2.6; c.beginPath(); c.arc(0, 0, R, 0, TAU); c.stroke();
  },
  /** Lunettes noires centrées sur l'origine. Les verres laissent deviner un regard : un point de lumière qui suit la cible. */
  shades(c, o) {
    const ink = col(mixv("#0d0b1c", C.white, o.fl * 0.5));
    c.lineCap = "round"; c.lineJoin = "round";
    if (o.arms) { c.strokeStyle = ink; c.lineWidth = 4; c.beginPath(); c.moveTo(-52, -11); c.lineTo(-80, -5); c.moveTo(52, -11); c.lineTo(88, -4); c.stroke(); }
    for (const sx of [-1, 1]) {
      const x0 = sx < 0 ? -52 : 6, w = 46, cx = x0 + w / 2;
      const path = () => { c.beginPath(); c.moveTo(x0 + 3, -15); c.lineTo(x0 + w - 3, -15); c.quadraticCurveTo(x0 + w + 1, -15, x0 + w, -8); c.quadraticCurveTo(x0 + w - 1, 16, cx, 16); c.quadraticCurveTo(x0 + 1, 16, x0, -8); c.quadraticCurveTo(x0 - 1, -15, x0 + 3, -15); c.closePath(); };
      if (!(o.hole && sx < 0)) {
        c.save(); path(); c.clip();
        const lg = c.createLinearGradient(0, -15, 0, 16); lg.addColorStop(0, "#07060f"); lg.addColorStop(0.6, "#1b1238"); lg.addColorStop(1, col(mixv("#1b1238", o.pink, 0.55 * o.lit)));
        c.fillStyle = lg; c.fillRect(x0 - 2, -17, w + 4, 36);
        // égaliseur reflété au bas du verre
        for (let i = 0; i < 4; i++) { const h = (2 + 9 * Math.abs(Math.sin(o.time * 5.3 + i * 1.9 + sx))) * (0.35 + 0.65 * o.beat) * o.lit; c.fillStyle = col(i % 2 ? o.cyan : o.pink, 0.75); c.fillRect(x0 + 8 + i * 8.5, 14 - h, 5.5, h + 3); }
        c.fillStyle = "rgba(255,255,255," + 0.2 * o.lit + ")"; c.beginPath(); c.moveTo(x0 + 6, -17); c.lineTo(x0 + 18, -17); c.lineTo(x0 + 4, 18); c.lineTo(x0 - 8, 18); c.closePath(); c.fill();
        // le regard derrière le verre
        const ex = cx + o.lx * 9, ey = -1 + o.ly * 5;
        c.fillStyle = "rgba(255,255,255," + 0.13 * o.lit + ")"; c.beginPath(); c.ellipse(cx + o.lx * 3, 1, 15, 9, 0, 0, Math.PI); c.fill();
        c.fillStyle = "rgba(255,255,255," + 0.95 * o.lit + ")"; c.beginPath(); c.ellipse(ex, ey, 4.2, Math.max(0.8, 4.2 * (1 - o.blink)), 0, 0, 6.2832); c.fill();
        c.restore();
      }
      path(); c.strokeStyle = ink; c.lineWidth = 3.6; c.stroke();
      if (o.crack >= (sx < 0 ? 1 : 2) && !(o.hole && sx < 0)) {
        const kx = cx - sx * 6, ky = -2;
        c.strokeStyle = "rgba(255,255,255,0.92)"; c.lineWidth = 1.5; c.beginPath();
        for (const [dx, dy, ex2, ey2] of [[-14, -10, -19, -14], [12, -11, 19, -8], [-9, 12, -14, 16], [13, 9, 15, 16], [2, -13, -1, -15]]) { c.moveTo(kx, ky); c.lineTo(kx + dx * 0.55, ky + dy * 0.5 + 2); c.lineTo(kx + dx, ky + dy); c.lineTo(kx + ex2, ky + ey2); }
        c.stroke();
      }
    }
    c.strokeStyle = ink; c.lineWidth = 5.5; c.beginPath(); c.moveTo(-53, -15); c.lineTo(53, -15); c.stroke();
    c.strokeStyle = col(o.pink, 0.95); c.lineWidth = 1.6; c.beginPath(); c.moveTo(-50, -17.5); c.lineTo(50, -17.5); c.stroke();
  },

  /* ------------------------------------------------------------ Le personnage ------------------------------------------------------------ */
  draw(c, b) {
    const B = BOSSES[5], P = B.palette, TAU = Math.PI * 2, R = 82;
    const t = b.t || 0, time = b.time == null ? t : b.time, look = b.look || { x: -1, y: 0 };
    const en = b.enter ?? 1, dying = b.dying ?? -1, dmg = b.dmg || 0;
    const fl = b.flash || 0, sq = b.squint || 0, rg = b.rageT || 0, beat = b.beat || 0;
    const gloat = b.gloat || 0, talk = b.talk || 0, threat = b.threat || 0, stun = (b.stun || 0) > 0;
    const A = atkPose(b), wind = easeOut(A.wind) * (1 - easeOut(A.strike)), strike = easeOut(A.strike) * (1 - easeInOut(A.rec));
    const cast = (b.cast ?? -1) >= 0 ? clamp(b.cast / 0.9, 0, 1) : -1, castK = cast < 0 ? 0 : Math.sin(cast * Math.PI);
    const dead = dying >= 0, d = dead ? dying : 0;
    // entrée : descente au câble (0–0,58), allumage (0,5–0,7), la main et la jauge arrivent (0,7–1)
    const drop = backOut(seg(en, 0, 0.58)), lit = easeOut(seg(en, 0.5, 0.7)), pop = seg(en, 0.7, 1);
    // mort : les facettes partent (0,03–0,4), il ne reste qu'un cadran (0,3–0,5) qui se pose sur sa mesure (0,46–0,66), puis il tombe (0,8–1)
    const shed = seg(d, 0.03, 0.4), morph = easeInOut(seg(d, 0.3, 0.5)), fall = easeIn(seg(d, 0.8, 1)), show = 1 - seg(d, 0, 0.3);

    const hot = (hex, k) => mixv(mixv(hex, P.rage, rg * k), C.white, fl * 0.6);
    const pink = hot(P.main, 0.9), cyan = mixv(mixv(P.accent, "#ffc23d", rg), C.white, fl * 0.6), ink = mixv("#141230", C.white, fl * 0.5);
    const own = b.own || {};
    const spin = (own.spin != null ? own.spin : t * 0.55 * (1 + rg * 1.6)) + d * d * 34 - beat * 0.06;

    const offX = wind * 12 - strike * 17 + threat * 5 + (dead ? Math.sin(d * 80) * 5 * (1 - seg(d, 0, 0.3)) : 0);
    const offY = Math.sin(t * 2.2) * 3 - beat * 5 * (dead ? 0 : 1) - (1 - drop) * 340 + fall * 160 - gloat * Math.abs(Math.sin(time * 13)) * 6;
    const tilt = Math.sin(t * 2.2 + 1) * 0.02 + wind * 0.1 - strike * 0.15 + threat * 0.04 - gloat * 0.07 + (stun ? Math.sin(time * 8) * 0.09 : 0) + fall * 0.5;
    const ws = B.weakSpot(b);

    // faisceau de poursuite qui cherche la scène pendant l'entrée
    if (en < 1) {
      const a = seg(en, 0, 0.1) * (1 - seg(en, 0.66, 0.92)), tx = (1 - easeOut(seg(en, 0.06, 0.5))) * Math.sin(en * 17) * 170;
      if (a > 0.01) {
        const g = c.createLinearGradient(30, -430, tx, 80); g.addColorStop(0, "rgba(255,255,255," + 0.34 * a + ")"); g.addColorStop(1, "rgba(255,240,250," + 0.05 * a + ")");
        c.fillStyle = g; c.beginPath(); c.moveTo(22, -430); c.lineTo(38, -430); c.lineTo(tx + 104, 96); c.lineTo(tx - 104, 96); c.closePath(); c.fill();
      }
    }

    c.save(); c.translate(offX, offY); c.rotate(tilt);
    if (dead && fall > 0) { c.globalAlpha *= 1 - seg(d, 0.9, 1); c.scale(1 - fall * 0.35, 1 - fall * 0.35); }
    const glow = lit * show;

    // halo, rayons de boule à facettes, lasers de rage
    if (glow > 0.01) {
      const hg = c.createRadialGradient(0, 0, 40, 0, 0, 185); hg.addColorStop(0, col(pink, (0.24 + beat * 0.08) * glow)); hg.addColorStop(0.6, col(cyan, 0.07 * glow)); hg.addColorStop(1, col(cyan, 0));
      c.fillStyle = hg; c.beginPath(); c.arc(0, 0, 185, 0, TAU); c.fill();
      const calm = glow * (1 - rg);
      if (calm > 0.02) {
        const len = 150 + beat * 22;
        for (const par of [0, 1]) {
          const k = par ? cyan : pink, g = c.createRadialGradient(0, 0, 80, 0, 0, len); g.addColorStop(0, col(k, (0.27 + beat * 0.13) * calm)); g.addColorStop(1, col(k, 0));
          c.fillStyle = g; c.beginPath();
          for (let i = par; i < 8; i += 2) {
            const a = spin * 0.3 + (i * TAU) / 8;
            c.moveTo(Math.cos(a - 0.05) * 78, Math.sin(a - 0.05) * 78); c.lineTo(Math.cos(a - 0.085) * len, Math.sin(a - 0.085) * len); c.lineTo(Math.cos(a + 0.085) * len, Math.sin(a + 0.085) * len); c.lineTo(Math.cos(a + 0.05) * 78, Math.sin(a + 0.05) * 78); c.closePath();
          }
          c.fill();
        }
      }
      if (rg > 0.02) {                                                                    // lasers : un seul tracé, deux passes (lueur, cœur)
        const g1 = c.createRadialGradient(0, 0, 84, 0, 0, 184); g1.addColorStop(0, col(P.rage, 0.55 * glow)); g1.addColorStop(1, col(P.rage, 0));
        const g2 = c.createRadialGradient(0, 0, 84, 0, 0, 184); g2.addColorStop(0, col(mixv(P.rage, C.white, 0.8), glow)); g2.addColorStop(1, col(mixv(P.rage, C.white, 0.4), 0.1 * glow));
        c.lineCap = "round"; c.beginPath();
        for (let i = 0; i < 6; i++) {
          const a = -spin * 0.8 + (i * TAU) / 6 + Math.sin(time * 3 + i) * 0.05, len = (156 + (i % 2) * 20 + beat * 8) * easeOut(rg);
          if (len > 86) { c.moveTo(Math.cos(a) * 84, Math.sin(a) * 84); c.lineTo(Math.cos(a) * len, Math.sin(a) * len); }
        }
        c.strokeStyle = g1; c.lineWidth = 9; c.stroke(); c.strokeStyle = g2; c.lineWidth = 2.4; c.stroke();
      }
    }
    // étincelles en orbite
    const spk = glow * pop;
    if (spk > 0.02) {
      for (let i = 0; i < 7; i++) {
        const a = (i * TAU) / 7 + t * 0.35 * (1 + rg), r = 124 + 9 * Math.sin(t * 1.3 + i * 2.1) + castK * 14 + gloat * 8, tw = 0.5 + 0.5 * Math.sin(time * 3.1 + i * 1.9);
        c.fillStyle = col(i % 3 === 0 ? C.white : i % 3 === 1 ? pink : cyan, (0.45 + 0.55 * tw) * spk);
        B.star(c, Math.cos(a) * r * 1.02, Math.sin(a) * r * 0.86, (4.5 + (i % 3) * 2.4) * (0.55 + 0.6 * tw + beat * 0.55) * spk, rg * time * 2);
      }
    }
    // mélange : les pierres du joueur tournent autour de lui (moitié arrière)
    const stones = (front) => {
      if (castK <= 0.02) return;
      c.save(); c.font = "700 15px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle";
      const ga = c.globalAlpha;
      for (let i = 0; i < 4; i++) {
        const a = cast * 11 + (i * TAU) / 4, dz = Math.sin(a);
        if ((dz >= 0) !== front) continue;
        const x = Math.cos(a) * 128, y = 16 + dz * 42 - castK * 8, r = 13 + dz * 2;
        c.globalAlpha = ga * castK * (front ? 1 : 0.6);
        c.fillStyle = "#d3d9ea"; c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill(); c.strokeStyle = "rgba(12,17,30,0.75)"; c.lineWidth = 2; c.stroke();
        c.fillStyle = C.night; c.fillText("ABCD"[(i + Math.floor(cast * 9)) % 4], x, y + 1);
      }
      c.restore();
    };
    stones(false);

    // câble et crochet de l'entrée : il tient la boule par l'arceau du casque, puis remonte
    if (en < 1) {
      const up = -easeIn(seg(en, 0.8, 1)) * 420;
      c.strokeStyle = "#8b96b3"; c.lineWidth = 2.5; c.lineCap = "round"; c.beginPath(); c.moveTo(0, -560 + up); c.lineTo(0, -116 + up); c.stroke();
      c.lineWidth = 3.5; c.beginPath(); c.arc(0, -107 + up, 9, -Math.PI / 2, Math.PI * 0.95); c.stroke();
    }

    // casque : il glisse à chaque stade de dégâts, et s'envole à la mort
    const slip = [0, 0.13, 0.3, 0.5][dmg] + Math.sin(t * 2.3) * 0.012 * dmg + (stun ? 0.08 : 0);
    const hd = seg(d, 0.06, 0.4), hpA = 1 - seg(d, 0.2, 0.36), dark = col(mixv("#23203f", C.white, fl * 0.5));
    const phones = (front) => {
      if (hpA <= 0) return;
      c.save(); c.globalAlpha *= hpA; c.translate(-hd * 30, -hd * 60 + hd * hd * 330); c.rotate(slip - hd * 1.1);
      if (!front) {
        c.lineCap = "round"; c.strokeStyle = dark; c.lineWidth = 10; c.beginPath(); c.arc(0, 0, 95, Math.PI * 1.07, Math.PI * 1.93); c.stroke();
        c.lineWidth = 15; c.beginPath(); c.arc(0, 0, 96, Math.PI * 1.4, Math.PI * 1.6); c.stroke();
        c.strokeStyle = col(pink, 0.85 * Math.max(0.3, lit)); c.lineWidth = 2.6; c.beginPath(); c.arc(0, 0, 98, Math.PI * 1.12, Math.PI * 1.88); c.stroke();
      } else {
        for (const sx of [-1, 1]) {
          c.save(); c.translate(sx * 93, 0);
          if (dmg >= 3 && sx > 0 && !dead) { c.strokeStyle = dark; c.lineWidth = 2.5; c.beginPath(); c.moveTo(0, -24); c.quadraticCurveTo(14, -6, 8, 14); c.stroke(); c.translate(8, 30); c.rotate(0.5 + Math.sin(t * 3.1) * 0.22); }
          rr(c, -12, -28, 24, 56, 10); c.fillStyle = dark; c.fill();
          rr(c, sx < 0 ? -10 : -6, -22, 16, 44, 7); c.fillStyle = col(pink, 0.3 + 0.7 * lit); c.fill();
          c.fillStyle = dark; c.beginPath(); c.arc(sx * -2, 0, 4.5 + beat * 2.2 * lit, 0, TAU); c.fill();
          if (beat > 0.05 && lit > 0.5 && !dead) { c.strokeStyle = col(pink, beat * 0.8); c.lineWidth = 2; c.beginPath(); c.arc(sx * 2, 0, 20 + (1 - beat) * 12, sx < 0 ? Math.PI * 0.82 : -Math.PI * 0.18, sx < 0 ? Math.PI * 1.18 : Math.PI * 0.18); c.stroke(); }
          c.restore();
        }
      }
      c.restore();
    };
    phones(false);

    // la boule : écrasement au coup reçu, facettes qui tombent
    const Rb = lerp(R, 66, morph), miss = dead ? lerp([0, 0.17, 0.34, 0.55][dmg], 1.01, easeOut(shed)) : [0, 0.17, 0.34, 0.55][dmg];
    c.save(); c.scale((1 + fl * 0.07 - wind * 0.03 + strike * 0.05) * (1 + beat * 0.02), (1 - fl * 0.07 + wind * 0.03 - strike * 0.04) * (1 + beat * 0.02));
    B.ball(c, b, Rb, spin, miss, { fl, lit, time, beat: beat * lit, pink, cyan, silver: mixv(mixv("#c4cbe2", "#ffd0a8", rg * 0.5), C.white, fl * 0.5), deep: mixv("#4a5078", "#6a2a3a", rg * 0.6), grout: "rgba(22,18,48,0.9)", rim: col(mixv(pink, "#23203f", (1 - lit) * 0.8), 0.9) });
    c.restore();
    // éclats de facettes de la mort, facettes qui se décrochent quand il est abîmé
    if (dead && d < 0.75) {
      for (let i = 0; i < 16; i++) {
        const h1 = (i * 0.618) % 1, h2 = (i * 0.377 + 0.2) % 1, age = (d - 0.03 - h1 * 0.3) / 0.36;
        if (age <= 0 || age >= 1) continue;
        const a = h2 * TAU + i, r = 66 + age * (70 + h1 * 80), x = Math.cos(a) * r * (Math.cos(a) > 0 ? 0.8 : 1), y = Math.sin(a) * r + age * age * 110;
        c.save(); c.translate(x, y); c.rotate(age * 9 * (h2 - 0.5) + i); c.globalAlpha *= 1 - age * age;
        c.fillStyle = col(i % 3 === 0 ? pink : i % 3 === 1 ? cyan : "#e6ebfa"); c.fillRect(-6, -5, 12 - h1 * 4, 10 - h2 * 3); c.restore();
      }
    } else if (dmg > 0 && !dead && en >= 1) {
      for (let i = 0; i < dmg; i++) {
        const u = (t * 0.55 + i * 0.37) % 1, x = -50 + ((i * 53 + Math.floor(t * 0.55 + i * 0.37) * 37) % 100), y = 60 + u * u * 120;
        c.save(); c.translate(x, y); c.rotate(u * 7 + i); c.globalAlpha *= 1 - u;
        c.fillStyle = col(i % 2 ? cyan : "#e6ebfa"); c.fillRect(-5, -4, 10, 8); c.restore();
      }
    }
    phones(true);

    // reflet en étoile, signature de la boule à facettes
    if (lit > 0.5 && shed < 0.3) { c.fillStyle = col(C.white, (0.55 + beat * 0.45) * (1 - shed * 3)); B.star(c, -43, -50, 8 + beat * 10, 0); }

    // visage (il disparaît quand la boule devient cadran)
    const faceA = dead ? 1 - seg(d, 0.24, 0.38) : 1, fx = -6 + look.x * 3.5, fy = -18 + look.y * 2;
    const blink = (time % 3.7) < 0.13 ? 1 : 0;
    const off = Math.max(rg, dead ? seg(d, 0.02, 0.4) : 0);                              // lunettes éjectées : en rage, et à la mort
    const slide = wind * 11 + threat * 12 + castK * 4 + (stun ? 7 : 0) + sq * 4;
    if (faceA > 0.01) {
      c.save(); c.globalAlpha *= faceA;
      const halo = (w) => { c.strokeStyle = "rgba(255,255,255," + 0.5 * lit + ")"; c.lineWidth = w; c.stroke(); };
      const inkc = col(ink), shock = dead ? 1 : 0, wide = clamp(threat + shock + sq * 0.6, 0, 1), fury = rg > 0.5 && !shock && !stun;
      // yeux : endormis derrière les verres, furieux en rage, ronds de stupeur à la fin
      for (const sx of [-1, 1]) {
        c.save(); c.translate(fx + sx * 30, fy - 4 + (fury ? 7 : 0));
        if (stun) {
          c.fillStyle = col(mixv("#fff6ea", C.white, fl)); c.beginPath(); c.arc(0, 3, 13.5, 0, TAU); c.fill(); c.strokeStyle = inkc; c.lineWidth = 2.2; c.stroke();
          c.lineWidth = 2.4; c.lineCap = "round"; c.beginPath();
          for (let q = 0; q <= 12; q++) { const a = q * 0.8 + time * 6 * sx, r = 0.8 + q * 0.8; c.lineTo(Math.cos(a) * r, 3 + Math.sin(a) * r); }
          c.stroke();
        } else if (fury) {
          const k = backOut(seg(rg, 0.5, 1)) * 1.32, cl = sq * 7; c.scale(k, k);
          c.beginPath(); c.moveTo(sx * 20, -12 + cl); c.lineTo(sx * -15, 2 + cl * 0.5); c.quadraticCurveTo(sx * -15, 12, 0, 13); c.quadraticCurveTo(sx * 19, 13, sx * 20, -12 + cl); c.closePath();
          c.save(); c.shadowColor = col(P.rage); c.shadowBlur = 14; c.fillStyle = col(mixv("#fff3d2", C.white, fl)); c.fill(); c.restore();
          c.save(); c.clip();
          c.fillStyle = col(P.rage); c.beginPath(); c.arc(look.x * 6 + sx * 1, 4 + look.y * 3.5, 7.6, 0, TAU); c.fill();
          c.fillStyle = "#1a0810"; c.beginPath(); c.arc(look.x * 7.5 + sx * 1, 4 + look.y * 4.2, 3.3, 0, TAU); c.fill();
          c.fillStyle = C.white; c.beginPath(); c.arc(look.x * 7.5 + sx * 1 - 2.5, 1.5 + look.y * 4.2, 1.5, 0, TAU); c.fill();
          c.restore();
          c.strokeStyle = inkc; c.lineWidth = 2; c.stroke();
          c.lineWidth = 6.5; c.lineCap = "round"; c.beginPath(); c.moveTo(sx * 25, -19 + cl - beat * 2); c.lineTo(sx * -16, -4 + cl * 0.5); c.stroke();
        } else {
          const lid = clamp(lerp(0.52, 0.04, wide) + blink * 0.5, 0, 1), pr = lerp(4.6, 3, wide), ry = 10 + wide * 2;
          c.beginPath(); c.ellipse(0, 0, 13, ry, 0, 0, TAU); c.fillStyle = col(mixv("#fff6ea", C.white, fl)); c.fill();
          c.save(); c.clip();
          c.fillStyle = "#1a1030"; c.beginPath(); c.arc(look.x * 5.5, 1 + look.y * 3.5 - wide * 4, pr, 0, TAU); c.fill();
          if (lid > 0.06) { c.fillStyle = col(mixv(pink, "#3a2a55", 0.35)); c.fillRect(-15, -ry - 2, 30, 2 * ry * lid + 2); c.fillStyle = inkc; c.fillRect(-15, -ry + 2 * ry * lid - 1, 30, 2); }
          c.restore();
          c.beginPath(); c.ellipse(0, 0, 13, ry, 0, 0, TAU); c.strokeStyle = inkc; c.lineWidth = 2; c.stroke();
        }
        c.restore();
      }
      // lunettes : fissurées au stade 1, un verre en moins au stade 3 ; elles s'envolent quand il enrage
      if (off < 1) {
        c.save();
        if (off > 0) { c.globalAlpha *= 1 - seg(off, 0.55, 1); c.translate(fx + off * 150, fy - off * 230 + off * off * 250); c.rotate(off * 7); }
        else { c.translate(fx, fy + slide); c.rotate(stun ? 0.2 : sq * -0.06); }
        B.shades(c, { fl, lit, time, beat, pink, cyan, lx: look.x, ly: look.y, blink, crack: dmg, hole: dmg >= 3, arms: off <= 0 }); c.restore();
      }
      // sourcils : l'un toujours levé, sûr de lui
      if (!fury && !stun) {
        const up = threat * 6 + gloat * 4 * Math.abs(Math.sin(time * 12)) + shock * 8, mean = wind * 6;
        c.lineCap = "round";
        for (const pass of [0, 1]) {
          c.beginPath();
          c.moveTo(fx - 47, fy - 25 - up + mean * 0.2); c.quadraticCurveTo(fx - 30, fy - 30 - up, fx - 12, fy - 26 - up * 0.6 + mean);
          c.moveTo(fx + 12, fy - 31 - up * 0.6 + mean * 1.6); c.quadraticCurveTo(fx + 30, fy - 41 - up, fx + 47, fy - 30 - up);
          if (pass) { c.strokeStyle = inkc; c.lineWidth = 5; c.stroke(); } else halo(9);
        }
      }
      // bouche
      const mx = -8 + look.x * 3.5, my = 37, open = Math.max(talk * 0.7, strike, shock);
      c.lineCap = "round"; c.lineJoin = "round";
      if (stun) {
        c.beginPath(); c.moveTo(mx - 20, my); for (let q = 1; q <= 4; q++) c.quadraticCurveTo(mx - 20 + q * 10 - 5, my + (q % 2 ? -7 : 7), mx - 20 + q * 10, my);
        halo(9); c.strokeStyle = inkc; c.lineWidth = 4.5; c.stroke();
      } else if (shock) {
        c.fillStyle = "#1a0f2a"; c.beginPath(); c.ellipse(mx, my + 2, 13, 17, 0, 0, TAU); c.fill(); halo(3);
      } else if (fury) {
        const h = 16 + talk * 9 + strike * 9 + gloat * 5, w = 31 + gloat * 5, my2 = my + 3;
        c.beginPath(); c.moveTo(mx - w, my2 - 3 - gloat * 5); c.quadraticCurveTo(mx, my2 - 12 + gloat * 8, mx + w, my2 - 3 - gloat * 5); c.quadraticCurveTo(mx + w - 2, my2 + h, mx, my2 + h - 3); c.quadraticCurveTo(mx - w + 2, my2 + h, mx - w, my2 - 3 - gloat * 5); c.closePath();
        c.fillStyle = col(mixv("#fffaf0", C.white, fl)); c.fill(); c.strokeStyle = inkc; c.lineWidth = 3.4; c.stroke();
        c.save(); c.clip(); c.lineWidth = 2.2; c.beginPath(); c.moveTo(mx - w, my2 + h * 0.45 - 2); c.quadraticCurveTo(mx, my2 + h * 0.45 - 7 + (talk + strike) * 5 + gloat * 8, mx + w, my2 + h * 0.45 - 2);
        for (let q = -2; q <= 2; q++) { c.moveTo(mx + q * 11, my2 - 14); c.lineTo(mx + q * 11, my2 + h); }
        c.stroke(); c.restore();
      } else if (gloat > 0.12) {
        const h = 12 + gloat * 12;
        c.beginPath(); c.moveTo(mx - 30, my - 6); c.quadraticCurveTo(mx, my - 1, mx + 30, my - 10); c.quadraticCurveTo(mx + 22, my + h + 4, mx - 2, my + h); c.quadraticCurveTo(mx - 24, my + h - 2, mx - 30, my - 6); c.closePath();
        c.fillStyle = "#1a0f2a"; c.fill(); halo(3);
        c.save(); c.clip(); c.fillStyle = "#fffaf0"; c.fillRect(mx - 32, my - 12, 64, 12 + gloat * 3); c.fillStyle = col(pink); c.beginPath(); c.ellipse(mx, my + h + 2, 14, 8, 0, 0, TAU); c.fill(); c.restore();
      } else if (open > 0.12) {
        const h = 6 + open * 17;
        c.beginPath(); c.moveTo(mx - 20, my - 4); c.quadraticCurveTo(mx, my - 8, mx + 20, my - 6); c.quadraticCurveTo(mx + 16, my + h, mx, my + h); c.quadraticCurveTo(mx - 16, my + h, mx - 20, my - 4); c.closePath();
        c.fillStyle = "#1a0f2a"; c.fill(); halo(3);
        c.save(); c.clip(); c.fillStyle = "#fffaf0"; c.fillRect(mx - 22, my - 10, 44, 8); c.fillStyle = col(pink); c.beginPath(); c.ellipse(mx, my + h + 1, 11, 6, 0, 0, TAU); c.fill(); c.restore();
      } else if (sq > 0.3 || threat > 0.3) {
        const amp = 3 + sq * 5;
        c.beginPath(); c.moveTo(mx - 22, my + 2); for (let q = 1; q <= 4; q++) c.quadraticCurveTo(mx - 22 + q * 11 - 5.5, my + 2 + (q % 2 ? -amp : amp), mx - 22 + q * 11, my + 2);
        halo(9); c.strokeStyle = inkc; c.lineWidth = 4.5; c.stroke();
      } else {
        for (const pass of [0, 1]) {
          c.beginPath(); c.moveTo(mx - 28, my - 3); c.quadraticCurveTo(mx - 2, my + 13, mx + 25, my - 9); c.moveTo(mx + 25, my - 9); c.quadraticCurveTo(mx + 31, my - 11, mx + 30, my - 17);
          if (pass) { c.strokeStyle = inkc; c.lineWidth = 4.8; c.stroke(); } else halo(9.5);
        }
      }
      // goutte de sueur quand le joueur vise, veine de colère en rage
      if (threat > 0.15 && !fury) {
        const sy = -52 + ((time * 26) % 16);
        c.fillStyle = col("#bfeaff", threat * 0.95); c.beginPath(); c.moveTo(58, sy - 9); c.quadraticCurveTo(66, sy + 4, 58, sy + 6); c.quadraticCurveTo(50, sy + 4, 58, sy - 9); c.fill();
      }
      if (rg > 0.3 && !dead) {
        c.save(); c.translate(48, -60); c.scale(rg * (1 + beat * 0.25), rg * (1 + beat * 0.25)); c.strokeStyle = col(P.rage); c.lineWidth = 3.8; c.lineCap = "round";
        for (let q = 0; q < 4; q++) { c.rotate(Math.PI / 2); c.beginPath(); c.moveTo(3.5, 11); c.quadraticCurveTo(3.5, 3.5, 11, 3.5); c.stroke(); }
        c.restore();
      }
      c.restore();
    }

    // platine du mélange : un scratch de DJ sous le gant
    if (castK > 0.02) {
      c.save(); c.translate(-112, 84); c.scale(backOut(seg(cast, 0, 0.25)) * (1 - seg(cast, 0.8, 1)), 0.36 * backOut(seg(cast, 0, 0.25)) * (1 - seg(cast, 0.8, 1)));
      c.rotate(Math.sin(cast * 34) * 0.9 + cast * 3); B.vinyl(c, 44, pink); c.restore();
      c.strokeStyle = col(C.white, castK * 0.8); c.lineWidth = 2; c.lineCap = "round";
      for (const q of [0, 1]) { c.beginPath(); c.arc(-112, 78, 50 + q * 9, Math.PI * (1.1 + q * 0.03), Math.PI * (1.26 - q * 0.03)); c.stroke(); c.beginPath(); c.arc(-112, 78, 50 + q * 9, Math.PI * (1.74 + q * 0.03), Math.PI * (1.9 - q * 0.03)); c.stroke(); }
    }
    // la main : pouce levé nonchalant ; il se retourne à l'armement, puis la main lance le vinyle
    const handK = pop > 0 && en < 1 ? backOut(seg(en, 0.7, 0.92)) : en >= 1 ? 1 : 0, hf = easeIn(seg(d, 0.04, 0.42));
    if (handK > 0.01 && hf < 1) {
      const restR = lerp(-0.14 + Math.sin(t * 1.7) * 0.07, -Math.PI / 2 + Math.sin(time * 31) * 0.06, rg) + (stun ? 1.1 : 0);
      let hx = -114 + Math.sin(t * 1.7) * 3, hy = 60 + Math.cos(t * 1.7) * 4 - beat * 5 - gloat * (16 + Math.abs(Math.sin(time * 13)) * 14) + (stun ? 14 : 0), hr = restR - gloat * 0.2;
      if (threat > 0.01) { hx = lerp(hx, -88, threat); hy = lerp(hy, 26, threat); hr = lerp(hr, 0.5 + Math.sin(time * 22) * 0.05, threat); }
      if (castK > 0.01) { hx = lerp(hx, -112 + Math.sin(cast * 34) * 15, castK); hy = lerp(hy, 66, castK); hr = lerp(hr, -1.2 + Math.sin(cast * 34) * 0.3, castK); }
      if (A.on) {
        const w = easeOut(A.wind), s = easeOut(A.strike), r = easeInOut(A.rec), rx0 = hx, ry0 = hy;
        hx = lerp(hx, -116, w); hy = lerp(hy, -46, w); hr = lerp(hr, Math.PI, easeInOut(A.wind));
        hx = lerp(hx, -150, s); hy = lerp(hy, 14, s);
        hx = lerp(hx, rx0, r); hy = lerp(hy, ry0, r); hr = lerp(hr, restR, r);
        if (A.strike <= 0) {                                                             // le vinyle se charge au bout des doigts
          const k = backOut(A.wind);
          c.save(); c.translate(hx - 36, hy + 6); c.scale(k, k);
          c.strokeStyle = col(P.rage, 0.5 + 0.4 * Math.sin(time * 30)); c.lineWidth = 3; c.beginPath(); c.arc(0, 0, 24 + A.wind * 3, 0, TAU); c.stroke();
          c.rotate(time * 16); B.vinyl(c, 19, rg > 0.5 ? P.rage : P.main); c.restore();
        } else if (A.rec < 0.5) {                                                        // traits de vitesse du lancer
          c.strokeStyle = col(C.white, 0.8 * (1 - A.rec * 2)); c.lineWidth = 2.5; c.lineCap = "round";
          for (let q = 0; q < 3; q++) { c.beginPath(); c.moveTo(-150 - q * 4, -44 + q * 14); c.lineTo(-176 - A.strike * 20 - q * 6, -40 + q * 16); c.stroke(); }
        }
      }
      c.save(); if (hf > 0) c.globalAlpha *= 1 - hf;
      B.glove(c, hx - hf * 30, hy + hf * 170, hr + hf * 2.6, 1.15 * handK * (1 + beat * 0.06), fl, pink);
      c.restore();
    }
    stones(true);

    // la jauge de métrique (cible critique) ; à la mort elle gagne le centre et devient le seul cadran, honnête
    const gk = en >= 1 ? 1 : backOut(seg(en, 0.8, 1));
    if (gk > 0.01) {
      const glide = easeInOut(seg(d, 0.14, 0.44)), settle = seg(d, 0.46, 0.66);
      const twitch = 0.5 + Math.sin(time * 9.3) * 0.34 + Math.sin(time * 23.7) * 0.13 + (stun ? 0 : Math.sin(time * 4.1) * 0.08);
      const val = dead ? lerp(twitch, 0.62 + (1 - settle) * 0.45 * Math.cos(settle * 16), seg(d, 0.34, 0.48)) : twitch;
      B.gauge(c, lerp(ws.x, 0, glide), lerp(ws.y, 0, glide), lerp(14, 58, morph) * gk, val, { fl, glow: (0.75 + beat * 0.25) * (1 - morph * 0.45), big: morph > 0.5, text: morph > 0.6 ? (settle > 0.6 ? "0,62" : "-,--") : null, textA: 0.6 + 0.4 * settle });
      if (dead && settle >= 1) {                                                         // mesuré : la coche verte
        const k = backOut(seg(d, 0.66, 0.74));
        c.fillStyle = C.ok; c.beginPath(); c.arc(56, -56, 15 * k, 0, TAU); c.fill();
        c.strokeStyle = "#0d1a14"; c.lineWidth = 4 * k; c.lineCap = "round"; c.lineJoin = "round"; c.beginPath(); c.moveTo(56 - 7 * k, -56); c.lineTo(56 - 2 * k, -56 + 5 * k); c.lineTo(56 + 7 * k, -56 - 6 * k); c.stroke();
      }
    }
    // éclair d'allumage à la fin de la descente
    if (en < 1 && en > 0.5 && en < 0.82) { const k = seg(en, 0.5, 0.82); c.strokeStyle = col(C.white, (1 - k) * 0.85); c.lineWidth = 6 * (1 - k) + 1; c.beginPath(); c.arc(0, 0, 84 + k * 100, 0, TAU); c.stroke(); }
    // étourdi : étoiles qui tournent au-dessus de la tête
    if (stun && !dead) for (let j = 0; j < 3; j++) { const a = time * 4 + (j * TAU) / 3; c.fillStyle = col(C.lamp, 0.95); B.star(c, Math.cos(a) * 40, -112 + Math.sin(a) * 9, 7, a); }
    c.restore();
  }
};
