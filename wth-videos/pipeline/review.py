"""scripts/scripts_revue.md : version lisible des scripts pour validation humaine."""
from datetime import date

from .common import ROOT, load_scripts

LABELS = {"accroche": "Accroche", "contexte": "Contexte", "point1": "Point 1", "point2": "Point 2",
          "point3": "Point 3", "chute": "Chute", "cta": "CTA"}
WORDS_PER_SECOND = 2.7  # débit moyen observé pour eleven_multilingual_v2 en français, à confirmer sur V01-V02


def review():
    lines = ["# Scripts vidéo WealthTech Horizon — revue", "",
             "Durée estimée à 2,7 mots/s ; la durée réelle est mesurée par le contrôle qualité après génération.", ""]
    for vid, s in sorted(load_scripts().items()):
        d = date.fromisoformat(s["date"]).strftime("%d/%m/%Y")
        lines += [f"## {vid} — {s['titre']}", "",
                  f"Source **{s['source']}** · publication **{d} à 17:00** · {s['mots']} mots · "
                  f"≈ {s['mots'] / WORDS_PER_SECOND:.0f} s", "",
                  "| Partie | Slides | Texte |", "|---|---|---|"]
        for g in s["segments"]:
            lines.append(f"| {LABELS[g['partie']]} | {', '.join(map(str, g['slides']))} | {g['texte']} |")
        lines += ["", "**Légende**", ""] + [f"> {l}" if l else ">" for l in s["legende"].split("\n")]
        lines += ["", f"**Hashtags** : {' '.join(s['hashtags'])}", ""]
        if s.get("notes_prononciation"):
            lines += ["<details><summary>Points de prononciation à vérifier</summary>", "",
                      s["notes_prononciation"], "", "</details>", ""]
    out = ROOT / "scripts" / "scripts_revue.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    review()
