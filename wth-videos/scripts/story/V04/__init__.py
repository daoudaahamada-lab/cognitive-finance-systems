"""V04 « Ton solde n’est pas ton budget » : mise en scène Story, en paquet (une partie par fichier).

Storyboard : scripts/storyboards/V04.json (v1, révisé après le test sans son, 21 scènes, 87 temps forts, 88,975 s),
version lisible scripts/storyboards/V04.md. Voix : build/V04/words.json (film : images 0-2670).
Fil : le compte de « Toi ». objet_fil = `solde` (pilule cyan « 800 € » en haut de l'écran du téléphone `appli`) :
les 8 pièces `c1`…`c8` naissent d'elle (S01) ; en S02 elle décompte les pièces qui partent (700 € … 0 €) puis vire
au rouge « À découvert » ; elle recompte au rembobinage (S03) ; ensuite elle ne change plus jamais de chiffre pendant
que les pièges retirent les pièces (S09-S20), tremble devant « 200 € » (S10), se relie au gros reflet du miroir
(S14), le fil de la dépense vers elle est barré (S20), et devient le bouton « S’abonner » de la carte de fin (S21).

Parties (scènes contiguës) :
- p1 : S01-S08, images 0-853. Accroche, rembobinage, « Solde » ≠ « Budget », le repère, le panier arrêté par « ≠ »,
  les factures, photo / film, le bac et ses fils (deux pièces par facture), le volet qui cache les factures.
- p2 : S09-S14, images 854-1699. Piège 1 (6 pièces partent le long des fils, « 200 € »), piège 2 (panier coché,
  horloge, carte et sablier, c8 en trois tiers), le miroir.
- p3 : S15-S21, images 1700-2670. Piège 3 (pièce fantôme dans le téléphone, le vide, le virement qui attend), la
  méthode (le stylo pose chaque « − »), « 2 min » une fois par semaine, la décision, la carte de fin.
ENTRY_P2 et ENTRY_P3 (plus bas) sont le contrat des raccords : la partie précédente finit exactement dans cet état,
la suivante l'épingle à first_frame - 1 (kit.pin). Les figurines n'y sont jamais (walk / enter / turn seulement).

Pas d'IA dans V04. « Toi » (figurine encre, échelle 1, pieds sur y 1230) est seul à tenir le stylo. Rouge : la seule
pilule « À découvert » (S02) et son mot du karaoké. Tirets encre = ce qui n'est pas (encore) réel ; trait plein = lien
réel ou geste de « Toi ».

RÈGLE DU BRAS (toutes les parties). « Toi » a le bras du côté gauche de l'écran (side="left") : il ne touche
proprement qu'une cible en haut à gauche de son épaule (dx ≤ −0,3 × dy) à 267 px au plus (arm_check). D'où deux places :
P1 (760, 1135) pour la colonne de droite et P2 (530, 1135) pour les pièces du téléphone.

« Toi » se retourne (S07 « penses. », S12 « oublier ») : relais de deux figurines à la même place (`toi`, bras côté
gauche, tourné vers le téléphone ; `toi_dos`, bras et stylo côté droit, tourné vers la droite), par un resserrement
horizontal de 2 + 2 images (turn) : la silhouette ne change jamais de forme, seul le côté du stylo change.

Écarts d'exécution assumés par rapport au storyboard (tour de revue 1 ; aucun sens changé) :
- téléphone allongé (x 140-460, y 520-1160) ; 8 pièces en 4 rangées de 2 (y 800, 880, 960, 1040) : les rangées 1-3
  sont à la hauteur des trois factures du bac, chaque facture a SA paire de pièces (c1 c2 Loyer, c3 c4 Forfait,
  c5 c6 Assurance), c7 et c8 sur la dernière rangée ;
- PNG remplacés par des formes plates (bac, carte et sablier, miroir et tirelires, vide) : traits encre, aplats light ;
- fils des prélèvements : de chaque facture vers SES deux pièces (fourche) ; en S09 les pièces glissent le long ;
- S07 « penses. » / S12 « oublier » : « Toi » se retourne en entier (stylo du côté droit) au lieu de ranger son stylo
  et de tourner la tête ; S08 « oublier » : un volet glisse sur le bac et cache les factures ;
- S13 : c8 est découpée en trois tiers (traits en tirets dessus), trois tiers en tirets s'alignent sous le sablier ;
- S14 : la petite tirelire est devant le miroir, le gros reflet (cyan profond) dedans grandit sur « haut » ;
- S15 : la pensée de « Toi » est une pièce fantôme en tirets posée dans la place vide de c8, cochée ;
- S16-S17 : deux blocs plats séparés d'un vide encre de 90 px ; le virement attend au bord, horloge sur lui ;
- S18 : « Toi » touche chaque place : chaque « − » sort de son stylo ; S19 : « = » devant c7 ;
- deux temps forts déplacés sur le mot voisin (storyboard mis à jour, storyboard-check OK) : S15 « À » ->
  « l’inverse, », S17 « dépense » -> « pas. ».
"""
import importlib
import math
import os
from types import SimpleNamespace

from pipeline.story import GEOM, STYLE, text_width
from pipeline.story_kit import Figure, Kit

PARTS = ["p1", "p2", "p3"]                      # S01-S08, S09-S14, S15-S21
NBSP, NNBSP = " ", " "                # espace insécable (avant €), fine insécable (milliers)
ALERT_WORDS = {"découvert"}                     # karaoké en rouge : le seul rouge du film (S02 « À découvert »)
ACOUSTIC_SNAP = {"gap": 0.2, "window": 0.08}    # temps fort après un silence : calé sur l'attaque audible
CAPTION_GROUPS = [                              # découpes imposées : pas de négation coupée, pas de mot seul
    ["Ça ne suffit pas"], ["Tant qu’il n’est", "pas crédité"], ["ne le dépense pas"],
    ["moins paiements", "différés"], ["Ce que tu peux", "vraiment dépenser"],
    ["Deuxième piège", "oublier les", "paiements différés"], ["Carte à débit", "différé"],
    ["il y a l’argent", "que tu crois", "déjà avoir"], ["attendu", "n’est pas encore", "à toi"],
]

# ---------- couleurs ----------
INK, CYAN, DEEP, LIGHT = STYLE["ink"], STYLE["cyan"], STYLE["deep"], STYLE["light"]
PAPER, RED, RULE = STYLE["paper"], STYLE["red"], STYLE["rule"]
WHITE = "#FFFFFF"

# ---------- textes à l'écran (typographie française) ----------
def euros(v):
    return f"{v}{NBSP}€"


T_800, T_600, T_200 = euros(800), euros(600), euros(200)
T_DECOUVERT = "À découvert"
T_FIN_MOIS = "fin du mois"
T_2MIN = f"2{NBSP}min"
T_SEMAINE = "1 fois par semaine"
T_MOINS, T_EGAL, T_NEQ = "−", "=", "≠"
T_ABONNER = "S’abonner"
FACTURES = [("Loyer", "house"), ("Forfait", "phone"), ("Assurance", "shield")]
MARKER_LABELS = ["Échéances", "Différés", "Virements"]
REMB, SALAIRE = "Remboursement", "Salaire"
TXT = 34                                   # corps minimal des libellés (32 px au moins)

# ---------- mise en page (1080 x 1920) ----------
X_MIN, X_MAX, Y_MIN, Y_MAX = 40, 940, 160, 1270
CX = 540
GROUND = 1230                              # ligne de sol : pieds de « Toi »
FIG_BASE = GEOM["FIGURE"]["base"]
SHOULDER = (-abs(GEOM["FIGURE"]["shoulder"][0]), GEOM["FIGURE"]["shoulder"][1])   # (-30, -16), bras côté gauche
REACH_OK = 267
TOI_SCALE = 1.0


def fig_pos(x, feet=GROUND, s=TOI_SCALE):
    return [x, round(feet - FIG_BASE * s, 2)]


P1 = fig_pos(760)                          # (760, 1135) : colonne de droite
P2 = fig_pos(530)                          # (530, 1135) : pièces du téléphone
HEAD_DY = GEOM["FIGURE"]["head"]["cy"]     # -64


def arm_check(fig_x, pt, fig_y=P1[1]):
    """(distance épaule -> cible, côté sûr) pour « Toi » centré en (fig_x, fig_y), bras côté gauche."""
    sx, sy = fig_x + SHOULDER[0], fig_y + SHOULDER[1]
    dx, dy = pt[0] - sx, sy - pt[1]
    return round(math.hypot(dx, dy), 1), dx <= -0.3 * max(dy, 0)


def assert_reach(fig_x, pt, what):
    d, ok = arm_check(fig_x, pt)
    assert d <= REACH_OK and ok, f"{what} : hors d'allonge depuis x {fig_x} ({d} px, côté sûr {ok})"


# --- le téléphone (appli bancaire), allongé jusqu'à y 1160 ---
APPLI_C, APPLI_W, APPLI_H, APPLI_R = (300, 840), 320, 640, 36       # x 140-460, y 520-1160
APPLI_TITRE = (0, -268)                    # « Solde » : monde (300, 572)
APPLI_BANQUE = (-78, -268)
APPLI_FILET = (0, -232)                    # monde y 608
SOLDE_C, SOLDE_W, SOLDE_H = (300, 680), 230, 84
SOLDE_BOTTOM = (300, 722)
SOLDE_RIGHT = (SOLDE_W / 2, 0)             # monde (415, 680)
COIN_R = 26
COIN_XS = (262, 338)
COIN_YS = (800, 880, 960, 1040)
COIN_PLACES = [(COIN_XS[k % 2], COIN_YS[k // 2]) for k in range(8)]   # c1 c2 | c3 c4 | c5 c6 | c7 c8
COIN_K = 0.6
CASE_LOCAL = [(x - APPLI_C[0], y - APPLI_C[1]) for x, y in COIN_PLACES]
MONTANT_200 = (300, 1112)                  # S10 : sous c7 et c8, dans le téléphone
EGAL_C = (196, 1040)                       # S19 : « = » devant c7
GHOST = COIN_PLACES[7]                     # S15-S17 : la pièce fantôme dans la place vide de c8
GHOST_TICK = (410, 1012)
GHOST_DOTS = [((470, 1076), 5), ((436, 1070), 7), ((398, 1064), 9)]   # de la tête de « Toi » (P2) vers la pièce

# --- S03-S07 : le cadre « Budget », « ≠ », le ◀◀, la pellicule, le viseur, le flash ---
BUDGET_C, BUDGET_W, BUDGET_H = (740, 720), 300, 400                  # x 590-890, y 520-920
BUDGET_TITRE = (760, 485)
BUDGET_CAL = (674, 485)
NEQ_C = (525, 720)
REMBOBINER_C = (540, 470)                  # S03 : ◀◀ r 48 (S18 : au-dessus du téléphone)
REMBOBINER_S18 = (300, 458)
BANDE_DX, BANDE_W = 140, 20                # pellicule : deux bandes encre à x ± 140 (bords intérieurs ± 130)
PERF_HALF, PERF_DASH = 160, [12, 16]
FILM_DRIFT = 36                            # S06 « film. » : la bande et les factures défilent de 36 px
VISEUR = [((128, 508), [[0, 56], [0, 0], [56, 0]]), ((472, 508), [[-56, 0], [0, 0], [0, 56]]),
          ((128, 1172), [[0, -56], [0, 0], [56, 0]]), ((472, 1172), [[-56, 0], [0, 0], [0, -56]])]
ALERTES_C = [(650, 720), (740, 720), (830, 720)]

# --- repère 1-2-3 légendé, libellés 34 px, style 'kept' (aucun gris) ---
MARKER_Y = 300
MARKER_GAP = max(150, round(max(text_width(t, TXT, 700) for t in MARKER_LABELS) + 12))   # 195
MARKER_XS = [CX - MARKER_GAP, CX, CX + MARKER_GAP]   # 345, 540, 735
MARKER_DISC = [(x, MARKER_Y) for x in MARKER_XS]

# --- le panier ---
PANIER_R = 44
PANIER_S04, PANIER_STOP = (600, 900), (530, 800)     # S04 : sort du stylo, s'arrête sous « ≠ »
PANIER_C = (640, 890)                      # S11-S12
PANIER_COCHE = (40, -42)
PANIER_TAP = (606, 902)                    # S11 « faites, » : côté gauche du panier
PANIER_CARTE, PANIER_CARTE_K = (680, 718), 0.85     # S13 : posé sur la carte
PANIER_S20 = (640, 960)
REACH_S04 = (575, 990)

# --- S05-S11 : les factures, le bac (plat) et ses fils, les montants ---
FACT_W, FACT_H, FACT_R = 260, 90, 14
FACT_DISC_X, FACT_TXT_X = -96, -64
FACT_BUDGET = [(740, 590), (740, 710), (740, 830)]   # S05-S06 : dans le cadre
FACT_K = 0.75
FACT_BAC = [(820, y - 40) for y in COIN_YS[:3]]      # S07-S11 : une facture par rangée de pièces (40 px plus haut :
                                                     # le bac reste au-dessus du stylo de « Toi » en P1)
FACT_SINK = 10
FACT_BAC_SUNK = [(x, y + FACT_SINK) for x, y in FACT_BAC]
COIN_IN_BAC = [(655, 0), (690, 0)]                   # S09 : la paire de pièces à gauche de sa facture (x, dy)
BAC_C, BAC_W, BAC_H = (770, 838), 320, 256           # dos du bac : x 610-930, y 710-966 (rebord jusqu'à 985)
BAC_LIP = (0, 132)                                   # rebord avant (local) : monde y 1010
VOLET_H = 210                                        # S08 : le volet couvre y 750-960 (bord haut de Loyer visible)
MONTANT_600 = (770, 650)
FIN_MOIS_S02, FIN_MOIS_S09 = (300, 470), (770, 574)

# --- S11-S14 : le fil de l'achat, l'horloge, la carte et le sablier, les tiers ---
HORLOGE_R = 40
HORLOGE_T = 0.2                            # S11 : l'horloge à 20 % du fil, côté panier (hors du téléphone)
CARTE_GRP = (760, 700)                     # S12-S14 : carte (680, 710) + sablier (850, 700)
CARTE_LOCAL, SABLIER_LOCAL = (-80, 10), (90, 0)
SABLIER_TOP = (850, 626)                   # haut du sablier (monde)
SABLIER_IN = (850, 662)                    # bulbe du haut (monde)
TIERS_C = [(730, 884), (810, 884), (890, 884)]      # sommet du tiers (arc en haut, à y − 36)
TIERS_R = 40
CARTE_S18_K = 0.55
CARTE_S18 = (630, 985)

# --- S14 : le miroir, la petite tirelire, le gros reflet ---
MIROIR_C = (800, 690)                      # cadre ovale 230 x 300 (x 685-915, y 540-840), pied jusqu'à y 902
MIROIR_W, MIROIR_H = 230, 300
TIRELIRE_C, TIRELIRE_K = (650, 872), 0.55  # petite tirelire, devant le miroir, posée au sol
REFLET_C, REFLET_K = (800, 700), 1.45      # gros reflet (miroir) ; il naît à l'échelle de la petite

# --- S16-S18 : le vide, le virement, les étiquettes, la place d'arrivée ---
VIDE_C = (690, 790)                        # groupe : bloc proche x 462-590, vide 590-680, bloc lointain 680-920
BLOC_TOP = 720
VIREMENT_R = 34
VIREMENT_FROM, VIREMENT_STOP = (880, BLOC_TOP - VIREMENT_R), (716, BLOC_TOP - VIREMENT_R)
HORLOGE_VIREMENT, HORLOGE_VIR_K = (752, 650), 0.65
ETIQ_REMB, ETIQ_SAL = (770, 598), (770, 528)
CASE_ARRIVEE = (510, BLOC_TOP - VIREMENT_R)

# --- S18-S20 : la méthode, la semaine, la décision ---
MOINS_C = [(500, 850), (500, 985)]
TAP_MOINS = [(615, 885), (600, 985)]       # depuis P1 : 261 / 187 px, côté sûr
BAC_S18, BAC_S18_K = (650, 840), 0.7
BAC_COINS = [(600, 826), (650, 826), (700, 826), (600, 862), (650, 862), (700, 862)]
SABLIER_IN_S18 = (680, 964)
TAP_SABLIER_S18 = (680, 982)
FUSION = (740, 920)                        # S19 « Deux » : tout se rassemble ici en « 2 min »
SEMAINE_CASES = [(596 + 48 * k, 790) for k in range(7)]
SEMAINE_CASES2 = [(596 + 48 * k, 846) for k in range(7)]
SEMAINE_TXT = (740, 722)
DECISION_SOLDE = (SOLDE_W / 2, 20)
DECISION_VIA = (360, 1105)
_DA = (PANIER_S20[0] - PANIER_R, PANIER_S20[1] - 8)          # départ du fil en tirets (bord du panier)
_DB = (SOLDE_C[0] + DECISION_SOLDE[0], SOLDE_C[1] + DECISION_SOLDE[1])   # arrivée sur la pilule (415, 700)
_DL = math.dist(_DA, _DB)
_DU = ((_DB[0] - _DA[0]) / _DL, (_DB[1] - _DA[1]) / _DL)
_DP = (_DA[0] + _DU[0] * 0.12 * _DL, _DA[1] + _DU[1] * 0.12 * _DL)   # S20 « jamais » : rature à 12 % du fil
DECISION_STRIKE = (tuple(round(_DP[i] - 24 * (-_DU[1], _DU[0])[i], 1) for i in range(2)),
                   tuple(round(_DP[i] + 24 * (-_DU[1], _DU[0])[i], 1) for i in range(2)))

# --- S21 : fin ---
FIN_C = (540, 760)
FIN_BUTTON = (540, 908)
FIN_TAP = (664, 962)
SOLDE_BTN_SCALE = 112 / SOLDE_H


def scene_f0(S, sid):
    return round(next(s for s in S.sb["scenes"] if s["id"] == sid)["t_start"] * S.fps)


def pill(S, id, pos, text, size=TXT, weight=700, fill=LIGHT, h=60, z=12, parent=None, scale=0, pad=40, w=None,
         **p):
    if w is None:
        w = round(text_width(text, size, weight) + pad + (30 if p.get("icon") else 0))
    S.add(id, "pill", z=z, parent=parent, text=text, w=w, h=h, size=size, weight=weight, fill=fill, **p)
    S.set(id, pos=list(pos), scale=scale, opacity=1)
    return id


def ring(S, id, f, d=8, s0=0.8, s1=1.35):
    S.key(id, "scale", f - 1, s0)
    S.key(id, "opacity", f - 1, 0)
    S.key(id, "opacity", f, 1)
    S.key(id, "scale", f, s1, d, "out")
    S.key(id, "opacity", f + 2, 0, d - 2, "linear")
    return f + d


def bulle_ronds(head_c, corner, radii=(6, 9, 12), head_r=35):
    hx, hy = head_c
    vx, vy = corner[0] - hx, corner[1] - hy
    L = math.hypot(vx, vy)
    ux, uy = vx / L, vy / L
    start, end = head_r + 4, L - 4
    return [[round(hx + ux * (start + (end - start) * (0.12 + 0.36 * k)), 1),
             round(hy + uy * (start + (end - start) * (0.12 + 0.36 * k)), 1)] for k in range(len(radii))]


def turn(S, a, b, f, d=2):
    """« Toi » se retourne : la figurine a (visible) se resserre (sx 1 -> 0, d images), puis la figurine b (cachée,
    même place, bras de l'autre côté) s'élargit (sx 0 -> 1). Bras et stylo de a s'effacent au départ, ceux de b
    paraissent à l'arrivée. Aucune clé de position : les deux rigs restent accrochés. -> f + 2d."""
    S.key(a.id, "sx", f, 0, d, "in")
    S.key(a.arm, "opacity", f, 0)
    S.key(a.pen, "opacity", f, 0)
    S.key(a.id, "scale", f + d, 0)
    S.key(a.id, "sx", f + d, 1)
    S.key(b.id, "sx", f + d - 1, 0)
    S.key(b.id, "scale", f + d - 1, 1)
    S.key(b.id, "sx", f + d, 1, d, "out")
    S.key(b.arm, "opacity", f + 2 * d - 1, 1)
    S.key(b.pen, "opacity", f + 2 * d - 1, 1)
    return f + 2 * d


def piggy(kit, id, pos, stroke, fill, z, parent=None, mirror=False, scale=0):
    """Tirelire plate (corps 120 x 84 à l'échelle 1, groin, oreille, œil, pattes, fente), tournée vers la droite
    (mirror : vers la gauche)."""
    S = kit.S
    kit.shape(id, pos, kind="ellipse", w=120, h=84, fill=fill, stroke=stroke, sw=5, shadow=4, z=z, parent=parent,
              scale=scale)
    S.set(id, sx=-1 if mirror else 1)
    kit.shape(f"{id}_groin", [60, 4], kind="round", w=22, h=30, r=8, fill=fill, stroke=stroke, sw=5, shadow=0,
              z=z + 0.1, parent=id)
    kit.shape(f"{id}_oreille", [28, -40], kind="poly", pts=[[-12, 6], [2, -14], [12, 8]], fill=fill, stroke=stroke,
              sw=5, shadow=0, z=z - 0.05, parent=id)
    kit.shape(f"{id}_oeil", [34, -12], kind="circle", w=9, fill=stroke, stroke=stroke, sw=0, shadow=0, z=z + 0.1,
              parent=id)
    for j, x in enumerate((-30, 26)):
        kit.shape(f"{id}_patte{j + 1}", [x, 44], kind="round", w=18, h=22, r=5, fill=fill, stroke=stroke, sw=5,
                  shadow=0, z=z - 0.05, parent=id)
    kit.shape(f"{id}_fente", [-6, -26], kind="poly", pts=[[-14, 0], [14, 0]], closed=False, fill="none",
              stroke=stroke, sw=5, shadow=0, z=z + 0.1, parent=id)
    return id


def pie_third(a0, r, n=8):
    """Tiers de disque (120°) de rayon r à partir de l'angle a0 (degrés, 0 = midi, sens horaire), centré sur le
    centre du disque : polygone fermé."""
    pts = [[0, 0]]
    for i in range(n + 1):
        a = math.radians(a0 + 120 * i / n)
        pts.append([round(r * math.sin(a), 2), round(-r * math.cos(a), 2)])
    return pts


COINS = [f"c{k + 1}" for k in range(8)]
CASES = [f"case{k + 1}" for k in range(8)]
FACT_IDS = [f"facture{k + 1}" for k in range(3)]
FILS = [f"fil_mandat{k + 1}{s}" for k in range(3) for s in ("a", "b")]   # a : pièce de droite, b : de gauche
FIL_COIN = {f"fil_mandat{k + 1}{s}": COINS[2 * k + (1 if s == "a" else 0)] for k in range(3) for s in ("a", "b")}
FIL_SAG_B = -14                            # le fil de la pièce de gauche passe au-dessus de sa voisine
TIERS = ["tiers1", "tiers2", "tiers3"]
COUPES = ["c8_coupe1", "c8_coupe2", "c8_coupe3"]
SABLE = ["sable1", "sable2", "sable3"]
SEM1 = [f"semaine_case{k + 1}" for k in range(7)]
SEM2 = [f"semaine2_case{k + 1}" for k in range(7)]
MARQ_OVER = [(f"marqueur_disque{k + 1}", f"marqueur_coche{k + 1}") for k in range(3)]

# ---------- raccords ----------
_OFF = lambda *ids: {i: {"scale": 0} for i in ids}   # noqa: E731

ENTRY_P2 = {   # fin de S08 = etat_initial de S09 : volet fermé sur les factures, six fils tendus, 8 pièces, repère 1
    "appli": {"pos": list(APPLI_C), "scale": 1, "opacity": 1},
    "solde_titre": {"under": 1},
    "solde": {"pos": list(SOLDE_C), "scale": 1, "opacity": 1, "fill": CYAN.lower(), "text": T_800},
    "solde_alerte": {"opacity": 0},
    **{c: {"pos": list(p), "scale": 1, "opacity": 1, "rot": 0} for c, p in zip(COINS, COIN_PLACES)},
    **{c: {"opacity": 0} for c in CASES},
    "bac": {"pos": list(BAC_C), "scale": 1, "opacity": 1},
    "bac_volet": {"sy": 1},
    **{f: {"pos": list(p), "scale": FACT_K, "opacity": 1} for f, p in zip(FACT_IDS, FACT_BAC_SUNK)},
    **{w: {"draw": 1, "from": 0} for w in FILS},
    **{f"{w}_halo": {"opacity": 0} for w in FILS},
    "marqueur": {"pos": [CX, MARKER_Y], "scale": 1, "on": 1, "active": 0, "done0": 0, "done1": 0, "done2": 0},
    "bulle_coche": {"draw": 0},
    **_OFF("budget", "budget_titre", "budget_cal", "neq", "viseur1", "viseur2", "viseur3", "viseur4",
           "alerte1", "alerte2", "alerte3", "rembobiner", "fin_du_mois", "montant_600", "montant_200", "panier",
           "bulle", "bulle_rond1", "bulle_rond2", "bulle_rond3"),
}
ENTRY_P3 = {   # fin de S14 = etat_initial de S15 : miroir, tirelire et reflet reliés, c7 seule, disques 1-2 cochés
    "appli": {"pos": list(APPLI_C), "scale": 1, "opacity": 1},
    "solde_titre": {"under": 1},
    "solde": {"pos": list(SOLDE_C), "scale": 1, "opacity": 1, "fill": CYAN.lower(), "text": T_800},
    "c7": {"pos": list(COIN_PLACES[6]), "scale": 1, "opacity": 1},
    **{c: {"opacity": 1} for i, c in enumerate(CASES) if i != 6},
    "case7": {"opacity": 0},
    "miroir": {"pos": list(MIROIR_C), "scale": 1, "opacity": 1},
    "tirelire": {"scale": TIRELIRE_K}, "reflet": {"scale": REFLET_K},
    "preuve_solde": {"draw": 1}, "preuve_piece": {"draw": 1},
    "marqueur": {"pos": [CX, MARKER_Y], "scale": 1, "on": 1, "active": 1, "done0": 1, "done1": 1, "done2": 0},
    "bulle_coche": {"draw": 0}, "panier_coche": {"draw": 0},
    **_OFF("c1", "c2", "c3", "c4", "c5", "c6", "c8", "bac", "facture1", "facture2", "facture3", "panier",
           "horloge", "carte_sablier", "tiers1", "tiers2", "tiers3", "montant_600", "montant_200", "fin_du_mois",
           "bulle", "bulle_rond1", "bulle_rond2", "bulle_rond3"),
}


def cast(S, kit):
    """Toute la distribution, à son état de l'image 0. Ce qui arrive plus tard : scale=0 (ou opacity=0, draw=0)."""

    # --- le téléphone ---
    kit.shape("appli", APPLI_C, kind="round", w=APPLI_W, h=APPLI_H, r=APPLI_R, fill=PAPER, stroke=INK, sw=5,
              shadow=6, z=2)
    kit.text("solde_titre", APPLI_TITRE, "Solde", size=TXT, weight=700, z=2.2, parent="appli", underColor=DEEP)
    S.set("solde_titre", under=0)
    kit.icon("appli_banque", APPLI_BANQUE, "bank", s=34, z=2.2, parent="appli")
    kit.shape("appli_filet", APPLI_FILET, kind="rect", w=260, h=3, fill=RULE, stroke=RULE, sw=0, shadow=0, z=2.1,
              parent="appli")
    for cid, pt in zip(CASES, CASE_LOCAL):
        kit.shape(cid, pt, kind="circle", w=2 * COIN_R, fill="none", stroke=INK, sw=3, dash=[8, 7], shadow=0, z=2.5,
                  parent="appli", opacity=0)
    kit.shape("flash", APPLI_C, kind="round", w=APPLI_W, h=APPLI_H, r=APPLI_R, fill=WHITE, stroke=WHITE, sw=0,
              shadow=0, z=7.5, opacity=0)

    # --- la pilule du fil « 800 € » ---
    S.add("solde", "pill", z=3, text=T_800, w=SOLDE_W, h=SOLDE_H, size=48, weight=800, fill=CYAN)
    S.set("solde", pos=list(SOLDE_C), scale=1, opacity=1, text=T_800, fill=CYAN, w=SOLDE_W)
    kit.text("solde_alerte", [0, 0], T_DECOUVERT, size=TXT, weight=700, color=PAPER, z=3.1, parent="solde", opacity=0)

    # --- les 8 pièces ; c8 porte ses trois coupes en tirets (S13) ; c7 l'anneau de S19 ---
    for cid, pt in zip(COINS, COIN_PLACES):
        kit.icon(cid, pt, "euro", disc=COIN_R, fill=LIGHT, shadow=3, z=6, scale=0)
        S.set(cid, rot=0)
    S.set("c7", ring=0)
    for k in range(3):
        a = math.radians(120 * k)
        kit.shape(COUPES[k], [0, 0], kind="poly", pts=[[0, 0], [round(COIN_R * math.sin(a), 2),
                                                               round(-COIN_R * math.cos(a), 2)]],
                  closed=False, fill="none", stroke=INK, sw=4, dash=[5, 4], shadow=0, z=6.2, parent="c8", draw=0)
    kit.text("egal", EGAL_C, T_EGAL, size=64, weight=800, color=DEEP, z=6.5, scale=0)

    # --- S03 : ◀◀, « ≠ », le cadre « Budget » (tirets dès la 1re image, aplat light en S06) ---
    kit.icon("rembobiner", REMBOBINER_C, "rewind", disc=48, s=44, fill=LIGHT, shadow=4, z=9, scale=0)
    kit.text("neq", NEQ_C, T_NEQ, size=80, weight=800, z=2.1, scale=0)
    kit.shape("budget", BUDGET_C, kind="round", w=BUDGET_W, h=BUDGET_H, r=24, fill=LIGHT, stroke=INK, sw=4,
              dash=[14, 10], shadow=0, z=2, scale=0)
    S.set("budget", fillOp=0)
    kit.text("budget_titre", BUDGET_TITRE, "Budget", size=TXT, weight=700, z=2.1, opacity=0)
    kit.icon("budget_cal", BUDGET_CAL, "cal", s=34, z=2.1, opacity=0)
    for k, sx in enumerate((-BANDE_DX, BANDE_DX)):
        b = f"bande{k + 1}"
        kit.shape(b, [sx, 0], kind="rect", w=BANDE_W, h=BUDGET_H, fill=INK, stroke=INK, sw=0, shadow=0, z=2.3,
                  parent="budget")
        S.set(b, sy=0)
        kit.shape(f"perf{k + 1}", [0, 0], kind="poly", pts=[[0, -PERF_HALF], [0, PERF_HALF]], closed=False,
                  fill="none", stroke=PAPER, sw=10, dash=PERF_DASH, shadow=0, z=2.4, parent=b)

    # --- S06 : le viseur ---
    for k, (pos, pts) in enumerate(VISEUR):
        kit.shape(f"viseur{k + 1}", pos, kind="poly", pts=pts, closed=False, fill="none", stroke=DEEP, sw=8,
                  shadow=0, z=7, scale=0)

    # --- S04 : les trois alertes ; le repère 1-2-3 (libellés 34 px à l'encre, style 'kept') ---
    for k in range(3):
        kit.icon(f"alerte{k + 1}", BUDGET_C, "warning", disc=34, s=34, fill=PAPER, shadow=4, z=8, scale=0)
    kit.steps_marker(MARKER_LABELS, id="marqueur", y=MARKER_Y, cx=CX, gap=MARKER_GAP, z=20)
    S.ents["marqueur"]["p"].update(moveBlank=True, labelSize=TXT, doneStyle="kept")
    S.set("marqueur", scale=0, on=0, done0=0, done1=0, done2=0)
    for k, (dk, ck) in enumerate(MARQ_OVER):      # coche du piège rangé, posée DANS le disque actif (cyan)
        kit.shape(dk, [MARKER_XS[k] - CX, 0], kind="circle", w=2 * GEOM["MARKER"]["activeR"], fill=CYAN,
                  stroke=INK, sw=4, shadow=0, z=20.2, parent="marqueur", opacity=0)
        kit.tick(ck, [MARKER_XS[k] - CX, 1], INK, size=34, sw=7, z=20.3, parent="marqueur", draw=0)

    # --- les trois factures (libellé SemiBold 34) ---
    for k, ((txt, ico), pos) in enumerate(zip(FACTURES, FACT_BUDGET)):
        fid = FACT_IDS[k]
        kit.shape(fid, pos, kind="round", w=FACT_W, h=FACT_H, r=FACT_R, fill=PAPER, stroke=INK, sw=4, shadow=6, z=4,
                  scale=0, opacity=0)
        kit.icon(f"{fid}_icone", [FACT_DISC_X, 0], ico, disc=22, fill=LIGHT, shadow=0, z=4.1, parent=fid)
        kit.text(f"{fid}_txt", [FACT_TXT_X, 0], txt, size=TXT, weight=600, anchor="start", z=4.1, parent=fid)

    # --- le bac (plat) : dos light, volet qui monte (S08), rebord avant ---
    kit.shape("bac", BAC_C, kind="round", w=BAC_W, h=BAC_H, r=18, fill=LIGHT, stroke=INK, sw=4, shadow=6, z=3.8,
              scale=0)
    vb = BAC_H / 2 - 6                                   # bas du volet (local)
    kit.shape("bac_volet", [0, vb], kind="round", w=BAC_W, h=VOLET_H, r=12, fill=LIGHT, stroke=INK, sw=4,
              shadow=0, z=6.2, parent="bac")
    S.set("bac_volet", sy=0)
    for j, (x0, x1) in enumerate(((-120, -60), (-70, -10))):
        kit.shape(f"bac_reflet{j + 1}", [0, 0], kind="poly", pts=[[x0, 60], [x1, -60]], closed=False, fill="none",
                  stroke=PAPER, sw=10, shadow=0, z=6.25, parent="bac_volet")
    kit.shape("bac_rebord", list(BAC_LIP), kind="round", w=BAC_W + 20, h=30, r=10, fill=LIGHT, stroke=INK, sw=4,
              shadow=4, z=6.3, parent="bac")

    # --- les fils des prélèvements : chaque facture -> SES deux pièces (fourche) ; doublons épais qui battent ---
    for w in FILS:
        k = int(w[len("fil_mandat")]) - 1
        a = {"id": FACT_IDS[k], "at": [-FACT_W / 2, 0]}
        b = {"id": FIL_COIN[w], "at": [0, 0] if w.endswith("a") else [0, -COIN_R]}   # gauche : par le haut
        sag = 0 if w.endswith("a") else FIL_SAG_B
        S.add(f"{w}_halo", "wire", z=5.4, color=DEEP, sw=11, a=a, b=b)
        S.set(f"{w}_halo", draw=1, sag=sag, opacity=0)
        S.set(f"{w}_halo", **{"from": 0})
        S.add(w, "wire", z=5.5, color=DEEP, sw=5, a=a, b=b)
        S.set(w, draw=0, sag=sag, opacity=1)
        S.set(w, **{"from": 0})

    # --- les montants ---
    pill(S, "fin_du_mois", FIN_MOIS_S02, T_FIN_MOIS, fill=LIGHT, h=60, z=9, icon="cal", shadow=4)
    pill(S, "montant_600", MONTANT_600, T_600, size=44, weight=800, fill=PAPER, h=76, z=9, w=190, shadow=6)
    pill(S, "montant_200", MONTANT_200, T_200, size=40, weight=800, fill=LIGHT, h=62, z=9, w=160, shadow=4,
         stroke=DEEP)

    # --- le panier ---
    kit.icon("panier", PANIER_C, "cart", disc=PANIER_R, fill=PAPER, shadow=4, z=10, scale=0)
    kit.tick("panier_coche", list(PANIER_COCHE), DEEP, size=40, sw=8, z=10.1, parent="panier", draw=0)

    # --- le fil de l'achat (tirets ; départ libre pa, arrivée sur c8) et l'horloge (deux aiguilles) ---
    S.add("fil_achat", "wire", z=5.8, color=INK, sw=4, dash=[12, 10], b={"id": "c8", "at": [0, 0]})
    S.set("fil_achat", pa=[PANIER_C[0] - PANIER_R, PANIER_C[1]], draw=0, sag=0, opacity=1)
    S.set("fil_achat", **{"from": 0})
    kit.shape("horloge", [528, 940], kind="circle", w=2 * HORLOGE_R, fill=LIGHT, stroke=INK, sw=4, shadow=4,
              z=10.5, scale=0)
    kit.shape("horloge_h", [0, 0], kind="poly", pts=[[0, 0], [-14, 11]], closed=False, fill="none", stroke=INK, sw=6,
              shadow=0, z=10.6, parent="horloge")
    kit.shape("horloge_m", [0, 0], kind="poly", pts=[[0, 0], [0, -29]], closed=False, fill="none", stroke=INK,
              sw=5, shadow=0, z=10.65, parent="horloge", rot=0)
    kit.shape("horloge_axe", [0, 0], kind="circle", w=10, fill=INK, stroke=INK, sw=0, shadow=0, z=10.7,
              parent="horloge")

    # --- la carte et le sablier (plats), le sable qui coule, les trois tiers en tirets ---
    kit.shape("carte_sablier", CARTE_GRP, kind="circle", w=2, fill="none", stroke="none", sw=0, shadow=0, z=4.4,
              scale=0, opacity=0)
    kit.shape("carte", list(CARTE_LOCAL), kind="round", w=190, h=120, r=14, fill=PAPER, stroke=INK, sw=4, shadow=6,
              z=4.5, parent="carte_sablier")
    kit.shape("carte_bande", [0, -30], kind="rect", w=186, h=20, fill=INK, stroke=INK, sw=0, shadow=0, z=4.55,
              parent="carte")
    kit.shape("carte_puce", [-56, 18], kind="round", w=36, h=28, r=6, fill=LIGHT, stroke=INK, sw=3, shadow=0,
              z=4.55, parent="carte")
    kit.shape("sablier", list(SABLIER_LOCAL), kind="poly",
              pts=[[-36, -68], [36, -68], [6, -4], [6, 4], [36, 68], [-36, 68], [-6, 4], [-6, -4]],
              fill=LIGHT, stroke=INK, sw=4, shadow=6, z=4.5, parent="carte_sablier")
    for j, y in enumerate((-74, 74)):
        kit.shape(f"sablier_barre{j + 1}", [0, y], kind="round", w=96, h=12, r=4, fill=INK, stroke=INK, sw=0,
                  shadow=0, z=4.6, parent="sablier")
    kit.shape("sablier_haut", [0, 0], kind="poly", pts=[[-22, -40], [22, -40], [3, -10], [-3, -10]], fill=INK,
              stroke=INK, sw=2, shadow=0, z=4.6, parent="sablier")
    kit.shape("sablier_bas", [0, 0], kind="poly", pts=[[-30, 64], [30, 64], [0, 40]], fill=INK, stroke=INK, sw=2,
              shadow=0, z=4.6, parent="sablier")
    for s in SABLE:
        kit.shape(s, [0, -6], kind="circle", w=5, fill=INK, stroke=INK, sw=0, shadow=0, z=4.65, parent="sablier",
                  opacity=0)
    for k, pos in enumerate(TIERS_C):
        kit.shape(TIERS[k], pos, kind="poly", pts=pie_third(-60, TIERS_R), fill=LIGHT, stroke=INK, sw=4,
                  dash=[7, 5], shadow=0, z=9, scale=0)

    # --- le miroir (cadre ovale épais, pied), la petite tirelire devant, le gros reflet dedans ---
    kit.shape("miroir", MIROIR_C, kind="ellipse", w=MIROIR_W, h=MIROIR_H, fill=LIGHT, stroke=INK, sw=12, shadow=6,
              z=4.5, scale=0)
    for j, (pa, pb) in enumerate((([-70, -60], [-30, -110]), ([-74, -10], [-10, -112]))):
        kit.shape(f"miroir_reflet{j + 1}", [0, 0], kind="poly", pts=[pa, pb], closed=False, fill="none", stroke=PAPER,
                  sw=9, shadow=0, z=4.55, parent="miroir")
    kit.shape("miroir_pied", [0, 0], kind="poly", pts=[[0, MIROIR_H / 2 + 4], [0, 206]], closed=False, fill="none",
              stroke=INK, sw=10, shadow=0, z=4.45, parent="miroir")
    kit.shape("miroir_socle", [0, 208], kind="round", w=130, h=14, r=6, fill=INK, stroke=INK, sw=0, shadow=0,
              z=4.46, parent="miroir")
    piggy(kit, "reflet", [REFLET_C[0] - MIROIR_C[0], REFLET_C[1] - MIROIR_C[1]], DEEP, PAPER, 4.7,
          parent="miroir", mirror=True)
    piggy(kit, "tirelire", TIRELIRE_C, INK, LIGHT, 6.6)
    S.add("preuve_solde", "wire", z=5.5, color=DEEP, sw=5, a={"id": "solde", "at": list(SOLDE_RIGHT)},
          b={"id": "reflet", "at": [54, 0]})
    S.set("preuve_solde", draw=0, sag=0, opacity=1)
    S.add("preuve_piece", "wire", z=5.5, color=DEEP, sw=5, a={"id": "c7", "at": [18, -18]},
          b={"id": "tirelire", "at": [-60, 0]})
    S.set("preuve_piece", draw=0, sag=0, opacity=1)

    # --- la pièce fantôme (S15-S17) et sa croix ---
    kit.shape("fantome", GHOST, kind="circle", w=2 * COIN_R, fill="none", stroke=INK, sw=4, dash=[7, 5], shadow=0,
              z=6.4, scale=0)
    kit.icon("fantome_euro", [0, 0], "euro", s=30, z=6.45, parent="fantome")
    kit.tick("fantome_coche", list(GHOST_TICK), DEEP, size=36, sw=8, z=6.5, draw=0)
    gx, gy = GHOST
    for j, ((ax, ay), (bx, by)) in enumerate((((-27, -27), (27, 27)), ((27, -27), (-27, 27)))):
        kit.shape(f"fantome_x{j + 1}", [0, 0], kind="poly", pts=[[ax, ay], [bx, by]], closed=False, fill="none",
                  stroke=INK, sw=8, shadow=0, z=6.6, parent="fantome", draw=0)
    for j, (pt, r) in enumerate(GHOST_DOTS):
        kit.shape(f"pensee{j + 1}", list(pt), kind="circle", w=2 * r, fill="none", stroke=INK, sw=3, dash=[5, 4],
                  shadow=0, z=17, scale=0)

    # --- le vide (deux blocs plats, vide encre), le virement, son fil en tirets, les étiquettes, la place ---
    kit.shape("vide", VIDE_C, kind="circle", w=2, fill="none", stroke="none", sw=0, shadow=0, z=4.4, scale=0,
              opacity=0)
    kit.shape("vide_trou", [635 - VIDE_C[0], 800 - VIDE_C[1]], kind="rect", w=90, h=160, fill=INK, stroke=INK, sw=0,
              shadow=0, z=4.45, parent="vide")
    kit.shape("bloc_proche", [526 - VIDE_C[0], 790 - VIDE_C[1]], kind="round", w=128, h=140, r=10, fill=LIGHT,
              stroke=INK, sw=4, shadow=6, z=4.5, parent="vide")
    kit.shape("bloc_loin", [800 - VIDE_C[0], 790 - VIDE_C[1]], kind="round", w=240, h=140, r=10, fill=LIGHT,
              stroke=INK, sw=4, shadow=6, z=4.5, parent="vide")
    kit.icon("virement", VIREMENT_FROM, "euro", disc=VIREMENT_R, fill=LIGHT, shadow=4, z=6.5, scale=0)
    S.set("virement", rot=0)
    kit.shape("case_arrivee", CASE_ARRIVEE, kind="circle", w=2 * VIREMENT_R, fill="none", stroke=INK, sw=4,
              dash=[8, 7], shadow=0, z=6.4, scale=0)
    S.add("vire_fil", "wire", z=6.3, color=DEEP, sw=6, dash=[12, 10], a={"id": "virement", "at": [-VIREMENT_R, 0]},
          b={"id": "case_arrivee", "at": [VIREMENT_R, 0]})
    S.set("vire_fil", draw=0, sag=-70, opacity=1)
    S.set("vire_fil", **{"from": 0})
    pill(S, "etiq_remb", ETIQ_REMB, REMB, fill=LIGHT, h=60, z=9, shadow=4)
    pill(S, "etiq_sal", ETIQ_SAL, SALAIRE, fill=LIGHT, h=60, z=9, shadow=4)

    # --- la méthode : deux « − », la routine « 2 min », deux semaines de sept cases ---
    for k, pos in enumerate(MOINS_C):
        kit.text(f"moins{k + 1}", pos, T_MOINS, size=80, weight=800, z=9, scale=0)
    pill(S, "semaine_pill", FUSION, T_2MIN, size=44, weight=800, fill=LIGHT, h=80, z=9.5, icon="clock", shadow=4)
    for ids, row in ((SEM1, SEMAINE_CASES), (SEM2, SEMAINE_CASES2)):
        for sid, pos in zip(ids, row):
            kit.shape(sid, pos, kind="rect", w=40, h=40, fill=PAPER, stroke=INK, sw=3, shadow=0, z=8.5, scale=0)
    S.set("semaine_case1", fill=PAPER)
    S.set("semaine2_case1", fill=PAPER)
    kit.shape("semaine_balai", SEMAINE_CASES[0], kind="rect", w=48, h=48, fill="none", stroke=CYAN, sw=6, shadow=0,
              z=8.7, scale=0)
    kit.text("semaine_txt", SEMAINE_TXT, T_SEMAINE, size=TXT, weight=700, z=8.5, opacity=0)

    # --- S20 : le fil en tirets panier -> « 800 € » (barré), la rature, le fil plein panier -> c7 ---
    S.add("decision_tirets", "wire", z=5.8, color=INK, sw=4, dash=[12, 10],
          a={"id": "panier", "at": [-PANIER_R, -8]}, b={"id": "solde", "at": list(DECISION_SOLDE)})
    S.set("decision_tirets", draw=0, sag=0, opacity=1)
    S.set("decision_tirets", **{"from": 0})
    (ax, ay), (bx, by) = DECISION_STRIKE
    mx, my = (ax + bx) / 2, (ay + by) / 2
    kit.shape("decision_barre", [mx, my], kind="poly", pts=[[ax - mx, ay - my], [bx - mx, by - my]], closed=False,
              fill="none", stroke=INK, sw=7, shadow=0, z=16.5, draw=0)
    S.add("decision_plein", "wire", z=5.9, color=DEEP, sw=6,
          a={"id": "panier", "at": [-PANIER_R, 6]}, b={"id": "c7", "at": [0, COIN_R]})
    S.set("decision_plein", draw=0, sag=0, opacity=1, via=list(DECISION_VIA))

    # --- la bulle de pensée de S01-S02 (tirets, cochée) ---
    kit.shape("bulle", (745, 905), kind="round", w=190, h=96, r=30, fill="none", stroke=INK, sw=4, dash=[14, 10],
              shadow=0, z=17, scale=0)
    for k, r in enumerate((6, 9, 12)):
        kit.shape(f"bulle_rond{k + 1}", (745, 905), kind="circle", w=2 * r, fill="none", stroke=INK, sw=3,
                  dash=[5, 4], shadow=0, z=17, scale=0)
    kit.tick("bulle_coche", [0, 0], DEEP, size=40, sw=8, z=17.2, parent="bulle", draw=0)

    # --- S21 : ondes du toucher du stylo sur le bouton ---
    for k in range(2):
        kit.shape(f"fin_onde{k + 1}", FIN_TAP, kind="circle", w=70, fill="none", stroke=DEEP, sw=6, shadow=0,
                  z=43.5, opacity=0)

    # --- « Toi » (bras côté gauche, tourné vers le téléphone) et « Toi » retourné (bras côté droit), même place ---
    toi = Figure(kit, "toi", pos=list(P1), scale=TOI_SCALE, z=15)
    S.set("toi", look=0, sx=1)
    dos = Figure(kit, "toi_dos", pos=list(P1), scale=TOI_SCALE, side="right", z=15)
    S.set("toi_dos", scale=0, sx=0)
    S.set(dos.arm, opacity=0)
    S.set(dos.pen, opacity=0)

    return SimpleNamespace(toi=toi, dos=dos, coins=COINS, cases=CASES, factures=FACT_IDS, fils=FILS,
                           marker_xs=list(MARKER_XS))


def build(S):
    kit = Kit(S)
    c = cast(S, kit)
    only = [p for p in os.environ.get("WTH_PARTS", "").split(",") if p]
    for name in PARTS:
        if not only or name in only:
            importlib.import_module(f".{name}", __name__).part(S, kit, c)
