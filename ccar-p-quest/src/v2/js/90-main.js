/* ============================================================
   Navigation, actions et démarrage.
   Routes : #tour, #etage-N, #combat-N, #revisions, #entrainement
   ============================================================ */
function go(hash) { if (location.hash === "#" + hash) render(); else location.hash = hash; }
function route() {
  const h = location.hash.replace(/^#/, ""); let m;
  if ((m = h.match(/^etage-(\d+)$/))) return { view: "level", n: +m[1] };
  if ((m = h.match(/^combat-(\d+)$/))) return { view: "fight", n: +m[1] };
  if (h === "revisions") return { view: "review" };
  if (h === "entrainement") return { view: "practice" };
  return { view: "home" };
}
function startFight(n, resume) {
  return Arena.mount({
    mode: "boss", n, resume,
    onExit: () => { ui.tab[n] = "boss"; go("etage-" + n); },
    onEnd: (r) => {
      if (r.action === "next" && byId(n + 1)) { elevator(n, n + 1, () => { ui.tab[n + 1] = null; go("etage-" + (n + 1)); }); }
      else if (r.action === "cards") { ui.tab[n] = "cards"; go("etage-" + n); }
      else go("tour");
    }
  });
}
function startPractice() {
  const p = ui.practice;
  if (!p || !p.queue.length) { go("revisions"); return; }
  const back = p.kind === "free" ? "etage-" + p.n : "revisions";
  Arena.mount({
    mode: "practice", practiceKind: p.kind, n: p.n || 0, queue: p.queue, title: p.title,
    onExit: () => { ui.practice = null; go(back); },
    onEnd: (r) => {
      ui.practice = null;
      if (r.action === "review") { openReview(); return; }
      go(back);
    }
  });
}
function openReview() {
  const queue = reviewIds().sort((a, b) => (state.review[b].misses || 0) - (state.review[a].misses || 0)).slice(0, 12);
  if (!queue.length) { go("revisions"); return; }
  ui.practice = { kind: "review", queue, title: "Salle de révision" };
  go("entrainement");
}
function render() {
  const r = route();
  if (r.view !== "fight" && r.view !== "practice") Arena.unmount();
  if (r.view === "level") renderLevel(r.n);
  else if (r.view === "fight") {
    if (!bossReady(r.n)) { ui.tab[r.n] = isUnlocked(r.n) ? "warmup" : null; go(isUnlocked(r.n) ? "etage-" + r.n : "tour"); return; }
    startFight(r.n, pendingResume && pendingResume.n === r.n ? pendingResume : null);
    pendingResume = null;
  }
  else if (r.view === "review") renderReview();
  else if (r.view === "practice") startPractice();
  else renderHome();
  renderNav(); renderConfirm();
}
let pendingResume = null;
onStateReplaced = () => { if (!Arena.active) render(); else renderNav(); };
window.addEventListener("hashchange", () => { render(); window.scrollTo(0, 0); });

/* ---------- Actions (boutons data-action) ---------- */
const actions = {
  tab(d) { const n = +d.n, level = byId(n); if (d.tab === "boss" && !bossReady(n)) return; ui.tab[n] = d.tab; renderLevel(n); },
  "warm-restart"(d) { ui.warm[+d.n] = null; ui.tab[+d.n] = "warmup"; renderLevel(+d.n); },
  "start-free"(d) { const level = byId(+d.n); ui.practice = { kind: "free", n: level.id, queue: shuffle(level.questions.map((q) => q.id)), title: "Mode libre · Étage " + pad(level.id) }; go("entrainement"); },
  "start-review"() { openReview(); },
  "ask-reset"() { ui.confirm = "reset"; renderConfirm(); },
  "ask-unlock"() { if (state.unlockAll) { state.unlockAll = false; save(); render(); } else { ui.confirm = "unlock"; renderConfirm(); } },
  "cancel-confirm"() { ui.confirm = null; renderConfirm(); },
  "do-reset"() { state = blankState(); state.updatedAt = Date.now(); ui.tab = {}; ui.warm = {}; ui.confirm = null; ui.practice = null; writeLocal(state); queueRemote(); go("tour"); },
  "do-unlock"() { state.unlockAll = true; ui.confirm = null; save(); render(); },
  sound() { Sound.toggle(); renderNav(); }
};
document.addEventListener("click", (e) => {
  const r = route();
  if (r.view === "level") {
    const level = byId(r.n), panel = document.getElementById("tabpanel");
    if (level && panel && panel.contains(e.target)) {
      const tab = ui.tab[r.n];
      if (tab === "cards" && cardsClick(level, e.target)) { renderSteps(level); return; }
      if (tab === "warmup" && warmupClick(level, e.target)) return;
    }
  }
  const t = e.target.closest("[data-action]");
  if (!t || t.disabled) return;
  const fn = actions[t.getAttribute("data-action")];
  if (fn) { e.preventDefault(); Sound.ensure(); fn(t.dataset); }
});
document.addEventListener("keydown", (e) => {
  if (e.metaKey || e.ctrlKey || e.altKey) return;
  const tag = (e.target && e.target.tagName) || "";
  if (tag === "INPUT" || tag === "TEXTAREA") return;
  if (Arena.active) { if (Arena.onKey(e)) e.preventDefault(); return; }
  const r = route();
  if (r.view === "level" && ui.tab[r.n] === "warmup") { const level = byId(r.n); if (level && warmupKey(level, e)) e.preventDefault(); }
});
document.addEventListener("visibilitychange", () => { if (document.hidden) Arena.onHidden(); });

/* ---------- Démarrage (avec reprise après une republication) ---------- */
try {
  if (window.claude && window.claude.hot && window.claude.hot.snapshot) window.claude.hot.snapshot(() => ({ fight: Arena.snapshot(), ui: { tab: ui.tab } }));
} catch (e) { /* hors visionneuse */ }
function boot(data) {
  if (data && data.ui && data.ui.tab) ui.tab = data.ui.tab;
  if (data && data.fight) pendingResume = data.fight;
  setSync("local");
  render();
  initRemote();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => { if (!Arena.active) Thumbs.scan(); });
}
const hot = window.claude && window.claude.hot;
if (hot && hot.ready) hot.ready(boot); else boot((hot && hot.data) || {});
