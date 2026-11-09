/* ============================================================
   Musique de combat générée dans la page (Web Audio, aucun fichier).
   Une boucle de 16 pas par boss : basse, arpège, percussions.
   Elle s'allège pendant la lecture et s'intensifie avec l'action et la rage.
   ============================================================ */
const Music = (() => {
  const SCALES = { minor: [0, 2, 3, 5, 7, 8, 10], dorian: [0, 2, 3, 5, 7, 9, 10], phrygian: [0, 1, 3, 5, 7, 8, 10], harmonic: [0, 2, 3, 5, 7, 8, 11] };
  const DRUMS = {
    steady: { kick: [0, 8], snare: [4, 12], hat: [2, 6, 10, 14] },
    four: { kick: [0, 4, 8, 12], snare: [4, 12], hat: [2, 6, 10, 14] },
    broken: { kick: [0, 3, 8, 11], snare: [4, 12], hat: [2, 6, 10, 14, 15] },
    heavy: { kick: [0, 10], snare: [8], hat: [4, 12] }
  };
  const _ = null;
  /* Notes en degrés de gamme (0 = fondamentale, 7 = octave au-dessus) ; _ = silence. */
  const TRACKS = {
    1: { bpm: 86, root: 45, scale: "dorian", drums: "steady", bass: [0, _, _, _, 0, _, _, 4, 0, _, _, _, 3, _, _, _], arp: [7, _, _, 9, _, _, 11, _, _, 9, _, _, 8, _, 7, _] },
    2: { bpm: 112, root: 40, scale: "minor", drums: "four", bass: [0, _, 0, _, 0, _, 3, _, 4, _, 4, _, 6, _, 4, _], arp: [7, 9, 11, 9, 7, 9, 11, 14, 7, 9, 11, 9, 10, 9, 7, 4] },
    3: { bpm: 104, root: 38, scale: "phrygian", drums: "broken", bass: [0, _, _, 0, _, _, 1, _, 0, _, _, 0, _, 4, _, 1], arp: [7, _, 8, _, _, 11, _, 8, 7, _, _, 12, _, 11, 8, _] },
    4: { bpm: 96, root: 41, scale: "harmonic", drums: "steady", bass: [0, _, _, 0, _, 2, _, _, 4, _, _, 5, _, 4, _, 2], arp: [7, _, 9, 10, _, 9, _, 13, 11, _, 9, 10, _, 9, _, 6] },
    5: { bpm: 118, root: 43, scale: "dorian", drums: "four", bass: [0, _, 7, _, 0, _, 7, _, 3, _, 10, _, 4, _, 11, _], arp: [_, _, 9, _, _, 11, _, 9, _, _, 12, _, _, 11, 9, _] },
    6: { bpm: 80, root: 36, scale: "phrygian", drums: "heavy", bass: [0, _, _, _, _, _, 0, _, 1, _, _, _, _, _, 0, _], arp: [7, _, _, _, 8, _, _, _, 7, _, _, _, 11, _, 8, _] },
    7: { bpm: 108, root: 35, scale: "harmonic", drums: "broken", bass: [0, _, 0, _, _, 0, _, 5, 0, _, 0, _, _, 6, _, 4], arp: [7, _, 13, _, 11, _, 9, _, 7, _, 13, _, 12, 11, 9, _] },
    8: { bpm: 100, root: 46, scale: "dorian", drums: "steady", bass: [0, _, _, 4, _, _, 0, _, 3, _, _, 5, _, _, 4, _], arp: [9, _, 11, _, 12, _, 11, _, 9, _, 7, _, 9, 11, _, _] },
    9: { bpm: 126, root: 40, scale: "phrygian", drums: "broken", bass: [0, 0, _, 0, _, 1, _, 0, 0, 0, _, 3, _, 1, _, 0], arp: [7, _, 8, 7, _, 11, _, 8, 7, _, 8, 7, _, 12, 11, 8] },
    10: { bpm: 92, root: 38, scale: "harmonic", drums: "steady", bass: [0, _, _, _, 0, _, 4, _, 5, _, _, _, 4, _, 2, _], arp: [7, _, 9, _, 11, _, 13, _, 14, _, 13, _, 11, _, 9, _] }
  };
  let ctx = null, out = null, timer = null, step = 0, nextT = 0, t0 = 0, track = null, level = 1, duck = 1, noiseBuf = null;
  const enabled = () => state.settings.sound !== false && state.settings.music !== false;
  const hz = (m) => 440 * Math.pow(2, (m - 69) / 12);
  const note = (deg) => track.root + 12 * Math.floor(deg / 7) + SCALES[track.scale][((deg % 7) + 7) % 7];
  function tone(type, f, t, dur, vol, cutoff) {
    const o = ctx.createOscillator(), g = ctx.createGain(), lp = ctx.createBiquadFilter();
    o.type = type; o.frequency.setValueAtTime(f, t); lp.type = "lowpass"; lp.frequency.setValueAtTime(cutoff, t);
    g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(vol, t + 0.012); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    o.connect(lp); lp.connect(g); g.connect(out); o.start(t); o.stop(t + dur + 0.03);
  }
  function kick(t, vol) {
    const o = ctx.createOscillator(), g = ctx.createGain();
    o.frequency.setValueAtTime(130, t); o.frequency.exponentialRampToValueAtTime(42, t + 0.13);
    g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.17);
    o.connect(g); g.connect(out); o.start(t); o.stop(t + 0.2);
  }
  function noise(t, dur, vol, type, freq) {
    if (!noiseBuf) { noiseBuf = ctx.createBuffer(1, ctx.sampleRate, ctx.sampleRate); const d = noiseBuf.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1; }
    const s = ctx.createBufferSource(), f = ctx.createBiquadFilter(), g = ctx.createGain();
    s.buffer = noiseBuf; f.type = type; f.frequency.value = freq;
    g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    s.connect(f); f.connect(g); g.connect(out); s.start(t, Math.random() * 0.5); s.stop(t + dur + 0.03);
  }
  /* Niveaux : 0 lecture de l'explication, 1 question, 2 action ou danger, 3 rage. */
  function schedule(s, t) {
    const d = DRUMS[track.drums], rage = level >= 3;
    const b = track.bass[s]; if (b != null) tone("triangle", hz(note(b)), t, 0.28, 0.5, 520);
    const a = track.arp[s]; if (a != null && (level >= 1 || s % 4 === 0)) tone("square", hz(note(a) + 12 + (rage && s % 2 ? 12 : 0)), t, 0.15, 0.06, 2300);
    if (level >= 1 ? d.kick.includes(s) : s === 0) kick(t, level >= 1 ? 0.6 : 0.35);
    if (level >= 1 && (d.hat.includes(s) || (rage && s % 2 === 1))) noise(t, 0.035, 0.08, "highpass", 7000);
    if (level >= 2 && d.snare.includes(s)) noise(t, 0.11, 0.2, "bandpass", 1900);
  }
  function pump() {
    if (!ctx || !track || !out) return;
    out.gain.setTargetAtTime(enabled() ? 0.3 * duck : 0, ctx.currentTime, 0.12);
    const spb = 60 / (track.bpm * (level >= 3 ? 1.08 : 1)) / 4;
    if (nextT < ctx.currentTime - 0.1) nextT = ctx.currentTime + 0.05;   // onglet resté en arrière-plan
    while (nextT < ctx.currentTime + 0.18) { if (enabled()) schedule(step, nextT); step = (step + 1) % 16; nextT += spb; }
  }
  function stop() {
    if (timer) clearInterval(timer); timer = null;
    if (out && ctx) { const o = out; try { o.gain.setTargetAtTime(0, ctx.currentTime, 0.1); } catch (e) { /* contexte fermé */ } setTimeout(() => { try { o.disconnect(); } catch (e) { /* déjà débranché */ } }, 700); }
    out = null; track = null;
  }
  return {
    start(n) {
      stop();
      const c = Sound.ensure(); if (!c || !TRACKS[n]) return;
      try { ctx = c; track = TRACKS[n]; out = ctx.createGain(); out.gain.value = 0; out.connect(ctx.destination); step = 0; nextT = ctx.currentTime + 0.08; t0 = nextT; level = 1; duck = 1; timer = setInterval(pump, 40); pump(); }
      catch (e) { stop(); }
    },
    stop,
    /** Niveau d'intensité (0 à 3) et volume relatif (0 à 1). */
    set(lv, dk) { level = lv; duck = dk; },
    /** Pulsation 1→0 à chaque temps : calée sur la musique si elle joue, sinon sur l'horloge du jeu. */
    beat(time, n) {
      const tr = track || TRACKS[n] || TRACKS[1];
      const ph = track && ctx ? ((((ctx.currentTime - t0) * tr.bpm / 60) % 1) + 1) % 1 : (time * tr.bpm / 60) % 1;
      return Math.max(0, 1 - ph * 2.4);
    },
    get on() { return state.settings.music !== false; },
    toggle() { state.settings.music = !(state.settings.music !== false); save(); return state.settings.music; },
    node: () => out
  };
})();
