# Kit d'entités Story : paramètres et pistes

Source : `motion/src/story/entities_kit.tsx` (types génériques du kit) et `entities.tsx` (types de la série, nés avec
V01 : fiche, rangée, document, fil, bulle, tampon…). Registre : `COMPONENTS` dans `entities.tsx` (qui inclut `KIT`).
Géométrie partagée : `motion/src/story/geometry.json` (lue aussi par `pipeline/story.py`, `GEOM`).
Planche de contrôle (locale, non versionnée : `build/` est ignoré) : `build/kit_demo/kit_sheet.png`, images 0/20/40/60.
Chemins de code ci-dessous : relatifs à `wth-videos/`.

Lis d'abord les conventions, puis seulement le type dont tu as besoin. Avant d'inventer un type, cherche ici une
combinaison qui fait l'affaire : un type de plus est du code à maintenir en Python et en TypeScript.

## Sommaire

- Conventions communes
- Kit générique (`entities_kit.tsx`) : shape, text, icon, sector, gauge, counter, curve, seesaw, cursor, endcard, crowd
- Types de la série (`entities.tsx`) :
  - **Fiche.** fiche, line, tick, label, doc, case, sheen ;
  - **Liens et signes.** wire, qmark, bubble, bullet, burst, pill, window, marker, stamp ;
  - **Personnages et objets.** figure, limb, pen, png.
- Ajouts aux types existants : tick `variant: 'ai'`, marker `labels`
- geometry.json (GEOM)

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
- **Textes visibles et QA** : la QA (orthographe, glyphes, NFC) lit les paramètres `text`, `key`, `value`, `title`,
  `date`, `sealText`, `labels`, `prefix` et `suffix`, ainsi que les valeurs des pistes du même nom (bascule de texte
  d'une pilule ou d'un `text`). Un texte affiché par un autre paramètre échappe à la QA : utilise ces noms
  (`STORY_TEXT_KEYS` dans `pipeline/qa.py`).
- **Ordre de peinture** : `z` est global (pas relatif au parent) ; une piste `z` change de calque en cours de film
  (`S.set(id, z=…)` puis une clé instantanée). L'opacité se cumule avec celle des parents ; un parent à l'échelle 0
  cache ses enfants.

## Kit générique (`entities_kit.tsx`)

Formes de base, réutilisables d'un film à l'autre. Déclaration Python : `kit.<type>(…)` (kit.md § 5).

### shape

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

### text

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

### icon

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

### sector

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

### gauge

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

### counter

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

### curve

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

### seesaw

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

### cursor

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

### endcard

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

### crowd

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

## Types de la série (`entities.tsx`)

Ils sont nés avec l'extrait V01 et servent à toute la série : la fiche et ses rangées, les preuves (documents, fils,
dates), la question, le tampon, les personnages. Plusieurs sont pilotés par une classe du kit qui calcule leurs
paramètres : passe par elle plutôt que de les déclarer à la main.

| Type | Déclaré par | Rôle |
|---|---|---|
| `fiche` | `Sheet.add` | la page (brief, checklist) |
| `line` | `Sheet.add` / `Sheet.line_params` | une rangée de la fiche |
| `tick` | `kit.tick`, `Sheet.ticks` | coche humaine (pleine) ou de l'IA (`variant="ai"`) |
| `label` | à la main | puce-date → étiquette-source |
| `doc` | à la main | document du client (carte → compact → pastille) |
| `case` | à la main | case-source en tirets |
| `sheen` | à la main | reflet qui balaie la page (« fluide ») |
| `wire` | à la main | fil de preuve (plein) ou faisceau de l'IA (pointillés) |
| `qmark` | à la main | grand « ? » |
| `bubble` | à la main | bulle du conseiller ↔ autocollant « ? » |
| `bullet` | à la main | pastille d'information isolée |
| `burst` | à la main | éclat (l'IA « produit ») |
| `pill` | à la main | pilule de texte (« Client · 9 h », « IA ») |
| `window` | à la main | outil validé par le cabinet (fenêtre scellée) |
| `marker` | `kit.steps_marker` | repère d'étapes 1-2-3 |
| `stamp` | à la main + `Figure.stamp` | tampon (« PRÊT POUR LE RDV ») |
| `figure`, `limb`, `pen` | `Figure` | personnage, son bras, son stylo |
| `png` | `S.png` + à la main | illustration en verre, alpha strict |

### fiche

La page : carte papier avec un titre d'en-tête à droite, un filet et des onglets cyan vides.

| Paramètre | Rôle |
|---|---|
| `w`, `h` | taille (V01 : 500 × 720) |
| `title` | titre de l'en-tête (ExtraBold 36, aligné à droite), ex. « Brief » |
| `headerH` | hauteur de l'en-tête (84) |
| `tabs`, `tabX` | y des onglets vides (un par rangée) et leur x |
| `sheen` | référence au reflet (voir sheen) |

**Pistes :** `tab0`, `tab1`… (opacité de l'onglet i : il disparaît quand la puce de sa rangée arrive). Ombre dure 8 px.

### line

Une rangée de la fiche : puce (pictogramme sur disque cyan, ou cercle tireté vide avec `icon="none"`), clé à gauche,
valeur à droite. Toute la géométrie vient de `Sheet.line_params(key, value, icon)` : valeur mesurée, fente entre la clé
et la valeur, épaisseur du trait.

| Paramètre | Rôle |
|---|---|
| `key`, `value`, `icon` | textes (32 px) et pictogramme de la puce |
| `x0`, `x1`, `h`, `hStrip`, `ty` | capsule de fond, bande de texte, ligne de base |
| `bulletX`, `textX`, `valueX`, `valueW` | colonnes ; `valueX` est le bord droit de la valeur |
| `crackX`, `tilt`, `drop`, `gap` | cassure : x de la fente, inclinaison (°), chute (px) et largeur de la fente (12) |
| `fallPx` (240), `strikeW` (7) | chute de la valeur barrée, épaisseur du trait qui barre |

**Pistes.**
- **Écriture et forme.**
  - `chars` : machine à écrire, clé puis valeur (`kit.type`).
  - `grow` (0 → 1) : la bande de texte devient une rangée pleine.
  - `slotFill` : opacité de la capsule beige.
- **Puce.**
  - `bulletOn` (0 : pas encore de puce).
  - `flash` : la puce grossit de 35 % ; le faisceau de l'IA l'atteint.
  - `pulse` : la puce bat × 1,6 ; « rien ne tient cette ligne ».
  - `alarm` : le contour de la puce vide passe au rouge.
- **Ligne fausse.**
  - `red` : texte et contour de la capsule au rouge.
  - `crack` (0 → 1) : la rangée se FEND entre clé et valeur, la moitié droite pivote de `tilt` et descend de `drop`.
    `pipeline.story.line_crack_point` donne la position d'un point de cette moitié.
- **Correction.**
  - `strike` (0 → 1) : un trait encre barre la valeur, de droite à gauche (`Figure.strike(..., line=id)`).
  - `fall` (0 → 1) : la valeur barrée se détache et tombe de la fiche, en s'effaçant à la fin.
  - `dimValue` : valeur barrée à 60 % d'encre. À éviter : un gris à 50 % se lit « rejeté ».

### tick

Coche dessinée d'un trait. Le défaut est la coche du conseiller (trait plein) ; `variant: 'ai'` donne celle de l'IA
(voir « Ajouts aux types existants »).

| Paramètre | Rôle |
|---|---|
| `color`, `sw` | couleur (deep pour l'humain, ai_tick pour l'IA) et trait (8) |
| `size` | largeur (défaut `GEOM.TICK.size`, 31 ; V01 : 40) ; le trait reste `sw` px |
| `dots` | pointillé du trait (ancienne coche de l'IA) |

**Piste :** `draw` (0 → 1), tracé. La coche chassée par le stylo : `kit.drop(id, f, out=True, h=52, dx=18, rot=35)`.

### label

La puce-date (calendrier + date) qui devient l'étiquette-source (pictogramme du document + date, coin plié). C'est le
même dessin que la version compacte d'un `doc` : un document peut se réduire DANS son étiquette sans fondu.

**Paramètres :** `icon` (pictogramme du document), `tag` = `{w, h, date, size}`.

**Pistes :**
- `tagged` (≥ 0,5 : aspect étiquette, sinon puce-date) ;
- `pop` (échelle 0,4 + 0,6 × pop tant que c'est une puce-date) ;
- `lit` (0 → 1 : papier → cyan pâle, contour encre → deep) ;
- `flash` (l'étiquette grossit de 35 %).

Écris la date en clair, ex. « sept. 2025 » : « 09/2025 » ou « 03/2026 » se lisent comme des échéances.

### doc

Un document du client. Il passe de la carte complète (160 × 200 : pastille, titre, deux lignes grises) à la carte
compacte (`cw` × `ch` : bande de date à gauche, pastille à droite), puis se réduit en sa pastille qui se pose sur
l'étiquette.

**Paramètres :** `title`, `icon`, `date`, `cw`, `ch`, `titleSize`, `tag` (`{w, h, date, size}`, comme label).

**Pistes :**
- `compact` (0 → 1) ;
- `tag` (0 → 1 : la carte se réduit en sa pastille) ;
- `txt` (opacité du contenu de la carte complète) ;
- `sh` (ombre en px).

### case

Case-source en tirets deep (14/10), tracée par le stylo du conseiller.

**Paramètres :** `w`, `h`. **Piste :** `draw` (0 → 1). Une case qui reste vide est la preuve qu'il n'y a pas de source.

### sheen

Reflet blanc qui balaie la page en diagonale : la réponse « fluide ».

**Paramètres :** `w`, `h`, `under`.

**Piste :** `p` (0 → 1 : le balayage ; invisible à 0 et à 1).

**`under=True`.** L'entité ne fait que porter la progression : la page, les rangées et la pilule qui ont un paramètre
`sheen = {id, dx, dy, w, h, color?, opacity?}` dessinent la bande SOUS leurs textes. C'est ainsi que V01 garde le texte
net pendant le reflet.

### wire

Un lien entre deux ancres : fil de preuve (trait plein) ou faisceau de l'IA (pointillés `dots`).

| Paramètre | Rôle |
|---|---|
| `a`, `b` | ancres `{id, at}` : point local d'une entité, suivi dans toutes ses transformations ; sans ancre, pistes `pa` / `pb` (points monde) |
| `color`, `sw` | couleur et épaisseur |
| `dash`, `dashAlt` | motif du trait, et motif « cassé » (piste `dashed`) |
| `dots`, `endDot` | points ronds aux extrémités (faisceau de l'IA) ; `endDot: false` pour ne garder que le départ |
| `tension` | courbure de la cubique (0,45) |

**Pistes.**
- **Tracé.**
  - `draw` (0 → 1) : tracé depuis a.
  - `from` (0 → 1) : le départ se retire, le fil « rentre » vers b.
- **Ancres.**
  - `aAt`, `bAt` : l'ancre glisse dans son entité, par exemple de la valeur à la date.
  - `pa`, `pb` : extrémités libres, sans ancre.
- **Forme.**
  - `via` : point monde de passage, ou `[]` pour aucun.
  - `sag` : affaissement en px.
  - `color` : couleur.
  - `dashed` (≥ 0,5) : le fil plein se casse en tirets ; c'est la preuve qui ne trouve rien.

Points de la courbe en Python : `S.wire_cubic(id, n)` puis `point_at_length` ; `S.along_wire` pour faire glisser un
objet le long du fil (sans tenir compte de `via`). Un fil de preuve part du texte qu'il prouve, pas d'un espace vide
entre deux rangées.

### qmark

Grand « ? » encre (ExtraBold). **Piste :** `gs` (corps, 100). Il naît de la valeur qu'il remplace :
`kit.pop("question", f, from_pt=<point de la valeur>)`.

### bubble

La bulle du conseiller (« ? » + mini-figurine du client), qui devient l'autocollant « ? » posé sur la fiche.

**Paramètres :**
- `big` et `small` : deux formes `{w, h, r, q, qx, px, ps, sw, shadow, gs}` (taille, rayon, corps et x du « ? », x et
  hauteur de la mini-figurine, trait, ombre) ;
- `tail` : pointe de la queue, sur la tête du conseiller ;
- `tailBase` : `[x0, x1]` de la base de la queue.

**Pistes :**
- `s` (0 bulle → 1 autocollant : plus petit, cyan, queue rentrée) ;
- `q` (« ? » affiché si ≥ 0,5) ;
- `glyph` (mini-figurine affichée si ≥ 0,5) ;
- `pulse` (+25 %).

Un autocollant se pose hors de la zone du tampon. Écris « à poser au RDV » à côté s'il reste ouvert à la décision.

### bullet

Pastille d'information isolée, même dessin que la puce d'une rangée. `icon="none"` donne le cercle tireté VIDE de
l'information sans source.

**Paramètres :** `icon`, `r` (22). **Piste :** `alarm` (contour du cercle vide vers le rouge).

### burst

Rayons courts qui jaillissent d'un point : le cerveau de l'IA « produit » quelque chose.

**Paramètres :** `r0`, `r1` (rayons de départ et d'arrivée), `n` (8), `sw` (6), `color` (deep), `a0` (angle du
premier rayon). **Piste :** `p` (0 → 1 ; invisible à 0 et à 1).

### pill

Pilule de texte : étiquette d'un personnage (« IA »), pastille du fil conducteur (« Client · 9 h »).

| Paramètre | Rôle |
|---|---|
| `text`, `size` (28), `weight` (700), `color` | texte |
| `w`, `h` (56) | taille : `w` = `text_width(text, size, weight)` + 48 environ |
| `fill` (cyan), `stroke`, `sw` (4), `shadow` (6) | pilule |
| `icon`, `iconColor` | pictogramme à gauche du texte |
| `sheen` | reflet sous le texte |

**Pistes :** `w`, `fill`, `text` (bascule de texte, contrôlée par la QA).

### window

L'outil validé par le cabinet : fenêtre avec une barre de titre, un cadenas et un sceau qui s'ouvre en « ✓ Cabinet ».
Elle peut se réduire en badge (pistes `w`, `h`, puis `scale`).

**Paramètres :** `titleH` (56), `r` (24), `sealW` (largeur du sceau ouvert), `sealText`.

**Pistes :**
- `w` (820), `h` (640) ;
- `seal` (0 → 1 : le disque cyan au pictogramme du cabinet s'ouvre en pilule) ;
- `lock` (1 fermé, 0 ouvert).

### marker

Repère d'étapes 1-2-3 : une ligne, des disques numérotés, et le disque actif cyan qui glisse.

**Paramètres :** `xs` (x des disques), `y`, `labels` (légende, voir « Ajouts »), `labelDy`, `labelSize`.

**Piste :** `active` (0 = « 1 », valeurs décimales pendant le glissement).

Déclare-le avec `kit.steps_marker` : il le pose en repère local centré, donc il peut se réduire vers son centre. Un
marker aux `xs` absolus (V01) se réduirait vers le coin haut gauche de l'écran.

### stamp

Le tampon : texte deep espacé dans un double cadre arrondi, sans fond (la page se voit à travers).

**Paramètres :** `text`, `w`, `h`, `size` (40).

**Piste :** `handle` (0 → 1 : poignée encre au-dessus, tenue par la main pendant le coup).

Le coup se joue par `Figure.stamp(f, id, shake=…)`. Ne tamponne pas VALIDÉ si une question reste ouverte : préfère
« PRÊT POUR LE RDV ».

### figure, limb, pen

Le personnage (`figure`), son bras (`limb`) et son stylo (`pen`). Déclare-les et anime-les UNIQUEMENT par
`Figure(kit, id, pos, variant=…)` (voir kit.md § 7) : le rig calcule le coude image par image avec des longueurs fixes.

**figure.**
- Paramètre `variant` : `ink` pour « toi », le conseiller, le seul à tenir un outil ; `paper` pour le client ou un
  tiers.
- Piste `lean` : inclinaison en degrés autour du pied (`GEOM.FIGURE.pivot`).
- Hauteur 191 px à l'échelle 1, de −96 (haut de la tête) à +95 (pied).

**limb.**
- Paramètres :
  - `a` : ancre de l'épaule sur la figurine ;
  - `b` : ancre de la prise du stylo ;
  - `sw` ;
  - `pivot`, `pivotTrack` (« lean ») : l'épaule suit l'inclinaison de la figurine.
- Pistes : `bend` (0 droit → 1 par le coude) et `elbow` (point monde).

**pen.** Paramètre `len` (`GEOM.PEN.len`, 120). Son origine est la prise ; la pointe est à (len, 0) et suit `rot`.

Le client sans outil : `Figure(kit, "client", pos, variant="paper", tool=False)`.

### png

Illustration en verre, dessinée en HTML (pas en SVG), après `S.png(name)` qui en fait un alpha strict pour l'ivoire.

| Paramètre | Rôle |
|---|---|
| `src` | `meta["src"]` renvoyé par `S.png` |
| `w`, `h` | taille d'affichage (garder le rapport `meta["w"] / meta["h"]`) |
| `shadow`, `blur`, `dy` | ombre portée douce autour de la silhouette (0,16, 24 px, 16 px) |
| `contact` | `{w, h, dy, blur, alpha}` : ombre de contact SOUS l'objet seulement, au lieu du halo autour de la silhouette ; à préférer sur l'ivoire |
| `saturate` | < 1 pour calmer des couleurs qui concurrencent le cyan (V01 : 0,85 pour l'IA) |

Pistes : seulement les pistes communes. Un PNG ne se déforme pas et ne raconte pas un processus à lui seul : ce qui doit
bouger se dessine en entités.

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
approuvé. Toute modification doit repasser la régression avant / après (PSNR ≥ 45 dB par image ; commandes : SKILL.md,
« Ajouter une entité », point 7).
