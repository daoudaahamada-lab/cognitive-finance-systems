"""V06, partie 2 : S07-S14, images 746-1766 (point 1 et point 2 jusqu'aux actions). 33 temps forts, 34,0 s.

ÉTAT D'ENTRÉE (etat_initial de S07, kit.pin(745, ENTRY_P2)) : rail (280-580, y 880) fléché vers la caisse, horloge à
fine tranche (480, 750), « liquidité » sous le rail, livret nommé « Livret » (372, 880), cadenas (520, 880),
appartement (700, 880) et pilule « 200 000 € » (700, 705), caisse vide (170, 880), facture partie, « Toi » (`toi`,
bras droit, bras baissé) en P1.

Temps forts (image du mot) :
S07  valeur@786  chiffre@854  rassure,@871  à@892  tort.@897
S08  appartement@933  estimé@955  200 000 € ?@971
S09  récupérer@1017  argent,@1038  vendre.@1068
S10  prend@1094  mois,@1112  frais,@1137  prix@1165  garanti.@1199
S11  l’immobilier@1230  isolé :@1272  délai.@1341
S12  Comptes@1361  livrets :@1394  quelques@1440  jours,@1449  perte.@1478
S13  Pour@1502  assurance-vie,@1514  verser@1569  deux@1610  maximum.@1626
S14  Actions@1660  vendent@1693  prix@1733  varie.@1743

Tour 1 de revue :
- S07 : l'horloge rentre dans l'appartement sur « valeur » (rien entre la feuille et la caisse) ; la petite pilule de
  la bulle essaie d'entrer dans une place de la caisse et rebondit (« à » : les places tremblent au choc) ; sur
  « tort. » le « ≠ » (120 px) surgit SUR la droite pilule -> places, relié aux deux par des tirets, et les deux
  termes battent ; la bulle et ses ronds s'effacent ensemble (aucun éclat isolé).
- S08 : la pilule hésite franchement (±12°, 3 oscillations) ; deux pilules fantômes en tirets sortent de derrière
  elle (la fourchette : « pas certain ») ; le « ? » fait 96 px et bat.
- S10 : l'horloge ressort de l'appartement pour se remplir ; les pièces de la vente passent DERRIÈRE le livret ; les
  deux pièces arrivées restent dans la caisse jusqu'à S12 « Comptes ».
- S11-S14 : la scène et l'échelle (voir __init__.py) ; la frise s'allonge en 700 ms, la flèche bat ; sur
  « placement », le livret puis l'appartement battent ; sur « délai. », l'horloge ressort de l'appartement et va
  marquer le bout lointain de la frise ; l'appartement (devenu disque) monte se ranger avec « plusieurs mois ».
- S12-S14 : un seul placement actif sur la scène, nommé juste au-dessus, délai juste dessous ; le précédent monte dans
  l'échelle. S14 « varie. » : les trois pièces finissent à x1,5 / x0,6 / x1, et le restent ; la place en tirets de la
  pièce rétrécie (x1, la taille d'avant) passe en cyan.

PASSAGE À p3 (image 1766) : exactement ENTRY_P3 (__init__.py).
"""
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401

from . import *  # noqa: F401,F403
from . import (AXE_Y, BULLE_S07, BULLE_S07_W, CAISSE_PLACES, COINS, COMPTE_C, COURBE_C, CYAN, DELAI_MOIS_S11,
               DELAIS, DIFFERENT_C, DISC_ID, DOUTE_C, DROP_FROM_Y, ENTRY_P2, FEUILLE_RANGEE, FEUILLE_RANGEE_K,
               FOURCHETTE, FRAIS_PIECE_S10, FRAIS_S10, FRISE_A, HEAD_DY, HORLOGE_C, HORLOGE_FIN, HORLOGE_FIN_K, INK,
               LAD_K, LAD_NOMS, LIGHT, MAISON_BUMP_C, MAISON_C, MAISON_S11_K, MAISON_TAP_S09, NOMS, P1, PAPER,
               PASTILLE_FEUILLE, PASTILLE_FEUILLE_K, PASTILLE_RANGEE, PASTILLE_RANGEE_K, PASTILLE_W, PLACES, RAIL_A,
               STAGE_C, assert_reach, bulle_ronds, hold_low, lad_pill_pt, lad_pt, lean_low, lower, scene_f0)

COINS_S12_FAN = [(310, 700), (372, 686), (434, 700)]   # au-dessus de « Comptes, livrets » (752-832)
S12_TO = [0, 2, 1]                              # pièce k -> place S12_TO[k] (trajets sans croisement)
FILE_S10 = [(560, AXE_Y), (444, AXE_Y), (502, AXE_Y)]  # piece_s10_1 en QUEUE de file (celle que « frais » prend)
FILE_S13 = [(385, AXE_Y), (445, AXE_Y), (505, AXE_Y)]  # file des pièces de l'assurance-vie (la 1re devant)
VA_LOCAL = (-20, -81)                           # S07 : la petite pilule de la bulle bute sous la place 3 (170, 950)


def _r(pt):
    return [round(pt[0], 2), round(pt[1], 2)]


def file_away(S, kit, pid, f, d=14):
    """Le placement actif monte se ranger dans l'échelle : son disque (r 30), sa pilule de délai (fond papier) ; son
    nom de scène rentre dans le disque et son nom d'échelle surgit à l'arrivée. -> arrivée."""
    disc, did = DISC_ID[pid], {"livret": "delai_jours", "assurance_vie": "delai_2mois", "actions": "delai_vite",
                               "per": "delai_retraite", "epargne_salariale": "delai_5ans", "maison": "delai_mois"}[pid]
    if pid in NOMS:
        kit.vanish(NOMS[pid][0], f, into=disc, d=6)
    g = kit.move(disc, f, list(lad_pt(pid)), d=d, scale=LAD_K, arc=30)
    kit.move(did, f + 2, list(lad_pill_pt(did)), d=d, arc=30)
    S.key(did, "fill", f + 2 + d - 4, PAPER, 4)
    kit.pop(LAD_NOMS[pid], g - 3, d=6)
    return g


def part(S, kit, c):
    toi = c.toi
    f0 = scene_f0(S, "S07")
    kit.pin(f0 - 1, ENTRY_P2)
    if S.val("toi", "scale", f0 - 1) == 0:      # partie construite seule : la figurine n'est pas entrée
        toi.enter(f0 - 10, at=list(P1))
    places_w = [list(p) for p in CAISSE_PLACES]

    # ================= S07 : la valeur sur le papier, ≠ caisse vide =================
    f = kit.at("S07", "valeur", "« liquidité » et « Livret » s'effacent, l'horloge rentre dans l'appartement ; la "
                                "feuille « Estimation » surgit au-dessus de l'appartement et la pilule « 200 000 € » "
                                "monte s'y poser")
    for t in ("liquidite", "nom_livret"):
        kit.fade(t, f, to=0)
    S.key("nom_livret", "scale", f + FADE, 0)
    kit.vanish("horloge", f, into="maison")
    kit.pop("feuille", f)
    kit.move("pastille", f, PASTILLE_FEUILLE, scale=PASTILLE_FEUILLE_K)

    f = kit.at("S07", "chiffre", "la pilule « 200 000 € » bat deux fois sur la feuille")
    kit.pulse("pastille", f, times=2)

    f = kit.at("S07", "rassure,", "« Toi » s'incline en arrière, détendu ; trois petits ronds puis une bulle en "
                                  "tirets sortent de sa tête, avec dedans une petite pilule « 200 000 € »")
    lean_end = lean_low(toi, f, -8, d=14)
    head = toi._body_pt([0, HEAD_DY], lean_end)
    ronds = bulle_ronds(head, (BULLE_S07[0] + BULLE_S07_W / 2 - 6, BULLE_S07[1] - 14))
    g = f + 2
    for k, pt in enumerate(ronds):
        rid = f"bulle_rond{k + 1}"
        S.key(rid, "pos", g + 2 * k - 1, _r(pt))
        kit.pop(rid, g + 2 * k)
    gb = g + 6
    S.key("bulle", "pos", gb - 1, list(BULLE_S07))
    S.key("bulle", "w", gb - 1, BULLE_S07_W)
    S.key("bulle", "h", gb - 1, 100)
    S.key("bulle_pilule", "scale", gb - 1, 1)
    S.key("bulle_q", "scale", gb - 1, 0)
    kit.pop("bulle", gb)

    f = kit.at("S07", "à", "la petite pilule de la bulle monte vers une place de la caisse, bute dessous et "
                           "rebondit ; au choc, les trois places vides tremblent, toujours vides")
    kit.move("bulle_pilule", f - 6, list(VA_LOCAL), d=6, e="in")
    kit.move("bulle_pilule", f, [0, 0], d=5, e="out")
    for k, pid in enumerate(PLACES):
        kit.shake(pid, f + k, amp=6)
    kit.shake("caisse", f, amp=4, axis="y")

    f = kit.at("S07", "tort.", "un grand « ≠ » surgit entre la pilule de la feuille et les places vides, relié aux "
                               "deux par des tirets ; la pilule et les places battent ; la bulle s'efface ; « Toi » "
                               "se redresse")
    kit.pop("different", f)
    kit.draw("lien_pilule", f + 2, 6)
    kit.draw("lien_caisse", f + 2, 6)
    kit.pulse("pastille", f, peak=1.15 * PASTILLE_FEUILLE_K)
    for pid in PLACES:
        kit.pulse(pid, f, peak=1.15)
    for i in ("bulle", "bulle_rond1", "bulle_rond2", "bulle_rond3"):
        kit.vanish(i, f, d=6)
    lean_low(toi, f + 2, 0, d=POP)

    # ================= S08 : estimé… 200 000 € ? =================
    f = kit.at("S08", "appartement", "l'appartement bat")
    kit.pulse("maison", f, peak=1.1)

    f = kit.at("S08", "estimé", "la pilule hésite franchement sur la feuille (±12°, trois fois) ; deux pilules "
                                "fantômes en tirets sortent de derrière elle, l'une à gauche, l'autre à droite : "
                                "une fourchette, pas un chiffre sûr ; le chiffre ne change pas")
    t = f
    for ang, d in ((-12, 3), (12, 5), (-12, 5), (10, 5), (0, 5)):
        S.key("pastille", "rot", t, ang, d, "inOut" if t > f else "out")
        t += d
    for k, (dx, dy) in enumerate(FOURCHETTE):
        kit.pop(f"fourchette{k + 1}", f + 2 + 2 * k, from_pt=list(PASTILLE_FEUILLE),
                to=[PASTILLE_FEUILLE[0] + dx, PASTILLE_FEUILLE[1] + dy])

    f = kit.at("S08", "200 000 € ?", "un grand « ? » sort du bord droit de la pilule, se pose à sa droite et bat")
    k = S.val("pastille", "scale", f - 1)
    edge = [PASTILLE_FEUILLE[0] + k * PASTILLE_W / 2, PASTILLE_FEUILLE[1]]
    g = kit.pop("doute", f, from_pt=edge, to=list(DOUTE_C))
    kit.pulse("doute", g, peak=1.25)

    # ================= S09 : il faut le vendre =================
    f = kit.at("S09", "récupérer", "l'appartement s'élance vers la caisse, bute contre le cadenas et revient ; le "
                                   "cadenas tremble")
    hit = kit.move("maison", f, MAISON_BUMP_C, d=8, e="in")
    kit.move("maison", hit, MAISON_C, d=9, e="out")
    kit.shake("cadenas", hit - 1, amp=8)

    f = kit.at("S09", "argent,", "les trois places vides de la caisse battent, toujours vides")
    for pid in PLACES:
        kit.pulse(pid, f, peak=1.15)

    f = kit.at("S09", "vendre.", "« Toi » touche du stylo le bas de l'appartement : la pancarte « À vendre » naît sous "
                                 "la pointe et s'y accroche ; aussitôt le cadenas s'ouvre et tombe du rail")
    assert_reach(P1[0], MAISON_TAP_S09, "S09 appartement")
    hit = toi.tap(f - TAP + 1, list(MAISON_TAP_S09))
    kit.pop("a_vendre", hit, from_pt=toi.tip(hit))
    lower(toi, hit + 6)
    kit.drop("cadenas", hit + 6, out=True, h=300, dx=60, rot=20)
    S.key("cadenas", "scale", hit + 6 + DROP + 6, 0)

    # ================= S10 : des mois, des frais, un prix pas garanti =================
    f = kit.at("S10", "prend", "le « ≠ » et ses tirets s'effacent ; l'horloge ressort de l'appartement ; trois pièces "
                               "en sortent et avancent très lentement sur le rail vers la caisse, derrière le "
                               "livret ; l'horloge se remplit au même rythme")
    g_end = kit.at("S10", "garanti.", "les deux pièces restantes entrent dans la caisse ; la troisième place tremble, "
                                      "vide ; l'horloge s'arrête presque pleine")
    kit.vanish("different", f)
    for lid in ("lien_pilule", "lien_caisse"):
        S.key(lid, "draw", f, 0, 6, "in")
    S.key("horloge", "rot", f - 1, 0)
    kit.pop("horloge", f, scale=1, from_pt="maison", to=list(HORLOGE_C))
    s10 = COINS["s10"]
    file0 = FILE_S10
    for k, cid in enumerate([s10[1], s10[2], s10[0]]):       # de la tête à la queue
        kit.pop(cid, f + 2 * k, from_pt=list(RAIL_A), to=list(file0[s10.index(cid)]))
    drift0 = f + 4 + POP
    v = (file0[2][0] - 255) / (g_end - drift0)
    S.key("horloge", "value", f + POP, 50, g_end - f - POP, "linear")
    f_frais = kit.at("S10", "frais,", "une pilule « frais » tombe sous le rail ; la dernière pièce de la file quitte "
                                      "le rail et tombe à côté d'elle, les deux autres continuent")
    f_mois = kit.at("S10", "mois,", "une pilule « plusieurs mois » surgit au-dessus de l'horloge ; les pièces avancent")
    drop1 = f_frais + 4
    S.key(s10[0], "pos", drift0, [round(file0[0][0] - v * (drop1 - drift0), 2), AXE_Y], drop1 - drift0, "linear")
    for k in (1, 2):
        S.key(s10[k], "pos", drift0, [round(file0[k][0] - v * (g_end - drift0), 2), AXE_Y], g_end - drift0, "linear")

    kit.pop("delai_mois", f_mois)
    kit.drop("frais", f_frais, h=70, to=FRAIS_S10)
    kit.move(s10[0], drop1, FRAIS_PIECE_S10, d=9, e="in")

    f = kit.at("S10", "prix", "la pilule « 200 000 € » vacille sur la feuille (-8°, +8°, droite), ses deux pilules "
                              "fantômes et son « ? » battent ; le chiffre ne change pas")
    S.key("pastille", "rot", f, -8, 3, "out")
    S.key("pastille", "rot", f + 3, 8, 6, "inOut")
    S.key("pastille", "rot", f + 9, 0, 6, "inOut")
    kit.pulse("doute", f, times=2, peak=1.3)
    for k in range(2):
        kit.pulse(f"fourchette{k + 1}", f + 2, peak=1.1)

    f = g_end
    kit.move(s10[1], f, places_w[0], d=6, e="out")
    kit.move(s10[2], f, places_w[1], d=6, e="out")
    kit.shake("place3", f + 6, amp=6)

    # ================= S11 : chaque placement a son délai =================
    f = kit.at("S11", "l’immobilier", "l'horloge, « À vendre », « frais » et sa pièce, le « ? » rentrent dans "
                                      "l'appartement, qui se réduit sur place ; « plusieurs mois » se pose sous lui ; "
                                      "la feuille et la pilule se rangent en haut à droite ; les deux pièces vendues "
                                      "restent dans la caisse")
    kit.move("maison", f, MAISON_C, scale=MAISON_S11_K)
    kit.move("feuille", f, FEUILLE_RANGEE, scale=FEUILLE_RANGEE_K)
    kit.move("pastille", f, PASTILLE_RANGEE, scale=PASTILLE_RANGEE_K)
    S.key("pastille", "fill", f + 4, LIGHT, MOVE - 4)
    for k in range(2):
        kit.vanish(f"fourchette{k + 1}", f, into="pastille", d=8)
    for k, x in enumerate(["horloge", "a_vendre", "frais", s10[0], "doute"]):
        kit.vanish(x, f + 2 * k, into="maison")
    kit.move("delai_mois", f + 4, list(DELAI_MOIS_S11))

    f = kit.at("S11", "isolé :", "le rail s'allonge vers la droite jusqu'au bord (700 ms) : il devient une frise ; "
                                 "sa flèche bat, toujours pointée sur la caisse")
    S.key("rail", "pa", f, list(FRISE_A), 21, "out")
    kit.pulse("rail_fleche", f + 2, peak=1.3, step=4)

    fp = S.word_after("placement", f)
    kit.pulse("livret", fp, peak=1.15)
    kit.pulse("maison", fp + 5, peak=1.12 * MAISON_S11_K)
    kit.pulse("delai_mois", fp + 5, peak=1.12)

    f = kit.at("S11", "délai.", "l'horloge ressort de l'appartement et file se poser, petite, au bout lointain de la "
                                "frise (loin = lent) ; l'appartement, devenu disque, monte se ranger en haut à gauche "
                                "avec « plusieurs mois » : la première ligne de l'échelle")
    S.key("horloge", "value", f - 1, 50)
    kit.pop("horloge", f, scale=HORLOGE_FIN_K * 1.6, from_pt="maison", d=6)
    kit.move("horloge", f + 4, list(HORLOGE_FIN), d=12, scale=HORLOGE_FIN_K, arc=40)
    g = f + 6
    lp = lad_pt("maison")
    kit.vanish("maison", g, into=list(lp), d=14)
    S.key("maison_d", "pos", g - 1, list(MAISON_C))
    kit.pop("maison_d", g, scale=LAD_K, to=list(lp), d=14)
    kit.move("delai_mois", g + 2, list(lad_pill_pt("delai_mois")), d=14, arc=30)
    S.key("delai_mois", "fill", g + 12, PAPER, 4)
    kit.pop(LAD_NOMS["maison"], g + 11, d=6)

    # ================= S12 : comptes et livrets, quelques jours, sans perte =================
    f = kit.at("S12", "Comptes", "les deux pièces vendues s'enfoncent dans la caisse, qui bat ; « Comptes, livrets » "
                                 "surgit juste au-dessus du livret")
    for cid in s10[1:]:
        kit.vanish(cid, f, into="caisse")
    kit.pulse("caisse", f + 6, peak=1.05)
    kit.pop(NOMS["livret"][0], f + 2)

    f = kit.at("S12", "livrets :", "le livret bat et trois pièces en sortent au-dessus de son nom")
    kit.pulse("livret", f)
    s12 = COINS["s12"]
    for k, cid in enumerate(s12):
        kit.pop(cid, f + 2 * k, from_pt="livret", to=list(COINS_S12_FAN[k]))

    f = kit.at("S12", "quelques", "les trois pièces filent très vite dans les places de la caisse")
    for k, cid in enumerate(s12):
        kit.move(cid, f + 2 * k, places_w[S12_TO[k]], d=12)

    f = kit.at("S12", "jours,", "« quelques jours » surgit juste sous le livret")
    kit.pop("delai_jours", f)

    f = kit.at("S12", "perte.", "les trois pièces battent l'une après l'autre et « 3/3 » s'écrit sous la caisse : "
                                "rien de perdu")
    kit.stagger(s12, f, 4, kit.pulse, peak=1.2)
    S.key("compte", "pos", f - 1, list(COMPTE_C))
    S.key("compte", "chars", f - 1, 0)
    S.key("compte", "scale", f - 1, 1)
    S.key("compte", "opacity", f - 1, 1)
    kit.type("compte", f)

    # ================= S13 : l'assurance-vie, deux mois maximum =================
    f = kit.at("S13", "Pour", "les trois pièces s'enfoncent dans la caisse, qui bat ; « 3/3 » se réduit ; le livret "
                              "monte se ranger dans l'échelle avec « quelques jours »")
    for cid in s12:
        kit.vanish(cid, f, into="caisse")
    kit.pulse("caisse", f + 6, peak=1.05)
    kit.vanish("compte", f)
    file_away(S, kit, "livret", f)

    f = kit.at("S13", "assurance-vie,", "l'assurance-vie tombe sur la frise, au milieu ; « Assurance-vie » surgit "
                                        "juste au-dessus d'elle")
    g = kit.drop("assurance_vie", f, h=STAGE_C["assurance_vie"][1] - DROP_FROM_Y)
    kit.pop(NOMS["assurance_vie"][0], g - 4)

    f = kit.at("S13", "verser", "trois pièces sortent de l'assurance-vie et avancent lentement en file vers la caisse")
    s13 = COINS["s13"]
    for k, cid in enumerate(s13):
        kit.pop(cid, f + 2 * k, from_pt="assurance_vie", to=list(FILE_S13[k]))
    f_max = kit.at("S13", "maximum.", "les trois pièces entrent dans les places de la caisse, qui bat")
    f_deux = kit.at("S13", "deux", "« 2 mois max. » surgit juste sous l'assurance-vie ; les pièces avancent toujours")
    drift0 = f + 4 + POP
    for k, cid in enumerate(s13):
        tgt = places_w[S12_TO[k]]
        a = FILE_S13[k]
        mid = [round(a[0] + 0.85 * (tgt[0] - a[0]), 2), round(a[1] + 0.85 * (tgt[1] - a[1]), 2)]
        S.key(cid, "pos", drift0, mid, f_max - drift0, "linear")
    kit.pop("delai_2mois", f_deux)
    for k, cid in enumerate(s13):
        kit.move(cid, f_max, places_w[S12_TO[k]], d=5, e="out")
    kit.pulse("caisse", f_max + 5, peak=1.05)

    # ================= S14 : actions et fonds, vite, mais le prix varie =================
    f = kit.at("S14", "Actions", "les pièces s'enfoncent dans la caisse ; l'assurance-vie monte se ranger dans "
                                 "l'échelle avec « 2 mois max. » ; les actions tombent tout près de la caisse, nommées "
                                 "« Actions, fonds » juste au-dessus")
    for cid in s13:
        kit.vanish(cid, f, into="caisse")
    kit.pulse("caisse", f + 6, peak=1.05)
    file_away(S, kit, "assurance_vie", f)
    g = kit.drop("actions", f + 10, h=STAGE_C["actions"][1] - DROP_FROM_Y)
    kit.pop(NOMS["actions"][0], g - 4)

    f = kit.at("S14", "vendent", "trois pièces sortent des actions et filent dans la caisse en 9 images ; « vite » "
                                 "surgit juste sous les actions")
    s14 = COINS["s14"]
    for k, cid in enumerate(s14):
        kit.pop(cid, f + 2 * k, from_pt="actions", to=places_w[k], d=9)
    kit.pop("delai_vite", f)

    f = kit.at("S14", "prix", "une courbe en dents de scie se trace au-dessus du nom des actions")
    S.key("courbe", "scale", f, 1)
    kit.draw("courbe", f, DRAW)

    f = kit.at("S14", "varie.", "dans la caisse, les trois pièces grossissent et rapetissent à contretemps, puis "
                                "restent nettement différentes (x1,5, x0,6, x1) ; la place en tirets de la petite, "
                                "à sa taille d'avant, passe en cyan : elle vaut moins")
    peaks, finals = (1.35, 0.7, 1.2), (1.5, 0.6, 1.0)
    for k, cid in enumerate(s14):
        g = f + 3 * k
        S.key(cid, "scale", g, peaks[k], 3, "out")
        S.key(cid, "scale", g + 3, 1, 3, "inOut")
        S.key(cid, "scale", g + 6, finals[k], 5, "out")
    S.key("place2", "stroke", f + 9, CYAN, 4)
    S.key("place2", "sw", f + 9, 5, 4)
    kit.pulse("place2", f + 12, peak=1.12)
    assert f + 6 + 12 <= scene_f0(S, "S15") - 1
    hold_low(toi, f, f + 1)
