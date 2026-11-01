"""V13, partie 1 : S01-S08, images 0-986 (40 temps forts, 32,9 s). Accroche (le solde regardé, réduit à une case sur
neuf), l'équation « grille − carte grise = Patrimoine net », la cible « Ta stratégie », le repère 1-2-3, point 1 :
la case du solde éclairée puis six cases nommées, chacune par un nom que le stylo de « Toi » émet.

ÉTAT D'ENTRÉE : l'image 0 du film = l'état de distribution (cast). SORTIE : ENTRY_P2 à l'image 986 (voir __init__.py).

Tour de revue 1 (aucun temps fort déplacé) :
- S02 « Ce » : relais carte -> case en 10 images (out) : la pilule est presque posée quand elle bat sur « chiffre »
  (×1,2) ;
- S06 : la cible et « Ta stratégie » rentrent dans « Patrimoine net », qui rentre dans le disque 3 « Limites » (rangés
  pour plus tard, plus de pilule qui rétrécit sur place) ;
- S08 : « Fais » : le stylo se lève à 40 px du bas de la grille ; « liste » : il la touche (contact 2 images après le
  mot), la rangée du bas bat ; puis, sur chaque nom, la pointe donne un petit coup en place et une pilule-libellé
  (« Comptes », « Livrets »…) en naît et vole en arc (10 images) dans sa case « ? », qui devient la case nommée à son
  arrivée ; « PER. » : stylo baissé après le dernier vol.
"""
import math

from pipeline.story import DRAW, MORPH, MOVE, POP

from . import (CASE_IDS, CASES, CELL_LOCAL, COMPTE_H0, COMPTE_ICO_CELL, COMPTE_ICO_CELL_K, COMPTE_MOT_CELL,
               COMPTE_MOT_CELL_K, COMPTE_W0, CELL_H, CELL_W, DEEP, DISQUE2, DISQUE3, GRILLE_FULL, HEAD_P1, INK, LIGHT,
               LBL_TEXTS, MARKER_LEGENDS, NET_C, NET_PEN, NET_PEN_TRACE, NOM_RIGHT, PAPER, Q_IDS, QUESTION_C,
               REGARD_CASE, SHOULDER_DX, SHOULDER_DY, SOLDE_C0, SOLDE_CELL_FULL, SOLDE_CELL_K, T_COMPTES, TAP_GRILLE,
               TOI_P1, TOI_P2, bez, cell_world, drop_in, grid_world, move_with_grid, ring)

NOM_HI, NOM_HI_K = (40, -125), 0.94             # pilule « Toi » quand la grille est PLEINE (S02, S04-S08)
RELAY_D = 10                                    # S02 : relais carte -> case (out)
LBL_FLY = 10                                    # S08 : vol d'une pilule-libellé, de la pointe à sa case


def _pulse_xy(kit, id, f, peak, step=3, times=1):
    """Battement sur les pistes sx / sy (multiplient l'échelle) : se superpose à un déplacement ou à une apparition
    en cours sur la piste scale sans la couper."""
    kit.pulse(id, f, times=times, peak=peak, step=step, track="sx")
    return kit.pulse(id, f, times=times, peak=peak, step=step, track="sy")


def part(S, kit, c):
    toi = c.toi
    # état d'entrée = distribution (image 0) : rien à imposer ; épingle sans effet, pour mémoire du contrat
    kit.pin(0 - 1, {"grille": {"pos": list(GRILLE_FULL), "scale": 1}, "solde": {"pos": list(SOLDE_C0), "scale": 1},
                    "compte": {"w": COMPTE_W0, "h": COMPTE_H0}})
    toi.lower(0, 1)                              # « Toi » bras baissé dès l'image 0, stylo tenu bas : aucun mouvement

    # ================= S01 « Tu regardes ton solde bancaire pour savoir où tu en es ? » =================
    f = kit.at("S01", "regardes", "un trait de regard en tirets encre se tend de la tête de « Toi » au bas de la "
                                  "carte « Solde »")
    kit.draw("regard", f, DRAW)
    f = kit.at("S01", "solde", "la pilule cyan « 3 200 € » bat deux fois (×1,1) ; rien d'autre ne bouge")
    kit.pulse("solde", f, times=2, step=3, peak=1.1)
    f = kit.at("S01", "où", "un grand « ? » sort de la tête de « Toi » et se pose à sa gauche")
    kit.pop("question", f, from_pt=HEAD_P1, to=list(QUESTION_C))

    # ================= S02 « Ce chiffre ne dit presque rien. » =================
    f = kit.at("S02", "Ce", "la carte « Solde » se réduit en petite case en haut à gauche, la pilule « 3 200 € » "
                            "dessus ; le regard suit la case ; le « ? » rentre dans la tête de « Toi »")
    kit.move("compte", f, list(CELL_LOCAL[0]), d=RELAY_D, e="out")
    S.key("compte", "w", f, CELL_W, RELAY_D, "out")
    S.key("compte", "h", f, CELL_H, RELAY_D, "out")
    kit.move("compte_ico", f, list(COMPTE_ICO_CELL), d=RELAY_D, e="out", scale=COMPTE_ICO_CELL_K)
    kit.move("compte_mot", f, list(COMPTE_MOT_CELL), d=RELAY_D, e="out", scale=COMPTE_MOT_CELL_K)
    kit.vanish("compte_filet", f, d=8)
    kit.move("solde", f, list(SOLDE_CELL_FULL), d=RELAY_D, e="out", scale=SOLDE_CELL_K)
    S.key("regard", "pb", f, list(REGARD_CASE), RELAY_D, "out")
    kit.vanish("question", f, into=HEAD_P1)
    kit.move("nom_toi", f, list(NOM_HI), scale=NOM_HI_K)   # la grille pleine arrive : la pilule se décale (18 px)
    f = kit.at("S02", "chiffre", "la pilule « 3 200 € », presque posée dans sa case, bat nettement (×1,2)")
    _pulse_xy(kit, "solde", f, 1.2)
    f = kit.at("S02", "presque", "huit cases « ? » en tirets sortent une à une de derrière la case du solde et "
                                 "glissent à leurs places : une grille 3 × 3")
    for i in range(1, 9):
        kit.pop(Q_IDS[i], f + 2 * (i - 1), to=list(CELL_LOCAL[i]), d=POP)
    f = kit.at("S02", "rien.", "les huit cases « ? » battent ensemble (×1,06) et restent vides")
    for i in range(1, 9):
        _pulse_xy(kit, Q_IDS[i], f, 1.06)

    # ================= S03 « Dans cette vidéo, on va voir comment calculer ton patrimoine net. … » =================
    f = kit.at("S03", "Dans", "la grille se réduit (×0,6) en haut à gauche, la pilule du solde avec elle ; le "
                              "regard rentre dans la tête de « Toi »")
    move_with_grid(kit, f, small=True)
    regard_local = (REGARD_CASE[0] - GRILLE_FULL[0], REGARD_CASE[1] - GRILLE_FULL[1])
    S.key("regard", "pb", f, grid_world(regard_local, small=True), MOVE, "inOut")
    g = kit.draw("regard", f + 4, DRAW, to=0)   # le bout rentre vers l'œil (draw 1 -> 0) ; from reste à 0
    f = kit.at("S03", "voir", "« Toi » marche vers la gauche, sous la grille ; sa pilule passe à droite de sa tête")
    toi.walk(f, TOI_P2[0], d=MOVE, low=True)
    kit.move("nom_toi", f, list(NOM_RIGHT), d=MOVE)
    f = kit.at("S03", "calculer", "« Toi » lève son stylo sous la grille")
    toi.reach(f, list(NET_PEN), d=DRAW)
    f = kit.at("S03", "patrimoine", "la pilule « Patrimoine net » naît sous la pointe du stylo et se pose sous la "
                                    "grille")
    kit.pop("net", f, from_pt=list(NET_PEN), to=list(NET_C))
    f = kit.at("S03", "net.", "« Patrimoine net » bat (×1,08) ; aucun signe autour d'elle")
    kit.pulse("net", f, step=3, peak=1.08)
    f = kit.at("S03", "lire", "la pointe du stylo glisse sous « Patrimoine net » : un trait deep la souligne de "
                              "bout en bout")
    hits = toi.trace(f, [list(p) for p in NET_PEN_TRACE])
    kit.draw("net_trait", hits[0], 19, e="linear")
    f = kit.at("S03", "chiffre.", "la pilule « 3 200 € » bat dans la grille, puis « Patrimoine net » : deux "
                                  "chiffres différents ; « Toi » baisse le stylo")
    kit.pulse("solde", f, step=3)
    kit.pulse("net", f + 6, step=3, peak=1.08)
    toi.lower(max(f + 2, hits[-1] + 1), 8)

    # ================= S04 « Ton patrimoine net, c’est tout ce que tu possèdes, moins tout ce que tu dois. » ====
    f = kit.at("S04", "Ton", "« Toi » revient à sa place en bas à droite, stylo baissé ; sa pilule repasse "
                             "au-dessus de sa tête")
    g = toi.walk(f, TOI_P1[0], d=24, low=True)
    kit.move("nom_toi", f, list(NOM_HI), d=g - f)
    f = kit.at("S04", "tout", "un cadre deep se trace autour de toute la grille")
    kit.draw("cadre", f, DRAW)
    f = kit.at("S04", "possèdes,", "« Ce que tu possèdes » s'écrit au-dessus de la grille, puis se souligne")
    kit.type("entete", f)                       # pas de soulignement : il tomberait sur le bord haut du cadre deep
    f = kit.at("S04", "moins", "un « − » apparaît à droite de la grille")
    kit.pop("moins", f)
    f = kit.at("S04", "dois.", "la carte grise « Ce que tu dois » tombe à droite du « − » ; puis « = » se pose "
                               "devant « Patrimoine net » : l'équation se ferme")
    drop_in(kit, "dettes", f)
    kit.pop("egal", f + 11)

    # ================= S05 « C’est la photo la plus honnête de ta situation. … stratégie patrimoniale. » ========
    f = kit.at("S05", "photo", "deux fils deep relient la grille encadrée et la carte grise à « Patrimoine net »")
    kit.draw("fil_grille", f, DRAW)
    kit.draw("fil_dettes", f + 3, DRAW)
    f = kit.at("S05", "honnête", "« Patrimoine net » grandit (×1,15) et reste grande")
    kit.move("net", f, list(NET_C), d=10, scale=1.15, e="out")
    f = kit.at("S05", "situation.", "« Toi » se penche vers l'équation et sa pilule « Toi » bat : c'est sa "
                                    "situation ; il se redresse")
    toi.lean_to(f, -6, d=14)
    toi.hold_low(f, f + 14)                      # bras baissé pendant qu'il se penche
    kit.pulse("nom_toi", f, step=3, peak=round(NOM_HI_K * 1.1, 4))
    g = f + 12 + 14
    toi.hold_low(f + 14, g)
    toi.lean_to(g, 0, d=14)
    toi.hold_low(g, g + 14)
    f = kit.at("S05", "point", "une cible tombe en bas à gauche")
    drop_in(kit, "cible", f)
    f = kit.at("S05", "départ", "un point cyan naît au bas gauche de « Patrimoine net » ; une flèche deep en part "
                                "jusqu'à la cible")
    kit.pop("depart", f, d=6)
    kit.draw("fleche", f + 6, 13)
    kit.pop("fleche_pointe", f + 6 + 11, d=4)
    f = kit.at("S05", "stratégie", "la cible bat et une onde deep part de son centre : la flèche l'atteint")
    kit.pulse("cible", f, step=3, peak=1.08)
    ring(S, "cible_onde", f, d=18)
    f = kit.at("S05", "patrimoniale.", "« Ta stratégie » s'écrit sous la cible")
    kit.type("strategie", f)

    # ================= S06 « Pourquoi commencer par ce que tu possèdes ? » =================
    f = kit.at("S06", "Pourquoi", "la cible et « Ta stratégie » rentrent dans « Patrimoine net » ; la flèche, les "
                                  "fils, le cadre, « − » et « = » se réduisent ; le repère 1-2-3 naît en haut et « Ce "
                                  "que tu possèdes » devient sa légende 1")
    kit.morph(["depart", "fleche_pointe", "cadre", "moins", "egal"], [], f)
    kit.vanish("cible", f, into="net", d=MORPH)
    kit.vanish("strategie", f + 1, into="net", d=MORPH)
    for w in ("fleche", "fil_grille", "fil_dettes"):
        g = kit.draw(w, f, 6, track="from")
        S.key(w, "draw", g, 0)                   # invisible : remis à draw 0 / from 0 (contrat ENTRY_P2)
        S.key(w, "from", g, 0)
    kit.pop("marqueur", f, d=MORPH)
    kit.vanish("entete", f, into=list(MARKER_LEGENDS[0]), d=MORPH)
    f = kit.at("S06", "commencer", "la carte grise rentre dans le disque 2 « Dois » ; « Patrimoine net » (avec la "
                                   "cible) rentre dans le disque 3 « Limites » : rangés pour plus tard")
    kit.vanish("dettes", f, into=list(DISQUE2), d=MORPH)
    g = kit.vanish("net", f + 3, into=list(DISQUE3), d=MORPH)
    S.key("net_trait", "draw", g, 0)
    f = kit.at("S06", "possèdes ?", "le disque 1 « Possèdes » s'allume en cyan ; la grille revient à pleine taille")
    S.key("marqueur", "on", f, 1, POP, "out")
    move_with_grid(kit, f, small=False)

    # ================= S07 « Parce que ton solde n’en montre souvent qu’une partie. » =================
    f = kit.at("S07", "solde", "la pilule « 3 200 € » bat deux fois dans sa case")
    kit.pulse("solde", f, times=2, step=3, peak=round(SOLDE_CELL_K * 1.12, 4))
    f = kit.at("S07", "montre", "la case du solde s'éclaire en cyan pâle, contour deep : c'est tout ce que montre "
                                "le solde")
    S.key("compte", "fill", f, LIGHT, DRAW, "out")
    S.key("compte", "stroke", f, DEEP, DRAW, "out")
    f = kit.at("S07", "partie.", "les huit cases « ? » battent deux fois, toujours vides")
    for i in range(1, 9):
        kit.pulse(Q_IDS[i], f, times=2, step=2, peak=1.06)

    # ================= S08 « Fais la liste complète : comptes, livrets, assurance-vie, PEA, épargne salariale, PER. »
    f = kit.at("S08", "Fais", "« Toi » lève son stylo vers le bas de la grille")
    sx, sy = TOI_P1[0] - SHOULDER_DX, TOI_P1[1] + SHOULDER_DY
    u = math.hypot(TAP_GRILLE[0] - sx, TAP_GRILLE[1] - sy)
    hover = [TAP_GRILLE[0] - (TAP_GRILLE[0] - sx) * 40 / u, TAP_GRILLE[1] - (TAP_GRILLE[1] - sy) * 40 / u]
    toi.reach(f, hover, d=DRAW)
    f = kit.at("S08", "liste", "la pointe frappe le bas de la grille ; les trois « ? » de la rangée du bas battent")
    hit = toi.tap(f - 1, list(TAP_GRILLE), d=4)
    for i in (6, 7, 8):
        _pulse_xy(kit, Q_IDS[i], hit, 1.08, step=2)

    def emit(f, i, target):
        """Coup de pointe en place (contact sur f) ; la pilule-libellé i en naît et vole en arc jusqu'à `target`
        (point monde). Renvoie l'image d'arrivée."""
        toi.tap(f - 3, list(TAP_GRILLE), d=4)
        lid = f"lbl_{i}"
        a, b = list(TAP_GRILLE), list(target)
        c = [(a[0] + b[0]) / 2 + 40, min(a[1], b[1]) - 70]
        S.key(lid, "pos", f - 1, a)
        S.key(lid, "scale", f - 1, 0)
        S.path(lid, f, LBL_FLY, "inOut", bez(a, c, b), scale_at=lambda p: min(1.0, 0.35 + 1.6 * p))
        arr = f + LBL_FLY
        kit.vanish(lid, arr, d=6)
        return arr

    f = kit.at("S08", "comptes,", "la pointe donne un coup : « Comptes » en sort et vole sur la case du solde, qui "
                                  "repasse au papier ; « Solde » y devient « Comptes » ; la pilule ne bouge pas")
    c0 = grid_world((CELL_LOCAL[0][0] + COMPTE_MOT_CELL[0] + 75, CELL_LOCAL[0][1] + COMPTE_MOT_CELL[1]))
    arr = emit(f, 0, c0)
    S.key("compte", "fill", f, PAPER, 3, "out")
    S.key("compte", "stroke", f, INK, 3, "out")
    S.key("compte_mot", "text", arr - 1, T_COMPTES)
    S.key("compte_mot", "chars", arr - 1, 0)
    kit.type("compte_mot", arr, n=len(T_COMPTES), rate=3)
    for i, mot, what in ((1, "livrets,", "« Livrets » sort de la pointe et vole dans la case « ? » à droite du solde, "
                                         "qui devient la case « Livrets »"),
                         (2, "assurance-vie,", "« Assurance-vie » sort de la pointe et vole en haut à droite : la "
                                               "case devient « Assurance-vie »"),
                         (3, "PEA,", "« PEA » sort de la pointe et vole au milieu à gauche : case « PEA »"),
                         (4, "épargne", "« Épargne salariale » sort de la pointe et vole au centre : case « Épargne "
                                        "salariale »"),
                         (5, "PER.", "« PER » sort de la pointe et vole au milieu à droite : case « PER » ; « Toi » "
                                     "baisse le stylo")):
        f = kit.at("S08", mot, what)
        two = "\n" in CASES[i][1]
        arr = emit(f, i, cell_world(i, False, 48 if two else 52))
        kit.morph(Q_IDS[i], CASE_IDS[i], arr - 3)
        kit.type(f"{CASE_IDS[i]}_mot", arr, rate=3)
    toi.lower(arr + 4, 8)
