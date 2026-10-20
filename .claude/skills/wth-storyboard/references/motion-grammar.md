# Grammaire du mouvement de la référence (mesurée)

Résumé de `reference_style.json` (même dossier) : mesures image par image de la vidéo de référence choisie par
l'utilisateur (165 s, créateur tiers, fond crème quadrillé, formes plates). Le dépôt est public : on garde les
mesures, jamais d'images de cette vidéo.

Lire ce résumé avant d'écrire un storyboard. Ouvrir le JSON seulement pour un chiffre précis (clé indiquée entre
crochets). Ses `recommendations_for_glass_version` visaient l'ancienne version sombre : ignorer leurs consignes de fond
noir et de couleurs, garder celles de rythme et de synchronisation.

## 1. Le principe : tenir, puis éclater

- **Rien ne bouge entre deux événements** [`idle_motion`]. 52 % des images sont identiques à la précédente ; des tenues
  de 2,2 s sont courantes. Ni flottement, ni respiration, ni parallaxe, ni caméra, ni zoom global ; le quadrillage ne
  bouge jamais.
- **Un événement est court** : de 0,17 à 0,70 s, médiane 0,37 s, attaque rapide (65 % des sursauts atteignent leur pic
  dans les 3 premières images), longue retombée.
- **La vie vient d'ailleurs** : un événement par seconde environ, chacun sur un mot ; le mot surligné des sous-titres
  saute toutes les 0,13 à 0,2 s ; quelques dérives narratives lentes et linéaires.
- **Dérive narrative** : un mouvement continu, à vitesse constante, qui illustre une durée ou un effort (la balle qui
  monte la pente pendant « ce ne sera pas facile », ~100 px/s à 1080). C'est la seule exception au « tenir » ; la
  réserver à une phrase qui la justifie (chercher, relire, monter, fondre).
- Notre garde-fou : la QA refuse toute image figée plus de 3,5 s (sauf la carte de fin). Prévoir un événement au moins
  toutes les 3 s.

## 2. Cadence [`visual_cadence`]

| Mesure | Référence (5 mots/s) | Pour nos voix (~2,5 mots/s, ~145 mots, ~57 s) |
|---|---|---|
| Nouvelle composition | médiane 1,3 s (p10 0,77, p90 3,7) ; ~1 par 9,5 mots | 15 à 20 compositions, une toutes les 2,5 à 3,5 s ; plus serré dans l'accroche (1 à 1,5 s) |
| Événement de mouvement | médiane 1,03 s ; ~1 par 7,5 mots | 20 au minimum, viser 50 à 55 (un par seconde) |
| Tenue explicative | 4 à 6 s parfois | jamais plus de 3 s sans événement (QA) |

`prep.py` imprime la cadence visée pour chaque vidéo.

## 3. Entrées et mouvements [`entrances`]

| Geste | Durée | Profil | Note |
|---|---|---|---|
| Apparition (petite forme) | 300 ms (`POP`) | échelle 0 → 1, ease-out cubique | jamais de rebond ni d'élastique |
| Changement d'échelle | 330 ms (`SCALE`) | ease-out | |
| Chute depuis le haut | 370 ms (`DROP`) | ease-out | sans rebond ni écrasement ; pour « arriver », « tomber » |
| Morph (réarrangement en la composition suivante) | 350 ms (`MORPH`) | ease-out, pièces décalées de 1 à 3 images | **la manière normale d'entrer** |
| Étirement / entrée latérale | 200 ms (`STRETCH`) | ease-out | une barre entre en s'élargissant |
| Déplacement d'un élément déjà là | 550 ms (`MOVE`) | **ease-in-out** | seul profil symétrique ; tout le reste est ease-out |
| Inclinaison | 450 ms (`TILT`) | ease-out | puis tenue |
| Fondu | 200 ms (`FADE`) | linéaire ou ease-out | **texte et interface seulement** ; une forme entre par apparition, pas par fondu |
| Machine à écrire | 1 caractère par image | par paliers | un curseur clignote ; le contenu s'efface en 0,2 s avant le changement |
| Fondu de couleur | 300 ms | ease-out | ex. un cercle devient carte en passant au blanc |

## 4. Passages d'une composition à l'autre [`transitions_between_visuals`]

- Aucune coupe sèche : chaque passage est un morph de 0,3 à 0,45 s.
- Les sortants se réduisent vers leur centre (ou en points) pendant que les entrants grandissent ou glissent, **dans
  les mêmes images**. La scène n'est jamais vide.
- **Ce qui porte le sens persiste et se déplace** au lieu de disparaître : le cercle-protagoniste de la référence
  survit à presque tous les passages. Chez nous, c'est l'objet du fil.
- Le passage démarre sur un début de mot (89 % à ±2 images), souvent un début de groupe de sous-titres (57 %).
- **Repère de chapitre** : sur « Numéro 2 », une rangée de cercles cernés dont le n-ième est agrandi (×1,6) et rempli
  d'accent, tenue 1 à 1,3 s, puis morph vers l'illustration du point. Chez nous : le repère 1-2-3 avec sa légende.

## 5. Synchronisation [`sync_rules`]

- Événement = image `round(début du mot × 30)`, sans avance ni retard. 83 des 107 départs tombent sur l'image même du
  mot surligné ; 92 % à ±2 images.
- **Synchronisation sémantique** : l'image change sur le mot qui la nomme. 33 cercles sur « 33 ans », 7 sur « 7
  choses », le « 5 » rouge sur « 5 euros ». Les nombres dits se comptent à l'écran.
- Les événements tombent sur des mots-clés, souvent au milieu d'un groupe de sous-titres, pas seulement aux changements
  de groupe.

## 6. Mise en page [`visual_layout`]

- Composition centrée en x (50 %) ; centre vertical médian à 41,8 % de la hauteur (y ≈ 800 à 1920).
- Largeur médiane 68 % (≈ 735 px), p90 81 % (≈ 875 px) : plafonner à 800 px chez nous (colonne de droite).
- Hauteur médiane 18 % (≈ 345 px), p90 32 % (≈ 620 px). La référence laisse ~160 px vides au-dessus des sous-titres ;
  nous descendons jusqu'à y ≈ 1250 (leçon V01 : le bas de l'image était vide).
- Symétrie : rangées de cercles, pyramides centrées, paires en miroir autour de x = 50 %.
- Tailles typiques à 1080 : petits cercles 47 à 56 px, cercle-protagoniste 113 à 150 px, grandes formes 245 à 395 px.
- Une forme peut traverser la bande des sous-titres en passant, jamais s'y poser.

## 7. Formes et fond [`background`, `other_details`]

- Papier crème quadrillé, 30 colonnes (36 px à 1080), traits 2 px à peine plus foncés, fixe, sans grain, vignette ni
  dégradé.
- Style néo-brutaliste : aplats, contour encre (5-6 px à 1080), ombre dure décalée (+7/+8 px), sans flou. Chez nous :
  contour 4-5 px, ombre +6/+6 (`style.md`).
- Vocabulaire petit et constant : cercles, carrés, triangles, un seul accent, un protagoniste récurrent.
- Métaphores jouées : la balle poussée en montée = « pas facile » ; les morceaux épars qui s'effondrent en pile =
  « tirer des leçons » ; la bascule = « injuste » ; une grille 3×3 qui se remplit = « on ne choisit pas ».
- Cartes typographiques rares : un grand chiffre en accent sur son mot ; une carte de message tapée lettre à lettre.

## 8. Sous-titres [`captions`] (gérés par le pipeline)

2 à 4 mots (mode 3), Inter Bold 64 px à 1080, une ligne, ligne de base y = 1350, karaoké (le mot prononcé change de
couleur à l'image exacte de son attaque), coupe sèche entre groupes, aucune boîte ni ombre, nombres en chiffres.

## 9. Carte de fin [`end_card`]

Le protagoniste grandit, devient une carte blanche (fondu de couleur 0,3 s), un bouton pilule « S'ABONNER » apparaît,
un pointeur entre en bas à droite, clique (le bouton s'enfonce dans son ombre ~3 images), puis tout reste immobile
jusqu'à la fin (~1,1 s après le dernier mot). Chez nous : `kit.outro` (voir `series-bible.md`).
