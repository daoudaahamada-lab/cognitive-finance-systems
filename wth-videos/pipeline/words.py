"""Alignement caractère par caractère (ElevenLabs) -> mots horodatés.

Un « mot » est un groupe séparé par une espace ordinaire : les espaces insécables
gardent ensemble « 1 % », « 4 600 € » ou « question ? », pour qu'ils ne soient
jamais coupés dans les sous-titres.
"""
import argparse
import difflib

from .common import build_dir, read_json, script, write_json

SEPARATORS = {" ", "\n", "\t"}
OPENING = set("«“‘‹„([¿¡")
SPOKEN_SYMBOLS = set("€%$£")


def canon(text):
    """Les espaces insécables comptent comme des espaces pour comparer avec l'alignement renvoyé."""
    return text.replace("\u00a0", " ").replace("\u202f", " ")


def char_times(text, alignment):
    """Associe à chaque caractère du texte ses temps (start, end), même si l'alignement diffère légèrement."""
    chars = alignment["characters"]
    starts = alignment["character_start_times_seconds"]
    ends = alignment["character_end_times_seconds"]
    aligned = canon("".join(chars))
    times = [None] * len(text)
    if aligned == canon(text):
        return list(zip(starts, ends)), True, 0
    sm = difflib.SequenceMatcher(None, canon(text), aligned, autojunk=False)
    for block in sm.get_matching_blocks():
        for k in range(block.size):
            times[block.a + k] = (starts[block.b + k], ends[block.b + k])
    unmatched = sum(1 for i, t in enumerate(times) if t is None and text[i].isalnum())
    # Caractères non retrouvés : on reprend le temps du voisin connu le plus proche.
    last = (0.0, 0.0)
    for i, t in enumerate(times):
        if t is None:
            times[i] = (last[1], last[1])
        else:
            last = t
    return times, False, unmatched


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
    # Une ponctuation isolée est rattachée à son mot : au suivant si elle ouvre (« ( …), sinon au précédent.
    merged, pending = [], None
    for a, b in spans:
        chunk = text[a:b]
        if not any(c.isalnum() for c in chunk):
            if all(c in OPENING for c in chunk):
                pending = a if pending is None else pending
                continue
            if merged and pending is None:
                merged[-1] = (merged[-1][0], b)
                continue
        merged.append((pending if pending is not None else a, b))
        pending = None
    if pending is not None:
        merged.append((pending, len(text)))
    return merged


def segment_index(segments):
    """Position de début de chaque segment dans le texte complet (segments joints par une espace)."""
    bounds, pos = [], 0
    for seg in segments:
        bounds.append(pos)
        pos += len(seg["texte"]) + 1
    return bounds


def trim_pause_ends(words, audio, margin=0.15, lead=0.05):
    """Facultatif (`--trim-pauses`, ajouté pour V12 ; défaut inchangé) : un mot dont la fin, selon l'alignement,
    enjambe une pause réellement mesurée dans l'audio (silencedetect, mêmes réglages que la QA « Synchro
    sous-titres ») finit au début de cette pause (+ `lead`). Seules les FINS changent : les débuts, donc les temps
    forts et la surbrillance, restent identiques. -> liste des mots raccourcis."""
    from .qa import pause_conflicts, silences   # import tardif : qa importe ce module
    pauses = [(a, b) for a, b in silences(audio) if a > 0.05]
    done = []
    for s0, s1 in pauses:
        for i, w in enumerate(words[:-1]):
            if " " in w["w"] or w["w"].rstrip("»  ").endswith((".", "!", "?", "…")):
                continue
            if w["start"] <= s0 + margin and w["end"] > s0 + margin and w["start"] < s1 - margin:
                end = round(max(w["start"] + 0.05, s0 + lead), 3)
                done.append(f"« {w['w']} » {w['start']:.2f}–{w['end']:.2f} -> {end:.2f} (pause {s0:.2f}–{s1:.2f})")
                w["end"] = end
    left = pause_conflicts(words, pauses)
    if left:
        print("conflits restants : " + " ; ".join(left))
    return done


def words_for(video_id, trim_pauses=False):
    s = script(video_id)
    tts = read_json(build_dir(video_id) / "tts.json")
    meta = read_json(tts["meta"])
    text = meta["request"]["text"]
    times, exact, unmatched = char_times(text, meta["alignment"])
    bounds = segment_index(s["segments"]) if text == s["texte"] else None
    words = []
    for a, b in tokenize(text):
        # Les symboles prononcés (« € » = « euros », « % » = « pour cent ») font partie du mot.
        core = [i for i in range(a, b) if text[i].isalnum() or text[i] in SPOKEN_SYMBOLS] or list(range(a, b))
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
    trimmed = trim_pause_ends(words, tts["audio"]) if trim_pauses else []
    out = build_dir(video_id) / "words.json"
    data = {"exact_alignment": exact, "unmatched_chars": unmatched, "text": text, "words": words}
    if trim_pauses:
        data["trimmed_ends"] = trimmed
    write_json(out, data)
    for t in trimmed:
        print(f"fin raccourcie sur la pause : {t}")
    state = "alignement exact" if exact else f"alignement recalé, {unmatched} caractère(s) non retrouvé(s)"
    print(f"{video_id} : {len(words)} mots horodatés ({state})")
    return words


def main():
    p = argparse.ArgumentParser()
    p.add_argument("id")
    p.add_argument("--trim-pauses", action="store_true",
                   help="fins de mots qui enjambent une pause mesurée ramenées au début de la pause (débuts inchangés)")
    a = p.parse_args()
    words_for(a.id, trim_pauses=a.trim_pauses)


if __name__ == "__main__":
    main()
