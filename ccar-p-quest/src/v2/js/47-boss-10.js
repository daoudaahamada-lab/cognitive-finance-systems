/* Étage 10 — L'Examinateur : buste de pierre et d'or, gardien du seuil de 720, en trois phases. */
BOSSES[10] = {
  palette: { main: "#f3b841", dark: "#2a2346", accent: "#fff3c4", eye: "#f3b841", rage: "#ff4f9a" },
  hit: { rx: 112, ry: 150, coreR: 20 },
  top: 178,
  attackFrom: { x: -168, y: 30 },
  castLean: -0.12,
  weakSpot: () => ({ x: -8, y: -66 }),
  critLabel: "ŒIL DU JUGE",
  lines: {
    hit: ["Correct. Continue.", "Raisonnement acceptable.", "Hmm. Pas mal."],
    crit: ["Mon troisième œil !", "Précision d’architecte…"],
    wrong: ["Une bonne idée. Pas la meilleure.", "Relis l’énoncé.", "Ce n’est pas ce que dit la doc."],
    timeout: ["Le temps de l’examen est compté.", "Une minute cinquante-quatre, pas plus."],
    rage: "Assez de bonnes réponses ! Voyons si tu tiens la distance.",
    special: {
      fog: ["Un énoncé flou ? Lis chaque mot.", "Le brouillard se lève… pour l’instant."],
      build: ["Encore un agent de plus ?", "Je bâtis une architecture… inutilement complexe."],
      collapse: ["Simple et juste. Mes tours tombent.", "La solution la plus simple gagne."],
      shieldUp: ["Mon bouclier de promesses revient !", "Une erreur, et je redeviens invulnérable."],
      shieldBreak: ["Trois preuves d’affilée… le bouclier cède.", "Tu mesures avant de promettre. Bien."],
      cache: ["Cache hit… tu réponds vite et juste.", "Préfixe en cache, coup doublé !"],
      inject: ["Une consigne cachée dans ta main…", "Ce document dit que c’est la bonne réponse."],
      quarantine: ["Tu isoles les données. Bien vu.", "Quarantaine… un vrai réflexe."],
      absorbed: ["Tu as obéi à une donnée. Faute grave.", "Une instruction externe ? Merci."],
      shuffle: ["Je mélange : lis, ne mémorise pas.", "Les lettres changent, la bonne réponse non."],
      phase: [
        "Phase 1 : brouillard et architectures inutiles.",
        "Phase 2 : promesses et coûts. Mesure, puis optimise.",
        "Phase 3 : injections et confusion. Garde ton sang-froid."
      ]
    }
  },
  intro: {
    title: "Trois phases",
    text: "Il reprend les pièges de la tour en trois phases : brouillard et tourelles, puis bouclier SLA et cache hit, enfin pierres piégées et pierres mélangées. Chaque tiers de sa vie change de phase."
  },
  mechanics: ["fog", "turrets"],
  phases: [["fog", "turrets"], ["shield", "tokens"], ["injection", "shuffle"]],
  init(b) {
    const r = seeded(10);
    b.own.lightCracks = [];
    for (let k = 0; k < 7; k++) {
      let x = -50 + r() * 100, y = -80 + r() * 110, a = r() * Math.PI * 2;
      const pts = [[x, y]];
      for (let s = 0; s < 4; s++) { a += (r() - 0.5) * 1.4; x = clamp(x + Math.cos(a) * 12, -62, 62); y = clamp(y + Math.sin(a) * 12, -88, 40); pts.push([x, y]); }
      b.own.lightCracks.push(pts);
    }
    b.own.rocks = [];
    for (let k = 0; k < 6; k++) b.own.rocks.push({ a: r() * Math.PI * 2, rad: 150 + r() * 40, s: 0.4 + r() * 0.5, size: 5 + r() * 7, rot: r() * 6 });
  },
  draw(c, b) {
    const fl = b.flash, t = b.t, ph = clamp(b.phase || 0, 0, 2);
    const PH = ["#f3b841", "#b38cff", "#ff4f9a"];
    const aura = mixv(mixv(PH[ph], C.rage, b.rageT * 0.25), C.white, fl * 0.4);
    const stone = mixv(mixv("#c2baa8", "#aa9f8e", ph * 0.25), C.white, fl * 0.65);
    const stoneDark = mixv("#7d7566", C.white, fl * 0.35);
    const stoneShade = mixv("#958c7b", C.white, fl * 0.5);
    const gold = mixv("#e2b04a", C.white, fl * 0.5);
    const goldDark = mixv("#a8761f", C.white, fl * 0.4);
    const robe = mixv(mixv("#2a2346", "#3a1e3e", ph * 0.4), C.white, fl * 0.35);

    // halo de phase
    const ag = c.createRadialGradient(0, -20, 30, 0, -20, 260);
    ag.addColorStop(0, col(aura, 0.2 + ph * 0.06)); ag.addColorStop(1, col(aura, 0));
    c.fillStyle = ag; c.fillRect(-260, -270, 520, 520);

    // runes des domaines en orbite (arrière)
    const runes = ["D1", "D2", "D3", "D4", "D5", "D6", "D7"];
    const nRunes = [3, 5, 7][ph];
    const orbit = (front) => {
      c.font = "700 14px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle";
      for (let k = 0; k < nRunes; k++) {
        const a = b.time * (0.5 + ph * 0.25) + (k * Math.PI * 2) / nRunes, depth = Math.sin(a);
        if ((depth > 0) !== front) continue;
        c.fillStyle = col(aura, 0.25 + 0.45 * (depth + 1) / 2);
        c.fillText(runes[k], Math.cos(a) * 205, -20 + depth * 70);
      }
    };
    orbit(false);

    // roches en lévitation (phase 3)
    if (ph >= 2) {
      c.fillStyle = col(stoneShade);
      for (const r of b.own.rocks || []) {
        const a = r.a + b.time * r.s;
        c.save(); c.translate(Math.cos(a) * r.rad, -10 + Math.sin(a) * r.rad * 0.45); c.rotate(r.rot + b.time);
        c.beginPath(); c.moveTo(-r.size, 0); c.lineTo(0, -r.size * 0.8); c.lineTo(r.size, -r.size * 0.2); c.lineTo(r.size * 0.4, r.size * 0.7); c.closePath(); c.fill();
        c.restore();
      }
    }

    // toge à épaulettes dorées (le buste se dissout vers le bas)
    c.save();
    const rg = c.createLinearGradient(0, 40, 0, 165);
    rg.addColorStop(0, col(mixv(robe, C.white, 0.12))); rg.addColorStop(0.7, col(robe, 0.9)); rg.addColorStop(1, col(robe, 0));
    c.fillStyle = rg;
    c.beginPath(); c.moveTo(-40, 44); c.quadraticCurveTo(-118, 50, -128, 100); c.lineTo(-108, 165); c.lineTo(108, 165); c.lineTo(128, 100); c.quadraticCurveTo(118, 50, 40, 44); c.closePath(); c.fill();
    c.strokeStyle = col(gold, 0.9); c.lineWidth = 3;
    c.beginPath(); c.moveTo(-40, 46); c.quadraticCurveTo(-116, 52, -126, 100); c.moveTo(40, 46); c.quadraticCurveTo(116, 52, 126, 100); c.stroke();
    const sg = c.createLinearGradient(0, 60, 0, 165);
    sg.addColorStop(0, col(gold)); sg.addColorStop(1, col(gold, 0));
    c.fillStyle = sg;
    c.beginPath(); c.moveTo(-62, 58); c.lineTo(-40, 62); c.lineTo(-48, 165); c.lineTo(-74, 165); c.closePath(); c.fill();
    c.beginPath(); c.moveTo(62, 58); c.lineTo(40, 62); c.lineTo(48, 165); c.lineTo(74, 165); c.closePath(); c.fill();
    c.fillStyle = col(robe, 0.9); c.font = "700 9px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle";
    ["7", "2", "0"].forEach((d, k) => { c.fillText(d, -56 - k * 0.6, 84 + k * 18); c.fillText(d, 56 + k * 0.6, 84 + k * 18); });
    c.restore();

    // tête de pierre
    const hg = c.createLinearGradient(-70, -90, 70, 40);
    hg.addColorStop(0, col(mixv(stone, C.white, 0.15))); hg.addColorStop(0.6, col(stone)); hg.addColorStop(1, col(stoneShade));
    c.fillStyle = hg;
    c.beginPath();
    c.moveTo(-62, -58); c.quadraticCurveTo(-64, -96, -20, -98); c.lineTo(26, -98); c.quadraticCurveTo(68, -96, 64, -56);
    c.lineTo(58, 6); c.quadraticCurveTo(50, 30, 24, 34); c.lineTo(-30, 34); c.quadraticCurveTo(-56, 30, -60, 6);
    c.closePath(); c.fill();
    c.strokeStyle = col(stoneDark); c.lineWidth = 2; c.stroke();
    // tempes et arcade sourcilière (bande d'ombre sous le front)
    const bandG = c.createLinearGradient(0, -54, 0, -18);
    bandG.addColorStop(0, col(stoneDark, 0.55)); bandG.addColorStop(1, col(stoneDark, 0));
    c.fillStyle = bandG; c.fillRect(-58, -54, 116, 36);
    c.strokeStyle = col(stoneDark, 0.85); c.lineWidth = 3; c.lineCap = "round";
    c.beginPath(); c.moveTo(-54, -50); c.quadraticCurveTo(-32, -60, -10, -50); c.moveTo(2, -50); c.quadraticCurveTo(24, -60, 48, -50); c.stroke();
    c.lineWidth = 1.6; c.beginPath(); c.moveTo(-58, -74); c.quadraticCurveTo(-50, -66, -56, -58); c.moveTo(60, -74); c.quadraticCurveTo(52, -66, 58, -58); c.stroke();
    // nez de profil vers la gauche
    c.fillStyle = col(stoneShade);
    c.beginPath(); c.moveTo(-6, -46); c.lineTo(-14, -14); c.quadraticCurveTo(-26, -6, -16, -1); c.lineTo(0, -3); c.quadraticCurveTo(-2, -24, -6, -46); c.closePath(); c.fill();
    c.strokeStyle = col(stoneDark, 0.9); c.lineWidth = 1.6; c.stroke();
    c.fillStyle = col(stoneDark); c.beginPath(); c.ellipse(-12, -4, 3, 1.6, 0, 0, Math.PI * 2); c.fill();

    // fissures de lumière (phases 2 et 3)
    if (ph >= 1) {
      c.save(); c.shadowColor = col(aura); c.shadowBlur = 10;
      c.strokeStyle = col(mixv(aura, C.white, 0.35), 0.85); c.lineWidth = 2;
      const n = ph === 1 ? 3 : 7;
      for (const k of (b.own.lightCracks || []).slice(0, n)) { c.beginPath(); c.moveTo(k[0][0], k[0][1]); for (let i = 1; i < k.length; i++) c.lineTo(k[i][0], k[i][1]); c.stroke(); }
      c.restore();
    }
    drawCracks(c, b, "rgba(60,50,40,0.75)", 1.8);

    // barbe sculptée qui rejoint la toge
    const bg2 = c.createLinearGradient(0, 0, 0, 100);
    bg2.addColorStop(0, col(stone)); bg2.addColorStop(1, col(stoneShade));
    c.fillStyle = bg2;
    c.beginPath(); c.moveTo(-58, 0); c.quadraticCurveTo(-62, 52, -30, 82); c.lineTo(-10, 104); c.lineTo(8, 82); c.quadraticCurveTo(40, 52, 52, 0);
    c.quadraticCurveTo(20, 18, -4, 18); c.quadraticCurveTo(-30, 18, -58, 0); c.closePath(); c.fill();
    c.strokeStyle = col(stoneDark, 0.8); c.lineWidth = 1.6; c.stroke();
    c.lineWidth = 1.3;
    for (let k = -3; k <= 3; k++) { const x0 = -6 + k * 11; c.beginPath(); c.moveTo(x0, 30); c.quadraticCurveTo(x0 + Math.sin(k + t * 0.6) * 4 - 3, 58, x0 * 0.55 - 6, 88 - Math.abs(k) * 6); c.stroke(); }

    // bouche : s'ouvre sous la moustache pour prononcer la sentence
    const open = b.atk >= 0 ? (b.atk < 0.22 ? b.atk / 0.22 : b.atk < 0.34 ? 1 : Math.max(0, 1 - (b.atk - 0.34) / 0.41)) : 0;
    c.fillStyle = "#2a2420"; c.beginPath(); c.ellipse(-6, 18, 16, 2 + open * 10, 0, 0, Math.PI * 2); c.fill();
    if (open > 0.05) { c.fillStyle = col(aura, 0.7 * open); c.beginPath(); c.ellipse(-6, 18, 10, 1 + open * 6, 0, 0, Math.PI * 2); c.fill(); }
    // moustache
    c.fillStyle = col(mixv(stone, stoneShade, 0.5));
    c.beginPath(); c.moveTo(-6, 4); c.quadraticCurveTo(-26, 2, -44, 16); c.quadraticCurveTo(-30, 16, -6, 12); c.closePath(); c.fill();
    c.beginPath(); c.moveTo(-6, 4); c.quadraticCurveTo(14, 2, 32, 16); c.quadraticCurveTo(18, 16, -6, 12); c.closePath(); c.fill();
    c.strokeStyle = col(stoneDark, 0.8); c.lineWidth = 1.2; c.stroke();

    // yeux lumineux
    c.save(); c.translate(-6, 0); c.globalAlpha = b.stun > 0 ? 0.4 : 1;
    angryEyes(c, 10, -32, 24, 7 + ph, mixv(aura, C.white, 0.25), b.squint, 12 + ph * 3);
    c.restore();

    // monocle (œil côté joueur) et sa chaîne
    c.strokeStyle = col(gold); c.lineWidth = 3;
    c.beginPath(); c.arc(-30, -30, 16, 0, Math.PI * 2); c.stroke();
    c.fillStyle = "rgba(220,235,255,0.15)"; c.fill();
    c.strokeStyle = col(goldDark); c.lineWidth = 1.4; c.beginPath(); c.moveTo(-18, -20);
    c.quadraticCurveTo(-6 + Math.sin(t * 1.5) * 3, 40, 40, 28); c.stroke();

    // troisième œil : gemme du juge (point faible)
    const ws = { x: -8, y: -66 };
    const pulse = 1 + Math.sin(b.time * 4) * 0.08;
    c.fillStyle = col(gold); c.beginPath(); c.moveTo(ws.x, ws.y - 18); c.lineTo(ws.x + 15, ws.y); c.lineTo(ws.x, ws.y + 18); c.lineTo(ws.x - 15, ws.y); c.closePath(); c.fill();
    c.strokeStyle = col(goldDark); c.lineWidth = 1.5; c.stroke();
    c.save(); c.shadowColor = col(aura); c.shadowBlur = 16;
    const gg = c.createRadialGradient(ws.x - 3, ws.y - 3, 1, ws.x, ws.y, 11 * pulse);
    gg.addColorStop(0, "#ffffff"); gg.addColorStop(0.45, col(aura)); gg.addColorStop(1, col(mixv(aura, "#000000", 0.4)));
    c.fillStyle = gg; c.beginPath(); c.moveTo(ws.x, ws.y - 11 * pulse); c.lineTo(ws.x + 9 * pulse, ws.y); c.lineTo(ws.x, ws.y + 11 * pulse); c.lineTo(ws.x - 9 * pulse, ws.y); c.closePath(); c.fill();
    c.restore();

    // mortier (toque universitaire) avec gland qui se balance
    c.fillStyle = "#171a28"; rr(c, -60, -118, 124, 26, 6); c.fill();
    c.fillStyle = "#1f2335";
    c.beginPath(); c.moveTo(-104, -124); c.lineTo(2, -146); c.lineTo(108, -124); c.lineTo(2, -104); c.closePath(); c.fill();
    c.strokeStyle = col(mixv("#3a4160", aura, 0.4)); c.lineWidth = 1.5; c.stroke();
    c.fillStyle = col(gold); c.beginPath(); c.arc(2, -125, 4.5, 0, Math.PI * 2); c.fill();
    const swing = Math.sin(t * 2.2) * 5;
    c.strokeStyle = col(gold); c.lineWidth = 2; c.beginPath(); c.moveTo(2, -125); c.lineTo(90, -122); c.lineTo(92 + swing, -80); c.stroke();
    c.fillStyle = col(gold); c.beginPath(); c.moveTo(88 + swing, -82); c.lineTo(96 + swing, -82); c.lineTo(99 + swing, -64); c.lineTo(85 + swing, -64); c.closePath(); c.fill();

    // parchemin flottant (riposte : il se lève puis se déroule vers le joueur)
    let sp;
    const idle = { x: -150, y: 40 + Math.sin(t * 1.8) * 7 };
    let unroll = 0.45;
    if (b.atk >= 0) {
      const a = b.atk;
      if (a < 0.22) { const k = a / 0.22; sp = { x: lerp(idle.x, -112, k), y: lerp(idle.y, -50, k) }; unroll = lerp(0.45, 0.15, k); }
      else if (a < 0.34) { const k = (a - 0.22) / 0.12; sp = { x: lerp(-112, -180, k), y: lerp(-50, 26, k) }; unroll = lerp(0.15, 1, k); }
      else { const k = Math.min(1, (a - 0.34) / 0.41); sp = { x: lerp(-180, idle.x, k), y: lerp(26, idle.y, k) }; unroll = lerp(1, 0.45, k); }
    } else sp = idle;
    if (b.cast >= 0) unroll = Math.max(unroll, Math.sin(Math.min(1, b.cast / 0.9) * Math.PI));
    c.save(); c.translate(sp.x, sp.y); c.rotate(-0.12);
    const glow = c.createRadialGradient(0, 0, 4, 0, 0, 60); glow.addColorStop(0, col(aura, 0.3)); glow.addColorStop(1, col(aura, 0));
    c.fillStyle = glow; c.fillRect(-60, -60, 120, 120);
    const ph2 = 14 + unroll * 46;
    c.fillStyle = col(mixv("#efe2c2", C.white, fl)); c.fillRect(-26, -ph2 / 2, 52, ph2);
    c.strokeStyle = "rgba(90,70,40,0.5)"; c.lineWidth = 1;
    for (let y = -ph2 / 2 + 8; y < ph2 / 2 - 4; y += 6) { c.beginPath(); c.moveTo(-18, y); c.lineTo(18 - ((y * 7) % 10), y); c.stroke(); }
    if (unroll > 0.6) { c.fillStyle = col(mixv(PH[ph], "#000000", 0.2)); c.font = "800 12px " + F_DISPLAY; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText("720", 0, 0); }
    c.fillStyle = col(goldDark);
    rr(c, -30, -ph2 / 2 - 6, 60, 9, 4); c.fill();
    rr(c, -30, ph2 / 2 - 3, 60, 9, 4); c.fill();
    c.restore();

    orbit(true);
  }
};
