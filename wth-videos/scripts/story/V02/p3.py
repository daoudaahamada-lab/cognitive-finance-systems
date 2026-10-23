"""V02, partie 3 : S15-S22, images 1802-2677. Erreur 3 « Accès » (l'appli testée branchée par « Toi » À TRAVERS la
porte, le cadran des mois, l'appli oubliée - « Toi » lui tourne le dos - qui reçoit encore des données par la porte,
coupée des deux côtés : un bout par interrupteur), la chute Avant / Maintenant sur le même montage (cadre en tirets,
balayage de droite à gauche, triple clic, alertes numérotées tombées du repère -> coches de « Toi » qui retournent
au repère), la carte de fin.

État d'entrée, épinglé à l'image 1801 : kit.pin(1801, ENTRY_P3). Figurines : `toi` en P2 ; `societe` en SOCIETE_C.

Temps forts (image du film ; voir le titre de chaque bande de revue) :
S15  Et  s’arrête  jour  connectes.
S16  Troisième  oublier  accès  n’utilises     (+ « testée » en S17 : l'appli testée bat)
S17  6  encore  actif.
S18  Coupe-le  réglages  l’appli.  propose,  espace  aussi.     (+ « banque » : la banque bat)
S19  Avant,  tu  cliquais  sans  réfléchir.
S20  Maintenant,  t’identifies  banque  vérifies  REGAFI.
S21  Et  6  tri.
S22  Abonne-toi  comprendre  argent.

« Toi » touche toujours ce qui est à sa GAUCHE (appli testée, panneau, clé, pilule « REGAFI ») : aucun bras en
travers du buste. Quand il traverse la bande basse, il passe DERRIÈRE l'appli testée (calque 9,4 < 10) : il ne
couvre jamais « Appli testée ».

Écarts d'exécution (places et temps seulement, aucun temps fort déplacé) :
- S16 « oublier » : « Toi » se tourne de profil vers la droite (piste look) et s'écarte jusqu'à x 872 seulement : au-delà,
  la zone réservée de droite (x > 940) serait touchée ;
- S18 : le panneau « Espace client » s'ouvre DANS la carte de la banque, sur les comptes (deux lignes ON) ;
- S20 « vérifies » / « REGAFI. » : une pilule « REGAFI » (le registre en raccourci) tombe d'en haut dans la place
  libérée par la bulle, au lieu du livre réduit ; « Toi » bondit à sa portée sur « et tu ».
"""
import math

from pipeline.story import DRAW, FADE, MORPH, MOVE, POP  # noqa: F401
from pipeline.story_kit import TAP

from . import (ALERTES_S19, BADGE_H, BADGE_UNDER_PHONE, BANK_C, BOUTON_C, BOUTON_TAP, BULLE_H, BULLE_S19,
               BULLE_S19_K, BULLE_W, CABLE_B, CABLE_LOOSE, CABLE_T_A, CABLE_T_B, CADRAN_S21, CADRE_C, CADRE_W,
               COMPTES_MID, ENTRY_P3, ESPACE_C, FICHE_APP_C, FICHE_C, FIN_BUTTON, FIN_TAP, GREY, HEAD_DY, MARKER_XS,
               MARKER_Y, P1, P2, P_BACK, P_S19, BOUTON_TAP_S19, CLE_HOME, CYAN, DEEP, P_REG, PAPER, REGAFI_PILL_C, SOC_HIDDEN, SOCIETE_C,
               TESTEE_SWITCH, TESTEE_TOP, TOI_SCALE, bulle_ronds, cable_route, fig_pos, perle_route, press, ring,
               scene_f0, t_at_x, toggle, vanish, wire_point)

F_START = 1802
P_AWAY = fig_pos(872)                      # S16 : « Toi » s'écarte à droite, de profil, dos à l'appli testée
CARD_BTN_SCALE = 1.4                       # bouton 250 x 96 -> 380 x 112 (bouton de la carte de fin)
REGAFI_W = 156
Z_BEHIND, Z_TOOL_BEHIND = 9.4, 9.45        # « Toi » passe derrière l'appli testée (z 10)
Z_TOI, Z_TOOL = 15, 15.5


def bank_to_testee(S, f):
    """Comptes -> câble principal jusqu'au tourniquet de la porte -> câble de l'appli testée -> haut de l'appli."""
    t_gate = t_at_x(S, "cable", 515, f)
    main = cable_route(S, f, 1.0, t_gate, 20)
    branch = [wire_point(S, "cable_testee", i / 20, f) for i in range(21)]
    return [list(COMPTES_MID), list(CABLE_B)] + main[1:] + branch[1:]


def bank_to_button(S, f):
    return [list(COMPTES_MID), list(CABLE_B)] + cable_route(S, f)[1:] + [list(BOUTON_C)]


def cross(toi, f, to, d, hop=None):
    """« Toi » traverse la bande basse DERRIÈRE l'appli testée : calque bas pendant le trajet. -> f + d."""
    toi.set_z(f, Z_BEHIND, tool_z=Z_TOOL_BEHIND)
    end = toi.hop(f, list(to), d, h=hop) if hop is not None else toi.walk(f, list(to), d)
    toi.set_z(end, Z_TOI, tool_z=Z_TOOL)
    return end


def resolve(S, kit, k, f, d=6):
    """L'alerte k se change SUR PLACE en coche pleine numérotée (elle reste à côté de son objet jusqu'à la carte de
    fin) ; dans le même temps le disque k du repère se coche et bat. -> image où tout est posé."""
    a, ok = f"alerte{k + 1}", f"alerte{k + 1}_ok"
    S.key(ok, "pos", f - 1, list(ALERTES_S19[k]))
    kit.morph([a], [ok], f, d=d)
    kit.draw(f"{ok}_coche", f + 1, d)
    S.key("marqueur", f"done{k}", f + 1, 1, d, "out")
    S.key(f"marqueur_ping{k + 1}", "pos", f, [MARKER_XS[k], MARKER_Y])
    ring(S, f"marqueur_ping{k + 1}", f + 1, d=10, s0=0.6, s1=1.3)
    return f + d + 1


def part(S, kit, c):
    toi = c.toi
    f0 = scene_f0(S, "S15")
    assert f0 == F_START, f0
    kit.pin(f0 - 1, ENTRY_P3)
    if S.val("toi", "scale", f0 - 1) == 0:
        toi.enter(f0 - 10, at=P2)
    if math.dist(S.val("toi", "pos", f0 - 1), P2) > 0.5:
        toi.walk(f0 - 1 - 36, P2, 36)
    if S.val("societe", "scale", f0 - 1) == 0:                 # partie seule : l'immeuble n'est pas sorti
        S.key("societe", "pos", f0 - 2, list(SOCIETE_C))
        S.key("societe", "scale", f0 - 2, 1)
    kit.ensure("toi", "look", 0)

    # ================= S15 « Et le risque ne s’arrête pas le jour où tu te connectes. » =================
    f = kit.at("S15", "Et", "rangement : le registre se réduit, le fil de preuve se rétracte ; l'attache pleine tire "
                            "le badge coché sous le téléphone pendant que la société rentre derrière lui")
    kit.morph(["registre"], [], f)
    kit.draw("preuve", f, 8, to=0)
    kit.move("societe", f, list(SOC_HIDDEN), MOVE)
    S.key("societe", "scale", f + MOVE, 0)                     # cachée sous le calque du téléphone (z 3 < 4)
    kit.move("badge", f, BADGE_UNDER_PHONE, MOVE)
    for wid in ("attache", "attache_pleine"):
        kit.draw(wid, f + MOVE, 6, to=0)

    f = kit.at("S15", "s’arrête", "en bas, sous la porte, surgit une seconde appli « Appli testée », interrupteur sur "
                                  "OFF, sans câble")
    kit.pop("testee", f)

    f = kit.at("S15", "jour", "un cadran de 12 mois surgit, vide, au-dessus de la porte, avec son compteur « 0 mois »")
    kit.pop("cadran", f)
    kit.pop("cadran_txt", f + 3)

    f = kit.at("S15", "connectes.", "« Toi » met l'interrupteur de l'appli testée sur ON : un câble descend de la porte "
                                    "jusqu'à elle ; le cadran commence à se remplir lentement")
    hit = toi.tap(f - TAP + 1, list(TESTEE_SWITCH))
    toggle(S, "testee_inter", hit, True)
    kit.draw("cable_testee", hit + 3, DRAW)
    toi.rest(hit + 6, 8)
    f_six = S.word_after("6", hit)
    S.key("cadran", "value", hit, 6, f_six - hit, "linear")   # la seule dérive du film, jusqu'à « 6 » (S17)
    S.key("cadran_txt", "value", hit, 6, f_six - hit, "linear")   # le compteur dit ce que le cadran mesure : des mois

    # ================= S16 « Troisième erreur : oublier les accès que tu n’utilises plus. » =================
    f = kit.at("S16", "Troisième", "repère : le disque actif glisse sur 3 « Accès » ; le disque 2 garde une coche, "
                                   "sa légende reste à l'encre ; le cadran continue de se remplir")
    kit.step(f, 2)
    S.key("marqueur", "done1", f + 6, 1, MOVE, "out")

    f = kit.at("S16", "oublier", "« Toi » range son stylo, se tourne de profil vers la droite (dos à l'appli testée) "
                                 "et s'en éloigne ; l'appli se rétracte un instant")
    toi.stow(f)
    S.key("toi", "look", f, 1, 4, "out")
    toi.walk(f + 2, list(P_AWAY), 14)
    kit.pulse("testee", f + 6, peak=0.93, step=4)

    f = kit.at("S16", "accès", "l'interrupteur de l'appli testée, toujours sur ON, bat deux fois")
    kit.pulse("testee_inter", f, times=2)

    f = kit.at("S16", "n’utilises", "l'appli testée s'éteint : son écran devient gris et son contour passe en tirets ; "
                                    "l'interrupteur reste ON (cyan), le câble branché")
    # tour sans son 1 : la lune se lisait « l'utilisateur s'endort » -> écran gris éteint, interrupteur toujours ON
    S.key("testee", "fill", f, GREY, POP, "out")
    S.key("testee", "stroke", f, PAPER, POP, "out")
    kit.pop("testee_veille", f, d=POP)
    kit.pulse("testee", S.word_after("testée", f), peak=1.05)    # vie secondaire (S17 « Une appli testée »)

    # ================= S17 « Une appli testée il y a 6 mois peut encore avoir un accès actif. » =================
    f = kit.at("S17", "6", "le cadran arrive à 6 sur 12 et s'arrête ; le compteur « 6 mois » bat")
    assert f == f_six, (f, f_six)
    kit.pulse("cadran_txt", f, peak=1.2, step=4)

    f = kit.at("S17", "encore", "un flot serré de grosses pastilles sort des comptes, passe par la porte et descend "
                                "dans l'appli éteinte : les lignes de données s'y empilent")
    for k in range(6):                     # deux vagues de trois (tour sans son 1 : « points très discrets »)
        t, pid = f + 5 * (k % 3) + 24 * (k // 3), f"perle{k % 3 + 1}"
        end = perle_route(S, pid, t, 18, bank_to_testee(S, t))
        S.key(pid, "scale", t, 1.4, 4, "out")
        vanish(kit, pid, end, into=list(TESTEE_TOP), d=5)
        if k < 3:
            kit.pop(f"testee_l{k + 1}", end + 1, d=6)
        else:
            kit.pulse(f"testee_l{k - 2}", end + 1, peak=1.15)
    assert end + 5 <= scene_f0(S, "S18"), end

    f = kit.at("S17", "actif.", "l'interrupteur ON de l'appli testée bat deux fois : l'accès est toujours actif")
    kit.pulse("testee_inter", f, times=2)

    # ================= S18 « Coupe-le dans les réglages de l’appli. Et si ta banque le propose… aussi. » ==========
    # tour sans son 1 : « deux options ? » -> un seul câble, DEUX fiches qui sautent l'une après l'autre (côté appli,
    # puis côté banque) ; UNE coche, seulement quand les deux sont tombées ; le câble de « Mon budget » reste actif
    f = kit.at("S18", "Coupe-le", "« Toi » ressort son stylo, se retourne et revient à droite de l'appli testée ; les "
                                  "deux fiches cyan du câble paraissent, une à chaque bout (porte, appli)")
    toi.unstow(f)
    S.key("toi", "look", f, 0, 4, "out")
    toi.walk(f, list(P2), 12)
    kit.pop("fiche", f + 2, d=6)
    kit.pop("fiche_app", f + 5, d=6)
    kit.pulse("banque", S.word_after("banque", f), peak=1.04)        # vie secondaire (« Et si ta banque le… »)

    f = kit.at("S18", "réglages", "« Toi » touche l'interrupteur de l'appli testée (à sa gauche) : il passe sur OFF")
    hit = toi.tap(f - TAP + 1, list(TESTEE_SWITCH))
    toggle(S, "testee_inter", hit, False)
    toi.rest(hit + 6, 8)

    f = kit.at("S18", "l’appli.", "1re fiche : la fiche côté appli saute (étincelle) et pend au bout du câble ; la fiche "
                                  "côté porte reste branchée et bat")
    S.key("coupure", "pos", f - 1, list(FICHE_APP_C))
    S.key("coupure", "scale", f - 1, 0.9)
    S.key("coupure", "p", f, 1, 6, "out")
    S.key("coupure", "p", f + 6, 0)
    S.key("cable_testee", "pb", f, CABLE_LOOSE, POP, "out")
    S.key("cable_testee", "sag", f, 24, POP, "out")
    S.key("fiche_app", "pos", f, [CABLE_LOOSE[0] + 4, CABLE_LOOSE[1] + 10], POP, "out")
    S.key("fiche_app", "rot", f, 70, POP, "out")
    kit.pulse("fiche", f + 10, times=2, peak=1.3)

    f = kit.at("S18", "propose,", "dans la banque s'ouvre une fenêtre « Espace client » : deux lignes, « Mon budget » "
                                  "ON et « Appli testée » ON ; une pastille file toujours vers « Mon budget »")
    kit.pop("espace_client", f, from_pt=list(BANK_C), to=list(ESPACE_C))
    end = perle_route(S, "perle2", f + 6, 18, bank_to_button(S, f + 6))
    vanish(kit, "perle2", end, into=list(BOUTON_C), d=5)

    f = kit.at("S18", "espace", "« Toi » met la ligne « Appli testée » sur OFF : 2e fiche, côté porte, elle saute avec "
                                "une étincelle ; le câble tombe, libre aux deux bouts ; alors seulement une coche "
                                "pleine se trace près de l'appli ; le câble de « Mon budget » s'allume, toujours actif")
    tgt = S.to_world("espace_inter2", [0, 0], f - TAP)
    hit = toi.tap(f - TAP + 1, tgt)
    toggle(S, "espace_inter2", hit, False)
    S.key("coupure", "pos", hit - 1, list(FICHE_C))
    S.key("coupure", "scale", hit - 1, 1)
    S.key("coupure", "p", hit, 1, 6, "out")
    S.key("coupure", "p", hit + 6, 0)
    kit.drop("fiche", hit, h=70, out=True, dx=12, rot=40)
    kit.drop("fiche_app", hit + 2, h=80, out=True, dx=-8, rot=-30)
    for tr in ("pa", "pb"):
        p = S.val("cable_testee", tr, hit - 1)
        S.key("cable_testee", tr, hit, [p[0], round(p[1] + 90, 2)], 10, "in")
    S.key("cable_testee", "opacity", hit + 4, 0, 6, "linear")
    S.key("cable", "color", hit + 2, CYAN, 3, "out")              # « Mon budget » : son câble reste actif
    S.key("cable", "color", hit + 14, DEEP, 6, "inOut")
    kit.draw("coupe_coche1", hit + 10, 7)                          # les deux fiches sont tombées : coupé
    toi.rest(hit + 6, 8)

    f = kit.at("S18", "aussi.", "une pastille sort de la banque, passe par la porte et arrive à « Mon budget » ; la "
                                "ligne « Mon budget » du panneau bat, toujours ON : l'appli utilisée reste branchée")
    end = perle_route(S, "perle1", f, 18, [list(CABLE_B)] + cable_route(S, f)[1:] + [list(BOUTON_C)])
    S.key("perle1", "scale", f, 1.3, 4, "out")
    vanish(kit, "perle1", end, into=list(BOUTON_C), d=6)
    kit.pulse("espace_inter1", f + 2, times=2, peak=1.25)
    kit.pulse("releve1", end + 2, peak=1.08)
    kit.pulse("coupe_coche1", end + 4, peak=1.2)

    # ================= S19 « Avant, tu cliquais sans réfléchir. » =================
    f = kit.at("S19", "Avant,", "retour en arrière : un cadre en tirets entoure le montage, « ◀◀ Avant » surgit en "
                                "grand en haut ; une barre balaie l'image de droite à gauche et défait tout sur son "
                                "passage (panneau, coches, câble rebranché ON, cadran, badge) ; « Toi » recule")
    kit.pop("etiquette_avant", f, scale=1.25)
    S.key("etiquette_avant", "scale", f + 16, 1.12, 8, "inOut")
    kit.draw("cadre_avant", f, 9)
    x0, x1, sweep = CADRE_C[0] + CADRE_W / 2 - 20, CADRE_C[0] - CADRE_W / 2 + 20, 12
    kit.pop("balayage", f, d=2)
    S.key("balayage", "pos", f, [x1, CADRE_C[1]], sweep, "linear")
    S.key("balayage", "opacity", f + sweep - 1, 0, 3, "linear")

    def at_x(x):
        return f + round((x0 - x) / (x0 - x1) * sweep)
    kit.draw("cle_coche", at_x(885), 4, to=0)
    kit.draw("coupe_coche2", at_x(550), 4, to=0)
    kit.draw("coupe_coche1", at_x(500), 4, to=0)
    vanish(kit, "espace_client", at_x(800), into=list(BANK_C), d=6)
    g = at_x(620)
    for tr, v in (("pa", list(CABLE_T_A)), ("pb", list(CABLE_T_B)), ("sag", 0), ("draw", 0), ("opacity", 1)):
        S.key("cable_testee", tr, g - 1, v)
    kit.draw("cable_testee", g, 6)
    toggle(S, "testee_inter", g, True)
    S.key("marqueur", "done1", at_x(690), 0, 4, "out")
    S.key("marqueur", "done0", at_x(400), 0, 4, "out")
    S.key("cadran", "value", at_x(470), 0, 5, "inOut")
    vanish(kit, "cadran_txt", at_x(560), d=6)
    vanish(kit, "cadran", at_x(440), d=6)
    g = at_x(230)
    kit.draw("badge_coche", g, 4, to=0)
    kit.draw("badge_plein", g, 4, to=0)
    kit.pop("badge_case", g + 2, d=5)
    cross(toi, f + 3, P_BACK, 11)

    f = kit.at("S19", "tu", "« Toi » revient d'un bond près du téléphone")
    hop_end = toi.hop(f, list(P_S19), 6, h=16)

    f = kit.at("S19", "cliquais", "« Toi » tape trois fois très vite sur « Connecter » : le bouton s'enfonce trois "
                                  "fois, une pastille file aussitôt des comptes au bouton ; il range son stylo")
    hits = []
    for k in range(3):
        hits.append(toi.tap(f - 1 + 4 * k, list(BOUTON_TAP_S19), d=4, lift=12))
        press(S, hits[-1], d_in=2, d_out=2)
    assert hits[0] >= hop_end - 1, (hits, hop_end)
    end = perle_route(S, "perle1", hits[-1], 10, bank_to_button(S, hits[-1]))
    vanish(kit, "perle1", end, into=list(BOUTON_C), d=5)
    toi.stow(hits[-1] + 4)

    f = kit.at("S19", "sans", "trois petits ronds puis la bulle (mini « Mon budget », clé fantôme) ressortent de la "
                              "tête de « Toi », en bas à gauche")
    head = [P_S19[0], P_S19[1] + HEAD_DY * TOI_SCALE]
    k_b = BULLE_S19_K
    corner = [BULLE_S19[0] + (BULLE_W / 2 - 18) * k_b, BULLE_S19[1] - (BULLE_H / 2 - 18) * k_b]
    for k, pt in enumerate(bulle_ronds(head, corner, head_r=35 * TOI_SCALE)):
        rid = f"bulle_rond{k + 1}"
        S.key(rid, "pos", f - 1, pt)
        kit.pop(rid, f + k, d=5)
    kit.pop("bulle", f + 3, scale=k_b, from_pt=head, to=list(BULLE_S19), d=7)

    f = kit.at("S19", "réfléchir.", "de chaque disque du repère tombe en arc une alerte numérotée : 1 sur le bord de la "
                                    "bulle, 2 sous le bout du badge en tirets, 3 sur le câble de l'appli testée ; "
                                    "chaque cible bat à l'arrivée. Tenue")
    targets = ["bulle", "badge", "testee"]
    for k in range(3):
        t, a = f + 5 * k, f"alerte{k + 1}"
        S.key(a, "pos", t - 1, [MARKER_XS[k], MARKER_Y])
        kit.pop(a, t, d=5)
        S.key(f"{a}_num", "opacity", t, 1)
        land = kit.move(a, t + 2, ALERTES_S19[k], 14, arc=60)
        kit.pulse(targets[k], land, peak=1.08 * S.val(targets[k], "scale", land - 1))
    assert land <= scene_f0(S, "S20"), land

    # ================= S20 « Maintenant, tu t’identifies chez ta banque et tu vérifies sur REGAFI. » ==========
    f = kit.at("S20", "Maintenant,", "« ◀◀ Avant » devient « Maintenant » et le cadre en tirets devient plein ; "
                                     "« Toi » ressort son stylo et repart vers la banque, derrière l'appli testée")
    kit.morph(["etiquette_avant"], ["etiquette_maint"], f)
    kit.draw("cadre_plein", f, MORPH)
    S.key("cadre_avant", "opacity", f, 0, MORPH, "linear")
    toi.unstow(f)
    cross(toi, f, P2, 25)

    f = kit.at("S20", "t’identifies", "« Toi » touche la clé dans la banque : sa coche pleine se retrace")
    hit = toi.tap(f - TAP + 1, list(CLE_HOME))
    kit.draw("cle_coche", hit, 6)
    toi.rest(hit + 6, 8)

    f = kit.at("S20", "banque", "la bulle tremble et éclate ; l'alerte 1 se change sur place en coche pleine numérotée "
                                "1 ; le disque 1 du repère se coche et bat")
    kit.shake("bulle", f)
    kit.vanish("bulle", f + 3, style="burst", n=8, spread=30)
    for k, rid in enumerate(["bulle_rond3", "bulle_rond2", "bulle_rond1"]):
        kit.vanish(rid, f + 3 + 2 * (k + 1), style="burst", n=4, spread=14, sw=3)
    resolve(S, kit, 0, f + 3)

    e = S.word_after("et", f + 1)
    cross(toi, e, P_REG, 12, hop=24)                           # « et tu » : un bond à portée de la pilule

    f = kit.at("S20", "vérifies", "une pilule « REGAFI » (le registre) tombe d'en haut dans la place libérée par la "
                                  "bulle ; « Toi » lève son stylo vers elle")
    S.key("regafi", "opacity", f - 1, 0)
    kit.drop("regafi", f, h=80, to=list(REGAFI_PILL_C))
    tap_pt = [REGAFI_PILL_C[0] + 40, REGAFI_PILL_C[1]]
    toi.reach(max(f + 2, e + 12), [tap_pt[0] + 10, tap_pt[1] - 24], 8)

    f = kit.at("S20", "REGAFI.", "« Toi » touche « REGAFI » : un fil plein monte de la pilule au badge, qui redevient "
                                 "plein et coché ; l'alerte 2 se change sur place en coche pleine numérotée 2 ; le "
                                 "disque 2 du repère se coche")
    hit = toi.tap(f - TAP + 1, tap_pt)
    x = REGAFI_PILL_C[0] - 50
    S.key("preuve", "pa", hit + 1, [x, REGAFI_PILL_C[1] - 24])
    S.key("preuve", "pb", hit + 1, [x, BADGE_UNDER_PHONE[1] + BADGE_H / 2 - 4])
    S.key("preuve", "sag", hit + 1, 0)
    S.key("preuve", "opacity", hit + 1, 1)
    arrive = kit.draw("preuve", hit + 2, 6)
    kit.pulse("badge", arrive - 1, peak=1.1)
    vanish(kit, "badge_case", arrive, d=5)
    kit.draw("badge_plein", arrive + 2, 6)
    kit.draw("badge_coche", arrive + 2, 6)
    resolve(S, kit, 1, arrive + 2)
    toi.rest(hit + 6, 8)

    # ================= S21 « Et tous les 6 mois, tu fais le tri. » =================
    f = kit.at("S21", "Et", "la pilule « REGAFI » et le fil de preuve se rangent ; « Toi » repart vers l'appli testée, "
                            "derrière elle")
    vanish(kit, "regafi", f)
    kit.draw("preuve", f, 6, to=0)
    cross(toi, f + 2, P2, 24)

    f = kit.at("S21", "6", "le cadran ressurgit, une flèche de boucle en fait le tour complet pendant qu'il se remplit "
                           "jusqu'à 6, se vide et se remplit de nouveau ; « tous les 6 mois » s'écrit à la pointe de "
                           "la flèche : une habitude qui revient")
    S.key("cadran", "pos", f - 1, list(CADRAN_S21))
    S.key("cadran", "value", f - 1, 0)
    kit.pop("cadran", f, d=6, scale=0.84)                   # dans la boucle (r 80)
    S.key("cadran", "value", f + 3, 6, 6, "inOut")
    S.key("cadran", "value", f + 9, 0)
    S.key("cadran", "value", f + 10, 6, 6, "inOut")
    kit.draw("cadran_boucle", f + 2, 14, e="linear")
    kit.pop("cadran_pointe", f + 15, d=4)
    kit.type("cadran_routine", f + 16, rate=3)

    f = kit.at("S21", "tri.", "« Toi » met l'interrupteur de l'appli testée sur OFF : son câble rentre dans la porte ; "
                              "l'alerte 3 se change sur place en coche pleine numérotée 3 ; le disque 3 se coche ; "
                              "« Toi » range son stylo. Tenue : trois coches, jusqu'à la carte de fin")
    hit = toi.tap(f - TAP + 1, list(TESTEE_SWITCH))
    toggle(S, "testee_inter", hit, False)
    kit.draw("cable_testee", hit + 2, 10, to=0)
    back = resolve(S, kit, 2, hit, d=5)
    # contrôle sans son : « le pas 3 jamais coché ». Le disque actif se réduit en disque simple (on -> 0) et une
    # pastille cochée s'y pose : les trois étapes sont faites, une coche dans chaque disque
    S.key("marqueur", "on", hit + 1, 0, 4, "out")
    kit.pop("marqueur_fait3", hit + 1, d=5)
    kit.draw("marqueur_fait3_coche", hit + 2, 5)
    toi.rest(hit + 2, 5)
    end = toi.stow(hit + 3)
    # tour sans son 1 : « la 3e coche arrive juste avant la coupe » -> tout est posé vers « tri. » + 10 et tenu
    # jusqu'à la carte de fin (S22 « comprendre »)
    hold_from = max(back, end, hit + 7)

    # ================= S22 « Abonne-toi pour comprendre ton argent. » =================
    outs = ["appli", "interrupteur", "porte", "porte_dsp2", "porte_ue", "banque", "cle", "cle_coche", "badge",
            "testee", "cadran", "cadran_boucle", "cadran_pointe", "cadran_routine", "etiquette_maint", "marqueur",
            "cadre_plein", "cable", "marqueur_fait3", "coupe_coche1", "coupe_coche2",
            "alerte1_ok", "alerte2_ok", "alerte3_ok"]
    kit.hold("S22", "Abonne-toi", "tenue : les trois coches numérotées et le repère coché restent à l'écran")
    out = kit.outro("S22", mot="comprendre", outs=outs, press="argent.", clear="fade")
    f = out["card"]
    assert f - hold_from >= 38, (hold_from, f)            # + 6 images de fondu : environ 1,5 s lisible
    S.set("bouton_txt", text=S.ents["bouton_txt"]["p"]["text"])
    S.key("bouton_txt", "text", f, "S’abonner")                 # avec le premier pas du bouton, jamais avant
    toi.exit(f)
    S.key("toi", "opacity", f, 0, 4, "linear")                  # aucun point résiduel pendant la réduction
    for id, z in (("bouton", 41), ("bouton_ombre", 40.9), ("bouton_txt", 41.1)):   # au-dessus de la carte (z 40)
        kit.ensure(id, "z", S.ents[id]["z"])
        S.key(id, "z", f, z)
    kit.move("bouton", f, FIN_BUTTON, 8, e="out", scale=CARD_BTN_SCALE)
    w, h = round(380 / CARD_BTN_SCALE, 2), round(112 / CARD_BTN_SCALE, 2)
    for id in ("bouton", "bouton_ombre"):
        for tr, v in (("w", w), ("h", h), ("r", h / 2)):
            kit.ensure(id, tr, S.ents[id]["p"][tr])
            S.key(id, tr, f, v, MORPH, "inOut")
    sh = round(8 / CARD_BTN_SCALE, 2)
    S.key("bouton_ombre", "pos", f, [sh, sh], MORPH, "inOut")
    relay = f + 6 + POP                                         # le bouton de la carte est entier dessous
    S.key("bouton", "opacity", relay, 0)

    # pas de pointeur de souris (film vu au téléphone) : un toucher au doigt sur le bas droit du bouton
    S.set(out["cursor"], opacity=0)
    fp = out["press"]
    kit.pop("fin_doigt", fp - 5, d=4)
    S.key("fin_doigt", "scale", fp, 0.8, 2, "out")
    kit.vanish("fin_doigt", fp + 5, d=5)
    for k in range(2):
        ring(S, f"fin_onde{k + 1}", fp + 4 * k, d=14, s0=0.6, s1=2.1)
    film_end = round(S.sb["scenes"][-1]["t_end"] * S.fps)
    assert out["press"] + 9 < film_end, (out, film_end)
