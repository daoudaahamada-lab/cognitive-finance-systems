"""V10, partie 2 : S08-S15, images 868-1850 (32 temps forts, 32,8 s).
Revue 1 du film : écarts d'exécution listés dans scripts/storyboards/V10.md (« Écarts de mise en scène »), le
code ci-dessous fait foi là où le brief qui suit diffère (S04 points rouges, S05 heurt, case de vérification…).

Piège 1 (délai) : accolade « Dans la journée », la rallonge cyan « Quelques jours » tirée jusqu'au bout ; le fil rouge
de l'interlocuteur la saisit et la ramène à « minuit », « Délai refusé » tombe du bout du fil ; le stylo qui vise
l'offre bute sur ce refus (la case de vérification rougit, ✕). « Délai refusé » reste épinglé : le champ de recherche
sort du stylo juste dessous. Piège 2 (registres) : l'offre réduite dans le coin (titre et barre seulement),
« Autorisé ? » sur l'interlocuteur, page de registre REGAFI puis ORIAS (place vide -> ✕ « Absent »), liste noire de
l'AMF, « Non autorisé » ; l'horloge « 2 min » ; « Toi » touche le champ : un fil deep coupe le crochet, les deux
moitiés retombent, la pastille libre revient près de « Toi ».

ÉTAT D'ENTRÉE : ENTRY_P2 épinglé à 867 (`kit.pin(f0 - 1, ENTRY_P2)`, f0 = scene_f0(S, "S08") = 868).
SORTIE : ENTRY_P3 à 1850 (voir la docstring de p3.py). Tout ce que cette partie commence finit avant 1851.
"""
from . import *  # noqa: F401,F403
from pipeline.story import DROP, FADE, MORPH, MOVE, POP, STRETCH, TILT  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401

RAL_X0 = RALLONGE_C[0] - RALLONGE_W / 2          # 528 : bord gauche de la rallonge (raccord avec la barre)
# S11 « affaire. » : le fil part du BAS de la pilule « Invest Minuit » et entre dans le bout gauche du champ (les deux
# se touchent presque : de CHAMP_LEFT à NOM_INTER_PT, le fil passait sous les deux et restait invisible)
FIL_NOM_A, FIL_CHAMP_B = (235, 1036), (293, 1080)


def ral(S, f, v, d=0, e="out"):
    """Longueur visible de la rallonge (part v de RALLONGE_W), bord gauche fixe en x 528 : pistes w et pos."""
    w = max(4.0, RALLONGE_W * v)
    S.key("rallonge", "w", f, round(w, 2), d, e)
    S.key("rallonge", "pos", f, [round(RAL_X0 + w / 2, 2), RALLONGE_C[1]], d, e)


def wire_reset(S, f, pa, pb, color=DEEP):
    """Fil de recherche effacé et ré-ancré, instantanément à l'image f (prêt à être tracé à f + 1)."""
    for k, v in (("draw", 0), ("from", 0), ("dashed", 0), ("sag", 0), ("pa", list(pa)), ("pb", list(pb)),
                 ("color", color)):
        S.key("fil_recherche", k, f, v)


def part(S, kit, c):
    toi, inter = c.toi, c.inter
    f0 = scene_f0(S, "S08")
    kit.pin(f0 - 1, ENTRY_P2)
    # la rallonge passe de value 0,5 (largeur 252) à value 1 sur 126 px : même cyan x 528-654, sans ombre vide
    kit.ensure("rallonge", "w", RALLONGE_W)
    S.key("rallonge", "value", f0 - 1, 1)
    ral(S, f0 - 1, 0.5)
    S.key("rallonge_mot", "opacity", f0 - 1, 1)
    # garde-fous (partie construite seule) : sans effet dans le film entier
    if S.val("interlocuteur", "scale", f0 - 1) == 0:
        inter.enter(f0 - 10, at=INTER_POS)
    if abs(S.val("toi", "pos", f0 - 1)[0] - P_S07[0]) > 1:
        walk_low(toi, f0 - 30, P_S07[0], d=18)
        toi.reach(f0 - 11, RALLONGE_MID, 10)

    # ---------------- S08 « Premier piège : décider dans la journée. » ----------------
    f = kit.at("S08", "Premier", "repère : le disque « 1 » s'allume en cyan, « Délai » en gras")
    S.key("marqueur", "on", f, 1, POP, "out")
    f = kit.at("S08", "piège :", "une accolade rouge épaisse se trace au-dessus de la partie rouge, de « maintenant » "
                                  "à « minuit », et bat")
    g = kit.draw("accolade_jour", f, 6)
    kit.pulse("accolade_jour", g, peak=1.08)
    f = kit.at("S08", "décider", "le bouton « J’investis » bat et se cerne de rouge : c'est là qu'on déciderait")
    kit.pulse("bouton", f, peak=1.1)
    S.key("bouton", "stroke", f, RED, 6)
    f = kit.at("S08", "journée.", "« Dans la journée » surgit en rouge sur l'accolade")
    kit.pop("accolade_mot", f)

    # ---------------- S09 « Une vraie opportunité supporte quelques jours de réflexion. » ----------------
    fv = S.word_after("vraie", scene_f0(S, "S09"))            # gestes secondaires : pas d'image figée
    kit.pulse("accolade_mot", fv, peak=1.1)                   # « vraie » : « Dans la journée » bat, rouge
    fo = S.word_after("opportunité", fv)                      # « opportunité » : « Toi » reprend en main le bout cyan
    hov = [RALLONGE_MID[0] + 6, RALLONGE_MID[1] - 16]
    toi._tip_line(fo, 4, list(RALLONGE_MID), hov, "out")
    toi._tip_line(fo + 4, 4, hov, list(RALLONGE_MID), "in")
    kit.pulse("rallonge", fo + 7, peak=1.06)
    f = kit.at("S09", "supporte", "« Toi » recule en tirant la rallonge cyan jusqu'au bout (x 528-780) ; "
                                  "son « ? » le suit au-dessus de sa tête")
    end = drag(toi, f, 15, RALLONGE_MID, RALLONGE_END)
    ral(S, f, 1, 15, "inOut")
    kit.move("question", f, Q_TETE_FAR, d=12)
    lower(toi, end + 1)
    f = kit.at("S09", "quelques", "« Quelques jours » s'écrit dans la partie cyan")
    kit.type("rallonge_mot", f, rate=1)
    f = kit.at("S09", "réflexion.", "le « ? » monte en arc se poser au-dessus des jours cyan : le temps de réfléchir")
    kit.move("question", f, Q_CYAN, d=MOVE, arc=60)

    # ---------------- S10 « Si on te refuse ce délai, c’est pour éviter que tu vérifies. » ----------------
    fsi = scene_f0(S, "S10")                                  # « Si » : l'interlocuteur commence à se pencher
    inter.lean_to(fsi, TILT / 2, 10)
    f = kit.at("S10", "refuse", "l'interlocuteur se penche et lance un fil rouge épais qui saisit le bout cyan et le "
                                "ramène jusqu'à « minuit » ; « Délai refusé » tombe du bout du fil à la place des jours ; "
                                "la pause saute, la barre rouge refond, le « ? » retombe")
    inter.lean_to(f, 10, TILT)
    S.key("fil_refus", "pb", f - 1, list(RALLONGE_END))
    g = kit.draw("fil_refus", f, 5, e="out")                  # le fil saisit le bout cyan
    pull = 12                                                 # 400 ms : on voit la rallonge tirée
    ral(S, g, 0, pull, "inOut")
    S.key("fil_refus", "pb", g, [RAL_X0 + 4, RALLONGE_C[1]], pull, "inOut")
    S.key("rallonge_mot", "opacity", g, 0, 5, "linear")
    h = g + pull
    S.key("rallonge", "scale", h, 0)
    kit.pop("refus", h, from_pt=[RAL_X0 + 4, RALLONGE_C[1]], to=list(REFUS_C))   # tombe du bout du fil
    S.key("fil_refus", "draw", h + 4, 0, 8, "in")             # le fil rentre dans l'interlocuteur
    kit.vanish("pause", f)
    S.key("compte_rebours", "value", f, 0.35, scene_f0(S, "S11") - 1 - f, "linear")
    kit.move("question", f, Q_TETE_FAR, d=DROP, e="out")

    f = kit.at("S10", "éviter", "« Toi » pousse le stylo vers l'offre : « Délai refusé » descend dans sa course, choc, "
                                "la pointe recule ; la barre bat en rouge ; la case de vérification tremble, rougit et "
                                "un grand ✕ s'y trace")
    C = BLOCK_S10
    toi.reach(f - 5, C, 6, e="in")
    S.key("refus", "pos", f - 4, [REFUS_C[0], REFUS_C[1] + 30], 4, "out")
    for k, dx in enumerate((8, -8, 8, -6, 4, 0)):
        S.key("refus", "pos", f + k, [REFUS_C[0] + dx, REFUS_C[1] + 30])
    S.key("refus", "pos", f + 12, list(REFUS_C), 6, "inOut")
    impact(S, f, C)
    kit.pulse("compte_rebours", f, peak=1.15)
    case_block(S, kit, f, hold=15)
    A = toi._shoulder(f)
    u = [A[0] - C[0], A[1] - C[1]]
    k = 60 / (u[0] ** 2 + u[1] ** 2) ** 0.5
    h = toi.reach(f + 1, [round(C[0] + u[0] * k, 2), round(C[1] + u[1] * k, 2)], 9, e="out")
    lower(toi, h + 3)
    f = kit.at("S10", "vérifies.", "« Délai refusé » bat deux fois, rouge ; l'interlocuteur se redresse")
    kit.pulse("refus", f, times=2, peak=1.08)
    inter.lean_to(f, 0, TILT)

    # ---------------- S11 « Ce délai, utilise-le pour savoir à qui tu as affaire. » ----------------
    f = kit.at("S11", "Ce", "« Délai refusé » reste épinglé ; « Toi » lève le stylo : un champ de recherche (loupe) "
                            "sort de sa pointe juste sous le refus")
    tip_pt = list(CHAMP_SPAWN)
    toi.reach(f - 6, tip_pt, 6)
    kit.pop("champ", f, from_pt=tip_pt, to=list(CHAMP_S11))
    kit.pulse("champ_loupe", f + POP, peak=1.5)
    lower(toi, f + 4)
    f = kit.at("S11", "utilise-le", "le champ de recherche descend se poser devant « Toi », sa loupe bat")
    kit.move("champ", f, list(CHAMP_C))
    kit.pulse("champ_loupe", f + 10, peak=1.5)
    f = kit.at("S11", "savoir", "« Toi » touche le champ : le « ? » saute dans son bout droit")
    hit = toi.tap(f - TAP + 1, CHAMP_TAP)
    kit.move("question", hit, Q_CHAMP, d=12, arc=50)
    S.key("question", "gs", hit, Q_GS_CHAMP, 12, "inOut")
    lower(toi, hit + 6)
    f = kit.at("S11", "affaire.", "le nom de l'interlocuteur bat ; un fil deep le relie au champ ; « Invest Minuit » "
                                  "s'écrit dans le champ")
    wire_reset(S, f - 1, FIL_NOM_A, FIL_CHAMP_B)
    S.key("fil_recherche", "sag", f - 1, 14)
    kit.pulse("nom_inter", f, peak=1.08)
    g = kit.draw("fil_recherche", f, 8)
    kit.type("champ_mot", g, rate=2)

    # ---------------- S12 « Deuxième piège : ne pas vérifier l’autorisation. » ----------------
    f = kit.at("S12", "Deuxième", "repère : le disque actif glisse sur « 2 · Registres », l'étape 1 se coche")
    kit.step(f, 1)
    S.key("marqueur", "done0", f, 1, 9, "out")
    f = kit.at("S12", "piège :", "l'offre se réduit en haut à gauche (titre et barre rouge seulement), « Délai refusé » "
                                 "rentre dans la barre, la pastille accrochée suit au bout du fil ; le fil rentre "
                                 "dans le champ")
    kit.move("offre", f, OFFRE_COIN, scale=OFFRE_COIN_K)
    for cid in COIN_HIDE:                                     # textes à 20 px : cachés, rien d'illisible dans le coin
        S.key(cid, "scale", f, 0, 6, "out")
    kit.vanish("refus", f, into=list(BAR_END), d=MOVE)
    S.key("crochet", "sag", f, 0, MOVE, "inOut")              # fil tendu : la pastille est retenue
    kit.move("pastille", f, PASTILLE_COIN, scale=PASTILLE_COIN_K)
    g = kit.draw("fil_recherche", f, 9, track="from")
    S.key("fil_recherche", "draw", g, 0)
    S.key("fil_recherche", "from", g, 0)
    f = kit.at("S12", "l’autorisation.", "au-dessus de l'interlocuteur surgit l'étiquette en tirets rouges "
                                         "« Autorisé ? », qui bat")
    g = kit.pop("verdict", f)
    kit.pulse("verdict_tirets", g, times=2, peak=1.06)

    # ---------------- S13 « …consulte le registre REGAFI. Pour un intermédiaire, c’est l’ORIAS. » ----------------
    f = kit.at("S13", "établissement", "une page de registre officiel surgit au centre : sceau, « REGAFI · "
                                       "Établissement financier », quatre noms inscrits et une place vide en tirets")
    kit.pop("registre", f)

    def row_pt(y_local, n):
        """Bout gauche d'une rangée de la page (avant le disque), en monde à l'image n."""
        return [round(v, 2) for v in S.to_world("registre", [REG_ICO_X - 24, y_local], n)]

    f = kit.at("S13", "consulte", "« Toi » touche le « ? » du champ : un fil monte dans la page et descend la "
                                  "liste, nom après nom, jusqu'à la place vide")
    hit = toi.tap(f - TAP + 1, Q_CHAMP)
    wire_reset(S, hit - 1, CHAMP_TOP, row_pt(REG_ROWS_Y[0], hit))
    g = kit.draw("fil_recherche", hit, 9)
    for y in REG_ROWS_Y[1:] + [REG_VIDE_LOCAL[1]]:
        S.key("fil_recherche", "pb", g, row_pt(y, g), 4, "inOut")
        g += 4
    lower(toi, hit + 6)
    f = kit.at("S13", "REGAFI.", "la place vide tremble et passe au rouge : un grand ✕ rouge s'y trace et « Absent » "
                                 "s'écrit dedans ; le fil se casse en tirets")
    kit.shake("reg_vide", f, 6)
    S.key("reg_vide", "stroke", f, RED, 6)
    kit.pop("reg_x", f, d=6)
    kit.type("reg_absent", f + 2, rate=1)
    S.key("fil_recherche", "dashed", f, 1)
    S.key("fil_recherche", "sag", f, 40, 9, "out")
    f = kit.at("S13", "intermédiaire,", "la page tourne : le registre devient « ORIAS · Intermédiaire », d'autres "
                                        "noms, la place vide redevient vide ; le fil rentre dans le champ")
    S.key("registre", "sx", f, 0, 5, "in")
    mid = f + 5
    for tid, txt in (("registre_titre", T_ORIAS), ("registre_sous_titre", T_ORIAS_SOUS)):
        S.key(tid, "text", mid, txt)
    S.key("reg_absent", "chars", mid, 0)
    S.key("reg_x", "scale", mid, 0)
    S.key("reg_vide", "stroke", mid, INK)
    kit.ensure("reg_nom1", "w", REG_TRAIT_W[0][0])
    for k, nid in enumerate(REG_NOMS):                       # une autre page : d'autres noms
        w = REG_TRAIT_W[1][k]
        kit.ensure(nid, "w", REG_TRAIT_W[0][k])
        S.key(nid, "w", mid, w)
        S.key(nid, "pos", mid, [REG_TRAIT_X0 + w / 2, REG_ROWS_Y[k]])
    S.key("registre", "sx", mid, 1, 5, "out")
    g = kit.draw("fil_recherche", f, 9, track="from")
    S.key("fil_recherche", "draw", g, 0)
    S.key("fil_recherche", "from", g, 0)
    f = kit.at("S13", "l’ORIAS.", "le fil cherche de nouveau jusqu'à la place vide : elle tremble en rouge, grand ✕, "
                                  "« Absent » s'écrit encore, le fil se casse")
    wire_reset(S, f - 1, CHAMP_TOP, row_pt(REG_VIDE_LOCAL[1], f - 1))
    g = kit.draw("fil_recherche", f, 9)
    kit.shake("reg_vide", g, 6)
    S.key("reg_vide", "stroke", g, RED, 6)
    kit.pop("reg_x", g, d=6)
    kit.type("reg_absent", g + 2, rate=1)
    S.key("fil_recherche", "dashed", g, 1)
    S.key("fil_recherche", "sag", g, 40, 9, "out")

    # ---------------- S14 « Regarde aussi les listes noires de l’AMF… non autorisés. » ----------------
    f = kit.at("S14", "Regarde", "la page de registre se replie et disparaît, puis une liste surgit à sa place, son "
                                 "en-tête encre s'étire ; le fil cassé rentre dans le champ")
    kit.vanish("registre", f, d=POP)
    g0 = kit.pop("liste_noire", f + 5)
    S.key("ln_entete", "sx", f + 9, 1, STRETCH, "out")
    g = kit.draw("fil_recherche", f, 9, track="from")
    S.key("fil_recherche", "draw", g, 0)
    S.key("fil_recherche", "from", g, 0)
    f = kit.at("S14", "noires", "« Liste noire » paraît dans l'en-tête, avec le même sceau officiel que le registre")
    kit.pop("ln_sceau", f)
    kit.pop("ln_titre", f + 2)
    f = kit.at("S14", "l’AMF,", "la pilule « AMF » tombe sur l'en-tête")
    drop_in(kit, "amf_liste", f, h=120)
    f = kit.at("S14", "recensent", "quatre lignes s'inscrivent une à une (2 sites, 2 sociétés) ; la dernière "
                                   "s'écrit « Invest Minuit »")
    for k, did in enumerate(LN_DISCS):
        kit.pop(did, f + 4 * k)
        if k < len(LN_TRAITS):
            kit.pop(LN_TRAITS[k], f + 4 * k + 1)
    kit.type("ln_nom", f + 12, rate=2)
    f = kit.at("S14", "non", "« Toi » touche le « ? » du champ : le fil atteint « Invest Minuit », le nom et son "
                             "disque passent au rouge et battent ; le « ? » tombe du champ")
    hit = toi.tap(f - TAP + 1, Q_CHAMP)
    name_pt = [round(v, 2) for v in S.to_world("liste_noire", [LN_NOM_LOCAL[0] + 35, LN_NOM_LOCAL[1] + 23], f - 1)]
    wire_reset(S, f - 1, CHAMP_TOP, name_pt)
    kit.draw("fil_recherche", f, 5)
    S.key("ln_nom", "color", f, RED, 6)
    S.key("ln_disc4", "fill", f, RED, 6)
    kit.pulse("ln_nom", f, peak=1.12)
    kit.drop("question", f + 1, out=True)
    S.key("question", "scale", f + 1 + DROP + 6, 0)
    lower(toi, hit + 6)
    f = kit.at("S14", "autorisés.", "le fil passe au rouge et file vers l'étiquette de l'interlocuteur, qui devient "
                                    "« Non autorisé » en rouge plein")
    S.key("fil_recherche", "color", f, RED, 6)
    edge = [round(v, 2) for v in S.to_world("verdict", [VERDICT_W / 2, 0], f - 1)]
    S.key("fil_recherche", "pa", f, edge, 9, "inOut")
    g = f + 9
    S.key("verdict_plein", "scale", g, 1)
    S.key("verdict_tirets", "scale", g, 0)
    S.key("verdict_mot", "text", g, T_NON_AUTORISE)
    S.key("verdict_mot", "color", g, RED, 6)
    kit.pulse("verdict", g, peak=1.1)

    # ---------------- S15 « Une recherche de deux minutes peut t’éviter de tout perdre. » ----------------
    f = kit.at("S15", "recherche", "l'horloge ressort de la pointe du stylo de « Toi » et monte se poser à droite")
    S.key("horloge", "value", f - 1, 0)
    S.key("horloge", "start", f - 1, 0)
    S.key("horloge", "pos", f - 1, [round(v, 2) for v in toi.tip(f - 1)])
    kit.pop("horloge", f)
    kit.move("horloge", f, HORLOGE_S15)
    f = kit.at("S15", "deux", "le secteur se remplit de 2 unités ; « 2 min » compte sous l'horloge")
    S.key("horloge", "value", f, 2, 12, "linear")
    kit.pop("horloge_2min", f)
    S.key("horloge_2min", "value", f, 2, 12, "linear")
    f = kit.at("S15", "t’éviter", "« Toi » touche le champ : un fil deep en part, monte et tranche le crochet rouge en "
                                  "son milieu (choc) ; les deux moitiés retombent, le crochet en J tombe de la pastille")
    hit = toi.tap(f - TAP + 1, CHAMP_TAP)
    lower(toi, hit + 6)
    a = [round(v, 2) for v in S.to_world("offre", list(CROCHET_A_LOCAL), hit)]
    b = [round(v, 2) for v in S.to_world("pastille", list(PASTILLE_HOOK_LOCAL), hit)]
    m = [round((a[0] + b[0]) / 2, 2), round((a[1] + b[1]) / 2, 2)]
    S.key("fil_coupe", "pa", hit - 1, list(FIL_COUPE_A))
    S.key("fil_coupe", "pb", hit - 1, m)
    cut = kit.draw("fil_coupe", hit, 6, e="in")               # le fil de la recherche atteint le crochet
    impact(S, cut, m)
    S.key("crochet", "opacity", cut, 0)                       # relais : deux moitiés libres
    for hid, pa, pb in (("crochet_h1", a, m), ("crochet_h2", m, b)):
        S.key(hid, "pa", cut - 1, pa)
        S.key(hid, "pb", cut - 1, pb)
        S.key(hid, "draw", cut, 1)
    S.key("crochet_h1", "pb", cut, [m[0] - 14, m[1] + 70], 9, "out")    # la moitié côté offre retombe et se retire
    S.key("crochet_h1", "draw", cut + 3, 0, 9, "in")
    S.key("crochet_h2", "pa", cut, [m[0] + 14, m[1] + 70], 9, "out")    # la moitié côté pastille aussi
    kit.ensure("crochet_h2", "from", 0)
    S.key("crochet_h2", "from", cut + 3, 1, 9, "in")
    kit.drop("crochet_j", cut, out=True, h=90, rot=30)
    kit.pulse("pastille", cut, peak=round(PASTILLE_COIN_K * 1.15, 3))
    S.key("fil_coupe", "from", cut + 6, 1, 8, "in")          # le fil de la recherche rentre dans le champ
    tidy = cut + DROP + 8                                     # invisibles : remis en place pour p3 (crochet_j)
    S.key("crochet_j", "scale", tidy, 0)
    S.key("crochet_j", "pos", tidy, list(PASTILLE_HOOK_LOCAL))
    S.key("crochet_j", "rot", tidy, 0)
    S.key("crochet_j", "opacity", tidy, 1)
    S.key("fil_coupe", "draw", tidy, 0)
    S.key("crochet_h2", "draw", tidy, 0)
    S.key("crochet_h2", "from", tidy, 0)
    S.key("fil_coupe", "from", tidy, 0)
    f = kit.at("S15", "perdre.", "la pastille « Ton argent », libre, reprend sa taille et revient en bas, du côté de "
                                 "« Toi », puis bat")
    g = kit.move("pastille", f, PASTILLE_S15, scale=1)
    kit.pulse("pastille", g, peak=1.05)
