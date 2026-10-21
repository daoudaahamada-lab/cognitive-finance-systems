"""V01, partie 2 : S09-S14, images 610-1238 (34 temps forts, 21,0 s). Le mur des règles, « 2 · Exiger » (la page
commandée, la fiche écrite par l'IA, la ligne inventée qui devient suspecte, les preuves), puis « 3 · Relire »
(relecture, rature, question gardée « à poser au RDV », tampon PRÊT POUR LE RDV).

État d'entrée, épinglé à l'image 609 : kit.pin(609, ENTRY_P2) (etat_initial de S09 : fenêtre scellée à gauche,
mail revenu devant l'éventail, marque du choc sur la face extérieure du mur, IA grand public entière à droite, repère
sur « 1 · Limiter »). Figurines : `toi` dehors en bas à droite (p1) ; `client` à l'échelle 0 ; jamais épinglés.

Temps forts (image du film, calés par kit.at ; « mot n » = début du mot quand l'attaque audible le devance) :
S09  RGPD=617  politique=654  s’appliquent.=680
S10  Ensuite,=707 (mot 706)  demande=724  brief=738  structuré=747  d’une=763  page.=768 (tenue)
S11  Mais=790 (mot 791)  IA=811  produire=835  réponse=853  fluide…=866  et=893 (tenue)  fausse.=897
S12  Exige=917 (mot 915)  chaque=933  ligne=943  renvoie=952  document=977  date.=1007
S13  Une=1030 (mot 1029)  sans=1043  source,=1049 (tenue)  c’est=1074 (mot 1073)  question=1085  poser=1100
     client.=1111
S14  Dernière=1137 (mot 1138)  étape :=1150  relis,=1170 (mot 1171)  corrige,=1191 (mot 1190)  décide.=1211 (mot 1212)

Scène par scène (tour de revue 3) :
- S09 « RGPD » : la brique encre (bouclier-cadenas + « RGPD », 32 px) tombe et s'encastre à cheval sur le mur, sur la
  marque du choc ; au contact, l'IA grand public recule (elle rapetisse et s'écarte : le mur l'écarte).
  « politique » : la 2e brique. « s’appliquent. » : un grand cadenas (piste window lockK) tombe sur le mur droit,
  au-dessus des briques (pistes lockDx / lockDy), son anse se ferme ; PUIS l'IA grand public, sa foule et sa pilule se
  réduisent en point ; le cadenas reste accroché au mur (x 2,4) jusqu'au badge.
- S10 « Ensuite, » : chaque brique s'écrase DANS le mur en 6 images (corps et texte s'effacent ensemble : jamais de
  pavé noir sans texte) ; la fenêtre s'élargit (le cadenas suit le mur) ; l'éventail en haut à gauche, l'IA en bas à
  gauche ; le conseiller regagne son coin. « demande » : il tend le bras vers la fenêtre, la page naît dans sa main, ses
  5 onglets paraissent un à un, puis elle vole dans la fenêtre ; « 2 · Exiger ». « brief », « structuré » : les 4
  pastilles, chacune sortie de son document. « d’une » : éclat, bulles de pensée, puce vide x 1,6 : tout fini en 5
  images. « page. » : tenue immobile 0,4 s, puis la puce tombe sur l'onglet 5.
- S11 « Mais » : badge (cadenas sur son bord droit), page au centre agrandie (x 1,18, y 400-1250), IA en bas à gauche
  (x 0,8), pilule au-dessus de la tête. « IA » : faisceau tête -> badge. « produire » : pour L1-L4, la carte source
  s'allume dans le badge (cyan pâle) et son pictogramme glisse le long du faisceau jusqu'à la puce ; la ligne s'écrit ;
  puis un court faisceau pointillé part de la TÊTE de l'IA jusqu'au carré de la ligne et y trace sa coche pointillée
  (56 px). « réponse » : rien du badge ; grand éclat (12 rayons) ; le faisceau part de la tête vers la puce de L5, qui
  reste VIDE pendant que la ligne s'écrit ; coche de la tête. « fluide… » : reflet. « fausse. » : la puce vide de L5
  bat deux fois (x 1,3), deux ondes rouges, anneau rouge ; pas de contour autour de la ligne.
- S12-S13 : comme au tour 2 ; les fils passent sous les carrés des coches (fond papier) ; les documents qui rentrent
  dans leurs étiquettes passent sous elles.
- S13 « client. » : le client naît du pictogramme de la pastille (rig : enter, run, scale_to) et vient sous la bulle.
- S14 « Dernière » : « 3 · Relire » (un seul disque qui glisse) ; la fiche grandit pour la relecture (x 1,1, x 120-670,
  y 409-1201) ; le conseiller (x 1,1) monte à droite ; la bulle se replie en autocollant « ? » (96 px). « étape : » /
  « relis, » : à chaque contact, la coche pointillée de l'IA bat (x 1,3), puis le stylo trace dessus la coche pleine
  cyan profond (trait de 10, 8 images). « corrige, » : la coche de l'IA de L5 s'envole en tournant (12 images) et finit
  contre l'IA ; son carré reste vide ; le stylo barre « 5 ans », qui tombe ; l'autocollant « ? » prend la place de la
  valeur (« Horizon : ? ») ; un fil pointillé cyan va du « ? » à la tête du client, qui hoche la tête deux fois ; une
  réplique de la pastille (« 9 h ») naît de l'en-tête et glisse devant « à poser au RDV ». « décide. » : tampon ; il
  s'écarte : la ligne sans coche reste à côté du tampon.
Tour de revue 4 : briques tombées DANS leurs contours tiretés (posés en S08 « non »), pictogrammes de 72-76 px ;
« IA grand public » s'efface sans rétrécir ; S10 : grand éclat, puce vide de 115 px à droite de la tête, traînée tête
-> onglet 5 ; S11 : page x 1,12, cascade L1-L4 finie avant « réponse », chaque coche pointillée au bout d'un faisceau
de la tête, qui bat ; les 5 coches battent sur « fluide… » ; L5 tenue rouge x 1,3 jusqu'à « Exige » ; S12 : fils de
120 px, documents et puces qui battent ; S13 : conseiller x 1,1 à droite du bord de la page ; S14 : la coche pleine
repasse et absorbe la pointillée, celle de L5 part en grand arc, « corrige » fini avant « décide », fil plein de la
question au-dessus du conseiller, tampon à horloge 9 h, il s'écarte aussitôt du tampon.
Raccord : à l'image 1238 l'état est ENTRY_P3.
"""
import math

from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, line_crack_point
from pipeline.story_kit import REACH, REACH_STAMP, TAP, frames, lerp

from . import (ADV_REST, ADV_S12, ADV_S13, ADV_S13_SCALE, ADV_S14_SCALE, BADGE, BRICK_H, BRICKS, BUBBLE_AT, BUBBLE_BIG,
               CASE_W, CASE_X, CLIENT_S13, CLOUD_H, CLOUD_W, ENTRY_P2, FRAME_H, IA_CORNER, IA_CORNER_SCALE, IA_PILL_CORNER, IA_PILL_RIGHT,
               IA_S10, IA_S11, IA_S11_SCALE, PAGE_S10, PAGE_S10_SCALE, PAGE_S11, PAGE_S11_SCALE, PAGE_S12,
               PAGE_S12_SCALE, PAGE_S14, PAGE_S14_SCALE, PILE_S10, PILE_S10_SCALE, PILE_SLOT, PILL_ICON, SEAL_K,
               SEAL_W, TITLE_H, WIN_S08_POS, WIN_S08_SCALE, WIN_S10, fan_pt, scene_f0, seal_mini_at, vanish)

# ---------- places propres à p2 ----------
# S09 : le cadenas tombe sur le mur droit, au-dessus des briques ; il y reste accroché (x 2,4) jusqu'au badge (S11)
LOCK_FALL_K, LOCK_K = 3.0, 2.4
LOCK_DX_OPEN = 42 + SEAL_W                 # lockDx : du cadenas de la barre au mur droit (sceau ouvert)
LOCK_DX_SHUT = 42 + 46 * SEAL_K            # ... sceau refermé (badge, S11)
LOCK_DY = 128.5                            # sous la barre : y ≈ 660 en S09 (au-dessus de « Politique interne »)
LOCK_DY_BADGE = 58                         # S11 : au milieu du bord droit du badge
# S10 : fenêtre élargie x 80-770, y 405-1165 ; la page, née dans la main du conseiller, se pose en x 585
WIN10 = dict(pos=tuple(WIN_S10["pos"]), w=WIN_S10["w"], h=WIN_S10["h"])
PAGE10 = (585, PAGE_S10[1])
TITLE_S10 = (WIN10["pos"][0] - 60, WIN10["pos"][1] - WIN10["h"] / 2 + TITLE_H / 2)   # titre, à gauche du sceau
PAGE_HAND_SCALE = 0.25                     # S10 « demande » : la page dans sa main
PILE_AIM = [-235, -45]                     # S10 : bout du faisceau de lecture, bas de l'éventail (repère de la fenêtre)
BADGE_AIM = [-80, 85]                      # S11 : le même faisceau sur le bas du badge (ancre déclarée)
HOVER_X = 400                              # S10 : colonne des puces sorties de l'éventail, entre lui et la page
PUCE5_AT, PUCE5_SCALE = (560, 1050), 2.6   # S10 : la puce vide (115 px), à droite de la tête de l'IA, sous la page,
#                                            à 200 px de la pile (tour 4 : lisible au téléphone)
BADGE_DOC_SCALE = 0.45                     # documents compacts rangés dans le badge (S11-S12)
IA_PILL_ABOVE = [0, -150]                  # S11 : pilule « IA » au-dessus de la tête (repère de l'IA)
PAGE12_EXIGE = (480, PAGE_S12[1])          # S12 « Exige » : premier glissement, sans couvrir l'IA
VIA_DX = 48                                # S11 : le faisceau descend la marge gauche, 48 px à gauche des puces
WRITE11 = 7.0                              # S11 : caractères par image (L1-L4 et leurs coches finies avant « réponse »)
PUB_PILL_W = (790, 980)                    # S09 : « IA grand public » sous la tête, à 48 px sous les briques (monde)
ADV_S12_Y = 780                            # S12 : épaule à mi-hauteur de la colonne des cases
ADV_S14_Y = (668, 1000)                    # S14 : relecture de L1-L3 (haut), puis L3-L5 et la rature (bas), x 1,1
ADV_S14_X = 740                            # S14 : à droite de la fiche agrandie, entre elle et le client
ADV_END = [716, 1075]                      # fin de S14 (x 1) : entre la fiche (ombre à 646) et le client (815)
CORRIDOR_Y = 385                           # S12 : couloir des documents entre la légende du repère et le haut de la page
DOC_ANCHOR = [-71, -22]                    # bout du fil sur le document
STICKER_PX = 96                            # autocollant « ? » de 96 px à l'écran (revue 3)
STAMP_AT, STAMP_ROT = [0, 300], -4         # tampon : en bas de la page, sous « à poser au RDV » (440 px)
HANG = (730, 1070)                         # S13 : le fil de L5 retombe dans le vide, sous la case 5


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
    return out


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
    toi, client, sheet = c.toi, c.client, c.sheet
    rows, X, ty, ly = sheet.rows, sheet.x, sheet.ty, sheet.ly
    p5 = sheet.lines[4][1]                                  # paramètres de L5 (fente, valeur mesurée)
    f0 = scene_f0(S, "S09")                                 # 610

    kit.pin(f0 - 1, ENTRY_P2)                               # etat_initial de S09
    if S.val("toi", "scale", f0 - 1) == 0:                  # partie construite seule : la figurine n'est pas entrée
        toi.enter(f0 - 10, at=list(ADV_REST))

    def spot_for(targets, y, x_hi, n, margin=0.985):
        """Place du conseiller (centre) à la hauteur y, la plus à droite (<= x_hi) d'où tous les `targets` (points
        monde) sont à portée confortable du stylo de 90 px (REACH x allonge, moins 1,5 %)."""
        R = margin * REACH * toi.reach_max(n)
        sc = S.world_scale("toi", n)
        for x in range(round(x_hi), round(x_hi) - 300, -1):
            A = [x + toi.shoulder[0] * sc, y + toi.shoulder[1] * sc]
            if all(math.dist(A, t) <= R for t in targets):
                return [x, y]
        raise SystemExit(f"p2 : aucune place à y {y} pour {len(targets)} cibles")

    # Mise en place de S12-S14, entités encore invisibles (clés directes : rien ne saute à l'écran).
    def row_c(i):                                            # centre monde de la rangée i, page en PAGE_S12
        return round(PAGE_S12[1] + rows[i] * PAGE_S12_SCALE, 2)

    def text_y(i):                                           # ligne de texte monde de la rangée i (PAGE_S12)
        return round(PAGE_S12[1] + (rows[i] + ty) * PAGE_S12_SCALE, 2)

    for i in range(5):
        S.key(f"case{i + 1}", "pos", f0 - 1, [CASE_X, row_c(i)])
    for i in range(4):
        kit.ensure(f"fil{i + 1}", "bAt", list(DOC_ANCHOR))
        S.key(f"fil{i + 1}", "aAt", f0 - 1, [X["value"] + 10, rows[i] + ty])   # au bout de la valeur
    kit.ensure("fil5", "aAt", [X["value"] + 10, rows[4] + ty])
    S.key("fil5", "pb", f0 - 1, [CASE_X - CASE_W / 2 + 2, text_y(4)])
    S.key("tampon", "pos", f0 - 1, list(STAMP_AT))
    S.key("tampon", "rot", f0 - 1, STAMP_ROT)
    S.key("autocollant", "scale", f0 - 1, round(STICKER_PX / 72 / PAGE_S14_SCALE, 4))
    kit.ensure("faisceau_lit", "bAt", list(BADGE_AIM))
    for i in range(4):                                       # tour 4 : fils de preuve de 6 px
        S.ents[f"fil{i + 1}"]["p"]["sw"] = 6

    # =================== S09 « Le RGPD et ta politique interne s’appliquent. » ===================
    win_top = WIN_S08_POS[1] - FRAME_H / 2 * WIN_S08_SCALE
    bar_bottom = win_top + TITLE_H * WIN_S08_SCALE + 3      # les briques partent sous la barre de titre
    brick_kids = [("brique1_txt", "brique1_ico", "brique1_cad"), ("brique2_txt", "brique2_ico", "brique2_toi")]

    def brick_drop(k, f):
        """La brique k tombe de sous la barre de titre DANS son contour tireté (posé en S08 « non »), qui s'efface
        sous elle ; son pictogramme et son texte sont écrits dès qu'elle paraît. Renvoie l'image d'arrivée."""
        b = f"brique{k + 1}"
        x, y = BRICKS[k][1]
        h = round(y - BRICK_H / 2 - bar_bottom)
        S.key(b, "pos", f - 1, [x, y - h])
        S.key(b, "scale", f, 1)                              # visible SUR le mot, pas une image avant
        S.key(b, "pos", f, [x, y], DROP, "out")
        for ch in brick_kids[k]:
            S.key(ch, "opacity", f, 1)
        S.key(f"{b}_vide", "opacity", f + DROP - 3, 0, 4, "linear")   # le contour s'efface sous la brique
        S.key(f"{b}_vide", "scale", f + DROP + 2, 0)
        return f + DROP

    f = kit.at("S09", "RGPD", "une brique encre (bouclier-cadenas de 76 px, « RGPD ») tombe DANS le contour tireté du "
               "mur, sur la marque du choc ; le contour s'efface sous elle ; au contact, l'IA grand public recule")
    land = brick_drop(0, f)
    S.key("impact2", "scale", land - 2, 0)                   # la marque du choc est sous la brique
    p_pub = S.val("ia_pub", "pos", land - 1)
    k_pub = 0.85
    pub2 = _r([p_pub[0] + 18, p_pub[1] - 10])
    S.key("ia_pub", "pos", land, pub2, 6, "out")             # recul : elle s'écarte et rapetisse (x <= 940)
    S.key("ia_pub", "scale", land, k_pub, 6, "out")
    # sa pilule reste à sa place et à 32 px (contre-clés) : sous la tête, à 48 px sous les briques
    S.key("ia_pub_pill", "pos", land, _r([(PUB_PILL_W[0] - pub2[0]) / k_pub, (PUB_PILL_W[1] - pub2[1]) / k_pub]), 6,
          "out")
    S.key("ia_pub_pill", "scale", land, round(1 / k_pub, 4), 6, "out")

    f = kit.at("S09", "politique", "une 2e brique (le bâtiment du sceau « ✓ Cabinet » avec sa mini-figurine, « Politique "
               "interne ») tombe dans le 2e contour et se pose sur la première, ferme, sans rebond")
    brick_drop(1, f)

    f = kit.at("S09", "s’appliquent.", "un grand cadenas tombe sur le mur droit, au-dessus des briques, et son anse se "
               "ferme ; alors seulement, l'IA grand public et sa foule se réduisent en point, sa pilule s'efface ; le "
               "cadenas reste accroché au mur")
    S.key("outil", "lockDx", f - 1, LOCK_DX_OPEN)
    S.key("outil", "lockK", f - 1, LOCK_FALL_K)
    S.key("outil", "lockDy", f - 1, LOCK_DY - 200)
    S.key("outil", "lockOn", f, 1)
    S.key("outil", "lockDy", f, LOCK_DY, 6, "out")           # posé sur le mur, sans rebond
    S.key("outil", "lock", f + 6, 1, 4, "out")                # l'anse se ferme (150 ms)
    shut = f + 10
    kit.fade("ia_pub_pill", shut, 0, d=4)                    # la pilule s'efface (elle ne rétrécit pas)
    vanish(kit, "ia_pub", shut)                              # le cadenas fermé la fait disparaître
    S.key("outil", "lockK", shut + 2, LOCK_K, 8, "inOut")     # il reste accroché au mur, x 2,4

    # =================== S10 « Ensuite, demande un brief structuré d’une page. » ===================
    f = kit.at("S10", "Ensuite,", "chaque brique s'écrase dans le mur en 6 images, son texte et son corps s'effaçant "
               "ensemble ; la fenêtre verrouillée s'élargit, le cadenas suit le mur ; l'éventail en haut à gauche, l'IA "
               "en bas à gauche ; le conseiller regagne son coin")
    d = 12
    S.keys("outil", f, d, "inOut", pos=list(WIN10["pos"]), w=WIN10["w"], h=WIN10["h"], scale=1)
    S.key("sceau_mini", "pos", f, seal_mini_at(WIN10["w"], WIN10["h"], 1), d, "inOut")   # suit le sceau ouvert
    for k, b in enumerate(("brique1", "brique2")):
        for ch in brick_kids[k]:
            S.key(ch, "opacity", f, 0, 3, "linear")
        x_b, y_b = S.val(b, "pos", f - 1)
        kit.ensure(b, "sx", 1)
        S.key(b, "sx", f, 0.06, 6, "out")                    # écrasée vite (sx < 0,3 dès f + 2)
        S.key(b, "opacity", f, 0, 6, "in")                   # le corps s'efface avec son texte
        S.key(b, "pos", f, [round(x_b + 8, 2), y_b], 6, "out")
        S.key(b, "scale", f + 6, 0)
    for i in range(4):
        S.keys(f"doc{i + 1}", f, d, "inOut", pos=fan_pt(PILE_S10, PILE_SLOT[i], PILE_S10_SCALE), scale=PILE_S10_SCALE)
    S.keys("ia", f, d, "inOut", pos=list(IA_S10), scale=1)
    S.keys("ia_pill", f, d, "inOut", pos=list(IA_PILL_RIGHT), scale=1)
    S.keys("pastille", f, d, "inOut", pos=list(TITLE_S10), scale=1)
    toi.walk(f, list(ADV_REST), d=d)

    f = kit.at("S10", "demande", "le conseiller tend le bras vers la fenêtre : une page vide naît dans sa main, ses 5 "
               "onglets paraissent un à un, puis elle vole se poser dans la fenêtre ; le repère passe au « 2 · Exiger »")
    if S.val("toi", "scale", f - 1) == 0:                   # partie seule
        toi.enter(f, at=list(ADV_REST))
    kit.step(f, 1)
    toi.rim(f, True)
    hand = [ADV_REST[0] - 95, ADV_REST[1] - 120]             # bras tendu vers la fenêtre
    toi.reach(f, hand, d=4, step=False)
    born = f + 2
    tip = toi.tip(born + 1)
    page_hand = [round(tip[0] - 40, 2), round(tip[1] - 70, 2)]
    S.key("fiche", "pos", born - 1, page_hand)
    S.key("fiche", "lite", born - 1, 1)                      # tour 4 : petite, son titre est une barre (pas 18 px)
    for i in range(5):
        S.key("fiche", f"tab{i}", born - 1, 0)
        S.key("fiche", f"tab{i}", born + 1 + i, 1)           # les 5 onglets vides, un par image
    kit.pop("fiche", born, scale=PAGE_HAND_SCALE, d=3)
    g = born + 6
    S.fly("fiche", g, 7, "inOut", to=list(PAGE10), scale=PAGE_S10_SCALE, arc=60)
    toi.rim(g - 2, False, d=2)                               # avant que le bras ne se replie (pas de boucle)
    toi.rest(g, 8)

    def tab_w(i, n):                                         # onglet (= puce) de la rangée i, en monde
        return S.to_world("fiche", [X["bullet"], rows[i] + ty], n)

    f = kit.at("S10", "brief", "le faisceau pointillé de l'IA passe sur l'éventail ; de chaque document sort une pastille "
               "pleine (€, barres, sablier, bouclier) qui se range en face de son onglet")
    S.key("faisceau_lit", "bAt", f - 1, list(PILE_AIM))
    kit.draw("faisceau_lit", f, 6)
    for i in range(4):
        hover = [HOVER_X, round(tab_w(i, f)[1], 2)]
        kit.pop(f"puce{i + 1}", f + 2 * i, from_pt=fan_pt(PILE_S10, PILE_SLOT[i], PILE_S10_SCALE), to=hover)

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

    f = kit.at("S10", "d’une", "seule, la tête de l'IA lance un grand éclat (12 rayons) ; 3 bulles de pensée pointillées "
               "partent de sa tête ; une 5e puce, vide et pointillée, grande (115 px), en sort et se pose à sa droite, "
               "loin de la pile : tout est en place en 5 images")
    S.key("ia_eclat2", "p", f - 1, 0)
    S.key("ia_eclat2", "p", f, 1, 6, "linear")
    head = S.to_world("ia", c.brain_front, f - 1)
    # contrôle sans son : la puce vide naît dans un NUAGE DE PENSÉE (signe universel de « ça sort de sa tête »), au
    # bout des 3 bulles qui montent de son front ; le nuage (230 x 166) tient sous la page, dans la fenêtre
    cloud_k = 0.92
    S.key("nuage", "pos", f - 1, _r(PUCE5_AT))
    S.key("nuage", "rot", f - 1, 0)
    edge = [PUCE5_AT[0] - 0.42 * CLOUD_W * cloud_k, PUCE5_AT[1] - 0.3 * CLOUD_H * cloud_k]   # haut gauche du nuage
    brow = [IA_S10[0] + 112, IA_S10[1] - 75]                 # juste devant le front de verre (pas sur le visage)
    for k in range(3):                                       # les bulles passent au-dessus de la pilule « IA »
        t = 0.15 + 0.35 * k
        at = [lerp(brow[0], edge[0], t), lerp(brow[1], edge[1], t) - 30 * math.sin(math.pi * t)]
        S.key(f"pensee{k + 1}", "pos", f - 1, _r(at))
        kit.pop(f"pensee{k + 1}", f + k, scale=1.7, d=3)
    kit.pop("nuage", f + 1, scale=cloud_k, d=4)
    kit.pop("puce5", f + 1, scale=PUCE5_SCALE, from_pt=head, to=list(PUCE5_AT), d=4)   # immobile dès 768 (« page. »)

    beat = kit.hold("S10", "page.", "tenue : la grande puce vide reste seule, immobile, dans le nuage de pensée de l'IA "
                    "(0,4 s), puis tombe sur l'onglet 5 en laissant un fil pointillé gris tête -> onglet 5 ; le nuage "
                    "et ses bulles se dégonflent")
    g = beat + 12                                            # immobile de 768 à 779
    tab5 = tab_w(4, g + 7)
    S.fly("puce5", g, 7, "inOut", to=tab_w(4, g), scale=PAGE_S10_SCALE, arc=40)
    S.key("faisceau_tete", "pb", g - 1, _r(tab5))          # sa traînée : la ligne 5 vient de la tête de l'IA
    S.key("faisceau_tete", "via", g - 1, [])
    kit.draw("faisceau_tete", g, 7, e="inOut")
    vanish(kit, "nuage", g + 1, d=6)
    for k in range(3):
        vanish(kit, f"pensee{k + 1}", g + k, d=5)
    arr = g + 7
    S.key("puce5", "opacity", arr, 0)
    S.key("fiche", "tab4", arr, 0)
    S.key("L5", "bulletOn", arr, 1)

    # =================== S11 « Mais une IA peut produire une réponse fluide… et fausse. » ===================
    f = kit.at("S11", "Mais", "la fenêtre se réduit en badge en haut à gauche avec ses documents, le cadenas sur son bord "
               "droit ; la page vient au centre en grandissant (x 1,12), son titre « Brief » paraît ; la pastille se "
               "pose sur son en-tête ; l'IA reste en bas à gauche, pilule au-dessus de la tête ; la traînée rentre")
    S.key("faisceau_tete", "from", f, 1, 4, "in")
    S.key("faisceau_tete", "draw", f + 4, 0)
    S.key("faisceau_tete", "from", f + 4, 0)
    S.keys("outil", f, MORPH, "out", pos=list(BADGE["pos"]), w=BADGE["w"], h=BADGE["h"], scale=BADGE["scale"], seal=0,
           lockDx=round(LOCK_DX_SHUT, 2), lockDy=LOCK_DY_BADGE)
    S.key("sceau_mini", "pos", f, seal_mini_at(BADGE["w"], BADGE["h"], 0), MORPH, "out")
    for i in range(4):
        sl = PILE_SLOT[i]
        bp = [BADGE["pos"][0] - 6 + 4 * sl, BADGE["pos"][1] + 10 + 4 * sl]
        S.keys(f"doc{i + 1}", f, MORPH, "out", pos=bp, scale=BADGE_DOC_SCALE, compact=1, txt=0)
    S.keys("ia", f, MORPH, "out", pos=list(IA_S11), scale=IA_S11_SCALE)
    S.keys("ia_pill", f, MORPH, "out", pos=list(IA_PILL_ABOVE), scale=round(1 / IA_S11_SCALE, 4))
    S.keys("fiche", f, MORPH, "out", pos=list(PAGE_S11), scale=PAGE_S11_SCALE)
    S.key("fiche", "lite", f + 4, 0, 6, "inOut")
    head_w = S.to_world("fiche", c.header_pill, f + MORPH)
    S.fly("pastille", f, MOVE, "inOut", to=_r(head_w), scale=PAGE_S11_SCALE, arc=40)
    S.key("pastille", "opacity", f + MOVE, 0)
    S.key("pastille_fiche", "opacity", f + MOVE, 1)

    f = kit.at("S11", "IA", "un faisceau pointillé relie la tête de l'IA au badge des documents")
    S.key("faisceau_lit", "bAt", f - 1, list(BADGE_AIM))
    kit.draw("faisceau_lit", f, 8)

    sc11 = PAGE_S11_SCALE
    via_x = PAGE_S11[0] + X["bullet"] * sc11 - VIA_DX
    ia_peak = round(IA_S11_SCALE * 1.05, 4)

    def row_y11(i):
        return PAGE_S11[1] + (rows[i] + ty) * sc11

    def plug(i):
        return [round(via_x + 24, 2), round(row_y11(i), 2)]

    def tick11(i):
        return S.to_world("fiche", sheet.pt(i, "tick"), f)

    def tick_beam(i, g):
        """Un court faisceau pointillé part de la TÊTE de l'IA (2 images) et, à son bout, la coche pointillée de la
        ligne i se trace dans son carré (4 images) pendant que la tête bat une fois : c'est elle qui coche ; puis le
        faisceau rentre. Renvoie l'image qui suit la coche."""
        w = f"faisceau_coche{i + 1}"
        S.key(w, "pb", g - 1, _r(tick11(i)))
        kit.draw(w, g, 2)
        kit.draw(f"coche_ia{i + 1}", g + 1, 4)               # au bout du faisceau
        kit.pulse("ia", g + 1, peak=ia_peak, step=2)         # la tête bat d'un coup
        S.key(w, "from", g + 4, 1, 3, "in")                  # il rentre dans la tête
        S.key(w, "draw", g + 7, 0)
        S.key(w, "from", g + 7, 0)
        return g + 5

    f = kit.at("S11", "produire", "pour L1 à L4, en cascade : la carte source s'allume dans le badge et son pictogramme "
               "glisse le long du faisceau jusqu'à la puce ; la ligne s'écrit ; puis un court faisceau pointillé part de "
               "la TÊTE de l'IA, sa coche pointillée se trace au bout et la tête bat : fini avant « réponse »")
    for i in range(4):
        lid, did, cid = f"L{i + 1}", f"doc{i + 1}", f"copie{i + 1}"
        dep = f + 2 * i                                      # la copie part (la 1re sur le mot)
        g = dep + 4                                          # elle arrive à la puce
        src = S.to_world(did, [0, 0], dep - 1)
        route = [src, [via_x, src[1] + 40], [via_x, row_y11(i)], plug(i)]
        S.key(did, "lit", dep, 1, 2, "out")                  # la source s'allume dans le badge
        kit.pulse(did, dep, peak=round(S.val(did, "scale", dep - 1) * 1.25, 4), step=2)
        S.key(cid, "pos", dep - 1, _r(src))
        S.key(cid, "scale", dep - 1, 0)
        S.key(cid, "scale", dep, 1, 2, "out")
        for m, q in frames(dep, 4, "inOut"):
            S.key(cid, "pos", m, _r(_poly(route, q)), 1, "linear")
        S.key(cid, "scale", g, 0)
        S.key(cid, "opacity", g, 0)
        S.key("faisceau", "pb", dep, plug(i))                # le faisceau du badge vise la puce de la ligne
        S.key("faisceau", "via", dep, [round(via_x, 2), round(row_y11(i), 2)])
        if i == 0:
            kit.draw("faisceau", dep, 2)                     # sur le mot, pas avant
        end = kit.type(lid, g, rate=WRITE11, flash=True)
        tick_beam(i, end)

    f = kit.at("S11", "réponse", "le badge reste éteint et son faisceau se retire : la tête de l'IA lance un grand éclat "
               "(12 rayons) et un faisceau part de sa tête vers la puce de L5, qui reste VIDE pendant que « Horizon : 5 "
               "ans » s'écrit ; puis la coche pointillée se trace au bout d'un faisceau de la tête, qui bat")
    S.key("faisceau", "draw", f, 0, 3, "in")
    S.key("faisceau_lit", "draw", f, 0, 3, "in")
    S.key("ia_eclat2", "p", f - 1, 0)
    S.key("ia_eclat2", "p", f, 1, POP, "linear")
    S.key("faisceau_tete", "pb", f - 1, plug(4))
    S.key("faisceau_tete", "via", f - 1, [round(via_x, 2), round(row_y11(4), 2)])
    kit.draw("faisceau_tete", f + 1, 4)
    # contrôle sans son : la valeur de L5 SORT DE SA TÊTE, visiblement. 3 bulles montent au-dessus de sa pilule vers
    # un nuage de pensée (165 x 119, à gauche de la page, entre les puces de L3 et L4) qui porte « 5 ans » ; L5
    # écrit d'abord sa clé seule, puis « 5 ans » sort du nuage et vole se poser au bout de la ligne (aucun document
    # n'a bougé) ; ensuite seulement, la coche pointillée de l'IA
    cloud11, ck11 = (118, 842), 0.62
    S.key("nuage", "pos", f - 1, list(cloud11))
    for k, pt in enumerate(((168, 974), (174, 944), (162, 912))):
        S.key(f"pensee{k + 1}", "pos", f - 1, list(pt))
        kit.pop(f"pensee{k + 1}", f + 1 + k, scale=1.4, d=3)
    kit.pop("nuage", f + 2, scale=ck11, d=5)
    S.key("nuage_val", "pos", f + 2, [cloud11[0], cloud11[1] + 2])
    S.key("nuage_val", "scale", f + 3, 1.4)
    kit.fade("nuage_val", f + 3, 1, d=4, frm=0)
    kit.type("L5", f + 4, n=len(sheet.lines[4][1]["key"]), rate=5)    # « Horizon » seul ; la valeur vient du nuage
    a5, b5 = sheet.value_span(4)
    g = f + 14                                                # « 5 ans » tenu 10 images dans le nuage
    val_w = S.to_world("fiche", [(a5[0] + b5[0]) / 2, a5[1]], g)
    S.fly("nuage_val", g, 8, "inOut", to=_r(val_w), scale=PAGE_S11_SCALE, arc=50)
    arr = g + 8
    S.key("L5", "chars", arr, len(sheet.lines[4][1]["key"]) + len(sheet.lines[4][1]["value"]))
    S.key("nuage_val", "opacity", arr, 0)                    # relais : la valeur de la ligne prend sa place
    S.key("nuage_val", "scale", arr + 1, 0)
    end = tick_beam(4, arr + 1)
    vanish(kit, "nuage", arr + 8, d=6)                        # le nuage se dégonfle avant la tenue de « et »
    for k in range(3):
        vanish(kit, f"pensee{k + 1}", arr + 8 + k, d=5)

    f = kit.at("S11", "fluide…", "les coches pointillées de L1-L4 battent l'une après l'autre (elle a tout coché "
               "elle-même), puis celle de L5 dès qu'elle est tracée ; un reflet traverse la page complète sous les "
               "textes ; le faisceau de la tête reste sur la puce vide de L5 ; puis immobilité")
    kit.stagger([f"coche_ia{k + 1}" for k in range(4)], f, 2, lambda i, n: kit.pulse(i, n, peak=1.2, step=2))
    kit.pulse("coche_ia5", end + 1, peak=1.2, step=2)
    S.key("reflet", "p", end + 1, 1, 12, "linear")

    kit.hold("S11", "et", "tenue : rien ne bouge, la fiche entièrement cochée par l'IA")

    f = kit.at("S11", "fausse.", "la puce vide de L5, toujours reliée à la tête de l'IA, bat deux fois (x 1,3), deux "
               "ondes rouges courtes en partent ; elle reste à x 1,3, cerclée d'un anneau rouge, jusqu'à « Exige » ; "
               "le texte reste à l'encre")
    S.key("L5", "bulletOn", f, 0)                            # relais : la même puce, enfant de la fiche, au-dessus
    S.key("puce5_alerte", "opacity", f, 1)
    S.key("puce5_alerte", "alarm", f, 1, 3, "out")
    for k in range(2):
        g = f + 6 * k
        S.key("puce5_alerte", "scale", g, 1.3, 3, "out")      # x 1,3 : l'alerte ne couvre pas « Horizon »
        S.key("puce5_alerte", "scale", g + 3, 1.15, 3, "inOut")
        o = f"onde{k + 1}"
        S.key(o, "scale", g, 1)
        S.key(o, "scale", g + 1, 1.5, 8, "out")             # tour 4 : 66 px au plus, à 9 px de « Horizon »
        S.key(o, "opacity", g + 1, 0, 8, "in")
        S.key(o, "scale", g + 9, 0)
    S.key("puce5_alerte", "scale", f + 12, 1.3, 3, "out")    # tenue à x 1,3 (0,6 s de plus)
    kit.pop("anneau5", f + 12, scale=1.3, d=3)               # la puce reste cerclée de rouge plein

    # =================== S12 « Exige que chaque ligne renvoie à un document et à une date. » ===================
    f = kit.at("S12", "Exige", "le conseiller prend la main : il monte à droite de la page, stylo levé ; la page glisse "
               "à gauche et se réduit pour lui faire place ; les 5 coches de l'IA restent ; la puce rouge de L5 "
               "reprend sa taille")
    S.key("faisceau_tete", "draw", f, 0, 4, "in")           # le faisceau de la tête rentre : l'humain prend la main
    S.key("puce5_alerte", "scale", f, 1.15, 4, "inOut")
    S.key("anneau5", "scale", f, 1.15, 4, "inOut")
    cases = [[CASE_X, row_c(i)] for i in range(5)]
    adv12 = spot_for(cases, ADV_S12_Y, ADV_S12[0], f - 1)
    toi.walk(f, adv12, d=12)
    S.keys("fiche", f, 10, "inOut", pos=list(PAGE12_EXIGE), scale=PAGE_S12_SCALE)   # 330 ms (tour 4)

    f = kit.at("S12", "chaque", "l'IA se range, plus petite, dans le coin en bas à gauche, à côté de la page, toujours "
               "visible, sa pilule « IA » à droite de la tête ; la page finit de glisser à gauche")
    S.keys("ia", f, 10, "out", pos=list(IA_CORNER), scale=IA_CORNER_SCALE)
    S.keys("ia_pill", f, 10, "out", pos=list(IA_PILL_CORNER), scale=round(1 / IA_CORNER_SCALE, 4))
    S.keys("fiche", f, 10, "inOut", pos=list(PAGE_S12))

    f = kit.at("S12", "ligne", "le stylo descend la colonne et trace, en face de chaque ligne, une case-source vide en "
               "tirets")
    hits = toi.trace(f, cases, d=6, lead=3)
    for i, h in enumerate(hits):
        kit.draw(f"case{i + 1}", h - 1, 2)
    toi.walk(hits[-1] + 1, [min(adv12[0] + 24, 940 - 59 - 4), adv12[1]], d=8)   # recule d'un pas (x <= 877 : jamais
    #                                                                             dans la colonne réservée x > 940)

    f = kit.at("S12", "renvoie", "les 4 documents sortent du badge, passent au-dessus de la page et se logent dans les "
               "cases 1 à 4 ; le badge vidé se replie ; la case 5 reste vide")
    for i in range(4):
        d_id, g = f"doc{i + 1}", f + 3 * i
        p0 = S.to_world(d_id, [0, 0], g - 1)
        s0 = S.world_scale(d_id, g - 1)
        p1, p2, p3 = [p0[0] + 220, CORRIDOR_Y], [CASE_X + 80, CORRIDOR_Y], cases[i]
        S.key(d_id, "z", g, 12.5 + 0.1 * i)
        S.path(d_id, g, 13, "inOut", lambda p, p0=p0, p1=p1, p2=p2, p3=p3: _cubic(p0, p1, p2, p3, p),
               lambda p, s0=s0: s0 + (PAGE_S12_SCALE - s0) * p * p)
    vanish(kit, "outil", f + 3 * 3 + 3)

    f = kit.at("S12", "document", "un fil cyan profond plein (6 px) part de chaque valeur L1-L4 et se tend, sur 120 px "
               "hors de la page, jusqu'à son document, qui bat à l'arrivée du fil ; la puce de la ligne bat aussi")
    for i in range(4):
        g = kit.draw(f"fil{i + 1}", f + 3 * i, DRAW)
        d_id = f"doc{i + 1}"
        kit.pulse(d_id, g, peak=round(S.val(d_id, "scale", g - 1) * 1.12, 4), step=2)
        S.key(f"L{i + 1}", "flash", g, 1, 2, "out")
        S.key(f"L{i + 1}", "flash", g + 2, 0, 3, "inOut")

    f = kit.at("S12", "date.", "de chaque document sort sa date écrite en clair sur une petite page cornée ; elle "
               "glisse le long du fil et se pose sous sa valeur")
    for i in range(4):
        src, fil, g = f"source{i + 1}", f"fil{i + 1}", f + 2 * i
        cub = S.wire_cubic(fil, g)
        a_x, b_x = cub[0][0], cub[3][0]
        a_y, b_y = cub[0][1], cub[3][1]
        doc = S.to_world(f"doc{i + 1}", [0, 0], g)
        tgt = S.to_world("fiche", [c.tag_cx, rows[i] + ly], g)
        o0, o1 = [doc[0] - b_x, doc[1] - b_y], [tgt[0] - a_x, tgt[1] - a_y]
        S.along_wire(src, fil, g, 12, "inOut", 1.0, 0.0, at_frame=g,
                     offset=lambda p, o0=o0, o1=o1: (o0[0] + (o1[0] - o0[0]) * p, o0[1] + (o1[1] - o0[1]) * p))
        kit.pop(src, g, d=6)

    # =================== S13 « Une info sans source, c’est une question à poser au client. » ===================
    f = kit.at("S13", "Une", "chaque document remonte son fil et se réduit dans son étiquette-source, en passant sous elle ; "
               "les fils rentrent ; les cases 1-4 s'effacent, la case 5 reste vide ; le conseiller redescend à droite de "
               "la page (x 1,1), seul son bras pourra y entrer")
    dur = MORPH
    for i in range(4):
        d_id, src, fil = f"doc{i + 1}", f"source{i + 1}", f"fil{i + 1}"
        a = S.to_world(d_id, [0, 0], f - 1)
        b = S.to_world(src, [-S.ents[src]["p"]["tag"]["w"] / 2 + 24, 0], f - 1)   # droit sur la pastille
        S.key(d_id, "z", f, 12.5 + 0.01 * i)                # sous l'étiquette qu'il rejoint : la date reste lisible
        S.path(d_id, f, dur, "inOut", lambda p, a=a, b=b: lerp(a, b, p))
        S.key(d_id, "tag", f, 1, dur, "inOut")
        S.key(fil, "from", f, 1, 5, "linear")
        S.key(fil, "opacity", f + 5, 0)
        arr = f + dur
        S.key(d_id, "opacity", arr, 0)
        S.key(src, "flash", arr, 1, 2, "out")
        S.key(src, "flash", arr + 2, 0, 3, "inOut")
        S.key(f"case{i + 1}", "draw", f, 0, dur, "in")
    toi.scale_to(f, ADV_S13_SCALE, d=12)
    # le long du bord droit, à droite de la case 5 ; x 1,1 : jamais au-delà de x 940 (zone réservée)
    down = [min(S.val("toi", "pos", f - 1)[0], 940 - 59 * ADV_S13_SCALE - 4), ADV_S13[1] - 90]
    g = toi.walk(f, down, d=6, e="inOutSine")
    toi.walk(g, list(ADV_S13), d=6, e="inOutSine")           # fini avant « sans »

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
    kit.draw("fil5", f, 3)
    touch = f + 2
    kit.shake("case5", touch + 1, amp=6)
    S.key("fil5", "pb", touch + 2, list(HANG), 3, "inOutSine")   # retombé avant « source, »
    S.key("fil5", "sag", touch + 2, 20, 3, "inOutSine")

    kit.hold("S13", "source,", "tenue (0,8 s) : le fil pend dans le vide sous la case 5, la case reste un contour vide, la "
             "ligne Horizon en lumière ; rien ne bouge")

    f = kit.at("S13", "c’est", "le stylo du conseiller touche « 5 ans » : au contact, la ligne vire au rouge et se fend ; "
               "la coche pointillée de l'IA reste, l'IA ne bouge pas")
    hit = toi.tap(f - 4, S.to_world("L5", [X["value"] - 15, ty], f - 1), d=5)   # approche courte : la case tient
    S.key("L5", "red", hit, 1, 3, "out")
    S.key("L5", "crack", hit, 1, POP, "out")

    f = kit.at("S13", "question", "un grand « ? » naît sur la valeur fendue, sous la pointe, puis glisse prendre la place "
               "de la case 5, qui se replie avec le fil")
    v_pt = S.to_world("L5", line_crack_point(p5, [X["value"] - p5["valueW"] / 2, ty], 1.0), f - 1)
    S.key("question", "pos", f - 1, _r(v_pt))
    S.key("question", "scale", f - 1, 0)
    S.key("question", "scale", f, 1, 7, "out")
    S.key("question", "pos", f + 4, list(cases[4]), 9, "inOut")
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
    route = _catmull([icon_w, [icon_w[0] + 160, head_y], [600, head_y], [872, 560], [884, 900], list(CLIENT_S13)])
    client.size = 0.5
    client.enter(f, at=_r(icon_w), d=2)                     # né du pictogramme, x 0,5 (rig de la figurine)
    client.run(f + 2, [_r(p) for p in route[::3]] + [list(CLIENT_S13)], 16)
    client.scale_to(f + 14, 1.0, d=4, e="out")              # il grandit en arrivant sous la bulle
    arr = f + 18
    kit.ensure("bulle", "rot", 0)
    S.key("bulle", "rot", arr, 5, 3, "out")
    S.key("bulle", "rot", arr + 4, 0, 4, "inOut")

    # =================== S14 « Dernière étape : relis, corrige, décide. » ===================
    f = kit.at("S14", "Dernière", "le repère passe au « 3 · Relire » (un seul disque glisse) ; la fiche grandit pour la "
               "relecture ; le conseiller monte à droite de la page ; sa bulle se replie en autocollant « ? » de 96 px "
               "qui va attendre sur la rangée L5, entre « Horizon » et la valeur fendue ; le client reste")
    kit.step(f, 2)
    S.keys("fiche", f, 10, "inOut", pos=list(PAGE_S14), scale=PAGE_S14_SCALE)
    n_end = f + 10
    ticks = [S.to_world("fiche", sheet.pt(i, "tick"), n_end) for i in range(5)]
    crack_r = S.to_world("L5", line_crack_point(p5, [X["value"] + 8, ty], 1.0), n_end)
    crack_l = S.to_world("L5", line_crack_point(p5, [X["value"] - p5["valueW"] - 8, ty], 1.0), n_end)
    toi.scale_to(f, ADV_S14_SCALE, d=10)
    spot_a = spot_for(ticks[:3], ADV_S14_Y[0], ADV_S14_X, f + 10)          # relit L1-L3 d'ici
    spot_b = spot_for(ticks[2:] + [crack_r, crack_l], ADV_S14_Y[1], ADV_S14_X, f + 10)   # L3-L5 et la rature
    toi.walk(f, spot_a, d=10, e="inOutSine")
    park = S.to_world("fiche", S.val("autocollant", "pos", f), n_end)
    S.fly("bulle", f, 10, "inOut", to=park, scale=STICKER_PX / 72, arc=30)
    S.key("bulle", "s", f, 1, 6, "out")                     # se replie d'abord, puis glisse
    arr = f + 10
    S.key("bulle", "opacity", arr, 0)
    S.key("bulle", "scale", arr, 0)
    S.key("autocollant", "opacity", arr, 1)

    f = kit.at("S14", "étape :", "le stylo touche la coche pointillée de L1 : elle se soulève et bat (x 1,25), puis la "
               "coche pleine cyan profond se trace par-dessus et la pointillée disparaît DANS elle ; son étiquette-source "
               "s'allume ; puis L2, au même pas de 0,35 s")
    r_f = kit.at("S14", "relis,", "même geste sur L3 puis L4 : la coche pointillée bat, la coche pleine la repasse et "
                 "l'absorbe ; la pointe s'arrête sur la coche de L5 sans la repasser")
    c_f = kit.at("S14", "corrige,", "d'un geste, le stylo chasse la coche pointillée de L5 (elle part en grand arc hors du "
                 "bord de la page en tournant ; son carré reste vide) puis barre « 5 ans », qui tombe ; l'autocollant « ? » "
                 "glisse sur la valeur ; « à poser au RDV » paraît, la réplique « 9 h » de la pastille à sa gauche ; un "
                 "fil plein cyan profond relie le « ? » au client, par-dessus la tête du conseiller ; tout est posé avant "
                 "« décide. »")
    toi.walk(f + 11, spot_b, d=26)
    hits = toi.trace(f - 3, ticks, d=c_f - f - 1, lead=4, step=False)   # L1 sur « étape », L3 sur « relis », L5 à
    #                                                                     « corrige » - 1 ; le corps descend (walk)
    if hits[0] != f or hits[2] != r_f or hits[4] != c_f - 1:
        kit.warn(f"p2 S14 : relecture décalée des mots ({hits} ; étape {f}, relis {r_f}, corrige {c_f})")
    for i in range(4):
        kit.pulse(f"coche_ia{i + 1}", hits[i], peak=1.25, step=2)        # au contact, la coche de l'IA bat
        kit.draw(f"coche{i + 1}", hits[i] + 2, 6)                        # la coche pleine se trace par-dessus
        vanish(kit, f"coche_ia{i + 1}", hits[i] + 4, into=f"coche{i + 1}", d=5)   # et l'absorbe
        S.key(f"source{i + 1}", "lit", hits[i] + 2, 1, 4, "out")

    f = c_f
    # la coche de l'IA de L5, sans son carré, est chassée : grand arc hors du bord droit de la page, en tournant
    S.key("carre5", "opacity", f, 1)                         # le carré tireté reste, vide
    S.key("coche_ia5", "draw", f, 0)
    S.key("coche_ia5_vol", "opacity", f, 1)
    S.key("coche_ia5_vol", "z", f, 16)
    kit.ensure("coche_ia5_vol", "rot", 0)
    p_vol = S.val("coche_ia5_vol", "pos", f)
    out_w = S.to_world("fiche", [p_vol[0], p_vol[1]], f)
    # elle tombe en travers de la page (pointillés gris sur papier : lisible), sort par son bord bas et s'efface ;
    # jamais devant le buste encre du conseiller, où elle disparaîtrait
    out_to = S.to_local("fiche", [out_w[0] - 90, out_w[1] + 340], f)
    S.key("coche_ia5_vol", "pos", f, _r(out_to), 14, "in", arc=40)   # 450 ms, chute de 340 px
    S.key("coche_ia5_vol", "rot", f, 90, 14, "out")
    S.key("coche_ia5_vol", "opacity", f + 10, 0, 4, "linear")
    g = toi.strike(f, crack_r, crack_l, d=5, lead=2, line="L5")    # g ≈ 1198
    hold = g + 1
    S.key("L5", "fall", hold, 1, 7, "in")
    S.key("L5", "crack", g, 0, 8, "inOut")
    S.key("L5", "red", g, 0, 4, "out")
    S.key("puce5_alerte", "alarm", g, 0, 4, "out")
    S.key("puce5_alerte", "scale", g, 1, 4, "inOut")
    S.key("puce5_alerte", "opacity", g + 4, 0)
    vanish(kit, "anneau5", g, d=4)
    S.key("L5", "bulletOn", g + 4, 1)
    vanish(kit, "surligneur", g)
    S.keys("autocollant", g + 1, 4, "inOut", pos=[X["value"] - 46, rows[4] + ty - 10])   # « Horizon : ? »
    kit.pop("source5", g + 1, d=6)
    # « ce client, à 9 h » : la réplique de la pastille paraît sur place, devant « à poser au RDV »
    mini_at = [round(X["value"] - S.ents["source5"]["p"]["tag"]["w"] - 58, 1), rows[4] + ly + 6]
    S.key("pastille_mini", "pos", g + 1, mini_at)
    kit.pop("pastille_mini", g + 2, d=4)
    # la question est adressée au client : fil plein cyan profond du « ? » à sa tête, au-dessus du conseiller ; le
    # client reste immobile (sa réponse viendra au rendez-vous, S19)
    kit.draw("fil_q", g + 3, 5)

    # « décide. » : un pas vers le bas de la page, le coup de tampon, la page tremble ; il s'écarte aussitôt
    hit_f = kit.at("S14", "décide.", "le conseiller fait un pas et abat le tampon PRÊT POUR LE RDV (horloge 9 h à gauche) "
                   "en bas de la page, sous « à poser au RDV », sans couvrir le « ? » ni son fil ; la page tremble ; il "
                   "s'écarte aussitôt : le tampon se lit en entier, la ligne 5 garde son carré vide") + 5
    if g + 8 > hit_f - 5:
        kit.warn(f"p2 S14 : les suites de « corrige » ({g + 8}) mordent sur « décide. » ({hit_f - 5})")
    grip_l = [0, -(S.ents["tampon"]["p"]["h"] / 2 + 14 + 10)]
    rr = math.radians(STAMP_ROT)
    grip_f = [STAMP_AT[0] + grip_l[0] * math.cos(rr) - grip_l[1] * math.sin(rr),
              STAMP_AT[1] + grip_l[0] * math.sin(rr) + grip_l[1] * math.cos(rr)]
    grip_w = S.to_world("fiche", grip_f, hit_f - 6)
    hand_r = 0.94 * REACH_STAMP * toi.reach_max(hit_f - 6, pen=False)
    sc = S.world_scale("toi", hit_f - 6)
    st_spot = [round(grip_w[0] + hand_r - toi.shoulder[0] * sc, 1), round(grip_w[1] - toi.shoulder[1] * sc, 1)]
    w0 = max(g + 8, hit_f - 5 - 5)
    toi.walk(w0, st_spot, d=hit_f - 5 - w0)
    f = hit_f - 5
    hit = toi.stamp(f, "tampon", shake="fiche", step=False)
    S.key("tampon", "handle", hit + 1, 0, 2, "linear")      # la poignée part avec la main
    toi.scale_to(hit + 1, 1.0, d=5)                          # il s'écarte (x 1) : le tampon se lit dès hit + 4
    w1 = toi.walk(hit + 1, ADV_END, d=5, e="inOutSine")
    toi.rest(w1, 4)
