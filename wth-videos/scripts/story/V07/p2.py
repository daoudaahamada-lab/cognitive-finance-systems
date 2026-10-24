"""V07, partie 2 : S10-S15, images 1045-1948 (erreur 1 : les noms et le MSCI World ; erreur 2 : le poids). 29 temps
forts, 30,1 s. La partie la plus dense (lecture au stylo S11, panier -> balance S12, pesée S14) : moins de temps forts.

ÉTAT D'ENTRÉE (etat_initial de S10, à épingler à 1044 : `kit.pin(f0 - 1, ENTRY_P2)` avec f0 = scene_f0(S, "S10")) :
« Toi » en P1 (660, 1135), bras baissé, dos au livre (look +1) ; repère `marqueur` sur 1 (on 1, active 0) sous
`titre_erreurs` « 3 erreurs » ; `livre` « Indice » (souligné) en LIVRE_C relié par `ficelle` au `panier` OUVERT
(PANIER_C, 10 titres light : titre1..7, titre9, titre10, titre_neuf) ; `etiquette` en ETIQ_C.
Garde-fou figurine (partie construite seule) : `if S.val("toi", "scale", f0 - 1) == 0: c.toi.enter(f0 - 10,
at=list(P1))` ; puis `kit.ensure("toi", "look", 0)` : dans le film entier look vaut +1 à f0 - 1 (posé par p1), en
partie seule 0 ; la clé look -> 0 de « Monde » marche dans les deux cas.

Temps forts (image du mot) :
S10  «Monde»,@1045  «États-Unis»,@1069  «Tech»:@1098  derrière@1121  indice@1172  règles.@1193
S11  Le@1216  MSCI@1223  exemple,@1296  couvre@1318  développés,@1344  mais@1371  émergents.@1393
S12  Ça@1418  savoir@1465  pèse@1488  pays.@1503
S13  Deuxième@1531  croire@1567  «Monde»@1590  équilibré.@1622
S14  indices@1664  taille@1713  entreprises,@1724  États-Unis@1762  pèsent@1779  70 %.@1824
S15  Ton@1868  «Monde»@1882  américain.@1919

BRIEF, scène par scène :
- S10 « Monde » : look +1 -> 0 ; {nom_monde} naît de {etiquette} (pop from_pt « etiquette ») et monte en (190, 520)
  (move 550) ; {ficelle} se retire (piste `from` 0 -> 1 : c'est l'état attendu par p3) ; {livre} passe SOUS la pilule
  (z) et se réduit en LIVRE_S10 x0,6 (move 550). « États-Unis » : {nom_usa} pop SUR PLACE (450, 520) — aucun lien
  avec le panier. « Tech » : {nom_tech} pop sur place (720, 520). « derrière » : {livre}, puis {livre_usa}, puis
  {livre_tech} (x0,6) glissent de 130 px vers le bas jusqu'à LIVRES_S10_Y (move 350 out, 4 images d'écart ; les deux
  autres livres : scale 0 -> 0,6 au départ, position y 560) ; {fil_nom_monde/usa/tech} se tracent (draw).
  « indice » : les trois livres battent (stagger 3, x1,08). « règles. » : sur chaque livre {<livre>_regle1..3} se
  tracent (stagger 3 de kit.draw) et leurs {<livre>_puce1..3} pop. Le panier et « Toi » ne bougent pas.
- S11 « Le » : {nom_monde} rentre dans {etiquette} (vanish into) ; {nom_usa}, {nom_tech}, {livre_usa}, {livre_tech}
  et les trois fils se réduisent sur place (4 images d'écart ; fils : opacité 0 en fin, état attendu par p3) ;
  {livre} grandit en LIVRE_S11 x1 (move 550). « MSCI » (7 images après « Le ») : {livre_titre} s'efface (FADE) et
  {livre_msci} « MSCI World » s'écrit (kit.type rate 1). « exemple, » : {panier} -> PANIER_S11 x0,7 et {etiquette}
  -> ETIQ_S11 x0,7 avec les MÊMES clés (move 550) ; « Toi » reste en P1 (les règles sont placées pour P1).
  « couvre » : {fil_livre_regle} se trace ; « Toi » lit : `c.toi.trace(f, [(REGLE_MARK_X, REGLE_Y[0]),
  (REGLE_TRACE_END_X, REGLE_Y[0])])` pendant que {regle1} s'écrit et que {regle1_coche} se trace au départ (coche
  HUMAINE pleine deep). « développés, » : {fil_regle_titres} (deep) se trace vers les titres du panier réduit, qui
  battent en vague (stagger 2, x1,15). « mais » : même lecture sur la 2e ligne (REGLE_Y[1]) pendant que {regle2}
  s'écrit. `lower` après. « émergents. » : {emergent1..3} sortent du bout de {regle2} (x ≈ REGLE_X + 250), sautent en
  arc 120 vers le panier (stagger 3), rebondissent (shake x 8) et tombent à EMERGENTS_SOL (kit.drop) ; {regle2_croix}
  se trace (kit.draw). Avant chaque geste : assert_reach(P1[0], …) (vérifié : 440 -> 570 sur les deux lignes).
- S12 « Ça » : {livre} se réduit dans le disque 1 (vanish into DISQUE_PT[0], MORPH) et une coche se trace dans le
  disque (`done0` 0 -> 1, 9 images) ; {regle1}, {regle2}, {regle1_coche}, {regle2_croix}, {fil_livre_regle},
  {fil_regle_titres}, {emergent1..3} sortent (morph sortie groupée). « savoir » : walk_low vers P2 ; {panier} revient
  en PANIER_BAL_C x1 et {etiquette} en (400, 1050) x1 (mêmes clés). « pèse » : MORPH 350 ms : {panier} se réduit
  vers le pivot (vanish, échelle 0 en fin ; ses titres partent avec lui) pendant que {balance} grandit en BALANCE_C
  (pop) ; {poids1..10} sautent des places des titres (position monde des titres à f - 1, S.parent_space) vers
  seat(SEATS_S12[k], TITRE_R) (stagger 1, arc 40) ; {etiquette} glisse vers ETIQ_BAL pendant que {ficelle_etiq}
  s'efface (draw 1 -> 0) et que {ficelle_etiq_bal} se trace (draw 0 -> 1). « pays. » : {poids} CYAN_SEATS passent au
  cyan (piste fill hex, 9 images) ; {pil_usa} et {pil_autres} pop. La planche reste à plat (autant de chaque côté).
- S13 « Deuxième » : kit.step(f, 1) (le disque actif glisse de 1 à 2 « Poids » ; done0 reste 1). « croire » :
  {bulle2_rond1..3} montent de la tête de « Toi » en P2 (stagger 2 de pop), {bulle2} s'ouvre avec sa mini balance à
  plat ({bulle2_balance}, {bulle2_jeton1..4}, enfants : ils viennent avec elle). « Monde » : {etiquette} bat (x1,15).
  « équilibré. » : {bulle2_coche} se trace (coche pleine deep). La mini balance ne bouge pas.
- S14 « indices » : le disque 1 coché bat (pulse sur le marker impossible par disque : faire battre tout le marker à
  x1,08, ou rien de plus qu'un `done0` déjà posé — choisir le pulse du marker). « taille » : {poids} prennent leur
  taille (scale -> S14_R[k] / TITRE_R, SCALE 10 images ; y du siège : seat(x, r) en même temps). « entreprises, » :
  {poids} glissent par pays vers S14_X (move arc 30, 550 inOut). « États-Unis » : {pil_usa} bat (x1,15). « pèsent » :
  {balance} rot 0 -> TILTS["S14"] (TILT 14 images, out) ; dans les mêmes images {bulle2} et tout son contenu + ses
  ronds éclatent (vanish 300 ms). « 70 %. » : {compteur} pop en COMPTEUR_C et compte 0 -> 70 (15 images out).
- S15 « Ton » : {etiquette} bat (x1,15). « Monde » : {lien_rouge} se trace (draw, 9 images) de l'étiquette au géant
  {poids1}. « américain. » : les 5 {poids} cyan et {compteur} battent ensemble (x1,12) ; tenue jusqu'à 1948.

PASSAGE À p3 (image 1948 = ENTRY_P3 de __init__, exactement) : balance BALANCE_C rot -12, poids à seat(S14_X, S14_R)
et à leur échelle S14_R/26 (cyan / light en hex), panier échelle 0 en PANIER_BAL_C, livre échelle 0 en DISQUE_PT[0],
étiquette en ETIQ_BAL (ficelle_etiq draw 0, ficelle_etiq_bal draw 1), ficelle from 1, lien_rouge tracé, compteur
70 en COMPTEUR_C, pil_usa / pil_autres à leur place, marqueur active 1 / done0 1 / done1 0, fils de S10-S11 à
opacité 0, bulle2 et ronds à 0 ; « Toi » en P2, bras baissé, look 0.

Règles : bras baissé entre deux gestes ; « Toi » ne bouge que par walk_low / reach / tap / trace / lower ; rouge
uniquement pour {compteur} et {lien_rouge} ; aucun gris ; aucune coche variant « ai ».
"""
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, SCALE, TILT  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401

from . import *  # noqa: F401,F403
from . import (BALANCE_C, CYAN, CYAN_SEATS, DEEP, DISQUE_PT, EMERGENTS_SOL, ENTRY_P2, ETIQ_BAL, ETIQ_S11, LIGHT,
               LIVRE_S10, LIVRE_S10_K, LIVRE_S11, LIVRE_S11_K, LIVRES_S10_Y, NOM_LIVRE, NOMS, P1, P2, PANIER_BAL_C,
               PANIER_S11, PANIER_S11_K, POIDS, REGLE_MARK_X, REGLE_TRACE_END_X, REGLE_Y, S14_R, S14_X, SEATS_S12,
               TILTS, TITRE_R, TITRE_TOMBE, TITRES, TITRES_LOCAL, assert_reach, lower, scene_f0, seat, walk_low)

LIVRES = ["livre", "livre_usa", "livre_tech"]
NOM_IDS = ["nom_monde", "nom_usa", "nom_tech"]
LIVRE_X = {"livre": NOMS["nom_monde"][1][0], "livre_usa": NOMS["nom_usa"][1][0], "livre_tech": NOMS["nom_tech"][1][0]}
LIVRE_FROM_Y = 560                              # S10 : chaque livre part de derrière son nom (y 560) vers y 690
# S11 « émergents. » : où chaque titre émergent heurte les titres du panier rangé (x0,7 : titres y ≈ 990-1010)
EMERG_HIT = [(300, 958), (262, 952), (224, 958)]
# la pointe relit chaque règle de x 440 à 570 (ligne 1) et à 505 (ligne 2 : au-delà, la cible est à moins de 177 px de
# l'épaule et le poignet se plie contre le buste)
REGLE_LIGNE = [[(REGLE_MARK_X, REGLE_Y[0]), (REGLE_TRACE_END_X, REGLE_Y[0])],
               [(REGLE_MARK_X, REGLE_Y[1]), (505, REGLE_Y[1])]]
# S13 : la bulle descend de 30 px et ses ronds font une chaîne régulière de la tête (860, 1039) au bas de la bulle
BULLE2_S13 = (700, 650)                         # x 540-860, y 565-735 (au-dessus de « autres pays », y 854)
BULLE2_RONDS_S13 = [(846, 990), (824, 900), (800, 790)]


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
    f = kit.at("S10", "« Monde »,", "« Toi » se retourne vers la scène ; la pilule « Monde » sort de l'étiquette et "
                                    "monte en haut à gauche ; la ficelle rentre dans le panier ; le livre se réduit "
                                    "et se cache derrière la pilule")
    S.key("toi", "look", f, 0, 4, "out")
    S.key("nom_monde", "pos", f - 1, _r(S.to_world("etiquette", [0, 0], f - 1)))
    kit.pop("nom_monde", f)
    kit.move("nom_monde", f, list(NOMS["nom_monde"][1]))
    S.key("ficelle", "from", f, 1, DRAW, "in")
    kit.move("livre", f, list(LIVRE_S10), scale=LIVRE_S10_K)
    kit.fade("livre_titre", f, to=0)
    S.key("livre_titre", "scale", f + FADE, 0)

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

    f = kit.at("S10", "indice", "les trois livres battent l'un après l'autre")
    kit.stagger(LIVRES, f, 3, kit.pulse, peak=round(LIVRE_S10_K * 1.08, 4))

    f = kit.at("S10", "règles.", "sur la page gauche de chaque livre, trois lignes de règles à puce s'écrivent")
    for k in range(3):
        for lid in LIVRES:
            kit.draw(f"{lid}_regle{k + 1}", f + 3 * k, DRAW)
            kit.pop(f"{lid}_puce{k + 1}", f + 3 * k, d=6)

    # ================= S11 : le MSCI World couvre les pays développés, pas les émergents =================
    f = kit.at("S11", "Le", "« Monde » rentre dans l'étiquette ; « États-Unis », « Tech » et leurs livres se "
                            "réduisent sur place ; le livre de « Monde » grandit au centre")
    kit.vanish("nom_monde", f, into="etiquette")
    for k, nid in enumerate(NOM_IDS):
        _wire_out(S, f"fil_{nid}", f)
    for k, nid in enumerate(NOM_IDS[1:]):
        kit.vanish(nid, f + 4 * k)
        kit.vanish(NOM_LIVRE[nid], f + 4 * k)
    kit.move("livre", f, list(LIVRE_S11), scale=LIVRE_S11_K)

    f = kit.at("S11", "MSCI", "le titre « MSCI World » s'écrit au-dessus du livre")
    kit.type("livre_msci", f, rate=1)

    f = kit.at("S11", "exemple,", "le panier, ses titres et l'étiquette se rangent en bas à gauche, plus petits ; "
                                  "« Toi » reste à sa place")
    kit.move("panier", f, list(PANIER_S11), scale=PANIER_S11_K)
    kit.move("etiquette", f, list(ETIQ_S11), scale=PANIER_S11_K)

    f = kit.at("S11", "couvre", "un fil sort du livre vers la 1re règle ; la pointe du stylo de « Toi » parcourt la "
                                "ligne pendant que « pays développés » s'écrit ; sa coche pleine se trace au début")
    for a, b in REGLE_LIGNE:
        assert_reach(P1[0], a, "S11 début de règle")
        assert_reach(P1[0], b, "S11 fin de règle")
    toi.reach(f - 8, list(REGLE_LIGNE[0][0]), d=8)
    kit.draw("fil_livre_regle", f, DRAW)
    n1 = len(S.ents["regle1"]["p"]["text"])
    toi.trace(f, REGLE_LIGNE[0], d=14)
    kit.type("regle1", f, rate=n1 / 14)
    kit.draw("regle1_coche", f, 6)

    f = kit.at("S11", "développés,", "le stylo touche la coche ; un fil cyan profond en part vers les titres du "
                                     "panier, qui battent tous en vague")
    hit = toi.tap(f - TAP + 1, list(REGLE_LIGNE[0][0]))
    kit.draw("fil_regle_titres", hit, DRAW)
    kit.stagger(_panier_titres(), hit + 5, 2, kit.pulse, peak=1.15)

    f = kit.at("S11", "mais", "la pointe passe à la 2e ligne et la parcourt pendant que « pays émergents » s'écrit")
    toi.reach(f - 5, list(REGLE_LIGNE[1][0]), d=5)
    n2 = len(S.ents["regle2"]["p"]["text"])
    toi.trace(f, REGLE_LIGNE[1], d=14)
    kit.type("regle2", f, rate=n2 / 14)

    f = kit.at("S11", "émergents.", "trois titres sortent du bout de la règle, sautent vers le panier, rebondissent "
                                    "sur ses titres et tombent par terre ; le stylo trace une croix devant la règle")
    for k, e in enumerate(EMERGENTS):
        g = f + 2 * k
        kit.pop(e, g, d=6)
        hit_e = kit.move(e, g, list(EMERG_HIT[k]), d=8, e="in", arc=90)
        kit.shake(e, hit_e, amp=8)
        sol = EMERGENTS_SOL[k]
        kit.drop(e, hit_e + 3, d=9, to=list(sol), h=sol[1] - EMERG_HIT[k][1], dx=EMERG_HIT[k][0] - sol[0])
    hit = toi.tap(f + 8 - TAP + 1, list(REGLE_LIGNE[1][0]))
    kit.draw("regle2_croix", hit, 6)
    lower(toi, hit + 6)

    # ================= S12 : combien pèse chaque pays ? Le panier devient balance =================
    f = kit.at("S12", "Ça", "le livre rentre dans le disque 1 du repère, qui se coche ; règles, coche, croix, fils "
                            "et titres émergents se réduisent")
    kit.vanish("livre", f, into=list(DISQUE_PT[0]), d=MORPH)
    S.key("marqueur", "done0", f + MORPH - 3, 1, DRAW, "out")    # coche deep du disque, cachée sous le disque actif
    kit.draw("disque1_coche", f + MORPH - 3, DRAW)                  # coche papier visible sur le disque actif cyan
    g = f + 6
    for wid in ("fil_livre_regle", "fil_regle_titres"):
        _wire_out(S, wid, g)
    kit.morph(["regle1", "regle2", "regle1_coche", "regle2_croix", *EMERGENTS], [], g)

    f = kit.at("S12", "savoir", "« Toi » passe à droite ; le panier et son étiquette reviennent au centre, à taille "
                                "normale")
    walk_low(toi, f, P2[0], d=22)
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
    kit.vanish("disque1_coche", f, d=6)          # le disque actif part : la coche deep du disque 1 (done0) reste

    f = kit.at("S13", "croire", "trois ronds montent de la tête de « Toi » et sa bulle s'ouvre : une petite balance "
                                "à plat, jetons en miroir")
    for k in range(3):
        S.key(f"bulle2_rond{k + 1}", "pos", f + 2 * k - 1, list(BULLE2_RONDS_S13[k]))
        kit.pop(f"bulle2_rond{k + 1}", f + 2 * k, d=6)
    S.key("bulle2", "pos", f + 5, list(BULLE2_S13))
    kit.pop("bulle2", f + 6)

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

    f = kit.at("S15", "« Monde »", "un fil rouge se trace de l'étiquette au géant cyan du côté États-Unis")
    kit.draw("lien_rouge", f, DRAW)

    f = kit.at("S15", "américain.", "les cinq titres cyan et « ≈ 70 % » battent ensemble ; tenue")
    for k in CYAN_SEATS:
        kit.pulse(POIDS[k], f, peak=round(S14_R[k] / TITRE_R * 1.12, 4))
    kit.pulse("compteur", f, peak=1.12)
    assert f + 6 < scene_f0(S, "S16")
