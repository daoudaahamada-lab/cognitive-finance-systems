# Kit d'entités Story : paramètres et pistes

Source : `motion/src/story/entities_kit.tsx` (types génériques) et `entities.tsx` (types de V01 : tick, marker…).
Géométrie partagée : `motion/src/story/geometry.json` (lue aussi par `pipeline/story.py`, `GEOM`).
Planche de contrôle (locale, non versionnée : `build/` est ignoré) : `build/kit_demo/kit_sheet.png`, images 0/20/40/60.
Chemins de code ci-dessous : relatifs à `wth-videos/`.

## Conventions communes

- Déclaration côté Python : `S.add(id, type, z=…, parent=…, **params)`, puis `S.set(id, piste=valeur)`, puis
  `S.key(...)` / `S.keys(...)`. Un `S.key` sur une piste sans `S.set` préalable échoue, sauf pos, scale, rot, opacity,
  sx et sy.
- Pistes communes à toutes les entités : `pos [x, y]`, `scale`, `sx`, `sy`, `rot` (degrés), `opacity`, `z`.
- Chaque entité se dessine centrée sur son origine, dans le repère local. Un enfant (`parent=`) suit son parent
  (translation, rotation, échelle).
- **Couleurs** : un nom de palette (`ink`, `cyan`, `deep`, `light`, `paper`, `grey`, `slot`, `rule`, `red`, `aiTick`
  ou `ai_tick`), `none`, ou un hex `#RRGGBB`.
  - Une piste de couleur ne s'interpole qu'entre deux hex (par exemple `STYLE["cyan"]` vers `STYLE["red"]`).
  - Avec un nom de palette, la couleur bascule d'un coup à la première image du segment.
- **Ombre dure** : `shadow` en px à l'écran, vers le bas-droite.
  - L'ombre garde cette direction quelle que soit la rotation : elle n'annule que la rotation, pas l'échelle.
  - Une entité à l'échelle 0,5 a donc une ombre de 3 px, comme pill ou doc.
- **Contours** : encre, 4 à 5 px. Les textes sont en Inter : 600 SemiBold, 700 Bold, 800 ExtraBold.
- **Textes visibles et QA** : la QA lit les clés `text`, `title` et `labels` des paramètres. Mettre le texte affiché
  dans ces clés.

## shape

Rectangle, rectangle arrondi, cercle, ellipse ou polygone. Le contour peut être tracé progressivement.

| Paramètre | Défaut | Rôle |
|---|---|---|
| `kind` | `round` | `rect`, `round`, `circle`, `ellipse` ou `poly` |
| `w`, `h` | 200, `w` | taille ; pour `circle`, `w` est le diamètre |
| `r` | 18 | rayon des coins (`round`) |
| `pts`, `closed` | —, true | sommets du polygone (repère local) ; ouvert si `closed=False` |
| `fill`, `stroke` | paper, ink | couleurs de l'aplat et du contour |
| `sw` | 4 | épaisseur du contour |
| `shadow` | 6 | ombre dure ; 0 pour aucune ombre |
| `dash` | — | pointillé du contour, par exemple `[14, 10]` |

**Pistes :**
- `w`, `h`, `r` : taille et rayon.
- `fill`, `stroke` : couleurs.
- `draw` (0→1) : le contour se trace depuis le haut ou le premier sommet.
- `fillOp` : opacité de l'aplat et de l'ombre. Sans piste, elle vaut 0 tant que `draw` < 1, puis 1 quand le contour
  se ferme.

## text

Texte libre, sur une ou plusieurs lignes (séparées par `\n`).

| Paramètre | Défaut | Rôle |
|---|---|---|
| `text` | — | le texte |
| `size`, `weight` | 40, 700 | corps et graisse |
| `color` | ink | couleur |
| `anchor` | `middle` | `start`, `middle` ou `end` |
| `lh` | 1,18 | interligne, en multiple de `size` |
| `spacing` | — | approche, en px |
| `w` | — | largeur mesurée par `text_width(text, size, weight)` ; nécessaire pour `mark` et `under` |
| `markColor`, `underColor` | light, deep | couleurs du surligneur et du soulignement |

**Pistes :**
- `chars` : machine à écrire. Les sauts de ligne ne comptent pas. La suite du texte est posée en transparent, donc un
  texte centré ne glisse pas pendant la frappe.
- `text` : bascule vers un autre texte.
- `color` : couleur.
- `mark` (0→1) : un surligneur tiré de gauche à droite derrière le texte.
- `under` (0→1) : un soulignement tracé de gauche à droite.

## icon

Pictogramme seul, ou posé sur un disque.

| Paramètre | Défaut | Rôle |
|---|---|---|
| `name` | — | voir la liste des pictogrammes plus bas |
| `s` | 64, ou `disc` × 1,15 | taille de la boîte du pictogramme |
| `color` | ink | couleur du trait |
| `sw` | auto | épaisseur du trait |
| `disc` | — | rayon du disque ; absent = pictogramme seul |
| `fill` | cyan | couleur du disque |
| `shadow` | 6 (3 si `disc` < 25) | ombre dure du disque |
| `ringColor` | deep | couleur de l'anneau |

**Pistes :**
- `color` : couleur du pictogramme.
- `fill` : couleur du disque.
- `ring` (0→1) : un anneau se trace autour du disque, depuis midi (l'élément est « coché »).

**Pictogrammes.**
- Avant le kit : euro, bars, mail, shield, cal, building (le sceau plein du cabinet), check, person.
- Ajoutés par le kit : rewind (◀◀), clock, house, bank (temple au trait), coin, percent, lock, cart, moon, pause,
  warning, phone, plus, minus, arrow (→ ; pour une autre direction, utiliser `rot`).

## sector

Cadran et secteur de temps, par exemple « le secteur de 10 minutes ».

| Paramètre | Défaut | Rôle |
|---|---|---|
| `r` | 120 | rayon |
| `unit` | 60 | unités par tour ; 0 = midi, sens horaire |
| `face` | paper | couleur du cadran. `none` : secteur seul, sans ombre ni graduations, à poser sur le cadran d'un PNG |
| `fill` | deep | couleur du secteur |
| `alpha` | 1 (0,6 si `face=none`) | opacité du secteur |
| `ticks` | 12 (0 si `face=none`) | graduations ; une sur trois est plus longue |
| `hand` | true | aiguille au bout du secteur (seulement avec un cadran) |
| `edge` | 3 (0 si `face=none`) | contour encre du secteur |
| `sw`, `shadow` | 5, 6 | contour et ombre du cadran |

**Pistes :**
- `start` : début du secteur, en unités. Pour « de :50 à :00 », `start=50`.
- `value` : taille du secteur, en unités. 0 = rien ; une valeur ≥ `unit` donne un disque plein.
- `fill` : couleur.

**Exemple :** `S.set("dix", start=50, value=0)` puis `S.key("dix", "value", f, 10, d, "linear")`. Le secteur se remplit
au rythme du stylo.

## gauge

Barre de temps ou de budget.

| Paramètre | Défaut | Rôle |
|---|---|---|
| `w`, `h` | 600, 48 | taille ; mettre `h` > `w` pour une barre verticale |
| `r` | min(14, côté/2) | rayon des coins |
| `dir` | `right` | côté d'où part le remplissage : `right`, `left`, `up` ou `down` (voir après le tableau) |
| `fill` | cyan | couleur du remplissage |
| `empty` | paper | couleur de la partie vide |
| `segments` | 0 | séparateurs encre : blocs, futurs jetons |
| `marks` | [] | repères (fractions comptées depuis l'origine du remplissage), par exemple `[0.8]` pour un budget |
| `sw`, `shadow` | 4, 6 | contour et ombre |

**Valeurs de `dir` :**
- `right` : la barre se remplit de gauche à droite.
- `left` : le reste est collé à droite ; quand `value` baisse, la barre « fond » vers la droite.
- `up` et `down` : les mêmes, à la verticale.

**Pistes :**
- `value` (0→1) : part remplie.
- `fill` : couleur. Par exemple, une clé hex de cyan vers rouge au moment du dépassement.
- `w`, `h` : taille.

## counter

Nombre interpolé, en typographie française (12 500 €, 3,5 %, −40 %).

| Paramètre | Défaut | Rôle |
|---|---|---|
| `size`, `weight` | 96, 800 | corps et graisse |
| `color` | ink | couleur |
| `decimals` | 0 | nombre de décimales |
| `prefix`, `suffix` | "" | unités. Un espace collé à l'unité devient insécable : passer `suffix=" €"` |
| `sign` | false | affiche « + » devant les valeurs positives |
| `anchor` | `middle` | ancrage du texte |

**Pistes :**
- `value` : le nombre, recalculé à chaque image.
- `color` : couleur.

**Format :**
- espace fine insécable U+202F entre les milliers ;
- virgule décimale ;
- vrai signe moins U+2212 ;
- chiffres à chasse fixe, pour que la largeur ne tremble pas pendant l'interpolation.

`formatFr(v, decimals, sign)` est exporté pour un usage hors du compteur.

## curve

Courbe tracée progressivement : frais, inflation.

| Paramètre | Défaut | Rôle |
|---|---|---|
| `pts` | — | points en repère local, y vers le bas |
| `smooth` | true | Catmull-Rom, qui passe par chaque point |
| `color`, `sw` | deep, 7 | couleur et épaisseur du trait |
| `area` | — | couleur de l'aire sous la courbe (par exemple `light`), limitée à la partie tracée |
| `base` | y maximal des points | ligne de base de l'aire et de l'axe horizontal |
| `axes` | false | axes encre en L avec flèches ; `{pad}` règle la marge (24) |
| `dot` | true | pastille sur la tête de la courbe |
| `dash` | — | pointillé du trait |

**Pistes :**
- `draw` (0→1) : part de la longueur tracée. La tête et l'aire suivent.
- `color` : couleur.

## seesaw

Planche à bascule.

**Géométrie.**
- L'origine est le sommet du pivot, au milieu du dessous de la planche.
- La planche occupe y ∈ [−h, 0].
- Le pivot (triangle) va de 0 à `baseH` ; une ligne de sol est tracée à `baseH`.

| Paramètre | Défaut | Rôle |
|---|---|---|
| `w`, `h` | 640, 24 | longueur et épaisseur de la planche |
| `fill` | ink | couleur de la planche (encre, comme dans le storyboard V01) |
| `base` | paper | couleur du pivot |
| `baseW`, `baseH` | 120, 90 | largeur et hauteur du pivot |
| `ground` | `baseW` + 120 | largeur du sol ; 0 = pas de sol |
| `sw`, `shadow` | 5, 6 | contours et ombre |

**Bascule.** Elle se fait avec la piste `rot` de l'entité, en degrés ; une valeur positive fait descendre le côté
droit.
- Les objets posés sur la planche sont des enfants (`parent="bascule"`, `pos=[x, -h - demi-hauteur]`) : ils
  basculent avec elle.
- Le pivot est contre-tourné et reste droit sur le sol.
- Sur un sol, l'ombre du pivot ne part que vers la droite.

## cursor

Le pointeur, c'est-à-dire la main du conseiller à l'écran. L'origine est la pointe de la flèche : `pos` est donc le
point cliqué.

| Paramètre | Défaut | Rôle |
|---|---|---|
| `size` | 64 | hauteur de la flèche |
| `fill`, `edge` | ink, paper | flèche encre, liseré papier de 3 px (lisible sur l'encre) |
| `shadow` | 5 | ombre dure |

**Pistes :**
- `press` (0→1) : la flèche s'enfonce (× 0,85) et l'ombre se réduit.
- `ring` (0→1) : deux ondes deep partent de la pointe ; c'est le clic.

**Un clic type :**
- `press` 0→1 en 3 images, puis retour en 4 ;
- `ring` 0→1 en environ 18 images, avec `e="out"`.

## endcard

Carte de fin : une carte avec un titre et un bouton pilule.

| Paramètre | Défaut | Rôle |
|---|---|---|
| `w`, `h`, `r` | 620, 560, 32 | taille et rayon de la carte |
| `title`, `titleSize`, `titleY` | —, 44, auto | titre (Bold) ; `titleY` vaut par défaut −h/2 + 150, ou + 214 avec `icon` |
| `icon` | — | pictogramme sur un disque cyan au-dessus du titre (par exemple `building`) |
| `labels`, `labelSize` | [], 30 | lignes sous le titre (SemiBold, deep), par exemple « Abonne-toi pour la suite » |
| `text` | — | libellé du bouton (par exemple « S’abonner ») ; pas de bouton s'il est absent |
| `bw`, `bh`, `by`, `bsize` | 380, 112, bas de la carte, 46 | taille, position et corps du bouton |
| `fill`, `bfill` | paper, cyan | couleurs de la carte et du bouton |
| `shadow` | 8 | ombre dure de la carte |

**Pistes :**
- `w`, `h` : taille ; la carte peut naître d'une autre forme.
- `btn` : échelle du bouton, 0→1.
- `press` (0→1) : le bouton s'enfonce dans son ombre de 8 px.
- `title` : opacité du titre, du pictogramme et des lignes.

## crowd

Une foule de n petites figurines (`ClientGlyph`, la même figurine que le client), éventuellement reliées à l'origine.

| Paramètre | Défaut | Rôle |
|---|---|---|
| `n` | 6 | nombre de figurines |
| `h` | 48 | hauteur d'une figurine |
| `layout` | `ring` | `ring` ou `row` ; `pts` impose des positions |
| `r`, `a0`, `span` | 130, −90, 360 | anneau ou arc : rayon, angle de départ, ouverture en degrés |
| `gap` | 56 | pas entre figurines en rang (`row`) |
| `pts` | — | positions explicites |
| `fill` | paper | intérieur des figurines |
| `tone` | aiTick | contour ; gris par défaut, la foule grand public |
| `sw` | 3 | épaisseur du contour |
| `link`, `linkColor`, `linkSw` | false, aiTick, 3 | traits fins tirés de l'origine (la tête de l'IA grand public) vers chaque figurine |

**Pistes :**
- `show` (0→n) : la figurine i apparaît pendant que `show` va de i à i+1. Une seule clé de 0 à n en d images donne un
  décalage régulier.
- `link` (0→1) : les traits se tirent depuis l'origine.
- `tone` : couleur du contour ; utiliser un hex pour un fondu.

`crowdPoints(p)` est exporté pour retrouver les positions côté TS. Le kit Python doit refaire le même calcul :
- en anneau, figurine i à l'angle `a0 + i × span/n` si `span` vaut 360, sinon `a0 + i × span/(n−1)` ;
- en rang, figurine i à x = `(i − (n−1)/2) × gap`.

## Ajouts aux types existants

### tick, `variant: 'ai'`

Une coche fine en pointillés dans un carré tireté. L'IA et le conseiller se distinguent alors par la forme, et pas
seulement par la couleur. La coche du conseiller (le défaut, trait plein) ne change pas.

**Paramètres :**
- `color`, `sw`, `size` : comme la coche par défaut.
- Le carré a pour côté `GEOM.TICK.aiBox × size` (1,3 × size) et un tireté de 2,5 à 3 px (`boxSw`, par défaut
  0,4 × `sw`).
- La coche intérieure fait 78 % de `size`. Ses points sont posés un à un, les trois sommets compris :
  - `thin` règle le diamètre des points (par défaut 0,7 × `sw`) ;
  - `dots` règle le pas entre deux points (par défaut 1,5 × `thin`).

**Piste `draw` (0→1) :** le carré se trace pendant [0 ; 0,5], puis la coche point par point pendant [0,45 ; 1].

**Exemple :** `S.add("coche_ia1", "tick", parent="fiche", color=AI_TICK, sw=8, size=40, variant="ai")`.

### marker, `labels`

Une légende sous chaque disque, par exemple `labels=["Limiter", "Exiger", "Relire"]`.
- L'étape active est en encre, les autres en gris (`ai_tick`). La couleur suit la piste `active` en fondu.
- `labelDy` (62) et `labelSize` (26) sont pris dans `GEOM.MARKER` par défaut.
- Avec 100 px entre les disques, des mots de plus de 7 lettres à 26 px se touchent : écarter les `xs` (≥ 150 px).

## geometry.json (GEOM)

| Clé | Contenu |
|---|---|
| `FIGURE` | `h` 191, `top` −96, `base` 95, `pivot` [0, 95], `bust` (chemin SVG), `head` {cy −64, r 32}, `sw` 5, `shoulder` [−30, −16], `hand` [−58, −6], `arm` {upper 84, fore 80, sw 13} (IK à 2 os du kit) |
| `PEN` | `len` 120, `r` 11 (demi-épaisseur), `tip` 26 |
| `STAMP_HANDLE` | `neck` 14, `neckW` 22, `knobW` 56, `knobH` 20 ; prise = [0, −(h/2 + neck + knobH/2)] |
| `TAG` | `r` 12, `fold` 10, `discR` 15, `iconX` 24, `textX` 46, `shadow` 3 |
| `DOC_DISC` | `r` 20, `inset` 32 |
| `BULLET` | `r` 22 |
| `TICK` | `size` 31, `pts` [[−15, 1], [−5, 11], [16, −12]], `aiBox` 1,3 |
| `MARKER` | `r` 20, `activeR` 32, `labelDy` 62, `labelSize` 26 |

Pour changer une valeur, la modifier dans geometry.json, puis lancer `python3 -m tests.story_parity` (chargement, clés,
`GEOM` identique côté Python) et `npx tsc --noEmit -p .` dans motion/.

**Attention :** une valeur de FIGURE, PEN, STAMP_HANDLE, TAG, DOC_DISC, TICK ou MARKER change le rendu de l'extrait V01
approuvé. Toute modification doit repasser la régression PSNR ≥ 45 dB.
