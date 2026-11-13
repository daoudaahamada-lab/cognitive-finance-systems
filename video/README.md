# Vidéo Agentic Wealth : « On audite un cabinet de gestion de patrimoine »

Vidéo pédagogique française (simulation) : un cabinet fictif, Horizon Patrimoine, est audité puis trois agents
sont mis en situation, avec un CGP qui vérifie, décide et autorise chaque envoi. Les images, le montage et les
sous-titres sont produits localement ; la voix off est générée avec ElevenLabs (voix « Bastien »), avec une voix
locale gratuite (Piper) en solution de repli.

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
tools/eleven_align.py   Voix ElevenLabs (build/eleven/<scène>.mp3) alignée mot à mot par Whisper : timeline, SRT, texte définitif
tools/tts.py            Repli : voix Piper locale, même format de sortie (VOICE=piper ./build.sh)
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
Voix ElevenLabs : les 11 MP3 (un par scène, voix « Bastien », modèle `eleven_multilingual_v2`) sont placés dans
`build/eleven/` sous le nom de la scène (`hook.mp3`, `title.mp3`, `cabinet.mp3`, …). Le texte envoyé est exactement
celui des beats de chaque scène, séparés par une ligne vide (fichiers `build/eleven/<scène>.txt`). Ils restent aussi
disponibles dans le flow ElevenLabs « Agentic Wealth : voix off audit CGP (Bastien) ».

Repli Piper : modèle de voix (non versionné, 63 Mo) à placer dans `models/` :

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

- Voix : ElevenLabs, voix de bibliothèque « Bastien - Calm & Clear French Teacher » (vérifier les conditions
  d'usage commercial de votre abonnement ElevenLabs). Repli : Piper `fr_FR-siwis-medium` (CC BY 4.0).
- Police : Inter (SIL Open Font License).
- Nappe musicale : générée par `tools/mix_audio.py` (aucun échantillon tiers).
- Identité : wordmark texte « Agentic Wealth » ; aucun logo officiel n'existait dans le projet, aucun n'a été inventé.

## Avertissement

Cabinet, personnes, dossiers, volumes, note sur 100, heures et montants sont fictifs et illustratifs. Les gains
sont des hypothèses à mesurer, pas des résultats observés chez un client. Les mentions réglementaires (AMF, CNIL,
vigilance) sont des repères généraux à faire valider par une personne compétente avant toute publication.
