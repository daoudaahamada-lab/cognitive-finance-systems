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
| `make motion ID=V01` | rendu motion design (Remotion) sur la voix existante → `output/WTH-V01.mp4` → contrôle qualité (voir plus bas) |
| `make story ID=V07` | film « Story » (méthode validée) sur la voix existante → `output/WTH-V07.mp4` + version sans sous-titres → contrôle qualité (voir plus bas) |
| `make lock ID=V07` | verrouille la voix validée : elle ne sera plus jamais régénérée |
| `make upload ID=V07` | upload sur Cloudinary `WTH-V2/videos/WTH-V07` (refusé si le contrôle qualité échoue) |
| `make planning` | écrit `output/planning_videos.csv` |
| `make all`, `make publish` | toutes les vidéos de `IDS` (par défaut V01 à V15) |
| `python3 -m tests.smoke [--slides]` | test hors ligne du montage et du contrôle qualité avec une voix factice |
| `python3 -m tests.story_smoke [--qa]` | test sans rendu de l'outillage Story (props, storyboard, garde-fous ; `--qa` : contrôles image sur l'extrait validé) |

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

## Motion design (`make motion`)

Direction « Noir galerie » : fond #0A0A0B et grille fixe de 36 px, illustrations en verre (`assets/illustrations/`)
avec leur halo, sous-titres karaoké Inter ExtraBold 66 px (mot prononcé en #FF4A5C), éléments graphiques dessinés
en code. Grammaire : tout reste immobile puis part sur le début d'un mot, dès l'image du mot (entrées 0,7 → 1 en
330 ms, ease-out cubique ; déplacements 530 ms ease-in-out ; passage d'un objet au suivant sans coupe ni scène vide
ni fondu enchaîné : l'entrant, opaque dès sa 1re image, grandit par-dessus le sortant qui rétrécit et s'efface en
4,5 images, si bien qu'on ne le voit jamais à travers l'entrant). Un seul rouge plein pour tous les aplats ; le corail #FF4A5C ne sert qu'au mot
prononcé et aux traits fins (anneaux, crochets, ligne de lecture, repère). Le rouge plein est le rouge de marque
#C8102E éclairci pour l'écran noir (#DC1835 : 4 : 1 sur le fond, texte crème à 4,4 : 1).

- Prérequis : Node 22 et `make motion-setup` (`npm ci` dans `motion/`). Le navigateur est le headless shell
  Playwright déjà installé : son chemin par défaut est écrit à un seul endroit, `motion/browser.json` (lu par
  `remotion.config.ts`, `scripts/stills.mjs` et `pipeline/motion.py`), et `REMOTION_BROWSER_EXECUTABLE` a priorité ;
  s'il n'existe pas, `make motion` s'arrête tout de suite avec un message clair.
- Licence Remotion : gratuite pour les particuliers et les entreprises de 3 personnes au plus ; au-delà, une licence
  entreprise est nécessaire (le MP4 porte le commentaire « Made with Remotion »). À confirmer avant de publier la série.
- Entrées : `scripts/shotlists/Vxx.json` (plans et événements calés sur des mots du script : `"at": "validé"`),
  `build/Vxx/words.json` et `tts.json` (vérifiés avant tout), `build/Vxx/audio.wav` (refait par `normalize_audio`
  s'il manque). La voix n'est jamais régénérée.
- `pipeline/motion.py` prépare chaque illustration (halo reconstruit dans une marge transparente de 100 px et intégré
  à l'image, sans rectangle, jamais agrandie au-delà de sa résolution) et le fond dans `motion/public/generated/Vxx/`,
  découpe les sous-titres (2-3 mots, 4 au plus, coupés aux ponctuations et aux silences > 0,15 s, jamais sur une
  préposition ou un article quand c'est évitable, toujours un groupe affiché), écrit les props `build/Vxx/motion.json`,
  rend la vidéo muette (images PNG, CRF 15, images clés forcées au début de chaque plan) avec la composition Remotion
  `Explainer`, puis y mixe `audio.wav` (AAC 192 kb/s, 48 kHz, départ à 0).
- Plan de tournage : chaque plan a `scale` et `center` (centre de l'objet à l'écran, px) ou `focus` ; `move`, `tilt`,
  `tone`, `shake` animent le héros ; `pill`, `badge`, `chips`, `dots`, `ring`, `sector`… sont les éléments dessinés
  (types inconnus et événements hors de leur plan refusés). Le cadrage est vérifié à chaque image : l'objet opaque reste
  au-dessus de y = 1140 (sinon l'échelle est réduite, avec un avertissement) et les débordements dans la colonne
  d'icônes (x > 940) sont signalés. Une entrée `{"chapter": N}` est une carte de chapitre : le héros précédent
  rétrécit vers la place du protagoniste rouge pendant que la rangée des étapes grandit au centre ; au plan suivant
  la rangée s'efface sur place derrière le héros et un rappel apparaît en haut. `captions.groups` impose des
  découpes de sous-titres (expressions figées). Le premier plan commence à l'image 0.
- Règles vérifiées avant le rendu (pour les 15 vidéos) : une vidéo n'utilise que les illustrations de son propre
  carrousel (`WTH-<source>-xx`, `source` de scripts.json) et les génériques ; typographie des étiquettes
  (« 9 h » avec espace fine insécable, symboles d'unité jamais en capitales : « 10 min ») ; illustration source
  sans vraie transparence refusée.
- `make motion-props ID=V01` : seulement assets + props ; `make motion-review ID=V01` : planche contact du MP4
  (`build/V01/review/contact.png`) ; `python3 -m pipeline.motion V01 --stills 120 380` : images fixes PNG sans rendu
  complet (`build/V01/review/stills/`). `motion.json` n'est réécrit que si son contenu change : une image fixe ou
  `--props` après le rendu ne périme pas la QA.
- Le mixage écrit dans le MP4 les balises `wth_mode`, `wth_props` et `wth_shotlist` (empreintes SHA-1 de
  `motion.json` et du plan) et la fiche `build/Vxx/motion_render.json` (mêmes empreintes + celle du MP4).
- Pour une nouvelle vidéo : écrire `scripts/shotlists/Vxx.json` sur le modèle de V01, puis `make motion ID=Vxx`.
  Le code Remotion (`motion/src/explainer/`) ne change pas.
- `make video` (montage classique) refuse d'écraser un `output/WTH-Vxx.mp4` rendu en motion (commentaire
  « Made with Remotion »), sauf `FORCE=1` ; `make all` passe par `make motion` pour les vidéos qui ont un plan de tournage.

## Story (méthode validée)

Méthode retenue pour les 15 films, validée sur un extrait de V01 (S11-S14, `make story ID=V01 FROM=25.612 TO=41.309`,
copie de référence dans `build/V01/baseline/`). Fond ivoire quadrillé, encre, un seul accent cyan, rouge d'alerte ; un
fil conducteur suivi d'un bout à l'autre ; chaque scène = état initial → action visible → résultat, calée sur les
débuts de mots de la voix ; lisible sans le son. Le film est un graphe de scène : des entités persistantes (composition
Remotion `Story`, `motion/src/story/`) dont les pistes sont posées image par image par `pipeline/story.py`.

- **Entrées** : la voix (`build/Vxx/tts.json`, `words.json` ; `build/Vxx/audio.wav` est refait par
  `motion.ensure_audio` s'il manque ou si la voix en cache est plus récente) ; le storyboard
  `scripts/storyboards/Vxx.json` (+ `.md`) : scènes contiguës, temps forts `{t, mot, evenement}` sur des débuts de
  mots, `idees_cles` (6 à 10 `{id, idee, scenes}`, notées par le contrôle sans son), `objet_fil` ; la mise en scène
  `scripts/story/Vxx.py` ou le paquet `scripts/story/Vxx/__init__.py` (+ parties `p1.py`… écrites en parallèle,
  importées en relatif), qui définit `build(story)` avec l'API `Story` (`add`, `set`, `key`, `keys`, `path`, `fly`,
  `along_wire`, `beat`, `word`, `word_after`, `png`…) et, au besoin, `CAPTION_GROUPS`, `ALERT_WORDS`, `ACOUSTIC_SNAP`.
  La géométrie partagée avec le rendu (figurine, stylo, tampon…) est dans `motion/src/story/geometry.json`
  (`pipeline.story.GEOM`). Illustrations : celles du carrousel de la vidéo (`WTH-<source>-xx`) et les génériques.
- **Commandes** :

  | Commande | Effet |
  |---|---|
  | `make voice ID=V07` | `tts` (voix en cache, aucun appel) + `words` + `audio.wav` normalisé |
  | `make storyboard-check ID=V07` | contrôle du storyboard : champs, scènes contiguës de 0 à la fin du dernier mot, débuts de scène et temps forts sur un début de mot (± 30 ms), textes des scènes = texte du script (NFC), idées-clés |
  | `make story-props ID=V07` | props du film sans rendu ; `FROM=… TO=…` pour un extrait ; `ALLOW_PARTIAL=1` admet une mise en scène incomplète |
  | `make story-stills ID=V07 FRAMES="0 120"` | images fixes PNG (numéros d'image de la vidéo rendue) → `build/V07/story/stills/` |
  | `make story ID=V07` | film entier (avec et sans sous-titres) puis `make qa` |
  | `make story ID=V01 FROM=25.612 TO=41.309` | extrait → `output/extraits/WTH-V01_extrait_S11-S14.mp4` (pas de QA) |
  | `make review-sheets ID=V07` | sorties de revue (`REVIEW="--nocap --sheets"` pour choisir) |
  | `make story-check` | parité Python / TypeScript (`tests.story_parity`) + `tsc --noEmit` |
  | `make films` | `make story` pour chaque vidéo de `IDS` qui a une mise en scène ; `make all` passe aussi par Story pour elles |
  | `make clean-tmp` | dossiers temporaires de Remotion (si aucun rendu ne tourne) et images de revue (garde les planches) |

- **Film entier** : refusé si une scène du storyboard n'a aucun temps fort mis en scène, si un temps fort n'a pas
  d'événement ou si le début n'est pas mis en scène (`--allow-partial` / `ALLOW_PARTIAL=1` pour un rendu de travail).
  Sorties : `build/Vxx/story/props_film.json`, `props_film_nocap.json`, `muet_film*.mp4`,
  `film_sans_sous_titres.mp4`, et **`output/WTH-Vxx.mp4`** (le nom que lisent `qa`, `upload` et `planning`). Un
  `output/WTH-Vxx.mp4` d'un autre rendu (classique, motion) est d'abord rangé dans `build/Vxx/archive/`. Le mixage
  écrit les balises `wth_mode=story`, `wth_props`, `wth_storyboard`, `wth_spec` (SHA-1 ; pour un paquet, de ses
  fichiers mis bout à bout) et la fiche `build/Vxx/story_render.json` (chemins et empreintes des props, du storyboard,
  de la mise en scène, des deux MP4, nombre d'images). `make video` et `make motion` n'écrasent jamais un film Story,
  sauf `FORCE=1`.
- **Sous-titres** : découpés sur tout le texte puis coupés à la fenêtre : un extrait montre les groupes du film (un
  groupe entamé avant la fenêtre n'en garde que les mots de la fenêtre). Inter Bold 64 px, mot prononcé en cyan
  profond, mots d'alerte en rouge.
- **Un seul rendu Remotion à la fois** (machine à 4 cœurs) : rendus et images fixes prennent le verrou
  `build/.render.lock` (attendu s'il est pris) et travaillent dans leur propre dossier temporaire, supprimé à la fin
  (bundles `remotion-webpack-bundle-*`, profils Chrome).
- **Revue** (`python3 -m pipeline.story_review Vxx [--nocap|--src <mp4>] [--sheets] [--beats] [--phone] [--holds]`,
  tout par défaut) → `build/Vxx/review/<film|Sa-Sb>[_nocap]/` : planches à 6 i/s en JPEG mi-résolution, 12 images par
  planche avec image, temps et scène ; une bande par temps fort (f−3 à f+12) ; taille téléphone (réencodage à 2 Mb/s
  puis 360 px de large, planches et vidéo) ; rapport des tenues (`holds.json`). Les relecteurs utilisent ces sorties
  au lieu d'extraire des images pleine résolution ; `--clean` (ou `make clean-tmp`) ne garde que planches et rapports.
- **QA en mode story** (`make qa`, mode lu dans la balise `wth_mode=story` avant le commentaire « Made with
  Remotion ») : contrôles communs (durée, format H.264 BT.709 plage tv, synchro, mots coupés, accents et orthographe
  des textes affichés par les entités, loudness, true peak) avec les props de `story_render.json` (largeur mesurée en
  Inter Bold 64 px, ≤ 760 px), plus « Rendu Story à jour » (empreintes du rendu = props, storyboard et mise en scène
  actuels, même nombre d'images que les props, version sans sous-titres du même rendu) et, sur les images décodées :
  surbrillance qui change à l'image exacte de chaque mot (cyan et rouge), zones réservées vides sur la version sans
  sous-titres (160 px du haut, 380 px du bas, x > 940), aucune image figée plus de 3,5 s hors carte de fin, version
  sans sous-titres identique au-dessus de y = 1270 (PSNR ≥ 40 dB, même nombre d'images), bande d'action jamais vide.
- **Skills** (`.claude/skills/` à la racine du dépôt) : `wth-video` (une vidéo ou la série de bout en bout : voix par
  le connecteur ElevenLabs, storyboard, mise en scène, revues, QA, livraison), `wth-storyboard` (méthode A : le
  storyboard et son test sans son), `wth-story-build` (méthodes B et C : mise en scène, rendu, revues, contrôle sans
  son, QA). `/wth-video V07` lance tout ; l'état de chaque vidéo est dans `scripts/production_status.json`.

## Contrôle qualité (`output/qa_report.md`)

Durée 45–60 s ; synchro sous-titres < 150 ms (alignement, arrondi à l'image et décalage de la piste audio
du MP4 mesuré par corrélation) ; aucun mot coupé (tous les mots, entiers, dans la largeur, fin d'audio
non tronquée) ; accents (NFC, glyphes présents, pas de mojibake, mots hors dictionnaire signalés) ;
pas de saturation (true peak ≤ −1 dBTP, aucun échantillon écrêté) ; loudness −14 ± 1 LUFS.
Le mode est lu dans le MP4 lui-même (balise `wth_mode`, commentaire « Made with Remotion », ou fiche
`motion_render.json` dont l'empreinte est celle du MP4) : un rendu motion est contrôlé avec `build/Vxx/motion.json`
(largeur mesurée avec la police et la taille réelles du rendu, aucune image sans sous-titre, même nombre d'images que
motion.json, empreintes du rendu = `motion.json` et plan actuels, BT.709 plage tv, orthographe des étiquettes) et sur
les images décodées du MP4 : scène jamais vide pendant les passages et les cartes de chapitre (≥ 3 % de pixels
allumés dans la bande visuelle), pas de creux de luminance aux passages, rangée d'étapes qui ne traverse jamais le
héros entrant, mot rouge du karaoké qui change exactement à l'image du début de chaque mot. Un film Story (balise
`wth_mode=story`) est contrôlé en mode story (section précédente). Un montage classique est contrôlé avec
`subs.ass` (forcer avec `python3 -m pipeline.qa Vxx --mode story|motion|classic`).
