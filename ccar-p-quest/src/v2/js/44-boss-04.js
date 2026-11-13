/* Étage 4 — L'Hydre des Connecteurs : un bloc multiprise d'où sortent des cous de câble, chacun terminé par une tête-fiche.
   La tête principale (la grosse, verte, couronnée de broches, dressée en cobra à gauche) est la cible critique.
   Les têtes leurres (b.mech.heads.count, de 0 à 4) sont les outils inutiles qu'on lui a branchés : USB « fetch », RJ45 « sql »,
   fiche « jira » qui regarde du mauvais côté, jack « s3 ». Elles poussent hors du bloc et tombent, débranchées, quand on les coupe.
   Rage : électrisée, des arcs sautent de tête en tête, le bloc se fend et rougeoie. Mort : les têtes se débranchent une à une. */
{
  const HUB = { x: 22, y: 74, w: 148, h: 62 };              // bloc multiprise : x -52…96, y 43…105
  const MAIN = { x: -92, y: -36, rx: -32, ry: 45 };          // tête principale au repos ; racine de son cou sur le bloc
  // Têtes leurres : repos (x, y), racine du cou (rx, ry), départ du cou (ox, oy), arrivée derrière la tête (cx, cy),
  // sens (f = -1 : elle regarde à droite), inclinaison, type de fiche, étiquette d'outil.
  const DEC = [
    { x: 4, y: -98, rx: 4, ry: 45, ox: -4, oy: -56, cx: 34, cy: 26, f: 1, tilt: -0.16, kind: 0, label: "fetch" },
    { x: 86, y: -74, rx: 40, ry: 45, ox: 10, oy: -52, cx: 30, cy: 30, f: 1, tilt: -0.3, kind: 1, label: "sql" },
    { x: 120, y: 0, rx: 76, ry: 46, ox: 6, oy: -44, cx: -30, cy: 14, f: -1, tilt: 0.12, kind: 2, label: "jira" },
    { x: -120, y: 64, rx: -50, ry: 84, ox: -26, oy: 26, cx: 24, cy: 22, f: 1, tilt: 0.22, kind: 3, label: "s3" }
  ];
  const METAL = "#c9d2e6", GRAY = "#2a3042";
  const hash = (n) => { const s = Math.sin(n * 91.7 + 17.3) * 43758.5453; return s - Math.floor(s); };
  /** Point d'une courbe de Bézier cubique P = [x0, y0, c1x, c1y, c2x, c2y, x1, y1]. */
  const bz = (P, u) => { const v = 1 - u, a = v * v * v, b = 3 * v * v * u, d = 3 * v * u * u, e = u * u * u; return { x: a * P[0] + b * P[2] + d * P[4] + e * P[6], y: a * P[1] + b * P[3] + d * P[5] + e * P[7] }; };

  /** Un cou de câble : gaine, annelures, liseré où court le signal. */
  function cable(c, P, lw, jacket, rib, stripe, off) {
    c.beginPath(); c.moveTo(P[0], P[1]); c.bezierCurveTo(P[2], P[3], P[4], P[5], P[6], P[7]);
    c.lineJoin = "round"; c.lineCap = "round"; c.strokeStyle = jacket; c.lineWidth = lw; c.stroke();
    c.lineCap = "butt"; c.setLineDash([2, 6]); c.strokeStyle = rib; c.stroke();
    c.lineCap = "round"; c.setLineDash([7, 12]); c.lineDashOffset = off; c.strokeStyle = stripe; c.lineWidth = lw * 0.26; c.stroke();
    c.setLineDash([]); c.lineDashOffset = 0;
  }
  /** Blessure sur un cou : ruban isolant (bare = false) ou fils de cuivre à nu qui crachent des étincelles. */
  function wound(c, P, u, lw, bare, sparkOn) {
    const p = bz(P, u), q = bz(P, u + 0.04);
    c.save(); c.translate(p.x, p.y); c.rotate(Math.atan2(q.y - p.y, q.x - p.x));
    c.fillStyle = "#0b0e17"; c.fillRect(-5, -lw / 2 - 1, 10, lw + 2);
    if (bare) {
      c.strokeStyle = "#ffb35c"; c.lineWidth = 1.3; c.lineCap = "round"; c.beginPath();
      c.moveTo(-3, -lw / 2); c.lineTo(-8, -lw / 2 - 8); c.moveTo(-1, -lw / 2); c.lineTo(-2, -lw / 2 - 11); c.moveTo(1, -lw / 2); c.lineTo(5, -lw / 2 - 10); c.moveTo(3, -lw / 2); c.lineTo(10, -lw / 2 - 5); c.stroke();
      if (sparkOn) star(c, 1, -lw / 2 - 11, 8, "#eaffff");
    } else { c.fillStyle = "rgba(243,184,65,0.85)"; c.fillRect(-3.4, -lw / 2 - 1, 1.7, lw + 2); c.fillRect(1.6, -lw / 2 - 1, 1.7, lw + 2); }
    c.restore();
  }
  function star(c, x, y, r, color) {
    c.strokeStyle = color; c.lineWidth = 1.6; c.lineCap = "round"; c.beginPath();
    for (let k = 0; k < 4; k++) { const a = k * Math.PI / 4 + 0.3, q = k % 2 ? r * 0.55 : r; c.moveTo(x - Math.cos(a) * q, y - Math.sin(a) * q); c.lineTo(x + Math.cos(a) * q, y + Math.sin(a) * q); }
    c.stroke();
  }
  /** Trace un éclair brisé entre deux points (à peindre ensuite). */
  function bolt(c, x0, y0, x1, y1, seed, amp) {
    const dx = x1 - x0, dy = y1 - y0, L = Math.hypot(dx, dy) || 1, nx = -dy / L, ny = dx / L;
    c.beginPath(); c.moveTo(x0, y0);
    for (let i = 1; i < 6; i++) { const u = i / 6, o = (hash(seed + i * 3.3) - 0.5) * 2 * amp * Math.sin(u * Math.PI); c.lineTo(x0 + dx * u + nx * o, y0 + dy * u + ny * o); }
    c.lineTo(x1, y1);
  }

  /** Une tête-fiche, dessinée tournée vers la gauche autour de (x, y).
      o : s, f, tilt, main, kind, jaw, hood, fang, shell, jawC, dark, trim, eye, look, lid, anger, happy, deadEyes, dizzy, glow, tongue, spark, time, seed */
  function head(c, x, y, o) {
    const main = o.main, prongs = main || o.kind === 2, lw = main ? 1.5 : 1.7, ja = -o.jaw * 0.6, fg = 17 * o.fang;
    c.save(); c.translate(x, y); c.scale(o.f * o.s, o.s); c.rotate(o.tilt);
    c.lineJoin = "round"; c.lineCap = "round";
    if (main) {   // capuchon de cobra : il s'ouvre quand elle menace
      const hf = 0.72 + o.hood * 0.5;
      c.beginPath(); c.moveTo(-9, -15); c.quadraticCurveTo(6, -36 * hf, 23, -22 * hf); c.quadraticCurveTo(33, -8, 29, 0); c.quadraticCurveTo(33, 8, 23, 22 * hf); c.quadraticCurveTo(6, 36 * hf, -9, 15); c.closePath();
      c.fillStyle = col(o.dark); c.fill(); c.strokeStyle = col(o.trim, 0.9); c.lineWidth = 1.5; c.stroke();
      c.strokeStyle = col(o.trim, 0.5); c.lineWidth = 1; c.beginPath();
      for (let k = -1; k <= 1; k += 2) { c.moveTo(6, 12 * k); c.lineTo(15, 26 * hf * k); c.moveTo(12, 10 * k); c.lineTo(25, 15 * hf * k); c.moveTo(1, 14 * k); c.lineTo(4, 28 * hf * k); }
      c.stroke();
      c.fillStyle = col(o.gold); c.fillRect(-8, -22.5, 3, 6); c.fillRect(-2.5, -24.5, 3, 8); c.fillRect(3, -22.5, 3, 6);   // couronne de broches
    }
    // manchon du câble, derrière la tête
    c.fillStyle = col(o.dark); c.beginPath(); c.moveTo(18, -11); c.lineTo(32, -7); c.lineTo(32, 9); c.lineTo(18, 13); c.closePath(); c.fill();
    c.strokeStyle = "rgba(255,255,255,0.16)"; c.lineWidth = 1; c.beginPath(); for (let k = 0; k < 3; k++) { c.moveTo(23 + k * 3.2, -8.5 + k); c.lineTo(23 + k * 3.2, 10.5 - k); } c.stroke();
    // connecteur à l'avant
    if (prongs) { c.fillStyle = col(o.metal); rr(c, -21 - fg, -11.5, fg + 3, 5, 1.5); c.fill(); c.fillStyle = "rgba(10,15,26,0.5)"; c.beginPath(); c.arc(-17 - fg, -9, 1.1, 0, Math.PI * 2); c.fill(); }
    else if (o.kind === 0) { c.fillStyle = col(o.metal); rr(c, -39, -8.5, 19, 17, 2); c.fill(); c.fillStyle = "#141a2b"; c.fillRect(-37, -6, 14, 12); c.fillStyle = col(o.trim, 0.9); c.fillRect(-37, 0.5, 14, 4.5); c.fillStyle = col(o.metal); c.fillRect(-34.5, -4.5, 3, 2.6); c.fillRect(-28.5, -4.5, 3, 2.6); }
    else if (o.kind === 1) { rr(c, -37, -10, 17, 20, 2); c.fillStyle = col(mixv(o.trim, "#1c2440", 0.55)); c.fill(); c.strokeStyle = col(o.trim, 0.8); c.lineWidth = 1; c.stroke(); c.fillStyle = col(o.gold); for (let k = 0; k < 4; k++) c.fillRect(-35.2 + k * 3.5, -8, 1.9, 9); c.fillStyle = col(o.trim, 0.7); c.fillRect(-33, -14.5, 9, 5); }
    else { c.fillStyle = col(o.dark); rr(c, -26, -6.5, 6, 13, 1.5); c.fill(); c.fillStyle = col(o.metal); rr(c, -43, -3.2, 20, 6.4, 3.2); c.fill(); c.fillStyle = "#141a2b"; c.fillRect(-37, -3.2, 1.7, 6.4); c.fillRect(-32, -3.2, 1.7, 6.4); }
    // gueule : l'intérieur, puis la mâchoire du bas qui pivote avec sa broche
    if (o.jaw > 0.04) {
      const lx = 14 + (-36) * Math.cos(ja) - (-1) * Math.sin(ja), ly = 6 + (-36) * Math.sin(ja) + (-1) * Math.cos(ja);
      c.fillStyle = "#2e0711"; c.beginPath(); c.moveTo(16, 5); c.lineTo(-22, 3); c.lineTo(lx, ly); c.closePath(); c.fill();
      if (o.tongue > 0.05) { const tl = 15 * o.tongue, ty = (5 + ly) / 2; c.strokeStyle = "#ffb35c"; c.lineWidth = 1.2; c.beginPath(); c.moveTo(-14, ty); c.lineTo(-22 - tl, ty + 1); c.lineTo(-27 - tl, ty - 2.5); c.moveTo(-22 - tl, ty + 1); c.lineTo(-27 - tl, ty + 4.5); c.stroke(); }
    }
    c.save(); c.translate(14, 6); c.rotate(ja); c.translate(-14, -6);
    if (prongs) { c.fillStyle = col(o.metal); rr(c, -21 - fg, 6.5, fg + 3, 5, 1.5); c.fill(); }
    c.beginPath(); c.moveTo(-22, 5); c.lineTo(22, 5); c.lineTo(22, 9); c.arcTo(22, 18, 13, 18, 9); c.lineTo(-13, 18); c.arcTo(-22, 18, -22, 9, 9); c.closePath();
    c.fillStyle = col(o.jawC); c.fill(); c.strokeStyle = col(o.trim, 0.95); c.lineWidth = lw; c.stroke();
    if (main) { c.fillStyle = col(o.trim, 0.95); c.font = "700 6.6px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText("MCP", 4, 12); }
    c.restore();
    // crâne
    c.beginPath(); c.moveTo(-22, 5.5); c.lineTo(-22, -9); c.arcTo(-22, -18, -13, -18, 9); c.lineTo(13, -18); c.arcTo(22, -18, 22, -9, 9); c.lineTo(22, 5.5); c.closePath();
    c.fillStyle = col(o.shell); c.fill(); c.strokeStyle = col(o.trim, 0.95); c.lineWidth = lw; c.stroke();
    rr(c, -16, -15.6, 28, 4.6, 2.3); c.fillStyle = "rgba(255,255,255,0.16)"; c.fill();
    if (!main) { c.strokeStyle = "rgba(255,255,255,0.14)"; c.lineWidth = 1.2; c.beginPath(); c.moveTo(14.5, -11); c.lineTo(14.5, 2); c.moveTo(18, -9); c.lineTo(18, 2); c.stroke(); }
    // yeux
    const E = main ? [[-11.5, -4.6, 5.3, 1], [3.6, -5.4, 6.5, -1]] : [[-10.5, -4.8, 4.9, 1], [3, -5.4, 5.9, -1]];
    for (const e of E) {
      const ex = e[0], ey = e[1], r = e[2];
      if (o.deadEyes) { c.strokeStyle = col(o.trim, 0.9); c.lineWidth = 1.6; c.beginPath(); c.moveTo(ex - r * 0.6, ey - r * 0.6); c.lineTo(ex + r * 0.6, ey + r * 0.6); c.moveTo(ex + r * 0.6, ey - r * 0.6); c.lineTo(ex - r * 0.6, ey + r * 0.6); c.stroke(); continue; }
      c.fillStyle = "#0a0f1a"; c.beginPath(); c.arc(ex, ey, r + 1.1, 0, Math.PI * 2); c.fill();
      if (o.glow > 0) { c.fillStyle = col(o.eye, 0.28 * o.glow); c.beginPath(); c.arc(ex, ey, r * 1.9, 0, Math.PI * 2); c.fill(); }
      c.fillStyle = col(o.eye); c.beginPath(); c.arc(ex, ey, r, 0, Math.PI * 2); c.fill();
      const px = ex + (o.dizzy ? Math.cos(o.time * 9 + e[3]) * r * 0.42 : clamp(o.look.x * o.f, -1, 1) * r * 0.46 + (main ? 0 : e[3] * o.derp)), py = ey + (o.dizzy ? Math.sin(o.time * 9 + e[3]) * r * 0.42 : clamp(o.look.y, -1, 1) * r * 0.36 + r * 0.12);
      c.fillStyle = "#0a0f1a"; c.beginPath();
      if (main) c.ellipse(px, py, r * (0.26 + o.wide * 0.14), r * 0.74, 0, 0, Math.PI * 2); else c.arc(px, py, r * 0.42, 0, Math.PI * 2);
      c.fill();
      c.fillStyle = "rgba(255,255,255,0.9)"; c.beginPath(); c.arc(px - r * 0.2, py - r * 0.3, r * 0.16, 0, Math.PI * 2); c.fill();
      // paupière : elle descend vers l'autre œil quand la tête est en colère, et ferme l'œil au clignement
      const up = ey - r - 1.6, shut = o.lid * 2.1 * r, dIn = r * (0.1 + 0.85 * o.anger) + shut, dOut = r * 0.05 + shut;
      c.fillStyle = col(o.shell); c.beginPath(); c.moveTo(ex - r - 1.6, up); c.lineTo(ex + r + 1.6, up); c.lineTo(ex + r + 1.6, up + (e[3] > 0 ? dIn : dOut)); c.lineTo(ex - r - 1.6, up + (e[3] > 0 ? dOut : dIn)); c.closePath(); c.fill();
      if (o.happy > 0.1) { c.beginPath(); c.ellipse(ex, ey + r * 1.5, r * 1.3, r * (0.45 + 0.75 * o.happy), 0, 0, Math.PI * 2); c.fill(); }
    }
    if (!main && !o.deadEyes) {   // petite bouche des leurres
      c.strokeStyle = "#0a0f1a"; c.lineWidth = 1.5; c.beginPath();
      if (o.kind === 1) c.arc(-4, 10.5, 2.2 + o.jaw * 2, 0, Math.PI * 2); else if (o.kind === 3) { c.moveTo(-9, 10.5); c.lineTo(1, 10.5); } else { c.moveTo(-10, 9); c.quadraticCurveTo(-4, 14 + o.jaw * 3, 2, 9); }
      c.stroke();
    }
    // étincelle entre les deux broches quand la gueule s'ouvre
    if (o.spark > 0.05 && prongs) {
      const lx = 14 + (-36 - fg) * Math.cos(ja) - 3 * Math.sin(ja), ly = 6 + (-36 - fg) * Math.sin(ja) + 3 * Math.cos(ja), tx = -21 - fg;
      c.fillStyle = col(o.sparkC, 0.35 * o.spark); c.beginPath(); c.arc(tx - 3, (ly - 9) / 2, 5 + 9 * o.spark, 0, Math.PI * 2); c.fill();
      bolt(c, tx, -9, lx, ly, o.seed, 5); c.strokeStyle = col(o.sparkC, 0.9); c.lineWidth = 2.4; c.stroke(); c.strokeStyle = "rgba(255,255,255,0.95)"; c.lineWidth = 1; c.stroke();
    }
    c.restore();
  }

  BOSSES[4] = {
    v: 2,
    palette: { main: "#c6e84a", dark: "#1a2233", accent: "#7fe3ff", eye: "#f4ff9a", rage: "#ff7a3d" },
    hit: { rx: 150, ry: 112, coreR: 24 },
    top: 134,
    attackFrom: { x: -192, y: -16 },
    castLean: -0.08,
    critLabel: "TÊTE PRINCIPALE",
    epitaph: "DÉBRANCHÉE",
    mechanics: ["heads"],
    lines: {
      hit: ["Un outil de moins…", "Ma sélection d’outils !", "Grr, tu filtres trop bien."],
      crit: ["Ma tête principale ?!", "Pas le port central !"],
      wrong: ["Encore un outil pour moi !", "Charge tout, on verra bien.", "Plus de contexte, plus de chaos."],
      timeout: ["Je cherche encore parmi mes 140 outils…", "Trop lent, je me branche ailleurs."],
      gloat: ["Mordu ! Par quelle tête, déjà ?", "140 outils, tous pour toi.", "Tsss… mauvais connecteur."],
      rage: "Branchez-moi TOUS les serveurs MCP !",
      special: {
        grow: ["Une tête de plus ! Un outil de plus !", "Je repousse, tu vois ?", "Encore un connecteur, gratuit !"],
        cut: ["Ma tête… tu l’as débranchée !", "Allowlist ?! Non !", "Tool search… quelle horreur."]
      }
    },
    intro: {
      title: "Têtes leurres",
      text: "Chaque erreur lui fait pousser une tête de connecteur inutile : un tir sur un leurre ne peut pas être critique et sa barre d’attaque accélère. Chaque bonne réponse en débranche une : vise la tête principale, la grosse tête verte couronnée de broches."
    },

    /* Têtes leurres : b.own.g[i] va de 0 à 1 quand la tête i pousse, et retombe à 0 quand elle est coupée. */
    init(b) { if (b.own) b.own.g = null; },
    update(b, dt) {
      if (!b.own) return;
      const n = b.mech && b.mech.heads ? b.mech.heads.count : 1;
      const g = b.own.g || (b.own.g = DEC.map((_, i) => (i < n ? 1 : 0)));
      for (let i = 0; i < g.length; i++) g[i] = i < n ? Math.min(1, g[i] + dt * 2.4) : Math.max(0, g[i] - dt * 2);
    },
    /* Tête principale : elle ondule, se cabre à l'armement puis frappe vers la gauche comme un cobra. */
    mainHead(b) {
      const t = b.t || 0, time = b.time == null ? t : b.time, A = atkPose(b), as = easeOut(A.strike), back = easeOut(A.wind) * (1 - as), fwd = as * (1 - easeInOut(A.rec));
      const rg = b.rageT || 0, th = b.threat || 0, gl = b.gloat || 0, st = (b.stun || 0) > 0 ? 1 : 0;
      return {
        x: MAIN.x + Math.sin(t * 1.3) * 6 + 30 * back - 62 * fwd + 9 * th - 4 * rg,
        y: MAIN.y + Math.sin(t * 1.7 + 1) * 5 - 22 * back + 18 * fwd - 5 * th - 6 * rg - gl * Math.abs(Math.sin(time * 15)) * 6 + st * 11,
        back, fwd
      };
    },
    weakSpot(b) { const m = BOSSES[4].mainHead(b); return { x: m.x, y: m.y }; },
    headLocal(i, count, b) {
      const D = DEC[i % DEC.length], t = b.t || 0, amp = 7 + 4 * (b.rageT || 0);
      return { x: D.x + Math.sin(t * 1.5 + i * 1.9) * amp, y: D.y + Math.cos(t * 1.2 + i * 1.3) * amp * 0.8 };
    },

    /* Déplacement : le corps se balance en huit ; en rage il louvoie en plus, vite. */
    motion(b) {
      const t = b.t || 0, r = b.rageT || 0;
      return { x: Math.sin(t * 0.62) * 16 - 6 + r * Math.sin(t * 1.9 + 1) * 13, y: Math.sin(t * 1.24) * 9 + r * Math.cos(t * 2.7) * 8 };
    },

    /* Projectile : un éclair craché par la tête principale. */
    shot: {
      color: "#bdf3ff",
      draw(c, s) {
        const hot = s.rage ? "#ff9a4d" : "#7fe3ff", f = Math.floor(s.t * 40);
        c.strokeStyle = col(hot, 0.85); c.lineWidth = 1.6; c.lineCap = "round"; c.beginPath();
        for (let k = 0; k < 4; k++) { const a = hash(f * 1.3 + k) * 6.28, r0 = 15 + hash(f + k * 7) * 8; c.moveTo(Math.cos(a) * r0 - 4, Math.sin(a) * r0); c.lineTo(Math.cos(a) * (r0 + 7) - 4, Math.sin(a) * (r0 + 7)); }
        c.stroke();
        c.save(); c.shadowColor = hot; c.shadowBlur = 14;
        c.beginPath(); c.moveTo(-26, 1); c.lineTo(-26, -9); c.lineTo(-5, -3); c.lineTo(-6, -12); c.lineTo(27, 5); c.lineTo(3, 0); c.lineTo(4, 9); c.closePath();
        c.fillStyle = s.rage ? "#fff0d0" : "#fbffe6"; c.fill(); c.restore();
        c.strokeStyle = hot; c.lineWidth = 2; c.lineJoin = "round"; c.stroke();
      }
    },

    /* Décor : le Réseau des Connecteurs. Pylônes et caténaires au-dessus, paraboles à gauche, baie de serveurs à droite. */
    net(env) {
      const W = env.W, gy = env.groundY;
      const A = { x: W * 0.07, top: gy - 470, base: 50, a1: 30, a2: 22 }, Bp = { x: W * 0.385, top: gy - 430, base: 36, a1: 22, a2: 16 }, Cp = { x: W * 1.02, top: gy - 500, base: 56, a1: 34, a2: 26 };
      return {
        pylons: [A, Bp, Cp],
        // caténaires : [x0, y0, x1, y1, flèche]
        wires: [
          [A.x + A.a1, A.top + 26, Bp.x - Bp.a1, Bp.top + 26, 34], [Bp.x + Bp.a1, Bp.top + 26, Cp.x - Cp.a1, Cp.top + 26, 44],
          [A.x + A.a2, A.top + 56, Bp.x - Bp.a2, Bp.top + 56, 32], [Bp.x + Bp.a2, Bp.top + 56, Cp.x - Cp.a2, Cp.top + 56, 46],
          [Bp.x + 10, gy - 196, W * 0.865, gy - 158, 46], [A.x + 12, gy - 214, W * 0.245, gy - 172, 22], [-12, A.top + 6, A.x - A.a1, A.top + 26, 10]
        ]
      };
    },
    backdrop(c, env) {
      const W = env.W, gy = env.groundY, N = BOSSES[4].net(env), line = "#2e3d68", dim = "#222e52";
      c.lineCap = "round"; c.lineJoin = "round";
      // caténaires
      for (const w of N.wires) { c.strokeStyle = "rgba(70,90,145,0.75)"; c.lineWidth = 1.4; c.beginPath(); c.moveTo(w[0], w[1]); c.quadraticCurveTo((w[0] + w[2]) / 2, (w[1] + w[3]) / 2 + 2 * w[4], w[2], w[3]); c.stroke(); }
      // pylônes en treillis
      N.pylons.forEach((p, k) => {
        const far = k === 1, h = gy - 40 - p.top, n = Math.round(h / (far ? 46 : 52));
        c.strokeStyle = far ? dim : line; c.lineWidth = far ? 1.6 : 2.2;
        const half = (q) => lerp(4, p.base / 2, q * q * 0.6 + q * 0.4);
        c.beginPath(); c.moveTo(p.x - half(1), gy - 40); c.lineTo(p.x - 4, p.top); c.lineTo(p.x + 4, p.top); c.lineTo(p.x + half(1), gy - 40);
        for (let i = 0; i < n; i++) { const q0 = i / n, q1 = (i + 1) / n, y0 = p.top + h * q0, y1 = p.top + h * q1; c.moveTo(p.x - half(q0), y0); c.lineTo(p.x + half(q1), y1); c.moveTo(p.x + half(q0), y0); c.lineTo(p.x - half(q1), y1); c.moveTo(p.x - half(q1), y1); c.lineTo(p.x + half(q1), y1); }
        c.stroke();
        c.lineWidth = far ? 2 : 2.6; c.beginPath(); c.moveTo(p.x - p.a1 - 4, p.top + 16); c.lineTo(p.x + p.a1 + 4, p.top + 16); c.moveTo(p.x - p.a2 - 4, p.top + 46); c.lineTo(p.x + p.a2 + 4, p.top + 46); c.moveTo(p.x, p.top); c.lineTo(p.x, p.top - 14); c.stroke();
        c.fillStyle = "#4a5d96"; for (const a of [[p.a1, 16], [p.a2, 46]]) for (const sgn of [-1, 1]) { c.fillRect(p.x + sgn * a[0] - 1.5, p.top + a[1], 3, 10); c.beginPath(); c.arc(p.x + sgn * a[0], p.top + a[1] + 10, 2.6, 0, Math.PI * 2); c.fill(); }
        c.fillStyle = "rgba(239,107,92,0.9)"; c.beginPath(); c.arc(p.x, p.top - 15, 2.6, 0, Math.PI * 2); c.fill();
      });
      // boîtiers de jonction sur les pylônes
      const box = (x, y, w, h) => { rr(c, x, y, w, h, 3); c.fillStyle = "#1c2748"; c.fill(); c.strokeStyle = line; c.lineWidth = 1.5; c.stroke(); c.fillStyle = "rgba(87,196,143,0.9)"; c.beginPath(); c.arc(x + w - 5, y + 6, 2, 0, Math.PI * 2); c.fill(); c.fillStyle = "rgba(255,255,255,0.1)"; c.fillRect(x + 4, y + h - 9, w - 8, 2); c.fillRect(x + 4, y + h - 5, w - 8, 2); };
      box(N.pylons[0].x - 2, gy - 232, 24, 32); box(N.pylons[1].x - 3, gy - 212, 20, 28);
      // paraboles
      const dish = (x, y, r, rot) => {
        c.strokeStyle = line; c.lineWidth = 3; c.beginPath(); c.moveTo(x, gy - 40); c.lineTo(x, y); c.stroke();
        c.save(); c.translate(x, y); c.rotate(rot);
        c.beginPath(); c.moveTo(-r, 0); c.quadraticCurveTo(0, r * 1.05, r, 0); c.quadraticCurveTo(0, r * 0.38, -r, 0); c.closePath(); c.fillStyle = "#33426f"; c.fill(); c.strokeStyle = "#4a5d96"; c.lineWidth = 1.4; c.stroke();
        c.beginPath(); c.moveTo(-r * 0.5, r * 0.3); c.lineTo(0, -r * 0.62); c.lineTo(r * 0.5, r * 0.3); c.stroke(); c.fillStyle = "rgba(127,227,255,0.85)"; c.beginPath(); c.arc(0, -r * 0.64, 3, 0, Math.PI * 2); c.fill();
        c.restore();
      };
      dish(W * 0.245, gy - 176, 30, 0.62); dish(W * 0.315, gy - 122, 19, -0.5);
      // baie de serveurs
      const sx = W * 0.855, sw = W * 0.118, sy = gy - 166;
      rr(c, sx - 34, gy - 126, 30, 100, 3); c.fillStyle = "#151d36"; c.fill(); c.strokeStyle = dim; c.lineWidth = 1.5; c.stroke();
      c.fillStyle = "rgba(243,184,65,0.7)"; c.fillRect(sx - 28, gy - 116, 3, 3); c.fillStyle = "rgba(87,196,143,0.8)"; c.fillRect(sx - 22, gy - 116, 3, 3);
      rr(c, sx, sy, sw, 140, 4); c.fillStyle = "#172039"; c.fill(); c.strokeStyle = line; c.lineWidth = 2; c.stroke();
      for (let k = 0; k < 4; k++) {
        const y = sy + 9 + k * 23; rr(c, sx + 6, y, sw - 12, 17, 2); c.fillStyle = "#202b4d"; c.fill();
        c.fillStyle = "rgba(255,255,255,0.08)"; for (let q = 0; q < 4; q++) c.fillRect(sx + sw - 34 + q * 6, y + 4, 3, 9);
        for (let q = 0; q < 3; q++) { c.fillStyle = (k * 3 + q) % 4 === 1 ? "rgba(243,184,65,0.9)" : (k + q) % 5 === 0 ? "rgba(239,107,92,0.9)" : "rgba(87,196,143,0.9)"; c.fillRect(sx + 11 + q * 7, y + 6.5, 4, 4); }
      }
      c.strokeStyle = "rgba(70,90,145,0.9)"; c.lineWidth = 2.2; c.beginPath(); c.moveTo(sx + 8, sy); c.lineTo(sx + 8, sy - 8); c.moveTo(sx + sw * 0.5, sy); c.quadraticCurveTo(sx + sw * 0.5, sy - 22, sx - 19, gy - 126); c.stroke();
    },
    /* Décor animé : des impulsions lumineuses courent le long des caténaires. */
    ambient(c, env, b) {
      const N = BOSSES[4].net(env).wires, time = env.time || (b && b.time) || 0, hot = b && b.rage ? "#ffb070" : "#7fe3ff";
      for (let k = 0; k < 5; k++) {
        const w = N[k], q = (time * (0.11 + k * 0.023) + k * 0.37) % 1, u = k % 2 ? 1 - q : q, x = lerp(w[0], w[2], u), y = lerp(w[1], w[3], u) + 4 * u * (1 - u) * w[4], a = Math.sin(q * Math.PI);
        c.fillStyle = col(hot, 0.22 * a); c.beginPath(); c.arc(x, y, 7, 0, Math.PI * 2); c.fill();
        c.fillStyle = col("#f2ffff", 0.95 * a); c.beginPath(); c.arc(x, y, 2.1, 0, Math.PI * 2); c.fill();
      }
    },

    draw(c, b) {
      const B = BOSSES[4], P = B.palette;
      const t = b.t || 0, time = b.time == null ? t : b.time, look0 = b.look || { x: -1, y: 0 };
      const enter = b.enter ?? 1, dying = b.dying ?? -1, dmg = b.dmg || 0;
      const fl = b.flash || 0, sq = b.squint || 0, beat = b.beat || 0, threat = b.threat || 0, gloat = b.gloat || 0, talk = b.talk || 0;
      const stun = (b.stun || 0) > 0, cp = b.cast != null && b.cast >= 0 ? clamp(b.cast / 0.9, 0, 1) : -1, castK = cp >= 0 ? Math.sin(cp * Math.PI) : 0;
      const dead = dying >= 0, d = dead ? clamp(dying, 0, 1) : 0;
      if (enter <= 0.002 || d >= 0.998) return;
      const rg = (b.rageT || 0) * (1 - seg(d, 0.05, 0.45)), step = Math.floor(time * 14);
      const n = b.mech && b.mech.heads ? b.mech.heads.count : 1, G = b.own && b.own.g;
      const M = B.mainHead(b), back = M.back, fwd = M.fwd;
      const panic = dead && d < 0.42;     // elle voit ses têtes tomber
      const look = panic ? { x: Math.sin(d * 55) * 0.9, y: 0.5 } : look0;

      const wh = (cl, a) => mixv(cl, C.white, fl * a), gz = (cl, k) => mixv(cl, GRAY, k * 0.8);
      const mainC = mixv(P.main, P.rage, rg), trim = wh(mainC, 0.6), accent = wh(mixv(P.accent, "#ffc27a", rg * 0.7), 0.6);
      const skull = wh(mixv(mixv(P.main, "#17202e", 0.52), mixv(P.rage, "#1f1018", 0.5), rg), 0.65);
      const jawC = wh(mixv(mixv(P.main, "#17202e", 0.66), mixv(P.rage, "#1f1018", 0.64), rg), 0.65);
      const hoodC = wh(mixv(mixv(P.main, "#131a28", 0.8), mixv(P.rage, "#190d14", 0.74), rg), 0.5);
      const eyeM = wh(mixv(P.eye, "#ff4a36", rg * 0.85), 1), eyeD = wh(mixv("#c9f6ff", "#ffcf8a", rg), 1);
      const decShell = wh("#36456f", 0.65), decJaw = wh("#2b3759", 0.65), decDark = wh("#1d2540", 0.5), decTrim = accent;
      const metal = wh(METAL, 0.8), gold = wh("#ffd66b", 0.6);

      c.save();
      c.scale(1 + fl * 0.06, 1 - fl * 0.07);
      c.lineCap = "round"; c.lineJoin = "round";

      // halo
      const hr = 228 * easeOut(seg(enter, 0, 0.35)) * (1 - seg(d, 0.5, 0.95));
      if (hr > 6) { const g = c.createRadialGradient(0, 10, 16, 0, 10, hr); g.addColorStop(0, col(mainC, 0.16 + rg * 0.08 + beat * 0.03)); g.addColorStop(1, col(mainC, 0)); c.fillStyle = g; c.fillRect(-hr, 10 - hr, hr * 2, hr * 2); }

      // ---------- Poses : chaque tête sort du bloc (ext), puis tombe quand on la débranche (fall) ----------
      const hubIn = backOut(seg(enter, 0, 0.22)), hubGray = seg(d, 0.55, 0.8), sink = easeIn(seg(d, 0.72, 1)), hubA = 1 - seg(d, 0.84, 1);
      const hubBob = Math.sin(t * 1.4) * 2.5;
      const pose = (i) => {
        const main = i < 0, D = main ? null : DEC[i];
        let ext, fall;
        if (main) { ext = backOut(seg(enter, 0.22, 0.58)); fall = seg(d, 0.4, 0.86); }
        else {
          const alive = i < n, g = G ? G[i] : alive ? 1 : 0;
          if (!alive && g <= 0.02) return null;
          ext = backOut(seg(enter, 0.4 + 0.1 * i, 0.68 + 0.1 * i)) * (alive ? backOut(g) : 1);
          fall = dead ? seg(d, 0.03 + 0.09 * i, 0.42 + 0.09 * i) : alive ? 0 : 1 - g;
        }
        if (ext <= 0.02) return null;
        const home = main ? M : B.headLocal(i, n, b), f = main ? 1 : D.f, e1 = Math.min(1, ext), fe = easeIn(fall);
        const rx = main ? MAIN.rx : D.rx, ry = (main ? MAIN.ry : D.ry) + hubBob;
        const x = lerp(rx, home.x, ext) - f * 12 * fall, y = lerp(ry - 8, home.y, ext) + 215 * fall * fall;
        let tilt;
        if (main) tilt = -0.08 - clamp(look.y, -1, 1) * 0.13 + 0.42 * back - 0.24 * fwd + Math.sin(t * 1.1) * 0.04 + gloat * 0.22 + (stun ? 0.28 + Math.sin(time * 3) * 0.08 : 0) - threat * 0.08 + beat * 0.03 + (panic ? Math.sin(d * 70) * 0.07 : 0);
        else tilt = D.tilt + Math.sin(t * 1.3 + i * 2) * 0.1 + castK * 0.2 + gloat * 0.16 * Math.sin(time * 14 + i) + beat * 0.05 - threat * 0.1;
        tilt = tilt * e1 - 1.2 * Math.min(1, fall * 1.6);
        const s = (main ? 1.75 : 1.15) * (0.4 + 0.6 * e1);
        const hbx = x + f * s * (30 * Math.cos(tilt) - Math.sin(tilt)), hby = y + s * (30 * Math.sin(tilt) + Math.cos(tilt));
        const rX = rx + f * 5 * fe, rY = ry - 13 * Math.sin(seg(fall, 0, 0.16) * Math.PI * 0.5) + 200 * Math.max(0, fall - 0.25) ** 2;
        const k1 = e1 * (1 - fe * 0.85), k2 = e1 * (1 - fall * 0.7);
        const ox = main ? 20 + 16 * back - 10 * fwd : D.ox, oy = main ? -66 : D.oy, cx = main ? 44 - 30 * fwd : D.cx, cy = main ? -48 + 30 * fwd - 10 * back : D.cy;
        return { i, main, D, f, x, y, s, tilt, fall, ext: e1, a: (1 - seg(fall, 0.6, 1)) * seg(ext, 0.02, 0.2), gray: seg(fall, 0, 0.22), P: [rX, rY, rX + ox * k1, rY + oy * k1, hbx + cx * k2, hby + cy * k2, hbx, hby] };
      };
      const poses = [];
      for (let i = 0; i < DEC.length; i++) { const p = pose(i); if (p) poses.push(p); }
      const pm = pose(-1); if (pm) poses.push(pm);

      // ---------- Cordon d'alimentation (la queue) ----------
      const hy = HUB.y + hubBob + sink * 52, hubRot = Math.sin(t * 0.9) * 0.035 + sink * 0.22 + (stun ? Math.sin(time * 30) * 0.015 : 0), hs = hubIn * (1 - sink * 0.25);
      if (hubIn > 0.02) {
        const limp = seg(d, 0.6, 0.9), tx = HUB.x + lerp(108 + Math.sin(t * 1.2) * 7, 70, limp), ty = hy + lerp(82 + Math.cos(t * 0.9) * 5, 110, limp);
        const T = [HUB.x + 66, hy + 18, HUB.x + lerp(108, 78, limp), hy + 30, HUB.x + lerp(58 + Math.sin(t * 1.2 + 1) * 10, 70, limp), hy + 78, tx, ty];
        c.globalAlpha = hubA * hubIn;
        cable(c, T, 8, col(gz(wh("#222b45", 0.5), hubGray)), "rgba(255,255,255,0.07)", col(gz(trim, hubGray), 0.5 * (1 - hubGray)), -time * 30);
        const q = bz(T, 0.96); c.save(); c.translate(tx, ty); c.rotate(Math.atan2(ty - q.y, tx - q.x));
        c.fillStyle = col(metal); c.fillRect(8, -5.5, 9, 3); c.fillRect(8, 2.5, 9, 3); c.fillStyle = col(gz(wh("#36456f", 0.6), hubGray)); rr(c, -4, -8, 14, 16, 4); c.fill();
        c.restore(); c.globalAlpha = 1;
      }

      // ---------- Cous (derrière le bloc) ----------
      for (const p of poses) {
        const lw = p.main ? 15 : 10, jk = p.main ? wh(mixv("#33421f", "#40241a", rg), 0.5) : wh("#232c47", 0.5);
        c.globalAlpha = p.a;
        cable(c, p.P, lw * (0.5 + 0.5 * p.ext), col(gz(jk, p.gray)), p.main ? "rgba(0,0,0,0.22)" : "rgba(255,255,255,0.08)", col(gz(p.main ? trim : decTrim, p.gray), (p.main ? 0.85 : 0.6) * (1 - p.gray)), -time * (p.main ? 46 : 30) * (1 + rg));
        if (p.fall <= 0 && p.ext >= 1) {
          if (p.main) { if (dmg >= 1) wound(c, p.P, 0.34, lw, false); if (dmg >= 3) wound(c, p.P, 0.66, lw, true, hash(step * 1.3) > 0.5); }
          else if (dmg >= 2 && p.i < 2) wound(c, p.P, 0.45 + p.i * 0.12, lw, p.i === 0, hash(step * 1.7 + p.i) > 0.55);
        }
        if (!p.main && p.ext > 0.85) {   // étiquette d'outil accrochée au cou
          const q = bz(p.P, 0.6);
          c.save(); c.translate(q.x, q.y + 3); c.rotate(Math.sin(t * 1.6 + p.i) * 0.12 + p.fall);
          c.strokeStyle = "rgba(232,236,246,0.6)"; c.lineWidth = 1; c.beginPath(); c.moveTo(0, -3); c.lineTo(0, 5); c.stroke();
          rr(c, -15, 5, 30, 12, 2.5); c.fillStyle = col(gz(wh("#e8ecf6", 1), p.gray * 0.7), 0.92); c.fill();
          c.fillStyle = "#141b2d"; c.font = "700 8.5px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText(p.D.label, 0, 11.5);
          c.restore();
        }
        if ((p.fall > 0.01 && p.fall < 0.3) || (p.ext > 0.05 && p.ext < 0.6 && enter < 1)) star(c, p.P[0], p.P[1] - 6, 11 * (p.fall > 0 ? 1 - p.fall / 0.3 : 1 - p.ext), "#eaffff");   // étincelle à la prise
      }
      c.globalAlpha = 1;

      // ---------- Bloc multiprise ----------
      if (hubIn > 0.02 && hubA > 0.01) {
        const hw = HUB.w / 2, hh = HUB.h / 2, hTrim = gz(trim, hubGray), power = 1 - seg(d, 0.6, 0.7);
        c.save(); c.globalAlpha = hubA; c.translate(HUB.x, hy); c.rotate(hubRot); c.scale(hs * (1 + beat * 0.015 + castK * 0.04), hs * (1 + beat * 0.015 + castK * 0.04));
        const g = c.createLinearGradient(0, -hh, 0, hh); g.addColorStop(0, col(gz(wh(mixv("#3d4a70", "#59363a", rg * 0.7), 0.65), hubGray))); g.addColorStop(1, col(gz(wh(mixv("#222b47", "#2c1a24", rg * 0.7), 0.65), hubGray)));
        rr(c, -hw, -hh, HUB.w, HUB.h, 15); c.fillStyle = g; c.fill(); c.strokeStyle = col(hTrim, 0.9); c.lineWidth = 2.5; c.stroke();
        rr(c, -hw + 5, -hh + 4, HUB.w - 10, 10, 5); c.fillStyle = "rgba(255,255,255,0.1)"; c.fill();
        if (rg > 0.02) {   // le bloc se fend et rougeoie de l'intérieur
          const gl = 0.7 + 0.3 * Math.sin(time * 9), rgc = c.createRadialGradient(0, 4, 4, 0, 4, 70); rgc.addColorStop(0, col(P.rage, 0.5 * rg * gl)); rgc.addColorStop(1, col(P.rage, 0));
          rr(c, -hw + 2, -hh + 2, HUB.w - 4, HUB.h - 4, 13); c.fillStyle = rgc; c.fill();
          c.strokeStyle = col(mixv(P.rage, "#fff2c0", 0.55 * gl), rg); c.lineWidth = 2.6; c.beginPath();
          c.moveTo(-34, -hh + 1); c.lineTo(-26, -12); c.lineTo(-33, -2); c.lineTo(-22, 9); c.lineTo(-27, hh - 1); c.moveTo(-26, -12); c.lineTo(-12, -8);
          c.moveTo(30, -hh + 1); c.lineTo(36, -9); c.lineTo(29, 1); c.lineTo(41, 12); c.lineTo(36, hh - 1); c.moveTo(29, 1); c.lineTo(14, 5); c.stroke();
        }
        // voyants de vie
        const frac = b.hpFrac == null ? 1 - dmg * 0.28 : clamp(b.hpFrac, 0, 1), lit = dead ? Math.round(2 * (1 - seg(d, 0.2, 0.6))) : Math.ceil(frac * 6) * (enter < 1 ? seg(enter, 0.14, 0.32) : 1);
        for (let k = 0; k < 6; k++) {
          const on = k < lit, low = lit <= 2;
          c.fillStyle = on ? col(low ? mixv(C.bad, C.white, 0.2 + 0.3 * Math.sin(time * 12)) : mixv(mainC, C.white, 0.15 + beat * 0.5), 0.98) : "rgba(8,12,22,0.55)";
          c.beginPath(); c.arc(-57 + k * 10.5, -8, 3.6, 0, Math.PI * 2); c.fill();
        }
        rr(c, 6, -14, 42, 11, 3); c.fillStyle = "rgba(6,10,20,0.4)"; c.fill();
        c.fillStyle = col(hTrim, 0.8); c.font = "700 6.4px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText("140 OUTILS", 27, -8.2);
        // interrupteur : il bascule et s'éteint à la mort
        rr(c, 55, -17, 13, 21, 3); c.fillStyle = "#10151f"; c.fill();
        rr(c, 56.5, power > 0.5 ? -15.5 : -6, 10, 9.5, 2); c.fillStyle = power > 0.5 ? col(mixv(C.bad, C.white, 0.25 + 0.2 * Math.sin(time * 5) + fl * 0.5)) : "#3a2a30"; c.fill();
        // prises : deux trous et une broche de terre, comme de petits visages
        for (let k = 0; k < 4; k++) {
          const sx = -51 + k * 33, sy = 13.5, burnt = (dmg >= 1 && k === 3) || (dmg >= 2 && k === 1);
          if (burnt) { c.fillStyle = "rgba(5,6,10,0.5)"; c.beginPath(); c.ellipse(sx + 2, sy - 5, 14, 12, 0.4, 0, Math.PI * 2); c.fill(); }
          c.fillStyle = burnt ? "#07090f" : "#0d1322"; c.beginPath(); c.arc(sx, sy, 10.5, 0, Math.PI * 2); c.fill();
          c.strokeStyle = col(hTrim, burnt ? 0.2 : 0.5); c.lineWidth = 1.4; c.stroke();
          const hole = burnt ? "rgba(255,255,255,0.12)" : col(mixv(mixv(mainC, C.white, castK), GRAY, hubGray), (0.55 + 0.45 * rg + castK * 0.4) * power + 0.12);
          c.fillStyle = hole; c.beginPath(); c.arc(sx - 4.2, sy + 1, 2.1, 0, Math.PI * 2); c.arc(sx + 4.2, sy + 1, 2.1, 0, Math.PI * 2); c.fill(); c.fillRect(sx - 1.2, sy - 8, 2.4, 4.5);
        }
        if (dmg >= 3) {   // coin arraché : on voit les fils
          c.fillStyle = "#090c15"; c.beginPath(); c.moveTo(hw - 30, -hh - 2); c.lineTo(hw + 2, -hh - 2); c.lineTo(hw + 2, -hh + 22); c.lineTo(hw - 7, -hh + 15); c.lineTo(hw - 13, -hh + 20); c.lineTo(hw - 19, -hh + 9); c.lineTo(hw - 26, -hh + 11); c.closePath(); c.fill();
          c.lineWidth = 1.8; [["#ef6b5c", -8], ["#f3b841", -1], ["#7fe3ff", 6]].forEach((w, k) => { c.strokeStyle = w[0]; c.beginPath(); c.moveTo(hw - 16 + k * 4, -hh + 10); c.quadraticCurveTo(hw - 8 + w[1], -hh - 12 + Math.sin(t * 3 + k) * 2, hw - 2 + w[1], -hh - 4 - k * 3); c.stroke(); });
          if (hash(step * 2.3) > 0.6) star(c, hw - 4, -hh - 8, 9, "#eaffff");
          for (let k = 0; k < 2; k++) { const q = (t * 0.5 + k * 0.5) % 1; c.fillStyle = "rgba(190,200,225," + 0.2 * (1 - q) + ")"; c.beginPath(); c.arc(hw - 12 + Math.sin(q * 5 + k) * 6, -hh - 6 - q * 46, 5 + q * 9, 0, Math.PI * 2); c.fill(); }
        }
        // embases des cous sur le dessus (une prise vide reste sombre)
        const base = (rx, ry, on, side, k) => { const lx = rx - HUB.x, ly = ry - HUB.y; c.fillStyle = "#0a0e19"; if (side) rr(c, lx - 4, ly - 8, 8, 16, 3); else rr(c, lx - 9, ly - 3, 18, 7, 3); c.fill(); if (on) { c.fillStyle = col(k); if (side) rr(c, lx - 8, ly - 9, 9, 18, 3); else rr(c, lx - 10, ly - 9, 20, 9, 3); c.fill(); } };
        base(MAIN.rx, MAIN.ry, pm && pm.fall <= 0 && pm.ext > 0.3, false, gz(wh(mixv("#4a5d2c", "#5e3324", rg), 0.5), hubGray));
        for (let i = 0; i < DEC.length; i++) { const p = poses.find((q) => q.i === i); base(DEC[i].rx, DEC[i].ry, !!p && p.fall <= 0 && p.ext > 0.3, i === 3, gz(decDark, hubGray)); }
        c.restore();
        drawCracks(c, b, col(mixv(mainC, C.white, 0.7), 0.8 * hubA), 1.6);
        if (cp >= 0) for (let k = 0; k < 2; k++) { const q = clamp(cp * 1.4 - k * 0.3, 0, 1); if (q > 0 && q < 1) { c.strokeStyle = col(trim, (1 - q) * 0.7); c.lineWidth = 2.5; c.beginPath(); c.ellipse(HUB.x, hy, 80 + q * 70, 36 + q * 46, 0, 0, Math.PI * 2); c.stroke(); } }
      }

      // ---------- Arcs électriques de la rage : de tête en tête ----------
      if (rg > 0.3 && !dead && enter >= 1) {
        const pts = poses.map((p) => [p.x, p.y - (p.main ? 30 : 0)]); pts.push([HUB.x - 10, hy - 34]); pts.push([HUB.x + 50, hy - 30]);
        for (let q = 0; q < 2; q++) {
          const sd = step * 3.7 + q * 11; if (hash(sd) < 0.25) continue;
          const i0 = Math.floor(hash(sd + 1) * pts.length), i1 = (i0 + 1 + Math.floor(hash(sd + 2) * (pts.length - 1))) % pts.length;
          bolt(c, pts[i0][0], pts[i0][1], pts[i1][0], pts[i1][1], sd, 16);
          c.strokeStyle = col(P.rage, 0.55 * rg); c.lineWidth = 5; c.stroke(); c.strokeStyle = col("#fff6d8", 0.95 * rg); c.lineWidth = 1.6; c.stroke();
        }
      }

      // ---------- Têtes ----------
      const hiss = Math.max(0, Math.sin(t * 1.9) - 0.88) * 8;
      for (const p of poses) {
        const i = p.i, blink = (t + i * 1.31) % (3.1 + i * 0.6) < 0.12 ? 1 : 0, off = p.gray > 0.5;
        c.globalAlpha = p.a;
        if (p.main) {
          const jaw = off ? 0.25 : Math.max(talk * 0.75, back * 0.85 + fwd, gloat * (0.45 + 0.4 * Math.sin(time * 16)), castK * 0.75, hiss * 0.35, stun ? 0.22 : 0, panic ? 0.5 : 0);
          head(c, p.x, p.y, {
            main: true, kind: 2, s: p.s, f: 1, tilt: p.tilt, jaw, time, seed: step, look, derp: 0,
            hood: clamp(0.3 + rg * 0.6 + threat * 0.5 + back * 0.9 + castK * 0.5 - p.gray, 0, 1.5), fang: 1 + rg * 0.35,
            shell: gz(skull, p.gray), jawC: gz(jawC, p.gray), dark: gz(hoodC, p.gray), trim: gz(trim, p.gray), metal, gold: gz(gold, p.gray), eye: eyeM, sparkC: accent,
            lid: Math.max(blink, sq * 0.75, stun ? 0.45 : 0), anger: panic ? 0 : clamp(0.6 + rg * 0.3 + threat * 0.3 + back * 0.2 - gloat * 0.35, 0, 1), wide: panic ? 1 : back,
            happy: gloat, deadEyes: off, dizzy: stun, glow: 1 + rg * 0.8 + beat * 0.5, tongue: Math.max(hiss, gloat, castK), spark: Math.max(back, fwd * 0.8, rg * (hash(step * 0.7) > 0.5 ? jaw : 0), castK * 0.8)
          });
        } else {
          head(c, p.x, p.y, {
            main: false, kind: p.D.kind, s: p.s, f: p.f, tilt: p.tilt, jaw: Math.max(castK * 0.7, gloat * 0.6, i === 2 ? talk * 0.4 : 0), time, seed: step + i * 9, look, derp: 0.9,
            hood: 0, fang: 0.8, shell: gz(decShell, p.gray), jawC: gz(decJaw, p.gray), dark: gz(decDark, p.gray), trim: gz(decTrim, p.gray), metal, gold: gz(gold, p.gray), eye: eyeD, sparkC: accent,
            lid: Math.max(blink, sq * 0.6, stun ? 0.4 : 0, 0.12), anger: 0.12 + rg * 0.5 + threat * 0.2, wide: 0,
            happy: gloat, deadEyes: off, dizzy: stun, glow: rg, tongue: 0, spark: rg > 0.5 && hash(step + i * 5) > 0.7 ? 0.6 : 0
          });
        }
      }
      c.globalAlpha = 1;

      // étourdie : des étoiles tournent au-dessus de la tête principale
      if (stun && pm && !dead) for (let k = 0; k < 3; k++) { const a = time * 4 + (k * Math.PI * 2) / 3; star(c, pm.x - 6 + Math.cos(a) * 40, pm.y - 58 + Math.sin(a) * 9, 7, col(gold, 0.6 + 0.4 * Math.sin(a))); }
      c.restore();
    }
  };
}
