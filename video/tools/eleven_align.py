# -*- coding: utf-8 -*-
"""
Voix off ElevenLabs (une génération par scène, voix « Bastien », modèle eleven_multilingual_v2) :
alignement mot à mot par Whisper local, puis reconstruction de la timeline, de la piste voix,
des sous-titres et du texte définitif, au même format que tools/tts.py.

Entrées : build/eleven/<scene>.mp3 (téléchargés depuis ElevenLabs)
Sorties : build/voice.wav, build/timeline.json, web/timeline.js, dist/*.srt, dist/voix_off_texte_definitif.txt,
          build/eleven/alignement.json (rapport d'alignement)
"""
import difflib
import json
import os
import re
import subprocess
import sys
import wave

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "script"))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from script import SCENES  # noqa: E402
from tts import split_sentences, chunk_sentence, wrap_lines, fmt_ts  # noqa: E402

SR = 44100
EL = os.path.join(ROOT, "build", "eleven")
SCENE_TAIL = 0.6      # silence ajouté après la dernière phrase de chaque scène
END_HOLD = 3.0        # tenue du carton final


def norm_words(s):
    import unicodedata
    s = s.lower().replace("’", "'").replace("-", " ").replace("'", "' ")
    s = re.sub(r"[«»:;,.?!()\"…]", " ", s)
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    out = []
    for w in s.split():
        if len(w) > 3 and w[-1] in "sx":
            w = w[:-1]
        out.append(w)
    return out


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def main():
    from faster_whisper import WhisperModel
    model = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
    track, t = [], 0.0
    tl = {"fps": 25, "scenes": [], "cues": [], "voice": "ElevenLabs, voix Bastien (eleven_multilingual_v2)"}
    report, words_spoken, script_lines = {}, 0, []

    for si, sc in enumerate(SCENES):
        audio = load(os.path.join(EL, sc["id"] + ".mp3"))
        x = np.arange(0, len(audio), SR / 16000)
        a16 = np.interp(x, np.arange(len(audio)), audio).astype(np.float32)
        segs, _ = model.transcribe(a16, language="fr", beam_size=5, word_timestamps=True,
                                   initial_prompt=" ".join(b[1] for b in sc["beats"])[:800])
        hw = []  # (mot normalisé, début, fin)
        for sg in segs:
            for w in sg.words:
                for piece in norm_words(w.word):
                    hw.append((piece, w.start, w.end))
        # mots du script avec indice de phrase
        sents = []
        for bid, text, pause in sc["beats"]:
            for k, s in enumerate(split_sentences(text)):
                sents.append({"beat": bid, "k": k, "text": s})
        sw, owner = [], []
        for i, s in enumerate(sents):
            for w in norm_words(s["text"]):
                sw.append(w)
                owner.append(i)
        sm = difflib.SequenceMatcher(None, sw, [h[0] for h in hw], autojunk=False)
        match = {}
        for a, b, n in sm.get_matching_blocks():
            for j in range(n):
                match[a + j] = b + j
        ratio = len(match) / max(1, len(sw))
        # bornes de chaque phrase : premier / dernier mot apparié
        CPS = 0.062  # secondes par caractère (débit moyen de la voix)
        for i, s in enumerate(sents):
            idx = [p for p in range(len(sw)) if owner[p] == i]
            mi = [p for p in idx if p in match]
            if not mi:
                s["t0"] = s["t1"] = None
                continue
            ws = norm_words(s["text"])
            before = sum(len(w) + 1 for w in ws[:mi[0] - idx[0]])
            after = sum(len(w) + 1 for w in ws[mi[-1] - idx[0] + 1:])
            s["t0"] = hw[match[mi[0]]][1] - before * CPS
            s["t1"] = hw[match[mi[-1]]][2] + after * CPS
        # interpolation des phrases non appariées
        for i, s in enumerate(sents):
            if s["t0"] is None:
                prev = next((sents[j]["t1"] for j in range(i - 1, -1, -1) if sents[j]["t1"] is not None), 0.0)
                nxt = next((sents[j]["t0"] for j in range(i + 1, len(sents)) if sents[j]["t0"] is not None), len(audio) / SR)
                s["t0"], s["t1"] = prev + 0.1, nxt - 0.1
        # monotonie + petites marges
        dur = len(audio) / SR
        for i, s in enumerate(sents):
            s["t0"] = max(0.0, s["t0"] - 0.06)
            s["t1"] = min(dur, s["t1"] + 0.12)
            if i and s["t0"] < sents[i - 1]["t1"]:
                mid = (s["t0"] + sents[i - 1]["t1"]) / 2
                sents[i - 1]["t1"], s["t0"] = mid, mid
        # découpe : on retire le silence initial au-delà de 0,05 s et on garde le reste tel quel (prosodie naturelle)
        cut0 = max(0, int((sents[0]["t0"] - 0.05) * SR))
        cut1 = min(len(audio), int((sents[-1]["t1"] + 0.25) * SR))
        seg = audio[cut0:cut1]
        lead = sc["lead_in"]
        s_start = t
        track.append(np.zeros(int(lead * SR), np.float32))
        base = t + lead - cut0 / SR
        track.append(seg)
        t += lead + len(seg) / SR
        tail = END_HOLD if si == len(SCENES) - 1 else SCENE_TAIL
        track.append(np.zeros(int(tail * SR), np.float32))
        t += tail
        sc_out = {"id": sc["id"], "title": sc["title"], "start": round(s_start, 3), "beats": [], "end": round(t, 3)}
        script_lines.append(f"\n## {sc['title']}\n")
        for bid, text, _ in sc["beats"]:
            bs = [s for s in sents if s["beat"] == bid]
            b_out = {"id": bid, "start": round(base + bs[0]["t0"], 3), "end": round(base + bs[-1]["t1"], 3), "sentences": []}
            for s in bs:
                st, en = base + s["t0"], base + s["t1"]
                b_out["sentences"].append({"start": round(st, 3), "end": round(en, 3), "text": s["text"]})
                words_spoken += len(re.findall(r"[\wÀ-ÿ'-]+", s["text"]))
                pieces = chunk_sentence(s["text"])
                total = sum(len(p) for p in pieces)
                cs = st
                for p in pieces:
                    d = (en - st) * len(p) / total
                    tl["cues"].append({"start": round(cs, 3), "end": round(cs + d, 3), "lines": wrap_lines(p)})
                    cs += d
            sc_out["beats"].append(b_out)
            script_lines.append(text + "\n")
        tl["scenes"].append(sc_out)
        report[sc["id"]] = {"mots_script": len(sw), "mots_apparies": len(match), "taux": round(ratio, 3),
                            "duree_voix_s": round(len(seg) / SR, 2)}
        print(sc["id"], report[sc["id"]], flush=True)

    tl["duration"] = round(t, 3)
    cues = tl["cues"]
    for i, c in enumerate(cues):
        nxt = cues[i + 1]["start"] if i + 1 < len(cues) else c["end"] + 1
        c["end"] = round(min(c["end"] + 0.25, nxt - 0.04) if nxt - c["end"] > 0.05 else c["end"], 3)

    voice = np.concatenate(track)
    with wave.open(os.path.join(ROOT, "build", "voice.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(voice, -1, 1) * 32767).astype(np.int16).tobytes())
    json.dump(tl, open(os.path.join(ROOT, "build", "timeline.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(os.path.join(ROOT, "web", "timeline.js"), "w", encoding="utf-8") as f:
        f.write("window.TIMELINE = " + json.dumps(tl, ensure_ascii=False) + ";\n")
    with open(os.path.join(ROOT, "dist", "agentic-wealth_audit-cgp.fr.srt"), "w", encoding="utf-8") as f:
        for i, c in enumerate(cues, 1):
            f.write(f"{i}\n{fmt_ts(c['start'])} --> {fmt_ts(c['end'])}\n" + "\n".join(c["lines"]) + "\n\n")
    with open(os.path.join(ROOT, "dist", "voix_off_texte_definitif.txt"), "w", encoding="utf-8") as f:
        f.write("Agentic Wealth | On audite un cabinet de gestion de patrimoine\n")
        f.write("Texte définitif de la voix off (simulation pédagogique, cabinet et chiffres fictifs)\n")
        f.write("Voix : ElevenLabs, « Bastien - Calm & Clear French Teacher », modèle eleven_multilingual_v2\n")
        f.write(f"Mots prononcés : {words_spoken}\n")
        f.write("".join(script_lines))
    json.dump(report, open(os.path.join(EL, "alignement.json"), "w"), indent=1)
    stats = {"duration_s": round(t, 2), "words": words_spoken, "cues": len(cues)}
    json.dump(stats, open(os.path.join(ROOT, "build", "tts_stats.json"), "w"), indent=1)
    print(json.dumps(stats))


if __name__ == "__main__":
    main()
