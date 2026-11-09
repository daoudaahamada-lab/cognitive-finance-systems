/* Sons synthétisés avec Web Audio : aucun fichier à charger. */
const Sound = (() => {
  let ac = null, master = null, noiseBuf = null;
  const isOn = () => state.settings.sound !== false;
  function ensure() {
    if (!ac) {
      try { const AC = window.AudioContext || window.webkitAudioContext; if (!AC) return null; ac = new AC(); master = ac.createGain(); master.gain.value = 0.42; master.connect(ac.destination); }
      catch (e) { ac = null; return null; }
    }
    if (ac.state === "suspended") ac.resume().catch(() => {});
    return ac;
  }
  function tone(f, d, type, vol, f2, delay) {
    if (!isOn()) return; const c = ensure(); if (!c) return;
    const t = c.currentTime + (delay || 0), o = c.createOscillator(), g = c.createGain();
    o.type = type || "sine"; o.frequency.setValueAtTime(f, t); if (f2) o.frequency.exponentialRampToValueAtTime(f2, t + d);
    g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(vol || 0.3, t + 0.01); g.gain.exponentialRampToValueAtTime(0.0001, t + d);
    o.connect(g); g.connect(master); o.start(t); o.stop(t + d + 0.03);
  }
  function noise(d, freq, vol, type, delay) {
    if (!isOn()) return; const c = ensure(); if (!c) return;
    if (!noiseBuf) { noiseBuf = c.createBuffer(1, c.sampleRate, c.sampleRate); const data = noiseBuf.getChannelData(0); for (let i = 0; i < data.length; i++) data[i] = Math.random() * 2 - 1; }
    const t = c.currentTime + (delay || 0), s = c.createBufferSource(), fl = c.createBiquadFilter(), g = c.createGain();
    s.buffer = noiseBuf; fl.type = type || "bandpass"; fl.frequency.value = freq || 1000;
    g.gain.setValueAtTime(vol || 0.3, t); g.gain.exponentialRampToValueAtTime(0.0001, t + d);
    s.connect(fl); fl.connect(g); g.connect(master); s.start(t); s.stop(t + d + 0.03);
  }
  const sfx = {
    click: () => tone(660, 0.05, "sine", 0.12),
    load: () => { tone(320, 0.09, "triangle", 0.2, 540); noise(0.05, 3200, 0.08); },
    stretch: (p) => tone(110 + p * 70, 0.05, "triangle", 0.07),
    release: () => { noise(0.25, 1600, 0.32, "highpass"); tone(240, 0.12, "triangle", 0.08, 120); },
    hit: () => { tone(150, 0.2, "sine", 0.5, 50); noise(0.12, 2600, 0.32); },
    crit: () => { tone(150, 0.24, "sine", 0.55, 45); noise(0.2, 4200, 0.4); tone(880, 0.3, "triangle", 0.22, 1320, 0.05); },
    block: () => { tone(220, 0.14, "square", 0.12, 170); tone(233, 0.14, "square", 0.1, 180); noise(0.06, 5000, 0.12); },
    dart: () => tone(950, 0.32, "sawtooth", 0.1, 150),
    hurt: () => { tone(90, 0.28, "sine", 0.6, 40); noise(0.2, 500, 0.3, "lowpass"); tone(420, 0.35, "triangle", 0.13, 210, 0.06); },
    inject: () => { for (let i = 0; i < 7; i++) tone(260 + Math.random() * 1000, 0.05, "square", 0.06, null, i * 0.05); },
    quarantine: () => { tone(520, 0.1, "triangle", 0.2); tone(780, 0.18, "triangle", 0.2, null, 0.09); tone(1040, 0.22, "triangle", 0.12, null, 0.18); },
    miss: () => tone(320, 0.16, "sine", 0.12, 200),
    warn: () => tone(70, 0.13, "sine", 0.32),
    heal: () => tone(400, 0.32, "sine", 0.14, 820),
    rage: () => { tone(80, 0.7, "sawtooth", 0.18, 40); noise(0.6, 400, 0.25, "lowpass"); },
    win: () => [523, 659, 784, 1047, 1319].forEach((f, i) => tone(f, 0.4, "triangle", 0.2, null, i * 0.11)),
    lose: () => [392, 349, 311, 262].forEach((f, i) => tone(f, 0.45, "triangle", 0.18, null, i * 0.17)),
    shatter: () => { noise(0.8, 3800, 0.5, "highpass"); tone(120, 0.6, "sine", 0.5, 30); },
    build: () => { tone(110, 0.12, "square", 0.12, 90); noise(0.1, 900, 0.2, "lowpass", 0.05); tone(160, 0.1, "square", 0.1, 120, 0.12); },
    collapse: () => { noise(0.5, 700, 0.35, "lowpass"); tone(90, 0.5, "sine", 0.3, 40); },
    cache: () => { tone(1320, 0.12, "triangle", 0.16); tone(1760, 0.2, "triangle", 0.16, null, 0.08); },
    shield: () => { tone(300, 0.4, "sine", 0.16, 600); noise(0.3, 2500, 0.08); },
    shieldBreak: () => { noise(0.4, 5000, 0.3, "highpass"); tone(900, 0.3, "triangle", 0.2, 300); },
    alarm: () => { tone(880, 0.12, "square", 0.08); tone(660, 0.12, "square", 0.08, null, 0.13); },
    ack: () => tone(980, 0.08, "sine", 0.14, 1300),
    shuffle: () => { for (let i = 0; i < 5; i++) noise(0.04, 3000 + i * 300, 0.12, "bandpass", i * 0.04); },
    fog: () => noise(0.7, 500, 0.18, "lowpass"),
    phase: () => { tone(220, 0.5, "sawtooth", 0.14, 440); tone(330, 0.6, "triangle", 0.12, 660, 0.1); },
    flip: () => noise(0.08, 2200, 0.14, "bandpass"),
    pop: () => { noise(0.18, 1800, 0.4); tone(500, 0.08, "square", 0.08, 200); },
    match: () => { tone(660, 0.1, "triangle", 0.16); tone(990, 0.16, "triangle", 0.14, null, 0.07); },
    nomatch: () => tone(200, 0.18, "square", 0.08, 150),
    ding: () => { tone(1046, 0.6, "sine", 0.18); tone(1568, 0.8, "sine", 0.1, null, 0.02); },
    whoosh: () => noise(0.5, 900, 0.22, "bandpass"),
    entrance: () => { noise(1.1, 300, 0.3, "lowpass"); tone(55, 1.2, "sawtooth", 0.16, 110); tone(220, 0.5, "triangle", 0.12, 440, 0.9); },
    telegraph: () => tone(520, 0.3, "square", 0.05, 880),
    glitch: () => { for (let i = 0; i < 4; i++) tone(180 + Math.random() * 900, 0.04, "sawtooth", 0.05, null, i * 0.035); },
    valid: () => { tone(880, 0.07, "triangle", 0.1); tone(1320, 0.1, "triangle", 0.1, null, 0.06); },
    mirage: () => noise(0.4, 1400, 0.12, "bandpass"),
    stamp: () => { tone(70, 0.25, "sine", 0.6, 40); noise(0.12, 900, 0.35, "lowpass"); }
  };
  return {
    ensure,
    play(n, a) { try { if (sfx[n]) sfx[n](a); } catch (e) { /* audio indisponible */ } },
    get on() { return isOn(); },
    toggle() { state.settings.sound = !isOn(); save(); if (isOn()) ensure(); return isOn(); }
  };
})();
