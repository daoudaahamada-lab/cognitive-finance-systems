# Voix : la recette par le connecteur ElevenLabs

À lire avant de générer ou de réimporter la voix d'une vidéo. C'est la recette réellement utilisée pour V01 à V06.

## Pourquoi cette recette

- **L'API ElevenLabs n'est pas joignable depuis la machine** (réseau filtré, pas de clé). `make tts` ne sait donc
  que relire le cache (`cache/tts/<clé>.mp3` + `.json`). La voix se génère par le connecteur MCP ElevenLabs (outils
  `creative_*`), puis `pipeline.connector` la range dans le cache **sous la même clé** que l'API (clé = texte du
  script + voix + modèle + réglages de `config.yaml`). Tout le reste du pipeline la relit ensuite sans réseau.
- **Chaque génération coûte des crédits** : 4 prises par appel, environ 870 à 1 010 crédits par prise, soit 3 500 à
  4 000 par vidéo. Le quota de l'utilisateur est de 40 000 crédits par période et il a déjà été épuisé une fois (le
  20/10, à V06 : « You have 580 credits remaining, while 908 credits are required »). D'où trois règles : vérifier
  les crédits avant un lot, une seule génération à la fois, jamais de nouvel appel pour « réessayer ».
- **La voix fixe tous les temps du film.** Les temps forts du storyboard sont des débuts de mots de cette voix :
  changer de prise après le storyboard oblige à le refaire. Choisis la prise une fois, avec soin.

## Avant un lot : les crédits

1. Le connecteur n'expose pas le solde ; seule l'erreur de quota l'affiche.
2. Estime le coût sans rien dépenser : `creative_generate_speech` avec les paramètres ci-dessous et
   `estimate_only: true` renvoie `estimate.credits` pour les 4 prises (rien n'est généré ni facturé).
3. Additionne pour le lot et demande à l'utilisateur si son solde le couvre. Ordre de grandeur : dix vidéos
   ≈ 37 000 crédits, presque une période entière. Note sa réponse :
   `python3 .claude/skills/wth-video/scripts/status.py checkpoint elevenlabs_credits done --note "<solde annoncé, date>"`.
4. Erreur de quota pendant un lot : **arrête tout**. Les vidéos suivantes échoueraient de la même façon. Consigne
   `status.py set Vxx voice blocked --note "quota ElevenLabs"` et demande à l'utilisateur.

## Les paramètres, à ne pas improviser

| Paramètre | Valeur | Pourquoi |
|---|---|---|
| `flow_id` | `iq3Sq0IyV8N3hBFkzVNg` | le flow de la série ; la prise et sa transcription doivent être sur le même flow. Introuvable : `creative_create_flow`, puis ce nouvel id pour TOUS les appels de la vidéo |
| `model_id` | `eleven_multilingual_v2` | celui de `config.yaml` (l'outil propose `eleven_v4` par défaut : ne pas le prendre) |
| `voice_id` | `SWPcnF19luPOF81eOcxl` | Abdelatif - Clear & Direct, voix choisie pour les 15 vidéos (`config.yaml` `tts.voice_id`) |
| `prompt` | le champ `texte` de `scripts/scripts.json`, **à l'identique** | la clé de cache et l'alignement comparent ce texte caractère par caractère (espaces insécables de « 4 600 € », apostrophes ’) |
| `generations_count` | **2** (consigne du 21/10 ; avant : défaut 4) | sans limite de durée, 2 prises suffisent pour choisir la plus naturelle |
| `context` | une phrase, ex. « voix off de la vidéo WTH V07 » | requis par chaque outil `creative_*` |

Lis le texte par script, jamais de mémoire :
```bash
cd wth-videos && python3 -c "import json;print({s['id']:s for s in json.load(open('scripts/scripts.json'))}['V07']['texte'])"
```

Ne modifie jamais la section `tts:` de `config.yaml` : toutes les clés de cache changeraient. Les voix non
verrouillées (`locks/` absent pour V01 à V06) seraient alors introuvables, et `make tts` tenterait l'API.

## La recette, vidéo par vidéo

Commandes `make` et `python3 -m pipeline…` : depuis `wth-videos/`. Scripts du skill : depuis la racine du dépôt.

0. **Préparer, et vérifier qu'il y a bien quelque chose à générer.**
   `python3 .claude/skills/wth-video/scripts/preflight.py Vxx --no-voice` (le script existe, il est dans
   `config/videos.csv`).
   - **La ligne voix dit « ✔ voix : prise …, … s, … mots alignés » : la voix est DÉJÀ en cache. Ne génère rien.** Le
     suivi a seulement pris du retard (voix commitée, `status.py set` oublié : c'est arrivé sur V12 à V15). Lance
     `make voice ID=Vxx`, commite le cache s'il est signalé « pas encore commité », puis enregistre-la avec la
     commande complète que donne `status.py next Vxx` (`set Vxx voice done take=… duration_s=… cache_key=…
     aligned=…`). Régénérer coûterait environ 4 000 crédits pour une voix déjà payée, et changerait tous les temps.
   - La voix est absente (« ! voix : absente du cache ») : `status.py set Vxx voice in_progress`, puis l'étape 1.
1. **Générer : un seul appel.** `creative_generate_speech` avec `flow_id`, `model_id`, `voice_id`, `prompt`,
   `context`. Note `flow_id`, `node_id` et les `session_ids` renvoyés. Si l'appel renvoie une erreur, ne le relance
   pas : lis-la (quota → section précédente).
2. **Attendre.** `creative_get_flow_run_status` (`flow_id`, `session_ids`, `context`) toutes les
   `poll_after_seconds` jusqu'à `all_completed` ou `has_failures`. Chaque prise donne un `generation_id`, sa durée
   (`duration_secs`) et un `content_url` sur `storage.googleapis.com` (URL signée, valable environ 2 h).
3. **Télécharger les 4 prises tout de suite** (les URL expirent) :
   ```bash
   mkdir -p build/Vxx/voice
   curl -sS -f -o build/Vxx/voice/take-<generation_id>.mp3 "<content_url>"     # une fois par prise
   ```
   Ce sont des fichiers téléchargés : n'exécute rien dans ce dossier.
4. **Choisir.** `python3 .claude/skills/wth-video/scripts/pick_take.py Vxx`. Il mesure chaque prise (ffprobe),
   depuis le 21/10 il n'y a plus de limite à 60 s : demande 2 prises (`generations_count: 2`) et garde la plus naturelle
   (QA : 45 s à 3 min). Ancienne règle, pour mémoire : écarte celles qui dépassent la limite (QA 60 s − 0,6 s de fin = **59,4 s**, ou la durée approuvée pour cette
   vidéo dans `config.yaml` `qa.max_duration_by_video`, ex. V03 : 62 s → 61,4 s), puis recommande la prise dont le
   débit est le plus proche de 2,6 mots/s (celui de V01 et V02, validées), avec un ordre de repli.
   **Code 2 = aucune prise ne tient** : ne régénère pas. Le script calcule l'accélération nécessaire. Consigne
   l'attente, puis demande à l'utilisateur de choisir entre les options (a), (b) et (c) ci-dessous :
   `status.py set Vxx voice blocked --note "4 prises de … à … s, aucune sous … s" --pending "choix de l'utilisateur : (a) ×F, (b) durée, (c) script"`.
   `blocked` (et non `in_progress`) dit à une session neuve qu'il n'y a rien à faire avant sa réponse.
   - **(a) Accélérer la prise la plus courte**, si ×F ≤ 1,04 (au-delà, ça s'entend). Transcris d'abord cette prise
     (étape 5 : la transcription porte sur la prise d'origine, la seule qui soit sur le flow), puis :
     ```bash
     python3 .claude/skills/wth-video/scripts/tempo_take.py Vxx <generation_id> 1.027
     ```
     Il écrit `take-<id>-x1.027.mp3` (`ffmpeg -filter:a atempo=1.027 -c:a libmp3lame`, au débit d'origine) et
     `words-<id>-x1.027.json`, où chaque `start` et `end` est **divisé** par F (la prise dure F fois moins
     longtemps). Puis `pick_take.py Vxx` (la prise accélérée apparaît comme `<id>-x1.027` et doit tenir), et
     l'étape 7 avec ces deux fichiers et le `--generation-id` d'origine. Au suivi, ajoute `tempo=1.027` et une note
     « prise accélérée ×1,027, accord de l'utilisateur le <date> ».
   - **(b) Accepter une durée plus longue pour cette vidéo** (V03, V07, V08, V10 et V11 l'ont été). Ajoute la
     vidéo sous `qa.max_duration_by_video` dans `config.yaml`, et rien d'autre (jamais la section `tts:`) :
     ```yaml
     max_duration_by_video: {V03: 62.0, V08: 62.5}    # durée de QA = prise + 0,6 s de fin, arrondie au-dessus
     ```
     Puis reporte-la au suivi et note l'accord :
     ```bash
     python3 .claude/skills/wth-video/scripts/status.py merge Vxx - <<'EOF'
     {"max_duration_s": 62.5, "notes": ["durée maximale 62,5 s approuvée par l'utilisateur le <date>"]}
     EOF
     python3 .claude/skills/wth-video/scripts/status.py set Vxx voice in_progress --pending ""
     ```
     Relance `pick_take.py Vxx` (la limite devient 62,5 − 0,6 = 61,9 s) et continue à l'étape 5. Commite
     `config.yaml` avec la voix (« QA : durée approuvée pour Vxx »).
   - **(c) Raccourcir le script** : l'utilisateur valide le nouveau texte dans `scripts/scripts.json`, puis
     nouvelle génération (étape 1) : de nouveaux crédits, donc la vérification du solde d'abord.
5. **Transcrire la prise choisie** (Scribe, 0 crédit) :
   - `creative_add_flow_asset_node` : `flow_id`, `modality: "audio"`, `generation_id`, `label: "Vxx prise <id>"`
     → `node_id` ;
   - `creative_transcribe_audio` : `flow_id`, `model_id: "eleven_scribe_v1"`, `connect_from: [node_id]` ;
   - interroge `creative_get_flow_run_status` jusqu'à la fin ; le résultat donne `transcripts[].words` et un
     `words_download_url` ;
   - `curl -sS -f -o build/Vxx/voice/words-<generation_id>.json "<words_download_url>"`.
6. **Vérifier avant d'importer.** Relance `pick_take.py Vxx` : la colonne Scribe montre maintenant « alignés/total »
   pour cette prise (calcul de `pipeline.connector`, sans rien écrire). Puis regarde dans le JSON Scribe les nombres
   et sigles listés dans `notes_prononciation` du script. Plus de 3 mots non alignés, ou un nombre lu de travers →
   transcris la prise suivante de l'ordre de repli. Ne régénère pas.
   - **Montants.** Le script écrit « 4 600 € » en un seul mot (espaces insécables) ; Scribe le découpe en « 4 »,
     « 600 », « € ». Le connecteur aligne ces morceaux sur le mot du script. La fin du montant inclut « euros »,
     avec un plafond de 0,45 s : Scribe compte souvent la pause qui suit dans la durée du symbole. Même chose pour
     « 1 % ». Un nombre écrit en toutes lettres par Scribe ne s'aligne pas : il apparaît dans les mots non alignés.
7. **Importer.**
   ```bash
   python3 -m pipeline.connector Vxx --audio build/Vxx/voice/take-<id>.mp3 \
       --words build/Vxx/voice/words-<id>.json --generation-id <id>
   ```
   C'est `make import ID=Vxx AUDIO=… WORDS=… GEN=…`. Il annonce « N/M mots alignés par Scribe ».
   - « déjà en cache, rien à importer » : une voix existe déjà pour ce texte exact. Vérifie laquelle (`status.py show
     Vxx`).
   - Pour remplacer une prise importée mais **pas encore commitée**, supprime `cache/tts/<clé>.mp3` et `.json`, puis
     importe l'autre prise.
   - Ne remplace jamais une voix commitée sans l'accord de l'utilisateur : le storyboard et la mise en scène en
     dépendent.
8. **Préparer la voix pour le pipeline.** `make voice ID=Vxx`. C'est `make tts` (lecture du cache : il écrit
   `build/Vxx/tts.json`, aucun appel réseau), puis `make words` (`build/Vxx/words.json`), puis `audio.wav`
   normalisé. L'ordre compte : `words` a besoin de `tts.json`, et c'est l'étape qui manquait dans la première
   version de la recette. Vérifie que `words.json` a autant de mots que le script et que le dernier mot finit près
   de la fin de la prise.
9. **Commiter.** Le cache est la seule copie d'une voix payée (`build/` n'est pas versionné) :
   ```bash
   git add wth-videos/cache/tts/<clé>.mp3 wth-videos/cache/tts/<clé>.json wth-videos/scripts/production_status.json
   git commit   # « Add Vxx voice (Abdelatif, take <generation_id>) » + les lignes d'attribution de la session
   git push -u origin HEAD
   ```
   La clé est dans `build/Vxx/tts.json` (`cache_key`) ou dans la sortie du connecteur.
10. **Suivi.** `status.py set Vxx voice done take=<id> duration_s=<durée> cache_key=<clé> aligned='"147/147"'`.
11. **Plus tard**, une fois le film validé par l'utilisateur : `make lock ID=Vxx`. Le fichier `locks/Vxx.json` fige
    la voix, même si le texte du script change. Les prises de `build/Vxx/voice/` peuvent alors être supprimées.

## Plusieurs voix d'affilée

- Une vidéo à la fois, dans l'ordre de publication, jamais deux générations en même temps. Le connecteur limite la
  concurrence : quand V01 et V02 ont tourné ensemble, une prise a buté sur « concurrency limit ».
- Un agent par vidéo convient, lancé l'un après l'autre. Chacun suit les étapes 0 à 10 et s'arrête à la première
  erreur de quota.
- Commit après chaque voix.
- Les voix ne passent jamais par `workflows/batch.wf.js` : les crédits demandent un regard humain.

## Quand ça ne va pas

| Symptôme | Cause probable | Que faire |
|---|---|---|
| `preflight.py` : « ✔ voix » mais le suivi dit `pending` (« ! suivi de la voix ») | voix commitée, suivi oublié | ne rien générer : étape 0 (`make voice`, puis la commande de `status.py next Vxx`) |
| « This request exceeds your quota of 40000 » | crédits épuisés | arrêter le lot ; `voice blocked` ; demander à l'utilisateur |
| `pick_take.py` sort en code 2 | script long ou débit lent | ne pas régénérer ; options (a), (b), (c) ci-dessus |
| `content_url` refusée (403) | URL signée expirée (≈ 2 h) | relire le run avec `creative_get_flow_run_status` (gratuit) pour obtenir de nouvelles URL ; à l'avenir, télécharger dès la fin du run |
| plus de 3 mots non alignés | prise mal articulée, nombre lu en lettres | transcrire la prise suivante |
| « concurrency limit » | deux générations en même temps | attendre la fin de l'autre ; ne pas relancer |
| `make tts` : « ELEVENLABS_API_KEY manquante » | la voix n'est pas dans le cache pour ce texte et ces réglages | import pas fait, texte de `scripts.json` modifié après l'import, ou `config.yaml` touché |
| `make words` : `tts.json absent` | `make tts` pas lancé | `make voice ID=Vxx` |
| `--check` du storyboard : temps hors début de mot | voix changée après le storyboard | refaire les temps du storyboard (skill `wth-storyboard`) |
