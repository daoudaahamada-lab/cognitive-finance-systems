"""V11, partie 1 : S01-S08, images 0-822 (27 temps forts, 27,4 s). Accroche, contexte, étape 1 « Famille ».

ÉTAT D'ENTRÉE : l'image 0 (distribution de `cast`), qui est l'etat_initial de S01 : fiche « Fiche client » (690, 565),
5 rangées écrites à l'encre, pastille « mars 2023 » sur l'en-tête (566, 365, échelle 0,76) ; « Toi » en TOI_HOME
(820, 1135) avec sa pilule « Toi », BRAS BAISSÉ dès l'image 0 ; la moitié gauche vide. Rien à épingler.
SORTIE : ENTRY_P2 à l'image 822 (voir __init__.py). Tout ce que cette partie commence finit avant 823.

Tour de revue 1 :
- S01 « dossier. » : la fiche tremble fort (14 px), un éclat ROUGE jaillit de son bord gauche au point de contact et
  la pilule « Info » est repoussée loin (MOVE), penchée de 8° ; « vie. » : l'anneau se trace lentement (24 images)
  pendant que le client s'incline vers elle ; puis « vidéo » (l'info bat) et « voir » (le client s'incline encore) :
  plus de longue image figée au début de S02.
- S01 « client » : le client est hors champ à f - 1 et franchit le bord sur le mot (marche ease-out).
- S02 « revoir. » : fils TIRETÉS qui s'arrêtent 40 px avant les puces ; les rangées tremblent (6 px) et leur puce bat.
- S03 : (correction après le contrôle sans son) plus de bulle « ? » : « Toi » lève le stylo vers la fiche, il ne
  regarde qu'elle ; la question n'est posée qu'en S20-S21 (la morale). Plus de « × » rouge en S01 ni en S04 ; la
  pilule « Info » reste au-dessus du client jusqu'en S08.
- S04 « figée. » : grosse punaise (r 24, reflet), chute + secousse.
- S05 « photo » : flash blanc sur toute la photo (0,85 puis 0), éclair, contour qui clignote ; « date. » : la pastille
  passe SOUS la fiche (z 7) en descendant : elle ne couvre plus les rangées.
- S07 « conseil » : la pilule naît à gauche du buste de « Toi » (pointe en CONSEIL_SPAWN) et glisse en CONSEIL_C
  (470, 1200), à 100 px du stylo au repos ; « inadapté. » : le fil se détend de 60 px.
"""
from . import *  # noqa: F401,F403
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, SCALE, TILT  # noqa: F401
from pipeline.story_kit import TAP, r3  # noqa: F401

LEAN_CLIENT = 5                                 # S01 « vie. » : le client se tourne vers l'info
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
        "evt_disque": {"scale": 0}, "question": {"scale": 0},
    })
    toi.lower(0, 1)                                 # « Toi » bras baissé dès l'image 0, stylo à la hanche

    # ================= S01 : « La meilleure info sur ton client n’est pas dans son dossier. Elle est dans sa vie. »
    f = kit.at("S01", "meilleure", "la pilule cyan « Info » (étoile) surgit au milieu de la gauche, avec un éclat de "
                                   "8 rayons deep : une information précieuse")
    kit.pop("info", f)
    S.key("eclat_info", "p", f, 1, POP, "out")

    f = kit.at("S01", "client", "le client (figurine papier, pilule « Client ») entre en marchant depuis le bord "
                                "gauche jusqu'en bas à gauche, face à « Toi »")
    S.key("client", "pos", f - 1, [CLIENT_FROM_X, CLIENT_C[1]])     # hors champ à f - 1 (buste x -121 à -3)
    S.key("client", "scale", f - 1, 1)
    if S.val("client", "opacity", f - 1) < 1:
        S.key("client", "opacity", f - 1, 1)
    client.walk(f, list(CLIENT_C), d=18, e="out")                    # franchit le bord sur le mot

    f = kit.at("S01", "dans", "la pilule « Info » file vers la fiche et bute contre son bord gauche")
    kit.move("info", f, INFO_BUMP, d=9, e="in")

    f = kit.at("S01", "dossier.", "au contact, la pilule « Info » s'écrase contre le bord de la fiche, un éclat encre "
                                  "jaillit, la fiche tremble fort et la renvoie en arc ample, penchée ; aucune rangée "
                                  "ne change : la fiche ne la prend pas")
    kit.shake("fiche", f, 14)
    S.key("eclat_refus", "p", f, 1, 12, "out")
    S.key("eclat_refus", "p", f + 12, 0)
    S.key("info", "sx", f, 0.78, 3, "out")         # écrasée au contact, puis reprend sa forme en repartant
    S.key("info", "sx", f + 3, 1, 8, "out")
    kit.move("info", f, INFO_BACK, d=MOVE, e="out", arc=INFO_BACK_ARC)
    S.key("info", "rot", f, INFO_BACK_ROT, MOVE, "out")

    f = kit.at("S01", "Elle", "la pilule « Info » vole en arc et se pose au-dessus du client ; elle y reste")
    kit.move("info", f, INFO_CLIENT, arc=80)
    S.key("info", "rot", f, 0, MOVE, "inOut")

    f = kit.at("S01", "vie.", "un anneau deep se trace lentement autour de la pilule « Info » pendant que le client "
                              "s'incline vers elle : elle est à lui")
    kit.draw("info_anneau", f, 24, e="inOut")
    client.lean_to(f, LEAN_CLIENT, TILT)
    g = S.word_after("vidéo", f)                    # S02 « Dans cette vidéo » : l'info bat (pas de longue tenue)
    kit.pulse("info", g, peak=1.15, step=4)
    g = S.word_after("voir", g)                     # « on va voir » : le client s'incline encore vers son info
    client.lean_to(g, LEAN_CLIENT + 4, 8, "inOut")

    # ================= S02 : « … les changements de vie qui doivent tout faire revoir. » =================
    f = kit.at("S02", "changements", "trois disques cyan (personne, immeuble, euro) sortent de la pilule « Info », "
                                     "qui reste au-dessus du client, et s'écartent en éventail ; il se redresse")
    kit.pulse("info", f, peak=1.12, step=3)
    for k, did in enumerate(disques):
        kit.pop(did, f + 2 * k, from_pt=INFO_CLIENT, to=DISQUES_S02[k], d=MORPH)
    client.lean_to(f, 0, TILT)

    f = kit.at("S02", "vie", "le client fait un petit bond sur place et les trois disques battent au-dessus de lui : "
                             "ces changements lui arrivent")
    client.hop(f, CLIENT_C, 8, h=12)
    for did in disques:
        kit.pulse(did, f)

    f = kit.at("S02", "revoir.", "de chaque disque part un fil tireté deep vers sa rangée (Famille, Travail, "
                                 "Patrimoine), sans la toucher ; la rangée tremble et sa puce grossit : à revoir")
    S.set(fils[0], sag=SAG_FIL1)
    for k, (fid, row) in enumerate(zip(fils, reliees)):
        g = kit.draw(fid, f + 3 * k, DRAW)
        kit.shake(row, g, 6)
        flash(S, kit, row, g)

    # ================= S03 : « Et la question qui les fait remonter. » =================
    # contrôle sans son : la bulle « ? » de « Toi » ici contredisait la morale (poser la question) : au début, « Toi »
    # ne regarde que la fiche ; le client, lui, bondit vers lui sans être vu
    f = kit.at("S03", "question", "« Toi » lève le stylo vers la fiche et ne regarde qu'elle, sans bulle ni question ; "
                                  "le client fait un petit bond vers lui")
    toi.reach(f, list(TOI_LIT), d=9)
    client.hop(f + 2, CLIENT_C, 8, h=10)

    # contrôle muet : le va-et-vient des disques (vers la fiche, puis renvoyés) se lisait comme une hésitation ; ils
    # restent en place : ce qui remonte, c'est le signal le long des fils, jusqu'aux puces des rangées
    f = kit.at("S03", "remonter.", "les trois disques battent l'un après l'autre et, au bout de chaque fil, la puce "
                                   "de la rangée s'allume : ce qui a changé remonte vers la fiche (sans aller-retour)")
    for k, (did, row) in enumerate(zip(disques, reliees)):
        kit.pulse(did, f + 3 * k, peak=1.25, step=4)
        flash(S, kit, row, f + 3 * k + 6)

    # ================= S04 : « Le problème, c’est la fiche figée. » =================
    f = kit.at("S04", "problème,", "la fiche tremble et renvoie les trois disques au-dessus du client pendant que "
                                   "leurs fils se retirent ; « Toi » baisse le stylo")
    g = f + 2
    kit.shake("fiche", f, 12)
    for k, (did, fid) in enumerate(zip(disques, fils)):
        kit.move(did, f, DISQUES_S04[k], d=12, e="out")
        S.key(fid, "from", f, 1, 9, "out")
        S.key(fid, "draw", f + 9, 0)                # fil rentré : effacé (raccord p2 : draw 0)
    toi.lower(g, 8)

    f = kit.at("S04", "fiche", "un cadre de photo papier, à marge basse large, se trace derrière la fiche")
    kit.draw("cadre", f, DRAW)

    f = kit.at("S04", "figée.", "une grosse punaise cyan tombe sur le milieu du bord haut du cadre ; au contact, le "
                                "cadre et la fiche tremblent : la fiche est une photo épinglée")
    hit = kit.drop("punaise", f, h=150, to=PUNAISE_C)
    kit.shake("cadre", hit, 5, axis="y")
    kit.shake("fiche", hit, 5, axis="y")
    kit.shake("punaise", hit, 3, axis="y")

    # ================= S05 : « Un dossier client est une photo prise à une date. » =================
    f = kit.at("S05", "photo", "flash : la photo-fiche blanchit d'un coup puis revient, un éclair la balaie et le "
                               "contour du cadre clignote en cyan profond, comme au déclenchement")
    S.key("flash", "opacity", f, 0.85, 2, "out")
    S.key("flash", "opacity", f + 2, 0, 9, "inOut")
    S.key("eclair", "p", f, 1, 12, "inOut")
    S.key("cadre", "stroke", f, DEEP)
    S.key("cadre", "stroke", f + 2, INK)

    # contrôle muet : passer SOUS la fiche la faisait disparaître ~0,3 s (« clignotement, comme un bug ») ; elle glisse
    # désormais d'un seul mouvement continu, par-dessus
    f = kit.at("S05", "date.", "la pastille « mars 2023 » glisse d'un seul mouvement continu de l'en-tête à la marge "
                               "basse du cadre en grandissant : c'est la date de la photo")
    kit.move("pastille", f, PASTILLE_PHOTO, scale=1, d=MOVE + 4)

    # ================= S06 : « La vie, elle, continue. » =================
    f = kit.at("S06", "vie,", "une copie de la pastille « mars 2023 » sort d'elle et glisse au-dessus du client : la "
                              "date de sa vie")
    g = kit.pop("vie", f, from_pt="pastille", to=list(PASTILLE_PHOTO), d=4)
    kit.move("vie", g, VIE_C)
    kit.move("info", f, INFO_HAUT, d=MOVE)          # l'info monte d'un cran : la date de la vie se pose dessous

    f = kit.at("S06", "continue.", "la date de la vie défile, une année à chaque battement : « mars 2024 », « mars "
                                   "2025 », « mars 2026 », « nov. 2026 » ; le client fait deux pas sur place ; sous la "
                                   "photo, la pastille reste à « mars 2023 »")
    for k, t in enumerate((T_MARS24, T_MARS25, "mars 2026", T_NOV)):
        S.key("vie", "text", f + 8 * k, t)
        kit.pulse("vie", f + 8 * k, peak=1.12, step=3)
    client.hop(f, CLIENT_C, 8, h=12)
    client.hop(f + 16, CLIENT_C, 8, h=12)

    # ================= S07 : « Et un conseil fondé sur une situation dépassée peut devenir inadapté. » ======
    f = kit.at("S07", "conseil", "« Toi » tend le stylo devant lui : la pilule « Ton conseil » sort de la pointe, à "
                                 "gauche de son buste, et glisse entre lui et le client ; il baisse le bras")
    g = toi.reach(f, list(CONSEIL_SPAWN), d=9)
    kit.pop("conseil", f + 2, from_pt=r3(toi.tip(f + 1)), to=list(CONSEIL_BORN))
    kit.move("conseil", g + 1, list(CONSEIL_C), d=MOVE)
    toi.lower(g + 1, 10)

    f = kit.at("S07", "fondé", "un fil deep se trace du haut de « Ton conseil » jusqu'au bas du cadre-photo : le "
                               "conseil repose sur la fiche")
    kit.draw("conseil_fil", max(f, g + 1), DRAW)

    f = kit.at("S07", "dépassée", "le contour de la pastille « mars 2023 » passe au rouge et elle tremble ; la date de "
                                  "la vie « nov. 2026 » bat : la fiche est dépassée")
    kit.fade("pastille_rouge", f, to=1)
    kit.shake("pastille", f, 6)
    kit.pulse("vie", f)

    f = kit.at("S07", "inadapté.", "le contour de « Ton conseil » passe au rouge, la pilule penche et son fil se "
                                   "détend nettement : le conseil n'est plus adapté")
    kit.fade("conseil_rouge", f, to=1)
    S.key("conseil", "rot", f, CONSEIL_TILT, TILT, "out")
    kit.ensure("conseil_fil", "sag", 0)
    S.key("conseil_fil", "sag", f, 60, TILT, "out")

    # ================= S08 : « Pourquoi commencer par la famille ? … peut tout remettre en question. » ======
    f = kit.at("S08", "Pourquoi", "les trois disques de la vie volent en arc vers le haut et se fondent dans le repère "
                                  "1-2-3, qui grandit")
    for k, did in enumerate(disques):
        g = kit.move(did, f + 2 * k, (MARKER_XS[k], MARKER_Y), arc=60)
        S.key(did, "scale", f + 2 * k + 6, MARKER_DISC_K, 10, "inOut")
        kit.vanish(did, g, d=4)
    kit.pop("marqueur", f + 8, d=MORPH)
    S.key("info", "opacity", f, 0, 10, "inOut")     # l'info s'efface en fondu (elle a donné les trois disques)
    S.key("info", "scale", f + 10, 0)               # raccord p2 : scale 0

    f = kit.at("S08", "famille ?", "l'étape 1 s'allume en cyan, légendée « Famille » ; les rangées Famille et "
                                   "Enfants de la fiche se surlignent")
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
