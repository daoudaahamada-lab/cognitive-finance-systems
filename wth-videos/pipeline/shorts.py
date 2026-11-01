"""Vidéos courtes sans voix (14 s) : composition Remotion « Short », une vidéo par objet de shorts/shorts.json.

    python3 -m pipeline.shorts                  les 5 : props -> rendu Remotion -> piste AAC muette -> contrôles
    python3 -m pipeline.shorts S02 S04          seulement ces vidéos
    python3 -m pipeline.shorts --stills "0 75 400"   images fixes PNG -> build/shorts/stills/Sxx_f0075.png (pas de rendu)
    python3 -m pipeline.shorts --check          contrôles seuls (ffprobe, zones réservées, planches) des MP4 existants

Sorties : output/shorts/WTH-Sxx.mp4 (1080x1920, 30 i/s, 420 images, h264 yuv420p bt709, AAC stéréo 48 kHz muet : la
musique est ajoutée sur TikTok / Instagram), build/shorts/Sxx_sheet.jpg (planche de 6 images). Rendus et images fixes
sous le verrou build/.render.lock (motion.run_locked : un seul rendu Remotion à la fois).
"""
import argparse
import subprocess
import sys
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .common import BUILD, OUTPUT, ROOT, ffprobe, read_json, run, write_json
from .motion import MOTION, remotion_env, run_locked

SPEC = ROOT / "shorts" / "shorts.json"
WORK = BUILD / "shorts"
OUT = OUTPUT / "shorts"
FONTS = MOTION / "public" / "fonts"
FPS, W, H, FRAMES = 30, 1080, 1920, 420
# Zones réservées (interface TikTok / Reels) : rien d'important en haut, en bas, à droite ; marge gauche.
ZONES = {"haut y<160": (slice(0, 160), slice(0, W)), "bas y>1540": (slice(1541, H), slice(0, W)),
         "droite x>930": (slice(0, H), slice(931, W)), "gauche x<60": (slice(0, H), slice(0, 60))}
BG = np.array([[246, 240, 228], [236, 228, 212]], dtype=np.int16)   # ivoire + lignes de grille
SHEET_TIMES = (1.2, 3.3, 5.3, 7.3, 11.3, 13.6)   # accroche, gestes 1 à 3 et 5 à leur sommet, fin


def shorts(ids):
    data = read_json(SPEC)["shorts"]
    chosen = [s for s in data if not ids or s["id"] in ids]
    unknown = set(ids) - {s["id"] for s in data}
    if unknown:
        raise SystemExit(f"Inconnu dans {SPEC.name} : {', '.join(sorted(unknown))}")
    return chosen


def write_props(short):
    path = WORK / "props" / f"{short['id']}.json"
    write_json(path, short)
    return path


def stills(items, frames):
    out = WORK / "stills"
    props = [str(write_props(s)) for s in items]
    t0 = time.time()
    proc = run_locked(["node", "scripts/shorts_stills.mjs", str(out), ",".join(map(str, frames)), *props],
                      "images fixes shorts", env=remotion_env())
    if proc.returncode != 0:
        print(proc.stdout[-3000:], proc.stderr[-3000:])
        raise SystemExit("Images fixes en échec")
    print(f"{len(items)} x {len(frames)} images fixes -> {out} ({time.time() - t0:.0f} s)")


def render(short):
    sid = short["id"]
    props = write_props(short)
    silent = WORK / f"{sid}_silent.mp4"
    # Images clés au début de chaque temps (accroche, 5 éléments, fin) : jamais de rafraîchissement GOP dans une tenue.
    kf = ",".join(f"{max(0.0, t - 0.001):.3f}" for t in (0, 2, 4, 6, 8, 10, 12))
    cmd = ["npx", "remotion", "render", "Short", str(silent), f"--props={props}", "--muted", "--log=error"]
    t0 = time.time()
    proc = run_locked(cmd, f"rendu short {sid}", env=remotion_env(WTH_KEYFRAMES=kf))
    if proc.returncode != 0:
        print(proc.stdout[-4000:], proc.stderr[-4000:])
        raise SystemExit(f"{sid} : rendu Remotion en échec ({proc.returncode})")
    print(f"{sid} : rendu Remotion {time.time() - t0:.0f} s")
    OUT.mkdir(parents=True, exist_ok=True)
    mp4 = OUT / f"WTH-{sid}.mp4"
    run(["ffmpeg", "-hide_banner", "-y", "-i", str(silent),
         "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
         "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
         "-bsf:v", "h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1:video_full_range_flag=0",
         "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv",
         "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-t", f"{FRAMES / FPS:.6f}",
         "-metadata", f"title={short['titre']}", "-metadata", "comment=WealthTech Horizon",
         "-movflags", "+faststart", str(mp4)])
    return mp4


def probe(mp4):
    p = ffprobe(mp4)
    v = next(s for s in p["streams"] if s["codec_type"] == "video")
    a = [s for s in p["streams"] if s["codec_type"] == "audio"]
    problems = []
    dur = float(p["format"]["duration"])
    nb = int(v.get("nb_frames", 0))
    want = {"codec_name": "h264", "pix_fmt": "yuv420p", "width": W, "height": H, "r_frame_rate": f"{FPS}/1",
            "color_space": "bt709", "color_primaries": "bt709", "color_transfer": "bt709"}
    for k, val in want.items():
        if v.get(k) != val:
            problems.append(f"{k}={v.get(k)} (attendu {val})")
    if nb != FRAMES:
        problems.append(f"{nb} images (attendu {FRAMES})")
    if abs(dur - FRAMES / FPS) > 0.03:
        problems.append(f"durée {dur:.3f} s")
    if not a:
        problems.append("pas de piste audio")
    else:
        au = a[0]
        if (au["codec_name"], int(au["sample_rate"]), au["channels"]) != ("aac", 48000, 2):
            problems.append(f"audio {au['codec_name']} {au['sample_rate']} Hz {au['channels']} canaux")
    line = (f"{dur:.3f} s, {nb} images, {v['codec_name']} {v['pix_fmt']} {v.get('color_space')}/"
            f"{v.get('color_primaries')}/{v.get('color_transfer')} {v['width']}x{v['height']} {v['r_frame_rate']}"
            + (f", {a[0]['codec_name']} {a[0]['sample_rate']} Hz {a[0]['channels']} canaux" if a else ""))
    return line, problems


def frames_of(mp4, step=3):
    """Images RGB du MP4 (une sur `step`) -> générateur (index, tableau HxWx3)."""
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(mp4), "-vf", f"select=not(mod(n\\,{step}))",
                             "-vsync", "0", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    n = 0
    size = W * H * 3
    while True:
        buf = proc.stdout.read(size)
        if len(buf) < size:
            break
        yield n * step, np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        n += 1
    proc.wait()


def safe_zones(mp4):
    """Pixels hors fond (ivoire / grille, tolérance 14) dans chaque zone réservée, au pire sur une image sur 3."""
    worst = {z: (0, -1) for z in ZONES}
    for n, img in frames_of(mp4):
        for z, (ys, xs) in ZONES.items():
            px = img[ys, xs].astype(np.int16)
            d = np.min(np.max(np.abs(px[:, :, None, :] - BG[None, None, :, :]), axis=3), axis=2)
            c = int((d > 14).sum())
            if c > worst[z][0]:
                worst[z] = (c, n)
    return worst


def contact_sheet(mp4, sid):
    tw, th = 360, 640
    font = ImageFont.truetype(str(FONTS / "Inter-SemiBold.otf"), 22)
    sheet = Image.new("RGB", (3 * tw + 4 * 10, 2 * (th + 34) + 10), (40, 40, 44))
    d = ImageDraw.Draw(sheet)
    for k, t in enumerate(SHEET_TIMES):
        png = WORK / f"_sheet_{sid}_{k}.png"
        run(["ffmpeg", "-hide_banner", "-y", "-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1", str(png)])
        x, y = 10 + (k % 3) * (tw + 10), 10 + (k // 3) * (th + 34)
        sheet.paste(Image.open(png).convert("RGB").resize((tw, th), Image.LANCZOS), (x, y + 30))
        d.text((x + 2, y + 2), f"{sid}  {t:.1f} s", font=font, fill=(235, 235, 235))
        png.unlink()
    out = WORK / f"{sid}_sheet.jpg"
    sheet.save(out, quality=88)
    return out


def check(sid):
    mp4 = OUT / f"WTH-{sid}.mp4"
    if not mp4.exists():
        raise SystemExit(f"{mp4} absent : lance « make shorts ».")
    line, problems = probe(mp4)
    zones = safe_zones(mp4)
    zl = ", ".join(f"{z} {c} px" + (f" (image {n})" if c else "") for z, (c, n) in zones.items())
    sheet = contact_sheet(mp4, sid)
    status = "OK" if not problems and not any(c for c, _ in zones.values()) else "À REVOIR"
    print(f"{sid} {status} : {mp4.relative_to(ROOT)} : {line}\n    zones réservées : {zl}\n    planche : {sheet.relative_to(ROOT)}")
    for p in problems:
        print(f"    problème : {p}")
    return status == "OK"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ids", nargs="*", help="S01 … S05 (défaut : toutes)")
    ap.add_argument("--stills", help="images à rendre en PNG, ex. \"0 75 400\" (pas de vidéo)")
    ap.add_argument("--check", action="store_true", help="contrôles seuls des MP4 existants")
    args = ap.parse_args(argv)
    items = shorts(args.ids)
    WORK.mkdir(parents=True, exist_ok=True)
    if args.stills:
        stills(items, [int(x) for x in args.stills.replace(",", " ").split()])
        return 0
    if not args.check:
        for s in items:
            render(s)
    ok = all([check(s["id"]) for s in items])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
