# Environnement : la machine, les accès, les illustrations, le ménage

À lire au démarrage d'une session neuve, quand `preflight.py` signale un manque, quand une illustration est absente
ou quand le disque se remplit.

## La machine et ses limites

| Ressource | Limite | Conséquence |
|---|---|---|
| Processeurs | 4 | Le moteur de workflows ne fait tourner que 2 agents à la fois par workflow (min(16, CPU − 2)). Un storyboard (≈ 11 agents) prend 70 à 90 min ; un film 4 h 30 à 7 h. |
| Rendus Remotion | 1 à la fois | Le verrou `wth-videos/build/.render.lock` est pris par `make story`, `story-stills` et `motion`. Un second rendu attend. Ne supprime jamais ce fichier ; ne lance jamais `npx remotion` à la main, il n'attendrait pas. |
| Disque | ≥ 4 Go libres | Un film de 58 s fait 1 750 images : des images pleine résolution extraites par des relecteurs ont rempli le disque pendant V01. Les relecteurs lisent les planches JPEG de `make review-sheets`. |
| Générations ElevenLabs | 1 à la fois | limite de concurrence du connecteur, et crédits (`voice-elevenlabs-mcp.md`) |

Pour voir l'occupation : `df -h /home/user/cognitive-finance-systems`.

## `preflight.py` : ce qu'il vérifie

```bash
python3 .claude/skills/wth-video/scripts/preflight.py V07 [V08 …] [--json] [--no-voice] [--no-clean]
```

- **Environnement**
  - `motion/node_modules` (Remotion) ;
  - le navigateur de rendu ;
  - les outils `ffmpeg`, `ffprobe`, `node`, `npx`, `git` ;
  - les modules Python du pipeline ;
  - le disque. Sous 4 Go, il lance `make clean-tmp` lui-même puis remesure, sauf avec `--no-clean` ;
  - un rendu en cours.
- **Par vidéo**
  - le script, présent dans `scripts/scripts.json` et dans `config/videos.csv`, avec le même carrousel ;
  - les illustrations du manifeste pour **son** carrousel et les génériques : présentes, et de la bonne taille ;
  - la voix : en cache, versionnée, sous la limite de durée, préparée (`tts.json`, `words.json`, `audio.wav`) ;
  - pour information : le storyboard (`--check`), la mise en scène et une QA existante.

Chaque ✘ donne la commande qui répare. Le script sort en code 1 tant qu'il reste un ✘. `--no-voice` change une voix
absente en simple alerte, pour préparer la recette voix.

## Accès réseau : passer par les connecteurs

| Service | Accès direct depuis la machine | Voie utilisée |
|---|---|---|
| API ElevenLabs | non | connecteur MCP ElevenLabs (`creative_*`) |
| `storage.googleapis.com` (prises, transcriptions Scribe) | oui (`curl`) | téléchargement direct des `content_url` |
| Google Drive (illustrations, MP4 déposés) | non | connecteur Google Drive (`download_file_content`, `search_files`) |
| API Cloudinary | non | connecteur Cloudinary (`upload-asset` depuis une URL) |
| Metricool | non | connecteur Metricool |
| GitHub (`git push`) | oui | `git push -u origin HEAD` |

Le HTTPS sortant passe par un proxy préconfiguré. En cas d'erreur TLS ou 403 du proxy, lis `/root/.ccr/README.md` ;
ne désactive jamais la vérification TLS.

## Session ou machine neuve

1. `cd wth-videos && make setup` (modules Python) et `make motion-setup` (`npm ci` dans `motion/`).
2. **Navigateur de rendu.** Son chemin est dans `motion/browser.json` (`executable`), lu par `remotion.config.ts`,
   `scripts/stills.mjs` et `pipeline/motion.py`. `REMOTION_BROWSER_EXECUTABLE` a priorité. Sur la machine
   actuelle, c'est le headless shell de Playwright déjà installé sous `/opt/pw-browsers/`. Ailleurs, installe un
   Chromium headless et mets son chemin dans `motion/browser.json`.
3. Illustrations : section suivante.
4. `python3 .claude/skills/wth-video/scripts/status.py show`, puis `status.py next`.

## Illustrations depuis le Drive

`wth-videos/assets/illustrations/*.png` n'est pas versionné : environ 2 Mo par fichier, et elles restent sur le
Drive. `wth-videos/data/illustrations_manifest.tsv` donne, pour chaque fichier, son identifiant Drive et sa taille
exacte.

Règle de la série, appliquée par le code (`Story.png` refuse le reste) : une vidéo n'utilise que **les illustrations
de son carrousel** (`WTH-<source>-xx`, où `source` vient de `scripts.json`) **et les 20 génériques**. Ne télécharge
que celles-là.

| Jeu au manifeste | Vidéo |
|---|---|
| WTH-003 (01-09) | V01 |
| WTH-002 (01-09) | V02 |
| WTH-006 (02-08) | V04 |
| WTH-004 (01-09) | V08 |
| 20 génériques (AI, BELL, BOOK, BUOY, CRADLE, CRYSTAL, FINGERPRINT, GEAR, GLOBE, HEART, PRINTER, RINGS, SHOES, SUITCASE, TAG, TARGET, TOKEN, TREE, TRUCK, WAVE) | toutes |

Les autres vidéos n'ont pas de jeu dédié : génériques et code seulement, et c'est la norme de la référence. Des jeux
WTH-005 et WTH-007 existent aussi, mais aucune des 15 vidéos n'a ces carrousels pour source.

Téléchargement d'un fichier :
1. Appelle `download_file_content` du connecteur Google Drive avec `fileId` = `drive_id` du manifeste.
2. Le résultat (≈ 1,8 Mo de base64) dépasse la taille d'un résultat d'outil. Le harnais l'enregistre dans un fichier
   et donne son chemin (« Output has been saved to … »). Ne lis pas ce fichier et n'affiche pas la base64 : elle
   remplirait le contexte.
3. Décode-le :
   ```bash
   python3 -I .claude/skills/wth-video/scripts/drive_decode.py <fichier enregistré> WTH-004-03.png
   ```
   Le script extrait la base64 (objet `{content, id, mimeType, title}`, éventuellement enveloppé) et vérifie la
   signature PNG. Il n'écrit `wth-videos/assets/illustrations/<nom>` que si la taille est celle du manifeste.
4. Un fichier à la fois. Relance `preflight.py Vxx` à la fin.

## Ménage du disque

| Quand | Commande (dans `wth-videos/`) | Ce qui part |
|---|---|---|
| après chaque rendu | `make clean-tmp` | dossiers temporaires de Remotion (bundles, profils Chrome), supprimés en tenant le verrou de rendu |
| vidéo terminée | `make clean-tmp ID=Vxx` | images de travail de revue de Vxx (bandes, images téléphone, images extraites) ; les planches restent |
| vidéo terminée | `rm -f build/Vxx/story/stills/*.png build/Vxx/story/muet_*.mp4` | images fixes et vidéos muettes intermédiaires |
| voix validée et verrouillée | `rm -f build/Vxx/voice/take-*.mp3` | prises non retenues (la voix retenue est dans `cache/tts`) |

Ne supprime pas `output/WTH-Vxx.mp4`, `build/Vxx/story/film_sans_sous_titres.mp4`, `build/Vxx/story_render.json`
ni les props tant que la vidéo n'est pas publiée : la QA (« Rendu Story à jour ») et la livraison s'en servent.

## Git

- Branche de travail : `claude/wth-video-pipeline`. Pousse avec `git push -u origin HEAD`. En cas d'erreur réseau,
  réessaie jusqu'à 4 fois en attendant 2, 4, 8 puis 16 s.
- Termine chaque message de commit par les lignes d'attribution que donne la session.
- Jamais de MP4, ni de `build/`, ni d'illustrations : ils sont ignorés par git, ne force pas leur ajout. Le dépôt est
  public, donc jamais d'image de la vidéo de référence d'un tiers (`data/reference/` est ignoré).

## Workflows

- Lance-les depuis la session principale :
  `Workflow({scriptPath: "<dépôt>/.claude/skills/<skill>/workflows/<nom>.wf.js", args: {...}})`. Un workflow
  lancé par un autre ne peut pas en lancer un troisième : l'imbrication s'arrête à un niveau.
- Les modèles ne lisent pas de fichiers : tout passe par `args` (`id`, `root` = chemin absolu de `wth-videos`, …).
  Ce sont leurs agents qui lisent le dépôt.
- Reprise après une interruption : relance le même `scriptPath` avec les mêmes `args` et
  `resumeFromRunId: "<runId>"`. Les agents déjà terminés ne sont pas refaits.
- Après modification d'un modèle :
  `node .claude/skills/wth-storyboard/scripts/check_wf.mjs <fichier.wf.js>`. `node --check` refuse le `return` de
  premier niveau que le moteur admet.

## Licence Remotion

Remotion est gratuit pour un particulier ou une entreprise de 3 personnes au plus ; au-delà, il faut une licence
entreprise. Chaque MP4 porte le commentaire « Made with Remotion ». Pose la question à l'utilisateur avant la
première publication (`references/publishing.md`).
