"""V13 « Ton patrimoine net n’est pas ton solde » : mise en scène Story, en paquet (une partie par fichier).

Storyboard : scripts/storyboards/V13.json (v1, révisé après le test sans son, 22 scènes, 112 temps forts, 92,272 s),
version lisible scripts/storyboards/V13.md. Voix : build/V13/words.json (film : images 0-2768 ; film_end(S) = 2768).
Fil : la pilule cyan « 3 200 € » (`solde`, pill 320 x 100, ExtraBold 60) : sur la carte « Solde » dès l'image 0,
regardée par « Toi » (S01) ; réduite avec sa carte en première case d'une grille de neuf (S02) ; dans sa case pendant
tout le calcul (S03-S19) ; sort vers « Toi », regard rouge barré, rentre (S20-S21) ; devient le bouton « S’abonner »
(S22). Jamais d'autre chiffre.
Parti pris : « le puzzle de ton patrimoine » : une grille de neuf cases (`grille`) = ce que tu possèdes ; la carte grise
« Ce que tu dois » (`dettes`) = la part de la banque ; la pilule « Patrimoine net » (`net`) = le résultat.
Pas d'IA dans ce film : « Toi » (figurine encre) est seul à tenir le stylo. Aucune coche d'IA, aucun pointillé d'IA.

Parties : p1 S01-S08 (images 0-986) ; p2 S09-S15 (987-1915) ; p3 S16-S22 (1916-2768). ENTRY_P2 et ENTRY_P3 sont le
contrat des raccords (kit.pin(f0 - 1, …)). Les figurines n'y sont jamais.

Code partagé : aucun nouveau type. Pictogrammes ajoutés à `Icon` (motion/src/story/draw.tsx, noms opt-in, aucun dessin
existant ne change) : `car` (case « Véhicule »), `eye` (l'œil de « Toi » sur les pastilles gardées, S18) et `unlock`
(cadenas ouvert de « disponible », opposé au cadenas fermé de « bloqué », S17).

TOUR DE REVUE 1 (corrections ; aucun temps fort déplacé, aucun texte du storyboard changé) :
- mise en page : repère en y 340 ; grille pleine x 70-788, y 460-1032 (cases 230 x 180, pas 244 x 196 : elle dégage la
  pilule « Toi ») ; grille réduite ×0,65 (x 60-527, y 460-832) SANS libellés : ses pictogrammes passent au centre des
  cases à ×1,4 (la pilule du solde, élargie à 34 px de corps rendus, et le jeton de l'immobilier en tiennent lieu) ;
  barre de l'appartement x 140-700, y 985-1095 (rapport 157 / 403 gardé) ; équation finale abaissée (« Patrimoine net »
  en (540, 960), « Limites » en y 1100) ;
- S08 : le stylo émet chaque nom (pilule-libellé née de la pointe à chaque mot, qui vole dans sa case « ? ») ;
- S10 : l'étiquette porte une date (« 2015 » -> « aujourd’hui ») et une flèche du temps se trace dessous ;
- S11-S15 : la barre naît du bas du jeton, porte une maison, une accolade deep la couvre en entier et la relie à
  l'étiquette (« la barre = la valeur de la maison ») ; la carte grise sort du disque 2 (onde) par un arc au-dessus
  du repère ; un fil relie la banque au disque 2 (S12) ; la part grise est faite de 12 tranches, une seule (rouge)
  est la mensualité (S13) ; S14 : valeurs posées (pas de compteur), copie « 250 000 € » sur l'accolade ; S15 : la
  part grise retirée laisse un contour en tirets ;
- S16-S18 : « Patrimoine net » naît sous la grille, signe d'attention 72 px, fente ; il monte à droite sur « mélange »
  (cadre + fil) ; six pastilles plus grandes, attachées à leur case, passent par la pilule, paires opposées (cadenas
  ouvert / fermé, bouclier / attention, trait plein / tirets) et « ↔ » ; « disponible » et « risqué » prennent l'œil de
  « Toi », qui les regarde à tour de rôle ;
- S19 : les points naissent de la pointe ; S21 : regard long (tirets encre -> plein deep), « Toi » se penche.
"""
import importlib
import math
import os
from types import SimpleNamespace

from pipeline.story import GEOM, STYLE, text_width
from pipeline.story_kit import Figure, Kit

PARTS = ["p1", "p2", "p3"]                      # S01-S08, S09-S15, S16-S22
NBSP, NNBSP = " ", " "                # espace insécable (avant « : », « ? », « € »), fine insécable (milliers)
ALERT_WORDS = {"prix", "d’achat", "mensualités"}   # karaoké en rouge : « Prix d’achat » (S10), tranche « Mensualité » (S13)
ACOUSTIC_SNAP = {"gap": 0.2, "window": 0.08}    # temps fort après un silence : calé sur l'attaque audible
CAPTION_GROUPS = [                              # tour 1 : pas de déterminant, de négation ni d'adjectif coupé, pas de
    ["Ce chiffre", "ne dit presque rien"],      # mot seul (groupes sans montant : « 250 000 € » est un seul mot)
    ["Et comment", "bien lire ce chiffre"],
    ["Parce que", "ton solde n’en montre", "souvent qu’une partie"],
    ["Fais la liste complète"],
    ["Et note", "leur valeur actuelle", "pas leur prix d’achat"],
    ["Ça ne suffit pas"],
    ["posséder un bien", "ne veut pas dire", "qu’il est à toi", "en entier"],
    ["Il ne représente pas"],
    ["Dernier point", "et pas le moindre"],
    ["Retiens ça", "ton patrimoine", "ce n’est pas", "ton solde"],
]

# ---------- couleurs ----------
INK, CYAN, DEEP, LIGHT = STYLE["ink"], STYLE["cyan"], STYLE["deep"], STYLE["light"]
PAPER, RED, RULE, GREY = STYLE["paper"], STYLE["red"], STYLE["rule"], STYLE["grey"]
SLICE = "#A69C8B"                               # traits des 12 tranches de la part grise (plus foncés que le gris)

# ---------- textes à l'écran (typographie française) ----------
T_SOLDE_VAL = f"3{NNBSP}200{NBSP}€"
T_ABONNER = "S’abonner"
T_SOLDE, T_COMPTES, T_TOI = "Solde", "Comptes", "Toi"
T_Q = "?"
T_NET = "Patrimoine net"
T_ENTETE = "Ce que tu possèdes"
T_MOINS, T_EGAL = "−", "="
T_DOIS_CARTE = "Ce que\ntu dois"                # carte grise (deux lignes, ancre start)
T_DOIS_BARRE = "Ce que tu dois"                 # part grise (S11, une ligne)
T_CRD = "Capital restant dû"                    # S12
T_STRATEGIE = "Ta stratégie"
T_PRIX_ACHAT, T_VALEUR = "Prix d’achat", "Valeur actuelle"
T_AN_ACHAT, T_AUJOURDHUI = "2015", "aujourd’hui"   # S10 : date de l'étiquette (achat -> aujourd'hui)
T_MENSUALITE = "Mensualité"
T_RESTANT = "restant à rembourser"
T_250 = f"250{NNBSP}000{NBSP}€"
T_180 = f"180{NNBSP}000{NBSP}€"
T_RESULTAT = f"≈{NBSP}70{NNBSP}000{NBSP}€ nets"
T_CALC_A = f"250{NNBSP}000{NBSP}€ {T_MOINS} 180{NNBSP}000{NBSP}€ = "   # encre
T_CALC_B = f"70{NNBSP}000{NBSP}€"                                        # deep
T_FREQ = "1 ou 2 fois / an"
T_AXE_Y, T_AUJ = "Patrimoine net", "aujourd’hui"
T_ANS = ["1 an", f"2{NBSP}ans", f"3{NBSP}ans"]
T_POSSEDES, T_DOIS, T_LIMITES = "Possèdes", "Dois", "Limites"
T_PAIRE = "↔"
MARKER_LABELS = [T_POSSEDES, T_DOIS, T_LIMITES]
# S08 : la pilule-libellé que le stylo émet à chaque mot (case 0 : « Comptes », la carte du solde)
LBL_TEXTS = ["Comptes", "Livrets", "Assurance-vie", "PEA", "Épargne salariale", "PER"]

# ---------- mise en page (1080 x 1920) ----------
X_MIN, X_MAX, Y_MIN, Y_MAX = 40, 930, 160, 1270  # zone d'action ; on descend jusqu'à y ≈ 1250
GROUND = 1230                                   # pied de « Toi »
FIG_BASE = GEOM["FIGURE"]["base"]               # 95
HEAD_DY = GEOM["FIGURE"]["head"]["cy"]          # -64 : centre de la tête
HEAD_R = GEOM["FIGURE"]["head"]["r"]            # 32
SHOULDER_DX, SHOULDER_DY = abs(GEOM["FIGURE"]["shoulder"][0]), GEOM["FIGURE"]["shoulder"][1]   # 30, -16
REACH_OK = 267                                  # allonge confortable (REACH x 284) à l'échelle 1
LOW_ROT_V13 = 40                                # stylo baissé plus à plat (pointe en y ≈ 1252, au-dessus des sous-titres)


def fig_pos(x, feet=GROUND, s=1.0):
    return [x, round(feet - FIG_BASE * s, 2)]


# --- « Toi » : bras côté gauche (il fait face à gauche) ; pied sur y 1230 ---
TOI_P1 = fig_pos(850)                           # (850, 1135) : repos ; épaule (820, 1119) ; haut de la tête 1039
TOI_P2 = fig_pos(590)                           # (590, 1135) : S03 (écrire, souligner)
TOI_P3 = fig_pos(560)                           # (560, 1135) : S09-S10, sous la grille pleine (tête à 7 px des cases)
HEAD_P1 = (850, 1071)
NOM_ABOVE, NOM_RIGHT = (0, -140), (100, -75)    # pilule « Toi » (enfant) : au-dessus de la tête en P1 (850, 995) ;
NOM_W, NOM_H = 100, 56                          # à droite de la tête en P2 / P3 (x + 100, 1060)
NOM_RIGHT_LOW = (100, -40)                      # S09-S10 (P3, sous la grille pleine) : à droite de la tête, plus bas
NOM_LEFT = (-100, -75)                          # S18-S19 : à gauche de la tête (le regard de « Toi » monte au-dessus)
QUESTION_C, Q_GS = (722, 905), 90               # « ? » de « Toi » (S01-S02), né de la tête, à gauche de sa pilule

# --- regard de « Toi » (wire, pistes pa / pb) ---
REGARD_EYE = (815, 1055)                        # S01 ; S20 (815, 1060)
REGARD_EYE_S20, REGARD_SOLDE_S20 = (815, 1060), (528, 1140)   # S20 : vers le bout droit de la pilule sortie (x 525)
REGARD_BARRE = ((688, 1070), (712, 1118))       # S21 « C’est » : le stylo coupe le regard près de la tête
REGARD_NET = ((815, 1050), (545, 994))          # S21 « dois. » : regard long, de la tête au milieu du bas de la pilule

# --- la grille 3 x 3 (groupe `grille`) ---
CELL_W, CELL_H, CELL_R, CELL_DX, CELL_DY = 230, 180, 16, 244, 196
GRILLE_FULL, GRILLE_FULL_K = (429, 746), 1.0    # x 70-788, y 460-1032 (S02, S06-S10)
GRILLE_SMALL_K = 0.65
GRILLE_SMALL = (round(60 + (2 * CELL_DX + CELL_W) / 2 * GRILLE_SMALL_K, 1),
                round(460 + (2 * CELL_DY + CELL_H) / 2 * GRILLE_SMALL_K, 1))   # (293.4, 645.9) : x 60-527, y 460-832
GRID_SMALL_BOTTOM = round(GRILLE_SMALL[1] + (CELL_DY + CELL_H / 2) * GRILLE_SMALL_K, 1)   # 832
GRID_SMALL_RIGHT = round(GRILLE_SMALL[0] + (CELL_DX + CELL_W / 2) * GRILLE_SMALL_K, 1)    # 527
CELL_LOCAL = [((c - 1) * CELL_DX, (r - 1) * CELL_DY) for r in range(3) for c in range(3)]   # ordre de lecture
# case -> (id, libellé, pictogramme, corps) ; la case 0 est la carte « Solde » (`compte`)
CASES = [None,
         ("livrets", "Livrets", "coin", 34), ("assurance", "Assurance-\nvie", "shield", 32),
         ("pea", "PEA", "bars", 34), ("epargne", "Épargne\nsalariale", "person", 32),
         ("per", "PER", "hourglass", 34), ("immo", "Immobilier", None, 32),
         ("vehicule", "Véhicule", "car", 34), ("societe", "Parts de\nsociété", "building", 32)]
CASE_IDS = [None] + [f"case_{c[0]}" for c in CASES[1:]]      # cases nommées (scale 0 jusqu'à leur mot)
Q_IDS = [None] + [f"q_{c[0]}" for c in CASES[1:]]            # cases « ? » (scale 0 jusqu'à S02 « presque »)
CELL_ICO_LOCAL, CELL_DISC_R = (0, -32), 32
CELL_MOT_LOCAL, CELL_MOT2_LOCAL = (0, 52), (0, 48)           # libellé une ligne / deux lignes (32 px)
ICO_SMALL_LOCAL, ICO_SMALL_K = (0, 0), 1.4                   # grille réduite : pictogramme au centre, ×1,4 (58 px rendus)
PCT_LOCAL, PCT_R = (28, -8), 14                              # « Parts de société » : petit disque % au coin du bâtiment
PCT_SMALL_LOCAL = (round(28 * ICO_SMALL_K, 1), round(24 * ICO_SMALL_K, 1))
IMMO_PLACE_LOCAL, IMMO_PLACE_W = (0, 0), 96                  # S11-S16 : cercle en tirets à la place du jeton


def grid_world(local, small=False):
    """Point monde d'un point du repère de la grille (GRILLE_FULL ou GRILLE_SMALL)."""
    c, k = (GRILLE_SMALL, GRILLE_SMALL_K) if small else (GRILLE_FULL, GRILLE_FULL_K)
    return [round(c[0] + local[0] * k, 1), round(c[1] + local[1] * k, 1)]


def cell_world(i, small=False, dy=0):
    """Centre monde de la case i (0-8), décalé de dy (repère de la grille)."""
    return grid_world((CELL_LOCAL[i][0], CELL_LOCAL[i][1] + dy), small)


# --- la carte « Solde » (enfant de la grille ; devient la case « Comptes ») et la pilule du solde (monde) ---
COMPTE_C0, COMPTE_W0, COMPTE_H0 = (540, 700), 440, 300       # S01 : x 320-760, y 550-850
COMPTE_LOCAL0 = (COMPTE_C0[0] - GRILLE_FULL[0], COMPTE_C0[1] - GRILLE_FULL[1])
COMPTE_ICO0, COMPTE_ICO_S0 = (-160, -95), 40   # pictogramme bank
COMPTE_MOT0, COMPTE_MOT_S0 = (-128, -82), 40   # « Solde » Bold 40, ancre start
COMPTE_FILET0, COMPTE_FILET_W0 = (0, -50), 408
COMPTE_ICO_CELL, COMPTE_MOT_CELL = (-80, -60), (-55, -48)    # case : bank 30 px, « Solde » / « Comptes » Bold 34
COMPTE_ICO_CELL_K, COMPTE_MOT_CELL_K = 0.75, 0.85
REGARD_CARTE = (COMPTE_C0[0] + 70, COMPTE_C0[1] + 155)       # S01 : bas de la carte « Solde » (610, 855)
REGARD_CASE = (GRILLE_FULL[0] - CELL_DX + 37, GRILLE_FULL[1] - CELL_DY + 93)   # S02 : le même point de la case
SOLDE_W, SOLDE_H, SOLDE_SIZE = 320, 100, 60
SOLDE_C0 = (COMPTE_C0[0], COMPTE_C0[1] + 50)    # S01 (échelle 1)
SOLDE_CELL_DY = 25                              # grille pleine : 25 px sous le centre de la case
SOLDE_CELL_K = 0.62                             # 198 x 62 dans la grille pleine
SOLDE_CELL_FULL = tuple(cell_world(0, False, SOLDE_CELL_DY))  # (185, 575)
SOLDE_SMALL_K, SOLDE_SMALL_W = round(34 / SOLDE_SIZE, 4), 262  # grille réduite : 140 x 57, corps 34 px rendus
SOLDE_CELL_SMALL = tuple(cell_world(0, True, 0))              # centre de la case réduite (134.8, 518.5)
SOLDE_OUT, SOLDE_OUT_K = (420, 1140), 0.8       # S20 : sortie vers « Toi » (256 x 80)

# --- l'équation (S03-S05, S20-S21) ---
ENTETE_C = (GRILLE_SMALL[0], 420)               # « Ce que tu possèdes » Bold 36 (S04-S06)
CADRE_C = GRILLE_SMALL
CADRE_W = round((2 * CELL_DX + CELL_W) * GRILLE_SMALL_K + 24)  # 491 : x 48-539
CADRE_H = round((2 * CELL_DY + CELL_H) * GRILLE_SMALL_K + 24)  # 396 : y 448-844
MOINS_C, EGAL_C, EGAL_CHUTE = (589, 646), (250, 960), (250, 930)
SIGNE_SIZE = 90
DETTES_C, DETTES_W, DETTES_H = (765, 646), 250, 150           # carte grise x 640-890, y 571-721
DETTES_ICO_CARD, DETTES_ICO_S = (-75, -32), 44
DETTES_MOT_CARD = (-40, -6)                     # « Ce que / tu dois » Bold 34, ancre start
MARKER_Y, MARKER_CX, MARKER_GAP, MARKER_LABEL = 340, 540, 180, 34   # disques x 360, 540, 720 ; légendes y 402
MARKER_DISCS = [(360, MARKER_Y), (540, MARKER_Y), (720, MARKER_Y)]
MARKER_LEGENDS = [(360, MARKER_Y + 62), (540, MARKER_Y + 62), (720, MARKER_Y + 62)]
DISQUE2, DISQUE3 = MARKER_DISCS[1], MARKER_DISCS[2]
NET_W, NET_H, NET_SIZE = 400, 96, 40
NET_C = (540, 960)                              # S03-S05, S16 ; ×1,15 après « honnête »
NET_PEN = (500, 1015)                           # S03 « patrimoine » : née sous la pointe
NET_TRAIT_LOCAL = ((-190, 60), (190, 60))       # soulignement (350 -> 730, y 1020), enfant de `net`
NET_PEN_TRACE = ((350, 1020), (510, 1020))      # la pointe ; le trait file seul jusqu'en 730
NET_P3, NET_P3_K = (735, 540), 0.85             # S17-S19 : 340 x 82
NET_CHUTE, NET_CHUTE_K = (540, 930), 1.2       # S20 (×1) puis S21 (×1,2) : y 872-988, le regard de S21 monte vers elle
NET_FROM_GRID = (GRILLE_SMALL[0], GRID_SMALL_BOTTOM)   # S16 : naît du bord bas de la grille réduite
FIL_GRILLE_A, FIL_NET_A = (0, CADRE_H / 2), (-110, -48)
FIL_DETTES_A, FIL_NET_B = (0, DETTES_H / 2), (110, -48)
FIL_P3_CADRE = (CADRE_W / 2, 0)                 # S17 : milieu du bord droit du cadre (toute la grille)
FIL_P3_NET = (-NET_W / 2, 0)                    # -> bout gauche de la pilule
FENTE_PTS = [[78, -46], [68, -20], [82, 2], [70, 26], [78, 46]]   # S16 : fente entre « Patrimoine » et « net »

# --- la cible de la stratégie (S05) ---
CIBLE_C, CIBLE_W = (190, 1130), 180
DEPART_C, DEPART_R = (372, 1010), 12            # point de départ cyan au bas gauche de « Patrimoine net » (×1,15)
FLECHE_B = (262, 1064)                          # pointe de la flèche, au bord de la cible
FLECHE_ROT = round(math.degrees(math.atan2(FLECHE_B[1] - DEPART_C[1], FLECHE_B[0] - DEPART_C[0])), 1)
STRATEGIE_C = (190, 1245)

# --- le jeton-maison (TOKEN.png, monde) et l'étiquette de prix (S09-S16) ---
JETON_W = 120                                   # largeur déclarée ; échelle = largeur voulue / 120
JETON_CELL_K = 0.88                             # dans sa case pleine (S09-S10) : 106 px
JETON_CELL = tuple(cell_world(6, False, -28))   # (185, 914) : au-dessus du libellé « Immobilier »
JETON_P2, JETON_P2_K = (755, 540), round(200 / JETON_W, 4)    # S11-S15 : 200 px (y 440-640)
JETON_SMALL_K = round(JETON_CELL_K * GRILLE_SMALL_K, 4)       # S16-S21 : 69 px, au centre de la case réduite
JETON_SMALL = tuple(cell_world(6, True, 0))
ETIQ_W, ETIQ_H = 300, 140
ETIQ_PTS = [[-150, 0], [-100, -70], [150, -70], [150, 70], [-100, 70]]   # pointe à gauche
ETIQ_S10 = (337, 1120)                          # S10 : sous la case « Immobilier » (x 187-487, y 1050-1190)
ETIQ_P2 = (755, 765)                            # S11-S15 : sous le jeton (x 605-905, y 695-835)
OEILLET_LOCAL, OEILLET_R = (-125, 0), 9
ACHAT_LOCAL, ACHAT_SIZE = (25, -22), 32         # « Prix d’achat » rouge
VALEUR_LOCAL, VALEUR_SIZE = (25, -22), 32       # « Valeur actuelle » deep
DATE_LOCAL, DATE_H = (16, 34), 48               # S10 : pilule-date (calendrier) dans le bas de l'étiquette
MONTANT_LOCAL, MONTANT_SIZE = (25, 32), 44      # « 250 000 € » (S14) : posé, pas compté
_W_ACHAT = text_width(T_PRIX_ACHAT, ACHAT_SIZE, 700)
ACHAT_STRIKE = ((round(ETIQ_S10[0] + ACHAT_LOCAL[0] + _W_ACHAT / 2 + 3, 1), ETIQ_S10[1] + ACHAT_LOCAL[1]),
                (round(ETIQ_S10[0] + ACHAT_LOCAL[0] - _W_ACHAT / 2 - 3, 1), ETIQ_S10[1] + ACHAT_LOCAL[1]))
FICELLE_CASE_A = (0, CELL_H / 2)                # bas de la case « Immobilier »
TEMPS_A, TEMPS_B = (190, 1218), (468, 1218)     # S10 : flèche du temps sous l'étiquette (passé -> aujourd'hui)

# --- la barre de l'appartement et la part grise (S11-S15) ---
BARRE_C, BARRE_W, BARRE_H = (420, 1040), 560, 110             # x 140-700, y 985-1095
BARRE_SHORT_W = 157                                           # part cyan (rapport 179 / 640 gardé)
BARRE_SHORT_C = (round(140 + BARRE_SHORT_W / 2, 1), 1040)     # x 140-297
GRISE_W, GRISE_H = BARRE_W - BARRE_SHORT_W, 110               # 403
GRISE_C = (round(140 + BARRE_SHORT_W + GRISE_W / 2, 1), 1040)  # x 297-700 (la carte `dettes`)
GAP = 12
GRISE_GAP_C = (GRISE_C[0] + GAP, 1040)          # S12 « retire » : détachée de 12 px vers la droite (x 309-712)
GRISE_ICO_S = 40
GRISE_TAP = (684, 1062)                         # S12, S14 : toucher la part grise depuis P1
MAISON_C = (180, 1040)                          # pictogramme maison au bout gauche (cyan) de la barre
N_TRANCHES = 12                                 # S13 : la part grise = 12 tranches (12 mensualités à venir)
TRANCHE_W = GRISE_W / N_TRANCHES                # 33,6
MENS_LOCAL = (round(GRISE_W / 2 - TRANCHE_W / 2, 1), 0)       # la tranche de droite (repère de la carte)
MENS_TAP = (round(GRISE_GAP_C[0] + MENS_LOCAL[0], 1), 1070)   # S13 : toucher la tranche de droite
MENS_MOT = (566, 1140)                          # « Mensualité » rouge Bold 34, ancre start (x 566-750)
MENS_CAL = (540, 1140)                          # petit calendrier rouge devant
_W_MENS = text_width(T_MENSUALITE, 34, 700)
MENS_STRIKE = ((round(MENS_MOT[0] + _W_MENS + 4, 1), MENS_MOT[1]), (MENS_MOT[0] - 4, MENS_MOT[1]))
CROCHET_C = (423, 968)                          # accolade deep sur TOUTE la barre (x 140-706), pointe en haut
CROCHET_PTS = [[-283, 14], [-283, 2], [-12, 2], [0, -14], [12, 2], [283, 2], [283, 14]]
CROCHET_FIL = ((706, 958), (702, 836))          # de son bout droit au bas de l'étiquette « Valeur actuelle »
CROCHET_VAL = (423, 926)                        # S14 : copie « 250 000 € » posée sur l'accolade
ACCOLADE_C = (GRISE_GAP_C[0], 1112)             # S13 : accolade SOUS la part grise (x 309-712), pointe en bas
ACCOLADE_PTS = [[-201, -12], [-201, 0], [-12, 0], [0, 14], [12, 0], [201, 0], [201, -12]]
RESTANT_C = (GRISE_GAP_C[0], 1160)
BRUT_C, BRUT_W, BRUT_H, BRUT_SIZE = (660, 1165), 230, 76, 36  # « 250 000 € » rouge sous la part grise (x 545-775)
_W_BRUT = text_width(T_250, BRUT_SIZE, 800)
BRUT_STRIKE = ((round(BRUT_C[0] + _W_BRUT / 2 + 3, 1), BRUT_C[1] - 2), (round(BRUT_C[0] - _W_BRUT / 2 - 3, 1),
                                                                         BRUT_C[1] - 2))
RESULTAT_C, RESULTAT_W, RESULTAT_H = (330, 1150), 380, 80     # « ≈ 70 000 € nets » (x 140-520)
CALC_X, CALC_Y, CALC_SIZE = 120, 1230, 34       # « 250 000 € − 180 000 € = » (encre) + « 70 000 € » (deep)
FIL_BANQUE_VIA = (560, 880)                     # S12 : fil banque -> disque 2, entre la grille et l'étiquette

# --- point 3 : signe d'attention, pastilles, graphe (S16-S19) ---
ALERTE_R = 36                                   # 72 px
ALERTE_C = (NET_C[0] + 188, NET_C[1] - 46)      # S16 : coin haut droit de « Patrimoine net » (728, 914)
ALERTE_P3 = (NET_P3[0] + 158, NET_P3[1] - 38)   # S17-S19 : coin de la pilule montée (893, 502)
ALERTE_CHUTE, ALERTE_CHUTE_K = (455, 1074), round(22 / ALERTE_R, 4)   # S21 : devant « Limites »
PAST_W, PAST_H, PAST_SIZE = 300, 80, 36
PAST_ICO_LOCAL, PAST_MOT_LOCAL, PAST_DISC = (-112, 0), (-76, 0), 26
PAST_COLS, PAST_ROWS = (240, 610), (1075, 985, 895)          # paires remplies de bas en haut (rien ne se croise)
# id -> (mot, pictogramme (None : « ≈ »), place S17, case d'origine (indice ; -1 : la pilule du solde ; 6 : le jeton),
#        contour en tirets (l'estimé, comme les « ? »))
PASTILLES = {
    "past_disponible": ("disponible", "unlock", (PAST_COLS[0], PAST_ROWS[0]), -1, False),
    "past_bloque": ("bloqué", "lock", (PAST_COLS[1], PAST_ROWS[0]), 5, False),
    "past_sur": ("sûr", "shield", (PAST_COLS[0], PAST_ROWS[1]), 1, False),
    "past_risque": ("risqué", "warning", (PAST_COLS[1], PAST_ROWS[1]), 3, False),
    "past_estime": ("estimé", None, (PAST_COLS[0], PAST_ROWS[2]), 6, True),
    "past_reel": ("réel", "check", (PAST_COLS[1], PAST_ROWS[2]), -1, False),
}
PAIRE_X = round((PAST_COLS[0] + PAST_COLS[1]) / 2, 1)          # « ↔ » entre les deux colonnes
PAST_TOUCH = (700, 606)                         # S17 : le bas de la pilule montée (passage de chaque pastille)
PAST_GARDE = {"past_disponible": (750, 650), "past_risque": (690, 760)}   # S18 : sous « Patrimoine net »
OEIL_LOCAL, OEIL_R = (PAST_W / 2, 0), 22        # œil de « Toi » sur le bout droit des deux pastilles gardées
REGARD_GARDE_EYE = (846, 1040)                  # haut de la tête (sa pilule est passée à gauche)
AXE_PTS = [[120, 860], [120, 1180], [720, 1180]]                # axes en L (monde) ; x s'arrête à 50 px du bras
AXE_Y_TIP, AXE_X_TIP = (120, 852), (728, 1180)
AXE_Y_MOT, AUJ_C = (140, 870), (160, 1222)      # « Patrimoine net » (ancre start), « aujourd’hui »
GRAD_XS, GRAD_Y = [300, 440, 580], 1222
POINTS = [(160, 1080), (230, 1062), (300, 1074), (370, 1046), (440, 1058), (510, 1020), (580, 1032), (650, 1000)]
POINT_R = 14
FREQ_C, FREQ_W, FREQ_H = (560, 885), 330, 64    # « 1 ou 2 fois / an »
ECART_H = [[160, 1080], [685, 1080]]            # trait fin deep 3 px
ECART_V = [[685, 1080], [685, 1000]]            # double flèche deep 4 px
AXE_TAP = (690, 1178)                           # S19 « calcule-le » : depuis P1

# --- légendes de l'équation finale (S21) ---
LEG_POSSEDES, LEG_DOIS, LEG_LIMITES = (200, 866), (765, 760), (560, 1082)   # « Possèdes » à gauche de la pilule

# --- la fin (kit.outro) : carte (540, 760), bouton 380 x 112 ; toucher au doigt, pas de flèche de souris ---
FIN_C = (540, 760)
FIN_BUTTON = (540, 908)
FIN_TAP = (684, 944)


def scene_f0(S, sid):
    return round(next(s for s in S.sb["scenes"] if s["id"] == sid)["t_start"] * S.fps)


def film_end(S):
    """Première image après le film (fin de la dernière scène du storyboard)."""
    return round(S.sb["scenes"][-1]["t_end"] * S.fps)


# ---------- l'allonge de « Toi » (bras gauche) ----------
def arm_check(fig_x, pt, fig_y=TOI_P1[1]):
    """(distance épaule -> cible, côté sûr, dégagement de la tête) pour « Toi » (side left) en (fig_x, fig_y)."""
    sx, sy = fig_x - SHOULDER_DX, fig_y + SHOULDER_DY
    dx, dy = pt[0] - sx, sy - pt[1]
    d = math.hypot(dx, dy)
    safe = -dx >= 0.3 * max(dy, 0) or abs(dx) < 1e-6
    hx, hy = fig_x, fig_y + HEAD_DY
    ux, uy = (pt[0] - sx) / max(d, 1e-6), (pt[1] - sy) / max(d, 1e-6)
    clear = min(math.hypot(sx + ux * t - hx, sy + uy * t - hy) for t in range(0, int(min(d, 120)) + 1))
    return round(d, 1), safe, round(clear, 1)


def assert_reach(fig_x, pt, what, fig_y=TOI_P1[1]):
    d, safe, clear = arm_check(fig_x, pt, fig_y)
    assert 63 <= d <= REACH_OK and safe and clear >= HEAD_R + 8, \
        f"{what} : hors d'allonge depuis x {fig_x} : {d} px, côté sûr {safe}, tête {clear} px"


TAP_GRILLE = (762, 1026)                        # S08 : bas de la case en bas à droite, depuis P1
for _x, _pt, _what in [(TOI_P2[0], NET_PEN, "S03 naissance de « Patrimoine net »"),
                       (TOI_P2[0], NET_PEN_TRACE[0], "S03 début du soulignement"),
                       (TOI_P2[0], NET_PEN_TRACE[1], "S03 fin du geste de soulignement"),
                       (TOI_P1[0], TAP_GRILLE, "S08 toucher le bas de la grille"),
                       (TOI_P3[0], ACHAT_STRIKE[0], "S10 « Prix d’achat » (droite)"),
                       (TOI_P3[0], ACHAT_STRIKE[1], "S10 « Prix d’achat » (gauche)"),
                       (TOI_P1[0], GRISE_TAP, "S12 / S14 toucher la part grise"),
                       (TOI_P1[0], MENS_TAP, "S13 toucher la tranche de droite"),
                       (TOI_P1[0], MENS_STRIKE[0], "S13 « Mensualité » (droite)"),
                       (TOI_P1[0], MENS_STRIKE[1], "S13 « Mensualité » (gauche)"),
                       (TOI_P1[0], BRUT_STRIKE[0], "S15 « 250 000 € » (droite)"),
                       (TOI_P1[0], BRUT_STRIKE[1], "S15 « 250 000 € » (gauche)"),
                       (TOI_P1[0], AXE_TAP, "S19 toucher l'axe du temps"),
                       (TOI_P1[0], REGARD_BARRE[0], "S21 barrer le regard (haut)"),
                       (TOI_P1[0], REGARD_BARRE[1], "S21 barrer le regard (bas)")]:
    assert_reach(_x, _pt, _what)


# ---------- petites fabriques ----------
def png(S, id, name, w, pos, z=5, contact=True, parent=None, scale=0, **extra):
    """Illustration générique (verre, alpha strict), largeur w, rapport gardé. -> meta (+ h_disp)."""
    m = S.png(name)
    h = round(w * m["h"] / m["w"])
    p = dict(contact=dict(w=round(w * 0.7), h=22, dy=4, blur=10, alpha=0.2)) if contact else {}
    S.add(id, "png", z=z, parent=parent, src=m["src"], w=w, h=h, **p, **extra)
    S.set(id, pos=list(pos), scale=scale, opacity=1, rot=0)
    return {**m, "h_disp": h}


def pill(S, id, pos, text, size=34, weight=700, fill=LIGHT, h=56, z=11.5, parent=None, scale=0, pad=48, w=None,
         shadow=4, **p):
    """Pilule de texte (type pill) ; w mesuré si absent (+ 30 px pour un pictogramme). -> largeur."""
    if w is None:
        w = round(text_width(text, size, weight) + pad + (30 if p.get("icon") else 0))
    S.add(id, "pill", z=z, parent=parent, text=text, w=w, h=h, size=size, weight=weight, fill=fill, shadow=shadow, **p)
    S.set(id, pos=list(pos), scale=scale, opacity=1, fill=fill, w=w, text=text, textOp=1)
    return w


def line(kit, id, pts, color=INK, sw=7, z=12, parent=None, pos=(0, 0)):
    """Trait ouvert à tracer (shape poly, draw 0) ; le 1er sommet est le départ du tracé."""
    return kit.shape(id, list(pos), kind="poly", pts=[list(q) for q in pts], closed=False, fill="none", stroke=color,
                     sw=sw, shadow=0, z=z, parent=parent, draw=0)


def head(kit, id, at, rot, color=DEEP, z=12, s=1.0):
    """Pointe de flèche (triangle plein) posée en `at`, orientée `rot` ; scale 0 (pop à la fin du tracé)."""
    pts = [[round(6 * s, 1), 0], [round(-16 * s, 1), round(-11 * s, 1)], [round(-16 * s, 1), round(11 * s, 1)]]
    kit.shape(id, list(at), kind="poly", pts=pts, fill=color, stroke=color, sw=2, shadow=0, z=z, rot=rot, scale=0)
    return id


def wire(S, id, z, color, sw, pa=None, pb=None, a=None, b=None, **p):
    """Fil (wire) à tracer : ancres a / b {id, at}, ou extrémités libres pa / pb (pistes monde)."""
    S.add(id, "wire", z=z, color=color, sw=sw, **({"a": a} if a else {}), **({"b": b} if b else {}), **p)
    S.set(id, draw=0, sag=0, opacity=1)
    S.set(id, **{"from": 0})
    if pa is not None:
        S.set(id, pa=list(pa), pb=list(pb))
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


def poly_path(pts):
    """Fonction p (0-1) -> point d'une polyligne parcourue à vitesse constante (S.path)."""
    acc = [0.0]
    for a, b in zip(pts, pts[1:]):
        acc.append(acc[-1] + math.dist(a, b))
    L = acc[-1]

    def at(p):
        s = max(0.0, min(1.0, p)) * L
        i = next((j for j in range(1, len(acc)) if acc[j] >= s - 1e-9), len(acc) - 1)
        t = (s - acc[i - 1]) / max(1e-9, acc[i] - acc[i - 1])
        a, b = pts[i - 1], pts[i]
        return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t]
    return at


def bez(a, c, b):
    return lambda p: [(1 - p) ** 2 * a[0] + 2 * (1 - p) * p * c[0] + p * p * b[0],
                      (1 - p) ** 2 * a[1] + 2 * (1 - p) * p * c[1] + p * p * b[1]]


def bez3(a, c1, c2, b):
    return lambda p: [(1 - p) ** 3 * a[k] + 3 * (1 - p) ** 2 * p * c1[k] + 3 * (1 - p) * p * p * c2[k] + p ** 3 * b[k]
                      for k in range(2)]


def past_src_id(src):
    """Entité d'où sort une pastille : -1 = la pilule du solde, 6 = le jeton, sinon la case nommée."""
    return "solde" if src == -1 else "jeton" if src == 6 else CASE_IDS[src]


def grid_mode(kit, f, small, d):
    """La grille change de taille : en réduite, les libellés des cases s'effacent (illisibles à ×0,65) et les
    pictogrammes passent au centre à ×1,4 ; en pleine, l'inverse. Mêmes images que le déplacement de la grille."""
    S = kit.S
    for i in range(1, 9):
        cid, icon = CASE_IDS[i], CASES[i][2]
        if icon:
            kit.move(f"{cid}_ico", f, list(ICO_SMALL_LOCAL if small else CELL_ICO_LOCAL), d=d,
                     scale=ICO_SMALL_K if small else 1)
        if small:
            S.key(f"{cid}_mot", "opacity", f, 0, 6, "linear")
        else:
            S.key(f"{cid}_mot", "opacity", f + d - 6, 1, 6, "linear")
    kit.move("case_societe_pct", f, list(PCT_SMALL_LOCAL if small else PCT_LOCAL), d=d,
             scale=ICO_SMALL_K if small else 1)
    for cid in ("compte_ico", "compte_mot"):
        if small:
            S.key(cid, "opacity", f, 0, 6, "linear")
        else:
            S.key(cid, "opacity", f + d - 6, 1, 6, "linear")


def move_with_grid(kit, f, small, d=None, e="inOut", extra=()):
    """Déplace la grille vers GRILLE_SMALL (small=True) ou GRILLE_FULL, et la pilule du solde avec la même clé
    (centrée et élargie dans la case réduite). `extra` : [(id, point monde, échelle)] à déplacer dans les mêmes
    images."""
    from pipeline.story import MOVE
    d = d or MOVE
    c, k = (GRILLE_SMALL, GRILLE_SMALL_K) if small else (GRILLE_FULL, GRILLE_FULL_K)
    kit.move("grille", f, list(c), d=d, e=e, scale=k)
    kit.move("solde", f, list(SOLDE_CELL_SMALL if small else SOLDE_CELL_FULL), d=d, e=e,
             scale=SOLDE_SMALL_K if small else SOLDE_CELL_K)
    kit.S.key("solde", "w", f, SOLDE_SMALL_W if small else SOLDE_W, d, e)
    grid_mode(kit, f, small, d)
    for id, pt, sc in extra:
        kit.move(id, f, list(pt), d=d, e=e, scale=sc)
    return f + d


# ---------- raccords (contrat des parties ; couleurs en hex minuscule : S.val rend du minuscule) ----------
def _lo(c):
    return c.lower()


_OFF = lambda *ids: {i: {"scale": 0} for i in ids}   # noqa: E731

ENTRY_P2 = {   # fin de S08 = etat_initial de S09 (image 986)
    "grille": {"pos": list(GRILLE_FULL), "scale": GRILLE_FULL_K},
    "compte": {"pos": list(CELL_LOCAL[0]), "scale": 1, "w": CELL_W, "h": CELL_H, "fill": _lo(PAPER),
               "stroke": _lo(INK)},
    "compte_mot": {"pos": list(COMPTE_MOT_CELL), "scale": COMPTE_MOT_CELL_K, "text": T_COMPTES,
                   "chars": len(T_COMPTES)},
    "compte_ico": {"pos": list(COMPTE_ICO_CELL), "scale": COMPTE_ICO_CELL_K},
    "compte_filet": {"scale": 0},
    "solde": {"pos": list(SOLDE_CELL_FULL), "scale": SOLDE_CELL_K, "text": T_SOLDE_VAL, "textOp": 1, "w": SOLDE_W},
    **{CASE_IDS[i]: {"pos": list(CELL_LOCAL[i]), "scale": 1} for i in range(1, 6)},
    **{f"{CASE_IDS[i]}_mot": {"chars": len(CASES[i][1].replace("\n", ""))} for i in range(1, 6)},
    **{Q_IDS[i]: {"pos": list(CELL_LOCAL[i]), "scale": 0} for i in range(1, 6)},
    **{Q_IDS[i]: {"pos": list(CELL_LOCAL[i]), "scale": 1} for i in range(6, 9)},
    **{CASE_IDS[i]: {"pos": list(CELL_LOCAL[i]), "scale": 0} for i in range(6, 9)},
    "marqueur": {"pos": [MARKER_CX, MARKER_Y], "scale": 1, "on": 1, "active": 0, "done0": 0, "done1": 0, "done2": 0},
    "regard": {"draw": 0, "from": 0},
    "net_trait": {"draw": 0},
    **_OFF("dettes", "net", "entete", "cadre", "moins", "egal", "cible", "depart", "fleche_pointe", "strategie",
           "question", "jeton", "etiquette", "barre", "brut", "resultat", "alerte", "graphe_freq",
           *[f"lbl_{i}" for i in range(6)]),
    "fil_grille": {"draw": 0, "from": 0}, "fil_dettes": {"draw": 0, "from": 0}, "fleche": {"draw": 0, "from": 0},
}

ENTRY_P3 = {   # fin de S15 = etat_initial de S16 (image 1915)
    "grille": {"pos": list(GRILLE_SMALL), "scale": GRILLE_SMALL_K},
    "compte": {"pos": list(CELL_LOCAL[0]), "scale": 1, "w": CELL_W, "h": CELL_H, "fill": _lo(PAPER),
               "stroke": _lo(INK)},
    "compte_mot": {"text": T_COMPTES},
    "solde": {"pos": list(SOLDE_CELL_SMALL), "scale": SOLDE_SMALL_K, "text": T_SOLDE_VAL, "w": SOLDE_SMALL_W},
    **{CASE_IDS[i]: {"pos": list(CELL_LOCAL[i]), "scale": 1} for i in range(1, 9)},
    **{Q_IDS[i]: {"scale": 0} for i in range(1, 9)},
    "case_immo_place": {"scale": 1},
    "marqueur": {"pos": [MARKER_CX, MARKER_Y], "scale": 1, "on": 1, "active": 1, "done0": 1, "done1": 0, "done2": 0},
    "jeton": {"pos": list(JETON_P2), "scale": JETON_P2_K},
    "etiquette": {"pos": list(ETIQ_P2), "scale": 1},
    "etiq_achat": {"opacity": 0}, "etiq_valeur": {"chars": len(T_VALEUR)}, "etiq_montant": {"scale": 1},
    "etiq_date": {"scale": 0},
    "ficelle": {"draw": 0}, "ficelle_jeton": {"draw": 1},
    "barre": {"pos": list(BARRE_SHORT_C), "scale": 1, "w": BARRE_SHORT_W},
    "resultat": {"pos": list(RESULTAT_C), "scale": 1},
    "calc_a": {"chars": len(T_CALC_A)}, "calc_b": {"chars": len(T_CALC_B)},
    "dettes": {"scale": 0},
    **_OFF("net", "entete", "cadre", "moins", "egal", "cible", "depart", "fleche_pointe", "strategie", "question",
           "alerte", "accolade", "restant", "graphe_freq"),
    "brut": {"opacity": 0}, "mensualite": {"scale": 0}, "mensualite_mot": {"opacity": 0},
    "regard": {"draw": 0, "from": 0}, "net_trait": {"draw": 0},
}


def cast(S, kit):
    """Toute la distribution, à son état de l'image 0. Ce qui arrive plus tard : scale=0 (ou draw=0, chars=0,
    opacity=0). Seuls `fin` et son curseur naissent dans kit.outro (p3)."""

    # --- la grille (groupe invisible) : pleine à l'image 0 (ses enfants sont cachés, sauf la carte « Solde ») ---
    kit.shape("grille", list(GRILLE_FULL), kind="rect", w=1, h=1, fill="none", stroke="none", sw=0, shadow=0, z=6)
    for i in range(1, 9):
        key, label, icon, size = CASES[i]
        kit.shape(Q_IDS[i], list(CELL_LOCAL[0]), kind="round", w=CELL_W, h=CELL_H, r=CELL_R, fill="none", stroke=INK,
                  sw=3, shadow=0, dash=[12, 9], z=6.2, parent="grille", scale=0)
        kit.text(f"{Q_IDS[i]}_mot", [0, 4], T_Q, size=80, weight=800, z=6.25, parent=Q_IDS[i])
        cid = CASE_IDS[i]
        kit.shape(cid, list(CELL_LOCAL[i]), kind="round", w=CELL_W, h=CELL_H, r=CELL_R, fill=PAPER, stroke=INK, sw=4,
                  shadow=6, z=6.4, parent="grille", scale=0)
        S.set(cid, stroke=INK)                  # hex : contour qui s'allume en deep quand une pastille en sort (S17)
        if icon:
            kit.icon(f"{cid}_ico", list(CELL_ICO_LOCAL), icon, disc=CELL_DISC_R, fill=LIGHT, color=INK, shadow=3,
                     z=6.45, parent=cid)
        two = "\n" in label
        kit.text(f"{cid}_mot", list(CELL_MOT2_LOCAL if two else CELL_MOT_LOCAL), label, size=size, weight=700,
                 z=6.5, parent=cid, typed=True)
    kit.icon("case_societe_pct", list(PCT_LOCAL), "percent", disc=PCT_R, fill=LIGHT, color=INK, shadow=2, z=6.47,
             parent="case_societe")
    kit.shape("case_immo_place", list(IMMO_PLACE_LOCAL), kind="circle", w=IMMO_PLACE_W, fill="none", stroke=INK, sw=3,
              shadow=0, dash=[10, 8], z=6.45, parent="case_immo", scale=0)

    # --- la carte « Solde » (enfant de la grille ; devient la case « Comptes ») ---
    kit.shape("compte", list(COMPTE_LOCAL0), kind="round", w=COMPTE_W0, h=COMPTE_H0, r=18, fill=PAPER, stroke=INK,
              sw=4, shadow=6, z=6.6, parent="grille")
    S.set("compte", w=COMPTE_W0, h=COMPTE_H0, fill=PAPER, stroke=INK)
    kit.icon("compte_ico", list(COMPTE_ICO0), "bank", s=COMPTE_ICO_S0, color=INK, z=6.7, parent="compte")
    kit.text("compte_mot", list(COMPTE_MOT0), T_SOLDE, size=COMPTE_MOT_S0, weight=700, anchor="start", z=6.7,
             parent="compte")
    S.set("compte_mot", text=T_SOLDE, chars=len(T_SOLDE))
    kit.shape("compte_filet", list(COMPTE_FILET0), kind="rect", w=COMPTE_FILET_W0, h=3, fill=RULE, stroke="none",
              sw=0, shadow=0, z=6.7, parent="compte")

    # --- la pilule du fil « 3 200 € » (monde) ---
    pill(S, "solde", SOLDE_C0, T_SOLDE_VAL, size=SOLDE_SIZE, weight=800, fill=CYAN, h=SOLDE_H, w=SOLDE_W, z=8,
         scale=1, shadow=6)
    S.set("solde", rot=0)

    # --- S08 : les pilules-libellés que le stylo émet (une par mot de la liste) ---
    for i, t in enumerate(LBL_TEXTS):
        pill(S, f"lbl_{i}", TAP_GRILLE, t, size=32, fill=LIGHT, h=52, z=16.5, scale=0, shadow=3, sw=3)

    # --- « Toi » (encre, visible dès l'image 0 en P1), son nom, son regard, son « ? » ---
    toi = Figure(kit, "toi", pos=TOI_P1, variant="ink", side="left", show=True)
    toi.low_rot = LOW_ROT_V13                   # stylo baissé plus à plat : la pointe reste au-dessus des sous-titres
    pill(S, "nom_toi", NOM_ABOVE, T_TOI, size=34, fill=LIGHT, h=NOM_H, w=NOM_W, z=15.8, parent="toi", scale=1,
         sw=3)
    wire(S, "regard", 14, INK, 4, pa=REGARD_EYE, pb=REGARD_CARTE, dash=[12, 10])
    S.set("regard", color=INK)                  # hex : INK -> RED (S20 « solde. »)
    line(kit, "regard_barre", REGARD_BARRE, color=INK, sw=6, z=14.2)
    # S21 « dois. » : le nouveau regard part en tirets encre (même grammaire que S01 / S20) puis devient plein deep
    wire(S, "regard_net", 14, INK, 6, pa=REGARD_NET[0], pb=REGARD_NET[1], dashAlt=[14, 10])
    S.set("regard_net", color=INK, dashed=1)
    # S18 : le regard de « Toi » vers les deux pastilles gardées (tirets deep), l'une après l'autre
    wire(S, "regard_garde", 14, DEEP, 4, pa=REGARD_GARDE_EYE, pb=REGARD_GARDE_EYE, dash=[12, 10])
    S.add("question", "qmark", z=17)
    S.set("question", pos=list(QUESTION_C), scale=0, opacity=1, gs=Q_GS)

    # --- l'équation : en-tête, cadre, signes, carte grise, « Patrimoine net », fils ---
    kit.text("entete", list(ENTETE_C), T_ENTETE, size=36, weight=700, z=9, typed=True)
    S.set("entete", under=0)
    kit.shape("cadre", list(CADRE_C), kind="round", w=CADRE_W, h=CADRE_H, r=22, fill="none", stroke=DEEP, sw=5,
              shadow=0, z=7, draw=0)
    kit.text("moins", list(MOINS_C), T_MOINS, size=SIGNE_SIZE, weight=800, z=9, scale=0)
    kit.text("egal", list(EGAL_C), T_EGAL, size=SIGNE_SIZE, weight=800, z=9, scale=0)
    kit.shape("dettes", list(DETTES_C), kind="round", w=DETTES_W, h=DETTES_H, r=16, fill=GREY, stroke=INK, sw=4,
              shadow=6, z=10.5, scale=0)
    S.set("dettes", w=DETTES_W, h=DETTES_H, stroke=INK)
    kit.icon("dettes_ico", list(DETTES_ICO_CARD), "bank", s=DETTES_ICO_S, color=INK, z=10.6, parent="dettes")
    kit.text("dettes_mot", list(DETTES_MOT_CARD), T_DOIS_CARTE, size=34, weight=700, anchor="start", z=10.6,
             parent="dettes")
    S.set("dettes_mot", text=T_DOIS_CARTE)
    kit.text("dettes_val", [15, 30], T_180, size=40, weight=800, z=10.6, parent="dettes", scale=0)
    # S13 : 11 traits = 12 tranches de la part grise (tracés de gauche à droite) ; la tranche de droite = une mensualité
    for k in range(1, N_TRANCHES):
        x = round(-GRISE_W / 2 + k * TRANCHE_W, 1)
        line(kit, f"tranche{k}", [[x, -44], [x, 44]], color=SLICE, sw=3, z=10.55, parent="dettes")
    kit.shape("mensualite", list(MENS_LOCAL), kind="rect", w=round(TRANCHE_W, 1), h=BARRE_H, fill=RED, stroke=INK,
              sw=3, shadow=0, z=10.62, parent="dettes", scale=0)
    pill(S, "net", NET_C, T_NET, size=NET_SIZE, weight=800, fill=LIGHT, h=NET_H, w=NET_W, z=11, shadow=6)
    line(kit, "net_trait", NET_TRAIT_LOCAL, color=DEEP, sw=5, z=11.1, parent="net")
    line(kit, "net_fente", FENTE_PTS, color=INK, sw=3, z=11.15, parent="net")   # S16 : la fente « un chiffre, des
    wire(S, "fil_grille", 7.5, DEEP, 5, a={"id": "cadre", "at": list(FIL_GRILLE_A)},          # choses différentes »
         b={"id": "net", "at": list(FIL_NET_A)})
    wire(S, "fil_dettes", 7.5, DEEP, 5, a={"id": "dettes", "at": list(FIL_DETTES_A)},
         b={"id": "net", "at": list(FIL_NET_B)})
    wire(S, "fil_net", 7.5, DEEP, 5, a={"id": "cadre", "at": list(FIL_P3_CADRE)},
         b={"id": "net", "at": list(FIL_P3_NET)})

    # --- la cible de la stratégie (S05) : ombre de contact retirée (elle se décalait sous la flèche) ---
    png(S, "cible", "TARGET", CIBLE_W, CIBLE_C, z=5, contact=False, shadow=0)
    kit.shape("cible_onde", list(CIBLE_C), kind="circle", w=120, fill="none", stroke=DEEP, sw=6, shadow=0, z=5.2,
              opacity=0)
    kit.shape("depart", list(DEPART_C), kind="circle", w=2 * DEPART_R, fill=CYAN, stroke=INK, sw=3, shadow=0, z=11.3,
              scale=0)
    wire(S, "fleche", 11.2, DEEP, 6, pa=DEPART_C, pb=FLECHE_B)
    head(kit, "fleche_pointe", FLECHE_B, FLECHE_ROT, color=DEEP, z=11.25, s=1.2)
    kit.text("strategie", list(STRATEGIE_C), T_STRATEGIE, size=34, weight=700, color=DEEP, z=9, typed=True)

    # --- le repère 1-2-3 (S06 -> S22) ---
    kit.steps_marker(MARKER_LABELS, id="marqueur", y=MARKER_Y, cx=MARKER_CX, gap=MARKER_GAP, z=20)
    S.ents["marqueur"]["p"].update(labelSize=MARKER_LABEL, moveBlank=True, doneStyle="kept")
    S.set("marqueur", scale=0, on=0, done0=0, done1=0, done2=0, lbl=1)
    kit.text("marqueur_leg3", list(MARKER_LEGENDS[2]), T_LIMITES, size=MARKER_LABEL, weight=700, z=20.5, opacity=0)
    S.set("marqueur_leg3", mark=0)
    kit.icon("marqueur_fait3", list(MARKER_DISCS[2]), "check", disc=32, fill=LIGHT, color=DEEP, shadow=6, z=20.6,
             scale=0)
    kit.shape("disque2_onde", list(DISQUE2), kind="circle", w=72, fill="none", stroke=DEEP, sw=6, shadow=0, z=20.7,
              opacity=0)                        # S11, S15 : le disque 2 « Dois » émet / reçoit la carte grise

    # --- le jeton-maison (TOKEN.png, monde) et l'étiquette de prix ---
    tok = png(S, "jeton", "TOKEN", JETON_W, JETON_CELL, z=9)
    jeton_bottom = (0, round(tok["h_disp"] / 2))
    kit.shape("etiquette", list(ETIQ_S10), kind="poly", pts=ETIQ_PTS, fill=PAPER, stroke=INK, sw=4, shadow=6, z=9.5,
              scale=0)
    kit.shape("etiq_oeillet", list(OEILLET_LOCAL), kind="circle", w=2 * OEILLET_R, fill=PAPER, stroke=INK, sw=4,
              shadow=0, z=9.6, parent="etiquette")
    kit.text("etiq_achat", list(ACHAT_LOCAL), T_PRIX_ACHAT, size=ACHAT_SIZE, weight=700, color=RED, z=9.6,
             parent="etiquette")
    line(kit, "etiq_achat_barre", [[_W_ACHAT / 2 + 3, 0], [-_W_ACHAT / 2 - 3, 0]], color=INK, sw=7, z=9.7,
         parent="etiq_achat")
    kit.text("etiq_valeur", list(VALEUR_LOCAL), T_VALEUR, size=VALEUR_SIZE, weight=700, color=DEEP, z=9.6,
             parent="etiquette", typed=True)
    pill(S, "etiq_date", DATE_LOCAL, T_AN_ACHAT, size=32, fill=PAPER, h=DATE_H, z=9.65, parent="etiquette",
         scale=1, shadow=0, sw=3, icon="cal")   # S10 : « 2015 » -> « aujourd’hui » (piste text, w, fill)
    S.set("etiq_date", fill=PAPER)
    kit.text("etiq_montant", list(MONTANT_LOCAL), T_250, size=MONTANT_SIZE, weight=800, z=9.6, parent="etiquette",
             scale=0)
    wire(S, "ficelle", 9.4, DEEP, 3, a={"id": "case_immo", "at": list(FICELLE_CASE_A)},
         b={"id": "etiquette", "at": list(OEILLET_LOCAL)})
    wire(S, "ficelle_jeton", 9.4, DEEP, 3, a={"id": "jeton", "at": list(jeton_bottom)},
         b={"id": "etiquette", "at": list(OEILLET_LOCAL)})
    line(kit, "temps", [TEMPS_A, TEMPS_B], color=DEEP, sw=5, z=9.3)   # S10 : flèche du temps (passé -> aujourd'hui)
    head(kit, "temps_pointe", (TEMPS_B[0] + 6, TEMPS_B[1]), 0, color=DEEP, z=9.35)

    # --- la barre de l'appartement, son accolade, la part grise, « 250 000 € » rouge, le résultat ---
    kit.shape("barre", list(BARRE_C), kind="round", w=BARRE_W, h=BARRE_H, r=14, fill=CYAN, stroke=INK, sw=5,
              shadow=6, z=9.3, scale=0)         # sous l'étiquette : elle naît du bas du jeton et passe derrière
    S.set("barre", w=BARRE_W)
    kit.icon("barre_maison", list(MAISON_C), "house", s=50, color=INK, z=9.35, scale=0)
    kit.shape("crochet", list(CROCHET_C), kind="poly", pts=CROCHET_PTS, closed=False, fill="none", stroke=DEEP,
              sw=5, shadow=0, z=11, draw=0)
    wire(S, "crochet_fil", 9.45, DEEP, 3, pa=CROCHET_FIL[0], pb=CROCHET_FIL[1])
    kit.text("crochet_val", list(CROCHET_VAL), T_250, size=40, weight=800, color=DEEP, z=11, scale=0)
    kit.shape("fantome", list(GRISE_GAP_C), kind="round", w=GRISE_W, h=BARRE_H, r=14, fill="none", stroke=INK, sw=3,
              shadow=0, dash=[12, 9], z=9.2, draw=0)   # S15 : la place de la part grise retirée
    wire(S, "fil_banque", 10.4, DEEP, 4, pa=(GRISE_GAP_C[0] - 165, 1018), pb=(DISQUE2[0], DISQUE2[1] + 84))
    S.set("fil_banque", via=list(FIL_BANQUE_VIA))
    wire(S, "trace_dettes", 9.0, DEEP, 4, pa=GRISE_GAP_C, pb=(DISQUE2[0], DISQUE2[1] + 84), dash=[10, 10])
    S.set("trace_dettes", via=list(FIL_BANQUE_VIA))
    kit.text("mensualite_mot", list(MENS_MOT), T_MENSUALITE, size=34, weight=700, color=RED, anchor="start", z=10.8,
             typed=True)
    kit.icon("mensualite_cal", list(MENS_CAL), "cal", s=34, color=RED, z=10.8, scale=0)
    line(kit, "mensualite_barre", [[_W_MENS + 4, 0], [-4, 0]], color=INK, sw=7, z=10.9, parent="mensualite_mot")
    kit.shape("accolade", list(ACCOLADE_C), kind="poly", pts=ACCOLADE_PTS, closed=False, fill="none", stroke=DEEP,
              sw=5, shadow=0, z=11, draw=0)
    kit.text("restant", list(RESTANT_C), T_RESTANT, size=34, weight=700, color=DEEP, z=11, typed=True)
    pill(S, "brut", BRUT_C, T_250, size=BRUT_SIZE, weight=800, fill=PAPER, h=BRUT_H, w=BRUT_W, z=9.25, color=RED,
         stroke=RED, sw=5)                      # sous la barre : il en sort par le bas (S15)
    line(kit, "brut_barre", [[_W_BRUT / 2 + 3, -2], [-_W_BRUT / 2 - 3, -2]], color=INK, sw=7, z=12.1, parent="brut")
    pill(S, "resultat", RESULTAT_C, T_RESULTAT, size=44, weight=800, fill=LIGHT, h=RESULTAT_H, w=RESULTAT_W, z=12,
         shadow=6)
    kit.text("calc_a", [CALC_X, CALC_Y], T_CALC_A, size=CALC_SIZE, weight=700, anchor="start", z=12, typed=True)
    kit.text("calc_b", [round(CALC_X + text_width(T_CALC_A, CALC_SIZE, 700), 1), CALC_Y], T_CALC_B, size=CALC_SIZE,
             weight=700, color=DEEP, anchor="start", z=12, typed=True)

    # --- point 3 : signe d'attention, pastilles, graphe ---
    kit.icon("alerte", list(ALERTE_C), "warning", disc=ALERTE_R, fill=PAPER, color=INK, shadow=4, z=11.5, scale=0)
    for pid, (mot, icon, place, src, dashed) in PASTILLES.items():
        kit.shape(pid, list(place), kind="round", w=PAST_W, h=PAST_H, r=PAST_H / 2, fill=PAPER, stroke=INK, sw=4,
                  shadow=0 if dashed else 4, z=12, scale=0, **({"dash": [14, 9]} if dashed else {}))
        if icon:
            kit.icon(f"{pid}_ico", list(PAST_ICO_LOCAL), icon, disc=PAST_DISC, s=40, fill=LIGHT, color=INK, shadow=0,
                     z=12.1, parent=pid)            # pictogramme 40 px sur un disque de 52 px : le sujet de la pastille
        else:                                   # « estimé » : « ≈ » ExtraBold dans un disque en tirets
            kit.shape(f"{pid}_ico", list(PAST_ICO_LOCAL), kind="circle", w=2 * PAST_DISC, fill=LIGHT, stroke=INK,
                      sw=3, shadow=0, dash=[6, 5], z=12.1, parent=pid)
            kit.text(f"{pid}_approx", [0, 1], "≈", size=34, weight=800, z=12.15, parent=f"{pid}_ico")
        kit.text(f"{pid}_mot", list(PAST_MOT_LOCAL), mot, size=PAST_SIZE, weight=700, anchor="start", z=12.1,
                 parent=pid)
        S.set(f"{pid}_mot", under=0)
        wire(S, f"lien_{pid}", 11.9, DEEP, 3, a={"id": past_src_id(src), "at": [0, 0]}, b={"id": pid, "at": [0, 0]},
             dash=[8, 8])               # attache pointillée : la case d'origine -> la pastille (S17)
    for k, y in enumerate(PAST_ROWS):
        kit.text(f"paire{k + 1}", [PAIRE_X, y + 2], T_PAIRE, size=40, weight=800, color=DEEP, z=12, scale=0)
    for pid in PAST_GARDE:
        kit.icon(f"oeil_{pid}", list(OEIL_LOCAL), "eye", disc=OEIL_R, fill=LIGHT, color=DEEP, shadow=0, z=12.2,
                 parent=pid, scale=0)
    line(kit, "axes", AXE_PTS, color=INK, sw=4, z=9)
    head(kit, "axe_y_pointe", AXE_Y_TIP, -90, color=INK, z=9.05)
    head(kit, "axe_x_pointe", AXE_X_TIP, 0, color=INK, z=9.05)
    kit.text("axe_y_mot", list(AXE_Y_MOT), T_AXE_Y, size=32, weight=700, anchor="start", z=9, opacity=0)
    kit.text("axe_auj", list(AUJ_C), T_AUJ, size=32, weight=700, z=9, opacity=0)
    for k, (x, t) in enumerate(zip(GRAD_XS, T_ANS)):
        kit.shape(f"grad{k + 1}", [x, 1180], kind="rect", w=4, h=14, fill=INK, stroke="none", sw=0, shadow=0, z=9,
                  opacity=0)
        kit.text(f"grad{k + 1}_mot", [x, GRAD_Y], t, size=32, weight=700, z=9, opacity=0)
    for k, p in enumerate(POINTS):
        kit.shape(f"point{k + 1}", list(p), kind="circle", w=2 * POINT_R, fill=CYAN, stroke=INK, sw=3, shadow=0,
                  z=9.6, scale=0)
    kit.curve("courbe", [0, 0], [list(p) for p in POINTS], draw=0, color=DEEP, sw=6, dot=False, smooth=True, z=9.4)
    pill(S, "graphe_freq", FREQ_C, T_FREQ, size=34, fill=LIGHT, h=FREQ_H, w=FREQ_W, z=11, icon="cal")
    kit.shape("axe_onde", list(AXE_TAP), kind="circle", w=60, fill="none", stroke=DEEP, sw=5, shadow=0, z=9.2,
              opacity=0)
    line(kit, "ecart_h", ECART_H, color=DEEP, sw=3, z=9.3)
    line(kit, "ecart_v", ECART_V, color=DEEP, sw=4, z=9.3)
    head(kit, "ecart_haut", ECART_V[1], -90, color=DEEP, z=9.35, s=0.8)
    head(kit, "ecart_bas", ECART_V[0], 90, color=DEEP, z=9.35, s=0.8)

    # --- légendes de l'équation finale (S21) ---
    for lid, txt, c in (("leg_possedes", T_POSSEDES, LEG_POSSEDES), ("leg_dois", T_DOIS, LEG_DOIS),
                        ("leg_limites", T_LIMITES, LEG_LIMITES)):
        kit.text(lid, list(c), txt, size=36, weight=700, z=11, typed=True)
        S.set(lid, under=0)

    # --- la fin : toucher au doigt (le curseur de kit.outro reste invisible) ---
    kit.shape("fin_doigt", list(FIN_TAP), kind="circle", w=44, fill=INK, stroke=PAPER, sw=4, shadow=0, z=42, scale=0)
    for k in range(2):
        kit.shape(f"fin_onde{k + 1}", list(FIN_TAP), kind="circle", w=70, fill="none", stroke=DEEP, sw=6, shadow=0,
                  z=41.9, opacity=0)

    return SimpleNamespace(toi=toi, tok=tok, jeton_bottom=jeton_bottom)


def build(S):
    kit = Kit(S)
    c = cast(S, kit)
    only = [p for p in os.environ.get("WTH_PARTS", "").split(",") if p]   # WTH_PARTS=p2 : cette partie seule
    for name in PARTS:
        if not only or name in only:
            importlib.import_module(f".{name}", __name__).part(S, kit, c)
