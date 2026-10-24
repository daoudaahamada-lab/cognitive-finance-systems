"""V11, partie 3 : S15-S22, images 1772-2790 (34 temps forts, 33,9 s). Patrimoine (bloc recomposé, crédit,
liquidités), déménagement à l'étranger, la question au rendez-vous, la réponse du client et la mise à jour de la fiche,
la fin standard.

ÉTAT D'ENTRÉE : ENTRY_P3 épinglé à 1771 (`kit.pin(f0 - 1, ENTRY_P3)`, f0 = scene_f0(S, "S15") = 1772) : etat_initial
de S15 = résultat de S14 (trois barres aux nouveaux niveaux dans la vie, fils encre vers le conseil rouge penché ;
badges famille / enfants / travail au-dessus du client ; L3 rouge, L1-L3 « à revoir » ; étape 2 active).
SORTIE : fin du film (image 2790, FILM_END = 2791).

Tour de revue 1 :
- S15-S17 : le patrimoine se joue dans la colonne de la vie : titre (240, 498), bloc (240, 570, x 45-435) ; le bloc
  naît du bout gauche de la rangée Patrimoine (rien ne traverse la fiche) ; la maison tombe juste sous le bloc et y
  entre par un petit arc ; « vend » : la maison glisse de 60 px et revient ;
- S17 « endettement » : la barre « − Crédit » ROUGE est tirée de la part « Maison » vers le bas et se remplit (dette) ;
  « évolue, » : elle monte de 0,35 à 0,85, trait d'avant tireté ; « liquidités » : UNE grande pièce (r 40) quitte
  « Maison » et tombe dans « Épargne », qui bat (x 1,15) ; « apparaître. » : l'épargne s'élargit ; la maison garde
  son pictogramme ;
- S15, S18, S20 : ce qui a servi se résorbe sur place (le conseil bat), sans traverser l'image ;
- S19 : la pile monte dans la vie comme en S10 (cyan pâle « à revoir », aucun rouge) ; le globe se range en badge ;
- S20 : le conseil ne bouge plus seul ; « rendez-vous, » : « Toi » marche 160 px vers le client, le conseil porté à la
  pointe de son stylo (40 px), le client se tourne vers lui ; « pose » : le stylo se lève SUR le mot ; le vieux fil du conseil se retire (il ne croise plus la
  queue de la bulle) ;
- S21 « Qu’est-ce » : le « ? » du coin se réduit pendant que la question s'écrit, centrée ; « échange ? » : le client
  bondit et RÉPOND (petite bulle « … ») ; ses cinq badges passent dans sa bulle puis montent un à un à leur rangée ;
  la date de sa vie en sort aussi et file vers la pastille ; « C’est » : « Toi » touche la pastille (« nov. 2026 ») ;
  chaque rangée se met à jour à l'arrivée de son badge ;
- S22 : la composition s'efface en 6 images AVANT que la carte grandisse ; la pastille garde « nov. 2026 » jusqu'au
  relais du bouton ; le client s'efface au lieu de rapetisser.
"""
from . import *  # noqa: F401,F403
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, SCALE, STRETCH, TILT  # noqa: F401
from pipeline.story_kit import TAP, r3  # noqa: F401

SORTIR_D = MOVE
BLOC_BORN = (BULLET_X - 40, ROWS_Y[3])          # S15 : le bloc sort du bout gauche de la rangée Patrimoine
BLOC_BORN_K = 0.4
TOKEN_BLOC, TOKEN_BLOC_K = (392, BLOC_C[1]), 0.4   # S17 « patrimoine » : la maison entre au bout droit du bloc
TRUCK_OUT = (-220, TRUCK_C[1])                  # S18 « surtout » : hors champ à gauche
B2_SMALL = (300, 776)                           # S20 « pose » : petite bulle (0,65 : x 183-417, y 704-848)
BADGE_ROW_K = 0.73                              # S21 : un badge (r 30) se pose sur la puce (r 22) de sa rangée
BUBBLE3_K = 0.6                                 # S21 : les badges réunis dans la bulle-réponse
PASTILLE_K_PEAK = 1.3
BTN_W, BTN_H = 380, 112
BTN_K = BTN_H / PASTILLE_H                      # relais pastille -> bouton (w = BTN_W / BTN_K, échelle BTN_K)
FIN_POS = (540, 760)                            # carte de fin (défaut de kit.outro)
FIN_BUTTON = (FIN_POS[0], FIN_POS[1] + 520 / 2 - BTN_H / 2 - 56)   # (540, 908) : centre du bouton
GROW_AT = FADE                                  # S22 : la carte grandit quand la composition s'est effacée


def part(S, kit, c):
    toi, client = c.toi, c.client
    f0 = scene_f0(S, "S15")                                   # 1772
    kit.pin(f0 - 1, ENTRY_P3)                                 # etat_initial de S15 = résultat de S14
    if S.val("client", "scale", f0 - 1) == 0:                 # partie construite seule (WTH_PARTS=p3)
        client.enter(f0 - 10, at=CLIENT_C)
    toi.lower(f0 - 9)                                         # « Toi » bras baissé (sans effet s'il l'est déjà)

    def conseil_top(n):
        return S.to_world("conseil", list(CONSEIL_TOP_LOCAL), n)

    def sortir(pid, f, to, d=SORTIR_D):
        kit.pop(pid, f, from_pt=conseil_top(f - 1), to=list(to))
        S.key(pid, "pos", f, r3(to), d, "out")
        return f + d

    # ======================= S15 : l'étape 3, le patrimoine =======================
    f = kit.at("S15", "Enfin,", "le repère glisse sur l'étape 3, légendée « Patrimoine » ; « Travail » passe à « à "
                                "revoir » ; les rangées Patrimoine et Résidence se surlignent")
    kit.step(f, 2)
    rows_state(S, kit, f, red=None, review=(3, 4), d=9)

    f = kit.at("S15", "décisions", "les fils lâchent le conseil ; les trois barres, leurs légendes et leurs flèches "
                                   "se résorbent sur place, l'une après l'autre ; le conseil bat")
    for k, (jid, *_rest) in enumerate(JAUGES):
        S.key(f"fil_jauge{k + 1}", "from", f + 2 * k, 1, POP, "in")
    fondre(kit, [o for j in JAUGES for o in (f"{j[0]}_mot", f"{j[0]}_fl", j[0])], f, step=1)
    kit.move("conseil", f + 4, list(CONSEIL_C))               # lâché par les fils, il retombe à sa place

    f = kit.at("S15", "déplacent", "une copie cyan de l'épargne sort du bout gauche de la rangée Patrimoine et monte "
                                   "dans la vie en grandissant : un bloc « Épargne »")
    kit.ensure("bloc_epargne", "w", BLOC_W)
    S.key("bloc_epargne", "pos", f - 1, list(BLOC_BORN))
    kit.pop("bloc_epargne", f, scale=BLOC_BORN_K, d=4)
    kit.move("bloc_epargne", f + 4, list(BLOC_C), scale=1)

    f = kit.at("S15", "patrimoine", "le titre « Patrimoine » s'écrit au-dessus du bloc ; un anneau cerne l'euro")
    kit.type("patrimoine_titre", f, rate=1)
    kit.draw("bloc_epargne_ico", f, d=DRAW, track="ring")

    # ======================= S16 : une maison achetée ou vendue =======================
    f = kit.at("S16", "achète", "une maison tombe dans la vie du client, juste sous le bloc « Épargne »")
    kit.drop("evt_token", f, h=150, to=list(TOKEN_C))

    # contrôle muet : « aucun n'a vu l'idée de la vente » ; vendre = la maison donne de l'argent
    f = kit.at("S16", "vend", "une flèche part de la maison et une pièce cyan surgit au bout : vendre la maison "
                              "redonne de l'argent")
    kit.pop("vente_fleche", f, d=6)
    kit.pop("vente_piece", f + 5)
    kit.pulse("vente_piece", f + 5 + POP, peak=1.2, step=3)

    f = kit.at("S16", "immobilier ?", "« Patrimoine : épargne » vire au rouge et sa puce bat deux fois")
    rows_state(S, kit, f, red=3)
    kit.pulse("fiche_L4", f, times=2, step=2, track="pulse")

    # ======================= S17 : le patrimoine se recompose =======================
    f = kit.at("S17", "patrimoine", "la maison saute en petit arc dans le bout droit du bloc en se réduisant")
    kit.vanish("vente_fleche", f, d=6)
    kit.vanish("vente_piece", f, d=6)
    set_z(kit, "evt_token", f, 12.5)                          # au-dessus du bloc (z 12)
    kit.move("evt_token", f, list(TOKEN_BLOC), arc=40, scale=TOKEN_BLOC_K)

    f = kit.at("S17", "recompose,", "l'épargne rétrécit à gauche pendant qu'une part « Maison » grandit à droite ; "
                                    "la maison s'y fond")
    S.key("bloc_epargne", "w", f, EPARGNE_RECOMP[1], MOVE, "inOut")
    kit.move("bloc_epargne", f, [EPARGNE_RECOMP[0], BLOC_C[1]])
    S.key("bloc_epargne_ico", "ring", f, 0, 8, "inOut")      # l'anneau se défait
    kit.ensure("bloc_maison", "w", MAISON_RECOMP[1])
    S.key("bloc_maison", "pos", f - 1, [MAISON_RECOMP[0], BLOC_C[1]])
    kit.pop("bloc_maison", f, d=MOVE, e="inOut")
    kit.vanish("evt_token", f + 2, into="bloc_maison", d=POP)

    f = kit.at("S17", "endettement", "une barre rouge « − Crédit » est tirée de la part « Maison » vers le bas et se "
                                     "remplit : une dette")
    maison = S.to_world("bloc_maison", [0, 0], f - 1)
    kit.ensure("credit", "w", CREDIT_W)
    kit.pop("credit", f, from_pt=maison, to=list(CREDIT_C), d=POP)
    S.key("credit", "value", f + 2, 0.35, 10, "out")

    f = kit.at("S17", "évolue,", "la dette monte : la barre rouge se remplit de 0,35 à 0,85, le niveau d'avant reste "
                                 "marqué d'un trait tireté")
    S.key("credit_trait", "opacity", f, 1)
    S.key("credit", "value", f, 0.85, 12, "out")
    kit.pulse("credit", f + 12, peak=1.08, step=3)

    f = kit.at("S17", "liquidités", "une grande pièce sort de la part « Maison » et tombe dans « Épargne », qui bat : "
                                    "de l'argent redevient disponible")
    maison = S.to_world("bloc_maison", [0, 0], f - 1)
    S.key("piece", "pos", f - 1, r3(maison))
    kit.pop("piece", f, d=6)
    arr = kit.move("piece", f + 2, [EPARGNE_RECOMP[0], BLOC_C[1]], d=MOVE, arc=12)
    kit.vanish("piece", arr, d=5)
    kit.pulse("bloc_epargne", arr, peak=1.15, step=4)

    f = kit.at("S17", "apparaître.", "l'épargne s'élargit pendant que la maison recule ; l'euro bat : de l'argent "
                                     "disponible est apparu")
    S.key("bloc_epargne", "w", f, EPARGNE_FIN[1], MOVE, "inOut")
    kit.move("bloc_epargne", f, [EPARGNE_FIN[0], BLOC_C[1]])
    S.key("bloc_maison", "w", f, MAISON_FIN[1], MOVE, "inOut")
    kit.move("bloc_maison", f, [MAISON_FIN[0], BLOC_C[1]])
    S.key("credit", "pos", f, [MAISON_FIN[0], CREDIT_C[1]], MOVE, "inOut")
    S.key("credit", "w", f, MAISON_FIN[1], MOVE, "inOut")
    S.key("credit_mot", "pos", f, [-MAISON_FIN[1] / 2 - 12, 0], MOVE, "inOut")
    S.key("credit_trait", "pos", f, [round(-MAISON_FIN[1] / 2 + MAISON_FIN[1] * 0.35, 1), 0], MOVE, "inOut")
    kit.draw("bloc_epargne_ico", f + 4, d=DRAW, track="ring")
    kit.pulse("bloc_epargne_ico", f + 4, peak=1.3, step=4)

    # ======================= S18 : un déménagement, à l'étranger =======================
    f = kit.at("S18", "Et", "le patrimoine (bloc, titre, crédit) se résorbe sur place ; un badge "
                            "« patrimoine » se range au-dessus du client ; « Patrimoine » passe à « à revoir »")
    rows_state(S, kit, f, red=None)
    maison = S.to_world("bloc_maison", [0, 0], f - 1)
    kit.pop("badge_token", f, from_pt=maison, to=list(BADGES[3]), d=MORPH)
    fondre(kit, ["bloc_maison", "credit", "bloc_epargne", "patrimoine_titre"], f + 2, step=2)

    f = kit.at("S18", "déménage,", "un camion de déménagement entre par la gauche dans la vie du client")
    S.key("evt_truck", "pos", f - 1, list(TRUCK_FROM))
    S.key("evt_truck", "scale", f - 1, 1)
    kit.move("evt_truck", f, list(TRUCK_C), e="out")

    f = kit.at("S18", "surtout", "le camion repart vers la gauche, hors de l'image")
    g = kit.move("evt_truck", f, list(TRUCK_OUT), d=12, e="in")
    S.key("evt_truck", "scale", g, 0)

    f = kit.at("S18", "l’étranger ?", "un globe tombe dans la vie du client ; « Résidence : France » vire au rouge et "
                                      "sa puce bat")
    impact = kit.drop("evt_globe", f, h=200, to=list(GLOBE_C))
    rows_state(S, kit, impact + 8, red=4)
    kit.pulse("fiche_L5", impact + 8, times=2, step=2, track="pulse")

    # ======================= S19 : fiscalité, résidence, produits =======================
    pile = []
    for k, (pid, word) in enumerate((("pile_fiscalite", "Fiscalité,"), ("pile_residence", "résidence,"),
                                     ("pile_produits", "produits"))):
        nom = dict(PILE)[pid]
        f = kit.at("S19", word, f"« {nom} » sort du conseil et se pose en bas de la colonne, qui monte d'une case" +
                   (" ; le globe se range en badge « résidence » au-dessus du client" if k == 0 else ""))
        if k == 0:
            kit.vanish("evt_globe", f, into=list(BADGES[4]), d=MORPH)
            kit.pop("badge_globe", f + 2, from_pt=GLOBE_C, to=list(BADGES[4]), d=MORPH)
        pile_push(kit, pile, pid, f, conseil_top(f - 1))

    f = kit.at("S19", "France", "la valeur rouge « France » tremble et le badge « résidence » bat : le pays change")
    kit.shake("fiche_L5", f, 6)
    kit.pulse("badge_globe", f, peak=1.25, step=4)

    f = kit.at("S19", "change", "les trois pilules passent au cyan pâle, « à revoir », et tremblent, de bas en haut")
    for k, pid in enumerate(pile):
        S.key(pid, "fill", f + 2 * k, LIGHT, 5, "out")
        kit.shake(pid, f + 2 * k, 5)

    # ======================= S20 : au rendez-vous, une question ouverte =======================
    f = kit.at("S20", "Alors,", "la pile se résorbe sur place, de haut en bas ; le conseil bat ; puis les cinq "
                                "badges de la vie battent l'un après l'autre en face des cinq rangées restées rouges : "
                                "les changements sont chez le client, pas dans la fiche")
    g = fondre(kit, pile[::-1], f, step=2)
    for i, bid in enumerate(BADGE_IDS):
        kit.pulse(bid, g + 3 * i, peak=1.3, step=3)
        kit.pulse(f"fiche_L{i + 1}", g + 3 * i, times=1, step=3, track="pulse")

    f = kit.at("S20", "rendez-vous,", "« Toi » marche vers le client en portant son conseil à la "
                                      "pointe du stylo ; le client se tourne vers lui : c'est le rendez-vous")
    g = toi.walk(f, TOI_RDV[0], low=True)
    kit.move("conseil", f, list(CONSEIL_RDV), d=g - f, e="inOut")   # porté : il suit la pointe du stylo
    client.lean_to(f + 4, 5, TILT)

    f = kit.at("S20", "pose", "« Toi » lève le stylo : un « ? » en sort et vole au-dessus de la vie du client ; une "
                              "bulle grandit autour, la queue vers « Toi » ; le vieux fil du conseil se retire")
    toi.reach(f, list(Q_PEN), d=8)
    tip = r3(toi.tip(f + 7))
    kit.ensure("question", "gs", Q_GS_S20)
    S.key("question", "gs", f - 1, Q_GS_S20)
    kit.pop("question", f + 6, from_pt=tip, to=tip, d=6)
    kit.move("question", f + 9, list(B2_SMALL), arc=60)
    S.key("bulle2", "pos", f + 14, list(B2_SMALL))
    kit.pop("bulle2", f + 15, scale=BULLE2_K0, d=SCALE)
    toi.lower(f + 12, 10)
    S.key("conseil_fil", "from", f, 1, 9, "in")
    S.key("conseil_fil", "draw", f + 9, 0)

    f = kit.at("S20", "ouverte.", "la bulle s'ouvre en grand, la queue sur « Toi » ; le « ? » glisse dans son coin")
    S.keys("bulle2", f, SCALE, "out", scale=1, pos=list(BULLE2_C))
    kit.move("question", f, list(Q_COIN), d=SCALE, e="out")
    S.key("question", "gs", f, Q_GS_COIN, SCALE, "out")

    # ======================= S21 : la question ; la réponse du client ; la fiche se met à jour =======================
    f = kit.at("S21", "« Qu’est-ce", "le « ? » du coin se résorbe et la question s'écrit, centrée dans la bulle : "
                                     "« Qu’est-ce qui a changé depuis notre dernier échange ? »")
    kit.vanish("question", f, d=7)
    kit.type("question_texte", f, rate=1)

    f = kit.at("S21", "dernier", "la pastille « mars 2023 » de la fiche bat et descend vers « Toi » : la date du "
                                 "dernier échange")
    kit.pulse("pastille", f, peak=PASTILLE_K_PEAK, step=5)
    kit.move("pastille", f, list(PASTILLE_LOW))

    f_cest = S.word_after("C’est", f)                         # temps fort « C’est » (posé plus bas)
    f = kit.at("S21", "échange ? »", "le client bondit et répond : une petite bulle « … » sort de sa tête ; ses cinq "
                                     "badges y entrent, puis la date de sa vie en sort")
    client.hop(f, CLIENT_C, 8, h=14)
    client.lean_to(f + 8, 8, TILT)
    kit.pop("bulle3", f, d=POP)
    arrive = []
    for i, bid in enumerate(BADGE_IDS):
        set_z(kit, bid, f, 17.5)                              # au-dessus de la fiche et des bulles
        kit.move(bid, f + 2 + 2 * i, list(BULLE3_C), d=8, e="inOut", scale=BUBBLE3_K)
        a = f_cest + 3 * i                                    # arrivée sur la puce de la rangée i
        kit.move(bid, a - 11, [BULLET_X, ROWS_Y[i]], d=11, e="inOut", scale=BADGE_ROW_K)
        arrive.append(a)
    S.key("vie", "pos", f_cest - 11, list(BULLE3_C))
    S.key("vie", "text", f_cest - 11, T_NOV)
    kit.pop("vie", f_cest - 10, scale=0.8, d=5)
    kit.move("vie", f_cest - 9, list(PASTILLE_LOW), d=9, e="inOut", scale=1)

    f = kit.at("S21", "C’est", "« Toi » touche la pastille : la date de la vie s'y fond, elle passe à « nov. 2026 » ; "
                               "chaque badge du client arrive sur sa rangée, l'ancienne valeur tombe et la nouvelle "
                               "s'écrit, rangée après rangée")
    assert f == f_cest, (f, f_cest)
    hit = toi.tap(f - TAP + 1, list(PASTILLE_TAP))
    assert hit == f, (hit, f)
    S.key("vie", "scale", f, 0, 3, "in")
    S.key("vie", "opacity", f + 3, 0)
    kit.ensure("pastille", "textOp", 1)
    S.key("pastille", "textOp", f, 0, 2, "out")
    S.key("pastille", "text", f + 2, T_NOV)
    S.key("pastille", "textOp", f + 2, 1, FADE, "out")
    S.key("pastille_rouge", "opacity", f, 0, FADE, "out")
    kit.pulse("pastille", f + 2, peak=1.12, step=3)
    toi.lower(hit + 6, 8)
    for i, a in enumerate(arrive):
        lid = f"fiche_L{i + 1}"
        kit.ensure(lid, "fall", 0)
        S.key(lid, "fall", a, 1, POP, "in")
        S.key(lid, "red", a, 0, 6, "out")
        S.key(lid, "slotFill", a, 1, 9, "out")
        S.key(f"fiche_hl{i + 1}", "opacity", a, 0, 9, "out")
        kit.ensure(lid, "flash", 0)
        S.key(lid, "flash", a, 1, 2, "out")
        S.key(lid, "flash", a + 2, 0, 4, "inOut")
        kit.type(f"fiche_v{i + 1}", a + 3)
        kit.vanish(BADGE_IDS[i], a, d=5)
    kit.vanish("bulle3", arrive[-1] - 4, d=6)

    f = kit.at("S21", "plus", "le repère se coche aux trois étapes ; le conseil se redresse, perd son rouge, se "
                              "remplit de cyan et se relie à la fiche à jour")
    for k in range(3):
        kit.ensure("marqueur", f"done{k}", 0)
        S.key("marqueur", f"done{k}", f + 3 * k, 1, 6, "out")
    kit.pop("marqueur_fait3", f + 6, d=5)                     # le disque actif garde son chiffre : pastille cochée
    kit.draw("marqueur_fait3_coche", f + 8, 6)
    S.key("conseil", "rot", f, 0, POP, "out")
    S.key("conseil_rouge", "opacity", f, 0, FADE, "out")
    S.key("conseil", "fill", f, CYAN, POP, "out")
    kit.draw("conseil_fil2", f + 4, d=POP)

    kit.hold("S21", "l’entretien.", "tenue : fiche à jour « nov. 2026 », repère coché, conseil cyan relié ; rien ne "
                                    "bouge jusqu'à « Abonne-toi »")

    # ======================= S22 : fin standard ; le bouton touché du stylo =======================
    outs = ["fiche", "cadre", "punaise", "bulle2", "question_texte", "marqueur", "marqueur_fait3", "conseil",
            "conseil_fil2", "nom_toi"]
    glide = GROW_AT + MORPH                                   # la pastille arrive au bouton quand la carte est pleine
    out = kit.outro("S22", outs=outs, clear="fade", btn_at=glide, press="comprendre", grow_at=GROW_AT,
                    title_at=GROW_AT + MORPH - 3, bsize=round(34 * BTN_K, 1))
    f, fp = out["card"], out["press"]
    S.set(out["cursor"], opacity=0)                           # pas de pointeur de souris : le stylo de « Toi »
    for bt in S.beats:
        if bt["scene"] == "S22" and bt["frame"] == f:
            bt["what"] = ("le client, la fiche, la bulle, le repère et le conseil s'effacent ; puis la carte de fin "
                          "grandit ; la pastille « nov. 2026 » descend et grandit jusqu'au bouton « S’abonner »")
        elif bt["scene"] == "S22" and bt["frame"] == fp:
            bt["what"] = ("le stylo de « Toi » touche le bas du bouton « S’abonner », qui s'enfonce ; puis plus rien "
                          "ne bouge")
    S.key("client", "opacity", f, 0, FADE, "linear")         # s'efface (ne rapetisse pas sur la carte)
    S.key("client", "scale", f + FADE, 0)
    set_z(kit, "pastille", f, 41)                             # au-dessus de la carte (z 40)
    kit.ensure("pastille", "w", PASTILLE_W)
    S.key("pastille", "w", f, round(BTN_W / BTN_K, 2), glide, "inOut")
    kit.move("pastille", f, list(FIN_BUTTON), d=glide, e="inOut", scale=round(BTN_K, 4))
    S.key("pastille", "textOp", f + glide - 4, 0, 3, "out")   # « nov. 2026 » jusqu'au relais, puis le bouton
    S.key("pastille", "opacity", f + glide, 0)                # relais exact : le bouton de la carte paraît dessous

    toi.set_z(fp - TAP - 4, S.ents[toi.id]["z"], tool_z=44)   # bras et stylo au-dessus de la carte
    hit = toi.tap(fp - TAP + 1, list(FIN_BTN_TAP))
    assert hit == fp, (hit, fp)
    end = toi.lower(hit + 6, 8)
    assert end < FILM_END, (end, FILM_END)
