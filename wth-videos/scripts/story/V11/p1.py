"""V11, partie 1 : S01-S08, images 0-822 (27 temps forts, 27,4 s). Accroche, contexte, étape 1 « Famille ».

ÉTAT D'ENTRÉE : l'image 0 (distribution de `cast`), qui est l'etat_initial de S01 : fiche « Fiche client » (690, 565),
5 rangées écrites à l'encre, pastille « mars 2023 » sur l'en-tête (566, 365, échelle 0,76) ; « Toi » en TOI_HOME
(820, 1135) avec sa pilule « Toi », BRAS BAISSÉ dès l'image 0 (`toi.hold_low` / `toi.lower(0, 1)`, puis `lower`
entre deux gestes) ; la moitié gauche vide. Rien à épingler (pas de kit.pin) : la partie commence au film.
SORTIE : ENTRY_P2 à l'image 822 (voir __init__.py). Tout ce que cette partie commence finit avant 823.

Ids : fiche, fiche_L1-L5, fiche_hl1-5, q_ligne1-5, eclair, cadre, punaise, pastille, pastille_rouge, toi (+ bras,
stylo), nom_toi, client, nom_client, info (+ info_etoile, info_mot, info_anneau), eclat_info, vie_disque1-3,
fil_vie1-3, marqueur, evt_disque, eclat_evt, vie, conseil, conseil_rouge, conseil_fil, question, bulle1.

BRIEF, scène par scène (temps forts : kit.at(scène, mot) ; écrire dans `what` ce qu'on voit) :
- S01 (0-132) « meilleure » : `info` pop en INFO_C0 + `eclat_info` (p 0 -> 1, 9 images). « client » : client.enter
  (frm=CLIENT_FROM_X, à CLIENT_C, face à « Toi ») avec sa pilule (enfant). « dans » : `info` file (move ease-in, 9 im.)
  jusqu'à INFO_BUMP (bord gauche à 465, contre la fiche). « dossier. » : kit.shake("fiche", x, 6) et `info` rebondit
  à INFO_BACK (POP, out) ; aucune rangée ne change. « Elle » : `info` vole en arc 80 jusqu'à INFO_CLIENT. « vie. » :
  kit.draw("info_anneau") + client.lean_to(5°, TILT) vers elle (puis revient à 0 avant S02 « vie »).
- S02 (133-267) « changements » : kit.morph("info", vie_disque1-3) pairs 1 -> 3 : les disques naissent en
  INFO_CLIENT et s'écartent vers DISQUES_S02 (décalés de 2 images). « vie » : client.hop(12 px, 8 im.) + kit.pulse des
  3 disques. « revoir. » : kit.draw fil_vie1-3 (décalés de 3) ; à l'arrivée de chacun, kit.shake de sa rangée (L1,
  L3, L4 ; 4 px) et sa puce flash (piste flash 1 puis 0, ~6 images).
- S03 (268-322) « question » : toi.reach vers la pointe (705, 1000) (assert_reach OK depuis TOI_HOME) ; `question`
  pop sous la pointe (gs Q_GS_S03) et `bulle1` grandit autour (scale 0 -> 1, SCALE) ; client.lean_to vers la bulle
  (5°, droite). « remonter. » : les 3 disques glissent vers DISQUES_S03 (MOVE, décalés de 2 ; les fils raccourcissent
  d'eux-mêmes, ancrés au disque) ; à l'arrivée, flash des 3 puces.
- S04 (323-383) « problème, » : kit.vanish("question", into=toi.tip) et `bulle1` se réduit avec ; kit.shake("fiche",
  x, 6) ; les 3 disques renvoyés à DISQUES_S04 (MOVE 12 im., out) pendant que fil_vie1-3 se retirent (piste from
  0 -> 1, 9 im.) ; « Toi » baisse le bras. « fiche » : kit.draw("cadre") (300 ms ; l'aplat paraît à la fermeture).
  « figée. » : kit.drop("punaise") en PUNAISE_C ; au contact, kit.shake("cadre", y, 4) et "fiche" (y, 4).
- S05 (384-466) « photo » : `eclair` p 0 -> 1 (12 im.) ; le contour du cadre clignote deep 2 images (hex) puis encre.
  « date. » : kit.move("pastille", PASTILLE_PHOTO, scale=1) (MOVE).
- S06 (467-517) « vie, » : `vie` naît sur la pastille (pop from_pt=pastille) et glisse à VIE_C (MOVE). « continue. » :
  bascules de la piste text de `vie` toutes les 5 images : T_MARS24, T_MARS25, T_NOV ; client.hop sur place.
- S07 (518-656) « conseil » : toi.reach(CONSEIL_SPAWN) ; `conseil` pop sous la pointe puis kit.move à CONSEIL_C ;
  le bras se rebaisse. « fondé » : kit.draw("conseil_fil") (9 im.). « dépassée » : kit.fade("pastille_rouge", to=1)
  + kit.shake("pastille", 6) ; kit.pulse("vie"). « inadapté. » : kit.fade("conseil_rouge", to=1) ; rot 0 -> 8 (TILT) ;
  conseil_fil sag 0 -> 30.
- S08 (657-822) « Pourquoi » : les 3 disques volent en arc vers MARKER_XS (y 200) et se réduisent dans le repère
  pendant que `marqueur` grandit (scale 0 -> 1, on reste 0) : relais (morph) ; légendes grises. « famille ? » :
  S.key("marqueur", "on", f, 1, POP) ; L1, L2 surlignées : fiche_hl1-2 opacity 0 -> 1 et slotFill 1 -> 0 (6 im.).
  « seul » : `evt_disque` part du disque 1 (MARKER_XS[0], 200) et tombe à EVT_C (kit.drop to=EVT_C ou pop from_pt +
  move DROP). « tout » : `eclat_evt` p 0 -> 1 (12 im.) + kit.shake("fiche", x, 8) deux fois. « question. » :
  kit.stagger q_ligne1-5 kit.pop, 2 images d'écart ; les « ? » restent à l'encre (rien ne rougit en S08).

RACCORD vers p2 : l'image 822 doit valoir ENTRY_P2 (marqueur on 1, active 0 ; L1-L2 surlignées ; 5 « ? » ; disque-
événement en EVT_C ; pastille et conseil rouges ; vie « nov. 2026 » ; conseil penché, fil sag 30 ; « Toi » en
TOI_HOME bras baissé ; client en CLIENT_C, lean 0).
"""
from . import *  # noqa: F401,F403
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, SCALE, TILT  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401

LEAN_CLIENT = 5                                 # S01 « vie. », S03 « question » : le client se tourne vers l'info / la bulle
Q_S03 = (705, 1000)                             # S03 : la pointe du stylo levé
Q_BULLE = (BULLE1_C[0] - 6, BULLE1_C[1] - 4)    # S03 : le « ? » glisse de la pointe au centre de la bulle
SAG_FIL1 = -55                                  # S02 : le fil personne -> Famille passe AU-DESSUS du disque immeuble
MARKER_DISC_K = 0.55                            # S08 : un disque de la vie (r 36) se réduit à la taille d'un disque du
                                                # repère (r 20) en y arrivant


def flash(S, kit, id, f, up=2, down=4):
    """La puce de la rangée `id` grossit de 35 % puis revient (piste flash). -> f + up + down."""
    kit.ensure(id, "flash", 0)
    S.key(id, "flash", f, 1, up, "out")
    S.key(id, "flash", f + up, 0, down, "inOut")
    return f + up + down


def part(S, kit, c):
    toi, client = c.toi, c.client
    rows = c.rows                                   # fiche_L1 … fiche_L5
    disques = [f"vie_disque{k + 1}" for k in range(3)]
    fils = [f"fil_vie{k + 1}" for k in range(3)]
    reliees = [rows[i] for i in DISQUES_ROWS]       # L1, L3, L4

    # ---------- état d'entrée (image 0 = etat_initial de S01 : la distribution) ----------
    kit.pin(0 - 1, {
        "fiche": {"pos": list(FICHE_C), "scale": 1},
        "pastille": {"pos": list(PASTILLE_HEAD), "scale": PASTILLE_HEAD_K},
        "cadre": {"draw": 0}, "punaise": {"scale": 0},
        "info": {"pos": list(INFO_C0), "scale": 0},
        "vie": {"scale": 0}, "conseil": {"scale": 0}, "marqueur": {"scale": 0, "on": 0},
        "evt_disque": {"scale": 0}, "question": {"scale": 0}, "bulle1": {"scale": 0},
    })
    toi.lower(0, 1)                                 # « Toi » bras baissé dès l'image 0, stylo à la hanche

    # ================= S01 : « La meilleure info sur ton client n’est pas dans son dossier. Elle est dans sa vie. »
    f = kit.at("S01", "meilleure", "la pilule cyan « Info » (étoile) surgit au milieu de la gauche, avec un éclat de "
                                   "8 rayons deep : une information précieuse")
    kit.pop("info", f)
    S.key("eclat_info", "p", f, 1, POP, "out")

    f = kit.at("S01", "client", "le client (figurine papier, pilule « Client ») entre en marchant depuis le bord "
                                "gauche jusqu'en bas à gauche, face à « Toi »")
    client.enter(f, at=CLIENT_C, frm=CLIENT_FROM_X, d=16)

    f = kit.at("S01", "dans", "la pilule « Info » file vers la fiche et bute contre son bord gauche")
    kit.move("info", f, INFO_BUMP, d=9, e="in")

    f = kit.at("S01", "dossier.", "au contact, la fiche tremble et repousse la pilule « Info », qui rebondit vers la "
                                  "gauche ; aucune rangée de la fiche ne change")
    kit.shake("fiche", f, 6)
    kit.move("info", f, INFO_BACK, d=POP, e="out")

    f = kit.at("S01", "Elle", "la pilule « Info » vole en arc et se pose au-dessus du client")
    kit.move("info", f, INFO_CLIENT, arc=80)

    f = kit.at("S01", "vie.", "un anneau deep se trace autour de la pilule « Info » ; le client s'incline vers elle : "
                              "elle est à lui")
    kit.draw("info_anneau", f, DRAW)
    client.lean_to(f, LEAN_CLIENT, TILT)

    # ================= S02 : « … les changements de vie qui doivent tout faire revoir. » =================
    f = kit.at("S02", "changements", "la pilule « Info » se divise en trois disques cyan (personne, immeuble, euro) "
                                     "qui s'écartent en éventail au-dessus du client ; il se redresse")
    kit.vanish("info", f, d=MORPH)
    for k, did in enumerate(disques):
        kit.pop(did, f + 2 * k, from_pt=INFO_CLIENT, to=DISQUES_S02[k], d=MORPH)
    client.lean_to(f, 0, TILT)

    f = kit.at("S02", "vie", "le client fait un petit bond sur place et les trois disques battent au-dessus de lui : "
                             "ces changements lui arrivent")
    client.hop(f, CLIENT_C, 8, h=12)
    for did in disques:
        kit.pulse(did, f)

    f = kit.at("S02", "revoir.", "de chaque disque part un fil deep vers la puce de sa rangée (Famille, Travail, "
                                 "Patrimoine) ; à l'arrivée, la rangée tremble et sa puce grossit : à revoir")
    S.set(fils[0], sag=SAG_FIL1)
    for k, (fid, row) in enumerate(zip(fils, reliees)):
        g = kit.draw(fid, f + 3 * k, DRAW)
        kit.shake(row, g, 4)
        flash(S, kit, row, g)

    # ================= S03 : « Et la question qui les fait remonter. » =================
    f = kit.at("S03", "question", "« Toi » lève le stylo : un « ? » sort de la pointe et une bulle grandit autour, "
                                  "queue vers sa tête ; le client lève la tête vers la bulle")
    tip0 = toi.tip(f - 1)
    toi.reach(f, list(Q_S03), d=9)
    kit.pop("question", f, from_pt=tip0, to=list(Q_BULLE))     # sort de la pointe, se pose au centre de la bulle
    kit.pop("bulle1", f + 3, d=SCALE)
    client.lean_to(f, LEAN_CLIENT, TILT)

    f = kit.at("S03", "remonter.", "les trois disques remontent le long de leurs fils jusqu'au bord gauche de la "
                                   "fiche, chacun à côté de sa rangée, dont la puce s'allume")
    for k, (did, row) in enumerate(zip(disques, reliees)):
        g = kit.move(did, f + 2 * k, DISQUES_S03[k])
        if k == 0:
            S.key(fils[0], "sag", f, 0, MOVE, "inOut")     # fil raccourci : plus besoin de contourner        flash(S, kit, row, g - 2)

    # ================= S04 : « Le problème, c’est la fiche figée. » =================
    f = kit.at("S04", "problème,", "la bulle et son « ? » rentrent dans le stylo ; la fiche tremble et renvoie les "
                                   "trois disques au-dessus du client pendant que leurs fils se retirent")
    tip = toi.tip(f - 1)
    kit.vanish("question", f, into=tip)
    g = kit.vanish("bulle1", f, into=tip)
    kit.shake("fiche", f, 6)
    for k, (did, fid) in enumerate(zip(disques, fils)):
        kit.move(did, f, DISQUES_S04[k], d=12, e="out")
        S.key(fid, "from", f, 1, 9, "out")
        S.key(fid, "draw", f + 9, 0)                # fil rentré : effacé (raccord p2 : draw 0)
    toi.lower(g, 8)
    client.lean_to(g, 0, TILT)

    f = kit.at("S04", "fiche", "un cadre de photo papier, à marge basse large, se trace derrière la fiche")
    kit.draw("cadre", f, DRAW)

    f = kit.at("S04", "figée.", "une punaise cyan tombe sur le milieu du bord haut du cadre ; au contact, le cadre et "
                                "la fiche tremblent : la fiche est une photo épinglée")
    hit = kit.drop("punaise", f, h=150, to=PUNAISE_C)
    kit.shake("cadre", hit, 4, axis="y")
    kit.shake("fiche", hit, 4, axis="y")

    # ================= S05 : « Un dossier client est une photo prise à une date. » =================
    f = kit.at("S05", "photo", "un éclair blanc balaie la photo-fiche en diagonale ; le contour du cadre clignote en "
                               "cyan profond, comme au déclenchement")
    S.key("eclair", "p", f, 1, 12, "inOut")
    S.key("cadre", "stroke", f, DEEP)
    S.key("cadre", "stroke", f + 2, INK)

    f = kit.at("S05", "date.", "la pastille « mars 2023 » quitte l'en-tête et descend dans la marge basse du cadre en "
                               "grandissant : c'est la date de la photo")
    kit.move("pastille", f, PASTILLE_PHOTO, scale=1)

    # ================= S06 : « La vie, elle, continue. » =================
    f = kit.at("S06", "vie,", "une copie de la pastille « mars 2023 » sort d'elle et glisse au-dessus du client : la "
                              "date de sa vie")
    g = kit.pop("vie", f, from_pt="pastille", to=list(PASTILLE_PHOTO), d=4)
    kit.move("vie", g, VIE_C)

    f = kit.at("S06", "continue.", "la date de la vie défile : « mars 2024 », « mars 2025 », « nov. 2026 » ; le client "
                                   "fait un pas sur place ; sous la photo, la pastille reste à « mars 2023 »")
    for k, t in enumerate((T_MARS24, T_MARS25, T_NOV)):
        S.key("vie", "text", f + 5 * k, t)
    client.hop(f, CLIENT_C, 8, h=12)

    # ================= S07 : « Et un conseil fondé sur une situation dépassée peut devenir inadapté. » ======
    f = kit.at("S07", "conseil", "« Toi » tend le stylo vers le sol : la pilule « Ton conseil » sort de la pointe et "
                                 "glisse entre lui et le client ; il baisse le bras")
    tip0 = toi.tip(f - 1)
    g = toi.reach(f, list(CONSEIL_SPAWN), d=9)
    kit.pop("conseil", f, from_pt=tip0, to=list(CONSEIL_SPAWN))
    kit.move("conseil", g, CONSEIL_C, d=12)
    toi.lower(g, 8)

    f = kit.at("S07", "fondé", "un fil deep se trace du haut de « Ton conseil » jusqu'au bas du cadre-photo : le "
                               "conseil repose sur la fiche")
    kit.draw("conseil_fil", f, DRAW)

    f = kit.at("S07", "dépassée", "le contour de la pastille « mars 2023 » passe au rouge et elle tremble ; la date de "
                                  "la vie « nov. 2026 » bat : la fiche est dépassée")
    kit.fade("pastille_rouge", f, to=1)
    kit.shake("pastille", f, 6)
    kit.pulse("vie", f)

    f = kit.at("S07", "inadapté.", "le contour de « Ton conseil » passe au rouge, la pilule penche et son fil se "
                                   "détend : le conseil n'est plus adapté")
    kit.fade("conseil_rouge", f, to=1)
    S.key("conseil", "rot", f, CONSEIL_TILT, TILT, "out")
    kit.ensure("conseil_fil", "sag", 0)
    S.key("conseil_fil", "sag", f, 30, TILT, "out")

    # ================= S08 : « Pourquoi commencer par la famille ? … peut tout remettre en question. » ======
    f = kit.at("S08", "Pourquoi", "les trois disques de la vie volent en arc vers le haut et se fondent dans le repère "
                                  "1-2-3 légendé « Famille », « Travail », « Patrimoine », qui grandit")
    for k, did in enumerate(disques):
        g = kit.move(did, f + 2 * k, (MARKER_XS[k], MARKER_Y), arc=60)
        S.key(did, "scale", f + 2 * k + 6, MARKER_DISC_K, 10, "inOut")
        kit.vanish(did, g, d=4)
    kit.pop("marqueur", f + 8, d=MORPH)

    f = kit.at("S08", "famille ?", "l'étape 1 « Famille » s'allume en cyan ; les rangées Famille et Enfants de la "
                                   "fiche se surlignent")
    S.key("marqueur", "on", f, 1, POP, "out")
    for i in (0, 1):
        S.key(f"fiche_hl{i + 1}", "opacity", f, 1, 6, "out")
        S.key(rows[i], "slotFill", f, 0, 6, "out")

    f = kit.at("S08", "seul", "un disque « famille » se détache du repère et tombe dans la vie du client")
    kit.drop("evt_disque", f, h=EVT_C[1] - MARKER_Y, dx=MARKER_XS[0] - EVT_C[0], to=EVT_C)
    S.key("evt_disque", "scale", f - 1, 0.72)
    S.key("evt_disque", "scale", f, 1, DROP, "out")

    f = kit.at("S08", "tout", "un éclat deep part du disque-événement et toute la fiche tremble, deux fois")
    S.key("eclat_evt", "p", f, 1, 12, "out")
    S.key("eclat_evt", "p", f + 12, 0)              # éclat fini (invisible à 1 comme à 0) : raccord p2, p 0
    g = kit.shake("fiche", f, 8)
    kit.shake("fiche", g + 1, 8)

    f = kit.at("S08", "question.", "un « ? » encre se pose devant chacune des 5 rangées de la fiche, l'un après "
                                   "l'autre : toute la fiche est remise en question")
    kit.stagger([f"q_ligne{i + 1}" for i in range(5)], f, 2, kit.pop)
