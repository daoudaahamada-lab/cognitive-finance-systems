"""V01, partie 1 : S01-S08, images 0-609 (37 temps forts, 20,3 s). Le dossier dispersé, le temps qui fond, puis
« 1 · Limiter » : le cadre ouvert par le stylo du conseiller et fermé derrière l'IA, l'outil scellé par le cabinet,
le mur qui retient le mail que le conseiller voulait glisser vers une IA grand public.

État d'entrée : celui de la distribution à l'image 0 (= etat_initial de S01) : horloge de verre héroïne (CLOCK_S01,
440 px), pile nette des 4 documents (PILE_S01) coiffée de la pastille « Client · 9 h » (PASTILLE_S01) ; rien d'autre.

Temps forts (image du film, calés par kit.at ; « mot n » = début du mot quand l'attaque audible le devance) :
S01  Client=0 (tenue)  9=16  heures ?=22
S02  L’IA=34 (mot 35)  prépare,=50  tu=68  décides.=73
S03  Le=99 (mot 98)  problème=110  avant=123  rendez-vous :=134
S04  temps=164  part=171  dans=177  recherche,=184  pas=210 (mot 208)  conseil.=221
S05  Première=251 (mot 249)  tu=282 (mot 281)  limites=286  l’IA=306  lire.=323
S06  lit=351  uniquement=359  dossier=379  client,=387
S07  dans=408 (mot 410)  outil=422  validé=430  par=453 (mot 451)  cabinet.=463
S08  Aucune=486  client=507  IA=537  grand=551  non=574  encadrée.=580

Scène par scène (tour de revue 1) :
- S01 « 9 » : la pastille bat. « heures ? » : les 4 documents glissent vers DOC_SPOTS (8 images, décalés d'une) :
  posés à l'image 32, avant « L’IA ».
- S02 « L’IA » : l'horloge se range en badge ; la tête IA, déjà à moitié dans l'image (x -60), glisse en 350 ms.
  « prépare, » : le faisceau empile les documents, la pastille se clipse. « tu » : le conseiller surgit (4 images).
  « décides. » : son stylo touche la pile SUR le mot (tap commencé 4 images avant, contact à 73) ; coche pleine.
- S03 « Le » : coche, pilules et IA sortent. « problème » : ◀◀ x 1,5 au-dessus de la pile, tenu jusqu'à ce que les
  documents soient revenus à leurs places. « avant » : deux cartes « Client · 14 h » glissent ENTRE les documents, un
  coin sur l'un d'eux (calques mêlés). « rendez-vous : » : la barre pleine de cyan se tend.
- S04 : 4 sauts (seule la traînée du saut en cours se voit, en tirets encre, effacée au saut suivant) ; à chaque saut
  un bloc se détache de la barre, tombe CYAN le long d'une traînée tiretée jusqu'à la carte fouillée et ne vire au
  gris (70 %) qu'en s'y posant. 4e saut sur la pilule d'une carte « Client · 14 h » : la carte tremble, sa pilule bat,
  il recule de 90 px penché en arrière. « pas » : le bout cyan bat. « conseil. » : la pastille bat et le client naît
  de son pictogramme, puis vole sous le bout cyan.
- S05 « Première » : repère légendé (34 px) ; le client rentre dans le pictogramme de la pastille ; documents en 2 x 2
  à l'échelle 1 ; cartes grises au bord droit ; le conseiller va dehors, en bas à droite (ADV_OUT). « tu » : la pointe
  de son stylo va sur le coin bas droit de la future zone. « limites » : le cadre en tirets part de la pointe et en
  fait le tour, en laissant ouvert le coin bas gauche. « l’IA » : l'IA entre par la gauche, par l'ouverture, dans le
  coin libre ; puis le tracé se referme derrière elle jusqu'au stylo. « lire. » : cône de lecture.
- S06 « lit » : lecture. « uniquement » : rayon pointillé vers la carte grise du bas, arrêté sur le cadre : 3 traits
  d'impact de 40 px, le bord se creuse de 12 px et tremble, le rayon reste 10 images contre le mur puis se retire ; la
  carte grise ne s'allume pas. « dossier » : pile, « Mail client » dessus. « client, » : la pastille en onglet.
- S07 « dans » : trait plein, les cartes grises sortent ; le conseiller RESTE dehors. « outil » : barre de titre (64 px),
  la pastille titre. « validé » : un grand sceau (96 px) tombe DANS la fenêtre, sous la légende du repère ; la
  fenêtre encaisse. « par » : une coche ivoire épaisse s'y trace, le sceau bat. « cabinet. » : le sceau vole et se
  range au bout de la barre de titre, où il s'ouvre en « ✓ Cabinet » (32 px).
- S08 « Aucune » : la fenêtre (x 0,88) se range à gauche ; le conseiller va en bas à droite, hors de la fenêtre.
  « client » : le curseur sort de la pointe de son stylo (un fil encre les relie) et prend le « Mail client ».
  « IA » : l'IA grand public (verre gris cerné d'encre, tournée vers la fenêtre) ; sa foule grise ; chaque figurine
  envoie une carte grise dans sa tête. « grand » : le curseur traîne le mail. « non » : le mail s'écrase contre le mur
  (x 0,85), le mur s'épaissit, 3 traits d'impact restent marqués ; le curseur pousse et tremble. « encadrée. » : le
  mail revient tout droit sur la pile ; le curseur rentre dans le stylo ; l'IA grand public reste entière.
Raccord : à l'image 609, tout est exactement dans ENTRY_P2 (vérifié en fin de partie : un écart est signalé par
kit.warn).
"""
import math

from pipeline.story import DROP, FADE, MORPH, MOVE, POP
from pipeline.story_kit import frames, lerp, r3

from . import (ADV_OUT, ADV_RECOIL, ADV_S02, ADV_S08, BAR_C, BAR_X0, BAR_W, BLOCK, CHOC, CLIENT_S04,
               CLIENT_S04_SCALE, CLOCK_BADGE, CLOCK_BADGE_SCALE, CLOCK_S01, CX, DOC_GRID_S05, DOC_GRID_SCALE,
               DOC_PILE_SCALE, DOC_SPOTS, DOC_TILTS, ENTRY_P2, FRAME_C, FRAME_TOP, FRAME_W, FRAME_X0, FRAME_X1,
               FRAME_Y1, GREY_EDGE_S05, GREY_EDGE_SCALE, GREY_SPOTS, IA_PUB_SCALE, IA_S02, IA_S02_SCALE, IA_S05,
               INK_25, MARKER_Y, PASTILLE_S01, PILE_S01, PILE_S02, PILE_S06, PILE_SLOT, PILE_TICK_S02, PILL_ICON,
               S04_HOPS, SEAL_S07, SEAL_SLOT, TITLE_S07, WALL_X, WIN_S08_POS, WIN_S08_SCALE, pile_pt, pile_z,
               scene_f0, vanish, win_map)

DOC_IDS = ["doc1", "doc2", "doc3", "doc4"]
GREY_IDS = ["carte_grise1", "carte_grise2"]
HOP_CARDS = ["doc2", "doc1", "doc3", "carte_grise2"]      # cartes fouillées en S04, dans l'ordre des sauts
PASTILLE_S02 = (PILE_S02[0], PILE_S02[1] - 120)          # même place relative qu'en S01 : coiffe la pile
PASTILLE_S05 = (580, 695)                                # au centre du groupe 2 x 2
PASTILLE_S06 = (TITLE_S07[0], FRAME_TOP + 14)            # sur le bord haut du cadre, sous la légende du repère
BLOCK_LAND = 62                                          # le bloc gris tombe sur le bas de la carte (sous le titre)
CORNER_BR = (FRAME_X1, FRAME_Y1)                         # le cadre part de la pointe du stylo (S05 « tu »)
FRAME_OPEN = 0.651                                       # tracé ouvert : il s'arrête sur le bord gauche à y ≈ 860


def _pt(p):
    return [round(p[0], 3), round(p[1], 3)]


def _rot(v, deg):
    t = math.radians(deg)
    return [v[0] * math.cos(t) - v[1] * math.sin(t), v[0] * math.sin(t) + v[1] * math.cos(t)]


def _quad(p0, p1, p2, t):
    u = 1 - t
    return [u * u * p0[k] + 2 * u * t * p1[k] + t * t * p2[k] for k in (0, 1)]


def _check_entry_p2(S, kit, n):
    """Raccord : l'état à l'image n doit être exactement ENTRY_P2 (sinon : avertissement)."""
    for id, tracks in ENTRY_P2.items():
        for track, v in tracks.items():
            cur = S.val(id, track, n, 0 if track not in ("pos",) else None)
            if isinstance(v, (list, tuple)):
                bad = cur is None or max(abs(a - b) for a, b in zip(cur, v)) > 0.5
            else:
                bad = abs((cur or 0) - v) > 1e-3
            if bad:
                kit.warn(f"raccord p1 -> p2 : {id}.{track} vaut {cur} à l'image {n}, ENTRY_P2 attend {v}")


def part(S, kit, c):
    toi, client = c.toi, c.client

    # État d'entrée = distribution (etat_initial de S01) : l'épingle ne fait que le redire.
    kit.pin(-1, {"horloge": {"pos": list(CLOCK_S01), "scale": 1}, "pastille": {"pos": list(PASTILLE_S01), "scale": 1},
                 **{d: {"pos": pile_pt(PILE_S01, i), "rot": 0, "scale": 1} for i, d in enumerate(DOC_IDS)}})

    # ======================= S01 : Client à 9 heures ? =======================
    kit.hold("S01", "Client", "tenue : l'horloge de 9 h et la pile coiffée de « Client · 9 h » sont là dès l'image 0")
    f = kit.at("S01", "9", "la pastille « Client · 9 h » bat une fois (×1,12)")
    S.key("pastille", "scale", f, 1.12, 4, "out")
    S.key("pastille", "scale", f + 4, 1, 5, "inOut")
    f = kit.at("S01", "heures ?", "la pile s'étale : les 4 documents glissent à 4 places séparées ; la pastille reste "
                                  "seule au centre")
    for i, d in enumerate(DOC_IDS):
        g = f + i                                        # 8 images, décalés d'une : posés à l'image 32
        S.keys(d, g, 8, "out", pos=_pt(DOC_SPOTS[i]), rot=DOC_TILTS[i])
        S.key(d, "sh", g, 6, 8, "out")

    # ======================= S02 : L'IA prépare, tu décides. =======================
    f = kit.at("S02", "L’IA", "l'horloge se range en badge en haut à droite ; la tête IA, déjà à moitié dans l'image, "
                              "glisse depuis la gauche, pilule « IA » dessous")
    kit.move("horloge", f, CLOCK_BADGE, d=10, e="inOut", scale=CLOCK_BADGE_SCALE)
    S.key("ia", "z", f - 1, 12.6)                    # S02 : l'IA passe devant les cartes encore étalées
    S.key("ia_pill", "z", f - 1, 12.7)
    S.key("ia", "pos", f - 1, [-60, IA_S02[1]])
    S.key("ia", "scale", f, IA_S02_SCALE)            # visible sur le mot, à moitié dans l'image
    kit.move("ia", f, IA_S02, d=MORPH, e="out")

    f = kit.at("S02", "prépare,", "le faisceau pointillé de l'IA tire les documents un par un : ils se redressent et "
                                  "s'empilent au centre ; la pastille se clipse sur la pile")
    S.key("faisceau_range", "pb", f - 1, list(PILE_S02))
    kit.draw("faisceau_range", f, 6)
    order = [2, 0, 3, 1]                             # du plus proche de l'IA au plus loin : doc3, doc1, doc4, doc2
    for k, i in enumerate(order):
        d, g = DOC_IDS[i], f + 4 * k
        S.keys(d, g, MORPH, "inOut", pos=pile_pt(PILE_S02, i), rot=0)
        S.key(d, "sh", g, 6 if i == 3 else 0, MORPH, "out")
    kit.move("pastille", f + 8, PASTILLE_S02, d=9, e="out")
    S.key("faisceau_range", "draw", f + 14, 0, 6, "inOut")      # le faisceau rentre dans la tête

    f_tu = kit.at("S02", "tu", "le conseiller « Toi » (figurine encre, stylo en main) surgit en bas à droite, pilule "
                               "« Toi » sous ses pieds")
    toi.enter(f_tu, at=ADV_S02, d=3)
    kit.pop("toi_pill", f_tu, d=POP)

    f = kit.at("S02", "décides.", "le stylo touche le coin de la pile sur le mot : au contact, une coche pleine cyan "
                                  "profond se trace")
    hit = toi.tap(f - 4, list(PILE_TICK_S02), d=5)   # contact sur l'image du mot
    kit.draw("coche_pile", hit, 6)
    toi.rest(hit + 6, d=8)

    # ======================= S03 : Le vrai problème avant un rendez-vous : =======================
    f = kit.at("S03", "Le", "la coche se réduit en point, les pilules « IA » et « Toi » s'effacent ; l'IA rétrécit et "
                            "sort par la gauche")
    vanish(kit, "coche_pile", f, d=6)
    kit.fade("ia_pill", f, 0)
    kit.fade("toi_pill", f, 0)
    S.key("toi_pill", "scale", f + FADE, 0)
    kit.vanish("ia", f, into=[-90, IA_S02[1]], d=9)
    S.key("ia", "z", f + 10, 4)
    S.key("ia_pill", "z", f + 10, 4.1)

    f = kit.at("S03", "problème", "◀◀ (x 1,5) au-dessus de la pile : les documents refont leur trajet à l'envers, "
                                  "avec traits de vitesse, jusqu'à leurs 4 places ; la pastille revient au centre")
    kit.pop("rembobine", f, scale=1.5, d=6)
    for i, d in enumerate(DOC_IDS):
        S.keys(d, f, MORPH, "inOut", pos=_pt(DOC_SPOTS[i]), rot=DOC_TILTS[i])
        S.key(d, "sh", f, 6, MORPH, "out")
        for j in range(3):
            v = f"vitesse{i + 1}_{j + 1}"
            S.key(v, "scale", f, 1, 2, "out")
            S.key(v, "scale", f + 8, 0, 3, "out")
    kit.move("pastille", f, PASTILLE_S01, d=MORPH)
    vanish(kit, "rembobine", f + MORPH, d=4)          # tenu jusqu'à ce que les 4 documents soient posés

    f = kit.at("S03", "avant", "deux cartes grises « Client · 14 h » glissent ENTRE les documents, un coin posé sur "
                               "l'un d'eux : les dossiers se mêlent")
    g = GREY_IDS[0]
    S.key(g, "pos", f - 1, [-130, GREY_SPOTS[0][1]])
    S.key(g, "scale", f, 1)
    kit.move(g, f, GREY_SPOTS[0], d=MOVE)
    g = GREY_IDS[1]
    S.key(g, "pos", f - 1, [800, GREY_SPOTS[1][1] - 20])
    kit.pop(g, f, scale=1)
    kit.move(g, f, GREY_SPOTS[1], d=MOVE, e="out")

    f = kit.at("S03", "rendez-vous :", "une barre pleine de cyan se tend du badge horloge vers la gauche (réserve de "
                                       "temps jusqu'à 9 h)")
    right = BAR_X0 + BAR_W
    S.key("barre", "pos", f - 1, [right, MARKER_Y])
    S.key("barre", "w", f - 1, 0)
    S.key("barre", "scale", f - 1, 1)
    S.key("barre", "w", f, BAR_W, 9, "out")
    S.key("barre", "pos", f, list(BAR_C), 9, "out")

    # ======================= S04 : ton temps part dans la recherche, pas dans le conseil. =======================
    words = ["temps", "part", "dans", "recherche,"]
    whats = ["1er saut, sur « Relevé PEA » ; un bloc cyan se détache de la barre et tombe sur la carte, gris à "
             "l'arrivée", "2e saut, sur « Avis d’impôt » ; 2e bloc", "3e saut, à côté du « Mail client » ; 3e bloc",
             "4e saut, sur une carte « Client · 14 h » : elle tremble, sa pilule bat ; 4e bloc ; il recule penché en "
             "arrière : mauvais dossier"]
    beats = [kit.at("S04", w, t) for w, t in zip(words, whats)]
    bw = BLOCK * BAR_W
    for k, f in enumerate(beats):
        nxt = beats[k + 1] if k + 1 < len(beats) else f + 7
        d = max(4, min(7, nxt - f))
        p0 = S.val("toi", "pos", f - 1)
        dist = math.dist(p0, S04_HOPS[k])
        toi.hop(f, S04_HOPS[k], d, h=min(70, 18 + 0.1 * dist))
        kit.draw(f"traine{k + 1}", f, d, e="inOut")                # seule la traînée du saut en cours
        if k:
            kit.fade(f"traine{k}", f, 0, d=6)
        # la jauge perd 22 % à gauche ; le bloc naît à cette place et tombe CYAN sur la carte, gris à l'arrivée
        b, ch = f"bloc{k + 1}", f"chute{k + 1}"
        slot = [BAR_X0 + bw * (k + 0.5), MARKER_Y]
        S.key("barre", "value", f, round(1 - BLOCK * (k + 1), 4))
        S.key(b, "scale", f, 1)
        S.set(b, z=5.6)
        S.key(b, "z", f + 1, 12.6)                               # tombe SUR la carte (au-dessus des cartes)
        card = HOP_CARDS[k]
        cpos, tilt = S.val(card, "pos", f), S.val(card, "rot", f)
        off = _rot([0, BLOCK_LAND], tilt) if card.startswith("doc") else [0, 40]
        land = _pt([cpos[0] + off[0], cpos[1] + off[1]])
        S.key(b, "pos", f + 1, land, DROP, "out")
        S.key(b, "rot", f + 1, tilt, DROP, "out")
        arr = f + 1 + DROP
        S.key(b, "fill", arr - 1, INK_25, 4, "out")              # gris seulement en se posant
        S.key(b, "opacity", arr - 1, 0.7, 4, "out")
        S.key(ch, "pa", f, _pt(slot))
        S.key(ch, "pb", f, land)
        kit.draw(ch, f + 1, DROP, e="out")                       # la traînée suit le bloc
        kit.fade(ch, arr, 0, d=6)
    f4 = beats[-1]
    land4 = f4 + max(4, min(7, 7))
    kit.shake("carte_grise2", land4, amp=6, axis="x")            # la carte de l'autre client tremble
    kit.pulse("carte_grise2_pill", land4, peak=1.2, step=3)
    last = land4 + 1
    toi.hop(last, ADV_RECOIL, 7, h=0, lean=-9)                   # recul de 90 px, penché en arrière
    kit.fade("traine4", last, 0, d=6)

    f = kit.at("S04", "pas", "le conseiller reste arrêté ; le bout cyan restant (12 %) contre l'horloge bat une fois")
    S.key("bout", "scale", f, 1)                                 # posé exactement sur ce qui reste de la jauge
    S.key("bout", "scale", f + 1, 1.15, 4, "out")
    S.key("bout", "scale", f + 5, 1, 5, "inOut")
    f = kit.at("S04", "conseil.", "la pastille bat et le client de 9 h naît de son pictogramme, puis vole se poser "
                                  "sous le bout cyan")
    kit.pulse("pastille", f, peak=1.12, step=3)
    icon0 = S.to_world("pastille", PILL_ICON, f - 1)
    via = [700, 900]                                 # vers la droite d'abord : loin du conseiller
    S.key("client", "pos", f - 1, _pt(icon0))
    S.key("client", "scale", f - 1, 0)
    S.key("client", "opacity", f, 1)
    S.path("client", f, 13, "inOut", lambda p: _quad(icon0, via, CLIENT_S04, p),
           lambda p: 0.15 + (CLIENT_S04_SCALE - 0.15) * p)

    # ======================= S05 : Première étape : tu limites ce que l'IA peut lire. =======================
    f = kit.at("S05", "Première", "la barre, le bout cyan et l'horloge se contractent en 3 cercles légendés « Limiter, "
                                  "Exiger, Relire », le 1 allumé ; le client rentre dans le pictogramme de la pastille ; "
                                  "les documents se regroupent, la pastille dessus ; les cartes grises glissent au bord "
                                  "droit ; le conseiller va dehors, en bas à droite")
    xs = S.ents["marqueur"]["p"]["xs"]
    discs = [[CX + x, MARKER_Y] for x in xs]
    for id, disc in zip(["bout", "barre", "horloge"], discs):
        vanish(kit, id, f, into=disc, d=MORPH)
    kit.pop("marqueur", f, d=MORPH)
    for k in range(4):
        vanish(kit, f"bloc{k + 1}", f, d=MORPH)
    for i, d in enumerate(DOC_IDS):
        S.keys(d, f, MOVE, "inOut", pos=_pt(DOC_GRID_S05[i]), scale=DOC_GRID_SCALE, rot=0)
    kit.move("pastille", f, PASTILLE_S05, d=MOVE)
    for g, at in zip(GREY_IDS, GREY_EDGE_S05):
        kit.move(g, f, at, d=MOVE, scale=GREY_EDGE_SCALE)
        S.key(f"{g}_pill", "scale", f, 0.75, MOVE, "inOut")     # sa pilule tient sous x 940
    # le client rentre dans le pictogramme de la pastille (qui se déplace) : image par image
    c0, s0, dc = S.val("client", "pos", f - 1), S.val("client", "scale", f - 1), 12
    for n, p in frames(f, dc, "inOut"):
        tgt = S.to_world("pastille", PILL_ICON, n)
        S.key("client", "pos", n, _pt(lerp(c0, tgt, p)), 1, "linear")
        S.key("client", "scale", n, round(max(0.04, s0 * (1 - p)), 4), 1, "linear")
    S.key("client", "scale", f + dc, 0)
    S.key("client", "opacity", f + dc, 0)
    toi.walk(f, ADV_OUT, d=MOVE)                     # il laisse la place au dossier regroupé, dehors en bas à droite

    f = kit.at("S05", "tu", "la pointe de son stylo se pose sur le coin bas droit de la future zone")
    toi.reach(f, list(CORNER_BR), d=4)

    f = kit.at("S05", "limites", "un cadre en tirets cyan profond part de la pointe du stylo et fait le tour de la zone "
                                 "(documents et coin libre), en laissant ouvert le coin bas gauche")
    kit.draw("cadre", f, 19, e="inOut", to=FRAME_OPEN)

    f = kit.at("S05", "l’IA", "la tête IA entre par la gauche, par l'ouverture, dans le coin libre ; le tracé se "
                              "referme derrière elle jusqu'au stylo")
    S.key("ia", "pos", f - 1, [-110, IA_S05[1]])
    S.key("ia", "scale", f, 1)
    S.key("ia", "opacity", f, 1)
    S.key("ia_pill", "opacity", f - 1, 1)
    kit.move("ia", f, IA_S05, d=MORPH, e="out")
    g = kit.draw("cadre", f + 8, 8, e="inOut", to=1)            # le stylo ferme la zone derrière l'IA
    toi.rest(g, 8)

    f = kit.at("S05", "lire.", "son faisceau s'ouvre en cône sur les 4 documents, coupé net par le cadre")
    kit.pop("cone", f, d=POP)

    # ======================= S06 : Elle lit uniquement le dossier client, =======================
    f = kit.at("S06", "lit", "lecture : les traits gris de chaque document passent au cyan, l'un après l'autre")
    for i, d in enumerate(DOC_IDS):
        S.key(d, "read", f + 3 * i, 1, 12, "out")

    f = kit.at("S06", "uniquement", "un rayon pointillé de l'IA vise la carte grise du bas et s'arrête net sur le bord du "
                                    "cadre : 3 traits d'impact, le bord se creuse et tremble ; le rayon reste contre le "
                                    "mur, puis se retire ; la carte grise n'est pas touchée")
    apex = S.to_world("ia", c.brain_front, f)
    target = S.val("carte_grise2", "pos", f)
    target = [target[0], target[1] + 60]             # le bas de la carte : le rayon passe sous les dates
    hy = apex[1] + (target[1] - apex[1]) * (FRAME_X1 - 4 - apex[0]) / (target[0] - apex[0])
    S.key("rayon", "pb", f - 1, _pt([FRAME_X1 - 4, hy]))
    kit.draw("rayon", f, 6, e="in")
    hit = f + 5
    S.key("impact1", "pos", f - 1, _pt([FRAME_X1 + 2, hy]))
    S.key("bosse", "pos", f - 1, _pt([FRAME_X1, hy]))
    kit.pop("impact1", hit, d=2)
    kit.pop("bosse", hit, d=2)
    kit.shake("bosse", hit + 2, amp=8, axis="x")
    S.key("rayon", "draw", hit + 10, 0, 6, "inOut")             # tenu 10 images contre le mur, puis retiré
    vanish(kit, "bosse", hit + 10, d=6)
    vanish(kit, "impact1", hit + 12, d=6)

    f = kit.at("S06", "dossier", "les 4 documents glissent en une pile décalée, le « Mail client » dessus ; le cône se "
                                 "replie")
    for i, d in enumerate(DOC_IDS):
        slot = PILE_SLOT[i]
        S.keys(d, f, MORPH, "inOut", pos=pile_pt(PILE_S06, slot), scale=DOC_PILE_SCALE)
        S.key(d, "sh", f, 6 if slot == 3 else 0, MORPH, "out")
        S.key(d, "z", f, pile_z(slot))
    vanish(kit, "cone", f, d=MORPH)

    f = kit.at("S06", "client,", "la pastille « Client · 9 h » se clipse sur le bord haut du cadre, au-dessus de la "
                                 "pile")
    kit.move("pastille", f, PASTILLE_S06, d=9, e="out")
    S.key("pastille", "scale", f + 9, 1.08, 3, "out")
    S.key("pastille", "scale", f + 12, 1, 4, "inOut")

    # ======================= S07 : dans un outil validé par ton cabinet. =======================
    f = kit.at("S07", "dans", "les tirets du cadre deviennent un trait plein ; les cartes grises sortent par la "
                              "droite ; le conseiller reste dehors, en bas à droite")
    S.key("outil", "scale", f - 1, 1)
    S.key("outil", "opacity", f - 1, 0)
    kit.fade("outil", f, 1, d=8)
    kit.fade("cadre", f, 0, d=8)
    S.key("cadre", "scale", f + 8, 0)
    for g in GREY_IDS:      # poussées vers le bord droit, elles s'y réduisent en point (rien ne passe x 940 ;
        y = S.val(g, "pos", f - 1)[1]      # opacité inchangée : p3 les reprend en S18 par leur échelle)
        S.key(g, "pos", f, [880, y], MORPH, "in")
        S.key(g, "scale", f, 0, MORPH, "in")

    f = kit.at("S07", "outil", "une barre de titre descend sur le bord haut : le cadre devient une fenêtre de "
                               "logiciel ; la pastille en est le titre")
    S.key("outil", "bar", f, 1, 9, "out")
    kit.move("pastille", f, TITLE_S07, d=9, e="out")

    f = kit.at("S07", "validé", "un grand sceau cyan à bâtiment tombe dans la fenêtre, sous la légende du repère ; la "
                                "fenêtre encaisse")
    S.key("sceau", "pos", f - 1, [SEAL_S07[0], SEAL_S07[1] - 110])
    S.key("sceau", "scale", f, 1)                                # visible sur le mot, déjà sous le repère
    S.key("sceau", "pos", f, list(SEAL_S07), DROP, "out")
    kit.shake("outil", f + DROP, amp=4, axis="y")

    f = kit.at("S07", "par", "une coche ivoire épaisse se trace sur le sceau, qui bat")
    kit.draw("coche_sceau", f, 6)
    kit.pulse("sceau", f, peak=1.15, step=3)

    f = kit.at("S07", "cabinet.", "le sceau coché vole se ranger au bout de la barre de titre et s'y ouvre en pilule "
                                  "« ✓ Cabinet »")
    k_slot = 46 * 1.25 / 96                                      # le disque de 96 px devient le sceau fermé (57 px)
    S.fly("sceau", f, 9, "inOut", to=list(SEAL_SLOT), scale=k_slot, arc=40)
    arr = f + 9
    S.key("sceau", "scale", arr, 0)
    S.key("sceau", "opacity", arr, 0)
    S.key("outil", "sealOn", arr, 1)
    S.key("outil", "seal", arr, 1, 6, "out")

    # ======================= S08 : Aucune donnée client dans une IA grand public non encadrée. ==================
    f = kit.at("S08", "Aucune", "la fenêtre scellée et tout son contenu se rangent à gauche ; le conseiller va en bas "
                                "à droite, hors de la fenêtre")
    s = WIN_S08_SCALE
    kit.move("outil", f, WIN_S08_POS, d=MOVE, scale=s)
    for i, d in enumerate(DOC_IDS):
        kit.move(d, f, win_map(pile_pt(PILE_S06, PILE_SLOT[i]), WIN_S08_POS, s), d=MOVE,
                 scale=round(DOC_PILE_SCALE * s, 4))
    kit.move("ia", f, win_map(IA_S05, WIN_S08_POS, s), d=MOVE, scale=s)
    kit.move("pastille", f, win_map(TITLE_S07, WIN_S08_POS, s), d=MOVE, scale=s)
    toi.walk(f, ADV_S08, d=MOVE)

    f = kit.at("S08", "client", "un curseur sort de la pointe du stylo du conseiller, relié à elle par un fil encre, et "
                                "attrape le « Mail client » sur la pile : la carte se soulève")
    home = S.val("doc3", "pos", f)
    sc = S.val("doc3", "scale", f)
    hw, hh = 100 * sc, 125 * sc
    grab_off = [hw - 14, hh - 14]                    # coin bas droit du « Mail client », dessus de la pile
    grab = [home[0] + grab_off[0], home[1] + grab_off[1]]
    tip = toi.tip(f - 1)
    S.key("curseur", "pos", f - 1, _pt(tip))
    kit.pop("curseur", f, d=6)
    kit.draw("attache", f, 6)
    g = kit.move("curseur", f, _pt(grab), d=12, e="inOut")
    S.key("curseur", "press", g, 1, 3, "out")
    S.key("doc3", "z", g, 14)
    S.key("doc3", "scale", g, round(sc * 1.05, 4), 6, "out")
    S.key("doc3", "sh", g, 4, 6, "out")

    f = kit.at("S08", "IA", "à droite, hors de la fenêtre, une 2e tête IA en verre gris cerné d'encre, tournée vers "
                            "la fenêtre ; sa foule grise ; chaque figurine envoie une carte grise dans sa tête : "
                            "l'IA grand public")
    kit.pop("ia_pub", f, scale=IA_PUB_SCALE, d=10)
    S.key("foule", "show", f + 2, 6, 8, "linear")
    S.key("foule", "link", f + 4, 1, 8, "out")
    pts = S.ents["foule"]["p"]["pts"]
    for k, pt in enumerate(pts):
        cid, g = f"colis{k + 1}", f + 6 + 2 * k
        S.key(cid, "pos", g - 1, list(pt))
        kit.pop(cid, g, d=3)
        S.key(cid, "pos", g + 2, list(c.pub_head), 6, "in")
        S.key(cid, "scale", g + 6, 0, 2, "in")
        S.key(cid, "opacity", g + 8, 0)

    f = kit.at("S08", "grand", "le curseur traîne le mail vers elle, à vitesse constante")
    hit = kit.at("S08", "non", "le mail s'écrase contre le mur droit de la fenêtre : il se tasse, le mur s'épaissit, "
                               "3 traits d'impact restent marqués ; le curseur pousse et tremble")
    w2 = 100 * round(sc * 1.05, 4)
    stop = [WALL_X - 3 - w2, CHOC[1]]                # bord droit du mail contre le mur, sur « non »
    d_drag = hit - f + 1
    cur = S.val("curseur", "pos", f - 1)
    delta = [stop[0] - home[0], stop[1] - home[1]]
    S.key("doc3", "pos", f, _pt(stop), d_drag, "linear")
    S.key("curseur", "pos", f, _pt([cur[0] + delta[0], cur[1] + delta[1]]), d_drag, "linear")
    # écrasement contre le mur : sx 1 -> 0,85 -> 1 en 6 images, le bord droit reste collé au mur
    kit.ensure("doc3", "sx", 1)
    for n, sx in zip(range(hit + 1, hit + 7), (0.92, 0.85, 0.85, 0.9, 0.96, 1.0)):
        S.key("doc3", "sx", n, sx)
        S.key("doc3", "pos", n, _pt([WALL_X - 3 - w2 * sx, CHOC[1]]))
    kit.pop("impact2", hit + 1, d=2)                 # reste marqué jusqu'à la brique RGPD (p2)
    kit.pop("mur_choc", hit + 1, d=2)
    S.key("mur_choc", "scale", hit + 7, 0, 2, "in")
    cur_end = S.val("curseur", "pos", hit)
    for k, dx in enumerate((5, -4, 4, -3, 0)):       # il pousse encore et tremble jusqu'à « encadrée. »
        S.key("curseur", "pos", hit + 1 + k, _pt([cur_end[0] + dx, cur_end[1]]))

    f = kit.at("S08", "encadrée.", "le mail revient tout droit sur la pile ; le curseur rentre dans le stylo du "
                                   "conseiller ; l'IA grand public reste là, entière")
    S.key("curseur", "press", f, 0, 3, "out")
    S.key("doc3", "pos", f, _pt(home), 12, "inOut")
    S.key("doc3", "scale", f, sc, 12, "inOut")
    S.key("doc3", "sh", f, 0, 12, "inOut")
    S.key("doc3", "z", f + 12, 12)
    back = kit.vanish("curseur", f, into=toi.tip(f + 10), d=10)
    S.key("attache", "draw", back, 0)

    _check_entry_p2(S, kit, scene_f0(S, "S09") - 1)
