/* Mannequin d'entraînement (révisions et mode libre) : pas d'attaque, pas de chrono. */
BOSSES.dummy = {
  palette: { main: "#c9a26a", dark: "#5a3f2e", accent: "#f3b841", eye: "#2b3657", rage: "#c9a26a" },
  hit: { rx: 60, ry: 110, coreR: 20 },
  top: 150,
  attackFrom: { x: 0, y: 0 },
  weakSpot: () => ({ x: 0, y: -20 }),
  critLabel: "EN PLEIN CENTRE",
  lines: { hit: ["Bien visé.", "Encore !"], crit: ["Dans le mille !"], wrong: ["Pas cette fois."], timeout: [], rage: "" },
  intro: { title: "Salle d’entraînement", text: "Pas de vies ni de chrono : prends le temps de lire chaque explication." },
  mechanics: [],
  draw(c, b) {
    const fl = b.flash, sway = Math.sin(b.t * 1.4) * 0.03;
    c.rotate(sway);
    c.fillStyle = "#5a3f2e"; c.fillRect(-6, 60, 12, 140);
    c.fillStyle = col(mixv("#c9a26a", C.white, fl)); rr(c, -52, -100, 104, 170, 40); c.fill();
    c.strokeStyle = "#8a6a40"; c.lineWidth = 2;
    for (let y = -80; y < 60; y += 16) { c.beginPath(); c.moveTo(-46, y); c.lineTo(46, y + 4); c.stroke(); }
    c.fillStyle = col(mixv("#d9b77e", C.white, fl)); c.beginPath(); c.arc(0, -126, 30, 0, Math.PI * 2); c.fill();
    c.fillStyle = "#2b3657"; c.fillRect(-12, -132, 7, 3); c.fillRect(5, -132, 7, 3); c.fillRect(-8, -114, 16, 3);
    c.strokeStyle = "#5a3f2e"; c.lineWidth = 8; c.lineCap = "round"; c.beginPath(); c.moveTo(-50, -60); c.lineTo(-96, -40); c.moveTo(50, -60); c.lineTo(96, -40); c.stroke();
    for (const [r, k] of [[46, 0], [32, 1], [18, 0], [7, 1]]) { c.fillStyle = k ? C.bad : "#f2ead7"; c.beginPath(); c.arc(0, -20, r, 0, Math.PI * 2); c.fill(); }
    drawCracks(c, b, "rgba(90,63,46,0.8)", 2);
  }
};
