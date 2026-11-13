# -*- coding: utf-8 -*-
"""
Synthèse vocale locale (Piper, voix fr_FR siwis medium) + construction de la timeline,
de la piste voix, des sous-titres SRT et du texte définitif de la voix off.

Usage : python3 tools/tts.py
Sorties : build/voice.wav, build/timeline.json, dist/*.srt, dist/voix_off_texte_definitif.txt
"""
import hashlib
import json
import os
import re
import sys
import wave

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "script"))
sys.path.insert(0, os.path.join(ROOT, "tools"))

from script import SCENES  # noqa: E402
from pronunciation import tts_text  # noqa: E402

MODEL = os.path.join(ROOT, "models", "fr_FR-siwis-medium.onnx")
BUILD = os.path.join(ROOT, "build")
DIST = os.path.join(ROOT, "dist")
CACHE = os.path.join(BUILD, "tts_cache")
SR = 22050
LENGTH_SCALE = 1.0      # débit légèrement posé
SENTENCE_GAP = 0.28      # silence entre deux phrases d'un même beat
MAX_CUE_CHARS = 84       # 2 lignes de 42 caractères
LINE_CHARS = 42
PAUSE_SCALE = 0.85

os.makedirs(CACHE, exist_ok=True)
os.makedirs(DIST, exist_ok=True)


def split_sentences(text):
    # Coupe après . ? ! (éventuellement suivis de ») sauf initiale du type "R."
    parts, buf = [], ""
    tokens = re.split(r"(\s+)", text)
    for i, tok in enumerate(tokens):
        buf += tok
        if re.search(r"[.?!](\s*»)?$", tok) and not re.fullmatch(r"[A-Z]\.", tok):
            nxt = "".join(tokens[i + 1:i + 3]).strip()
            if nxt.startswith("»"):
                continue
            parts.append(buf.strip())
            buf = ""
    if buf.strip():
        parts.append(buf.strip())
    return parts


_voice = None


def voice():
    global _voice
    if _voice is None:
        from piper import PiperVoice
        _voice = PiperVoice.load(MODEL)
    return _voice


# Phrases à mots difficiles : plusieurs synthèses (Piper est stochastique), on garde
# celle que la reconnaissance vocale locale (Whisper small) restitue le mieux.
TRICKY = re.compile(r"Léa|Aix-en-Provence|chatbot|onze|\bIA\b|CNIL|Agentic|Camille|briefs?\b|cockpit|horodatage|ambiguë")
N_CANDIDATES = 5
_asr = None


def asr_score(audio, ref):
    global _asr
    if _asr is None:
        from faster_whisper import WhisperModel
        _asr = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
    x = np.arange(0, len(audio), SR / 16000)
    a16 = np.interp(x, np.arange(len(audio)), audio).astype(np.float32)
    segs, _ = _asr.transcribe(a16, language="fr", beam_size=5)
    hyp = " ".join(s.text for s in segs)
    norm = lambda s: re.sub(r"[^\wÀ-ÿ' ]", " ", s.lower().replace("-", " ")).split()
    import difflib
    return difflib.SequenceMatcher(None, norm(ref), norm(hyp)).ratio(), hyp


def synth(text):
    """Retourne un np.float32 [-1,1] à 22050 Hz, silences de bord retirés. Mis en cache."""
    spoken = tts_text(text)
    tricky = bool(TRICKY.search(text))
    key = hashlib.sha1(f"{spoken}|{LENGTH_SCALE}|siwis|{'best' if tricky else '1'}".encode()).hexdigest()[:16]
    path = os.path.join(CACHE, key + ".npy")
    if os.path.exists(path):
        return np.load(path), spoken
    from piper import SynthesisConfig
    cfg = SynthesisConfig(length_scale=LENGTH_SCALE, noise_scale=0.6, noise_w_scale=0.75)
    best = None
    for _ in range(N_CANDIDATES if tricky else 1):
        cand = np.concatenate([c.audio_float_array for c in voice().synthesize(spoken, syn_config=cfg)]).astype(np.float32)
        if not tricky:
            best = (1, cand, "")
            break
        sc, hyp = asr_score(cand, text)
        if best is None or sc > best[0]:
            best = (sc, cand, hyp)
    if tricky:
        with open(os.path.join(BUILD, "tts_bestof.log"), "a", encoding="utf-8") as lg:
            lg.write(f"{best[0]:.3f} | {text} || ASR: {best[2]}\n")
    audio = best[1]
    # retrait des silences de bord (seuil -45 dBFS), on garde 40 ms
    thr = 10 ** (-45 / 20)
    idx = np.where(np.abs(audio) > thr)[0]
    if len(idx):
        a = max(0, idx[0] - int(0.04 * SR))
        b = min(len(audio), idx[-1] + int(0.06 * SR))
        audio = audio[a:b]
    np.save(path, audio)
    return audio, spoken


WEAK = set("""de du des le la les un une et à au aux en ses son sa leur leurs ce cette ces qu'il que qui dont ou
par pour sur avec sans dans ne n'est d' l' qu' s' c'est est sont a ont mais puis entre vers très plus si où car""".split())


def protect(s):
    """Espaces insécables typographiques : jamais de « ou » isolé, ni de : ? ! ; en début de ligne."""
    import re as _re
    s = s.replace("« ", "«\u00a0").replace(" »", "\u00a0»")
    return _re.sub(r" ([:;?!])", "\u00a0\\1", s)


def _line_split(words):
    """Meilleure coupe d'un cue en 1 ou 2 lignes (<= LINE_CHARS)."""
    text = " ".join(words)
    if len(text) <= LINE_CHARS and len(text) <= 34:
        return [text], 0
    best = None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        if len(a) > LINE_CHARS or len(b) > LINE_CHARS:
            continue
        cost = abs(len(a) - len(b)) * 0.6
        if words[i - 1].lower() in WEAK:
            cost += 25
        if words[i - 1][-1] in ",:;":
            cost -= 8
        if best is None or cost < best[1]:
            best = ([a, b], cost)
    if best is None:
        return ([text], 0) if len(text) <= LINE_CHARS else (None, None)
    return best


def wrap_lines(text):
    lines, _ = _line_split(text.split(" "))
    return lines or [text]


def chunk_sentence(sent):
    """Découpage optimal (programmation dynamique) d'une phrase en cues de 1 à 2 lignes."""
    words = protect(sent).split(" ")
    n = len(words)
    INF = float("inf")
    best = [INF] * (n + 1)
    prev = [-1] * (n + 1)
    best[0] = 0
    for j in range(1, n + 1):
        for i in range(max(0, j - 20), j):
            seg = words[i:j]
            lines, lc = _line_split(seg)
            if lines is None:
                continue
            L = len(" ".join(seg))
            cost = 40 + lc
            if L < 18 and j < n:
                cost += 60
            if L < 12:
                cost += 40
            last = seg[-1]
            if j < n:
                if last[-1] in ",:;":
                    cost -= 15
                elif last.lower() in WEAK:
                    cost += 70
                else:
                    cost += 12
            if best[i] + cost < best[j]:
                best[j] = best[i] + cost
                prev[j] = i
    cuts, j = [], n
    while j > 0:
        cuts.append((prev[j], j))
        j = prev[j]
    return [" ".join(words[i:j]) for i, j in reversed(cuts)]


def fmt_ts(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main():
    track = []
    t = 0.0
    timeline = {"fps": 25, "scenes": [], "cues": []}
    words_spoken = 0
    script_lines = []

    def add_silence(sec):
        nonlocal t
        track.append(np.zeros(int(round(sec * SR)), dtype=np.float32))
        t += sec

    for sc in SCENES:
        s_start = t
        add_silence(sc["lead_in"])
        sc_out = {"id": sc["id"], "title": sc["title"], "start": round(s_start, 3), "beats": []}
        script_lines.append(f"\n## {sc['title']}\n")
        for bid, text, pause in sc["beats"]:
            b_start = t
            sents = split_sentences(text)
            b_out = {"id": bid, "start": round(t, 3), "sentences": []}
            for k, sent in enumerate(sents):
                audio, spoken = synth(sent)
                st = t
                track.append(audio)
                t += len(audio) / SR
                b_out["sentences"].append({"start": round(st, 3), "end": round(t, 3), "text": sent})
                words_spoken += len(re.findall(r"[\wÀ-ÿ'-]+", sent))
                # cues sous-titres
                pieces = chunk_sentence(sent)
                total = sum(len(p) for p in pieces)
                cs = st
                for p in pieces:
                    dur = (t - st) * len(p) / total
                    timeline["cues"].append({"start": round(cs, 3), "end": round(cs + dur, 3),
                                             "lines": wrap_lines(p)})
                    cs += dur
                if k < len(sents) - 1:
                    add_silence(SENTENCE_GAP)
            b_out["end"] = round(t, 3)
            add_silence(round(pause * PAUSE_SCALE, 3))
            sc_out["beats"].append(b_out)
            script_lines.append(text + "\n")
        sc_out["end"] = round(t, 3)
        timeline["scenes"].append(sc_out)

    timeline["duration"] = round(t, 3)
    voice_audio = np.concatenate(track)
    pcm = np.clip(voice_audio * 0.95, -1, 1)
    with wave.open(os.path.join(BUILD, "voice.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((pcm * 32767).astype(np.int16).tobytes())

    # prolonge légèrement les cues pour la lisibilité (sans chevaucher la suivante)
    cues = timeline["cues"]
    for i, c in enumerate(cues):
        nxt = cues[i + 1]["start"] if i + 1 < len(cues) else c["end"] + 1
        c["end"] = round(min(c["end"] + 0.25, nxt - 0.04) if nxt - c["end"] > 0.05 else c["end"], 3)

    with open(os.path.join(BUILD, "timeline.json"), "w", encoding="utf-8") as f:
        json.dump(timeline, f, ensure_ascii=False, indent=1)
    with open(os.path.join(ROOT, "web", "timeline.js"), "w", encoding="utf-8") as f:
        f.write("window.TIMELINE = " + json.dumps(timeline, ensure_ascii=False) + ";\n")

    with open(os.path.join(DIST, "agentic-wealth_audit-cgp.fr.srt"), "w", encoding="utf-8") as f:
        for i, c in enumerate(cues, 1):
            f.write(f"{i}\n{fmt_ts(c['start'])} --> {fmt_ts(c['end'])}\n" + "\n".join(c["lines"]) + "\n\n")

    with open(os.path.join(DIST, "voix_off_texte_definitif.txt"), "w", encoding="utf-8") as f:
        f.write("Agentic Wealth | On audite un cabinet de gestion de patrimoine\n")
        f.write("Texte définitif de la voix off (simulation pédagogique, cabinet et chiffres fictifs)\n")
        f.write(f"Mots prononcés : {words_spoken}\n")
        f.write("".join(script_lines))

    stats = {"duration_s": round(t, 2), "words": words_spoken, "cues": len(cues),
             "wpm": round(words_spoken / (t / 60), 1)}
    with open(os.path.join(BUILD, "tts_stats.json"), "w") as f:
        json.dump(stats, f, indent=1)
    print(json.dumps(stats))


if __name__ == "__main__":
    main()
