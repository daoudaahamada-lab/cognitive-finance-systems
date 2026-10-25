"""V07, partie 3 : S16-S22, images 1949-2967 (erreur 3 : les doublons ; la chute : 3 questions, avant / après ; fin).
30 temps forts, 33,9 s.

ÉTAT D'ENTRÉE (etat_initial de S16, à épingler à 1948 : `kit.pin(f0 - 1, ENTRY_P3)`) : `balance` à -10° côté
États-Unis, ses `poids` rangés par pays (3 géants cyan r 32, 2 cyan r 18 à gauche ; 5 light r 17 à droite),
`lien_rouge` de « États-Unis » à l'`etiquette` (ETIQ_BAL), `compteur` « ≈ 70 % » rouge au-dessus de `pil_usa`,
`pil_autres` à droite ; repère sur 2 (done0 1) ; « Toi » en P2 (860), bras baissé.

Temps forts (image du mot) :
S16  Et@1949  voulant@1974  corriger@1983  aggrave@2010  choses.@2023
S17  Troisième@2046  empiler@2085  ETF@2108  ressemblent.@2138
S18  Monde,@2197  S&P@2252  Nasdaq ?@2337
S19  plusieurs@2381  mêmes@2403  lignes,@2463  pas@2489  diversification.@2504
S20  Le@2544  réflexe@2556  trois@2586  questions.@2593  indice ?@2629  dedans ?@2685  coûte@2723
S21  nom@2761  suffit@2769  composition,@2839  si.@2862
S22  Abonne-toi@2883  argent.@2929   (film : dernière image 2967)
Gestes secondaires (S.word_after) : S18 « ETF »@2224 (pb1 bat), « 500 »@2279 (l'étiquette sœur bat), « ETF »@2311
(pb2 bat).

Tour de revue 1 :
- S16 : « ≈ 70 % » et « États-Unis » montent en haut à gauche ; le petit panier naît sous la pointe avec son étiquette
  sœur VIERGE pendue à sa ficelle, se pose au bout clair de la planche et y tient 8 images (petit tremblé), puis
  glisse toute la planche jusqu'aux géants (d 9) ; bascule -10 -> -18°.
- S17 : « ≈ 70 % » et « États-Unis » se rangent dans le disque 2 du repère (« ×3 » sera le seul rouge) ; le second
  petit panier, lui aussi né avec son étiquette vierge, tombe sur le premier (d 9) ; bascule -25°, la planche cogne
  (shake y 6), le bout « autres pays » monte et sa pilule avec.
- S18 : les étiquettes sœurs ne font que s'écrire (« ETF S&P 500 », « ETF Nasdaq ») ; battements secondaires.
- S19 : les 3 géants prennent un pictogramme (A téléphone, B chariot, C cible) identique dans les trois contenants ;
  les trois A battent et un trait rouge en tirets les relie à « ×3 » ; la place vide (r 38, tirets cyan profond)
  est reliée à « autres pays », « Toi » la touche : elle bat deux fois et reste vide pendant que les 3 lignes de la
  liste battent.
- S20 : sorties en échelle + opacité vers le centre du panier (2 images d'écart) ; l'étiquette se pose au-dessus de la
  planche ; la planche revient à plat DANS le repli (aucune image à plat) ; les disques du repère se retournent un à
  un (livre, balance penchée, pièce cyan venue de l'étiquette ; « ? » sur chacun) ; la fiche (3 rangées, h 410)
  surgit à sa place sous le repère ; chaque réponse rend son disque cyan ; ligne 2 : puce mini-balance ; ligne 3 :
  « Frais par an : bas », pièce cyan face à 4 pièces grises barrées.
- S21 : la fiche se range dans le repère sur « nom » et revient avec le couvercle envolé ; coche du rebord x 72.
- S22 : tout sort en 4 images AVANT la carte de fin.
"""
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, SCALE, TILT  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401

from . import *  # noqa: F401,F403
from . import (BALANCE_C, COUVERCLE_LOCAL, CYAN, ETIQ_NQ_C, ETIQ_SP_C, PLANCHE_H, PLANCHE_W, MARKER_CX, MARKER_Y, DISQUE_PT, ENTRY_P3, ETIQ_BAL, ETIQ_H, ETIQ_LISTE, FICHE_S20, FIN_BUTTON, FIN_C,
               FIN_TAP, GEANTS, LIGHT, P1, P2, P_FIN, PANIER_BAL_C, PB1_SEAT, PB2_SEAT, PB_K, PB_NEE, PB_POSE,
               PIL_AUTRES_S16, PLACE_VIDE_R, PLACE_VIDE_X, POIDS, RED, T_ABONNER, TILTS, TITRE_R, TITRE_TOMBE,
               TITRES, TITRES_LOCAL, assert_reach, line, lower, ring, scene_f0, seat, walk_low)

FILM_END = 2967
BTN_K = round(112 / ETIQ_H, 4)
ETIQ_LISTE_X0 = ETIQ_LISTE[0][0] - 10
PB_HAUT = 50                                     # S16 : le petit panier tombe de 50 px sur le bout de la planche
PB2_ARC = 100
COMPTEUR_HAUT, PIL_USA_HAUT, HAUT_K = (200, 455), (200, 535), 0.7
COUVERCLE_FUITE = (-200, -150)
PANIER_S20 = (340, 1090)
ETIQ_S20 = (PANIER_S20[0], PANIER_S20[1] + 40)                                  # (340, 1130)
PANIER_NEE_S20 = (BALANCE_C[0], 1075)                                           # sur le pivot
ETIQ_TAP_S21 = (PANIER_S20[0] + 115, PANIER_S20[1] + 40)                        # (455, 1130)
COUVERCLE_TAP_S21 = (PANIER_S20[0] + 190, PANIER_S20[1] - 118)                  # (530, 972)
COCHE_S21 = (PANIER_S20[0] + 235, PANIER_S20[1] - 130)                          # (575, 960) : coche du rebord
LIVRE_VOL = (260, 430)
VERS_PANIER = (BALANCE_C[0], 1000)               # S20 « Le » : les éléments de S16-S19 rentrent vers le panier

_VISIBLES = [t if k != TITRE_TOMBE else "titre_neuf" for k, t in enumerate(TITRES)]
_R = [32, 18, 32, 18, 32, 17, 17, 17, 17, 17]
TITRES_S20 = {t: {"pos": [TITRES_LOCAL[k][0], -118 - _R[k] if k < 5 else -95 - _R[k]],
                  "scale": round(_R[k] / TITRE_R, 4), "fill": CYAN if k < 5 else LIGHT}
              for k, t in enumerate(_VISIBLES)}
GEANT_SAUT = _VISIBLES[2]


def _r(pt):
    return [round(pt[0], 3), round(pt[1], 3)]


def part(S, kit, c):
    toi, sheet = c.toi, c.sheet
    f0 = scene_f0(S, "S16")

    def _same_hex(i, k, v):                    # même couleur que la fin de p2, à la casse près : la garder
        if isinstance(v, str) and v.startswith("#") and k in S.ents[i]["t"]:
            cur = S.val(i, k, f0 - 2)
            return cur if isinstance(cur, str) and cur.lower() == v.lower() else v
        return v
    entry = {i: {k: _same_hex(i, k, v) for k, v in tr.items()} for i, tr in ENTRY_P3.items()}
    kit.pin(f0 - 1, {**entry,
                     "panier_couvercle": {"scale": 0},
                     "titre_questions": {"scale": 0},
                     "marqueur2": {"scale": 0, "on": 0},
                     "fiche": {"scale": 0},
                     "toi_nom": {"opacity": 0}})
    if S.val("toi", "scale", f0 - 1) == 0:      # partie construite seule : la figurine n'est pas entrée
        toi.enter(f0 - 10, at=list(P2))
        lower(toi, f0 - 1, d=1)
    if abs(S.val("toi", "pos", f0 - 1)[0] - P2[0]) > 0.5:
        walk_low(toi, f0 - 40, P2[0], d=30)
    kit.ensure("toi", "look", 0)

    def bal_world(local, n):
        return S.to_world("balance", list(local), n)

    assert_reach(P2[0], PB_NEE, "S16 pointe du petit panier", fig_y=P2[1])
    for pt, what in ((ETIQ_TAP_S21, "S21 étiquette"), (COUVERCLE_TAP_S21, "S21 couvercle"), (COCHE_S21, "S21 coche")):
        assert_reach(P1[0], pt, what)
    assert_reach(P_FIN[0], FIN_TAP, "S22 bouton", fig_y=P_FIN[1])

    # ================= S16 « Et c’est souvent en voulant corriger qu’on aggrave les choses. » =================
    f = kit.at("S16", "Et", "le fil rouge se retire et l'étiquette repend au pivot ; « ≈ 70 % » et « États-Unis » "
                            "montent en haut à gauche ; « autres pays » monte au-dessus du bout clair")
    S.key("lien_rouge", "from", f, 1, DRAW, "in")
    S.key("lien_rouge", "opacity", f + DRAW, 0)
    kit.draw("ficelle_etiq_bal", f + 4, DRAW)
    kit.move("pil_usa", f, list(PIL_USA_HAUT))
    kit.move("pil_autres", f, list(PIL_AUTRES_S16))
    kit.move("compteur", f, list(COMPTEUR_HAUT), scale=HAUT_K)

    f = kit.at("S16", "voulant", "« Toi » lève son stylo vers le bout clair de la planche")
    toi.reach(f, list(PB_NEE), d=POP)

    f = kit.at("S16", "corriger", "sous la pointe naît un petit panier plein de titres cyan, avec son étiquette sœur "
                                  "vierge pendue à une ficelle ; il se pose sur le bout clair de la planche et y "
                                  "tient, en équilibre")
    above = [PB_POSE[0], PB_POSE[1] - PB_HAUT]
    g = kit.pop("pb1", f, scale=PB_K, from_pt=list(PB_NEE), to=above, d=6)
    land = kit.drop("pb1", g, h=PB_HAUT, d=7, to=list(PB_POSE))
    kit.pop("etiq_sp", f + 2, from_pt="pb1", to=list(ETIQ_SP_C), d=MORPH)
    kit.draw("ficelle_etiq_sp", f + 6, DRAW)
    kit.ensure("pb1", "rot", 0)
    for k, r in enumerate((4, -3, 2, 0)):        # tient 8 images : petit tremblé d'équilibre
        S.key("pb1", "rot", land + 2 * k, r, 2, "inOut")
    lower(toi, f + 8)

    f = kit.at("S16", "aggrave", "le petit panier glisse sur toute la planche, du bout clair jusqu'aux géants cyan ; "
                                 "à son arrivée la balance penche nettement plus (-18°)")
    g = kit.move("pb1", f, list(PB1_SEAT), d=9, e="out")
    choses = S.word_after("choses.", f)
    S.key("balance", "rot", g - 4, TILTS["S16"], 8, "out")
    assert g - 4 + 8 <= choses, (g, choses)

    f = kit.at("S16", "choses.", "« ≈ 70 % » et « États-Unis » battent ensemble ; tenue")
    kit.pulse("compteur", f, peak=round(HAUT_K * 1.15, 4))
    kit.pulse("pil_usa", f)

    # ================= S17 « Troisième erreur : empiler des ETF qui se ressemblent. » =================
    f = kit.at("S17", "Troisième", "le repère passe au 3 « Doublons » ; le disque 2 se coche et « ≈ 70 % » et "
                                   "« États-Unis » s'y rangent")
    kit.step(f, 2)
    S.key("marqueur", "done1", f + 4, 1, DRAW, "out")
    kit.vanish("compteur", f, into=list(DISQUE_PT[1]), d=MORPH)
    kit.vanish("pil_usa", f + 2, into=list(DISQUE_PT[1]), d=MORPH)

    f = kit.at("S17", "empiler", "un second petit panier, avec son étiquette sœur vierge, naît sous la pointe et "
                                 "tombe sur le premier : empilés ; la balance penche à -25°, le bout bas cogne, le "
                                 "bout « autres pays » monte")
    toi.reach(f - POP, list(PB_NEE), d=POP)
    here = _r(S.parent_space("pb2", list(PB_NEE), f - 1))
    g = kit.pop("pb2", f, scale=PB_K, from_pt=list(PB_NEE), to=here, d=6)
    kit.pop("etiq_nq", f + 2, from_pt="pb2", to=list(ETIQ_NQ_C), d=MORPH)
    kit.draw("ficelle_etiq_nq", f + 6, DRAW)
    land = kit.move("pb2", g, list(PB2_SEAT), d=9, e="in", arc=PB2_ARC)
    end_before = bal_world([PLANCHE_W / 2, -PLANCHE_H], land - 3)
    S.key("balance", "rot", land - 2, TILTS["S17"], 8, "out")
    kit.shake("balance", land + 6, amp=6, axis="y")
    end_after = S.to_world("balance", [PLANCHE_W / 2, -PLANCHE_H], land + 8)
    x, y = S.val("pil_autres", "pos", land - 3)
    kit.move("pil_autres", land - 2, [x, round(y + end_after[1] - end_before[1], 2)], d=8, e="out")
    lower(toi, g + 2)

    f = kit.at("S17", "ETF", "les deux petits paniers battent l'un après l'autre")
    kit.stagger(["pb1", "pb2"], f, 4, kit.pulse, peak=round(PB_K * 1.15, 4))

    f = kit.at("S17", "ressemblent.", "les 3 géants de la planche et ceux des deux petits paniers battent ensemble : "
                                      "les mêmes")
    planche_geants = [POIDS[k] for k in GEANTS]
    pb_geants = [f"{pb}_geant{k + 1}" for pb in ("pb1", "pb2") for k in range(3)]
    for gid in planche_geants + pb_geants:
        kit.pulse(gid, f, peak=round(S.val(gid, "scale", f - 1) * 1.2, 4))

    # ================= S18 « Un ETF Monde, un ETF S&P 500 et un ETF Nasdaq ? » =================
    f = kit.at("S18", "Monde,", "l'étiquette « ETF Monde » bat")
    kit.pulse("etiquette", f, peak=1.18)
    g = S.word_after("ETF", f)                   # « un ETF S&P 500 » : le petit panier du bas bat
    kit.pulse("pb1", g, peak=round(PB_K * 1.12, 4))

    f = kit.at("S18", "S&P", "l'étiquette vierge du petit panier du bas s'écrit : « ETF S&P 500 »")
    kit.type("etiq_sp_txt", f, rate=1.6)
    kit.pulse("etiq_sp", S.word_after("500", f), peak=1.15)
    g = S.word_after("ETF", f + 30)              # « et un ETF Nasdaq » : le petit panier du haut bat
    kit.pulse("pb2", g, peak=round(PB_K * 1.12, 4))

    f = kit.at("S18", "Nasdaq ?", "l'étiquette vierge du petit panier du haut s'écrit : « ETF Nasdaq » ; puis les "
                                  "deux étiquettes sœurs battent ensemble")
    done = kit.type("etiq_nq_txt", f, rate=1.6)
    for eid in ("etiq_sp", "etiq_nq"):
        kit.pulse(eid, done + 2, peak=1.12)

    # ================= S19 « Tu achètes plusieurs fois les mêmes grandes entreprises. Plus de lignes, … » =========
    f = kit.at("S19", "plusieurs", "les géants battent en trois temps : sur la planche, dans le petit panier du bas, "
                                   "dans celui du haut")
    for k, grp in enumerate((planche_geants, pb_geants[:3], pb_geants[3:])):
        for gid in grp:
            kit.pulse(gid, f + 5 * k, peak=round(S.val(gid, "scale", f - 1) * 1.25, 4))

    f = kit.at("S19", "mêmes", "chaque géant prend son pictogramme (A, B, C), le même dans les trois contenants ; les "
                               "trois A battent ensemble, un trait rouge en tirets les relie à « ×3 » rouge")
    for k in range(3):
        kit.pop(f"{POIDS[GEANTS[k]]}_p", f + k, d=6)
        for pb in ("pb1", "pb2"):
            kit.pop(f"{pb}_geant{k + 1}_p", f + k, d=6)
    a_ids = [f"{POIDS[GEANTS[0]]}_p", "pb1_geant1_p", "pb2_geant1_p"]
    pts = [S.to_world(i, [0, 0], f + 8) for i in a_ids]
    pts.sort(key=lambda p: -p[1])                # du bas (planche) vers le haut (petit panier du haut)
    top = [round(pts[-1][0] + 10, 1), round(pts[-1][1] - 110, 1)]
    S.key("fois3", "pos", f + 7, top)
    kit.pop("fois3", f + 8)
    rel = [[round(p[0] - top[0], 1), round(p[1] - top[1], 1)] for p in pts] + [[0, 30]]
    line(kit, "lien_x3", rel, color=RED, sw=5, z=11.9, dash=[12, 9], pos=top)
    kit.draw("lien_x3", f + 8, 9)
    for i in a_ids:
        kit.pulse(i, f + 8, peak=1.25)

    f = kit.at("S19", "lignes,", "les ficelles se retirent ; les trois étiquettes se rangent en liste à droite, sous "
                                 "« 3 ETF » : les lignes d'un portefeuille")
    for wid in ("ficelle_etiq_bal", "ficelle_etiq_sp", "ficelle_etiq_nq"):
        S.key(wid, "from", f, 1, 6, "in")
        S.key(wid, "opacity", f + 6, 0)
    dests = [(ETIQ_LISTE_X0, ETIQ_LISTE[0][1]), ETIQ_LISTE[1], ETIQ_LISTE[2]]
    for k, (eid, to) in enumerate(zip(("etiquette", "etiq_sp", "etiq_nq"), dests)):
        kit.move(eid, f + 2 + 4 * k, list(to), d=14)
    kit.pop("liste_titre", f + 8)

    f = kit.at("S19", "pas", "« Toi » pointe son stylo vers le bout clair de la planche, à côté des titres clairs")
    vide = S.to_world("balance", seat(PLACE_VIDE_X, PLACE_VIDE_R), f)
    assert_reach(P2[0], vide, "S19 place vide", fig_y=P2[1])
    toi.reach(f, [vide[0] + 8, vide[1] - 30], d=POP)

    f = kit.at("S19", "diversification.", "une grande place ronde en tirets surgit au bout de la planche, reliée à "
                                          "« autres pays » ; « Toi » la touche : elle bat deux fois et reste VIDE, "
                                          "pendant que les trois lignes de la liste battent une fois")
    kit.pop("place_vide", f)
    kit.draw("fil_vide", f + 2, 7)
    hit = toi.tap(f + 1, [vide[0] + 8, vide[1] - PLACE_VIDE_R + 6])
    kit.pulse("place_vide", hit, times=2, peak=1.3, step=3)
    for k, eid in enumerate(("etiquette", "etiq_sp", "etiq_nq")):
        kit.pulse(eid, hit + 1, peak=1.12)
    lower(toi, hit + 6)

    # ================= S20 « Le bon réflexe tient en trois questions. Quel indice ? … » =================
    f = kit.at("S20", "Le", "les petits paniers, les étiquettes sœurs, « ×3 », « 3 ETF », la place vide et "
                            "« autres pays » rentrent l'un après l'autre vers le centre ; « ETF Monde » quitte la "
                            "liste et se pose au-dessus du pivot")
    outs = ["pb1", "pb2", "etiq_sp", "etiq_nq", "fois3", "lien_x3", "liste_titre", "place_vide", "fil_vide",
            "pil_autres"]
    for k, o in enumerate(outs):
        g = f + 2 * (k // 2)
        S.key(o, "pos", g, _r(S.parent_space(o, list(VERS_PANIER), g)), 8, "in")
        S.key(o, "scale", g, 0, 8, "in")
        S.key(o, "opacity", g, 0, 8, "in")
    kit.move("etiquette", f, [PANIER_BAL_C[0], PANIER_BAL_C[1] + 40], d=10)

    f = kit.at("S20", "réflexe", "la balance se replie (la planche revient à plat en se repliant) et le panier ouvert "
                                 "en renaît : ses titres y retombent avec leurs couleurs et leurs tailles ; "
                                 "l'étiquette se pose sur le devant du panier ; « Toi » revient à gauche")
    for t, st in TITRES_S20.items():
        S.key(t, "pos", f - 1, st["pos"])
        S.key(t, "scale", f - 1, st["scale"])
        S.key(t, "fill", f - 1, st["fill"])
        S.key(t, "opacity", f - 1, 1)
    S.key("balance", "rot", f, 0, MORPH, "out")
    kit.vanish("balance", f, d=MORPH)
    S.key("panier", "pos", f - 1, list(PANIER_NEE_S20))
    g = kit.pop("panier", f, scale=1, d=MORPH)
    arr = kit.move("panier", g, list(PANIER_S20))
    kit.move("etiquette", f, list(ETIQ_S20), d=arr - f)
    kit.draw("ficelle_etiq", arr - 6)
    walk_low(toi, f, P1[0], d=arr - f)

    f = kit.at("S20", "trois", "« 3 erreurs » devient « 3 questions » ; les disques du repère se retournent un à un : "
                               "un livre, une balance penchée, une pièce (venue de l'étiquette), chacun avec son « ? » ; "
                               "les légendes deviennent Indice · Pays · Frais")
    kit.morph(["titre_erreurs"], ["titre_questions"], f)
    S.key("marqueur", "lbl", f, 0, 4, "out")
    for k in range(3):
        n = f + 4 * k
        qd = f"qd{k + 1}"
        S.key(qd, "sx", n - 1, 0)
        S.key(qd, "opacity", n, 1)
        S.key(qd, "sx", n, 1, 5, "out")
    sw = f + 12
    S.key("marqueur", "scale", sw, 0)
    S.key("marqueur2", "pos", sw - 1, [MARKER_CX, MARKER_Y])
    S.key("marqueur2", "lbl", sw - 1, 0)
    S.key("marqueur2", "scale", sw, 1)
    S.key("marqueur2", "lbl", sw + 1, 1, FADE, "out")
    g = kit.pop("frais_etf", f + 6, from_pt="etiquette", to=[ETIQ_S20[0] + 150, ETIQ_S20[1] - 70], d=6)
    g = kit.move("frais_etf", g, list(DISQUE_PT[2]), d=12, arc=60)
    kit.vanish("frais_etf", g, d=4)
    kit.pop("qd3_piece", g, scale=1, d=5)

    f = kit.at("S20", "questions.", "la fiche « Composition » à trois lignes vides surgit sous le repère et "
                                    "descend à sa place")
    g = kit.pop("fiche", f, scale=1, from_pt=[FICHE_S20[0], 440], to=list(FICHE_S20), d=10)
    fiche_ok = g

    def bullet(i):
        return _r(sheet.world(S, i, "bullet", n=fiche_ok))

    def answer(i, g, src, bullet_on=True):
        kit.vanish(src, g, into=bullet(i), d=5)
        kit.vanish(f"fiche_tirets{i + 1}", g, d=5)
        if bullet_on:
            S.key(c.lignes[i], "bulletOn", g + 3, 1)
        return kit.type(c.lignes[i], g + 3, flash=bullet_on)

    def answered(k, n):
        qd = f"qd{k + 1}"
        S.key(qd, "fill", n, CYAN, 6, "out")
        kit.vanish(f"{qd}_q", n, d=6)
        kit.pulse(qd, n, peak=1.15)

    f = kit.at("S20", "indice ?", "disque 1 : son « ? » disparaît, il devient cyan ; le livre ressort du disque 1, file "
                                  "vers la 1re ligne et devient sa puce : « Indice : MSCI World » s'écrit")
    answered(0, f)
    for lid in ["livre"] + [i for i, e in S.ents.items() if e.get("parent") == "livre"]:
        z0 = S.ents[lid]["z"]
        kit.ensure(lid, "z", z0)
        S.key(lid, "z", f, z0 + 4)
    g = kit.pop("livre", f, scale=0.4, from_pt=list(DISQUE_PT[0]), to=list(LIVRE_VOL))
    g = kit.move("livre", g, bullet(0), d=12, scale=0.12)
    answer(0, g, "livre")

    f = kit.at("S20", "dedans ?", "disque 2 : son « ? » disparaît, il devient cyan ; une copie d'un géant cyan saute du "
                                  "panier jusqu'à la 2e ligne, dont la puce devient une mini balance penchée : "
                                  "« États-Unis : ≈ 70 % » s'écrit")
    answered(1, f)
    S.key("saut_geant", "pos", f - 1, _r(S.to_world(GEANT_SAUT, [0, 0], f - 1)))
    S.key("saut_geant", "scale", f - 1, round(S.world_scale(GEANT_SAUT, f - 1) * TITRE_R / 32, 4))
    S.key("saut_geant", "opacity", f - 1, 1)
    g = kit.move("saut_geant", f, bullet(1), arc=80, scale=0.6)
    kit.pop("fiche_bal_disc", g + 1, d=6)
    answer(1, g, "saut_geant", bullet_on=False)

    f = kit.at("S20", "coûte", "disque 3 : son « ? » disparaît, il devient cyan ; la pièce cyan en ressort et file "
                               "vers la 3e ligne, dont elle devient la puce : « Frais par an : bas » s'écrit, la pièce "
                               "cyan face à quatre pièces grises barrées")
    answered(2, f)
    S.key("frais_etf", "pos", f - 1, list(DISQUE_PT[2]))
    S.key("frais_etf", "opacity", f - 1, 1)
    g = kit.pop("frais_etf", f, scale=0.8, d=6)
    g = kit.move("frais_etf", g, bullet(2), d=12, scale=0.8)
    done = answer(2, g, "frais_etf")
    kit.pop("cmp_cyan", done, d=6)
    for j in range(4):
        kit.pop(f"cmp_gris{j + 1}", done + 2 + j, d=5)
    kit.draw("cmp_barre", done + 8, 6)

    # ================= S21 « Un nom ne suffit pas à savoir ce que tu achètes. La composition, si. » =============
    f = kit.at("S21", "nom", "le couvercle retombe sur le panier et cache les titres ; la fiche se range dans le "
                             "repère : on ne voit plus que l'étiquette « ETF Monde »")
    kit.drop("panier_couvercle", f, h=70, d=7, to=list(COUVERCLE_LOCAL))
    for t in TITRES_S20:
        x, y = TITRES_S20[t]["pos"]
        S.key(t, "pos", f + 1, [x, y + 24], 4, "in")
        S.key(t, "scale", f + 1, 0, 4, "in")
    kit.move("fiche", f, [MARKER_CX, MARKER_Y + 10], d=10, e="inOut", scale=0.05)
    S.key("fiche", "scale", f + 10, 0)

    f = kit.at("S21", "suffit", "« Toi » touche l'étiquette : elle tremble, rien n'en sort")
    hit = toi.tap(f - TAP + 1, list(ETIQ_TAP_S21))
    kit.shake("etiquette", hit, amp=8)
    lower(toi, hit + 6)

    f = kit.at("S21", "composition,", "« Toi » touche le couvercle : il s'envole en haut à gauche ; les titres "
                                      "colorés réapparaissent et la fiche « Composition », remplie, redescend du repère")
    hit = toi.tap(f - TAP + 1, list(COUVERCLE_TAP_S21))
    kit.ensure("panier_couvercle", "z", S.ents["panier_couvercle"]["z"])
    kit.ensure("panier_bouton", "z", S.ents["panier_bouton"]["z"])
    S.key("panier_couvercle", "z", hit, 9)
    S.key("panier_bouton", "z", hit, 9.1)
    kit.move("panier_couvercle", hit, list(COUVERCLE_FUITE), d=MORPH, e="out", arc=60)
    kit.vanish("panier_couvercle", hit, d=MORPH)
    for k, (t, st) in enumerate(TITRES_S20.items()):
        S.key(t, "pos", hit + 1, st["pos"])
        kit.pop(t, hit + 1 + k // 3, scale=st["scale"])
    kit.pop("fiche", hit + 1, scale=1, from_pt=[MARKER_CX, MARKER_Y + 10], to=list(FICHE_S20), d=10)
    lower(toi, hit + 6)

    f = kit.at("S21", "si.", "« Toi » touche le bord du panier : une grande coche pleine s'y trace ; tenue")
    hit = toi.tap(f - TAP + 1, list(COCHE_S21))
    kit.draw("panier_coche", hit)
    lower(toi, hit + 6)

    # ================= S22 « Abonne-toi pour comprendre ton argent. » =================
    glide = MOVE
    out = kit.outro("S22", outs=[], btn_at=glide, press="argent.", pos=FIN_C, bsize=round(34 * BTN_K, 1),
                    labelSize=34)
    for o in ("panier", "fiche", "marqueur2", "titre_questions", "qd1", "qd2", "qd3"):
        S.key(o, "scale", out["card"] - 2, 0, 4, "in")    # tout sort en 4 images AVANT la carte : aucune image
        S.key(o, "opacity", out["card"] + 2, 0)           # commune avec la carte qui grandit
    f = out["card"]
    S.set(out["cursor"], opacity=0)
    S.key("ficelle_etiq", "draw", f - 2, 0, 4, "in")
    kit.ensure("etiquette", "z", S.ents["etiquette"]["z"])
    S.key("etiquette", "z", f, 41)
    kit.ensure("etiquette", "textOp", 1)
    S.key("etiquette", "textOp", f, 0, 4, "out")
    S.key("etiquette", "text", f + 4, T_ABONNER)
    S.key("etiquette", "textOp", f + 4, 1, FADE, "out")
    S.key("etiquette", "w", f, round(380 / BTN_K, 2), glide, "inOut")
    kit.move("etiquette", f, list(FIN_BUTTON), d=glide, e="inOut", scale=BTN_K)
    S.key("etiquette", "opacity", f + glide, 0)
    walk_low(toi, f, P_FIN[0])

    fp = out["press"]
    toi.set_z(fp - TAP - 12, S.ents[toi.id]["z"], tool_z=44)
    toi.reach(fp - TAP - 10, [FIN_TAP[0] + 10, FIN_TAP[1] + 40], d=10)
    hit = toi.tap(fp - TAP + 1, list(FIN_TAP))
    for k in range(2):
        ring(S, f"fin_onde{k + 1}", hit + 4 * k, d=14, s0=0.6, s1=2.0)
    end = lower(toi, hit + 6, 8)
    assert hit == fp and end < FILM_END and hit + 4 + 14 < FILM_END, (hit, fp, end)
