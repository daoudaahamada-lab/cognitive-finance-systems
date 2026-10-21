"""Kit de mise en scène Story : macros de la grammaire (pop, morph, move…), figurine articulée (bras à 2 os de longueur
fixe), fiche, repère d'étapes, carte de fin, et une fonction de déclaration par entité du kit (entities_kit.tsx).

    from pipeline.story_kit import Figure, Kit, Sheet
    kit = Kit(S)
    f = kit.at("S05", "limites")                  # temps fort du storyboard (= S.beat)
    kit.pop("loupe", f)                            # apparition 300 ms
    kit.morph(["dossier"], ["outil"], f)           # passage d'une composition à l'autre, mêmes images
    toi = Figure(kit, "toi", pos=[800, 1040])      # figurine encre + bras + stylo
    hit = toi.tap(f, sheet.world(S, 0, "tick", n=f))   # image du contact : déclenche la coche

Tout passe par l'API Story (key, keys, path, fly, val, to_world) : le rendu ne change pas. Images = images du FILM ;
chaque macro renvoie l'image qui suit son mouvement (f + d), sauf mention contraire. Référence complète (signatures,
comportement, exemples) : .claude/skills/wth-story-build/references/kit.md (à la racine du dépôt) ; entités :
references/entities.md ; démonstration : scripts/story/_demo_kit.py.
"""
import math

from .story import (DRAW, DROP, FADE, GEOM, MORPH, MOVE, POP, _ease, text_width)

# ---------- constantes ----------
WRITE_RATE = 3.5      # caractères par image (V01 : L1-L4 écrites par l'IA)
TRACE_SPEED = 20      # px par image : la pointe qui relit une colonne (V01 : 18 images pour 4 rangées)
WALK_SPEED = 7        # px par image
HOP, HOP_PERIOD, WALK_LEAN = 5, 8, 4   # marche : petits sauts de 5 px toutes les 8 images, penchée de 4°
REACH = 0.94          # au-delà de 94 % de l'allonge (bras + stylo), la figurine fait un pas vers la cible
REACH_STAMP = 0.98    # coup de tampon : bras presque tendu (main seule, sans stylo)
WRIST = 0.35          # cible trop près de l'épaule : la prise reste à 35 % de (bras + avant-bras), le poignet plie
REST_UP = 255         # stylo levé au repos (V01) : pointe en haut, un peu vers l'extérieur (bras à gauche)
TAP = 8               # images d'un tapotement (approche + coup)
STEP = 8              # images du pas fait avant un coup de tampon hors d'atteinte
_TRACKS0 = {"draw": 0, "chars": 0, "value": 0, "ring": 0, "press": 0, "mark": 0, "under": 0, "strike": 0, "pulse": 0,
            "flash": 0, "lean": 0, "btn": 0, "title": 0, "show": 0, "link": 0, "handle": 1, "active": 0}


# ---------- géométrie ----------

def lerp(a, b, p):
    if isinstance(a, (int, float)):
        return a + (b - a) * p
    return [a[k] + (b[k] - a[k]) * p for k in range(len(a))]


def ang_lerp(a, b, p):
    """Angle (degrés) de a vers b par le plus court chemin."""
    return a + ((b - a + 180) % 360 - 180) * p


def r3(pt):
    return [round(c, 3) for c in pt]


def rotate_about(pt, deg, c):
    """Comme entities.tsx rotateAbout (penché `lean` du bras autour du pied de la figurine)."""
    t = math.radians(deg)
    dx, dy = pt[0] - c[0], pt[1] - c[1]
    return [c[0] + dx * math.cos(t) - dy * math.sin(t), c[1] + dx * math.sin(t) + dy * math.cos(t)]


def frames(f, d, e):
    """(image, progression assouplie) d'un segment de d images commençant en f (LEAD : l'image f montre le pas 1/d)."""
    for k in range(int(math.ceil(d))):
        yield f + k, _ease(e, min(1.0, (k + 1) / d))


def solve_ik(shoulder, target, l1, l2, bend=1):
    """Bras à 2 os de longueurs FIXES l1 (épaule -> coude) et l2 (coude -> main) vers `target` -> (coude, main, atteint).
    Hors d'atteinte, la main s'arrête sur la droite épaule -> cible (bras tendu, ou replié au plus court) : les deux
    longueurs restent exactes. bend = +1 : coude à gauche du trajet épaule -> main (en dessous pour un bras qui se tend
    vers la gauche), -1 : de l'autre côté."""
    ax, ay = shoulder
    dx, dy = target[0] - ax, target[1] - ay
    d = math.hypot(dx, dy)
    lo, hi = abs(l1 - l2), l1 + l2
    if hi < 1e-9:
        return [ax, ay], [ax, ay], d < 1e-6
    ux, uy = (dx / d, dy / d) if d > 1e-9 else (0.0, 1.0)
    dc = min(max(d, lo, 1e-9), hi)
    a = (l1 * l1 - l2 * l2 + dc * dc) / (2 * dc)
    h = math.sqrt(max(0.0, l1 * l1 - a * a))
    nx, ny = (uy, -ux) if bend > 0 else (-uy, ux)
    elbow = [ax + ux * a + nx * h, ay + uy * a + ny * h]
    return elbow, [ax + ux * dc, ay + uy * dc], lo - 1e-6 <= d <= hi + 1e-6


def crowd_points(p):
    """Positions des figurines d'une foule (copie de entities_kit.tsx crowdPoints : `pts: []` donne une foule vide,
    comme en TypeScript où un tableau vide est vrai)."""
    if p.get("pts") is not None:
        return [list(q) for q in p["pts"]]
    n = p.get("n", 6)
    if p.get("layout") == "row":
        gap = p.get("gap", 56)
        return [[(i - (n - 1) / 2) * gap, 0] for i in range(n)]
    r, span, a0 = p.get("r", 130), p.get("span", 360), p.get("a0", -90)
    step = span / n if span >= 360 else span / max(1, n - 1)
    return [[r * math.cos(math.radians(a0 + step * i)), r * math.sin(math.radians(a0 + step * i))] for i in range(n)]


def js_round(x):
    """Math.round de JavaScript : entier le plus proche, les demis vers +∞ (round de Python arrondit au pair)."""
    r = math.floor(x)
    return r + 1 if x - r >= 0.5 else r


def format_fr(v, decimals=0, sign=False):
    """Nombre en typographie française (copie de entities_kit.tsx formatFr) : 12 500, 3,5, −40 ; les demis sont
    arrondis comme Math.round (2,5 -> 3 ; 0,125 à 2 décimales -> 0,13)."""
    x = js_round(abs(v) * 10 ** decimals) / 10 ** decimals
    ent, _, dec = f"{x:.{decimals}f}".partition(".")
    grouped = f"{int(ent):,}".replace(",", "\u202f")
    s = "" if x == 0 else "\u2212" if v < 0 else "+" if sign else ""
    return s + grouped + ("," + dec if dec else "")


def _num_diff(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b)
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        return max((abs(x - y) for x, y in zip(a, b)), default=0.0)
    return 0.0 if a == b else math.inf


# ---------- macros ----------

class Kit:
    """Macros de la grammaire du mouvement (motion-grammar : durées de la référence) sur une Story."""

    def __init__(self, S):
        self.S = S
        self.warnings = []

    def warn(self, msg):
        self.warnings.append(msg)
        print(f"  attention (kit) : {msg}")

    def ensure(self, id, track, v=None):
        """Valeur initiale d'une piste (Story.key l'exige) : `v`, ou 0 / la valeur neutre de la piste."""
        if track not in self.S.ents[id]["t"] and track not in ("pos", "scale", "rot", "opacity", "sx", "sy"):
            self.S.set(id, **{track: _TRACKS0.get(track, 0) if v is None else v})

    def _world_of(self, x, n):
        return self.S.to_world(x, [0, 0], n) if isinstance(x, str) else list(x)

    # --- temps ---
    def at(self, scene, mot, what=""):
        """Temps fort du storyboard (scène, mot) -> image (= Story.beat, vérifié à ±30 ms)."""
        return self.S.beat(scene, mot, what)

    def hold(self, scene, mot, what="tenue : rien ne bouge"):
        """Temps fort de tenue : posé (couverture du storyboard) sans événement ; rien ne doit y commencer."""
        return self.S.beat(scene, mot, what)

    def pin(self, f, states, tol=0.5):
        """État imposé à l'image f (début d'une partie : état initial du storyboard) : {id: {piste: valeur}}. Une
        valeur différente à f - 1 (fin de la partie précédente) est signalée : un saut se verrait. Renvoie f."""
        S = self.S
        for id, tracks in states.items():
            for track, v in tracks.items():
                tr = S.ents[id]["t"].get(track)
                if tr is None and track not in ("pos", "scale", "rot", "opacity", "sx", "sy"):
                    S.set(id, **{track: v})
                    continue
                cur = S.val(id, track, f - 1)
                if _num_diff(cur, v) > tol:
                    self.warn(f"pin {f} : {id}.{track} vaut {cur} à l'image {f - 1}, imposé {v} (saut)")
                S.key(id, track, f, v)
        return f

    # --- apparitions, disparitions ---
    def pop(self, id, f, scale=None, from_pt=None, to=None, d=POP, e="out"):
        """Apparition : échelle 0 -> `scale` (300 ms, ease-out, sans rebond). `from_pt` (point monde ou id) : naît là
        et glisse à sa place (`to`, repère du parent, ou sa position actuelle) pendant qu'il grandit. Clés : scale
        (0 à f - 1, puis -> scale en d), opacity (1 à f si elle était < 1), pos (from_pt -> to)."""
        S = self.S
        s0 = S.val(id, "scale", f - 1)
        s1 = scale if scale is not None else (s0 if s0 > 1e-6 else 1)
        if s0 != 0:
            S.key(id, "scale", f - 1, 0)
        if S.val(id, "opacity", f - 1) < 1:
            S.key(id, "opacity", f, 1)
        if from_pt is not None or to is not None:
            target = list(to) if to is not None else S.val(id, "pos", f - 1)
            if from_pt is not None:
                S.key(id, "pos", f - 1, r3(S.parent_space(id, self._world_of(from_pt, f - 1), f - 1)))
            S.key(id, "pos", f, r3(target), d, e)
        S.key(id, "scale", f, s1, d, e)
        return f + d

    def vanish(self, id, f, into=None, d=POP, e="out", style=None, n=7, spread=42, color="ink", sw=4):
        """Disparition : se réduit vers son centre (ou vers `into`, point monde ou id) puis opacité 0. Clés : scale
        (-> 0 en d), pos (-> into), opacity (0 à f + d).

        style="burst" (facultatif ; défaut inchangé) : l'élément ÉCLATE. Il se réduit en 3 images pendant que `n`
        éclats en tirets (`color`, `sw`), posés sur son contour (ellipse w x h du paramètre de l'entité, à son échelle
        monde), filent de `spread` px vers l'extérieur et s'effacent en `d` images (8 par défaut : 250 ms). Les éclats
        sont déclarés ici (ids `<id>__eclat<f>_<k>`, calque de l'élément + 0,5). -> f + d."""
        S = self.S
        if style == "burst":
            return self._burst(id, f, 8 if d == POP else d, n, spread, color, sw)
        if into is not None:
            S.key(id, "pos", f, r3(S.parent_space(id, self._world_of(into, f + d), f + d)), d, e)
        S.key(id, "scale", f, 0, d, e)
        S.key(id, "opacity", f + d, 0)
        return f + d

    def _burst(self, id, f, d, n, spread, color, sw):
        """vanish(style="burst") : éclats en tirets qui filent vers l'extérieur et s'effacent."""
        S = self.S
        c = S.to_world(id, [0, 0], f - 1)
        s = S.world_scale(id, f - 1)
        p = S.ents[id]["p"]
        w = p.get("w", 2 * p.get("r", 50)) * s
        h = p.get("h", w / max(s, 1e-6)) * s
        rx, ry = max(w / 2, 12), max(h / 2, 12)
        L = max(14.0, min(34.0, 0.22 * (rx + ry)))
        z = S.ents[id].get("z", 0) + 0.5
        for k in range(n):
            a = 2 * math.pi * k / n + 0.35
            pt = [c[0] + rx * math.cos(a), c[1] + ry * math.sin(a)]
            out = [pt[0] + spread * math.cos(a), pt[1] + spread * math.sin(a)]
            fid = f"{id}__eclat{f}_{k}"
            S.add(fid, "shape", z=z, kind="poly", pts=[[-L / 2, 0], [L / 2, 0]], closed=False, fill="none",
                  stroke=color, sw=sw, dash=[7, 5], shadow=0)
            S.set(fid, pos=r3(pt), scale=0, opacity=1, rot=round(math.degrees(a) + 90, 2))
            S.key(fid, "scale", f, 1)
            S.key(fid, "pos", f, r3(out), d, "out")
            S.key(fid, "scale", f + 1, 0.6, d - 1, "in")
            S.key(fid, "opacity", f + 2, 0, d - 2, "linear")
        S.key(id, "scale", f, 0, 3, "out")
        S.key(id, "opacity", f + 3, 0)
        return f + d

    def morph(self, outs, ins, f, d=MORPH, pair=None, e="out"):
        """Passage d'une composition à l'autre (350 ms) : les sortants se réduisent vers leur centre pendant que les
        entrants grandissent, dans les mêmes images. `pair` (défaut : autant de sortants que d'entrants) : l'entrant i
        naît à la place du sortant i et le sortant i se réduit vers la place de l'entrant i (relais)."""
        outs = [outs] if isinstance(outs, str) else list(outs)
        ins = [ins] if isinstance(ins, str) else list(ins)
        pair = len(outs) == len(ins) if pair is None else pair
        born = {i: self.S.to_world(o, [0, 0], f - 1) for i, o in enumerate(outs)}
        for i, o in enumerate(outs):
            self.vanish(o, f, into=ins[i] if pair and i < len(ins) else None, d=d, e=e)
        for j, x in enumerate(ins):
            self.pop(x, f, from_pt=born[j] if pair and j in born else None, d=d, e=e)
        return f + d

    # --- mouvements ---
    def move(self, id, f, to, d=MOVE, e="inOut", arc=None, scale=None, world=False):
        """Déplacement (550 ms, ease-in-out) vers `to` (repère du parent ; world=True : point monde, trajet image par
        image même si le parent bouge — Story.fly). `arc` px : bombé vers le haut à mi-course. Clés : pos (+ scale)."""
        if world:
            self.S.fly(id, f, d, e, to=list(to), scale=scale, arc=arc or 0)
            return f + d
        self.S.key(id, "pos", f, r3(to), d, e, arc)
        if scale is not None:
            self.S.key(id, "scale", f, scale, d, e)
        return f + d

    def draw(self, id, f, d=DRAW, track="draw", e="out", to=1):
        """Trait tracé (fil, contour, coche…) : piste `track` 0 -> `to` en d images (250-450 ms)."""
        self.ensure(id, track, 0)
        self.S.key(id, track, f, to, d, e)
        return f + d

    def fade(self, id, f, to=1, d=FADE, frm=None, e="out"):
        """Fondu d'opacité (200 ms ; texte et interface seulement). `frm` : valeur posée à f - 1."""
        if frm is not None:
            self.S.key(id, "opacity", f - 1, frm)
        self.S.key(id, "opacity", f, to, d, e)
        return f + d

    def pulse(self, id, f, times=1, peak=None, step=3, track="scale"):
        """Battement : `track` monte à `peak` puis revient, `times` fois (pas de `step` images). scale : peak = 1,15 x la
        valeur actuelle ; autre piste (pulse d'une ligne, d'une bulle) : peak = 1. V01 « fausse » : times=2, step=2."""
        self.ensure(id, track, 0)
        base = self.S.val(id, track, f - 1)
        peak = (base * 1.15 if track == "scale" else 1) if peak is None else peak
        for k in range(times):
            self.S.key(id, track, f + 2 * k * step, peak, step, "out")
            self.S.key(id, track, f + (2 * k + 1) * step, base, step, "inOut")
        return f + 2 * times * step

    def shake(self, id, f, amp=6, axis="x"):
        """Secousse de 3 images (clés instantanées) autour de la position à f - 1 : axis x (case vide qui refuse), y,
        ou xy (la page sous le tampon : +4/-3, -3/+2, 0)."""
        x, y = self.S.val(id, "pos", f - 1)
        offs = {"x": [(amp, 0), (-0.8 * amp, 0), (0, 0)], "y": [(0, amp), (0, -0.8 * amp), (0, 0)],
                "xy": [(amp, -0.75 * amp), (-0.75 * amp, 0.5 * amp), (0, 0)]}[axis]
        for k, (dx, dy) in enumerate(offs):
            self.S.key(id, "pos", f + k, r3([x + dx, y + dy]))
        return f + len(offs)

    def drop(self, id, f, h=None, d=DROP, out=False, dx=0, rot=0, to=None):
        """Chute (370 ms, ease-out, sans rebond). Entrée (défaut) : tombe de `h` px (240) au-dessus de sa place (`to`
        ou position actuelle), visible dès f. out=True : tombe de sa place de `h` px (60), décalée de dx, tournée de
        `rot`°, puis s'efface (la coche de l'IA chassée par le stylo : h=52, dx=18, rot=35)."""
        S = self.S
        x, y = S.val(id, "pos", f - 1)
        if out:
            h = 60 if h is None else h
            S.key(id, "pos", f, r3([x + dx, y + h]), d, "out")
            if rot:
                S.key(id, "rot", f, S.val(id, "rot", f - 1) + rot, d, "out")
            S.key(id, "opacity", f + d // 2, 0, 6, "linear")
            return f + d
        h = 240 if h is None else h
        x, y = to if to is not None else (x, y)
        S.key(id, "pos", f - 1, r3([x + dx, y - h]))
        if S.val(id, "scale", f - 1) < 1e-6:
            S.key(id, "scale", f - 1, 1)
        if S.val(id, "opacity", f - 1) < 1:
            S.key(id, "opacity", f, 1)
        S.key(id, "pos", f, r3([x, y]), d, "out")
        return f + d

    def type(self, id, f, n=None, rate=WRITE_RATE, flash=False):
        """Machine à écrire (piste chars, linéaire) : `n` caractères (défaut : tout le texte ; une ligne de fiche : clé
        + valeur) à `rate` caractères par image. flash=True : la puce d'une ligne bat au départ. Renvoie l'image qui
        suit le dernier caractère."""
        p = self.S.ents[id]["p"]
        if n is None:
            n = len(p["key"]) + len(p["value"]) if "key" in p else len(p.get("text", "").replace("\n", ""))
        self.ensure(id, "chars", 0)
        self.S.key(id, "chars", f, n, n / rate, "linear")
        if flash:
            self.ensure(id, "flash", 0)
            self.S.key(id, "flash", f, 1, 2, "out")
            self.S.key(id, "flash", f + 2, 0, 3, "inOut")
        return math.ceil(f + n / rate)

    def stagger(self, ids, f, step, fn, *args, **kw):
        """fn(id, f + i x step, *args, **kw) pour chaque id (décalage régulier) -> liste des retours."""
        return [fn(id, f + i * step, *args, **kw) for i, id in enumerate(ids)]

    # --- déclarations : une fonction par entité du kit (entities_kit.tsx) ---
    def _add(self, id, type, pos, z, parent, scale, opacity, rot, tracks, **p):
        S = self.S
        S.add(id, type, z=z, parent=parent, **{k: v for k, v in p.items() if v is not None})
        init = {"pos": list(pos), "scale": scale, "opacity": opacity, **({"rot": rot} if rot is not None else {})}
        S.set(id, **init, **{k: v for k, v in tracks.items() if v is not None})
        return id

    def shape(self, id, pos, kind="round", w=200, h=None, z=10, parent=None, scale=1, opacity=1, rot=None, draw=None,
              **p):
        """Forme : rect, round, circle, ellipse ou poly (pts) ; fill, stroke, sw, shadow, dash, r. draw=0 : contour à
        tracer (kit.draw)."""
        return self._add(id, "shape", pos, z, parent, scale, opacity, rot, {"draw": draw}, kind=kind, w=w, h=h, **p)

    def text(self, id, pos, text, size=40, weight=700, z=10, parent=None, scale=1, opacity=1, rot=None, typed=False,
             **p):
        """Texte (une ou plusieurs lignes « \\n ») ; `w` mesuré (surligneur `mark`, soulignement `under`). typed=True :
        caché jusqu'à kit.type."""
        w = round(max(text_width(t, size, weight) for t in text.split("\n")), 1) if weight in (600, 700, 800) else None
        return self._add(id, "text", pos, z, parent, scale, opacity, rot, {"chars": 0 if typed else None}, text=text,
                         size=size, weight=weight, w=p.pop("w", w), **p)

    def icon(self, id, pos, name, z=10, parent=None, scale=1, opacity=1, rot=None, **p):
        """Pictogramme (s, color, sw), sur un disque si `disc` (rayon ; fill, ringColor ; piste ring)."""
        return self._add(id, "icon", pos, z, parent, scale, opacity, rot, {}, name=name, **p)

    def sector(self, id, pos, start=0, value=0, z=10, parent=None, scale=1, opacity=1, **p):
        """Cadran et secteur de temps (r, unit, face, fill…) : pistes start et value (en unités du cadran)."""
        return self._add(id, "sector", pos, z, parent, scale, opacity, None, {"start": start, "value": value}, **p)

    def gauge(self, id, pos, value=1, w=600, h=48, z=10, parent=None, scale=1, opacity=1, **p):
        """Jauge (dir, fill, empty, segments, marks) : piste value 0 -> 1, fill (hex pour un fondu)."""
        return self._add(id, "gauge", pos, z, parent, scale, opacity, None, {"value": value}, w=w, h=h, **p)

    def counter(self, id, pos, value=0, size=96, z=10, parent=None, scale=1, opacity=1, **p):
        """Compteur en typographie française (decimals, prefix, suffix " €" : l'espace devient insécable, sign) :
        piste value."""
        return self._add(id, "counter", pos, z, parent, scale, opacity, None, {"value": value}, size=size, **p)

    def curve(self, id, pos, pts, draw=0, z=10, parent=None, scale=1, opacity=1, **p):
        """Courbe (pts locaux, smooth, area, axes, dot, dash) : piste draw 0 -> 1."""
        return self._add(id, "curve", pos, z, parent, scale, opacity, None, {"draw": draw}, pts=[list(q) for q in pts],
                         **p)

    def seesaw(self, id, pos, rot=0, z=10, parent=None, scale=1, opacity=1, **p):
        """Bascule (w, h, baseW, baseH, ground) : piste rot (> 0 : le côté droit descend). Objets posés : enfants,
        pos = kit.seat(id, x, hauteur de l'objet)."""
        return self._add(id, "seesaw", pos, z, parent, scale, opacity, rot, {}, **p)

    def seat(self, seesaw_id, x, obj_h):
        """Position locale d'un objet de hauteur obj_h posé à x sur la planche d'une bascule."""
        return [x, -self.S.ents[seesaw_id]["p"].get("h", 24) - obj_h / 2]

    def cursor(self, id, pos, z=30, parent=None, scale=1, opacity=1, **p):
        """Pointeur (origine = pointe) : pistes press et ring (kit.click)."""
        return self._add(id, "cursor", pos, z, parent, scale, opacity, None, {"press": 0, "ring": 0}, **p)

    def click(self, id, f):
        """Clic du pointeur : s'enfonce en 3 images, remonte en 4 ; deux ondes partent de la pointe (18 images)."""
        S = self.S
        S.key(id, "press", f, 1, 3, "out")
        S.key(id, "press", f + 3, 0, 4, "inOut")
        S.key(id, "ring", f - 1, 0)
        S.key(id, "ring", f, 1, 18, "out")
        return f + 7

    def endcard(self, id, pos, title=None, text=None, labels=None, z=40, parent=None, scale=1, opacity=1, btn=1,
                **p):
        """Carte de fin (titre, lignes, bouton pilule `text`) : pistes w, h, btn, press, title. Voir kit.outro."""
        return self._add(id, "endcard", pos, z, parent, scale, opacity, None, {"btn": btn, "press": 0, "title": 1},
                         title=title, text=text, labels=list(labels) if labels else None, **p)

    def crowd(self, id, pos, n=6, show=None, link=None, z=10, parent=None, scale=1, opacity=1, **p):
        """Foule de n figurines (layout ring/row, pts, h, tone, link) : pistes show (0 -> n), link (0 -> 1), tone.
        crowd_points(p) donne leurs positions locales."""
        return self._add(id, "crowd", pos, z, parent, scale, opacity, None, {"show": show, "link": link}, n=n, **p)

    def tick(self, id, pos, color, size=None, sw=8, variant=None, z=11, parent=None, draw=0, **p):
        """Coche (draw 0 -> 1) : pleine (conseiller), ou variant='ai' (pointillés dans un carré tireté)."""
        return self._add(id, "tick", pos, z, parent, 1, 1, None, {"draw": draw}, color=color, sw=sw,
                         size=size if size is not None else GEOM["TICK"]["size"], variant=variant, **p)

    def stamp(self, id, pos, text, w, h, size=40, sub=None, sub_on=None, rot=None, z=11.8, parent=None, scale=1,
              opacity=1, handle=None, **p):
        """Tampon (double cadre deep, sans fond) : `text` ExtraBold espacé ; facultatif `sub`, seconde ligne précédée
        d'un « ? » cerclé (GEOM.STAMP_SUB ; largeur mesurée -> subW ; cadre h >= 84). Pistes handle (poignée,
        Figure.stamp), lite, subOn (opacité de la seconde ligne, défaut 1 : sub_on=0 pour la faire paraître au
        contact, S.key(id, "subOn", hit, 1, 3) avec hit = Figure.stamp(...)). Déclarer seulement : le coup se joue
        par Figure.stamp."""
        Q = GEOM["STAMP_SUB"]
        inner = w - 2 * 18                      # double cadre : 9 px de marge + respiration
        need = text_width(text, size, 800) + 3 * (len(text) - 1)
        if need > inner:
            raise SystemExit(f"{id} : « {text} » trop large pour le tampon ({need:.0f} px > {inner} px) : élargis w")
        extra = {}
        if sub is not None:
            sub_w = round(text_width(sub, Q["size"], 600), 1)
            line2 = 2 * Q["qR"] + Q["qSw"] + Q["gap"] + sub_w
            if line2 > inner or h < 84:
                raise SystemExit(f"{id} : seconde ligne « {sub} » : il faut w >= {line2 + 36:.0f} et h >= 84")
            extra = {"sub": sub, "subW": sub_w}
        tracks = {"handle": handle, "subOn": sub_on if sub is not None else None}
        return self._add(id, "stamp", pos, z, parent, scale, opacity, rot, tracks, text=text, w=w, h=h, size=size,
                         **extra, **p)

    # --- éléments de la série ---
    def steps_marker(self, labels=None, n=None, id="marqueur", y=300, cx=540, gap=None, active=0, z=20):
        """Repère d'étapes 1-2-3 (marker), avec sa légende `labels` sous les disques ; écart >= 150 px avec légende
        (mesuré sur le libellé le plus long). Disques en repère local centré, entité posée en [cx, y] : elle se réduit
        vers son centre (vanish, morph). Changer d'étape : kit.step. Renvoie l'id."""
        n = n or len(labels)
        M = GEOM["MARKER"]
        if gap is None:
            gap = max(150, round(max(text_width(t, M["labelSize"], 700) for t in labels) + 28)) if labels else 100
        xs = [round((i - (n - 1) / 2) * gap, 1) for i in range(n)]
        self.S.add(id, "marker", z=z, xs=xs, y=0, **({"labels": list(labels)} if labels else {}))
        self.S.set(id, pos=[cx, y], active=active)
        return id

    def step(self, f, k, id="marqueur", d=MOVE):
        """Le disque actif glisse sur l'étape k (0 = « 1 ») en 550 ms."""
        self.S.key(id, "active", f, k, d, "inOut")
        return f + d

    def outro(self, scene, mot=None, outs=(), press=16, title="WealthTech Horizon", labels=("Comprendre ton argent",),
              text="S’abonner", icon=None, pos=(540, 760), w=620, h=520, id="fin", z=40, clear=None, card_at=None,
              btn_at=None, **card):
        """Fin standard des 15 films, sur le temps fort (scène, mot ; défaut : le 1er de la scène) : les `outs` se
        réduisent pendant que la carte de fin grandit (morph 350 ms) ; titre et lignes en fondu, le bouton surgit ;
        le pointeur entre en bas à droite, glisse sur le bas du bouton (jamais sur le libellé) et l'enfonce `press`
        images après la carte (ou sur le mot `press` de la scène) ; puis tout reste immobile jusqu'à la fin.
        clear="fade" (facultatif ; défaut inchangé) : les `outs` s'effacent en opacité sur FADE images, sans se
        réduire en éclats ni en points, pendant que la carte grandit.
        card_at (facultatif ; défaut inchangé) : la carte ne grandit pas depuis 0, elle paraît d'un coup à pleine
        taille à l'image f + card_at : c'est le relais d'une entité de la composition que la mise en scène a amenée
        exactement à sa place (la fiche du film) ; titre et lignes entrent à f + card_at + 4.
        btn_at (facultatif) : le bouton paraît d'un coup (btn 1) à f + btn_at, relais d'une pilule amenée à sa place
        (la pastille du fil), au lieu de surgir à f + 6.
        **card (facultatif) : paramètres de plus de la carte (labelSize, bsize…), passés tels quels à endcard.
        -> {"card": image, "press": image du clic}."""
        S = self.S
        sc = next((s for s in S.sb["scenes"] if s["id"] == scene), None)
        if sc is None:
            raise SystemExit(f"outro : scène {scene} absente du storyboard")
        f = self.at(scene, mot or sc["beats"][0]["mot"], "fin : la carte de fin remplace la composition, bouton S’abonner")
        fp = self.at(scene, press, "fin : le pointeur enfonce le bouton") if isinstance(press, str) else f + press
        self.endcard(id, pos, title=title, text=text, labels=labels, icon=icon, w=w, h=h, z=z, scale=0, btn=0, **card)
        S.set(id, title=0)
        t0 = f
        if clear == "fade":
            for o in outs:
                S.key(o, "opacity", f, 0, FADE, "linear")
                S.key(o, "scale", f + FADE, 0)
            if card_at is None:
                self.pop(id, f, d=MORPH)
        elif card_at is None:
            self.morph(list(outs), [id], f, pair=False)
        elif outs:
            self.morph(list(outs), [], f, pair=False)
        if card_at is not None:                                  # relais : la carte paraît à pleine taille
            t0 = f + card_at
            S.key(id, "scale", t0, 1)
        S.key(id, "title", t0 + 4, 1, FADE, "out")
        if btn_at is not None:
            S.key(id, "btn", f + btn_at, 1)
        else:
            S.key(id, "btn", f + 6, 1, POP, "out")
        bw, bh = 380, 112
        by = pos[1] + h / 2 - bh / 2 - 56
        aim = [pos[0] + bw / 2 - 46, by + bh / 2 - 20]          # bas droit du bouton, hors du libellé
        cur = f"{id}_curseur"
        self.cursor(cur, [aim[0] + 150, aim[1] + 120], z=z + 1, scale=0)
        glide = max(6, min(12, fp - f - 10))
        self.pop(cur, fp - glide - 6, d=6)
        self.move(cur, fp - glide, aim, d=glide, e="inOut")
        self.click(cur, fp)
        S.key(id, "press", fp, 1, 2, "out")
        S.key(id, "press", fp + 5, 0, 4, "out")
        return {"card": f, "press": fp, "id": id, "cursor": cur}


def outro(S, scene, **kw):
    """Fin standard (carte, bouton « S’abonner », pointeur) : Kit(S).outro(scene, **kw)."""
    return Kit(S).outro(scene, **kw)


def steps_marker(S, labels, **kw):
    """Repère d'étapes avec légende : Kit(S).steps_marker(labels, **kw)."""
    return Kit(S).steps_marker(labels, **kw)


# ---------- figurine articulée ----------

class Figure:
    """Figurine (encre : « toi » / papier : le client) avec son bras et son stylo. Le bras est une chaîne à 2 os de
    longueurs FIXES (GEOM.FIGURE.arm, à l'échelle de la figurine) : coude (piste elbow du limb, bend = 1) et prise du
    stylo sont posés image par image. Le stylo prolonge la droite épaule -> pointe (comme V01) ; trop près de l'épaule,
    le poignet plie. Cible hors d'atteinte : la figurine fait un pas (reach, tap, stamp).

    La figurine, son bras et son stylo ne bougent QUE par ces méthodes (une clé posée à la main décroche le bras).
    side='left' : bras du côté gauche de l'écran (V01, la figurine se tourne vers la gauche) ; 'right' : miroir.
    Repère : pos = centre de la figurine (haut de la tête à -96, pied à +95 x échelle)."""

    def __init__(self, kit, id, pos, scale=1.0, variant="ink", side="left", tool=True, z=15, show=True):
        S, G = kit.S, GEOM["FIGURE"]
        self.kit, self.S, self.id, self.size = kit, S, id, scale
        m = -1 if side == "left" else 1
        self.m, self.bend = m, (1 if side == "left" else -1)
        self.shoulder = [abs(G["shoulder"][0]) * m, G["shoulder"][1]]
        self.hand = [abs(G["hand"][0]) * m, G["hand"][1]]
        self.pivot = list(G["pivot"])
        self.l1, self.l2 = G["arm"]["upper"], G["arm"]["fore"]
        self.rest_up = REST_UP if side == "left" else (180 - REST_UP) % 360
        S.add(id, "figure", z=z, variant=variant)
        S.set(id, pos=list(pos), scale=scale if show else 0, lean=0)
        self.arm = self.pen = None
        if tool:
            self.arm, self.pen, self.pen_len = f"{id}_bras", f"{id}_stylo", GEOM["PEN"]["len"]
            S.add(self.arm, "limb", z=z + 0.5, a={"id": id, "at": self.shoulder}, b={"id": self.pen, "at": [0, 0]},
                  sw=G["arm"]["sw"], pivot=self.pivot, pivotTrack="lean")
            S.add(self.pen, "pen", z=z + 1, len=self.pen_len)
            grip = self._rest_grip(0)
            elbow = solve_ik(self._shoulder(0), grip, self.l1 * self._scale(0), self.l2 * self._scale(0), self.bend)[0]
            S.set(self.pen, pos=r3(grip), rot=self.rest_up, scale=scale if show else 0, opacity=1)
            S.set(self.arm, opacity=1 if show else 0, bend=1, elbow=r3(elbow))

    # --- repères ---
    def _scale(self, n):
        return self.S.world_scale(self.id, n)

    def _body_pt(self, pt, n):
        lean = self.S.val(self.id, "lean", n, 0)
        return self.S.to_world(self.id, rotate_about(pt, lean, self.pivot) if lean else pt, n)

    def _shoulder(self, n):
        """Épaule monde à l'image n, calculée comme entities.tsx Limb (penché autour du pied)."""
        return self._body_pt(self.shoulder, n)

    def _rest_grip(self, n):
        return self._body_pt(self.hand, n)

    def _rest_rot(self, n):
        return self.rest_up + self.S.val(self.id, "lean", n, 0)

    def tip(self, n):
        """Pointe du stylo (monde) à l'image n."""
        g, rot = self.S.val(self.pen, "pos", n), math.radians(self.S.val(self.pen, "rot", n))
        L = self.pen_len * self.S.val(self.pen, "scale", n)
        return [g[0] + L * math.cos(rot), g[1] + L * math.sin(rot)]

    def reach_max(self, n, pen=True):
        s = self._scale(n)
        return (self.l1 + self.l2) * s + (self.pen_len * s if pen and self.pen else 0)

    def place_for(self, targets, n, pen=True, margin=REACH):
        """Position du corps (même y) la plus proche de l'actuelle d'où tous les `targets` (points monde) sont à
        portée confortable (`margin` x allonge) : à donner à walk avant une relecture ou un tampon."""
        pos, s = self.S.val(self.id, "pos", n), self._scale(n)
        R = margin * self.reach_max(n, pen)
        sh = [self.shoulder[0] * s, self.shoulder[1] * s]
        lo, hi = -math.inf, math.inf
        for t in targets:
            dy = t[1] - (pos[1] + sh[1])
            if abs(dy) > R:
                raise SystemExit(f"{self.id} : cible {r3(t)} à {abs(dy):.0f} px au-dessus ou en dessous de l'épaule, "
                                 f"hors d'atteinte ({R:.0f} px) : rapproche la figurine en hauteur")
            w = math.sqrt(R * R - dy * dy)
            lo, hi = max(lo, t[0] - w - sh[0]), min(hi, t[0] + w - sh[0])
        if lo > hi:
            raise SystemExit(f"{self.id} : cibles trop écartées pour un seul emplacement ({len(targets)} points)")
        return [round(min(max(pos[0], lo), hi), 2), pos[1]]

    def _need_tool(self, what):
        if not self.pen:
            raise SystemExit(f"{self.id}.{what} : figurine sans bras ni stylo (tool=False)")

    # --- pose image par image ---
    def _pose(self, n, grip, rot=None, pen_scale=None):
        """Image n : prise du stylo en `grip` (monde), coude par IK à longueurs fixes."""
        A, s = self._shoulder(n), self._scale(n)
        elbow, hand, ok = solve_ik(A, grip, self.l1 * s, self.l2 * s, self.bend)
        if not ok and s > 0.05 and math.dist(hand, grip) > 1:
            self.kit.warn(f"{self.id} image {n} : prise hors d'atteinte de {math.dist(hand, grip):.0f} px "
                          f"(la figurine doit s'approcher : walk / place_for)")
        S = self.S
        S.key(self.pen, "pos", n, r3(hand), 1, "linear")
        if rot is not None:
            S.key(self.pen, "rot", n, round(rot, 3), 1, "linear")
        if pen_scale is not None:
            S.key(self.pen, "scale", n, round(pen_scale, 5), 1, "linear")
        S.key(self.arm, "elbow", n, r3(elbow), 1, "linear")

    def _tip_pose(self, A, T, s, strict=True):
        """(prise, angle) du stylo dont la pointe est en T : stylo dans le prolongement épaule -> pointe ; plus près
        que (stylo + WRIST x bras), la prise reste à WRIST x bras de l'épaule et le poignet plie (prise du côté bas)."""
        L, r_lo = self.pen_len * s, WRIST * (self.l1 + self.l2) * s
        D = math.dist(A, T)
        if D < 1e-6 or (D < L - r_lo + 1 and not strict):
            u = [math.cos(math.radians(self.rest_up)), math.sin(math.radians(self.rest_up))] if D < 1e-6 else \
                [(T[0] - A[0]) / D, (T[1] - A[1]) / D]
            T, D = [A[0] + u[0] * (L - r_lo + 1), A[1] + u[1] * (L - r_lo + 1)], L - r_lo + 1
        u = [(T[0] - A[0]) / D, (T[1] - A[1]) / D]
        if D >= L + r_lo:
            return [T[0] - L * u[0], T[1] - L * u[1]], math.degrees(math.atan2(u[1], u[0])) % 360
        if D < L - r_lo - 1e-6:
            raise SystemExit(f"{self.id} : cible à {D:.0f} px de l'épaule, trop près pour le stylo "
                             f"(minimum {L - r_lo:.0f} px) : éloigne la figurine (walk)")
        a = (r_lo * r_lo - L * L + D * D) / (2 * D)
        h = math.sqrt(max(0.0, r_lo * r_lo - a * a))
        cands = [[A[0] + u[0] * a + sg * -u[1] * h, A[1] + u[1] * a + sg * u[0] * h] for sg in (1, -1)]
        G = max(cands, key=lambda g: g[1] + 0.3 * g[0] * self.m)     # prise en bas, du côté du bras
        return G, math.degrees(math.atan2(T[1] - G[1], T[0] - G[0])) % 360

    def _start(self, f):
        """Pose à f - 1, relative à l'épaule (suit le corps s'il bouge)."""
        A = self._shoulder(f - 1)
        g = self.S.val(self.pen, "pos", f - 1)
        return [g[0] - A[0], g[1] - A[1]], self.S.val(self.pen, "rot", f - 1)

    def _tip_line(self, f, d, a, b, e):
        for n, p in frames(f, d, e):
            G, rot = self._tip_pose(self._shoulder(n), lerp(a, b, p), self._scale(n))
            self._pose(n, G, rot)

    def _move_body(self, f, d, to, e="inOut", hop=HOP, lean=WALK_LEAN):
        """Le corps glisse vers `to` en d images, à petits sauts, penché vers l'avant (clés image par image)."""
        S = self.S
        p0 = S.val(self.id, "pos", f - 1)
        hops = max(1, round(d / HOP_PERIOD))
        for k, (n, p) in enumerate(frames(f, d, e)):
            bob = -hop * abs(math.sin(math.pi * hops * (k + 1) / d)) if k < d - 1 else 0
            S.key(self.id, "pos", n, r3([lerp(p0[0], to[0], p), lerp(p0[1], to[1], p) + bob]), 1, "linear")
        side = (to[0] > p0[0]) - (to[0] < p0[0])
        if lean and side:
            t = min(6, max(1, d // 2))
            S.key(self.id, "lean", f, lean * side, t, "out")
            S.key(self.id, "lean", f + d - t, 0, t, "inOut")

    def _step_for(self, targets, f, d, e, pen=True, margin=REACH):
        """Pas vers les cibles si elles sont hors d'atteinte confortable : le corps bouge pendant [f, f + d)."""
        x0 = self.S.val(self.id, "pos", f - 1)
        goal = self.place_for(targets, f - 1, pen, margin)
        dx = goal[0] - x0[0]
        if abs(dx) <= 0.5:
            return False
        if abs(dx) / d > 10:
            self.kit.warn(f"{self.id} image {f} : pas automatique de {abs(dx):.0f} px en {d} images (saccadé) : "
                          f"place la figurine avant, walk(f, place_for([...]))")
        self._move_body(f, d, goal, e, hop=HOP if d >= 8 else 0)
        return True

    def _hand_rest(self, f, d, e="inOut"):
        rel0, r0 = self._start(f)
        for n, p in frames(f, d, e):
            A, R = self._shoulder(n), self._rest_grip(n)
            self._pose(n, lerp([A[0] + rel0[0], A[1] + rel0[1]], R, p), ang_lerp(r0, self._rest_rot(n), p))

    # --- actions ---
    def enter(self, f, at=None, frm=None, d=None, arm_from=2):
        """Entrée : pop sur place (`at`, ou sa position) en 300 ms, bras et stylo avec elle ; frm=x : arrive en
        marchant depuis x (même y ; attention à la zone x > 940 réservée). arm_from (facultatif) : image, après f, où
        le bras paraît (2 par défaut, en 3 images ; 0 : entier dès f, avec le corps). Renvoie f + d."""
        S = self.S
        at = list(at) if at is not None else S.val(self.id, "pos", f - 1)
        if S.val(self.id, "opacity", f - 1) < 1:                 # après une sortie (exit)
            S.key(self.id, "opacity", f - 1, 1)
        if frm is not None:
            S.key(self.id, "pos", f - 1, r3([frm, at[1]]))
            S.key(self.id, "scale", f - 1, self.size)
            if self.pen:
                S.key(self.arm, "opacity", f - 1, 1)
                S.key(self.pen, "scale", f - 1, self.size)
                self._pose(f - 1, self._rest_grip(f - 1), self._rest_rot(f - 1))
            return self.walk(f, at, d)
        d = d or POP
        S.key(self.id, "pos", f - 1, r3(at))
        for n, p in frames(f, d, "out"):
            S.key(self.id, "scale", n, round(p * self.size, 5), 1, "linear")
            if self.pen:
                self._pose(n, self._rest_grip(n), self._rest_rot(n), pen_scale=p * self.size)
        if self.pen:
            S.key(self.arm, "opacity", f + arm_from, 1, 3 if arm_from else 0, "out")
        return f + d

    def exit(self, f, d=POP):
        """Sortie : se réduit vers son centre (bras et stylo avec elle, la main rejoint le repos). Renvoie f + d."""
        S = self.S
        s0 = S.val(self.id, "scale", f - 1)
        if self.pen:
            S.key(self.arm, "opacity", f, 0, 2, "linear")
            rel0, r0 = self._start(f)
        for n, p in frames(f, d, "out"):
            S.key(self.id, "scale", n, round(s0 * (1 - p), 5), 1, "linear")
            if self.pen:
                A, k = self._shoulder(n), 1 - p
                self._pose(n, lerp([A[0] + rel0[0] * k, A[1] + rel0[1] * k], self._rest_grip(n), p),
                           ang_lerp(r0, self._rest_rot(n), p), pen_scale=s0 * k)
        S.key(self.id, "opacity", f + d, 0)
        return f + d

    def walk(self, f, to, d=None, e="inOut"):
        """Marche vers `to` (x, ou [x, y]) : glisse à petits sauts, penchée vers l'avant ; la main revient au repos et
        suit le corps. d par défaut : distance / 7 px par image (8 images au moins). Renvoie f + d."""
        p0 = self.S.val(self.id, "pos", f - 1)
        to = [to, p0[1]] if isinstance(to, (int, float)) else list(to)
        if math.dist(p0, to) < 0.5:
            return f
        d = d or max(8, math.ceil(math.dist(p0, to) / WALK_SPEED))
        self._move_body(f, d, to, e)
        if self.pen:
            k0 = min(6, d)
            self._hand_rest(f, k0, "out")
            for n in range(f + k0, f + d):
                self._pose(n, self._rest_grip(n), self._rest_rot(n))
        return f + d

    def reach(self, f, target, d=MOVE, e="inOut", step=True):
        """La pointe du stylo va sur `target` (point monde) en d images ; hors d'atteinte, la figurine fait un pas
        pendant le geste (step=False : avertissement, la pointe s'arrête avant). Renvoie f + d."""
        self._need_tool("reach")
        if step:
            self._step_for([target], f, d, e)
        rel0, r0 = self._start(f)
        t0 = self.tip(f - 1)
        for n, p in frames(f, d, e):
            A, s = self._shoulder(n), self._scale(n)
            G, rot = self._tip_pose(A, lerp(t0, target, p), s, strict=p >= 1)
            self._pose(n, lerp([A[0] + rel0[0], A[1] + rel0[1]], G, p), ang_lerp(r0, rot, p))
        return f + d

    def tap(self, f, target, d=TAP, lift=14):
        """Tapotement : approche au-dessus de `target`, coup (3 images), relève de `lift` px. Renvoie l'IMAGE DU
        CONTACT (f + d - 1) : y caler l'événement qu'il déclenche (coche, fente, « ? »)."""
        self._need_tool("tap")
        A = self._shoulder(f - 1)
        u = [target[0] - A[0], target[1] - A[1]]
        k = lift * self._scale(f - 1) / max(1e-6, math.hypot(*u))
        hover = [target[0] - u[0] * k, target[1] - u[1] * k]
        self.reach(f, hover, d - 3)
        self._tip_line(f + d - 3, 3, hover, target, "in")
        impact = f + d - 1
        self._tip_line(impact + 1, 5, target, hover, "out")
        return impact

    def _approach(self, f, pts, lead, speed, step):
        """Avant un tracé : la pointe va sur pts[0] en `lead` images, et la figurine fait un pas pendant ce temps si
        un des points est hors d'atteinte. Renvoie l'image où commence le tracé."""
        t0, x0 = self.tip(f - 1), self.S.val(self.id, "pos", f - 1)[0]
        need = step and abs(self.place_for(pts, f - 1)[0] - x0) > 0.5
        if math.dist(t0, pts[0]) <= 1 and not need:
            return f
        lead = lead or max(4, math.ceil(math.dist(t0, pts[0]) / (2 * speed)))
        if need:
            lead = max(lead, STEP)
            self._step_for(pts, f, lead, "inOut")
        return self.reach(f, pts[0], lead, step=False)

    def trace(self, f, pts, speed=TRACE_SPEED, d=None, e="linear", lead=None, step=True):
        """La pointe parcourt la polyligne `pts` (points monde) à vitesse constante (« relis ») ; si elle n'est pas
        sur pts[0] (ou si la figurine doit d'abord faire un pas), elle y va en `lead` images. Renvoie l'image où la
        pointe atteint chaque point de pts (événements sous la pointe : coche, étiquette qui s'allume)."""
        self._need_tool("trace")
        pts = [list(q) for q in pts]
        f = self._approach(f, pts, lead, speed, step)
        acc = [0.0]
        for a, b in zip(pts, pts[1:]):
            acc.append(acc[-1] + math.dist(a, b))
        L = acc[-1]
        d = d or max(1, math.ceil(L / speed))
        hits = [None] * len(pts)
        hits[0] = f - 1
        for n, p in frames(f, d, e):
            target = p * L
            i = next((j for j in range(1, len(acc)) if acc[j] >= target - 1e-9), len(acc) - 1)
            t = (target - acc[i - 1]) / max(1e-9, acc[i] - acc[i - 1]) if L else 1
            for j in range(1, len(pts)):
                if hits[j] is None and target >= acc[j] - 1e-6:
                    hits[j] = n
            G, rot = self._tip_pose(self._shoulder(n), lerp(pts[i - 1], pts[i], t) if L else pts[0], self._scale(n))
            self._pose(n, G, rot)
        return hits

    def strike(self, f, a, b, d=6, lead=3, line=None, track="strike", step=True):
        """Barre de a à b (points monde) : la pointe va sur a (`lead` images ; 8 au moins si la figurine doit faire
        un pas), puis file jusqu'à b en d images ; la piste `track` de `line` (ligne de fiche : strike) va de 0 à 1
        dans les mêmes images. Renvoie l'image qui suit le trait."""
        self._need_tool("strike")
        g = self._approach(f, [list(a), list(b)], lead, TRACE_SPEED, step)
        self._tip_line(g, d, a, b, "inOut")
        if line:
            self.kit.ensure(line, track, 0)
            self.S.key(line, track, g, 1, d, "inOut")
        return g + d

    def stamp(self, f, stamp_id, d=6, shake=None, step=True):
        """Coup de tampon : l'entité stamp (poignée : piste handle) apparaît dans la main à 1,4 et s'abat à 1 en d
        images ; la main tient la poignée (stylo caché), la figurine plonge de 6 px ; `shake` (id, ex. la fiche)
        secoue au contact ; la poignée s'efface, la main revient au repos et le stylo y réapparaît (pop) 10 images
        après le contact. Hors d'atteinte : un pas de 8 images AVANT f (la main y revient au repos). Renvoie l'image
        du contact (f + d - 1)."""
        self._need_tool("stamp")
        S, H = self.S, GEOM["STAMP_HANDLE"]
        grip_local = [0, -(S.ents[stamp_id]["p"]["h"] / 2 + H["neck"] + H["knobH"] / 2)]
        hit = f + d - 1
        self.kit.ensure(stamp_id, "handle", 1)
        S.key(stamp_id, "opacity", f - 1, 0)
        S.key(stamp_id, "scale", f - 1, 1.4)
        S.key(stamp_id, "opacity", f, 1)
        S.key(stamp_id, "scale", f, 1.0, d, "out")
        if step and self._step_for([S.to_world(stamp_id, grip_local, hit)], f - STEP, STEP, "inOut", pen=False,
                                   margin=REACH_STAMP):
            self._hand_rest(f - STEP, STEP, "inOut")
        if shake:
            self.kit.shake(shake, hit + 1, amp=4, axis="xy")
        pos = S.val(self.id, "pos", hit - 1)
        S.key(self.id, "pos", hit, r3([pos[0], pos[1] + 6]), 3, "out")
        S.key(self.id, "pos", hit + 3, r3(pos), 4, "inOut")
        for t, v, dd, ee in ((hit, 6, 3, "out"), (hit + 3, -2, 3, "inOut"), (hit + 6, 0, 3, "inOut")):
            S.key(self.id, "lean", t, v * self.m, dd, ee)
        S.key(self.pen, "opacity", f, 0)
        for n in range(f, hit + 4):
            self._pose(n, S.to_world(stamp_id, grip_local, n), self._rest_rot(n))
        S.key(stamp_id, "handle", hit + 3, 0, 3, "linear")
        self._hand_rest(hit + 4, 6, "inOut")
        back = hit + 10                                  # le stylo revient dans la main au repos (pop), jamais au-dessus
        S.key(self.pen, "scale", back - 1, 0)            # de la fiche pendant que le bras se retire
        S.key(self.pen, "opacity", back, 1)
        S.key(self.pen, "scale", back, round(self._scale(back), 5), 5, "out")
        return hit

    def rest(self, f, d=8, e="inOut"):
        """La main revient au repos (stylo levé contre le corps). Renvoie f + d."""
        self._need_tool("rest")
        self._hand_rest(f, d, e)
        return f + d

    # --- gestes facultatifs (ajoutés pour V01 ; aucune méthode existante ne change) ---
    def _follow_rest(self, fa, fb):
        """Images [fa, fb) : la main reste au repos et suit le corps (bras re-posé image par image)."""
        if self.pen:
            for n in range(fa, fb):
                self._pose(n, self._rest_grip(n), self._rest_rot(n))

    def hop(self, f, to, d, h=0, lean=WALK_LEAN):
        """Un seul bond vers `to` ([x, y]) en d images, de `h` px de haut ; lean < 0 : penchée en arrière (recul).
        La main revient au repos puis suit le corps. Renvoie f + d."""
        self._move_body(f, d, list(to), "inOut", hop=h, lean=lean)
        if self.pen:
            k0 = min(6, d)
            self._hand_rest(f, k0, "out")
            self._follow_rest(f + k0, f + d)
        return f + d

    def run(self, f, pts, d):
        """Course à vitesse constante le long de la polyligne `pts` (points monde) en d images, main au repos.
        Renvoie f + d."""
        acc = [0.0]
        for a, b in zip(pts, pts[1:]):
            acc.append(acc[-1] + math.dist(a, b))
        L = acc[-1]
        for n, p in frames(f, d, "linear"):
            s = p * L
            i = next((j for j in range(1, len(acc)) if acc[j] >= s - 1e-9), len(acc) - 1)
            t = (s - acc[i - 1]) / max(1e-9, acc[i] - acc[i - 1])
            self.S.key(self.id, "pos", n, r3(lerp(pts[i - 1], pts[i], t)), 1, "linear")
            if self.pen:
                self._pose(n, self._rest_grip(n), self._rest_rot(n))
        return f + d

    def rim(self, f, on, d=3):
        """Liseré papier du bras (piste `rim` du limb, facultative) : on=True le montre en d images (bras tendu qui
        croise le buste encre), on=False l'efface en d images, AVANT que le bras ne se replie contre le buste.
        Renvoie f + d."""
        self._need_tool("rim")
        self.kit.ensure(self.arm, "rim", 0)
        self.S.key(self.arm, "rim", f, 1 if on else 0, d, "out" if on else "linear")
        return f + d

    def lean_to(self, f, deg, d=POP, e="out"):
        """Incline la figurine de `deg`° autour du pied en d images (signe : celui de la piste lean) ; la main au repos
        suit. Renvoie f + d."""
        self.kit.ensure(self.id, "lean", 0)
        self.S.key(self.id, "lean", f, deg, d, e)
        self._follow_rest(f, f + d)
        return f + d

    def scale_to(self, f, s, d=10, e="inOut"):
        """Change d'échelle (s) en d images, autour de son centre ; le bras et le stylo suivent, main au repos. La
        taille d'entrée (`enter`) devient s. Renvoie f + d."""
        S = self.S
        s0 = S.val(self.id, "scale", f - 1)
        pen_on = self.pen and S.val(self.pen, "opacity", f - 1) > 0.5 and S.val(self.pen, "scale", f - 1) > 1e-6
        for n, p in frames(f, d, e):
            S.key(self.id, "scale", n, round(lerp(s0, s, p), 5), 1, "linear")
            if self.pen:
                self._pose(n, self._rest_grip(n), self._rest_rot(n),
                           pen_scale=lerp(s0, s, p) if pen_on else None)
        self.size = s
        return f + d

    def stow(self, f, d=4):
        """Range le stylo : il se réduit dans la main en d images, puis disparaît. Renvoie f + d."""
        self._need_tool("stow")
        self.S.key(self.pen, "scale", f, 0, d, "in")
        self.S.key(self.pen, "opacity", f + d, 0)
        return f + d

    def unstow(self, f, d=6):
        """Le stylo revient dans la main (pop, à l'échelle de la figurine). Renvoie f + d."""
        self._need_tool("unstow")
        self.S.key(self.pen, "scale", f - 1, 0)
        self.S.key(self.pen, "opacity", f, 1)
        self.S.key(self.pen, "scale", f, round(self._scale(f + d), 5), d, "out")
        return f + d

    def set_z(self, f, z, tool_z=None):
        """Change de calque à l'image f : la figurine passe en z ; avec `tool_z`, le bras passe en tool_z et le stylo
        en tool_z + 0,5 (sinon ils gardent le leur). Renvoie f."""
        S = self.S
        for id, v in ((self.id, z),) + (((self.arm, tool_z), (self.pen, tool_z + 0.5)) if tool_z is not None and
                                         self.pen else ()):
            self.kit.ensure(id, "z", S.ents[id]["z"])
            S.key(id, "z", f, v)
        return f


# ---------- fiche ----------

class Sheet:
    """Mise en page d'une fiche (brief, checklist) : rangées, ligne de texte et ligne de la date de chaque rangée,
    colonnes (puce, clé, valeur, coche, capsule), comme la fiche de V01 (Sheet(5) = ses ROWS, TY, VALUE_X…).
    Coordonnées locales de la fiche (origine au centre) ; world() les passe en monde."""

    def __init__(self, n=5, w=500, h=None, head=84, pitch=104, top=52, ty=-22, ly=23, slot_h=92, strip=48):
        self.n, self.w, self.head, self.ty, self.ly = n, w, head, ty, ly
        self.slot_h, self.strip = slot_h, strip
        self.h = h if h is not None else head + top + pitch * (n - 1) + slot_h / 2 + 122
        self.rows = [-self.h / 2 + head + top + pitch * i for i in range(n)]
        self.x = {"bullet": -w / 2 + 2, "text": -w / 2 + 44, "value": w / 2 - 100, "tick": w / 2 - 50,
                  "slot0": -w / 2 + 18, "slot1": w / 2 - 78}
        self.id, self.lines = None, []

    def pt(self, i, col="value", line="text"):
        """Point local : colonne `col` (bullet, text, value, tick, slot0, slot1 ou un x) de la rangée i, sur sa ligne
        de texte (`line`='text'), de date ('date') ou au centre de la rangée ('row')."""
        x = self.x[col] if isinstance(col, str) else col
        return [x, self.rows[i] + {"text": self.ty, "date": self.ly, "row": 0}[line]]

    def world(self, S, i, col="value", line="text", n=0):
        return S.to_world(self.id, self.pt(i, col, line), n)

    def value_span(self, i, pad=8):
        """Extrémités locales (droite, gauche) de la valeur de la rangée i, débordées de `pad` px : le trait qui barre."""
        p = self.lines[i][1]
        return [self.x["value"] + pad, self.pt(i)[1]], [self.x["value"] - p["valueW"] - pad, self.pt(i)[1]]

    def line_params(self, key, value, icon="none", **over):
        """Paramètres d'une entité line (rangée de V01 : puce, clé à gauche, valeur à droite, fente, trait, chute)."""
        vw = round(text_width(value, 32, 600), 1)
        X = self.x
        p = dict(key=key, value=value, icon=icon, x0=X["slot0"], x1=X["slot1"], h=self.slot_h, hStrip=self.strip,
                 ty=self.ty, bulletX=X["bullet"], textX=X["text"], valueX=X["value"], valueW=vw,
                 crackX=round(X["value"] - vw - 20, 1), gap=14, tilt=5, drop=14, fallPx=240, strikeW=7)
        p.update(over)
        return p

    def add(self, kit, id, lines, pos, title="Brief", scale=1, z=8, typed=True, show=True):
        """Déclare la fiche (entité fiche) et ses rangées (entités line, enfants `id`_L1…) : lines = [(clé, valeur,
        pictogramme)]. typed=True : rangées vides, à écrire avec kit.type. Renvoie les ids des rangées."""
        if len(lines) > self.n:
            raise SystemExit(f"Fiche {id} : {len(lines)} rangées pour {self.n} places (Sheet(n=…))")
        S = kit.S
        self.id = id
        S.add(id, "fiche", z=z, w=self.w, h=self.h, title=title, headerH=self.head, tabs=[], tabX=self.x["bullet"])
        S.set(id, pos=list(pos), scale=scale if show else 0)
        self.lines = []
        for i, (k, v, icon) in enumerate(lines):
            lid = f"{id}_L{i + 1}"
            p = self.line_params(k, v, icon)
            S.add(lid, "line", z=z + 1, parent=id, **p)
            S.set(lid, pos=[0, self.rows[i]], chars=0 if typed else len(k) + len(v), red=0, crack=0, flash=0, pulse=0,
                  alarm=0, strike=0, fall=0, grow=0, dimValue=0, slotFill=1, bulletOn=1, opacity=1)
            self.lines.append((lid, p))
        return [lid for lid, _ in self.lines]

    def ticks(self, kit, prefix, color, size=40, sw=8, variant=None, z=None):
        """Une coche par rangée, dans la colonne des coches (draw = 0) : ids `prefix`1…"""
        z = z if z is not None else kit.S.ents[self.id]["z"] + 3
        return [kit.tick(f"{prefix}{i + 1}", self.pt(i, "tick"), color, size=size, sw=sw, variant=variant, z=z,
                         parent=self.id) for i in range(len(self.lines))]
