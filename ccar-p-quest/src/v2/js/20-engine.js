/* ============================================================
   Moteur de combat : arène canvas, lance-pierre, boss, questions.
   Un seul combat à la fois : Arena.mount(opts) / Arena.unmount().
   ============================================================ */
const SKIES = [
  ["#060a15", "#10182f", "#1c2647"], ["#070b18", "#121a35", "#22294f"], ["#080b1b", "#141b3a", "#282c56"],
  ["#0a0c1e", "#181c40", "#30305e"], ["#0c0d22", "#1d1e46", "#3b3364"], ["#0e0e25", "#221f4a", "#483667"],
  ["#0f0f27", "#27214d", "#563a69"], ["#11102a", "#2c2350", "#6a4068"], ["#131130", "#332655", "#8a4a62"],
  ["#15132f", "#3a2a5a", "#c0644f"]
];

const Arena = (() => {
  let F = null, raf = 0, ro = null, lastFrame = 0;

  /* ---------------- Montage ---------------- */
  function mount(opts) {
    unmount();
    const practice = opts.mode === "practice";
    const level = practice ? null : byId(opts.n);
    const B = practice ? BOSSES.dummy : BOSSES[opts.n];
    if (!B || (!practice && !level)) return false;
    const questions = practice ? opts.queue.map((id) => QINDEX[id].q) : shuffle(level.questions);
    F = {
      mode: opts.mode, n: practice ? (opts.n || 0) : opts.n, level, B, opts, practiceKind: opts.practiceKind || null,
      questions, i: 0, hearts: HEARTS, prevHearts: HEARTS, hp: MAX_HP, score: 0, scoreShown: 0, combo: 0, bestCombo: 0, crits: 0, results: [], t0: 0,
      sel: [], perm: [], loaded: null, arriveAt: 0, bar: 0, barMax: practice ? Infinity : secondsFor(opts.n), warnT: 0, paused: false,
      tutDone: !!state.seenTutorial, timeouts: 0, phase: "intro", phaseIdx: 0, mods: [], bonus: 0,
      W: 1000, H: 600, scale: 1, dpr: 1, groundY: 530, bs: 1, time: 0, hitStop: 0, timeScale: 1, shakeMag: 0, hurtFlash: 0, bubble: null, tickStep: 0,
      player: { x: 140, knock: 0, dy: 0, hurt: 0, blink: 0, blinkT: 2, mood: "idle" },
      b: { x0: 700, y0: 230, x: 700, y: 230, t: 0, time: 0, rot: 0, knock: 0, flash: 0, squint: 0, rage: false, rageT: 0, hpFrac: 1, atk: -1, atkFired: false, atkCb: null, cast: -1, lean: 0, stun: 0, aiming: false, cracks: [], dead: false, gone: false, mech: {}, phase: 0, own: {} },
      proj: null, drag: null, pull: { x: 0, y: 0 }, spring: { x: 0, y: 0, vx: 0, vy: 0 },
      particles: [], texts: [], darts: [], timers: [], stars: [], debris: [], els: {}
    };
    document.body.classList.add("in-fight");
    $("view").innerHTML = fightHTML();
    const els = F.els;
    ["stage", "stage-wrap", "arena-col", "boss-name", "phase-tag", "hp-num", "hp-bar", "hp-chip", "hp-fill", "combo", "score", "hearts", "sound-btn", "pause-btn", "quit-btn",
     "arena-actions", "attack", "attack-fill", "attack-exam", "attack-zone", "attack-time", "banner", "toast", "hint", "pause-veil", "quit-veil",
     "q-count", "q-domain", "q-level", "dots", "q-stem", "lesson", "pick-hint", "stones", "actions", "auto-btn", "feedback"].forEach((id) => { els[id] = $(id); });
    els.ctx = els.stage.getContext("2d");
    els.bg = document.createElement("canvas");
    if (B.init) B.init(F.b);
    setMods(B.mechanics || []);
    bindEvents();
    ro = window.ResizeObserver ? new ResizeObserver(resize) : null;
    if (ro) ro.observe(els["stage-wrap"]); else window.addEventListener("resize", resize);
    resize();
    els["boss-name"].textContent = practice ? (opts.title || "Entraînement") : level.boss.name;
    if (!practice) els["attack-exam"].style.left = clamp(EXAM_S / F.barMax, 0, 1) * 100 + "%";
    els["sound-btn"].setAttribute("aria-pressed", String(Sound.on));
    F.perm = F.questions[0].options.map((_, i) => i);
    renderQuestion(); renderHUD(true);
    lastFrame = performance.now();
    raf = requestAnimationFrame(frame);
    if (opts.resume) resumeFrom(opts.resume);
    else if (practice) start();
    else showIntro();
    return true;
  }
  function unmount() {
    if (!F) return;
    cancelAnimationFrame(raf); raf = 0;
    if (ro) ro.disconnect(); else window.removeEventListener("resize", resize);
    ro = null;
    document.querySelectorAll(".fly").forEach((d) => d.remove());
    document.body.classList.remove("in-fight");
    hideOverlay();
    F = null;
  }
  function fightHTML() {
    const practice = F.mode === "practice";
    return '<section class="fight' + (practice ? " practice" : "") + '" id="fight">' +
      '<div class="arena-col" id="arena-col"><header class="hud">' +
        '<button class="icon-btn" type="button" id="quit-btn" aria-label="Quitter le combat"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3L5 8l5 5" stroke="currentColor" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></button>' +
        '<div class="hud-boss"><div class="hud-name"><span class="boss-name" id="boss-name"></span><span class="phase-tag" id="phase-tag" hidden></span><span class="hp-num" id="hp-num"></span></div>' +
        '<div class="hp" id="hp-bar" role="img" aria-label="Vie du boss"><div class="hp-chip" id="hp-chip"></div><div class="hp-fill" id="hp-fill"></div><i class="hp-mid"></i></div></div>' +
        '<div class="hud-right"><span class="combo" id="combo" hidden></span><div class="score"><span>Score</span><b id="score">0</b></div><div class="hearts" id="hearts" role="img"></div>' +
        '<button class="icon-btn optional" type="button" id="sound-btn" aria-pressed="true" aria-label="Son"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2 6h3l4-3v10L5 10H2z" fill="currentColor"/><path d="M11 5.5c1 .8 1 4.2 0 5M12.8 3.8c2 1.8 2 6.6 0 8.4" stroke="currentColor" fill="none" stroke-width="1.4" stroke-linecap="round"/></svg></button>' +
        '<button class="icon-btn" type="button" id="pause-btn" aria-label="Pause"><svg viewBox="0 0 16 16" aria-hidden="true"><rect x="3.5" y="3" width="3" height="10" rx="1" fill="currentColor"/><rect x="9.5" y="3" width="3" height="10" rx="1" fill="currentColor"/></svg></button></div>' +
      '</header><div class="stage" id="stage-wrap">' +
        '<canvas id="stage" aria-label="Arène : ton architecte et son lance-pierre face au boss. Charge une réponse, tire vers l’arrière puis relâche."></canvas>' +
        '<div class="arena-actions" id="arena-actions"></div>' +
        '<div class="attack" id="attack"><div class="attack-meta"><span>Attaque du boss</span><span>dans <b id="attack-time">—</b></span></div><div class="attack-track"><div class="attack-zone" id="attack-zone" hidden></div><div class="attack-fill" id="attack-fill"></div><div class="attack-exam" id="attack-exam" title="Rythme de l’examen : 1 min 54 par question"></div></div></div>' +
        '<div class="banner" id="banner"></div><div class="toast" id="toast"></div><div class="hint" id="hint" hidden></div>' +
        '<div class="pause-veil" id="pause-veil" hidden><b>Pause</b><span>Touche l’arène pour reprendre</span></div>' +
        '<div class="quit-veil" id="quit-veil" hidden><p>Quitter ce combat ?' + (practice ? "" : " La tentative compte.") + '</p><div class="btn-row"><button class="btn" type="button" data-quit="yes">Quitter</button><button class="btn btn-primary" type="button" data-quit="no">Continuer</button></div></div>' +
      '</div></div>' +
      '<section class="panel" id="panel" aria-live="polite">' +
        '<div class="qmeta"><span id="q-count"></span><span class="chip" id="q-domain"></span><span id="q-level"></span><span class="dots" id="dots"></span></div>' +
        '<p class="stem" id="q-stem" lang="en"></p>' +
        '<div class="lesson" id="lesson" hidden></div>' +
        '<p class="pick-hint" id="pick-hint"></p><ol class="stones" id="stones"></ol>' +
        '<div class="actions" id="actions"><button class="btn" type="button" id="auto-btn">Tir automatique <kbd>Espace</kbd></button><span class="note">Il touche toujours, sans critique. A à E pour charger une pierre.</span></div>' +
        '<div class="feedback" id="feedback" hidden></div>' +
      "</section></section>";
  }

  /* ---------------- Mécaniques ---------------- */
  const API = {
    get F() { return F; },
    say: (text, dur) => say(text, dur),
    sayLine: (key, p) => { const l = F.B.lines.special && F.B.lines.special[key]; if (l && l.length && Math.random() < (p == null ? 1 : p)) say(pick(l), 2.4); },
    toast: (t, k) => toast(t, k), sound: (n) => Sound.play(n), burst: (x, y, n, o) => burst(x, y, n, o), popText: (...a) => popText(...a),
    addScore: (n) => { F.score += n; F.bonus += n; }, refreshStones: () => renderStones(), refreshArena: () => refreshArena(), reshuffle: () => reshuffle(),
    banner: (t, c) => banner(t, c), later: (s, fn) => later(s, fn), cast: () => { F.b.cast = 0; }, bossAttack: (cb) => bossAttack(cb),
    bossPos: () => ({ x: F.b.x + F.b.knock, y: F.b.y }), local: (p) => toWorld(p), weak: () => weakWorld(),
    playerPos: () => ({ x: F.player.x + 4, y: F.groundY - 92 }), shake: (m) => shake(m), lesson: (html) => { F.els.lesson.innerHTML = html; F.els.lesson.hidden = false; },
    unload: () => { F.loaded = null; F.sel = []; }, hurtPlayer: (cb) => playerHit(cb), questionId: () => curQ().id, isBoss: () => F.mode === "boss",
    showFeedback: (m) => showFeedback(m), updateHint: () => updateHint(), renderHUD: () => renderHUD(),
    failQuestion: () => { const q = curQ(); F.results.push({ k: F.i, id: q.id, ok: false }); recordAnswer(q, false, false); save(); }
  };
  function setMods(names) {
    for (const m of F.mods) { if (m.def.exit) m.def.exit(API, m.st); delete F.b.mech[m.name]; }
    F.mods = names.filter((n) => MECH[n]).map((name) => { const st = {}; F.b.mech[name] = st; return { name, def: MECH[name], st }; });
    for (const m of F.mods) if (m.def.init) m.def.init(API, m.st);
    if (F.els.stones) refreshArena();
  }
  function call(hook, ...args) { const out = []; for (const m of F.mods) { const fn = m.def[hook]; if (fn) out.push(fn(API, m.st, ...args)); } return out; }
  const firstOf = (arr) => arr.find((x) => x);

  /* ---------------- Monde ---------------- */
  function resize() {
    if (!F) return;
    const cv = F.els.stage, r = cv.getBoundingClientRect();
    if (r.width < 10 || r.height < 10) return;
    F.dpr = Math.min(window.devicePixelRatio || 1, 2);
    cv.width = Math.round(r.width * F.dpr); cv.height = Math.round(r.height * F.dpr);
    F.scale = Math.min(r.height / 600, r.width / 760);
    F.W = r.width / F.scale; F.H = r.height / F.scale;
    F.groundY = F.H - 64;
    F.bs = clamp(F.W / 980, 0.82, 1.05);
    F.player.x = Math.max(96, F.W * 0.14);
    F.b.x0 = F.W * 0.71;
    F.b.y0 = F.B.ground ? F.groundY - F.B.ground * F.bs : F.groundY - Math.min(320, F.H * 0.52);
    const rnd = seeded(7 + (F.n || 0));
    F.stars = []; for (let i = 0; i < 80; i++) F.stars.push({ x: rnd() * F.W, y: rnd() * (F.groundY - 120), r: rnd() * 1.4 + 0.3, p: rnd() * 6, s: rnd() * 2 + 0.5 });
    buildBackground();
  }
  function buildBackground() {
    const { W, H, groundY } = F, bg = F.els.bg, cv = F.els.stage;
    bg.width = cv.width; bg.height = cv.height;
    const b = bg.getContext("2d"); b.setTransform(F.dpr * F.scale, 0, 0, F.dpr * F.scale, 0, 0);
    const lvl = clamp(F.n || 1, 1, 10), sky = SKIES[lvl - 1], alt = (lvl - 1) / 9;
    const g = b.createLinearGradient(0, 0, 0, groundY); g.addColorStop(0, sky[0]); g.addColorStop(0.7, sky[1]); g.addColorStop(1, sky[2]);
    b.fillStyle = g; b.fillRect(0, 0, W, groundY);
    const mx = W * 0.88, my = Math.max(60, groundY - 470);
    if (lvl < 10) {
      const mg = b.createRadialGradient(mx, my, 10, mx, my, 120); mg.addColorStop(0, "rgba(232,236,246," + (0.18 * (1 - alt * 0.6)) + ")"); mg.addColorStop(1, "rgba(232,236,246,0)");
      b.fillStyle = mg; b.fillRect(mx - 120, my - 120, 240, 240);
      b.globalAlpha = 1 - alt * 0.55; b.fillStyle = "#dfe5f3"; b.beginPath(); b.arc(mx, my, 30, 0, Math.PI * 2); b.fill();
      b.fillStyle = sky[1]; b.beginPath(); b.arc(mx + 12, my - 7, 26, 0, Math.PI * 2); b.fill(); b.globalAlpha = 1;
    } else {
      const sg = b.createRadialGradient(W * 0.5, groundY - 30, 10, W * 0.5, groundY - 30, W * 0.6); sg.addColorStop(0, "rgba(243,184,65,0.45)"); sg.addColorStop(1, "rgba(243,184,65,0)");
      b.fillStyle = sg; b.fillRect(0, 0, W, groundY);
    }
    // ville : elle s'éloigne à mesure qu'on monte, puis passe sous les nuages
    const rnd = seeded(42); let x = -10;
    const drop = alt * 70, maxH = 150 * (1 - alt * 0.6);
    while (x < W + 20) {
      const w = 26 + rnd() * 50, h = 30 + rnd() * maxH, top = groundY - 40 - h + drop;
      b.fillStyle = col(mixv("#0e1528", sky[2], alt * 0.35)); b.fillRect(x, top, w, h + 40);
      for (let wy = top + 8; wy < groundY - 46; wy += 12) for (let wx = x + 5; wx < x + w - 6; wx += 9) if (rnd() < 0.16) { b.fillStyle = rnd() < 0.8 ? "rgba(243,184,65," + (0.55 - alt * 0.3) + ")" : "rgba(232,236,246,0.3)"; b.fillRect(wx, wy, 3, 5); }
      x += w + 2 + rnd() * 8;
    }
    if (alt > 0.3) {
      const cr = seeded(9);
      for (let k = 0; k < 14; k++) { const cx = cr() * W, cy = groundY - 40 - cr() * 40 * alt, rw = 90 + cr() * 140; b.fillStyle = "rgba(232,236,246," + (0.05 + alt * 0.1) + ")"; b.beginPath(); b.ellipse(cx, cy, rw, 18 + cr() * 14, 0, 0, Math.PI * 2); b.fill(); }
    }
    b.fillStyle = "#1a2238"; b.fillRect(0, groundY - 34, W, 34);
    b.strokeStyle = "#2b3657"; b.lineWidth = 1.5;
    for (let mxp = -10; mxp < W + 40; mxp += 64) { b.fillStyle = "#1d2643"; b.fillRect(mxp, groundY - 58, 40, 26); b.strokeRect(mxp + 0.5, groundY - 57.5, 39, 25); }
    b.beginPath(); b.moveTo(0, groundY - 34); b.lineTo(W, groundY - 34); b.stroke();
    for (let row = 0; row < 2; row++) for (let jx = (row % 2) * 30; jx < W; jx += 60) { b.beginPath(); b.moveTo(jx, groundY - 34 + row * 17); b.lineTo(jx, groundY - 17 + row * 17); b.stroke(); }
    b.fillStyle = "#141b2f"; b.fillRect(0, groundY, W, H - groundY);
    b.strokeStyle = "#232d4b"; b.beginPath(); b.moveTo(0, groundY + 0.5); b.lineTo(W, groundY + 0.5); b.stroke();
    for (let jx = 20; jx < W; jx += 80) { b.beginPath(); b.moveTo(jx, groundY); b.lineTo(jx - 30, H); b.stroke(); }
    if (F.n) { b.fillStyle = "rgba(232,236,246,0.08)"; b.font = "800 120px " + F_DISPLAY; b.textAlign = "left"; b.textBaseline = "alphabetic"; b.fillText(pad(F.n), 18, groundY - 66); }
  }
  const pointerToWorld = (e) => { const r = F.els.stage.getBoundingClientRect(); return { x: (e.clientX - r.left) / F.scale, y: (e.clientY - r.top) / F.scale }; };
  const restPouch = () => ({ x: F.player.x + F.player.knock + 46, y: F.groundY + F.player.dy - 126 });
  function pouchWorld() { const p = restPouch(), o = F.drag ? F.pull : F.spring; return { x: p.x + o.x, y: p.y + o.y }; }
  function toScreen(p) { const r = F.els.stage.getBoundingClientRect(); return { x: r.left + p.x * F.scale, y: r.top + p.y * F.scale }; }
  function toWorld(local) { const b = F.b, c = Math.cos(b.rot), s = Math.sin(b.rot); return { x: b.x + b.knock + (local.x * c - local.y * s) * F.bs, y: b.y + (local.x * s + local.y * c) * F.bs }; }
  const weakWorld = () => toWorld(F.B.weakSpot ? F.B.weakSpot(F.b) : { x: 0, y: 0 });
  const curQ = () => F.questions[F.i];

  /* ---------------- Effets ---------------- */
  function later(sec, fn) { F.timers.push({ t: sec, fn }); }
  function shake(m) { if (!reduceMotion) F.shakeMag = Math.max(F.shakeMag, m); }
  function popText(text, x, y, color, size, vy) { F.texts.push({ text, x, y, color, size, vy: vy == null ? -70 : vy, life: 0, max: 1.1 }); }
  function burst(x, y, n, o) {
    if (reduceMotion) n = Math.ceil(n / 3);
    for (let i = 0; i < n; i++) {
      const a = o.angle != null ? o.angle + rand(-o.spread, o.spread) : rand(0, Math.PI * 2), sp = rand(o.min || 60, o.max || 320);
      F.particles.push({ x, y, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp - (o.lift || 0), life: 0, max: rand(o.lmin || 0.5, o.lmax || 1.1), size: rand(o.smin || 2, o.smax || 5), color: o.color, kind: o.kind || "dot", rot: rand(0, 6), vr: rand(-10, 10), g: o.g == null ? GRAV : o.g, text: o.text });
    }
  }
  function say(text, dur) { if (text) F.bubble = { text, life: 0, max: dur || 2.6 }; }
  function sayMaybe(list, p) { if (list && list.length && Math.random() < p) say(pick(list), 2.2); }
  let toastT = null;
  function toast(text, kind) { const el = F.els.toast; el.textContent = text; el.className = "toast show" + (kind ? " " + kind : ""); clearTimeout(toastT); toastT = setTimeout(() => { if (F) el.className = "toast"; }, 2400); }
  function banner(text, cls) { const b = F.els.banner; b.textContent = text; b.className = "banner"; void b.offsetWidth; b.className = "banner show" + (cls ? " " + cls : ""); }
  function showHint(text) { F.els.hint.textContent = text; F.els.hint.hidden = false; }
  function hideHint() { F.els.hint.hidden = true; }
  function addCrack(wx, wy, big) {
    const b = F.B.hit, lx = clamp((wx - F.b.x - F.b.knock) / F.bs, -b.rx * 0.85, b.rx * 0.85), ly = clamp((wy - F.b.y) / F.bs, -b.ry * 0.8, b.ry * 0.8);
    for (let k = 0; k < (big ? 5 : 3); k++) {
      const pts = [[lx, ly]]; let a = rand(0, Math.PI * 2), x = lx, y = ly;
      for (let s = 0; s < 3; s++) { a += rand(-0.7, 0.7); const l = rand(9, big ? 22 : 15); x = clamp(x + Math.cos(a) * l, -b.rx, b.rx); y = clamp(y + Math.sin(a) * l, -b.ry, b.ry); pts.push([x, y]); }
      F.b.cracks.push(pts);
    }
    if (F.b.cracks.length > 48) F.b.cracks.splice(0, F.b.cracks.length - 48);
  }

  /* ---------------- Déroulé ---------------- */
  function start() {
    Sound.ensure();
    F.t0 = performance.now();
    if (F.mode === "boss") { lv(F.n).attempts = (L(F.n).attempts || 0) + 1; save(); }
    hideOverlay();
    startQuestion();
    if (F.mode === "boss") later(0.4, () => say(unquote(F.level.boss.taunt), 4));
  }
  function startQuestion() {
    const q = curQ();
    F.perm = shuffle(q.options.map((_, i) => i)); F.sel = []; F.loaded = null; F.bar = 0; F.warnT = 0;
    F.phase = "question";
    call("questionStart");
    renderQuestion();
    banner((F.mode === "boss" ? "Question " : "Révision ") + (F.i + 1) + " / " + F.questions.length);
    window.scrollTo({ top: 0 });
    updateHint(); refreshArena();
  }
  function renderQuestion() {
    const q = curQ(), els = F.els;
    els["q-count"].textContent = "Question " + (F.i + 1) + " / " + F.questions.length;
    els["q-domain"].textContent = q.domain + " " + DOMAINS[q.domain].short;
    els["q-domain"].title = DOMAINS[q.domain].name;
    els["q-level"].textContent = F.mode === "practice" && QINDEX[q.id] ? "Étage " + pad(QINDEX[q.id].level.id) : "";
    els["q-stem"].innerHTML = stemHTML(q.stem);
    els.lesson.hidden = true;
    els.feedback.hidden = true; els.feedback.innerHTML = "";
    els["pick-hint"].hidden = false; els.actions.hidden = false;
    renderStones(); renderDots();
  }
  function renderDots() {
    let h = "";
    for (let k = 0; k < F.questions.length; k++) { const r = F.results.find((x) => x.k === k); h += '<i class="' + (r ? (r.ok ? "ok" : "bad") : k === F.i ? "now" : "") + '"></i>'; }
    F.els.dots.innerHTML = F.questions.length <= 12 ? h : "";
  }
  function renderStones() {
    if (!F) return;
    const q = curQ(), revealed = F.phase === "feedback", need = q.answer.length;
    F.els["pick-hint"].textContent = need > 1
      ? "Charge 2 pierres : touche les deux réponses justes (" + F.sel.length + "/2). Elles partiront ensemble."
      : "Choisis ta pierre : touche une réponse pour la charger dans le lance-pierre.";
    let html = F.perm.map((oi, pos) => {
      const o = q.options[oi], sel = F.sel.includes(oi), good = q.answer.includes(oi);
      let cls = "stone";
      if (revealed) cls += good && sel ? " is-correct" : good ? " is-missed" : sel ? " is-wrong" : " is-dim";
      else if (sel) cls += " is-loaded";
      const why = revealed ? '<span class="why ' + (good ? "ok" : "bad") + '"><b>' + (good ? "Juste" : "Faux") + "</b>" + fmt(o.why) + "</span>" : "";
      const tag = !revealed && sel ? '<span class="loaded-tag">Chargée</span>' : "";
      return '<li><button type="button" class="' + cls + '" data-oi="' + oi + '" aria-pressed="' + sel + '"' + (revealed ? " disabled" : "") + '><span class="rune">' + LETTERS[pos] + '</span><span class="stone-body"><span lang="en">' + fmt(o.text) + "</span>" + why + "</span>" + tag + "</button></li>";
    }).join("");
    if (!revealed) html += call("stonesExtra").filter(Boolean).join("");
    F.els.stones.innerHTML = html;
  }
  function reshuffle() {
    const q = curQ(); F.perm = shuffle(q.options.map((_, i) => i));
    if (F.loaded && F.loaded.kind === "answer") F.loaded.letters = F.sel.map((x) => LETTERS[F.perm.indexOf(x)]);
    renderStones();
    const s = F.els.stones; s.classList.remove("shuffled"); void s.offsetWidth; s.classList.add("shuffled");
  }
  function refreshArena() {
    if (!F) return;
    const html = F.phase === "question" || F.phase === "flying" ? call("arena").filter(Boolean).join("") : "";
    F.els["arena-actions"].innerHTML = html;
    const zone = firstOf(call("barZone")), z = F.els["attack-zone"];
    if (zone && F.mode === "boss") { z.hidden = false; z.style.left = zone.from * 100 + "%"; z.style.width = (zone.to - zone.from) * 100 + "%"; z.title = zone.label || ""; } else z.hidden = true;
  }
  function renderHUD(instant) {
    const els = F.els, pct = clamp(F.hp / MAX_HP * 100, 0, 100);
    els["hp-fill"].style.width = pct + "%"; els["hp-chip"].style.width = pct + "%";
    if (instant) { els["hp-chip"].style.transition = "none"; void els["hp-chip"].offsetWidth; els["hp-chip"].style.transition = ""; }
    els["hp-num"].textContent = F.mode === "boss" ? Math.ceil(F.hp) + " / " + MAX_HP : (F.i + 1) + " / " + F.questions.length;
    els["hp-bar"].setAttribute("aria-label", "Vie du boss : " + Math.ceil(F.hp) + " sur " + MAX_HP);
    let h = "";
    for (let k = 0; k < HEARTS; k++) {
      const lost = k >= F.hearts, popNow = lost && k < F.prevHearts;
      h += '<svg class="heart' + (lost ? " lost" : "") + (popNow ? " pop" : "") + '" viewBox="0 0 24 22" aria-hidden="true"><path d="M12 20.5 L3.2 11.7 A5.2 5.2 0 0 1 12 4.4 A5.2 5.2 0 0 1 20.8 11.7 Z"/></svg>';
    }
    els.hearts.innerHTML = h; els.hearts.setAttribute("aria-label", plural(F.hearts, "vie"));
    F.prevHearts = F.hearts;
    if (F.combo >= 2) { els.combo.hidden = false; els.combo.textContent = "Combo ×" + F.combo; els.combo.classList.remove("pop"); void els.combo.offsetWidth; els.combo.classList.add("pop"); } else els.combo.hidden = true;
  }
  function updateHint() {
    if (!F || F.phase !== "question") { hideHint(); return; }
    const q = curQ();
    if (!F.loaded) { if (!F.tutDone) showHint(q.answer.length > 1 && F.sel.length ? "Choisis ta deuxième pierre" : "Touche une réponse pour charger ta pierre"); else hideHint(); }
    else if (!F.tutDone) showHint("Tire vers l’arrière dans l’arène, vise, puis relâche");
    else hideHint();
  }
  function scrollToEl(el) {
    const mobile = window.matchMedia("(max-width: 860px)").matches;
    const offset = mobile ? F.els["arena-col"].getBoundingClientRect().height + 12 : 16;
    const y = el.getBoundingClientRect().top + window.scrollY - offset;
    window.scrollTo({ top: Math.max(0, y), behavior: reduceMotion ? "auto" : "smooth" });
  }

  /* ---------------- Charger une pierre ---------------- */
  function flyStone(fromEl, letter, cls) {
    const rune = fromEl && fromEl.querySelector(".rune");
    F.arriveAt = F.time + 0.38;
    if (!rune || reduceMotion) { F.arriveAt = F.time; return; }
    const r = rune.getBoundingClientRect();
    if (r.bottom < 0 || r.top > window.innerHeight) { F.arriveAt = F.time; return; }
    const target = toScreen(restPouch()), d = document.createElement("div");
    d.className = "fly" + (cls ? " " + cls : ""); d.textContent = letter;
    const sx = r.left + r.width / 2, sy = r.top + r.height / 2;
    d.style.left = sx - 14 + "px"; d.style.top = sy - 14 + "px";
    document.body.appendChild(d);
    requestAnimationFrame(() => requestAnimationFrame(() => { d.style.transform = "translate(" + (target.x - sx) + "px," + (target.y - sy) + "px) scale(.75)"; }));
    setTimeout(() => d.remove(), 450);
  }
  function chooseOption(oi, el) {
    if (!F || F.phase !== "question" || F.paused) return;
    const q = curQ(), need = q.answer.length;
    if (F.loaded && F.loaded.kind !== "answer") F.loaded = null;
    const k = F.sel.indexOf(oi);
    if (need === 1) F.sel = [oi];
    else if (k >= 0) F.sel.splice(k, 1);
    else { if (F.sel.length >= need) F.sel.shift(); F.sel.push(oi); }
    const ready = F.sel.length === need;
    F.loaded = ready ? { kind: "answer", letters: F.sel.map((x) => LETTERS[F.perm.indexOf(x)]) } : null;
    Sound.play(ready ? "load" : "click");
    if (F.sel.includes(oi)) flyStone(el, LETTERS[F.perm.indexOf(oi)]);
    renderStones(); updateHint();
  }
  /** Charge une pierre spéciale (par exemple la pierre injectée). */
  function loadSpecial(kind, letter, el, cls) {
    if (!F || F.phase !== "question" || F.paused) return;
    F.sel = []; F.loaded = { kind, letters: [letter] };
    Sound.play("load"); flyStone(el, letter, cls);
    renderStones(); updateHint();
  }
  API.loadSpecial = loadSpecial;

  /* ---------------- Tir ---------------- */
  function bindEvents() {
    const cv = F.els.stage;
    cv.addEventListener("pointerdown", (e) => {
      if (!F) return;
      Sound.ensure();
      if (F.paused) { setPause(false); return; }
      const p = pointerToWorld(e);
      if (call("tap", p).some(Boolean)) return;
      if (F.phase !== "question") return;
      if (!F.loaded) {
        const q = curQ();
        toast(q.answer.length > 1 && F.sel.length ? "Il te faut une deuxième pierre" : "Choisis d’abord une pierre dans la liste");
        const s = F.els.stones; s.classList.remove("nudge"); void s.offsetWidth; s.classList.add("nudge");
        return;
      }
      F.drag = { sx: p.x, sy: p.y, id: e.pointerId }; F.pull.x = F.pull.y = 0; F.tickStep = 0;
      cv.setPointerCapture(e.pointerId); cv.classList.add("dragging");
    });
    cv.addEventListener("pointermove", (e) => {
      if (!F || !F.drag || e.pointerId !== F.drag.id) return;
      const p = pointerToWorld(e);
      let dx = p.x - F.drag.sx, dy = p.y - F.drag.sy; const len = Math.hypot(dx, dy);
      if (len > MAX_PULL) { dx *= MAX_PULL / len; dy *= MAX_PULL / len; }
      F.pull.x = dx; F.pull.y = dy;
      const step = Math.floor(Math.min(len, MAX_PULL) / 30);
      if (step !== F.tickStep) { F.tickStep = step; if (step > 0) Sound.play("stretch", step); }
    });
    const endDrag = (e, cancel) => {
      if (!F || !F.drag || (e && e.pointerId !== F.drag.id)) return;
      F.drag = null; F.els.stage.classList.remove("dragging");
      const len = Math.hypot(F.pull.x, F.pull.y);
      F.spring.x = F.pull.x; F.spring.y = F.pull.y; F.spring.vx = F.spring.vy = 0;
      if (!cancel && len > 22 && F.phase === "question") launch(-F.pull.x * K_LAUNCH, -F.pull.y * K_LAUNCH, false);
      F.pull.x = F.pull.y = 0;
    };
    cv.addEventListener("pointerup", (e) => endDrag(e, false));
    cv.addEventListener("pointercancel", (e) => endDrag(e, true));
    F.els["auto-btn"].addEventListener("click", autoShot);
    F.els.stones.addEventListener("click", (e) => {
      for (const m of F.mods) if (m.def.panelClick && m.def.panelClick(API, m.st, e.target)) return;
      const b = e.target.closest("button.stone[data-oi]"); if (!b || b.disabled) return;
      chooseOption(Number(b.dataset.oi), b);
    });
    F.els["arena-actions"].addEventListener("click", (e) => {
      const b = e.target.closest("[data-mech]"); if (!b) return;
      const m = F.mods.find((x) => x.name === b.dataset.mech);
      if (m && m.def.action) m.def.action(API, m.st, b.dataset.act);
    });
    F.els["sound-btn"].addEventListener("click", () => { const on = Sound.toggle(); F.els["sound-btn"].setAttribute("aria-pressed", String(on)); });
    F.els["pause-btn"].addEventListener("click", () => setPause(!F.paused));
    F.els["pause-veil"].addEventListener("click", () => setPause(false));
    F.els["quit-btn"].addEventListener("click", () => { if (F.phase === "intro" || F.phase === "end") { exit(); return; } F.els["quit-veil"].hidden = false; setPause(true, true); });
    F.els["quit-veil"].addEventListener("click", (e) => {
      const b = e.target.closest("[data-quit]"); if (!b) return;
      if (b.dataset.quit === "yes") exit(); else { F.els["quit-veil"].hidden = true; setPause(false); }
    });
  }
  function exit() { const o = F.opts; unmount(); if (o.onExit) o.onExit(); }
  function launch(vx, vy, auto) {
    const P = pouchWorld();
    F.proj = { x: P.x, y: P.y, vx, vy, r: 11, kind: F.loaded.kind, letters: F.loaded.letters.slice(), rot: 0, t: 0, trail: [], done: false, auto: !!auto };
    F.drag = null;
    F.phase = "flying";
    if (!F.tutDone) { F.tutDone = true; if (!state.seenTutorial) { state.seenTutorial = true; save(); } }
    hideHint(); Sound.play("release");
  }
  function autoShot() {
    if (!F || F.phase !== "question" || F.paused) return;
    if (!F.loaded) { toast("Choisis d’abord une pierre dans la liste"); return; }
    const P = restPouch(), T = 0.95, tx = F.b.x + F.B.hit.rx * 0.45 * F.bs, ty = F.b.y + F.B.hit.ry * 0.3 * F.bs;
    launch((tx - P.x) / T, (ty - P.y - 0.5 * GRAV * T * T) / T, true);
  }
  function updateProjectile(dt) {
    const p = F.proj; if (!p) return;
    const b = F.b, B = F.B, bs = F.bs;
    p.t += dt; p.vy += GRAV * dt;
    if (!p.done && !b.dead) {
      const dx = b.x - p.x, dy = b.y - p.y, d = Math.hypot(dx, dy), R = Math.max(B.hit.rx, B.hit.ry) * 1.25 * bs + 60;
      if (d < R && d > 1) { const f = (p.kind === "final" ? 5000 : p.auto ? 2600 : 1500) * (1 - d / R); p.vx += dx / d * f * dt; p.vy += dy / d * f * dt; }
    }
    p.x += p.vx * dt; p.y += p.vy * dt; p.rot += dt * 11;
    p.trail.push({ x: p.x, y: p.y }); if (p.trail.length > 14) p.trail.shift();
    if (!p.done && !b.dead) {
      if (!p.auto && p.kind !== "final") {
        const hit = firstOf(call("collide", p));
        if (hit && hit.type === "block") { blocked(hit); return; }
        if (hit && hit.type === "decoy") { impact(false); return; }
      }
      const ws = weakWorld(), crit = call("critAllowed").every((v) => v !== false);
      if (Math.hypot(p.x - ws.x, p.y - ws.y) < B.hit.coreR * bs + p.r * 0.6) { impact(!p.auto && crit); return; }
      const ex = p.x - b.x - b.knock, ey = p.y - b.y, rx = B.hit.rx * bs + p.r, ry = B.hit.ry * bs + p.r;
      if ((ex * ex) / (rx * rx) + (ey * ey) / (ry * ry) < 1) { impact(false); return; }
      if (p.kind === "final" && p.t > 1.4) { impact(true); return; }
    }
    if (p.y > F.groundY - 6) {
      if (!p.done) miss();
      p.y = F.groundY - 6; p.vy *= -0.35; p.vx *= 0.6;
      if (Math.abs(p.vy) < 70) { burst(p.x, p.y, 5, { color: C.muted, min: 30, max: 110, angle: -Math.PI / 2, spread: 1, smax: 3 }); F.proj = null; return; }
    }
    if (p.x > F.W + 120 || p.x < -120 || p.t > 3.5) { if (!p.done) miss(); F.proj = null; }
  }
  function miss(label) {
    if (F.proj) F.proj.done = true;
    Sound.play("miss");
    toast(label || "Raté : la pierre revient dans ta main");
    call("miss");
    later(0.55, () => { if (F && F.phase === "flying") { F.phase = "question"; F.arriveAt = F.time + 0.15; updateHint(); refreshArena(); } });
  }
  function blocked(hit) {
    const p = F.proj; p.done = true; p.vx = -Math.abs(p.vx) * 0.3 - 80; p.vy = -200;
    burst(p.x, p.y, 10, { color: C.muted, kind: "shard", min: 60, max: 220, smin: 3, smax: 6 });
    Sound.play("block"); shake(4);
    miss(hit.label || "Bloqué : la pierre revient dans ta main");
  }

  /* ---------------- Impact ---------------- */
  function impact(crit) {
    const p = F.proj; p.done = true;
    const hx = p.x, hy = p.y;
    if (p.kind === "final") { F.proj = null; bossDie(); return; }
    for (const m of F.mods) if (m.def.impactSpecial && m.def.impactSpecial(API, m.st, p, hx, hy)) { F.proj = null; return; }
    const q = curQ(), ok = sameSet(F.sel, q.answer), B = F.B;
    const pal = B.palette || {};
    if (ok) {
      F.proj = null;
      F.combo++; F.bestCombo = Math.max(F.bestCombo, F.combo); if (crit) F.crits++;
      let mult = 1, notes = [];
      if (F.mode === "boss") for (const r of call("correct", { crit, hx, hy })) if (r) { if (r.mult) mult *= r.mult; if (r.label) notes.push(r.label); }
      const remaining = F.questions.length - F.i;
      const dmg = F.mode === "boss" ? Math.max(6, Math.round(F.hp / (remaining + 0.6) * (crit ? 1.45 : 1) * (1 + 0.06 * Math.min(4, F.combo - 1)) * mult)) : (crit ? 18 : 10);
      const before = F.hp;
      if (F.mode === "boss") F.hp = Math.max(1, F.hp - dmg);
      const speed = F.mode === "boss" ? Math.round(50 * Math.max(0, 1 - F.bar / F.barMax)) : 0;
      F.score += 100 + (crit ? 50 : 0) + 25 * Math.min(4, F.combo - 1) + speed;
      F.hitStop = crit ? 0.13 : 0.07; shake(crit ? 17 : 9);
      F.b.flash = 1; F.b.knock = crit ? 30 : 16; F.b.squint = 1;
      addCrack(hx, hy, crit);
      burst(hx, hy, crit ? 26 : 14, { color: pal.accent || "#d9e8ff", kind: "shard", min: 120, max: crit ? 520 : 380, smin: 4, smax: 9, lift: 120 });
      burst(hx, hy, 14, { color: F.b.rage ? (pal.rage || C.rage) : (pal.main || C.toxic), min: 60, max: 300, lift: 80, smin: 2, smax: 5 });
      burst(hx, hy, crit ? 16 : 8, { color: C.lamp, kind: "spark", min: 200, max: 520, g: 0, lmin: 0.2, lmax: 0.4 });
      popText("-" + dmg, hx + rand(-10, 10), hy - 30, crit ? C.lamp : C.ink, crit ? 66 : 48);
      if (crit) popText(B.critLabel || "CRITIQUE", hx, hy - 90, C.lamp, 30, -40);
      notes.forEach((t, k) => popText(t, hx, hy - 130 - k * 34, C.glitch, 24, -30));
      Sound.play(crit ? "crit" : "hit");
      if (F.mode === "boss" && F.hp === 1 && before - dmg < 1) say("Je… m’accroche…", 2.4); else sayMaybe(crit ? B.lines.crit : B.lines.hit, 0.45);
      F.results.push({ k: F.i, id: q.id, ok: true, crit });
      recordAnswer(q, true, F.practiceKind === "review"); save();
      renderHUD();
      F.phase = "resolving";
      if (F.mode === "boss") checkPhase();
      later(0.8, () => showFeedback(crit ? "crit" : "hit"));
    } else {
      p.vx = -Math.abs(p.vx) * 0.3 - 140; p.vy = -280;
      F.combo = 0;
      popText("BLOQUÉ", hx, hy - 40, C.bad, 42);
      shake(6); F.b.flash = 0.35; Sound.play("block");
      burst(hx, hy, 10, { color: C.muted, kind: "shard", min: 80, max: 260, smin: 3, smax: 6 });
      F.results.push({ k: F.i, id: q.id, ok: false });
      recordAnswer(q, false, false); save();
      renderHUD();
      F.phase = "resolving";
      if (F.mode === "boss") {
        call("wrong");
        sayMaybe(B.lines.wrong, 0.7);
        later(0.35, () => bossAttack(() => later(0.5, () => showFeedback("wrong"))));
      } else later(0.6, () => showFeedback("wrong"));
    }
  }
  function checkPhase() {
    const B = F.B;
    if (B.phases) {
      const idx = F.hp > 66 ? 0 : F.hp > 33 ? 1 : 2;
      if (idx !== F.phaseIdx) later(0.9, () => enterPhase(idx));
    } else if (!F.b.rage && F.hp <= MAX_HP / 2) later(0.9, enrage);
  }
  function enterPhase(idx) {
    if (!F || F.b.dead || idx === F.phaseIdx) return;
    F.phaseIdx = idx; F.b.phase = idx;
    setMods(F.B.phases[idx]);
    if (idx === 2) { F.b.rage = true; F.els["hp-fill"].classList.add("rage"); }
    F.els["phase-tag"].hidden = false; F.els["phase-tag"].textContent = "Phase " + (idx + 1);
    banner("Phase " + (idx + 1), "rage"); shake(12); Sound.play("phase");
    const lines = F.B.lines.special && F.B.lines.special.phase;
    say(lines && lines[idx] ? lines[idx] : F.B.lines.rage, 3);
    const pal = F.B.palette || {};
    burst(F.b.x, F.b.y, 30, { color: pal.rage || C.rage, min: 100, max: 420, g: 200 });
  }
  function enrage() {
    if (!F || F.b.rage || F.b.dead) return;
    F.b.rage = true; shake(12);
    banner("Phase 2 · Il enrage", "rage");
    F.els["phase-tag"].hidden = false; F.els["phase-tag"].textContent = "Phase 2"; F.els["hp-fill"].classList.add("rage");
    say(F.B.lines.rage, 3); Sound.play("rage");
    call("rage");
    burst(F.b.x, F.b.y, 30, { color: (F.B.palette || {}).rage || C.rage, min: 100, max: 420, g: 200 });
  }

  /* ---------------- Riposte ---------------- */
  function bossAttack(cb) { F.b.atk = 0; F.b.atkFired = false; F.b.atkCb = cb; }
  function fireDart() {
    const s = toWorld(F.B.attackFrom || { x: 0, y: 0 });
    F.darts.push({ sx: s.x, sy: s.y, x: s.x, y: s.y, tx: F.player.x + 4, ty: F.groundY - 92, t: 0, dur: 0.42, trail: [], cb: F.b.atkCb });
    F.b.atkCb = null; Sound.play("dart");
  }
  function playerHit(cb) {
    F.hearts = Math.max(0, F.hearts - 1);
    F.player.hurt = 1; F.hurtFlash = 1; shake(15); F.hitStop = 0.06;
    const pal = F.B.palette || {};
    burst(F.player.x + 4, F.groundY - 92, 16, { color: F.b.rage ? (pal.rage || C.rage) : (pal.main || C.toxic), min: 80, max: 320, smin: 2, smax: 5 });
    popText("-1 vie", F.player.x, F.groundY - 170, C.bad, 34);
    Sound.play("hurt");
    if (F.hearts <= 0) F.player.mood = "lose";
    renderHUD();
    if (cb) cb();
  }
  function timedOut() {
    F.phase = "resolving"; F.timeouts++; F.combo = 0;
    if (F.drag) { F.drag = null; F.els.stage.classList.remove("dragging"); F.spring.x = F.pull.x; F.spring.y = F.pull.y; F.pull.x = F.pull.y = 0; }
    sayMaybe(F.B.lines.timeout, 1);
    bossAttack(() => {
      F.bar = 0;
      if (F.hearts <= 0) { const q = curQ(); F.results.push({ k: F.i, id: q.id, ok: false }); recordAnswer(q, false, false); save(); later(0.4, () => showFeedback("timeout")); }
      else later(0.4, () => { F.phase = "question"; toast("Il a frappé : −1 vie. Le chrono repart.", "warn"); updateHint(); refreshArena(); });
    });
  }

  /* ---------------- Retour d'information ---------------- */
  function showFeedback(mode) {
    if (!F) return;
    F.phase = "feedback";
    const q = curQ();
    const notes = call("feedbackNote").filter(Boolean).join("");
    if (F.loaded && F.loaded.kind !== "answer") F.loaded = null;
    renderStones(); renderDots(); refreshArena();
    F.els["pick-hint"].hidden = true; F.els.actions.hidden = true; hideHint();
    const heads = { crit: ["crit", "Coup critique !"], hit: ["good", "Touché !"], wrong: ["bad", F.mode === "boss" ? "Bloqué. Il riposte." : "Pas cette fois."], timeout: ["bad", "Trop lent : il a frappé le premier."], injected: ["bad", "Tu as lancé sa pierre piégée."] };
    const [cls, title] = heads[mode] || heads.wrong;
    const last = F.i >= F.questions.length - 1;
    const label = F.mode === "practice" ? (last ? "Terminer" : "Question suivante") : F.hearts <= 0 ? "Voir le résultat" : last ? "Coup de grâce" : "Question suivante";
    const fb = F.els.feedback;
    fb.className = "feedback " + cls;
    fb.innerHTML = "<h3>" + title + "</h3><p>" + fmt(q.explanation) + '</p><div class="tip"><b>Réflexe examen</b><span>' + fmt(q.tip) + "</span></div>" + notes +
      (q.source && q.source.url ? '<p class="src">Doc officielle : <a href="' + esc(q.source.url) + '" target="_blank" rel="noopener">' + esc(q.source.title || q.source.url) + " ↗</a></p>" : "") +
      '<div class="btn-row"><button class="btn btn-primary" type="button" id="next-btn">' + label + " → <kbd>Entrée</kbd></button></div>";
    fb.hidden = false;
    $("next-btn").addEventListener("click", next);
    const rect = fb.getBoundingClientRect();
    if (rect.top > window.innerHeight * 0.7 || rect.top < 0) scrollToEl(fb);
    $("next-btn").focus({ preventScroll: true });
  }
  function next() {
    if (!F || F.phase !== "feedback") return;
    if (F.mode === "practice") { if (F.i >= F.questions.length - 1) { endPractice(); return; } F.i++; renderHUD(); startQuestion(); return; }
    if (F.hearts <= 0) { endFight(false); return; }
    if (F.i >= F.questions.length - 1) { coupDeGrace(); return; }
    F.i++; startQuestion();
  }
  function coupDeGrace() {
    F.phase = "finale"; F.els.feedback.hidden = true;
    banner("Coup de grâce");
    F.loaded = { kind: "final", letters: ["★"] }; F.arriveAt = F.time;
    later(0.9, () => {
      const P = restPouch(), T = 0.8, ws = weakWorld();
      F.proj = { x: P.x, y: P.y, vx: (ws.x - P.x) / T, vy: (ws.y - P.y - 0.5 * GRAV * T * T) / T, r: 14, kind: "final", letters: ["★"], rot: 0, t: 0, trail: [], done: false, auto: false };
      F.loaded = null; Sound.play("release");
    });
  }
  function bossDie() {
    const b = F.b, pal = F.B.palette || {}, bs = F.bs, B = F.B;
    b.dead = true; F.hp = 0; renderHUD();
    F.timeScale = reduceMotion ? 1 : 0.35; later(1.1, () => { if (F) F.timeScale = 1; });
    shake(24); F.hitStop = 0.15; Sound.play("shatter");
    for (let k = 0; k < 46; k++) F.particles.push({ x: b.x + rand(-B.hit.rx, B.hit.rx) * bs, y: b.y + rand(-B.hit.ry, B.hit.ry) * bs, vx: rand(-260, 260), vy: rand(-520, -120), life: 0, max: rand(1.2, 2.2), size: rand(5, 13), color: pick([pal.accent || "#d9e8ff", pal.main || C.toxic, pal.dark || C.slab2]), kind: "shard", rot: rand(0, 6), vr: rand(-12, 12), g: GRAV });
    burst(b.x, b.y, 50, { color: pal.main || C.toxic, min: 80, max: 460, lift: 160, smin: 3, smax: 7, lmax: 1.6 });
    F.debris = [
      { x: b.x - B.hit.rx * 0.6 * bs, y: b.y, vx: -120, vy: -260, rot: b.rot, vr: -4, w: 70, h: 18, color: pal.dark || C.slab2 },
      { x: b.x + B.hit.rx * 0.6 * bs, y: b.y, vx: 160, vy: -300, rot: b.rot, vr: 5, w: 50, h: 40, color: pal.main || C.toxic }
    ];
    b.gone = true; F.player.mood = "win";
    later(0.9, () => { Sound.play("win"); for (let k = 0; k < 60; k++) F.particles.push({ x: rand(0, F.W), y: rand(-60, -10), vx: rand(-40, 40), vy: rand(60, 200), life: 0, max: rand(2, 3.4), size: rand(4, 8), color: pick([C.lamp, C.ok, C.ink, pal.main || C.toxic]), kind: "confetti", rot: rand(0, 6), vr: rand(-6, 6), g: 60 }); });
    later(2.2, () => endFight(true));
  }

  /* ---------------- Fin ---------------- */
  function endFight(win) {
    F.phase = "end"; hideHint(); refreshArena();
    const elapsed = (performance.now() - F.t0) / 1000;
    const correct = F.results.filter((r) => r.ok).length;
    const misses = F.results.filter((r) => !r.ok);
    const s = lv(F.n);
    s.best = Math.max(s.best || 0, correct);
    let record = false;
    if (win) {
      s.won = true; s.stars = Math.max(s.stars || 0, F.hearts);
      if (F.score > (s.bestScore || 0)) { s.bestScore = F.score; record = true; }
      s.bestCombo = Math.max(s.bestCombo || 0, F.bestCombo);
      s.bestTime = s.bestTime ? Math.min(s.bestTime, Math.round(elapsed)) : Math.round(elapsed);
    }
    save();
    if (!win) { Sound.play("lose"); say(unquote(F.level.boss.victory), 5); }
    const stars = win ? F.hearts : 0, level = F.level, n = F.n, lastFloor = n === LEVELS[LEVELS.length - 1].id;
    let starHTML = ""; for (let k = 0; k < 3; k++) starHTML += '<span class="' + (k < stars ? "on" : "") + '">★</span>';
    const missList = misses.length ? '<div><p class="eyebrow" style="margin-bottom:8px">À revoir (ajoutées à ta salle de révision)</p><ul class="misslist">' + misses.map((r) => { const q = QINDEX[r.id].q; return '<li lang="en">' + fmt(q.stem.length > 150 ? q.stem.slice(0, 150) + "…" : q.stem) + "</li>"; }).join("") + "</ul></div>" : "";
    const buttons = win
      ? (lastFloor ? '<button class="btn btn-primary" type="button" data-end="tower">Contempler la tour</button>' : '<button class="btn btn-primary" type="button" data-end="next">Monter à l’étage ' + pad(n + 1) + " ↑</button>") + '<button class="btn" type="button" data-end="again">Rejouer</button>' + (lastFloor ? "" : '<button class="btn" type="button" data-end="tower">La tour</button>')
      : '<button class="btn btn-primary" type="button" data-end="again">Réessayer</button><button class="btn" type="button" data-end="cards">Revoir les fiches</button><button class="btn" type="button" data-end="tower">La tour</button>';
    showOverlay(
      '<p class="eyebrow">Étage ' + pad(n) + " · " + (win ? "Victoire" : "Défaite") + "</p>" +
      '<h1 id="ov-title">' + (win ? (lastFloor ? "La tour est à toi" : esc(level.boss.name) + (/^La /.test(level.boss.name) ? " est vaincue" : " est vaincu")) : esc(level.boss.name) + " garde l’étage") + "</h1>" +
      '<p class="quote">« ' + esc(unquote(win ? level.boss.defeat : level.boss.victory)) + " »</p>" +
      (win ? '<div class="stars" aria-label="' + stars + ' étoiles sur 3">' + starHTML + "</div>" : "") +
      '<div><p class="eyebrow">Score</p><div class="big-score">' + F.score + "</div>" + (record ? '<p class="record">Nouveau record</p>' : s.bestScore ? '<p class="note">Record : ' + s.bestScore + "</p>" : "") + "</div>" +
      '<dl class="stats"><div><dt>Bonnes réponses</dt><dd>' + correct + " / " + F.results.length + "</dd></div><div><dt>Coups critiques</dt><dd>" + F.crits + "</dd></div><div><dt>Meilleur combo</dt><dd>×" + F.bestCombo + "</dd></div><div><dt>Bonus de mécanique</dt><dd>+" + F.bonus + "</dd></div><div><dt>Temps total</dt><dd>" + fmtMS(elapsed) + "</dd></div><div><dt>Rythme moyen</dt><dd>" + fmtMS(elapsed / Math.max(1, F.results.length)) + "</dd></div></dl>" +
      (win && lastFloor ? '<p class="lede">Tu as vaincu les dix boss. Vide ta salle de révision et rejoue les étages sans trois étoiles pour consolider.</p>' : "") +
      missList + '<div class="btn-row">' + buttons + "</div>",
      (e) => {
        const b = e.target.closest("[data-end]"); if (!b) return;
        const act = b.dataset.end, o = F.opts;
        if (act === "again") { const n0 = F.n; unmount(); mount({ mode: "boss", n: n0, onExit: o.onExit, onEnd: o.onEnd }); return; }
        unmount(); if (o.onEnd) o.onEnd({ win, action: act, n });
      }
    );
  }
  function endPractice() {
    F.phase = "end";
    const correct = F.results.filter((r) => r.ok).length, left = reviewIds().length, review = F.practiceKind === "review";
    showOverlay(
      '<p class="eyebrow">' + esc(F.opts.title || "Entraînement") + '</p><h1 id="ov-title">Session terminée : ' + correct + " / " + F.results.length + "</h1>" +
      '<p class="lede">' + (review ? (left ? "Il reste " + plural(left, "question") + " dans ta salle de révision. Chaque bonne réponse en révision retire la question." : "Ta salle de révision est vide. Bravo.") : "Les erreurs de ce mode libre rejoignent ta salle de révision.") + "</p>" +
      '<div class="btn-row">' + (review && left ? '<button class="btn btn-primary" type="button" data-end="review">Relancer une révision</button>' : "") + '<button class="btn' + (review && left ? "" : " btn-primary") + '" type="button" data-end="back">Retour</button></div>',
      (e) => {
        const b = e.target.closest("[data-end]"); if (!b) return;
        const o = F.opts; unmount(); if (o.onEnd) o.onEnd({ action: b.dataset.end });
      }
    );
  }
  function showIntro() {
    F.phase = "intro";
    const level = F.level, B = F.B, s = L(F.n);
    const steps = state.seenTutorial ? "" :
      '<ol class="steps">' +
        '<li><svg viewBox="0 0 34 34" aria-hidden="true"><rect x="6" y="4" width="22" height="26" rx="3" fill="none" stroke="#9aa5c3" stroke-width="2"/><path d="M11 11h12M11 16h12M11 21h8" stroke="#f3b841" stroke-width="2" stroke-linecap="round"/></svg><b>1. Lis</b><span>La question est en anglais, comme à l’examen.</span></li>' +
        '<li><svg viewBox="0 0 34 34" aria-hidden="true"><path d="M10 5h14l7 12-7 12H10L3 17z" fill="#a9b2cc"/><text x="17" y="22" text-anchor="middle" font-family="monospace" font-weight="700" font-size="13" fill="#0c111e">B</text></svg><b>2. Charge</b><span>Touche ta réponse : elle devient une pierre. « Select TWO » : charges-en deux.</span></li>' +
        '<li><svg viewBox="0 0 34 34" aria-hidden="true"><path d="M17 31V18M17 18L10 6M17 18l7-12" stroke="#7a5a3f" stroke-width="3" stroke-linecap="round" fill="none"/><path d="M10 6l-4 10M24 6l-18 10" stroke="#d9774b" stroke-width="1.6" fill="none"/><circle cx="6" cy="17" r="3.5" fill="#f3b841"/></svg><b>3. Tire</b><span>Tire vers l’arrière dans l’arène, vise, relâche. Sa cible critique vaut plus de dégâts.</span></li>' +
      "</ol>";
    showOverlay(
      '<p class="eyebrow">Étage ' + pad(F.n) + " · " + esc(level.title) + "</p>" +
      '<h1 id="ov-title">' + esc(level.boss.name) + '</h1><p class="epithet">' + esc(level.boss.epithet) + '</p><p class="quote">« ' + esc(unquote(level.boss.taunt)) + " »</p>" +
      '<div class="mech-card"><b>' + esc(B.intro ? B.intro.title : "Sa mécanique") + "</b><span>" + esc(B.intro ? B.intro.text : "") + "</span></div>" +
      steps +
      '<ul class="rules"><li><strong>Bonne réponse</strong> : il perd de la vie. <strong>Mauvaise</strong> : ta pierre se brise et il riposte, −1 vie. 3 vies : survis aux 10 questions.</li>' +
      "<li><strong>Sa barre d’attaque</strong> : " + fmtMS(F.barMax) + " par question" + (F.barMax > EXAM_S ? " à cet étage (le trait blanc marque le rythme de l’examen, " + fmtMS(EXAM_S) + ")" : ", le rythme réel de l’examen") + ". Pleine, il frappe.</li>" +
      "<li>L’adresse rapporte des points, jamais la bonne réponse. Le tir automatique (Espace) touche toujours, sans critique.</li></ul>" +
      (s.bestScore ? '<p class="note">Ton record ici : ' + s.bestScore + " points" + (s.stars ? " · " + plural(s.stars, "étoile") : "") + "</p>" : "") +
      '<div class="btn-row"><button class="btn btn-primary" type="button" data-intro="go">Combattre</button><button class="btn" type="button" data-intro="back">Retour à l’étage</button></div>',
      (e) => {
        const b = e.target.closest("[data-intro]"); if (!b) return;
        if (b.dataset.intro === "go") start(); else exit();
      }
    );
  }
  function showOverlay(html, onClick) {
    const ov = $("overlay"), card = $("ov-card");
    card.innerHTML = html; ov.hidden = false;
    card.onclick = onClick || null;
    const first = card.querySelector(".btn-primary"); if (first) first.focus({ preventScroll: true });
  }
  function hideOverlay() { const ov = $("overlay"); if (ov) { ov.hidden = true; $("ov-card").onclick = null; } }
  function setPause(v, silent) {
    if (!F || F.phase === "intro" || F.phase === "end") return;
    F.paused = v; F.els["pause-veil"].hidden = !v || !!silent; F.els.attack.classList.toggle("paused-bar", v);
    F.els["pause-btn"].setAttribute("aria-label", v ? "Reprendre" : "Pause");
  }

  /* ---------------- Mise à jour ---------------- */
  function update(dt, real) {
    F.time += dt;
    const b = F.b, B = F.B;
    for (let i = F.timers.length - 1; i >= 0; i--) { F.timers[i].t -= real; if (F.timers[i].t <= 0) { const f = F.timers[i].fn; F.timers.splice(i, 1); f(); if (!F) return; } }
    if (F.mode === "boss" && F.phase === "question") {
      const mult = call("barMult").reduce((a, v) => a * (v || 1), 1) * (b.rage ? 1.18 : 1) * (b.stun > 0 ? 0 : 1);
      F.bar += real * mult;
      const frac = F.bar / F.barMax;
      if (frac > 0.8) { F.warnT -= real; if (F.warnT <= 0) { Sound.play("warn"); F.warnT = Math.max(0.35, 1 - (frac - 0.8) * 3); } }
      if (frac >= 1) timedOut();
    }
    call("tick", dt, real);
    if (!F) return;
    const p = F.player;
    p.blinkT -= dt; if (p.blinkT <= 0) { p.blink = 0.12; p.blinkT = rand(2.2, 4.5); }
    p.blink = Math.max(0, p.blink - dt); p.hurt = Math.max(0, p.hurt - dt * 1.6); p.knock = -18 * p.hurt;
    p.dy = p.mood === "win" ? -Math.abs(Math.sin(F.time * 6)) * 18 : p.mood === "lose" ? 16 : 0;
    const sp = F.spring;
    if (!F.drag) { sp.vx += (-320 * sp.x - 15 * sp.vx) * dt; sp.vy += (-320 * sp.y - 15 * sp.vy) * dt; sp.x += sp.vx * dt; sp.y += sp.vy * dt; }
    b.t += dt; b.time = F.time;
    const fast = b.rage ? 1.7 : 1;
    b.x = b.x0 + (B.static ? 0 : b.rage ? Math.sin(b.t * 0.95) * 44 : Math.sin(b.t * 0.45) * 10);
    b.y = b.y0 + (B.static ? 0 : Math.sin(b.t * 1.7 * fast) * 14 * F.bs);
    b.flash = Math.max(0, b.flash - dt * 4); b.squint = Math.max(0, b.squint - dt * 2.5);
    b.knock = lerp(b.knock, 0, 1 - Math.exp(-dt * 7));
    b.rageT = clamp(b.rageT + (b.rage ? dt : -dt) * 1.2, 0, 1);
    b.hpFrac = lerp(b.hpFrac, F.hp / MAX_HP, 1 - Math.exp(-dt * 5));
    b.stun = Math.max(0, b.stun - dt);
    b.aiming = F.phase === "question" || F.phase === "flying";
    let lean = 0;
    if (b.atk >= 0) {
      b.atk += dt; const a = b.atk;
      if (a < 0.22) lean = 0.07 * (a / 0.22);
      else if (a < 0.34) { lean = -0.09; if (!b.atkFired) { b.atkFired = true; fireDart(); b.knock = -26; } }
      else if (a < 0.75) lean = -0.09 * (1 - (a - 0.34) / 0.41);
      else b.atk = -1;
    }
    if (b.cast >= 0) { b.cast += dt; const a = b.cast, k = a < 0.25 ? a / 0.25 : a < 0.6 ? 1 : Math.max(0, 1 - (a - 0.6) / 0.3); lean += (B.castLean == null ? -0.15 : B.castLean) * k; if (a > 0.9) b.cast = -1; }
    if (b.stun > 0) lean += Math.sin(b.t * 32) * 0.03;
    b.lean = lerp(b.lean, lean, 1 - Math.exp(-dt * 18));
    b.rot = (B.static ? 0 : Math.sin(b.t * 1.1) * 0.045) + b.lean;
    if (B.update) B.update(b, dt);
    for (let i = F.darts.length - 1; i >= 0; i--) {
      const d = F.darts[i]; d.t += dt; const k = Math.min(1, d.t / d.dur);
      d.x = lerp(d.sx, d.tx, k); d.y = lerp(d.sy, d.ty, k) - Math.sin(k * Math.PI) * 40;
      d.trail.push({ x: d.x, y: d.y }); if (d.trail.length > 10) d.trail.shift();
      if (k >= 1) { F.darts.splice(i, 1); playerHit(d.cb); if (!F) return; }
    }
    updateProjectile(dt);
    if (!F) return;
    const parts = F.particles;
    for (let i = parts.length - 1; i >= 0; i--) {
      const q = parts[i]; q.life += dt;
      if (q.life >= q.max) { parts.splice(i, 1); continue; }
      q.vy += q.g * dt; q.x += q.vx * dt; q.y += q.vy * dt; q.rot += q.vr * dt;
      if (q.kind !== "confetti" && q.kind !== "token" && q.y > F.groundY && q.vy > 0) { q.y = F.groundY; q.vy *= -0.3; q.vx *= 0.6; }
      if (q.kind === "spark" || q.kind === "glitch") { q.vx *= 0.94; q.vy *= 0.94; }
    }
    if (parts.length > 420) parts.splice(0, parts.length - 420);
    for (let i = F.texts.length - 1; i >= 0; i--) { const t = F.texts[i]; t.life += dt; t.y += t.vy * dt; t.vy *= 0.97; if (t.life >= t.max) F.texts.splice(i, 1); }
    for (const d of F.debris) { d.vy += GRAV * dt; d.x += d.vx * dt; d.y += d.vy * dt; d.rot += d.vr * dt; if (d.y > F.groundY - 8) { d.y = F.groundY - 8; d.vy *= -0.3; d.vx *= 0.5; d.vr *= 0.5; } }
    if (F.bubble) { F.bubble.life += real; if (F.bubble.life > F.bubble.max) F.bubble = null; }
    F.shakeMag = Math.max(0, F.shakeMag - real * 40);
    F.hurtFlash = Math.max(0, F.hurtFlash - real * 2);
    if (Math.random() < dt * 6) { const bx = Math.random() < 0.5 ? F.W * 0.04 : F.W * 0.965; parts.push({ x: bx + rand(-4, 4), y: F.groundY - 74, vx: rand(-10, 10), vy: rand(-60, -30), life: 0, max: rand(0.8, 1.6), size: rand(1, 2.4), color: C.lamp, kind: "dot", rot: 0, vr: 0, g: -10 }); }
    F.scoreShown = lerp(F.scoreShown, F.score, 1 - Math.exp(-real * 8));
    if (Math.abs(F.scoreShown - F.score) < 0.5) F.scoreShown = F.score;
    F.els.score.textContent = Math.round(F.scoreShown);
    if (F.mode === "boss") {
      const frac = F.phase === "intro" ? 0 : clamp(F.bar / F.barMax, 0, 1);
      F.els["attack-fill"].style.width = frac * 100 + "%";
      F.els["attack-time"].textContent = F.phase === "question" || F.phase === "flying" ? fmtMS(F.barMax - F.bar) : "—";
      F.els.attack.classList.toggle("danger", frac > 0.8 && F.phase === "question");
    }
  }

  /* ---------------- Dessin ---------------- */
  function drawStone(ctx, x, y, r, letter, rot, kind) {
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot);
    const g = ctx.createRadialGradient(-r * 0.4, -r * 0.4, 1, 0, 0, r * 1.1);
    if (kind === "inject") { g.addColorStop(0, "#eadfff"); g.addColorStop(1, C.glitch); }
    else if (kind === "final") { g.addColorStop(0, "#fff4cf"); g.addColorStop(1, C.lamp); }
    else { g.addColorStop(0, "#cfd6e8"); g.addColorStop(1, "#6b7593"); }
    ctx.fillStyle = g; ctx.beginPath();
    for (let i = 0; i < 9; i++) { const a = (i / 9) * Math.PI * 2, r2 = r * (0.86 + 0.14 * Math.sin(i * 2.7)); ctx.lineTo(Math.cos(a) * r2, Math.sin(a) * r2); }
    ctx.closePath(); ctx.fill(); ctx.strokeStyle = "rgba(12,17,30,0.55)"; ctx.lineWidth = 1.5; ctx.stroke();
    ctx.rotate(-rot); ctx.fillStyle = C.night; ctx.font = "700 " + Math.round(r * 1.05) + "px " + F_MONO; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText(letter, 0, 1);
    ctx.restore();
    if (kind === "inject" && Math.random() < 0.35) { ctx.fillStyle = col(C.glitch, 0.5); ctx.fillRect(x + rand(-r, r), y + rand(-r, r), rand(4, 10), 2); }
  }
  function drawLoad(ctx, x, y, letters, kind, rot) {
    if (letters.length === 2) {
      const a = rot * 0.6, dx = Math.cos(a) * 12, dy = Math.sin(a) * 12;
      ctx.strokeStyle = C.rubber; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(x - dx, y - dy); ctx.lineTo(x + dx, y + dy); ctx.stroke();
      drawStone(ctx, x - dx, y - dy, 9.5, letters[0], rot, kind); drawStone(ctx, x + dx, y + dy, 9.5, letters[1], rot, kind);
    } else drawStone(ctx, x, y, kind === "final" ? 14 : 11, letters[0], rot, kind);
  }
  function drawPlayer(ctx) {
    const p = F.player, x = p.x + p.knock, y = F.groundY + p.dy, h = p.hurt;
    const breath = Math.sin(F.time * 2.2) * 1.4;
    const coat = col(mixv(C.coat, C.bad, h * 0.6)), skin = col(mixv(C.skin, C.bad, h * 0.35)), trouser = col(mixv("#222b47", C.bad, h * 0.4));
    ctx.save(); ctx.translate(x, y);
    ctx.fillStyle = "rgba(0,0,0,0.35)"; ctx.beginPath(); ctx.ellipse(4, 3 - p.dy, 34, 7, 0, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = trouser; rr(ctx, -15, -52, 11, 50, 4); ctx.fill(); rr(ctx, 4, -52, 11, 50, 4); ctx.fill();
    ctx.fillStyle = "#11172a"; rr(ctx, -18, -8, 16, 8, 3); ctx.fill(); rr(ctx, 3, -8, 18, 8, 3); ctx.fill();
    ctx.translate(0, breath * 0.5);
    ctx.fillStyle = coat; ctx.beginPath(); ctx.moveTo(-21, -113); ctx.lineTo(21, -113); ctx.lineTo(27, -48); ctx.lineTo(-27, -48); ctx.closePath(); ctx.fill();
    ctx.fillStyle = C.lamp; ctx.fillRect(-24, -90, 48, 6); ctx.fillRect(-25.5, -71, 51, 6);
    ctx.fillStyle = "rgba(232,236,246,0.6)"; ctx.fillRect(-24, -88, 48, 2); ctx.fillRect(-25.5, -69, 51, 2);
    ctx.fillStyle = "#26304f"; ctx.fillRect(-3, -113, 6, 65);
    ctx.fillStyle = skin; ctx.beginPath(); ctx.arc(3, -131, 17, 0, Math.PI * 2); ctx.fill();
    const eh = p.blink > 0 ? 0.4 : 3;
    ctx.fillStyle = C.night; ctx.beginPath(); ctx.ellipse(8, -133, 2.2, eh, 0, 0, Math.PI * 2); ctx.ellipse(15, -133, 2.2, eh, 0, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = C.night; ctx.lineWidth = 1.6; ctx.beginPath();
    if (p.mood === "lose" || h > 0.3) { ctx.moveTo(7, -121); ctx.quadraticCurveTo(11, -125, 15, -121); } else { ctx.moveTo(7, -124); ctx.quadraticCurveTo(11, -120, 16, -124); }
    ctx.stroke();
    ctx.fillStyle = C.lamp; ctx.beginPath(); ctx.arc(3, -137, 19, Math.PI, 0); ctx.fill(); rr(ctx, -16, -139, 44, 6, 3); ctx.fill();
    ctx.fillStyle = "#c98f22"; ctx.fillRect(0, -155, 5, 17);
    ctx.restore();
  }
  function drawSling(ctx) {
    const p = F.player, ox = p.x + p.knock, oy = F.groundY + p.dy + Math.sin(F.time * 2.2) * 0.7, h = p.hurt;
    const coat = col(mixv(C.coat, C.bad, h * 0.6)), skin = col(mixv(C.skin, C.bad, h * 0.35));
    const sh1 = { x: ox + 10, y: oy - 104 }, hand = { x: ox + 40, y: oy - 102 };
    ctx.lineCap = "round";
    ctx.strokeStyle = coat; ctx.lineWidth = 9; ctx.beginPath(); ctx.moveTo(sh1.x, sh1.y); ctx.lineTo(hand.x, hand.y); ctx.stroke();
    const fork = { x: hand.x + 5, y: hand.y - 14 }, tipL = { x: ox + 37, y: oy - 133 }, tipR = { x: ox + 57, y: oy - 131 };
    ctx.strokeStyle = C.wood; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(hand.x + 3, hand.y + 6); ctx.lineTo(fork.x, fork.y); ctx.lineTo(tipL.x, tipL.y); ctx.moveTo(fork.x, fork.y); ctx.lineTo(tipR.x, tipR.y); ctx.stroke();
    ctx.fillStyle = skin; ctx.beginPath(); ctx.arc(hand.x + 2, hand.y, 5.5, 0, Math.PI * 2); ctx.fill();
    const pouch = pouchWorld(), rest = restPouch(), stretch = Math.hypot(pouch.x - rest.x, pouch.y - rest.y) / MAX_PULL;
    const band = col(mixv(C.rubber, C.bad, stretch * 0.5));
    ctx.strokeStyle = band; ctx.lineWidth = 3 - stretch; ctx.beginPath(); ctx.moveTo(tipL.x, tipL.y); ctx.lineTo(pouch.x, pouch.y); ctx.stroke();
    const showLoad = F.loaded ? F.loaded : (F.sel.length && F.phase === "question" ? { kind: "answer", letters: F.sel.map((x) => LETTERS[F.perm.indexOf(x)]) } : null);
    if (showLoad && F.time >= F.arriveAt && !F.proj && (F.phase === "question" || F.phase === "finale")) drawLoad(ctx, pouch.x, pouch.y, showLoad.letters, showLoad.kind, 0);
    ctx.fillStyle = "#5a3f2e"; ctx.beginPath(); ctx.ellipse(pouch.x, pouch.y + 6, 9, 4, 0, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = band; ctx.lineWidth = 3 - stretch; ctx.beginPath(); ctx.moveTo(tipR.x, tipR.y); ctx.lineTo(pouch.x, pouch.y); ctx.stroke();
    const sh2 = { x: ox - 4, y: oy - 104 }, el = elbow(sh2, pouch, 30, 32, false);
    ctx.strokeStyle = coat; ctx.lineWidth = 9; ctx.beginPath(); ctx.moveTo(sh2.x, sh2.y); ctx.lineTo(el.x, el.y); ctx.lineTo(pouch.x, pouch.y); ctx.stroke();
    ctx.fillStyle = skin; ctx.beginPath(); ctx.arc(pouch.x, pouch.y + 1, 5.5, 0, Math.PI * 2); ctx.fill();
  }
  function drawBoss(ctx) {
    const b = F.b; if (b.gone) return;
    ctx.save(); ctx.translate(b.x + b.knock, b.y); ctx.rotate(b.rot); ctx.scale(F.bs, F.bs);
    try { F.B.draw(ctx, b); } catch (e) { /* un dessin raté ne doit pas casser le combat */ }
    ctx.restore();
    if ((F.phase === "question" || F.phase === "flying") && call("critAllowed").every((v) => v !== false)) {
      const ws = weakWorld(), r = (F.B.hit.coreR + 12) * F.bs;
      ctx.save(); ctx.translate(ws.x, ws.y); ctx.rotate(F.time * 0.8); ctx.setLineDash([6, 6]); ctx.strokeStyle = col(C.lamp, 0.65); ctx.lineWidth = 1.6; ctx.beginPath(); ctx.arc(0, 0, r, 0, Math.PI * 2); ctx.stroke(); ctx.restore();
    }
  }
  function drawTorches(ctx) {
    for (const bx of [F.W * 0.04, F.W * 0.965]) {
      const by = F.groundY - 60;
      const g = ctx.createRadialGradient(bx, by - 14, 4, bx, by - 14, 90); g.addColorStop(0, "rgba(243,184,65,0.22)"); g.addColorStop(1, "rgba(243,184,65,0)");
      ctx.fillStyle = g; ctx.fillRect(bx - 90, by - 104, 180, 180);
      ctx.fillStyle = "#2b3657"; ctx.beginPath(); ctx.moveTo(bx - 14, by); ctx.lineTo(bx + 14, by); ctx.lineTo(bx + 9, by + 9); ctx.lineTo(bx - 9, by + 9); ctx.closePath(); ctx.fill();
      for (let k = 0; k < 3; k++) {
        const fh = 22 + Math.sin(F.time * (9 + k * 3) + k) * 5 - k * 5, fw = 10 - k * 2.5;
        ctx.fillStyle = [C.bad, C.lamp, "#fff1c9"][k];
        ctx.beginPath(); ctx.moveTo(bx - fw, by); ctx.quadraticCurveTo(bx - fw * 0.6, by - fh * 0.6, bx + Math.sin(F.time * 7 + k) * 2, by - fh); ctx.quadraticCurveTo(bx + fw * 0.6, by - fh * 0.6, bx + fw, by); ctx.closePath(); ctx.fill();
      }
    }
  }
  function drawBubble(ctx) {
    const bub = F.bubble; if (!bub || F.b.gone) return;
    const a = Math.min(1, bub.life * 5, (bub.max - bub.life) * 4); if (a <= 0) return;
    ctx.save(); ctx.globalAlpha = a; ctx.font = "600 17px " + F_BODY;
    const words = bub.text.split(" "), lines = []; let line = "";
    const maxW = Math.min(280, F.W * 0.42);
    for (const w of words) { const t = line ? line + " " + w : w; if (ctx.measureText(t).width > maxW && line) { lines.push(line); line = w; } else line = t; }
    if (line) lines.push(line);
    const lw = Math.max(...lines.map((l) => ctx.measureText(l).width)) + 24, lh = lines.length * 22 + 16;
    let x = F.b.x - lw / 2 - 40 * F.bs, y = F.b.y - (F.B.top || 120) * F.bs - lh - 8;
    x = clamp(x, 10, F.W - lw - 10); y = Math.max(10, y);
    ctx.fillStyle = "rgba(232,236,246,0.96)"; rr(ctx, x, y, lw, lh, 10); ctx.fill();
    ctx.beginPath(); ctx.moveTo(x + lw * 0.6, y + lh); ctx.lineTo(x + lw * 0.6 + 14, y + lh); ctx.lineTo(x + lw * 0.6 + 22, y + lh + 14); ctx.closePath(); ctx.fill();
    ctx.fillStyle = C.night; ctx.textAlign = "left"; ctx.textBaseline = "top";
    lines.forEach((l, k) => ctx.fillText(l, x + 12, y + 9 + k * 22));
    ctx.restore();
  }
  function drawTrajectory(ctx) {
    if (!F.drag || F.phase !== "question") return;
    if (Math.hypot(F.pull.x, F.pull.y) < 10) return;
    const scaleP = Math.min(1, ...call("previewScale").map((v) => (v == null ? 1 : v)));
    const P = pouchWorld(); let x = P.x, y = P.y, vx = -F.pull.x * K_LAUNCH, vy = -F.pull.y * K_LAUNCH;
    const dt = 1 / 60, steps = Math.max(12, Math.round(75 * scaleP)), b = F.b, B = F.B, bs = F.bs;
    for (let s = 1; s <= steps; s++) {
      vy += GRAV * dt; x += vx * dt; y += vy * dt;
      if (y > F.groundY) break;
      const dx = x - b.x, dy = y - b.y;
      if (scaleP > 0.6 && (dx * dx) / ((B.hit.rx + 12) ** 2 * bs * bs) + (dy * dy) / ((B.hit.ry + 8) ** 2 * bs * bs) < 1) { ctx.strokeStyle = col(C.lamp, 0.7); ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(x, y, 9, 0, Math.PI * 2); ctx.stroke(); break; }
      if (s % 3 === 0) { ctx.fillStyle = col(C.ink, 0.75 * (1 - s / (steps + 5))); ctx.beginPath(); ctx.arc(x, y, 3, 0, Math.PI * 2); ctx.fill(); }
    }
  }
  function drawTutorial(ctx) {
    if (F.tutDone || F.phase !== "question" || !F.loaded || F.drag || F.time < F.arriveAt) return;
    const P = restPouch(), c = (F.time % 2.2) / 2.2, k = c < 0.7 ? c / 0.7 : 1, hx = P.x - 100 * k, hy = P.y + 46 * k, a = c < 0.85 ? 1 : 1 - (c - 0.85) / 0.15;
    ctx.save(); ctx.globalAlpha = a;
    ctx.setLineDash([5, 6]); ctx.strokeStyle = col(C.lamp, 0.8); ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(P.x, P.y); ctx.lineTo(hx, hy); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle = col(C.ink, 0.9); ctx.beginPath(); ctx.arc(hx, hy, 11, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = col(C.lamp); ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(hx, hy, 16 + 4 * Math.sin(F.time * 8), 0, Math.PI * 2); ctx.stroke();
    ctx.restore();
  }
  function render() {
    const ctx = F.els.ctx, { W, H } = F;
    ctx.setTransform(F.dpr * F.scale, 0, 0, F.dpr * F.scale, 0, 0);
    ctx.clearRect(0, 0, W, H);
    ctx.drawImage(F.els.bg, 0, 0, W, H);
    ctx.save();
    if (F.shakeMag > 0) ctx.translate(rand(-F.shakeMag, F.shakeMag), rand(-F.shakeMag, F.shakeMag));
    for (const s of F.stars) { ctx.fillStyle = "rgba(232,236,246," + (0.25 + 0.6 * Math.abs(Math.sin(F.time * s.s + s.p))) + ")"; ctx.fillRect(s.x, s.y, s.r, s.r); }
    drawTorches(ctx);
    call("draw", ctx, "back");
    drawBoss(ctx);
    call("draw", ctx, "front");
    for (const d of F.debris) { ctx.save(); ctx.translate(d.x, d.y); ctx.rotate(d.rot); ctx.fillStyle = col(d.color); rr(ctx, -d.w / 2 * F.bs, -d.h / 2 * F.bs, d.w * F.bs, d.h * F.bs, 5); ctx.fill(); ctx.restore(); }
    const pal = F.B.palette || {};
    for (const d of F.darts) {
      const dc = F.b.rage ? (pal.rage || C.rage) : (pal.main || C.toxic);
      d.trail.forEach((t, k) => { ctx.fillStyle = col(dc, (k / d.trail.length) * 0.5); ctx.beginPath(); ctx.arc(t.x, t.y, 2 + k * 0.5, 0, Math.PI * 2); ctx.fill(); });
      ctx.save(); ctx.shadowColor = col(dc); ctx.shadowBlur = 16; ctx.fillStyle = "#f8fbff"; ctx.beginPath(); ctx.arc(d.x, d.y, 7, 0, Math.PI * 2); ctx.fill(); ctx.restore();
    }
    drawPlayer(ctx); drawSling(ctx);
    const p = F.proj;
    if (p) {
      p.trail.forEach((t, k) => { ctx.fillStyle = col(p.kind === "inject" ? C.glitch : p.kind === "final" ? C.lamp : C.ink, (k / p.trail.length) * 0.35); ctx.beginPath(); ctx.arc(t.x, t.y, 2 + k * 0.45, 0, Math.PI * 2); ctx.fill(); });
      drawLoad(ctx, p.x, p.y, p.letters, p.kind, p.rot);
    }
    drawTrajectory(ctx); drawTutorial(ctx);
    for (const q of F.particles) {
      const a = 1 - q.life / q.max;
      if (q.kind === "shard") { ctx.save(); ctx.translate(q.x, q.y); ctx.rotate(q.rot); ctx.fillStyle = col(q.color, 0.85 * a); ctx.beginPath(); ctx.moveTo(0, -q.size); ctx.lineTo(q.size * 0.6, q.size * 0.5); ctx.lineTo(-q.size * 0.5, q.size * 0.3); ctx.closePath(); ctx.fill(); ctx.restore(); }
      else if (q.kind === "spark") { ctx.strokeStyle = col(q.color, a); ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(q.x, q.y); ctx.lineTo(q.x - q.vx * 0.04, q.y - q.vy * 0.04); ctx.stroke(); }
      else if (q.kind === "glitch") { ctx.fillStyle = col(q.color, a); ctx.fillRect(q.x, q.y, q.size * 2.2, q.size * 0.7); }
      else if (q.kind === "confetti" || q.kind === "token") { ctx.save(); ctx.translate(q.x, q.y); ctx.rotate(q.rot); ctx.fillStyle = col(q.color, Math.min(1, a * 2)); ctx.fillRect(-q.size / 2, -q.size / 2, q.size, q.kind === "token" ? q.size : q.size / 2); ctx.restore(); }
      else { ctx.fillStyle = col(q.color, a); ctx.beginPath(); ctx.arc(q.x, q.y, q.size, 0, Math.PI * 2); ctx.fill(); }
    }
    for (const t of F.texts) {
      const a = Math.min(1, (t.max - t.life) * 3), sc = t.life < 0.12 ? 0.6 + (t.life / 0.12) * 0.6 : 1.2 - Math.min(0.2, t.life - 0.12);
      ctx.save(); ctx.globalAlpha = a; ctx.translate(t.x, t.y); ctx.scale(sc, sc);
      ctx.font = "800 " + t.size + "px " + F_DISPLAY; ctx.textAlign = "center"; ctx.textBaseline = "middle";
      ctx.lineWidth = 6; ctx.strokeStyle = C.night; ctx.strokeText(t.text, 0, 0); ctx.fillStyle = t.color; ctx.fillText(t.text, 0, 0);
      ctx.restore();
    }
    call("draw", ctx, "overlay");
    drawBubble(ctx);
    ctx.restore();
    if (F.hurtFlash > 0) {
      const g = ctx.createRadialGradient(W / 2, H / 2, Math.min(W, H) * 0.3, W / 2, H / 2, Math.max(W, H) * 0.75);
      g.addColorStop(0, "rgba(239,107,92,0)"); g.addColorStop(1, col(C.bad, 0.5 * F.hurtFlash));
      ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
    }
    if (F.b.rageT > 0) { ctx.fillStyle = col((F.B.palette || {}).rage || C.rage, 0.05 * F.b.rageT); ctx.fillRect(0, 0, W, H); }
  }
  function frame(now) {
    if (!F) return;
    let real = Math.min(0.05, (now - lastFrame) / 1000); lastFrame = now;
    if (F.paused) real = 0;
    let dt = real * F.timeScale;
    if (F.hitStop > 0) { F.hitStop -= real; dt = 0; }
    update(dt, real);
    if (!F) return;
    render();
    raf = requestAnimationFrame(frame);
  }

  /* ---------------- Clavier, pause, reprise ---------------- */
  function onKey(e) {
    if (!F) return false;
    const k = e.key.toLowerCase();
    if (!$("overlay").hidden) return false;
    if (k === "escape") { setPause(!F.paused); return true; }
    if (F.paused) return false;
    if (F.phase === "question") {
      const pos = "abcde".indexOf(k);
      if (pos >= 0 && pos < F.perm.length) { const oi = F.perm[pos]; chooseOption(oi, F.els.stones.querySelector('[data-oi="' + oi + '"]')); return true; }
      if (k === " " || k === "spacebar") { autoShot(); return true; }
    }
    if (F.phase === "feedback" && k === "enter" && document.activeElement && document.activeElement.id !== "next-btn") { next(); return true; }
    return false;
  }
  function onHidden() { if (F && F.phase === "question") setPause(true); }
  function snapshot() {
    if (!F || F.mode !== "boss" || !["question", "flying", "resolving", "feedback"].includes(F.phase)) return null;
    return { n: F.n, ids: F.questions.map((q) => q.id), i: F.i, hearts: F.hearts, hp: F.hp, score: F.score, combo: F.combo, bestCombo: F.bestCombo, crits: F.crits, results: F.results, bonus: F.bonus, phaseIdx: F.phaseIdx, rage: F.b.rage, elapsed: performance.now() - F.t0, advance: F.phase !== "question" && F.phase !== "flying" };
  }
  function resumeFrom(s) {
    F.questions = s.ids.map((id) => QINDEX[id] && QINDEX[id].q).filter(Boolean);
    Object.assign(F, { i: s.i, hearts: s.hearts, prevHearts: s.hearts, hp: s.hp, score: s.score, scoreShown: s.score, combo: s.combo, bestCombo: s.bestCombo, crits: s.crits, results: s.results || [], bonus: s.bonus || 0, t0: performance.now() - (s.elapsed || 0) });
    F.b.hpFrac = F.hp / MAX_HP;
    if (F.B.phases && s.phaseIdx) { F.phaseIdx = s.phaseIdx; F.b.phase = s.phaseIdx; setMods(F.B.phases[s.phaseIdx]); }
    if (s.rage) { F.b.rage = true; F.els["phase-tag"].hidden = false; F.els["phase-tag"].textContent = "Phase " + (F.B.phases ? F.phaseIdx + 1 : 2); F.els["hp-fill"].classList.add("rage"); }
    renderHUD(true);
    if (s.advance && F.hearts > 0 && F.i < F.questions.length - 1) F.i++;
    if (F.hearts <= 0) endFight(false); else startQuestion();
  }

  return { mount, unmount, onKey, onHidden, snapshot, get active() { return !!F; } };
})();
