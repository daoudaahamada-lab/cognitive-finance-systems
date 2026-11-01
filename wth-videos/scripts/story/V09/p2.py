"""V09, partie 2 : S08-S15, images 906-1810 (étape 1 : le garant vide, trois garants, le bouclier qui suit le garant
fissuré, l'astérisque de la garantie, la pièce des frais qui traverse le bouclier, la barre de temps et l'échéance ;
étape 2 : le « 5 % » géant, cadre court OU cadre long, passé / futur en plein cadre, « boosté » puis « ? % » ;
relais de l'étape 3, la pièce extraite). 31 temps forts, 30,2 s.

ÉTAT D'ENTRÉE (etat_initial de S08, épinglé à 905 : ENTRY_P2) : bouclier cyan r 62 sur la boîte, étiquette collée
(x 0,42, un grand « * ») ; « Capital garanti » (coche ronde) sous le repère ; repère `on` 1 sur l'étape 1 (disques 2
et 3 : pictogrammes % et horloge) ; rond « Signature » rentré ; 5 pièces dans la boîte ; « Toi » en P3, bras baissé.

Temps forts :
S08  « Capital@906  mais@944  qui ?@974
S09  assureur,@1003  banque,@1026  émetteur.@1045  celui@1119  donne.@1135
S10  Et@1155  parfois@1177  hors@1194  seulement@1226  précise.@1252
S11  Vient@1282  chiffre@1305  attire@1322
S12  annoncé,@1397  mais@1438  période ?@1458
S13  Un@1483  passé@1501  prédit@1515  futur.@1532
S14  taux@1569  « boosté »@1582  quelques@1625  conditions.@1658
S15  Reste@1689  quotidien :@1741  récupérer@1764  argent.@1787

Tour de revue 1 (ce qui change) :
- S08 : le fil monte du bouclier jusqu'à une place vide (cercle en tirets) dans la silhouette ; le « ? » s'y pose.
- S09 : noms des garants AU-DESSUS des immeubles, le fil arrive à leur pied ; à « émetteur. » le fil balaie encore
  les trois garants avant de se fixer (n'importe lequel) ; « garantie » : le bouclier bat ; « vaut » : une onde deep
  court le long du fil jusqu'à l'émetteur, dont le nom bat ; « celui » : l'émetteur se fissure et vacille (lean_to,
  plus de clé directe), le bouclier rétrécit et tremble ; « donne. » : il se redresse, la fissure s'efface, le
  bouclier revient à sa taille d'origine (pas au-dessus).
- S10 « parfois » : le bouclier remonte de 40 px et couvre la fente ; « hors » : la pièce monte À TRAVERS le
  bouclier (dessinée devant), vire au rouge en le traversant, une onde fantôme de 2 images, une encoche reste au
  bord du bouclier ; elle tombe sous « hors frais ». « seulement » : le rond « Signature » renaît au départ de la
  barre élargie (640 px), qui s'étire jusqu'au calendrier ; le bouclier de la boîte n'est plus qu'un contour en
  tirets. « précise. » : un curseur court de « Signature » à « Échéance » pendant que le contour en tirets le suit ;
  au contact de l'échéance, le bouclier redevient plein.
- S12 : cadre court (deep) et cadre long (encre), pleins 6 px à aplat cyan clair, 180 et 760 px de large ; le
  « 5 % » saute dans le cadre court (« mais »), puis dans le long, et alterne entre les deux ; « ? » à côté.
- S13 : barre, bouclier et boîte sortent ; graphique plein cadre (x 150-900, y 480-980), légendes 34 px, futurs
  5 px, « 5 % » de 90 px posé d'abord au point « aujourd'hui », « ? » au bout des futurs.
- S14 : le cadre court revient ; la bande « boosté » le remplit (173 x 44) pendant que le « 5 % » roule dessus et
  s'arrête net à son bord ; « ↑ boosté » centré sur la bande ; « quelques » : le reste de la barre passe en tirets ;
  « conditions. » : le « 5 % » descend de la bande sur les tirets et devient « ? % » avec son « * ».
- S15 : le « ? % » reste accroché à « Rendement » et rentre avec elle dans le disque 2 (pictogramme %).
"""
from pipeline.story import DRAW, FADE, MORPH, MOVE, POP, SCALE, STRETCH  # noqa: F401
from pipeline.story_kit import TAP

from . import *  # noqa: F401,F403
from . import (BOITE_TAP, BOOST_PILL_C, BOOST_X0, BOOST_X1, BOUCLIER_BOITE, BOUCLIER_COUVERCLE, BOUCLIER_ECHEANCE,
               BOUCLIER_K_ECHEANCE, BOUCLIER_K_FAIBLE, BOUCLIER_R0, BOUCLIER_TAP, BRANCHES, CAL_C, CREUX_C, DISQUES,
               ENTRY_P2, FENTE, FIL_BAS, FIL_HAUT, FRISE_C, FRISE_GROUPE, FRISE_W, FRISE_X0, FRISE_X1, FRISE_Y,
               GARANT_PILLS, GARANTS_C, HORS_FRAIS_C, LIGHT, MOT_ECHEANCE_C, MOT_SIGNATURE_FRISE, P1, P2, P3, PAPER,
               PASTILLE_ANNONCE, PASTILLE_CENTRE, PASTILLE_K_ANNONCE, PASTILLE_K_CENTRE, PASTILLE_K_FRISE,
               PASTILLE_K_GRAPHE, PASTILLE_K_PILL, PASTILLE_K_QPCT, PASTILLE_ROND, PIECE_EXTRAITE, PIECE_FRAIS_SOL,
               PROMESSE_POINT, Q_FRISE_C, Q_FUTUR_C, RED, SIGNATURE_FRISE, SIGNATURE_K_FRISE, SILHOUETTE_C, T_Q_PCT,
               APRES_X0, AUJOURDHUI, CADRE_COURT_C, CADRE_LONG_C, ETIQ_COLLEE_K, FIL_HAUT_S08, MOT_SIGNATURE_FRISE,
               assert_reach, beat, hold_low, lower, scene_f0, walk_low)

PANIER_TIP_BAS = (535, 1062)         # S15 : pointe tendue près de la boîte ; le panier au-dessus
PANIER_POS = [535, 1012]
TOI_ATTIRE = -6                      # S11 « attire » : penché vers le « 5 % »
PIECE_HAUT = (300, 968)              # S10 « hors » : la pièce traverse le bouclier jusqu'ici
PASTILLE_COURT = [CADRE_COURT_C[0], FRISE_Y]          # S12 : le « 5 % » dans le cadre court
PASTILLE_LONG = [640, FRISE_Y]                        # S12 : le « 5 % » sur la durée entière (cadre long)
PASTILLE_DEPART = [BOOST_X0 + 36, FRISE_Y]            # S14 « taux » : au début de la bande
PASTILLE_ARRET = [BOOST_X1, FRISE_Y]                  # S14 « boosté » : arrêt net au bord de la bande
PASTILLE_TIRETS = [570, FRISE_Y]                      # S14 « conditions. » : sur la partie en tirets
PASTILLE_PILL = [790, PROMESSE_POINT[1]]              # S15 : accrochée au bout droit de « Rendement »
RIDE = 14                            # S14 : durée du trajet sur la bande (ease-in : arrêt net)


def _r(pt):
    return [round(pt[0], 3), round(pt[1], 3)]


def _shield_top(k, c=BOUCLIER_BOITE):
    return [c[0], round(c[1] - BOUCLIER_R0 * k, 3)]


def _fil(S, track, f, v, d=0, e="out"):
    """Même clé sur le fil des garants et sur son onde (même tracé)."""
    for wid in ("fil_garant", "fil_onde"):
        S.key(wid, track, f, v, d, e)


def _stretch(S, id, f, x0, c, w, d=STRETCH, e="out"):
    """Barre ou bande qui s'étire depuis son bord gauche x0 (pistes `w` et `pos` ensemble). -> f + d."""
    S.key(id, "w", f - 1, 0)
    S.key(id, "pos", f - 1, [x0, c[1]])
    S.key(id, "scale", f - 1, 1)
    S.key(id, "w", f, w, d, e)
    S.key(id, "pos", f, list(c), d, e)
    return f + d


def _x_cross(x0, x1, xc, d, f, e="inOut"):
    """Image où un trajet x0 -> x1 (d images, assouplissement e) dépasse xc."""
    def ease(p):
        if e == "in":
            return p ** 3
        return 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2
    return f + next((k for k in range(d) if x0 + (x1 - x0) * ease((k + 1) / d) >= xc), d - 1)


def part(S, kit, c):
    toi = c.toi
    f0 = scene_f0(S, "S08")
    kit.pin(f0 - 1, ENTRY_P2)
    if S.val("toi", "scale", f0 - 1) == 0:      # partie construite seule : la figurine n'est pas entrée
        toi.enter(f0 - 10, at=list(P3))
        lower(toi, f0 - 2, d=1)
    elif abs(S.val("toi", "pos", f0 - 1)[0] - P3[0]) > 0.5:
        walk_low(toi, f0 - 25, P3[0], d=20)

    # ================= S08 « « Capital garanti » : mais garanti par qui ? » =================
    f = beat(kit, "S08", 0, "la pilule « Capital garanti » sous le repère bat deux fois")
    kit.pulse("promesse1", f, times=2, step=3, peak=1.1)

    f = beat(kit, "S08", 1, "« Toi » touche du stylo le bord droit du bouclier : un fil encre monte du bouclier "
                            "jusqu'à une place vide (cercle en tirets) au cœur d'une silhouette d'immeuble en tirets")
    hit = toi.tap(f - TAP + 1, list(BOUCLIER_TAP))
    kit.draw("fil_garant", hit, DRAW)
    kit.draw("silhouette", hit, DRAW)
    kit.pop("creux", hit + 5)
    lower(toi, hit + 6)

    f = beat(kit, "S08", 2, "un « ? » naît au point touché du bouclier et monte se poser dans la place vide, au bout "
                            "du fil ; la silhouette tremble : personne ne tient le bouclier")
    kit.pop("q_garant", f, from_pt=list(BOUCLIER_TAP), d=6)
    arr = kit.move("q_garant", f + 3, list(CREUX_C), arc=60)
    kit.shake("silhouette", arr, amp=6)
    kit.pulse("creux", arr, peak=1.15)

    # ================= S09 « Un assureur, une banque, un émetteur. La garantie vaut ce que vaut celui qui la donne. »
    f = beat(kit, "S09", 0, "le « ? » et la place vide deviennent un immeuble « Assureur » ; la silhouette s'efface ; "
                            "le fil aboutit à son pied, son nom au-dessus")
    kit.vanish("q_garant", f)
    kit.vanish("creux", f)
    c.assureur.enter(f, at=list(GARANTS_C[0]))
    kit.draw("silhouette", f, 6, to=0)
    S.key("silhouette", "scale", f + 6, 0)
    kit.pop(GARANT_PILLS[0], f + 3)
    _fil(S, "pb", f, list(FIL_HAUT[0]), 10, "inOut")

    f = beat(kit, "S09", 1, "un 2e immeuble « Banque » surgit à droite ; le bout du fil glisse jusqu'à lui")
    c.banque.enter(f, at=list(GARANTS_C[1]))
    kit.pop(GARANT_PILLS[1], f + 3)
    _fil(S, "pb", f, list(FIL_HAUT[1]), 10, "inOut")

    f = beat(kit, "S09", 2, "un 3e immeuble « Émetteur » surgit ; le fil glisse jusqu'à lui, balaie encore les trois "
                            "garants et se fixe sur l'émetteur : n'importe lequel peut tenir le bouclier")
    c.emetteur.enter(f, at=list(GARANTS_C[2]))
    kit.pop(GARANT_PILLS[2], f + 3)
    _fil(S, "pb", f, list(FIL_HAUT[2]), 10, "inOut")
    for k, tgt in enumerate((0, 1, 2)):
        _fil(S, "pb", f + 12 + 8 * k, list(FIL_HAUT[tgt]), 8, "inOut")
    g = S.word_after("garantie", f)                   # « La garantie vaut » : le bouclier bat
    kit.pulse("bouclier", g, peak=1.08)
    v = S.word_after("vaut", g)                       # « vaut » : une onde court le long du fil jusqu'à l'émetteur
    S.key("fil_onde", "draw", v, 1, 12, "inOut")
    S.key("fil_onde", "from", v + 4, 1, 12, "inOut")
    S.key("fil_onde", "draw", v + 16, 0)
    S.key("fil_onde", "from", v + 16, 0)
    kit.pulse(GARANT_PILLS[2], v + 12, peak=1.12)

    f = beat(kit, "S09", 3, "l'émetteur relié au fil se fissure et vacille ; dans les mêmes images le bouclier "
                            "rétrécit et tremble ; l'assureur et la banque ne bougent pas")
    kit.draw("fissure", f, 6)
    c.emetteur.lean_to(f, 14, d=4)
    c.emetteur.lean_to(f + 4, 20, d=3)
    c.emetteur.lean_to(f + 7, 8, d=3)
    c.emetteur.lean_to(f + 10, 14, d=3)
    S.key("bouclier", "scale", f, BOUCLIER_K_FAIBLE, SCALE, "out")
    _fil(S, "pa", f, _shield_top(BOUCLIER_K_FAIBLE), SCALE, "out")
    kit.shake("bouclier", f + 4, amp=6)
    kit.shake("bouclier", f + 8, amp=5)

    f = beat(kit, "S09", 4, "l'émetteur se redresse, sa fissure s'efface ; le bouclier revient exactement à sa taille "
                            "d'origine")
    c.emetteur.lean_to(f, 0, d=SCALE)
    kit.draw("fissure", f, 6, to=0)
    S.key("bouclier", "scale", f, 1, SCALE, "out")
    _fil(S, "pa", f, list(FIL_BAS), SCALE, "out")

    # ================= S10 « Et elle s'entend parfois hors frais, ou seulement à une date précise. » =================
    f = beat(kit, "S10", 0, "les trois garants et leurs noms se réduisent, le fil rentre ; « Toi » recule à droite, "
                            "bras baissé")
    for g in c.garants:
        g.exit(f)
    S.key("fissure", "scale", f, 0)
    for pid in GARANT_PILLS:
        kit.vanish(pid, f)
    S.key("fil_garant", "from", f, 1, 6, "in")
    S.key("fil_garant", "scale", f + 6, 0)
    S.key("fil_onde", "scale", f, 0)
    walk_low(toi, f, P1[0], d=20)

    f = beat(kit, "S10", 1, "un astérisque « * » surgit au bout de « Capital garanti » ; le bouclier remonte et "
                            "couvre la fente de la boîte comme un couvercle")
    kit.pop("ast1", f)
    kit.move("bouclier", f, list(BOUCLIER_COUVERCLE), d=10)

    f = beat(kit, "S10", 2, "une pièce monte À TRAVERS le bouclier, qui ne la retient pas : elle vire au rouge en le "
                            "traversant, une onde fantôme, une encoche reste au bord ; elle tombe au sol sous « hors "
                            "frais » en rouge")
    S.key("piece5", "pos", f - 1, [BOUCLIER_COUVERCLE[0], BOUCLIER_COUVERCLE[1] + 30])
    S.key("piece5", "fill", f - 1, LIGHT)
    S.key("piece5", "rot", f - 1, 0)
    kit.pop("piece5", f, d=4)
    S.key("piece5", "pos", f, list(PIECE_HAUT), 9, "out")
    S.key("piece5", "fill", f + 2, RED, 6, "out")
    S.key("onde_bouclier", "pos", f + 2, list(BOUCLIER_COUVERCLE))
    S.key("onde_bouclier", "scale", f + 2, 1)
    S.key("onde_bouclier", "opacity", f + 2, 0.8)
    S.key("onde_bouclier", "opacity", f + 4, 0)
    kit.pop("encoche", f + 4, d=4)
    kit.move("piece5", f + 9, list(PIECE_FRAIS_SOL), d=12, arc=70)
    kit.pop("hors_frais", f + 14, to=list(HORS_FRAIS_C))

    f = beat(kit, "S10", 3, "le rond « Signature » renaît à gauche et une barre de temps large s'étire de lui jusqu'à "
                            "un calendrier « Échéance » ; le bouclier de la boîte n'est plus qu'un contour en tirets")
    S.key("signature", "pos", f - 1, list(SIGNATURE_FRISE))
    kit.pop("signature", f, scale=SIGNATURE_K_FRISE, d=6)
    S.keys("mot_signature", f - 1, pos=list(MOT_SIGNATURE_FRISE), chars=0)
    S.key("mot_signature", "scale", f - 1, 1)
    S.key("mot_signature", "opacity", f - 1, 1)
    kit.type("mot_signature", f + 2, rate=3)
    g = _stretch(S, "frise", f + 4, FRISE_X0, FRISE_C, FRISE_W, d=10)
    kit.pop("calendrier", g - 3)
    kit.type("mot_echeance", g, rate=3)
    kit.morph(["bouclier"], ["bouclier_vide"], f + 2)

    f = beat(kit, "S10", 4, "un curseur court sur la barre de « Signature » à « Échéance » ; le contour en tirets du "
                            "bouclier le suit en arc ; au contact de l'échéance, le bouclier redevient plein, au-dessus "
                            "du calendrier")
    S.key("curseur", "pos", f - 1, list(SIGNATURE_FRISE))
    kit.pop("curseur", f, d=4)
    S.key("curseur", "pos", f, list(CAL_C), 16, "inOut")
    kit.move("bouclier_vide", f, list(BOUCLIER_ECHEANCE), d=16, arc=90, scale=BOUCLIER_K_ECHEANCE)
    hit = f + 16
    S.key("bouclier_vide", "scale", hit, 0)
    S.key("bouclier", "pos", hit - 1, list(BOUCLIER_ECHEANCE))
    S.key("bouclier", "opacity", hit, 1)
    kit.pop("bouclier", hit, scale=BOUCLIER_K_ECHEANCE, d=6)
    kit.pulse("calendrier", hit, peak=1.15)
    S.key("onde_bouclier", "pos", hit, list(BOUCLIER_ECHEANCE))
    S.key("onde_bouclier", "scale", hit, BOUCLIER_K_ECHEANCE)
    S.key("onde_bouclier", "opacity", hit, 1)
    S.key("onde_bouclier", "scale", hit, BOUCLIER_K_ECHEANCE * 1.4, 8, "out")
    S.key("onde_bouclier", "opacity", hit + 2, 0, 6, "linear")

    # ================= S11 « Vient ensuite le chiffre qui attire l'œil : le rendement. » =================
    f = beat(kit, "S11", 0, "repère : le disque actif glisse sur 2, le 1 garde son « * » (vu, sous conditions) ; "
                            "« Capital garanti » rentre dans le disque 1 pendant que « Rendement » et sa pastille "
                            "« 5 % » ressortent du disque 2 ; la pièce rouge, « hors frais » et le curseur sortent")
    kit.step(f, 1)
    S.key("marqueur", "done0", f + 6, 1, POP, "out")
    kit.vanish("promesse1", f, into=list(DISQUES[0]), d=12)
    S.key("marqueur", "icon0", f + 10, 1, 5, "out")
    S.key("marqueur", "icon1", f, 0, 6, "out")
    kit.pop("promesse2", f, from_pt=list(DISQUES[1]), to=list(PROMESSE_POINT), d=MOVE)
    kit.pop("pastille", f, scale=1, from_pt=list(DISQUES[1]), to=list(PASTILLE_ROND), d=MOVE)
    for gid in ("piece5", "hors_frais", "curseur"):
        kit.vanish(gid, f)

    f = beat(kit, "S11", 1, "la pastille « 5 % » se détache, se redresse et descend au centre en grandissant : un "
                            "énorme « 5 % »")
    kit.move("pastille", f, list(PASTILLE_CENTRE), scale=PASTILLE_K_CENTRE)
    S.key("pastille", "rot", f, 0, MOVE, "inOut")

    f = beat(kit, "S11", 2, "« Toi » avance vers le « 5 % », bras baissé, et reste penché vers lui : attiré")
    g = walk_low(toi, f, P2[0], d=10)
    toi.lean_to(g, TOI_ATTIRE, d=POP)
    hold_low(toi, g, g + POP)
    kit.pulse("promesse2", S.word_after("rendement", f), peak=1.08)   # « le rendement. » : plus d'image figée

    # ================= S12 « Un rendement annoncé, d'accord, mais sur quelle période ? » =================
    f = beat(kit, "S12", 0, "le « 5 % » rapetisse et se pose au-dessus du début de la barre de temps ; « Toi » se "
                            "redresse")
    kit.move("pastille", f, list(PASTILLE_ANNONCE), scale=PASTILLE_K_ANNONCE)
    toi.lean_to(f, 0, d=POP)
    hold_low(toi, f, f + POP)

    f = beat(kit, "S12", 1, "un cadre court plein (cyan profond, aplat cyan clair) se trace autour du début de la "
                            "barre ; le « 5 % » saute dedans")
    kit.draw("cadre_court", f, DRAW)
    g = kit.move("pastille", f + 3, PASTILLE_COURT, d=10, arc=40, scale=PASTILLE_K_FRISE)
    kit.pulse("cadre_court", g, peak=1.05)

    f = beat(kit, "S12", 2, "un cadre long plein (encre, aplat cyan clair) se trace autour de toute la barre ; le "
                            "« 5 % » saute du cadre court au cadre long et revient, deux fois ; un « ? » entre eux")
    kit.draw("cadre_long", f, DRAW)
    hops = [PASTILLE_LONG, PASTILLE_COURT, PASTILLE_LONG]
    g = f + 1
    for k, tgt in enumerate(hops):
        g = kit.move("pastille", g, tgt, d=8, arc=46)
        kit.pulse("cadre_long" if tgt is PASTILLE_LONG else "cadre_court", g - 1, peak=1.03, step=2)
    kit.pop("q_frise", f + 4, to=list(Q_FRISE_C))

    # ================= S13 « Un rendement passé ne prédit pas le futur. » =================
    f = beat(kit, "S13", 0, "la barre, ses cadres, le bouclier et la boîte sortent ; le « 5 % » file droit au point "
                            "« aujourd'hui » ; de grands axes en L se tracent, « passé » et « futur » s'écrivent "
                            "dessous ; le « ? » glisse au bout des futurs")
    for gid in (*FRISE_GROUPE, "cadre_court", "cadre_long", "bouclier", "produit", "etiquette"):
        kit.vanish(gid, f)
    kit.move("pastille", f, list(AUJOURDHUI), scale=PASTILLE_K_GRAPHE, d=12)
    kit.draw("axes", f + 4, DRAW)
    kit.type("mot_passe", f + 8, rate=1.5)
    kit.type("mot_futur", f + 8, rate=1.5)
    kit.move("q_frise", f, list(Q_FUTUR_C), scale=0.8)

    f = beat(kit, "S13", 1, "la courbe du passé monte en dents de scie jusqu'au « 5 % » posé à aujourd'hui")
    kit.draw("courbe_passe", f, 14, e="linear")
    kit.pulse("pastille", f + 14, peak=round(PASTILLE_K_GRAPHE * 1.1, 4))

    f = beat(kit, "S13", 2, "un trait vertical en tirets (aujourd'hui) coupe le graphique sous le « 5 % »")
    kit.draw("aujourdhui", f, DRAW)

    f = beat(kit, "S13", 3, "trois chemins en tirets partent du « 5 % » : vers le haut, à plat, vers le bas ; le « ? » "
                            "bat à leur bout")
    kit.stagger(BRANCHES, f, 3, kit.draw, DRAW)
    kit.pulse("q_frise", f + 9, peak=0.95)

    # ================= S14 « Et un taux « boosté » peut ne valoir que quelques mois, et sous conditions. » ==========
    f = beat(kit, "S14", 0, "le graphique se replie ; la barre, le bouclier et la boîte reviennent ; le cadre court "
                            "se retrace ; le « 5 % » se pose au début de la barre, dans le cadre court")
    for gid in ("axes", "courbe_passe", "aujourdhui", *BRANCHES, "mot_passe", "mot_futur", "q_frise"):
        kit.vanish(gid, f)
    for gid, k in (("frise", 1), ("signature", SIGNATURE_K_FRISE), ("mot_signature", 1), ("calendrier", 1),
                   ("mot_echeance", 1), ("bouclier", BOUCLIER_K_ECHEANCE), ("produit", 1),
                   ("etiquette", ETIQ_COLLEE_K)):
        kit.pop(gid, f + 2, scale=k)
    for cid in ("cadre_court", "cadre_long"):
        S.key(cid, "scale", f + 3, 1)
        S.key(cid, "opacity", f + 3, 1)
        S.key(cid, "draw", f + 3, 0)
    kit.draw("cadre_court", f + 4, DRAW)
    kit.move("pastille", f, PASTILLE_DEPART, scale=PASTILLE_K_FRISE)

    f = beat(kit, "S14", 1, "une bande cyan remplit le cadre court pendant que le « 5 % » roule dessus et s'arrête "
                            "net à son bord ; « ↑ boosté » surgit, centré sur la bande")
    _stretch(S, "boost", f, BOOST_X0, [(BOOST_X0 + BOOST_X1) / 2, FRISE_Y], BOOST_X1 - BOOST_X0, d=RIDE, e="in")
    g = kit.move("pastille", f, PASTILLE_ARRET, d=RIDE, e="in")
    kit.shake("pastille", g, amp=5)
    kit.pulse("cadre_court", g, peak=1.04)
    kit.pop("boost_pill", f + 4, to=list(BOOST_PILL_C))

    f = beat(kit, "S14", 2, "après le cadre court, le reste de la barre jusqu'à l'échéance passe en tirets : "
                            "personne ne dit ce qu'il vaudra")
    kit.draw("apres", f, 12, e="linear")

    f = beat(kit, "S14", 3, "le « 5 % » descend de la bande sur les tirets : il pâlit, devient « ? % » et reçoit "
                            "un « * » ; il tremble")
    x0 = S.val("pastille", "pos", f - 1)[0]
    kit.move("pastille", f, PASTILLE_TIRETS, d=12, arc=50, scale=PASTILLE_K_QPCT)
    g = _x_cross(x0, PASTILLE_TIRETS[0], APRES_X0 + 10, 12, f)
    S.key("pastille", "fill", g, PAPER, FADE, "out")
    S.key("pastille_mot", "opacity", g - 2, 0, 4, "in")
    S.key("pastille_mot", "text", g + 2, T_Q_PCT)
    S.key("pastille_mot", "opacity", g + 2, 1, FADE, "out")
    h = kit.pop("pastille_ast", f + 12, d=6)
    kit.shake("pastille", h, amp=6)

    # ================= S15 « Reste la promesse la plus concrète au quotidien : récupérer ton argent. » ============
    f = beat(kit, "S15", 0, "repère : le disque actif glisse sur 3, le 2 reçoit son « * » ; bande, cadres et tirets "
                            "s'effacent ; le « ? % » s'accroche au bout de « Rendement » et rentre avec elle dans le "
                            "disque 2 ; « Disponible » ressort du disque 3")
    kit.step(f, 2)
    S.key("marqueur", "done1", f + 6, 1, POP, "out")
    for bid in ("boost", "boost_pill"):
        kit.vanish(bid, f)
    for sid in ("cadre_court", "cadre_long", "apres"):
        kit.draw(sid, f, 6, to=0)
        S.key(sid, "scale", f + 6, 0)
    g = kit.move("pastille", f, PASTILLE_PILL, d=10, arc=60, scale=PASTILLE_K_PILL)
    kit.vanish("promesse2", g, into=list(DISQUES[1]), d=10)
    kit.vanish("pastille", g, into=list(DISQUES[1]), d=10)
    S.key("marqueur", "icon1", g + 8, 1, 5, "out")
    S.key("marqueur", "icon2", f + 6, 0, 6, "out")
    kit.pop("promesse3", f + 6, from_pt=list(DISQUES[2]), to=list(PROMESSE_POINT), d=MOVE)

    f = beat(kit, "S15", 1, "« Toi » s'approche de la boîte en levant le stylo ; un panier de courses surgit au "
                            "bout de la pointe et y reste")
    assert_reach(P3[0], PANIER_TIP_BAS, "S15 panier")
    walk_low(toi, f, P3[0], d=10)
    toi.reach(f + 1, list(PANIER_TIP_BAS), d=9, step=False)
    kit.pop("panier", f + 4, from_pt=_r(toi.tip(f + 3)), to=list(PANIER_POS))

    f = beat(kit, "S15", 2, "le stylo descend toucher le coin de la boîte ; le panier se réduit dans la main")
    assert_reach(P3[0], BOITE_TAP, "S15 boîte")
    hit = toi.tap(f - TAP + 1, list(BOITE_TAP))
    kit.vanish("panier", hit, into=_r(S.val(toi.pen, "pos", hit + 3)), d=4)
    lower(toi, hit + 6)

    f = beat(kit, "S15", 3, "une pièce sort de la fente de la boîte et monte en arc vers « Toi », où elle reste en "
                            "l'air")
    S.key("piece1", "pos", f - 1, list(FENTE))
    S.key("piece1", "fill", f - 1, LIGHT)
    kit.pop("piece1", f, d=6)
    end = kit.move("piece1", f, list(PIECE_EXTRAITE), arc=60)
    assert end <= scene_f0(S, "S16"), end
