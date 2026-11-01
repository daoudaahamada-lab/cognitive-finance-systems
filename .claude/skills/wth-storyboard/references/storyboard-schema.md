# Le storyboard : champs, contraintes, modèle Markdown

Deux fichiers par vidéo, versionnés :
- `wth-videos/scripts/storyboards/Vxx.json` : lu par la mise en scène (`Story.beat`, `kit.at`), par `--check` et par
  le contrôle sans son ;
- `wth-videos/scripts/storyboards/Vxx.md` : la même chose, lisible par l'utilisateur.

Le JSON fait foi. Schéma machine : `storyboard.schema.json` (vérifié par `scripts/soft_check.py`). Le contrôle
`python3 -m pipeline.story Vxx --check` (`make storyboard-check ID=Vxx`) refuse un storyboard qui casserait la mise en
scène ; ce qu'il vérifie est marqué **[check]** ci-dessous.

## 1. Racine

| Champ | Requis | Contenu |
|---|---|---|
| `version` | oui **[check]** | « v1 · 2026-10-21 · révisé après le test sans son ». Monter la version à chaque révision. |
| `angle` | conseillé | le parti pris, puis « Réponse aux 7 points » : une ligne par règle du brief, concrète (quelle scène, quel geste). |
| `thread` | oui **[check]** | le fil conducteur en 3 à 6 phrases : l'objet suivi, son état initial, ses transformations, son état final. |
| `objet_fil` | oui (alerte **[check]** s'il manque) | `{id, description}` : id de la distribution qui porte le fil, ce qu'il est, où il se pose, ce qu'il devient. |
| `cast` | oui **[check]** | la distribution (§ 2). |
| `style` | oui **[check]** | ce qui est propre au film (à quoi sert le rouge, places fixes, PNG retenus) ; le reste renvoie à `style.md`. |
| `scenes` | oui **[check]** | les scènes (§ 3). |
| `idees_cles` | oui **[check]** | 6 à 10 idées (§ 4). |
| `entites_nouvelles` | si besoin | au plus 3 entités simples à créer avant la mise en scène : `{nom, description, pourquoi}`. |
| `test_sans_son` | oui à la fin (alerte **[check]** s'il manque) | résultat du test du spectateur muet (§ 5). |
| `risks` | conseillé | risques et replis : ce qui peut mal se lire, et quoi faire à la place. |
| `excerpt` | facultatif | `{t_start, t_end, why}` : un extrait de 10 à 15 s sur des débuts de phrase, si une validation rapide est utile. |
| `revisions` | après `revise.wf.js` | `[{version, scenes, pourquoi}]`. |

## 2. Distribution (`cast`)

Chaque élément : `{id, name_fr, look, source, evolution}` (+ `entite` conseillé).
- `id` : minuscules et `_` (`pastille`, `toi`, `ia`, `fiche`). Ce sont ces ids qu'on cite dans `elements`.
- `look` : forme, taille en px à 1080, jetons de couleur, contour, ombre, texte affiché exact.
- `source` : « code », un PNG autorisé (« AI.png », « WTH-006-03.png ») ou « PNG + code ».
- `entite` : le type Story et la macro qui le réalisent (« figure ink + Figure.tap/stamp », « line ×5 via Sheet ») ou
  « NOUVEAU : … » renvoyant à `entites_nouvelles`.
- `evolution` : son parcours, scène par scène (« S01 : … S05 : … »). C'est la réponse au point 5 du brief.

La distribution récurrente (« Toi », IA, objet du fil, repère, carte de fin) suit `series-bible.md`.

## 3. Scènes (`scenes`)

Champs **[check]** : `id, t_start, t_end, texte, elements, etat_initial, action, resultat, transition, beats,
lecture_sans_son`. Conseillé : `segment` (accroche, contexte, point1, point2, point3, chute, cta).

| Contrainte | Vérifiée par |
|---|---|
| `id` = S01, S02… dans l'ordre | schéma |
| S01 commence à 0 ; chaque `t_start` = `t_end` de la précédente (±1 ms) | **[check]** |
| chaque `t_start` tombe sur le début d'un mot de `words.json` (±30 ms) | **[check]** |
| la dernière `t_end` ≥ fin du dernier mot ; la prendre égale à la durée de `build/Vxx/audio.wav` (`prep.json` : `duree`) | **[check]** |
| `texte` mis bout à bout = texte du script, exactement (NFC, espaces normalisées, mêmes apostrophes ’ et points de suspension …) | **[check]** |
| au moins un temps fort par scène | **[check]** |

Découpage : une scène par phrase ou par idée, 14 à 22 scènes pour ~57 s. La dernière scène est la phrase d'appel
seule (« Abonne-toi pour comprendre ton argent. ») : c'est la carte de fin, seule scène que la QA dispense du contrôle
d'image figée. Une phrase longue peut faire deux scènes
(V01 : « Mais une IA peut produire une réponse fluide… et fausse. » en une scène, « Le vrai problème… : » et « ton temps
part… » en deux).

Champs de sens :
- `etat_initial` : ce qu'on voit à la première image de la scène (= résultat de la précédente). Assez précis pour qu'un
  auteur puisse poser `kit.pin` dessus : positions, tailles, états.
- `action` : l'action visible, en verbes visuels, dans l'ordre.
- `resultat` : ce qu'on voit à la fin, et ce qui a changé.
- `transition` : sur quel mot et comment on passe à la scène suivante (ce qui sort, ce qui reste, ce qui se déplace).
- `elements` : ids de la distribution visibles.
- `lecture_sans_son` : ce que comprend un spectateur sans le son. Honnête : si c'est faible, la scène est à revoir.

### Temps forts (`beats`)

`{t, mot, evenement}` **[check]** :
- `t` = début exact du mot dans `words.json` (le copier de `build/Vxx/storyboard/words.tsv`), ±30 ms, et dans la
  scène.
- `mot` = le mot tel qu'il est dans `words.json`. La comparaison ignore la ponctuation et les espaces insécables
  (« fausse. » = « fausse » ; une espace insécable vaut une espace) mais **respecte la casse** (« Mais » ≠ « mais »).
- `evenement` = ce qui bouge : verbe visuel, éléments, positions (x, y à 1080 × 1920), tailles, durée et assouplissement
  (`motion-grammar.md`). « Tenue : rien ne bouge » pour une tenue voulue.

Règles qui ne se voient pas au contrôle mais cassent la suite :
- **Deux temps forts sur le même mot dans une scène** : `Story.beat` ne trouve que le premier. Un mot répété (« L’IA
  … l’IA ») se résout par le temps, mais pas deux fois dans la même scène. (`soft_check.py` le refuse.)
- **Chaque temps fort sera mis en scène.** Le film entier est refusé s'il manque un temps fort à la mise en scène :
  n'écrire que des temps forts qu'on veut voir (une tenue se pose avec `kit.hold`).
- **Pas plus de 3 s sans temps fort** (QA : image figée > 3,5 s refusée, sauf la carte de fin).
- **Une action principale par temps fort**, 1 à 4 éléments actifs.

## 4. Idées-clés (`idees_cles`)

6 à 10 `{id, idee, scenes, principale}` **[check]** (`id`, `idee`, `scenes` requis ; scènes existantes ; 6 à 10).
- `idee` : ce qu'un spectateur muet doit comprendre, formulé comme un constat visible (« la seule ligne sans document
  casse, alors que l'IA l'avait cochée »), pas comme le texte de la voix.
- `scenes` : les scènes qui la montrent.
- `principale: true` pour les idées des trois points et de la chute (au moins une par segment, `soft_check.py`
  l'alerte). Le contrôle sans son de la vidéo finale exige au moins 85 % d'idées GOT et **aucune idée principale
  MISSED**.
- Elles servent deux fois : au test muet du storyboard (ici) et au contrôle sans son du film rendu (skill
  `wth-story-build`). Les écrire pour qu'un évaluateur puisse trancher GOT / PARTIAL / MISSED.

## 5. Test sans son (`test_sans_son`)

`{message_reconstruit, idees, bilan, changements}` :
- `message_reconstruit` : le message tel que le spectateur muet l'a reconstitué (citation) ;
- `idees` : `[{id, score: GOT|PARTIAL|MISSED, preuve}]` pour chaque idée-clé ;
- `bilan` : contresens et flous relevés ;
- `changements` : `[{id: scène, lecture: ce qu'il a lu, changement: ce qu'on a modifié}]`.

## 6. Modèle Markdown (`Vxx.md`)

En français, dans cet ordre (V01.md en est l'exemple complet) :

```markdown
# Vxx · Storyboard (vN) : « <titre> »

WealthTech Horizon · vertical 1080×1920 · 30 i/s · <durée> s · voix finale · animation Remotion (formes plates en code + PNG de verre).

Critère de réussite : sous-titres masqués, on comprend l’action principale de chaque passage et on voit ce qui change.

## Fil conducteur
<thread>  ·  **Objet du fil** : <objet_fil.description>

## Idées-clés (contrôle sans son)
| Id | Idée | Scènes | Principale |
|---|---|---|---|

## Parti pris et réponse aux 7 corrections
<angle : 1) … 7) …>

## Test sans son
> <message_reconstruit>
<bilan>
| Scène | Lecture muette | Ce qui change |
|---|---|---|

## Distribution
### <name_fr> · `<id>`
- **Aspect** : … - **Source** : … - **Entité** : … - **Évolution** : …

## Style
<style>

## Storyboard scène par scène
### S01 · 0,00 → 1,17 s · « <texte> »
**État initial** : …
| Temps | Texte | Éléments visibles | Action | Résultat | Transition |
|---|---|---|---|---|---|
**Temps forts**
- 0,00 s · « Client » : …
**Sans le son** : …

## Entités nouvelles
## Risques et replis
## Extrait recommandé (facultatif)
## Révisions (après revise.wf.js)
```

Nombres en notation française dans le `.md` (« 26,38 s ») ; le JSON garde des nombres (`26.378`).
