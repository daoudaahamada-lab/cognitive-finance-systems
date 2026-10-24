# Leçons de V01 : les retours de revue devenus des règles

V01 a demandé deux storyboards, deux tours de revue d'un extrait de 15 s et un contrôle sans son final avant d'être
validé. Chaque règle ci-dessous vient d'un défaut réellement constaté : un spectateur muet a lu autre chose que voulu,
ou un critique a classé le défaut « majeur ». Les appliquer dès le storyboard évite de payer un tour de revue
(≈ 1 h 30 sur V01) pour le même défaut.

Sources : `wth-videos/build/wf_sb_result.json` (juges et test muet du storyboard), `wf_ex_result.json` (revues de
l'extrait, tours 1 et 2), contrôle sans son final de l'extrait (deux spectateurs, idées notées GOT / PARTIAL / MISSED).

## 1. Cause et preuve

1. **La preuve avant le verdict, et la cause visible.** La ligne fausse cassait sur « fausse », avant toute
   vérification : les spectateurs voyaient l'effet sans cause (« rien de visible ne le déclenche » ; « la vérification
   d'après ressemble à un replay »). Règle : on montre d'abord ce qui manque (la puce vide, la case vide), puis le
   verdict, et **c'est le geste de « Toi » qui le déclenche** (le stylo touche la valeur, elle casse).
2. **Un signe de vide reste vide.** Le « clignotement » de la puce vide la remplissait de cyan pendant 4 images : la
   ligne semblait avoir une source. Faire battre le contour, secouer, rougir le contour ; ne jamais remplir.
3. **Le moment « sans source » doit durer.** Le test de la ligne inventée était trop bref et effacé trop tôt : c'est
   pourtant l'idée centrale. Jouer pour elle le même test que pour les autres (le fil part, bute sur la case vide, la
   case tremble et reste vide), et tenir le résultat au moins 1 s.
4. **Les fils partent du texte qu'ils prouvent.** Un fil qui démarre dans le blanc entre deux lignes ne se rattache à
   rien à taille téléphone. Ancrer sur la valeur, au milieu de la ligne de texte.
5. **Ce qui naît d'une chose en sort.** Le « ? » apparaissait à côté de la fiche : il doit naître de la valeur sans
   source, sous la pointe du stylo, puis voyager.

## 2. L'IA et « Toi »

6. **Formes différentes, pas seulement couleurs.** Les coches de l'IA et du conseiller ne différaient que par la
   couleur. Désormais : coche de l'IA `variant="ai"` (pointillés dans un carré tireté), coche de « Toi » pleine `deep`.
7. **L'IA reste immobile quand elle se trompe.** Un faisceau de l'IA qui entourait la ligne cassée se lisait « l'IA
   signale elle-même ses erreurs ». Pendant l'erreur : ni faisceau, ni battement, ni sortie.
8. **Garder la coche de l'IA sur la ligne fausse.** Effacer les coches grises juste après la fissure se lisait « les
   coches sont retirées parce que la ligne a cassé » : le contraste « l'IA l'avait validée » disparaissait.
9. **La sortie de l'IA ne doit pas dire « l'humain remplace l'IA ».** Elle se range (badge, coin, retour à sa place),
   elle n'est pas chassée par « Toi ». Le partage se montre sans exclure (V01 : la bascule, elle apporte, il porte le poids).
10. **Les outils tiennent dans la main de « Toi ».** Un stylo qui flottait sans bras, un tampon venu de nulle part, puis
    un bras élastique : l'agence du conseiller ne se lisait plus. Le rig `Figure` (bras à longueur fixe, pas
    automatique) règle le dessin ; le storyboard, lui, place « Toi » à portée de ce qu'il touche.

## 3. Les personnes

11. **L'autre personne arrive sur son mot et reste.** Le client, à l'écran trop peu de temps et entré trop tôt, épaule
    contre épaule avec le conseiller, se lisait « un collègue ». Règle : il apparaît sur le mot qui le nomme, face à
    « Toi », à 120 px au moins, et reste assez longtemps pour être identifié (≥ 1,5 s) ; il ne sort pas en se réduisant
    à un point au milieu d'une action.
12. **La bulle part de celui qui parle.** Une bulle « ? » au-dessus du client se lisait « le client a une question ».
    Une question à poser au client part de « Toi », queue tournée vers lui.

## 4. Lisibilité, densité, rythme

13. **1 à 4 éléments actifs, ~8 formes au plus à l'écran.** La fiche avec 5 cases, 4 documents, 4 fils et 19 textes
    devenait « un tableur miniature » à taille téléphone. Ce qui a fini d'agir sort de scène ou se réduit.
14. **Une action principale par temps fort.** Aux entrées de scène, plusieurs temps forts fusionnaient en un long
    mouvement chargé. Sur le mot d'entrée : la sortie et le déplacement, puis tenue ; le geste suivant sur le mot
    suivant.
15. **Ouverture légère.** L'accroche faisait apparaître le client, battre l'horloge, ouvrir la chemise et disperser les
    papiers en 1,2 s : un « éclair de papiers ». Première image déjà lisible, un seul geste.
16. **Pas d'abstraction qui demande la voix.** Barre qui se remplit = progrès (et non temps perdu) ; coffre + câble =
    archivage ou recharge ; lumière découpée par un cadre = décor ; pile qui éclate = échec. Préférer un verbe visuel
    sans ambiguïté (`visual-verbs.md`) : une barre qui **fond**, un mur qui **bloque**, un ◀◀ qui **rembobine**.
17. **Pas de lien de cause involontaire.** Des cartes grises qui disparaissaient juste après que le rayon les visait se
    lisaient « l'IA a supprimé les autres dossiers ». Deux événements successifs se lisent comme cause et effet.

## 5. Transformations (point 5 du brief)

18. **Transformer pour de vrai, pas en fondu.** « Le document devient une étiquette-source » était simulé par un
    fondu ; le critique l'a refusé. L'objet voyage jusqu'à sa nouvelle place et se change en route (morph de 350 ms).
19. **Casser, c'est séparer.** Une ligne qui s'incline se lisait « de travers ». Une vraie fente, un écart où l'on voit
    le fond, une moitié qui tombe.
20. **Corriger n'est pas valider.** Barrer « 5 ans » laissait la valeur à côté de l'autocollant « ? » : le tampon
    semblait approuver « 5 ans ». La valeur barrée tombe hors de la fiche, la question prend sa place.

## 6. Décision et vérité

21. **Jamais « VALIDÉ » avec une question ouverte.** Le tampon VALIDÉ tombait alors qu'une ligne restait à confirmer.
    La question porte « à poser au RDV » et le tampon dit ce qui est vrai (par exemple « PRÊT POUR LE RDV »).
22. **L'image finale d'une scène est propre.** Collision sur la ligne finale (autocollant sur la valeur barrée) : la
    dernière image d'un résultat ne doit avoir aucun chevauchement (≥ 12 px d'air).

## 7. Mise en page et textes

23. **Utiliser le bas de l'image.** Les 40 % du bas étaient vides : la composition descend jusqu'à y ≈ 1250 (ligne de
    sol vers 1230), en restant au-dessus des sous-titres.
24. **Dates en clair.** « 09/25 » était ambigu : écrire « sept. 2025 ».
25. **Le repère 1-2-3 a une légende.** Sans elle, trois cercles numérotés ne disent rien : un mot par étape.
26. **Gris à 50 % = rejeté.** Des lignes grisées pour les « mettre en retrait » se lisaient refusées. Réduire, déplacer
    ou sortir plutôt que griser.
27. **Ce qu'on ne comprend que par un mot écrit est fragile.** Le test muet signale tout ce qui n'est compris que grâce
    à une étiquette : l'action doit porter le sens, l'étiquette ne fait que confirmer.

28. **Toute la hauteur utile (V02).** Une action tassée dans le tiers haut, avec un bas vide, devient illisible à
    360 px : composer de y≈180 à y≈1240 et donner aux libellés clés au moins 34 px.
29. **Un objet se reconnaît sans son étiquette (V02).** Une société = un immeuble (pas un portrait, lu « pièce
    d'identité ») ; une appli = la même carte-appli que celle du héros ; une clé = une vraie silhouette de clé (pas une
    capsule) ; un registre = une liste d'inscrits sous un sceau.
30. **Un geste en deux temps doit se lire comme les deux moitiés d'un même acte (V02).** Couper « dans l'appli puis à
    la banque » se lisait comme deux options : montrer les deux fiches du câble qui tombent l'une après l'autre, et la
    coche seulement quand les deux sont tombées.
31. **Récapitulatif lent (V02).** Environ 2 s par correction, alertes numérotées grandes et posées à côté de leur
    objet ; l'état final se tient au moins 1,5 s avant la carte de fin.
32. **Pas de curseur de souris (V02).** Le film est vu sur téléphone : toucher au doigt (anneau d'impact) ou stylet de
    « Toi ».

33. **Pas de métaphore indirecte (V03-V04).** Miroir, pellicule, viseur, hélice, vide, rond vide, tampon : jamais
    compris sans le son. Montrer les objets concrets du sujet (pièces, carte, téléphone, facture, calendrier,
    graphique) et des gestes directs (prendre, retirer, compter, barrer, relier).
34. **Contraste « subi / maîtrisé » en deux temps nets (V03).** Une main levée seule se lit « gêne ». Montrer la main
    repoussée par ce qu'on ne contrôle pas (croix ou cadenas dessus), puis la main qui saisit ce qu'on contrôle.
35. **Chiffre immobile = bug apparent (V04).** Un solde qui ne bouge pas pendant que tout change doit être signalé
    (cerclé, « toujours 800 € ») ; et le résultat final s'écrit en chiffres.
36. **« Toi » nommé dès sa première image, bras baissé au repos (V03).** Sinon on y voit un élève ou un présentateur.

37. **Un tableau final se remplit (V06).** Des cases en tirets « à remplir » se lisent « rien ici » (« seul
    l'appartement a des frais ») : remplir chaque case, ou écrire en clair « à toi de remplir ».
38. **Un axe de frise se légende à ses deux bouts (V06).** « tout de suite » / « des années » ; sinon on ne lit pas
    qu'il mesure un délai.

## 8. Ce qui a marché (à garder)

- Un objet unique qui change sous les yeux (la fiche) et une pastille-protagoniste qui ne le quitte pas.
- Le rouge réservé à une seule chose fausse : il se voit d'autant plus.
- Les verbes francs : fissure, fil tendu vers un document, case vide, rature, tampon.
- Les places fixes : IA à gauche, « Toi » à droite, repère en haut.
- La tenue avant le verdict (« et… » : rien ne bouge, puis « fausse »).
