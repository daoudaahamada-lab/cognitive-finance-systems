"""V13 « Ton patrimoine net n’est pas ton solde » : mise en scène Story, en paquet (une partie par fichier).

Storyboard : scripts/storyboards/V13.json (v1, révisé après le test sans son, 22 scènes, 112 temps forts, 92,272 s),
version lisible scripts/storyboards/V13.md. Voix : build/V13/words.json (film : images 0-2767, FILM_END = 2768).
Fil : la pilule cyan « 3 200 € » (`solde`, pill 320 x 100, ExtraBold 60) : sur la carte « Solde » dès l'image 0,
regardée par « Toi » (S01) ; réduite avec sa carte en première case d'une grille de neuf (S02) ; dans sa case pendant
tout le calcul (S03-S19) ; sort vers « Toi », regard rouge barré, rentre (S20-S21) ; devient le bouton « S’abonner »
(S22). Jamais d'autre chiffre.
Parti pris : « le puzzle de ton patrimoine » : une grille de neuf cases (`grille`) = ce que tu possèdes ; la carte grise
« Ce que tu dois » (`dettes`) = la part de la banque ; la pilule « Patrimoine net » (`net`) = le résultat.
Pas d'IA dans ce film : « Toi » (figurine encre) est seul à tenir le stylo. Aucune coche d'IA, aucun pointillé d'IA.

Parties (scènes contiguës ; poids : temps forts et secondes) :
- p1 : S01-S08, images 0-986 (40 temps forts, 32,9 s). Accroche (solde, grille de « ? »), équation, cible, repère
  1-2-3, point 1 : six cases nommées.
- p2 : S09-S15, images 987-1915 (36 temps forts, 31,0 s). Fin du point 1 (immobilier, véhicule, parts, étiquette
  « Valeur actuelle ») ; point 2 : barre de l'appartement, part grise, mensualité, 250 000 € / 180 000 €, ≈ 70 000 €.
- p3 : S16-S22, images 1916-2767 (36 temps forts, 28,4 s). Point 3 (limites, six pastilles, courbe), chute, fin.
ENTRY_P2 et ENTRY_P3 sont le contrat des raccords (kit.pin(f0 - 1, …)). Les figurines n'y sont jamais.

Entités nouvelles : AUCUN nouveau type. Seul ajout au code partagé : le pictogramme `car` (voiture) dans `Icon`
(motion/src/story/draw.tsx : IconName, ICON_NAMES, switch), un nom de plus (opt-in, aucun dessin existant ne change) ;
déclaré ici sur la case « Véhicule » (`case_vehicule_ico`) : tant qu'il n'est pas dessiné, le disque est vide (un nom
inconnu ne dessine rien, sans erreur). À ajouter par l'auteur de p2 (S09), puis `make story-check`.
Compositions (catalogue) :
- grille = groupe invisible (shape rect 1 x 1 sans trait) : ses enfants (carte « Solde » / case « Comptes », 8 cases
  « ? », 8 cases nommées) suivent ses deux places : GRILLE_FULL (×1) et GRILLE_SMALL (×0,6) ; un seul kit.move.
- la pilule du solde, le jeton, l'étiquette, les pastilles restent des entités MONDE (elles quittent la grille) : quand
  la grille bouge, les déplacer avec la même clé (même f, d, e) vers grid_world(...) : le raccord est exact.
- étiquette de prix = shape poly (pentagone) + œillet (circle) + textes enfants + compteur + ficelles (wire).
- part grise = la carte `dettes` elle-même (pistes w, h) : même carte de S04 à S21.
- regards : `regard` (wire en tirets, pistes pa / pb / color en hex : encre -> rouge) ; `regard_net` (wire plein deep).
- traits barrés : shape poly ouverte (piste draw) passée à Figure.strike(line=…, track="draw").
- pastilles = capsules (shape round + icon disc + text, piste under) ; graphe = shape poly + shape circle + curve.
- toucher de fin : `fin_doigt` + `fin_onde1-2` (comme V12) ; le curseur de kit.outro est rendu invisible.

ÉCARTS DE PLACE (raisons de mise en page ou d'allonge du bras, aucun sens changé) :
- P2 = (590, 1135) et non (700, 1135) (S03 et S13) : souligner « Patrimoine net » et barrer « Mensualité » ne sont
  pas à portée depuis x 700 (bras côté gauche : la cible doit rester à gauche de l'épaule) ; la pilule « Patrimoine
  net » naît sous la pointe en (500, 955) (et non (560, 955), qui est à l'aplomb de l'épaule) ;
- S03 : la pointe trace le soulignement de (350, 960) à (510, 960) ; le trait (`net_trait`, 350 -> 730) file seul
  ensuite jusqu'au bout (précédent V12 S17) : 380 px en un seul geste sont hors d'allonge ;
- étiquette en S10 : centre (329, 1110) (et non (300, 1110)), « Prix d’achat » et « Valeur actuelle » en Bold 32 (et
  non 34) : le trait qui barre (270 -> 463, y 1092) tient dans l'allonge depuis P3 (560) sans heurter le corps ;
- « 250 000 € » rouge (S15) : pilule 244 x 80, ExtraBold 38, en (657, 1100) (et non (600, 1060), 44) : barrée depuis
  P1 sans marcher (trait 758 -> 556, y 1098 : toute la bande d'allonge sûre de P1 à cette hauteur) ; « ≈ 70 000 € nets » garde sa place (330, 1060) ;
- « 1 ou 2 fois / an » (S19) en (575, 860) et non (440, 860) : à (440, 860) la pilule couvrait la légende d'axe
  « Patrimoine net » (x 140-353, y 820-850).
"""
import importlib
import math
import os
from types import SimpleNamespace

from pipeline.story import GEOM, STYLE, text_width
from pipeline.story_kit import Figure, Kit

PARTS = ["p1", "p2", "p3"]                      # S01-S08, S09-S15, S16-S22
NBSP, NNBSP = " ", " "                # espace insécable (avant « : », « ? », « € »), fine insécable (milliers)
ALERT_WORDS = {"prix", "d’achat", "mensualités"}   # karaoké en rouge : « Prix d’achat » (S10), bord « Mensualité » (S13)
                                                # (« 250 000 € » et « solde » reviennent ailleurs en non-rouge)
ACOUSTIC_SNAP = {"gap": 0.2, "window": 0.08}    # temps fort après un silence : calé sur l'attaque audible

# ---------- couleurs ----------
INK, CYAN, DEEP, LIGHT = STYLE["ink"], STYLE["cyan"], STYLE["deep"], STYLE["light"]
PAPER, RED, RULE, GREY = STYLE["paper"], STYLE["red"], STYLE["rule"], STYLE["grey"]

# ---------- textes à l'écran (typographie française) ----------
T_SOLDE_VAL = f"3{NNBSP}200{NBSP}€"
T_ABONNER = "S’abonner"
T_SOLDE, T_COMPTES, T_TOI = "Solde", "Comptes", "Toi"
T_Q = "?"
T_NET = "Patrimoine net"
T_ENTETE = "Ce que tu possèdes"
T_MOINS, T_EGAL = "−", "="
T_DOIS_CARTE = "Ce que\ntu dois"                # carte grise (deux lignes, ancre start)
T_DOIS_BARRE = "Ce que tu dois"                 # part grise (S11, une ligne centrée)
T_CRD = "Capital restant dû"                    # S12
T_STRATEGIE = "Ta stratégie"
T_PRIX_ACHAT, T_VALEUR = "Prix d’achat", "Valeur actuelle"
T_MENSUALITE = "Mensualité"
T_RESTANT = "restant à rembourser"
T_250 = f"250{NNBSP}000{NBSP}€"
T_RESULTAT = f"≈{NBSP}70{NNBSP}000{NBSP}€ nets"
T_CALC_A = f"250{NNBSP}000{NBSP}€ {T_MOINS} 180{NNBSP}000{NBSP}€ = "   # encre
T_CALC_B = f"70{NNBSP}000{NBSP}€"                                        # deep
T_FREQ = "1 ou 2 fois / an"
T_AXE_Y, T_AUJ = "Patrimoine net", "aujourd’hui"
T_ANS = ["1 an", f"2{NBSP}ans", f"3{NBSP}ans"]
T_POSSEDES, T_DOIS, T_LIMITES = "Possèdes", "Dois", "Limites"
MARKER_LABELS = [T_POSSEDES, T_DOIS, T_LIMITES]
V_250, V_180 = 250000, 180000

# ---------- mise en page (1080 x 1920) ----------
X_MIN, X_MAX, Y_MIN, Y_MAX = 40, 930, 160, 1270  # zone d'action ; on descend jusqu'à y ≈ 1250
GROUND = 1230                                   # pied de « Toi »
FIG_BASE = GEOM["FIGURE"]["base"]               # 95
HEAD_DY = GEOM["FIGURE"]["head"]["cy"]          # -64 : centre de la tête
HEAD_R = GEOM["FIGURE"]["head"]["r"]            # 32
SHOULDER_DX, SHOULDER_DY = abs(GEOM["FIGURE"]["shoulder"][0]), GEOM["FIGURE"]["shoulder"][1]   # 30, -16
REACH_OK = 267                                  # allonge confortable (REACH x 284) à l'échelle 1


def fig_pos(x, feet=GROUND, s=1.0):
    return [x, round(feet - FIG_BASE * s, 2)]


# --- « Toi » : bras côté gauche (il fait face à gauche) ; pied sur y 1230 ---
TOI_P1 = fig_pos(850)                           # (850, 1135) : repos ; épaule (820, 1119) ; haut de la tête 1039
TOI_P2 = fig_pos(590)                           # (590, 1135) : S03 (écrire, souligner), S13 (barrer « Mensualité »)
TOI_P3 = fig_pos(560)                           # (560, 1135) : S09-S10, sous la case « Immobilier »
HEAD_P1 = (850, 1071)
NOM_ABOVE, NOM_RIGHT = (0, -140), (100, -75)    # pilule « Toi » (enfant) : au-dessus de la tête en P1 (850, 995) ;
NOM_W, NOM_H = 100, 56                          # à droite de la tête en P2 / P3 (x + 100, 1060)
QUESTION_C, Q_GS = (735, 975), 90               # « ? » de « Toi » (S01-S02), né de la tête

# --- regard de « Toi » (wire, pistes pa / pb) ---
REGARD_EYE = (815, 1055)                        # S01 ; S20 (815, 1060)
REGARD_CARTE = (610, 795)                       # S01 : bas de la carte « Solde » (local carte (70, 155))
REGARD_CASE = (235, 603)                        # S02 : le même point de la carte devenue case (pb suit avec la même clé)
REGARD_EYE_S20, REGARD_SOLDE_S20 = (815, 1060), (548, 1140)   # S20 : vers le bout droit de la pilule sortie
REGARD_BARRE = ((688, 1070), (712, 1118))       # S21 « C’est » : le stylo coupe le regard près de la tête
REGARD_NET = ((815, 1050), (770, 985))          # S21 « dois. » : regard plein deep vers « Patrimoine net »

# --- la grille 3 x 3 (groupe `grille`) ---
GRILLE_FULL, GRILLE_FULL_K = (461, 706), 1.0    # x 70-852, y 420-992 (S02, S06-S10)
GRILLE_SMALL, GRILLE_SMALL_K = (295, 592), 0.6  # x 60-530, y 420-764 (S03-S05, S11-S21)
CELL_W, CELL_H, CELL_R, CELL_DX, CELL_DY = 250, 180, 16, 266, 196
CELL_LOCAL = [((c - 1) * CELL_DX, (r - 1) * CELL_DY) for r in range(3) for c in range(3)]   # ordre de lecture
# case -> (id, libellé, pictogramme, corps) ; la case 0 est la carte « Solde » (`compte`)
CASES = [None,
         ("livrets", "Livrets", "coin", 34), ("assurance", "Assurance-vie", "shield", 32),
         ("pea", "PEA", "bars", 34), ("epargne", "Épargne\nsalariale", "person", 30),
         ("per", "PER", "hourglass", 34), ("immo", "Immobilier", None, 34),
         ("vehicule", "Véhicule", "car", 34), ("societe", "Parts de\nsociété", "building", 30)]
CASE_IDS = [None] + [f"case_{c[0]}" for c in CASES[1:]]      # cases nommées (scale 0 jusqu'à leur mot)
Q_IDS = [None] + [f"q_{c[0]}" for c in CASES[1:]]            # cases « ? » (scale 0 jusqu'à S02 « presque »)
CELL_ICO_LOCAL, CELL_DISC_R = (0, -30), 32
CELL_MOT_LOCAL, CELL_MOT2_LOCAL = (0, 52), (0, 50)           # libellé une ligne / deux lignes (30 px)
PCT_LOCAL, PCT_R = (28, -6), 14                              # « Parts de société » : petit disque % au coin du bâtiment
IMMO_PLACE_LOCAL, IMMO_PLACE_W = (0, -22), 96                # S11-S16 : cercle en tirets à la place du jeton


def grid_world(local, small=False):
    """Point monde d'un point du repère de la grille (GRILLE_FULL ou GRILLE_SMALL)."""
    c, k = (GRILLE_SMALL, GRILLE_SMALL_K) if small else (GRILLE_FULL, GRILLE_FULL_K)
    return [round(c[0] + local[0] * k, 1), round(c[1] + local[1] * k, 1)]


def cell_world(i, small=False, dy=0):
    """Centre monde de la case i (0-8), décalé de dy (repère de la grille)."""
    return grid_world((CELL_LOCAL[i][0], CELL_LOCAL[i][1] + dy), small)


# --- la carte « Solde » (enfant de la grille ; devient la case « Comptes ») et la pilule du solde (monde) ---
COMPTE_C0, COMPTE_W0, COMPTE_H0 = (540, 640), 440, 300       # S01 : x 320-760, y 490-790
COMPTE_LOCAL0 = (COMPTE_C0[0] - GRILLE_FULL[0], COMPTE_C0[1] - GRILLE_FULL[1])   # (79, -66) dans la grille pleine
COMPTE_ICO0, COMPTE_ICO_S0 = (-160, -95), 40   # pictogramme bank (monde (380, 545))
COMPTE_MOT0, COMPTE_MOT_S0 = (-128, -82), 40   # « Solde » Bold 40, ancre start (monde (412, 558))
COMPTE_FILET0, COMPTE_FILET_W0 = (0, -50), 408  # filet rule en y 590
COMPTE_ICO_CELL, COMPTE_MOT_CELL = (-85, -60), (-60, -48)    # case : bank 30 px, « Solde » / « Comptes » Bold 34
COMPTE_ICO_CELL_K, COMPTE_MOT_CELL_K = 0.75, 0.85             # échelles locales des enfants dans la case (30/40, 34/40)
SOLDE_W, SOLDE_H, SOLDE_SIZE = 320, 100, 60
SOLDE_C0 = (540, 690)                           # S01 (échelle 1)
SOLDE_CELL_DY = 25                              # dans la case : 25 px sous son centre (repère de la grille)
SOLDE_CELL_K = 0.62                             # 198 x 62 dans la grille pleine (x 0,6 dans la grille réduite)
SOLDE_CELL_FULL = tuple(cell_world(0, False, SOLDE_CELL_DY))  # (195, 535)
SOLDE_CELL_SMALL = tuple(cell_world(0, True, SOLDE_CELL_DY))  # (135.4, 489.4), échelle 0.372
SOLDE_OUT, SOLDE_OUT_K = (420, 1140), 0.8       # S20 : sortie vers « Toi » (256 x 80)

# --- l'équation (S03-S05, S20-S21) ---
ENTETE_C = (295, 385)                           # « Ce que tu possèdes » Bold 36 (S04-S06)
CADRE_C, CADRE_W, CADRE_H = (295, 592), 494, 368              # x 48-542, y 408-776 (S04-S06)
MOINS_C, EGAL_C, EGAL_CHUTE = (590, 592), (250, 900), (250, 930)
SIGNE_SIZE = 90
DETTES_C, DETTES_W, DETTES_H = (765, 592), 250, 150           # carte grise x 640-890, y 517-667
DETTES_ICO_CARD, DETTES_ICO_S = (-75, -32), 44                # monde (690, 560)
DETTES_MOT_CARD = (-40, -6)                     # « Ce que / tu dois » Bold 34, ancre start (lignes y 565 et 607)
DISQUE2 = (540, 300)                            # S06, S15 : la carte entre dans le disque 2 du repère ; S11, S20 : en sort
NET_W, NET_H, NET_SIZE = 400, 96, 40
NET_C = (540, 900)                              # S03-S05 ; ×1,15 après « honnête »
NET_PEN = (500, 955)                            # S03 « patrimoine » : née sous la pointe
NET_TRAIT_LOCAL = ((-190, 60), (190, 60))       # soulignement (350 -> 730, y 960), enfant de `net`
NET_PEN_TRACE = ((350, 960), (510, 960))        # la pointe ; le trait file seul jusqu'en 730
NET_P3, NET_P3_K = (735, 500), 0.85             # S16-S19 : 340 x 86
NET_CHUTE, NET_CHUTE_K = (540, 930), 1.2        # S20 (×1) puis S21 (×1,2)
NET_FROM_GRID = (530, 592)                      # S16 : naît du bord droit de la grille réduite
FIL_GRILLE_A, FIL_NET_A = (0, CADRE_H / 2), (-110, -48)       # S05 : bas du cadre -> haut gauche de la pilule
FIL_DETTES_A, FIL_NET_B = (0, DETTES_H / 2), (110, -48)       # S05 : bas de la carte grise -> haut droit
FIL_P3_GRILLE = (CELL_DX + CELL_W / 2, 0)       # S17 : bord droit de la grille (local grille (391, 0) -> (530, 592))
FIL_P3_NET = (-NET_W / 2, 0)                    # -> bout gauche de la pilule (565, 515 à ×0,85)

# --- la cible de la stratégie (S05) ---
CIBLE_C, CIBLE_W = (190, 1110), 180
DEPART_C, DEPART_R = (380, 955), 12             # point de départ cyan au bas gauche de « Patrimoine net »
FLECHE_B = (255, 1035)                          # pointe de la flèche, au bord de la cible
FLECHE_ROT = round(math.degrees(math.atan2(FLECHE_B[1] - DEPART_C[1], FLECHE_B[0] - DEPART_C[0])), 1)
STRATEGIE_C = (190, 1232)

# --- le repère 1-2-3 ---
MARKER_Y, MARKER_CX, MARKER_GAP, MARKER_LABEL = 300, 540, 180, 34   # disques x 360, 540, 720 ; légendes y 362
MARKER_DISCS = [(360, 300), (540, 300), (720, 300)]
MARKER_LEGENDS = [(360, 362), (540, 362), (720, 362)]

# --- le jeton-maison (TOKEN.png, monde) et l'étiquette de prix (S09-S16) ---
JETON_W = 120                                   # largeur déclarée ; échelle = largeur voulue / 120
JETON_CELL = tuple(cell_world(6, False, -22))   # (195, 880) dans la case « Immobilier » (grille pleine)
JETON_P2, JETON_P2_K = (735, 500), round(200 / JETON_W, 4)    # S11-S15 : 200 px (y 400-600)
JETON_SMALL, JETON_SMALL_K = tuple(cell_world(6, True, -22)), 0.6   # S16-S21 : 72 px (135, 696)
ETIQ_W, ETIQ_H = 330, 140
ETIQ_PTS = [[-165, 0], [-115, -70], [165, -70], [165, 70], [-115, 70]]   # pointe à gauche
ETIQ_S10 = (329, 1110)                          # S10 : sous la case « Immobilier » (x 164-494, y 1040-1180)
ETIQ_P2 = (735, 725)                            # S11-S15 : sous le jeton (x 570-900)
OEILLET_LOCAL, OEILLET_R = (-140, 0), 9
ACHAT_LOCAL, ACHAT_SIZE = (38, -18), 32         # « Prix d’achat » rouge (monde S10 (367, 1092), x 275-460)
VALEUR_LOCAL, VALEUR_SIZE = (25, -18), 32       # « Valeur actuelle » deep (x 234-482 en S10)
MONTANT_LOCAL, MONTANT_SIZE = (25, 30), 44      # compteur « 250 000 € » (S14)
ACHAT_STRIKE = ((463, 1092), (270, 1092))       # S10 « valeur » : de droite à gauche, depuis P3
FICELLE_CASE_A = (0, CELL_H / 2)                # bas de la case « Immobilier » (195, 992)

# --- la barre de l'appartement et la part grise (S11-S15) ---
BARRE_C, BARRE_W, BARRE_H = (460, 940), 640, 110              # x 140-780, y 885-995
BARRE_SHORT_C, BARRE_SHORT_W = (229.5, 940), 179              # S15 : x 140-319
GRISE_C, GRISE_W, GRISE_H = (549.5, 940), 461, 110            # part grise x 319-780 (la carte `dettes`)
GRISE_GAP_C = (561.5, 940)                      # S12 « retire » : détachée de 12 px vers la droite
GRISE_ICO, GRISE_ICO_S = (-195, 0), 40          # pictogramme bank (monde (355, 940))
GRISE_MOT, GRISE_MOT2 = (15, 0), (15, -18)      # « Ce que tu dois » (565, 940) ; « Capital restant dû » (565, 922)
GRISE_VAL, GRISE_VAL_SIZE = (15, 30), 40        # compteur « 180 000 € » (565, 970)
GRISE_TAP = (760, 960)                          # S12 « retire », S15 « mais » : depuis P1
MENS_C, MENS_W = (339, 940), 40                 # bord « Mensualité » x 319-359 (contour rouge, sans fond)
MENS_MOT = (320, 1040)                          # « Mensualité » rouge Bold 34, ancre start (x 320-504)
MENS_STRIKE = ((510, 1040), (314, 1040))        # S13 « mais » : depuis P2 (590)
ACCOLADE_C = (550, 866)
ACCOLADE_PTS = [[-231, 14], [-231, 2], [-10, 2], [0, -14], [10, 2], [231, 2], [231, 14]]   # x 319-781, pointe y 852
RESTANT_C = (550, 830)
BRUT_C, BRUT_W, BRUT_H, BRUT_SIZE = (657, 1100), 244, 80, 38  # « 250 000 € » rouge (x 535-779, texte 559-756)
BRUT_FROM = (760, 755)                          # S15 « représente » : se détache du compteur de l'étiquette
BRUT_STRIKE = ((758, 1098), (556, 1098))        # S15 « patrimoine, » : depuis P1 (bande d'allonge 554-760)
RESULTAT_C, RESULTAT_W, RESULTAT_H = (330, 1060), 380, 80     # « ≈ 70 000 € nets » (x 140-520)
CALC_X, CALC_Y, CALC_SIZE = 140, 1170, 36       # « 250 000 € − 180 000 € = » (encre) + « 70 000 € » (deep)

# --- point 3 : signe d'attention, pastilles, graphe (S16-S19) ---
ALERTE_C, ALERTE_R = (885, 455), 26             # coin haut droit de « Patrimoine net » (point 3)
ALERTE_CHUTE, ALERTE_CHUTE_K = (455, 1040), round(22 / 26, 4)  # S21 : devant « Limites »
PAST_W, PAST_H = 280, 66
PAST_ICO_LOCAL, PAST_MOT_LOCAL, PAST_DISC = (-104, 0), (-74, 0), 20
# id -> (mot, pictogramme (None : « ≈ »), place S17, case d'origine (indice de case ; -1 : la pilule du solde ; 6 : jeton))
PASTILLES = {
    "past_disponible": ("disponible", "euro", (250, 860), -1),
    "past_bloque": ("bloqué", "lock", (570, 860), 5),
    "past_sur": ("sûr", "shield", (250, 945), 1),
    "past_risque": ("risqué", "warning", (570, 945), 3),
    "past_estime": ("estimé", None, (570, 1030), 6),
    "past_reel": ("réel", "check", (250, 1030), -1),
}
PAST_GARDE = {"past_disponible": (735, 610), "past_risque": (735, 690)}   # S18 : sous « Patrimoine net »
AXE_PTS = [[120, 830], [120, 1180], [760, 1180]]                # axes en L (monde)
AXE_Y_TIP, AXE_X_TIP = (120, 822), (768, 1180)
AXE_Y_MOT, AUJ_C = (140, 835), (160, 1222)      # « Patrimoine net » (ancre start), « aujourd’hui »
GRAD_XS, GRAD_Y = [320, 480, 640], 1222
POINTS = [(160, 1080), (240, 1062), (320, 1074), (400, 1046), (480, 1058), (560, 1020), (640, 1032), (720, 1000)]
POINT_R = 14
FREQ_C, FREQ_W, FREQ_H = (575, 860), 330, 64    # « 1 ou 2 fois / an » (écart : voir l'en-tête)
ECART_H = [[160, 1080], [755, 1080]]            # trait fin deep 3 px
ECART_V = [[755, 1080], [755, 1000]]            # double flèche deep 4 px
AXE_TAP = (730, 1178)                           # S19 « calcule-le » : depuis P1

# --- légendes de l'équation finale (S21) ---
LEG_POSSEDES, LEG_DOIS, LEG_LIMITES = (295, 805), (765, 705), (560, 1048)

# --- la fin (kit.outro) : carte (540, 760), bouton 380 x 112 ; toucher au doigt, pas de flèche de souris ---
FIN_C = (540, 760)
FIN_BUTTON = (540, 908)
FIN_TAP = (684, 944)                            # bas droit du bouton, hors du libellé


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


for _x, _pt, _what in [(TOI_P2[0], NET_PEN, "S03 naissance de « Patrimoine net »"),
                       (TOI_P2[0], NET_PEN_TRACE[0], "S03 début du soulignement"),
                       (TOI_P2[0], NET_PEN_TRACE[1], "S03 fin du geste de soulignement"),
                       (TOI_P1[0], (720, 996), "S08 toucher le bas de la grille"),
                       (TOI_P3[0], ACHAT_STRIKE[0], "S10 « Prix d’achat » (droite)"),
                       (TOI_P3[0], ACHAT_STRIKE[1], "S10 « Prix d’achat » (gauche)"),
                       (TOI_P1[0], GRISE_TAP, "S12 / S15 toucher la part grise"),
                       (TOI_P2[0], MENS_STRIKE[0], "S13 « Mensualité » (droite)"),
                       (TOI_P2[0], MENS_STRIKE[1], "S13 « Mensualité » (gauche)"),
                       (TOI_P1[0], BRUT_STRIKE[0], "S15 « 250 000 € » (droite)"),
                       (TOI_P1[0], BRUT_STRIKE[1], "S15 « 250 000 € » (gauche)"),
                       (TOI_P1[0], AXE_TAP, "S19 toucher l'axe du temps"),
                       (TOI_P1[0], REGARD_BARRE[0], "S21 barrer le regard (haut)"),
                       (TOI_P1[0], REGARD_BARRE[1], "S21 barrer le regard (bas)")]:
    assert_reach(_x, _pt, _what)


# ---------- petites fabriques ----------
def png(S, id, name, w, pos, z=5, contact=True, parent=None, scale=0):
    """Illustration générique (verre, alpha strict), largeur w, rapport gardé. -> meta (+ h_disp)."""
    m = S.png(name)
    h = round(w * m["h"] / m["w"])
    p = dict(contact=dict(w=round(w * 0.7), h=22, dy=4, blur=10, alpha=0.2)) if contact else {}
    S.add(id, "png", z=z, parent=parent, src=m["src"], w=w, h=h, **p)
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
    """Trait ouvert à tracer (shape poly, draw 0) ; le 1er sommet est le départ du tracé (Figure.strike(line=id,
    track="draw"))."""
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


def move_with_grid(kit, f, small, d=None, e="inOut", extra=()):
    """Déplace la grille vers GRILLE_SMALL (small=True) ou GRILLE_FULL, et la pilule du solde avec la même clé
    (sauf si elle est hors de sa case). `extra` : [(id, point monde, échelle)] à déplacer dans les mêmes images."""
    from pipeline.story import MOVE
    d = d or MOVE
    c, k = (GRILLE_SMALL, GRILLE_SMALL_K) if small else (GRILLE_FULL, GRILLE_FULL_K)
    kit.move("grille", f, list(c), d=d, e=e, scale=k)
    kit.move("solde", f, list(SOLDE_CELL_SMALL if small else SOLDE_CELL_FULL), d=d, e=e,
             scale=round(SOLDE_CELL_K * k, 4))
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
    "solde": {"pos": list(SOLDE_CELL_FULL), "scale": SOLDE_CELL_K, "text": T_SOLDE_VAL, "textOp": 1},
    **{CASE_IDS[i]: {"pos": list(CELL_LOCAL[i]), "scale": 1} for i in range(1, 6)},
    **{f"{CASE_IDS[i]}_mot": {"chars": len(CASES[i][1].replace("\n", ""))} for i in range(1, 6)},
    **{Q_IDS[i]: {"pos": list(CELL_LOCAL[i]), "scale": 0} for i in range(1, 6)},
    **{Q_IDS[i]: {"pos": list(CELL_LOCAL[i]), "scale": 1} for i in range(6, 9)},
    **{CASE_IDS[i]: {"pos": list(CELL_LOCAL[i]), "scale": 0} for i in range(6, 9)},
    "marqueur": {"pos": [MARKER_CX, MARKER_Y], "scale": 1, "on": 1, "active": 0, "done0": 0, "done1": 0, "done2": 0},
    "regard": {"draw": 0, "from": 0},
    "net_trait": {"draw": 0},
    **_OFF("dettes", "net", "entete", "cadre", "moins", "egal", "cible", "depart", "fleche_pointe", "strategie",
           "question", "jeton", "etiquette", "barre", "brut", "resultat", "alerte", "graphe_freq"),
    "fil_grille": {"draw": 0, "from": 0}, "fil_dettes": {"draw": 0, "from": 0}, "fleche": {"draw": 0, "from": 0},
}

ENTRY_P3 = {   # fin de S15 = etat_initial de S16 (image 1915)
    "grille": {"pos": list(GRILLE_SMALL), "scale": GRILLE_SMALL_K},
    "compte": {"pos": list(CELL_LOCAL[0]), "scale": 1, "w": CELL_W, "h": CELL_H, "fill": _lo(PAPER),
               "stroke": _lo(INK)},
    "compte_mot": {"text": T_COMPTES},
    "solde": {"pos": list(SOLDE_CELL_SMALL), "scale": round(SOLDE_CELL_K * GRILLE_SMALL_K, 4), "text": T_SOLDE_VAL},
    **{CASE_IDS[i]: {"pos": list(CELL_LOCAL[i]), "scale": 1} for i in range(1, 9)},
    **{Q_IDS[i]: {"scale": 0} for i in range(1, 9)},
    "case_immo_place": {"scale": 1},
    "marqueur": {"pos": [MARKER_CX, MARKER_Y], "scale": 1, "on": 1, "active": 1, "done0": 1, "done1": 0, "done2": 0},
    "jeton": {"pos": list(JETON_P2), "scale": JETON_P2_K},
    "etiquette": {"pos": list(ETIQ_P2), "scale": 1},
    "etiq_achat": {"opacity": 0}, "etiq_valeur": {"chars": len(T_VALEUR)}, "etiq_montant": {"scale": 1, "value": V_250},
    "ficelle": {"draw": 0}, "ficelle_jeton": {"draw": 1},
    "barre": {"pos": list(BARRE_SHORT_C), "scale": 1, "w": BARRE_SHORT_W},
    "resultat": {"pos": list(RESULTAT_C), "scale": 1},
    "calc_a": {"chars": len(T_CALC_A)}, "calc_b": {"chars": len(T_CALC_B)},
    "dettes": {"scale": 0},
    **_OFF("net", "entete", "cadre", "moins", "egal", "cible", "depart", "fleche_pointe", "strategie", "question",
           "alerte", "accolade", "restant", "graphe_freq"),
    "brut": {"opacity": 0}, "mensualite": {"opacity": 0}, "mensualite_mot": {"opacity": 0},
    "regard": {"draw": 0, "from": 0}, "net_trait": {"draw": 0},
}


def cast(S, kit):
    """Toute la distribution, à son état de l'image 0. Ce qui arrive plus tard : scale=0 (ou draw=0, chars=0,
    opacity=0). Seuls `fin` et son curseur naissent dans kit.outro (p3)."""

    # --- la grille (groupe invisible) : pleine à l'image 0 (ses enfants sont cachés, sauf la carte « Solde ») ---
    kit.shape("grille", list(GRILLE_FULL), kind="rect", w=1, h=1, fill="none", stroke="none", sw=0, shadow=0, z=6)
    for i in range(1, 9):
        key, label, icon, size = CASES[i]
        # case « ? » : contour encre 3 px en tirets, sans fond ni ombre ; « ? » ExtraBold 80 ; posée DERRIÈRE la case
        # du solde (case 0, z plus bas) : en S02 elle en sort (pop) puis glisse à CELL_LOCAL[i]
        kit.shape(Q_IDS[i], list(CELL_LOCAL[0]), kind="round", w=CELL_W, h=CELL_H, r=CELL_R, fill="none", stroke=INK,
                  sw=3, shadow=0, dash=[12, 9], z=6.2, parent="grille", scale=0)
        kit.text(f"{Q_IDS[i]}_mot", [0, 4], T_Q, size=80, weight=800, z=6.25, parent=Q_IDS[i])
        # case nommée : papier, contour encre 4, ombre ; disque light + pictogramme ; libellé (à écrire)
        cid = CASE_IDS[i]
        kit.shape(cid, list(CELL_LOCAL[i]), kind="round", w=CELL_W, h=CELL_H, r=CELL_R, fill=PAPER, stroke=INK, sw=4,
                  shadow=6, z=6.4, parent="grille", scale=0)
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
    S.set("compte", w=COMPTE_W0, h=COMPTE_H0, fill=PAPER, stroke=INK)   # hex : PAPER -> LIGHT, INK -> DEEP (S07)
    kit.icon("compte_ico", list(COMPTE_ICO0), "bank", s=COMPTE_ICO_S0, color=INK, z=6.7, parent="compte")
    kit.text("compte_mot", list(COMPTE_MOT0), T_SOLDE, size=COMPTE_MOT_S0, weight=700, anchor="start", z=6.7,
             parent="compte")
    S.set("compte_mot", text=T_SOLDE, chars=len(T_SOLDE))               # S08 : « Comptes » (piste text, puis chars)
    kit.shape("compte_filet", list(COMPTE_FILET0), kind="rect", w=COMPTE_FILET_W0, h=3, fill=RULE, stroke="none",
              sw=0, shadow=0, z=6.7, parent="compte")

    # --- la pilule du fil « 3 200 € » (monde) ---
    pill(S, "solde", SOLDE_C0, T_SOLDE_VAL, size=SOLDE_SIZE, weight=800, fill=CYAN, h=SOLDE_H, w=SOLDE_W, z=8,
         scale=1, shadow=6)
    S.set("solde", rot=0)

    # --- « Toi » (encre, visible dès l'image 0 en P1), son nom, son regard, son « ? » ---
    toi = Figure(kit, "toi", pos=TOI_P1, variant="ink", side="left", show=True)
    pill(S, "nom_toi", NOM_ABOVE, T_TOI, size=34, fill=LIGHT, h=NOM_H, w=NOM_W, z=15.8, parent="toi", scale=1,
         sw=3)
    wire(S, "regard", 14, INK, 4, pa=REGARD_EYE, pb=REGARD_CARTE, dash=[12, 10])
    S.set("regard", color=INK)                  # hex : INK -> RED (S20 « solde. »)
    line(kit, "regard_barre", REGARD_BARRE, color=INK, sw=6, z=14.2)   # S21 « C’est » : le stylo coupe le regard
    wire(S, "regard_net", 14, DEEP, 6, pa=REGARD_NET[0], pb=REGARD_NET[1])
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
    S.set("dettes", w=DETTES_W, h=DETTES_H, stroke=INK)   # S11 : part grise (w, h) ; S13 : contour INK -> DEEP (hex)
    kit.icon("dettes_ico", list(DETTES_ICO_CARD), "bank", s=DETTES_ICO_S, color=INK, z=10.6, parent="dettes")
    kit.text("dettes_mot", list(DETTES_MOT_CARD), T_DOIS_CARTE, size=34, weight=700, anchor="start", z=10.6,
             parent="dettes")
    S.set("dettes_mot", text=T_DOIS_CARTE)      # S11 : T_DOIS_BARRE (ancre start : recaler pos) ; S12 : T_CRD
    kit.counter("dettes_val", list(GRISE_VAL), value=0, size=GRISE_VAL_SIZE, weight=800, suffix=" €", z=10.6,
                parent="dettes", scale=0)
    pill(S, "net", NET_C, T_NET, size=NET_SIZE, weight=800, fill=LIGHT, h=NET_H, w=NET_W, z=11, shadow=6)
    line(kit, "net_trait", NET_TRAIT_LOCAL, color=DEEP, sw=5, z=11.1, parent="net")
    wire(S, "fil_grille", 7.5, DEEP, 5, a={"id": "cadre", "at": list(FIL_GRILLE_A)},
         b={"id": "net", "at": list(FIL_NET_A)})
    wire(S, "fil_dettes", 7.5, DEEP, 5, a={"id": "dettes", "at": list(FIL_DETTES_A)},
         b={"id": "net", "at": list(FIL_NET_B)})
    wire(S, "fil_net", 7.5, DEEP, 5, a={"id": "grille", "at": list(FIL_P3_GRILLE)},
         b={"id": "net", "at": list(FIL_P3_NET)})

    # --- la cible de la stratégie (S05) ---
    png(S, "cible", "TARGET", CIBLE_W, CIBLE_C, z=5)
    kit.shape("cible_onde", list(CIBLE_C), kind="circle", w=120, fill="none", stroke=DEEP, sw=6, shadow=0, z=5.2,
              opacity=0)
    kit.shape("depart", list(DEPART_C), kind="circle", w=2 * DEPART_R, fill=CYAN, stroke=INK, sw=3, shadow=0, z=11.3,
              scale=0)
    wire(S, "fleche", 11.2, DEEP, 6, pa=DEPART_C, pb=FLECHE_B)
    head(kit, "fleche_pointe", FLECHE_B, FLECHE_ROT, color=DEEP, z=11.25, s=1.2)
    kit.text("strategie", list(STRATEGIE_C), T_STRATEGIE, size=34, weight=700, color=DEEP, z=9, typed=True)

    # --- le repère 1-2-3 (S06 -> S22), sans étape active jusqu'à « possèdes ? » (piste on) ---
    kit.steps_marker(MARKER_LABELS, id="marqueur", y=MARKER_Y, cx=MARKER_CX, gap=MARKER_GAP, z=20)
    S.ents["marqueur"]["p"].update(labelSize=MARKER_LABEL, moveBlank=True, doneStyle="kept")
    S.set("marqueur", scale=0, on=0, done0=0, done1=0, done2=0, lbl=1)

    # --- le jeton-maison (TOKEN.png, monde) et l'étiquette de prix ---
    tok = png(S, "jeton", "TOKEN", JETON_W, JETON_CELL, z=9)
    jeton_bottom = (0, round(tok["h_disp"] / 2))
    kit.shape("etiquette", list(ETIQ_S10), kind="poly", pts=ETIQ_PTS, fill=PAPER, stroke=INK, sw=4, shadow=6, z=9.5,
              scale=0)
    kit.shape("etiq_oeillet", list(OEILLET_LOCAL), kind="circle", w=2 * OEILLET_R, fill=PAPER, stroke=INK, sw=4,
              shadow=0, z=9.6, parent="etiquette")
    kit.text("etiq_achat", list(ACHAT_LOCAL), T_PRIX_ACHAT, size=ACHAT_SIZE, weight=700, color=RED, z=9.6,
             parent="etiquette")
    w_achat = text_width(T_PRIX_ACHAT, ACHAT_SIZE, 700)
    line(kit, "etiq_achat_barre", [[w_achat / 2 + 3, 0], [-w_achat / 2 - 3, 0]], color=INK, sw=7, z=9.7,
         parent="etiq_achat")              # S10 « valeur » : Figure.strike(line="etiq_achat_barre", track="draw")
    kit.text("etiq_valeur", list(VALEUR_LOCAL), T_VALEUR, size=VALEUR_SIZE, weight=700, color=DEEP, z=9.6,
             parent="etiquette", typed=True)
    kit.counter("etiq_montant", list(MONTANT_LOCAL), value=0, size=MONTANT_SIZE, weight=800, suffix=" €", z=9.6,
                parent="etiquette", scale=0)
    wire(S, "ficelle", 9.4, DEEP, 3, a={"id": "case_immo", "at": list(FICELLE_CASE_A)},
         b={"id": "etiquette", "at": list(OEILLET_LOCAL)})
    wire(S, "ficelle_jeton", 9.4, DEEP, 3, a={"id": "jeton", "at": list(jeton_bottom)},
         b={"id": "etiquette", "at": list(OEILLET_LOCAL)})

    # --- la barre de l'appartement, le bord « Mensualité », l'accolade, « 250 000 € » rouge, le résultat ---
    kit.shape("barre", list(BARRE_C), kind="round", w=BARRE_W, h=BARRE_H, r=14, fill=CYAN, stroke=INK, sw=5,
              shadow=6, z=10, scale=0)
    S.set("barre", w=BARRE_W)
    kit.shape("mensualite", list(MENS_C), kind="rect", w=MENS_W, h=BARRE_H, fill="none", stroke=RED, sw=4, shadow=0,
              z=10.8, draw=0)
    kit.text("mensualite_mot", list(MENS_MOT), T_MENSUALITE, size=34, weight=700, color=RED, anchor="start", z=10.8,
             typed=True)
    w_mens = text_width(T_MENSUALITE, 34, 700)
    line(kit, "mensualite_barre", [[w_mens + 6, 0], [-6, 0]], color=INK, sw=7, z=10.9, parent="mensualite_mot")
    kit.shape("accolade", list(ACCOLADE_C), kind="poly", pts=ACCOLADE_PTS, closed=False, fill="none", stroke=DEEP,
              sw=5, shadow=0, z=11, draw=0)
    kit.text("restant", list(RESTANT_C), T_RESTANT, size=34, weight=700, color=DEEP, z=11, typed=True)
    pill(S, "brut", BRUT_C, T_250, size=BRUT_SIZE, weight=800, fill=PAPER, h=BRUT_H, w=BRUT_W, z=12, color=RED,
         stroke=RED, sw=5)
    w_brut = text_width(T_250, BRUT_SIZE, 800)
    line(kit, "brut_barre", [[w_brut / 2 + 3, -2], [-w_brut / 2 - 3, -2]], color=INK, sw=7, z=12.1, parent="brut")
    pill(S, "resultat", RESULTAT_C, T_RESULTAT, size=44, weight=800, fill=LIGHT, h=RESULTAT_H, w=RESULTAT_W, z=12,
         shadow=6)
    kit.text("calc_a", [CALC_X, CALC_Y], T_CALC_A, size=CALC_SIZE, weight=700, anchor="start", z=12, typed=True)
    kit.text("calc_b", [round(CALC_X + text_width(T_CALC_A, CALC_SIZE, 700), 1), CALC_Y], T_CALC_B, size=CALC_SIZE,
             weight=700, color=DEEP, anchor="start", z=12, typed=True)

    # --- point 3 : signe d'attention, pastilles, graphe ---
    kit.icon("alerte", list(ALERTE_C), "warning", disc=ALERTE_R, fill=PAPER, color=INK, shadow=4, z=11.5, scale=0)
    for pid, (mot, icon, place, _src) in PASTILLES.items():
        kit.shape(pid, list(place), kind="round", w=PAST_W, h=PAST_H, r=PAST_H / 2, fill=PAPER, stroke=INK, sw=4,
                  shadow=4, z=12, scale=0)
        if icon:
            kit.icon(f"{pid}_ico", list(PAST_ICO_LOCAL), icon, disc=PAST_DISC, fill=LIGHT, color=INK, shadow=0,
                     z=12.1, parent=pid)
        else:                                   # « estimé » : « ≈ » ExtraBold dans le disque
            kit.shape(f"{pid}_ico", list(PAST_ICO_LOCAL), kind="circle", w=2 * PAST_DISC, fill=LIGHT, stroke=INK,
                      sw=3, shadow=0, z=12.1, parent=pid)
            kit.text(f"{pid}_approx", [0, 1], "≈", size=28, weight=800, z=12.15, parent=f"{pid}_ico")
        kit.text(f"{pid}_mot", list(PAST_MOT_LOCAL), mot, size=34, weight=700, anchor="start", z=12.1, parent=pid)
        S.set(f"{pid}_mot", under=0)
    line(kit, "axes", AXE_PTS, color=INK, sw=4, z=9)
    head(kit, "axe_y_pointe", AXE_Y_TIP, -90, color=INK, z=9.05)
    head(kit, "axe_x_pointe", AXE_X_TIP, 0, color=INK, z=9.05)
    kit.text("axe_y_mot", list(AXE_Y_MOT), T_AXE_Y, size=30, weight=700, anchor="start", z=9, opacity=0)
    kit.text("axe_auj", list(AUJ_C), T_AUJ, size=30, weight=700, z=9, opacity=0)
    for k, (x, t) in enumerate(zip(GRAD_XS, T_ANS)):
        kit.shape(f"grad{k + 1}", [x, 1180], kind="rect", w=4, h=14, fill=INK, stroke="none", sw=0, shadow=0, z=9,
                  opacity=0)
        kit.text(f"grad{k + 1}_mot", [x, GRAD_Y], t, size=30, weight=700, z=9, opacity=0)
    for k, p in enumerate(POINTS):
        kit.shape(f"point{k + 1}", list(p), kind="circle", w=2 * POINT_R, fill=CYAN, stroke=INK, sw=3, shadow=0,
                  z=9.6, scale=0)          # point1 = le point « repère » (tombe de « Patrimoine net », S18)
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
