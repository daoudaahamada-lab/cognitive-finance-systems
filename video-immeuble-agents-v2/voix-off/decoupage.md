# Voix off et découpage, phrase par phrase

Durée totale : 1 min 25 s. Les timecodes viennent de la voix témoin actuelle (`public/voix/durees.json`).
Avec une autre voix, tout se recale automatiquement : chaque plan est accroché au début, à un moment précis ou à la fin de sa phrase (voir `src/timeline.ts`).

Colonnes : **Début / fin voix** = premier et dernier mot. **Image** = ce qu’on voit. **Mouvement** = animation. **À l’écran** = texte affiché en plus des sous-titres. **Transition** = moment où le plan suivant commence.

## 1. Le point de départ

| # | Voix off | Début / fin voix | Image | Mouvement | À l’écran | Transition |
|---|---|---|---|---|---|---|
| L01 | J’ai toujours plusieurs projets en même temps. | 0:01.0 / 0:03.7 | Les vraies salles du jeu, en pastilles éparpillées : Salle de sport, Cuisine, Chambre, Architect, Build, Studio Marketing, Sales, Finance, Hall Inbox, Labo d’apps, Bureau carrière, Archives. | Apparition une à une à partir de 0:00.3, léger flottement. | Les compteurs réels de chaque salle (« 1 proj. · 0/17 »…). | Enchaîne sur place. |
| L02 | Ma santé, mon argent, mon business, mes idées. | 0:04.2 / 0:08.4 | Mêmes pastilles. | Sur chaque mot, les pastilles du domaine nommé passent au bleu (Health, Wealth, Business, puis l’Inbox et le labo pour « mes idées »). | | Enchaîne sur place. |
| L03 | Tout avance en parallèle… mais je ne savais jamais vraiment où j’en étais, ni où mettre mon énergie. | 0:08.7 / 0:15.2 | Mêmes pastilles. | Le flottement s’emballe : les pastilles se croisent, certaines se brouillent. On ne sait plus où regarder. | | Les pastilles partent vers le centre au milieu de L04. |

## 2. L’idée

| # | Voix off | Début / fin voix | Image | Mouvement | À l’écran | Transition |
|---|---|---|---|---|---|---|
| L04 | Alors j’ai imaginé ma vie comme un immeuble. | 0:16.1 / 0:19.6 | L’immeuble en vue éclatée, 5 étages. | À partir de « immeuble », chaque pastille s’envole vers son étage, qui se pose dessous (du sous-sol au dernier étage). | | Enchaîne sur place. |
| L05 | Un immeuble que je construis, étage par étage. | 0:20.6 / 0:24.1 | L’immeuble complet. | Lente poussée de caméra. | | Glissement latéral au début de L06. |

## 3. L’organisation

| # | Voix off | Début / fin voix | Image | Mouvement | À l’écran | Transition |
|---|---|---|---|---|---|---|
| L06 | Chaque étage, c’est un domaine de ma vie. | 0:25.0 / 0:28.0 | L’immeuble, décalé à gauche. | Les noms des étages apparaissent un à un. | 3 Health, 2 Wealth, 1 Business, RDC SMART, S1 Life | Plongée vers Health au début de L07. |
| L07 | Et chacun est piloté par son propre agent IA. | 0:28.5 / 0:32.3 | Étage Health + carte Ascenseur du jeu. | Plongée de la caméra, la carte monte. Sur « agent IA », les points « agent en service » pulsent. | Légende « Agent en service » | L’ascenseur descend au début de L08. |
| L08 | À l’intérieur, chaque salle abrite un sous-agent, avec une mission précise. | 0:32.7 / 0:37.9 | Descente Health, Wealth, Business, puis la salle Sales. | Deux trajets d’ascenseur, zoom dans la salle, anneau bleu sur Sales. | Pastille « Sous-agent » | Le panneau de la salle s’ouvre juste avant L09. |

## 4. La mécanique

| # | Voix off | Début / fin voix | Image | Mouvement | À l’écran | Transition |
|---|---|---|---|---|---|---|
| L09 | Mes projets ont un objectif. | 0:39.7 / 0:42.1 | Panneau Sales (capture 07) sous la salle. | Le panneau monte. Le bloc projet est encadré sur « objectif ». | « Objectif » sur « Signer 1 pilote Agentic Wealth payant » | Enchaîne sur place. |
| L10 | Et chaque objectif se découpe en tâches concrètes. | 0:42.9 / 0:46.2 | Même panneau. | Léger défilement, la liste des tâches est encadrée sur « tâches ». | « Tâches » | Enchaîne sur place. |
| L11 | Chaque fois que j’en valide une, je gagne des crédits. | 0:46.6 / 0:50.0 | Panneau + barre du QG (niveau, XP, crédits). | La barre du QG descend. Sur « valide », la première tâche est cochée. Le gain « +30 crédits » de la tâche s’envole vers le compteur, qui passe de 330 à 360. | « +30 crédits » | Le panneau redescend au début de L12. |
| L12 | Et ces crédits font avancer la construction. | 0:51.5 / 0:54.4 | Salle Sales, puis tout l’étage Business. | La salle passe de 0/17 à 1/17, puis la caméra recule sur l’étage. La barre de niveau du QG progresse. | | La carte du cockpit monte avant L13. |

## 5. Le suivi

| # | Voix off | Début / fin voix | Image | Mouvement | À l’écran | Transition |
|---|---|---|---|---|---|---|
| L13 | Chaque jour, je suis mes objectifs. | 0:56.2 / 0:59.3 | Cockpit « Aujourd’hui », recréé d’après la capture mobile. | Les + sont touchés : contacts 4/4, commentaires 5/5, post 1/1, moteur du jour 3/3. | Les compteurs | La carte s’efface vers le haut, l’étage Wealth remonte. |
| L14 | Je vois les chantiers en cours… | 1:01.5 / 1:03.6 | Étage Wealth, en travaux. | Architect, Build puis Run clignotent en jaune, puis toutes ensemble. | Noms des pièces | Enchaîne sur place. |
| L15 | …et les domaines qui ont besoin de plus d’attention. | 1:04.8 / 1:07.7 | L’étage remonte, la carte Ascenseur revient. | Wealth et Life (0 %) s’allument en jaune dans l’ascenseur. | Légende « En travaux », pourcentages | Recul vers l’immeuble au début de L16. |

## 6. Le sens

| # | Voix off | Début / fin voix | Image | Mouvement | À l’écran | Transition |
|---|---|---|---|---|---|---|
| L16 | Je ne gère plus seulement des tâches. | 1:09.0 / 1:11.4 | L’immeuble entier. | Grand recul : les étages se rassemblent. | | Enchaîne sur place. |
| L17 | Je vois ce que je construis. Et je sais où j’en suis. | 1:12.1 / 1:16.0 | L’immeuble entier. | L’avancement de chaque domaine apparaît étage par étage. | Health 44 %, Wealth 0 %, Business 1 %, SMART 29 %, Life 0 % | La caméra part vers le rez-de-chaussée au début de L18. |
| L18 | Je joue au jeu de la vie. | 1:16.4 / 1:18.1 | Du haut de l’immeuble vers le RDC. | Approche continue vers Daouda, dans le Hall Inbox. | | Sans coupe. |
| L19 | Et chaque action me rapproche de l’immeuble que je veux construire. | 1:18.7 / 1:22.4 | Daouda en plan rapproché, l’immeuble en arrière-plan, flou. | Sur « action », l’avatar 3D prend le relais de la capture. La caméra passe de la vue du jeu à un plan de trois quarts légèrement en contre-plongée, pendant que l’immeuble recule et se floute derrière lui. Le mouvement se termine sur « construire ». | Étiquette « Daouda », comme dans le jeu | Tenue de 3 s sur le personnage, sans texte. |

## Enregistrer votre propre voix

1. Enregistrez chaque phrase dans un fichier séparé : `L01.wav` à `L19.wav` (texte exact dans `voix-off/script.json`).
2. Déposez-les dans `public/voix/` (à la place de la voix témoin).
3. Lancez `bash outils/mesurer-voix.sh`, puis `npm run render`.

Le montage se recale sur vos durées. Si une phrase est plus courte que l’animation qu’elle accompagne, l’image garde le temps nécessaire (durées minimales dans `src/voix.ts`).
