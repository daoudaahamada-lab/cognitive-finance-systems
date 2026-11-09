# Interface d'un boss (version 2)

Chaque boss est un objet `BOSSES[n]` dans `src/v2/js/4x-boss-NN.js`. Le moteur (`20-engine.js`) gère la position, les collisions, la cible critique, les effets et le son. Le boss fournit son **dessin dans tous ses états**, son **décor**, son **projectile** et ses **répliques**.

Tous les fichiers `js/` sont concaténés dans un seul scope. Les utilitaires de `00-core.js` sont donc disponibles directement :

- couleurs : `col(c, alpha)`, `mixv(a, b, t)` (renvoie `[r,g,b]`, accepté par `col`), `C` (jetons : `C.ink`, `C.lamp`, `C.bad`, `C.ok`, `C.night`, `C.white`…) ;
- formes : `rr(c, x, y, w, h, r)` (rectangle arrondi, à remplir ensuite), `drawCracks(c, b, couleur, épaisseur)`, `angryEyes(c, x, y, w, h, couleur, squint, glow)` ;
- nombres : `clamp`, `lerp`, `rand`, `pick`, `seeded(graine)` ;
- animation : `easeOut`, `easeIn`, `easeInOut`, `backOut` (dépassement), `seg(t, a, b)` (avancement de `t` dans `[a, b]`), `atkPose(b)` ;
- polices : `F_DISPLAY`, `F_MONO`, `F_BODY`.

Ne rien déclarer d'autre au niveau global que `BOSSES[n] = { … }`. Les fonctions d'aide vont dans l'objet (méthodes) ou dans un bloc `{ … }` autour de la déclaration.

## L'objet

```js
BOSSES[n] = {
  v: 2,                                  // obligatoire : le boss gère b.enter et b.dying
  palette: { main, dark, accent, eye, rage },  // hex. Éclats et particules : main/accent. rage = teinte de la phase 2
  sky: ["#haut", "#milieu", "#horizon"], // facultatif : remplace le dégradé du ciel de l'étage
  hit: { rx, ry, coreR },                // ellipse du corps et rayon de la cible critique (unités locales)
  top: 150,                              // distance du centre au haut du dessin (ancre de la bulle de dialogue)
  attackFrom: { x, y },                  // d'où part le projectile (unités locales)
  castLean: -0.15,                       // inclinaison pendant une action spéciale (facultatif)
  weakSpot(b) { return { x, y }; },      // position locale de la cible critique (peut bouger avec b.t)
  critLabel: "CRITIQUE",                 // texte du coup critique
  epitaph: "CLARIFIÉ",                   // mot tamponné à l'écran à sa mort (1 ou 2 mots, majuscules)
  lines: { hit: [], crit: [], wrong: [], timeout: [], gloat: [], rage: "…", special: { … } },
  intro: { title, text },                // sa mécanique expliquée avant le combat (2 phrases)
  mechanics: ["…"],                      // fixé par le moteur : ne pas changer
  shot: { color, spin, draw(c, s) {} },  // son projectile de riposte
  motion(b, env) { return { x, y }; },   // facultatif : sa façon de se déplacer
  backdrop(c, env) {},                   // décor fixe de son étage
  ambient(c, env, b) {},                 // facultatif : décor animé (léger)
  init(b) {}, update(b, dt) {},          // facultatifs : état propre dans b.own
  draw(c, b) {}                          // dessine le boss dans tous ses états
};
```

## Repères

**Dessin du boss (`draw`)** : le contexte est déjà translaté au centre du boss, tourné et mis à l'échelle (×1,15 dans l'arène). Le joueur est **à gauche** : le boss regarde vers la gauche. Rester dans **x de −230 à +185** (le bord droit de l’arène est à 190 unités du centre) **et y de −190 à +190**. `hit.rx`/`hit.ry` couvrent le corps visible.

**Décor (`backdrop`, `ambient`)** : coordonnées du monde. `env = { W, H, groundY, n, rnd, time }` avec `W ≈ 760` (parfois plus large), `H ≈ 600 à 850`, `groundY = H − 64`. Le sol est à `groundY` ; le parapet crénelé couvre `groundY − 58 … groundY` et est repeint **par-dessus** le décor. Le joueur se tient vers `x ≈ 110`, le boss flotte vers `x ≈ 0,71 × W`, `y ≈ groundY − 312`. Toujours placer les éléments **par rapport à `W` et `groundY`** (jamais en coordonnées absolues), car l'arène change de taille.

## État `b` (lecture seule, sauf `b.own`)

| Champ | Sens |
|---|---|
| `b.t`, `b.time` | secondes depuis l'apparition ; horloge globale |
| `b.enter` | **entrée en scène** : 0→1 en 1,5 s, puis reste à 1 |
| `b.dying` | **mort** : −1 en vie, puis 0→1 en 1,7 s après le coup de grâce ; à 1 le moteur retire le boss |
| `b.hpFrac` | vie restante lissée, de 0 à 1 |
| `b.dmg` | **stade de dégâts** : 0 (intact), 1 (< 75 %), 2 (< 50 %), 3 (< 25 %) |
| `b.flash` | 1→0 juste après un coup reçu (éclat blanc, écrasement) |
| `b.squint` | 1→0 : yeux plissés de douleur |
| `b.rage`, `b.rageT` | phase 2 (vie < 50 %) ; `rageT` va de 0 à 1 pendant la transformation |
| `b.atk` | −1 au repos, sinon secondes depuis le début de la riposte. Utiliser `atkPose(b)` → `{ on, wind, strike, rec }`, chacun de 0 à 1 : armement (0,45 s), détente (0,15 s, le projectile part au début), retour (0,4 s) |
| `b.cast` | −1, ou secondes (0→0,9) depuis le début d'une action spéciale de sa mécanique |
| `b.stun` | secondes d'étourdissement restantes |
| `b.look` | `{ x, y }` entre −1 et 1 : où regarder (la pierre en vol, sinon le joueur). **Les pupilles suivent ce vecteur.** |
| `b.threat` | 0→1 : le joueur bande son lance-pierre (le boss peut se crisper, se protéger) |
| `b.gloat` | 1→0 : il vient de toucher le joueur (ricanement, pose de victoire) |
| `b.talk` | 0→1 : ouverture de bouche pendant qu'une bulle de dialogue est affichée |
| `b.beat` | 1→0 à chaque temps de la musique (rebond léger, pulsation) |
| `b.cracks` | fissures d'impact : `drawCracks(c, b, couleur)` |
| `b.mech` | état des mécaniques (voir plus bas) |
| `b.phase` | 0, 1 ou 2 (étage 10) |
| `b.isMirage` | vrai quand le moteur dessine une copie leurre (étage 1) |
| `b.own` | objet libre pour l'état propre au boss |

## Ce que `draw` doit montrer

1. **Repos vivant** : respiration, flottement, pièces qui bougent (`b.t`), pulsation sur `b.beat`, pupilles qui suivent `b.look`, clignements.
2. **Entrée en scène** (`b.enter < 1`) : une arrivée propre au personnage (il se condense, s'assemble, tombe du ciel, se gonfle…). À `b.enter = 0` on ne voit presque rien ; à 1 il est en place. Utiliser `backOut`/`easeOut` pour l'élan.
3. **Coup reçu** : `b.flash` (couleurs vers le blanc, écrasement/étirement), `b.squint`.
4. **Dégâts progressifs** (`b.dmg` 1, 2, 3) : il s'abîme visiblement (pièces qui manquent, fuites, rustines, lunettes cassées…), en plus des fissures.
5. **Rage** (`b.rageT`) : une vraie transformation (forme, posture, détails en plus), pas seulement une teinte.
6. **Riposte** (`atkPose(b)`) : armement lisible (il recule, charge, lève le bras), détente vers la gauche, retour.
7. **Action spéciale** (`b.cast`), **étourdissement** (`b.stun`), **ricanement** (`b.gloat`), **parole** (`b.talk`), **crispation** (`b.threat`).
8. **Mort** (`b.dying` 0→1) : une fin propre au personnage (il s'évapore, tombe en pièces, se dégonfle en zigzag, implose…). À 1, il ne reste presque rien : le moteur ajoute l'explosion finale, le mot `epitaph` et les confettis.

## Projectile (`shot`)

`shot.draw(c, s)` dessine le projectile centré sur l'origine, **pointe vers +x** (le moteur l'oriente dans le sens du vol), dans un carré d'environ 40 unités. `s = { t, k, rage }` (`t` secondes de vol, `k` avancement 0→1). `shot.spin` (radians par seconde) le fait tournoyer au lieu de l'orienter. `shot.color` colore sa traînée.

## Déplacement (`motion`)

`motion(b, env)` renvoie le décalage `{ x, y }` du boss par rapport à sa position de repos, en unités du monde. Le moteur le borne à −90…+40 en x et −80…+70 en y. Sans `motion`, le boss flotte doucement. Donner à chaque boss une allure propre (lourd, nerveux, dansant…) et la rendre plus vive quand `b.rage`.

## Décor (`backdrop`, `ambient`)

`backdrop(c, env)` est peint **une seule fois** dans le fond : après le ciel et la ville lointaine, avant le parapet. Il installe le lieu de l'étage (voir le nom de l'étage) avec quelques éléments forts : silhouettes, machines, lumières. Rester sobre derrière le boss (zone `x > 0,45 × W`, `y < groundY − 120`) pour qu'il se détache, et ne rien mettre d'important sous `groundY − 58`. `env.rnd()` est un générateur pseudo-aléatoire stable.

`ambient(c, env, b)` est dessiné **à chaque image** derrière le boss : un ou deux éléments animés au maximum (fumée, étincelles, radar qui tourne, projecteur). Rester très léger.

## Règles visuelles

- Vectoriel uniquement (canvas 2D), aucune image externe. Formes nettes, quelques dégradés, un halo coloré, des yeux très expressifs.
- Lisible en petit : le boss fait environ 150 px de large sur téléphone. Silhouette forte, peu de détails fins indispensables.
- Performance : `draw` sous 1,5 ms. `shadowBlur` sur quelques éléments seulement, pas de boucle de plus de ~60 éléments par image.
- Le personnage incarne un anti-pattern d'architecte : son visage, sa posture et ses répliques doivent le raconter.
- Répliques en français, moins de 60 caractères, avec du caractère. `lines.gloat` : ce qu'il dit quand il touche le joueur.

## Mécaniques (`mechanics`, état dans `b.mech`)

| Module | Effet en jeu | État utile au dessin | Répliques attendues (`lines.special`) |
|---|---|---|---|
| `fog` | brouillard : cache la cible critique, raccourcit la visée ; par moments un **mirage** (copie leurre, `b.isMirage`) apparaît | `b.mech.fog.shown` (0→1) | `fog`, `mirage` |
| `turrets` | tourelles « multi-agents » qui bloquent les tirs | `b.mech.turrets.list.length` | `build`, `collapse` |
| `parse` | alternance **valide / corrompu** : touché quand il est corrompu, les dégâts tombent à ×0,6 et pas de critique | `b.mech.parse.bad` (booléen), `b.mech.parse.k` (0→1, avancement dans l'état en cours) | `corrupt`, `valid` |
| `heads` | une tête leurre de plus à chaque erreur | `b.mech.heads.count` ; fournir `headLocal(i, count, b)` et dessiner ces têtes | `grow`, `cut` |
| `shuffle` | mélange les pierres | — | `shuffle` |
| `tokens` | barre d'attaque plus rapide ; réponse rapide = « cache hit » ×2 | — | `cache` |
| `injection` | pierre piégée à mettre en quarantaine | — | `inject`, `quarantine`, `absorbed` |
| `shield` | bouclier SLA : dégâts ÷2 jusqu'à 3 bonnes réponses d'affilée (le moteur dessine la bulle) | `b.mech.shield.up`, `b.mech.shield.streak` | `shieldUp`, `shieldBreak` |
| `incidents` | incidents à acquitter ; un hook les bloque | `b.mech.incidents.hook` | `incident`, `hook` |

Toujours lire `b.mech` prudemment (`b.mech.parse && b.mech.parse.bad`) : les portraits de la tour dessinent le boss sans mécanique active.

## Vérifier un boss

```bash
node scripts/preview-bosses.mjs 3 --out b3.html          # aperçu du seul boss 3
node scripts/shot.cjs dist/dev/b3.html /chemin/b3.png     # capture, animation en cours
node scripts/shot.cjs dist/dev/b3.html /chemin/b3-f25.png f=0.25   # boucles figées à 25 %
```

La page montre 8 états (repos, coup reçu, riposte, rage, vie basse, action spéciale, entrée, mort), puis le boss dans l'arène avec son décor, son déplacement et son projectile. Les pointillés montrent l'ellipse de touche, la cible critique (rouge), le point de départ du projectile et le haut du dessin ; ajouter `noguides` à l'ancre (`f=0.5,noguides`) pour les masquer. Capturer l'entrée et la mort à plusieurs instants (`f=0.15`, `0.4`, `0.7`, `0.95`) et regarder les images.
