#!/usr/bin/env python3
"""Préparation du storyboard d'une vidéo WTH (étape « Prep » de la méthode A).

    python3 .claude/skills/wth-storyboard/scripts/prep.py V05            (depuis la racine du dépôt)
    python3 .claude/skills/wth-storyboard/scripts/prep.py V05 --root /abs/wth-videos --no-sheet

Lit le script (scripts/scripts.json), la voix (build/Vxx/words.json, build/Vxx/audio.wav), le carrousel
(data/carousels/<source>.json) et les illustrations présentes, puis écrit dans build/Vxx/storyboard/ :
  prep.json   phrases minutées, segments, durée, débit, cadence visée, PNG utilisables, storyboard existant ;
  words.tsv   un mot par ligne : i, début, fin, mot (tel que dans words.json : à recopier dans « mot » des temps forts) ;
  pngs.jpg    planche des PNG utilisables (carrousel de la vidéo + génériques), sur ivoire, en alpha strict.
Imprime un résumé. Code 1 si un prérequis manque (script, voix) : le storyboard ne peut pas commencer.
Aucune écriture hors de build/ (ignoré par git).
"""
import argparse
import csv
import json
import re
import sys
import unicodedata
import wave
from pathlib import Path

CAROUSEL = re.compile(r"^(WTH-\d{3})-(\d+)\.png$")
END_PUNCT = ".?!…"
TRAIL = "   »”\")"


def default_root():
    # .claude/skills/wth-storyboard/scripts/prep.py -> racine du dépôt -> wth-videos
    return Path(__file__).resolve().parents[4] / "wth-videos"


def read_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def ends_sentence(w):
    w = w.rstrip(TRAIL)
    return bool(w) and w[-1] in END_PUNCT


def audio_seconds(path):
    try:
        with wave.open(str(path)) as f:
            return f.getnframes() / f.getframerate()
    except (OSError, wave.Error):
        return None


def sentences(words):
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(i)
        if ends_sentence(w["w"]) or i == len(words) - 1:
            a, b = words[cur[0]], words[cur[-1]]
            out.append({"t_start": round(a["start"], 3), "t_end": round(b["end"], 3), "i0": cur[0], "i1": cur[-1],
                        "segment": a.get("segment"),
                        "texte": " ".join(words[k]["w"] for k in cur).replace(" ", " ")})
            cur = []
    return out


def contact_sheet(names, illus_dir, out, thumb=300, cols=4):
    try:
        import numpy as np
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return None
    font_path = illus_dir.parent.parent / "motion" / "public" / "fonts" / "Inter-SemiBold.otf"
    try:
        font = ImageFont.truetype(str(font_path), 22)
    except OSError:
        font = ImageFont.load_default()
    ivory, ink = (246, 240, 228), (30, 20, 22)
    th = int(thumb * 2 / 3)
    rows = (len(names) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb, rows * (th + 34)), ivory)
    draw = ImageDraw.Draw(sheet)
    for k, name in enumerate(names):
        im = Image.open(illus_dir / name).convert("RGBA")
        im.thumbnail((thumb - 10, th - 6))
        arr = np.asarray(im).astype(np.float32)
        # alpha strict (comme pipeline.story.strict_png : le halo cuit pour fond noir disparaît sur ivoire)
        a = np.clip((arr[..., 3] / 255 - 0.40) / (0.88 - 0.40), 0, 1)[..., None]
        bg = np.array(ivory, np.float32)
        rgb = (arr[..., :3] * a + bg * (1 - a)).astype(np.uint8)
        x, y = (k % cols) * thumb, (k // cols) * (th + 34)
        sheet.paste(Image.fromarray(rgb), (x + (thumb - im.width) // 2, y + 3))
        draw.text((x + 8, y + th + 4), name[:-4], fill=ink, font=font)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=82)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("id")
    ap.add_argument("--root", type=Path, default=None, help="dossier wth-videos (défaut : celui du dépôt)")
    ap.add_argument("--no-sheet", action="store_true", help="sans planche des PNG")
    a = ap.parse_args()
    root = (a.root or default_root()).resolve()
    vid = a.id
    problems = []

    scripts = {s["id"]: s for s in read_json(root / "scripts" / "scripts.json")}
    if vid not in scripts:
        print(f"{vid} : absent de scripts/scripts.json (ajouter le script, puis make lint ID={vid})")
        raise SystemExit(1)
    sc = scripts[vid]
    source = sc.get("source", "")

    wp = root / "build" / vid / "words.json"
    if not wp.exists():
        print(f"{vid} : build/{vid}/words.json absent : la voix n'est pas finale (skill wth-video, recette voix, "
              f"puis make voice ID={vid}). Les temps forts se calent sur les débuts de mots : pas de storyboard avant.")
        raise SystemExit(1)
    words = read_json(wp)["words"]
    wav = root / "build" / vid / "audio.wav"
    dur = audio_seconds(wav)
    if dur is None:
        problems.append(f"build/{vid}/audio.wav absent : lancer « python3 -m pipeline.story {vid} --audio » dans wth-videos/ "
                        f"(refait audio.wav depuis la voix en cache, sans appel à ElevenLabs), puis relancer prep.py ; "
                        f"en attendant, durée estimée sur le dernier mot")
        dur = words[-1]["end"] + 0.15
    joined = re.sub(r"\s+", " ", unicodedata.normalize("NFC", " ".join(w["w"] for w in words))
                    .replace(" ", " ").replace(" ", " ")).strip()
    texte = re.sub(r"\s+", " ", unicodedata.normalize("NFC", sc["texte"]).replace(" ", " ")
                   .replace(" ", " ")).strip()
    if joined != texte:
        problems.append("les mots de words.json ne redonnent pas exactement le texte du script : vérifier la voix "
                        "(pipeline.connector) avant d'écrire les textes des scènes")

    sents = sentences(words)
    segs = []
    for k, seg in enumerate(sc.get("segments", [])):
        ws = [w for w in words if w.get("segment") == k]
        if ws:
            segs.append({"partie": seg["partie"], "t_start": round(ws[0]["start"], 3), "t_end": round(ws[-1]["end"], 3),
                         "texte": seg["texte"]})

    # Illustrations : carrousel de la vidéo + génériques (règle de la série, appliquée aussi par Story.png).
    illus = root / "assets" / "illustrations"
    manifest = root / "data" / "illustrations_manifest.tsv"
    listed = []
    if manifest.exists():
        with manifest.open(encoding="utf-8") as f:
            listed = [r["fichier"] for r in csv.DictReader(f, delimiter="\t")]
    present = sorted(p.name for p in illus.glob("*.png")) if illus.exists() else []
    own = [n for n in present if (m := CAROUSEL.match(n)) and m.group(1) == source]
    generic = [n for n in present if not CAROUSEL.match(n)]
    missing = [n for n in listed if n not in present and (not CAROUSEL.match(n) or CAROUSEL.match(n).group(1) == source)]
    if missing:
        problems.append(f"{len(missing)} illustration(s) du manifeste absente(s) : {', '.join(missing)} "
                        f"(Drive : data/illustrations_manifest.tsv, voir le skill wth-video)")
    slides = []
    cj = root / "data" / "carousels" / f"{source}.json"
    if cj.exists():
        slides = [{"n": s.get("n"), "fichier": s.get("fichier"), "titre": s.get("titre")}
                  for s in read_json(cj).get("slides", [])]

    sb = root / "scripts" / "storyboards" / f"{vid}.json"
    existing = read_json(sb).get("version", "sans version") if sb.exists() else None

    n = len(words)
    prep = {
        "id": vid, "titre": sc.get("titre"), "source": source, "date": sc.get("date"),
        "duree": round(dur, 3), "dernier_mot_fin": words[-1]["end"], "mots": n, "debit": round(n / dur, 2),
        "cadence": {"compositions": [round(n / 9.5), round(n / 7.5)], "evenements": [round(n / 7.5), round(dur)],
                    "regle": "compositions : ≈ 1 nouvelle composition par 9,5 mots (plus serré dans l'accroche) ; "
                             "événements : au moins 1 par 7,5 mots, viser 1 par seconde, chacun sur un début de mot ; "
                             "jamais plus de 3 s sans mouvement (QA : image figée > 3,5 s refusée)"},
        "phrases": sents, "segments": segs,
        "notes_prononciation": sc.get("notes_prononciation", ""),
        "pngs": {"carrousel": own, "generiques": generic, "absents": missing},
        "carrousel_slides": slides,
        "storyboard_existant": existing,
        "problemes": problems,
    }
    out = root / "build" / vid / "storyboard"
    out.mkdir(parents=True, exist_ok=True)
    (out / "prep.json").write_text(json.dumps(prep, ensure_ascii=False, indent=1), encoding="utf-8")
    with (out / "words.tsv").open("w", encoding="utf-8") as f:
        f.write("i\tdebut\tfin\tmot\tsegment\n")
        for i, w in enumerate(words):
            f.write(f"{i}\t{w['start']:.3f}\t{w['end']:.3f}\t{w['w']}\t{w.get('segment', '')}\n")
    sheet = None if a.no_sheet else contact_sheet(own + generic, illus, out / "pngs.jpg")

    rel = lambda p: p.relative_to(root) if p else "—"
    print(f"{vid} « {sc.get('titre')} » · carrousel {source} · {dur:.2f} s · {n} mots · {n / dur:.2f} mots/s")
    print(f"  cadence visée : {prep['cadence']['compositions'][0]}-{prep['cadence']['compositions'][1]} compositions, "
          f"{prep['cadence']['evenements'][0]} à {prep['cadence']['evenements'][1]} événements")
    for s in sents:
        print(f"  {s['t_start']:6.2f}-{s['t_end']:6.2f} | {s['texte']}")
    print("  segments : " + " · ".join(f"{s['partie']} {s['t_start']:.2f}-{s['t_end']:.2f}" for s in segs))
    print(f"  PNG du carrousel : {', '.join(own) or 'aucun (mise en scène en code + génériques)'}")
    print(f"  génériques : {len(generic)}")
    print(f"  storyboard existant : {existing or 'non'}")
    print(f"  écrit : {rel(out / 'prep.json')}, {rel(out / 'words.tsv')}, {rel(sheet) if sheet else 'pas de planche'}")
    for p in problems:
        print(f"  attention : {p}")


if __name__ == "__main__":
    sys.exit(main())
