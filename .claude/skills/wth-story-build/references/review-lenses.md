# Revues : les regards, l'évaluation sans son, la gravité

Méthode C. Comment un film Story est relu, par qui, sur quelles images, et comment on décide de ce qu'on corrige. Le
workflow `workflows/build-review.wf.js` applique tout cela. Ce document sert à le comprendre, à lancer un regard à la
main pour une retouche, et à juger les constats.

## Sommaire

1. Pourquoi plusieurs regards
2. Les sorties de revue (`make review-sheets`)
3. Échelle de gravité et arbitrage
4. Le spectateur muet
5. L'évaluation sans son (mute-eval)
6. Critique « continuité et référence »
7. Critique « visuel et marque »
8. Critique « synchro et technique »
9. Contrôle sans son final (`mute-verify.wf.js`)
10. Revue légère d'une retouche

## 1. Pourquoi plusieurs regards

Un seul relecteur voit ce qu'il cherche. Sur V01, chaque regard a trouvé des défauts que les autres avaient manqués :
- le spectateur muet a vu que la ligne fausse cassait sans cause visible ;
- la critique visuelle a vu que les fils partaient d'un espace vide entre deux rangées ;
- la critique de continuité a vu que le stylo flottait loin du corps.

Le spectateur muet compte le plus : il applique directement le critère de l'utilisateur. Il ne doit donc rien savoir
du sujet.

## 2. Les sorties de revue

Les relecteurs lisent les sorties de `make review-sheets` et n'extraient PAS d'images eux-mêmes. Un film de 58 s fait
1 750 images ; les vider en pleine résolution a rempli le disque pendant V01 (21 Go d'images de revue).

```bash
make review-sheets ID=Vxx                                    # film avec sous-titres -> build/Vxx/review/film/
make review-sheets ID=Vxx REVIEW="--nocap --sheets --phone"  # sans sous-titres -> build/Vxx/review/film_nocap/
make review-sheets ID=Vxx REVIEW="--beats"                   # seulement les bandes de temps forts
```

`make story` fait déjà les planches (`sheets/`) du film avec sous-titres.

| Sortie | Contenu | Pour qui |
|---|---|---|
| `sheets/sheet_NN.jpg` | 6 images par seconde, demi-résolution (540 × 960), 12 par planche, avec scène, temps et image du film | tous ; la version `film_nocap` pour le spectateur muet |
| `beats/bNNNNN_Sxx_mot.jpg` | une bande par temps fort : images f−3 à f+12 ; le titre donne la scène, le mot et l'événement voulu (`what`) | continuité, synchro |
| `phone/phone_NN.jpg` et `phone/<nom>_360.mp4` | après réencodage à 2 Mb/s, 360 px de large, 2 images par seconde : ce que voit un téléphone | spectateur muet, visuel |
| `holds.json` | tenues de 0,5 s ou plus ; signalées au-delà de 3,5 s, hors carte de fin | synchro |

Si un détail exige la pleine résolution, extrais au plus 6 images en JPEG dans `build/Vxx/review/frames/<regard>/`.
`make clean-tmp ID=Vxx` les supprime avec les bandes et les images téléphone, et garde les planches.

Pour un rendu incomplet ou un extrait :
`make review-sheets ID=Vxx REVIEW="--src build/Vxx/story/film_partiel.mp4"`, ou `--src output/extraits/<fichier>.mp4`.

## 3. Échelle de gravité et arbitrage

| Gravité | Définition | Exemples (V01) |
|---|---|---|
| blocker | trahit la demande de l'utilisateur (son critère ou une de ses 7 règles), ou ferait honte à la marque | idée principale illisible sans le son ; texte faux à l'écran ; rendu qui casse |
| major | défaut clairement visible, ou sens d'une scène flou ou faux | ligne qui casse avant toute vérification ; « ? » qui naît loin de la valeur ; client qui arrive avant la question, épaule contre épaule avec le conseiller |
| minor | finition | ombre un peu lourde ; 2 images de décalage sur un geste secondaire |

Ce qu'on fait de chaque gravité :
- **Bloquants et majeurs.** Tous corrigés avant le tour suivant.
- **Mineurs.** Corrigés quand c'est sûr et peu coûteux.
- **Tours.** Deux au plus. Ce qui reste est noté dans l'état de la vidéo et signalé, sans boucler.

**Arbitrage.** Quand deux regards se contredisent, la lisibilité sans le son et la simplicité gagnent : c'est le
critère de l'utilisateur. Exemple : le visuel veut moins d'éléments, la continuité veut garder un objet du fil. On
garde l'objet du fil et on retire le reste.

**Format d'un constat :**
- gravité ;
- scène, temps et image du film ;
- problème ;
- preuve : quelle planche, quelle bande, quelle image ;
- correction concrète, en entités, macros du kit, mise en page ou timing.

Un constat sans preuve ou sans correction ne se traite pas : renvoie-le.

## 4. Le spectateur muet

**But.** Appliquer le critère de l'utilisateur à la lettre : comprend-on l'action principale et ce qui change, sans
son ni sous-titres ?

**Règles.**
- Il ne lit QUE les planches de `film_nocap/`.
- Pas de storyboard, de script, de props ni de rapport : il ne doit rien savoir du sujet.
- Il commence par les planches téléphone, pour le rythme réel, puis passe aux planches de détail.

**Consigne** (telle que dans le workflow, `mutePrompt`) :

```
You are a first-time viewer of a short vertical video, muted and WITHOUT captions. You do not know its topic or its
script. Look ONLY at the images below. Do not open any other file of the repository: no storyboard, script, spec,
props or report. Reading them would spoil the test.
1. First, the phone-size sheets, in order, to get the flow: <film_nocap>/phone/phone_*.jpg (what a phone shows,
   2 images per second).
2. Then the detail sheets, all of them, in order: <film_nocap>/sheets/sheet_*.jpg (6 images per second, half
   resolution). Each frame is labelled "scene id, time, film frame #".
Describe, beat by beat with timestamps:
- the main action;
- who acts: what each character or object seems to be;
- what changes.
Then say in 4-6 sentences what the video is trying to say.
Be honest about what was ambiguous or misleading, and about what you understood only thanks to written words on
screen.
```

**Sortie.**
- `beats` : `[{t, action, acteurs, changement, ambiguite}]` ;
- `message` ;
- `ambiguites`.

## 5. L'évaluation sans son (mute-eval)

**But.** Comparer la lecture du spectateur muet au sens VOULU, idée par idée. Elle s'appuie sur les `idees_cles` du
storyboard : 6 à 10 `{id, idee, scenes}`, avec éventuellement `principale`.

**Notes.**
- **GOT** : compris comme voulu.
- **PARTIAL** : flou, incomplet, ou compris seulement grâce aux mots écrits.
- **MISSED** : absent ou faux.

**Idées principales.** Celles marquées `principale: true`. Sans marque, ce sont celles qui portent la thèse de la
vidéo, ses étapes numérotées et sa phrase de fin.

**Constats.** Chaque idée qui n'est pas GOT devient un constat, avec une correction visuelle dans ses scènes :
- blocker : une idée principale MISSED ;
- major : une idée MISSED, ou une idée principale PARTIAL ;
- minor : le reste.

**Consigne** (`muteEvalPrompt`) :

```
Compare what a first-time MUTED viewer (no captions, no script) understood from the full film of <Vxx> with the
INTENDED meaning. Read the storyboard <storyboard>:
- its idees_cles: {id, idee, scenes}, plus principale when present;
- the scenes' texte and lecture_sans_son.
Score each idee_cle once, in storyboard order:
- GOT: understood as intended;
- PARTIAL: vague, incomplete, or understood only through written labels;
- MISSED: absent or wrong.
Quote the viewer's report as evidence.
Mark the main ideas (principale = true): those marked so in the storyboard. If none is marked, take the ideas that
carry the video's thesis, its numbered steps and its closing line.
Then, for every idea that is not GOT, add a finding with a concrete visual fix in that idea's scenes:
- blocker if a main idea is MISSED;
- major if any idea is MISSED or a main idea is PARTIAL;
- minor otherwise.
MUTED VIEWER REPORT: <report>
```

## 6. Critique « continuité et référence » (reference-continuity)

**But.** Vérifier que les éléments interagissent et se transforment, selon le storyboard, les 7 règles et la
grammaire de la référence.

**Sources :**
- les bandes de temps forts `film/beats/` ;
- les planches `film/sheets/` ;
- le storyboard ;
- `.claude/skills/wth-storyboard/references/motion-grammar.md`.

**Consigne** (dans `CRITICS`) :

```
Mise-en-scène against the storyboard, the user's 7 rules and the reference motion grammar (motion-grammar.md).
Use the beat strips <film>/beats/*.jpg, one per beat. Each strip shows frames f-3 to f+12, and its title gives the
scene, the word and the intended event. Use also the sheets <film>/sheets/*.jpg, against the storyboard.
Check scene by scene:
- elements really INTERACT and TRANSFORM (they meet obstacles, approach, separate, become something else) rather
  than appear, zoom or fade in sequence;
- each scene shows its etat_initial -> action -> resultat, and hands over to the next one as its transition says;
- the same entities persist along the thread (objet_fil); nothing is replaced when it could evolve;
- hold then burst: still between beats, one burst per beat, 1-4 active elements;
- every event lands on its word (strip frame +0 is the word onset);
- the AI and the human are unmistakably distinct: the shape of their marks, tools only in the human's hand, the AI
  acting through dotted beams. The human's tool CAUSES the change, and the proof comes before the verdict;
- the full meaning of each sentence is shown, not just its keyword.
```

**Constats typiques (V01) :**
- le passage du document à l'étiquette-source était simulé par un fondu au lieu d'une transformation ;
- plusieurs temps forts fusionnaient en un long mouvement chargé à l'entrée d'une scène ;
- l'IA lançait un faisceau sur la ligne cassée, alors que le storyboard la voulait immobile.

## 7. Critique « visuel et marque » (visual-brand)

**But.** Juger la lisibilité à taille téléphone, la discipline des couleurs, la simplicité et la finition sur ivoire.

**Sources :**
- les planches téléphone `film/phone/` (d'abord) ;
- les planches `film/sheets/` ;
- au plus 6 images pleine résolution ;
- `assets/v01_reference_sheet.jpg`, le niveau validé.

**Consigne** (dans `CRITICS`) :

```
Visual quality and identity on ivory, at phone size first. Use these sources:
- the phone sheets <film>/phone/phone_*.jpg: re-encoded at 2 Mb/s and 360 px wide, this is what viewers see;
- the half-resolution sheets <film>/sheets/*.jpg;
- at most 6 full-resolution frames, extracted into build/<Vxx>/review/frames/visual-brand/ as JPEG, only where a
  detail must be checked.
Compare with the approved level, assets/v01_reference_sheet.jpg. Check:
- legibility at phone size (text at least 32 px at scale 1, short lines), typographic hierarchy, French spelling and
  typography;
- colour discipline: ivory, ink, a single cyan accent, deep cyan for the human; red only for the alert element; no
  50 % greyed lines that read as "rejected";
- simplicity: 1-4 active elements and about 8 primitives at most at phone size; calm and premium, like the reference;
- composition: action centred around y≈800 and using the frame down to y≈1250, with no empty bottom 40 %. Safe zones
  empty: top 160 px, bottom 380 px, x > 940. No collision with the caption line (y 1280-1380);
- PNG compositing on ivory: fringes, leftover glow, shadows (a contact shadow is preferred);
- alignment of wires, boxes and stickers; wires start on the text they prove; the last frame of each scene has no
  collision;
- banding or mush after the re-encode.
```

**Constats typiques (V01) :**
- à taille téléphone, la fiche devenait un mini-tableur : environ 50 marques et 19 textes de même corps ;
- les fils partaient de l'espace entre deux rangées ;
- le « ? » naissait à 100 px de la valeur ;
- l'autocollant chevauchait la valeur barrée sur l'image finale.

## 8. Critique « synchro et technique » (sync-technical)

**But.** Vérifier que les événements tombent sur leurs mots, sans tenue morte, que la QA et la version sans
sous-titres sont bonnes, et que la mise en scène est propre.

**Sources :**
- les bandes `film/beats/` ;
- `film/holds.json` ;
- les props `build/Vxx/story/props_film.json` (`meta.beats`, `beats_off_onset`, `storyboard_beats_missing`,
  `beats_snapped_to_attack`, `captions`) ;
- `output/qa/Vxx.json`.

**Consigne** (dans `CRITICS`) :

```
Sync and technical. Use these sources:
- the beat strips <film>/beats/*.jpg;
- the holds report <film>/holds.json;
- the props build/<Vxx>/story/props_film.json: meta.beats, meta.beats_off_onset, meta.storyboard_beats_missing,
  meta.beats_snapped_to_attack and captions;
- the QA report output/qa/<Vxx>.json, written by make story. Re-run "make qa ID=<Vxx>" only if that report is older
  than the film.
Check:
- every beat event starts on its word-onset frame (strip frame +0); nothing important starts mid-word or on a hold
  beat;
- holds: no frozen picture over 3.5 s except the end card, and no hold that feels dead even under 3.5 s;
- karaoke: the highlighted word changes on the exact onset; caption groups read naturally (2-3 words, at most
  760 px); alert words are red only where intended;
- QA: list every failed check with its value. "Version sans sous-titres conforme" must pass;
- the code of the staging package:
  - beat or word lookups (kit.at, S.word_after) instead of magic frame numbers;
  - no keys on figures outside the Figure rig;
  - every part ends before the next one starts;
  - no "attention (kit)" warning in the output of "make story-props ID=<Vxx>".
```

**Préambule commun aux trois critiques** (`criticPrompt`) :

```
You are a demanding critic reviewing the FULL film of <Vxx> (review round <n>) through ONE lens. Do not modify
project files. The review sheets are already made: do not extract frames beyond what your lens allows.
Film: <output> (with captions) and <no-caption film> (without). Build report: <report>
LENS "<lens>": <brief>
Severity:
- blocker: defeats the user's request (his criterion or one of his 7 rules) or would embarrass the brand;
- major: clearly visible, or the meaning of a scene is unclear or wrong;
- minor: polish.
For each finding, give:
- the scene id, the timecode and the film frame;
- the evidence: which sheet, strip or frame shows it;
- a concrete fix, in terms of entities, kit macros, layout or timing.
List the strengths to keep too.
```

Chaque prompt commence aussi par le contexte commun du workflow (`CTX`) : marque, méthode, critère, chemins, règles.

## 9. Contrôle sans son final (`mute-verify.wf.js`)

Il a lieu après les tours de revue et la QA, sur le film définitif. C'est la porte de sortie de la vidéo.

```
Workflow({scriptPath: "<dépôt>/.claude/skills/wth-story-build/workflows/mute-verify.wf.js",
          args: {id: "Vxx", root: "<dépôt>/wth-videos"}})
```

**Déroulé.**
1. Un agent de préparation refait les planches sans sous-titres et relit la liste des `idees_cles`.
2. Deux spectateurs indépendants regardent ces planches, dans un ordre différent : le premier commence par le
   téléphone, le second par le détail.
3. Un évaluateur note chaque idée sur leurs DEUX rapports :
   - GOT si les deux l'ont comprise ;
   - PARTIAL si un seul l'a comprise, ou si elle est floue ;
   - MISSED si aucun ne l'a comprise.
   Il répond aussi au critère de l'utilisateur, en français.

**Réussite :**
- au moins 85 % des idées en GOT (7 idées : 6 GOT ; 8 idées : 7 GOT ; 10 idées : 9 GOT) ;
- aucune idée principale en MISSED ;
- `critere_oui` vrai.

Une idée que l'évaluateur oublie compte MISSED.

**En dessous du seuil :**
1. Fais UN tour de correction ciblé sur les scènes des idées manquées : verbe visuel plus net, avant/après plus
   fort, tenue plus longue sur le moment clé, moins d'éléments concurrents.
2. Refais le rendu, la QA, puis ce contrôle.
3. Si le seuil n'est toujours pas atteint, remonte à l'utilisateur avec les points faibles.

**Exemple : V01, extrait S11-S14.** Les 6 idées en GOT et « oui, avec des réserves ». Les réserves sont devenues les
leçons de la grammaire (SKILL.md) :
- la cause de la cassure n'était pas visible ;
- les coches ne différaient que par la couleur ;
- le client restait trop peu à l'écran ;
- VALIDÉ était posé avec une question ouverte ;
- les dates étaient ambiguës ;
- l'IA sortait comme si l'humain la remplaçait.

## 10. Revue légère d'une retouche

Pour une retouche d'une scène, ne relance pas tout le workflow :
1. `make story ID=Vxx`, puis `make review-sheets ID=Vxx REVIEW="--beats --sheets"`.
2. Lis les bandes des temps forts de la scène touchée et les planches qui l'encadrent (une scène avant, une après).
3. Si le SENS de la scène a changé, lance `mute-verify.wf.js` ; sinon, la QA suffit.
