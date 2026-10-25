"""Test hors ligne du pipeline (mots -> sous-titres -> montage -> QA) avec une voix factice.

Aucun appel ElevenLabs ni Cloudinary : l'audio est une suite de bips calés sur un alignement
synthétique. Usage : python3 -m tests.smoke [--slides]
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent

TEXT_SEGMENTS = [
    ("accroche", [1], "Ton solde n’est pas ton budget."),
    ("contexte", [2], "Ton appli affiche 800 €, mais ce chiffre ne dit rien de ce qui va sortir demain."),
    ("point1", [3], "Premier piège : oublier les prélèvements à venir. Avec 800 € sur le compte et 600 € prévus, "
                    "il te reste vraiment 200 €."),
    ("point2", [4], "Deuxième piège : les paiements différés. L’achat est fait, mais l’argent n’est pas encore "
                    "parti. Ton solde paraît plus haut qu’il ne l’est."),
    ("point3", [6], "Troisième piège : regarder ton solde un seul jour. Le 2 du mois et le 28, ce n’est pas le même "
                    "compte. Regarde plutôt le point bas du mois."),
    ("chute", [8], "Ne décide jamais d’une dépense sur le chiffre affiché. Décide sur ce qui restera après les "
                   "échéances. C’est ça, ton vrai budget."),
    ("cta", [9], "Abonne-toi pour comprendre ton argent."),
]


def fake_alignment(text, rate=0.36, gap=0.06):
    chars, starts, ends = [], [], []
    t = 0.3
    words = text.split(" ")
    for wi, word in enumerate(words):
        dur = max(0.18, rate * len(word) / 6)
        step = dur / len(word)
        for k, ch in enumerate(word):
            chars.append(ch)
            starts.append(round(t + k * step, 3))
            ends.append(round(t + (k + 1) * step, 3))
        t += dur
        if wi < len(words) - 1:
            pause = 0.25 if word.endswith((".", ",", ":", "?")) else gap
            chars.append(" ")
            starts.append(round(t, 3))
            ends.append(round(t + pause, 3))
            t += pause
    return {"characters": chars, "character_start_times_seconds": starts, "character_end_times_seconds": ends}, t


def fake_audio(alignment, total, path, sr=44100):
    sig = np.zeros(int((total + 0.4) * sr), dtype=np.float32)
    for ch, a, b in zip(alignment["characters"], alignment["character_start_times_seconds"],
                        alignment["character_end_times_seconds"]):
        if ch.strip():
            i, j = int(a * sr), int(b * sr)
            t = np.arange(j - i) / sr
            sig[i:j] += 0.25 * np.sin(2 * np.pi * (180 + 40 * (ord(ch) % 7)) * t)
    wav = path.with_suffix(".wav")
    with wave.open(str(wav), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((np.clip(sig, -1, 1) * 32767).astype("<i2").tobytes())
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-b:a", "128k", str(path)], check=True)


def fake_slides(folder, source):
    folder.mkdir(parents=True, exist_ok=True)
    for n in range(1, 10):
        img = Image.new("RGB", (1080, 1350), "#F6F0E4")
        d = ImageDraw.Draw(img)
        d.rectangle([60, 60, 1020, 1290], outline="#7A0E14", width=12)
        d.text((540, 675), f"{source} — slide {n:02d}", fill="#7A0E14", anchor="mm", font_size=70)
        img.save(folder / f"{source}-{n:02d}.png")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--slides", action="store_true", help="tester le mode fond carrousel avec des PNG factices")
    p.add_argument("--keep", help="dossier de travail à conserver")
    args = p.parse_args()
    tmp = Path(args.keep or tempfile.mkdtemp(prefix="wth-smoke-"))
    tmp.mkdir(parents=True, exist_ok=True)
    text = " ".join(t for _, _, t in TEXT_SEGMENTS)
    script = [{"id": "T01", "source": "WTH-006", "date": "2026-10-26", "titre": "Ton solde n’est pas ton budget",
               "texte": text, "legende": "Test", "hashtags": ["#WealthTechHorizon"],
               "segments": [{"partie": a, "slides": b, "texte": c} for a, b, c in TEXT_SEGMENTS]}]
    (tmp / "scripts.json").write_text(json.dumps(script, ensure_ascii=False), encoding="utf-8")
    alignment, total = fake_alignment(text)
    mp3 = tmp / "voice.mp3"
    fake_audio(alignment, total, mp3)
    meta = tmp / "voice.json"
    meta.write_text(json.dumps({"request": {"text": text}, "alignment": alignment}, ensure_ascii=False),
                    encoding="utf-8")
    build = tmp / "build" / "T01"
    build.mkdir(parents=True, exist_ok=True)
    (build / "tts.json").write_text(json.dumps({"cache_key": "smoke", "audio": str(mp3), "meta": str(meta)}),
                                    encoding="utf-8")
    env = dict(os.environ, WTH_SCRIPTS=str(tmp / "scripts.json"), WTH_BUILD=str(tmp / "build"),
               WTH_OUTPUT=str(tmp / "output"), WTH_ASSETS=str(tmp / "assets"))
    if args.slides:
        fake_slides(tmp / "assets" / "WTH-006", "WTH-006")
    for step in ("words", "subs", "render", "qa"):
        r = subprocess.run([sys.executable, "-m", f"pipeline.{step}", "T01"], cwd=ROOT, env=env, text=True,
                           capture_output=True)
        print(r.stdout.strip())
        if r.returncode:
            print(r.stderr[-3000:])
            if step != "qa":
                sys.exit(r.returncode)
    print(f"Dossier de test : {tmp}")


if __name__ == "__main__":
    main()
