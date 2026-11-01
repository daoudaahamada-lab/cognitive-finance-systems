"""V07 « Ton ETF te rend vraiment diversifié ? » : mise en scène Story, en paquet (une partie par fichier).

Storyboard : scripts/storyboards/V07.json (v1, révisé après le test sans son, 22 scènes, 94 temps forts, 98,9 s),
version lisible scripts/storyboards/V07.md. Voix : build/V07/words.json (film : images 0-2967).
Fil : l'étiquette cyan « ETF Monde » (`etiquette`, pilule 240 x 60, x 1,3 en S01-S09) collée sur le panier de « Toi »
(`panier`, x 1,3 en S01-S09). Le panier fermé de l'accroche (S01) est ouvert par le contexte (S05), attaché au livre
de l'indice (`livre`, BOOK.png), devient la balance (`balance`, S12) qui penche côté États-Unis, redevient panier (S20)
et se referme puis se rouvre dans la chute (S21) ; l'étiquette devient le bouton « S’abonner » (S22).

Parties (scènes contiguës, coupées là où la composition change) :
- p1 : S01-S09, images 0-1044. Accroche, annonce « 3 erreurs », contexte (ETF, Bourse, indice, 10 titres, frais,
  ficelle livre -> panier, le livre décide), erreur 1 allumée.
- p2 : S10-S15, images 1045-1948. Les noms et leurs livres, le MSCI World et les émergents dehors, le panier devient
  balance, « Monde » n'est pas équilibré (≈ 70 %), fil rouge vers les États-Unis.
- p3 : S16-S22, images 1949-2967. Les deux petits paniers (S&P 500, Nasdaq), la liste « 3 ETF » et la place vide, la
  balance redevient panier, « 3 questions » et la fiche « Composition », avant / après, carte de fin.
ENTRY_P2 et ENTRY_P3 sont le contrat des raccords (kit.pin à first_frame - 1). Les figurines n'y sont jamais.

Tour de revue 1 (corrections) : composition agrandie et remontée (panier x 1,3 centré (340, 980), « Toi » x 1,15),
bras baissé plus haut (pointe <= y 1245), la pièce part du stylo en l'air, S07 glissement de 180 px, S08 titre retiré
rougi puis tombé au sol, S09 ligne de regard, S10 livres x 0,8 aux pages distinctes, S11 barrière et émergents au sol,
balance S12-S19 relevée et bascule -10 / -18 / -25°, « ≈ 70 % » et « États-Unis » rangés au repère en S17, S19
pictogrammes A, B, C et lien « ×3 », place vide r 38, S20 disques retournés un à un.

Pas d'IA dans V07. « Toi » (figurine encre, side « left », échelle 1,15, pieds sur y 1230) est seul à tenir le stylo.
Entre deux gestes son bras est BAISSÉ (`lower` / `hold_low` / `walk_low`, repris de V06). Places : P1 (760) S01-S11
et S20-S21 ; P2 (860) S12-S19 ; P_FIN (800) S22. Le bras gauche ne touche proprement qu'une cible à sa gauche
(|dx| >= 0,3 x dy) à 267 x 1,15 px au plus : `assert_reach(x_figurine, cible, quoi)` avant chaque geste.
Rouge : « ≈ 70 % » (`compteur`, S14-S16), le fil rouge (`lien_rouge`, S15), puis seulement « ×3 » et son lien
(S19) ; S08 : le titre retiré rougit. Gris : les seules pièces de la gestion active (S06). Pas de gris de retrait.
"""
import importlib
import math
import os
from types import SimpleNamespace

from pipeline.story import GEOM, STYLE, text_width
from pipeline.story_kit import Figure, Kit, Sheet, ang_lerp, frames, lerp, solve_ik

PARTS = ["p1", "p2", "p3"]                      # S01-S09, S10-S15, S16-S22
NBSP, NNBSP = " ", " "                # espace insécable, fine insécable
ALERT_WORDS = {f"70{NBSP}%"}                    # karaoké en rouge : « 70 %. » (S14), la concentration cachée
ACOUSTIC_SNAP = {"gap": 0.2, "window": 0.08}    # temps fort après un silence : calé sur l'attaque audible
CAPTION_GROUPS = [                              # découpes imposées : pas de nom propre ni de sujet coupé
    ["un ETF", "donc je suis", "diversifié"],
    ["Dans cette vidéo", "on va voir", "trois erreurs", "fréquentes", "avec les ETF"],
    ["Parce que c’est lui", "qui décide", "de ce que", "tu possèdes"],
    ["Ça ne suffit pas"],
    ["Un ETF Monde", "un ETF S&P 500", "et un ETF Nasdaq"],
    ["Le bon réflexe", "tient en", "trois questions"],
    ["Combien", "il te coûte", "par an"],
]

# ---------- couleurs ----------
INK, CYAN, DEEP, LIGHT = STYLE["ink"], STYLE["cyan"], STYLE["deep"], STYLE["light"]
PAPER, RED, GREY, RULE, BG = STYLE["paper"], STYLE["red"], STYLE["grey"], STYLE["rule"], STYLE["bg"]
OCRE = "#E6C88E"                                # S11 : titres des pays émergents (papier ocre : pas un titre du panier)

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
FICHE_LINES = [("Indice", T_MSCI, "bars"), (T_USA, f"≈{NBSP}70{NBSP}%", "none"), ("Frais par an", "bas", "euro")]

# ---------- mise en page (1080 x 1920) ----------
X_MIN, X_MAX, Y_MIN, Y_MAX = 40, 940, 160, 1270
GROUND = 1230                                   # ligne de sol : pieds de « Toi »
FIG_BASE = GEOM["FIGURE"]["base"]
TOI_SCALE = 1.15
HEAD_DY = GEOM["FIGURE"]["head"]["cy"] * TOI_SCALE          # -73,6 : centre de la tête
HEAD_R = GEOM["FIGURE"]["head"]["r"] * TOI_SCALE            # 36,8
SHOULDER_DX = abs(GEOM["FIGURE"]["shoulder"][0]) * TOI_SCALE  # 34,5
SHOULDER_DY = GEOM["FIGURE"]["shoulder"][1] * TOI_SCALE       # -18,4
REACH_OK = round(267 * TOI_SCALE)               # 307 : allonge confortable (REACH x allonge maximale)


def fig_pos(x, feet=GROUND, s=TOI_SCALE):
    return [x, round(feet - FIG_BASE * s, 2)]


P1 = fig_pos(760)                               # (760, 1120,75) : S01-S11, S20-S21
P_ASIDE = fig_pos(870)                          # S07-S08 : « Toi » s'écarte (le panier glisse vers lui)
P_S11 = fig_pos(800)                            # S11 : lecture des règles (marche sur « exemple, »)
P2 = fig_pos(860)                               # S12-S19 : à droite de la balance
P_FIN = fig_pos(800)                            # S22 : le bouton (690, 950) à sa gauche
HEAD_PT = (P1[0], P1[1] + HEAD_DY)              # (760, 1047)
TOI_NOM_C = (P1[0] + 85, 1050)                  # « Toi » à droite de la tête (S01-S06, S09)
TOI_NOM_ASIDE = (P_ASIDE[0], 985)               # S07-S08 : au-dessus de la tête (à droite il sortirait du cadre)

# --- le repère 1-2-3 (en haut) et son titre ---
MARKER_Y, MARKER_CX, MARKER_GAP = 300, 540, 150  # disques x 390, 540, 690 ; légende y 362
MARKER_LABEL_SIZE = 32
TITRE_MARQUEUR_C = (540, 222)                   # « 3 erreurs », puis « 3 questions » (ExtraBold 40)
DISQUE_PT = [(MARKER_CX + (k - 1) * MARKER_GAP, MARKER_Y) for k in range(3)]   # monde : (390, 300) …

# --- le panier (repère local : centre du corps, échelle PANIER_K en S01-S09), son couvercle, ses titres ---
PANIER_C, PANIER_K = (340, 980), 1.3            # corps x 106-574, y 880-1110 ; rebord y 863 ; couvercle y 827


def pw(local, c=PANIER_C, k=PANIER_K):
    """Point local du panier -> monde (panier en c, échelle k)."""
    return (round(c[0] + k * local[0], 2), round(c[1] + k * local[1], 2))


BODY_PTS = [[-180, -77], [180, -77], [140, 100], [-140, 100]]
REBORD_LOCAL, REBORD_W, REBORD_H = (0, -90), 380, 26
LATTES = [[[-90, -77], [-70, 100]], [[0, -77], [0, 100]], [[90, -77], [70, 100]]]
TRESSE = [[-158 + 20 * k, 4 if k % 2 == 0 else 16] for k in range(17)]
ANSES = [[[-176, -66], [-204, -56], [-212, -24], [-192, 0], [-166, 2]],
         [[176, -66], [204, -56], [212, -24], [192, 0], [166, 2]]]
COUVERCLE_LOCAL, COUVERCLE_W, COUVERCLE_H = (0, -118), 400, 40
BOUTON_LOCAL = (0, -26)
COUVERCLE_TAP = (585, 845)                      # bas du bout droit du couvercle (monde, panier x 1,3)
TITRE_R = 26                                    # disques light r 26 (x 1,3 : r 34 à l'écran)
TITRES_LOCAL = ([[x, -138] for x in (-130, -65, 0, 65, 130)]
                + [[x, -110] for x in (-97, -32, 33, 98, 163)])
TITRE_TOMBE = 7                                 # S08 : titre8, 3e de l'avant, quitte le panier
T8_SOL = (95, 1212)                             # S08 : il tombe au sol à gauche du panier et y reste
PANIER_S10, PANIER_S10_K = (300, 1080), 0.85    # S10-S11 : rangé en bas à gauche (titres r 22)
PANIER_BAL_C = (420, 990)                       # S12 : revient ici (x 1) puis se replie en balance

# --- l'étiquette « ETF Monde » (objet du fil) : pas enfant du panier (elle le quitte en S12) ---
ETIQ_W, ETIQ_H = 240, 60
ETIQ_K = PANIER_K                               # S01-S09 : à l'échelle du panier
ETIQ_LOCAL_DY = 40                              # son décalage (local) sous le centre du panier
ETIQ_C = pw((0, ETIQ_LOCAL_DY))                 # (340, 1032)
ETIQ_TAP = (480, 1032)                          # bout droit (x 1,3 : bord à 496)
ETIQ_S10 = pw((0, ETIQ_LOCAL_DY), PANIER_S10, PANIER_S10_K)   # (300, 1114)
BALANCE_C, PLANCHE_W, PLANCHE_H = (420, 1030), 720, 24     # planche x 60-780 ; pivot jusqu'à y 1120
ETIQ_BAL = (580, 1170)                          # S12-S18 : pendue au flanc droit du pivot
FICELLE_BAL_PA = (452, 1076)                    # flanc droit du pivot (monde, le pivot ne tourne pas)
ETIQ_LISTE = [(520, 520), (520, 600), (520, 680)]                              # S19 : liste « 3 ETF »
LISTE_TITRE_C = (520, 440)

# --- la bulle de pensée (S01-S03) et la pièce de l'achat ---
BULLE_C, BULLE_W, BULLE_H = (720, 640), 320, 120
BULLE_RONDS = [((778, 968), 10), ((766, 880), 15), ((750, 782), 20)]           # de la tête vers la bulle
BULLE_TEXTE_LOCAL, BULLE_COCHE_LOCAL = (-40, 0), (100, 0)
QUESTION_NEE = (585, 760)                       # S02 : le « ? » sort du couvercle sous la pointe
QUESTION_BULLE, QUESTION_GS = (820, 640), 90    # dans la bulle, à la place de la coche
PIECE_R = 28

# --- la bulle de S13-S14 (au-dessus de « Toi » en P2) ---
BULLE2_C, BULLE2_W, BULLE2_H = (700, 560), 320, 170
BULLE2_RONDS = [((848, 968), 10), ((832, 862), 14), ((812, 740), 18)]
BULLE2_BALANCE_LOCAL = (-20, 30)
BULLE2_COCHE_LOCAL = (120, -45)

# --- le livre de l'indice (BOOK.png 300 px), ses mini-titres, ses pages de S10 ---
LIVRE_C, LIVRE_W = (190, 600), 300
LIVRE_TITRE_LOCAL = (0, -130)
LIVRE_MSCI_LOCAL = (0, -145)
LIVRE_BAS_LOCAL = (0, 95)                       # départ de la ficelle (monde 190, 695)
MINI_R = 15
MINI_LOCAL = ([[x, -40] for x in (16, 46, 76, 106, 136)]                       # page droite, deux rangées de 5
              + [[x, -8] for x in (18, 48, 78, 108, 138)])
LIVRE_ETC_LOCAL = (78, 26)                      # « … » sous les deux rangées : la liste continue
LIVRE_RANGE, LIVRE_RANGE_K = (150, 470), 0.7    # S06 : rangé en haut à gauche
SLIDE_DX = 180                                  # S07 : le livre (et le panier) glisse de 180 px
LIVRE_S10, LIVRE_S10_K = (190, 560), 0.8        # S10 : derrière « Monde », puis glisse vers y 720
LIVRES_S10_Y = 720
LIVRE_S11, LIVRE_S11_K = (300, 600), 1.0        # S11 : au centre haut
FICELLE_PANIER_LOCAL = (-175, -85)
# S10 : pages distinctes de chaque livre (local livre) : pictogramme sur la page gauche, 3 règles sur la droite
PAGE_PICTO_LOCAL = (-72, -14)
PAGE_BARS = {"livre": [104, 72, 92], "livre_usa": [66, 110, 52], "livre_tech": [92, 54, 112]}
PAGE_BAR_Y = [-40, -14, 12]
PAGE_BAR_X0 = 26

# --- S04 : le petit graphique « Bourse » (né de l'étiquette) ---
BOURSE_C, BOURSE_MOT_C = (700, 560), (700, 440)
BOURSE_PTS = [[-130, 60], [-80, 20], [-55, 40], [-10, -5], [15, 15], [60, -35], [85, -15], [130, -60]]

# --- S05 : « 10 titres » ---
NB_TITRES_C = (700, 620)

# --- S06 : les frais (deux rangées à droite, au-dessus de « Toi ») ---
FRAIS_MOT_C = (640, 470)
FRAIS_LBL_X = 560                               # légendes ancrées à droite
FRAIS_ETF_C = (608, 570)
FRAIS_GA_C = [(608, 680), (668, 680), (728, 680), (788, 680)]
FRAIS_R = 26

# --- S10 : les noms d'ETF et leurs livres ---
NOMS = {"nom_monde": (T_MONDE, (190, 520)), "nom_usa": (T_USA, (450, 520)), "nom_tech": (T_TECH, (720, 520))}
NOM_LIVRE = {"nom_monde": "livre", "nom_usa": "livre_usa", "nom_tech": "livre_tech"}

# --- S11 : les deux règles du MSCI World (texte ancré à droite, marque après : le bras ne cache pas le texte) ---
REGLE_X_END, REGLE_MARK_X = 600, 628
REGLE_Y = (850, 915)
FIL_LIVRE_REGLE = ((300, 694), (350, 828))
FIL_REGLE_TITRES = ((338, 864), (300, 955))
BARRIERE_X, BARRIERE_Y = 490, (930, 1185)       # barrière encre devant le panier rangé
EMERG_X0, EMERG_IN_Y = 908, 966                                # trajectoire au-dessus de la tête de « Toi »
EMERGENTS_SOL = [(514, 1222), (566, 1222), (540, 1177)]   # petit tas au sol, entre la barrière et « Toi »
EMERGENT_R = 26

# --- la balance (seesaw : origine au sommet du pivot) ---
SEATS_S12 = [-330, -260, -190, -120, -50, 50, 120, 190, 260, 330]
CYAN_SEATS = [0, 2, 4, 6, 8]
GEANTS = [0, 2, 4]
S14_X = {0: -330, 2: -260, 4: -190, 6: -135, 8: -95, 1: 60, 3: 105, 5: 150, 7: 195, 9: 240}
S14_R = {i: (32 if i in GEANTS else 18 if i in CYAN_SEATS else 17) for i in range(10)}
TILTS = {"S14": -10, "S16": -18, "S17": -25}
PIL_SIZE, PIL_H = 34, 58
PIL_USA_C, PIL_AUTRES_C = (210, 820), (650, 820)
COMPTEUR_C = (210, 730)
PICTOS = ["phone", "cart", "target"]            # S19 : les 3 géants, A, B, C (mêmes dans les 3 contenants)


def seat(x, r):
    """Position locale (repère de la balance) d'un titre de rayon r posé à x sur la planche."""
    return [x, -PLANCHE_H - r]


# --- les deux petits paniers (enfants de la balance, x 0,6, sans couvercle) ---
PB_K = 0.6
PB_NEE = (720, 850)                             # S16 : pointe du stylo (« Toi » en P2)
PB_POSE = (295, -102)                           # local balance : posé sur les titres clairs du bout haut
PB1_SEAT, PB2_SEAT = (-150, -124), (-120, -255)  # posé SUR les géants, puis empilé
PB_GEANTS_LOCAL = [[-110, -128], [0, -128], [110, -128]]
PB_PETITS_LOCAL = [[-55, -104], [55, -104]]
ETIQ_SP_C, ETIQ_NQ_C, ETIQ_SOEUR_W = (440, 820), (440, 740), 260
PLACE_VIDE_X, PLACE_VIDE_R = 315, 38            # enfant de la balance, au bout clair, à côté des titres clairs
PIL_AUTRES_S16 = (800, 700)                     # S16 : « autres pays » cède le bout de la planche au petit panier

# --- la fiche « Composition » (Sheet n = 3, h 410, x 1 : x 250-750, y 420-830 ; rangées y 556, 660, 764) ---
FICHE_S20, FICHE_H = (480, 625), 410
CMP_X0 = 282                                    # S20 ligne 3 : pièce cyan, puis 4 mini-pièces grises barrées

# --- S22 : fin (kit.outro, pos (540, 760), 620 x 520 : bouton (540, 908), x 350-730) ---
FIN_C = (540, 760)
FIN_BUTTON = (540, 908)
FIN_TAP = (690, 950)
BTN_W, BTN_H = 380, 112

# ---------- identifiants ----------
TITRES = [f"titre{k + 1}" for k in range(10)]
MINIS = [f"mini{k + 1}" for k in range(10)]
COPIES = [f"copie{k + 1}" for k in range(10)]
POIDS = [f"poids{k + 1}" for k in range(10)]
FRAIS_GA = [f"frais_ga{k + 1}" for k in range(4)]
EMERGENTS = [f"emergent{k + 1}" for k in range(3)]
PANIER_PARTS = ["panier_rebord", "panier_latte1", "panier_latte2", "panier_latte3", "panier_tresse",
                "panier_anse1", "panier_anse2"]
LIVRES = ["livre", "livre_usa", "livre_tech"]


def page_ids(lid):
    """Ids de la page d'un livre en S10 : pictogramme (et ses traits), puis 3 règles et leurs puces."""
    return [f"{lid}_picto"], [f"{lid}_barre{k + 1}" for k in range(3)], [f"{lid}_puce{k + 1}" for k in range(3)]


def scene_f0(S, sid):
    return round(next(s for s in S.sb["scenes"] if s["id"] == sid)["t_start"] * S.fps)


# ---------- l'allonge de « Toi » (bras gauche, échelle TOI_SCALE) ----------
def arm_check(fig_x, pt, side="left", fig_y=P1[1]):
    """(distance épaule -> cible, côté sûr, dégagement de la tête) pour une figurine en (fig_x, fig_y)."""
    m = 1 if side == "right" else -1
    sx, sy = fig_x + m * SHOULDER_DX, fig_y + SHOULDER_DY
    dx, dy = pt[0] - sx, sy - pt[1]
    d = math.hypot(dx, dy)
    safe = dx * m >= 0.3 * max(dy, 0)
    hx, hy = fig_x, fig_y + HEAD_DY
    ux, uy = (pt[0] - sx) / max(d, 1e-6), (pt[1] - sy) / max(d, 1e-6)
    clear = min(math.hypot(sx + ux * t - hx, sy + uy * t - hy) for t in range(0, int(min(d, 140)) + 1))
    return round(d, 1), safe, round(clear, 1)


def assert_reach(fig_x, pt, what, side="left", fig_y=P1[1]):
    d, safe, clear = arm_check(fig_x, pt, side, fig_y)
    assert d <= REACH_OK and safe and clear >= HEAD_R + 6, \
        f"{what} : hors d'allonge depuis x {fig_x} ({side}) : {d} px, côté sûr {safe}, tête {clear} px"


# ---------- bras baissé (pose de repos de V06, relevée : pointe du stylo à y <= 1245) ----------
LOW_GRIP = (52, 20)          # prise du stylo, repère de la figurine (x du côté du bras) : à la hanche
LOW_ROT = 40                 # stylo vers le bas et vers l'extérieur (côté droit ; côté gauche : 180 - 40)


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


def lean_low(fig, f, deg, d=6):
    """Penche la figurine (piste lean) bras baissé (la pose basse suit le penché). -> f + d."""
    fig.kit.ensure(fig.id, "lean", 0)
    fig.S.key(fig.id, "lean", f, deg, d, "out")
    hold_low(fig, f, f + d)
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
    """Onde d'impact : paraît à f, grandit et s'efface en d images. -> f + d."""
    S.key(id, "scale", f - 1, s0)
    S.key(id, "opacity", f - 1, 0)
    S.key(id, "opacity", f, 1)
    S.key(id, "scale", f, s1, d, "out")
    S.key(id, "opacity", f + 2, 0, d - 2, "linear")
    return f + d


def titre(kit, id, pos, r=TITRE_R, fill=LIGHT, z=5.5, parent=None, scale=0, name="building"):
    """Un titre (une entreprise) : disque r, aplat light (piste fill en hex), pictogramme encre, ombre 3."""
    kit.icon(id, list(pos), name, disc=r, fill=fill, shadow=3, z=z, parent=parent, scale=scale)
    kit.S.set(id, fill=fill, rot=0)
    return id


def basket(kit, id, pos, z, scale=1.0, parent=None, lid=True, prefix=None, sw_k=1.0, braid=True):
    """Un panier en formes plates (corps trapèze papier, rebord, 3 lattes, tresse, 2 anses ; couvercle si lid).
    Repère local : centre du corps. `sw_k` : traits épaissis (petit panier : traits du grand à l'écran)."""
    S = kit.S
    pre = prefix or id
    kit.shape(id, list(pos), kind="poly", pts=BODY_PTS, fill=PAPER, stroke=INK, sw=round(5 * sw_k, 2), shadow=6,
              z=z, parent=parent, scale=scale)
    parts = []
    for k, pts in enumerate(LATTES):
        parts.append(kit.shape(f"{pre}_latte{k + 1}", [0, 0], kind="poly", pts=pts, closed=False, fill="none",
                               stroke=INK, sw=round(3 * sw_k, 2), shadow=0, z=z + 0.05, parent=id))
    if braid:
        parts.append(kit.shape(f"{pre}_tresse", [0, 0], kind="poly", pts=TRESSE, closed=False, fill="none",
                               stroke=INK, sw=3, shadow=0, z=z + 0.06, parent=id))
    for k, pts in enumerate(ANSES):
        parts.append(kit.shape(f"{pre}_anse{k + 1}", [0, 0], kind="poly", pts=pts, closed=False, fill="none",
                               stroke=INK, sw=round(5 * sw_k, 2), shadow=0, z=z - 0.05, parent=id))
    parts.append(kit.shape(f"{pre}_rebord", list(REBORD_LOCAL), kind="round", w=REBORD_W, h=REBORD_H, r=12,
                           fill=PAPER, stroke=INK, sw=round(5 * sw_k, 2), shadow=3, z=z + 1, parent=id))
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
        kit.shape(f"{id}_rond{k + 1}", list(pt), kind="circle", w=2 * r, fill=PAPER, stroke=INK, sw=3, dash=[6, 5],
                  shadow=0, z=z, scale=0)
    return id


def line(kit, id, pts, color=INK, sw=5, z=10, parent=None, dash=None, draw=0, pos=(0, 0), scale=1):
    """Trait ouvert (polyligne) à tracer (draw 0 -> 1)."""
    return kit.shape(id, list(pos), kind="poly", pts=[list(p) for p in pts], closed=False, fill="none", stroke=color,
                     sw=sw, shadow=0, z=z, parent=parent, dash=dash, draw=draw, scale=scale)


# ---------- raccords ----------
_OFF = lambda *ids: {i: {"scale": 0} for i in ids}   # noqa: E731

ENTRY_P2 = {   # fin de S09 = etat_initial de S10 (image 1044) : panier ouvert relié au livre, repère sur 1
    "panier": {"pos": list(PANIER_C), "scale": PANIER_K},
    **{t: {"pos": list(TITRES_LOCAL[k]), "scale": 1, "fill": LIGHT} for k, t in enumerate(TITRES)
       if k != TITRE_TOMBE},
    TITRES[TITRE_TOMBE]: {"scale": 0, "opacity": 0},
    "titre_neuf": {"pos": list(TITRES_LOCAL[TITRE_TOMBE]), "scale": 1, "fill": LIGHT},
    "etiquette": {"pos": list(ETIQ_C), "scale": ETIQ_K, "rot": 0},
    "ficelle_etiq": {"draw": 1},
    "livre": {"pos": list(LIVRE_C), "scale": 1},
    "livre_titre": {"opacity": 1, "under": 1},
    **{m: {"scale": 1} for k, m in enumerate(MINIS) if k != TITRE_TOMBE},
    MINIS[TITRE_TOMBE]: {"scale": 0},
    "mini_neuf": {"scale": 1},
    "livre_etc": {"scale": 1},
    "ficelle": {"draw": 1, "from": 0},
    "ficelle_halo": {"opacity": 0},
    "marqueur": {"pos": [MARKER_CX, MARKER_Y], "scale": 1, "on": 1, "active": 0, "done0": 0},
    "titre_erreurs": {"scale": 1},
    "toi_nom": {"opacity": 0},
    "regard": {"draw": 1},
    **_OFF("panier_couvercle", "piece", "bulle", "bulle_rond1", "bulle_rond2", "bulle_rond3", "question", "bourse",
           "bourse_mot", "nb_titres", "frais_mot", "frais_etf", "frais_etf_lbl", *FRAIS_GA, "frais_ga_lbl",
           *COPIES),
}
ENTRY_P3 = {   # fin de S15 = etat_initial de S16 (image 1948) : balance à -10°, fil rouge, « ≈ 70 % »
    "balance": {"pos": list(BALANCE_C), "scale": 1, "rot": TILTS["S14"]},
    **{p: {"pos": seat(S14_X[k], S14_R[k]), "scale": round(S14_R[k] / TITRE_R, 4),
           "fill": CYAN if k in CYAN_SEATS else LIGHT} for k, p in enumerate(POIDS)},
    "panier": {"pos": list(PANIER_BAL_C), "scale": 0},
    "etiquette": {"pos": list(ETIQ_BAL), "scale": 1, "rot": 0},
    "ficelle_etiq": {"draw": 0},
    "ficelle": {"from": 1},
    "livre": {"pos": list(DISQUE_PT[0]), "scale": 0},
    "ficelle_etiq_bal": {"draw": 0},
    "lien_rouge": {"draw": 1, "from": 0},
    "compteur": {"pos": list(COMPTEUR_C), "scale": 1, "value": 70},
    "pil_usa": {"pos": list(PIL_USA_C), "scale": 1},
    "pil_autres": {"pos": list(PIL_AUTRES_C), "scale": 1},
    "marqueur": {"pos": [MARKER_CX, MARKER_Y], "scale": 1, "on": 1, "active": 1, "done0": 1, "done1": 0},
    "titre_erreurs": {"scale": 1},
    **{w: {"opacity": 0} for w in ("fil_livre_regle", "fil_regle_titres", "fil_nom_monde", "fil_nom_usa",
                                   "fil_nom_tech", "fil_monde")},
    **_OFF(*TITRES, "titre_neuf", "frais_etf", "livre_usa", "livre_tech", *NOMS, "regle1", "regle2",
           "regle1_coche", "regle2_croix", *EMERGENTS, "barriere", "bulle2", "bulle2_rond1", "bulle2_rond2",
           "bulle2_rond3"),
}


def cast(S, kit):
    """Toute la distribution, à son état de l'image 0. Ce qui arrive plus tard : scale=0 (ou draw=0, chars=0,
    opacity=0). Seuls `fin` et `fin_curseur` naissent dans kit.outro, et le lien « ×3 » dans p3 (points mesurés)."""

    # --- le panier de « Toi » (fermé : couvercle posé, x 1,3), ses 10 titres (cachés) et le titre neuf de S08 ---
    basket(kit, "panier", PANIER_C, z=5, lid=True, scale=PANIER_K)
    for k, t in enumerate(TITRES):
        titre(kit, t, TITRES_LOCAL[k], parent="panier", z=5.5)
    titre(kit, "titre_neuf", TITRES_LOCAL[TITRE_TOMBE], parent="panier", z=5.5)
    kit.tick("panier_coche", [235, -130], DEEP, size=72, sw=10, z=6.8, parent="panier")   # S21 « si. »

    # --- l'étiquette « ETF Monde » et sa ficelle (au rebord ; puis au pivot de la balance) ---
    S.add("etiquette", "pill", z=7, text=T_ETF_MONDE, w=ETIQ_W, h=ETIQ_H, size=34, weight=700, fill=CYAN, shadow=6)
    S.set("etiquette", pos=list(ETIQ_C), scale=ETIQ_K, opacity=1, rot=0, text=T_ETF_MONDE, fill=CYAN, w=ETIQ_W,
          textOp=1)
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
        S.set(mid, scale=0, on=0, done0=0, done1=0, done2=0, lbl=0 if mid == "marqueur" else 1)
    kit.tick("disque1_coche", list(DISQUE_PT[0]), PAPER, size=30, sw=7, z=20.5)
    kit.text("titre_erreurs", list(TITRE_MARQUEUR_C), T_3_ERREURS, size=40, weight=800, z=20, scale=0)
    kit.text("titre_questions", list(TITRE_MARQUEUR_C), T_3_QUESTIONS, size=40, weight=800, z=20, scale=0)

    # --- S04 : le graphique « Bourse » ---
    kit.curve("bourse", list(BOURSE_C), BOURSE_PTS, draw=0, z=10, color=DEEP, sw=6, smooth=False, dot=True,
              axes=True, scale=0)
    kit.text("bourse_mot", list(BOURSE_MOT_C), T_BOURSE, size=40, weight=700, z=10, typed=True)

    # --- le livre de l'indice (BOOK.png), son titre, sa liste de mini-titres ---
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
        S.ents[m]["p"].update(shadow=0, s=20, sw=2)
    titre(kit, "mini_neuf", MINI_LOCAL[TITRE_TOMBE], r=MINI_R, z=8.2, parent="livre", scale=0)
    S.ents["mini_neuf"]["p"].update(shadow=0, s=20, sw=2)
    kit.text("livre_etc", list(LIVRE_ETC_LOCAL), "…", size=40, weight=800, z=8.2, parent="livre")
    S.ents["livre_etc"]["p"]["text"] = "…"
    for lid in LIVRES:
        if lid != "livre":
            S.add(lid, "png", z=8, src=book["src"], w=LIVRE_W, h=book_h,
                  contact=dict(w=round(LIVRE_W * 0.8), h=22, dy=4, blur=10, alpha=0.18))
            S.set(lid, pos=[NOMS[{"livre_usa": "nom_usa", "livre_tech": "nom_tech"}[lid]][1][0], LIVRES_S10_Y],
                  scale=0, opacity=1)
        # S10 : page gauche = pictogramme distinct (globe, drapeau, puce) ; page droite = 3 règles de longueurs
        # distinctes, chacune avec sa puce
        pic = f"{lid}_picto"
        kit.shape(pic, list(PAGE_PICTO_LOCAL), kind="circle", w=8, fill="none", stroke="none", sw=0, shadow=0,
                  z=8.25, parent=lid, scale=0)
        if lid == "livre":            # globe : disque, méridien, équateur
            kit.shape(f"{pic}_a", [0, 0], kind="circle", w=64, fill=LIGHT, stroke=INK, sw=5, shadow=0, z=8.26,
                      parent=pic)
            kit.shape(f"{pic}_b", [0, 0], kind="ellipse", w=28, h=64, fill="none", stroke=INK, sw=4, shadow=0,
                      z=8.27, parent=pic)
            line(kit, f"{pic}_c", [[-32, 0], [32, 0]], sw=4, z=8.27, parent=pic, draw=1)
        elif lid == "livre_usa":      # drapeau : rectangle rayé, canton
            kit.shape(f"{pic}_a", [0, 0], kind="rect", w=76, h=50, fill=PAPER, stroke=INK, sw=5, shadow=0, z=8.26,
                      parent=pic)
            for j, y in enumerate((-10, 4, 18)):
                line(kit, f"{pic}_s{j + 1}", [[-36, y], [36, y]], sw=5, z=8.27, parent=pic, draw=1)
            kit.shape(f"{pic}_c", [-20, -12], kind="rect", w=34, h=24, fill=DEEP, stroke=INK, sw=3, shadow=0,
                      z=8.28, parent=pic)
        else:                         # puce électronique : carré encre et ses pattes
            kit.shape(f"{pic}_a", [0, 0], kind="round", w=46, h=46, r=6, fill=INK, stroke=INK, sw=3, shadow=0,
                      z=8.27, parent=pic)
            for j, v in enumerate((-12, 0, 12)):
                line(kit, f"{pic}_l{j + 1}", [[-34, v], [-23, v]], sw=4, z=8.26, parent=pic, draw=1)
                line(kit, f"{pic}_r{j + 1}", [[23, v], [34, v]], sw=4, z=8.26, parent=pic, draw=1)
                line(kit, f"{pic}_t{j + 1}", [[v, -34], [v, -23]], sw=4, z=8.26, parent=pic, draw=1)
                line(kit, f"{pic}_b{j + 1}", [[v, 23], [v, 34]], sw=4, z=8.26, parent=pic, draw=1)
            kit.shape(f"{pic}_c", [0, 0], kind="circle", w=14, fill=CYAN, stroke="none", sw=0, shadow=0, z=8.28,
                      parent=pic)
        for k, (L, y) in enumerate(zip(PAGE_BARS[lid], PAGE_BAR_Y)):
            line(kit, f"{lid}_barre{k + 1}", [[PAGE_BAR_X0, y], [PAGE_BAR_X0 + L, y]], sw=9, z=8.25, parent=lid)
            kit.shape(f"{lid}_puce{k + 1}", [PAGE_BAR_X0 - 14, y], kind="circle", w=12, fill=INK, stroke=INK, sw=0,
                      shadow=0, z=8.25, parent=lid, scale=0)
    S.add("livre_onde", "shape", z=7.9, kind="ellipse", w=360, h=250, fill="none", stroke=CYAN, sw=7, shadow=0)
    S.set("livre_onde", pos=list(LIVRE_C), scale=0.8, opacity=0)          # S09 : le livre appelle

    # --- S04 : les copies de la liste qui volent vers le panier ---
    for c in COPIES:
        titre(kit, c, LIVRE_C, r=MINI_R, z=9, scale=0)

    # --- la ficelle livre -> panier (S07-S10) et son doublon épais (la ficelle « bat ») ---
    for wid, sw, op in (("ficelle_halo", 13, 0), ("ficelle", 6, 1)):
        S.add(wid, "wire", z=7.5 if wid == "ficelle" else 7.45, a={"id": "livre", "at": list(LIVRE_BAS_LOCAL)},
              b={"id": "panier", "at": list(FICELLE_PANIER_LOCAL)}, color=INK, sw=sw)
        S.set(wid, draw=0, sag=10, opacity=op)
        S.set(wid, **{"from": 0})

    # --- S09 : la ligne de regard de « Toi » (tirets, de l'œil à l'étiquette) ---
    S.add("regard", "wire", z=14.5, color=DEEP, sw=4, dash=[10, 9])
    S.set("regard", pa=[HEAD_PT[0] - 46, HEAD_PT[1] - 2], pb=[ETIQ_TAP[0] + 26, ETIQ_C[1] - 6], draw=0, sag=0)
    S.set("regard", **{"from": 0})

    # --- S05 : le compteur « 10 titres » ---
    kit.counter("nb_titres", list(NB_TITRES_C), value=2, size=64, weight=800, z=12, suffix=" titres", scale=0)

    # --- S06 : les pièces des frais (ETF cyan ; gestion active grises) et leurs légendes ---
    kit.text("frais_mot", list(FRAIS_MOT_C), T_FRAIS, size=44, weight=700, z=12, opacity=0)
    kit.icon("frais_etf", list(FRAIS_ETF_C), "euro", disc=FRAIS_R, fill=CYAN, shadow=3, z=12, scale=0)
    kit.text("frais_etf_lbl", [FRAIS_LBL_X, FRAIS_ETF_C[1]], T_ETF, size=44, weight=700, anchor="end", z=12,
             opacity=0)
    for k, cid in enumerate(FRAIS_GA):
        kit.icon(cid, list(FRAIS_GA_C[k]), "euro", disc=FRAIS_R, fill=GREY, shadow=3, z=12, scale=0)
    kit.text("frais_ga_lbl", [FRAIS_LBL_X, FRAIS_GA_C[0][1]], T_GESTION, size=44, weight=700, anchor="end", z=12,
             opacity=0)

    # --- S10 : les trois noms d'ETF (pilules light), leurs courts fils, et le fil « Monde » -> étiquette ---
    for nid, (txt, pos) in NOMS.items():
        pill(S, nid, pos, txt, fill=LIGHT, z=9)
        S.add(f"fil_{nid}", "wire", z=8.9, a={"id": nid, "at": [0, 29]}, b={"id": NOM_LIVRE[nid], "at": [0, -78]},
              color=INK, sw=3)
        S.set(f"fil_{nid}", draw=0, sag=0)
        S.set(f"fil_{nid}", **{"from": 0})
    S.add("fil_monde", "wire", z=8.95, a={"id": "etiquette", "at": [-60, -30]}, b={"id": "nom_monde", "at": [0, 29]},
          color=DEEP, sw=4, dots=False)
    S.set("fil_monde", draw=0, sag=0)
    S.set("fil_monde", **{"from": 0})

    # --- S11 : les deux règles, la coche, la croix, les fils, la barrière, les titres émergents ---
    for k, (rid, txt) in enumerate((("regle1", T_REGLE1), ("regle2", T_REGLE2))):
        kit.text(rid, [REGLE_X_END, REGLE_Y[k]], txt, size=32, weight=700, anchor="end", z=10, typed=True)
    kit.tick("regle1_coche", [REGLE_MARK_X + 4, REGLE_Y[0] - 10], DEEP, size=36, sw=8, z=10.2)
    kit.shape("regle2_croix", [REGLE_MARK_X + 4, REGLE_Y[1] - 10], kind="poly",
              pts=[[-14, -14], [14, 14], [0, 0], [14, -14], [-14, 14]], closed=False, fill="none", stroke=INK, sw=6,
              shadow=0, z=10.2, draw=0)
    for wid, (a, b), col in (("fil_livre_regle", FIL_LIVRE_REGLE, INK), ("fil_regle_titres", FIL_REGLE_TITRES, DEEP)):
        S.add(wid, "wire", z=9.8, color=col, sw=4)
        S.set(wid, pa=list(a), pb=list(b), draw=0, sag=8)
        S.set(wid, **{"from": 0})
    ym = (BARRIERE_Y[0] + BARRIERE_Y[1]) / 2       # origine au milieu : elle se réduit sur place
    line(kit, "barriere", [[0, BARRIERE_Y[0] - ym], [0, BARRIERE_Y[1] - ym]], sw=9, z=10.4, pos=(BARRIERE_X, ym))
    for k, e in enumerate(EMERGENTS):
        kit.icon(e, [EMERG_X0, EMERG_IN_Y], "building", disc=EMERGENT_R, fill=OCRE, shadow=3, z=10.5, scale=0)
        S.set(e, rot=0, fill=OCRE)

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
    usa_w = S.ents["pil_usa"]["p"]["w"]
    S.add("lien_rouge", "wire", z=11.2, a={"id": "pil_usa", "at": [usa_w / 2 - 6, 10]},
          b={"id": "etiquette", "at": [-ETIQ_W / 2 + 14, -26]}, color=RED, sw=6)
    S.set("lien_rouge", draw=0, sag=-60)
    S.set("lien_rouge", **{"from": 0})

    # --- la bulle de S13-S14 : une mini balance à plat (2 jetons cyan, 2 clairs) et la coche de « Toi » ---
    bubble(kit, "bulle2", BULLE2_C, BULLE2_W, BULLE2_H, BULLE2_RONDS)
    kit.seesaw("bulle2_balance", list(BULLE2_BALANCE_LOCAL), rot=0, w=200, h=12, fill=INK, base=PAPER, baseW=40,
               baseH=30, ground=0, sw=3, shadow=0, z=17.2, parent="bulle2")
    for k, (x, col) in enumerate(((-80, CYAN), (-50, LIGHT), (50, LIGHT), (80, CYAN))):
        kit.shape(f"bulle2_jeton{k + 1}", [x, -12 - 12], kind="circle", w=24, fill=col, stroke=INK, sw=3, shadow=0,
                  z=17.3, parent="bulle2_balance")
    kit.tick("bulle2_coche", list(BULLE2_COCHE_LOCAL), DEEP, size=40, sw=8, z=17.4, parent="bulle2")

    # --- S16-S19 : les deux petits paniers (enfants de la balance, traits du grand à l'écran, sans tresse) ---
    for pb in ("pb1", "pb2"):
        basket(kit, pb, PB_POSE, z=6.6, scale=0, parent="balance", lid=False, sw_k=round(1 / PB_K, 3), braid=False)
        for k, pt in enumerate(PB_GEANTS_LOCAL):
            titre(kit, f"{pb}_geant{k + 1}", pt, r=30, fill=CYAN, z=6.62, parent=pb, scale=1)
            titre(kit, f"{pb}_geant{k + 1}_p", [0, 0], r=30, fill=CYAN, z=6.63, parent=f"{pb}_geant{k + 1}",
                  scale=0, name=PICTOS[k])
        for k, pt in enumerate(PB_PETITS_LOCAL):
            titre(kit, f"{pb}_petit{k + 1}", pt, r=18, fill=CYAN, z=6.62, parent=pb, scale=1)
    for k, g in enumerate(GEANTS):                 # pictogrammes A, B, C des géants de la planche (S19)
        titre(kit, f"{POIDS[g]}_p", [0, 0], r=TITRE_R, fill=CYAN, z=6.55, parent=POIDS[g], scale=0, name=PICTOS[k])
    for eid, txt, pos, pb in (("etiq_sp", T_ETF_SP, ETIQ_SP_C, "pb1"), ("etiq_nq", T_ETF_NQ, ETIQ_NQ_C, "pb2")):
        S.add(eid, "pill", z=7, text=txt, w=ETIQ_SOEUR_W, h=ETIQ_H, size=34, weight=700, fill=CYAN, shadow=6)
        S.set(eid, pos=list(pos), scale=0, opacity=1, rot=0, fill=CYAN, w=ETIQ_SOEUR_W, textOp=0)   # vierge
        kit.text(f"{eid}_txt", [0, 0], txt, size=34, weight=700, z=7.1, parent=eid, typed=True)       # S18 : écrite
        S.add(f"ficelle_{eid}", "wire", z=6.9, a={"id": pb, "at": [0, -92]},
              b={"id": eid, "at": [-ETIQ_SOEUR_W / 2, 0]}, color=DEEP, sw=4)
        S.set(f"ficelle_{eid}", draw=0, sag=6)
        S.set(f"ficelle_{eid}", **{"from": 0})
    kit.text("fois3", [120, 700], T_FOIS3, size=56, weight=800, color=RED, z=12, scale=0)
    kit.text("liste_titre", list(LISTE_TITRE_C), T_3_ETF, size=44, weight=800, z=12, scale=0)
    kit.shape("place_vide", seat(PLACE_VIDE_X, PLACE_VIDE_R), kind="circle", w=2 * PLACE_VIDE_R, fill="none",
              stroke=DEEP, sw=6, dash=[14, 10], shadow=0, z=7, parent="balance", scale=0)
    autres_w = S.ents["pil_autres"]["p"]["w"]
    S.add("fil_vide", "wire", z=6.95, a={"id": "pil_autres", "at": [-autres_w / 2 + 30, 29]},
          b={"id": "place_vide", "at": [0, -PLACE_VIDE_R]}, color=DEEP, sw=4, dash=[8, 7])
    S.set("fil_vide", draw=0, sag=0)
    S.set("fil_vide", **{"from": 0})

    # --- S20 : les 3 disques retournés du repère (livre, balance penchée, pièce) et leurs « ? » ---
    for k in range(3):
        qd = f"qd{k + 1}"
        kit.shape(qd, list(DISQUE_PT[k]), kind="circle", w=70, fill=PAPER, stroke=INK, sw=4, shadow=3, z=20.6,
                  scale=1, opacity=0)
        S.set(qd, fill=PAPER, sx=1)
        kit.text(f"{qd}_q", [32, -28], T_Q, size=34, weight=800, z=20.9, parent=qd)
    S.add("qd1_livre", "png", z=20.7, parent="qd1", src=book["src"], w=46, h=round(46 * book["h"] / book["w"]))
    S.set("qd1_livre", pos=[0, 0], scale=1, opacity=1)
    kit.seesaw("qd2_bal", [0, 4], rot=-20, w=44, h=6, fill=INK, base=PAPER, baseW=14, baseH=12, ground=0, sw=2,
               shadow=0, z=20.7, parent="qd2")
    kit.icon("qd3_piece", [0, 0], "euro", disc=21, fill=CYAN, shadow=0, z=20.7, parent="qd3", scale=0)
    S.set("qd3_piece", fill=CYAN)

    # --- S20 : la fiche « Composition » (3 rangées vides, écrites par kit.type), le géant qui saute ---
    sheet = Sheet(n=3, w=500, h=FICHE_H)
    lignes = sheet.add(kit, "fiche", FICHE_LINES, pos=list(FICHE_S20), title=T_COMPOSITION, scale=1, z=8,
                       typed=True, show=False)
    for k, lid in enumerate(lignes):
        S.set(lid, bulletOn=0)
        kit.shape(f"fiche_tirets{k + 1}", sheet.pt(k, "bullet"), kind="circle", w=44, fill="none", stroke=INK, sw=3,
                  dash=[8, 6], shadow=0, z=9.5, parent="fiche")
    bx, by = sheet.pt(1, "bullet")
    kit.shape("fiche_bal_disc", [bx, by], kind="circle", w=48, fill=CYAN, stroke=INK, sw=3, shadow=0, z=9.6,
              parent="fiche", scale=0)          # ligne 2 : la puce est une mini balance penchée (les pays)
    kit.seesaw("fiche_bal", [0, 3], rot=-20, w=32, h=5, fill=INK, base=PAPER, baseW=10, baseH=9, ground=0, sw=2,
               shadow=0, z=9.7, parent="fiche_bal_disc")
    y3 = sheet.pt(2, "bullet")[1]
    kit.icon("cmp_cyan", [CMP_X0, y3], "euro", disc=20, fill=CYAN, shadow=3, z=9.6, parent="fiche", scale=0)
    for j in range(4):
        kit.icon(f"cmp_gris{j + 1}", [CMP_X0 + 44 + 30 * j, y3], "euro", disc=14, fill=GREY, shadow=0, z=9.6,
                 parent="fiche", scale=0)
    line(kit, "cmp_barre", [[CMP_X0 + 24, y3 + 18], [CMP_X0 + 148, y3 - 18]], sw=5, z=9.8, parent="fiche")
    titre(kit, "saut_geant", PANIER_C, r=32, fill=CYAN, z=12, scale=0)

    # --- S22 : ondes du toucher du stylo sur le bouton (pas de pointeur de souris) ---
    for k in range(2):
        kit.shape(f"fin_onde{k + 1}", list(FIN_TAP), kind="circle", w=70, fill="none", stroke=DEEP, sw=6, shadow=0,
                  z=43.5, opacity=0)

    # --- « Toi » (bras gauche, x 1,15), bras baissé dès l'image 0, et son nom ---
    toi = Figure(kit, "toi", pos=list(P1), scale=TOI_SCALE, side="left", z=15)
    S.set("toi", look=0)
    G, rot = low_pose(toi, 0)
    S.set(toi.pen, pos=[round(G[0], 3), round(G[1], 3)], rot=round(rot, 3))
    S.set(toi.arm, elbow=[round(v, 3) for v in solve_ik(toi._shoulder(0), G, toi.l1 * TOI_SCALE,
                                                       toi.l2 * TOI_SCALE, toi.bend)[0]])
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
