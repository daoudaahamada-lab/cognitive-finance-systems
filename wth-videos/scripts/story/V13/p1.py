"""V13, partie 1 : S01-S08, images 0-986 (40 temps forts, 32,9 s). Accroche (le solde regardé, réduit à une case sur
neuf), l'équation « grille − carte grise = Patrimoine net », la cible « Ta stratégie », le repère 1-2-3, point 1 :
la case du solde éclairée puis six cases nommées.

ÉTAT D'ENTRÉE : l'image 0 du film = l'état de distribution (cast) : carte « Solde » (enfant de `grille`, monde
(540, 640), 440 x 300) et pilule « 3 200 € » (`solde`, (540, 690), échelle 1) au centre ; « Toi » en TOI_P1, VISIBLE
dès l'image 0 (Figure show=True), pilule « Toi » au-dessus de sa tête. Rien d'autre. Pas d'épingle (la partie commence à
l'image 0). Image 0 lisible et immobile : poser le bras baissé dès l'image 0 (c.toi.lower(0, d=1) ou équivalent) sans
mouvement visible.
SORTIE : ENTRY_P2 à l'image 986 (voir __init__.py). Tout ce que cette partie commence finit avant 987. Les fils
rétractés (regard, fil_grille, fil_dettes, fleche) finissent en draw 0 ET from 0 (clés instantanées une fois
invisibles) ; net_trait en draw 0 (après la sortie de `net`) ; compte_filet à l'échelle 0 (sorti en S02) ; « Toi » en
P1, stylo baissé.

Ids : grille ; compte (+ compte_ico, compte_mot, compte_filet) ; solde ; q_livrets … q_societe (+ _mot) ; case_livrets,
case_assurance, case_pea, case_epargne, case_per (+ _ico, _mot) ; toi (c.toi), nom_toi, regard, question ; entete,
cadre, moins, egal, dettes (+ dettes_ico, dettes_mot), net (+ net_trait), fil_grille, fil_dettes ; cible, cible_onde,
depart, fleche, fleche_pointe, strategie ; marqueur.
Constantes et aides : voir __init__.py (grid_world, cell_world, move_with_grid, drop_in, ring, scene_f0, line, head).

BRIEF, scène par scène (images = round(t × 30), avant calage acoustique ; poser CHAQUE temps fort par kit.at / kit.hold
avec un `what` qui dit ce qu'on voit) :
- S01 (0-88) « regardes » (7) : kit.draw("regard", f, 9) (tirets encre, REGARD_EYE -> REGARD_CARTE). « solde » (22) :
  kit.pulse("solde", f, times=2, step=3, peak=1.1) ; rien d'autre ne bouge. « où » (63) : kit.pop("question", f,
  from_pt=HEAD_P1, to=QUESTION_C) ; tenue.
- S02 (89-139) « Ce » (89) : RELAIS carte -> case (MOVE 16, inOut) : compte pos COMPTE_LOCAL0 -> CELL_LOCAL[0], w/h
  440x300 -> 250x180 (S.key w, h même clé), compte_ico -> COMPTE_ICO_CELL échelle 0.75, compte_mot -> COMPTE_MOT_CELL
  échelle 0.85, compte_filet vanish ; solde -> SOLDE_CELL_FULL échelle SOLDE_CELL_K (même clé) ; regard pb ->
  REGARD_CASE (même clé : le regard reste accroché au bas de la case) ; kit.vanish("question", f, into=HEAD_P1).
  « chiffre » (94) : kit.pulse("solde", f, step=3, peak=1.12). « presque » (110) : les 8 cases « ? » sortent de
  derrière la case du solde (elles y sont déjà, z plus bas) : kit.stagger(Q_IDS[1:], f, 2, …) pop (scale 1) puis
  kit.move vers CELL_LOCAL[i] (9 images, out), dans l'ordre de lecture. « rien. » (121) : les 8 « ? » battent ensemble
  (kit.pulse peak 1.05, step 2) ; rien ne se remplit.
- S03 (140-301) « Dans » (140) : move_with_grid(kit, f, small=True) (grille ×0,6 en haut à gauche, la pilule suit) ;
  regard : pb suit la case (même clé, vers grid_world point bas de la case réduite) puis rétraction kit.draw("regard",
  f + 4, 9, track="from"). « voir » (176) : c.toi.walk(f, TOI_P2[0]) (590 : écart, voir __init__) ; nom_toi ->
  NOM_RIGHT (kit.move, même durée). « calculer » (192) : c.toi.unstow si rangé, c.toi.reach(f, NET_PEN, d=9).
  « patrimoine » (214) : kit.pop("net", f, from_pt=NET_PEN, to=NET_C). « net. » (229) : kit.pulse("net", f, step=3,
  peak=1.08) ; AUCUN signe. « lire » (270) : c.toi.trace(f, list(NET_PEN_TRACE)) et kit.draw("net_trait", hits[0],
  19, e="linear") (le trait part sous la pointe et file seul jusqu'au bout). « chiffre. » (281) : kit.pulse("solde",
  f, step=3, peak=1.15) puis kit.pulse("net", f + 6, step=3, peak=1.08) ; c.toi.lower (stylo baissé).
- S04 (302-427) « Ton » (302) : c.toi.walk(f, TOI_P1[0]) (bras baissé : walk(..., low=True)) ; nom_toi -> NOM_ABOVE.
  « tout » (347) : kit.draw("cadre", f, 9). « possèdes, » (363) : kit.type("entete", f) puis S.key("entete",
  "under", …, 1, FADE). « moins » (385) : kit.pop("moins", f). « dois. » (412) : drop_in(kit, "dettes", f) en
  DETTES_C (scale 1 à f - 1 par kit.drop) ; kit.pop("egal", f + 11) en EGAL_C : l'équation se ferme maintenant.
- S05 (428-601) « photo » (438) : kit.draw("fil_grille", f, 9) ; kit.draw("fil_dettes", f + 3, 9). « honnête » (457) :
  kit.move("net", f, NET_C, d=10, scale=1.15, e="out"). « situation. » (472) : c.toi.lean_to(f, 6, d=14) (vers
  l'équation) ; kit.pulse("nom_toi", f, step=3, peak=1.1) ; c.toi.lean_to(f + 12 + 14, 0) (se redresse).
  « point » (517) : drop_in(kit, "cible", f) en CIBLE_C. « départ » (528) : kit.pop("depart", f, d=6) ;
  kit.draw("fleche", f + 6, 13) ; kit.pop("fleche_pointe", f + 6 + 11, d=4). « stratégie » (551) :
  kit.pulse("cible", f, step=3, peak=1.08) ; ring(S, "cible_onde", f, d=18). « patrimoniale. » (568) :
  kit.type("strategie", f) ; tenue.
- S06 (602-667) « Pourquoi » (602) : morph (MORPH 11) : sortent cible, strategie, depart, fleche_pointe, cadre, moins,
  egal (kit.vanish) ; fleche, fil_grille, fil_dettes se rétractent (track "from", 6 images) puis draw/from à 0 ; entrée
  du repère : kit.pop("marqueur", f) (on 0) ; « Ce que tu possèdes » glisse et se réduit sur la légende 1
  (kit.vanish("entete", f, into=MARKER_LEGENDS[0])) pendant que le repère grandit (relais à la même place).
  « commencer » (616) : kit.vanish("dettes", f, into=DISQUE2, d=MORPH) ; kit.vanish("net", f + 3) (sur place ; puis
  S.key("net_trait", "draw", f + 3 + POP, 0)). « possèdes ? » (649) : S.key("marqueur", "on", f, 1, POP, "out") ;
  move_with_grid(kit, f, small=False) (la grille revient à pleine taille, la pilule suit).
- S07 (668-756) « solde » (686) : kit.pulse("solde", f, times=2, step=3, peak=1.12). « montre » (706) :
  S.key("compte", "fill", f, LIGHT, 9) et S.key("compte", "stroke", f, DEEP, 9) (hex). « partie. » (733) : les 8 « ? »
  battent (kit.pulse peak 1.06, times=2, step=2) ; vides.
- S08 (757-986) « Fais » (757) : c.toi.unstow(f) (ou le stylo remonte de la pose basse). « liste » (766) :
  hit = c.toi.tap(f, (720, 996)) ; les 3 « ? » du bas battent au contact (pulse peak 1.05). « comptes, » (797) : compte
  fill -> PAPER, stroke -> INK (hex, 3 images) ; compte_mot : fade 3 images, text -> T_COMPTES, chars 0 -> 7 (kit.type
  rate 2), fade retour ; la pilule ne bouge pas. « livrets, » (814), « assurance-vie, » (832), « PEA, » (863),
  « épargne » (903), « PER. » (943) : kit.morph(Q_IDS[i], CASE_IDS[i], f) (relais à la même place) puis
  kit.type(f"{CASE_IDS[i]}_mot", f + 3, rate=3). Sur « PER. » : c.toi.lower(f + 12) (stylo baissé). Fin : six cases
  nommées, trois « ? » en bas.

PASSAGE À p2 : la grille pleine, six cases nommées, trois « ? » (immo, vehicule, societe) en bas ; « Toi » en P1 stylo
baissé ; repère étape 1 allumé ; rien d'autre (ENTRY_P2).
"""
from pipeline.story import STYLE  # noqa: F401


def part(S, kit, c):
    pass
