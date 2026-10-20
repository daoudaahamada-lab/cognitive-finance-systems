"""Parité Python / TypeScript de la composition Story : pipeline/story.py recopie motion/src/story/timeline.ts
(assouplissements, LEAD, matrices, cubiques des fils) pour calculer les positions monde avec les nombres mêmes du
rendu. Ce test évalue quelques pistes, matrices et points de fil des deux côtés et compare (écart <= 1e-6).

    python3 -m tests.story_parity

timeline.ts est transpilé par l'esbuild de motion/node_modules (aucune dépendance de plus), puis exécuté par node.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from pipeline.story import (cubic_at, eval_track, local_matrix, mat_apply, mat_mul, point_at_length, wire_cubic)

ROOT = Path(__file__).resolve().parent.parent
MOTION = ROOT / "motion"

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


def flat(x):
    if isinstance(x, (list, tuple)):
        return [v for y in x for v in flat(y)]
    return [float(x)]


def main():
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
