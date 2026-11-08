/* ============================================================
   Tour de l'Architecte V2 — socle commun
   Tous les fichiers js/ sont concaténés dans un seul scope par scripts/build.mjs.
   ============================================================ */
"use strict";

/* ---------- Données ---------- */
const LEVELS = (window.__LEVELS__ || []).slice().sort((a, b) => a.id - b.id);
const DOMAINS = {
  D1: { name: "Solution Design & Architecture", short: "Design", weight: 17 },
  D2: { name: "Claude Models, Prompting & Context Engineering", short: "Models & Prompting", weight: 13 },
  D3: { name: "Integration", short: "Integration", weight: 19 },
  D4: { name: "Evaluation, Testing & Optimization", short: "Evaluation", weight: 16 },
  D5: { name: "Governance, Safety & Risk Management", short: "Governance", weight: 14 },
  D6: { name: "Stakeholder Communication & Lifecycle Management", short: "Stakeholders", weight: 14 },
  D7: { name: "Developer Productivity & Operational Enablement", short: "Dev Productivity", weight: 7 }
};
const QINDEX = {};
LEVELS.forEach((l) => l.questions.forEach((q) => { QINDEX[q.id] = { q, level: l }; }));
const byId = (n) => LEVELS.find((l) => l.id === n) || null;

/* ---------- Règles du jeu ---------- */
const HEARTS = 3, MAX_HP = 100, PASS = 0.72;
const K_LAUNCH = 7, MAX_PULL = 150, GRAV = 900;
const EXAM_S = Math.round(120 * 60 / 63);                                   // 114 s par question à l'examen
const secondsFor = (n) => Math.round(EXAM_S * (1 + 0.9 * (10 - n) / 9));    // barre progressive : 217 s à l'étage 1, 114 s au sommet
const LETTERS = "ABCDE";
const STORE_KEY = "ccarp-quest-v1";

/* ---------- Registres (remplis par les autres fichiers) ---------- */
const BOSSES = {};   // BOSSES[n] : apparence et répliques du boss de l'étage n (voir BOSS_API.md)
const MECH = {};     // MECH[nom] : mécaniques de combat (brouillard, tourelles, injection…)

/* ---------- Utilitaires ---------- */
const $ = (id) => document.getElementById(id);
const reduceMotion = !!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const lerp = (a, b, t) => a + (b - a) * t;
const rand = (a, b) => a + Math.random() * (b - a);
const pick = (a) => a[Math.floor(Math.random() * a.length)];
const shuffle = (a) => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const sameSet = (a, b) => a.length === b.length && a.every((x) => b.includes(x));
const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const fmt = (s) => esc(s).replace(/`([^`]+)`/g, "<code>$1</code>");
const stemHTML = (s) => fmt(s).replace(/\(Select TWO\.\)\s*$/, '<span class="select-two">(Select TWO.)</span>');
const unquote = (s) => String(s || "").replace(/^[\s«"“]+|[\s»"”]+$/g, "");
const pad = (n) => (n < 10 ? "0" : "") + n;
const fmtMS = (sec) => { sec = Math.max(0, Math.ceil(sec)); return Math.floor(sec / 60) + ":" + String(sec % 60).padStart(2, "0"); };
const plural = (n, word) => n + " " + word + (n > 1 ? "s" : "");

/* Couleurs : les jetons CSS sont lus une fois, puis mélangés pour le canvas. */
const cssTok = getComputedStyle(document.documentElement);
const tok = (n, fallback) => (cssTok.getPropertyValue(n) || "").trim() || fallback;
const C = {
  night: tok("--night", "#0c111e"), slab: tok("--slab", "#141b2d"), slab2: tok("--slab-2", "#1c2541"), line: tok("--line", "#2b3657"),
  ink: tok("--ink", "#e8ecf6"), muted: tok("--muted", "#9aa5c3"), lamp: tok("--lamp", "#f3b841"), ok: tok("--ok", "#57c48f"), bad: tok("--bad", "#ef6b5c"),
  toxic: tok("--toxic", "#62f0a6"), rage: tok("--rage", "#ff4f9a"), glitch: tok("--glitch", "#b38cff"), white: "#ffffff",
  coat: "#33406b", skin: "#eec7a0", rubber: "#d9774b", wood: "#7a5a3f", metal: "#9aa5c3"
};
const F_DISPLAY = '"Big Shoulders Display", "Arial Narrow", sans-serif';
const F_MONO = '"JetBrains Mono", ui-monospace, monospace';
const F_BODY = '"Source Sans 3", "Segoe UI", system-ui, sans-serif';
const rgbCache = {};
function rgb(hex) {
  if (Array.isArray(hex)) return hex;
  if (rgbCache[hex]) return rgbCache[hex];
  let h = String(hex).replace("#", ""); if (h.length === 3) h = h.split("").map((c) => c + c).join("");
  const n = parseInt(h, 16);
  return (rgbCache[hex] = [(n >> 16) & 255, (n >> 8) & 255, n & 255]);
}
/** Mélange deux couleurs (hex ou [r,g,b]) et renvoie [r,g,b]. */
const mixv = (a, b, t) => { const A = rgb(a), B = rgb(b); t = clamp(t, 0, 1); return [A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t, A[2] + (B[2] - A[2]) * t]; };
/** Couleur CSS rgba à partir d'un hex ou d'un [r,g,b]. */
const col = (c, al = 1) => { const v = rgb(c); return "rgba(" + (v[0] | 0) + "," + (v[1] | 0) + "," + (v[2] | 0) + "," + al + ")"; };
function seeded(seed) { return () => { seed |= 0; seed = (seed + 0x6d2b79f5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
/** Trace un rectangle arrondi (sans le remplir). */
function rr(c, x, y, w, h, r) { r = Math.min(r, w / 2, h / 2); c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); }
function elbow(s, h, l1, l2, flip) {
  const dx = h.x - s.x, dy = h.y - s.y, d = Math.max(1, Math.hypot(dx, dy)), dd = Math.min(d, l1 + l2 - 0.01);
  const a = Math.atan2(dy, dx), ang = Math.acos(clamp((l1 * l1 + dd * dd - l2 * l2) / (2 * l1 * dd), -1, 1)), e = a + (flip ? -ang : ang);
  return { x: s.x + Math.cos(e) * l1, y: s.y + Math.sin(e) * l1 };
}
/** Dessine les fissures d'impact accumulées sur le boss (coordonnées locales). */
function drawCracks(c, b, color, width) {
  if (!b.cracks || !b.cracks.length) return;
  c.save(); c.strokeStyle = color || "rgba(235,244,255,0.85)"; c.lineWidth = width || 1.6; c.lineCap = "round"; c.lineJoin = "round";
  for (const k of b.cracks) { c.beginPath(); c.moveTo(k[0][0], k[0][1]); for (let i = 1; i < k.length; i++) c.lineTo(k[i][0], k[i][1]); c.stroke(); }
  c.restore();
}
/** Yeux fendus en colère, utilisés par plusieurs boss. */
function angryEyes(c, x, y, w, h, color, squint, glow) {
  const sq = 1 - (squint || 0) * 0.75;
  c.save(); if (glow) { c.shadowColor = col(color); c.shadowBlur = glow; }
  c.fillStyle = col(color);
  c.beginPath(); c.moveTo(-x - w, y - h * 0.8); c.lineTo(-x, y); c.lineTo(-x, y + h * sq); c.lineTo(-x - w, y - h * 0.8 + h * sq); c.closePath(); c.fill();
  c.beginPath(); c.moveTo(x + w, y - h * 0.8); c.lineTo(x, y); c.lineTo(x, y + h * sq); c.lineTo(x + w, y - h * 0.8 + h * sq); c.closePath(); c.fill();
  c.restore();
}

/* ---------- Progression (navigateur + compte Claude) ---------- */
function blankState() { return { v: 2, updatedAt: 0, levels: {}, domains: {}, review: {}, unlockAll: false, settings: { sound: true }, seenTutorial: false }; }
function normalize(s) {
  const b = blankState();
  if (!s || typeof s !== "object") return b;
  b.updatedAt = Number(s.updatedAt) || 0;
  b.levels = s.levels && typeof s.levels === "object" ? s.levels : {};
  b.domains = s.domains && typeof s.domains === "object" ? s.domains : {};
  b.review = s.review && typeof s.review === "object" ? s.review : {};
  b.unlockAll = !!s.unlockAll;
  b.settings = Object.assign({ sound: true }, s.settings || {});
  b.seenTutorial = !!s.seenTutorial;
  return b;
}
function readLocal() { try { const raw = localStorage.getItem(STORE_KEY); return raw ? normalize(JSON.parse(raw)) : null; } catch (e) { return null; } }
function writeLocal(s) { try { localStorage.setItem(STORE_KEY, JSON.stringify(s)); } catch (e) { /* stockage indisponible */ } }

let state = readLocal() || blankState();
const sync = { ref: null, writing: false, pending: false, timer: null };
let onStateReplaced = () => {};

function save() { state.updatedAt = Date.now(); writeLocal(state); queueRemote(); if (typeof renderNav === "function") renderNav(); }
function queueRemote() { if (!sync.ref) return; clearTimeout(sync.timer); sync.timer = setTimeout(flushRemote, 1200); }
function flushRemote() {
  if (!sync.ref) return;
  if (sync.writing) { sync.pending = true; return; }
  sync.writing = true;
  sync.ref.set({ state: JSON.stringify(state), updatedAt: state.updatedAt })
    .then(() => setSync("cloud"))
    .catch(() => { sync.ref = null; setSync("local"); })
    .then(() => { sync.writing = false; if (sync.pending) { sync.pending = false; flushRemote(); } });
}
function setSync(mode) {
  const el = $("sync-status"); if (!el) return;
  el.innerHTML = mode === "cloud"
    ? '<span class="sync-dot cloud"></span>Progression synchronisée avec ton compte Claude'
    : '<span class="sync-dot"></span>Progression enregistrée dans ce navigateur';
}
function initRemote() {
  const c = window.claude;
  if (!c || typeof c.use !== "function") return;
  Promise.all([c.use("db"), c.use("user")]).then(([db, user]) => {
    if (!db || !user) return null;
    return user.id().then((id) => {
      if (!id) return null;
      const ref = db.doc("data/users/" + id + "/progress");
      const timeout = new Promise((_, reject) => setTimeout(() => reject(new Error("timeout")), 10000));
      return Promise.race([ref.get(), timeout]).then((snap) => {
        sync.ref = ref;
        let remote = null;
        if (snap.exists) { try { remote = normalize(JSON.parse(snap.data().state)); } catch (e) { remote = null; } }
        if (remote && remote.updatedAt > state.updatedAt) { state = remote; writeLocal(state); setSync("cloud"); onStateReplaced(); }
        else if (state.updatedAt > 0 && (!remote || remote.updatedAt < state.updatedAt)) flushRemote();
        else setSync("cloud");
      });
    });
  }).catch(() => { /* reste en local */ });
}

const L = (n) => state.levels[n] || {};
const lv = (n) => state.levels[n] || (state.levels[n] = {});
const isUnlocked = (n) => state.unlockAll || n === 1 || !!L(n - 1).won;
const bossReady = (n) => isUnlocked(n) && (state.unlockAll || !!L(n).warmupDone);
const currentFloor = () => { for (const l of LEVELS) if (isUnlocked(l.id) && !L(l.id).won) return l.id; return null; };
const reviewIds = () => Object.keys(state.review).filter((id) => QINDEX[id]);
function recordAnswer(q, ok, fromReview) {
  const d = state.domains[q.domain] || (state.domains[q.domain] = { seen: 0, ok: 0 });
  d.seen++; if (ok) d.ok++;
  if (!ok) { const r = state.review[q.id] || (state.review[q.id] = { misses: 0 }); r.misses++; r.at = Date.now(); }
  else if (fromReview) delete state.review[q.id];
}
