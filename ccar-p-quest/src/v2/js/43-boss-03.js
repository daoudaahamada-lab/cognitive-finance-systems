/* Étage 3 — Le Schéma Brisé : un objet JSON vivant dont l'accolade fermante s'est échappée. */
BOSSES[3] = {
  palette: { main: "#5fd8e6", dark: "#173042", accent: "#f3b841", eye: "#5fd8e6", rage: "#ff4f9a" },
  hit: { rx: 140, ry: 100, coreR: 22 },
  top: 116,
  attackFrom: { x: -152, y: 0 },
  castLean: -0.1,
  weakSpot(b) { const a = b.t * (b.rage ? 1.35 : 0.75); return { x: Math.cos(a) * 158, y: Math.sin(a) * 94 }; },
  critLabel: "} FERMÉ",
  lines: {
    hit: ["Une virgule de moins !", "Mon champ obligatoire !", "Tu valides mes types ?!"],
    crit: ["Tu as fermé mon accolade !", "Parsé ! Je suis parsé !"],
    wrong: ["« Respond only in JSON », hein ?", "Encore un parseur à base de regex.", "SyntaxError: unexpected token."],
    timeout: ["Timeout. Réessaie… sans schéma.", "Ta requête a expiré."],
    rage: "Je corromps tous tes champs à la fois !",
    special: { glitch: ["Unexpected end of JSON input.", "Champ manquant ? Quel champ ?"] }
  },
  intro: {
    title: "L’accolade manquante",
    text: "Son point faible est l’accolade fermante qui lui manque : elle tourne autour de lui, plus vite quand il enrage. Touche-la pour un coup critique « } FERMÉ » : un JSON valide est un JSON contraint par un schéma."
  },
  mechanics: [],
  draw(c, b) {
    const t = b.t, fl = b.flash, rg = b.rageT;
    const cyan = mixv(mixv("#5fd8e6", C.rage, rg * 0.8), C.white, fl * 0.7);
    const dark = mixv("#173042", C.white, fl * 0.35);
    const amber = mixv("#f3b841", C.white, fl * 0.5);
    const eye = mixv(mixv("#5fd8e6", C.bad, rg), C.white, fl);
    const glitchK = 0.6 + rg * 1.2;

    // l'accolade gauche recule puis frappe comme une griffe
    let reach = 0;
    if (b.atk >= 0) {
      const a = b.atk;
      reach = a < 0.22 ? 12 * (a / 0.22) : a < 0.34 ? 12 - 58 * ((a - 0.22) / 0.12) : -46 * Math.max(0, 1 - (a - 0.34) / 0.41);
    }

    const halo = c.createRadialGradient(0, 0, 20, 0, 0, 240);
    halo.addColorStop(0, col(cyan, 0.16)); halo.addColorStop(1, col(cyan, 0));
    c.fillStyle = halo; c.fillRect(-250, -230, 500, 460);

    // fantôme de l'accolade droite disparue + éclats
    c.save(); c.setLineDash([6, 7]); c.strokeStyle = col(cyan, 0.28); c.lineWidth = 3;
    c.beginPath(); c.moveTo(100, -102); c.quadraticCurveTo(122, -98, 122, -78); c.lineTo(122, -22); c.quadraticCurveTo(124, -4, 146, 0); c.quadraticCurveTo(124, 4, 122, 22); c.lineTo(122, 78); c.quadraticCurveTo(122, 98, 100, 102); c.stroke();
    c.restore();
    c.strokeStyle = col(cyan, 0.75); c.lineWidth = 7; c.lineCap = "round";
    c.beginPath(); c.moveTo(102, -100); c.quadraticCurveTo(120, -96, 121, -80); c.stroke();
    c.beginPath(); c.moveTo(121, 82); c.quadraticCurveTo(120, 98, 102, 100); c.stroke();
    c.fillStyle = col(cyan, 0.6);
    for (let k = 0; k < 4; k++) { const y = -60 + k * 34 + Math.sin(t * 2 + k) * 4; c.fillRect(128 + Math.sin(t * 1.3 + k * 2) * 6, y, 5, 9); }

    // panneau (corps)
    rr(c, -100, -72, 200, 144, 16);
    c.fillStyle = col(dark, 0.94); c.fill();
    c.strokeStyle = col(cyan, 0.55); c.lineWidth = 2; c.stroke();

    // visage
    c.save(); c.globalAlpha = b.stun > 0 ? 0.4 : 1;
    angryEyes(c, 6, -50, 22, 7, eye, b.squint, 10);
    const open = b.atk >= 0.2 && b.atk < 0.55 ? 1 : 0;
    c.strokeStyle = col(eye); c.lineWidth = 2.4; c.lineJoin = "round";
    c.beginPath(); c.moveTo(-26, -30 + open * 3);
    for (let k = 1; k <= 8; k++) c.lineTo(-26 + k * 6, k % 2 ? -34 - open * 3 : -30 + open * 3);
    c.stroke();
    c.restore();

    // lignes clé: valeur ; celles qui sont corrigées passent au vert quand sa vie baisse
    const rows = [
      ['"order_id": ', "4812,", "4812,"],
      ['"amount": ', '"12,5O",', "12.50,"],
      ['"status": ', ",", '"paid",'],
      ['"items": ', '[{"sku": 3', '[{"sku": 3}],'],
      ['"date": ', '"2026-13-45"', '"2026-11-08"']
    ];
    const fixed = 4 - Math.ceil(clamp(b.hpFrac, 0, 1) * 4);
    c.font = "600 13px " + F_MONO; c.textAlign = "left"; c.textBaseline = "middle";
    rows.forEach((r, i) => {
      const y = -10 + i * 17;
      const ok = i === 0 || i > 4 - fixed;
      let dx = 0;
      if (!ok && Math.sin(b.time * 7 * glitchK + i * 3.1) > 0.82) dx = 6 * (i % 2 ? 1 : -1);
      if (b.cast >= 0) dx += Math.sin(b.cast * 30 + i * 2) * 14 * (1 - b.cast / 0.9);
      const x = -84 + dx;
      const val = ok ? r[2] : r[1];
      if (!ok) {
        c.fillStyle = col(C.rage, 0.55); c.fillText(r[0] + val, x + 2, y);
        c.fillStyle = col("#5fd8e6", 0.55); c.fillText(r[0] + val, x - 2, y);
      }
      c.fillStyle = col(amber); c.fillText(r[0], x, y);
      const kw = c.measureText(r[0]).width;
      c.fillStyle = ok ? col(mixv(C.ok, C.white, fl * 0.5)) : col(mixv(C.bad, C.white, fl * 0.5));
      c.fillText(val, x + kw, y);
      if (ok && i > 0) { c.fillStyle = col(C.ok); c.fillText("✓", 78, y); }
    });

    drawCracks(c, b, col(cyan, 0.7), 1.6);

    // accolade gauche : bras-griffe
    c.save(); c.translate(reach, 0);
    c.shadowColor = col(cyan); c.shadowBlur = 12;
    c.strokeStyle = col(cyan); c.lineWidth = 13; c.lineCap = "round"; c.lineJoin = "round";
    c.beginPath(); c.moveTo(-100, -104); c.quadraticCurveTo(-122, -100, -122, -80); c.lineTo(-122, -24); c.quadraticCurveTo(-124, -6, -148, 0); c.quadraticCurveTo(-124, 6, -122, 24); c.lineTo(-122, 80); c.quadraticCurveTo(-122, 100, -100, 104); c.stroke();
    c.restore();

    // message d'erreur pendant une action spéciale
    if (b.cast >= 0) {
      const k = clamp(b.cast / 0.9, 0, 1);
      c.font = "700 14px " + F_MONO; c.textAlign = "center"; c.fillStyle = col(C.bad, 1 - k * 0.6);
      c.fillText("SyntaxError", Math.sin(b.time * 40) * 3, -88 - k * 12);
    }

    // l'accolade fermante en fuite (point faible), avec sa traînée
    const orbit = BOSSES[3].weakSpot(b);
    for (let k = 1; k <= 4; k++) {
      const a = b.t * (b.rage ? 1.35 : 0.75) - k * 0.12;
      c.fillStyle = col(amber, 0.12 * (5 - k));
      c.beginPath(); c.arc(Math.cos(a) * 158, Math.sin(a) * 94, 10 - k, 0, Math.PI * 2); c.fill();
    }
    const pulse = 1 + Math.sin(t * 6) * 0.1;
    const og = c.createRadialGradient(orbit.x, orbit.y, 2, orbit.x, orbit.y, 32 * pulse);
    og.addColorStop(0, col(amber, 0.7)); og.addColorStop(1, col(amber, 0));
    c.fillStyle = og; c.beginPath(); c.arc(orbit.x, orbit.y, 32 * pulse, 0, Math.PI * 2); c.fill();
    c.save(); c.setLineDash([4, 4]); c.strokeStyle = col(amber, 0.9); c.lineWidth = 2;
    c.beginPath(); c.arc(orbit.x, orbit.y, 20, 0, Math.PI * 2); c.stroke(); c.restore();
    c.font = "800 34px " + F_DISPLAY; c.textAlign = "center"; c.textBaseline = "middle";
    c.fillStyle = col(mixv("#fff3cf", C.white, fl)); c.fillText("}", orbit.x, orbit.y + 1);

    // symboles orphelins en orbite
    c.font = "600 14px " + F_MONO;
    const gl = [",", ";", '"', "null", "NaN", "]", "undefined"];
    for (let k = 0; k < gl.length; k++) {
      const a = -t * 0.45 * (b.rage ? 2 : 1) + (k * Math.PI * 2) / gl.length, depth = Math.sin(a);
      c.fillStyle = col(cyan, 0.18 + 0.3 * (depth + 1) / 2);
      c.fillText(gl[k], Math.cos(a) * 215, depth * 120);
    }
  }
};
