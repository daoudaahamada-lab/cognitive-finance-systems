# WealthTech Horizon — pipeline vidéo

15 vidéos verticales éducatives tirées des carrousels d'octobre V2 :
script → voix ElevenLabs → sous-titres mot à mot → montage → MP4 → Cloudinary.

## Prérequis

- Python 3.11+, ffmpeg avec libass et libx264 ; `make setup` installe les dépendances Python.
- Variables d'environnement (jamais dans le dépôt) : `ELEVENLABS_API_KEY`, `CLOUDINARY_URL`
  (`cloudinary://CLÉ:SECRET@byfnwwcw`).
- Accès réseau à `api.elevenlabs.io`, `api.cloudinary.com`, `res.cloudinary.com`.

## Utilisation

| Commande | Effet |
|---|---|
| `make extract` | lit `data/WTH_Octobre_V2_Textes_Slides.xlsx` → `data/carousels/WTH-XXX.json` |
| `make lint` | vérifie `scripts/scripts.json` (130–150 mots, CTA, chiffres présents dans la source…) |
| `make voices` | liste les voix françaises et génère un extrait de 10 s pour chaque voix présélectionnée |
| `make assets ID=V02` | télécharge les PNG de carrousel V2 depuis Cloudinary dans `assets/WTH-XXX/` |
| `make import ID=V01 AUDIO=… WORDS=… GEN=…` | si l'API ElevenLabs n'est pas joignable : range dans le cache une voix générée par le connecteur ElevenLabs et ses temps de mots Scribe (même clé de cache que l'endpoint with-timestamps) |
| `make video ID=V07` | voix → mots horodatés → `.ass` → montage → contrôle qualité, pour une vidéo |
| `make lock ID=V07` | verrouille la voix validée : elle ne sera plus jamais régénérée |
| `make upload ID=V07` | upload sur Cloudinary `WTH-V2/videos/WTH-V07` (refusé si le contrôle qualité échoue) |
| `make planning` | écrit `output/planning_videos.csv` |
| `make all`, `make publish` | toutes les vidéos de `IDS` (par défaut V01 à V15) |
| `python3 -m tests.smoke [--slides]` | test hors ligne du montage et du contrôle qualité avec une voix factice |

Chaque étape lit les sorties de la précédente dans `build/Vxx/` et peut être relancée seule
(`make subs ID=V07`, `make render ID=V07`, `make qa ID=V07`).

## Où sont les choses

- `config.yaml` : voix, modèle, couleurs de marque, police, mise en page, cibles audio, seuils qualité.
  Un fichier `assets/brand/brand.yaml` (couleurs, polices) remplace la section `brand`.
- `config/videos.csv` : vidéo → carrousel source → date.
- `scripts/scripts.json` : les 15 scripts (texte, segments calés sur les slides, titre, légende, hashtags).
- `cache/tts/` : audio et alignement ElevenLabs, indexés par hash (texte, voix, modèle, réglages). Versionné.
- `locks/` : vidéos dont la voix est validée.
- `output/` : MP4 (non versionnés), `qa_report.md`, `qa/Vxx.json`, `uploads.json`, `planning_videos.csv`.

## Voix

Chemin normal : `make video` appelle `text-to-speech/{voice}/with-timestamps` (eleven_multilingual_v2) et met
en cache l'audio et l'alignement par caractère. Si l'API n'est pas joignable depuis la machine, la voix est générée
par le connecteur ElevenLabs puis importée avec `make import` : l'alignement vient alors de la transcription Scribe
du même audio, reconstruite caractère par caractère sur le texte exact du script. Le contrôle qualité vérifie dans
les deux cas qu'aucun mot horodaté ne tombe dans une pause réellement mesurée dans l'audio.

## Règles de montage

- 1080×1920, 30 fps, H.264 + AAC, loudness −14 LUFS (true peak −1,5 dBTP).
- Fond : PNG de `assets/WTH-XXX/` si présents (zoom lent, fondus, calés sur les segments du script),
  sinon fond crème avec le titre et « WealthTech Horizon ».
- Sous-titres : 1 à 3 mots, mot prononcé en rouge #C8102E, texte bordeaux #7A0E14, contour crème,
  centrés dans le tiers inférieur, hors des zones masquées par l'interface TikTok.

## Contrôle qualité (`output/qa_report.md`)

Durée 45–60 s ; synchro sous-titres < 150 ms (alignement, arrondi à l'image et décalage de la piste audio
du MP4 mesuré par corrélation) ; aucun mot coupé (tous les mots, entiers, dans la largeur, fin d'audio
non tronquée) ; accents (NFC, glyphes présents, pas de mojibake, mots hors dictionnaire signalés) ;
pas de saturation (true peak ≤ −1 dBTP, aucun échantillon écrêté) ; loudness −14 ± 1 LUFS.
