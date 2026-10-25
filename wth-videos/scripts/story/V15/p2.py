"""V15, partie 2 : S09-S16, images 900-1745 (30 temps forts, 28,2 s). Fin du point 1, point 2, début du point 3.

ÉTAT D'ENTRÉE (etat_initial de S09) : kit.pin(899, ENTRY_P2) en tête de partie. Tour de 4 blocs étiquetés (x 300-620,
y 830-1230), pastille au sommet (460, 798), accolade et « Grand plan » à gauche ; huit « ? » au-dessus de « Toi » ;
jauge « Énergie » vide (fill RED) ; « Lundi » ; « Toi » au sol en TOI_RECUL (780, 1135), affaissé, bras baissé.
Partie isolée (WTH_PARTS=p2) : « Toi » est à son état de distribution (TOI_P0, lean 0) ; si S.val("toi", "pos", 899)
n'est pas TOI_RECUL, le faire marcher (walk low) jusqu'à TOI_RECUL vers 885-899 : sans effet dans le film entier.
Jamais de kit.pin sur toi / toi_bras / toi_stylo.

RÈGLES DE LA PARTIE
- Blocs : set_blocks(S, f, d, e, geoms) pose blocs + enfants dans une même clé ; un bloc qui change de largeur garde
  ses enfants à -w/2 + 35 / + 67 (block_children). La pastille suit le bloc du haut (même f, d, e).
- Penché en avant = lean négatif ; bras baissé au repos (hold_low après lean_to / hop quand il n'écrit pas).
- Le stylo de « Toi » cause chaque changement : cercles, chiffres et coches se tracent AU CONTACT (hit de tap).
- « Plus tard » est la seule alerte rouge de la partie (S09 -> S11).

SCÈNE PAR SCÈNE
- S09 (900-999) « Et » : q1-q8 reviennent dans leur bloc (kit.stagger 1 image, kit.vanish into centre du bloc) ;
  lean 0. « marche » : set_blocks(…, d=14, "inOut", [tower(i, 110)]) ; pastille -> PASTILLE_TOUR[110] ; accolade sy
  1,1 et gp_nom -> GP_NOM_C[110] (mêmes images) ; AU MÊME INSTANT walk(low) à reculons vers TOI_RECUL2 (10 images).
  « repousse » : idem vers 120 (PASTILLE_TOUR[120], sy 1,2, GP_NOM_C[120]) et walk(low) vers TOI_P0, tête basse.
  « départ. » : calendrier text « Plus tard », w cal_w, fill RED (hex, 6 images) ; textOp 0 et cal_alerte opacité 1
  (le libellé devient papier) ; pulse 1,1.
- S10 (1000-1083) « solution, » : walk vers TOI_TIRE (10 images), puis la pointe se pose sur le bord droit de B1
  (622, 1170) (reach court : elle y RESTE, pas de tap qui relève) ; pulse bloc1 x1,04 au contact. « donc » : walk(…,
  TOI_P0, 12) puis, image par image, la pointe suit le bord droit de B1 qui s'allonge de x 620 à 790 (bloc1 : w 320 ->
  490, centre x 460 -> 545, bord gauche fixe ; enfants block_children) : un reach d=1 par image APRÈS le walk.
  « baisser » : set_blocks vers [stairs(i)] marche par marche (kit.stagger 3 images, MOVE inOut ; h 120 -> 100) ;
  pastille -> PASTILLE_ESCALIER avec bloc4 ; kit.vanish de accolade et gp_nom dans B1 ; bras au repos (lower).
  « marche. » : les 4 marches battent de B1 à B4 (stagger 3, x1,04).
- S11 (1084-1172) « l’inverse : » : calendrier « Semaine 1 », fill LIGHT (6 images), cal_alerte 0, textOp 1 ; pulse.
  « choisis » : hit = toi.tap(f - TAP + 1, NUM_PTS[0]) ; kit.draw("num1", hit, 8) + kit.type("num1_txt", hit) ;
  bloc1 fill PAPER -> LIGHT (hex, 9 images).
- S12 (1173-1243) « Fais-la, » : toi.hop(f, TOI_M1, 16, h=40) (saut LOURD) puis lean -8 / +6 / 0 (3 x 4 images,
  vacille) ; nom_toi -> NOM_MARCHE (MOVE). « note » : tap NUM_PTS[1] ; draw num2 + type ; 3 et 4 restent sans numéro.
- S13 (1244-1376) « exemple, » : `abonnement` (TAG.png + texte) kit.pop(from_pt=ABO_FROM) qui vole jusqu'à ABO_C (MOVE,
  arc 60). « 10 » : cadran en CADRAN_TOI, start 0 / value 0 à f-1, kit.pop(from_pt=CAL_C) ; value 0 -> 10 en 15 images
  linéaire ; cadran_txt « 10 min » pop. « résilier » : toi.strike(f, *ABO_STRIKE, line="abonnement_trait",
  track="draw") (diagonale, à portée depuis TOI_M1). « abonnement » : kit.drop("abonnement", f, out=True, h=420,
  dx=-40, rot=25). « inutile. » : tap COCHE_PTS[0] ; kit.draw("coche1", hit, 6).
- S14 (1377-1526) « Ou » : kit.vanish("cadran", f, into=CAL_C) (cadran_txt suit). « virement » / « dater » / « frais » :
  kit.pop(opt_virement | opt_projet | opt_frais, f, from_pt=OPT_FROM[id], d=MOVE) : chaque carte sort de la fin de SA
  marche et monte à OPT_C (735 / 175 / 455, y 560). « Toi » ne les touche pas.
- S15 (1527-1587) « L’élan » : energie fill -> CYAN (clé instantanée, la jauge est vide) ; kit.pop("elan1", f) puis
  kit.move vers ENERGIE_QUARTS[0] (MOVE, arc 200) ; à l'arrivée energie value 0 -> 0,25 (4 images) et elan1 disparaît
  (scale 0). « vient » : les 3 cartes rentrent chacune dans sa marche (stagger 2 ; kit.vanish into OPT_FROM[id]).
  « l’action, » : toi.hop(f, TOI_M2, 12, h=30), sans vaciller (nom_toi suit, enfant).
- S16 (1588-1745) « marche ? » : les 4 marches battent (stagger 3). « Parce » : calendrier « Semaine 2 », pulse.
  « chaque » : tap COCHE_PTS[1] ; draw coche2. « réussie » : elan2 de COCHE_PTS[1] vers ENERGIE_QUARTS[1] ; value
  0,25 -> 0,5. « suivante » : tap NUM_PTS[2] ; draw num3 + type. « facile. » : toi.hop(f, TOI_M3, 8, h=20, lean=0),
  bond éclair sans vaciller (comparer au saut lourd de S12) ; pulse energie 1,08.

CONTRÔLE SANS SON : S09 un écart au sol (`ecart`, trait encre et deux butées, y 1256) relie la face de la tour au pied
de « Toi » et s'allonge avec chaque bond en arrière (49 -> 129 -> 199 px) ; « Plus tard » bat deux fois ; S10 l'écart se
referme quand il revient, puis s'efface ; segments d'énergie : vol de 13 images, la jauge bat à l'emboîtement ; petite
horloge des montées r 50.

PASSAGE À p3 (ENTRY_P3, épinglé par p3 à l'image 1745) : tout finit avant 1746 (le bond de « facile. » finit vers
1728). Fin exacte attendue : blocs stairs(i), bloc1 fill LIGHT, les autres PAPER ; pastille PASTILLE_ESCALIER ;
accolade et gp_nom 0 ; num1-3 scale 1 draw 1 chiffre écrit ; coche1-2 draw 1, coche3 draw 0 ; energie value 0,5 fill
CYAN ; elan1-3 0 ; calendrier « Semaine 2 » fill LIGHT ; cadran, cadran_txt, abonnement, cartes, q*, numt* à 0 ;
nom_toi en NOM_MARCHE. « Toi » en TOI_M3 (378, 835), lean 0.

ÉCARTS D'EXÉCUTION (aucun sens changé, aucun temps fort déplacé) :
- les trois montées (S12, S15, S16) passent par Figure.run sur un trajet qui monte d'abord presque à la verticale puis
  arque jusqu'à la marche (_climb), en 16 / 12 / 8 images : un hop (trajet droit + rebond h 40 / 30 / 20) faisait
  passer le bas du buste (2 x 59 px) dans l'arête de la marche ; le contraste lourd / léger / éclair tient à la durée
  et au vacillement de S12 ;
- « baisser » : chaque marche glisse en 12 images (au lieu de MOVE 16), décalées de 3 : chacune est posée quand elle
  bat sur « marche. » (12 images plus tard).

REVUE 1 : S09 croissance 100 -> 125 -> 150 px en SCALE + secousse, « Grand plan » bat, recul par bonds de 80 / 70 px
(TOI_RECUL2 / TOI_RECUL3) avec trait de poussière au talon ; « Plus tard » glisse de 40 px ; S10 prise du bord de B1 à
y 1190 ; S12 élan en arrière 4 images, montée lourde 18 images, petite horloge (45 min) ; S13 carte plate, tour du
week-end en tirets autour de l'horloge, chute derrière l'escalier hors champ ; S14 cartes garées au-dessus de leur
marche, fil tireté ; S15 segment 2 x (9 images, arrivée sur « vient »), cartes qui redescendent en arc (14 images,
décalées de 4) ; S16 montée éclair en 6 images avec traits de vitesse, horloge à peine entamée. Pince de fin : assert
max(fins) < scene_f0(S, "S17").
"""
import math

from pipeline.story import FADE, MORPH, MOVE, POP, SCALE, STYLE  # noqa: F401
from pipeline.story_kit import TAP

from . import *  # noqa: F401,F403


def _climb_pts(a, b):
    """Trajet de la montée sur la marche suivante (centre de la figurine) : d'abord presque à la verticale (le bas du
    buste, large de 2 x 59 px, passe au-dessus de l'arête de la marche), puis en arc jusqu'à la place `b`. Un hop
    (trajet droit + rebond) ferait passer le buste dans la marche."""
    dx = b[0] - a[0]
    return [list(a), [a[0] - 2, a[1] - 75], [a[0] - 12, a[1] - 120], [a[0] + 0.4 * dx, a[1] - 140],
            [a[0] + 0.72 * dx, a[1] - 130], list(b)]


def _climb(toi, f, to, d):
    """Monte sur la marche `to` en d images (Figure.run), bras baissé. Renvoie f + d."""
    a = toi.S.val("toi", "pos", f - 1)
    end = toi.run(f, _climb_pts(a, to), d)
    toi.hold_low(f, end)
    return end


def _cal(S, kit, f, key, fill, alert):
    """La pilule-calendrier bascule sur T_CAL[key] et bat x1,1. alert=True : fond rouge, libellé encre effacé sous le
    texte papier `cal_alerte` ; False : retour au neutre (le nouveau libellé paraît quand la largeur est presque là)."""
    S.key("calendrier", "fill", f, fill, FADE, "out")
    S.key("calendrier", "w", f, cal_w(T_CAL[key]), FADE, "out")
    if alert:
        S.key("calendrier", "text", f, T_CAL[key])
        S.key("calendrier", "textOp", f, 0, 2, "out")
    else:
        S.key("calendrier", "text", f + 2, T_CAL[key])
        S.key("calendrier", "textOp", f + 2, 1, 4, "out")
    kit.fade("cal_alerte", f, 1 if alert else 0, d=FADE if alert else 3)
    kit.pulse("calendrier", f, peak=1.1)


def _ecart(S, f, d, toi_x, e="inOut"):
    """Contrôle sans son : l'écart au sol entre la face de la tour (x 622) et le pied avant de « Toi » (trait encre
    et deux butées) va à sa nouvelle longueur en d images, avec la même clé que le bond de « Toi »."""
    x1 = toi_x - ECART_TOE
    w = round(x1 - ECART_X0, 1)
    S.keys("ecart", f, d, e, pos=[round((ECART_X0 + x1) / 2, 1), ECART_Y], w=w)
    S.key("ecart_g", "pos", f, [-w / 2, 0], d, e)
    S.key("ecart_d", "pos", f, [w / 2, 0], d, e)
    return f + d


def _tower_step(S, kit, f, bh, toi_to, toi):
    """La tour grandit d'un cran d'un coup (blocs de bh px, 330 ms ease-out) et tremble à l'arrivée ; la pastille,
    l'accolade et « Grand plan » suivent dans les mêmes images, « Grand plan » bat ; AU MÊME INSTANT « Toi » fait un
    bond en arrière (h 20), penché en arrière, et un petit trait de poussière part de son talon. -> fin du bond."""
    D = SCALE
    set_blocks(S, f, D, "out", [tower(i, bh) for i in range(4)])
    S.key("pastille", "pos", f, list(PASTILLE_TOUR[bh]), D, "out")
    S.key("accolade", "sy", f, ACCOLADE_SY[bh], D, "out")
    S.key("gp_nom", "pos", f, list(GP_NOM_C[bh]), D, "out")
    for b in BLOC_IDS + ["pastille"]:
        kit.shake(b, f + D, amp=4, axis="x")
    kit.pulse("gp_nom", f, peak=1.15)
    end = toi.hop(f, list(toi_to), D, h=20, lean=8)          # side +1 : penché en arrière (loin de la tour)
    _ecart(S, f, D, toi_to[0])                                # l'écart au sol s'allonge avec le bond
    kit.pulse("ecart", end, peak=1.12, step=3)
    toi.hold_low(f, end)
    heel = [toi_to[0] + 52, GROUND - 6]
    marks(S, end - 1, [([heel[0] + 10, heel[1] - 14], -30), ([heel[0] + 22, heel[1]], 0)], hold=3)
    toi.lean_to(end, -6, 6)
    toi.hold_low(end, end + 7)
    return end


def _chrono(S, kit, f, pos, value, d, out):
    """La petite horloge d'une montée paraît près de « Toi » (pop) ; son secteur prend `value` minutes en d images
    (le temps de la montée) ; elle se réduit sur place à `out`."""
    S.key("chrono", "pos", f - 1, list(pos))
    S.key("chrono", "start", f - 1, 0)
    S.key("chrono", "value", f - 1, 0)
    S.key("chrono", "opacity", f - 1, 1)
    kit.pop("chrono", f, d=6)
    S.key("chrono", "value", f, value, d, "linear")
    return kit.vanish("chrono", out, d=6)


def part(S, kit, c):
    toi = c.toi
    f0 = scene_f0(S, "S09")
    kit.pin(f0 - 1, ENTRY_P2)                   # etat_initial de S09 (raccord avec p1)
    if S.val("toi", "scale", f0 - 1) == 0:      # garde-fou de la série (la figurine de V15 est visible dès l'image 0)
        toi.enter(f0 - 10, at=list(TOI_RECUL))
    p = S.val("toi", "pos", f0 - 1)
    if math.dist(p, TOI_RECUL) > 0.5:           # partie construite seule : « Toi » va à sa place d'entrée (p1 l'y laisse)
        toi.walk(f0 - 15, list(TOI_RECUL), 12, low=True)
    ends = []

    # ---------------- S09 : la tour grandit d'un coup, « Toi » recule d'un bond, « Plus tard » ----------------
    f = kit.at("S09", "Et", "les huit « ? » rentrent un à un dans leur bloc et s'y réduisent ; « Toi » se redresse, "
                            "bras baissé")
    for k, q in enumerate(Q_IDS):
        home = tower(k // 2, 100)[0]
        kit.vanish(q, f + k, into=[home[0] + (-40 if k % 2 == 0 else 40), home[1]], d=6)
    toi.lean_to(f, 0)
    toi.hold_low(f, f + POP)
    _ecart(S, f, 0, TOI_RECUL[0])               # contrôle sans son : l'écart tour -> « Toi » paraît au sol, court
    kit.pop("ecart", f + 6, d=6)

    f = kit.at("S09", "marche", "la tour grandit d'un coup (blocs de 100 à 125 px : 500 px), tremble, l'argent "
                                "monte de 100 px, « Grand plan » bat ; au même instant « Toi » recule d'un bond")
    _tower_step(S, kit, f, 125, TOI_RECUL2, toi)

    f = kit.at("S09", "repousse", "la tour grandit encore (blocs de 150 px : 600 px, sommet à y 566) ; « Toi » recule "
                                  "d'un second bond, tête basse")
    _tower_step(S, kit, f, 150, TOI_RECUL3, toi)

    f = kit.at("S09", "départ.", "le calendrier passe à « Plus tard », fond rouge, texte papier, glisse de 40 px vers "
                                 "la droite (repoussé) et bat")
    _cal(S, kit, f, "tard", RED, alert=True)
    kit.move("calendrier", f, [CAL_C[0] + CAL_TARD_DX, CAL_C[1]], MORPH)
    kit.pulse("calendrier", f + 8, peak=1.12)    # contrôle sans son : « Plus tard » bat deux fois
    kit.pulse("ecart", f + 8, peak=1.12, step=3)

    # ---------------- S10 : il tire le bloc du bas, la tour s'étale en escalier ----------------
    f = kit.at("S10", "solution,", "« Toi » revient à la tour et pose la pointe du stylo sur le bord droit du bloc "
                                   "Budget ; le bloc bat au contact")
    g = toi.walk(f, list(TOI_TIRE), 10, low=True)
    _ecart(S, f, 10, TOI_TIRE[0])               # l'écart se referme pendant qu'il revient, puis s'efface
    kit.vanish("ecart", f + 10, d=6)
    ey = GROUND - 40                            # prise basse sur le bord : à bonne distance de l'épaule une fois tiré
    edge0 = [S.val("bloc1", "pos", g)[0] + S.val("bloc1", "w", g) / 2 + 2, ey]
    hit = toi.reach(g, edge0, 8) - 1
    kit.pulse("bloc1", hit, peak=1.04)

    f = kit.at("S10", "donc", "« Toi » recule en tirant : le bord droit du bloc Budget suit la pointe du stylo, de "
                              "x 620 à 790, jusqu'à ses pieds")
    toi.walk(f, list(TOI_P0), 12)
    c1, w1 = [545, tower(0, 150)[0][1]], 490                   # bord gauche fixe (300), bord droit 620 -> 790
    S.keys("bloc1", f, 12, "inOut", pos=c1, w=w1)
    ico, nom = block_children(w1)
    S.key(BLOC_ICO[0], "pos", f, ico, 12, "inOut")
    S.key(BLOC_NOM[0], "pos", f, nom, 12, "inOut")
    for n, _ in frames(f, 12, "inOut"):         # la pointe suit le bord, image par image
        x = S.val("bloc1", "pos", n)[0] + S.val("bloc1", "w", n) / 2 + 2
        toi.reach(n, [x, ey], 1, step=False)

    f = kit.at("S10", "baisser", "toute la tour s'étale vers la gauche en escalier de 4 marches basses, marche par "
                                 "marche ; l'argent glisse au sommet ; l'accolade « Grand plan » rentre dans le "
                                 "bloc Budget")
    D = 12
    for i in range(4):
        cc, w, h = stairs(i)
        S.keys(BLOC_IDS[i], f + 3 * i, D, "inOut", pos=list(cc), w=w, h=h)
        ico, nom = block_children(w)
        S.key(BLOC_ICO[i], "pos", f + 3 * i, ico, D, "inOut")
        S.key(BLOC_NOM[i], "pos", f + 3 * i, nom, D, "inOut")
    S.key("pastille", "pos", f + 9, list(PASTILLE_ESCALIER), D, "inOut")
    kit.vanish("accolade", f, into="bloc1")
    kit.vanish("gp_nom", f, into="bloc1")
    toi.lower(f, 8)

    f = kit.at("S10", "marche.", "les quatre marches battent l'une après l'autre, de Budget à Papiers")
    kit.stagger(BLOC_IDS, f, 3, kit.pulse, peak=1.04)

    # ---------------- S11 : « Semaine 1 », la marche 1 choisie ----------------
    f = kit.at("S11", "l’inverse :", "« Plus tard » redevient neutre, revient à sa place et passe à « Semaine 1 » ; "
                                     "la pilule bat")
    _cal(S, kit, f, "s1", LIGHT, alert=False)
    kit.move("calendrier", f, list(CAL_C), MORPH)

    f = kit.at("S11", "choisis", "le stylo touche le bout de la marche Budget : un « 1 » cerclé s'y trace et la "
                                 "marche se colore en cyan pâle")
    hit = toi.tap(f - TAP + 1, list(NUM_PTS[0]))
    kit.draw("num1", hit, 8)
    kit.type("num1_txt", hit + 2)
    S.key("bloc1", "fill", hit, LIGHT, 9, "out")
    toi.lower(hit + 6, 8)

    # ---------------- S12 : il monte sur la marche 1 (lourd, lent), note « 2 » ----------------
    f = kit.at("S12", "Fais-la,", "« Toi » prend son élan en arrière, monte lourdement sur la marche 1 et vacille ; "
                                  "une petite horloge à côté de lui prend un grand secteur (c'est lent) ; son "
                                  "étiquette passe à droite de sa tête")
    toi.lean_to(f, 8, 4, "out")                 # élan : il se ramasse en arrière (4 images)
    toi.lean_to(f + 4, 0, 4, "inOut")
    end = _climb(toi, f + 4, TOI_M1, 18)
    toi.hold_low(f, f + 4)
    kit.move("nom_toi", end - 10, list(NOM_MARCHE), MOVE)   # quand il file déjà à gauche : jamais au-delà de x 940
    for k, deg in enumerate((-8, 6, 0)):        # vacille
        toi.lean_to(end + 4 * k, deg, 4, "inOut")
    toi.hold_low(end, end + 12)
    _chrono(S, kit, f + 4, (600, 870), 45, 18, end + 8)

    f = kit.at("S12", "note", "le stylo écrit « 2 » cerclé au bout de la marche Épargne ; les marches 3 et 4 restent "
                              "sans numéro")
    hit = toi.tap(f - TAP + 1, list(NUM_PTS[1]))
    kit.draw("num2", hit, 8)
    kit.type("num2_txt", hit + 2)
    toi.lower(hit + 6, 8)

    # ---------------- S13 : l'abonnement barré en 10 min (contre un week-end), marche 1 cochée ----------------
    f = kit.at("S13", "exemple,", "la carte « Abonnement inutile » (pictogramme de paiement récurrent, −9,99 € / "
                                  "mois) sort du pictogramme Budget et vole devant « Toi »")
    kit.pop("abonnement", f, from_pt=list(ABO_FROM))
    kit.move("abonnement", f, list(ABO_C), MOVE, "inOut", arc=60)

    f = kit.at("S13", "10", "l'horloge ressort du calendrier près de « Toi » dans le tour complet en tirets du "
                            "« week-end » et ne fait qu'un sixième de tour : « 10 min »")
    S.key("cadran", "start", f - 1, 0)
    S.key("cadran", "value", f - 1, 0)
    S.key("cadran", "opacity", f - 1, 1)
    S.key("cadran_txt", "scale", f - 1, 0)
    kit.pop("cadran", f, from_pt=list(CAL_C), to=list(CADRAN_TOI), d=12)
    S.key("cadran_we", "scale", f + 2, 0)       # le tour complet (week-end) paraît derrière, en tirets
    S.key("cadran_we", "scale", f + 3, 1, POP, "out")
    kit.pop("cadran_we_txt", f + 6)
    S.key("cadran", "value", f + 8, 10, 15, "linear")
    kit.pop("cadran_txt", f + 14)

    f = kit.at("S13", "résilier", "« Toi » barre la carte d'un trait de stylo en diagonale")
    end = toi.strike(f, *ABO_STRIKE, line="abonnement_trait", track="draw")
    toi.lower(end + 2, 8)

    f = kit.at("S13", "abonnement", "la carte barrée tombe en pivotant derrière l'escalier, qui la cache")
    for id in ("abonnement", "abonnement_ico", "abonnement_txt", "abonnement_prix", "abonnement_trait"):
        kit.ensure(id, "z", S.ents[id]["z"])
        S.key(id, "z", f, round(S.ents[id]["z"] - 8.6, 2))    # sous les marches (z 6) : elle passe derrière
    x, y = S.val("abonnement", "pos", f - 1)
    S.key("abonnement", "pos", f, [x - 150, y + 310], DROP_OUT, "in")   # finit cachée derrière les marches 1-2
    S.key("abonnement", "rot", f, 10, DROP_OUT, "in")
    S.key("abonnement", "scale", f + DROP_OUT, 0)                       # (zone basse réservée : pas de sortie par le bas)

    f = kit.at("S13", "inutile.", "le stylo touche la marche Budget : une coche pleine s'y trace au contact")
    hit = toi.tap(f - TAP + 1, list(COCHE_PTS[0]))
    kit.draw("coche1", hit, 6)
    toi.lower(hit + 6, 8)

    # ---------------- S14 : trois autres petites actions, chacune garée au-dessus de SA marche ----------------
    f = kit.at("S14", "Ou", "l'horloge, « 10 min » et le tour du week-end rentrent dans la pilule-calendrier")
    g = kit.vanish("cadran", f, into=list(CAL_C))
    S.key("cadran_txt", "scale", g, 0)
    kit.vanish("cadran_we", f, into=list(CAL_C))
    kit.vanish("cadran_we_txt", f, into=list(CAL_C))

    for mot, oid, what in (("virement", "opt_virement", "la carte « Virement d’épargne » sort du bout de la marche "
                                                         "Épargne et se gare juste au-dessus ; un fil tireté la relie "
                                                         "au « 2 »"),
                           ("dater", "opt_projet", "la carte « Dater un projet » sort du bout de la marche Papiers et "
                                                   "se gare juste au-dessus, reliée par un fil tireté"),
                           ("frais", "opt_frais", "la carte « Vérifier les frais » sort du bout de la marche "
                                                  "Placements et se gare au-dessus : un escalier de tâches")):
        f = kit.at("S14", mot, what)
        kit.pop(oid, f, from_pt=list(OPT_FROM[oid]))
        arr = kit.move(oid, f, list(OPT_C[oid]), MOVE, "inOut")
        kit.draw(f"{oid}_lien", arr, 8)

    # ---------------- S15 : le premier segment d'énergie, les cartes redescendent, montée sur la marche 2 --------
    f = kit.at("S15", "L’élan", "la coche de la marche 1 bat et lance un grand segment cyan (traînée) qui vole "
                                "s'emboîter dans la jauge « Énergie », qui se remplit d'un quart")
    S.key("energie", "fill", f, CYAN)
    kit.pulse("coche1", f, peak=1.3)
    arr = elan_fly(S, kit, "elan1", f, COCHE_PTS[0], ENERGIE_QUARTS[0], 0.25)

    f = kit.at("S15", "vient", "les fils se retirent ; les trois cartes redescendent en arc, l'une après l'autre, "
                               "chacune dans sa marche, qui bat à l'arrivée")
    for k, oid in enumerate(("opt_virement", "opt_frais", "opt_projet")):
        S.key(f"{oid}_lien", "draw", f, 0, 4, "in")
        g = f + 3 + 4 * k
        a = kit.move(oid, g, list(OPT_FROM[oid]), 14, "inOut", arc=40, scale=0.3)
        S.key(oid, "scale", a, 0, 2, "in")
        S.key(oid, "opacity", a + 2, 0)
        kit.pulse(BLOC_IDS[k + 1], a, peak=1.06)
        if k == 0:
            kit.pulse("num2", a, peak=1.25)
        ends.append(a + 6)

    f = kit.at("S15", "l’action,", "« Toi » monte sur la marche 2, plus vite, sans vaciller")
    ends.append(_climb(toi, f, TOI_M2, 12))

    # ---------------- S16 : marche 2 cochée, « 3 » noté, bond éclair sur la marche 3 ----------------
    f = kit.at("S16", "marche ?", "les quatre marches battent l'une après l'autre, de bas en haut")
    kit.stagger(BLOC_IDS, f, 3, kit.pulse, peak=1.04)

    f = kit.at("S16", "Parce", "le calendrier passe à « Semaine 2 » et bat")
    cal_swap(S, kit, f, T_CAL["s2"])

    f = kit.at("S16", "chaque", "le stylo touche la marche Épargne : une coche pleine s'y trace")
    hit = toi.tap(f - TAP + 1, list(COCHE_PTS[1]))
    kit.draw("coche2", hit, 6)
    toi.lower(hit + 6, 8)

    f = kit.at("S16", "réussie", "la coche bat et lance un deuxième grand segment cyan vers la jauge : moitié pleine")
    kit.pulse("coche2", f, peak=1.3)
    elan_fly(S, kit, "elan2", f, COCHE_PTS[1], ENERGIE_QUARTS[1], 0.5)

    f = kit.at("S16", "suivante", "le stylo écrit « 3 » cerclé au bout de la marche Placements")
    hit = toi.tap(f - TAP + 1, list(NUM_PTS[2]))
    kit.draw("num3", hit, 8)
    kit.type("num3_txt", hit + 2)
    toi.lower(hit + 6, 8)

    f = kit.at("S16", "facile.", "« Toi » bondit en un éclair sur la marche 3 (traits de vitesse derrière lui) ; la "
                                 "petite horloge n'a qu'un fil de secteur ; la jauge à moitié pleine bat")
    end = _climb(toi, f, TOI_M3, 6)
    p3 = S.val("toi", "pos", f + 2)
    ends.append(marks(S, f + 2, [([p3[0] + 85, p3[1] - 40], 0), ([p3[0] + 100, p3[1]], 0),
                                 ([p3[0] + 85, p3[1] + 40], 0)], hold=4))
    ends.append(_chrono(S, kit, f + 1, (TOI_M3[0] + 212, TOI_M3[1] - 155), 5, 6, f + 12))
    ends.append(kit.pulse("energie", end, peak=1.08))
    ends.append(end)
    assert max(ends) < scene_f0(S, "S17"), f"p2 : des clés débordent sur S17 ({max(ends)})"
