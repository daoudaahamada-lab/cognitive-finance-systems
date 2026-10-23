"""V03, partie 1 : S01-S07, images 0-982 (32 temps forts, 32,8 s). L'étiquette « 1 % / an » sur la colonne de
l'épargne, les trois questions, les jetons arrachés chaque année, « + » contre « + 0 € », la pile « plus de 4 600 € »,
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

Brief, scène par scène (ids de la distribution, places = constantes du paquet) :
- S01. Image 0 déjà lisible (colonne + « Toi »). « 1 % » : `etiquette` pop en ETIQ_HOME pendant que `ficelle` se trace
  (kit.draw 9). « frais » : `etiquette_mot` en fondu (texte, FADE). « paraît » : l'étiquette (et son mot, enfant)
  passe à l'échelle 0,6 sur place (MORPH). Tenue jusqu'à « Pourtant ».
- S02. « Pourtant, » : l'étiquette revient à 1. « épargne, » : `epargne` bat (kit.pulse, peak 1,05). « facture » :
  l'étiquette descend en ETIQ_PESE (MOVE) ; la ficelle (ancrée aux deux) s'allonge. « lourde. » : value de `epargne`
  0,60 -> 0,55 (10 images) et l'étiquette descend encore de 20 px. Tenue.
- S03. « Dans » : l'étiquette remonte en ETIQ_HOME ; la colonne RESTE à 0,55. « combien », « viennent, »,
  « connaître. » : `question1`, `question2`, `question3` naissent de l'étiquette (kit.pop from_pt = « etiquette »)
  et se posent en QUESTIONS_C (MOVE). Tenue.
- S04. « Les » : les 3 questions rentrent dans l'étiquette (kit.vanish into) ; `barre_temps` s'étire en BARRE_C
  (sx 0 -> 1 ou pop). Quatre prélèvements, « prélevés », « année, », « monte », « baisse. » : une case de plus
  (value k/20), l'étiquette bascule de TILT puis revient, `jetonK` naît au haut du remplissage côté étiquette
  (x ≈ 600, level_y du niveau courant) et tombe (kit.drop) dans BAC_SLOTS[k], la colonne perd TOKEN_DV ; au 1er,
  `bac` pop et `barre_1an` s'inscrit. « marché » : `vague` (échelle VAGUE_S04_K, sa pilule `vague_marche` enfant)
  tombe en VAGUE_S04. « monte » : la vague monte de 60 px ; « baisse. » : elle descend de 120 px. Fin : 4 jetons,
  colonne à LEVELS["S04"] (0,47), 4 cases. Garde la cause visible : la bascule de l'étiquette PRÉCÈDE chaque chute.
- S05. « l’argent » : les 4 jetons battent ensemble. « travaille » : `epargne_plus` pop, colonne 0,47 -> 0,53,
  case 5 ; `bac_zero` « + 0 € » pop au-dessus du bac, les jetons immobiles. « suivantes. » : « + » et « + 0 € »
  rebattent, colonne -> 0,59, case 6. Tenue.
- S06. « Résultat : » : `vague` sort (vanish) ; les 4 jetons glissent dans `pile` qui naît en PILE_C à PILE_BASE
  (relais : kit.morph(jetons, [], …) + pop de la pile) ; `epargne_plus`, `bac_zero` s'effacent. « 10 000 € » :
  `epargne_montant` bat (peak 1,12). « 20 ans, » : `barre_temps` value -> 1 (18 images, linéaire), `barre_20ans`
  pop. « 1 % » : l'étiquette bat et bascule de -8°. « coûter » : `pile_gains` pop puis value 0 -> PILE_GAINS_V
  (MOVE, out), les `pile_plusK` naissent bloc par bloc. « 4 600 €. » : `pile_plusde` et `pile_montant` (rouge)
  pop. Tenue (≥ 1 s : c'est le moment clé).
- S07. « D’où » : `question` naît sous la pointe du stylo de « Toi » (kit.pop from_pt = c.toi.tip(f - 1)).
  « écart ? » : il vole en QUESTION_ECART (MOVE, arc). « Regarde » (1er temps, morph 11) : `bac` s'efface ;
  `epargne` -> `graph_point` (relais apparié ; `epargne_montant` part avec la colonne et `graph_montant` pop) ;
  `barre_temps` + labels -> `axe_x` (relais) et `axe_20ans` ; `etiquette_mot` s'efface (FADE), `ficelle` se retire
  (piste from 0 -> 1, ou draw -> 0) et l'étiquette descend en ETIQ_GRAPH. La pile et son chiffre ne bougent pas
  encore. « calcul, » : `axe_y` se trace (kit.draw 9) ; 6 images plus tard, `pile`, `pile_gains`, `pile_plusde`
  se réduisent dans `pile_montant`, qui monte en RED_HIGH pendant que `question` monte en QUESTION_HIGH (MOVE).
  « théorique, » : `mention1` et `mention2` en fondu. « garanti. » : `mention_trait` se trace (kit.draw 9).

Raccord vers p2 : à l'image 982, l'état est exactement ENTRY_P2 (graphique vide, chiffre rouge et « ? » en haut à
droite, mention soulignée, étiquette en ETIQ_GRAPH, échelle 1, rot 0) ; « Toi » en P_TOI, stylo au repos.
Rien de ce que p1 commence ne dépasse l'image 982.
"""
from pipeline.story import DRAW, FADE, MORPH, MOVE, POP, STRETCH

from . import (BAC_RIM, BAC_SLOTS, BAC_ZERO, BARRE_C, BARRE_W, BARRE_N, EPARGNE_C, EPARGNE_PLUS, ETIQ_GRAPH,
               ETIQ_HOME, ETIQ_PESE, GRAPH_MONTANT, LEVELS, P_TOI, PILE_BASE, PILE_C, PILE_GAINS_V, PILE_H0, PILE_X,
               QUESTION_ECART, QUESTION_HIGH, QUESTIONS_C, RED_HIGH, TILT, TOKEN_DV, VAGUE_S04, VAGUE_S04_K, level_y,
               scene_f0)

F_START, F_END = 0, 982

# --- places propres à cette partie ---
JETON_X = 590                      # S04 : un jeton naît au haut du remplissage, côté étiquette
JETON_HOP = 50                     # il est arraché vers le haut avant de tomber (px)
JETON_FALL = 13                    # images de vol jusqu'au bac
VAGUE_FROM_Y = VAGUE_S04[1] - 240  # S04 « marché » : la vague tombe de 240 px
# S06 « coûter » : les gains perdus forment une jauge de 240 px posée sur la base cyan (y 1060 -> 820), à l'intérieur
# du tube de la pile (y 720-1120) : à h = 400 (distribution), son contour dépasserait le tube jusqu'à y 660 et
# couperait « 4 600 € ». On règle sa piste h quand elle est encore invisible ; value 0 -> 1 = 0 -> PILE_GAINS_V du tube.
GAINS_H = round(PILE_H0 * PILE_GAINS_V)                    # 240
GAINS_BASE = BAC_RIM - PILE_H0 * PILE_BASE                 # 1060
GAINS_C = [PILE_X, GAINS_BASE - GAINS_H / 2]               # (150, 940)
GAINS_BLOCK = GAINS_H / 8                                  # 30 px (8 segments)
PLUS_DY = [round(GAINS_H / 2 - GAINS_BLOCK * (2 * k + 0.5), 1) for k in range(4)]   # « + » dans les blocs 1, 3, 5, 7
PILE_FROM = [PILE_X, BAC_RIM - 20]                         # S06 : la pile naît du fond du bac
PEN_UP = [705, 975]                                        # S07 « D’où » : « Toi » lève le stylo (allonge 175 px)


def jeton_flight(S, jid, f, start, end):
    """Le jeton arraché : petit bond vers le haut puis chute en parabole jusqu'à sa place dans le bac -> f + JETON_FALL."""
    (x0, y0), (x1, y1) = start, end

    def at(p):
        return [round(x0 + (x1 - x0) * p, 2), round(y0 + (y1 - y0) * p * p - 4 * JETON_HOP * p * (1 - p), 2)]
    S.path(jid, f, JETON_FALL, "linear", at)
    return f + JETON_FALL


def part(S, kit, c):
    toi = c.toi
    kit.pin(0 - 1, {
        "epargne": {"pos": list(EPARGNE_C), "scale": 1, "opacity": 1, "value": LEVELS["S01"]},
        "etiquette": {"pos": list(ETIQ_HOME), "scale": 0, "rot": 0},
        "etiquette_mot": {"opacity": 0}, "ficelle": {"draw": 0, "from": 0},
        "barre_temps": {"scale": 0, "value": 0}, "bac": {"scale": 0}, "pile": {"scale": 0},
        "pile_gains": {"scale": 0}, "vague": {"scale": 0}, "question": {"scale": 0},
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
                                "prix accroché à l'épargne")
    S.key("etiquette", "scale", f, 0.6, MORPH, "out")

    # ================= S02 : le petit prix pèse =================
    f = kit.at("S02", "Pourtant,", "l'étiquette reprend sa taille (échelle 1)")
    S.key("etiquette", "scale", f, 1, MORPH, "out")

    f = kit.at("S02", "épargne,", "la colonne de l'épargne, son disque euro et « 10 000 € » battent une fois")
    kit.pulse("epargne", f, peak=1.05)

    f = kit.at("S02", "facture", "l'étiquette descend de 150 px au bout de sa ficelle, qui s'allonge depuis le coin "
                                 "de la colonne")
    kit.move("etiquette", f, list(ETIQ_PESE))

    f = kit.at("S02", "lourde.", "sous la traction, le niveau de la colonne baisse d'un demi-bloc (0,60 -> 0,55) ; "
                                 "l'étiquette descend encore de 20 px. Tenue")
    S.key("epargne", "value", f, LEVELS["S02"], 10, "out")
    kit.move("etiquette", f, [ETIQ_PESE[0], ETIQ_PESE[1] + 20], d=10, e="out")

    # ================= S03 : trois questions sortent de l'étiquette =================
    f = kit.at("S03", "Dans", "l'étiquette et son mot « frais » remontent à leur place ; la colonne reste baissée "
                              "(0,55)")
    kit.move("etiquette", f, list(ETIQ_HOME))

    for k, mot, txt in ((0, "combien", "« Combien ? »"), (1, "viennent,", "« D’où ? »"),
                        (2, "connaître.", "« Comment ? »")):
        f = kit.at("S03", mot, f"la pilule {txt} sort de l'étiquette et va se poser en haut"
                   + (" (à côté des précédentes). Tenue" if k == 2 else ""))
        q = f"question{k + 1}"
        S.key(q, "pos", f - 1, list(ETIQ_HOME))
        kit.pop(q, f)
        S.key(q, "pos", f, list(QUESTIONS_C[k]), MOVE, "inOut", 50)

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
        remplissage et tombe dans le bac ; la colonne perd TOKEN_DV. -> image d'arrivée du jeton."""
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
        return jeton_flight(S, j, g + 3, start, list(BAC_SLOTS[k]))

    f = kit.at("S04", "prélevés", "1re année : la case 1 se remplit et « 1 an » s'inscrit dessous ; le bac « frais » "
                                  "surgit à gauche ; l'étiquette bascule contre la colonne, puis un jeton se détache "
                                  "du haut du remplissage et tombe dans le bac")
    kit.pop("bac", f)
    kit.pop("barre_1an", f + 2)
    levy(0, f)

    f = kit.at("S04", "année,", "2e année : case 2 ; même bascule de l'étiquette ; un 2e jeton tombe dans le bac")
    levy(1, f)

    f = kit.at("S04", "marché", "la vague du marché, sa pilule « marché » dessous, tombe à gauche sous la barre")
    S.key("vague", "pos", f - 1, [VAGUE_S04[0], VAGUE_FROM_Y])
    S.key("vague", "scale", f, VAGUE_S04_K)
    S.key("vague", "pos", f, list(VAGUE_S04), 10, "out")

    f = kit.at("S04", "monte", "la vague monte de 60 px ; 3e année : case 3, bascule, un 3e jeton tombe quand même")
    S.key("vague", "pos", f, [VAGUE_S04[0], VAGUE_S04[1] - 60], 12, "inOut")
    levy(2, f)

    f = kit.at("S04", "baisse.", "la vague descend de 120 px ; 4e année : case 4, bascule, un 4e jeton tombe quand "
                                 "même. Tenue")
    S.key("vague", "pos", f, [VAGUE_S04[0], VAGUE_S04[1] + 60], 12, "inOut")
    end = levy(3, f)
    assert abs(level[0] - LEVELS["S04"]) < 1e-6 and end < scene_f0(S, "S05"), (level, end)

    # ================= S05 : la colonne grossit, le bac fait « + 0 € » =================
    f = kit.at("S05", "l’argent", "les 4 jetons du bac battent ensemble : c'est l'argent prélevé")
    for k in range(4):
        kit.pulse(f"jeton{k + 1}", f, peak=1.15)

    f = kit.at("S05", "travaille", "une année de plus (case 5) : un « + » surgit à côté de « 10 000 € » et la colonne "
                                   "monte (0,47 -> 0,53) ; au-dessus du bac, « + 0 € » surgit, les jetons ne bougent pas")
    S.key("barre_temps", "value", f, 5 / BARRE_N, 6, "out")
    kit.pop("epargne_plus", f)
    S.key("epargne", "value", f, 0.53, 10, "out")
    kit.pop("bac_zero", f)

    f = kit.at("S05", "suivantes.", "encore une année (case 6) : le « + » rebat, la colonne monte (0,53 -> 0,59) ; "
                                    "« + 0 € » rebat au-dessus du bac immobile. Tenue")
    S.key("barre_temps", "value", f, 6 / BARRE_N, 6, "out")
    kit.pulse("epargne_plus", f, peak=1.2)
    S.key("epargne", "value", f, LEVELS["S05"], 10, "out")
    kit.pulse("bac_zero", f, peak=1.2)

    # ================= S06 : la pile de 20 ans : plus de 4 600 € =================
    f = kit.at("S06", "Résultat :", "la vague « marché » se réduit et sort ; les 4 jetons glissent au fond du bac et "
                                    "deviennent la base cyan d'une pile qui monte du bac ; « + » et « + 0 € » s'effacent")
    kit.vanish("vague", f)
    for k in range(4):
        kit.vanish(f"jeton{k + 1}", f, into=[PILE_X, BAC_RIM - 30], d=MORPH)
    kit.vanish("epargne_plus", f)
    kit.vanish("bac_zero", f)
    kit.pop("pile", f + 2, from_pt=PILE_FROM, to=list(PILE_C), d=MORPH)

    f = kit.at("S06", "10 000 €", "« 10 000 € » au-dessus de la colonne bat")
    kit.pulse("epargne_montant", f, peak=1.12, step=4)

    f = kit.at("S06", "20 ans,", "la barre du temps se remplit jusqu'à la 20e case ; « 20 ans » surgit sous son bout")
    S.key("barre_temps", "value", f, 1, 18, "linear")
    kit.pop("barre_20ans", f + 12)

    f = kit.at("S06", "1 %", "l'étiquette « 1 % / an » bat et bascule de -8° vers la colonne, puis se redresse")
    kit.pulse("etiquette", f, peak=1.12, step=4)
    S.key("etiquette", "rot", f, -8, 5, "out")
    S.key("etiquette", "rot", f + 12, 0, 8, "inOut")

    f = kit.at("S06", "coûter", "sur la base cyan de la pile monte une jauge claire, un « + » par bloc : les gains "
                                "que l'argent prélevé n'a pas faits (y 1060 -> 820)")
    kit.ensure("pile_gains", "h", PILE_H0)                             # h de la distribution, puis 240 px
    S.key("pile_gains", "h", f - 1, GAINS_H)
    S.key("pile_gains", "pos", f - 1, list(GAINS_C))
    for k, dy in enumerate(PLUS_DY):
        S.key(f"pile_plus{k + 1}", "pos", f - 1, [0, dy])
    S.key("pile_gains", "scale", f, 1)
    S.key("pile_gains", "value", f, 1, MOVE, "out")
    for k in range(4):                                                  # chaque « + » quand son bloc est rempli
        kit.pop(f"pile_plus{k + 1}", f + (1, 3, 5, 8)[k], d=6)

    f = kit.at("S06", "4 600 €.", "« plus de » et « 4 600 € » en rouge surgissent au-dessus de la pile. Tenue")
    kit.pop("pile_plusde", f)
    kit.pop("pile_montant", f + 2)

    # ================= S07 : d'où vient l'écart ? Tout se réarrange en graphique vide =================
    f = kit.at("S07", "D’où", "« Toi » lève le stylo ; un grand « ? » naît sous sa pointe")
    toi.reach(f, PEN_UP, d=8)
    tip = toi.tip(f + 7)
    kit.pop("question", f + 6, from_pt=tip, to=[tip[0] - 10, tip[1] - 60])

    f = kit.at("S07", "écart ?", "le « ? » vole en arc et se pose contre le « 4 600 € » rouge")
    kit.move("question", f, list(QUESTION_ECART), arc=70)
    toi.rest(f + 2, d=10)

    f = kit.at("S07", "Regarde", "réarrangement : le bac s'efface ; la colonne se réduit en un point de départ et "
                                 "« 10 000 € » s'y pose ; la barre du temps descend et devient l'axe horizontal "
                                 "« 20 ans » ; « frais » et la ficelle s'effacent ; l'étiquette se range sous l'axe")
    born = S.to_world("epargne_montant", [0, 0], f - 1)
    # la pile ne part qu'à « calcul, » + 6 : jusque-là, le point de départ et « 10 000 € » passent DEVANT elle
    for x, z0 in (("graph_point", 4), ("graph_montant", 4.1)):
        kit.ensure(x, "z", z0)
        S.key(x, "z", f, 7.4)
        S.key(x, "z", f + 40, z0)                                      # pile rentrée (calcul, + 6 + 11) : calque normal
    kit.vanish("bac", f)
    kit.morph(["epargne", "barre_temps", "barre_20ans", "barre_1an"], ["graph_point", "axe_x", "axe_20ans"], f,
              pair=True)
    kit.pop("graph_montant", f, from_pt=born, to=list(GRAPH_MONTANT), d=MORPH)
    kit.fade("etiquette_mot", f, to=0)
    S.key("ficelle", "from", f, 1, 6, "in")
    S.key("ficelle", "draw", f + 6, 0)                                  # fil rentré : remis à zéro, invisible
    S.key("ficelle", "from", f + 6, 0)
    kit.move("etiquette", f, list(ETIQ_GRAPH))

    f = kit.at("S07", "calcul,", "l'axe vertical se trace ; puis la pile se réduit dans son chiffre rouge, qui monte "
                                 "en haut à droite avec son « ? »")
    kit.draw("axe_y", f, DRAW)
    g = f + 6
    into = S.to_world("pile_montant", [0, 0], g - 1)
    for x in ("pile", "pile_gains", "pile_plusde"):                  # la pile rentre dans son chiffre, sur place
        kit.vanish(x, g, into=into, d=POP)
    kit.move("pile_montant", g + 5, list(RED_HIGH))                    # puis le chiffre monte avec son « ? »
    kit.move("question", g + 5, list(QUESTION_HIGH))

    f = kit.at("S07", "théorique,", "la mention « Exemple théorique, / rendement non garanti » s'inscrit en fondu en "
                                    "haut")
    kit.fade("mention1", f)
    kit.fade("mention2", f)

    f = kit.at("S07", "garanti.", "« non garanti » se souligne en cyan profond. Tenue")
    end = kit.draw("mention_trait", f, DRAW)
    assert end <= F_END, end
