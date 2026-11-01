"""V06 « Ton patrimoine est-il vraiment disponible ? » : mise en scène Story, en paquet (une partie par fichier).

Storyboard : scripts/storyboards/V06.json (v1, révisé après le test sans son, 22 scènes, 88 temps forts, 89,3 s),
version lisible scripts/storyboards/V06.md. Voix : build/V06/words.json (film : images 0-2680).
Fil : ce que possède « Toi ». objet_fil = `pastille` (pilule cyan « 200 000 € ») : posée sur l'appartement (S01),
montée sur la feuille « Estimation » (S07-S10), rangée en haut à droite avec la feuille (S11-S16), sur l'en-tête de
« Ma liste » (S17-S21), rebondit sur la facture de demain sans la payer (S20), devient le bouton « S’abonner » (S22).
Face à elle, toujours la même caisse « Disponible » et la même facture « 3 000 € » (S02-S06, S20-S21).

Parties (scènes contiguës) :
- p1 : S01-S06, images 0-745. Accroche, annonce, « liquidité », le livret qui paie, l'appartement bloqué.
- p2 : S07-S14, images 746-1766. Point 1 (feuille « Estimation », ≠, « ? », « À vendre », la vente lente) et point 2
  jusqu'aux actions.
- p3 : S15-S22, images 1767-2680. PER et épargne salariale derrière le mur, « Ma liste », Délai · Frais · Risque, la
  facture de demain, la ligne qui paie, la carte de fin.
ENTRY_P2 et ENTRY_P3 sont le contrat des raccords (kit.pin à first_frame - 1). Les figurines n'y sont jamais.

TOUR 1 DE REVUE (corrections) — grammaire du point 2 (S11-S16) : une SCÈNE et une ÉCHELLE.
- La scène (bande y 760-1030) : la caisse, le rail fléché vers elle (la frise) et UN SEUL placement actif, posé à sa
  distance de la caisse, son nom juste au-dessus (y ≈ 800), son délai juste dessous (y 960), ses pièces sur le rail.
  Au bout lointain de la frise, la petite horloge presque pleine (S11 « délai. ») : loin = lent.
- L'échelle (en haut à gauche, rangées y 400-700) : quand un placement a montré son délai, il monte s'y ranger avec
  son nom et sa pilule (fond papier) ; le suivant arrive sur la scène. En S17 l'échelle devient « Ma liste ».
- Plus aucune pilule ni nom flottant : chaque texte est collé à son disque ; 34 px au moins sur la scène.
- L'appartement (TOKEN.png) n'est en PNG qu'en grand (S01-S11) ; plus petit, il devient le disque `maison_d`
  (pictogramme maison sur disque light, même famille que les autres placements).

Pas d'IA dans V06. « Toi » (figurine encre, échelle 1, pieds sur y 1230) est seul à tenir le stylo et seul à décider.
Entre deux gestes, son bras est BAISSÉ (`lower` / `hold_low` / `walk_low` ci-dessous : stylo tenu bas, pointe vers
le sol) ; il ne lève le stylo que pour un geste. Rouge : le seul montant « 3 000 € » de la facture impayée (et son
mot du karaoké, et l'éclair rouge du bord de la pilule qui rebondit sur cette facture en S20). Aucun gris.

RÈGLE DU BRAS. Deux figurines à la même place, relayées par `turn` : `toi` (bras côté DROIT) et `toi_g` (bras côté
GAUCHE). Un bras ne touche proprement qu'une cible de son côté (|dx| >= 0,3 x dy) à 267 px au plus (`assert_reach`).
`turn` (V06) passe d'un bras à l'autre sans image sans bras : le bras de a reste jusqu'à l'image où b s'élargit, et la
main de b est posée image par image pendant qu'elle s'élargit (le défaut « main posée à sx 0 » ne se produit plus).
Places : P1 (420, 1135) S01-S16 ; P2 (600, 1135) S17-S18 ; 570 / 620 en S19 ; 620 de S20 à la fin.
"""
import importlib
import math
import os
from types import SimpleNamespace

from pipeline.story import GEOM, STYLE, text_width
from pipeline.story_kit import Figure, Kit, ang_lerp, frames, lerp, solve_ik

PARTS = ["p1", "p2", "p3"]                      # S01-S06, S07-S14, S15-S22
NBSP, NNBSP = " ", " "                # espace insécable, fine insécable
ALERT_WORDS = {f"3{NBSP}000{NBSP}€"}            # karaoké en rouge : « 3 000 €. » (S02), le seul rouge du film
ACOUSTIC_SNAP = {"gap": 0.2, "window": 0.08}    # temps fort après un silence : calé sur l'attaque audible
# Découpes de sous-titres : jamais une négation, un déterminant ou une unité coupée de son mot (≤ 4 mots, ≤ 760 px).
# (un mot à espace insécable de words.json, « 3 000 € » ou « 5 ans », ne peut pas figurer dans une découpe : il est
# laissé à la découpe automatique, juste après la découpe imposée qui le précède)
CAPTION_GROUPS = [["et ne pas", "pouvoir payer", "une facture"],
                  ["avec des frais", "et un prix", "qui n’est pas garanti"],
                  ["Et l’immobilier", "n’est pas", "un cas isolé"],
                  ["chaque placement", "a son propre délai"],
                  ["l’assureur doit", "te verser les fonds", "en deux mois maximum"],
                  ["mais leur prix", "varie"],
                  ["Et l’épargne salariale", "est souvent"],
                  ["Et avec quel risque", "sur le prix"],
                  ["La vraie question", "ce n’est pas", "combien tu possèdes"],
                  ["si tu en as", "besoin demain"]]

# ---------- couleurs ----------
INK, CYAN, DEEP, LIGHT = STYLE["ink"], STYLE["cyan"], STYLE["deep"], STYLE["light"]
PAPER, RED, RULE, BG = STYLE["paper"], STYLE["red"], STYLE["rule"], STYLE["bg"]

# ---------- textes à l'écran (typographie française) ----------
T_200K = f"200{NNBSP}000{NNBSP}€"
T_3000 = f"3{NNBSP}000{NNBSP}€"
T_DISPO, T_FACTURE, T_DEMAIN = "Disponible", "Facture", "demain"
T_LIQUIDITE, T_COMPTE = "liquidité", "3/3"
T_ESTIMATION, T_LISTE = "Estimation", "Ma liste"
T_NEQ, T_Q, T_MOINS = "≠", "?", "−"
T_A_VENDRE, T_FRAIS = "À vendre", "frais"
T_ABONNER = "S’abonner"
T_SANS_PERTE = "sans perte"
T_UNE = "×1"
MARKER_LABELS = ["Délai", "Frais", "Risque"]
# lignes de « Ma liste », du plus rapide au plus lent : (placement, nom, nom de la liste, délai, pictogramme)
ROWS = [("livret", "Comptes, livrets", "Comptes,\nlivrets", "quelques jours", "bank"),
        ("actions", "Actions, fonds", "Actions,\nfonds", "vite", "bars"),
        ("assurance_vie", "Assurance-vie", "Assurance-vie", f"2{NBSP}mois max.", "shield"),
        ("per", "PER", "PER", "à la retraite", "hourglass"),
        ("epargne_salariale", "Épargne salariale", "Épargne\nsalariale", f"5{NBSP}ans", "person"),
        ("maison", "Appartement", "Appartement", "plusieurs mois", "house")]
PLACEMENTS = [r[0] for r in ROWS]
DISC_ID = {pid: ("maison_d" if pid == "maison" else pid) for pid in PLACEMENTS}   # disques (l'appartement : maison_d)
TXT = 34                                        # libellés de la scène
PILL_SIZE, PILL_H = 34, 58                      # pilules (délais, « frais », « À vendre », « demain »)

# ---------- mise en page (1080 x 1920) ----------
X_MIN, X_MAX, Y_MIN, Y_MAX = 40, 940, 160, 1270
GROUND = 1230                                   # ligne de sol : pieds de « Toi »
FIG_BASE = GEOM["FIGURE"]["base"]
HEAD_DY = GEOM["FIGURE"]["head"]["cy"]          # -64 : centre de la tête
HEAD_R = GEOM["FIGURE"]["head"]["r"]
SHOULDER_DX, SHOULDER_DY = abs(GEOM["FIGURE"]["shoulder"][0]), GEOM["FIGURE"]["shoulder"][1]   # 30, -16
REACH_OK = 267
TOI_SCALE = 1.0


def fig_pos(x, feet=GROUND, s=TOI_SCALE):
    return [x, round(feet - FIG_BASE * s, 2)]


P1 = fig_pos(420)                               # (420, 1135) : S01-S16
P2 = fig_pos(600)                               # (600, 1135) : S17-S18
P_FRAIS, P_FIN = fig_pos(570), fig_pos(620)     # S19 « frais » ; S19 « risque » -> fin
TOI_NOM_C = (420, 1000)                         # étiquette « Toi » au-dessus de la tête (S01-S02)

AXE_Y = 880                                     # le rail puis la frise

# --- la caisse « Disponible » (à gauche) ---
CAISSE_C, CAISSE_W, CAISSE_H, CAISSE_R = (170, 880), 220, 240, 22          # x 60-280, y 760-1000
CAISSE_PLACES = [(115, 880), (225, 880), (170, 950)]                       # monde ; S10 : la 3e reste vide
CAISSE_PLACES_LOCAL = [(x - CAISSE_C[0], y - CAISSE_C[1]) for x, y in CAISSE_PLACES]
CAISSE_EDGE_TAP = (275, 950)                    # S02 : bord droit touché par le stylo (toi_g)
CAISSE_HAUT = (170, 292)                        # S17-S21 : en haut à gauche, x 60-280, y 172-412 (au-dessus de la liste)
COIN_R = 26
COMPTE_C = (170, 1045)                          # « 3/3 » (S05, S12) sous la caisse

# --- la facture « 3 000 € » (220 x 150 : titre, montant, rangée des pièces qui la paient), « demain » ---
FACTURE_C, FACTURE_W, FACTURE_H = (170, 680), 220, 150                     # posée sur la caisse : y 605-755
FACTURE_DROP_FROM_Y = 300
FACTURE_OUT = (-220, 680)                       # S06 : sortie par la gauche
FACTURE_TITRE_LOCAL, FACTURE_MONTANT_LOCAL = (0, -44), (0, 2)
FACTURE_COINS_LOCAL = [(-62, 48), (0, 48), (62, 48)]                       # sous le montant, dans la facture
FACTURE_COCHE_LOCAL, FACTURE_COCHE_R = (128, -42), 32                      # coche sur le coin haut droit (libre du « € »)
FACTURE_HAUT = (400, 302)                       # S20-S21 : à droite de la caisse, x 290-510, y 227-377
DEMAIN_HAUT = (400, 196)                        # S20 : « demain » collé sur le bord haut de la facture
PAY_K = 0.7                                     # pièces posées dans la facture (r 18)

# --- l'appartement (TOKEN.png, en grand seulement) et son disque, la pilule du fil ---
MAISON_C, MAISON_W = (700, 880), 220            # x 590-810, y 760-1000
MAISON_TAP = (600, 975)                         # S01 : bas gauche du jeton (toi, bras droit)
MAISON_TAP_S09 = (610, 985)
MAISON_S11_K = round(150 / MAISON_W, 4)         # S11 : 150 px, toujours en PNG (au-dessus de 140 px)
A_VENDRE_LOCAL = (0, 95)                        # enfant de maison : monde (700, 975)
MAISON_BUMP_C = (550 + MAISON_W / 2, 880)       # S06/S09 : centre quand son bord gauche touche le cadenas (550)
PASTILLE_C, PASTILLE_W, PASTILLE_H = (700, 705), 310, 90
PASTILLE_FEUILLE, PASTILLE_FEUILLE_K = (720, 545), 0.85                    # S07-S10
FEUILLE_RANGEE, FEUILLE_RANGEE_K = (810, 250), 0.7                         # S11-S16 : en haut à droite (712-908, 180-320)
PASTILLE_RANGEE = (810, round(250 + 35 * 0.7, 2))                          # sur la feuille rangée
PASTILLE_RANGEE_K = round(PASTILLE_FEUILLE_K * FEUILLE_RANGEE_K, 4)

# --- le rail, puis la frise ---
RAIL_A, RAIL_B = (580, AXE_Y), (280, AXE_Y)     # tracé de l'appartement vers la caisse (draw part de A)
FRISE_A = (920, AXE_Y)                          # S11 : pa glisse de 580 à 920
FLECHE_C = (300, AXE_Y)                         # flèche deep 36 px (282-318), rot 180, pointée sur la caisse
HORLOGE_C, HORLOGE_R = (480, 750), 50           # x 430-530 : libre de « Livret » (325-420)
HORLOGE_FIN, HORLOGE_FIN_K = (905, 880), 0.5    # S11 « délai. » -> S16 : bout lointain de la frise (loin = lent)
TIP_S03 = (310, 905)                            # S03 : pointe levée (toi_g ; 330 passait du mauvais côté)
LIQUIDITE_C = (470, 960)                        # sous le rail : x 365-575 (sous le livret 918, au-dessus de la tête)
PIECE_TIRETS_STOP = (480, AXE_Y)                # S03 : la pièce en tirets s'arrête sous l'horloge

# --- les placements (disques light r 38) sur la scène ---
DISC_R = 38
LIVRET_C = (372, AXE_Y)                         # 334-410 : la flèche (282-318) reste visible
STAGE_C = {"livret": LIVRET_C, "actions": (400, AXE_Y), "assurance_vie": (560, AXE_Y), "per": (800, AXE_Y),
           "epargne_salariale": (800, AXE_Y)}
DROP_FROM_Y = 300                               # les placements tombent du haut (y 300)
NOM_LIVRET_C = (372, 805)                       # S05-S06 « Livret » au-dessus du livret
NOM_Y = 800                                     # noms de la scène : juste au-dessus du disque actif
NOMS = {"livret": ("nom_comptes", "Comptes,\nlivrets"), "assurance_vie": ("nom_assurance_vie", "Assurance-vie"),
        "actions": ("nom_actions", "Actions,\nfonds"), "per": ("nom_per", "PER"),
        "epargne_salariale": ("nom_epargne", "Épargne\nsalariale")}
CADENAS_C = (520, AXE_Y)

# --- les délais (pilules light 34 px) : sur la scène, sous le disque actif ---
DELAIS = {"delai_mois": ("plusieurs mois", None, (480, 665), "maison"),        # S10 au-dessus de l'horloge
          "delai_jours": ("quelques jours", None, (442, 960), "livret"),       # x 299-585 : libre de la caisse
          "delai_2mois": (f"2{NBSP}mois max.", None, (560, 960), "assurance_vie"),
          "delai_vite": ("vite", None, (400, 960), "actions"),
          "delai_retraite": ("à la retraite", "hourglass", (800, 960), "per"),
          "delai_5ans": (f"5{NBSP}ans", "cal", (800, 960), "epargne_salariale")}
DELAI_OF = {v[3]: k for k, v in DELAIS.items()}
DELAI_MOIS_S11 = (700, 1000)                    # S11 : sous l'appartement réduit
COURBE_C = (400, 700)                           # S14 : au-dessus de « Actions, fonds » (nom 752-828)
COURBE_PTS = [[-60, 20], [-30, -25], [0, 12], [30, -22], [60, 22]]

# --- l'échelle des placements déjà vus (S11-S16), en haut à gauche ---
LAD_ORDER = ["maison", "livret", "assurance_vie", "actions", "per", "epargne_salariale"]   # ordre d'arrivée
LAD_Y = [400, 475, 550, 625, 700, 775]
LAD_DISC_X, LAD_NAME_X, LAD_PILL_X = 90, 135, 440
LAD_K = round(30 / DISC_R, 4)                   # disques de l'échelle : r 30


def lad_pt(pid):
    return (LAD_DISC_X, LAD_Y[LAD_ORDER.index(pid)])


def pill_w(text, icon=None, pad=40):
    return round(text_width(text, PILL_SIZE, 700) + pad + (30 if icon else 0))


def lad_pill_pt(did):
    txt, ico, _pos, pid = DELAIS[did]
    return (LAD_PILL_X + pill_w(txt, ico) / 2, LAD_Y[LAD_ORDER.index(pid)])


# --- point 1 : la feuille « Estimation », « ≠ », « ? », « À vendre », « frais » ---
FEUILLE_C, FEUILLE_W, FEUILLE_H = (720, 510), 280, 200                     # x 580-860, y 410-610
BANDEAU_LOCAL, BANDEAU_W, BANDEAU_H = (0, -72), 272, 52
DIFFERENT_C = (445, 712)                        # S07 : sur la droite pilule (720, 545) -> places de la caisse
LIEN_PILULE = ((596, 588), (488, 675))          # tirets : bas gauche de la pilule -> « ≠ »
LIEN_CAISSE = ((282, 790), (398, 735))          # tirets : haut droit de la caisse -> « ≠ »
DOUTE_C = (912, 545)                            # S08 : « ? » 96 px à droite de la pilule (885-940)
FOURCHETTE = [(-34, 16), (34, 16)]              # S08 : deux pilules fantômes en tirets derrière la pilule (local feuille)
FRAIS_S10, FRAIS_PIECE_S10 = (480, 965), (405, 965)

# --- le mur de briques à cadenas et sa porte (S15-S16) ---
MUR_C, MUR_W, MUR_H = (640, AXE_Y), 50, 200     # x 615-665, y 780-980
MUR_CADENAS_LOCAL = (0, -100)                   # monde (640, 780)
MUR_CONTACT_X = 665 + COIN_R                    # centre d'une pièce qui cogne le mur
PORTE_W, PORTE_H = 64, 110                      # porte deep 5 px, déborde du mur des deux côtés

# --- point 3 : « Ma liste » (la feuille qui grandit), S17-S21 ---
LIST_C, LIST_W, LIST_H, LIST_HEAD = (490, 720), 880, 600, 80               # x 50-930 (ombre 936), y 420-1020
ROWS_Y = [543, 629, 715, 801, 887, 973]
COL_DISC, COL_NAME, COL_DELAI, COL_FRAIS, COL_RISQUE = 84, 118, 486, 659, 832
CELL_H, CELL_DELAI_W, CELL_FRAIS_W, CELL_RISQUE_W = 66, 250, 80, 180
LIST_TXT = 32
LIST_DISC_K = round(24 / DISC_R, 4)             # disques des placements dans la liste : r 24
LISTE_TITRE_X = 76
PASTILLE_LISTE, PASTILLE_LISTE_K = (790, 460), 0.7                         # sur l'en-tête de la liste
ANNEAU_W, ANNEAU_H = 856, 84                    # S21 : anneau (gélule) de la ligne 1, 12 px à l'intérieur de la carte


def list_local(x, y):
    """Point monde de la liste (S17-S21) -> repère local de la feuille (enfants)."""
    return [x - LIST_C[0], y - LIST_C[1]]


def row_pt(i, col):
    return [col, ROWS_Y[i]]


# --- le repère 1-2-3 « Délai · Frais · Risque », au-dessus des colonnes ---
MARKER_Y = 322                                  # légende vers y 384 ; la carte commence en 420
MARKER_GAP = COL_FRAIS - COL_DELAI              # 173
MARKER_XS = [COL_DELAI, COL_FRAIS, COL_RISQUE]
MARKER_LABEL_SIZE = 32

# --- bulles de pensée ---
BULLE_S07, BULLE_S07_W, BULLE_S07_H = (190, 1085), 200, 100
BULLE_RONDS_R = (6, 8, 10)

# --- S22 : fin (kit.outro, pos (540, 720), 620 x 520 : bouton centré (540, 868)) ---
FIN_C = (540, 720)
FIN_BUTTON = (540, 868)
FIN_TAP = (718, 915)                            # bas droit du bouton, hors du libellé (toi depuis x 620)
PASTILLE_BTN_W, PASTILLE_BTN_H = 380, 112


def scene_f0(S, sid):
    return round(next(s for s in S.sb["scenes"] if s["id"] == sid)["t_start"] * S.fps)


# ---------- l'allonge de « Toi » ----------
def arm_check(fig_x, pt, side="right", fig_y=P1[1]):
    """(distance épaule -> cible, côté sûr, dégagement de la tête) pour une figurine en (fig_x, fig_y)."""
    m = 1 if side == "right" else -1
    sx, sy = fig_x + m * SHOULDER_DX, fig_y + SHOULDER_DY
    dx, dy = pt[0] - sx, sy - pt[1]
    d = math.hypot(dx, dy)
    safe = dx * m >= 0.3 * max(dy, 0)
    hx, hy = fig_x, fig_y + HEAD_DY
    ux, uy = (pt[0] - sx) / max(d, 1e-6), (pt[1] - sy) / max(d, 1e-6)
    clear = min(math.hypot(sx + ux * t - hx, sy + uy * t - hy) for t in range(0, int(min(d, 120)) + 1))
    return round(d, 1), safe, round(clear, 1)


def assert_reach(fig_x, pt, what, side="right", fig_y=P1[1]):
    d, safe, clear = arm_check(fig_x, pt, side, fig_y)
    assert d <= REACH_OK and safe and clear >= HEAD_R + 8, \
        f"{what} : hors d'allonge depuis x {fig_x} ({side}) : {d} px, côté sûr {safe}, tête {clear} px"


# ---------- bras baissé (pose de repos de V06) ----------
LOW_GRIP = (52, 40)          # prise du stylo, repère de la figurine (x du côté du bras) : à la hanche
LOW_ROT = 58                 # stylo vers le bas et vers l'extérieur (côté droit ; côté gauche : 180 - 58)


def low_pose(fig, n):
    G = fig._body_pt([fig.m * LOW_GRIP[0], LOW_GRIP[1]], n)
    rot = (LOW_ROT if fig.m > 0 else 180 - LOW_ROT) + fig.S.val(fig.id, "lean", n, 0)
    return G, rot


def lower(fig, f, d=8, e="inOut"):
    """Le bras redescend : stylo tenu bas, à la hanche, pointe vers le sol (pose de repos de V06). -> f + d."""
    rel0, r0 = fig._start(f)
    for n, p in frames(f, d, e):
        A = fig._shoulder(n)
        G, rot = low_pose(fig, n)
        fig._pose(n, lerp([A[0] + rel0[0], A[1] + rel0[1]], G, p), ang_lerp(r0, rot, p))
    return f + d


def hold_low(fig, fa, fb):
    """Images [fa, fb) : bras baissé, posé image par image (le corps peut bouger ou s'élargir)."""
    for n in range(fa, fb):
        G, rot = low_pose(fig, n)
        fig._pose(n, G, rot)


def walk_low(fig, f, to, d=None, e="inOut"):
    """Marche (comme Figure.walk) mais bras baissé du début à la fin. -> f + d."""
    S = fig.S
    p0 = S.val(fig.id, "pos", f - 1)
    to = [to, p0[1]] if isinstance(to, (int, float)) else list(to)
    if math.dist(p0, to) < 0.5:
        return f
    d = d or max(8, math.ceil(math.dist(p0, to) / 7))
    fig._move_body(f, d, to, e)
    k0 = min(6, d)
    rel0, r0 = fig._start(f)
    for n, p in frames(f, k0, "out"):
        A = fig._shoulder(n)
        G, rot = low_pose(fig, n)
        fig._pose(n, lerp([A[0] + rel0[0], A[1] + rel0[1]], G, p), ang_lerp(r0, rot, p))
    hold_low(fig, f + k0, f + d)
    return f + d


def lean_low(fig, f, deg, d=9, e="out"):
    """Incline la figurine, bras baissé qui suit. -> f + d."""
    fig.kit.ensure(fig.id, "lean", 0)
    fig.S.key(fig.id, "lean", f, deg, d, e)
    hold_low(fig, f, f + d)
    return f + d


def turn(S, a, b, f, d=2):
    """« Toi » change de bras : a (visible) se resserre (sx 1 -> 0, d images) pendant que b (cachée, bras de l'autre
    côté) s'élargit À LA PLACE DE a (sx 0 -> 1) à partir de f + d - 1 : à chaque image, un corps et un bras sont
    visibles. Le bras de a s'efface à f + d - 1, celui de b paraît sur la même image, sa main posée bras baissé image
    par image pendant qu'elle s'élargit (jamais posée à sx 0). -> f + 2d."""
    pos = S.val(a.id, "pos", f + d - 1)
    S.key(a.id, "sx", f, 0, d, "in")
    S.key(a.arm, "opacity", f + d - 1, 0)
    S.key(a.pen, "opacity", f + d - 1, 0)
    S.key(a.id, "scale", f + d, 0)
    S.key(a.id, "sx", f + d, 1)
    S.key(b.id, "pos", f + d - 2, [round(pos[0], 3), round(pos[1], 3)])
    S.key(b.id, "sx", f + d - 2, 0)
    S.key(b.id, "scale", f + d - 2, b.size)
    S.key(b.id, "sx", f + d - 1, 1, d, "out")
    S.key(b.arm, "opacity", f + d - 1, 1)
    S.key(b.pen, "opacity", f + d - 1, 1)
    S.key(b.pen, "scale", f + d - 2, b.size)
    hold_low(b, f + d - 1, f + 2 * d + 1)
    return f + 2 * d


# ---------- petites fabriques ----------
def pill(S, id, pos, text, size=PILL_SIZE, weight=700, fill=LIGHT, h=PILL_H, z=11.5, parent=None, scale=0, pad=40,
         w=None, shadow=4, **p):
    if w is None:
        w = round(text_width(text, size, weight) + pad + (30 if p.get("icon") else 0))
    S.add(id, "pill", z=z, parent=parent, text=text, w=w, h=h, size=size, weight=weight, fill=fill, shadow=shadow, **p)
    S.set(id, pos=list(pos), scale=scale, opacity=1, fill=fill)
    return id


def coin(kit, id, pos, r=COIN_R, z=11, parent=None, scale=0):
    """Une pièce : disque light, « € » encre, contour encre 4, ombre +3."""
    kit.icon(id, list(pos), "euro", disc=r, fill=LIGHT, shadow=3, z=z, parent=parent, scale=scale)
    kit.S.set(id, rot=0)
    return id


def ring(S, id, f, d=8, s0=0.8, s1=1.35):
    """Onde d'impact (cercle deep) : paraît à f, grandit et s'efface en d images. -> f + d."""
    S.key(id, "scale", f - 1, s0)
    S.key(id, "opacity", f - 1, 0)
    S.key(id, "opacity", f, 1)
    S.key(id, "scale", f, s1, d, "out")
    S.key(id, "opacity", f + 2, 0, d - 2, "linear")
    return f + d


def bulle_ronds(head_c, edge, radii=BULLE_RONDS_R, head_r=HEAD_R + 4):
    """Centres des petits ronds de la bulle, de la tête (head_c) vers le bord de la bulle (edge)."""
    hx, hy = head_c
    vx, vy = edge[0] - hx, edge[1] - hy
    L = math.hypot(vx, vy)
    ux, uy = vx / L, vy / L
    start, end = head_r + radii[0], L - radii[-1] - 2
    n = len(radii)
    return [[round(hx + ux * (start + (end - start) * k / (n - 1)), 1),
             round(hy + uy * (start + (end - start) * k / (n - 1)), 1)] for k in range(n)]


# ---------- identifiants ----------
PLACES = [f"place{k + 1}" for k in range(3)]
COINS = {sid: [f"piece_{sid}_{k + 1}" for k in range(3)] for sid in ("s05", "s10", "s12", "s13", "s14", "s15",
                                                                        "s16", "s21")}
LIGNES = [f"ligne{k + 1}" for k in range(6)]
LAD_NOMS = {pid: f"lad_nom_{pid}" for pid in LAD_ORDER}
DROPPED = ["livret", "cadenas", "facture", "frais", "assurance_vie", "actions", "per", "mur", "epargne_salariale"]

# ---------- raccords ----------
_OFF = lambda *ids: {i: {"scale": 0} for i in ids}   # noqa: E731

ENTRY_P2 = {   # fin de S06 = etat_initial de S07 (image 745)
    "caisse": {"pos": list(CAISSE_C), "scale": 1},
    **{p: {"pos": list(q), "scale": 1} for p, q in zip(PLACES, CAISSE_PLACES_LOCAL)},
    "facture": {"pos": list(FACTURE_OUT), "scale": 0},
    "facture_montant": {"color": DEEP.lower()},
    "facture_coche": {"scale": 1},
    "compte": {"opacity": 0},
    "rail": {"draw": 1, "pa": list(RAIL_A), "pb": list(RAIL_B)},
    "rail_halo": {"opacity": 0},
    "rail_fleche": {"scale": 1},
    "horloge": {"pos": list(HORLOGE_C), "scale": 1, "value": 5, "rot": 0},
    "liquidite": {"pos": list(LIQUIDITE_C), "scale": 1, "opacity": 1, "chars": len(T_LIQUIDITE), "mark": 1},
    "livret": {"pos": list(LIVRET_C), "scale": 1},
    "nom_livret": {"scale": 1, "opacity": 1},
    "cadenas": {"pos": list(CADENAS_C), "scale": 1, "opacity": 1, "rot": 0},
    "maison": {"pos": list(MAISON_C), "scale": 1},
    "pastille": {"pos": list(PASTILLE_C), "scale": 1, "rot": 0, "text": T_200K},
    "toi_nom": {"opacity": 0},
    **_OFF("question_toi", "piece_tirets", *COINS["s05"], "feuille", "different", "doute", "bulle", "a_vendre",
           "frais", *DELAIS, *[n for n, _t in NOMS.values()], "actions", "assurance_vie", "per", "epargne_salariale",
           "courbe", "mur", "maison_d", *LAD_NOMS.values()),
}
ENTRY_P3 = {   # fin de S14 = etat_initial de S15 (image 1766)
    "caisse": {"pos": list(CAISSE_C), "scale": 1},
    **{c: {"pos": list(q), "scale": s, "opacity": 1} for c, q, s in zip(COINS["s14"], CAISSE_PLACES, (1.5, 0.6, 1))},
    "compte": {"opacity": 0},
    "rail": {"draw": 1, "pa": list(FRISE_A), "pb": list(RAIL_B)},
    "rail_fleche": {"scale": 1},
    "horloge": {"pos": list(HORLOGE_FIN), "scale": HORLOGE_FIN_K},
    "actions": {"pos": list(STAGE_C["actions"]), "scale": 1},
    "nom_actions": {"scale": 1},
    "delai_vite": {"pos": list(DELAIS["delai_vite"][2]), "scale": 1},
    "courbe": {"pos": list(COURBE_C), "scale": 1, "draw": 1},
    **{DISC_ID[pid]: {"pos": list(lad_pt(pid)), "scale": LAD_K} for pid in ("maison", "livret", "assurance_vie")},
    **{LAD_NOMS[pid]: {"scale": 1} for pid in ("maison", "livret", "assurance_vie")},
    **{DELAI_OF[pid]: {"pos": list(lad_pill_pt(DELAI_OF[pid])), "scale": 1}
       for pid in ("maison", "livret", "assurance_vie")},
    "feuille": {"pos": list(FEUILLE_RANGEE), "scale": FEUILLE_RANGEE_K},
    "pastille": {"pos": list(PASTILLE_RANGEE), "scale": PASTILLE_RANGEE_K, "rot": 0, "text": T_200K},
    "liquidite": {"opacity": 0},
    **_OFF("doute", "a_vendre", "frais", "piece_s10_1", "different", "cadenas", "facture", "bulle", "maison",
           "nom_livret", "nom_comptes", "nom_assurance_vie", "per", "epargne_salariale", "mur", "nom_per",
           "nom_epargne", "delai_retraite", "delai_5ans", *COINS["s15"], *COINS["s16"],
           *[LAD_NOMS[p] for p in ("actions", "per", "epargne_salariale")]),
}


def cast(S, kit):
    """Toute la distribution, à son état de l'image 0. Ce qui arrive plus tard : scale=0 (ou opacity=0, draw=0,
    chars=0). Seuls `fin` et `fin_curseur` naissent dans kit.outro (p3)."""

    # --- le rail (fil plein deep, extrémités libres pa / pb), son doublon épais, sa flèche ---
    S.add("rail_halo", "wire", z=2.9, color=DEEP, sw=11)
    S.set("rail_halo", pa=list(RAIL_A), pb=list(RAIL_B), draw=1, sag=0, opacity=0)
    S.set("rail_halo", **{"from": 0})
    S.add("rail", "wire", z=3, color=DEEP, sw=6)
    S.set("rail", pa=list(RAIL_A), pb=list(RAIL_B), draw=0, sag=0, opacity=1)
    S.set("rail", **{"from": 0})
    kit.icon("rail_fleche", FLECHE_C, "arrow", s=36, color=DEEP, z=10.6, rot=180, scale=0)

    # --- la caisse « Disponible » et ses trois places en tirets ---
    kit.shape("caisse", CAISSE_C, kind="round", w=CAISSE_W, h=CAISSE_H, r=CAISSE_R, fill=PAPER, stroke=INK, sw=5,
              shadow=6, z=4)
    kit.icon("caisse_icone", [-88, -85], "euro", disc=16, fill=LIGHT, shadow=0, z=4.1, parent="caisse")
    kit.text("caisse_titre", [16, -85], T_DISPO, size=32, weight=700, z=4.1, parent="caisse")
    kit.shape("caisse_filet", [0, -55], kind="rect", w=190, h=3, fill=RULE, stroke=RULE, sw=0, shadow=0, z=4.1,
              parent="caisse")
    for pid, pt in zip(PLACES, CAISSE_PLACES_LOCAL):
        kit.shape(pid, list(pt), kind="circle", w=2 * (COIN_R + 2), fill="none", stroke=INK, sw=3, dash=[8, 7],
                  shadow=0, z=4.2, parent="caisse")
        S.set(pid, stroke=INK, sw=3)
        kit.icon(f"{pid}_euro", [0, 0], "euro", s=24, sw=2.5, z=4.25, parent=pid)
    kit.text("compte", COMPTE_C, T_COMPTE, size=36, weight=800, color=DEEP, z=9, typed=True)

    # --- l'appartement (TOKEN.png) et son disque (en petit), la pancarte « À vendre » (enfant) ---
    tok = S.png("TOKEN")
    S.add("maison", "png", z=10.4, src=tok["src"], w=MAISON_W, h=round(MAISON_W * tok["h"] / tok["w"]),
          contact=dict(w=round(MAISON_W * 0.7), h=24, dy=4, blur=10, alpha=0.2))
    S.set("maison", pos=list(MAISON_C), scale=1, opacity=1)
    kit.icon("maison_d", MAISON_C, "house", disc=DISC_R, fill=LIGHT, shadow=4, z=10.5, scale=0)
    pill(S, "a_vendre", A_VENDRE_LOCAL, T_A_VENDRE, fill=PAPER, z=10.6, parent="maison", w=190)

    # --- la pilule du fil « 200 000 € » et son éclair rouge (S20 : elle ne paie pas la facture) ---
    S.add("pastille", "pill", z=12, text=T_200K, w=PASTILLE_W, h=PASTILLE_H, size=52, weight=800, fill=CYAN,
          shadow=6)
    S.set("pastille", pos=list(PASTILLE_C), scale=1, opacity=1, rot=0, text=T_200K, fill=CYAN, w=PASTILLE_W)
    kit.shape("pastille_alerte", [0, 0], kind="round", w=PASTILLE_W + 10, h=PASTILLE_H + 10, r=50, fill="none",
              stroke=RED, sw=7, shadow=0, z=12.2, parent="pastille", opacity=0)
    for k, dx in enumerate((-1, 1)):            # S08 : fourchette (deux pilules fantômes en tirets)
        kit.shape(f"fourchette{k + 1}", [PASTILLE_FEUILLE[0], PASTILLE_FEUILLE[1]], kind="round",
                  w=round(PASTILLE_W * PASTILLE_FEUILLE_K), h=round(PASTILLE_H * PASTILLE_FEUILLE_K), r=38,
                  fill="none", stroke=INK, sw=3, dash=[10, 8], shadow=0, z=11.8, scale=0)

    # --- la facture « 3 000 € » (montant encre -> rouge -> deep, en hex), sa coche, « demain » ---
    kit.shape("facture", FACTURE_C, kind="round", w=FACTURE_W, h=FACTURE_H, r=14, fill=PAPER, stroke=INK, sw=4,
              shadow=6, z=13, scale=0)
    kit.text("facture_titre", list(FACTURE_TITRE_LOCAL), T_FACTURE, size=TXT, weight=700, z=13.1, parent="facture")
    kit.text("facture_montant", list(FACTURE_MONTANT_LOCAL), T_3000, size=44, weight=800, z=13.1, parent="facture")
    S.set("facture_montant", color=INK)
    kit.icon("facture_coche", list(FACTURE_COCHE_LOCAL), "check", disc=FACTURE_COCHE_R, fill=PAPER, color=DEEP,
             shadow=3, z=13.6, parent="facture", scale=0)
    pill(S, "demain", DEMAIN_HAUT, T_DEMAIN, fill=LIGHT, z=13.4, icon="cal")

    # --- les pièces : la pièce en tirets (S03-S04) et un groupe de trois par scène ---
    kit.shape("piece_tirets", RAIL_A, kind="circle", w=2 * COIN_R, fill="none", stroke=INK, sw=3, dash=[8, 7],
              shadow=0, z=11, scale=0)
    kit.icon("piece_tirets_euro", [0, 0], "euro", s=26, sw=2.5, z=11.1, parent="piece_tirets")
    for sid, ids in COINS.items():
        zc = {"s05": 13.5, "s21": 13.5, "s10": 10.3}.get(sid, 11)   # s10 : passent DERRIÈRE le livret
        for cid in ids:
            coin(kit, cid, CAISSE_C, z=zc)
    for cid in (COINS["s15"][0], COINS["s16"][0]):                 # la seule pièce qui passe la porte : cerclée, « ×1 »
        kit.shape(f"{cid}_anneau", [0, 0], kind="circle", w=70, fill="none", stroke=CYAN, sw=6, shadow=0, z=11.2,
                  parent=cid, scale=0)
        kit.text(f"{cid}_un", [0, -52], T_UNE, size=32, weight=800, color=DEEP, z=11.3, parent=cid, scale=0)

    # --- l'horloge (secteur deep sur cadran papier), le « ? » de « Toi » qui la précède, « liquidité » ---
    kit.sector("horloge", HORLOGE_C, start=0, value=0, r=HORLOGE_R, unit=60, face=PAPER, fill=DEEP, ticks=12,
               hand=True, sw=5, shadow=6, z=9, scale=0)
    S.set("horloge", fill=DEEP, rot=0)
    kit.text("question_toi", HORLOGE_C, T_Q, size=100, weight=800, z=12, scale=0)
    kit.text("liquidite", LIQUIDITE_C, T_LIQUIDITE, size=52, weight=800, color=DEEP, z=9, typed=True,
             markColor=LIGHT)
    S.set("liquidite", mark=0)

    # --- les placements (disques light r 38) ---
    for pid, _nom, _nl, _delai, ico in ROWS:
        if pid != "maison":
            kit.icon(pid, STAGE_C[pid], ico, disc=DISC_R, fill=LIGHT, shadow=4, z=10.5, scale=0)
    kit.icon("cadenas", CADENAS_C, "lock", disc=28, fill=PAPER, shadow=4, z=10.7, scale=0)
    S.set("cadenas", rot=0)

    # --- les noms de la scène (Inter Bold 34, au-dessus du disque actif) et « Livret » (S05-S06) ---
    kit.text("nom_livret", NOM_LIVRET_C, "Livret", size=TXT, weight=700, z=11.5, scale=0)
    for pid, (nid, txt) in NOMS.items():
        kit.text(nid, [STAGE_C[pid][0], NOM_Y - (8 if "\n" in txt else 0)], txt, size=TXT, weight=700, z=11.5,
                 scale=0)

    # --- l'échelle : noms (une ligne, Bold 34, ancrés à gauche) ---
    for pid in LAD_ORDER:
        nom = next(r[1] for r in ROWS if r[0] == pid)
        kit.text(LAD_NOMS[pid], [LAD_NAME_X, LAD_Y[LAD_ORDER.index(pid)]], nom, size=TXT, weight=700, anchor="start",
                 z=11.5, scale=0)

    # --- les délais (pilules light, Bold 34) et la courbe en dents de scie ---
    for did, (txt, ico, pos, _pid) in DELAIS.items():
        pill(S, did, pos, txt, fill=LIGHT, z=11.5, icon=ico, pad=40)
    kit.curve("courbe", COURBE_C, COURBE_PTS, draw=0, z=11.5, color=DEEP, sw=6, smooth=False, dot=True, scale=0)

    # --- point 1 : la feuille « Estimation » (pistes w, h : elle grandit en « Ma liste » en S17) ---
    kit.shape("feuille", FEUILLE_C, kind="round", w=FEUILLE_W, h=FEUILLE_H, r=14, fill=PAPER, stroke=INK, sw=4,
              shadow=6, z=10, scale=0)
    S.set("feuille", w=FEUILLE_W, h=FEUILLE_H)
    kit.shape("feuille_bandeau", list(BANDEAU_LOCAL), kind="round", w=BANDEAU_W, h=BANDEAU_H, r=10, fill=LIGHT,
              stroke="none", sw=0, shadow=0, z=10.1, parent="feuille")
    S.set("feuille_bandeau", w=BANDEAU_W, h=BANDEAU_H)
    kit.icon("feuille_icone", [-100, 0], "house", s=30, z=10.2, parent="feuille_bandeau")
    kit.text("feuille_titre", [18, 0], T_ESTIMATION, size=30, weight=700, z=10.2, parent="feuille_bandeau")
    kit.text("liste_titre", list_local(LISTE_TITRE_X, LIST_C[1] - LIST_H / 2 + LIST_HEAD / 2), T_LISTE, size=40,
             weight=800, anchor="start", z=10.2, parent="feuille", scale=0)
    kit.text("different", DIFFERENT_C, T_NEQ, size=120, weight=800, z=11, scale=0)
    for lid, (a, b) in (("lien_pilule", LIEN_PILULE), ("lien_caisse", LIEN_CAISSE)):
        kit.shape(lid, [0, 0], kind="poly", pts=[list(a), list(b)], closed=False, fill="none", stroke=INK, sw=4,
                  dash=[10, 8], shadow=0, z=10.95, draw=0)
    kit.text("doute", DOUTE_C, T_Q, size=96, weight=800, z=12.5, scale=0)
    pill(S, "frais", FRAIS_S10, T_FRAIS, fill=PAPER, z=10.9, w=120)

    # --- point 2 : le mur de briques à cadenas, sa porte deep sur charnière (gauche) et son ouverture ---
    kit.shape("mur", MUR_C, kind="rect", w=MUR_W, h=MUR_H, fill=PAPER, stroke=INK, sw=4, shadow=6, z=10.8, scale=0)
    for k, (y, xs) in enumerate(((-66, (-8,)), (-33, (12,)), (33, (-10,)), (66, (10,)))):
        kit.shape(f"mur_joint{k + 1}", [0, y], kind="rect", w=MUR_W - 4, h=3, fill=INK, stroke=INK, sw=0, shadow=0,
                  z=10.81, parent="mur")
        for j, x in enumerate(xs):
            kit.shape(f"mur_joint{k + 1}_{j}", [x, y + (16 if y > 0 else -16)], kind="rect", w=3, h=30, fill=INK,
                      stroke=INK, sw=0, shadow=0, z=10.81, parent="mur")
    kit.shape("mur_trou", [0, 0], kind="rect", w=MUR_W + 2, h=PORTE_H - 8, fill=BG, stroke="none", sw=0, shadow=0,
              z=10.82, parent="mur", opacity=0)
    kit.shape("mur_trou_rail", [0, 0], kind="rect", w=MUR_W + 2, h=6, fill=DEEP, stroke="none", sw=0, shadow=0,
              z=10.825, parent="mur_trou")      # porte ouverte : le rail se voit à travers le mur
    kit.shape("mur_charniere", [-PORTE_W / 2, 0], kind="rect", w=1, h=1, fill="none", stroke="none", sw=0, shadow=0,
              z=10.83, parent="mur", scale=0)
    S.set("mur_charniere", sx=1)
    kit.shape("mur_porte", [PORTE_W / 2, 0], kind="round", w=PORTE_W, h=PORTE_H, r=6, fill=PAPER, stroke=DEEP, sw=5,
              shadow=0, z=10.84, parent="mur_charniere")
    kit.icon("mur_cadenas", list(MUR_CADENAS_LOCAL), "lock", disc=26, fill=PAPER, shadow=3, z=10.9, parent="mur")

    # --- point 3 : les lignes de « Ma liste » (enfants de la feuille, repère de la liste) ---
    for k, (lid, (pid, _nom, nom_l, delai, _ico)) in enumerate(zip(LIGNES, ROWS)):
        y = ROWS_Y[k]
        kit.text(f"{lid}_nom", list_local(COL_NAME, y), nom_l, size=LIST_TXT, weight=700, anchor="start", z=10.4,
                 parent="feuille", typed=True)
        kit.text(f"{lid}_delai", list_local(COL_DELAI, y), delai, size=LIST_TXT, weight=700, color=DEEP, z=10.4,
                 parent="feuille", typed=True)
        for col, cw, suf in ((COL_DELAI, CELL_DELAI_W, "cdelai"), (COL_FRAIS, CELL_FRAIS_W, "frais"),
                             (COL_RISQUE, CELL_RISQUE_W, "risque")):
            kit.shape(f"{lid}_{suf}", list_local(col, y), kind="round", w=cw, h=CELL_H, r=10, fill="none",
                      stroke=INK, sw=3, dash=[8, 6], shadow=0, z=10.3, parent="feuille", scale=0)
        kit.shape(f"{lid}_barre", list_local(LIST_C[0], y), kind="poly", pts=[[-372, 0], [432, 0]], closed=False,
                  fill="none", stroke=INK, sw=6, shadow=0, z=10.6, parent="feuille", draw=0)
    kit.text("ligne1_sans_perte", list_local(COL_RISQUE, ROWS_Y[0]), T_SANS_PERTE, size=LIST_TXT, weight=700,
             color=DEEP, z=10.45, parent="feuille", typed=True)
    for lid in ("ligne2", "ligne6"):
        k = LIGNES.index(lid)
        kit.text(f"{lid}_q", list_local(COL_RISQUE, ROWS_Y[k]), T_Q, size=48, weight=800, z=10.45, parent="feuille",
                 scale=0)
    kit.text("ligne6_moins", list_local(COL_FRAIS - 20, ROWS_Y[5]), T_MOINS, size=36, weight=800, z=10.45,
             parent="feuille", scale=0)
    coin(kit, "piece_s19", list_local(COL_FRAIS + 16, ROWS_Y[5]), r=18, z=10.45, parent="feuille")
    kit.shape("surligneur", list_local(COL_DELAI, ROWS_Y[5]), kind="round", w=CELL_DELAI_W - 10, h=CELL_H - 10, r=12,
              fill=LIGHT, stroke="none", sw=0, shadow=0, z=10.25, parent="feuille", scale=0)
    kit.shape("anneau", list_local(LIST_C[0], ROWS_Y[0]), kind="round", w=ANNEAU_W, h=ANNEAU_H, r=ANNEAU_H / 2,
              fill="none", stroke=DEEP, sw=6, shadow=0, z=10.5, parent="feuille", draw=0)

    # --- le repère 1-2-3 « Délai · Frais · Risque » (aucun gris : doneStyle 'kept') ---
    kit.steps_marker(MARKER_LABELS, id="marqueur", y=MARKER_Y, cx=COL_FRAIS, gap=MARKER_GAP, z=20)
    S.ents["marqueur"]["p"].update(moveBlank=True, labelSize=MARKER_LABEL_SIZE, doneStyle="kept")
    S.set("marqueur", scale=0, on=0, done0=0, done1=0, done2=0)

    # --- la bulle de pensée en tirets (S07 : petite pilule « 200 000 € » ; S17 : « ? ») ---
    kit.shape("bulle", BULLE_S07, kind="round", w=BULLE_S07_W, h=BULLE_S07_H, r=28, fill="none", stroke=INK, sw=4,
              dash=[14, 10], shadow=0, z=17, scale=0)
    S.set("bulle", w=BULLE_S07_W, h=BULLE_S07_H)
    head = (P1[0], P1[1] + HEAD_DY)
    for k, (pt, r) in enumerate(zip(bulle_ronds(head, (BULLE_S07[0] + BULLE_S07_W / 2, BULLE_S07[1])),
                                    BULLE_RONDS_R)):
        kit.shape(f"bulle_rond{k + 1}", pt, kind="circle", w=2 * r, fill="none", stroke=INK, sw=3, dash=[5, 4],
                  shadow=0, z=17, scale=0)
    S.add("bulle_pilule", "pill", z=17.2, parent="bulle", text=T_200K, w=170, h=52, size=28, weight=800, fill=CYAN,
          shadow=3)
    S.set("bulle_pilule", pos=[0, 0], scale=1, opacity=1)
    kit.text("bulle_q", [0, 0], T_Q, size=56, weight=800, z=17.2, parent="bulle", scale=0)

    # --- S22 : ondes du toucher du stylo sur le bouton (pas de pointeur de souris) ---
    for k in range(2):
        kit.shape(f"fin_onde{k + 1}", FIN_TAP, kind="circle", w=70, fill="none", stroke=DEEP, sw=6, shadow=0,
                  z=43.5, opacity=0)

    # --- « Toi » : bras droit (visible) et son relais bras gauche (caché, même place), l'étiquette « Toi » ---
    toi = Figure(kit, "toi", pos=list(P1), scale=TOI_SCALE, side="right", z=15)
    S.set("toi", look=0, sx=1)
    toi_g = Figure(kit, "toi_g", pos=list(P1), scale=TOI_SCALE, side="left", z=15)
    S.set("toi_g", scale=0, sx=0, look=0)
    S.set(toi_g.arm, opacity=0)
    S.set(toi_g.pen, opacity=0)
    kit.text("toi_nom", TOI_NOM_C, "Toi", size=TXT, weight=700, z=15.2)
    # bras baissé dès l'image 0 (pose de repos de V06), pour les deux figurines
    for fig in (toi, toi_g):
        G, rot = low_pose(fig, 0)
        S.set(fig.pen, pos=[round(G[0], 3), round(G[1], 3)], rot=round(rot, 3))
        S.set(fig.arm, elbow=[round(v, 3) for v in solve_ik(fig._shoulder(0), G, fig.l1, fig.l2, fig.bend)[0]])

    for i in DROPPED:                            # kit.drop rend visible à f - 1 (échelle) : opacité 0 jusqu'à f
        S.set(i, opacity=0)

    return SimpleNamespace(toi=toi, toi_g=toi_g, places=PLACES, coins=COINS, lignes=LIGNES, placements=PLACEMENTS)


def build(S):
    kit = Kit(S)
    c = cast(S, kit)
    only = [p for p in os.environ.get("WTH_PARTS", "").split(",") if p]   # WTH_PARTS=p2 : cette partie seule
    for name in PARTS:
        if not only or name in only:
            importlib.import_module(f".{name}", __name__).part(S, kit, c)
