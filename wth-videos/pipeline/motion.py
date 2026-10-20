"""Rendu motion design (Remotion) : illustrations en verre sur fond noir, sous-titres karaoké, plans calés sur les mots.

    python3 -m pipeline.motion V01            assets + props + rendu Remotion + mixage audio -> output/WTH-V01.mp4
    python3 -m pipeline.motion V01 --props    seulement assets + build/V01/motion.json (pas de rendu)

Entrées : scripts/shotlists/Vxx.json (plans, événements calés sur des mots), build/Vxx/words.json,
build/Vxx/audio.wav (refait par render.normalize_audio s'il manque). Sorties : motion/public/generated/Vxx/
(illustrations prêtes pour Remotion, fond), build/Vxx/motion.json (props), build/Vxx/motion_silent.mp4, output/WTH-Vxx.mp4.
"""
import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import time
import unicodedata
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageFont

from .common import ASSETS, OUTPUT, ROOT, build_dir, ffprobe, load_config, read_json, run, script, write_json
from .subs import WEAK

MOTION = ROOT / "motion"
GENERATED = MOTION / "public" / "generated"
SHOTLISTS = ROOT / "scripts" / "shotlists"
ILLUSTRATIONS = ASSETS / "illustrations"
ASSET_VERSION = 4  # à incrémenter si la recette des illustrations change
BG_VERSION = 2     # à incrémenter si la recette du fond change (2 : lignes de grille jusqu'aux bords haut et gauche)
BROWSER_FILE = MOTION / "browser.json"  # chemin par défaut du navigateur, partagé avec remotion.config.ts et stills.mjs

# Direction A « Noir galerie » : jetons de style partagés par Python (mesures, QA) et Remotion (rendu).
STYLE = {
    "bg": "#0A0A0B",
    "cream": "#F6F0E4",
    "accent": "#FF4A5C",   # mot prononcé et traits fins (anneaux, crochets, ligne de lecture, repère) : 6,0:1 sur le fond
    # Rouge plein unique de TOUS les aplats (pastilles, badges, protagoniste, « ? », point de saisie, secteur, bouton) :
    # le rouge de marque #C8102E éclairci pour l'écran noir (4,0:1 sur le fond au lieu de 3,4:1, luminance 68 au lieu
    # de 57), texte crème dessus à 4,4:1 (texte ≥ 34 px ExtraBold).
    "fill": "#DC1835",
    "fill_shadow": "#7A0E14",
    "font_family": "WTH Inter",
    "grid": {"pitch": 36, "line": 2, "opacity": 0.075},
    "lift": {"amount": 0.022, "cx": 540, "cy": 800, "rx": 560, "ry": 620},
    "stage": {"cx": 540, "cy": 800, "box": [720, 600]},
    "hero_mask": {"top0": 130, "top1": 230, "bottom0": 1150, "bottom1": 1262},
    "caption": {"size": 66, "weight": 800, "tracking_em": -0.015, "baseline": 1350, "max_width": 760,
                "max_words": 3, "max_words_hard": 4, "gap_break": 0.15},
    # Passage de héros (morph de la référence : les formes sortantes, opaques, rétrécissent et les entrantes les
    # recouvrent) : l'entrant est opaque dès sa 1re image et grandit 0,7 -> 1 par-dessus le sortant, qu'on ne voit donc
    # jamais à travers lui (aucun fondu enchaîné) ; le sortant rétrécit et s'efface en 4,5 images (ease-in-out :
    # 0,96 / 0,65 / 0,15 / 0), visible seulement autour de l'entrant ; la bande garde ≥ 0,8 de sa luminance.
    "motion": {"enter": 11, "enter_fade": 1, "enter_from": 0.7, "exit": 8, "exit_fade": 4.5, "exit_ease": "in-out",
               "exit_to": 0.8, "move": 16, "tilt": 14, "pop": 9,
               "tone": 12, "fade": 6},
    # Indicateur d'étapes : carte de chapitre au centre (« Numéro N » de la référence : rangée ~65 % de la largeur,
    # protagoniste ~21 %) et rappel en haut. Le héros qui cède la scène à un chapitre rétrécit (0,4) vers la place
    # du protagoniste et s'efface en 9 images.
    "steps": {"small": {"d": 26, "red": 34, "gap": 64, "stroke": 3, "opacity": 0.6},
              "big": {"d": 112, "red": 250, "gap": 270, "stroke": 7, "opacity": 1.0},
              "enter": 11, "leave": 3, "slide": 16,
              "hero_exit": {"to": 0.4, "dur": 11, "fade": 9}},
}
BREAK_AFTER = tuple(".,;:!?…")
# Mots qu'on évite aussi en fin de groupe, en plus de subs.WEAK (« erreur devant | le client »).
WEAK_EXTRA = {"devant", "qu’une", "qu’un", "d’une", "d’un", "chaque", "plus", "très", "sans", "vers", "chez"}
STRIP = set(".,;:!?…«»\"“”()[]")
CAPTION_FONT = Path(__file__).resolve().parent.parent / "motion" / "public" / "fonts" / "Inter-ExtraBold.otf"


# ---------- illustrations ----------

def _taper(n, edge):
    t = np.ones(n, np.float32)
    ramp = (0.5 - 0.5 * np.cos(np.linspace(0, np.pi, edge))).astype(np.float32)
    t[:edge] = ramp
    t[-edge:] = ramp[::-1]
    return t


HALO_PAD = 100     # marge transparente ajoutée autour de la source avant de reconstruire le halo
SOURCE_TAPER = 100  # biseau (cosinus) du halo d'origine contre les bords de l'image source
EDGE_TAPER = 24     # biseau final du halo seul, contre les bords du canevas agrandi


def bake_illustration(src, bg_hex=STYLE["bg"], warnings=None):
    """Illustration SeamUI -> une seule image RGBA (alpha droit) qui, posée sur le fond, rend exactement
    la maquette A : halo reconstruit (RGB x (1-a) x masque de diffusion x biseau des bords) en mode « screen »,
    puis l'objet par-dessus.

    Le halo d'origine vit dans le RGB des pixels d'alpha 0 et touche souvent le bord du canevas : on le
    reconstruit, puis on convertit le « screen » sur la couleur de fond B en couleur + alpha
    (ah = max(h), ch = (h + B (ah - h)) / ah), exact sur B et à moins de 5 niveaux sur les lignes de grille.
    Le halo est donc dans la même image que l'objet : il suit toutes ses transformations, sans rectangle.

    La source est d'abord entourée de HALO_PAD px transparents : la diffusion tirée de la silhouette continue
    dans cette marge. Là où le biseau des bords de la source efface le halo d'origine (objet à moins de 100 px
    du bord, ex. le haut du globe), on le remplace par un halo de synthèse de la couleur moyenne du halo près
    de l'objet. Les biseaux ne touchent jamais l'objet lui-même.
    """
    im = Image.open(src).convert("RGBA")
    rgb0 = np.asarray(im.convert("RGB"), np.float32) / 255
    a0 = np.clip(np.asarray(im.getchannel("A"), np.float32) / 250.0, 0, 1)  # alpha max 252-254 : 250 = opaque
    h0, w0 = a0.shape
    P = HALO_PAD
    ys0, xs0 = np.where(a0 > 0.5)
    # Une source sans vraie transparence (RGB, PNG aplati) deviendrait un rectangle opaque sur la grille.
    clear = float((a0 < 0.05).mean())
    cover = ((xs0.max() - xs0.min() + 1) * (ys0.max() - ys0.min() + 1)) / (w0 * h0) if len(xs0) else 1.0
    if clear < 0.20 or cover > 0.95:
        raise SystemExit(f"{Path(src).name} : pas de vraie transparence ({clear:.0%} de pixels transparents, objet sur "
                         f"{cover:.0%} du canevas) : il faut le PNG détouré (RGBA) d'origine, pas une image aplatie")
    margin = min(int(xs0.min()), int(ys0.min()), w0 - 1 - int(xs0.max()), h0 - 1 - int(ys0.max()))
    if margin < EDGE_TAPER and warnings is not None:
        warnings.append(f"{Path(src).name} : objet à {margin} px du bord de l'image source (halo de synthèse de ce côté ; vérifier que l'objet n'y est pas coupé)")
    rgb = np.zeros((h0 + 2 * P, w0 + 2 * P, 3), np.float32)
    a = np.zeros((h0 + 2 * P, w0 + 2 * P), np.float32)
    rgb[P:P + h0, P:P + w0], a[P:P + h0, P:P + w0] = rgb0, a0
    h, w = a.shape
    taper_src = np.zeros((h, w), np.float32)
    taper_src[P:P + h0, P:P + w0] = _taper(h0, SOURCE_TAPER)[:, None] * _taper(w0, SOURCE_TAPER)[None, :]

    sil = Image.fromarray(((a > 0.5) * 255).astype(np.uint8), "L")
    r1 = np.asarray(sil.filter(ImageFilter.GaussianBlur(40)), np.float32) / 255
    r2 = np.asarray(sil.filter(ImageFilter.GaussianBlur(100)), np.float32) / 255
    m = np.clip(np.maximum(r1 * 1.6, r2 * 1.1), 0, 1) ** 1.3
    halo = rgb * ((1 - a) * m * taper_src)[..., None]
    # Halo de synthèse là où la source manque : couleur moyenne du halo d'origine près de l'objet.
    near = (a < 0.05) & (m > 0.3) & (taper_src > 0.999)
    wgt = (m * m)[near]
    glow = (rgb[near] * wgt[:, None]).sum(0) / max(float(wgt.sum()), 1e-6) if near.any() else np.zeros(3, np.float32)
    halo = halo + glow[None, None, :] * ((1 - a) * m * (1 - taper_src))[..., None]

    B = np.array([int(bg_hex[i:i + 2], 16) for i in (1, 3, 5)], np.float32) / 255
    ah = halo.max(-1)
    ch = (halo + B * (ah[..., None] - halo)) / np.maximum(ah, 1e-6)[..., None]
    # Bords du canevas agrandi : seul le halo est biseauté, jamais l'objet.
    ah *= _taper(h, EDGE_TAPER)[:, None] * _taper(w, EDGE_TAPER)[None, :]
    A = a + ah * (1 - a)
    C = (rgb * a[..., None] + ch * (ah * (1 - a))[..., None]) / np.maximum(A, 1e-6)[..., None]
    # Quantification avec tramage de l'alpha (évite les paliers dans la diffusion du halo).
    rng = np.random.default_rng(1234)
    A8 = np.where(A > 0, np.floor(A * 255 + rng.random(A.shape, dtype=np.float32)), 0)
    A8 = np.clip(A8, 0, 255).astype(np.uint8)
    C8 = np.clip(np.round(C * 255), 0, 255).astype(np.uint8)
    C8[A8 == 0] = 0
    out = np.dstack([C8, A8])

    ys, xs = np.where(a > 0.5)
    box = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
    nz_y, nz_x = np.where(A8 > 0)
    pad = 2
    crop = [max(int(nz_x.min()) - pad, 0), max(int(nz_y.min()) - pad, 0),
            min(int(nz_x.max()) + 1 + pad, w), min(int(nz_y.max()) + 1 + pad, h)]
    tile = Image.fromarray(out, "RGBA").crop(crop)
    # Marge transparente garantie autour de l'image (échantillonnage bilinéaire du navigateur).
    canvas = Image.new("RGBA", (tile.width + 2 * pad, tile.height + 2 * pad), (0, 0, 0, 0))
    canvas.paste(tile, (pad, pad))
    ox, oy = crop[0] - pad, crop[1] - pad
    rows = [[y - oy, x0 - ox, x1 - ox] for y, x0, x1 in object_rows(a)]
    return canvas, [box[0] - ox, box[1] - oy, box[2] - ox, box[3] - oy], rows


def _digest(*parts):
    h = hashlib.sha1()
    for p in parts:
        h.update(str(p).encode())
    return h.hexdigest()[:12]


def prepare_assets(video_id, names, warnings=None):
    """Une image prête pour Remotion par illustration utilisée (mise en cache par contenu source + recette)."""
    out_dir = GENERATED / video_id
    out_dir.mkdir(parents=True, exist_ok=True)
    meta = {}
    for name in sorted(set(names)):
        src = ILLUSTRATIONS / f"{name}.png"
        if not src.exists():
            raise SystemExit(f"Illustration absente : {src}")
        key = _digest(ASSET_VERSION, STYLE["bg"], src.stat().st_size, src.stat().st_mtime_ns)
        png, info = out_dir / f"{name}.png", out_dir / f"{name}.json"
        if png.exists() and info.exists() and read_json(info).get("key") == key:
            meta[name] = read_json(info)
            if warnings is not None:
                warnings += meta[name].get("notes", [])
            continue
        t0 = time.time()
        notes = []
        img, box, rows = bake_illustration(src, warnings=notes)
        img.save(png, optimize=False, compress_level=6)
        meta[name] = {"key": key, "src": f"generated/{video_id}/{name}.png", "w": img.width, "h": img.height,
                      "box": box, "notes": notes, "rows": rows}
        write_json(info, meta[name])
        if warnings is not None:
            warnings += notes
        print(f"  illustration {name} : {img.width}x{img.height}, objet {box} ({time.time() - t0:.1f} s)")
    # Les illustrations préparées que le plan n'utilise plus sortent du dossier (copié dans chaque bundle Remotion).
    keep = {f"{n}.{ext}" for n in names for ext in ("png", "json")} | {"bg.png", "bg.json"}
    for f in out_dir.iterdir():
        if f.is_file() and f.name not in keep:
            f.unlink()
    return meta


def make_background(video_id, width, height):
    """Fond plat #0A0A0B, grille fixe de 36 px ancrée en haut à gauche, léger halo neutre tramé."""
    out = GENERATED / video_id / "bg.png"
    key = _digest(BG_VERSION, json.dumps(STYLE["grid"]), json.dumps(STYLE["lift"]), STYLE["bg"], width, height)
    info = out.with_suffix(".json")
    if out.exists() and info.exists() and read_json(info).get("key") == key:
        return f"generated/{video_id}/bg.png"
    g, lift = STYLE["grid"], STYLE["lift"]
    bg = np.array([int(STYLE["bg"][i:i + 2], 16) for i in (1, 3, 5)], np.float32)
    cream = np.array([int(STYLE["cream"][i:i + 2], 16) for i in (1, 3, 5)], np.float32)
    yy, xx = np.mgrid[0:height, 0:width].astype(np.float32)
    d2 = ((xx - lift["cx"]) / lift["rx"]) ** 2 + ((yy - lift["cy"]) / lift["ry"]) ** 2
    img = bg + np.exp(-d2)[..., None] * (lift["amount"] * 255)
    # Lignes de 2 px : x = 36k-1 et 36k (k >= 1), idem en y ; jamais déplacées. Le bord du cadre (k = 0) n'a pas
    # de ligne, mais chaque ligne court jusqu'aux quatre bords (le masque ne vise que la ligne de bord elle-même).
    p, lw = g["pitch"], g["line"]
    on_x = ((xx + lw // 2) % p) < lw
    on_y = ((yy + lw // 2) % p) < lw
    line = (on_x & (xx >= p - lw)) | (on_y & (yy >= p - lw))
    img = img + line[..., None] * g["opacity"] * (cream - img)
    rng = np.random.default_rng(7)
    noise = (rng.random(img.shape[:2], dtype=np.float32) + rng.random(img.shape[:2], dtype=np.float32) - 1.0)
    img = img + noise[..., None] * 0.75  # tramage triangulaire ±0,75 niveau : pas de paliers dans le halo
    Image.fromarray(np.clip(np.round(img), 0, 255).astype(np.uint8), "RGB").save(out)
    write_json(info, {"key": key})
    return f"generated/{video_id}/bg.png"


# ---------- sous-titres ----------

def clean_word(word):
    """Mot affiché : sans ponctuation (sauf apostrophes et traits d'union), espaces insécables retirées."""
    w = word.replace("\u00a0", " ").replace("\u202f", " ")
    return "".join(ch for ch in w if ch not in STRIP).strip()


class CaptionMeasure:
    """Largeur réelle d'un groupe : Inter ExtraBold à la taille du rendu, avec l'interlettrage CSS."""

    def __init__(self, size=None, tracking_em=None, font_file=CAPTION_FONT):
        cap = STYLE["caption"]
        self.size = size or cap["size"]
        self.tracking = (cap["tracking_em"] if tracking_em is None else tracking_em) * self.size
        self.font = ImageFont.truetype(str(font_file), self.size)

    def width(self, text):
        # Chrome ajoute letter-spacing après chaque caractère, espaces compris.
        return self.font.getlength(text) + self.tracking * len(text)


def _fixed_groups(words, overrides):
    """Découpes imposées par le plan (« captions.groups ») : {index du premier mot: [groupes d'index]}.

    Chaque entrée est une suite de groupes consécutifs écrits comme à l'écran, ex.
    ["Abonne-toi", "pour comprendre", "ton argent"] ; elle remplace la découpe automatique de ces mots
    (expressions figées, « valent mieux », ou ponctuation qu'on choisit d'enjamber).
    """
    keys = [_norm(w["w"]) for w in words]
    fixed, used = {}, set()
    for run in overrides or []:
        toks = [_norm(t) for g in run for t in g.split()]
        n = len(toks)
        start = next((i for i in range(len(keys) - n + 1)
                      if keys[i:i + n] == toks and not used & set(range(i, i + n))), None)
        if start is None:
            raise SystemExit(f"Découpe de sous-titres imposée introuvable dans le texte : {run}")
        k, groups = start, []
        for g in run:
            m = len(g.split())
            groups.append(list(range(k, k + m)))
            k += m
        used |= set(range(start, k))
        fixed[start] = groups
    return fixed


def caption_groups(words, measure, cap=STYLE["caption"], overrides=None):
    """Groupes de 2-3 mots (4 au plus), coupés aux ponctuations et aux silences > 0,15 s.

    Chaque phrase est découpée par programmation dynamique : le moins de groupes possible, sans groupe d'un
    mot, sans article ni préposition en fin de groupe, sans groupe trop court (< 0,5 s) ni trop large.
    Les découpes imposées par le plan (`overrides`, voir _fixed_groups) passent avant.
    """
    fixed = _fixed_groups(words, overrides)
    phrases, cur = [], []
    i = 0
    while i < len(words):
        if i in fixed:
            if cur:
                phrases.append(cur)
                cur = []
            phrases += [("fixed", g) for g in fixed[i]]
            i = fixed[i][-1][-1] + 1
            continue
        w = words[i]
        if cur:
            prev = words[i - 1]
            if prev["w"].rstrip("\u00a0\u202f ").endswith(BREAK_AFTER) or w["start"] - prev["end"] > cap["gap_break"]:
                phrases.append(cur)
                cur = []
        cur.append(i)
        i += 1
    if cur:
        phrases.append(cur)

    def cost(ph, a, b):
        idx = ph[a:b]
        n = b - a
        c = 1.0
        width = measure.width(" ".join(clean_word(words[i]["w"]) for i in idx))
        if width > cap["max_width"]:
            c += 100 if n > 1 else 0
        c += max(0.0, width - 680) / 120  # préférence pour des lignes courtes
        if n > cap["max_words_hard"]:
            c += 100
        if n == 1 and len(ph) > 1:
            c += 2.5
        if n == cap["max_words_hard"]:
            c += 0.8
        if b < len(ph) and clean_word(words[idx[-1]]["w"]).lower() in WEAK | WEAK_EXTRA:
            # Plus cher qu'un groupe d'un mot : « Abonne-toi | pour comprendre » plutôt que « Abonne-toi pour | … ».
            c += 3.5
        end = words[ph[b]]["start"] if b < len(ph) else words[idx[-1]]["end"]
        if end - words[idx[0]]["start"] < 0.5 and len(ph) > 1:
            c += 1.0
        return c

    groups = []
    for ph in phrases:
        if isinstance(ph, tuple):
            groups.append(ph[1])
            continue
        n = len(ph)
        best = [0.0] + [math.inf] * n
        back = [0] * (n + 1)
        for b in range(1, n + 1):
            for a in range(max(0, b - cap["max_words_hard"]), b):
                c = best[a] + cost(ph, a, b)
                if c < best[b]:
                    best[b], back[b] = c, a
        cuts, b = [], n
        while b > 0:
            cuts.append((back[b], b))
            b = back[b]
        groups += [ph[a:b] for a, b in reversed(cuts)]
    return groups


def caption_track(words, fps, total_frames, measure, overrides=None):
    groups = caption_groups(words, measure, overrides=overrides)
    out = []
    for gi, g in enumerate(groups):
        frames = []
        for i in g:
            f = round(words[i]["start"] * fps)
            if frames and f <= frames[-1]:
                f = frames[-1] + 1
            frames.append(f)
        out.append({"words": [{"text": clean_word(words[i]["w"]), "i": i, "from": f} for i, f in zip(g, frames)]})
    for gi, g in enumerate(out):
        g["from"] = 0 if gi == 0 else g["words"][0]["from"]
    for gi, g in enumerate(out):
        g["to"] = out[gi + 1]["from"] if gi + 1 < len(out) else total_frames
        text = " ".join(w["text"] for w in g["words"])
        g["width"] = round(measure.width(text), 1)
    return out


# ---------- plans ----------

def _norm(s):
    return unicodedata.normalize("NFC", clean_word(s)).replace("’", "'")


class WordClock:
    """Résout « at » (mot cherché en avant, sensible à la casse, ou index) en index de mot et en image."""

    def __init__(self, words, fps):
        self.words, self.fps = words, fps
        self.keys = [_norm(w["w"]) for w in words]

    def index(self, at, start=0):
        if isinstance(at, int):
            return at
        q = _norm(at)
        for i in range(start, len(self.keys)):
            if self.keys[i] == q:
                return i
        raise SystemExit(f"Mot « {at} » introuvable après le mot n° {start} ({self.words[start]['w']!r})")

    def frame(self, i):
        return round(self.words[i]["start"] * self.fps)


HERO_EVENTS = {"move", "tilt", "tone", "shake"}
OVERLAY_TYPES = {"dot", "dots", "ring", "bar", "sector", "brackets", "scan", "pill", "badge", "qmark", "ticks",
                 "typing", "chips", "leader"}
FRAME_KEYS = ("fill_at", "flip_at", "tilt_at", "tick_at", "end", "until", "press_at", "go_at")
# Illustrations propres à un carrousel : WTH-<carrousel>-<slide>. Une vidéo n'utilise que celles de SON carrousel
# (scripts.json « source ») et les illustrations génériques (sans préfixe WTH-) : jamais l'image d'un autre
# épisode de la série (ex. l'image d'accroche de V02 « validée » dans V01).
CAROUSEL_ASSET = re.compile(r"^(WTH-\d{3})-\d+$")
# Zone utile du héros : l'objet opaque reste au-dessus de la bande de sous-titres (le masque du calque héros
# commence à fondre à hero_mask.bottom0), et sous le haut du cadre (hero_mask.top1).
HERO_BOTTOM = STYLE["hero_mask"]["bottom0"] - 10
HERO_TOP = STYLE["hero_mask"]["top1"]
RAIL_X, RAIL_Y = 940, (800, 1540)  # colonne d'icônes TikTok / Reels à droite


def object_rows(a, step=8):
    """Profil de l'objet (alpha > 0,5) : [y, x min, x max] toutes les `step` lignes, en px de l'image préparée."""
    rows = []
    for y in range(0, a.shape[0], step):
        xs = np.where(a[y] > 0.5)[0]
        if len(xs):
            rows.append([y, int(xs[0]), int(xs[-1]) + 1])
    return rows


def framing_extent(shot, asset, scale, focus, rot=0.0):
    """Étendue à l'écran de l'objet opaque pour un cadrage donné : haut, bas, x max dans la zone des icônes."""
    bx0, by0, bx1, by1 = asset["box"]
    k = shot["fit"] * scale
    fx, fy = bx0 + focus[0] * (bx1 - bx0), by0 + focus[1] * (by1 - by0)
    ax, ay = shot["anchor"]
    c, s_ = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    top, bottom, right, left, xmax = math.inf, -math.inf, -math.inf, math.inf, -math.inf
    rows = asset.get("rows") or [[by0, bx0, bx1], [by1 - 1, bx0, bx1]]
    for y, x0, x1 in rows:
        for x in (x0, x1):
            px, py = (x - fx) * k, (y - fy) * k
            sx, sy = ax + px * c - py * s_, ay + px * s_ + py * c
            top, bottom = min(top, sy), max(bottom, sy)
            left, xmax = min(left, sx), max(xmax, sx)
            if RAIL_Y[0] <= sy <= RAIL_Y[1]:
                right = max(right, sx)
    return {"top": top, "bottom": bottom, "right": right, "left": left, "xmax": xmax}


def check_framing(shot, asset, warnings):
    """Garde l'objet opaque au-dessus de la bande de sous-titres à chaque image du plan (cadrage d'ouverture,
    chaque déplacement et ses étapes intermédiaires, inclinaisons comprises) : sinon l'échelle est réduite."""
    tilt = max([abs(t["deg"]) for t in shot["tilts"]] + [0])

    def fix(scale, focus, label):
        e = framing_extent(shot, asset, scale, focus, tilt)
        e = max(e, framing_extent(shot, asset, scale, focus, -tilt), key=lambda d: d["bottom"])
        if e["bottom"] > HERO_BOTTOM + 0.5:
            bx0, by0, bx1, by1 = asset["box"]
            fy = by0 + focus[1] * (by1 - by0)
            lowest = e["bottom"] - shot["anchor"][1]
            new = scale * (HERO_BOTTOM - shot["anchor"][1]) / lowest if lowest > 0 else scale
            warnings.append(f"{shot['id']} {label} : objet jusqu'à y={e['bottom']:.0f} (> {HERO_BOTTOM}), "
                            f"échelle {scale:.2f} ramenée à {new:.2f}")
            return new, framing_extent(shot, asset, new, focus, tilt)
        return scale, e

    shot["scale"], e = fix(shot["scale"], shot["focus"], "ouverture")
    report = [e]
    prev_scale, prev_focus = shot["scale"], shot["focus"]
    for m in shot["moves"]:
        m["scale"], e = fix(m["scale"], m["focus"], f"déplacement image {m['frame']}")
        report.append(e)
        for t in (0.25, 0.5, 0.75):  # le zoom est interpolé en log, le point de visée linéairement
            sc = math.exp((1 - t) * math.log(prev_scale) + t * math.log(m["scale"]))
            fo = [prev_focus[0] + t * (m["focus"][0] - prev_focus[0]), prev_focus[1] + t * (m["focus"][1] - prev_focus[1])]
            mid = framing_extent(shot, asset, sc, fo, tilt)
            if mid["bottom"] > HERO_BOTTOM + 0.5:
                warnings.append(f"{shot['id']} : pendant le déplacement image {m['frame']}, objet jusqu'à "
                                f"y={mid['bottom']:.0f} (> {HERO_BOTTOM})")
            report.append(mid)
        prev_scale, prev_focus = m["scale"], m["focus"]
    top = min(r["top"] for r in report)
    right = max(r["right"] for r in report)
    if top < HERO_TOP - 0.5:
        warnings.append(f"{shot['id']} : objet jusqu'à y={top:.0f} en haut (fondu du haut à {HERO_TOP})")
    if right > RAIL_X + 0.5:
        warnings.append(f"{shot['id']} : objet jusqu'à x={right:.0f} dans la colonne d'icônes (x > {RAIL_X}, "
                        f"y {RAIL_Y[0]}-{RAIL_Y[1]})")
    shot["extent"] = {"top": round(top), "bottom": round(max(r["bottom"] for r in report)),
                      "right": round(right) if right > -math.inf else None,
                      # Boîte de l'objet opaque sur tout le plan (QA : rien de rouge ne doit la traverser au passage).
                      "box": [round(min(r["left"] for r in report)), round(top),
                              round(max(r["xmax"] for r in report)), round(max(r["bottom"] for r in report))]}


def build_plan(shotlist, clock, assets_meta, total_frames, fps):
    """Plans (héros), éléments graphiques, chapitres d'étapes et repères, tout en numéros d'image.

    La liste « shots » mélange des plans (« asset ») et des chapitres (« chapter » : rang de l'étape) : un
    chapitre termine le héros précédent et occupe la scène jusqu'au plan suivant (rangée de cercles au centre).
    """
    st, mo = STYLE["stage"], STYLE["motion"]
    entries, shots, overlays, beats, warnings, pending = [], [], [], [], [], []
    cursor = 0
    for si, s in enumerate(shotlist["shots"]):
        i0 = clock.index(s["at"], cursor if si == 0 else cursor + 1)
        cursor = i0
        f0 = clock.frame(i0)
        if "chapter" in s:
            ch = {"id": s["id"], "index": s["chapter"], "from": f0, "i0": i0}
            ch["go"] = clock.frame(clock.index(s["go"], i0)) if "go" in s else f0
            entries.append(("chapter", ch))
            beats.append({"frame": f0, "word": clock.words[i0]["w"], "what": f"{s['id']} chapitre {s['chapter'] + 1}"})
            if ch["go"] != f0:
                beats.append({"frame": ch["go"], "word": "", "what": f"{s['id']} protagoniste"})
            continue
        if s["asset"] not in assets_meta:
            raise SystemExit(f"{s['id']} : illustration {s['asset']} non préparée")
        a = assets_meta[s["asset"]]
        bw, bh = a["box"][2] - a["box"][0], a["box"][3] - a["box"][1]
        fit = min(st["box"][0] / bw, st["box"][1] / bh)
        anchor = s.get("anchor", [st["cx"], st["cy"]])

        def focus_of(spec, scale):
            # « center » : où poser le centre de la boîte de contenu à l'écran (px) ; sinon « focus » (fractions).
            if "center" in spec:
                cx, cy = spec["center"]
                return [round(0.5 + (anchor[0] - cx) / (fit * scale * bw), 4),
                        round(0.5 + (anchor[1] - cy) / (fit * scale * bh), 4)]
            return spec.get("focus", [0.5, 0.5])

        shot = {"id": s["id"], "asset": s["asset"], "from": f0, "fit": fit, "i0": i0,
                "anchor": anchor, "enter": s.get("enter", "grow"),
                "enter_offset": s.get("enter_offset", [0, 0]), "exit_offset": s.get("exit_offset", [0, 0]),
                "scale": s["scale"], "focus": focus_of(s, s["scale"]), "moves": [], "tilts": [], "tones": [],
                "shakes": [], "tone": s.get("tone")}
        if shot["enter"] not in ("grow", "cut"):
            raise SystemExit(f"{s['id']} : entrée « {shot['enter']} » inconnue (grow, cut)")
        beats.append({"frame": f0, "word": clock.words[i0]["w"], "what": f"{s['id']} {s['asset']}"})
        for ev in s.get("events", []):
            kind = ev.get("do")
            if kind not in HERO_EVENTS | OVERLAY_TYPES:
                raise SystemExit(f"{s['id']} : événement « {kind} » inconnu "
                                 f"(connus : {', '.join(sorted(HERO_EVENTS | OVERLAY_TYPES))})")
            ei = clock.index(ev["at"], i0)
            f = clock.frame(ei) + ev.get("delay", 0)
            beat = {"frame": f, "word": clock.words[ei]["w"], "what": f"{s['id']} {kind}"}
            if ev.get("delay"):
                beat["chained"] = True  # décalage voulu dans un geste enchaîné (ex. carte de fin)
            beats.append(beat)
            pending.append((shot, ev, f))
            if kind == "move":
                shot["moves"].append({"frame": f, "dur": ev.get("dur", mo["move"]), "scale": ev["scale"],
                                      "focus": focus_of(ev, ev["scale"])})
                continue
            if kind == "tilt":
                shot["tilts"].append({"frame": f, "dur": ev.get("dur", mo["tilt"]), "deg": ev["deg"]})
                continue
            if kind == "shake":
                shot["shakes"].append({"frame": f, "dur": ev.get("dur", mo["tilt"]), "deg": ev.get("deg", 6)})
                continue
            if kind == "tone":
                shot["tones"].append({"frame": f, "dur": ev.get("dur", mo["tone"]),
                                      "brightness": ev.get("brightness", 1), "saturate": ev.get("saturate", 1)})
                continue
            ov = {k: v for k, v in ev.items() if k not in ("at", "do", "delay")}
            ov.update({"id": f"{s['id']}-{len(overlays)}", "type": kind, "shot": s["id"], "from": f})
            chained_keys = set()
            for key in FRAME_KEYS:
                if isinstance(ov.get(key), (str, int)):
                    ov[key] = clock.frame(clock.index(ov[key], ei))
                    # « fill_delay » etc. : suite d'un même geste, quelques images après le début du mot.
                    lag = ov.pop(f"{key[:-3]}_delay", 0) if key.endswith("_at") else 0
                    if lag:
                        ov[key] += lag
                        chained_keys.add(key)
            if isinstance(ov.get("fill_at"), list):
                fills, j = [], ei
                for word in ov["fill_at"]:
                    j = clock.index(word, j)
                    fills.append(clock.frame(j))
                    beats.append({"frame": fills[-1], "word": clock.words[j]["w"], "what": f"{s['id']} {kind} fill"})
                ov["fill_at"] = fills
            for key in ("fill_at", "flip_at", "tilt_at", "tick_at", "press_at", "go_at"):
                if isinstance(ov.get(key), int):
                    beats.append({"frame": ov[key], "word": "", "what": f"{s['id']} {kind} {key}",
                                  **({"chained": True} if key in chained_keys else {})})
            overlays.append(ov)
        shots.append(shot)
        entries.append(("shot", shot))

    if entries and entries[0][1]["from"] != 0:
        raise SystemExit(f"{entries[0][1]['id']} : le premier plan commence à l'image {entries[0][1]['from']} : il doit "
                         f"commencer à l'image 0 (sinon la vidéo s'ouvre sur une scène vide)")
    # Fin de chaque plan / chapitre = début de l'entrée suivante.
    for k, (kind, e) in enumerate(entries):
        e["to"] = entries[k + 1][1]["from"] if k + 1 < len(entries) else total_frames
        if e["to"] <= e["from"]:
            raise SystemExit(f"{e['id']} : plan vide (image {e['from']} à {e['to']}), vérifier les mots « at »")
    for shot, ev, f in pending:
        if not shot["from"] <= f < shot["to"]:
            raise SystemExit(f"{shot['id']} : « {ev['do']} » sur « {ev['at']} » tombe à l'image {f}, hors du plan "
                             f"({shot['from']}-{shot['to']})")
        until = ev.get("until")
        if until is not None:
            ov = next(o for o in overlays if o["shot"] == shot["id"] and o["from"] == f and o["type"] == ev["do"])
            if ov["until"] <= f:
                raise SystemExit(f"{shot['id']} : « {ev['do']} » finit (until) avant de commencer")

    for shot in shots:
        a = assets_meta[shot["asset"]]
        # Aucun agrandissement au-delà de la résolution source (1 px source = 1 px écran au maximum).
        peak = max([shot["scale"]] + [m["scale"] for m in shot["moves"]])
        if shot["fit"] * peak > 1.0001:
            cap = 1.0 / shot["fit"]
            warnings.append(f"{shot['id']} : échelle {peak} > résolution source, ramenée à {cap:.2f}")
            shot["scale"] = min(shot["scale"], cap)
            for m in shot["moves"]:
                m["scale"] = min(m["scale"], cap)
        check_framing(shot, a, warnings)
    chapters = [e for kind, e in entries if kind == "chapter"]
    return shots, overlays, beats, warnings, chapters


def build_steps(spec, chapters, clock):
    """Indicateur d'étapes : chapitres au centre de la scène, puis rangée réduite en haut jusqu'à « hide »."""
    if not spec or not chapters:
        return None
    hide = clock.index(spec["hide"], chapters[-1]["i0"] + 1)
    return {"count": spec["count"], "y": spec.get("y", 250), "cy": spec.get("cy", STYLE["stage"]["cy"]),
            "chapters": [{k: c[k] for k in ("from", "to", "go", "index")} for c in chapters],
            "hide": clock.frame(hide)}


def build_end_card(spec, clock, start_index, beats):
    if not spec:
        return None
    out = {}
    for part, cfg in spec.items():
        c = dict(cfg)
        i = clock.index(c.pop("at"), start_index)
        c["from"] = clock.frame(i) + c.pop("delay", 0)
        beats.append({"frame": c["from"], "word": "" if cfg.get("delay") else clock.words[i]["w"],
                      "what": f"fin {part}", **({"chained": True} if cfg.get("delay") else {})})
        for key in ("press_at", "flip_at"):
            if key in c:
                j = clock.index(c[key], i)
                c[key] = clock.frame(j) + c.pop(key.replace("_at", "_delay"), 0)
                beats.append({"frame": c[key], "word": clock.words[j]["w"], "what": f"fin {part} {key}",
                              **({"chained": True} if cfg.get(key.replace("_at", "_delay")) else {})})
        out[part] = c
    return out


# ---------- props ----------

def check_series_assets(video_id, shotlist):
    """Une vidéo n'utilise que les illustrations de son propre carrousel (WTH-<source>-xx) et les génériques."""
    source = script(video_id).get("source", "")
    bad = [f"{s['id']} : {s['asset']}" for s in shotlist["shots"] if "asset" in s
           and (m := CAROUSEL_ASSET.match(s["asset"])) and m.group(1) != source]
    if bad:
        raise SystemExit(f"{video_id} (carrousel {source}) utilise des illustrations d'un autre carrousel de la série : "
                         f"{', '.join(bad)}. Règle : son propre carrousel + illustrations génériques seulement.")


def shown_overlay_texts(overlays, end_card):
    """Textes tels qu'ils s'affichent (capitales comprises) : étiquettes, puces, carte de fin."""
    out = []
    for o in overlays:
        upper = o["type"] == "chips" or (o["type"] == "pill" and o.get("case") != "keep")
        for t in [o.get("text"), o.get("flip_text")] + list(o.get("texts", [])):
            if t:
                out.append((o["id"], t.upper() if upper else t))
    for part, cfg in (end_card or {}).items():
        for key in ("text", "flip_text"):
            if cfg.get(key):
                out.append((f"fin {part}", cfg[key]))
    return out


TYPO_RULES = [
    (re.compile(r"\d(?:[ \u00a0])?h\b"), "heure : « 9\u202fh » (espace fine insécable U+202F entre le nombre et h)"),
    (re.compile(r"\d[\s\u00a0\u202f]*(?:MIN|H|S|KM|KG)\b"), "symbole d'unité en capitales (« 10 MIN ») : « case »: « keep » et « 10 min »"),
    (re.compile(r"\d(?:min|kg|km)\b"), "unité collée au nombre : « 10\u00a0min »"),
    (re.compile(r"\d (?:min|h|kg|km|%|€)"), "espace ordinaire entre le nombre et l'unité : espace insécable"),
]


def lint_overlay_texts(overlays, end_card):
    """Typographie française des étiquettes (vaut pour les 15 vidéos) : erreur avant le rendu."""
    problems = [f"{oid} « {t} » : {msg}" for oid, t in shown_overlay_texts(overlays, end_card)
                for rx, msg in TYPO_RULES if rx.search(t)]
    if problems:
        raise SystemExit("Typographie des étiquettes :\n  " + "\n  ".join(problems))


def sha1_file(path):
    return hashlib.sha1(Path(path).read_bytes()).hexdigest()


def check_inputs(video_id):
    """Entrées obligatoires, vérifiées avant de créer quoi que ce soit dans build/."""
    shot_file = SHOTLISTS / f"{video_id}.json"
    if not shot_file.exists():
        raise SystemExit(f"Plan de tournage absent : {shot_file} (voir scripts/shotlists/V01.json)")
    from .common import BUILD
    for name, hint in (("words.json", "make video ID=… ou make words ID=…"), ("tts.json", "make tts ID=…")):
        if not (BUILD / video_id / name).exists():
            raise SystemExit(f"{video_id} : build/{video_id}/{name} absent ({hint}) : la voix verrouillée et ses "
                             f"temps de mots sont nécessaires au rendu motion")


def build_props(video_id, cfg=None):
    cfg = cfg or load_config()
    v = cfg["video"]
    fps = v["fps"]
    check_inputs(video_id)
    out_dir = build_dir(video_id)
    wdata = read_json(out_dir / "words.json")
    words = wdata["words"]
    shotlist = read_json(SHOTLISTS / f"{video_id}.json")
    shot_file = SHOTLISTS / f"{video_id}.json"
    audio = ensure_audio(video_id, cfg)
    audio_dur = float(ffprobe(audio)["format"]["duration"])
    end_t = words[-1]["end"] + v["tail_seconds"]
    total = math.ceil(end_t * fps - 1e-6)
    if total / fps > audio_dur + 1e-3:
        total = math.floor(audio_dur * fps)

    check_series_assets(video_id, shotlist)
    names = [s["asset"] for s in shotlist["shots"] if "asset" in s]
    asset_notes = []
    assets_meta = prepare_assets(video_id, names, asset_notes)
    bg = make_background(video_id, v["width"], v["height"])
    clock = WordClock(words, fps)
    shots, overlays, beats, warnings, chapters = build_plan(shotlist, clock, assets_meta, total, fps)
    warnings = asset_notes + warnings
    steps = build_steps(shotlist.get("steps"), chapters, clock)
    if steps:
        # Le héros qui cède la scène à un chapitre rétrécit vers la place du protagoniste rouge de ce chapitre.
        big, he = STYLE["steps"]["big"], STYLE["steps"]["hero_exit"]
        for ch in steps["chapters"]:
            prev = next((sh for sh in shots if sh["to"] == ch["from"]), None)
            if prev:
                slot_x = v["width"] / 2 + (ch["index"] - (steps["count"] - 1) / 2) * big["gap"]
                prev["exit"] = {**he, "target": [round(slot_x, 1), steps["cy"]]}
        beats.append({"frame": steps["hide"], "word": clock.words[clock.index(shotlist["steps"]["hide"],
                                                                                chapters[-1]["i0"] + 1)]["w"],
                      "what": "étapes : sortie"})
    end_card = build_end_card(shotlist.get("end_card"), clock, shots[-1]["i0"], beats)
    lint_overlay_texts(overlays, end_card)
    measure = CaptionMeasure()
    captions = caption_track(words, fps, total, measure, (shotlist.get("captions") or {}).get("groups"))
    onsets = {clock.frame(i) for i in range(len(words))}
    off = sorted({b["frame"] for b in beats if b["frame"] not in onsets and not b.get("chained")})
    chained = sorted({b["frame"] for b in beats if b.get("chained")})
    for shot in shots:
        shot.pop("i0", None)
    # Images clés H.264 forcées au début de chaque plan / chapitre : le rafraîchissement d'image clé
    # tombe dans une transition, jamais dans un plan tenu immobile.
    keyframes = sorted({0} | {s["from"] for s in shots} | {c["from"] for c in chapters}
                       | {c["to"] for c in chapters if c["to"] < total})

    props = {
        "id": video_id,
        "fps": fps, "width": v["width"], "height": v["height"], "durationInFrames": total,
        "style": STYLE,
        "background": bg,
        "assets": {k: {"src": m["src"], "w": m["w"], "h": m["h"], "box": m["box"]} for k, m in assets_meta.items()},
        "shots": shots,
        "overlays": overlays,
        "steps": steps,
        "endCard": end_card,
        "captions": captions,
        "beats": sorted(beats, key=lambda b: b["frame"]),
        "meta": {"words": len(words), "audio_seconds": round(audio_dur, 3), "last_word_end": words[-1]["end"],
                 "shotlist": str(shot_file.relative_to(ROOT)), "warnings": warnings,
                 "beats_off_onset": off, "beats_chained": chained, "keyframes": keyframes},
    }
    path = out_dir / "motion.json"
    # Réécrit seulement si le contenu change : une image fixe ou un « --props » après le rendu ne le périme pas.
    text = json.dumps(props, ensure_ascii=False, indent=2) + "\n"
    if not path.exists() or path.read_text(encoding="utf-8") != text:
        path.write_text(text, encoding="utf-8")
    widest = max(c["width"] for c in captions)
    print(f"{video_id} : {len(shots)} plans, {len(overlays)} éléments, {len(beats)} événements, "
          f"{len(captions)} groupes de sous-titres (le plus large {widest:.0f}/{STYLE['caption']['max_width']} px), "
          f"{total} images ({total / fps:.2f} s) -> {path}")
    for w in warnings:
        print("  attention :", w)
    if off:
        print("  attention : événements hors début de mot aux images", off)
    return path, props


def ensure_audio(video_id, cfg):
    """build/Vxx/audio.wav normalisé (-14 LUFS) : réutilisé s'il est plus récent que la voix en cache."""
    from .render import normalize_audio
    out_dir = build_dir(video_id)
    tts = read_json(out_dir / "tts.json")
    src, dst = Path(tts["audio"]), out_dir / "audio.wav"
    if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
        print(f"{video_id} : normalisation de la voix -> {dst}")
        normalize_audio(src, dst, cfg)
    return dst


# ---------- rendu ----------

def browser_executable():
    """Navigateur de rendu : REMOTION_BROWSER_EXECUTABLE, sinon motion/browser.json (seul endroit où est écrit le
    chemin par défaut ; remotion.config.ts et scripts/stills.mjs lisent le même fichier)."""
    path = os.environ.get("REMOTION_BROWSER_EXECUTABLE") or read_json(BROWSER_FILE)["executable"]
    if not (Path(path).is_file() and os.access(path, os.X_OK)):
        raise SystemExit(f"Navigateur de rendu introuvable : {path}. Indique un Chrome / headless shell avec "
                         f"REMOTION_BROWSER_EXECUTABLE=/chemin/vers/headless_shell (ou corrige {BROWSER_FILE}).")
    return path


def remotion_env(**extra):
    return dict(os.environ, REMOTION_BROWSER_EXECUTABLE=browser_executable(), **extra)


def remotion_render(video_id, props_path, silent, keyframes=()):
    if not (MOTION / "node_modules").is_dir():
        raise SystemExit("motion/node_modules absent : lance « npm ci » dans motion/ (registre npm).")
    cmd = ["npx", "remotion", "render", "Explainer", str(silent), f"--props={props_path}", "--muted",
           "--log=error"]
    fps = read_json(props_path)["fps"]
    # Images clés forcées (motion/remotion.config.ts) : temps légèrement avant l'image visée.
    env = remotion_env(WTH_KEYFRAMES=",".join(f"{max(0.0, f / fps - 0.001):.4f}" for f in keyframes))
    t0 = time.time()
    proc = subprocess.run(cmd, cwd=MOTION, text=True, capture_output=True, env=env)
    if proc.returncode != 0:
        print(proc.stdout[-4000:], proc.stderr[-4000:])
        raise SystemExit(f"Rendu Remotion en échec ({proc.returncode})")
    print(f"{video_id} : rendu Remotion {time.time() - t0:.0f} s -> {silent}")


RENDER_SIDECAR = "motion_render.json"


def render_stamp(video_id):
    """Empreintes de ce qui a été rendu : props (motion.json) et plan (scripts/shotlists/Vxx.json)."""
    out_dir = build_dir(video_id)
    return {"mode": "motion", "props_sha1": sha1_file(out_dir / "motion.json"),
            "shotlist_sha1": sha1_file(SHOTLISTS / f"{video_id}.json")}


def mux(video_id, silent, audio, frames, cfg):
    v = cfg["video"]
    OUTPUT.mkdir(parents=True, exist_ok=True)
    mp4 = OUTPUT / f"WTH-{video_id}.mp4"
    duration = frames / v["fps"]
    stamp = render_stamp(video_id)
    # Le mode et les empreintes vont dans le MP4 (balises wth_*) ET dans build/Vxx/motion_render.json :
    # la QA compare des empreintes, pas des dates de fichiers.
    run(["ffmpeg", "-hide_banner", "-y", "-i", str(silent), "-i", str(audio),
         "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
         "-c:a", "aac", "-b:a", v["audio_bitrate"], "-ar", str(v["audio_rate"]), "-ac", "2",
         "-metadata", f"wth_mode={stamp['mode']}", "-metadata", f"wth_props={stamp['props_sha1']}",
         "-metadata", f"wth_shotlist={stamp['shotlist_sha1']}",
         "-t", f"{duration:.6f}", "-movflags", "+faststart+use_metadata_tags", str(mp4)])
    probe = ffprobe(mp4)
    write_json(build_dir(video_id) / RENDER_SIDECAR,
               {**stamp, "file": str(mp4.relative_to(ROOT)), "mp4_sha1": sha1_file(mp4), "frames": frames,
                "rendered_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")})
    starts = {s["codec_type"]: float(s.get("start_time", 0)) for s in probe["streams"]}
    print(f"{video_id} : {mp4} ({float(probe['format']['duration']):.3f} s, départs {starts})")
    return mp4


def review(video_id, step=2.0, extra=None, cols=8, thumb_w=270):
    """Images décodées du MP4 (toutes les `step` s + milieux de transitions) -> build/Vxx/review/contact.png."""
    from PIL import ImageDraw
    out_dir = build_dir(video_id) / "review"
    frames_dir = out_dir / "frames"
    if frames_dir.exists():
        for f in frames_dir.glob("*.png"):
            f.unlink()
    frames_dir.mkdir(parents=True, exist_ok=True)
    props = read_json(build_dir(video_id) / "motion.json")
    fps, total = props["fps"], props["durationInFrames"]
    picks = {min(total - 1, round(k * step * fps)): "" for k in range(int(total / fps / step) + 1)}
    for shot in props["shots"][1:]:
        picks[shot["from"] + 2] = f"{shot['id']} entrée"
    for k, ch in enumerate((props.get("steps") or {}).get("chapters", [])):
        picks[ch["go"] + 10] = f"chapitre {ch['index'] + 1}"
    for f in extra or []:
        picks[int(f)] = "extra"
    picks[total - 1] = "fin"
    mp4 = OUTPUT / f"WTH-{video_id}.mp4"
    sel = "+".join(f"eq(n\\,{f})" for f in sorted(picks))
    run(["ffmpeg", "-hide_banner", "-y", "-i", str(mp4), "-vf", f"select={sel}", "-vsync", "0",
         str(frames_dir / "f_%03d.png")])
    files = sorted(frames_dir.glob("f_*.png"))
    labels = sorted(picks)
    named = []
    for f, n in zip(files, labels):
        dst = frames_dir / f"t{n / fps:06.2f}_f{n:04d}.png"
        f.rename(dst)
        named.append((n, dst))
    th = round(thumb_w * props["height"] / props["width"])
    rows = math.ceil(len(named) / cols)
    sheet = Image.new("RGB", (cols * (thumb_w + 8) + 8, rows * (th + 34) + 8), (30, 30, 32))
    d = ImageDraw.Draw(sheet)
    font = ImageFont.truetype(str(CAPTION_FONT), 17)
    for k, (n, f) in enumerate(named):
        x, y = 8 + (k % cols) * (thumb_w + 8), 8 + (k // cols) * (th + 34)
        sheet.paste(Image.open(f).convert("RGB").resize((thumb_w, th), Image.LANCZOS), (x, y + 26))
        d.text((x, y + 2), f"{n / fps:5.2f} s  #{n}  {picks[n]}", font=font, fill=(235, 235, 235))
    path = out_dir / "contact.png"
    sheet.save(path)
    print(f"{video_id} : {len(named)} images -> {path}")
    return path


def motion(video_id, props_only=False):
    cfg = load_config()
    props_path, props = build_props(video_id, cfg)
    if props_only:
        return props_path
    out_dir = build_dir(video_id)
    silent = out_dir / "motion_silent.mp4"
    remotion_render(video_id, props_path, silent, props["meta"].get("keyframes", ()))
    return mux(video_id, silent, out_dir / "audio.wav", props["durationInFrames"], cfg)


def stills(video_id, frames):
    """Images fixes PNG d'images choisies, sans rendu complet -> build/Vxx/review/stills/ (motion/scripts/stills.mjs)."""
    props_path, _ = build_props(video_id)
    out = build_dir(video_id) / "review" / "stills"
    proc = subprocess.run(["node", "scripts/stills.mjs", str(props_path), str(out), *map(str, frames)], cwd=MOTION,
                          text=True, capture_output=True, env=remotion_env())
    if proc.returncode != 0:
        print(proc.stdout[-3000:], proc.stderr[-3000:])
        raise SystemExit("Images fixes en échec")
    print(f"{video_id} : {len(frames)} images fixes -> {out}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("id")
    p.add_argument("--props", action="store_true", help="assets et props seulement, sans rendu")
    p.add_argument("--stills", nargs="+", type=int, metavar="IMAGE",
                   help="images fixes PNG de ces numéros d'image (sans rendu complet)")
    p.add_argument("--review", nargs="*", type=int, metavar="IMAGE",
                   help="planche contact du MP4 rendu (images en plus en option), sans rendu")
    a = p.parse_args()
    if a.stills:
        stills(a.id, a.stills)
    elif a.review is not None:
        review(a.id, extra=a.review)
    else:
        motion(a.id, props_only=a.props)


if __name__ == "__main__":
    main()
