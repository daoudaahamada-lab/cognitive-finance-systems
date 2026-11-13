# Tour de l’Architecte

Jeu d’entraînement à l’examen **Claude Certified Architect – Professional (CCAR-P)** d’Anthropic.

Dix étages, dix boss à abattre au lance-pierre, 100 questions au format de l’examen. Les questions sont en anglais, comme le jour J ; les explications sont en français.

## Comment ça marche

Chaque étage suit trois étapes :

1. **Fiches** : 6 cartes à retourner. Chacune donne la notion, le piège classique de l’examen et la page de doc officielle. Tu les classes en « Je sais » ou « À revoir ».
2. **Échauffement** : deux mini-jeux.
   - *Relier* : associer chaque notion à sa définition.
   - *Tir aux pigeons* : un pigeon d’argile traverse l’écran ; tu tires si l’affirmation est vraie, tu le laisses passer si elle est fausse.
3. **Boss** : 10 questions d’examen, 3 vies, au lance-pierre.
   - Tu charges ta réponse (elle devient une pierre), tu tires vers l’arrière, tu vises, tu relâches. « Select TWO » : deux pierres partent ensemble.
   - Bonne réponse : il perd de la vie. Mauvaise : ta pierre se brise et il riposte (−1 vie). Survis aux 10 questions pour le vaincre.
   - Sa cible critique double presque les dégâts. **L’adresse rapporte des points, jamais la bonne réponse** ; le tir automatique (Espace) touche toujours, sans critique.
   - Sa barre d’attaque est progressive : 3 min 37 par question à l’étage 1, 1 min 54 au sommet (le rythme réel de l’examen). Pleine, il frappe.
   - Chaque boss a son entrée en scène, ses stades de dégâts, sa transformation en rage, son projectile, sa mort et le décor de son étage.
   - Ses yeux suivent ta pierre, il annonce sa riposte (ligne rouge et « ! ») et ricane quand il te touche.
   - Phase 2 à mi-vie, combos, coups critiques, coup de grâce final, sons et musique générés dans la page (la musique s'allège pendant la lecture ; elle se coupe depuis l'écran de pause).

Les questions ratées vont dans la **salle de révision**, où tu les retravailles contre un mannequin, sans vies ni chrono. Une bonne réponse les retire de la pile.

## Les dix boss

Chaque boss incarne un anti-pattern d’architecte, et sa mécanique enseigne la leçon de son domaine.

| Étage | Boss | Mécanique | La leçon |
|---|---|---|---|
| 1 | L’Ambigu | Brouillard qui cache sa cible et raccourcit ta visée ; par moments un mirage barre ta ligne de tir | La clarté du prompt |
| 2 | Le Sur-Ingénieur | Construit des tourelles « multi-agents » qui bloquent tes tirs ; une bonne réponse les fait tomber | La solution la plus simple d’abord |
| 3 | Le Schéma Brisé | Il alterne entre « valide » et « corrompu » : il faut tirer au bon moment ; sa cible est l’accolade manquante qui tourne autour de lui | Les sorties structurées |
| 4 | L’Hydre des Connecteurs | Une tête leurre de plus à chaque erreur ; elle attaque plus vite | Trop d’outils exposés |
| 5 | Le Vibe-Checker | Mélange tes pierres toutes les 25 s et après un tir raté | Lire au lieu de mémoriser |
| 6 | Le Gouffre à Tokens | Sa barre file plus vite, mais une réponse rapide fait un « cache hit » ×2 | Coût et latence |
| 7 | L’Injecteur | Glisse une pierre piégée « reçue d’un document externe » ; la lancer le soigne, la mettre en quarantaine rapporte | L’injection de prompt |
| 8 | La Promesse à 99,9 % | Bouclier SLA qui divise tes dégâts tant que tu n’as pas 3 bonnes réponses d’affilée | Promettre ce qui est mesuré |
| 9 | Le Chaos Ops | Incidents à acquitter d’un toucher ; un hook les bloque tous | Les contrôles déterministes |
| 10 | L’Examinateur | Trois phases qui reprennent les pièges de la tour | La synthèse |

Sur les 100 questions, chaque domaine pèse autant qu’à l’examen : D1 17, D2 13, D3 19, D4 16, D5 14, D6 14, D7 7.

## Jouer

- **En ligne** : la version publiée sur claude.ai synchronise ta progression avec ton compte Claude (ordinateur et téléphone).
- **En local** : ouvre `dist/index.html` dans un navigateur. La progression reste dans ce navigateur.

Clavier : `A` à `E` pour charger une pierre, `Espace` pour le tir automatique, `Entrée` pour continuer, `Échap` pour la pause. Échauffement : `V` (vrai, tirer) et `F` (faux, laisser passer).

## D’où viennent les questions

Les questions sont **originales**, rédigées à partir de la documentation officielle d’Anthropic :

- https://platform.claude.com/docs (API, outils, évaluations, garde-fous, administration)
- https://code.claude.com/docs (Claude Code)
- https://www.anthropic.com/engineering (articles d’ingénierie)

Elles imitent le format et le niveau de l’examen, mais ce ne sont pas les questions réelles, qui sont confidentielles. La répartition par domaine suit le blueprint du CCAR-P (7 domaines, 63 questions, 120 minutes, 720/1000). Le guide d’examen officiel est distribué via l’Anthropic Partner Academy : en cas d’écart, c’est lui qui fait foi.

## Structure du code

```
content/level-XX.json      un fichier par étage : fiches, échauffement, 10 questions
content/CONTENT_GUIDE.md   format et règles de style des questions
src/v2/shell.html          squelette de la page
src/v2/styles.css          styles
src/v2/js/00-core.js       données, utilitaires, progression (navigateur + compte Claude)
src/v2/js/10-sound.js      sons synthétisés (Web Audio)
src/v2/js/11-music.js      musique de combat générée (une boucle par boss)
src/v2/js/15-backdrop.js   décor commun de l’arène (ciel, ville, parapet)
src/v2/js/20-engine.js     moteur de combat : arène, lance-pierre, boss, questions
src/v2/js/30-mechanics.js  mécaniques des boss (brouillard, tourelles, injection…)
src/v2/js/4x-boss-NN.js    un fichier par boss : dessin, décor, projectile, répliques (voir src/v2/BOSS_API.md)
src/v2/js/50-dummy.js      mannequin de la salle de révision
src/v2/js/60-training.js   fiches à retourner, relier, tir aux pigeons
src/v2/js/70-screens.js    la tour, la page d’étage, la salle de révision, l’ascenseur
src/v2/js/90-main.js       navigation et démarrage
scripts/validate.mjs       vérifie la structure et l’équilibre des questions
scripts/build.mjs          assemble tout dans dist/index.html et dist/artifact.html
scripts/preview-bosses.mjs page d’aperçu des boss (dist/dev/boss-preview.html)
scripts/shot.cjs           capture d’écran d’une page locale (outil de développement, demande Playwright)
```

```bash
node scripts/validate.mjs        # vérifie les 10 niveaux
node scripts/build.mjs           # régénère dist/index.html et dist/artifact.html
node scripts/preview-bosses.mjs  # aperçu des boss : huit états, puis dans leur arène
```

Le validateur refuse un niveau si la répartition par domaine ne suit pas le plan, si une source n’est pas une page officielle, ou si la longueur des options trahit la bonne réponse.
