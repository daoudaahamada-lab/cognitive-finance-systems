"""V02, partie 2 : S08-S14, images 923-1801. Erreur 1 « Codes » (bulle de pensée : un mini « Mon budget » dont
l'écran montre une clé fantôme en tirets étiquetée « Mot de passe » ; la vraie clé reste dans la banque ; le stylo
barre la clé fantôme et la bulle éclate ; l'appli au loup dont le fil passe loin sous la porte et dont la pince bute
sur le mur devant la clé, coupée par « Toi » puis rouge) et erreur 2 « Société » (la société, coiffée d'un fronton
d'immeuble, sort de derrière le téléphone ; son badge nommé garde une case vide ; le registre REGAFI au sceau de
l'autorité ; le nom trouvé sur la feuille du registre, le badge prouvé et coché).

État d'entrée, épinglé à l'image 922 : kit.pin(922, ENTRY_P2). Figurines : `toi` en P2 ; `societe` à l'échelle 0,
cachée en SOC_HIDDEN derrière le téléphone (z 3 < 4).

Temps forts (image du film ; voir le titre de chaque bande de revue) :
S08  Première  croire  l’appli  passe.        (+ « principe » : la bulle tremble doucement)
S09  t’identifies  banque,  pas  l’appli.
S10  Une  demande  directement  codes  Méfiance.
S11  Ça  connexion  société  face.
S12  Deuxième  vérifier  qui  derrière  l’appli.
S13  France,  enregistrés  l’ACPR.        (+ « services » : le sceau bat)
S14  vérifier  gratuitement  REGAFI,  tapant  nom  société.

Raccord vers p3 : à l'image 1801, l'état est exactement ENTRY_P3 ; « Toi » en P2, stylo au repos ; société en
SOCIETE_C.
"""
import math

from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, text_width  # noqa: F401
from pipeline.story_kit import TAP

from . import (BADGE_H, BADGE_ON_SOC, BADGE_W, BOUTON_C, BULLE_C, BULLE_H, BULLE_W, CABLE_A, CABLE_B, CADENAS_BAS,
               CHAMP_TAP, CLE_HOME, COMPTES_MID, CYAN, DEEP, DOUTEUSE_C, DOUTEUSE_FIL_A, DOUTEUSE_FIL_B,
               DOUTEUSE_FIL_MID, DOUTEUSE_START, ENTRY_P2, HEAD_DY, P2, QUESTION2_C, RED, REG_DOT_X, REG_ROWS,
               REGISTRE_C,
               SOC_HIDDEN, SOCIETE_C, TOI_SCALE, bulle_ronds, fig_pos, cable_route, perle_route, ring, scene_f0, vanish)

F_START = 923
PHONE_BOTTOM = 982                         # bas du téléphone, ombre comprise : le badge (z 16) ne paraît qu'en dessous
BADGE_DY = BADGE_ON_SOC[1] - SOCIETE_C[1]  # badge : décalage vertical depuis le centre de la société
NAME_W = text_width("Société X", 30, 700)
P_S10 = fig_pos(822)                       # S10 : un pas à droite, la pointe au repos loin de la pince du fil


def bank_to_button(S, f):
    return [list(COMPTES_MID), list(CABLE_B)] + cable_route(S, f)[1:] + [list(BOUTON_C)]


def part(S, kit, c):
    toi, soc = c.toi, c.societe
    f0 = scene_f0(S, "S08")
    assert f0 == F_START, f0
    kit.pin(f0 - 1, ENTRY_P2)
    if S.val("toi", "scale", f0 - 1) == 0:                     # partie construite seule : « Toi » n'est pas entré
        toi.enter(f0 - 10, at=P2)
    if math.dist(S.val("toi", "pos", f0 - 1), P2) > 0.5:       # partie seule : « Toi » est resté en P1
        toi.walk(f0 - 1 - 36, P2, 36)

    # ================= S08 « Première erreur : croire que l'appli connaît ton mot de passe. » =================
    f = kit.at("S08", "Première", "repère : le disque 1 « Codes » s'allume en cyan, sa légende passe à l'encre")
    S.key("marqueur", "on", f, 1, MOVE, "out")

    f = kit.at("S08", "croire", "trois petits ronds en tirets sortent aussitôt de la tête de « Toi », puis une grande "
                                "bulle de pensée en tirets éclot au bout, dans la bande basse")
    head = S.to_world("toi", [0, HEAD_DY], f)
    corner = [BULLE_C[0] + BULLE_W / 2 - 18, BULLE_C[1] - BULLE_H / 2 + 18]
    for k, pt in enumerate(bulle_ronds(head, corner, head_r=35 * TOI_SCALE)):
        S.key(f"bulle_rond{k + 1}", "pos", f - 1, pt)
        kit.pop(f"bulle_rond{k + 1}", f + k, d=4)
    kit.pop("bulle", f + 3, from_pt=head, to=list(BULLE_C))

    f = kit.at("S08", "l’appli", "dans la bulle : un mini « Mon budget » (bouton cyan) dont l'écran montre une clé "
                                 "fantôme en tirets ; « Mot de passe » s'écrit sous la clé")
    kit.pop("bulle_tel", f)
    kit.type("bulle_txt", f + 5, rate=2)

    f = kit.at("S08", "passe.", "un guide en tirets file de la clé fantôme à la vraie clé, qui bat dans la banque "
                                "(anneau) sans bouger : deux clés, une seule vraie. Tenue")
    ghost = S.to_world("bulle_cle", [0, 0], f)
    S.key("bulle_guide", "pa", f - 1, [round(ghost[0] + 70, 2), round(ghost[1], 2)])
    S.key("bulle_guide", "pb", f - 1, [CLE_HOME[0] - 78, CLE_HOME[1] + 4])
    kit.draw("bulle_guide", f, 7, e="out")
    kit.pulse("cle", f + 5, peak=1.2, step=4)
    ring(S, "cle_anneau", f + 6, d=9)
    kit.shake("bulle", S.word_after("principe", f) + 4, amp=3)       # vie secondaire avant « t’identifies »

    # ================= S09 « En principe, tu t'identifies chez ta banque, pas dans l'appli. » =================
    f = kit.at("S09", "t’identifies", "« Toi » touche la vraie clé dans la banque : une coche pleine se trace à côté")
    hit = toi.tap(f - TAP + 1, list(CLE_HOME))
    kit.draw("cle_coche", hit, 6)
    toi.rest(hit + 6, 8)

    f = kit.at("S09", "banque,", "la clé ne bouge pas (son anneau bat sur place) : seules trois grosses pastilles de "
                                 "données sortent des comptes, passent la porte et filent jusqu'à l'écran du téléphone")
    ring(S, "cle_anneau", f, d=10)
    ends = []
    for k in range(3):
        t, pid = f + 4 * k, f"perle{k + 1}"
        ends.append(perle_route(S, pid, t, 17, bank_to_button(S, t)))
        S.key(pid, "scale", t, 1.5, 4, "out")                  # contrôle sans son : pastilles trop petites

    f = kit.at("S09", "pas", "chaque pastille se fond dans l'écran : les lignes de relevé battent l'une après l'autre "
                             "(l'appli a reçu des données, pas la clé) ; la bulle tremble fort")
    for k, end in enumerate(ends):
        vanish(kit, f"perle{k + 1}", end, into=list(BOUTON_C), d=5)
        kit.pulse(f"releve{k + 1}", end + 2, peak=1.12)
    kit.shake("bulle", f, amp=8)

    f = kit.at("S09", "l’appli.", "le stylo de « Toi » barre la clé fantôme d'un trait d'encre, puis la bulle éclate "
                                  "en éclats de tirets ; ses petits ronds et le guide disparaissent")
    gk = S.to_world("bulle_cle", [0, 0], f)
    a, b = [round(gk[0] + 60, 2), round(gk[1] - 32, 2)], [round(gk[0] - 30, 2), round(gk[1] + 30, 2)]
    S.key("bulle_barre", "pa", f - 1, a)
    S.key("bulle_barre", "pb", f - 1, b)
    kit.draw("bulle_guide", f, 4, to=0, e="in")
    end = toi.strike(f - 4, a, b, d=5, lead=4, line="bulle_barre", track="draw", step=False)
    toi.rest(end + 1, 8)
    burst = end + 2
    S.key("bulle_barre", "opacity", burst, 0, 3, "linear")
    kit.vanish("bulle", burst, style="burst", n=16, spread=130, sw=6)   # contrôle sans son : « se dissout »
    S.key("coupure", "pos", burst - 1, list(BULLE_C))                    # gros éclair au cœur de la bulle
    S.key("coupure", "scale", burst - 1, 2.4)
    S.key("coupure", "p", burst, 1, 7, "out")
    S.key("coupure", "p", burst + 7, 0)
    for k, rid in enumerate(["bulle_rond3", "bulle_rond2", "bulle_rond1"]):
        kit.vanish(rid, burst + 2 * (k + 1), style="burst", n=5, spread=24, sw=3)

    # ================= S10 « Une appli te demande directement tes codes bancaires ? Méfiance. » =================
    f = kit.at("S10", "Une", "une autre appli, en-tête noir au loup de voleur, sans bouton cyan, entre par le bord "
                             "gauche, loin du téléphone")
    S.key("douteuse", "pos", f - 1, list(DOUTEUSE_START))
    S.key("douteuse", "scale", f - 1, 1)
    S.key("douteuse", "opacity", f - 1, 1)
    kit.move("douteuse", f, DOUTEUSE_C, MOVE, e="out")
    toi.walk(f, list(P_S10), 8)                                # « Toi » s'écarte : sa pointe ne touche pas le fil

    f = kit.at("S10", "demande", "son écran écrit « Tes codes ? », puis un champ vide surgit dessous")
    g = kit.type("douteuse_txt", f, rate=1)
    kit.pop("douteuse_champ", g - 4)

    A, M, B = DOUTEUSE_FIL_A, DOUTEUSE_FIL_MID, DOUTEUSE_FIL_B
    L = math.dist(M, B)
    u = ((B[0] - M[0]) / L, (B[1] - M[1]) / L)
    B0 = [round(B[0] - 22 * u[0], 2), round(B[1] - 22 * u[1], 2)]
    S.set("douteuse_fil2", pb=B0)

    f = kit.at("S10", "directement", "la porte officielle et son câble s'allument (la voie officielle) ; le fil épais en "
                                     "tirets de l'appli passe loin sous la porte, vers la clé, et finit par une pince "
                                     "ouverte tournée vers elle")
    kit.pulse("porte", f, peak=1.06)
    kit.pulse("porte_dsp2", f, peak=1.1)
    S.key("cable", "color", f, CYAN, 3, "out")
    S.key("cable", "color", f + 9, DEEP, 6, "inOut")
    # contrôle sans son : le contraste « porte officielle / fil qui la contourne » ne se voyait pas. Pendant que le
    # fil passe SOUS la porte, une pastille fait le vrai chemin, À TRAVERS la porte, jusqu'au bouton
    end = perle_route(S, "perle1", f, 18, bank_to_button(S, f))
    S.key("perle1", "scale", f, 1.4, 4, "out")
    vanish(kit, "perle1", end, into=list(BOUTON_C), d=5)
    kit.draw("douteuse_fil1", f + 2, 6, e="linear")
    kit.draw("douteuse_fil2", f + 8, 6, e="out")
    S.key("douteuse_pince", "pos", f + 12, B0)
    kit.pop("douteuse_pince", f + 12, d=5)

    f = kit.at("S10", "codes", "la pince cogne le mur de la banque juste devant la clé : un trait de mur et un cadenas "
                               "s'y posent, la clé tremble ; le fil recule. Le mur protège la clé")
    S.key("douteuse_fil2", "pb", f, list(B), 2, "in")
    S.key("douteuse_pince", "pos", f, list(B), 2, "in")
    kit.pop("mur_bas", f + 1, d=3)
    S.key("cadenas", "pos", f - 1, list(CADENAS_BAS))
    kit.pop("cadenas", f + 2, d=4)
    kit.shake("cle", f + 2, amp=6)
    kit.shake("cle", f + 5, amp=4)
    back = [round(B[0] - 24 * u[0], 2), round(B[1] - 24 * u[1], 2)]
    S.key("douteuse_fil2", "pb", f + 8, back, 6, "out")
    S.key("douteuse_pince", "pos", f + 8, back, 6, "out")

    f = kit.at("S10", "Méfiance.", "le stylo de « Toi » coupe le fil sous la porte d'un grand trait : gros éclair, les "
                                   "deux moitiés se rétractent et tombent, loin l'une de l'autre ; le stylo se retire ; "
                                   "ensuite seulement l'appli vire au rouge et tremble")
    a = [M[0] + 30, M[1] - 64]                                 # contrôle sans son : « coup de stylet petit »
    b = [M[0] - 30, M[1] + 70]
    end = toi.strike(f - 4, a, b, d=6, lead=4, step=False)     # pointe sur a à f - 1 ; elle passe sur le fil vers f + 3
    cut = f + 3
    S.key("coupure", "pos", cut - 1, list(M))
    S.key("coupure", "scale", cut - 1, 1.7)
    S.key("coupure", "p", cut, 1, 7, "out")
    S.key("coupure", "p", cut + 7, 0)
    toi.rest(end + 1, 8)
    for wid, tr, anchor in (("douteuse_fil1", "pb", A), ("douteuse_fil2", "pa", B)):
        tgt = [round(M[0] + 0.4 * (anchor[0] - M[0]), 2), round(M[1] + 0.4 * (anchor[1] - M[1]) + 56, 2)]
        S.key(wid, tr, cut, tgt, 9, "out")
        S.key(wid, "sag", cut, 22, 9, "out")
    red = cut + 2                                              # contrôle sans son : « le passage au rouge est bref »
    S.key("douteuse", "stroke", red, RED, 6, "out")
    S.key("douteuse_txt", "color", red, RED, 6, "out")
    S.key("douteuse_tete", "fill", red, RED, 6, "out")        # l'en-tête au loup vire au rouge : un grand aplat
    kit.shake("douteuse", red + 4, amp=8)

    # ================= S11 « Ça ne suffit pas : une connexion propre ne dit rien de la société en face. » ==========
    f = kit.at("S11", "Ça", "l'appli rouge tombe et s'efface, avec les deux moitiés du fil et la pince ; le mur et le "
                            "cadenas rentrent dans la banque")
    H = 90
    kit.drop("douteuse", f, h=H, out=True)
    toi.walk(f + 2, list(P2), 8)
    for wid in ("douteuse_fil1", "douteuse_fil2"):
        for tr in ("pa", "pb"):
            p = S.val(wid, tr, f - 1)
            S.key(wid, tr, f, [p[0], round(p[1] + H, 2)], DROP, "out")
        S.key(wid, "opacity", f + DROP // 2, 0, 6, "linear")
        S.key(wid, "draw", f + DROP + 2, 0)
    kit.drop("douteuse_pince", f, h=H, out=True)
    S.key("douteuse", "scale", f + DROP + 2, 0)
    S.key("douteuse_pince", "scale", f + DROP + 2, 0)
    vanish(kit, "cadenas", f, into=[CLE_HOME[0] - 40, CLE_HOME[1]], d=7)
    vanish(kit, "mur_bas", f + 2, d=6)

    f = kit.at("S11", "connexion", "une pastille propre part des comptes, franchit la porte et rejoint le bouton")
    end = perle_route(S, "perle1", f, 18, bank_to_button(S, f))
    vanish(kit, "perle1", end, into=list(BOUTON_C), d=6)
    kit.pulse("releve2", end + 3, peak=1.08)

    f = kit.at("S11", "société", "le téléphone se soulève : la société (silhouette blanche coiffée d'un fronton "
                                 "d'immeuble) sort de derrière lui ; sur sa poitrine, un grand immeuble et un badge vide "
                                 "en tirets, relié au téléphone par un fil en tirets")
    for id in ("appli", "bouton", "interrupteur"):
        p = S.val(id, "pos", f - 1)
        S.key(id, "pos", f, [p[0], p[1] - 18], 4, "out")
        S.key(id, "pos", f + 10, list(p), 8, "inOut")
    S.key("cable", "pa", f, [CABLE_A[0], CABLE_A[1] - 18], 4, "out")
    S.key("cable", "pa", f + 10, list(CABLE_A), 8, "inOut")
    soc.enter(f - POP - 1, at=list(SOC_HIDDEN))                # cachée sous le calque du téléphone (z 3 < 4)
    mid = [118, 1040]
    S.key("badge", "pos", f - 1, [SOC_HIDDEN[0], round(SOC_HIDDEN[1] + BADGE_DY, 2)])
    soc.hop(f, mid, 8, h=0)
    soc.hop(f + 8, list(SOCIETE_C), 10, h=0)
    S.key("badge", "pos", f, [mid[0], round(mid[1] + BADGE_DY, 2)], 8, "linear")
    S.key("badge", "pos", f + 8, list(BADGE_ON_SOC), 10, "out")
    show = next(n for n in range(f, f + 18) if S.val("badge", "pos", n)[1] - BADGE_H / 2 > PHONE_BOTTOM)
    S.key("badge", "opacity", show, 1)
    S.key("badge", "scale", show - 1, 0)
    S.key("badge", "scale", show, 1, 5, "out")
    kit.draw("attache", show + 3, 8)

    f = kit.at("S11", "face.", "la société s'incline vers « Toi » : face à face. Tenue")
    soc.lean_to(f, 10)

    # ================= S12 « Deuxième erreur : ne pas vérifier qui est derrière l'appli. » =================
    f = kit.at("S12", "Deuxième", "repère : le disque actif glisse sur 2 « Société » ; le disque 1 garde une coche, "
                                  "sa légende reste à l'encre (étape faite)")
    kit.step(f, 1)
    S.key("marqueur", "done0", f + 6, 1, MOVE, "out")

    f = kit.at("S12", "vérifier", "un « ? » naît de la pointe du stylo de « Toi » et vole jusqu'à côté du fronton de "
                                  "la société")
    tip = toi.tip(f - 1)
    kit.pop("question2", f, from_pt=tip, to=tip)
    kit.move("question2", f + 3, QUESTION2_C, MOVE, arc=60)

    f = kit.at("S12", "qui", "le contour en tirets du badge bat deux fois ; il reste vide")
    kit.pulse("badge_fond", f, times=2)

    f = kit.at("S12", "derrière", "« Société X » s'écrit dans le badge ; une case de coche VIDE, en tirets, surgit au "
                                  "bout du badge ; le contour reste en tirets")
    g = kit.type("badge_nom", f, rate=1.5)
    kit.pop("badge_case", g, d=5)

    f = kit.at("S12", "l’appli.", "la case vide du badge et le « ? » de « Toi » battent deux fois ensemble : nommée, "
                                  "pas vérifiée. Tenue")
    kit.pulse("question2", f, times=2)
    kit.pulse("badge_case", f, times=2, peak=1.3)

    # ================= S13 « En France, ces services doivent être enregistrés auprès de l'ACPR. » =================
    f = kit.at("S13", "France,", "un registre (livre ouvert, sceau rond de l'autorité sur la page de gauche, une "
                                 "feuille vierge sur celle de droite, bandeau vide au-dessus) monte du bas entre la "
                                 "société et « Toi »")
    kit.pop("registre", f, from_pt=[REGISTRE_C[0], 1250])
    kit.pulse("registre_sceau", S.word_after("services", f), peak=1.15)   # vie secondaire

    f = kit.at("S13", "enregistrés", "trois téléphones tombent dans les rangées de la feuille, un trait se trace à "
                                     "côté de chacun : des applis inscrites")
    for k, dy in enumerate(REG_ROWS):
        t, tr, tel = f + 4 * k, f"registre_trait{k + 1}", f"registre_tel{k + 1}"
        S.key(tel, "opacity", t - 1, 0)
        kit.drop(tel, t, h=30)
        w0 = S.ents[tr]["p"]["w"]
        x0 = S.val(tr, "pos", t)[0]
        S.set(tr, w=w0)
        S.key(tr, "w", t + 5, 0)
        S.key(tr, "pos", t + 5, [x0 - w0 / 2, dy])
        S.key(tr, "draw", t + 6, 1)                            # trait plein : il s'allonge vers la droite
        S.key(tr, "w", t + 6, w0, 6, "out")
        S.key(tr, "pos", t + 6, [x0, dy], 6, "out")

    f = kit.at("S13", "l’ACPR.", "« ACPR » s'abat sur la page de gauche comme un tampon ; le sceau du registre et la "
                                 "porte DSP2 battent ensemble : la même autorité. Tenue")
    S.key("registre_acpr", "opacity", f - 1, 0)
    land = kit.drop("registre_acpr", f, h=110, d=7)
    S.key("registre_acpr", "scale", f, 1.3)
    S.key("registre_acpr", "scale", land, 1.0, 4, "out")
    kit.shake("registre", land, amp=4, axis="y")
    for id, pk in (("registre_sceau", 1.25), ("porte", 1.07), ("porte_dsp2", 1.15)):
        kit.pulse(id, land + 3, peak=pk, step=4, times=2)

    # ================= S14 « Tu peux le vérifier gratuitement sur le registre REGAFI, en tapant le nom… » ==========
    vanish(kit, "question2", S.word_after("Tu", scene_f0(S, "S14") - 3))   # la vérification va répondre au « ? »

    f = kit.at("S14", "vérifier", "un champ de recherche surgit au-dessus du livre ; « Toi » lève son stylo vers lui")
    kit.pop("champ", f)
    toi.reach(f + 3, list(CHAMP_TAP), MOVE)

    f = kit.at("S14", "gratuitement", "une pilule « gratuit » surgit à GAUCHE du champ")
    kit.pop("gratuit", f)

    f = kit.at("S14", "REGAFI,", "« REGAFI » s'écrit sur le bandeau au-dessus du livre")
    kit.type("registre_titre", f, rate=1)

    f = kit.at("S14", "tapant", "« Toi » touche le champ : « Société X » s'y tape")
    hit = toi.tap(f - TAP + 1, list(CHAMP_TAP))
    S.key("champ_nom", "opacity", hit - 1, 1)
    kit.type("champ_nom", hit, rate=1.2)
    toi.rest(hit + 8, 8)

    f = kit.at("S14", "nom", "le nom tapé quitte le champ, descend sur la feuille du registre et se pose sur la "
                             "rangée du milieu, qui se surligne ; le champ et « gratuit » s'effacent aussitôt")
    vanish(kit, "registre_trait2", f, d=6)
    vanish(kit, "registre_tel2", f, d=6)
    name_c = S.to_world("registre_nom", [NAME_W / 2, 0], f)
    S.fly("champ_nom", f, 9, "inOut", to=name_c, scale=30 / 32)
    land = f + 9
    S.key("champ_nom", "opacity", land, 0)                     # relais instantané : le nom du livre prend la place
    S.key("registre_nom", "chars", land, len("Société X"))
    kit.draw("registre_nom", land, 5, track="mark")
    kit.morph(["champ", "gratuit"], [], f + 3, d=8)

    f = kit.at("S14", "société.", "« Toi » touche l'inscription : une coche s'y trace ; un fil plein court du bout de la "
                                  "rangée, le long du bas du livre, jusqu'au badge : la case vide devient une coche "
                                  "pleine, le contour devient plein ; son attache devient pleine")
    tgt = S.to_world("registre_nom", [NAME_W - 30, 2], f)
    hit = toi.tap(f - TAP + 1, tgt)
    kit.draw("registre_coche", hit, 6)
    pa = S.to_world("registre_page", [REG_DOT_X, REG_ROWS[1]], hit)
    pb = [BADGE_ON_SOC[0] + BADGE_W / 2 - 8, BADGE_ON_SOC[1] + 8]
    S.key("preuve", "pa", hit + 2, [round(v, 2) for v in pa])
    S.key("preuve", "pb", hit + 2, pb)
    S.key("preuve", "sag", hit + 2, 64)
    arrive = kit.draw("preuve", hit + 3, 9)
    kit.pulse("badge", arrive - 1, peak=1.12)
    vanish(kit, "badge_case", arrive + 2, d=5)
    kit.draw("badge_plein", arrive + 3, 6)
    kit.draw("badge_coche", arrive + 3, 6)
    kit.draw("attache_pleine", arrive + 5, 8)
    end = toi.rest(hit + 6, 10)
    assert max(end, arrive + 13) <= scene_f0(S, "S15") - 1, (end, arrive)
