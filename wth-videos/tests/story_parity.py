"""Parité Python / TypeScript de la composition Story : pipeline/story.py recopie motion/src/story/timeline.ts
(assouplissements, LEAD, matrices, cubiques des fils) pour calculer les positions monde avec les nombres mêmes du
rendu. Ce test évalue quelques pistes, matrices et points de fil des deux côtés et compare (écart <= 1e-6).
Il vérifie aussi motion/src/story/geometry.json, la géométrie partagée (figurine, stylo, tampon, étiquette...) : le
fichier se charge, porte les clés attendues, est importé par draw.tsx / entities.tsx et, si pipeline/story.py expose
GEOM, c'est bien ce fichier. Enfin, les copies Python du kit (pipeline/story_kit.py format_fr et crowd_points) donnent
les mêmes textes et positions que entities_kit.tsx (formatFr, crowdPoints), demis et foule vide compris.

    python3 -m tests.story_parity

timeline.ts est transpilé par l'esbuild de motion/node_modules (aucune dépendance de plus), puis exécuté par node.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pipeline.story as story
from pipeline.story import (cubic_at, eval_track, local_matrix, mat_apply, mat_mul, point_at_length, wire_cubic)
from pipeline.story_kit import crowd_points, format_fr

ROOT = Path(__file__).resolve().parent.parent
MOTION = ROOT / "motion"
GEOMETRY = MOTION / "src" / "story" / "geometry.json"
GEOM_KEYS = {
    "FIGURE": ("h", "top", "base", "pivot", "bust", "head", "sw", "shoulder", "hand", "arm"),
    "PEN": ("len", "r", "tip"),
    "STAMP_HANDLE": ("neck", "neckW", "knobW", "knobH"),
    "TAG": ("r", "fold", "discR", "iconX", "textX", "shadow"),
    "DOC_DISC": ("r", "inset"),
    "BULLET": ("r",),
    "TICK": ("size", "pts", "aiBox"),
    "MARKER": ("r", "activeR", "labelDy", "labelSize"),
}

TRACKS = [
    [{"f": 0, "v": 0}, {"f": 10, "v": 1, "d": 9, "e": "out"}, {"f": 14, "v": 0.4, "d": 6, "e": "inOut"}],
    [{"f": 0, "v": [100, 200]}, {"f": 5, "v": [300, 120], "d": 16, "e": "inOut", "arc": 40},
     {"f": 30, "v": [0, 0], "d": 11, "e": "in"}],
    [{"f": 0, "v": 1}, {"f": 3, "v": 2, "d": 0}, {"f": 8, "v": 0.5, "d": 7, "e": "outQuad"}],
    [{"f": 0, "v": 0}, {"f": 2, "v": 1, "d": 12, "e": "inOutSine"}, {"f": 6, "v": 3, "d": 5, "e": "linear"}],
]
FRAMES = list(range(-2, 48, 3))
MATS = [([540, 740], 0, 1, 1), ([310, 740], -8, 0.95, 0.95), ([12.5, -30], 37, 1.4, 0.7)]
POINTS = [[0, 0], [-250, 192], [150, -22]]
WIRES = [([462, 518], [690, 520], 0), ([450, 910], [700, 905], 34), ([300, 400], [100, 900], -12)]
FRACS = [0, 0.13, 0.5, 0.77, 1]

NODE = r"""
import * as T from './timeline.mjs';
const spec = JSON.parse(process.argv[2]);
const out = {tracks: [], mats: [], wires: []};
for (const tr of spec.tracks) out.tracks.push(spec.frames.map((n) => T.evalTrack(tr, n, 0)));
let m = T.IDENTITY;
for (const [pos, rot, sx, sy] of spec.mats) {
  m = T.mul(m, T.localMatrix(pos, rot, sx, sy));
  out.mats.push({m, pts: spec.points.map((p) => T.apply(m, p))});
}
for (const [a, b, sag] of spec.wires) {
  const c = T.wireCubic(a, b, sag);
  const path = T.wirePath(a, b, sag);
  out.wires.push({at: spec.fracs.map((t) => T.cubicAt(c, t)), len: spec.fracs.map((t) => path.pointAt(t))});
}
console.log(JSON.stringify(out));
"""


# Copies Python du kit : nombres (demis, négatifs, milliers, signe) et foules (anneau, arc, rang, points donnés, vide).
NUMBERS = [(2.5, 0, False), (0.125, 2, False), (-2.5, 0, False), (3.45, 1, False), (12500.5, 0, False),
           (1234567.891, 2, False), (-40, 0, False), (0.004, 2, True), (7.5, 0, True), (-0.4, 0, False), (99.95, 1, False)]
CROWDS = [{"n": 6}, {"n": 5, "r": 90, "span": 180, "a0": -180}, {"n": 4, "layout": "row", "gap": 40}, {"pts": []},
          {"pts": [[1, 2], [3, -4]], "n": 6}, {"n": 1, "span": 120}]
KIT_TS = MOTION / "src" / "story" / "entities_kit.tsx"
KIT_NODE = r"""
import {formatFr, crowdPoints} from './kit.mjs';
const spec = JSON.parse(process.argv[2]);
console.log(JSON.stringify({numbers: spec.numbers.map(([v, d, s]) => formatFr(v, d, s)),
                            crowds: spec.crowds.map((p) => crowdPoints(p))}));
"""


def ts_function(src, name):
    """Source d'une fonction exportée `export const name = ... };` de entities_kit.tsx (sans ses imports React)."""
    m = re.search(rf"^export const {name} = .*?^}};$", src, re.S | re.M)
    if not m:
        raise SystemExit(f"ÉCHEC : {name} introuvable dans {KIT_TS.relative_to(ROOT)}")
    return m.group(0)


def check_kit_helpers(esbuild, tmp):
    """format_fr / crowd_points (Python) = formatFr / crowdPoints (entities_kit.tsx, transpilés et exécutés)."""
    src = KIT_TS.read_text(encoding="utf-8")
    (tmp / "kit.ts").write_text("\n\n".join(ts_function(src, n) for n in ("formatFr", "crowdPoints")) + "\n")
    subprocess.run([str(esbuild), str(tmp / "kit.ts"), "--format=esm", "--log-level=error",
                    f"--outfile={tmp / 'kit.mjs'}"], check=True)
    (tmp / "kit_run.mjs").write_text(KIT_NODE)
    ts = json.loads(subprocess.run(["node", str(tmp / "kit_run.mjs"), json.dumps({"numbers": NUMBERS, "crowds": CROWDS})],
                                   check=True, text=True, capture_output=True).stdout)
    bad = [f"format_fr{args} = {format_fr(*args)!r}, formatFr = {t!r}"
           for args, t in zip(NUMBERS, ts["numbers"]) if format_fr(*args) != t]
    for p, t in zip(CROWDS, ts["crowds"]):
        py = crowd_points(p)
        if len(py) != len(t) or any(abs(a - b) > 1e-9 for q, r in zip(py, t) for a, b in zip(q, r)):
            bad.append(f"crowd_points({p}) : {len(py)} points, crowdPoints : {len(t)}")
    if bad:
        raise SystemExit("ÉCHEC : story_kit diverge de entities_kit.tsx :\n  " + "\n  ".join(bad))
    print(f"kit     {len(NUMBERS) + len(CROWDS):4d} cas (format_fr, crowd_points), identiques")


def flat(x):
    if isinstance(x, (list, tuple)):
        return [v for y in x for v in flat(y)]
    return [float(x)]


def check_geometry():
    """geometry.json : chargement, clés, cohérence de la figurine, import côté TSX et côté Python (GEOM)."""
    try:
        geom = json.loads(GEOMETRY.read_text())
    except (OSError, ValueError) as e:
        raise SystemExit(f"ÉCHEC : {GEOMETRY.relative_to(ROOT)} illisible ({e})")
    missing = [f"{k}.{f}" for k, fields in GEOM_KEYS.items() for f in fields if f not in geom.get(k, {})]
    if missing:
        raise SystemExit(f"ÉCHEC : geometry.json, clés manquantes : {', '.join(missing)}")
    fig = geom["FIGURE"]
    if fig["base"] - fig["top"] != fig["h"] or fig["pivot"] != [0, fig["base"]]:
        raise SystemExit("ÉCHEC : geometry.json, FIGURE incohérente (h = base - top, pivot = [0, base])")
    if not {"upper", "fore", "sw"} <= set(fig["arm"]) or len(geom["TICK"]["pts"]) != 3:
        raise SystemExit("ÉCHEC : geometry.json, FIGURE.arm (upper, fore, sw) ou TICK.pts (3 points) incomplets")
    for tsx in ("draw.tsx", "entities.tsx"):
        if "from './geometry.json'" not in (GEOMETRY.parent / tsx).read_text():
            raise SystemExit(f"ÉCHEC : {tsx} n'importe pas geometry.json")
    py = getattr(story, "GEOM", None)
    if py is not None and py != geom:
        raise SystemExit("ÉCHEC : pipeline.story.GEOM diffère de motion/src/story/geometry.json")
    print(f"geometry {len(geom) - ('_doc' in geom):4d} blocs, OK" + ("" if py is not None else " (pipeline.story.GEOM absent)"))


def main():
    check_geometry()
    spec = {"tracks": TRACKS, "frames": FRAMES, "mats": MATS, "points": POINTS, "wires": WIRES, "fracs": FRACS}
    esbuild = MOTION / "node_modules" / ".bin" / "esbuild"
    if not esbuild.exists():
        raise SystemExit("motion/node_modules absent (esbuild) : lance « npm ci » dans motion/.")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        subprocess.run([str(esbuild), str(MOTION / "src" / "story" / "timeline.ts"), "--format=esm", "--log-level=error",
                        f"--outfile={tmp / 'timeline.mjs'}"], check=True)
        (tmp / "run.mjs").write_text(NODE)
        ts = json.loads(subprocess.run(["node", str(tmp / "run.mjs"), json.dumps(spec)], check=True, text=True,
                                       capture_output=True).stdout)
        check_kit_helpers(esbuild, tmp)
    py = {"tracks": [[eval_track(tr, n, 0) for n in FRAMES] for tr in TRACKS], "mats": [], "wires": []}
    m = [1, 0, 0, 1, 0, 0]
    for pos, rot, sx, sy in MATS:
        m = mat_mul(m, local_matrix(pos, rot, sx, sy))
        py["mats"].append({"m": m, "pts": [mat_apply(m, p) for p in POINTS]})
    for a, b, sag in WIRES:
        c = wire_cubic(a, b, sag)
        # wirePath (sans point de passage) = point_at_length sur 32 segments, comme pipeline.story.point_at_length
        py["wires"].append({"at": [cubic_at(c, t) for t in FRACS], "len": [point_at_length(c, t) for t in FRACS]})
    worst = 0.0
    for key in ("tracks", "mats", "wires"):
        if key == "tracks":
            a, b = flat(py[key]), flat(ts[key])
        else:
            a = flat([[v for k in sorted(d) for v in flat(d[k])] for d in py[key]])
            b = flat([[v for k in sorted(d) for v in flat(d[k])] for d in ts[key]])
        if len(a) != len(b):
            raise SystemExit(f"{key} : {len(a)} valeurs (Python) contre {len(b)} (TypeScript)")
        err = max(abs(x - y) for x, y in zip(a, b))
        worst = max(worst, err)
        print(f"{key:7s} {len(a):4d} valeurs, écart max {err:.2e}")
    if worst > 1e-6:
        print("ÉCHEC : pipeline/story.py et motion/src/story/timeline.ts divergent")
        sys.exit(1)
    print("OK : parité Python / TypeScript")


if __name__ == "__main__":
    main()
