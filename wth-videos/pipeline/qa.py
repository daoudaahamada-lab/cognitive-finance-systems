"""Contrôle qualité automatique d'une vidéo -> output/qa/Vxx.json et output/qa_report.md.

Trois modes, lus dans le MP4 lui-même : « story » (balise wth_mode=story, film Story : props de
build/Vxx/story_render.json), « motion » (rendu motion design : build/Vxx/motion.json), « classic » (subs.ass)."""
import argparse
import itertools
import math
import re
import subprocess
import unicodedata
from datetime import datetime, timezone

import numpy as np

from .common import OUTPUT, ROOT, build_dir, ffprobe, load_config, read_json, run, script, videos, write_json
from .motion import CAPTION_FONT, GENERATED, RENDER_SIDECAR, SHOTLISTS, clean_word, sha1_file
from .story import FONTS as STORY_FONTS, STORY_SIDECAR, STORYBOARDS, spec_path, spec_sha1
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


def story_sidecar(out_dir, mp4):
    """build/Vxx/story_render.json s'il décrit bien CE fichier (même empreinte), sinon None."""
    path = out_dir / STORY_SIDECAR
    if not path.exists():
        return None
    rec = read_json(path)
    return rec if rec.get("mp4_sha1") == sha1_file(mp4) else None


def caption_source(probe, mode="auto", sidecar=None, story=None):
    """Source des sous-titres à contrôler, déduite du MP4 lui-même (et non des dates des fichiers de build). Le film
    Story porte aussi le commentaire « Made with Remotion » : sa balise wth_mode=story (ou sa fiche
    story_render.json) est lue d'abord."""
    if mode != "auto":
        return mode
    if mp4_tags(probe).get("wth_mode") == "story" or story:
        return "story"
    return "motion" if is_motion_render(probe, sidecar) else "classic"


def props_captions(props):
    """Surbrillance (début en s dans la vidéo, mot affiché) et groupes affichés de props Remotion (images du film :
    l'image 0 de la vidéo est frameOffset)."""
    fps, off = props["fps"], props.get("frameOffset", 0)
    active = [((w["from"] - off) / fps, w["text"]) for g in props["captions"] for w in g["words"]]
    groups = [" ".join(w["text"] for w in g["words"]) for g in props["captions"]]
    return active, groups


def motion_captions(out_dir, path=None):
    """Surbrillance (début en s, mot affiché), groupes affichés et textes des éléments graphiques de motion.json."""
    props = read_json(path or out_dir / "motion.json")
    active, groups = props_captions(props)
    texts = [o.get(k, "") for o in props.get("overlays", []) for k in ("text", "flip_text")]
    texts += [t for o in props.get("overlays", []) for t in o.get("texts", [])]
    texts += [part.get("flip_text", "") for part in (props.get("endCard") or {}).values()]
    texts += [part.get("text", "") for part in (props.get("endCard") or {}).values()]
    return props, active, groups, [t for t in texts if t]


STORY_TEXT_KEYS = ("text", "key", "value", "title", "date", "sealText", "labels", "prefix", "suffix")


def entity_texts(props):
    """Textes affichés par les entités Story : paramètres p (étiquettes, rangées, documents, tampon, légendes,
    préfixe et suffixe d'un compteur) et valeurs texte des pistes du même nom (bascule de texte : piste `text` d'une
    pastille ou du type text du kit)."""
    out = []

    def add(v):
        if isinstance(v, str):
            out.append(v)
        elif isinstance(v, list):
            out.extend(t for t in v if isinstance(t, str))

    for e in props.get("entities", []):
        for k in STORY_TEXT_KEYS:
            add(e.get("p", {}).get(k))
            for key in e.get("t", {}).get(k, []):
                add(key.get("v"))
    return list(dict.fromkeys(t for t in out if t.strip()))


def story_inputs(out_dir):
    """Film Story : fiche build/Vxx/story_render.json -> (fiche, props du film avec sous-titres, surbrillance,
    groupes, textes à l'écran)."""
    path = out_dir / STORY_SIDECAR
    if not path.exists():
        raise SystemExit(f"{path} absent : le film Story n'a pas été rendu par pipeline.story (make story ID=…)")
    rec = read_json(path)
    if not rec.get("props"):
        raise SystemExit(f"{path} : pas de version avec sous-titres (relancer make story ID=… sans --no-captions)")
    props = read_json(ROOT / rec["props"])
    active, groups = props_captions(props)
    return rec, props, active, groups, entity_texts(props)


CAPTION_FILES = {"motion": "motion.json", "story": "props Story", "classic": "subs.ass"}


def story_render_check(video_id, mp4, probe, rec, props):
    """« Rendu Story à jour » : le MP4 contrôlé (et sa version sans sous-titres) est celui que décrivent les props,
    le storyboard et la mise en scène actuels (empreintes des balises wth_* du MP4, sinon de story_render.json), avec
    le nombre d'images des props. Les dates de fichiers ne comptent pas."""
    vs = next(st for st in probe["streams"] if st["codec_type"] == "video")
    frames = int(vs.get("nb_frames", 0))
    tags = mp4_tags(probe)
    stamp = {"props": tags.get("wth_props") or rec.get("props_sha1"),
             "storyboard": tags.get("wth_storyboard") or rec.get("storyboard_sha1"),
             "spec": tags.get("wth_spec") or rec.get("spec_sha1")}
    try:
        spec_now = spec_sha1(spec_path(video_id))
    except SystemExit:
        spec_now = None
    now = {"props": sha1_file(ROOT / rec["props"]), "storyboard": sha1_file(STORYBOARDS / f"{video_id}.json"),
           "spec": spec_now}
    stale = [k for k in now if stamp[k] != now[k]]
    problems = []
    if rec.get("mp4_sha1") != sha1_file(mp4):
        problems.append("story_render.json décrit un autre MP4")
    if frames != props["durationInFrames"]:
        problems.append(f"{frames} images pour {props['durationInFrames']} dans les props")
    nocap = ROOT / rec["nocap"] if rec.get("nocap") else None
    if not (nocap and nocap.exists()):
        problems.append("version sans sous-titres absente")
    else:
        if rec.get("nocap_sha1") != sha1_file(nocap):
            problems.append("version sans sous-titres modifiée depuis le rendu")
        if not rec.get("props_nocap") or rec.get("props_nocap_sha1") != sha1_file(ROOT / rec["props_nocap"]):
            stale.append("props sans sous-titres")
    ok = not stale and not problems and all(stamp.values())
    return check("Rendu Story à jour", ok,
                 f"{frames} images, empreintes {'identiques' if not stale else 'DIFFÉRENTES : ' + ', '.join(stale)}"
                 + ("" if all(stamp.values()) else " (MP4 sans empreinte de rendu)"),
                 f"{props['durationInFrames']} images (props), empreintes props + storyboard + mise en scène du rendu "
                 "= fichiers actuels, version sans sous-titres du même rendu",
                 "; ".join(problems + (["relancer make story"] if stale else [])) or
                 f"props {now['props'][:10]}, storyboard {now['storyboard'][:10]}, mise en scène {(now['spec'] or '?')[:10]}")


def story_staging_check(probe, props):
    """« Mise en scène complète » : le film Story livré couvre tout le storyboard. Refusé si le MP4 porte la balise
    wth_partial (rendu de travail --allow-partial) ou si ses props signalent une mise en scène incomplète : film
    partiel, scènes sans aucun temps fort, temps forts du storyboard sans événement, début non mis en scène."""
    meta = props.get("meta", {})
    staged = set(meta.get("staged_scenes", []))
    unstaged = meta.get("unstaged_scenes")
    if unstaged is None:   # props d'avant la balise : scènes du storyboard sans temps fort posé
        try:
            sb = read_json(ROOT / meta["storyboard"])
            unstaged = [s["id"] for s in sb["scenes"] if s["id"] not in staged]
        except (KeyError, OSError, ValueError):
            unstaged = ["storyboard illisible"]
    missing = meta.get("storyboard_beats_missing", [])
    before = meta.get("unstaged_before_frame")
    partial = mp4_tags(probe).get("wth_partial") == "1" or bool(meta.get("partial"))
    window = meta.get("window_frames", [None, None])
    full = props.get("frameOffset", 0) == 0 and window[0] == 0
    problems = [x for x in (
        "rendu de travail (--allow-partial)" if partial else "",
        "extrait, pas le film entier" if not full else "",
        f"scènes non mises en scène : {', '.join(unstaged)}" if unstaged else "",
        f"temps forts sans événement : {', '.join(missing[:6])}{' …' if len(missing) > 6 else ''}" if missing else "",
        f"rien n'est mis en scène avant l'image {before}" if before is not None else "") if x]
    return check("Mise en scène complète", not problems, "; ".join(problems) or
                 f"{len(staged)} scènes mises en scène, tous les temps forts posés",
                 "chaque scène du storyboard mise en scène, chaque temps fort avec son événement, pas de rendu partiel",
                 f"mise en scène {meta.get('spec', '?')}, storyboard {meta.get('storyboard', '?')}")


def caption_gaps(props, from_first_word=False):
    """Images sans sous-titre (il doit toujours y en avoir un, d'un groupe au suivant), en images du film.
    `from_first_word` (film Story) : compté à partir du premier mot, un groupe ne s'affichant jamais avant son premier
    mot (pipeline.story.caption_track) ; le rendu motion, lui, montre son premier groupe dès l'image 0."""
    off = props.get("frameOffset", 0)
    cursor, gaps = off, []
    if from_first_word and props["captions"]:
        cursor = max(off, min(g["from"] for g in props["captions"]))
    for g in props["captions"]:
        if g["from"] > cursor:
            gaps.append((cursor, g["from"]))
        cursor = max(cursor, g["to"])
    if cursor < off + props["durationInFrames"]:
        gaps.append((cursor, off + props["durationInFrames"]))
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
    out.append(karaoke_check(cap_masks, props["captions"], n, 0, "rouge"))
    return out


def karaoke_check(cap_masks, captions, n, off=0, colour="rouge"):
    """Le mot surligné (masque de la ligne de sous-titres décodée, image par image) change exactement à l'image du
    début de chaque mot, jamais avant, et il y en a toujours un à l'écran à partir du premier mot. `off` : image du
    film montrée par l'image 0 de la vidéo (props Story : frameOffset)."""
    onsets = sorted({w["from"] - off for g in captions for w in g["words"] if w["from"] - off > 0})
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
    first = max(0, min(w["from"] for g in captions for w in g["words"]) - off)
    blank = [i for i in range(first, n) if cap_masks[i].sum() < 15]  # avant le 1er mot : groupe sans surbrillance
    return check("Surbrillance à l'image près", not (late or early or missing or blank),
                 f"{len(onsets) - len(late) - len(early)}/{len(onsets)} changements à l'image exacte",
                 f"le mot {colour} change à l'image du début du mot, pas avant ; toujours un mot {colour} à l'écran",
                 "; ".join(x for x in (f"en retard : {late[:5]}" if late else "", f"en avance : {early[:5]}" if early else "",
                                        f"sans mot {colour} : {(missing or blank)[:5]}" if (missing or blank) else "") if x)
                 or "mesuré sur la ligne de sous-titres décodée")


# ---------- contrôles sur l'image décodée (film Story) ----------

STORY_SAFE = {"top": 160, "bottom": 380, "right": 940}  # px : bandeaux et colonne d'icônes de TikTok / Reels
SAFE_TOL = 0.003      # part des pixels d'une zone réservée que l'anticrénelage ou une ombre peut toucher
STORY_BAND = (160, 1270)  # bande d'action (au-dessus de la ligne de sous-titres), px pleine résolution
STORY_CAP_Y = 1270    # au-dessus : la version sans sous-titres doit être identique à la version avec
ACTION_MIN = 0.01     # part minimale de pixels hors fond dans la bande d'action, à chaque image
FROZEN_MAX = 3.5      # s : image figée la plus longue admise, hors carte de fin
MOVE_LEVEL = 16       # niveaux : un pixel a bougé d'une image à la suivante (au-delà du bruit du codage)
MOVE_PIXELS = 12      # pixels (mi-résolution) qui doivent bouger pour que l'image ne soit pas figée
NOCAP_PSNR = 40.0     # dB
CONTENT_LEVEL = 28    # niveaux : écart au fond ivoire ET à la grille au-delà duquel un pixel est du contenu


def hex_rgb(c):
    return np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)], np.int16)


def accent_mask(rgb, colours, tol=48):
    """Pixels d'une des couleurs d'accent (#RRGGBB), à `tol` niveaux près : généralise red_mask aux sous-titres Story
    (mot prononcé en cyan profond, mots d'alerte en rouge)."""
    px = rgb.astype(np.int16)
    mask = np.zeros(rgb.shape[:2], bool)
    for c in colours:
        mask |= np.abs(px - hex_rgb(c)).max(-1) <= tol
    return mask


def content_mask(rgb, style):
    """Pixels qui ne sont ni le fond ivoire ni une ligne de grille (marge du codage et du sous-échantillonnage)."""
    px = rgb.astype(np.int16)
    d = np.minimum(np.abs(px - hex_rgb(style["bg"])).max(-1), np.abs(px - hex_rgb(style["grid"]["color"])).max(-1))
    return d > CONTENT_LEVEL


def still_runs(moving, fps, min_s=0.5):
    """Tenues : [(première image, dernière image)] des suites d'images figées d'au moins `min_s` s. `moving[i]` : vrai
    si l'image i diffère de la précédente."""
    runs, start = [], None
    for i, m in enumerate(list(moving) + [True]):
        if not m and start is None:
            start = i - 1 if i > 0 else 0
        elif m and start is not None:
            if (i - 1 - start + 1) / fps >= min_s:
                runs.append((start, i - 1))
            start = None
    return runs


def moved(prev, cur):
    """L'image a bougé : au moins MOVE_PIXELS pixels changent de plus de MOVE_LEVEL niveaux."""
    return int((np.abs(cur.astype(np.int16) - prev.astype(np.int16)).max(-1) > MOVE_LEVEL).sum()) >= MOVE_PIXELS


def end_card_frame(props):
    """Image de la vidéo où commence la dernière scène du storyboard (carte de fin), ou None."""
    try:
        sb = read_json(ROOT / props["meta"]["storyboard"])
        return round(sb["scenes"][-1]["t_start"] * props["fps"]) - props.get("frameOffset", 0)
    except (KeyError, IndexError, OSError, ValueError):
        return None


def story_picture_checks(mp4, nocap, props):
    """Contrôles mesurés sur les images décodées du film Story (mi-résolution) :
    1. surbrillance karaoké (cyan profond / rouge d'alerte) qui change à l'image exacte du début de chaque mot ;
    2. zones réservées vides sur la version sans sous-titres : 160 px du haut, 380 px du bas, x > 940 ;
    3. aucune image figée plus de 3,5 s, hors carte de fin ;
    4. version sans sous-titres = version avec, hors bande des sous-titres (PSNR ≥ 40 dB sur y < 1270), même nombre
       d'images ;
    5. bande d'action jamais vide."""
    fps, total, off = props["fps"], props["durationInFrames"], props.get("frameOffset", 0)
    style, capst = props["style"], props["style"]["caption"]
    k = HALF[0] / props["width"]
    c0, c1 = (round(y * k) for y in CAP_BAND)
    b0, b1 = (round(y * k) for y in STORY_BAND)
    top, bottom = round(STORY_SAFE["top"] * k), round((props["height"] - STORY_SAFE["bottom"]) * k)
    right = round(STORY_SAFE["right"] * k)
    y_cap = round(STORY_CAP_Y * k)
    accents = [capst["active"], capst["alert"]]
    cap_masks, moving, psnr, action = [], [], [], []
    safe = {"haut": [], "bas": [], "droite": []}
    n_cap = n_nocap = 0
    prev = None
    for a, b in itertools.zip_longest(decoded_frames(mp4), decoded_frames(nocap)):
        n_cap += a is not None
        n_nocap += b is not None
        if a is None or b is None:
            continue
        cap_masks.append(accent_mask(a[c0:c1], accents) & ~accent_mask(b[c0:c1], accents))
        cm = content_mask(b, style)
        safe["haut"].append(float(cm[:top].mean()))
        safe["bas"].append(float(cm[bottom:].mean()))
        safe["droite"].append(float(cm[top:bottom, right:].mean()))
        action.append(float(cm[b0:b1].mean()))
        mse = float(np.mean((a[:y_cap].astype(np.float32) - b[:y_cap].astype(np.float32)) ** 2))
        psnr.append(99.0 if mse == 0 else 10 * math.log10(255 ** 2 / mse))
        moving.append(True if prev is None else moved(prev, b))
        prev = b
    n = len(cap_masks)
    out = []

    # 1. Karaoké.
    out.append(karaoke_check(cap_masks, props["captions"], n, off, "surligné"))

    # 2. Zones réservées.
    worst = {z: (max(v), int(np.argmax(v))) for z, v in safe.items() if v}
    bad = {z: w for z, w in worst.items() if w[0] > SAFE_TOL}
    out.append(check("Zones réservées dégagées", not bad,
                     "; ".join(f"{z} {w[0]:.2%} (image {w[1]})" for z, w in worst.items()),
                     f"≤ {SAFE_TOL:.1%} de pixels hors fond dans les {STORY_SAFE['top']} px du haut, les "
                     f"{STORY_SAFE['bottom']} px du bas et à droite de x = {STORY_SAFE['right']} (version sans sous-titres)",
                     "interface TikTok / Reels : rien d'important sous les bandeaux ni sous la colonne d'icônes"))

    # 3. Image figée.
    runs = still_runs(moving, fps)
    end = end_card_frame(props)
    long = [(s, e) for s, e in runs if (e - s + 1) / fps > FROZEN_MAX
            and not (e >= n - 1 and end is not None and s >= end)]
    longest = max(runs, key=lambda r: r[1] - r[0], default=None)
    out.append(check("Jamais d'image figée", not long,
                     f"tenue la plus longue {(longest[1] - longest[0] + 1) / fps:.1f} s (images {longest[0]}-{longest[1]})"
                     if longest else "aucune tenue ≥ 0,5 s",
                     f"aucune image figée plus de {FROZEN_MAX} s, hors carte de fin (dès l'image {end})",
                     "; ".join(f"{(e - s + 1) / fps:.1f} s images {s}-{e}" for s, e in long[:5])
                     or f"{len(runs)} tenues ≥ 0,5 s (au moins {MOVE_PIXELS} px à mi-résolution qui changent de plus "
                        f"de {MOVE_LEVEL} niveaux = mouvement)"))

    # 4. Version sans sous-titres conforme.
    low = (min(psnr), int(np.argmin(psnr))) if psnr else (0.0, 0)
    same_n = n_cap == n_nocap == total
    out.append(check("Version sans sous-titres conforme", same_n and low[0] >= NOCAP_PSNR,
                     f"PSNR {low[0]:.1f} dB au pire (image {low[1]}), {n_cap} / {n_nocap} images",
                     f"≥ {NOCAP_PSNR:.0f} dB au-dessus de y = {STORY_CAP_Y}, {total} images dans les deux versions",
                     f"médiane {np.median(psnr):.1f} dB" if psnr else ""))

    # 5. Bande d'action jamais vide.
    lo = (min(action), int(np.argmin(action))) if action else (0.0, 0)
    out.append(check("Bande d'action jamais vide", lo[0] >= ACTION_MIN, f"{lo[0]:.1%} au pire (image {lo[1]})",
                     f"≥ {ACTION_MIN:.0%} de pixels hors fond entre y = {STORY_BAND[0]} et {STORY_BAND[1]}, à chaque image",
                     f"médiane {np.median(action):.1%}" if action else ""))
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
    mode = caption_source(probe, mode, sidecar, story_sidecar(out_dir, mp4))
    remotion = mode in ("motion", "story")
    if mode == "motion":
        props, active, groups, overlay_texts = motion_captions(out_dir)
        cap = props["style"]["caption"]
        measure = FontMeasure(CAPTION_FONT, cap["size"], cap["tracking_em"])
        max_width = cap["max_width"]
        shown_text = "\n".join(groups + overlay_texts)
    elif mode == "story":
        rec, props, active, groups, overlay_texts = story_inputs(out_dir)
        cap = props["style"]["caption"]
        # Sous-titres Story : Inter Bold, sans interlettrage (pipeline.story.caption_track).
        measure = FontMeasure(STORY_FONTS / "Inter-Bold.otf", cap["size"], 0)
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
    max_duration = (q.get("max_duration_by_video") or {}).get(video_id, q["max_duration"])
    results.append(check("Durée", q["min_duration"] <= duration <= max_duration, f"{duration:.2f} s",
                         f"{q['min_duration']:.0f} à {max_duration:.0f} s"))
    vs = next(st for st in probe["streams"] if st["codec_type"] == "video")
    aus = next((st for st in probe["streams"] if st["codec_type"] == "audio"), {})
    fmt = f"{vs['codec_name']} {vs['width']}x{vs['height']} {vs['avg_frame_rate']} {vs['pix_fmt']} + {aus.get('codec_name')}"
    want = f"h264 1080x1920 {cfg['video']['fps']}/1 yuv420p + aac"
    colour = {k: vs.get(k, "?") for k in ("color_range", "color_space", "color_primaries", "color_transfer")}
    audio_fmt = f"{aus.get('sample_rate', '?')} Hz, {round(int(aus.get('bit_rate', 0)) / 1000)} kb/s"
    fmt_problems = [] if fmt == want else [fmt]
    if remotion:
        # Un rendu Remotion est toujours marqué BT.709 plage limitée (remotion.config.ts, setColorSpace).
        bad = {k: v for k, v in colour.items() if v != ("tv" if k == "color_range" else "bt709")}
        if bad:
            fmt_problems.append(f"couleur {bad}")
    results.append(check("Format", not fmt_problems, f"{fmt}, profil {vs.get('profile')}, "
                         f"{colour['color_range']}/{colour['color_space']}, audio {audio_fmt}", want +
                         (", BT.709 plage tv" if remotion else ""), "; ".join(fmt_problems)))
    if mode == "story":
        results.append(story_render_check(video_id, mp4, probe, rec, props))
        results.append(story_staging_check(probe, props))
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
    if len(active) == len(words) and remotion:
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
                         f"sous-titres ({CAPTION_FILES[mode]})/alignement + image : "
                         f"{sub_err * 1000:.0f} ms ; décalage audio MP4 : "
                         f"{offset * 1000:.0f} ms ; alignement {source} vérifié sur {len(pauses)} pauses mesurées"
                         + (f", conflits : {'; '.join(conflicts[:3])}" if conflicts else ", aucun conflit")))

    # Mots coupés
    tokens = [wdata["text"][a:b] for a, b in tokenize(wdata["text"])]
    if remotion:
        tokens = [clean_word(t) for t in tokens]  # sous-titres Remotion : ponctuation retirée
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
    gaps = caption_gaps(props, from_first_word=mode == "story") if remotion else []
    if gaps:
        problems.append(f"images sans sous-titre : {gaps[:3]}")
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
                         + (f" (Inter ExtraBold {cap['size']} px, rendu motion)" if mode == "motion" else
                            f" (Inter Bold {cap['size']} px, film Story)" if mode == "story" else "")))

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
    # Orthographe : le texte lu ET les étiquettes affichées (rendu motion ou Story).
    unknown = spell_warnings(text + ("\n" + "\n".join(overlay_texts) if remotion else ""))
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
    elif mode == "story":
        nocap = ROOT / rec["nocap"] if rec.get("nocap") else None
        if nocap and nocap.exists():
            results += story_picture_checks(mp4, nocap, props)
        else:
            results.append(check("Version sans sous-titres conforme", False, "absente", "build/Vxx/story/"
                                 "film_sans_sous_titres.mp4 (make story ID=…)", "contrôles image non faits"))

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
    p.add_argument("--mode", choices=["auto", "story", "motion", "classic"], default="auto",
                   help="source des sous-titres : props Story (story_render.json), motion.json (rendu motion) ou "
                        "subs.ass (montage classique)")
    a = p.parse_args()
    report = qa_video(a.id, a.mode)
    raise SystemExit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
