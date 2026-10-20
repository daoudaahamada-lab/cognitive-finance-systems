---
name: wth-video
description: Produit de bout en bout une ou plusieurs vidéos WealthTech Horizon (V01 à V15 ou nouvelle Vxx) avec la méthode Story validée sur V01 - voix ElevenLabs par le connecteur, storyboard, mise en scène Remotion ivoire et cyan, revues et contrôle sans son, QA, commit, livraison, puis Cloudinary et Metricool avec l'accord de l'utilisateur - et tient l'avancement dans scripts/production_status.json pour reprendre après une coupure. Utilise-le dès qu'on demande de créer, générer, produire, refaire, terminer, reprendre, rendre, livrer, programmer ou publier une ou plusieurs vidéos WTH, ou de générer ou choisir une voix (« génère les 15 vidéos », « fais V07 », « reprends la série », « où en est la production ? », « une vidéo sur l'inflation », « programme les vidéos », « /wth-video V16 »), même sans les mots skill, Story ou Remotion. Pour un storyboard seul ou une retouche de scène, wth-storyboard et wth-story-build suffisent.
---

# wth-video : une vidéo WealthTech Horizon de bout en bout

Ce skill est le chef d'orchestre de la méthode Story. Le métier est dans deux skills frères : `wth-storyboard`
(méthode A : le storyboard et son test sans son) et `wth-story-build` (méthodes B et C : mise en scène, rendu,
revues, contrôle sans son, QA). Celui-ci porte ce qu'ils ne font pas : la voix, le suivi de production, les limites
de la machine, les commits, la livraison et la publication. V01 est l'exemple travaillé : l'utilisateur en a validé
un extrait (« C'est absolument parfait »), et ses défauts restants sont devenus des règles.

Chemins : `wth-videos/…` est relatif à la racine du dépôt (`/home/user/cognitive-finance-systems`). Les commandes
`make` et `python3 -m pipeline…` se lancent depuis `wth-videos/`, les scripts du skill depuis la racine
(`python3 .claude/skills/wth-video/scripts/<script>.py`).

## Ce que tu livres, par vidéo

- `wth-videos/output/WTH-Vxx.mp4` (sous-titres karaoké) et `wth-videos/build/Vxx/story/film_sans_sous_titres.mp4` ;
- le storyboard `scripts/storyboards/Vxx.json` et `.md`, et la mise en scène `scripts/story/Vxx/` ;
- `output/qa/Vxx.json` OK en mode story, et un contrôle sans son réussi ;
- l'entrée de la vidéo à jour dans `scripts/production_status.json`, tout commité et poussé.

Le critère de l'utilisateur, mot pour mot : « en masquant les sous-titres, je dois pouvoir comprendre l’action
principale et percevoir ce qui change ». Ses 7 règles, à relire avant toute décision de mise en scène :
`.claude/skills/wth-storyboard/references/brief-utilisateur.md`.

## Démarrage

1. **Lis la demande.**
   - Identifiants : « V07 », « V03-V15 » ou « V03 à V15 », « les 15 vidéos » (V01 à V15).
   - « Reprends » ou « continue » : la prochaine étape de chaque vidéo, donnée par `status.py next`.
   - « Où en est la production ? » : `status.py show`, sans rien lancer.
   - Une étape de départ (« reprends V07 à la revue », `--from review`) : voix, storyboard, build, review, verify,
     qa, livraison ou publication.
   - Un sujet sans identifiant (« une vidéo sur l'inflation ») : cherche d'abord dans les titres de
     `scripts/scripts.json` (V12 traite déjà l'inflation) ; sinon, section « Nouvelle vidéo ».
2. **Lis le suivi.**
   ```bash
   python3 .claude/skills/wth-video/scripts/status.py init          # crée le fichier ou ajoute les vidéos manquantes
   python3 .claude/skills/wth-video/scripts/status.py show V07      # où en est la vidéo
   python3 .claude/skills/wth-video/scripts/status.py next V07      # prochaine étape et moyen de la faire
   ```
   Le suivi évite de refaire une voix payée ou un storyboard déjà validé. Il permet aussi à une session neuve de
   reprendre sans la conversation. Schéma et états : `references/status-schema.md`.
3. **Contrôle l'environnement.**
   ```bash
   python3 .claude/skills/wth-video/scripts/preflight.py V07 [V08 …]    # --no-voice avant la recette voix
   ```
   Il vérifie Remotion, le navigateur de rendu, ffmpeg, les illustrations du carrousel de la vidéo et les
   génériques, le disque (≥ 4 Go), le script et la voix. Chaque ✘ donne sa commande de réparation. Un manque
   découvert au rendu coûte une heure ; ici, une seconde. Détails : `references/environment.md`.
4. **Regarde les points de validation** (section du même nom). S'il en manque un, dis-le à l'utilisateur et avance
   sur ce qui n'en dépend pas.
   - Demande explicite d'une vidéo V02 à V15 (« /wth-video V06 ») alors que `status.py next` affiche « ⏸ attend la
     validation de V01 » : rappelle le point de validation et propose de finir V01 d'abord (`status.py next V01`).
     En attendant sa réponse, fais seulement ce qui n'en dépend pas (`make voice`, `preflight.py`). Lance le
     storyboard ou le film de V06 seulement s'il confirme, et note-le :
     `status.py checkpoint v01_full_approved pending --note "V06 lancée avant V01 à la demande de l'utilisateur (<date>)"`.

## Les étapes

| # | Étape | Comment | Produit | Ensuite |
|---|---|---|---|---|
| 1 | Voix | `references/voice-elevenlabs-mcp.md` : connecteur, `pick_take.py`, `pipeline.connector`, `make voice` | `cache/tts/<clé>.*`, `build/Vxx/tts.json`, `words.json`, `audio.wav` | commit ; `voice done` |
| 2 | Storyboard | skill `wth-storyboard` : `storyboard.wf.js` (`revise.wf.js` s'il existe déjà) | `scripts/storyboards/Vxx.json` + `.md` | commit ; `storyboard done` ; résumé à l'utilisateur |
| 3 | Mise en scène, rendu, revues | skill `wth-story-build` : `build-review.wf.js` | `scripts/story/Vxx/`, les deux MP4 | — |
| 4 | Contrôle sans son | `mute-verify.wf.js`, lancé par `build-review.wf.js` | score des idées-clés | — |
| 5 | QA | `make qa ID=Vxx`, lancé par `build-review.wf.js` | `output/qa/Vxx.json` | `status.py merge` ; commit ; ménage |
| 6 | Livraison | `references/publishing.md` §1 | MP4 envoyé avec légende et hashtags | `delivered done` |
| 7 | Publication | `references/publishing.md` §2 à 5 | Cloudinary, `uploads.json`, Metricool | **après l'accord sur les dates** ; `published done` |

### 1. Voix

La voix fixe tous les temps du film : les temps forts du storyboard sont des débuts de mots. Elle se fait donc en
premier, une fois pour toutes. Elle coûte des crédits ElevenLabs : environ 3 500 à 4 000 par vidéo, sur un quota de
40 000 par période, déjà épuisé une fois. Donc :
- fais confirmer le solde par l'utilisateur avant chaque lot ;
- une seule génération à la fois ;
- jamais de nouvel appel pour « réessayer » ;
- garde une prise de 59,4 s au plus, ou de la durée de QA approuvée pour la vidéo moins 0,6 s (V03 : QA à 62 s,
  soit une prise ≤ 61,4 s) ;
- si aucune prise ne tient, demande à l'utilisateur plutôt que de régénérer.

Toute la recette, pas à pas : `references/voice-elevenlabs-mcp.md`.

### 2. Storyboard

```
Workflow({scriptPath: "/home/user/cognitive-finance-systems/.claude/skills/wth-storyboard/workflows/storyboard.wf.js",
          args: {id: "V07", root: "/home/user/cognitive-finance-systems/wth-videos"}})
```
Lis d'abord `.claude/skills/wth-storyboard/SKILL.md` : options (`notes`, `overwrite`, `muteRounds`), révision
(`revise.wf.js`), contrôles. Compte 70 à 90 min. Ensuite :
- commite les deux fichiers ;
- `status.py set V07 storyboard done version='"v1 · …"'` ;
- résume le storyboard à l'utilisateur en 3 lignes, avec le chemin du `.md`. C'est le moment où changer d'avis coûte
  le moins. En production en série après l'accord sur V01, n'attends pas sa réponse pour continuer.

### 3 à 5. Le film

```
Workflow({scriptPath: "/home/user/cognitive-finance-systems/.claude/skills/wth-story-build/workflows/build-review.wf.js",
          args: {id: "V07", root: "/home/user/cognitive-finance-systems/wth-videos", parts: 3, maxRounds: 2}})
```
Le workflow enchaîne :
- distribution, parties écrites deux par deux, intégration et rendu ;
- revues (spectateur muet et 3 critiques), corrections ;
- QA, puis contrôle sans son final et un tour de correction ciblé si besoin.

Compte 4 h 30 à 7 h. Lance-le depuis la session principale : il appelle lui-même `mute-verify.wf.js`, ce qu'un
workflow lancé par un autre ne pourrait pas faire. Lis d'abord `.claude/skills/wth-story-build/SKILL.md`, et
`.claude/skills/wth-story-build/references/troubleshooting.md` à la première erreur.

Reporte le résultat dans le suivi : son objet `status` se reporte tel quel. Il ne contient que les étapes que le
workflow a réellement faites (avec `from: "verify"` : `qa` et `mute_verify`), et soit `open_issues` (remplace la
liste), soit `open_issues_add` (l'allonge : une vérification seule ne fait pas oublier les problèmes de la revue) :
```bash
python3 .claude/skills/wth-video/scripts/status.py merge V07 - <<'EOF'
{"spec": "done", "render": "done", "review": "fixed", "mute_verify": {"state": "done", "got": "8/9", "critere": "oui"},
 "qa": "done", "open_issues": []}
EOF
```
`ok: false` : voir « Quand ça casse ». Pour une retouche (une scène, un temps fort, un défaut de QA), suis la liste
« Retouche d'une scène » du skill `wth-story-build`, sans relancer tout le workflow.

### Après le film : commit et ménage

1. Commite les sources (« Politique de commit ») et pousse.
2. `make clean-tmp ID=V07` (garde les planches de revue), puis
   `rm -rf build/V07/story/stills && rm -f build/V07/story/muet_*.mp4`. Le disque doit rester au-dessus de 4 Go.
3. Dis à l'utilisateur, en français :
   - le chemin du film et de sa version sans sous-titres ;
   - le résultat de la QA ;
   - le score du contrôle sans son et la réponse au critère ;
   - les problèmes encore ouverts.

### 6 et 7. Livraison et publication

Envoie chaque vidéo dès qu'elle est prête (`SendUserFile`), avec sa légende et ses hashtags tirés de
`scripts.json`. La publication suit la route choisie par l'utilisateur :
1. il dépose les MP4 dans un dossier Drive partagé ;
2. tu les envoies sur Cloudinary (`upload-asset` depuis l'URL Drive, `WTH-V2/videos/WTH-Vxx`, sans écraser) ;
3. tu écris `output/uploads.json` et lances `make planning` ;
4. tu programmes dans Metricool (TikTok, Reel Instagram, Reel Facebook, 17:00, publication automatique), seulement
   **après son accord sur les dates**.

Formats exacts et contrôles : `references/publishing.md`.

## Règles de ressources

La machine a 4 processeurs et un disque limité : chaque règle évite une panne déjà vécue.
- **Un seul rendu Remotion à la fois.** Le verrou `build/.render.lock` l'impose à `make story`, `story-stills` et
  `motion`. Passe toujours par `make` ou `python3 -m pipeline.story`, jamais par `npx remotion`, qui ne prend pas le
  verrou. Ne supprime jamais ce fichier.
- **2 agents à la fois par workflow** (limite du moteur sur 4 processeurs), et au plus 2 workflows en même temps :
  le storyboard de la vidéo suivante pendant la fabrication de la vidéo en cours.
- **ElevenLabs : une génération à la fois**, jamais de relance ; les voix ne passent pas dans `batch.wf.js`.
- **Images de revue : planches JPEG demi-résolution** de `make review-sheets`, jamais d'images pleine résolution d'un
  film entier. C'est ce qui a rempli le disque pendant V01.
- **Disque ≥ 4 Go** : `make clean-tmp` après chaque rendu ; ménage de la vidéo quand elle est finie.

## Politique de commit

- **Ce que tu commites** : uniquement des sources.
  - `scripts/storyboards/Vxx.*` et `scripts/story/Vxx/` ;
  - `motion/src/story/` et `pipeline/` s'ils ont changé (code partagé : `make story-check` doit passer) ;
  - `cache/tts/<clé>.*` (la voix, déjà versionnée par conception) ;
  - `output/qa/Vxx.json`, `output/qa_report.md`, `scripts/production_status.json` ;
  - à la publication, `output/uploads.json` et `output/planning_videos.csv`.
- **Jamais** de MP4, ni de `build/`, ni d'illustrations : ils sont ignorés par git, et le dépôt est public.
- **Quand** : un commit par étape franchie (une voix ; un storyboard ; un film avec sa mise en scène, sa QA et son
  suivi ; le rapport final). Pousse aussitôt, sur la branche `claude/wth-video-pipeline` : une coupure de session
  ne perd alors rien.
- **Message** : en français, avec l'identifiant (« V07 : storyboard v1 (méthode Story) », « V07 : film Story
  (mise en scène, revues, QA, contrôle sans son) »), terminé par les lignes d'attribution que donne la session.

## Production en série

1. **Ordre.** V01 complète d'abord : c'est la référence, elle passe le point de validation. Puis V02 à V15 dans
   l'ordre de publication. L'utilisateur a demandé de les enchaîner sans s'arrêter une fois V01 acceptée, en livrant
   chaque vidéo dès qu'elle est prête.
2. **Voix d'abord, hors workflow**, une vidéo après l'autre, après la vérification des crédits. Elles peuvent avancer
   pendant que V01 se fabrique.
3. **Par défaut, pilote toi-même la série**, vidéo par vidéo : storyboard, film, `status.py merge`, commit et push,
   livraison, ménage, puis la vidéo suivante. C'est le mode qui livre chaque vidéo à temps et laisse l'utilisateur
   réagir. Si l'outil Workflow accepte deux workflows à la fois, lance le storyboard de la vidéo suivante pendant le
   film en cours.
4. **Lot sans surveillance** : `workflows/batch.wf.js` enchaîne plusieurs vidéos dans un seul workflow.
   ```
   Workflow({scriptPath: "/home/user/cognitive-finance-systems/.claude/skills/wth-video/workflows/batch.wf.js",
             args: {ids: ["V02", "V03"], root: "/home/user/cognitive-finance-systems/wth-videos",
                    commit: "<lignes d'attribution de la session>"}})
   ```
   Il commence par un préflight : il répare ce qui est sûr (`make voice`, illustrations, `clean-tmp`), saute les
   vidéos sans voix, et refuse V02 et suivantes tant que V01 n'est pas validée. Puis, pour chaque vidéo :
   - le storyboard (celui de la vidéo suivante se prépare pendant le film en cours) ;
   - `build-review.wf.js` avec `verify: false` ;
   - `mute-verify.wf.js`, avec un tour de correction ciblé, une QA et un second contrôle si le seuil n'est pas
     atteint ;
   - l'enregistrement : suivi, ménage, et commit si `commit` est donné.

   Options :
   - `stages` (`["storyboard","build","verify"]`) ;
   - `lookahead` (0 pour une vidéo à la fois) ;
   - `notes` (`{V07: "…"}`) ;
   - `revise` (`{V01: {notes: [...], version: "v3"}}`) ;
   - `from` (`{V07: "review"}`) ;
   - `parts`, `maxRounds`, `muteRounds` ;
   - `allowBeforeV01`, seulement sur demande explicite de l'utilisateur.

   Il ne livre rien lui-même : à la fin, envoie les fichiers de sa liste `deliver` et passe `delivered` à `done`.
   Fais des lots de 2 ou 3 vidéos, pour que les livraisons n'attendent pas des jours.
5. **Fin de série.**
   - `make qa` sur les 15 vidéos, puis le rapport `output/qa_report.md`.
   - Un agent « cohérence de la série » compare une image par scène des 15 films : palette, distribution
     récurrente, sous-titres, carte de fin, rouge seulement là où il est prévu.
   - Un tableau des durées et de la loudness.
   - Puis la proposition de dates et la publication.

## Nouvelle vidéo (hors V01 à V15)

1. Écris le script avec l'utilisateur dans `scripts/scripts.json`, sur le modèle d'une entrée existante :
   - les champs `id`, `source`, `date`, `titre`, `texte`, `legende`, `hashtags`, `segments`, `mots`,
     `notes_prononciation` ;
   - 7 segments : accroche, contexte, point1 à point3, chute, cta ;
   - une fin sur « Abonne-toi pour comprendre ton argent. ».
2. Ajoute la ligne dans `config/videos.csv`, lance `make lint ID=V16` et corrige ce qu'il signale.
3. Fais valider le texte par l'utilisateur **avant** la voix : la voix coûte des crédits et fige tous les temps.
4. `status.py init` ajoute la vidéo au suivi. Puis les étapes normales.

## Quand ça casse

| Problème | Que faire |
|---|---|
| Aucune prise de voix sous la limite | Ne régénère pas. `voice blocked`, puis demande à l'utilisateur : accélérer (≤ ×1,04, `tempo_take.py`), accepter une durée plus longue pour cette vidéo (`config.yaml`), ou raccourcir le script. Commandes : `references/voice-elevenlabs-mcp.md`, étape 4. |
| Erreur de quota ElevenLabs | Arrête le lot de voix ; `voice blocked` ; demande à l'utilisateur. |
| Transcription Scribe en désaccord (> 3 mots, nombre mal lu) | Transcris la prise suivante (`pick_take.py` donne l'ordre). |
| Agent `null` ou workflow interrompu | Relance avec `resumeFromRunId` : les agents finis ne sont pas refaits. |
| Storyboard refusé par `--check` | Skill `wth-storyboard` : retouche à la main ou `revise.wf.js`. |
| Mise en scène refusée (temps fort sans événement, scène non mise en scène) | L'agent auteur corrige. `ALLOW_PARTIAL=1` ne sert qu'aux rendus de travail. |
| Rendu en échec | Disque et navigateur (`preflight.py`), puis `wth-story-build/references/troubleshooting.md` ; une seule nouvelle tentative. |
| Problèmes majeurs après 2 tours de revue | `review open`, `open_issues` ; signale-les et continue : on ne boucle jamais. |
| Contrôle sans son sous le seuil | Un tour de correction ciblé, puis un nouveau contrôle ; sinon remonte à l'utilisateur avec les points faibles. |
| QA en échec | Corrige la cause, relance `make qa`. Ne desserre jamais un seuil : une durée plus longue demande l'accord de l'utilisateur. |
| Disque sous 4 Go | `preflight.py` lance `make clean-tmp` ; puis ménage des vidéos finies (`references/environment.md`). |
| `batch.wf.js` s'arrête en « checkpoint » | V01 n'est pas validée : envoie-la, attends l'accord. |
| Session perdue | `status.py show` et `status.py next` : le suivi et les fichiers commités suffisent pour reprendre. `next` signale une voix déjà en cache que le suivi n'a pas enregistrée : ne la régénère pas. |

## Points de validation avec l'utilisateur

Ce sont les seuls moments où tu attends sa réponse. Note chacun dans le suivi (`status.py checkpoint <nom> done
--note "…"`).

1. **Crédits ElevenLabs** (`elevenlabs_credits`) : avant chaque lot de voix, avec le coût estimé.
2. **Durée** : une voix sans prise sous la limite ; il choisit l'option.
3. **V01 complète** (`v01_full_approved`) : envoie-la avec et sans sous-titres, et attends son accord explicite
   avant toute vidéo V02 à V15. Après l'accord, enchaîne V02 à V15 sans t'arrêter.
4. **Dates de publication** (`publication_dates_approved`) : propose le tableau (une vidéo tous les 2 jours à 17:00,
   décalé), et ne programme rien avant son accord.
5. **Avant la première publication** (`publication_questions`) : licence Remotion et déclaration « contenu IA ».
6. **Ce qui ne se défait pas** : écraser un fichier sur Cloudinary, remplacer une voix déjà commitée, réécrire un
   storyboard validé (`overwrite`). Demande d'abord.

## Références : quand lire quoi

| Fichier | Lis-le quand |
|---|---|
| `references/voice-elevenlabs-mcp.md` | avant de générer, choisir ou importer une voix, ou de vérifier les crédits |
| `references/publishing.md` | pour livrer, proposer les dates, envoyer sur Cloudinary, programmer dans Metricool |
| `references/environment.md` | session neuve, ✘ du préflight, illustration absente, disque plein, push, reprise d'un workflow, licence |
| `references/status-schema.md` | pour lire ou modifier le suivi, ou comprendre un état |
| `scripts/preflight.py` | au démarrage et avant chaque étape lourde |
| `scripts/status.py` | à chaque étape franchie (`set`, `merge`, `checkpoint`), et pour `show` / `next` |
| `scripts/pick_take.py` | après le téléchargement des prises, puis après la transcription |
| `scripts/tempo_take.py` | aucune prise sous la limite, et l'utilisateur choisit d'accélérer (option (a)) |
| `scripts/drive_decode.py` | après chaque `download_file_content` d'une illustration |
| `workflows/batch.wf.js` | lot sans surveillance de plusieurs vidéos dont la voix est prête |
| `.claude/skills/wth-storyboard/SKILL.md` | avant l'étape 2 |
| `.claude/skills/wth-story-build/SKILL.md` | avant les étapes 3 à 5, et pour toute retouche de film |
