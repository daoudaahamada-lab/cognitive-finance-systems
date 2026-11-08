/* Étage 4 — L'Hydre des Connecteurs : un multiprise géant dont chaque câble finit en tête de connecteur.
   La tête principale (à gauche, la plus grosse) porte le port lumineux : c'est la cible critique.
   Les têtes leurres (b.mech.heads.count) sont les outils inutiles qu'on lui a branchés. */
BOSSES[4] = {
  palette: { main: "#c6e84a", dark: "#1a2233", accent: "#7fe3ff", eye: "#c6e84a", rage: "#ff7a3d" },
  hit: { rx: 135, ry: 102, coreR: 24 },
  top: 118,
  attackFrom: { x: -140, y: -52 },
  castLean: -0.12,
  critLabel: "TÊTE PRINCIPALE",
  lines: {
    hit: ["Un outil de moins…", "Ma sélection d’outils !", "Grr, tu filtres trop bien."],
    crit: ["Ma tête principale ?!", "Pas le port central !"],
    wrong: ["Encore un outil pour moi !", "Charge tout, on verra bien.", "Plus de contexte, plus de chaos."],
    timeout: ["Je cherche encore parmi mes 140 outils…", "Trop lent, je me branche ailleurs."],
    rage: "Branchez-moi TOUS les serveurs MCP !",
    special: {
      grow: ["Une tête de plus ! Un outil de plus !", "Je repousse, tu vois ?", "Encore un connecteur, gratuit !"],
      cut: ["Ma tête… tu l’as débranchée !", "Allowlist ?! Non !", "Tool search… quelle horreur."]
    }
  },
  intro: {
    title: "Têtes leurres",
    text: "Chaque erreur lui fait pousser une tête de connecteur inutile : un tir sur un leurre ne peut pas être critique et sa barre d’attaque accélère. Chaque bonne réponse en coupe une : vise la tête principale, celle au port lumineux."
  },
  mechanics: ["heads"],

  /* Tête principale : flotte, recule à l'armement puis se détend vers la gauche. */
  mainHead(b) {
    let x = -78 + Math.sin(b.t * 1.3) * 7, y = -52 + Math.sin(b.t * 1.7) * 6;
    if (b.atk >= 0) {
      const a = b.atk;
      const k = a < 0.22 ? a / 0.22 : a < 0.34 ? 1 - ((a - 0.22) / 0.12) * 2 : -(1 - Math.min(1, (a - 0.34) / 0.41));
      x += k * 26; y -= k * 6;
    }
    return { x, y };
  },
  weakSpot(b) { return BOSSES[4].mainHead(b); },
  headLocal(i, count, b) {
    const S = [[34, -76], [104, -34], [-104, 42], [104, 48], [-12, 80]];
    const s = S[i % S.length], amp = b.rage ? 11 : 7;
    return { x: s[0] + Math.sin(b.t * 1.5 + i * 1.9) * amp, y: s[1] + Math.cos(b.t * 1.2 + i * 1.3) * amp * 0.8 };
  },

  draw(c, b) {
    const B = BOSSES[4], P = B.palette, fl = b.flash, rage = b.rageT, t = b.time;
    const main = mixv(mixv(P.main, P.rage, rage), C.white, fl * 0.6);
    const eye = mixv(mixv(P.eye, C.bad, rage), C.white, fl);
    const shell = mixv("#2a3550", C.white, fl * 0.7);
    const cable = mixv("#222b45", C.white, fl * 0.5);
    const hub = { x: 10, y: 10 };
    const count = b.mech && b.mech.heads ? b.mech.heads.count : 1;
    const castK = b.cast >= 0 ? Math.sin(Math.min(1, b.cast / 0.9) * Math.PI) : 0;

    // halo
    const ag = c.createRadialGradient(0, 0, 20, 0, 0, 230); ag.addColorStop(0, col(main, 0.18)); ag.addColorStop(1, col(main, 0));
    c.fillStyle = ag; c.fillRect(-240, -220, 480, 440);

    const heads = [];
    for (let i = 0; i < count; i++) heads.push({ p: B.headLocal(i, count, b), main: false, i });
    heads.push({ p: B.mainHead(b), main: true, i: -1 });

    // câbles (derrière le boîtier)
    for (const h of heads) {
      const end = { x: h.p.x + (h.main ? 34 : 24), y: h.p.y };
      const dx = end.x - hub.x, dy = end.y - hub.y, len = Math.max(1, Math.hypot(dx, dy));
      const nx = -dy / len, ny = dx / len, wob = Math.sin(t * 2 + h.i) * 14;
      const c1 = { x: hub.x + dx * 0.35 + nx * (22 + wob), y: hub.y + dy * 0.35 + ny * (22 + wob) };
      const c2 = { x: end.x + 34, y: end.y + Math.sin(t * 1.6 + h.i) * 8 };
      c.lineCap = "round";
      c.strokeStyle = col(cable); c.lineWidth = h.main ? 19 : 14;
      c.beginPath(); c.moveTo(hub.x, hub.y); c.bezierCurveTo(c1.x, c1.y, c2.x, c2.y, end.x, end.y); c.stroke();
      c.save(); c.setLineDash([5, 9]); c.lineDashOffset = -t * 40;
      c.strokeStyle = col(main, h.main ? 0.75 : 0.5); c.lineWidth = h.main ? 5 : 3.5;
      c.beginPath(); c.moveTo(hub.x, hub.y); c.bezierCurveTo(c1.x, c1.y, c2.x, c2.y, end.x, end.y); c.stroke(); c.restore();
      if (b.rage && Math.random() < 0.3) {
        const k = Math.random(), sx = lerp(hub.x, end.x, k) + rand(-10, 10), sy = lerp(hub.y, end.y, k) + rand(-10, 10);
        c.strokeStyle = col(P.accent, 0.9); c.lineWidth = 1.5; c.beginPath(); c.moveTo(sx, sy); c.lineTo(sx + rand(-8, 8), sy + rand(-8, 8)); c.lineTo(sx + rand(-8, 8), sy + rand(-8, 8)); c.stroke();
      }
    }

    // boîtier multiprise (le corps)
    c.save();
    rr(c, -60, -28, 140, 88, 18); c.fillStyle = col(shell); c.fill();
    c.strokeStyle = col(main, 0.8); c.lineWidth = 2.5; c.stroke();
    rr(c, -52, -21, 124, 20, 8); c.fillStyle = "rgba(255,255,255,0.06)"; c.fill();
    // prises
    for (let k = 0; k < 3; k++) {
      const ox = -30 + k * 40, oy = 28;
      c.fillStyle = col(mixv("#141b2d", C.white, fl * 0.5)); c.beginPath(); c.arc(ox, oy, 14, 0, Math.PI * 2); c.fill();
      c.strokeStyle = col(main, 0.45); c.lineWidth = 1.5; c.stroke();
      c.fillStyle = col(main, 0.7); c.fillRect(ox - 6, oy - 5, 4, 10); c.fillRect(ox + 2, oy - 5, 4, 10);
    }
    // voyants de vie
    const lit = Math.ceil(clamp(b.hpFrac, 0, 1) * 6);
    for (let k = 0; k < 6; k++) {
      const on = k < lit;
      c.fillStyle = on ? col(main, 0.95) : "rgba(255,255,255,0.08)";
      c.beginPath(); c.arc(-42 + k * 16, -11, 4.5, 0, Math.PI * 2); c.fill();
    }
    // interrupteur
    rr(c, 56, -18, 16, 30, 5); c.fillStyle = col(mixv(P.rage, C.white, fl)); c.fill();
    c.restore();
    drawCracks(c, b, "rgba(235,250,210,0.85)");

    // têtes
    const tools = ["fetch", "sql", "jira", "s3", "pdf"];
    for (const h of heads) B.drawHead(c, h.p.x, h.p.y, h.main ? 1.7 : 1.2, h.main, b, { main, eye, shell, P, castK, label: h.main ? "MCP" : tools[h.i % tools.length] });

    // étourdi : petites étoiles autour de la tête principale
    if (b.stun > 0) {
      const mh = B.mainHead(b);
      for (let k = 0; k < 3; k++) {
        const a = t * 4 + (k * Math.PI * 2) / 3;
        B.star(c, mh.x + Math.cos(a) * 36, mh.y - 44 + Math.sin(a) * 8, 6, col(P.accent, 0.9));
      }
    }
  },

  drawHead(c, x, y, s, isMain, b, o) {
    const fl = b.flash, t = b.time;
    c.save(); c.translate(x, y);
    const tilt = isMain ? -0.06 + (b.atk >= 0 && b.atk > 0.22 && b.atk < 0.34 ? -0.12 : 0) : Math.sin(t * 1.1 + x * 0.05) * 0.12;
    c.rotate(tilt); c.scale(s * (1 + o.castK * 0.08), s * (1 + o.castK * 0.08));
    // broches métalliques (vers la gauche)
    c.fillStyle = col(mixv(C.metal, C.white, fl)); c.fillRect(-38, -11, 15, 5); c.fillRect(-38, 6, 15, 5);
    // boîtier de la fiche
    rr(c, -25, -19, 48, 38, 10); c.fillStyle = col(o.shell); c.fill();
    c.strokeStyle = col(o.main, isMain ? 0.95 : 0.6); c.lineWidth = isMain ? 2.5 : 2; c.stroke();
    // nervures de préhension
    c.strokeStyle = "rgba(255,255,255,0.14)"; c.lineWidth = 2;
    for (let k = 0; k < 3; k++) { c.beginPath(); c.moveTo(11 + k * 4, -13); c.lineTo(11 + k * 4, 13); c.stroke(); }
    // bouche (fente avant), s'ouvre pendant la riposte ou l'action spéciale
    const open = isMain && b.atk >= 0 ? 6 : o.castK * 4;
    c.fillStyle = "#05070e"; rr(c, -25, -3 - open / 2, 9, 6 + open, 2); c.fill();
    // yeux
    c.globalAlpha = b.stun > 0 ? 0.45 : 1;
    angryEyes(c, 1, -10, isMain ? 9 : 8, 4, o.eye, b.squint, isMain || o.castK > 0.2 ? 10 : 0);
    c.globalAlpha = 1;
    // port lumineux (tête principale) ou voyant (leurres)
    if (isMain) {
      const pulse = 1 + Math.sin(t * 4) * 0.1;
      const g = c.createRadialGradient(-2, 4, 1, -2, 4, 14 * pulse); g.addColorStop(0, "rgba(255,255,255,0.95)"); g.addColorStop(0.4, col(o.main, 0.9)); g.addColorStop(1, col(o.main, 0));
      c.fillStyle = g; c.beginPath(); c.arc(-2, 4, 14 * pulse, 0, Math.PI * 2); c.fill();
    } else {
      c.fillStyle = col(o.main, 0.5 + 0.4 * Math.abs(Math.sin(t * 3 + x))); c.beginPath(); c.arc(-4, 6, 3, 0, Math.PI * 2); c.fill();
    }
    // étiquette d'outil
    c.fillStyle = col(o.main, 0.8); c.font = "700 8px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle";
    c.fillText(o.label, 0, 14);
    c.restore();
  },

  star(c, x, y, r, color) {
    c.fillStyle = color; c.beginPath();
    for (let k = 0; k < 8; k++) { const a = (k * Math.PI) / 4, rr2 = k % 2 ? r * 0.4 : r; c.lineTo(x + Math.cos(a) * rr2, y + Math.sin(a) * rr2); }
    c.closePath(); c.fill();
  }
};
