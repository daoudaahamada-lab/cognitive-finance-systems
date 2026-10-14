# Vidéo v2 : « Je joue au jeu de la vie »

Évolution de la vidéo d’origine (`../video-immeuble-agents/`, conservée intacte) : même identité visuelle, mêmes captures et mêmes animations, mais un récit en 6 étapes porté par une voix off, et un plan final sur l’avatar du joueur.

Vertical **1080 x 1920, 30 i/s, environ 59 s**, avec [Remotion](https://www.remotion.dev) (React) et Three.js pour l’avatar.

## Démarrer

Prérequis : Node.js 18 ou plus récent.

**Déposez d’abord les 13 captures dans `public/captures/`** (mêmes noms que la v1, voir `public/captures/LISEZMOI.md`).
Elles ne sont pas versionnées (le dépôt est public) et le rendu échoue sans elles.

```bash
npm install
npm run studio        # aperçu interactif
npm run render        # MP4 avec voix off -> out/immeuble-agents-v2.mp4
npm run render:muet   # MP4 sans voix (sous-titres conservés), pour doubler soi-même
```

L’avatar final est rendu en 3D par logiciel (`swangle`) : ça fonctionne sur toute machine, avec ou sans carte graphique.

## Le récit

| Étape | Ce que raconte la voix | Ce que montre l’image |
|---|---|---|
| 1. Le point de départ | Plusieurs projets en parallèle, et le besoin de clarté pour savoir où mettre son énergie. | Les vraies salles du jeu en pastilles éparpillées, qui finissent par s’emballer. |
| 2. L’idée | Ma vie comme un immeuble que je construis. | Chaque pastille rejoint son étage, l’immeuble se construit sous nos yeux. |
| 3. L’organisation | Un domaine par étage, un agent IA par étage, un sous-agent par salle. | Noms des étages, ascenseur où chaque étage reçoit son « Agent IA », salle Sales, son sous-agent et sa mission. |
| 4. Le jeu | Objectif, tâches, validation, crédits, construction. | Panneau Sales : objectif, tâches, une tâche cochée (0/6 puis 1/6), +30 crédits qui rejoignent le compteur (330 puis 360), la salle passe de 0/17 à 1/17 et l’étage Business de 1 % à 2 %. |
| 5. Au quotidien | Mes objectifs du jour, les chantiers, les domaines à surveiller. | Compteurs du cockpit, pièces de Wealth qui clignotent en jaune, domaines à 0 % dans l’ascenseur. |
| 6. Ce que ça change | Je vois ce que je construis. Je joue au jeu de la vie. | L’immeuble entier et l’avancement de chaque étage, puis un seul mouvement de caméra jusqu’à Daouda en plan rapproché. |

Découpage complet (phrase, image, moment, mouvement, texte, transition) : **`voix-off/decoupage.md`**.

## La voix off

- Texte : `voix-off/script.json`. Le champ `texte` sert aux sous-titres, le champ `prononciation` à la synthèse vocale.
- La voix fournie est générée avec ElevenLabs (modèle v4, voix « Alexandre ») : `voix-off/prise-elevenlabs-v4.mp3` pour la prise complète, `voix-off/prise-elevenlabs-v4-L03.mp3` pour la phrase 3 réécrite ensuite. Une voix témoin (synthèse Pico, `bash outils/voix-temoin.sh`) reste disponible pour caler le montage hors ligne.
- **Pour une vraie voix** :
  - **Une prise complète** : les 19 phrases dans l’ordre, avec une pause nette entre chacune. Lancez `python3 outils/decouper-prise.py prise.mp3`.
  - **Phrase par phrase** : déposez `L01.wav` à `L19.wav` dans `public/voix/` et lancez `bash outils/mesurer-voix.sh`.

  Puis `npm run render`. Les silences sont rognés et le montage se recale seul sur vos durées.
- Musique facultative : `--props='{"voix":true,"sousTitres":true,"musique":"musique.mp3"}'` (fichier dans `public/`). Elle est automatiquement baissée sous la voix.

## Où modifier quoi

| Fichier | Contenu |
|---|---|
| `voix-off/script.json` | Les 19 phrases de la voix off. |
| `src/data.ts` | Sous-titres découpés pour l’écran, pastilles de l’étape 1, étages, zones des captures. |
| `src/voix.ts` | Calage sur la voix : pauses, durées minimales par phrase, tenue du plan final. |
| `src/timeline.ts` | Chorégraphie, accrochée aux phrases (`R.L09.debut`, `a('L11', 0.42)`…). |
| `src/components/` | `Cartes` (étapes 1-2), `Immeuble` (caméra et étages), `Ascenseur`, `Salle` et `Hud` (étape 4), `Cockpit` (étape 5), `PlanFinal` et `Avatar3D` (fin), `SousTitres`. |

## L’avatar

Daouda ne mesure que 140 px de haut sur les captures, trop peu pour un gros plan.
Il est donc reconstruit en 3D (`src/components/Avatar3D.tsx`) dans le style du jeu, avec les couleurs relevées sur la capture :
- tête ronde, peau `#90512c` ;
- cheveux et barbe noirs ;
- pull bleu à col roulé `#1756c7` ;
- pantalon et chaussures anthracite.

La caméra part du cadrage exact du jeu, puis l’avatar 3D prend le relais de la capture pendant le mouvement.
