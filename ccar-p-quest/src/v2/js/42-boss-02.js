/* Étage 2 — Le Sur-Ingénieur : un robot fait de beaucoup trop de modules empilés, avec un gros bouton DEPLOY sur le torse.
   Sous l'usine à gaz se cache un tout petit robot très simple : c'est lui qui reste à la fin. */
{
  const TAU = Math.PI * 2, OY = 16;                            // le robot est dessiné 16 unités sous le centre (la pile monte haut)
  const BX = 0, BY = 18;                                       // bouton DEPLOY, dans le repère du robot
  const INK = "#1b2340", VISOR = "#0c1224";
  const rgba = (v, a) => col(v, a <= 0 ? 0 : a >= 1 ? 1 : Math.round(a * 1000) / 1000);
  const hash = (k) => { const s = Math.sin(k * 91.7 + 12.3) * 43758.5453; return s - Math.floor(s); };

  /* Modules : [x, y au repos, début d'entrée, d'où il arrive (dx, dy), instant de la mort où il se décroche, vitesse latérale, rotation]. */
  const M = {
    pod: [0, 89, 0, 0, 220, 0.66, 14, 0.7], torso: [0, 19, 0.08, 215, -30, 0.56, -26, -0.9],
    shL: [-90, -6, 0.2, -190, -70, 0.4, -90, -2.4], shR: [91, 0, 0.25, 190, 60, 0.33, 100, 2.8], shRh: [96, 16, 0, 0, 0, 0.33, 100, 2.8],
    head: [0, -74, 0.32, -30, -230, 0.47, -46, -1.7],
    s1: [1, -115, 0.44, 140, -200, 0.18, 60, 2.2], s2: [4, -136, 0.52, -140, -200, 0.11, -70, -3], s3: [9, -155, 0.6, 60, -210, 0.04, 90, 3.6], s3h: [64, -98, 0, 0, 0, 0.04, 90, 3.6],
    g1: [94, 54, 0.5, 150, 40, 0.28, 120, 5], g2: [119, 24, 0.54, 150, -20, 0.24, 150, -6],
    t1: [62, 66, 0.62, 0, 0, 0.3, 70, 4], t2: [70, 30, 0.66, 0, 0, 0.2, 130, -5], t3: [-62, 62, 0.64, 0, 0, 0.26, -80, -4],
    r1: [58, -40, 0, 0, 0, 0.08, 120, 4], r2: [-50, -44, 0, 0, 0, 0.14, -110, -4]
  };

  BOSSES[2] = {
    v: 2,
    palette: { main: "#6f86b8", dark: "#26304f", accent: "#f39a3b", eye: "#7fe3ff", rage: "#ff5a36" },
    hit: { rx: 112, ry: 132, coreR: 22 },
    top: 172,
    attackFrom: { x: -122, y: -66 },
    castLean: -0.05,
    weakSpot: () => ({ x: BX, y: BY + OY }),
    critLabel: "DEPLOY ANNULÉ",
    epitaph: "SIMPLIFIÉ",
    lines: {
      hit: ["Ma couche d’abstraction !", "Il me faut un agent de plus.", "Rien de grave, j’ai douze replis.", "Ce module était… décoratif."],
      crit: ["Pas le bouton DEPLOY !", "Tu as visé la mise en prod ?!", "Rollback ! ROLLBACK !"],
      wrong: ["Ajoutons un orchestrateur.", "Trop simple pour être vrai.", "Un agent de plus et ça passe.", "Il manque un diagramme, voilà tout."],
      timeout: ["Mes agents débattent encore…", "Réunion de synchro, désolé.", "Le comité d’architecture délibère."],
      gloat: ["Et ça, ce n’est que le prototype.", "Livré par douze agents. Admire.", "Complexe, donc forcément mieux.", "Clé de 12 ou de 14 ? Les deux."],
      rage: "Plan B : vingt agents et un méta-orchestrateur !",
      special: {
        build: ["Je construis un agent de plus.", "Une tourelle de plus, par précaution.", "Il manque une couche, non ?", "Superviseur du superviseur : en ligne."],
        collapse: ["Mes tourelles… inutiles ?", "Ta solution simple les a rasées !", "Un seul appel ?! C’est de la triche."]
      }
    },
    intro: {
      title: "Tourelles multi-agents",
      text: "À chaque question, il dresse une tourelle « multi-agents » entre toi et lui, qui arrête tes pierres. Une bonne réponse les fait toutes s’effondrer : la solution simple gagne."
    },
    mechanics: ["turrets"],

    init(b) { b.own.dmgSeen = b.dmg || 0; b.own.dmgAt = []; },
    update(b) {
      const o = b.own, dmg = b.dmg || 0;
      if (!o.dmgAt) { o.dmgAt = []; o.dmgSeen = dmg; }
      while (o.dmgSeen < dmg) o.dmgAt[++o.dmgSeen] = b.t;      // l'instant où chaque stade de dégâts commence : les pièces tombent à ce moment
      if (dmg < o.dmgSeen) o.dmgSeen = dmg;
    },

    /* Vol stationnaire lourd : il s'affaisse lentement, puis ses tuyères le remontent d'un coup. En rage, il avance par à-coups. */
    motion(b) {
      const t = b.t || 0, rg = b.rageT || 0;
      const u = (t * 0.3) % 1, sink = u < 0.8 ? easeInOut(u / 0.8) : 1 - easeOut((u - 0.8) / 0.2);
      const cx = Math.sin(t * 0.31) * 13 - 8, cy = sink * 18 - 8 + Math.sin(t * 29) * 0.9 + Math.sin(t * 43 + 1) * 0.6;
      const step = (p, seed) => { const q = t / p, k = Math.floor(q); return lerp(hash(k + seed), hash(k + 1 + seed), backOut(seg(q - k, 0.7, 1))) * 2 - 1; };
      const sx = step(0.62, 3) * 40 - 24 + Math.sin(t * 61) * 1.6, sy = step(0.5, 17) * 30 + Math.sin(t * 53) * 1.8;
      return { x: lerp(cx, sx, rg), y: lerp(cy, sy, rg) };
    },

    /* Projectile : une clé plate qui tournoie. */
    shot: {
      color: "#f39a3b", spin: 13,
      draw(c, s) {
        const hot = s.rage ? 1 : 0, steel = hot ? "#ffd0b0" : "#dfe6f7";
        if (hot) { c.fillStyle = "rgba(255,90,54,0.28)"; c.beginPath(); c.arc(0, 0, 21, 0, TAU); c.fill(); }
        const body = (grow, color) => {
          c.strokeStyle = color; c.fillStyle = color; c.lineCap = "butt";
          rr(c, -12 - grow, -3.6 - grow, 24 + grow * 2, 7.2 + grow * 2, 2); c.fill();
          c.lineWidth = 5.4 + grow * 2; c.beginPath(); c.arc(15.5, 0, 7.4, 0.7, TAU - 0.7); c.stroke();
          c.lineWidth = 4.4 + grow * 2; c.beginPath(); c.arc(-15.5, 0, 5.6, 0, TAU); c.stroke();
        };
        body(1.5, INK); body(0, steel);
        c.fillStyle = "#f39a3b"; c.fillRect(-6, -3.6, 9, 7.2); c.fillStyle = "rgba(255,255,255,0.5)"; c.fillRect(-11, -2.6, 22, 1.4);
      }
    },

    /* Le Bureau d'Études : chantier de nuit, échafaudage et planche à plans, grue à tour, cabane de chantier, caisses. */
    backdrop(c, env) {
      const W = env.W, g = env.groundY, rnd = env.rnd || seeded(1002);
      const line = (x0, y0, x1, y1) => { c.beginPath(); c.moveTo(x0, y0); c.lineTo(x1, y1); c.stroke(); };
      const glow = (x, y, r, a, hue) => { const q = c.createRadialGradient(x, y, 2, x, y, r); q.addColorStop(0, "rgba(" + hue + "," + a + ")"); q.addColorStop(1, "rgba(" + hue + ",0)"); c.fillStyle = q; c.fillRect(x - r, y - r, r * 2, r * 2); };

      // grue à tour : fût en treillis, flèche vers la gauche, contre-flèche et lest à droite
      const mx = W * 0.405, jy = g - 456, jx0 = W * 0.045, jx1 = W * 0.485;
      c.strokeStyle = "#6f5a2c"; c.lineWidth = 2.2;
      line(mx - 8, g, mx - 8, jy); line(mx + 8, g, mx + 8, jy);
      c.lineWidth = 1.3; for (let y = g - 60, k = 0; y > jy; y -= 18, k++) { line(mx - 8, y, mx + 8, y - 18); line(mx + 8, y, mx - 8, y - 18); }
      c.lineWidth = 2; line(jx0, jy, jx1, jy); line(jx0, jy + 11, jx1 - 34, jy + 11);
      c.lineWidth = 1.2; for (let x = jx0; x < mx - 12; x += 13) { line(x, jy + 11, x + 6.5, jy); line(x + 6.5, jy, x + 13, jy + 11); }
      c.lineWidth = 1.4; line(mx, jy - 40, jx0 + 30, jy); line(mx, jy - 40, jx1 - 6, jy); c.lineWidth = 2.4; line(mx, jy - 40, mx, jy);
      c.fillStyle = "#4b4a55"; c.fillRect(jx1 - 30, jy + 2, 26, 20);                                   // lest
      c.fillStyle = "#57482a"; c.fillRect(mx - 13, jy - 4, 26, 24); c.fillStyle = "rgba(243,184,65,0.75)"; c.fillRect(mx - 9, jy + 1, 10, 9);   // cabine
      c.fillStyle = "#6f5a2c"; c.fillRect(W * 0.325 - 9, jy + 11, 18, 6);                               // chariot

      // échafaudage : montants, lisses, croisillons, platelages
      const x0 = W * 0.022, x1 = W * 0.292, xm = (x0 + x1) / 2, top = g - 356;
      c.strokeStyle = "#3b4464"; c.lineWidth = 3.4; for (const x of [x0, xm, x1]) line(x, top - 14, x, g);
      c.lineWidth = 2; for (const y of [top, g - 176, g - 92]) line(x0 - 6, y, x1 + 6, y);
      c.lineWidth = 1.5; c.strokeStyle = "#333b59"; line(x0, g - 176, xm, g - 92); line(xm, g - 176, x0, g - 92); line(xm, g - 176, x1, g - 92); line(x1, g - 176, xm, g - 92);
      c.fillStyle = "#4d3d36"; c.fillRect(x0 - 10, g - 181, x1 - x0 + 20, 6); c.fillRect(x0 - 10, top - 4, x1 - x0 + 20, 6);
      c.fillStyle = "#6a554a"; c.fillRect(x0 - 10, g - 181, x1 - x0 + 20, 1.6); c.fillRect(x0 - 10, top - 4, x1 - x0 + 20, 1.6);

      // la planche à plans : un schéma absurdement compliqué
      const bx = x0 + 9, by = g - 338, bw = x1 - x0 - 18, bh = 150;
      c.fillStyle = "#2a2f47"; c.fillRect(bx - 4, by - 4, bw + 8, bh + 8);
      const bg = c.createLinearGradient(0, by, 0, by + bh); bg.addColorStop(0, "#1c4a8c"); bg.addColorStop(1, "#133468");
      c.fillStyle = bg; c.fillRect(bx, by, bw, bh);
      c.strokeStyle = "rgba(150,195,255,0.1)"; c.lineWidth = 1;
      for (let x = bx + 12; x < bx + bw; x += 12) line(x, by, x, by + bh);
      for (let y = by + 12; y < by + bh; y += 12) line(bx, y, bx + bw, y);
      const cols = 5, rows = 4, nodes = [];
      for (let r = 0; r < rows; r++) for (let k = 0; k < cols; k++) nodes.push([bx + 20 + (k + 0.5) * ((bw - 40) / cols) + (rnd() - 0.5) * 9, by + 22 + (r + 0.5) * ((bh - 44) / rows) + (rnd() - 0.5) * 7, rnd()]);
      c.strokeStyle = "rgba(170,210,255,0.42)"; c.lineWidth = 1;
      for (let i = 0; i < nodes.length; i++) for (let k = 0; k < 2; k++) { const a = nodes[i], q = nodes[(i + 1 + Math.floor(rnd() * (nodes.length - 1))) % nodes.length]; c.beginPath(); c.moveTo(a[0], a[1]); if (rnd() < 0.5) c.lineTo(q[0], a[1]); else c.lineTo(a[0], q[1]); c.lineTo(q[0], q[1]); c.stroke(); }
      for (const n of nodes) {
        c.fillStyle = "#17407c"; c.strokeStyle = "rgba(205,228,255,0.9)"; c.lineWidth = 1.2;
        if (n[2] < 0.22) { c.beginPath(); c.arc(n[0], n[1], 6, 0, TAU); c.fill(); c.stroke(); }
        else if (n[2] < 0.36) { c.beginPath(); c.moveTo(n[0], n[1] - 7); c.lineTo(n[0] + 9, n[1]); c.lineTo(n[0], n[1] + 7); c.lineTo(n[0] - 9, n[1]); c.closePath(); c.fill(); c.stroke(); }
        else { c.fillRect(n[0] - 10, n[1] - 5.5, 20, 11); c.strokeRect(n[0] - 10, n[1] - 5.5, 20, 11); c.fillStyle = "rgba(205,228,255,0.6)"; c.fillRect(n[0] - 6, n[1] - 1, 8 + n[2] * 5, 1.6); }
      }
      c.fillStyle = "rgba(205,228,255,0.85)"; c.font = "700 8px " + F_MONO; c.textAlign = "left"; c.textBaseline = "middle"; c.fillText("ARCHI v37 — 20 AGENTS", bx + 6, by + 9);
      c.strokeStyle = "rgba(205,228,255,0.6)"; c.strokeRect(bx + bw - 44, by + bh - 20, 40, 16); c.fillStyle = "rgba(205,228,255,0.5)"; c.fillRect(bx + bw - 40, by + bh - 15, 26, 1.5); c.fillRect(bx + bw - 40, by + bh - 10, 18, 1.5);
      // le plan simple, relégué sur un post-it dans le coin
      c.save(); c.translate(bx + bw - 20, by + 21); c.rotate(0.12); c.fillStyle = "#f2d264"; c.fillRect(-17, -13, 34, 26); c.strokeStyle = "#5a4a1c"; c.lineWidth = 1.3; c.strokeRect(-12, -4, 8, 8); c.strokeRect(5, -4, 8, 8); line(-4, 0, 4, 0); line(1.5, -2.5, 4, 0); line(1.5, 2.5, 4, 0); c.fillStyle = "#d9544a"; c.beginPath(); c.arc(0, -12, 2.4, 0, TAU); c.fill(); c.restore();
      // projecteur de chantier au-dessus de la planche
      glow(xm, by - 6, 150, 0.2, "255,214,150"); c.fillStyle = "#2a2f47"; c.fillRect(xm - 9, top - 16, 18, 9); c.fillStyle = "#ffe6a8"; c.fillRect(xm - 7, top - 9, 14, 3);

      // cabane de chantier : le bureau d'études
      const hx = W * 0.447, hw = W * 0.152, hy = g - 124;
      c.fillStyle = "#2b3350"; c.fillRect(hx, hy, hw, 124); c.fillStyle = "#39436a"; c.fillRect(hx - 3, hy - 5, hw + 6, 7);
      c.strokeStyle = "rgba(20,26,46,0.6)"; c.lineWidth = 1; for (let x = hx + 9; x < hx + hw; x += 9) line(x, hy + 4, x, g - 58);
      glow(hx + hw * 0.36, hy + 38, 60, 0.3, "243,184,65");
      c.fillStyle = "#f3c35a"; c.fillRect(hx + 12, hy + 22, hw * 0.5, 30); c.strokeStyle = "#1c2238"; c.lineWidth = 2; c.strokeRect(hx + 12, hy + 22, hw * 0.5, 30); line(hx + 12 + hw * 0.25, hy + 22, hx + 12 + hw * 0.25, hy + 52);
      c.fillStyle = "#1c2238"; c.beginPath(); c.arc(hx + 30, hy + 52, 9, Math.PI, 0); c.fill(); c.fillRect(hx + 26, hy + 34, 8, 12); c.fillRect(hx + 48, hy + 40, 22, 3); c.fillRect(hx + 60, hy + 30, 2.5, 12);   // un ingénieur, sa lampe d'architecte
      c.fillStyle = "#222a44"; c.fillRect(hx + hw - 30, hy + 20, 21, 104); c.fillStyle = "#f39a3b"; c.fillRect(hx + hw - 14, hy + 56, 3, 3);
      c.fillStyle = "#141a2e"; c.fillRect(hx + 8, hy + 5, hw - 16, 12); c.fillStyle = "rgba(243,184,65,0.9)"; c.font = "700 8px " + F_MONO; c.textAlign = "center"; c.fillText("BUREAU D’ÉTUDES", hx + hw / 2, hy + 11.5);

      // caisses de modules en attente, à droite
      const crate = (x, y, w, h, tag) => {
        c.fillStyle = "#4a3b35"; c.fillRect(x, y, w, h); c.strokeStyle = "#2c2320"; c.lineWidth = 1.5; c.strokeRect(x + 0.5, y + 0.5, w - 1, h - 1);
        c.strokeStyle = "rgba(30,22,20,0.55)"; c.lineWidth = 1; line(x + 5, y + 1, x + 5, y + h - 1); line(x + w - 5, y + 1, x + w - 5, y + h - 1);
        c.fillStyle = "#65524a"; c.fillRect(x + 1, y + 1, w - 2, 2);
        if (tag) { c.fillStyle = "rgba(232,220,200,0.55)"; c.font = "700 7px " + F_MONO; c.textAlign = "center"; c.fillText(tag, x + w / 2, y + h / 2 + 1); }
      };
      const kx = W * 0.815;
      crate(kx, g - 92, 40, 36, "AGENT"); crate(kx + 43, g - 96, 46, 40, "AGENT"); crate(kx + 92, g - 88, 34, 32, "");
      crate(kx + 18, g - 124, 38, 32, "MÉTA"); crate(kx + 60, g - 130, 40, 34, "AGENT"); crate(kx + 40, g - 156, 34, 30, "");
      // cône et barrière, au pied de la grue
      c.fillStyle = "#d9772f"; c.beginPath(); c.moveTo(W * 0.63, g - 84); c.lineTo(W * 0.63 + 8, g - 56); c.lineTo(W * 0.63 - 8, g - 56); c.closePath(); c.fill(); c.fillStyle = "#f2ead7"; c.fillRect(W * 0.63 - 4.5, g - 72, 9, 4);
      c.fillStyle = "#39436a"; c.fillRect(W * 0.67, g - 86, 3, 30); c.fillRect(W * 0.76, g - 86, 3, 30);
      for (let k = 0; k < 6; k++) { c.fillStyle = k % 2 ? "#f2ead7" : "#d9544a"; c.fillRect(W * 0.67 + 3 + (k * (W * 0.09 - 3)) / 6, g - 82, (W * 0.09 - 3) / 6, 8); }
    },

    /* Décor animé : la grue apporte encore un module, son crochet se balance ; le feu de balisage clignote. */
    ambient(c, env) {
      const W = env.W, g = env.groundY, t = env.time || 0;
      const tx = W * 0.325, ty = g - 439, sw = Math.sin(t * 0.9) * 0.06 + Math.sin(t * 2.3) * 0.012, L = 132;
      const hx = tx + Math.sin(sw) * L, hy = ty + Math.cos(sw) * L;
      c.strokeStyle = "#57482a"; c.lineWidth = 1.4; c.beginPath(); c.moveTo(tx, ty); c.lineTo(hx, hy); c.stroke();
      c.save(); c.translate(hx, hy); c.rotate(-sw * 1.4);
      c.fillStyle = "#6f5a2c"; c.fillRect(-5, -4, 10, 8);
      c.strokeStyle = "#8a8f9f"; c.lineWidth = 1.1; c.beginPath(); c.moveTo(0, 4); c.lineTo(-17, 20); c.moveTo(0, 4); c.lineTo(17, 20); c.stroke();
      c.fillStyle = "#5d77ad"; c.fillRect(-19, 20, 38, 24); c.strokeStyle = "#1b2340"; c.lineWidth = 1.6; c.strokeRect(-19, 20, 38, 24);
      c.fillStyle = "rgba(255,255,255,0.2)"; c.fillRect(-16, 22.5, 32, 2); c.fillStyle = "#e6ecff"; c.font = "700 7px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText("AGENT+1", 0, 33.5);
      c.restore();
      const on = (t * 0.9) % 1 < 0.45, mx = W * 0.405, my = g - 498;
      if (on) { const q = c.createRadialGradient(mx, my, 1, mx, my, 26); q.addColorStop(0, "rgba(255,90,70,0.55)"); q.addColorStop(1, "rgba(255,90,70,0)"); c.fillStyle = q; c.fillRect(mx - 26, my - 26, 52, 52); }
      c.fillStyle = on ? "#ff6a52" : "#6b2a26"; c.beginPath(); c.arc(mx, my, 3.2, 0, TAU); c.fill();
    },

    draw(c, b) {
      const t = b.t || 0, fl = b.flash || 0, rg = b.rageT || 0, dmg = b.dmg || 0, o = b.own || {};
      const e = b.enter ?? 1, dying = b.dying ?? -1, dead = dying >= 0, d = dead ? dying : 0;
      const look = b.look || { x: -1, y: 0 }, beat = b.beat || 0, threat = b.threat || 0, gloat = b.gloat || 0, talk = b.talk || 0;
      const stun = (b.stun || 0) > 0, sq = b.squint || 0, GA = c.globalAlpha;
      const castK = b.cast >= 0 ? Math.sin(clamp(b.cast / 0.9, 0, 1) * Math.PI) : 0;
      const ap = atkPose(b), aw = !ap.on ? 0 : easeOut(ap.wind), swing = !ap.on ? 0 : easeOut(ap.strike), rc = !ap.on ? 0 : easeInOut(ap.rec);
      const since = (k) => (o.dmgAt && o.dmgAt[k] != null ? t - o.dmgAt[k] : 99);
      const rgB = backOut(rg), lx = clamp(look.x, -1, 1), ly = clamp(look.y, -1, 1), wfl = fl * 0.7;
      const live = dead ? 1 - seg(d, 0, 0.5) : 1;                                                       // l'agitation retombe quand il meurt
      const boot = seg(e, 0.86, 1), lit = e >= 1 ? 1 : boot;
      const K = (hex, a, w) => rgba(mixv(mixv(hex, "#d2502e", rg * 0.22), C.white, Math.max(wfl, w || 0)), a == null ? 1 : a);
      const N = (hex, a) => rgba(mixv(hex, C.white, wfl), a == null ? 1 : a);
      const inkC = N(INK), eyeHex = mixv(mixv("#7fe3ff", "#ff6a4a", rg), C.white, fl);
      const line = (x0, y0, x1, y1) => { c.beginPath(); c.moveTo(x0, y0); c.lineTo(x1, y1); c.stroke(); };
      const box = (x, y, w, h, r, fill, wh) => { rr(c, x, y, w, h, r); c.fillStyle = K(fill, 1, wh); c.fill(); c.lineWidth = 2.2; c.strokeStyle = inkC; c.stroke(); c.fillStyle = "rgba(255,255,255,0.17)"; c.fillRect(x + r * 0.7, y + 2.4, w - r * 1.4, 2.4); c.fillStyle = "rgba(10,14,30,0.2)"; c.fillRect(x + r * 0.7, y + h - 5, w - r * 1.4, 2.6); };
      const label = (txt, x, y, size, a) => { c.font = "700 " + size + "px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle"; c.fillStyle = N("#e6ecff", a == null ? 0.85 : a); c.fillText(txt, x, y); };
      const led = (x, y, r, color, on) => { c.fillStyle = N(color, on ? 1 : 0.26); c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill(); };
      const limb = (x0, y0, x1, y1, w, fill) => { c.lineCap = "round"; c.strokeStyle = inkC; c.lineWidth = w + 3.4; line(x0, y0, x1, y1); c.strokeStyle = fill; c.lineWidth = w; c.stroke(); };
      const joint = (x, y, r) => { c.fillStyle = inkC; c.beginPath(); c.arc(x, y, r + 1.6, 0, TAU); c.fill(); c.fillStyle = K("#aab6d6"); c.beginPath(); c.arc(x, y, r * 0.55, 0, TAU); c.fill(); };
      const tape = (x, y, w, h, rot) => { c.save(); c.translate(x, y); c.rotate(rot); c.fillStyle = N("#b9bfcc", 0.96); c.fillRect(-w / 2, -h / 2, w, h); c.fillStyle = "rgba(60,66,84,0.35)"; c.fillRect(-w / 2, -h / 2, 3, h); c.fillRect(w / 2 - 3, -h / 2, 3, h); c.fillRect(-w / 2, h / 2 - 2, w, 2); c.restore(); };
      const spark = (x, y, s, ph) => { const k = Math.sin(t * 17 + ph); if (k < 0.2) return; c.strokeStyle = rgba("#fff3b0", k); c.lineWidth = 1.7; c.lineCap = "round"; for (let i = 0; i < 4; i++) { const a = i * 1.57 + ph + Math.floor(t * 9) * 0.7, r = s * (0.5 + 0.5 * hash(i + Math.floor(t * 12) + ph)); line(x + Math.cos(a) * 2, y + Math.sin(a) * 2, x + Math.cos(a) * r, y + Math.sin(a) * r); } };
      const puffs = (x, y, dx, dy, k, hue) => { for (let i = 0; i < 3; i++) { const p = (t * 1.1 + i / 3) % 1; c.fillStyle = rgba(hue, 0.34 * (1 - p) * k); c.beginPath(); c.arc(x + dx * p + Math.sin(t * 3 + i * 2) * 3 * p, y + dy * p, 4 + p * 11, 0, TAU); c.fill(); } };
      let pk = 0;                                                                                       // avancement d'entrée du dernier module posé
      /** Pose un module : vol d'arrivée puis claquement, chute quand il se décroche (mort, ou dégâts depuis `lost` s). Renvoie l'éclat du claquement, −1 s'il n'y a rien à dessiner. */
      const put = (m, lost) => {
        pk = e >= 1 ? 1 : seg(e, m[2], m[2] + 0.2);
        if (pk <= 0) return -1;
        let x = m[0], y = m[1], r = 0, a = 1, el = -1;
        if (pk < 1) { const p = backOut(pk); x += m[3] * (1 - p); y += m[4] * (1 - p); r = (1 - p) * (m[3] > 0 ? 0.5 : -0.5); a = seg(pk, 0, 0.3); }
        if (dead && d > m[5]) el = (d - m[5]) * T_DIE; else if (lost != null && lost >= 0) el = lost;
        if (el >= 0) { x += m[6] * el; y += -120 * el + 620 * el * el; r += m[7] * el; a *= 1 - seg(y, 96, 168); if (a <= 0.01) return -1; }
        c.save(); c.translate(x, y); c.rotate(r); c.globalAlpha = GA * a;
        return pk < 1 || e >= 1 ? 0 : Math.max(0, 1 - (e - m[2] - 0.2) / 0.07);
      };

      // halo
      const hg = c.createRadialGradient(0, 4, 30, 0, 4, 185);
      hg.addColorStop(0, rgba(mixv("#f39a3b", "#ff5a36", rg), (0.14 + 0.12 * rg) * lit * live)); hg.addColorStop(1, rgba("#f39a3b", 0));
      c.fillStyle = hg; c.fillRect(-185, -181, 370, 370);

      c.save();
      const jit = rg * live, back = aw * (1 - swing), fwd = swing * (1 - rc);
      c.translate(Math.sin(t * 47) * 1.2 * jit + 9 * back - 20 * fwd, OY - Math.abs(Math.sin(t * 12)) * 7 * gloat + Math.sin(t * 61) * 1 * jit + (stun ? 5 : 0));
      c.rotate(0.07 * back - 0.11 * fwd + (stun ? Math.sin(t * 3) * 0.05 : 0) - 0.03 * castK);
      c.scale(1 + 0.05 * fl, 1 - 0.05 * fl);
      c.lineJoin = "round";
      const spin = t * (1.6 + 4.4 * rg + 5 * castK) * live;
      const busy = castK > 0.05 ? Math.sin(t * 26) : Math.sin(t * 3.1);                                 // les petits bras bricolent sans arrêt
      const up = Math.max(gloat, 0);                                                                    // bras levés quand il jubile

      // --- bras de rage, dépliés dans son dos : scie circulaire à gauche, chalumeau à droite ---
      if (rg > 0.02 || (dead && rg > 0)) {
        const k = rgB;
        let w = put(M.r1);
        if (w >= 0) {
          const a1 = lerp(1.2, -0.62, k) + Math.sin(t * 2.2) * 0.06, a2 = lerp(2.6, -1.2, k) + Math.sin(t * 2.9) * 0.1, ex = Math.cos(a1) * 34 * k, ey = Math.sin(a1) * 34 * k, hx = ex + Math.cos(a2) * 32 * k, hy = ey + Math.sin(a2) * 32 * k;
          limb(0, 0, ex, ey, 6, K("#7f8fb0")); limb(ex, ey, hx, hy, 5, K("#8fa5d4")); joint(ex, ey, 4);
          c.save(); c.translate(hx, hy); c.rotate(a2 - 0.5); c.scale(k, k);
          const fk = 0.8 + 0.2 * Math.sin(t * 31); c.fillStyle = "rgba(127,227,255,0.85)"; c.beginPath(); c.moveTo(14, -4); c.quadraticCurveTo(24 + 16 * fk, 0, 14, 4); c.fill(); c.fillStyle = "#fff"; c.beginPath(); c.moveTo(14, -2); c.quadraticCurveTo(20 + 6 * fk, 0, 14, 2); c.fill();
          box(-6, -5, 20, 10, 3, "#c2925a"); c.fillStyle = inkC; c.fillRect(-2, 5, 5, 6);
          c.restore(); c.restore();
        }
        w = put(M.r2);
        if (w >= 0) {
          const a1 = lerp(1.9, -2.0, k) + Math.sin(t * 2.5) * 0.05, a2 = lerp(0.6, -1.4, k) + Math.sin(t * 3.3) * 0.08, ex = Math.cos(a1) * 36 * k, ey = Math.sin(a1) * 36 * k, hx = ex + Math.cos(a2) * 34 * k, hy = ey + Math.sin(a2) * 34 * k;
          limb(0, 0, ex, ey, 6, K("#7f8fb0")); limb(ex, ey, hx, hy, 5, K("#8fa5d4")); joint(ex, ey, 4);
          c.save(); c.translate(hx, hy); c.scale(k, k); c.rotate(t * 14);
          c.fillStyle = N("#dfe6f7"); c.strokeStyle = inkC; c.lineWidth = 1.6; c.beginPath(); for (let i = 0; i < 20; i++) { const a = (i / 20) * TAU, r = i % 2 ? 10 : 14.5; c.lineTo(Math.cos(a) * r, Math.sin(a) * r); } c.closePath(); c.fill(); c.stroke();
          c.fillStyle = K("#f39a3b"); c.beginPath(); c.arc(0, 0, 4, 0, TAU); c.fill();
          c.restore(); c.restore();
        }
      }

      // --- câbles emmêlés (derrière) ---
      const ca = seg(e, 0.6, 0.9) * (1 - seg(d, 0.03, 0.3));
      if (ca > 0.01) {
        c.lineCap = "round"; c.lineWidth = 2.8;
        const cab = (hue, x0, y0, x1, y1, x2, y2, x3, y3, ph) => { c.strokeStyle = N(hue, 0.9 * ca); c.beginPath(); c.moveTo(x0, y0); c.bezierCurveTo(x1, y1 + Math.sin(t * 1.9 + ph) * 5, x2, y2 + Math.cos(t * 1.6 + ph) * 5, x3, y3); c.stroke(); };
        cab("#f39a3b", -86, -28, -128, -80, -84, -112, -44, -98, 0);
        cab("#7fe3ff", 96, -24, 150, -90, 96, -132, 40, -116, 1.3);
        cab("#57c48f", 104, 22, 158, 70, 120, 124, 26, 100, 2.6);
        cab("#ef6b5c", -70, 60, -118, 96, -66, 128, -26, 100, 3.9);
        if (dmg < 3) cab("#f2c14e", 30, -148, 80, -160, 86, -96, 50, -84, 5.2);
      }

      // --- engrenages (derrière le torse) ---
      const gear = (m, r, teeth, dir, lost, wob) => {
        const w = put(m, lost); if (w < 0) return;
        c.scale(backOut(pk), backOut(pk)); c.translate(wob ? Math.cos(spin * 1.3) * 3 : 0, wob ? Math.sin(spin * 1.3) * 3 : 0); c.rotate(spin * dir);
        c.fillStyle = K("#aab6d6", 1, w); c.strokeStyle = inkC; c.lineWidth = 2; c.beginPath();
        for (let i = 0; i < teeth * 2; i++) { const a = (i / (teeth * 2)) * TAU, rad = i % 2 ? r * 0.78 : r; c.lineTo(Math.cos(a - 0.07) * rad, Math.sin(a - 0.07) * rad); c.lineTo(Math.cos(a + 0.07) * rad, Math.sin(a + 0.07) * rad); }
        c.closePath(); c.fill(); c.stroke();
        c.fillStyle = K("#4a5a8c", 1, w); c.beginPath(); c.arc(0, 0, r * 0.42, 0, TAU); c.fill(); c.fillStyle = K("#f39a3b", 1, w); c.beginPath(); c.arc(0, 0, r * 0.16, 0, TAU); c.fill();
        c.restore();
      };
      gear(M.g2, 13, 8, -1.85, dmg >= 3 ? since(3) : -1, false);
      gear(M.g1, 24, 12, 1, -1, dmg >= 3);

      // --- tuyère : flamme puis nacelle ---
      const mu = (t * 0.3) % 1, boost = mu > 0.8 ? 1 - (mu - 0.8) / 0.2 : 0;                              // même rythme que motion()
      let w = put(M.pod);
      if (w >= 0) {
        const ign = seg(e, 0.16, 0.3) * (e < 1 ? 1 : 1), fh = (24 + Math.sin(t * 31) * 4 + Math.sin(t * 47) * 3 + 16 * boost + 14 * rg + 10 * beat) * ign * (dead ? 1 - seg(d, 0.3, 0.66) * 0.6 : 1);
        if (fh > 1) {
          c.fillStyle = rgba(mixv("#f39a3b", "#ff5a36", rg), 0.3); c.beginPath(); c.ellipse(0, 22 + fh * 0.5, 20, fh * 0.85, 0, 0, TAU); c.fill();
          c.fillStyle = rgba(mixv("#ffc566", "#ff7a4a", rg), 0.95); c.beginPath(); c.moveTo(-15, 16); c.quadraticCurveTo(-11, 18 + fh * 0.7, Math.sin(t * 23) * 3, 18 + fh * 1.5); c.quadraticCurveTo(11, 18 + fh * 0.7, 15, 16); c.fill();
          c.fillStyle = "rgba(255,248,224,0.95)"; c.beginPath(); c.moveTo(-7, 16); c.quadraticCurveTo(-5, 18 + fh * 0.4, 0, 18 + fh * 0.8); c.quadraticCurveTo(5, 18 + fh * 0.4, 7, 16); c.fill();
          for (const sd of [-1, 1]) { c.fillStyle = rgba("#ffc566", 0.85); c.beginPath(); c.moveTo(sd * 40 - 4, 2); c.quadraticCurveTo(sd * 42, 4 + fh * 0.5, sd * 40 + 4, 2); c.fill(); }
        }
        c.fillStyle = K("#4a5a8c", 1, w); c.strokeStyle = inkC; c.lineWidth = 2.2;
        c.beginPath(); c.moveTo(-36, -15); c.lineTo(36, -15); c.lineTo(22, 13); c.lineTo(-22, 13); c.closePath(); c.fill(); c.stroke();
        for (const sd of [-1, 1]) { rr(c, sd * 40 - 7, -12, 14, 15, 3); c.fill(); c.stroke(); }
        box(-40, -19, 80, 9, 3, "#8fa5d4", w); rr(c, -24, 11, 48, 7, 3); c.fillStyle = N("#232c4a"); c.fill();
        c.fillStyle = N("#f2c14e"); for (let k = -1; k <= 1; k++) c.fillRect(k * 14 - 4, 0, 8, 3);
        c.restore();
      }

      // --- le petit robot tout simple qui se cachait dessous (visible quand tout est tombé) ---
      const tiny = dead ? seg(d, 0.5, 0.6) : 0, endK = 1 - easeIn(seg(d, 0.93, 1));
      const tinyBob = Math.sin(t * 5) * 2;
      if (tiny > 0 && endK > 0.01) {
        c.save(); c.translate(BX, BY + tinyBob); c.scale(endK, endK);
        const rise = backOut(seg(d, 0.56, 0.68)), fh = 12 + Math.sin(t * 33) * 3;
        c.fillStyle = "rgba(255,197,102,0.95)"; c.beginPath(); c.moveTo(-7, 26); c.quadraticCurveTo(0, 30 + fh * 1.6, 7, 26); c.fill();
        c.fillStyle = N("#4a5a8c"); rr(c, -9, 24, 18, 7, 3); c.fill();
        limb(-24, 2, -36, 12 + Math.sin(t * 6) * 2, 3.4, N("#8fa5d4"));                                    // bras gauche, ballant
        box(-16, -28 - 22 * rise, 32, 22, 7, "#8fa5d4");                                                   // petite tête
        rr(c, -12, -24 - 22 * rise, 24, 13, 4); c.fillStyle = VISOR; c.fill();
        const blink = (t * 0.9) % 1 < 0.08, ex = Math.sin(t * 2.4) * 2.2;
        c.fillStyle = "#7fe3ff"; if (blink) { c.fillRect(-8 + ex, -18 - 22 * rise, 5, 1.6); c.fillRect(3 + ex, -18 - 22 * rise, 5, 1.6); } else { c.beginPath(); c.arc(-5.5 + ex, -17.5 - 22 * rise, 2.6, 0, TAU); c.arc(5.5 + ex, -17.5 - 22 * rise, 2.6, 0, TAU); c.fill(); }
        c.restore();
      }

      // --- épaules ---
      const shoulderR = () => {
        box(-19, -26, 38, 52, 7, "#7f8fb0", w); label("A7", 0, -14, 9); c.fillStyle = N(VISOR); c.beginPath(); c.arc(0, 8, 9, 0, TAU); c.fill();
        c.strokeStyle = N(rg > 0.5 ? "#ff6a4a" : "#57c48f"); c.lineWidth = 2; const na = rg > 0.5 ? -0.5 + Math.sin(t * 40) * 0.12 : -2.2 + Math.sin(t * 1.7) * 0.7; line(0, 8, Math.cos(na) * 7, 8 + Math.sin(na) * 7);
        // bras-marteau : il se tape sur la tête pour « faire tenir » la pile
        const limp = dmg >= 2, a1 = limp ? 1.9 : -1.95 - 0.5 * up, a2 = limp ? 1.5 + Math.sin(t * 2.4) * 0.2 : -2.75 + Math.max(0, busy) * 0.5 - 0.3 * up, k = backOut(seg(e, 0.66, 0.86));
        if (k > 0.02) { const px = 4, py = -26, ex = px + Math.cos(a1) * 18 * k, ey = py + Math.sin(a1) * 18 * k, hx = ex + Math.cos(a2) * 17 * k, hy = ey + Math.sin(a2) * 17 * k; limb(px, py, ex, ey, 4.4, K("#8fa5d4")); limb(ex, ey, hx, hy, 4, K("#8fa5d4")); joint(ex, ey, 3); c.save(); c.translate(hx, hy); c.rotate(a2); c.scale(k, k); c.fillStyle = N("#8a6a4a"); c.fillRect(0, -1.6, 10, 3.2); box(8, -7, 9, 14, 2, "#4a5a8c"); c.restore(); }
      };
      w = put(M.shL);
      if (w >= 0) {
        box(-18, -24, 36, 48, 7, "#6f86b8", w); label("A1", 0, -13, 9); led(-9, 14, 2.6, C.ok, lit && Math.sin(t * 5) > -0.3); led(0, 14, 2.6, C.lamp, lit && Math.sin(t * 3.3 + 1) > 0);
        c.strokeStyle = N(INK, 0.5); c.lineWidth = 1.4; for (let k = 0; k < 3; k++) line(-11, -2 + k * 4, 11, -2 + k * 4);
        if (rg > 0.05) {                                                                                 // gyrophare d'alerte
          const gk = rgB; c.fillStyle = N("#232c4a"); c.fillRect(-8, -24 - 4 * gk, 16, 4 * gk);
          c.fillStyle = rgba("#ff5a36", 0.22 * gk); const ga = t * 9; c.beginPath(); c.moveTo(0, -30); c.lineTo(Math.cos(ga) * 44, -30 + Math.sin(ga) * 14 - 8); c.lineTo(Math.cos(ga) * 44, -30 + Math.sin(ga) * 14 + 8); c.fill();
          c.fillStyle = N(Math.sin(t * 18) > 0 ? "#ff8a5c" : "#ff5a36"); c.beginPath(); c.arc(0, -24 - 4 * gk, 7 * gk, Math.PI, 0); c.fill(); c.strokeStyle = inkC; c.lineWidth = 1.6; c.stroke();
        }
        c.restore();
      }
      if (dmg >= 2 && !(e < 1)) {                                                                         // l'épaule droite pend au bout de ses câbles, puis tombe
        w = put(M.shRh, dmg >= 3 ? since(3) : -1);
        if (w >= 0) { c.rotate(0.38 + Math.sin(t * 2.4) * 0.07); c.strokeStyle = N("#7fe3ff", 0.9); c.lineWidth = 2.4; line(-8, -26, -20, -46); c.strokeStyle = N("#f2c14e", 0.9); line(6, -26, -12, -44); shoulderR(); c.restore(); }
        spark(74, -22, 9, 1.3);
      } else { w = put(M.shR); if (w >= 0) { shoulderR(); c.restore(); } }

      // --- fer à souder (perdu au stade 2) ---
      w = put(M.t2, dmg >= 2 ? since(2) : -1);
      if (w >= 0) {
        const k = backOut(pk), a1 = -0.55 + busy * 0.12 - 0.5 * up, a2 = -1.9 + busy * 0.22 - 0.3 * up, ex = Math.cos(a1) * 19 * k, ey = Math.sin(a1) * 19 * k, hx = ex + Math.cos(a2) * 16 * k, hy = ey + Math.sin(a2) * 16 * k;
        limb(0, 0, ex, ey, 4.4, K("#8fa5d4")); limb(ex, ey, hx, hy, 4, K("#8fa5d4")); joint(ex, ey, 3);
        c.save(); c.translate(hx, hy); c.rotate(a2); c.scale(k, k); box(-2, -3, 12, 6, 2, "#f39a3b"); c.strokeStyle = N("#dfe6f7"); c.lineWidth = 2; line(10, 0, 19, 0); c.restore();
        if (!dead && e >= 1) spark(hx + Math.cos(a2) * 19, hy + Math.sin(a2) * 19, 6, 4.1);
        c.restore();
      } else if (dmg >= 2 && !dead) spark(72, 30, 8, 2.2);

      // --- torse ---
      const button = (wh) => {
        const pulse = 1 + Math.sin(t * (5 + 6 * rg)) * 0.06 + 0.1 * beat, on = dead ? 1 : lit;
        const q = c.createRadialGradient(BX, BY, 6, BX, BY, 46 * pulse); q.addColorStop(0, rgba("#ef6b5c", 0.5 * on)); q.addColorStop(1, rgba("#ef6b5c", 0)); c.fillStyle = q; c.beginPath(); c.arc(BX, BY, 46 * pulse, 0, TAU); c.fill();
        c.fillStyle = inkC; c.beginPath(); c.arc(BX, BY, 30, 0, TAU); c.fill();
        c.lineWidth = 6; c.strokeStyle = N("#f2c14e"); c.beginPath(); c.arc(BX, BY, 25.5, 0, TAU); c.stroke();
        c.setLineDash([8, 8.02]); c.strokeStyle = N("#232c4a"); c.beginPath(); c.arc(BX, BY, 25.5, t * 0.4 * live, t * 0.4 * live + TAU); c.stroke(); c.setLineDash([]);
        const press = 1 - 0.1 * fl, dg = c.createRadialGradient(BX - 6, BY - 7, 2, BX, BY, 21);
        dg.addColorStop(0, N(mixv("#ffb0a2", "#7a2a22", 1 - on))); dg.addColorStop(1, rgba(mixv(mixv("#d23a2c", "#5a1d18", 1 - on), C.white, Math.max(wfl, wh || 0) * 0.6), 1));
        c.fillStyle = dg; c.beginPath(); c.arc(BX, BY, 20.5 * press, 0, TAU); c.fill(); c.lineWidth = 1.8; c.strokeStyle = inkC; c.stroke();
        c.strokeStyle = "rgba(255,255,255,0.5)"; c.lineWidth = 2.2; c.lineCap = "round"; c.beginPath(); c.arc(BX, BY, 15.5, Math.PI * 1.12, Math.PI * 1.5); c.stroke();
        c.font = "700 8px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle"; c.fillStyle = rgba("#fff4f0", 0.5 + 0.5 * on); c.fillText("DEPLOY", BX, BY + 1);
      };
      w = put(M.torso);
      if (w >= 0) {
        const tg = c.createLinearGradient(0, -55, 0, 55); tg.addColorStop(0, K("#8fa5d4", 1, w)); tg.addColorStop(0.55, K("#6f86b8", 1, w)); tg.addColorStop(1, K("#4f6094", 1, w));
        rr(c, -70, -55, 140, 110, 13); c.fillStyle = tg; c.fill(); c.lineWidth = 2.6; c.strokeStyle = inkC; c.stroke();
        if (rg > 0.02) { const q = c.createLinearGradient(0, 5, 0, 55); q.addColorStop(0, rgba("#ff5a36", 0)); q.addColorStop(1, rgba("#ff5a36", 0.42 * rg)); rr(c, -68, -53, 136, 106, 11); c.fillStyle = q; c.fill(); }
        rr(c, -62, -49, 124, 16, 5); c.fillStyle = N("#232c4a", 0.85); c.fill();
        const ledC = [C.ok, C.lamp, C.ok, "#7fe3ff", C.bad];
        for (let k = 0; k < 5; k++) led(-52 + k * 10, -41, 3, rg > 0.5 || (dmg >= 1 && k === 2) ? C.bad : ledC[k], e < 1 ? e > 0.82 + k * 0.03 : Math.sin(t * (3 + k * 1.7 + 9 * rg) + k * 2) > -0.2 || beat > 0.6);
        label("v12.4-rc3", 30, -40.5, 7.5, 0.8);
        c.strokeStyle = N(INK, 0.55); c.lineWidth = 1.8; for (let k = 0; k < 3; k++) { line(-60, 36 + k * 5.5, -38, 36 + k * 5.5); line(38, 36 + k * 5.5, 60, 36 + k * 5.5); }
        c.fillStyle = N("#aab6d6", 0.7); for (const [x, y] of [[-62, -27], [62, -27], [-62, 27], [62, 27]]) { c.beginPath(); c.arc(x, y, 1.8, 0, TAU); c.fill(); }
        c.strokeStyle = N(INK, 0.3); c.lineWidth = 1.4; line(-34, -30, -34, 28); line(34, -30, 34, 28);
        if (dmg >= 3) {                                                                                  // trappe ouverte : les fils pendent
          rr(c, 36, 2, 26, 26, 3); c.fillStyle = N(VISOR); c.fill(); c.lineWidth = 2.4; c.lineCap = "round";
          for (const [hue, dx, ph] of [["#ef6b5c", 0, 0], ["#f2c14e", 7, 2], ["#57c48f", 14, 4]]) { c.strokeStyle = N(hue); c.beginPath(); c.moveTo(42 + dx, 8); c.quadraticCurveTo(40 + dx + Math.sin(t * 3 + ph) * 4, 26, 46 + dx + Math.sin(t * 2.2 + ph) * 5, 40); c.stroke(); }
          c.save(); c.translate(62, 28); c.rotate(0.5 + Math.sin(t * 2.1) * 0.08); box(0, -3, 26, 24, 3, "#6f86b8"); c.restore();
        }
        if (dmg >= 1) tape(-42, 14, 46, 13, -0.55);
        if (dmg >= 2) { tape(-42, 14, 46, 13, 0.6); tape(48, -18, 30, 11, 0.3); }
        if (dmg >= 3) tape(-6, 46, 52, 12, -0.12);
        if (!dead) button(w);
        c.restore();
      }
      if (rg > 0.05 && !dead) { puffs(-70, 58, -34, -26, rg, "#e8ecf6"); puffs(70, 58, 34, -26, rg, "#e8ecf6"); }   // la surchauffe : vapeur aux évents
      if (dead && endK > 0.01) { c.save(); c.translate(0, tinyBob); c.translate(BX, BY); c.scale(endK, endK); c.translate(-BX, -BY); button(0); c.restore(); }

      // --- tête, visière, visage ---
      const nod = (Math.sin(t * 0.9) * 0.025 + lx * 0.03 + ly * -0.02) * live + (stun ? 0.1 : 0) - 0.06 * sq + 0.05 * back, hbob = Math.sin(t * 1.7) * 1.4 * live + 1.5 * beat;
      const onHead = () => { c.translate(0, -44 + hbob); c.rotate(nod); c.translate(0, 44); };          // la tête pivote sur son cou ; la pile suit
      const panic = dead ? 1 : 0;
      if (e > 0.3) { c.fillStyle = N("#232c4a"); for (let k = 0; k < 3; k++) { rr(c, -13 + k, -47 + k * 4, 26 - k * 2, 4, 2); c.fill(); } }                 // cou
      c.save(); onHead(); w = put(M.head);
      if (w >= 0) {
        box(-52, -30, 104, 60, 13, "#7c93c4", w);
        box(-59, -9, 8, 18, 3, "#4a5a8c", w); c.strokeStyle = inkC; c.lineWidth = 2; line(52, -8, 60, -12); const dw = 3 + 7 * Math.abs(Math.cos(t * 1.3 * live));
        c.fillStyle = K("#aab6d6", 1, w); c.beginPath(); c.ellipse(62, -13, dw, 9, 0.3, 0, TAU); c.fill(); c.stroke();
        rr(c, -47, -21, 86, 32, 10); c.fillStyle = N(VISOR); c.fill(); c.lineWidth = 2; c.strokeStyle = inkC; c.stroke();
        led(45, 16, 2.4, C.ok, lit && Math.sin(t * 6) > 0); led(45, 23, 2.4, rg > 0.5 ? C.bad : C.lamp, lit && Math.sin(t * 4.3) > 0);
        // les yeux : des diodes qui suivent la cible
        const ec = rgba(eyeHex, 1), flick = dmg >= 3 && !dead ? (Math.sin(t * 23) > -0.4 ? 1 : 0.25) : 1;
        if (e < 1 && boot < 0.55) {                                                                      // démarrage : barre de progression, puis les yeux s'allument
          const bk = seg(e, 0.72, 0.9); if (bk > 0) { c.fillStyle = rgba("#7fe3ff", 0.25); rr(c, -36, -8, 64, 6, 3); c.fill(); c.fillStyle = rgba("#7fe3ff", 0.95); rr(c, -36, -8, 64 * bk, 6, 3); c.fill(); }
        } else {
          c.save(); c.shadowColor = ec; c.shadowBlur = 9; c.fillStyle = ec; c.strokeStyle = ec; c.lineCap = "round"; c.lineWidth = 3.4;
          const blink = (t * 0.37 + 0.2) % 1 < 0.04 && !panic, bootFlick = e < 1 ? (Math.sin(e * 260) > 0 ? 1 : 0.2) : 1;
          for (const sd of [-1, 1]) {
            const x = -4 + sd * 18 + lx * 5, y = -5 + ly * 3;
            c.globalAlpha = GA * (sd > 0 ? flick : 1) * bootFlick;
            if (stun) { const r = 5.5; c.save(); c.translate(x, y); c.rotate(t * 3 * sd); line(-r, -r, r, r); line(-r, r, r, -r); c.restore(); }
            else if (sq > 0.25) { line(x - sd * 6, y - 6, x + sd * 4, y); line(x + sd * 4, y, x - sd * 6, y + 6); }                               // > <
            else if (gloat > 0.4) { c.beginPath(); c.arc(x, y + 5, 7.5, Math.PI * 1.15, Math.PI * 1.85); c.stroke(); }                        // ^ ^
            else if (panic) { c.lineWidth = 2.6; c.beginPath(); c.arc(x, y, 6.6, 0, TAU); c.stroke(); c.beginPath(); c.arc(x + Math.sin(t * 9) * 2, y + 1, 1.8, 0, TAU); c.fill(); c.lineWidth = 3.4; }
            else if (blink) c.fillRect(x - 8, y - 1, 16, 2.4);
            else { const big = 1 + 0.25 * threat + 0.15 * aw; rr(c, x - 8.5, y - 6.5 * big, 17, 13 * big, 4.5); c.fill(); }
          }
          c.restore();
          if (!stun && sq <= 0.25 && gloat <= 0.4 && !panic) {
            // paupières (de la couleur de la visière) : blasé au repos, fâché en rage, inquiet quand on le vise ; puis la pupille
            c.fillStyle = N(VISOR);
            for (const sd of [-1, 1]) {
              const x = -4 + sd * 18 + lx * 5, y = -5 + ly * 3, calm = (sd > 0 ? 0.18 : 0.36) * (1 - threat) * (1 - rg), hIn = (calm + 0.6 * rg + 0.3 * aw) * 13, hOut = (calm + 0.3 * threat) * 13;
              c.beginPath(); c.moveTo(x - 10, y - 9); c.lineTo(x + 10, y - 9); c.lineTo(x + 10, y - 7 + (sd > 0 ? hOut : hIn)); c.lineTo(x - 10, y - 7 + (sd > 0 ? hIn : hOut)); c.closePath(); c.fill();
            }
            c.fillStyle = "rgba(255,255,255,0.88)"; for (const sd of [-1, 1]) { rr(c, -4 + sd * 18 + lx * 8 - 3, -5 + ly * 4.6 - 1.5, 6, 6, 2); c.fill(); }
          }
        }
        c.fillStyle = "rgba(255,255,255,0.07)"; c.beginPath(); c.moveTo(-36, -21); c.lineTo(-14, -21); c.lineTo(-30, 11); c.lineTo(-47, 11); c.lineTo(-47, -10); c.closePath(); c.fill();   // reflet
        if (dmg >= 1) { c.strokeStyle = "rgba(230,240,255,0.7)"; c.lineWidth = 1.3; c.beginPath(); c.moveTo(39, -16); c.lineTo(28, -9); c.lineTo(31, -3); c.lineTo(22, 4); if (dmg >= 3) { c.moveTo(28, -9); c.lineTo(14, -13); c.lineTo(6, -21); c.moveTo(31, -3); c.lineTo(36, 8); } c.stroke(); }
        // la bouche : une rangée de diodes
        const mc = rgba(eyeHex, 0.9 * (e < 1 ? boot : 1));
        c.fillStyle = mc;
        for (let i = 0; i < 7; i++) {
          const x = -4 + (i - 3) * 6.2 - 2.2, u = i - 3; let y = 18, h = 3;
          if (panic) { h = Math.abs(u) <= 1 ? 8 : 0; y = 20; }
          else if (gloat > 0.3) { y = 22 - u * u * 0.85; h = 4.4; }
          else if (talk > 0.05) { h = 3 + talk * 8 * Math.abs(Math.sin(t * 19 + i * 1.3)); y = 19; }
          else if (sq > 0.25 || stun) { y = 19 + Math.sin(i * 1.7 + t * 12) * 2.2; }
          else if (aw > 0.2 && swing < 0.5) { h = 7; y = 19; }
          else if (rg > 0.5) { y = 19 + (i % 2 ? -2.4 : 2.4); h = 4.6; }
          else { y = 20 - (u < 0 ? -u * 1.1 : 0); }                                                    // petit sourire en coin, côté joueur
          if (h > 0) c.fillRect(x, y - h / 2, 4.4, h);
        }
        if (dmg >= 2) tape(30, -24, 36, 11, 0.5);
        if (threat > 0.3 && !dead) { c.fillStyle = rgba("#9fd8ff", 0.9 * threat); const dy = ((t * 1.4) % 1) * 14; c.beginPath(); c.moveTo(48, -22 + dy); c.quadraticCurveTo(53, -14 + dy, 48, -11 + dy); c.quadraticCurveTo(43, -14 + dy, 48, -22 + dy); c.fill(); }   // goutte de liquide de refroidissement
        c.restore();
      }
      c.restore();

      // --- la pile de modules en trop, sur la tête ---
      const wobble = (i) => { const amp = (1 + 3 * fl + (stun ? 2 : 0) + 1.5 * rg) * live; c.translate(Math.sin(t * 1.5 - i * 0.6) * (1 + i) * 1.1 * amp, beat * 1.2 * (i + 1)); c.rotate(Math.sin(t * 1.5 - i * 0.6 - 0.5) * 0.018 * (i + 1) * amp + 0.02 * i); };
      const stackMod = (i, wd, hh, hue, name, wh) => { box(-wd / 2, -hh / 2, wd, hh, 5, hue, wh); label(name, 2, 0.5, 8); led(-wd / 2 + 7, 0, 2.2, i === 1 ? C.lamp : C.ok, lit && Math.sin(t * (4 + i) + i) > 0); c.fillStyle = inkC; c.beginPath(); c.arc(wd / 2 - 6, 0, 1.6, 0, TAU); c.fill(); };
      c.save(); onHead();
      w = put(M.s1);
      if (w >= 0) { wobble(0); if (dmg >= 3) { c.translate(-4, 1); c.rotate(-0.13); } stackMod(0, 78, 22, "#8f86c9", "ORCH", w); if (dmg >= 3) tape(-24, 2, 26, 30, 0.1); c.restore(); }
      w = put(M.s2, dmg >= 3 ? since(3) : -1);
      if (w >= 0) { wobble(1); if (dmg >= 2) { c.translate(5, 1); c.rotate(0.15); } stackMod(1, 60, 20, "#5fa3a8", "ROUTER", w); if (dmg >= 2) tape(16, 4, 22, 30, -0.1); c.restore(); }
      if (dmg === 0 || e < 1) { w = put(M.s3); if (w >= 0) { wobble(2); stackMod(2, 46, 18, "#c2925a", "META", w); c.restore(); } }
      else {                                                                                             // le module du haut a glissé : il pend à son câble, puis tombe
        w = put(M.s3h, dmg >= 2 ? since(2) : -1);
        if (w >= 0) { const swg = Math.sin(t * 2.2) * 0.16 * live; c.translate(-30, -40); c.rotate(swg); c.translate(30, 40); c.strokeStyle = N("#f2c14e"); c.lineWidth = 2.6; c.lineCap = "round"; line(-30, -40, -6, -12); c.rotate(1.25); stackMod(2, 46, 18, "#c2925a", "META", w); c.restore(); }
      }
      // casque de chantier, posé sur le module du haut ; à sa mort il retombe sur le petit robot
      const topI = dmg === 0 ? 2 : dmg === 1 ? 1 : 0, hatK = backOut(seg(e, 0.78, 0.94));
      let hatX = [1, 4, 9][topI], hatY = [-126, -146, -164][topI], hatR = 0.02 * topI + (dmg >= 3 ? -0.13 : dmg === 2 ? 0 : 0) + Math.sin(t * 1.5 - topI * 0.6 - 0.5) * 0.02 * (topI + 1) * live;
      if (o.hatY != null && !dead && e >= 1) { hatX = o.hatX; hatY = o.hatY; }
      const hatFly = dead ? seg(d, 0.05, 0.76) : 0;
      c.restore();
      const hat = () => {
        c.fillStyle = N("#f2c14e"); c.strokeStyle = inkC; c.lineWidth = 2;
        c.beginPath(); c.moveTo(-15, 0); c.quadraticCurveTo(-15, -17, 0, -17); c.quadraticCurveTo(15, -17, 15, 0); c.closePath(); c.fill(); c.stroke();
        rr(c, -21, -2.5, 42, 5.5, 2.6); c.fill(); c.stroke(); c.fillStyle = N("#fff0b8", 0.8); c.fillRect(-2.5, -16, 5, 14);
      };
      if (hatK > 0.02 && (!dead || endK > 0.01)) {
        c.save();
        if (dead) {
          const u = easeInOut(hatFly), land = hatFly >= 1 ? Math.max(0, 1 - (d - 0.76) / 0.06) : 0;
          c.translate(lerp(hatX, BX, u), lerp(hatY, BY - 50 + tinyBob, u) - Math.sin(u * Math.PI) * 34 + (hatFly >= 1 ? 0 : 0)); c.rotate(hatR + u * TAU * 2); c.scale(endK * (1 + 0.25 * land), endK * (1 - 0.25 * land));
        } else { onHead(); c.translate(hatX + Math.sin(t * 1.5 - topI * 0.6) * (1 + topI) * 1.1 * live, hatY - (1 - hatK) * 40 + beat * 1.2 * (topI + 1)); c.rotate(hatR + (1 - hatK) * 0.6 - 0.12); c.scale(hatK, hatK); }
        hat(); c.restore();
      }
      // antennes
      const antK = backOut(seg(e, 0.7, 0.9)) * (1 - seg(d, 0.02, 0.1));
      if (antK > 0.02) {
        c.save(); onHead(); c.lineCap = "round";
        const sway = Math.sin(t * 2.1) * 3 * live + 5 * fl, bent = dmg >= 3;
        c.strokeStyle = N("#aab6d6"); c.lineWidth = 2.2; c.beginPath(); c.moveTo(-40, -104);
        if (bent) { c.lineTo(-48, -126); c.lineTo(-64 + sway, -122 * antK); } else c.lineTo(-40 - 16 * antK + sway, -104 - 46 * antK);
        c.stroke();
        const a1x = bent ? -64 + sway : -40 - 16 * antK + sway, a1y = bent ? -122 * antK : -104 - 46 * antK;
        led(a1x, a1y, 4, rg > 0.5 ? C.bad : C.ok, lit && (Math.sin(t * 6) > 0 || beat > 0.5));
        if (!dead) { const bx = hatX + 15, by = hatY - 2; c.strokeStyle = N("#aab6d6"); c.beginPath(); c.moveTo(bx, by); c.lineTo(bx + 10 * antK - sway * 0.6, by - 28 * antK); c.stroke(); led(bx + 10 * antK - sway * 0.6, by - 28 * antK, 3.6, C.lamp, lit && Math.sin(t * 4 + 1) > 0); }
        if (rg > 0.05) {                                                                                 // antennes télescopiques de plus, sorties en rage
          c.strokeStyle = N("#aab6d6"); c.lineWidth = 3; line(46, -104, 54, -104 - 20 * rgB); c.lineWidth = 1.8; line(54, -104 - 20 * rgB, 62 - sway, -104 - 46 * rgB); led(62 - sway, -104 - 46 * rgB, 3.6, C.bad, Math.sin(t * 14) > 0);
          c.lineWidth = 3; line(-22, -104, -24, -104 - 8 * rgB);
        }
        c.restore();
      }
      if (!dead && e >= 1) { c.save(); c.translate(0, -OY); drawCracks(c, b, "rgba(230,236,250,0.7)", 1.7); c.restore(); }

      // --- petits bras, devant : tournevis à droite, porte-bloc à gauche (il s'en fait un bouclier quand on le vise) ---
      w = put(M.t1, dmg >= 3 ? since(3) : -1);
      if (w >= 0) {
        const k = backOut(pk), a1 = 0.95 - busy * 0.1 - 1.6 * up, a2 = 2.3 + busy * 0.3 - 2.6 * up, ex = Math.cos(a1) * 15 * k, ey = Math.sin(a1) * 15 * k, hx = ex + Math.cos(a2) * 14 * k, hy = ey + Math.sin(a2) * 14 * k;
        limb(0, 0, ex, ey, 4.4, K("#8fa5d4")); limb(ex, ey, hx, hy, 4, K("#8fa5d4")); joint(ex, ey, 3); joint(0, 0, 3.4);
        c.save(); c.translate(hx, hy); c.rotate(a2); c.scale(k, k); box(-1, -3.4, 11, 6.8, 2.5, "#f39a3b"); c.strokeStyle = N("#dfe6f7"); c.lineWidth = 2.2; c.lineCap = "butt"; line(10, 0, 20, 0); c.restore();
        c.restore();
      }
      w = put(M.t3);
      if (w >= 0) {
        const k = backOut(pk), sh = easeOut(threat) * (dead ? 0 : 1), a1 = lerp(2.5, -0.2, sh) - 1.2 * up * (1 - sh), a2 = lerp(3.5, -0.75, sh) + busy * 0.06 - 0.6 * up * (1 - sh), ex = Math.cos(a1) * 17 * k, ey = Math.sin(a1) * 17 * k, hx = ex + Math.cos(a2) * 16 * k, hy = ey + Math.sin(a2) * 16 * k;
        limb(0, 0, ex, ey, 4.4, K("#8fa5d4")); limb(ex, ey, hx, hy, 4, K("#8fa5d4")); joint(ex, ey, 3); joint(0, 0, 3.4);
        c.save(); c.translate(hx, hy); c.rotate(lerp(-0.25, 0.1, sh) + busy * 0.03); c.scale(k, k);
        box(-13, -17, 26, 32, 3, "#b98d5a"); c.fillStyle = N("#f2ead7"); c.fillRect(-10, -12, 20, 24); c.fillStyle = N("#8a93ab"); c.fillRect(-5, -19, 10, 5);
        c.fillStyle = N(INK, 0.6); for (let i = 0; i < 4; i++) { c.fillRect(-7, -8 + i * 5, 3, 2); c.fillRect(-2, -8 + i * 5, 9 - (i % 2) * 3, 2); }
        c.restore(); c.restore();
      }

      // --- le grand bras lanceur (épaule gauche) : il arme la clé au-dessus de lui, puis la jette ---
      w = put(M.shL);
      if (w >= 0) {
        const k = backOut(seg(e, 0.62, 0.84)), limpArm = dead ? seg(d, 0.1, 0.3) : 0;
        if (k > 0.02) {
          const wave = gloat * Math.sin(t * 12) * 0.25;
          let a1 = lerp(lerp(lerp(2.3, 3.78, aw), 2.6, swing), 2.3, rc) + Math.sin(t * 1.3) * 0.04 * live + 1.1 * up + wave, a2 = lerp(lerp(lerp(4.08, 4.58, aw), 3.0, swing), 4.08, rc) + Math.sin(t * 1.7) * 0.05 * live + 0.5 * up + wave + 0.3 * castK * busy;
          a1 = lerp(a1, 1.7, limpArm); a2 = lerp(a2, 1.5, limpArm);
          const px = -16, py = 10, ex = px + Math.cos(a1) * 34 * k, ey = py + Math.sin(a1) * 34 * k, hx = ex + Math.cos(a2) * 36 * k, hy = ey + Math.sin(a2) * 36 * k;
          limb(px, py, ex, ey, 8, K("#7f8fb0")); limb(ex, ey, hx, hy, 6.4, K("#8fa5d4")); joint(px, py, 5.5); joint(ex, ey, 4.6);
          const wk = !ap.on ? 1 : ap.strike > 0 ? backOut(seg(ap.rec, 0.55, 0.95)) : 1;                  // la clé part avec le projectile, une autre sort du bras
          c.save(); c.translate(hx, hy); c.rotate(a2 + lerp(0.45, 0.6, aw * (1 - swing)));
          if (wk > 0.02 && !dead) {
            c.save(); c.scale(k * wk, k * wk);
            const body = (grow, color) => { c.strokeStyle = color; c.fillStyle = color; c.lineCap = "butt"; rr(c, -4 - grow, -4 - grow, 36 + grow * 2, 8 + grow * 2, 2); c.fill(); c.lineWidth = 6 + grow * 2; c.beginPath(); c.arc(39, 0, 8.4, 0.72, TAU - 0.72); c.stroke(); };
            body(1.6, inkC); body(0, N("#dfe6f7")); c.fillStyle = K("#f39a3b"); c.fillRect(6, -4, 11, 8); c.fillStyle = "rgba(255,255,255,0.5)"; c.fillRect(-2, -2.8, 32, 1.5);
            c.restore();
          }
          c.fillStyle = K("#4a5a8c"); c.strokeStyle = inkC; c.lineWidth = 1.8; rr(c, -6, -7.5, 12, 15, 4); c.fill(); c.stroke();    // pince
          c.restore();
        }
        c.restore();
      }

      // --- drapeau blanc du petit robot (devant) ---
      if (tiny > 0 && endK > 0.01) {
        const fk = backOut(seg(d, 0.64, 0.78));
        if (fk > 0.02) {
          c.save(); c.translate(BX, BY + tinyBob); c.scale(endK, endK);
          const fa = -1.25 + Math.sin(t * 9) * 0.22, hx = 24 + Math.cos(fa) * 16 * fk, hy = 0 + Math.sin(fa) * 16 * fk;
          limb(24, 0, hx, hy, 3.4, N("#8fa5d4"));
          c.save(); c.translate(hx, hy); c.rotate(fa + 1.25 - 0.1); c.scale(fk, fk);
          c.strokeStyle = N("#aab6d6"); c.lineWidth = 2.4; c.lineCap = "round"; line(0, 6, 0, -44);
          c.fillStyle = "#f8fbff"; c.strokeStyle = inkC; c.lineWidth = 1.4; c.beginPath(); c.moveTo(0, -43);
          for (let i = 1; i <= 6; i++) c.lineTo(i * 5.4, -43 + Math.sin(t * 11 - i * 0.9) * 2.4 * (i / 6));
          for (let i = 6; i >= 0; i--) c.lineTo(i * 5.4, -22 + Math.sin(t * 11 - i * 0.9 + 0.5) * 2.4 * (i / 6));
          c.closePath(); c.fill(); c.stroke();
          c.restore(); c.restore();
        }
      }

      // --- effets ---
      if (dmg >= 2 && !dead && e >= 1) { puffs(50, -128, 16, -34, 0.9, "#59607a"); spark(-66, -24, 8, 5.2); }
      if (dmg >= 3 && !dead && e >= 1) { spark(62, 26, 10, 0.4); spark(-24, -100, 7, 3.3); }
      if (fl > 0.3 && !dead) { spark(-30, -6, 14, 1); spark(34, 40, 12, 2.4); }
      if (castK > 0.02) {                                                                                // action spéciale : il projette le plan d'un agent de plus
        const k = clamp(b.cast / 0.9, 0, 1), px = -128, py = -128;
        c.fillStyle = rgba("#7fe3ff", 0.12 * castK); c.beginPath(); c.moveTo(-56, -76); c.lineTo(px - 34, py + 18); c.lineTo(px + 34, py + 18); c.closePath(); c.fill();
        c.save(); c.translate(px, py); c.scale(0.6 + 0.4 * backOut(seg(k, 0, 0.3)), 0.6 + 0.4 * backOut(seg(k, 0, 0.3)));
        rr(c, -36, -22, 72, 40, 5); c.fillStyle = rgba("#0c1a36", 0.82 * castK); c.fill(); c.strokeStyle = rgba("#7fe3ff", castK); c.lineWidth = 1.6; c.stroke();
        c.strokeStyle = rgba("#7fe3ff", 0.9 * castK); c.lineWidth = 1.4; c.strokeRect(-28, -6, 12, 16); c.strokeRect(-24, -13, 4, 7); line(-10, 2, -2, 2); c.strokeRect(-2, -3, 10, 10); line(8, 2, 14, 2); c.strokeRect(14, -3, 10, 10);
        c.fillStyle = rgba("#f39a3b", castK); c.fillRect(-28, 13, 56 * k, 3);
        c.font = "700 8px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle"; c.fillStyle = rgba("#e6ecff", castK); c.fillText("+1 AGENT", 0, -15);
        c.restore();
        spark(-150, 4, 9, 6.1);
      }
      if (stun) { for (let i = 0; i < 3; i++) { const a = t * 3.6 + i * 2.09, x = Math.cos(a) * 44, y = -136 + Math.sin(a) * 9; c.fillStyle = rgba(C.lamp, 0.6 + 0.4 * Math.sin(a)); c.beginPath(); for (let j = 0; j < 8; j++) { const q = (j / 8) * TAU, r = j % 2 ? 2.4 : 6; c.lineTo(x + Math.cos(q) * r, y + Math.sin(q) * r); } c.fill(); } }
      c.restore();
    }
  };
}
