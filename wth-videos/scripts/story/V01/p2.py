"""V01, partie 2 : S08-S14, images 890-1935 (29,651 -> 64,539 s). 32 temps forts.

Entrée (épinglée à l'image 889 : kit.pin(889, ENTRY_P2), etat_initial de S08) : 4 sources à leurs places DOC_S07
(170, 610), (810, 600), (330, 1080), (750, 1080), bandeau et date visibles, info sur leur coin ; pastille (540, 865)
et rond vide dessous (540, 935) ; conseiller au sol (540, 1135) ; IA rangée (60, 1200) x 0,42 ; repère en haut
(disque 1 actif) ; barre2 vide (contour) sous le repère ; horloge-badge (830, 300).
Garde-fou figurine (partie isolée) : `if S.val("toi", "scale", 889) == 0: c.toi.enter(880, at=ADV_S07)`.
NB : le storyboard écrit la pastille en (540, 820) dans l'etat_initial de S08 ; c'est (540, 865) en S06-S07, gardé ici.

Sortie (image 1935) = ENTRY_P3 (etat_initial de S15) : page à gauche (PAGE_S13, x 0,95), titre « Brief · 1 page »
(fiche_titre2), pastille posée sur l'en-tête (relais pastille -> pastille_fiche, la pastille monde à 0) ; L1-L5
écrites et en rangées (grow 1), cochées par l'IA (coche_ia1-5 draw 1), puce de L5 cerclée de rouge (alarm 1) ;
case1-5 tracées en colonne x 730 ; doc1-4 en version compacte dans case1-4 ; fil1-4 tracés ; dates source1-4 (tagged
0) sous les valeurs ; case5 vide, fil5 non tracé ; badge (outil) replié à 0, cadre à 0 ; nuage, rond, info1-4 à 0
(relayés par les puces de la page) ; IA rangée (60, 1200) x 0,42 ; repère sur 2 ; conseiller en (870, 800)
(non épinglé).

Brief, scène par scène :
- S08 « Pourquoi » : le disque 1 bat deux fois ([chapitre] posé sur le disque actif, ou pulse) ; legende1 se souligne.
  « Parce » : [ia] regrandit en IA_S08 (x 0,75), pilule dessous. « gagner » : [faisceau1-4] partent ensemble vers les
  4 sources ; de doc2 (CRM) glissent [carte_grise1-2] (pilules « 14 h », « 16 h ») jusqu'à GREY_S08, à la hauteur de
  la pastille ; à leur arrivée, la pastille puis les deux pilules grises battent l'une après l'autre (décalées de
  4 images) ; +12 images : [faisceau5-6] filent vers elles. « protéger » : le conseiller bondit (place_for) stylo levé
  en travers des faisceau5-6 (pointe ≈ (700, 850)) : ils cassent net sur la pointe ([impact_stylo]), puis tous les
  faisceaux se rétractent (from 0 -> 1). Pas de rouge, pas de traits de vitesse : l'IA n'est pas une voleuse.
  « client » : doc1-4 glissent en 2 x 2 (DOC_GRID_S08, x 0,85), la pastille en PASTILLE_S08, le rond en ROND_S08 ;
  les cartes grises vont au bord droit (GREY_EDGE, x 0,55) ; le conseiller recule en ADV_S08.
- S09 « Première » : [chapitre] grandit x 1,6 sur le disque 1 et revient ; [barre2] (contour vide) se rétracte vers la
  droite dans le pied de l'horloge (piste w -> 0, ou vanish into horloge) ; le conseiller va au coin bas droit du
  cadre (820, 1135). « limites » : toi.trace le long du rectangle FRAME (bas vers la gauche, gauche, haut, droite)
  pendant que [cadre] (case, rot 180) se trace sous la pointe (draw linéaire, même durée) ; il finit dehors
  (840, 1135). Le groupe et le coin bas gauche sont dedans ; les cartes grises dehors. « l’IA » : [ia] glisse dans le
  coin libre IA_S09 (x 0,8), pilule à droite. « lire » : [cone] (sommets à poser : apex = tête de l'IA, coupé net par
  le haut et le bord droit du cadre) s'ouvre ; les traits gris des sources passent au deep (doc read 0 -> 1).
- S10 « Uniquement » : [rayon] pivote vers la carte grise du haut et bute sur le bord droit du cadre (≈ (780, 660)) :
  [cadre_flash] flashe (opacity 1 -> 0, 100 ms), [impact_cadre], le rayon recule et s'éteint ; le cône s'éteint ; les
  cartes grises ne bougent pas. « outil » : relais [cadre] -> [outil] (window : bar 0 -> 1, la barre de titre
  descend) ; doc1-4 s'empilent en éventail en FAN_S10 ; la pastille vole sur la barre de titre (TITLE_S10, x 0,85),
  le rond dessous (RONDE_S10). « validé » : [sceau] tombe en SEAL_DROP et se coche ([coche_sceau]). « cabinet » : le
  sceau vole au bout de la barre et s'ouvre en « ✓ Cabinet » (relais par outil sealOn / seal 0 -> 1) ; les cartes
  grises glissent vers le bord droit en se réduisant (x 920, scale 0 : rien sous la colonne x > 940).
- S11 « Jamais » : la fenêtre et tout son contenu (docs, pastille, rond, IA) glissent à gauche et se réduisent (centre
  WIN_S11, x 0,88 : mur droit x 555) ; le conseiller reste au repos, stylo baissé. « IA » : [ia_pub] surgit en IA_PUB
  avec [ia_pub_pill] ; [foule] show 0 -> 6, link 0 -> 1. « non » : [trait_pub] se tire de sa tête jusqu'à la face
  extérieure du mur ; la carte Mail (doc3) se soulève de l'éventail et glisse vers lui à vitesse constante, heurte le
  mur de l'intérieur, s'arrête net ([impact_mur], kit.shake x), retombe sur l'éventail (300 ms plus tard) ; le trait
  se rétracte. « RGPD » : [brique1] tombe et s'encastre à cheval sur le mur (CHOC). « politique » : [brique2] se pose
  dessus. « s’appliquent » : le cadenas de [outil] tombe sur la barre de titre et se ferme (lockOn, lockDy, lock) ;
  ia_pub, sa pilule et sa foule se réduisent en point. Jamais de rouge ici ; le conseiller n'envoie rien.
- S12 « Ça » : morph : les briques s'enfoncent dans le mur (scale 0) ; [outil] se réduit en badge (BADGE_C, x 0,3)
  avec son contenu (éventail, pastille en titre, rond) ; [ia] en sort et se pose en IA_S12 (x 0,8). « documents » :
  [faisceau_lit] relie la tête de l'IA au badge ; info1-4 quittent le coin de leur source (kit.move world=True) et se
  rangent en colonne sur la colonne des puces de la page, où elles relaient la puce de L1-L4 (bulletOn 0 -> 1) ;
  derrière elles, au bout du faisceau, [fiche] naît en PAGE_S12 (pop), titre [fiche_titre1] « Réponse » ; le rond
  quitte le badge et devient la puce de L5. « IA » : [faisceau_page] balaie la page ; L1-L4 s'écrivent (kit.type,
  4 caractères / image, décalés de 2 images, finies avant « peut ») ; chaque rangée finie reçoit [coche_iaN]. « peut » :
  le faisceau vers le badge est éteint ; [pensee1-3] montent de la tête de l'IA et [nuage] surgit en CLOUD_C avec
  [nuage_val] « 5 ans » ; tenue ≈ 1,4 s, rien d'autre ne bouge. « fluide » : « 5 ans » vole en arc (80) jusqu'à L5,
  qui s'écrit « Horizon … 5 ans » et reçoit [coche_ia5] ; le nuage rentre dans la tête ; [reflet] balaie la page
  (p 0 -> 1, 400 ms). Puis immobilité (tenue sur « et »). « fausse » : la puce vide de L5 bat deux fois
  (kit.pulse(..., track="pulse")) et son contour passe au rouge (alarm 0 -> 1) ; rien d'autre ne bouge.
- S13 « Deuxième » : kit.step(f, 1) ; [chapitre] (texte « 2 ») grandit x 1,6 et revient ; l'IA se range en
  IA_CORNER x 0,42 (pilule à droite) ; ses coches restent. « étape » : la page glisse en PAGE_S13 (x 0,95) ; le
  conseiller monte à droite de la page (ADV_S13, walk), stylo vers elle. « exiges » : toi.trace descend la colonne
  x 730 ; sous la pointe, [case1-5] se tracent (draw), avec leurs tirets de bandeau et de date ([caseN_l1-2]).
- S14 « structuré » : [fiche_titre1] -> [fiche_titre2] « Brief · 1 page » (fondu enchaîné) ; la pastille vole du
  badge à l'en-tête (arc 60) puis relais par [pastille_fiche] ; les rangées se déploient (grow 0 -> 1, décalées de
  2 images). « page » : le badge rend ses 4 sources en version compacte (doc compact 0 -> 1) qui tombent chacune dans
  sa case (doc1 en face de Bilan, doc2 Contrat, doc3 Décision, doc4 Promis) ; leurs bandeaux et dates s'effacent ; le
  badge vidé se replie (outil scale 0) ; case5 reste vide. « renvoie » : [fil1-4] se tracent de la valeur de chaque
  ligne vers sa source (décalés de 3 images) ; L5 n'en a pas. « date » : [source1-4] (puce-date, tagged 0) se
  détachent de leur source et glissent le long de leur fil jusque sous la valeur (S.along_wire, 550 ms).

Mise en scène réalisée (écarts au brief, places propres à p2 en tête de module) :
- S08 : dossiers gris en (750, 850) et (875, 850) x 0,9 (pilules sans chevauchement, sous x 940) ; bond du conseiller
  en (800, 1010), pointe en (700, ≈ 840) sur les faisceaux 5-6 (bras sans croiser le buste) ; groupe 2 x 2 en y 575 /
  885 et pastille / rond en y 730 (allée de 98 px : ni la pastille ni le rond ne touchent les cartes).
- S09 : le tour du cadre est une course (corps posé image par image par toi.hop, pointe par toi.trace sur le contour
  exact de la case) ; il finit en (850, 1135). Le cône est un polygone posé à la tête de l'IA (pts relatifs).
- S10 : éventail en cascade (FAN) : chaque bandeau de source dépasse de la carte de devant.
- S11 : pas de bombement du mur (la fenêtre n'a pas de piste pour cela) : la carte bute, tremble, traits d'impact.
- S13 « étape » : le badge (et ses sources, sa pastille) se range en (880, 480) x 0,18 : la page en PAGE_S13 le
  couvrait en (150, 470). S14 : les sources en tombent dans leurs cases, la pastille en part vers l'en-tête.
- S14 « renvoie » : les fils partent du bout de la valeur (piste aAt) et non de son milieu, qui la barrait.
- Les temps forts calés sur l'attaque audible tombent une ou deux images avant le mot (S08 « Pourquoi » en 888,
  S11 « Jamais » en 1269, S13 « Deuxième » en 1709).

Tour de revue 1 (corrections) :
- Raccord : épingle à seam(S, "S08") = 887 (« Pourquoi » calé sur l'attaque, 888), plus 889.
- S08 : le contour vide de la barre rentre dans l'horloge dès « Pourquoi » ; faisceaux vers le bout gauche des
  bandeaux (pas sur les dates), repliés en tronçons de 40 px quand naissent les dossiers gris ; dossiers gris coiffés
  d'une pilule de même facture que la pastille (60 px, Bold 32, pictogramme de personne) ; « protéger » : bond à côté
  de la pastille (640, 1000), corps, bras et stylo DERRIÈRE la pastille (set_z), la pointe la dépasse et casse les
  faisceaux 5-6 (éclats [eclat] + traits d'impact), tenue 10 images.
- S09 : plus de tour en courant (il passait sur le repère et débordait sur « l’IA ») : bond à droite du coin bas droit,
  pointe sur le coin ; sur « limites », le contour part de la pointe, fait le tour et revient à elle en 17 images
  (fini en 1096, avant « l’IA » en 1100). Il redescend au sol après « lire ».
- S10 : choc du rayon plus grand (éclats x 1,3, tenue 10 images, recul visible) ; « cabinet » : le sceau se lève vers
  nous (x 1,5) et s'abat sur le bout de la barre (choc, éclats) où il s'ouvre en « ✓ Cabinet » ; dossiers gris
  glissés à x 882 puis effacés en opacité (jamais réduits).
- S11 : [mur] (bord droit encré, 14 px, enfant de la fenêtre) dès « Jamais » ; 4 petites cartes versées par la foule
  dans l'IA grand public ; la carte Mail s'écrase contre le mur (sx 0,85) sans le franchir, y reste et recule d'un
  cran à chaque brique ; grand cadenas (lockK 2) qui bat ; l'IA grand public se réduit 4 images plus tard.
- S12 : briques enfoncées dans le mur (sx -> 0) ; fenêtre en deux temps : x 0,65 au centre gauche (lisible) sur
  « Ça », badge sur « documents » quand le faisceau l'atteint ; nuage et « 5 ans » sans retard sur « peut » ; reflet
  fini en 1680 ; « 5 ans » garde le contour pointillé du nuage ([nuage5]) ; « fausse » : puce x 1,6 -> 1,15 deux fois
  puis tenue x 1,15, onde rouge, anneau rouge en tirets ([anneau5]), ligne surlignée de rouge clair à contour rouge en
  tirets ([bande5]).
- S14 : chaque source bat quand son fil l'atteint.

Raccord vers p3 : tout finit avant l'image 1936 ; état final = ENTRY_P3 exactement.
Recyclage : git show 6962c86:wth-videos/scripts/story/V01/p1.py (S05-S08 : cadre, sceau, mur) et p2.py (S09-S13 :
briques, page écrite, nuage, cases, fils, dates).
"""
import math

from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, SCALE, STRETCH, point_at_length

from . import (ADV_S07, ADV_S08, ADV_S13, BADGE_C, BADGE_S, BAR_W, BAR_X0, BAR_Y, CASE_X, CHOC, DOC_GRID_S, DOC_W,
               ENTRY_P2, ENTRY_P3, FICHE_LINES, FRAME_C, FRAME_H, FRAME_W, FRAME_X1,
               FRAME_TOP, GREY_EDGE, GREY_EDGE_S, IA_CORNER, IA_CORNER_S, IA_S08, IA_S08_S, IA_S09,
               IA_S09_S, IA_S12, IA_S12_S, MARKER_XS, PAGE_S12, PAGE_S12_S, PAGE_S13, PAGE_S13_S,
               PASTILLE_HEAD_S, PASTILLE_S08, ROND_S08, RONDE_S10, SEAL_DROP, SEAL_K, TITLE_H, TITLE_S10,
               TITLE_S10_S, WIN_S11, WIN_S11_S, FOULE, IA_PUB, GREY_W, GREY_H, GREY_PILL_W, GREY_PILL_K, PILL_H,
               WALL_X, seam, scene_f0, vanish)

# ---------- places propres à p2 ----------
# S08 : les dossiers gris à droite de la pastille, à sa hauteur ; x 0,9 et 125 px d'écart : leurs pilules (126 px) ne
# se chevauchent pas et la seconde reste sous x 940 (GREY_S08 de __init__ : pilules de 140 px qui se recouvraient)
GREY_P2, GREY_P2_S = [(757, 838), (868, 900)], 0.75   # cartes x 0,75, pilules x 0,85 de même facture que la
#                                                       pastille ; en escalier, à droite de la pastille, sous x 940
ADV_HOP_S08 = [640, 1000]               # S08 « protéger » : le bond, à côté de la pastille (pointe à sa gauche)
PEN_X_S08 = 590                         # pointe du stylo levée sur les faisceaux 5-6, au-dessus de la pastille
ADV_S09 = [870, 1010]                   # S09 : bond à droite du coin bas droit de la zone, pointe sur le coin
ADV_S09_END = [850, 1135]               # S09 : il redescend au sol, en bas à droite, hors du cadre
LASSO = 17                              # S09 « limites » : le contour part de la pointe et en fait le tour (570 ms)
BANNER_DY = -93                         # centre du bandeau de source (repère du document, bandeau de 64 px)
MID_C, MID_S = (380, 760), 0.65         # S12 « Ça » : la fenêtre réduite, encore lisible, au centre gauche
# S08 « client » : groupe 2 x 2 un peu plus ouvert que DOC_GRID_S08 (allée de 98 px) : la pastille et le rond n'y
# touchent ni les cartes ni leurs pastilles d'information
GRID_P2 = [(330, 575), (570, 575), (330, 885), (570, 885)]
PASTILLE_P2, ROND_P2 = (PASTILLE_S08[0], 730), (ROND_S08[0], 730)
ADV_S12 = [880, 1135]                   # S12 : au repos, le stylo hors de la page (bord droit x 810)
BADGE_S13, BADGE_S13_S = (880, 480), 0.18   # S13 « étape » : le badge se range en haut à droite, au-dessus du
#                                            conseiller (la page en PAGE_S13 le couvrait en (150, 470))
FRAME_R = 14                            # rayon des coins de l'entité case (cadre)
# S10 : éventail des 4 sources dans la fenêtre (repère monde, fenêtre à l'échelle 1) : en cascade, doc4 au fond en
# haut, doc1 devant en bas ; chaque bandeau de source dépasse de la carte de devant (x, y, rot)
FAN = [(460, 795, -4), (480, 745, -1.5), (500, 695, 1.5), (520, 645, 4)]
SEAL_CLOSED = (FRAME_X1 - 12 - 46 * SEAL_K / 2, FRAME_TOP + TITLE_H / 2)   # sceau fermé au bout de la barre
SEAL_DISC = 96                                                              # disque du sceau qui tombe (icon disc 48)
IA_PILL_RIGHT = [122, 60]               # pilule « IA » à droite de la tête (repère de l'IA)
IA_PILL_CORNER = [212, 30]              # S13 : rangée petite, pilule à 32 px (x 1 / 0,42) à sa droite
LOCK_FALL = -160                        # S11 : le cadenas tombe de 160 px (repère de la fenêtre)
PENSEE_AT = [(150, 978), (160, 932), (170, 880)]   # S12 : bulles de pensée, de la tête de l'IA au nuage


def _r(p):
    return [round(p[0], 2), round(p[1], 2)]


def _map(p, c0, c1, k):
    """Point p d'une composition centrée en c0 transporté dans la même composition centrée en c1, à l'échelle k."""
    return _r([c1[0] + (p[0] - c0[0]) * k, c1[1] + (p[1] - c0[1]) * k])


def _frame_path(step=2.0):
    """Polyligne monde dense du contour du cadre (case w=FRAME_W, h=FRAME_H, coins de FRAME_R, centre FRAME_C,
    tourné de 180°), dans le sens de son tracé (roundRect de draw.tsx tourné) : coin bas droit -> bas vers la gauche
    -> côté gauche -> haut -> côté droit. Renvoie (points, longueurs cumulées, longueurs des 4 coins)."""
    w, h, r = FRAME_W, FRAME_H, FRAME_R
    x, y = -w / 2, -h / 2
    loc, marks = [], []

    def line(a, b):
        n = max(1, math.ceil(math.dist(a, b) / step))
        loc.extend([a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n] for k in range(n))

    def arc(c, a0, a1):
        marks.append(len(loc))
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
    return pts, acc, [acc[m] for m in marks]


def _frac_at_x(S, wire, n, x):
    """Fraction de longueur du fil `wire` (image n) où il passe à l'abscisse x (le fil va de gauche à droite)."""
    cub = S.wire_cubic(wire, n)
    lo, hi = 0.0, 1.0
    for _ in range(30):
        mid = (lo + hi) / 2
        if point_at_length(cub, mid)[0] < x:
            lo = mid
        else:
            hi = mid
    return round((lo + hi) / 2, 4), point_at_length(cub, (lo + hi) / 2)


def part(S, kit, c):
    toi, sheet = c.toi, c.sheet
    rows, X, ty, ly = sheet.rows, sheet.x, sheet.ty, sheet.ly
    docs = [f"doc{i + 1}" for i in range(4)]
    entry = seam(S, "S08")                                        # 887 : « Pourquoi » calé sur l'attaque (888)

    kit.pin(entry, ENTRY_P2)                                      # etat_initial de S08
    if S.val("toi", "scale", entry) == 0:                         # partie construite seule : la figurine n'est pas entrée
        toi.enter(entry - 10, at=list(ADV_S07))

    def head(n):
        """Avant de la tête de verre de l'IA (monde), départ de ses faisceaux."""
        return S.to_world("ia", c.brain_front, n)

    def beam_off(ids, f, d=8):
        """Les faisceaux rentrent dans la tête (from 0 -> 1), puis sont remis à zéro. Renvoie l'image de fin."""
        for w in ids:
            S.key(w, "from", f, 1, d, "in")
            S.key(w, "draw", f + d, 0)
            S.key(w, "from", f + d, 0)
        return f + d

    # =================== S08 « Pourquoi commencer par limiter ? … protéger ton client. » ===================
    f = kit.at("S08", "Pourquoi", "le disque 1 « Limiter » du repère bat deux fois (x 1,3) ; sa légende se souligne")
    S.key("chapitre", "pos", f - 1, [MARKER_XS[0], S.val("chapitre", "pos", f - 1)[1]])
    S.key("chapitre", "scale", f, 1)                              # posé exactement sur le disque actif
    end = kit.pulse("chapitre", f, times=2, peak=1.3, step=3)
    S.key("chapitre", "scale", end, 0)
    kit.draw("legende1", f, DRAW, track="under")
    kit.pulse("legende1", f, peak=1.12, step=3)
    g = f + 6                                 # le contour vide de la barre rentre dans le pied de l'horloge
    S.keys("barre2", g, STRETCH + 2, "in", w=0, pos=[BAR_X0 + BAR_W, BAR_Y])
    S.key("barre2", "scale", g + STRETCH + 2, 0)

    f = kit.at("S08", "Parce", "l'IA regrandit depuis son coin jusqu'à gauche (x 0,75), sa pilule « IA » dessous")
    kit.move("ia", f, IA_S08, scale=IA_S08_S)
    S.keys("ia_pill", f, MOVE, "inOut", pos=[0, round(c.ai_h / 2 + 30, 1)], scale=1)

    f = kit.at("S08", "gagner", "4 faisceaux pointillés partent ensemble de la tête de l'IA vers les bandeaux des 4 "
               "sources ; de la carte CRM glissent deux dossiers gris, chacun coiffé d'une pilule grise de même forme que "
               "« Client · 9 h » (« 14 h », « 16 h ») ; les 4 faisceaux se replient en courts tronçons ; la pastille puis "
               "les deux pilules grises battent ; deux faisceaux filent vers les dossiers gris, au-dessus de la pastille")
    a = head(f - 1)
    for i, d in enumerate(docs):
        p = S.val(d, "pos", f - 1)
        end = _r([p[0] - (DOC_W / 2 - 18), p[1] + BANNER_DY])           # bout gauche du bandeau (pas sur la date)
        S.key(f"faisceau{i + 1}", "pb", f - 1, end)
        kit.draw(f"faisceau{i + 1}", f, 8)
    doc2 = S.val("doc2", "pos", f - 1)
    for k in range(2):
        g = f"carte_grise{k + 1}"
        kit.pop(g, f, scale=GREY_P2_S, from_pt=doc2, to=GREY_P2[k], d=MOVE, e="inOut")
    arr = f + MOVE
    for i in range(4):                                            # tronçons de 40 px contre les bandeaux
        w = f"faisceau{i + 1}"
        cub = S.wire_cubic(w, arr)
        L = sum(math.dist(point_at_length(cub, k / 20), point_at_length(cub, (k + 1) / 20)) for k in range(20))
        S.key(w, "from", arr, round(max(0.0, 1 - 40 / L), 4), 6, "inOut")
    kit.pulse("pastille", arr, peak=1.15, step=3)
    kit.pulse("carte_grise1_pill", arr + 4, peak=round(GREY_PILL_K * 1.15, 4), step=3)
    kit.pulse("carte_grise2_pill", arr + 8, peak=round(GREY_PILL_K * 1.15, 4), step=3)
    g5 = arr + 4
    pill_y = -GREY_H / 2 * GREY_P2_S
    for k in range(2):
        gx, gy = GREY_P2[k]
        S.key(f"faisceau{k + 5}", "pb", g5 - 1, _r([gx - GREY_PILL_W * GREY_PILL_K * GREY_P2_S / 2 + 6, gy + pill_y]))
        kit.draw(f"faisceau{k + 5}", g5, 8)

    f = kit.at("S08", "protéger", "le conseiller bondit à côté de la pastille et lève son stylo en travers des deux "
               "faisceaux qui visent les dossiers gris : ils cassent net sur sa pointe (éclats et traits d'impact au "
               "point de contact) et restent coupés ; puis tous les faisceaux rentrent dans la tête de l'IA ; pas de rouge")
    toi.set_z(f, 13.3, tool_z=12.9)                               # bras et stylo derrière la pastille, la pointe la
    toi.hop(f, ADV_HOP_S08, 6, h=0)                               # dépasse : on lit toujours « Client · 9 h »
    fr5, hit5 = _frac_at_x(S, "faisceau5", f + 5, PEN_X_S08)
    fr6, hit6 = _frac_at_x(S, "faisceau6", f + 5, PEN_X_S08)
    tip = _r([PEN_X_S08, (hit5[1] + hit6[1]) / 2])
    toi.reach(f + 2, tip, d=4, step=False)
    hit = f + 5                                                   # la pointe est sur les faisceaux
    S.key("faisceau5", "draw", hit, fr5)
    S.key("faisceau6", "draw", hit, fr6)
    S.key("impact_stylo", "pos", hit - 1, _r([tip[0] + 6, tip[1]]))
    kit.pop("impact_stylo", hit, d=3)
    S.key("eclat", "pos", hit - 1, tip)
    S.key("eclat", "p", hit - 1, 0)
    S.key("eclat", "p", hit, 1, 9, "out")
    S.key("eclat", "p", hit + 9, 0)
    vanish(kit, "impact_stylo", hit + 10, d=6)
    beam_off([f"faisceau{k + 1}" for k in range(6)], hit + 10, d=8)

    f = kit.at("S08", "client", "les 4 sources se regroupent en 2 x 2 autour de la pastille (rond vide à sa droite) ; "
               "les dossiers gris glissent au bord droit, intacts ; le conseiller recule")
    for i, d in enumerate(docs):
        S.keys(d, f, MOVE, "inOut", pos=list(GRID_P2[i]), scale=DOC_GRID_S, rot=0)
    kit.move("pastille", f, PASTILLE_P2)
    kit.move("rond", f, ROND_P2)
    for k in range(2):
        kit.move(f"carte_grise{k + 1}", f, GREY_EDGE[k], scale=GREY_EDGE_S)
    toi.rest(f - 1, 6)
    toi.walk(f + 4, ADV_S08, d=14)
    toi.set_z(f + 6, 15, tool_z=15.5)

    # =================== S09 « Première étape : tu limites ce que l’IA peut lire. » ===================
    pts, acc, corners = _frame_path()
    f = kit.at("S09", "Première", "chapitre : le disque 1 grandit (x 1,6) puis revient ; le conseiller bondit à droite "
               "du coin bas droit de la future zone, la pointe de son stylo posée sur ce coin")
    S.key("chapitre", "scale", f, 1)
    S.key("chapitre", "scale", f + 1, 1.6, SCALE, "out")
    S.key("chapitre", "scale", f + 20, 1, SCALE, "inOut")
    S.key("chapitre", "scale", f + 30, 0)
    g = toi.hop(f, ADV_S09, 10, h=0)
    toi.reach(g + 2, _r(pts[0]), d=8, step=False)                 # pointe sur le coin bas droit, bras tendu

    f = kit.at("S09", "limites", "de la pointe de son stylo, un contour en tirets part et fait le tour de la zone (bas, "
               "gauche, haut, droite) jusqu'à revenir à la pointe : le groupe et un coin vide sont dedans, les dossiers "
               "gris dehors ; il a fini avant que l'IA ne bouge")
    S.key("cadre", "draw", f, 1, LASSO, "linear")
    toi.rest(S.word_after("lire", f) - 12, 8)                     # (après le glissement de l'IA : un seul geste à la fois)

    f = kit.at("S09", "l’IA", "l'IA glisse dans le coin libre du cadre, en bas à gauche (x 0,8), sa pilule à sa droite")
    kit.move("ia", f, IA_S09, scale=IA_S09_S)
    kit.move("ia_pill", f, IA_PILL_RIGHT)

    f = kit.at("S09", "lire", "un cône de lecture pointillé s'ouvre de la tête de l'IA sur les 4 sources et s'arrête net "
               "sur les bords haut et droit du cadre ; les traits gris des sources passent au cyan profond (lues)")
    apex = _r(head(f - 1))
    x0, x1, y0 = FRAME_C[0] - FRAME_W / 2 + 15, FRAME_X1 - 3, FRAME_TOP + 3
    cone = [[0, 0], [x0 - apex[0], y0 - apex[1]], [x1 - apex[0], y0 - apex[1]], [x1 - apex[0], 1000 - apex[1]]]
    S.ents["cone"]["p"]["pts"] = [_r(q) for q in cone]
    S.key("cone", "pos", f - 1, apex)
    kit.pop("cone", f, d=POP)
    for i, d in enumerate(docs):
        S.key(d, "read", f + 2 * i, 1, 12, "out")
    toi.hop(f + 11, ADV_S09_END, 8, h=0)                          # il redescend au sol, hors du cadre

    # =================== S10 « Uniquement le dossier client, dans un outil validé par ton cabinet. » ===================
    f = kit.at("S10", "Uniquement", "un rayon de l'IA vise le dossier gris du haut et bute sur le bord droit du cadre : "
               "le bord flashe, traits d'impact, le rayon recule et s'éteint ; les dossiers gris ne bougent pas ; le "
               "cône s'éteint")
    gy = GREY_EDGE[0][1] + 20
    S.key("rayon", "pb", f - 1, [FRAME_X1 - 4, gy])
    kit.draw("rayon", f, 5)
    hit = f + 5
    S.key("cadre_flash", "opacity", hit, 1)
    S.key("cadre_flash", "opacity", hit + 1, 0, 3, "in")
    S.key("impact_cadre", "pos", hit - 1, [FRAME_X1 - 4, gy])
    kit.pop("impact_cadre", hit, d=3)
    S.key("eclat", "pos", hit - 1, [FRAME_X1 - 4, gy])
    S.key("eclat", "scale", hit - 1, 1.3)
    S.key("eclat", "p", hit - 1, 0)
    S.key("eclat", "p", hit, 1, 10, "out")
    S.key("eclat", "p", hit + 10, 0)
    vanish(kit, "impact_cadre", hit + 10, d=6)
    S.key("rayon", "draw", hit + 9, 0, 10, "inOut")             # le rayon tient, cassé, puis recule visiblement
    vanish(kit, "cone", hit + 4, d=MORPH)

    f = kit.at("S10", "outil", "le cadre passe en trait plein et une barre de titre descend sur son bord haut : une "
               "fenêtre de logiciel ; les 4 sources s'empilent en éventail ; la pastille vole sur la barre de titre (son "
               "titre), le rond vide dessous")
    S.key("outil", "scale", f, 1)                                 # relais exact du cadre (cadre plein deep, 6 px)
    S.key("cadre", "scale", f, 0)
    S.key("outil", "bar", f, 1, POP, "out")
    for i, d in enumerate(docs):
        x, y, rot = FAN[i]
        S.keys(d, f, MOVE, "inOut", pos=[x, y], rot=rot)
    kit.move("pastille", f, TITLE_S10, scale=TITLE_S10_S, arc=40)
    kit.move("rond", f, RONDE_S10)

    f = kit.at("S10", "validé", "le sceau du cabinet (disque cyan, bâtiment) tombe dans la fenêtre et se coche")
    S.key("sceau", "pos", f - 1, [SEAL_DROP[0], SEAL_DROP[1] - 200])
    S.key("sceau", "scale", f, 1)
    S.key("sceau", "pos", f, list(SEAL_DROP), DROP, "out")
    kit.draw("coche_sceau", f + DROP, 6)

    f = kit.at("S10", "cabinet", "le sceau vole au bout de la barre de titre et s'ouvre en pilule « ✓ Cabinet » ; les "
               "dossiers gris glissent vers le bord droit et s'y réduisent")
    up = [SEAL_CLOSED[0], SEAL_CLOSED[1] + 40]
    S.fly("sceau", f, 7, "out", to=_r(up), scale=1.5)             # il se lève vers nous, sous le bout de la barre…
    S.fly("sceau", f + 7, 4, "in", to=list(SEAL_CLOSED), scale=round(44 * SEAL_K / SEAL_DISC, 4))   # … et s'y abat
    arr = f + 11                                                  # le choc : le sceau s'imprime sur la barre
    S.key("sceau", "scale", arr, 0)
    S.key("sceau", "opacity", arr, 0)
    S.key("outil", "sealOn", arr, 1)
    S.key("outil", "seal", arr, 1, 8, "out")
    S.key("eclat", "pos", arr - 1, list(SEAL_CLOSED))
    S.key("eclat", "scale", arr - 1, 1.2)
    S.key("eclat", "p", arr - 1, 0)
    S.key("eclat", "p", arr, 1, 9, "out")
    S.key("eclat", "p", arr + 9, 0)
    for k in range(2):                                 # ils glissent vers le bord droit, intacts, et s'effacent
        g = f"carte_grise{k + 1}"
        S.key(g, "pos", f, [882, GREY_EDGE[k][1]], MOVE, "inOut")
        S.key(g, "opacity", f + MOVE - 5, 0, 5, "linear")
        S.key(g, "scale", f + MOVE, 0)

    # =================== S11 « Jamais de données client dans une IA grand public… s’appliquent. » ===================
    def win(p):
        return _map(p, FRAME_C, WIN_S11, WIN_S11_S)

    f = kit.at("S11", "Jamais", "la fenêtre et tout son contenu glissent à gauche et se réduisent ; le conseiller reste "
               "au repos")
    kit.move("outil", f, WIN_S11, scale=WIN_S11_S)
    for i, d in enumerate(docs):
        kit.move(d, f, win(FAN[i][:2]), scale=round(DOC_GRID_S * WIN_S11_S, 4))
    kit.move("pastille", f, win(TITLE_S10), scale=round(TITLE_S10_S * WIN_S11_S, 4))
    kit.move("rond", f, win(RONDE_S10), scale=WIN_S11_S)
    kit.move("ia", f, win(IA_S09), scale=round(IA_S09_S * WIN_S11_S, 4))
    kit.pop("mur", f + 4, d=10)                                   # le bord droit devient un mur épais, encré

    f = kit.at("S11", "IA", "hors de la fenêtre, une IA grand public grise surgit à droite, avec sa pilule « IA grand "
               "public » et une foule de petites figurines grises reliées à sa tête")
    kit.pop("ia_pub", f)
    S.key("foule", "show", f + 2, 6, 9, "linear")
    S.key("foule", "link", f + 6, 1, 9, "out")
    pub_top = _r([IA_PUB[0] + c.pub_head[0], IA_PUB[1] + c.pub_head[1]])
    for k, j in enumerate((0, 1, 3, 5)):                          # chacun verse sa carte dans la même IA
        src = _r([IA_PUB[0] + FOULE["pts"][j][0], IA_PUB[1] + FOULE["pts"][j][1] + 10])
        cp, g = f"carte_pub{k + 1}", f + 14 + 4 * k
        S.key(cp, "pos", g - 1, src)
        kit.pop(cp, g, d=4)
        S.key(cp, "pos", g + 4, pub_top, 10, "in")
        S.key(cp, "scale", g + 4, 0.3, 10, "in")
        S.key(cp, "scale", g + 14, 0)

    f = kit.at("S11", "non", "un trait gris part de la tête de l'IA grand public jusqu'au mur ; la carte « Mail » se "
               "soulève de l'éventail, glisse vers lui, heurte le mur de l'intérieur, s'arrête net et retombe ; le "
               "conseiller ne fait rien")
    kit.draw("trait_pub", f, 8)
    lift = f + 8
    home3 = win(FAN[2][:2])
    half = DOC_W / 2 * DOC_GRID_S * WIN_S11_S
    wall_in = WALL_X - 14 * WIN_S11_S / 2 - 1                     # face intérieure du mur
    stop = _r([wall_in - half, CHOC[1]])
    group3 = ["doc3", "doc3_bandeau", "doc3_bandeau_txt", "doc3_date", "doc3_date_txt"]
    for id in group3:                                             # la carte et ses enfants passent devant l'éventail
        kit.ensure(id, "z", S.ents[id]["z"])
        S.key(id, "z", lift, round(S.ents[id]["z"] + 0.5, 2))
    S.key("doc3", "rot", lift, 0, 4, "out")
    S.key("doc3", "pos", lift, stop, 12, "linear")
    hit = lift + 12
    kit.ensure("doc3", "sx", 1)
    S.key("doc3", "sx", hit, 0.85, 2, "out")                      # elle s'écrase contre le mur, sans le franchir
    S.key("doc3", "pos", hit, _r([wall_in - half * 0.85, CHOC[1]]), 2, "out")
    kit.pop("impact_mur", hit, d=3)
    S.key("eclat", "pos", hit - 1, _r([wall_in, CHOC[1]]))
    S.key("eclat", "scale", hit - 1, 1.2)
    S.key("eclat", "p", hit - 1, 0)
    S.key("eclat", "p", hit, 1, 9, "out")
    S.key("eclat", "p", hit + 9, 0)
    vanish(kit, "impact_mur", hit + 10, d=6)
    pressed = _r([wall_in - half - 10, CHOC[1]])
    S.key("doc3", "sx", hit + 8, 1, 5, "out")                     # elle reste plaquée près du mur
    S.key("doc3", "pos", hit + 8, pressed, 5, "out")
    beam_off(["trait_pub"], hit + 9, d=8)

    f = kit.at("S11", "RGPD", "au point du choc, une brique encre « RGPD » tombe et s'encastre à cheval sur le mur")
    S.key("brique1", "pos", f - 1, [CHOC[0], CHOC[1] - 200])
    S.key("brique1", "scale", f, 1)
    S.key("brique1", "pos", f, list(CHOC), DROP, "out")
    x3 = S.val("doc3", "pos", f + DROP - 1)                       # la carte recule d'un cran : le mur s'épaissit
    S.key("doc3", "pos", f + DROP, _r([x3[0] - 26, x3[1]]), 6, "out")

    f = kit.at("S11", "politique", "une brique « Politique interne » tombe et se pose sur la première, ferme")
    b2 = S.val("brique2", "pos", f - 1)
    S.key("brique2", "pos", f - 1, [b2[0], b2[1] - 200])
    S.key("brique2", "scale", f, 1)
    S.key("brique2", "pos", f, b2, DROP, "out")
    x3 = S.val("doc3", "pos", f + DROP - 1)
    S.key("doc3", "pos", f + DROP, _r([x3[0] - 26, x3[1]]), 6, "out")

    f = kit.at("S11", "s’appliquent", "un cadenas tombe sur la barre de titre et se ferme ; l'IA grand public, sa pilule "
               "et sa foule se réduisent en point")
    S.key("outil", "lockDy", f - 1, LOCK_FALL)
    S.key("outil", "lockK", f - 1, 2)                             # grand cadenas (56 px) au centre de la barre
    S.key("outil", "lockOn", f, 1)
    S.key("outil", "lockDy", f, 0, 9, "out")
    S.key("outil", "lock", f + 9, 1, 6, "out")
    S.key("outil", "lockK", f + 15, 2.3, 3, "out")
    S.key("outil", "lockK", f + 18, 2, 4, "inOut")
    vanish(kit, "ia_pub", f + 13)
    S.key("doc3", "pos", f + 2, home3, MOVE, "inOut")              # la carte retourne dans l'éventail
    S.key("doc3", "rot", f + 2, FAN[2][2], MOVE, "inOut")
    for id in group3:
        S.key(id, "z", f + 2 + MOVE, S.ents[id]["z"])

    # =================== S12 « Ça ne suffit pas : … une réponse fluide… et fausse. » ===================
    def badge(p):
        return _map(p, FRAME_C, BADGE_C, BADGE_S)

    f = kit.at("S12", "Ça", "les briques s'enfoncent dans le mur ; la fenêtre se réduit en badge en haut à gauche avec "
               "ses sources, sa pastille-titre et le rond vide ; l'IA en sort et se pose en bas à gauche")
    def mid(p):
        return _map(p, FRAME_C, MID_C, MID_S)

    for b in ("brique1", "brique2"):                              # les briques s'enfoncent dans le mur
        kit.ensure(b, "sx", 1)
        S.key(b, "sx", f, 0, 6, "in")
        S.key(b, "scale", f + 6, 0)
    g = f + 5                                                     # 1er temps : la fenêtre, réduite de moitié, lisible
    S.keys("outil", g, MORPH, "out", pos=list(MID_C), scale=MID_S)
    for i, d in enumerate(docs):
        S.keys(d, g, MORPH, "out", pos=mid(FAN[i][:2]), scale=round(DOC_GRID_S * MID_S, 4))
    S.keys("pastille", g, MORPH, "out", pos=mid(TITLE_S10), scale=round(TITLE_S10_S * MID_S, 4))
    S.keys("rond", g, MORPH, "out", pos=mid(RONDE_S10), scale=MID_S)
    S.keys("ia", f, MOVE, "inOut", pos=list(IA_S12), scale=IA_S12_S)
    toi.walk(f, ADV_S12, d=10)

    f = kit.at("S12", "documents", "un faisceau pointillé relie la tête de l'IA au badge ; les 4 pastilles "
               "d'information en sortent et se rangent en colonne ; derrière elles naît une page « Réponse » dont "
               "elles deviennent les puces ; le rond vide se pose sur la 5e rangée")
    S.keys("outil", f, MORPH, "out", pos=list(BADGE_C), scale=BADGE_S)   # 2e temps : le badge
    for i, d in enumerate(docs):
        S.keys(d, f, MORPH, "out", pos=badge(FAN[i][:2]), scale=round(DOC_GRID_S * BADGE_S, 4))
    S.keys("pastille", f, MORPH, "out", pos=badge(TITLE_S10), scale=round(TITLE_S10_S * BADGE_S, 4))
    S.keys("rond", f, MORPH, "out", pos=badge(RONDE_S10), scale=BADGE_S)
    S.key("faisceau_lit", "pb", f + 5, _r([BADGE_C[0] + 10, BADGE_C[1] + FRAME_H / 2 * BADGE_S - 6]))
    kit.draw("faisceau_lit", f + 6, 6)                            # le faisceau atteint le badge quand il s'y pose
    f = f + 8
    kit.pop("fiche", f + 2, scale=PAGE_S12_S)

    def bullet_w(i):                                              # puce de la rangée i, page en PAGE_S12
        return _r([PAGE_S12[0] + X["bullet"] * PAGE_S12_S, PAGE_S12[1] + (rows[i] + ty) * PAGE_S12_S])

    k_b = 22 / 28 * PAGE_S12_S                                    # pastille de 56 px -> puce de 44 px
    for i in range(4):
        g = f + 4 + 3 * i
        S.fly(f"info{i + 1}", g, MOVE, "inOut", to=bullet_w(i), scale=k_b)
        S.key(f"info{i + 1}", "scale", g + MOVE, 0)
        S.key(f"info{i + 1}", "opacity", g + MOVE, 0)
        S.key(f"L{i + 1}", "bulletOn", g + MOVE, 1)
    g = f + 7
    S.fly("rond", g, MOVE, "inOut", to=bullet_w(4), scale=k_b)
    S.key("rond", "scale", g + MOVE, 0)
    S.key("rond", "opacity", g + MOVE, 0)
    S.key("L5", "bulletOn", g + MOVE, 1)

    f = kit.at("S12", "IA", "un faisceau pointillé de l'IA balaie la page : les lignes 1 à 4 s'écrivent (Bilan, "
               "Contrat, Décision, Promis) et chacune reçoit la coche pointillée de l'IA")
    pa = S.to_world("fiche", [X["text"] + 30, rows[0] + ty], f - 1)
    pb = S.to_world("fiche", [X["text"] + 30, rows[3] + ty], f - 1)
    S.key("faisceau_page", "pb", f - 1, _r(pa))
    kit.draw("faisceau_page", f, 3)
    S.key("faisceau_page", "pb", f + 3, _r(pb), 10, "linear")
    beam_off(["faisceau_page"], f + 13, d=5)
    beam_off(["faisceau_lit"], f + 8, d=6)                       # le faisceau vers les documents s'éteint
    for i in range(4):
        done = kit.type(f"L{i + 1}", f + 2 * i, rate=4)
        kit.draw(f"coche_ia{i + 1}", done, 5)

    f = kit.at("S12", "peut", "seul en mouvement : trois bulles pointillées montent de la tête de l'IA et un nuage de "
               "pensée surgit à gauche de la page, avec « 5 ans » dedans ; il reste là")
    for k, at in enumerate(PENSEE_AT):
        S.key(f"pensee{k + 1}", "pos", f - 1, list(at))
        kit.pop(f"pensee{k + 1}", f + k, d=6)
    kit.pop("nuage", f, d=POP)
    kit.pop("nuage_val", f + 3, d=6)

    f = kit.at("S12", "fluide", "« 5 ans » quitte le nuage et vole sur la 5e rangée, qui s'écrit « Horizon 5 ans » aussi "
               "proprement que les autres et reçoit la même coche pointillée ; le nuage rentre dans la tête ; un "
               "reflet balaie la page ; puis plus rien ne bouge")
    p5 = sheet.lines[4][1]
    val5 = S.to_world("fiche", [X["value"] - p5["valueW"] / 2, rows[4] + ty], f - 1)
    S.fly("nuage_val", f, MOVE, "inOut", to=_r(val5), scale=round(32 / 34, 4), arc=80)
    kit.type("L5", f, n=len(FICHE_LINES[4][0]), rate=4)
    arr = f + MOVE
    S.key("nuage_val", "scale", arr, 0)
    S.key("nuage_val", "opacity", arr, 0)
    S.key("L5", "chars", arr, len(FICHE_LINES[4][0]) + len(FICHE_LINES[4][1]))
    kit.draw("coche_ia5", arr, 5)
    top = c.brain_top
    vanish(kit, "nuage", f + 3, into=S.to_world("ia", top, f + 3), d=POP)
    for k in range(3):
        vanish(kit, f"pensee{3 - k}", f + 3 + k, into=S.to_world("ia", top, f + 3), d=6)
    kit.pop("nuage5", arr, d=6)                                   # « 5 ans » garde le contour du nuage
    S.key("reflet", "p", arr + 1, 1, 7, "linear")                  # fini à l'image 1680 : immobile sur « et »

    f = kit.at("S12", "fausse", "la puce vide de la 5e ligne bat deux fois et son contour passe au rouge ; rien "
               "d'autre ne bouge (ni l'IA, ni sa coche, ni le conseiller)")
    S.key("L5", "alarm", f, 1, 3, "out")                          # la puce éclate : x 1,6 -> 1,15, deux fois,
    S.key("L5", "pulse", f, 1, 4, "out")                          # contour rouge, et reste agrandie
    S.key("L5", "pulse", f + 4, 0.25, 4, "inOut")
    S.key("L5", "pulse", f + 8, 1, 4, "out")
    S.key("L5", "pulse", f + 12, 0.25, 4, "inOut")
    S.key("onde5", "scale", f, 1)                                 # une onde rouge part de la puce
    S.key("onde5", "opacity", f, 0.6)
    S.key("onde5", "scale", f + 1, 2.6, 12, "out")
    S.key("onde5", "opacity", f + 1, 0, 12, "linear")
    S.key("onde5", "scale", f + 13, 0)
    kit.pop("anneau5", f + 8, d=6)                                # puis un anneau rouge en tirets l'entoure
    kit.fade("bande5", f + 4, 1, d=6)                             # la ligne entière surlignée de rouge clair

    # =================== S13 « Deuxième étape : tu exiges. » ===================
    f = kit.at("S13", "Deuxième", "le repère passe à « 2 · Exiger » et le disque 2 grandit puis revient ; l'IA se range, "
               "petite, dans le coin bas gauche ; ses coches restent sur la page")
    arr = kit.step(f, 1)
    S.key("legende1", "under", f, 0, FADE, "inOut")
    kit.draw("legende2", f + 4, DRAW, track="under")
    S.key("chapitre", "pos", f - 1, [MARKER_XS[1], S.val("chapitre", "pos", f - 1)[1]])
    S.key("chapitre_txt", "text", f - 1, "2")
    S.key("chapitre", "scale", arr, 1)
    S.key("chapitre", "scale", arr + 1, 1.6, SCALE, "out")
    S.key("chapitre", "scale", arr + 11, 1, SCALE, "inOut")
    S.key("chapitre", "scale", arr + 21, 0)
    kit.move("ia", f, IA_CORNER, scale=IA_CORNER_S)
    S.keys("ia_pill", f, MOVE, "inOut", pos=list(IA_PILL_CORNER), scale=round(1 / IA_CORNER_S, 4))

    f = kit.at("S13", "étape", "la page glisse à gauche ; le conseiller monte à sa droite, stylo pointé vers elle : il "
               "prend la main")
    kit.move("fiche", f, PAGE_S13, scale=PAGE_S13_S)
    kit.move("outil", f, BADGE_S13, scale=BADGE_S13_S)            # le badge se range hors de la page, sources dedans
    for i, d in enumerate(docs):
        kit.move(d, f, _map(FAN[i][:2], FRAME_C, BADGE_S13, BADGE_S13_S), scale=round(DOC_GRID_S * BADGE_S13_S, 4))
    kit.move("pastille", f, _map(TITLE_S10, FRAME_C, BADGE_S13, BADGE_S13_S),
             scale=round(TITLE_S10_S * BADGE_S13_S, 4))
    col = [[CASE_X, c.case_y(i)] for i in range(5)]
    g = toi.walk(f, list(ADV_S13), d=14)
    toi.reach(g + 1, col[0], d=8, step=False)

    f = kit.at("S13", "exiges", "la pointe descend la colonne : en face de chaque ligne se trace une case-source vide "
               "en tirets (bandeau et date vides), de la forme des sources")
    hits = toi.trace(f, col, step=False)
    for i in range(5):
        h = max(hits[i], f)
        kit.draw(f"case{i + 1}", h, 4)
        kit.draw(f"case{i + 1}_l1", h + 1, 4)
        kit.draw(f"case{i + 1}_l2", h + 2, 4)
    toi.rest(hits[-1] + 1, 8)

    # =================== S14 « Un brief structuré d’une page, … à un document et à une date. » ===================
    f = kit.at("S14", "structuré", "l'en-tête « Réponse » devient « Brief · 1 page » ; la pastille vole du badge à "
               "l'en-tête ; chaque ligne se déploie en rangée")
    kit.fade("fiche_titre1", f, 0)
    kit.fade("fiche_titre2", f + 2, 1)
    S.fly("pastille", f, MOVE, "inOut", to=_r(S.to_world("fiche", c.head_pill, f - 1)),
          scale=round(PASTILLE_HEAD_S * PAGE_S13_S, 4), arc=60)
    arr = f + MOVE
    S.key("pastille", "scale", arr, 0)
    S.key("pastille", "opacity", arr, 0)
    S.key("pastille_fiche", "opacity", arr, 1)
    for i in range(5):
        S.key(f"L{i + 1}", "grow", f + 2 * i, 1, POP, "out")

    f = kit.at("S14", "page", "le badge rend ses 4 sources en version compacte, qui tombent chacune dans sa case ; le "
               "badge vidé se replie ; la case 5 reste vide")
    for i, d in enumerate(docs):
        g = f + 2 * i
        S.keys(d, g, MOVE, "inOut", pos=list(col[i]), scale=1, compact=1, rot=0)
        S.key(f"{d}_bandeau", "opacity", g, 0, FADE, "out")
        S.key(f"{d}_date", "opacity", g, 0, FADE, "out")
    vanish(kit, "outil", f + 12, d=POP)

    f = kit.at("S14", "renvoie", "un fil plein part de la valeur de chaque ligne 1 à 4 et rejoint sa source ; la ligne 5 "
               "n'en a pas")
    for i in range(4):                                            # le fil part du bout de la valeur (pas à travers)
        kit.ensure(f"fil{i + 1}", "aAt", list(c.wire_a[i]))
        S.key(f"fil{i + 1}", "aAt", f - 1, [X["value"] + 6, rows[i] + ty])
        kit.draw(f"fil{i + 1}", f + 3 * i, DRAW)
        kit.pulse(f"doc{i + 1}", f + 3 * i + DRAW, peak=1.08, step=3)   # la source bat quand le fil l'atteint

    f = kit.at("S14", "date", "la date de chaque source se détache et glisse le long de son fil jusque sous la valeur de "
               "sa ligne ; la case 5 reste vide")
    for i in range(4):
        s = f"source{i + 1}"
        dst = S.to_world("fiche", S.val(s, "pos", f - 1), f - 1)
        a0 = point_at_length(S.wire_cubic(f"fil{i + 1}", f - 1), 0)
        off = [dst[0] - a0[0], dst[1] - a0[1]]
        kit.pop(s, f, d=6)
        S.along_wire(s, f"fil{i + 1}", f, MOVE, "inOut", 1, 0, f - 1, offset=lambda p, o=off: [o[0] * p, o[1] * p])

    # raccord vers p3 : l'état de l'image 1935 doit être exactement ENTRY_P3
    last = scene_f0(S, "S15") - 1
    for id, tracks in ENTRY_P3.items():
        for track, v in tracks.items():
            cur = S.val(id, track, last, 0 if track not in ("pos",) else None)
            diff = (max(abs(a - b) for a, b in zip(cur, v)) if isinstance(v, (list, tuple))
                    else abs((cur or 0) - v))
            if diff > 1e-3:
                kit.warn(f"raccord p2 -> p3 : {id}.{track} vaut {cur} à l'image {last}, ENTRY_P3 attend {v}")
