#!/usr/bin/env python3
"""Contrôles complémentaires d'un storyboard Story, après « python3 -m pipeline.story Vxx --check ».

    python3 .claude/skills/wth-storyboard/scripts/soft_check.py V05 [--root /abs/wth-videos]

--check refuse ce qui casserait la mise en scène (champs, scènes contiguës, débuts de mots, texte, idées-clés). Ce script
signale ce qui la rendrait fragile ou ferait échouer la QA plus tard :
  ✘ (code 1)  écart au schéma (references/storyboard.schema.json) ; deux temps forts sur le même mot dans une scène
              (Story.beat prendrait toujours le premier) ;
  ! (alerte)  plus de 3 s sans temps fort (la QA refuse une image figée > 3,5 s, hors carte de fin) ; objet du fil
              absent de la distribution ou de beaucoup de scènes ; point 1-3 ou chute sans idée-clé principale ;
              plus de 3 entités nouvelles ; temps forts trop rares pour la cadence de la référence ; dernière scène
              qui n'est pas la phrase d'appel seule (seule la carte de fin est dispensée du contrôle d'image figée).
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
STRIP = set(".,;:!?…«»\"“”()[]")
GAP_MAX = 3.0          # s sans temps fort (la QA tolère 3,5 s d'image figée)
MAIN_SEGMENTS = ("point1", "point2", "point3", "chute")


def norm(w):
    w = w.replace(" ", " ").replace(" ", " ")
    return unicodedata.normalize("NFC", "".join(c for c in w if c not in STRIP).strip()).replace("’", "'")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("id")
    ap.add_argument("--root", type=Path, default=SKILL.parents[2] / "wth-videos")
    a = ap.parse_args()
    root = a.root.resolve()
    sb_path = root / "scripts" / "storyboards" / f"{a.id}.json"
    if not sb_path.exists():
        print(f"{a.id} : {sb_path} absent")
        return 1
    sb = json.loads(sb_path.read_text(encoding="utf-8"))
    errors, alerts = [], []

    try:
        import jsonschema
        schema = json.loads((SKILL / "references" / "storyboard.schema.json").read_text(encoding="utf-8"))
        for e in sorted(jsonschema.Draft7Validator(schema).iter_errors(sb), key=lambda e: list(e.path)):
            where = "/".join(str(p) for p in e.path) or "(racine)"
            errors.append(f"schéma, {where} : {e.message[:160]}")
    except ImportError:
        alerts.append("jsonschema absent : schéma non vérifié (pip install jsonschema)")

    scenes = sb.get("scenes") or []
    dur = scenes[-1]["t_end"] if scenes else 0
    beats = []
    for s in scenes:
        seen = {}
        for b in s.get("beats", []):
            k = norm(b.get("mot", ""))
            if k in seen:
                errors.append(f"{s['id']} : deux temps forts sur « {b['mot']} » ({seen[k]} et {b.get('t')} s) : "
                              f"Story.beat ne trouve que le premier ; garder un seul temps fort ou caler le second sur "
                              f"un autre mot")
            seen[k] = b.get("t")
            if isinstance(b.get("t"), (int, float)):
                beats.append((b["t"], s["id"]))
    beats.sort()
    last_scene = scenes[-1]["id"] if scenes else None
    prev = (0.0, scenes[0]["id"] if scenes else "")
    for t, sid in beats + [(dur, None)]:
        if t - prev[0] > GAP_MAX and prev[1] != last_scene:
            alerts.append(f"{prev[0]:.2f} → {t:.2f} s ({prev[1]}) : {t - prev[0]:.1f} s sans temps fort. Si rien ne bouge, "
                          f"la QA refuse (image figée > 3,5 s) : ajouter un événement ou une dérive narrative linéaire")
        prev = (t, sid)
    if dur and len(beats) < dur / 2.5:
        alerts.append(f"{len(beats)} temps forts pour {dur:.1f} s : la référence vise environ un événement par seconde "
                      f"(au moins un par 7,5 mots)")

    cast = {c.get("id") for c in sb.get("cast", [])}
    fil = (sb.get("objet_fil") or {}).get("id")
    if fil and fil not in cast:
        alerts.append(f"objet_fil « {fil} » absent de la distribution (cast)")
    elif fil:
        absent = [s["id"] for s in scenes if not re.search(rf"\b{re.escape(fil)}\b", s.get("elements", ""))]
        if len(absent) > max(2, len(scenes) // 4):
            alerts.append(f"objet du fil « {fil} » absent des éléments de {len(absent)} scènes ({', '.join(absent)}) : "
                          f"le fil conducteur doit rester visible")

    news = sb.get("entites_nouvelles") or []
    if len(news) > 3:
        alerts.append(f"{len(news)} entités nouvelles (au plus 3, simples)")

    # Idées-clés principales : au moins une par point et pour la chute (segments du script, temps de words.json).
    try:
        script = next(x for x in json.loads((root / "scripts" / "scripts.json").read_text(encoding="utf-8"))
                      if x["id"] == a.id)
        words = json.loads((root / "build" / a.id / "words.json").read_text(encoding="utf-8"))["words"]
    except (StopIteration, OSError, KeyError):
        script, words = None, None
    cta = next((s["texte"] for s in (script or {}).get("segments", []) if s["partie"] == "cta"), None)
    flat = lambda t: re.sub(r"\s+", " ", unicodedata.normalize("NFC", t).replace(" ", " ")).strip()
    if cta and scenes and flat(scenes[-1].get("texte", "")) != flat(cta):
        alerts.append(f"dernière scène ({scenes[-1]['id']}) ≠ la phrase d'appel seule (« {cta} ») : la QA ne dispense que "
                      f"la dernière scène (carte de fin) du contrôle d'image figée")
    idees = sb.get("idees_cles") or []
    if script and words and idees:
        by_id = {s["id"]: s for s in scenes}
        for k, seg in enumerate(script.get("segments", [])):
            if seg["partie"] not in MAIN_SEGMENTS:
                continue
            ws = [w for w in words if w.get("segment") == k]
            if not ws:
                continue
            a0, a1 = ws[0]["start"], ws[-1]["end"]
            cover = [i for i in idees if i.get("principale")
                     and any((sc := by_id.get(x)) and sc["t_start"] < a1 and sc["t_end"] > a0 for x in i.get("scenes", []))]
            if not cover:
                alerts.append(f"segment {seg['partie']} ({a0:.2f}-{a1:.2f} s) sans idée-clé « principale » : le contrôle "
                              f"sans son ne saura pas qu'elle est essentielle")

    for m in alerts:
        print(f"  ! {m}")
    for m in errors:
        print(f"  ✘ {m}")
    n = len(scenes)
    print(f"{a.id} : contrôles complémentaires {'REFUSÉS' if errors else 'OK'} ({n} scènes, {len(beats)} temps forts, "
          f"{len(alerts)} alerte(s))")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
