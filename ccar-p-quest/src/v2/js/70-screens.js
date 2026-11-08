/* ============================================================
   Écrans hors combat : la tour, la page d'étage, la salle de révision, l'ascenseur.
   ============================================================ */

/* ---------- Portraits animés des boss (petits canvas) ---------- */
const Thumbs = (() => {
  let list = [], raf = 0, last = 0, skip = false;
  function scan() {
    list = [...document.querySelectorAll("canvas[data-boss]")].map((cv) => {
      const key = cv.dataset.boss, B = BOSSES[key];
      if (!B) return null;
      const b = { t: rand(0, 5), time: rand(0, 5), hpFrac: 1, flash: 0, squint: 0, rage: false, rageT: 0, atk: -1, cast: -1, stun: 0, aiming: false, cracks: [], mech: { heads: { count: 2 }, shield: { up: false, streak: 0 }, fog: { shown: 0.3 }, incidents: { hook: false } }, phase: 0, own: {} };
      if (B.init) try { B.init(b); } catch (e) { /* portrait sans état propre */ }
      return { cv, B, b, mode: cv.dataset.mode || "idle", fit: Number(cv.dataset.fit) || 1 };
    }).filter(Boolean);
    size();
    for (const x of list) draw(x, 0);
    if (!raf && list.length && !reduceMotion) { last = performance.now(); raf = requestAnimationFrame(loop); }
  }
  function size() {
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    for (const x of list) { const r = x.cv.getBoundingClientRect(); x.w = r.width; x.h = r.height; x.dpr = dpr; x.cv.width = Math.max(1, Math.round(r.width * dpr)); x.cv.height = Math.max(1, Math.round(r.height * dpr)); }
  }
  function draw(x, dt) {
    const c = x.cv.getContext("2d"), b = x.b;
    b.t += dt; b.time += dt;
    if (x.mode === "won") { b.stun = 1; b.hpFrac = 0.1; }
    if (x.B.update) try { x.B.update(b, dt); } catch (e) { /* ignoré */ }
    c.setTransform(x.dpr, 0, 0, x.dpr, 0, 0); c.clearRect(0, 0, x.w, x.h);
    const s = Math.min(x.w / 560, x.h / 440) * x.fit;
    c.save(); c.translate(x.w / 2, x.h / 2 + (x.B.ground ? 30 * s : 0) + (reduceMotion ? 0 : Math.sin(b.t * 1.5) * 3)); c.scale(s, s);
    try { x.B.draw(c, b); } catch (e) { /* ignoré */ }
    c.restore();
    if (x.mode === "locked") {
      c.save(); c.globalCompositeOperation = "source-atop"; c.fillStyle = "rgba(58,70,108,0.95)"; c.fillRect(0, 0, x.w, x.h); c.restore();
      c.fillStyle = "rgba(232,236,246,0.85)"; c.font = "800 " + Math.round(x.h * 0.38) + "px " + F_DISPLAY; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText("?", x.w / 2, x.h / 2);
    }
  }
  function loop(now) {
    list = list.filter((x) => x.cv.isConnected);
    if (!list.length) { raf = 0; return; }
    const dt = Math.min(0.08, (now - last) / 1000);
    skip = !skip;
    if (!skip || reduceMotion) {
      last = now;
      for (const x of list) { const r = x.cv.getBoundingClientRect(); if (r.bottom < 0 || r.top > window.innerHeight) continue; draw(x, reduceMotion ? 0 : dt); }
    }
    raf = reduceMotion ? 0 : requestAnimationFrame(loop);
  }
  window.addEventListener("resize", () => { size(); if (reduceMotion) list.forEach((x) => draw(x, 0)); });
  return { scan };
})();
const thumb = (n, w, h, mode, fit) => '<canvas class="thumb" data-boss="' + n + '" data-mode="' + (mode || "idle") + '"' + (fit ? ' data-fit="' + fit + '"' : "") + ' width="' + w + '" height="' + h + '" style="width:' + w + "px;height:" + h + 'px" aria-hidden="true"></canvas>';
function starsHTML(n, cls) { let h = '<span class="' + (cls || "stars") + '" aria-label="' + plural(n, "étoile") + ' sur 3">'; for (let i = 0; i < 3; i++) h += '<span class="' + (i < n ? "on" : "") + '">★</span>'; return h + "</span>"; }
function domainMix(level) {
  const c = {}; level.questions.forEach((q) => { c[q.domain] = (c[q.domain] || 0) + 1; });
  return Object.keys(c).sort().map((d) => '<span class="chip" title="' + esc(DOMAINS[d].name) + '">' + d + " " + esc(DOMAINS[d].short) + " ×" + c[d] + "</span>").join("");
}

/* ---------- Barre du haut et pied de page ---------- */
function renderNav() {
  const won = LEVELS.filter((l) => L(l.id).won).length;
  const p = $("nav-progress"); if (p) p.textContent = won + " / " + LEVELS.length + " étages";
  const r = $("nav-review"); if (r) { const n = reviewIds().length; r.textContent = n; r.className = "count" + (n ? " has" : ""); }
  const u = $("unlock-btn"); if (u) u.textContent = state.unlockAll ? "Revenir à la progression étage par étage" : "Débloquer tous les étages";
  const s = $("nav-sound"); if (s) { s.setAttribute("aria-pressed", String(Sound.on)); s.title = Sound.on ? "Couper le son" : "Activer le son"; }
}
function renderConfirm() {
  const slot = $("confirm-slot"); if (!slot) return;
  if (ui.confirm === "reset") slot.innerHTML = '<div class="confirm"><span>Effacer toute ta progression (étages, statistiques, révisions) ?</span><button class="btn" type="button" data-action="do-reset">Oui, tout effacer</button><button class="link-btn" type="button" data-action="cancel-confirm">Annuler</button></div>';
  else if (ui.confirm === "unlock") slot.innerHTML = '<div class="confirm"><span>Débloquer tous les étages et tous les boss, sans passer par l’échauffement ?</span><button class="btn" type="button" data-action="do-unlock">Débloquer</button><button class="link-btn" type="button" data-action="cancel-confirm">Annuler</button></div>';
  else slot.innerHTML = "";
}

/* ---------- La tour ---------- */
function renderHome() {
  const view = $("view");
  if (!LEVELS.length) { view.innerHTML = '<section class="page wrap"><h1>Contenu manquant</h1><p class="lede">Lance <code>node scripts/build.mjs</code> pour générer la page.</p></section>'; return; }
  const cur = currentFloor(), allWon = LEVELS.every((l) => L(l.id).won), curLevel = cur ? byId(cur) : null;
  const floors = LEVELS.slice().reverse().map((l) => {
    const s = L(l.id), open = isUnlocked(l.id), best = s.best || 0, here = l.id === cur;
    let status;
    if (!open) status = '<span class="pill">Verrouillé</span>';
    else if (s.won) status = starsHTML(s.stars || 1);
    else if (bossReady(l.id)) status = '<span class="pill ready">Boss prêt</span>';
    else status = '<span class="pill train">Entraînement</span>';
    let win = ""; for (let i = 0; i < 10; i++) win += '<i class="win' + (i < best ? " lit" : "") + '"></i>';
    const inner = '<div class="floor-num"><span class="eyebrow">Étage</span><b>' + pad(l.id) + "</b></div>" +
      '<div class="floor-thumb">' + thumb(l.id, 92, 72, !open ? "locked" : s.won ? "won" : "idle") + "</div>" +
      '<div class="floor-body"><h3>' + esc(l.title) + '</h3><div class="floor-meta"><span>' + esc(l.theme) + "</span><span>Boss : " + (open ? esc(l.boss.name) : "???") + "</span></div>" + (here ? '<span class="here">Tu es ici</span>' : "") + "</div>" +
      '<div class="floor-side">' + status + '<div class="windows" title="Meilleur score : ' + best + '/10">' + win + "</div>" + (s.bestScore ? '<span class="mono floor-score">' + s.bestScore + " pts</span>" : "") + "</div>";
    const cls = "floor" + (!open ? " is-locked" : "") + (here ? " is-current" : "") + (s.won ? " is-won" : "");
    return "<li>" + (open ? '<a class="' + cls + '" href="#etage-' + l.id + '">' + inner + "</a>" : '<div class="' + cls + '" aria-disabled="true">' + inner + "</div>") + "</li>";
  }).join("");

  let answered = 0, correct = 0;
  const domRows = Object.keys(DOMAINS).map((k) => {
    const d = DOMAINS[k], s = state.domains[k] || { seen: 0, ok: 0 };
    answered += s.seen; correct += s.ok;
    const pct = s.seen ? s.ok / s.seen : null, cls = pct == null ? "" : pct >= PASS ? "good" : pct >= 0.5 ? "mid" : "low";
    return '<div class="dom"><div class="dom-top"><span title="' + esc(d.name) + '">' + k + " " + esc(d.short) + ' <span class="mono">' + d.weight + ' %</span></span><span class="mono">' + (pct == null ? "pas encore vu" : s.ok + "/" + s.seen + " · " + Math.round(pct * 100) + " %") + "</span></div>" +
      '<div class="bar"><i class="' + cls + '" style="width:' + (pct == null ? 0 : Math.round(pct * 100)) + '%"></i><span class="pass" title="Seuil de réussite 72 %"></span></div></div>';
  }).join("");
  const won = LEVELS.filter((l) => L(l.id).won).length, nReview = reviewIds().length;
  const totalScore = LEVELS.reduce((s, l) => s + (L(l.id).bestScore || 0), 0);
  const cta = curLevel
    ? '<a class="btn btn-primary btn-big" href="#etage-' + curLevel.id + '">' + (won ? "Continuer" : "Commencer") + " · Étage " + pad(curLevel.id) + " : " + esc(curLevel.boss.name) + " →</a>"
    : '<a class="btn btn-primary btn-big" href="#revisions">Consolider en salle de révision →</a>';

  view.innerHTML =
    '<section class="home wrap">' +
      '<div class="home-main">' +
        '<div class="hero"><p class="eyebrow">Claude Certified Architect – Professional · CCAR-P</p>' +
        "<h1>Dix étages,<br>dix boss,<br><em>un examen.</em></h1>" +
        '<p class="lede">À chaque étage : des fiches à retourner, un échauffement, puis un boss à abattre au lance-pierre. Dix questions au format de l’examen, trois vies, une mécanique différente par boss.</p>' +
        '<div class="btn-row">' + cta + (nReview ? '<a class="btn" href="#revisions">Salle de révision · ' + nReview + "</a>" : "") + "</div></div>" +
        '<div class="spire' + (allWon ? " lit" : "") + '" aria-hidden="true"><svg viewBox="0 0 80 54"><line class="mast" x1="40" y1="10" x2="40" y2="54"/><line class="mast" x1="28" y1="54" x2="40" y2="30"/><line class="mast" x1="52" y1="54" x2="40" y2="30"/><circle class="beacon" cx="40" cy="8" r="5"/></svg></div>' +
        '<ol class="tower" aria-label="Les 10 étages, du sommet au rez-de-chaussée">' + floors + "</ol>" +
        '<div class="ground"><span class="eyebrow">Rez-de-chaussée · départ</span></div>' +
      "</div>" +
      '<aside class="dossier" aria-label="Dossier d’examen"><h2>Dossier d’examen</h2>' +
        '<div class="kpis"><div class="kpi"><b>' + won + '<small>/' + LEVELS.length + '</small></b><span>boss vaincus</span></div><div class="kpi"><b>' + (answered ? Math.round(correct / answered * 100) + "%" : "—") + '</b><span>de réussite</span></div><div class="kpi"><b>' + totalScore + "</b><span>points records</span></div></div>" +
        '<div class="domains"><p class="eyebrow">Maîtrise par domaine · poids à l’examen</p>' + domRows + '<p class="note">Le trait blanc marque 72 %, l’équivalent du score de réussite (720/1000).</p></div>' +
        '<div><p class="eyebrow" style="margin-bottom:10px">L’examen réel</p><dl class="facts"><dt>63</dt><dd>questions indépendantes, réponse unique ou multiple</dd><dt>120 min</dt><dd>soit environ 1 min 54 s par question</dd><dt>720</dt><dd>sur 1000 pour réussir</dd><dt>7</dt><dd>domaines, de 7 % à 19 % chacun</dd></dl></div>' +
        '<p class="note">La barre d’attaque des boss est progressive : ' + fmtMS(secondsFor(1)) + " par question à l’étage 1, " + fmtMS(secondsFor(10)) + " au sommet, le rythme de l’examen.</p>" +
      "</aside>" +
    "</section>";
  Thumbs.scan();
}

/* ---------- Page d'étage ---------- */
function renderSteps(level) {
  const n = level.id, s = L(n), w = ui.warm[n];
  const known = (s.known || []).length;
  const el = document.getElementById("steps"); if (!el) return;
  el.innerHTML =
    stepBtn(n, "cards", "1", "Fiches", known + "/" + level.cards.length + " maîtrisées", false) +
    stepBtn(n, "warmup", "2", "Échauffement", s.warmupDone ? "fait · " + (s.warmupBest || 0) + "/5 pigeons" : w && w.stage === "pigeons" ? "pigeons" : "relier + pigeons", false) +
    stepBtn(n, "boss", "3", "Boss", bossReady(n) ? (s.won ? "vaincu · " + plural(s.stars || 1, "étoile") : "10 questions") : "après l’échauffement", !bossReady(n));
}
function stepBtn(n, key, num, label, sub, disabled) {
  return '<button class="step" role="tab" type="button" data-action="tab" data-n="' + n + '" data-tab="' + key + '" aria-selected="' + (ui.tab[n] === key) + '"' + (disabled ? " disabled" : "") + '><span class="mono">' + num + "</span>" + label + ' <span class="mono">' + sub + "</span></button>";
}
function renderLevel(n) {
  const view = $("view"), level = byId(n);
  if (!level) { go("tour"); return; }
  if (!isUnlocked(n)) {
    view.innerHTML = '<section class="page wrap"><a class="back" href="#tour">← La tour</a><h1>Étage ' + pad(n) + ' verrouillé</h1><p class="lede">Bats d’abord le boss de l’étage ' + pad(n - 1) + '.</p><div class="btn-row"><a class="btn btn-primary" href="#etage-' + (n - 1) + '">Aller à l’étage ' + pad(n - 1) + "</a></div></section>";
    return;
  }
  const s = L(n), B = BOSSES[n] || {};
  let tab = ui.tab[n] || (bossReady(n) ? "boss" : s.cardsSeen ? "warmup" : "cards");
  if (tab === "boss" && !bossReady(n)) tab = "warmup";
  ui.tab[n] = tab;
  if (tab === "cards" && !s.cardsSeen) { lv(n).cardsSeen = true; save(); }
  const body = tab === "cards" ? cardsHTML(level) : tab === "warmup" ? warmupHTML(level) : bossTabHTML(level);
  view.innerHTML =
    '<section class="level wrap">' +
      '<a class="back" href="#tour">← La tour</a>' +
      '<div class="level-head"><div class="level-portrait">' + thumb(n, 200, 160, s.won ? "won" : "idle", 1.15) + "</div>" +
        '<div><p class="eyebrow">Étage ' + pad(n) + " · " + esc(level.theme) + "</p><h1>" + esc(level.title) + '</h1><p class="lede">' + fmt(level.intro) + '</p><div class="chips">' + domainMix(level) + "</div></div></div>" +
      '<div class="steps" role="tablist" aria-label="Étapes de l’étage" id="steps"></div>' +
      '<div role="tabpanel" id="tabpanel" data-tab="' + tab + '">' + body + "</div>" +
    "</section>";
  renderSteps(level);
  Thumbs.scan();
}
function bossTabHTML(level) {
  const n = level.id, s = L(n), B = BOSSES[n] || {};
  return '<div class="boss-card"><div class="boss-portrait">' + thumb(n, 320, 250, s.won ? "won" : "idle", 1.1) + "</div>" +
    '<div><p class="eyebrow">Boss de l’étage ' + pad(n) + "</p><h2>" + esc(level.boss.name) + '</h2><p class="lede" style="margin-top:6px">' + esc(level.boss.epithet) + '</p><p class="boss-quote">« ' + esc(unquote(level.boss.taunt)) + " »</p>" +
    (B.intro ? '<div class="mech-card"><b>Sa mécanique · ' + esc(B.intro.title) + "</b><span>" + esc(B.intro.text) + "</span></div>" : "") +
    '<ul class="rules"><li><span>10</span><span>questions d’examen en anglais, dans un ordre aléatoire.</span></li><li><span>♥ 3</span><span>vies : chaque erreur en coûte une, la troisième fait gagner le boss.</span></li><li><span>' + fmtMS(secondsFor(n)) + "</span><span>par question avant qu’il frappe (barre d’attaque).</span></li><li><span>2</span><span>pierres à charger quand la question dit « Select TWO ». Tout ou rien.</span></li></ul>" +
    (s.attempts ? '<p class="note" style="margin-bottom:14px">Meilleur score : ' + (s.best || 0) + "/10" + (s.bestScore ? " · record " + s.bestScore + " points" : "") + " · " + plural(s.attempts, "tentative") + "</p>" : "") +
    '<div class="btn-row"><a class="btn btn-primary btn-big" href="#combat-' + n + '">Combattre →</a>' + (s.won ? '<button class="btn" type="button" data-action="start-free" data-n="' + n + '">Mode libre, sans vies</button>' : "") + "</div></div></div>";
}

/* ---------- Salle de révision ---------- */
function renderReview() {
  const ids = reviewIds().sort((a, b) => (state.review[b].misses || 0) - (state.review[a].misses || 0));
  let body;
  if (!ids.length) body = '<div class="empty">' + thumb("dummy", 140, 150, "idle") + '<div><h2 class="section-title">Aucune erreur en attente</h2><p class="lede">Chaque question ratée face à un boss arrive ici. Tu la retravailles au lance-pierre contre le mannequin, sans vies ni chrono, jusqu’à la réussir.</p><a class="btn" href="#tour">Retour à la tour</a></div></div>';
  else body = '<div class="review-head">' + thumb("dummy", 140, 150, "idle") + '<div><p class="lede">' + plural(ids.length, "question") + " à retravailler, des plus ratées aux moins ratées. Une bonne réponse retire la question de la pile.</p>" +
    '<div class="btn-row"><button class="btn btn-primary btn-big" type="button" data-action="start-review">Entrer dans la salle (' + ids.length + ")</button></div></div></div>" +
    '<ul class="misslist">' + ids.map((id) => { const q = QINDEX[id].q; return '<li><span class="mono">Étage ' + pad(QINDEX[id].level.id) + " · " + q.domain + " " + esc(DOMAINS[q.domain].short) + " · ratée " + state.review[id].misses + ' fois</span><span lang="en">' + fmt(q.stem.length > 200 ? q.stem.slice(0, 200) + "…" : q.stem) + "</span></li>"; }).join("") + "</ul>";
  $("view").innerHTML = '<section class="page wrap"><a class="back" href="#tour">← La tour</a><p class="eyebrow">Salle de révision</p><h1>Tes erreurs à retravailler</h1>' + body + "</section>";
  Thumbs.scan();
}

/* ---------- Ascenseur entre deux étages ---------- */
function elevator(from, to, done) {
  if (reduceMotion) { done(); return; }
  const el = document.createElement("div");
  el.className = "elevator";
  el.innerHTML = '<div class="elev-doors"><i></i><i></i></div><div class="elev-panel"><span class="eyebrow">Ascenseur</span><b id="elev-floor">' + pad(from) + '</b><span class="elev-arrow">▲</span></div>';
  document.body.appendChild(el);
  Sound.play("whoosh");
  requestAnimationFrame(() => el.classList.add("closing"));
  setTimeout(() => { const f = el.querySelector("#elev-floor"); f.textContent = pad(to); f.classList.add("tick"); Sound.play("ding"); }, 750);
  setTimeout(() => { done(); el.classList.add("opening"); }, 1300);
  setTimeout(() => el.remove(), 2000);
}
