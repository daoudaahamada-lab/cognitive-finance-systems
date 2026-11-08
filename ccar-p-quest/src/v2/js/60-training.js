/* ============================================================
   Entraînement avant le boss : fiches à retourner, « relier », tir aux pigeons.
   ============================================================ */
const ui = { tab: {}, warm: {}, confirm: null, practice: null };

/* ---------- Fiches à retourner ---------- */
function cardsHTML(level) {
  const known = L(level.id).known || [];
  const cards = level.cards.map((c, i) => {
    const k = known.includes(i);
    return '<li class="flip' + (k ? " is-known" : "") + '" data-card="' + i + '">' +
      '<div class="flip-inner">' +
        '<button type="button" class="flip-face flip-front" data-flip="' + i + '" aria-label="Retourner la fiche ' + esc(c.term) + '">' +
          '<span class="eyebrow">Fiche ' + (i + 1) + " / " + level.cards.length + "</span><h3>" + fmt(c.term) + '</h3><span class="flip-cta">' + (k ? "Maîtrisée · retourner" : "Toucher pour retourner") + "</span></button>" +
        '<div class="flip-face flip-back"><h3>' + fmt(c.term) + "</h3><p>" + fmt(c.fr) + '</p><div class="trap"><b>Piège d’examen</b><span>' + fmt(c.trap) + "</span></div>" +
          (c.source && c.source.url ? '<p class="src">Doc officielle : <a href="' + esc(c.source.url) + '" target="_blank" rel="noopener">' + esc(c.source.title) + " ↗</a></p>" : "") +
          '<div class="btn-row"><button type="button" class="btn btn-small btn-ok" data-know="' + i + '">Je sais</button><button type="button" class="btn btn-small" data-again="' + i + '">À revoir</button><button type="button" class="link-btn" data-flip="' + i + '">Retourner</button></div>' +
        "</div></div></li>";
  }).join("");
  return '<p class="tab-intro">Retourne chaque fiche, lis-la, puis classe-la. <strong>' + known.length + " / " + level.cards.length + "</strong> maîtrisée" + (known.length > 1 ? "s" : "") + ".</p>" +
    '<ol class="flips">' + cards + "</ol>" +
    '<div class="tab-foot"><span class="note">Les questions du boss sont en anglais : les termes clés restent en anglais ici.</span><button class="btn btn-primary" type="button" data-action="tab" data-n="' + level.id + '" data-tab="warmup">Passer à l’échauffement →</button></div>';
}
function cardsClick(level, target) {
  const flip = target.closest("[data-flip]");
  if (flip) { const li = flip.closest(".flip"); li.classList.toggle("flipped"); Sound.play("flip"); const front = li.querySelector(".flip-front"); if (!li.classList.contains("flipped")) front.focus({ preventScroll: true }); return true; }
  const know = target.closest("[data-know]"), again = target.closest("[data-again]");
  if (know || again) {
    const i = Number((know || again).dataset.know ?? (know || again).dataset.again), s = lv(level.id);
    s.known = (s.known || []).filter((x) => x !== i); if (know) s.known.push(i);
    s.cardsSeen = true; save(); Sound.play(know ? "match" : "click");
    const li = (know || again).closest(".flip"); li.classList.remove("flipped"); li.classList.toggle("is-known", !!know);
    li.querySelector(".flip-cta").textContent = know ? "Maîtrisée · retourner" : "Toucher pour retourner";
    const p = document.querySelector(".tab-intro strong"); if (p) p.textContent = s.known.length + " / " + level.cards.length;
    return true;
  }
  return false;
}

/* ---------- Échauffement : relier puis tir aux pigeons ---------- */
const STOP = new Set(["and", "the", "of", "with", "for", "vs", "les", "des", "and/or", "via", "a", "an", "to", "in", "on"]);
function maskedDefinition(card) {
  let first = (card.fr.match(/^.*?[.!?](\s|$)/) || [card.fr])[0].trim();
  if (first.length < 60) { const two = card.fr.match(/^(.*?[.!?]\s){2}/); if (two) first = two[0].trim(); }
  if (first.length > 190) first = first.slice(0, 186).replace(/\s+\S*$/, "") + "…";
  const tokens = card.term.split(/[^A-Za-zÀ-ÿ0-9-]+/).filter((t) => t && !STOP.has(t.toLowerCase()) && (t.length >= 4 || /^[A-Z0-9]{2,}$/.test(t)));
  for (const t of tokens) first = first.replace(new RegExp("\\b" + t.replace(/[-]/g, "\\-") + "s?\\b", "gi"), "▢▢▢");
  return first;
}
function warmState(n) {
  const level = byId(n);
  if (!ui.warm[n]) ui.warm[n] = {
    stage: "match",
    match: { order: shuffle(level.cards.map((_, i) => i)), done: [], pick: null, mistakes: 0 },
    pig: { i: 0, picks: [], revealed: false, key: 0 }
  };
  return ui.warm[n];
}
function warmupHTML(level) {
  const w = warmState(level.id);
  const steps = '<div class="warm-steps"><span class="' + (w.stage === "match" ? "now" : "done") + '">1. Relier les notions</span><span class="' + (w.stage === "pigeons" ? "now" : w.stage === "done" ? "done" : "") + '">2. Tir aux pigeons</span></div>';
  if (w.stage === "match") return steps + matchHTML(level, w);
  if (w.stage === "pigeons") return steps + pigeonHTML(level, w);
  const score = level.warmup.filter((x, i) => w.pig.picks[i] === x.answer).length;
  return steps + '<div class="drill"><h2 class="section-title">Échauffement terminé</h2>' +
    '<dl class="stats"><div><dt>Relier</dt><dd>' + (w.match.mistakes === 0 ? "Parfait" : plural(w.match.mistakes, "erreur")) + "</dd></div><div><dt>Pigeons</dt><dd>" + score + " / " + level.warmup.length + "</dd></div></dl>" +
    '<p class="lede">' + (score >= 4 && w.match.mistakes <= 1 ? "Bonne base. Le boss t’attend." : "Relis les fiches sur les points ratés avant d’affronter le boss.") + "</p>" +
    '<div class="btn-row"><button class="btn btn-primary" type="button" data-action="tab" data-n="' + level.id + '" data-tab="boss">Affronter le boss →</button><button class="btn" type="button" data-action="warm-restart" data-n="' + level.id + '">Recommencer</button><button class="btn" type="button" data-action="tab" data-n="' + level.id + '" data-tab="cards">Revoir les fiches</button></div></div>';
}
function matchHTML(level, w) {
  const m = w.match;
  const terms = level.cards.map((c, i) => '<button type="button" class="term' + (m.done.includes(i) ? " matched" : "") + (m.pick === i ? " picked" : "") + '" data-term="' + i + '"' + (m.done.includes(i) ? " disabled" : "") + ">" + fmt(c.term) + "</button>").join("");
  const defs = m.order.map((i) => '<li><button type="button" class="def' + (m.done.includes(i) ? " matched" : "") + '" data-def="' + i + '"' + (m.done.includes(i) ? " disabled" : "") + ">" + (m.done.includes(i) ? '<b class="def-term">' + fmt(level.cards[i].term) + "</b>" : "") + "<span>" + fmt(maskedDefinition(level.cards[i])) + "</span></button></li>").join("");
  return '<div class="match"><p class="tab-intro">Touche une notion, puis la définition qui lui correspond. ' + m.done.length + " / " + level.cards.length + (m.mistakes ? " · " + plural(m.mistakes, "erreur") : "") + "</p>" +
    '<div class="terms" role="group" aria-label="Notions">' + terms + '</div><ol class="defs">' + defs + "</ol></div>";
}
function matchClick(level, target) {
  const w = warmState(level.id), m = w.match;
  const t = target.closest("[data-term]"), d = target.closest("[data-def]");
  if (t && !t.disabled) { m.pick = Number(t.dataset.term); Sound.play("click"); rerenderWarm(level); return true; }
  if (d && !d.disabled) {
    if (m.pick == null) { const terms = document.querySelector(".terms"); if (terms) { terms.classList.remove("nudge"); void terms.offsetWidth; terms.classList.add("nudge"); } return true; }
    const i = Number(d.dataset.def);
    if (i === m.pick) {
      m.done.push(i); m.pick = null; Sound.play("match");
      if (m.done.length === level.cards.length) { Sound.play("win"); setTimeout(() => { w.stage = "pigeons"; rerenderWarm(level); }, 700); }
      rerenderWarm(level);
    } else {
      m.mistakes++; Sound.play("nomatch");
      d.classList.remove("wrong"); void d.offsetWidth; d.classList.add("wrong");
      const p = document.querySelector(".match .tab-intro"); if (p) p.textContent = "Touche une notion, puis la définition qui lui correspond. " + m.done.length + " / " + level.cards.length + " · " + plural(m.mistakes, "erreur");
    }
    return true;
  }
  return false;
}
function pigeonHTML(level, w) {
  const p = w.pig, items = level.warmup, x = items[p.i];
  const dots = items.map((it, i) => { const pk = p.picks[i]; return '<i class="' + (pk == null ? (i === p.i ? "now" : "") : (pk === it.answer ? "done-ok" : "done-bad")) + '"></i>'; }).join("");
  let body;
  if (!p.revealed) {
    body = '<div class="range" id="range"><div class="disc-track" style="animation-duration:' + (reduceMotion ? 0 : 13) + 's" data-key="' + p.key + '"><button type="button" class="disc" data-shoot="1" aria-label="Tirer : l’affirmation est vraie"><span></span></button></div><span class="range-label">Tire si c’est vrai. Laisse passer si c’est faux.</span></div>' +
      '<div class="tf"><button class="btn btn-primary" type="button" data-shoot="1">Tirer · vrai <kbd>V</kbd></button><button class="btn" type="button" data-pass="1">Laisser passer · faux <kbd>F</kbd></button></div>';
  } else {
    const pk = p.picks[p.i], ok = pk === x.answer;
    body = '<div class="feedback ' + (ok ? "good" : "bad") + '"><h3>' + (ok ? (pk ? "Pigeon abattu, c’était vrai" : "Bien vu, c’était faux") : (pk ? "Raté : c’était faux" : "Il fallait tirer : c’était vrai")) + "</h3><p>" + fmt(x.fr) + '</p><div class="btn-row"><button class="btn btn-primary" type="button" data-pig-next="1" id="pig-next">' + (p.i === items.length - 1 ? "Voir le bilan" : "Pigeon suivant") + " → <kbd>Entrée</kbd></button></div></div>";
  }
  return '<div class="drill"><div class="dots">' + dots + '</div><p class="eyebrow">Pigeon ' + (p.i + 1) + " / " + items.length + '</p><p class="statement" lang="en">' + fmt(x.statement) + "</p>" + body + "</div>";
}
function pigeonAnswer(level, val, fromDisc) {
  const w = warmState(level.id), p = w.pig;
  if (p.revealed || w.stage !== "pigeons") return;
  p.picks[p.i] = val; p.revealed = true;
  const disc = document.querySelector(".disc"), track = document.querySelector(".disc-track");
  if (val && disc && track) {
    track.style.animationPlayState = "paused";
    const r = disc.getBoundingClientRect(), range = document.getElementById("range").getBoundingClientRect();
    disc.classList.add("hit"); Sound.play("pop");
    for (let k = 0; k < 12; k++) {
      const s = document.createElement("i"); s.className = "shard";
      s.style.left = r.left - range.left + r.width / 2 + "px"; s.style.top = r.top - range.top + r.height / 2 + "px";
      document.getElementById("range").appendChild(s);
      const a = Math.random() * Math.PI * 2, d = 30 + Math.random() * 60;
      requestAnimationFrame(() => { s.style.transform = "translate(" + Math.cos(a) * d + "px," + Math.sin(a) * d + "px) rotate(" + (Math.random() * 360) + "deg)"; s.style.opacity = "0"; });
    }
    setTimeout(() => rerenderWarm(level), reduceMotion ? 0 : 450);
  } else { Sound.play(val ? "click" : "whoosh"); rerenderWarm(level); }
  const ok = val === level.warmup[p.i].answer;
  setTimeout(() => Sound.play(ok ? "match" : "nomatch"), 200);
}
function pigeonNext(level) {
  const w = warmState(level.id), p = w.pig;
  if (!p.revealed) return;
  p.i++; p.revealed = false; p.key++;
  if (p.i >= level.warmup.length) {
    w.stage = "done";
    const score = level.warmup.filter((x, i) => p.picks[i] === x.answer).length, s = lv(level.id);
    s.warmupDone = true; s.warmupBest = Math.max(s.warmupBest || 0, score); save();
  }
  rerenderWarm(level);
}
function warmupClick(level, target) {
  const w = warmState(level.id);
  if (w.stage === "match") return matchClick(level, target);
  if (w.stage === "pigeons") {
    if (target.closest("[data-shoot]")) { pigeonAnswer(level, true); return true; }
    if (target.closest("[data-pass]")) { pigeonAnswer(level, false); return true; }
    if (target.closest("[data-pig-next]")) { pigeonNext(level); return true; }
  }
  return false;
}
function warmupKey(level, e) {
  const w = warmState(level.id), k = e.key.toLowerCase();
  if (w.stage !== "pigeons") return false;
  if (!w.pig.revealed && (k === "v" || k === "f")) { pigeonAnswer(level, k === "v"); return true; }
  if (w.pig.revealed && k === "enter" && document.activeElement && document.activeElement.id !== "pig-next") { pigeonNext(level); return true; }
  return false;
}
/** Le pigeon sort de l'écran sans tir : c'est « laisser passer ». */
document.addEventListener("animationend", (e) => {
  if (!e.target.classList || !e.target.classList.contains("disc-track")) return;
  const m = location.hash.match(/^#etage-(\d+)$/); if (!m) return;
  const level = byId(Number(m[1])), w = level && ui.warm[level.id];
  if (w && w.stage === "pigeons" && !w.pig.revealed && Number(e.target.dataset.key) === w.pig.key) pigeonAnswer(level, false);
});
function rerenderWarm(level) {
  const panel = document.getElementById("tabpanel");
  if (!panel) return;
  panel.innerHTML = warmupHTML(level);
  const nextBtn = document.getElementById("pig-next"); if (nextBtn) nextBtn.focus({ preventScroll: true });
  if (typeof renderSteps === "function") renderSteps(level);
}
