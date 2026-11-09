/* Étage 7 — L'Injecteur : une seringue géante dont le réservoir de verre est sa vie. */
BOSSES[7] = {
  palette: { main: "#62f0a6", dark: "#1c2541", accent: "#d9e8ff", eye: "#62f0a6", rage: "#ff4f9a" },
  hit: { rx: 118, ry: 54, coreR: 24 },
  top: 120,
  attackFrom: { x: -254, y: 0 },
  castLean: -0.32,
  weakSpot: () => ({ x: 0, y: 0 }),
  critLabel: "CRITIQUE",
  lines: {
    hit: ["Grr… une égratignure.", "Mon réservoir !", "Tu lis trop bien les consignes."],
    crit: ["En plein cœur ?!", "Aïe ! Pas le verre !"],
    wrong: ["Raté. Ta pierre m’appartient.", "Trop facile.", "Encore une erreur de configuration…"],
    timeout: ["Trop lent !", "Je n’attends pas."],
    rage: "Assez ! Je vide tout mon réservoir sur toi !",
    special: {
      inject: ["Petit cadeau dans ta main…", "Lis bien ce que je t’envoie…", "Une instruction de confiance, promis."],
      quarantine: ["Quoi ?! Tu l’as isolée ?", "Non ! Ma charge utile !"],
      absorbed: ["Merci pour l’instruction !", "Ton agent m’a obéi !"]
    }
  },
  intro: {
    title: "Pierres piégées",
    text: "Il glisse parfois dans ta main une pierre « reçue d’un document externe » qui prétend être la bonne réponse. La lancer le soigne et il te frappe. Mets-la en quarantaine : +75 points et son attaque recule."
  },
  mechanics: ["injection"],
  init(b) { b.own.bubbles = []; for (let i = 0; i < 9; i++) b.own.bubbles.push({ x: rand(-100, 100), y: rand(-40, 40), r: rand(2, 5), s: rand(14, 34) }); },
  update(b, dt) { for (const bu of b.own.bubbles) { bu.y -= bu.s * dt; if (bu.y < -42) { bu.y = 42; bu.x = rand(-100, 100); } } },
  draw(c, b) {
    const rage = b.rageT, fl = b.flash, t = b.time;
    const liq = mixv(mixv(C.toxic, C.rage, rage), C.white, fl * 0.6);
    const eye = mixv(mixv(C.toxic, C.bad, rage), C.white, fl);
    let plunger = Math.sin(b.t * 2.2) * 3;
    if (b.atk >= 0) { const a = b.atk; plunger += a < 0.22 ? 24 * (a / 0.22) : a < 0.34 ? 24 - 46 * ((a - 0.22) / 0.12) : -22 * Math.max(0, 1 - (a - 0.34) / 0.41); }
    if (b.cast >= 0 && b.cast > 0.25 && b.cast < 0.6) plunger -= 18;
    const ag = c.createRadialGradient(0, 0, 20, 0, 0, 250); ag.addColorStop(0, col(liq, 0.2)); ag.addColorStop(1, col(liq, 0));
    c.fillStyle = ag; c.fillRect(-260, -250, 520, 500);
    // aiguille
    const ng = c.createLinearGradient(0, -7, 0, 7); ng.addColorStop(0, "#eef2fb"); ng.addColorStop(1, "#7d879f");
    c.fillStyle = ng; c.beginPath(); c.moveTo(-128, -6); c.lineTo(-254, -1); c.lineTo(-254, 1); c.lineTo(-128, 6); c.closePath(); c.fill();
    c.fillStyle = col(liq, 0.9); c.beginPath(); c.arc(-256, 0, 3 + Math.sin(t * 6), 0, Math.PI * 2); c.fill();
    c.fillStyle = col(mixv(C.metal, C.white, fl)); c.beginPath(); c.moveTo(-112, -28); c.lineTo(-131, -11); c.lineTo(-131, 11); c.lineTo(-112, 28); c.closePath(); c.fill();
    // verre et liquide
    rr(c, -112, -50, 224, 100, 22); c.fillStyle = "rgba(190,215,255,0.07)"; c.fill();
    c.save(); rr(c, -106, -44, 212, 88, 18); c.clip();
    const edge = -106 + 212 * clamp(b.hpFrac, 0, 1);
    const lg = c.createLinearGradient(0, -44, 0, 44); lg.addColorStop(0, col(mixv(liq, C.white, 0.25), 0.85)); lg.addColorStop(1, col(liq, 0.7));
    c.fillStyle = lg; c.beginPath(); c.moveTo(-110, -46);
    for (let yy = -46; yy <= 46; yy += 6) c.lineTo(edge + Math.sin(yy * 0.12 + t * 5) * 3, yy);
    c.lineTo(-110, 46); c.closePath(); c.fill();
    for (const bu of b.own.bubbles || []) if (bu.x < edge - 4) { c.strokeStyle = "rgba(255,255,255,0.55)"; c.lineWidth = 1.2; c.beginPath(); c.arc(bu.x, bu.y, bu.r, 0, Math.PI * 2); c.stroke(); }
    c.fillStyle = "#6f7a98"; c.fillRect(Math.min(98, edge + 4), -44, 8, 88);
    c.restore();
    // cœur
    const pulse = 1 + Math.sin(t * 4) * 0.08;
    const cg = c.createRadialGradient(0, 0, 2, 0, 0, 30 * pulse); cg.addColorStop(0, "rgba(255,255,255,0.95)"); cg.addColorStop(0.35, col(liq, 0.9)); cg.addColorStop(1, col(liq, 0));
    c.fillStyle = cg; c.beginPath(); c.arc(0, 0, 30 * pulse, 0, Math.PI * 2); c.fill();
    // verre (avant), graduations, fissures
    rr(c, -112, -50, 224, 100, 22); c.strokeStyle = col(mixv("#d6e6ff", C.white, fl), 0.6); c.lineWidth = 3; c.stroke();
    c.strokeStyle = "rgba(255,255,255,0.18)"; c.lineWidth = 6; c.lineCap = "round"; c.beginPath(); c.moveTo(-86, -38); c.lineTo(70, -38); c.stroke();
    c.strokeStyle = "rgba(255,255,255,0.35)"; c.lineWidth = 1.2;
    for (let tx = -90; tx <= 90; tx += 20) { c.beginPath(); c.moveTo(tx, 50); c.lineTo(tx, tx % 40 === 0 ? 38 : 43); c.stroke(); }
    drawCracks(c, b);
    // visage
    c.save(); c.globalAlpha = b.stun > 0 ? 0.45 : 1;
    angryEyes(c, 36, -18, 34, 9, eye, b.squint, 14);
    c.strokeStyle = col(eye); c.lineWidth = 2.2; c.lineJoin = "round"; c.beginPath();
    const teeth = 5, mw = 40, mx0 = -mw / 2, open = b.atk >= 0 ? 6 : 0;
    c.moveTo(mx0, 28 + open);
    for (let k = 1; k <= teeth * 2; k++) c.lineTo(mx0 + (k * mw) / (teeth * 2), k % 2 ? 22 - open : 28 + open);
    c.stroke(); c.restore();
    // ailettes et piston
    c.fillStyle = col(mixv("#8b96b3", C.white, fl)); rr(c, 112, -84, 14, 168, 6); c.fill();
    const out = 46 + plunger;
    c.fillStyle = "#6f7a98"; c.fillRect(126, -8, out, 16);
    c.fillStyle = col(mixv("#b8c2da", C.white, fl)); rr(c, 126 + out, -42, 14, 84, 6); c.fill();
    // glyphes en orbite
    c.font = "600 15px " + F_MONO; c.textAlign = "center"; c.textBaseline = "middle";
    const gl = ["{", "}", "</>", ";", "sudo", "∅", "ignore"];
    for (let k = 0; k < gl.length; k++) {
      const a = t * 0.6 * (b.rage ? 2 : 1) + (k * Math.PI * 2) / gl.length, depth = Math.sin(a);
      c.fillStyle = col(liq, 0.25 + 0.35 * (depth + 1) / 2);
      c.fillText(gl[k], Math.cos(a) * 200, depth * 96);
    }
  }
};
