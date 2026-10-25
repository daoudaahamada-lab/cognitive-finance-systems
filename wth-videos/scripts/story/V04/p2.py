"""V04, partie 2 : S09-S14, images 854-1699. Piège 1 : « Toi » se retourne et compte 8 pièces ; le volet s'ouvre ;
les 6 pièces accrochées glissent le long de leurs fils jusqu'à leurs factures (« 600 € », « fin du mois ») ; il en
reste 2 : « 200 € » sort du stylo sous elles, la pilule « 800 € » tremble ; le piège 1 se range dans le disque 1.
Piège 2 : le panier coché relié à c8 par un fil à horloge (l'aiguille tourne), « Toi » se retourne, la carte et le
sablier plats (le sable coule) ; c8 se découpe en trois tiers ; c8 entre dans le sablier ; le piège 2 se range dans
le disque 2 ; le miroir : « 800 € » relié au gros reflet qui grandit, c7 à la petite tirelire posée devant.

Temps forts :
S09  Tu@854  800 €@869  Mais@926  600 €@932  partent@979  fin@1019
S10  Ce@1047  dépenser :@1078  200 €,@1104  pas@1133  800 €.@1143
S11  Ça@1183  suffit@1192  dépenses@1229  faites,@1260  mais@1282  voient@1294
S12  Deuxième@1335  oublier@1364  différés.@1395
S13  Carte@1425  différé,@1445  plusieurs@1482  fait.@1521  parti.@1581
S14  Résultat :@1609  solde@1639  paraît@1649  haut@1670  l’est.@1688

Raccord vers p3 : à l'image 1699, l'état est exactement ENTRY_P3 ; « Toi » retourné (`toi_dos`) en P1.
"""
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, point_at_length  # noqa: F401
from pipeline.story_kit import TAP, frames

from . import (BAC_H, COIN_IN_BAC, COIN_K, COIN_R, COIN_PLACES, COINS, ENTRY_P2, FACT_BAC, FACT_IDS, FILS, FIL_COIN,
               FIN_MOIS_S09, HORLOGE_T, MARKER_DISC, MARQ_OVER, MONTANT_200, MONTANT_600, P1, P2, PANIER_C,
               PANIER_CARTE, PANIER_CARTE_K, PANIER_R, PANIER_TAP, REFLET_K, SABLE, SABLIER_IN, SABLIER_TOP, TIERS,
               TIERS_C, COUPES, TIRELIRE_K, assert_reach, scene_f0, turn)

SABLE_PERIOD = 9                                  # le sable coule : un grain toutes les 3 images, chute de 9 images


def _horloge_on_wire(S, f, d, e="inOut", t=HORLOGE_T):
    """L'horloge suit le point t du fil de l'achat pendant d images (le bout pa glisse), sans saut. -> f + d."""
    h0 = S.val("horloge", "pos", f - 1)
    m0 = point_at_length(S.wire_cubic("fil_achat", f - 1), t)
    off = [h0[0] - m0[0], h0[1] - m0[1]]
    for n, p in frames(f, d, e):
        m = point_at_length(S.wire_cubic("fil_achat", n), t)
        S.key("horloge", "pos", n, [round(m[0] + off[0] * (1 - p), 3), round(m[1] + off[1] * (1 - p), 3)], 1,
              "linear")
    return f + d


def tick_clock(S, f, d=6):
    """La grande aiguille de l'horloge tourne d'un quart de tour : le temps passe. -> f + d."""
    S.key("horloge_m", "rot", f, S.val("horloge_m", "rot", f - 1) + 90, d, "inOut")
    return f + d


def marker_done(S, kit, f, k):
    """Le piège k est rangé : coche du disque k (done{k}) et, tant que le disque actif est dessus, la même coche encre
    sur un disque cyan posé dessus (sinon elle resterait cachée jusqu'au changement d'étape)."""
    S.key("marqueur", f"done{k}", f, 1, POP, "out")
    dk, ck = MARQ_OVER[k]
    kit.fade(dk, f + POP - 3, to=1, d=3)
    kit.draw(ck, f + POP, DRAW)


def marker_leave(S, kit, f, k):
    """Le disque actif quitte l'étape k : la coche posée dessus s'efface (la coche du disque rangé reste)."""
    dk, ck = MARQ_OVER[k]
    kit.fade(dk, f, to=0, d=3)
    S.key(ck, "draw", f, 0, 3, "in")


def _t_for_x(cub, x, lo=0.0, hi=1.0):
    """Fraction de longueur du fil dont le point a l'abscisse x (le fil va de la facture, 0, à la pièce, 1)."""
    best = min((abs(point_at_length(cub, i / 400)[0] - x), i / 400) for i in range(int(lo * 400), int(hi * 400) + 1))
    return best[1]


def part(S, kit, c):
    toi, dos = c.toi, c.dos
    f0 = scene_f0(S, "S09")
    kit.pin(f0 - 1, ENTRY_P2)

    # ================= S09 : 8 pièces, 6 partent le long de leurs fils =================
    f = kit.at("S09", "Tu", "« Toi » se retourne vers le téléphone (son stylo repasse à gauche)")
    turn(S, dos, toi, f)

    f = kit.at("S09", "800 €", "les 8 pièces du téléphone battent une à une : il compte 800 €")
    kit.stagger(COINS, f, 2, kit.pulse, peak=1.2)

    f = kit.at("S09", "Mais", "le volet du bac redescend : les trois factures réapparaissent et remontent")
    vb = BAC_H / 2 - 6
    S.keys("bac_volet", f, 6, "out", sy=0, pos=[0, vb])
    for fid, pos in zip(FACT_IDS, FACT_BAC):
        kit.move(fid, f, pos, d=6, e="out")

    f = kit.at("S09", "600 €", "six pièces (c1 à c6) battent une à une ; l'étiquette « 600 € » surgit au-dessus du bac")
    kit.stagger(COINS[:6], f, 2, kit.pulse, peak=1.2)
    kit.pop("montant_600", f, to=MONTANT_600)

    f = kit.at("S09", "partent", "les six pièces glissent le long de leurs fils jusqu'au bac et se posent deux par deux "
                                 "devant leur facture ; leurs places restent vides ; les fils rentrent dans les factures")
    last = f
    wire_of = {v: k for k, v in FIL_COIN.items()}
    for i, cid in enumerate(COINS[:6]):
        w = wire_of[cid]
        g = f + 3 * i
        cub = S.wire_cubic(w, g - 1)
        tx = COIN_IN_BAC[0 if cid in ("c1", "c3", "c5") else 1][0]
        ty = FACT_BAC[i // 2][1]
        t_end = _t_for_x(cub, tx, 0.0, 0.5)
        dy = 0 if w.endswith("a") else COIN_R              # fil de gauche accroché au haut de la pièce
        S.path(cid, g, MOVE, "inOut", lambda p, cub=cub, t_end=t_end: point_at_length(cub, 1 + (t_end - 1) * p),
               lambda p: 1 + (COIN_K - 1) * p, offset=lambda p, dy=dy: (0, dy * (1 + (COIN_K - 1) * p)))
        kit.move(cid, g + MOVE, [tx, ty], d=4, e="out")
        kit.fade(c.cases[i], g, to=1)
        last = g + MOVE + 4
    for w in FILS:
        S.key(w, "draw", last, 0, DRAW, "inOut")

    f = kit.at("S09", "fin", "l'étiquette « fin du mois » surgit au-dessus de « 600 € »")
    S.key("fin_du_mois", "pos", f - 1, list(FIN_MOIS_S09))
    kit.pop("fin_du_mois", f)

    # ================= S10 : 200 €, pas 800 € =================
    f = kit.at("S10", "Ce", "« Toi » marche jusqu'au téléphone")
    toi.walk(f, P2, d=24)

    f = kit.at("S10", "dépenser :", "le stylo touche la dernière pièce ; les deux pièces qui restent battent")
    assert_reach(P2[0], COIN_PLACES[7], "S10 c8")
    hit = toi.tap(f - TAP + 1, COIN_PLACES[7])
    kit.pulse("c7", hit, peak=1.2)
    kit.pulse("c8", hit, peak=1.2)

    f = kit.at("S10", "200 €,", "« 200 € » sort de la pointe du stylo et se pose sous les deux pièces, dans le téléphone")
    kit.pop("montant_200", f, from_pt=toi.tip(f - 1), to=MONTANT_200)
    toi.rest(f)

    kit.hold("S10", "pas", "tenue : « 200 € » sous les deux pièces, « 800 € » en haut, rien ne bouge")

    f = kit.at("S10", "800 €.", "la pilule « 800 € » tremble fort, deux fois : ce n'est pas ce chiffre-là ; "
                                "« 200 € » ne bouge pas")
    kit.shake("solde", f, amp=18)
    kit.shake("solde", f + 4, amp=14)

    # ================= S11 : le panier coché, le fil à horloge =================
    f = kit.at("S11", "Ça", "le bac, les factures, leurs 6 pièces, « 600 € », « fin du mois » et « 200 € » se rangent "
                            "dans le disque 1, qui se coche ; « Toi » retourne à droite")
    for x in ["bac", *FACT_IDS, *COINS[:6], "montant_600", "fin_du_mois", "montant_200"]:
        kit.vanish(x, f, into=list(MARKER_DISC[0]))
    marker_done(S, kit, f, 0)
    toi.walk(f, P1, d=24)

    f = kit.at("S11", "suffit", "les deux pièces qui restent battent")
    kit.pulse("c7", f, peak=1.2)
    kit.pulse("c8", f, peak=1.2)

    f = kit.at("S11", "dépenses", "le panier ressort de la pointe du stylo et se pose devant « Toi »")
    kit.pop("panier", f, from_pt=toi.tip(f - 1), to=PANIER_C)

    f = kit.at("S11", "faites,", "le stylo touche le panier : sa coche se trace au contact, l'achat est fait")
    assert_reach(P1[0], PANIER_TAP, "S11 panier")
    hit = toi.tap(f - TAP + 1, list(PANIER_TAP))
    kit.draw("panier_coche", hit, DRAW)
    toi.rest(hit + 6)

    f = kit.at("S11", "mais", "un fil en tirets va du panier à la pièce c8 ; une grande horloge sort du panier et se "
                              "pose sur le fil")
    kit.draw("fil_achat", f, DRAW)
    hp = point_at_length(S.wire_cubic("fil_achat", f + 4), HORLOGE_T)
    kit.pop("horloge", f + 4, from_pt=list(PANIER_C), to=[round(hp[0], 2), round(hp[1], 2)])

    f = kit.at("S11", "voient", "la pilule « 800 € » bat, inchangée ; l'aiguille de l'horloge tourne ; c8 ne bouge pas")
    kit.pulse("solde", f, peak=1.15)
    tick_clock(S, f)

    # ================= S12 : deuxième piège, la carte et le sablier =================
    f = kit.at("S12", "Deuxième", "le disque actif du repère glisse sur 2 (« Différés ») ; le disque 1 reste coché")
    marker_leave(S, kit, f, 0)
    kit.step(f, 1)

    f = kit.at("S12", "oublier", "« Toi » se retourne en entier, dos au panier")
    turn(S, toi, dos, f)

    f = kit.at("S12", "différés.", "une carte bancaire et un sablier tombent au-dessus du panier")
    kit.drop("carte_sablier", f, h=180)

    # ================= S13 : carte à débit différé, trois tiers =================
    f = kit.at("S13", "Carte", "le panier monte se poser sur la carte ; son fil et l'horloge le suivent ; l'aiguille "
                               "tourne ; le sable commence à couler")
    kit.move("panier", f, PANIER_CARTE, MOVE, scale=PANIER_CARTE_K)
    pa = [round(PANIER_CARTE[0] - PANIER_R * PANIER_CARTE_K, 2), PANIER_CARTE[1]]
    S.key("fil_achat", "pa", f, pa, MOVE, "inOut")
    _horloge_on_wire(S, f, MOVE)
    tick_clock(S, f)
    sand_end = scene_f0(S, "S14") + 30                   # jusqu'au rangement dans le disque 2
    for j, s in enumerate(SABLE):
        S.key(s, "opacity", f + 3 * j, 1)
        for n in range(f + 3 * j, sand_end - SABLE_PERIOD, SABLE_PERIOD):
            S.key(s, "pos", n, [0, -6])
            S.key(s, "pos", n + 1, [0, 40], SABLE_PERIOD - 1, "linear")

    f = kit.at("S13", "différé,", "le bout du fil passe du panier au haut du sablier ; l'aiguille tourne encore, puis "
                                  "l'horloge rentre dans le sablier")
    tick_clock(S, f)
    S.key("fil_achat", "pa", f, list(SABLIER_TOP), 12, "inOut")
    g = _horloge_on_wire(S, f, 12)
    kit.vanish("horloge", g, into=list(SABLIER_IN))

    f = kit.at("S13", "plusieurs", "c8 se découpe en trois tiers (traits en tirets dessus) ; trois tiers en tirets en "
                                   "sortent et s'alignent sous le sablier")
    for k, cp in enumerate(COUPES):
        kit.draw(cp, f + 2 * k, 6)
    for k, tid in enumerate(TIERS):
        kit.pop(tid, f + 6 + 3 * k, from_pt="c8", to=TIERS_C[k], d=MOVE)

    f = kit.at("S13", "fait.", "le panier coché bat deux fois : l'achat est fait ; le premier tiers monte dans le "
                               "sablier")
    kit.pulse("panier", f, times=2, peak=round(1.25 * PANIER_CARTE_K, 4))
    kit.pulse("panier_coche", f, peak=1.4)
    for tid, n in zip(TIERS, (f + 8, S.word_after("pas", f), S.word_after("encore", f))):
        kit.vanish(tid, n, into=[SABLIER_IN[0], SABLIER_IN[1] + 78], d=MORPH)

    f = kit.at("S13", "parti.", "c8 bat deux fois à sa place, sans partir ; la pilule « 800 € » ne bouge pas")
    kit.pulse("c8", f, times=2, peak=1.3)

    # ================= S14 : le miroir =================
    f = kit.at("S14", "Résultat :", "c8 glisse le long du fil jusque dans le haut du sablier ; sa place reste vide")
    S.along_wire("c8", "fil_achat", f, MOVE, "inOut", 1, 0, at_frame=f - 1, scale=COIN_K)
    kit.move("c8", f + MOVE, list(SABLIER_IN), d=4, e="out")
    kit.fade("case8", f, to=1)

    f = kit.at("S14", "solde", "la carte, le sablier, le panier et c8 se rangent dans le disque 2, qui se coche")
    S.key("fil_achat", "draw", f, 0)
    for x in ["carte_sablier", "panier", "c8"]:
        kit.vanish(x, f, into=list(MARKER_DISC[1]))
    marker_done(S, kit, f, 1)
    S.key("panier_coche", "draw", f + POP + 1, 0)
    for cp in COUPES:
        S.key(cp, "draw", f + POP + 1, 0)

    f = kit.at("S14", "paraît", "un miroir surgit ; une petite tirelire est posée devant ; dans le miroir, son reflet")
    kit.pop("miroir", f)
    kit.pop("tirelire", f + 2, scale=TIRELIRE_K)
    kit.pop("reflet", f + 4, scale=TIRELIRE_K)

    f = kit.at("S14", "haut", "dans le miroir, le reflet grandit, bien plus gros que la tirelire ; un fil plein relie "
                              "la pilule « 800 € » au gros reflet")
    S.key("reflet", "scale", f, REFLET_K, 12, "inOut")
    kit.draw("preuve_solde", f, 12)

    f = kit.at("S14", "l’est.", "un fil plein relie la seule pièce restante (c7) à la petite tirelire, qui bat")
    g = kit.draw("preuve_piece", f, 5)
    last = kit.pulse("tirelire", g, peak=round(1.25 * TIRELIRE_K, 4))
    assert last <= scene_f0(S, "S15") - 1, last
