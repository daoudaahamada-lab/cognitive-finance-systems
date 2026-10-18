"""Alignement caractère par caractère (ElevenLabs) -> mots horodatés.

Un « mot » est un groupe séparé par une espace ordinaire : les espaces insécables
gardent ensemble « 1 % », « 4 600 € » ou « question ? », pour qu'ils ne soient
jamais coupés dans les sous-titres.
"""
import argparse
import difflib

from .common import build_dir, read_json, script, write_json

SEPARATORS = {" ", "\n", "\t"}


def char_times(text, alignment):
    """Associe à chaque caractère du texte ses temps (start, end), même si l'alignement diffère légèrement."""
    chars = alignment["characters"]
    starts = alignment["character_start_times_seconds"]
    ends = alignment["character_end_times_seconds"]
    aligned = "".join(chars)
    times = [None] * len(text)
    if aligned == text:
        return list(zip(starts, ends)), True
    sm = difflib.SequenceMatcher(None, text, aligned, autojunk=False)
    for block in sm.get_matching_blocks():
        for k in range(block.size):
            times[block.a + k] = (starts[block.b + k], ends[block.b + k])
    # Caractères non retrouvés : on reprend le temps du voisin connu le plus proche.
    last = (0.0, 0.0)
    for i, t in enumerate(times):
        if t is None:
            times[i] = (last[1], last[1])
        else:
            last = t
    return times, False


def tokenize(text):
    """[(début, fin)] des groupes séparés par des espaces ordinaires."""
    spans, start = [], None
    for i, ch in enumerate(text):
        if ch in SEPARATORS:
            if start is not None:
                spans.append((start, i))
                start = None
        elif start is None:
            start = i
    if start is not None:
        spans.append((start, len(text)))
    # Une ponctuation isolée (ex. « — ») est rattachée au mot précédent.
    merged = []
    for a, b in spans:
        if merged and not any(c.isalnum() for c in text[a:b]):
            merged[-1] = (merged[-1][0], b)
        else:
            merged.append((a, b))
    return merged


def segment_index(segments):
    """Position de début de chaque segment dans le texte complet (segments joints par une espace)."""
    bounds, pos = [], 0
    for seg in segments:
        bounds.append(pos)
        pos += len(seg["texte"]) + 1
    return bounds


def words_for(video_id):
    s = script(video_id)
    tts = read_json(build_dir(video_id) / "tts.json")
    meta = read_json(tts["meta"])
    text = meta["request"]["text"]
    times, exact = char_times(text, meta["alignment"])
    bounds = segment_index(s["segments"]) if text == s["texte"] else None
    words = []
    for a, b in tokenize(text):
        core = [i for i in range(a, b) if text[i].isalnum()] or list(range(a, b))
        seg = None
        if bounds:
            seg = max(k for k, start in enumerate(bounds) if start <= a)
        words.append({
            "w": text[a:b],
            "start": round(times[core[0]][0], 3),
            "end": round(times[core[-1]][1], 3),
            "char_start": a,
            "segment": seg,
        })
    out = build_dir(video_id) / "words.json"
    write_json(out, {"exact_alignment": exact, "text": text, "words": words})
    print(f"{video_id} : {len(words)} mots horodatés ({'alignement exact' if exact else 'alignement recalé'})")
    return words


def main():
    p = argparse.ArgumentParser()
    p.add_argument("id")
    words_for(p.parse_args().id)


if __name__ == "__main__":
    main()
