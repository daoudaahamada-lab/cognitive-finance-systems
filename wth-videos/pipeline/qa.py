"""Contrôle qualité automatique d'une vidéo -> output/qa/Vxx.json et output/qa_report.md."""
import argparse
import math
import re
import subprocess
import unicodedata
from datetime import datetime, timezone

import numpy as np

from .common import OUTPUT, build_dir, ffprobe, load_config, read_json, run, script, videos, write_json
from .motion import CAPTION_FONT, GENERATED, RENDER_SIDECAR, SHOTLISTS, clean_word, sha1_file
from .subs import Measure
from .words import tokenize

QA_DIR = OUTPUT / "qa"
MOJIBAKE = re.compile(r"Ã.|Â.|â€|\ufffd|Å“|Ã©")
ACTIVE = re.compile(r"\{\\1c[^}]*\}(.*?)\{\\r\}")
TAGS = re.compile(r"\{[^}]*\}")
ALLOW = {"wealthtech", "fintech", "open", "banking", "etf", "nasdaq", "msci", "world", "regafi", "orias", "dsp2",
         "pea", "per", "dic", "amf", "acpr", "rgpd", "cgp", "ia", "crm", "pdf", "pacs", "s&p", "app", "apps",
         "abonne-toi", "toi", "agrégateur", "agrégateurs", "wealthtechhorizon"}


def parse_ass(path):
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("Dialogue:"):
            continue
        parts = line.split(",", 9)
        start, end, text = parts[1], parts[2], parts[9]
        events.append({"start": ass_seconds(start), "end": ass_seconds(end), "text": text})
    return events


def ass_seconds(t):
    h, m, s = t.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def pcm(path, rate=16000):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(rate), "-f", "f32le", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def raw_samples(path):
    """Échantillons de tous les canaux, au taux d'origine, sans mixage (pour compter l'écrêtage)."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a", "-f", "f32le", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def audio_offset(ref, test, rate=16000, window=20.0, max_lag=1.0):
    """Décalage (s) de la piste du MP4 par rapport à l'audio en cache, par corrélation croisée."""
    a = ref[: int(window * rate)]
    b = test[: int((window + max_lag) * rate)]
    n = 1 << math.ceil(math.log2(len(a) + len(b)))
    corr = np.fft.irfft(np.fft.rfft(b, n) * np.conj(np.fft.rfft(a, n)), n)
    lags = np.concatenate([corr[: int(max_lag * rate)], corr[-int(max_lag * rate):]])
    idx = int(np.argmax(lags))
    lag = idx if idx < int(max_lag * rate) else idx - 2 * int(max_lag * rate)
    return lag / rate


def silences(path, noise="-40dB", min_len=0.2):
    """Pauses réellement présentes dans l'audio (silencedetect)."""
    out = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af",
               f"silencedetect=n={noise}:d={min_len}", "-f", "null", "-"]).stderr
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", out)]
    ends = [float(x) for x in re.findall(r"silence_end: (-?[\d.]+)", out)]
    return list(zip(starts, ends))


def pause_conflicts(words, pauses, margin=0.15):
    """Mots horodatés incompatibles avec une pause mesurée dans l'audio.

    Un mot ne doit ni commencer au milieu d'une pause, ni l'enjamber (de plus de `margin` des deux côtés).
    Le dernier mot est seulement contrôlé sur son début : sa fin est souvent prolongée jusqu'à la fin du fichier.
    """
    bad = []
    for s0, s1 in pauses:
        for i, w in enumerate(words):
            starts_inside = s0 + margin < w["start"] < s1 - margin
            spans = w["start"] < s1 - margin and w["end"] > s0 + margin and i < len(words) - 1
            if starts_inside or spans:
                bad.append(f"« {w['w']} » ({w['start']:.2f}–{w['end']:.2f}) dans la pause {s0:.2f}–{s1:.2f}")
    return bad


def loudness(path):
    out = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-map", "0:a", "-af", "ebur128=peak=true",
               "-f", "null", "-"]).stderr
    summary = out[out.rfind("Summary:"):]
    integrated = float(re.search(r"I:\s+(-?[\d.]+) LUFS", summary).group(1))
    peak = float(re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", summary).group(1))
    return integrated, peak


def check(name, ok, value, expected, detail=""):
    return {"check": name, "ok": bool(ok), "value": value, "expected": expected, "detail": detail}


def spell_warnings(text):
    try:
        from spellchecker import SpellChecker
    except ImportError:
        return ["pyspellchecker absent : vérification orthographique non faite"]
    sp = SpellChecker(language="fr")
    unknown = []
    for raw in text.split():
        token = raw.strip(".,;:!?…«»\u00a0").replace("\u00a0", " ")
        for part in re.split(r"[-\s]", token):
            part = part.split("’")[-1]
            low = part.lower()
            if not part or any(c.isdigit() for c in part) or part.isupper() or low in ALLOW or not part.isalpha():
                continue
            if low not in sp:
                unknown.append(part)
    return sorted(set(unknown))


REMOTION_TAG = "Made with Remotion"


def mp4_tags(probe):
    return {k.lower(): v for k, v in (probe.get("format", {}).get("tags", {}) or {}).items()}


def render_sidecar(out_dir, mp4):
    """build/Vxx/motion_render.json s'il décrit bien CE fichier (même empreinte), sinon None."""
    path = out_dir / RENDER_SIDECAR
    if not path.exists():
        return None
    side = read_json(path)
    return side if side.get("mp4_sha1") == sha1_file(mp4) else None


def is_motion_render(probe, sidecar=None):
    """Rendu motion : balise wth_mode=motion, commentaire « Made with Remotion x.y.z », ou fiche de rendu
    build/Vxx/motion_render.json dont l'empreinte est celle du MP4 (survit à un remontage sans métadonnées)."""
    tags = mp4_tags(probe)
    return (tags.get("wth_mode") == "motion" or REMOTION_TAG in tags.get("comment", "")
            or bool(sidecar and sidecar.get("mode") == "motion"))


def caption_source(probe, mode="auto", sidecar=None):
    """Source des sous-titres à contrôler, déduite du MP4 lui-même (et non des dates des fichiers de build)."""
    if mode != "auto":
        return mode
    return "motion" if is_motion_render(probe, sidecar) else "classic"


def motion_captions(out_dir):
    """Surbrillance (début en s, mot affiché), groupes affichés et textes des éléments graphiques de motion.json."""
    props = read_json(out_dir / "motion.json")
    fps = props["fps"]
    active = [(w["from"] / fps, w["text"]) for g in props["captions"] for w in g["words"]]
    groups = [" ".join(w["text"] for w in g["words"]) for g in props["captions"]]
    texts = [o.get(k, "") for o in props.get("overlays", []) for k in ("text", "flip_text")]
    texts += [t for o in props.get("overlays", []) for t in o.get("texts", [])]
    texts += [part.get("flip_text", "") for part in (props.get("endCard") or {}).values()]
    texts += [part.get("text", "") for part in (props.get("endCard") or {}).values()]
    return props, active, groups, [t for t in texts if t]


def caption_gaps(props):
    """Images sans sous-titre (il doit toujours y en avoir un, d'un groupe au suivant)."""
    cursor, gaps = 0, []
    for g in props["captions"]:
        if g["from"] > cursor:
            gaps.append((cursor, g["from"]))
        cursor = max(cursor, g["to"])
    if cursor < props["durationInFrames"]:
        gaps.append((cursor, props["durationInFrames"]))
    return gaps


class FontMeasure:
    """Largeur d'un groupe avec la police, la taille et l'interlettrage réels du rendu motion."""

    def __init__(self, font_file, size, tracking_em):
        from fontTools.ttLib import TTFont
        from PIL import ImageFont
        self.font = ImageFont.truetype(str(font_file), size)
        self.tracking = tracking_em * size
        self.cmap = TTFont(str(font_file), lazy=True).getBestCmap()

    def width(self, text):
        return self.font.getlength(text) + self.tracking * len(text)

    def missing_glyphs(self, text):
        return sorted({c for c in text if not c.isspace() and ord(c) not in self.cmap})



# ---------- contrôles sur l'image décodée (rendu motion) ----------

HALF = (540, 960)
BAND = (120, 1240)      # bande visuelle, au-dessus des sous-titres (px pleine résolution)
CAP_BAND = (1280, 1380)  # ligne de sous-titres (ligne de base 1350)
INK_MIN = 0.03          # part minimale de pixels allumés dans la bande visuelle pendant un passage
# Luminance minimale d'un passage, rapportée au plan le moins lumineux des deux. L'entrant grandit de 0,7 à 1 : une
# fois le sortant parti, sa propre surface plafonne la bande vers 0,8 pendant 1-2 images ; un vrai creux (les deux
# héros translucides en même temps, rendu n° 1) mesurait 0,54 à 0,72.
DIP_MIN = 0.78


def decoded_frames(mp4, size=HALF):
    """Images décodées du MP4, à mi-résolution, en flux (RGB 8 bits)."""
    w, h = size
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(mp4), "-vf", f"scale={w}:{h}:flags=area",
                             "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    n = w * h * 3
    while True:
        buf = proc.stdout.read(n)
        if len(buf) < n:
            break
        yield np.frombuffer(buf, np.uint8).reshape(h, w, 3)
    proc.wait()


def red_mask(rgb):
    """Rouges de la marque (corail du mot prononcé et rouge plein des aplats), même atténués."""
    r, g, b = (rgb[..., k].astype(np.int16) for k in range(3))
    return (r > 150) & (g < 120) & (r - g > 80) & (r - b > 50)


def picture_checks(video_id, mp4, props):
    """Contrôles mesurés sur les images du MP4 (et non sur les props) :
    - scène jamais vide pendant les passages de héros et les cartes de chapitre (pixels allumés, rouge compris) ;
    - pas de creux de luminance aux passages ;
    - la rangée d'étapes ne traverse jamais le héros qui entre (aucun rouge dans sa boîte à son arrivée) ;
    - la surbrillance karaoké change exactement à l'image du début de chaque mot.
    """
    fps, total = props["fps"], props["durationInFrames"]
    k = HALF[0] / props["width"]
    b0, b1 = (round(y * k) for y in BAND)
    c0, c1 = (round(y * k) for y in CAP_BAND)
    from PIL import Image
    bg = np.asarray(Image.open(GENERATED / video_id / "bg.png").convert("RGB").resize(HALF, Image.BOX), np.float32)
    lum_w = np.array([0.2126, 0.7152, 0.0722], np.float32)
    bg_l = bg[b0:b1] @ lum_w
    shots, steps = props["shots"], props.get("steps") or {"chapters": []}
    chapters = steps["chapters"]
    style = props["style"]
    # Images où la rangée d'étapes ne doit plus rien laisser de rouge dans la boîte du héros entrant.
    probe_red = {}
    for ch in chapters:
        hero = next((sh for sh in shots if sh["from"] == ch["to"]), None)
        if hero and hero.get("extent", {}).get("box"):
            half_h = style["steps"]["big"]["red"] / 2 + 12
            x0, y0, x1, y1 = hero["extent"]["box"]
            y0, y1 = max(y0, steps["cy"] - half_h), min(y1, steps["cy"] + half_h)
            for f in range(ch["to"], ch["to"] + style["steps"]["leave"] + 2):
                probe_red[f] = (hero["id"], [round(v * k) for v in (x0, y0, x1, y1)])
    ink, lum, cap_masks, red_hits = [], [], [], {}
    for i, fr in enumerate(decoded_frames(mp4)):
        band = fr[b0:b1].astype(np.float32)
        ink.append(float((band.max(-1) > 60).mean()))
        lum.append(float(np.clip(band @ lum_w - bg_l, 0, None).mean()))
        cap_masks.append(red_mask(fr[c0:c1]))
        if i in probe_red:
            hid, (x0, y0, x1, y1) = probe_red[i]
            red_hits[i] = (hid, int(red_mask(fr[y0:y1, x0:x1]).sum()))
    ink, lum = np.array(ink), np.array(lum)
    n = len(ink)
    out = []

    # 1. Scène jamais vide : passages de héros et cartes de chapitre.
    windows = [(sh["id"], sh["from"] - 1, sh["from"] + 12) for sh in shots[1:]]
    windows += [(f"chapitre {ch['index'] + 1}", ch["from"] - 1, ch["to"] + 12) for ch in chapters]
    worst = min(((float(ink[max(a, 0):min(b, n)].min()), int(np.argmin(ink[max(a, 0):min(b, n)])) + max(a, 0), w)
                 for w, a, b in windows if a < n), default=(1.0, 0, ""))
    out.append(check("Scène jamais vide", worst[0] >= INK_MIN, f"{worst[0]:.1%} au pire (image {worst[1]}, {worst[2]})",
                     f"≥ {INK_MIN:.0%} de pixels allumés dans la bande visuelle à chaque passage et carte de chapitre",
                     f"{len(windows)} fenêtres ; médiane de toute la vidéo {np.median(ink):.1%}, minimum "
                     f"{ink.min():.1%} (image {int(np.argmin(ink))})"))

    # 2. Pas de creux de luminance aux passages (héros -> héros, héros -> chapitre, chapitre -> héros).
    cuts = sorted({sh["from"] for sh in shots[1:]} | {ch["from"] for ch in chapters} | {ch["to"] for ch in chapters})
    ratios = []
    for f in cuts:
        if f + 14 >= n or f < 1:
            continue
        ref = min(lum[f - 1], lum[f + 14])
        ratios.append((float(lum[f:f + 9].min() / max(ref, 1e-6)), f))
    low = min(ratios, default=(1.0, 0))
    out.append(check("Passages sans creux", low[0] >= DIP_MIN, f"{low[0]:.2f} au pire (image {low[1]})",
                     f"≥ {DIP_MIN:.2f} (luminance du passage / plan le moins lumineux des deux)",
                     f"{len(ratios)} passages, médiane {np.median([r for r, _ in ratios]):.2f}" if ratios else ""))

    # 3. La rangée d'étapes quitte la scène sans traverser le héros qui entre.
    bad = {f: v for f, v in red_hits.items() if v[1] > 20}
    out.append(check("Rangée d'étapes dégagée", not bad,
                     "ok" if not bad else "; ".join(f"image {f} ({h}) : {c} px rouges" for f, (h, c) in sorted(bad.items())),
                     "aucun rouge dans la boîte du héros pendant ses premières images après une carte de chapitre",
                     f"{len(red_hits)} images contrôlées"))

    # 4. Surbrillance karaoké : le mot rouge change exactement à l'image du début de chaque mot, jamais avant.
    onsets = sorted({w["from"] for g in props["captions"] for w in g["words"] if w["from"] > 0})
    late, early, missing = [], [], []

    def iou(a, b):
        u = (a | b).sum()
        return (a & b).sum() / u if u else 1.0

    for f in onsets:
        if f >= n:
            continue
        if cap_masks[f].sum() < 15:
            missing.append(f)
        if iou(cap_masks[f - 1], cap_masks[f]) > 0.5:
            late.append(f)
        if f - 2 >= 0 and (f - 1) not in onsets and iou(cap_masks[f - 2], cap_masks[f - 1]) < 0.8:
            early.append(f)
    first = min(w["from"] for g in props["captions"] for w in g["words"])
    blank = [i for i in range(first, n) if cap_masks[i].sum() < 15]  # avant le 1er mot : groupe en crème
    out.append(check("Surbrillance à l'image près", not (late or early or missing or blank),
                     f"{len(onsets) - len(late) - len(early)}/{len(onsets)} changements à l'image exacte",
                     "le mot rouge change à l'image du début du mot, pas avant ; toujours un mot rouge à l'écran",
                     "; ".join(x for x in (f"en retard : {late[:5]}" if late else "", f"en avance : {early[:5]}" if early else "",
                                            f"sans mot rouge : {(missing or blank)[:5]}" if (missing or blank) else "") if x)
                     or "mesuré sur la ligne de sous-titres décodée"))
    return out


def qa_video(video_id, mode="auto"):
    cfg = load_config()
    q, sc = cfg["qa"], cfg["subtitles"]
    s = script(video_id)
    out_dir = build_dir(video_id)
    mp4 = OUTPUT / f"WTH-{video_id}.mp4"
    tts = read_json(out_dir / "tts.json")
    wdata = read_json(out_dir / "words.json")
    words = wdata["words"]
    probe = ffprobe(mp4)
    sidecar = render_sidecar(out_dir, mp4)
    mode = caption_source(probe, mode, sidecar)
    if mode == "motion":
        props, active, groups, overlay_texts = motion_captions(out_dir)
        cap = props["style"]["caption"]
        measure = FontMeasure(CAPTION_FONT, cap["size"], cap["tracking_em"])
        max_width = cap["max_width"]
        shown_text = "\n".join(groups + overlay_texts)
    else:
        events = parse_ass(out_dir / "subs.ass")
        active = [(e["start"], ACTIVE.search(e["text"]).group(1)) for e in events if ACTIVE.search(e["text"])]
        groups = [TAGS.sub("", e["text"]) for e in events]
        measure = Measure(cfg["brand"]["font_bold_file"], sc["font_size"])
        max_width = sc["max_width_px"]
        shown_text = (out_dir / "subs.ass").read_text(encoding="utf-8")
    results = []

    # Durée et format
    duration = float(probe["format"]["duration"])
    results.append(check("Durée", q["min_duration"] <= duration <= q["max_duration"], f"{duration:.2f} s",
                         f"{q['min_duration']:.0f} à {q['max_duration']:.0f} s"))
    vs = next(st for st in probe["streams"] if st["codec_type"] == "video")
    aus = next((st for st in probe["streams"] if st["codec_type"] == "audio"), {})
    fmt = f"{vs['codec_name']} {vs['width']}x{vs['height']} {vs['avg_frame_rate']} {vs['pix_fmt']} + {aus.get('codec_name')}"
    want = f"h264 1080x1920 {cfg['video']['fps']}/1 yuv420p + aac"
    colour = {k: vs.get(k, "?") for k in ("color_range", "color_space", "color_primaries", "color_transfer")}
    audio_fmt = f"{aus.get('sample_rate', '?')} Hz, {round(int(aus.get('bit_rate', 0)) / 1000)} kb/s"
    fmt_problems = [] if fmt == want else [fmt]
    if mode == "motion":
        # Le rendu motion est toujours marqué BT.709 plage limitée (remotion.config.ts, setColorSpace).
        bad = {k: v for k, v in colour.items() if v != ("tv" if k == "color_range" else "bt709")}
        if bad:
            fmt_problems.append(f"couleur {bad}")
    results.append(check("Format", not fmt_problems, f"{fmt}, profil {vs.get('profile')}, "
                         f"{colour['color_range']}/{colour['color_space']}, audio {audio_fmt}", want +
                         (", BT.709 plage tv" if mode == "motion" else ""), "; ".join(fmt_problems)))
    if mode == "motion":
        # Le MP4 contrôlé doit être celui que décrivent motion.json et le plan : mêmes empreintes (balises wth_* du
        # MP4, ou fiche de rendu), même nombre d'images. Les dates de fichiers ne comptent pas (une image fixe ou
        # « --props » après le rendu réécrit motion.json à l'identique sans le périmer).
        frames = int(vs.get("nb_frames", 0))
        tags = mp4_tags(probe)
        stamp = {"props": tags.get("wth_props") or (sidecar or {}).get("props_sha1"),
                 "shotlist": tags.get("wth_shotlist") or (sidecar or {}).get("shotlist_sha1")}
        now = {"props": sha1_file(out_dir / "motion.json"), "shotlist": sha1_file(SHOTLISTS / f"{video_id}.json")}
        stale = [k for k in ("props", "shotlist") if stamp[k] != now[k]]
        ok = frames == props["durationInFrames"] and not stale and all(stamp.values())
        results.append(check("Rendu motion à jour", ok,
                             f"{frames} images, empreintes {'identiques' if not stale else 'DIFFÉRENTES : ' + ', '.join(stale)}"
                             + ("" if all(stamp.values()) else " (MP4 sans empreinte de rendu)"),
                             f"{props['durationInFrames']} images (motion.json), empreintes props + plan du rendu = "
                             "fichiers actuels",
                             "plan ou props modifiés depuis le rendu : relancer make motion" if stale else
                             f"props {now['props'][:10]}, plan {now['shotlist'][:10]}"))

    # Synchronisation : début de surbrillance vs alignement, quantification à l'image, décalage audio
    fps = cfg["video"]["fps"]
    if len(active) == len(words) and mode == "motion":
        # La surbrillance est dessinée à l'image près : seul compte l'écart image / début du mot.
        sub_err = max(abs(t - w["start"]) for (t, _), w in zip(active, words))
    elif len(active) == len(words):
        diffs = [abs(t - w["start"]) for (t, _), w in zip(active, words)]
        frame_lag = [math.ceil(t * fps - 1e-6) / fps - t for t, _ in active]
        sub_err = max(diffs) + max(frame_lag)
    else:
        sub_err = float("inf")
    ref, test = pcm(tts["audio"]), pcm(mp4)
    offset = audio_offset(ref, test)
    total_ms = (sub_err + abs(offset)) * 1000
    pauses = [(a, b) for a, b in silences(tts["audio"]) if a > 0.05 and b < len(ref) / 16000 - 0.05]
    conflicts = pause_conflicts(words, pauses)
    source = read_json(tts["meta"]).get("alignment_source", "with-timestamps")
    results.append(check("Synchro sous-titres", total_ms < q["max_sync_ms"] and not conflicts, f"{total_ms:.0f} ms",
                         f"< {q['max_sync_ms']} ms",
                         f"sous-titres ({'motion.json' if mode == 'motion' else 'subs.ass'})/alignement + image : "
                         f"{sub_err * 1000:.0f} ms ; décalage audio MP4 : "
                         f"{offset * 1000:.0f} ms ; alignement {source} vérifié sur {len(pauses)} pauses mesurées"
                         + (f", conflits : {'; '.join(conflicts[:3])}" if conflicts else ", aucun conflit")))

    # Mots coupés
    tokens = [wdata["text"][a:b] for a, b in tokenize(wdata["text"])]
    if mode == "motion":
        tokens = [clean_word(t) for t in tokens]  # sous-titres motion : ponctuation retirée
    shown = [w for _, w in active]
    widest = max((measure.width(g) for g in groups), default=0)
    ref_dur = len(ref) / 16000
    tail_rms = float(np.sqrt(np.mean(ref[-800:] ** 2))) if len(ref) else 0.0
    tail_db = 20 * math.log10(max(tail_rms, 1e-9))
    problems = []
    if shown != tokens:
        problems.append(f"{len(shown)} mots surlignés pour {len(tokens)} mots dans le texte")
    if widest > max_width:
        problems.append(f"groupe trop large : {widest:.0f} px")
    if mode == "motion" and caption_gaps(props):
        problems.append(f"images sans sous-titre : {caption_gaps(props)[:3]}")
    if wdata.get("unmatched_chars", 0):
        problems.append(f"{wdata['unmatched_chars']} caractère(s) du texte absents de l'alignement ElevenLabs")
    if words[-1]["end"] > ref_dur - 0.02:
        problems.append("dernier mot collé à la fin du fichier audio")
    if tail_db > -40:
        problems.append(f"fin d'audio non silencieuse ({tail_db:.0f} dBFS)")
    if duration < words[-1]["end"] + 0.2:
        problems.append("vidéo coupée avant la fin du dernier mot")
    results.append(check("Aucun mot coupé", not problems, "ok" if not problems else "; ".join(problems),
                         "tous les mots, entiers, dans la largeur",
                         f"{len(tokens)} mots, groupe le plus large {widest:.0f}/{max_width} px"
                         + (f" (Inter ExtraBold {cap['size']} px, rendu motion)" if mode == "motion" else "")))

    # Accents et caractères
    text = s["texte"]
    issues = []
    if unicodedata.normalize("NFC", text) != text:
        issues.append("texte non normalisé NFC")
    if MOJIBAKE.search(text) or MOJIBAKE.search(shown_text):
        issues.append("caractères mal encodés")
    if unicodedata.normalize("NFC", shown_text) != shown_text:
        issues.append("texte affiché non normalisé NFC")
    missing = measure.missing_glyphs(text + s["titre"] + shown_text)
    if missing:
        issues.append(f"glyphes absents de la police : {''.join(missing)}")
    if wdata["text"] != text:
        issues.append("audio verrouillé sur un texte différent de scripts.json")
    # Orthographe : le texte lu ET les étiquettes affichées (rendu motion).
    unknown = spell_warnings(text + ("\n" + "\n".join(overlay_texts) if mode == "motion" else ""))
    results.append(check("Accents et caractères", not issues, "ok" if not issues else "; ".join(issues),
                         "UTF-8 NFC, glyphes présents, aucun mojibake",
                         f"mots hors dictionnaire à relire : {', '.join(unknown)}" if unknown else
                         "aucun mot hors dictionnaire"))

    # Saturation et loudness
    integrated, true_peak = loudness(mp4)
    clipped = int(np.sum(np.abs(raw_samples(mp4)) >= 0.999))
    tol = q["loudness_tolerance"]
    target = cfg["loudness"]["integrated"]
    results.append(check("Pas de saturation", clipped == 0 and true_peak <= q["max_true_peak"],
                         f"true peak {true_peak:.1f} dBTP, {clipped} échantillon(s) écrêté(s)",
                         f"≤ {q['max_true_peak']} dBTP, 0 écrêtage"))
    results.append(check("Loudness", abs(integrated - target) <= tol, f"{integrated:.1f} LUFS",
                         f"{target:.0f} ± {tol:.0f} LUFS"))

    if mode == "motion":
        results += picture_checks(video_id, mp4, props)

    report = {
        "id": video_id,
        "mode": mode,
        "source": s["source"],
        "file": str(mp4.relative_to(OUTPUT.parent)),
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "ok": all(r["ok"] for r in results),
        "checks": results,
    }
    write_json(QA_DIR / f"{video_id}.json", report)
    write_report()
    print(f"{video_id} : QA {'OK' if report['ok'] else 'ÉCHEC'} (sous-titres : {mode})")
    for r in results:
        print(f"  {'✔' if r['ok'] else '✘'} {r['check']} : {r['value']}")
    return report


def write_report():
    lines = ["# Rapport qualité — vidéos WealthTech Horizon", ""]
    reports = [read_json(QA_DIR / f"{vid}.json") for vid in videos() if (QA_DIR / f"{vid}.json").exists()]
    lines += ["| Vidéo | Source | Résultat | Durée | Synchro | Loudness | Contrôlée le |", "|---|---|---|---|---|---|---|"]
    for r in reports:
        by = {c["check"]: c for c in r["checks"]}
        lines.append(f"| {r['id']} | {r['source']} | {'✅ OK' if r['ok'] else '❌ ÉCHEC'} | {by['Durée']['value']} | "
                     f"{by['Synchro sous-titres']['value']} | {by['Loudness']['value']} | {r['checked_at']} |")
    for r in reports:
        lines += ["", f"## {r['id']} ({r['source']}) — {'OK' if r['ok'] else 'ÉCHEC'}", "",
                  "| Contrôle | Résultat | Valeur | Attendu | Détail |", "|---|---|---|---|---|"]
        for c in r["checks"]:
            lines.append(f"| {c['check']} | {'✔' if c['ok'] else '✘'} | {c['value']} | {c['expected']} | "
                         f"{c['detail']} |")
    (OUTPUT / "qa_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("id")
    p.add_argument("--mode", choices=["auto", "motion", "classic"], default="auto",
                   help="source des sous-titres : motion.json (rendu motion) ou subs.ass (montage classique)")
    a = p.parse_args()
    report = qa_video(a.id, a.mode)
    raise SystemExit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
