# Le brief de l'utilisateur (mot pour mot)

Ce fichier est la source de vérité de la méthode Story. Les 7 règles et le critère ci-dessous sont les mots de
l'utilisateur : ne pas les reformuler dans un storyboard, y répondre point par point (champ `angle`, section « Parti pris
et réponse aux 7 corrections » du `.md`).

## Contexte

- Le premier remake de V01 (illustrations de verre sur fond noir, apparaissant l'une après l'autre avec zooms, fondus
  et étiquettes) a été refusé. Le verdict ci-dessous est la réponse de l'utilisateur à ce rendu.
- L'utilisateur a ensuite validé, le 20/10/2026, l'extrait de V01 mis en scène avec la méthode Story (scènes S11 à S14,
  15,7 s, `output/extraits/WTH-V01_extrait_S11-S14.mp4`) : « C'est absolument parfait ».
- Puis il a demandé : « Créer un skills qui permet de répéter la méthodologie pour créer les vidéo similairement », et
  les 15 vidéos avec cette méthode.

## Le verdict (copie exacte)

> Dans la référence de 2 min 45, les éléments graphiques interagissent pour expliquer les idées : ils rencontrent des
> obstacles, se rapprochent, se séparent, se transforment. Le mouvement porte une partie du message.
> Dans ton rendu, les illustrations apparaissent surtout à la suite les unes des autres, avec des zooms, des fondus et
> des étiquettes. Je veux davantage de démonstration visuelle et une continuité entre les scènes.
> 1. Construis un fil conducteur : nous suivons le même dossier client, depuis les informations dispersées jusqu’à la
>    fiche vérifiée utilisée en rendez-vous.
> 2. Pour chaque scène, définis un état initial, une action visible et un résultat. Par exemple : plusieurs documents
>    entrent dans un outil autorisé ; des informations en sont extraites ; elles se regroupent dans une fiche.
> 3. Illustre le sens complet des phrases. Pour « une réponse fluide peut être fausse », montre une réponse convaincante
>    dont une affirmation devient suspecte. Pour « chaque ligne doit renvoyer à un document », relie réellement une
>    ligne de la fiche à sa source.
> 4. Distingue clairement l’IA et le conseiller. Le robot ne doit pas porter l’étiquette « Toi ». Montre le conseiller
>    qui relit, corrige et décide.
> 5. Fais évoluer les mêmes éléments entre les scènes : un document devient une source, une information devient une
>    ligne de synthèse, une ligne non vérifiée devient une question pour le client.
> 6. Utilise les PNG fournis lorsqu’ils servent cette mise en scène. Crée des éléments séparés pour les actions qui
>    nécessitent une véritable animation. Un zoom sur un PNG ne suffit pas à représenter un processus.
> 7. Recherche la simplicité visuelle de la référence, en conservant l’identité WealthTech Horizon : fond clair ivoire,
>    cyan, typographie lisible et peu d’accents concurrents.
>
> Critère de réussite : en masquant les sous-titres, je dois pouvoir comprendre l’action principale et percevoir ce qui
> change.

## Lecture pour n'importe quelle vidéo de la série

Les exemples du verdict parlent de V01. La règle derrière chaque point vaut pour les 15 films :

| Point | Règle générale | Ce que le storyboard doit contenir |
|---|---|---|
| 1. Fil conducteur | Un seul objet, ou un seul personnage, est suivi du début à la fin : on voit son état initial dans l'accroche et son état final dans la chute. | `thread`, `objet_fil`, et l'objet du fil dans les `elements` de presque toutes les scènes. |
| 2. État initial / action visible / résultat | Chaque scène part du résultat de la précédente, déclenche une action sur un mot et finit sur un résultat qu'on voit. | `etat_initial`, `action`, `resultat`, `transition` et des `beats` calés sur des débuts de mots. |
| 3. Le sens complet | La phrase entière est jouée, y compris sa nuance (« peut être fausse », « sans source », « net de frais ») : pas seulement son mot-clé. | Une action qui montre la nuance (une affirmation qui devient suspecte, un fil réellement tiré vers sa source, une jauge qui fond). |
| 4. L'IA ≠ le conseiller / « Toi » | Les rôles se lisent sans texte : forme, place, manière d'agir. La figurine encre « Toi » est seule à tenir les outils et à décider ; l'IA n'agit qu'en pointillés. | Distribution conforme à `series-bible.md` ; jamais l'étiquette « Toi » sur l'IA. |
| 5. Les mêmes éléments évoluent | Un élément change de rôle au lieu d'être remplacé : document → source, information → ligne, ligne non vérifiée → question. | Champ `evolution` de chaque élément de la distribution ; les transitions déplacent ce qui porte le sens. |
| 6. PNG au service de la scène | Un PNG est un lieu ou un objet qui reçoit ou émet des éléments animés en code. Tout processus est animé en code. | `source` de chaque élément ; aucun « zoom sur PNG » comme action. |
| 7. Simplicité de la référence | Fond ivoire quadrillé, encre, un seul accent cyan, Inter lisible, 1 à 4 éléments actifs à la fois, peu d'accents concurrents. | `style` conforme à `style.md` ; rouge réservé à l'alerte. |

**Critère de réussite.** Le storyboard le vise dès l'écriture : chaque scène a une `lecture_sans_son`, le film a 6 à 10
`idees_cles` que le contrôle sans son notera une à une (GOT, PARTIAL ou MISSED), et le test du spectateur muet est fait
sur le storyboard avant toute mise en scène (`test_sans_son`).
