/* Étage 6 — Le Gouffre à Tokens : un vortex vorace, gueule de trou noir bordée de dents, cerclé d'un anneau d'accrétion
   fait de tokens qui tombent en spirale dans son gosier. Il gaspille tout : contexte renvoyé en entier, cache jamais chaud.
   Sa cible critique est l'œil de la singularité, au fond de la gueule. Moins il a de vie, moins il lui reste de tokens à avaler. */
BOSSES[6] = {
  v: 2,
  palette: { main: "#9b6bff", dark: "#140f2a", accent: "#f3b841", eye: "#ffd76a", rage: "#ff4f6d" },
  hit: { rx: 106, ry: 102, coreR: 21 },
  top: 126,
  attackFrom: { x: -50, y: 12 },
  castLean: 0,
  critLabel: "SINGULARITÉ",
  epitaph: "OPTIMISÉ",
  lines: {
    hit: ["Ma facture… elle baisse ?!", "Hé ! Je n’ai rien avalé !", "Tu as réduit mes sorties ?", "Moins de tokens ?! Sacrilège."],
    crit: ["En plein dans la singularité !", "Ma gueule ! Mon budget !", "Tu as visé le préfixe stable ?!"],
    wrong: ["Miam, 80 000 tokens de plus.", "Pas de cache ? Délicieux.", "Renvoie tout le contexte, encore !"],
    timeout: ["Le temps aussi, je l’avale.", "Chaque seconde te coûte."],
    gloat: ["Burp. C’est toi qui régales.", "Encore ! Sans cache, bien saignant.", "Ta facture vient de doubler.", "Miam. Un budget entier."],
    rage: "J’ai faim ! Envoie-moi tout, sans cache !",
    special: {
      cache: ["Un cache hit ?! Je n’ai rien eu à manger !", "Préfixe en cache… je meurs de faim.", "Trop rapide, trop économique !", "Dix fois moins cher ?! Tricheur !"]
    }
  },
  intro: {
    title: "Cache hit",
    text: "Il aspire ton temps : sa barre d’attaque se remplit plus vite qu’ailleurs. Une bonne réponse dans les premiers 40 % de la barre est un « cache hit » qui frappe deux fois plus fort."
  },
  mechanics: ["tokens"],

  weakSpot: () => ({ x: 0, y: 12 }),

  /* Projectile : un paquet de tokens recrachés, collés dans leur bave. */
  shot: {
    color: "#f3b841", spin: 7,
    draw(c, s) {
      const B = BOSSES[6], hot = s && s.rage, goo = hot ? "#ff4f6d" : "#9b6bff";
      c.fillStyle = col(goo, 0.9); c.beginPath(); c.arc(-3, 2, 14, 0, 6.2832); c.arc(9, -5, 9, 0, 6.2832); c.arc(7, 9, 8, 0, 6.2832); c.fill();
      c.fillStyle = col(mixv(goo, C.white, 0.5), 0.8); c.beginPath(); c.arc(-9, -5, 3.5, 0, 6.2832); c.fill();
      B.coin(c, -5, 1, 9.5, 0.3, "#f3b841", "#7a5210", 1); B.coin(c, 9, -5, 7, 1.0, "#ffd76a", "#7a5210", 1); B.coin(c, 6, 9, 6, 0.6, "#f3b841", "#7a5210", 1);
    }
  },

  /* Précession lente d'un astre lourd ; en rage, il se penche vers le joueur et tangue plus fort. */
  motion(b) {
    const t = b.t || 0, r = b.rageT || 0;
    return { x: -6 + Math.sin(t * 0.37) * 16 - r * 46 + r * Math.sin(t * 1.3) * 14, y: Math.sin(t * 0.53) * 14 + Math.cos(t * 0.29) * 8 + r * (10 + Math.sin(t * 1.9) * 10) };
  },

  init(b) { if (b.own) { b.own.spin = 0; b.own.ring = 0; } },
  update(b, dt) {
    const o = b.own; if (!o) return;
    const A = atkPose(b), k = (b.stun || 0) > 0 ? 0.2 : 1;
    const boost = 1 + (b.rageT || 0) * 0.9 + A.wind * (1 - A.strike) * 2.4 + ((b.cast ?? -1) >= 0 ? 2.2 : 0) + (b.flash || 0) * 1.5;
    o.spin = ((o.spin || 0) + dt * 0.95 * boost * k) % 6283.1853;
    o.ring = ((o.ring || 0) + dt * 0.7 * boost * k) % 6283.1853;
  },

  /* ------------------------------------------------------------ Décor : la Salle des Machines ------------------------------------------------------------ */
  lay(env) {
    const W = env.W, G = env.groundY;
    return { W, G, leak: { x: W * 0.405, y: G - 236 }, fan: { x: W * 0.87, y: G - 88, r: 25 }, deck: G - 122 };
  },
  backdrop(c, env) {
    const B = BOSSES[6], L = B.lay(env), W = L.W, G = L.G, rnd = env.rnd || seeded(6);
    const iron = "#12172e", iron2 = "#1b2242", edge = "rgba(125,145,210,0.32)", copper = "#4a3230", copperHi = "rgba(214,138,84,0.5)";
    c.lineCap = "round"; c.lineJoin = "round";
    // tuyau horizontal : corps, reflet, brides
    const pipeH = (x0, x1, y, th, body, hi) => {
      c.fillStyle = body; c.fillRect(x0, y, x1 - x0, th); c.fillStyle = hi; c.fillRect(x0, y + th * 0.18, x1 - x0, Math.max(1.5, th * 0.12));
      c.fillStyle = "rgba(4,6,16,0.35)"; c.fillRect(x0, y + th * 0.72, x1 - x0, th * 0.28);
    };
    const pipeV = (x, y0, y1, th, body, hi) => {
      c.fillStyle = body; c.fillRect(x, y0, th, y1 - y0); c.fillStyle = hi; c.fillRect(x + th * 0.18, y0, Math.max(1.5, th * 0.12), y1 - y0);
      c.fillStyle = "rgba(4,6,16,0.35)"; c.fillRect(x + th * 0.72, y0, th * 0.28, y1 - y0);
    };
    const flangeV = (x, y, th) => { c.fillStyle = iron2; c.fillRect(x - 4, y - 3, 8, th + 6); c.fillStyle = edge; c.fillRect(x - 4, y - 3, 1.5, th + 6); };
    const flangeH = (x, y, th) => { c.fillStyle = iron2; c.fillRect(x - 3, y - 4, th + 6, 8); c.fillStyle = edge; c.fillRect(x - 3, y - 4, th + 6, 1.5); };
    const wheel = (x, y, r) => {
      c.strokeStyle = "#c2473d"; c.lineWidth = 3.5; c.beginPath(); c.arc(x, y, r, 0, 6.2832); c.stroke();
      c.lineWidth = 2; c.beginPath(); for (let i = 0; i < 3; i++) { const a = i * 1.047 + 0.4; c.moveTo(x - Math.cos(a) * r, y - Math.sin(a) * r); c.lineTo(x + Math.cos(a) * r, y + Math.sin(a) * r); } c.stroke();
      c.fillStyle = "#e8705f"; c.beginPath(); c.arc(x, y, 3, 0, 6.2832); c.fill();
    };

    // conduites du plafond : elles passent devant la lune et encadrent la salle
    pipeH(-10, W + 10, 16, 22, iron2, "rgba(125,145,210,0.22)");
    pipeH(W * 0.2, W + 10, 46, 9, copper, copperHi);
    for (let x = W * 0.08; x < W; x += W * 0.21) { flangeV(x, 16, 22); c.fillStyle = iron; c.fillRect(x - 2, -4, 4, 20); }
    wheel(W * 0.56, 27, 11);
    pipeV(W - 24, 38, G - 40, 16, iron2, "rgba(125,145,210,0.2)");
    for (let y = 120; y < G - 80; y += 150) flangeH(W - 24, y, 16);

    // chaudière : cuve rivetée, dôme, manomètre dans le rouge, foyer qui rougeoie
    const bx = W * 0.025, bw = 132, bt = G - 292;
    pipeV(bx + bw * 0.5 - 13, -10, bt - 10, 26, iron2, "rgba(125,145,210,0.2)");
    flangeH(bx + bw * 0.5 - 13, bt - 34, 26);
    const bg = c.createLinearGradient(bx, 0, bx + bw, 0); bg.addColorStop(0, "#161c38"); bg.addColorStop(0.3, "#232b54"); bg.addColorStop(1, "#0f1328");
    c.fillStyle = bg; c.beginPath(); c.moveTo(bx, G - 40); c.lineTo(bx, bt + 30); c.quadraticCurveTo(bx, bt - 12, bx + bw / 2, bt - 12); c.quadraticCurveTo(bx + bw, bt - 12, bx + bw, bt + 30); c.lineTo(bx + bw, G - 40); c.closePath(); c.fill();
    c.strokeStyle = edge; c.lineWidth = 1.5; c.stroke();
    for (const y of [bt + 34, bt + 116, bt + 198]) {
      c.fillStyle = "rgba(6,8,20,0.45)"; c.fillRect(bx, y, bw, 9); c.fillStyle = "rgba(150,170,230,0.5)";
      for (let x = bx + 9; x < bx + bw - 4; x += 15) { c.beginPath(); c.arc(x, y + 4.5, 1.7, 0, 6.2832); c.fill(); }
    }
    const gx = bx + bw * 0.5, gy = bt + 76;
    c.fillStyle = "#0b0e1e"; c.beginPath(); c.arc(gx, gy, 25, 0, 6.2832); c.fill(); c.strokeStyle = copperHi; c.lineWidth = 2.5; c.stroke();
    c.fillStyle = "rgba(240,232,205,0.86)"; c.beginPath(); c.arc(gx, gy, 20, 0, 6.2832); c.fill();
    c.lineCap = "butt"; c.lineWidth = 4;
    c.strokeStyle = col(C.ok, 0.9); c.beginPath(); c.arc(gx, gy, 15, Math.PI * 0.8, Math.PI * 1.45); c.stroke();
    c.strokeStyle = col(C.lamp, 0.95); c.beginPath(); c.arc(gx, gy, 15, Math.PI * 1.45, Math.PI * 1.85); c.stroke();
    c.strokeStyle = col(C.bad, 0.95); c.beginPath(); c.arc(gx, gy, 15, Math.PI * 1.85, Math.PI * 2.2); c.stroke();
    c.lineCap = "round"; c.strokeStyle = "#141230"; c.lineWidth = 2.4; c.beginPath(); c.moveTo(gx, gy); c.lineTo(gx + 15, gy - 5); c.stroke();
    c.fillStyle = "#141230"; c.beginPath(); c.arc(gx, gy, 3, 0, 6.2832); c.fill();
    const fg = c.createRadialGradient(bx + 34, G - 104, 2, bx + 34, G - 104, 62); fg.addColorStop(0, "rgba(255,150,70,0.5)"); fg.addColorStop(1, "rgba(255,150,70,0)");
    c.fillStyle = fg; c.fillRect(bx - 30, G - 170, 130, 130);
    rr(c, bx + 14, G - 124, 40, 40, 6); c.fillStyle = "#0b0e1e"; c.fill(); c.strokeStyle = copperHi; c.lineWidth = 2; c.stroke();
    c.fillStyle = "#ff9a4a"; for (let i = 0; i < 4; i++) c.fillRect(bx + 20, G - 117 + i * 8, 28, 3.5);
    c.fillStyle = col(C.bad, 0.9); c.beginPath(); c.arc(bx + bw - 16, bt + 16, 4, 0, 6.2832); c.fill();

    // conduite de cuivre : de la chaudière à un coude qui fuit, vanne rouge au milieu
    const py = L.leak.y, ex = L.leak.x;
    pipeH(bx + bw, ex, py, 16, copper, copperHi); pipeV(ex - 16, py, G - 40, 16, copper, copperHi);
    c.fillStyle = copper; c.beginPath(); c.arc(ex - 16, py + 16, 16, -Math.PI / 2, 0); c.lineTo(ex - 16, py + 16); c.closePath(); c.fill();
    flangeV(bx + bw + 26, py, 16); flangeV(ex - 34, py, 16); flangeH(ex - 16, py + 34, 16); flangeH(ex - 16, G - 150, 16);
    c.fillStyle = iron2; c.fillRect(W * 0.29 - 3, py - 16, 6, 18); wheel(W * 0.29, py - 22, 14);
    // pompe au pied du coude, avec son petit cadran
    rr(c, W * 0.25, G - 112, 86, 72, 7); c.fillStyle = iron2; c.fill(); c.strokeStyle = edge; c.lineWidth = 1.4; c.stroke();
    c.fillStyle = "rgba(240,232,205,0.8)"; c.beginPath(); c.arc(W * 0.25 + 24, G - 88, 12, 0, 6.2832); c.fill();
    c.strokeStyle = "#141230"; c.lineWidth = 2; c.beginPath(); c.moveTo(W * 0.25 + 24, G - 88); c.lineTo(W * 0.25 + 31, G - 95); c.stroke();
    [C.ok, C.lamp, C.bad].forEach((k, i) => { c.fillStyle = col(k, 0.85); c.fillRect(W * 0.25 + 48 + i * 11, G - 94, 7, 7); });

    // turbines sous la passerelle : un carter rond dont l'hélice tourne (ambient), un gros tambour
    const dk = L.deck, F2 = L.fan;
    c.fillStyle = iron2; c.beginPath(); c.arc(W * 0.6, G - 46, 58, Math.PI, 0); c.closePath(); c.fill(); c.strokeStyle = edge; c.lineWidth = 1.4; c.stroke();
    c.strokeStyle = "rgba(6,8,20,0.5)"; c.lineWidth = 3; for (let i = -2; i <= 2; i++) { c.beginPath(); c.moveTo(W * 0.6 + i * 22, G - 46); c.lineTo(W * 0.6 + i * 19, G - 46 - Math.sqrt(58 * 58 - i * i * 361)); c.stroke(); }
    rr(c, F2.x - 44, F2.y - 34, 88, 76, 10); c.fillStyle = iron2; c.fill(); c.strokeStyle = edge; c.lineWidth = 1.4; c.stroke();
    c.fillStyle = "#080a18"; c.beginPath(); c.arc(F2.x, F2.y, F2.r + 4, 0, 6.2832); c.fill(); c.strokeStyle = copperHi; c.lineWidth = 2.5; c.stroke();
    // passerelle : tablier, garde-corps, croisillons
    c.fillStyle = iron; c.fillRect(W * 0.47, dk, W, 6); c.fillStyle = edge; c.fillRect(W * 0.47, dk, W, 1.5);
    c.strokeStyle = "rgba(125,145,210,0.4)"; c.lineWidth = 1.6; c.beginPath();
    for (let x = W * 0.47 + 4; x < W + 10; x += 44) { c.moveTo(x, dk); c.lineTo(x, dk - 24); }
    c.moveTo(W * 0.47, dk - 24); c.lineTo(W + 10, dk - 24); c.moveTo(W * 0.47, dk - 12); c.lineTo(W + 10, dk - 12);
    c.stroke();
    c.strokeStyle = iron; c.lineWidth = 3; c.beginPath();
    for (let x = W * 0.47 + 4; x < W; x += 88) { c.moveTo(x, dk + 6); c.lineTo(x + 30, G - 40); c.moveTo(x + 30, dk + 6); c.lineTo(x, G - 40); }
    c.stroke();
    // quelques gouttes de rouille et de lumière : voyants épars
    for (let i = 0; i < 5; i++) { c.fillStyle = col(i % 2 ? C.lamp : C.bad, 0.5 + rnd() * 0.3); c.fillRect(W * (0.5 + rnd() * 0.45), dk + 14 + rnd() * 30, 3, 3); }
  },
  /* Décor animé : la vapeur du coude qui fuit, l'hélice de la turbine. */
  ambient(c, env, b) {
    const B = BOSSES[6], L = B.lay(env), time = env.time || 0, F2 = L.fan, rg = (b && b.rageT) || 0;
    for (let i = 0; i < 5; i++) {
      const u = (time * 0.33 + i / 5) % 1, r = 7 + u * 22;
      c.fillStyle = "rgba(214,222,245," + 0.26 * (1 - u) * Math.min(1, u * 6) + ")";
      c.beginPath(); c.arc(L.leak.x + 6 + u * 26 + Math.sin(time * 1.3 + i * 2.1) * 6 * u, L.leak.y - 4 - u * 74, r, 0, 6.2832); c.fill();
    }
    c.save(); c.translate(F2.x, F2.y); c.rotate(time * 2.6);
    c.fillStyle = col(mixv("#7b88b8", "#ff7a6a", rg * 0.5), 0.9);
    for (let i = 0; i < 5; i++) { c.rotate(1.2566); c.beginPath(); c.moveTo(3, -2); c.quadraticCurveTo(F2.r * 0.7, -F2.r * 0.55, F2.r, -3); c.quadraticCurveTo(F2.r * 0.6, 4, 3, 3); c.closePath(); c.fill(); }
    c.fillStyle = "#c98a55"; c.beginPath(); c.arc(0, 0, 4.5, 0, 6.2832); c.fill();
    c.restore();
  },

  /* ------------------------------------------------------------ Pièces du personnage ------------------------------------------------------------ */
  /** Un token : pièce vue de biais (flip = angle de bascule), frappée d'un T. */
  coin(c, x, y, r, flip, tint, dark, al) {
    const w = r * (0.34 + 0.66 * Math.abs(Math.cos(flip)));
    c.fillStyle = col(dark, al); c.beginPath(); c.ellipse(x + 1.2, y + 1.5, w, r, 0, 0, 6.2832); c.fill();
    c.fillStyle = col(tint, al); c.beginPath(); c.ellipse(x, y, w, r, 0, 0, 6.2832); c.fill();
    if (r > 4.2) { c.fillStyle = col(dark, al * 0.85); c.fillRect(x - w * 0.5, y - r * 0.52, w, r * 0.26); c.fillRect(x - w * 0.15, y - r * 0.52, w * 0.3, r * 1.02); }
  },
  /** Une moitié (avant ou arrière) d'un anneau d'accrétion : la bande lumineuse, les tokens qui tournent, ceux qui tombent dans la gueule. */
  ring(c, o, front) {
    const B = BOSSES[6], TAU = Math.PI * 2;
    c.save(); c.translate(o.cx, o.cy); c.rotate(o.tilt); c.scale(o.k, o.k);
    if (o.band > 0.01) {
      if (o.dash) { c.setLineDash([26, o.dash]); c.lineDashOffset = -o.spin * 50; }
      c.beginPath(); c.ellipse(0, 0, o.rx, o.ry, 0, front ? 0 : Math.PI, front ? Math.PI : TAU);
      c.strokeStyle = col(o.tint, 0.17 * o.band * (front ? 1 : 0.6)); c.lineWidth = 12; c.stroke();
      c.strokeStyle = col(o.tint, 0.8 * o.band * (front ? 1 : 0.5)); c.lineWidth = 2.2; c.stroke();
      c.setLineDash([]);
    }
    for (let i = 0; i < o.n; i++) {
      const al = Math.min(1, o.count - i); if (al <= 0) break;
      const a = i * 2.39996 + o.spin * (0.85 + (i % 3) * 0.1), s = Math.sin(a);
      if ((s >= 0) !== front) continue;
      const k = 1 + 0.045 * Math.sin(o.time * 1.7 + i * 1.3);
      B.coin(c, Math.cos(a) * o.rx * k, s * o.ry * k, (5.6 + (i % 3) * 1.2) * (1 + s * 0.22), a * 1.5 + o.time * 2 + i, o.tint, o.dark, al * (front ? 1 : 0.6) * o.alpha);
    }
    for (let i = 0; i < o.fall; i++) {
      const p = (o.time * 0.38 * o.pull + i / o.fall + i * 0.137) % 1, a = i * 1.9 + o.spin + p * p * 6.5, s = Math.sin(a);
      if ((s >= 0) !== front) continue;
      const k = 1 - Math.pow(p, 1.6) * 0.96, x = Math.cos(a) * o.rx * k, y = s * o.ry * k, al = clamp((Math.hypot(x, y) - o.mawR * 0.45) / (o.mawR * 0.6), 0, 1);
      if (al > 0.02) B.coin(c, x, y, 6.4 * (0.5 + 0.5 * k), a * 2 + i, o.tint, o.dark, al * (front ? 1 : 0.6) * o.alpha);
    }
    c.restore();
  },
  /** Le disque du vortex et ses bras spiraux, qui dépassent et font la silhouette. */
  swirl(c, o) {
    const TAU = Math.PI * 2, R = o.R, K = 7;
    const g = c.createRadialGradient(0, 0, R * 0.35, 0, 0, R);
    g.addColorStop(0, col(o.deep)); g.addColorStop(0.72, col(mixv(o.deep, o.main, 0.62))); g.addColorStop(1, col(mixv(o.main, o.lite, 0.2)));
    c.fillStyle = g; c.beginPath(); c.arc(0, 0, R, 0, TAU); c.fill();
    c.strokeStyle = col(o.lite, 0.45); c.lineWidth = 2; c.stroke();
    const edgeAt = (j, q, sgn) => { const s = q / K, a = o.spin + (j * TAU) / o.arms - s * o.sweep, r = lerp(o.r0, o.reach, s) + sgn * o.w * (1 - Math.pow(s, 1.6)); return [Math.cos(a) * r, Math.sin(a) * r]; };
    const ag = c.createRadialGradient(0, 0, R * 0.5, 0, 0, o.reach);
    ag.addColorStop(0, col(mixv(o.main, o.deep, 0.4))); ag.addColorStop(0.55, col(o.main)); ag.addColorStop(1, col(o.lite));
    c.beginPath();
    for (let j = 0; j < o.arms; j++) {
      for (let q = 0; q <= K; q++) { const p = edgeAt(j, q, 1); if (q) c.lineTo(p[0], p[1]); else c.moveTo(p[0], p[1]); }
      for (let q = K; q >= 0; q--) { const p = edgeAt(j, q, -1); c.lineTo(p[0], p[1]); }
      c.closePath();
    }
    c.fillStyle = ag; c.fill();
    c.beginPath();
    for (let j = 0; j < o.arms; j++) for (let q = 0; q <= K; q++) { const p = edgeAt(j, q, 1); if (q) c.lineTo(p[0], p[1]); else c.moveTo(p[0], p[1]); }
    c.strokeStyle = col(mixv(o.lite, C.white, 0.35), 0.85); c.lineWidth = 2.2; c.lineJoin = "round"; c.lineCap = "round"; c.stroke();
    // traînées de vitesse
    c.beginPath();
    for (let i = 0; i < 6; i++) { const r = R * (0.62 + i * 0.06), a = o.spin * 1.7 + i * 1.9; c.moveTo(Math.cos(a) * r, Math.sin(a) * r); c.arc(0, 0, r, a, a + 0.55); }
    c.strokeStyle = col(C.white, 0.2); c.lineWidth = 1.6; c.stroke();
  },
  /** La gueule : gosier noir, deux couronnes de dents, l'œil de la singularité au fond, la lèvre de lumière. */
  maw(c, o) {
    const TAU = Math.PI * 2, rx = o.rx, ry = o.ry;
    const g = c.createRadialGradient(0, 0, 2, 0, 0, rx);
    g.addColorStop(0, col(mixv("#2a1456", o.eyeC, 0.3))); g.addColorStop(0.5, "#0d0620"); g.addColorStop(1, "#040208");
    c.fillStyle = g; c.beginPath(); c.ellipse(0, 0, rx, ry, 0, 0, TAU); c.fill();
    c.strokeStyle = col(o.main, 0.4); c.lineWidth = 1.5; c.beginPath(); c.ellipse(0, 0, rx * 0.64, ry * 0.64, 0, 0, TAU); c.stroke();
    const tooth = (a, hw, base, tip) => { c.moveTo(Math.cos(a - hw) * rx * base, Math.sin(a - hw) * ry * base); c.lineTo(Math.cos(a) * rx * tip, Math.sin(a) * ry * tip); c.lineTo(Math.cos(a + hw) * rx * base, Math.sin(a + hw) * ry * base); c.closePath(); };
    c.fillStyle = col(mixv("#8573b4", C.white, o.fl)); c.beginPath();
    for (let i = 0; i < 8; i++) tooth((i / 8) * TAU + o.spin * 0.5, 0.34, 0.66, 0.66 - 0.22 * o.teeth);
    c.fill();
    // œil de la singularité : la cible critique
    if (o.eye > 0.01) {
      const er = 13.5 * o.eye * (1 + 0.07 * Math.sin(o.time * 5) + o.beat * 0.08), ery = er * (1 - o.sq * 0.62);
      const hg = c.createRadialGradient(0, 0, er * 0.5, 0, 0, er * 2.5); hg.addColorStop(0, col(o.eyeC, 0.6)); hg.addColorStop(1, col(o.eyeC, 0));
      c.fillStyle = hg; c.beginPath(); c.arc(0, 0, er * 2.5, 0, TAU); c.fill();
      const ig = c.createRadialGradient(0, 0, 1, 0, 0, er); ig.addColorStop(0, "#ffffff"); ig.addColorStop(0.45, col(o.eyeC)); ig.addColorStop(1, col(mixv(o.eyeC, "#7a2a00", 0.55)));
      c.fillStyle = ig; c.beginPath(); c.ellipse(0, 0, er, ery, 0, 0, TAU); c.fill();
      c.fillStyle = "#07030f"; c.beginPath(); c.ellipse(o.lx * 4.6, o.ly * 3, Math.max(1.2, 3 * (1 - o.sq * 0.5) * o.pupil), ery * 0.76, 0, 0, TAU); c.fill();
      c.fillStyle = "rgba(255,255,255,0.9)"; c.beginPath(); c.arc(-er * 0.38 + o.lx * 2, -ery * 0.4, er * 0.16, 0, TAU); c.fill();
    }
    // grandes dents : elles tombent une à une avec les dégâts
    c.fillStyle = col(mixv("#fff4dc", C.white, o.fl)); c.beginPath();
    for (let i = 0; i < 12; i++) {
      const gone = (o.dmg >= 2 && i === 4) || (o.dmg >= 3 && (i === 9 || i === 1)), chip = (o.dmg >= 1 && i === 4) || (o.dmg >= 2 && i === 9) || (o.dmg >= 3 && (i === 6 || i === 11));
      if (gone) continue;
      tooth((i / 12) * TAU - o.spin * 0.3, 0.25, 1.01, 1 - o.len * o.teeth * (chip ? 0.4 : i % 2 ? 0.8 : 1));
    }
    c.fill(); c.strokeStyle = "rgba(60,30,90,0.55)"; c.lineWidth = 1.2; c.stroke();
    c.save(); c.shadowColor = col(o.lip); c.shadowBlur = 12; c.strokeStyle = col(mixv(o.lip, C.white, 0.35 + o.fl * 0.5)); c.lineWidth = 3.6; c.beginPath(); c.ellipse(0, 0, rx, ry, 0, 0, TAU); c.stroke(); c.restore();
  },
  /** Un œil en amande, incliné vers le centre. Le repère local pointe vers l'extérieur du visage (sx = -1 : œil gauche). */
  eye(c, sx, o) {
    const L = 19 * o.size, H = 8.5 * o.size;
    c.save(); c.translate(sx * o.x, o.y); c.scale(sx, 1); c.rotate(-o.tilt);
    c.fillStyle = "rgba(14,7,34,0.78)"; c.beginPath(); c.moveTo(-L - 7, 3); c.quadraticCurveTo(0, -H * 2.9, L + 8, -1); c.quadraticCurveTo(0, H * 2.2, -L - 7, 3); c.fill();
    if (o.glee > 0.5) {                                                                   // ricanement : deux croissants réjouis
      c.strokeStyle = col(o.color); c.lineWidth = 5.5 * o.size; c.lineCap = "round"; c.beginPath(); c.moveTo(-L + 2, 3); c.quadraticCurveTo(0, -H * 1.9, L - 2, 3); c.stroke();
    } else {
      const op = o.open;
      c.beginPath(); c.moveTo(-L, 1); c.quadraticCurveTo(2, -H * 2.1 * op, L, -1); c.quadraticCurveTo(0, H * 1.5 * op, -L, 1); c.closePath();
      c.save(); c.shadowColor = col(o.color); c.shadowBlur = 12; c.fillStyle = col(o.color); c.fill(); c.restore();
      c.save(); c.clip();
      c.fillStyle = "rgba(255,255,255,0.55)"; c.beginPath(); c.ellipse(o.px, o.py - 1, 8.5 * o.size, 7 * o.size, 0, 0, 6.2832); c.fill();
      c.fillStyle = "#08030f"; c.beginPath(); c.ellipse(o.px, o.py, Math.max(1.4, 3.1 * o.size * o.pupil), H * 1.15, 0, 0, 6.2832); c.fill();
      c.restore();
      c.strokeStyle = col(o.ink); c.lineWidth = 6 * o.size; c.lineCap = "round";                // paupière lourde : le sourcil
      c.beginPath(); c.moveTo(-L - 5, 3 - o.brow); c.quadraticCurveTo(0, -H * 2.2 * op - 3, L + 6, -H * 0.9 - 2 - o.brow * 0.4); c.stroke();
      if (o.flame > 0.05) { c.fillStyle = col(o.color, o.flame); c.beginPath(); c.moveTo(L - 2, -H * 0.6); c.lineTo(L + 17 * o.flame, -H * 1.9); c.lineTo(L + 5, -H * 0.2); c.lineTo(L + 20 * o.flame, -H * 0.4); c.lineTo(L, 2); c.closePath(); c.fill(); }
    }
    c.restore();
  },

  /* ------------------------------------------------------------ Le personnage ------------------------------------------------------------ */
  draw(c, b) {
    const B = BOSSES[6], P = B.palette, TAU = Math.PI * 2;
    const t = b.t || 0, time = b.time == null ? t : b.time, look = b.look || { x: -1, y: 0 };
    const en = b.enter ?? 1, dying = b.dying ?? -1, dmg = b.dmg || 0, hp = clamp(b.hpFrac ?? 1, 0, 1);
    const fl = b.flash || 0, sq = b.squint || 0, rg = b.rageT || 0, beat = b.beat || 0;
    const gloat = b.gloat || 0, talk = b.talk || 0, threat = b.threat || 0, stun = (b.stun || 0) > 0;
    const A = atkPose(b), wind = easeInOut(A.wind) * (1 - easeOut(A.strike)), strike = easeOut(A.strike) * (1 - easeInOut(A.rec));
    const cast = (b.cast ?? -1) >= 0 ? clamp(b.cast / 0.9, 0, 1) : -1, castK = cast < 0 ? 0 : Math.sin(cast * Math.PI);
    const dead = dying >= 0, d = dead ? dying : 0;
    // entrée : un point de lumière, une déchirure, elle s'ouvre et se met à tourner, l'anneau et les dents arrivent
    const rip = easeOut(seg(en, 0.02, 0.3)), open = easeInOut(seg(en, 0.2, 0.6)), grow = backOut(seg(en, 0.2, 0.82)), ringIn = backOut(seg(en, 0.5, 0.94)), teethIn = backOut(seg(en, 0.58, 0.9)), eyesIn = seg(en, 0.72, 0.96);
    // mort : il déglutit de travers (0–0,12), implose (0,1–0,68), un éclair (0,6–0,8), quelques tokens dérivent
    const imp = easeIn(seg(d, 0.1, 0.68)), ringFall = easeIn(seg(d, 0.03, 0.56)), gulp = dead ? Math.sin(Math.PI * seg(d, 0, 0.16)) : 0;

    const main = mixv(mixv(P.main, P.rage, rg * 0.85), C.white, fl * 0.6), deep = mixv(mixv("#1d1042", "#3d0a20", rg), C.white, fl * 0.35), lite = mixv(mixv("#cdb8ff", "#ffb48c", rg), C.white, fl * 0.6);
    const gold = mixv(P.accent, C.white, fl * 0.6), goldDark = "#6e4a0e", eyeC = mixv(mixv(P.eye, "#ff7038", rg * 0.85), C.white, fl * 0.8), ink = mixv("#120a2a", C.white, fl * 0.4);
    const own = b.own || {};
    const spin = (own.spin != null ? own.spin : t * 0.95 * (1 + rg * 0.9)) - (1 - easeOut(seg(en, 0.15, 1))) * 9 + d * d * 46;
    const rspin = (own.ring != null ? own.ring : t * 0.7 * (1 + rg * 0.9)) + d * d * 30;

    // corps : respiration, pulsation sur le temps, inspiration (il se contracte) puis rot (il se dilate)
    const wob = dead ? 0 : (0.012 + dmg * 0.022) * Math.sin(t * (3 + dmg)) + (stun ? Math.sin(time * 9) * 0.05 : 0);
    const S = grow * (1 + Math.sin(t * 1.3) * 0.012 + beat * 0.03 - wind * 0.16 + strike * 0.15 + rg * 0.06 - threat * 0.05 + castK * 0.06 + gulp * 0.1) * (1 - imp);
    const offX = wind * 11 - strike * 17 + threat * 6 + (dmg >= 3 && !dead ? Math.sin(time * 23) * 1.5 : 0), offY = Math.sin(t * 1.3) * 3;
    const R = 90, mawR = 46 + rg * 12;
    // gueule : elle mâche sur le temps, se pince à l'inspiration, bée au rot, parle, ricane
    const chew = gloat * Math.abs(Math.sin(time * 15)) * 0.22;
    const mOpen = clamp(1 - beat * 0.05 - wind * 0.34 + strike * 0.42 + talk * 0.16 - chew - threat * 0.12 + castK * 0.25 + gulp * 0.3, 0.5, 1.6);
    const mrx = (mawR + rg * 5) * mOpen, mry = mawR * mOpen * (1 - gloat * 0.1 + talk * 0.06);
    const teethLen = clamp(0.36 + rg * 0.06 + wind * 0.2 - strike * 0.22 + threat * 0.42 + chew * 0.6, 0.1, 0.86);

    const tilt = -0.14 + Math.sin(t * 0.35) * 0.09 + wind * 0.1, ry = 58 + Math.sin(t * 0.27) * 7;
    const ringK = Math.max(0, ringIn * (1 - wind * 0.22 + strike * 0.14 + castK * 0.08) * (1 - ringFall));
    const R1 = { cx: offX, cy: 10 + offY, tilt, rx: 162, ry, k: ringK, spin: rspin, time: t, n: 16, count: 3 + 13 * hp, fall: dmg >= 3 ? 2 : dmg >= 2 ? 4 : 6, pull: 1 + wind * 2 + castK * 1.5,
      tint: gold, dark: goldDark, band: (0.55 + beat * 0.2) * (dead ? 1 - seg(d, 0.2, 0.5) : 1), dash: dmg ? 10 + dmg * 14 : 0, alpha: 1, mawR };
    const R2 = rg > 0.02 ? { cx: offX, cy: 8 + offY, tilt: 0.62 - Math.sin(t * 0.35) * 0.09, rx: 150, ry: 40, k: ringK * (0.4 + 0.6 * backOut(rg)), spin: -rspin * 1.35, time: t + 9, n: 8, count: 8, fall: 0, pull: 1,
      tint: mixv(P.rage, "#ffb070", 0.35 + fl * 0.4), dark: "#5a1024", band: rg * (1 + beat * 0.25) * (dead ? 1 - seg(d, 0.2, 0.5) : 1), dash: 0, alpha: rg, mawR } : null;

    // halo
    const lifeA = clamp(grow, 0, 1) * (1 - imp);
    if (lifeA > 0.01) {
      const hg = c.createRadialGradient(offX, offY, 40, offX, offY, 190); hg.addColorStop(0, col(main, (0.3 + beat * 0.08) * lifeA)); hg.addColorStop(1, col(main, 0));
      c.fillStyle = hg; c.beginPath(); c.arc(offX, offY, 190, 0, TAU); c.fill();
    }
    // déchirure de l'entrée : un point, puis une fente dentelée qui s'élargit
    if (en < 0.7) {
      const a = 1 - seg(en, 0.4, 0.7), w = 96 * rip, st = seg(en, 0, 0.12);
      c.save(); c.shadowColor = col(P.main); c.shadowBlur = 14; c.strokeStyle = col(mixv(P.main, C.white, 0.7), a); c.lineWidth = 3; c.lineJoin = "miter"; c.beginPath();
      for (let i = 0; i <= 10; i++) { const u = i / 10 - 0.5, y = (i % 2 ? -1 : 1) * 5 * rip * (1 - Math.abs(u) * 2) - open * 30 * (1 - 4 * u * u); if (i) c.lineTo(u * 2 * w, y); else c.moveTo(u * 2 * w, y); }
      c.stroke(); c.restore();
      c.fillStyle = col(C.white, a * st); c.beginPath(); for (let q = 0; q < 8; q++) { const an = (q * Math.PI) / 4, r = q % 2 ? 2.5 : 15 * st + 10 * rip * (1 - open); c.lineTo(Math.cos(an) * r, Math.sin(an) * r); } c.closePath(); c.fill();
    }
    // inspiration : des filets d'air (et de tokens) filent vers la gueule ; à la mort, tout y passe
    const suck = Math.max(wind, castK * 0.7, dead ? Math.sin(Math.PI * seg(d, 0.05, 0.66)) : 0);
    if (suck > 0.03) {
      c.strokeStyle = col(mixv(gold, C.white, 0.4), 0.75 * suck); c.lineWidth = 2.2; c.lineCap = "round"; c.beginPath();
      const n = dead ? 9 : 6;
      for (let i = 0; i < n; i++) {
        const u = (time * 2.4 + i * 0.37) % 1, a = dead ? (i * TAU) / n + u * 1.4 + d * 6 : Math.PI + (i - 2.5) * 0.24 + u * 0.25, r1 = lerp(dead ? 170 : 200, 62, u) * (dead ? 1 - imp * 0.8 : 1), r0 = r1 + 30 * (1 - u * 0.5);
        c.moveTo(offX + Math.cos(a - 0.12) * r0, 12 + offY + Math.sin(a - 0.12) * r0 * 0.8); c.lineTo(offX + Math.cos(a) * r1, 12 + offY + Math.sin(a) * r1 * 0.8);
      }
      c.stroke();
    }

    if (R2) B.ring(c, R2, false);
    if (ringK > 0.02) B.ring(c, R1, false);

    if (S > 0.012) {
      c.save(); c.translate(offX, offY);
      c.rotate(t * 0.6); c.scale((1 + wob) * (1 + fl * 0.06), (1 - wob) * (1 - fl * 0.06)); c.rotate(-t * 0.6);                    // tangage : l'axe de l'ovale tourne lentement
      c.scale(S, S * lerp(0.05, 1, open));
      B.swirl(c, { R, spin, arms: 4, sweep: 1.7 + rg * 0.25 + imp * 1.6, r0: 58, reach: 118 + rg * 12 + strike * 6, w: 14 - rg * 2, main, deep, lite });
      // entailles par où il fuit (stades 2 et 3)
      if (dmg >= 2) {
        const at = (a, r) => [Math.cos(a) * r, Math.sin(a) * r];
        for (const a of dmg >= 3 ? [0.95, 2.45] : [0.95]) {
          c.beginPath();
          [[-0.075, R + 2], [-0.02, R - 13], [-0.065, R - 19], [0.01, R - 38], [0.05, R - 19], [0.02, R - 12], [0.085, R + 2]].forEach(([da, r], i) => { const p = at(a + da, r); if (i) c.lineTo(p[0], p[1]); else c.moveTo(p[0], p[1]); });
          c.fillStyle = "#070410"; c.fill(); c.strokeStyle = col(gold, 0.7); c.lineWidth = 1.3; c.lineJoin = "round"; c.stroke();
        }
      }
      drawCracks(c, b, "rgba(255,226,180,0.5)", 1.5);
      // gueule
      c.save(); c.translate(0, 12);
      B.maw(c, { rx: mrx, ry: mry, len: teethLen, teeth: clamp(teethIn, 0, 1.15), spin, main, eyeC, lip: mixv(gold, P.rage, rg * 0.6), fl, sq, dmg, time, beat, lx: look.x, ly: look.y,
        eye: clamp(teethIn, 0, 1) * (stun ? 0.8 : 1), pupil: 1 - threat * 0.45 + wind * 0.3 });
      c.restore();
      // yeux en amande : ils suivent la cible, se plissent sous le coup, s'écarquillent quand on le vise
      const eo = clamp(eyesIn * (1 - sq * 0.75) * (stun ? 0.45 : 1) * (1 + threat * 0.35 + strike * 0.3 + gulp * 0.6 - wind * 0.45) * ((time % 4.3) < 0.12 ? 0.15 : 1), 0, 1.5);
      if (eyesIn > 0.01) {
        const pull = dead ? imp : 0, E = { x: lerp(41 + rg * 4, 4, pull), y: lerp(-55 - rg * 5, 8, pull), size: (1 + rg * 0.24) * (1 - pull * 0.7), tilt: 0.34 + rg * 0.14 - threat * 0.2 - gloat * 0.1 + wind * 0.08, open: eo, color: eyeC, ink,
          glee: stun ? 0 : gloat, pupil: 1 - threat * 0.4 + rg * 0.1, brow: wind * 3 - threat * 4 - gulp * 5, flame: rg * (0.8 + beat * 0.2), px: 0, py: 0 };
        for (const sx of [-1, 1]) {
          E.px = stun ? Math.cos(time * 7) * 5 : look.x * sx * 6.5; E.py = stun ? Math.sin(time * 7) * 3 : look.y * 3.2 + 1;
          B.eye(c, sx, E);
        }
      }
      c.restore();
    }

    if (ringK > 0.02) B.ring(c, R1, true);
    if (R2) B.ring(c, R2, true);

    // fuites : les tokens lui échappent goutte à goutte
    if (dmg >= 2 && !dead && en >= 1) {
      const n = dmg >= 3 ? 6 : 3;
      for (let i = 0; i < n; i++) {
        const u = (t * 0.75 + i * 0.31) % 1, left = i >= 3, x0 = left ? -66 : 54, y0 = left ? 58 : 72;
        B.coin(c, offX + x0 + (i % 3 - 1) * 7 + u * (left ? -14 : 12), offY + y0 + u * u * 96, 5.6 - u * 1.5, t * 5 + i * 2, gold, goldDark, 1 - u * u);
      }
    }
    // le rot : une onde et des postillons vers le joueur
    if (A.on && A.strike > 0 && A.rec < 1) {
      const k = clamp(A.strike * 0.4 + A.rec * 0.6, 0, 1), a = (1 - k) * 0.9;
      c.strokeStyle = col(mixv(gold, C.white, 0.5), a); c.lineCap = "round";
      for (const q of [0, 1]) { c.lineWidth = 5 - q * 2; c.beginPath(); c.ellipse(offX - 20, 12 + offY, 58 + k * 80 + q * 22, 40 + k * 44 + q * 14, 0, Math.PI - 0.62 + q * 0.12, Math.PI + 0.62 - q * 0.12); c.stroke(); }
      c.lineWidth = 2.5; c.beginPath();
      for (let i = 0; i < 4; i++) { const an = Math.PI + (i - 1.5) * 0.3, r = 70 + k * 90; c.moveTo(offX + Math.cos(an) * r, 12 + offY + Math.sin(an) * r * 0.7); c.lineTo(offX + Math.cos(an) * (r + 16), 12 + offY + Math.sin(an) * (r + 16) * 0.7); }
      c.stroke();
    }
    // mort : l'éclair de la singularité, puis quelques tokens qui dérivent, enfin économisés
    if (dead) {
      const fz = Math.sin(Math.PI * seg(d, 0.6, 0.82));
      if (fz > 0.01) {
        c.fillStyle = col(C.white, fz); c.beginPath(); c.ellipse(0, 6, 130 * fz, 2.6, 0, 0, TAU); c.fill(); c.beginPath(); c.ellipse(0, 6, 2.2, 46 * fz, 0, 0, TAU); c.fill();
        c.strokeStyle = col(lite, fz * 0.7); c.lineWidth = 2.5; c.beginPath(); c.arc(0, 6, 14 + seg(d, 0.6, 0.82) * 64, 0, TAU); c.stroke();
      }
      const dr = seg(d, 0.56, 1), fade = 1 - seg(d, 0.86, 1);
      if (dr > 0 && fade > 0) {
        for (let i = 0; i < 6; i++) { const a = i * 1.05 + 0.4, r = 10 + easeOut(dr) * (40 + (i % 3) * 22); B.coin(c, Math.cos(a) * r, 6 + Math.sin(a) * r * 0.7 + dr * dr * 16, 5.5 - (i % 2), d * 9 + i * 1.7, P.accent, goldDark, fade * Math.min(1, dr * 5)); }
        c.fillStyle = col(C.white, (1 - seg(d, 0.7, 0.92)) * 0.9); c.beginPath(); c.arc(0, 6, 3.2 * (1 - seg(d, 0.7, 0.92)), 0, TAU); c.fill();
      }
    }
    // étourdi : étoiles qui tournent au-dessus
    if (stun && !dead) {
      c.fillStyle = col(C.lamp, 0.95);
      for (let j = 0; j < 3; j++) {
        const a = time * 4 + (j * TAU) / 3, x = offX + Math.cos(a) * 40, y = -118 + Math.sin(a) * 9;
        c.beginPath(); for (let q = 0; q < 8; q++) { const an = (q * Math.PI) / 4 + a, r = q % 2 ? 2.2 : 7; c.lineTo(x + Math.cos(an) * r, y + Math.sin(an) * r); } c.closePath(); c.fill();
      }
    }
  }
};
