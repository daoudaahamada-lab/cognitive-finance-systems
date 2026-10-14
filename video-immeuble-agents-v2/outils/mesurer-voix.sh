#!/usr/bin/env bash
# Rogne les silences de début et de fin de chaque phrase de public/voix/ (en place, sans effet si déjà rogné),
# puis mesure les durées dans public/voix/durees.json. Le montage (src/voix.ts) se recale sur ces durées.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 - <<'PY'
import json, os, subprocess
lignes = json.load(open('voix-off/script.json'))
rogne = ('silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.04,'
         'areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse')
durees = {}
for l in lignes:
    f = f"public/voix/{l['id']}.wav"
    tmp = f + '.tmp.wav'
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', f, '-af', rogne, '-ar', '48000', '-ac', '1', tmp], check=True)
    os.replace(tmp, f)
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True, check=True)
    durees[l['id']] = round(float(out.stdout.strip()), 3)
json.dump(durees, open('public/voix/durees.json', 'w'), indent=2)
print(json.dumps(durees, indent=2))
print('total', round(sum(durees.values()), 2), 's')
PY
