# Vidéo Agentic Wealth : « On audite un cabinet de gestion de patrimoine »

Vidéo pédagogique française (simulation) : un cabinet fictif, Horizon Patrimoine, est audité puis trois agents
sont mis en situation, avec un CGP qui vérifie, décide et autorise chaque envoi. Tout est produit localement,
sans service payant.

## Livrables (dossier `dist/`)

| Fichier | Contenu |
|---|---|
| `agentic-wealth_audit-cgp_fr.mp4` | Vidéo finale 1920×1080, 25 i/s, H.264 + AAC, sous-titres incrustés (non versionnée : voir `build.sh`) |
| `agentic-wealth_audit-cgp.fr.srt` | Sous-titres français synchronisés (générés depuis la timeline de la voix) |
| `voix_off_texte_definitif.txt` | Texte définitif prononcé, par scène |
| `conducteur.md` | Conducteur scène par scène : durées mesurées, texte prononcé, visuel, animation, texte à l'écran, transition |
| `rapport_controle.md` | Rapport de contrôle (durée, résolution, audio, mots, calculs, points à valider) |

## Structure du projet

```
script/script.py        Source unique du texte : scènes, beats (ancres temporelles), pauses
tools/pronunciation.py  Ajustements phonétiques pour la synthèse (n'affecte pas les sous-titres)
tools/tts.py            Voix Piper locale, timeline, SRT, texte définitif (meilleure prise via Whisper local pour les mots difficiles)
tools/mix_audio.py      Mixage voix + nappe originale générée par calcul, normalisation -16 LUFS
tools/render.js         Rendu image par image (Playwright/Chromium -> ffmpeg), en parallèle
tools/preview.js        Captures de contrôle à un instant ou une ancre : node tools/preview.js DOSSIER p_7+2 120
tools/conducteur.py     Génère dist/conducteur.md
web/                    Scènes HTML/CSS animées par le temps (engine.js + scenes1..4.js), police Inter
build.sh                Chaîne complète
```

Les animations ne dépendent que du temps `t` : chaque élément déclare son ancre (`data-in="p_7@2+0.5"` =
0,5 s après le début de la 3e phrase du beat `p_7`). Modifier le texte puis relancer `build.sh` resynchronise
automatiquement images, voix et sous-titres.

## Reconstruire

Prérequis : Python 3, Node 18+, ffmpeg, Playwright avec Chromium, `pip install piper-tts faster-whisper numpy`.
Modèle de voix (non versionné, 63 Mo) à placer dans `models/` :

```bash
curl -L -o models/fr_FR-siwis-medium.onnx https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx
```

```bash
curl -L -o models/fr_FR-siwis-medium.onnx.json https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json
```

```bash
./build.sh
```

Le contrôle d'intelligibilité utilise le modèle Whisper « small » (téléchargé automatiquement depuis Hugging Face).

## Licences et crédits

- Voix : Piper, voix `fr_FR-siwis-medium`, entraînée sur le corpus SIWIS (licence CC BY 4.0) : attribution
  affichée sur le carton final.
- Police : Inter (SIL Open Font License).
- Nappe musicale : générée par `tools/mix_audio.py` (aucun échantillon tiers).
- Identité : wordmark texte « Agentic Wealth » ; aucun logo officiel n'existait dans le projet, aucun n'a été inventé.

## Avertissement

Cabinet, personnes, dossiers, volumes, note sur 100, heures et montants sont fictifs et illustratifs. Les gains
sont des hypothèses à mesurer, pas des résultats observés chez un client. Les mentions réglementaires (AMF, CNIL,
vigilance) sont des repères généraux à faire valider par une personne compétente avant toute publication.
