"""Montage : fond (slides du carrousel ou fond crème titré), sous-titres incrustés, audio normalisé -> MP4."""
import argparse
import os
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .subs import WEAK
from .common import ASSETS, OUTPUT, build_dir, ffprobe, load_config, read_json, run, script


# ---------- audio ----------

def measure(path):
    """Loudness intégrée (LUFS) et true peak (dBTP) d'un fichier audio."""
    out = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true",
               "-f", "null", "-"]).stderr
    summary = out[out.rfind("Summary:"):]
    integrated = float(re.search(r"I:\s+(-?[\d.]+) LUFS", summary).group(1))
    peak = float(re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", summary).group(1))
    return integrated, peak


def normalize_audio(src, dst, cfg):
    """Voix ramenée à -14 LUFS sans dépasser le true peak cible, 48 kHz stéréo, avec une fin silencieuse.

    Compression douce puis gain calculé et limiteur de crête ; la loudness obtenue est mesurée
    et le gain corrigé jusqu'à être à ±0,3 LU de la cible (loudnorm seul reste souvent sous la cible
    quand il doit protéger les crêtes).
    """
    ln = cfg["loudness"]
    target, tp = ln["integrated"], ln["true_peak"]
    tail = cfg["video"]["tail_seconds"]
    limit = 10 ** ((tp - 1.0) / 20)  # marge de 1 dB entre crête échantillon et true peak
    source_i, _ = measure(src)
    gain = target - source_i
    for _ in range(4):
        chain = (f"aresample=48000,acompressor=threshold=-24dB:ratio=2.5:attack=10:release=120,"
                 f"volume={gain:.2f}dB,alimiter=limit={limit:.4f}:attack=3:release=60:level=false,"
                 f"apad=pad_dur={tail}")
        run(["ffmpeg", "-hide_banner", "-y", "-i", str(src), "-af", chain, "-ac", "2", "-c:a", "pcm_s16le",
             str(dst)])
        integrated, _ = measure(dst)
        if abs(integrated - target) <= 0.3:
            break
        gain += target - integrated
    return float(ffprobe(dst)["format"]["duration"])


# ---------- fonds ----------

def slide_files(source):
    """Numéro de slide -> PNG, pour assets/WTH-XXX/*NN.png (WTH-002-01.png ou WTH-V2-002-01.png)."""
    folder = ASSETS / source
    files = {}
    if folder.is_dir():
        for f in sorted(folder.glob("*.png")):
            m = re.search(r"(\d{2})\.png$", f.name)
            if m:
                files[int(m.group(1))] = f
    return files


def wrap(draw, text, font, max_width):
    """Coupe le titre en lignes de largeur équilibrée (pas de mot orphelin sur la dernière ligne)."""
    words = [w for w in text.split(" ") if w]  # les espaces insécables (« banque : ») ne coupent pas
    greedy, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width or not cur:
            cur = trial
        else:
            greedy.append(cur)
            cur = word
    greedy.append(cur)
    n = len(greedy)

    def score(lines):
        # Largeur de la ligne la plus longue, avec un bonus pour les coupures après une ponctuation.
        width = max(draw.textlength(l, font=font) for l in lines)
        bonus = 120 * sum(l.endswith((":", "?", ",", "!")) for l in lines[:-1])
        weak = 150 * sum(l.split(" ")[-1].lower() in WEAK for l in lines[:-1])
        return width - bonus + weak

    best, best_score = greedy, score(greedy)

    def search(start, lines_left, acc):
        nonlocal best, best_score
        if lines_left == 1:
            lines = acc + [" ".join(words[start:])]
            if max(draw.textlength(l, font=font) for l in lines) <= max_width and score(lines) < best_score:
                best, best_score = lines, score(lines)
            return
        for end in range(start + 1, len(words) - lines_left + 2):
            search(end, lines_left - 1, acc + [" ".join(words[start:end])])

    if len(words) <= 14:
        search(0, n, [])
    return best


def title_background(title, path, cfg):
    """Fond crème, « WEALTHTECH HORIZON » en petit, titre de la vidéo en haut."""
    v, b = cfg["video"], cfg["brand"]
    img = Image.new("RGB", (v["width"], v["height"]), b["creme"])
    d = ImageDraw.Draw(img)
    label_font = ImageFont.truetype(b["font_label_file"], 34)
    label = "W E A L T H T E C H   H O R I Z O N"
    d.text((v["width"] / 2, 150), label, font=label_font, fill=b["bordeaux"], anchor="mm")
    d.rectangle([v["width"] / 2 - 60, 190, v["width"] / 2 + 60, 196], fill=b["rouge"])
    # Plus grande taille qui tient en 2 lignes (jusqu'à 72 px), sinon en 3 lignes.
    # Une ligne qui finit par un article (« le | moment ») fait descendre d'une taille si une autre coupe existe.
    choice = fallback = None
    for max_lines, smallest in ((2, 72), (3, 56)):
        for size in range(88, smallest - 1, -4):
            font = ImageFont.truetype(b["font_bold_file"], size)
            lines = wrap(d, title, font, v["width"] - 160)
            if len(lines) > max_lines:
                continue
            fallback = fallback or (size, font, lines)
            if not any(l.split(" ")[-1].lower() in WEAK for l in lines[:-1]):
                choice = (size, font, lines)
                break
        if choice:
            break
    size, font, lines = choice or fallback or (size, font, lines)
    y = 280
    for line in lines:
        d.text((v["width"] / 2, y), line, font=font, fill=b["bordeaux"], anchor="ma")
        y += int(size * 1.18)
    img.save(path)
    return path


def slide_schedule(s, words, duration, available, cfg):
    """[(n° slide, début)] calé sur le début de chaque segment du script."""
    starts = {}
    for w in words:
        if w["segment"] is not None and w["segment"] not in starts:
            starts[w["segment"]] = w["start"]
    segs = s["segments"]
    if len(starts) != len(segs):
        # Audio verrouillé sur un ancien texte : répartition régulière des slides.
        flat = [n for seg in segs for n in seg["slides"]]
        starts = {i: duration * i / len(segs) for i in range(len(segs))}
    bounds = [0.0] + [starts[i] for i in range(1, len(segs))] + [duration]
    plan = []
    for i, seg in enumerate(segs):
        a, b = bounds[i], bounds[i + 1]
        step = (b - a) / len(seg["slides"])
        for k, n in enumerate(seg["slides"]):
            plan.append((n, a + k * step))
    # Slides absentes : on garde la précédente ; slides consécutives identiques : fusion.
    out = []
    for n, t in plan:
        if n not in available:
            continue
        if out and out[-1][0] == n:
            continue
        out.append((n, t))
    if out:
        out[0] = (out[0][0], 0.0)
    # Une slide affichée moins longtemps que le fondu + 0,4 s est retirée.
    min_len = cfg["video"]["crossfade"] + 0.4
    cleaned = []
    for i, (n, t) in enumerate(out):
        end = out[i + 1][1] if i + 1 < len(out) else duration
        if end - t < min_len and cleaned:
            continue
        cleaned.append((n, t))
    return cleaned


def prescale(src, dst, box, factor=4):
    """Slide agrandie (x4) : zoompan travaille au pixel entier, d'où un zoom lent plus fluide."""
    img = Image.open(src).convert("RGB")
    w, h = box["w"] * factor, box["h"] * factor
    img = img.resize((w, h), Image.LANCZOS)
    img.save(dst)
    return dst


# ---------- montage ----------

def guard_motion_output(video_id, by="classic"):
    """Refuse d'écraser un rendu Remotion de output/WTH-Vxx.mp4, sauf FORCE=1 (WTH_FORCE=1).

    output/WTH-Vxx.mp4 est le même fichier pour tous les rendus. Le film Story (balise wth_mode=story, méthode
    validée) n'est écrasé ni par le montage classique ni par `make motion` (by="motion") ; le rendu motion design
    (wth_mode=motion ou commentaire « Made with Remotion ») ne l'est pas par le montage classique. Sans ce garde-fou,
    `make video` / `make all` remplaçait le rendu retenu par un style rejeté, et `make upload` l'aurait publié.
    """
    mp4 = OUTPUT / f"WTH-{video_id}.mp4"
    if not mp4.exists() or os.environ.get("WTH_FORCE") == "1":
        return
    tags = {k.lower(): v for k, v in (ffprobe(mp4).get("format", {}).get("tags", {}) or {}).items()}
    comment = tags.get("comment", "") or tags.get("wth_mode", "")
    if tags.get("wth_mode") == "story":
        raise SystemExit(f"{mp4} est le film Story (méthode validée, wth_mode=story) : le rendu "
                         f"{'motion' if by == 'motion' else 'classique'} ne l'écrase pas. Utilise « make story "
                         f"ID={video_id} », ou force avec « make {'motion' if by == 'motion' else 'video'} "
                         f"ID={video_id} FORCE=1 ».")
    if by == "classic" and ("Made with Remotion" in comment or tags.get("wth_mode") == "motion"):
        raise SystemExit(f"{mp4} est le rendu motion design ({comment}) : le montage classique ne l'écrase pas. "
                         f"Utilise « make motion ID={video_id} », ou force avec « make video ID={video_id} FORCE=1 ».")


def render(video_id):
    guard_motion_output(video_id)
    cfg = load_config()
    v = cfg["video"]
    s = script(video_id)
    out_dir = build_dir(video_id)
    tts = read_json(out_dir / "tts.json")
    words = read_json(out_dir / "words.json")["words"]
    subs = out_dir / "subs.ass"

    audio = out_dir / "audio.wav"
    duration = normalize_audio(tts["audio"], audio, cfg)
    fps = v["fps"]

    available = slide_files(s["source"])
    schedule = slide_schedule(s, words, duration, available, cfg) if available else []
    inputs, filters = [], []
    fonts = cfg["brand"]["fonts_dir"]
    # ffmpeg tourne dans build/Vxx avec un lien « fonts » : aucun chemin externe dans le filtergraph,
    # donc rien à échapper même si le dossier contient ' : , [ ] ou des espaces.
    link = out_dir / "fonts"
    if link.is_symlink() or link.exists():
        link.unlink()
    link.symlink_to(Path(fonts).resolve(), target_is_directory=True)
    sub_filter = f"subtitles=f={subs.name}:fontsdir=fonts"

    if schedule:
        canvas = out_dir / "canvas.png"
        Image.new("RGB", (v["width"], v["height"]), cfg["brand"]["creme"]).save(canvas)
        inputs += ["-loop", "1", "-framerate", str(fps), "-t", f"{duration:.3f}", "-i", str(canvas)]
        box, fade = v["slide_box"], v["crossfade"]
        times = [t for _, t in schedule] + [duration]
        offsets = []
        for k, (n, t) in enumerate(schedule):
            start = 0.0 if k == 0 else times[k] - fade
            length = times[k + 1] - start
            offsets.append(start)
            img = prescale(available[n], out_dir / f"slide{n:02d}.png", box)
            # Une seule image en entrée : zoompan en tire toutes les images du plan (d = nombre d'images).
            inputs += ["-i", str(img)]
            frames = max(1, round(length * fps))
            z = v["zoom_max"] - 1
            filters.append(
                f"[{k + 1}:v]zoompan=z='1+{z}*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                f":d={frames}:s={box['w']}x{box['h']}:fps={fps},setsar=1,format=rgb24[s{k}]")
        last = "s0"
        for k in range(1, len(schedule)):
            filters.append(f"[{last}][s{k}]xfade=transition=fade:duration={fade}:offset={offsets[k]:.3f}[x{k}]")
            last = f"x{k}"
        filters.append(f"[0:v]format=rgb24[bg];[bg][{last}]overlay=x={box['x']}:y={box['y']}:format=rgb,"
                       f"{sub_filter}[comp]")
        audio_index = len(schedule) + 1
        mode = f"slides du carrousel ({len(schedule)} plans)"
    else:
        bg = title_background(s["titre"], out_dir / "background.png", cfg)
        inputs += ["-loop", "1", "-framerate", str(fps), "-t", f"{duration:.3f}", "-i", str(bg)]
        filters.append(f"[0:v]format=rgb24,{sub_filter}[comp]")
        audio_index = 1
        mode = "fond crème titré"

    filters.append("[comp]scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[v]")
    inputs += ["-i", str(audio)]
    OUTPUT.mkdir(parents=True, exist_ok=True)
    mp4 = OUTPUT / f"WTH-{video_id}.mp4"
    cmd = ["ffmpeg", "-hide_banner", "-y", *inputs, "-filter_complex", ";".join(filters),
           "-map", "[v]", "-map", f"{audio_index}:a", "-t", f"{duration:.3f}",
           "-c:v", "libx264", "-preset", v["preset"], "-crf", str(v["crf"]), "-profile:v", "high",
           "-pix_fmt", "yuv420p", "-r", str(fps), "-g", str(fps * 2),
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
           "-c:a", "aac", "-b:a", v["audio_bitrate"], "-ar", str(v["audio_rate"]), "-ac", "2",
           "-movflags", "+faststart", str(mp4.resolve())]
    run(cmd, cwd=out_dir)
    (out_dir / "render.json").write_text(json.dumps({"mode": mode, "schedule": schedule, "duration": duration},
                                                    ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{video_id} : {mp4} ({duration:.1f} s, {mode})")
    return mp4


def main():
    p = argparse.ArgumentParser()
    p.add_argument("id")
    render(p.parse_args().id)


if __name__ == "__main__":
    main()
