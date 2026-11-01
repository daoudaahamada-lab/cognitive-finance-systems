"""V15, partie 3 : S17-S22, images 1746-2450 (23 temps forts, 23,5 s). Fin du point 3, chute, fin.

ÉTAT D'ENTRÉE (etat_initial de S17) : kit.pin(1745, ENTRY_P3) en tête de partie. Escalier de 4 marches (B1 light), la
pastille au sommet (170, 798) ; « 1 », « 2 », « 3 » cerclés ; coches sur B1 et B2 ; jauge à 1/2 ; « Semaine 2 » ;
« Toi » sur la marche 3 en TOI_M3 (378, 835), étiquette à droite de la tête (NOM_MARCHE).
Partie isolée (WTH_PARTS=p3) : « Toi » est en TOI_P0 ; si S.val("toi", "pos", 1745) n'est pas TOI_M3, le faire sauter
(hop) en TOI_M3 vers 1730-1745 : sans effet dans le film entier. Jamais de kit.pin sur la figurine.

RÈGLES DE LA PARTIE
- Rouge : seulement « 0 ✓ » (S17 « jamais » -> S18 « D’où »).
- Au rembobinage (S19), ce qui a fini d'agir RENTRE dans un objet (marche, pilule) : pas de gris.
- Pas de flèche de souris à la fin : le stylo de « Toi » touche le bouton (modèle : scripts/story/V14/p3.py, l. 370-405 :
  kit.outro(..., clear="fade", btn_at=MOVE), S.set(out["cursor"], opacity=0), la pastille relayée par le bouton,
  ring(S, "fin_onde1-2", hit, …)).

SCÈNE PAR SCÈNE
- S17 (1746-1887) « quelques » : calendrier « Semaine 3 », pulse. « semaines, » : tap COCHE_PTS[2] ; draw coche3 ;
  elan3 de COCHE_PTS[2] vers ENERGIE_QUARTS[2] (arc) ; energie 0,5 -> 0,75 à l'arrivée. « avancé » : coche1-3 battent
  (stagger 4, x1,2) ; kit.pop de bilan3 + bilan3_coche (« 3 ✓ » en BILAN3_C). « grand » : fantome1-4 kit.pop(from_pt=
  FANTOME_FROM) (stagger 3) : la tour du début en tirets, mêmes pictogrammes ; fantome_nom pop. « jamais » : pop zero +
  zero_coche (« 0 ✓ » rouge, même hauteur que « 3 ✓ »).
- S18 (1888-2079) « D’où » : fantome*, fantome_nom, zero, zero_coche se réduisent dans FANTOME_FROM ; bilan3 et sa
  coche dans COCHE_PTS[2] ; energie et energie_nom dans la tête de « Toi ». « règle : » : calendrier vers CAL_REGLE_C,
  scale 1,25 (MOVE inOut), text « 1 décision / semaine », w cal_w. « décision » : coche1-3 battent (stagger 4, x1,2).
  « fin » : `annee` s'étire hors de la pilule (kit.pop from_pt=CAL_REGLE_C, ou sy 0 -> 1 puis move) ; kit.type de
  annee_s1 et annee_fin. « l’année, » : coche_double1-3 (scale 1 sur COCHE_PTS) volent en monde vers ANNEE_CASES
  (stagger 3, 9 images) et s'y fondent ; annee value -> 3/52 à leur arrivée ; puis value -> 1 en 20 images linéaire et
  `compteur` (pop à 3) -> 52 dans les mêmes images. « 52 » : pulse compteur 1,15. « décisions » : kit.type decisions.
- S19 (2080-2169) « Avant, » : annee, annee_s1, annee_fin, compteur, decisions rentrent dans la pilule (morph vers
  CAL_REGLE_C) qui revient en CAL_C, scale 1, text « Avant », w cal_w ; cal_rewind (◀◀) pop en (cal_icon_x("Avant"),
  0) ; toi.run(f, [TOI_M3, TOI_M2, TOI_M1, TOI_P0], 18) ; nom_toi -> NOM_SOL. « attendais » : coche*, num* rentrent dans
  leurs marches (200 ms) ; bloc1 fill -> PAPER ; set_blocks vers [tower(i, 100)] (stagger 3, MOVE) ; pastille ->
  PASTILLE_TOUR[100] avec bloc4. « temps » : cadran en CADRAN_CAL (start 0 / value 0 à f-1), pop from_pt CAL_C ; value
  0 -> 20 linéaire jusqu'à 2169 (dérive lente) ; « Toi » immobile, bras baissé (hold_low).
- S20 (2170-2233) « Maintenant, » : calendrier « Maintenant », w ; cal_rewind se réduit ; cadran dans CAL_C ;
  set_blocks vers [stairs(i)] (stagger 3, MOVE) ; pastille -> PASTILLE_ESCALIER. « fais » : toi.hop(f, TOI_M1, 12,
  h=30) ; nom_toi -> NOM_MARCHE. « chose. » : tap COCHE_PTS[0] ; draw coche1 au contact ; num1 (scale 1, draw 0,
  chars 0 à f-1) se retrace et « 1 » s'écrit ; bloc1 fill -> LIGHT.
- S21 (2234-2355) « tout » : bloc2-4 battent (stagger 4, x1,04), sans coche ; numt2-4 (cercles en tirets) pop sur
  leurs marches. « commencer » : kit.move("pastille", f, PASTILLE_RETOUR, arc=80) et toi.reach(f, PASTILLE_RETOUR_TIP)
  dans les mêmes images ; pulse pastille 1,12 à l'arrivée. « mieux » : pulse numt2 1,15 ; puis plus rien ne bouge
  (tenue ≈ 1,6 s).
- S22 (2356-2450) « Abonne-toi » : kit.outro("S22", outs=[blocs, sol, coche1, num1, numt2-4, calendrier, nom_toi…],
  press="argent.", clear="fade", btn_at=MOVE) ; la pastille quitte le stylo, vole à la place du bouton, text
  « S’abonner », puis relais (opacité 0) ; toi.hop vers TOI_P0. « argent. » : hit = toi.tap(f - TAP + 1, FIN_TAP)
  (dans le bouton, hors du libellé) ; ondes fin_onde1-2 (ring) ; immobile jusqu'à la fin (2450).

CONTRÔLE SANS SON : S17 « 3 ✓ » et « 0 ✓ » au même corps (120) et à la même hauteur (y 560), tour fantôme posée face aux
marches (x 640-920, y 625-1025) ; S19 le grand ◀◀ reste pendant tout le rembobinage (jusqu'à « temps ») ;
l'horloge tourne au-dessus de « Toi » qui attend (CADRAN_ATTENTE).

ÉCARTS D'EXÉCUTION (aucun sens changé, aucun temps fort déplacé) :
- S19 « Avant, » : la descente passe par Figure.run sur le trajet des montées de p2 PARCOURU À L'ENVERS (au-dessus de
  chaque arête, puis presque à la verticale), en 24 images : la ligne droite marche -> marche faisait passer le bas du
  buste dans l'arête de la marche (même raison que p2) ; la pilule part au centre 4 images après le mot et le rangement
  vise la pilule en mouvement.
- S19 « attendais » : les marches se ré-empilent de haut en bas (rembobinage de S10, joué à l'envers), 14 images
  chacune, décalées de 3, pour être posées avant « temps ».
- S20 « fais » : montée par le même trajet que p2 (_climb, 12 images) et non un hop droit (le buste passait dans
  l'arête de la marche B1).
- S22 : la pastille vole sans libellé (« Ton argent » s'efface au départ) et le relais vers le bouton se fait par un
  fondu de 6 images (et non un relais sec) : elle porte le pictogramme euro, absent du bouton ; « S’abonner » serré
  contre l'euro était peu lisible et un relais sec ferait sauter le libellé de 26 px.
- S20-S21 : « Toi » se pose sur la marche 1 en (735, 1035) (TOI_M1 + 27 px) et non en TOI_M1 : depuis TOI_M1, le
  coude du bras levé vers l'argent couvrait le « 2 » tireté qui bat sur « mieux ».

REVUE 1 : S17 ondes des coches sur « avancé », « 3 ✓ » à f + 2, tour fantôme à l'échelle réelle avec cases vides,
« 0 ✓ » au même corps ; S18 bascule de texte sans image vide, ondes sur « décision », doubles des coches lents (12 images,
décalés de 5) et compteur après la troisième ; S19 grand ◀◀ + voile, ré-empilement par paliers de 2 images, horloge à
tour complet ; S20 grand ▶▶, « Toi » touche Budget avant l'étalement ; S21 argent levé comme en S01, cercles tiretés
qui battent ; S22 le sol reste, la pastille entière devient le bouton (relais sec), légende de la carte en 34.
"""
import math

from pipeline.story import FADE, MORPH, MOVE, POP, STYLE  # noqa: F401
from pipeline.story_kit import TAP

from . import *  # noqa: F401,F403

VOILE_OP = 0.07                                 # voile du rembobinage (0,13 salissait les zones réservées : QA)
FIN_BUTTON = (540, 908)                         # centre du bouton de la carte (540, 760), 620 x 520 : 760 + 260 - 112
FIN_BW = 380                                    # largeur du bouton de la carte
FIN_K = round(FIN_BW / PASTILLE_W, 4)           # la pastille entière (« € Ton argent ») grandit à la largeur du bouton
COCHES = ["coche1", "coche2", "coche3"]
NUMS = ["num1", "num2", "num3"]
DOUBLES = ["coche_double1", "coche_double2", "coche_double3"]
TOI_M1_P3 = (TOI_M1[0] + 27, TOI_M1[1])        # S20-S21 : sur la marche 1, 27 px plus à droite que TOI_M1 : le coude du
#                                                 bras levé vers l'argent (S21) ne couvre plus le « 2 » tireté
for _pt, _what in [(COCHE_PTS[0], "S20 cocher la marche 1"), (PASTILLE_RETOUR_TIP, "S21 lever l'argent"),
                   ((TOWER_X + TOWER_W / 2 + 2, 1180), "S20 toucher le bloc Budget")]:
    assert_reach(TOI_M1_P3 if "S20 toucher" not in _what else TOI_P0, _pt, _what)


def _set_what(S, scene, frame, what):
    for bt in S.beats:
        if bt["scene"] == scene and bt["frame"] == frame:
            bt["what"] = what


def _climb_pts(a, b):
    """Trajet de la montée de la place `a` à la marche `b` (comme p2) : presque à la verticale d'abord (le bas du buste
    passe au-dessus de l'arête), puis en arc jusqu'à `b`."""
    dx = b[0] - a[0]
    return [list(a), [a[0] - 2, a[1] - 75], [a[0] - 12, a[1] - 120], [a[0] + 0.4 * dx, a[1] - 140],
            [a[0] + 0.72 * dx, a[1] - 130], list(b)]


def _climb(toi, f, to, d):
    """Monte sur la marche `to` en d images (Figure.run), bras baissé. Renvoie f + d."""
    a = toi.S.val("toi", "pos", f - 1)
    end = toi.run(f, _climb_pts(a, to), d)
    toi.hold_low(f, end)
    return end


def _descent_pts(places):
    """Descente marche après marche : chaque montée de p2 parcourue à l'envers (au-dessus de l'arête, puis vers le
    bas presque à la verticale)."""
    pts = [list(places[0])]
    for hi, lo in zip(places, places[1:]):
        pts += list(reversed(_climb_pts(lo, hi)))[1:]
    return pts


def _set_stairs(S, f, geoms, order, step, d, pastille_to, rewind=False):
    """Les blocs vont sur `geoms` un par un dans l'ordre `order` (décalage `step`, d images ease-in-out), enfants
    compris ; la pastille suit le bloc du haut (bloc4) avec la même clé. Renvoie la dernière image."""
    end = f
    for k, i in enumerate(order):
        c, w, h = geoms[i]
        g = f + step * k
        ico, nom = block_children(w)
        if rewind:                              # rembobinage : le même trajet, par paliers de 2 images
            for tr, v in (("pos", list(c)), ("w", w), ("h", h)):
                stepped(S, BLOC_IDS[i], tr, g, d, v)
            stepped(S, BLOC_ICO[i], "pos", g, d, ico)
            stepped(S, BLOC_NOM[i], "pos", g, d, nom)
            if i == 3:
                stepped(S, "pastille", "pos", g, d, list(pastille_to))
        else:
            S.keys(BLOC_IDS[i], g, d, "inOut", pos=list(c), w=w, h=h)
            S.key(BLOC_ICO[i], "pos", g, ico, d, "inOut")
            S.key(BLOC_NOM[i], "pos", g, nom, d, "inOut")
            if i == 3:
                S.key("pastille", "pos", g, list(pastille_to), d, "inOut")
        end = max(end, g + d)
    return end


def _reappear(S, id, n, **tracks):
    """Remet un élément rangé (vanish) à l'échelle 1, opacité 1, à l'image n, avec ses pistes de départ."""
    S.key(id, "scale", n, 1)
    S.key(id, "opacity", n, 1)
    for k, v in tracks.items():
        S.key(id, k, n, v)


def part(S, kit, c):
    toi = c.toi
    f0 = scene_f0(S, "S17")
    kit.pin(f0 - 1, ENTRY_P3)                   # etat_initial de S17 (raccord avec p2)
    if S.val("toi", "scale", f0 - 1) == 0:      # garde-fou de la série (« Toi » est visible dès l'image 0 en V15)
        toi.enter(f0 - 10, at=list(TOI_M3))
    if math.dist(S.val("toi", "pos", f0 - 1), TOI_M3) > 0.5:   # partie construite seule : « Toi » saute à sa place
        toi.hop(f0 - 16, list(TOI_M3), 14, h=30)
        toi.lower(f0 - 16, 14)

    # ================= S17 : marche 3 cochée, « 3 ✓ » contre la tour fantôme « 0 ✓ » =================
    f = kit.at("S17", "quelques", "le calendrier passe à « Semaine 3 » et bat")
    cal_swap(S, kit, f, T_CAL["s3"])

    f = kit.at("S17", "semaines,", "le stylo touche la marche Placements : une coche pleine s'y trace ; elle bat et "
                                   "lance un troisième grand segment cyan dans la jauge, qui passe aux trois quarts")
    hit = toi.tap(f - TAP + 1, list(COCHE_PTS[2]))
    kit.draw("coche3", hit, 6)
    toi.lower(hit + 6, 8)
    kit.pulse("coche3", hit + 6, peak=1.3)
    elan_fly(S, kit, "elan3", hit + 6, COCHE_PTS[2], ENERGIE_QUARTS[2], 0.75)

    f = kit.at("S17", "avancé", "« 3 ✓ » (ExtraBold 96) sort de la troisième coche et se pose au-dessus de l'escalier ; "
                                "une onde part de chaque coche, l'une après l'autre, et sa marche bat")
    kit.pop("bilan3", f + 2, from_pt=list(COCHE_PTS[2]), d=MORPH)
    kit.pop("bilan3_coche", f + 3, from_pt=list(COCHE_PTS[2]), d=MORPH)
    for k in range(3):
        count_rings(S, kit, f + 4 * k, k)

    f = kit.at("S17", "grand", "à droite, la tour du grand plan ressort du bloc Budget en fantôme, à sa taille réelle : "
                               "quatre blocs en tirets, les mêmes pictogrammes, quatre cases de coche vides ; « Grand "
                               "plan » dessous")
    for k, fid in enumerate(FANTOME_IDS):
        kit.pop(fid, f + 3 * k, from_pt=list(FANTOME_FROM), to=fantome_c(k))
    kit.pop("fantome_nom", f + 12)

    f = kit.at("S17", "jamais", "« 0 ✓ » (même corps que « 3 ✓ », le 0 en rouge) paraît au-dessus de la tour fantôme : "
                                "jamais commencée")
    kit.pop("zero", f)
    kit.pop("zero_coche", f + 2)

    # ================= S18 : la règle, la barre des 52 semaines =================
    f = kit.at("S18", "D’où", "la tour fantôme, « Grand plan » et « 0 ✓ » rentrent dans le bloc Budget ; « 3 ✓ » "
                              "rentre dans la troisième coche ; la jauge « Énergie » rentre dans la tête de « Toi »")
    for id in FANTOME_IDS + ["fantome_nom", "zero", "zero_coche"]:
        kit.vanish(id, f, into=list(FANTOME_FROM), d=7)
    for id in ("bilan3", "bilan3_coche"):
        kit.vanish(id, f, into=list(COCHE_PTS[2]), d=7)
    tp = S.val("toi", "pos", f)
    head = [tp[0], tp[1] + HEAD_DY]
    for id in ("energie", "energie_nom"):
        kit.vanish(id, f, into=head, d=7)

    f = kit.at("S18", "règle :", "la pilule-calendrier vient au centre en grandissant et devient « 1 décision / "
                                 "semaine »")
    kit.move("calendrier", f, list(CAL_REGLE_C), MOVE, scale=CAL_REGLE_K)
    cal_swap(S, kit, f, T_CAL["regle"], d_w=8, pulse=False, extra_w=28)

    f = kit.at("S18", "décision", "une onde part de chacune des trois coches de l'escalier, l'une après l'autre, et sa "
                                  "marche bat : une coche = une décision")
    for k in range(3):
        count_rings(S, kit, f + 4 * k, k)

    f = kit.at("S18", "fin", "une barre vide de 52 semaines s'étire hors de la pilule ; « Semaine 1 » et « Fin "
                             "d’année » s'écrivent dessous")
    kit.pop("annee", f, from_pt=list(CAL_REGLE_C), d=MORPH)
    kit.type("annee_s1", f + 6)
    kit.type("annee_fin", f + 6)

    f = kit.at("S18", "l’année,", "chaque coche de l'escalier bat et lance son double, qui vole en arc remplir une "
                                  "case de la barre et y bat ; après la troisième, le compteur paraît sur « 3 » ; puis "
                                  "la barre se remplit jusqu'au bout pendant que le compteur monte à 52")
    f52 = kit.at("S18", "52", "le compteur s'arrête sur « 52 » et bat ; la barre est pleine")
    arr = f
    for k, did in enumerate(DOUBLES):
        g = f + 5 * k
        kit.pulse(COCHES[k], g, peak=1.3)
        S.key(did, "pos", g - 1, list(COCHE_PTS[k]))
        S.key(did, "scale", g - 1, 1)
        arr = kit.move(did, g, list(ANNEE_CASES[k]), 12, "inOut", arc=90, scale=0.7)
        kit.pulse(did, arr, peak=0.95, step=2)
        S.key("annee", "value", arr, round((k + 1) / 52, 5), 2, "out")
        S.key(did, "scale", arr + 4, 0, 3, "in")
        S.key(did, "opacity", arr + 7, 0)
    kit.pop("compteur", arr)                    # « 3 » : après la troisième coche
    g = arr + 4
    fill_d = max(6, f52 - g)
    S.key("annee", "value", g, 1, fill_d, "linear")
    S.key("compteur", "value", g, 52, fill_d, "linear")
    kit.pulse("compteur", max(f52, g + fill_d))

    f = kit.at("S18", "décisions", "« décisions » s'écrit à droite du 52")
    kit.type("decisions", f)

    # ================= S19 : ◀◀ Avant (rembobinage en tour, attente) =================
    f = kit.at("S19", "Avant,", "on rembobine : un grand ◀◀ paraît au centre et y reste, le fond se voile ; barre, "
                                "légendes et compteur rentrent dans la pilule, qui repart en haut à gauche et devient "
                                "« ◀◀ Avant » ; « Toi » redescend l'escalier à reculons jusqu'au sol")
    S.key("voile", "opacity", f, VOILE_OP, FADE, "out")
    kit.pop("rembobine", f)
    f_temps = S.word_after("temps", f)          # contrôle sans son : le grand ◀◀ reste pendant TOUT le rembobinage
    kit.pulse("rembobine", f + 14, peak=1.12, step=3)
    kit.move("calendrier", f, list(CAL_C), MOVE, scale=1)
    cal_swap(S, kit, f, T_CAL["avant"], pulse=False)
    kit.pop("cal_rewind", f + 3, d=6)
    for id in ("annee", "annee_s1", "annee_fin", "compteur", "decisions"):
        kit.vanish(id, f, into="calendrier", d=MORPH)
    g = kit.vanish("rembobine", f_temps, into=list(CAL_C), d=9)
    kit.pulse("calendrier", g, peak=1.12)
    end = toi.run(f, _descent_pts([TOI_M3, TOI_M2, TOI_M1, TOI_P0]), 24)
    toi.hold_low(f, end)
    kit.move("nom_toi", f, list(NOM_SOL), 24)

    f = kit.at("S19", "attendais", "coches et numéros rentrent dans leurs marches ; Budget redevient blanc ; "
                                   "l'escalier se ré-empile en tour par saccades (le trajet de S10 joué à l'envers), "
                                   "l'argent de nouveau au sommet")
    for k in range(3):
        kit.vanish(COCHES[k], f + k, d=FADE)
        kit.vanish(NUMS[k], f + k, d=FADE)
    S.key("bloc1", "fill", f, PAPER, 9, "out")
    _set_stairs(S, f + 2, [tower(i, 100) for i in range(4)], [3, 2, 1, 0], 3, 14, PASTILLE_TOUR[100], rewind=True)

    f = kit.at("S19", "temps", "le grand ◀◀ se range dans la pilule « Avant » ; une horloge paraît au-dessus de « Toi » "
                               "et fait un tour complet, comme en S06, pendant qu'il attend, immobile, devant la tour")
    S.key("cadran", "start", f - 1, 0)
    S.key("cadran", "value", f - 1, 0)
    S.key("cadran", "opacity", f - 1, 1)
    S.key("cadran", "pos", f - 1, list(CADRAN_ATTENTE))   # contrôle sans son : grande, au-dessus de « Toi » qui attend
    kit.pop("cadran", f, d=POP)
    s20 = scene_f0(S, "S20")
    S.key("cadran", "value", f + 6, 60, s20 - 1 - (f + 6), "linear")

    # ================= S20 : Maintenant, une seule marche =================
    f = kit.at("S20", "Maintenant,", "un grand ▶▶ paraît et file se ranger dans la pilule, qui devient « Maintenant » ; "
                                     "le voile se lève, l'horloge rentre ; « Toi » touche du stylo le bord droit du "
                                     "bloc Budget et la tour s'étale de nouveau en escalier, l'argent glisse au sommet")
    S.key("voile", "opacity", f, 0, FADE, "out")
    kit.pop("avance", f, d=6)
    kit.vanish("avance", f + 8, into=list(CAL_C), d=8)
    cal_swap(S, kit, f, T_CAL["maintenant"], pulse=False)
    kit.vanish("cal_rewind", f, d=FADE)
    kit.pulse("calendrier", f + 16, peak=1.1)
    kit.vanish("cadran", f, into=list(CAL_C))
    hit = toi.tap(f - TAP + 1, [TOWER_X + TOWER_W / 2 + 2, 1180])
    assert hit == f, (hit, f)
    kit.pulse("bloc1", hit, peak=1.04)
    toi.lower(hit + 6, 8)
    _set_stairs(S, hit + 3, [stairs(i) for i in range(4)], [0, 1, 2, 3], 3, 14, PASTILLE_ESCALIER)

    f = kit.at("S20", "fais", "« Toi » monte sur la première marche ; son étiquette passe à droite de sa tête")
    _climb(toi, f, TOI_M1_P3, 12)
    kit.move("nom_toi", f, list(NOM_MARCHE), 12)

    f = kit.at("S20", "chose.", "le stylo touche la marche Budget : la coche s'y trace, « 1 » cerclé se réécrit et la "
                                "marche se colore en cyan pâle")
    hit = toi.tap(f - TAP + 1, list(COCHE_PTS[0]))
    _reappear(S, "coche1", hit - 1, draw=0)
    kit.draw("coche1", hit, 6)
    _reappear(S, "num1", hit, draw=0)
    S.key("num1_txt", "chars", hit, 0)
    kit.draw("num1", hit + 1, 8)
    kit.type("num1_txt", hit + 3)
    S.key("bloc1", "fill", hit, LIGHT, 9, "out")
    toi.lower(hit + 6, 8)

    # ================= S21 : l'argent revient dans la main, levé ; la suite notée en tirets =================
    f = kit.at("S21", "tout", "les marches 2, 3 et 4 battent l'une après l'autre, sans coche ; leurs numéros ressortent "
                              "en cercles tiretés : à faire")
    for k, i in enumerate((1, 2, 3)):
        kit.pulse(BLOC_IDS[i], f + 4 * k, peak=1.04)
        kit.pop(f"numt{i + 1}", f + 4 * k)

    f = kit.at("S21", "commencer", "l'argent quitte le sommet et vole jusqu'au bout du stylo de « Toi », qui le lève à "
                                   "bout de bras, au-dessus de sa tête, comme au début ; la pastille bat")
    arr = kit.move("pastille", f, list(PASTILLE_RETOUR), MOVE, "inOut", arc=80)
    toi.reach(f, list(PASTILLE_RETOUR_TIP), MOVE)
    kit.pulse("pastille", arr, peak=1.12)

    f = kit.at("S21", "mieux", "les cercles tiretés 2, 3 et 4 battent l'un après l'autre : la suite est notée, pas "
                               "faite ; « Toi » reste sur la marche 1, l'argent levé, sans les regarder ; puis plus "
                               "rien ne bouge")
    for k, i in enumerate((1, 2, 3)):
        kit.pulse(f"numt{i + 1}", f + 4 * k, peak=1.25)

    # ================= S22 : fin standard ; la pastille devient le bouton =================
    fe = scene_f0(S, "S22")
    outs = []
    for id, e in S.ents.items():                # tout ce qui est encore à l'écran, sauf la pastille, « Toi » et le sol
        if e.get("parent") or id in ("pastille", "sol") or id.startswith("toi") or id.startswith("fin"):
            continue
        if S.val(id, "scale", fe - 1) < 1e-3 or S.val(id, "opacity", fe - 1) < 1e-2:
            continue
        if e["type"] == "shape" and S.val(id, "draw", fe - 1, 1) < 1e-3:
            continue
        outs.append(id)
    out = kit.outro("S22", outs=outs, press="argent.", clear="fade", btn_at=MOVE, labelSize=34)
    S.set(out["cursor"], opacity=0)             # pas de flèche de souris : le stylo de « Toi »
    f, fp = out["card"], out["press"]
    S.key("nom_toi", "opacity", f, 0, FADE, "linear")
    kit.ensure("pastille", "z", S.ents["pastille"]["z"])
    S.key("pastille", "z", f, 41)               # au-dessus de la carte (z 40)
    kit.move("pastille", f, list(FIN_BUTTON), scale=FIN_K)   # « € Ton argent » entière, à la largeur du bouton
    S.key("pastille", "opacity", f + MOVE, 0)   # relais sec : le bouton « S’abonner » paraît à cette image (btn_at)
    toi.set_z(f, 42, tool_z=42.5)               # « Toi » et son stylo au-dessus de la carte
    toi.hop(f, list(TOI_P0), 10)
    toi.lower(f + 10, 8)
    _set_what(S, "S22", f, "tout s'efface sauf l'argent, « Toi » et le sol ; la carte de fin surgit ; la pastille "
              "« Ton argent » quitte le stylo, grandit à la place du bouton et devient « S’abonner » ; « Toi » "
              "redescend au sol")
    hit = toi.tap(fp - TAP + 1, list(FIN_TAP))
    assert hit == fp, (hit, fp)
    _set_what(S, "S22", fp, "« Toi » touche du stylo le coin bas droit du bouton « S’abonner » : il s'enfonce, deux "
              "ondes partent du point touché ; puis plus rien ne bouge")
    for k in range(2):
        S.key(f"fin_onde{k + 1}", "pos", hit - 1, list(FIN_TAP))
    ring(S, "fin_onde1", hit, d=14, s0=0.6, s1=2.1)
    last = ring(S, "fin_onde2", hit + 4, d=14, s0=0.6, s1=2.1)
    toi.lower(hit + 6, 8)
    assert last < film_end(S), (last, film_end(S))
