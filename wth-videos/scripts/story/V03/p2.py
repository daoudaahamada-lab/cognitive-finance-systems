"""V03, partie 2 : S08-S15, images 983-2087 (34 temps forts, 36,8 s). Les deux courbes (5 % puis 4 % net), l'écart
rouge de 4 600 €, le repli en colonne et le repère « Frais : Entrée, Gestion, Autres », l'entonnoir d'entrée
(1 000 € -> 970 € + jeton de 30 €), la gestion qui tranche l'encours et dont la pile écrase le jeton d'entrée.

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
- S12-S13 : la carte « 1 000 € » se pose en VERSEMENT_TIP (735, 960), posée sur la pointe du stylo au repos
  (751, 1013) ; en VERSEMENT_HOME (720, 990), la pointe la percerait et la carte mordrait sur la colonne (x 630).
- S14-S15 : le crochet « encours » longe le flanc DROIT de la colonne (x 645, branches vers la colonne) et
  « encours » s'écrit à sa droite (662, 950) : à gauche, entre la pile (x 190) et la colonne (x 410), il couperait
  l'étiquette « entrée 3 % » (x 205-395).
- S11 : le « ? » né du toucher se pose juste au-dessus de l'étiquette (775, 775) avant de monter au repère.

Raccord vers p3 : à l'image 2087, l'état est exactement ENTRY_P3 (colonne en EPARGNE_C à 0,60, étiquette en
ETIQ_LOW avec sa ficelle, pile h 520 value 0,95 surmontée de « gestion », jeton d'entrée, « 30 € » et « entrée 3 % »
dans le bac, disque 2 actif, « Frais : », crochet « encours » effacé) ; « Toi » en P_TOI, stylo au repos.
Rien de ce que p2 commence ne dépasse l'image 2087.
"""
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP  # noqa: F401
from pipeline.story_kit import TAP

from . import (BAC_C, BAC_RIM, CROCHET_TXT, CROCHET_TXT_K, ENTONNOIR_C, ENTONNOIR_GOULOT, ENTRY_P2, EPARGNE_C,
               EPARGNE_H, EPARGNE_W, ETIQ_ENTREE, ETIQ_H, ETIQ_LOW, ETIQ_ON_TAUX, ETIQ_TAUX, FLOOR, GRAPH_START,
               JETON_ENTREE, LEVELS, P_TOI, PILE_C, PILE_H0, PILE_S11, PILE_S14, PILE_S15, PILE_W, PILE_X,
               QUESTION_MARKER, SLICE_DV, T_4NET, T_970, TAUX_LOW, TILT, TRANCHE_H, TRANCHE_W,
               VERSEMENT_970, VERSEMENT_HAUT, level_y, scene_f0)

F_START, F_END = 983, 2087
HIT_DX = 24                                # S09 « frais » : l'étiquette avance de 24 px contre la pilule
VERSEMENT_TIP = (735, 960)                 # S12 : la carte posée sur la pointe du stylo au repos (écart, voir en tête)
QUESTION_ETIQ = (775, 775)                 # S11 : le « ? » né du toucher, au-dessus de l'étiquette
ENCOURS_X = EPARGNE_C[0] + EPARGNE_W / 2 + 15    # 645 : crochet le long du flanc droit de la colonne
ENCOURS_TXT_R = (662, 950)                 # « encours » Bold 34, ancre start, à droite du haut du crochet
PILE_STEP = 0.05                           # S14 : une tranche de gestion ajoutée à la pile
GRAPH = ["courbe_a", "courbe_b", "courbe_a_txt", "courbe_b_txt", "axe_x", "axe_y", "axe_20ans", "mention1",
         "mention2", "mention_trait", "pilule_taux", "taux_diff", "graph_montant"]


def part(S, kit, c):
    toi = c.toi
    f0 = scene_f0(S, "S08")
    assert f0 == F_START, f0
    kit.pin(f0 - 1, ENTRY_P2)
    if S.val("toi", "scale", f0 - 1) == 0:                     # partie construite seule : « Toi » n'est pas entré
        toi.enter(f0 - 10, at=list(P_TOI))

    # crochet « encours » sur le flanc droit (écart assumé, voir en tête) : branches tournées vers la colonne
    half = (FLOOR - level_y(LEVELS["S14"])) / 2
    S.ents["crochet_encours"]["p"]["pts"] = [[-14, half], [0, half], [0, -half], [-14, -half]]
    S.ents["encours_txt"]["p"]["anchor"] = "start"

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
    kit.pop("courbe_a_txt", f)

    f = kit.at("S08", "20 ans.", "« 20 ans » bat sous le bout de l'axe. Tenue")
    kit.pulse("axe_20ans", f, peak=1.15, step=4)

    # ================= S09 « Avec 1 % de frais en plus, tu tombes à 4 % net. » =================
    f = kit.at("S09", "1 %", "l'étiquette « 1 % / an » quitte sa place sous l'axe et monte à droite de la pilule "
                             "« 5 % / an »")
    kit.move("etiquette", f, ETIQ_TAUX)

    f = kit.at("S09", "frais", "l'étiquette cogne la pilule « 5 % / an », qui tremble ; l'étiquette recule")
    S.key("etiquette", "pos", f, [ETIQ_TAUX[0] - HIT_DX, ETIQ_TAUX[1]], 4, "in")
    kit.shake("pilule_taux", f + 4, amp=7)
    S.key("etiquette", "pos", f + 5, list(ETIQ_TAUX), 6, "out")

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

    f = kit.at("S10", "21 900 €.", "un crochet rouge relie les bouts des deux courbes ; « 4 600 € » rouge descend s'y "
                                   "loger et le « ? » s'y résorbe : l'écart est expliqué. Tenue")
    kit.draw("crochet", f, DRAW)
    kit.move("pile_montant", f + 3, CROCHET_TXT, scale=CROCHET_TXT_K)
    kit.vanish("question", f + 3, into=list(CROCHET_TXT), d=MOVE, e="inOut")

    # ================= S11 « Connaître un taux ne suffit pas : encore faut-il savoir quels frais tu paies. » =====
    f = kit.at("S11", "Connaître", "le graphique se replie dans son point de départ, qui regrandit en colonne de "
                                   "l'épargne ; crochet et « 4 600 € » redeviennent le bac et la pile ; l'étiquette "
                                   "revient près de la colonne et sa ficelle se retrace")
    S.key("epargne", "pos", f - 1, list(EPARGNE_C))           # places d'arrivée, encore invisibles (échelle 0)
    S.key("epargne", "value", f - 1, LEVELS["S11"])
    for ch in ("epargne_euro", "epargne_montant"):
        S.key(ch, "scale", f - 1, 1)
        S.key(ch, "opacity", f - 1, 1)
    S.key("bac", "pos", f - 1, list(BAC_C))
    S.key("pile", "pos", f - 1, list(PILE_C))
    S.key("pile", "h", f - 1, PILE_H0)
    S.key("pile", "value", f - 1, PILE_S11)
    for g in GRAPH:
        kit.vanish(g, f, into=list(GRAPH_START), d=MORPH)
    kit.morph(["graph_point", "crochet", "pile_montant"], ["epargne", "bac", "pile"], f)
    kit.move("etiquette", f, ETIQ_LOW)
    S.key("ficelle", "from", f - 1, 0)
    kit.draw("ficelle", f + 6, DRAW)

    f = kit.at("S11", "taux", "l'étiquette « 1 % / an » bat : un taux, seul")
    kit.pulse("etiquette", f, peak=1.12, step=3)

    f = kit.at("S11", "suffit", "« Toi » touche du stylo le bas de l'étiquette : un « ? » naît sous la pointe")
    hit = toi.tap(f - TAP + 1, [ETIQ_LOW[0], ETIQ_LOW[1] + ETIQ_H / 2])
    kit.pop("question", hit, from_pt=toi.tip(hit), to=list(QUESTION_ETIQ))
    toi.rest(hit + 6, 8)

    f = kit.at("S11", "savoir", "le « ? » monte en haut, au centre")
    kit.move("question", f, QUESTION_MARKER)

    f = kit.at("S11", "frais", "le « ? » éclate en trois disques numérotés légendés « Entrée », « Gestion », "
                               "« Autres » ; « Frais : » s'inscrit à gauche. Tenue")
    kit.morph(["question"], ["marqueur"], f)
    kit.fade("frais_label", f + 4)

    # ================= S12 « D’abord, les frais d’entrée, prélevés sur chaque versement. » =================
    f = kit.at("S12", "D’abord,", "le disque 1 « Entrée » grandit et se remplit de cyan")
    S.key("marqueur", "on", f, 1, POP, "out")

    f = kit.at("S12", "d’entrée,", "un entonnoir papier tombe sur le haut de la colonne et coiffe son disque euro")
    kit.drop("entonnoir", f, h=150)

    f = kit.at("S12", "versement.", "une carte « 1 000 € » sort de la pointe du stylo de « Toi » et se pose devant "
                                    "lui. Tenue")
    kit.pop("versement", f, from_pt=toi.tip(f - 1), to=list(VERSEMENT_TIP))

    # ================= S13 « Avec 3 % de frais d’entrée, sur 1 000 € versés, seuls 970 € sont investis. » ======
    f = kit.at("S13", "3 %", "une pilule « 3 % » surgit sur la lèvre gauche de l'entonnoir")
    kit.pop("entonnoir_taux", f)

    f = kit.at("S13", "1 000 €", "la carte « 1 000 € » glisse au-dessus de l'entonnoir")
    kit.move("versement", f, VERSEMENT_HAUT, d=14, arc=60)

    f = kit.at("S13", "versés,", "la carte tombe dans l'embouchure en rapetissant et disparaît dans l'entonnoir")
    for id, z0, z1 in (("versement", 13, 7.9), ("versement_txt", 13.1, 7.95)):
        kit.ensure(id, "z", z0)
        S.key(id, "z", f, z1)
    S.key("versement", "pos", f, [ENTONNOIR_C[0], ENTONNOIR_C[1] - 5], DROP, "in")
    S.key("versement", "scale", f, 0.6, DROP, "out")
    S.key("versement", "opacity", f + DROP, 0)

    f = kit.at("S13", "seuls", "au goulot, un jeton cyan se détache et tombe dans le bac, à côté de la pile ; « 30 € » "
                               "surgit au-dessus")
    S.key("jeton_entree", "pos", f - 1, list(ENTONNOIR_GOULOT))
    kit.pop("jeton_entree", f, d=5)
    S.key("jeton_entree", "pos", f + 1, list(JETON_ENTREE), 11, "inOut", arc=70)
    kit.pop("jeton_entree_txt", f + 9)

    f = kit.at("S13", "970 €", "la carte ressort sous le goulot, dans le haut de la colonne, devenue « 970 € »")
    S.key("versement_txt", "text", f - 1, T_970)
    S.key("versement", "z", f - 1, 13)
    S.key("versement_txt", "z", f - 1, 13.1)
    kit.pop("versement", f, scale=1, from_pt=list(ENTONNOIR_GOULOT), to=list(VERSEMENT_970))

    f = kit.at("S13", "investis.", "la carte « 970 € » se fond dans la colonne, dont le niveau monte d'un cran. Tenue")
    kit.vanish("versement", f, into=[EPARGNE_C[0], level_y(LEVELS["S11"])])
    S.key("epargne", "value", f + 4, LEVELS["S13"], 10, "out")

    # ================= S14 « Ensuite, les frais de gestion, prélevés chaque année sur l’encours. » =================
    f = kit.at("S14", "Ensuite,", "le disque 2 « Gestion » s'allume ; l'entonnoir et sa pilule se replient en une "
                                  "étiquette « entrée 3 % » posée au-dessus du jeton de 30 €")
    kit.step(f, 1)
    for id in ("entonnoir", "entonnoir_taux"):
        kit.vanish(id, f, into=list(ETIQ_ENTREE), d=MORPH)
    kit.pop("etiquette_entree", f, from_pt=list(ENTONNOIR_C), d=MORPH)

    f = kit.at("S14", "gestion,", "« gestion » s'écrit au-dessus de l'étiquette « 1 % / an »")
    kit.type("etiquette_gestion", f, rate=1.5)

    def slice_(f, k, v_col, v_pile):
        """L'étiquette bascule contre la colonne : une tranche se détache du haut du remplissage et tombe sur la
        pile, qui monte d'un cran. -> image d'arrivée."""
        tid = f"tranche{k}"
        S.key("etiquette", "rot", f, TILT, 4, "out")
        y = level_y(v_col) + SLICE_DV * EPARGNE_H / 2
        S.key(tid, "pos", f + 2, [EPARGNE_C[0], round(y, 2)])
        S.key(tid, "scale", f + 2, 1)
        S.key("epargne", "value", f + 2, round(v_col - SLICE_DV, 4))
        top = BAC_RIM - PILE_H0 * v_pile - TRANCHE_H / 2
        S.key(tid, "pos", f + 3, [PILE_X, round(top, 2)], DROP, "inOut", arc=90)
        S.key(tid, "sx", f + 3, round(PILE_W / TRANCHE_W, 4), DROP, "inOut")
        S.key("etiquette", "rot", f + 8, 0, 6, "inOut")
        land = f + 3 + DROP
        S.key("pile", "value", land, round(v_pile + PILE_STEP, 4), 4, "out")
        S.key(tid, "opacity", land, 0, 3, "linear")
        S.key(tid, "scale", land + 3, 0)
        return land

    f = kit.at("S14", "prélevés", "l'étiquette bascule contre la colonne : une tranche cyan se détache du haut de la "
                                  "colonne et tombe sur la pile du bac, qui monte")
    slice_(f, 1, LEVELS["S13"], PILE_S11)

    f = kit.at("S14", "année", "même geste : une deuxième tranche tombe sur la pile, la colonne baisse encore")
    slice_(f, 2, LEVELS["S13"] - SLICE_DV, PILE_S11 + PILE_STEP)

    f = kit.at("S14", "l’encours.", "un crochet se trace le long de la colonne, du sol à son sommet, marqué « encours » ;"
                                    " la colonne entière bat. Tenue")
    top = level_y(LEVELS["S14"])
    S.key("crochet_encours", "pos", f - 1, [ENCOURS_X, round((top + FLOOR) / 2, 2)])
    S.key("encours_txt", "pos", f - 1, list(ENCOURS_TXT_R))
    kit.draw("crochet_encours", f, DRAW)
    kit.fade("encours_txt", f + 4)
    kit.pulse("epargne", f + 6, peak=1.05, step=3)

    # ================= S15 « Ce sont eux qui pèsent le plus sur la durée. » =================
    f = kit.at("S15", "Ce", "« gestion » descend se poser sur le sommet de la pile du bac ; le crochet « encours » "
                            "s'efface")
    kit.move("etiquette_gestion", f, [PILE_X, BAC_RIM - PILE_H0 - 30])
    kit.fade("crochet_encours", f, to=0)
    kit.fade("encours_txt", f, to=0)

    def grow(f, h, v):
        """La pile s'allonge vers le haut (bas toujours sur le bord du bac), « gestion » monte avec elle."""
        S.key("pile", "h", f, h, 10, "out")
        S.key("pile", "pos", f, [PILE_X, BAC_RIM - h / 2], 10, "out")
        S.key("pile", "value", f, v, 10, "out")
        S.key("etiquette_gestion", "pos", f, [PILE_X, BAC_RIM - h - 30], 10, "out")
        return f + 10

    f = kit.at("S15", "pèsent", "la pile « gestion » monte encore ; le jeton d'entrée, à côté, ne bouge pas")
    grow(f, 460, PILE_S15["value"])

    f = kit.at("S15", "durée.", "la pile « gestion » monte une fois de plus, très haut au-dessus du jeton de 30 €. "
                                "Tenue")
    end = grow(f, PILE_S15["h"], PILE_S15["value"])
    assert end <= F_END and abs(S.val("pile", "value", F_END) - PILE_S15["value"]) < 1e-6
    assert abs(S.val("epargne", "value", F_END) - LEVELS["S14"]) < 1e-6
    assert abs(S.val("pile", "value", 1990) - PILE_S14) < 1e-6
