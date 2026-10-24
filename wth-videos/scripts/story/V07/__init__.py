"""V07 « Ton ETF te rend vraiment diversifié ? » : mise en scène Story, en paquet (une partie par fichier).

Storyboard : scripts/storyboards/V07.json (v1, révisé après le test sans son, 22 scènes, 94 temps forts, 98,9 s),
version lisible scripts/storyboards/V07.md. Voix : build/V07/words.json (film : images 0-2967).
Fil : l'étiquette cyan « ETF Monde » (`etiquette`, pilule 240 x 60) collée sur le panier de « Toi » (`panier`). Le
panier fermé de l'accroche (S01) est ouvert par le contexte (S05), attaché au livre de l'indice (`livre`, BOOK.png),
devient la balance (`balance`, S12) qui penche côté États-Unis, redevient panier (S20) et se referme puis se rouvre
dans la chute (S21) ; l'étiquette devient le bouton « S’abonner » (S22).

Parties (scènes contiguës, coupées là où la composition change) :
- p1 : S01-S09, images 0-1044. Accroche, annonce « 3 erreurs », contexte (ETF, Bourse, indice, 10 titres, frais,
  ficelle livre -> panier, le livre décide), erreur 1 allumée.
- p2 : S10-S15, images 1045-1948. Les noms et leurs livres, le MSCI World et les émergents dehors, le panier devient
  balance, « Monde » n'est pas équilibré (≈ 70 %), fil rouge vers les États-Unis.
- p3 : S16-S22, images 1949-2967. Les deux petits paniers (S&P 500, Nasdaq), la liste « 3 ETF » et la place vide, la
  balance redevient panier, « 3 questions » et la fiche « Composition », avant / après, carte de fin.
ENTRY_P2 et ENTRY_P3 sont le contrat des raccords (kit.pin à first_frame - 1). Les figurines n'y sont jamais.

Pas d'IA dans V07. « Toi » (figurine encre, side « left », échelle 1, pieds sur y 1230) est seul à tenir le stylo.
Entre deux gestes son bras est BAISSÉ (`lower` / `hold_low` / `walk_low`, repris de V06). Places : P1 (660, 1135)
S01-S11 et S20-S21 ; P2 (860, 1135) S12-S19 ; P_FIN (800, 1135) S22. Le bras gauche ne touche proprement qu'une cible
à sa gauche (|dx| >= 0,3 x dy) à 267 px au plus : `assert_reach(x_figurine, cible, quoi)` avant chaque geste.
Rouge : « ≈ 70 % » (`compteur`), le fil rouge (`lien_rouge`) et « ×3 » (`fois3`), et le mot « 70 % » du karaoké.
Gris : les seules pièces de la gestion active (S06). Pas de gris de mise en retrait.
Aucune entité nouvelle : panier = shapes (poly, round), balance = seesaw, titres = icon building sur disque.
"""
import importlib
import math
import os
from types import SimpleNamespace

from pipeline.story import GEOM, STYLE, text_width
from pipeline.story_kit import Figure, Kit, Sheet, ang_lerp, frames, lerp, solve_ik

PARTS = ["p1", "p2", "p3"]                      # S01-S09, S10-S15, S16-S22
NBSP, NNBSP = " ", " "                # espace insécable, fine insécable
ALERT_WORDS = {f"70{NBSP}%"}                    # karaoké en rouge : « 70 %. » (S14), la concentration cachée
ACOUSTIC_SNAP = {"gap": 0.2, "window": 0.08}    # temps fort après un silence : calé sur l'attaque audible
# CAPTION_GROUPS : aucune découpe imposée pour l'instant (à n'ajouter que si une découpe automatique est fausse).

# ---------- couleurs ----------
INK, CYAN, DEEP, LIGHT = STYLE["ink"], STYLE["cyan"], STYLE["deep"], STYLE["light"]
PAPER, RED, GREY, RULE, BG = STYLE["paper"], STYLE["red"], STYLE["grey"], STYLE["rule"], STYLE["bg"]

# ---------- textes à l'écran (typographie française) ----------
T_ETF_MONDE, T_ETF_SP, T_ETF_NQ = "ETF Monde", "ETF S&P 500", "ETF Nasdaq"
T_ABONNER = "S’abonner"
T_TOI, T_DIVERSIFIE, T_Q = "Toi", "diversifié", "?"
T_3_ERREURS, T_3_QUESTIONS = "3 erreurs", "3 questions"
MARKER_LABELS = ["Indice", "Poids", "Doublons"]
MARKER2_LABELS = ["Indice", "Pays", "Frais"]
T_BOURSE, T_INDICE, T_MSCI = "Bourse", "Indice", "MSCI World"
T_FRAIS, T_ETF, T_GESTION = "frais", "ETF", "gestion active"
T_MONDE, T_USA, T_TECH = "Monde", "États-Unis", "Tech"
T_REGLE1, T_REGLE2 = "pays développés", "pays émergents"
T_AUTRES = "autres pays"
T_3_ETF, T_FOIS3 = "3 ETF", "×3"
T_COMPOSITION = "Composition"
FICHE_LINES = [("Indice", T_MSCI, "bars"), (T_USA, f"≈{NBSP}70{NBSP}%", "percent"), ("Frais /an", "bas", "euro")]

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


P1 = fig_pos(660)                               # (660, 1135) : S01-S11, S20-S21 (couvercle à 248 px, étiquette 188)
P2 = fig_pos(860)                               # (860, 1135) : S12-S19, à droite de la balance
P_FIN = fig_pos(800)                            # (800, 1135) : S22, le bouton (690, 950) à sa gauche
TOI_NOM_C = (745, 1060)                         # étiquette « Toi » à droite de la tête (S01-S08)

# --- le repère 1-2-3 (en haut) et son titre ---
MARKER_Y, MARKER_CX, MARKER_GAP = 300, 540, 150  # disques x 390, 540, 690 ; légende y 362
MARKER_LABEL_SIZE = 32                          # 32 px (règle de lisibilité ; « Doublons » 149 px, écart 150)
TITRE_MARQUEUR_C = (540, 222)                   # « 3 erreurs », puis « 3 questions » (ExtraBold 40)
DISQUE_PT = [(MARKER_CX + (k - 1) * MARKER_GAP, MARKER_Y) for k in range(3)]   # monde : (390, 300) …

# --- le panier (repère local : centre du corps), son couvercle, ses titres ---
PANIER_C = (340, 1010)
BODY_PTS = [[-180, -77], [180, -77], [140, 100], [-140, 100]]                   # corps trapèze (x 160-520, y 933-1110)
REBORD_LOCAL, REBORD_W, REBORD_H = (0, -90), 380, 26                           # monde y 907-933 (x 150-530)
LATTES = [[[-90, -77], [-70, 100]], [[0, -77], [0, 100]], [[90, -77], [70, 100]]]
TRESSE = [[-158 + 20 * k, 4 if k % 2 == 0 else 16] for k in range(17)]          # tresse en zigzag, y ≈ 1020
ANSES = [[[-176, -66], [-204, -56], [-212, -24], [-192, 0], [-166, 2]],
         [[176, -66], [204, -56], [212, -24], [192, 0], [166, 2]]]
COUVERCLE_LOCAL, COUVERCLE_W, COUVERCLE_H = (0, -118), 400, 40                 # monde (340, 892), x 140-540
BOUTON_LOCAL = (0, -26)                         # enfant du couvercle : monde (340, 866)
COUVERCLE_TAP = (530, 892)                      # bout droit du couvercle (depuis P1 : 248 px ; levé de 14 : 261)
REBORD_TAP = (520, 915)                         # S21 « si. » : coche du rebord
TITRE_R = 26                                    # disques light r 26, immeuble encre
TITRES_LOCAL = ([[x, -138] for x in (-130, -65, 0, 65, 130)]                   # arrière y 872, x 210-470
                + [[x, -110] for x in (-97, -32, 33, 98, 163)])                # avant y 900, x 243-503
TITRE_TOMBE = 7                                 # S08 : titre8 (373, 900), 3e de l'avant, quitte le panier
PANIER_S11, PANIER_S11_K = (200, 1085), 0.7     # S11 : rangé en bas à gauche
PANIER_BAL_C = (400, 1010)                      # S12 : revient ici (x 1) puis se replie en balance ; S20 : en renaît

# --- l'étiquette « ETF Monde » (objet du fil) : pas enfant du panier (elle le quitte en S12) ---
ETIQ_C, ETIQ_W, ETIQ_H = (340, 1050), 240, 60
ETIQ_LOCAL_DY = ETIQ_C[1] - PANIER_C[1]         # 40 : son décalage sous le centre du panier (S07, S11 : la suivre)
ETIQ_TAP = (455, 1050)                          # bout droit (depuis P1 : 188 px)
ETIQ_S11 = (PANIER_S11[0], round(PANIER_S11[1] + ETIQ_LOCAL_DY * PANIER_S11_K, 2))  # (200, 1113), x 0,7
ETIQ_BAL = (600, 1180)                          # S12-S18 : pendue au flanc droit du pivot
FICELLE_BAL_PA = (432, 1126)                    # flanc droit du pivot (monde, le pivot ne tourne pas)
ETIQ_LISTE = [(690, 560), (690, 640), (690, 720)]                              # S19 : liste « 3 ETF »
LISTE_TITRE_C = (690, 480)

# --- la bulle de pensée (S01-S03) et la pièce de l'achat ---
BULLE_C, BULLE_W, BULLE_H = (700, 760), 320, 120
BULLE_RONDS = [((690, 995), 7), ((700, 945), 10), ((705, 885), 13)]
BULLE_TEXTE_LOCAL, BULLE_COCHE_LOCAL = (-40, 0), (100, 0)
QUESTION_NEE = (530, 820)                       # S02 : le « ? » sort du couvercle sous la pointe
QUESTION_BULLE, QUESTION_GS = (800, 760), 90    # dans la bulle : x 70/90 ; S03 : x 110/90
PIECE_R = 26

# --- la bulle de S13-S14 (autre place : au-dessus de « Toi » en P2) ---
BULLE2_C, BULLE2_W, BULLE2_H = (700, 620), 320, 170
BULLE2_RONDS = [((842, 1000), 7), ((818, 950), 10), ((786, 892), 13)]          # de la tête (860, 1071) vers la bulle
BULLE2_BALANCE_LOCAL = (-20, 30)                # mini balance (planche 200 x 12) : monde (680, 650)
BULLE2_COCHE_LOCAL = (120, -45)                 # monde (820, 575)

# --- le livre de l'indice (BOOK.png 300 px), ses mini-titres, ses règles ---
LIVRE_C, LIVRE_W = (190, 600), 300
LIVRE_TITRE_LOCAL = (0, -130)                   # « Indice » (Bold 36) au-dessus : monde (190, 470)
LIVRE_MSCI_LOCAL = (0, -145)                    # « MSCI World » (Bold 40) : monde (300, 455) en S11
LIVRE_BAS_LOCAL = (0, 95)                       # départ de la ficelle (monde 190, 695)
MINI_R = 10
MINI_LOCAL = ([[x, -36] for x in (24, 48, 72, 96, 120)]                         # page droite, deux rangées de 5
              + [[x, -8] for x in (26, 50, 74, 98, 122)])                        # (vérifié sur image fixe)
LIVRE_REGLES_LOCAL = [(-62, -34), (-62, -12), (-62, 10)]                        # page gauche : 3 lignes à puce
LIVRE_RANGE, LIVRE_RANGE_K = (150, 470), 0.55   # S06 : rangé en haut à gauche
SLIDE_DX = 60                                   # S07 : le livre (et le panier) glisse de 60 px
LIVRE_S10, LIVRE_S10_K = (190, 560), 0.6        # S10 : derrière « Monde », puis glisse vers y 690
LIVRES_S10_Y = 690
LIVRE_S11, LIVRE_S11_K = (300, 600), 1.0        # S11 : au centre haut
FICELLE_PANIER_LOCAL = (-175, -85)              # bord gauche du rebord (monde 165, 925)

# --- S04 : le petit graphique « Bourse » ---
BOURSE_C, BOURSE_MOT_C = (690, 600), (690, 480)
BOURSE_PTS = [[-130, 60], [-80, 20], [-55, 40], [-10, -5], [15, 15], [60, -35], [85, -15], [130, -60]]

# --- S05 : « 10 titres » ---
NB_TITRES_C = (600, 800)

# --- S06 : les frais ---
FRAIS_MOT_C = (610, 480)
FRAIS_ETF_C, FRAIS_ETF_LBL = (430, 570), (380, 570)
FRAIS_GA_C = [(430, 670), (490, 670), (550, 670), (610, 670)]
FRAIS_GA_LBL = (380, 670)
FRAIS_R = 24

# --- S10 : les noms d'ETF et leurs livres ---
NOMS = {"nom_monde": (T_MONDE, (190, 520)), "nom_usa": (T_USA, (450, 520)), "nom_tech": (T_TECH, (720, 520))}
NOM_LIVRE = {"nom_monde": "livre", "nom_usa": "livre_usa", "nom_tech": "livre_tech"}

# --- S11 : les deux règles du MSCI World (sous le livre, à portée du stylo depuis P1) ---
REGLE_X, REGLE_MARK_X = 462, 440                # texte (ancré à gauche) ; coche / croix devant
REGLE_Y = (935, 995)                            # L1 « pays développés », L2 « pays émergents » (au-dessus de la tête)
REGLE_TRACE_END_X = 570                         # la pointe parcourt 440 -> 570 (au-delà le bras passerait devant la tête)
FIL_LIVRE_REGLE = ((380, 640), (REGLE_MARK_X, 912))
FIL_REGLE_TITRES = ((REGLE_MARK_X - 4, 952), (300, 990))
EMERGENTS_SOL = [(330, 1225), (370, 1225), (410, 1225)]
EMERGENT_R = 20

# --- la balance (seesaw : origine au sommet du pivot) ---
BALANCE_C, PLANCHE_W, PLANCHE_H = (400, 1080), 720, 24     # planche x 40-760, y 1056-1080 ; pivot jusqu'à y 1170
SEATS_S12 = [-330, -260, -190, -120, -50, 50, 120, 190, 260, 330]
CYAN_SEATS = [0, 2, 4, 6, 8]                    # S12 : x locaux -330, -190, -50, 120, 260 virent au cyan
GEANTS = [0, 2, 4]                              # S14 : les 3 géants (r 32) ; 6, 8 : cyan r 18 ; les clairs r 17
S14_X = {0: -330, 2: -260, 4: -190, 6: -135, 8: -95, 1: 90, 3: 140, 5: 190, 7: 240, 9: 290}
S14_R = {i: (32 if i in GEANTS else 18 if i in CYAN_SEATS else 17) for i in range(10)}
TILTS = {"S14": -12, "S16": -15, "S17": -17}
PIL_USA_C, PIL_AUTRES_C, PIL_SIZE, PIL_H = (210, 880), (650, 880), 30, 52   # « autres pays » x 564-736
COMPTEUR_C = (210, 780)
COMPTEUR_HAUT, PIL_USA_HAUT, HAUT_K = (200, 440), (200, 520), 0.7             # S16-S19
LIEN_ROUGE_B = (0, 0)                           # ancré au centre du géant poids1 (suit la planche)


def seat(x, r):
    """Position locale (repère de la balance) d'un titre de rayon r posé à x sur la planche."""
    return [x, -PLANCHE_H - r]


# --- les deux petits paniers (enfants de la balance, x 0,6, sans couvercle) ---
PB_K = 0.6
PB_NEE = (700, 960)                             # S16 : pointe du stylo (« Toi » en P2 : 205 px)
PB_POSE = (290, -180)                           # local balance : sur le bout haut de la planche
PB1_SEAT, PB2_SEAT = (-160, -148), (-160, -303)  # local balance : posé SUR les géants, puis empilé (à -17° : monde
                                                 # (204, 985) et (158, 834), bords x 44-318 : pas plus à gauche)
PB_GEANTS_LOCAL = [[-110, -128], [0, -128], [110, -128]]   # r 30 local = r 18 monde
PB_PETITS_LOCAL = [[-55, -104], [55, -104]]                # r 18 local = r 11 monde
ETIQ_SP_C, ETIQ_NQ_C, ETIQ_SOEUR_W = (420, 905), (420, 820), 260         # x 290-550, à droite de la pile
FOIS3_C = (120, 660)                            # au-dessus de la pile (dont le haut est vers y 735)
PLACE_VIDE_X, PLACE_VIDE_R = 336, 20            # enfant de la balance, au bout droit de la planche (monde ≈ 716, 940 à -17°)

# --- la fiche « Composition » (Sheet n = 3, x 0,8 : x 170-570, y 395-805 ; rangées y 504, 587, 670) ---
FICHE_C, FICHE_K = (370, 600), 0.8

# --- S22 : fin (kit.outro, pos (540, 760), 620 x 520 : bouton (540, 908), x 350-730) ---
FIN_C = (540, 760)
FIN_BUTTON = (540, 908)
FIN_TAP = (690, 950)                            # bas droit du bouton, hors du libellé (« Toi » en P_FIN : 187 px)
BTN_W, BTN_H = 380, 112

# ---------- identifiants ----------
TITRES = [f"titre{k + 1}" for k in range(10)]   # dans le panier (enfants de `panier`) ; + `titre_neuf` (S08)
MINIS = [f"mini{k + 1}" for k in range(10)]     # sur la page du livre ; + `mini_neuf` (S08)
COPIES = [f"copie{k + 1}" for k in range(10)]   # S04 : copies qui volent de la page au panier
POIDS = [f"poids{k + 1}" for k in range(10)]    # sur la balance (enfants de `balance`), siège SEATS_S12[k]
FRAIS_GA = [f"frais_ga{k + 1}" for k in range(4)]
EMERGENTS = [f"emergent{k + 1}" for k in range(3)]
PANIER_PARTS = ["panier_rebord", "panier_latte1", "panier_latte2", "panier_latte3", "panier_tresse",
                "panier_anse1", "panier_anse2"]


def scene_f0(S, sid):
    return round(next(s for s in S.sb["scenes"] if s["id"] == sid)["t_start"] * S.fps)


# ---------- l'allonge de « Toi » (bras gauche) ----------
def arm_check(fig_x, pt, side="left", fig_y=P1[1]):
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


def assert_reach(fig_x, pt, what, side="left", fig_y=P1[1]):
    d, safe, clear = arm_check(fig_x, pt, side, fig_y)
    assert d <= REACH_OK and safe and clear >= HEAD_R + 8, \
        f"{what} : hors d'allonge depuis x {fig_x} ({side}) : {d} px, côté sûr {safe}, tête {clear} px"


# ---------- bras baissé (pose de repos de V06, valable des deux côtés) ----------
LOW_GRIP = (52, 40)          # prise du stylo, repère de la figurine (x du côté du bras) : à la hanche
LOW_ROT = 58                 # stylo vers le bas et vers l'extérieur (côté droit ; côté gauche : 180 - 58)


def low_pose(fig, n):
    G = fig._body_pt([fig.m * LOW_GRIP[0], LOW_GRIP[1]], n)
    rot = (LOW_ROT if fig.m > 0 else 180 - LOW_ROT) + fig.S.val(fig.id, "lean", n, 0)
    return G, rot


def lower(fig, f, d=8, e="inOut"):
    """Le bras redescend : stylo tenu bas, à la hanche, pointe vers le sol. -> f + d."""
    rel0, r0 = fig._start(f)
    for n, p in frames(f, d, e):
        A = fig._shoulder(n)
        G, rot = low_pose(fig, n)
        fig._pose(n, lerp([A[0] + rel0[0], A[1] + rel0[1]], G, p), ang_lerp(r0, rot, p))
    return f + d


def hold_low(fig, fa, fb):
    """Images [fa, fb) : bras baissé, posé image par image (le corps peut bouger)."""
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


# ---------- petites fabriques ----------
def pill(S, id, pos, text, size=34, weight=700, fill=LIGHT, h=58, z=11.5, parent=None, scale=0, pad=48, w=None,
         shadow=6, **p):
    if w is None:
        w = round(text_width(text, size, weight) + pad + (30 if p.get("icon") else 0))
    S.add(id, "pill", z=z, parent=parent, text=text, w=w, h=h, size=size, weight=weight, fill=fill, shadow=shadow, **p)
    S.set(id, pos=list(pos), scale=scale, opacity=1, fill=fill, w=w)
    return id


def ring(S, id, f, d=8, s0=0.8, s1=1.35):
    """Onde d'impact (cercle deep) : paraît à f, grandit et s'efface en d images. -> f + d."""
    S.key(id, "scale", f - 1, s0)
    S.key(id, "opacity", f - 1, 0)
    S.key(id, "opacity", f, 1)
    S.key(id, "scale", f, s1, d, "out")
    S.key(id, "opacity", f + 2, 0, d - 2, "linear")
    return f + d


def titre(kit, id, pos, r=TITRE_R, fill=LIGHT, z=5.5, parent=None, scale=0):
    """Un titre (une entreprise) : disque r, aplat light (piste fill en hex -> cyan), immeuble encre, ombre 3."""
    kit.icon(id, list(pos), "building", disc=r, fill=fill, shadow=3, z=z, parent=parent, scale=scale)
    kit.S.set(id, fill=fill, rot=0)
    return id


def basket(kit, id, pos, z, scale=1.0, parent=None, lid=True, prefix=None):
    """Un panier en formes plates (corps trapèze papier, rebord, 3 lattes, tresse, 2 anses ; couvercle si lid).
    Repère local : centre du corps. Les parties sont enfants de `id` ; renvoie leurs ids."""
    S = kit.S
    pre = prefix or id
    kit.shape(id, list(pos), kind="poly", pts=BODY_PTS, fill=PAPER, stroke=INK, sw=5, shadow=6, z=z, parent=parent,
              scale=scale)
    parts = []
    for k, pts in enumerate(LATTES):
        parts.append(kit.shape(f"{pre}_latte{k + 1}", [0, 0], kind="poly", pts=pts, closed=False, fill="none",
                               stroke=INK, sw=3, shadow=0, z=z + 0.05, parent=id))
    parts.append(kit.shape(f"{pre}_tresse", [0, 0], kind="poly", pts=TRESSE, closed=False, fill="none", stroke=INK,
                           sw=3, shadow=0, z=z + 0.06, parent=id))
    for k, pts in enumerate(ANSES):
        parts.append(kit.shape(f"{pre}_anse{k + 1}", [0, 0], kind="poly", pts=pts, closed=False, fill="none",
                               stroke=INK, sw=5, shadow=0, z=z - 0.05, parent=id))
    parts.append(kit.shape(f"{pre}_rebord", list(REBORD_LOCAL), kind="round", w=REBORD_W, h=REBORD_H, r=12,
                           fill=PAPER, stroke=INK, sw=5, shadow=3, z=z + 1, parent=id))
    S.set(f"{pre}_rebord", w=REBORD_W, h=REBORD_H, fill=PAPER)
    if lid:
        kit.shape(f"{pre}_couvercle", list(COUVERCLE_LOCAL), kind="round", w=COUVERCLE_W, h=COUVERCLE_H, r=14,
                  fill=PAPER, stroke=INK, sw=4, shadow=4, z=z + 1.5, parent=id)
        kit.shape(f"{pre}_bouton", list(BOUTON_LOCAL), kind="circle", w=24, fill=PAPER, stroke=INK, sw=4, shadow=0,
                  z=z + 1.6, parent=f"{pre}_couvercle")
    return parts


def bubble(kit, id, c, w, h, ronds, z=17):
    """Bulle de pensée en tirets (sans ombre) et ses 3 ronds (ids id_rond1..3), tous à l'échelle 0."""
    kit.shape(id, list(c), kind="round", w=w, h=h, r=30, fill=PAPER, stroke=INK, sw=4, dash=[14, 10], shadow=0, z=z,
              scale=0)
    kit.S.set(id, w=w, h=h)
    for k, (pt, r) in enumerate(ronds):
        kit.shape(f"{id}_rond{k + 1}", list(pt), kind="circle", w=2 * r, fill=PAPER, stroke=INK, sw=3, dash=[5, 4],
                  shadow=0, z=z, scale=0)
    return id


# ---------- raccords ----------
_OFF = lambda *ids: {i: {"scale": 0} for i in ids}   # noqa: E731

ENTRY_P2 = {   # fin de S09 = etat_initial de S10 (image 1044) : panier ouvert relié au livre, repère sur 1
    "panier": {"pos": list(PANIER_C), "scale": 1},
    **{t: {"pos": list(TITRES_LOCAL[k]), "scale": 1, "fill": LIGHT} for k, t in enumerate(TITRES)
       if k != TITRE_TOMBE},
    TITRES[TITRE_TOMBE]: {"scale": 0, "opacity": 0},
    "titre_neuf": {"pos": list(TITRES_LOCAL[TITRE_TOMBE]), "scale": 1, "fill": LIGHT},
    "etiquette": {"pos": list(ETIQ_C), "scale": 1, "rot": 0},
    "ficelle_etiq": {"draw": 1},
    "livre": {"pos": list(LIVRE_C), "scale": 1},
    "livre_titre": {"opacity": 1, "under": 1},
    **{m: {"scale": 1} for k, m in enumerate(MINIS) if k != TITRE_TOMBE},
    MINIS[TITRE_TOMBE]: {"scale": 0},
    "mini_neuf": {"scale": 1},
    "ficelle": {"draw": 1, "from": 0},
    "ficelle_halo": {"opacity": 0},
    "marqueur": {"pos": [MARKER_CX, MARKER_Y], "scale": 1, "on": 1, "active": 0, "done0": 0},
    "titre_erreurs": {"scale": 1},
    "toi_nom": {"opacity": 0},
    **_OFF("panier_couvercle", "piece", "bulle", "bulle_rond1", "bulle_rond2", "bulle_rond3", "question", "bourse",
           "bourse_mot", "nb_titres", "frais_mot", "frais_etf", "frais_etf_lbl", *FRAIS_GA, "frais_ga_lbl",
           *COPIES, "titre_neuf_vol"),
}
ENTRY_P3 = {   # fin de S15 = etat_initial de S16 (image 1948) : balance à -12°, fil rouge, « ≈ 70 % »
    "balance": {"pos": list(BALANCE_C), "scale": 1, "rot": TILTS["S14"]},
    **{p: {"pos": seat(S14_X[k], S14_R[k]), "scale": round(S14_R[k] / TITRE_R, 4),
           "fill": CYAN if k in CYAN_SEATS else LIGHT} for k, p in enumerate(POIDS)},
    "panier": {"pos": list(PANIER_BAL_C), "scale": 0},
    "etiquette": {"pos": list(ETIQ_BAL), "scale": 1, "rot": 0},
    "ficelle_etiq": {"draw": 0},
    "ficelle": {"from": 1},
    "livre": {"pos": list(DISQUE_PT[0]), "scale": 0},
    "ficelle_etiq_bal": {"draw": 1},
    "lien_rouge": {"draw": 1, "from": 0},
    "compteur": {"pos": list(COMPTEUR_C), "scale": 1, "value": 70},
    "pil_usa": {"pos": list(PIL_USA_C), "scale": 1},
    "pil_autres": {"pos": list(PIL_AUTRES_C), "scale": 1},
    "marqueur": {"pos": [MARKER_CX, MARKER_Y], "scale": 1, "on": 1, "active": 1, "done0": 1, "done1": 0},
    "titre_erreurs": {"scale": 1},
    **{w: {"opacity": 0} for w in ("fil_livre_regle", "fil_regle_titres", "fil_nom_monde", "fil_nom_usa",
                                   "fil_nom_tech")},
    **_OFF(*TITRES, "titre_neuf", "frais_etf", "livre_usa", "livre_tech", *NOMS, "regle1", "regle2",
           "regle1_coche", "regle2_croix", *EMERGENTS, "bulle2", "bulle2_rond1", "bulle2_rond2", "bulle2_rond3"),
}


def cast(S, kit):
    """Toute la distribution, à son état de l'image 0. Ce qui arrive plus tard : scale=0 (ou draw=0, chars=0,
    opacity=0). Seuls `fin` et `fin_curseur` naissent dans kit.outro (p3)."""

    # --- le panier de « Toi » (fermé : couvercle posé), ses 10 titres (cachés) et le titre neuf de S08 ---
    basket(kit, "panier", PANIER_C, z=5, lid=True)
    for k, t in enumerate(TITRES):
        titre(kit, t, TITRES_LOCAL[k], parent="panier", z=5.5)
    titre(kit, "titre_neuf", TITRES_LOCAL[TITRE_TOMBE], parent="panier", z=5.5)
    kit.tick("panier_coche", [REBORD_TAP[0] - PANIER_C[0], REBORD_TAP[1] - PANIER_C[1]], DEEP, size=48, sw=9, z=6.8,
             parent="panier")              # S21 « si. » : coche pleine sur le rebord (520, 915)

    # --- l'étiquette « ETF Monde » et sa ficelle (au rebord ; puis au pivot de la balance) ---
    S.add("etiquette", "pill", z=7, text=T_ETF_MONDE, w=ETIQ_W, h=ETIQ_H, size=34, weight=700, fill=CYAN, shadow=6)
    S.set("etiquette", pos=list(ETIQ_C), scale=1, opacity=1, rot=0, text=T_ETF_MONDE, fill=CYAN, w=ETIQ_W, textOp=1)
    S.add("ficelle_etiq", "wire", z=5.3, a={"id": "panier", "at": [0, -78]}, b={"id": "etiquette", "at": [0, -30]},
          color=DEEP, sw=4, dots=False)
    S.set("ficelle_etiq", draw=1, sag=0)
    S.set("ficelle_etiq", **{"from": 0})
    S.add("ficelle_etiq_bal", "wire", z=6.8, b={"id": "etiquette", "at": [0, -30]}, color=DEEP, sw=4, dots=False)
    S.set("ficelle_etiq_bal", pa=list(FICELLE_BAL_PA), draw=0, sag=0)
    S.set("ficelle_etiq_bal", **{"from": 0})

    # --- la pièce de l'achat (S01) ---
    kit.icon("piece", list(P1), "euro", disc=PIECE_R, fill=PAPER, shadow=3, z=12, scale=0)

    # --- la bulle de pensée S01-S03 : « diversifié » + coche, puis le « ? » ---
    bubble(kit, "bulle", BULLE_C, BULLE_W, BULLE_H, BULLE_RONDS)
    kit.text("bulle_texte", list(BULLE_TEXTE_LOCAL), T_DIVERSIFIE, size=36, weight=700, z=17.2, parent="bulle",
             typed=True)
    kit.tick("bulle_coche", list(BULLE_COCHE_LOCAL), DEEP, size=40, sw=8, z=17.3, parent="bulle")
    S.add("question", "qmark", z=17.5)
    S.set("question", pos=list(QUESTION_NEE), scale=0, opacity=1, gs=QUESTION_GS)

    # --- le repère 1-2-3 « 3 erreurs », puis « 3 questions » (aucun gris : doneStyle 'kept') ---
    for mid, labels in (("marqueur", MARKER_LABELS), ("marqueur2", MARKER2_LABELS)):
        kit.steps_marker(labels, id=mid, y=MARKER_Y, cx=MARKER_CX, gap=MARKER_GAP, z=20)
        S.ents[mid]["p"].update(moveBlank=True, labelSize=MARKER_LABEL_SIZE, doneStyle="kept")
        S.set(mid, scale=0, on=0, done0=0, done1=0, done2=0)
    kit.text("titre_erreurs", list(TITRE_MARQUEUR_C), T_3_ERREURS, size=40, weight=800, z=20, scale=0)
    kit.text("titre_questions", list(TITRE_MARQUEUR_C), T_3_QUESTIONS, size=40, weight=800, z=20, scale=0)

    # --- S04 : le graphique « Bourse » ---
    kit.curve("bourse", list(BOURSE_C), BOURSE_PTS, draw=0, z=10, color=DEEP, sw=6, smooth=False, dot=True,
              axes=True, scale=0)
    kit.text("bourse_mot", list(BOURSE_MOT_C), T_BOURSE, size=36, weight=700, z=10, typed=True)

    # --- le livre de l'indice (BOOK.png), son titre, sa liste de mini-titres, ses règles (S10) ---
    book = S.png("BOOK")
    book_h = round(LIVRE_W * book["h"] / book["w"])
    S.add("livre", "png", z=8, src=book["src"], w=LIVRE_W, h=book_h,
          contact=dict(w=round(LIVRE_W * 0.8), h=22, dy=4, blur=10, alpha=0.18))
    S.set("livre", pos=list(LIVRE_C), scale=0, opacity=1)
    kit.text("livre_titre", list(LIVRE_TITRE_LOCAL), T_INDICE, size=36, weight=700, z=8.3, parent="livre",
             opacity=0)
    S.set("livre_titre", under=0)
    kit.text("livre_msci", list(LIVRE_MSCI_LOCAL), T_MSCI, size=40, weight=700, z=8.3, parent="livre", typed=True)
    for k, m in enumerate(MINIS):
        titre(kit, m, MINI_LOCAL[k], r=MINI_R, z=8.2, parent="livre", scale=1)
        S.ents[m]["p"].update(shadow=0, s=14, sw=1.6)
    titre(kit, "mini_neuf", MINI_LOCAL[TITRE_TOMBE], r=MINI_R, z=8.2, parent="livre", scale=0)
    S.ents["mini_neuf"]["p"].update(shadow=0, s=14, sw=1.6)
    for lid in ("livre", "livre_usa", "livre_tech"):
        if lid != "livre":
            S.add(lid, "png", z=8, src=book["src"], w=LIVRE_W, h=book_h,
                  contact=dict(w=round(LIVRE_W * 0.8), h=22, dy=4, blur=10, alpha=0.18))
            S.set(lid, pos=[NOMS[{"livre_usa": "nom_usa", "livre_tech": "nom_tech"}[lid]][1][0], LIVRES_S10_Y],
                  scale=0, opacity=1)
        for k, (x, y) in enumerate(LIVRE_REGLES_LOCAL):
            kit.shape(f"{lid}_regle{k + 1}", [x + 10, y], kind="poly", pts=[[-26, 0], [30, 0]], closed=False,
                      fill="none", stroke=INK, sw=6, shadow=0, z=8.25, parent=lid, draw=0)
            kit.shape(f"{lid}_puce{k + 1}", [x - 24, y], kind="circle", w=10, fill=INK, stroke=INK, sw=0, shadow=0,
                      z=8.25, parent=lid, scale=0)

    # --- S04 : les copies de la liste qui volent vers le panier ; S08 : le titre neuf qui descend la ficelle ---
    for c in COPIES:
        titre(kit, c, LIVRE_C, r=MINI_R, z=9, scale=0)
    titre(kit, "titre_neuf_vol", LIVRE_C, r=MINI_R, z=9, scale=0)      # facultatif : relais vers titre_neuf

    # --- la ficelle livre -> panier (S07-S10) et son doublon épais (la ficelle « bat », S08) ---
    for wid, sw, op in (("ficelle_halo", 10, 0), ("ficelle", 5, 1)):
        S.add(wid, "wire", z=7.5 if wid == "ficelle" else 7.45, a={"id": "livre", "at": list(LIVRE_BAS_LOCAL)},
              b={"id": "panier", "at": list(FICELLE_PANIER_LOCAL)}, color=INK, sw=sw)
        S.set(wid, draw=0, sag=10, opacity=op)
        S.set(wid, **{"from": 0})

    # --- S05 : le compteur « 10 titres » ---
    kit.counter("nb_titres", list(NB_TITRES_C), value=1, size=44, weight=800, z=12, suffix=" titres", scale=0)

    # --- S06 : les pièces des frais (ETF cyan ; gestion active grises) et leurs légendes ---
    kit.text("frais_mot", list(FRAIS_MOT_C), T_FRAIS, size=36, weight=700, z=12, opacity=0)
    kit.icon("frais_etf", list(FRAIS_ETF_C), "euro", disc=FRAIS_R, fill=CYAN, shadow=3, z=12, scale=0)
    kit.text("frais_etf_lbl", list(FRAIS_ETF_LBL), T_ETF, size=32, weight=700, anchor="end", z=12, opacity=0)
    for k, cid in enumerate(FRAIS_GA):
        kit.icon(cid, list(FRAIS_GA_C[k]), "euro", disc=FRAIS_R, fill=GREY, shadow=3, z=12, scale=0)
    kit.text("frais_ga_lbl", list(FRAIS_GA_LBL), T_GESTION, size=32, weight=700, anchor="end", z=12, opacity=0)

    # --- S10 : les trois noms d'ETF (pilules light) et leurs courts fils vers leur livre ---
    for nid, (txt, pos) in NOMS.items():
        pill(S, nid, pos, txt, fill=LIGHT, z=9)
        S.add(f"fil_{nid}", "wire", z=8.9, a={"id": nid, "at": [0, 29]}, b={"id": NOM_LIVRE[nid], "at": [0, -70]},
              color=INK, sw=3)
        S.set(f"fil_{nid}", draw=0, sag=0)
        S.set(f"fil_{nid}", **{"from": 0})

    # --- S11 : les deux règles, la coche de « Toi », la croix, les fils, les titres émergents ---
    for k, (rid, txt) in enumerate((("regle1", T_REGLE1), ("regle2", T_REGLE2))):
        kit.text(rid, [REGLE_X, REGLE_Y[k]], txt, size=32, weight=700, anchor="start", z=10, typed=True)
    kit.tick("regle1_coche", [REGLE_MARK_X, REGLE_Y[0]], DEEP, size=34, sw=7, z=10.2)
    kit.shape("regle2_croix", [REGLE_MARK_X, REGLE_Y[1]], kind="poly",
              pts=[[-12, -12], [12, 12], [0, 0], [12, -12], [-12, 12]], closed=False, fill="none", stroke=INK, sw=5,
              shadow=0, z=10.2, draw=0)
    for wid, (a, b), col in (("fil_livre_regle", FIL_LIVRE_REGLE, INK), ("fil_regle_titres", FIL_REGLE_TITRES, DEEP)):
        S.add(wid, "wire", z=9.8, color=col, sw=4)
        S.set(wid, pa=list(a), pb=list(b), draw=0, sag=8)
        S.set(wid, **{"from": 0})
    for k, e in enumerate(EMERGENTS):
        kit.icon(e, [REGLE_X + 250, REGLE_Y[1]], "building", disc=EMERGENT_R, fill=PAPER, shadow=3, z=10.5, scale=0)
        S.set(e, rot=0)

    # --- la balance (seesaw, née du panier en S12) : ses 10 titres, ses légendes, « ≈ 70 % », le fil rouge ---
    kit.seesaw("balance", list(BALANCE_C), rot=0, w=PLANCHE_W, h=PLANCHE_H, fill=INK, base=PAPER, baseW=120, baseH=90,
               ground=160, sw=5, shadow=6, z=6, scale=0)
    for k, p in enumerate(POIDS):
        titre(kit, p, seat(SEATS_S12[k], TITRE_R), parent="balance", z=6.5, scale=0)
    pill(S, "pil_usa", PIL_USA_C, T_USA, size=PIL_SIZE, h=PIL_H, fill=CYAN, z=11)
    pill(S, "pil_autres", PIL_AUTRES_C, T_AUTRES, size=PIL_SIZE, h=PIL_H, fill=LIGHT, z=11)
    kit.counter("compteur", list(COMPTEUR_C), value=0, size=80, weight=800, z=12, prefix=f"≈{NBSP}", suffix=" %",
                scale=0)
    S.set("compteur", color=RED)
    S.ents["compteur"]["p"].update(color=RED)
    S.add("lien_rouge", "wire", z=6.9, a={"id": "etiquette", "at": [-ETIQ_W / 2, 0]},
          b={"id": POIDS[0], "at": list(LIEN_ROUGE_B)}, color=RED, sw=5)
    S.set("lien_rouge", draw=0, sag=0)
    S.set("lien_rouge", **{"from": 0})

    # --- la bulle de S13-S14 : une mini balance à plat (2 jetons cyan, 2 clairs) et la coche de « Toi » ---
    bubble(kit, "bulle2", BULLE2_C, BULLE2_W, BULLE2_H, BULLE2_RONDS)
    kit.seesaw("bulle2_balance", list(BULLE2_BALANCE_LOCAL), rot=0, w=200, h=12, fill=INK, base=PAPER, baseW=40,
               baseH=30, ground=0, sw=3, shadow=0, z=17.2, parent="bulle2")
    for k, (x, col) in enumerate(((-80, CYAN), (-50, LIGHT), (50, LIGHT), (80, CYAN))):   # en miroir
        kit.shape(f"bulle2_jeton{k + 1}", [x, -12 - 12], kind="circle", w=24, fill=col, stroke=INK, sw=3, shadow=0,
                  z=17.3, parent="bulle2_balance")
    kit.tick("bulle2_coche", list(BULLE2_COCHE_LOCAL), DEEP, size=40, sw=8, z=17.4, parent="bulle2")

    # --- S16-S19 : les deux petits paniers (enfants de la balance, ouverts, remplis de titres cyan) ---
    for pb in ("pb1", "pb2"):
        basket(kit, pb, PB_POSE, z=6.6, scale=0, parent="balance", lid=False)
        for k, pt in enumerate(PB_GEANTS_LOCAL):
            titre(kit, f"{pb}_geant{k + 1}", pt, r=30, fill=CYAN, z=6.62, parent=pb, scale=1)
        for k, pt in enumerate(PB_PETITS_LOCAL):
            titre(kit, f"{pb}_petit{k + 1}", pt, r=18, fill=CYAN, z=6.62, parent=pb, scale=1)
    for eid, txt, pos, pb in (("etiq_sp", T_ETF_SP, ETIQ_SP_C, "pb1"), ("etiq_nq", T_ETF_NQ, ETIQ_NQ_C, "pb2")):
        S.add(eid, "pill", z=7, text=txt, w=ETIQ_SOEUR_W, h=ETIQ_H, size=34, weight=700, fill=CYAN, shadow=6)
        S.set(eid, pos=list(pos), scale=0, opacity=1, rot=0, fill=CYAN, w=ETIQ_SOEUR_W)
        S.add(f"ficelle_{eid}", "wire", z=6.9, a={"id": pb, "at": [150, -90]},
              b={"id": eid, "at": [-ETIQ_SOEUR_W / 2, 0]}, color=DEEP, sw=4)
        S.set(f"ficelle_{eid}", draw=0, sag=6)
        S.set(f"ficelle_{eid}", **{"from": 0})
    kit.text("fois3", list(FOIS3_C), T_FOIS3, size=48, weight=800, color=RED, z=12, scale=0)
    kit.text("liste_titre", list(LISTE_TITRE_C), T_3_ETF, size=44, weight=800, z=12, scale=0)
    kit.shape("place_vide", seat(PLACE_VIDE_X, PLACE_VIDE_R), kind="circle", w=2 * PLACE_VIDE_R, fill="none",
              stroke=INK, sw=4, dash=[10, 8], shadow=0, z=7, parent="balance", scale=0)

    # --- S20 : la fiche « Composition » (3 rangées vides, écrites par kit.type), le géant qui saute ---
    sheet = Sheet(n=3, w=500)
    lignes = sheet.add(kit, "fiche", FICHE_LINES, pos=list(FICHE_C), title=T_COMPOSITION, scale=FICHE_K, z=8,
                       typed=True, show=False)
    for k, lid in enumerate(lignes):
        S.set(lid, bulletOn=0)                  # pas de puce tant que sa réponse n'est pas entrée (bulletOn -> 1)
        kit.shape(f"fiche_tirets{k + 1}", sheet.pt(k, "bullet"), kind="circle", w=44, fill="none", stroke=INK, sw=3,
                  dash=[8, 6], shadow=0, z=9.5, parent="fiche")   # puce vide en tirets, remplacée par la réponse
    titre(kit, "saut_geant", PANIER_C, r=32, fill=CYAN, z=12, scale=0)

    # --- S22 : ondes du toucher du stylo sur le bouton (pas de pointeur de souris) ---
    for k in range(2):
        kit.shape(f"fin_onde{k + 1}", list(FIN_TAP), kind="circle", w=70, fill="none", stroke=DEEP, sw=6, shadow=0,
                  z=43.5, opacity=0)

    # --- « Toi » (bras gauche), bras baissé dès l'image 0, et son nom ---
    toi = Figure(kit, "toi", pos=list(P1), scale=TOI_SCALE, side="left", z=15)
    S.set("toi", look=0)
    G, rot = low_pose(toi, 0)
    S.set(toi.pen, pos=[round(G[0], 3), round(G[1], 3)], rot=round(rot, 3))
    S.set(toi.arm, elbow=[round(v, 3) for v in solve_ik(toi._shoulder(0), G, toi.l1, toi.l2, toi.bend)[0]])
    kit.text("toi_nom", list(TOI_NOM_C), T_TOI, size=34, weight=700, z=15.2)

    return SimpleNamespace(toi=toi, sheet=sheet, lignes=lignes, titres=TITRES, minis=MINIS, copies=COPIES,
                           poids=POIDS, frais_ga=FRAIS_GA, emergents=EMERGENTS, panier_parts=PANIER_PARTS)


def build(S):
    kit = Kit(S)
    c = cast(S, kit)
    only = [p for p in os.environ.get("WTH_PARTS", "").split(",") if p]   # WTH_PARTS=p2 : cette partie seule
    for name in PARTS:
        if not only or name in only:
            importlib.import_module(f".{name}", __name__).part(S, kit, c)
