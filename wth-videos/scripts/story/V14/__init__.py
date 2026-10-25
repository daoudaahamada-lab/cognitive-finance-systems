"""V14 « Ton IA financière dit « je ne sais pas » ? » : mise en scène Story, en paquet (une partie par fichier).

Storyboard : scripts/storyboards/V14.json (v1, révisé après le test sans son, 22 scènes, 88 temps forts, 87,814 s),
version lisible scripts/storyboards/V14.md. Voix : build/V14/words.json (film : images 0-2633, FILM_END = 2634).
Fil : la pilule cyan « Question fiscale ? » (`pastille`, pill 388 x 64, Bold 34) : dans la main de « Toi » à
l'image 0 (630, 1060), envoyée devant l'IA (S01), posée sur l'en-tête de la réponse d'aplomb (S02-S09), seule en l'air
quand celle-ci rentre dans la boule (S10), sur l'en-tête de la carte neuve (S10-S18), repart devant l'IA pour le test
(S19), revient sur la carte « Après » (S20-S21), devient le bouton « S’abonner » (S22). Entité MONDE : quand sa carte
bouge, la déplacer avec la même clé (même f, d, e) vers head_pt(...).
Parti pris : « une question, trois réponses » : la réponse d'aplomb (`reponse`, Sheet(3), case « Source » vide au pied),
la réponse prudente (`bonne_reponse`, Sheet(4) : réponse, source, date, limites), la réponse « Je ne sais pas » (bulle de
pensée `pensee` en S03-S04, bulle parlée `bulle_jnsp` en S20-S22).
IA (AI.png, en bas à gauche) : n'agit qu'en POINTILLÉS ai_tick (faisceaux `f_*`, coches variant « ai », contours de
ses bulles et de sa réponse au test). « Toi » (figurine encre 0,9, en bas à droite) : seul à tenir le stylo et le
tampon ; trait plein deep. Conseiller : figurine papier (S15-S18).

Parties (scènes contiguës ; poids : temps forts et secondes) :
- p1 : S01-S07, images 0-855 (28 temps forts, 28,5 s). Accroche (question envoyée, réponse d'aplomb à case « Source »
  vide, doute, pensée « Je ne sais pas », cible du test) ; contexte (pensée ravalée, rembobinage, case « Source »
  détachée, boule de cristal, valeurs inventées) ; point 1 : les pièces de « Toi » reliées à la réponse.
- p2 : S08-S15, images 856-1746 (30 temps forts, 29,7 s). Point 1 : trois lignes cassées au stylo, deux pièces
  perdues ; point 2 : la réponse rangée dans la boule, la carte neuve à 4 lignes, le livre dans la case « Source »,
  la citation, l'empreinte, où vérifier, la coche de « Toi » ; point 3 : le faisceau qui retombe, le conseiller.
- p3 : S16-S22, images 1747-2633 (30 temps forts, 29,6 s). Les trois cas, la sonnette et « Vois un conseiller », les
  deux applis, le test à la cible, Avant / Après et « Je ne sais pas » coché, tampon CONFIANCE, fin.
Les coupes tombent sur des débuts de scène où la composition repart : S08 (« Toi » monte vérifier) et S16 (la colonne
des cas). ENTRY_P2 et ENTRY_P3 sont le contrat des raccords (kit.pin(f0 - 1, …)). Les figurines n'y sont jamais.

Entités nouvelles : AUCUN nouveau type, aucun changement du code partagé. Compositions (catalogue) :
- case « Source » = shape round en tirets deep (pistes w, h, stroke hex deep -> rouge -> deep) + silhouette de livre
  (shape poly en tirets, enfant) + mot « Source » (text, monde) ;
- bulles de l'IA = shape round au contour pointillé ai_tick + pointe (shape poly ouverte pointillée, enfant) ou ronds
  de pensée (2 shape circle pointillés) + textes ; une entité par bulle (pensee, citation, bulle_conseil, bulle_jnsp) ;
- fenêtres d'appli = shape round (contour tracé, piste draw) + filet de barre de titre + 3 points (enfants) ; le type
  window n'a pas de piste draw ;
- épaississement d'un fil (5 -> 9 px, 4 -> 7 px rouge) = fil doublé (`fil_source_gras`, `fil_jetons_rouge`, mêmes
  ancres, opacité 0 -> 1) : la piste sw n'existe pas sur wire ;
- surligneur de L4 = shape rect light sous la ligne (pistes w + pos, bord gauche fixe) ; passer la piste slotFill de
  L4 à 0 dans les mêmes images, sinon la capsule beige le cache ;
- pile de pièces = groupe invisible `pile` (origine au sol, pivot du vacillement) + ellipses `piece1-7` enfants ;
- réponse de l'IA au test = shape round pointillé ai_tick + texte (pill n'a pas de contour en tirets) ;
- toucher final au stylo de « Toi » (pas de flèche de souris) : kit.outro puis S.set(out["cursor"], opacity=0),
  ondes `fin_onde1-2`.

ÉCARTS DE PLACE OU DE TAILLE (raisons de mise en page ou d'allonge, aucun sens changé) :
- livre BOOK.png à 150 px (et non 170) : il tient avec 15 px de marge dans la case de 180 x 160 et sa silhouette en
  tirets a exactement son contour (150 x 92 dans la grande case, 90 x 55 au pied de la carte) ;
- empreinte FINGERPRINT.png à 90 px de large (110 de haut, rapport 1,21) en (590, 1176) : posée au sol (bas y 1231),
  sous la bulle de la citation (bas y 1120) ;
- cible TARGET.png : rapport 0,667 (200 x 133 en S19, y 893-1027) ;
- fil de la source : part de la puce de L2 (bord gauche de la carte), là d'où le point de S13 part déjà, et non du
  milieu de « site officiel » : S.along_wire suit alors le fil exact (il ignore `via`) ;
- S14 : la coche de « Toi » (740, 890) est hors d'allonge depuis le repos (261 px > 240 à l'échelle 0,9) : « Toi »
  saute en TOI_MID (860, 830) sur « C’est », puis redescend au repos sur « certitude » (après la coche) ;
- bouton de fin : toucher en FIN_TAP (700, 955), dans le bouton et hors du libellé, à 226 px de l'épaule (le coin
  (690, 965) est au bord du bouton).
"""
import importlib
import math
import os
from types import SimpleNamespace

from pipeline.story import GEOM, STYLE, text_width
from pipeline.story_kit import Figure, Kit, Sheet

PARTS = ["p1", "p2", "p3"]                      # S01-S07, S08-S15, S16-S22
NBSP = " "                                 # espace insécable (avant « : », « ? », après « », avant « »)
ALERT_WORDS = {"faux", "inventée", "erroné", "fausse", "cher"}   # karaoké en rouge (style du storyboard)
ACOUSTIC_SNAP = {"gap": 0.2, "window": 0.08}    # temps fort après un silence : calé sur l'attaque audible

# ---------- couleurs ----------
INK, CYAN, DEEP, LIGHT = STYLE["ink"], STYLE["cyan"], STYLE["deep"], STYLE["light"]
PAPER, RED, BG, AI_TICK = STYLE["paper"], STYLE["red"], STYLE["bg"], STYLE["ai_tick"]
AI_INK = "#706864"                              # pointillés de l'IA (faisceaux, bulles) : gris encre lisible au
#                                                 téléphone, comme V01 (mix(BG, INK, 0,62)) ; coches de l'IA en AI_TICK

# ---------- sous-titres : découpes imposées (tour de revue 1) ----------
CAPTION_GROUPS = [["Tu poses", "une question", "fiscale", "à ton IA"],
                  ["voir pourquoi", "une IA financière"],
                  ["doit savoir dire", "je ne sais pas"],
                  ["Même sans", "l’information"],
                  ["et sourcée", "te dit où vérifier"],
                  ["Une IA", "qui dit", "je ne sais pas"]]

# ---------- textes à l'écran (typographie française) ----------
T_QUESTION = f"Question fiscale{NBSP}?"
T_ABONNER = "S’abonner"
T_TOI, T_IA, T_CONSEILLER = "Toi", "Ton IA", "Conseiller"
T_REPONSE = "Réponse"                           # en-tête des deux cartes
LINES_A = [(f"Règle{NBSP}:", "déductible", "none"), (f"Plafond{NBSP}:", "aucun", "none"),
           (f"Date{NBSP}:", "fin du mois", "none")]                    # réponse d'aplomb : puces vides, neutres
LINES_B = [(f"Réponse{NBSP}:", "en général", "chat"), (f"Source{NBSP}:", "site officiel", "bank"),
           (f"Date{NBSP}:", "à jour", "cal"), (f"Limites{NBSP}:", "ton cas", "person")]   # réponse prudente
T_SOURCE = "Source"
T_JNSP = "Je ne sais pas"
T_CIT1 = f"«{NBSP}Cette règle s’applique"       # citation (S12), Bold 30, 3 lignes
T_CIT2A, T_CIT2B = "en général", ", mais dépend"        # « en général » : surligneur (mark)
T_CIT3A, T_CIT3B, T_CIT3C = "de ", "ta situation", f"{NBSP}»"   # « ta situation » : soulignement (under)
T_CAS = ["Question réglementaire\nhors contexte", "Situation personnelle\ncomplexe", "Montant important"]
T_SIGNE = "§"
T_CONSEIL = "Vois un\nconseiller"
T_TEST = "en général"                           # les deux réponses du test (S19)
T_AVANT, T_APRES = "Avant", "Après"
T_TAMPON = "CONFIANCE"
T_EURO = "€"

# ---------- mise en page (1080 x 1920) ----------
X_MIN, X_MAX, Y_MIN, Y_MAX = 40, 930, 160, 1270  # zone d'action ; on descend jusqu'à y ≈ 1250
GROUND = 1230                                   # pied des figurines
FIG_S = 0.9                                     # « Toi » et le conseiller
FIG_BASE = GEOM["FIGURE"]["base"]               # 95
HEAD_DY, HEAD_R = GEOM["FIGURE"]["head"]["cy"], GEOM["FIGURE"]["head"]["r"]     # -64, 32 (échelle 1)
SHOULDER = GEOM["FIGURE"]["shoulder"]           # [-30, -16]
REACH_OK = 267 * FIG_S                          # allonge confortable à l'échelle 0,9 (240 px)
REACH_MIN = 63 * FIG_S
REACH_HAND = 161 * FIG_S * 0.98                 # main seule (tampon) : 142 px


def fig_pos(x, feet=GROUND, s=FIG_S):
    return [x, round(feet - FIG_BASE * s, 1)]


# --- « Toi » (bras côté gauche : il fait face à gauche) ---
TOI_REST = (870, 1144)                          # repos : pied y 1229,5 ; tête y 1058-1115 ; épaule (843, 1129,6)
TOI_HIGH = (880, 640)                           # S08 : à hauteur de la carte, corps hors de la carte (x ≥ 835)
TOI_MID = (868, 770)                            # S14 : la coche de la carte prudente et la case de la boule
TOI_LIVRE = (330, 950)                          # S13 « vérifier » : à portée du livre, sous la carte
TOI_TEST = (770, 1144)                          # S19 : à portée du centre de la cible (au sol)
TOI_STAMP = (796, 834)                          # S21 : poignée du tampon à portée de la main seule
TOI_CHEST = (0, -20)                            # point de la poitrine (repère de « Toi ») : la cible, l'empreinte
TOI_LOW_GRIP, TOI_LOW_ROT = (52, 10), 80        # bras BAISSÉ (repos lisible : stylo vers le sol, pas levé)
NOM_LOCAL = (0, round(-122 / FIG_S, 1))         # étiquette « Toi » 122 px au-dessus du centre (enfant de toi)
NOM_SIZE, NOM_H = round(34 / FIG_S, 1), round(56 / FIG_S, 1)   # 34 px / 56 px à l'écran (enfant à l'échelle 0,9)


def toi_head(c=TOI_REST):
    return (c[0], round(c[1] + HEAD_DY * FIG_S, 1))


def hop_low(toi, f, to, d):
    """Saut de « Toi » bras BAISSÉ du début à la fin (le saut du kit ramène le stylo levé : on re-pose par-dessus)."""
    toi.hop(f, list(to), d)
    toi.lower(f, d)
    return f + d


def walk_low(toi, f, to, d=None):
    return toi.walk(f, list(to), d=d, low=True)


# --- l'IA (AI.png, en bas à gauche) ---
IA_C, IA_W = (165, 1110), 170                   # 170 x 216 : x 80-250, y 1002-1218
NOM_IA_C = (165, 995)                           # « Ton IA » : x 88-242, y 967-1023
IA_HEAD = (270, 1044)                           # départ des faisceaux : devant le front, à droite de « Ton IA »
IA_MOUTH = (252, 1078)                          # pointe des bulles parlées
IA_BRAIN = (175, 1060)                          # éclat (burst) du cerveau de verre

# --- la pastille-question (objet du fil, monde) ---
PASTILLE_W, PASTILLE_H, PASTILLE_SIZE = 388, 64, 34
PASTILLE_C0, PASTILLE_K0 = (560, 945), 1.3      # S01 : grande (libellé 44 px), dans la main de « Toi » (x 308-812)
PASTILLE_TAP = (770, 950)                       # S01 « poses » : près du bout droit
PASTILLE_IA, PASTILLE_IA_K = (470, 880), 1.15   # S01 « fiscale » : devant le front de l'IA (x 247-693)
PASTILLE_IA_LEFT = (256, 896)                   # S01 « IA. » : bout gauche, touché par le faisceau
PASTILLE_DOCK_W = 330                           # sur un en-tête : pilule resserrée (libellé 34 -> 32 px à 0,94)
PASTILLE_HEAD_K = 0.94                          # 310 px à l'échelle 1 de la carte (même largeur qu'avant)
PASTILLE_TEST, PASTILLE_TEST_K = (400, 985), 0.8    # S19 : devant l'IA (x 268-532), sous l'appli choisie


# --- les deux cartes « Réponse » (fiche Sheet) ---
CARD_C = (540, 640)                             # carte d'aplomb (S02-S09)
CARD_B_C = (540, 545)                           # carte prudente (S10-S14) : y 237-853 (le bas reste aux acteurs)
SHEET_A = Sheet(n=3, w=520)                     # réponse d'aplomb : 520 x 512 (x 280-800, y 384-896) ; rangées 520/624/728
SHEET_B = Sheet(n=4, w=520)                     # réponse prudente : 520 x 616 ; rangées locales -172/-68/36/140
HEAD_A_LOCAL = (-100, round(-SHEET_A.h / 2 + SHEET_A.head / 2, 1))   # pastille sur l'en-tête : (440, 426)
HEAD_B_LOCAL = (-100, round(-SHEET_B.h / 2 + SHEET_B.head / 2, 1))   # (440, 279)
CARD_A_FROM, CARD_A_FROM_K = (200, 1060), 0.1   # S02 : sort de la tête de l'IA
REP_A_IDS = [f"reponse_L{i + 1}" for i in range(3)]
REP_B_IDS = [f"bonne_reponse_L{i + 1}" for i in range(4)]
TICK_A_IDS = [f"reponse_ia{i + 1}" for i in range(3)]   # coches pointillées de l'IA (x 750)
VALUE_END_A = [(690, 510), (690, 614), (690, 718)]      # S08 : la pointe touche la fin de chaque valeur
VALUE_W_A = [164, 96, 171]                              # largeur des valeurs (Inter 600, 32 px)
# places des cartes
B_SMALL_C, B_SMALL_K = (650, 450), 0.55         # S15-S17 : x 507-793, y 281-620 (lignes en barres, lite)
B_APPLI_C, B_APPLI_K = (600, 600), 0.6          # S18-S19 : dans l'appli de droite (x 444-756, y 415-785)
A_APPLI_C, A_APPLI_K = (220, 590), 0.6          # S18 : réponse cassée dans l'appli de gauche (x 64-376)
B_APRES_C, B_APRES_K = (540, 650), 0.8          # S20-S21 : « Après » (x 332-748, y 404-896)
A_AVANT_C, A_AVANT_K = (175, 560), 0.5          # S20-S21 : « Avant » (x 45-305, y 432-688)


def head_pt(card="bonne_reponse", c=None, k=1.0):
    """Place (monde) et échelle de la pastille sur l'en-tête d'une carte posée en c à l'échelle k."""
    loc = HEAD_A_LOCAL if card == "reponse" else HEAD_B_LOCAL
    c = c or (CARD_C if card == "reponse" else CARD_B_C)
    return [round(c[0] + loc[0] * k, 1), round(c[1] + loc[1] * k, 1)], round(PASTILLE_HEAD_K * k, 4)


def card_pt(card, local, c=None, k=1.0):
    """Point monde d'un point local d'une carte posée en c à l'échelle k (sans lire l'état)."""
    c = c or (CARD_C if card in ("a", "reponse") else CARD_B_C)
    return [round(c[0] + local[0] * k, 1), round(c[1] + local[1] * k, 1)]


# --- la case « Source » (monde) et le livre ---
SOURCE_SMALL_C, SOURCE_SMALL_W, SOURCE_SMALL_H = (560, 830), 150, 80     # S02-S05 : au pied de la carte (x 485-635)
SOURCE_BIG_C, SOURCE_BIG_W, SOURCE_BIG_H = (150, 700), 180, 160          # S05-S11 : à gauche (x 60-240, y 620-780)
SOURCE_MOT_SMALL, SOURCE_MOT_BIG = (390, 830), (150, 590)                # « Source » Bold 32 -> 34 (échelle 34/32)
SOURCE_MOT_BIG_K = round(34 / 32, 4)
SOURCE_EDGE_RIGHT = (234, 772)                  # S05 « réponse. » : la branche de l'IA s'arrête au coin bas droit
LIVRE_W = 150                                   # BOOK.png (rapport 0,61 : 150 x 92 dans la grande case)
LIVRE_SMALL_K = round(110 / LIVRE_W, 4)         # S15-S19 : 110 px
LIVRE_SMALL_C = (420, 450)                      # S15-S17 : à gauche de la carte réduite
LIVRE_APPLI_C = (520, 875)                      # S18-S19 : sous la carte, dans l'appli choisie
LIVRE_TAP = (205, 726)                          # S13 « vérifier » : le stylo touche le livre (bord droit)
SILH_SMALL_K = 0.6                              # silhouette en tirets : 90 x 55 au pied de la carte
SILH_BIG_K = 1.0                                # 150 x 92 dans la grande case (exactement le contour du livre)
CADRE_LIVRE_W, CADRE_LIVRE_H = 182, 124         # S13 : cadre deep autour du livre (16 px de marge)

# --- la boule de cristal (CRYSTAL.png, rapport 1,06 : 150 x 141 à l'échelle 1) ---
BOULE_W = 150
BOULE_TETE = (340, 1000)                        # S06 : sortie de la tête de l'IA
BOULE_SOL, BOULE_SOL_K = (400, 1160), round(140 / BOULE_W, 4)   # S10-S13 : au sol entre l'IA et l'empreinte
BOULE_CHOIX = (600, 962)                        # S14 : se relève sous la carte, face à la coche (150 px)
BOULE_APPLI = (220, 862)                        # S18 : dans l'appli de gauche
BOULE_AVANT, BOULE_AVANT_K = (180, 800), round(130 / BOULE_W, 4)   # S20-S21 : sous la carte « Avant »
CASE_W = 56                                     # cases de coche vides (pointillés) : S14
CASE_BOULE = (712, 930)                         # à droite de la boule
CASE_CARTE_LOCAL = (200, 250)                   # = coche de « Toi » (740, 795)

# --- la bulle « ? » de « Toi » (bubble), puis autocollant sur la carte d'aplomb ---
DOUTE_C = (720, 960)
STICKER_C = (762, 866)                          # coin bas droit de la carte (dans la carte : x 730-794)
DOUTE_BIG = dict(w=150, h=120, r=36, q=80, qx=0, px=0, ps=0, sw=5, shadow=6, gs=4)
DOUTE_SMALL = dict(w=64, h=64, r=32, q=44, qx=0, px=0, ps=0, sw=4, shadow=4, gs=3)

# --- le retour en arrière (S04) ---
REWIND_C, REWIND_R = (540, 312), 56

# --- l'IA pense / parle ---
PENSEE_C, PENSEE_W, PENSEE_H = (566, 985), 380, 120               # S03-S04 : pensée (x 376-756, y 925-1045)
PENSEE_RONDS = [((262, 1030), 12), ((298, 1004), 18), ((342, 978), 26)]   # ronds pointillés (tête -> bulle)
CITATION_C, CITATION_W, CITATION_H = (470, 946), 440, 136         # S12-S13 : parole (x 250-690, y 878-1014)
CIT_Y = [908, 946, 984]                                           # 3 lignes Bold 30
CONSEIL_C, CONSEIL_W, CONSEIL_H = (150, 820), 220, 120            # S17 : « Vois un / conseiller » (x 40-260, Bold 30)
CONSEIL_TIP = (196, 960)                        # pointe vers la tête de l'IA (au-dessus de « Ton IA »)
DESIGNE_A, DESIGNE_VIA, DESIGNE_B = (250, 878), (302, 988), (406, 1022)   # S17 : bulle -> étiquette « Conseiller »
JNSP_C, JNSP_W, JNSP_H = (566, 1010), 380, 120                    # S20-S22 : « Je ne sais pas » (x 376-756)
JNSP_RONDS = [((262, 1040), 12), ((298, 1018), 18), ((342, 1000), 26)]
JNSP_TAP = (752, 1012)                          # S20 « faiblesse. » : bout droit de la bulle
JNSP_TICK_LOCAL = (150, 0)                      # coche pleine deep 44 px (716, 1010)
BEAM = dict(color=AI_INK, sw=7, dash=[0.01, 16], dots=True)       # faisceau / trait de l'IA (V01 : 7 px, gris encre)

# --- l'argent de « Toi » : la pile (groupe, origine au sol), le fil ---
PILE_C = (700, 1235)                            # origine = milieu du bas de la pile (pivot du vacillement)
PIECE_W, PIECE_H, PIECE_DY = 110, 30, 14
PIECE_LOCAL = [(0, -PIECE_H / 2 - PIECE_DY * k) for k in range(7)]   # piece1 (bas) ... piece7 ; 1-4 dès S07
PILE_TOP_LOCAL = (0, PIECE_LOCAL[3][1] - PIECE_H / 2)               # haut de la pièce du dessus (4 pièces)
FIL_JETONS_A = (180, 256)                       # bas de la carte d'aplomb (720, 896) (repère de la carte)
PILE_CAS_K = round(60 / PIECE_W, 4)             # S16 : 60 px dans la carte-cas « Montant important »

# --- la situation de « Toi » (empreinte) ---
EMPREINTE_W = 130                               # FINGERPRINT.png 130 x 157
EMPREINTE_C = (700, 1152)                       # au sol sous le coin bas droit de la carte (x 635-765, y 1074-1230)
EMPREINTE_TOI = (756, 1075)                     # S12 : d'abord tenue contre « Toi », à hauteur de poitrine
EMPREINTE_CAS_K = round(70 / EMPREINTE_W, 4)    # S16 : 70 px dans la carte-cas 2
FIL_EMPREINTE_PTS = [(712, 663), (746, 663), (746, 1082)]   # S12 : fin de « ton cas » -> haut de l'empreinte

# --- le conseiller (figurine papier) ---
CONSEILLER_C = (525, 1144)                      # entre le faisceau mort et l'empreinte ; face à « Toi »
CONSEILLER_FROM = 300                           # entre en marchant depuis la droite de l'IA

# --- les trois cas (S16-S18) ---
CAS_C = [(540, 712), (540, 814), (540, 916)]    # x 300-780, y 666-962 (46 px sous la carte réduite)
CAS_W, CAS_H = 480, 92
CAS_FROM = (330, 1010)                          # S16 : les cartes-cas partent d'où le faisceau a échoué
CAS_OBJ_LOCAL = (-195, 0)                       # objet à gauche : « § » sur disque cyan, empreinte, pièces (x 345)
CAS_TXT_LOCAL = (-150, 0)                       # texte Bold 30, ancre start (x 390)

# --- la sonnette (BELL.png) ---
SONNETTE_W = 130
SONNETTE_C = (165, 560)                         # S17 : colonne de gauche, au-dessus de l'IA
SONNETTE_APPLI, SONNETTE_APPLI_K = (680, 872), round(100 / SONNETTE_W, 4)   # S18-S19
SONNETTE_BTN = (165, 522)                       # bouton (haut) : le faisceau de l'IA le frappe
ONDES_VERS_CONSEILLER = 52                      # S17 : ondes tournées vers le conseiller (degrés)

# --- les deux applis (S18-S19), plus bas : y 360-950 ---
APPLI_W, APPLI_H, APPLI_R = 340, 590, 24
APPLI_G_C, APPLI_D_C = (220, 655), (600, 655)   # x 50-390 et 430-770
APPLI_TAP = (771, 915)                          # S18 « l’incertitude. » : bord droit de l'appli, touché du sol
CADRE_APPLI_W, CADRE_APPLI_H = 370, 620         # x 415-785, y 345-965

# --- le test (S19) : cible retournée (flèche à gauche, mille à droite) ---
CIBLE_W = 300                                   # TARGET.png 300 x 202 ; face ≈ x 0,415-0,894 de la largeur
CIBLE_K03 = round(136 / CIBLE_W, 4)             # S03-S05 : 136 px
CIBLE_S03 = (871, 906)                          # S03 : au-dessus de l'étiquette « Toi » (x 803-939)
CIBLE_C = (548, 1100)                           # S19 : devant « Toi » (x 398-698, y 999-1201)
MILLE_LOCAL = (29, -12)                         # le mille (retourné) : (577, 1088)
TEST_W, TEST_H, TEST_SIZE = 160, 44, 26         # pilules du test (dans la cible, échelle 1)
TEST_IA_DX = (0, 0)                             # S19 : la réponse de l'IA se pose exactement sur celle de « Toi » et s'y fond
COCHE_CIBLE_LOCAL = (128, -90)                  # (676, 1010) : coin haut droit, à 20 px des pilules

# --- Avant / Après, tampon (S20-S21) ---
AVANT_C, APRES_C = (175, 392), (540, 362)
CADRE_L4_W, CADRE_L4_H = round(420 / B_APRES_K), round(84 / B_APRES_K)   # 420 x 84 à l'écran
TAMPON_LOCAL = (117, 252)                       # (655, 874) : dans la marge basse, à 19 px du bord droit
TAMPON_W, TAMPON_H, TAMPON_SIZE = 248, round(70 / B_APRES_K), 31   # 211 x 70 à l'écran, libellé 26 px
COCHE_TOI_LOCAL = (200, 250)                    # S14 : coche pleine 70 px (740, 795), marge basse droite

# --- la fin (kit.outro) : carte (540, 760), bouton centre (540, 908) ; toucher au stylo, pas de souris ---
FIN_C = (540, 760)
FIN_BUTTON = (540, 908)
FIN_TAP = (700, 955)                            # dans le bouton, hors du libellé

# ---------- surligneur de L4 (enfant de bonne_reponse) ----------
_KEY_X = SHEET_B.x["text"]                      # -216
SURL_L4_X0, SURL_L4_X1 = _KEY_X - 10, SHEET_B.x["value"] + 10      # -226 -> 170
SURL_L4_Y = SHEET_B.rows[3] + SHEET_B.ty        # 118 (ligne de texte de L4)
SURL_L4_W, SURL_L4_H = SURL_L4_X1 - SURL_L4_X0, 44
SURL_L4_C = ((SURL_L4_X0 + SURL_L4_X1) / 2, SURL_L4_Y)


def scene_f0(S, sid):
    return round(next(s for s in S.sb["scenes"] if s["id"] == sid)["t_start"] * S.fps)


def film_end(S):
    """Première image après le film (fin de la dernière scène du storyboard)."""
    return round(S.sb["scenes"][-1]["t_end"] * S.fps)


# ---------- l'allonge de « Toi » (bras gauche, échelle 0,9) ----------
def arm_check(fig, pt):
    """(distance épaule -> cible, côté sûr, dégagement de la tête) pour « Toi » (side left) en fig = (x, y)."""
    sx, sy = fig[0] + SHOULDER[0] * FIG_S, fig[1] + SHOULDER[1] * FIG_S
    dx, dy = pt[0] - sx, sy - pt[1]
    d = math.hypot(dx, dy)
    safe = -dx >= 0.3 * max(dy, 0) or abs(dx) < 1e-6
    hx, hy = fig[0], fig[1] + HEAD_DY * FIG_S
    ux, uy = (pt[0] - sx) / max(d, 1e-6), (pt[1] - sy) / max(d, 1e-6)
    clear = min(math.hypot(sx + ux * t - hx, sy + uy * t - hy) for t in range(0, int(min(d, 120)) + 1))
    return round(d, 1), safe, round(clear, 1)


def assert_reach(fig, pt, what):
    d, safe, clear = arm_check(fig, pt)
    assert REACH_MIN <= d <= REACH_OK and safe and clear >= HEAD_R * FIG_S + 6, \
        f"{what} : hors d'allonge depuis {fig} : {d} px, côté sûr {safe}, tête {clear} px"


_MILLE = (CIBLE_C[0] + MILLE_LOCAL[0], CIBLE_C[1] + MILLE_LOCAL[1])
_COCHE_CARTE = (CARD_B_C[0] + COCHE_TOI_LOCAL[0], CARD_B_C[1] + COCHE_TOI_LOCAL[1])
for _fig, _pt, _what in [(TOI_REST, PASTILLE_TAP, "S01 toucher la pastille"),
                         *[(TOI_HIGH, p, f"S08 casser L{i + 1}") for i, p in enumerate(VALUE_END_A)],
                         (TOI_LIVRE, LIVRE_TAP, "S13 toucher le livre"),
                         (TOI_MID, _COCHE_CARTE, "S14 coche de « Toi »"),
                         (TOI_MID, (CASE_BOULE[0], CASE_BOULE[1] - 14), "S14 hésiter sur la case de la boule"),
                         (TOI_REST, APPLI_TAP, "S18 toucher l'appli de droite"),
                         (TOI_TEST, (_MILLE[0] - 62, _MILLE[1]), "S19 écrire (début de la pilule)"),
                         (TOI_TEST, (_MILLE[0] + 62, _MILLE[1]), "S19 écrire (fin de la pilule)"),
                         (TOI_TEST, (CIBLE_C[0] + COCHE_CIBLE_LOCAL[0], CIBLE_C[1] + COCHE_CIBLE_LOCAL[1]),
                          "S19 cocher la cible"),
                         (TOI_REST, JNSP_TAP, "S20 toucher la bulle « Je ne sais pas »"),
                         (TOI_REST, FIN_TAP, "S22 toucher le bouton")]:
    assert_reach(_fig, _pt, _what)


# ---------- petites fabriques ----------
def png(S, id, name, w, pos, z=5, contact=True, parent=None, scale=0, keep_largest=False, **p):
    """Illustration générique (verre, alpha strict), largeur w, rapport gardé. -> meta (+ h_disp)."""
    m = S.png(name, keep_largest=keep_largest)
    h = round(w * m["h"] / m["w"])
    c = dict(contact=dict(w=round(w * 0.7), h=22, dy=4, blur=10, alpha=0.2)) if contact else {}
    S.add(id, "png", z=z, parent=parent, src=m["src"], w=w, h=h, **c, **p)
    S.set(id, pos=list(pos), scale=scale, opacity=1, rot=0)
    return {**m, "h_disp": h}


def pill(S, id, pos, text, size=34, weight=700, fill=PAPER, h=56, z=12, parent=None, scale=0, pad=48, w=None,
         shadow=4, **p):
    """Pilule de texte (type pill) ; w mesuré si absent. -> largeur."""
    if w is None:
        w = round(text_width(text, size, weight) + pad + (30 if p.get("icon") else 0))
    S.add(id, "pill", z=z, parent=parent, text=text, w=w, h=h, size=size, weight=weight, fill=fill, shadow=shadow, **p)
    S.set(id, pos=list(pos), scale=scale, opacity=1, fill=fill, w=w, text=text, textOp=1)
    return w


def line(kit, id, pts, color=INK, sw=7, z=12, parent=None, pos=(0, 0), dash=None):
    """Trait ouvert à tracer (shape poly, draw 0) ; le 1er sommet est le départ du tracé."""
    p = {"dash": dash} if dash else {}
    return kit.shape(id, list(pos), kind="poly", pts=[list(q) for q in pts], closed=False, fill="none", stroke=color,
                     sw=sw, shadow=0, z=z, parent=parent, draw=0, **p)


def wire(S, id, z, color, sw, pa=None, pb=None, a=None, b=None, draw=0, opacity=1, **p):
    """Fil (wire) : ancres a / b {id, at}, ou extrémités libres pa / pb (pistes monde)."""
    S.add(id, "wire", z=z, color=color, sw=sw, **({"a": a} if a else {}), **({"b": b} if b else {}), **p)
    S.set(id, draw=draw, sag=0, opacity=opacity, color=color)
    S.set(id, **{"from": 0})
    if pa is not None:
        S.set(id, pa=list(pa), pb=list(pb))
    return id


def beam(S, id, pa, pb, z=12.2):
    """Faisceau pointillé de l'IA (extrémités libres pa / pb, monde) : 7 px, gris encre, point au bout."""
    return wire(S, id, z, BEAM["color"], BEAM["sw"], pa=pa, pb=pb, dash=BEAM["dash"], dots=True)


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


def look(S, id, f, v, d=4):
    """Regard d'une figurine (piste look, -1 gauche ... 1 droite) : piste de rendu seule, sans effet sur le bras."""
    S.key(id, "look", f, v, d, "out")
    return f + d


def book_pts(w, h):
    """Silhouette d'un livre ouvert (contour fermé, deux pages en V), w x h, centrée."""
    a, b = w / 2, h / 2
    return [[-a, -b + 8], [-a * 0.45, -b], [0, -b + 8], [a * 0.45, -b], [a, -b + 8], [a, b], [a * 0.45, b - 8],
            [0, b], [-a * 0.45, b - 8], [-a, b]]


def arc_pts(cx, r, a0=-38, a1=38, n=7):
    """Arc de cercle (ondes de la sonnette), centre (cx, 0), angles en degrés (0 = vers la droite)."""
    return [[round(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / (n - 1))), 1),
             round(r * math.sin(math.radians(a0 + (a1 - a0) * i / (n - 1))), 1)] for i in range(n)]


def card(kit, sheet, id, lines, pos, scale, sheen_id=None, bullet_on=1):
    """Fiche « Réponse » (fiche + rangées line), avec keyW (piste lite) et, si `sheen_id`, le reflet sous les textes.
    Rangées vides (typed) ; renvoie leurs ids."""
    S = kit.S

    def sheen(dy):
        return {"id": sheen_id, "dx": 0, "dy": dy, "w": sheet.w, "h": sheet.h} if sheen_id else None
    sheet.id, sheet.lines = id, []
    S.add(id, "fiche", z=8, w=sheet.w, h=sheet.h, title=T_REPONSE, headerH=sheet.head, tabs=[],
          tabX=sheet.x["bullet"], **({"sheen": sheen(0)} if sheen_id else {}))
    S.set(id, pos=list(pos), scale=scale, opacity=1, lite=0)
    ids = []
    for i, (k, v, icon) in enumerate(lines):
        lid = f"{id}_L{i + 1}"
        p = sheet.line_params(k, v, icon, keyW=round(text_width(k, 32, 600), 1),
                              **({"sheen": sheen(sheet.rows[i])} if sheen_id else {}))
        S.add(lid, "line", z=9, parent=id, **p)
        S.set(lid, pos=[0, sheet.rows[i]], scale=1, chars=0, red=0, crack=0, flash=0, pulse=0, alarm=0, strike=0,
              fall=0, grow=0, dimValue=0, slotFill=1, bulletOn=bullet_on, opacity=1, lite=0)
        sheet.lines.append((lid, p))
        ids.append(lid)
    return ids


def _tail_pts(c, w, h, tip, base):
    """Pointe pleine d'une bulle parlée : (origine locale = milieu de la base, sommets relatifs à cette origine).
    La base est rentrée de 6 px dans la bulle (son aplat la couvre) ; la pointe va sur `tip` (monde)."""
    tx, ty = tip[0] - c[0], tip[1] - c[1]
    if abs(tx) <= w / 2 and abs(ty) > h / 2 - 4:  # base sur le bord haut / bas
        by = math.copysign(h / 2 - 6, ty)
        bx = max(-w / 2 + 34 + base / 2, min(w / 2 - 34 - base / 2, tx * 0.55))
        o = [round(bx, 1), round(by, 1)]
        pts = [[-base / 2, 0], [tx - o[0], ty - o[1]], [base / 2, 0]]
    else:                                        # base sur le bord gauche / droit
        bx = math.copysign(w / 2 - 6, tx)
        lim = max(0.0, h / 2 - base / 2 - 4)
        o = [round(bx, 1), round(max(-lim, min(lim, ty * 0.5)), 1)]
        pts = [[0, -base / 2], [tx - o[0], ty - o[1]], [0, base / 2]]
    return o, [[round(a, 1), round(b, 1)] for a, b in pts]


def ai_bubble(kit, id, c, w, h, r, z=13, tip=None, speech=False, base=40):
    """Bulle de l'IA (shape round papier, échelle 0). speech=False : PENSÉE, contour pointillé gris encre, sans
    pointe. speech=True : PAROLE, contour plein encre 4 px et grande pointe pleine (`id`_pointe, enfant, sous la
    bulle, origine au milieu de sa base) vers `tip` (la bouche de l'IA)."""
    if speech:
        kit.shape(id, list(c), kind="round", w=w, h=h, r=r, fill=PAPER, stroke=INK, sw=4, shadow=0, z=z, scale=0)
    else:
        kit.shape(id, list(c), kind="round", w=w, h=h, r=r, fill=PAPER, stroke=AI_INK, sw=4, dash=[0.01, 11],
                  shadow=0, z=z, scale=0)
    if speech and tip is not None:
        o, pts = _tail_pts(c, w, h, tip, base)
        kit.shape(f"{id}_pointe", o, kind="poly", pts=pts, closed=True, fill=PAPER, stroke=INK, sw=4, shadow=0,
                  z=z - 0.05, parent=id)
    return id


def thought_dots(kit, prefix, ronds, z=12.95):
    """Ronds de pensée pointillés (tête -> bulle), échelle 0 : ids prefix1..n."""
    for k, (c, r) in enumerate(ronds):
        kit.shape(f"{prefix}{k + 1}", list(c), kind="circle", w=2 * r, fill=PAPER, stroke=AI_INK, sw=4,
                  dash=[0.01, 9], shadow=0, z=z, scale=0)
    return [f"{prefix}{k + 1}" for k in range(len(ronds))]


# ---------- raccords (contrat des parties ; couleurs en hex minuscule : S.val rend du minuscule) ----------
def _lo(c):
    return c.lower()


_OFF = lambda *ids: {i: {"scale": 0} for i in ids}   # noqa: E731
_FULL_A = [len(k) + len(v) for k, v, _ in LINES_A]
_FULL_B = [len(k) + len(v) for k, v, _ in LINES_B]
_BEAMS_P1 = ["f_lit", "f_carte", "f_case", "f_boule1", "f_boule2", "f_boule3"]
_BEAMS_P2 = ["f_question", "f_ecrit", "f_empreinte"]

ENTRY_P2 = {   # fin de S07 = etat_initial de S08 (image 855)
    "pastille": {"pos": head_pt("reponse")[0], "scale": PASTILLE_HEAD_K, "text": T_QUESTION, "textOp": 1,
                 "w": PASTILLE_DOCK_W},
    "reponse": {"pos": list(CARD_C), "scale": 1, "lite": 0},
    **{lid: {"chars": _FULL_A[i], "red": 0, "crack": 0, "alarm": 0, "pulse": 0, "lite": 0}
       for i, lid in enumerate(REP_A_IDS)},
    **{t: {"draw": 1} for t in TICK_A_IDS},
    "reflet": {"p": 1},
    "doute": {"pos": list(STICKER_C), "scale": 1, "s": 1, "q": 1, "pulse": 0},
    "source": {"pos": list(SOURCE_BIG_C), "scale": 1, "w": SOURCE_BIG_W, "h": SOURCE_BIG_H, "stroke": _lo(DEEP),
               "opacity": 1},
    "source_livre": {"scale": SILH_BIG_K, "stroke": _lo(DEEP)},
    "source_mot": {"pos": list(SOURCE_MOT_BIG), "scale": SOURCE_MOT_BIG_K},
    "boule": {"pos": list(BOULE_TETE), "scale": 1},
    "pile": {"pos": list(PILE_C), "scale": 1, "rot": 0},
    **{f"piece{k}": {"scale": 1, "opacity": 1} for k in range(1, 5)},
    **_OFF("piece5", "piece6", "piece7"),
    "fil_jetons": {"draw": 1, "from": 0, "color": _lo(INK), "opacity": 1},
    "fil_jetons_rouge": {"opacity": 0},
    **{b: {"draw": 0, "from": 0} for b in _BEAMS_P1},
    **_OFF("cible", "pensee", "pensee_rond1", "pensee_rond2", "pensee_rond3", "rembobiner", "bonne_reponse", "livre",
           "empreinte", "eclat_ia"),
}

ENTRY_P3 = {   # fin de S15 = etat_initial de S16 (image 1746)
    "pastille": {"pos": head_pt("bonne_reponse", B_SMALL_C, B_SMALL_K)[0],
                 "scale": head_pt("bonne_reponse", B_SMALL_C, B_SMALL_K)[1], "text": T_QUESTION, "textOp": 0,
                 "w": PASTILLE_DOCK_W},
    "bonne_reponse": {"pos": list(B_SMALL_C), "scale": B_SMALL_K, "lite": 1},
    **{lid: {"chars": _FULL_B[i], "bulletOn": 1, "lite": 1, "flash": 0} for i, lid in enumerate(REP_B_IDS)},
    "coche_toi": {"draw": 1}, "coche_source": {"draw": 1},
    "livre": {"pos": list(LIVRE_SMALL_C), "scale": LIVRE_SMALL_K},
    "fil_source": {"draw": 1, "from": 0, "opacity": 1},
    "fil_source_gras": {"opacity": 0},
    "source": {"opacity": 0}, "source_mot": {"scale": 0},
    "cadre_livre": {"draw": 0}, "fil_empreinte": {"draw": 0},
    "empreinte": {"pos": list(EMPREINTE_C), "scale": 1},
    "pile": {"scale": 0},
    "piece1": {"scale": 1}, "piece2": {"scale": 1}, "piece2_euro": {"opacity": 1},
    "piece3": {"opacity": 0}, "piece4": {"opacity": 0},
    "fil_jetons": {"draw": 0, "from": 0}, "fil_jetons_rouge": {"opacity": 0},
    "boule": {"scale": 0},
    "reponse": {"scale": 0},
    **{lid: {"red": 1, "crack": 1} for lid in REP_A_IDS},
    "doute": {"scale": 0},
    **{b: {"draw": 0, "from": 0} for b in _BEAMS_P1 + _BEAMS_P2},
    **_OFF("citation", "point_source", "cible", "eclat_ia", "eclat_boule", "case_boule", "case_carte"),
}


def cast(S, kit):
    """Toute la distribution, à son état de l'image 0. Ce qui arrive plus tard : scale=0 (ou draw=0, chars=0,
    opacity=0). Seuls `fin` et son curseur naissent dans kit.outro (p3)."""

    # --- l'IA (AI.png) et son étiquette ---
    ai = png(S, "ia", "AI", IA_W, IA_C, z=4, scale=1, keep_largest=True, saturate=0.85)
    pill(S, "nom_ia", NOM_IA_C, T_IA, size=34, fill=PAPER, h=56, z=4.2, scale=1)
    S.add("eclat_ia", "burst", z=4.5, r0=40, r1=86, n=8, sw=6, color=DEEP, a0=-90)
    S.set("eclat_ia", pos=list(IA_BRAIN), scale=1, opacity=1, p=0)

    # --- « Toi » (encre, échelle 0,9, visible dès l'image 0) et son étiquette (enfant) ; bras baissé au repos ---
    toi = Figure(kit, "toi", pos=list(TOI_REST), scale=FIG_S, variant="ink", side="left", show=True)
    toi.low_grip, toi.low_rot = TOI_LOW_GRIP, TOI_LOW_ROT
    kit.ensure("toi", "look", 0)
    pill(S, "nom_toi", NOM_LOCAL, T_TOI, size=NOM_SIZE, fill=INK, color=BG, h=NOM_H, z=15.8, parent="toi", scale=1)

    # --- la pastille-question (objet du fil, monde) ---
    pill(S, "pastille", PASTILLE_C0, T_QUESTION, size=PASTILLE_SIZE, fill=CYAN, h=PASTILLE_H, w=PASTILLE_W, z=12.5,
         scale=PASTILLE_K0, shadow=6)
    S.set("pastille", rot=0)

    # --- les faisceaux et traits pointillés de l'IA (pa / pb monde ; draw 0) ---
    beam(S, "f_lit", IA_HEAD, PASTILLE_IA_LEFT)                         # S01 « IA. »
    beam(S, "f_carte", IA_HEAD, (290, 720))                             # S05 « générative »
    beam(S, "f_case", (272, 1040), SOURCE_EDGE_RIGHT)                   # S05 « réponse. » -> S06 « sans » (150, 700)
    for i in range(3):                                                  # S06 « fabriquer » : boule -> début des valeurs
        y = SHEET_A.rows[i] + CARD_C[1] + SHEET_A.ty
        beam(S, f"f_boule{i + 1}", (BOULE_TETE[0] + 20, BOULE_TETE[1] - 66), (700 - VALUE_W_A[i] - 8, y))
    beam(S, "f_question", IA_HEAD, head_pt("reponse")[0])               # S10 « bonne » : touche la pastille
    beam(S, "f_ecrit", IA_HEAD, (284, 420))                             # S11 « réponse, » : bord gauche de la carte
    beam(S, "f_empreinte", (262, 1056), (455, 1108))                    # S15 : s'arrête 180 px avant l'empreinte
    beam(S, "f_sonnette", (255, 1040), SONNETTE_BTN)                    # S17 « signaler, » (ne pas traverser « Ton IA »)
    beam(S, "f_test", (262, 1040), (PASTILLE_TEST[0] - PASTILLE_DOCK_W * PASTILLE_TEST_K / 2 + 8,
                                     PASTILLE_TEST[1] + 10))            # S19
    wire(S, "f_designe", 12.2, AI_INK, BEAM["sw"], pa=DESIGNE_A, pb=DESIGNE_B, dash=BEAM["dash"], dots=True)
    S.set("f_designe", via=list(DESIGNE_VIA))                           # S17 : « Vois un conseiller » -> le conseiller

    # --- la réponse d'aplomb (Sheet(3)), son reflet, les coches de l'IA, la bulle « ? » ---
    S.add("reflet", "sheen", z=10, w=SHEET_A.w, h=SHEET_A.h, under=True)
    S.set("reflet", p=0)
    card(kit, SHEET_A, "reponse", LINES_A, CARD_C, 0, sheen_id="reflet")
    SHEET_A.ticks(kit, "reponse_ia", AI_TICK, size=40, sw=8, variant="ai")
    head_tip = (toi_head()[0] - 26, toi_head()[1] - 20)
    S.add("doute", "bubble", z=11.7, big=DOUTE_BIG, small=DOUTE_SMALL,
          tail=[head_tip[0] - DOUTE_C[0], head_tip[1] - DOUTE_C[1]], tailBase=[18, 58])
    S.set("doute", pos=list(DOUTE_C), scale=0, s=0, q=1, glyph=0, pulse=0, opacity=1, rot=0)

    # --- la case « Source » (monde) : tirets deep, silhouette de livre, mot « Source » ---
    kit.shape("source", list(SOURCE_SMALL_C), kind="round", w=SOURCE_SMALL_W, h=SOURCE_SMALL_H, r=12, fill="none",
              stroke=DEEP, sw=4, dash=[14, 10], shadow=0, z=9.5, scale=0)
    S.set("source", w=SOURCE_SMALL_W, h=SOURCE_SMALL_H, stroke=DEEP)   # hex : DEEP -> RED (S02) -> DEEP (S04)
    lh = round(LIVRE_W * 0.61, 1)
    kit.shape("source_livre", [0, 0], kind="poly", pts=book_pts(LIVRE_W, lh), fill="none", stroke=DEEP, sw=3,
              dash=[10, 8], shadow=0, z=9.55, parent="source", scale=SILH_SMALL_K)
    S.set("source_livre", stroke=DEEP)
    line(kit, "source_livre_dos", [(0, -lh / 2 + 8), (0, lh / 2)], color=DEEP, sw=3, z=9.56, parent="source_livre",
         dash=[10, 8])
    S.set("source_livre_dos", draw=1)
    kit.text("source_mot", list(SOURCE_MOT_SMALL), T_SOURCE, size=32, weight=700, z=9.5, scale=0)

    # --- S08 : les sondes du stylo (ligne pleine deep : de la valeur, sous le texte, jusqu'à la case « Source ») ---
    for i in range(3):
        y = SHEET_A.rows[i] + CARD_C[1] + SHEET_A.ly
        yb = max(SOURCE_BIG_C[1] - 60, min(SOURCE_BIG_C[1] + 60, y))
        line(kit, f"sonde{i + 1}", [(696, y), (300, y), (SOURCE_BIG_C[0] + SOURCE_BIG_W / 2 - 4, yb)], color=DEEP, sw=5,
             z=9.7)

    # --- le livre (BOOK.png), son cadre ---
    livre = png(S, "livre", "BOOK", LIVRE_W, SOURCE_BIG_C, z=7)
    kit.shape("cadre_livre", list(SOURCE_BIG_C), kind="round", w=CADRE_LIVRE_W, h=CADRE_LIVRE_H, r=18, fill="none",
              stroke=DEEP, sw=5, shadow=0, z=7.2, draw=0)

    # --- la boule de cristal (CRYSTAL.png) et son éclat ---
    png(S, "boule", "CRYSTAL", BOULE_W, BOULE_TETE, z=7)
    S.add("eclat_boule", "burst", z=7.1, r0=70, r1=118, n=8, sw=6, color=LIGHT, a0=-90)
    S.set("eclat_boule", pos=list(BOULE_CHOIX), scale=1, opacity=1, p=0)

    # --- S14 : deux cases de coche vides (tirets encre) : celle de la boule, celle de la carte ---
    for cid, c in (("case_boule", CASE_BOULE), ("case_carte", _COCHE_CARTE)):
        kit.shape(cid, list(c), kind="round", w=CASE_W, h=CASE_W, r=8, fill=PAPER, stroke=INK, sw=4, dash=[9, 7],
                  shadow=0, z=10.8, scale=0)

    # --- le retour en arrière (S04) ---
    kit.icon("rembobiner", list(REWIND_C), "rewind", disc=REWIND_R, fill=LIGHT, color=INK, z=12, scale=0)

    # --- les bulles de l'IA et leurs textes ---
    ai_bubble(kit, "pensee", PENSEE_C, PENSEE_W, PENSEE_H, 50)                    # pensée (S03-S04)
    thought_dots(kit, "pensee_rond", PENSEE_RONDS)
    kit.text("pensee_txt", [0, 2], T_JNSP, size=36, weight=700, z=13.1, parent="pensee", typed=True)

    ai_bubble(kit, "citation", CITATION_C, CITATION_W, CITATION_H, 30, tip=IA_MOUTH, speech=True, base=60)   # parole (S12)
    cx = CITATION_C[0]
    x2 = cx - text_width(T_CIT2A + T_CIT2B, 30, 700) / 2
    x3 = cx - text_width(T_CIT3A + T_CIT3B + T_CIT3C, 30, 700) / 2
    loc = lambda x, y: [round(x - CITATION_C[0], 1), round(y - CITATION_C[1], 1)]   # noqa: E731
    kit.text("cit_l1", loc(cx, CIT_Y[0]), T_CIT1, size=30, weight=700, z=13.1, parent="citation", typed=True)
    kit.text("cit_l2a", loc(x2, CIT_Y[1]), T_CIT2A, size=30, weight=700, anchor="start", z=13.1, parent="citation",
             typed=True)
    S.set("cit_l2a", mark=0)
    kit.text("cit_l2b", loc(x2 + text_width(T_CIT2A, 30, 700), CIT_Y[1]), T_CIT2B, size=30, weight=700,
             anchor="start", z=13.1, parent="citation", typed=True)
    kit.text("cit_l3a", loc(x3, CIT_Y[2]), T_CIT3A.strip(), size=30, weight=700, anchor="start", z=13.1,
             parent="citation", typed=True)
    x3b = x3 + text_width(T_CIT3A, 30, 700)
    kit.text("cit_l3b", loc(x3b, CIT_Y[2]), T_CIT3B, size=30, weight=700, anchor="start", z=13.1, parent="citation",
             typed=True)
    S.set("cit_l3b", under=0)
    kit.text("cit_l3c", loc(x3b + text_width(T_CIT3B, 30, 700), CIT_Y[2]), T_CIT3C, size=30, weight=700,
             anchor="start", z=13.1, parent="citation", typed=True)

    ai_bubble(kit, "bulle_conseil", CONSEIL_C, CONSEIL_W, CONSEIL_H, 30, tip=CONSEIL_TIP, speech=True)   # S17
    kit.text("bulle_conseil_txt", [0, 2], T_CONSEIL, size=30, weight=700, z=13.1, parent="bulle_conseil", typed=True,
             lh=1.18)

    # S20 : « Je ne sais pas » naît en PENSÉE (pointillés + ronds) et devient PAROLE sur « dit » (contour plein,
    # pointe pleine, ronds rentrés) : bulle de base pointillée + contour plein par-dessus (opacité 0 -> 1).
    ai_bubble(kit, "bulle_jnsp", JNSP_C, JNSP_W, JNSP_H, 30)
    kit.shape("bulle_jnsp_trait", [0, 0], kind="round", w=JNSP_W, h=JNSP_H, r=30, fill="none", stroke=INK, sw=4,
              shadow=0, z=13.02, parent="bulle_jnsp", opacity=0)
    o, pts = _tail_pts(JNSP_C, JNSP_W, JNSP_H, IA_MOUTH, 70)
    kit.shape("bulle_jnsp_pointe", o, kind="poly", pts=pts, closed=True, fill=PAPER, stroke=INK, sw=4, shadow=0,
              z=12.95, parent="bulle_jnsp", scale=0)
    thought_dots(kit, "jnsp_rond", JNSP_RONDS)
    kit.text("bulle_jnsp_txt", [-30, 2], T_JNSP, size=36, weight=700, z=13.1, parent="bulle_jnsp", typed=True)
    kit.tick("coche_jnsp", list(JNSP_TICK_LOCAL), DEEP, size=44, sw=8, z=13.2, parent="bulle_jnsp")
    kit.shape("onde_jnsp", list(JNSP_TAP), kind="circle", w=56, fill="none", stroke=DEEP, sw=5, shadow=0, z=13.3,
              opacity=0)
    for k, r in enumerate((14, 26)):            # S20 « dit » : deux petits arcs de voix à la bouche
        line(kit, f"son_arc{k + 1}", arc_pts(0, r, -50, 50), color=AI_INK, sw=4, z=12.9, pos=(IA_MOUTH[0] - 4,
             IA_MOUTH[1] + 22), dash=[0.01, 8])
        S.set(f"son_arc{k + 1}", opacity=0)

    # --- l'argent de « Toi » : pile (groupe invisible, origine au sol), fil (et son double rouge) ---
    kit.shape("pile", list(PILE_C), kind="rect", w=1, h=1, fill="none", stroke="none", sw=0, shadow=0, z=10, scale=0)
    S.set("pile", rot=0)
    for k in range(7):
        kit.shape(f"piece{k + 1}", list(PIECE_LOCAL[k]), kind="ellipse", w=PIECE_W, h=PIECE_H, fill=LIGHT, stroke=INK,
                  sw=4, shadow=6, z=round(10.1 + 0.1 * k, 2), parent="pile", scale=1 if k < 4 else 0)
    for k, op in ((2, 0), (4, 1), (7, 1)):       # « € » sur la pièce du dessus (2 : après la chute de 3 et 4, S09)
        kit.text(f"piece{k}_euro", [0, 1], T_EURO, size=30, weight=800, z=round(10.15 + 0.1 * (k - 1), 2),
                 parent=f"piece{k}", opacity=op)
    wire(S, "fil_jetons", 9.8, INK, 4, a={"id": "reponse", "at": list(FIL_JETONS_A)},
         b={"id": "pile", "at": list(PILE_TOP_LOCAL)}, dash=[14, 10])
    wire(S, "fil_jetons_rouge", 9.85, RED, 7, a={"id": "reponse", "at": list(FIL_JETONS_A)},
         b={"id": "pile", "at": list(PILE_TOP_LOCAL)}, dash=[14, 10], draw=1, opacity=0)

    # --- la réponse prudente (Sheet(4)), ses coches, son surligneur, son cadre de L4, le tampon ---
    card(kit, SHEET_B, "bonne_reponse", LINES_B, CARD_B_C, 0, bullet_on=0)
    kit.tick("coche_toi", list(COCHE_TOI_LOCAL), DEEP, size=70, sw=10, z=11, parent="bonne_reponse")
    kit.tick("coche_source", [SHEET_B.x["tick"], SHEET_B.rows[1] + SHEET_B.ty + 4], DEEP, size=44, sw=9, z=11,
             parent="bonne_reponse")         # S13 : vérifié dans le livre
    kit.shape("surligne_L4", [SURL_L4_X0, SURL_L4_Y], kind="rect", w=SURL_L4_W, h=SURL_L4_H, fill=LIGHT,
              stroke="none", sw=0, shadow=0, z=8.6, parent="bonne_reponse")
    S.set("surligne_L4", w=0)                   # S13 « prudente » : w 0 -> SURL_L4_W et pos -> SURL_L4_C (même clé)
    kit.shape("cadre_L4", [0, SHEET_B.rows[3]], kind="round", w=CADRE_L4_W, h=CADRE_L4_H, r=16, fill="none",
              stroke=DEEP, sw=6, shadow=0, z=9.6, parent="bonne_reponse", draw=0)
    kit.stamp("tampon", list(TAMPON_LOCAL), T_TAMPON, TAMPON_W, TAMPON_H, size=TAMPON_SIZE, rot=-6,
              parent="bonne_reponse", scale=0, opacity=0, handle=1)
    S.set("tampon", lite=0)

    # --- le fil de la source : puce de L2 -> bord droit du livre (et son double épais) ---
    fs_a = {"id": "bonne_reponse_L2", "at": [SHEET_B.x["bullet"] - GEOM["BULLET"]["r"], 0]}
    fs_b = {"id": "livre", "at": [round(LIVRE_W / 2 - 4, 1), 0]}
    wire(S, "fil_source", 9.2, DEEP, 5, a=fs_a, b=fs_b)
    wire(S, "fil_source_gras", 9.25, DEEP, 9, a=fs_a, b=fs_b, draw=1, opacity=0)
    kit.shape("point_source", [0, 0], kind="circle", w=20, fill=DEEP, stroke="none", sw=0, shadow=0, z=9.4, scale=0)
    kit.shape("onde_livre", list(LIVRE_TAP), kind="circle", w=60, fill="none", stroke=DEEP, sw=5, shadow=0, z=9.45,
              opacity=0)

    # --- la situation de « Toi » (FINGERPRINT.png) et son fil vers « ton cas » (7 px, point au bout) ---
    png(S, "empreinte", "FINGERPRINT", EMPREINTE_W, EMPREINTE_C, z=10)
    line(kit, "fil_empreinte", FIL_EMPREINTE_PTS, color=DEEP, sw=7, z=9.2)
    kit.shape("fil_empreinte_pt", list(FIL_EMPREINTE_PTS[-1]), kind="circle", w=20, fill=DEEP, stroke="none", sw=0,
              shadow=0, z=10.5, scale=0)

    # --- le conseiller (figurine papier, sans outil) et son étiquette (enfant) ---
    conseiller = Figure(kit, "conseiller", pos=list(CONSEILLER_C), scale=FIG_S, variant="paper", tool=False,
                        show=False)
    kit.ensure("conseiller", "look", 0)
    pill(S, "nom_conseiller", NOM_LOCAL, T_CONSEILLER, size=NOM_SIZE, fill=PAPER, h=NOM_H, z=15.8,
         parent="conseiller", scale=1)

    # --- les trois cas (et leurs cadres deep de S17) ---
    for i, c in enumerate(CAS_C):
        cid = f"cas{i + 1}"
        kit.shape(cid, list(c), kind="round", w=CAS_W, h=CAS_H, r=16, fill=PAPER, stroke=INK, sw=4, shadow=6, z=9.5,
                  scale=0)
        kit.text(f"{cid}_txt", list(CAS_TXT_LOCAL), T_CAS[i], size=30, weight=700, anchor="start", z=9.6,
                 parent=cid, typed=True, lh=1.15)
        kit.shape(f"cadre_cas{i + 1}", list(c), kind="round", w=CAS_W + 18, h=CAS_H + 14, r=22, fill="none",
                  stroke=DEEP, sw=4, shadow=0, z=9.45, draw=0)
    kit.shape("cas1_disque", list(CAS_OBJ_LOCAL), kind="circle", w=60, fill=CYAN, stroke=INK, sw=3, shadow=3, z=9.65,
              parent="cas1")
    kit.text("cas1_signe", [0, 2], T_SIGNE, size=40, weight=800, z=9.7, parent="cas1_disque")

    # --- la sonnette (BELL.png) et ses trois ondes (enfants, flanc droit ; piste rot pour les orienter) ---
    png(S, "sonnette", "BELL", SONNETTE_W, SONNETTE_C, z=7)
    for k in range(3):
        line(kit, f"sonnette_onde{k + 1}", arc_pts(40, 34 + 16 * k), color=DEEP, sw=6, z=7.1, parent="sonnette")
        S.set(f"sonnette_onde{k + 1}", rot=0)

    # --- les deux applis (contour tracé, barre de titre et trois points) et le cadre du choix ---
    for aid, c in (("appli_g", APPLI_G_C), ("appli_d", APPLI_D_C)):
        kit.shape(aid, list(c), kind="round", w=APPLI_W, h=APPLI_H, r=APPLI_R, fill=PAPER, stroke=INK, sw=4,
                  shadow=6, z=6, draw=0)
        kit.shape(f"{aid}_barre", [0, -APPLI_H / 2 + 40], kind="rect", w=APPLI_W - 4, h=4, fill=INK, stroke="none",
                  sw=0, shadow=0, z=6.1, parent=aid, opacity=0)
        for k in range(3):
            kit.shape(f"{aid}_point{k + 1}", [-APPLI_W / 2 + 26 + 22 * k, -APPLI_H / 2 + 20], kind="circle", w=12,
                      fill=INK, stroke="none", sw=0, shadow=0, z=6.1, parent=aid, opacity=0)
    kit.shape("cadre_appli", list(APPLI_D_C), kind="round", w=CADRE_APPLI_W, h=CADRE_APPLI_H, r=28, fill="none",
              stroke=DEEP, sw=6, shadow=0, z=6.2, draw=0)

    # --- le test : la cible retournée (TARGET.png), la pilule de « Toi » (enfant, vide jusqu'à S19 : elle annonce
    #     le test dès S03), celle de l'IA (monde, pointillés), coche, deux ondes ---
    cible = png(S, "cible", "TARGET", CIBLE_W, CIBLE_S03, z=13, flip=True)
    kit.shape("test_toi", list(MILLE_LOCAL), kind="round", w=TEST_W, h=TEST_H, r=TEST_H / 2, fill=LIGHT, stroke=DEEP,
              sw=4, shadow=0, z=13.2, parent="cible")
    kit.text("test_toi_txt", [0, 1], T_TEST, size=TEST_SIZE, weight=700, z=13.25, parent="test_toi", typed=True)
    kit.shape("test_ia", [0, 0], kind="round", w=TEST_W, h=TEST_H, r=TEST_H / 2, fill=PAPER, stroke=AI_INK, sw=4,
              dash=[0.01, 9], shadow=0, z=13.5, scale=0)
    kit.text("test_ia_txt", [0, 1], T_TEST, size=TEST_SIZE, weight=700, z=13.55, parent="test_ia")
    kit.tick("coche_cible", list(COCHE_CIBLE_LOCAL), DEEP, size=56, sw=9, z=13.3, parent="cible")
    for oid in ("onde_cible", "onde_cible2"):
        kit.shape(oid, list(MILLE_LOCAL), kind="circle", w=200, fill="none", stroke=DEEP, sw=5, shadow=0, z=13.6,
                  parent="cible", opacity=0)

    # --- Avant / Après ---
    pill(S, "etiq_avant", AVANT_C, T_AVANT, size=34, fill=PAPER, h=56, z=12)
    pill(S, "etiq_apres", APRES_C, T_APRES, size=34, fill=LIGHT, h=56, z=12)

    # --- la fin : ondes du toucher du stylo (le curseur de kit.outro reste invisible) ---
    for k in range(2):
        kit.shape(f"fin_onde{k + 1}", list(FIN_TAP), kind="circle", w=60, fill="none", stroke=DEEP, sw=5, shadow=0,
                  z=41.9, opacity=0)

    return SimpleNamespace(toi=toi, conseiller=conseiller, sheet_a=SHEET_A, sheet_b=SHEET_B, rep_a=REP_A_IDS,
                           rep_b=REP_B_IDS, ticks_a=TICK_A_IDS, ai=ai, livre=livre, cible=cible)


def build(S):
    kit = Kit(S)
    c = cast(S, kit)
    only = [p for p in os.environ.get("WTH_PARTS", "").split(",") if p]   # WTH_PARTS=p2 : cette partie seule
    for name in PARTS:
        if not only or name in only:
            importlib.import_module(f".{name}", __name__).part(S, kit, c)
