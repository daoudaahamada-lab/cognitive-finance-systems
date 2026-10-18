"""Montage : fond (slides du carrousel ou fond crème titré), sous-titres incrustés, audio normalisé -> MP4."""
import argparse
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .common import ASSETS, OUTPUT, build_dir, ffprobe, load_config, read_json, run, script


# ---------- audio ----------

def normalize_audio(src, dst, cfg):
    """Loudnorm en deux passes vers -14 LUFS, true peak -1,5 dBTP, 48 kHz stéréo, avec une fin silencieuse."""
    ln = cfg["loudness"]
    target = f"I={ln['integrated']}:TP={ln['true_peak']}:LRA={ln['lra']}"
    first = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(src), "-af",
                 f"loudnorm={target}:print_format=json", "-f", "null", "-"])
    m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", first.stderr, re.S).group(0))
    second = (f"loudnorm={target}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
              f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:"
              f"linear=true:print_format=summary")
    tail = cfg["video"]["tail_seconds"]
    run(["ffmpeg", "-hide_banner", "-y", "-i", str(src), "-af",
         f"{second},aresample=48000,apad=pad_dur={tail}", "-ac", "2", "-c:a", "pcm_s16le", str(dst)])
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
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def title_background(title, path, cfg):
    """Fond crème, « WEALTHTECH HORIZON » en petit, titre de la vidéo en haut."""
    v, b = cfg["video"], cfg["brand"]
    img = Image.new("RGB", (v["width"], v["height"]), b["creme"])
    d = ImageDraw.Draw(img)
    label_font = ImageFont.truetype(b["font_label_file"], 34)
    label = "W E A L T H T E C H   H O R I Z O N"
    d.text((v["width"] / 2, 150), label, font=label_font, fill=b["bordeaux"], anchor="mm")
    d.rectangle([v["width"] / 2 - 60, 190, v["width"] / 2 + 60, 196], fill=b["rouge"])
    size = 88
    while True:
        font = ImageFont.truetype(b["font_bold_file"], size)
        lines = wrap(d, title, font, v["width"] - 160)
        if len(lines) <= 3 or size <= 60:
            break
        size -= 4
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

def render(video_id):
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
