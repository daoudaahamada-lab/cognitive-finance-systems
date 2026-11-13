#!/usr/bin/env bash
# Reconstruit la vidéo complète à partir des sources (voir README.md).
set -euo pipefail
cd "$(dirname "$0")"
OUT=dist/agentic-wealth_audit-cgp_fr.mp4

if [ "${VOICE:-eleven}" = "piper" ]; then
  python3 tools/tts.py          # voix locale gratuite (Piper) + timeline + SRT + texte définitif
else
  python3 tools/eleven_align.py # voix ElevenLabs (build/eleven/*.mp3) alignée + timeline + SRT + texte définitif
fi
python3 tools/mix_audio.py      # voix + nappe originale, -16 LUFS
python3 tools/conducteur.py     # conducteur scène par scène
node tools/render.js --workers "${WORKERS:-4}"   # images 1920x1080 25 i/s -> build/video_noaudio.mp4

ffmpeg -y -v error -i build/video_noaudio.mp4 -i build/mix.wav \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart \
  -metadata title="On audite un cabinet de gestion de patrimoine (simulation pédagogique)" \
  -metadata language=fra "$OUT"
ffprobe -v error -show_entries format=duration:stream=codec_type,codec_name,width,height -of compact "$OUT"
