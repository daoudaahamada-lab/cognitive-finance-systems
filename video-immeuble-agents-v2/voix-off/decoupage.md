# Voix off et découpage, phrase par phrase

Durée totale : 1 min 12 s. Les timecodes viennent de la voix témoin actuelle (`public/voix/durees.json`, fichiers rognés sans silence).
Avec une autre voix, tout se recale automatiquement : chaque plan est accroché au début, à un moment précis ou à la fin de sa phrase (voir `src/timeline.ts`).

Colonnes :
- **Début / fin voix** : premier et dernier mot.
- **Image** : ce qu’on voit.
- **Mouvement** : l’animation.
- **À l’écran** : le texte affiché en plus des sous-titres.
- **Transition** : le moment où le plan suivant commence.

Un surtitre bleu discret nomme l’étape en cours (Le point de départ, L’idée, L’organisation, Le jeu, Au quotidien, Ce que ça change). Il disparaît pendant le plan final.

## 1. Le point de départ

| # | Voix off | Début / fin voix | Image | Mouvement | À l’écran | Transition |
|---|---|---|---|---|---|---|
| L01 | J’ai toujours plusieurs projets en même temps. | 0:01.0 / 0:03.2 | Les vraies salles du jeu en pastilles éparpillées (Salle de sport, Cuisine, Chambre, Architect, Build, Studio Marketing, Sales, Finance, Hall Inbox, Labo d’apps, Bureau carrière, Archives). | Apparition une à une à partir de 0:00.3, léger flottement. | Les compteurs réels de chaque salle (« 1 proj. · 0/17 »…). | Sur place. |
| L02 | Ma santé, mon argent, mon business, mes idées. | 0:03.9 / 0:07.5 | Mêmes pastilles. | Sur chaque mot, les pastilles du domaine nommé s’allument en bleu (Health, Wealth, Business, puis l’Inbox, le labo et la carrière pour « mes idées »). | | Sur place. |
| L03 | Tout avançait en parallèle… mais je ne savais jamais vraiment où j’en étais, ni où mettre mon énergie. | 0:07.8 / 0:13.6 | Mêmes pastilles. | Le flottement s’emballe : les pastilles se croisent, certaines se brouillent. | | Les pastilles partent vers l’immeuble pendant L04. |

## 2. L’idée

| # | Voix off | Début / fin voix | Image | Mouvement | À l’écran | Transition |
|---|---|---|---|---|---|---|
| L04 | Alors j’ai imaginé ma vie comme un immeuble. | 0:14.3 / 0:17.2 | Le sous-sol se pose sur « immeuble ». | Chaque pastille s’envole vers son étage au moment où il se pose. | | Sur place. |
| L05 | Un immeuble que je construis, étage par étage. | 0:17.5 / 0:20.4 | L’immeuble se construit. | Les étages se posent un à un, Health en dernier sur « étage par étage ». | | Glissement latéral au début de L06. |

## 3. L’organisation

| # | Voix off | Début / fin voix | Image | Mouvement | À l’écran | Transition |
|---|---|---|---|---|---|---|
| L06 | Chaque étage, c’est un domaine de ma vie. | 0:21.6 / 0:24.1 | L’immeuble, décalé à gauche. | Les noms des étages apparaissent un à un. | 3 Health, 2 Wealth, 1 Business, RDC SMART, S1 Life | Plongée vers Health au début de L07. |
| L07 | Et chacun est piloté par son propre agent IA. | 0:24.7 / 0:27.9 | Étage Health + carte Ascenseur du jeu. | Plongée de la caméra, la carte monte. Sur « agent IA », chaque étage reçoit sa pastille « Agent IA », l’un après l’autre. | « Un agent IA par étage » | L’ascenseur descend au début de L08. |
| L08 | À l’intérieur, chaque salle a son sous-agent, avec une mission précise. | 0:28.3 / 0:32.8 | Descente rapide jusqu’au 1er, zoom dans la salle Sales, puis son panneau. | Anneau bleu et pastille « Sous-agent » sur « sous-agent ». Le panneau s’ouvre, son agent en service est encadré sur « mission précise ». | « Sous-agent », « Sa mission » | Sur place. |

## 4. Le jeu

| # | Voix off | Début / fin voix | Image | Mouvement | À l’écran | Transition |
|---|---|---|---|---|---|---|
| L09 | Mes projets ont un objectif. | 0:34.0 / 0:35.7 | Panneau Sales (capture 07). | Le projet est encadré sur « objectif ». | « Objectif » sur « Signer 1 pilote Agentic Wealth payant » | Sur place. |
| L10 | Et cet objectif se découpe en tâches concrètes. | 0:36.9 / 0:39.4 | Même panneau. | Léger défilement, les tâches sont encadrées sur « tâches ». | « Tâches » | Sur place. |
| L11 | Quand j’en valide une, je gagne des crédits. | 0:40.1 / 0:42.5 | Panneau + barre du QG (niveau, XP, crédits). | La barre du QG apparaît. Sur « valide », la première tâche est cochée et « Arsenal de prospection » passe de 0/6 à 1/6. Les « +30 crédits » de la tâche s’envolent vers le compteur, qui passe de 330 à 360. | « +30 crédits » | Le panneau redescend juste après la phrase. |
| L12 | Et ces crédits font avancer la construction. | 0:43.4 / 0:45.8 | Salle Sales, puis tout l’étage Business. | La salle passe de 0/17 à 1/17, la caméra recule sur l’étage. La carte de l’étage passe de 1 % à 2 %. | « Business 1 % → 2 % », « Sales : 1 tâche faite sur 17 » | La carte du cockpit monte avant L13. |

## 5. Au quotidien

| # | Voix off | Début / fin voix | Image | Mouvement | À l’écran | Transition |
|---|---|---|---|---|---|---|
| L13 | Au quotidien, je garde un œil sur mes objectifs du jour, | 0:47.4 / 0:50.8 | Cockpit « Aujourd’hui », recréé d’après la capture mobile. | Les + sont touchés : contacts 4/4, commentaires 5/5, post 1/1, moteur du jour 3/3. | Les compteurs | Fondu enchaîné vers l’étage Wealth. |
| L14 | sur les chantiers en cours… | 0:51.3 / 0:52.6 | Étage Wealth, en travaux. | Architect, Build puis Run clignotent en jaune, puis toutes ensemble. | Noms des pièces | Sur place. |
| L15 | et sur les domaines qui demandent plus d’attention. | 0:53.8 / 0:56.1 | L’étage remonte, la carte Ascenseur revient. | Wealth et Life (0 %) s’allument en jaune. | « En travaux », avancement par étage | Recul vers l’immeuble au début de L16. |

## 6. Ce que ça change

| # | Voix off | Début / fin voix | Image | Mouvement | À l’écran | Transition |
|---|---|---|---|---|---|---|
| L16 | Je ne gère plus seulement des tâches. | 0:57.3 / 0:59.0 | L’immeuble entier, centré. | Grand recul : les étages se rassemblent. | | Sur place. |
| L17 | Je vois ce que je construis. Et je sais où j’en suis. | 0:59.9 / 1:03.3 | L’immeuble entier. | Il glisse à gauche, l’avancement de chaque domaine apparaît. | Health 44 %, Wealth 0 %, Business 2 %, SMART 29 %, Life 0 % | La caméra part au début de L18. |
| L18 | Je joue au jeu de la vie. | 1:03.6 / 1:04.7 | Plan final, début du mouvement. | Un seul mouvement continu commence : descente vers le rez-de-chaussée dans l’immeuble entier. | | Sans coupe. |
| L19 | Et chaque action me rapproche de l’immeuble que je veux construire. | 1:05.4 / 1:08.6 | Daouda, puis Daouda en plan rapproché, l’immeuble flou derrière lui. | Le mouvement plonge sur Daouda dans le Hall Inbox. Vers « action », l’avatar 3D prend le relais de la capture sans ralentir. L’immeuble recule et se floute en arrière-plan. Le mouvement se pose sur « construire ». | Étiquette « Daouda », comme dans le jeu | Tenue de 3 s sur le personnage, sans texte ni surtitre. |

## Enregistrer votre propre voix

Deux possibilités :

- **Une prise complète** (par exemple depuis ElevenLabs) : dites les 19 phrases dans l’ordre, avec une pause nette entre chacune, puis lancez `python3 outils/decouper-prise.py prise.mp3`. L’outil coupe aux 18 plus longues pauses et écrit `public/voix/L01.wav` à `L19.wav`.
- **Phrase par phrase** : enregistrez `L01.wav` à `L19.wav` dans `public/voix/`, puis lancez `bash outils/mesurer-voix.sh`.

Ensuite, `npm run render`. Le montage se recale sur vos durées (silences rognés automatiquement). Si une phrase est plus courte que l’animation qu’elle accompagne, l’image garde le temps nécessaire (durées minimales dans `src/voix.ts`).
