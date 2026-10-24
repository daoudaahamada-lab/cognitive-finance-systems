#!/usr/bin/env python3
"""Choix de la prise de voix d'une vidéo WTH parmi les prises téléchargées du connecteur ElevenLabs.

    python3 .claude/skills/wth-video/scripts/pick_take.py V07 [--root /abs/wth-videos] [--json]

Lit build/Vxx/voice/take-<generation_id>.mp3 (et, s'il existe, words-<generation_id>.json : la transcription Scribe
de cette prise). Pour chaque prise : durée (ffprobe), débit en mots/s, marge sous la limite, alignement sur le texte
du script (si la transcription est là), prise déjà en cache. Recommande une prise et imprime son generation_id.

Limite = durée maximale de la QA (config.yaml qa.max_duration, ou qa.max_duration_by_video pour cette vidéo)
         − video.tail_seconds (0,6 s tenus après la dernière syllabe) : 60 s -> 59,4 s ; V03 (62 s) -> 61,4 s.
Règle : parmi les prises sous la limite (et, si transcrites, avec au plus 3 mots non alignés), celle dont le débit
est le plus proche de 2,6 mots/s, le débit de V01 et V02 validées (une prise plus rapide sonne pressée, une plus
lente traîne et mange la marge).
Code 0 : une prise recommandée ; 2 : aucune prise ne tient (ne pas régénérer : demander à l'utilisateur) ;
1 : pas de prise ou erreur.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

TAKE = re.compile(r"^take-(.+)\.mp3$")
TARGET_PACE = 2.6        # mots/s : V01 2,55 ; V02 2,69 (validées)
MAX_UNMATCHED = 3        # au-delà, transcrire une autre prise (références : voice-elevenlabs-mcp.md)


def default_root():
    return Path(__file__).resolve().parents[4] / "wth-videos"


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        return None


def load_pipeline(root):
    sys.path.insert(0, str(root))
    from pipeline import common  # noqa: E402
    return common


def alignment(root, text, words_path):
    """(alignés, total) du connecteur, sans rien écrire ; None si le calcul n'est pas possible."""
    try:
        sys.path.insert(0, str(root))
        from pipeline.connector import build_alignment, scribe_words
        _, matched, total = build_alignment(text, scribe_words(words_path))
        return matched, total
    except Exception as e:  # noqa: BLE001 - information facultative
        return ("?", str(e)[:80])


def cached_generation(root, vid):
    tts = Path(root) / "build" / vid / "tts.json"
    try:
        meta = json.loads(Path(json.loads(tts.read_text(encoding="utf-8"))["meta"]).read_text(encoding="utf-8"))
        return meta.get("generation_id") or None
    except (OSError, KeyError, json.JSONDecodeError):
        return None


def main():
    p = argparse.ArgumentParser(description="Choisit la prise de voix d'une vidéo WTH")
    p.add_argument("id")
    p.add_argument("--root", default=str(default_root()))
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    root = Path(a.root)
    vid = a.id
    common = load_pipeline(root)
    cfg = common.load_config()
    q = cfg["qa"]
    qa_max = float((q.get("max_duration_by_video") or {}).get(vid, q["max_duration"]))
    tail = float(cfg["video"]["tail_seconds"])
    limit = round(qa_max - tail, 3)
    s = common.script(vid)
    n_words = int(s.get("mots") or len(s["texte"].split()))

    vdir = root / "build" / vid / "voice"
    takes = sorted(vdir.glob("take-*.mp3")) if vdir.exists() else []
    in_cache = cached_generation(root, vid)
    if not takes:
        if in_cache:
            # Voix déjà importée (prises supprimées après le choix) : rien à choisir.
            mp3 = Path(json.loads((root / "build" / vid / "tts.json").read_text(encoding="utf-8"))["audio"])
            d = duration(mp3)
            msg = (f"{vid} : aucune prise téléchargée ; la voix en cache est la prise {in_cache} "
                   f"({d:.2f} s, limite {limit:.1f} s{'' if d and d <= limit else ' : DÉPASSE LA LIMITE'}). "
                   f"Rien à choisir.")
            print(json.dumps({"id": vid, "ok": True, "limit_s": limit, "takes": [], "recommended": None,
                              "cached": {"generation_id": in_cache, "duration_s": round(d, 2) if d else None}},
                             ensure_ascii=False) if a.json else msg)
            sys.exit(0)
        msg = (f"{vid} : aucune prise dans {vdir} (attendu take-<generation_id>.mp3, téléchargées depuis les "
               f"content_url du connecteur : references/voice-elevenlabs-mcp.md)")
        print(json.dumps({"id": vid, "ok": False, "error": msg}, ensure_ascii=False) if a.json else msg)
        sys.exit(1)

    rows = []
    for t in takes:
        gen = TAKE.match(t.name).group(1)
        d = duration(t)
        words = vdir / f"words-{gen}.json"
        al = alignment(root, s["texte"], words) if words.exists() else None
        unmatched = (al[1] - al[0]) if al and isinstance(al[0], int) else None
        fits = d is not None and d <= limit
        aligned_ok = unmatched is None or unmatched <= MAX_UNMATCHED
        rows.append({
            "take": t.name, "generation_id": gen, "duration_s": round(d, 2) if d else None,
            "pace_wps": round(n_words / d, 3) if d else None, "margin_s": round(limit - d, 2) if d else None,
            "fits": fits, "scribe": words.name if words.exists() else None,
            "aligned": f"{al[0]}/{al[1]}" if al else None, "unmatched": unmatched,
            "eligible": fits and aligned_ok, "in_cache": gen == in_cache,
        })
    eligible = [r for r in rows if r["eligible"]]
    eligible.sort(key=lambda r: (abs(r["pace_wps"] - TARGET_PACE), -r["duration_s"]))
    best = eligible[0] if eligible else None
    result = {"id": vid, "ok": bool(best), "limit_s": limit, "qa_max_s": qa_max, "tail_s": tail, "words": n_words,
              "target_pace_wps": TARGET_PACE, "takes": rows, "recommended": best,
              "order": [r["generation_id"] for r in eligible]}
    if a.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if best else 2)

    src = "qa.max_duration_by_video" if vid in (q.get("max_duration_by_video") or {}) else "qa.max_duration"
    print(f"{vid} « {s.get('titre', '')} » : {n_words} mots ; limite {limit:.1f} s ({src} {qa_max:g} s − "
          f"{tail:g} s de fin)")
    print(f"{'prise':34} {'durée':>7} {'débit':>7} {'marge':>7}  Scribe        état")
    for r in rows:
        etat = []
        etat.append("tient" if r["fits"] else "TROP LONGUE")
        if r["unmatched"] is not None and r["unmatched"] > MAX_UNMATCHED:
            etat.append(f"{r['unmatched']} mots non alignés")
        if r["in_cache"]:
            etat.append("en cache")
        dur = f"{r['duration_s']:.2f}" if r["duration_s"] else "?"
        pace = f"{r['pace_wps']:.2f}" if r["pace_wps"] else "?"
        marg = f"{r['margin_s']:+.2f}" if r["margin_s"] is not None else "?"
        print(f"{r['take']:34} {dur:>7} {pace:>7} {marg:>7}  {(r['aligned'] or '—'):12}  {', '.join(etat)}")
    if best:
        print(f"\nRecommandée : {best['take']} (generation_id {best['generation_id']}, {best['duration_s']:.2f} s, "
              f"{best['pace_wps']:.2f} mots/s ; débit visé {TARGET_PACE} mots/s)")
        if len(eligible) > 1:
            print("Ordre de repli (Scribe en désaccord, chiffre mal lu) : " +
                  " > ".join(r["generation_id"] for r in eligible[1:]))
        if not best["scribe"]:
            print("Étape suivante : creative_add_flow_asset_node puis creative_transcribe_audio sur cette prise.")
        sys.exit(0)
    timed = [r for r in rows if r["duration_s"] and (r["unmatched"] is None or r["unmatched"] <= MAX_UNMATCHED)]
    shortest = min(timed or [r for r in rows if r["duration_s"]], key=lambda r: r["duration_s"], default=None)
    print(f"\nAucune prise ne tient sous {limit:.1f} s. Ne relance PAS de génération (elle est facturée).")
    if shortest:
        factor = shortest["duration_s"] / limit
        need = shortest["duration_s"] + tail
        print(f"La plus courte : {shortest['take']} ({shortest['duration_s']:.2f} s) ; il faudrait l'accélérer de "
              f"×{factor:.3f}{' (au-delà de ×1,04, ça s’entend)' if factor > 1.04 else ''}, ou accepter "
              f"{need:.1f} s pour cette vidéo.")
    print("Demande à l'utilisateur : (a) accélérer la prise la plus courte (ffmpeg atempo ≤ 1,04, temps Scribe mis à "
          "l'échelle) ; (b) accepter une durée plus longue pour cette vidéo (config.yaml qa.max_duration_by_video, "
          "comme V03 à 62 s) ; (c) raccourcir le script (nouvelle génération, crédits). "
          "Consigne ensuite le choix : status.py set " + vid + " voice blocked --note \"…\".")
    sys.exit(2)


if __name__ == "__main__":
    main()
