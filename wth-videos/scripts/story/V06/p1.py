"""V06, partie 1 : S01-S06, images 0-745 (accroche, annonce, contexte). 22 temps forts, 24,9 s.

ÉTAT D'ENTRÉE (image 0 = distribution) : ivoire quadrillé ; à droite l'appartement `maison` (TOKEN.png 220 px,
centre 700, 880) et dessus la pilule `pastille` « 200 000 € » (700, 705) ; à gauche la `caisse` « Disponible »
(170, 880) et ses trois places en tirets, vides ; « Toi » (`toi`, bras droit) en P1 (420, 1135), bras baissé,
nommé par `toi_nom` « Toi ». Rien ne bouge.

Temps forts (image du mot) :
S01  200 000 €@24  patrimoine…@55
S02  payer@119  facture@132  3 000 €.@151
S03  pourquoi,@239  combien@290  récupères@317  argent.@339
S04  Tout@364  liquidité.@405
S05  facilité@448  actif@498  argent@520  disponible,@530  vite,@557  perdre@591  valeur.@605
S06  Un@629  livret@635  appartement,@689  beaucoup@716

Tour 1 de revue :
- « Toi » garde le bras baissé entre deux gestes (lower) ; il ne lève le stylo que pour un geste.
- S02-S03 : la tenue de 2,9 s (images 153-238) est animée sans nouveau sens : « Toi » regarde la facture
  (« Dans »), l'appartement (« vidéo », la pilule bat à x1,05), puis devant lui (« voir »).
- « Toi » (étiquette) s'efface sur « pourquoi, » : la figurine est établie, « liquidité » ne s'y colle plus.
- Le livret tombe en (372, 880) : la flèche du rail (282-318) reste visible ; « Livret » surgit avec lui (« actif ») ;
  S06 « livret » ne fait plus que battre (livret, nom, horloge).
- S05 « vite, » : l'horloge bat (x1,15) en prenant sa tranche (5/60).
- Paiement (S05, même recette en S21) : les pièces montent des places DANS la facture, sous le montant (sans le
  traverser) ; le montant passe au deep à leur arrivée, la coche (r 32) surgit à x1,3 puis revient à x1.
- S06 « beaucoup » : l'appartement prend de l'élan (recule de 30 px), fonce, bute ; le cadenas tremble fort (amp 10).
"""
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401

from . import *  # noqa: F401,F403
from . import (CAISSE_C, CAISSE_EDGE_TAP, CADENAS_C, COINS, DEEP, DROP_FROM_Y, FACTURE_C, FACTURE_COINS_LOCAL,
               FACTURE_DROP_FROM_Y, FACTURE_OUT, HORLOGE_C, LIVRET_C, MAISON_BUMP_C, MAISON_C, MAISON_TAP, P1,
               PASTILLE_C, PIECE_TIRETS_STOP, PLACES, CAISSE_PLACES, CAISSE_PLACES_LOCAL, RAIL_A, RED, TIP_S03,
               PAY_K, assert_reach, hold_low, lower, scene_f0, turn)

FAN_S05 = [(310, 708), (358, 694), (406, 708)]  # S05 : éventail au-dessus de « Livret » (788-822), entre la facture et l'horloge
Q_BORN = (TIP_S03[0], TIP_S03[1] - 55)          # S03 : le « ? » naît juste au-dessus de la pointe
EXIT_DX = FACTURE_OUT[0] - FACTURE_C[0]         # S06 : -390, la facture et ses pièces sortent ensemble


def pay_points():
    return [[FACTURE_C[0] + x, FACTURE_C[1] + y] for x, y in FACTURE_COINS_LOCAL]


def part(S, kit, c):
    toi, toi_g = c.toi, c.toi_g
    coins = COINS["s05"]

    # ---------- état d'entrée (image 0 = distribution) : épinglé à -1 ----------
    kit.pin(0 - 1, {
        "maison": {"pos": list(MAISON_C), "scale": 1},
        "pastille": {"pos": list(PASTILLE_C), "scale": 1, "rot": 0},
        "caisse": {"pos": list(CAISSE_C), "scale": 1},
        **{p: {"pos": list(q), "scale": 1} for p, q in zip(PLACES, CAISSE_PLACES_LOCAL)},
        "facture": {"pos": list(FACTURE_C), "scale": 0},
        "horloge": {"pos": list(HORLOGE_C), "scale": 0, "value": 0, "rot": 0},
        "toi_nom": {"opacity": 1},
    })
    if S.val(toi.id, "scale", -1) == 0:          # partie construite seule après une sortie : sans effet ici
        toi.enter(0, at=list(P1))
    assert_reach(P1[0], MAISON_TAP, "S01 appartement", "right")
    assert_reach(P1[0], CAISSE_EDGE_TAP, "S02 bord de la caisse", "left")
    assert_reach(P1[0], TIP_S03, "S03 stylo levé", "left")

    def turn_to(a, b, f):
        return turn(S, a, b, f)

    # ================= S01 : « Tu peux avoir 200 000 € de patrimoine… » =================
    f = kit.at("S01", "200 000 €", "la pilule « 200 000 € » posée sur l'appartement bat une fois (x1,15) ; "
                                    "rien d'autre ne bouge")
    kit.pulse("pastille", f, peak=1.15)

    f = kit.at("S01", "patrimoine…", "« Toi » lève le stylo et en pose la pointe sur le bas gauche de l'appartement ; "
                                      "au contact, l'appartement et la pilule battent ensemble (x1,08)")
    hit = toi.tap(f - TAP + 1, MAISON_TAP)
    toi.reach(hit + 1, MAISON_TAP, d=5)          # le stylo reste posé (annule la relève du tapotement)
    kit.pulse("maison", hit, peak=1.08)
    kit.pulse("pastille", hit, peak=1.08)

    # ================= S02 : « et ne pas pouvoir payer une facture de 3 000 €. » =================
    f02 = scene_f0(S, "S02")
    g = lower(toi, f02 + 1, 8)                   # « Toi » lâche l'appartement, bras baissé...
    g = turn_to(toi, toi_g, g)                   # ... et se tourne vers la caisse (bras gauche)

    f = kit.at("S02", "payer", "« Toi » touche du stylo le bord droit de la caisse ; ses trois places en tirets "
                                "tremblent, vides")
    hit = toi_g.tap(f - TAP + 1, CAISSE_EDGE_TAP)
    for k, p in enumerate(PLACES):
        kit.shake(p, hit + k, amp=6)
    lower(toi_g, hit + 6, 8)

    f = kit.at("S02", "facture", "une facture « 3 000 € » (montant encre) tombe du haut sur la caisse vide")
    kit.drop("facture", f, h=FACTURE_C[1] - FACTURE_DROP_FROM_Y)

    f = kit.at("S02", "3 000 €.", "le montant « 3 000 € » vire au rouge et la facture tremble ; la pilule "
                                   "« 200 000 € » ne bouge pas")
    S.key("facture_montant", "color", f, RED, 3)
    kit.shake("facture", f, amp=8)

    # --- tenue animée (S02 -> S03, « Dans cette vidéo, on va voir ») : « Toi » regarde, rien de nouveau ---
    kit.ensure("toi_g", "look", 0)
    fa = S.word_after("Dans", f)
    S.key("toi_g", "look", fa, -0.9, POP, "out")                 # vers la facture rouge
    fb = S.word_after("vidéo", fa)
    S.key("toi_g", "look", fb, 0.9, MOVE, "inOut")               # vers l'appartement
    kit.pulse("pastille", fb + 4, peak=1.05)
    fc = S.word_after("voir", fb)
    S.key("toi_g", "look", fc, 0, POP, "inOut")                  # devant lui, vers le vide entre les deux

    # ================= S03 : « … pourquoi, et … en combien de temps tu récupères ton argent. » =================
    f = kit.at("S03", "pourquoi,", "« Toi » lève le stylo entre la caisse et l'appartement ; un grand « ? » naît "
                                    "au-dessus de la pointe et monte au-dessus du rail à venir ; l'étiquette « Toi » "
                                    "s'efface")
    kit.fade("toi_nom", f, to=0)
    g = toi_g.reach(f, TIP_S03, d=POP)
    g = kit.pop("question_toi", g - 1, from_pt=TIP_S03, to=Q_BORN)
    kit.move("question_toi", g, HORLOGE_C, d=MOVE)

    f = kit.at("S03", "combien", "le « ? » se change en horloge (cadran vide, aiguille sur midi) ; « Toi » baisse "
                                  "le bras")
    kit.morph("question_toi", "horloge", f)
    lower(toi_g, f, 8)

    f = kit.at("S03", "récupères", "un rail deep se trace de l'appartement à la caisse, sous l'horloge ; une "
                                    "flèche surgit à son bout, pointée sur la caisse")
    g = kit.draw("rail", f, DRAW)
    kit.pop("rail_fleche", g)

    f = kit.at("S03", "argent.", "une pièce en tirets sort de l'appartement et glisse sur le rail jusque sous "
                                  "l'horloge ; l'aiguille fait un tour, le secteur reste vide")
    kit.pop("piece_tirets", f, from_pt=RAIL_A)
    g = kit.move("piece_tirets", f + 4, PIECE_TIRETS_STOP, d=MOVE)
    S.key("horloge", "rot", f + 4, 360, MOVE, "inOut")
    S.key("horloge", "rot", g, 0)                # remise à 0 d'un coup : même dessin

    # ================= S04 : « Tout tient en un mot : la liquidité. » =================
    f = kit.at("S04", "Tout", "le rail bat (il s'épaissit et revient) et la pièce en tirets rentre dans "
                               "l'appartement")
    kit.pulse("rail_halo", f, peak=1, step=4, track="opacity")
    kit.vanish("piece_tirets", f, into="maison")

    f = kit.at("S04", "liquidité.", "« liquidité » s'écrit lettre à lettre sous le rail (deep)")
    kit.type("liquidite", f, rate=1)

    # ================= S05 : « C'est la facilité à transformer un actif en argent disponible, vite, ... » =========
    f = kit.at("S05", "facilité", "un surligneur light passe sous « liquidité », de gauche à droite")
    kit.draw("liquidite", f, DRAW, track="mark")

    f = kit.at("S05", "actif", "un livret (disque light, pictogramme banque) tombe sur le rail tout près de la "
                                "caisse, la flèche du rail reste visible ; « Livret » surgit au-dessus de lui")
    g = kit.drop("livret", f, h=LIVRET_C[1] - DROP_FROM_Y)
    kit.pop("nom_livret", g - 3)

    f = kit.at("S05", "argent", "trois pièces sortent du livret et se posent en éventail au-dessus de lui")
    for k, (cid, pt) in enumerate(zip(coins, FAN_S05)):
        kit.pop(cid, f + 2 * k, from_pt="livret", to=pt)

    f = kit.at("S05", "disponible,", "les trois pièces filent dans les trois places de la caisse")
    for k, (cid, pt) in enumerate(zip(coins, CAISSE_PLACES)):
        kit.move(cid, f + 2 * k, pt, d=MOVE)

    f = kit.at("S05", "vite,", "l'horloge bat (x1,15) et ne prend qu'une fine tranche (5 sur 60) : c'est rapide")
    S.key("horloge", "value", f, 5, 6)
    kit.pulse("horloge", f, peak=1.15)

    f = kit.at("S05", "perdre", "les trois pièces de la caisse battent l'une après l'autre et « 3/3 » s'écrit sous "
                                 "la caisse : rien de perdu")
    for k, cid in enumerate(coins):
        kit.pulse(cid, f + 4 * k, peak=1.2)
    kit.type("compte", f)

    f = kit.at("S05", "valeur.", "les trois pièces montent des places DANS la facture, sous le montant ; à leur "
                                  "arrivée « 3 000 € » passe du rouge au deep et une grande coche surgit : payée")
    arrive = pay(S, kit, coins, f)

    # ================= S06 : « Un livret est très liquide. Un appartement, beaucoup moins. » =================
    f = kit.at("S06", "Un", "la facture payée, sa coche et ses trois pièces glissent ensemble hors de l'image par "
                             "la gauche ; « 3/3 » se réduit ; la caisse reste vide")
    out = 12
    kit.move("facture", f, FACTURE_OUT, d=out, e="in")
    for cid, pt in zip(coins, pay_points()):
        kit.move(cid, f, [pt[0] + EXIT_DX, pt[1]], d=out, e="in")
    for i in ("facture", *coins):
        S.key(i, "scale", f + out, 0)
    kit.vanish("compte", f)
    assert arrive < f

    f = kit.at("S06", "livret", "le livret bat deux fois, son nom et la fine tranche de l'horloge avec lui")
    kit.pulse("livret", f, times=2, peak=1.15)
    kit.pulse("nom_livret", f, times=2, peak=1.12)
    kit.pulse("horloge", f, times=2, peak=1.1)

    f = kit.at("S06", "appartement,", "un cadenas tombe sur le rail entre le livret et l'appartement ; « Toi » se "
                                       "retourne vers l'appartement")
    g = kit.drop("cadenas", f, h=CADENAS_C[1] - DROP_FROM_Y)
    turn_to(toi_g, toi, g)

    f = kit.at("S06", "beaucoup", "l'appartement (et sa pilule) recule pour prendre de l'élan, fonce vers la caisse, "
                                   "bute contre le cadenas qui tremble fort, et revient à sa place")
    back = 30
    g = kit.move("maison", f, [MAISON_C[0] + back, MAISON_C[1]], d=5, e="out")
    kit.move("pastille", f, [PASTILLE_C[0] + back, PASTILLE_C[1]], d=5, e="out")
    bump_dx = MAISON_BUMP_C[0] - MAISON_C[0]
    h = kit.move("maison", g, list(MAISON_BUMP_C), d=7, e="in")
    kit.move("pastille", g, [PASTILLE_C[0] + bump_dx, PASTILLE_C[1]], d=7, e="in")
    kit.shake("cadenas", h, amp=10)
    kit.move("maison", h, list(MAISON_C), d=9, e="out")
    kit.move("pastille", h, list(PASTILLE_C), d=9, e="out")


def pay(S, kit, coins, f, jump=12, arc=28):
    """Paiement (S05 et S21, même recette) : les pièces vont de leur place jusque dans la facture, sous le montant
    (trajet sous le montant) ; à l'arrivée, montant deep et coche r 32 qui surgit à x1,3 puis revient. -> arrivée."""
    for k, (cid, pt) in enumerate(zip(coins, [S.to_world("facture", list(q), f) for q in FACTURE_COINS_LOCAL])):
        kit.move(cid, f + k, [round(pt[0], 2), round(pt[1], 2)], d=jump, arc=arc, scale=PAY_K)
    arrive = f + jump + len(coins) - 2
    S.key("facture_montant", "color", arrive, DEEP, 6)
    g = kit.pop("facture_coche", arrive, scale=1.3, d=6)
    S.key("facture_coche", "scale", g, 1, 5, "inOut")
    return arrive
