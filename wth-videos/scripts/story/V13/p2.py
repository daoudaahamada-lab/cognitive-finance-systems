"""V13, partie 2 : S09-S15, images 987-1915 (36 temps forts, 31,0 s). Fin du point 1 (immobilier, véhicule, parts de
société ; l'étiquette « Prix d’achat » barrée devient « Valeur actuelle », sa date passe de « 2015 » à « aujourd’hui ») ;
point 2 « Dois » : la barre de l'appartement (née du jeton, accolade qui la relie à l'étiquette) recouverte par la part
grise « Ce que tu dois » sortie du disque 2 ; capital restant dû = les 12 tranches, pas la seule mensualité ;
250 000 € / 180 000 € ; « 250 000 € » rouge barré ; part grise rendue au disque 2 ; ≈ 70 000 € nets.

ÉTAT D'ENTRÉE : ENTRY_P2 épinglé à 986 (etat_initial de S09). SORTIE : ENTRY_P3 à l'image 1915.

Tour de revue 1 (aucun temps fort déplacé ; écarts de mise en scène) :
- S09 : le jeton tombe de 30 px seulement, dans sa propre case (il ne traverse plus la case « PEA ») ;
- S10 : l'étiquette tombe sous la grille (elle ne passe plus sur les libellés) et reste à 20 px de « Toi » ; après le
  trait, le stylo revient au repos LEVÉ (baissé, il croiserait la flèche du temps) ; la date « 2015 » devient
  « aujourd’hui » et une flèche deep se trace sous l'étiquette, du passé à aujourd'hui (l'étiquette ne glisse pas :
  elle toucherait « Toi ») ;
- S11 : la barre naît du bas du jeton en passant DERRIÈRE l'étiquette ; une maison au bout cyan ; une accolade deep
  couvre toute la barre et un fil la relie au bas de l'étiquette « Valeur actuelle » ; la carte grise : onde du disque
  2, vol en arc au-dessus du repère puis à la verticale entre la grille et l'étiquette, toute petite, et ne grandit
  qu'au-dessus de la barre ; libellé coupé net (pas de fondu croisé) ;
- S12 : au toucher, un fil deep part de la banque de la part grise jusqu'au disque 2 « Dois » (passant entre la grille
  et l'étiquette) ; « crédits. » : le stylo touche la part grise, qui bat entière (sy) avec sa banque ;
- S13 : « Toi » reste en P1 (sous la barre, en P2, sa tête la toucherait) ; « Pas » : 11 traits découpent la part
  grise en 12 tranches ; « mensualités, » : le stylo touche la tranche de droite, elle seule rougit et se lève de
  10 px, « Mensualité » (calendrier) s'écrit dessous ; « mais » : barrée, la tranche retombe et redevient grise ;
  « montant » : l'accolade (SOUS la part grise, l'autre accolade est au-dessus de la barre) balaie les 12 tranches,
  dont les traits s'allument de gauche à droite ;
- S14 : valeurs posées (pas de compteur qui monte) ; « 250 000 € » se copie de l'étiquette sur l'accolade de la
  barre ; « 180 000 € » posé, la part grise bat ; « crédit » : le stylo touche la part grise (elle bat), puis la part
  cyan bat (la part de la banque, puis la tienne) ;
- S15 : la copie rouge sort de « 250 000 € » de l'accolade et passe DERRIÈRE la barre pour se poser dessous (elle ne
  heurte plus la carte grise) ; la part grise, tirée dès le mot, rapetisse aussitôt et monte à la verticale entre la
  grille et l'étiquette jusqu'au disque 2 (20 images, traînée en tirets, onde du disque à l'arrivée) ; un contour en
  tirets garde sa place : « ≈ 70 000 € nets » est une part de toute la barre.
"""
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, STRETCH, text_width  # noqa: F401

from . import (ACHAT_STRIKE, BARRE_C, BARRE_H, BARRE_SHORT_C, BARRE_SHORT_W, BARRE_W, BRUT_C, BRUT_STRIKE,
               CASE_IDS, CROCHET_VAL, DATE_H, DEEP, DETTES_ICO_S, DISQUE2, ENTRY_P2, ETIQ_P2, ETIQ_S10,
               GREY, GRISE_C, GRISE_GAP_C, GRISE_H, GRISE_ICO_S, GRISE_TAP, GRISE_W, INK, JETON_CELL, JETON_CELL_K,
               JETON_P2, JETON_P2_K, LIGHT, LOW_ROT_V13, MENS_LOCAL, MENS_STRIKE, MENS_TAP, NOM_ABOVE, NOM_RIGHT,
               NOM_RIGHT_LOW, N_TRANCHES, Q_IDS, RESULTAT_C, SHOULDER_DX, SHOULDER_DY, SLICE, T_AUJOURDHUI, T_CRD,
               T_DOIS_BARRE, TOI_P1, TOI_P3, bez, drop_in, move_with_grid, poly_path, ring, scene_f0)

WALK_D = MOVE                                    # « Figure.walk 550 ms » du storyboard
MOT_SIZE = 34
ICO_X = -165                                     # banque dans la part grise (repère de la carte)
MOT_X = 15                                       # centre des textes de la part grise (repère de la carte)
W_DOIS = text_width(T_DOIS_BARRE, MOT_SIZE, 700)
W_CRD = text_width(T_CRD, MOT_SIZE, 700)
W_DATE_AUJ = round(text_width(T_AUJOURDHUI, 32, 700) + 48 + 30)
TAP15 = (690, 1062)                              # S15 « mais » : contact sur la part grise (depuis P1)
PULL15 = (718, 1058)                             # S15 « environ » : la pointe tire la part vers la droite
LOW_ROT_LEFT = 180 - LOW_ROT_V13                 # stylo baissé, côté gauche
POINT_TAG = (507, 1186)                          # S10 : la pointe désigne le coin bas droit de l'étiquette (à 20 px)
CARD_FLY = 20                                    # S11 / S15 : vol de la carte grise depuis / vers le disque 2
CARD_SMALL = 0.18                                # taille de la carte en vol (73 x 20 px) : elle passe entre la
#                                                  grille (x ≤ 527) et l'étiquette (x ≥ 605)


def _toward_shoulder(pt, dist):
    """Point à `dist` px de `pt`, vers l'épaule de « Toi » en P1 (départ d'un geste)."""
    sx, sy = TOI_P1[0] - SHOULDER_DX, TOI_P1[1] + SHOULDER_DY
    dx, dy = sx - pt[0], sy - pt[1]
    n = (dx * dx + dy * dy) ** 0.5
    return [round(pt[0] + dx * dist / n, 1), round(pt[1] + dy * dist / n, 1)]


def part(S, kit, c):
    toi = c.toi
    f0 = scene_f0(S, "S09")                      # 987
    kit.pin(f0 - 1, ENTRY_P2)
    if S.val("toi", "scale", f0 - 1) == 0:       # partie isolée : la figurine n'est pas entrée (sans effet ici)
        toi.enter(f0 - 10, at=list(TOI_P1))
    if abs(S.val(toi.pen, "rot", f0 - 1) - LOW_ROT_LEFT) > 2:   # partie isolée : stylo encore levé
        toi.lower(f0 - 12, d=8)
    if "chars" not in S.ents["dettes_mot"]["t"]:
        S.set("dettes_mot", chars=1000000)       # texte entier (défaut du rendu) ; S12 le réécrit par kit.type
    for k in range(1, N_TRANCHES):
        S.set(f"tranche{k}", stroke=SLICE)       # hex : les traits s'allument en deep (S13 « montant »)
    S.set("mensualite", fill=S.ents["mensualite"]["p"]["fill"])

    # ================= S09 : l'immobilier, un véhicule, des parts de société =================
    f = kit.at("S09", "l’immobilier,", "la case « ? » en bas à gauche devient la case papier « Immobilier » ; le "
               "jeton-maison de verre s'y pose d'une courte chute ; « Immobilier » s'écrit")
    kit.morph(Q_IDS[6], CASE_IDS[6], f)
    kit.type("case_immo_mot", f + 4, rate=3)
    S.key("jeton", "scale", f + MORPH - 1, JETON_CELL_K)
    drop_in(kit, "jeton", f + MORPH, to=list(JETON_CELL), h=30)   # dans sa case : ne traverse pas « PEA »

    f = kit.at("S09", "véhicule,", "la case « ? » du milieu devient « Véhicule », avec le pictogramme voiture")
    kit.morph(Q_IDS[7], CASE_IDS[7], f)
    kit.type("case_vehicule_mot", f + 3, rate=3)

    f = kit.at("S09", "parts", "la dernière case « ? » devient « Parts de société » (immeuble + petit disque %) : "
               "plus aucun « ? »")
    kit.morph(Q_IDS[8], CASE_IDS[8], f)
    kit.type("case_societe_mot", f + 3, rate=3)

    f = kit.at("S09", "société.", "« Toi » marche sous la grille, vers la case « Immobilier » ; sa pilule passe à "
               "droite de sa tête")
    toi.walk(f, TOI_P3[0], d=WALK_D, low=True)
    kit.move("nom_toi", f, list(NOM_RIGHT_LOW), d=WALK_D)

    # ================= S10 : valeur actuelle, pas prix d'achat =================
    f = kit.at("S10", "note", "une étiquette de prix tombe sous la grille, pendue à la case « Immobilier » : « Prix "
               "d’achat » en rouge et une date, « 2015 » (calendrier)")
    drop_in(kit, "etiquette", f, to=list(ETIQ_S10), h=40)
    toi.reach(f - 2, list(POINT_TAG), d=8)                  # le stylo désigne l'étiquette (baissé, il la croiserait ;
    #                                                         levé au repos, il entrerait dans la case « Véhicule »)
    kit.draw("ficelle", f + DROP - 4, 6)

    f = kit.at("S10", "valeur", "« Toi » barre « Prix d’achat » au stylo, de droite à gauche")
    toi.reach(f - 7, ACHAT_STRIKE[0], d=6)
    end = toi.strike(f, *ACHAT_STRIKE, line="etiq_achat_barre", track="draw")
    toi.reach(end, list(POINT_TAG), d=8)                      # le stylo revient désigner le coin de l'étiquette

    f = kit.at("S10", "actuelle,", "« Prix d’achat » barré tombe ; « Valeur actuelle » s'écrit ; la date passe de "
               "« 2015 » à « aujourd’hui » pendant qu'une flèche deep se trace sous l'étiquette, du passé à aujourd'hui")
    kit.drop("etiq_achat", f, out=True, h=110, rot=-8)
    kit.type("etiq_valeur", f + 2, rate=3)
    S.key("etiq_date", "textOp", f, 0, 3, "linear")
    S.key("etiq_date", "text", f + 3, T_AUJOURDHUI)
    S.key("etiq_date", "w", f + 3, W_DATE_AUJ, 6, "out")
    S.key("etiq_date", "fill", f + 3, LIGHT, 6, "out")
    S.key("etiq_date", "textOp", f + 5, 1, 4, "out")
    g = kit.draw("temps", f, 12, e="inOut")
    kit.pop("temps_pointe", g - 2, d=5)

    f = kit.at("S10", "pas", "l'étiquette « Valeur actuelle · aujourd’hui » bat ; le jeton-maison bat avec elle")
    kit.pulse("etiquette", f, step=3, peak=1.06)
    kit.pulse("jeton", f + 2, step=3, peak=round(JETON_CELL_K * 1.08, 4))

    # ================= S11 : posséder n'est pas tout avoir =================
    f = kit.at("S11", "Ça", "la grille se réduit en haut à gauche ; le jeton sort de sa case (cercle en tirets à sa "
               "place) et grandit à droite, l'étiquette pendue dessous ; « Toi » revient à droite")
    move_with_grid(kit, f, small=True)
    kit.pop("case_immo_place", f)
    kit.move("jeton", f, list(JETON_P2), arc=80, scale=JETON_P2_K)
    kit.vanish("etiq_date", f, d=6)
    kit.move("etiquette", f, list(ETIQ_P2))
    S.key("ficelle", "draw", f, 0, 4, "in")
    kit.draw("ficelle_jeton", f + MOVE, DRAW)
    g = kit.draw("temps", f, 6, track="from")
    S.key("temps", "draw", g, 0)
    S.key("temps", "from", g, 0)
    kit.vanish("temps_pointe", f, d=6)
    toi.walk(f, TOI_P1[0], d=WALK_D, low=True)
    kit.move("nom_toi", f, list(NOM_ABOVE), d=WALK_D)

    f = kit.at("S11", "posséder", "une barre cyan sort du bas du jeton (derrière l'étiquette) et s'étire en bas : une "
               "maison à son bout ; une accolade deep la couvre en entier, reliée par un fil à l'étiquette « Valeur "
               "actuelle » : la barre = la valeur de l'appartement")
    S.key("barre", "w", f - 1, BARRE_H)
    end = kit.pop("barre", f, from_pt=S.to_world("jeton", list(c.jeton_bottom), f - 1), to=list(BARRE_C))
    S.key("barre", "w", end, BARRE_W, STRETCH, "out")
    kit.pop("barre_maison", end + 2, d=6)
    g = kit.draw("crochet", end, DRAW)
    kit.draw("crochet_fil", g - 3, 6)

    f = kit.at("S11", "bien", "le jeton-maison bat")
    kit.pulse("jeton", f, step=3, peak=round(JETON_P2_K * 1.08, 4))

    f = kit.at("S11", "toi", "« Toi » se penche vers la barre : il croit que tout est à lui")
    toi.lean_to(f, -6, d=14)
    toi.hold_low(f, f + 14)

    f = kit.at("S11", "entier.", "le disque 2 « Dois » émet une onde ; la carte grise en sort, monte en arc au-dessus "
               "du repère, descend entre la grille et l'étiquette et s'élargit sur les trois quarts droits de la "
               "barre : « Ce que tu dois » ; « Toi » se redresse")
    ring(S, "disque2_onde", f, d=10, s0=0.9, s1=1.6)
    g = f + 2
    S.key("dettes", "pos", g - 1, list(DISQUE2))
    S.key("dettes", "w", g - 1, GRISE_W)
    S.key("dettes", "h", g - 1, GRISE_H)
    S.key("dettes", "stroke", g - 1, INK)
    S.key("dettes_ico", "pos", g - 1, [ICO_X, 0])
    S.key("dettes_ico", "scale", g - 1, round(GRISE_ICO_S / DETTES_ICO_S, 4))
    S.key("dettes_mot", "pos", g - 1, [round(MOT_X - W_DOIS / 2, 1), 0])
    S.key("dettes_mot", "text", g - 1, T_DOIS_BARRE)            # coupé net, invisible (échelle 0)
    S.key("dettes_mot", "opacity", g - 1, 1)
    S.key("dettes", "opacity", g, 1)
    route = poly_path([list(DISQUE2), [550, 236], [566, 330], [566, 900], list(GRISE_C)])

    def grow(p, a=0.78):
        return CARD_SMALL if p < a else CARD_SMALL + (1 - CARD_SMALL) * ((p - a) / (1 - a)) ** 0.8

    S.path("dettes", g, CARD_FLY, "inOut", route, scale_at=grow)
    toi.lean_to(f + 6, 0, d=9)
    toi.hold_low(f + 6, f + 15)

    # ================= S12 : retirer le capital restant dû =================
    f = kit.at("S12", "Ensuite,", "le repère passe à l'étape 2 « Dois » ; coche deep dans le disque 1")
    kit.step(f, 1)
    S.key("marqueur", "done0", f, 1, DRAW)

    f = kit.at("S12", "retire", "« Toi » touche la part grise au stylo : elle tremble et se détache de la part cyan "
               "par un liseré ivoire ; un fil deep part de sa banque jusqu'au disque 2 « Dois »")
    hit = toi.tap(f - 5, list(GRISE_TAP), d=8)
    kit.shake("dettes", hit, amp=6)
    S.key("barre", "w", hit + 2, BARRE_SHORT_W)                # sous la carte : la barre ne garde que sa part cyan
    S.key("barre", "pos", hit + 2, list(BARRE_SHORT_C))
    kit.move("dettes", hit + 3, list(GRISE_GAP_C), d=9, e="out")
    kit.draw("fil_banque", hit + 4, 10)
    toi.lower(hit + 6, d=10)

    f = kit.at("S12", "capital", "« Ce que tu dois » s'efface ; « Capital restant dû » s'écrit dans la part grise")
    kit.fade("dettes_mot", f, 0, d=3)
    S.key("dettes_mot", "text", f + 3, T_CRD)
    S.key("dettes_mot", "pos", f + 3, [round(MOT_X - W_CRD / 2, 1), -18])
    S.key("dettes_mot", "chars", f + 2, 0)
    S.key("dettes_mot", "opacity", f + 3, 1)
    kit.type("dettes_mot", f + 3, n=len(T_CRD), rate=3)

    f = kit.at("S12", "crédits.", "le stylo touche la part grise : elle bat tout entière, deux fois, avec sa banque ; "
               "le fil vers le disque 2 se retire ensuite")
    hit = toi.tap(f - 6, list(GRISE_TAP), d=7)
    ico_k = S.val("dettes_ico", "scale", f - 1)
    kit.pulse("dettes", hit, times=2, step=3, peak=1.08, track="sy")
    kit.pulse("dettes_ico", hit, times=2, step=3, peak=round(ico_k * 1.25, 4))
    toi.lower(hit + 5, d=8)
    g = kit.draw("fil_banque", hit + 14, 6, track="from")
    S.key("fil_banque", "draw", g, 0)
    S.key("fil_banque", "from", g, 0)

    # ================= S13 : pas la mensualité, tout ce qui reste à rembourser =================
    f = kit.at("S13", "Pas", "11 traits découpent la part grise en 12 tranches, de gauche à droite ; « Toi » lève le "
               "stylo vers la tranche de droite")
    for k in range(1, N_TRANCHES):
        kit.draw(f"tranche{k}", f + (k - 1) // 2, 4)
    toi.reach(f, _toward_shoulder(MENS_TAP, 34), d=5)

    f = kit.at("S13", "mensualités,", "le stylo touche la tranche de droite : elle seule rougit et se lève de 10 px ; "
               "« Mensualité » (petit calendrier) s'écrit en rouge dessous")
    hit = toi.tap(f - 4, list(MENS_TAP), d=5)
    S.key("mensualite", "pos", hit - 1, list(MENS_LOCAL))
    kit.pop("mensualite", hit, d=4)
    kit.move("mensualite", hit + 2, [MENS_LOCAL[0], -10], d=5, e="out")
    kit.pop("mensualite_cal", hit + 2, d=6)
    kit.type("mensualite_mot", hit + 3, rate=3)

    f = kit.at("S13", "mais", "« Toi » barre « Mensualité » ; la tranche rouge retombe dans la part grise et "
               "redevient grise")
    toi.reach(f - 7, MENS_STRIKE[0], d=6)
    end = toi.strike(f, *MENS_STRIKE, line="mensualite_barre", track="draw")
    kit.move("mensualite", end, list(MENS_LOCAL), d=5, e="in")
    S.key("mensualite", "fill", end + 2, GREY, 5)
    toi.lower(end, d=10)

    f = kit.at("S13", "montant", "« Mensualité » barrée s'efface ; une accolade deep balaie SOUS la part grise ses 12 "
               "tranches, dont les traits s'allument un à un de gauche à droite : tout le reste à rembourser")
    kit.fade("mensualite_mot", f, 0)
    kit.fade("mensualite_cal", f, 0)
    kit.draw("accolade", f + 2, 10, e="inOut")
    for k in range(1, N_TRANCHES):
        g = f + 2 + k
        S.key(f"tranche{k}", "stroke", g, DEEP, 2, "out")
        S.key(f"tranche{k}", "stroke", g + 5, SLICE, 4, "inOut")

    f = kit.at("S13", "restant", "« restant à rembourser » s'écrit sous l'accolade")
    kit.type("restant", f, rate=3)

    f = kit.at("S13", "rembourser.", "le contour de la part grise passe au deep et bat : c'est tout cela qu'on retire")
    S.key("dettes", "stroke", f, DEEP, 6)
    kit.pulse("dettes", f, step=3, peak=1.04)

    # ================= S14 : 250 000 € estimés, 180 000 € de crédit =================
    f = kit.at("S14", "Imagine", "l'accolade du dessous et son libellé se réduisent")
    kit.vanish("accolade", f)
    kit.vanish("restant", f)
    S.key("mensualite", "scale", f, 0)                         # grise, sur sa tranche : invisible

    f = kit.at("S14", "appartement", "le jeton-maison bat")
    kit.pulse("jeton", f, step=3, peak=round(JETON_P2_K * 1.1, 4))

    f = kit.at("S14", "estimé", "l'étiquette « Valeur actuelle » bat")
    kit.pulse("etiquette", f, step=3, peak=1.06)

    f = kit.at("S14", "250 000 €,", "« 250 000 € » se pose sur l'étiquette ; une copie deep vole sur l'accolade de la "
               "barre : toute la barre vaut 250 000 €")
    kit.pop("etiq_montant", f, d=POP)
    g = kit.pop("crochet_val", f + 6, from_pt=S.to_world("etiq_montant", [0, 0], f + 6), to=list(CROCHET_VAL), d=14,
                e="inOut")
    kit.pulse("crochet", g, step=3, peak=1.04)

    f = kit.at("S14", "180 000 €", "« 180 000 € » se pose dans la part grise, sous « Capital restant dû » ; la part "
               "grise bat")
    kit.pop("dettes_val", f, d=POP)
    kit.pulse("dettes", f + POP, step=3, peak=1.07, track="sy")

    f = kit.at("S14", "crédit", "le stylo touche la part grise : elle bat avec sa banque (la part de la banque) ; puis "
               "la part cyan bat (la tienne)")
    hit = toi.tap(f - 6, list(GRISE_TAP), d=7)
    kit.pulse("dettes", hit, step=3, peak=1.08, track="sy")
    kit.pulse("dettes_ico", hit, step=3, peak=round(ico_k * 1.25, 4))
    toi.lower(hit + 5, d=8)
    kit.pulse("barre", hit + 18, step=3, peak=1.1, track="sy")
    kit.pulse("barre_maison", hit + 18, step=3, peak=1.15)

    # ================= S15 : pas 250 000 € de patrimoine, ≈ 70 000 € nets =================
    f = kit.at("S15", "représente", "une copie rouge « 250 000 € » sort du « 250 000 € » de l'accolade, passe derrière "
               "la barre et se pose dessous")
    a = list(CROCHET_VAL)
    S.key("brut", "pos", f - 1, a)
    S.key("brut", "scale", f - 1, 0)
    S.key("brut", "opacity", f - 1, 1)
    S.path("brut", f, MOVE, "inOut", bez(a, [600, 1060], list(BRUT_C)), scale_at=lambda p: 0.5 + 0.5 * min(1, 1.4 * p))
    toi.rest(f, d=8)                                          # stylo levé : baissé, il croiserait la pilule rouge

    f = kit.at("S15", "250 000 €", "la pilule rouge « 250 000 € » tremble ; la part grise au-dessus bat")
    kit.shake("brut", f, amp=6)
    kit.pulse("dettes", f, step=3, peak=1.07, track="sy")

    f = kit.at("S15", "patrimoine,", "« Toi » lève le stylo et barre « 250 000 € »")
    toi.reach(f - 7, BRUT_STRIKE[0], d=7)
    toi.strike(f, *BRUT_STRIKE, line="brut_barre", track="draw")

    f = kit.at("S15", "mais", "« 250 000 € » barré tombe et s'efface ; le stylo touche la part grise")
    kit.drop("brut", f, out=True, h=80, rot=10)
    toi.tap(f - 7, list(TAP15), d=12)                          # contact à f + 4

    f = kit.at("S15", "environ", "la pointe tire la part grise vers la droite ; elle rapetisse aussitôt et remonte en "
               "laissant une traînée jusqu'au disque 2 « Dois », qui émet une onde ; un contour en tirets garde sa "
               "place : la courte barre cyan n'est qu'une part de la barre entière")
    d_pull = 5
    p0 = S.val("dettes", "pos", f - 1)
    p1 = [round(p0[0] + PULL15[0] - TAP15[0], 1), round(p0[1] + PULL15[1] - TAP15[1], 1)]
    toi.reach(f, list(PULL15), d=d_pull, e="out")
    kit.move("dettes", f, p1, d=d_pull, e="out")
    S.key("dettes", "scale", f, 0.55, d_pull, "out")
    g = f + d_pull
    route = poly_path([p1, [566, 930], [566, 420], [DISQUE2[0], DISQUE2[1] + 6]])
    S.path("dettes", g, CARD_FLY, "inOut", route,
           scale_at=lambda p: 0.55 - (0.55 - CARD_SMALL) * min(1, p / 0.2) if p < 0.9 else CARD_SMALL * (1 - p) / 0.1)
    S.key("dettes", "opacity", g + CARD_FLY, 0)
    S.key("dettes", "scale", g + CARD_FLY, 0)
    S.key("dettes", "stroke", g + CARD_FLY + 1, INK)         # carte rangée : contour encre (raccord de p3)
    for k in range(1, N_TRANCHES):
        S.key(f"tranche{k}", "draw", g + CARD_FLY + 1, 0)   # la carte redevient la carte « Ce que tu dois » (S20)
    t = kit.draw("trace_dettes", g, CARD_FLY, e="inOut")
    t = kit.draw("trace_dettes", t, 8, track="from")
    S.key("trace_dettes", "draw", t, 0)
    S.key("trace_dettes", "from", t, 0)
    ring(S, "disque2_onde", g + CARD_FLY - 1, d=10, s0=0.9, s1=1.6)
    kit.draw("fantome", f + 3, 8)
    toi.lower(g + 1)

    f = kit.at("S15", "70 000 €", "la pilule « ≈ 70 000 € nets » sort de la courte barre cyan et se pose dessous")
    kit.pop("resultat", f, from_pt=list(BARRE_SHORT_C), to=list(RESULTAT_C))

    f = kit.at("S15", "nets.", "« 250 000 € − 180 000 € = 70 000 € » s'écrit sous le résultat")
    end = kit.type("calc_a", f, rate=2.5)
    end = kit.type("calc_b", end, rate=2.5)
    assert end <= 1916, f"S15 : le calcul finit à {end}, après le début de p3"
