"""V03, partie 2 : S08-S15, images 983-2087 (34 temps forts, 36,8 s). Les deux courbes (5 % puis 4 % net), l'écart
rouge de 4 600 €, le repli en colonne et le repère « Frais : Entrée, Gestion, Autres », l'entonnoir d'entrée
(1 000 € -> 970 € + jeton de 30 €), la gestion qui tranche l'encours et dont la pile monte à côté du jeton d'entrée.

État d'entrée, épinglé à l'image 982 : kit.pin(982, ENTRY_P2) (etat_initial de S08 : graphique vide, point
« 10 000 € », axes, « 20 ans », « 4 600 € » rouge en RED_HIGH et « ? » en QUESTION_HIGH, mention soulignée,
étiquette en ETIQ_GRAPH). « Toi » en P_TOI, stylo au repos (jamais épinglé).

Temps forts (image du film, round(t x 30) ; ACOUSTIC_SNAP peut décaler d'une image) :
S08  5 %@988  10 000 €@1033  deviendraient@1056  26 500 €@1105  20 ans.@1152
S09  1 %@1209  frais@1228  tombes@1269  net.@1300
S10  Et@1329  environ@1356  21 900 €.@1375
S11  Connaître@1441  taux@1460  suffit@1468  savoir@1515  frais@1538
S12  D’abord,@1574  d’entrée,@1606  versement.@1653
S13  3 %@1690  1 000 €@1752  versés,@1767  seuls@1791  970 €@1805  investis.@1857
S14  Ensuite,@1884  gestion,@1925  prélevés@1948  année@1973  l’encours.@1987
S15  Ce@2011  pèsent@2036  durée.@2065

Écarts d'exécution de cette partie (places seulement, aucun sens changé) :
- S08-S09 : « ≈ 26 500 € » au-dessus à droite du bout de la courbe A (790, 440) et l'étiquette en ETIQ_HIT
  (544, 468) au lieu de (560, 480).
- S14 : « gestion » s'écrit 14 px plus haut que GESTION_ABOVE (775, 798) : l'étiquette basculée le toucherait.

Tour de revue 1 :
- S10 : le chiffre rouge attend 4 images que le crochet se trace, puis passe à DROITE du crochet (870, 500) avant de s'y
  loger ; le « ? » s'y résorbe, hors de « ≈ 26 500 € ».
- S11 : le « ? » naît sous la pointe, à gauche de l'étiquette (et non au-dessus), puis monte au repère par la droite de
  « 10 000 € ». La pile revient pleine (120 px, comme à la fin de S06).
- S12-S13 : « 10 000 € » glisse à gauche de l'entonnoir et le disque euro rentre (ils reviennent sur « Ensuite, ») ;
  l'entonnoir tombe ensuite, sans traverser le chiffre ; carte « 1 000 € » (espace insécable, 48 px, 230 px) qui monte à
  droite puis passe au-dessus de l'entonnoir ; sur « d’entrée, » (S13), « 3 % » bat et l'entonnoir bascule de 4°.
- S14 : tranches de 0,06 sur toute la largeur du remplissage, 12 images d'arc par-dessus le bord de la colonne
  jusqu'à la pile ; sur « l’encours. », tout le remplissage est cerné de deep (du sol au sommet) et bat avec le
  crochet ; disque 1 fait (coché, légende encre).
- S15 : la pile monte en deux paliers nets (188 puis 215 px, sous le haut du remplissage) à côté du jeton de 30 €
  posé sur la même base ; un repère pointillé deep à la hauteur du jeton traverse la pile.

Raccord vers p3 : à l'image 2087, l'état est exactement ENTRY_P3. Rien de ce que p2 commence ne dépasse l'image 2087.
"""
from pipeline.story import DRAW, DROP, MORPH, POP
from pipeline.story_kit import TAP

from . import (BAC_C, BAC_RIM, CROCHET_TXT, CROCHET_TXT_K, ENTONNOIR_C, ENTONNOIR_GOULOT, ENTONNOIR_TAUX, ENTRY_P2,
               EPARGNE_C, EPARGNE_EURO, EPARGNE_MONTANT, EPARGNE_MONTANT_S12, ETIQ_ENTREE, ETIQ_H, ETIQ_LOW,
               ETIQ_ON_TAUX, GESTION_ABOVE, GRAPH_START, JETON_ENTREE, LEVELS, P_TOI, PILE_H, PILE_W, PILE_X,
               QUESTION_MARKER, SLICE_DV, T_4NET, T_970, TAUX_LOW, TILT, TRANCHE_H, TRANCHE_W, VERSEMENT_970,
               VERSEMENT_HAUT, VERSEMENT_TIP, VERSEMENT_VIA, drop_in, level_y, pile_pos, scene_f0)

F_START, F_END = 983, 2087
ETIQ_HIT = (544, 468)                      # S09 : à droite de la pilule, hors de la courbe A et de son point final
HIT_DX = 14                                # S09 « frais » : l'étiquette avance jusqu'au contact de la pilule (x 420)
COURBE_A_TXT_R = (790, 440)                # « ≈ 26 500 € » au-dessus à droite du bout de A
CROCHET_VIA = (835, 505)                   # S10 : le chiffre rouge passe à droite du crochet avant de s'y loger
QUESTION_VIA = (720, 600)                  # S11 « savoir » : le « ? » monte par la droite de « 10 000 € »
GESTION_AT = (GESTION_ABOVE[0], GESTION_ABOVE[1] - 14)  # 798 : l'étiquette basculée ne le touche pas
JETON_VIA = (380, 700)                     # S13 « seuls » : le jeton sort du goulot par la gauche de la colonne
SLICE_STEP = 20                            # S14 : une tranche de gestion ajoute 20 px à la pile
SLICE_FLIGHT = 10                          # images d'arc d'une tranche jusqu'à la pile
GRAPH = ["courbe_a", "courbe_b", "courbe_a_txt", "courbe_b_txt", "axe_x", "axe_y", "axe_20ans", "mention1",
         "mention2", "mention_trait", "pilule_taux", "taux_diff", "graph_montant"]


def cubic(p0, p1, p2, p3):
    def at(t):
        u = 1 - t
        return [round(u ** 3 * a + 3 * t * u * u * b + 3 * t * t * u * c + t ** 3 * d, 2)
                for a, b, c, d in zip(p0, p1, p2, p3)]
    return at


def part(S, kit, c):
    toi = c.toi
    f0 = scene_f0(S, "S08")
    assert f0 == F_START, f0
    kit.pin(f0 - 1, ENTRY_P2)
    if S.val("toi", "scale", f0 - 1) == 0:                     # partie construite seule : « Toi » n'est pas entré
        toi.enter(f0 - 10, at=list(P_TOI))

    # ================= S08 « À 5 % par an, 10 000 € deviendraient environ 26 500 € en 20 ans. » =================
    f = kit.at("S08", "5 %", "la pilule bleu pâle « 5 % / an » surgit en haut à gauche du graphique vide")
    kit.pop("pilule_taux", f)

    f = kit.at("S08", "10 000 €", "le point de départ cyan et « 10 000 € » battent")
    kit.pulse("graph_point", f, peak=1.2, step=4)
    kit.pulse("graph_montant", f, peak=1.2, step=4)

    f = kit.at("S08", "deviendraient", "la courbe à 5 % (aire bleu pâle) se trace du point de départ jusqu'au bout "
                                       "des 20 ans, en montant de plus en plus fort")
    kit.draw("courbe_a", f, 48, e="linear")

    f = kit.at("S08", "26 500 €", "« ≈ 26 500 € » surgit au-dessus du bout de la courbe")
    S.key("courbe_a_txt", "pos", f - 1, list(COURBE_A_TXT_R))
    kit.pop("courbe_a_txt", f)

    f = kit.at("S08", "20 ans.", "« 20 ans » bat sous le bout de l'axe. Tenue")
    kit.pulse("axe_20ans", f, peak=1.15, step=4)

    # ================= S09 « Avec 1 % de frais en plus, tu tombes à 4 % net. » =================
    f = kit.at("S09", "1 %", "l'étiquette « 1 % / an » quitte sa place sous l'axe et monte à droite de la pilule "
                             "« 5 % / an »")
    kit.move("etiquette", f, ETIQ_HIT)

    f = kit.at("S09", "frais", "l'étiquette cogne la pilule « 5 % / an », qui tremble ; l'étiquette recule")
    S.key("etiquette", "pos", f, [ETIQ_HIT[0] - HIT_DX, ETIQ_HIT[1]], 4, "in")
    kit.shake("pilule_taux", f + 4, amp=7)
    S.key("etiquette", "pos", f + 5, list(ETIQ_HIT), 6, "out")

    f = kit.at("S09", "tombes", "l'étiquette s'abat sur la pilule, qui tombe d'un cran : « 5 % / an » devient "
                                "« 4 % net » à mi-chute ; l'étiquette reste posée dessus")
    S.key("pilule_taux", "pos", f, list(TAUX_LOW), DROP, "out")
    S.key("pilule_taux", "text", f + DROP // 2, T_4NET)
    S.key("etiquette", "pos", f, list(ETIQ_ON_TAUX), DROP, "out", arc=30)

    f = kit.at("S09", "net.", "« 4 % net » bat ; « 5 % − 1 % » s'inscrit dessous. Tenue")
    kit.pulse("pilule_taux", f, peak=1.1, step=4)
    kit.fade("taux_diff", f + 2)

    # ================= S10 « Et là, tu obtiens environ 21 900 €. » =================
    f = kit.at("S10", "Et", "une deuxième courbe part du même point et se trace sous la première, moins haut")
    kit.draw("courbe_b", f, 25, e="linear")             # fini avant « environ »

    f = kit.at("S10", "environ", "« ≈ 21 900 € » surgit à droite du bout de la deuxième courbe")
    kit.pop("courbe_b_txt", f)

    f = kit.at("S10", "21 900 €.", "un crochet rouge relie les bouts des deux courbes ; « 4 600 € » rouge descend par "
                                   "la droite du crochet et s'y loge ; le « ? » s'y résorbe : l'écart est expliqué. Tenue")
    kit.draw("crochet", f, DRAW)
    g = f + 4
    S.key("pile_montant", "pos", g, list(CROCHET_VIA), 8, "inOut")
    S.key("pile_montant", "pos", g + 8, list(CROCHET_TXT), 8, "inOut")
    S.key("pile_montant", "scale", g, CROCHET_TXT_K, 16, "inOut")
    kit.vanish("question", g, into=list(CROCHET_VIA), d=8, e="in")

    # ================= S11 « Connaître un taux ne suffit pas : encore faut-il savoir quels frais tu paies. » =====
    f = kit.at("S11", "Connaître", "le graphique se replie dans son point de départ, qui regrandit en colonne de "
                                   "l'épargne ; crochet et « 4 600 € » redeviennent le bac et la pile (pleine) ; "
                                   "l'étiquette revient près de la colonne et sa ficelle se retrace")
    S.key("epargne", "pos", f - 1, list(EPARGNE_C))           # places d'arrivée, encore invisibles (échelle 0)
    S.key("epargne", "value", f - 1, LEVELS["S11"])
    for ch in ("epargne_euro", "epargne_montant"):
        S.key(ch, "scale", f - 1, 1)
        S.key(ch, "opacity", f - 1, 1)
    S.key("bac", "pos", f - 1, list(BAC_C))
    S.key("pile", "h", f - 1, PILE_H["S06"])
    S.key("pile", "pos", f - 1, pile_pos(PILE_H["S06"]))
    for g in GRAPH:
        kit.vanish(g, f, into=list(GRAPH_START), d=MORPH)
    kit.morph(["graph_point", "crochet", "pile_montant"], ["epargne", "bac", "pile"], f)
    kit.move("etiquette", f, ETIQ_LOW)
    S.key("ficelle", "from", f - 1, 0)
    kit.draw("ficelle", f + 6, DRAW)

    f = kit.at("S11", "taux", "l'étiquette « 1 % / an » bat : un taux, seul")
    kit.pulse("etiquette", f, peak=1.12, step=3)

    f = kit.at("S11", "suffit", "« Toi » touche du stylo le bas de l'étiquette : un « ? » naît sous la pointe, à gauche")
    hit = toi.tap(f - TAP + 1, [ETIQ_LOW[0], ETIQ_LOW[1] + ETIQ_H / 2])
    tip = toi.tip(hit)
    kit.pop("question", hit, from_pt=tip, to=[tip[0] - 95, tip[1] + 60])
    toi.rest(hit + 6, 8)

    f = kit.at("S11", "savoir", "le « ? » monte en haut, au centre, par la droite de « 10 000 € »")
    S.key("question", "pos", f, list(QUESTION_VIA), 7, "in")
    S.key("question", "pos", f + 7, list(QUESTION_MARKER), 9, "out")

    f = kit.at("S11", "frais", "le « ? » éclate en trois disques numérotés légendés « Entrée », « Gestion », "
                               "« Autres » ; « Frais : » s'inscrit à gauche. Tenue")
    kit.morph(["question"], ["marqueur"], f)
    kit.fade("frais_label", f + 4)

    # ================= S12 « D’abord, les frais d’entrée, prélevés sur chaque versement. » =================
    f = kit.at("S12", "D’abord,", "le disque 1 « Entrée » grandit et se remplit de cyan")
    S.key("marqueur", "on", f, 1, POP, "out")

    f = kit.at("S12", "d’entrée,", "« 10 000 € » glisse à gauche et le disque euro rentre dans la colonne ; un entonnoir "
                                   "papier tombe sur le haut de la colonne")
    kit.move("epargne_montant", f, list(EPARGNE_MONTANT_S12), d=8, e="out")
    kit.vanish("epargne_euro", f, d=6)
    drop_in(kit, "entonnoir", f + 8, h=150, to=list(ENTONNOIR_C))

    f = kit.at("S12", "versement.", "une carte « 1 000 € » sort de la pointe du stylo de « Toi » et se pose devant "
                                    "lui. Tenue")
    kit.pop("versement", f, from_pt=toi.tip(f - 1), to=list(VERSEMENT_TIP))

    # ================= S13 « Avec 3 % de frais d’entrée, sur 1 000 € versés, seuls 970 € sont investis. » ======
    f = kit.at("S13", "3 %", "une pilule « 3 % » surgit sur la lèvre gauche de l'entonnoir")
    S.key("entonnoir_taux", "pos", f - 1, list(ENTONNOIR_TAUX))
    kit.pop("entonnoir_taux", f)
    g = S.word_after("d’entrée", f)            # accent secondaire (pas un temps fort) : « 3 % » bat, l'entonnoir penche
    kit.pulse("entonnoir_taux", g, peak=1.15, step=4)
    S.key("entonnoir", "rot", g, 4, 5, "out")
    S.key("entonnoir", "rot", g + 8, 0, 8, "inOut")

    f = kit.at("S13", "1 000 €", "la carte « 1 000 € » monte à droite puis glisse au-dessus de l'entonnoir")
    assert g + 16 < f, (g, f)
    S.key("versement", "pos", f, list(VERSEMENT_VIA), 6, "in")
    S.key("versement", "pos", f + 6, list(VERSEMENT_HAUT), 8, "out")

    f = kit.at("S13", "versés,", "la carte tombe dans l'embouchure en rapetissant et disparaît dans l'entonnoir")
    for id, z0, z1 in (("versement", 13, 7.9), ("versement_txt", 13.1, 7.95)):
        kit.ensure(id, "z", z0)
        S.key(id, "z", f, z1)
    S.key("versement", "pos", f, [ENTONNOIR_C[0], ENTONNOIR_C[1] - 5], DROP, "in")
    S.key("versement", "scale", f, 0.6, DROP, "out")
    S.key("versement", "opacity", f + DROP, 0)

    f = kit.at("S13", "seuls", "au goulot, un jeton cyan se détache, sort par la gauche de la colonne et tombe sur le "
                               "bord du bac, à côté de la pile ; « 30 € » surgit au-dessus")
    S.key("jeton_entree", "pos", f - 1, list(ENTONNOIR_GOULOT))
    kit.pop("jeton_entree", f, d=5)
    S.key("jeton_entree", "pos", f + 1, list(JETON_VIA), 5, "out")
    S.key("jeton_entree", "pos", f + 6, list(JETON_ENTREE), 8, "in")
    kit.pop("jeton_entree_txt", f + 12)

    f = kit.at("S13", "970 €", "la carte ressort sous le goulot, dans le haut de la colonne, devenue « 970 € »")
    S.key("versement_txt", "text", f - 1, T_970)
    S.key("versement", "z", f - 1, 13)
    S.key("versement_txt", "z", f - 1, 13.1)
    kit.pop("versement", f, scale=1, from_pt=list(ENTONNOIR_GOULOT), to=list(VERSEMENT_970))

    f = kit.at("S13", "investis.", "la carte « 970 € » se fond dans la colonne, dont le niveau monte d'un cran. Tenue")
    kit.vanish("versement", f, into=[EPARGNE_C[0], level_y(LEVELS["S11"])])
    S.key("epargne", "value", f + 4, LEVELS["S13"], 10, "out")

    # ================= S14 « Ensuite, les frais de gestion, prélevés chaque année sur l’encours. » =================
    f = kit.at("S14", "Ensuite,", "le disque 2 « Gestion » s'allume et le disque 1 se coche (fait) ; l'entonnoir et sa "
                                  "pilule se replient en une étiquette « entrée 3 % » au-dessus du jeton de 30 € ; "
                                  "« 10 000 € » et le disque euro reviennent")
    kit.step(f, 1)
    S.key("marqueur", "done0", f + 4, 1, 8, "out")
    for id in ("entonnoir", "entonnoir_taux"):
        kit.vanish(id, f, into=list(ETIQ_ENTREE), d=MORPH)
    kit.pop("etiquette_entree", f, from_pt=list(ENTONNOIR_C), d=MORPH)
    kit.move("epargne_montant", f, list(EPARGNE_MONTANT), d=MORPH)
    S.key("epargne_euro", "pos", f - 1, list(EPARGNE_EURO))
    kit.pop("epargne_euro", f + 4)

    f = kit.at("S14", "gestion,", "« gestion » s'écrit au-dessus de l'étiquette « 1 % / an »")
    S.key("etiquette_gestion", "pos", f - 1, list(GESTION_AT))
    kit.type("etiquette_gestion", f, rate=1.5)

    def slice_(f, k, v_col, h_pile):
        """L'étiquette bascule contre la colonne : une tranche de toute la largeur se détache du haut du remplissage,
        passe par-dessus le bord de la colonne et tombe sur la pile, qui monte d'un bloc. -> image d'arrivée."""
        tid = f"tranche{k}"
        S.key("etiquette", "rot", f, TILT, 4, "out")
        y = level_y(v_col) + TRANCHE_H / 2
        S.key(tid, "pos", f + 2, [EPARGNE_C[0], round(y, 2)])
        S.key(tid, "scale", f + 2, 1)
        S.key("epargne", "value", f + 2, round(v_col - SLICE_DV, 4))
        top = BAC_RIM - h_pile - SLICE_STEP / 2
        S.path(tid, f + 3, SLICE_FLIGHT, "inOut",
               cubic([EPARGNE_C[0], y], [EPARGNE_C[0], 690], [330, 640], [PILE_X, round(top, 2)]))
        S.key(tid, "sx", f + 3, round(PILE_W / TRANCHE_W, 4), SLICE_FLIGHT, "inOut")
        S.key(tid, "sy", f + 3, round(SLICE_STEP / TRANCHE_H, 4), SLICE_FLIGHT, "inOut")
        S.key("etiquette", "rot", f + 8, 0, 6, "inOut")
        land = f + 3 + SLICE_FLIGHT
        S.key("pile", "h", land, h_pile + SLICE_STEP, 4, "out")
        S.key("pile", "pos", land, pile_pos(h_pile + SLICE_STEP), 4, "out")
        S.key(tid, "opacity", land, 0, 3, "linear")
        S.key(tid, "scale", land + 3, 0)
        return land

    f = kit.at("S14", "prélevés", "l'étiquette bascule contre la colonne : une tranche cyan de toute la largeur se "
                                  "détache du haut du remplissage, passe par-dessus le bord et tombe sur la pile du "
                                  "bac, qui monte d'un bloc")
    slice_(f, 1, LEVELS["S13"], PILE_H["S06"])

    f = kit.at("S14", "année", "même geste : une deuxième tranche tombe sur la pile, la colonne baisse encore")
    slice_(f, 2, LEVELS["S13"] - SLICE_DV, PILE_H["S06"] + SLICE_STEP)

    f = kit.at("S14", "l’encours.", "tout le remplissage de la colonne, du sol à son sommet, se cerne de deep et bat ; "
                                    "un crochet le longe à droite, marqué « encours ». Tenue")
    f_enc = f
    kit.draw("encours_cadre", f, DRAW)
    kit.draw("crochet_encours", f, DRAW)
    kit.fade("encours_txt", f + 4)
    kit.pulse("encours_cadre", f + DRAW, peak=1.04, step=3)

    # ================= S15 « Ce sont eux qui pèsent le plus sur la durée. » =================
    f = kit.at("S15", "Ce", "« gestion » descend se poser sur le sommet de la pile du bac ; le contour et le crochet "
                            "« encours » s'effacent")
    kit.move("etiquette_gestion", f, [PILE_X, BAC_RIM - PILE_H["S14"] - 30])
    for o in ("encours_cadre", "crochet_encours", "encours_txt"):
        kit.fade(o, f, to=0)

    def grow(f, h):
        """La pile s'allonge d'un palier vers le haut (bas toujours sur le bord du bac), « gestion » monte avec elle."""
        S.key("pile", "h", f, h, 10, "out")
        S.key("pile", "pos", f, pile_pos(h), 10, "out")
        S.key("etiquette_gestion", "pos", f, [PILE_X, BAC_RIM - h - 30], 10, "out")
        return f + 10

    f = kit.at("S15", "pèsent", "1er palier : la pile « gestion » monte d'un bloc ; le jeton d'entrée, posé à côté sur "
                                "le même bord, ne bouge pas")
    grow(f, PILE_H["S15a"])

    f = kit.at("S15", "durée.", "2e palier : la pile monte encore ; un repère pointillé deep, à la hauteur du jeton, "
                                "traverse la pile : elle le dépasse de loin. Tenue")
    g = grow(f, PILE_H["S15"])
    end = kit.draw("pile_repere", g, DRAW)
    assert end <= F_END and abs(S.val("pile", "h", F_END) - PILE_H["S15"]) < 1e-6
    assert abs(S.val("epargne", "value", F_END) - LEVELS["S14"]) < 1e-6
    assert abs(S.val("pile", "h", f_enc + 4) - PILE_H["S14"]) < 1e-6
    assert BAC_RIM - PILE_H["S15"] > level_y(LEVELS["S14"]), "la pile doit rester sous le haut du remplissage"
