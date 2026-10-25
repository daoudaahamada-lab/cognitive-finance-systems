"""V08, partie 2 : S07-S14, images 738-1805 (étape 1 : les revenus réguliers, la prime écartée ; étape 2 : les
charges se servent, la liste cochée, 3 relevés, la moyenne). 33 temps forts, 35,6 s.

ÉTAT D'ENTRÉE (etat_initial de S07, à épingler à 737 : `kit.pin(f0 - 1, ENTRY_P2)` avec f0 = scene_f0(S, "S07")) :
colonne `revenus` en COL_S01 (x 270-570, bas 1180) : billets `salaire`, `mot_salaire` couvert par le haut cyan
`reste` (RESTE_S05, y 620-786) qui porte `legende_reste` « reste à vivre » (encre) ; pile `charges` en PILE_S04
(`loyer`, `factures`, `credits`, y 786-1180), `cadenas` au bord, `ligne_partie` sous les blocs ; accolades
`accolade_g` / `accolade_d` et `acc_revenus` / `acc_charges` ; `egal` « = » deep ; `pastille` « ? € » en
PASTILLE_S04 ; `marqueur` on 0, légende visible ; « Toi » en P1 (860, 1135), bras baissé. Garde-fou figurine :
`if S.val("toi", "scale", f0 - 1) == 0: c.toi.enter(f0 - 10, at=list(P1))`.

Temps forts (image du mot) :
S07  Pourquoi@738  revenus ?@775  base@824  bon@861  mois.@866
S08  Première@887  additionne@920  net,@954  allocations@972  autres@1005  fixes.@1024
S09  primes@1056  exceptionnelles ?@1092  Laisse-les@1120  reviennent@1171  chaque@1189
S10  Ensuite,@1216  part@1269  dépenses.@1299
S11  Deuxième@1325  liste@1356  loyer@1403  abonnements.@1420
S12  Ouvre@1448  3 ?@1517
S13  tromper :@1570  facture@1596  sans@1644  dépense@1672
S14  moyenne@1719  3@1737  base@1767  honnête.@1782

BRIEF, scène par scène :
- S07 « Pourquoi » (morph 350 + MOVE 550) : {charges} se soulève et se range en PILE_RANGE_S07 x PILE_RANGE_K
  (move 550) ; {revenus} glisse en COL_S07 ; {reste}, {legende_reste}, {accolade_g}, {accolade_d}, {acc_revenus},
  {acc_charges}, {egal}, {cadenas}, {ligne_partie} se réduisent (morph sortie groupée ; une poly tracée : vanish ou
  draw 1 -> 0) ; {pastille} -> PASTILLE_ATTENTE x PASTILLE_ATTENTE_K. {mot_salaire} redevient visible (le cyan est
  parti). « revenus ? » : walk_low vers P2 ({nom_toi} suit). « base » : {socle} sx 0 -> 1 (STRETCH) ; à f + 6,
  {chaque_mois} `scale` 1 puis kit.type. « bon » : {bon_mois} pop en BON_MOIS_SOMMET (tirets, « bon mois »).
  « mois. » : {bon_mois} oscille (rot ±6°, 2 battements) puis glisse le long du flanc droit et tombe en
  BON_MOIS_ATTENTE x BON_MOIS_K (move 12 images « in ») : il ne tient pas.
- S08 « Première » : {marqueur} `on` 0 -> 1 (POP) : disque 1 cyan, « Revenus » en Bold. « additionne » : {plus} pop
  en PLUS_C, à la place du bon mois. « net, » : {mot_salaire} glisse en MOT_SALAIRE_NET_LOCAL (6 images) et {net}
  s'écrit (kit.type), puis `under` 0 -> 1 (8 images). « allocations » : {allocations} (enfant de revenus) entre par
  la droite depuis ALLOC_ENTREE (monde -> local : S.parent_space) et se pose en ALLOC_LOCAL (scale 1 posé à l'image
  de départ, move 550) ; {plus} -> PLUS_HAUT. « autres » : {autres} de même en AUTRES_LOCAL ; {plus} vanish into
  « revenus » (vers le haut de la colonne). « fixes. » : c.toi.tap(f - TAP + 1, REVENUS_TAP) (assert_reach(P2[0])) ;
  au contact {mot_revenus} pop. `lower`.
- S09 « primes » : {bon_mois_mot} bascule `text` T_PRIME (textes : fondu de la piste opacity du mot, 4 + FADE) ;
  {bon_mois} bat (x1,12). « exceptionnelles ? » : {bon_mois} -> PRIME_COLLE (move 14 images) et `stroke` INK -> RED
  (hex, 9 images). « Laisse-les » : c.toi.tap(f - TAP + 1, PRIME_TAP) (assert_reach(P2[0], PRIME_TAP, …) : partie
  gauche du bloc, pas son centre) ; au contact {bon_mois} part en arc (arc 60) jusqu'à PRIME_SOL (move 550,
  x BON_MOIS_K) en passant devant le pied de la colonne ; `stroke` RED -> INK. `lower`. « reviennent » :
  {cal1..3} pop en rang (stagger 3). « chaque » : {cal1} seul `fill` PAPER -> CYAN (hex, 9 images).
- S10 « Ensuite, » (morph) : {bon_mois}, {cal1..3}, {chaque_mois} se réduisent ; {revenus} -> COL_RANGE
  x COL_RANGE_K (move 550) ; {charges} -> PILE_S10 x1 (move 550). « part » : « Toi » GARDE le bras baissé
  (hold_low) ; {piece1..3} pop en PIECES_DEPART puis volent en arc (S.fly ou move arc 60, 14 images, stagger 3)
  vers les centres monde de {loyer}, {factures}, {credits} et s'y réduisent (vanish into le bloc) ; chaque bloc
  bat (x1,06) à l'arrivée de sa pièce. « dépenses. » : APRÈS seulement, c.toi.reach vers PANIER_S10_TIP et {panier}
  pop à la pointe (from_pt = c.toi.tip(f + …)) : il arrive après les charges.
- S11 « Deuxième » : kit.step(f, 1) et `done0` 0 -> 1 ; {panier} vanish into la pointe ; `lower`. « liste » :
  walk_low vers P3. « loyer » : c.toi.trace(f, [(TRACE_X, y) pour y du loyer, des factures, des crédits]) (points
  monde : S.to_world("charges", (165, BLOC_LOCAL[...][1]), f) ; vérifier assert_reach(P3[0], …) sur chacun, le plus
  haut à y 870 : COCHES_LOCAL) ; {coche1..3} (enfants de {charges}, coches PLEINES deep) se tracent sous la pointe
  (kit.draw(c, hit, 6)). « abonnements. » : {abonnements} tombe de ABOS_CHUTE_H px sur les crédits, en
  BLOC_LOCAL["abonnements"] (kit.drop) ; `lower` (le bras redescend avant ou pendant la chute).
- S12 « Ouvre » : {charges} -> PILE_S12 x PILE_S12_K (move 550) ; {releve1..3} naissent du haut de la pile (pop
  from_pt monde, stagger 3) et s'ouvrent en éventail vers RELEVE_C ; walk_low vers P2. « 3 ? » : {trois} pop en
  TROIS_C ; les relevés sautent l'un après l'autre (stagger 4 : move -16 px en y et retour, ou pulse x1,08).
- S13 « tromper : » : {trois} vanish ; {barre1..3} montent depuis 0 jusqu'à BARRES_H (clés `h` ET `pos`
  [0, BARRE_BAS - h/2] ensemble, 10 images « out », stagger 3). « facture » : {rouge1} `scale` 1 (posé sur le haut de
  barre1) puis `fill` PAPER -> RED (hex, 9) ; {piege1} pop. « sans » : {prime_mini} pop (au-dessus de barre2),
  {prime_mini_barre} se trace (draw 6), puis {prime_mini} tombe hors du relevé (kit.drop out=True) ; {piege2} pop.
  « dépense » : {vide3} pop (rectangle vide en tirets rouges sur barre3) ; {piege3} pop. Tenue lisible ≥ 1 s.
- S14 « moyenne » : {moyenne_ligne} se trace (draw 9) à y 610 ; {moyenne_titre} pop. « 3 » : les trois barres
  prennent BARRE_MOY (h et pos ensemble, move 550 « inOut ») ; {rouge1} tombe (kit.drop out) ; {vide3} se réduit
  pendant que barre3 monte dans sa place ; {piege1..3} se réduisent. « base » : {moyenne_titre}, {moyenne_ligne},
  puis {releve1..3} rentrent dans la pile (vanish into « charges », stagger 3) ; {charges} -> PILE_S10 x1 (move
  550). « honnête. » : c.toi.tap(f - TAP + 1, CHARGES_TAP) (assert_reach(P2[0])) ; au contact {mot_charges} pop.
  `lower`. Tenue.

PASSAGE À p3 (image 1805 = ENTRY_P3 de __init__, à respecter exactement) : revenus en COL_RANGE x0,4 (salaire,
allocations, autres, socle sx 1, mot_salaire en MOT_SALAIRE_NET_LOCAL, net écrit et souligné, mot_revenus ;
chaque_mois et reste à 0) ; charges en PILE_S10 x1 avec les 4 blocs, coches tracées, mot_charges ; pastille « ? € »
en PASTILLE_ATTENTE x0,85 ; marqueur on 1, active 1, done0 1 ; relevés, barres, pièges, trois, moyenne, prime,
calendriers, plus, pièces, panier à 0 ; « Toi » en P2, bras baissé. Tout ce qui commence ici finit avant 1806.

Règles : bras baissé entre deux gestes ; jamais de clé ni d'épingle sur la figurine ; rouge seulement pour la Prime
(S09, aussitôt écartée) et les trois pièges (S13, effacés en S14) ; aucune coche variant « ai » (pas d'IA) ; aucun
gris ; dates ni montants inventés (aucun chiffre sur les relevés).
"""
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, SCALE, STRETCH  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401

from . import *  # noqa: F401,F403
from . import (ABOS_CHUTE_H, ALLOC_ENTREE, ALLOC_LOCAL, AUTRES_LOCAL, BARRE_BAS, BARRE_MOY, BARRES, BARRES_H,
               BLOC_LOCAL, BON_MOIS_ATTENTE, BON_MOIS_K, BON_MOIS_SOMMET, CALENDRIERS, CHARGES_TAP, COCHES,
               COCHES_LOCAL, COL_RANGE, COL_RANGE_K, COL_S07, CYAN, ENTRY_P2, INK, MOT_SALAIRE_NET_LOCAL, P1, P2, P3,
               PANIER_S10_TIP, PASTILLE_ATTENTE, PASTILLE_ATTENTE_K, PIECES, PIECES_DEPART, PIEGES_LBL,
               PILE_RANGE_K, PILE_RANGE_S07, PILE_S10, PILE_S12, PILE_S12_K, PLUS_C, PLUS_HAUT, PRIME_COLLE,
               PRIME_SOL, PRIME_TAP, RED, RELEVE_C, RELEVES, REVENUS_TAP, T_NET, T_PRIME, TRACE_X, assert_reach,
               lower, scene_f0, walk_low)

# S07 « mois. » : le bon mois glisse du sommet vers la droite, puis tombe le long du flanc droit de la colonne
BON_MOIS_BORD = (720, 592)                      # au bord droit du sommet (colonne x 330-630, haut y 620)
AUTRES_ENTREE = (ALLOC_ENTREE[0], 490)          # S08 : « Autres revenus » entre par la droite (10 px plus bas : passe sous la pastille)
PLUS_DANS_COLONNE = (480, 540)                  # S08 « autres » : le « + » rentre dans le haut de la colonne
PIECE_CIBLE_X = 570                             # S10 : les pièces entrent dans la partie droite de chaque bloc
PILE_HAUT_S12 = (480, 980)                      # S12 : les relevés sortent du haut de la pile réduite
PILE_ENTREE_S14 = (480, 760)                    # S14 : titre et relevés rentrent dans le haut de la pile
RELEVE_HOP = 16                                 # S12 « 3 ? » : saut des relevés (px)


def _r(pt):
    return [round(pt[0], 3), round(pt[1], 3)]


def _bar(S, bid, f, h, d, e):
    """Barre d'un relevé (rect posé sur y local BARRE_BAS) : pistes h et pos ensemble, le bas reste fixe."""
    S.key(bid, "h", f, h, d, e)
    S.key(bid, "pos", f, [0, BARRE_BAS - h / 2], d, e)
    return f + d


def part(S, kit, c):
    toi = c.toi
    f0 = scene_f0(S, "S07")
    kit.pin(f0 - 1, ENTRY_P2)
    if S.val("toi", "scale", f0 - 1) == 0:      # partie construite seule : la figurine n'est pas entrée
        toi.enter(f0 - 10, at=list(P1))
        lower(toi, f0 - 1, d=1)

    # ================= S07 : une base fiable, pas un bon mois =================
    f = kit.at("S07", "Pourquoi", "les charges se rangent en petit à gauche ; la colonne de salaire glisse au centre, "
                                  "toute en argent ; partie cyan, légende, accolades, « = », cadenas et trait se "
                                  "réduisent ; la pastille « ? € » monte attendre en haut à droite")
    kit.move("charges", f, list(PILE_RANGE_S07), scale=PILE_RANGE_K)
    kit.move("revenus", f, list(COL_S07))
    kit.move("pastille", f, list(PASTILLE_ATTENTE), scale=PASTILLE_ATTENTE_K)
    kit.morph(["reste", "legende_reste", "acc_revenus", "acc_charges", "egal", "cadenas"], [], f)
    for pid in ("accolade_g", "accolade_d", "ligne_partie"):
        S.key(pid, "draw", f, 0, MORPH, "in")
        kit.vanish(pid, f, d=MORPH)

    f = kit.at("S07", "revenus ?", "« Toi » s'approche de la colonne à petits sauts, bras baissé ; son nom le suit")
    walk_low(toi, f, P2[0])

    f = kit.at("S07", "base", "un socle encre s'étire sous la colonne ; « chaque mois » s'écrit dans son bas")
    S.key("socle", "sx", f, 1, STRETCH, "out")
    S.key("chaque_mois", "scale", f + 6, 1)
    kit.type("chaque_mois", f + 6)

    f = kit.at("S07", "bon", "un bloc en tirets « bon mois » surgit sur le sommet de la colonne")
    kit.pop("bon_mois", f)

    f = kit.at("S07", "mois.", "le bloc « bon mois » vacille, glisse du sommet et tombe le long du flanc droit de "
                               "la colonne jusqu'à une place à part, à droite : il ne tient pas")
    S.key("bon_mois", "rot", f, 6, 2, "out")
    S.key("bon_mois", "rot", f + 2, -6, 3, "inOut")
    S.key("bon_mois", "rot", f + 5, 0, 3, "inOut")
    g = f + 8
    S.key("bon_mois", "pos", g, list(BON_MOIS_BORD), 5, "in")
    S.key("bon_mois", "rot", g, 12, 5, "in")
    S.key("bon_mois", "scale", g, BON_MOIS_K, 13, "inOut")
    S.key("bon_mois", "pos", g + 5, list(BON_MOIS_ATTENTE), 8, "in")
    S.key("bon_mois", "rot", g + 5, 0, 8, "inOut")
    assert g + 13 <= scene_f0(S, "S08")

    # ================= S08 : étape 1, additionner les revenus fixes =================
    f = kit.at("S08", "Première", "repère : le disque « 1 » grandit en disque cyan, légende « Revenus »")
    S.key("marqueur", "on", f, 1, POP, "out")

    f = kit.at("S08", "additionne", "un « + » deep surgit au sommet de la colonne, là où le bon mois n'a pas tenu")
    kit.pop("plus", f)

    f = kit.at("S08", "net,", "« Salaire » glisse à gauche ; « net » s'écrit après lui, puis se souligne")
    kit.move("mot_salaire", f, list(MOT_SALAIRE_NET_LOCAL), d=6, e="out")
    g = kit.type("net", f + 4, n=len(T_NET), rate=1)
    kit.draw("net", g, 8, track="under")

    f = kit.at("S08", "allocations", "le bloc « Allocations » entre par la droite et se pose sur le haut de la "
                                     "colonne ; le « + » remonte au-dessus")
    S.key("allocations", "pos", f - 1, _r(S.parent_space("allocations", ALLOC_ENTREE, f - 1)))
    kit.pop("allocations", f, d=6)
    kit.move("allocations", f, list(ALLOC_LOCAL))
    kit.move("plus", f, list(PLUS_HAUT))

    f = kit.at("S08", "autres", "le bloc « Autres revenus » entre par la droite et se pose sur les allocations ; "
                                "le « + » rentre dans la colonne : 740 px d'un seul tenant")
    S.key("autres", "pos", f - 1, _r(S.parent_space("autres", AUTRES_ENTREE, f - 1)))
    kit.pop("autres", f, d=6)
    kit.move("autres", f, list(AUTRES_LOCAL))
    kit.vanish("plus", f, into=list(PLUS_DANS_COLONNE))

    f = kit.at("S08", "fixes.", "« Toi » touche du stylo le bord droit de la colonne : « Revenus » surgit au pied")
    assert_reach(P2[0], REVENUS_TAP, "S08 colonne")
    hit = toi.tap(f - TAP + 1, list(REVENUS_TAP))
    kit.pop("mot_revenus", hit)
    lower(toi, hit + 6)

    # ================= S09 : la prime, mise de côté =================
    f = kit.at("S09", "primes", "le bloc en attente devient « Prime » et bat une fois")
    S.key("bon_mois_mot", "opacity", f, 0, 3, "in")
    S.key("bon_mois_mot", "text", f + 3, T_PRIME)
    S.key("bon_mois_mot", "opacity", f + 3, 1, FADE, "out")
    kit.pulse("bon_mois", f, peak=round(BON_MOIS_K * 1.12, 4))

    f = kit.at("S09", "exceptionnelles ?", "la « Prime » glisse se coller au flanc de la colonne et son contour "
                                           "vire au rouge : l'erreur")
    kit.move("bon_mois", f, list(PRIME_COLLE), d=14)
    S.key("bon_mois", "stroke", f, RED, 9, "out")

    f = kit.at("S09", "Laisse-les", "« Toi » touche la Prime du stylo : elle part en arc devant le pied de la colonne "
                                    "et se pose au sol à gauche ; son contour redevient encre")
    assert_reach(P2[0], PRIME_TAP, "S09 prime")
    hit = toi.tap(f - TAP + 1, list(PRIME_TAP))
    kit.move("bon_mois", hit, list(PRIME_SOL), arc=60)
    S.key("bon_mois", "stroke", hit, INK, 9, "out")
    lower(toi, hit + 6)

    f = kit.at("S09", "reviennent", "trois calendriers surgissent en rang au-dessus de la Prime")
    kit.stagger(CALENDRIERS, f, 3, kit.pop)

    f = kit.at("S09", "chaque", "seul le premier calendrier passe au cyan : la prime ne revient pas chaque mois")
    S.key("cal1", "fill", f, CYAN, 9, "out")

    # ================= S10 : les charges se servent avant toi =================
    f = kit.at("S10", "Ensuite,", "la Prime, ses calendriers et « chaque mois » se réduisent ; les revenus se rangent "
                                  "en petit à gauche, la pile des charges revient en grand au centre")
    kit.morph(["bon_mois", *CALENDRIERS, "chaque_mois"], [], f)
    kit.move("revenus", f, list(COL_RANGE), scale=COL_RANGE_K)
    kit.move("charges", f, list(PILE_S10), scale=1)

    f = kit.at("S10", "part", "bras de « Toi » baissé, trois pièces quittent seules le haut des revenus et volent en "
                              "arc dans le loyer, les factures et les crédits ; chaque bloc bat en recevant la sienne")
    for k, (pid, bid) in enumerate(zip(PIECES, ("loyer", "factures", "credits"))):
        g = f + 3 * k
        S.key(pid, "pos", g - 1, list(PIECES_DEPART))
        kit.pop(pid, g, d=6)
        y = S.to_world("charges", BLOC_LOCAL[bid], g)[1]
        arr = kit.move(pid, g + 3, [PIECE_CIBLE_X, round(y, 3)], d=13, arc=80)
        kit.vanish(pid, arr, d=5)
        kit.pulse(bid, arr, peak=1.06)

    f = kit.at("S10", "dépenses.", "après seulement, « Toi » lève le stylo : le panier de courses ressort à sa pointe, "
                                   "l'argent des charges est déjà parti")
    assert_reach(P2[0], PANIER_S10_TIP, "S10 panier")
    toi.reach(f, list(PANIER_S10_TIP), d=10)
    kit.pop("panier", f + 5, from_pt=_r(toi.tip(f + 4)), to=list(PANIER_S10_TIP), d=6)

    # ================= S11 : étape 2, la liste des charges fixes =================
    f = kit.at("S11", "Deuxième", "le repère passe à l'étape 2 « Charges », le 1 garde sa coche ; le panier rentre "
                                  "dans le stylo, le bras redescend")
    kit.step(f, 1)
    S.key("marqueur", "done0", f + 6, 1, DRAW, "out")
    kit.vanish("panier", f, into=_r(toi.tip(f - 1)), d=6)
    lower(toi, f + 6)

    f = kit.at("S11", "liste", "« Toi » s'approche de la pile, bras baissé")
    walk_low(toi, f, P3[0])

    f = kit.at("S11", "loyer", "la pointe du stylo remonte le bord droit de la pile : une coche pleine deep se trace "
                               "sous elle à côté du loyer, des factures, des crédits")
    pts = [[TRACE_X, round(S.to_world("charges", COCHES_LOCAL[k], f)[1], 3)] for k in range(3)]
    for k, pt in enumerate(pts):
        assert_reach(P3[0], pt, f"S11 coche {k + 1}")
    hits = toi.trace(f, pts)
    for cid, h in zip(COCHES, hits):
        kit.draw(cid, h, 6)

    f = kit.at("S11", "abonnements.", "le bloc « Abonnements » tombe d'en haut sur les crédits : la liste est "
                                      "complète ; le bras redescend")
    kit.drop("abonnements", f, h=ABOS_CHUTE_H)
    lower(toi, max(f, hits[-1] + 1))

    # ================= S12 : trois relevés =================
    f = kit.at("S12", "Ouvre", "la pile des charges se réduit en bas au centre ; trois relevés en sortent et "
                               "s'ouvrent en éventail ; « Toi » recule d'un pas")
    kit.move("charges", f, list(PILE_S12), scale=PILE_S12_K)
    for bid in BARRES:                          # barres à h 0 : cachées (sinon un trait au bas du relevé)
        S.key(bid, "scale", f - 1, 0)
    for k, rid in enumerate(RELEVES):
        kit.pop(rid, f + 3 * k, from_pt=list(PILE_HAUT_S12), to=list(RELEVE_C[k]), d=14)
    walk_low(toi, f, P2[0])

    f = kit.at("S12", "3 ?", "un grand « 3 » surgit au-dessus des relevés, qui sautent l'un après l'autre : un, "
                             "deux, trois")
    kit.pop("trois", f)
    for k, rid in enumerate(RELEVES):
        g = f + 3 + 4 * k
        x, y = RELEVE_C[k]
        S.key(rid, "pos", g, [x, y - RELEVE_HOP], 4, "out")
        S.key(rid, "pos", g + 4, [x, y], 4, "inOut")

    # ================= S13 : un seul mois peut tromper =================
    f = kit.at("S13", "tromper :", "le « 3 » se réduit ; dans chaque relevé une barre de dépenses monte : trois "
                                   "hauteurs différentes")
    kit.vanish("trois", f)
    for k, bid in enumerate(BARRES):
        S.key(bid, "scale", f + 3 * k, 1)
        _bar(S, bid, f + 3 * k, BARRES_H[k], 10, "out")

    f = kit.at("S13", "facture", "mois 1 : le haut de la barre vire au rouge ; « facture annuelle » en rouge dessous")
    S.key("rouge1", "scale", f, 1)
    S.key("rouge1", "fill", f, RED, 9, "out")
    kit.pop(PIEGES_LBL[0], f + 2)

    f = kit.at("S13", "sans", "mois 2 : un petit bloc « Prime » surgit, un trait rouge le barre et il tombe hors du "
                              "relevé ; « sans prime » en rouge dessous")
    kit.pop("prime_mini", f)
    g = kit.draw("prime_mini_barre", f + 6, 6)
    kit.drop("prime_mini", g + 1, out=True, h=110, dx=90, rot=30)
    kit.pop(PIEGES_LBL[1], g + 1)

    f = kit.at("S13", "dépense", "mois 3 : un morceau manque en haut de la barre, en tirets rouges ; « dépense "
                                 "oubliée » en rouge dessous ; tenue")
    kit.pop("vide3", f)
    kit.pop(PIEGES_LBL[2], f + 2)

    # ================= S14 : la moyenne sur 3 mois =================
    f = kit.at("S14", "moyenne", "un trait deep se trace en travers des trois relevés ; « moyenne sur 3 mois » "
                                 "surgit au-dessus")
    kit.draw("moyenne_ligne", f, DRAW)
    kit.pop("moyenne_titre", f + 3)

    f = kit.at("S14", "3", "les trois barres s'égalisent sur le trait : le rouge du mois 1 tombe, la barre du mois 3 "
                           "monte dans le morceau manquant ; les légendes rouges se réduisent")
    for bid in BARRES:
        _bar(S, bid, f, BARRE_MOY, MOVE, "inOut")
    kit.drop("rouge1", f, out=True, h=80, dx=-80, rot=-30)
    kit.vanish("vide3", f, d=MOVE, e="inOut")
    kit.stagger(PIEGES_LBL, f + 4, 2, kit.vanish)

    f = kit.at("S14", "base", "le titre, le trait et les trois relevés rentrent dans la pile des charges, qui "
                              "reprend sa taille au centre")
    kit.vanish("moyenne_titre", f, into=list(PILE_ENTREE_S14), d=10)
    S.key("moyenne_ligne", "draw", f, 0, 6, "in")
    kit.stagger(RELEVES, f + 2, 3, kit.vanish, into=list(PILE_ENTREE_S14), d=10)
    kit.move("charges", f, list(PILE_S10), scale=1)

    f = kit.at("S14", "honnête.", "« Toi » touche du stylo le bord droit de la pile : « Charges » surgit au pied")
    assert_reach(P2[0], CHARGES_TAP, "S14 pile")
    hit = toi.tap(f - TAP + 1, list(CHARGES_TAP))
    kit.pop("mot_charges", hit)
    end = lower(toi, hit + 6)
    assert end < scene_f0(S, "S15"), end
