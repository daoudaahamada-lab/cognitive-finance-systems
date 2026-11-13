/* Étage 8 — La Promesse à 99,9 % : un ballon-vendeur gonflé de certitudes, contrat brillant à la main.
   Anti-pattern : promettre aux parties prenantes ce que les évaluations ne soutiennent pas.
   Tout se gonfle à partir du nœud du ballon ; le badge « 99,9 % » sur le ventre est le point faible. */
{
  const TAU = Math.PI * 2;
  const KNOT = 118;                                  // nœud du ballon (ancre du gonflage)
  const BADGE = { x: -8, y: 44 };                    // badge 99,9 % = point faible
  /* Trajectoire en zigzag de la mort, à l'intérieur de sa boîte. */
  const zipPos = (u) => { const a = easeOut(Math.min(1, u * 3)); return { x: a * (112 * Math.sin(u * 11.5 + 0.5) - 12), y: a * (74 * Math.sin(u * 16.3 + 2.2) - 10) }; };

  const drop = (c, x, y, s) => { c.beginPath(); c.moveTo(x, y - 6 * s); c.quadraticCurveTo(x + 5 * s, y + s, x, y + 4.5 * s); c.quadraticCurveTo(x - 5 * s, y + s, x, y - 6 * s); c.fill(); };
  const star4 = (c, x, y, r, rot) => { c.beginPath(); for (let i = 0; i < 8; i++) { const a = (i * Math.PI) / 4 + (rot || 0), q = i % 2 ? r * 0.3 : r; c.lineTo(x + Math.cos(a) * q, y + Math.sin(a) * q); } c.closePath(); c.fill(); };
  const patch = (c, x, y, rot, w, h) => {
    c.save(); c.translate(x, y); c.rotate(rot);
    rr(c, -w / 2, -h / 2, w, h, h / 2); c.fillStyle = "#ecc9a0"; c.fill(); c.strokeStyle = "rgba(120,78,40,0.7)"; c.lineWidth = 1.2; c.stroke();
    c.fillStyle = "#f8e6cc"; c.fillRect(-w * 0.2, -h / 2 + 1, w * 0.4, h - 2);
    c.fillStyle = "rgba(120,78,40,0.55)"; for (const sx of [-1, 1]) for (const sy of [-1, 1]) { c.beginPath(); c.arc(sx * w * 0.34, sy * h * 0.18, 0.9, 0, TAU); c.fill(); }
    c.restore();
  };

  /* Avion en papier plié dans le contrat, nez vers +x (projectile et main pendant l'armement). */
  const plane = (c, rage) => {
    c.lineJoin = "round";
    c.fillStyle = "#d8d0b8"; c.beginPath(); c.moveTo(21, 0); c.lineTo(-17, 7); c.lineTo(-9, 0.5); c.closePath(); c.fill();
    c.fillStyle = "#b5ad94"; c.beginPath(); c.moveTo(21, 0); c.lineTo(-9, 0.5); c.lineTo(-12, 11); c.closePath(); c.fill();
    c.fillStyle = rage ? "#fff0e8" : "#fffdf2"; c.beginPath(); c.moveTo(21, 0); c.lineTo(-19, -12); c.lineTo(-9, 0.5); c.closePath(); c.fill();
    c.strokeStyle = "rgba(70,56,20,0.55)"; c.lineWidth = 1; c.stroke();
    c.fillStyle = rage ? "#ff5a3c" : "#e9b93a"; c.beginPath(); c.moveTo(-19, -12); c.lineTo(-9, 0.5); c.lineTo(-5, -0.2); c.lineTo(-12.5, -9.9); c.closePath(); c.fill();
    c.strokeStyle = "rgba(27,20,5,0.45)"; c.lineWidth = 1; c.beginPath(); c.moveTo(-6, -5.6); c.lineTo(6, -2.6); c.moveTo(-3, -2.4); c.lineTo(8, -0.6); c.stroke();
    c.fillStyle = "#e0453a"; c.beginPath(); c.arc(-1, -5.2, 2.2, 0, TAU); c.fill();
  };

  /* Contrat brillant : bandeau doré, lignes, signature, sceau de cire, astérisque en tout petit. */
  const drawContract = (c, K, x, y, rot, s) => {
    if (s <= 0.02) return;
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s);
    rr(c, -23, -31, 46, 62, 3); c.fillStyle = col(K.paper); c.fill(); c.strokeStyle = col(K.goldLo, 0.9); c.lineWidth = 1.6; c.stroke();
    c.fillStyle = col(K.badge); c.fillRect(-22, -27, 44, 14);
    c.fillStyle = "#1d1408"; c.font = "800 10.5px " + F_DISPLAY; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText("SLA 99,9 %", 0, -19.5);
    c.strokeStyle = "rgba(27,20,5,0.42)"; c.lineWidth = 1.5; c.lineCap = "butt";
    for (let k = 0; k < 4; k++) { c.beginPath(); c.moveTo(-16, -6 + k * 6.3); c.lineTo(k === 3 ? 1 : 16, -6 + k * 6.3); c.stroke(); }
    c.strokeStyle = "rgba(40,54,150,0.85)"; c.lineWidth = 1.3; c.lineCap = "round"; c.beginPath(); c.moveTo(-1, 23); c.bezierCurveTo(3, 14, 6, 29, 10, 20); c.bezierCurveTo(12, 16, 15, 25, 19, 20); c.stroke();
    c.fillStyle = col(K.red); c.beginPath(); c.moveTo(-18, 21); c.lineTo(-20, 34); c.lineTo(-14.5, 30); c.lineTo(-9, 34); c.lineTo(-11, 21); c.closePath(); c.fill(); c.beginPath(); c.arc(-14.5, 19.5, 6.5, 0, TAU); c.fill();
    c.fillStyle = "rgba(255,255,255,0.4)"; c.beginPath(); c.arc(-16, 18, 2, 0, TAU); c.fill();
    c.fillStyle = "rgba(27,20,5,0.4)"; c.font = "600 4px " + F_MONO; c.textAlign = "left"; c.fillText("*sauf annexe", -3, 28);
    c.fillStyle = "rgba(255,255,255,0.55)"; c.beginPath(); c.moveTo(-22, -30); c.lineTo(-6, -30); c.lineTo(-22, -6); c.closePath(); c.fill();
    c.restore();
  };

  const hand = (c, K, x, y, r, g) => {
    c.lineCap = "round";
    if (g === "point" || g === "thumb") {
      const fx = g === "point" ? x - 2 : x + 2, fy = y - r * (g === "point" ? 2.05 : 1.7);
      c.strokeStyle = col(K.goldLo); c.lineWidth = r * 0.64 + 2.4; c.beginPath(); c.moveTo(x, y - 2); c.lineTo(fx, fy); c.stroke();
      c.strokeStyle = col(K.gold); c.lineWidth = r * 0.64; c.stroke();
    }
    c.beginPath(); c.arc(x, y, r, 0, TAU); c.fillStyle = col(K.gold); c.fill(); c.strokeStyle = col(K.goldLo); c.lineWidth = 1.6; c.stroke();
    c.fillStyle = "rgba(255,255,255,0.42)"; c.beginPath(); c.arc(x - r * 0.36, y - r * 0.4, r * 0.28, 0, TAU); c.fill();
    if (g === "fist") { c.strokeStyle = col(K.goldLo); c.lineWidth = 1.5; for (let i = -1; i <= 1; i++) { c.beginPath(); c.moveTo(x + i * r * 0.42, y - r * 0.1); c.lineTo(x + i * r * 0.42, y + r * 0.55); c.stroke(); } }
  };

  /* Bras : une manche de ballon courbe, une manchette blanche et une main dorée. Renvoie la main. */
  const arm = (c, K, sx, sy, hx, hy, bx, by, w, g) => {
    const mx = (sx + hx) / 2 + bx, my = (sy + hy) / 2 + by;
    const p = () => { c.beginPath(); c.moveTo(sx, sy); c.quadraticCurveTo(mx, my, hx, hy); };
    c.lineCap = "round"; c.lineJoin = "round";
    p(); c.strokeStyle = col(K.suitLo); c.lineWidth = w + 3; c.stroke();
    p(); c.strokeStyle = col(K.suit); c.lineWidth = w; c.stroke();
    c.save(); c.translate(-w * 0.12, -w * 0.24); p(); c.strokeStyle = col(K.suitHi, 0.6); c.lineWidth = w * 0.2; c.stroke(); c.restore();
    const dx = hx - mx, dy = hy - my, d = Math.max(1, Math.hypot(dx, dy)), ux = dx / d, uy = dy / d;
    c.lineCap = "butt"; c.strokeStyle = col(K.shirt); c.lineWidth = w * 0.86; c.beginPath(); c.moveTo(hx - ux * 3, hy - uy * 3); c.lineTo(hx + ux * 4, hy + uy * 4); c.stroke();
    hand(c, K, hx + ux * 11, hy + uy * 11, w * 0.54, g);
    return { x: hx + ux * 11, y: hy + uy * 11 };
  };

  /* Visage, en coordonnées de tête (rayon 42, tourné vers la gauche). */
  const drawFace = (c, K, F) => {
    const ink = col(K.ink);
    c.lineCap = "round"; c.lineJoin = "round";
    c.fillStyle = col(K.blush, 0.45);
    c.beginPath(); c.ellipse(-32, 9, 7.5, 4.6, 0, 0, TAU); c.fill(); c.beginPath(); c.ellipse(20, 10, 8, 4.8, 0, 0, TAU); c.fill();
    const eye = (ex, ey, rx, ry, side, shut) => {
      c.strokeStyle = ink; c.lineWidth = 2.8;
      if (F.mode === "x") { c.beginPath(); c.moveTo(ex - 5, ey - 5); c.lineTo(ex + 5, ey + 5); c.moveTo(ex + 5, ey - 5); c.lineTo(ex - 5, ey + 5); c.stroke(); return; }
      if (F.mode === "pain") { c.beginPath(); c.moveTo(ex + side * 6, ey - 6); c.lineTo(ex - side * 5, ey); c.lineTo(ex + side * 6, ey + 6); c.stroke(); return; }
      if (F.mode === "happy" || shut) { c.beginPath(); c.moveTo(ex - rx * 0.9, ey + 3); c.quadraticCurveTo(ex, ey - 8, ex + rx * 0.9, ey + 3); c.stroke(); return; }
      if (F.mode === "smug") { c.beginPath(); c.moveTo(ex - rx * 0.9, ey - 1); c.quadraticCurveTo(ex, ey + 6, ex + rx * 0.9, ey - 1); c.stroke(); return; }
      const h = ry * F.wide;
      c.beginPath(); c.ellipse(ex, ey, rx, h, 0, 0, TAU); c.fillStyle = "#ffffff"; c.fill();
      c.save(); c.clip();
      if (F.mode === "spiral") {
        c.strokeStyle = col(K.pupil); c.lineWidth = 1.8; c.beginPath();
        for (let k = 0; k <= 22; k++) { const a = k * 0.55 + F.spin * side, q = k * 0.42; if (k) c.lineTo(ex + Math.cos(a) * q, ey + Math.sin(a) * q); else c.moveTo(ex, ey); }
        c.stroke();
      } else {
        const px = ex + F.lx * rx * 0.44, py = ey + F.ly * h * 0.38;
        c.fillStyle = col(K.pupil); c.beginPath(); c.arc(px, py, F.pr, 0, TAU); c.fill();
        c.fillStyle = "#ffffff"; c.beginPath(); c.arc(px - F.pr * 0.35, py - F.pr * 0.4, F.pr * 0.32, 0, TAU); c.fill();
      }
      if (F.lid > 0.02) {
        const ly = ey - h + h * 2 * F.lid;
        c.fillStyle = col(K.gold); c.fillRect(ex - rx - 1, ey - h - 1, rx * 2 + 2, ly - (ey - h) + 1);
        c.strokeStyle = ink; c.lineWidth = 2; c.beginPath(); c.moveTo(ex - rx - 1, ly); c.lineTo(ex + rx + 1, ly); c.stroke();
      }
      c.restore();
      c.strokeStyle = ink; c.lineWidth = 2.2; c.beginPath(); c.ellipse(ex, ey, rx, h, 0, 0, TAU); c.stroke();
    };
    eye(-24, -8, 8.6, 9.6, -1, false);
    eye(6, -8, 10, 10.6, 1, F.wink);
    // sourcils épais (ang > 0 : colère, < 0 : inquiet)
    const brow = (bx, by, w, side, ang, up) => {
      const ix = bx - side * w / 2, ox = bx + side * w / 2, iy = by + ang * 6 - up, oy = by - ang * 4 - up;
      c.strokeStyle = col(K.hair); c.lineWidth = 4.4; c.beginPath(); c.moveTo(ix, iy); c.quadraticCurveTo(bx, Math.min(iy, oy) - 3 + Math.abs(ang) * 2, ox, oy); c.stroke();
    };
    brow(-25, -23, 19, -1, F.browL, F.upL);
    brow(7, -24, 22, 1, F.browR, F.upR);
    // nez
    c.strokeStyle = col(K.goldLo); c.lineWidth = 2.6; c.beginPath(); c.moveTo(-12, -3); c.quadraticCurveTo(-22, 5, -13, 8); c.stroke();
    // bouche
    const m = F.m, mx = -8, y0 = 21;
    if (m.mode === "o") {
      c.beginPath(); c.ellipse(mx, y0 + 5, 9 + m.open * 2, 8 + m.open * 5, 0, 0, TAU); c.fillStyle = "#4a1016"; c.fill(); c.strokeStyle = ink; c.lineWidth = 2.4; c.stroke();
      c.fillStyle = "#ff8b8b"; c.beginPath(); c.ellipse(mx, y0 + 9 + m.open * 3, 5, 3, 0, 0, TAU); c.fill();
    } else if (m.mode === "zig" || m.mode === "wave") {
      c.strokeStyle = ink; c.lineWidth = 2.8; c.beginPath();
      for (let k = 0; k <= 8; k++) { const px = mx - 22 + k * 5.5, py = y0 + 5 + (m.mode === "zig" ? (k % 2 ? -4 : 4) : Math.sin(k * 1.5 + F.spin) * 3.5); if (k) c.lineTo(px, py); else c.moveTo(px, py); }
      c.stroke();
    } else {
      const hw = m.w / 2, L = { x: mx - hw, y: y0 - 5 * m.grin }, R = { x: mx + hw, y: y0 - 6 * m.grin };
      const cu = y0 + 3 * m.grin - (m.bared ? 8 : 0), cd = y0 + (m.bared ? 18 : 6 + 11 * Math.max(0.3, m.grin)) + m.open * 15, nw = m.nerv ? Math.sin(F.spin * 2.6) * 2.2 * m.nerv : 0;
      const path = () => { c.beginPath(); c.moveTo(L.x, L.y); c.quadraticCurveTo(mx, cu, R.x, R.y); c.quadraticCurveTo(mx + nw * 2, cd + nw, L.x, L.y); c.closePath(); };
      const at = (u, k) => ({ x: (1 - u) * (1 - u) * L.x + 2 * u * (1 - u) * mx + u * u * R.x, y: (1 - u) * (1 - u) * L.y + 2 * u * (1 - u) * k + u * u * R.y });
      const th = m.bared ? (cd - cu) / 4 - 0.7 : 7 + m.open * 1.5;
      path(); c.fillStyle = "#4a1016"; c.fill();
      c.save(); c.clip();
      if (m.open > 0.3 && !m.bared) { c.fillStyle = "#ff8b8b"; c.beginPath(); c.ellipse(mx + 2, cd - 5, hw * 0.5, 7, 0, 0, TAU); c.fill(); }
      c.lineCap = "butt";
      c.strokeStyle = m.bared ? "#ff9aa0" : "#ffffff"; c.lineWidth = th * 2 + (m.bared ? 4 : 0); c.beginPath(); c.moveTo(L.x - 3, L.y); c.quadraticCurveTo(mx, cu, R.x + 3, R.y); c.stroke();
      if (m.bared) {
        c.beginPath(); c.moveTo(L.x - 3, L.y); c.quadraticCurveTo(mx, cd, R.x + 3, R.y); c.stroke();
        c.strokeStyle = "#ffffff"; c.lineWidth = th * 2; c.beginPath(); c.moveTo(L.x - 3, L.y); c.quadraticCurveTo(mx, cu + 3, R.x + 3, R.y); c.stroke();
        c.beginPath(); c.moveTo(L.x - 3, L.y); c.quadraticCurveTo(mx, cd - 3, R.x + 3, R.y); c.stroke();
      }
      const g0 = at(0.18, cu), g1 = at(0.3, cu);
      c.strokeStyle = col(K.badge); c.lineWidth = th * 2; c.beginPath(); c.moveTo(g0.x, g0.y + (m.bared ? 3 : 0)); c.lineTo(g1.x, g1.y + (m.bared ? 3 : 0)); c.stroke();
      c.strokeStyle = "rgba(60,20,20,0.35)"; c.lineWidth = 1; c.beginPath();
      for (let u = 0.06; u < 0.97; u += 0.12) { const a0 = at(u, cu), a1 = at(u, cd); c.moveTo(a0.x, a0.y); c.lineTo(a1.x, a1.y); }
      c.stroke();
      c.restore();
      c.lineCap = "round";
      path(); c.strokeStyle = ink; c.lineWidth = 2.5; c.stroke();
      c.lineWidth = 2.2; c.beginPath(); c.arc(L.x - 1.5, L.y - 0.5, 4.2, 1.9, 4.5); c.stroke(); c.beginPath(); c.arc(R.x + 1.5, R.y - 0.5, 4.2, -1.3, 1.3); c.stroke();
      if (F.sparkle > 0.05) { const g = at(0.24, cu); c.fillStyle = "#ffffff"; star4(c, g.x - 1, g.y + th * 0.6, 9 * F.sparkle, F.spin * 0.3); }
    }
  };

  BOSSES[8] = {
    v: 2,
    palette: { main: "#f6d477", dark: "#2f4aa3", accent: "#fff6d8", eye: "#2a1a0c", rage: "#ff5c40" },
    hit: { rx: 100, ry: 136, coreR: 24 },
    top: 150,
    attackFrom: { x: -104, y: -132 },
    castLean: -0.08,
    weakSpot: () => ({ x: BADGE.x, y: BADGE.y }),
    critLabel: "PROMESSE PERCÉE",
    epitaph: "SLA RÉVISÉ",
    lines: {
      hit: ["Ce n’est qu’une petite marge d’erreur…", "Aïe ! Un chiffre mesuré.", "Doucement, c’est du sur-mesure !", "Ça ? Une fuite sans importance."],
      crit: ["Mon badge 99,9 % !", "Tu as lu les petites lignes ?!", "Pas l’annexe ! Pas l’annexe !"],
      wrong: ["Signé ! Merci pour la confiance.", "Promis, ça tiendra en production.", "Le client adore ce chiffre.", "Tes évals disent 96 % ? Arrondissons."],
      timeout: ["Le client n’attend pas. Signe !", "Trop tard, j’ai déjà promis."],
      gloat: ["Encore un client satisfait !", "Personne ne lit l’annexe.", "Satisfait ou… satisfait."],
      rage: "Très bien : 100 % garanti, sans la moindre évaluation !",
      special: {
        shieldUp: ["Mon SLA est regonflé à bloc !", "Une erreur ? J’en promets encore plus !", "99,9 %, c’est écrit en gros."],
        shieldBreak: ["Trois preuves d’affilée ?! Mon SLA éclate !", "Non… pas des mesures !", "Qui a invité les évaluations ?"]
      }
    },
    intro: {
      title: "Bouclier SLA",
      text: "Son bouclier « 99,9 % » divise tes dégâts par deux tant que tu n’enchaînes pas 3 bonnes réponses. Une erreur le regonfle : seules des preuves répétées font tomber une promesse."
    },
    mechanics: ["shield"],

    /* Projectile : le contrat plié en avion de papier, avec un sillage d'étincelles dorées. */
    shot: {
      color: "#f6d477", spin: 0,
      draw(c, s) {
        const t = s.t || 0;
        c.fillStyle = s.rage ? "rgba(255,120,80,0.9)" : "rgba(255,226,140,0.95)";
        for (let i = 0; i < 4; i++) { const u = (t * 2.6 + i * 0.25) % 1; c.globalAlpha = 1 - u; star4(c, -20 - u * 24, Math.sin(i * 2.3 + t * 7) * (3 + u * 8), 5 * (1 - u) + 1, t * 6 + i); }
        c.globalAlpha = 1;
        c.save(); c.shadowColor = s.rage ? "#ff5c40" : "#f6d477"; c.shadowBlur = 10; c.rotate(Math.sin(t * 9) * 0.08); plane(c, s.rage); c.restore();
      }
    },

    /* Ballon : il danse au bout de son fil et perd de l'altitude en se dégonflant. */
    motion(b) {
      const t = b.t || 0, hp = clamp(b.hpFrac ?? 1, 0, 1), k = easeOut(b.enter ?? 1);
      let x = Math.sin(t * 0.5) * 15 + Math.sin(t * 1.3) * 4 - 10, y = Math.sin(t * 1.25) * 14 - 14 + (1 - hp) * 56;
      if (b.rage) { x += Math.sin(t * 7.3) * 2.5 + Math.sin(t * 0.9) * 9; y += Math.sin(t * 9.1) * 2.5 - Math.abs(Math.sin(t * 2.2)) * 10; }
      return { x: x * k, y: y * k };
    },

    /* Le Conseil des Parties Prenantes : salle du conseil en terrasse, panneau « 99,9 % », pupitre, tours de verre, chaises. */
    backdrop(c, env) {
      const W = env.W, gy = env.groundY, rnd = env.rnd || seeded(88);
      const tower = (x, w, h, a) => {
        const g = c.createLinearGradient(x, gy - h, x + w, gy); g.addColorStop(0, col("#3b3f7d", a)); g.addColorStop(0.55, col("#262a5c", a)); g.addColorStop(1, col("#1a1c44", a));
        c.fillStyle = "#15173a"; c.fillRect(x, gy - h, w, h); c.fillStyle = g; c.fillRect(x, gy - h, w, h);
        c.save(); c.beginPath(); c.rect(x, gy - h, w, h); c.clip();
        c.fillStyle = "rgba(190,200,255,0.07)"; c.beginPath(); c.moveTo(x - 4, gy - h * 0.5); c.lineTo(x + w + 4, gy - h * 0.92); c.lineTo(x + w + 4, gy - h * 0.66); c.lineTo(x - 4, gy - h * 0.24); c.closePath(); c.fill();
        c.strokeStyle = "rgba(170,180,245,0.13)"; c.lineWidth = 1; c.beginPath();
        for (let y = gy - h + 12; y < gy - 60; y += 15) { c.moveTo(x, y); c.lineTo(x + w, y); }
        for (let k = 1; k < 4; k++) { c.moveTo(x + (w * k) / 4, gy - h); c.lineTo(x + (w * k) / 4, gy); }
        c.stroke();
        for (let y = gy - h + 14; y < gy - 70; y += 15) for (let k = 0; k < 4; k++) if (rnd() < 0.1) { c.fillStyle = "rgba(255,226,150," + (0.22 + rnd() * 0.25) * a + ")"; c.fillRect(x + (w * k) / 4 + 2, y, w / 4 - 4, 11); }
        c.restore();
        c.fillStyle = "rgba(205,212,255,0.32)"; c.fillRect(x, gy - h, w, 2); c.fillRect(x, gy - h, 1.5, h);
      };
      tower(-14, 76, 262, 0.9);
      tower(W * 0.445, 62, 318, 0.75); tower(W * 0.535, 48, 236, 0.7);
      tower(W * 0.8, 78, 352, 0.72); tower(W * 0.905, 80, 268, 0.8);
      c.fillStyle = "rgba(205,212,255,0.4)"; c.fillRect(W * 0.8 + 56, gy - 392, 2, 40);
      c.fillStyle = C.bad; c.beginPath(); c.arc(W * 0.8 + 57, gy - 394, 2.5, 0, TAU); c.fill();

      // grand panneau : la courbe qui monte toujours, « 99,9 % » en gros, l'astérisque en tout petit
      const bx = W * 0.055, bw = W * 0.37, by = gy - 432, bh = 168;
      c.strokeStyle = "#2a2f5c"; c.lineWidth = 6; c.beginPath(); c.moveTo(bx + 34, by + bh); c.lineTo(bx + 34, gy - 40); c.moveTo(bx + bw - 34, by + bh); c.lineTo(bx + bw - 34, gy - 40); c.stroke();
      c.lineWidth = 2; c.strokeStyle = "rgba(90,100,160,0.7)"; c.beginPath();
      for (let y = by + bh; y < gy - 70; y += 44) { c.moveTo(bx + 34, y); c.lineTo(bx + bw - 34, y + 44); c.moveTo(bx + bw - 34, y); c.lineTo(bx + 34, y + 44); }
      c.stroke();
      rr(c, bx - 5, by - 5, bw + 10, bh + 10, 6); c.fillStyle = "#0c0e24"; c.fill(); c.strokeStyle = "#474f8c"; c.lineWidth = 2.5; c.stroke();
      const pg = c.createLinearGradient(0, by, 0, by + bh); pg.addColorStop(0, "#1b2356"); pg.addColorStop(1, "#11163a");
      c.fillStyle = pg; c.fillRect(bx, by, bw, bh);
      c.strokeStyle = "rgba(150,165,240,0.1)"; c.lineWidth = 1; c.beginPath();
      for (let k = 1; k < 5; k++) { c.moveTo(bx, by + (bh * k) / 5); c.lineTo(bx + bw, by + (bh * k) / 5); }
      for (let k = 1; k < 8; k++) { c.moveTo(bx + (bw * k) / 8, by); c.lineTo(bx + (bw * k) / 8, by + bh); }
      c.stroke();
      const pts = [[0.04, 0.9], [0.18, 0.84], [0.3, 0.86], [0.42, 0.72], [0.54, 0.66], [0.66, 0.46], [0.78, 0.34], [0.9, 0.1], [0.985, -0.16]];
      c.fillStyle = "rgba(243,184,65,0.14)";
      for (let k = 0; k < 8; k++) { const px = bx + bw * (0.07 + k * 0.115), ph = bh * (0.1 + 0.095 * k + (k > 4 ? (k - 4) * 0.03 : 0)); c.fillRect(px, by + bh - ph, bw * 0.07, ph); }
      const ag = c.createLinearGradient(0, by, 0, by + bh); ag.addColorStop(0, "rgba(243,184,65,0.34)"); ag.addColorStop(1, "rgba(243,184,65,0)");
      c.save(); c.beginPath(); c.rect(bx, by, bw, bh); c.clip();
      c.fillStyle = ag; c.beginPath(); c.moveTo(bx + bw * pts[0][0], by + bh);
      for (const [u, v] of pts) c.lineTo(bx + bw * u, by + bh * v);
      c.lineTo(bx + bw, by + bh); c.closePath(); c.fill();
      c.restore();
      c.strokeStyle = "#f3b841"; c.lineWidth = 4; c.lineJoin = "round"; c.lineCap = "round"; c.beginPath();
      pts.forEach(([u, v], i) => { if (i) c.lineTo(bx + bw * u, by + bh * v); else c.moveTo(bx + bw * u, by + bh * v); });
      c.stroke();
      const tipx = bx + bw * 0.985, tipy = by + bh * -0.16;                 // la flèche crève le cadre par le haut
      c.fillStyle = "#f3b841"; c.beginPath(); c.moveTo(tipx + 6, tipy - 15); c.lineTo(tipx + 9, tipy + 7); c.lineTo(tipx - 11, tipy - 2); c.closePath(); c.fill();
      c.fillStyle = "#fff3c4"; c.font = "800 " + Math.round(bh * 0.33) + "px " + F_DISPLAY; c.textAlign = "left"; c.textBaseline = "alphabetic"; c.fillText("99,9 %", bx + 14, by + bh * 0.42);
      c.fillStyle = "rgba(243,184,65,0.9)"; c.font = "700 " + Math.round(bh * 0.07) + "px " + F_MONO; c.fillText("SLA GARANTI*", bx + 16, by + bh * 0.54);
      c.fillStyle = "rgba(232,236,246,0.4)"; c.font = "600 " + Math.round(bh * 0.042) + "px " + F_MONO; c.fillText("*voir annexe", bx + 16, by + bh * 0.95);
      for (let k = 0; k < 3; k++) {                                          // rampes d'éclairage
        const lx = bx + bw * (0.2 + k * 0.3);
        c.strokeStyle = "#474f8c"; c.lineWidth = 2; c.beginPath(); c.moveTo(lx, by - 5); c.lineTo(lx, by - 16); c.lineTo(lx + 9, by - 19); c.stroke();
        c.fillStyle = "rgba(255,243,196,0.9)"; c.fillRect(lx + 6, by - 21, 8, 4);
      }

      // rangées de chaises du conseil, quelques parties prenantes assises
      const px = W * 0.665;
      for (let x = W * 0.21 + 17; x < W + 20; x += 34) { if (Math.abs(x - px) < 50) continue; rr(c, x - 9, gy - 101, 18, 26, 4); c.fillStyle = "#1c1f48"; c.fill(); c.fillStyle = "rgba(190,200,255,0.16)"; c.fillRect(x - 7, gy - 101, 14, 1.5); }
      for (let x = W * 0.21; x < W + 20; x += 34) {
        if (Math.abs(x - px) < 52) continue;
        if (rnd() < 0.42) { c.fillStyle = "#0e1028"; c.beginPath(); c.arc(x, gy - 100, 8.5, 0, TAU); c.fill(); c.beginPath(); c.ellipse(x, gy - 82, 14, 10, 0, Math.PI, 0); c.fill(); }
        rr(c, x - 11, gy - 87, 22, 32, 5); c.fillStyle = "#14163a"; c.fill(); c.fillStyle = "rgba(190,200,255,0.22)"; c.fillRect(x - 9, gy - 87, 18, 1.5);
      }

      // pupitre et micro, sous le ballon
      const sg = c.createRadialGradient(px, gy - 96, 6, px, gy - 96, 90); sg.addColorStop(0, "rgba(255,240,200,0.16)"); sg.addColorStop(1, "rgba(255,240,200,0)");
      c.fillStyle = sg; c.fillRect(px - 90, gy - 186, 180, 150);
      c.fillStyle = "#33264a"; c.beginPath(); c.moveTo(px - 27, gy - 50); c.lineTo(px - 33, gy - 104); c.lineTo(px + 33, gy - 104); c.lineTo(px + 27, gy - 50); c.closePath(); c.fill();
      c.fillStyle = "rgba(255,255,255,0.06)"; c.beginPath(); c.moveTo(px - 33, gy - 104); c.lineTo(px - 18, gy - 104); c.lineTo(px - 14, gy - 50); c.lineTo(px - 27, gy - 50); c.closePath(); c.fill();
      rr(c, px - 38, gy - 111, 76, 9, 3); c.fillStyle = "#59477a"; c.fill();
      c.fillStyle = "#f3b841"; c.beginPath(); c.arc(px, gy - 80, 10, 0, TAU); c.fill();
      c.fillStyle = "#33264a"; c.font = "800 11px " + F_DISPLAY; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText("%", px, gy - 79.5);
      c.strokeStyle = "#8a93b8"; c.lineWidth = 2.2; c.lineCap = "round"; c.beginPath(); c.moveTo(px - 8, gy - 111); c.quadraticCurveTo(px - 8, gy - 130, px - 20, gy - 137); c.stroke();
      c.beginPath(); c.moveTo(px + 12, gy - 111); c.quadraticCurveTo(px + 12, gy - 124, px + 3, gy - 131); c.stroke();
      c.fillStyle = "#0e1028"; c.beginPath(); c.ellipse(px - 23, gy - 139, 6.5, 4.6, 0.5, 0, TAU); c.fill(); c.beginPath(); c.ellipse(px + 1, gy - 132.5, 5.5, 4, 0.6, 0, TAU); c.fill();
      c.fillStyle = C.bad; c.beginPath(); c.arc(px + 28, gy - 115, 2.2, 0, TAU); c.fill();
    },

    /* Flashs des photographes dans le public ; le panneau grésille. */
    ambient(c, env) {
      const W = env.W, gy = env.groundY, t = env.time || 0;
      const slot = Math.floor(t / 0.5), u = (t / 0.5) % 1, r = seeded(slot * 7919 + 13);
      const fx = W * (0.22 + r() * 0.76), fy = gy - 96 - r() * 8;
      if (r() < 0.72 && u < 0.34) {
        const k = 1 - u / 0.34, g = c.createRadialGradient(fx, fy, 1, fx, fy, 16 + 26 * k);
        g.addColorStop(0, "rgba(255,255,255," + 0.95 * k + ")"); g.addColorStop(0.3, "rgba(220,232,255," + 0.4 * k + ")"); g.addColorStop(1, "rgba(220,232,255,0)");
        c.fillStyle = g; c.fillRect(fx - 44, fy - 44, 88, 88);
        c.strokeStyle = "rgba(255,255,255," + 0.9 * k + ")"; c.lineWidth = 1.6; c.beginPath(); c.moveTo(fx - 22 * k, fy); c.lineTo(fx + 22 * k, fy); c.moveTo(fx, fy - 15 * k); c.lineTo(fx, fy + 15 * k); c.stroke();
      }
      const bx = W * 0.055, bw = W * 0.37, by = gy - 432, bh = 168;
      const fl = Math.sin(t * 13) * Math.sin(t * 3.7) > 0.8 ? 0.1 : 0.025 + 0.02 * Math.sin(t * 1.9);
      c.fillStyle = "rgba(255,243,196," + fl + ")"; c.fillRect(bx, by, bw, bh);
      const sy = by + ((t * 34) % bh); c.fillStyle = "rgba(255,255,255,0.05)"; c.fillRect(bx, sy, bw, 5);
    },

    draw(c, b) {
      const t = b.t || 0, time = b.time ?? t;
      const look = b.look || { x: -1, y: 0 };
      const enter = b.enter ?? 1, dying = b.dying ?? -1, dmg = b.dmg || 0;
      const fl = b.flash || 0, sq = b.squint || 0, rt = b.rageT || 0, hp = clamp(b.hpFrac ?? 1, 0, 1);
      const stun = (b.stun || 0) > 0, gloat = b.gloat || 0, talk = b.talk || 0, beat = b.beat || 0, threat = b.threat || 0;
      const A = atkPose(b), dead = dying >= 0;
      const castT = b.cast >= 0 ? b.cast : -1, castK = castT >= 0 ? Math.sin(clamp(castT / 0.9, 0, 1) * Math.PI) : 0;
      const shieldDown = !!(b.mech && b.mech.shield && b.mech.shield.up === false);
      const nerv = dead ? 1 : Math.max(shieldDown ? 1 : 0, threat * 0.9, dmg >= 3 ? 0.55 : 0);

      // palette de l'instant : l'or vire au rouge quand il est surgonflé
      const wht = fl * 0.65, red = rt * 0.85;
      const K = {
        gold: mixv(mixv("#f6d477", "#ff5c40", red), C.white, wht), goldHi: mixv(mixv("#fff3c2", "#ffc0a0", red), C.white, wht), goldLo: mixv(mixv("#bf8a26", "#9c1f1c", red), C.white, wht * 0.6),
        suit: mixv(mixv("#2f4aa3", "#472a86", rt * 0.5), C.white, wht * 0.7), suitHi: mixv(mixv("#5d7be2", "#8a5fd0", rt * 0.5), C.white, wht * 0.7), suitLo: mixv(mixv("#172655", "#24124a", rt * 0.5), C.white, wht * 0.5),
        shirt: mixv("#fbf7ec", C.white, wht), red: mixv("#e0453a", C.white, wht * 0.6), badge: mixv("#f3c343", C.white, wht), paper: mixv("#fffdf2", C.white, wht),
        ink: "#1d1408", hair: mixv("#1c1a34", "#3a1222", rt * 0.6), blush: mixv("#ff8f80", "#ff2f5e", rt), pupil: mixv("#2a1a0c", "#b01212", rt)
      };

      // gonflage : entrée (trois coups de pompe), vie, rage (surgonflé), mort (il se vide)
      let inf = lerp(0.92, 1, hp) + 0.13 * rt + Math.sin(t * 8.5) * 0.012 * rt + castK * 0.07, headInf = 1, armK = 1, faceA = 1, paperK = 1, limp = dmg >= 3 ? 0.12 : 0;
      let flop = 0, alpha = 1, oy = 0, ox = 0, spin = 0, pumpPuff = 0;
      if (enter < 1) {
        const p1 = backOut(seg(enter, 0.08, 0.28)), p2 = backOut(seg(enter, 0.32, 0.52)), p3 = backOut(seg(enter, 0.56, 0.78)), end = seg(enter, 0.78, 1);
        inf *= 0.16 + 0.3 * p1 + 0.3 * p2 + 0.24 * p3 + 0.1 * Math.sin(end * Math.PI) * (1 - end);
        headInf = 0.12 + 0.88 * backOut(seg(enter, 0.56, 0.8)); armK = backOut(seg(enter, 0.64, 0.88)); faceA = seg(enter, 0.6, 0.72); paperK = backOut(seg(enter, 0.84, 0.98));
        limp = 1 - seg(enter, 0.1, 0.62); flop = 1.1 * (1 - easeOut(seg(enter, 0.08, 0.56))) + Math.sin(enter * 36) * 0.06 * (1 - enter);
        alpha = seg(enter, 0, 0.07); oy = 26 * (1 - easeOut(seg(enter, 0, 0.3)));
        pumpPuff = Math.max(Math.sin(seg(enter, 0.08, 0.3) * Math.PI), Math.sin(seg(enter, 0.32, 0.54) * Math.PI), Math.sin(seg(enter, 0.56, 0.8) * Math.PI));
      }
      let zipU = 0, dropK = 0;
      if (dead) {
        zipU = seg(dying, 0.1, 0.72); dropK = seg(dying, 0.72, 1);
        const P = zipPos(zipU), Q = zipPos(Math.min(1, zipU + 0.012));
        inf = (1.05 + 0.13 * rt + 0.06 * seg(dying, 0, 0.1)) * lerp(1, 0.24, Math.pow(zipU, 0.7)) * (1 - 0.15 * dropK);
        headInf = lerp(1, 0.42, zipU); armK = 1 - 0.55 * zipU; limp = zipU; paperK = 0;
        ox = P.x + Math.sin(dropK * 9) * 9 * (1 - dropK); oy = P.y + 150 * dropK * dropK;
        spin = zipU > 0 && zipU < 1 ? (Math.atan2(Q.y - P.y, Q.x - P.x) + Math.PI / 2) * seg(zipU, 0, 0.06) : zipU >= 1 ? 2.4 + Math.sin(dropK * 8) * 0.35 * (1 - dropK) : 0;
        alpha = 1 - seg(dying, 0.9, 1);
        // sillage : bouffées d'air le long du zigzag
        for (let i = 1; i <= 8; i++) {
          const u = zipU - i * 0.028; if (u <= 0 || dropK >= 1) continue;
          const p = zipPos(u), a = (0.5 - i * 0.055) * (1 - dropK);
          c.fillStyle = "rgba(240,244,255," + Math.max(0, a) + ")"; c.beginPath(); c.arc(p.x + Math.sin(i * 5.1) * 4, p.y + 30 + Math.cos(i * 3.7) * 4, 4 + i * 1.5, 0, TAU); c.fill();
        }
        // le contrat lui échappe et tombe comme une feuille
        const ca = 1 - seg(dying, 0.35, 0.7);
        if (ca > 0) { c.save(); c.globalAlpha = ca; drawContract(c, K, -134 + Math.sin(dying * 15) * 18, -36 + 250 * dying * dying, Math.sin(dying * 12) * 0.9, 1); c.restore(); }
      }
      const breath = Math.sin(t * 2.3) * 0.018 + beat * 0.02;
      const rx = 86 * inf * (1 + breath) * (1 + 0.08 * limp), ry = 82 * inf * (1 + breath * 0.7) * (1 - 0.2 * limp);
      const cy = KNOT - ry - 2, top = cy - ry;
      const R = 42 * headInf * (inf > 0.9 ? 1 + (inf - 1) * 0.6 : Math.max(0.3, inf + 0.06));
      const lean = A.on ? 0.13 * easeOut(A.wind) * (1 - A.strike) - 0.14 * easeOut(A.strike) * (1 - easeInOut(A.rec)) : 0;
      const jit = (rt * 1.1 + (stun ? 1.2 : 0) + nerv * 0.5 + (dead ? 2.5 * (1 - zipU) : 0)) * (enter < 1 ? 0 : 1);
      const bounce = gloat > 0.1 ? -Math.abs(Math.sin(t * 11)) * 7 * gloat : 0;

      c.globalAlpha = alpha;
      c.translate(ox + Math.sin(t * 57) * jit, oy + bounce + Math.cos(t * 49) * jit);
      if (!dead) {
        // fil du ballon : il pend sous le nœud et ondule
        const sway = Math.sin(t * 1.6) * 9, sway2 = Math.sin(t * 1.6 - 1.2) * 12;
        c.strokeStyle = "rgba(232,236,246,0.62)"; c.lineWidth = 1.7; c.lineCap = "round"; c.beginPath(); c.moveTo(0, KNOT + 7);
        c.bezierCurveTo(12 + sway, KNOT + 26, -14 - sway2, KNOT + 48, 4 + sway2 * 0.6, 189); c.stroke();
      }
      // halo
      const hg = c.createRadialGradient(0, cy, 20, 0, cy, 215); hg.addColorStop(0, col(K.gold, (0.2 + 0.08 * rt + 0.05 * beat) * Math.min(1, inf))); hg.addColorStop(1, col(K.gold, 0));
      c.fillStyle = hg; c.fillRect(-225, -190, 410, 380);

      c.translate(0, dead ? 30 : KNOT); c.rotate(flop + lean + spin + (dead ? 0 : Math.sin(t * 1.1) * 0.035 + (stun ? Math.sin(t * 6) * 0.07 : 0))); c.scale(1 + fl * 0.07, 1 - fl * 0.08); c.translate(0, dead ? -30 : -KNOT);

      if (dead) {                                                   // fil qui flotte derrière lui
        c.strokeStyle = "rgba(232,236,246,0.6)"; c.lineWidth = 1.7; c.lineCap = "round"; c.beginPath(); c.moveTo(0, KNOT + 7);
        c.bezierCurveTo(10 * Math.sin(t * 30), KNOT + 22, -10 * Math.sin(t * 30 + 1), KNOT + 38, 6 * Math.sin(t * 30 + 2), KNOT + 52); c.stroke();
        if (zipU > 0 && zipU < 1) { c.fillStyle = "rgba(240,244,255,0.75)"; for (let i = 0; i < 3; i++) { const u = (t * 5 + i / 3) % 1; c.beginPath(); c.arc(Math.sin(i * 4 + t * 20) * 5, KNOT + 12 + u * 30, 3 + u * 6, 0, TAU); c.globalAlpha = alpha * (1 - u); c.fill(); } c.globalAlpha = alpha; }
      }
      if (pumpPuff > 0.05) {                                        // coups de pompe : l'air entre par le nœud
        c.strokeStyle = "rgba(240,244,255," + 0.8 * pumpPuff + ")"; c.lineWidth = 2.4; c.lineCap = "round";
        for (const sgn of [-1, 1]) for (let i = 0; i < 2; i++) { c.beginPath(); c.moveTo(sgn * (12 + i * 9), KNOT + 4 - i * 8); c.lineTo(sgn * (20 + i * 11 + 6 * pumpPuff), KNOT + 8 - i * 12); c.stroke(); }
      }

      // --- bras arrière (côté droit) : main sur la hanche, doigt levé, poing ou pouce ---
      const S2 = { x: rx * 0.78, y: cy - ry * 0.4 };
      let H2 = { x: rx + 8, y: cy + ry * 0.34 }, bend2 = { x: 24, y: -8 }, g2 = "fist";
      if (rt > 0.5 && !dead) { H2 = { x: 114, y: -46 + Math.sin(t * 14) * 4 }; bend2 = { x: 22, y: 12 }; g2 = "fist"; }
      else if (shieldDown && !dead) { H2 = { x: 34 + Math.sin(t * 9) * 2, y: top + 8 }; bend2 = { x: 44, y: 8 }; g2 = "fist"; }
      if (castK > 0.05 || talk > 0.05) { const k = Math.max(castK, talk > 0.05 ? 1 : 0); H2 = { x: lerp(H2.x, 116, k), y: lerp(H2.y, -40 + Math.sin(t * 5) * 3, k) }; bend2 = { x: 20, y: 14 }; g2 = "point"; }
      if (gloat > 0.1) { H2 = { x: 118, y: -22 + bounce }; bend2 = { x: 20, y: 12 }; g2 = "thumb"; }
      if (dead) { H2 = { x: rx + 26, y: cy + ry * 0.5 + Math.sin(t * 31) * 8 }; bend2 = { x: 8, y: 0 }; g2 = "open"; }
      const aw = 23 * Math.min(1, 0.4 + inf * 0.6);
      if (armK > 0.05) arm(c, K, S2.x, S2.y, lerp(S2.x, H2.x, armK), lerp(S2.y, H2.y, armK), bend2.x * armK, bend2.y * armK, aw, g2);

      // --- ventre : ballon en costume, plastron, revers, boutons ---
      const bg = c.createRadialGradient(-rx * 0.38, cy - ry * 0.45, 6, 0, cy, rx * 1.25);
      bg.addColorStop(0, col(K.suitHi)); bg.addColorStop(0.5, col(K.suit)); bg.addColorStop(1, col(K.suitLo));
      c.beginPath(); c.ellipse(0, cy, rx, ry, 0, 0, TAU); c.fillStyle = bg; c.fill();
      c.save(); c.clip();
      c.strokeStyle = col(K.suitHi, 0.3); c.lineWidth = 1.2; c.beginPath();
      for (let i = -4; i <= 4; i++) { if (Math.abs(i) < 2) continue; const x = i * rx * 0.2; c.moveTo(x * 0.72, top); c.quadraticCurveTo(x * 1.28, cy, x * 0.72, cy + ry); }
      c.stroke();
      const open = 1 + 0.5 * rt + 0.15 * castK, sw = 27 * Math.min(1, inf);
      c.fillStyle = col(K.shirt);
      c.beginPath(); c.moveTo(-sw, top - 2); c.quadraticCurveTo(-sw * 1.5 * open, cy - ry * 0.05, -sw * 0.5 * open, cy + ry); c.lineTo(sw * 0.6 * open, cy + ry); c.quadraticCurveTo(sw * 1.65 * open, cy - ry * 0.05, sw, top - 2); c.closePath(); c.fill();
      c.strokeStyle = col(K.suitLo, 0.8); c.lineWidth = 2.4; c.stroke();
      // boutons de chemise ; en rage le tissu tire entre eux
      c.fillStyle = "rgba(160,150,130,0.9)";
      for (let k = 0; k < 3; k++) { const yb = cy - ry * 0.05 + k * ry * 0.3; if (Math.hypot(4 - BADGE.x, yb - BADGE.y) < 30) continue; c.beginPath(); c.arc(4, yb, 2, 0, TAU); c.fill(); }
      if (rt > 0.3) { c.strokeStyle = "rgba(120,110,100," + 0.5 * rt + ")"; c.lineWidth = 1.2; c.beginPath(); for (const yb of [cy - ry * 0.38, cy - ry * 0.2]) { c.moveTo(-sw * 0.9, yb - 4); c.lineTo(4, yb); c.lineTo(sw, yb - 4); c.moveTo(-sw * 0.9, yb + 5); c.lineTo(4, yb); c.lineTo(sw, yb + 5); } c.stroke(); }
      // revers
      c.fillStyle = col(K.suitHi);
      for (const sgn of [-1, 1]) { c.beginPath(); c.moveTo(sgn * sw, top - 2); c.lineTo(sgn * sw * 2.4, top + ry * 0.36); c.lineTo(sgn * sw * 1.75, top + ry * 0.4); c.lineTo(sgn * sw * 1.36 * open, cy - ry * 0.12); c.quadraticCurveTo(sgn * sw * 1.25, top + ry * 0.4, sgn * sw, top - 2); c.closePath(); c.fill(); }
      c.strokeStyle = col(K.suitLo, 0.7); c.lineWidth = 1.6;
      for (const sgn of [-1, 1]) { c.beginPath(); c.moveTo(sgn * sw * 2.4, top + ry * 0.36); c.lineTo(sgn * sw * 1.75, top + ry * 0.4); c.lineTo(sgn * sw * 1.36 * open, cy - ry * 0.12); c.stroke(); }
      // boutons dorés de la veste (le second saute en rage) et pochette
      c.fillStyle = col(K.badge);
      c.beginPath(); c.arc(-sw * 1.45 * open - 7, cy + ry * 0.12, 3.6, 0, TAU); c.fill();
      if (rt < 0.6) { c.beginPath(); c.arc(-sw * 1.2 * open - 7, cy + ry * 0.48, 3.6, 0, TAU); c.fill(); }
      c.fillStyle = col(K.shirt); c.beginPath(); c.moveTo(rx * 0.5, cy - ry * 0.34); c.lineTo(rx * 0.58, cy - ry * 0.5); c.lineTo(rx * 0.64, cy - ry * 0.37); c.lineTo(rx * 0.7, cy - ry * 0.48); c.lineTo(rx * 0.76, cy - ry * 0.34); c.closePath(); c.fill();
      c.strokeStyle = col(K.suitLo, 0.8); c.lineWidth = 2; c.beginPath(); c.moveTo(rx * 0.46, cy - ry * 0.34); c.lineTo(rx * 0.8, cy - ry * 0.34); c.stroke();
      // plis quand il se dégonfle
      if (limp > 0.05) { c.strokeStyle = col(K.suitLo, 0.75 * Math.min(1, limp * 2)); c.lineWidth = 2; c.beginPath(); for (let i = -2; i <= 2; i++) { c.moveTo(i * rx * 0.3, cy + ry * 0.98); c.quadraticCurveTo(i * rx * 0.36 + 5, cy + ry * 0.6, i * rx * 0.42, cy + ry * (0.45 - 0.2 * limp)); } c.stroke(); }
      c.restore();
      c.fillStyle = "rgba(255,255,255,0.26)"; c.beginPath(); c.ellipse(-rx * 0.6, cy - ry * 0.36, rx * 0.11, ry * 0.3, 0.5, 0, TAU); c.fill();
      c.fillStyle = "rgba(255,255,255,0.4)"; c.beginPath(); c.ellipse(-rx * 0.5, cy - ry * 0.66, rx * 0.07, ry * 0.07, 0.5, 0, TAU); c.fill();
      c.beginPath(); c.ellipse(0, cy, rx, ry, 0, 0, TAU); c.strokeStyle = col(K.suitLo); c.lineWidth = 2; c.stroke();
      if (rt > 0.3 && !dead) {                                      // tendu à craquer : traits de tension autour du ventre
        c.strokeStyle = col(K.goldHi, 0.8 * rt); c.lineWidth = 2.4; c.lineCap = "round";
        for (const a of [-2.75, -2.35, -0.75, -0.35, 0.2, 2.9]) { const k = 0.5 + 0.5 * Math.sin(t * 17 + a * 5), r0 = 7 + 4 * k; c.beginPath(); c.moveTo(Math.cos(a) * (rx + r0), cy + Math.sin(a) * (ry + r0)); c.lineTo(Math.cos(a) * (rx + r0 + 9), cy + Math.sin(a) * (ry + r0 + 9)); c.stroke(); }
      }
      // nœud
      c.fillStyle = col(K.goldLo); c.beginPath(); c.moveTo(-8, KNOT - 5); c.lineTo(8, KNOT - 5); c.lineTo(4, KNOT + 3); c.lineTo(7, KNOT + 10); c.lineTo(-7, KNOT + 10); c.lineTo(-4, KNOT + 3); c.closePath(); c.fill();
      c.fillStyle = col(K.gold); c.beginPath(); c.moveTo(-6, KNOT - 4); c.lineTo(6, KNOT - 4); c.lineTo(3, KNOT + 3); c.lineTo(-3, KNOT + 3); c.closePath(); c.fill();

      // --- cravate : desserrée puis dénouée avec les dégâts, rabattue par-dessus l'épaule en rage ---
      const ts = Math.min(1, inf), loose = dmg >= 1 ? 3 + dmg * 2 : 0;
      c.save(); c.translate(dmg >= 2 ? 3 : 0, top + 7 * ts + loose); c.rotate((dmg >= 2 ? 0.14 : 0) + Math.sin(t * 2) * 0.03 - rt * 0.5 * (dead ? 0 : 1) - 0.9 * easeOut(A.strike) * (1 - A.rec) * 0.3); c.scale(ts, ts);
      c.fillStyle = col(K.red);
      if (dmg >= 3) { c.beginPath(); c.moveTo(-5, 0); c.lineTo(3, 0); c.lineTo(-3, 48); c.lineTo(-11, 42); c.closePath(); c.fill(); c.beginPath(); c.moveTo(2, 0); c.lineTo(9, 2); c.lineTo(16, 34); c.lineTo(8, 36); c.closePath(); c.fill(); }
      else { c.beginPath(); c.moveTo(-5, 9); c.lineTo(5, 9); c.lineTo(10.5, 52); c.lineTo(0, 64); c.lineTo(-10.5, 52); c.closePath(); c.fill(); c.beginPath(); c.moveTo(-7.5, -2); c.lineTo(7.5, -2); c.lineTo(5, 10); c.lineTo(-5, 10); c.closePath(); c.fill(); c.fillStyle = "rgba(255,255,255,0.22)"; c.beginPath(); c.moveTo(-3, 12); c.lineTo(1, 12); c.lineTo(-4, 50); c.lineTo(-8, 50); c.closePath(); c.fill(); c.strokeStyle = "rgba(100,20,16,0.6)"; c.lineWidth = 1.4; c.beginPath(); c.moveTo(-5, 9.5); c.lineTo(5, 9.5); c.stroke(); }
      c.restore();

      // --- rustines et fuites du ventre ---
      if (dmg >= 1 && inf > 0.6) patch(c, rx * 0.5, cy + ry * 0.05, -0.45, 26, 13);
      if (dmg >= 3 && inf > 0.6) { patch(c, -rx * 0.56, cy + ry * 0.52, 0.7, 26, 12); patch(c, -rx * 0.56, cy + ry * 0.52, -0.6, 26, 12); }
      const leak = (a, k) => {
        const px = Math.cos(a) * rx, py = cy + Math.sin(a) * ry, nx = Math.cos(a), ny = Math.sin(a);
        c.fillStyle = "#0b0f22"; c.beginPath(); c.ellipse(px - nx * 2, py - ny * 2, 4.5, 2.2, a + Math.PI / 2, 0, TAU); c.fill();
        c.lineCap = "round"; c.lineWidth = 2.2;
        for (let j = -1; j <= 1; j++) { const u = (t * 2.6 * k + (j + 1) / 3) % 1, da = a + j * 0.32, r0 = 5 + u * 20; c.strokeStyle = "rgba(240,244,255," + 0.85 * (1 - u) + ")"; c.beginPath(); c.moveTo(px + Math.cos(da) * r0, py + Math.sin(da) * r0); c.lineTo(px + Math.cos(da) * (r0 + 8), py + Math.sin(da) * (r0 + 8)); c.stroke(); }
      };
      if (dmg >= 2 && !dead && enter >= 1) leak(0.42, 1);
      if (dead && zipU <= 0) { leak(0.9, 3); c.fillStyle = "#ffffff"; star4(c, Math.cos(0.9) * rx + 6, cy + Math.sin(0.9) * ry + 6, 16 * (1 - seg(dying, 0, 0.1)) + 4, 0.4); }

      // --- badge 99,9 % : macaron doré dentelé, rubans rouges (point faible) ---
      if (inf > 0.55) {
        const bs = Math.min(1, inf) * (1 + beat * 0.07 + Math.sin(time * 4) * 0.025), dim = shieldDown ? 0.55 : 1;
        c.save(); c.translate(BADGE.x, BADGE.y); c.scale(bs, bs);
        c.fillStyle = col(K.red); c.beginPath(); c.moveTo(-13, 12); c.lineTo(-19, 40); c.lineTo(-10, 35); c.lineTo(-4, 42); c.lineTo(-1, 14); c.closePath(); c.fill(); c.beginPath(); c.moveTo(13, 12); c.lineTo(19, 40); c.lineTo(10, 35); c.lineTo(4, 42); c.lineTo(1, 14); c.closePath(); c.fill();
        if (!shieldDown) { c.shadowColor = col(K.badge); c.shadowBlur = 14; }
        c.fillStyle = col(mixv(K.badge, "#8a7a4a", 1 - dim)); c.beginPath();
        for (let i = 0; i < 28; i++) { const a = (i * TAU) / 28 + (shieldDown ? 0 : time * 0.25), q = i % 2 ? 23.5 : 27.5; c.lineTo(Math.cos(a) * q, Math.sin(a) * q); }
        c.closePath(); c.fill(); c.shadowBlur = 0;
        c.fillStyle = col(mixv("#fff6d8", "#c9c2ac", 1 - dim)); c.beginPath(); c.arc(0, 0, 20.5, 0, TAU); c.fill();
        c.strokeStyle = col(K.red, dim); c.lineWidth = 1.6; c.beginPath(); c.arc(0, 0, 17.5, 0, TAU); c.stroke();
        c.fillStyle = shieldDown ? "rgba(29,20,8,0.6)" : "#1d1408"; c.font = "800 16px " + F_DISPLAY; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText("99,9 %", 0, 1);
        if (shieldDown || dmg >= 3) { c.strokeStyle = "rgba(150,40,30,0.9)"; c.lineWidth = 2; c.lineJoin = "round"; c.beginPath(); c.moveTo(-15, -13); c.lineTo(-4, -3); c.lineTo(-9, 4); c.lineTo(8, 9); c.lineTo(13, 17); c.stroke(); }
        c.fillStyle = "rgba(255,255,255,0.5)"; c.beginPath(); c.ellipse(-9, -11, 6, 2.6, -0.6, 0, TAU); c.fill();
        c.restore();
      }
      if (!dead) drawCracks(c, b, "rgba(20,14,40,0.75)", 1.8);

      // --- col de chemise ---
      c.fillStyle = col(K.shirt); c.strokeStyle = "rgba(150,140,120,0.8)"; c.lineWidth = 1.2;
      const co = dmg >= 3 ? 1.5 : 1;
      for (const sgn of [-1, 1]) { c.beginPath(); c.moveTo(sgn * 24 * ts * co, top + 1); c.lineTo(sgn * 2 * co, top + 14 * ts); c.lineTo(sgn * 13 * ts * co, top + 24 * ts); c.closePath(); c.fill(); c.stroke(); }

      // --- tête : ballon doré, banane gominée, grand sourire commercial ---
      const hx = -6 * Math.min(1, inf), hy = top - R * 0.58 + (gloat > 0.1 ? -2 : 0), hs = R / 42;
      const headRot = (gloat > 0.1 ? 0.16 * gloat : 0) + (nerv > 0.3 && rt < 0.5 ? Math.sin(t * 2.6) * 0.03 : 0) - 0.05 * castK + (limp > 0.3 ? 0.5 * (limp - 0.3) : 0) + Math.sin(t * 1.1 + 0.8) * 0.025;
      c.save(); c.translate(hx, hy + R * 0.7); c.rotate(headRot); c.translate(0, -R * 0.7); c.scale(hs, hs);
      c.fillStyle = col(K.goldLo); c.beginPath(); c.ellipse(39, 2, 6.5, 8.5, 0.2, 0, TAU); c.fill();
      c.fillStyle = col(K.gold); c.beginPath(); c.ellipse(38, 2, 4, 6, 0.2, 0, TAU); c.fill();
      const hg2 = c.createRadialGradient(-16, -18, 4, 0, 0, 46); hg2.addColorStop(0, col(K.goldHi)); hg2.addColorStop(0.55, col(K.gold)); hg2.addColorStop(1, col(K.goldLo));
      c.beginPath(); c.arc(0, 0, 42, 0, TAU); c.fillStyle = hg2; c.fill(); c.strokeStyle = col(K.goldLo); c.lineWidth = 1.8; c.stroke();
      c.fillStyle = "rgba(255,255,255,0.5)"; c.beginPath(); c.ellipse(-27, -20, 5, 10, 0.75, 0, TAU); c.fill();
      // cheveux : banane gominée ; en rage ils se hérissent
      c.fillStyle = col(K.hair);
      if (rt > 0.5) {
        c.beginPath(); c.moveTo(42, -2); c.lineTo(50, -24); c.lineTo(36, -30); c.lineTo(40, -52); c.lineTo(20, -44); c.lineTo(14, -64); c.lineTo(-2, -49); c.lineTo(-16, -66); c.lineTo(-24, -47); c.lineTo(-46, -56); c.lineTo(-42, -32);
        c.quadraticCurveTo(-30, -36, -24, -29); c.quadraticCurveTo(0, -24, 22, -29); c.quadraticCurveTo(34, -24, 37, -6); c.closePath(); c.fill();
      } else {
        c.beginPath(); c.moveTo(42, -2); c.bezierCurveTo(48, -40, 18, -57, -8, -53); c.bezierCurveTo(-28, -60, -54, -52, -49, -30); c.quadraticCurveTo(-41, -36, -36, -25);
        c.quadraticCurveTo(-14, -37, 8, -30); c.quadraticCurveTo(31, -26, 37, -6); c.closePath(); c.fill();
        c.strokeStyle = "rgba(255,255,255,0.3)"; c.lineWidth = 3; c.lineCap = "round"; c.beginPath(); c.moveTo(-40, -43); c.quadraticCurveTo(-20, -53, 6, -46); c.stroke();
        if (dmg >= 2) { c.strokeStyle = col(K.hair); c.lineWidth = 3; c.beginPath(); c.moveTo(-2, -50); c.quadraticCurveTo(6, -66, 18, -60); c.moveTo(-30, -50); c.quadraticCurveTo(-34, -62, -44, -62); c.stroke(); }
      }
      // expression
      const blink = (t % 4.3) > 4.16, winkCycle = (t % 5.2) > 4.4 && (t % 5.2) < 4.85;
      const F = {
        lx: clamp(look.x, -1, 1), ly: clamp(look.y, -1, 1), lid: 0.3, wide: 1, pr: 4.7, mode: "open", wink: false, browL: -0.15, browR: -0.1, upL: 3 + Math.sin(t * 0.9) * 1.5, upR: 0, spin: t * 7, sparkle: 0,
        m: { w: 58, grin: 1, open: 0.12 + 0.05 * Math.sin(t * 2.3), bared: false, nerv: 0, mode: "grin" }
      };
      if (blink) F.mode = "happy";
      if (winkCycle && !rt && !nerv) { F.wink = true; F.sparkle = Math.sin(seg(t % 5.2, 4.4, 4.85) * Math.PI); }
      if (nerv > 0.05) { F.lid = lerp(F.lid, 0, nerv); F.wide = 1 + 0.12 * nerv; F.pr = lerp(F.pr, 3.2, nerv); F.browL = F.browR = -0.7 * nerv; F.upL = F.upR = 3 * nerv; F.lx = clamp(F.lx + Math.sin(t * 5.3) * 0.35 * nerv, -1, 1); F.m.nerv = nerv; F.m.open = 0.1; F.m.grin = lerp(1, 0.55, nerv); }
      if (rt > 0) { F.lid = lerp(F.lid, 0, rt); F.wide = lerp(F.wide, 1.18, rt); F.pr = lerp(F.pr, 3, rt); F.browL = lerp(F.browL, 1.15, rt); F.browR = lerp(F.browR, 1.15, rt); F.upL = lerp(F.upL, -3, rt); F.upR = lerp(F.upR, -3, rt); if (rt > 0.5) { F.m.bared = true; F.m.grin = -0.5; F.m.w = 60; F.m.open = 0.06 * Math.sin(t * 13); F.m.nerv = 0; F.wink = false; } }
      if (A.on) { const aim = A.wind * (1 - A.rec); F.lid = lerp(F.lid, 0.42, aim); F.browL = lerp(F.browL, 0.5, aim); F.browR = lerp(F.browR, 0.5, aim); if (!F.m.bared) F.m.open = Math.max(F.m.open, A.strike * (1 - A.rec) * 0.9); }
      if (castK > 0.05) { F.mode = "smug"; if (!F.m.bared) { F.m.grin = 1; F.m.w = 62; F.m.open = 0.2; } F.upL = F.upR = 4 * castK; F.sparkle = castK; }
      if (talk > 0.05) F.m.open = Math.max(F.m.open, F.m.bared ? 0.25 + talk * 0.5 : 0.15 + talk * 0.75);
      if (gloat > 0.1) { F.mode = "happy"; F.m.bared = false; F.m.grin = 1; F.m.w = 62; F.m.open = 0.6 + 0.35 * Math.sin(t * 22); F.m.nerv = 0; F.browL = F.browR = -0.2; F.upL = F.upR = 4; }
      if (sq > 0.25) { F.mode = "pain"; F.m.mode = "wave"; F.browL = F.browR = -0.6; }
      if (stun) { F.mode = "spiral"; F.lid = 0; F.wide = 1.1; F.m.mode = "zig"; F.browL = F.browR = -0.5; F.upL = F.upR = 2; }
      if (dead) { F.mode = zipU > 0.85 ? "x" : "open"; F.lid = 0; F.wide = 1.3; F.pr = 2.4; F.lx = Math.sin(t * 23) * 0.6; F.ly = Math.cos(t * 19) * 0.6; F.browL = F.browR = -0.9; F.upL = F.upR = 5; F.m.mode = zipU > 0.85 ? "wave" : "o"; F.m.open = 1; F.wink = false; }
      if (faceA > 0.02) { c.globalAlpha = alpha * faceA; drawFace(c, K, F); c.globalAlpha = alpha; }
      if (dmg >= 2) patch(c, 21, -33, -0.5, 22, 10);
      if (rt > 0.3 && !dead) {                                      // veine de colère sur la tempe
        const k = 0.8 + 0.2 * Math.sin(t * 15); c.strokeStyle = col("#8f0f1c", rt); c.lineWidth = 2.6; c.lineCap = "round";
        c.save(); c.translate(27, -18); c.scale(k, k);
        for (let i = 0; i < 4; i++) { c.rotate(Math.PI / 2); c.beginPath(); c.moveTo(2.5, 7); c.quadraticCurveTo(2.5, 2.5, 7, 2.5); c.stroke(); }
        c.restore();
        c.strokeStyle = col("#8f0f1c", 0.55 * rt); c.lineWidth = 1.5; c.beginPath(); c.moveTo(-38, -4); c.lineTo(-33, -10); c.lineTo(-35, -17); c.moveTo(-33, -10); c.lineTo(-28, -12); c.stroke();
      }
      c.restore();

      // sueur (nerveux, bouclier tombé, dégâts), vapeur (rage), étoiles (étourdi)
      const nSweat = dead ? 0 : Math.min(3, (nerv > 0.3 ? 2 : 0) + (dmg >= 1 ? 1 : 0) + (rt > 0.5 ? 1 : 0));
      c.fillStyle = "rgba(176,220,255,0.92)";
      for (let i = 0; i < nSweat; i++) { const u = (t * 0.85 + i * 0.37) % 1; c.globalAlpha = alpha * (1 - u * u); drop(c, hx + R * (0.92 - i * 0.62) + (i === 1 ? -R * 0.9 : 0), hy - R * 0.45 + u * R * 1.0, 0.95); }
      c.globalAlpha = alpha;
      if (rt > 0.4 && !dead) {
        for (let i = 0; i < 4; i++) { const u = (t * 1.3 + i * 0.25) % 1, sgn = i % 2 ? 1 : -1; c.fillStyle = "rgba(255,240,236," + 0.5 * (1 - u) * rt + ")"; c.beginPath(); c.arc(hx + sgn * (R * 0.95 + u * 12), hy - R * 0.5 - u * 26, 4 + u * 7, 0, TAU); c.fill(); }
      }
      if (stun) { c.fillStyle = col(C.lamp); for (let k = 0; k < 3; k++) { const a = time * 4 + k * 2.1; star4(c, hx + Math.cos(a) * R * 0.95, hy - R * 1.25 + Math.sin(a) * 7, 7, a); } }
      if (dmg >= 3 && !dead && enter >= 1) { c.save(); c.translate(hx, hy); const a = -0.75; c.translate(Math.cos(a) * R, Math.sin(a) * R); c.lineCap = "round"; c.lineWidth = 2; for (let j = -1; j <= 1; j++) { const u = (t * 2.2 + (j + 1) / 3) % 1, da = a + j * 0.3, r0 = 4 + u * 16; c.strokeStyle = "rgba(240,244,255," + 0.8 * (1 - u) + ")"; c.beginPath(); c.moveTo(Math.cos(da) * r0, Math.sin(da) * r0); c.lineTo(Math.cos(da) * (r0 + 7), Math.sin(da) * (r0 + 7)); c.stroke(); } c.restore(); }

      // --- bras avant (côté joueur) : il agite le contrat, s'en protège, ou arme puis lance son avion ---
      const S1 = { x: -rx * 0.76, y: cy - ry * 0.44 };
      let H1 = { x: -124, y: -14 + Math.sin(t * 2) * 4 }, bend1 = { x: -4, y: 20 }, paperRot = -0.2 + Math.sin(t * 2) * 0.06, held = "contract";
      if (threat > 0.05) { H1 = { x: lerp(H1.x, -86, threat), y: lerp(H1.y, 22, threat) }; paperRot = lerp(paperRot, 0.12, threat); }
      if (castK > 0.05) { H1 = { x: lerp(H1.x, -118, castK), y: lerp(H1.y, -74, castK) }; paperRot -= 0.25 * castK; }
      if (gloat > 0.1) { H1 = { x: -128, y: -44 + bounce * 1.5 }; paperRot = -0.35 + Math.sin(t * 22) * 0.12; }
      if (A.on) {
        const w = easeOut(A.wind), s = easeIn(A.strike), r = easeInOut(A.rec), idle = H1;
        if (A.strike <= 0) { H1 = { x: lerp(idle.x, -84, w), y: lerp(idle.y, -146, w) }; bend1 = { x: -22 * w, y: 8 }; held = A.wind > 0.3 ? "plane" : "fold"; }
        else if (A.rec <= 0) { H1 = { x: lerp(-84, -156, s), y: lerp(-146, -22, s) }; bend1 = { x: -10, y: -10 * s }; held = "none"; }
        else { H1 = { x: lerp(-156, idle.x, r), y: lerp(-22, idle.y, r) }; held = A.rec > 0.5 ? "contract" : "none"; paperK = seg(A.rec, 0.5, 0.95); }
      }
      if (dead) { H1 = { x: -rx - 26, y: cy + ry * 0.4 + Math.sin(t * 29) * 8 }; bend1 = { x: -6, y: 0 }; held = "none"; }
      if (armK > 0.05) {
        const hxx = lerp(S1.x, H1.x, armK), hyy = lerp(S1.y, H1.y, armK);
        const hd = arm(c, K, S1.x, S1.y, hxx, hyy, bend1.x * armK, bend1.y * armK, aw, "open");
        if (held === "contract") { drawContract(c, K, hd.x - 9, hd.y - 27, paperRot, paperK * Math.min(1, inf)); hand(c, K, hd.x, hd.y, aw * 0.5, "open"); if (paperK > 0.5 && (castK > 0.05 || (t % 3.1) < 0.5)) { const k = castK > 0.05 ? castK : Math.sin(((t % 3.1) / 0.5) * Math.PI); c.fillStyle = "rgba(255,255,255," + 0.95 * k + ")"; star4(c, hd.x - 24, hd.y - 52, 10 * k, t); } }
        else if (held === "fold") { drawContract(c, K, hd.x - 6, hd.y - 20, paperRot - 0.4, 1 - A.wind / 0.3 * 0.5); hand(c, K, hd.x, hd.y, aw * 0.5, "open"); }
        else if (held === "plane") { c.save(); c.translate(hd.x - 4, hd.y - 8); c.rotate(Math.PI + 0.5 - 0.3 * A.wind); c.scale(1.25, -1.25); plane(c, rt > 0.5); c.restore(); hand(c, K, hd.x, hd.y, aw * 0.5, "open"); }
      }
    }
  };
}
