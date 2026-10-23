"""V02, partie 1 : S01-S07, images 0-922. Le clic, le câble, le « ? » qui devient le repère 1-2-3, « open banking »,
la directive DSP2 qui devient la porte (et sa barrière), l'interrupteur « Accès », le mur fermé et son cadenas, la clé
qui ouvre les comptes.

État d'entrée : l'image 0 de la distribution (cast), etat_initial de S01 : téléphone « Mon budget » et bouton cyan ;
« Toi » en P1, stylo levé ; moitié droite vide.

Temps forts (image du film) :
S01  cliqué=9  « Connecter=32  banque »=49            (+ « appli » 74 : le bouton bat, vie secondaire)
S02  ce=109  autorisé ?=124                           (+ « vidéo » 166 : le « ? » oscille jusqu'à « trois »)
S03  trois=203  connectes=254  réflexe=310
S04  bouton,=359  l’open=385  banking.=394
S05  directive=434  DSP2,=470  ouvrir=520  comptes=559  autorisés.=594   (+ « banque » 506 : la banque bat)
S06  seulement=636  accord.=660  pirate=698  passe=734
S07  Pourquoi=792  identifiants ?=831  clés=886  compte.=902

Sens des données : TOUJOURS des comptes de la banque vers le téléphone (aucune pastille ne part du bouton). Chaque
pastille qui arrive allume ou fait battre une ligne de relevé de l'écran : l'appli reçoit des données, rien d'autre.
Seule exception : S06 « pirate », une pastille d'intrusion part du téléphone, passe par-dessus la porte et rebondit sur
le mur de la banque (le cadenas se pose au point du choc) : mur fermé, porte ouverte.

Raccord vers p2 : à l'image 922, l'état est exactement ENTRY_P2 ; « Toi » arrêté en P2, stylo au repos.
"""
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP  # noqa: F401
from pipeline.story_kit import TAP

from . import (ALERTE_R, ALERTES_CABLE, BANK_C, BARRIERE_C, BARRIERE_W, BOUTON_C, BOUTON_TAP, CABLE_A, CABLE_B,
               CADENAS_C, CARTE_ID_C, CLE_HOME, COMPTES_DY, COMPTES_KEY, COMPTES_MID, DIRECTIVE_C, DIRECTIVE_CROWN,
               DIRECTIVE_DSP2, MARKER_XS, MARKER_Y, MUR_C, OPEN_BANKING_C, P2, PHONE_C, PORTE_C, PORTE_UE_C,
               PORTE_VIA, QUESTION_C, QUESTION_LINK, RELEVE_DY, SWITCH_C, HEAD_DY, TOI_SCALE, along, bulle_ronds, cable_route,
               perle_route, press, ring, scene_f0, t_at_x, toggle, vanish)
from pipeline.story import text_width

ALERT_HIGH_Y = 700               # S03 : les alertes naissent à la hauteur du « ? » puis tombent sur le câble
PERLE_STOP_X = BARRIERE_C[0] + BARRIERE_W / 2 + 16 + 24     # S05 : la pastille attend à 24 px de la barrière
PERLE_HIT_X = BARRIERE_C[0] + BARRIERE_W / 2 + 16 - 3       # S06 : contact (écrasée contre la barrière)
OVER_HEAD = (352, 972)           # S02 : le « ? » passe au-dessus de la tête de « Toi »
CADENAS_INTO = (742, 792)
PIRATE_ROUTE = [(356, 700), (440, 652), (515, 638), (600, 660), (MUR_C[0] - 18, CADENAS_C[1])]   # S06 : par-dessus la porte


def releve_pt(k):
    """Ligne de relevé k de l'écran du téléphone (monde)."""
    return [PHONE_C[0], PHONE_C[1] + RELEVE_DY[k]]


def bank_to_button(S, f, wid="cable"):
    """Trajet monde d'une pastille : barre de comptes -> bord de la banque -> câble (porte comprise) -> bouton."""
    return [list(COMPTES_MID), list(CABLE_B)] + cable_route(S, f)[1:] + [list(BOUTON_C)]


def part(S, kit, c):
    toi = c.toi
    kit.pin(0 - 1, {"bouton": {"pos": list(BOUTON_C), "scale": 1}, "banque": {"scale": 0},
                    "cable": {"draw": 0}, "marqueur": {"scale": 0, "on": 0}, "interrupteur": {"scale": 0}})

    # ================= S01 : le clic tire le câble vers la banque =================
    f = kit.at("S01", "cliqué", "le stylo de « Toi » touche le bouton « Connecter ma banque » : il s'enfonce")
    hit = toi.tap(f - TAP + 1, BOUTON_TAP)
    press(S, hit)
    toi.rest(hit + 7)

    f = kit.at("S01", "« Connecter", "un câble cyan profond se trace du bord droit du téléphone vers la droite")
    kit.draw("cable", f, DRAW)

    f = kit.at("S01", "banque »", "la banque surgit au bout du câble, qui s'accroche à son bord gauche")
    kit.pop("banque", f)
    kit.pulse("bouton", S.word_after("appli", f), peak=1.06)          # vie secondaire sur « appli »

    # ================= S02 : des données COPIÉES glissent ; un « ? » sort du bouton =================
    f = kit.at("S02", "ce", "une copie en tirets se détache de chaque barre de comptes (qui bat, pleine) et devient "
                            "une pastille qui glisse jusqu'au téléphone : deux lignes de relevé s'allument à l'écran")
    for k in range(2):
        g = f + 7 * k
        cid, cop = f"compte{k + 1}", f"compte{k + 1}_copie"
        S.key(cop, "scale", g, 1)
        S.key(cop, "opacity", g, 1)
        kit.pulse(cid, g, peak=1.06)
        S.key(cop, "pos", g, [CABLE_B[0] - BANK_C[0] + 10, CABLE_B[1] - BANK_C[1]], 6, "in")
        S.key(cop, "scale", g, 0.15, 6, "in")
        S.key(cop, "opacity", g + 6, 0)
        route = [list(CABLE_B)] + cable_route(S, g + 6)[1:]
        end = perle_route(S, f"perle{k + 1}", g + 6, 13, route)
        vanish(kit, f"perle{k + 1}", end, into=releve_pt(k), d=6)
        kit.pop(f"releve{k + 1}", end + 2, d=7)

    f = kit.at("S02", "autorisé ?", "un grand « ? » jaillit du bouton cliqué et se pose juste au-dessus du câble, "
                                    "relié au bouton par un trait court en tirets ; « Toi » se penche vers lui")
    # tour sans son 1 : « le ? paraît venir de l'utilisateur » -> il sort DU BOUTON et y reste relié (plus de ronds
    # de pensée depuis la tête de « Toi »)
    kit.pop("question", f, from_pt=BOUTON_C, to=list(QUESTION_C), d=11)
    S.key("question", "scale", f + 11, 1.12, 4, "out")
    S.key("question", "scale", f + 15, 1.0, 5, "inOut")
    S.key("question_lien", "pa", f - 1, list(QUESTION_LINK[0]))
    S.key("question_lien", "pb", f - 1, list(QUESTION_LINK[1]))
    kit.draw("question_lien", f + 6, 6)
    kit.pulse("bouton", f + 1, peak=1.05)
    toi.lean_to(f + 2, 6)
    g = S.word_after("vidéo,", f)                                    # vie secondaire : le « ? » oscille
    for k, dy in enumerate((-7, 7, -7, 0)):
        S.key("question", "pos", g + 9 * k, [QUESTION_C[0], QUESTION_C[1] + dy], 9, "inOutSine")

    # ================= S03 : trois alertes sur le câble, puis le repère 1-2-3 =================
    f = kit.at("S03", "trois", "le « ? » éclate en trois alertes qui tombent sur le câble, une à une : 1, 2, 3")
    vanish(kit, "question", f)
    kit.draw("question_lien", f, 5, to=0, e="in")
    toi.lean_to(f, 0)
    for k in range(3):
        a = f"alerte{k + 1}"
        x, y = ALERTES_CABLE[k]
        kit.pop(a, f, from_pt=list(QUESTION_C), to=[x, ALERT_HIGH_Y])
        kit.drop(a, f + POP + 4 * k, h=y - ALERT_HIGH_Y, to=[x, y])

    f = kit.at("S03", "connectes", "une pastille sort des comptes, parcourt le câble sous les alertes et arrive au "
                                   "bouton ; les lignes de relevé battent")
    end = perle_route(S, "perle1", f, 20, bank_to_button(S, f))
    vanish(kit, "perle1", end, into=list(BOUTON_C), d=6)
    kit.pulse("releve1", end, peak=1.08)
    kit.pulse("releve2", end + 2, peak=1.08)

    f = kit.at("S03", "réflexe", "le repère 1-2-3 légendé (Codes, Société, Accès) surgit ; chaque alerte s'envole, "
                                 "l'une après l'autre, jusqu'à SON disque, qui s'entoure d'un anneau à l'impact")
    # tour sans son 1 : « les triangles disparaissent sans cause visible » -> le repère est là AVANT, chaque alerte
    # vole vers sa case numérotée et la case « bat » à l'impact
    kit.pop("marqueur", f)
    k_disc = 20 / ALERTE_R
    for k in range(3):
        a = f"alerte{k + 1}"
        g = kit.move(a, f + 3 + 7 * k, [MARKER_XS[k], MARKER_Y], arc=90, scale=k_disc)
        vanish(kit, a, g - 2, d=5)
        S.key(f"marqueur_ping{k + 1}", "pos", g - 3, [MARKER_XS[k], MARKER_Y])
        ring(S, f"marqueur_ping{k + 1}", g - 2, d=10, s0=0.6, s1=1.3)
    assert g + 8 <= 352 + 1, g

    # ================= S04 : le bouton, c'est l'open banking =================
    f = kit.at("S04", "bouton,", "« Toi » touche à nouveau le bouton : il s'enfonce")
    hit = toi.tap(f - TAP + 1, BOUTON_TAP)
    press(S, hit)
    toi.rest(hit + 7)

    f = kit.at("S04", "l’open", "l'étiquette « open banking » naît du bouton et monte au-dessus du câble")
    g = kit.pop("open_banking", f, from_pt=BOUTON_C, to=list(BOUTON_C))
    kit.move("open_banking", g, list(OPEN_BANKING_C), arc=60)

    f = kit.at("S04", "banking.", "une pastille sort des comptes, parcourt tout le câble sous l'étiquette et arrive "
                                  "au bouton")
    end = perle_route(S, "perle2", f, 20, bank_to_button(S, f))
    vanish(kit, "perle2", end, into=list(BOUTON_C), d=6)
    kit.pulse("releve2", end, peak=1.08)

    # ================= S05 : la directive DSP2 devient la porte ; l'interrupteur « Accès » sur OFF =================
    f = kit.at("S05", "directive", "« open banking » s'efface en fondu ; la directive européenne (couronne "
                                   "d'étoiles) surgit au-dessus du câble, sous le repère")
    S.key("open_banking", "opacity", f, 0, FADE, "linear")
    S.key("open_banking", "scale", f + FADE, 0)
    kit.pop("directive", f, from_pt=[DIRECTIVE_C[0], DIRECTIVE_C[1] + 50], to=list(DIRECTIVE_C))

    f = kit.at("S05", "DSP2,", "« DSP2 » se souligne d'un trait épais cyan profond et bat ; la carte bat ensuite")
    w = text_width("DSP2", 46, 800)
    S.key("directive_trait", "w", f, w, 6, "out")
    S.key("directive_trait", "pos", f, [DIRECTIVE_DSP2[0], DIRECTIVE_DSP2[1] + 30], 6, "out")
    kit.pulse("directive_dsp2", f, peak=1.18)
    kit.pulse("directive", f + 6, peak=1.05)
    kit.pulse("banque", S.word_after("banque", f), peak=1.04)          # « ta banque doit ouvrir »

    f = kit.at("S05", "ouvrir", "la directive descend sur le câble et se change en porte « DSP2 » (barrière "
                                "fermée) ; sa couronne d'étoiles reste sur l'arche ; le câble passe par son tourniquet")
    kit.move("directive", f, list(PORTE_C), d=10)
    crown = S.to_world("directive", list(DIRECTIVE_CROWN), f + 7)
    g = kit.morph(["directive"], ["porte"], f + 7)
    S.key("cable", "via", f + 7, list(PORTE_VIA), MORPH, "inOut")
    kit.pop("porte_ue", f + 7, from_pt=crown, to=list(PORTE_UE_C), d=MORPH)
    kit.pop("porte_dsp2", f + 10)
    kit.pop("barriere", g)

    f = kit.at("S05", "comptes", "les comptes battent ; une pastille en sort et s'arrête contre la barrière de la "
                                 "porte")
    kit.pulse("compte1", f, peak=1.1)
    kit.pulse("compte2", f, peak=1.1)
    route = [list(COMPTES_MID), list(CABLE_B), [PERLE_STOP_X, 862]]
    perle_route(S, "perle3", f, 12, route)
    S.key("perle3", "scale", f + 4, 1.08, 4, "out")                   # 34 px : elle attend, bien visible

    f = kit.at("S05", "autorisés.", "l'interrupteur « Accès » sort de dessous le bouton, sur OFF ; la pastille bute "
                                    "deux fois contre la barrière pendant que l'interrupteur OFF bat")
    kit.pop("interrupteur", f, from_pt=BOUTON_C)
    for k in range(2):
        g = f + 6 + 7 * k
        S.key("perle3", "pos", g, [PERLE_HIT_X, 862], 2, "out")
        S.key("perle3", "pos", g + 2, [PERLE_STOP_X, 862], 4, "out")
        kit.shake("barriere", g + 2, amp=5)
    kit.pulse("interrupteur", f + 8, peak=1.15, times=2)

    # ================= S06 : sans accord rien ne passe ; le mur fermé ; la porte officielle =================
    f = kit.at("S06", "seulement", "la pastille fonce sur la barrière et s'y écrase : la barrière tremble, la porte "
                                   "bascule, l'interrupteur OFF bat fort dans un anneau cyan profond ; elle recule")
    S.key("perle3", "pos", f, [PERLE_HIT_X, 862], 2, "out")
    S.key("perle3", "sx", f + 1, 0.72, 2, "out")                       # écrasée au contact (3 images)
    S.key("perle3", "sx", f + 4, 1, 3, "out")
    S.key("perle3", "pos", f + 4, [PERLE_STOP_X + 12, 862], 6, "out")
    S.key("perle3", "pos", f + 10, [PERLE_STOP_X, 862], 5, "inOut")
    kit.shake("barriere", f + 1, amp=9)
    S.key("porte", "rot", f + 2, 4, 2, "out")
    S.key("porte", "rot", f + 6, 0, 4, "inOut")
    kit.pulse("interrupteur", f + 3, peak=1.3, step=4)
    ring(S, "inter_anneau", f + 3, d=10)

    f = kit.at("S06", "accord.", "« Toi » met l'interrupteur « Accès » sur ON : la barrière se lève, la pastille "
                                 "franchit la porte et une troisième ligne de relevé s'allume")
    hit = toi.tap(f - TAP + 1, list(SWITCH_C))
    toggle(S, "interrupteur", hit, True)
    S.key("barriere", "pos", hit + 1, [BARRIERE_C[0], BARRIERE_C[1] - 70], 6, "in")
    vanish(kit, "barriere", hit + 3, d=5)
    t0 = t_at_x(S, "cable", PERLE_STOP_X, hit + 2)
    end = along(S, "perle3", "cable", hit + 2, 14, t0, 0)
    vanish(kit, "perle3", end, into=releve_pt(2), d=6)
    kit.pop("releve3", end + 2, d=7)
    toi.rest(hit + 7)

    f = kit.at("S06", "pirate", "une pastille venue du téléphone passe par-dessus la porte et fonce sur le mur de la "
                                "banque : elle rebondit sur un trait épais ; un cadenas se pose au point du choc")
    hit = perle_route(S, "perle2", f, 9, [list(q) for q in PIRATE_ROUTE])
    kit.pop("mur", hit - 1, d=4)
    kit.pop("cadenas", hit, from_pt=list(CADENAS_C), d=6)
    kit.shake("mur", hit + 1, amp=4)
    S.key("perle2", "pos", hit, [PIRATE_ROUTE[-1][0] - 50, PIRATE_ROUTE[-1][1] - 26], 6, "out")
    vanish(kit, "perle2", hit + 6, d=6)

    f = kit.at("S06", "passe", "le cadenas reste fermé ; une pastille sort des comptes et passe par la porte ouverte, "
                               "qui bat à son passage ; elle arrive au bouton. Tenue")
    kit.pulse("cadenas", f, peak=1.15)
    route = bank_to_button(S, f)
    end = perle_route(S, "perle1", f + 3, 24, route)
    beat_gate = f + 3 + 10
    kit.pulse("porte", beat_gate, peak=1.06)
    kit.pulse("porte_dsp2", beat_gate, peak=1.08)
    vanish(kit, "perle1", end, into=list(BOUTON_C), d=6)
    kit.pulse("releve3", end, peak=1.08)

    # ================= S07 : les identifiants deviennent la clé des comptes =================
    f = kit.at("S07", "Pourquoi", "le cadenas et le trait du mur rentrent dans la banque ; « Toi » va se placer sous "
                                  "la banque")
    vanish(kit, "cadenas", f, into=list(CADENAS_INTO))
    vanish(kit, "mur", f, into=list(CADENAS_INTO))
    toi.walk(f, list(P2), 36)

    f = kit.at("S07", "identifiants ?", "une carte « Identifiant •••••• » sort de la pointe du stylo de « Toi »")
    kit.pop("carte_id", f, from_pt=toi.tip(f - 1), to=list(CARTE_ID_C))
    kit.pulse("carte_id", S.word_after("Parce", f), peak=1.06)        # vie secondaire pendant « Parce que ce sont »

    f = kit.at("S07", "clés", "la carte d'identifiants se change en clé (capsule de verre, clé cyan profond)")
    kit.morph(["carte_id"], ["cle"], f)

    f = kit.at("S07", "compte.", "la clé s'éloigne du téléphone en arc par la droite, entre dans la banque, se dresse "
                                 "dans les comptes et tourne : les deux barres s'écartent nettement (déverrouillées) ; "
                                 "puis elle se range sous le câble, dans la banque")
    p0 = S.val("cle", "pos", f - 1)
    ctrl = (960, 1010)
    S.path("cle", f, 9, "inOut", lambda t: [round((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * ctrl[0] + t * t * COMPTES_KEY[0], 2),
                                            round((1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * ctrl[1] + t * t * COMPTES_KEY[1], 2)])
    S.key("cle", "scale", f, 0.9, 9, "inOut")
    S.key("cle", "rot", f + 3, 90, 6, "out")
    for k, dy in enumerate((-16, 16)):
        S.key(f"compte{k + 1}", "pos", f + 8, [0, COMPTES_DY[k] + dy], 3, "out")
        S.key(f"compte{k + 1}", "pos", f + 17, [0, COMPTES_DY[k]], 6, "inOut")
    ring(S, "cle_anneau", f + 9, d=6)
    S.key("cle_anneau", "pos", f + 8, list(COMPTES_KEY))
    S.key("cle", "pos", f + 11, list(CLE_HOME), 9, "inOut")
    S.key("cle", "rot", f + 11, 0, 9, "inOut")
    S.key("cle", "scale", f + 11, 1, 9, "inOut")
    S.key("cle_anneau", "pos", f + 20, list(CLE_HOME))
    assert f + 11 + 9 - 1 <= scene_f0(S, "S08") - 2, "S07 : la clé doit être rangée avant S08"
