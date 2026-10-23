"""V03 « 1 % de frais par an : ce que ça coûte » : mise en scène Story, en paquet (une partie par fichier).

Storyboard : scripts/storyboards/V03.json (v1, révisé après le test sans son, 21 scènes, 99 temps forts, 97,52 s),
version lisible scripts/storyboards/V03.md. Voix : build/V03/words.json (film : images 0-2926).
Fil : une seule étiquette de prix. objet_fil = `etiquette` (pilule cyan « 1 % / an », pendue par la `ficelle` deep au
coin haut droit de la colonne de l'épargne) : elle surgit (S01), pèse (S02), arrache un jeton par an (S04-S05), se
range sous l'axe du graphique (S07), frappe le taux de 5 % qui tombe à 4 % net (S09), revient sur la colonne et fait
naître le « ? » du repère (S11), tranche l'encours sous « gestion » (S14), prend la tête de la liste des frais (S16),
passe au stylo de « Toi » (S19), bute contre le panneau « Rendement affiché » (S20) et devient le bouton « S’abonner »
de la carte de fin (S21).

Parties (scènes contiguës ; coupes aux changements de composition) :
- p1 : S01-S07, images 0-982. L'étiquette sur la colonne, les trois questions, les jetons arrachés chaque année
  (vague « marché »), « + » contre « + 0 € », la pile « plus de 4 600 € », puis le réarrangement en graphique vide.
- p2 : S08-S15, images 983-2087. Les deux courbes (5 % puis 4 % net), l'écart rouge de 4 600 €, le repli en colonne,
  le repère « Frais : Entrée, Gestion, Autres », l'entonnoir (1 000 € -> 970 € + jeton de 30 €), la gestion qui
  tranche l'encours et dont la pile écrase le jeton d'entrée.
- p3 : S16-S21, images 2088-2926. La liste des frais, le DIC, l'intermédiaire et son relevé, la vague contre la
  ficelle tenue par « Toi », le panneau barré, la carte de fin.
ENTRY_P2 et ENTRY_P3 (plus bas) sont le contrat des raccords : la partie précédente finit exactement dans cet état,
la suivante l'épingle à first_frame - 1 (kit.pin). Les figurines n'y sont jamais.

Pas d'IA dans V03 (aucun faisceau en pointillés, aucune coche de l'IA). « Toi » (figurine encre, échelle 1, pieds sur
y 1230) est seul à tenir le stylo : « ? » nés sous sa pointe (S07, S11, S17), carte « 1 000 € » sortie du stylo (S12),
toucher et ficelle (S11, S19), rature du 5 % (S20). L'intermédiaire est une figurine papier sans outil (S18).
Rouge : le coût des frais seulement, « 4 600 € » et le crochet de l'écart (S06-S10).

Écarts d'exécution assumés par rapport au storyboard (places et tailles seulement, aucun sens changé) :
- S11-S15 : l'étiquette revient à ETIQ_LOW (775, 870), sa place « lourde » de S02, et non à (775, 720) : à 720, elle
  est à 367 px au-dessus de l'épaule de « Toi », hors d'atteinte du stylo (allonge confortable 267 px) ;
  « gestion » s'écrit donc au-dessus d'elle en (775, 812) ;
- S09 : après le choc, l'étiquette se pose SUR la pilule tombée (ETIQ_ON_TAUX) au lieu de (560, 590), où elle
  couperait la courbe à 5 % ;
- S20 : panneau en (400, 995), « 5 % / an » et « 4 % net » à droite du panneau (ExtraBold 48), « Toi » en
  P_TOI_S20 (x 653) : c'est la seule place d'où la rature tient dans l'allonge (place_for vérifié) ; l'étiquette bute
  contre le bord droit du panneau en ETIQ_BUTE ; « ton rendement » sous le panneau ;
- « + » de la colonne à droite de « 10 000 € » (EPARGNE_PLUS) : à (520, 600), il couvrirait le disque euro ;
- graphique : « 10 000 € » sous le point de départ, « ≈ 21 900 € » à droite du bout de la courbe B (sous la
  courbe, il la couperait), chiffre rouge et « ? » en haut à droite à RED_HIGH / QUESTION_HIGH ;
- légendes du repère à 34 px (au lieu de 26) et écart de 170 px ; « Frais : » à gauche du disque 1.
"""
import importlib
import os
from types import SimpleNamespace

from pipeline.story import GEOM, STYLE, text_width
from pipeline.story_kit import Figure, Kit

PARTS = ["p1", "p2", "p3"]                      # S01-S07, S08-S15, S16-S21
NBSP, NNBSP = " ", " "                # espace insécable (avant % € : ?), fine insécable (milliers)
ALERT_WORDS = {f"4{NBSP}600{NBSP}€"}            # karaoké en rouge : le seul coût rouge du film (S06)
ACOUSTIC_SNAP = {"gap": 0.2, "window": 0.08}    # temps fort après un silence : calé sur l'attaque audible

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
T_ZERO = f"+{NBSP}0{NBSP}€"
T_1000 = f"1{NNBSP}000{NBSP}€"
T_970 = f"970{NBSP}€"
T_30 = f"30{NBSP}€"
T_3 = f"3{NBSP}%"
T_ENTREE3 = f"entrée 3{NBSP}%"
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
P_TOI_S20 = fig_pos(653)                   # S20 : à droite du panneau (buste x ≥ 612), rature dans l'allonge
P_INTERM = fig_pos(400, s=INTERM_SCALE)    # S18 : l'intermédiaire sous le livre, face à « Toi » (440 px d'écart)
INTERM_FROM = -90                          # S18 : il entre en marchant depuis la gauche (hors cadre)

# --- la colonne de l'épargne (jauge verticale, 10 blocs) ---
EPARGNE_C, EPARGNE_W, EPARGNE_H = (520, 950), 220, 520      # x 410-630, y 690-1210
EPARGNE_EURO = (0, -300)                   # disque euro (r 34), repère de la colonne : monde (520, 650)
EPARGNE_MONTANT = (0, -385)                # « 10 000 € » ExtraBold 56 : monde (520, 565)
EPARGNE_CORNER = (EPARGNE_W / 2, -EPARGNE_H / 2)   # coin haut droit (630, 690) : départ de la ficelle
EPARGNE_PLUS = (676, 568)                  # S05 : « + » deep, à droite de « 10 000 € » (ExtraBold 56)
LEVELS = {"S01": 0.60, "S02": 0.55, "S04": 0.47, "S05": 0.59, "S11": 0.60, "S13": 0.66, "S14": 0.60}
TOKEN_DV, SLICE_DV = 0.02, 0.03            # un jeton arraché (S04) ; une tranche de gestion (S14)
EPARGNE_S16 = (300, 950)                   # S16 : la colonne glisse à gauche
EPARGNE_MINI, EPARGNE_MINI_K = (140, 1110), 0.45   # S17-S21 : réduite en bas à gauche (x 90-190, y 993-1227)


def level_y(v, c=EPARGNE_C, k=1.0):
    """y monde du haut du remplissage de la colonne au niveau v (colonne en c, échelle k)."""
    return c[1] + k * (EPARGNE_H / 2 - v * EPARGNE_H)


# --- l'étiquette du fil et sa ficelle ---
ETIQ_W, ETIQ_H, ETIQ_SIZE = 220, 64, 34
ETIQ_HOME = (775, 720)                     # S01, S03-S07 : pendue au coin haut droit de la colonne
ETIQ_PESE = (775, 870)                     # S02 « facture » : elle pèse (puis + 20 px sur « lourde »)
ETIQ_LOW = (775, 870)                      # S11-S15 : à portée du stylo de « Toi » (écart assumé, voir en tête)
ETIQ_MOT = (0, -56)                        # mot « frais » au-dessus d'elle (repère de l'étiquette), S01-S07
ETIQ_GRAPH = (480, 1150)                   # S07-S08 : rangée sous l'axe du graphique
ETIQ_TAUX = (560, 480)                     # S09 « 1 % » : à droite de la pilule « 5 % / an »
ETIQ_ON_TAUX = (320, 522)                  # S09 « tombes » : posée sur la pilule tombée (y 558-622)
GESTION_ABOVE = (775, 812)                 # S14 : « gestion » s'écrit au-dessus de l'étiquette en ETIQ_LOW
ETIQ_LISTE = (720, 440)                    # S16-S18 : tête de la liste des frais
ETIQ_TOI = (790, 860)                      # S19 : devant « Toi »
ETIQ_TAP = (790, 888)                      # S19 : point touché (bord bas de l'étiquette, à portée)
ETIQ_TIRE = (812, 880)                     # S19 « frais. » : tirée de ~ 30 px vers « Toi »
ETIQ_BUTE = (709, 905)                     # S20 : collée au bord droit du panneau (x 599-819)
ETIQ_BTN_SCALE = 112 / ETIQ_H              # S21 : 1,75 -> ≈ 385 x 112, la taille du bouton de la carte
TILT = -14                                 # S04, S14 : l'étiquette bascule contre la colonne

# --- le bac des frais, ses jetons, la pile ---
BAC_C, BAC_W, BAC_H = (200, 1170), 260, 100        # x 70-330, y 1120-1220 (trapèze papier, mot « frais »)
BAC_RIM = BAC_C[1] - BAC_H / 2                     # 1120 : bord du bac
JETON_R = 26
BAC_SLOTS = [(118, 1108), (166, 1108), (214, 1108), (262, 1108)]   # 4 jetons (S04), moitié basse dans le bac
BAC_ZERO = (200, 1062)                     # S05 : « + 0 € » Bold 40 au-dessus du bac
PILE_X, PILE_W, PILE_H0 = 150, 80, 400     # pile cyan posée sur le bord du bac (x 110-190)
PILE_C = (PILE_X, BAC_RIM - PILE_H0 / 2)   # (150, 920) : y 720-1120
PILE_BASE = 0.15                           # S06 : les 4 jetons fondus (60 px)
PILE_GAINS_C = (PILE_X, BAC_RIM - PILE_H0 * PILE_BASE - PILE_H0 / 2)   # (150, 860) : sa base à y 1060
PILE_GAINS_V = 0.60                        # S06 « coûter » : les gains perdus montent de y 1060 à 820
PILE_PLUS_DY = [175, 125, 75, 25]          # « + » dans les blocs 1-4 de la jauge des gains (repère local)
PILE_PLUSDE = (175, 632)                   # « plus de » SemiBold 30, au-dessus du tube (y 720)
PILE_MONTANT = (175, 685)                  # « 4 600 € » ExtraBold 56 rouge (x 69-281)
PILE_S11 = 0.75                            # S11 : la pile du bac (gains fondus)
PILE_S14 = 0.85                            # S14 : + 2 tranches de gestion
PILE_S15 = {"h": 520, "value": 0.95}       # S15 « durée. » : le tube allongé à 520 px, bas toujours à y 1120
JETON_ENTREE = (272, 1100)                 # S13 : le jeton de 30 €, dans le bac à droite de la pile
JETON_ENTREE_TXT = (272, 1052)             # « 30 € » Bold 34 juste au-dessus
ETIQ_ENTREE = (300, 1000)                  # S14 : étiquette light « entrée 3 % » au-dessus du jeton (x 205-395 : entre pile et colonne)
TRANCHE_W, TRANCHE_H = EPARGNE_W - 4, 16   # S14 : tranche cyan (0,03 x 520 px)
CROCHET_ENCOURS_X = 395                    # S14 : crochet deep le long du flanc gauche, du sol au niveau 0,60
ENCOURS_TXT = (380, 940)                   # « encours » Bold 34, ancre end

# --- la barre du temps (S04-S06), puis l'axe des 20 ans ---
BARRE_C, BARRE_W, BARRE_H, BARRE_N = (590, 300), 500, 40, 20     # x 340-840
BARRE_1AN = (BARRE_C[0] - BARRE_W / 2 + BARRE_W / BARRE_N / 2, 352)   # sous la case 1
BARRE_20ANS = (790, 352)                   # sous le bout droit
QUESTIONS_C = [(230, 430), (520, 430), (790, 430)]                # S03 : pilules papier
VAGUE_W = 340                              # WAVE.png à 340 px (S19), échelle VAGUE_S04_K en S04
VAGUE_S04, VAGUE_S04_K = (200, 560), 280 / 340
VAGUE_S19 = (330, 640)
VAGUE_PILL_SIZE = 40                       # 33 px à l'écran en S04 (échelle 0,82)

# --- le graphique (S07-S10) ---
AXE_O = (160, 1060)                        # origine des axes
AXE_X1, AXE_TOP = 740, 420                 # bout de l'axe horizontal, haut de l'axe vertical
GRAPH_START = (160, 960)                   # point de départ cyan r 16 (la colonne réduite)
GRAPH_END_X = 680
GRAPH_Y_PER_EURO = 480 / 16533             # 26 533 € -> y 480
GRAPH_MONTANT = (178, 1012)                # « 10 000 € » Bold 34, ancre start, sous le point
AXE_20ANS = (690, 1100)                    # « 20 ans » sous le bout de l'axe (690 : à 720, le stylo de « Toi » au repos coupait le « s »)
COURBE_A_TXT = (600, 430)                  # « ≈ 26 500 € » Bold 40
COURBE_B_TXT = (770, 668)                  # « ≈ 21 900 € » Bold 40, à droite sous le bout de B
CROCHET_X, CROCHET_Y = 715, (480, 614)     # S10 : crochet rouge de l'écart
CROCHET_TXT = (825, 547)                   # « 4 600 € » rouge logé à droite du crochet (échelle 44/56)
CROCHET_TXT_K = 44 / 56
RED_HIGH = (800, 360)                      # S07 : le chiffre rouge monte en haut à droite
QUESTION_ECART = (330, 690)                # S07 « écart ? » : le « ? » contre le chiffre rouge
QUESTION_HIGH = (905, 290)                 # S07 « calcul, » : il monte avec lui
TAUX_C, TAUX_LOW, TAUX_W, TAUX_H = (320, 480), (320, 590), 200, 64
TAUX_DIFF = (320, 665)                     # S09 « net. » : « 5 % − 1 % » Bold 34
MENTION1, MENTION2 = (430, 312), (430, 352)    # S07-S10 : « Exemple théorique, » / « rendement non garanti »


def courbe_pts(rate, years=20):
    """Points monde de la courbe 10 000 € x (1 + rate)^t, t = 0..20, sur le graphique (x 160 -> 680)."""
    dx = (GRAPH_END_X - GRAPH_START[0]) / years
    return [[round(GRAPH_START[0] + t * dx, 1),
             round(GRAPH_START[1] - (10000 * (1 + rate) ** t - 10000) * GRAPH_Y_PER_EURO, 1)] for t in range(years + 1)]


# --- repère 1-2-3 légendé (S11 -> S21) ---
MARKER_Y, MARKER_GAP, MARKER_LABEL, MARKER_DY = 300, 170, 34, 68
MARKER_XS = [CX - MARKER_GAP, CX, CX + MARKER_GAP]          # 370, 540, 710
MARKER_LABELS = ["Entrée", "Gestion", "Autres"]
FRAIS_LABEL = (322, 300)                   # « Frais : » Bold 34, ancre end (x 222-322)
QUESTION_MARKER = (CX, MARKER_Y)           # S11 « savoir » : le « ? » monte à la place du repère

# --- entrée (S12-S14) ---
ENTONNOIR_C = (520, 650)                   # trapèze 240 -> 80 px, 110 de haut : y 595-705, goulot dans la colonne
ENTONNOIR_PTS = [[-120, -55], [120, -55], [40, 55], [-40, 55]]
ENTONNOIR_GOULOT = (520, 705)
ENTONNOIR_TAUX = (345, 640)                # pilule light « 3 % » contre la lèvre gauche (x 290-400)
VERSEMENT_HOME = (720, 990)                # S12 : la carte « 1 000 € » à portée de « Toi »
VERSEMENT_HAUT = (520, 480)                # S13 « 1 000 € » : au-dessus de l'entonnoir
VERSEMENT_970 = (520, 770)                 # S13 « 970 € » : ressort sous le goulot, dans le haut de la colonne
VERSEMENT_W, VERSEMENT_H = 200, 90

# --- liste des frais (S16-S17) ---
LISTE_X = 720
LISTE_YS = [510, 580, 650, 720, 790, 860, 930]
LISTE_H = 56
LISTE_FIL = ((LISTE_X, 472), (LISTE_X, 960))     # ficelle deep 4 px sous l'étiquette du fil

# --- DIC (S17-S18) ---
LIVRE_C, LIVRE_W = (330, 720), 360
QUESTION_LIVRE = (330, 700)                # S17 « retrouver ? »
QUESTION_COIN = (470, 590)                 # S17 « Demande » : sur le coin haut droit du livre
LIVRE_DIC = (0, -72)                       # « DIC » ExtraBold 44 (repère du livre)
LIVRE_LIGNES = [(-80, -30), (-80, 0), (-80, 30), (-80, 60), (80, -30), (80, 0), (80, 30)]   # 7 traits 90 x 8
LIVRE_LEGENDE = [(330, 900), (330, 942)]   # « Document » / « d’informations clés » SemiBold 34

# --- intermédiaire et relevé (S18) ---
INTERM_NOM = (400, 1165)                   # pilule papier « ton intermédiaire » sur sa poitrine
INTERM_OBLIG = (400, 1010)                 # pilule deep « obligatoire » au-dessus de lui
RELEVE_C, RELEVE_H = (680, 790), 220
RELEVE_FROM = (330, 760)                   # sort du livre
RELEVE_VIA = (400, 900)                    # passe devant l'intermédiaire
RELEVE_TITRE_DY, RELEVE_LIGNES_DY = -68, [-2, 56]

# --- panneau « Rendement affiché » (S20) ---
PANNEAU_C, PANNEAU_W, PANNEAU_H = (400, 995), 390, 270       # x 205-595, y 860-1130
PANNEAU_TITRE = (0, -95)                   # « Rendement affiché » SemiBold 32
PANNEAU_TAUX = (85, 10)                    # « 5 % / an » ExtraBold 48 (monde x 390-580, y 1005)
PANNEAU_NET = (85, 85)                     # « 4 % net » ExtraBold 48 deep (monde y 1080)
PANNEAU_TON = (400, 1180)                  # pilule light « ton rendement » sous le panneau
PANNEAU_SIZE = 48

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
    **_OFF("epargne", "bac", "pile", "pile_gains", "pile_plusde", "barre_temps", "barre_1an", "barre_20ans",
           "vague", "epargne_plus", "bac_zero", "jeton1", "jeton2", "jeton3", "jeton4", "pilule_taux",
           "courbe_a_txt", "courbe_b_txt", "marqueur", "question1", "question2", "question3"),
}
ENTRY_P3 = {   # fin de S15 = etat_initial de S16 : colonne au centre, pile « gestion » très haute, disque 2 actif
    "epargne": {"pos": list(EPARGNE_C), "scale": 1, "opacity": 1, "value": LEVELS["S14"]},
    "etiquette": {"pos": list(ETIQ_LOW), "scale": 1, "rot": 0, "opacity": 1, "text": T_ETIQ},
    "ficelle": {"draw": 1},
    "bac": {"pos": list(BAC_C), "scale": 1, "opacity": 1},
    "pile": {"pos": [PILE_X, BAC_RIM - PILE_S15["h"] / 2], "scale": 1, "opacity": 1, "h": PILE_S15["h"],
             "value": PILE_S15["value"]},
    "etiquette_gestion": {"pos": [PILE_X, BAC_RIM - PILE_S15["h"] - 30], "scale": 1, "opacity": 1},
    "jeton_entree": {"pos": list(JETON_ENTREE), "scale": 1, "opacity": 1},
    "jeton_entree_txt": {"pos": list(JETON_ENTREE_TXT), "scale": 1, "opacity": 1},
    "etiquette_entree": {"pos": list(ETIQ_ENTREE), "scale": 1, "opacity": 1},
    "marqueur": {"pos": [CX, MARKER_Y], "scale": 1, "active": 1, "on": 1},
    "frais_label": {"opacity": 1},
    "crochet_encours": {"opacity": 0}, "encours_txt": {"opacity": 0},
    **_OFF("entonnoir", "entonnoir_taux", "versement", "pile_gains", "pile_montant", "pile_plusde", "question",
           "tranche1", "tranche2", "graph_point", "axe_x", "axe_y", "pilule_taux", "jeton1", "jeton2", "jeton3",
           "jeton4"),
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
    # S14 : crochet « encours », du sol au niveau 0,60, le long du flanc gauche (tracé depuis le sol)
    top, bot = level_y(LEVELS["S14"]), FLOOR
    half = (bot - top) / 2
    kit.shape("crochet_encours", [CROCHET_ENCOURS_X, (top + bot) / 2], kind="poly",
              pts=[[14, half], [0, half], [0, -half], [14, -half]], closed=False, fill="none", stroke=DEEP, sw=6,
              shadow=0, z=6.5, draw=0)
    kit.text("encours_txt", ENCOURS_TXT, "encours", size=34, weight=700, anchor="end", z=6.5, opacity=0)
    for k in range(2):        # S14 : deux tranches cyan détachées du haut du remplissage
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

    # --- les trois questions de l'annonce (S03-S04) ---
    for k, (txt, pos) in enumerate(zip(QUESTIONS, QUESTIONS_C)):
        pill(S, f"question{k + 1}", pos, txt, size=34, fill=PAPER, h=60, z=12, shadow=4)

    # --- la barre du temps (20 cases), « 1 an », « 20 ans » ---
    kit.gauge("barre_temps", BARRE_C, value=0, w=BARRE_W, h=BARRE_H, dir="right", segments=BARRE_N, fill=CYAN,
              empty=PAPER, sw=4, shadow=4, z=5, scale=0)
    kit.text("barre_1an", BARRE_1AN, T_1AN, size=34, weight=700, z=5.1, scale=0)
    kit.text("barre_20ans", BARRE_20ANS, T_20ANS, size=34, weight=700, z=5.1, scale=0)

    # --- le bac des frais, ses 4 jetons, « + 0 € » ---
    hw, hh = BAC_W / 2, BAC_H / 2
    kit.shape("bac", BAC_C, kind="poly", pts=[[-hw, -hh], [hw, -hh], [hw - 20, hh], [-hw + 20, hh]], fill=PAPER,
              stroke=INK, sw=5, shadow=6, z=7.5, scale=0)
    kit.text("bac_txt", [0, 8], "frais", size=34, weight=700, z=7.6, parent="bac")
    for k in range(4):        # arrachés au haut du remplissage, ils tombent dans le bac (moitié basse cachée)
        kit.icon(f"jeton{k + 1}", BAC_SLOTS[k], "euro", disc=JETON_R, fill=CYAN, shadow=3, z=7.3, scale=0)
    kit.text("bac_zero", BAC_ZERO, T_ZERO, size=40, weight=700, z=11, scale=0)

    # --- la pile des frais (base cyan), les gains perdus (light, à « + »), « plus de 4 600 € » rouge ---
    kit.gauge("pile", PILE_C, value=PILE_BASE, w=PILE_W, h=PILE_H0, dir="up", segments=8, fill=CYAN, empty=PAPER,
              sw=4, shadow=6, z=7.0, scale=0)
    S.set("pile", fill=CYAN, h=PILE_H0)
    kit.gauge("pile_gains", PILE_GAINS_C, value=0, w=PILE_W, h=PILE_H0, dir="up", segments=8, fill=LIGHT,
              empty="none", sw=3, shadow=0, z=7.05, scale=0)
    for k, dy in enumerate(PILE_PLUS_DY):
        kit.text(f"pile_plus{k + 1}", [0, dy], "+", size=34, weight=800, color=DEEP, z=7.1, parent="pile_gains",
                 scale=0)
    kit.text("pile_plusde", PILE_PLUSDE, "plus de", size=30, weight=600, z=11, scale=0)
    kit.text("pile_montant", PILE_MONTANT, T_4600, size=56, weight=800, color=RED, z=11, scale=0)

    # --- la vague du marché (WAVE.png) et sa pilule « marché » (enfant : elle suit la vague) ---
    wave = S.png("WAVE")
    vague_h = round(VAGUE_W * wave["h"] / wave["w"])
    S.add("vague", "png", z=5, src=wave["src"], w=VAGUE_W, h=vague_h,
          contact=dict(w=round(VAGUE_W * 0.7), h=20, dy=4, blur=10, alpha=0.18))
    S.set("vague", pos=list(VAGUE_S04), scale=0, opacity=1)
    pill(S, "vague_marche", [0, round(vague_h / 2 + 30)], "marché", size=VAGUE_PILL_SIZE, fill=PAPER, h=64, z=5.1,
         parent="vague", scale=1, shadow=4)

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
    kit.text("mention1", MENTION1, "Exemple théorique,", size=30, weight=600, z=9, opacity=0)
    kit.text("mention2", MENTION2, "rendement non garanti", size=30, weight=600, z=9, opacity=0)
    w2, w3 = text_width("rendement non garanti", 30, 600), text_width("non garanti", 30, 600)
    x_end = MENTION2[0] + w2 / 2
    kit.shape("mention_trait", [x_end - w3 / 2, MENTION2[1] + 24], kind="poly", pts=[[-w3 / 2, 0], [w3 / 2, 0]],
              closed=False, fill="none", stroke=DEEP, sw=5, shadow=0, z=9.1, draw=0)

    # --- le « ? » de « Toi » (S07, S11, S17 : un seul id, réutilisé) ---
    S.add("question", "qmark", z=17)
    S.set("question", pos=list(P_TOI), scale=0, opacity=1, gs=90)

    # --- repère 1-2-3 légendé (S11 -> S21), sans étape active jusqu'à « D’abord » (piste on), « Frais : » ---
    kit.steps_marker(MARKER_LABELS, id="marqueur", y=MARKER_Y, cx=CX, gap=MARKER_GAP, z=20)
    S.ents["marqueur"]["p"].update(labelSize=MARKER_LABEL, labelDy=MARKER_DY, moveBlank=True)
    S.set("marqueur", scale=0, on=0, done0=0, done1=0, done2=0)
    kit.text("frais_label", FRAIS_LABEL, T_FRAIS_DEUX_POINTS, size=34, weight=700, anchor="end", z=20, opacity=0)

    # --- l'entonnoir d'entrée et sa pilule « 3 % », la carte du versement, le jeton de 30 €, « entrée 3 % » ---
    kit.shape("entonnoir", ENTONNOIR_C, kind="poly", pts=ENTONNOIR_PTS, fill=PAPER, stroke=INK, sw=5, shadow=6,
              z=8, scale=0)
    pill(S, "entonnoir_taux", ENTONNOIR_TAUX, T_3, size=34, fill=LIGHT, h=56, z=8.2)
    kit.shape("versement", VERSEMENT_HOME, kind="round", w=VERSEMENT_W, h=VERSEMENT_H, r=14, fill=PAPER,
              stroke=INK, sw=4, shadow=6, z=13, scale=0)
    kit.text("versement_txt", [0, 0], T_1000, size=40, weight=800, z=13.1, parent="versement")
    S.set("versement_txt", text=T_1000)
    kit.icon("jeton_entree", ENTONNOIR_GOULOT, "euro", disc=JETON_R, fill=CYAN, shadow=3, z=7.3, scale=0)
    kit.text("jeton_entree_txt", JETON_ENTREE_TXT, T_30, size=34, weight=700, z=11, scale=0)
    pill(S, "etiquette_entree", ETIQ_ENTREE, T_ENTREE3, size=30, fill=LIGHT, h=48, z=8.3, shadow=4, pad=32)

    # --- la liste des frais (S16-S17) : ficelle + 7 étiquettes (light : connues ; papier : nouvelles) ---
    S.add("liste_fil", "wire", z=9.4, color=DEEP, sw=4, tension=0)
    S.set("liste_fil", pa=list(LISTE_FIL[0]), pb=list(LISTE_FIL[1]), sag=0, draw=0, opacity=1)
    for k, ((txt, fill), y) in enumerate(zip(LISTE, LISTE_YS)):
        pill(S, f"liste{k + 1}", [LISTE_X, y], txt, size=34, fill=fill, h=LISTE_H, z=9.6, shadow=4)

    # --- le DIC (BOOK.png) : « DIC », 7 lignes encre, légende ---
    book = S.png("BOOK")
    livre_h = round(LIVRE_W * book["h"] / book["w"])
    S.add("livre", "png", z=5, src=book["src"], w=LIVRE_W, h=livre_h,
          contact=dict(w=round(LIVRE_W * 0.8), h=22, dy=4, blur=10, alpha=0.18))
    S.set("livre", pos=list(LIVRE_C), scale=0, opacity=1)
    kit.text("livre_dic", LIVRE_DIC, "DIC", size=44, weight=800, z=5.3, parent="livre", scale=0)
    for k, pt in enumerate(LIVRE_LIGNES):
        kit.shape(f"livre_ligne{k + 1}", pt, kind="round", w=90, h=8, r=4, fill=INK, stroke=INK, sw=0, shadow=0,
                  z=5.2, parent="livre", scale=0)
    kit.text("livre_legende1", LIVRE_LEGENDE[0], "Document", size=34, weight=600, z=5.1, opacity=0)
    kit.text("livre_legende2", LIVRE_LEGENDE[1], "d’informations clés", size=34, weight=600, z=5.1, opacity=0)

    # --- l'intermédiaire (figurine papier, sans outil), « ton intermédiaire », « obligatoire » ---
    interm = Figure(kit, "intermediaire", pos=list(P_INTERM), scale=INTERM_SCALE, variant="paper", tool=False,
                    z=14.5, show=False)
    S.set("intermediaire", look=0)
    pill(S, "interm_nom", INTERM_NOM, "ton intermédiaire", size=34, fill=PAPER, h=56, z=16.5, shadow=4)
    pill(S, "interm_oblig", INTERM_OBLIG, "obligatoire", size=34, fill=DEEP, h=56, z=16.5, color=PAPER, shadow=4)

    # --- le relevé « Coûts et frais » (S18) : titre souligné, deux lignes « en € » / « en % » (clé deep) ---
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

    # S19 : la ficelle passe au stylo de « Toi » (de la pointe du stylo au bas de l'étiquette)
    S.add("ficelle_toi", "wire", z=15.9, color=DEEP, sw=6, tension=0,
          a={"id": "toi_stylo", "at": [GEOM["PEN"]["len"], 0]}, b={"id": "etiquette", "at": [0, ETIQ_H / 2]})
    S.set("ficelle_toi", sag=0, draw=0, opacity=1)
    S.set("ficelle_toi", **{"from": 0})

    return SimpleNamespace(toi=toi, interm=interm, vague_h=vague_h, livre_h=livre_h, releve_w=releve_w)


def build(S):
    kit = Kit(S)
    c = cast(S, kit)
    only = [p for p in os.environ.get("WTH_PARTS", "").split(",") if p]   # WTH_PARTS=p2 : cette partie seule
    for name in PARTS:
        if not only or name in only:
            importlib.import_module(f".{name}", __name__).part(S, kit, c)
