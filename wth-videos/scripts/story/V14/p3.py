"""V14, partie 3 : S16-S22, images 1747-2633 (30 temps forts, 29,6 s). Les trois cas au-dessus du conseiller, la
sonnette et « Vois un conseiller », les deux applis et le choix, le test à la cible, Avant / Après et « Je ne sais
pas » coché, le tampon CONFIANCE, la fin standard (la pastille devient le bouton « S’abonner »).

TOUR DE REVUE 1 (le brief ci-dessous est celui de la v1 ; le code fait foi) : S16 les cartes-cas volent d'à côté de
l'IA jusqu'à la colonne (40 px sous la carte), les pièces ressortent de « Toi » ; S17 ondes de la sonnette tournées
vers le conseiller, bulle PARLÉE écrite mot par mot, trait pointillé qui désigne le conseiller, cadres deep autour des
cas ; S18 textes effacés avant le repli, applis plus basses (y 360-950), « Toi » touche l'appli depuis le sol ; S19
« Toi » fait un pas, cible retournée de 320 px, il écrit « en général » sous le stylo, la réponse de l'IA se pose
pile sur la sienne (2 anneaux), coche en haut à droite ; S20 décalages (carte, pastille, Avant), « Je ne sais pas »
né en pensée puis devenu parole sur « dit » ; S21 le cadre de L4 s'efface, tampon dans la carte. Bras baissé au repos.

ÉTAT D'ENTRÉE (etat_initial de S16) : kit.pin(1746, ENTRY_P3 + compléments) en tête de partie (f0 = scene_f0(S, "S16")
= 1747). Carte prudente réduite en B_SMALL_C (0,55, lignes en barres, cochée), pastille sur son en-tête, livre en
LIVRE_SMALL_C relié à L2 (fil_source) ; conseiller en CONSEILLER_C face à « Toi » ; empreinte en EMPREINTE_C et 2 pièces
(pile en PILE_C) au sol entre eux ; boule au sol (BOULE_SOL) avec la réponse cassée dedans (reponse scale 0, lignes
rouges fendues, coches de l'IA gardées) ; IA en bas à gauche ; « Toi » en TOI_REST.
Compléments épinglés (égaux à la fin de p2, donc sans saut dans le film entier) : coches de l'IA reponse_ia1-3 draw 1,
surligneur de L4 déployé et capsule de L4 vide (S13).
Garde-fou de partie isolée (WTH_PARTS=p3 ; sans effet dans le film entier) :
    if S.val("conseiller", "scale", f0 - 1) == 0: c.conseiller.enter(f0 - 10, at=CONSEILLER_C)
SORTIE : fin du film à 2633 (FILM_END 2634) : rien ne bouge après le toucher du bouton (ondes finies avant 2634).

Ids : cas1-3 (+ cas{i}_txt, cas1_disque, cas1_signe), empreinte, pile (+ piece1-7, piece2_euro, piece7_euro),
conseiller (c.conseiller), nom_conseiller ; sonnette (+ sonnette_onde1-3), f_sonnette, bulle_conseil
(+ bulle_conseil_pointe, bulle_conseil_txt) ; appli_g, appli_d (+ _barre, _point1-3), cadre_appli ; bonne_reponse
(+ L1-4, coche_toi, surligne_L4, cadre_L4, tampon), livre, fil_source, fil_source_gras ; reponse (+ L1-3, reponse_ia1-3),
boule ; cible (+ test_toi, coche_cible, onde_cible), test_ia (+ test_ia_txt), f_test, pastille ; bulle_jnsp
(+ bulle_jnsp_pointe, bulle_jnsp_txt, coche_jnsp), onde_jnsp ; etiq_avant, etiq_apres ; nom_ia, ia ; fin_onde1-2.

ÉCARTS (exécution seulement, aucun sens changé) :
- S16 : les pièces 5-7 se posent aux places 3-5 de la pile (les places 3-4 sont vides depuis S09) : pile de 5 jointive.
- S17 : le faisceau f_sonnette passe à droite de l'étiquette « Ton IA » (piste via) et se retire avant la bulle
  « Vois un conseiller » (il la traverserait) : il frappe, la sonnette sonne, il s'éteint.
- S18 : le fil du livre longe le bord gauche de la carte (via (436, 610), ancre sur le bord gauche du livre), passé
  sous la carte et ses puces (piste z 7,9) au lieu de traverser L3 et L4.
- S21 : « Toi » saute en (848, 830) au lieu de TOI_MID (860, 830) : la poignée du tampon est alors à portée de la main
  seule (pas de pas automatique pendant le saut) ; le tampon est posé 8 px plus bas (hors du cadre de L4) et la coche
  de « Toi » (S14) glisse en bas à gauche de la carte pendant le MORPH de S20 : le tampon ne la recouvre plus.
"""
from pipeline.story import FADE, MORPH, MOVE, POP
from pipeline.story_kit import TAP

from . import *  # noqa: F401,F403
from . import ENTRY_P3

FIN_K = 1.75                                    # pastille -> bouton : 64 x 1,75 = 112 px (hauteur du bouton)
FIN_W = round(380 / FIN_K, 1)                   # largeur de la pilule pour 380 px à l'écran
FIN_BSIZE = round(PASTILLE_SIZE * FIN_K, 1)     # libellé du bouton = libellé de la pastille grandie (relais exact)
SONNETTE_PB = [212, 548]                        # S17 : le faisceau monte droit, à droite de « Ton IA », et frappe la sonnette
SONNETTE_PA = [272, 1040]
FIL_VIA = [436, 720]                            # S18 : le fil du livre longe le bord gauche de la carte, derrière
FIL_Z = 7.9                                     # les puces L3-L4 (sous la carte z 8, au-dessus de l'appli z 6)
LIVRE_LEFT = [-round(LIVRE_W / 2 - 4, 1), 0]    # ancre du fil sur le bord gauche du livre
COCHE_TOI_APRES = (-170, 250)                   # S20 : coche de « Toi » en bas à gauche de la carte « Après »


def _cas_type(S, id, segs):
    """Écriture d'un texte de cas au rythme de la voix : segs = [(image, nb de caractères visé, durée)]."""
    for f, n, d in segs:
        S.key(id, "chars", f, n, d, "linear")


def _reset_beam(S, id, f):
    S.key(id, "draw", f, 0)
    S.key(id, "from", f, 0)


def _retract(S, id, f, d=9):
    """Le faisceau rentre vers son bout (from -> 1), puis remis à 0 invisible. -> f + d + 1."""
    S.key(id, "from", f, 1, d, "out")
    _reset_beam(S, id, f + d)
    return f + d + 1


def _ring_bell(kit, f, scale):
    """La sonnette bat (x 1,12) ; ses trois ondes se tracent l'une après l'autre puis s'effacent ; remises à zéro
    (invisibles) pour la sonnerie suivante. -> image où tout est fini."""
    S = kit.S
    kit.pulse("sonnette", f, peak=round(scale * 1.12, 4), step=3)
    ondes = [f"sonnette_onde{k + 1}" for k in range(3)]
    kit.stagger(ondes, f, 2, kit.draw, 6)
    for o in ondes:
        S.key(o, "opacity", f + 10, 0, 6, "linear")
        S.key(o, "draw", f + 16, 0)
        S.key(o, "opacity", f + 17, 1)          # draw 0 : invisible
    return f + 17


def _bullet_world(S, line_id, n):
    return S.to_world(line_id, [S.ents[line_id]["p"]["bulletX"], 0], n)


def _set_what(S, scene, frame, what):
    for bt in S.beats:
        if bt["scene"] == scene and bt["frame"] == frame:
            bt["what"] = what


def part(S, kit, c):
    toi, rep_a, rep_b = c.toi, c.rep_a, c.rep_b
    f0 = scene_f0(S, "S16")                      # 1747
    entry = {id: dict(v) for id, v in ENTRY_P3.items()}
    extra = {**{t: {"draw": 1} for t in TICK_A_IDS},                       # coches de l'IA gardées (fin de p1)
             **{lid: {"chars": len(k) + len(v)} for lid, (k, v, _) in zip(REP_A_IDS, LINES_A)},   # lignes écrites
             "surligne_L4": {"w": SURL_L4_W, "pos": list(SURL_L4_C)},  # surligneur de L4 (S13)
             "bonne_reponse_L4": {"slotFill": 0}}
    for id, v in extra.items():                 # fusion par entité : les pistes d'ENTRY_P3 restent
        entry.setdefault(id, {}).update(v)
    kit.pin(f0 - 1, entry)
    if S.val("conseiller", "scale", f0 - 1) == 0:     # partie isolée seulement : le conseiller est entré en S15 (p2)
        c.conseiller.enter(f0 - 10, at=list(CONSEILLER_C))
        look(S, "conseiller", f0 - 10, 1)

    def chest(n):
        return S.to_world("toi", list(TOI_CHEST), n)

    def slot(i):
        return [CAS_C[i][0] + CAS_OBJ_LOCAL[0], CAS_C[i][1]]

    # ================= S16 : trois cas trop gros pour la machine, portés à l'humain =================
    f = kit.at("S16", "Question", "une carte-cas part d'à côté de l'IA (là où son faisceau est retombé) et vole se "
               "poser au-dessus du conseiller, signe « § » sur disque cyan ; « Question réglementaire / hors "
               "contexte » s'y écrit")
    kit.pop("cas1", f, from_pt=list(CAS_FROM), to=list(CAS_C[0]), d=14)
    _cas_type(S, "cas1_txt", [(f + 6, 22, S.word_after("hors", f) - f - 7), (S.word_after("hors", f), 35, 26)])

    f = kit.at("S16", "situation", "une 2e carte-cas vole de l'IA jusqu'à la colonne ; l'empreinte de « Toi » quitte le "
               "sol et s'y pose ; « Situation personnelle / complexe » s'y écrit")
    kit.pop("cas2", f, from_pt=list(CAS_FROM), to=list(CAS_C[1]), d=14)
    kit.move("empreinte", f, slot(1), scale=EMPREINTE_CAS_K)
    g = S.word_after("complexe", f)
    _cas_type(S, "cas2_txt", [(f + 6, 21, g - f - 7), (g, 29, 16)])

    f = kit.at("S16", "montant", "une 3e carte-cas vole de l'IA jusqu'à la colonne ; les 2 pièces ressortent de la "
               "poitrine de « Toi » et s'y posent ; « Montant important » s'y écrit")
    pile_y = round(CAS_C[2][1] + (PIECE_H + 14 * 4) / 2 * PILE_CAS_K, 1)   # pile de 5 centrée sur la carte-cas 3
    kit.pop("cas3", f, from_pt=list(CAS_FROM), to=list(CAS_C[2]), d=14)
    kit.pop("pile", f, scale=PILE_CAS_K, from_pt=chest(f - 1), to=[slot(2)[0], pile_y], d=14)
    g = S.word_after("important", f)
    _cas_type(S, "cas3_txt", [(f + 6, 7, g - f - 7), (g, 17, 16)])

    f = kit.at("S16", "important ?", "3 pièces tombent sur la petite pile : 5 pièces, le « € » passe sur celle du "
               "dessus ; les trois cas sont empilés au-dessus du conseiller")
    for k, pid in enumerate(("piece5", "piece6", "piece7")):
        drop_in(kit, pid, f + 2 * k, h=110, d=9, to=list(PIECE_LOCAL[2 + k]))
    kit.fade("piece2_euro", f + 2, 0)

    # ================= S17 : l'outil sonne et dit « Vois un conseiller » : il désigne l'humain =================
    f = kit.at("S17", "L’outil", "une sonnette tombe dans la colonne de gauche, au-dessus de l'IA")
    drop_in(kit, "sonnette", f)
    for k in range(3):                           # ses ondes partiront vers le conseiller
        S.key(f"sonnette_onde{k + 1}", "rot", f, ONDES_VERS_CONSEILLER)

    f = kit.at("S17", "signaler,", "un faisceau pointillé de l'IA monte et frappe le bouton de la sonnette : elle bat, "
               "trois ondes partent vers le conseiller ; le faisceau s'éteint")
    S.set("f_sonnette", pa=list(SONNETTE_PA), pb=list(SONNETTE_PB))
    hit = kit.draw("f_sonnette", f, 6, e="linear")
    _ring_bell(kit, hit, S.val("sonnette", "scale", hit - 1))
    _retract(S, "f_sonnette", hit + 6, d=8)

    f = kit.at("S17", "pas", "une bulle PARLÉE sort de la tête de l'IA, sous la sonnette : « Vois un » puis "
               "« conseiller » s'y écrivent, mot par mot")
    kit.pop("bulle_conseil", f, from_pt=list(IA_HEAD), to=list(CONSEIL_C), d=6)
    S.key("bulle_conseil_txt", "chars", f + 2, 7)            # mots entiers : jamais de mot coupé à l'écran
    S.key("bulle_conseil_txt", "chars", f + 5, 17)

    f = kit.at("S17", "cacher.", "un trait pointillé part de la bulle et désigne le conseiller ; un cadre deep se trace "
               "autour de chacun des trois cas, qui restent en vue ; l'étiquette « Conseiller » bat")
    kit.draw("f_designe", f, 8)
    kit.stagger([f"cadre_cas{i + 1}" for i in range(3)], f + 2, 2, kit.draw, 8)
    kit.pulse("nom_conseiller", f + 8, peak=round(S.val("nom_conseiller", "scale", f - 1) * 1.12, 4), times=2, step=3)

    # ================= S18 : deux applis, « Toi » choisit celle au livre et à la sonnette =================
    f = kit.at("S18", "Pour", "les textes des cas s'effacent, puis les cas (empreinte et pièces comprises) rentrent dans "
               "le conseiller, qui sort ; la bulle rentre dans la tête de l'IA ; « Toi » regarde devant lui")
    for i in range(3):
        S.key(f"cas{i + 1}_txt", "opacity", f, 0, 4, "linear")
        S.key(f"cadre_cas{i + 1}", "opacity", f, 0, 4, "linear")
    for k, (cas, extra) in enumerate((("cas1", None), ("cas2", "empreinte"), ("cas3", "pile"))):
        kit.vanish(cas, f + 4 + 2 * k, into="conseiller")
        if extra:
            kit.vanish(extra, f + 4 + 2 * k, into="conseiller")
    c.conseiller.exit(f + 12)
    S.key("bulle_conseil_txt", "opacity", f, 0, 3, "linear")
    kit.vanish("bulle_conseil", f + 2, into=list(IA_HEAD))
    _retract(S, "f_designe", f, d=6)
    for k in range(3):
        S.key(f"sonnette_onde{k + 1}", "rot", f, 0)
    look(S, "toi", f, 0)

    f = kit.at("S18", "tien,", "la carte cochée glisse dans une fenêtre d'appli qui se trace à droite, la question avec "
               "elle ; le livre et la sonnette se placent dessous")
    kit.move("bonne_reponse", f, list(B_APPLI_C), d=MORPH, scale=B_APPLI_K, e="out")
    hp, hk = head_pt("bonne_reponse", B_APPLI_C, B_APPLI_K)
    kit.move("pastille", f, hp, d=MORPH, scale=hk, e="out")
    kit.move("livre", f, list(LIVRE_APPLI_C), d=MORPH, e="out")
    kit.move("sonnette", f, list(SONNETTE_APPLI), d=MORPH, scale=SONNETTE_APPLI_K, e="out")
    for w in ("fil_source", "fil_source_gras"):           # le fil longe le bord gauche de la carte
        b0 = S.to_world("livre", [round(LIVRE_W / 2 - 4, 1), 0], f - 1)
        a0 = _bullet_world(S, "bonne_reponse_L2", f - 1)
        kit.ensure(w, "bAt", [round(LIVRE_W / 2 - 4, 1), 0])
        kit.ensure(w, "via", [])
        S.key(w, "via", f - 1, [round((a0[0] + b0[0]) / 2, 1), round((a0[1] + b0[1]) / 2, 1)])   # sans coude visible
        S.key(w, "bAt", f, LIVRE_LEFT, MORPH, "out")
        S.key(w, "via", f, list(FIL_VIA), MORPH, "out")
        kit.ensure(w, "z", S.ents[w]["z"])
        S.key(w, "z", f, FIL_Z)
    end = kit.draw("appli_d", f, 9)
    for k in ["appli_d_barre"] + [f"appli_d_point{i + 1}" for i in range(3)]:
        kit.fade(k, end, 1)

    f = kit.at("S18", "privilégie", "à gauche, la boule de cristal ressort de la tête de l'IA ; la réponse cassée "
               "(barres rouges fendues, coches pointillées de l'IA) en ressort et grandit ; une seconde fenêtre d'appli "
               "se trace autour d'elles")
    kit.pop("boule", f, scale=1, from_pt=list(IA_HEAD), to=list(BOULE_APPLI), d=MORPH)
    for id in ["reponse"] + rep_a:
        S.key(id, "lite", f - 1, 1)
    kit.pop("reponse", f + 3, scale=A_APPLI_K, from_pt=list(BOULE_APPLI), to=list(A_APPLI_C), d=MORPH)
    end = kit.draw("appli_g", f, 9)
    for k in ["appli_g_barre"] + [f"appli_g_point{i + 1}" for i in range(3)]:
        kit.fade(k, end, 1)

    f = kit.at("S18", "sources", "à droite, le fil entre la ligne « Source » et le livre s'épaissit et le livre bat ; "
               "à gauche, rien ne part des lignes cassées")
    S.key("fil_source_gras", "opacity", f, 1, 9, "out")
    kit.pulse("livre", f, peak=round(S.val("livre", "scale", f - 1) * 1.1, 4))

    f = kit.at("S18", "signalent", "la sonnette de l'appli de droite bat et lance ses trois ondes")
    _ring_bell(kit, f, S.val("sonnette", "scale", f - 1))

    f = kit.at("S18", "l’incertitude.", "« Toi », resté au sol, touche du stylo le bord de l'appli de droite : un "
               "cadre deep se trace autour d'elle, c'est celle qu'il choisit")
    hit = toi.tap(f - TAP + 1, list(APPLI_TAP))
    kit.draw("cadre_appli", hit, 9)
    toi.lower(hit + 6, 8)

    # ================= S19 : le test à la cible =================
    f = kit.at("S19", "Puis", "la réponse cassée et sa fenêtre rentrent dans la boule, qui rentre dans la tête de "
               "l'IA ; « Toi » fait un pas vers le milieu ; l'appli choisie reste encadrée")
    kit.vanish("reponse", f, into="boule")
    kit.vanish("appli_g", f, into="boule")
    for k in ["appli_g_barre"] + [f"appli_g_point{i + 1}" for i in range(3)]:
        S.key(k, "opacity", f, 0, 4, "linear")
    kit.vanish("boule", f + 8, into=list(IA_HEAD), d=10)
    walk_low(toi, f, TOI_TEST, 12)

    f = kit.at("S19", "teste-le", "une grande cible sort de la poitrine de « Toi » et se pose devant lui, sa pilule "
               "vide au centre")
    kit.pop("cible", f, scale=1, from_pt=chest(f - 1), to=list(CIBLE_C), d=MORPH)

    f = kit.at("S19", "avec", "« Toi » écrit au centre de la cible, sous son stylo qui glisse de gauche à droite, la "
               "réponse qu'il connaît : « en général »")
    mille = [CIBLE_C[0] + MILLE_LOCAL[0], CIBLE_C[1] + MILLE_LOCAL[1] + 2]
    a, b = [mille[0] - 62, mille[1]], [mille[0] + 62, mille[1]]
    toi.reach(f - 6, a, d=6)
    toi.trace(f, [a, b], d=10)
    kit.type("test_toi_txt", f, rate=1)
    toi.lower(f + 11, 7)

    f = kit.at("S19", "question", "la question quitte l'en-tête de la carte et vole jusque devant l'IA, qui la lit "
               "(elle bat, éclat du cerveau de l'IA)")
    arr = kit.move("pastille", f, list(PASTILLE_TEST), arc=120, scale=PASTILLE_TEST_K)
    S.key("pastille", "textOp", arr - 6, 1, FADE, "out")
    kit.pulse("pastille", arr, peak=round(PASTILLE_TEST_K * 1.1, 4), step=3)   # l'IA lit la question :
    S.key("eclat_ia", "scale", arr - 1, 1)                                      # éclat de son cerveau
    S.key("eclat_ia", "p", arr - 1, 0)
    S.key("eclat_ia", "p", arr, 1, 9, "out")
    S.key("eclat_ia", "scale", arr + 10, 0)

    f = kit.at("S19", "déjà", "la réponse de l'IA, « en général » en pointillés, sort de sa tête, vole et se pose pile "
               "sur celle de « Toi » et s'y fond (mêmes mots) ; la pilule bat, deux anneaux partent du mille")
    land = [mille[0] + TEST_IA_DX[0], mille[1] - 2 + TEST_IA_DX[1]]
    arr = kit.pop("test_ia", f, scale=1, from_pt=list(IA_HEAD), to=land, d=7)
    S.key("test_ia", "opacity", arr, 0, 6, "linear")        # fusion : la réponse de l'IA se fond dans celle de « Toi »
    kit.pulse("test_toi", arr, peak=1.15, step=3)              # (mêmes mots, même place : pile dans le mille)
    ring(S, "onde_cible", arr, d=10, s0=0.85, s1=1.35)
    ring(S, "onde_cible2", arr + 4, d=10, s0=0.85, s1=1.35)

    f = kit.at("S19", "réponse.", "« Toi » coche la cible, au-dessus à droite des deux réponses identiques : test réussi")
    hit = toi.tap(f - TAP + 1, [CIBLE_C[0] + COCHE_CIBLE_LOCAL[0], CIBLE_C[1] + COCHE_CIBLE_LOCAL[1]])
    kit.draw("coche_cible", hit, 5)
    toi.lower(hit + 6, 8)

    # ================= S20 : Avant / Après ; « Je ne sais pas » dit à voix haute et coché =================
    f = kit.at("S20", "Une", "la cible et ses deux réponses rentrent dans « Toi », qui revient au repos ; la fenêtre de "
               "l'appli et son cadre s'effacent ; le faisceau se retire")
    walk_low(toi, f, TOI_REST, 12)
    ch = chest(f + POP)
    kit.vanish("cible", f, into=ch)
    for id in ("appli_d", "cadre_appli", "appli_d_barre", "appli_d_point1", "appli_d_point2", "appli_d_point3"):
        S.key(id, "opacity", f, 0, FADE, "linear")

    f = kit.at("S20", "IA", "Après : la carte cochée vient à droite et grandit (barres, puis lignes lisibles) ; le "
               "livre rentre dans la puce de L2, la sonnette dans celle de L4 ; la question revient sur l'en-tête ; "
               "étiquette « Après ». Avant : à gauche, la boule ressort de l'IA et la réponse cassée en sort ; "
               "étiquette « Avant »")
    kit.move("bonne_reponse", f, list(B_APRES_C), d=MORPH, scale=B_APRES_K, e="out")
    S.key("coche_toi", "pos", f, list(COCHE_TOI_APRES), MORPH, "out")   # la coche laisse la place au tampon
    for id in ["bonne_reponse"] + rep_b:
        S.key(id, "lite", f + MORPH + 3, 0, 3, "linear")            # lignes lisibles une fois la carte posée
    kit.vanish("livre", f, into=_bullet_world(S, rep_b[1], f + POP))
    kit.vanish("sonnette", f, into=_bullet_world(S, rep_b[3], f + POP))
    for w in ("fil_source", "fil_source_gras"):
        _retract(S, w, f, d=6)
    hp, hk = head_pt("bonne_reponse", B_APRES_C, B_APRES_K)
    S.key("pastille", "textOp", f, 0, 3, "linear")
    arr = kit.move("pastille", f + 2, hp, d=12, scale=hk, arc=60, e="inOut")
    S.key("pastille", "textOp", arr, 1, FADE, "out")
    kit.pop("etiq_apres", f + 8)
    kit.pop("boule", f + 4, scale=BOULE_AVANT_K, from_pt=list(IA_HEAD), to=list(BOULE_AVANT), d=MORPH)
    kit.pop("reponse", f + 8, scale=A_AVANT_K, from_pt=list(BOULE_AVANT), to=list(A_AVANT_C), d=MORPH)
    kit.pop("etiq_avant", f + 10)

    g = S.word_after("qui", f)                   # la PENSÉE d'abord (comme en S03) : ronds pointillés, bulle pointillée
    for k in range(3):
        kit.pop(f"jnsp_rond{k + 1}", g - 8 + 2 * k, d=6)
    kit.pop("bulle_jnsp", g - 2, d=7)

    f = kit.at("S20", "dit", "la pensée devient PAROLE : les ronds rentrent, le contour pointillé devient plein et une "
               "grande pointe pleine sort vers la bouche de l'IA, deux arcs de voix ; « Je ne sais pas » s'y écrit")
    for k in range(3):
        kit.vanish(f"jnsp_rond{3 - k}", f + k, into=list(IA_MOUTH), d=6)
    S.key("bulle_jnsp_trait", "opacity", f, 1, MORPH, "out")
    kit.pop("bulle_jnsp_pointe", f + 2, scale=1, d=8)
    for k in range(2):
        a_id = f"son_arc{k + 1}"
        S.key(a_id, "opacity", f + 2 * k, 1)
        kit.draw(a_id, f + 2 * k, 4)
        S.key(a_id, "opacity", f + 7 + 2 * k, 0, 4, "linear")
        S.key(a_id, "draw", f + 12 + 2 * k, 0)
    kit.type("bulle_jnsp_txt", f + 3, rate=1)

    f = kit.at("S20", "pas", "en face, les trois lignes cassées de la carte « Avant » battent en rouge")
    for k, lid in enumerate(rep_a):
        kit.pulse(lid, f + 2 * k, times=2, step=2, track="pulse")

    f = kit.at("S20", "faiblesse.", "« Toi » touche du stylo le bout de la bulle « Je ne sais pas » : un anneau part "
               "du point touché, rien ne casse ; une coche pleine se trace dans la bulle")
    hit = toi.tap(f - TAP + 1, list(JNSP_TAP))
    S.key("onde_jnsp", "pos", hit - 1, list(JNSP_TAP))
    ring(S, "onde_jnsp", hit, d=10)
    kit.draw("coche_jnsp", hit, 5)
    toi.lower(hit + 6, 8)

    f = kit.at("S20", "limites.", "la puce de « Limites : ton cas » grossit et un cadre deep se trace autour de la "
               "ligne")
    kit.pulse(rep_b[3], f, track="flash", step=3)
    kit.draw("cadre_L4", f, 9)

    # ================= S21 : tampon CONFIANCE =================
    f = kit.at("S21", "Et", "le cadre de « Limites » s'efface ; « Toi » saute au coin bas droit de la carte « Après », "
               "son étiquette avec lui")
    S.key("cadre_L4", "opacity", f, 0, FADE, "linear")
    hop_low(toi, f, TOI_STAMP, 7)

    f = kit.at("S21", "confiance", "« Toi » abat le tampon « CONFIANCE » dans la marge basse de la carte « Après », qui "
               "tremble ; puis plus rien ne bouge")
    S.key("tampon", "pos", f - 1, list(TAMPON_LOCAL))
    hit = toi.stamp(f, "tampon", shake="bonne_reponse", step=False)   # placé par le saut (poignée à portée de main)
    toi.lower(hit + 16, 6)

    # ================= S22 : fin standard ; la pastille devient le bouton =================
    fe = scene_f0(S, "S22")
    outs, wires = [], []
    for id, e in S.ents.items():                # tout ce qui est encore à l'écran, sauf la pastille et « Toi »
        if e.get("parent") or id == "pastille" or id.startswith("toi") or id.startswith("fin"):
            continue
        if S.val(id, "scale", fe - 1) < 1e-3 or S.val(id, "opacity", fe - 1) < 1e-2:
            continue
        if e["type"] == "wire":
            if S.val(id, "draw", fe - 1, 0) > S.val(id, "from", fe - 1, 0):
                wires.append(id)
            continue
        if e["type"] == "shape" and S.val(id, "draw", fe - 1, 1) < 1e-3:
            continue
        outs.append(id)
    out = kit.outro("S22", outs=outs, press="argent.", clear="fade", btn_at=MOVE, bsize=FIN_BSIZE)
    S.set(out["cursor"], opacity=0)             # pas de flèche de souris : le stylo de « Toi »
    f, fp = out["card"], out["press"]
    for w in wires:
        S.key(w, "opacity", f, 0, FADE, "linear")
    S.key("nom_toi", "opacity", f, 0, FADE, "linear")
    kit.ensure("pastille", "z", S.ents["pastille"]["z"])
    S.key("pastille", "z", f, 41)               # au-dessus de la carte (z 40)
    S.key("pastille", "textOp", f, 0, 3, "out")
    S.key("pastille", "text", f + MOVE // 2, T_ABONNER)   # le libellé change quand la pilule est assez étroite
    S.key("pastille", "textOp", f + MOVE // 2, 1, FADE, "out")
    S.key("pastille", "w", f, FIN_W, MOVE, "inOut")
    kit.move("pastille", f, list(FIN_BUTTON), scale=FIN_K)
    S.key("pastille", "opacity", f + MOVE, 0)   # relais : le bouton de la carte paraît dessous (btn_at)
    toi.set_z(f, 42, tool_z=42.5)               # « Toi » et son stylo au-dessus de la carte
    hop_low(toi, f, TOI_REST, 10)
    _set_what(S, "S22", f, "tout s'efface sauf la question et « Toi » ; la carte de fin surgit ; la question descend "
              "au bas de la carte, devient « S’abonner » et grandit : c'est son bouton ; « Toi » redescend")
    hit = toi.tap(fp - TAP + 1, list(FIN_TAP))
    assert hit == fp, (hit, fp)
    _set_what(S, "S22", fp, "« Toi » touche du stylo le coin bas droit du bouton « S’abonner » : il s'enfonce, deux "
              "ondes partent du point touché ; puis plus rien ne bouge")
    for k in range(2):
        S.key(f"fin_onde{k + 1}", "pos", hit - 1, list(FIN_TAP))
    ring(S, "fin_onde1", hit, d=14, s0=0.6, s1=2.1)
    last = ring(S, "fin_onde2", hit + 4, d=14, s0=0.6, s1=2.1)
    toi.lower(hit + 6, 8)
    assert last < film_end(S), (last, film_end(S))
