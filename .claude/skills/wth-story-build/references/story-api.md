# API Story (`pipeline/story.py`)

Chaque méthode publique de la classe `Story`, avec sa signature, ce qu'elle écrit et ses pièges. Elle complète
`kit.md` : les macros du kit ne font qu'appeler ces méthodes. Chemins relatifs à `wth-videos/`.

## Sommaire

1. Le module de mise en scène (contrat)
2. Temps : `frame_of`, `word`, `word_after`, `beat`
3. Distribution et pistes : `add`, `set`, `key`, `keys`
4. Lecture de l'état : `val`, `world`, `world_scale`, `to_world`, `to_local`, `parent_space`, `wire_cubic`
5. Trajets image par image : `path`, `fly`, `along_wire`
6. Illustrations : `png`
7. Export et attributs
8. Fonctions et constantes du module
9. Pièges, en un coup d'œil

## 1. Le module de mise en scène (contrat)

`scripts/story/Vxx.py` ou le paquet `scripts/story/Vxx/__init__.py` (pas les deux : arrêt « Deux mises en scène »).
`pipeline.story.load_spec` le charge à chaque construction (aucun cache : une modification est prise tout de suite).

| Nom | Obligatoire | Rôle |
|---|---|---|
| `build(story)` | oui | Déclare la distribution et pose toutes les clés du film. Appelée une fois par construction de props, avec une `Story` neuve. |
| `ALERT_WORDS` | non | Ensemble de mots affichés en rouge dans le karaoké (comparés sans ponctuation), ex. `{"fausse", "erreur"}`. |
| `CAPTION_GROUPS` | non | Découpes de sous-titres imposées : liste de suites de groupes consécutifs, écrits comme à l'écran, ex. `[["à un document", "et à une date"]]`. 4 mots au plus par groupe (arrêt sinon). |
| `ACOUSTIC_SNAP` | non | `{"gap": 0.2, "window": 0.08}` : un temps fort dont le mot suit un silence d'au moins `gap` s est calé sur l'attaque audible de la voix, si elle tombe à moins de `window` s. Le karaoké suit le même calage. |

Paquet : les parties s'importent en relatif (`from . import p1`, ou `importlib.import_module(f".{name}", __name__)`
pour pouvoir n'en construire qu'une avec `WTH_PARTS`). L'empreinte de la mise en scène (balise `wth_spec`, QA « Rendu
Story à jour ») porte sur tous les `.py` du paquet.

## 2. Temps

Toutes les images sont des images du FILM (n / 30 s), jamais des images d'un extrait.

### `S.frame_of(i)` → image
Image de début du mot n° `i` de `words.json` : `round(start × 30)`.

### `S.word(text, near=None)` → image
Image du mot `text` (sans ponctuation, sensible à la casse). S'il apparaît plusieurs fois : le plus proche de `near`
(en secondes), sinon le premier. Arrêt « Mot « x » absent de words.json » s'il n'existe pas.

N'enregistre AUCUN temps fort : un événement posé sur `S.word` ne compte pas pour la couverture du storyboard. Sers-t'en
pour un geste secondaire, jamais à la place d'un temps fort.

### `S.word_after(text, frame)` → image
Premier mot `text` qui commence à l'image `frame` ou après. Pour un mot repéré par rapport à un temps fort (« le
« que » qui suit « Exige » ») plutôt que par un temps absolu.

### `S.beat(scene, mot, what="")` → image
Temps fort du storyboard (= `kit.at`). Étapes :
1. Cherche dans la scène le PREMIER temps fort dont le `mot` est égal à `mot` (ponctuation retirée, ’ = ').
2. Cherche dans `words.json` l'occurrence de ce mot la plus proche du `t` du storyboard. Arrêt si elle est à plus de
   30 ms (« mot introuvable à ce temps dans words.json »).
3. Avec `ACOUSTIC_SNAP`, recale éventuellement l'image sur l'attaque audible (`meta.beats_snapped_to_attack`).
4. Enregistre le temps fort dans `S.beats`, donc dans `meta.beats` : couverture du storyboard, images clés x264
   forcées, titres des bandes de `make review-sheets`.

Arrêts possibles : « Scène Sxx absente du storyboard », « Sxx : pas de temps fort sur « mot » dans le storyboard ».

**Pièges.**
- Casse : « Exige » ≠ « exige ». Recopie le `mot` du storyboard ; la ponctuation peut rester (« relis, »).
- Nombres : le mot de `words.json` est « 4 600 € » (espaces insécables) ; écris `"4 600 €"`, les espaces sont normalisées.
- Deux temps forts sur le même mot dans une scène : `beat` ne trouve que le premier. Pour le second, prends
  `S.word(text, near=t)` ou `S.word_after(text, f)`. Mieux : fais déplacer le second sur un mot voisin dans le
  storyboard.
- `what` est lu par les relecteurs : écris l'événement visible, pas une intention.

## 3. Distribution et pistes

### `S.add(id, type, z=0, parent=None, **p)` → id
Déclare une entité.
- `type` : un type de `entities.md`.
- `z` : ordre de peinture GLOBAL ; à égalité, l'ordre de déclaration.
- `parent` : entité déjà déclarée.
- `**p` : paramètres statiques (textes, tailles, couleurs, ancres). Ils ne changent jamais pendant le film.

Arrêts : « Entité « x » déjà déclarée », « x : parent « p » à déclarer avant ».

**Piège.** Sans `set`, une entité vaut pos [0, 0], scale 1, opacity 1 : elle est visible dans le coin haut gauche dès
l'image 0. Pose toujours sa position, et `scale=0` si elle arrive plus tard.

### `S.set(id, **tracks)`
Valeurs initiales des pistes (leur état avant toute clé). Sur une piste qui a déjà des clés, `set` remplace seulement la
valeur initiale : les clés restent.

Une couleur qui doit passer en fondu se pose en hex (`S.set("jauge", fill=STYLE["cyan"])`) : entre deux noms de
palette, la couleur bascule d'un coup.

### `S.key(id, track, f, v, d=0, e="out", arc=None)`
Clé : à partir de l'image `f`, la piste va de sa valeur à f − 1 vers `v` en `d` images, avec l'assouplissement `e`.
- **LEAD = 1.** L'image f montre déjà le pas 1/d ; la valeur `v` est atteinte à l'image f + d − 1. Le segment suivant
  peut commencer à f + d (c'est ce que renvoient les macros).
- **`d=0`.** Saut instantané à l'image f.
- **Assouplissements.** `linear`, `out` (cubique, le défaut), `in`, `inOut`, `outQuad`, `inOutSine`. Aucun ne
  rebondit. Un autre nom arrête la construction.
- **`arc`** (px, points [x, y] seulement) : le trajet bombe vers le haut de `arc` à mi-course.
- **Valeurs.** Un nombre, une liste de nombres (interpolée terme à terme) ou une couleur `#RRGGBB` (interpolée si
  les deux bouts sont en hex). Sinon la valeur bascule à la première image du segment (textes, noms de palette).
- **Ordre.** Les clés sont rangées par image, quel que soit l'ordre des appels. Une clé posée pendant un segment en
  cours le coupe et repart de la valeur de f − 1 : pas de saut, mais une vitesse cassée.
- **Même image.** Deux clés sur la même image : la dernière posée gagne.

Arrêt « id.piste : valeur initiale manquante (Story.set) » si la piste n'a pas de valeur initiale. Seules `pos`,
`scale`, `rot`, `opacity`, `sx` et `sy` ont un défaut ; les macros du kit posent celle qui manque (`kit.ensure`).

### `S.keys(id, f, d=0, e="out", arc=None, **tracks)`
Plusieurs pistes avec le même segment : `S.keys("doc1", f, 9, "out", scale=1, opacity=1)`. L'`arc` ne s'applique
qu'à `pos`.

## 4. Lecture de l'état

Ces méthodes évaluent les pistes TELLES QU'ELLES SONT AU MOMENT DE L'APPEL. Une clé posée plus tard, même à une image
antérieure, n'est pas vue : écris la mise en scène dans l'ordre du temps.

| Méthode | Retour |
|---|---|
| `S.val(id, track, n, fallback=None)` | valeur de la piste à l'image n (défaut : `fallback`, ou la valeur neutre de pos/scale/rot/opacity/sx/sy) |
| `S.world(id, n)` | matrice monde [a, b, c, d, e, f] (parents compris, `sx`/`sy` compris) |
| `S.world_scale(id, n)` | échelle monde (parents compris) |
| `S.to_world(id, pt, n)` | point local de `id` → point monde (1080 × 1920) |
| `S.to_local(parent, pt, n)` | point monde → repère local de `parent` |
| `S.parent_space(id, pt, n)` | point monde → repère du PARENT de `id` (le monde s'il n'en a pas) : la valeur à donner à sa piste `pos` |
| `S.wire_cubic(wire_id, n)` | les 4 points de contrôle monde d'un fil (`wire`) à l'image n, ancres `a`/`b` ou pistes `pa`/`pb` |

**Pièges.**
- `to_local` et `parent_space` arrêtent sur « matrice non inversible » si le parent est à l'échelle 0 à cette image.
  Calcule à une image où il est visible.
- `wire_cubic` ignore la piste `via` d'un fil. Un fil coudé se calcule à la main (voir `via_path_point` dans
  `scripts/story/V01.py`).

## 5. Trajets image par image

Ils posent UNE clé par image (d = 1, linéaire), exprimée dans le repère du parent à chaque image : le trajet monde est
exact même si le parent bouge pendant ce temps. Contrepartie : des props plus lourdes. Réserve-les aux trajets qu'aucune
clé simple ne donne.

### `S.path(id, f, d, e, point_at, scale_at=None, offset=(0, 0))`
Pendant `ceil(d)` images à partir de f, l'entité est au point monde `point_at(p)`, p étant la progression assouplie
(0 → 1).
- `scale_at(p)` : l'échelle MONDE voulue (elle est divisée par celle du parent).
- `offset` : un décalage monde fixe, ou une fonction de p.

### `S.fly(id, f, d, e="inOut", to=None, scale=None, arc=0)`
Vol monde : de la position et de l'échelle monde à l'image f − 1 vers le point monde `to` (et l'échelle monde
`scale`), en arc de `arc` px. Sert à faire passer un objet d'un parent à un autre sans saut (re-parentage).

### `S.along_wire(id, wire_id, f, d, e, t0, t1, at_frame, offset=(0, 0), scale=None)`
L'entité glisse le long du fil `wire_id`, de la fraction de longueur `t0` à `t1`. La géométrie du fil est figée à
l'image `at_frame`. Exemple : la puce-date de V01 qui descend le fil de preuve.

**Pièges.**
- Après un trajet, la piste `pos` reste sur la dernière valeur. Une clé posée par-dessus dans la même plage d'images
  se mélange aux clés image par image : enchaîne APRÈS la fin du trajet.
- Le départ est lu à f − 1 : l'entité doit déjà être à sa place à ce moment-là.

## 6. Illustrations

### `S.png(name, keep_largest=False)` → meta
Prépare `assets/illustrations/<name>.png` pour le fond ivoire. Les illustrations ont été rendues pour un fond noir,
avec un halo cuit.
- **Alpha strict.** Le halo est coupé, les couleurs de bord sont reprises des pixels opaques voisins et l'image est
  recadrée.
- **`keep_largest=True`.** Ne garde que la plus grande pièce (ex. la tête de `AI` sans son cube détaché).
- **Cache.** `motion/public/generated/story/Vxx/` ; `PNG_VERSION` est à incrémenter si la recette change.
- **Retour.** `{"src", "w", "h", "crop", "key"}`.

Déclaration :

```python
ai = S.png("AI", keep_largest=True)
w = 170
S.add("ia", "png", z=4, src=ai["src"], w=w, h=round(w * ai["h"] / ai["w"]), saturate=0.85,
      contact=dict(w=round(w * 0.72), h=26, dy=4, blur=10, alpha=0.2))
```

Arrêts :
- « Illustration absente » : télécharge-la (skill `wth-video`, `references/environment.md`).
- « illustration … d'un autre carrousel » : règle de la série, la vidéo n'utilise que son propre carrousel
  (`WTH-<source>-xx`) et les génériques.

## 7. Export et attributs

- `S.entities()` : la liste des entités pour les props (appelée par le constructeur).
- Attributs utiles :
  - `S.video_id` ;
  - `S.fps` (30), `S.width` (1080), `S.height` (1920) ;
  - `S.words` (mots de `words.json`) ;
  - `S.sb` (le storyboard : `S.sb["scenes"]`, `S.sb["cast"]`…) ;
  - `S.ents` (entités déclarées) ;
  - `S.beats` (temps forts posés) ;
  - `S.assets` (PNG préparés).
- Image de début d'une scène : `round(next(s for s in S.sb["scenes"] if s["id"] == "S07")["t_start"] * S.fps)`.

## 8. Fonctions et constantes du module

| Nom | Rôle |
|---|---|
| `STYLE` | palette : `bg` #F6F0E4, `ink` #1E1416, `cyan` #19B3C7, `deep` #0A7487, `light` #D3F0F6, `paper` #FFFDF8, `grey` #DDD5C6, `red` #C8102E, `slot` #F4EEE3, `rule` #E6DECF, `ai_tick` #8E8887, grille 36 px #ECE4D4, sous-titres |
| `GEOM` | `motion/src/story/geometry.json` (figurine, stylo, tampon, étiquette, coche, repère) |
| `POP` 9, `SCALE` 10, `MORPH` 11, `MOVE` 16, `DROP` 11, `TILT` 14, `FADE` 6, `DRAW` 9, `STRETCH` 6 | durées de la référence, en images |
| `LEAD` | 1 (voir `key`) |
| `text_width(text, size, weight=600)` | largeur en px (Inter ; graisses 600, 700 ou 800 seulement) : mesure des étiquettes, des pilules et de `w` pour `mark`/`under` |
| `wire_cubic(a, b, sag, tension=0.45)`, `cubic_at(c, t)`, `point_at_length(c, frac)` | géométrie des fils, comme le rendu |
| `line_crack_point(p, pt, crack=1)` | point de la moitié droite d'une rangée `line` cassée |
| `eval_track(track, n)`, `local_matrix`, `mat_mul`, `mat_apply`, `mat_inv` | évaluation brute (copie de `timeline.ts`) |
| `check_storyboard(id)` | contrôle du storyboard (`make storyboard-check`) → (erreurs, avertissements) |
| `check_staging(id)` | le film entier est-il rendable ? (`make story-staging`) |

## 9. Pièges, en un coup d'œil

| Symptôme | Cause | Remède |
|---|---|---|
| Un élément apparaît dans le coin haut gauche dès l'image 0 | `add` sans `set(pos=…, scale=0)` | déclare-le à sa place, `scale=0` |
| Un mouvement ignore l'état imposé au début d'une partie | `kit.pin(f)` et une clé sur la même image f | épingle à f − 1 |
| Le bras de la figurine se détache | clé manuelle (ou `pin`) sur la figurine, son bras ou son stylo | uniquement les méthodes de `Figure` |
| Couleur qui saute au lieu d'un fondu | nom de palette au lieu d'un hex | `S.set(id, fill=STYLE["cyan"])` puis clé en hex |
| Trajet calculé faux | `fly`/`path`/`to_world` appelés avant les clés antérieures | écrire dans l'ordre du temps |
| « mot introuvable à ce temps » | `t` du storyboard à plus de 30 ms, ou casse / mot différents | corriger le storyboard (`make storyboard-check`) |
| Second temps fort d'une scène sur le même mot jamais déclenché | `beat` prend le premier | `S.word(..., near=t)` ou changer de mot |
| Élément d'un enfant caché sous un autre objet | `z` global | donner à l'enfant un `z` supérieur |
| « valeur initiale manquante » | `key` sur une piste sans `set` | `S.set(id, piste=…)` |
