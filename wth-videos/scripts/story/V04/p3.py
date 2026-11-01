"""V04, partie 3 : S15-S21, images 1700-2670. Piège 3 : « Toi » se retourne et revient au téléphone ; sa pensée (trois
petits ronds) pose une pièce fantôme en tirets dans la place vide de c8, cochée ; deux blocs plats séparés d'un vide
encre ; le virement avance jusqu'au bord et attend (horloge dont l'aiguille tourne, la pièce se penche vers le vide
et revient), « Remboursement », « Salaire » ; la place d'arrivée reste vide ; « Toi » barre la pièce fantôme d'une
grande croix : elle sort du téléphone, sa place reste vide. La méthode : rembobinage (◀◀), les 7 pièces reviennent ;
le stylo de « Toi » touche chaque place : le « − » sort de sa pointe, le bac (c1-c6) puis le sablier (c8) ; c7 seule,
cerclée, « = » devant elle ; tout se rassemble en « 2 min », logé dans une case sur sept, et la semaine suivante
encore. La décision : le fil vers « 800 € » barré, le fil plein du panier vers c7. La carte de fin.

Temps forts :
S15  l’inverse,@1705  crois@1758  avoir.@1773
S16  Troisième@1798  compter@1837  virement@1862  pas@1878  arrivé.@1895
S17  remboursement@1924  salaire@1974  toi.@2033  Tant@2054  crédité,@2078  ne@2099  pas.@2118
S18  La@2138  solde@2175  moins@2205  venir,@2235  paiements@2270  différés.@2281
S19  reste,@2320  utiliser.@2382  Deux@2414  une@2438  semaine.@2452
S20  Et@2479  décide@2487  jamais@2508  dépense@2524
S21  Abonne-toi@2579  argent.@2632
"""
import math

from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP  # noqa: F401
from pipeline.story_kit import TAP

from . import (BAC_COINS, BAC_S18, BAC_S18_K, CARTE_S18, CARTE_S18_K, COIN_K, COIN_PLACES, CYAN, DECISION_STRIKE,
               ENTRY_P3, FIN_BUTTON, FIN_TAP, FUSION, GHOST, HEAD_DY, HORLOGE_VIR_K, HORLOGE_VIREMENT, MARKER_DISC,
               MARQ_OVER, MOINS_C, P1, P2, PANIER_S20, REMBOBINER_S18, SABLIER_IN_S18, SEM1, SEM2, SEMAINE_CASES,
               SEMAINE_CASES2, SOLDE_BTN_SCALE, T_ABONNER, TAP_MOINS, TAP_SABLIER_S18, VIREMENT_STOP, COUPES,
               assert_reach, ring,
               scene_f0, turn)
from .p2 import marker_done, marker_leave, tick_clock

SOLDE_TXT_SIZE = 48
BTN_SIZE = round(SOLDE_TXT_SIZE * SOLDE_BTN_SCALE, 1)   # 64 : le relais pilule -> bouton ne saute pas
PENSEE = ["pensee1", "pensee2", "pensee3"]


def _head(S, n):
    return S.to_world("toi", [0, HEAD_DY], n)


def wait_beat(S, kit, f):
    """Le virement attend : l'aiguille de son horloge tourne d'un quart de tour ; la pièce se penche vers le vide et
    revient, sans le franchir."""
    tick_clock(S, f)
    x, y = S.val("virement", "pos", f - 1)
    S.keys("virement", f, 5, "out", pos=[x - 9, y], rot=-14)
    S.keys("virement", f + 5, 7, "inOut", pos=[x, y], rot=0)


def part(S, kit, c):
    toi, dos = c.toi, c.dos
    f0 = scene_f0(S, "S15")
    kit.pin(f0 - 1, ENTRY_P3)
    f_end = math.ceil(S.sb["scenes"][-1]["t_end"] * S.fps)   # dernière image du film

    # ================= S15 : l'argent qu'il croit déjà avoir =================
    f = kit.at("S15", "l’inverse,", "le miroir et la tirelire se réduisent lentement, leurs fils se retirent ; « Toi » "
                                    "se retourne vers le téléphone et revient près de lui")
    kit.vanish("miroir", f, d=MORPH)
    kit.vanish("tirelire", f, d=MORPH)
    for w in ("preuve_solde", "preuve_piece"):
        S.key(w, "draw", f + 4, 0, MORPH, "inOut")
    g = turn(S, dos, toi, f)
    toi.walk(g, P2, d=24)

    g = S.word_after("l’argent", f)
    for k, pid in enumerate(PENSEE):
        kit.pop(pid, g + 3 * k)

    f = kit.at("S15", "crois", "au bout des trois petits ronds de sa pensée, une pièce en tirets se pose dans la "
                               "place vide de c8, DANS le téléphone : il la compte déjà")
    kit.pop("fantome", f)
    S.key("case8", "opacity", f, 0)                      # la pièce fantôme prend la place (un seul cercle en tirets)
    toi.stow(f)                                          # il pense : le stylo est rangé, rien ne gêne sa pensée

    f = kit.at("S15", "avoir.", "une coche pleine se trace à côté de la pièce en tirets : pour lui, c'est sûr")
    kit.draw("fantome_coche", f, DRAW)

    # ================= S16 : troisième piège, le virement pas encore arrivé =================
    f = kit.at("S16", "Troisième", "le disque actif du repère glisse sur 3 (« Virements ») ; le disque 2 reste coché")
    marker_leave(S, kit, f, 1)
    kit.step(f, 2)

    f = kit.at("S16", "compter", "deux blocs tombent à droite du téléphone, séparés par un vide noir")
    kit.drop("vide", f, h=160)

    f = kit.at("S16", "virement", "une pièce surgit au bout du bloc lointain ; un trait en tirets montre où elle doit "
                                  "aller : le bord du téléphone")
    kit.pop("virement", f)
    kit.draw("vire_fil", f + 4, DRAW)

    f = kit.at("S16", "pas", "la pièce avance jusqu'au bord du vide et s'y arrête")
    kit.move("virement", f, list(VIREMENT_STOP), d=14, e="inOut")

    f = kit.at("S16", "arrivé.", "l'horloge sort de la pièce et se pose sur son coin : il est en route")
    S.key("horloge", "opacity", f, 1)
    kit.pop("horloge", f, scale=HORLOGE_VIR_K, from_pt="virement", to=HORLOGE_VIREMENT)

    # ================= S17 : remboursement, salaire, pas encore à toi =================
    f = kit.at("S17", "remboursement", "l'étiquette « Remboursement » surgit au-dessus du virement ; l'aiguille tourne, "
                                       "la pièce se penche vers le vide et revient")
    kit.pop("etiq_remb", f)
    wait_beat(S, kit, f)

    f = kit.at("S17", "salaire", "l'étiquette « Salaire » surgit au-dessus ; l'aiguille tourne, la pièce attend")
    kit.pop("etiq_sal", f)
    wait_beat(S, kit, f)

    f = kit.at("S17", "toi.", "la pièce en tirets du téléphone bat deux fois ; le vrai virement reste derrière le vide")
    kit.pulse("fantome", f, times=2, peak=1.3)
    wait_beat(S, kit, f)

    f = kit.at("S17", "Tant", "au bord du téléphone, une place vide en tirets apparaît : là où la pièce arrivera")
    kit.pop("case_arrivee", f)
    wait_beat(S, kit, f)

    f = kit.at("S17", "crédité,", "la place d'arrivée bat deux fois et reste vide ; le virement ne bouge pas")
    g = kit.pulse("case_arrivee", f, times=2, peak=1.15)
    toi.unstow(f)
    gx, gy = GHOST
    a1, b1, a2, b2 = [gx - 27, gy - 27], [gx + 27, gy + 27], [gx + 27, gy - 27], [gx - 27, gy + 27]
    for p in (a1, b1, a2, b2):
        assert_reach(P2[0], p, "S17 croix")
    toi.reach(g, a1, d=max(3, S.word_after("ne", g) - g))

    f = kit.at("S17", "ne", "« Toi » barre la pièce en tirets d'une grande croix")
    e1 = toi.strike(f, a1, b1, d=4, lead=2, line="fantome_x1", track="draw")
    e2 = toi.strike(e1, a2, b2, d=4, lead=3, line="fantome_x2", track="draw")
    toi.rest(e2 + 1)

    f = kit.at("S17", "pas.", "ses petits ronds de pensée rentrent dans sa tête ; la pièce barrée sort du téléphone, "
                              "sa place reste vide")
    head = _head(S, f - 1)
    for pid in PENSEE:
        kit.vanish(pid, f, into=head)
    g = max(e2 + 15, f + 6)
    kit.vanish("fantome", g, d=6)
    S.key("fantome_coche", "draw", g, 0, 4, "in")
    S.key("case8", "opacity", g + 5, 1)                  # la place de c8 reste vide
    assert g + 6 <= scene_f0(S, "S18") - 1, g

    # ================= S18 : la méthode, solde − bac − sablier, au stylo =================
    f = kit.at("S18", "La", "le vide, le virement, son horloge, les deux étiquettes et la place d'arrivée se rangent "
                            "dans le disque 3, qui se coche ; « Toi » repasse à droite")
    S.key("vire_fil", "draw", f, 0, 4, "in")
    for x in ["vide", "virement", "horloge", "etiq_remb", "etiq_sal", "case_arrivee"]:
        kit.vanish(x, f, into=list(MARKER_DISC[2]))
    marker_done(S, kit, f, 2)
    toi.walk(f, P1, d=24)

    f = kit.at("S18", "solde", "le ◀◀ revient au-dessus du téléphone : les 7 pièces remontent dans leurs places comme "
                               "au début ; la pilule « 800 € » bat")
    kit.pop("rembobiner", f, to=list(REMBOBINER_S18))
    back = [k for k in range(8) if k != 6]
    for j, k in enumerate(back):
        cid, (x, y) = c.coins[k], COIN_PLACES[k]
        g = f + 2 + 2 * j
        S.key(cid, "pos", g - 1, [x, 1250])
        S.key(cid, "scale", g - 1, 1)
        S.key(cid, "rot", g - 1, 0)
        S.key(cid, "opacity", g - 1, 0)
        kit.fade(cid, g, to=1, d=4)
        kit.move(cid, g, [x, y], d=12, e="out")
        S.key(c.cases[k], "opacity", g + 9, 0)
    kit.pulse("solde", f + 12, times=2, peak=1.12, step=4)
    kit.vanish("rembobiner", f + 2 + 2 * len(back) + 10)

    f = kit.at("S18", "moins", "le stylo de « Toi » touche à droite du téléphone : un « − » sort de sa pointe ; le bac "
                               "ressort du disque 1 et se pose à côté")
    assert_reach(P1[0], TAP_MOINS[0], "S18 moins 1")
    hit = toi.tap(f - TAP + 1, list(TAP_MOINS[0]))
    kit.pop("moins1", hit, from_pt=toi.tip(hit), to=MOINS_C[0])
    S.key("bac", "pos", hit + 1, list(MARKER_DISC[0]))
    S.key("bac", "scale", hit + 1, round(0.15 * BAC_S18_K, 4))
    S.key("bac", "opacity", hit + 1, 1)
    kit.move("bac", hit + 2, list(BAC_S18), MOVE, scale=BAC_S18_K)
    toi.rest(hit + 5)

    f = kit.at("S18", "venir,", "le stylo touche le bac : c1 à c6 quittent le téléphone et tombent dedans ; leurs "
                                "places redeviennent vides")
    hit = toi.tap(f - TAP + 1, list(TAP_MOINS[0]))
    for i in range(6):
        g = hit + 3 * i
        S.fly(c.coins[i], g, MOVE, "inOut", to=list(BAC_COINS[i]), scale=0.5, arc=60)
        kit.fade(c.cases[i], g, to=1)
    toi.rest(hit + 5)

    f = kit.at("S18", "paiements", "le stylo touche plus bas : un second « − » sort de sa pointe ; la carte et le "
                                   "sablier ressortent du disque 2 et se posent à côté")
    assert_reach(P1[0], TAP_MOINS[1], "S18 moins 2")
    hit = toi.tap(f - TAP + 1, list(TAP_MOINS[1]))
    kit.pop("moins2", hit, from_pt=toi.tip(hit), to=MOINS_C[1])
    S.key("carte_sablier", "pos", hit + 1, list(MARKER_DISC[1]))
    S.key("carte_sablier", "scale", hit + 1, round(0.15 * CARTE_S18_K, 4))
    S.key("carte_sablier", "opacity", hit + 1, 1)
    kit.move("carte_sablier", hit + 1, list(CARTE_S18), 10, e="out", scale=CARTE_S18_K)

    f = kit.at("S18", "différés.", "le stylo touche le sablier : c8 quitte le téléphone et entre dans son haut ; c7 "
                                   "reste seule")
    tgt = list(TAP_SABLIER_S18)
    assert_reach(P1[0], tgt, "S18 sablier")
    hit = toi.tap(f - TAP + 1, tgt)
    for cp in COUPES:
        S.key(cp, "draw", hit - 1, 0)
    S.fly("c8", hit, MOVE, "out", to=list(SABLIER_IN_S18), scale=0.45, arc=60)
    kit.fade("case8", hit, to=1)
    g = toi.rest(hit + 5)
    walk_end = toi.walk(g, P2, d=24)
    assert walk_end <= S.word_after("reste", f), walk_end

    # ================= S19 : ce qui reste, 2 min une fois par semaine =================
    f = kit.at("S19", "reste,", "c7, la seule pièce du téléphone, bat deux fois")
    kit.pulse("c7", f, times=2, peak=1.3)

    f = kit.at("S19", "utiliser.", "le stylo touche c7 : un anneau se trace autour d'elle et reste ; un « = » cyan "
                                   "profond se pose devant elle")
    assert_reach(P2[0], COIN_PLACES[6], "S19 c7")
    hit = toi.tap(f - TAP + 1, list(COIN_PLACES[6]))
    kit.draw("c7", hit, DRAW, track="ring")
    kit.pop("egal", hit + 2)
    toi.rest(hit + 6)

    f = kit.at("S19", "Deux", "le bac, le sablier, les deux « − » et leurs pièces glissent ensemble vers un même point "
                              "et s'y fondent en une pilule « 2 min », qui bat")
    for x in ["bac", "carte_sablier", "moins1", "moins2", *c.coins[:6], "c8"]:
        s = S.val(x, "scale", f - 1)
        kit.move(x, f, list(FUSION), d=12, e="inOut", scale=round(s * 0.55, 4))
        kit.vanish(x, f + 12, d=5)
    g = kit.pop("semaine_pill", f + 12)
    kit.pulse("semaine_pill", g, peak=1.2)

    f = kit.at("S19", "une", "sept cases vides se posent en rang ; « 1 fois par semaine » s'inscrit au-dessus")
    kit.stagger(SEM1, f, 2, kit.pop)
    kit.fade("semaine_txt", f + 4, to=1)

    f = kit.at("S19", "semaine.", "la pilule « 2 min » descend dans la première case, qui devient cyan ; un cadre "
                                  "balaie les six autres cases, puis la semaine suivante pose sa première case cyan")
    kit.vanish("semaine_pill", f, into=list(SEMAINE_CASES[0]), d=8)
    S.key("semaine_case1", "fill", f + 6, CYAN, 6, "out")
    kit.pop("semaine_balai", f + 8, d=4)
    S.key("semaine_balai", "pos", f + 10, list(SEMAINE_CASES[6]), 10, "linear")
    kit.stagger(SEM2, f + 10, 1, kit.pop, d=6)
    S.key("semaine_balai", "pos", f + 20, list(SEMAINE_CASES2[0]), 6, "inOut")
    S.key("semaine2_case1", "fill", f + 24, CYAN, 6, "out")
    kit.vanish("semaine_balai", f + 28, d=6)

    # ================= S20 : ne décide plus sur le chiffre affiché =================
    f = kit.at("S20", "Et", "un panier sort du stylo de « Toi », qui revient à droite")
    kit.pop("panier", f, from_pt=toi.tip(f - 1), to=PANIER_S20)
    g = toi.walk(f, P1, d=16)

    f = kit.at("S20", "décide", "un fil en tirets se trace du panier vers la pilule « 800 € »")
    kit.draw("decision_tirets", f, DRAW)
    a, b = DECISION_STRIKE
    assert_reach(P1[0], a, "S20 rature")
    fj = S.word_after("jamais", f)
    toi.reach(g, list(a), d=max(3, fj - g))

    f = kit.at("S20", "jamais", "« Toi » barre le fil en tirets ; il se détend et rentre dans « 800 € »")
    end = toi.strike(f, list(a), list(b), line="decision_barre", track="draw")
    S.key("decision_tirets", "sag", end, 40, DRAW, "inOut")
    S.key("decision_tirets", "from", end, 1, DRAW, "inOut")
    kit.fade("decision_barre", end + 5, to=0)

    f = kit.at("S20", "dépense", "un fil plein part du panier et se pose sur la pièce cerclée c7, qui bat. Tenue")
    kit.draw("decision_plein", f, DRAW)
    kit.pulse("c7", f + DRAW, peak=1.15)
    toi.rest(f)

    # ================= S21 : la carte de fin, la pilule devient « S’abonner » =================
    f_card = kit.S.word_after("Abonne-toi", f)
    S.key("marqueur", "active", f_card - 1, 1.999)       # disque actif sans chiffre : aucun « 3 » sous la coche
    outs = ["appli", "c7", "egal", "panier", "decision_tirets", "decision_barre", "decision_plein", *SEM1, *SEM2,
            "semaine_txt", "marqueur", *[x for pair in MARQ_OVER for x in pair]]
    out = kit.outro("S21", mot="Abonne-toi", outs=outs, press="argent.", clear="fade", card_at=FADE,
                    btn_at=FADE + MORPH, bsize=BTN_SIZE, labelSize=34)
    S.set(out["cursor"], opacity=0)
    f, fp = out["card"], out["press"]
    for bt in S.beats:
        if bt["scene"] == "S21" and bt["frame"] == f:
            bt["what"] = ("tout s'efface puis la carte de fin paraît ; la pilule « 800 € » devient « S’abonner », passe "
                          "sous le sous-titre de la carte et devient son bouton ; « Toi » reste dessous")
        elif bt["scene"] == "S21" and bt["frame"] == fp:
            bt["what"] = "le stylo de « Toi » touche le bouton « S’abonner » : il s'enfonce, deux ondes partent"
    kit.ensure("solde", "z", S.ents["solde"]["z"])
    S.key("solde", "z", f, 41)
    S.key("solde", "text", f + 4, T_ABONNER)
    S.key("solde", "w", f, 285, MORPH, "inOut")
    S.key("solde", "pos", f, [300, 905], 8, "inOut")      # descend d'abord sous le sous-titre de la carte…
    S.key("solde", "pos", f + 8, list(FIN_BUTTON), 9, "inOut")   # … puis glisse sur le bouton
    S.key("solde", "scale", f, round(SOLDE_BTN_SCALE, 4), 16, "inOut")
    S.key("solde", "opacity", f + FADE + MORPH, 0)       # relais : le bouton (btn 1) est entier dessous
    toi.set_z(f, 42, tool_z=42.5)

    assert_reach(P1[0], FIN_TAP, "S21 bouton")
    hit = toi.tap(fp - TAP + 1, list(FIN_TAP))
    assert hit == fp, (hit, fp)
    for k in range(2):
        S.key(f"fin_onde{k + 1}", "pos", hit - 1, list(FIN_TAP))
    ring(S, "fin_onde1", hit, d=14, s0=0.6, s1=2.1)
    last = ring(S, "fin_onde2", hit + 4, d=14, s0=0.6, s1=2.1)
    assert last < f_end, (last, f_end)
