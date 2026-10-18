"""Import d'une voix générée par le connecteur ElevenLabs (Flows) dans le cache du pipeline.

Utilisé quand l'API n'est pas joignable depuis la machine (réseau filtré, pas de clé) :
la voix est générée par le connecteur (eleven_multilingual_v2), les temps de chaque mot
viennent de la transcription Scribe du même audio. On reconstruit un alignement par
caractère sur le texte exact du script, rangé sous la même clé de cache que l'endpoint
with-timestamps : `make video` le réutilise ensuite sans jamais rappeler l'API.

    python3 -m pipeline.connector V01 --audio take.mp3 --words words.json --generation-id XXX
"""
import argparse
import difflib
import json
import re
import shutil
from datetime import datetime, timezone

from .common import CACHE_TTS, load_config, read_json, script, write_json
from .tts import cache_key, cache_paths, request_spec
from .words import tokenize


def norm(word):
    return re.sub(r"[^\w’']", "", word.lower().replace(" ", " ")).replace("'", "’")


def scribe_words(path):
    data = read_json(path)
    words = data.get("words", data) if isinstance(data, dict) else data
    return [w for w in words if w.get("type", "word") == "word" and norm(w["text"])]


def build_alignment(text, words):
    """Alignement caractère par caractère reconstruit à partir des temps de mots Scribe."""
    spans = tokenize(text)
    ours = [norm(text[a:b]) for a, b in spans]
    theirs = [norm(w["text"]) for w in words]
    times = [None] * len(spans)
    sm = difflib.SequenceMatcher(None, ours, theirs, autojunk=False)
    for block in sm.get_matching_blocks():
        for k in range(block.size):
            w = words[block.b + k]
            times[block.a + k] = (float(w["start"]), float(w["end"]))
    matched = sum(t is not None for t in times)
    # Mots non retrouvés : répartis entre les voisins connus, au prorata de leur longueur.
    i = 0
    while i < len(spans):
        if times[i] is not None:
            i += 1
            continue
        j = i
        while j < len(spans) and times[j] is None:
            j += 1
        left = times[i - 1][1] if i > 0 else 0.0
        right = times[j][0] if j < len(spans) else (words[-1]["end"] if words else left)
        lengths = [spans[k][1] - spans[k][0] for k in range(i, j)]
        total, pos = sum(lengths) or 1, left
        for k, n in zip(range(i, j), lengths):
            step = (right - left) * n / total
            times[k] = (pos, pos + step)
            pos += step
        i = j

    starts, ends = [0.0] * len(text), [0.0] * len(text)
    prev_end = 0.0
    for idx, ((a, b), (s, e)) in enumerate(zip(spans, times)):
        for c in range(prev_char_end(spans, idx), a):
            starts[c], ends[c] = prev_end, s
        for c in range(a, b):
            frac0, frac1 = (c - a) / (b - a), (c - a + 1) / (b - a)
            starts[c], ends[c] = s + (e - s) * frac0, s + (e - s) * frac1
        prev_end = e
    for c in range(spans[-1][1] if spans else 0, len(text)):
        starts[c], ends[c] = prev_end, prev_end
    alignment = {
        "characters": list(text),
        "character_start_times_seconds": [round(x, 3) for x in starts],
        "character_end_times_seconds": [round(x, 3) for x in ends],
    }
    return alignment, matched, len(spans)


def prev_char_end(spans, idx):
    return spans[idx - 1][1] if idx > 0 else 0


def import_take(video_id, audio, words_path, generation_id="", voice_id=None):
    cfg = load_config()
    voice_id = voice_id or cfg["tts"]["voice_id"]
    if not voice_id:
        raise SystemExit("Renseigne tts.voice_id dans config.yaml ou passe --voice-id.")
    s = script(video_id)
    spec = request_spec(s["texte"], voice_id, cfg)
    key = cache_key(spec)
    mp3, meta = cache_paths(key)
    if mp3.exists() and meta.exists():
        print(f"{video_id} : déjà en cache ({key}), rien à importer.")
        return key
    words = scribe_words(words_path)
    alignment, matched, total = build_alignment(s["texte"], words)
    if matched < total:
        print(f"{video_id} : {total - matched} mot(s) sur {total} absents de la transcription, temps interpolés.")
    CACHE_TTS.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(audio, mp3)
    write_json(meta, {
        "request": spec,
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "elevenlabs-connector",
        "generation_id": generation_id,
        "alignment_source": "scribe",
        "alignment_matched_words": f"{matched}/{total}",
        "alignment": alignment,
        "scribe_words": words,
    })
    print(f"{video_id} : voix importée dans le cache ({key}), {matched}/{total} mots alignés par Scribe.")
    return key


def main():
    p = argparse.ArgumentParser()
    p.add_argument("id")
    p.add_argument("--audio", required=True)
    p.add_argument("--words", required=True, help="JSON des mots Scribe (liste ou {words: [...]})")
    p.add_argument("--generation-id", default="")
    p.add_argument("--voice-id")
    a = p.parse_args()
    import_take(a.id, a.audio, a.words, a.generation_id, a.voice_id)


if __name__ == "__main__":
    main()
