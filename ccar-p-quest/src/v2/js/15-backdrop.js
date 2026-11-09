/* ============================================================
   Décor commun de l'arène : ciel, ville, décor propre au boss, parapet.
   Utilisé par le moteur de combat et par la page d'aperçu des boss.
   ============================================================ */
const SKIES = [
  ["#060a15", "#10182f", "#1c2647"], ["#070b18", "#121a35", "#22294f"], ["#080b1b", "#141b3a", "#282c56"],
  ["#0a0c1e", "#181c40", "#30305e"], ["#0c0d22", "#1d1e46", "#3b3364"], ["#0e0e25", "#221f4a", "#483667"],
  ["#0f0f27", "#27214d", "#563a69"], ["#11102a", "#2c2350", "#6a4068"], ["#131130", "#332655", "#8a4a62"],
  ["#15132f", "#3a2a5a", "#c0644f"]
];
/** Taille d'affichage des boss dans l'arène (multiplie leurs unités locales). */
const ARENA_SCALE = 1.15;

/**
 * Peint le décor fixe d'un étage. `c` est déjà à l'échelle du monde (1 unité = 1 unité de jeu).
 * env = { W, H, groundY, n, rnd } ; B = le boss de l'étage (peut fournir sky et backdrop).
 */
function paintBackground(c, env, B) {
  const { W, H, groundY } = env, n = clamp(env.n || 1, 1, 10), alt = (n - 1) / 9;
  const sky = (B && B.sky) || SKIES[n - 1];
  const g = c.createLinearGradient(0, 0, 0, groundY); g.addColorStop(0, sky[0]); g.addColorStop(0.7, sky[1]); g.addColorStop(1, sky[2]);
  c.fillStyle = g; c.fillRect(0, 0, W, groundY);

  // Lune (elle pâlit en montant), puis soleil levant au sommet.
  const mx = W * 0.88, my = Math.max(60, groundY - 470);
  if (n < 10) {
    const mg = c.createRadialGradient(mx, my, 10, mx, my, 120); mg.addColorStop(0, "rgba(232,236,246," + 0.18 * (1 - alt * 0.6) + ")"); mg.addColorStop(1, "rgba(232,236,246,0)");
    c.fillStyle = mg; c.fillRect(mx - 120, my - 120, 240, 240);
    c.globalAlpha = 1 - alt * 0.55; c.fillStyle = "#dfe5f3"; c.beginPath(); c.arc(mx, my, 30, 0, Math.PI * 2); c.fill();
    c.fillStyle = sky[1]; c.beginPath(); c.arc(mx + 12, my - 7, 26, 0, Math.PI * 2); c.fill(); c.globalAlpha = 1;
  } else {
    const sg = c.createRadialGradient(W * 0.5, groundY - 30, 10, W * 0.5, groundY - 30, W * 0.6); sg.addColorStop(0, "rgba(243,184,65,0.45)"); sg.addColorStop(1, "rgba(243,184,65,0)");
    c.fillStyle = sg; c.fillRect(0, 0, W, groundY);
  }

  // Ville au loin : elle s'éloigne à mesure qu'on monte.
  const rnd = seeded(42); let x = -10;
  const drop = alt * 70, maxH = 150 * (1 - alt * 0.6);
  while (x < W + 20) {
    const w = 26 + rnd() * 50, h = 30 + rnd() * maxH, top = groundY - 40 - h + drop;
    c.fillStyle = col(mixv("#0e1528", sky[2], alt * 0.35)); c.fillRect(x, top, w, h + 40);
    for (let wy = top + 8; wy < groundY - 46; wy += 12) for (let wx = x + 5; wx < x + w - 6; wx += 9) if (rnd() < 0.16) { c.fillStyle = rnd() < 0.8 ? "rgba(243,184,65," + (0.55 - alt * 0.3) + ")" : "rgba(232,236,246,0.3)"; c.fillRect(wx, wy, 3, 5); }
    x += w + 2 + rnd() * 8;
  }

  // Décor propre à l'étage (fourni par le boss).
  if (B && B.backdrop) { c.save(); try { B.backdrop(c, env); } catch (e) { /* un décor raté ne casse pas l'arène */ } c.restore(); }

  if (alt > 0.3) {
    const cr = seeded(9);
    for (let k = 0; k < 14; k++) { const cx = cr() * W, cy = groundY - 40 - cr() * 40 * alt, rw = 90 + cr() * 140; c.fillStyle = "rgba(232,236,246," + (0.05 + alt * 0.1) + ")"; c.beginPath(); c.ellipse(cx, cy, rw, 18 + cr() * 14, 0, 0, Math.PI * 2); c.fill(); }
  }

  // Parapet crénelé et dalle.
  c.fillStyle = "#1a2238"; c.fillRect(0, groundY - 34, W, 34);
  c.strokeStyle = "#2b3657"; c.lineWidth = 1.5;
  for (let mxp = -10; mxp < W + 40; mxp += 64) { c.fillStyle = "#1d2643"; c.fillRect(mxp, groundY - 58, 40, 26); c.strokeRect(mxp + 0.5, groundY - 57.5, 39, 25); }
  c.beginPath(); c.moveTo(0, groundY - 34); c.lineTo(W, groundY - 34); c.stroke();
  for (let row = 0; row < 2; row++) for (let jx = (row % 2) * 30; jx < W; jx += 60) { c.beginPath(); c.moveTo(jx, groundY - 34 + row * 17); c.lineTo(jx, groundY - 17 + row * 17); c.stroke(); }
  c.fillStyle = "#141b2f"; c.fillRect(0, groundY, W, H - groundY);
  c.strokeStyle = "#232d4b"; c.beginPath(); c.moveTo(0, groundY + 0.5); c.lineTo(W, groundY + 0.5); c.stroke();
  for (let jx = 20; jx < W; jx += 80) { c.beginPath(); c.moveTo(jx, groundY); c.lineTo(jx - 30, H); c.stroke(); }
  if (env.n) { c.fillStyle = "rgba(232,236,246,0.08)"; c.font = "800 120px " + F_DISPLAY; c.textAlign = "left"; c.textBaseline = "alphabetic"; c.fillText(pad(env.n), 18, groundY - 66); }
}
