#!/usr/bin/env bash
# Génère la voix témoin (synthèse Pico, fr-FR) phrase par phrase dans public/voix/,
# puis mesure les durées. Prérequis Linux : sudo apt install libttspico-utils ffmpeg python3
# Pour votre propre voix : déposez L01.wav ... L19.wav dans public/voix/ puis lancez outils/mesurer-voix.sh.
set -euo pipefail
cd "$(dirname "$0")/.."
TMP=$(mktemp -d)
python3 -c "import json; [print(l['id'] + '\t' + l['prononciation']) for l in json.load(open('voix-off/script.json'))]" |
while IFS=$'\t' read -r id texte; do
  pico2wave -l fr-FR -w "$TMP/$id.wav" "$texte" < /dev/null
  # un peu plus posé (tempo 0,92 sans changer la hauteur), 48 kHz, niveau homogène
  ffmpeg -nostdin -v error -y -i "$TMP/$id.wav" -af "atempo=0.92,highpass=f=70,loudnorm=I=-18:TP=-2:LRA=7,aresample=48000" -ac 1 "public/voix/$id.wav"
done
rm -rf "$TMP"
bash outils/mesurer-voix.sh
