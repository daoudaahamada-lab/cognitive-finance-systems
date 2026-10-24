"""V07, partie 2 : S10-S15, images 1045-1948 (erreur 1 : les noms et le MSCI World ; erreur 2 : le poids). 29 temps
forts, 30,1 s.

ÉTAT D'ENTRÉE (etat_initial de S10, à épingler à 1044 : `kit.pin(f0 - 1, ENTRY_P2)`) : « Toi » en P1 (760), bras
baissé, penché vers l'étiquette (lean -9, look -1, ligne de regard `regard` tracée) ; repère sur 1 sous « 3 erreurs » ;
`livre` « Indice » en LIVRE_C relié par `ficelle` au `panier` OUVERT x 1,3 (PANIER_C) ; `etiquette` x 1,3 en ETIQ_C.

Temps forts (image du mot) :
S10  «Monde»,@1045  «États-Unis»,@1069  «Tech»:@1098  derrière@1121  indice@1172  règles.@1193
S11  Le@1216  MSCI@1223  exemple,@1296  couvre@1318  développés,@1344  mais@1371  émergents.@1393
S12  Ça@1418  savoir@1465  pèse@1488  pays.@1503
S13  Deuxième@1531  croire@1567  «Monde»@1590  équilibré.@1622
S14  indices@1664  taille@1713  entreprises,@1724  États-Unis@1762  pèsent@1779  70 %.@1824
S15  Ton@1868  «Monde»@1882  américain.@1919
Geste secondaire : S11 « World, »@1275 (le titre « MSCI World » bat).

Tour de revue 1 : S10 le panier se range x 0,85 en (300, 1080) pour libérer la place ; « Monde » reste relié à
l'étiquette par un fil pendant sa montée ; les trois livres (x 0,8, y 720) ont des pages distinctes (globe, drapeau,
puce ; 3 règles de longueurs différentes, tracées une à une). S11 : règles ancrées à droite (x 600), marque après le
texte (le bras ne cache rien) ; « Toi » se place en P_S11 sur « exemple, » ; « émergents. » : une barrière encre se
trace devant le panier, trois titres ocre arrivent de la droite, la heurtent (elle tremble) et tombent au sol, où ils
restent jusqu'à « Ça » ; la croix se trace au troisième choc. S12 : le fil livre -> règle rentre dans le livre, les
règles s'effacent en opacité. S13 : ronds décalés d'une image, bulle à +2. S15 : le fil rouge part de « États-Unis »
et entre dans « ETF Monde » (seul fil vers l'étiquette).

PASSAGE À p3 (image 1948 = ENTRY_P3 de __init__, exactement) : balance BALANCE_C rot -10, poids à seat(S14_X,
S14_R), panier échelle 0, livre échelle 0 en DISQUE_PT[0], étiquette en ETIQ_BAL (ficelle_etiq 0, ficelle_etiq_bal
draw 0), lien_rouge tracé, compteur 70 en COMPTEUR_C, pil_usa / pil_autres à leur place, marqueur active 1 / done0 1,
fils de S10-S11 à opacité 0, barrière et bulle2 à 0 ; « Toi » en P2, bras baissé, look 0, lean 0.
"""
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, SCALE, TILT  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401

from . import *  # noqa: F401,F403
from . import (BALANCE_C, BARRIERE_X, CYAN, CYAN_SEATS, DISQUE_PT, EMERG_IN_Y, EMERGENT_R, EMERGENTS_SOL,
               ENTRY_P2, ETIQ_BAL, ETIQ_S10, LIGHT, LIVRE_S10, LIVRE_S10_K, LIVRE_S11, LIVRE_S11_K, LIVRES,
               LIVRES_S10_Y, MINIS, NOM_LIVRE, NOMS, P1, P2, P_S11, PANIER_BAL_C, PANIER_S10, PANIER_S10_K, POIDS,
               REGLE_MARK_X, REGLE_Y, S14_R, S14_X, SEATS_S12, TILTS, TITRE_R, TITRE_TOMBE, TITRES, TITRES_LOCAL,
               assert_reach, lean_low, lower, page_ids, scene_f0, seat, walk_low)

NOM_IDS = ["nom_monde", "nom_usa", "nom_tech"]
LIVRE_X = {"livre": NOMS["nom_monde"][1][0], "livre_usa": NOMS["nom_usa"][1][0], "livre_tech": NOMS["nom_tech"][1][0]}
LIVRE_FROM_Y = 560                              # S10 : chaque livre part de derrière son nom (y 560) vers y 720
MARK = [(REGLE_MARK_X, REGLE_Y[0] - 8), (REGLE_MARK_X, REGLE_Y[1] - 8)]   # pointe du stylo : la marque de chaque règle
BULLE2_S13 = (700, 560)
BULLE2_RONDS_S13 = [(848, 968), (832, 862), (812, 740)]
VISIBLE_MINIS = [m for k, m in enumerate(MINIS) if k != TITRE_TOMBE] + ["mini_neuf", "livre_etc"]


def _r(pt):
    return [round(pt[0], 3), round(pt[1], 3)]


def _panier_titres():
    """Les 10 titres visibles du panier, triés de gauche à droite (x local) : (id, x local, y local)."""
    ids = [(t, TITRES_LOCAL[k]) for k, t in enumerate(TITRES) if k != TITRE_TOMBE]
    ids.append(("titre_neuf", TITRES_LOCAL[TITRE_TOMBE]))
    return [t for t, _ in sorted(ids, key=lambda it: (it[1][0], it[1][1]))]


def _wire_out(S, wid, f, d=5):
    """Un fil se retire (draw 1 -> 0, ease-in) puis passe à l'opacité 0 (état attendu par p3). -> f + d."""
    S.key(wid, "draw", f, 0, d, "in")
    S.key(wid, "opacity", f + d, 0)
    return f + d


def part(S, kit, c):
    toi = c.toi
    f0 = scene_f0(S, "S10")
    kit.pin(f0 - 1, ENTRY_P2)
    if S.val("toi", "scale", f0 - 1) == 0:      # partie construite seule : la figurine n'est pas entrée
        toi.enter(f0 - 10, at=list(P1))
        lower(toi, f0 - 1, d=1)
    kit.ensure("toi", "look", 0)

    # ================= S10 : « Monde », « États-Unis », « Tech » : derrière chaque nom, un livre =================
    f = kit.at("S10", "« Monde »,", "« Toi » se redresse ; la pilule « Monde » sort de l'étiquette et monte en haut "
                                    "à gauche, reliée à elle par un fil ; la ficelle rentre ; le livre se réduit "
                                    "derrière la pilule ; le panier se range en bas à gauche")
    S.key("toi", "look", f, 0, 4, "out")
    lean_low(toi, f, 0, d=5)
    S.key("regard", "from", f, 1, 5, "in")
    S.key("nom_monde", "pos", f - 1, _r(S.to_world("etiquette", [0, 0], f - 1)))
    kit.pop("nom_monde", f)
    kit.move("nom_monde", f, list(NOMS["nom_monde"][1]))
    S.key("ficelle", "from", f, 1, DRAW, "in")
    kit.move("livre", f, list(LIVRE_S10), scale=LIVRE_S10_K)
    kit.fade("livre_titre", f, to=0)
    S.key("livre_titre", "scale", f + FADE, 0)
    for m in VISIBLE_MINIS:                      # la page du livre se vide : elle portera ses règles
        kit.vanish(m, f, d=6)
    kit.move("panier", f, list(PANIER_S10), scale=PANIER_S10_K)
    kit.move("etiquette", f, list(ETIQ_S10), scale=PANIER_S10_K)
    kit.draw("fil_monde", f + 3, 8)

    f = kit.at("S10", "« États-Unis »,", "la pilule « États-Unis » surgit sur place, à droite de « Monde », sans lien "
                                         "avec le panier")
    kit.pop("nom_usa", f)

    f = kit.at("S10", "« Tech » :", "la pilule « Tech » surgit sur place : trois noms d'ETF en rang")
    kit.pop("nom_tech", f)

    f = kit.at("S10", "derrière", "de derrière chaque nom, un livre glisse vers le bas (Monde, puis États-Unis, puis "
                                  "Tech) ; un court fil relie chaque nom à son livre")
    for k, lid in enumerate(LIVRES):
        g = f + 4 * k
        if lid != "livre":
            S.key(lid, "pos", g - 1, [LIVRE_X[lid], LIVRE_FROM_Y])
            kit.pop(lid, g, scale=LIVRE_S10_K, d=6)
        kit.move(lid, g, [LIVRE_X[lid], LIVRES_S10_Y], d=MORPH, e="out")
        kit.draw(f"fil_{NOM_IDS[k]}", g + 5, DRAW)

    f = kit.at("S10", "indice", "les trois livres battent l'un après l'autre et chacun montre son pictogramme : un "
                                "globe, un drapeau, une puce")
    for k, lid in enumerate(LIVRES):
        kit.pulse(lid, f + 3 * k, peak=round(LIVRE_S10_K * 1.1, 4))
        kit.pop(page_ids(lid)[0][0], f + 3 * k, scale=1, d=7)

    f = kit.at("S10", "règles.", "sur la page droite de chaque livre, trois règles de longueurs différentes "
                                 "s'écrivent une à une, puis les trois livres battent ensemble")
    for k in range(3):
        for j, lid in enumerate(LIVRES):
            _, bars, puces = page_ids(lid)
            g = f + 3 * k + j
            kit.pop(puces[k], g, d=4)
            kit.draw(bars[k], g, 6)
    for lid in LIVRES:
        kit.pulse(lid, f + 14, peak=round(LIVRE_S10_K * 1.15, 4))

    # ================= S11 : le MSCI World couvre les pays développés, pas les émergents =================
    f = kit.at("S11", "Le", "« Monde » rentre dans l'étiquette, son fil avec lui ; « États-Unis », « Tech » et leurs "
                            "livres se réduisent ; le livre de « Monde » grandit au centre, sa liste de titres revient")
    kit.vanish("nom_monde", f, into="etiquette")
    S.key("fil_monde", "draw", f, 0, 6, "in")
    S.key("fil_monde", "opacity", f + 6, 0)
    for nid in NOM_IDS:
        _wire_out(S, f"fil_{nid}", f)
    for k, nid in enumerate(NOM_IDS[1:]):
        kit.vanish(nid, f + 4 * k)
        kit.vanish(NOM_LIVRE[nid], f + 4 * k)
    pic, bars, puces = page_ids("livre")
    for i in pic + bars + puces:
        kit.vanish(i, f, d=6)
    kit.move("livre", f, list(LIVRE_S11), scale=LIVRE_S11_K)
    for k, m in enumerate(VISIBLE_MINIS):
        kit.pop(m, f + 6 + k // 3, scale=1, d=6)

    f = kit.at("S11", "MSCI", "le titre « MSCI World » s'écrit au-dessus du livre")
    kit.type("livre_msci", f, rate=1)
    kit.pulse("livre_msci", S.word_after("World,", f), peak=1.08)

    f = kit.at("S11", "exemple,", "« Toi » s'avance sous le livre, prêt à le lire")
    walk_low(toi, f, P_S11[0], d=10)

    f = kit.at("S11", "couvre", "un fil sort du livre vers la 1re règle ; la pointe du stylo de « Toi » se pose au "
                                "bout de la ligne pendant que « pays développés » s'écrit vers elle ; sa coche pleine "
                                "se trace au bout")
    for pt in MARK:
        assert_reach(P_S11[0], pt, "S11 marque de règle", fig_y=P_S11[1])
    toi.reach(f - 8, [MARK[0][0] + 6, MARK[0][1] - 12], d=8)
    kit.draw("fil_livre_regle", f, DRAW)
    n1 = len(S.ents["regle1"]["p"]["text"])
    done = kit.type("regle1", f, rate=n1 / 13)
    hit = toi.tap(done - TAP + 1, list(MARK[0]))
    kit.draw("regle1_coche", hit, 6)

    f = kit.at("S11", "développés,", "un fil cyan profond part de la règle vers les titres du panier, qui battent tous "
                                     "en vague : ils sont tous de pays développés")
    kit.draw("fil_regle_titres", f, DRAW)
    kit.stagger(_panier_titres(), f + 4, 2, kit.pulse, peak=1.18)

    f = kit.at("S11", "mais", "la pointe passe au bout de la 2e ligne pendant que « pays émergents » s'écrit vers elle")
    toi.reach(f - 4, [MARK[1][0] + 6, MARK[1][1] - 10], d=6)
    n2 = len(S.ents["regle2"]["p"]["text"])
    kit.type("regle2", f, rate=n2 / 13)

    f = kit.at("S11", "émergents.", "« Toi » baisse le stylo ; une barrière encre se trace devant le panier ; trois "
                                    "titres ocre arrivent de la droite, la heurtent l'un après l'autre (elle tremble) "
                                    "et tombent au sol ; au 3e choc, une croix se trace devant « pays émergents »")
    lower(toi, f, 6)
    kit.draw("barriere", f, 7)
    shock = f
    for k, e in enumerate(c.emergents):
        g = f + 3 + 3 * k
        kit.pop(e, g, d=5)
        hit_x = BARRIERE_X + EMERGENT_R + 6
        shock = kit.move(e, g, [hit_x, EMERG_IN_Y + 6 * k], d=9, e="in")
        kit.shake("barriere", shock, amp=8, axis="x")
        sol = EMERGENTS_SOL[k]
        S.key(e, "pos", shock, [hit_x + 14, EMERG_IN_Y + 6 * k - 6], 3, "out")
        kit.drop(e, shock + 3, d=9, to=list(sol), h=sol[1] - (EMERG_IN_Y + 6 * k - 6),
                 dx=hit_x + 14 - sol[0])
    kit.draw("regle2_croix", shock, 6)

    # ================= S12 : combien pèse chaque pays ? Le panier devient balance =================
    f = kit.at("S12", "Ça", "le livre rentre dans le disque 1 du repère (son fil rentre avec lui), qui se coche ; les "
                            "règles s'effacent ; barrière et titres émergents se réduisent")
    a = S.to_world("livre", [0, 0], f - 1)
    b = DISQUE_PT[0]
    s0 = S.world_scale("livre", f - 1)
    S.path("livre", f, MORPH, "inOut",
           lambda p: [a[0] + (b[0] - a[0]) * p - 120 * p * (1 - p) * 4 * 0.5, a[1] + (b[1] - a[1]) * p],
           scale_at=lambda p: s0 * (1 - p) + 0.001)
    S.key("livre", "scale", f + MORPH, 0)
    S.key("livre", "opacity", f + MORPH, 0)
    S.key("fil_livre_regle", "draw", f, 0, 6, "in")
    S.key("fil_livre_regle", "opacity", f + 6, 0)
    S.key("marqueur", "done0", f + MORPH - 3, 1, DRAW, "out")
    kit.draw("disque1_coche", f + MORPH - 3, DRAW)
    g = f + 6
    _wire_out(S, "fil_regle_titres", g)
    for i in ("regle1", "regle2", "regle1_coche", "regle2_croix"):
        kit.fade(i, g, to=0)
        S.key(i, "scale", g + FADE, 0)
    kit.morph([*c.emergents, "barriere"], [], g)

    f = kit.at("S12", "savoir", "« Toi » passe à droite ; le panier et son étiquette reviennent au centre, à taille "
                                "normale")
    walk_low(toi, f, P2[0], d=12)
    kit.move("panier", f, list(PANIER_BAL_C), scale=1)
    kit.move("etiquette", f, [PANIER_BAL_C[0], PANIER_BAL_C[1] + 40], scale=1)

    f = kit.at("S12", "pèse", "le panier se replie pendant que la balance surgit à sa place ; ses titres sautent un "
                              "à un sur la planche, à plat ; l'étiquette glisse et pend au flanc du pivot")
    kit.pop("balance", f, d=MORPH)
    kit.vanish("panier", f, d=MORPH, e="in")
    order = _panier_titres()
    landed = {}
    for k, (tid, pid) in enumerate(zip(order, POIDS)):
        g = f + 1 + k
        start = S.to_world(tid, [0, 0], g - 1)
        s0 = S.world_scale(tid, g - 1)
        lx, ly = seat(SEATS_S12[k], TITRE_R)
        end = [BALANCE_C[0] + lx, BALANCE_C[1] + ly]
        S.key(tid, "scale", g, 0)
        S.key(pid, "opacity", g - 1, 1)
        S.path(pid, g, 10, "inOut",
               lambda p, a=start, b=end: [a[0] + (b[0] - a[0]) * p, a[1] + (b[1] - a[1]) * p - 40 * 4 * p * (1 - p)],
               scale_at=lambda p, s=s0: s + (1 - s) * p)
        S.key(pid, "pos", g + 9, [lx, ly])
        S.key(pid, "scale", g + 9, 1)
        landed[k] = g + 10
    S.key("ficelle_etiq", "draw", f, 0, 6, "in")
    kit.move("etiquette", f, list(ETIQ_BAL))
    kit.draw("ficelle_etiq_bal", f + 8, DRAW)

    f = kit.at("S12", "pays.", "cinq titres passent au cyan, cinq restent clairs ; les légendes « États-Unis » "
                               "(cyan) et « autres pays » surgissent ; autant de chaque côté : la planche reste à plat")
    for k in CYAN_SEATS:
        S.key(POIDS[k], "fill", max(f, landed[k] - 4), CYAN, 9)
    kit.pop("pil_usa", f)
    kit.pop("pil_autres", f + 3)

    # ================= S13 : croire que « Monde » veut dire équilibré =================
    f = kit.at("S13", "Deuxième", "le disque actif du repère glisse du 1 au 2 « Poids »")
    kit.step(f, 1)
    kit.vanish("disque1_coche", f, d=6)

    f = kit.at("S13", "croire", "trois ronds montent de la tête de « Toi » et sa bulle s'ouvre : une petite balance "
                                "à plat, jetons en miroir")
    for k in range(3):
        S.key(f"bulle2_rond{k + 1}", "pos", f + k - 1, list(BULLE2_RONDS_S13[k]))
        kit.pop(f"bulle2_rond{k + 1}", f + k, d=6)
    S.key("bulle2", "pos", f + 1, list(BULLE2_S13))
    kit.pop("bulle2", f + 2)

    f = kit.at("S13", "« Monde »", "l'étiquette « ETF Monde » bat")
    kit.pulse("etiquette", f, peak=1.15)

    f = kit.at("S13", "équilibré.", "une coche pleine se trace dans le coin de la bulle : il en est sûr")
    kit.draw("bulle2_coche", f, DRAW)

    # ================= S14 : pondéré par la taille, ≈ 70 % États-Unis =================
    f = kit.at("S14", "indices", "le repère bat (disque 1 coché : l'indice)")
    kit.pulse("marqueur", f, peak=1.08)

    f = kit.at("S14", "taille", "les titres prennent la taille de leur entreprise : trois cyan deviennent géants, "
                                "les clairs rapetissent ; la planche reste à plat")
    for k, pid in enumerate(POIDS):
        S.key(pid, "scale", f, round(S14_R[k] / TITRE_R, 4), SCALE, "inOut")
        S.key(pid, "pos", f, seat(SEATS_S12[k], S14_R[k]), SCALE, "inOut")

    f = kit.at("S14", "entreprises,", "les titres se rangent par pays : les cyan à gauche, les clairs à droite")
    for k, pid in enumerate(POIDS):
        kit.move(pid, f, seat(S14_X[k], S14_R[k]), arc=30 if k in CYAN_SEATS else 70)

    f = kit.at("S14", "États-Unis", "la pilule « États-Unis » bat au-dessus de son groupe")
    kit.pulse("pil_usa", f, peak=1.15)

    f = kit.at("S14", "pèsent", "la balance penche franchement côté États-Unis ; la bulle de « Toi » éclate")
    S.key("balance", "rot", f, TILTS["S14"], TILT, "out")
    kit.vanish("bulle2", f, style="burst")
    for k in range(3):
        kit.vanish(f"bulle2_rond{k + 1}", f, d=6)

    f = kit.at("S14", "70 %.", "le chiffre rouge « ≈ 70 % » surgit au-dessus de « États-Unis » et compte de 0 à 70")
    kit.pop("compteur", f)
    S.key("compteur", "value", f, 70, 15, "out")

    # ================= S15 : ton « Monde » est surtout américain =================
    f = kit.at("S15", "Ton", "l'étiquette « ETF Monde » bat")
    kit.pulse("etiquette", f, peak=1.15)

    f = kit.at("S15", "« Monde »", "la ficelle du pivot se retire ; un fil rouge épais se trace de « États-Unis » "
                                   "jusqu'à « ETF Monde », par-dessus la planche")
    S.key("ficelle_etiq_bal", "draw", f, 0, 5, "in")
    kit.draw("lien_rouge", f + 2, DRAW)

    f = kit.at("S15", "américain.", "les cinq titres cyan et « ≈ 70 % » battent ensemble ; tenue")
    for k in CYAN_SEATS:
        kit.pulse(POIDS[k], f, peak=round(S14_R[k] / TITRE_R * 1.12, 4))
    kit.pulse("compteur", f, peak=1.12)
    assert f + 6 < scene_f0(S, "S16")
