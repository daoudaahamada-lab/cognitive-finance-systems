# Exemple annoté : deux scènes de V01 (le niveau de précision visé)

Les scènes S11 et S13 de `wth-videos/scripts/storyboards/V01.json` (v2), c'est-à-dire le cœur de l'extrait validé par
l'utilisateur (« C'est absolument parfait »). Elles montrent le niveau de détail qui permet de mettre en scène sans
deviner. Après chaque scène : pourquoi elle marche, puis ce que les revues ont corrigé ensuite (à faire dès le
storyboard sur les autres films, voir `lessons-v01.md`).

## S11 · « Mais une IA peut produire une réponse fluide… et fausse. »

```json
{
  "id": "S11", "t_start": 26.378, "t_end": 30.512,
  "texte": "Mais une IA peut produire une réponse fluide… et fausse.",
  "elements": "fiche, lignes, ligne_inventee, ia, outil (badge), pastille, temps_etapes (marqueur)",
  "etat_initial": "Page à 5 puces (4 à pictogramme, 1 vide en bas) dans la moitié droite de la fenêtre ; pile et IA dedans ; conseiller dehors en bas à droite ; marqueur sur « 2 ».",
  "action": "La fenêtre se réduit en badge avec la pile ; l’IA reste en bas à gauche, le conseiller sort ; la page vient au centre en grandissant et la pastille se pose sur son en-tête. Un faisceau d’écriture relie l’IA à la page : les 5 lignes s’écrivent d’un trait et l’IA coche chacune en gris ; un reflet balaie la page. Silence. Puis la puce vide de la 5e ligne clignote : rien ne la porte. La ligne vire au rouge, se fissure et sa moitié droite s’affaisse, sous la coche grise de l’IA qui, elle, ne bouge pas.",
  "resultat": "Une fiche impeccable en apparence, dont la seule ligne sans document est rouge et cassée, toujours cochée par l’IA.",
  "transition": "Sur « Exige », l’IA sort par la gauche et les coches grises s’effacent ; la ligne cassée reste rouge.",
  "beats": [
    {"t": 26.378, "mot": "Mais", "evenement": "Morph 350 ms : la fenêtre se réduit en badge en haut à gauche (x 170, y 330, 130 px : barre de titre, sceau, cadenas), la pile dedans ; l’IA reste en bas à gauche (x 170, y 1030, 200 px) ; le conseiller se réduit en point ; la page passe au centre (x 540, y 720) et grandit à 520×640. La pastille vole du titre de la fenêtre à l’en-tête de la page (550 ms)."},
    {"t": 27.04, "mot": "IA", "evenement": "Un faisceau d’écriture cyan pointillé relie l’IA à la page."},
    {"t": 27.841, "mot": "produire", "evenement": "Les 5 lignes s’écrivent en continu de L1 à L5 (3 caractères par image, fin vers 28,8 s) ; chaque ligne terminée reçoit une petite coche grise de l’IA."},
    {"t": 28.875, "mot": "fluide…", "evenement": "Un reflet blanc traverse la page en diagonale (400 ms), puis immobilité totale."},
    {"t": 29.722, "mot": "et", "evenement": "Tenue : rien ne bouge."},
    {"t": 29.896, "mot": "fausse.", "evenement": "La puce vide de L5 clignote deux fois (200 ms) ; « Horizon : 5 ans » passe au rouge (100 ms) ; une fissure en zigzag la coupe et sa moitié droite tombe de 14 px en pivotant de 5° (300 ms ease-out). La coche grise de l’IA reste en place, intacte."}
  ],
  "lecture_sans_son": "La machine écrit une fiche qui a l’air parfaite ; la seule ligne qui ne vient d’aucun document casse, et la machine la coche quand même."
}
```

**Pourquoi elle marche**
- **Le sens complet de la phrase** (point 3) : « fluide » est joué (écriture d'un trait, coches, reflet), puis
  « fausse » (rouge, fissure), et la nuance « peut » est portée par la ligne préparée dès S10 (puce vide, née de la tête
  de l'IA).
- **Continuité** (point 5) : `etat_initial` reprend exactement le `resultat` de S10 ; la pastille du fil vole de la
  fenêtre à l'en-tête de la page au lieu d'être recréée.
- **Chaque temps fort sur un mot** : 6 temps forts en 4,1 s, chacun avec position, taille, durée et profil. Un auteur
  peut écrire `kit.at("S11", "produire")` puis `kit.stagger(rows, f, …, kit.type)` sans rien inventer.
- **La tenue avant le verdict** : « et » ne fait rien bouger. C'est le « tenir, puis éclater » de la référence.
- **Un seul rouge**, sur la seule chose fausse.
- **`lecture_sans_son` honnête et vérifiable** : elle devient presque mot pour mot une idée-clé.

**Ce que les revues ont corrigé ensuite (à faire d'emblée)**
- La ligne casse sur « fausse », avant toute vérification : les spectateurs muets ont vu l'effet sans cause. Dans la
  v3, la fissure attend le stylo de « Toi » (S13-S14) ; sur « fausse », on montre seulement le manque (la puce vide
  bat, contour rougi, jamais remplie) et la tenue.
- Les coches de l'IA ne différaient de celles du conseiller que par la couleur : coche `variant="ai"`.
- Le « clignotement » remplissait la puce vide : un signe de vide reste vide.
- La transition efface les coches grises : on les garde, sinon « la coche de l'IA sur la ligne fausse » se perd.

## S13 · « Une info sans source, c’est une question à poser au client. »

```json
{
  "id": "S13", "t_start": 34.296, "t_end": 37.919,
  "texte": "Une info sans source, c’est une question à poser au client.",
  "elements": "fiche, lignes, ligne_inventee, sources, documents, conseiller, outils (stylo), question (« ? », bulle WTH-003-06), client, pastille",
  "etat_initial": "Page à gauche, 4 fils tendus vers 4 documents datés, case 5 vide en face de L5 rouge ; conseiller en bas à droite.",
  "action": "Les documents remontent leurs fils et deviennent de petites étiquettes-sources au bout des lignes ; la colonne se vide, sauf la case 5. L5 lance un fil vers sa case : vide, le fil retombe. Le conseiller s’approche et touche du stylo la valeur « 5 ans » : un grand « ? » en sort, monte au-dessus de sa tête, et une bulle de verre grandit autour, la queue tournée vers lui. Le client apparaît en face de lui.",
  "resultat": "Les lignes prouvées portent leur source ; l’info sans source est devenue une question que le conseiller va poser au client.",
  "transition": "Sur « Dernière », la bulle se réduit en autocollant « ? » qui attend au bout de L5 ; le client sort.",
  "beats": [
    {"t": 34.296, "mot": "Une", "evenement": "Les 4 documents glissent le long de leurs fils et rétrécissent en étiquettes-sources (pictogramme + date) accrochées au bout de leur ligne ; les fils se rétractent ; les cases 1 à 4 s’effacent (350 ms). La case 5 reste, vide."},
    {"t": 34.772, "mot": "sans", "evenement": "Les lignes 1 à 4 passent à 40 %. L5 lance un fil pointillé encre vers la case 5 (250 ms) : la case est vide, le fil se détend et retombe en courbe molle (300 ms), puis s’efface avec la case."},
    {"t": 35.759, "mot": "c’est", "evenement": "Retour à 100 %. Le conseiller s’avance (x 660, y 1090 ; 400 ms) et pointe son stylo sur « 5 ans »."},
    {"t": 36.166, "mot": "question", "evenement": "Sous la pointe du stylo, un grand « ? » encre (110 px) sort de « 5 ans », qui reste rouge et fissuré (pop 300 ms)."},
    {"t": 36.665, "mot": "poser", "evenement": "Le « ? » monte en arc au-dessus du conseiller (550 ms) ; la bulle WTH-003-06 grandit autour de lui (x 800, y 870, 260 px), le « ? » dans son creux à côté de la loupe, la queue en bas à gauche pointée vers la tête du conseiller."},
    {"t": 37.036, "mot": "client.", "evenement": "Le client apparaît face au conseiller, à droite (x 890, y 1090 ; pop 300 ms), et s’incline de 5° vers lui."}
  ],
  "lecture_sans_son": "Ce qui n’a pas de preuve devient une question : le conseiller la posera au client."
}
```

**Pourquoi elle marche**
- **Les éléments évoluent** (point 5) : le document devient étiquette-source, la ligne sans source devient « ? », le
  « ? » devient bulle, puis autocollant en S14. Rien n'est remplacé.
- **Le geste de « Toi » cause l'effet** : le « ? » naît sous la pointe du stylo, de la valeur elle-même.
- **Synchronisation sémantique** : la question naît sur « question », la bulle sur « poser », le client sur « client ».
- **Un PNG au service de la scène** (point 6) : la bulle de verre reçoit un « ? » dessiné en code ; elle n'est pas
  zoomée pour raconter.

**Ce que les revues ont corrigé ensuite**
- La preuve du « sans source » était trop brève et effacée trop tôt : faire le même test qu'aux lignes 1-4 (le fil
  bute sur la case vide, qui tremble et reste vide) et tenir le résultat.
- Lignes 1 à 4 « à 40 % » : lues comme rejetées. Mettre en retrait en réduisant ou en éloignant, pas en grisant.
- Le client entrait trop tôt, épaule contre épaule : il apparaît sur « client. », face à « Toi », à 120 px au moins, et
  reste jusqu'à la décision.
- La question est marquée « à poser au RDV », et le tampon de S14 ne dit plus « VALIDÉ » tant qu'elle est ouverte.

## Champs ajoutés depuis (absents de la v2 de V01)

V01 v2 précède les champs `objet_fil` et `idees_cles` : sa v3 les ajoute. Exemple de forme attendue :

```json
"objet_fil": {"id": "pastille", "description": "Pilule cyan « Client · 9 h », toujours posée sur ce qui contient le dossier (chemise, pile, fenêtre, fiche) ; devient le bouton « S’abonner »."},
"idees_cles": [
  {"id": "a", "idee": "Les documents du client sont dispersés et chercher à la main mange le temps du conseiller.", "scenes": ["S03", "S04"], "principale": false},
  {"id": "b", "idee": "Le conseiller limite ce que l’IA lit : seulement ce dossier, dans un outil scellé par le cabinet.", "scenes": ["S05", "S06", "S07"], "principale": true},
  {"id": "c", "idee": "Les données du client ne vont pas dans une IA grand public : un mur les arrête.", "scenes": ["S08", "S09"], "principale": true},
  {"id": "d", "idee": "L’IA écrit une fiche qui a l’air parfaite, mais la seule ligne sans document est fausse.", "scenes": ["S10", "S11"], "principale": true},
  {"id": "e", "idee": "Chaque ligne est reliée à un document daté ; l’info sans source devient une question pour le client.", "scenes": ["S12", "S13"], "principale": true},
  {"id": "f", "idee": "C’est le conseiller, pas l’IA, qui relit, corrige et décide.", "scenes": ["S14", "S15", "S16"], "principale": true},
  {"id": "g", "idee": "Dix minutes de relecture évitent l’erreur devant le client.", "scenes": ["S17"], "principale": false},
  {"id": "h", "idee": "Avant : il arrive avec une pile ; après : avec une fiche vérifiée et comprise.", "scenes": ["S18", "S19"], "principale": true}
]
```
