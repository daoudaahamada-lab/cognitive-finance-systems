"""V08, partie 1 : S01-S06, images 0-737 (accroche, annonce 1-2-3, contexte : le bas est déjà pris, le haut cyan
est le reste à vivre). 27 temps forts, 24,6 s.

ÉTAT D'ENTRÉE (image 0 = distribution, à épingler à -1) : ivoire quadrillé ; en haut au centre l'`enveloppe`
(WTH-004-01, 340 px, ENVELOPPE_C) ; la `pastille` cyan « Salaire » (260 x 84) dépasse de sa bouche en PASTILLE_S00,
DEVANT elle ; « Toi » (`c.toi`) en P1 (860, 1135), bras BAISSÉ (`low_pose`), nommé par `nom_toi` (pilule light
« Toi », enfant de la figurine). Tout le reste à l'échelle 0 (le groupe `revenus` aussi). Rien ne bouge.

Temps forts (image du mot ; kit.at peut caler ±1 sur l'attaque, ACOUSTIC_SNAP) :
S01  salaire@8  tomber.@30
S02  Mais@54  combien@60  vraiment@79  dépenser@92  mois-ci ?@109
S03  Dans@134  reste@210  3@246  étapes@255
S04  Ton@287  trompe@307  Une@339  partie@345  réservée@371  penses :@418  loyer,@435  factures,@455  crédits.@474
S05  Le@499  reste@544  revenus@581  moins@612  incontournables.@639
S06  C’est@677  reste@703

BRIEF, scène par scène (ids de la distribution entre accolades ; places = constantes du paquet) :
- S01 « salaire » : {pastille} bat une fois dans la bouche (pulse x1,12, times 1, step 3). « tomber. » : le groupe
  {revenus} (billets {salaire} 300 x 560 à 7 filets, origine au bas-centre) naît à l'échelle 0 dans
  ENVELOPPE_BOUCHE et tombe jusqu'au sol en COL_S01 en grandissant (pop from_pt + drop ou move « out » 370 ms,
  sans rebond ; le bas arrive sur y 1180) ; {pastille} descend avec lui et se pose en PASTILLE_S01 (même durée).
  « Toi » regarde (aucun geste).
- S02 « Mais » : {enveloppe} vanish (300 ms). Plus aucun PNG. « combien » : {pastille} -> PASTILLE_S02 (move 550) ;
  pendant la montée, textOp 1 -> 0 (4 images), bascule `text` T_Q_EUR, textOp -> 1 (FADE) ; {mot_salaire} (enfant
  de revenus) naît de la pastille (pop from_pt « pastille ») et se pose en MOT_SALAIRE_LOCAL. « vraiment » :
  c.toi.reach vers PANIER_S02_TIP (assert_reach(P1[0], …)) : pointe arrêtée à 30 px du bord de la colonne.
  « dépenser » : {panier} (icon cart, disque papier) pop à la pointe (`c.toi.tip(f)`), sans toucher l'argent ;
  {pastille} bat (x1,1) sur la même image. « mois-ci ? » : {pastille} shake x 6 ; le stylo reste tendu.
- S03 « Dans » : {panier} vanish into la pointe (c.toi.tip) puis `lower` (8 images). « reste » : {legende_reste}
  (deep, LEGENDE_S03) s'écrit (kit.type, 3,5 car./image). « 3 » : {marqueur} pop (on 0, lbl 0 : trois disques
  papier, aucun cyan ; un seul pop de l'entité, les disques ne se décalent pas). « étapes » : légende du repère en
  fondu (piste `lbl` 0 -> 1, FADE), « Revenus », « Charges », « Soustraire » à l'encre SemiBold (doneStyle kept).
- S04 « Ton » : {pastille} -> PASTILLE_S04 et {legende_reste} -> LEGENDE_S04 (move 550, mêmes images).
  « trompe » : {egal} « ≠ » rouge pop en EGAL_C. « Une » : {maison} (WTH-004-05) pop en MAISON_C. « partie » :
  {ligne_partie} se trace (kit.draw 9) à y 786 ; laisse-la visible ~0,9 s avant le loyer. « réservée » : {cadenas}
  pop en CADENAS_C. « penses : » : « Toi » lève le stylo (c.toi.reach vers CADENAS_TAP en ~8 images, assert_reach) ;
  au contact {cadenas} shake x 6 ; le bras retombe (`lower` 8, « out ») : subi, rien n'a bougé dans la colonne.
  « loyer, » / « factures, » / « crédits. » : chaque bloc {loyer}, {factures}, {credits} (enfants de {charges},
  groupe en PILE_S04) naît de MAISON_SORTIE (pop from_pt) puis tombe à BLOC_LOCAL[id] (drop 370 ms, sans rebond),
  devant l'argent, empilés y 990-1180, 886-990, 786-886. Le cadenas reste au-dessus (z 8).
- S05 « Le » : {maison} vanish ; {pastille} bat (x1,12). « reste » : {reste} (enfant de revenus, cyan, contour
  encre) se remplit de bas en haut : clés `h` 0 -> RESTE_S05["h"] ET `pos` reste_pos(bottom, 0) -> reste_pos(**RESTE_S05)
  sur les mêmes images (10 images « out ») après `scale` 1 instantané ; il couvre {mot_salaire}. « revenus » :
  {accolade_g} se trace (draw 9) ; {acc_revenus} naît de ACC_REVENUS_NEE (pop from_pt) et se pose en
  ACC_REVENUS_C. « moins » : {accolade_d} se trace ; {acc_charges} « − charges » pop en ACC_CHARGES_C.
  « incontournables. » : c.toi.tap(f - TAP + 1, LOYER_TAP) (contact sur le mot ; assert_reach) ; au contact
  {loyer} avance de -8 px en x, shake x 6 et revient EXACTEMENT à BLOC_LOCAL["loyer"] ; {cadenas} pulse x1,3 ;
  `lower`.
- S06 « C’est » : {egal} bascule `text` T_EG et `color` RED -> DEEP (hex, 9 images) ; pulse x1,15. « reste » :
  {legende_reste} -> LEGENDE_S06 (move 550) et `color` DEEP -> INK ; à l'arrivée {reste} bat (x1,05). Tenue.

PASSAGE À p2 (image 737 = ENTRY_P2 de __init__, à respecter exactement) : revenus en COL_S01 x1 (salaire,
mot_salaire), reste RESTE_S05 (h 166), legende_reste sur le cyan (LEGENDE_S06, encre, écrite), charges en PILE_S04
avec loyer / factures / crédits, cadenas, egal « = » deep, ligne_partie tracée (sous les blocs), accolades tracées et
leurs mots, pastille « ? € » en PASTILLE_S04 (w 260), marqueur on 0 / lbl 1 ; enveloppe, maison, panier à 0 ;
« Toi » en P1, bras baissé. Tout ce qui commence ici finit avant 738.

Règles : bras baissé entre deux gestes (`lower`) ; jamais de clé ni d'épingle sur la figurine (ni sur `nom_toi` : il
suit son parent) ; chaque geste : `assert_reach(P1[0], cible, "S0x …")`. Pas de VALIDÉ, pas de gris, un seul PNG à la
fois (l'enveloppe sort en S02, la maison entre en S04).
"""
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, SCALE  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401

from . import *  # noqa: F401,F403


PANIER_DX, PANIER_K = 24, 1.4                   # le panier (r 26 x 1,4) pend au bout du stylo : 20 px d'air


def part(S, kit, c):
    toi = c.toi

    # ---------- état d'entrée (image 0 = distribution) : épinglé à -1 ----------
    kit.pin(0 - 1, {
        "enveloppe": {"pos": list(ENVELOPPE_C), "scale": 1},
        "pastille": {"pos": list(PASTILLE_S00), "scale": 1, "text": T_SALAIRE, "w": PASTILLE_W, "textOp": 1},
        "revenus": {"pos": list(COL_S01), "scale": 0},
        "salaire": {"scale": 1},
        "mot_salaire": {"pos": list(MOT_SALAIRE_LOCAL), "scale": 0},
        "reste": {"scale": 0},
        "legende_reste": {"pos": list(LEGENDE_S03), "chars": 0, "color": DEEP},
        "panier": {"scale": 0},
        "marqueur": {"pos": [MARKER_CX, MARKER_Y], "scale": 0, "on": 0, "active": 0, "lbl": 0},
        "egal": {"pos": list(EGAL_C), "scale": 0, "text": T_NE, "color": RED},
        "maison": {"pos": list(MAISON_C), "scale": 0},
        "ligne_partie": {"draw": 0},
        "cadenas": {"pos": list(CADENAS_C), "scale": 0},
        "charges": {"pos": list(PILE_S04), "scale": 1},
        **{b: {"pos": list(BLOC_LOCAL[b]), "scale": 0} for b in ("loyer", "factures", "credits")},
        "accolade_g": {"draw": 0}, "accolade_d": {"draw": 0},
        "acc_revenus": {"pos": list(ACC_REVENUS_C), "scale": 0},
        "acc_charges": {"pos": list(ACC_CHARGES_C), "scale": 0},
    })
    if S.val(toi.id, "scale", -1) == 0:          # garde-fou (figurine absente) : sans effet ici, elle est à l'image 0
        toi.enter(0, at=list(P1))

    assert_reach(P1[0], PANIER_S02_TIP, "S02 panier")
    assert_reach(P1[0], CADENAS_TAP, "S04 cadenas")
    assert_reach(P1[0], LOYER_TAP, "S05 loyer")

    # ================= S01 : « Ton salaire vient de tomber. » =================
    f = kit.at("S01", "salaire", "la pastille cyan « Salaire » bat une fois dans la bouche de l'enveloppe")
    kit.pulse("pastille", f, peak=1.12)

    f = kit.at("S01", "tomber.", "la colonne de billets sort de l'enveloppe et tombe au sol en grandissant ; la "
                                 "pastille « Salaire » descend avec elle et se pose sur son sommet")
    kit.pop("revenus", f, from_pt=ENVELOPPE_BOUCHE, to=COL_S01, d=DROP)
    kit.move("pastille", f, PASTILLE_S01, d=DROP, e="out")

    # ================= S02 : « Mais combien peux-tu vraiment dépenser ce mois-ci ? » =================
    f = kit.at("S02", "Mais", "l'enveloppe vide se réduit vers son centre et sort")
    kit.vanish("enveloppe", f)

    f = kit.at("S02", "combien", "la pastille remonte au-dessus de la colonne et devient « ? € » ; le mot « Salaire » "
                                 "tombe d'elle sur le haut de la colonne")
    kit.move("pastille", f, PASTILLE_S02)
    S.key("pastille", "textOp", f, 0, 4, "out")
    S.key("pastille", "text", f + 4, T_Q_EUR)
    S.key("pastille", "textOp", f + 4, 1, FADE, "out")
    kit.pop("mot_salaire", f, from_pt="pastille", to=MOT_SALAIRE_LOCAL)

    f = kit.at("S02", "vraiment", "« Toi » tend son stylo vers l'argent et s'arrête à 30 px de la colonne, sans la "
                                  "toucher")
    toi.reach(f, PANIER_S02_TIP)

    f = kit.at("S02", "dépenser", "un panier de courses surgit au bout du stylo tendu, devant l'argent ; la pastille "
                                  "« ? € » bat")
    tip = toi.tip(f - 1)
    kit.pop("panier", f, scale=PANIER_K, from_pt=tip, to=[tip[0] + PANIER_DX, tip[1]])
    kit.pulse("pastille", f, peak=1.1)

    f = kit.at("S02", "mois-ci ?", "la pastille « ? € » tremble : la question reste ouverte")
    kit.shake("pastille", f, amp=6)

    # ================= S03 : « Dans cette vidéo, on va calculer ton vrai reste à vivre, en 3 étapes simples. » ======
    f = kit.at("S03", "Dans", "le panier rentre dans la pointe du stylo, puis « Toi » baisse le bras")
    g = kit.vanish("panier", f, into=toi.tip(f - 1))
    lower(toi, g - 2, 10)

    f = kit.at("S03", "reste", "sous la pastille « ? € », « reste à vivre » s'écrit en cyan profond")
    kit.type("legende_reste", f)

    f = kit.at("S03", "3", "en haut, le repère 1-2-3 surgit : trois disques papier, aucune étape allumée")
    kit.pop("marqueur", f)

    f = kit.at("S03", "étapes", "sous les disques, leurs légendes « Revenus », « Charges », « Soustraire » entrent en "
                                "fondu")
    S.key("marqueur", "lbl", f, 1, FADE, "out")

    # ================= S04 : « Ton salaire trompe un peu. Une partie est déjà réservée … : loyer, factures, crédits. »
    f = kit.at("S04", "Ton", "la pastille « ? € » et sa légende « reste à vivre » glissent à droite, en face du haut "
                             "de la colonne")
    kit.move("pastille", f, PASTILLE_S04)
    kit.move("legende_reste", f, LEGENDE_S04)

    f = kit.at("S04", "trompe", "un « ≠ » rouge surgit entre le haut de la colonne et la pastille : le salaire n'est "
                                "pas ce qu'on peut dépenser")
    kit.pop("egal", f)

    f = kit.at("S04", "Une", "la maison des charges surgit en haut à gauche")
    kit.pop("maison", f)

    f = kit.at("S04", "partie", "un trait en tirets se trace en travers de la colonne, à mi-hauteur : la partie basse")
    kit.draw("ligne_partie", f, DRAW)

    f = kit.at("S04", "réservée", "un cadenas surgit sur le bord droit de la partie basse")
    kit.pop("cadenas", f)

    f = kit.at("S04", "penses :", "« Toi » lève son stylo vers la partie basse : la pointe bute sur le cadenas, qui "
                                  "tressaille ; le bras retombe")
    g = toi.reach(f, CADENAS_TAP, d=8)
    kit.shake("cadenas", g - 1, amp=6)
    lower(toi, g + 1, 8, e="out")

    for mot, bid, what in (("loyer,", "loyer", "le bloc « Loyer » sort de la maison et tombe au pied de la colonne"),
                           ("factures,", "factures", "le bloc « Factures » sort de la maison et tombe sur le loyer"),
                           ("crédits.", "credits", "le bloc « Crédits » sort de la maison et tombe sur les factures, "
                                                   "sous le trait en tirets")):
        f = kit.at("S04", mot, what)
        kit.pop(bid, f, from_pt=MAISON_SORTIE, to=BLOC_LOCAL[bid], d=DROP)

    # ================= S05 : « Le chiffre utile, c’est ce qui reste après. Tes revenus du mois, moins … » ==========
    f = kit.at("S05", "Le", "la maison se réduit et sort ; la pastille « ? € » bat : le chiffre utile")
    kit.vanish("maison", f)
    kit.pulse("pastille", f, peak=1.12)

    f = kit.at("S05", "reste", "la partie libre du haut de la colonne se remplit de cyan, de bas en haut : ce qui reste")
    bottom, h = RESTE_S05["bottom"], RESTE_S05["h"]
    S.key("reste", "h", f - 1, 0)
    S.key("reste", "pos", f - 1, reste_pos(bottom, 0))
    S.key("reste", "scale", f, 1)
    S.key("reste", "h", f, h, SCALE, "out")
    S.key("reste", "pos", f, reste_pos(bottom, h), SCALE, "out")

    f = kit.at("S05", "revenus", "une accolade se trace le long de toute la colonne, à gauche ; « revenus » sort de la "
                                 "colonne et s'y pose")
    kit.draw("accolade_g", f, DRAW)
    kit.pop("acc_revenus", f, from_pt=ACC_REVENUS_NEE, to=ACC_REVENUS_C, d=MOVE - 4)

    f = kit.at("S05", "moins", "une seconde accolade se trace le long des seuls blocs, à droite ; « − charges » "
                               "surgit à côté")
    kit.draw("accolade_d", f, DRAW)
    kit.pop("acc_charges", f)

    f = kit.at("S05", "incontournables.", "« Toi » pousse du stylo le bloc « Loyer » : il bute, tressaille et revient "
                                          "exactement en place ; le cadenas bat")
    hit = toi.tap(f - TAP + 1, LOYER_TAP)
    lx, ly = BLOC_LOCAL["loyer"]
    S.key("loyer", "pos", hit, [lx - 8, ly], 3, "out")
    g = kit.shake("loyer", hit + 3, amp=6)
    S.key("loyer", "pos", g, [lx, ly], 5, "inOut")
    kit.pulse("cadenas", hit, peak=1.3)
    lower(toi, hit + 6, 8)

    # ================= S06 : « C’est ça, ton reste à vivre. » =================
    f = kit.at("S06", "C’est", "le « ≠ » rouge devient un « = » cyan profond et bat")
    S.key("egal", "text", f, T_EG)
    S.key("egal", "color", f, DEEP, 9, "out")
    kit.pulse("egal", f)

    f = kit.at("S06", "reste", "la légende « reste à vivre » quitte la pastille et se pose sur la partie cyan, qui bat")
    g = kit.move("legende_reste", f, LEGENDE_S06)
    S.key("legende_reste", "color", f, INK, MOVE, "inOut")
    kit.pulse("reste", g, peak=1.05)
