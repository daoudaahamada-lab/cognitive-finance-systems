# Verbes visuels : ce qu'on écrit dans le storyboard, ce qui le réalise

Un storyboard est jugé sur deux choses : un spectateur muet comprend l'action, et la mise en scène peut la construire
sans inventer d'outil. Ce tableau relie chaque verbe visuel à son sens sans le son, aux entités Story qui le dessinent et
aux macros du kit qui l'animent. Écrire les `evenement` avec ces verbes rend le storyboard constructible tel quel.

Catalogue complet : `../../wth-story-build/references/entities.md` (paramètres et pistes) et `kit.md` (macros, figurine,
fiche, fin). Les noms entre accents graves sont ceux du code.

## 1. Les 14 verbes de base

| Verbe | Ce que lit le spectateur muet | Entités | Macros et pistes | Exemple (V01 sauf mention) |
|---|---|---|---|---|
| **entrer** | « ça arrive », « ça commence » | toute entité ; `Figure` | `kit.pop(id, f, from_pt=…)` ; `kit.drop` pour « arriver, tomber » ; `kit.morph(outs, ins, f)` pour un relais ; `fig.enter(f, frm=x)` (marche depuis x) | S01 : la chemise s'ouvre, les 4 documents glissent vers 4 places ; S09 : les briques « RGPD » tombent dans le mur |
| **buter** (être bloqué) | « interdit », « limite » | obstacle `shape` (barre, mur), `window`, `icon` `lock` | `kit.move` jusqu'au contact puis retour en ease-out ; `kit.shake(id, f, axis="x")` sur ce qui est refusé | S06 : le faisceau de l'IA bute sur le bord du cadre ; S08 : le mail rebondit sur le mur |
| **extraire** | « on en tire une information » | `bullet`, `pill`, `text`, `icon` sur disque, depuis un `doc` ou un PNG | `kit.pop(id, f, from_pt=source)` puis `kit.move(id, g, to)` | S10 : une pastille sort de chaque document, puis une 5e, vide, de la tête de l'IA |
| **empiler / ranger** | « ça s'organise » | `line` (fiche `Sheet`), `shape`, `doc` | `kit.stagger(ids, f, step, kit.move, to=…)` ; `kit.drop(…, to=…)` sur une pile ; `kit.type` pour écrire une rangée | S10-S11 : les pastilles deviennent les lignes de la fiche |
| **relier** | « ceci prouve cela » | `wire` plein (preuve) ou pointillé (IA), `label` (date → étiquette-source) | `kit.draw(wire, f)` ; `S.along_wire` pour faire glisser un objet le long du fil | S12 : un fil part de chaque ligne vers son document ; la date glisse jusqu'à la ligne |
| **fissurer / casser** | « c'est faux », « ça ne tient pas » | `line` (pistes `alarm`, `pulse`, `red`, `crack`) ; ailleurs deux `shape` | `kit.pulse(id, f, track="pulse")`, clés `red` puis `crack` ; `kit.drop(moitie, f, out=True)` | S11 : « Horizon : 5 ans » vire au rouge et casse — **à déclencher par le stylo de « Toi »** |
| **barrer** | « on retire », « on corrige » | `line` (pistes `strike`, `fall`) ; ailleurs une `shape` `poly` ouverte | `fig.strike(f, a, b, line=…)` (points : `Sheet.value_span`) ; `fall` fait tomber la valeur barrée | S14 : le conseiller barre « 5 ans » |
| **tamponner** | « c'est décidé » | `stamp` (texte ExtraBold `deep`) | `fig.stamp(f, "tampon", shake="fiche")` (renvoie l'image du contact) | S14 : tampon sur « décide » ; jamais « VALIDÉ » si une question reste ouverte |
| **remplir** | « ça monte », « c'est complet » | `gauge`, `sector`, `counter`, `crowd` (`show`), `shape` (`fillOp`) | `S.key(id, "value", f, v, d, "linear")` ; `kit.draw` pour un contour | S17 : le secteur de 10 minutes se remplit au rythme du stylo |
| **vider / fondre** | « ça s'en va », « on perd » | `gauge` (`dir="left"`), `counter`, jetons `shape` | clé `value` vers le bas ; couleur `cyan` → `red` en hex ; `kit.drop(…, out=True)` pour ce qui part | S04 : à chaque saut du conseiller, un bloc de la barre de temps devient gris et tombe dans les papiers ; idée pour V03 : les frais prélèvent un jeton chaque année |
| **basculer / peser** | « le poids est de ce côté », « injuste » | `seesaw` + objets enfants (`kit.seat`) | `S.key(id, "rot", f, deg, TILT, "out")` | S15-S16 : l'IA apporte, « Toi » porte le poids |
| **compter** | « combien » | `counter`, `crowd`, n `shape` | clé `value` (format français automatique) ; `kit.stagger(ids, f, 2, kit.pop)` | référence : 33 cercles sur « 33 ans » ; idée pour V03 : un compteur de 10 000 € à 26 500 € |
| **comparer** | « avant / après », « l'un contre l'autre » | deux `gauge`, deux `curve`, deux colonnes, `pill` « Avant » / « Après » | même objet montré dans deux états côte à côte ; `kit.move` pour les rapprocher | S18-S19 : la pile « Avant », la fiche « Après » |
| **rembobiner** | « retour au début », « sans méthode » | `icon` `rewind` (◀◀) | `kit.pop` du ◀◀, puis `kit.move` des éléments vers leur place d'avant | S03 : remplace la pile qui éclatait (lue « l'IA a échoué ») |

## 2. Gestes de « Toi » (figurine articulée `Figure`)

| Verbe | Sens | Macro | Note |
|---|---|---|---|
| toucher, pointer | « c'est lui qui déclenche » | `fig.tap(f, cible)` → image du contact | y caler l'effet : fissure, coche, « ? » qui naît |
| relire | « il vérifie tout » | `fig.trace(f, points)` (vitesse constante) | dérive narrative légitime ; une coche sous la pointe à chaque passage |
| cocher | « vérifié par lui » | `fig.tap` + `kit.draw(coche, contact)` | coche pleine `deep` ; celle de l'IA est `variant="ai"` |
| marcher, se placer | « il s'approche » | `fig.walk(f, fig.place_for(cibles, f))` | une seule marche avant une séquence de gestes |
| cliquer | « il agit sur l'outil » | `cursor` + `kit.click` | le pointeur est sa main à l'écran : même encre |
| demander | « question pour quelqu'un » | `qmark` né sous le stylo (`kit.pop(…, from_pt=valeur)`), `bubble` (pistes `s`, `q`) | la bulle part de « Toi », tournée vers l'autre personne |

## 3. Autres verbes utiles

| Verbe | Entités, macros |
|---|---|
| écrire | `kit.type(id, f, rate=…)` sur une `line` ou un `text` ; `kit.type` renvoie l'image où tout est écrit |
| délimiter, enfermer | `shape` dont le contour se trace (`draw=0` puis `kit.draw`) ; puis `window` (pistes `seal`, `lock`) |
| sceller, autoriser | `window` `seal` (« ✓ Cabinet ») ; `icon` `building` |
| croître, s'accumuler dans le temps | `curve` (`kit.draw(id, f, 20)`), `area` pour l'aire ; deux courbes pour un écart (frais, inflation) |
| se disperser | `kit.stagger` de `kit.move` vers des places éloignées, ou `kit.morph` d'un objet en plusieurs |
| fusionner, devenir | `kit.morph(outs, ins, f)` apparié (relais à la même place) |
| sortir, se ranger | `kit.vanish(id, f, into=…)` ; une figurine : `fig.exit(f)` |
| surligner, souligner | `text` pistes `mark`, `under` |
| alerter | `kit.pulse` + couleur `red` ; `icon` `warning` ; `kit.shake` |
| attendre, durer | `sector` qui se remplit ; `icon` `clock`, `pause` |
| verrouiller | `icon` `lock` ; `window` `lock` |
| typer un chiffre-clé | `counter` ou `text` ExtraBold en `cyan`/`red`, pop sur son mot |

Pictogrammes disponibles (`icon`) : euro, bars, mail, shield, cal, building, check, person, rewind, clock, house, bank,
coin, percent, lock, cart, moon, pause, warning, phone, plus, minus, arrow (tourner avec `rot`).

## 4. Hors catalogue

Quand aucun verbe ne convient :
1. Chercher d'abord une composition de verbes existants (un mur = une `shape` ; une pièce = un cercle avec `icon` `coin`).
2. Sinon, déclarer l'élément dans `entites_nouvelles` : nom, forme, pistes, et pourquoi rien ne suffit. **Au plus 3
   par film, et simples** : formes plates paramétrées et une ou deux pistes. Pas de personnage articulé au-delà de
   `Figure`, pas de 3D, de liquide ni de particules : le juge « sens-faisabilité » pénalise.
3. Proscrits : zoom sur un PNG pour raconter, apparition en fondu d'une forme, mouvement continu sans raison (flotter,
   respirer), caméra ou zoom global, coupe sèche entre compositions.
