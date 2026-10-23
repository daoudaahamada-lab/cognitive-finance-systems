"""V03 « 1 % de frais par an : ce que ça coûte » : mise en scène Story, en paquet (une partie par fichier).

Storyboard : scripts/storyboards/V03.json (v1, révisé après le test sans son, 21 scènes, 99 temps forts, 97,52 s),
version lisible scripts/storyboards/V03.md. Voix : build/V03/words.json (film : images 0-2926).
Fil : une seule étiquette de prix. objet_fil = `etiquette` (pilule cyan « 1 % / an », pendue par la `ficelle` deep au
coin haut droit de la colonne de l'épargne) : elle surgit (S01), pèse et arrache un bloc (S02), arrache un jeton par
an (S04-S05), se range sous l'axe du graphique (S07), frappe le taux de 5 % qui tombe à 4 % net (S09), revient sur la
colonne et fait naître le « ? » du repère (S11), tranche l'encours sous « gestion » (S14), prend la tête de la liste
des frais (S16), passe au stylo de « Toi » (S19), bute contre le panneau « Rendement affiché » (S20) et devient, seule
sur l'ivoire, le bouton « S’abonner » de la carte de fin (S21).

Parties (scènes contiguës ; coupes aux changements de composition) :
- p1 : S01-S07, images 0-982. L'étiquette sur la colonne, les trois questions, les jetons arrachés chaque année
  (vague « marché » plate), « + » qui meurt sur le bac, la pile et ses gains fantômes « plus de 4 600 € »,
  l'écart pointillé sur la colonne, puis le réarrangement en graphique vide (pile d'abord, colonne ensuite).
- p2 : S08-S15, images 983-2087. Les deux courbes (5 % puis 4 % net), l'écart rouge de 4 600 €, le repli en colonne,
  le repère « Frais : Entrée, Gestion, Autres », l'entonnoir (1 000 € -> 970 € + jeton de 30 €), la gestion qui
  tranche l'encours (contour de tout le remplissage) et dont la pile monte en deux paliers à côté du jeton d'entrée.
- p3 : S16-S21, images 2088-2926. La liste des frais en deux colonnes, le document d'informations clés (papier plat),
  l'intermédiaire qui remet le relevé à « Toi » (« obligatoire » tamponné dessus, coche de « Toi »), la vague plate qui
  esquive le stylo de « Toi » et reçoit un cadenas, l'étiquette qu'il ramasse, tient et coche, le panneau barré à côté de la colonne, l'étiquette qui
  devient le bouton.
ENTRY_P2 et ENTRY_P3 (plus bas) sont le contrat des raccords : la partie précédente finit exactement dans cet état,
la suivante l'épingle à first_frame - 1 (kit.pin). Les figurines n'y sont jamais.

Pas d'IA dans V03 (aucun faisceau en pointillés, aucune coche de l'IA). « Toi » (figurine encre, échelle 1, pieds sur
y 1230) est seul à tenir le stylo : « ? » nés sous sa pointe (S07, S11, S17), carte « 1 000 € » sortie du stylo (S12),
toucher et coche du relevé (S18), toucher et ficelle (S11, S19), rature du 5 % (S20). L'intermédiaire est une
figurine papier sans outil (S18) : il tient le relevé et le remet.
Rouge : le coût des frais seulement, « 4 600 € », l'écart de la colonne et le crochet de l'écart (S06-S10).

Tour de revue 1 (corrections) : voir les docstrings des parties. Écarts d'exécution assumés par rapport au storyboard
(places, tailles, niveaux ; aucun sens changé, aucun temps fort déplacé) :
- niveaux de la colonne (LEVELS) : S02 0,50 (un bloc entier arraché, et non un demi), S04 0,42, S05 0,52 puis 0,62,
  S11 0,68, S13 0,74, S14 0,62 (tranches de 0,06) : la pile des frais reste sous le haut du remplissage ;
- la pile des frais est une jauge pleine à blocs de 30 px (segPx) dont la hauteur suit le contenu (60 px = les
  4 jetons ; 120 px avec les gains fantômes ; 160 px après la gestion ; 188 puis 215 px en S15) ;
- S11-S15 : l'étiquette revient à ETIQ_LOW (775, 870), à portée du stylo de « Toi » ;
- S16-S17 : liste en deux colonnes (corps 32) ; S17 : document papier plat (et non le livre PNG) ;
- S20 : panneau en (477, 960), colonne réduite à 0,8 à sa gauche, « Toi » en P_TOI_S20 (x 620) pour la rature.

Correction après le contrôle sans son (idée h manquée en S19, lue « les frais tombent quoi qu'il arrive ») :
- S19 en deux temps : « Toi » tend le stylo vers la vague, elle l'esquive (« pas »), retombe et le repousse, un cadenas
  se pose sur elle (« marchés. ») ; puis il pique l'étiquette posée au sol, la ramène dans sa main, basse, devant le
  buste (« contrôles »), la retourne et une pastille deep cochée s'y pose (« frais. »). Bras jamais levé au-dessus de
  la tête. La ficelle du stylo ne se tire qu'en S20 (« rendement »).
- S05 : plus de « + 0 € » (mal lu) ; S16 : le bac sort du cadre par la gauche (il semblait aspiré dans la colonne) ;
  S21 : « 1 % / an » s'efface (piste facultative `textOp` de la pilule) avant que l'étiquette ne devienne le bouton.
"""
import importlib
import math
import os
from types import SimpleNamespace

from pipeline.story import GEOM, STYLE, text_width
from pipeline.story_kit import Figure, Kit

PARTS = ["p1", "p2", "p3"]                      # S01-S07, S08-S15, S16-S21
NBSP, NNBSP = " ", " "                # espace insécable (avant % € : ?), fine insécable (milliers)
ALERT_WORDS = {f"4{NBSP}600{NBSP}€"}            # karaoké en rouge : le seul coût rouge du film (S06)
ACOUSTIC_SNAP = {"gap": 0.2, "window": 0.08}    # temps fort après un silence : calé sur l'attaque audible
CAPTION_GROUPS = [                              # découpes imposées : pas de groupe coupé dans une négation ou un nom
    ["Et l’argent prélevé", "ne travaille plus", "pour toi", "les années suivantes."],
    ["encore faut-il", "savoir quels frais", "tu paies."],
    ["prélevés", "sur chaque versement."],
    ["Ce sont eux", "qui pèsent", "le plus", "sur la durée."],
    ["Et un rendement", "affiché", "sans les frais", "n’est pas", "ton rendement."],
]

# ---------- couleurs (storyboard « style » = pipeline.story.STYLE) ----------
INK, CYAN, DEEP, LIGHT = STYLE["ink"], STYLE["cyan"], STYLE["deep"], STYLE["light"]
PAPER, RED, RULE = STYLE["paper"], STYLE["red"], STYLE["rule"]

# ---------- textes à l'écran (typographie française) ----------
T_ETIQ = f"1{NBSP}%{NBSP}/ an"
T_10K = f"10{NNBSP}000{NBSP}€"
T_4600 = f"4{NNBSP}600{NBSP}€"
T_26500 = f"≈{NBSP}26{NNBSP}500{NBSP}€"
T_21900 = f"≈{NBSP}21{NNBSP}900{NBSP}€"
T_5 = f"5{NBSP}%{NBSP}/ an"
T_4NET = f"4{NBSP}%{NBSP}net"
T_DIFF = f"5{NBSP}%{NBSP}−{NBSP}1{NBSP}%"
T_20ANS = f"20{NBSP}ans"
T_1AN = f"1{NBSP}an"
T_1000_CARTE = f"1{NBSP}000{NBSP}€"             # carte du versement : espace insécable pleine (la fine s'y perd)
T_970 = f"970{NBSP}€"
T_30 = f"30{NBSP}€"
T_3 = f"3{NBSP}%"
T_ENTREE3 = f"entrée 3{NBSP}%"
T_SUR10K = f"sur 10{NNBSP}000{NBSP}€"
T_FRAIS_DEUX_POINTS = f"Frais{NBSP}:"
QUESTIONS = [f"Combien{NBSP}?", f"D’où{NBSP}?", f"Comment{NBSP}?"]
LISTE = [("gestion", LIGHT), ("entrée", LIGHT), ("arbitrage", PAPER), ("sortie", PAPER), ("transaction", PAPER),
         ("change", PAPER), ("droits de garde", PAPER)]
RELEVE_LIGNES = [(f"en{NBSP}€{NBSP}:", f"100{NBSP}€{NBSP}/ an"), (f"en{NBSP}%{NBSP}:", f"1{NBSP}%{NBSP}/ an")]

# ---------- mise en page (1080 x 1920) ----------
# Action entre x 40-940 et y 160-1270 ; bande basse utilisée jusqu'à y ≈ 1250 ; sous-titres 1280-1380.
X_MIN, X_MAX, Y_MIN, Y_MAX = 40, 940, 160, 1270
CX = 540
GROUND = 1230                              # ligne de sol : pieds des figurines
FLOOR = 1210                               # sol de la colonne de l'épargne
FIG_BASE = GEOM["FIGURE"]["base"]          # 95 : du centre de la figurine à ses pieds (x échelle)
TOI_SCALE = 1.0
INTERM_SCALE = 0.9


def fig_pos(x, feet=GROUND, s=TOI_SCALE):
    """Centre d'une figurine d'échelle s dont les pieds sont sur la ligne y = feet."""
    return [x, round(feet - FIG_BASE * s, 2)]


P_TOI = fig_pos(840)                       # (840, 1135) : « Toi » au repos, en bas à droite, S01-S19
P_TOI_S20 = fig_pos(620)                   # S20 : sous la droite du panneau, la rature dans l'allonge
P_INTERM = fig_pos(400, s=INTERM_SCALE)    # S18 : l'intermédiaire entre jusqu'ici...
P_INTERM_PAS = fig_pos(440, s=INTERM_SCALE)   # ... puis fait un pas vers « Toi » en remettant le relevé
INTERM_FROM = -90                          # S18 : il entre en marchant depuis la gauche (hors cadre)

# --- la colonne de l'épargne (jauge verticale, 10 blocs) ---
EPARGNE_C, EPARGNE_W, EPARGNE_H = (520, 950), 220, 520      # x 410-630, y 690-1210
EPARGNE_EURO = (0, -300)                   # disque euro (r 34), repère de la colonne : monde (520, 650)
EPARGNE_MONTANT = (0, -385)                # « 10 000 € » ExtraBold 56 : monde (520, 565)
EPARGNE_MONTANT_S12 = (-240, -390)         # S12-S13 : « 10 000 € » s'écarte à gauche de l'entonnoir (monde 280, 560)
EPARGNE_CORNER = (EPARGNE_W / 2, -EPARGNE_H / 2)   # coin haut droit (630, 690) : départ de la ficelle
EPARGNE_PLUS = (676, 568)                  # S05 : « + » deep, à droite de « 10 000 € » (ExtraBold 56)
LEVELS = {"S01": 0.60, "S02": 0.50, "S04": 0.42, "S05a": 0.52, "S05": 0.62, "S11": 0.68, "S13": 0.74, "S14": 0.62}
NOFEE_V = 0.80                             # S06 : le niveau qu'aurait la colonne sans frais (trait pointillé)
TOKEN_DV, SLICE_DV = 0.02, 0.06            # un jeton arraché (S04) ; une tranche de gestion (S14)
EPARGNE_S16 = (300, 950)                   # S16 : la colonne glisse à gauche
EPARGNE_MINI, EPARGNE_MINI_K = (150, 1050), 0.7    # S17-S19 : réduite en bas à gauche (x 73-227, « 10 000 € » 39 px)
EPARGNE_S20, EPARGNE_S20_K = (130, 1030), 0.8      # S20 : à gauche du panneau (x 42-218, « 10 000 € » 45 px)


def level_y(v, c=EPARGNE_C, k=1.0):
    """y monde du haut du remplissage de la colonne au niveau v (colonne en c, échelle k)."""
    return c[1] + k * (EPARGNE_H / 2 - v * EPARGNE_H)


def level_local(v):
    """y local (repère de la colonne) du niveau v."""
    return EPARGNE_H / 2 - v * EPARGNE_H


# --- l'étiquette du fil et sa ficelle ---
ETIQ_W, ETIQ_H, ETIQ_SIZE = 220, 64, 34
ETIQ_HOME = (775, 720)                     # S01, S03-S07 : pendue au coin haut droit de la colonne
ETIQ_PESE = (775, 870)                     # S02 « facture » : elle pèse (puis + 40 px sur « lourde »)
ETIQ_LOW = (775, 870)                      # S11-S15 : à portée du stylo de « Toi »
ETIQ_MOT = (0, -56)                        # mot « frais » au-dessus d'elle (repère de l'étiquette), S01-S07
ETIQ_GRAPH = (480, 1150)                   # S07-S08 : rangée sous l'axe du graphique
ETIQ_TAUX = (560, 480)                     # S09 « 1 % » : à droite de la pilule « 5 % / an »
ETIQ_ON_TAUX = (320, 522)                  # S09 « tombes » : posée sur la pilule tombée (y 558-622)
GESTION_ABOVE = (775, 812)                 # S14 : « gestion » s'écrit au-dessus de l'étiquette en ETIQ_LOW
ETIQ_LISTE = (680, 440)                    # S16-S18 : tête de la liste des frais (x 570-790)
ETIQ_SOL = (470, 1195)                     # S19 « Tu » : posée au sol devant « Toi », hors de sa main (x 360-580)
ETIQ_SOL_PRISE = (555, 1177)               # S19 « contrôles » : la pointe la prend par son bout droit (261 px de l'épaule)
TIP_TIENT = (705, 1140)                    # S19 « frais. » : pointe du stylo tenue basse, devant le buste (bras au repos)
ETIQ_TENUE_DX = -95                        # S19 : l'étiquette tenue, centrée 95 px à gauche de la pointe (x 500-720)
ETIQ_OK = (-ETIQ_W / 2 - 8, 0)             # S19 : pastille deep cochée sur le bout gauche de l'étiquette (repère local)
ETIQ_BTN_SCALE = 112 / ETIQ_H              # S21 : 1,75 -> ≈ 385 x 112, la taille du bouton de la carte
TILT = -14                                 # S04, S14 : l'étiquette bascule contre la colonne

# --- le bac des frais, ses jetons, la pile ---
BAC_C, BAC_W, BAC_H = (200, 1170), 260, 100        # x 70-330, y 1120-1220 (trapèze papier, mot « frais »)
BAC_RIM = BAC_C[1] - BAC_H / 2                     # 1120 : bord du bac
JETON_R = 26
BAC_SLOTS = [(118, 1108), (166, 1108), (214, 1108), (262, 1108)]   # 4 jetons (S04), moitié basse dans le bac
BAC_PLUS = (200, 1040)                     # S05 : le « + » que le bac essaie de faire (il meurt sur les jetons)
PILE_X, PILE_W, PILE_SEG = 150, 80, 30     # pile cyan à blocs de 30 px posée sur le bord du bac (x 110-190)
PILE_H = {"base": 60, "S06": 120, "S14": 160, "S15a": 188, "S15": 215}   # hauteur de la pile (= son contenu)
FANTOMES = [(PILE_X, BAC_RIM - 60 - 15), (PILE_X, BAC_RIM - 60 - 45)]   # S06 : 2 gains fantômes (y 1045, 1015)
PILE_PLUSDE = (150, 898)                   # « plus de » Bold 34, au-dessus de la pile et de ses fantômes
PILE_MONTANT = (150, 952)                  # « 4 600 € » ExtraBold 56 rouge (x 42-258)
JETON_ENTREE = (290, 1094)                 # S13-S15 : le jeton de 30 €, posé sur le bord du bac à côté de la pile
JETON_ENTREE_TXT = (290, 1045)             # « 30 € » Bold 34 juste au-dessus
ETIQ_ENTREE = (300, 992)                   # S14-S15 : étiquette light « entrée 3 % » au-dessus (x 194-406)
TRANCHE_W, TRANCHE_H = EPARGNE_W - 4, round(SLICE_DV * EPARGNE_H)   # S14 : tranche cyan de toute la largeur (31 px)
ENCOURS_TXT = (672, 950)                   # « encours » Bold 34, ancre start, à droite du crochet


def pile_pos(h):
    """Centre de la pile de hauteur h, sa base toujours sur le bord du bac."""
    return [PILE_X, round(BAC_RIM - h / 2, 2)]


# --- la barre du temps (S04-S06), puis l'axe des 20 ans ---
BARRE_C, BARRE_W, BARRE_H, BARRE_N = (590, 300), 500, 40, 20     # x 340-840
BARRE_1AN = (BARRE_C[0] - BARRE_W / 2 + BARRE_W / BARRE_N / 2, 352)   # sous la case 1
BARRE_20ANS = (790, 352)                   # sous le bout droit
QUESTIONS_C = [(230, 440), (520, 440), (790, 440)]                # S03 : pilules papier, même y
QUESTIONS_VIA_Y = 470                      # S03 : la pilule monte d'abord (au-dessus de « 10 000 € ») puis glisse

# --- la vague du marché : courbe plate deep sur une aire bleu clair (plus de PNG) ---
VAGUE_PTS = [[x, round(-46 * math.sin(math.pi * (x + 150) / 100), 1)]
             for x in range(-150, 151, 15)]
VAGUE_BASE = 64                            # bas de l'aire (repère de la vague)
VAGUE_S04, VAGUE_S04_K = (180, 600), 0.9   # S04 : à gauche, sous la barre
VAGUE_S04_DY = 85                          # S04 : elle monte (« monte ») puis plonge (« baisse. ») de 85 px
VAGUE_MARCHE_S04 = (165, 815)              # « marché » sous la vague (hors du vol des jetons)
VAGUE_S19 = (420, 1000)                    # S19 : à gauche de « Toi », à hauteur d'épaule (x 270-570, y 954-1064)
VAGUE_S19_ESQUIVE = (430, 790)             # S19 « pas » : elle esquive le stylo (vers le haut, -10°)
TIP_VAGUE = (575, 1030)                    # S19 : pointe tendue à l'horizontale jusqu'au bord de la vague (251 px)
VAGUE_NOM_S19 = (-20, -112)                # « marché » au-dessus de la vague (repère local : il la suit)
VAGUE_FLECHE_S19 = (125, -112)             # disque deep à flèche, à droite de « marché » (repère local de la vague)
VAGUE_LOCK = (0, 4)                        # S19 « marchés. » : cadenas (disque encre 88 px) posé sur la vague (repère local)
VAGUE_PILL_SIZE = 40

# --- le graphique (S07-S10) ---
AXE_O = (160, 1060)                        # origine des axes
AXE_X1, AXE_TOP = 700, 420                 # bout de l'axe horizontal (60 px d'ivoire avant le stylo), haut de l'axe vertical
GRAPH_START = (160, 960)                   # point de départ cyan r 16 (la colonne réduite)
GRAPH_END_X = 680
GRAPH_Y_PER_EURO = 480 / 16533             # 26 533 € -> y 480
GRAPH_MONTANT = (178, 1012)                # « 10 000 € » Bold 34, ancre start, sous le point
AXE_20ANS = (650, 1100)                    # « 20 ans » sous le bout de l'axe, loin du bras de « Toi »
COURBE_A_TXT = (600, 430)                  # « ≈ 26 500 € » Bold 40
COURBE_B_TXT = (770, 668)                  # « ≈ 21 900 € » Bold 40, à droite sous le bout de B
CROCHET_X, CROCHET_Y = 715, (480, 614)     # S10 : crochet rouge de l'écart
CROCHET_TXT = (825, 547)                   # « 4 600 € » rouge logé à droite du crochet (échelle 44/56)
CROCHET_TXT_K = 44 / 56
RED_HIGH = (800, 360)                      # S07 : le chiffre rouge monte en haut à droite
QUESTION_ECART = (300, 950)                # S07 « écart ? » : le « ? » contre le chiffre rouge de la pile
QUESTION_HIGH = (905, 290)                 # S07 « Regarde » : il monte avec lui
TAUX_C, TAUX_LOW, TAUX_W, TAUX_H = (320, 480), (320, 590), 200, 64
TAUX_DIFF = (320, 665)                     # S09 « net. » : « 5 % − 1 % » Bold 34
MENTION1, MENTION2 = (420, 306), (420, 350)    # S07-S10 : « Exemple théorique, » / « rendement non garanti » (34)
MENTION_SIZE = 34


def courbe_pts(rate, years=20):
    """Points monde de la courbe 10 000 € x (1 + rate)^t, t = 0..20, sur le graphique (x 160 -> 680)."""
    dx = (GRAPH_END_X - GRAPH_START[0]) / years
    return [[round(GRAPH_START[0] + t * dx, 1),
             round(GRAPH_START[1] - (10000 * (1 + rate) ** t - 10000) * GRAPH_Y_PER_EURO, 1)] for t in range(years + 1)]


# --- repère 1-2-3 légendé (S11 -> S19) ---
MARKER_Y, MARKER_GAP, MARKER_LABEL, MARKER_DY = 300, 170, 34, 68
MARKER_XS = [CX - MARKER_GAP, CX, CX + MARKER_GAP]          # 370, 540, 710
MARKER_LABELS = ["Entrée", "Gestion", "Autres"]
FRAIS_LABEL = (322, 300)                   # « Frais : » Bold 34, ancre end (x 222-322)
QUESTION_MARKER = (CX, MARKER_Y)           # S11 « savoir » : le « ? » monte à la place du repère

# --- entrée (S12-S14) ---
ENTONNOIR_C = (520, 662)                   # trapèze 240 -> 80 px, 110 de haut : y 607-717, goulot dans la colonne
ENTONNOIR_PTS = [[-120, -55], [120, -55], [40, 55], [-40, 55]]
ENTONNOIR_GOULOT = (520, 717)
ENTONNOIR_TAUX = (345, 652)                # pilule light « 3 % » contre la lèvre gauche (x 290-400)
VERSEMENT_TIP = (748, 958)                 # S12 : la carte posée sur la pointe du stylo au repos
VERSEMENT_VIA = (700, 600)                 # S13 : elle monte d'abord à droite, puis passe au-dessus de l'entonnoir
VERSEMENT_HAUT = (520, 470)                # S13 « 1 000 € » : au-dessus de l'entonnoir
VERSEMENT_970 = (520, 782)                 # S13 « 970 € » : ressort sous le goulot, dans le haut de la colonne
VERSEMENT_W, VERSEMENT_H, VERSEMENT_SIZE = 230, 90, 48

# --- liste des frais (S16-S17) : deux colonnes, corps 32 ---
LISTE_SIZE, LISTE_H = 32, 52
LISTE_A_X, LISTE_B_X = 568, 800
LISTE_ROWS = [505, 570, 635, 700]
LISTE_FIL_A = ((580, 472), (580, 730))     # ficelle deep 4 px sous l'étiquette du fil, colonne A
LISTE_FIL_B = ((780, 472), (780, 665))     # colonne B
# place finale : gestion, entrée, arbitrage, sortie en A ; droits de garde, change, transaction en B (la plus
# récente arrive en haut de B et pousse les autres d'un cran)
LISTE_SLOTS = [(LISTE_A_X, LISTE_ROWS[0]), (LISTE_A_X, LISTE_ROWS[1]), (LISTE_A_X, LISTE_ROWS[2]),
               (LISTE_A_X, LISTE_ROWS[3]), (LISTE_B_X, LISTE_ROWS[0]), (LISTE_B_X, LISTE_ROWS[0]),
               (LISTE_B_X, LISTE_ROWS[0])]

# --- le document d'informations clés (S17-S18) : carte papier plate ---
DIC_C, DIC_W, DIC_H = (255, 565), 390, 300   # x 60-450, y 415-715
DIC_TITRE = [(0, -112), (0, -74)]          # « Document » / « d’informations clés » SemiBold 34
DIC_SIGLE = (0, -28)                       # « DIC » ExtraBold 44 deep, sous le titre
DIC_LIGNES = [(-95, 20), (-95, 50), (-95, 80), (-95, 110), (95, 20), (95, 50), (95, 80)]   # 7 traits 150 x 8
QUESTION_NEE = (560, 1000)                 # S17 « retrouver ? » : le « ? » sort du stylo, sous la liste
QUESTION_DIC = (255, 600)                  # S17 : il attend à la place du document...
QUESTION_COIN = (420, 440)                 # ... puis se pose sur son coin haut droit quand il tombe

# --- intermédiaire et relevé (S18) ---
INTERM_NOM = (400, 1022)                   # pilule « ton intermédiaire » (32) au-dessus de sa tête
INTERM_NOM_PAS = (440, 1022)
RELEVE_C, RELEVE_H = (640, 860), 250       # le relevé posé devant « Toi », à portée de stylo (x 481-799, y 735-985)
RELEVE_MAIN, RELEVE_MAIN_K = (470, 1110), 0.45   # S18 « doit » : dans la main de l'intermédiaire
RELEVE_FROM = (255, 650)                   # il sort du document
RELEVE_TITRE_DY, RELEVE_LIGNES_DY, RELEVE_SUR_DY = -75, [-22, 66], 22
RELEVE_OBLIG = (-62, -125)                 # « obligatoire » tamponné sur le coin haut gauche du relevé
RELEVE_COCHE = (132, 96)                   # la coche de « Toi », coin bas droit (à portée de stylo)
RELEVE_TAP = (700, 972)                    # S18 « euros » : « Toi » touche le bas du relevé

# --- panneau « Rendement affiché » (S20) ---
PANNEAU_C, PANNEAU_W, PANNEAU_H = (477, 960), 420, 270       # x 267-687, y 825-1095
PANNEAU_TITRE = (0, -95)                   # « Rendement affiché » SemiBold 32
PANNEAU_TAUX = (0, 15)                     # « 5 % / an » ExtraBold 48, centré
PANNEAU_NET = (0, 85)                      # « 4 % net » ExtraBold 48 deep, centré
PANNEAU_TON = (400, 1140)                  # pilule light « ton rendement » sous le panneau (x 258-542)
PANNEAU_SIZE = 48
ETIQ_S20 = (800, 780)                      # S20 « rendement » : l'étiquette suit « Toi », au-dessus du coin du panneau
ETIQ_BUTE = (640, 793)                     # S20 « sans » : elle bute sur le bord haut du panneau...
ETIQ_POSEE = (640, 765)                    # ... et se pose 28 px au-dessus

# --- fin (S21) ---
FIN_C = (540, 760)
FIN_BUTTON = (540, 908)                    # bouton de la carte de fin (kit.outro : 380 x 112)
FIN_TAP = (684, 944)                       # toucher : bas droit du bouton, hors du libellé


def scene_f0(S, sid):
    """Première image de la scène sid (round(t_start x 30))."""
    return round(next(s for s in S.sb["scenes"] if s["id"] == sid)["t_start"] * S.fps)


def pill(S, id, pos, text, size=34, weight=700, fill=LIGHT, h=56, z=12, parent=None, scale=0, pad=40, **p):
    """Pilule de texte mesurée (w = largeur du texte + pad), déclarée à sa place, échelle 0 par défaut."""
    S.add(id, "pill", z=z, parent=parent, text=text, w=round(text_width(text, size, weight) + pad), h=h, size=size,
          weight=weight, fill=fill, **p)
    S.set(id, pos=list(pos), scale=scale, opacity=1)
    return id


def ring(S, id, f, d=8, s0=0.8, s1=1.35):
    """Anneau qui s'élargit et s'efface (toucher, impact). -> f + d."""
    S.key(id, "scale", f - 1, s0)
    S.key(id, "opacity", f - 1, 0)
    S.key(id, "opacity", f, 1)
    S.key(id, "scale", f, s1, d, "out")
    S.key(id, "opacity", f + 2, 0, d - 2, "linear")
    return f + d


def drop_in(kit, id, f, **kw):
    """kit.drop d'entrée, l'objet caché jusqu'à l'image du mot (drop le montrerait déjà à f - 1, en haut)."""
    kit.S.key(id, "opacity", f - 1, 0)
    return kit.drop(id, f, **kw)


# ---------- raccords : état épinglé au début de p2 (image 982) et de p3 (image 2087) ----------
_OFF = lambda *ids: {i: {"scale": 0} for i in ids}   # noqa: E731

ENTRY_P2 = {   # fin de S07 = etat_initial de S08 : graphique vide, chiffre rouge et « ? » en haut à droite
    "axe_x": {"pos": [(AXE_O[0] + AXE_X1) / 2, AXE_O[1]], "scale": 1, "opacity": 1},
    "axe_y": {"pos": [AXE_O[0], (AXE_O[1] + AXE_TOP) / 2], "scale": 1, "opacity": 1, "draw": 1},
    "graph_point": {"pos": list(GRAPH_START), "scale": 1, "opacity": 1},
    "graph_montant": {"pos": list(GRAPH_MONTANT), "scale": 1, "opacity": 1},
    "axe_20ans": {"pos": list(AXE_20ANS), "scale": 1, "opacity": 1},
    "pile_montant": {"pos": list(RED_HIGH), "scale": 1, "opacity": 1},
    "question": {"pos": list(QUESTION_HIGH), "scale": 1, "opacity": 1},
    "mention1": {"opacity": 1}, "mention2": {"opacity": 1}, "mention_trait": {"draw": 1},
    "etiquette": {"pos": list(ETIQ_GRAPH), "scale": 1, "rot": 0, "opacity": 1, "text": T_ETIQ},
    "etiquette_mot": {"opacity": 0}, "ficelle": {"draw": 0},
    "courbe_a": {"draw": 0}, "courbe_b": {"draw": 0}, "crochet": {"draw": 0},
    "epargne_nofee": {"opacity": 0}, "epargne_ecart": {"opacity": 0}, "epargne_ecart_txt": {"opacity": 0},
    **_OFF("epargne", "bac", "pile", "fantome1", "fantome2", "pile_plusde", "barre_temps", "barre_1an", "barre_20ans",
           "vague", "vague_marche", "epargne_plus", "bac_plus", "jeton1", "jeton2", "jeton3", "jeton4",
           "pilule_taux", "courbe_a_txt", "courbe_b_txt", "marqueur", "question1", "question2", "question3"),
}
ENTRY_P3 = {   # fin de S15 = etat_initial de S16 : colonne au centre, pile « gestion » à côté du jeton, disque 2 actif
    "epargne": {"pos": list(EPARGNE_C), "scale": 1, "opacity": 1, "value": LEVELS["S14"]},
    "etiquette": {"pos": list(ETIQ_LOW), "scale": 1, "rot": 0, "opacity": 1, "text": T_ETIQ},
    "ficelle": {"draw": 1},
    "bac": {"pos": list(BAC_C), "scale": 1, "opacity": 1},
    "pile": {"pos": pile_pos(PILE_H["S15"]), "scale": 1, "opacity": 1, "h": PILE_H["S15"], "value": 1},
    "etiquette_gestion": {"pos": [PILE_X, BAC_RIM - PILE_H["S15"] - 30], "scale": 1, "opacity": 1},
    "jeton_entree": {"pos": list(JETON_ENTREE), "scale": 1, "opacity": 1},
    "jeton_entree_txt": {"pos": list(JETON_ENTREE_TXT), "scale": 1, "opacity": 1},
    "etiquette_entree": {"pos": list(ETIQ_ENTREE), "scale": 1, "opacity": 1},
    "pile_repere": {"draw": 1},
    "marqueur": {"pos": [CX, MARKER_Y], "scale": 1, "active": 1, "on": 1, "done0": 1, "lbl": 1},
    "frais_label": {"opacity": 1},
    "crochet_encours": {"opacity": 0}, "encours_txt": {"opacity": 0}, "encours_cadre": {"opacity": 0},
    **_OFF("entonnoir", "entonnoir_taux", "versement", "fantome1", "fantome2", "pile_montant", "pile_plusde",
           "question", "tranche1", "tranche2", "graph_point", "axe_x", "axe_y", "pilule_taux", "jeton1", "jeton2",
           "jeton3", "jeton4"),
}


def cast(S, kit):
    """Toute la distribution, à son état de l'image 0 : S01 montre la colonne de l'épargne (6 blocs pleins,
    disque euro, « 10 000 € ») et « Toi » au repos en bas à droite. Ce qui arrive plus tard est déclaré à sa première
    place avec scale=0 (l'intermédiaire : show=False)."""

    # --- la colonne de l'épargne (jauge verticale à 10 blocs), son disque euro, « 10 000 € » ---
    kit.gauge("epargne", EPARGNE_C, value=LEVELS["S01"], w=EPARGNE_W, h=EPARGNE_H, dir="up", segments=10,
              fill=CYAN, empty=PAPER, sw=4, shadow=6, z=6)
    S.set("epargne", fill=CYAN)
    kit.icon("epargne_euro", EPARGNE_EURO, "euro", disc=34, fill=CYAN, z=6.2, parent="epargne")
    kit.text("epargne_montant", EPARGNE_MONTANT, T_10K, size=56, weight=800, z=6.3, parent="epargne")
    kit.text("epargne_plus", EPARGNE_PLUS, "+", size=56, weight=800, color=DEEP, z=11, scale=0)
    # S02 : le bloc du haut arraché par l'étiquette (posé exactement sur le 6e bloc, puis tiré dans l'étiquette)
    kit.shape("epargne_bloc", [0, level_local(0.55)], kind="rect", w=EPARGNE_W - 4, h=EPARGNE_H / 10,
              fill=CYAN, stroke=INK, sw=3, shadow=0, z=6.05, scale=0, parent="epargne")
    S.set("epargne_bloc", fill=CYAN)
    # S06 : le niveau sans frais (trait pointillé deep) et l'écart rouge « 4 600 € » entre lui et le remplissage
    y_nf, y_f = level_local(NOFEE_V), level_local(LEVELS["S05"])
    kit.shape("epargne_nofee", [0, y_nf], kind="poly", pts=[[-EPARGNE_W / 2 + 6, 0], [EPARGNE_W / 2 - 6, 0]],
              closed=False, fill="none", stroke=DEEP, sw=7, dash=[16, 9], shadow=0, z=6.4, parent="epargne", draw=0)
    hh = (y_f - y_nf) / 2
    kit.shape("epargne_ecart", [EPARGNE_W / 2 + 25, (y_nf + y_f) / 2], kind="poly",
              pts=[[-14, -hh], [0, -hh], [0, hh], [-14, hh]], closed=False, fill="none", stroke=RED, sw=6, shadow=0,
              z=6.5, parent="epargne", draw=0)
    kit.text("epargne_ecart_txt", [EPARGNE_W / 2 + 40, (y_nf + y_f) / 2], T_4600, size=44, weight=800, color=RED,
             anchor="start", z=6.6, parent="epargne", opacity=0)
    # S14 : crochet « encours » le long du flanc droit (x 655, branches vers la colonne), du sol au niveau
    top, bot = level_y(LEVELS["S14"]), FLOOR
    half = (bot - top) / 2
    kit.shape("crochet_encours", [EPARGNE_C[0] + EPARGNE_W / 2 + 25, (top + bot) / 2], kind="poly",
              pts=[[-14, half], [0, half], [0, -half], [-14, -half]], closed=False, fill="none", stroke=DEEP, sw=6,
              shadow=0, z=6.5, draw=0)
    kit.text("encours_txt", ENCOURS_TXT, "encours", size=34, weight=700, anchor="start", z=6.5, opacity=0)
    # S14 « l’encours. » : contour deep de TOUT le remplissage, du sol à son sommet
    kit.shape("encours_cadre", [EPARGNE_C[0], (top + bot) / 2], kind="rect", w=EPARGNE_W + 10, h=bot - top + 10,
              fill="none", stroke=DEEP, sw=6, shadow=0, z=6.45, draw=0)
    for k in range(2):        # S14 : deux tranches cyan de toute la largeur, détachées du haut du remplissage
        kit.shape(f"tranche{k + 1}", [EPARGNE_C[0], level_y(LEVELS["S13"])], kind="rect", w=TRANCHE_W, h=TRANCHE_H,
                  fill=CYAN, stroke=INK, sw=3, shadow=0, z=7.4, scale=0)

    # --- l'étiquette du fil, son mot « frais », sa ficelle (colonne -> étiquette), « gestion » (S14-S15) ---
    S.add("etiquette", "pill", z=10, text=T_ETIQ, w=ETIQ_W, h=ETIQ_H, size=ETIQ_SIZE, weight=700, fill=CYAN)
    S.set("etiquette", pos=list(ETIQ_HOME), scale=0, opacity=1, rot=0, text=T_ETIQ)
    kit.text("etiquette_mot", ETIQ_MOT, "frais", size=34, weight=700, z=10.1, parent="etiquette", opacity=0)
    S.add("ficelle", "wire", z=9, color=DEEP, sw=6, tension=0,
          a={"id": "epargne", "at": list(EPARGNE_CORNER)}, b={"id": "etiquette", "at": [-ETIQ_W / 2, 0]})
    S.set("ficelle", sag=0, draw=0, opacity=1)
    S.set("ficelle", **{"from": 0})
    kit.text("etiquette_gestion", GESTION_ABOVE, "gestion", size=34, weight=700, z=10.2, typed=True)
    # S19 « frais. » : l'étiquette tenue par « Toi » est vérifiée : pastille deep cochée sur son bout gauche
    kit.icon("etiq_ok", ETIQ_OK, "check", disc=30, fill=DEEP, color=PAPER, z=10.3, parent="etiquette", scale=0)

    # --- les trois questions de l'annonce (S03-S04) ---
    for k, (txt, pos) in enumerate(zip(QUESTIONS, QUESTIONS_C)):
        pill(S, f"question{k + 1}", pos, txt, size=34, fill=PAPER, h=60, z=12, shadow=4)

    # --- la barre du temps (20 cases), « 1 an », « 20 ans » ---
    kit.gauge("barre_temps", BARRE_C, value=0, w=BARRE_W, h=BARRE_H, dir="right", segments=BARRE_N, fill=CYAN,
              empty=PAPER, sw=4, shadow=4, z=5, scale=0)
    kit.text("barre_1an", BARRE_1AN, T_1AN, size=34, weight=700, z=5.1, scale=0)
    kit.text("barre_20ans", BARRE_20ANS, T_20ANS, size=34, weight=700, z=5.1, scale=0)

    # --- le bac des frais, ses 4 jetons, son « + » qui meurt ---
    hw, hh = BAC_W / 2, BAC_H / 2
    kit.shape("bac", BAC_C, kind="poly", pts=[[-hw, -hh], [hw, -hh], [hw - 20, hh], [-hw + 20, hh]], fill=PAPER,
              stroke=INK, sw=5, shadow=6, z=7.5, scale=0)
    kit.text("bac_txt", [0, 8], "frais", size=34, weight=700, z=7.6, parent="bac")
    for k in range(4):        # arrachés au haut du remplissage, ils sortent par le haut et tombent dans le bac
        kit.icon(f"jeton{k + 1}", BAC_SLOTS[k], "euro", disc=JETON_R, fill=CYAN, shadow=3, z=7.3, scale=0)
    kit.text("bac_plus", BAC_PLUS, "+", size=56, weight=800, color=DEEP, z=11, scale=0)

    # --- la pile des frais (jauge pleine à blocs de 30 px, hauteur = contenu), 2 gains fantômes, « plus de 4 600 € » ---
    kit.gauge("pile", pile_pos(PILE_H["base"]), value=1, w=PILE_W, h=PILE_H["base"], dir="up", fill=CYAN,
              empty=PAPER, sw=4, shadow=6, z=7.0, scale=0, segPx=PILE_SEG)
    S.set("pile", fill=CYAN, h=PILE_H["base"])
    for k, pt in enumerate(FANTOMES):     # gains que les jetons prélevés n'ont pas faits : tirets cyan, sans fond
        kit.shape(f"fantome{k + 1}", pt, kind="round", w=PILE_W - 6, h=PILE_SEG - 5, r=8, fill="none", stroke=CYAN,
                  sw=6, dash=[10, 6], shadow=0, z=6.95, scale=0)
    kit.text("pile_plusde", PILE_PLUSDE, "plus de", size=34, weight=700, z=11, scale=0)
    kit.text("pile_montant", PILE_MONTANT, T_4600, size=56, weight=800, color=RED, z=11, scale=0)

    # --- la vague du marché (courbe plate deep, aire bleu clair), « marché », sa flèche ---
    kit.curve("vague", list(VAGUE_S04), VAGUE_PTS, draw=1, z=5, color=DEEP, sw=8, area=LIGHT, base=VAGUE_BASE,
              dot=False, scale=0)
    pill(S, "vague_marche", VAGUE_MARCHE_S04, "marché", size=VAGUE_PILL_SIZE, fill=PAPER, h=64, z=5.1, shadow=4)
    pill(S, "vague_nom", VAGUE_NOM_S19, "marché", size=VAGUE_PILL_SIZE, fill=PAPER, h=64, z=5.1, shadow=4,
         parent="vague")                   # S19 : l'étiquette « marché » enfant de la vague (elle esquive avec elle)
    kit.icon("vague_fleche", VAGUE_FLECHE_S19, "arrow", disc=32, fill=DEEP, color=PAPER, z=5.2, scale=0, rot=-90,
             parent="vague")
    # S19 « marchés. » : le marché est hors de portée de « Toi » : un cadenas se pose sur la vague (et la suit)
    kit.icon("vague_lock", VAGUE_LOCK, "lock", disc=44, fill=INK, color=PAPER, z=5.3, parent="vague", scale=0)

    # --- le graphique (S07-S10) : axes, point de départ, deux courbes, crochet rouge, libellés ---
    half_x = (AXE_X1 - AXE_O[0]) / 2
    kit.shape("axe_x", [AXE_O[0] + half_x, AXE_O[1]], kind="poly", pts=[[-half_x, 0], [half_x, 0]], closed=False,
              fill="none", stroke=INK, sw=5, shadow=0, z=3, scale=0)
    half_y = (AXE_O[1] - AXE_TOP) / 2
    kit.shape("axe_y", [AXE_O[0], AXE_O[1] - half_y], kind="poly", pts=[[0, half_y], [0, -half_y]], closed=False,
              fill="none", stroke=INK, sw=5, shadow=0, z=3, draw=0)
    kit.text("axe_20ans", AXE_20ANS, T_20ANS, size=34, weight=700, z=3.1, scale=0)
    kit.shape("graph_point", GRAPH_START, kind="circle", w=32, fill=CYAN, stroke=INK, sw=4, shadow=3, z=4, scale=0)
    kit.text("graph_montant", GRAPH_MONTANT, T_10K, size=34, weight=700, anchor="start", z=4.1, scale=0)
    kit.curve("courbe_a", [0, 0], courbe_pts(0.05), draw=0, z=3.5, color=DEEP, sw=7, area=LIGHT, base=AXE_O[1],
              dot=True)
    kit.curve("courbe_b", [0, 0], courbe_pts(0.04), draw=0, z=3.6, color=DEEP, sw=7, dot=True)
    kit.text("courbe_a_txt", COURBE_A_TXT, T_26500, size=40, weight=700, z=4.1, scale=0)
    kit.text("courbe_b_txt", COURBE_B_TXT, T_21900, size=40, weight=700, z=4.1, scale=0)
    ch = (CROCHET_Y[1] - CROCHET_Y[0]) / 2
    kit.shape("crochet", [CROCHET_X, (CROCHET_Y[0] + CROCHET_Y[1]) / 2], kind="poly",
              pts=[[-14, -ch], [0, -ch], [0, ch], [-14, ch]], closed=False, fill="none", stroke=RED, sw=6, shadow=0,
              z=3.8, draw=0)
    pill(S, "pilule_taux", TAUX_C, T_5, size=36, fill=LIGHT, h=TAUX_H, z=9.5)
    S.ents["pilule_taux"]["p"]["w"] = TAUX_W
    S.set("pilule_taux", text=T_5)
    kit.text("taux_diff", TAUX_DIFF, T_DIFF, size=34, weight=700, z=9.6, opacity=0)
    kit.text("mention1", MENTION1, "Exemple théorique,", size=MENTION_SIZE, weight=700, z=9, opacity=0)
    kit.text("mention2", MENTION2, "rendement non garanti", size=MENTION_SIZE, weight=700, z=9, opacity=0)
    w2, w3 = (text_width(t, MENTION_SIZE, 700) for t in ("rendement non garanti", "non garanti"))
    x_end = MENTION2[0] + w2 / 2
    kit.shape("mention_trait", [x_end - w3 / 2, MENTION2[1] + 26], kind="poly", pts=[[-w3 / 2, 0], [w3 / 2, 0]],
              closed=False, fill="none", stroke=DEEP, sw=5, shadow=0, z=9.1, draw=0)

    # --- le « ? » de « Toi » (S07, S11, S17 : un seul id, réutilisé) ---
    S.add("question", "qmark", z=17)
    S.set("question", pos=list(P_TOI), scale=0, opacity=1, gs=90)

    # --- repère 1-2-3 légendé (S11 -> S19), sans étape active jusqu'à « D’abord » (piste on), « Frais : » ---
    # doneStyle « kept » : aucune légende grise ; étape faite = disque bleu clair coché, légende encre Bold
    kit.steps_marker(MARKER_LABELS, id="marqueur", y=MARKER_Y, cx=CX, gap=MARKER_GAP, z=20)
    S.ents["marqueur"]["p"].update(labelSize=MARKER_LABEL, labelDy=MARKER_DY, moveBlank=True, doneStyle="kept")
    S.set("marqueur", scale=0, on=0, done0=0, done1=0, done2=0, lbl=1)
    kit.text("frais_label", FRAIS_LABEL, T_FRAIS_DEUX_POINTS, size=34, weight=700, anchor="end", z=20, opacity=0)

    # --- l'entonnoir d'entrée et sa pilule « 3 % », la carte du versement, le jeton de 30 €, « entrée 3 % » ---
    kit.shape("entonnoir", ENTONNOIR_C, kind="poly", pts=ENTONNOIR_PTS, fill=PAPER, stroke=INK, sw=5, shadow=6,
              z=8, scale=0)
    pill(S, "entonnoir_taux", ENTONNOIR_TAUX, T_3, size=34, fill=LIGHT, h=56, z=8.2)
    kit.shape("versement", VERSEMENT_TIP, kind="round", w=VERSEMENT_W, h=VERSEMENT_H, r=14, fill=PAPER,
              stroke=INK, sw=4, shadow=6, z=13, scale=0)
    kit.text("versement_txt", [0, 0], T_1000_CARTE, size=VERSEMENT_SIZE, weight=800, z=13.1, parent="versement")
    S.set("versement_txt", text=T_1000_CARTE)
    kit.icon("jeton_entree", ENTONNOIR_GOULOT, "euro", disc=JETON_R, fill=CYAN, shadow=3, z=7.3, scale=0)
    kit.text("jeton_entree_txt", JETON_ENTREE_TXT, T_30, size=34, weight=700, z=11, scale=0)
    pill(S, "etiquette_entree", ETIQ_ENTREE, T_ENTREE3, size=32, fill=LIGHT, h=48, z=8.3, shadow=4, pad=28)
    # S15 : repère deep à la hauteur du jeton, en travers de la pile : l'écart se lit
    kit.shape("pile_repere", [(PILE_X - 50 + JETON_ENTREE[0] + 36) / 2, JETON_ENTREE[1] - JETON_R], kind="poly",
              pts=[[-(JETON_ENTREE[0] + 36 - PILE_X + 50) / 2, 0], [(JETON_ENTREE[0] + 36 - PILE_X + 50) / 2, 0]],
              closed=False, fill="none", stroke=INK, sw=6, dash=[12, 7], shadow=0, z=7.35, draw=0)

    # --- la liste des frais (S16-S17) : deux ficelles + 7 étiquettes (light : connues ; papier : nouvelles) ---
    for wid, (a, b) in (("liste_fil", LISTE_FIL_A), ("liste_fil2", LISTE_FIL_B)):
        S.add(wid, "wire", z=9.4, color=DEEP, sw=4, tension=0)
        S.set(wid, pa=list(a), pb=list(b), sag=0, draw=0, opacity=1)
    for k, ((txt, fill), slot) in enumerate(zip(LISTE, LISTE_SLOTS)):
        pill(S, f"liste{k + 1}", slot, txt, size=LISTE_SIZE, fill=fill, h=LISTE_H, z=9.6, shadow=4)

    # --- le document d'informations clés : carte papier plate, titre en clair, « DIC », 7 traits encre ---
    kit.shape("dic", DIC_C, kind="round", w=DIC_W, h=DIC_H, r=16, fill=PAPER, stroke=INK, sw=5, shadow=6, z=5,
              scale=0)
    for k, (t, pt) in enumerate(zip(("Document", "d’informations clés"), DIC_TITRE)):
        kit.text(f"dic_titre{k + 1}", pt, t, size=34, weight=600, z=5.2, parent="dic", opacity=0)
    kit.text("dic_sigle", DIC_SIGLE, "DIC", size=44, weight=800, color=DEEP, z=5.3, parent="dic", scale=0)
    for k, pt in enumerate(DIC_LIGNES):
        kit.shape(f"dic_ligne{k + 1}", pt, kind="round", w=150, h=8, r=4, fill=INK, stroke=INK, sw=0, shadow=0,
                  z=5.2, parent="dic", scale=0)

    # --- l'intermédiaire (figurine papier, sans outil), « ton intermédiaire » au-dessus de sa tête ---
    interm = Figure(kit, "intermediaire", pos=list(P_INTERM), scale=INTERM_SCALE, variant="paper", tool=False,
                    z=14.5, show=False)
    S.set("intermediaire", look=0)
    pill(S, "interm_nom", INTERM_NOM, "ton intermédiaire", size=32, fill=PAPER, h=52, z=16.5, shadow=4)

    # --- le relevé « Coûts et frais » (S18) : titre souligné, « en € », « sur 10 000 € », « en % », tampon, coche ---
    lines_w = [text_width(f"{k} {v}", 34, 700) for k, v in RELEVE_LIGNES]
    titre_w = text_width("Coûts et frais", 34, 700)
    releve_w = round(max(lines_w + [titre_w]) + 56)
    kit.shape("releve", RELEVE_FROM, kind="round", w=releve_w, h=RELEVE_H, r=16, fill=PAPER, stroke=INK, sw=4,
              shadow=6, z=14, scale=0)
    kit.text("releve_titre", [0, RELEVE_TITRE_DY], "Coûts et frais", size=34, weight=700, z=14.1, parent="releve",
             underColor=DEEP)
    S.set("releve_titre", under=0)
    for k, ((key, val), dy, lw) in enumerate(zip(RELEVE_LIGNES, RELEVE_LIGNES_DY, lines_w)):
        x0 = -lw / 2
        kit.text(f"releve_cle{k + 1}", [x0, dy], key, size=34, weight=700, color=DEEP, anchor="start", z=14.1,
                 parent="releve", typed=True)
        kit.text(f"releve_val{k + 1}", [x0 + text_width(f"{key} ", 34, 700), dy], val, size=34, weight=700,
                 anchor="start", z=14.1, parent="releve", typed=True)
    kit.text("releve_sur", [lines_w[0] / 2, RELEVE_SUR_DY], T_SUR10K, size=32, weight=600, anchor="end", z=14.1,
             parent="releve", typed=True)
    pill(S, "interm_oblig", RELEVE_OBLIG, "obligatoire", size=32, fill=LIGHT, h=50, z=14.3, shadow=3, pad=36,
         parent="releve")
    S.set("interm_oblig", rot=-8)
    kit.tick("releve_coche", RELEVE_COCHE, DEEP, size=34, sw=7, z=14.4, parent="releve")

    # --- le panneau « Rendement affiché » (S20) : titre, « 5 % / an » barré, « 4 % net », « ton rendement » ---
    kit.shape("panneau", PANNEAU_C, kind="round", w=PANNEAU_W, h=PANNEAU_H, r=18, fill=PAPER, stroke=INK, sw=5,
              shadow=6, z=8.5, scale=0)
    kit.text("panneau_titre", PANNEAU_TITRE, "Rendement affiché", size=32, weight=600, z=8.6, parent="panneau")
    kit.text("panneau_taux", PANNEAU_TAUX, T_5, size=PANNEAU_SIZE, weight=800, z=8.6, parent="panneau", scale=0)
    tw = text_width(T_5, PANNEAU_SIZE, 800)
    kit.shape("panneau_barre", PANNEAU_TAUX, kind="poly", pts=[[tw / 2 + 8, 0], [-tw / 2 - 8, 0]], closed=False,
              fill="none", stroke=INK, sw=7, shadow=0, z=8.7, parent="panneau", draw=0)
    kit.text("panneau_net", PANNEAU_NET, T_4NET, size=PANNEAU_SIZE, weight=800, color=DEEP, z=8.6, parent="panneau",
             scale=0)
    pill(S, "panneau_ton", PANNEAU_TON, "ton rendement", size=34, fill=LIGHT, h=56, z=8.8, shadow=4)

    # --- S21 : toucher au doigt (point d'appui + deux ondes), pas de pointeur de souris ---
    kit.shape("fin_doigt", FIN_TAP, kind="circle", w=44, fill=INK, stroke=PAPER, sw=4, shadow=0, z=42, scale=0)
    for k in range(2):
        kit.shape(f"fin_onde{k + 1}", FIN_TAP, kind="circle", w=70, fill="none", stroke=DEEP, sw=6, shadow=0,
                  z=41.9, opacity=0)

    # --- « Toi » : au repos en bas à droite dès l'image 0, stylo baissé (bras côté gauche : il fait face à gauche) ---
    toi = Figure(kit, "toi", pos=list(P_TOI), scale=TOI_SCALE, z=15)
    S.set("toi", look=0)

    # S19 : la ficelle passe au stylo de « Toi » (de la pointe du stylo au bas de l'étiquette)
    S.add("ficelle_toi", "wire", z=15.9, color=DEEP, sw=6, tension=0,
          a={"id": "toi_stylo", "at": [GEOM["PEN"]["len"], 0]}, b={"id": "etiquette", "at": [0, ETIQ_H / 2]})
    S.set("ficelle_toi", sag=0, draw=0, opacity=1)
    S.set("ficelle_toi", **{"from": 0})

    return SimpleNamespace(toi=toi, interm=interm, releve_w=releve_w)


def build(S):
    kit = Kit(S)
    c = cast(S, kit)
    only = [p for p in os.environ.get("WTH_PARTS", "").split(",") if p]   # WTH_PARTS=p2 : cette partie seule
    for name in PARTS:
        if not only or name in only:
            importlib.import_module(f".{name}", __name__).part(S, kit, c)
