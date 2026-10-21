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

Scène par scène (tour de revue 3) :
- S01 « 9 » : la pastille bat. « heures ? » : les 4 documents (230 px, titres de 29 px) glissent vers DOC_SPOTS.
- S02 « L’IA » : l'horloge se range en badge ; la tête IA glisse depuis la gauche. « prépare, » : le faisceau gris
  encre de l'IA empile les documents, la pastille se clipse. « tu » : le conseiller arrive par la droite (pop + 5
  images de marche ; bras visible avec le corps), pilule « Toi » à l'arrivée. « décides. » : son stylo touche la pile
  sur le mot ; coche pleine.
- S03 « Le » : coche, pilules et IA sortent. « problème » : ◀◀ de 140 px, tenu jusqu'à la fin du rembobinage ;
  chaque document refait son trajet avec 3 longs traits de vitesse. « avant » : deux papiers gris « Client · 14 h »
  (coin corné, lignes de texte grises) arrivent par la gauche, décalés de 2 images, à deux places libres entre les
  documents. « rendez-vous : » : la barre (700 x 60) se tend, invisible jusqu'au mot.
- S04 : 4 sauts ; il se pose sur le bas droit de la carte fouillée, le titre lisible au-dessus de sa tête, et se
  penche vers elle ; seule la traînée du saut en cours se voit, effacée à l'arrivée. À chaque saut, un bloc de la
  barre vole en arc (taille 1) et s'abat comme un tampon gris sur le coin libre de la carte, puis s'y fond en 6
  images. 4e saut sur un papier gris : il tremble, sa pilule bat, recul. « pas » : le bout cyan bat. « conseil. » :
  le client naît du pictogramme de la pastille et vole se poser sous le bout cyan, contre l'horloge (rig : enter,
  run, scale_to).
- S05 « Première » : repère légendé ; le client rentre dans la pastille (rig) ; documents en 2 x 2 (x 0,88), la
  pastille dans l'allée ; les deux papiers gris vont au bord droit, hors du cadre ; le conseiller va dehors (x 876).
  « tu » : il se penche et sa pointe va au coin bas droit de la future zone, le bras cerné d'un liseré papier (lisible
  sur le buste encre). « limites » : le cadre en tirets part de la pointe. « l’IA » : l'IA entre par l'ouverture,
  pilule à droite de la tête ; le tracé se referme. « lire. » : cône.
- S06 « lit » : lecture. « uniquement » : la tête IA bat ; le rayon gris (épais) part de la tête dès le mot et bute
  sur le bord droit : 3 longs traits d'impact, le bord flashe au cyan vif et se creuse de 14 px, le papier gris visé
  recule (penche et rapetisse). « dossier » : les 4 documents en éventail, chacun dépasse de 64 px (4 pictogrammes),
  « Mail client » devant. « client, » : la pastille se clipse sur le bord haut.
- S07 « dans » : trait plein ; les deux papiers gris filent vers la droite en rapetissant. « outil » : barre de titre.
  « validé » : le sceau s'abat comme un tampon (1,4 -> 1) dans la fenêtre, qui tremble 2 images et dont le contour
  flashe au cyan vif. « par » : coche. « cabinet. » : il se range en « ✓ Cabinet ».
- S08 « Aucune » : la fenêtre se range à gauche ; le conseiller va en bas à droite. « client » : il fait un pas vers
  la fenêtre, bras tendu (liseré) ; le curseur naît de la pointe, relié par un fil encre de 4 px, et attrape le
  « Mail client » ; les 3 autres documents restent épinglés. « IA » : l'IA grand public (x 1) et sa foule. « grand » :
  le curseur traîne le mail ; 4 figurines de la foule versent chacune un papier dans la tête de verre (décalés de 3
  images). « non » : le mail s'écrase de l'intérieur contre le mur, qui bombe de 10 px vers l'extérieur ; 3 traits
  d'impact partent de sa face extérieure vers l'IA grand public. « encadrée. » : curseur repoussé, le mail revient,
  le curseur rentre dans le stylo, le bras retombe.
Tour de revue 4 : S01 la pastille respire dès l'image 0 ; S02 « Toi » sur « tu » ; S03 ◀◀ tenu jusqu'à « avant »,
l'aiguille des minutes recule (9 h -> 8 h 50) ; les papiers gris en une pile décalée, personne grise sur leur pilule ;
S04 il se pose À CÔTÉ de chaque carte, sa pointe en touche le bord ; le bloc entre DANS la carte (rien n'y reste
posé) ; l'aiguille avance d'un cran par saut ; le client (153 px) reste sous le bout cyan ; S05 il fait lui-même le
tour de la zone en courant, le cadre se trace sous sa pointe, puis l'IA paraît dans le cadre fermé (storyboard) ;
S06 le rayon passe sous les documents et vise le papier gris du bas, qui tremble ; S07 le sceau (bâtiment + mini-
figurine du conseiller) tombe comme un tampon, la fenêtre tremble en xy ; la mini-figurine reste dans « ✓ Cabinet » ;
S08 liens de la foule tirés l'un après l'autre vers la tête ; au choc, les contours des deux briques à venir.
Raccord : à l'image 609, tout est exactement dans ENTRY_P2 (vérifié en fin de partie).
"""
import math

from pipeline.story import DROP, FADE, MORPH, MOVE, POP, text_width
from pipeline.story_kit import frames, lerp

from . import (ADV_OUT, ADV_RECOIL, ADV_S02, ADV_S03, ADV_S08, ADV_S08_PUSH, BAR_W, BAR_X0, BLOCK, CHOC, CLIENT_S04,
               CLIENT_S04_SCALE, CLOCK_BADGE, CLOCK_BADGE_SCALE, CLOCK_S01, CX, DOC_GRID_S05, DOC_GRID_SCALE,
               DOC_PILE_SCALE, DOC_SPOTS, DOC_TILTS, DOC_W, ENTRY_P2, FRAME_C, FRAME_H, FRAME_TOP, FRAME_W, FRAME_X1,
               FRAME_Y1, GREY, GREY_EDGE_S05, GREY_EDGE_SCALE, GREY_ICON_X, GREY_PILL, GREY_SPOTS, GREY_TILTS, GREY_Z,
               IA_PILL_RIGHT, IA_PUB_SCALE, IA_S02, IA_S02_SCALE, IA_S05, INK_25, INK_40, MARKER_Y, PASTILLE_S01,
               PILE_S01, PILE_S02, PILE_S06, PILE_SLOT, PILE_TICK_S02, PILL_ICON, S04_HOPS, S04_TOUCH, SEAL_MINI_K,
               SEAL_S07, SEAL_SLOT, TITLE_H, TITLE_S07, WALL_X, WIN_S08_POS, WIN_S08_SCALE, fan_pt, pile_pt, pile_z,
               scene_f0, seal_mini_at, vanish, win_map)

DOC_IDS = ["doc1", "doc2", "doc3", "doc4"]
GREY_IDS = ["carte_grise1", "carte_grise2"]
HOP_CARDS = ["doc2", "doc1", "doc3", "carte_grise2"]      # cartes fouillées en S04, dans l'ordre des sauts
BLOCK_LAND = (-52, 66)                                    # le bloc s'abat sur le coin bas gauche de la carte (repère de
BLOCK_LAND_SCALE = 0.8                                    # la carte), à côté du conseiller, jamais sous lui
PASTILLE_S02 = (PILE_S02[0], PILE_S02[1] - 120)          # même place relative qu'en S01 : coiffe la pile
PASTILLE_S05 = (round((DOC_GRID_S05[0][0] + DOC_GRID_S05[1][0]) / 2),   # dans l'allée entre les 2 rangées
                round((DOC_GRID_S05[0][1] + DOC_GRID_S05[2][1]) / 2))
PASTILLE_S06 = (TITLE_S07[0], FRAME_TOP + 14)            # sur le bord haut du cadre, sous la légende du repère
FRAME_R = 14                                             # rayon des coins du cadre (entité case)
GREY_TEXT = "Client · 14 h"
GREY_PILL_SCALE = 0.75                                   # échelle (relative) des pilules grises laissée à p3 (S18)
GREY_TAG, GREY_TAG_K = "14 h", 0.95                      # S05-S07 : pilule courte, 32 px à l'écran (tour 4)
GREY_TAG_W = round(text_width(GREY_TAG, GREY_PILL["size"], 700) + 92)
CLIENT_VIA = (760, 820)                                  # le client passe entre la pile grise et « Relevé PEA » (S04)
BLOCK_INTO = (10, 20)                                    # S04 : le bloc entre dans la bande du milieu de la carte
# S05 « tu » / « limites » (tour 4) : décalage corps - pointe du stylo pendant le tour du cadre (dehors, sauf le long
# du bas, où il court à l'intérieur, pieds sur le trait) ; fondus de 70 px de part et d'autre de chaque coin
RUN_OFF = dict(bottom=(62, -106), left=(-100, 14), top=(-40, -110), right=(108, -12))
TOI_ENTER_X = 870                                        # S02 : il arrive par la droite (bord droit < 940)


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




def _frame_path(step=2.0):
    """Polyligne monde dense du contour du cadre (case w=FRAME_W, h=FRAME_H, coins de FRAME_R, centre FRAME_C, tourné
    de 180°), dans le sens de son tracé : coin bas droit -> bas -> côté gauche -> haut -> côté droit -> coin bas droit
    (même chemin que roundRect de draw.tsx). Renvoie (points, longueurs cumulées)."""
    w, h, r = FRAME_W, FRAME_H, FRAME_R
    x, y = -w / 2, -h / 2
    loc = []

    def line(a, b):
        n = max(1, math.ceil(math.dist(a, b) / step))
        loc.extend([a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n] for k in range(n))

    def arc(c, a0, a1):
        n = max(2, math.ceil(abs(a1 - a0) * r / step))
        loc.extend([c[0] + r * math.cos(a0 + (a1 - a0) * k / n), c[1] + r * math.sin(a0 + (a1 - a0) * k / n)]
                   for k in range(n))

    line([x + r, y], [x + w - r, y])
    arc([x + w - r, y + r], -math.pi / 2, 0)
    line([x + w, y + r], [x + w, y + h - r])
    arc([x + w - r, y + h - r], 0, math.pi / 2)
    line([x + w - r, y + h], [x + r, y + h])
    arc([x + r, y + h - r], math.pi / 2, math.pi)
    line([x, y + h - r], [x, y + r])
    arc([x + r, y + r], math.pi, 1.5 * math.pi)
    loc.append([x + r, y])
    pts = [[FRAME_C[0] - p[0], FRAME_C[1] - p[1]] for p in loc]          # rotation de 180°
    acc = [0.0]
    for a, b in zip(pts, pts[1:]):
        acc.append(acc[-1] + math.dist(a, b))
    return pts, acc


def _at_len(pts, acc, s):
    """Point de la polyligne à la longueur s."""
    s = max(0.0, min(acc[-1], s))
    lo, hi = 0, len(acc) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if acc[mid] <= s:
            lo = mid
        else:
            hi = mid
    t = (s - acc[lo]) / max(1e-9, acc[hi] - acc[lo])
    return [pts[lo][0] + (pts[hi][0] - pts[lo][0]) * t, pts[lo][1] + (pts[hi][1] - pts[lo][1]) * t]


def _ctrl_lerp(ctrl, s):
    """Interpolation linéaire d'un décalage [dx, dy] entre des points de contrôle (s, [dx, dy])."""
    for (s0, a), (s1, b) in zip(ctrl, ctrl[1:]):
        if s <= s1:
            t = (s - s0) / max(1e-9, s1 - s0)
            return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t]
    return list(ctrl[-1][1])


def part(S, kit, c):
    toi, client = c.toi, c.client
    S.ents["rayon"]["p"].update(sw=12, dash=[0.01, 22])   # S06 : le rayon, épais (revue 3)

    # État d'entrée = distribution (etat_initial de S01) : l'épingle ne fait que le redire.
    kit.pin(-1, {"horloge": {"pos": list(CLOCK_S01), "scale": 1}, "pastille": {"pos": list(PASTILLE_S01), "scale": 1},
                 **{d: {"pos": pile_pt(PILE_S01, i), "rot": 0, "scale": 1} for i, d in enumerate(DOC_IDS)}})

    # ======================= S01 : Client à 9 heures ? =======================
    kit.hold("S01", "Client", "tenue : l'horloge de 9 h et la pile coiffée de « Client · 9 h » sont là dès l'image 0 ; "
                              "seule la pastille respire (1 -> 1,03)")
    S.key("pastille", "scale", 0, 1.03, 15, "inOut")       # tour 4 : l'accroche n'est pas figée (respiration lente)
    f = kit.at("S01", "9", "la pastille « Client · 9 h » bat une fois (×1,12)")
    S.key("pastille", "scale", f, 1.12, 4, "out")
    S.key("pastille", "scale", f + 4, 1, 5, "inOut")
    f = kit.at("S01", "heures ?", "la pile s'étale : les 4 documents glissent à 4 places séparées (haut gauche, droite, "
                                  "bas gauche, bas) ; la pastille reste seule au centre")
    for i, d in enumerate(DOC_IDS):
        g = f + i                                        # 8 images, décalés d'une : posés à l'image 32
        S.keys(d, g, 8, "out", pos=_pt(DOC_SPOTS[i]), rot=DOC_TILTS[i])
        S.key(d, "sh", g, 6, 8, "out")

    # ======================= S02 : L'IA prépare, tu décides. =======================
    f = kit.at("S02", "L’IA", "l'horloge se range en badge en haut à droite ; la tête IA, déjà à moitié dans l'image, "
                              "glisse depuis la gauche entre « Avis d’impôt » et « Mail client », pilule « IA » dessous")
    kit.move("horloge", f, CLOCK_BADGE, d=10, e="inOut", scale=CLOCK_BADGE_SCALE)
    S.key("ia", "z", f - 1, 12.6)                    # S02 : l'IA passe devant les cartes encore étalées
    S.key("ia_pill", "z", f - 1, 12.7)
    S.key("ia", "pos", f - 1, [-60, IA_S02[1]])
    S.key("ia", "scale", f, IA_S02_SCALE)            # visible sur le mot, à moitié dans l'image
    kit.move("ia", f, IA_S02, d=MORPH, e="out")

    f = kit.at("S02", "prépare,", "le faisceau pointillé gris de l'IA tire les documents un par un : ils se redressent "
                                  "et s'empilent au centre ; la pastille se clipse sur la pile")
    S.key("faisceau_range", "pb", f - 1, list(PILE_S02))
    kit.draw("faisceau_range", f, 6)
    order = sorted(range(4), key=lambda i: math.dist(DOC_SPOTS[i], IA_S02))   # du plus proche de l'IA au plus loin
    for k, i in enumerate(order):
        d, g = DOC_IDS[i], f + 4 * k
        S.keys(d, g, MORPH, "inOut", pos=pile_pt(PILE_S02, i), rot=0)
        S.key(d, "sh", g, 6 if i == 3 else 0, MORPH, "out")
    kit.move("pastille", f + 8, PASTILLE_S02, d=9, e="out")
    S.key("faisceau_range", "draw", f + 14, 0, 6, "inOut")      # le faisceau rentre dans la tête

    f_tu = kit.at("S02", "tu", "le conseiller « Toi » (figurine encre, stylo en main) arrive par la droite en bas, bras "
                               "et stylo avec lui ; sa pilule « Toi » surgit sous ses pieds pendant la marche")
    toi.enter(f_tu, at=[TOI_ENTER_X, ADV_S02[1]], d=1, arm_from=0)   # entier dès le mot, bras compris (rig)
    toi.walk(f_tu, ADV_S02, d=5)                     # il arrive en marchant (5 images), avant le geste de « décides. »
    S.key("toi_pill", "pos", f_tu - 1, [0, 125])
    kit.pop("toi_pill", f_tu + 1, d=POP)             # tour 4 : sur « tu », pas sur « décides. »

    f = kit.at("S02", "décides.", "le stylo touche le coin de la pile sur le mot : au contact, une coche pleine cyan "
                                  "profond se trace")
    hit = toi.tap(f - 4, list(PILE_TICK_S02), d=5)   # contact sur l'image du mot
    kit.draw("coche_pile", hit, 6)
    toi.rest(hit + 6, d=8)

    # ======================= S03 : Le vrai problème avant un rendez-vous : =======================
    f = kit.at("S03", "Le", "la coche se réduit en point, les pilules « IA » et « Toi » s'effacent ; l'IA rétrécit et "
                            "sort par la gauche ; le conseiller recule d'un pas")
    vanish(kit, "coche_pile", f, d=6)
    kit.fade("ia_pill", f, 0)
    kit.fade("toi_pill", f, 0)
    S.key("toi_pill", "scale", f + FADE, 0)
    kit.vanish("ia", f, into=[-90, IA_S02[1]], d=9)
    toi.walk(f, list(ADV_S03), d=8)
    S.key("ia", "z", f + 10, 4)
    S.key("ia_pill", "z", f + 10, 4.1)

    f = kit.at("S03", "problème", "un grand ◀◀ (140 px) au-dessus de la pile : les documents refont leur trajet à "
                                  "l'envers, avec 3 longs traits de vitesse, jusqu'à leurs 4 places ; la pastille revient ; "
                                  "l'aiguille des minutes de l'horloge tourne à rebours (9 h -> 8 h 50)")
    kit.pop("rembobine", f, scale=1, d=6)
    for i, d in enumerate(DOC_IDS):
        S.keys(d, f, MORPH, "inOut", pos=_pt(DOC_SPOTS[i]), rot=DOC_TILTS[i])
        S.key(d, "sh", f, 6, MORPH, "out")
        for j in range(3):
            v = f"vitesse{i + 1}_{j + 1}"
            S.key(v, "scale", f, 1, 2, "out")
            S.key(v, "scale", f + 9, 0, 3, "out")
    kit.move("pastille", f, PASTILLE_S01, d=MORPH)
    S.key("aiguille", "rot", f - 1, 0)               # tour 4 : l'aiguille des minutes paraît sur 9 h et recule
    S.key("aiguille", "scale", f, 1)
    S.key("aiguille", "rot", f, -60, MORPH, "inOut")

    f = kit.at("S03", "avant", "le ◀◀ s'efface ; deux papiers gris « Client · 14 h » (personne grise, coin corné) "
                               "arrivent par la gauche et se posent en une petite pile décalée, au milieu des documents")
    vanish(kit, "rembobine", f, d=5)                 # tenu jusqu'à « avant » (0,43 s)
    for k, g in enumerate(reversed(GREY_IDS)):       # celle de dessous d'abord
        i = GREY_IDS.index(g)
        gk = f + 2 * k
        S.key(g, "pos", gk - 1, [-150, GREY_SPOTS[i][1]])
        S.key(g, "scale", gk, 1)
        kit.move(g, gk, GREY_SPOTS[i], d=MOVE, e="inOut")

    f = kit.at("S03", "rendez-vous :", "une barre pleine de cyan (700 x 60) se tend du badge horloge vers la gauche "
                                       "(réserve de temps jusqu'à 9 h)")
    right = BAR_X0 + BAR_W
    S.key("barre", "pos", f - 1, [right, MARKER_Y])
    S.key("barre", "w", f - 1, 0)
    S.key("barre", "scale", f - 1, 0)                # invisible jusqu'au mot : aucun point cyan avant (revue 3)
    S.key("barre", "scale", f, 1)
    S.key("barre", "w", f, BAR_W, 9, "out")
    S.key("barre", "pos", f, [BAR_X0 + BAR_W / 2, MARKER_Y], 9, "out")
    S.key("minutes_barre", "scale", f + 5, 1)                # contrôle sans son : l'unité de la barre, « 45 min »
    kit.fade("minutes_barre", f + 5, 1, d=FADE, frm=0)

    # ======================= S04 : ton temps part dans la recherche, pas dans le conseil. =======================
    words = ["temps", "part", "dans", "recherche,"]
    whats = ["1er saut, sous « Relevé PEA » (à côté, jamais dessus) : sa pointe touche le bas de la carte, qui pivote ; "
             "un bloc cyan de la barre vole en arc, grisé, et disparaît DANS la carte ; l'aiguille avance d'un cran",
             "2e saut, sous « Avis d’impôt » ; 2e bloc ; un cran", "3e saut, à droite de « Mail client » ; 3e bloc ; "
             "un cran", "4e saut, à droite de la pile grise « Client · 14 h » : 4e bloc ; la pile tremble, sa pilule "
             "bat ; il recule penché en arrière, à l'écart des cartes : mauvais dossier ; l'aiguille est sur 9 h"]
    beats = [kit.at("S04", w, t) for w, t in zip(words, whats)]
    for k, f in enumerate(beats):
        d = 5
        card, local = S04_TOUCH[k]
        p0 = S.val("toi", "pos", f - 1)
        dist = math.dist(p0, S04_HOPS[k])
        toi.hop(f, S04_HOPS[k], d, h=min(70, 18 + 0.1 * dist))
        kit.draw(f"traine{k + 1}", f, d, e="inOut")                # seule la traînée du saut en cours
        kit.fade(f"traine{k + 1}", f + d, 0, d=4)                 # effacée à l'arrivée
        touch = S.to_world(card, list(local), f + d)
        toi.reach(f + d, _pt(touch), d=2, step=False)            # sa pointe touche le bord de la carte
        tilt = S.val(card, "rot", f)
        if card.startswith("doc"):                                 # la carte fouillée pivote sous la pointe
            kit.pulse(card, f + d + 1, peak=round(tilt + (5 if tilt < 0 else -5), 2), step=2, track="rot")
        # la jauge perd 22 % à gauche ; l'aiguille avance d'un cran ; le bloc vole en arc, grisé, et entre DANS la
        # carte (bande du milieu, jamais sur la date) : rien ne reste posé dessus (tour 4)
        b = f"bloc{k + 1}"
        S.key("barre", "value", f, round(1 - BLOCK * (k + 1), 4))
        S.key("minutes_barre", "value", f, 45 - 10 * (k + 1), 5, "out")   # 45 -> 35 -> 25 -> 15 -> 5 min
        S.key("aiguille", "rot", f, -60 + 15 * (k + 1), 3, "out")
        S.key(b, "scale", f, 1)
        S.set(b, z=5.6)
        S.key(b, "z", f + 1, 12.6)                               # au-dessus des cartes
        into = "carte_grise1" if card.startswith("carte") else card
        fl = 6 if k == 3 else 7
        arr = f + 1 + fl
        land = S.to_world(into, list(BLOCK_INTO), arr)
        S.key(b, "pos", f + 1, _pt(land), fl, "inOut", arc=90)
        S.key(b, "rot", f + 1, S.val(into, "rot", f), fl, "out")
        # contrôle sans son : le bloc reste cyan pendant son vol (un morceau de la barre de temps, pas un rectangle
        # gris non identifié) et entre tel quel dans la carte
        S.key(b, "scale", f + 1, 0.5, fl, "in")
        vanish(kit, b, arr, d=3)
        if 0 < k < 3:                                              # (« Relevé PEA », contre le bord droit, ne
            kit.pulse(card, arr, peak=1.05, step=3)                # grossit pas : colonne réservée x > 940)
    land4 = arr                                                   # le 4e bloc est dans la pile grise
    kit.shake("carte_grise1", land4, amp=6, axis="x")             # la pile de l'autre client tremble
    kit.shake("carte_grise2", land4, amp=6, axis="x")
    kit.pulse("carte_grise1_pill", land4, peak=1.2, step=3)
    kit.pulse("pastille", land4, peak=1.12, step=3)               # les deux pilules battent ensemble : pas le même
    #                                                               client (contrôle sans son)
    toi.hop(land4 + 1, ADV_RECOIL, 7, h=0, lean=-9)               # recul penché en arrière, à l'écart des cartes

    f = kit.at("S04", "pas", "le conseiller reste arrêté ; le bout cyan restant (12 %) contre l'horloge bat une fois, "
                             "avec « 5 min » au-dessus")
    S.key("bout", "scale", f, 1)                                 # posé exactement sur ce qui reste de la jauge
    S.key("bout", "scale", f + 1, 1.15, 4, "out")
    S.key("bout", "scale", f + 5, 1, 5, "inOut")
    kit.pulse("minutes_barre", f + 1, peak=1.15, step=4)        # il ne reste que 5 min pour le client
    f = kit.at("S04", "conseil.", "la pastille bat et le client de 9 h naît de son pictogramme, puis vole se poser, "
                                  "grand (153 px), sous le bout cyan, à gauche du badge ; il y reste")
    kit.pulse("pastille", f, peak=1.12, step=3)
    icon0 = S.to_world("pastille", PILL_ICON, f - 1)
    client.size = 0.15
    client.enter(f, at=_pt(icon0), d=2)                          # né du pictogramme (rig de la figurine)
    route = [_pt(_quad(icon0, CLIENT_VIA, CLIENT_S04, q / 12)) for q in range(13)]
    client.run(f + 2, route, 8)
    client.scale_to(f + 2, CLIENT_S04_SCALE, d=8, e="inOut")

    # ======================= S05 : Première étape : tu limites ce que l'IA peut lire. =======================
    f = kit.at("S05", "Première", "la barre, le bout cyan et l'horloge se contractent en 3 cercles légendés « Limiter, "
                                  "Exiger, Relire », le 1 allumé ; le client rentre dans le pictogramme de la pastille ; "
                                  "les documents se regroupent en 2 x 2, la pastille entre les deux rangées ; les deux "
                                  "papiers gris se séparent et vont au bord droit ; le conseiller va dehors, en bas à droite")
    xs = S.ents["marqueur"]["p"]["xs"]
    discs = [[CX + x, MARKER_Y] for x in xs]
    for id, disc in zip(["bout", "barre", "horloge"], discs):
        vanish(kit, id, f, into=disc, d=MORPH)
    vanish(kit, "minutes_barre", f, into=discs[2], d=MORPH)      # l'unité part avec la barre
    kit.pop("marqueur", f, d=MORPH)
    for i, d in enumerate(DOC_IDS):
        S.keys(d, f, MOVE, "inOut", pos=_pt(DOC_GRID_S05[i]), scale=DOC_GRID_SCALE, rot=0)
    kit.move("pastille", f, PASTILLE_S05, d=MOVE)
    # les deux papiers gris restent, au bord droit, hors du cadre ; pilules raccourcies (« 14 h »), à 32 px
    tag_x = round(-GREY_TAG_W / 2 + GREY_ICON_X, 1)
    for k, g in enumerate(GREY_IDS):
        kit.move(g, f, GREY_EDGE_S05[k], d=MOVE, scale=GREY_EDGE_SCALE)
        S.key(g, "rot", f, 0, MOVE, "inOut")
        S.key(g, "z", f, GREY_Z[k])
        kit.ensure(f"{g}_pill", "text", GREY_TEXT)
        kit.ensure(f"{g}_pill", "w", GREY_PILL["w"])
        S.key(f"{g}_pill", "text", f, GREY_TAG)
        S.key(f"{g}_pill", "w", f, GREY_TAG_W, MOVE, "inOut")
        S.key(f"{g}_qui", "pos", f, [tag_x, 0], MOVE, "inOut")   # la personne suit le bord gauche de la pilule
        S.key(f"{g}_pill", "scale", f, round(GREY_TAG_K / GREY_EDGE_SCALE, 4), MOVE, "inOut")
    kit.fade("carte_grise2_pill", f, 1, d=FADE)                   # la carte du dessous a aussi son visage
    # le client rentre dans le pictogramme de la pastille, qui se déplace (rig : run vers sa place à l'arrivée)
    dc = 12
    tgt = S.to_world("pastille", PILL_ICON, f + dc - 1)
    client.run(f, [S.val("client", "pos", f - 1), _pt(tgt)], dc)
    client.scale_to(f, 0.05, d=dc, e="inOut")
    client.exit(f + dc, d=1)
    toi.walk(f, ADV_OUT, d=MOVE)                     # il laisse la place au dossier regroupé, dehors en bas à droite

    # S05 « tu » / « limites » (tour 4) : il fait lui-même le tour de la zone en courant à vitesse constante ; la
    # pointe de son stylo trace le cadre en tirets image par image (la tête du trait reste sous la pointe), de son coin
    # bas droit vers la gauche, puis le côté gauche, le haut et le côté droit ; il finit dehors, à sa place de départ
    f_tu = kit.at("S05", "tu", "il se met à courir : la pointe de son stylo se pose sur le coin bas droit de la future "
                               "zone et le trait en tirets cyan profond naît sous elle")
    f_lim = kit.at("S05", "limites", "il fait le tour de la zone à vitesse constante (dehors à gauche, en haut et à "
                                     "droite, pieds sur le trait en bas) : le cadre se trace sous la pointe de son stylo "
                                     "et se ferme derrière lui ; il finit dehors, en bas à droite")
    f_ia = kit.at("S05", "l’IA", "la tête IA apparaît dans le coin libre, à l'intérieur du cadre fermé (pop 300 ms), "
                                 "sa pilule à droite de la tête ; le conseiller relève son stylo, dehors")
    pts, acc = _frame_path()
    L = acc[-1]
    c1, c2, c3 = 582 + 11, 593 + 22 + 752, 1367 + 22 + 582
    tip0 = pts[0]
    home = [ADV_OUT[0] - tip0[0], ADV_OUT[1] - tip0[1]]
    ctrl = [(0, home), (110, RUN_OFF["bottom"]), (c1 - 70, RUN_OFF["bottom"]), (c1 + 70, RUN_OFF["left"]),
            (c2 - 70, RUN_OFF["left"]), (c2 + 70, RUN_OFF["top"]), (c3 - 70, RUN_OFF["top"]),
            (c3 + 70, RUN_OFF["right"]), (L - 140, RUN_OFF["right"]), (L, home)]
    run_end = f_ia - 1                                            # fermé sur l'image qui précède « l'IA »
    N = run_end - f_tu + 1
    toi.rim(f_tu, True, d=2)                                      # bras cerné de papier quand il croise le buste
    for n in range(f_tu, run_end + 1):
        q = (n - f_tu + 1) / N
        s = q * L
        tip = _at_len(pts, acc, s)
        off = _ctrl_lerp(ctrl, s)
        toi.walk(n, _pt([tip[0] + off[0], tip[1] + off[1]]), d=1)
        toi.reach(n, _pt(tip), d=1, step=False)
        S.key("cadre", "draw", n, round(q, 5), 1, "linear")
    if f_lim <= f_tu or f_lim > run_end:
        kit.warn(f"p1 S05 : « limites » ({f_lim}) hors du tour ({f_tu}-{run_end})")
    toi.rim(run_end - 1, False, d=2)                              # avant que le bras ne se replie contre le buste
    toi.rest(f_ia, 8)

    f = f_ia
    S.key("ia", "pos", f - 1, list(IA_S05))
    S.key("ia", "z", f - 1, 4)
    S.key("ia_pill", "pos", f - 1, list(IA_PILL_RIGHT))
    S.key("ia_pill", "opacity", f - 1, 1)
    kit.pop("ia", f, scale=1, d=POP)

    f = kit.at("S05", "lire.", "son faisceau s'ouvre en cône sur les 4 documents, coupé net par le cadre")
    kit.pop("cone", f, d=POP)

    # ======================= S06 : Elle lit uniquement le dossier client, =======================
    f = kit.at("S06", "lit", "lecture : le cône s'éclaire ; chaque document bat légèrement pendant que ses traits gris "
                             "passent au cyan, l'un après l'autre")
    S.key("cone", "fillOp", f, 1.0, 3, "out")
    S.key("cone", "fillOp", f + 3, 0.7, 8, "inOut")
    for i, d in enumerate(DOC_IDS):
        S.key(d, "read", f + 3 * i, 1, 12, "out")
        kit.pulse(d, f + 3 * i, peak=round(DOC_GRID_SCALE * 1.05, 4), step=2)

    f = kit.at("S06", "uniquement", "la tête IA bat ; un rayon épais part de sa tête dès le mot, passe sous les documents "
                                    "et vise le papier gris du bas, au bord droit (sa personne grise) : il bute sur le "
                                    "bord du cadre, 3 longs traits d'impact, le bord flashe et se creuse ; le papier visé "
                                    "et sa personne tremblent ; le rayon se retire")
    kit.pulse("ia", f, peak=1.06, step=2)
    apex = S.to_world("ia", c.brain_front, f)
    corner = [DOC_GRID_S05[3][0] + DOC_W / 2 * DOC_GRID_SCALE + 6, DOC_GRID_S05[3][1] + 125 * DOC_GRID_SCALE + 12]
    hx = FRAME_X1 - 4
    hy = apex[1] + (corner[1] - apex[1]) * (hx - apex[0]) / (corner[0] - apex[0])   # juste sous la grille
    S.key("rayon", "pb", f - 1, _pt([hx, hy]))
    kit.draw("rayon", f, 5, e="out")                  # un bout de rayon visible dès le mot
    hit = f + 4
    S.key("impact1", "pos", f - 1, _pt([FRAME_X1 + 2, hy]))
    S.key("bosse", "pos", f - 1, _pt([FRAME_X1, hy]))
    kit.pop("impact1", hit, d=2)
    kit.pop("bosse", hit, d=2)
    kit.shake("bosse", hit + 2, amp=8, axis="x")
    S.key("cadre_flash", "opacity", hit, 1)
    S.key("cadre_flash", "opacity", hit + 2, 0, 8, "in")
    kit.shake("carte_grise2", hit + 1, amp=6, axis="x")          # le papier visé et sa personne tremblent
    kit.pulse("carte_grise2_qui", hit + 1, peak=1.3, step=3)
    S.key("rayon", "draw", hit + 10, 0, 6, "inOut")             # tenu contre le mur, puis retiré
    vanish(kit, "bosse", hit + 6, d=6)
    vanish(kit, "impact1", hit + 13, d=6)

    f = kit.at("S06", "dossier", "les 4 documents se rangent en éventail : chacun dépasse de 64 px (son pictogramme et "
                                 "son bord), le « Mail client » devant ; le cône se replie")
    for i, d in enumerate(DOC_IDS):
        slot = PILE_SLOT[i]
        S.keys(d, f, MORPH, "inOut", pos=fan_pt(PILE_S06, slot), scale=DOC_PILE_SCALE)
        S.key(d, "sh", f, 6 if slot == 0 else 3, MORPH, "out")
        S.key(d, "z", f, pile_z(slot))
    vanish(kit, "cone", f, d=MORPH)

    f = kit.at("S06", "client,", "la pastille « Client · 9 h » se clipse sur le bord haut du cadre, au-dessus de "
                                 "l'éventail")
    kit.move("pastille", f, PASTILLE_S06, d=9, e="out")
    S.key("pastille", "scale", f + 9, 1.08, 3, "out")
    S.key("pastille", "scale", f + 12, 1, 4, "inOut")

    # ======================= S07 : dans un outil validé par ton cabinet. =======================
    f = kit.at("S07", "dans", "les tirets du cadre deviennent un trait plein ; les deux papiers gris filent vers la "
                              "droite en rapetissant ; le conseiller reste dehors, en bas à droite")
    S.key("outil", "scale", f - 1, 1)
    S.key("outil", "opacity", f - 1, 0)
    kit.fade("outil", f, 1, d=8)
    kit.fade("cadre", f, 0, d=8)
    S.key("cadre", "scale", f + 8, 0)
    for k, g in enumerate(GREY_IDS):                 # poussés dehors, ils s'y réduisent (rien ne passe x 940)
        gk = f + 2 * k
        y = S.val(g, "pos", gk - 1)[1]
        S.key(g, "pos", gk, [880, y], MOVE, "inOut")
        S.key(g, "scale", gk, 0, MOVE, "inOut")
        # cachés : leurs pilules reprennent le texte, l'échelle et la place de la personne que p3 attend (S18)
        S.keys(f"{g}_pill", gk + MOVE, text=GREY_TEXT, w=GREY_PILL["w"], scale=GREY_PILL_SCALE)
        S.key(f"{g}_qui", "pos", gk + MOVE, [round(-GREY_PILL["w"] / 2 + GREY_ICON_X, 1), 0])

    f = kit.at("S07", "outil", "une barre de titre descend sur le bord haut : le cadre devient une fenêtre de "
                               "logiciel ; la pastille en est le titre")
    S.key("outil", "bar", f, 1, 9, "out")
    kit.move("pastille", f, TITLE_S07, d=9, e="out")

    f = kit.at("S07", "validé", "le sceau du cabinet (bâtiment à colonnes, la mini-figurine encre du conseiller sous son "
                                "fronton) tombe et s'abat comme un tampon dans la fenêtre ; la fenêtre tremble et son "
                                "contour flashe au cyan vif")
    x, y = SEAL_S07
    S.key("sceau", "pos", f - 1, [x, y - 170])
    S.key("sceau", "scale", f - 1, 0)
    S.key("sceau", "scale", f, 1.25)
    S.key("sceau", "pos", f, [x, y], 6, "in")                    # il tombe (ease-in : il frappe)
    S.key("sceau", "scale", f + 1, 1, 5, "out")
    hit = f + 6                                                  # contact : il s'abat
    kit.shake("outil", hit, amp=4, axis="xy")
    S.key("cadre_flash", "opacity", hit, 1)
    S.key("cadre_flash", "opacity", hit + 2, 0, 8, "in")

    f = kit.at("S07", "par", "une coche ivoire épaisse se trace sur le sceau, qui bat")
    kit.draw("coche_sceau", f, 6)
    kit.pulse("sceau", f, peak=1.15, step=3)

    f = kit.at("S07", "cabinet.", "le sceau coché vole se ranger au bout de la barre de titre et s'y ouvre en pilule "
                                  "« ✓ Cabinet » ; la mini-figurine reste devant son bâtiment")
    k_slot = 46 * 1.25 / 96                                      # le disque de 96 px devient le sceau fermé (57 px)
    S.fly("sceau", f, 9, "inOut", to=list(SEAL_SLOT), scale=k_slot, arc=40)
    arr = f + 9
    S.key("sceau", "scale", arr, 0)
    S.key("sceau", "opacity", arr, 0)
    S.key("outil", "sealOn", arr, 1)
    S.key("outil", "seal", arr, 1, 6, "out")
    S.key("sceau_mini", "pos", arr - 1, seal_mini_at(FRAME_W, FRAME_H, 0))
    S.key("sceau_mini", "scale", arr, SEAL_MINI_K)
    S.key("sceau_mini", "pos", arr, seal_mini_at(FRAME_W, FRAME_H, 1), 6, "out")   # suit l'ouverture du sceau

    # ======================= S08 : Aucune donnée client dans une IA grand public non encadrée. ==================
    f = kit.at("S08", "Aucune", "la fenêtre scellée et tout son contenu se rangent à gauche ; le conseiller va en bas "
                                "à droite, hors de la fenêtre")
    s = WIN_S08_SCALE
    kit.move("outil", f, WIN_S08_POS, d=MOVE, scale=s)
    for i, d in enumerate(DOC_IDS):
        kit.move(d, f, win_map(fan_pt(PILE_S06, PILE_SLOT[i]), WIN_S08_POS, s), d=MOVE,
                 scale=round(DOC_PILE_SCALE * s, 4))
    kit.move("ia", f, win_map(IA_S05, WIN_S08_POS, s), d=MOVE, scale=s)
    S.key("ia_pill", "scale", f, round(1 / s, 4), MOVE, "inOut")   # « IA » garde ses 32 px
    kit.move("pastille", f, win_map(TITLE_S07, WIN_S08_POS, s), d=MOVE, scale=s)
    toi.walk(f, ADV_S08, d=MOVE)

    f = kit.at("S08", "client", "le conseiller fait un pas vers la fenêtre, bras tendu ; un curseur naît de la pointe de "
                                "son stylo, relié à elle par un fil encre, et attrape le « Mail client » : la carte se "
                                "soulève ; les autres documents ne bougent pas")
    pinned = [d for d in DOC_IDS if d != "doc3"]                 # seul le « Mail client » bougera
    f_enc = S.word_after("encadrée", f)                          # jusqu'au retour du mail (« encadrée. »)
    for d in pinned:
        for n in (f - 1, f_enc):
            S.key(d, "pos", n, _pt(S.val(d, "pos", f - 1)))
            S.key(d, "scale", n, S.val(d, "scale", f - 1))
    home = S.val("doc3", "pos", f)
    sc = S.val("doc3", "scale", f)
    hw, hh = DOC_W / 2 * sc, 125 * sc
    grab_off = [hw - 16, hh - 16]                    # coin bas droit du « Mail client », devant l'éventail
    grab = [home[0] + grab_off[0], home[1] + grab_off[1]]
    toi.rim(f, True)
    toi.walk(f, ADV_S08_PUSH, d=6)
    aim = [ADV_S08_PUSH[0] - 150, ADV_S08_PUSH[1] - 95]          # bras tendu vers la fenêtre, à hauteur d'épaule
    toi.reach(f, aim, d=6, step=False)
    born = f + 6
    tip = toi.tip(born - 1)
    S.key("curseur", "pos", born - 1, _pt(tip))
    kit.pop("curseur", born, d=5)
    kit.draw("attache", born, 5)
    g = kit.move("curseur", born, _pt(grab), d=10, e="inOut")
    S.key("curseur", "press", g, 1, 3, "out")
    S.key("doc3", "z", g, 14)
    S.key("doc3", "scale", g, round(sc * 1.05, 4), 6, "out")
    S.key("doc3", "sh", g, 4, 6, "out")

    f = kit.at("S08", "IA", "à droite, hors de la fenêtre, une 2e tête IA en verre gris cerné d'encre, tournée vers "
                            "la fenêtre, et sa foule grise (56 px) ; un lien gris part de chaque figurine et bat vers la "
                            "tête, l'un après l'autre : tout le monde la nourrit (l'IA grand public)")
    kit.pop("ia_pub", f, scale=IA_PUB_SCALE, d=10)
    S.key("foule", "show", f + 1, 6, 6, "linear")
    kit.stagger([f"lien{k + 1}" for k in range(6)], f + 2, 2, kit.draw, 3)   # pas de 2 images, figurine -> tête

    f = kit.at("S08", "grand", "le curseur traîne le mail vers elle, à vitesse constante ; 4 figurines de la foule "
                               "versent chacune un petit papier dans la tête de verre : tout le monde y met ses données")
    pts = S.ents["foule"]["p"]["pts"]
    for k, idx in enumerate((0, 2, 4, 5)):          # 4 papiers décalés de 3 images, finis avant « non »
        cid, g = f"colis{idx + 1}", f + 3 * k
        S.key(cid, "pos", g - 1, list(pts[idx]))
        kit.pop(cid, g, d=3)
        S.key(cid, "pos", g + 3, list(c.pub_head), 6, "in")
        S.key(cid, "scale", g + 7, 0, 2, "in")
        S.key(cid, "opacity", g + 9, 0)
    hit = kit.at("S08", "non", "le mail s'écrase de l'intérieur contre le mur droit de la fenêtre : il se tasse, le mur "
                               "bombe de 10 px vers l'extérieur ; 3 traits d'impact partent de sa face extérieure ; sur "
                               "le pan de mur touché paraissent, en tirets encre pâles, les contours des deux briques à "
                               "venir avec leurs pictogrammes (bouclier-cadenas, bâtiment) : le mur est fait de règles")
    w2 = DOC_W / 2 * round(sc * 1.05, 4)
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
    kit.pop("mur_choc", hit + 1, d=2)                # le mur bombé tient jusqu'après le retour du mail
    for k, v in enumerate(("brique1_vide", "brique2_vide")):   # les règles du mur, en attente de leurs briques
        S.key(v, "scale", hit + 1 + k, 1, 3, "out")              # (S09) ; opacité 0,35 gardée (pas de pop)
    cur_end = S.val("curseur", "pos", hit)
    for k, dx in enumerate((5, -4, 4, -3, 0)):       # il pousse encore et tremble jusqu'à « encadrée. »
        S.key("curseur", "pos", hit + 1 + k, _pt([cur_end[0] + dx, cur_end[1]]))

    f = kit.at("S08", "encadrée.", "le curseur est repoussé et lâche le mail, qui revient tout droit devant l'éventail ; "
                                   "le curseur rentre dans le stylo, le bras retombe ; l'IA grand public reste là")
    S.key("curseur", "press", f, 0, 3, "out")
    S.key("curseur", "pos", f, _pt([cur_end[0] - 30, cur_end[1]]), 3, "out")   # repoussé par le mur : bloqué
    S.key("doc3", "pos", f, _pt(home), 12, "inOut")
    S.key("doc3", "scale", f, sc, 12, "inOut")
    S.key("doc3", "sh", f, 6, 12, "inOut")
    S.key("doc3", "z", f + 12, pile_z(0))
    back = kit.vanish("curseur", f + 3, into=toi.tip(f + 12), d=9)
    S.key("attache", "draw", back, 0)
    toi.rim(back - 2, False, d=2)                    # tour 4 : effacé AVANT que le bras ne se replie (pas de boucle)
    toi.rest(back, 8)
    S.key("mur_choc", "scale", f + 14, 0, 4, "in")   # dernière clé de la partie : avant l'image 609

    _check_entry_p2(S, kit, scene_f0(S, "S09") - 1)
