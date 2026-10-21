"""V01, partie 2 : S09-S14, images 610-1238 (34 temps forts, 21,0 s). Le mur des règles, « 2 · Exiger » (la page
commandée, la fiche écrite par l'IA, la ligne inventée qui devient suspecte, les preuves), puis « 3 · Relire »
(relecture, rature, question gardée « à poser au RDV », tampon PRÊT POUR LE RDV).

État d'entrée, épinglé à l'image 609 : kit.pin(609, ENTRY_P2) (etat_initial de S09 : fenêtre scellée à gauche,
mail revenu sur la pile, marque du choc sur le mur, IA grand public entière à droite, repère sur « 1 · Limiter »).
Figurines : `toi` est dehors en bas à droite (ADV_S08, p1) ; `client` à l'échelle 0 ; jamais épinglés.

Temps forts (image du film, calés par kit.at ; « mot n » = début du mot quand l'attaque audible le devance) :
S09  RGPD=617  politique=654  s’appliquent.=680
S10  Ensuite,=707 (mot 706)  demande=724  brief=738  structuré=747  d’une=763  page.=768 (tenue)
S11  Mais=790 (mot 791)  IA=811  produire=835  réponse=853  fluide…=866  et=893 (tenue)  fausse.=897
S12  Exige=917 (mot 915)  chaque=933  ligne=943  renvoie=952  document=977  date.=1007
S13  Une=1030 (mot 1029)  sans=1043  source,=1049 (tenue)  c’est=1074 (mot 1073)  question=1085  poser=1100
     client.=1111
S14  Dernière=1137 (mot 1138)  étape :=1150  relis,=1170 (mot 1171)  corrige,=1191 (mot 1190)  décide.=1211 (mot 1212)

Scène par scène (tour de revue 1) :
- S09 « RGPD » : la brique encre (bouclier-cadenas + « RGPD », écrits dès qu'elle paraît) tombe d'au-dessous de la
  barre de titre et s'encastre à cheval sur le mur, sur la marque du choc, qu'elle couvre. « politique » : la 2e brique
  (bâtiment à colonnes du sceau « ✓ Cabinet » + « Politique interne ») se pose dessus : la règle du cabinet.
  « s’appliquent. » : le cadenas tombe et se ferme ; PUIS (cause : le cadenas) l'IA grand public et sa foule se
  réduisent en point.
- S10 « Ensuite, » : textes des briques en fondu, puis elles rentrent dans le mur ; la fenêtre s'élargit ; le
  conseiller regagne son coin. « demande » : la page vide part de sa main ; « 2 · Exiger ». « brief », « structuré » :
  les 4 pastilles. « d’une » : la tête de l'IA étincelle, 3 bulles de pensée pointillées montent de sa tête jusqu'à la
  5e puce, vide, x 1,6. « page. » : tenue 0,45 s, puis elle tombe sur l'onglet 5 (posée 5 images avant « Mais »).
- S11 « Mais » : badge, page au centre, pastille sur l'en-tête. « IA » : faisceau tête -> badge. « produire » : pour
  chaque ligne, le pictogramme du document (€, barres, sablier, bouclier) bat dans le badge et une copie voyage par le
  faisceau jusqu'à la puce ; la ligne s'écrit pendant que la pointe du faisceau file sous elle jusqu'au carré tireté
  de la coche : au contact, la coche pointillée de l'IA (gris encre, 46 px) s'y trace. « réponse » : rien du badge :
  la tête étincelle, son faisceau va à la puce vide de L5, la ligne s'écrit, la pointe file jusqu'au carré, coche.
  « fluide… » : reflet. « fausse. » : la puce vide de L5 bat deux fois (x 2,2), deux ondes rouges en partent ; elle
  reste x 1,3, contour rouge ; un contour rouge en tirets entoure la rangée L5 (jusqu'à « c’est ») ; texte à l'encre,
  rien ne se fend, la coche de l'IA reste.
- S12 : prise en main, cases, documents, fils, dates (inchangé).
- S13 « Une » : étiquettes-sources ; le conseiller redescend AU PIED DE LA PAGE, à gauche de la colonne des sources
  (x 580) : sous la case 5, l'ivoire est vide. « sans » : surligneur ; le fil de L5 touche le bord de la case 5 (tenu
  4 images, la case tremble) puis retombe tout droit dans le vide (y 1090), loin de toute figurine. « c’est » : le stylo
  touche « 5 ans » : rouge, fente ; le contour rouge de la rangée s'efface. « question » : « ? » sur la case 5.
  « poser » : la bulle grandit décalée vers la droite (760, 860), queue sur la tête du conseiller, corps vers la place du
  client. « client. » : la pastille de la fiche bat ; le client en sort à x 0,5, longe l'en-tête puis descend le bord
  droit, et grandit sous le côté ouvert de la bulle (arrivé à 1129) ; la bulle penche de 5° vers lui.
- S14 « Dernière » : « 3 · Relire » ; la bulle se replie en autocollant. « étape : » / « relis, » : sur chaque ligne
  prouvée, la coche pointillée de l'IA bat (x 1,15) sous la pointe, puis la coche pleine se trace dessus (8 images).
  « corrige, » : la coche de l'IA de L5 repart en arc vers l'IA (450 ms), rendue à son auteur, son carré reste vide ;
  le stylo barre « 5 ans » (10 images), la valeur barrée reste 0,2 s puis tombe ; « à poser au RDV » (mini-horloge +
  pictogramme du client) apparaît. « décide. » : tampon ; le conseiller s'écarte en 5 images : tampon lisible dès 1222.
Raccord : à l'image 1238 l'état est ENTRY_P3.
"""
import math

from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, line_crack_point
from pipeline.story_kit import REACH, REACH_STAMP, TAP, frames, lerp

from . import (ADV_REST, ADV_S12, ADV_S13, BADGE, BRICK_H, BRICKS, BUBBLE_AT, BUBBLE_BIG, CASE_W, CASE_X, CHOC,
               CLIENT_S13, ENTRY_P2, IA_CORNER, IA_CORNER_SCALE, IA_PILL_CORNER, IA_S10, IA_S11, PAGE_S10,
               PAGE_S10_SCALE, PAGE_S11, PAGE_S12, PAGE_S12_SCALE, PILE_S10, PILE_S10_SCALE, PILE_SLOT, PILL_ICON,
               TITLE_H, WIN_S08_POS, WIN_S08_SCALE, WIN_S10, FRAME_H, pile_pt, scene_f0, vanish)

# ---------- places propres à p2 ----------
# S10 : fenêtre élargie x 80-770 (et non 80-900) et page en x 600 : le stylo levé du conseiller, au repos en bas à
# droite (ADV_REST), reste dehors, à 29 px du bord de la fenêtre.
WIN10 = dict(pos=(425, WIN_S10["pos"][1]), w=690, h=WIN_S10["h"])
PAGE10 = (600, PAGE_S10[1])
TITLE_S10 = (WIN10["pos"][0] - 60, WIN10["pos"][1] - WIN10["h"] / 2 + TITLE_H / 2)   # titre, avant le cadenas
PILE_AIM = [-230, -40]               # S10 : bout du faisceau de lecture, bas de la pile (repère de la fenêtre)
BADGE_AIM = [-80, 85]                # S11 : le même faisceau sur le bas du badge (ancre déclarée)
HOVER_X = 400                        # S10 : colonne des puces sorties de la pile, entre la pile et la page
PUCE5_AT, PUCE5_SCALE = (380, 760), 1.6   # S10 : la puce vide, en haut à droite de la tête de l'IA, x 1,6
BADGE_DOC_SCALE = 0.45               # documents compacts rangés dans le badge (S11-S12)
IA_S11_AT = (IA_S11[0] - 10, IA_S11[1] - 20)   # pilule « IA » au-dessus de y 1270 ; tête à gauche des puces
PAGE11 = (PAGE_S11[0] - 15, PAGE_S11[1])  # S11 : la page à 16 px du stylo levé du conseiller (ADV_REST)
PAGE12_EXIGE = (480, PAGE_S12[1])    # S12 « Exige » : premier glissement, sans couvrir l'IA ; PAGE_S12 sur « chaque »
VIA_DX = 48                          # S11 : le faisceau descend la marge gauche, 48 px à gauche de la colonne des puces
UNDER = 28                           # S11 : la pointe du faisceau file 28 px sous le centre de la rangée (sous le texte)
WRITE11 = 5.5                        # S11 : caractères par image (4 lignes en 18 images, avant « réponse »)
ADV_S12_Y = 780                      # S12 : épaule à mi-hauteur de la colonne des cases (x : 5 cases à portée)
ADV_S14_Y = (760, 920)               # S14 : relecture de L1-L2 (haut), puis L5 et sa valeur (bas) : stylo de 90 px
ADV_END = [665, 860]                 # fin de S14 : à droite de la page, stylo levé hors de la page
CORRIDOR_Y = 385                     # S12 : couloir des documents entre la légende du repère et le haut de la page
DOC_ANCHOR = [-71, 23]               # bout du fil sur le document : bord gauche, à la hauteur de la ligne de date
STICKER_SCALE = 0.68                 # autocollant « ? » : 72 px x 0,68 x 0,95 = 47 px, « ? » de 31 px (= valeur)
STAMP_AT, STAMP_ROT = [-10, 300], -4  # tampon : bout droit à gauche du corps du conseiller (x < 560 monde)
HANG = (700, 1095)                   # S13 : le fil de L5 retombe dans le vide, sous la case 5, loin du conseiller


def _catmull(pts, n=24):
    """Points denses d'une courbe de Catmull-Rom passant par `pts` (trajet lisse du client)."""
    P = [pts[0]] + [list(p) for p in pts] + [pts[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            out.append([0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                               + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in (0, 1)])
    out.append(list(pts[-1]))
    acc = [0.0]
    for a, b in zip(out, out[1:]):
        acc.append(acc[-1] + math.dist(a, b))
    return out, acc


def _at_length(curve, frac):
    out, acc = curve
    target = max(0.0, min(1.0, frac)) * acc[-1]
    for i in range(1, len(out)):
        if acc[i] >= target:
            t = (target - acc[i - 1]) / max(1e-9, acc[i] - acc[i - 1])
            return lerp(out[i - 1], out[i], t)
    return out[-1]


def _cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return [u ** 3 * p0[k] + 3 * u * u * t * p1[k] + 3 * u * t * t * p2[k] + t ** 3 * p3[k] for k in (0, 1)]


def _poly(pts, frac):
    """Point à la fraction `frac` de la longueur d'une polyligne."""
    acc = [0.0]
    for a, b in zip(pts, pts[1:]):
        acc.append(acc[-1] + math.dist(a, b))
    s = max(0.0, min(1.0, frac)) * acc[-1]
    for i in range(1, len(acc)):
        if acc[i] >= s - 1e-9:
            t = (s - acc[i - 1]) / max(1e-9, acc[i] - acc[i - 1])
            return lerp(pts[i - 1], pts[i], t)
    return list(pts[-1])


def _r(p):
    return [round(p[0], 2), round(p[1], 2)]


def part(S, kit, c):
    toi, sheet = c.toi, c.sheet                         # le client (sans outil) se pilote par S.path
    rows, X, ty, ly = sheet.rows, sheet.x, sheet.ty, sheet.ly
    p5 = sheet.lines[4][1]                                  # paramètres de L5 (fente, valeur mesurée)
    f0 = scene_f0(S, "S09")                                 # 610

    kit.pin(f0 - 1, ENTRY_P2)                               # etat_initial de S09
    if S.val("toi", "scale", f0 - 1) == 0:                  # partie construite seule : la figurine n'est pas entrée
        toi.enter(f0 - 10, at=list(ADV_REST))

    def spot_for(targets, y, x_hi, n, margin=0.985):
        """Place du conseiller (centre, échelle 1) à la hauteur y, la plus à droite (<= x_hi) d'où tous les `targets`
        (points monde) sont à portée confortable du stylo de 90 px (REACH x allonge, moins 1,5 %)."""
        R = margin * REACH * toi.reach_max(n)
        for x in range(round(x_hi), round(x_hi) - 300, -1):
            A = [x + toi.shoulder[0], y + toi.shoulder[1]]
            if all(math.dist(A, t) <= R for t in targets):
                return [x, y]
        raise SystemExit(f"p2 : aucune place à y {y} pour {len(targets)} cibles")

    # Mise en place de S12-S14, entités encore invisibles (clés directes : rien ne saute à l'écran).
    def row_c(i):                                            # centre monde de la rangée i, page en PAGE_S12
        return round(PAGE_S12[1] + rows[i] * PAGE_S12_SCALE, 2)

    def date_y(i):                                           # ligne de date monde de la rangée i (PAGE_S12)
        return round(PAGE_S12[1] + (rows[i] + ly) * PAGE_S12_SCALE, 2)

    for i in range(5):
        S.key(f"case{i + 1}", "pos", f0 - 1, [CASE_X, row_c(i)])
    for i in range(4):
        kit.ensure(f"fil{i + 1}", "bAt", list(DOC_ANCHOR))
        S.key(f"fil{i + 1}", "aAt", f0 - 1, [X["value"] + 10, rows[i] + ly])
    kit.ensure("fil5", "aAt", [X["value"] + 10, rows[4] + ly])
    S.key("fil5", "pb", f0 - 1, [CASE_X - CASE_W / 2 + 2, date_y(4)])
    S.key("tampon", "pos", f0 - 1, list(STAMP_AT))
    S.key("tampon", "rot", f0 - 1, STAMP_ROT)
    S.key("autocollant", "scale", f0 - 1, STICKER_SCALE)
    kit.ensure("faisceau_lit", "bAt", list(BADGE_AIM))

    # =================== S09 « Le RGPD et ta politique interne s’appliquent. » ===================
    win_top = WIN_S08_POS[1] - FRAME_H / 2 * WIN_S08_SCALE
    bar_bottom = win_top + TITLE_H * WIN_S08_SCALE + 3      # les briques partent sous la barre de titre

    def brick_drop(k, f):
        """La brique k tombe de sous la barre de titre et s'encastre ; son pictogramme et son texte sont écrits dès
        qu'elle paraît (jamais une dalle vide). Renvoie l'image d'arrivée."""
        b = f"brique{k + 1}"
        x, y = BRICKS[k][1]
        h = round(y - BRICK_H / 2 - bar_bottom)
        S.key(b, "pos", f - 1, [x, y - h])
        S.key(b, "scale", f, 1)                              # visible SUR le mot, pas une image avant
        S.key(b, "pos", f, [x, y], DROP, "out")
        for ch in (f"{b}_txt", f"{b}_ico") + (("brique1_cad",) if k == 0 else ()):
            S.key(ch, "opacity", f, 1)
        return f + DROP

    f = kit.at("S09", "RGPD", "une brique encre (bouclier-cadenas, « RGPD ») tombe et s'encastre à cheval sur le mur "
               "droit de la fenêtre, sur la marque du choc du mail, qu'elle couvre")
    land = brick_drop(0, f)
    S.key("impact2", "scale", land - 2, 0)                   # la marque du choc est sous la brique

    f = kit.at("S09", "politique", "une 2e brique (bâtiment du cabinet, « Politique interne ») tombe et se pose sur la "
               "première, ferme, sans rebond")
    brick_drop(1, f)

    f = kit.at("S09", "s’appliquent.", "un cadenas tombe sur la barre de titre et son anse se ferme ; alors seulement, "
               "l'IA grand public et sa foule se réduisent en point")
    S.key("outil", "lockDy", f - 1, -120)                     # part sous la légende du repère
    S.key("outil", "lockOn", f, 1)
    S.key("outil", "lockDy", f, 0, DROP, "out")
    S.key("outil", "lock", f + DROP, 1, 5, "out")
    vanish(kit, "ia_pub", f + DROP + 5)                      # le cadenas fermé la fait disparaître

    # =================== S10 « Ensuite, demande un brief structuré d’une page. » ===================
    f = kit.at("S10", "Ensuite,", "les textes des briques s'effacent et les briques rentrent dans le mur ; la fenêtre "
               "verrouillée s'élargit, la pile en haut à gauche, l'IA en bas à gauche ; le conseiller regagne son coin")
    for b in ("brique1", "brique2"):                        # échelle uniforme : jamais de texte écrasé
        vanish(kit, b, f, into=[S.val(b, "pos", f - 1)[0] - 40, S.val(b, "pos", f - 1)[1]], d=MORPH)
    d = 12
    S.keys("outil", f, d, "inOut", pos=list(WIN10["pos"]), w=WIN10["w"], h=WIN10["h"], scale=1)
    for i in range(4):
        S.keys(f"doc{i + 1}", f, d, "inOut", pos=pile_pt(PILE_S10, PILE_SLOT[i]), scale=PILE_S10_SCALE)
    S.keys("ia", f, d, "inOut", pos=list(IA_S10), scale=1)
    S.keys("pastille", f, d, "inOut", pos=list(TITLE_S10), scale=1)
    toi.walk(f, list(ADV_REST), d=d)

    f = kit.at("S10", "demande", "une page vide à 5 onglets part de la main du conseiller et se pose en arc dans la "
               "fenêtre ; le repère passe au « 2 · Exiger »")
    if S.val("toi", "scale", f - 1) == 0:                   # partie seule
        toi.enter(f, at=list(ADV_REST))
    kit.step(f, 1)
    g = f + 2
    S.key("fiche", "pos", g - 1, [round(v, 2) for v in S.to_world("toi", toi.hand, g - 1)])
    S.fly("fiche", g, 12, "inOut", to=list(PAGE10), scale=PAGE_S10_SCALE, arc=80)

    def tab_w(i, n):                                         # onglet (= puce) de la rangée i, en monde
        return S.to_world("fiche", [X["bullet"], rows[i] + ty], n)

    f = kit.at("S10", "brief", "le faisceau pointillé de l'IA passe sur la pile ; de chaque document sort une pastille "
               "pleine (€, barres, sablier, bouclier) qui se range en face de son onglet")
    S.key("faisceau_lit", "bAt", f - 1, list(PILE_AIM))
    kit.draw("faisceau_lit", f, 6)
    for i in range(4):
        hover = [HOVER_X, round(tab_w(i, f)[1], 2)]
        kit.pop(f"puce{i + 1}", f + 2 * i, from_pt=pile_pt(PILE_S10, PILE_SLOT[i]), to=hover)

    f = kit.at("S10", "structuré", "les 4 pastilles glissent sur les onglets 1 à 4 et deviennent les puces des lignes ; "
               "le faisceau rentre")
    S.key("faisceau_lit", "draw", f, 0, 5, "in")
    for i in range(4):
        g = f + 2 * i
        S.fly(f"puce{i + 1}", g, MORPH, "inOut", to=tab_w(i, g), scale=PAGE_S10_SCALE, arc=20)
        arr = g + MORPH
        S.key(f"puce{i + 1}", "opacity", arr, 0)
        S.key("fiche", f"tab{i}", arr, 0)
        S.key(f"L{i + 1}", "bulletOn", arr, 1)

    f = kit.at("S10", "d’une", "seule, la tête de l'IA étincelle ; 3 bulles de pensée pointillées montent de sa tête ; "
               "une 5e puce, vide et pointillée, grande, en sort et reste au bout")
    S.key("ia_eclat", "p", f, 1, POP, "linear")
    head = S.to_world("ia", c.brain_top, f - 1)
    for k in range(3):
        t = (k + 1) / 4
        at = [head[0] + (PUCE5_AT[0] - head[0]) * t, head[1] + (PUCE5_AT[1] - head[1]) * t + 6]
        S.key(f"pensee{k + 1}", "pos", f - 1, _r(at))
        kit.pop(f"pensee{k + 1}", f + 2 * k, d=5)
    kit.pop("puce5", f + 4, scale=PUCE5_SCALE, from_pt=head, to=list(PUCE5_AT), d=8)

    beat = kit.hold("S10", "page.", "tenue : la grande puce vide reste seule au bout des bulles de pensée, puis tombe sur "
                    "l'onglet 5 ; tout s'immobilise avant « Mais »")
    g = beat + 9                                             # 0,45 s après son apparition (763 + 4)
    S.fly("puce5", g, 8, "inOut", to=tab_w(4, g), scale=PAGE_S10_SCALE, arc=40)
    for k in range(3):
        vanish(kit, f"pensee{k + 1}", g + k, d=5)
    arr = g + 8
    S.key("puce5", "opacity", arr, 0)
    S.key("fiche", "tab4", arr, 0)
    S.key("L5", "bulletOn", arr, 1)

    # =================== S11 « Mais une IA peut produire une réponse fluide… et fausse. » ===================
    f = kit.at("S11", "Mais", "la fenêtre se réduit en badge en haut à gauche avec la pile ; la page vient au centre en "
               "grandissant ; la pastille vole se poser sur son en-tête ; l'IA reste en bas à gauche")
    S.keys("outil", f, MORPH, "out", pos=list(BADGE["pos"]), w=BADGE["w"], h=BADGE["h"], scale=BADGE["scale"], seal=0)
    for i in range(4):
        sl = PILE_SLOT[i]
        bp = [BADGE["pos"][0] - 6 + 4 * sl, BADGE["pos"][1] + 10 + 4 * sl]
        S.keys(f"doc{i + 1}", f, MORPH, "out", pos=bp, scale=BADGE_DOC_SCALE, compact=1, txt=0)
    S.keys("ia", f, MORPH, "out", pos=list(IA_S11_AT), scale=1)
    S.keys("fiche", f, MORPH, "out", pos=list(PAGE11), scale=1)
    head_w = [PAGE11[0] + c.header_pill[0], PAGE11[1] + c.header_pill[1]]
    S.fly("pastille", f, MOVE, "inOut", to=head_w, scale=1, arc=40)
    S.key("pastille", "opacity", f + MOVE, 0)
    S.key("pastille_fiche", "opacity", f + MOVE, 1)

    f = kit.at("S11", "IA", "un faisceau pointillé relie la tête de l'IA au badge des documents")
    S.key("faisceau_lit", "bAt", f - 1, list(BADGE_AIM))
    kit.draw("faisceau_lit", f, 8)

    via_x = PAGE11[0] + X["bullet"] - VIA_DX

    def row_y11(i):
        return PAGE11[1] + rows[i] + ty

    def plug(i):
        return [via_x + 24, row_y11(i)]

    def under(i):                                            # sous la rangée, pointe contre le carré de la coche
        return [round(PAGE11[0] + X["tick"] - 30, 2), PAGE11[1] + rows[i] + UNDER - 6]

    def via_under(i):
        return [via_x, PAGE11[1] + rows[i] + UNDER]

    def glide(wire, g0, g1, a, b, va, vb):
        """La pointe du faisceau file de a à b (et son coude de va à vb) pendant [g0, g1] : elle écrit la ligne."""
        d = max(1, g1 - g0)
        for n, p in frames(g0, d, "inOut"):
            S.key(wire, "pb", n, _r(lerp(a, b, p)), 1, "linear")
            S.key(wire, "via", n, _r(lerp(va, vb, p)), 1, "linear")

    f = kit.at("S11", "produire", "pour chaque ligne, le pictogramme du document bat dans le badge et une copie voyage "
               "par le faisceau jusqu'à la puce ; la ligne s'écrit pendant que la pointe du faisceau file sous elle ; "
               "quand elle touche le carré tireté, la coche pointillée de l'IA s'y trace")
    t = f + 5                                                # la 1re copie arrive à la puce
    for i in range(4):
        lid, did, cid = f"L{i + 1}", f"doc{i + 1}", f"copie{i + 1}"
        g = math.ceil(t - 1e-6)
        p = S.ents[lid]["p"]
        n = len(p["key"]) + len(p["value"])
        # la copie du pictogramme : du document (dans le badge) à la puce, par le chemin du faisceau
        dep = g - 5
        src = S.to_world(did, [0, 0], dep - 1)
        route = [src, [via_x, src[1] + 40], [via_x, row_y11(i)], plug(i)]
        kit.pulse(did, dep, peak=round(S.val(did, "scale", dep - 1) * 1.25, 4), step=2)
        S.key(cid, "pos", dep - 1, _r(src))
        S.key(cid, "scale", dep - 1, 0)
        S.key(cid, "scale", dep, 1, 2, "out")
        for m, q in frames(dep, 5, "inOut"):
            S.key(cid, "pos", m, _r(_poly(route, q)), 1, "linear")
        S.key(cid, "scale", g, 0)
        S.key(cid, "opacity", g, 0)
        # le faisceau (re)vise la puce, puis sa pointe file sous la ligne pendant l'écriture
        aim = dep - 1 if i == 0 else g                       # la 1re fois avant le tracé, ensuite au relais
        S.key("faisceau", "pb", aim, _r(plug(i)))
        S.key("faisceau", "via", aim, [via_x, row_y11(i)])
        if i == 0:
            kit.draw("faisceau", g - 3, 3)
        end = kit.type(lid, g, rate=WRITE11, flash=True)
        glide("faisceau", g, end, plug(i), under(i), [via_x, row_y11(i)], via_under(i))
        kit.draw(f"coche_ia{i + 1}", end, 6)                 # au contact du faisceau
        t = end

    f = kit.at("S11", "réponse", "le faisceau du badge se retire : la tête de l'IA étincelle et un faisceau part de sa "
               "tête vers la puce vide de L5 ; « Horizon : 5 ans » s'écrit, la pointe file sous elle et coche le carré")
    S.key("faisceau", "draw", f, 0, 3, "in")
    S.key("faisceau_lit", "draw", f, 0, 3, "in")
    S.key("ia_eclat", "p", f - 1, 0)
    S.key("ia_eclat", "p", f, 1, POP, "linear")
    S.key("faisceau_tete", "pb", f - 1, plug(4))
    S.key("faisceau_tete", "via", f - 1, [via_x, row_y11(4)])
    kit.draw("faisceau_tete", f + 1, 4)
    end = kit.type("L5", f + 5, flash=True)
    glide("faisceau_tete", f + 5, end + 1, plug(4), under(4), [via_x, row_y11(4)], via_under(4))
    kit.draw("coche_ia5", end + 1, 6)

    f = kit.at("S11", "fluide…", "un reflet traverse la page sous les textes ; le faisceau s'efface ; puis immobilité")
    S.key("reflet", "p", f, 1, 12, "linear")
    S.key("faisceau_tete", "draw", f + 2, 0, 4, "in")

    kit.hold("S11", "et", "tenue : rien ne bouge, la fiche entièrement cochée par l'IA")

    f = kit.at("S11", "fausse.", "la puce vide de L5 bat deux fois très fort (x 2,2), deux ondes rouges en partent ; elle "
               "reste grosse, contour rouge ; un contour rouge en tirets entoure la rangée ; le texte reste à l'encre, "
               "rien ne se fend, l'IA et sa coche ne bougent pas")
    S.key("L5", "bulletOn", f, 0)                            # relais : la même puce, enfant de la fiche, au-dessus
    S.key("puce5_alerte", "opacity", f, 1)
    S.key("puce5_alerte", "alarm", f, 1, 3, "out")
    for k in range(2):
        g = f + 6 * k
        S.key("puce5_alerte", "scale", g, 2.2, 3, "out")
        S.key("puce5_alerte", "scale", g + 3, 1.3 if k else 1.2, 3, "inOut")
        o = f"onde{k + 1}"
        S.key(o, "scale", g, 1)
        S.key(o, "scale", g + 1, 3.2, 8, "out")
        S.key(o, "opacity", g + 1, 0, 8, "in")
        S.key(o, "scale", g + 9, 0)
    kit.draw("cadre5", f + 3, 8, e="inOut")
    kit.pop("anneau5", f + 12, scale=1.3, d=3)               # la puce reste x 1,3, cerclée de rouge plein

    # =================== S12 « Exige que chaque ligne renvoie à un document et à une date. » ===================
    f = kit.at("S12", "Exige", "le conseiller prend la main : il monte à droite de la page, stylo levé ; la page glisse "
               "un peu à gauche pour lui faire place ; les 5 coches de l'IA restent")
    cases = [[CASE_X, row_c(i)] for i in range(5)]
    adv12 = spot_for(cases, ADV_S12_Y, ADV_S12[0], f - 1)
    toi.walk(f, adv12, d=12)
    S.keys("fiche", f, MOVE, "inOut", pos=list(PAGE12_EXIGE), scale=PAGE_S12_SCALE)

    f = kit.at("S12", "chaque", "l'IA se range, plus petite, dans le coin en bas à gauche, toujours visible, sa pilule "
               "« IA » à droite de la tête ; la page finit de glisser à gauche")
    S.keys("ia", f, MOVE, "out", pos=list(IA_CORNER), scale=IA_CORNER_SCALE)
    S.keys("ia_pill", f, MOVE, "out", pos=list(IA_PILL_CORNER), scale=round(1 / IA_CORNER_SCALE, 4))
    S.keys("fiche", f, MOVE, "inOut", pos=list(PAGE_S12))

    f = kit.at("S12", "ligne", "le stylo descend la colonne et trace, en face de chaque ligne, une case-source vide en "
               "tirets")
    hits = toi.trace(f, cases, d=10, lead=4)
    for i, h in enumerate(hits):
        kit.draw(f"case{i + 1}", h - 1, 3)
    toi.rest(hits[-1] + 1, 8)

    f = kit.at("S12", "renvoie", "les 4 documents sortent du badge, passent au-dessus de la page et se logent dans les "
               "cases 1 à 4 ; le badge vidé se replie ; la case 5 reste vide")
    for i in range(4):
        d_id, g = f"doc{i + 1}", f + 3 * i
        p0 = S.to_world(d_id, [0, 0], g - 1)
        s0 = S.world_scale(d_id, g - 1)
        p1, p2, p3 = [p0[0] + 220, CORRIDOR_Y], [CASE_X + 80, CORRIDOR_Y], cases[i]   # arrive par le haut droit
        S.key(d_id, "z", g, 12.5 + 0.1 * i)                 # celui qui vole passe devant ceux déjà posés
        S.path(d_id, g, 13, "inOut", lambda p, p0=p0, p1=p1, p2=p2, p3=p3: _cubic(p0, p1, p2, p3, p),
               lambda p, s0=s0: s0 + (PAGE_S12_SCALE - s0) * p * p)
    vanish(kit, "outil", f + 3 * 3 + 3)

    f = kit.at("S12", "document", "un fil cyan profond plein part de chaque valeur L1-L4 et se tend jusqu'à son document")
    for i in range(4):
        kit.draw(f"fil{i + 1}", f + 3 * i, DRAW)

    f = kit.at("S12", "date.", "de chaque document sort sa date écrite en clair sur une petite page cornée ; elle "
               "glisse le long du fil et se pose sous sa valeur")
    for i in range(4):
        src, fil, g = f"source{i + 1}", f"fil{i + 1}", f + 2 * i
        cub = S.wire_cubic(fil, g)
        a_x, b_x = cub[0][0], cub[3][0]
        doc_x = S.to_world(f"doc{i + 1}", [0, 0], g)[0]
        tgt_x = S.to_world("fiche", [c.tag_cx, rows[i] + ly], g)[0]
        o0, o1 = doc_x - b_x, tgt_x - a_x
        S.along_wire(src, fil, g, 12, "inOut", 1.0, 0.0, at_frame=g, offset=lambda p, o0=o0, o1=o1: (o0 + (o1 - o0) * p, 0))
        kit.pop(src, g, d=6)

    # =================== S13 « Une info sans source, c’est une question à poser au client. » ===================
    f = kit.at("S13", "Une", "chaque document remonte son fil et se réduit dans son étiquette-source au bout de sa "
               "ligne ; les fils rentrent ; les cases 1-4 s'effacent, la case 5 reste vide ; le conseiller redescend au "
               "pied de la page, à gauche de la colonne des sources : sous la case 5, l'ivoire reste vide")
    dur = MORPH
    for i in range(4):
        d_id, src, fil = f"doc{i + 1}", f"source{i + 1}", f"fil{i + 1}"
        a = S.to_world(d_id, [0, 0], f - 1)
        b = S.to_world(src, [-S.ents[src]["p"]["tag"]["w"] / 2 + 24, 0], f - 1)   # droit sur la pastille
        S.key(d_id, "z", f, 12.8 + 0.01 * i)                # au-dessus de l'étiquette qu'il rejoint
        S.path(d_id, f, dur, "inOut", lambda p, a=a, b=b: lerp(a, b, p))
        S.key(d_id, "tag", f, 1, dur, "inOut")
        S.key(fil, "from", f, 1, 5, "linear")
        S.key(fil, "opacity", f + 5, 0)
        arr = f + dur
        S.key(d_id, "opacity", arr, 0)
        S.key(src, "flash", arr, 1, 2, "out")
        S.key(src, "flash", arr + 2, 0, 3, "inOut")
        S.key(f"case{i + 1}", "draw", f, 0, dur, "in")
    down = [adv12[0], ADV_S13[1]]
    g = toi.walk(f, down, d=7)
    toi.walk(g, list(ADV_S13), d=9)                          # x 580 : la place sous la case 5 reste vide

    f = kit.at("S13", "sans", "un surligneur cyan pâle s'étire sous « Horizon : 5 ans » ; la ligne lance le même fil vers "
               "la case 5 : il en touche le bord, n'y trouve rien (la case tremble) et retombe tout droit dans le vide")
    sl_w = X["slot1"] - X["slot0"]
    sl_y = rows[4] + ty
    S.key("surligneur", "w", f - 1, 0)
    S.key("surligneur", "pos", f - 1, [X["slot0"], sl_y])
    S.key("surligneur", "scale", f - 1, 1)
    S.key("surligneur", "w", f, sl_w, FADE, "out")
    S.key("surligneur", "pos", f, [round((X["slot0"] + X["slot1"]) / 2, 1), sl_y], FADE, "out")
    S.key("L5", "slotFill", f, 0, FADE, "out")
    kit.draw("fil5", f, 4)
    touch = f + 3
    kit.shake("case5", touch + 1, amp=6)
    hang = list(HANG)                                        # sous la case 5 : ivoire vide, loin du conseiller
    S.key("fil5", "pb", touch + 4, hang, 9, "in")           # tenu 4 images au bord, puis il tombe

    kit.hold("S13", "source,", "tenue : le fil pend dans le vide sous la case 5, la case reste un contour vide, la ligne "
             "Horizon en lumière ; rien ne bouge")

    f = kit.at("S13", "c’est", "le stylo du conseiller touche « 5 ans » : au contact, la ligne vire au rouge et se fend ; "
               "la coche pointillée de l'IA reste, l'IA ne bouge pas")
    vx = X["value"] - p5["valueW"] / 2
    hit = toi.tap(f - TAP + 1, S.to_world("L5", [X["value"] - 15, ty], f - 1))   # sur « ans » : à portée
    S.key("L5", "red", hit, 1, 3, "out")
    S.key("L5", "crack", hit, 1, POP, "out")
    kit.fade("cadre5", hit, 0, d=4)                          # le soupçon devient le verdict, sous le stylo

    f = kit.at("S13", "question", "un grand « ? » sort de la valeur fendue sous la pointe et prend la place de la case 5, "
               "qui se replie avec le fil")
    v_pt = S.to_world("L5", line_crack_point(p5, [vx, ty], 1.0), f - 1)
    kit.pop("question", f, from_pt=v_pt, to=list(cases[4]))
    vanish(kit, "case5", f)
    S.key("fil5", "draw", f, 0, 6, "in")
    toi.rest(f + 3, 8)

    f = kit.at("S13", "poser", "le « ? » monte dans une bulle qui grandit à droite du conseiller, queue sur sa tête, son "
               "corps tourné vers la place du client")
    kit.pop("bulle", f)
    q_at = [BUBBLE_AT[0] + BUBBLE_BIG["qx"], BUBBLE_AT[1]]
    S.fly("question", f, 10, "inOut", to=q_at, scale=BUBBLE_BIG["q"] / 110, arc=30)
    arr = f + 10
    S.key("question", "opacity", arr, 0)
    S.key("question", "scale", arr, 0)
    S.key("bulle", "q", arr, 1)

    f = kit.at("S13", "client.", "la pastille de la fiche bat ; le client naît de son pictogramme, longe l'en-tête, "
               "descend le bord droit et grandit sous le côté ouvert de la bulle, face au conseiller ; la bulle penche "
               "vers lui")
    kit.pulse("pastille_fiche", f, peak=1.15, step=3)
    icon_w = S.to_world("pastille_fiche", PILL_ICON, f - 1)
    head_y = icon_w[1]
    route = _catmull([icon_w, [icon_w[0] + 160, head_y], [600, head_y], [872, 560], [884, 900],
                      list(CLIENT_S13)])                    # bord droit de la figurine < 940 (zone réservée)
    dc = 18

    def client_scale(q):                                    # x 0,5 le long de l'en-tête et du bord, puis x 1
        return 0.5 if q < 0.84 else 0.5 + 0.5 * (q - 0.84) / 0.16
    S.key("client", "pos", f - 1, [round(v, 2) for v in icon_w])
    S.key("client", "scale", f - 1, 0)
    S.key("client", "opacity", f, 1)
    S.key("client", "scale", f, 0.5, 2, "out")              # x 0,5 dès f + 1, à côté du pictogramme
    S.path("client", f + 2, dc - 2, "inOutSine", lambda q: _at_length(route, q), client_scale)
    arr = f + dc
    kit.ensure("bulle", "rot", 0)
    S.key("bulle", "rot", arr, 5, 3, "out")                  # la bulle penche vers le client qui arrive
    S.key("bulle", "rot", arr + 4, 0, 4, "inOut")

    # =================== S14 « Dernière étape : relis, corrige, décide. » ===================
    f = kit.at("S14", "Dernière", "le repère passe au « 3 · Relire » ; le conseiller monte à droite de la page ; sa bulle "
               "se replie en autocollant « ? » qui va attendre sous « Horizon » ; le client reste")
    kit.step(f, 2)
    ticks = [S.to_world("fiche", sheet.pt(i, "tick"), f) for i in range(5)]
    crack_r = S.to_world("L5", line_crack_point(p5, [X["value"] + 8, ty], 1.0), f)
    crack_l = S.to_world("L5", line_crack_point(p5, [X["value"] - p5["valueW"] - 8, ty], 1.0), f)
    spot_a = spot_for(ticks, ADV_S14_Y[0], 680, f - 1)        # L1 à L5 à portée ; relit L1-L2 d'ici
    spot_b = spot_for(ticks[2:] + [crack_r, crack_l], ADV_S14_Y[1], 640, f - 1)   # L3-L5 et la rature
    toi.walk(f, spot_a, d=10)
    park = S.to_world("fiche", S.val("autocollant", "pos", f), f)
    S.fly("bulle", f, 10, "inOut", to=park, scale=STICKER_SCALE * PAGE_S12_SCALE, arc=30)
    S.key("bulle", "s", f, 1, 6, "out")                     # se replie d'abord, puis glisse
    arr = f + 10
    S.key("bulle", "opacity", arr, 0)
    S.key("bulle", "scale", arr, 0)
    S.key("autocollant", "opacity", arr, 1)

    f = kit.at("S14", "étape :", "le stylo touche la coche pointillée de L1 : elle bat, puis une coche pleine se trace "
               "dessus ; son étiquette-source s'allume ; puis L2")
    toi.walk(f + 11, spot_b, d=26)                          # il descend en relisant (avant trace : le stylo suit)
    hits = toi.trace(f - 3, ticks, d=39, lead=4)            # hits[0] = f ; une ligne toutes les 0,33 s
    for i in range(4):
        kit.pulse(f"coche_ia{i + 1}", hits[i], peak=1.15, step=2)
        kit.draw(f"coche{i + 1}", hits[i] + 1, 8)
        S.key(f"source{i + 1}", "lit", hits[i] + 1, 1, 4, "out")

    kit.at("S14", "relis,", "même geste sur L3 puis L4 : la coche pointillée bat, la coche pleine se trace dessus ; la "
           "pointe s'arrête sur la coche de L5 sans la repasser")

    f = kit.at("S14", "corrige,", "la coche pointillée de l'IA quitte L5 et repart en arc vers l'IA (son carré reste "
               "vide) ; le stylo barre « 5 ans » d'un trait lent, la valeur barrée reste un instant puis tombe ; la "
               "fente se referme ; l'autocollant « ? » prend la place de la valeur ; « à poser au RDV » apparaît dessous")
    # la coche de l'IA de L5, sans son carré, rendue à son auteur
    S.key("coche_ia5", "draw", f, 0.5)                       # le carré tireté reste, vide
    S.key("coche_ia5_vol", "opacity", f, 1)
    ia_head = S.to_world("ia", c.brain_front, f)
    S.key("coche_ia5_vol", "z", f, 16)                       # au-dessus de la page et du stylo pendant son vol
    S.fly("coche_ia5_vol", f + 2, 14, "inOut", to=_r(ia_head), scale=0.8, arc=220)
    S.key("coche_ia5_vol", "opacity", f + 13, 0, 3, "linear")
    g = toi.strike(f, crack_r, crack_l, d=12, line="L5")
    hold = g + 9                                             # la valeur barrée reste 0,3 s
    S.key("L5", "fall", hold, 1, DROP, "in")
    S.key("L5", "crack", g, 0, 8, "inOut")
    S.key("L5", "red", g, 0, 4, "out")
    S.key("puce5_alerte", "alarm", g, 0, 4, "out")           # la puce redevient la puce vide de L5
    S.key("puce5_alerte", "scale", g, 1, 4, "inOut")
    S.key("puce5_alerte", "opacity", g + 4, 0)
    vanish(kit, "anneau5", g, d=4)
    S.key("L5", "bulletOn", g + 4, 1)
    vanish(kit, "surligneur", g)
    S.keys("autocollant", hold + 1, 8, "inOut", pos=[X["value"] - 40, rows[4] + ty - 6])
    kit.pop("source5", g + 1)

    # pas vers le bas de la page, avant « décide » : la poignée du tampon à portée de la main seule
    hit_f = kit.at("S14", "décide.", "le conseiller abat le tampon PRÊT POUR LE RDV en bas de la page, sous « à poser au "
                   "RDV » ; la page tremble ; il s'écarte aussitôt : le tampon se lit en entier, la question reste "
                   "ouverte") + 5
    grip_l = [0, -(S.ents["tampon"]["p"]["h"] / 2 + 14 + 10)]
    rr = math.radians(STAMP_ROT)
    grip_f = [STAMP_AT[0] + grip_l[0] * math.cos(rr) - grip_l[1] * math.sin(rr),
              STAMP_AT[1] + grip_l[0] * math.sin(rr) + grip_l[1] * math.cos(rr)]
    grip_w = S.to_world("fiche", grip_f, hit_f - 6)
    hand_r = 0.94 * REACH_STAMP * toi.reach_max(hit_f - 6, pen=False)
    st_spot = [round(grip_w[0] + hand_r - toi.shoulder[0], 1), round(grip_w[1] - toi.shoulder[1], 1)]
    w0 = max(g, hit_f - 5 - 7)                               # le pas vers le tampon, après le trait
    toi.walk(w0, st_spot, d=hit_f - 5 - w0)
    f = hit_f - 5
    hit = toi.stamp(f, "tampon", shake="fiche", step=False)
    toi.walk(hit + 1, ADV_END, d=5)                          # il s'écarte en 5 images : tampon entier lisible
    toi.rest(hit + 6, 4)                                     # le bras suit le corps déplacé (fin du geste du tampon)
