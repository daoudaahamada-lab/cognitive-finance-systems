---
name: wth-storyboard
description: Écrit le storyboard d'une vidéo WealthTech Horizon selon la méthode Story validée sur V01 — un fil conducteur, pour chaque scène état initial → action visible → résultat, temps forts calés sur les débuts de mots de la voix, lisible sans le son — par 3 brouillons, 3 juges, une synthèse, un test du spectateur muet, une révision et le contrôle --check, vers scripts/storyboards/Vxx.json et .md. Utilise-le pour tout storyboard, découpage en scènes, fil conducteur, idées-clés, révision de scène ou test sans son d'une vidéo WTH (V01 à V15 ou nouvelle Vxx), même si la demande dit seulement « prépare la mise en scène de V09 », « refais S11 de V01 », « intègre les retours de la revue dans le storyboard » ou « le storyboard de V07 ne passe pas le check ».
---

# wth-storyboard : le storyboard Story (méthode A)

Le storyboard est l'endroit où les 7 règles de l'utilisateur se gagnent ou se perdent. Une scène qui ne se comprend pas
sans le son sur le papier ne se comprendra pas dans le film ; la corriger ici coûte quelques minutes, la corriger après
le rendu coûte un tour de revue (≈ 1 h 30 sur V01). Ce skill produit un storyboard que la mise en scène (skill
`wth-story-build`) peut construire sans deviner, et qui a déjà passé un test sans son.

Chemins : `wth-videos/…` est relatif à la racine du dépôt ; les commandes `python3 -m pipeline…` et `make …` se lancent
depuis `wth-videos/`.

## Ce que tu produis

- `wth-videos/scripts/storyboards/Vxx.json` : fait foi. Lu par la mise en scène (`kit.at`, `Story.beat`), par
  `--check` et par le contrôle sans son du film.
- `wth-videos/scripts/storyboards/Vxx.md` : la même chose en français lisible, pour l'utilisateur.
- Contenu : `version`, `angle` (réponse aux 7 règles), `thread`, `objet_fil`, `cast`, `style`, 14 à 22 `scenes`
  contiguës (état initial, action, résultat, transition, temps forts, lecture sans son), 6 à 10 `idees_cles`,
  `entites_nouvelles` (au plus 3), `test_sans_son`, `risks`. Détail : `references/storyboard-schema.md`.

## Prérequis

1. **La voix est finale** : `wth-videos/build/Vxx/words.json` existe, ainsi que `audio.wav` (sinon
   `python3 -m pipeline.story Vxx --audio` le refait depuis la voix en cache, sans appel à ElevenLabs).
   Les temps forts sont des débuts de mots : si la voix change après, tous les temps glissent et le storyboard est à
   refaire. Sans voix, passer d'abord par la recette voix du skill `wth-video` ; ne jamais storyboarder sur une voix
   provisoire.
2. **Le script est dans `wth-videos/scripts/scripts.json`** (texte, segments, `source` du carrousel).
3. **Lance la préparation** (rapide, sans coût) :
   ```bash
   python3 .claude/skills/wth-storyboard/scripts/prep.py Vxx
   ```
   Elle imprime les phrases minutées, les segments, la cadence visée, les PNG autorisés et signale ce qui manque ; elle
   écrit `build/Vxx/storyboard/prep.json`, `words.tsv` (les débuts de mots à recopier dans les temps forts) et
   `pngs.jpg` (planche des PNG utilisables, à regarder).
4. **Un storyboard existe déjà ?** Le réviser (`revise.wf.js`) plutôt que le réécrire : une réécriture perd les
   corrections déjà validées. Ne le réécrire qu'à la demande (`overwrite: true`).

## Les 7 règles et le critère (résumé)

Texte exact de l'utilisateur et lecture générale : `references/brief-utilisateur.md`. À relire avant chaque storyboard.

1. Un fil conducteur : un seul objet suivi du début à la fin (`objet_fil`).
2. Chaque scène : un état initial, une action visible, un résultat.
3. Illustrer le sens complet de la phrase, nuance comprise.
4. Distinguer l'IA et « Toi » : formes, places, manière d'agir ; l'IA ne porte jamais « Toi ».
5. Faire évoluer les mêmes éléments plutôt que les remplacer.
6. Les PNG seulement quand ils servent la scène ; tout processus est animé en code.
7. La simplicité de la référence : ivoire, cyan, typographie lisible, peu d'accents.

**Critère de réussite** : « en masquant les sous-titres, je dois pouvoir comprendre l’action principale et percevoir ce
qui change ».

## La méthode A, et pourquoi chaque étape

| Étape | Ce qu'elle fait | Pourquoi |
|---|---|---|
| 0. Prep | `prep.py`, regard sur les PNG, public (« Toi » = conseiller ou spectateur), chiffres et dates à écrire, légende du repère | Tous les agents travaillent sur les mêmes temps, les mêmes PNG et les mêmes contraintes. |
| 1. 3 brouillons | trois storyboards complets sous trois angles : **objets persistants** (continuité), **grammaire de la référence** (formes plates, tenir puis éclater), **lisible sans son** (verbes visuels francs) | L'espace des solutions est large ; trois angles indépendants trouvent des idées qu'une seule tentative ne trouve pas. |
| 2. 3 juges | une lentille chacun : **muet** (compréhension sans son), **référence-simplicité**, **sens-faisabilité** (sens complet, rôles, exactitude, constructible avec le catalogue d'entités, au plus 3 entités nouvelles) | Un juge par critère évite qu'un seul défaut masque les autres ; la faisabilité est jugée avant de coûter. |
| 3. Synthèse | part du gagnant (somme des notes), greffe les meilleures idées, corrige les scènes faibles ; écrit `.json` et `.md` | On garde la cohérence d'un auteur et le meilleur des trois. |
| 4. Test muet + révision | un lecteur ne voit que ce qui est à l'écran (ni voix, ni texte) et reconstruit le message ; les idées-clés sont notées GOT / PARTIAL / MISSED ; les scènes mal lues sont refaites ; `test_sans_son` est rempli | C'est le critère de l'utilisateur, appliqué avant toute mise en scène. Sur V01, ce test a relevé 4 contresens et une dizaine de flous, corrigés avant toute ligne de code. |
| 5. Contrôle | `--check` + `soft_check.py`, corrections minimales, `.md` aligné ; résumé en 3 lignes | Un storyboard refusé au contrôle bloque la mise en scène ; mieux vaut le savoir ici. |

## Lancer le workflow (cas normal)

```
Workflow({scriptPath: "<dépôt>/.claude/skills/wth-storyboard/workflows/storyboard.wf.js",
          args: {id: "V05", root: "<dépôt>/wth-videos"}})
```

`<dépôt>` = chemin absolu de la racine (ici `/home/user/cognitive-finance-systems`). Options de `args` :

| Option | Défaut | Emploi |
|---|---|---|
| `notes` | — | consignes propres à la vidéo (de l'utilisateur, ou d'un retour sur un film précédent) ; elles priment sur les défauts |
| `overwrite` | `false` | réécrire un storyboard existant |
| `excerpt` | `false` | recommander un extrait de 10 à 15 s (validation rapide) |
| `muteRounds` | `1` | 2 pour un second tour test muet + révision si des idées restent PARTIAL ou MISSED |

Ordres de grandeur : 11 agents, 2 à la fois (machine à 4 cœurs), 70 à 90 min, ~1,5 M jetons (V01 : 80 min). Le
storyboard de la vidéo suivante peut tourner pendant la fabrication de la vidéo en cours. Si le workflow s'interrompt,
le relancer avec `resumeFromRunId` : les agents déjà finis ne sont pas refaits.

Le résultat donne `ok`, `files`, `version`, le gagnant et les notes des juges, le message reconstruit par le
spectateur muet, les scores des idées-clés, `entites_nouvelles` et la sortie du contrôle avec `resume_fr`.
- `ok: false` à l'étape `prep` : un prérequis manque (voix, script) ou un storyboard existe ; lire `reason`.
- `check.ok: false` : lire `check_output` et `alerts_left`, corriger à la main (section suivante), relancer les
  contrôles.
- Des idées encore PARTIAL ou MISSED : relancer `revise.wf.js` avec ces idées en `notes`, ou les signaler à
  l'utilisateur avec le résumé.

## Réviser un storyboard existant

Pour des retours de revue, des points faibles du contrôle sans son, ou une remarque de l'utilisateur sur quelques
scènes :

```
Workflow({scriptPath: "<dépôt>/.claude/skills/wth-storyboard/workflows/revise.wf.js",
          args: {id: "V01", root: "<dépôt>/wth-videos", version: "v3", scenes: ["S11", "S13", "S14"],
                 notes: ["le stylo du conseiller déclenche la fissure de la ligne fausse",
                         "le client arrive sur « client. », face au conseiller, et reste jusqu’à « décide »"]}})
```

Étapes : révision des scènes visées et de leur continuité (version montée, entrée dans `revisions`), test muet par
deux lecteurs indépendants, évaluation des idées-clés et une correction ciblée si besoin, contrôle. 5 à 8 agents,
20 à 40 min. Il ajoute `objet_fil` et `idees_cles` aux storyboards qui n'en ont pas encore (V01 v2).

## Retouche à la main (une ou deux corrections précises)

Pour un temps décalé, un mot mal recopié ou un détail d'aspect, un workflow est disproportionné :
1. Modifier `Vxx.json`, puis la même chose dans `Vxx.md`.
2. Recopier tout temps depuis `build/Vxx/storyboard/words.tsv` (relancer `prep.py` s'il manque).
3. Monter la version (« v2 · retouche S07 ») et ajouter une entrée à `revisions`.
4. Relancer les deux contrôles (section suivante).

## Contrôles

**Durs** — `make storyboard-check ID=Vxx` (= `python3 -m pipeline.story Vxx --check`, code 1 si refusé) : champs
obligatoires ; au moins un temps fort par scène ; scènes contiguës de 0 à la fin du dernier mot ; débuts de scène et
temps forts sur un début de mot (± 30 ms) et dans leur scène ; textes des scènes mis bout à bout = texte du script ;
6 à 10 idées-clés dont les scènes existent. Alertes : `objet_fil` ou `test_sans_son` absents.

**Complémentaires** — `python3 .claude/skills/wth-storyboard/scripts/soft_check.py Vxx` : schéma
(`references/storyboard.schema.json`), deux temps forts sur le même mot d'une scène (✘, code 1) ; plus de 3 s sans
temps fort (la QA refusera une image figée > 3,5 s), objet du fil absent de nombreuses scènes, point ou chute sans
idée-clé principale, plus de 3 entités nouvelles, dernière scène qui n'est pas la phrase d'appel seule (alertes).

**À relire soi-même** (ce qu'aucun script ne voit ; détail dans `references/lessons-v01.md`) :
- l'objet du fil est à l'écran dès l'image 0 et devient le bouton « S’abonner » ;
- chaque verdict a sa preuve avant lui, et sa cause est un geste visible de « Toi » ;
- l'IA n'agit qu'en pointillés, reste immobile quand elle se trompe, se range sans être chassée ;
- l'autre personne arrive sur son mot, face à « Toi », et reste ;
- 1 à 4 éléments actifs par temps fort, une action principale, ~8 formes au plus à l'écran ;
- le repère 1-2-3 a sa légende ; dates en clair ; nombres du script ; rouge seulement pour l'alerte annoncée ;
- jamais « VALIDÉ » avec une question ouverte ; aucun gris à 50 % pour « mettre en retrait » ;
- la composition descend jusqu'à y ≈ 1250 ; rien dans les zones réservées ; 800 px de large au plus ;
- chaque `lecture_sans_son` est honnête, et chaque idée-clé est assez visible pour être notée GOT.

## Après le storyboard

1. Contrôles verts (ci-dessus).
2. Suivi, si le skill `wth-video` est présent (l'état de chaque vidéo est dans
   `wth-videos/scripts/production_status.json`) :
   ```bash
   python3 .claude/skills/wth-video/scripts/status.py set Vxx storyboard done
   ```
3. Commit et push des deux fichiers seulement, message « Vxx : storyboard vN (méthode Story) » avec les lignes
   d'attribution de la session ; jamais `build/` ni de MP4 :
   ```bash
   git add wth-videos/scripts/storyboards/Vxx.json wth-videos/scripts/storyboards/Vxx.md
   ```
4. Résumé à l'utilisateur, en français, en 3 lignes (le fil, l'idée visuelle de chaque point, ce que le test muet a
   changé) avec le chemin du `.md`. Il peut le lire avant la mise en scène : c'est le moment le moins cher pour changer
   d'avis.
5. Suite : skill `wth-story-build` (il crée d'abord les `entites_nouvelles`, puis met en scène).

## Références : quand lire quoi

| Fichier | Lire quand |
|---|---|
| `references/brief-utilisateur.md` | avant tout storyboard ; quand un choix oppose deux règles |
| `references/series-bible.md` | avant d'écrire la distribution : rôles récurrents, structure des scripts, PNG autorisés par vidéo |
| `references/lessons-v01.md` | avant d'écrire les scènes, et pour juger ou réviser |
| `references/visual-verbs.md` | en écrivant chaque `action` et `evenement` : verbe → entité → macro |
| `references/motion-grammar.md` | pour la cadence, les durées, les passages entre compositions, la mise en page |
| `references/reference_style.json` | seulement pour un chiffre précis de la référence (clé citée dans motion-grammar.md) |
| `references/style.md` | pour une couleur, une taille de texte, une zone de l'image (jetons de `pipeline/story.py`) |
| `references/storyboard-schema.md` | pour un champ, une contrainte de `--check`, le modèle du `.md` |
| `references/storyboard.schema.json` | schéma machine (utilisé par `soft_check.py`) |
| `references/exemple-V01.md` | pour calibrer la précision attendue (deux scènes annotées de V01) |
| `../wth-story-build/references/entities.md`, `kit.md` | pour vérifier qu'une action est constructible |

Scripts : `scripts/prep.py` (préparation), `scripts/soft_check.py` (contrôles complémentaires), `scripts/check_wf.mjs`
(contrôle d'un modèle de workflow après modification ; `node --check` refuse le `return` de premier niveau que le
moteur de workflows admet) :
```bash
node .claude/skills/wth-storyboard/scripts/check_wf.mjs .claude/skills/wth-storyboard/workflows/*.wf.js
```

## Pièges fréquents

- **Texte des scènes ≠ script** : apostrophe droite ' au lieu de ’, « ... » au lieu de « … », espace en trop, mot
  oublié entre deux scènes. Recopier depuis `scripts.json`, jamais de mémoire.
- **Temps forts** : la casse compte (« Mais » ≠ « mais ») ; un mot répété se résout par son temps, mais pas deux temps
  forts sur le même mot dans une scène ; recopier `t` depuis `words.tsv`, jamais arrondi à la main.
- **Dernière scène** : la phrase d'appel seule (« Abonne-toi pour comprendre ton argent. »), mise en scène par la carte
  de fin standard ; la QA ne dispense que la dernière scène du contrôle d'image figée. Son `t_end` = durée de
  `audio.wav` (`prep.json` : `duree`), pas la fin du dernier mot.
- **Temps fort non voulu** : chaque temps fort devra être mis en scène, sinon le film entier est refusé. Une tenue
  s'écrit « Tenue : rien ne bouge ».
- **Trou de plus de 3 s** : la QA refuse une image figée de plus de 3,5 s ; prévoir un événement ou une dérive lente.
- **Carrousel d'un autre épisode** : `Story.png` refuse ; seuls le carrousel de la vidéo et les génériques sont permis.
- **Storyboard trop chargé** : 5 éléments ou plus qui bougent ensemble, 19 textes sur une fiche ; à taille téléphone,
  c'est illisible. Retirer ce qui a fini d'agir.
