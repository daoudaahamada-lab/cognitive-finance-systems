"""V13, partie 3 : S16-S22, images 1916-2768 (36 temps forts, 28,4 s). Point 3 « Limites » : « Patrimoine net » naît
sous la grille, signe d'attention 72 px et fente ; il monte à droite, relié au cadre de toute la grille ; six pastilles
sortent chacune de sa case (attache en tirets), passent par la pilule (elle bat : « il mélange ») et se rangent par
paires opposées (« ↔ ») ; deux restent sous la pilule avec l'œil de « Toi », qui les regarde l'une après l'autre ; une
courbe de mesures naît sous la pointe ; chute : l'équation complète, « Toi » barre son regard rouge vers le solde et
regarde longuement le Patrimoine net ; fin : la pilule du solde devient le bouton « S’abonner ».

ÉTAT D'ENTRÉE : ENTRY_P3 épinglé à 1915. SORTIE : fin du film (dernière image 2768).

Tour de revue 1 (aucun temps fort déplacé ; écarts de mise en scène) :
- S16 « point, » : le jeton rentre dans sa case par-dessous la grille (il ne traverse plus les cases) ;
- S16 « moindre : » : « Patrimoine net » sort du bord BAS de la grille réduite et se pose en (540, 960), sa place de
  S03-S05 (ease out : lisible dès +3) ; « limites. » : signe d'attention 72 px, qui bat deux fois avec la légende 3,
  puis une fente encre traverse la pilule entre « Patrimoine » et « net » ;
- S17 « mélange » : la pilule monte en (735, 540) pendant que le cadre deep se retrace autour de toute la grille et
  qu'un fil part du milieu de son bord droit vers la pilule ; chaque pastille : sa case s'allume (contour deep) et
  bat, une attache en tirets la relie à sa case, elle vole jusqu'au bas de la pilule (qui bat), puis descend à sa
  place ; les paires se remplissent de bas en haut (aucune pastille ne passe sur une autre) ; « ↔ » sur le second mot
  de chaque paire ;
- S18 « Utilise-le » : l'œil de « Toi » se pose sur « disponible » et « risqué » (le stylo ne les atteint pas depuis
  P1 : « Toi » se penche vers elles), qui montent sous la pilule ; « liquidité », « risques. » : le regard de « Toi »
  (tirets deep) va à l'une puis à l'autre (au lieu d'un soulignement) ;
- S19 : le stylo se lève au-dessus de l'axe dès la fin de S18 ; « calcule-le » : toucher en 4 images ; « fois » : les
  sept points naissent de la pointe et volent à leur place ;
- S20-S21 : la pilule du solde passe par la marge gauche et sous « = » ; « dois. » : regard long (la tête -> le bas
  de « Patrimoine net »), en tirets encre puis plein deep 4 images plus tard ; « Toi » se penche et sa pilule bat.
"""
from pipeline.story import DRAW, FADE, MORPH, MOVE, POP, STYLE  # noqa: F401

from . import (ALERTE_C, ALERTE_CHUTE, ALERTE_CHUTE_K, ALERTE_P3, AXE_TAP, CADRE_C, CASE_IDS, DEEP, DETTES_C,
               DETTES_H, DETTES_ICO_CARD, DETTES_MOT_CARD, DETTES_W, DISQUE2, EGAL_CHUTE, ENTRY_P3, FIN_BUTTON,
               FREQ_C, INK, JETON_SMALL, JETON_SMALL_K, JETON_P2, LOW_ROT_V13, MOINS_C, NET_C, NET_CHUTE,
               NET_CHUTE_K, NET_FROM_GRID, NOM_ABOVE, NOM_LEFT, NET_P3, NET_P3_K, OEIL_R, PAST_GARDE, PAST_TOUCH, PASTILLES, POINTS, RED,
               REGARD_BARRE, REGARD_EYE_S20, REGARD_GARDE_EYE, REGARD_NET, REGARD_SOLDE_S20, SHOULDER_DX,
               SHOULDER_DY, SOLDE_CELL_SMALL, SOLDE_H, SOLDE_OUT, SOLDE_OUT_K, SOLDE_SIZE, SOLDE_SMALL_K, T_ABONNER,
               T_DOIS_CARTE, TOI_P1, bez, bez3, film_end, past_src_id, ring, scene_f0)

LOW_ROT_LEFT = 180 - LOW_ROT_V13                # stylo baissé, côté gauche (comme p2)
PAST_POP_D, PAST_SMALL, LEG1, LEG2 = 3, 0.6, 8, 9   # S17 : naît à ×0,6 sur sa case, vole à la pilule, descend
POINT1_FROM = (600, 584)                        # S18 : sous le bord bas gauche de « Patrimoine net » (×0,85)
FIN_K = 112 / SOLDE_H                           # S22 : pilule 320 x 100 -> bouton 380 x 112 (x 1,12)
FIN_W = round(380 / FIN_K, 2)
FIN_BSIZE = round(SOLDE_SIZE * FIN_K, 1)
FIN_TAP_P3 = (700, 962)
FIN_DOIGT_FROM = (FIN_TAP_P3[0] + 90, FIN_TAP_P3[1] + 90)
GRAPHE = (["axes", "axe_y_pointe", "axe_x_pointe", "axe_y_mot", "axe_auj"]
          + [f"grad{k}" for k in (1, 2, 3)] + [f"grad{k}_mot" for k in (1, 2, 3)]
          + [f"point{k}" for k in range(1, 9)] + ["courbe", "graphe_freq"])
ECART = ["ecart_h", "ecart_v", "ecart_haut", "ecart_bas"]
SOLDE_OUT_C1, SOLDE_OUT_C2 = (60, 700), (60, 1200)   # S20-S21 : la marge gauche, sous « = »


def _toward_shoulder(pt, dist):
    sx, sy = TOI_P1[0] - SHOULDER_DX, TOI_P1[1] + SHOULDER_DY
    dx, dy = sx - pt[0], sy - pt[1]
    n = (dx * dx + dy * dy) ** 0.5
    return [round(pt[0] + dx * dist / n, 1), round(pt[1] + dy * dist / n, 1)]


def part(S, kit, c):
    toi = c.toi
    f0 = scene_f0(S, "S16")                     # 1916
    kit.pin(f0 - 1, {**ENTRY_P3, "fil_net": {"draw": 0, "from": 0}})
    if S.val("toi", "scale", f0 - 1) == 0:      # partie isolée : la figurine n'est pas entrée (sans effet ici)
        toi.enter(f0 - 10, at=list(TOI_P1))
    if abs(S.val(toi.pen, "rot", f0 - 1) - LOW_ROT_LEFT) > 2:   # partie isolée : stylo encore levé
        toi.lower(f0 - 12, d=8)

    # ================= S16 : dernier point, ce chiffre a ses limites =================
    f = kit.at("S16", "Dernier", "le disque actif du repère glisse de 2 à 3 « Limites » ; coche deep dans le disque 2")
    kit.step(f, 2)
    S.key("marqueur", "done1", f, 1, DRAW)

    f = kit.at("S16", "point,", "le calcul, « ≈ 70 000 € nets », la barre, son accolade et l'étiquette se réduisent "
               "dans le jeton ; le jeton rentre par-dessous dans sa case « Immobilier »")
    kit.stagger(["calc_b", "calc_a", "resultat", "fantome", "crochet_val", "crochet", "barre_maison", "barre",
                 "etiquette"], f, 1, kit.vanish, into="jeton")
    S.key("crochet_fil", "draw", f, 0, 5, "in")
    S.key("ficelle_jeton", "draw", f + 6, 0, 5, "in")
    g = f + 15                                  # l'étiquette est rentrée
    a = S.val("jeton", "pos", g - 1)
    k0 = S.val("jeton", "scale", g - 1)
    S.path("jeton", g, MOVE, "inOut", bez3(a, [620, 960], [JETON_SMALL[0], 960], list(JETON_SMALL)),
           scale_at=lambda p: k0 + (JETON_SMALL_K - k0) * min(1.0, 1.3 * p))
    kit.vanish("case_immo_place", g + MOVE - 5, d=6)

    f = kit.at("S16", "moindre :", "la pilule « Patrimoine net » sort du bord bas de la grille (le total de toutes "
               "les cases) et se pose dessous, au milieu")
    kit.pop("net", f, scale=1, from_pt=list(NET_FROM_GRID), to=list(NET_C), d=POP + 3, e="out")

    f = kit.at("S16", "chiffre", "« Patrimoine net » bat")
    kit.pulse("net", f, step=3, peak=1.1)

    f = kit.at("S16", "limites.", "un grand signe d'attention (72 px, encre) surgit au coin de « Patrimoine net » et "
               "bat deux fois avec la légende 3 « Limites » du repère ; puis une fente traverse la pilule")
    S.key("alerte", "pos", f - 1, list(ALERTE_C))
    g = kit.pop("alerte", f, scale=1, d=6)
    kit.pulse("alerte", g, times=2, step=3, peak=1.2)
    S.key("marqueur_leg3", "opacity", g, 1)
    S.key("marqueur_leg3", "mark", g, 1)
    kit.pulse("marqueur_leg3", g, times=2, step=3, peak=1.15)
    S.key("marqueur_leg3", "opacity", g + 12, 0, FADE)
    kit.draw("net_fente", g + 13, 6, e="linear")

    # ================= S17 : il mélange... =================
    f = kit.at("S17", "mélange", "« Patrimoine net » monte à droite ; un cadre deep se retrace autour de toute la "
               "grille et un fil le relie à la pilule")
    kit.move("net", f, list(NET_P3), scale=NET_P3_K)
    kit.move("alerte", f, list(ALERTE_P3))
    S.key("cadre", "pos", f - 1, list(CADRE_C))
    S.key("cadre", "scale", f - 1, 1)
    S.key("cadre", "opacity", f - 1, 1)
    S.key("cadre", "draw", f - 1, 0)
    kit.draw("cadre", f, DRAW)
    kit.draw("fil_net", f + 7, DRAW)

    words = [("disponible", "past_disponible"), ("bloqué,", "past_bloque"), ("sûr", "past_sur"),
             ("risqué,", "past_risque"), ("l’estimé", "past_estime"), ("réel.", "past_reel")]
    for k, (mot, pid) in enumerate(words):
        m, ico, place, src, _dash = PASTILLES[pid]
        sid = past_src_id(src)
        f = kit.at("S17", mot, f"sa case s'allume ; « {m} » en sort, attachée à elle par des tirets, vole jusqu'au "
                   f"bas de « Patrimoine net » (qui bat) puis descend à sa place"
                   + (" ; « ↔ » la lie à l'autre mot de la paire" if k % 2 else ""))
        spt = S.to_world(sid, [0, 0], f - 1)
        if src in (-1, 6):
            kit.pulse(sid, f, step=3)
        else:
            S.key(sid, "stroke", f, DEEP, 2, "out")
            S.key(sid, "stroke", f + 10, INK, 5, "inOut")
            kit.pulse(sid, f, step=3, peak=1.06)
        S.key(pid, "pos", f - 1, list(spt))
        g = kit.pop(pid, f, scale=PAST_SMALL, d=PAST_POP_D)
        kit.draw(f"lien_{pid}", f, 4)
        S.path(pid, g, LEG1, "inOut", bez(spt, [(spt[0] + PAST_TOUCH[0]) / 2, min(spt[1], PAST_TOUCH[1]) - 30],
                                         list(PAST_TOUCH)))
        h = g + LEG1
        kit.pulse("net", h - 1, step=2, peak=round(NET_P3_K * 1.06, 4))
        t = kit.draw(f"lien_{pid}", h - 2, 5, track="from")
        S.key(f"lien_{pid}", "draw", t, 0)
        S.key(f"lien_{pid}", "from", t, 0)
        ctrl = [640, place[1]] if place[0] < 400 else [(PAST_TOUCH[0] + place[0]) / 2, (PAST_TOUCH[1] + place[1]) / 2]
        S.path(pid, h, LEG2, "inOut", bez(list(PAST_TOUCH), ctrl, list(place)),
               scale_at=lambda p: PAST_SMALL + (1 - PAST_SMALL) * p)
        if k % 2:
            kit.pop(f"paire{k // 2 + 1}", h + LEG2 - 2, d=6)

    # ================= S18 : utilise-le comme repère =================
    f = kit.at("S18", "Utilise-le", "l'œil de « Toi » se pose sur « disponible » et « risqué », qui montent sous "
               "« Patrimoine net » ; « bloqué », « sûr », « estimé » et « réel » rentrent dans leur case ; le cadre "
               "et le fil se retirent ; « Toi » se penche vers elles")
    for pid in PAST_GARDE:
        kit.pop(f"oeil_{pid}", f, d=6)
    kit.move("nom_toi", f, list(NOM_LEFT))      # sa pilule passe à gauche : son regard montera au-dessus de sa tête
    toi.lean_to(f, -5, d=10)
    toi.hold_low(f, f + 10)
    for k in range(3):
        kit.vanish(f"paire{k + 1}", f + 3, d=6)
    for k, pid in enumerate(["past_sur", "past_bloque", "past_reel", "past_estime"]):
        g = f + 6 + 2 * k
        kit.vanish(pid, g, into=S.to_world(past_src_id(PASTILLES[pid][3]), [0, 0], g))
    for pid, to in PAST_GARDE.items():
        kit.move(pid, f + 8, list(to))
    g = kit.draw("fil_net", f, 6, track="from")
    S.key("fil_net", "draw", g, 0)
    S.key("fil_net", "from", g, 0)
    kit.draw("cadre", f + 2, 6, to=0)
    toi.lean_to(f + 24, 0, d=10)
    toi.hold_low(f + 24, f + 34)

    f = kit.at("S18", "comme", "les axes d'un graphique se tracent en bas ; légendes « Patrimoine net », "
               "« aujourd’hui », « 1 an », « 2 ans », « 3 ans »")
    end = kit.draw("axes", f, 9)
    kit.pop("axe_y_pointe", end - 1, d=6)
    kit.pop("axe_x_pointe", end - 1, d=6)
    for tid in ["axe_y_mot", "axe_auj", "grad1", "grad2", "grad3", "grad1_mot", "grad2_mot", "grad3_mot"]:
        kit.fade(tid, f + 4, 1)

    f = kit.at("S18", "repère,", "un point cyan tombe de « Patrimoine net » sur le graphique, au-dessus "
               "de « aujourd’hui » : le repère")
    S.key("point1", "pos", f - 1, list(POINT1_FROM))
    g = kit.pop("point1", f, d=6)
    kit.move("point1", g, list(POINTS[0]), arc=60)

    for mot, pid in (("liquidité", "past_disponible"), ("risques.", "past_risque")):
        f = kit.at("S18", mot, f"le regard de « Toi » (tirets deep) va jusqu'à l'œil de « {PASTILLES[pid][0]} », qui "
                   f"bat : il la garde à l'œil")
        tip = S.to_world(f"oeil_{pid}", [round(OEIL_R * 0.7), round(OEIL_R * 0.7)] if pid == "past_disponible"
                         else [0, OEIL_R], f - 1)      # « disponible » : par la droite, loin de l'œil de « risqué »
        S.key("regard_garde", "pa", f - 1, list(REGARD_GARDE_EYE))
        S.key("regard_garde", "pb", f - 1, [round(tip[0], 1), round(tip[1], 1)])
        S.key("regard_garde", "draw", f - 1, 0)
        S.key("regard_garde", "from", f - 1, 0)
        kit.draw("regard_garde", f, 8)
        kit.pulse(pid, f + 6, step=3, peak=1.08)
        kit.pulse(f"oeil_{pid}", f + 6, step=3, peak=1.3)
        t = kit.draw("regard_garde", f + 22, 6, track="from")
        S.key("regard_garde", "draw", t, 0)
        S.key("regard_garde", "from", t, 0)
    hover = _toward_shoulder(AXE_TAP, 14)
    toi.reach(f + 14, hover, d=10)              # le stylo se lève au-dessus de l'axe pendant la tenue de fin de S18

    # ================= S19 : calcule-le une ou deux fois par an =================
    f = kit.at("S19", "calcule-le", "« Toi » touche l'axe du temps au stylo ; anneau d'impact")
    hit = toi.tap(f, list(AXE_TAP), d=4)
    ring(S, "axe_onde", hit)

    f = kit.at("S19", "une", "la pilule « 1 ou 2 fois / an » (calendrier) apparaît au-dessus du graphique")
    S.key("graphe_freq", "pos", f - 1, list(FREQ_C))
    kit.pop("graphe_freq", f)

    f = kit.at("S19", "fois", "sept points cyan naissent de la pointe du stylo l'un après l'autre et volent à leur "
               "place, tantôt plus haut, tantôt plus bas ; puis « Toi » baisse le stylo")
    tip = toi.tip(f - 1)
    for k in range(2, 9):
        kit.pop(f"point{k}", f + 3 * (k - 2), from_pt=list(tip), to=list(POINTS[k - 1]), d=POP)
    toi.lower(f + 3 * 6 + POP, d=10)

    f = kit.at("S19", "évolution", "la courbe deep se trace par les huit points (deux creux)")
    kit.draw("courbe", f, 18, e="linear")

    f = kit.at("S19", "compte.", "le premier et le dernier point battent ensemble ; l'écart entre eux se mesure "
               "(trait horizontal, double flèche)")
    kit.pulse("point1", f, step=3, peak=1.4)
    kit.pulse("point8", f, step=3, peak=1.4)
    g = kit.draw("ecart_h", f, 5)
    kit.pop("ecart_bas", g, d=5)
    g = kit.draw("ecart_v", g, 6)
    kit.pop("ecart_haut", g - 1, d=5)

    # ================= S20 : retiens ça : ton patrimoine n'est pas ton solde =================
    f = kit.at("S20", "Retiens", "le graphique, les deux pastilles et le signe d'attention rentrent dans « Patrimoine "
               "net », qui redescend sous la grille ; la carte grise ressort du disque 2 ; « − » et « = » reviennent : "
               "l'équation")
    for gid in GRAPHE:
        kit.vanish(gid, f, into="net")
    for k, pid in enumerate(["past_disponible", "past_risque", "alerte"]):
        kit.vanish(pid, f + 2 + k, into="net")
    for gid in ECART:
        kit.vanish(gid, f + 4, into="net")
    kit.draw("net_fente", f + 2, 6, to=0)
    kit.move("nom_toi", f, list(NOM_ABOVE))
    kit.move("net", f + 10, list(NET_CHUTE), scale=1)
    g = f + 14
    S.key("dettes", "pos", g - 1, list(DISQUE2))
    S.key("dettes", "w", g - 1, DETTES_W)
    S.key("dettes", "h", g - 1, DETTES_H)
    S.key("dettes", "stroke", g - 1, INK)
    S.key("dettes_ico", "pos", g - 1, list(DETTES_ICO_CARD))
    S.key("dettes_ico", "scale", g - 1, 1)
    S.key("dettes_mot", "pos", g - 1, list(DETTES_MOT_CARD))
    S.key("dettes_mot", "text", g - 1, T_DOIS_CARTE)
    kit.ensure("dettes_mot", "chars", 1000000)
    S.key("dettes_mot", "chars", g - 1, 1000000)
    S.key("dettes_mot", "opacity", g - 1, 1)
    S.key("dettes_val", "scale", g - 1, 0)
    S.key("dettes", "opacity", g, 1)
    ring(S, "disque2_onde", g, d=10, s0=0.9, s1=1.6)
    kit.pop("dettes", g, to=list(DETTES_C), d=MOVE)
    S.key("moins", "pos", g + 3, list(MOINS_C))
    kit.pop("moins", g + 4)
    S.key("egal", "pos", g + 6, list(EGAL_CHUTE))
    kit.pop("egal", g + 7)

    f = kit.at("S20", "patrimoine,", "« Patrimoine net » bat")
    kit.pulse("net", f, step=3, peak=1.1)

    f = kit.at("S20", "n’est", "la pilule « 3 200 € » quitte sa case « Comptes », passe par la marge gauche et "
               "glisse vers « Toi » en grandissant")
    kit.ensure("solde", "z", S.ents["solde"]["z"])
    S.key("solde", "z", f, 12)
    S.path("solde", f, MOVE, "inOut", bez3(S.val("solde", "pos", f - 1), SOLDE_OUT_C1, SOLDE_OUT_C2, SOLDE_OUT),
           scale_at=lambda p, s0=S.val("solde", "scale", f - 1): s0 + (SOLDE_OUT_K - s0) * p)

    f = kit.at("S20", "pas", "« Toi » regarde la pilule : son regard en tirets encre se tend vers elle")
    S.key("regard", "pa", f - 1, list(REGARD_EYE_S20))
    S.key("regard", "pb", f - 1, list(REGARD_SOLDE_S20))
    S.key("regard", "color", f - 1, INK)
    S.key("regard", "draw", f - 1, 0)
    S.key("regard", "from", f - 1, 0)
    S.key("regard", "sag", f - 1, 0)
    kit.draw("regard", f, 8)

    f = kit.at("S20", "solde.", "le regard vire au rouge et tremble : ce regard est faux")
    S.key("regard", "color", f, RED, 3)
    for k, (dx, dy) in enumerate([(4, -3), (-3, 2), (0, 0)]):
        for tr, p in (("pa", REGARD_EYE_S20), ("pb", REGARD_SOLDE_S20)):
            S.key("regard", tr, f + 3 + k, [p[0] + dx, p[1] + dy])

    # ================= S21 : ce que tu possèdes moins ce que tu dois =================
    f = kit.at("S21", "C’est", "« Toi » barre son regard rouge au stylo ; le regard se détend et rentre")
    g = toi.strike(f, *REGARD_BARRE, line="regard_barre", track="draw")
    S.key("regard", "sag", g, 30, 6, "out")
    h = kit.draw("regard", g + 5, 9, track="from")
    kit.fade("regard_barre", h - 3, 0)
    toi.lower(g + 1, d=10)

    f = kit.at("S21", "possèdes", "la pilule « 3 200 € » rentre dans sa case par la marge gauche : une case parmi "
               "d'autres ; « Possèdes » s'écrit et se souligne sous la grille")
    S.path("solde", f, MOVE, "inOut", bez3(S.val("solde", "pos", f - 1), SOLDE_OUT_C2, SOLDE_OUT_C1, SOLDE_CELL_SMALL),
           scale_at=lambda p, s0=S.val("solde", "scale", f - 1): s0 + (SOLDE_SMALL_K - s0) * p)
    S.key("solde", "z", f + MOVE, S.ents["solde"]["z"])
    e = kit.type("leg_possedes", f + 8, rate=3)
    S.key("leg_possedes", "under", e, 1, 9)

    f = kit.at("S21", "moins", "« Dois » s'écrit et se souligne sous la carte grise ; le « − » bat")
    e = kit.type("leg_dois", f, rate=3)
    S.key("leg_dois", "under", e, 1, 9)
    kit.pulse("moins", f, step=3, peak=1.1)

    f = kit.at("S21", "dois.", "« Toi » se penche et regarde longuement « Patrimoine net » : un regard en tirets encre "
               "de sa tête au bas de la pilule, qui devient plein deep ; sa pilule « Toi » bat ; « Patrimoine net » "
               "grandit (×1,2)")
    S.key("regard_net", "pa", f - 1, list(REGARD_NET[0]))
    S.key("regard_net", "pb", f - 1, list(REGARD_NET[1]))
    g = kit.draw("regard_net", f, 8)
    S.key("regard_net", "dashed", g + 4, 0)
    S.key("regard_net", "color", g + 4, DEEP, 3)
    kit.move("net", f, list(NET_CHUTE), d=10, scale=NET_CHUTE_K, e="out")
    toi.lean_to(f, -6, d=14)
    toi.hold_low(f, f + 14)
    kit.pulse("nom_toi", f + 2, step=3)
    toi.lean_to(f + 34, 0, d=12)
    toi.hold_low(f + 34, f + 46)

    f = kit.at("S21", "Simple,", "le signe d'attention ressort de la pilule et se pose dessous ; « Limites » s'écrit "
               "à sa droite et se souligne")
    kit.pop("alerte", f, scale=ALERTE_CHUTE_K, from_pt="net", to=list(ALERTE_CHUTE))
    e = kit.type("leg_limites", f + 4, rate=3)
    S.key("leg_limites", "under", e, 1, 9)

    f = kit.at("S21", "pourtant", "une coche deep se trace dans le disque 3 du repère : les trois étapes sont faites ; "
               "tenue")
    S.key("marqueur", "done2", f, 1, DRAW)
    kit.pop("marqueur_fait3", f)

    # ================= S22 : fin standard ; la pilule du solde devient le bouton =================
    outs = ["grille", "jeton", "dettes", "net", "moins", "egal", "leg_possedes", "leg_dois", "leg_limites", "alerte",
            "marqueur", "marqueur_fait3"]
    out = kit.outro("S22", outs=outs, press="argent.", btn_at=MOVE, bsize=FIN_BSIZE)
    f = out["card"]
    toi.exit(f)
    S.key("regard_net", "opacity", f, 0, FADE, "linear")
    S.key("solde", "z", f, 41)
    kit.ensure("solde", "textOp", 1)
    S.key("solde", "textOp", f, 0, 3, "out")
    S.key("solde", "text", f + MOVE // 2, T_ABONNER)
    S.key("solde", "textOp", f + MOVE // 2, 1, FADE, "out")
    S.key("solde", "w", f, FIN_W, MOVE, "inOut")
    kit.move("solde", f, list(FIN_BUTTON), scale=round(FIN_K, 4))
    S.key("solde", "opacity", f + MOVE, 0)
    S.set(out["cursor"], opacity=0)

    g = kit.at("S22", "comprendre", "un doigt glisse jusqu'au bas du bouton « S’abonner », hors du libellé")
    S.key("fin_doigt", "pos", g - 1, list(FIN_DOIGT_FROM))
    kit.pop("fin_doigt", g, to=list(FIN_TAP_P3), d=MORPH)
    fp = out["press"]
    S.key("fin_doigt", "scale", fp, 0.8, 2, "out")
    kit.vanish("fin_doigt", fp + 5, d=5)
    for k in range(2):
        S.key(f"fin_onde{k + 1}", "pos", fp - 1, list(FIN_TAP_P3))
        ring(S, f"fin_onde{k + 1}", fp + 3 * k, d=14, s0=0.6, s1=2.1)
    assert fp + 3 + 14 < film_end(S), (fp, film_end(S))
