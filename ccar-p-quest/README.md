# Tour de l’Architecte

Jeu d’entraînement à l’examen **Claude Certified Architect – Professional (CCAR-P)** d’Anthropic.

Dix étages, dix boss, 100 questions au format de l’examen. Les questions sont en anglais, comme le jour J. Les explications sont en français.

## Comment ça marche

Chaque étage suit trois étapes :

1. **Fiches** : 6 notions clés, chacune avec le piège classique de l’examen et un lien vers la doc officielle.
2. **Échauffement** : 5 affirmations vrai/faux pour vérifier que les notions sont acquises. Il débloque le boss.
3. **Boss** : 10 questions d’examen, dans un ordre aléatoire, avec 3 vies. Il faut au moins 8/10 pour le vaincre (l’examen demande 720/1000). Une victoire débloque l’étage suivant.

Après chaque réponse, le jeu explique pourquoi chaque option est juste ou fausse, donne un réflexe d’examen et la page de doc officielle à relire. Les questions ratées vont dans la **salle de révision**, et en sortent quand tu les réussis.

| Étage | Thème | Boss | Domaines |
|---|---|---|---|
| 1 | Modèles, prompting et contexte | L’Ambigu | D2 ×9, D1 ×1 |
| 2 | Conception de solution | Le Sur-Ingénieur | D1 ×10 |
| 3 | Intégration I : API, tool use, sorties structurées | Le Schéma Brisé | D3 ×10 |
| 4 | Intégration II : MCP, RAG, clouds | L’Hydre des Connecteurs | D3 ×7, D2 ×3 |
| 5 | Évaluation et tests | Le Vibe-Checker | D4 ×10 |
| 6 | Optimisation : coût, latence, échelle | Le Gouffre à Tokens | D4 ×5, D1 ×4, D6 ×1 |
| 7 | Gouvernance, sécurité et risques | L’Injecteur | D5 ×10 |
| 8 | Parties prenantes et cycle de vie | La Promesse à 99,9 % | D6 ×10 |
| 9 | Productivité des développeurs et opérations | Le Chaos Ops | D7 ×6, D6 ×2, D5 ×2 |
| 10 | Simulation finale, tous domaines | L’Examinateur | les 7 domaines |

Sur les 100 questions, chaque domaine pèse autant qu’à l’examen : D1 17, D2 13, D3 19, D4 16, D5 14, D6 14, D7 7.

## Jouer

- **En ligne** : la version publiée sur claude.ai synchronise ta progression avec ton compte Claude (ordinateur et téléphone).
- **En local** : ouvre `dist/index.html` dans un navigateur. La progression reste dans ce navigateur.

Raccourcis clavier pendant un combat : `A` à `E` (ou `1` à `5`) pour choisir, `Entrée` pour valider puis continuer. À l’échauffement : `V` pour vrai, `F` pour faux.

## Prototype V2 : le combat au lance-pierre

`src/prototype-injecteur.html` est un prototype jouable du combat V2, sur l’étage 7 (L’Injecteur) :

- tu charges ta réponse comme une pierre, tu tires vers l’arrière et tu relâches ; la trajectoire s’affiche pendant la visée ;
- le cœur de verre du boss donne un coup critique ; l’adresse rapporte des points, jamais la bonne réponse ;
- une mauvaise pierre se brise et le boss riposte ; sa barre d’attaque suit un rythme progressif (2 min 28 s par question à l’étage 7, 1 min 54 s au sommet, comme à l’examen) ;
- L’Injecteur glisse parfois une pierre piégée « reçue d’un document externe » : la lancer le soigne, la mettre en quarantaine rapporte des points ;
- phase 2 à mi-vie, combos, sons synthétisés, coup de grâce final.

```bash
node scripts/build-prototype.mjs   # produit dist/prototype-injecteur.html
```

## D’où viennent les questions

Les questions sont **originales**. Elles sont rédigées à partir de la documentation officielle d’Anthropic :

- https://platform.claude.com/docs (API, outils, évaluations, garde-fous, administration)
- https://code.claude.com/docs (Claude Code)
- https://www.anthropic.com/engineering (articles d’ingénierie)

Elles imitent le format et le niveau de l’examen, mais ce ne sont pas les questions réelles, qui sont confidentielles. La répartition par domaine suit le blueprint du CCAR-P (7 domaines, 63 questions, 120 minutes, 720/1000). Le guide d’examen officiel est distribué via l’Anthropic Partner Academy : en cas d’écart, c’est lui qui fait foi.

## Faire évoluer le contenu

```
content/level-XX.json   un fichier par étage (fiches, échauffement, questions)
content/CONTENT_GUIDE.md format et règles de style des questions
src/app.html            le jeu (HTML, CSS et JavaScript sans dépendance)
scripts/validate.mjs    vérifie la structure et l’équilibre des questions
scripts/build.mjs       injecte le contenu et produit dist/
```

Pour modifier ou ajouter des questions :

```bash
node scripts/validate.mjs     # vérifie tous les niveaux
node scripts/build.mjs        # régénère dist/index.html et dist/artifact.html
```

Le validateur refuse un niveau si la répartition par domaine ne suit pas le plan, si une source n’est pas une page officielle, ou si la longueur des options trahit la bonne réponse.
