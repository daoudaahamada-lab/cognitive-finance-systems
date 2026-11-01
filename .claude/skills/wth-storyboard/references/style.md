# Style de la série (jetons, zones, typographie)

Les valeurs viennent du code : `wth-videos/pipeline/story.py` (`STYLE`, durées `POP`… `STRETCH`),
`wth-videos/pipeline/qa.py` (zones contrôlées) et `wth-videos/motion/src/story/geometry.json`. **Si ce fichier et le
code divergent, le code gagne** : relire `STYLE` avant d'écrire une couleur, puis corriger ce fichier.

Un storyboard n'écrit que des jetons de cette page. Une couleur ou une taille hors de cette page est un nouvel accent :
c'est ce que le point 7 du brief interdit (« peu d'accents concurrents »).

## Couleurs (`STYLE`)

| Jeton | Hex | Emploi | Contraste sur ivoire |
|---|---|---|---|
| `bg` | `#F6F0E4` | fond ivoire, toujours | — |
| `grid` | `#ECE4D4`, pas 36 px, trait 2 px | quadrillage fixe, ancré en haut à gauche | — |
| `ink` | `#1E1416` | contours 4-5 px, textes, figurine « Toi », ombres dures | 15,9 : 1 |
| `cyan` | `#19B3C7` | l'accent unique, en aplat : objet du fil, cercle actif, pastilles, bouton ; toujours cerné d'encre, texte encre dessus | encre sur cyan 7,1 : 1 |
| `deep` | `#0A7487` | cyan profond pour les traits fins (fils, cadres, coches du conseiller, tampon) et le mot prononcé des sous-titres | 4,8 : 1 |
| `light` | `#D3F0F6` | fonds de pilules, barres de titre, jetons, surligneur | — |
| `paper` | `#FFFDF8` | documents, fiches, figurine papier (client), carte de fin | — |
| `grey` | `#DDD5C6` | ce qui n'est pas « nous » : cartes d'un autre client, pilule « IA grand public » | — |
| `red` | `#C8102E` | **seule couleur d'alerte**, rare : la chose fausse, le piège, le mot d'alerte des sous-titres | 5,2 : 1 |
| `slot` | `#F4EEE3` | fond des rangées d'une fiche | — |
| `rule` | `#E6DECF` | filet sous un en-tête | — |
| `ai_tick` | `#8E8887` | encre à ~50 % : coches et traits de l'IA, foule grand public | — |

Discipline :
- **Un seul accent : le cyan.** Ses trois tons (`cyan`, `deep`, `light`) suffisent pour tout ce qui est positif ou actif.
- **Rouge = alerte, et seulement là où le storyboard l'annonce** (dans `style`, avec ses scènes). Jamais sur un mur,
  un cadenas, un obstacle neutre ou l'IA. Les mots d'alerte des sous-titres (`ALERT_WORDS` de la mise en scène) le
  reprennent.
- **Gris = « pas nous » ou « éteint »**, jamais « refusé ». Une ligne grisée à 50 % se lit comme rejetée (leçon V01) :
  pour mettre en retrait, réduire, déplacer ou sortir l'élément plutôt que de le griser.

## Formes

- **Personnes et processus : plats, dessinés en code.** Aplat, contour encre de 4 à 5 px, coins de 14 à 18 px, ombre
  dure encre +6/+6 px sans flou, aucun dégradé ni lueur.
- **Objets et machine : PNG de verre** (carrousel de la vidéo et génériques). Alpha strict (le halo cuit pour fond noir
  disparaît), ombre douce de contact (flou 24 px, décalage 16 px, encre 16 % ; 22 % pour un objet blanc). Déplacés, mis
  à l'échelle, tournés ou masqués, jamais déformés. Un seul PNG entre ou sort à la fois.
- **Grammaire de trait** : pointillés = action de l'IA ; trait plein = preuve (fil vers un document) ou geste de « Toi ».

## Typographie (Inter, `font_family: "WTH Inter"`)

| Usage | Corps et graisse | Règle |
|---|---|---|
| Sous-titres karaoké (`STYLE.caption`) | Bold 64 px, une ligne, ligne de base y = 1350 | 2 à 3 mots (`max_words` 3 ; jusqu'à 4 par `CAPTION_GROUPS` de la mise en scène), largeur ≤ 760 px, mot prononcé en `deep`, mots d'alerte en `red`, coupe sèche. Gérés par le pipeline : le storyboard n'en dessine pas. |
| Texte qui doit être lu sur un objet | SemiBold ou Bold, 32 px conseillé, jamais moins de 26 px | lignes courtes : 22 caractères au plus ; une fiche ne descend pas sous l'échelle 0,85 tant qu'on doit la lire |
| Chiffres-clés, tampon, « ? », numéros du repère | ExtraBold | un chiffre-clé peut monter à ~2× le corps des sous-titres, en `cyan` ou `red`, sur le mot qui le dit |
| Légende du repère 1-2-3 | 26 px (`GEOM.MARKER.labelSize`) | un mot de 10 lettres au plus par étape |

Écriture française à l'écran : « 4 600 € » (espace fine insécable), « 3,5 % », « −40 % », « 9 h », dates en clair
(« sept. 2025 », jamais « 09/25 »), majuscules accentuées (« VALIDÉ »). La QA contrôle accents et orthographe des
textes affichés.

## Zones de l'image (1080 × 1920, `qa.py`)

| Zone | Valeurs | Pourquoi |
|---|---|---|
| Réservée en haut | y < 160 | bandeau de TikTok / Reels ; la QA refuse un pixel hors fond (tolérance 0,3 %) |
| Réservée en bas | y > 1540 (380 px du bas) | légende et boutons de la plateforme |
| Réservée à droite | x > 940 | colonne d'icônes |
| Sous-titres | ligne de base 1350 (bande 1280-1380) | la version sans sous-titres doit être identique au-dessus de y = 1270 |
| Action | y 250 → 1250, x 40 → 940 ; centre de composition vers y ≈ 760-800 | la bande d'action (160-1270) n'est jamais vide (QA) ; utiliser le bas jusqu'à y ≈ 1250 (ligne de sol vers y ≈ 1230) : sur V01, les 40 % du bas étaient vides |

Largeur d'une composition : 800 px au plus (au-delà, on entre dans la colonne de droite).

## Places fixes (lisibles sans texte)

- L'IA à gauche, « Toi » à droite (repos en bas à droite), le repère 1-2-3 en haut (y ≈ 300).
- L'objet du fil au centre de la composition, ou posé sur ce qui le contient.
- 1 à 4 éléments actifs par temps fort ; à taille téléphone, environ 8 formes au plus à l'écran. Ce qui n'agit plus
  sort de scène.

## Durées (images à 30 i/s, `story.py`)

| Constante | Images | ms | Profil |
|---|---|---|---|
| `POP` | 9 | 300 | apparition, échelle 0 → 1, ease-out cubique, sans rebond |
| `SCALE` | 10 | 330 | changement d'échelle, ease-out |
| `MORPH` | 11 | 350 | passage d'une composition à l'autre |
| `MOVE` | 16 | 550 | déplacement, ease-in-out (seul profil symétrique) |
| `DROP` | 11 | 370 | chute, ease-out, sans rebond |
| `TILT` | 14 | 450 | inclinaison, ease-out |
| `FADE` | 6 | 200 | fondu, réservé au texte et à l'interface |
| `DRAW` | 9 | 300 | trait ou fil tracé (250-450 ms) |
| `STRETCH` | 6 | 200 | étirement |

Un événement calé sur un mot est visible sur l'image même du mot (`LEAD = 1`). Détail du rythme : `motion-grammar.md`.
