# Vidéo « J’ai mis ma vie dans un immeuble d’agents »

Motion design vertical **1080 x 1920, 30 i/s, 40,5 s**, construit avec [Remotion](https://www.remotion.dev) (React).
Tout est en code : textes, minutage, caméra, surbrillances. L’export MP4 se fait en une commande.

## Démarrer

Prérequis : Node.js 18 ou plus récent.

**Déposez d’abord les 13 captures dans `public/captures/`**, avec les noms du tableau « Captures » plus bas.
Elles ne sont pas versionnées (le dépôt est public) et le rendu échoue sans elles.

```bash
npm install
npm run studio      # aperçu interactif dans le navigateur (timeline, lecture image par image)
npm run render      # export MP4 -> out/immeuble-agents.mp4
```

Le premier rendu télécharge automatiquement le navigateur de rendu de Remotion.
Les polices (Inter, JetBrains Mono, licence SIL OFL) sont embarquées dans `public/fonts` : hormis ce téléchargement initial, aucun accès réseau n’est nécessaire.

Export H.264, `yuv420p`, BT.709, CRF 16 : le fichier se lit partout (LinkedIn, Instagram, TikTok, iPhone).

### Ajouter une musique

Déposez un fichier dans `public/` (par exemple `public/musique.mp3`), puis :

```bash
npx remotion render ImmeubleAgents out/immeuble-agents.mp4 --props='{"musique":"musique.mp3"}'
```

Sous Windows, mettez plutôt `{"musique":"musique.mp3"}` dans un fichier `props.json` à la racine du projet et lancez
`npx remotion render ImmeubleAgents out/immeuble-agents.mp4 --props=props.json`.

Le son monte en 0,5 s au début et redescend sur la dernière seconde et demie.

## Déroulé

| Temps | Scène | Captures | Ce qui se passe |
|---|---|---|---|
| 0 à 3 s | Accroche | | « J’ai mis ma vie dans un immeuble d’agents. » en très gros, trait bleu sous « d’agents ». |
| 3 à 6 s | L’immeuble apparaît | 02 à 06 | Les 5 étages se posent l’un sur l’autre, du sous-sol au dernier étage. Légende : « Chaque étage est un agent. » |
| 6 à 12,3 s | Descente en ascenseur | 02 à 06 | La caméra plonge sur Health puis descend étage par étage. La carte Ascenseur suit la caméra. |
| 12,3 à 18,5 s | Une salle s’ouvre | 04, 07 | Remontée au 1er, zoom sur la salle Sales, son panneau s’ouvre : sous-agent, projet, tâches. |
| 18,5 à 25 s | Le chantier | 03, 08 | Le panneau « Ce qui est en travaux » descend jusqu’à Wealth, puis chaque pièce clignote en jaune en même temps que son badge. |
| 25 à 34,5 s | Le cockpit | 10, 09 | Aperçu des écrans Projets puis Aujourd’hui, puis les compteurs du jour montent (+1, +1, +1) jusqu’à 3/3 objectifs. |
| 34,5 à 40,5 s | Fin | 12 | La carte du cockpit se replie en téléphone (version mobile), puis « Mon système tourne. Moi, je prospecte. » |

## Où modifier quoi

| Fichier | Contenu |
|---|---|
| `src/data.ts` | **Tous les textes** (accroche, légendes, phrase de chute), les étages (nom, description, %, statut), les fichiers de captures, les zones à surligner. |
| `src/timeline.ts` | Le minutage de chaque scène, en images (30 images = 1 s). Les arrêts de l’ascenseur, les « + » du cockpit, etc. |
| `src/theme.ts` | Couleurs (accent bleu `#2f6bff`, fond, cockpit sombre) et polices. |
| `src/components/` | Une scène par fichier : `Accroche`, `Immeuble` (caméra et étages), `Ascenseur`, `Salle`, `Chantier`, `Cockpit`, `Fin`. |

Le rez-de-chaussée s’appelle **SMART** dans la vidéo, comme dans le brief, alors que l’application affiche encore « Main ».
Changez `nom` dans `ETAGES` si besoin. Sur la capture mobile 12, l’onglet « Main » est recouvert par « SMART » : réglez `ONGLET_RDC_MOBILE.actif` dans `src/data.ts` pour garder la capture telle quelle.

Pour garder la règle « pas de tiret cadratin », utilisez des virgules, deux-points ou le point médian `·` dans les textes.

## Captures

Les captures vont dans `public/captures/` (non versionnées, voir `public/captures/LISEZMOI.md`), renommées par rôle :

| Fichier | Contenu |
|---|---|
| `01-qg-vue-generale.png` | QG, rez-de-chaussée (non utilisée, doublon de 05) |
| `02-etage-health.png` | Étage 3, Health |
| `03-etage-wealth.png` | Étage 2, Wealth |
| `04-etage-business.png` | Étage 1, Business |
| `05-etage-rdc.png` | Rez-de-chaussée |
| `06-etage-life.png` | Sous-sol, Life |
| `07-salle-sales.png` | Salle Sales ouverte (panneau projets et tâches) |
| `08-travaux.png` | Panneau « Ce qui est en travaux » |
| `09-cockpit-aujourdhui.png` | Cockpit, onglet Aujourd’hui |
| `10-cockpit-projets.png` | Cockpit, onglet Projets |
| `11-cockpit-atelier.png` | Cockpit, onglet Atelier (non utilisée) |
| `12-mobile-qg.png` | QG sur mobile |
| `13-mobile-cockpit.png` | Cockpit sur mobile (référence du cockpit recréé en vectoriel) |

Les étages sont découpés selon la silhouette de l’immeuble (`POLY_ETAGE` dans `src/data.ts`) : si vous remplacez une capture d’étage, gardez le même cadrage (3200 x 1800, même zoom) pour que la découpe tombe juste.

Les compteurs du cockpit sont recréés en vectoriel (d’après la capture mobile 13) pour pouvoir animer les chiffres : modifiez les instants des « + » dans `COCKPIT` (`src/timeline.ts`).
