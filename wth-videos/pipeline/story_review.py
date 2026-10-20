"""Planches de revue d'un film Story (ou d'un extrait), pour les relecteurs qui extrayaient eux-mêmes des images
pleine résolution : JPEG mi-résolution seulement -> build/Vxx/review/<film|Sa-Sb>[_nocap]/.

    python3 -m pipeline.story_review V01                       tout (planches, temps forts, téléphone, tenues) du film
    python3 -m pipeline.story_review V01 --nocap --sheets      planches de la version sans sous-titres
    python3 -m pipeline.story_review V01 --src output/extraits/WTH-V01_extrait_S11-S14.mp4 --beats
    python3 -m pipeline.story_review V01 --clean               supprime bandes et images téléphone (garde planches et tenues)

--sheets  planches : 6 i/s, images mi-résolution (540 x 960), 12 par planche (6 par rangée = 1 s), avec image et temps
          du film et scène du storyboard -> sheets/sheet_NN.jpg
--beats   une bande par temps fort (props meta.beats) : images f-3 à f+12, quart de résolution -> beats/
--phone   taille téléphone : réencodage à 2 Mb/s (compression des plateformes), puis images de 360 px de large à 2 i/s
          -> phone/phone_NN.jpg et phone/<nom>_360.mp4 (à regarder avec le son)
--holds   tenues : pixels qui bougent d'une image à la suivante (mi-résolution, hors ligne de sous-titres), tenues
          de 0,5 s ou plus, signalées au-delà de 3,5 s (règle de la QA) -> holds.json

Source : par défaut le film décrit par build/Vxx/story_render.json (--nocap : sa version sans sous-titres) ; --src
un MP4 rendu par pipeline.story (ses props sont retrouvées par la balise wth_props, ou --props).
"""
import argparse
import json
import math
import shutil
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .common import ROOT, build_dir, ffprobe, read_json, run
from .motion import sha1_file
from .qa import CAP_BAND, FROZEN_MAX, MOVE_LEVEL, MOVE_PIXELS, decoded_frames, end_card_frame, still_runs
from .story import FONTS, STORY_SIDECAR

HALF = (540, 960)
SHEET_STEP = 5         # une image sur 5 : 6 i/s à 30 i/s
SHEET_PER = 12         # images par planche (12 à 16)
SHEET_COLS = 6
BEAT_SPAN = (-3, 12)   # images autour du temps fort
BEAT_THUMB = 270
BEAT_COLS = 8
PHONE_W = 360
PHONE_RATE = "2M"
PHONE_STEP = 15        # 2 i/s
KINDS = ("sheets", "beats", "phone", "holds")
BG, FG, DIM = (40, 40, 44), (235, 235, 235), (160, 160, 165)


def _font(size, weight="SemiBold"):
    return ImageFont.truetype(str(FONTS / f"Inter-{weight}.otf"), size)


def resolve(video_id, src="cap", props=None):
    """(MP4, props) à relire : film de story_render.json (« cap » / « nocap ») ou MP4 donné."""
    out = build_dir(video_id)
    if src in ("cap", "nocap"):
        path = out / STORY_SIDECAR
        if not path.exists():
            raise SystemExit(f"{path} absent : rendre d'abord le film (make story ID={video_id}), ou --src <mp4>")
        rec = read_json(path)
        k_mp4, k_props = ("file", "props") if src == "cap" else ("nocap", "props_nocap")
        if not rec.get(k_mp4):
            raise SystemExit(f"{path} : pas de version {'avec' if src == 'cap' else 'sans'} sous-titres")
        return ROOT / rec[k_mp4], Path(props) if props else ROOT / rec[k_props]
    mp4 = Path(src)
    if not mp4.exists():
        raise SystemExit(f"MP4 absent : {mp4}")
    if props:
        return mp4, Path(props)
    tags = {k.lower(): v for k, v in (ffprobe(mp4).get("format", {}).get("tags", {}) or {}).items()}
    cands = sorted((out / "story").glob("props_*.json"))
    if tags.get("wth_props"):
        hit = next((p for p in cands if sha1_file(p) == tags["wth_props"]), None)
        if hit:
            return mp4, hit
    if tags.get("wth_scenes"):
        p = out / "story" / f"props_{tags['wth_scenes']}{'' if tags.get('wth_captions') == '1' else '_nocap'}.json"
        if p.exists():
            return mp4, p
    raise SystemExit(f"{mp4} : props introuvables (balises wth_props / wth_scenes) : préciser --props")


class Timeline:
    """Image de la vidéo -> image et temps du film, scène du storyboard."""

    def __init__(self, props):
        self.fps, self.off = props["fps"], props.get("frameOffset", 0)
        try:
            sb = read_json(ROOT / props["meta"]["storyboard"])
            self.scenes = [(round(s["t_start"] * self.fps), s["id"]) for s in sb["scenes"]]
        except (KeyError, OSError, ValueError):
            self.scenes = []

    def film(self, n):
        return n + self.off

    def scene(self, n):
        f = self.film(n)
        return next((sid for start, sid in reversed(self.scenes) if f >= start), "")

    def label(self, n):
        f = self.film(n)
        return f"{self.scene(n)}  {f / self.fps:.2f} s  #{f}".strip()


def _sheet(items, cols, tw, th, font, path, title=None, title_font=None):
    """Planche JPEG : [(légende, image RGB)] en `cols` colonnes de vignettes tw x th."""
    head = 34 if title else 0
    rows = math.ceil(len(items) / cols)
    im = Image.new("RGB", (cols * (tw + 6) + 6, head + rows * (th + 26) + 6), BG)
    d = ImageDraw.Draw(im)
    if title:
        d.text((8, 6), title, font=title_font, fill=FG)
    for k, (cap, fr) in enumerate(items):
        x, y = 6 + (k % cols) * (tw + 6), head + 6 + (k // cols) * (th + 26)
        thumb = Image.fromarray(fr) if fr.shape[1] == tw else Image.fromarray(fr).resize((tw, th), Image.BOX)
        im.paste(thumb, (x, y + 22))
        d.text((x + 2, y + 2), cap, font=font, fill=FG)
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, quality=82)
    return path


def _clear(d, pattern="*"):
    if d.exists():
        for f in d.glob(pattern):
            if f.is_file():
                f.unlink()
    d.mkdir(parents=True, exist_ok=True)


def scan(mp4, props, out, kinds, per=SHEET_PER):
    """Un seul décodage mi-résolution pour les planches, les bandes de temps forts et les tenues."""
    tl = Timeline(props)
    total = props["durationInFrames"]
    k = HALF[0] / props["width"]
    c0, c1 = (round(y * k) for y in CAP_BAND)
    font, big = _font(15), _font(19)
    results = {}
    sheet_items, sheets = [], []
    if "sheets" in kinds:
        _clear(out / "sheets", "*.jpg")
    beats = []
    if "beats" in kinds:
        _clear(out / "beats", "*.jpg")
        for b in props.get("meta", {}).get("beats", []):
            n = b["frame"] - tl.off
            if 0 <= n < total:
                beats.append({**b, "n": n, "items": []})
    bh = round(BEAT_THUMB * HALF[1] / HALF[0])
    moving, counts, prev = [], [], None
    keep = np.ones(HALF[1], bool)
    keep[c0:c1] = False   # la ligne de sous-titres change à chaque mot : hors du calcul des tenues

    def flush_sheet():
        if sheet_items:
            path = out / "sheets" / f"sheet_{len(sheets) + 1:02d}.jpg"
            sheets.append(str(_sheet(sheet_items, SHEET_COLS, HALF[0], HALF[1], big, path)))
            sheet_items.clear()

    n = -1
    for n, fr in enumerate(decoded_frames(mp4, HALF)):
        if "holds" in kinds:
            if prev is None:
                counts.append(0)
                moving.append(True)
            else:
                c = int((np.abs(fr[keep].astype(np.int16) - prev[keep].astype(np.int16)).max(-1) > MOVE_LEVEL).sum())
                counts.append(c)
                moving.append(c >= MOVE_PIXELS)
            prev = fr
        if "sheets" in kinds and n % SHEET_STEP == 0:
            sheet_items.append((tl.label(n), fr))
            if len(sheet_items) == per:
                flush_sheet()
        for b in beats:
            if b["n"] + BEAT_SPAN[0] <= n <= b["n"] + BEAT_SPAN[1]:
                small = np.asarray(Image.fromarray(fr).resize((BEAT_THUMB, bh), Image.BOX))
                b["items"].append((f"{n - b['n']:+d}  #{tl.film(n)}", small))
    flush_sheet()
    n_frames = n + 1
    if "sheets" in kinds:
        results["sheets"] = sheets
        print(f"  planches : {len(sheets)} x {per} images à {props['fps'] / SHEET_STEP:.0f} i/s -> {out / 'sheets'}")
    if "beats" in kinds:
        made = []
        for b in beats:
            what = b.get("what", "")
            title = (f"{b['scene']} « {b['word']} »  image {b['frame']} ({b['frame'] / tl.fps:.2f} s) : "
                     f"{what[:150] + ('…' if len(what) > 150 else '')}")
            word = "".join(ch for ch in b["word"] if ch.isalnum())[:16] or "x"
            path = out / "beats" / f"b{b['frame']:05d}_{b['scene']}_{word}.jpg"
            made.append(str(_sheet(b["items"], BEAT_COLS, BEAT_THUMB, bh, font, path, title, big)))
        results["beats"] = made
        print(f"  temps forts : {len(made)} bandes (images {BEAT_SPAN[0]} à +{BEAT_SPAN[1]}) -> {out / 'beats'}")
    if "holds" in kinds:
        fps = props["fps"]
        end = end_card_frame(props)
        runs = still_runs(moving, fps)
        holds = [{"from": s, "to": e, "film": [tl.film(s), tl.film(e)], "t": [round(tl.film(s) / fps, 2),
                  round((tl.film(e) + 1) / fps, 2)], "s": round((e - s + 1) / fps, 2), "scene": tl.scene(s),
                  "too_long": (e - s + 1) / fps > FROZEN_MAX and not (e >= n_frames - 1 and end is not None and s >= end)}
                 for s, e in runs]
        report = {"mp4": str(mp4), "frames": n_frames, "rule": f"tenue = moins de {MOVE_PIXELS} px (mi-résolution) qui "
                  f"changent de plus de {MOVE_LEVEL} niveaux ; signalée au-delà de {FROZEN_MAX} s hors carte de fin",
                  "holds": holds, "moving_pixels": counts}
        path = out / "holds.json"
        path.write_text(json.dumps(report, ensure_ascii=False) + "\n", encoding="utf-8")
        results["holds"] = str(path)
        longest = max(holds, key=lambda h: h["s"], default=None)
        print(f"  tenues : {len(holds)} de 0,5 s ou plus"
              + (f", la plus longue {longest['s']} s ({longest['scene']} {longest['t'][0]}-{longest['t'][1]} s)"
                 if longest else "") + f" -> {path}")
        for h in holds:
            if h["too_long"]:
                print(f"    attention : image figée {h['s']} s ({h['scene']}, {h['t'][0]}-{h['t'][1]} s)")
    return results


def phone(mp4, props, out, step=PHONE_STEP, per=SHEET_PER):
    """Ce que voit un téléphone : réencodage 2 Mb/s pleine résolution (compression des plateformes), puis réduction à
    360 px de large -> planches JPEG à 2 i/s et une vidéo 360 px avec le son."""
    tl = Timeline(props)
    d = out / "phone"
    _clear(d, "*.jpg")
    tw, th = PHONE_W, round(PHONE_W * props["height"] / props["width"])
    with tempfile.TemporaryDirectory(prefix="wth-phone-") as tmp:
        crushed = Path(tmp) / "2mbps.mp4"
        run(["ffmpeg", "-hide_banner", "-y", "-i", str(mp4), "-c:v", "libx264", "-preset", "veryfast",
             "-b:v", PHONE_RATE, "-maxrate", PHONE_RATE, "-bufsize", "4M", "-c:a", "copy", str(crushed)])
        small = d / f"{out.name}_360.mp4"
        run(["ffmpeg", "-hide_banner", "-y", "-i", str(crushed), "-vf", f"scale={tw}:{th}:flags=area",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "copy", str(small)])
        items, sheets = [], []
        font = _font(13)
        for n, fr in enumerate(decoded_frames(crushed, (tw, th))):
            if n % step == 0:
                items.append((tl.label(n), fr))
            if len(items) == per:
                sheets.append(str(_sheet(items, SHEET_COLS, tw, th, font, d / f"phone_{len(sheets) + 1:02d}.jpg")))
                items = []
        if items:
            sheets.append(str(_sheet(items, SHEET_COLS, tw, th, font, d / f"phone_{len(sheets) + 1:02d}.jpg")))
    print(f"  téléphone : {len(sheets)} planches ({PHONE_W} px, après {PHONE_RATE}b/s, {props['fps'] / step:.0f} i/s) "
          f"+ {small}")
    return {"phone": sheets, "phone_mp4": str(small)}


def review(video_id, kinds=KINDS, src="cap", props=None):
    """Sorties de revue demandées (`kinds`) pour la source `src` -> {type: chemins}."""
    mp4, props_path = resolve(video_id, src, props)
    p = read_json(props_path)
    name = props_path.stem.removeprefix("props_")
    out = build_dir(video_id) / "review" / name
    out.mkdir(parents=True, exist_ok=True)
    print(f"{video_id} : revue de {mp4} ({name}) -> {out}")
    results = scan(mp4, p, out, [k for k in kinds if k != "phone"]) if set(kinds) - {"phone"} else {}
    if "phone" in kinds:
        results.update(phone(mp4, p, out))
    return results


def clean(video_id):
    """Supprime les images de travail de revue (bandes de temps forts, téléphone, images extraites), garde les
    planches (sheets/) et les rapports de tenues."""
    root = build_dir(video_id) / "review"
    gone = 0
    for d in list(root.glob("*/beats")) + list(root.glob("*/phone")) + [root / "frames", root / "stills"]:
        if d.is_dir():
            gone += sum(f.stat().st_size for f in d.rglob("*") if f.is_file())
            shutil.rmtree(d)
    print(f"{video_id} : {gone / 1e6:.1f} Mo d'images de revue supprimés ({root})")


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("id")
    p.add_argument("--src", default=None, help="MP4 à relire (défaut : le film de story_render.json)")
    p.add_argument("--nocap", action="store_true", help="la version sans sous-titres du film")
    p.add_argument("--props", help="props du MP4 (si elles ne se retrouvent pas par ses balises)")
    for k in KINDS:
        p.add_argument(f"--{k}", action="store_true")
    p.add_argument("--clean", action="store_true", help="supprime bandes et images téléphone (garde planches, tenues)")
    a = p.parse_args()
    if a.clean:
        clean(a.id)
        return
    kinds = [k for k in KINDS if getattr(a, k)] or list(KINDS)
    review(a.id, kinds, a.src or ("nocap" if a.nocap else "cap"), a.props)


if __name__ == "__main__":
    main()
