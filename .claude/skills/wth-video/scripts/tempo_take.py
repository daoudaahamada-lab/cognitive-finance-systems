#!/usr/bin/env python3
"""Accélère une prise de voix (option (a) de la recette quand aucune prise ne tient sous la limite).

    python3 .claude/skills/wth-video/scripts/tempo_take.py V08 <generation_id> 1.027 [--root /abs/wth-videos]

Seulement après l'accord de l'utilisateur sur cette option. Lit build/Vxx/voice/take-<id>.mp3 et, s'il existe,
words-<id>.json (transcription Scribe de cette prise). Écrit à côté :
  take-<id>-x<F>.mp3    ffmpeg atempo=F (hauteur de voix conservée), MP3 au débit de la prise d'origine ;
  words-<id>-x<F>.json  la transcription avec chaque start/end DIVISÉ par F (la prise dure F fois moins).
pick_take.py voit ensuite la prise accélérée comme une prise de plus (« <id>-x<F> »). Puis imprime les commandes
d'import (connecteur, avec le generation_id d'origine) et de suivi.

F entre 1,001 et 1,04 : au-delà, l'accélération s'entend (--force pour passer outre, avec l'accord explicite).
Code 1 sur une erreur. Aucun appel réseau, aucun crédit.
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

MAX_FACTOR = 1.04


def default_root():
    return Path(__file__).resolve().parents[4] / "wth-videos"


def probe(path, entry):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", entry, "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True)
    return out.stdout.strip().splitlines()[0] if out.stdout.strip() else ""


def main():
    p = argparse.ArgumentParser(description="Accélère une prise de voix et sa transcription Scribe")
    p.add_argument("id", help="V08")
    p.add_argument("generation_id")
    p.add_argument("factor", type=float, help="facteur atempo, ex. 1.027")
    p.add_argument("--root", default=str(default_root()))
    p.add_argument("--force", action="store_true", help=f"facteur au-delà de ×{MAX_FACTOR}")
    a = p.parse_args()
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg absent du PATH")
    f = a.factor
    if not 1.001 <= f <= (10 if a.force else MAX_FACTOR):
        sys.exit(f"facteur {f} refusé : entre 1,001 et {MAX_FACTOR} (au-delà, --force avec l'accord de l'utilisateur)")
    vdir = Path(a.root) / "build" / a.id / "voice"
    src = vdir / f"take-{a.generation_id}.mp3"
    if not src.exists():
        sys.exit(f"{src} absent (prises téléchargées : references/voice-elevenlabs-mcp.md, étape 3)")
    tag = f"{a.generation_id}-x{f:g}"
    dst = vdir / f"take-{tag}.mp3"
    kbps = probe(src, "format=bit_rate")
    bitrate = f"{max(64, round(int(kbps) / 1000))}k" if kbps.isdigit() else "128k"
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-filter:a", f"atempo={f}",
                        "-c:a", "libmp3lame", "-b:a", bitrate, str(dst)], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ffmpeg en échec : {r.stderr[-800:]}")
    d0, d1 = float(probe(src, "format=duration") or 0), float(probe(dst, "format=duration") or 0)
    print(f"{dst.name} : {d0:.2f} s -> {d1:.2f} s (×{f:g}, {bitrate})")

    words = vdir / f"words-{a.generation_id}.json"
    out_words = vdir / f"words-{tag}.json"
    if words.exists():
        data = json.loads(words.read_text(encoding="utf-8"))
        items = data.get("words", data) if isinstance(data, dict) else data
        n = 0
        for w in items:
            for k in ("start", "end"):
                if isinstance(w.get(k), (int, float)):
                    w[k] = round(w[k] / f, 3)
                    n += 1
        out_words.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        print(f"{out_words.name} : {n} temps divisés par {f:g}")
    else:
        print(f"{words.name} absent : transcris d'abord la prise d'origine (étape 5), puis relance ce script. "
              "Ne transcris pas la prise accélérée : elle n'est pas sur le flow.")
    print("\nEnsuite :")
    print(f"  python3 .claude/skills/wth-video/scripts/pick_take.py {a.id}    # racine du dépôt : {tag} doit tenir")
    print(f"  cd wth-videos && python3 -m pipeline.connector {a.id} --audio build/{a.id}/voice/{dst.name} \\\n"
          f"      --words build/{a.id}/voice/{out_words.name} --generation-id {a.generation_id}")
    print(f"  make voice ID={a.id}    # dans wth-videos/")
    print(f"  python3 .claude/skills/wth-video/scripts/status.py set {a.id} voice done take={a.generation_id} tempo={f:g} duration_s={d1:.2f} cache_key=<clé> "
          f"aligned='\"…\"' --note \"prise accélérée ×{f:g} avec l'accord de l'utilisateur (<date>)\"")


if __name__ == "__main__":
    main()
