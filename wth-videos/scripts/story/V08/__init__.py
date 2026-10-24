"""V08 « Ton vrai reste à vivre en 3 étapes » : mise en scène Story, en paquet (une partie par fichier).

Storyboard : scripts/storyboards/V08.json (v1, révisé après le test sans son, 22 scènes, 94 temps forts, 95,709 s),
version lisible scripts/storyboards/V08.md. Voix : build/V08/words.json (film : images 0-2872).
Fil : la pastille cyan du reste à vivre (`pastille`, pill 260 x 84, ExtraBold 44) posée sur l'argent du mois de
« Toi » : « Salaire » (S01) -> « ? € » (S02) -> « = » la partie cyan `reste` (S06) -> « 850 € / mois » (S17) ->
« ≈ 28 € / jour » (S18) -> « ? € / jour » quand la mensualité tombe (S20) -> bouton « S’abonner » (S22).
Parti pris : UNE colonne d'argent (`revenus`) posée au sol ; les charges (`charges`, une pile de blocs papier)
tombent dessus et la couvrent par le bas ; ce qui reste découvert en haut, en cyan, c'est le reste à vivre.

Parties (scènes contiguës, coupées là où la composition change, sur un morph) :
- p1 : S01-S06, images 0-737. Accroche (enveloppe, colonne qui tombe, « ? € », panier), annonce 1-2-3, contexte
  (≠ rouge, maison, cadenas, loyer / factures / crédits, haut cyan, accolades, « = »).
- p2 : S07-S14, images 738-1805. Étape 1 (socle « chaque mois », bon mois -> Prime écartée, colonne « Revenus »
  740 px) et étape 2 (les charges se servent, coches, 3 relevés, pièges rouges, moyenne, « Charges »).
- p3 : S15-S22, images 1806-2872. Étape 3 (face à face, 2 200 € − 1 350 €, 850 € / mois), 30 jours, ≈ 28 € / jour
  et 4 usages, la banque et la mensualité, « ? € / jour », carte de fin.
ENTRY_P2 et ENTRY_P3 sont le contrat des raccords (kit.pin à first_frame - 1). Les figurines n'y sont jamais.

Repères des deux GROUPES (formes invisibles, origine au BAS-CENTRE, sur le sol y 1180) : `revenus` (la colonne :
billets `salaire`, `allocations`, `autres`, `socle`, mots, partie cyan `reste`) et `charges` (la pile : `loyer`,
`factures`, `credits`, `abonnements`, coches, mot « Charges »). Les enfants sont en repère local (y < 0 = au-dessus
du sol). Quand la pile est posée sur la colonne (S16-S22), les deux groupes ont la même `pos` et la même `scale` :
leur poser LES MÊMES clés les garde collés (S18 rangement, S19 retour).

Pas d'IA dans V08. « Toi » (figurine encre, side « left », échelle 1, pieds sur y 1230) est seul à tenir le stylo ;
nommé dès l'image 0 par `nom_toi` (pilule light, enfant de la figurine : il la suit). Entre deux gestes son bras est
BAISSÉ (`lower` / `hold_low` / `walk_low`, repris de V07). Places : P1 (860, 1135) S01-S06 ; P2 (790, 1135) S07-S10,
S12-S14 ; P3 (755, 1135) S11 ; P1_R (870, 1135) S15-S22. Le bras gauche ne touche proprement qu'une cible à sa gauche
(|dx| >= 0,3 x dy) à 267 px au plus : `assert_reach(x_figurine, cible, quoi)` avant chaque geste.
La banque (S19-S21) : figurine papier sans outil (`banque`, Figure tool=False), pilule `banque_nom` enfant.
Rouge : « ≠ » (S04-S05), le contour de la Prime (S09), les trois pièges des relevés (S13) ; karaoké « trompe »,
« tromper ». Pas de gris de mise en retrait. Aucune entité nouvelle (compositions du catalogue).
"""
import importlib
import math
import os
from types import SimpleNamespace

from pipeline.story import GEOM, STYLE, text_width
from pipeline.story_kit import Figure, Kit, ang_lerp, frames, lerp, solve_ik

PARTS = ["p1", "p2", "p3"]                      # S01-S06, S07-S14, S15-S22
NBSP = " "                                 # espace insécable
ALERT_WORDS = {"trompe", "tromper"}             # karaoké en rouge : le « ≠ » (S04), les pièges des relevés (S13)
ACOUSTIC_SNAP = {"gap": 0.2, "window": 0.08}    # temps fort après un silence : calé sur l'attaque audible
# CAPTION_GROUPS : aucune découpe imposée (à n'ajouter que si une découpe automatique est fausse).

# ---------- couleurs ----------
INK, CYAN, DEEP, LIGHT = STYLE["ink"], STYLE["cyan"], STYLE["deep"], STYLE["light"]
PAPER, RED, BG = STYLE["paper"], STYLE["red"], STYLE["bg"]

# ---------- textes à l'écran (typographie française : insécable avant €, ?, vrai signe moins) ----------
T_TOI, T_BANQUE = "Toi", "Banque"
T_SALAIRE, T_NET = "Salaire", "net"
T_Q_EUR = f"?{NBSP}€"
T_850 = f"850{NBSP}€"
T_850_MOIS = f"850{NBSP}€ / mois"
T_28_JOUR = f"≈{NBSP}28{NBSP}€ / jour"
T_28 = f"≈{NBSP}28{NBSP}€"                     # S20 : le morceau qui se détache et tombe de la pastille
T_Q_JOUR = f"?{NBSP}€ / jour"
T_ABONNER = "S’abonner"
T_RESTE = "reste à vivre"
T_NE, T_EG = "≠", "="
T_ACC_REVENUS, T_ACC_CHARGES = "revenus", f"−{NBSP}charges"
T_CHAQUE_MOIS, T_BON_MOIS, T_PRIME = "chaque mois", "bon mois", "Prime"
T_PLUS, T_MOINS = "+", "−"
T_ALLOC, T_AUTRES = "Allocations", "Autres revenus"
T_REVENUS, T_CHARGES = "Revenus", "Charges"
T_RELEVE, T_MOIS = "Relevé", ["mois 1", "mois 2", "mois 3"]
T_PIEGES = ["facture\nannuelle", "sans\nprime", "dépense\noubliée"]
T_TROIS, T_MOYENNE = "3", "moyenne sur 3 mois"
T_CREDIT_Q = f"Un crédit{NBSP}?"
T_TAUX = "taux\nd’endettement"
T_USAGES = ["courses", "loisirs", "imprévus", "épargne"]
MARKER_LABELS = ["Revenus", "Charges", "Soustraire"]

# ---------- mise en page (1080 x 1920) ----------
X_MIN, X_MAX, Y_MIN, Y_MAX = 40, 940, 160, 1270
GROUND = 1230                                   # ligne de sol : pieds de « Toi » et de la banque
FLOOR = 1180                                    # bas des colonnes (origine des groupes `revenus` et `charges`)
FIG_BASE = GEOM["FIGURE"]["base"]
HEAD_DY = GEOM["FIGURE"]["head"]["cy"]          # -64 : centre de la tête
HEAD_R = GEOM["FIGURE"]["head"]["r"]
SHOULDER_DX, SHOULDER_DY = abs(GEOM["FIGURE"]["shoulder"][0]), GEOM["FIGURE"]["shoulder"][1]   # 30, -16
REACH_OK = 267
TOI_SCALE = 1.0


def fig_pos(x, feet=GROUND, s=TOI_SCALE):
    return [x, round(feet - FIG_BASE * s, 2)]


P1 = fig_pos(860)                               # (860, 1135) : S01-S06 (cadenas 612,983 : 257 px ; loyer 575,1085 : 257)
P2 = fig_pos(790)                               # (790, 1135) : S07-S10, S12-S14
P3 = fig_pos(755)                               # (755, 1135) : S11, contre la pile (crédits 645,870 : 262 px, côté sûr)
P1_R = fig_pos(870)                             # (870, 1135) : S15-S22 (tap 772,1100 : 71 px ; bouton 690,950 : 215)
NOM_TOI_LOCAL, NOM_TOI_W, NOM_TOI_H = (0, -135), 96, 54   # pilule « Toi » au-dessus de la tête (monde y 1000)
BANQUE_POS = fig_pos(190)                       # (190, 1135) : S19-S21, face à « Toi », la colonne entre eux
BANQUE_NOM_LOCAL = (0, -145)                    # pilule « Banque » (monde 190, 990), grand pictogramme bank r 30
BANQUE_TETE = (215, 1065)                       # départ du regard (bord droit de la tête)

# --- le repère 1-2-3 légendé (en haut) ---
MARKER_Y, MARKER_CX, MARKER_GAP = 280, 540, 188  # disques x 352, 540, 728 ; légende Bold 32 (« Soustraire » 161 px)
MARKER_LABEL_SIZE = 32

# --- l'enveloppe de paie (WTH-004-01) et la maison des charges (WTH-004-05) ---
ENVELOPPE_C, ENVELOPPE_W = (420, 420), 340      # y ≈ 305-535
ENVELOPPE_BOUCHE = (420, 470)                   # S01 : la colonne naît ici
MAISON_C, MAISON_W = (200, 470), 300            # S04-S05, en haut à gauche
MAISON_SORTIE = (200, 520)                      # S04 : les blocs sortent d'ici

# --- la pastille (objet du fil) ---
PASTILLE_W, PASTILLE_H = 260, 84
PASTILLE_W_MOIS, PASTILLE_W_JOUR, PASTILLE_W_Q_JOUR = 340, 380, 300
PASTILLE_S00 = (420, 400)                       # image 0 : dépasse de la bouche de l'enveloppe
PASTILLE_S01 = (420, 575)                       # S01 : posée sur le sommet de la colonne (haut y 620)
PASTILLE_S02 = (420, 470)                       # S02-S03 : au-dessus de la colonne
PASTILLE_S04 = (780, 700)                       # S04-S06 : en face du haut de la colonne
PASTILLE_ATTENTE, PASTILLE_ATTENTE_K = (780, 410), 0.85   # S07-S16 : en attente en haut à droite
PASTILLE_S17 = (690, 720)                       # S17 : sous le trait de total (bord gauche x 520 à 340 px)
PASTILLE_S18 = (540, 430)                       # S18 : au centre en haut
PASTILLE_S19 = (480, 390)                       # S19-S21 : au-dessus de la colonne
_TW28, _TW28P = text_width(T_28_JOUR, 44, 800), text_width(T_28, 44, 800)
PASTILLE_28_DX = round(-_TW28 / 2 + _TW28P / 2, 1)   # S20 : centre du morceau « ≈ 28 € » (repère de la pastille)

# --- la légende « reste à vivre » ---
LEGENDE_S03 = (420, 552)                        # sous la pastille (deep)
LEGENDE_S04 = (780, 790)                        # la suit (deep)
LEGENDE_S06 = (420, 703)                        # sur la partie cyan (encre)
LEGENDE_S17 = (290, 583)
LEGENDE_S19 = (480, 583)
LEGENDE_S20 = (480, 538)                        # remonte quand le cyan rétrécit

# --- la colonne d'argent `revenus` (groupe, origine au bas-centre) ---
COL_W = 300
COL_S01 = (420, FLOOR)                          # S01-S06 : x 270-570
COL_S07 = (480, FLOOR)                          # S07-S09 : x 330-630
COL_RANGE, COL_RANGE_K = (110, FLOOR), 0.4      # S10-S14 et S18 : rangée en petit à gauche (y 884-1180)
COL_S15 = (290, FLOOR)                          # S15-S17 : x 140-440
COL_S19 = (480, FLOOR)                          # S19-S22
SALAIRE_H, ALLOC_H, AUTRES_H = 560, 100, 80     # 740 px en tout
SALAIRE_LOCAL = (0, -SALAIRE_H / 2)             # gauge verticale (dir up, segPx 80 : 7 billets)
ALLOC_LOCAL = (0, -(SALAIRE_H + ALLOC_H / 2))   # (0, -610) : y 520-620 au sol de S07
AUTRES_LOCAL = (0, -(SALAIRE_H + ALLOC_H + AUTRES_H / 2))   # (0, -700) : y 440-520
ALLOC_ENTREE = (780, 570)                       # S08 : les blocs entrent par la droite (monde ; bord droit 930 < 940, QA zones)
SOCLE_LOCAL, SOCLE_W, SOCLE_H = (0, 12), 340, 22
CHAQUE_MOIS_LOCAL = (0, -40)                    # monde y 1140
MOT_PIED_LOCAL = (0, 48)                        # « Revenus » / « Charges » sous le socle (monde y 1228)
_SW, _NW = text_width(T_SALAIRE, 36, 700), text_width(T_NET, 36, 800)
MOT_SALAIRE_LOCAL = (0, -528)                   # monde y 652 (sur le haut du billet du haut)
MOT_SALAIRE_NET_LOCAL = (round(-(_SW + 12 + _NW) / 2 + _SW / 2, 1), -528)   # S08 : « Salaire » glisse à gauche
NET_LOCAL = (round(-(_SW + 12 + _NW) / 2 + _SW + 12, 1), -528)              # « net » ancré à gauche, après lui

# --- la partie cyan `reste` (enfant de `revenus` ; forme rect : pistes h et pos ensemble = bas fixe) ---
RESTE_S05 = dict(bottom=-394, h=166)            # S05-S06 : y 620-786 (au-dessus de Loyer/Factures/Crédits)
RESTE_S17 = dict(bottom=-454, h=286)            # S17-S20 : y 440-726 (au-dessus des 4 charges)
RESTE_S20 = dict(bottom=-544, h=196)            # S20-S21 : y 440-636 (au-dessus de la mensualité)


def reste_pos(bottom, h):
    """Position locale du centre de `reste` dont le bas est à `bottom` (repère de `revenus`) et la hauteur h."""
    return [0, bottom - h / 2]


# --- la pile des charges `charges` (groupe, origine au bas-centre) ; blocs papier 300 px ---
PILE_S04 = (420, FLOOR)                         # S04-S06 : sur le bas de la colonne
PILE_RANGE_S07, PILE_RANGE_K = (175, 978.5), 0.5   # S07-S09 : rangée en petit à gauche (centre 175, 880)
PILE_S10 = (480, FLOOR)                         # S10-S11, S14 : au centre
PILE_S12, PILE_S12_K = (480, FLOOR), 0.5        # S12-S13 : réduite en bas au centre
PILE_S15 = (620, FLOOR)                         # S15 : face à face, x 470-770
PILE_S16 = COL_S15                              # S16-S17 : posée sur le bas des revenus
BLOCS = [("loyer", "Loyer", "house", 190, 26, 34), ("factures", "Factures", "mail", 104, 26, 34),
         ("credits", "Crédits", "bank", 100, 26, 34), ("abonnements", "Abonnements", "phone", 60, 20, 32)]
BLOC_LOCAL = {}                                 # centre local de chaque bloc (empilés depuis le sol)
_y = 0
for _bid, _t, _ic, _h, _r, _s in BLOCS:
    BLOC_LOCAL[_bid] = (0, -(_y + _h / 2))      # loyer -95, factures -242, crédits -344, abonnements -424
    _y += _h
PILE_TOP = {"S04": -394, "S11": -454}           # haut de la pile : y 786 (3 blocs), y 726 (4 blocs)
BLOC_ICON_X, BLOC_TEXT_X = -110, -70            # pictogramme sur disque light ; mot ancré à gauche
BLOC_ICON_X_PETIT, BLOC_TEXT_X_PETIT = -118, -88   # « Abonnements » (Bold 32, 220 px)
MENSUALITE_C, MENSUALITE_H = (480, 681), 90     # S20 : y 636-726, sur les 4 charges
COCHES_LOCAL = [(180, -95), (180, -240), (180, -310)]   # monde (660, 1085), (660, 940), (660, 870) pile en PILE_S10
TRACE_X = 645                                   # S11 : la pointe remonte le bord droit des blocs, aux y des coches

# --- S04-S06 : « ≠ », trait « une partie », cadenas, accolades ---
EGAL_C = (615, 700)
LIGNE_PARTIE_C, LIGNE_PARTIE_PTS = (420, 786), [[-160, 0], [160, 0]]   # x 260-580
CADENAS_C, CADENAS_R = (580, 983), 30
CADENAS_TAP = (612, 983)                        # S04 : la pointe bute sur le cadenas (depuis P1 : 257 px)
LOYER_TAP = (575, 1085)                         # S05 : « Toi » pousse le loyer
ACC_G_C, ACC_G_HALF = (252, 900), 280           # accolade gauche : x 252, y 620-1180
ACC_D_C, ACC_D_HALF = (622, 983), 197           # accolade droite : y 786-1180 ; x 622 (et non 590 : le cadenas
                                                # r 30 en x 580 la couvrirait), ouverte vers la gauche
ACC_REVENUS_NEE, ACC_REVENUS_C = (420, 900), (150, 900)
ACC_CHARGES_C = (735, 930)                      # x ≈ 652-818 (et non 705 : l'accolade est à 622)


def brace_pts(half, right=False):
    """Accolade verticale (poly ouverte), pointe vers l'extérieur ; repère local centré."""
    m = 1 if right else -1
    return [[-m * 14, -half], [0, -half + 14], [0, -14], [m * 12, 0], [0, 14], [0, half - 14], [-m * 14, half]]


# --- S07-S09 : « bon mois » -> « Prime », « + », calendriers ---
BON_MOIS_W, BON_MOIS_H, BON_MOIS_K = 300, 80, 0.65
BON_MOIS_SOMMET = (480, 580)                    # S07 : sur le sommet de la colonne
BON_MOIS_ATTENTE = (745, 880)                   # S07-S08 : à part, à droite (x 0,65)
PRIME_COLLE = (700, 880)                        # S09 : veut se coller au flanc de la colonne (rouge)
PRIME_TAP = (640, 900)                          # S09 : partie gauche du bloc (depuis P2 : 250 px, côté sûr)
PRIME_SOL = (175, 1140)                         # S09 : écartée, au sol à gauche
PLUS_C, PLUS_HAUT = (480, 585), (480, 485)
CAL_C, CAL_R = [(105, 1050), (175, 1050), (245, 1050)], 30
REVENUS_TAP = (632, 1060)                       # S08 : « Toi » touche le bord droit de la colonne

# --- S10-S11 : pièces, panier, coches ---
PIECE_R, PANIER_R = 22, 26
PIECES_DEPART = (110, 900)                      # haut des revenus rangés
PANIER_S02_TIP = (600, 1010)                    # S02 : pointe tendue à 30 px de la colonne (depuis P1 : 254 px)
PANIER_S10_TIP = (690, 960)                     # S10 : vers les revenus, après les pièces (depuis P2 : 174 px)
ABOS_CHUTE_H = 240                              # S11 : « Abonnements » tombe d'en haut

# --- S12-S14 : relevés (formes : carte papier 180 x 240 + mots + barre), pièges, moyenne ---
RELEVE_C = [(250, 620), (460, 620), (670, 620)]  # y 500-740
RELEVE_W, RELEVE_H = 180, 240
RELEVE_TITRE_LOCAL, RELEVE_MOIS_LOCAL = (0, -96), (0, -66)
BARRE_W, BARRE_BAS = 60, 100                    # barre posée sur y local 100 (monde 720), origine en bas
BARRES_H = [140, 90, 60]                        # S13 ; S14 : toutes à BARRE_MOY
BARRE_MOY = 110                                 # haut à y local -10 (monde 610)
ROUGE1_H = 50                                   # mois 1 : les 50 px du haut virent au rouge
PRIME_MINI_LOCAL, PRIME_MINI_W, PRIME_MINI_H = (0, -16), 100, 44   # mois 2 : au-dessus de la barre
VIDE3_LOCAL, VIDE3_W, VIDE3_H = (0, 20), 60, 40  # mois 3 : sur le haut de la barre (y local 0-40)
PIEGE_LBL_Y = 790
TROIS_C = (460, 420)
MOYENNE_LIGNE_C, MOYENNE_LIGNE_PTS = (460, 610), [[-300, 0], [300, 0]]   # x 160-760
MOYENNE_TITRE_C = (460, 440)
CHARGES_TAP = (632, 1100)                       # S14 : « Toi » touche le bord droit de la pile

# --- S15-S17 : face à face, soustraction ---
NIVEAU_C, NIVEAU_PTS = (455, 726), [[315, 0], [-315, 0]]   # tracé de droite (770) à gauche (140)
CHARGES_TAP_S15 = (772, 1100)                   # S15-S16 : bord droit des charges (depuis P1_R : 71 px)
MOINS_PIED = (455, 1228)                        # « Revenus − Charges »
MOINS_CALCUL = (545, 590)
COMPTEUR_2200_C, COMPTEUR_1350_C = (860, 500), (860, 590)   # ancrés à droite
TOTAL_C, TOTAL_W, TOTAL_H = (690, 645), 340, 6  # x 520-860
FIL_RESTE_A, FIL_PASTILLE_B = (150, 0), (-170, 0)   # du bord droit du cyan au bout gauche de la pastille (340)

# --- S18 : les 30 jours (page de calendrier), les 4 usages ---
PAGE_C, PAGE_W, PAGE_H = (540, 690), 440, 400   # x 320-760, y 490-890
BANDEAU_LOCAL, BANDEAU_H = (0, -180), 40
ANNEAUX_LOCAL = [(-110, -200), (110, -200)]
JOUR_S, JOUR_STEP = 56, 66
JOURS_C = [(375 + JOUR_STEP * (k % 6), 578 + JOUR_STEP * (k // 6)) for k in range(30)]   # 6 x 5, centre (540, 710)
USAGE_PNG = [("panier_png", "WTH-004-03", 200, (330, 650)), ("valise", "SUITCASE", 150, (720, 650)),
             ("bouee", "BUOY", 200, (330, 920))]
EPARGNE_C = [(720, 950), (720, 920), (720, 890)]   # pile de 3 pièces (coin, disque light r 26)
USAGE_MOT_C = [(330, 760), (720, 760), (330, 1040), (720, 1040)]

# --- S19-S21 : bulle, banque, regard, taux, « ? » ---
BULLE_C, BULLE_W, BULLE_H = (770, 880), 240, 80
BULLE_QUEUE = [[10, 36], [62, 82], [40, 36]]    # repère de la bulle : pointe (832, 962) vers la tête de « Toi »
CREDITS_REGARD = (330, 836)                     # S19 : bord gauche du bloc « Crédits » (colonne en COL_S19)
RESTE_REGARD, RESTE_REGARD_APRES = (330, 583), (330, 538)
TAUX_C = (170, 770)
QUESTION_C, QUESTION_GS = (870, 900), 110

# --- S22 : fin (kit.outro, pos (540, 760), 620 x 520 : bouton ≈ (540, 908), x 350-730) ---
FIN_C = (540, 760)
FIN_BUTTON = (540, 908)
FIN_TAP = (690, 950)                            # bas droit du bouton, hors du libellé (depuis P1_R : 215 px)
BTN_W, BTN_H = 380, 112

# ---------- identifiants ----------
BLOC_IDS = [b[0] for b in BLOCS]                # loyer, factures, credits, abonnements (enfants de `charges`)
COCHES = ["coche1", "coche2", "coche3"]         # S11 : loyer, factures, crédits (enfants de `charges`)
CALENDRIERS = ["cal1", "cal2", "cal3"]
PIECES = ["piece1", "piece2", "piece3"]
RELEVES = ["releve1", "releve2", "releve3"]
BARRES = ["barre1", "barre2", "barre3"]         # enfants des relevés
PIEGES_LBL = ["piege1", "piege2", "piege3"]     # légendes rouges sous les relevés
JOURS = [f"jour{k + 1}" for k in range(30)]
EPARGNE = ["epargne1", "epargne2", "epargne3"]
USAGE_MOTS = ["mot_courses", "mot_loisirs", "mot_imprevus", "mot_epargne"]


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
    assert 63 <= d <= REACH_OK and safe and clear >= HEAD_R + 8, \
        f"{what} : hors d'allonge depuis x {fig_x} ({side}) : {d} px, côté sûr {safe}, tête {clear} px"


# ---------- bras baissé (pose de repos de V06/V07) ----------
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


def charge_block(kit, id, pos, label, icon, h, r, size, z, parent=None, scale=1):
    """Bloc de charge : forme papier 300 x h, pictogramme sur disque light, mot Bold (ancré à gauche)."""
    small = h < 80
    kit.shape(id, list(pos), kind="round", w=COL_W, h=h, r=14, fill=PAPER, stroke=INK, sw=4, shadow=6, z=z,
              parent=parent, scale=scale)
    kit.S.set(id, stroke=INK)
    ix, tx = (BLOC_ICON_X_PETIT, BLOC_TEXT_X_PETIT) if small else (BLOC_ICON_X, BLOC_TEXT_X)
    kit.icon(f"{id}_icone", [ix, 0], icon, disc=r, fill=LIGHT, shadow=3 if r < 25 else 4, z=z + 0.2, parent=id)
    kit.text(f"{id}_mot", [tx, 0], label, size=size, weight=700, anchor="start", z=z + 0.2, parent=id)
    return id


# ---------- raccords ----------
_OFF = lambda *ids: {i: {"scale": 0} for i in ids}   # noqa: E731

ENTRY_P2 = {   # fin de S06 = etat_initial de S07 (image 737) : colonne, haut cyan nommé, charges verrouillées, « = »
    "revenus": {"pos": list(COL_S01), "scale": 1},
    "salaire": {"scale": 1},
    "mot_salaire": {"pos": list(MOT_SALAIRE_LOCAL), "scale": 1},
    "reste": {"pos": reste_pos(**RESTE_S05), "h": RESTE_S05["h"], "scale": 1},
    "legende_reste": {"pos": list(LEGENDE_S06), "scale": 1, "chars": len(T_RESTE), "color": INK.lower()},
    "charges": {"pos": list(PILE_S04), "scale": 1},
    **{b: {"pos": list(BLOC_LOCAL[b]), "scale": 1} for b in ("loyer", "factures", "credits")},
    "cadenas": {"pos": list(CADENAS_C), "scale": 1},
    "egal": {"pos": list(EGAL_C), "scale": 1, "text": T_EG, "color": DEEP.lower()},   # minuscules : _mix sort du hex minuscule
    "ligne_partie": {"draw": 1},
    "socle": {"sx": 0}, "net": {"chars": 0, "under": 0},
    "accolade_g": {"draw": 1}, "accolade_d": {"draw": 1},
    "acc_revenus": {"pos": list(ACC_REVENUS_C), "scale": 1},
    "acc_charges": {"pos": list(ACC_CHARGES_C), "scale": 1},
    "pastille": {"pos": list(PASTILLE_S04), "scale": 1, "text": T_Q_EUR, "w": PASTILLE_W, "textOp": 1},
    "marqueur": {"pos": [MARKER_CX, MARKER_Y], "scale": 1, "on": 0, "active": 0, "lbl": 1},
    **_OFF("enveloppe", "maison", "panier", "abonnements", "chaque_mois", "bon_mois", "plus", "allocations",
           "autres", "mot_revenus"),
}
ENTRY_P3 = {   # fin de S14 = etat_initial de S15 (image 1805) : pile « Charges » au centre, revenus rangés à gauche
    "revenus": {"pos": list(COL_RANGE), "scale": COL_RANGE_K},
    "salaire": {"scale": 1},
    "allocations": {"pos": list(ALLOC_LOCAL), "scale": 1},
    "autres": {"pos": list(AUTRES_LOCAL), "scale": 1},
    "socle": {"sx": 1, "scale": 1},
    "mot_salaire": {"pos": list(MOT_SALAIRE_NET_LOCAL), "scale": 1},
    "net": {"chars": len(T_NET), "under": 1, "scale": 1},
    "mot_revenus": {"scale": 1},
    "charges": {"pos": list(PILE_S10), "scale": 1},
    **{b: {"pos": list(BLOC_LOCAL[b]), "scale": 1} for b in BLOC_IDS},
    **{c: {"draw": 1} for c in COCHES},
    "mot_charges": {"scale": 1},
    "pastille": {"pos": list(PASTILLE_ATTENTE), "scale": PASTILLE_ATTENTE_K, "text": T_Q_EUR, "w": PASTILLE_W},
    "marqueur": {"pos": [MARKER_CX, MARKER_Y], "scale": 1, "on": 1, "active": 1, "done0": 1, "done1": 0},
    **_OFF("reste", "legende_reste", "chaque_mois", "egal", "cadenas", "acc_revenus", "acc_charges", "bon_mois",
           "plus", *CALENDRIERS, *PIECES, "panier", *RELEVES, *PIEGES_LBL, "trois", "moyenne_titre"),
    "moyenne_ligne": {"draw": 0}, "ligne_partie": {"draw": 0}, "accolade_g": {"draw": 0}, "accolade_d": {"draw": 0},
}


def cast(S, kit):
    """Toute la distribution, à son état de l'image 0. Ce qui arrive plus tard : scale=0 (ou draw=0, chars=0,
    sx=0). Seuls `fin` et `fin_curseur` naissent dans kit.outro (p3)."""

    # --- l'enveloppe de paie (image 0, en haut) et la maison des charges (S04) ---
    env = S.png("WTH-004-01")
    S.add("enveloppe", "png", z=4, src=env["src"], w=ENVELOPPE_W, h=round(ENVELOPPE_W * env["h"] / env["w"]),
          contact=dict(w=round(ENVELOPPE_W * 0.75), h=24, dy=4, blur=10, alpha=0.18))
    S.set("enveloppe", pos=list(ENVELOPPE_C), scale=1, opacity=1)
    mai = S.png("WTH-004-05")
    S.add("maison", "png", z=4, src=mai["src"], w=MAISON_W, h=round(MAISON_W * mai["h"] / mai["w"]),
          contact=dict(w=round(MAISON_W * 0.75), h=24, dy=4, blur=10, alpha=0.18))
    S.set("maison", pos=list(MAISON_C), scale=0, opacity=1)

    # --- la colonne d'argent `revenus` (groupe au bas-centre) : billets, blocs, socle, mots, partie cyan ---
    group(kit, "revenus", COL_S01, z=5, scale=0)
    kit.gauge("salaire", list(SALAIRE_LOCAL), value=1, w=COL_W, h=SALAIRE_H, dir="up", segPx=80, fill=LIGHT, sw=4,
              shadow=6, z=5, parent="revenus")
    kit.shape("allocations", list(ALLOC_LOCAL), kind="round", w=COL_W, h=ALLOC_H, r=10, fill=LIGHT, stroke=INK, sw=4,
              shadow=6, z=5.05, parent="revenus", scale=0)
    kit.text("allocations_mot", [0, 0], T_ALLOC, size=34, weight=700, z=5.25, parent="allocations")
    kit.shape("autres", list(AUTRES_LOCAL), kind="round", w=COL_W, h=AUTRES_H, r=10, fill=LIGHT, stroke=INK, sw=4,
              shadow=6, z=5.06, parent="revenus", scale=0)
    kit.text("autres_mot", [0, 0], T_AUTRES, size=34, weight=700, z=5.26, parent="autres")
    kit.shape("socle", list(SOCLE_LOCAL), kind="round", w=SOCLE_W, h=SOCLE_H, r=11, fill=INK, stroke=INK, sw=0,
              shadow=6, z=5.1, parent="revenus")
    S.set("socle", sx=0)                        # S07 « base » : STRETCH sx 0 -> 1
    kit.text("mot_salaire", list(MOT_SALAIRE_LOCAL), T_SALAIRE, size=36, weight=700, z=5.3, parent="revenus",
             scale=0)
    kit.text("net", list(NET_LOCAL), T_NET, size=36, weight=800, color=DEEP, anchor="start", z=5.3,
             parent="revenus", typed=True)
    S.set("net", under=0)
    kit.text("chaque_mois", list(CHAQUE_MOIS_LOCAL), T_CHAQUE_MOIS, size=34, weight=700, color=DEEP, z=5.3,
             parent="revenus", typed=True, scale=0)
    kit.text("mot_revenus", list(MOT_PIED_LOCAL), T_REVENUS, size=36, weight=700, z=5.3, parent="revenus", scale=0)
    kit.shape("reste", reste_pos(**RESTE_S05), kind="rect", w=COL_W, h=RESTE_S05["h"], fill=CYAN, stroke=INK, sw=4,
              shadow=0, z=6, parent="revenus", scale=0)
    S.set("reste", w=COL_W, h=RESTE_S05["h"], fill=CYAN)

    # --- la pastille du reste à vivre (objet du fil) et sa légende ---
    S.add("pastille", "pill", z=12, text=T_SALAIRE, w=PASTILLE_W, h=PASTILLE_H, size=44, weight=800, fill=CYAN,
          shadow=6)
    S.set("pastille", pos=list(PASTILLE_S00), scale=1, opacity=1, rot=0, text=T_SALAIRE, fill=CYAN, w=PASTILLE_W,
          textOp=1)
    kit.text("legende_reste", list(LEGENDE_S03), T_RESTE, size=36, weight=700, color=DEEP, z=12, typed=True)
    S.set("legende_reste", color=DEEP)
    kit.text("pastille_28", list(PASTILLE_S19), T_28, size=44, weight=800, z=12.2, scale=0)   # S20 : tombe

    # --- la pile des charges `charges` (groupe au bas-centre) : 4 blocs, coches de « Toi », mot du pied ---
    group(kit, "charges", PILE_S04, z=7)
    for bid, label, icon, h, r, size in BLOCS:
        charge_block(kit, bid, BLOC_LOCAL[bid], label, icon, h, r, size, z=7, parent="charges", scale=0)
    for k, cid in enumerate(COCHES):
        kit.tick(cid, list(COCHES_LOCAL[k]), DEEP, size=40, sw=8, z=7.4, parent="charges")
    kit.text("mot_charges", list(MOT_PIED_LOCAL), T_CHARGES, size=36, weight=700, z=7.2, parent="charges", scale=0)
    charge_block(kit, "mensualite", MENSUALITE_C, "Mensualité", "bank", MENSUALITE_H, 26, 34, z=7.1, scale=0)

    # --- S04-S06 : « ≠ » -> « = », trait « une partie », cadenas, accolades ---
    kit.text("egal", list(EGAL_C), T_NE, size=72, weight=800, color=RED, z=9, scale=0)
    S.set("egal", color=RED, text=T_NE)
    kit.shape("ligne_partie", list(LIGNE_PARTIE_C), kind="poly", pts=LIGNE_PARTIE_PTS, closed=False, fill="none",
              stroke=INK, sw=4, dash=[14, 10], shadow=0, z=6.5, draw=0)
    kit.icon("cadenas", list(CADENAS_C), "lock", disc=CADENAS_R, fill=PAPER, shadow=4, z=8, scale=0)
    kit.shape("accolade_g", list(ACC_G_C), kind="poly", pts=brace_pts(ACC_G_HALF), closed=False, fill="none",
              stroke=DEEP, sw=5, shadow=0, z=8, draw=0)
    kit.shape("accolade_d", list(ACC_D_C), kind="poly", pts=brace_pts(ACC_D_HALF, right=True), closed=False,
              fill="none", stroke=DEEP, sw=5, shadow=0, z=8, draw=0)
    kit.text("acc_revenus", list(ACC_REVENUS_C), T_ACC_REVENUS, size=34, weight=700, color=DEEP, z=8, scale=0)
    kit.text("acc_charges", list(ACC_CHARGES_C), T_ACC_CHARGES, size=34, weight=700, z=8, scale=0)

    # --- S07-S10 : « bon mois » -> « Prime » (tirets, contour en hex), « + », calendriers ---
    kit.shape("bon_mois", list(BON_MOIS_SOMMET), kind="round", w=BON_MOIS_W, h=BON_MOIS_H, r=12, fill=LIGHT,
              stroke=INK, sw=4, dash=[14, 10], shadow=0, z=8.5, scale=0)
    S.set("bon_mois", stroke=INK)
    kit.text("bon_mois_mot", [0, 0], T_BON_MOIS, size=34, weight=700, z=8.6, parent="bon_mois")
    S.set("bon_mois_mot", text=T_BON_MOIS)
    kit.text("plus", list(PLUS_C), T_PLUS, size=72, weight=800, color=DEEP, z=9, scale=0)
    for k, cid in enumerate(CALENDRIERS):
        kit.icon(cid, list(CAL_C[k]), "cal", disc=CAL_R, fill=PAPER, shadow=4, z=8.5, scale=0)
        S.set(cid, fill=PAPER)

    # --- S02, S10 : le panier de courses au bout du stylo ; S10 : les trois pièces ---
    kit.icon("panier", list(PANIER_S02_TIP), "cart", disc=PANIER_R, fill=PAPER, shadow=4, z=16.5, scale=0)
    for pid in PIECES:
        kit.icon(pid, list(PIECES_DEPART), "euro", disc=PIECE_R, fill=LIGHT, shadow=3, z=11, scale=0)

    # --- S12-S14 : les 3 relevés (carte papier + « Relevé » + « mois k »), barres, pièges, « 3 », moyenne ---
    for k, rid in enumerate(RELEVES):
        kit.shape(rid, list(RELEVE_C[k]), kind="round", w=RELEVE_W, h=RELEVE_H, r=14, fill=PAPER, stroke=INK, sw=4,
                  shadow=6, z=9, scale=0)
        kit.text(f"{rid}_titre", list(RELEVE_TITRE_LOCAL), T_RELEVE, size=28, weight=600, z=9.1, parent=rid)
        kit.text(f"{rid}_mois", list(RELEVE_MOIS_LOCAL), T_MOIS[k], size=28, weight=700, color=DEEP, z=9.1,
                 parent=rid)
        bid = BARRES[k]
        kit.shape(bid, [0, BARRE_BAS], kind="rect", w=BARRE_W, h=0, fill=PAPER, stroke=INK, sw=4, shadow=0, z=9.2,
                  parent=rid)
        S.set(bid, w=BARRE_W, h=0)              # barre posée sur y local 100 : pos = [0, 100 - h/2] avec h
        kit.text(PIEGES_LBL[k], [RELEVE_C[k][0], PIEGE_LBL_Y], T_PIEGES[k], size=32, weight=700, color=RED, z=9,
                 scale=0)
    kit.shape("rouge1", [0, BARRE_BAS - BARRES_H[0] + ROUGE1_H / 2], kind="rect", w=BARRE_W, h=ROUGE1_H, fill=PAPER,
              stroke=INK, sw=4, shadow=0, z=9.3, parent="releve1", scale=0)
    S.set("rouge1", fill=PAPER)                 # S13 « facture » : fill PAPER -> RED (hex, fondu 300 ms)
    kit.shape("prime_mini", list(PRIME_MINI_LOCAL), kind="round", w=PRIME_MINI_W, h=PRIME_MINI_H, r=8, fill=LIGHT,
              stroke=INK, sw=3, dash=[10, 7], shadow=0, z=9.3, parent="releve2", scale=0)
    kit.text("prime_mini_mot", [0, 0], T_PRIME, size=26, weight=700, z=9.35, parent="prime_mini")
    kit.shape("prime_mini_barre", [0, 0], kind="poly", pts=[[-56, 14], [56, -14]], closed=False, fill="none",
              stroke=RED, sw=5, shadow=0, z=9.4, parent="prime_mini", draw=0)
    kit.shape("vide3", list(VIDE3_LOCAL), kind="rect", w=VIDE3_W, h=VIDE3_H, fill="none", stroke=RED, sw=4,
              dash=[8, 6], shadow=0, z=9.3, parent="releve3", scale=0)
    S.set("vide3", fill="none")                 # S14 : se remplit de papier (bascule fill, ou relais par barre3)
    kit.text("trois", list(TROIS_C), T_TROIS, size=140, weight=800, color=DEEP, z=9.5, scale=0)
    kit.shape("moyenne_ligne", list(MOYENNE_LIGNE_C), kind="poly", pts=MOYENNE_LIGNE_PTS, closed=False, fill="none",
              stroke=DEEP, sw=6, shadow=0, z=9.6, draw=0)
    kit.text("moyenne_titre", list(MOYENNE_TITRE_C), T_MOYENNE, size=36, weight=700, color=DEEP, z=9.6, scale=0)

    # --- S15-S17 : trait de niveau, « − », compteurs, trait de total, fil cyan -> pastille ---
    kit.shape("ligne_niveau", list(NIVEAU_C), kind="poly", pts=NIVEAU_PTS, closed=False, fill="none", stroke=INK,
              sw=4, dash=[14, 10], shadow=0, z=8, draw=0)
    kit.text("moins", list(MOINS_PIED), T_MOINS, size=72, weight=800, z=9, scale=0)
    kit.counter("compteur_2200", list(COMPTEUR_2200_C), value=0, size=64, weight=800, anchor="end", suffix=" €",
                z=10, scale=0)
    kit.counter("compteur_1350", list(COMPTEUR_1350_C), value=0, size=64, weight=800, anchor="end", suffix=" €",
                z=10, scale=0)
    kit.shape("total", list(TOTAL_C), kind="rect", w=TOTAL_W, h=TOTAL_H, fill=INK, stroke=INK, sw=0, shadow=0, z=10)
    S.set("total", sx=0)                        # S16 « fixes. » : STRETCH sx 0 -> 1
    S.add("fil_pastille", "wire", z=11.8, a={"id": "reste", "at": list(FIL_RESTE_A)},
          b={"id": "pastille", "at": list(FIL_PASTILLE_B)}, color=DEEP, sw=5)
    S.set("fil_pastille", draw=0, sag=0)
    S.set("fil_pastille", **{"from": 0})

    # --- S18 : la page de calendrier et ses 30 jours ; les 4 usages ---
    kit.shape("page", list(PAGE_C), kind="round", w=PAGE_W, h=PAGE_H, r=16, fill=PAPER, stroke=INK, sw=4, shadow=6,
              z=9, scale=0)
    kit.shape("page_bandeau", list(BANDEAU_LOCAL), kind="round", w=PAGE_W, h=BANDEAU_H, r=12, fill=INK, stroke=INK,
              sw=0, shadow=0, z=9.1, parent="page")
    for k, pt in enumerate(ANNEAUX_LOCAL):
        kit.shape(f"page_anneau{k + 1}", list(pt), kind="round", w=16, h=36, r=8, fill=PAPER, stroke=INK, sw=4,
                  shadow=0, z=9.2, parent="page")
    for k, jid in enumerate(JOURS):
        kit.shape(jid, list(JOURS_C[k]), kind="round", w=JOUR_S, h=JOUR_S, r=10, fill=CYAN, stroke=INK, sw=3,
                  shadow=3, z=9.5, scale=0)
    for uid, name, w, pos in USAGE_PNG:
        meta = S.png(name)
        S.add(uid, "png", z=10, src=meta["src"], w=w, h=round(w * meta["h"] / meta["w"]),
              contact=dict(w=round(w * 0.72), h=20, dy=4, blur=10, alpha=0.18))
        S.set(uid, pos=list(pos), scale=0, opacity=1)
    for k, eid in enumerate(EPARGNE):
        kit.icon(eid, list(EPARGNE_C[k]), "coin", disc=26, fill=LIGHT, shadow=3, z=10 + 0.01 * k, scale=0)
    for k, mid in enumerate(USAGE_MOTS):
        kit.text(mid, list(USAGE_MOT_C[k]), T_USAGES[k], size=34, weight=700, z=10, scale=0)

    # --- S19-S21 : la bulle « Un crédit ? », la banque, son regard, « taux d’endettement », le « ? » de « Toi » ---
    kit.shape("bulle_credit", list(BULLE_C), kind="round", w=BULLE_W, h=BULLE_H, r=18, fill=PAPER, stroke=INK, sw=4,
              shadow=6, z=14, scale=0)
    kit.shape("bulle_queue", [0, 0], kind="poly", pts=BULLE_QUEUE, closed=True, fill=PAPER, stroke=INK, sw=4,
              shadow=0, z=13.9, parent="bulle_credit")
    kit.text("bulle_mot", [0, 0], T_CREDIT_Q, size=34, weight=700, z=14.1, parent="bulle_credit")
    S.add("regard", "wire", z=13, color=INK, sw=3)
    S.set("regard", pa=list(BANQUE_TETE), pb=list(CREDITS_REGARD), draw=0, sag=0)
    S.set("regard", **{"from": 0})
    kit.text("legende_taux", list(TAUX_C), T_TAUX, size=34, weight=700, z=12, scale=0)
    S.add("question", "qmark", z=17)
    S.set("question", pos=list(QUESTION_C), scale=0, opacity=1, gs=QUESTION_GS)

    # --- le repère 1-2-3 légendé (aucun gris : doneStyle « kept », légende en fondu par la piste lbl) ---
    kit.steps_marker(MARKER_LABELS, y=MARKER_Y, cx=MARKER_CX, gap=MARKER_GAP, z=20)
    S.ents["marqueur"]["p"].update(moveBlank=True, labelSize=MARKER_LABEL_SIZE, doneStyle="kept")
    S.set("marqueur", scale=0, on=0, done0=0, done1=0, done2=0, lbl=0)

    # --- S22 : ondes du toucher du stylo sur le bouton (pas de pointeur de souris) ---
    for k in range(2):
        kit.shape(f"fin_onde{k + 1}", list(FIN_TAP), kind="circle", w=70, fill="none", stroke=DEEP, sw=6, shadow=0,
                  z=43.5, opacity=0)

    # --- « Toi » (bras gauche), bras baissé dès l'image 0, et son nom (enfant : il le suit) ---
    toi = Figure(kit, "toi", pos=list(P1), scale=TOI_SCALE, side="left", z=15)
    S.set("toi", look=0)
    G, rot = low_pose(toi, 0)
    S.set(toi.pen, pos=[round(G[0], 3), round(G[1], 3)], rot=round(rot, 3))
    S.set(toi.arm, elbow=[round(v, 3) for v in solve_ik(toi._shoulder(0), G, toi.l1, toi.l2, toi.bend)[0]])
    pill(S, "nom_toi", NOM_TOI_LOCAL, T_TOI, size=34, fill=LIGHT, h=NOM_TOI_H, w=NOM_TOI_W, z=15.2, parent="toi",
         scale=1, shadow=3)

    # --- la banque (figurine papier sans outil, S19-S21) et sa pilule « Banque » ---
    banque = Figure(kit, "banque", pos=list(BANQUE_POS), scale=1.0, variant="paper", side="right", tool=False, z=14,
                    show=False)
    S.set("banque", look=0)
    pill(S, "banque_nom", BANQUE_NOM_LOCAL, T_BANQUE, size=34, fill=LIGHT, h=64, z=14.2, parent="banque", scale=1,
         shadow=3, icon="bank")

    return SimpleNamespace(toi=toi, banque=banque, blocs=BLOC_IDS, coches=COCHES, calendriers=CALENDRIERS,
                           pieces=PIECES, releves=RELEVES, barres=BARRES, pieges_lbl=PIEGES_LBL, jours=JOURS,
                           epargne=EPARGNE, usage_mots=USAGE_MOTS, usages_png=[u[0] for u in USAGE_PNG])


def build(S):
    kit = Kit(S)
    c = cast(S, kit)
    only = [p for p in os.environ.get("WTH_PARTS", "").split(",") if p]   # WTH_PARTS=p2 : cette partie seule
    for name in PARTS:
        if not only or name in only:
            importlib.import_module(f".{name}", __name__).part(S, kit, c)
