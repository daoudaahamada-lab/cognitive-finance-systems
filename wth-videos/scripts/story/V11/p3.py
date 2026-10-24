"""V11, partie 3 : S15-S22, images 1772-2790 (34 temps forts, 33,9 s). Patrimoine (bloc recomposé, crédit,
liquidités), déménagement à l'étranger, la question au rendez-vous, la mise à jour de la fiche, la fin standard.

ÉTAT D'ENTRÉE : ENTRY_P3 épinglé à 1771 (`kit.pin(f0 - 1, ENTRY_P3)`, f0 = scene_f0(S, "S15") = 1772) : etat_initial
de S15 = résultat de S14 (trois barres aux nouveaux niveaux, traits d'avant, fils encre vers le conseil rouge penché ;
badges alliances / berceau / immeuble à y 430 ; L1-L3 rouges, L3 surlignée ; étape 2 active). Garde-fous de partie
isolée : `if S.val("client", "scale", f0 - 1) == 0: c.client.enter(f0 - 10, at=CLIENT_C)` ; `c.toi.lower(f0 - 9)`.
SORTIE : fin du film (image 2790, FILM_END = 2791).

Ids : marqueur, fiche_L3-L5, fiche_hl3-5, jauge_* (+ `_mot`, `_trait`), fil_jauge1-3, conseil, conseil_rouge,
conseil_fil, conseil_fil2, patrimoine_titre, bloc_epargne (+ `_ico`, `_mot`), bloc_maison (+ `_ico`, `_mot`), credit
(+ credit_mot), piece1-3, evt_token, badge_token, evt_truck, evt_globe, badge_globe, pile_fiscalite / pile_residence /
pile_produits, toi, client, question, bulle2, question_texte, pastille, pastille_rouge, vie, badge_rings,
badge_cradle, badge_travail, fiche_v1-5, cadre, punaise, fiche ; `fin` naît dans kit.outro.

BRIEF, scène par scène :
- S15 (1772-1894) « Enfin, » : kit.step(f, 2) ; fiche_hl4-5 -> 1 (slotFill L4-L5 -> 0), fiche_hl3 -> 0 (L3 slotFill
  -> 1). « décisions » : les 3 jauges (avec `_mot`, `_trait`) et fil_jauge1-3 rentrent dans le conseil (vanish into
  "conseil", décalés de 2 ; fils : piste from -> 1 ou opacity). « déplacent » : `bloc_epargne` naît sur la valeur de
  L4 (point monde (VALUE_X - 64, ROWS_Y[3]), échelle 0,4) et descend à BLOC_C en grandissant (MOVE, scale 1) ; la
  rangée garde son texte. « patrimoine » : kit.type("patrimoine_titre", rate=1) ; kit.draw("bloc_epargne_ico",
  track="ring").
- S16 (1895-1985) « achète » : drop `evt_token` à EVT_C. « vend » : rot -12 puis 0 (TILT). « immobilier ? » : L4
  red -> 1 + pulse x2.
- S17 (1986-2163) « patrimoine » : evt_token vole en arc 80 jusqu'à (680, 1000) en se réduisant à 110 px (scale 0,5).
  « recompose, » : bloc_epargne w 460 -> EPARGNE_RECOMP (pistes w et pos) pendant que bloc_maison grandit
  (pop, MAISON_RECOMP) ; evt_token s'y fond (vanish). Recentrer `_ico` / `_mot` de l'épargne dans 220 px (pos des
  enfants). « endettement » : `credit` s'étire (sx 0 -> 1, STRETCH), vide. « évolue, » : credit value 0 -> 0,7 (MOVE).
  « liquidités » : piece1-3 pop from_pt=bloc_maison et sautent en arc 60 vers (430, 1000), 3 images d'écart, puis s'y
  fondent. « apparaître. » : épargne -> EPARGNE_FIN, maison -> MAISON_FIN (MOVE) ; kit.pulse("bloc_epargne_ico").
- S18 (2164-2239) « Et » : bloc_epargne, bloc_maison, patrimoine_titre, credit rentrent dans le conseil (vanish into,
  décalés de 2) ; `badge_token` pop en BADGES[3]. « déménage, » : evt_truck roule de TRUCK_FROM à TRUCK_C (MOVE out).
  « surtout » : il repart vers la gauche hors champ (12 im., in), puis scale 0. « l’étranger ? » : drop `evt_globe`
  à GLOBE_C ; 8 images après l'impact L5 red -> 1 + pulse.
- S19 (2240-2414) « Fiscalité, » / « résidence, » / « produits » : pile_fiscalite / pile_residence / pile_produits
  sortent du conseil vers PILE_YS[0..2]. « France » : kit.shake("fiche_L5", 6) ; evt_globe rot 15 (TILT) puis tenue.
  « change » : stroke des 3 -> RED + shake, décalés de 2.
- S20 (2415-2544) « Alors, » : les 3 pilules rentrent dans le conseil ; kit.move("conseil", CONSEIL_RDV) ;
  kit.morph("evt_globe", "badge_globe") vers BADGES[4]. « rendez-vous, » : c.toi.walk(f, TOI_RDV[0], low=True).
  « pose » : le stylo se lève (reach Q_PEN), `question` pop à la pointe puis vole (MOVE, arc 60) au centre de la
  bulle ; `bulle2` grandit (scale 0 -> BULLE2_K0 à bulle2_pos(BULLE2_K0)). « ouverte. » : bulle2 scale BULLE2_K0 -> 1
  ET pos bulle2_pos(BULLE2_K0) -> BULLE2_C avec la MÊME clé (la queue reste fixe) ; `question` glisse à Q_COIN,
  gs 64 -> 40.
- S21 (2545-2696) « « Qu’est-ce » : kit.type("question_texte", rate=1). « dernier » : la pastille bat (×1,3) et
  descend à PASTILLE_LOW (MOVE). « échange ? » » : client.lean_to(6°) vers « Toi » ; les 5 badges volent en arc (MOVE,
  3 images d'écart) vers la puce de leur rangée (BULLET_X, ROWS_Y[i]) à l'échelle 0,55, au-dessus de la fiche (z).
  « C’est » : c.toi.tap(f - TAP + 1, PASTILLE_TAP) ; `vie` glisse dans la pastille et s'y fond ; pastille text ->
  T_NOV, pastille_rouge -> 0 ; puis de L1 à L5 (3 images d'écart) : fall 0 -> 1, red -> 0, kit.type("fiche_vN"),
  badge vanish, slotFill -> 1, hl -> 0. « plus » : marqueur done0-2 -> 1 (3 images d'écart) ; conseil_fil from -> 1 ;
  conseil rot -> 0, conseil_rouge -> 0, fill LIGHT -> CYAN ; kit.draw("conseil_fil2"). « l’entretien. » : kit.hold.
- S22 (2697-2790) « Abonne-toi » : kit.outro("S22", outs=[…, nom_toi], clear="fade", btn_at=MORPH,
  press="comprendre", bsize=34 x BTN_K) ; c.client.exit ; la pastille passe à T_ABONNER et vole / grandit jusqu'au
  bouton (relais btn_at). « comprendre » : c.toi.tap au contact sur le mot, en FIN_BTN_TAP (sous la droite du
  libellé) ; pas de pointeur de souris (opacité 0). Puis immobile jusqu'à 2790.
"""
from . import *  # noqa: F401,F403
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, SCALE, STRETCH, TILT  # noqa: F401
from pipeline.story_kit import TAP, r3  # noqa: F401

BLOC_BORN = (VALUE_X - 64, ROWS_Y[3])           # S15 : le bloc naît sur la valeur « épargne » de L4
BLOC_BORN_K = 0.4
# Écart de place (p3) : le patrimoine finit à x 755 et non 780 : à 780 il passait sous la pilule « Toi » (x 772) et la
# barre « Crédit » touchait son buste ; le titre se décale à gauche du fil du conseil (x 580), qui le traversait.
BLOC_TGT, BLOC_W2 = (537.5, BLOC_C[1]), 435    # x 320-755
TITRE_C = (465, PATRIMOINE_TITRE_C[1])          # x 375-555
EPARGNE_RC, MAISON_RC = (432.5, 225), (652.5, 205)   # « recompose » : x 320-545 | 550-755
EPARGNE_FN, MAISON_FN = (455, 270), (675, 160)       # « apparaître » : x 320-590 | 595-755
CREDIT_TGT, CREDIT_W2 = (537.5, CREDIT_C[1]), 435    # x 320-755
TOKEN_BLOC, TOKEN_BLOC_K = (680, 1000), 0.5     # S17 « patrimoine » : le jeton se pose au bout droit du bloc
EPARGNE_ICO, EPARGNE_MOT = (-74, 0), (27, 0)    # S17 : « Épargne » + pictogramme recentrés (194 px dans 220)
MAISON_ICO, MAISON_MOT = (-67, 0), (21, 0)      # S17 : « Maison » + pictogramme recentrés (164 px dans 235)
PIECE_DROP = (432.5, 1000)     # S17 « liquidités » : les pièces sautent dans l'épargne
TRUCK_OUT = (-220, TRUCK_C[1])                  # S18 « surtout » : hors champ à gauche
Q_PEN = (630, 1010)
# Écart de place (p3) : la grande bulle fait 360 x 220 en (240, 760) (x 60-420) et non 400 en (260, 760) (x 60-460) :
# à 460 elle couvrait les puces des rangées L4-L5 (x 445-489), où se posent les badges en S21. La petite bulle de
# « pose » (échelle 0,65) se tient dans la colonne libre, en (300, 790) (x 183-417, y 718-862) : à bulle2_pos(0,65)
# elle couvrait le cadre et la pilule de la vie ; sa queue pointe vers « Toi » et se pose sur sa tête à « ouverte. ».
B2_C, B2_W = (240, 760), 360
B2_SMALL = (300, 790)
Q_COIN2 = (88, 700)                             # le « ? » dans le coin haut gauche de la bulle
QTXT = (118, 765)                               # le texte (4 lignes, centre du bloc en y) à droite du « ? »
FIN_TAP = (615, 955)                            # bas du bouton (x 350-730, y 852-964), sous la droite du libellé                             # S20 « pose » : la pointe se lève devant « Toi »
BADGE_ROW_K = 0.55                              # S21 : un badge (r 36) se pose sur la puce (r 22) de sa rangée
PASTILLE_K_PEAK = 1.3
BTN_W, BTN_H = 380, 112
BTN_K = BTN_H / PASTILLE_H                      # relais pastille -> bouton (w = BTN_W / BTN_K, échelle BTN_K)
FIN_POS = (540, 760)                            # carte de fin (défaut de kit.outro)
FIN_BUTTON = (FIN_POS[0], FIN_POS[1] + 520 / 2 - BTN_H / 2 - 56)   # (540, 908) : centre du bouton
BADGES_IDS = ["badge_rings", "badge_cradle", "badge_travail", "badge_token", "badge_globe"]


def part(S, kit, c):
    toi, client = c.toi, c.client
    f0 = scene_f0(S, "S15")                                   # 1772
    kit.pin(f0 - 1, ENTRY_P3)                                 # etat_initial de S15 = résultat de S14
    if S.val("client", "scale", f0 - 1) == 0:                 # partie construite seule (WTH_PARTS=p3)
        client.enter(f0 - 10, at=CLIENT_C)
    toi.lower(f0 - 9)                                         # « Toi » bras baissé (sans effet s'il l'est déjà)

    def conseil_top(n):
        return S.to_world("conseil", list(CONSEIL_TOP_LOCAL), n)

    def sortir(pid, f, to, d=12):
        """Une pilule sort du haut du conseil et monte à sa place (POP + glissé de 400 ms)."""
        kit.pop(pid, f, from_pt=conseil_top(f - 1), to=list(to))
        S.key(pid, "pos", f, r3(to), d, "out")
        return f + d

    def set_z(id, f, z):
        kit.ensure(id, "z", S.ents[id]["z"])
        S.key(id, "z", f, z)

    # ======================= S15 : l'étape 3, le patrimoine =======================
    f = kit.at("S15", "Enfin,", "le repère glisse sur l'étape 3 « Patrimoine » ; les rangées Patrimoine et Résidence "
                                "se surlignent, le surlignage de Travail s'efface")
    kit.step(f, 2)
    for i, on in ((2, 0), (3, 1), (4, 1)):
        S.key(f"fiche_hl{i + 1}", "opacity", f, on, 9, "out")
        S.key(f"fiche_L{i + 1}", "slotFill", f, 1 - on, 9, "out")

    f = kit.at("S15", "décisions", "les trois barres, leurs légendes et leurs fils rentrent dans le conseil, l'une "
                                   "après l'autre")
    for k, (jid, *_rest) in enumerate(JAUGES):
        g = f + 2 * k
        S.key(f"fil_jauge{k + 1}", "from", g, 1, POP, "in")
        kit.vanish(jid, g, into="conseil")
        kit.vanish(f"{jid}_mot", g, into="conseil")

    f = kit.at("S15", "déplacent", "une copie de l'épargne sort de la valeur de la rangée Patrimoine (qui garde son "
                                   "texte) et descend au centre en grandissant : un bloc cyan « Épargne »")
    kit.ensure("bloc_epargne", "w", BLOC_W2)
    S.key("bloc_epargne", "pos", f - 1, list(BLOC_BORN))
    kit.pop("bloc_epargne", f, scale=BLOC_BORN_K, d=4)
    kit.move("bloc_epargne", f + 4, list(BLOC_TGT), scale=1)

    f = kit.at("S15", "patrimoine", "le titre « Patrimoine » s'écrit au-dessus du bloc ; un anneau cerne l'euro")
    S.key("patrimoine_titre", "pos", f - 1, list(TITRE_C))
    kit.type("patrimoine_titre", f, rate=1)
    kit.draw("bloc_epargne_ico", f, d=DRAW, track="ring")

    # ======================= S16 : une maison achetée ou vendue =======================
    f = kit.at("S16", "achète", "un jeton-maison tombe dans la vie du client")
    kit.drop("evt_token", f, h=200, to=list(EVT_C))

    f = kit.at("S16", "vend", "le jeton-maison pivote puis revient : il change de mains")
    S.key("evt_token", "rot", f, -12, 7, "out")
    S.key("evt_token", "rot", f + 7, 0, 8, "inOut")

    f = kit.at("S16", "immobilier ?", "« Patrimoine : épargne » vire au rouge et sa puce bat deux fois")
    S.key("fiche_L4", "red", f, 1, 3, "out")
    kit.pulse("fiche_L4", f, times=2, step=2, track="pulse")

    # ======================= S17 : le patrimoine se recompose =======================
    f = kit.at("S17", "patrimoine", "le jeton-maison vole en arc jusqu'au bout droit du bloc en se réduisant")
    set_z("evt_token", f, 12.5)                               # au-dessus du bloc (z 12)
    kit.move("evt_token", f, list(TOKEN_BLOC), arc=80, scale=TOKEN_BLOC_K)

    f = kit.at("S17", "recompose,", "l'épargne rétrécit à gauche pendant qu'une part « Maison » grandit à droite ; "
                                    "le jeton s'y fond")
    S.key("bloc_epargne", "w", f, EPARGNE_RC[1], MOVE, "inOut")
    kit.move("bloc_epargne", f, [EPARGNE_RC[0], BLOC_C[1]])
    S.key("bloc_epargne_ico", "ring", f, 0, 8, "inOut")      # l'anneau se défait : place pour le pictogramme
    kit.move("bloc_epargne_ico", f, list(EPARGNE_ICO))
    kit.move("bloc_epargne_mot", f, list(EPARGNE_MOT))
    S.key("bloc_maison_ico", "pos", f - 1, list(MAISON_ICO))
    S.key("bloc_maison_mot", "pos", f - 1, list(MAISON_MOT))
    kit.ensure("bloc_maison", "w", MAISON_RC[1])
    S.key("bloc_maison", "pos", f - 1, [MAISON_RC[0], BLOC_C[1]])
    kit.pop("bloc_maison", f, d=MOVE, e="inOut")
    kit.vanish("evt_token", f + 2, into="bloc_maison", d=POP)

    f = kit.at("S17", "endettement", "une barre « Crédit » s'étire sous le bloc, vide")
    kit.ensure("credit", "w", CREDIT_W2)
    S.key("credit", "pos", f - 1, list(CREDIT_TGT))
    S.key("credit_mot", "pos", f - 1, [-CREDIT_W2 / 2 + 20, 0])
    S.key("credit", "sx", f - 1, 0)
    S.key("credit", "scale", f - 1, 1)
    S.key("credit", "sx", f, 1, STRETCH, "out")

    f = kit.at("S17", "évolue,", "la barre « Crédit » se remplit de gris aux deux tiers")
    S.key("credit", "value", f, 0.7, MOVE, "inOut")

    f = kit.at("S17", "liquidités", "trois pièces sortent de la part « Maison » et sautent une à une dans l'épargne, "
                                    "où elles se fondent")
    maison = S.to_world("bloc_maison", [0, 0], f - 1)
    for k in range(3):
        pid, g = f"piece{k + 1}", f + 3 * k
        S.key(pid, "pos", g - 1, r3(maison))
        kit.pop(pid, g, d=6)
        arr = kit.move(pid, g, list(PIECE_DROP), d=12, arc=60)
        kit.vanish(pid, arr, d=5)

    f = kit.at("S17", "apparaître.", "l'épargne se réélargit pendant que la maison recule ; l'euro bat : de l'argent "
                                     "disponible est apparu")
    S.key("bloc_epargne", "w", f, EPARGNE_FN[1], MOVE, "inOut")
    kit.move("bloc_epargne", f, [EPARGNE_FN[0], BLOC_C[1]])
    S.key("bloc_maison", "w", f, MAISON_FN[1], MOVE, "inOut")
    kit.move("bloc_maison", f, [MAISON_FN[0], BLOC_C[1]])
    kit.draw("bloc_epargne_ico", f + 4, d=DRAW, track="ring")   # l'anneau se retrace autour de l'euro
    kit.vanish("bloc_maison_ico", f, d=8)                     # 175 px : « Maison » seul, sans pictogramme
    kit.move("bloc_maison_mot", f, [0, 0])
    kit.pulse("bloc_epargne_ico", f + 4, peak=1.3, step=4)

    # ======================= S18 : un déménagement, à l'étranger =======================
    f = kit.at("S18", "Et", "le patrimoine (bloc, titre, crédit) rentre dans le conseil ; un badge maison se range "
                            "en haut de la vie du client")
    for k, oid in enumerate(("bloc_epargne", "bloc_maison", "patrimoine_titre", "credit")):
        kit.vanish(oid, f + 2 * k, into="conseil")
    kit.pop("badge_token", f)

    f = kit.at("S18", "déménage,", "un camion de déménagement entre par la gauche dans la vie du client")
    S.key("evt_truck", "pos", f - 1, list(TRUCK_FROM))
    S.key("evt_truck", "scale", f - 1, 1)
    kit.move("evt_truck", f, list(TRUCK_C), e="out")

    f = kit.at("S18", "surtout", "le camion repart vers la gauche, hors de l'image")
    g = kit.move("evt_truck", f, list(TRUCK_OUT), d=12, e="in")
    S.key("evt_truck", "scale", g, 0)

    f = kit.at("S18", "l’étranger ?", "un globe tombe dans la vie du client ; « Résidence : France » vire au rouge et "
                                      "sa puce bat")
    impact = kit.drop("evt_globe", f, h=200, to=list(GLOBE_C))
    S.key("fiche_L5", "red", impact + 8, 1, 3, "out")
    kit.pulse("fiche_L5", impact + 8, times=2, step=2, track="pulse")

    # ======================= S19 : fiscalité, résidence, produits =======================
    for pid, word in (("pile_fiscalite", "Fiscalité,"), ("pile_residence", "résidence,"),
                      ("pile_produits", "produits")):
        nom = dict(PILE)[pid]
        k = ("pile_fiscalite", "pile_residence", "pile_produits").index(pid)
        f = kit.at("S19", word, f"« {nom} » sort du conseil et s'empile au-dessus")
        sortir(pid, f, (PILE_X, PILE_YS[k]))

    f = kit.at("S19", "France", "la valeur rouge « France » tremble et le globe pivote : le pays change")
    kit.shake("fiche_L5", f, 6)
    S.key("evt_globe", "rot", f, 15, TILT, "inOut")

    f = kit.at("S19", "change", "les contours des trois pilules virent au rouge et elles tremblent, de bas en haut")
    for k, pid in enumerate(("pile_fiscalite", "pile_residence", "pile_produits")):
        S.key(pid, "stroke", f + 2 * k, RED, 4, "out")
        kit.shake(pid, f + 2 * k, 5)

    # ======================= S20 : au rendez-vous, une question ouverte =======================
    f = kit.at("S20", "Alors,", "la pile rentre dans le conseil, qui glisse entre les deux personnages ; le globe se "
                                "range en cinquième badge")
    kit.move("conseil", f, list(CONSEIL_RDV))
    bp = S.ents["bulle2"]["p"]                                # grande bulle, p3 seule : 360 px, queue vers « Toi »
    for shp in ("big", "small"):
        bp[shp] = dict(bp[shp], w=B2_W)
    bp["tail"] = [BULLE2_TIP[0] - B2_C[0], BULLE2_TIP[1] - B2_C[1]]
    for k, pid in enumerate(("pile_produits", "pile_residence", "pile_fiscalite")):
        kit.vanish(pid, f + 2 * k, into="conseil")
    kit.morph("evt_globe", "badge_globe", f)

    f = kit.at("S20", "rendez-vous,", "« Toi » s'avance vers le client : c'est le rendez-vous")
    toi.walk(f, TOI_RDV[0], low=True)

    f = kit.at("S20", "pose", "« Toi » lève le stylo : un « ? » en sort et vole au-dessus de la vie du client ; une "
                              "bulle grandit autour, la queue vers « Toi »")
    toi.reach(f - 8, list(Q_PEN), d=8)
    tip = r3(toi.tip(f - 1))
    kit.ensure("question", "gs", Q_GS_S20)
    S.key("question", "gs", f - 1, Q_GS_S20)
    kit.pop("question", f, from_pt=tip, to=tip)
    kit.move("question", f + 3, list(B2_SMALL), arc=60)
    S.key("bulle2", "pos", f + 8, list(B2_SMALL))
    kit.pop("bulle2", f + 9, scale=BULLE2_K0, d=SCALE)
    toi.lower(f + 6, 10)

    f = kit.at("S20", "ouverte.", "la bulle s'ouvre en grand, la queue toujours sur « Toi » ; le « ? » glisse dans son "
                                  "coin")
    S.keys("bulle2", f, SCALE, "out", scale=1, pos=list(B2_C))
    kit.move("question", f, list(Q_COIN2), d=SCALE, e="out")
    S.key("question", "gs", f, Q_GS_COIN, SCALE, "out")

    # ======================= S21 : la question ; la fiche se met à jour =======================
    f = kit.at("S21", "« Qu’est-ce", "la question s'écrit dans la bulle : « Qu’est-ce qui a changé depuis notre "
                                     "dernier échange ? »")
    S.key("question_texte", "pos", f - 1, list(QTXT))
    kit.type("question_texte", f, rate=1)

    f = kit.at("S21", "dernier", "la pastille « mars 2023 » de la fiche bat et descend un peu : la date du dernier "
                                 "échange")
    kit.pulse("pastille", f, peak=PASTILLE_K_PEAK, step=5)
    kit.move("pastille", f, list(PASTILLE_LOW))

    f = kit.at("S21", "échange ? »", "le client se penche vers « Toi » ; les cinq badges de sa vie volent chacun "
                                     "jusqu'à sa rangée de la fiche")
    client.lean_to(f, 6, TILT)
    for i, bid in enumerate(BADGES_IDS):
        g = f + 3 * i
        set_z(bid, g, 10)                                     # au-dessus de la fiche et de ses rangées
        if f"{bid}_png" in S.ents:
            set_z(f"{bid}_png", g, 10.1)
        kit.move(bid, g, [BULLET_X, ROWS_Y[i]], arc=60, scale=BADGE_ROW_K)

    f = kit.at("S21", "C’est", "« Toi » touche la date de la fiche : la date de la vie s'y fond, elle passe à « nov. "
                               "2026 » ; puis, rangée après rangée, chaque valeur rouge tombe et la nouvelle s'écrit")
    hit = toi.tap(f - TAP + 1, list(PASTILLE_TAP))
    assert hit == f, (hit, f)
    arr = kit.move("vie", hit, list(PASTILLE_LOW), d=8, e="inOut")
    S.key("vie", "scale", arr, 0, 3, "in")
    S.key("vie", "opacity", arr + 3, 0)
    kit.ensure("pastille", "textOp", 1)
    S.key("pastille", "textOp", hit + 4, 0, 4, "out")
    S.key("pastille", "text", arr, T_NOV)
    S.key("pastille", "textOp", arr, 1, FADE, "out")
    S.key("pastille_rouge", "opacity", arr, 0, FADE, "out")
    toi.lower(hit + 6, 8)
    for i in range(5):
        g = arr + 3 * i
        lid = f"fiche_L{i + 1}"
        kit.ensure(lid, "fall", 0)
        S.key(lid, "fall", g, 1, POP, "in")
        S.key(lid, "red", g, 0, 6, "out")
        S.key(lid, "slotFill", g, 1, 9, "out")
        S.key(f"fiche_hl{i + 1}", "opacity", g, 0, 9, "out")
        kit.type(f"fiche_v{i + 1}", g + 4)
        kit.vanish(BADGES_IDS[i], g, d=6)

    f = kit.at("S21", "plus", "le repère se coche aux trois étapes ; le conseil lâche son vieux fil, se redresse, "
                              "perd son rouge, se remplit de cyan et se relie à la fiche à jour")
    for k in range(3):
        kit.ensure("marqueur", f"done{k}", 0)
        S.key("marqueur", f"done{k}", f + 3 * k, 1, 6, "out")
    kit.pop("marqueur_fait3", f + 6, d=5)                     # le disque actif garde son chiffre : pastille cochée
    kit.draw("marqueur_fait3_coche", f + 8, 6)
    S.key("conseil_fil", "from", f, 1, POP, "in")
    S.key("conseil", "rot", f, 0, POP, "out")
    S.key("conseil_rouge", "opacity", f, 0, FADE, "out")
    S.key("conseil", "fill", f, CYAN, POP, "out")
    kit.draw("conseil_fil2", f + 4, d=POP)

    kit.hold("S21", "l’entretien.", "tenue : fiche à jour « nov. 2026 », repère coché, conseil cyan relié ; rien ne "
                                    "bouge jusqu'à « Abonne-toi »")

    # ======================= S22 : fin standard ; le bouton touché du stylo =======================
    outs = ["fiche", "cadre", "punaise", "bulle2", "question", "question_texte", "marqueur", "marqueur_fait3",
            "conseil", "conseil_fil", "conseil_fil2", "nom_toi"]
    glide = MORPH
    out = kit.outro("S22", outs=outs, clear="fade", btn_at=glide, press="comprendre",
                    bsize=round(34 * BTN_K, 1))
    f, fp = out["card"], out["press"]
    S.set(out["cursor"], opacity=0)                           # pas de pointeur de souris : le stylo de « Toi »
    for bt in S.beats:
        if bt["scene"] == "S22" and bt["frame"] == f:
            bt["what"] = ("le client sort ; la fiche, la bulle, le repère et le conseil s'effacent, la carte de fin "
                          "surgit ; la pastille « nov. 2026 » devient « S’abonner », descend et grandit : c'est le "
                          "bouton")
        elif bt["scene"] == "S22" and bt["frame"] == fp:
            bt["what"] = ("le stylo de « Toi » touche le bas du bouton « S’abonner », qui s'enfonce ; puis plus rien "
                          "ne bouge")
    client.exit(f)
    set_z("pastille", f, 41)                                  # au-dessus de la carte (z 40)
    S.key("pastille", "textOp", f, 0, 4, "out")
    S.key("pastille", "text", f + 4, T_ABONNER)
    S.key("pastille", "textOp", f + 4, 1, FADE, "out")
    kit.ensure("pastille", "w", PASTILLE_W)
    S.key("pastille", "w", f, round(BTN_W / BTN_K, 2), glide, "inOut")
    kit.move("pastille", f, list(FIN_BUTTON), d=glide, e="inOut", scale=round(BTN_K, 4))
    S.key("pastille", "opacity", f + glide, 0)                # relais exact : le bouton de la carte paraît dessous

    toi.set_z(fp - TAP - 4, S.ents[toi.id]["z"], tool_z=44)   # bras et stylo au-dessus de la carte
    assert_reach(TOI_RDV[0], FIN_TAP, "S22 bouton (p3)")
    hit = toi.tap(fp - TAP + 1, list(FIN_TAP))
    assert hit == fp, (hit, fp)
    end = toi.lower(hit + 6, 8)
    assert end < FILM_END, (end, FILM_END)
