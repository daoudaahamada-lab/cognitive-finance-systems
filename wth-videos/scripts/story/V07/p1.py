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
import math

from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, SCALE  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401

from . import *  # noqa: F401,F403
from . import (BULLE_RONDS, COUVERCLE_TAP, DEEP, ETIQ_C, ETIQ_TAP, FRAIS_ETF_C, FRAIS_GA_C, HEAD_DY, LIVRE_C,
               LIVRE_RANGE, LIVRE_RANGE_K, MARKER_CX, MARKER_Y, MINI_LOCAL, MINI_R, NB_TITRES_C, P1, PANIER_C,
               QUESTION_BULLE, QUESTION_GS, QUESTION_NEE, SLIDE_DX, TITRE_R, TITRE_TOMBE, TITRES_LOCAL, TOI_NOM_C,
               assert_reach, lower)

# ---------- places propres à p1 ----------
PAY_TIP = (540, 930)            # S01 : pointe levée vers le panier, d'où part la pièce de l'achat
FRAIS_TIP = (550, 920)          # S06 : pointe levée d'où partent les pièces des frais
LID_IN = (360, 872)             # S01, S04 : point d'entrée sur le couvercle (au-dessus du bouton, à droite)
LID_FLY_LOCAL = (300, -330)     # S05 : le couvercle s'envole vers le haut à droite (monde 640, 680)
HEAD_PT = (P1[0], P1[1] + HEAD_DY)   # tête de « Toi » (660, 1071)
T8_OUT_LOCAL = (-255, 75)       # S08 : titre8 saute hors du panier, à gauche (monde 85, 1085)
QUESTION_K_BULLE = 70 / QUESTION_GS
QUESTION_K_DANS = 110 / QUESTION_GS
PRE = 8                         # images de levée du stylo avant un tapotement (le tap seul n'a que 5 images)

M_DIVERSIFIE = "diversifié. »"
M_INDICE_Q = "l’indice ?"
M_INDICE = "l’indice."


def part(S, kit, c):
    toi = c.toi
    titres = c.titres

    # ---------- état d'entrée (image 0 = distribution) : épinglé à -1 ----------
    kit.pin(0 - 1, {
        "panier": {"pos": list(PANIER_C), "scale": 1},
        "panier_couvercle": {"scale": 1},
        "etiquette": {"pos": list(ETIQ_C), "scale": 1, "rot": 0},
        "ficelle_etiq": {"draw": 1},
        "toi_nom": {"opacity": 1},
        "livre": {"pos": list(LIVRE_C), "scale": 0},
        "marqueur": {"pos": [MARKER_CX, MARKER_Y], "scale": 0, "on": 0, "active": 0, "lbl": 0},
        "question": {"scale": 0},
        "bulle": {"scale": 0},
    })
    if S.val(toi.id, "scale", -1) == 0:          # partie construite seule après une sortie : sans effet ici
        toi.enter(0, at=list(P1))

    for pt, what in ((PAY_TIP, "S01 pièce"), (COUVERCLE_TAP, "S02-S05 couvercle"),
                     ((COUVERCLE_TAP[0], COUVERCLE_TAP[1] - 14), "S03 couvercle levé"),
                     (FRAIS_TIP, "S06 frais"), (ETIQ_TAP, "S09 étiquette")):
        assert_reach(P1[0], pt, what)

    def tap_on(f_word, target):
        """Le stylo se lève au-dessus de la cible, puis la touche sur l'image du mot (contact = f_word)."""
        g = f_word - TAP + 1
        toi.reach(g - PRE, [target[0], target[1] - 14], d=PRE)
        return toi.tap(g, target)

    # ================= S01 : « J’ai acheté un ETF, donc je suis diversifié. » =================
    f = kit.at("S01", "acheté", "« Toi » lève le stylo vers le panier ; une pièce « € » naît de la pointe, vole en "
                                "arc jusqu'au couvercle et s'y réduit ; le couvercle tressaute, l'étiquette « ETF "
                                "Monde » et le panier battent ensemble")
    toi.reach(f - 6, PAY_TIP, d=7)
    kit.pop("piece", f, from_pt=PAY_TIP, to=PAY_TIP, d=6)
    g = kit.move("piece", f + 4, LID_IN, d=13, arc=60)
    g = kit.vanish("piece", g, into="panier_couvercle", d=6)
    kit.shake("panier_couvercle", g - 2, amp=4, axis="y")
    kit.pulse("etiquette", g - 2, peak=1.08)
    kit.pulse("panier", g - 2, peak=1.08)
    lower(toi, f + 8, 10)

    f = kit.at("S01", "donc", "trois petits cercles en tirets montent de la tête de « Toi », l'un après l'autre")
    for k in range(3):
        kit.pop(f"bulle_rond{k + 1}", f + 2 * k, from_pt=HEAD_PT, to=BULLE_RONDS[k][0])

    f = kit.at("S01", M_DIVERSIFIE, "la bulle de pensée s'ouvre ; « diversifié » s'y écrit, puis la coche pleine "
                                    "(cyan profond, celle de « Toi ») se trace : il en est sûr")
    kit.pop("bulle", f)
    g = kit.type("bulle_texte", f + 3, rate=2)
    kit.draw("bulle_coche", g + 1, DRAW)

    # ================= S02 : « Tu le penses aussi ? Pas si vite. » =================
    f = kit.at("S02", "penses", "la bulle « diversifié ✓ » et le nom « Toi » battent sur la même image")
    kit.pulse("bulle", f, peak=1.08)
    kit.pulse("toi_nom", f, peak=1.08)

    f = kit.at("S02", "Pas", "le stylo de « Toi » touche le bout droit du couvercle fermé ; un « ? » en naît sous la "
                             "pointe et s'arrête juste au-dessus")
    hit = tap_on(f, COUVERCLE_TAP)
    kit.pop("question", hit, from_pt=COUVERCLE_TAP, to=QUESTION_NEE)

    f = kit.at("S02", "vite.", "la coche de la bulle se détache et tombe ; le « ? » vole en arc dans la bulle à sa "
                               "place : « diversifié ? »")
    kit.drop("bulle_coche", f, out=True, h=52, dx=18, rot=35)
    kit.move("question", f, QUESTION_BULLE, d=MOVE, arc=60, scale=QUESTION_K_BULLE)
    lower(toi, f + 2, 10)

    # ================= S03 : « Dans cette vidéo, on va voir trois erreurs … ce que tu achètes vraiment. » ========
    f = kit.at("S03", "Dans", "la bulle et ses trois cercles se réduisent dans le « ? », qui reste seul et grandit")
    kit.vanish("bulle", f, into="question")
    for k in range(3):
        kit.vanish(f"bulle_rond{k + 1}", f, into="question")
    S.key("question", "scale", f + 4, QUESTION_K_DANS, SCALE, "out")

    f = kit.at("S03", "trois", "le « ? » monte en haut de l'image et s'y change en trois disques numérotés 1-2-3 "
                               "(aucun allumé)")
    kit.move("question", f, [MARKER_CX, MARKER_Y + 30], d=10, e="out")
    kit.morph("question", "marqueur", f + 5)

    f = kit.at("S03", "erreurs", "le titre « 3 erreurs » surgit au-dessus des disques ; leurs légendes « Indice », "
                                 "« Poids », « Doublons » entrent en fondu dessous")
    kit.pop("titre_erreurs", f)
    S.key("marqueur", "lbl", f + 4, 1, FADE, "out")

    f = kit.at("S03", "savoir", "« Toi » lève le stylo vers le couvercle fermé, pointe juste au-dessus de son bout")
    toi.reach(f, [COUVERCLE_TAP[0], COUVERCLE_TAP[1] - 14], d=POP)

    f = kit.at("S03", "achètes", "la pointe touche le couvercle : il tremble mais reste fermé")
    hit = toi.tap(f - TAP + 1, COUVERCLE_TAP)
    kit.shake("panier_couvercle", hit, amp=8, axis="x")
    lower(toi, hit + 6, 10)

    # ================= S04 : « D’abord, un ETF, c’est quoi ? Un fonds coté en Bourse qui cherche à reproduire … » ==
    f = kit.at("S04", "ETF,", "l'étiquette « ETF Monde » et le panier battent ensemble : voici l'ETF")
    kit.pulse("etiquette", f, peak=1.1)
    kit.pulse("panier", f, peak=1.1)

    f = kit.at("S04", "coté", "à droite, un petit graphique en dents de scie se trace de gauche à droite")
    kit.pop("bourse", f, d=6)
    kit.draw("bourse", f, 20, e="linear")

    f = kit.at("S04", "Bourse", "« Bourse » s'écrit au-dessus du graphique")
    kit.type("bourse_mot", f, rate=1)

    f = kit.at("S04", "cherche", "le graphique et « Bourse » se réduisent ; un livre ouvert tombe à gauche, titré "
                                 "« Indice », sa page porte la liste de 10 mini-titres")
    kit.vanish("bourse", f)
    kit.vanish("bourse_mot", f)
    kit.drop("livre", f, h=200)
    kit.fade("livre_titre", f + 6, to=1)

    f = kit.at("S04", "reproduire", "de chaque mini-titre de la page part une copie qui file en arc vers le panier "
                                    "en grandissant et disparaît sous le couvercle, qui tressaute")
    k_big = TITRE_R / MINI_R
    last = f
    for k, cid in enumerate(c.copies):
        fi = f + 2 * k
        src = S.to_world("livre", MINI_LOCAL[k], fi - 1)
        S.key(cid, "pos", fi, [round(v, 3) for v in src])
        S.key(cid, "scale", fi, 1)
        dst = [LID_IN[0] - 80 + 18 * k, LID_IN[1]]
        g = kit.move(cid, fi + 1, dst, d=MOVE, arc=80, scale=k_big)
        last = kit.vanish(cid, g, into="panier_couvercle", d=6)
    kit.shake("panier_couvercle", last - 4, amp=4, axis="y")

    # ================= S05 : « Tu achètes en une fois tout un panier de titres. » =================
    f = kit.at("S05", "achètes", "le stylo de « Toi » touche le bout droit du couvercle")
    hit = tap_on(f, COUVERCLE_TAP)
    lower(toi, hit + 6, 10)

    f = kit.at("S05", "fois", "le couvercle s'envole en arc vers le haut à droite et disparaît ; les 10 titres "
                              "surgissent tous ensemble au-dessus du rebord : le panier est ouvert")
    S.key("panier_couvercle", "pos", f, list(LID_FLY_LOCAL), MORPH, "out", 60)
    S.key("panier_couvercle", "scale", f, 0, MORPH, "in")
    S.key("panier_couvercle", "opacity", f + MORPH, 0)
    for t in titres:
        kit.pop(t, f)

    f = kit.at("S05", "panier", "le panier et ses 10 titres battent ensemble")
    kit.pulse("panier", f, peak=1.06)

    f = kit.at("S05", "titres.", "les titres battent l'un après l'autre de gauche à droite pendant que le compteur "
                                 "« 10 titres » surgit et monte de 1 à 10")
    order = sorted(range(10), key=lambda k: TITRES_LOCAL[k][0])
    for i, k in enumerate(order):
        kit.pulse(titres[k], f + 2 * i, peak=1.2)
    kit.pop("nb_titres", f)
    S.key("nb_titres", "value", f, 10, 2 * 9 + 3, "linear")

    # ================= S06 : « Et en général, avec des frais plus bas qu’un fonds géré activement. » =============
    f = kit.at("S06", "Et", "le livre se range en petit en haut à gauche ; « 10 titres » se réduit")
    kit.move("livre", f, list(LIVRE_RANGE), d=MOVE, scale=LIVRE_RANGE_K)
    kit.fade("livre_titre", f, to=0)             # « Indice » à x0,55 ferait 20 px : illisible, il revient avec le livre
    kit.vanish("nb_titres", f)

    f = kit.at("S06", "frais", "« frais » paraît ; « Toi » lève le stylo et une pièce cyan en part, vole se poser en "
                               "haut, légendée « ETF »")
    kit.fade("frais_mot", f, to=1)
    toi.reach(f - 4, FRAIS_TIP, d=7)
    kit.pop("frais_etf", f + 2, from_pt=FRAIS_TIP, to=FRAIS_TIP, d=5)
    kit.move("frais_etf", f + 5, list(FRAIS_ETF_C), d=13, arc=60)
    kit.fade("frais_etf_lbl", f + 12, to=1)

    f = kit.at("S06", "géré", "légende « gestion active » ; quatre pièces grises partent du stylo l'une après "
                              "l'autre et se posent en rang sous la pièce de l'ETF")
    kit.fade("frais_ga_lbl", f, to=1)
    end = f
    for k, cid in enumerate(c.frais_ga):
        fi = f + 3 * k
        kit.pop(cid, fi, from_pt=FRAIS_TIP, to=FRAIS_TIP, d=4)
        end = kit.move(cid, fi + 3, list(FRAIS_GA_C[k]), d=13, arc=60)

    f = kit.at("S06", "activement.", "la pièce unique de l'ETF bat, seule ; les quatre pièces grises ne bougent pas")
    kit.pulse("frais_etf", f, peak=1.15)
    lower(toi, end, 10)

    # ================= S07 : « Mais ce panier dépend entièrement de l’indice. » =================
    f = kit.at("S07", "Mais", "la pièce cyan rentre dans l'étiquette « ETF Monde » ; les pièces grises, les légendes "
                              "et « frais » se réduisent ; le livre revient à sa place en grand")
    kit.vanish("frais_etf", f, into="etiquette")
    kit.morph([*c.frais_ga, "frais_etf_lbl", "frais_ga_lbl", "frais_mot"], [], f)
    kit.move("livre", f, list(LIVRE_C), d=MOVE, scale=1)
    kit.fade("livre_titre", f + MOVE - FADE, to=1)

    f = kit.at("S07", "dépend", "une ficelle encre se trace du bas du livre au bord gauche du panier")
    g = kit.draw("ficelle", f, DRAW)
    S.key("ficelle_halo", "draw", g, 1)          # doublon épais, invisible (opacité 0) jusqu'à « décide »

    f = kit.at("S07", "entièrement", "le livre glisse de 60 px à droite et le panier, ses titres et son étiquette "
                                     "glissent exactement avec lui, ficelle tendue, sans mouvement vertical")
    for i in ("livre", "panier", "etiquette"):
        x, y = S.val(i, "pos", f - 1)
        kit.move(i, f, [x + SLIDE_DX, y], d=MOVE)

    f = kit.at("S07", M_INDICE, "le livre revient à gauche, le panier avec lui ; à l'arrêt, les mini-titres de la "
                                "page et les titres du panier battent sur la même image : la même liste")
    for i, home in (("livre", LIVRE_C), ("panier", PANIER_C), ("etiquette", ETIQ_C)):
        g = kit.move(i, f, list(home), d=MOVE)
    for i in [*c.minis, *titres]:
        kit.pulse(i, g, peak=1.15)

    # ================= S08 : « Pourquoi commencer par l’indice ? Parce que c’est lui qui décide … » =============
    f = kit.at("S08", M_INDICE_Q, "le livre bat et son titre « Indice » se souligne ; le nom « Toi » s'efface")
    kit.pulse("livre", f, peak=1.08)
    kit.draw("livre_titre", f, DRAW, track="under")
    kit.fade("toi_nom", f, to=0)

    f = kit.at("S08", "décide", "un mini-titre disparaît de la page du livre et la ficelle bat ; aussitôt le titre "
                                "correspondant saute hors du panier et tombe à côté")
    t8, m8 = titres[TITRE_TOMBE], c.minis[TITRE_TOMBE]
    kit.vanish(m8, f)
    kit.pulse("ficelle_halo", f, peak=1, step=4, track="opacity")
    g = f + 6
    S.set(t8, z=5.5)
    S.key(t8, "z", g, 6.9)                       # il saute PAR-DESSUS le rebord (z 6), pas à travers
    S.key(t8, "pos", g, list(T8_OUT_LOCAL), 14, "inOut", 140)
    S.key(t8, "rot", g, -30, 14, "out")

    f = kit.at("S08", "possèdes.", "un nouveau mini-titre surgit sur la page ; un nouveau titre sort du livre, "
                                   "glisse le long de la ficelle et saute à la place libre du panier")
    kit.pop("mini_neuf", f)
    a_end = S.wire_cubic("ficelle", f)[3]
    place = S.to_world("panier", TITRES_LOCAL[TITRE_TOMBE], f)

    def offset(p):
        q = min(1.0, max(0.0, (p - 0.55) / 0.45))
        qe = q * q * (3 - 2 * q)
        return [(place[0] - a_end[0]) * qe, (place[1] - a_end[1]) * qe - 70 * math.sin(math.pi * q)]

    S.along_wire("titre_neuf", "ficelle", f, 24, "inOut", 0, 1, f, offset=offset, scale=1)
    S.key("titre_neuf", "pos", f + 24, list(TITRES_LOCAL[TITRE_TOMBE]))
    kit.vanish(t8, f + 26)                       # le titre tombé s'en va une fois l'autre arrivé

    # ================= S09 : « Première erreur : ne pas le lire. » =================
    f = kit.at("S09", "Première", "le disque 1 « Indice » du repère s'allume en cyan, sous « 3 erreurs »")
    S.key("marqueur", "on", f, 1, POP, "out")

    f = kit.at("S09", "ne", "le stylo de « Toi » touche l'étiquette « ETF Monde », qui bat : il ne lit que le nom")
    hit = tap_on(f, ETIQ_TAP)
    kit.pulse("etiquette", hit, peak=1.08)
    lower(toi, hit + 5, 8)

    f = kit.at("S09", "lire.", "« Toi » tourne la tête à droite, dos au livre ; derrière lui le livre bat deux fois ; "
                               "il ne se retourne pas")
    kit.ensure("toi", "look", 0)
    S.key("toi", "look", f, 1, 4, "out")
    kit.pulse("livre", f + 2, times=2, peak=1.1, step=4)
