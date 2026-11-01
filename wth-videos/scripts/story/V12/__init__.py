"""V12 « L’inflation : la perte que tu ne vois pas » : mise en scène Story, en paquet (une partie par fichier).

Storyboard : scripts/storyboards/V12.json (v1, révisé après le test sans son, 22 scènes, 101 temps forts, 95,755 s),
version lisible scripts/storyboards/V12.md. Voix : build/V12/words.json (film : images 0-2872, FILM_END = 2873).
Fil : la pilule cyan « 10 000 € » (`cash`, pill 250 x 80, ExtraBold 48) : sur la carte « Solde » dès l'image 0, reliée
au panier qu'elle achète (S02), égalée puis dépassée par le pouvoir d'achat qui fond (S08-S09), cerclée « toujours »
(S10), descend avec la carte en bas à gauche et donne naissance aux 10 billets (S11), un dernier billet en sort pour
dormir sans mission (S21), devient le bouton « S’abonner » de la carte de fin (S22).
Parti pris : un seul instrument de mesure, le panier de courses (10 articles) ; la pilule ne bouge jamais pendant que
le panier se vide ; puis les billets reçoivent un rôle (bouée, valise, arbre) ou n'en reçoivent pas (berceau).
Pas d'IA dans ce film : « Toi » (figurine encre) est seul à tenir le stylo.

Parties (scènes contiguës ; poids : temps forts et secondes) :
- p1 : S01-S08, images 0-969 (36 temps forts, 32,3 s). Solde et panier, inflation nommée, 100 € -> 102 €, relevé muet,
  exemple sur 10 ans (dérive jusqu'à l'image 956).
- p2 : S09-S14, images 970-1862 (30 temps forts, 29,8 s). ≈ 8 200 €, « toujours », grand relais (S11) vers les
  billets, bouée / valise, bascule, berceau.
- p3 : S15-S22, images 1863-2872 (35 temps forts, 33,7 s). Panier du berceau, 10 / 20 ans, ligne des horizons,
  imprévu payé, arbre, courbe, tableau, billet rouge, fin.
ENTRY_P2 et ENTRY_P3 sont le contrat des raccords (kit.pin(f0 - 1, …)). Les figurines n'y sont jamais.

Aucune entité nouvelle : tout se compose avec le catalogue (storyboard : entites_nouvelles = []).
- Panier : shape poly (corbeille) + anse (poly ouvert) + 2 roues (circle), enfants ; articles b1-b10 = gauge dir up
  (fill light, empty paper ; b5 rougit : piste fill en hex) ; places perdues vide4/5/9/10 = shape round en tirets rouges.
- Étiquette des prix : png TAG + compteur `etiq_prix` et texte `etiq_taux` enfants, inclinés comme sa face.
- Flèche de la mission : wire (pa/pb) + pointe triangle (shape poly) ; flèches de hausse : icon arrow (rot -90).
- Billets : shape round cyan + rond papier + « € » (enfants) ; le billet sans mission rougit (fill en hex).
- Pilules de rôle : capsules (shape round + texte enfant, piste `under` du texte) ; pilules « ? » : shape round en
  tirets + texte « ? » (stroke / color en hex pour le rouge de S21) ; « Progresser » relaie la pilule « ? » en fondu.
- Barre du temps : `temps` (S08-S10, 10 cases de 40 px) et `temps_long` (S15-S16, cases de 20 px, segPx) ; le repère
  « Court » / « Long » = deux gauges sans cases (`court`, `long`) qui relaient les morceaux de la barre cassée (S17).
- Toucher de fin (pas de flèche de souris) : `fin_doigt` + `fin_onde1-2` (comme V02 / V03), le curseur de kit.outro
  est rendu invisible (opacity 0).

TOUR DE REVUE 1 : regard en cône translucide (shape poly, fillOp) ; articles en ART_FILL ; piles en escalier ; valise
nettoyée (SUITCASE_V12.png : carte d'embarquement effacée, clean_png) ; étiquette sans ombre, face mesurée (+2 %) ;
fils deep bouclier -> rôles (S13) et pile -> morceau de barre (S20) ; coches deep (S21) ; CAPTION_GROUPS.
Voix : build/V12/words.json refait par `python3 -m pipeline.words V12 --trim-pauses` (fins de « par » et « un »
ramenées au début des pauses mesurées ; débuts et temps forts identiques).

ÉCARTS DE PLACE (raisons de mise en page, aucun sens changé) :
- étiquette TAG.png 240 px de large (et non 220) : sa face (≈ 150 px) porte « + 2 % / an » en Bold 30 (146 px) ;
  accrochée au panier en S08-S10 à l'échelle 1 (et non 0,8) en (300, 610), pour que ce texte se lise à 30 px ; la
  pilule « inflation » au-dessus en (300, 495) ; en S15-S19 ×0,6 en (850, 770) (et non 858 : ombre en deçà de x 930) ;
- pilules mesurées (text_width + 48) : « inflation » 185 px, « inflation : 2 % / an » 346 px (et non 390 : x 547-893
  à droite, le risque « x 915 » du storyboard disparaît) ; « exemple » / « exemple illustratif » en SemiBold 32 (le
  corps d'une pill est fixe) ; le ◀◀ est un pictogramme enfant (`mention_ico`) qui se réduit en S09 ;
- S15-S16 : « 10 ans » et « 20 ans » AU-DESSUS du bout de la barre (y 250 et non 350) : sous la barre, « 20 ans »
  (x 794-906, y 333-367) heurtait le « z » de 48 px en (865, 345) ;
- S17 : la pointe de « Toi » (en x 700) tire la ligne de (530, 960) à (530, 895) (65 px et non 100) : (530, 860) est à
  294 px de l'épaule, au-delà de l'allonge ; la ligne file seule ensuite jusqu'en (530, 390) ;
- S07 : le stylo se lève vers (760, 990) et non (800, 985) : à la verticale de l'épaule, le bras frôlait la tête ;
- bascule : disques et légendes en entités monde (pas enfants de la bascule, qui naît à l'échelle 0 sur le même mot) ;
  l'inclinaison les emporte par S.path + rotate_about autour du pivot (voir p2).
"""
import importlib
import math
import os
from types import SimpleNamespace

from pipeline.story import GEOM, STYLE, text_width
from pipeline.story_kit import Figure, Kit

PARTS = ["p1", "p2", "p3"]                      # S01-S08, S09-S14, S15-S22
NBSP, NNBSP = " ", " "                # espace insécable (avant « : », « % », « € »), fine insécable (milliers)
ALERT_WORDS = {"perte", "l’érosion", "risque"}  # karaoké en rouge : les seuls rouges à l'écran (places perdues S07, S10,
                                                # S16 ; creux de la courbe S19)
ACOUSTIC_SNAP = {"gap": 0.2, "window": 0.08}    # temps fort après un silence : calé sur l'attaque audible
CAPTION_GROUPS = [                              # tour 1 : pas de mot seul, pas de négation coupée (groupes sans
    ["ce que l’inflation fait", "à ton argent"],   # mot à espace insécable : « 10 ans », « 2 % » ne s'y prêtent pas)
    ["un an plus tard"],
    ["Parce que", "cette perte", "n’apparaît", "sur aucun relevé"],
    ["dont tu", "n’as pas besoin"],
    ["Alors sépare", "les horizons"],
    ["Le problème", "n’est pas le cash"],
]

# ---------- couleurs ----------
INK, CYAN, DEEP, LIGHT = STYLE["ink"], STYLE["cyan"], STYLE["deep"], STYLE["light"]
PAPER, RED, RULE, BG = STYLE["paper"], STYLE["red"], STYLE["rule"], STYLE["bg"]

# ---------- textes à l'écran (typographie française) ----------
T_CASH = f"10{NNBSP}000{NBSP}€"
T_ABONNER = "S’abonner"
T_SOLDE, T_TOI = "Solde", "Toi"
T_INTERETS = f"intérêts{NBSP}: 0{NBSP}€"
N_INTERETS = len(T_INTERETS)                    # 14 caractères (piste chars, kit.type)
T_TOUJOURS = "toujours"
T_INFL = "inflation"
T_INFL_TAUX = f"inflation{NBSP}: 2{NBSP}%{NBSP}/ an"
T_TAUX_FACE = f"+2{NBSP}%"                      # tour 1 : « / an » reste sur la pilule « inflation : 2 % / an »
T_UN_AN = f"+{NBSP}1{NBSP}an"
T_POUVOIR = "pouvoir d’achat"
T_APPROX = "≈"
T_AUJOURDHUI_EUROS = "en euros d’aujourd’hui"
T_EXEMPLE, T_EXEMPLE_ILL = "exemple", "exemple illustratif"
T_AUJ, T_10ANS, T_20ANS = "aujourd’hui", f"10{NBSP}ans", f"20{NBSP}ans"
T_COURT, T_LONG = "Court", "Long"
T_IMPREVUS, T_PROJET, T_PROGRESSER, T_Q = "Imprévus", "Projet", "Progresser", "?"
T_STABILITE, T_RENDEMENT = "stabilité", "rendement"
T_EUR = "€"
T_CASH_ROLL = f"9{NNBSP}999{NBSP}€"             # S10 « toujours » : le compteur roule et retombe sur 10 000 €
T_TOUT = "tout"
T_PRIX_0 = f"100{NBSP}€"
ART_FILL = "#9FDDEA"                            # tour 1 : partie pleine des articles, plus soutenue que LIGHT

# ---------- mise en page (1080 x 1920) ----------
X_MIN, X_MAX, Y_MIN, Y_MAX = 40, 930, 240, 1250  # composition (storyboard : y 240-1230, rien au-delà de x 930)
GROUND = 1230                                   # pied de « Toi »
FIG_BASE = GEOM["FIGURE"]["base"]               # 95
HEAD_DY = GEOM["FIGURE"]["head"]["cy"]          # -64 : centre de la tête
HEAD_R = GEOM["FIGURE"]["head"]["r"]            # 32
SHOULDER_DX, SHOULDER_DY = abs(GEOM["FIGURE"]["shoulder"][0]), GEOM["FIGURE"]["shoulder"][1]   # 30, -16
REACH_OK = 267                                  # allonge confortable (REACH x 284) à l'échelle 1


def fig_pos(x, feet=GROUND, s=1.0):
    return [x, round(feet - FIG_BASE * s, 2)]


def film_end(S):
    """Première image après le film (fin de la dernière scène du storyboard)."""
    return round(S.sb["scenes"][-1]["t_end"] * S.fps)


# --- « Toi » : P1 en bas à droite (S03-S10), P2 au centre (S11-S22) ; bras côté gauche (il fait face à gauche) ---
TOI_P1 = fig_pos(850)                           # (850, 1135) ; épaule (820, 1119) ; haut de la tête 1039
TOI_P2 = fig_pos(700)                           # (700, 1135) ; épaule (670, 1119)
NOM_LOCAL, NOM_W, NOM_H = (0, -145), 100, 56    # pilule « Toi » au-dessus de la tête : monde (850, 990)
# Tour 1 : le regard est un cône translucide deep (sommet au visage, base cachée sous le bas de la carte), et non un
# trait en tirets ; il naît du visage (pop) et y rentre (vanish).
REGARD_APEX = (836, 1048)
REGARD_PTS = [[0, 0], [-261, -243], [49, -243]]  # base en y 805, x 575-885 (sous la carte, z plus bas)
REGARD_OP = 0.2
QUESTION_S07, QUESTION_S11, Q_GS = (902, 972), (640, 900), 90   # S07 : le « ? » naît au-dessus de la tête (pas de
                                                                # stylo avant S11)

# --- la carte « Solde » (le compte) et la pilule du fil ---
COMPTE_C, COMPTE_W, COMPTE_H = (720, 680), 340, 260          # x 550-890, y 550-810 (S01-S10)
COMPTE_LOW, COMPTE_LOW_K = (380, 1080), 0.8                  # S11-S21 : x 244-516, y 976-1184
COMPTE_TXT_LOW_K = 1.25                         # tour 1 : « Solde » et sa banque gardent 34 px quand la carte est à 0,8
HOOK_K = 1.15                                   # tour 1 : S01-S03, panier et carte plus grands et plus bas (le bas de
PANIER_HOOK, COMPTE_HOOK = (300, 950), (720, 670)   # l'image n'est plus vide) ; retour en place sur S04 « Dans »
CASH_HOOK = (720, round(670 + 15 * HOOK_K))
COMPTE_ICO_LOCAL = (-108, -80)                  # pictogramme bank (monde (612, 600))
COMPTE_MOT_LOCAL = (-80, -80)                   # « Solde » ancré à gauche, juste après le pictogramme
COMPTE_FILET_LOCAL, COMPTE_FILET_W = (0, -48), 300            # filet rule en y 632
INTERETS_LOCAL = (0, 90)                        # « intérêts : 0 € » (monde (720, 770)), enfant de la carte
CASH_C, CASH_W, CASH_H = (720, 695), 250, 80    # pilule du fil, monde (pas enfant : elle quitte la carte en S22)
CASH_LOW = (380, 1092)                          # S11-S21, échelle COMPTE_LOW_K (même relation qu'à l'échelle 1)
CASH_TAP = (470, 1092)                          # S11 « Non. » : bout droit de la pilule, à portée depuis TOI_P2
CERCLE_C, CERCLE_W, CERCLE_H = (720, 695), 300, 116           # S10 : ellipse encre autour de la pilule
TOUJOURS_C = (720, 515)                         # S10 : « toujours » au-dessus de la carte
TEMPS_MINI_C, TEMPS_MINI_W = (720, 848), 200    # S10 « toujours » : mini-barre de 10 cases sous la carte (le temps
                                                # passe, le solde retombe sur 10 000 €)

# --- le panier (centre (300, 790) : corbeille haut x 120-480 en y 700, bas x 150-450 en y 870) et ses 10 articles ---
PANIER_C = (300, 790)
PANIER_PTS = [[-180, -90], [180, -90], [150, 80], [-150, 80]]
ANSE_PTS = [[-180, -90], [-234, -142]]          # poignée : du coin haut gauche vers (66, 648)
ROUES_LOCAL = [(-105, 115), (105, 115)]         # (195, 905), (405, 905), r 22
PANIER_LOW, PANIER_LOW_K = (740, 860), 0.8      # S15-S19 : b6-b10 en y 878, x 641-840
ART_XS, ART_YS, ART_W = [176, 238, 300, 362, 424], [742, 812], 56
ART_LOCAL = [(x - PANIER_C[0], y - PANIER_C[1]) for y in ART_YS for x in ART_XS]   # b1-b5 puis b6-b10
ARTICLES = [f"b{i + 1}" for i in range(10)]
VIDES = {"vide4": 3, "vide5": 4, "vide9": 8, "vide10": 9}  # place perdue -> indice de l'article (b4, b5, b9, b10)
HAUSSE_LOCAL_Y = 672 - PANIER_C[1]              # petites flèches ↑ au-dessus des colonnes (monde y 672)
HAUSSE = [f"hausse{i + 1}" for i in range(5)]   # hausse5 au-dessus de b5 (S02) ; hausse1-4 en S05
HAUSSE_GRANDE_C = (720, 300)                    # S05 « hausse » : grande flèche (110 px) à droite de l'étiquette
HAUSSE5_S, HAUSSE_S, HAUSSE_GRANDE_S = 64, 48, 110   # tour 1 : flèches lisibles (trait 8 / 6 / 12 px)
LIEN_A_LOCAL = (-CASH_W / 2, 0)                 # fil deep : bord gauche de la pilule (595, 695)
LIEN_B_LOCAL = (180, -85)                       # -> coin haut droit de la corbeille (480, 705)

# --- la cible (S04) et la flèche de la mission ---
CIBLE_C, CIBLE_W = (540, 330), 170
MISSION_A, MISSION_B = (700, 550), (585, 350)   # du haut de la carte au bord de l'anneau central
MISSION_ROT = round(math.degrees(math.atan2(MISSION_B[1] - MISSION_A[1], MISSION_B[0] - MISSION_A[0])), 1)

# --- l'étiquette des prix (TAG.png) et la pilule « inflation » ---
TAG_W = 240
# Tour 1 : centre de la face mesuré sur TAG.png, loin de l'œillet, et inclinaison réelle de la face (≈ 26°).
TAG_FACE_ORIG, TAG_HOLE_ORIG, TAG_BOTTOM_ORIG = (958, 562), (480, 340), (760, 800)   # pixels de TAG.png (1536 x 1024)
TAG_FACE_ROT = 26
ETIQ_DROP, ETIQ_UP = (540, 360), (540, 320)     # S05 « L’inflation, » puis « hausse »
ETIQ_LEFT, ETIQ_RIGHT = (330, 330), (720, 330)  # S06 « Quand », « coûte »
ETIQ_PANIER, ETIQ_PANIER_K = (300, 610), 1.0    # S08-S10 (écart : ×1)
ETIQ_LOW, ETIQ_LOW_K = (836, 745), 0.8          # S15-S19 (tour 1 : ×0,8 et sa pilule « inflation » au-dessus)
TAUX_LOW = (845, 655)
GHOST_C = ETIQ_LEFT                              # S06 « coûte » : la place de « 100 € » reste marquée (tirets)
TAUX_C0 = (400, 600)                            # S04 « l’inflation » : au-dessus de la flèche de b5
TAUX_UNDER_DY = 150                             # S05-S07 : pendue 150 px sous le centre de l'étiquette
TAUX_PANIER = (300, 495)                        # S08-S10 : au-dessus de l'étiquette accrochée au panier
UN_AN_C = (505, 250)                            # tour 1 : au-dessus de la flèche fantôme -> étiquette
PRIX_0, PRIX_1 = 100, 102

# --- le pouvoir d'achat chiffré (sous le panier) et la pilule « exemple » ---
POUVOIR_TITRE_C, POUVOIR_VAL_C = (300, 975), (300, 1045)
POUVOIR_APPROX_C, POUVOIR_NOTE_C = (150, 1045), (300, 1110)
POUVOIR_0, POUVOIR_1 = 10000, 8200
MENTION_C, MENTION_H = (300, 1175), 54
MENTION_ICO_LOCAL = (-92, 0)

# --- la barre du temps ---
TEMPS_C, TEMPS_W, TEMPS_H = (540, 300), 400, 40  # S08-S10 : x 340-740, 10 cases (segPx 40)
TEMPS_AUJ_END_X, TEMPS_10_X = 325, 755           # S08 : « aujourd’hui » finit en x 325, « 10 ans » part de x 755
TEMPS_LONG_C0, TEMPS_LONG_W0 = (550, 300), 200   # S15 : x 450-650, cases de 20 px
TEMPS_LONG_C1, TEMPS_LONG_W1 = (650, 300), 400   # S16 « 20 ans, » : x 450-850 (pos et w avec la même clé)
TEMPS_LONG_AUJ_END_X = 435
TEMPS_LONG_10_C, TEMPS_LONG_20_C = (650, 250), (850, 250)   # écart : au-dessus de la barre
SEP_X = 530
SEP_A, SEP_B = (SEP_X, 960), (SEP_X, 270)       # S17 : la ligne qui sépare les horizons (trait deep 6) ; tour 1 : elle
                                                # croise la barre du temps (y 300), qui casse là où elle passe
SEP_PEN_B = (SEP_X, 895)                        # S17 « sépare » : la pointe monte de 65 px, la ligne file seule
COURT_CUT, LONG_CUT = (490, 300), (690, 300)    # S17 : les deux morceaux de la barre cassée (x 450-530, 530-850)
COURT_C, COURT_W, LONG_C, LONG_W = (290, 300), 80, (700, 300), 320
COURT_MOT_C, LONG_MOT_C = (290, 355), (700, 355)

# --- les billets (ton cash) ---
BILLET_W, BILLET_H, BILLET_R = 76, 44, 8
BILLETS = [f"billet{i + 1}" for i in range(10)]               # nés de la pilule en S11
BILLET_ROWS = [(x, y) for y in (880, 935) for x in (212, 296, 380, 464, 548)]   # billet1-5 en y 880, billet6-10 en 935
ARBRE_ROWS = [(x, y) for y in (612, 668) for x in (532, 616, 700, 784, 868)]    # S11 « placer. » : au pied de l'arbre
# Tour 1 : piles en escalier (14 px en x et en y) pour qu'on compte 3 et 2 billets ; billets du berceau en éventail
# (12 px, ±6°) pour qu'on en compte 5.
PILE_BOUEE = [(176, 636), (190, 622), (204, 608)]             # billet1-3 (billet3 en haut : il paie l'imprévu, S18)
PILE_VALISE = [(393, 636), (407, 622)]                        # billet4-5
PILE_BERCEAU, PILE_BERCEAU_K = [(676 + 12 * k, 514 - 9 * k) for k in range(5)], 0.8   # billet6-10 couchés (S14-S18)
PILE_BERCEAU_ROT = [-6, -3, 0, 3, 6]
TOUT_START, TOUT_TREE = (380, 828), (425, 640)  # S11 : pilule « tout » au-dessus des billets, puis à gauche du groupe
PILE_ARBRE = [(700, 620 - 6 * k) for k in range(5)]           # S19 « progresser » : billet6-10 aux racines, échelle 1
BILLET_ARBRE_FROM, BILLET_ARBRE_C = (700, 430), (700, 590)    # S19 « argent » : le 6e billet tombe du feuillage
BILLET_DORT_C, BILLET_DORT_K = (590, 872), 1.2                # S21 : le billet sans mission, dans le berceau

# --- les lieux (PNG génériques, alpha strict, ombre de contact ; un seul entre ou sort à la fois) ---
PNG_W = {"TARGET": CIBLE_W, "TAG": TAG_W, "TREE": 220, "BUOY": 190, "SUITCASE": 130, "CRADLE": 210}
# Tour 1 : SUITCASE.png porte une carte d'embarquement cuite en bas à droite (tache grise et éclat cyan à côté de la
# valise) : copie propre à V12, carte effacée (polygone en pixels du PNG préparé), recadrée sur la valise.
SUITCASE_ERASE = [(748, 733), (1112, 693), (1169, 693), (1169, 940), (690, 940), (706, 912)]
ARBRE_C, ARBRE_S19_K = (700, 480), round(200 / 220, 4)        # S19 : 200 px
BOUEE_C, VALISE_C, BERCEAU_C = (190, 520), (400, 525), (700, 480)
BERCEAU_LOW, BERCEAU_LOW_K = (590, 880), round(180 / 210, 4)  # S21 : 180 px, à cheval sur le bas de la ligne,
                                                              # entre les deux colonnes (cash sans rôle ni durée)
ZZZ = [("zzz1", (790, 420), 32), ("zzz2", (825, 385), 40), ("zzz3", (865, 345), 48)]

# --- rôles et durées ---
ROLE_H = 54
ROLE_IMPREVUS_C, ROLE_PROJET_C, ROLE_PROG_C = (190, 690), (400, 690), (700, 690)
ROLE_VIDE_W = 100                               # S14 : pilule « ? » en tirets sous le berceau (étroite : la pilule
                                                # « inflation » de S15 tient à sa droite)
ROLE_DORT_C, ROLE_DORT_W, ROLE_DORT_H = (760, 890), 120, 50   # S21 : « ? » à droite du berceau (vire au rouge)
COCHES = [("coche1", (262, 600)), ("coche2", (466, 600)), ("coche3", (772, 600))]   # S21 : à côté des 3 piles
DUREES = [("duree1", T_COURT, (190, 755)), ("duree2", T_COURT, (400, 755)), ("duree3", T_LONG, (700, 755))]
DUREE_W, DUREE_H = 120, 54

# --- la bascule (S13) et le bouclier (S13, S18) ---
BASCULE_C, BASCULE_W, BASCULE_TILT = (700, 820), 330, -18      # sommet du pivot ; -18 (tour 1) : penche nettement
BASCULE_OVER = -20                                              # côté « stabilité », amorti par -20 puis -18
BOUCLIER_SEAT, POURCENT_SEAT, DISQUE_R = (560, 782), (840, 782), 34
BOUCLIER_BIG_K, BOUCLIER_BIG_SEAT, POURCENT_SMALL_K = 1.5, (560, 765), 0.8   # S13 « stabilité » : le poids se voit
STABILITE_C, RENDEMENT_C = (560, 720), (830, 720)
STABILITE_UP = (560, 696)
BOUCLIER_S18, BOUCLIER_S18_K = (295, 415), round(30 / 34, 4)
IMPREVU_C, IMPREVU_R = (150, 830), 50           # tour 1 : disque ⚠ r 50 (et non 34)

# --- la courbe en zigzag (S19) ---
# Tour 1 : courbe de 360 px, qui finit nettement plus haut qu'elle ne commence ; tracée jusqu'au creux sur
# « acceptant », puis repart au-dessus du creux sur « risque. ».
COURBE_C = (740, 878)
COURBE_PTS_WORLD = [(560, 955), (640, 900), (700, 920), (770, 855), (830, 935), (920, 785)]
COURBE_CREUX = (830, 935)

# --- la fin (kit.outro) : carte (540, 760), bouton 380 x 112 ; toucher au doigt, pas de flèche de souris ---
FIN_C = (540, 760)
FIN_BUTTON = (540, 908)
FIN_TAP = (684, 944)                            # bas droit du bouton, hors du libellé


def scene_f0(S, sid):
    return round(next(s for s in S.sb["scenes"] if s["id"] == sid)["t_start"] * S.fps)


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


for _x, _pt, _what in [(TOI_P2[0], CASH_TAP, "S11 pilule"),
                       (TOI_P2[0], SEP_A, "S17 départ de la ligne"), (TOI_P2[0], SEP_PEN_B, "S17 pointe en haut")]:
    assert_reach(_x, _pt, _what)


# ---------- petites fabriques ----------
def png_local(meta, w, pt_orig):
    """Point local (repère de l'entité png de largeur w) d'un pixel de l'image source (avant recadrage)."""
    x0, y0, x1, y1 = meta["crop"]
    k = w / (x1 - x0)
    return [round((pt_orig[0] - (x0 + x1) / 2) * k, 1), round((pt_orig[1] - (y0 + y1) / 2) * k, 1)]


def clean_png(S, name, erase):
    """Copie propre à V12 d'une illustration préparée par S.png : le polygone `erase` (pixels du PNG préparé) est
    rendu transparent, puis l'image est recadrée sur ce qui reste (alpha > 8). L'illustration partagée n'est pas
    touchée. -> meta (src, w, h, crop en pixels de la source)."""
    from PIL import Image, ImageChops, ImageDraw
    from pipeline.story import GENERATED, read_json, write_json
    m = S.png(name)
    out_dir = GENERATED / "story" / S.video_id
    out, info = out_dir / f"{name}_V12.png", out_dir / f"{name}_V12.json"
    key = f"{m['key']}:{erase}"
    if out.exists() and info.exists() and read_json(info).get("key") == key:
        meta = read_json(info)
    else:
        im = Image.open(out_dir / f"{name}.png").convert("RGBA")
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).polygon([tuple(q) for q in erase], fill=255)
        im.putalpha(ImageChops.subtract(im.getchannel("A"), mask))
        box = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
        im = im.crop(box)
        im.save(out)
        x0, y0 = m["crop"][0] + box[0], m["crop"][1] + box[1]
        meta = {"key": key, "w": im.size[0], "h": im.size[1], "crop": [x0, y0, x0 + im.size[0], y0 + im.size[1]]}
        write_json(info, meta)
    meta["src"] = f"generated/story/{S.video_id}/{name}_V12.png"
    S.assets[f"{name}_V12"] = meta
    return meta


def png(S, id, name, w, pos, z=5, contact=True, parent=None, scale=0, meta=None):
    """Illustration générique (verre, alpha strict), largeur w, rapport gardé. -> meta (+ h)."""
    m = meta or S.png(name)
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
    S.set(id, pos=list(pos), scale=scale, opacity=1, fill=fill, w=w, text=text)
    return w


def capsule(kit, id, pos, text, size=32, weight=700, h=ROLE_H, fill=PAPER, z=11, scale=0, shadow=4, dash=None,
            sw=4, w=None, color=INK):
    """Pilule composée : shape round (piste stroke en hex) + texte enfant `id`_mot (pistes under, color en hex).
    dash : contour en tirets (pilule « ? » sans rôle, fill none). -> largeur."""
    w = w or round(text_width(text, size, weight) + 48)
    kit.shape(id, list(pos), kind="round", w=w, h=h, r=h / 2, fill=fill, stroke=INK, sw=sw, shadow=shadow, z=z,
              scale=scale, dash=dash)
    kit.S.set(id, stroke=INK)
    kit.text(f"{id}_mot", [0, 0], text, size=size, weight=weight, z=z + 0.1, parent=id, color=color)
    kit.S.set(f"{id}_mot", color=color, under=0)
    return w


def billet(kit, id, pos, z, scale=0):
    """Billet cyan 76 x 44 (contour encre 4, ombre +4), « € » ExtraBold 28 dans un rond papier r 14 (enfants)."""
    kit.shape(id, list(pos), kind="round", w=BILLET_W, h=BILLET_H, r=BILLET_R, fill=CYAN, stroke=INK, sw=4, shadow=4,
              z=z, scale=scale)
    kit.S.set(id, fill=CYAN)                    # hex : CYAN -> RED (billet sans mission, S21)
    kit.shape(f"{id}_rond", [0, 0], kind="circle", w=28, fill=PAPER, stroke=INK, sw=2, shadow=0, z=z + 0.05,
              parent=id)
    kit.text(f"{id}_eur", [0, 1], T_EUR, size=28, weight=800, z=z + 0.08, parent=id)
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


def taux_under(etiq_pos):
    """Place de la pilule « inflation » pendue sous l'étiquette (S05-S07)."""
    return [etiq_pos[0], etiq_pos[1] + TAUX_UNDER_DY]


# ---------- raccords (contrat des parties ; couleurs en hex minuscule : S.val rend du minuscule) ----------
def _lo(c):
    return c.lower()


_OFF = lambda *ids: {i: {"scale": 0} for i in ids}   # noqa: E731

W_INFL = round(text_width(T_INFL, 34, 700) + 48)                 # 185
W_INFL_TAUX = round(text_width(T_INFL_TAUX, 34, 700) + 48)       # 346
W_EXEMPLE = round(text_width(T_EXEMPLE, 32, 600) + 48 + 36)      # place du ◀◀ à gauche
W_EXEMPLE_ILL = round(text_width(T_EXEMPLE_ILL, 32, 600) + 48)   # 323

ENTRY_P2 = {   # fin de S08 = etat_initial de S09 (image 969)
    "compte": {"pos": list(COMPTE_C), "scale": 1},
    "interets": {"scale": 1, "chars": N_INTERETS},
    "cash": {"pos": list(CASH_C), "scale": 1, "text": T_CASH, "textOp": 1},
    "panier": {"pos": list(PANIER_C), "scale": 1},
    **{b: {"scale": 1, "opacity": 1, "fill": _lo(ART_FILL), "value": 1} for b in ARTICLES},
    "b4": {"scale": 1, "opacity": 1, "fill": _lo(ART_FILL), "value": 0.2},
    "b5": {"scale": 1, "opacity": 1, "fill": _lo(ART_FILL), "value": 0},
    "vide4": {"draw": 0}, "vide5": {"draw": 1},          # tour 1 : la place de b5 vire aux tirets rouges en S08
    "lien": {"draw": 1},
    "regard": {"scale": 0},
    "mission": {"draw": 0},
    "etiquette": {"pos": list(ETIQ_PANIER), "scale": ETIQ_PANIER_K},
    "etiq_prix": {"opacity": 0}, "etiq_taux": {"opacity": 1},
    "ficelle_taux": {"draw": 0}, "ficelle_panier": {"draw": 1},
    "taux": {"pos": list(TAUX_PANIER), "scale": 1, "text": T_INFL_TAUX, "w": W_INFL_TAUX},
    "pouvoir_titre": {"scale": 1}, "pouvoir_val": {"scale": 1, "value": POUVOIR_1},
    "pouvoir_note": {"opacity": 0},
    "mention": {"pos": list(MENTION_C), "scale": 1, "text": T_EXEMPLE, "w": W_EXEMPLE},
    "mention_ico": {"scale": 1},
    "temps": {"pos": list(TEMPS_C), "scale": 1, "w": TEMPS_W, "value": 1},
    "temps_auj": {"opacity": 0}, "temps_10": {"scale": 1, "opacity": 1, "under": 0},
    "cercle": {"draw": 0}, "toujours": {"chars": 0},
    "fleche_an": {"draw": 0}, "fantome": {"scale": 0},
    **_OFF(*HAUSSE, "hausse_grande", "nom_toi", "question", "cible", "mission_pointe", "un_an", "pouvoir_approx",
           "fleche_an_pointe", "fantome_prix", "temps_mini"),
}

ENTRY_P3 = {   # fin de S14 = etat_initial de S15 (image 1862)
    "compte": {"pos": list(COMPTE_LOW), "scale": COMPTE_LOW_K},
    "compte_mot": {"scale": COMPTE_TXT_LOW_K}, "compte_ico": {"scale": COMPTE_TXT_LOW_K},
    "interets": {"scale": 0},
    "cash": {"pos": list(CASH_LOW), "scale": COMPTE_LOW_K, "text": T_CASH, "textOp": 1},
    "bouee": {"pos": list(BOUEE_C), "scale": 1},
    "valise": {"pos": list(VALISE_C), "scale": 1},
    "berceau": {"pos": list(BERCEAU_C), "scale": 1},
    **{b: {"pos": list(p), "scale": 1} for b, p in zip(BILLETS[0:3], PILE_BOUEE)},
    **{b: {"pos": list(p), "scale": 1} for b, p in zip(BILLETS[3:5], PILE_VALISE)},
    **{b: {"pos": list(p), "scale": PILE_BERCEAU_K, "rot": r}
       for b, p, r in zip(BILLETS[5:10], PILE_BERCEAU, PILE_BERCEAU_ROT)},
    "role_imprevus": {"pos": list(ROLE_IMPREVUS_C), "scale": 1},
    "role_projet": {"pos": list(ROLE_PROJET_C), "scale": 1},
    "role_vide": {"pos": list(ROLE_PROG_C), "scale": 1, "draw": 1},
    "role_vide_mot": {"opacity": 1},
    **{zid: {"pos": list(p), "scale": 1} for zid, p, _ in ZZZ},
    # le panier revient en S15 avec b6-b10 seulement : tout le reste de son monde est éteint pendant qu'il est caché
    "panier": {"scale": 0},
    **{b: {"scale": 0, "value": 1, "fill": _lo(ART_FILL), "opacity": 1} for b in ARTICLES},
    **_OFF(*VIDES, *HAUSSE),
    "lien": {"draw": 0}, "regard": {"scale": 0}, "mission": {"draw": 0},
    "fil_bouee": {"draw": 0}, "fil_valise": {"draw": 0}, "tout_barre": {"draw": 0}, "vague": {"draw": 0},
    "ficelle_taux": {"draw": 0}, "ficelle_panier": {"draw": 0},
    "etiq_prix": {"opacity": 0}, "etiq_taux": {"opacity": 1},
    **_OFF("etiquette", "taux", "un_an", "hausse_grande", "cible", "mission_pointe", "pouvoir_titre", "pouvoir_val",
           "pouvoir_approx", "pouvoir_note", "mention", "temps", "temps_auj", "temps_10", "temps_20", "temps_long",
           "cercle", "toujours", "question", "nom_toi", "arbre", "bascule", "bouclier", "pourcent", "stabilite",
           "rendement", "billet_arbre", "billet_dort", "role_progresser", "role_dort", "imprevu", "courbe",
           "courbe_creux", "court", "long", "court_mot", "long_mot", "duree1", "duree2", "duree3", "temps_mini", "tout",
           "fantome_prix", "fleche_an_pointe"),
}


def cast(S, kit):
    """Toute la distribution, à son état de l'image 0. Ce qui arrive plus tard : scale=0 (ou draw=0, chars=0,
    opacity=0). Seuls `fin` et son curseur naissent dans kit.outro (p3)."""

    # --- la carte « Solde » (enfants : pictogramme, mot, filet, « intérêts : 0 € ») ---
    kit.shape("compte", list(COMPTE_HOOK), kind="round", w=COMPTE_W, h=COMPTE_H, r=18, fill=PAPER, stroke=INK, sw=4,
              shadow=6, z=6, scale=HOOK_K)
    kit.icon("compte_ico", list(COMPTE_ICO_LOCAL), "bank", s=36, color=INK, z=6.1, parent="compte")
    kit.text("compte_mot", list(COMPTE_MOT_LOCAL), T_SOLDE, size=34, weight=700, anchor="start", z=6.1,
             parent="compte")
    kit.shape("compte_filet", list(COMPTE_FILET_LOCAL), kind="rect", w=COMPTE_FILET_W, h=3, fill=RULE, stroke="none",
              sw=0, shadow=0, z=6.1, parent="compte")
    kit.text("interets", list(INTERETS_LOCAL), T_INTERETS, size=32, weight=600, z=6.2, parent="compte", typed=True)

    # --- la pilule du fil « 10 000 € » (monde ; elle suit la carte en S11 par la même clé) ---
    pill(S, "cash", CASH_HOOK, T_CASH, size=48, weight=800, fill=CYAN, h=CASH_H, w=CASH_W, z=8, scale=HOOK_K,
         shadow=6)
    S.set("cash", textOp=1, rot=0)
    kit.shape("cercle", list(CERCLE_C), kind="ellipse", w=CERCLE_W, h=CERCLE_H, fill="none", stroke=INK, sw=5,
              shadow=0, z=9, draw=0)
    kit.text("toujours", list(TOUJOURS_C), T_TOUJOURS, size=34, weight=700, z=9, typed=True)
    kit.gauge("temps_mini", list(TEMPS_MINI_C), value=0, w=TEMPS_MINI_W, h=24, dir="right", fill=LIGHT, empty=PAPER,
              sw=3, shadow=3, segPx=20, z=7, scale=0)

    # --- le panier, ses roues, son anse, ses 10 articles, ses places perdues, les petites flèches de hausse ---
    kit.shape("panier", list(PANIER_HOOK), kind="poly", pts=PANIER_PTS, fill=PAPER, stroke=INK, sw=5, shadow=6, z=6,
              scale=HOOK_K)
    kit.shape("panier_anse", [0, 0], kind="poly", pts=ANSE_PTS, closed=False, fill="none", stroke=INK, sw=6,
              shadow=0, z=5.9, parent="panier")
    for k, q in enumerate(ROUES_LOCAL):
        kit.shape(f"panier_roue{k + 1}", list(q), kind="circle", w=44, fill=PAPER, stroke=INK, sw=4, shadow=3, z=5.9,
                  parent="panier")
    for b, q in zip(ARTICLES, ART_LOCAL):
        kit.gauge(b, list(q), value=1, w=ART_W, h=ART_W, r=8, dir="up", fill=ART_FILL, empty=PAPER, sw=4, shadow=3,
                  z=6.5, parent="panier")
        S.set(b, fill=ART_FILL)                 # hex : ART_FILL -> RED (b5, S02)
    for vid, i in VIDES.items():
        kit.shape(vid, list(ART_LOCAL[i]), kind="round", w=ART_W, h=ART_W, r=8, fill="none", stroke=RED, sw=4,
                  shadow=0, dash=[8, 6], z=6.7, parent="panier", draw=0)
    for k, hid in enumerate(HAUSSE):
        big = hid == "hausse5"                  # la cause de S02 : 64 px, trait 8 ; les quatre de S05 : 48 px, trait 6
        kit.icon(hid, [ART_XS[k] - PANIER_C[0], HAUSSE_LOCAL_Y], "arrow", s=HAUSSE5_S if big else HAUSSE_S,
                 sw=8 if big else 6, color=DEEP, rot=-90, z=6.7, parent="panier", scale=0)
    kit.icon("hausse_grande", list(HAUSSE_GRANDE_C), "arrow", s=HAUSSE_GRANDE_S, sw=12, color=DEEP, rot=-90, z=9.2,
             scale=0)

    # --- le fil du solde au panier ---
    S.add("lien", "wire", z=7.5, a={"id": "cash", "at": list(LIEN_A_LOCAL)},
          b={"id": "panier", "at": list(LIEN_B_LOCAL)}, color=DEEP, sw=5)
    S.set("lien", draw=0, sag=0, opacity=1)
    S.set("lien", **{"from": 0})

    # --- « Toi » (encre, entre en S03), son nom, son regard, son « ? » ---
    toi = Figure(kit, "toi", pos=TOI_P1, variant="ink", side="left", show=False)
    pill(S, "nom_toi", NOM_LOCAL, T_TOI, size=34, fill=LIGHT, h=NOM_H, w=NOM_W, z=15.8, parent="toi", scale=0)
    kit.shape("regard", list(REGARD_APEX), kind="poly", pts=REGARD_PTS, fill=DEEP, stroke="none", sw=0, shadow=0,
              z=5.5, scale=0)                   # sous la carte (z 6) : la base du cône se cache sous son bas
    S.set("regard", fillOp=REGARD_OP)
    S.add("question", "qmark", z=17)
    S.set("question", pos=list(QUESTION_S07), scale=0, opacity=1, gs=Q_GS)

    # --- la cible et la flèche de la mission (S04) ---
    png(S, "cible", "TARGET", PNG_W["TARGET"], CIBLE_C, z=5)
    S.add("mission", "wire", z=7.4, color=DEEP, sw=6)
    S.set("mission", pa=list(MISSION_A), pb=list(MISSION_B), draw=0, sag=0, opacity=1)
    S.set("mission", **{"from": 0})
    kit.shape("mission_pointe", list(MISSION_B), kind="poly", pts=[[6, 0], [-18, -12], [-18, 12]], fill=DEEP,
              stroke=DEEP, sw=2, shadow=0, z=7.45, rot=MISSION_ROT, scale=0)

    # --- l'étiquette des prix (TAG.png) : prix et taux sur sa face ; ses ficelles ; la pilule « inflation » ---
    tag = png(S, "etiquette", "TAG", TAG_W, ETIQ_DROP, z=9, contact=False)   # pendue : pas d'ombre au sol
    face = png_local(tag, TAG_W, TAG_FACE_ORIG)
    kit.counter("etiq_prix", face, value=PRIX_0, size=42, weight=800, suffix=" €", z=9.1, parent="etiquette")
    S.set("etiq_prix", rot=TAG_FACE_ROT)
    kit.text("etiq_taux", face, T_TAUX_FACE, size=40, weight=700, z=9.1, parent="etiquette", opacity=0,
             rot=TAG_FACE_ROT)
    S.add("ficelle_taux", "wire", z=8.8, a={"id": "etiquette", "at": png_local(tag, TAG_W, TAG_BOTTOM_ORIG)},
          b={"id": "taux", "at": [0, -28]}, color=DEEP, sw=4)
    S.set("ficelle_taux", draw=0, sag=0, opacity=1)
    S.set("ficelle_taux", **{"from": 0})
    S.add("ficelle_panier", "wire", z=8.8, a={"id": "etiquette", "at": png_local(tag, TAG_W, TAG_HOLE_ORIG)},
          b={"id": "panier", "at": [-170, -85]}, color=DEEP, sw=4)     # S15 : bAt -> [170, -85] (coin haut droit)
    S.set("ficelle_panier", draw=0, sag=0, opacity=1, bAt=[-170, -85])
    S.set("ficelle_panier", **{"from": 0})
    pill(S, "taux", TAUX_C0, T_INFL, size=34, fill=LIGHT, w=W_INFL, z=9.5)
    pill(S, "un_an", UN_AN_C, T_UN_AN, size=34, fill=LIGHT, z=9.5, icon="cal")
    # S06 « coûte » : la place de « 100 € » reste marquée (cadre en tirets incliné comme la face) ; « + 1 an » sur une
    # flèche du fantôme à l'étiquette
    kit.shape("fantome", list(GHOST_C), kind="round", w=150, h=66, r=14, fill="none", stroke=INK, sw=3, shadow=0,
              dash=[10, 8], z=8.9, rot=TAG_FACE_ROT, scale=0, draw=0)
    kit.text("fantome_prix", [0, 2], T_PRIX_0, size=34, weight=700, z=8.95, parent="fantome", opacity=0,
             color="#8E8887")
    S.add("fleche_an", "wire", z=9.3, color=DEEP, sw=4)
    S.set("fleche_an", pa=[GHOST_C[0] + 82, GHOST_C[1]], pb=[ETIQ_RIGHT[0] - 112, ETIQ_RIGHT[1] - 40], draw=0, sag=0,
          opacity=1)
    S.set("fleche_an", **{"from": 0})
    kit.shape("fleche_an_pointe", [ETIQ_RIGHT[0] - 112, ETIQ_RIGHT[1] - 40], kind="poly",
              pts=[[6, 0], [-16, -10], [-16, 10]], fill=DEEP, stroke=DEEP, sw=2, shadow=0, z=9.35, scale=0,
              rot=round(math.degrees(math.atan2(-40, ETIQ_RIGHT[0] - 112 - GHOST_C[0] - 82)), 1))

    # --- le pouvoir d'achat chiffré et la pilule « exemple » ---
    kit.text("pouvoir_titre", list(POUVOIR_TITRE_C), T_POUVOIR, size=34, weight=600, z=9, scale=0)
    kit.counter("pouvoir_val", list(POUVOIR_VAL_C), value=POUVOIR_0, size=56, weight=800, suffix=" €", z=9, scale=0)
    kit.text("pouvoir_approx", list(POUVOIR_APPROX_C), T_APPROX, size=56, weight=800, z=9, scale=0)
    kit.text("pouvoir_note", list(POUVOIR_NOTE_C), T_AUJOURDHUI_EUROS, size=34, weight=600, z=9, opacity=0)
    pill(S, "mention", MENTION_C, T_EXEMPLE, size=32, weight=600, fill=PAPER, h=MENTION_H, w=W_EXEMPLE, z=9, sw=3,
         pad=0)
    kit.icon("mention_ico", list(MENTION_ICO_LOCAL), "rewind", s=26, color=INK, z=9.1, parent="mention")

    # --- la barre du temps (S08-S10), puis la longue (S15-S16), le repère « Court » / « Long » (S17-S21) ---
    kit.gauge("temps", list(TEMPS_C), value=0, w=TEMPS_W, h=TEMPS_H, dir="right", fill=LIGHT, empty=PAPER, sw=4,
              shadow=6, segPx=40, z=9, scale=0)
    kit.shape("temps_case10", [TEMPS_C[0] + TEMPS_W / 2 - 20, TEMPS_C[1]], kind="round", w=40, h=40, r=10,
              fill=LIGHT, stroke=INK, sw=4, shadow=0, z=9.05, scale=0)   # S09 « fin, » : la dernière case bat (p2)
    kit.text("temps_auj", [TEMPS_AUJ_END_X, TEMPS_C[1]], T_AUJ, size=34, weight=600, anchor="end", z=9, opacity=0)
    kit.text("temps_10", [TEMPS_10_X, TEMPS_C[1]], T_10ANS, size=34, weight=700, anchor="start", z=9, opacity=0)
    S.set("temps_10", under=0)
    kit.text("temps_20", list(TEMPS_LONG_20_C), T_20ANS, size=34, weight=700, z=9, scale=0)
    kit.gauge("temps_long", list(TEMPS_LONG_C0), value=0, w=TEMPS_LONG_W0, h=TEMPS_H, dir="right", fill=LIGHT,
              empty=PAPER, sw=4, shadow=6, segPx=20, z=9, scale=0)
    S.add("separateur", "wire", z=9.5, color=DEEP, sw=6)
    S.set("separateur", pa=list(SEP_A), pb=list(SEP_B), draw=0, sag=0, opacity=1)
    S.set("separateur", **{"from": 0})
    for gid, c, w, mid, mc, txt in (("court", COURT_CUT, COURT_W, "court_mot", COURT_MOT_C, T_COURT),
                                    ("long", LONG_CUT, LONG_W, "long_mot", LONG_MOT_C, T_LONG)):
        kit.gauge(gid, list(c), value=1, w=w, h=TEMPS_H, dir="right", fill=LIGHT, empty=PAPER, sw=4, shadow=6, z=9,
                  scale=0)
        S.set(gid, fill=LIGHT)                  # hex : LIGHT -> CYAN (morceau actif, S18 / S19)
        kit.text(mid, list(mc), txt, size=34, weight=700, z=9, scale=0, color=INK)
        S.set(mid, color=INK)                   # hex : INK -> DEEP (légende active)

    # --- les lieux (PNG) ---
    png(S, "arbre", "TREE", PNG_W["TREE"], ARBRE_C, z=5)
    png(S, "bouee", "BUOY", PNG_W["BUOY"], BOUEE_C, z=5)
    png(S, "valise", "SUITCASE", PNG_W["SUITCASE"], VALISE_C, z=5, meta=clean_png(S, "SUITCASE", SUITCASE_ERASE))
    # S12 « imprévus, » : une vaguelette passe sous la bouée quand les billets s'y posent (la bouée = les imprévus)
    kit.curve("vague", [190, 592], [[-80, 0], [-53, -9], [-27, 0], [0, 9], [27, 0], [53, -9], [80, 0]], draw=0,
              color=DEEP, sw=5, dot=False, smooth=True, z=5.2)
    png(S, "berceau", "CRADLE", PNG_W["CRADLE"], BERCEAU_C, z=5)
    for zid, p, size in ZZZ:
        kit.text(zid, list(p), "z", size=size, weight=800, z=13, scale=0)

    # --- les billets : 10 nés de la pilule (S11), le 6e de l'arbre (S19), celui qui dort sans mission (S21) ---
    for k, bid in enumerate(BILLETS):
        billet(kit, bid, CASH_LOW, z=12 + 0.2 * k)
    # S11 « placer. » : « tout » part avec les billets ; « Non. » le barre (trait encre 6 px)
    pill(S, "tout", TOUT_START, T_TOUT, size=34, fill=LIGHT, z=14.6)
    S.add("tout_barre", "wire", z=14.7, a={"id": "tout", "at": [-62, 9]}, b={"id": "tout", "at": [62, -9]}, color=INK,
          sw=6)
    S.set("tout_barre", draw=0, sag=0, opacity=1)
    S.set("tout_barre", **{"from": 0})
    billet(kit, "billet_arbre", BILLET_ARBRE_FROM, z=14.2)
    billet(kit, "billet_dort", CASH_LOW, z=14.4)

    # --- rôles et durées ---
    capsule(kit, "role_imprevus", ROLE_IMPREVUS_C, T_IMPREVUS)
    capsule(kit, "role_projet", ROLE_PROJET_C, T_PROJET)
    capsule(kit, "role_progresser", ROLE_PROG_C, T_PROGRESSER, z=15)   # au-dessus de la pile de l'arbre (S19)
    capsule(kit, "role_vide", ROLE_PROG_C, T_Q, size=34, fill="none", w=ROLE_VIDE_W, shadow=0, sw=3, dash=[10, 8])
    S.set("role_vide", draw=0)                  # se trace (kit.draw) en S14 ; relayée par « Progresser » en S19
    S.set("role_vide_mot", opacity=0)
    capsule(kit, "role_dort", ROLE_DORT_C, T_Q, size=34, h=ROLE_DORT_H, fill="none", w=ROLE_DORT_W, shadow=0, sw=3,
            dash=[10, 8], z=14.5)
    S.set("role_dort", draw=0)                  # S21 : stroke INK -> RED (hex), role_dort_mot color INK -> RED
    S.set("role_dort_mot", opacity=0)
    for did, txt, c in DUREES:
        pill(S, did, COURT_MOT_C if txt == T_COURT else LONG_MOT_C, txt, size=34, fill=LIGHT, h=DUREE_H, w=DUREE_W,
             z=11)

    # --- la bascule (S13) : disques et légendes en entités monde (voir l'en-tête) ---
    kit.seesaw("bascule", list(BASCULE_C), w=BASCULE_W, h=22, baseW=100, baseH=80, ground=200, fill=INK, base=PAPER,
               z=10, scale=0)
    kit.icon("bouclier", list(BOUCLIER_SEAT), "shield", disc=DISQUE_R, fill=LIGHT, color=INK, shadow=4, z=10.5,
             scale=0)
    S.set("bouclier", fill=LIGHT)               # hex : LIGHT -> CYAN (S13 « stabilité » : le côté qui pèse)
    for wid, role, at in (("fil_bouee", "role_imprevus", [60, 0]), ("fil_valise", "role_projet", [30, 0])):
        S.add(wid, "wire", z=10.3, a={"id": "bouclier", "at": [0, 0]}, b={"id": role, "at": at}, color=DEEP, sw=4)
        S.set(wid, draw=0, sag=0, opacity=1)
        S.set(wid, **{"from": 0})
    kit.icon("pourcent", list(POURCENT_SEAT), "percent", disc=DISQUE_R, fill=LIGHT, color=INK, shadow=4, z=10.5,
             scale=0)
    kit.text("stabilite", list(STABILITE_C), T_STABILITE, size=32, weight=700, z=10.5, scale=0)
    kit.text("rendement", list(RENDEMENT_C), T_RENDEMENT, size=32, weight=700, z=10.5, scale=0)

    # --- l'imprévu (S18), la courbe en zigzag et son creux rouge (S19) ---
    kit.icon("imprevu", list(IMPREVU_C), "warning", disc=IMPREVU_R, fill=LIGHT, color=INK, shadow=4, z=11, scale=0)
    kit.curve("courbe", list(COURBE_C), [[x - COURBE_C[0], y - COURBE_C[1]] for x, y in COURBE_PTS_WORLD], draw=0,
              color=DEEP, sw=6, dot=False, smooth=True, z=10)
    kit.shape("courbe_creux", list(COURBE_CREUX), kind="circle", w=20, fill=RED, stroke=RED, sw=2, shadow=0, z=10.2,
              scale=0)

    # --- S20 : un fil deep de chaque pile à son morceau de barre ; S21 : une coche à côté de chaque pile à rôle ---
    for wid in ("fil_court1", "fil_court2", "fil_long"):
        S.add(wid, "wire", z=5.3, color=DEEP, sw=4)
        S.set(wid, pa=[0, 0], pb=[0, 0], draw=0, sag=0, opacity=1)
        S.set(wid, **{"from": 0})
    for cid, p in COCHES:
        kit.tick(cid, list(p), DEEP, z=15.5)

    # --- la fin : toucher au doigt (le curseur de kit.outro reste invisible) ---
    kit.shape("fin_doigt", list(FIN_TAP), kind="circle", w=44, fill=INK, stroke=PAPER, sw=4, shadow=0, z=42, scale=0)
    for k in range(2):
        kit.shape(f"fin_onde{k + 1}", list(FIN_TAP), kind="circle", w=70, fill="none", stroke=DEEP, sw=6, shadow=0,
                  z=41.9, opacity=0)

    return SimpleNamespace(toi=toi, tag=tag)


def build(S):
    kit = Kit(S)
    c = cast(S, kit)
    only = [p for p in os.environ.get("WTH_PARTS", "").split(",") if p]   # WTH_PARTS=p2 : cette partie seule
    for name in PARTS:
        if not only or name in only:
            importlib.import_module(f".{name}", __name__).part(S, kit, c)
