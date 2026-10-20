# Bible de la série : ce qui ne change pas d'un film à l'autre

Les 15 films doivent se reconnaître comme une seule série : même distribution, mêmes places, même manière d'agir,
même fin. Un spectateur qui a vu V01 doit savoir, sans texte, qui est « Toi » et qui est l'IA dans V09. Ce qui varie :
le sujet, l'objet du fil et les métaphores.

## 1. Structure commune des scripts

Chaque script de `scripts/scripts.json` a les mêmes segments (`prep.py` les minute) :

| Segment | Rôle | Ce que la mise en scène fait toujours |
|---|---|---|
| `accroche` (≈ 0-3 s) | question ou affirmation choc | l'objet du fil est à l'écran **dès l'image 0** dans un état lisible ; un seul geste, pas d'ouverture surchargée (leçon V01) |
| `contexte` | le problème | on voit le problème agir sur l'objet du fil (il se disperse, fond, se bloque…) |
| `point1`, `point2`, `point3` | les 3 étapes, pièges ou erreurs (parfois 4) | le repère 1-2-3 légendé passe à l'étape sur « Première / Deuxième / Dernière… » ; chaque point transforme l'objet du fil |
| `chute` | la leçon, souvent un Avant / Après | comparaison visuelle avec l'état de l'accroche (même objet, deux états), pas un nouveau décor |
| `cta` | « Abonne-toi pour comprendre ton argent. » (identique sur les 15) | **dernière scène, à elle seule** : fin standard `kit.outro`, l'objet du fil devient le bouton « S’abonner », puis plus rien ne bouge (la QA ne dispense que la dernière scène du contrôle d'image figée) |

## 2. Distribution récurrente

| Rôle | Aspect et entité | Règles |
|---|---|---|
| **« Toi »** | figurine pleine encre (`Figure`, `variant="ink"` : tête ronde, buste trapèze, bras à longueur fixe, stylo) | Le conseiller dans les films pour CGP (V01, V05, V11 : le script parle de « ton client », « ton dossier »), le spectateur ailleurs. **Seule à tenir des outils** (stylo, tampon, curseur) et seule à décider. Repos en bas à droite. Ses gestes partent de sa main : le stylo déclenche ce qu'il touche (la cause est visible). Porte l'étiquette « Toi » si une étiquette est nécessaire, jamais l'IA. |
| **Autre personne** (client, banque, vendeur…) | figurine papier (`Figure`, `variant="paper"`, `tool=False`) : contour encre, intérieur blanc, ni visage ni bras | Apparaît sur le mot qui la nomme et **reste assez longtemps pour être identifiée** (≥ 1,5 s), tournée vers « Toi », face à face, avec ≥ 120 px d'écart. Jamais d'outil. |
| **L'IA** | `AI.png` (tête de céramique, cerveau en cube de verre), pilule « IA » | Agit **seulement en pointillés** : faisceaux `wire` pointillés, coches `tick` `variant="ai"` (pointillés dans un carré tireté : la forme, pas seulement la couleur, la distingue de « Toi »). Toujours à gauche. **Reste immobile quand elle se trompe** (pas de faisceau, pas de réaction) : elle ne « signale » pas ses erreurs. Sa sortie ne doit pas se lire « l'humain remplace l'IA » : elle se range (badge, coin), elle ne disparaît pas sous l'action de « Toi ». |
| **IA grand public** (si le script l'oppose à l'outil autorisé) | second `AI.png` + pilule grise « IA grand public » + `crowd` grise reliée par des traits | Dehors, de l'autre côté d'un mur ou d'un cadre ; jamais en rouge. |
| **Objet du fil** | le plus souvent la pastille cyan (`pill`), parfois un disque-protagoniste (`shape` cercle cyan) | Le protagoniste de la référence. Toujours posé sur ce qui contient le sujet suivi (dossier, compte, épargne…), présent dans presque toutes les scènes, déplacé plutôt que remplacé. Devient le bouton « S’abonner » de la carte de fin. Déclaré dans `objet_fil`. |
| **Repère 1-2-3** | `kit.steps_marker(labels)` en haut (y ≈ 300) | **Toujours avec une légende** : un mot par étape (≤ 10 lettres : « Limiter », « Exiger », « Relire »). Sans légende, « 1-2-3 » ne dit rien (leçon V01). Le disque actif glisse sur le mot « Première / Deuxième / Dernière ». |
| **Carte de fin** | `kit.outro` : carte, titre « WealthTech Horizon », ligne « Comprendre ton argent », bouton « S’abonner » | Même déroulé sur les 15 : morph vers la carte, bouton, pointeur, clic, puis immobile jusqu'à la dernière image. |

Couleurs, tailles et zones : `style.md`. Verbes visuels et entités : `visual-verbs.md`.

## 3. Règles de rôle (la confusion la plus coûteuse sur V01)

- **Ce que fait l'IA** : lire, extraire, ranger, rédiger, cocher en pointillés. **Ce que fait « Toi »** : délimiter,
  exiger, relier à une preuve, relire, barrer, corriger, tamponner, décider, demander.
- **La preuve avant le verdict.** On montre d'abord pourquoi c'est faux (rien ne la porte, la case est vide), puis le
  verdict (rouge, fissure), et le verdict est déclenché par « Toi » (le stylo touche, la ligne casse).
- **Jamais de validation avec une question ouverte.** Si une information reste à confirmer, elle porte « à poser au
  RDV » (ou l'équivalent du film) et le tampon dit ce qui est vrai (« PRÊT POUR LE RDV »), pas « VALIDÉ ».
- Un partage IA / humain se montre sans exclure l'IA : elle apporte, il porte le poids (V01 : la planche à bascule).

## 4. Illustrations (PNG)

Règle de la série, appliquée par le code (`Story.png` refuse sinon) : **le carrousel de la vidéo** (`WTH-<source>-xx`,
`source` dans `scripts.json`) **et les 20 génériques**, jamais l'image d'un autre épisode.

| Carrousel présent localement | Vidéos |
|---|---|
| WTH-003 (01-09) | V01 |
| WTH-002 (01-09) | V02 |
| WTH-006 (02-08) | V04 |
| WTH-004 (01-09) | V08 |
| aucun : génériques et code seulement | V03, V05, V06, V07, V09 à V15 |

`prep.py` donne la liste réelle et une planche (`build/Vxx/storyboard/pngs.jpg`). Absents : `data/illustrations_manifest.tsv`
donne l'identifiant Drive (téléchargement : skill `wth-video`).

Les 20 génériques : AI (tête de céramique au cerveau de verre), BELL (sonnette de comptoir), BOOK (livre ouvert), BUOY
(bouée), CRADLE (berceau), CRYSTAL (boule de cristal), FINGERPRINT (empreinte sur socle), GEAR (machine à engrenages),
GLOBE, HEART (cœur dans une main), PRINTER (imprimante), RINGS (alliances sur coussin), SHOES (baskets), SUITCASE
(valise), TAG (étiquette), TARGET (cible et flèche), TOKEN (jeton à maison), TREE (arbre aux racines dans un cube), TRUCK
(camion de déménagement), WAVE (vague).

Emploi :
- Un PNG est **un lieu ou un objet** qui reçoit ou émet des éléments dessinés en code (l'horloge reçoit un secteur de
  10 minutes ; la bulle reçoit un « ? »). Jamais un zoom qui raconte, jamais un diaporama.
- Un PNG qui fait lire autre chose que voulu est retiré (V01 : le coffre lu « archivage », le globe lu « internet »).
- Un seul PNG entre ou sort à la fois ; jamais déformé.
- Peu de PNG par film : 3 à 6 suffisent. Les films sans carrousel sont presque entièrement en code : c'est la norme de
  la référence, pas un manque.

## 5. Contenu affiché

- Textes courts, en français correct, accents compris (la QA lit les textes des entités) ; 22 caractères au plus par
  ligne d'objet.
- Nombres : ceux du script, écrits comme lui (« 4 600 € », « 1 % »), comptés à l'écran quand ils sont dits (un compteur
  qui monte, n jetons pour « n »).
- Dates en clair : « sept. 2025 », « mars 2026 ».
- Exemples plausibles pour un CGP ou un particulier français ; vocabulaire réglementaire exact (RGPD, ACPR, REGAFI,
  DIC, adéquation) ; aucun conseil personnalisé implicite.
