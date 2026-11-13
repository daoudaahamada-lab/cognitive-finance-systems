/* Moteur d'animation déterministe : l'image affichée dépend uniquement de t (secondes).
 * Aucune transition ni animation CSS : tout est calculé ici, ce qui garantit un rendu
 * image par image identique et synchronisé avec la voix (window.TIMELINE).
 *
 * Attributs reconnus (temps exprimés en "ancres" : beatId, beatId@n (phrase n), beatId$ (fin),
 * suivis d'un décalage optionnel +1.2 / -0.5 ; ou un nombre absolu) :
 *   data-in="p_2+0.5"  data-anim="up|down|left|right|pop|fade|none"  data-dur="0.5"
 *   data-out="p_3"     data-outdur="0.35"
 *   data-cls="p_4+1:active; p_5:-active"        (ajout / retrait de classe)
 *   data-var="p_4:0.8:p:0:1"                    (variable CSS --p animée de 0 à 1 en 0.8 s)
 *   data-type="p_6+0.5:40"                      (machine à écrire, 40 caractères/s)
 *   data-count="a_45:1.5:0:45:0"                (compteur de 0 à 45 en 1,5 s, 0 décimale)
 */
(function () {
  const TL = window.TIMELINE;
  const anchors = {};
  for (const sc of TL.scenes) {
    anchors['scene:' + sc.id] = { start: sc.start, end: sc.end, sentences: [] };
    for (const b of sc.beats) anchors[b.id] = b;
  }

  function T(expr) {
    expr = String(expr).trim();
    if (/^-?\d+(\.\d+)?$/.test(expr)) return parseFloat(expr);
    const m = expr.match(/^([\w:]+)(@(\d+))?(\$)?\s*([+-]\s*\d+(\.\d+)?)?$/);
    if (!m) throw new Error('Ancre invalide : ' + expr);
    const a = anchors[m[1]];
    if (!a) throw new Error('Ancre inconnue : ' + m[1]);
    let base;
    if (m[3] !== undefined) {
      const s = a.sentences[parseInt(m[3], 10)];
      if (!s) throw new Error('Phrase inconnue : ' + expr);
      base = m[4] ? s.end : s.start;
    } else base = m[4] ? a.end : a.start;
    return base + (m[5] ? parseFloat(m[5].replace(/\s/g, '')) : 0);
  }
  window.T = T;

  const ease = {
    out: p => 1 - Math.pow(1 - p, 3),
    inout: p => (p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2),
    lin: p => p,
    back: p => { const c1 = 1.4, c3 = c1 + 1; return 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2); },
  };
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));

  // ---------- pistes ----------
  class Track {
    constructor(el) { this.el = el; this.props = {}; this.cls = []; this.custom = []; }
    key(t, vals, e = 'out') {
      for (const k in vals) (this.props[k] = this.props[k] || []).push({ t, v: vals[k], e });
      return this;
    }
    finalize() {
      for (const k in this.props) this.props[k].sort((a, b) => a.t - b.t);
      this.cls.sort((a, b) => a.t - b.t);
    }
    val(k, t) {
      const ks = this.props[k];
      if (!ks) return undefined;
      if (t <= ks[0].t) return ks[0].v;
      for (let i = 1; i < ks.length; i++) {
        if (t < ks[i].t) {
          const a = ks[i - 1], b = ks[i];
          const p = ease[b.e]((t - a.t) / Math.max(1e-6, b.t - a.t));
          return a.v + (b.v - a.v) * p;
        }
      }
      return ks[ks.length - 1].v;
    }
    apply(t) {
      const el = this.el, st = el.style;
      if (this.props.o) {
        const o = this.val('o', t);
        st.opacity = o.toFixed(3);
        st.visibility = o <= 0.001 ? 'hidden' : 'visible';
      }
      if (this.props.x || this.props.y || this.props.s || this.props.r) {
        const x = this.val('x', t) || 0, y = this.val('y', t) || 0;
        const s = this.props.s ? this.val('s', t) : 1, r = this.val('r', t) || 0;
        st.transform = `translate(${x.toFixed(2)}px,${y.toFixed(2)}px) scale(${s.toFixed(4)}) rotate(${r.toFixed(2)}deg)`;
      }
      if (this.cls.length) {
        const state = {};
        for (const c of this.cls) if (t >= c.t) state[c.name] = c.on;
        for (const name of new Set(this.cls.map(c => c.name))) el.classList.toggle(name, !!state[name]);
      }
      for (const f of this.custom) f(t, el);
    }
  }

  const ANIMS = {
    up: { y: 34 }, down: { y: -34 }, left: { x: 60 }, right: { x: -60 },
    pop: { s: 0.86 }, fade: {}, none: {},
  };

  function parseList(attr) {
    return attr.split(';').map(s => s.trim()).filter(Boolean);
  }

  function buildTrack(el) {
    const tr = new Track(el);
    const d = el.dataset;
    if (d.in !== undefined) {
      const t0 = T(d.in), dur = parseFloat(d.dur || '0.55');
      const a = ANIMS[d.anim || 'up'];
      const from = Object.assign({ o: 0 }, a), to = { o: 1 };
      for (const k in a) to[k] = k === 's' ? 1 : 0;
      if (d.anim === 'none') { tr.key(t0 - 0.001, { o: 0 }, 'lin').key(t0, { o: 1 }, 'lin'); }
      else tr.key(t0, from).key(t0 + dur, to, d.anim === 'pop' ? 'back' : 'out');
    }
    if (d.out !== undefined) {
      const t1 = T(d.out), dur = parseFloat(d.outdur || '0.35');
      if (!tr.props.o) tr.key(t1, { o: 1 });
      tr.key(t1, { o: 1 }, 'lin').key(t1 + dur, { o: 0 }, 'lin');
    }
    if (d.cls) for (const item of parseList(d.cls)) {
      const i = item.lastIndexOf(':');
      const t = T(item.slice(0, i)); let name = item.slice(i + 1).trim(); let on = true;
      if (name.startsWith('-')) { on = false; name = name.slice(1); }
      tr.cls.push({ t, name, on });
    }
    if (d.var) {
      const list = parseList(d.var).map(item => {
        const [te, dur, name, from, to, e] = item.split(':');
        return { t: T(te), dur: parseFloat(dur), name, from: parseFloat(from), to: parseFloat(to), e: e || 'inout' };
      }).sort((a, b) => a.t - b.t);
      // une seule entrée appliquée par variable : la dernière commencée, sinon la première
      const byName = {};
      for (const v of list) (byName[v.name] = byName[v.name] || []).push(v);
      for (const name in byName) {
        const vs = byName[name];
        tr.custom.push((t, el2) => {
          let cur = vs[0];
          for (const v of vs) if (t >= v.t) cur = v;
          const p = ease[cur.e](clamp((t - cur.t) / Math.max(1e-6, cur.dur), 0, 1));
          el2.style.setProperty('--' + name, (cur.from + (cur.to - cur.from) * p).toFixed(4));
        });
      }
    }
    if (d.type) {
      const [te, cps] = d.type.split(':');
      const t0 = T(te), rate = parseFloat(cps || '40');
      const full = el.textContent;
      el.textContent = '';
      tr.custom.push((t, el2) => {
        const n = clamp(Math.floor((t - t0) * rate), 0, full.length);
        el2.textContent = full.slice(0, n);
        el2.classList.toggle('typing', n > 0 && n < full.length);
      });
    }
    if (d.count) {
      const [te, dur, from, to, dec, suffix] = d.count.split(':');
      const t0 = T(te), du = parseFloat(dur), f = parseFloat(from), g = parseFloat(to), nd = parseInt(dec || '0', 10);
      tr.custom.push((t, el2) => {
        const p = ease.out(clamp((t - t0) / du, 0, 1));
        const v = f + (g - f) * p;
        el2.textContent = v.toLocaleString('fr-FR', { minimumFractionDigits: nd, maximumFractionDigits: nd }).replace(/ | /g, ' ') + (suffix || '');
      });
    }
    tr.finalize();
    return tr;
  }

  // ---------- curseur ----------
  function makeCursor(root, steps) {
    // steps : [{t: 'p_1+1', sel: '#btn', click: true, dx, dy}]
    const cur = document.createElement('div');
    cur.className = 'cursor';
    cur.innerHTML = '<svg width="34" height="40" viewBox="0 0 34 40"><path d="M3 2 L3 31 L10.5 24 L15.5 36 L21 33.5 L16 22 L26 22 Z" fill="#fff" stroke="#0F1E33" stroke-width="2.4" stroke-linejoin="round"/></svg><div class="ripple"></div>';
    root.appendChild(cur);
    const pts = steps.map(s => Object.assign({}, s, { t: T(s.t) })).sort((a, b) => a.t - b.t);
    const rootRect = () => root.getBoundingClientRect();
    function posOf(s) {
      const el = root.querySelector(s.sel);
      if (!el) throw new Error('Cible curseur introuvable : ' + s.sel);
      const r = el.getBoundingClientRect(), rr = rootRect();
      return { x: r.left - rr.left + r.width * (s.fx ?? 0.5) + (s.dx || 0), y: r.top - rr.top + r.height * (s.fy ?? 0.55) + (s.dy || 0) };
    }
    return function (t) {
      if (!pts.length || t < pts[0].t - 0.6 || t > pts[pts.length - 1].t + (pts[pts.length - 1].hold || 1.2)) { cur.style.opacity = 0; return; }
      cur.style.opacity = 1;
      let i = 0;
      while (i < pts.length - 1 && t >= pts[i + 1].t) i++;
      let p;
      if (t < pts[0].t) { const a = posOf(pts[0]); p = { x: a.x + 160, y: a.y + 120 }; const k = ease.out(clamp((t - (pts[0].t - 0.6)) / 0.6, 0, 1)); p = { x: p.x + (a.x - p.x) * k, y: p.y + (a.y - p.y) * k }; }
      else if (i < pts.length - 1) {
        const a = posOf(pts[i]), b = posOf(pts[i + 1]);
        const moveStart = Math.max(pts[i].t + 0.25, pts[i + 1].t - (pts[i + 1].move || 0.8));
        const k = ease.inout(clamp((t - moveStart) / Math.max(0.01, pts[i + 1].t - moveStart), 0, 1));
        p = { x: a.x + (b.x - a.x) * k, y: a.y + (b.y - a.y) * k };
      } else p = posOf(pts[i]);
      cur.style.transform = `translate(${p.x - 4}px, ${p.y - 3}px)`;
      // clic
      const rip = cur.querySelector('.ripple');
      let rp = -1;
      for (const s of pts) if (s.click && t >= s.t && t < s.t + 0.5) rp = (t - s.t) / 0.5;
      if (rp >= 0) { rip.style.opacity = (1 - rp).toFixed(3); rip.style.transform = `translate(-50%,-50%) scale(${0.3 + rp * 1.2})`; }
      else rip.style.opacity = 0;
    };
  }

  // ---------- scènes ----------
  const scenes = [];
  const XF = 0.6; // fondu enchaîné entre scènes
  window.registerScene = function (id, builder) {
    const sc = TL.scenes.find(s => s.id === id);
    if (!sc) throw new Error('Scène inconnue ' + id);
    scenes.push({ id, sc, builder });
  };

  let chromeTitle, chromeBar, chromeEl, subEl, subLines;
  window.buildAll = function () {
    const stage = document.getElementById('stage');
    for (const s of scenes) {
      const root = document.createElement('div');
      root.className = 'scene scene-' + s.id;
      stage.appendChild(root);
      const res = s.builder(root, s.sc) || {};
      s.root = root;
      s.cursors = (res.cursors || (res.cursor ? [res.cursor] : [])).map(seq => makeCursor(root, seq));
      s.chrome = res.chrome !== false;
      s.chromeUntil = res.chromeUntil ? T(res.chromeUntil) : Infinity;
      s.tracks = [];
      s.updates = res.update ? [res.update] : [];
    }
    // pistes construites après insertion (les mesures DOM sont alors possibles)
    for (const s of scenes) {
      s.root.querySelectorAll('[data-in],[data-out],[data-cls],[data-var],[data-type],[data-count]').forEach(el => s.tracks.push(buildTrack(el)));
    }
    chromeEl = document.getElementById('chrome');
    chromeTitle = document.getElementById('chrome-title');
    chromeBar = document.getElementById('chrome-progress');
    subEl = document.getElementById('subs');
    subLines = subEl.querySelector('.lines');
  };

  window.render = function (t) {
    let activeChrome = null;
    for (const s of scenes) {
      const a = s.sc.start, b = s.sc.end + XF;
      const vis = t >= a - 0.001 && t < b;
      s.root.style.display = vis ? 'block' : 'none';
      if (!vis) continue;
      let o = 1;
      if (t > s.sc.end) o = 1 - (t - s.sc.end) / XF;
      s.root.style.opacity = o.toFixed(3);
      s.root.style.zIndex = t > s.sc.end ? 1 : 2;
      for (const tr of s.tracks) tr.apply(t);
      for (const f of s.updates) f(t);
      for (const c of s.cursors) c(t);
      if (t <= s.sc.end || !activeChrome) activeChrome = s;
    }
    // bandeau supérieur
    if (activeChrome && activeChrome.chrome && t < activeChrome.chromeUntil) {
      chromeEl.style.opacity = 1;
      chromeTitle.textContent = activeChrome.sc.title;
      const p = clamp((t - activeChrome.sc.start) / (activeChrome.sc.end - activeChrome.sc.start), 0, 1);
      chromeBar.style.width = (p * 100).toFixed(2) + '%';
    } else chromeEl.style.opacity = 0;
    // sous-titres
    let cue = null;
    for (const c of TL.cues) { if (t >= c.start && t < c.end) { cue = c; break; } }
    if (cue) { subEl.style.opacity = 1; subLines.innerHTML = cue.lines.map(l => '<span>' + l.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</span>').join('<br>'); }
    else subEl.style.opacity = 0;
    return true;
  };
})();
