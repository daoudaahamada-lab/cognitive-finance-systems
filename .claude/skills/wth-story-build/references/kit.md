# Kit de mise en scène Story : macros, figurine articulée, fiche, fin standard

Source : `wth-videos/pipeline/story_kit.py`. Entités dessinées : `entities.md` (même dossier : paramètres et pistes
de chaque type). Chemins de code ci-dessous : relatifs à `wth-videos/`.
Démonstration : `scripts/story/_demo_kit.py` (6,7 s sur la voix de V01, S18 à S20 ; ce n'est pas une vidéo de la série).
Tests : `python3 -m tests.story_smoke` (cas « kit : clés de pop, move, morph » et « figurine : bras de longueur fixe image
par image »).

Le kit n'ajoute rien au rendu. Chaque macro pose des clés avec l'API Story (`S.key`, `S.keys`, `S.path`, `S.fly`) et lit
l'état avec `S.val`, `S.to_world` et `S.world_scale`. Les props produites sont donc de simples props Story, et
`tests.story_parity` couvre toujours la parité Python / TypeScript.

```python
from pipeline.story_kit import Figure, Kit, Sheet

def build(S):
    kit = Kit(S)
    f = kit.at("S05", "limites", "la loupe apparaît sur le dossier")
    kit.pop("loupe", f)
```

## Sommaire

1. Conventions : images, valeurs de retour, repères, valeurs initiales
2. Durées de la référence et constantes du kit
3. Temps : `at`, `hold`, `pin`
4. Macros de mouvement : `pop`, `vanish`, `morph`, `move`, `draw`, `fade`, `pulse`, `shake`, `drop`, `type`, `stagger`
5. Déclarations : une fonction par entité du kit (`shape`, `text`, `icon`, `gauge`, `counter`, `tick`…)
6. Éléments de la série : `steps_marker`, `step`, `outro`
7. Figurine articulée : `Figure` (principe, `place_for`, méthodes, `stamp`)
8. Fiche : `Sheet`
9. Fonctions utilitaires (module)
10. Démonstration et rendu
11. Pièges

## 1. Conventions

- **Images.** Les images sont celles du film : image n = n / 30 s. `kit.at` donne l'image du début du mot.
  - Une clé posée à l'image f montre déjà le premier pas sur f (LEAD = 1). Un événement calé sur un mot est donc
    visible sur l'image même du mot.
- **Valeur de retour.** Une macro renvoie l'image qui suit son mouvement (f + d), qui sert à enchaîner l'étape suivante.
  - Exceptions : `type` renvoie l'image qui suit le dernier caractère, `Figure.tap` et `Figure.stamp` l'image du
    contact, et `Figure.trace` la liste des images de passage.
- **Repères.**
  - Un argument `to` ou `pos` est exprimé dans le repère du parent de l'entité (le monde si elle n'en a pas).
  - Un argument `*_pt`, `into` ou `target` est un point monde (1080 × 1920). `into` et `from_pt` acceptent aussi un id
    d'entité, qui désigne son origine.
- **Valeur initiale.** `S.key` exige une valeur initiale pour toute piste qui n'est pas pos, scale, rot, opacity, sx ou
  sy.
  - Les macros la posent quand elle manque (`kit.ensure` : 0, ou 1 pour `handle`).
  - Les déclarations du § 5 posent celles de leur type.
  - Une piste de couleur qui doit passer en fondu reste à poser avec un hex, par exemple
    `S.set("jauge", fill=STYLE["cyan"])`.
- **État de départ.** Un élément qui apparaît plus tard se déclare avec `scale=0`.
  - Avec `scale=1`, il serait visible dès l'image 0 du film.
  - `pop` pose de toute façon l'échelle 0 à f − 1.
- **Avertissements.** Ils sont imprimés (« attention (kit) : … ») et gardés dans `kit.warnings`. Une mise en scène
  terminée n'en a aucun.

## 2. Durées (pipeline/story.py, mesurées sur la référence)

| Constante | Images | Emploi |
|---|---|---|
| `POP` | 9 (300 ms) | apparition, ease-out cubique, sans rebond |
| `SCALE` | 10 | changement d'échelle |
| `MORPH` | 11 (350 ms) | passage d'une composition à l'autre |
| `MOVE` | 16 (550 ms) | déplacement, ease-in-out ; seul profil symétrique de la référence |
| `DROP` | 11 (370 ms) | chute, ease-out, sans rebond |
| `TILT` | 14 | inclinaison |
| `FADE` | 6 (200 ms) | fondu, réservé au texte et à l'interface |
| `DRAW` | 9 | trait ou fil tracé |

Constantes du kit :

| Constante | Valeur | Rôle |
|---|---|---|
| `WRITE_RATE` | 3,5 | caractères par image (V01) |
| `TRACE_SPEED` | 20 | px par image : vitesse de la pointe qui relit |
| `WALK_SPEED` | 7 | px par image |
| `HOP`, `HOP_PERIOD`, `WALK_LEAN` | 5, 8, 4 | sauts de la marche (px, images) et penché (°) |
| `REACH` | 0,94 | au-delà de cette part de l'allonge, la figurine fait un pas |
| `REACH_STAMP` | 0,98 | idem pour le tampon (main seule) |
| `WRIST` | 0,35 | prise minimale, en part de (bras + avant-bras), quand la cible est trop près |
| `REST_UP` | 255° | angle du stylo levé au repos |
| `TAP` | 8 | images d'un tapotement |
| `STEP` | 8 | images du pas fait avant un coup de tampon |

## 3. Temps

### `kit.at(scene, mot, what="")` → image
Temps fort du storyboard. C'est `S.beat` :
- le mot est vérifié à ±30 ms ;
- l'appel est compté dans la couverture du storyboard (`storyboard_beats_missing`, film entier refusé s'il en manque) ;
- `what` (ce qui se passe) va dans `meta.beats`.

```python
f = kit.at("S12", "Exige", "l'IA sort par la gauche ; le conseiller apparaît")
```

### `kit.hold(scene, mot, what="tenue : rien ne bouge")` → image
Temps fort de tenue : il est posé pour la couverture du storyboard, sans événement. Ne rien faire commencer sur cette
image : une tenue n'a pas d'image clé forcée.

### `kit.pin(f, states, tol=0.5)` → f
Impose l'état `states = {id: {piste: valeur}}` à l'image f, par une clé instantanée.
- **Rôle.** Ouvre chaque partie d'un paquet `scripts/story/Vxx/pN.py` avec l'`etat_initial` de sa scène. Les parties
  écrites en parallèle ne dépendent ainsi plus de la fin exacte de la précédente.
- **Saut détecté.** Si la valeur à f − 1 (fin de la partie précédente) s'écarte de plus de `tol`, un avertissement
  « (saut) » est émis : le saut se verrait. Pour une chaîne, il faut l'égalité stricte.
- **Piste absente.** Une piste qui n'existe pas encore (hors pos, scale, rot, opacity) reçoit la valeur comme valeur
  initiale.
- **Image de l'épingle.** Épingle à l'image qui PRÉCÈDE le premier événement de la partie (f0 − 1, f0 étant le
  début de sa première scène). Une clé posée sur f part de la valeur de f − 1 : un mouvement qui commence sur f0
  ignorerait une épingle posée sur f0 même.
- **Figurines.** N'épingle jamais une figurine, son bras ou son stylo : le bras se décrocherait. Place-la par
  `walk` / `enter`.
- **Partie isolée.** Avec `WTH_PARTS=pN` (une partie construite seule), les « (saut) » sont normaux : la partie
  précédente n'a pas tourné. Seuls comptent ceux du film entier.
- **Figurine en partie isolée.** Une figurine déclarée `show=False` et entrée dans une partie précédente reste
  invisible : son allonge vaut 0 et le rig s'arrête. Garde-fou en tête de partie, sans effet dans le film entier :
  `if S.val("toi", "scale", f0 - 1) == 0: toi.enter(f0 - 10, at=[x, y])`.

```python
sc = next(s for s in S.sb["scenes"] if s["id"] == "S05")
f0 = round(sc["t_start"] * S.fps)
kit.pin(f0 - 1, {"fiche": {"pos": [540, 760], "scale": 1}, "marqueur": {"active": 0}})
f = kit.at("S05", "Première")
```

## 4. Macros de mouvement

### `kit.pop(id, f, scale=None, from_pt=None, to=None, d=POP, e="out")` → f + d
Apparition, l'échelle passant de 0 à `scale`. Par défaut, `scale` vaut l'échelle actuelle si elle est > 0, sinon 1.

Clés posées :
- `scale` : 0 à f − 1 (seulement si elle n'y vaut pas déjà 0), puis `{f, scale, d, e}` ;
- `opacity` : 1 à f, si elle valait moins de 1 ;
- `pos` : si `from_pt` est donné (point monde ou id), l'élément est posé en `from_pt` à f − 1 puis glisse vers `to`
  (repère du parent) ou vers sa position actuelle pendant qu'il grandit. Avec `to` seul, il glisse depuis sa position.

```python
kit.pop("question", f, from_pt=valeur_monde)   # le « ? » naît de la valeur
```

### `kit.vanish(id, f, into=None, d=POP, e="out")` → f + d
Disparition : l'élément se réduit vers son centre, ou glisse vers `into` (point monde ou id, position prise à f + d).

Clés posées : `scale` vers 0 en d, `pos` vers `into` en d, `opacity` à 0 à f + d.

### `kit.morph(outs, ins, f, d=MORPH, pair=None, e="out")` → f + d
Passage d'une composition à l'autre, dans les mêmes images : les sortants (`vanish`) se réduisent pendant que les
entrants (`pop`) grandissent. La scène n'est jamais vide.

- `outs` et `ins` : un id ou une liste ; `[]` est admis (rien n'entre, ou rien ne sort).
- `pair` : par défaut vrai quand il y a autant de sortants que d'entrants. Alors l'entrant i naît à la place du sortant
  i (sa position à f − 1), et le sortant i se réduit vers la place de l'entrant i : c'est un relais.

Clés posées :
- sortants : `scale` vers 0 en d, `opacity` à 0 à f + d, et `pos` vers l'entrant apparié ;
- entrants : `scale` 0 à f − 1 puis vers 1 (ou leur échelle) en d, et `pos` depuis le sortant apparié.

```python
kit.morph(["dossier", "loupe"], ["outil", "badge"], f)        # relais deux à deux
kit.morph(["jauge", "compteur", "horloge"], [], f)             # sortie groupée
```

### `kit.move(id, f, to, d=MOVE, e="inOut", arc=None, scale=None, world=False)` → f + d
Déplacement vers `to`, dans le repère du parent.
- Clés posées : `pos` (`{f, to, d, e, arc}`) et `scale` si elle est donnée.
- `arc` : le trajet bombe vers le haut de `arc` px à mi-course.
- `world=True` : `to` est un point monde. C'est `S.fly` : clés image par image, et le trajet monde reste exact même si
  le parent bouge.

### `kit.draw(id, f, d=DRAW, track="draw", e="out", to=1)` → f + d
Trace un trait : la piste `track` passe de 0 à `to`. S'applique au contour d'une shape, à un fil, une coche, une courbe,
l'anneau d'une icon (`track="ring"`), le surligneur d'un text (`track="mark"`) ou son soulignement (`track="under"`).

### `kit.fade(id, f, to=1, d=FADE, frm=None, e="out")` → f + d
Fondu d'opacité vers `to`. `frm` pose une valeur à f − 1. À réserver au texte et à l'interface : une forme entre par
`pop`, pas par un fondu.

### `kit.pulse(id, f, times=1, peak=None, step=3, track="scale")` → f + 2·times·step
Battement : la piste monte à `peak` en `step` images (ease-out), puis revient en `step` images (ease-in-out), `times`
fois.
- `peak` par défaut : 1,15 × l'échelle actuelle pour `scale`, 1 pour une autre piste (le `pulse` d'une ligne ou d'une
  bulle).
- V01 « fausse » (la puce de L5 bat deux fois) : `kit.pulse("L5", f, times=2, step=2, track="pulse")`.

### `kit.shake(id, f, amp=6, axis="x")` → f + 3
Secousse de 3 images, en clés instantanées autour de la position à f − 1 :
- `x` : +amp, −0,8 amp, 0 (la case vide qui refuse) ;
- `y` : le même mouvement à la verticale ;
- `xy` : (+amp, −0,75 amp), (−0,75 amp, +0,5 amp), 0 (la page sous le tampon, avec amp = 4).

### `kit.drop(id, f, h=None, d=DROP, out=False, dx=0, rot=0, to=None)` → f + d
Chute en ease-out, sans rebond.
- **Entrée (défaut).** L'élément tombe de `h` px (240 par défaut) au-dessus de sa place (`to`, ou sa position) et
  arrive en d images. Il est rendu visible à f : échelle 1 si elle valait 0, opacité 1.
- **`out=True`.** L'élément tombe de sa place de `h` px (60 par défaut), décalé de `dx`, tourne de `rot`°, puis
  s'efface en 6 images à partir de f + d/2.
- La coche de l'IA chassée par le stylo (V01) : `kit.drop("coche_ia1", g, out=True, h=52, dx=18, rot=35)`.

### `kit.type(id, f, n=None, rate=WRITE_RATE, flash=False)` → ceil(f + n / rate)
Machine à écrire : la piste `chars` passe de 0 à `n`, en linéaire.
- `n` par défaut :
  - pour une ligne de fiche (entité `line`) : longueur de la clé + longueur de la valeur ;
  - pour un `text` : longueur du texte, sans les sauts de ligne.
- `flash=True` : la puce de la ligne bat au départ (`flash` 1 puis 0).
- La référence tape 1 caractère par image (`rate=1`) ; V01 écrit à 3,5.
- La valeur renvoyée est la première image où tout est écrit : y caler la coche.

```python
fin = kit.type("fiche_L1", f, rate=2, flash=True)
kit.draw("coche1", fin, 6)
```

### `kit.stagger(ids, f, step, fn, *args, **kw)` → liste des retours
Appelle `fn(id, f + i·step, *args, **kw)` pour chaque id, avec un décalage régulier.

```python
kit.stagger(rows, f, 6, kit.type, rate=2, flash=True)   # lignes écrites une à une
kit.stagger(["a", "b", "c"], f, 2, kit.pop)             # pops décalés de 2 images
```

## 5. Déclarations (une fonction par entité du kit)

Chaque fonction est `S.add` plus `S.set` des pistes de départ, et renvoie l'id.
- Signature commune : `id, pos, …, z, parent=None, scale=1, opacity=1`.
- Les paramètres en plus (`**p`) passent tels quels à l'entité : voir entities.md.
- Les paramètres valant `None` sont omis.

| Fonction | Pistes posées | Notes |
|---|---|---|
| `kit.shape(id, pos, kind="round", w=200, h=None, …, rot=None, draw=None)` | pos, scale, opacity (rot) ; `draw` si donné | `draw=0` : contour à tracer avec `kit.draw` |
| `kit.text(id, pos, text, size=40, weight=700, …, typed=False)` | `chars=0` si typed | `w` mesuré par `text_width` (plus longue ligne) : il sert à `mark` et `under` |
| `kit.icon(id, pos, name, …)` | — | `disc=` rayon pour un pictogramme sur disque ; piste `ring` via `kit.draw(id, f, track="ring")` |
| `kit.sector(id, pos, start=0, value=0, …)` | start, value | `S.key(id, "value", f, 10, d, "linear")` |
| `kit.gauge(id, pos, value=1, w=600, h=48, …)` | value | couleur en fondu : `S.set(id, fill=STYLE["cyan"])`, puis une clé vers `STYLE["red"]` |
| `kit.counter(id, pos, value=0, size=96, …)` | value | `suffix=" min"` ou `" €"` : l'espace devient insécable ; `color` à poser en hex pour un fondu |
| `kit.curve(id, pos, pts, draw=0, …)` | draw | tracée avec `kit.draw(id, f, 20)` |
| `kit.seesaw(id, pos, rot=0, …)` | rot | bascule : `S.key(id, "rot", f, 8, TILT, "out")` |
| `kit.seat(seesaw_id, x, obj_h)` | — | position locale d'un objet posé sur la planche (enfant de la bascule) |
| `kit.cursor(id, pos, z=30, …)` | press, ring | `kit.click(id, f)` |
| `kit.click(id, f)` → f + 7 | press (3 images, puis 4 pour remonter), ring (0 à f − 1, puis 1 en 18 images) | le clic du pointeur |
| `kit.endcard(id, pos, title=None, text=None, labels=None, z=40, …, btn=1)` | btn, press, title | voir `kit.outro` |
| `kit.crowd(id, pos, n=6, show=None, link=None, …)` | show, link si donnés | `show` 0 → n en d images : apparitions décalées |
| `kit.tick(id, pos, color, size=None, sw=8, variant=None, z=11, parent=None, draw=0)` | draw | `variant="ai"` : pointillés dans un carré tireté ; `size` par défaut `GEOM.TICK.size` |

```python
kit.gauge("temps", [560, 410], value=1, w=480, h=40, segments=6)
S.set("temps", fill=STYLE["cyan"])
S.key("temps", "value", f, 0.15, g - f, "linear")      # la jauge se vide
S.key("temps", "fill", g, STYLE["red"], 6, "out")     # puis passe au rouge
kit.counter("minutes", [560, 500], value=0, size=56, suffix=" min")
S.key("minutes", "value", f, 45, g - f, "inOut")
```

## 6. Éléments de la série

### `kit.steps_marker(labels=None, n=None, id="marqueur", y=300, cx=540, gap=None, active=0, z=20)` → id
Repère d'étapes 1-2-3, avec sa légende sous les disques (marker).
- **Écart.** Avec une légende, `gap` vaut au moins 150 px, mesuré sur le libellé le plus long (+ 28 px). Sans légende,
  il vaut 100 px.
- **Repère.** Les disques sont en repère local centré, et l'entité est posée en `[cx, y]`. Elle peut donc se réduire
  vers son centre (`vanish`, `morph`).
- Le repère de V01 (`xs` absolus) n'est pas touché.
- Fonction de module équivalente : `steps_marker(S, labels, **kw)`.

### `kit.step(f, k, id="marqueur", d=MOVE)` → f + d
Le disque actif glisse sur l'étape k (0 = « 1 ») en 550 ms. La légende passe du gris à l'encre en fondu.

```python
kit.steps_marker(["Limiter", "Exiger", "Relire"])
kit.step(kit.at("S12", "Exige"), 1)
```

### `kit.outro(scene, mot=None, outs=(), press=16, title="WealthTech Horizon", labels=("Comprendre ton argent",), text="S’abonner", icon=None, pos=(540, 760), w=620, h=520, id="fin", z=40)` → dict
Fin standard des 15 films (d'après la fin de la référence).

Déroulé, à partir de f = le temps fort (`scene`, `mot` ; par défaut le premier temps fort de la scène) :
1. À f, les `outs` se réduisent pendant que la carte de fin grandit (morph de 350 ms).
2. Le titre et les lignes entrent en fondu à f + 4.
3. Le bouton surgit (pop) à f + 6.
4. Le pointeur `id_curseur` apparaît en bas à droite, puis glisse vers le bas droit du bouton, jamais sur le libellé.
5. Il clique (`kit.click`) : le bouton s'enfonce de 8 px dans son ombre (piste `press` de la carte, 5 images), puis
   remonte.
6. Ensuite, plus rien ne bouge jusqu'à la dernière image.

Paramètres :
- `press` : un entier, le clic tombant alors `press` images après f (16, comme la fin du montage classique) ; ou un mot
  de la scène, le clic tombant alors sur ce temps fort, par exemple `"comprendre"`.
- `outs` : tout ce qui est encore à l'écran. Une figurine sort par `Figure.exit(out["card"])`, pas par `outs`.

Retour : `{"card": f, "press": image du clic, "id": id, "cursor": id du pointeur}`.

Autres points :
- La QA dispense la dernière scène du contrôle d'image figée : la carte peut rester immobile jusqu'à la fin.
- Fonction de module équivalente : `outro(S, scene, **kw)`.

```python
out = kit.outro("S20", outs=["fiche", "marqueur"], press="comprendre")
toi.exit(out["card"])
kit.hold("S20", "argent.", "tenue : la carte de fin reste immobile")
```

## 7. Figurine articulée : `Figure`

`Figure(kit, id, pos, scale=1.0, variant="ink", side="left", tool=True, z=15, show=True)` déclare trois entités :
- `id`, la figurine (`variant="ink"` : « toi », `variant="paper"` : le client) ;
- `id_bras`, le bras (limb, avec `pivotTrack="lean"`) ;
- `id_stylo`, le stylo (pen).

Options :
- `tool=False` : la figurine seule, sans bras ni stylo (le client). Elle sait entrer, sortir et marcher.
- `show=False` : figurine déclarée à l'échelle 0, à faire entrer avec `enter`.
- `pos` : le centre de la figurine. Le haut de la tête est à −96 × échelle et le pied à +95 × échelle : pour poser le
  pied sur une ligne de sol y_sol, prendre pos = [x, y_sol − 95 × échelle].

### Principe
- **Bras.** C'est une chaîne à 2 os de longueurs FIXES (`GEOM.FIGURE.arm` : bras 84, avant-bras 80, × l'échelle de la
  figurine), résolue par `solve_ik`. Le coude (piste `elbow` du limb, `bend` = 1) et la prise du stylo sont posés image
  par image : le bras ne s'étire plus.
- **Épaule.** Elle est calculée comme le rendu (entities.tsx Limb) : `GEOM.FIGURE.shoulder`, penchée de `lean` autour
  du pied (`pivot`), puis passée en monde.
- **Côté (`side`).**
  - `"left"` (V01) : bras du côté gauche de l'écran, la figurine se tourne vers la gauche, coude vers le bas.
  - `"right"` : miroir (épaule en +30, stylo au repos à 285°).
- **Stylo.** Il prolonge la droite épaule → pointe, comme V01 (« bras et stylo dans le prolongement »). Quand la cible
  est à moins de stylo + 0,35 × (bras + avant-bras) de l'épaule (177 px à l'échelle 1), le poignet plie : la prise
  reste à 57 px de l'épaule, du côté bas.
- **Allonge, à l'échelle 1.**

  | Mesure | Valeur | Ce qui se passe au-delà ou en deçà |
  |---|---|---|
  | maximum | 284 px (164 de bras + 120 de stylo) | — |
  | confortable | 267 px (`REACH`) | au-delà, la figurine fait un pas |
  | minimum | 63 px | en deçà : arrêt, « éloigne la figurine » |
  | main seule (tampon) | 161 px | — |

- **Hauteur.** Une cible plus haute (ou plus basse) que l'épaule de plus de 267 px est hors d'atteinte : arrêt.
  Rapprocher la figurine en hauteur ou l'agrandir.
- **Repos.** La main est sur `GEOM.FIGURE.hand`, stylo levé à 255° : la pose de V01, avec le coude caché dans le buste
  encre.
- **Règle.** La figurine, son bras et son stylo ne bougent QUE par ces méthodes. Une clé posée à la main sur la
  figurine décroche le bras, puisque le coude est une piste monde.
  - Deux méthodes qui se recouvrent : la dernière appelée gagne sur les images communes.

### Placement : `fig.place_for(targets, n, pen=True, margin=REACH)` → [x, y]
Donne la position du corps (même y), la plus proche de la position actuelle, d'où tous les `targets` (points monde)
sont à portée confortable. Arrêt si c'est impossible (« cibles trop écartées », ou hors d'atteinte en hauteur).

Modèle d'écriture : faire marcher la figurine UNE fois vers l'emplacement de toute la séquence. Les pas automatiques ne
sont qu'un filet de sécurité, et un pas trop rapide (plus de 10 px par image) émet un avertissement.

```python
ticks = [sheet.world(S, i, "tick", n=f) for i in range(3)]
toi.walk(f, toi.place_for(ticks, f - 1))
```

### Méthodes

| Méthode | Retour | Comportement |
|---|---|---|
| `enter(f, at=None, frm=None, d=None, arm_from=2)` | f + d | Pop sur place (`at`, ou sa position) en 300 ms, bras et stylo avec elle ; le bras apparaît à f + `arm_from` (2 par défaut ; 0 : entier dès f, avec le corps). `frm=x` : arrive en marchant depuis x (même y), en évitant x > 940, zone réservée. Après une sortie (`exit`), l'opacité revient à 1. |
| `exit(f, d=POP)` | f + d | Se réduit vers son centre ; la main rejoint le repos, le bras s'efface en 2 images ; opacité 0 à la fin. |
| `walk(f, to, d=None, e="inOut")` | f + d | Glisse vers `to` (x, ou [x, y]) à petits sauts (5 px toutes les 8 images, posée à l'arrivée), penchée de 4° vers l'avant. La main revient au repos en 6 images puis suit le corps. Durée par défaut : distance / 7, au moins 8 images. Ne fait rien si `to` est la position actuelle. |
| `reach(f, target, d=MOVE, e="inOut", step=True)` | f + d | La pointe du stylo va sur `target`. La pose part de la pose précédente (relative à l'épaule) et la rejoint en fondu, sans saut. Hors d'atteinte : un pas pendant le geste ; avec `step=False`, un avertissement et la pointe s'arrête avant. |
| `tap(f, target, d=TAP, lift=14)` | **image du contact** f + d − 1 | Approche à `lift` px de la cible (reach en d − 3 images), coup en 3 images (ease-in), relève de `lift` px en 5 images. Y caler l'événement (coche, fente, « ? »). Pour un contact sur le mot m : `tap(m - TAP + 1, …)`. |
| `trace(f, pts, speed=TRACE_SPEED, d=None, e="linear", lead=None, step=True)` | images de passage sur chaque point | La pointe parcourt la polyligne `pts` (points monde) à vitesse constante (« relis »). Si elle n'est pas sur `pts[0]`, elle y va d'abord en `lead` images : par défaut au moins 4, et 8 si la figurine doit faire un pas. Le retour donne l'image d'arrivée sur chaque point (`hits[0]` = fin de l'approche). |
| `strike(f, a, b, d=6, lead=3, line=None, track="strike", step=True)` | image qui suit le trait | Approche de a (`lead` images, 8 si un pas est nécessaire), puis la pointe file de a à b en d images (ease-in-out). La piste `track` de `line` va de 0 à 1 dans les mêmes images. Points : `sheet.value_span(i)`. |
| `stamp(f, stamp_id, d=6, shake=None, step=True)` | **image du contact** f + d − 1 | Coup de tampon (V01 « décide »), détaillé après le tableau. |
| `rest(f, d=8, e="inOut")` | f + d | La main revient au repos. |
| `hop(f, to, d, h=0, lean=WALK_LEAN)` | f + d | Un seul bond vers `to` ([x, y]) ; `lean` < 0 : penchée en arrière (recul). Remplace les appels privés `_move_body` / `_hand_rest`. |
| `run(f, pts, d)` | f + d | Course à vitesse constante le long d'une polyligne, main au repos. |
| `rim(f, on, d=3)` | f + d | Liseré papier du bras (piste `rim` du limb) : `on=True` le montre (bras tendu qui croise le buste encre), `on=False` l'efface ; à éteindre AVANT que le bras ne se replie contre le buste (sinon une boucle blanche y reste). |
| `lean_to(f, deg, d=POP, e="out")` | f + d | Incline la figurine (piste `lean`) en re-posant le bras image par image. |
| `scale_to(f, s, d=10, e="inOut")` | f + d | Change d'échelle ; bras et stylo suivent ; la taille d'entrée devient `s`. |
| `stow(f, d=4)` / `unstow(f, d=6)` | f + d | Range le stylo (il se réduit dans la main) / le fait revenir (pop). |
| `set_z(f, z, tool_z=None)` | f | Change de calque ; avec `tool_z`, le bras passe en `tool_z` et le stylo en `tool_z` + 0,5. |
| `tip(n)` | [x, y] | Pointe du stylo à l'image n. |
| `reach_max(n, pen=True)` | px | Allonge maximale à l'échelle de l'image n. |

Déroulé de `stamp`, à partir de l'image f :
1. **Apparition.** L'entité `stamp` est cachée à f − 1, apparaît à 1,4 dans la main à f et s'abat à 1 en d images
   (ease-out).
2. **Main.** La main tient la poignée : prise = [0, −(h/2 + neck + knobH/2)], `GEOM.STAMP_HANDLE`. Le stylo est caché.
3. **Contact.**
   - `shake` (un id, par exemple la fiche) secoue en xy à hit + 1.
   - La figurine plonge de 6 px et penche vers la cible de 6°, puis −2°, puis 0.
4. **Retour.** La poignée s'efface à hit + 3 et la main revient au repos. Le stylo réapparaît à hit + 10 par un pop :
   il ne passe jamais au-dessus de la fiche.
5. **Pas.** Si la poignée est hors d'atteinte (98 % de la main seule), la figurine fait un pas de 8 images AVANT f,
   pendant que la main rejoint le repos.

```python
toi = Figure(kit, "toi", pos=[880, 955])
hit = toi.tap(f, sheet.world(S, 0, "tick", n=f))
kit.draw("coche1", hit, 6)                                  # la coche se trace au contact
hits = toi.trace(g, [sheet.world(S, i, "tick", n=g) for i in range(3)])
for t, h in zip(["coche2", "coche3"], hits[1:]):
    kit.draw(t, h, 6)                                       # chaque coche sous la pointe
a, b = (S.to_world("fiche", q, h) for q in sheet.value_span(2))
toi.strike(h + 2, a, b, line="fiche_L3")                    # barre « retraite »
toi.stamp(kit.at("S19", "compris."), "tampon", shake="fiche")
```

## 8. Fiche : `Sheet`

`Sheet(n=5, w=500, h=None, head=84, pitch=104, top=52, ty=-22, ly=23, slot_h=92, strip=48)` donne la mise en page d'une
fiche (brief, checklist).
- `Sheet(5)` redonne exactement la fiche de V01 : rangées −224, −120, −16, 88, 192.
- Hauteur par défaut : head + top + pitch·(n − 1) + slot_h/2 + 122 (720 pour n = 5, 512 pour n = 3). Les 122 px du
  bas restent libres pour le tampon ou l'autocollant.

| Attribut ou méthode | Contenu |
|---|---|
| `rows` | centres y des rangées (repère local de la fiche) |
| `x` | colonnes : `bullet` −w/2 + 2, `text` −w/2 + 44, `value` w/2 − 100, `tick` w/2 − 50, `slot0` −w/2 + 18, `slot1` w/2 − 78 |
| `pt(i, col="value", line="text")` | point local : colonne `col` (nom ou x) de la rangée i, sur la ligne de texte (`"text"`, rangée + ty), de date (`"date"`, rangée + ly) ou au centre (`"row"`) |
| `world(S, i, col, line, n)` | le même point en monde à l'image n (après `add`) |
| `add(kit, id, lines, pos, title="Brief", scale=1, z=8, typed=True, show=True)` | déclare la fiche et ses rangées, lines = [(clé, valeur, pictogramme)] ; renvoie les ids `id_L1…` |
| `line_params(key, value, icon="none", **over)` | paramètres d'une entité `line` : valeur mesurée, fente (crackX) entre la clé et la valeur, trait, chute |
| `value_span(i, pad=8)` | extrémités locales (droite, gauche) de la valeur de la rangée i : le trait qui barre |
| `ticks(kit, prefix, color, size=40, sw=8, variant=None)` | une coche par rangée, dans la colonne des coches (`draw` = 0) ; ids `prefix1…` |

Détails de `add` :
- Les rangées sont enfants de la fiche, en z + 1, avec toutes les pistes de la ligne V01 à leur valeur neutre.
- `typed=True` : rangées vides, à écrire avec `kit.type`. `grow=0` : bande de texte, sans la rangée pleine.

```python
sheet = Sheet(n=3)
rows = sheet.add(kit, "fiche", [("Dossier", "12 docs", "bars"), ("Contrat", "AV 2019", "shield"),
                                ("Objectif", "retraite", "cal")], pos=[390, 820], scale=0.9)
coches = sheet.ticks(kit, "coche", STYLE["deep"])
kit.stagger(rows, f, 6, kit.type, rate=2, flash=True)
```

## 9. Fonctions utilitaires (module)

| Fonction | Rôle |
|---|---|
| `solve_ik(shoulder, target, l1, l2, bend=1)` | → (coude, main, atteint). Hors d'atteinte, la main s'arrête sur la droite épaule → cible : les longueurs restent exactes. `bend` +1 / −1 : côté du coude. |
| `rotate_about(pt, deg, c)` | rotation autour de c, comme entities.tsx (penché `lean`) |
| `frames(f, d, e)` | (image, progression assouplie) d'un segment de d images, avec LEAD : à écrire soi-même un trajet image par image |
| `lerp(a, b, p)`, `ang_lerp(a, b, p)` | interpolation (nombres ou points) ; angle par le plus court chemin |
| `crowd_points(p)` | positions locales des figurines d'une `crowd` (copie de crowdPoints ; `pts: []` = foule vide) |
| `format_fr(v, decimals=0, sign=False)` | nombre français comme le compteur : U+202F entre les milliers, virgule, U+2212 pour le moins ; demis arrondis comme Math.round (2,5 -> 3) |

## 10. Démonstration et rendu

```bash
python3 scripts/story/_demo_kit.py --props                  # -> build/kit_demo/props_demo.json
python3 scripts/story/_demo_kit.py --stills 0 36 77 114 166 # images de la démo -> build/kit_demo/stills_demo/
python3 scripts/story/_demo_kit.py --clip                   # -> build/kit_demo/demo_kit.mp4 (voix + sous-titres)
```

Fonctionnement :
- La démo passe par `pipeline.story.build_props` sur la fenêtre 51,038 s → fin de V01 (S18 à S20, images 1524-1747).
- Elle remplace la mise en scène de V01 par la sienne et écrit sous `build/kit_demo/` : rien dans `build/V01/story/`
  ni dans `output/`.
- Les images fixes et le clip prennent le verrou de rendu (`build/.render.lock`).

Contenu, mot par mot :

| Mot | Ce qui se passe |
|---|---|
| « Avant » | la jauge de temps se vide pendant que le compteur monte à 45 min |
| « arrives » | la figurine marche jusqu'à `place_for`, et les trois lignes s'écrivent |
| « cherché » | la jauge et le compteur passent au rouge (pulse, shake) |
| « Après » | le repère passe à 2, la jauge sort (morph) ; tapotement sur la 1re coche, tracée au contact |
| « arrives » | la pointe relit la colonne, et chaque coche se trace sous elle |
| « compris » | coup de tampon COMPRIS, la fiche tremble |
| « Abonne-toi » | outro, avec le clic sur « comprendre » |

## 11. Pièges

- **Bras qui se détache.** Seules les méthodes de `Figure` bougent la figurine, son bras et son stylo. Un `kit.move`, un
  `kit.pin` ou un `S.key` sur la figurine décroche le bras.
- **Épingle ignorée.** `kit.pin(f, …)` suivi d'un mouvement qui commence sur la même image f : le mouvement part de la
  valeur de f − 1 et l'épingle ne sert à rien. Épingle à f − 1 (voir § 3).
- **`morph` et figurine.** Ne pas passer une figurine dans les `outs` d'un `morph` : appeler `fig.exit(f)` sur la même
  image.
- **Pas automatique saccadé.** Un pas automatique pendant un geste court (tap : 5 images d'approche) est saccadé, et
  l'avertissement le signale. Placer la figurine avant avec `walk` + `place_for`.
- **Tampon.** Il ne prolonge pas le bras : il faut se tenir à moins de 161 px de la poignée. Le poser en bas à droite de
  la fiche, côté figurine.
- **Morph sur un marqueur V01.** Un marqueur déclaré à la main avec des `xs` absolus (V01) se réduit vers le coin
  (0, 0) de l'écran. Utiliser `kit.steps_marker`.
- **Couleur en fondu.** Une piste de couleur ne se fond qu'entre deux hex. `S.set(id, fill=STYLE["cyan"])` d'abord,
  jamais le nom `"cyan"`.
- **Valeur initiale.** `pop` remet l'échelle à 0 à f − 1 si elle ne l'est pas. Un élément visible avant ce pop
  clignote : le déclarer avec `scale=0`.
- **Recouvrement.** Deux macros sur la même piste qui se recouvrent : la clé posée en dernier gagne sur les images
  communes, et l'autre est coupée net. Enchaîner sur la valeur de retour.
