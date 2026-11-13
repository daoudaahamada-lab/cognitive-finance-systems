# -*- coding: utf-8 -*-
"""
Mixage audio : voix off (build/voice.wav) + nappe musicale originale générée ici (aucun fichier tiers),
atténuée sous la voix. Sortie : build/mix.wav (48 kHz stéréo), normalisée à -16 LUFS intégrés (ffmpeg loudnorm, 2 passes).
"""
import json
import os
import re
import subprocess
import wave

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "build")
SR = 48000


def load_voice():
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(BUILD, "voice.wav"), "-f", "f32le",
                          "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def pad(duration):
    """Nappe douce : accords tenus (sinus + 2e harmonique faible), enveloppes lentes."""
    n = int(duration * SR)
    t = np.arange(n) / SR
    out = np.zeros((n, 2), np.float32)
    # progression en ré majeur, 4 accords, 10 s chacun (fréquences en Hz)
    chords = [
        [146.83, 220.00, 293.66, 369.99],   # D
        [123.47, 185.00, 246.94, 293.66],   # Bm
        [98.00, 196.00, 246.94, 293.66],    # G
        [110.00, 220.00, 277.18, 329.63],   # A
    ]
    L = 10.0
    for i in range(int(duration // L) + 2):
        ch = chords[i % 4]
        start = i * L - 1.5
        a, b = max(0, int(start * SR)), min(n, int((start + L + 3.0) * SR))
        if a >= b:
            continue
        tt = t[a:b] - start
        env = np.clip(tt / 3.0, 0, 1) * np.clip((L + 3.0 - tt) / 3.0, 0, 1)
        env = env ** 1.5
        for j, f in enumerate(ch):
            ph = 2 * np.pi * f * t[a:b]
            lfo = 1 + 0.15 * np.sin(2 * np.pi * (0.07 + 0.02 * j) * t[a:b] + j)
            s = (np.sin(ph) + 0.18 * np.sin(2 * ph + 0.3)) * lfo * env * (0.9 if j == 0 else 0.55)
            pan = 0.35 + 0.1 * j
            out[a:b, 0] += s * (1 - pan)
            out[a:b, 1] += s * pan
    out /= np.max(np.abs(out)) + 1e-9
    return out


def main():
    tl = json.load(open(os.path.join(BUILD, "timeline.json")))
    voice = load_voice()
    dur = tl["duration"] + 0.5
    n = int(dur * SR)
    v = np.zeros(n, np.float32)
    v[:min(n, len(voice))] = voice[:n]
    music = pad(dur)
    # enveloppe de présence de la voix (phrases de la timeline), lissée
    act = np.zeros(n, np.float32)
    for sc in tl["scenes"]:
        for b in sc["beats"]:
            for s in b["sentences"]:
                act[int(s["start"] * SR):int(s["end"] * SR)] = 1
    k = int(0.4 * SR)
    kernel = np.ones(k, np.float32) / k
    act = np.convolve(act, kernel, mode="same")
    music_gain = 10 ** (-31 / 20) * (1 - 0.55 * act)        # nappe à -31 dB, -7 dB sous la voix
    # fondus début / fin
    fade = np.ones(n, np.float32)
    fi, fo = int(2 * SR), int(4 * SR)
    fade[:fi] = np.linspace(0, 1, fi)
    fade[-fo:] = np.linspace(1, 0, fo)
    mix = np.stack([v, v], axis=1) * 0.9 + music * (music_gain * fade)[:, None]
    mix = np.clip(mix, -1, 1)
    tmp = os.path.join(BUILD, "mix_raw.wav")
    with wave.open(tmp, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())
    # loudnorm 2 passes
    p1 = subprocess.run(["ffmpeg", "-hide_banner", "-i", tmp, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
                         "-f", "null", "-"], capture_output=True, text=True).stderr
    m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", p1, re.S).group(0))
    af = (f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-af", af, "-ar", str(SR), os.path.join(BUILD, "mix.wav")], check=True)
    print("mix ok", m["input_i"], "->", -16)


if __name__ == "__main__":
    main()
