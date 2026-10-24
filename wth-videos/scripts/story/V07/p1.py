"""V07, partie 1 : S01-S09, images 0-1044 (accroche, annonce, contexte, erreur 1 allumée). 34 temps forts, 34,8 s.

ÉTAT D'ENTRÉE (image 0 = distribution, à épingler à -1) : ivoire quadrillé ; au centre gauche le `panier` FERMÉ
(corps 340, 1010 ; `panier_couvercle` en 892 et son `panier_bouton`) ; sur son devant l'`etiquette` cyan « ETF Monde »
(340, 1050) pendue au rebord par `ficelle_etiq` ; à droite « Toi » (`c.toi`, bras gauche) en P1 (660, 1135), bras
BAISSÉ (pose `low_pose`), nommé par `toi_nom` « Toi » (745, 1060). Tout le reste est à l'échelle 0. Rien ne bouge.

Temps forts (image du mot ; kit.at peut caler ±1 sur l'attaque, ACOUSTIC_SNAP) :
S01  acheté@10  donc@48  diversifié.»@64
S02  penses@109  Pas@140  vite.@150
S03  Dans@172  trois@219  erreurs@229  savoir@312  achètes@338
S04  ETF,@402  coté@468  Bourse@480  cherche@499  reproduire@511
S05  achètes@563  fois@585  panier@606  titres.@618
S06  Et@638  frais@681  géré@719  activement.@730
S07  Mais@759  dépend@778  entièrement@790  l’indice.@811
S08  l’indice ?@867  décide@919  possèdes.@953
S09  Première@980  ne@1008  lire.@1021

BRIEF, scène par scène (ids de la distribution entre accolades ; toutes les places sont des constantes du paquet) :
- S01 « acheté » : la main de « Toi » se lève (`c.toi.reach` commencé ~6 images avant, cible à sa gauche, vérifier
  `assert_reach`) ; {piece} naît de la pointe (kit.pop from_pt = c.toi.tip), vole en arc 60 jusqu'au couvercle et s'y
  réduit (kit.vanish into `panier_couvercle`) ; à l'arrivée le couvercle tressaute (kit.shake y, 4) et {etiquette} +
  {panier} battent une fois (pulse x1,08). Puis `lower`. « donc » : {bulle_rond1..3} montent de la tête (stagger 2 de
  pop). « diversifié. » : {bulle} s'ouvre (pop), {bulle_texte} s'écrit (kit.type rate 2), {bulle_coche} se trace
  (coche HUMAINE pleine deep).
- S02 « penses » : {bulle} et {toi_nom} battent sur la même image (pulse x1,08). « Pas » : tap sur COUVERCLE_TAP
  (contact = l'image du mot : `c.toi.tap(f - TAP + 1, …)`) ; {question} naît du contact (pop from_pt) et s'arrête en
  QUESTION_NEE. « vite. » : {bulle_coche} tombe (kit.drop out=True, h 52, dx 18, rot 35) ; {question} vole en arc
  jusqu'à QUESTION_BULLE en passant à x 70/90 : « diversifié ? ». `lower`.
- S03 « Dans » : {bulle} et ses ronds se réduisent dans le « ? » (vanish into « question »), {question} grandit à
  x 110/90. « trois » : {question} monte en (540, 300) et se change en {marqueur} (morph relais ; `on` reste 0 : aucune
  étape active). « erreurs » : {titre_erreurs} « 3 erreurs » surgit en TITRE_MARQUEUR_C ; 4 images après, les légendes
  entrent en fondu (piste `lbl` du marker, doneStyle « kept » : S.set("marqueur", lbl=0) avant le pop, puis
  0 -> 1 en FADE) — vérifier qu'aucun disque n'est cyan (on = 0). « savoir » :
  c.toi.reach à 14 px au-dessus de COUVERCLE_TAP. « achètes » : tap, le couvercle tremble (shake x, 8) et RESTE fermé.
  `lower` puis tenue jusqu'à 376.
- S04 « ETF, » : {etiquette} + {panier} battent (x1,1). « coté » : {bourse} se trace (kit.draw 20, linéaire).
  « Bourse » : {bourse_mot} s'écrit (rate 1). « cherche » : {bourse}, {bourse_mot} vanish ; {livre} tombe en LIVRE_C
  (kit.drop, opacity déjà 1, échelle posée par drop) ; {livre_titre} « Indice » en fondu (FADE) ; les {mini1..10}
  sont enfants du livre (déjà à l'échelle 1) : ils arrivent avec lui. « reproduire » : les {copie1..10} partent des
  minis (position monde = S.to_world("livre", MINI_LOCAL[k], f)), filent en arc 80 vers le couvercle en grandissant
  (stagger 2 de kit.move + scale x2,6), s'y réduisent (vanish into `panier_couvercle`) ; à la dernière, shake y 4.
- S05 « achètes » : tap COUVERCLE_TAP. « fois » : {panier_couvercle} s'envole en arc vers le haut à droite et se
  réduit (move arc 60 + vanish, 350 ms) ; dans les mêmes images {titre1..10} surgissent TOUS sur la même image
  (pop 300 ms, scale 1). `lower`. « panier » : panier + titres battent (x1,06). « titres. » : vague (stagger 2 de pulse
  x1,2) et {nb_titres} pop en NB_TITRES_C, valeur 1 -> 10 en linéaire sur la durée de la vague.
- S06 « Et » : {livre} -> LIVRE_RANGE x0,55 (move 550 ms) ; {nb_titres} vanish. « frais » : {frais_mot} fondu ;
  reach de la main (cible à gauche de l'épaule) ; {frais_etf} naît de la pointe, vole en arc 60 vers FRAIS_ETF_C ;
  {frais_etf_lbl} « ETF » fondu. « géré » : {frais_ga_lbl} fondu ; {frais_ga1..4} partent de la pointe l'un après
  l'autre (stagger 3, arc 60) vers FRAIS_GA_C. « activement. » : {frais_etf} bat seul (x1,15) ; `lower`.
- S07 « Mais » : {frais_etf} rentre dans {etiquette} (vanish into « etiquette ») ; {frais_ga1..4}, les deux légendes
  et {frais_mot} se réduisent (morph sortie groupée) ; {livre} revient en LIVRE_C x1 (move 550 ms). « dépend » :
  {ficelle} se trace (kit.draw 9). « entièrement » : {livre}, {panier}, {etiquette} glissent de +SLIDE_DX en x
  EXACTEMENT ensemble (mêmes clés : move 550 ms inOut, aucun mouvement vertical) ; {ficelle} suit (ancrée).
  « l’indice. » : retour de -SLIDE_DX ; à l'arrêt, {mini*} et {titre*} battent sur la même image (x1,15).
- S08 « l’indice ? » : {livre} bat (x1,08), {livre_titre} se souligne (`under` 0 -> 1, 9 images), {toi_nom} s'efface
  (FADE). « décide » : {mini8} (MINIS[TITRE_TOMBE]) vanish ; {ficelle_halo} bat (opacité 0 -> 1 -> 0, ~8 images ; la
  piste sw d'un fil n'existe pas) ; 6 images après {titre8} saute hors du panier et tombe à gauche
  (kit.drop out=True, h 80, dx -120, rot -30). « possèdes. » : {mini_neuf} pop ; {titre_neuf} (enfant du panier)
  glisse le long de {ficelle} (S.along_wire, 550 ms, t 0 -> 1, la géométrie figée au mot) puis se pose en
  TITRES_LOCAL[TITRE_TOMBE] (déjà sa place : finir l'along_wire là, ou relais `titre_neuf_vol` -> titre_neuf).
- S09 « Première » : {marqueur} `on` 0 -> 1 (POP, disque 1 cyan, légende « Indice » en Bold). « ne » : tap sur
  ETIQ_TAP ; {etiquette} bat (x1,08). `lower`. « lire. » : « Toi » tourne la tête dos au livre (`look` 0 -> +1,
  4 images ; kit.ensure("toi", "look", 0)) ; {livre} bat deux fois (pulse x1,1, times 2, ~8 images d'écart). Tenue.

PASSAGE À p2 (image 1044 = ENTRY_P2 de __init__, à respecter exactement) : panier ouvert en PANIER_C (couvercle 0),
titres light à TITRES_LOCAL (titre8 échelle 0 et opacité 0, titre_neuf à sa place), étiquette en ETIQ_C, frais_etf
à 0 (rangée dans l'étiquette), livre en LIVRE_C x1 avec livre_titre (opacité 1, under 1) et ses minis (mini8 0,
mini_neuf 1), ficelle tracée (draw 1, from 0), ficelle_halo opacité 0, marqueur on 1 / active 0, titre_erreurs 1,
toi_nom opacité 0 ; « Toi » en P1, bras baissé, look +1. Tout ce qui commence ici finit avant 1045.

Règles : bras baissé entre deux gestes (`lower`) ; jamais de clé ni d'épingle sur la figurine ; chaque mouvement de
« Toi » vers une cible : `assert_reach(P1[0], cible, "S0x …")`. Aucune coche variant « ai » (pas d'IA).
"""
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401

from . import *  # noqa: F401,F403


def part(S, kit, c):
    pass
