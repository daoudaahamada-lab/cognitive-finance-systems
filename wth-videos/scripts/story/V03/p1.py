"""V03, partie 1 : S01-S07, images 0-982 (32 temps forts, 32,8 s). L'étiquette « 1 % / an » sur la colonne de
l'épargne, les trois questions, les jetons arrachés chaque année, « + » qui meurt sur le bac, la pile « plus de 4 600 € »,
puis le réarrangement en graphique vide.

État d'entrée : l'état de distribution (image 0) : colonne `epargne` en EPARGNE_C à 0,60 avec `epargne_euro` et
`epargne_montant` « 10 000 € » ; « Toi » en P_TOI (840, 1135), stylo au repos ; tout le reste à l'échelle 0.

Temps forts (image du film, round(t x 30) ; ACOUSTIC_SNAP peut décaler d'une image) :
S01  1 %@0  frais@22  paraît@61
S02  Pourtant,@91  épargne,@120  facture@141  lourde.@169
S03  Dans@191  combien@243  viennent,@315  connaître.@350
S04  Les@377  prélevés@394  année,@420  marché@446  monte@456  baisse.@470
S05  l’argent@496  travaille@519  suivantes.@567
S06  Résultat :@595  10 000 €@630  20 ans,@662  1 %@689  coûter@731  4 600 €.@752
S07  D’où@802  écart ?@825  Regarde@846  calcul,@861  théorique,@908  garanti.@954

Tour de revue 1 :
- S01-S02 : l'étiquette reste petite (0,6) de « paraît » à « facture » (« Pourtant, » : elle tressaille, bascule de
  −12° et revient) ; elle ne regrandit qu'en tirant vers le bas (« facture »). « lourde. » : ficelle tendue, bascule de
  −10°, 40 px de plus, la colonne penche de 3° et tremble, et le bloc du haut (0,60 -> 0,50) passe au deep et file dans
  l'étiquette : la baisse est causée et se voit au téléphone.
- S03 : les questions montent d'abord (y 470, au-dessus de « 10 000 € ») puis glissent à leur place, toutes à y 440 ;
  sur « frais, » l'étiquette bat (accent secondaire, mot cherché par S.word_after).
- S04 : vague plate (courbe deep sur aire bleu clair, plus de PNG) qui monte de 90 px et bascule (« monte »), puis plonge
  (« baisse. ») ; chaque jeton sort par le haut de la colonne (y 645, au-dessus du bord) puis file à gauche par une
  courbe qui contourne la colonne jusqu'au bac.
- S05 : sur « travaille » et « suivantes. », un « + » deep naît aussi au-dessus du bac et meurt sur les jetons
  immobiles (vanish 8 images) ; « + 0 € » retiré après le contrôle sans son (mal lu). La colonne monte 0,42 -> 0,52 -> 0,62.
- S06 : les 4 jetons glissent l'un sur l'autre (kit.stagger, 2 images) puis deviennent la base cyan (60 px) de la
  pile ; sur « coûter », deux blocs fantômes (tirets cyan, sans fond, sans « + ») montent de la base, et sur la colonne
  un trait pointillé deep marque le niveau sans frais, un crochet rouge « 4 600 € » le relie au remplissage.
- S07 : « Regarde » : la pile, ses fantômes et « plus de » rentrent dans le chiffre rouge, qui monte en haut à droite
  avec son « ? » (courbe par la gauche de la colonne) ; « calcul, » : seulement alors, colonne -> point de départ,
  barre -> axe horizontal, et l'axe vertical se trace en dernier.

Raccord vers p2 : à l'image 982, l'état est exactement ENTRY_P2. Rien de ce que p1 commence ne dépasse l'image 982.
"""
from pipeline.story import DRAW, MORPH, POP, STRETCH

from . import (BAC_PLUS, BAC_RIM, BAC_SLOTS, BARRE_C, BARRE_N, BARRE_W, DEEP, EPARGNE_C, ETIQ_GRAPH,
               ETIQ_HOME, ETIQ_PESE, FANTOMES, GRAPH_MONTANT, LEVELS, P_TOI, PILE_H, PILE_X, QUESTION_ECART,
               QUESTION_HIGH, QUESTIONS_C, QUESTIONS_VIA_Y, RED_HIGH, TILT, TOKEN_DV, VAGUE_MARCHE_S04, VAGUE_S04,
               VAGUE_S04_DY, VAGUE_S04_K, drop_in, level_y, pile_pos, scene_f0)

F_START, F_END = 0, 982

# --- places propres à cette partie ---
JETON_X = 590                      # S04 : un jeton naît au haut du remplissage, côté étiquette
JETON_OUT_Y = 645                  # il sort d'abord par le haut de la colonne (bord à y 690)
JETON_CTRL = (380, 560)            # puis file à gauche en contournant la colonne (Bézier quadratique)
JETON_FALL = 11                    # images de vol jusqu'au bac
PILE_FROM = [PILE_X, BAC_RIM - 30]                         # S06 : les jetons s'empilent au centre de la base
PEN_UP = [705, 975]                                        # S07 « D’où » : « Toi » lève le stylo (allonge 175 px)
MONTANT_CTRL = (150, 380)          # S07 : le chiffre rouge monte par la gauche de la colonne, puis passe au-dessus


def bezier(p0, c, p1):
    def at(p):
        return [round((1 - p) ** 2 * p0[0] + 2 * p * (1 - p) * c[0] + p * p * p1[0], 2),
                round((1 - p) ** 2 * p0[1] + 2 * p * (1 - p) * c[1] + p * p * p1[1], 2)]
    return at


def jeton_flight(S, jid, f, start, end):
    """Le jeton arraché sort par le haut de la colonne (5 images) puis file à gauche, par-dessus son bord, jusqu'à sa
    place dans le bac -> image d'arrivée."""
    out = [start[0], JETON_OUT_Y]
    S.key(jid, "pos", f, out, 5, "out")
    S.path(jid, f + 5, JETON_FALL, "in", bezier(out, JETON_CTRL, end))
    return f + 5 + JETON_FALL


def part(S, kit, c):
    toi = c.toi
    kit.pin(0 - 1, {
        "epargne": {"pos": list(EPARGNE_C), "scale": 1, "opacity": 1, "value": LEVELS["S01"], "rot": 0},
        "etiquette": {"pos": list(ETIQ_HOME), "scale": 0, "rot": 0},
        "etiquette_mot": {"opacity": 0}, "ficelle": {"draw": 0, "from": 0},
        "barre_temps": {"scale": 0, "value": 0}, "bac": {"scale": 0}, "pile": {"scale": 0},
        "vague": {"scale": 0}, "question": {"scale": 0},
        "axe_x": {"scale": 0}, "graph_point": {"scale": 0}, "pile_montant": {"scale": 0},
    })
    # p1 ouvre le film : « Toi » est déjà là (distribution, show=True), au repos en P_TOI ; aucun garde-fou d'entrée.
    assert S.val("toi", "scale", -1) > 0 and S.val("toi", "pos", -1) == list(P_TOI)

    # ================= S01 : l'étiquette surgit, se nomme « frais », paraît minuscule =================
    f = kit.at("S01", "1 %", "l'étiquette cyan « 1 % / an » surgit à droite de la colonne pendant que sa ficelle se "
                             "trace depuis le coin haut droit de la colonne")
    kit.pop("etiquette", f)
    kit.draw("ficelle", f, POP)

    f = kit.at("S01", "frais", "le mot « frais » s'inscrit en fondu juste au-dessus de l'étiquette")
    kit.fade("etiquette_mot", f)

    f = kit.at("S01", "paraît", "l'étiquette et son mot « frais » rapetissent sur place à l'échelle 0,6 : un petit "
                                "prix accroché à l'épargne ; elle reste petite jusqu'à « facture »")
    S.key("etiquette", "scale", f, 0.6, MORPH, "out")

    # ================= S02 : le petit prix pèse =================
    f = kit.at("S02", "Pourtant,", "la petite étiquette tressaille au bout de sa ficelle : elle bascule de −12° vers "
                                   "la colonne et revient (elle reste petite)")
    S.key("etiquette", "rot", f, -12, 5, "out")
    S.key("etiquette", "rot", f + 7, 0, 8, "inOut")

    f = kit.at("S02", "épargne,", "la colonne de l'épargne, son disque euro et « 10 000 € » battent une fois")
    kit.pulse("epargne", f, peak=1.05)

    f = kit.at("S02", "facture", "l'étiquette regrandit (0,6 -> 1) en tirant vers le bas : elle descend de 150 px au "
                                 "bout de sa ficelle, qui s'allonge depuis le coin de la colonne")
    kit.move("etiquette", f, list(ETIQ_PESE), scale=1)

    f = kit.at("S02", "lourde.", "elle tire : ficelle tendue, bascule de −10°, 40 px de plus ; la colonne penche et "
                                 "tremble, son bloc du haut vire au deep et file dans l'étiquette : le niveau perd un "
                                 "bloc entier (0,60 -> 0,50). Tenue")
    S.key("etiquette", "rot", f, -10, 4, "out")
    kit.move("etiquette", f, [ETIQ_PESE[0], ETIQ_PESE[1] + 40], d=10, e="out")
    S.key("etiquette", "rot", f + 12, 0, 8, "inOut")
    S.key("epargne", "rot", f, 3, 4, "out")
    kit.shake("epargne", f + 1, amp=5)
    S.key("epargne", "rot", f + 8, 0, 8, "inOut")
    S.key("epargne", "value", f, LEVELS["S02"], 10, "out")
    S.key("epargne_bloc", "scale", f, 1)                        # le 6e bloc se détache, posé sur sa place
    S.key("epargne_bloc", "fill", f, DEEP, 3, "out")            # il vire au deep (flash)
    kit.vanish("epargne_bloc", f + 3, into="etiquette", d=10, e="inOut")

    # ================= S03 : trois questions sortent de l'étiquette =================
    f = kit.at("S03", "Dans", "l'étiquette et son mot « frais » remontent à leur place ; la colonne reste baissée "
                              "(0,50)")
    f_dans = f
    kit.move("etiquette", f, list(ETIQ_HOME))

    for k, mot, txt in ((0, "combien", "« Combien ? »"), (1, "viennent,", "« D’où ? »"),
                        (2, "connaître.", "« Comment ? »")):
        f = kit.at("S03", mot, f"la pilule {txt} sort de l'étiquette, monte au-dessus de « 10 000 € » puis glisse se "
                   "poser en haut" + (" (à côté des précédentes). Tenue" if k == 2 else ""))
        q = f"question{k + 1}"
        S.key(q, "pos", f - 1, list(ETIQ_HOME))
        kit.pop(q, f)
        S.key(q, "pos", f, [ETIQ_HOME[0], QUESTIONS_VIA_Y], 7, "out")
        S.key(q, "pos", f + 7, list(QUESTIONS_C[k]), 11, "inOut")
        if k == 0:     # accent secondaire (pas un temps fort) : sur « frais, », l'étiquette des frais bat
            g = S.word_after("frais", f)
            kit.pulse("etiquette", g, peak=1.08, step=4)
    assert f_dans < S.word_after("frais", f_dans) < f

    # ================= S04 : chaque année, l'étiquette arrache un jeton =================
    f = kit.at("S04", "Les", "les trois questions rentrent dans l'étiquette ; la barre du temps (20 cases vides) "
                             "s'étire en haut, de gauche à droite")
    for k in range(3):
        kit.vanish(f"question{k + 1}", f, into="etiquette")
    x_left = BARRE_C[0] - BARRE_W / 2
    S.key("barre_temps", "pos", f - 1, [x_left, BARRE_C[1]])
    S.key("barre_temps", "sx", f - 1, 0)
    S.key("barre_temps", "scale", f, 1)
    S.key("barre_temps", "sx", f, 1, STRETCH, "out")
    S.key("barre_temps", "pos", f, list(BARRE_C), STRETCH, "out")
    S.key("etiquette", "scale", f + POP - 1, 1.08, 3, "out")          # elle « avale » les questions
    S.key("etiquette", "scale", f + POP + 2, 1, 4, "inOut")

    level = [LEVELS["S02"]]

    def levy(k, f):
        """Un prélèvement : une case de plus, l'étiquette bascule (cause), PUIS le jeton k se détache du haut du
        remplissage, sort par le haut de la colonne et tombe dans le bac ; la colonne perd TOKEN_DV."""
        S.key("barre_temps", "value", f, (k + 1) / BARRE_N, 6, "out")
        S.key("etiquette", "rot", f, TILT, 5, "out")
        S.key("etiquette", "rot", f + 9, 0, 6, "inOut")
        j = f"jeton{k + 1}"
        g = f + 4                                                       # la bascule est faite : le jeton se détache
        start = [JETON_X, round(level_y(level[0]), 1)]
        S.key(j, "pos", g - 1, start)
        kit.pop(j, g, d=4)
        level[0] = round(level[0] - TOKEN_DV, 3)
        S.key("epargne", "value", g, level[0], 5, "out")
        return jeton_flight(S, j, g + 1, start, list(BAC_SLOTS[k]))

    f = kit.at("S04", "prélevés", "1re année : la case 1 se remplit et « 1 an » s'inscrit dessous ; le bac « frais » "
                                  "surgit à gauche ; l'étiquette bascule contre la colonne, puis un jeton se détache "
                                  "du haut du remplissage, sort par le haut de la colonne et tombe dans le bac")
    kit.pop("bac", f)
    kit.pop("barre_1an", f + 2)
    levy(0, f)

    f = kit.at("S04", "année,", "2e année : case 2 ; même bascule de l'étiquette ; un 2e jeton sort et tombe dans le "
                                "bac")
    levy(1, f)

    f = kit.at("S04", "marché", "la vague du marché (courbe plate sur aire bleu clair) tombe à gauche sous la barre ; "
                                "« marché » surgit dessous")
    S.key("vague", "scale", f - 1, VAGUE_S04_K)
    drop_in(kit, "vague", f, h=120, to=list(VAGUE_S04))
    kit.pop("vague_marche", f + 3)

    f = kit.at("S04", "monte", "la vague monte de 90 px en basculant ; 3e année : case 3, bascule, un 3e jeton tombe "
                               "quand même, sur la crête")
    S.key("vague", "pos", f, [VAGUE_S04[0], VAGUE_S04[1] - VAGUE_S04_DY], 12, "inOut")
    S.key("vague", "rot", f, -8, 12, "inOut")
    levy(2, f)

    f = kit.at("S04", "baisse.", "la vague plonge de 180 px en basculant de l'autre côté ; 4e année : case 4, bascule, "
                                 "un 4e jeton tombe quand même, au creux. Tenue")
    S.key("vague", "pos", f, [VAGUE_S04[0], VAGUE_S04[1] + VAGUE_S04_DY], 14, "inOut")
    S.key("vague", "rot", f, 8, 14, "inOut")
    end = levy(3, f)
    S.key("vague", "rot", f + 16, 0, 10, "inOut")
    assert abs(level[0] - LEVELS["S04"]) < 1e-6 and end <= scene_f0(S, "S05") + 2, (level, end)

    # ================= S05 : la colonne grossit, le « + » du bac meurt =================
    f = kit.at("S05", "l’argent", "les 4 jetons du bac battent ensemble : c'est l'argent prélevé")
    for k in range(4):
        kit.pulse(f"jeton{k + 1}", f, peak=1.15)

    def plus_meurt(f):
        """Le « + » deep naît aussi au-dessus du bac... et meurt sur les jetons immobiles (vanish 8 images)."""
        S.key("bac_plus", "pos", f - 1, list(BAC_PLUS))
        kit.pop("bac_plus", f)
        return kit.vanish("bac_plus", f + 9, into=[BAC_PLUS[0], BAC_SLOTS[0][1]], d=8, e="in")

    f = kit.at("S05", "travaille", "une année de plus (case 5) : un « + » surgit à côté de « 10 000 € » et la colonne "
                                   "monte (0,42 -> 0,52) ; le même « + » naît au-dessus du bac et meurt aussitôt sur "
                                   "les jetons immobiles")
    S.key("barre_temps", "value", f, 5 / BARRE_N, 6, "out")
    kit.pop("epargne_plus", f)
    S.key("epargne", "value", f, LEVELS["S05a"], 10, "out")
    plus_meurt(f)

    f = kit.at("S05", "suivantes.", "encore une année (case 6) : le « + » rebat, la colonne monte (0,52 -> 0,62) ; au "
                                    "bac, un « + » renaît et meurt de nouveau sur les jetons immobiles. Tenue")
    S.key("barre_temps", "value", f, 6 / BARRE_N, 6, "out")
    kit.pulse("epargne_plus", f, peak=1.2)
    S.key("epargne", "value", f, LEVELS["S05"], 10, "out")
    plus_meurt(f + 2)

    # ================= S06 : la pile de 20 ans : plus de 4 600 € =================
    f = kit.at("S06", "Résultat :", "la vague et « marché » se réduisent et sortent ; « + » s'efface ; "
                                    "les 4 jetons glissent l'un sur l'autre, puis deviennent la base cyan de la pile")
    for o in ("vague", "vague_marche", "epargne_plus"):
        kit.vanish(o, f)
    jetons = [f"jeton{k + 1}" for k in range(4)]
    kit.stagger(jetons, f, 2, kit.move, PILE_FROM, d=8)
    g = f + 3 * 2 + 8
    S.key("pile", "h", g - 1, PILE_H["base"])
    S.key("pile", "pos", g - 1, pile_pos(PILE_H["base"]))
    kit.morph(jetons, ["pile"], g, pair=False)

    f = kit.at("S06", "10 000 €", "« 10 000 € » au-dessus de la colonne bat")
    kit.pulse("epargne_montant", f, peak=1.12, step=4)

    f = kit.at("S06", "20 ans,", "la barre du temps se remplit jusqu'à la 20e case ; « 20 ans » surgit sous son bout")
    S.key("barre_temps", "value", f, 1, 18, "linear")
    kit.pop("barre_20ans", f + 12)

    f = kit.at("S06", "1 %", "l'étiquette « 1 % / an » bat et bascule de -8° vers la colonne, puis se redresse")
    kit.pulse("etiquette", f, peak=1.12, step=4)
    S.key("etiquette", "rot", f, -8, 5, "out")
    S.key("etiquette", "rot", f + 12, 0, 8, "inOut")

    f = kit.at("S06", "coûter", "deux blocs fantômes (tirets cyan, vides) montent de la base de la pile : les gains "
                                "que les jetons n'ont pas faits ; sur la colonne, un trait pointillé marque le niveau "
                                "sans frais et un crochet rouge « 4 600 € » le relie au remplissage")
    for k, pt in enumerate(FANTOMES):
        kit.pop(f"fantome{k + 1}", f + 4 * k, from_pt=[PILE_X, BAC_RIM - PILE_H["base"]], to=list(pt), d=POP)
    kit.draw("epargne_nofee", f + 4, DRAW)
    kit.draw("epargne_ecart", f + 10, DRAW)
    kit.fade("epargne_ecart_txt", f + 14)

    f = kit.at("S06", "4 600 €.", "« plus de » et « 4 600 € » en rouge surgissent au-dessus de la pile. Tenue")
    kit.pop("pile_plusde", f)
    kit.pop("pile_montant", f + 2)
    kit.pulse("epargne_ecart_txt", f + 4, peak=1.12, step=4)

    # ================= S07 : d'où vient l'écart ? Tout se réarrange en graphique vide =================
    f = kit.at("S07", "D’où", "« Toi » lève le stylo ; un grand « ? » naît sous sa pointe")
    toi.reach(f, PEN_UP, d=8)
    tip = toi.tip(f + 7)
    kit.pop("question", f + 6, from_pt=tip, to=[tip[0] - 10, tip[1] - 60])

    f = kit.at("S07", "écart ?", "le « ? » vole en arc et se pose contre le « 4 600 € » rouge de la pile")
    kit.move("question", f, list(QUESTION_ECART), arc=90)
    toi.rest(f + 2, d=10)

    f = kit.at("S07", "Regarde", "1er temps : la pile, ses fantômes et « plus de » rentrent dans le chiffre rouge ; le "
                                 "bac s'efface ; le chiffre monte en haut à droite avec son « ? »")
    into = S.to_world("pile_montant", [0, 0], f - 1)
    for x in ("pile", "fantome1", "fantome2", "pile_plusde"):
        kit.vanish(x, f, into=into, d=POP)
    kit.vanish("bac", f)
    for x in ("barre_1an", "barre_20ans"):
        kit.fade(x, f, to=0)
    g = f + 5
    start = S.val("pile_montant", "pos", g - 1)
    S.path("pile_montant", g, 18, "inOut", bezier(start, MONTANT_CTRL, list(RED_HIGH)))
    kit.move("question", g, list(QUESTION_HIGH), d=18, arc=60)

    f = kit.at("S07", "calcul,", "2e temps : la colonne se réduit en point de départ (« 10 000 € » s'y pose) et la "
                                 "barre du temps devient l'axe horizontal « 20 ans » ; l'étiquette se range sous l'axe ;"
                                 " l'axe vertical se trace en dernier")
    born = S.to_world("epargne_montant", [0, 0], f - 1)
    kit.morph(["epargne", "barre_temps"], ["graph_point", "axe_x"], f, pair=True)
    for x in ("barre_1an", "barre_20ans"):
        S.key(x, "scale", f, 0)
    kit.pop("graph_montant", f, from_pt=born, to=list(GRAPH_MONTANT), d=MORPH)
    kit.pop("axe_20ans", f + 4)
    for x in ("epargne_nofee", "epargne_ecart", "epargne_ecart_txt"):   # partis avec la colonne ; cachés pour S11
        S.key(x, "opacity", f + MORPH, 0)
    kit.fade("etiquette_mot", f, to=0)
    S.key("ficelle", "from", f, 1, 6, "in")
    S.key("ficelle", "draw", f + 6, 0)                                  # fil rentré : remis à zéro, invisible
    S.key("ficelle", "from", f + 6, 0)
    kit.move("etiquette", f, list(ETIQ_GRAPH))
    kit.draw("axe_y", f + MORPH, DRAW)

    f = kit.at("S07", "théorique,", "la mention « Exemple théorique, / rendement non garanti » s'inscrit en fondu en "
                                    "haut")
    kit.fade("mention1", f)
    kit.fade("mention2", f)

    f = kit.at("S07", "garanti.", "« non garanti » se souligne en cyan profond. Tenue")
    end = kit.draw("mention_trait", f, DRAW)
    assert end <= F_END, end
