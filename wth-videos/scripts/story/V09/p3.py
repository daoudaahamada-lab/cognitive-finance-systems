"""V09, partie 3 : S16-S22, images 1811-2723 (étape 3 : cadenas, durée, pénalité reprise par la boîte, délai ;
le mythe « Protégé ≠ sans risque » barré par le stylo ; perdre avant l'échéance OU rien gagner à l'échéance ; chute :
rembobinage, fiche « 4 questions », la boîte qui écrit les réponses, fils « * » -> réponse, coches de « Toi » ; carte
de fin née des pilules). 31 temps forts, 30,4 s.

ÉTAT D'ENTRÉE (etat_initial de S16, épinglé à 1810 : ENTRY_P3) : une pièce en l'air au-dessus de la boîte ;
« Disponible » sous le repère ; repère sur l'étape 3 (disques 1 et 2 : pictogramme + « * ») ; barre de temps vide,
rond « Signature », calendrier, « Échéance » ; bouclier au-dessus de l'échéance ; étiquette collée ; « Toi » en P3.

Temps forts :
S16  suite ?@1859  imposent@1908  durée,@1927  pénalités@1953  sortie@1975  délai.@2005
S17  Et@2024  attention@2030  mythe :@2051  ne@2088
S18  Tu@2138  sors@2168  l’échéance,@2181  ou@2205  gagner@2219
S19  Avant@2250  signer,@2264  4@2290  Qu’est-ce@2327  Par@2365  Jusqu’à@2386  Sous@2411
S20  demande@2457  réponses@2472  écrit.@2490
S21  Quand@2514  promesse@2526  conditions@2580  vraie.@2616
S22  Abonne-toi@2643  argent.@2687

Tour de revue 1 (ce qui change) :
- S16 : « Disponible » bat et la pièce en l'air oscille (plus d'image figée) ; « suite ? » : le cadenas tombe sur la
  boîte et la pièce, qui cherchait à sortir, est ramenée dans la fente ; « imposent » : le cadenas se ferme (anneau) ;
  « pénalités » : « Toi » force le cadenas, deux pièces de 76 px sortent, il recule en P2 ; « sortie » : l'une vire au
  rouge et est aspirée par la fente, « Pénalités » (34 px) à côté d'elle ; « délai. » : l'autre roule vers « Toi »,
  bute sur un cadran dont l'aiguille fait un tour, « Délai » au-dessus ; S17 « Et » : elle rejoint enfin « Toi ».
- S17 : la barre s'écarte (elle revient en S18) ; la formule s'écrit à y 920 ; « Toi » vient en x 585 ; « ne » : son
  stylo trace le trait qui barre le « = » (Figure.strike, piste draw) ; « sans » / « risque » : trois pièces à
  l'abri devant le bouclier, une 4e glisse dessous, vire au rouge et sort.
- S18 : « sors » : le stylo touche la barre au tiers, 4 pièces sur le couvercle ; « l’échéance, » : la 4e vire au
  rouge et tombe vers l'extérieur avec « −1 » (jamais par la fente) ; « ou » : on défait la sortie (3 pièces
  rentrent, le repère s'efface) et la barre se remplit jusqu'à l'échéance ; « gagner » : le bouclier verse 4 pièces
  claires sur le couvercle, puis la 5e place en tirets (r 38) porte un « 5 % » fantôme qui bat et s'efface.
- S19 : rembobinage d'une seconde (◀◀ en taille réelle), la formule et « Disponible » rentrent dans le disque 3, la
  barre se rétracte vers « Signature » ; la fiche naît de la carte collée sur la boîte.
- S20 : plus de PNG : la boîte sort un bac à papier plat et une lèvre sur sa fente, tremble, et la fiche ressort par
  le bac ; les réponses s'écrivent une à une, chacune avec le pictogramme de l'objet qu'elle rappelle.
- S21 : fiche lisible (x 0,88) ; pilules au-dessus (y 230-410) ; trois fils deep 5 px partent des « * » vers les
  réponses (la pilule tirée descend de 6 px) ; « Toi » touche le bord de la fiche et les coches se tracent DANS la
  fiche, devant chaque réponse. Le « ? % » est revenu avec « Rendement ».
- S22 : les trois pilules se fondent en une, qui glisse jusqu'au bouton pendant que la carte grandit DERRIÈRE elle
  (outro grow_at 4) ; le titre n'entre qu'une fois le bouton en place (title_at 24).
"""
import math

from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, SCALE, STRETCH, STYLE  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401

from . import *  # noqa: F401,F403
from . import _FULL

BTN_K = round(112 / PROMESSE_H, 4)              # S22 : la pilule (h 76) à l'échelle du bouton (h 112)
TOI_RECUL_S18 = 690                             # S18 : « Toi » recule d'un pas après la sortie (stylo hors des pièces)
Q_TOI_POS = (860, 905)
LIGNE_TEXTE_DY = FICHE.ty + 2
FICHE_AST_K = 1.4
PIECE_EN_FUITE = (520, 992)                     # S16 « vraiment » : la pièce tente de filer vers « Toi »
ROULE = round(360 / (2 * math.pi * PIECE_R * PIECE_K_SORTIE), 4)   # degrés par px d'une pièce qui roule


def _r(pt):
    return [round(pt[0], 2), round(pt[1], 2)]


def _into_slot(S, kit, pid, f, d=10, arc=40, e="in"):
    """La pièce est aspirée par la fente : elle file vers la fente et s'y réduit. -> f + d."""
    g = kit.move(pid, f, list(FENTE), d=d, e=e, arc=arc)
    S.key(pid, "scale", g - 4, 0, 4, "in")
    S.key(pid, "opacity", g, 0)
    return g


def part(S, kit, c):
    toi = c.toi
    f0 = scene_f0(S, "S16")
    film_last = film_end(S)
    kit.pin(f0 - 1, {**ENTRY_P3,
                     **_FULL("promesse1_mot", T_PROMESSES[0]), **_FULL("promesse2_mot", T_PROMESSES[1]),
                     **_FULL("promesse3_mot", T_PROMESSES[2]),
                     "ficelle_etiquette": {"from": 1}, "etiq_ast": {"scale": 1}, "sous_conditions": {"opacity": 0},
                     "piece5": {"scale": 0, "fill": RED.lower()}})
    if S.val("toi", "scale", f0 - 1) == 0:      # partie construite seule : la figurine n'est pas entrée
        toi.enter(f0 - 10, at=list(P3))
        lower(toi, f0 - 2, d=1)
    elif abs(S.val("toi", "pos", f0 - 1)[0] - P3[0]) > 0.5:
        walk_low(toi, f0 - 25, P3[0], d=20)

    # ================= S16 « « Disponible », vraiment tout de suite ? Certains produits imposent … » =================
    g = S.word("Disponible", near=60.4)            # « Disponible » bat ; la pièce en l'air oscille
    kit.pulse("promesse3", g, peak=1.08)
    S.key("piece1", "pos", g, [PIECE_EXTRAITE[0], PIECE_EXTRAITE[1] - 6], 7, "inOut")
    S.key("piece1", "pos", g + 7, list(PIECE_EXTRAITE), 7, "inOut")
    v = S.word_after("vraiment", g)                # « vraiment » : elle tente de filer vers « Toi »
    kit.move("piece1", v, list(PIECE_EN_FUITE), d=12)

    f = beat(kit, "S16", 0, "un cadenas tombe sur le devant de la boîte ; la pièce qui filait vers « Toi » le heurte "
                            "et est ramenée dans la fente")
    land = kit.drop("cadenas", f, h=240, to=list(CADENAS_C))
    kit.shake("piece1", land - 4, amp=8)
    _into_slot(S, kit, "piece1", land - 1, d=10, arc=20)

    f = beat(kit, "S16", 1, "le cadenas se ferme : un anneau se trace autour de lui, il bat ; l'argent est bloqué")
    kit.draw("cadenas", f, 8, track="ring")
    kit.pulse("cadenas", f + 4, peak=1.12)

    f = beat(kit, "S16", 2, "« Durée » s'écrit au-dessus de la barre de temps, qui se remplit lentement jusqu'au tiers : "
                            "il faut attendre, le cadenas reste fermé")
    kit.type("mot_duree", f, rate=2)
    S.key("frise", "value", f, FRISE_TIERS, 36, "linear")

    f = beat(kit, "S16", 3, "« Toi » force le cadenas du stylo : il saute et tombe ; deux grosses pièces sortent de la "
                            "fente et sautent au sol ; « Toi » recule d'un pas")
    hit = toi.tap(f - TAP + 1, list(CADENAS_C))
    kit.drop("cadenas", hit, out=True, h=30, rot=30)
    for k, pid in enumerate(("piece1", "piece2")):
        g = hit + 3 * k
        S.key(pid, "pos", g - 1, list(FENTE))
        S.key(pid, "fill", g - 1, LIGHT)
        S.key(pid, "rot", g - 1, 0)
        S.key(pid, "opacity", g - 1, 1)
        kit.pop(pid, g, scale=PIECE_K_SORTIE, d=6)
        kit.move(pid, g, list(PIECES_SORTIE[k]), d=12, arc=80)
    walk_low(toi, hit + 5, P_RECUL[0], d=12)

    f = beat(kit, "S16", 4, "la pièce de droite vire au rouge et est aspirée par la fente ; « Pénalités » en rouge à "
                            "côté d'elle : le produit garde une pièce")
    S.key("piece2", "fill", f, RED, 6, "out")
    kit.pop("mot_penalites", f, to=list(MOT_PENALITES_C))
    _into_slot(S, kit, "piece2", f + 7, d=DROP, arc=60)

    f = beat(kit, "S16", 5, "un cadran « Délai » surgit devant « Toi » ; la pièce restante roule vers lui, bute sur le "
                            "cadran et recule ; l'aiguille fait un tour complet")
    kit.vanish("mot_penalites", f)
    kit.pop("horloge", f, to=list(HORLOGE_C))
    kit.pop("mot_delai", f + 2, to=list(MOT_DELAI_C))
    x0 = PIECES_SORTIE[0][0]
    g = kit.move("piece1", f + 1, [PIECE_BUTEE, PIECES_SORTIE[0][1]], d=6, e="in")
    S.key("piece1", "rot", f + 1, round((PIECE_BUTEE - x0) * ROULE, 1), 6, "in")
    kit.shake("horloge", g, amp=5)
    kit.move("piece1", g, [PIECE_BUTEE - 10, PIECES_SORTIE[0][1]], d=3, e="out")
    S.key("horloge", "value", g, 60, 10, "linear")
    end = g + 10
    assert end <= scene_f0(S, "S17") + 2, end

    # ================= S17 « Et attention au mythe : protégé ne veut pas dire sans risque. » =================
    f = beat(kit, "S17", 0, "le cadran, « Durée » et « Délai » sortent ; la pièce roule enfin jusqu'à « Toi » ; la "
                            "barre de temps s'écarte")
    for gid in ("horloge", "mot_delai", "mot_duree"):
        kit.vanish(gid, f + 3)
    p0 = S.val("piece1", "pos", f + 1)
    g = kit.move("piece1", f + 2, [690, PIECES_SORTIE[0][1]], d=8, e="out")
    S.key("piece1", "rot", f + 2, round(S.val("piece1", "rot", f + 1) + (690 - p0[0]) * ROULE, 1), 8, "out")
    kit.vanish("piece1", g, into=_r(S.val(toi.pen, "pos", g)), d=6)
    for gid in FRISE_GROUPE:
        kit.vanish(gid, f + 4)

    f = beat(kit, "S17", 1, "le bouclier quitte l'échéance et vient en arc à gauche ; « Toi » s'approche (x 585)")
    kit.move("bouclier", f, list(BOUCLIER_MYTHE), arc=80, scale=BOUCLIER_K_MYTHE)
    walk_low(toi, f, P_MYTHE[0])

    f = beat(kit, "S17", 2, "« Protégé = sans risque » s'écrit à droite du bouclier, le « = » en rouge, qui tremble : "
                            "c'est l'erreur")
    g = kit.type("mythe_g", f, rate=1.2)
    g = kit.type("mythe_egal", g, rate=1)
    g = kit.type("mythe_d", g, rate=1.2)
    kit.shake("mythe_egal", g + 1, amp=4)

    f = beat(kit, "S17", 3, "« Toi » lève le stylo jusqu'au « = » et trace lui-même le trait qui le barre : « ≠ » ; le "
                            "« = » repasse à l'encre ; le bouclier bat une fois")
    a = _r(S.to_world("mythe", BARRE_EGAL_PTS[0], f))
    b = _r(S.to_world("mythe", BARRE_EGAL_PTS[1], f))
    lead = 7
    g = toi.strike(f - lead, a, b, d=8, lead=lead, line="barre_egal", track="draw")
    S.key("mythe_egal", "color", g - 2, INK, FADE, "out")
    kit.pulse("bouclier", g, peak=round(BOUCLIER_K_MYTHE * 1.12, 4))
    lower(toi, g + 2, 9)

    s = S.word_after("sans", f + 10)              # « sans risque » : trois pièces à l'abri devant le bouclier ...
    for k, pid in enumerate(PIECES[:3]):
        h = s + 2 * k
        S.keys(pid, h - 1, pos=list(FENTE), fill=LIGHT, rot=0)
        S.key(pid, "opacity", h - 1, 1)
        kit.pop(pid, h, d=6)
        kit.move(pid, h, list(ABRI[k]), d=10, arc=50)
    r = S.word_after("risque", s)                 # ... et une 4e glisse dessous, vire au rouge et sort
    S.keys("piece4", r - 1, pos=[BOUCLIER_MYTHE[0], BOUCLIER_MYTHE[1] + 30], fill=LIGHT, rot=0)
    S.key("piece4", "opacity", r - 1, 1)
    kit.pop("piece4", r, d=5)
    g = kit.move("piece4", r + 2, list(GLISSE), d=9, e="in")
    S.key("piece4", "fill", r + 4, RED, 6, "out")
    kit.drop("piece4", g, out=True, h=70, dx=-14, rot=-30)

    # ================= S18 « Tu peux perdre si tu sors avant l'échéance, ou ne rien gagner du tout. » =================
    f = beat(kit, "S18", 0, "la formule monte se centrer en plus petit ; les pièces abritées rentrent dans la fente ; "
                            "la barre revient (son tiers cyan) et le bouclier retourne au-dessus de l'échéance")
    kit.move("mythe", f, list(MYTHE_S18), scale=MYTHE_K_S18)
    for k, pid in enumerate(PIECES[:3]):
        _into_slot(S, kit, pid, f + 2 * k, d=10, arc=30)
    for gid, k in (("frise", 1), ("signature", SIGNATURE_K_FRISE), ("mot_signature", 1), ("calendrier", 1),
                   ("mot_echeance", 1)):
        kit.pop(gid, f + 6, scale=k)
    kit.move("bouclier", f + 4, list(BOUCLIER_ECHEANCE), arc=60, scale=BOUCLIER_K_ECHEANCE)

    f = beat(kit, "S18", 1, "« Toi » touche la barre au bout du tiers cyan, avant l'échéance : un repère encre y "
                            "reste ; 4 pièces sortent de la fente et se rangent sur le couvercle")
    hit = toi.tap(f - TAP + 1, list(FRISE_TAP))
    kit.draw("repere", hit, 6)
    last = hit
    for k in range(4):
        pid = PIECES[k]
        g = hit + 2 * k
        S.keys(pid, g - 1, pos=list(FENTE), fill=LIGHT, rot=0)
        S.key(pid, "opacity", g - 1, 1)
        kit.pop(pid, g, scale=1, d=6)
        last = kit.move(pid, g, list(COUVERCLE[k]), d=10, arc=60)
    walk_low(toi, hit + 6, TOI_RECUL_S18, d=8)

    f = beat(kit, "S18", 2, "le calendrier et le bouclier tremblent, hors d'atteinte ; la pièce de droite vire au "
                            "rouge et tombe vers l'extérieur, à droite de la boîte, avec « −1 » : perdue")
    kit.shake("calendrier", f, amp=6)
    kit.shake("bouclier", f, amp=6)
    g = max(f + 2, last)
    S.key("piece4", "fill", g, RED, 5, "out")
    kit.drop("piece4", g + 4, out=True, h=250, dx=115, rot=40)
    kit.pop("moins1", g + 5)

    f = beat(kit, "S18", 3, "on défait la sortie : les 3 pièces rentrent dans la fente, le repère et « −1 » "
                            "s'effacent ; la barre se remplit jusqu'à l'échéance")
    for k, pid in enumerate(PIECES[:3]):
        _into_slot(S, kit, pid, f + k, d=7, arc=24)
    kit.draw("repere", f, 6, to=0)
    kit.vanish("moins1", f)
    S.key("frise", "value", f + 3, 1, 11, "inOut")

    f = beat(kit, "S18", 4, "à l'échéance, le bouclier bat et verse 4 pièces claires sur le couvercle (la perdue "
                            "comprise) ; une 5e place en tirets s'ouvre au bout du rang : un « 5 % » fantôme y bat et "
                            "s'efface ; « rien gagné » s'écrit")
    kit.pulse("bouclier", f, peak=round(BOUCLIER_K_ECHEANCE * 1.18, 4))
    src = _r(S.val("bouclier", "pos", f))
    land = f
    for k, pid in enumerate(PIECES[:4]):
        h = f + 2 + k
        S.keys(pid, h - 1, pos=list(src), fill=LIGHT, rot=0)
        S.key(pid, "opacity", h - 1, 1)
        kit.pop(pid, h, scale=1, d=5)
        land = kit.move(pid, h, list(COUVERCLE[k]), d=9, arc=70)
    kit.pop("place_gain", land - 1)
    kit.pop("fantome", land + 1, d=6)
    kit.pulse("fantome", land + 8, peak=1.12)
    S.key("fantome", "opacity", land + 12, 0, 6, "linear")
    S.key("fantome", "scale", land + 18, 0)
    kit.type("rien_gagne", land + 1, rate=2.5)

    # ================= S19 « Avant de signer, pose 4 questions. Qu'est-ce qui est garanti ? Par qui ? … » ==========
    f = beat(kit, "S19", 0, "un grand ◀◀ surgit : tout se rembobine pendant une seconde ; les 4 pièces et la pièce des "
                            "frais reviennent en arc à la pile ; la formule et « Disponible » rentrent dans le disque 3 "
                            "(son « * ») ; la barre se vide ; « Toi » recule à droite")
    kit.pop("rembobiner", f)
    kit.pulse("rembobiner", f + 12, peak=1.1)
    for gid in ("place_gain", "rien_gagne"):
        kit.vanish(gid, f + 8)
    kit.move("mythe", f, list(DISQUES[2]), d=14, scale=0.08)
    S.key("mythe", "opacity", f + 14, 0)
    S.key("mythe", "scale", f + 14, 0)
    kit.vanish("promesse3", f + 2, into=list(DISQUES[2]), d=12)
    S.key("marqueur", "icon2", f + 12, 1, 5, "out")
    S.key("marqueur", "done2", f + 14, 1, POP, "out")
    S.key("frise", "value", f, 0, 20, "inOut")
    S.keys("piece5", f - 1, pos=list(PIECE_FRAIS_SOL), fill=LIGHT, rot=0)
    S.key("piece5", "opacity", f - 1, 1)
    kit.pop("piece5", f, scale=1, d=6)
    for k, pid in enumerate(PIECES):
        kit.move(pid, f + 2 * k, list(PILE[k]), d=24, arc=70)
    walk_low(toi, f, P1[0], d=20)

    f = beat(kit, "S19", 1, "la barre se rétracte vers « Signature », qui rentre avec le calendrier, « Échéance » et "
                            "le bouclier ; la carte collée sur la boîte s'en décolle, monte et grandit en fiche "
                            "« 4 questions » aux lignes vides ; le ◀◀ s'éteint")
    sig = list(SIGNATURE_FRISE)
    S.key("frise", "w", f, 0, 10, "in")
    S.key("frise", "pos", f, [FRISE_X0, FRISE_Y], 10, "in")
    S.key("frise", "scale", f + 10, 0)
    for gid in ("calendrier", "bouclier"):
        kit.vanish(gid, f, into=sig, d=10)
    for gid in ("mot_echeance", "mot_signature"):
        S.key(gid, "opacity", f, 0, FADE, "linear")
        S.key(gid, "scale", f + FADE, 0)
    kit.vanish("signature", f + 6, d=6)
    kit.morph(["etiquette"], ["fiche"], f)
    kit.vanish("rembobiner", max(f + 14, scene_f0(S, "S19") + 30))

    f = beat(kit, "S19", 2, "un « ? » sort de la tête de « Toi » et se divise en quatre « ? » qui volent se poser sur "
                            "les puces des quatre lignes ; la fiche bat")
    S.key("q_toi", "gs", f - 1, 90)
    g = kit.pop("q_toi", f, from_pt=list(TOI_TETE["P1"]), to=list(Q_TOI_POS), d=POP)
    kit.pulse("fiche", f, peak=1.04)
    for q in Q_LIGNES:
        S.key(q, "pos", g - 1, list(Q_TOI_POS))
    kit.morph(["q_toi"], Q_LIGNES, g, d=6, pair=False)
    for k, q in enumerate(Q_LIGNES):
        h = g + 2 + 3 * k
        kit.move(q, h, _r(S.to_world("fiche", [FICHE.x["bullet"], FICHE.rows[k] + LIGNE_TEXTE_DY], h)), d=MOVE,
                 arc=40)

    for k in range(4):
        what = [f"ligne 1 : son « ? » devient la puce bouclier et « {T_QUESTIONS[0]} » s'écrit",
                f"ligne 2 : puce immeuble et « {T_QUESTIONS[1]} » s'écrit",
                f"ligne 3 : puce calendrier et « {T_QUESTIONS[2]} » s'écrit",
                f"ligne 4 : puce « * » (les conditions) et « {T_QUESTIONS[3]} » s'écrit"][k]
        f = beat(kit, "S19", 3 + k, what)
        kit.vanish(Q_LIGNES[k], f, d=6)
        S.key(c.lignes[k], "bulletOn", f + 2, 1, POP, "out")
        kit.type(c.lignes[k], f + 2, rate=3.5)
        if k == 3:
            S.key("fiche_ast", "pos", f + 1, [FICHE.x["bullet"], FICHE.rows[3] + LIGNE_TEXTE_DY + 10])
            kit.pop("fiche_ast", f + 2, scale=FICHE_AST_K)

    # ================= S20 « Et demande les réponses par écrit. » =================
    f = beat(kit, "S20", 0, "« Toi » touche le coin bas droit de la fiche : elle rapetisse et descend dans la fente de "
                            "la boîte")
    hit = toi.tap(f - TAP + 1, list(FICHE_TAP))
    g = kit.move("fiche", hit, [FENTE[0], FENTE[1] - 45], d=10, scale=0.2)
    kit.vanish("fiche", g, into=list(FENTE), d=5)
    lower(toi, hit + 6)

    f = beat(kit, "S20", 1, "la boîte sort un bac à papier plat par-dessous et une lèvre sur sa fente, puis tremble "
                            "deux fois : elle écrit")
    kit.pop("bac", f, d=MORPH)
    kit.pop("levre", f + 2, d=MORPH)
    g = kit.shake("produit", f + MORPH, amp=4, axis="y")
    kit.shake("produit", g + 2, amp=4, axis="y")

    f = beat(kit, "S20", 2, "la fiche ressort par le bac et remonte à sa place ; ses réponses s'écrivent une à une, "
                            "chacune avec le pictogramme de son objet (« hors frais », « Émetteur », « Échéance », "
                            "« Pénalités »)")
    kit.pop("fiche", f, scale=1, from_pt=list(BAC_C), to=list(FICHE_C), d=MOVE)
    for k, rid in enumerate(REPONSES):
        kit.pop(rid, f + 6 + 3 * k)

    # ================= S21 « Quand une promesse paraît simple, ce sont les conditions qui la rendent vraie. » =======
    f = beat(kit, "S21", 0, "le bac et la lèvre rentrent ; la fiche se cale un peu plus bas (x 0,88, lisible) ; "
                            "« Toi » avance d'un pas")
    kit.vanish("bac", f)
    kit.vanish("levre", f)
    kit.move("fiche", f, list(FICHE_S21), scale=FICHE_K_S21)
    walk_low(toi, f, TOI_S21, d=10)

    f = beat(kit, "S21", 1, "les trois promesses ressortent des disques du repère, qui s'efface, et se rangent l'une "
                            "sous l'autre au-dessus de la fiche avec leurs marques (« Rendement » avec son « ? % ») ; "
                            "un reflet les balaie")
    for k, pid in enumerate(PROMESSES):
        S.key(pid, "rot", f + 3 * k - 1, 0)
        S.key(pid, "opacity", f + 3 * k - 1, 1)
        kit.pop(pid, f + 3 * k, scale=1, from_pt=list(DISQUES[k]), to=list(PROMESSES_S21[k]), d=MOVE)
    S.key("pastille", "opacity", f + 2, 1)
    S.key("pastille", "rot", f + 2, -12)
    kit.pop("pastille", f + 3, scale=PASTILLE_K_PILL, from_pt=list(DISQUES[1]), to=list(PASTILLE_S21), d=MOVE)
    kit.vanish("marqueur", f + 2, d=POP)
    S.key("reflet_promesses", "pos", f, list(PROMESSES_S21[1]))
    S.key("reflet_promesses", "p", f + 6 + MOVE - 1, 0)
    S.key("reflet_promesses", "p", f + 6 + MOVE, 1, 12, "inOut")

    f = beat(kit, "S21", 2, "trois fils cyan profond partent des « * » des promesses et vont se nouer à leurs "
                            "réponses écrites (Capital garanti -> hors frais, Rendement -> Échéance, Disponible -> "
                            "Pénalités) ; chaque pilule descend un peu, tirée par son fil")
    for k, (wid, pid, r) in enumerate(zip(FICELLES, PROMESSES, FICELLE_VERS)):
        h = kit.draw(wid, f + 3 * k, 9)
        x, y = PROMESSES_S21[k]
        S.key(pid, "pos", h, [x, y + 6], 4, "out")
        if pid == "promesse2":
            S.key("pastille", "pos", h, [PASTILLE_S21[0], PASTILLE_S21[1] + 6], 4, "out")
        kit.pulse(REPONSES[r], h, peak=1.1)
    kit.pulse("fiche", f + 18, peak=round(FICHE_K_S21 * 1.03, 4))

    f = beat(kit, "S21", 3, "« Toi » touche le bord droit de la fiche : quatre coches pleines se tracent DANS la fiche, "
                            "devant les quatre réponses attachées ; aucune coche sur les promesses")
    hit = toi.tap(f - TAP + 1, list(FICHE_S21_TAP))
    for k, cid in enumerate(COCHES):
        kit.draw(cid, hit + 1 + 3 * k, 6)
    end = lower(toi, hit + 6)
    assert end <= scene_f0(S, "S22"), end

    # ================= S22 « Abonne-toi pour comprendre ton argent. » =================
    glide = MOVE
    outs = ["fiche", *FICELLES, *PIECES, "nom_toi", "produit", "etiquette"]
    btn_at, title_at = 6 + glide, 6 + glide + 2
    out = kit.outro("S22", outs=outs, btn_at=btn_at, press="argent.", pos=FIN_C, clear="fade",
                    bsize=round(PROMESSE_SIZE * BTN_K, 1), grow_at=4, title_at=title_at)
    f = out["card"]
    S.set(out["cursor"], opacity=0)
    for pid in ("promesse1", "promesse3", "pastille"):   # les pilules 1 et 3 et le « ? % » se fondent dans la 2
        kit.move(pid, f, list(PROMESSES_S21[1]), d=MORPH, e="inOut")
        S.key(pid, "opacity", f + 3, 0, MORPH - 3, "linear")
        S.key(pid, "scale", f + MORPH, 0)
    for cid in ("promesse2_icone", "promesse2_mot", "ast2"):
        S.key(cid, "opacity", f, 0, 4, "out")
    kit.pulse("promesse2", f + 2, peak=1.1)
    kit.ensure("promesse2", "z", S.ents["promesse2"]["z"])
    S.key("promesse2", "z", f, 41)
    S.key("promesse2", "text", f + 8, T_ABONNER)
    S.key("promesse2", "textOp", f + 8, 1, FADE, "out")
    S.key("promesse2", "w", f + 6, round(380 / BTN_K, 2), glide, "inOut")
    kit.move("promesse2", f + 6, list(FIN_BUTTON), d=glide, e="inOut", scale=BTN_K)
    S.key("promesse2", "opacity", f + btn_at, 0)

    fp = out["press"]
    toi.set_z(fp - TAP - 12, S.ents[toi.id]["z"], tool_z=44)
    hit = toi.tap(fp - TAP + 1, list(FIN_TAP))
    for k in range(2):
        ring(S, f"fin_onde{k + 1}", hit + 4 * k, d=14, s0=0.6, s1=2.0)
    end = lower(toi, hit + 6, 8)
    assert hit == fp and end < film_last and hit + 4 + 14 < film_last, (hit, fp, end)
