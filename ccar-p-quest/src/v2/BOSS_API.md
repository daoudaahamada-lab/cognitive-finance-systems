# Interface d'un boss (V2)

Chaque boss est un objet `BOSSES[n]` déclaré dans `src/v2/js/4x-boss-NN.js`. Le moteur (`20-engine.js`) s'occupe de la position, du balancement, du recul, de la cible critique, des collisions et des effets. Le boss ne fait que **se dessiner** et fournir ses répliques. `40-boss-07.js` (L'Injecteur) est l'exemple de référence.

Tous les fichiers `js/` sont concaténés dans un seul scope : les utilitaires de `00-core.js` sont directement disponibles (`col`, `mixv`, `rr`, `clamp`, `lerp`, `rand`, `pick`, `drawCracks`, `angryEyes`, `C`, `F_MONO`, `F_DISPLAY`, `F_BODY`). Ne rien déclarer d'autre au niveau global que `BOSSES[n] = { … }` : mettre les fonctions d'aide à l'intérieur de l'objet ou dans un bloc `{ … }`.

```js
BOSSES[n] = {
  palette: { main, dark, accent, eye, rage },   // hex ; éclats et particules utilisent main/accent ; rage = teinte de la phase 2
  hit: { rx, ry, coreR },      // ellipse du corps et rayon de la cible critique, en unités locales
  top: 120,                    // distance du centre au haut du dessin (ancre de la bulle de dialogue)
  attackFrom: { x, y },        // d'où part sa riposte (unités locales)
  castLean: -0.15,             // inclinaison pendant une action spéciale (b.cast), facultatif
  weakSpot(b) { return { x, y }; },  // position locale de la cible critique (peut bouger avec b.t)
  critLabel: "CRITIQUE",       // texte affiché sur un coup critique, facultatif
  lines: {                     // répliques en français, courtes (moins de 60 caractères)
    hit: [], crit: [], wrong: [], timeout: [], rage: "…",
    special: { … }             // répliques propres à sa mécanique, voir ci-dessous
  },
  intro: { title, text },      // explication de sa mécanique, affichée avant le combat (français, 2 phrases)
  mechanics: [],               // modules de combat (fixés par le moteur, voir la liste plus bas)
  init(b) {},                  // facultatif : prépare b.own (état propre au boss)
  update(b, dt) {},            // facultatif : anime b.own
  draw(c, b) {}                // dessine le boss
};
```

## Repère de dessin

- `draw(c, b)` reçoit un contexte déjà translaté au **centre du boss**, tourné et mis à l'échelle. Le joueur est **à gauche** : le boss regarde vers la gauche.
- Taille : environ 250 unités de large, 200 de haut. Rester dans ±260 en x et ±200 en y. La cible critique doit être visible et lisible.
- `hit.rx`/`hit.ry` doivent couvrir le corps visible (un tir sur le corps doit toucher).

## État `b` (lecture seule, sauf `b.own`)

| Champ | Sens |
|---|---|
| `b.t` | secondes depuis l'apparition (animation au repos) |
| `b.time` | horloge globale en secondes |
| `b.hpFrac` | vie restante lissée, de 0 à 1 |
| `b.flash` | 0 à 1 : éclat blanc juste après un coup (mélanger les couleurs vers le blanc) |
| `b.squint` | 0 à 1 : yeux plissés après un coup |
| `b.rage`, `b.rageT` | phase 2 (vie sous 50 %) et transition 0→1 vers `palette.rage` |
| `b.atk` | `-1` au repos, sinon secondes depuis le début de sa riposte : armement 0–0,22, frappe 0,22–0,34, retour jusqu'à 0,75 |
| `b.cast` | `-1` ou secondes depuis le début d'une action spéciale (0–0,9) |
| `b.stun` | secondes d'étourdissement restantes (yeux ternes) |
| `b.aiming` | le joueur est en train de viser |
| `b.cracks` | fissures d'impact en coordonnées locales : `drawCracks(c, b, couleur)` |
| `b.mech` | état des mécaniques actives (`b.mech.heads.count`, `b.mech.shield.up`…) |
| `b.phase` | 0, 1 ou 2 (étage 10 seulement) |
| `b.own` | objet libre pour l'état propre au boss (rempli dans `init`, animé dans `update`) |

## Règles visuelles

- Vectoriel uniquement (canvas 2D), pas d'image externe. Style cohérent avec L'Injecteur : formes nettes, quelques dégradés, un halo coloré, des yeux expressifs.
- Toujours animer le repos avec `b.t` (respiration, flottement, pièces qui tournent).
- Réagir à `b.flash` (couleurs vers le blanc), `b.squint`, `b.rageT` (couleurs vers `palette.rage`, mouvements plus vifs), `b.atk` (armement visible puis frappe : bouche ouverte, bras, recul…).
- `shadowBlur` sur quelques éléments seulement : le dessin doit rester sous ~1 ms par image.
- Le visage doit exprimer l'anti-pattern du boss : il est l'ennemi que l'architecte apprend à vaincre.

## Mécaniques disponibles (`mechanics`)

| Module | Effet en jeu | Ce que le boss doit fournir |
|---|---|---|
| `fog` | brouillard qui cache la cible critique et raccourcit la visée ; chaque bonne réponse le dissipe | `lines.special.fog` |
| `turrets` | construit à chaque question une tourelle « multi-agents » qui bloque les tirs ; une bonne réponse les fait tomber | `lines.special.build`, `lines.special.collapse` |
| `heads` | une tête leurre de plus à chaque erreur (pas de critique sur un leurre, la barre d'attaque accélère) ; une bonne réponse en coupe une | `headLocal(i, count, b)` : position locale de la tête leurre `i` ; dessiner `b.mech.heads.count` têtes à ces positions ; `lines.special.grow`, `lines.special.cut` |
| `shuffle` | mélange les pierres toutes les 25 s et après un tir raté | `lines.special.shuffle` |
| `tokens` | la barre d'attaque va plus vite ; une bonne réponse dans les premiers 40 % = « cache hit » ×2 | `lines.special.cache` |
| `injection` | pierre piégée à mettre en quarantaine | `lines.special.inject`, `quarantine`, `absorbed` |
| `shield` | bouclier SLA : dégâts divisés par deux tant qu'il n'y a pas 3 bonnes réponses d'affilée ; une erreur le regonfle | `lines.special.shieldUp`, `shieldBreak` |
| `incidents` | incidents qui foncent vers le joueur ; un toucher les acquitte, un hook les bloque | `lines.special.incident`, `hook` |

## Vérifier un boss

```bash
node scripts/preview-bosses.mjs      # produit dist/dev/boss-preview.html
```

La page montre chaque boss dans plusieurs états (repos, coup reçu, riposte, rage avec fissures, vie basse, action spéciale). Faire une capture avec Playwright et la regarder.
