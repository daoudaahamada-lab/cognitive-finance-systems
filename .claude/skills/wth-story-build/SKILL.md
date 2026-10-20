---
name: wth-story-build
description: Met en scène et rend une vidéo WealthTech Horizon à partir de son storyboard (méthode Story validée sur V01) - écrit scripts/story/Vxx (API Story + macros story_kit + figurine articulée), ajoute au besoin des entités Remotion (motion/src/story), rend le film avec et sans sous-titres (make story), lance les revues sur les planches de make review-sheets (spectateur muet + 3 critiques), corrige, vérifie sans son (idées-clés) et passe la QA story. Utilise-le dès qu'il faut animer, mettre en scène, rendre, re-rendre, corriger une scène ou un temps fort, ajouter un élément graphique, réparer un rendu Story ou Remotion (« film entier refusé », « mot introuvable », verrou de rendu, image figée, halo de PNG) ou passer la QA d'une vidéo WTH, même pour une demande courte comme « la ligne casse trop tôt dans V01 S11 » ou « refais la fin de V04 ».
---

# Mise en scène, rendu, revues et QA d'une vidéo WealthTech Horizon

Ce skill couvre les méthodes B (mise en scène et rendu) et C (revues, contrôle sans son, QA) de la méthode Story.
Il part d'un storyboard validé (`scripts/storyboards/Vxx.json`, skill `wth-storyboard`) et d'une voix finale
(`build/Vxx/words.json`, skill `wth-video`). Il livre `output/WTH-Vxx.mp4`, sa version sans sous-titres et une QA verte.

Les chemins sont relatifs à `wth-videos/` (lancer `make` depuis ce dossier) ; le skill est dans
`.claude/skills/wth-story-build/` à la racine du dépôt.

## Ce qu'on vise

Le critère de l'utilisateur, mot pour mot : « en masquant les sous-titres, je dois pouvoir comprendre l’action
principale et percevoir ce qui change ».

Ses 7 règles, en bref (texte exact : `.claude/skills/wth-storyboard/references/brief-utilisateur.md`) :
1. un fil conducteur ;
2. pour chaque scène, état initial, action visible, résultat ;
3. illustrer le sens complet des phrases ;
4. distinguer l'IA et le conseiller ;
5. faire évoluer les mêmes éléments ;
6. PNG seulement s'ils servent la mise en scène, processus animés en code ;
7. simplicité de la référence : ivoire, cyan, typo lisible, peu d'accents.

Regarde `assets/v01_reference_sheet.jpg` avant d'écrire une première scène : 8 images de l'extrait V01 (S11-S14)
que l'utilisateur a validé (« C'est absolument parfait »). Prends-y le niveau de lisibilité, de densité et de finition
attendu, **pas ses détails** : le contrôle sans son de cet extrait y a relevé six défauts, devenus des règles depuis
(« Grammaire de mise en scène »). Ne les recopie pas :
1. coches de l'IA et de l'humain de même forme, distinctes seulement par la couleur (#125 gris, #438 cyan) : la
   coche de l'IA prend `variant="ai"` ;
2. la ligne L5 casse sur « fausse » sans geste de personne (#146) : c'est le stylo du conseiller qui la fait casser ;
3. dates ambiguës « 09/2025 », « 03/2026 » (#258 et suivantes) : écris « sept. 2025 » ;
4. lignes grisées à 50 % environ en S13 (#300, #362) : elles se lisent « rejetées » ;
5. tampon VALIDÉ posé alors que le « ? » reste ouvert (#469) : marque-le « à poser au RDV » ;
6. bas de l'image vide sur 40 % : descends jusqu'à y ≈ 1250.

## Prérequis

Vérifie-les avant d'écrire une ligne : un manque découvert au rendu coûte une heure.

| Prérequis | Contrôle | Si absent |
|---|---|---|
| Voix finale | `build/Vxx/tts.json` et `words.json` | `make voice ID=Vxx` (voix en cache) ; sinon skill `wth-video`, recette de la voix |
| Storyboard | `make storyboard-check ID=Vxx` OK | skill `wth-storyboard` |
| Illustrations | `assets/illustrations/WTH-<carrousel>-xx.png` et génériques | skill `wth-video` (`references/environment.md`, téléchargement Drive) |
| Remotion | `motion/node_modules`, navigateur de `motion/browser.json` | `make motion-setup` |
| Disque | `df -h .` : au moins 4 Go libres | `make clean-tmp`, puis `make clean-tmp ID=<vidéo terminée>` |

## Architecture en bref

- Le temps est celui du FILM : image n = n / 30 s. Un extrait n'est qu'une fenêtre sur ce temps.
- Un temps fort du storyboard `{t, mot}` devient l'image de début de ce mot dans `words.json` (`kit.at`, à ±30 ms).
- Une clé posée à l'image f montre déjà le premier pas sur f (LEAD = 1) : l'événement est visible sur le mot même.
- Le film est un graphe de scène : des ENTITÉS persistantes (ids stables) avec des PISTES (pos, scale, rot,
  opacity, plus des pistes propres au type : draw, crack, chars…) posées par clés `{f, v, d, e}`.
- Un enfant (`parent=`) suit son parent ; l'ordre de peinture est `z` (global, pas relatif au parent).
- La mise en scène Python (`scripts/story/Vxx/`) écrit des props JSON ; la composition Remotion `Story`
  (`motion/src/story/`) les dessine. Le rendu est une fonction pure des props.
- `pipeline/story.py` recopie exactement l'évaluation des pistes de `timeline.ts` : Python connaît donc les positions
  monde au pixel près (fils, ancres, pointe du stylo). `make story-check` garde cette parité.
- Sous-titres karaoké calculés à partir de la voix (Inter Bold 64 px, ligne de base 1350, mot dit en cyan profond).
- Le film entier est refusé si une scène ou un temps fort du storyboard n'a pas d'événement.

## Deux façons de travailler

**Un film entier (nouvelle vidéo, ou V01 complète) : lance le workflow.** Il enchaîne distribution, parties écrites
deux par deux, intégration, rendu, revues, corrections, contrôle sans son et QA, en environ 4 h 30 à 7 h.

```
Workflow({scriptPath: "<dépôt>/.claude/skills/wth-story-build/workflows/build-review.wf.js",
          args: {id: "V07", root: "<dépôt>/wth-videos", parts: 3, maxRounds: 2}})
```

- `parts` : un nombre de parties (3 par défaut, scènes contiguës réparties par l'agent de distribution) ou une liste
  explicite `[["S01", "S06"], ["S07", "S13"], ["S14", "S20"]]`.
- `maxRounds` : tours de revue (2 par défaut). Le 2e tour n'a lieu que s'il reste des problèmes bloquants ou majeurs.
- `from: "review"` reprend aux revues sur un film déjà rendu ; `from: "verify"` ne fait que la QA et le contrôle sans
  son (« reprends V07 à la revue »).
- `verify: false` saute le contrôle sans son final (le workflow `batch.wf.js` du skill `wth-video` le lance lui-même :
  un workflow appelé par un autre ne peut pas en appeler un troisième).
- Le résultat contient `status`, à reporter dans `scripts/production_status.json` (skill `wth-video`, `status.py`).

Lance-le depuis la session principale, pas dans un sous-agent, pour qu'il puisse appeler `mute-verify.wf.js`. Pour
reprendre après une interruption : `Workflow({scriptPath: …, args: …, resumeFromRunId: "<runId>"})`.

**Une retouche (une scène, un temps fort, un défaut de QA) : travaille à la main**, avec la liste qui suit.

### Retouche d'une scène (« corrige S04 de V02 », « la ligne casse trop tôt dans V01 S11 »)

1. **Trie la demande.** Elle change ce que la scène montre ou veut dire (un autre objet, une autre action, une idée
   en plus) : commence par le storyboard, skill `wth-storyboard` (`revise.wf.js` avec `scenes: ["S04"]`, ou retouche
   à la main puis `make storyboard-check ID=V02`), puis remets la scène en scène. Elle porte sur l'exécution (temps,
   place, collision, taille, couleur) : la mise en scène seule change.
2. **Trouve la partie.** `grep -l S04 scripts/story/V02/*.py` : la docstring de chaque partie liste ses scènes
   (`scripts/story/V02.py` si la mise en scène tient en un seul fichier).
3. **Corrige**, puis `make story-props ID=V02` doit rester propre (étape 3 ci-dessous).
4. **Images fixes** autour du changement : `make story-stills ID=V02 FRAMES="…"` (début de scène + 2, temps fort + 12,
   dernière image). Regarde-les.
5. **Rends** : `make story ID=V02` (film, version sans sous-titres, QA).
6. **Revue légère** : `references/review-lenses.md` §10 (planches de la scène et de ses voisines).
7. **Contrôle sans son** (`mute-verify.wf.js`) seulement si le sens de la scène a changé ; sinon la QA suffit.
8. **Suivi et commit** : `status.py merge V02` avec les étapes refaites (`render`, `qa`, et `mute_verify` s'il a
   tourné), puis commit et push des sources (étape 10).
9. **Suites.** Vidéo déjà livrée : renvoie-la à l'utilisateur et dis ce qui a changé. Déjà sur Cloudinary ou
   programmée : demande son accord avant d'écraser `WTH-V02` ou de modifier la publication (skill `wth-video`,
   `references/publishing.md`).

## Procédure

### 1. Distribution : `scripts/story/Vxx/__init__.py`

Écris la mise en scène en PAQUET (un fichier par partie) : deux auteurs peuvent ainsi travailler en parallèle, et
une partie cassée s'isole. `scripts/story/Vxx.py` (un seul fichier) reste accepté, mais pas les deux à la fois.

```python
"""V07 « <titre> » : mise en scène Story. Storyboard : scripts/storyboards/V07.json (fil : <objet_fil>)."""
import importlib
import os
from types import SimpleNamespace

from pipeline.story import STYLE
from pipeline.story_kit import Figure, Kit, Sheet

PARTS = ["p1", "p2", "p3"]                      # S01-S06, S07-S13, S14-S20 : parties contiguës
ALERT_WORDS = {"fausse"}                        # mots du karaoké en rouge (facultatif)
ACOUSTIC_SNAP = {"gap": 0.2, "window": 0.08}    # temps fort après un silence : calé sur l'attaque audible
# CAPTION_GROUPS = [["à un document", "et à une date"]]   # découpes imposées (facultatif, ≤ 4 mots par groupe)
LINES = [("Revenus", "82 k€", "euro"), ("PEA", "46 k€", "bars"), ("Retraite", "à 62 ans", "mail"),
         ("Horizon", "5 ans", "none")]          # rangées de la fiche : (clé, valeur, pictogramme)


def cast(S, kit):
    """Toute la distribution, à son état de l'image 0. Ce qui arrive plus tard est déclaré avec scale=0."""
    kit.steps_marker(["Limiter", "Exiger", "Relire"])
    toi = Figure(kit, "toi", pos=[860, 800], show=False)   # à mi-hauteur de la fiche : ses coches à portée de stylo
    sheet = Sheet(n=4)
    rows = sheet.add(kit, "fiche", LINES, pos=[440, 760], show=False)
    return SimpleNamespace(toi=toi, sheet=sheet, rows=rows)


def build(S):
    kit = Kit(S)
    c = cast(S, kit)
    only = [p for p in os.environ.get("WTH_PARTS", "").split(",") if p]   # WTH_PARTS=p2 : cette partie seule
    for name in PARTS:
        if not only or name in only:
            importlib.import_module(f".{name}", __name__).part(S, kit, c)
```

- Déclare TOUTE la distribution dans `cast` : un id déclaré dans une partie est invisible pour les autres.
- Règle d'or de la série : les mêmes objets évoluent d'une scène à l'autre (règle 5). Un nouvel objet par scène
  est le premier signe d'une mise en scène qui ne tient pas le fil.
- Fixe les positions communes (colonne d'action, ligne de sol, place de la fiche) en constantes du paquet : les
  parties les partagent et les raccords tombent juste.

### 2. Parties `pN.py`

```python
"""V07, partie 2 : S07-S13."""
from pipeline.story import STYLE


def part(S, kit, c):
    f0 = round(next(s for s in S.sb["scenes"] if s["id"] == "S07")["t_start"] * S.fps)
    kit.pin(f0 - 1, {"fiche": {"pos": [440, 760], "scale": 1}, "marqueur": {"active": 1}})   # etat_initial de S07
    if S.val("toi", "scale", f0 - 1) == 0:     # partie construite seule (WTH_PARTS) : la figurine n'est pas entrée
        c.toi.enter(f0 - 10, at=[860, 800])
    f = kit.at("S07", "Ensuite", "la fiche glisse à gauche ; le repère passe sur 2")
    ...
```

- Ouvre chaque partie par `kit.pin(f0 - 1, …)` avec l'`etat_initial` de sa première scène. Épingle à f0 − 1 et
  non à f0 : un mouvement qui commence sur f0 part de la valeur de f0 − 1 et ignorerait une épingle posée sur f0.
- N'épingle jamais une figurine : sa position se change par `walk` ou `enter`, sinon son bras se décroche. Une
  partie qui utilise une figurine entrée plus tôt la fait entrer seulement si elle est absente, comme ci-dessus. Dans
  le film entier cette ligne ne fait rien ; en partie isolée, sans elle, le rig s'arrête (« hors d'atteinte (0 px) »).
- Pose CHAQUE temps fort de tes scènes : `kit.at` pour un événement, `kit.hold` pour une tenue voulue. Écris dans
  `what` ce qu'on doit voir : le titre de la bande de revue de ce temps fort l'affiche aux relecteurs.
- Tout ce qu'une partie commence finit avant la première image de la partie suivante.
- Écris dans l'ordre du temps : `fly`, `path`, les macros et la figurine lisent l'état à f − 1 au moment de l'appel.

### 3. Props : aucun trou

```bash
make story-props ID=V07 ALLOW_PARTIAL=1        # en cours d'écriture
WTH_PARTS=p2 make story-props ID=V07 ALLOW_PARTIAL=1   # une partie seule (figurines à leur état de distribution)
make story-props ID=V07                        # film entier : doit passer sans ALLOW_PARTIAL
```

Le film est prêt quand la sortie ne montre :
- ni « temps forts du storyboard sans événement » ;
- ni « scènes sans aucun temps fort » ;
- ni « attention (kit) » ;
- ni « temps forts hors début de mot ».

`make story-staging ID=V07` répond oui ou non sans rien écrire.

### 4. Images fixes aux raccords

```bash
make story-stills ID=V07 FRAMES="0 182 395 612" [ALLOW_PARTIAL=1]   # -> build/V07/story/stills/sNNNN.png
```

Avec `WTH_PARTS=p2`, les props et les images d'une partie seule vont à part (`props_film_partiel_p2*.json`,
`stills/p2/`) : deux auteurs en parallèle ne lisent jamais les images de l'autre.

Prends le début de chaque scène + 2, le résultat de chaque temps fort important (+ 12) et la dernière image. Lis-les :
chevauchements, texte illisible, éléments hors zones sûres, plus d'une action principale. Un appel coûte environ 30 s de
préparation, puis 1 à 3 s par image : groupe les images dans un seul appel.

### 5. Rendu du film

```bash
make story ID=V07     # film avec et sans sous-titres, planches de revue, puis QA ; environ 4 min + 2 min
```

- Sorties : `output/WTH-V07.mp4`, `build/V07/story/film_sans_sous_titres.mp4`, `build/V07/story_render.json`,
  `output/qa/V07.json`.
- La commande sort en code 1 si la QA échoue, alors que le film est bien rendu : lis le tableau de QA avant de conclure.
- Un seul rendu à la fois sur la machine : le verrou `build/.render.lock` fait attendre les autres. Passe toujours
  par `make` ou `python3 -m pipeline.story`, jamais par `npx remotion` directement.

### 6. Planches de revue

```bash
make review-sheets ID=V07                                  # build/V07/review/film/ : sheets, beats, phone, holds.json
make review-sheets ID=V07 REVIEW="--nocap --sheets --phone"   # build/V07/review/film_nocap/ : pour le spectateur muet
```

Les relecteurs lisent ces JPEG demi-résolution. N'extrais jamais d'images pleine résolution d'un film entier : 58 s
font 1 750 images, et c'est ce qui a rempli le disque pendant V01.

### 7. Revues

Un spectateur muet et trois critiques : continuité et référence, visuel et marque, synchro et technique. Une
évaluation compare ensuite ce que le spectateur muet a compris aux `idees_cles` du storyboard. Les consignes exactes,
l'échelle de gravité et le partage des planches sont dans `references/review-lenses.md`.

### 8. Corrections

- Corrige tous les problèmes bloquants et majeurs, et les mineurs quand c'est sûr et peu coûteux.
- Quand deux critiques se contredisent, la lisibilité sans le son et la simplicité gagnent : c'est le critère de
  l'utilisateur, et le reste se rattrape.
- Après les corrections, refais `make story` et les planches, puis regarde les images autour de chaque changement.
- Deux tours au plus. S'il reste des majeurs, consigne-les dans l'état de la vidéo et signale-les : ne boucle jamais.

### 9. Contrôle sans son

```
Workflow({scriptPath: "<dépôt>/.claude/skills/wth-story-build/workflows/mute-verify.wf.js",
          args: {id: "V07", root: "<dépôt>/wth-videos"}})
```

Deux spectateurs indépendants regardent le film sans sous-titres. Un évaluateur note chaque idée-clé du storyboard :
GOT, PARTIAL ou MISSED.

Seuil de réussite :
- au moins 85 % des `idees_cles` en GOT ;
- aucune idée principale en MISSED ;
- « oui » au critère de l'utilisateur.

En dessous : un seul tour de correction ciblé sur les scènes des idées manquées, nouveau rendu, nouveau contrôle. Si
le seuil n'est toujours pas atteint, remonte à l'utilisateur avec les points faibles plutôt que de recommencer.

### 10. QA, puis commit

```bash
make qa ID=V07        # contrôle qualité en mode story -> output/qa/V07.json + output/qa_report.md
```

Les contrôles et la façon de corriger chacun sont dans `references/qa-checklist.md`.

Une fois la QA verte, commite seulement les sources :
- `scripts/story/V07/` ;
- `motion/src/story/` et `pipeline/` s'ils ont changé ;
- `output/qa/V07.json` et `output/qa_report.md` ;
- l'état de la vidéo.

Ne commite jamais de MP4 ni `build/`. Ajoute les lignes d'attribution de la session au message de commit, puis pousse.

## Grammaire de mise en scène

Ces règles viennent de la vidéo de référence mesurée image par image et des revues de V01. Chaque règle évite un
défaut que l'utilisateur ou un spectateur muet a déjà relevé.

- **Tenir, puis éclater.** Rien ne bouge entre deux temps forts ; l'événement part sur l'image du mot. Un mouvement
  continu noie le sens.
- **Durées de la référence** (`pipeline/story.py`) :

  | Geste | Durée |
  |---|---|
  | POP | 300 ms |
  | MORPH | 350 ms |
  | MOVE | 550 ms, ease-in-out |
  | DROP | 370 ms |
  | FADE | 200 ms, texte et interface seulement |

  Aucun rebond. Une forme entre par `pop`, jamais par un fondu.
- **Jamais vide.** On passe d'une composition à l'autre par `kit.morph`, dans les mêmes images. La QA refuse une
  bande d'action vide et une image figée plus de 3,5 s, hors carte de fin.
- **Peu d'éléments.** 1 à 4 éléments actifs par temps fort ; au plus 8 primitives environ à taille téléphone. Une
  fiche de 5 lignes avec fils, dates et coches est déjà à la limite.
- **Mise en page.**
  - Le centre de l'action est vers y ≈ 800, sur 800 px de large au plus.
  - L'action reste entre x 40 et 940 et entre y 160 et 1270.
  - Descends jusqu'à y ≈ 1250 : V01 laissait vide le bas de l'image, soit 40 % du cadre.
  - Les sous-titres occupent la bande 1280-1380 ; le haut (160 px) et le bas (380 px) sont réservés à l'interface
    TikTok et Reels.
- **Texte.** 32 px au moins à l'échelle 1, phrases courtes. Écris les dates en clair (« sept. 2025 ») : « 03/2026 »
  s'est lu comme une échéance.
- **Couleurs.**
  - Fond ivoire, encre, cyan pour l'accent unique, cyan profond pour ce que fait l'humain.
  - Le rouge est réservé à l'élément d'alerte et à ses mots du karaoké.
  - Ne grise pas des lignes à 50 % pour dire « traité » : on lit « rejeté ».
- **IA et humain.**
  - La figurine encre (« toi ») est la seule à tenir un outil (stylo, tampon). L'IA agit par faisceaux pointillés.
  - Leurs coches diffèrent par la FORME (`kit.tick(..., variant="ai")` : pointillés dans un carré tireté), pas
    seulement par la couleur.
  - L'IA ne sort pas pour céder la place : l'IA prépare, l'humain vérifie. Garde-la visible, en retrait, quand
    l'humain prend la main.
- **La cause se voit.** L'outil de l'humain déclenche le changement. Dans V01, la ligne fausse cassait avant toute
  vérification ; c'est le stylo du conseiller qui doit la faire casser. Montre la preuve avant le verdict.
- **Le moment clé dure.** Un « pas de source », une case vide, une question : laisse au moins 1 s de tenue lisible.
- **Les personnages sont présents.** Un personnage arrive sur son mot (le client sur « client »), fait face à celui
  à qui il parle et reste assez longtemps pour être reconnu.
- **Pas de décision avec une question ouverte.** Pas de VALIDÉ tant qu'un « ? » reste ouvert : marque-le « à poser
  au RDV ».
- **Ouverture légère.** La première scène pose UN objet, celui du fil.
- **Repère 1-2-3 légendé.** `kit.steps_marker(["Limiter", "Exiger", "Relire"])`. Les fils partent du texte qu'ils
  prouvent, et le « ? » naît de la valeur qu'il remplace (`kit.pop(..., from_pt=…)`).
- **Image finale propre.** La dernière image de chaque scène ne montre aucune collision. La fin de chaque film est la
  carte standard `kit.outro`.
- **PNG.** Seulement ceux du carrousel de la vidéo et les génériques (`S.png` refuse les autres). Un zoom sur un PNG
  ne raconte pas un processus.

Leçons complètes et exemples : `.claude/skills/wth-storyboard/references/lessons-v01.md`.

## Exemple : une relecture au stylo

```python
def part(S, kit, c):
    toi, sheet = c.toi, c.sheet
    e = kit.at("S14", "étape", "le conseiller se place à droite de la fiche")
    pts = [sheet.world(S, i, "tick", n=e) for i in range(4)]
    toi.walk(e, toi.place_for(pts, e - 1))                 # se placer AVANT le geste (un pas automatique est saccadé)
    f = kit.at("S14", "relis", "le conseiller relit la colonne : chaque coche se trace sous la pointe")
    hits = toi.trace(f, pts)                               # image d'arrivée sur chaque point
    for i, h in enumerate(hits):
        kit.draw(f"coche{i + 1}", h, 6)                    # coche humaine : trait plein, cyan profond
    g = kit.at("S14", "corrige", "le stylo barre la valeur inventée ; elle tombe de la fiche")
    a, b = (S.to_world("fiche", q, g) for q in sheet.value_span(3))
    end = toi.strike(g, a, b, line="fiche_L4")
    kit.draw("fiche_L4", end, 12, track="fall", e="in")    # la valeur barrée se détache et tombe
    kit.pop("question", end + 2, from_pt=b)               # le « ? » naît de la valeur (déclaré en cast, scale=0)
    h = toi.stamp(kit.at("S14", "décide", "tampon PRÊT POUR LE RDV"), "tampon", shake="fiche")
    kit.pulse("question", h + 2)                           # la question reste ouverte, signalée
```

API complète : `references/story-api.md` (Story), `references/kit.md` (macros, figurine, fiche, fin standard),
`references/entities.md` (types d'entités, paramètres et pistes).

## Ajouter une entité

Ajoute un type seulement quand aucune combinaison de `shape`, `text`, `icon`, `gauge`, `counter`, `curve`… ne fait
l'affaire : chaque type de plus est du code à maintenir dans deux langages. Au plus 3 nouveaux types simples par film.

1. Dessine le composant dans `motion/src/story/entities_kit.tsx`, centré sur son origine, contour encre 4-5 px, ombre
   dure via `Hard`, couleurs par `usePalette()`, pistes lues par `r.get(piste, défaut)`.
2. Enregistre-le dans `KIT` (même fichier) et ajoute son nom au commentaire de `Entity.type` dans `types.ts`.
3. Ajoute la déclaration Python dans `pipeline/story_kit.py` (`Kit.<type>`, sur le modèle de `Kit.gauge`) et, si une
   macro a besoin de sa géométrie, mets les nombres dans `motion/src/story/geometry.json` (lu des deux côtés).
4. Si le type affiche du texte, mets-le sous une clé que la QA relit (orthographe, glyphes) : `text`, `title`,
   `labels`… (liste `STORY_TEXT_KEYS` dans `pipeline/qa.py`). Un texte sous un autre nom lui échappe.
5. Lance `make story-check` (parité Python / TypeScript + `tsc`), puis des images fixes de l'entité dans ses états
   clés.
6. Documente-la dans `references/entities.md`.
7. Rends un nouveau comportement d'un type EXISTANT optionnel (nouveau paramètre ou `variant`) : le défaut doit
   rester identique au pixel près, sinon les films déjà validés changent. Vérifie-le **avant / après** sur le même
   commit : la référence est le rendu du code d'avant ta modification, pas un fichier figé.
   ```bash
   git stash push -- motion/src/story pipeline                 # remet le code partagé d'avant ta modification
   rm -rf build/kit_demo/avant build/kit_demo/stills_demo
   python3 scripts/story/_demo_kit.py --stills 0 30 60 90 120 150 180 && mv build/kit_demo/stills_demo build/kit_demo/avant
   make story ID=V01 FROM=25.612 TO=41.309 && cp output/extraits/WTH-V01_extrait_S11-S14.mp4 build/V01/avant.mp4
   git stash pop                                               # rend ta modification
   python3 scripts/story/_demo_kit.py --stills 0 30 60 90 120 150 180
   for f in build/kit_demo/avant/*.png; do echo -n "$(basename $f) "; ffmpeg -v info -i $f \
     -i build/kit_demo/stills_demo/$(basename $f) -lavfi psnr -f null - 2>&1 | grep -o 'average:[0-9.inf]*'; done
   make story ID=V01 FROM=25.612 TO=41.309
   ffmpeg -v error -i output/extraits/WTH-V01_extrait_S11-S14.mp4 -i build/V01/avant.mp4 \
     -lavfi psnr=stats_file=build/V01/psnr.log -f null -
   awk '{for(i=1;i<=NF;i++) if($i~/^psnr_avg:/){v=substr($i,10); if(v=="inf")v=99; if(m==""||v+0<m){m=v+0;n=$1}}}
        END{print "PSNR minimal", m, "dB à", n}' build/V01/psnr.log          # attendu ≥ 45 dB
   ```
   La démo du kit (`_demo_kit.py`, S18-S20 de V01) ne change pas avec la série : c'est le banc d'essai stable.
   L'extrait V01 compte tant que `scripts/story/V01.py` contient l'extrait validé ; une fois V01 refaite sur le
   storyboard v3, compare le film V01 entier de la même façon (`make story ID=V01`, `output/WTH-V01.mp4`).
   `build/V01/baseline/` (rendu de l'extrait validé, absent d'un clone neuf) sert à `tests/story_smoke.py`.

## Ressources et disque

- **Agents.** 2 au plus en même temps par workflow (machine à 4 cœurs).
- **Rendus.** Un seul rendu Remotion à la fois, images fixes comprises : le verrou est automatique avec `make`.
- **Après chaque rendu.** `make clean-tmp` supprime les dossiers temporaires de Remotion, sous le verrou.
- **Vidéo terminée.**
  - `make clean-tmp ID=Vxx` garde les planches et supprime bandes, images téléphone et images extraites.
  - `rm -rf build/Vxx/story/stills && rm -f build/Vxx/story/muet_*.mp4`
- **Seuil.** Garde 4 Go libres (`df -h .`). En dessous, nettoie avant de rendre : un rendu interrompu par un disque
  plein laisse des fichiers partiels.

## Ce qu'il faut rapporter

À la fin, donne à l'utilisateur (en français) :
- le chemin du film et de sa version sans sous-titres ;
- le résultat de la QA ;
- le score du contrôle sans son (GOT / PARTIAL / MISSED par idée) et la réponse au critère ;
- les problèmes encore ouverts.

Mets à jour l'état de la vidéo (`spec`, `render`, `review`, `mute_verify`, `qa`) avec le script `status.py` du skill
`wth-video`.

## Références : quand les lire

| Fichier | Lis-le quand |
|---|---|
| `references/story-api.md` | tu écris ou corriges une mise en scène : chaque méthode de `Story`, ses pièges, le contrat du module |
| `references/kit.md` | tu écris une scène : macros, figurine articulée, fiche, repère 1-2-3, fin standard (table des matières en tête) |
| `references/entities.md` | tu déclares une entité ou cherches une piste : catalogue complet des types (table des matières en tête) |
| `references/review-lenses.md` | tu lances ou fais une revue : consignes des 4 regards, évaluation sans son, gravités, planches |
| `references/qa-checklist.md` | avant `make qa`, ou quand un contrôle échoue |
| `references/troubleshooting.md` | dès qu'une commande s'arrête ou qu'un rendu semble faux : erreurs connues et remèdes |
| `workflows/build-review.wf.js` | film entier : distribution, parties, intégration, rendu, revues, corrections, vérification |
| `workflows/mute-verify.wf.js` | contrôle sans son final (2 spectateurs + notation des idées-clés) |
| `assets/v01_reference_sheet.jpg` | avant la première scène : le niveau validé par l'utilisateur |

Exemples dans le dépôt :
- `scripts/story/V01.py` : extrait validé S10-S14, écrit avant le kit, donc très détaillé ;
- `scripts/story/_demo_kit.py` : démonstration du kit (S18-S20 de V01, ce n'est pas une vidéo de la série).
