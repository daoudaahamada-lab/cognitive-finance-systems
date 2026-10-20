"""Composition « Story » (graphe de scène) : props, rendu Remotion, extrait audio, mixage, planches de contrôle.

    python3 -m pipeline.story V01 --from 26.378 --to 41.309                extrait avec sous-titres
    python3 -m pipeline.story V01 --from 26.378 --to 41.309 --no-captions  seulement la version sans sous-titres
    python3 -m pipeline.story V01 --from 26.378 --to 41.309 --props        props seulement (pas de rendu)
    python3 -m pipeline.story V01 --from 26.378 --to 41.309 --stills 0 40  images fixes (numéros d'image de l'extrait)
    python3 -m pipeline.story V01 --full                                    le film entier (0 -> fin de audio.wav)

Numéros d'image : image de l'extrait # = round(t × 30) − meta.window_frames[0] (la fenêtre s'ouvre juste avant
l'attaque audible du premier mot, pas forcément à round(from × 30)) ; le tableau des temps forts est imprimé dans les
deux numérotations.

Entrées : scripts/storyboards/Vxx.json (scènes, temps forts calés sur des mots), scripts/story/Vxx.py (mise en scène :
distribution, états et pistes image par image, écrite avec l'API Story ci-dessous), build/Vxx/words.json,
build/Vxx/audio.wav. Sorties : build/Vxx/story/ (props, vidéo muette, planches), output/extraits/WTH-Vxx_extrait_Sa-Sb.mp4
et build/Vxx/story/extrait_sans_sous_titres.mp4.

Le temps est celui du FILM (image n = n / 30 s) : chaque temps fort du storyboard est résolu sur l'image de début de son
mot dans words.json (round(start × 30)). Un extrait est une fenêtre [F0, F1) sur ce temps : sa première image montre
l'état du film à F0, sans animation d'entrée. L'évaluation des pistes (assouplissements, LEAD, matrices) est la copie
exacte de motion/src/story/timeline.ts : le constructeur calcule les positions monde (re-parentage, ancres, trajets le
long d'un fil) avec les nombres mêmes du rendu.
"""
import argparse
import bisect
import importlib.util
import json
import math
import subprocess
import time
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .common import OUTPUT, ROOT, build_dir, ffprobe, load_config, read_json, run, write_json
from .motion import GENERATED, ILLUSTRATIONS, MOTION, CaptionMeasure, _norm, caption_groups, clean_word, remotion_env

STORYBOARDS = ROOT / "scripts" / "storyboards"
SPECS = ROOT / "scripts" / "story"
FONTS = MOTION / "public" / "fonts"
PNG_VERSION = 1  # à incrémenter si la recette des PNG (alpha strict) change

# Jetons du storyboard (section « style ») : fond ivoire quadrillé, encre, un seul accent cyan, rouge d'alerte.
STYLE = {
    "bg": "#F6F0E4",
    "grid": {"pitch": 36, "line": 2, "color": "#ECE4D4"},
    "ink": "#1E1416",
    "cyan": "#19B3C7",
    "deep": "#0A7487",
    "light": "#D3F0F6",
    "paper": "#FFFDF8",
    "grey": "#DDD5C6",
    "red": "#C8102E",
    "slot": "#F4EEE3",      # fond des rangées de la fiche
    "rule": "#E6DECF",      # filet sous l'en-tête
    "ai_tick": "#8E8887",   # encre à ~50 % sur papier : coches de l'IA (lisibles à taille téléphone)
    "font_family": "WTH Inter",
    # max_words_hard borne la découpe AUTOMATIQUE ; une découpe imposée par la mise en scène (CAPTION_GROUPS du
    # fichier Vxx.py) peut aller jusqu'à 4 mots (ex. « et à une date »), vérifié par caption_track.
    "caption": {"size": 64, "weight": 700, "baseline": 1350, "color": "#1E1416", "active": "#0A7487",
                "alert": "#C8102E", "max_width": 760, "max_words": 3, "max_words_hard": 3, "gap_break": 0.15},
}
OVERRIDE_MAX_WORDS = 4
ALERT_WORDS = set()   # mots d'alerte (rouge) : propres à chaque film, lus dans scripts/story/Vxx.py (ALERT_WORDS)

# Durées de la référence en images à 30 i/s (mesures image par image) :
POP = 9        # apparition 300 ms, ease-out cubique, sans rebond
SCALE = 10     # changement d'échelle 330 ms, ease-out
MORPH = 11     # passage d'une composition à l'autre 350 ms
MOVE = 16      # déplacement 550 ms, ease-in-out
DROP = 11      # chute 370 ms
TILT = 14      # inclinaison 450 ms
FADE = 6       # fondu de texte 200 ms
DRAW = 9       # trait ou fil dessiné 250-450 ms
STRETCH = 6    # étirement 200 ms

LEAD = 1  # l'image f d'un segment montre déjà le pas 1/d (comme timeline.ts)


# ---------- évaluation des pistes (copie de timeline.ts) ----------

def _ease(name, t):
    if name == "linear":
        return t
    if name == "out":
        return 1 - (1 - t) ** 3
    if name == "in":
        return t ** 3
    if name == "inOut":
        return 4 * t ** 3 if t < 0.5 else 1 - ((1 - t) * 2) ** 3 / 2
    if name == "outQuad":
        return 1 - (1 - t) ** 2
    if name == "inOutSine":
        return (1 - math.cos(math.pi * t)) / 2
    raise ValueError(f"assouplissement inconnu : {name}")


EASES = {"linear", "out", "in", "inOut", "outQuad", "inOutSine"}


def _progress(key, n):
    d = key.get("d", 0)
    if d <= 0:
        return 1.0 if n >= key["f"] else 0.0
    return _ease(key.get("e", "out"), min(1.0, max(0.0, (n - key["f"] + LEAD) / d)))


def _mix(a, b, p, arc=None):
    if isinstance(a, (int, float)) and not isinstance(a, bool) and isinstance(b, (int, float)) and not isinstance(b, bool):
        return a + (b - a) * p
    if isinstance(a, list) and isinstance(b, list):
        out = [x + (y - x) * p for x, y in zip(a, b)]
        if arc and len(out) == 2:
            out[1] -= arc * 4 * p * (1 - p)
        return out
    if isinstance(a, str) and isinstance(b, str) and a.startswith("#") and b.startswith("#") and len(a) == len(b) == 7:
        A = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
        B = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
        return "#" + "".join(f"{round(x + (y - x) * p):02x}" for x, y in zip(A, B))
    return b if p > 0 else a


def eval_track(track, n, fallback=None):
    if not track:
        return fallback
    seg, start = None, track[0]["v"]
    for key in track[1:]:
        if n < key["f"]:
            break
        start = _mix(start, seg["v"], _progress(seg, key["f"] - 1), seg.get("arc")) if seg else track[0]["v"]
        seg = key
    return _mix(start, seg["v"], _progress(seg, n), seg.get("arc")) if seg else track[0]["v"]


# ---------- matrices 2D [a, b, c, d, e, f] (comme timeline.ts) ----------

def mat_mul(m, n):
    return [m[0] * n[0] + m[2] * n[1], m[1] * n[0] + m[3] * n[1], m[0] * n[2] + m[2] * n[3],
            m[1] * n[2] + m[3] * n[3], m[0] * n[4] + m[2] * n[5] + m[4], m[1] * n[4] + m[3] * n[5] + m[5]]


def mat_apply(m, p):
    return [m[0] * p[0] + m[2] * p[1] + m[4], m[1] * p[0] + m[3] * p[1] + m[5]]


def mat_inv(m):
    det = m[0] * m[3] - m[1] * m[2]
    if abs(det) < 1e-12:
        raise ValueError("matrice non inversible (entité réduite à un point)")
    a, b, c, d = m[3] / det, -m[1] / det, -m[2] / det, m[0] / det
    return [a, b, c, d, -(a * m[4] + c * m[5]), -(b * m[4] + d * m[5])]


def local_matrix(pos, rot, sx, sy):
    r = math.radians(rot)
    c, s = math.cos(r), math.sin(r)
    return [c * sx, s * sx, -s * sy, c * sy, pos[0], pos[1]]


def wire_cubic(a, b, sag, tension=0.45):
    dx = (b[0] - a[0]) * tension
    return [list(a), [a[0] + dx, a[1] + sag], [b[0] - dx, b[1] + sag], list(b)]


def cubic_at(c, t):
    u = 1 - t
    w = [u * u * u, 3 * u * u * t, 3 * u * t * t, t * t * t]
    return [sum(w[i] * c[i][0] for i in range(4)), sum(w[i] * c[i][1] for i in range(4))]


def point_at_length(c, frac, n=32):
    pts = [cubic_at(c, i / n) for i in range(n + 1)]
    acc = [0.0]
    for i in range(1, n + 1):
        acc.append(acc[-1] + math.dist(pts[i], pts[i - 1]))
    target = frac * acc[-1]
    for i in range(1, n + 1):
        if acc[i] >= target:
            t = (target - acc[i - 1]) / max(1e-6, acc[i] - acc[i - 1])
            return [pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * t, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * t]
    return pts[-1]


def line_crack_point(p, pt, crack=1.0):
    """Point local de la partie droite d'une rangée (`line`) cassée, comme entities.tsx Line : elle pivote de
    tilt × crack degrés autour de sa charnière (bord gauche de la fente, crackX + gap / 2, haut de la bande de texte)
    puis descend de drop × crack px."""
    cx, cy = p["crackX"] + p.get("gap", 0) / 2, -p["h"] / 2
    t = math.radians(p["tilt"] * crack)
    dx, dy = pt[0] - cx, pt[1] - cy
    return [cx + dx * math.cos(t) - dy * math.sin(t), cy + dx * math.sin(t) + dy * math.cos(t) + p["drop"] * crack]


DEFAULTS = {"pos": [0, 0], "scale": 1, "rot": 0, "opacity": 1, "sx": 1, "sy": 1}


# ---------- texte ----------

_FONTS = {}


def text_width(text, size, weight=600):
    key = (size, weight)
    if key not in _FONTS:
        name = {600: "Inter-SemiBold.otf", 700: "Inter-Bold.otf", 800: "Inter-ExtraBold.otf"}[weight]
        _FONTS[key] = ImageFont.truetype(str(FONTS / name), size)
    return _FONTS[key].getlength(text)


# ---------- PNG : alpha strict pour le fond ivoire ----------

def _neighbours(arr):
    """Les 8 voisins de chaque pixel (bords répliqués)."""
    p = np.pad(arr, [(1, 1), (1, 1)] + [(0, 0)] * (arr.ndim - 2), mode="edge")
    h, w = arr.shape[:2]
    return [p[1 + dy:1 + dy + h, 1 + dx:1 + dx + w] for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dy or dx]


def _largest_component(mask, scale=4):
    """Composante connexe principale (reconstruction géodésique sur un masque réduit), remise à l'échelle."""
    small = np.asarray(Image.fromarray(mask.astype(np.uint8) * 255).resize(
        (mask.shape[1] // scale, mask.shape[0] // scale), Image.BILINEAR)) > 64
    ys, xs = np.where(small)
    cy, cx = int(np.median(ys)), int(np.median(xs))
    if not small[cy, cx]:
        k = np.argmin((ys - cy) ** 2 + (xs - cx) ** 2)
        cy, cx = ys[k], xs[k]
    seed = np.zeros_like(small)
    seed[cy, cx] = True
    for _ in range(4000):
        grown = seed.copy()
        for nb in _neighbours(seed):
            grown |= nb
        grown &= small
        if (grown == seed).all():
            break
        seed = grown
    big = np.asarray(Image.fromarray(seed.astype(np.uint8) * 255).resize((mask.shape[1], mask.shape[0]), Image.NEAREST)) > 0
    # Marge de 3 px du masque réduit (le bord exact vient de l'alpha d'origine).
    for _ in range(3 * scale):
        g = big.copy()
        for nb in _neighbours(big):
            g |= nb
        big = g
    return big


def strict_png(name, out_path, keep_largest=False, lo=0.40, hi=0.88):
    """Illustration rendue pour fond noir -> PNG pour fond ivoire.

    Le halo cuit (RGB des pixels d'alpha ~0) et l'ombre de contact semi-transparente sont coupés par un alpha strict
    (smoothstep lo..hi) ; la couleur des pixels de bord est remplacée par celle des pixels opaques voisins
    (sinon frange sombre ou sarcelle sur l'ivoire). L'ombre douce est ajoutée au rendu (CSS drop-shadow).
    """
    src = ILLUSTRATIONS / f"{name}.png"
    im = Image.open(src).convert("RGBA")
    arr = np.asarray(im).astype(np.float32) / 255
    rgb, a = arr[..., :3].copy(), arr[..., 3]
    t = np.clip((a - lo) / (hi - lo), 0, 1)
    a_s = t * t * (3 - 2 * t)
    if keep_largest:
        a_s *= _largest_component(a_s > 0.5)
    known = a >= 0.97
    for _ in range(8):
        todo = (~known) & (a_s > 0)
        if not todo.any():
            break
        acc = np.zeros_like(rgb)
        cnt = np.zeros(a.shape, np.float32)
        for nb_k, nb_c in zip(_neighbours(known), _neighbours(rgb)):
            acc += nb_c * nb_k[..., None]
            cnt += nb_k
        fill = todo & (cnt > 0)
        rgb[fill] = acc[fill] / cnt[fill][:, None]
        known = known | fill
    ys, xs = np.where(a_s > 0.004)
    pad = 6
    x0, y0 = max(0, xs.min() - pad), max(0, ys.min() - pad)
    x1, y1 = min(a.shape[1], xs.max() + 1 + pad), min(a.shape[0], ys.max() + 1 + pad)
    out = np.dstack([rgb, a_s])[y0:y1, x0:x1]
    out8 = np.clip(np.round(out * 255), 0, 255).astype(np.uint8)
    out8[out8[..., 3] == 0, :3] = 0
    Image.fromarray(out8, "RGBA").save(out_path)
    return {"w": int(x1 - x0), "h": int(y1 - y0), "crop": [int(x0), int(y0), int(x1), int(y1)]}


# ---------- Story : distribution, pistes, temps ----------

class Story:
    """Graphe de scène d'un film : entités persistantes et pistes en images du film."""

    def __init__(self, video_id, words, storyboard, fps=30, width=1080, height=1920, snap=None):
        """`snap` (optionnel) : {"gap": s, "window": s, "attack": t -> t_attaque | None}. Un temps fort dont le mot
        suit un silence d'au moins `gap` s est calé sur l'attaque audible de la voix si elle tombe à moins de
        `window` s du début annoncé par words.json (la voix ne précède alors plus l'image)."""
        self.video_id, self.words, self.sb, self.fps = video_id, words, storyboard, fps
        self.snap = snap
        self.width, self.height = width, height
        self.ents = {}
        self.beats = []      # temps forts posés par la mise en scène (rapport, couverture du storyboard)
        self.assets = {}     # PNG préparés : nom -> {src, w, h}
        self.keys_norm = [_norm(w["w"]) for w in words]

    # --- temps ---
    def frame_of(self, i):
        return round(self.words[i]["start"] * self.fps)

    def word(self, text, near=None):
        """Image du mot `text` (le plus proche de `near` secondes s'il y en a plusieurs)."""
        q = _norm(text)
        hits = [i for i, k in enumerate(self.keys_norm) if k == q]
        if not hits:
            raise SystemExit(f"Mot « {text} » absent de words.json")
        i = min(hits, key=lambda j: abs(self.words[j]["start"] - near)) if near is not None else hits[0]
        return self.frame_of(i)

    def word_after(self, text, frame):
        """Image du premier mot `text` qui commence à l'image `frame` ou après (mot hors temps fort, repéré par
        rapport à un temps fort plutôt que par un temps absolu)."""
        q = _norm(text)
        hits = [i for i, k in enumerate(self.keys_norm) if k == q and self.frame_of(i) >= frame]
        if not hits:
            raise SystemExit(f"Mot « {text} » absent de words.json après l'image {frame}")
        return self.frame_of(hits[0])

    def beat(self, scene, mot, what=""):
        """Temps fort du storyboard (scène, mot) -> image de début du mot dans words.json (vérifiée)."""
        sc = next((s for s in self.sb["scenes"] if s["id"] == scene), None)
        if sc is None:
            raise SystemExit(f"Scène {scene} absente du storyboard")
        b = next((b for b in sc["beats"] if _norm(b["mot"]) == _norm(mot)), None)
        if b is None:
            raise SystemExit(f"{scene} : pas de temps fort sur « {mot} » dans le storyboard")
        q = _norm(mot)
        hits = [i for i, k in enumerate(self.keys_norm) if k == q]
        i = min(hits, key=lambda j: abs(self.words[j]["start"] - b["t"])) if hits else None
        if i is None or abs(self.words[i]["start"] - b["t"]) > 0.03:
            raise SystemExit(f"{scene} « {mot} » ({b['t']} s) : mot introuvable à ce temps dans words.json")
        f = self.frame_of(i)
        rec = {"scene": scene, "word": mot, "i": i, "t": self.words[i]["start"], "frame": f, "what": what}
        if self.snap and i > 0 and self.words[i]["start"] - self.words[i - 1]["end"] >= self.snap["gap"]:
            t_ac = self.snap["attack"](self.words[i]["start"])
            if t_ac is not None and abs(t_ac - self.words[i]["start"]) <= self.snap["window"]:
                f = round(t_ac * self.fps)
                rec.update(frame=f, word_frame=self.frame_of(i), attack_t=round(t_ac, 3))
        self.beats.append(rec)
        return f

    # --- distribution ---
    def add(self, id, type, z=0, parent=None, **p):
        if id in self.ents:
            raise SystemExit(f"Entité « {id} » déjà déclarée")
        if parent and parent not in self.ents:
            raise SystemExit(f"{id} : parent « {parent} » à déclarer avant")
        self.ents[id] = {"id": id, "type": type, "z": z, **({"parent": parent} if parent else {}), "p": p, "t": {}}
        return id

    def set(self, id, **tracks):
        """Valeurs initiales (état du film avant toute clé)."""
        for name, v in tracks.items():
            tr = self.ents[id]["t"].setdefault(name, [{"f": 0, "v": v}])
            tr[0] = {"f": 0, "v": v}

    def key(self, id, track, f, v, d=0, e="out", arc=None):
        if e not in EASES:
            raise SystemExit(f"{id}.{track} : assouplissement « {e} » inconnu")
        tr = self.ents[id]["t"].get(track)
        if tr is None:
            init = self.val(id, track, -10 ** 9, DEFAULTS.get(track))
            if init is None:
                raise SystemExit(f"{id}.{track} : valeur initiale manquante (Story.set)")
            tr = self.ents[id]["t"][track] = [{"f": 0, "v": init}]
        k = {"f": round(f, 3), "v": v}
        if d:
            k["d"] = round(d, 3)
            k["e"] = e
        if arc:
            k["arc"] = arc
        pos = bisect.bisect_right([x["f"] for x in tr[1:]], k["f"]) + 1
        tr.insert(pos, k)

    def keys(self, id, f, d=0, e="out", arc=None, **tracks):
        for name, v in tracks.items():
            self.key(id, name, f, v, d, e, arc if name == "pos" else None)

    # --- évaluation ---
    def val(self, id, track, n, fallback=None):
        return eval_track(self.ents[id]["t"].get(track), n, DEFAULTS.get(track, fallback) if fallback is None else fallback)

    def world(self, id, n):
        e = self.ents[id]
        s = self.val(id, "scale", n)
        m = local_matrix(self.val(id, "pos", n), self.val(id, "rot", n), s * self.val(id, "sx", n), s * self.val(id, "sy", n))
        return mat_mul(self.world(e["parent"], n), m) if e.get("parent") else m

    def world_scale(self, id, n):
        m = self.world(id, n)
        return math.hypot(m[0], m[1])

    def to_world(self, id, pt, n):
        return mat_apply(self.world(id, n), pt)

    def to_local(self, parent, pt, n):
        return mat_apply(mat_inv(self.world(parent, n)), pt)

    def parent_space(self, id, pt, n):
        """Point monde -> coordonnées du parent de `id` (ou monde s'il n'en a pas)."""
        par = self.ents[id].get("parent")
        return self.to_local(par, pt, n) if par else list(pt)

    def wire_cubic(self, wire_id, n):
        e = self.ents[wire_id]
        p = e["p"]
        A = (self.to_world(p["a"]["id"], self.val(wire_id, "aAt", n, p["a"]["at"]), n) if p.get("a")
             else self.val(wire_id, "pa", n))
        B = (self.to_world(p["b"]["id"], self.val(wire_id, "bAt", n, p["b"]["at"]), n) if p.get("b")
             else self.val(wire_id, "pb", n))
        return wire_cubic(A, B, self.val(wire_id, "sag", n, 0), p.get("tension", 0.45))

    # --- trajets calculés image par image ---
    def path(self, id, f, d, e, point_at, scale_at=None, offset=(0, 0)):
        """Clés image par image : à l'image f + k, l'entité est au point monde point_at(p) (+ offset, éventuellement
        fonction de p), p étant la progression assouplie ; `scale_at(p)` = échelle MONDE voulue. Les clés sont
        exprimées dans l'espace du parent à chaque image : le trajet monde est exact même si le parent bouge."""
        n_frames = max(1, int(math.ceil(d)))
        for k in range(n_frames):
            n = f + k
            p = _ease(e, min(1.0, (k + LEAD) / d))
            q = point_at(p)
            o = offset(p) if callable(offset) else offset
            q = [q[0] + o[0], q[1] + o[1]]
            self.key(id, "pos", n, [round(c, 3) for c in self.parent_space(id, q, n)], 1, "linear")
            if scale_at is not None:
                par = self.ents[id].get("parent")
                ps = self.world_scale(par, n) if par else 1.0
                self.key(id, "scale", n, round(scale_at(p) / ps, 5), 1, "linear")

    def fly(self, id, f, d, e="inOut", to=None, scale=None, arc=0):
        """Vol monde : de la position (et échelle) monde à l'image f - 1 vers `to` (point monde), en arc."""
        start = self.to_world(id, [0, 0], f - 1)
        s0 = self.world_scale(id, f - 1)
        to = to or start

        def pt(p):
            return [start[0] + (to[0] - start[0]) * p, start[1] + (to[1] - start[1]) * p - arc * 4 * p * (1 - p)]

        self.path(id, f, d, e, pt, (lambda p: s0 + (scale - s0) * p) if scale is not None else None)

    def along_wire(self, id, wire_id, f, d, e, t0, t1, at_frame, offset=(0, 0), scale=None):
        """Glisse le long du fil (géométrie figée à l'image `at_frame`) de la fraction de longueur t0 à t1."""
        cub = self.wire_cubic(wire_id, at_frame)
        s0 = self.world_scale(id, f - 1)
        self.path(id, f, d, e, lambda p: point_at_length(cub, t0 + (t1 - t0) * p),
                  (lambda p: s0 + (scale - s0) * p) if scale is not None else None, offset)

    # --- PNG ---
    def png(self, name, keep_largest=False):
        out_dir = GENERATED / "story" / self.video_id
        out_dir.mkdir(parents=True, exist_ok=True)
        src = ILLUSTRATIONS / f"{name}.png"
        if not src.exists():
            raise SystemExit(f"Illustration absente : {src}")
        stamp = f"{PNG_VERSION}:{keep_largest}:{src.stat().st_size}:{src.stat().st_mtime_ns}"
        png, info = out_dir / f"{name}.png", out_dir / f"{name}.json"
        if png.exists() and info.exists() and read_json(info).get("key") == stamp:
            meta = read_json(info)
        else:
            meta = {"key": stamp, **strict_png(name, png, keep_largest)}
            write_json(info, meta)
        meta["src"] = f"generated/story/{self.video_id}/{name}.png"
        self.assets[name] = meta
        return meta

    # --- export ---
    def entities(self):
        out = []
        for e in self.ents.values():
            t = {k: v for k, v in e["t"].items()}
            out.append({**e, "t": t})
        return out


# ---------- sous-titres ----------

def caption_track(words, fps, f0, f1, overrides=None, snapped=None, alert_words=None):
    """Groupes karaoké (2-3 mots) des mots qui commencent dans [f0, f1), en images du film. `overrides` : découpes
    imposées par la mise en scène (même format que « captions.groups » des plans, voir motion._fixed_groups).
    `snapped` : {indice du mot: image} des temps forts calés sur l'attaque audible (Story.beat) ; le mot s'allume
    alors sur la même image que l'événement, la voix, le surlignage et l'image coïncident. `alert_words` : mots en
    rouge (ALERT_WORDS du fichier de mise en scène)."""
    snapped = snapped or {}
    alert = {_norm(w) for w in (alert_words if alert_words is not None else ALERT_WORDS)}
    for run in overrides or []:
        for g in run:
            if len(g.split()) > OVERRIDE_MAX_WORDS:
                raise SystemExit(f"Découpe imposée de plus de {OVERRIDE_MAX_WORDS} mots : « {g} »")
    idx = [i for i, w in enumerate(words) if f0 <= round(w["start"] * fps) < f1]
    sub = [words[i] for i in idx]
    cap = STYLE["caption"]
    measure = CaptionMeasure(size=cap["size"], tracking_em=0.0, font_file=FONTS / "Inter-Bold.otf")
    groups = caption_groups(sub, measure, cap=cap, overrides=overrides)
    out = []
    for g in groups:
        ws, prev = [], None
        for j in g:
            f = snapped.get(idx[j], round(sub[j]["start"] * fps))
            if prev is not None and f <= prev:
                f = prev + 1
            prev = f
            text = clean_word(sub[j]["w"])
            w = {"text": text, "i": idx[j], "from": f}
            if _norm(text) in alert:
                w["tone"] = "alert"
            ws.append(w)
        out.append({"words": ws})
    for g in out:
        g["from"] = g["words"][0]["from"]   # un groupe ne s'affiche jamais avant son premier mot
    for k, g in enumerate(out):
        g["to"] = out[k + 1]["from"] if k + 1 < len(out) else f1
        g["width"] = round(measure.width(" ".join(w["text"] for w in g["words"])), 1)
    return out


# ---------- audio : coupe sans clic ----------

def _envelope(path, hop=0.005, win=0.010):
    with wave.open(str(path)) as w:
        sr, ch, n = w.getframerate(), w.getnchannels(), w.getnframes()
        x = np.frombuffer(w.readframes(n), dtype=np.int16).reshape(-1, ch).astype(np.float32).mean(1) / 32768
    h, k = int(sr * hop), int(sr * win)
    starts = np.arange(0, len(x) - k, h)
    env = np.sqrt(np.array([np.mean(x[s:s + k] ** 2) for s in starts]))
    return env, hop, sr


def acoustic_onset(env, hop, t_word, thr=0.03, floor=0.006, quiet=0.04, search=0.25):
    """Début acoustique du mot annoncé à t_word : premier passage de la voix au-dessus de `thr` (-30 dBFS, une
    respiration reste en dessous) précédé de `quiet` s sans voix, cherché dans [t_word - search, t_word + 0.03],
    puis reculé jusqu'au pied de l'attaque (`floor`)."""
    q = int(quiet / hop)
    lo, hi = int((t_word - search) / hop), int((t_word + 0.03) / hop)
    for i in range(max(q, lo), min(hi, len(env))):
        if env[i] > thr and (env[i - q:i] < thr).all():
            # recul jusqu'au pied de l'attaque, sans sortir du silence qui la précède (en milieu de phrase, la
            # voix ne redescend pas sous `floor` : sans borne, on reculerait jusqu'au début de la phrase)
            i0 = i
            while i > i0 - q and env[i - 1] > floor:
                i -= 1
            return i * hop
    return t_word


def audio_duration(audio):
    with wave.open(str(audio)) as w:
        return w.getnframes() / w.getframerate()


def attack_time(env, hop, t_word, window=0.08, thr=0.03, quiet=0.04):
    """Attaque audible du mot annoncé à t_word : premier passage de la voix au-dessus de `thr` (-30 dBFS) après
    `quiet` s de silence, cherché dans [t_word - window, t_word + window] ; None si rien de net (mot enchaîné)."""
    q = int(quiet / hop)
    lo, hi = int((t_word - window) / hop), int((t_word + window) / hop)
    for i in range(max(q, lo), min(hi, len(env))):
        if env[i] > thr and (env[i - q:i] < thr).all():
            return i * hop
    return None


def excerpt_window(audio, t_from, t_to, fps):
    """[F0, F1) sur la grille d'images du film : F0 juste avant le début acoustique du premier mot (la voix n'est pas
    coupée en pleine attaque), F1 avant le début acoustique du mot suivant. Bornée au film : F0 >= 0, et F1 <= la
    dernière image de audio.wav, entamée comprise (t_to à la fin de l'audio ou au-delà = jusqu'au bout, sans recherche)."""
    env, hop, _ = _envelope(audio)
    dur = audio_duration(audio)
    # Dernière image : celle qui contient encore de la voix (le film entier garde les dernières ms de audio.wav).
    last = math.ceil(dur * fps - 1e-6)
    on0 = acoustic_onset(env, hop, t_from) if t_from > 0.03 else 0.0
    f0 = 0 if t_from <= 0.03 else math.floor((min(t_from, on0 - 0.015)) * fps + 1e-9)
    if t_to >= dur - 1e-3:
        on1, f1 = dur, last
    else:
        on1 = acoustic_onset(env, hop, t_to)
        f1 = math.floor((min(t_to, on1 - 0.010)) * fps + 1e-9)
    f0, f1 = max(0, f0), min(f1, last)
    if f1 <= f0:
        raise SystemExit(f"Fenêtre vide : {t_from} -> {t_to} s (audio de {dur:.3f} s)")
    return f0, f1, on0, on1


def cut_audio(audio, f0, f1, fps, out, fade_in=0.005, fade_out=0.08):
    with wave.open(str(audio)) as w:
        sr, n = w.getframerate(), w.getnframes()
    s0, s1 = max(0, round(f0 / fps * sr)), min(n, round(f1 / fps * sr))
    dur = (s1 - s0) / sr
    run(["ffmpeg", "-hide_banner", "-y", "-i", str(audio), "-af",
         f"atrim=start_sample={s0}:end_sample={s1},asetpts=PTS-STARTPTS,"
         f"afade=t=in:st=0:d={fade_in},afade=t=out:st={dur - fade_out:.6f}:d={fade_out}",
         "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(out)])
    return dur


# ---------- rendu ----------

def load_spec(video_id):
    path = SPECS / f"{video_id}.py"
    if not path.exists():
        raise SystemExit(f"Mise en scène absente : {path}")
    spec = importlib.util.spec_from_file_location(f"story_spec_{video_id}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, path


LEAD_IN_MAX = 1.0   # s : une scène dont l'extrait ne montre que la fin (ou le début) sur moins d'1 s ne le nomme pas


def scene_overlaps(storyboard, t_from, t_to):
    """[(id, durée couverte, durée de la scène)] des scènes touchées par la fenêtre."""
    out = []
    for s in storyboard["scenes"]:
        cov = min(t_to, s["t_end"]) - max(t_from, s["t_start"])
        if cov > 1e-3:
            out.append((s["id"], cov, s["t_end"] - s["t_start"]))
    return out


def scene_range(storyboard, t_from, t_to):
    """Étiquette « Sa-Sb » de l'extrait. Une scène seulement effleurée (moins de LEAD_IN_MAX s, et pas en entier :
    ex. la fin de S10 montrée en ouverture d'un extrait S11-S14) est une amorce et ne compte pas."""
    hits = scene_overlaps(storyboard, t_from, t_to)
    ids = [i for i, cov, dur in hits if cov >= min(LEAD_IN_MAX, dur - 1e-3)] or [i for i, _, _ in hits]
    return f"{ids[0]}-{ids[-1]}" if len(ids) > 1 else ids[0]


def lead_in_scenes(storyboard, t_from, t_to):
    label = scene_range(storyboard, t_from, t_to).split("-")
    ids = [s["id"] for s in storyboard["scenes"]]
    lo, hi = ids.index(label[0]), ids.index(label[-1])
    return [i for i, _, _ in scene_overlaps(storyboard, t_from, t_to) if not lo <= ids.index(i) <= hi]


def build_props(video_id, t_from, t_to, captions=True):
    cfg = load_config()
    fps = cfg["video"]["fps"]
    out_dir = build_dir(video_id) / "story"
    out_dir.mkdir(parents=True, exist_ok=True)
    words = read_json(build_dir(video_id) / "words.json")["words"]
    storyboard = read_json(STORYBOARDS / f"{video_id}.json")
    audio = build_dir(video_id) / "audio.wav"
    f0, f1, on0, on1 = excerpt_window(audio, t_from, t_to, fps)
    mod, spec_path = load_spec(video_id)
    snap = None
    if getattr(mod, "ACOUSTIC_SNAP", None):
        env, hop, _ = _envelope(audio)
        snap = {**mod.ACOUSTIC_SNAP, "attack": lambda t: attack_time(env, hop, t, mod.ACOUSTIC_SNAP["window"])}
    story = Story(video_id, words, storyboard, fps, cfg["video"]["width"], cfg["video"]["height"], snap=snap)
    mod.build(story)
    snapped_frames = {b["i"]: b["frame"] for b in story.beats if "attack_t" in b}
    caps = caption_track(words, fps, f0, f1, getattr(mod, "CAPTION_GROUPS", None), snapped=snapped_frames,
                         alert_words=getattr(mod, "ALERT_WORDS", None))
    label = scene_range(storyboard, t_from, t_to)
    lead_in = lead_in_scenes(storyboard, t_from, t_to)
    onsets = {round(w["start"] * fps) for w in words}
    off = sorted({b["frame"] for b in story.beats if b["frame"] not in onsets and "attack_t" not in b})
    snapped = [f"{b['scene']} « {b['word']} » {b['word_frame']} -> {b['frame']}" for b in story.beats if "attack_t" in b]
    covered = {(b["scene"], _norm(b["word"])) for b in story.beats}
    missing = [f"{s['id']} « {b['mot']} »" for s in storyboard["scenes"] for b in s["beats"]
               if f0 <= round(b["t"] * fps) < f1 and (s["id"], _norm(b["mot"])) not in covered]
    # Une mise en scène partielle (ex. V01 : S11-S14, état de fin de S10 reconstitué à l'image 0) ne couvre pas le
    # film entier : avant sa première scène, l'image reste figée sur l'état reconstitué.
    # Images où commence au moins une clé (± 1 image : un événement peut être amorcé juste avant son mot).
    starts = {round(k["f"]) + d for e in story.ents.values() for tr in e["t"].values() for k in tr[1:] for d in (-1, 0, 1)}
    staged = sorted({b["scene"] for b in story.beats})
    first_staged = min((round(s["t_start"] * fps) for s in storyboard["scenes"] if s["id"] in staged), default=f0)
    unstaged_before = f0 < first_staged - fps // 2     # tolérance : la pré-attaque acoustique d'un extrait
    props = {
        "id": f"{video_id}_{label}",
        "fps": fps, "width": story.width, "height": story.height,
        "durationInFrames": f1 - f0, "frameOffset": f0,
        "style": {k: v for k, v in STYLE.items()},
        "entities": story.entities(),
        "captions": caps,
        "showCaptions": captions,
        "meta": {"video": video_id, "scenes": label, "from_s": t_from, "to_s": t_to,
                 "window_frames": [f0, f1], "window_s": [round(f0 / fps, 4), round(f1 / fps, 4)],
                 "acoustic_onsets_s": [round(on0, 3), round(on1, 3)],
                 "storyboard": str((STORYBOARDS / f"{video_id}.json").relative_to(ROOT)),
                 "spec": str(spec_path.relative_to(ROOT)), "assets": story.assets,
                 "beats": sorted(story.beats, key=lambda b: b["frame"]), "beats_off_onset": off,
                 "beats_snapped_to_attack": snapped,
                 "storyboard_beats_missing": missing, "staged_scenes": staged, "lead_in_scenes": lead_in,
                 "frame_mapping": "image de l'extrait = image du film - window_frames[0] = round(t * fps) - window_frames[0]",
                 # Images clés forcées (x264) sur les temps forts : le rafraîchissement tombe dans un mouvement,
                 # jamais dans une tenue immobile (comme pipeline/motion.py).
                 # Un temps fort de tenue (« et » : rien ne bouge) n'en reçoit pas : rien n'y commence.
                 "keyframes": sorted({f0} | {b["frame"] for b in story.beats
                                             if f0 <= b["frame"] < f1 and b["frame"] in starts}),
                 "unstaged_before_frame": first_staged if unstaged_before else None},
    }
    suffix = "" if captions else "_nocap"
    path = out_dir / f"props_{label}{suffix}.json"
    text = json.dumps(props, ensure_ascii=False, indent=1) + "\n"
    if not path.exists() or path.read_text(encoding="utf-8") != text:
        path.write_text(text, encoding="utf-8")
    n_keys = sum(len(t) for e in props["entities"] for t in e["t"].values())
    print(f"{video_id} {label} : images du film {f0}-{f1} ({(f1 - f0) / fps:.3f} s, de {f0 / fps:.3f} à {f1 / fps:.3f} s ; "
          f"débuts acoustiques {on0:.3f} / {on1:.3f} s), {len(props['entities'])} entités, {n_keys} clés, "
          f"{len(caps)} groupes de sous-titres -> {path}")
    if lead_in:
        print(f"  amorce : fin de {', '.join(lead_in)} en ouverture (moins de {LEAD_IN_MAX:.0f} s) ; étiquette {label}")
    print("  temps forts (image du film -> image de l'extrait #) :")
    for b in sorted(story.beats, key=lambda b: b["frame"]):
        if f0 <= b["frame"] < f1:
            snap = f" (mot {b['word_frame']}, attaque {b['attack_t']} s)" if "attack_t" in b else ""
            print(f"    {b['scene']} « {b['word']} » {b['frame']} -> #{b['frame'] - f0}{snap}")
    if off:
        print("  attention : temps forts hors début de mot :", off)
    if snapped:
        print("  calés sur l'attaque audible :", ", ".join(snapped))
    if missing:
        print("  attention : temps forts du storyboard sans événement :", ", ".join(missing))
    if unstaged_before:
        print(f"  attention : la mise en scène ({spec_path.name}) ne couvre que {staged[0]}-{staged[-1]} ; "
              f"de l'image {f0} à {first_staged} ({f0 / fps:.2f}-{first_staged / fps:.2f} s) l'image reste figée sur "
              f"l'état initial reconstitué")
    return path, props


def remotion_render(props_path, silent):
    if not (MOTION / "node_modules").is_dir():
        raise SystemExit("motion/node_modules absent : lance « npm ci » dans motion/.")
    cmd = ["npx", "remotion", "render", "Story", str(silent), f"--props={props_path}", "--muted", "--log=error"]
    props = read_json(props_path)
    fps, off = props["fps"], props["frameOffset"]
    # Images clés forcées sur les temps forts (motion/remotion.config.ts lit WTH_KEYFRAMES, en secondes de la
    # vidéo rendue, juste avant l'image visée) : jamais de rafraîchissement GOP dans une tenue.
    kf = props.get("meta", {}).get("keyframes", [off])
    env = remotion_env(WTH_KEYFRAMES=",".join(f"{max(0.0, (f - off) / fps - 0.001):.4f}" for f in kf))
    t0 = time.time()
    proc = subprocess.run(cmd, cwd=MOTION, text=True, capture_output=True, env=env)
    if proc.returncode != 0:
        print(proc.stdout[-4000:], proc.stderr[-4000:])
        raise SystemExit(f"Rendu Remotion en échec ({proc.returncode})")
    print(f"  rendu Remotion {time.time() - t0:.0f} s -> {silent}")


def mux(silent, wav, out, dur, cfg, tags):
    out.parent.mkdir(parents=True, exist_ok=True)
    v = cfg["video"]
    meta = []
    for k, val in tags.items():
        meta += ["-metadata", f"{k}={val}"]
    run(["ffmpeg", "-hide_banner", "-y", "-i", str(silent), "-i", str(wav), "-map", "0:v:0", "-map", "1:a:0",
         "-c:v", "copy", "-c:a", "aac", "-b:a", v["audio_bitrate"], "-ar", str(v["audio_rate"]), "-ac", "2",
         *meta, "-t", f"{dur:.6f}", "-movflags", "+faststart+use_metadata_tags", str(out)])
    probe = ffprobe(out)
    vs = next(s for s in probe["streams"] if s["codec_type"] == "video")
    aus = next(s for s in probe["streams"] if s["codec_type"] == "audio")
    print(f"  {out} : {float(probe['format']['duration']):.3f} s, {vs['codec_name']} {vs['pix_fmt']} "
          f"{vs.get('color_space')}/{vs.get('color_primaries')}/{vs.get('color_transfer')} {vs['width']}x{vs['height']} "
          f"{vs['r_frame_rate']}, {aus['codec_name']} {aus['sample_rate']} Hz {aus['channels']} canaux")
    return probe


def contact_sheets(mp4, out_dir, f0, fps, step=5, cols=10, thumb_w=180):
    """Images du MP4 à 6 i/s (une sur `step`) -> keyframes.png + une planche par seconde (sheets/sec_XX.png)."""
    frames_dir = out_dir / "frames"
    if frames_dir.exists():
        for f in frames_dir.glob("*.png"):
            f.unlink()
    frames_dir.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-hide_banner", "-y", "-i", str(mp4), "-vf", f"select=not(mod(n\\,{step}))", "-vsync", "0",
         str(frames_dir / "k_%04d.png")])
    files = sorted(frames_dir.glob("k_*.png"))
    font = ImageFont.truetype(str(FONTS / "Inter-SemiBold.otf"), 15)
    big = ImageFont.truetype(str(FONTS / "Inter-SemiBold.otf"), 20)

    def sheet(items, cols, tw, fnt, path):
        th = round(tw * 1920 / 1080)
        rows = math.ceil(len(items) / cols)
        im = Image.new("RGB", (cols * (tw + 6) + 6, rows * (th + 28) + 6), (40, 40, 44))
        d = ImageDraw.Draw(im)
        for k, (n, f) in enumerate(items):
            x, y = 6 + (k % cols) * (tw + 6), 6 + (k // cols) * (th + 28)
            im.paste(Image.open(f).convert("RGB").resize((tw, th), Image.LANCZOS), (x, y + 24))
            d.text((x + 2, y + 2), f"#{n}  {(f0 + n) / fps:.2f} s", font=fnt, fill=(235, 235, 235))
        im.save(path)
        return path

    items = [((k) * step, f) for k, f in enumerate(files)]
    keyframes = sheet(items, cols, thumb_w, font, out_dir / "keyframes.png")
    sec_dir = out_dir / "sheets"
    sec_dir.mkdir(exist_ok=True)
    for f in sec_dir.glob("*.png"):
        f.unlink()
    per = fps // step
    for s in range(math.ceil(len(items) / per)):
        sheet(items[s * per:(s + 1) * per], per, 300, big, sec_dir / f"sec_{s:02d}.png")
    print(f"  planches : {keyframes} ({len(items)} images à {fps / step:.0f} i/s) + {sec_dir}/sec_XX.png")
    return keyframes


def stills(video_id, t_from, t_to, frames, captions=True):
    props_path, _ = build_props(video_id, t_from, t_to, captions)
    out = build_dir(video_id) / "story" / "stills"
    proc = subprocess.run(["node", "scripts/story_stills.mjs", str(props_path), str(out), *map(str, frames)], cwd=MOTION,
                          text=True, capture_output=True, env=remotion_env())
    if proc.returncode != 0:
        print(proc.stdout[-3000:], proc.stderr[-3000:])
        raise SystemExit("Images fixes en échec")
    print(f"{video_id} : {len(frames)} images fixes -> {out}")


def excerpt(video_id, t_from, t_to, captions=True, sheets=True):
    """Rendu de l'extrait : version sans sous-titres (build/Vxx/story/) et, sauf --no-captions, version avec
    sous-titres (output/extraits/), toutes deux avec la voix coupée image par image."""
    cfg = load_config()
    fps = cfg["video"]["fps"]
    out_dir = build_dir(video_id) / "story"
    storyboard = read_json(STORYBOARDS / f"{video_id}.json")
    label = scene_range(storyboard, t_from, t_to)
    results = {}
    variants = [False] + ([True] if captions else [])
    wav = None
    for cap in variants:
        props_path, props = build_props(video_id, t_from, t_to, captions=cap)
        f0, f1 = props["meta"]["window_frames"]
        if wav is None:
            wav = out_dir / f"voix_{label}.wav"
            dur = cut_audio(build_dir(video_id) / "audio.wav", f0, f1, fps, wav)
        silent = out_dir / f"muet_{label}{'' if cap else '_nocap'}.mp4"
        remotion_render(props_path, silent)
        full = props["meta"]["window_frames"][0] == 0 and f1 >= math.ceil(audio_duration(build_dir(video_id) / "audio.wav") * fps - 1e-6)
        if cap:
            mp4 = (OUTPUT / f"WTH-{video_id}_story.mp4") if full else (OUTPUT / "extraits" / f"WTH-{video_id}_extrait_{label}.mp4")
        else:
            mp4 = out_dir / ("film_sans_sous_titres.mp4" if full else "extrait_sans_sous_titres.mp4")
        mux(silent, wav, mp4, (f1 - f0) / fps, cfg,
            {"wth_mode": "story", "wth_scenes": label, "wth_window": f"{f0}-{f1}", "wth_captions": int(cap)})
        results[cap] = mp4
    if sheets:
        contact_sheets(results[captions], out_dir, props["meta"]["window_frames"][0], fps)
    return results


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("id")
    p.add_argument("--from", dest="t_from", type=float, help="début (s) : début du premier mot")
    p.add_argument("--to", dest="t_to", type=float, help="fin (s) : début du mot qui suit l'extrait")
    p.add_argument("--full", action="store_true", help="le film entier : de 0 à la fin de audio.wav")
    p.add_argument("--no-captions", action="store_true", help="seulement la version sans sous-titres")
    p.add_argument("--props", action="store_true", help="props seulement, sans rendu")
    p.add_argument("--stills", nargs="+", type=int, metavar="IMAGE", help="images fixes (images de l'extrait)")
    p.add_argument("--no-sheets", action="store_true", help="sans planches de contrôle")
    a = p.parse_args()
    if a.full:
        a.t_from, a.t_to = 0.0, audio_duration(build_dir(a.id) / "audio.wav")
    elif a.t_from is None or a.t_to is None:
        p.error("--from et --to sont requis (ou --full)")
    if a.stills:
        stills(a.id, a.t_from, a.t_to, a.stills, captions=not a.no_captions)
    elif a.props:
        build_props(a.id, a.t_from, a.t_to, captions=not a.no_captions)
    else:
        excerpt(a.id, a.t_from, a.t_to, captions=not a.no_captions, sheets=not a.no_sheets)


if __name__ == "__main__":
    main()
