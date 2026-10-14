#!/usr/bin/env bash
# Mesure la durée de chaque phrase de public/voix/ et écrit public/voix/durees.json.
# Le montage (src/timeline.ts) se recale automatiquement sur ces durées.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 - <<'PY'
import json, subprocess
lignes = json.load(open('voix-off/script.json'))
durees = {}
for l in lignes:
    f = f"public/voix/{l['id']}.wav"
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True, check=True)
    durees[l['id']] = round(float(out.stdout.strip()), 3)
json.dump(durees, open('public/voix/durees.json', 'w'), indent=2)
print(json.dumps(durees, indent=2))
print('total', round(sum(durees.values()), 2), 's')
PY
