"""V09 « « Capital garanti, 5 %, disponible » ? » : mise en scène Story, en paquet (une partie par fichier).

Storyboard : scripts/storyboards/V09.json (v1, révisé après le test sans son, 22 scènes, 90 temps forts, 90,786 s),
version lisible scripts/storyboards/V09.md. Voix : build/V09/words.json (film : images 0-2723).
Fil : les trois promesses cyan de l'offre (`promesse1..3`, pill 440 x 76, Bold 36) : imprimées sur l'étiquette
(S01) -> sanglées puis séparées (S06) -> rangées dans le repère (leur pictogramme reste dans le disque) et
ressorties une par une (S07, S11, S15) -> attachées par des fils à leurs réponses écrites (S21) -> fondues en bouton
« S’abonner » (S22).
Parti pris : les promesses à l'épreuve de l'argent de « Toi » : 5 pièces versées dans la boîte du produit (S07) ;
le bouclier (garant, frais, échéance), le « 5 % » (cadre court / cadre long, passé / futur, boosté), la sortie
(cadenas, durée, pénalités, délai), le mythe ; chute : rembobinage, 4 questions, réponses écrites par la boîte, coches.

Tour de revue 1 (corrections) : barre de temps élargie (x 210-850, y 880, h 44 ; rond « Signature » et calendrier de
90 px), cadres court / long pleins à aplat cyan clair, bande « boosté » qui remplit le cadre court, graphique S13 en
plein cadre, repère à grands disques (r 38) qui gardent le pictogramme de la promesse rangée et marquent une étape vue
d'un « * » (doneMark « asterisk », jamais une coche), plus de PNG (la boîte écrit elle-même les réponses), fils
« * » -> réponse en S21, carte de fin qui naît de la fusion des pilules (outro grow_at / title_at).

Parties (scènes contiguës) :
- p1 : S01-S07, images 0-905 ; p2 : S08-S15, images 906-1810 ; p3 : S16-S22, images 1811-2723.
ENTRY_P2 et ENTRY_P3 sont le contrat des raccords (kit.pin à first_frame - 1). Les figurines n'y sont jamais.

Pas d'IA dans V09. « Toi » (figurine encre, side « left », échelle 1, pieds sur y 1230) est seul à tenir le stylo ;
nommé dès l'image 0 par `nom_toi`. Entre deux gestes, son bras est BAISSÉ (Figure.lower / hold_low / walk(low=True),
prise relevée : pointe du stylo à y <= 1250). Places : P1 (860, 1135), P2 (790, 1135), P3 (650, 1135), mythe
(575, 1135). Le bras gauche ne touche proprement qu'une cible à sa gauche (|dx| >= 0,3 x dy) à 267 px au plus :
`assert_reach` (toutes les cibles de GESTES sont vérifiées à l'import).
Garants (S09-S10) : figurines papier `variant="societe"` sans outil, qui ne bougent que par Figure (lean_to, enter,
exit). Rouge : la sangle et les fausses coches (S06), la pièce des frais et « hors frais » (S10), la pièce reprise et
« Pénalités » (S16), le « = » du mythe et la pièce qui glisse (S17), la pièce perdue et « −1 » (S18) ; karaoké :
ALERT_WORDS. Aucun gris de mise en retrait. Aucun PNG.
"""
import importlib
import math
import os
from types import SimpleNamespace

from pipeline.story import GEOM, STYLE, text_width
from pipeline.story_kit import Figure, Kit, Sheet, solve_ik

PARTS = ["p1", "p2", "p3"]                      # S01-S07, S08-S15, S16-S22
NBSP = " "                                 # espace insécable (avant « : », « ? »)
NNBSP = " "                                # espace fine insécable (« 5 % », « ? % », « ↑ boosté »)
ALERT_WORDS = {"piège", "frais", "pénalités", "perdre"}   # karaoké en rouge : les pièges (S06, S10, S16, S18)
ACOUSTIC_SNAP = {"gap": 0.2, "window": 0.08}    # temps fort après un silence : calé sur l'attaque audible
CAPTION_GROUPS = [                              # pas de mot seul, pas de négation ni de déterminant coupés
    ["on va voir pourquoi", "ces trois promesses", "sont trois réalités", "différentes"],
    ["Et quelles questions", "poser avant de signer"],
    ["La garantie vaut", "ce que vaut", "celui qui la donne"],
    ["d’accord mais", "sur quelle période"],
    ["peut ne valoir que", "quelques mois"],
    ["Disponible", "vraiment tout de suite"],
    ["protégé", "ne veut pas dire", "sans risque"],
    ["ou ne rien gagner", "du tout"],
    ["Qu’est-ce qui", "est garanti"],
    ["ce sont les conditions", "qui la rendent", "vraie"],
]

# ---------- couleurs ----------
INK, CYAN, DEEP, LIGHT = STYLE["ink"], STYLE["cyan"], STYLE["deep"], STYLE["light"]
PAPER, RED, BG = STYLE["paper"], STYLE["red"], STYLE["bg"]

# ---------- textes à l'écran (typographie française) ----------
T_TOI = "Toi"
T_PRODUIT = "Produit"
T_PROMESSES = ["Capital garanti", "Rendement", "Disponible"]
PROMESSE_ICONES = ["shield", "percent", "clock"]
T_5 = f"5{NNBSP}%"
T_Q_PCT = f"?{NNBSP}%"
T_AST = "*"
T_SOUS_COND = "* sous conditions"
MARKER_LABELS = ["Garantie", "Rendement", "Disponible"]
T_SIGNATURE, T_ECHEANCE = "Signature", "Échéance"
T_GARANTS = ["Assureur", "Banque", "Émetteur"]
T_HORS_FRAIS = "hors frais"
T_BOOSTE = "boosté"
T_PASSE, T_FUTUR = "passé", "futur"
T_DUREE, T_PENALITES, T_DELAI = "Durée", "Pénalités", "Délai"
T_MYTHE = ["Protégé", "=", "sans risque"]       # le « = » rouge, barré en « ≠ » par le stylo (S17)
T_MOINS1 = "−1"
T_PLUS = "+"
T_RIEN_GAGNE = "rien gagné"
T_FICHE_TITRE = "4 questions"
T_QUESTIONS = [f"Garanti{NBSP}: quoi{NBSP}?", f"Par qui{NBSP}?", f"Jusqu’à quand{NBSP}?", f"Conditions{NBSP}?"]
QUESTION_ICONES = ["shield", "building", "cal", "none"]   # 4e puce : cercle vide + « * » (fiche_ast) par-dessus
T_REPONSES = ["hors frais", "Émetteur", "Échéance", "Pénalités"]
REPONSE_ICONES = ["euro", "building", "cal", "lock"]      # l'objet que chaque réponse rappelle (S10, S09, S10, S16)
T_ABONNER = "S’abonner"

# ---------- mise en page (1080 x 1920) ----------
X_MIN, X_MAX, Y_MIN, Y_MAX = 40, 940, 160, 1270
GROUND = 1230                                   # ligne de sol : pieds de « Toi »
FLOOR = 1180                                    # sol des pièces (centres des pièces posées : y 1180)
FIG_BASE = GEOM["FIGURE"]["base"]
HEAD_DY = GEOM["FIGURE"]["head"]["cy"]          # -64 : centre de la tête
HEAD_R = GEOM["FIGURE"]["head"]["r"]
SHOULDER_DX, SHOULDER_DY = abs(GEOM["FIGURE"]["shoulder"][0]), GEOM["FIGURE"]["shoulder"][1]   # 30, -16
REACH_OK = 267
TOI_SCALE = 1.0
TOI_LOW_GRIP = (52, 10)                         # bras baissé : prise relevée de 30 px (pointe à y 1247, hors sous-titres)


def fig_pos(x, feet=GROUND, s=TOI_SCALE):
    return [x, round(feet - FIG_BASE * s, 2)]


P1 = fig_pos(860)                               # (860, 1135) : S01, S10, S19-S20
P2 = fig_pos(790)                               # (790, 1135) : S02-S06, S11-S14, S16 (après le cadenas)
P3 = fig_pos(650)                               # (650, 1135) : S07-S09, S15-S16
P_MYTHE = fig_pos(585)
P_RECUL = fig_pos(820)                          # S16 : recul après le cadenas (stylo loin des pièces)                          # (585, 1135) : S17-S18 (le stylo atteint le « = » et la barre)
TOI_S21 = 820                                   # S21-S22
NOM_TOI_LOCAL, NOM_TOI_W, NOM_TOI_H = (0, -135), 96, 54   # pilule « Toi » au-dessus de la tête (monde y 1000)
TOI_TETE = {k: (p[0], p[1] + HEAD_DY) for k, p in (("P1", P1), ("P2", P2), ("P3", P3))}   # centre de la tête

# --- colonne d'action et places fixes ---
ACTION_X = 540
PROMESSE_POINT = (540, 470)                     # la promesse du point, seule sous le repère (S07-S19)

# --- le repère 1-2-3 légendé (en haut), grands disques, pictogramme de la promesse rangée ---
MARKER_Y, MARKER_CX, MARKER_GAP = 300, 540, 240   # disques x 300, 540, 780
MARKER_LABEL_SIZE, MARKER_LABEL_DY = 32, 86       # légendes y 386
MARKER_R, MARKER_ACTIVE_R = 38, 46
DISQUES = [(300, MARKER_Y), (540, MARKER_Y), (780, MARKER_Y)]
LEGENDE_BAS = MARKER_Y + MARKER_LABEL_DY + 20     # bas des légendes (y 406)

# --- l'étiquette de l'offre (S01-S06 au centre ; S07-S19 collée sur la boîte) ---
ETIQ_C, ETIQ_W, ETIQ_H, ETIQ_R = (470, 680), 560, 380, 24     # x 190-750, y 490-870
ETIQ_COLLEE, ETIQ_COLLEE_K = (300, 1125), 0.42  # S07-S19 : x 182-418, y 1045-1205 (sur le devant de la boîte)
TROU_LOCAL, TROU_R = (-242, 0), 14
SOUS_COND_LOCAL = (0, 165)                      # « * sous conditions » (monde 470, 845), SemiBold 28
ETIQ_AST_SIZE = 114                             # S07 : un seul grand « * » sur la carte collée (48 px à l'écran)

# --- les trois promesses (objet du fil) : pill sans `icon` + pictogramme et mot enfants ---
PROMESSE_W, PROMESSE_H, PROMESSE_SIZE = 440, 76, 36
PROMESSES_ETIQ = [(500, 580), (500, 680), (500, 780)]          # S01-S05, sur l'étiquette
PROMESSES_ECARTEES = [(500, 555), (500, 680), (500, 790)]      # S06 « sépare, »
PROMESSES_S21 = [(540, 230), (540, 320), (540, 410)]           # S21 : l'une sous l'autre, au-dessus de la fiche
PROMESSE_ICONE_LOCAL, PROMESSE_ICONE_S = (-PROMESSE_W / 2 + 34, 0), 46
PROMESSE_MOT_LOCAL = (18, 0)
COCHE_RONDE_LOCAL, COCHE_RONDE_R = (185, 0), 22                # coche imprimée au bout de la pilule 1
AST_LOCAL = {2: (168, 12), 3: (190, 12)}                       # « * » des pilules 2 et 3, dans l'aplat cyan
AST1_LOCAL = (250, -15)                                        # S10 : « * » de la pilule 1, après sa coche
AST_SIZE = 64
AST_VIS_DY = -14                                               # centre visible du « * » (ExtraBold 64) / son ancre

# --- la pastille « 5 % » (cercle 120 = r 60 à l'échelle 1 ; texte enfant ExtraBold 52) ---
PASTILLE_R0 = 60
PASTILLE_S01, PASTILLE_ROT0 = (770, 680), -12   # S01-S05 : au bout de la pilule 2, inclinée
PASTILLE_ROND = (800, 470)                      # S11 : ressort collée au bout droit de « Rendement »
PASTILLE_CENTRE, PASTILLE_K_CENTRE = (540, 660), 2.0      # S11 : r 120
PASTILLE_K_FRISE = 40 / 60                      # S12-S14 : r 40 (80 px), sur la barre
PASTILLE_ANNONCE = (384, 776)                   # S12 « annoncé, » : au-dessus du début de la barre
PASTILLE_K_ANNONCE = 44 / 60
PASTILLE_K_GRAPHE = 45 / 60                     # S13 : 90 px
PASTILLE_K_QPCT = 40 / 60
PASTILLE_AST_LOCAL = (52, -60)                  # « * » enfant, coin haut droit
PASTILLE_K_PILL = 34 / 60                       # S15-S22 : la pastille « ? % » accrochée à « Rendement »

# --- la boîte du produit ---
PRODUIT_C, PRODUIT_W, PRODUIT_H = (300, 1115), 280, 190   # x 160-440, y 1020-1210
FENTE_LOCAL, FENTE_W, FENTE_H = (0, -83), 90, 12          # fente (monde 300, 1032)
FENTE = (300, 1032)
PRODUIT_COIN_HG_LOCAL = (-140, -95)
PRODUIT_NOM_LOCAL = (0, 30)                     # S01-S06 : étiquette « Produit » sur le devant de la boîte
BAC_C, BAC_W, BAC_H = (300, 1224), 250, 28      # S20 : bac à papier (sous la boîte)
LEVRE_C, LEVRE_W, LEVRE_H = (300, 1012), 140, 14  # S20 : lèvre d'entrée sur la fente

# --- les 5 pièces de « Toi » (icon euro, disque light r 28 ; fill en hex : light -> rouge) ---
PIECE_R = 28
PILE = [(510, 1180), (566, 1180), (622, 1180), (538, 1128), (594, 1128)]   # 60 px à gauche : hors du stylo de « Toi »
PILE_HAUT = (594, 1128)
PIECE_FRAIS_SOL = (520, 1180)                   # S10 : la pièce des frais tombe ici, rouge, sous « hors frais »
HORS_FRAIS_C = (545, 1112)
PIECE_EXTRAITE = (480, 1000)                    # S15 « argent. » -> S16
COUVERCLE = [(185, 990), (245, 990), (305, 990), (365, 990)]   # S18 : piece1..4 rangées sur la boîte
PLACE_GAIN_C, PLACE_GAIN_R = (432, 990), 38     # S18 : 5e place en tirets, à la taille d'une pièce x 1,4
RIEN_GAGNE_C = (545, 1062)

# --- le rond de signature puis la barre de temps « Signature -> Échéance » (élargie) ---
SIGNATURE_C, SIGNATURE_R = (640, 905), 36       # S04 : sous le coin bas droit de l'étiquette
MOT_SIGNATURE_C = (510, 905)
SIGNATURE_TIP = (668, 940)                      # S04 « signer. » : la pointe s'arrête avant le rond
FRISE_Y, FRISE_X0, FRISE_X1, FRISE_H = 880, 210, 850, 44
FRISE_C, FRISE_W = ((FRISE_X0 + FRISE_X1) / 2, FRISE_Y), FRISE_X1 - FRISE_X0   # (530, 880), 640
SIGNATURE_FRISE, SIGNATURE_K_FRISE = (FRISE_X0, FRISE_Y), 45 / 36            # S10 : départ de la barre, 90 px
MOT_SIGNATURE_FRISE = (FRISE_X0, 805)            # légendes AU-DESSUS de la barre (dessous : « Toi », pièces)
CAL_C, CAL_R = (FRISE_X1, FRISE_Y), 45          # calendrier de l'échéance (disque cyan, 90 px)
MOT_ECHEANCE_C = (FRISE_X1, 805)
BARRE_G, BARRE_D = FRISE_X0 + 45, FRISE_X1 - 45  # partie visible de la barre entre les deux disques (255-805)
CADRE_COURT_C, CADRE_COURT_W, CADRE_COURT_H = (340, FRISE_Y), 180, 92     # x 250-430 : le court début
CADRE_LONG_C, CADRE_LONG_W, CADRE_LONG_H = (530, FRISE_Y), 760, 112       # x 150-910 : toute la durée
BOOST_X0, BOOST_X1 = BARRE_G, 428               # bande « boosté » : remplit le cadre court (173 x 44)
BOOST_PILL_C = ((BOOST_X0 + BOOST_X1) / 2, 963)  # « ↑ boosté » centré sur la bande, 8 px sous le cadre court
APRES_X0, APRES_X1 = 446, 798                   # S14 « quelques » : le reste de la barre en tirets
CURSEUR_R = 15                                  # S10 « précise. » : curseur qui court sur la barre
FRISE_TIERS = 0.37                              # S16 « durée, » : la barre se remplit à 0,37 (x 447)
FRISE_TAP = (round(FRISE_X0 + FRISE_TIERS * FRISE_W), FRISE_Y)   # S18 « sors » : (447, 880)
REPERE_C, REPERE_H = FRISE_TAP, 60

# --- le bouclier (icon shield, disque cyan r 62 à l'échelle 1) ---
BOUCLIER_R0 = 62
BOUCLIER_BOITE = (300, 1120)
BOUCLIER_COUVERCLE = (300, 1080)                # S10 « parfois » : remonté de 40 px, il couvre la fente
BOUCLIER_TAP = (362, 1110)                      # S08 « mais » : bord droit du bouclier (depuis P3 : 258 px)
BOUCLIER_HAUT = (300, 1058)                     # départ du fil vers le garant
BOUCLIER_ECHEANCE, BOUCLIER_K_ECHEANCE = (FRISE_X1, 728), 45 / 62   # au-dessus de « Échéance »
BOUCLIER_MYTHE, BOUCLIER_K_MYTHE = (192, 905), 52 / 62     # S17 : à gauche de la formule
ABRI = [(150, 960), (192, 968), (234, 960)]     # S17 « sans » : trois pièces à l'abri, devant le bouclier
GLISSE = (96, 1012)                             # S17 « risque » : la 4e glisse dessous et sort, rouge
BOUCLIER_K_FAIBLE = 30 / 62                     # S09 « celui » : rétrécit avec le garant qui se fissure

# --- garants (S08-S10) : immeubles plus bas, noms AU-DESSUS (le fil arrive au pied, sans croiser les noms) ---
SILHOUETTE_C = (300, 700)
SILHOUETTE_PTS = [[-75, 105], [-75, -45], [0, -105], [75, -45], [75, 105]]   # immeuble : corps + pignon
CREUX_C, CREUX_R = (300, 724), 30               # S08 : la place vide du garant (cercle en tirets) dans la silhouette
GARANTS_C = [(300, 700), (510, 700), (720, 700)]           # assureur, banque, emetteur (centres, échelle 0,75)
GARANT_K = 0.75
GARANT_PILLS_Y = 552                            # noms au-dessus des immeubles (haut du portique : y 590)
FIL_BAS = BOUCLIER_HAUT
FIL_HAUT = [(x, 776) for x, _ in GARANTS_C]     # bout haut du fil : au pied de l'immeuble visé
FIL_HAUT_S08 = (CREUX_C[0], CREUX_C[1] + CREUX_R)   # S08 : sous la place vide
FIL_COUDE = [300, 850]                          # le fil monte droit du bouclier puis file vers le garant
FISSURE_PTS = [[-10, -150], [12, -122], [-12, -96], [10, -66], [-8, -36], [6, -6]]   # S09 : fissure du haut en bas

# --- graphique passé / futur (S13, plein cadre : bar, bouclier et boîte sortis) ---
AXES_O = (150, 980)                             # origine ; x -> 900, y -> 480
AXES_C = (525, 730)
AXES_PTS = [[AXES_O[0] - 525, 480 - 730], [AXES_O[0] - 525, AXES_O[1] - 730], [900 - 525, AXES_O[1] - 730]]
AUJOURDHUI = (520, 740)                         # le point « aujourd'hui » : tête de la courbe, départ des futurs
COURBE_C = (345, 830)
COURBE_PTS = [[175 - 345, 940 - 830], [215 - 345, 890 - 830], [255 - 345, 915 - 830], [305 - 345, 840 - 830],
              [350 - 345, 870 - 830], [405 - 345, 790 - 830], [450 - 345, 815 - 830], [AUJOURDHUI[0] - 345,
                                                                                         AUJOURDHUI[1] - 830]]
AUJOURDHUI_C, AUJOURDHUI_PTS = (AUJOURDHUI[0], 735), [[0, 245], [0, -245]]   # tirets x 520, y 980 -> 490
BRANCHES_FIN = [(850, 560), (850, 740), (850, 920)]         # haut, plat, bas
MOT_PASSE_C, MOT_FUTUR_C = (335, 1022), (680, 1022)
Q_FRISE_C, Q_FUTUR_C = (700, 790), (905, 742)

# --- freins à la sortie (S15-S17) ---
PANIER_TIP, PANIER_R = (555, 950), 44
PANIER_C = (555, 896)
BOITE_TAP = (430, 1035)                         # S15 « récupérer » : coin haut droit de la boîte
CADENAS_C, CADENAS_R = (405, 1075), 44          # 88 px, sur le devant droit de la boîte
MOT_DUREE_C = (530, 815)
PIECE_K_SORTIE = 1.35                           # S16 : pièces de 76 px
PIECES_SORTIE = [(485, 1185), (562, 1185)]      # S16 « pénalités » : deux pièces sautent au sol
MOT_PENALITES_C = (590, 1105)
HORLOGE_C, HORLOGE_R = (645, 1178), 46          # S16 « délai. » : cadran (secteur) dont l'aiguille fait un tour
PIECE_BUTEE = HORLOGE_C[0] - HORLOGE_R - round(PIECE_R * PIECE_K_SORTIE)   # x 567 : la pièce bute sur le cadran
MOT_DELAI_C = (645, 1098)

# --- la formule « Protégé ≠ sans risque » (groupe `mythe`, enfants en repère local) ---
MYTHE_X0, MYTHE_Y, MYTHE_SIZE, MYTHE_GAP = 268, 920, 44, 16   # y 920 : le « = » à portée du stylo
_MW = [text_width(t, MYTHE_SIZE, 800) for t in T_MYTHE]
MYTHE_W = sum(_MW) + 2 * MYTHE_GAP
MYTHE_C = (round(MYTHE_X0 + MYTHE_W / 2, 1), MYTHE_Y)      # S17 : centre du groupe
MYTHE_S18, MYTHE_K_S18 = (540, 560), 0.75
_x = -MYTHE_W / 2
MYTHE_LOCAL = []
for _w in _MW:
    MYTHE_LOCAL.append((round(_x, 1), 0))
    _x += _w + MYTHE_GAP
EGAL_CX = round(MYTHE_LOCAL[1][0] + _MW[1] / 2, 1)          # centre du « = » (repère du groupe)
BARRE_EGAL_PTS = [[EGAL_CX - 18, 25], [EGAL_CX + 18, -25]]  # trait deep 6 en biais (≠)
EGAL_MONDE = (round(MYTHE_C[0] + EGAL_CX, 1), MYTHE_Y)      # (≈ 470, 920)
MOINS1_C = (470, 1112)                          # S18 : « −1 » à côté de la pièce perdue

# --- chute (S19-S21) ---
REMBOBINER_C, REMBOBINER_R = (838, 620), 56     # à droite de la fiche qui naît
FICHE = Sheet(n=4, w=560, pitch=96)             # h 592 : rangées locales -160, -64, 32, 128
FICHE_C = (450, 710)                            # S19-S20 : x 170-730, y 414-1006
FICHE_S21, FICHE_K_S21 = (450, 760), 0.88       # S21 : x 204-696, y 500-1020 (lisible : réponses 23 px)
FICHE_TAP = (700, 990)                          # S20 « demande » : coin bas droit (depuis P1 : 183 px)
FICHE_S21_TAP = (692, 950)                      # S21 « vraie. » : bord droit de la fiche (depuis x 820 : 196 px)
REPONSE_DROITE, REPONSE_H, REPONSE_SIZE = 262, 44, 26   # réponses alignées à droite (x local 262), pictogramme
COCHE_FICHE_X = 46                              # coches de « Toi » DANS la fiche, devant chaque réponse
FICHE_AST_SIZE = 40

# --- S22 : fin (kit.outro, pos (540, 760), 620 x 520 : bouton ≈ (540, 908)) ---
FIN_C = (540, 760)
FIN_BUTTON = (540, 908)
FIN_TAP = (690, 965)
BTN_W, BTN_H = 380, 112

# --- les cibles des gestes de « Toi » (vérifiées à l'import) ---
SANGLE_NOEUD = (680, 870)                       # sur le bord bas de la sangle (côté sûr depuis P2)
GESTES = [  # (quoi, x de la figurine, cible)
    ("S04 signature (pointe arrêtée)", P2[0], SIGNATURE_TIP),
    ("S06 nœud de la sangle", P2[0], SANGLE_NOEUD),
    ("S07 haut de la pile", P2[0], PILE_HAUT),
    ("S08 bouclier", P3[0], BOUCLIER_TAP),
    ("S15 boîte", P3[0], BOITE_TAP),
    ("S16 cadenas", P3[0], CADENAS_C),
    ("S17 « = » du mythe (début du trait)", P_MYTHE[0], (EGAL_MONDE[0] - 18, EGAL_MONDE[1] + 25)),
    ("S17 « = » du mythe (fin du trait)", P_MYTHE[0], (EGAL_MONDE[0] + 18, EGAL_MONDE[1] - 25)),
    ("S18 barre", P_MYTHE[0], FRISE_TAP),
    ("S20 fiche", P1[0], FICHE_TAP),
    ("S21 fiche", TOI_S21, FICHE_S21_TAP),
    ("S22 bouton", TOI_S21, FIN_TAP),
]

# ---------- identifiants ----------
PROMESSES = ["promesse1", "promesse2", "promesse3"]
PROMESSE_MOTS = [f"{p}_mot" for p in PROMESSES]
PROMESSE_ICONES_IDS = [f"{p}_icone" for p in PROMESSES]
PIECES = [f"piece{k + 1}" for k in range(5)]
Q_ETAPES = ["q_etape1", "q_etape2", "q_etape3"]
Q_LIGNES = ["q_ligne1", "q_ligne2", "q_ligne3", "q_ligne4"]
LIENS = ["lien1", "lien2", "lien3"]             # S03 : pointillés pilule -> légende de son étape
ECLATS = ["eclat1", "eclat2"]                   # S02 : éclats de l'offre « parfaite »
GARANTS = ["assureur", "banque", "emetteur"]
GARANT_PILLS = [f"{g}_nom" for g in GARANTS]
BRANCHES = ["branche_haut", "branche_plat", "branche_bas"]
REPONSES = [f"reponse{k + 1}" for k in range(4)]
COCHES = [f"coche{k + 1}" for k in range(4)]
FICELLES = ["ficelle1", "ficelle2", "ficelle3"]   # S21 : un fil par promesse, de son « * » à sa réponse écrite
FICELLE_VERS = [0, 2, 3]                        # Capital garanti -> hors frais ; Rendement -> Échéance ;
#                                                 Disponible -> Pénalités
VIAS = [[900, 450], [884, 590], [862, 690]]     # S21 : les fils contournent les pilules par la droite
PASTILLE_S21 = (288, 322)                       # S21 : le « ? % » à gauche de « Rendement » (les fils passent à droite)
FICELLE_DE = ["ast1", "ast2", "ast3"]
FAUSSES_COCHES = ["fausse_coche2", "fausse_coche3"]
MYTHE_MOTS = ["mythe_g", "mythe_egal", "mythe_d"]
FRISE_GROUPE = ["frise", "signature", "mot_signature", "calendrier", "mot_echeance"]


def scene_f0(S, sid):
    return round(next(s for s in S.sb["scenes"] if s["id"] == sid)["t_start"] * S.fps)


def film_end(S):
    """Dernière image du film (90,786 s -> 2723) : fin de la dernière scène du storyboard."""
    return int(S.sb["scenes"][-1]["t_end"] * S.fps)


def beat(kit, sid, i, what=""):
    """Temps fort n° i (0 = premier) de la scène `sid` : kit.at avec le `mot` exact du storyboard."""
    sc = next(s for s in kit.S.sb["scenes"] if s["id"] == sid)
    return kit.at(sid, sc["beats"][i]["mot"], what)


# ---------- l'allonge de « Toi » (bras gauche) ----------
def arm_check(fig_x, pt, side="left", fig_y=P1[1]):
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
    assert 63 <= d <= REACH_OK and safe and clear >= HEAD_R + 8, \
        f"{what} : hors d'allonge depuis x {fig_x} ({side}) : {d} px, côté sûr {safe}, tête {clear} px"


def _check_reaches():
    for what, x, pt in GESTES:
        assert_reach(x, pt, what)


_check_reaches()


# ---------- bras baissé : méthodes publiques de Figure (story_kit, facultatives) ----------
def lower(fig, f, d=8, e="inOut"):
    return fig.lower(f, d, e)


def hold_low(fig, fa, fb):
    fig.hold_low(fa, fb)


def walk_low(fig, f, to, d=None, e="inOut"):
    return fig.walk(f, to, d, e, low=True)


# ---------- petites fabriques ----------
def group(kit, id, pos, z, scale=1, parent=None):
    """Groupe invisible (cercle de 2 px sans trait) : origine commune de ses enfants."""
    kit.shape(id, list(pos), kind="circle", w=2, fill="none", stroke="none", sw=0, shadow=0, z=z, parent=parent,
              scale=scale)
    return id


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


def _round_rect_perimeter(w, h, r, seg=5):
    pts = []
    corners = [(w / 2 - r, -h / 2 + r, -90), (w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90),
               (-w / 2 + r, -h / 2 + r, 180)]
    pts.append((0, -h / 2))
    for cx, cy, a0 in corners:
        for k in range(seg + 1):
            a = math.radians(a0 + 90 * k / seg)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    pts.append((0, -h / 2))
    return pts


def _split_loop(pts, x_cut_bottom, x_cut_top):
    top_y, bot_y = pts[0][1], max(p[1] for p in pts)
    right, left = [(x_cut_top, top_y)], [(x_cut_bottom, bot_y)]
    for p in pts[1:-1]:
        on_right = p[0] > x_cut_top if p[1] < 0 else p[0] > x_cut_bottom
        (right if on_right else left).append(p)
    right.append((x_cut_bottom, bot_y))
    left.append((x_cut_top, top_y))
    return right, left


def _centered(pts):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    c = ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)
    return c, [[round(p[0] - c[0], 1), round(p[1] - c[1], 1)] for p in pts]


# --- la sangle rouge (S06) : enserre aussi la pastille « 5 % » (qu'elle ne coupe plus) ---
SANGLE_C, SANGLE_W, SANGLE_H, SANGLE_R = (557, 699), 590, 342, 30   # x 262-852, y 528-870
_loop = _round_rect_perimeter(SANGLE_W, SANGLE_H, SANGLE_R)
_cut_b = SANGLE_NOEUD[0] - SANGLE_C[0]
_half_r, _half_l = _split_loop(_loop, _cut_b, -_cut_b)
_cr, SANGLE_D_PTS = _centered(_half_r)
_cl, SANGLE_G_PTS = _centered(_half_l)
SANGLE_D_C = (round(SANGLE_C[0] + _cr[0], 1), round(SANGLE_C[1] + _cr[1], 1))
SANGLE_G_C = (round(SANGLE_C[0] + _cl[0], 1), round(SANGLE_C[1] + _cl[1], 1))
NOEUD_R = 16


# ---------- raccords ----------
_OFF = lambda *ids: {i: {"scale": 0} for i in ids}   # noqa: E731
_FULL = lambda id, t: {id: {"chars": len(t.replace(chr(10), ""))}}   # noqa: E731

ENTRY_P2 = {   # fin de S07 = etat_initial de S08 (image 905)
    "marqueur": {"pos": [MARKER_CX, MARKER_Y], "scale": 1, "on": 1, "active": 0, "lbl": 1,
                 "done0": 0, "done1": 0, "done2": 0, "icon0": 0, "icon1": 1, "icon2": 1},
    "promesse1": {"pos": list(PROMESSE_POINT), "scale": 1},
    **_FULL("promesse1_mot", T_PROMESSES[0]), **_FULL("promesse2_mot", T_PROMESSES[1]),
    **_FULL("promesse3_mot", T_PROMESSES[2]),
    "coche_ronde": {"scale": 1}, "ast2": {"scale": 1}, "ast3": {"scale": 1},
    "etiquette": {"pos": list(ETIQ_COLLEE), "scale": ETIQ_COLLEE_K},
    "etiq_ast": {"scale": 1}, "sous_conditions": {"opacity": 0},
    "ficelle_etiquette": {"from": 1},
    "bouclier": {"pos": list(BOUCLIER_BOITE), "scale": 1},
    "produit": {"pos": list(PRODUIT_C), "scale": 1},
    **_OFF("promesse2", "promesse3", "pastille", "ast1", *PIECES, "sangle", "sangle_g", "sangle_d", "noeud",
           *FAUSSES_COCHES, "q_toi", *Q_ETAPES, "signature", "mot_signature", "produit_nom"),
}
ENTRY_P3 = {   # fin de S15 = etat_initial de S16 (image 1810)
    "marqueur": {"pos": [MARKER_CX, MARKER_Y], "scale": 1, "on": 1, "active": 2, "lbl": 1,
                 "done0": 1, "done1": 1, "done2": 0, "icon0": 1, "icon1": 1, "icon2": 0},
    "promesse3": {"pos": list(PROMESSE_POINT), "scale": 1},
    "ast1": {"scale": 1}, "ast2": {"scale": 1}, "ast3": {"scale": 1}, "coche_ronde": {"scale": 1},
    "etiquette": {"pos": list(ETIQ_COLLEE), "scale": ETIQ_COLLEE_K},
    "produit": {"pos": list(PRODUIT_C), "scale": 1},
    "piece1": {"pos": list(PIECE_EXTRAITE), "scale": 1, "fill": LIGHT.lower()},
    "frise": {"pos": list(FRISE_C), "scale": 1, "value": 0, "w": FRISE_W},
    "calendrier": {"pos": list(CAL_C), "scale": 1},
    "signature": {"pos": list(SIGNATURE_FRISE), "scale": SIGNATURE_K_FRISE},
    "mot_signature": {"pos": list(MOT_SIGNATURE_FRISE), "scale": 1, "chars": len(T_SIGNATURE)},
    "mot_echeance": {"scale": 1, "chars": len(T_ECHEANCE)},
    "bouclier": {"pos": list(BOUCLIER_ECHEANCE), "scale": BOUCLIER_K_ECHEANCE},
    "pastille": {"scale": 0},
    **_OFF("promesse1", "promesse2", "piece2", "piece3", "piece4", "piece5", "hors_frais", "panier", "boost",
           "boost_pill", "q_frise", "cadre_court", "cadre_long", "apres", "axes", "courbe_passe", "aujourdhui",
           *BRANCHES, "mot_passe", "mot_futur", "silhouette", "creux", "fil_garant", "fil_onde", "q_garant",
           *GARANT_PILLS, "bouclier_vide", "curseur", "fissure"),
}


def cast(S, kit):
    """Toute la distribution, à son état de l'image 0. Ce qui arrive plus tard : scale=0 (ou draw=0, chars=0).
    Seuls `fin` et `fin_curseur` naissent dans kit.outro (p3)."""

    # --- la boîte du produit (bas gauche), sa fente, son étiquette « Produit » ; bac et lèvre (S20) ---
    kit.shape("produit", list(PRODUIT_C), kind="round", w=PRODUIT_W, h=PRODUIT_H, r=16, fill=PAPER, stroke=INK, sw=4,
              shadow=6, z=6)
    kit.shape("fente", list(FENTE_LOCAL), kind="round", w=FENTE_W, h=FENTE_H, r=6, fill=INK, stroke=INK, sw=0,
              shadow=0, z=6.1, parent="produit")
    pill(S, "produit_nom", PRODUIT_NOM_LOCAL, T_PRODUIT, size=30, fill=PAPER, h=50, z=6.2, parent="produit", scale=1,
         shadow=3)
    kit.shape("bac", list(BAC_C), kind="round", w=BAC_W, h=BAC_H, r=8, fill=PAPER, stroke=INK, sw=4, shadow=4, z=5.9,
              scale=0)
    kit.shape("levre", list(LEVRE_C), kind="round", w=LEVRE_W, h=LEVRE_H, r=7, fill=PAPER, stroke=INK, sw=4, shadow=0,
              z=6.05, scale=0)

    # --- l'étiquette de l'offre : carte, trou, « * sous conditions », grand « * » (collée), ficelle, reflet ---
    kit.shape("etiquette", list(ETIQ_C), kind="round", w=ETIQ_W, h=ETIQ_H, r=ETIQ_R, fill=PAPER, stroke=INK, sw=4,
              shadow=6, z=8)
    kit.shape("etiquette_trou", list(TROU_LOCAL), kind="circle", w=2 * TROU_R, fill=BG, stroke=INK, sw=4, shadow=0,
              z=8.1, parent="etiquette")
    kit.text("sous_conditions", list(SOUS_COND_LOCAL), T_SOUS_COND, size=28, weight=600, z=8.2, parent="etiquette",
             typed=True)
    kit.text("etiq_ast", [0, 40], T_AST, size=ETIQ_AST_SIZE, weight=800, z=8.2, parent="etiquette", scale=0)
    S.add("ficelle_etiquette", "wire", z=7, a={"id": "etiquette", "at": list(TROU_LOCAL)},
          b={"id": "produit", "at": list(PRODUIT_COIN_HG_LOCAL)}, color=INK, sw=4)
    S.set("ficelle_etiquette", draw=1, sag=30)
    S.set("ficelle_etiquette", **{"from": 0})
    S.add("reflet", "sheen", z=8.5, w=ETIQ_W, h=ETIQ_H)
    S.set("reflet", pos=list(ETIQ_C), p=0)
    S.add("reflet_promesses", "sheen", z=8.5, w=PROMESSE_W, h=280, under=True)
    S.set("reflet_promesses", pos=[560, 610], p=0)
    for k, eid in enumerate(ECLATS):           # S02 : éclats aux coins de l'étiquette
        S.add(eid, "burst", z=8.6, r0=14, r1=46, n=8, sw=5, color=DEEP, a0=22 * k)
        S.set(eid, pos=[[760, 492], [196, 868]][k], p=0)

    # --- les trois promesses (objet du fil) : pill cyan, pictogramme et mot enfants (mot tapé), marques ---
    for k, (pid, label, icon) in enumerate(zip(PROMESSES, T_PROMESSES, PROMESSE_ICONES)):
        dy = (k - 1) * 90
        S.add(pid, "pill", z=9, text=label, w=PROMESSE_W, h=PROMESSE_H, size=PROMESSE_SIZE, weight=700, fill=CYAN,
              shadow=6, sheen={"id": "reflet_promesses", "w": PROMESSE_W, "h": 280, "dx": 0, "dy": dy})
        S.set(pid, pos=list(PROMESSES_ETIQ[k]), scale=1, opacity=1, fill=CYAN, w=PROMESSE_W, text=label, textOp=0)
        kit.icon(f"{pid}_icone", list(PROMESSE_ICONE_LOCAL), icon, s=PROMESSE_ICONE_S, z=9.2, parent=pid)
        kit.text(f"{pid}_mot", list(PROMESSE_MOT_LOCAL), label, size=PROMESSE_SIZE, weight=700, z=9.2, parent=pid,
                 typed=True)
    kit.icon("coche_ronde", list(COCHE_RONDE_LOCAL), "check", disc=COCHE_RONDE_R, fill=PAPER, shadow=3, z=9.3,
             parent="promesse1", scale=0)
    for k in (2, 3):
        kit.text(f"ast{k}", list(AST_LOCAL[k]), T_AST, size=AST_SIZE, weight=800, z=9.3, parent=f"promesse{k}",
                 scale=0)
    kit.text("ast1", list(AST1_LOCAL), T_AST, size=AST_SIZE, weight=800, z=9.3, parent="promesse1", scale=0)
    for k, lid in enumerate(LIENS):             # S03 : pointillés deep du pictogramme à la légende de l'étape
        S.add(lid, "wire", z=8.7, color=DEEP, sw=5, dash=[2, 11])
        S.set(lid, pa=[PROMESSES_ETIQ[k][0] + PROMESSE_ICONE_LOCAL[0], PROMESSES_ETIQ[k][1] - 26],
              pb=[DISQUES[k][0], LEGENDE_BAS + 4], draw=0, sag=0)
        S.set(lid, **{"from": 0})

    # --- la pastille « 5 % » (au-dessus de la sangle : z 9,82) et son « * » ---
    kit.shape("pastille", list(PASTILLE_S01), kind="circle", w=2 * PASTILLE_R0, fill=CYAN, stroke=INK, sw=4,
              shadow=6, z=9.82, scale=0, rot=PASTILLE_ROT0)
    S.set("pastille", fill=CYAN)
    kit.text("pastille_mot", [0, 0], T_5, size=52, weight=800, z=9.83, parent="pastille")
    S.set("pastille_mot", text=T_5)
    kit.text("pastille_ast", list(PASTILLE_AST_LOCAL), T_AST, size=round(AST_SIZE / PASTILLE_K_QPCT), weight=800,
             z=9.84, parent="pastille", scale=0)
    kit.shape("fantome", list(PLACE_GAIN_C), kind="circle", w=2 * PLACE_GAIN_R, fill=CYAN, stroke=DEEP, sw=4,
              shadow=0, z=10.9, scale=0, opacity=0.55)             # S18 : le « 5 % » fantôme dans la 5e place
    kit.text("fantome_mot", [0, 0], T_5, size=26, weight=800, z=10.95, parent="fantome")

    # --- la sangle rouge (S06) : contour tracé, deux moitiés (relais à la coupure), nœud, fausses coches ---
    kit.shape("sangle", list(SANGLE_C), kind="round", w=SANGLE_W, h=SANGLE_H, r=SANGLE_R, fill="none", stroke=RED,
              sw=6, shadow=0, z=9.8, draw=0)
    for sid, c, pts in (("sangle_g", SANGLE_G_C, SANGLE_G_PTS), ("sangle_d", SANGLE_D_C, SANGLE_D_PTS)):
        kit.shape(sid, list(c), kind="poly", pts=pts, closed=False, fill="none", stroke=RED, sw=6, shadow=0, z=9.8,
                  scale=0)
    kit.shape("noeud", list(SANGLE_NOEUD), kind="circle", w=2 * NOEUD_R, fill=RED, stroke=INK, sw=3, shadow=3,
              z=9.9, scale=0)
    for fid in FAUSSES_COCHES:
        kit.icon(fid, list(PROMESSES_ETIQ[0]), "check", disc=COCHE_RONDE_R, fill=PAPER, shadow=3, ringColor=RED,
                 z=9.95, scale=0)
        S.set(fid, ring=1)

    # --- le rond de signature (S04 ; départ de la barre en S10) et son mot ---
    kit.icon("signature", list(SIGNATURE_C), "sign", disc=SIGNATURE_R, fill=PAPER, shadow=3, z=9.2, scale=0)
    kit.text("mot_signature", list(MOT_SIGNATURE_C), T_SIGNATURE, size=34, weight=700, z=9, typed=True)

    # --- la barre de temps « Signature -> Échéance » (S10-S19, élargie) et ses ajouts ---
    kit.gauge("frise", list(FRISE_C), value=0, w=FRISE_W, h=FRISE_H, fill=CYAN, empty=PAPER, sw=4, shadow=6, z=9,
              scale=0)
    S.set("frise", fill=CYAN, w=FRISE_W, h=FRISE_H)
    kit.icon("calendrier", list(CAL_C), "cal", disc=CAL_R, fill=CYAN, shadow=5, z=9.2, scale=0)
    kit.text("mot_echeance", list(MOT_ECHEANCE_C), T_ECHEANCE, size=34, weight=700, z=9, typed=True)
    kit.shape("curseur", list(SIGNATURE_FRISE), kind="circle", w=2 * CURSEUR_R, fill=DEEP, stroke=INK, sw=3,
              shadow=3, z=9.25, scale=0)
    kit.shape("cadre_long", list(CADRE_LONG_C), kind="round", w=CADRE_LONG_W, h=CADRE_LONG_H, r=22, fill=LIGHT,
              stroke=INK, sw=6, shadow=0, z=8.8, draw=0)
    kit.shape("cadre_court", list(CADRE_COURT_C), kind="round", w=CADRE_COURT_W, h=CADRE_COURT_H, r=16, fill=LIGHT,
              stroke=DEEP, sw=6, shadow=0, z=8.85, draw=0)
    kit.shape("boost", [BOOST_X0, FRISE_Y], kind="round", w=BOOST_X1 - BOOST_X0, h=FRISE_H, r=14, fill=CYAN,
              stroke=INK, sw=4, shadow=0, z=9.1, scale=0)
    S.set("boost", w=BOOST_X1 - BOOST_X0)
    _bw = round(text_width(T_BOOSTE, 34, 700) + 48 + 30)
    S.add("boost_pill", "pill", z=9.5, text=T_BOOSTE, w=_bw, h=58, size=34, weight=700, fill=LIGHT, shadow=4)
    S.set("boost_pill", pos=list(BOOST_PILL_C), scale=0, opacity=1, fill=LIGHT, w=_bw)
    kit.icon("boost_fleche", [-_bw / 2 + 32, 0], "arrow", s=30, z=9.6, parent="boost_pill", rot=-90)
    kit.shape("apres", [(APRES_X0 + APRES_X1) / 2, FRISE_Y], kind="poly",
              pts=[[-(APRES_X1 - APRES_X0) / 2, 0], [(APRES_X1 - APRES_X0) / 2, 0]], closed=False, fill="none",
              stroke=INK, sw=6, dash=[16, 12], shadow=0, z=9.15, draw=0)
    kit.shape("repere", list(REPERE_C), kind="poly", pts=[[0, -REPERE_H / 2], [0, REPERE_H / 2]], closed=False,
              fill="none", stroke=INK, sw=6, shadow=0, z=9.5, draw=0)

    # --- le bouclier de la garantie, son double en tirets (S10), son onde, son encoche ---
    kit.icon("bouclier", list(BOUCLIER_BOITE), "shield", disc=BOUCLIER_R0, fill=CYAN, shadow=6, z=10.5, scale=0)
    kit.shape("encoche", [0, -BOUCLIER_R0 + 4], kind="poly", pts=[[-12, -8], [0, 10], [12, -8]], closed=True, fill=BG,
              stroke=INK, sw=3, shadow=0, z=10.55, parent="bouclier", scale=0)
    kit.shape("bouclier_vide", list(BOUCLIER_COUVERCLE), kind="circle", w=2 * BOUCLIER_R0, fill="none", stroke=INK,
              sw=4, dash=[12, 9], shadow=0, z=10.5, scale=0)
    kit.icon("bouclier_vide_icone", [0, 0], "shield", s=round(BOUCLIER_R0 * 1.15), z=10.52, parent="bouclier_vide",
             opacity=0.9)
    kit.shape("onde_bouclier", list(BOUCLIER_COUVERCLE), kind="circle", w=2 * BOUCLIER_R0 + 16, fill="none",
              stroke=DEEP, sw=5, shadow=0, z=10.45, opacity=0)

    # --- les garants (S08-S10) : silhouette vide et sa place en tirets, fil (et son onde), trois immeubles ---
    kit.shape("silhouette", list(SILHOUETTE_C), kind="poly", pts=SILHOUETTE_PTS, closed=True, fill="none",
              stroke=DEEP, sw=4, dash=[14, 10], shadow=0, z=11.8, draw=0)
    kit.shape("creux", list(CREUX_C), kind="circle", w=2 * CREUX_R, fill="none", stroke=DEEP, sw=4, dash=[8, 7],
              shadow=0, z=11.85, scale=0)
    for wid, col, sw in (("fil_garant", INK, 4), ("fil_onde", DEEP, 9)):
        S.add(wid, "wire", z=10.4 if wid == "fil_garant" else 10.42, color=col, sw=sw)
        S.set(wid, pa=list(FIL_BAS), pb=list(FIL_HAUT_S08), draw=0, sag=0, via=list(FIL_COUDE))
        S.set(wid, **{"from": 0})
    garants = []
    for k, gid in enumerate(GARANTS):
        g = Figure(kit, gid, pos=list(GARANTS_C[k]), scale=GARANT_K, variant="societe", side="right", tool=False,
                   z=12, show=False)
        S.set(gid, look=1)
        garants.append(g)
        pill(S, GARANT_PILLS[k], (GARANTS_C[k][0], GARANT_PILLS_Y), T_GARANTS[k], size=34, fill=LIGHT, h=58, z=12.5,
             scale=0, shadow=4)
    kit.shape("fissure", [0, 0], kind="poly", pts=FISSURE_PTS, closed=False, fill="none", stroke=INK, sw=7, shadow=0,
              z=12.3, parent="emetteur", draw=0)

    # --- les « ? » (questions de « Toi ») ---
    for k, qid in enumerate(Q_ETAPES):
        S.add(qid, "qmark", z=17)
        S.set(qid, pos=[DISQUES[k][0], 455], scale=0, opacity=1, gs=60, rot=(-10, 0, 10)[k])
    S.add("q_toi", "qmark", z=17)
    S.set("q_toi", pos=[P2[0], 915], scale=0, opacity=1, gs=100)
    S.add("q_garant", "qmark", z=17)
    S.set("q_garant", pos=list(BOUCLIER_TAP), scale=0, opacity=1, gs=60)
    S.add("q_frise", "qmark", z=17)
    S.set("q_frise", pos=list(Q_FRISE_C), scale=0, opacity=1, gs=80)
    for k, qid in enumerate(Q_LIGNES):
        S.add(qid, "qmark", z=17)
        S.set(qid, pos=list(TOI_TETE["P1"]), scale=0, opacity=1, gs=44)

    # --- le graphique passé / futur (S13, plein cadre) ---
    kit.shape("axes", list(AXES_C), kind="poly", pts=AXES_PTS, closed=False, fill="none", stroke=INK, sw=6, shadow=0,
              z=9, draw=0)
    kit.curve("courbe_passe", list(COURBE_C), COURBE_PTS, draw=0, color=DEEP, sw=8, smooth=False, dot=False, z=9.1)
    kit.shape("aujourdhui", list(AUJOURDHUI_C), kind="poly", pts=AUJOURDHUI_PTS, closed=False, fill="none",
              stroke=INK, sw=5, dash=[14, 10], shadow=0, z=9, draw=0)
    for bid, end in zip(BRANCHES, BRANCHES_FIN):
        c = ((AUJOURDHUI[0] + end[0]) / 2, (AUJOURDHUI[1] + end[1]) / 2)
        pts = [[AUJOURDHUI[0] - c[0], AUJOURDHUI[1] - c[1]], [end[0] - c[0], end[1] - c[1]]]
        kit.curve(bid, list(c), pts, draw=0, color=DEEP, sw=5, smooth=False, dot=False, dash=[16, 11], z=9.1)
    kit.text("mot_passe", list(MOT_PASSE_C), T_PASSE, size=34, weight=700, z=9, typed=True)
    kit.text("mot_futur", list(MOT_FUTUR_C), T_FUTUR, size=34, weight=700, z=9, typed=True)

    # --- les 5 pièces de « Toi » (pile au sol), la place du gain, « hors frais », « −1 », « rien gagné » ---
    for k, pid in enumerate(PIECES):
        kit.icon(pid, list(PILE[k]), "euro", disc=PIECE_R, fill=LIGHT, shadow=3, z=11 + 0.01 * k)
        S.set(pid, fill=LIGHT)
    kit.shape("place_gain", list(PLACE_GAIN_C), kind="circle", w=2 * PLACE_GAIN_R, fill="none", stroke=INK, sw=4,
              dash=[10, 8], shadow=0, z=11, scale=0)
    kit.text("place_gain_plus", [0, 0], T_PLUS, size=40, weight=800, z=11.1, parent="place_gain")
    kit.text("hors_frais", list(HORS_FRAIS_C), T_HORS_FRAIS, size=34, weight=700, color=RED, z=11, scale=0)
    kit.text("moins1", list(MOINS1_C), T_MOINS1, size=40, weight=800, color=RED, z=11.2, scale=0)
    kit.text("rien_gagne", list(RIEN_GAGNE_C), T_RIEN_GAGNE, size=34, weight=700, z=11, typed=True)

    # --- les freins à la sortie (S15-S17) : panier, cadenas, « Durée », « Pénalités », cadran, « Délai » ---
    kit.icon("panier", list(PANIER_C), "cart", disc=PANIER_R, fill=PAPER, shadow=3, z=16.5, scale=0)
    kit.icon("cadenas", list(CADENAS_C), "lock", disc=CADENAS_R, fill=PAPER, shadow=6, z=11.5, scale=0)
    S.set("cadenas", ring=0)
    kit.text("mot_duree", list(MOT_DUREE_C), T_DUREE, size=34, weight=700, z=9.5, typed=True)
    kit.text("mot_penalites", list(MOT_PENALITES_C), T_PENALITES, size=34, weight=700, color=RED, z=11, scale=0)
    kit.sector("horloge", list(HORLOGE_C), start=0, value=0, r=HORLOGE_R, face=PAPER, fill=LIGHT, ticks=12,
               hand=True, sw=4, shadow=4, z=10.8, scale=0)
    kit.text("mot_delai", list(MOT_DELAI_C), T_DELAI, size=34, weight=700, z=11, scale=0)

    # --- la formule « Protégé = sans risque » (groupe), le « = » rouge, le trait qui le barre ---
    group(kit, "mythe", MYTHE_C, z=9, scale=1)
    for k, (mid, t) in enumerate(zip(MYTHE_MOTS, T_MYTHE)):
        kit.text(mid, list(MYTHE_LOCAL[k]), t, size=MYTHE_SIZE, weight=800, color=RED if k == 1 else INK,
                 anchor="start", z=9.1, parent="mythe", typed=True)
    S.set("mythe_egal", color=RED)
    kit.shape("barre_egal", [0, 0], kind="poly", pts=BARRE_EGAL_PTS, closed=False, fill="none", stroke=DEEP, sw=6,
              shadow=0, z=9.2, parent="mythe", draw=0)

    # --- le ◀◀ (S19) ---
    kit.icon("rembobiner", list(REMBOBINER_C), "rewind", disc=REMBOBINER_R, fill=CYAN, shadow=6, z=18, scale=0)

    # --- la fiche « 4 questions » (S19-S22), ses réponses écrites, le « * » de la 4e puce, les coches de « Toi » ---
    lignes = FICHE.add(kit, "fiche", [(q, "", ic) for q, ic in zip(T_QUESTIONS, QUESTION_ICONES)], list(FICHE_C),
                       title=T_FICHE_TITRE, z=8.3, typed=True, show=False)
    for lid in lignes:
        S.set(lid, bulletOn=0)
    bx, by = FICHE.pt(3, "bullet", "row")
    kit.text("fiche_ast", [bx, by + 12], T_AST, size=FICHE_AST_SIZE, weight=800, z=9.6, parent="fiche", scale=0)
    ty = FICHE.ty + 2
    for k, rid in enumerate(REPONSES):
        w = round(text_width(T_REPONSES[k], REPONSE_SIZE, 700) + 36 + 30)
        pill(S, rid, (REPONSE_DROITE - w / 2, FICHE.rows[k] + ty), T_REPONSES[k], size=REPONSE_SIZE, weight=700,
             fill=LIGHT, h=REPONSE_H, z=10.4, parent="fiche", scale=0, w=w, shadow=3, icon=REPONSE_ICONES[k])
    for k, cid in enumerate(COCHES):
        kit.tick(cid, [COCHE_FICHE_X, FICHE.rows[k] + ty], DEEP, size=34, sw=8, z=11.3, parent="fiche")

    # --- les fils « * » -> réponse (S21), deep 5 px, qui contournent les pilules par la droite ---
    for k, (wid, src, r) in enumerate(zip(FICELLES, FICELLE_DE, FICELLE_VERS)):
        w = S.ents[REPONSES[r]]["p"]["w"]
        S.add(wid, "wire", z=9.25, a={"id": src, "at": [0, AST_VIS_DY]}, b={"id": REPONSES[r], "at": [w / 2 - 6, 0]},
              color=DEEP, sw=5)
        S.set(wid, draw=0, sag=0, via=list(VIAS[k]))
        S.set(wid, **{"from": 0})

    # --- le repère 1-2-3 légendé : grands disques, pictogramme de la promesse rangée, « * » des étapes vues ---
    kit.steps_marker(MARKER_LABELS, y=MARKER_Y, cx=MARKER_CX, gap=MARKER_GAP, z=20)
    S.ents["marqueur"]["p"].update(moveBlank=True, labelSize=MARKER_LABEL_SIZE, labelDy=MARKER_LABEL_DY,
                                   doneStyle="kept", doneMark="asterisk", discR=MARKER_R, activeR=MARKER_ACTIVE_R,
                                   digitSize=30, activeDigitSize=40, icons=list(PROMESSE_ICONES))
    S.set("marqueur", scale=0, on=0, done0=0, done1=0, done2=0, lbl=0, icon0=0, icon1=0, icon2=0)

    # --- S22 : ondes du toucher du stylo sur le bouton ---
    for k in range(2):
        kit.shape(f"fin_onde{k + 1}", list(FIN_TAP), kind="circle", w=70, fill="none", stroke=DEEP, sw=6, shadow=0,
                  z=43.5, opacity=0)

    # --- « Toi » (bras gauche), bras baissé dès l'image 0, et son nom (enfant : il le suit) ---
    toi = Figure(kit, "toi", pos=list(P1), scale=TOI_SCALE, side="left", z=15)
    toi.low_grip = TOI_LOW_GRIP
    S.set("toi", look=0)
    G, rot = toi.low_pose(0)
    S.set(toi.pen, pos=[round(G[0], 3), round(G[1], 3)], rot=round(rot, 3))
    S.set(toi.arm, elbow=[round(v, 3) for v in solve_ik(toi._shoulder(0), G, toi.l1, toi.l2, toi.bend)[0]])
    pill(S, "nom_toi", NOM_TOI_LOCAL, T_TOI, size=34, fill=LIGHT, h=NOM_TOI_H, w=NOM_TOI_W, z=15.2, parent="toi",
         scale=1, shadow=3)

    return SimpleNamespace(toi=toi, garants=garants, assureur=garants[0], banque=garants[1], emetteur=garants[2],
                           promesses=PROMESSES, promesse_mots=PROMESSE_MOTS, promesse_icones=PROMESSE_ICONES_IDS,
                           pieces=PIECES, q_etapes=Q_ETAPES, q_lignes=Q_LIGNES, garant_pills=GARANT_PILLS,
                           branches=BRANCHES, fiche=FICHE, lignes=lignes, reponses=REPONSES, coches=COCHES,
                           fausses_coches=FAUSSES_COCHES, mythe_mots=MYTHE_MOTS)


def build(S):
    kit = Kit(S)
    c = cast(S, kit)
    only = [p for p in os.environ.get("WTH_PARTS", "").split(",") if p]   # WTH_PARTS=p2 : cette partie seule
    for name in PARTS:
        if not only or name in only:
            importlib.import_module(f".{name}", __name__).part(S, kit, c)
