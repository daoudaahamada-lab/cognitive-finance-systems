"""V07, partie 1 : S01-S09, images 0-1044 (accroche, annonce, contexte, erreur 1 allumée). 34 temps forts, 34,8 s.

ÉTAT D'ENTRÉE (image 0 = distribution, à épingler à -1) : ivoire quadrillé ; au centre gauche le `panier` FERMÉ
x 1,3 (corps 340, 980 ; `panier_couvercle` et son `panier_bouton`) ; sur son devant l'`etiquette` cyan « ETF Monde »
x 1,3 (340, 1032) pendue au rebord par `ficelle_etiq` ; à droite « Toi » (`c.toi`, x 1,15, bras gauche) en P1
(760, 1121), bras BAISSÉ (pose `low_pose`), nommé par `toi_nom` « Toi ». Tout le reste est à l'échelle 0.

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
Gestes secondaires (S.word_after, hors storyboard) : S03 « ETF. »@269, S04 « quoi »@432 et « fonds »@461,
S08 « Parce »@889.

Tour de revue 1 : la pièce de l'achat (S01) et celles des frais (S06) naissent de la POINTE du stylo levé en l'air,
loin du panier, sur un petit coup de stylo ; S07 « Toi » s'écarte (P_ASIDE) et le livre, le panier et l'étiquette
glissent de 180 px aller-retour, la ficelle bat à chaque départ ; S08 le mini-titre et le titre retirés rougissent
4 images, le titre tombe au sol (T8_SOL) et y reste jusqu'à la fin de la scène ; le nouveau titre descend la ficelle
dès le mot en grandissant ; S09 « Toi » revient, touche l'étiquette, se penche vers elle (ligne de regard en tirets)
pendant que le livre, hors de son regard, l'appelle (onde cyan, battements x 1,2, ficelle qui tressaute).
"""
import math

from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, SCALE  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401

from . import *  # noqa: F401,F403
from . import (BULLE_RONDS, COUVERCLE_TAP, ETIQ_C, ETIQ_K, ETIQ_TAP, FRAIS_ETF_C, FRAIS_GA_C, HEAD_PT, LIGHT,
               LIVRE_C, LIVRE_RANGE, LIVRE_RANGE_K, MARKER_CX, MARKER_Y, MINI_LOCAL, MINI_R, NB_TITRES_C, P1,
               P_ASIDE, PANIER_C, PANIER_K, QUESTION_BULLE, QUESTION_GS, QUESTION_NEE, RED, SLIDE_DX, T8_SOL,
               TITRE_R, TITRE_TOMBE, TITRES_LOCAL, TOI_NOM_ASIDE, TOI_NOM_C, BOURSE_C, assert_reach, lean_low,
               lower, ring, walk_low)

# ---------- places propres à p1 ----------
PAY_TIP = (664, 910)            # S01 : pointe levée EN L'AIR, à droite du panier (>= 86 px du couvercle)
FRAIS_TIP = (636, 822)          # S06 : pointe levée vers les rangées des frais
LID_ABOVE = (380, 740)          # S01 : la pièce arrive au-dessus du couvercle…
LID_IN = (380, 812)             # … et y descend
LID_FLY_LOCAL = (300, -330)     # S05 : le couvercle s'envole vers le haut à droite (local panier)
HEAD_TOP = (P1[0] + 14, P1[1] - 96 * 1.15)
QUESTION_K_BULLE = 70 / QUESTION_GS
QUESTION_K_DANS = 110 / QUESTION_GS
PRE = 8                         # images de levée du stylo avant un tapotement (le tap seul n'a que 5 images)

M_DIVERSIFIE = "diversifié. »"
M_INDICE_Q = "l’indice ?"
M_INDICE = "l’indice."


def part(S, kit, c):
    toi = c.toi
    titres = c.titres

    # ---------- état d'entrée (image 0 = distribution) : épinglé à -1 ----------
    kit.pin(0 - 1, {
        "panier": {"pos": list(PANIER_C), "scale": PANIER_K},
        "panier_couvercle": {"scale": 1},
        "etiquette": {"pos": list(ETIQ_C), "scale": ETIQ_K, "rot": 0},
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

    def tap_on(f_word, target, pre=PRE):
        """Le stylo se lève au-dessus de la cible, puis la touche sur l'image du mot (contact = f_word)."""
        g = f_word - TAP + 1
        toi.reach(g - pre, [target[0], target[1] - 14], d=pre)
        return toi.tap(g, target)

    # ================= S01 : « J’ai acheté un ETF, donc je suis diversifié. » =================
    f = kit.at("S01", "acheté", "« Toi » lève le stylo en l'air à droite du panier et donne un petit coup : une "
                                "pièce « € » naît de la pointe, monte en arc et entre dans le couvercle par le "
                                "haut ; le couvercle tressaute, l'étiquette et le panier battent")
    toi.reach(1, [PAY_TIP[0], PAY_TIP[1] - 14], d=5)
    hit = toi.tap(f - TAP + 3, list(PAY_TIP))
    kit.pop("piece", hit, from_pt=list(PAY_TIP), to=[PAY_TIP[0] - 6, PAY_TIP[1] - 34], d=6)
    g = kit.move("piece", hit + 4, list(LID_ABOVE), d=12, arc=60)
    g = kit.vanish("piece", g, into=list(LID_IN), d=6, e="in")
    kit.shake("panier_couvercle", g - 1, amp=5, axis="y")
    kit.pulse("etiquette", g - 1, peak=round(ETIQ_K * 1.06, 4))
    kit.pulse("panier", g - 1, peak=round(PANIER_K * 1.06, 4))
    lower(toi, hit + 6, 10)

    f = kit.at("S01", "donc", "trois cercles en tirets montent de la tête de « Toi », l'un après l'autre")
    for k in range(3):
        kit.pop(f"bulle_rond{k + 1}", f + 2 * k, from_pt=list(HEAD_TOP), to=BULLE_RONDS[k][0])

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
                             "pointe et monte juste au-dessus")
    hit = tap_on(f, COUVERCLE_TAP)
    kit.pop("question", hit, from_pt=list(COUVERCLE_TAP), to=QUESTION_NEE)

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

    g = S.word_after("ETF.", f)                  # « … avec les ETF. » : l'étiquette bat (le repère parle d'elle)
    kit.pulse("etiquette", g, peak=round(ETIQ_K * 1.12, 4))

    f = kit.at("S03", "savoir", "« Toi » lève le stylo vers le couvercle fermé, pointe juste au-dessus de son bout")
    toi.reach(f, [COUVERCLE_TAP[0], COUVERCLE_TAP[1] - 14], d=POP)

    f = kit.at("S03", "achètes", "la pointe touche le couvercle : il tremble mais reste fermé")
    hit = toi.tap(f - TAP + 1, list(COUVERCLE_TAP))
    kit.shake("panier_couvercle", hit, amp=8, axis="x")
    lower(toi, hit + 6, 10)

    # ================= S04 : « D’abord, un ETF, c’est quoi ? Un fonds coté en Bourse qui cherche à reproduire … » ==
    f = kit.at("S04", "ETF,", "l'étiquette « ETF Monde » et le panier battent ensemble : voici l'ETF")
    kit.pulse("etiquette", f, peak=round(ETIQ_K * 1.15, 4))
    kit.pulse("panier", f, peak=round(PANIER_K * 1.15, 4))

    g = S.word_after("quoi", f)                  # « c’est quoi ? » : le couvercle fermé tressaute
    kit.shake("panier_couvercle", g, amp=5, axis="y")
    g = S.word_after("fonds", g)                 # « Un fonds » : le panier et l'étiquette battent
    kit.pulse("etiquette", g, peak=round(ETIQ_K * 1.06, 4))
    kit.pulse("panier", g, peak=round(PANIER_K * 1.06, 4))

    f = kit.at("S04", "coté", "un petit graphique en dents de scie sort de l'étiquette et se trace à droite ; le "
                              "panier monte et descend au rythme des dents : son prix bouge en Bourse")
    kit.pop("bourse", f, from_pt="etiquette", to=list(BOURSE_C), d=8)
    kit.draw("bourse", f + 2, 20, e="linear")
    for k, dy in enumerate((-10, 6, -10, 0)):
        for i, home in (("panier", PANIER_C), ("etiquette", ETIQ_C)):
            S.key(i, "pos", f + 2 + 5 * k, [home[0], home[1] + dy], 5, "inOut")

    f = kit.at("S04", "Bourse", "« Bourse » s'écrit au-dessus du graphique")
    kit.type("bourse_mot", f, rate=1)

    f = kit.at("S04", "cherche", "le graphique et « Bourse » se réduisent ; un livre ouvert tombe à gauche, titré "
                                 "« Indice », sa page porte la liste de 10 mini-titres")
    kit.vanish("bourse", f)
    kit.vanish("bourse_mot", f)
    S.key("livre", "opacity", f - 1, 0)          # le livre (et ses enfants) n'est visible qu'à partir du mot
    kit.drop("livre", f, h=200)
    kit.fade("livre_titre", f + 2, to=1)

    f = kit.at("S04", "reproduire", "les mini-titres de la page battent ; de chacun part une copie qui file en arc "
                                    "vers le panier en grandissant et entre sous le couvercle, qui tressaute")
    for k in range(10):
        kit.pulse(c.minis[k], f + k // 2, peak=1.25, step=2)
    k_big = TITRE_R * PANIER_K / MINI_R
    last = f
    for k, cid in enumerate(c.copies):
        fi = f + 2 * k
        src = S.to_world("livre", MINI_LOCAL[k], fi - 1)
        S.key(cid, "pos", fi - 1, [round(v, 3) for v in src])
        S.key(cid, "scale", fi - 1, 1)
        dst = [250 + 24 * k, 790]
        g = kit.move(cid, fi, dst, d=14, e="out", arc=80, scale=k_big)
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
    kit.pulse("panier", f, peak=round(PANIER_K * 1.06, 4))

    f = kit.at("S05", "titres.", "les titres battent l'un après l'autre de gauche à droite pendant que le compteur "
                                 "« 10 titres » surgit et monte jusqu'à 10")
    order = sorted(range(10), key=lambda k: TITRES_LOCAL[k][0])
    for i, k in enumerate(order):
        kit.pulse(titres[k], f + 2 * i, peak=1.2)
    kit.pop("nb_titres", f)
    S.key("nb_titres", "value", f, 10, 2 * 9 + 3, "linear")

    # ================= S06 : « Et en général, avec des frais plus bas qu’un fonds géré activement. » =============
    f = kit.at("S06", "Et", "le livre se range en petit en haut à gauche ; « 10 titres » se réduit")
    kit.move("livre", f, list(LIVRE_RANGE), d=MOVE, scale=LIVRE_RANGE_K)
    kit.fade("livre_titre", f, to=0)
    kit.vanish("nb_titres", f)

    f = kit.at("S06", "frais", "« frais » paraît ; « Toi » lève le stylo vers le haut et donne un petit coup : une "
                               "pièce cyan part de la pointe et vole se poser en haut, légendée « ETF »")
    kit.fade("frais_mot", f, to=1)
    toi.reach(f - 14, [FRAIS_TIP[0], FRAIS_TIP[1] - 14], d=7)
    hit = toi.tap(f - TAP + 1, list(FRAIS_TIP))
    kit.pop("frais_etf", hit, from_pt=list(FRAIS_TIP), to=[FRAIS_TIP[0], FRAIS_TIP[1] - 30], d=5)
    kit.move("frais_etf", hit + 5, list(FRAIS_ETF_C), d=13, arc=60)
    kit.fade("frais_etf_lbl", hit + 12, to=1)

    f = kit.at("S06", "géré", "légende « gestion active » ; le stylo, toujours levé, redonne un coup et quatre pièces "
                              "grises en partent l'une après l'autre, posées en rang sous la pièce de l'ETF")
    kit.fade("frais_ga_lbl", f, to=1)
    hit = toi.tap(f - TAP + 1, list(FRAIS_TIP), lift=12)
    end = f
    for k, cid in enumerate(c.frais_ga):
        fi = hit + 3 * k
        kit.pop(cid, fi, from_pt=list(FRAIS_TIP), to=[FRAIS_TIP[0], FRAIS_TIP[1] - 26], d=4)
        end = kit.move(cid, fi + 3, list(FRAIS_GA_C[k]), d=13, arc=60)

    f = kit.at("S06", "activement.", "la pièce unique de l'ETF bat, seule ; les quatre pièces grises ne bougent pas")
    kit.pulse("frais_etf", f, peak=1.15)
    lower(toi, end, 10)

    # ================= S07 : « Mais ce panier dépend entièrement de l’indice. » =================
    f = kit.at("S07", "Mais", "la pièce cyan descend devant le panier et entre dans l'étiquette, qui bat ; les "
                              "pièces grises et les légendes se réduisent ; le livre revient en grand ; « Toi » "
                              "s'écarte à droite")
    g = kit.move("frais_etf", f, list(ETIQ_C), d=12, e="inOut", arc=40)
    g = kit.vanish("frais_etf", g, into="etiquette", d=5)
    kit.pulse("etiquette", g - 2, peak=round(ETIQ_K * 1.1, 4))
    kit.morph([*c.frais_ga, "frais_etf_lbl", "frais_ga_lbl", "frais_mot"], [], f)
    kit.move("livre", f, list(LIVRE_C), d=MOVE, scale=1)
    kit.fade("livre_titre", f + MOVE - FADE, to=1)
    walk_low(toi, f, P_ASIDE[0], d=16)
    kit.move("toi_nom", f, list(TOI_NOM_ASIDE), d=16)

    f = kit.at("S07", "dépend", "une ficelle encre épaisse se trace du bas du livre au bord gauche du panier")
    g = kit.draw("ficelle", f, DRAW)
    S.key("ficelle_halo", "draw", g, 1)          # doublon épais, invisible (opacité 0) : la ficelle « bat »

    def beat_string(n):
        kit.pulse("ficelle_halo", n, peak=1, step=3, track="opacity")

    f = kit.at("S07", "entièrement", "la ficelle bat ; le livre glisse de 180 px à droite et le panier, ses titres et "
                                     "son étiquette glissent exactement avec lui, ficelle tendue")
    beat_string(f)
    for i in ("livre", "panier", "etiquette"):
        x, y = S.val(i, "pos", f - 1)
        kit.move(i, f, [x + SLIDE_DX, y], d=MOVE)

    f = kit.at("S07", M_INDICE, "la ficelle bat ; le livre revient à gauche, le panier avec lui ; à l'arrêt, les "
                                "mini-titres de la page et les titres du panier battent sur la même image")
    beat_string(f)
    for i, home in (("livre", LIVRE_C), ("panier", PANIER_C), ("etiquette", ETIQ_C)):
        g = kit.move(i, f, list(home), d=MOVE)
    for i in [*c.minis, *titres]:
        kit.pulse(i, g, peak=1.15)

    # ================= S08 : « Pourquoi commencer par l’indice ? Parce que c’est lui qui décide … » =============
    f = kit.at("S08", M_INDICE_Q, "le livre bat et son titre « Indice » se souligne ; « Toi » regarde, stylo baissé")
    kit.pulse("livre", f, peak=1.08)
    kit.draw("livre_titre", f, DRAW, track="under")

    beat_string(S.word_after("Parce", f))        # « Parce que c’est lui… » : la ficelle bat

    f = kit.at("S08", "décide", "un mini-titre de la page ET le titre correspondant du panier rougissent ; le "
                                "mini-titre disparaît de la page et la ficelle bat ; le titre saute hors du panier "
                                "et tombe au sol, où il reste")
    t8, m8 = titres[TITRE_TOMBE], c.minis[TITRE_TOMBE]
    S.key(m8, "fill", f, RED, 2, "out")
    S.key(t8, "fill", f, RED, 2, "out")
    kit.vanish(m8, f + 5)
    beat_string(f + 5)
    g = f + 6
    S.set(t8, z=5.5)
    S.key(t8, "z", g, 6.9)                       # il saute PAR-DESSUS le rebord (z 6), pas à travers
    sol = [round((T8_SOL[0] - PANIER_C[0]) / PANIER_K, 2), round((T8_SOL[1] - PANIER_C[1]) / PANIER_K, 2)]
    S.key(t8, "pos", g, sol, 16, "inOut", 150)
    S.key(t8, "rot", g, -30, 16, "out")
    S.key(t8, "fill", g + 16, LIGHT, 8, "inOut")   # posé au sol : il redevient un titre ordinaire, hors du panier

    f = kit.at("S08", "possèdes.", "un nouveau mini-titre surgit sur la page ; dès le mot, un nouveau titre sort du "
                                   "livre, descend la ficelle en grandissant et prend la place libre du panier, "
                                   "qui tressaute")
    kit.pop("mini_neuf", f)
    a_end = S.wire_cubic("ficelle", f)[3]
    place = S.to_world("panier", TITRES_LOCAL[TITRE_TOMBE], f)

    def offset(p):
        q = min(1.0, max(0.0, (p - 0.6) / 0.4))
        qe = q * q * (3 - 2 * q)
        return [(place[0] - a_end[0]) * qe, (place[1] - a_end[1]) * qe - 60 * math.sin(math.pi * q)]

    S.key("titre_neuf", "scale", f - 1, round(MINI_R / TITRE_R / PANIER_K, 4))
    S.along_wire("titre_neuf", "ficelle", f, 18, "out", 0, 1, f, offset=offset, scale=PANIER_K)
    S.key("titre_neuf", "pos", f + 18, list(TITRES_LOCAL[TITRE_TOMBE]))
    S.key("titre_neuf", "scale", f + 18, 1)
    kit.shake("panier", f + 18, amp=4, axis="y")

    # ================= S09 : « Première erreur : ne pas le lire. » =================
    f = kit.at("S09", "Première", "le disque 1 « Indice » du repère s'allume en cyan ; « Toi » revient près du "
                                  "panier ; le titre tombé disparaît")
    S.key("marqueur", "on", f, 1, POP, "out")
    kit.vanish(t8, f)
    walk_low(toi, f, P1[0], d=14)
    kit.move("toi_nom", f, list(TOI_NOM_C), d=14)

    f = kit.at("S09", "ne", "le stylo de « Toi » touche l'étiquette « ETF Monde », qui bat : il ne lit que le nom")
    hit = tap_on(f, ETIQ_TAP, pre=5)
    kit.pulse("etiquette", hit, peak=round(ETIQ_K * 1.08, 4))
    lower(toi, hit + 4, 7)

    f = kit.at("S09", "lire.", "« Toi » se penche vers l'étiquette, son regard en tirets fixé sur elle ; derrière, "
                               "hors de son regard, le livre l'appelle (onde cyan, deux battements, la ficelle "
                               "tressaute) ; « Toi » ne se tourne pas vers lui")
    kit.ensure("toi", "look", 0)
    S.key("toi", "look", f, -1, 4, "out")
    lean_low(toi, f, -9, d=6)
    kit.draw("regard", f + 2, 7)
    for k in range(2):
        n = f + 4 + 8 * k
        ring(S, "livre_onde", n, d=10, s0=0.8, s1=1.3)
        kit.pulse("livre", n, peak=1.2, step=3)
        kit.shake("livre", n, amp=7, axis="x")
        beat_string(n)
    kit.fade("toi_nom", f + 10, to=0)
    hold_end = f + 4 + 8 + 10
    assert hold_end < 1044, hold_end
