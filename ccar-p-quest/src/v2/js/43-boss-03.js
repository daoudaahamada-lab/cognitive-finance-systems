/* Étage 3 — Le Schéma Brisé : un objet JSON vivant. Un panneau sombre de lignes « "clé": valeur » avec un visage,
   une accolade ouvrante « { » en griffe lumineuse à gauche. L'accolade fermante « } » lui manque : elle tourne autour
   de lui et c'est sa cible critique.
   Mécanique « parse » : il alterne VALIDE (écran net, lignes cyan/vertes) et CORROMPU (écran rouge, lignes brouillées en
   tranches décalées, étiquette SyntaxError, accolade en orbite éteinte et cassée). À k > 0,8 l'écran clignote vers l'état suivant.
   Dégâts à l'envers : plus il est blessé, plus ses lignes sont réparées (✓ vert) et plus sa griffe s'abîme. */
{
  // Lignes du panneau : clé, valeur cassée, valeur réparée.
  const ROWS = [
    ['"order_id": ', '"4812"', "4812,"],
    ['"amount": ', '"12,5O",', "12.50,"],
    ['"status": ', ",,", '"paid",'],
    ['"items": ', '[{"sku": 3', '[{"sku": 3}],'],
    ['"date": ', '"2026-13-45"', '"2026-11-08"']
  ];
  const JUNK = "#%&?!<>/\\|;:*^~$";
  const RED = "#ff4d5e", GREEN = "#6df0a8", GOLD = "#ffd66b";
  const PX = -80, PY = -80, PW = 184, PH = 160, SPLIT = -2, PCX = PX + PW / 2;   // panneau ; SPLIT sépare visage et lignes
  const ORB = { cx: -4, rx: 164, ry: 98 };                                       // orbite de l'accolade fermante
  const SLOT = 128;                                                              // x où l'accolade fermante devrait être
  const hash = (n) => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };

  /** Trace une accolade (à peindre ensuite). dir = -1 : « { », pointe vers la gauche ; +1 : « } ».
      part : 0 entière, -1 moitié haute, 1 moitié basse. cut : le crochet du bas est cassé. */
  function brace(c, x, y, h, w, tip, dir, part, cut) {
    const r = Math.min(w, h * 0.32), k = r * 0.85;
    c.beginPath();
    if (part <= 0) { c.moveTo(x - dir * w, y - h); c.quadraticCurveTo(x, y - h, x, y - h + r); c.lineTo(x, y - k); c.quadraticCurveTo(x, y, x + dir * tip, y); }
    if (part >= 0) {
      c.moveTo(x + dir * tip, y); c.quadraticCurveTo(x, y, x, y + k);
      if (cut) c.lineTo(x, y + h * 0.56); else { c.lineTo(x, y + h - r); c.quadraticCurveTo(x, y + h, x - dir * w, y + h); }
    }
  }
  /** Brouille une ligne : une partie des caractères devient du bruit, renouvelé à chaque pas. */
  function scramble(s, row, step, p) {
    let out = "";
    for (let j = 0; j < s.length; j++) { const h = hash(row * 31.7 + j * 7.3 + step * 3.1); out += h < p ? JUNK[Math.floor((h / p) * JUNK.length) % JUNK.length] : s[j]; }
    return out;
  }
  function tick(c, x, y, s) { c.beginPath(); c.moveTo(x - 4 * s, y); c.lineTo(x - 1 * s, y + 3.5 * s); c.lineTo(x + 5 * s, y - 4 * s); c.stroke(); }
  function cross(c, x, y, s) { c.beginPath(); c.moveTo(x - 3.5 * s, y - 3.5 * s); c.lineTo(x + 3.5 * s, y + 3.5 * s); c.moveTo(x + 3.5 * s, y - 3.5 * s); c.lineTo(x - 3.5 * s, y + 3.5 * s); c.stroke(); }
  /** Trace une roue dentée (à peindre ensuite). */
  function gear(c, x, y, r, n, rot) {
    c.beginPath();
    for (let i = 0; i < n; i++) {
      const a = rot + (i / n) * Math.PI * 2, st = (Math.PI * 2) / n, ri = r * 0.82;
      c.lineTo(x + Math.cos(a) * ri, y + Math.sin(a) * ri);
      c.lineTo(x + Math.cos(a + st * 0.14) * r, y + Math.sin(a + st * 0.14) * r);
      c.lineTo(x + Math.cos(a + st * 0.42) * r, y + Math.sin(a + st * 0.42) * r);
      c.lineTo(x + Math.cos(a + st * 0.56) * ri, y + Math.sin(a + st * 0.56) * ri);
    }
    c.closePath();
  }

  BOSSES[3] = {
    v: 2,
    palette: { main: "#5fd8e6", dark: "#12283a", accent: "#ffd66b", eye: "#5fd8e6", rage: "#ff4fb4" },
    hit: { rx: 142, ry: 100, coreR: 22 },
    top: 114,
    attackFrom: { x: -186, y: 0 },
    castLean: -0.08,
    critLabel: "} FERMÉ",
    epitaph: "VALIDÉ",
    mechanics: ["parse"],
    lines: {
      hit: ["Une virgule de moins !", "Mon champ obligatoire !", "Tu valides mes types ?!"],
      crit: ["Tu as fermé mon accolade !", "Parsé ! Je suis parsé !"],
      wrong: ["« Respond only in JSON », hein ?", "Encore un parseur à base de regex.", "SyntaxError: unexpected token."],
      timeout: ["Timeout. Réessaie… sans schéma.", "Ta requête a expiré."],
      gloat: ["null, NaN, undefined : fais ton choix.", "Ton ERP ne s’en remettra pas.", "Unexpected token : toi."],
      rage: "Je corromps tous tes champs à la fois !",
      special: {
        corrupt: ["Unexpected end of JSON input.", "Champ manquant ? Quel champ ?", "Corrompu ! Tire donc, pour voir."],
        valid: ["Touché en plein JSON valide…", "Tu as attendu mon 200 OK ?!", "Parsé du premier coup. Zut."]
      }
    },
    intro: {
      title: "Valide ou corrompu",
      text: "Il alterne entre VALIDE (écran cyan) et CORROMPU (écran rouge, « SyntaxError ») : touché quand il est corrompu, tes dégâts tombent à ×0,6 et aucun coup critique n’est possible. Attends qu’il redevienne valide, puis vise l’accolade « } » qui tourne autour de lui pour le critique « } FERMÉ »."
    },

    /* L'accolade en orbite : l'angle est intégré (b.own.orb) pour accélérer sans à-coup quand il enrage. */
    init(b) { if (b.own) b.own.orb = 0.6; },
    update(b, dt) { if (b.own) b.own.orb = (b.own.orb == null ? 0.6 : b.own.orb) + dt * lerp(0.75, 1.35, b.rageT || 0); },
    orbit(b, lag) { const a = (b.own && b.own.orb != null ? b.own.orb : 0.6 + (b.t || 0) * 0.75) - (lag || 0); return { x: ORB.cx + Math.cos(a) * ORB.rx, y: Math.sin(a) * ORB.ry }; },
    weakSpot(b) { return BOSSES[3].orbit(b, 0); },

    /* Déplacement : micro-sauts de glitch. Il reste figé, puis saute d'un coup à une autre position. */
    jump(t, rage) {
      const per = rage ? 0.62 : 1.05, n = Math.floor(t / per), amp = rage ? 1.45 : 1;
      const at = (k) => ({ x: (hash(k * 3.1) - 0.6) * 44 * amp, y: (hash(k * 7.7 + 2) - 0.5) * 46 * amp });
      return { cur: at(n), prev: at(n - 1), age: t - n * per };
    },
    motion(b) {
      const t = b.t || 0, j = BOSSES[3].jump(t, b.rage), k = clamp(j.age / 0.07, 0, 1);
      const jit = j.age < 0.16 ? (hash(Math.floor(t * 60)) - 0.5) * 7 * (1 - j.age / 0.16) : 0;
      return { x: lerp(j.prev.x, j.cur.x, k) + jit + Math.sin(t * 0.7) * 4, y: lerp(j.prev.y, j.cur.y, k) + Math.sin(t * 1.9) * 5 };
    },

    /* Projectile : un éclat de code dentelé qui porte un jeton invalide. */
    shot: {
      color: "#ff5c7a", n: 0, last: 9,
      draw(c, s) {
        const S = BOSSES[3].shot;
        if (s.t < S.last - 0.05) S.n++;
        S.last = s.t;
        const tok = ["null", "NaN", "undefined", "]"][S.n % 4], hot = s.rage ? "#ff4fb4" : "#ff5c7a", f = Math.floor(s.t * 30);
        c.save(); c.scale(1.2, 1.2);
        for (let k = 0; k < 3; k++) { c.fillStyle = col(k % 2 ? "#49e6ff" : hot, 0.5 - k * 0.12); c.fillRect(-30 - k * 9 - hash(f + k) * 8, -9 + ((f + k * 2) % 4) * 5, 9 - k * 2, 2.5); }
        c.save(); c.shadowColor = hot; c.shadowBlur = 10;
        c.beginPath(); c.moveTo(26, 0); c.lineTo(10, -8); c.lineTo(5, -14); c.lineTo(-7, -9); c.lineTo(-20, -13); c.lineTo(-15, -3); c.lineTo(-24, 2); c.lineTo(-13, 8); c.lineTo(-17, 14); c.lineTo(0, 10); c.lineTo(9, 12); c.closePath();
        c.fillStyle = "#2a0812"; c.fill(); c.restore();
        c.strokeStyle = hot; c.lineWidth = 2; c.lineJoin = "round"; c.stroke();
        c.strokeStyle = "rgba(255,255,255,0.55)"; c.lineWidth = 1; c.beginPath(); c.moveTo(24, 0); c.lineTo(10, -7); c.lineTo(6, -12); c.stroke();
        if (c.getTransform && c.getTransform().a < 0) c.rotate(Math.PI);    // le jeton reste lisible quand l'éclat vole vers la gauche
        c.fillStyle = "#ffe3e8"; c.font = "700 " + (tok.length > 4 ? 6.5 : tok.length > 1 ? 10 : 15) + "px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle";
        c.fillText(tok, 0, 0.5);
        c.restore();
      }
    },

    /* Décor : l'Atelier des Outils. Panneau perforé et établi à gauche, engrenages et tapis roulant à droite. */
    backdrop(c, env) {
      const W = env.W, gy = env.groundY, ink = "#3b4d7c", mid = "#2a3960", low = "#1a2440";
      // lampe d'atelier et son cône
      const lx = W * 0.2, ly = gy - 408;
      const cone = c.createLinearGradient(0, ly, 0, gy - 110); cone.addColorStop(0, "rgba(243,184,65,0.16)"); cone.addColorStop(1, "rgba(243,184,65,0)");
      c.fillStyle = cone; c.beginPath(); c.moveTo(lx - 16, ly); c.lineTo(lx + 16, ly); c.lineTo(lx + 150, gy - 110); c.lineTo(lx - 150, gy - 110); c.closePath(); c.fill();
      c.strokeStyle = mid; c.lineWidth = 2; c.beginPath(); c.moveTo(lx, 0); c.lineTo(lx, ly - 16); c.stroke();
      c.fillStyle = "#26335a"; c.beginPath(); c.moveTo(lx - 8, ly - 18); c.lineTo(lx + 8, ly - 18); c.lineTo(lx + 22, ly); c.lineTo(lx - 22, ly); c.closePath(); c.fill();
      c.fillStyle = "rgba(255,226,150,0.9)"; c.beginPath(); c.ellipse(lx, ly + 1, 12, 4, 0, 0, Math.PI * 2); c.fill();

      // panneau perforé
      const bx = W * 0.03, bw = W * 0.38, by = gy - 366, bh = 222;
      rr(c, bx, by, bw, bh, 6); c.fillStyle = "rgba(19,27,50,0.94)"; c.fill(); c.strokeStyle = mid; c.lineWidth = 2; c.stroke();
      c.fillStyle = "rgba(6,10,21,0.75)";
      for (let y = by + 12; y < by + bh - 6; y += 15) for (let x = bx + 12; x < bx + bw - 6; x += 15) c.fillRect(x, y, 2.4, 2.4);
      const tool = (fill) => { c.fillStyle = fill; c.fill(); c.strokeStyle = "rgba(90,110,165,0.55)"; c.lineWidth = 1.2; c.stroke(); };
      c.save(); c.translate(bx, by); c.lineJoin = "round";
      const u = bw / 290;   // les outils suivent la largeur du panneau
      // clé plate
      c.save(); c.translate(34 * u, 58); c.rotate(0.08);
      rr(c, -6, -24, 12, 98, 5); tool(ink);
      c.beginPath(); c.arc(0, -34, 16, 0, Math.PI * 2); tool(ink); c.beginPath(); c.arc(0, 80, 10, 0, Math.PI * 2); tool(ink);
      c.fillStyle = "rgba(19,27,50,1)"; c.beginPath(); c.arc(0, 80, 4.5, 0, Math.PI * 2); c.fill();
      c.beginPath(); c.moveTo(-6.5, -54); c.lineTo(-6.5, -37); c.arc(0, -37, 6.5, Math.PI, 0, true); c.lineTo(6.5, -54); c.closePath(); c.fill();
      c.restore();
      // marteau
      c.save(); c.translate(86 * u, 40);
      rr(c, -5, 0, 10, 128, 4); tool("#5a4632");
      rr(c, -26, -14, 46, 24, 4); tool(ink); c.beginPath(); c.moveTo(20, -12); c.lineTo(34, -16); c.lineTo(34, 12); c.lineTo(20, 8); c.closePath(); tool(ink);
      c.restore();
      // tournevis
      c.save(); c.translate(134 * u, 34);
      rr(c, -8, 0, 16, 48, 7); tool("#7a4a3a"); c.fillStyle = "rgba(255,255,255,0.08)"; c.fillRect(-3, 6, 2, 36);
      rr(c, -2.5, 48, 5, 70, 2); tool(ink); c.beginPath(); c.moveTo(-5, 118); c.lineTo(5, 118); c.lineTo(3, 128); c.lineTo(-3, 128); c.closePath(); tool(ink);
      c.restore();
      // scie
      c.save(); c.translate(168 * u, 46);
      c.beginPath(); c.moveTo(0, 0); c.lineTo(96 * u, 14); c.lineTo(96 * u, 26);
      for (let k = 12; k >= 0; k--) c.lineTo((96 * u * k) / 12, 40 - k * 1.1 + (k % 2 ? 0 : 5));
      c.closePath(); tool(mid);
      rr(c, -22, -6, 30, 52, 9); tool("#5a4632"); rr(c, -14, 6, 12, 28, 5); c.fillStyle = "rgba(19,27,50,1)"; c.fill();
      c.restore();
      // équerre et plan de schéma épinglé
      c.save(); c.translate(170 * u, 118);
      c.beginPath(); c.moveTo(0, 0); c.lineTo(0, 74); c.lineTo(58, 74); c.closePath(); c.moveTo(11, 30); c.lineTo(11, 63); c.lineTo(37, 63); c.closePath(); c.fillStyle = mid; c.fill("evenodd"); c.strokeStyle = "rgba(90,110,165,0.55)"; c.stroke();
      c.restore();
      c.save(); c.translate(236 * u, 108); c.rotate(-0.05);
      c.fillStyle = "rgba(95,216,230,0.13)"; c.fillRect(0, 0, 44, 84); c.strokeStyle = "rgba(95,216,230,0.4)"; c.lineWidth = 1; c.strokeRect(0.5, 0.5, 43, 83);
      c.fillStyle = "rgba(95,216,230,0.75)"; c.font = "700 17px " + F_MONO; c.textAlign = "left"; c.textBaseline = "alphabetic"; c.fillText("{", 5, 20); c.fillText("}", 5, 76);
      c.fillStyle = "rgba(95,216,230,0.4)"; for (let k = 0; k < 4; k++) c.fillRect(13, 27 + k * 9, 14 + ((k * 7) % 12), 2.5);
      c.fillStyle = "rgba(239,107,92,0.9)"; c.beginPath(); c.arc(22, 0, 3, 0, Math.PI * 2); c.fill();
      c.restore();
      c.restore();

      // établi et étau
      const ex = W * 0.015, ew = W * 0.43, ey = gy - 128;
      c.fillStyle = "#3a3048"; c.fillRect(ex, ey, ew, 11); c.fillStyle = "rgba(255,255,255,0.1)"; c.fillRect(ex, ey, ew, 2);
      c.fillStyle = "#251f33"; c.fillRect(ex + 10, ey + 11, ew - 20, 20); c.fillRect(ex + 16, ey + 31, 14, 100); c.fillRect(ex + ew - 30, ey + 31, 14, 100);
      c.fillStyle = "#322a42"; rr(c, ex + ew * 0.36, ey + 14, 64, 14, 2); c.fill(); c.fillStyle = "rgba(243,184,65,0.5)"; c.fillRect(ex + ew * 0.36 + 26, ey + 19, 12, 3);
      const vx = ex + ew * 0.76;
      c.fillStyle = "#3d4f80"; rr(c, vx - 26, ey - 10, 56, 10, 2); c.fill();
      rr(c, vx - 20, ey - 44, 14, 36, 3); c.fill(); rr(c, vx + 4, ey - 40, 13, 32, 3); c.fill();
      c.fillStyle = "#2c3b63"; c.fillRect(vx + 17, ey - 28, 30, 6); c.fillRect(vx + 42, ey - 42, 4, 34);
      c.fillStyle = "#56699c"; c.beginPath(); c.arc(vx + 44, ey - 43, 4, 0, Math.PI * 2); c.arc(vx + 44, ey - 7, 4, 0, Math.PI * 2); c.fill();
      c.strokeStyle = "rgba(243,184,65,0.75)"; c.lineWidth = 3.5; c.lineCap = "round"; brace(c, vx - 1, ey - 56, 13, 6, 5, -1, 0); c.stroke();   // une accolade serrée dans l'étau

      // grands engrenages (immobiles, très sombres) derrière le tapis
      const gearAt = (x, y, r, n, rot) => { gear(c, x, y, r, n, rot); c.fillStyle = "rgba(25,35,64,0.95)"; c.fill(); c.strokeStyle = "rgba(54,72,120,0.95)"; c.lineWidth = 2; c.stroke(); c.beginPath(); c.arc(x, y, r * 0.52, 0, Math.PI * 2); c.stroke(); c.fillStyle = "rgba(54,72,120,0.95)"; c.beginPath(); c.arc(x, y, r * 0.16, 0, Math.PI * 2); c.fill(); };
      gearAt(W * 0.955, gy - 78, 88, 18, 0.1); gearAt(W * 0.8, gy - 52, 54, 12, 0.4); gearAt(W * 0.555, gy - 58, 38, 10, 0.2);

      // tapis roulant et portique de validation
      const tx = W * 0.47, ty = gy - 100;
      c.fillStyle = low; for (let x = tx + 40; x < W; x += 110) c.fillRect(x, ty + 10, 7, 60);
      rr(c, tx, ty, W - tx + 30, 14, 7); c.fillStyle = "#1e2a4a"; c.fill(); c.strokeStyle = ink; c.lineWidth = 1.5; c.stroke();
      c.fillStyle = "rgba(95,216,230,0.16)"; c.fillRect(tx + 8, ty + 1.5, W - tx, 2);
      for (let x = tx + 9; x < W + 10; x += 30) { c.fillStyle = "#2c3b63"; c.beginPath(); c.arc(x, ty + 7, 4.2, 0, Math.PI * 2); c.fill(); }
      const px = W * 0.895;
      c.fillStyle = "#26335a"; c.fillRect(px - 26, ty - 58, 7, 58); c.fillRect(px + 19, ty - 58, 7, 58); rr(c, px - 32, ty - 72, 64, 18, 4); c.fill();
      c.fillStyle = "#33457a"; c.fillRect(px - 4, ty - 54, 8, 14); rr(c, px - 11, ty - 42, 22, 8, 2); c.fill();
      c.fillStyle = "rgba(109,240,168,0.85)"; c.font = "700 11px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText("{ ✓ }", px, ty - 62.5);
      c.fillStyle = "rgba(109,240,168,0.9)"; c.beginPath(); c.arc(px + 22.5, ty - 78, 3, 0, Math.PI * 2); c.fill();
    },
    /* Décor animé : les caisses avancent sur le tapis (rouges avant le portique, vertes après) et la roue d'entraînement tourne. */
    ambient(c, env, b) {
      const W = env.W, gy = env.groundY, time = env.time || (b && b.time) || 0, tx = W * 0.47, ty = gy - 100, span = W + 30 - tx, px = W * 0.895;
      c.font = "700 10px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle";
      for (let i = 0; i < 4; i++) {
        const x = tx + ((time * 0.055 + i / 4) % 1) * span, ok = x > px, cl = ok ? GREEN : "#ff7a6b";
        rr(c, x - 12, ty - 18, 24, 18, 3); c.fillStyle = "#1b2644"; c.fill(); c.strokeStyle = col(cl, 0.75); c.lineWidth = 1.5; c.stroke();
        c.fillStyle = col(cl, 0.9); c.fillText(ok ? "{}" : "{,", x, ty - 8.5);
      }
      gear(c, tx + 2, ty + 7, 17, 9, time * 0.9); c.fillStyle = "#33457a"; c.fill(); c.strokeStyle = "#4b5f96"; c.lineWidth = 1.5; c.stroke();
      c.fillStyle = "#141b2f"; c.beginPath(); c.arc(tx + 2, ty + 7, 5, 0, Math.PI * 2); c.fill();
    },

    draw(c, b) {
      const B = BOSSES[3], P = B.palette;
      const t = b.t || 0, time = b.time == null ? t : b.time, look = b.look || { x: -1, y: 0 };
      const enter = b.enter ?? 1, dying = b.dying ?? -1, dmg = b.dmg || 0;
      const fl = b.flash || 0, sq = b.squint || 0, beat = b.beat || 0, threat = b.threat || 0, gloat = b.gloat || 0, talk = b.talk || 0;
      const stun = (b.stun || 0) > 0, cp = b.cast != null && b.cast >= 0 ? clamp(b.cast / 0.9, 0, 1) : -1, castK = cp >= 0 ? Math.sin(cp * Math.PI) : 0;
      const A = atkPose(b), as = easeOut(A.strike), back = easeOut(A.wind) * (1 - as), fwd = as * (1 - easeInOut(A.rec));
      // mort : l'accolade se remet (dSnap), les lignes passent au vert (dGreen), le panneau se replie en « { } » (dFold), puis s'éteint
      const dead = dying >= 0, d = dead ? clamp(dying, 0, 1) : 0;
      const dSnap = easeIn(seg(d, 0, 0.2)), dGreen = seg(d, 0.16, 0.5), dFold = easeInOut(seg(d, 0.5, 0.8)), okK = dead ? seg(d, 0.12, 0.3) : 0;
      const rg = (b.rageT || 0) * (1 - seg(d, 0, 0.25));
      // mécanique parse : état réel (bad) et aspect de l'écran à cette image (scr), qui clignote avant la bascule
      const parse = !dead && b.mech && b.mech.parse ? b.mech.parse : null;
      const bad = !!(parse && parse.bad), pk = parse ? clamp(parse.k || 0, 0, 1) : 0;
      const warn = parse ? seg(pk, 0.8, 1) : 0, flick = warn > 0 && Math.sin(time * 38) > 0.55 - warn * 0.8;
      const scr = bad !== flick, punch = pk > 0 ? 1 - seg(pk, 0, 0.1) : 0, step = Math.floor(time * 9);

      const wh = (cl, a) => mixv(cl, C.white, fl * a);
      const frame = wh(mixv(mixv(P.main, P.rage, rg * 0.9), GREEN, okK), 0.7);            // griffe et cadre
      const tint = scr ? wh(RED, 0.6) : frame;                                           // couleur dominante de l'état
      const txt = wh(scr ? RED : mixv(P.main, GREEN, okK), 0.6);
      const eyeC = wh(scr ? "#ff5a68" : mixv(mixv("#8cecf6", "#ffb3e0", rg * 0.8), GREEN, okK), 1);
      const scrBg = wh(scr ? "#2e0c17" : mixv(mixv("#0b2230", "#0d2b3a", rg), "#0b2a1f", okK), 0.35);

      // extinction finale : « { } » clignote, puis se réduit à un trait
      let GA = seg(enter, 0, 0.04), vs = 0;
      if (dead) { if (d >= 0.95) { vs = seg(d, 0.95, 1); GA = 1 - vs; } else if (d >= 0.82) GA = Math.floor((d - 0.82) / 0.0325) % 2 ? 0.1 : 1; }
      if (GA <= 0.003) return;
      const snapK = enter >= 0.8 && enter < 1 ? 1 - seg(enter, 0.8, 0.94) : 0;            // la griffe vient de se clipser
      c.save();
      c.globalAlpha = GA;
      c.translate(snapK * Math.cos(enter * 70) * 7 + (stun ? Math.sin(time * 40) * 1.5 : 0) + threat * 4 + back * 7 - fwd * 9, -gloat * Math.abs(Math.sin(time * 15)) * 7);
      c.scale((1 + fl * 0.07 + beat * 0.012) * (1 + vs * 0.5), (1 - fl * 0.09 + beat * 0.012) * (1 - vs * 0.96));

      // halo de l'état
      const hr = 232 * easeOut(enter) * (1 - dFold * 0.55);
      if (hr > 6) {
        const g = c.createRadialGradient(PCX * 0.5, 0, 12, PCX * 0.5, 0, hr); g.addColorStop(0, col(tint, 0.2 + rg * 0.05 + beat * 0.04 + (scr ? 0.06 : 0))); g.addColorStop(1, col(tint, 0));
        c.fillStyle = g; c.fillRect(-hr, -hr, hr * 2 + 12, hr * 2);
      }
      // rémanence du dernier micro-saut
      const J = B.jump(t, b.rage);
      if (J.age < 0.14 && enter >= 1 && !dead) {
        c.strokeStyle = col(tint, 0.4 * (1 - J.age / 0.14)); c.lineWidth = 2;
        rr(c, PX + (J.prev.x - J.cur.x) * 0.8, PY + (J.prev.y - J.cur.y) * 0.8, PW, PH, 13); c.stroke();
      }

      // ---------- Panneau (replié à la mort autour de son centre) ----------
      const eOpen = Math.max(0.03, easeOut(seg(enter, 0, 0.14))), pa = 1 - seg(d, 0.66, 0.8);
      const x1 = PX + PW, y1 = PY + PH, r = 13, za = 5 * rg;
      const zig = (rev) => { for (let i = 1; i < 9; i++) { const j = rev ? 9 - i : i; c.lineTo(PX + (PW * j) / 9, SPLIT + (j % 2 ? za : -za)); } };
      c.save();
      c.translate(PCX, 0); c.scale(lerp(1, 0.1, dFold), lerp(1, 0.2, dFold) * eOpen); c.translate(-PCX, 0);
      c.globalAlpha = GA * pa;

      // panneaux fantômes de la rage : l'objet se dédouble, imbriqué dans lui-même
      if (rg > 0.02) for (let k = 2; k >= 1; k--) {
        const gx = (15 * k + (hash(step + k) > 0.8 ? 6 : 0)) * rg, gyy = -13 * k * rg;
        rr(c, PX + gx, PY + gyy, PW, PH, r); c.fillStyle = col(mixv("#0e1626", P.rage, 0.12), 0.8 * rg); c.fill();
        c.strokeStyle = col(frame, (0.62 - 0.17 * k) * rg); c.lineWidth = 2; c.stroke();
        c.fillStyle = col(frame, 0.2 * rg); for (let q = 0; q < 3; q++) c.fillRect(x1 + gx - 12 * k - 2, PY + gyy + 30 + q * 40, 8, 3);
      }
      // lueur dans la déchirure
      if (rg > 0.02) { c.strokeStyle = col(mixv(P.rage, C.white, 0.3 + 0.3 * Math.sin(time * 12)), rg); c.lineWidth = 12; c.lineCap = "butt"; c.beginPath(); c.moveTo(PX + 8, SPLIT + 1); c.lineTo(x1 - 2, SPLIT + 1); c.stroke(); }

      // --- moitié haute : barre de titre et visage
      c.save();
      c.translate(-5 * rg, -5 * rg); c.rotate(-0.04 * rg - (dmg >= 3 ? 0.025 : 0));
      if (rg > 0.02) {    // gyrophare
        const bx = PX + 30, sw = Math.cos(time * 9), on = 0.55 + 0.45 * Math.sin(time * 18);
        c.fillStyle = col(RED, 0.2 * rg * (0.5 + 0.5 * Math.abs(sw)));
        c.beginPath(); c.moveTo(bx, PY - 6); c.lineTo(bx + sw * 96, PY - 26); c.lineTo(bx + sw * 96, PY + 8); c.closePath(); c.fill();
        c.beginPath(); c.moveTo(bx, PY - 6); c.lineTo(bx - sw * 60, PY - 20); c.lineTo(bx - sw * 60, PY + 4); c.closePath(); c.fill();
        c.fillStyle = col(mixv(RED, C.white, on * 0.6), rg); c.beginPath(); c.arc(bx, PY + 1, 10 * rg, Math.PI, 0); c.fill();
        c.fillStyle = col("#3a4666", rg); c.fillRect(bx - 12 * rg, PY - 1, 24 * rg, 3);
      }
      c.beginPath(); c.moveTo(PX, SPLIT); c.lineTo(PX, PY + r); c.arcTo(PX, PY, PX + r, PY, r); c.lineTo(x1 - r, PY); c.arcTo(x1, PY, x1, PY + r, r); c.lineTo(x1, SPLIT); zig(true); c.closePath();
      c.fillStyle = col(scrBg, 0.97); c.fill(); c.strokeStyle = col(tint, 0.9); c.lineWidth = 2.4; c.lineJoin = "round"; c.stroke();
      rr(c, PX + 3.5, PY + 3.5, PW - 7, 15, 9); c.fillStyle = "rgba(3,8,15,0.6)"; c.fill();
      for (let k = 0; k < 3; k++) { c.fillStyle = k < dmg ? "rgba(255,255,255,0.1)" : col([RED, GOLD, GREEN][k], 0.9); c.beginPath(); c.arc(PX + 13 + k * 10, PY + 11, 3, 0, Math.PI * 2); c.fill(); }
      c.textBaseline = "middle"; c.textAlign = "left"; c.font = "600 9px " + F_MONO;
      const name = "sortie.json", nt = seg(enter, 0.05, 0.16);
      c.fillStyle = col(tint, 0.75); c.fillText(nt < 1 ? name.slice(0, Math.floor(name.length * nt)) : name, PX + 42, PY + 11.5);
      if (enter > 0.3) {  // voyant d'état
        const on = scr ? 0.65 + 0.35 * Math.sin(time * 16) : 1;
        rr(c, x1 - 42, PY + 5, 34, 12, 6); c.fillStyle = col(scr ? RED : GREEN, 0.92 * on); c.fill();
        c.fillStyle = "#06121c"; c.font = "700 8.5px " + F_MONO; c.textAlign = "center"; c.fillText(scr ? "ERR" : "200", x1 - 25, PY + 11.5);
      }
      if (parse) {        // temps restant dans l'état en cours
        c.fillStyle = "rgba(255,255,255,0.1)"; c.fillRect(PX + 8, PY + 21, PW - 16, 2.5);
        c.fillStyle = col(scr ? RED : GREEN, warn > 0 && !flick ? 0.5 : 0.95); c.fillRect(PX + 8, PY + 21, (PW - 16) * (1 - pk), 2.5);
      }
      // yeux : fentes en colère, pupilles qui suivent la cible
      const eyeOn = easeOut(seg(enter, 0.36, 0.5)), calm = dead ? seg(d, 0.08, 0.3) : 0, shut = dead && d > 0.3;
      if (eyeOn > 0) {
        const blink = t % 3.7 > 3.57 || t % 5.9 > 5.8 ? 1 : 0;
        const open = (1 - 0.88 * blink) * (1 - 0.6 * sq) * (1 - 0.25 * threat) * eyeOn * (stun ? 0.4 : 1) * (1 + 0.12 * back);
        const slant = (7 + 3 * rg + 4 * threat + 4 * back) * (1 - calm) * (1 - gloat * 0.4);
        const gj = scr ? (hash(step * 1.3) - 0.5) * 3 : 0;
        const EYES = [[-39, -40, 22, 14, 1], [25, -40, 20, 13, -1]];    // x, y, demi-largeur, demi-hauteur, côté intérieur
        if (shut) {       // validé : yeux fermés, apaisés
          c.strokeStyle = col(eyeC); c.lineWidth = 3.2; c.lineCap = "round";
          for (const e of EYES) { c.beginPath(); c.arc(e[0], e[1] - 5, 13, 0.2 * Math.PI, 0.8 * Math.PI); c.stroke(); }
        } else {
          c.save(); if (!stun) { c.shadowColor = col(eyeC); c.shadowBlur = 12; }
          c.fillStyle = col(eyeC, stun ? 0.5 : 1); c.beginPath();
          for (const e of EYES) {
            const m = scr ? (e[4] > 0 ? 1.14 : 0.8) : 1, hw = e[2] * m, hh = e[3] * m * open, ex = e[0] + gj, ey = e[1] + (scr && e[4] < 0 ? 3 : 0);
            const top = ey - hh, bot = ey + hh, inTop = Math.min(top + slant * m, bot - 1.6);
            c.moveTo(ex - e[4] * hw, top - slant * 0.15); c.lineTo(ex + e[4] * hw, inTop); c.lineTo(ex + e[4] * hw, bot); c.lineTo(ex - e[4] * hw, bot); c.closePath();
          }
          c.fill(); c.restore();
          for (const e of EYES) {
            const m = scr ? (e[4] > 0 ? 1.14 : 0.8) : 1, hh = e[3] * m * open, ex = e[0] + gj, ey = e[1] + (scr && e[4] < 0 ? 3 : 0);
            if (gloat > 0.15) { c.fillStyle = col(scrBg); c.beginPath(); c.ellipse(ex, ey + hh + 3, e[2] * 1.05, hh * 1.25 * gloat + 3, 0, 0, Math.PI * 2); c.fill(); }
            if (hh > 4.5) {
              const px = ex + (stun ? Math.cos(time * 9 + e[4]) * 6 : clamp(look.x, -1, 1) * 9), py = ey + 1.5 + (stun ? Math.sin(time * 9 + e[4]) * 3 : clamp(look.y, -1, 1) * 3.5) + slant * 0.25 - gloat * 3;
              const ph = Math.min(15, hh * 2 - 4) * (1 - threat * 0.25), pw = 10.5 - threat * 2.5;
              c.fillStyle = "#04101a"; rr(c, px - pw / 2, py - ph / 2, pw, ph, 2.5); c.fill();
              c.fillStyle = "rgba(255,255,255,0.85)"; c.fillRect(px - pw / 2 + 1.2, py - ph / 2 + 1.2, 3, 3);
            }
          }
          if (dmg >= 2) { c.fillStyle = col(scrBg); c.fillRect(33, -49, 8, 6); c.strokeStyle = col(scrBg); c.lineWidth = 2; c.beginPath(); c.moveTo(13, -55); c.lineTo(26, -41); c.lineTo(21, -37); c.lineTo(36, -26); c.stroke(); }   // œil droit : pixels morts
          if (scr && hash(step * 2.1) > 0.55) { c.fillStyle = col(eyeC, 0.8); c.fillRect(-68 + hash(step) * 12, -46 + hash(step + 4) * 12, 56, 2.5); }
        }
        // bouche : une ligne brisée, qui s'ouvre en mâchoires dentelées
        const mo = Math.max(talk * 7, back * 4 + fwd * 11, gloat * (5 + 3 * Math.sin(time * 15)), castK * 6, stun ? 2 : 0) * eyeOn;
        const bend = dead ? lerp(-3, 4.5, calm) : lerp(-3 - rg, 7, gloat), amp = (3.2 + rg) * (1 - calm * 0.75), mx = -7, mw = 25 + gloat * 8 + rg * 3, my = -14.5;
        const mp = (i, off) => { const q = i / 8; c.lineTo(mx - mw + 2 * mw * q, my + (i % 8 ? (i % 2 ? -amp : amp) : 0) + bend * (1 - (2 * q - 1) ** 2) + off); };
        c.strokeStyle = col(eyeC, eyeOn); c.lineWidth = 2.3; c.lineJoin = "round"; c.lineCap = "round";
        c.beginPath();
        if (mo > 0.6) { for (let i = 0; i <= 8; i++) mp(i, -mo * 0.3); for (let i = 8; i >= 0; i--) mp(i, mo); c.closePath(); c.fillStyle = "#02070c"; c.fill(); }
        else for (let i = 0; i <= 8; i++) mp(i, 0);
        c.stroke();
      }
      c.restore();

      // --- moitié basse : les lignes "clé": valeur
      c.save();
      c.translate(7 * rg, 5 * rg); c.rotate(0.032 * rg);
      c.beginPath(); c.moveTo(PX, SPLIT); zig(false); c.lineTo(x1, SPLIT); c.lineTo(x1, y1 - 30);
      if (dmg >= 2) { c.lineTo(x1 - 5, y1 - 24); c.lineTo(x1 - 15, y1 - 21); c.lineTo(x1 - 17, y1 - 9); c.lineTo(x1 - 30, y1); }   // coin ébréché
      else { c.lineTo(x1, y1 - r); c.arcTo(x1, y1, x1 - r, y1, r); }
      c.lineTo(PX + r, y1); c.arcTo(PX, y1, PX, y1 - r, r); c.closePath();
      c.fillStyle = col(scrBg, 0.97); c.fill(); c.strokeStyle = col(tint, 0.9); c.lineWidth = 2.4; c.lineJoin = "round"; c.stroke();
      if (dmg >= 2) { const fy = Math.sin(t * 1.7) * 3; c.fillStyle = col(scrBg, 0.9); c.beginPath(); c.moveTo(x1 + 6, y1 - 14 + fy); c.lineTo(x1 + 15, y1 - 4 + fy); c.lineTo(x1 + 2, y1 + 4 + fy); c.closePath(); c.fill(); c.strokeStyle = col(tint, 0.7); c.lineWidth = 1.5; c.stroke(); }
      c.font = "600 11px " + F_MONO; c.textAlign = "left"; c.textBaseline = "middle";
      const cw = c.measureText("0").width, rep = dead ? Math.max(dmg ? dmg + 1 : 0, Math.ceil(dGreen * 5 - 0.001)) : dmg ? dmg + 1 : 0;
      for (let i = 0; i < 5; i++) {
        const typed = seg(enter, 0.14 + i * 0.09, 0.26 + i * 0.09); if (typed <= 0) break;
        const R = ROWS[i], y = 11 + i * 14, fixed = i < rep, x = PX + 11;
        let dx = castK * Math.sin(time * 30 + i * 2) * 9 + fl * (hash(i + step) - 0.5) * 12;
        if (scr) {
          const gh = hash(i * 5.3 + Math.floor(time * 7) * 1.7); if (gh > 0.6) dx += (gh - 0.79) * 76 * (1 + punch * 1.5);
          c.fillStyle = col(RED, 0.14 + 0.12 * hash(i * 9 + step)); c.fillRect(PX - 7 + dx * 1.3, y - 6.5, PW + 14, 13);
          const s = scramble(R[0] + R[1], i, step, 0.42 + punch * 0.4);
          c.fillStyle = "rgba(73,230,255,0.5)"; c.fillText(s, x + dx - 2.4, y);
          c.fillStyle = col(txt); c.fillText(s, x + dx + 0.8, y);
          c.strokeStyle = col(txt, fixed ? 0.35 : 0.95); c.lineWidth = 2; cross(c, x1 - 13 + dx, y, 1);
        } else {
          let key = R[0], val = fixed ? R[2] : R[1];
          if (typed < 1) { const n = Math.floor((key.length + val.length) * typed); val = val.slice(0, Math.max(0, n - key.length)); key = key.slice(0, n); }
          const keyC = fixed ? mixv(GREEN, C.white, 0.25) : mixv(mixv("#d6f3f7", GREEN, okK), C.white, fl * 0.5);
          c.fillStyle = col(keyC, 0.92); c.fillText(key, x + dx, y);
          c.fillStyle = col(fixed ? wh(GREEN, 0.5) : txt); c.fillText(val, x + dx + key.length * cw, y);
          if (typed < 1) { c.fillStyle = col(txt); c.fillRect(x + dx + (key.length + val.length) * cw + 1, y - 6, 6, 12); }
          else if (fixed) { c.strokeStyle = col(GREEN); c.lineWidth = 2.3; c.lineCap = "round"; tick(c, x1 - 13, y, 1); }
          else {            // valeur encore fausse : soulignée comme un avertissement de linter
            const vx = x + dx + key.length * cw, n = Math.max(2, Math.floor((val.length * cw) / 4));
            c.strokeStyle = col(GOLD, 0.7); c.lineWidth = 1.1; c.beginPath(); for (let q = 0; q <= n; q++) c.lineTo(vx + q * 4, y + 6.4 + (q % 2 ? 1.6 : 0)); c.stroke();
            if (i === 4 && enter >= 1 && time % 1 < 0.5) { c.fillStyle = col(txt, 0.9); c.fillRect(vx + val.length * cw + 2, y - 6, 6, 12); }
          }
        }
      }
      // bascule : balayage vert quand il redevient valide, éclair rouge quand il se corrompt
      if (punch > 0) {
        if (bad) { c.fillStyle = col(RED, punch * 0.3); c.fillRect(PX, SPLIT, PW, y1 - SPLIT); }
        else { const sy = lerp(SPLIT, y1 - 3, 1 - punch); c.fillStyle = col(GREEN, 0.1 * punch); c.fillRect(PX + 2, SPLIT, PW - 4, sy - SPLIT); c.fillStyle = col(GREEN, 0.85 * punch); c.fillRect(PX + 2, sy - 1.5, PW - 4, 3); }
      }
      c.restore();
      if (dmg >= 1 && Math.sin(time * 23) > 0.86) { c.fillStyle = "rgba(255,255,255,0.1)"; c.fillRect(PX + 2, PY + ((time * 90) % PH), PW - 4, 4); }   // balayage qui saute
      if (cp >= 0) for (let k = 0; k < 2; k++) { const q = clamp(cp * 1.4 - k * 0.3, 0, 1); if (q > 0 && q < 1) { c.strokeStyle = col(tint, (1 - q) * 0.7); c.lineWidth = 2.5; rr(c, PX - q * 34, PY - q * 26, PW + q * 68, PH + q * 52, 13 + q * 14); c.stroke(); } }
      if (okK < 1) drawCracks(c, b, col(mixv(tint, C.white, 0.5), 0.75 * (1 - okK)), 1.6);
      c.restore();
      c.globalAlpha = GA;

      // ---------- Côté droit : l'accolade manquante (silhouette en pointillés, moignons, caractères qui fuient) ----------
      const gA = seg(enter, 0.5, 0.7) * (1 - dSnap) * (1 - dFold);
      if (gA > 0.01) {
        const gx = SLOT + 6 * rg;
        c.save(); c.setLineDash([5, 7]); c.lineDashOffset = -time * 12; c.strokeStyle = col(tint, 0.34 * gA); c.lineWidth = 2.5; c.lineCap = "round";
        brace(c, gx, 0, 94, 22, 26, 1, 0); c.stroke(); c.restore();
        c.strokeStyle = col(tint, 0.85 * gA); c.lineWidth = 8; c.lineCap = "round";
        c.beginPath(); c.moveTo(gx - 22, -94); c.quadraticCurveTo(gx - 6, -94, gx - 2, -82); c.stroke();
        c.beginPath(); c.moveTo(gx - 22, 94); c.quadraticCurveTo(gx - 6, 94, gx - 2, 82); c.stroke();
        if (hash(step * 3.7) > 0.7) { c.strokeStyle = col(GOLD, 0.9 * gA); c.lineWidth = 1.5; const sy = hash(step) > 0.5 ? -80 : 80; c.beginPath(); c.moveTo(gx - 1, sy); c.lineTo(gx + 7, sy - 5); c.lineTo(gx + 4, sy + 2); c.lineTo(gx + 12, sy + 3); c.stroke(); }
        c.font = "600 11px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle";
        for (let k = 0; k < 6; k++) {
          const q = (t * 0.33 + k / 6 + hash(k) * 0.3) % 1;
          c.fillStyle = col(txt, (1 - q) * 0.6 * gA); c.fillText(',":01;'[k], x1 + 4 + q * 44 + Math.sin(k * 5) * 5, -34 + k * 18 + q * q * 40);
        }
      }

      // ---------- Griffe « { » ----------
      if (enter > 0.62) {
        const fly = 1 - easeIn(seg(enter, 0.62, 0.8));
        const cx = lerp(-104 - 5 * rg, PCX - 24, dFold) - fly * 210 + snapK * 8 + 20 * back - 30 * fwd - 5 * threat + castK * Math.sin(time * 40) * 3;
        const ch = lerp(96 + 7 * back - 5 * fwd + Math.sin(t * 2.1) * 1.5 + gloat * 4, 30, dFold), cwid = lerp(24, 9, dFold), clw = lerp(12, 6.5, dFold);
        const ctip = lerp(30 - 12 * back + 26 * fwd + beat * 3 + threat * 5, 9, dFold), broken = dmg >= 3 && !dead;
        c.lineCap = "round"; c.lineJoin = "round";
        if (fwd > 0.05) for (let k = 1; k <= 2; k++) { c.strokeStyle = col(frame, 0.2 * fwd / k); c.lineWidth = clw; brace(c, cx + 20 * k * fwd, 0, ch, cwid, ctip, -1, 0, broken); c.stroke(); }   // traînée de la détente
        if (rg > 0.02 && dFold < 0.5) for (let k = 2; k >= 1; k--) {    // accolades imbriquées de la rage
          const nx = cx - 16 * k * rg + 6 * k * fwd + Math.sin(t * 3 + k) * 1.5;
          c.strokeStyle = col(mixv(frame, C.white, 0.1 * k), (0.9 - 0.22 * k) * rg * (1 - dFold * 2)); c.lineWidth = clw - 2.5 * k;
          brace(c, nx, 0, ch + 9 * k * rg, cwid, ctip - 2 * k, -1, 0); c.stroke();
        }
        c.save(); c.shadowColor = col(frame); c.shadowBlur = 14 + beat * 6 + back * 12 + snapK * 20;
        c.strokeStyle = col(mixv(frame, C.white, snapK * 0.7)); c.lineWidth = clw; brace(c, cx, 0, ch, cwid, ctip, -1, 0, broken); c.stroke();
        c.restore();
        c.fillStyle = col(frame);     // pointe et serres
        const sharp = 1 - (dead ? seg(d, 0.2, 0.42) : 0);
        if (sharp > 0) {
          c.beginPath(); c.moveTo(cx - ctip + 5, -clw * 0.5); c.lineTo(cx - ctip - 13 * sharp, 0); c.lineTo(cx - ctip + 5, clw * 0.5); c.closePath(); c.fill();
          c.beginPath(); c.moveTo(cx + cwid - 2, -ch - clw * 0.5); c.lineTo(cx + cwid + 13 * sharp, -ch + 4); c.lineTo(cx + cwid - 2, -ch + clw * 0.5); c.closePath(); c.fill();
          if (!broken) { c.beginPath(); c.moveTo(cx + cwid - 2, ch - clw * 0.5); c.lineTo(cx + cwid + 13 * sharp, ch - 4); c.lineTo(cx + cwid - 2, ch + clw * 0.5); c.closePath(); c.fill(); }
        }
        c.strokeStyle = "rgba(255,255,255,0.6)"; c.lineWidth = clw * 0.26; brace(c, cx, 0, ch, cwid, ctip, -1, 0, broken); c.stroke();
        if (dmg >= 1 && !dead) {      // entailles, puis crochet du bas cassé qui pend
          c.fillStyle = "#0b1426"; c.beginPath(); c.moveTo(cx + 8, -ch * 0.6); c.lineTo(cx - 2, -ch * 0.555); c.lineTo(cx + 8, -ch * 0.51); c.closePath(); c.fill();
          if (dmg >= 2) { c.beginPath(); c.moveTo(cx - 8, ch * 0.3); c.lineTo(cx + 2, ch * 0.35); c.lineTo(cx - 8, ch * 0.4); c.closePath(); c.fill(); c.beginPath(); c.moveTo(cx - 8, -ch * 0.3); c.lineTo(cx, -ch * 0.27); c.lineTo(cx - 8, -ch * 0.24); c.closePath(); c.fill(); }
          if (broken) {
            c.save(); c.translate(cx + 3, ch * 0.66); c.rotate(0.35 + Math.sin(t * 2.6) * 0.22);
            c.strokeStyle = col(frame, 0.75); c.lineWidth = clw - 2; c.beginPath(); c.moveTo(0, 6); c.lineTo(0, 16); c.quadraticCurveTo(0, 30, 18, 30); c.stroke();
            c.restore();
            if (hash(step * 1.9) > 0.6) { c.strokeStyle = col(GOLD, 0.95); c.lineWidth = 1.5; c.beginPath(); c.moveTo(cx, ch * 0.58); c.lineTo(cx - 7, ch * 0.66); c.lineTo(cx - 2, ch * 0.68); c.lineTo(cx - 8, ch * 0.78); c.stroke(); }
          }
        }
        if (back > 0.05) {            // l'éclat se forme au bout de la pointe
          const sx = cx - ctip - 20, sr = 5 + back * 9;
          c.fillStyle = col(RED, 0.3 * back); c.beginPath(); c.arc(sx, 0, sr * 1.9, 0, Math.PI * 2); c.fill();
          c.fillStyle = col(mixv(RED, C.white, 0.5), back); c.beginPath(); c.moveTo(sx - sr, 0); c.lineTo(sx - 1, -sr * 0.7); c.lineTo(sx + sr * 0.7, -1); c.lineTo(sx + 1, sr * 0.75); c.closePath(); c.fill();
        }
      }

      // ---------- Étiquette SyntaxError ----------
      if (parse && enter >= 1 && (bad || flick)) {
        const ta = bad ? (flick ? 0.4 : 1) : 0.45, ts = 1 + punch * 0.55;
        c.save(); c.globalAlpha = GA * ta; c.translate(54 + (hash(step) - 0.5) * 3, -93); c.rotate(-0.06); c.scale(ts, ts);
        c.fillStyle = col(RED); rr(c, -53, -11.5, 106, 23, 5); c.fill();
        c.beginPath(); c.moveTo(-34, 10); c.lineTo(-27, 20); c.lineTo(-18, 10); c.closePath(); c.fill();
        c.fillStyle = "#2a060c"; c.font = "700 12.5px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText("SyntaxError", 0, 0.5);
        c.restore(); c.globalAlpha = GA;
      }

      // ---------- L'accolade fermante « } » : en orbite (cible critique), éteinte et cassée quand il est corrompu ----------
      const ba = seg(enter, 0.78, 0.84);
      if (ba > 0) {
        const ws = B.weakSpot(b), slotX = lerp(SLOT, PCX + 24, dFold), mv = dead ? dSnap : 1 - easeOut(seg(enter, 0.86, 1));   // mv : 0 en orbite, 1 dans son logement
        const ox = lerp(ws.x, slotX, mv), oy = lerp(ws.y, 0, mv), big = dead ? dSnap : 0;
        const oh = lerp(17, lerp(96, 30, dFold), big), ow = lerp(8, lerp(24, 9, dFold), big), ot = lerp(8, lerp(30, 9, dFold), big), olw = lerp(6, lerp(12, 6.5, dFold), big);
        c.lineCap = "round"; c.lineJoin = "round";
        if (bad && !flick) {
          const fa = 0.5 + 0.2 * hash(step * 1.7), cl = mixv("#8b93ad", RED, 0.35);
          c.globalAlpha = GA * ba * fa;
          c.strokeStyle = col(cl); c.lineWidth = 5;
          c.save(); c.translate(ox - 3, oy - 5); c.rotate(-0.38); brace(c, 0, 0, oh, ow, ot, 1, -1); c.stroke(); c.restore();
          c.save(); c.translate(ox + 3, oy + 5); c.rotate(0.3); brace(c, 0, 0, oh, ow, ot, 1, 1); c.stroke(); c.restore();
          c.strokeStyle = col(RED); c.lineWidth = 2.4; cross(c, ox + 15, oy - 15, 1.2);
          c.globalAlpha = GA;
        } else {
          const cl = dead ? mixv(GOLD, GREEN, seg(d, 0.1, 0.25)) : mixv(GOLD, C.white, fl * 0.6), pulse = 1 + Math.sin(t * 6) * 0.1 + beat * 0.15;
          if (!dead && enter >= 1) for (let k = 1; k <= 4; k++) { const p = B.orbit(b, k * 0.11); c.fillStyle = col(cl, 0.11 * (5 - k)); c.beginPath(); c.arc(p.x, p.y, 9 - k * 1.5, 0, Math.PI * 2); c.fill(); }
          const gr = lerp(34 * pulse, 64, big), ga2 = dead ? 0.6 * (1 - seg(d, 0.2, 0.34)) : 0.6 * ba;
          if (ga2 > 0.01) { const g = c.createRadialGradient(ox, oy, 2, ox, oy, gr); g.addColorStop(0, col(cl, ga2)); g.addColorStop(1, col(cl, 0)); c.fillStyle = g; c.fillRect(ox - gr, oy - gr, gr * 2, gr * 2); }
          if (!dead) { c.strokeStyle = col("#3a2a06", 0.6 * ba); c.lineWidth = olw + 3.5; brace(c, ox, oy, oh, ow, ot, 1, 0); c.stroke(); }
          c.save(); if (dead) { c.shadowColor = col(cl); c.shadowBlur = 14 * big; }
          c.strokeStyle = col(mixv(cl, C.white, dead ? 0 : 0.25), ba); c.lineWidth = olw; brace(c, ox, oy, oh, ow, ot, 1, 0); c.stroke(); c.restore();
          c.strokeStyle = "rgba(255,255,255,0.7)"; c.lineWidth = olw * 0.28; brace(c, ox, oy, oh, ow, ot, 1, 0); c.stroke();
          if (dead && d > 0.18 && d < 0.4) { const q = seg(d, 0.18, 0.4); c.strokeStyle = col(GREEN, 1 - q); c.lineWidth = 4 * (1 - q) + 1; c.beginPath(); c.arc(slotX, 0, 20 + q * 90, 0, Math.PI * 2); c.stroke(); }   // clic !
        }
      }

      // étourdi : jetons perdus qui tournent au-dessus de lui
      if (stun && !dead) { c.font = "700 13px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle"; for (let k = 0; k < 3; k++) { const a = time * 4 + (k * Math.PI * 2) / 3; c.fillStyle = col(GOLD, 0.6 + 0.4 * Math.sin(a)); c.fillText("?,;"[k], PCX - 20 + Math.cos(a) * 46, PY - 16 + Math.sin(a) * 9); } }
      c.restore();
    }
  };
}
