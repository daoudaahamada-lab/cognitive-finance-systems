"""Vérifie scripts/scripts.json contre les règles éditoriales et le carrousel source."""
import argparse
import re
import sys

from .common import CAROUSELS, load_scripts, read_json

CTA = "Abonne-toi pour comprendre ton argent."
# Structure validée le 21/10 : la problématique d'abord, puis l'annonce (« dans cette vidéo, on va voir comment… »),
# le contexte, trois points qui s'ouvrent chacun sur une phrase de contexte (transition), la chute et l'appel.
PARTIES = ["accroche", "annonce", "contexte", "point1", "point2", "point3", "chute", "cta"]
MOTS_MIN, MOTS_MAX = 180, 280          # plus de limite à 60 s : on prend le temps d'expliquer
PHRASE_MAX = 18
FORBIDDEN = [
    (re.compile(r"\bRDV\b", re.I), "abréviation « RDV »"),
    (re.compile(r"\b\d+\s?h\d*\b", re.I), "heure abrégée"),
    (re.compile(r"[/()\[\]≠−=+*#@<>≈•]"), "symbole non lisible à l’oral"),
    (re.compile(r"(?<![\w-])(vous|votre|vos)\b", re.I), "vouvoiement (hors « rendez-vous »)"),
    (re.compile(r"\b(slides?|carrousels?|glisse|swipe|ce post)\b", re.I), "référence au carrousel"),
]


def count_words(text):
    return len([w for w in text.split() if re.search(r"\w", w)])


def sentences(text):
    return [s for s in re.split(r"(?<=[.!?…])[ \n]+", text) if s.strip()]


def numbers(text):
    return {re.sub(r"[\s  ]", "", n) for n in re.findall(r"\d+(?:[   ]\d{3}(?!\d))*(?:,\d+)?", text)}


def source_text(source):
    c = read_json(CAROUSELS / f"{source}.json")
    return "\n".join(f"{s['titre']}\n{s['texte']}" for s in c["slides"]) + "\n" + c["legende"]


def lint(s):
    errors = []
    text = s["texte"]
    order = [g["partie"] for g in s["segments"]]
    if order != PARTIES:
        errors.append(f"segments {order}")
    if " ".join(g["texte"] for g in s["segments"]) != text:
        errors.append("texte différent de la concaténation des segments")
    seg = {g["partie"]: g for g in s["segments"]}
    if seg.get("cta", {}).get("texte") != CTA:
        errors.append("CTA inexact")
    n = count_words(text)
    if not MOTS_MIN <= n <= MOTS_MAX:
        errors.append(f"{n} mots ({MOTS_MIN} à {MOTS_MAX})")
    if count_words(seg["accroche"]["texte"]) > 20:
        errors.append("accroche > 20 mots")
    if "vidéo" not in seg.get("annonce", {}).get("texte", ""):
        errors.append("annonce : doit dire ce que la vidéo va montrer (« dans cette vidéo… »)")
    for sent in sentences(text):
        if count_words(sent) > PHRASE_MAX:
            errors.append(f"phrase de {count_words(sent)} mots : {sent}")
    for rx, label in FORBIDDEN:
        if rx.search(text):
            errors.append(label)
    src = numbers(source_text(s["source"]))
    for field in ("texte", "titre", "legende"):
        for num in numbers(s[field]) - src:
            errors.append(f"{field} : nombre {num} absent de la source")
    if len(s["titre"]) > 45:
        errors.append("titre > 45 caractères")
    return errors


def main():
    p = argparse.ArgumentParser()
    p.add_argument("ids", nargs="*")
    args = p.parse_args()
    scripts = load_scripts()
    failed = False
    for vid in args.ids or sorted(scripts):
        errs = lint(scripts[vid])
        print(f"{vid} ({scripts[vid]['source']}, {count_words(scripts[vid]['texte'])} mots) : "
              f"{'OK' if not errs else 'ÉCHEC'}")
        for e in errs:
            print(f"  - {e}")
        failed |= bool(errs)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
