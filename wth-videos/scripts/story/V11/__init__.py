"""V11 « La meilleure info n’est pas dans le dossier » : mise en scène Story, en paquet (une partie par fichier).

Storyboard : scripts/storyboards/V11.json (v1, révisé après le test sans son, 22 scènes, 93 temps forts, 93,015 s),
version lisible scripts/storyboards/V11.md. Voix : build/V11/words.json (film : images 0-2790, FILM_END = 2791).
Fil : la pastille cyan « mars 2023 » (`pastille`, pill 250 x 62, pictogramme cal, Bold 34) : sur l'en-tête de la fiche
dès l'image 0 (échelle 0,76), légende de la photo (S05), engendre la pilule de la vie (S06), cerclée de rouge (S07-S20),
mise à jour « nov. 2026 » par le stylo de « Toi » (S21), bouton « S’abonner » de la carte de fin (S22).
Parti pris « la photo et la vie » : à droite la fiche du client (une photo épinglée, datée), à gauche sa vie (une
colonne x 40-440 au-dessus de lui : événements, cas, barres, patrimoine, sujets à revoir) ; la question de « Toi »
est le seul pont.

Tour de revue 1 (corrections) :
- la colonne de la vie est la SCÈNE de chaque processus (pile des sujets à revoir, barres du travail, patrimoine) ;
  le couloir entre les deux personnages ne garde que le conseil ;
- le conseil est posé en CONSEIL_C (470, 1200), à 100 px de la pointe du stylo de « Toi » au repos : il n'est touché
  que par des gestes voulus (S07 naissance, S14 tapotement, S20 « Toi » vient à lui) ;
- rouge : seulement la rangée de la scène en cours, la pastille et le conseil ; une rangée déjà touchée passe à
  l'état « à revoir » (encre sur aplat cyan pâle) ; les pilules de la pile sont encre sur papier, puis cyan pâle ;
- badges des événements : disques cyan au pictogramme de LEUR rangée (personne, plus, immeuble, euro, maison), en
  rangée juste au-dessus de la tête du client (y 905, là où était la pilule de la vie, masquée de S09 à S21) ;
- repère : seule la légende de l'étape active (labelShow « active ») ; aucune légende grise.

Parties (scènes contiguës, coupées sur un changement de composition) :
- p1 : S01-S08, images 0-822 (27 temps forts, 27,4 s). Accroche, contexte (photo datée, vie, conseil rouge), étape 1.
- p2 : S09-S14, images 823-1771 (32 temps forts, 31,6 s). Famille (alliances, berceau, pile) et travail (barres).
- p3 : S15-S22, images 1772-2790 (34 temps forts, 33,9 s). Patrimoine, déménagement, question, mise à jour, fin.
ENTRY_P2 et ENTRY_P3 sont le contrat des raccords (kit.pin(f0 - 1, …)). Les figurines n'y sont jamais.

Aucune entité nouvelle : tout se compose avec le catalogue.
- Contour qui rougit (pastille, conseil) : la pill n'a pas de piste `stroke` ; un liseré rouge enfant (`*_rouge`,
  shape round fill none, même taille) passe en fondu (opacity 0 -> 1, puis 1 -> 0 en S21).
- Pilules « à revoir » : capsules = shape round (pistes `stroke` et `fill` en hex) + texte enfant : `capsule()`.
- Surligneur des rangées : un aplat light (`fiche_hlN`, sous la rangée) paraît pendant que la capsule beige de la
  rangée s'efface (slotFill 1 -> 0), et l'inverse.
- Nouvelle valeur de rangée (S21) : texte deep enfant de la fiche (`fiche_vN`, ancré à droite, tapé) ; l'ancienne valeur
  tombe (piste `fall` de la line).
- Pilule « Info » : capsule cyan + étoile en polygone + anneau deep (shape, draw).
"""
import importlib
import math
import os
from types import SimpleNamespace

from pipeline.story import GEOM, STYLE, text_width
from pipeline.story_kit import Figure, Kit, Sheet

PARTS = ["p1", "p2", "p3"]                      # S01-S08, S09-S14, S15-S22
NBSP = " "                                 # espace insécable (avant « : », « ? », dans les guillemets)
ALERT_WORDS = {"dépassée", "inadapté"}          # karaoké en rouge : ce que la vie a rendu faux (S07)
ACOUSTIC_SNAP = {"gap": 0.2, "window": 0.08}    # temps fort après un silence : calé sur l'attaque audible
# découpes imposées : sans elles, « dossier | client », « situation | dépassée », « clause | bénéficiaire »,
# « objectif | d’épargne » et « a | changé » étaient coupés ; « Nouvel », « c’est », « elle », « il y a » restaient
# seuls 5 à 11 images (revue 1)
CAPTION_GROUPS = [
    ["Le problème c’est", "la fiche figée"],
    ["Un dossier client", "est une photo", "prise à une date"],
    ["La vie", "elle continue"],
    ["Et un conseil", "fondé sur", "une situation dépassée", "peut devenir inadapté"],
    ["Nouvel objectif", "d’épargne", "protection du foyer", "prévoyance", "et clause bénéficiaire", "à mettre à jour"],
    ["il y a aussi", "le travail"],
    ["Enfin il y a", "les décisions"],
    ["Qu’est-ce qui", "a changé depuis", "notre dernier échange"],
]

FILM_END = 2791                                 # images 0-2790 (93,015 s)

# ---------- couleurs ----------
INK, CYAN, DEEP, LIGHT = STYLE["ink"], STYLE["cyan"], STYLE["deep"], STYLE["light"]
PAPER, RED, GREY, BG = STYLE["paper"], STYLE["red"], STYLE["grey"], STYLE["bg"]
GHOST = STYLE.get("ai_tick", "#8E8887")         # trait d'avant (S14) : tireté gris

# ---------- textes à l'écran (typographie française : insécable avant « : » et « ? », apostrophe ’) ----------
T_FICHE = "Fiche client"
T_MARS, T_MARS24, T_MARS25, T_NOV = "mars 2023", "mars 2024", "mars 2025", "nov. 2026"
T_ABONNER = "S’abonner"
T_TOI, T_CLIENT, T_INFO, T_CONSEIL = "Toi", "Client", "Info", "Ton conseil"
LINES = [(f"Famille{NBSP}:", "célibataire", "person"),
         (f"Enfants{NBSP}:", "aucun", "plus"),
         (f"Travail{NBSP}:", "salarié", "building"),
         (f"Patrimoine{NBSP}:", "épargne", "euro"),
         (f"Résidence{NBSP}:", "France", "house")]
NEW_VALUES = ["marié", "1", "dirigeant", "maison", "Portugal"]   # S21, deep Bold 32
MARKER_LABELS = ["Famille", "Travail", "Patrimoine"]
T_OU, T_SEPARATION = "ou", "Séparation"
PILE = [  # (id, texte) : S10 (mariage), S11 (naissance), S19 (étranger)
    ("pile_regime", "Régime matrimonial"), ("pile_clause", "Clause bénéficiaire"), ("pile_donation", "Donation"),
    ("pile_transmission", "Transmission"),
    ("pile_objectif", "Objectif d’épargne"), ("pile_protection", "Protection du foyer"),
    ("pile_prevoyance", "Prévoyance"),
    ("pile_fiscalite", "Fiscalité"), ("pile_residence", "Résidence"), ("pile_produits", "Produits accessibles"),
]
TRAVAIL = [  # S13 : (id, texte, pictogramme, rotation du pictogramme) ; un cas à la fois, grand, dans la vie
    ("travail1", "Entreprise", "building", 0), ("travail2", "Emploi perdu", "minus", 0),
    ("travail3", "Promotion", "arrow", -90), ("travail4", "Retraite", "hourglass", 0),
]
JAUGES = [  # S14 : (id, légende, niveau d'avant, nouveau niveau, y, sens) ; sens -1 : flèche ↓ rouge, +1 : ↑ deep
    ("jauge_revenus", "Revenus", 0.6, 0.25, 585, -1), ("jauge_fiscalite", "Fiscalité", 0.4, 0.75, 705, 1),
    ("jauge_liquidites", "Besoin de liquidités", 0.3, 0.85, 825, 1),
]
T_PATRIMOINE, T_EPARGNE, T_MAISON, T_CREDIT = "Patrimoine", "Épargne", "Maison", "− Crédit"
T_QUESTION = f"«{NBSP}Qu’est-ce qui\na changé depuis\nnotre dernier\néchange{NBSP}?{NBSP}»"
T_DOTS = "…"

# ---------- mise en page (1080 x 1920) ----------
X_MIN, X_MAX, Y_MIN, Y_MAX = 40, 940, 160, 1270
GROUND = 1230                                   # pieds de « Toi », du client et du conjoint
FIG_BASE = GEOM["FIGURE"]["base"]               # 95
HEAD_DY = GEOM["FIGURE"]["head"]["cy"]          # -64 : centre de la tête
HEAD_R = GEOM["FIGURE"]["head"]["r"]            # 32
SHOULDER_DX, SHOULDER_DY = abs(GEOM["FIGURE"]["shoulder"][0]), GEOM["FIGURE"]["shoulder"][1]   # 30, -16
REACH_OK = 267                                  # allonge confortable (REACH x 284) à l'échelle 1


def fig_pos(x, feet=GROUND, s=1.0):
    return [x, round(feet - FIG_BASE * s, 2)]


# --- les deux colonnes : à droite la fiche (le dossier), à gauche la vie du client ---
TOI_HOME = fig_pos(820)                         # (820, 1135) S01-S19 ; épaule (790, 1119)
TOI_RDV = fig_pos(660)                          # (660, 1135) S20-S22 : « Toi » vient au client (160 px), jusqu'au
                                                # conseil ; d'ici la pastille (S21) et le bouton (S22) sont à portée
CLIENT_C = fig_pos(220)                         # (220, 1135), tourné vers « Toi » (side « right »)
CLIENT_FROM_X = -62                             # S01 « client » : hors champ à f - 1, franchit le bord sur le mot
CONJOINT_K = 0.95
CONJOINT_IN = fig_pos(100, s=CONJOINT_K)        # (100, 1140) S09 « marie » : à GAUCHE du client, face à lui
CONJOINT_OUT_X = -110                           # S09 « sépare » : sort du champ par la gauche
NOM_LOCAL, NOM_H = (0, -135), 54                # pilules « Toi » / « Client » au-dessus de la tête (monde y 1000)
NOM_TOI_W, NOM_CLIENT_W = 96, 150

# --- la fiche (Sheet 5 rangées, 450 x 470, centre (690, 565) : x 465-915, y 330-800) ---
FICHE_C = (690, 565)
SHEET = Sheet(n=5, w=450, h=470, head=70, pitch=80, top=45, ty=0, slot_h=60, strip=60)
SHEET.x["value"] = SHEET.w / 2 - 26             # 199 : pas de colonne de coches dans V11, valeurs à droite
SHEET.x["slot1"] = SHEET.w / 2 - 12             # capsule jusqu'au bord droit
ROWS_Y = [round(FICHE_C[1] + y) for y in SHEET.rows]          # monde : 445, 525, 605, 685, 765
BULLET_X = FICHE_C[0] + SHEET.x["bullet"]                     # 467 : puce (r 22) sur le bord gauche de la fiche
VALUE_X = FICHE_C[0] + SHEET.x["value"]                       # 889 : bord droit des valeurs
QLIGNE_LOCAL_X = -262                           # S08 : « ? » devant chaque rangée (monde x 428), à gauche de la puce

# --- le cadre-photo, sa punaise, la pastille ---
CADRE_C, CADRE_W, CADRE_H = (690, 595), 480, 560              # x 450-930, y 315-875 (marge basse 75 px)
PUNAISE_C, PUNAISE_R = (690, 330), 24
CADRE_FIL_LOCAL = (-110, CADRE_H / 2)           # bas du cadre (580, 875) : là où s'accroche le fil du conseil
PASTILLE_W, PASTILLE_H = 250, 62
PASTILLE_HEAD, PASTILLE_HEAD_K = (566, 365), 0.76  # S01-S05 : en-tête (x 471-661 ; « Fiche client » de 684 à 889)
PASTILLE_PHOTO = (690, 838)                     # S05-S21 : marge basse du cadre (x 565-815)
PASTILLE_LOW = (650, 880)                       # S21 « dernier » : descend vers « Toi » (x 525-775)
PASTILLE_TAP = (532, 892)                       # S21 « C’est » : contact (bout gauche de la pastille)

# --- la vie du client (colonne x 40-440) ---
INFO_C0, INFO_W, INFO_H = (330, 640), 150, 62   # S01 « meilleure »
INFO_BUMP = (390, 640)                          # S01 « dans » : bord droit contre la fiche (465)
INFO_BACK = (285, 668)                          # S01 « dossier. » : repoussée loin, penchée
INFO_BACK_ROT = -8
INFO_CLIENT = (220, 870)                        # S01 « Elle » : au-dessus du client
INFO_BACK_ARC = 70                              # S01 « dossier. » : rebond en arc ample (contrôle muet)
REFUS_S01, REFUS_S04 = (440, 640), (425, 560)   # grand « × » rouge au point de contact : la fiche refuse
REFUS_A = 36                                    # demi-diagonale du « × » (72 px)
VIE_C = (220, 915)                              # la pilule de la vie (date du client)
DISQUE_R = 36
DISQUES_S02 = [(95, 560), (220, 560), (345, 560)]   # personne, immeuble, euro
DISQUES_S03 = [(405, 445), (405, 605), (405, 685)]  # au bord gauche de la fiche, à côté de L1, L3, L4
DISQUES_S04 = [(95, 430), (220, 430), (345, 430)]   # repoussés au-dessus du client
DISQUES_ROWS = [0, 2, 3]                        # rangées reliées (L1, L3, L4)
FIL_VIE_STOP = SHEET.x["bullet"] - 62           # S02 : les fils s'arrêtent 40 px avant la puce (monde x 405)
EVT_C = (225, 650)                              # centre de la colonne de la vie : les événements tombent ici
BADGES = [(70, 905), (145, 905), (220, 905), (295, 905), (370, 905)]   # au-dessus de la tête du client
BADGE_R = 30
BADGE_ICONS = ["person", "plus", "building", "euro", "house"]          # le pictogramme de LEUR rangée

# --- le repère 1-2-3 (en haut) ---
MARKER_Y, MARKER_CX, MARKER_GAP = 200, 540, 200   # disques x 340, 540, 740 ; légende Bold 32 à y 262
MARKER_XS = [MARKER_CX - MARKER_GAP, MARKER_CX, MARKER_CX + MARKER_GAP]

# --- le conseil (au sol entre les deux personnages) ---
CONSEIL_C, CONSEIL_W, CONSEIL_H = (470, 1200), 270, 64        # x 335-605 ; stylo de « Toi » au repos (704, 1277)
CONSEIL_TILT = 8                                # penché (S07-S21)
CONSEIL_TOP_LOCAL = (0, -CONSEIL_H / 2)
CONSEIL_SPAWN = (650, 1185)                     # S07 « conseil » : pointe du stylo, à gauche du buste (x 761)
CONSEIL_BORN = (600, 1196)                      # S07 : la pilule grandit à gauche de « Toi », puis glisse en place
CONSEIL_FIL_XS = [60, 0, -60]                   # S14 : arrivée des trois fils (barre du haut -> bout droit)
CONSEIL_RDV = (430, 1200)                       # S20 : porté par la pointe du stylo pendant que « Toi » s'avance


def conseil_world(local, c=CONSEIL_C, tilt=CONSEIL_TILT):
    a = math.radians(tilt)
    return (round(c[0] + local[0] * math.cos(a) - local[1] * math.sin(a), 1),
            round(c[1] + local[0] * math.sin(a) + local[1] * math.cos(a), 1))


CONSEIL_TAP = conseil_world((CONSEIL_W / 2 - 14, -CONSEIL_H / 2))   # S14 « conseil » : bord haut, bout droit

# --- la pile des sujets à revoir (S10, S11, S19) : dans la colonne de la vie, de bas en haut, pas de 80 ---
PILE_X, PILE_H = 240, 54
PILE_YS = [760, 680, 600, 520]                  # du bas vers le haut ; 26 px entre deux pilules
MINI_R, MINI_DY = 30, -62                       # S11 : pictogrammes famille / enfants posés sur les bouts de la clause
FOIS2_DY = -64                                  # S11 « clause » : « ×2 » deep entre les deux pictogrammes

# --- S09 (famille) ---
RINGS_C, RINGS_W = (225, 640), 240              # 240 x 137 : y 572-708
RING_R = 34
RINGS_SPLIT = [(203, 640), (247, 640)], [(145, 640), (305, 640)]
# S09 « sépare » (contrôle muet : « sans le mot, ces deux cercles ne veulent rien dire ») : un cœur cyan dessiné en
# code, en deux moitiés à bord en zigzag, qui se brise : les moitiés s'écartent et penchent
COEUR_C, COEUR_K = (225, 640), 4.6
COEUR_SPLIT = (-58, 58)                         # écart final des deux moitiés (x local), rotation ±14°
OU_FAMILLE_C, SEPARATION_C = (225, 778), (225, 852)
CRADLE_C, CRADLE_W = (225, 660), 180            # 180 x 164 : y 578-742 (sous la clause, en haut de pile)

# --- S13 : un cas de travail à la fois, grand, dans la vie ---
CASE_C, CASE_R = (225, 625), 76                 # disque 152 px (la taille des alliances)
CASE_LBL_DY = 118                               # étiquette sous le disque (monde y 743)
OU_TRAVAIL_C = (225, 487)

# --- S14 : les barres du travail, dans la colonne de la vie (x 80-380) ---
JAUGE_CX, JAUGE_W, JAUGE_H = 230, 300, 40
JAUGE_LEG_X, JAUGE_LEG_DY = 60, -46             # légende au-dessus de la barre, ancrée à gauche
JAUGE_LEG_SIZE = 32                             # contrôle muet : « Besoin de liquidités » (et non « Liquidités ») tient
                                                # dans la colonne avec sa flèche (x 60-422)
FIL_JAUGE_SW = 8                                # contrôle muet : fils « trop fins » -> 8 px
CONSEIL_PULL = (440, 1150)                      # S14 « suivre. » : le conseil tiré vers les barres y RESTE (rouge,
                                                # penché) jusqu'à S15 « décisions », où les fils le lâchent

# --- S15-S17 : le patrimoine, dans la colonne de la vie ---
PATRIMOINE_TITRE_C = (240, 498)
BLOC_C, BLOC_W, BLOC_H = (240, 570), 390, 70    # x 45-435
EPARGNE_RECOMP, MAISON_RECOMP = (140, 190), (337.5, 195)   # S17 « recompose » : (centre x, largeur)
EPARGNE_FIN, MAISON_FIN = (155, 220), (352.5, 165)          # S17 « apparaître »
CREDIT_C, CREDIT_W, CREDIT_H = (337.5, 648), 195, 40        # S17 : sous « Maison », dette en rouge
PIECE_R = 40
TOKEN_C, TOKEN_W = (225, 762), 190              # 190 x 207 : y 658-866
VENTE_FLECHE, VENTE_PIECE = (332, 812), (382, 852)   # S16 « vend » : maison -> € (vendre refait de l'argent),
VENTE_ROT = 38                                         # en bas à droite de la maison, loin des puces de la fiche

# --- les illustrations (une seule à la fois dans la vie du client) ---
TRUCK_C, TRUCK_FROM, TRUCK_W = (225, 700), (-160, 700), 280
GLOBE_C, GLOBE_W = (225, 700), 190              # 190 x 231 : y 585-815

# --- la question de « Toi » (S03 : petite bulle ; S20-S21 : grande bulle) ; la réponse du client (S21) ---
Q_GS_S03, Q_GS_S20, Q_GS_COIN = 64, 64, 40
BULLE1_C, BULLE1_W, BULLE1_H = (520, 960), 150, 110   # S03 : à mi-chemin, queue sur la pointe du stylo
Q_S03 = (705, 1000)                             # S03 : la pointe du stylo levé
BULLE2_C, BULLE2_W, BULLE2_H = (240, 730), 360, 220   # x 60-420, y 620-840
BULLE2_TIP = (626, 1046)                        # S20 : queue vers la tête de « Toi » en TOI_RDV (660, 1071)
BULLE2_K0 = 0.65
Q_COIN = (90, 650)                              # S20 « ouverte. » : le « ? » dans le coin haut gauche
QUESTION_TXT = (112, 735)                       # S21 : 4 lignes, ancre start, bloc centré dans la bulle
BULLE3_C, BULLE3_W, BULLE3_H = (372, 1012), 124, 78   # S21 : la réponse du client (x 310-434, y 973-1051)
BULLE3_TIP = (258, 1050)                        # queue vers la tête du client (220, 1071)
Q_PEN = (580, 1005)                             # S20 « pose » : la pointe se lève devant « Toi »
FIN_BTN_TAP = (560, 960)                        # S22 « comprendre » : bas du bouton, sous le libellé


def scene_f0(S, sid):
    return round(next(s for s in S.sb["scenes"] if s["id"] == sid)["t_start"] * S.fps)


def bulle2_pos(k):
    """Centre de la grande bulle à l'échelle k, sa queue restant sur BULLE2_TIP (pos et scale avec la même clé)."""
    lx, ly = BULLE2_TIP[0] - BULLE2_C[0], BULLE2_TIP[1] - BULLE2_C[1]
    return [round(BULLE2_TIP[0] - k * lx, 2), round(BULLE2_TIP[1] - k * ly, 2)]


# ---------- l'allonge de « Toi » (bras gauche) ----------
def arm_check(fig_x, pt, fig_y=TOI_HOME[1]):
    """(distance épaule -> cible, côté sûr, dégagement de la tête) pour « Toi » (side left) en (fig_x, fig_y)."""
    sx, sy = fig_x - SHOULDER_DX, fig_y + SHOULDER_DY
    dx, dy = pt[0] - sx, sy - pt[1]
    d = math.hypot(dx, dy)
    safe = -dx >= 0.3 * max(dy, 0)
    hx, hy = fig_x, fig_y + HEAD_DY
    ux, uy = (pt[0] - sx) / max(d, 1e-6), (pt[1] - sy) / max(d, 1e-6)
    clear = min(math.hypot(sx + ux * t - hx, sy + uy * t - hy) for t in range(0, int(min(d, 120)) + 1))
    return round(d, 1), safe, round(clear, 1)


def assert_reach(fig_x, pt, what, fig_y=TOI_HOME[1]):
    d, safe, clear = arm_check(fig_x, pt, fig_y)
    assert 63 <= d <= REACH_OK and safe and clear >= HEAD_R + 8, \
        f"{what} : hors d'allonge depuis x {fig_x} : {d} px, côté sûr {safe}, tête {clear} px"


for _x, _pt, _what in [(TOI_HOME[0], Q_S03, "S03 « ? » à la pointe"), (TOI_HOME[0], CONSEIL_SPAWN, "S07"),
                       (TOI_HOME[0], CONSEIL_TAP, "S14 conseil"), (TOI_RDV[0], Q_PEN, "S20 pose"),
                       (TOI_RDV[0], PASTILLE_TAP, "S21 pastille"), (TOI_RDV[0], FIN_BTN_TAP, "S22 bouton")]:
    assert_reach(_x, _pt, _what)


# ---------- petites fabriques ----------
def pill(S, id, pos, text, size=34, weight=700, fill=LIGHT, h=58, z=11.5, parent=None, scale=0, pad=48, w=None,
         shadow=6, **p):
    """Pilule de texte (type pill) ; w mesuré si absent (+ 30 px pour un pictogramme)."""
    if w is None:
        w = round(text_width(text, size, weight) + pad + (30 if p.get("icon") else 0))
    S.add(id, "pill", z=z, parent=parent, text=text, w=w, h=h, size=size, weight=weight, fill=fill, shadow=shadow, **p)
    S.set(id, pos=list(pos), scale=scale, opacity=1, fill=fill, w=w)
    return id


def outline(kit, id, parent, w, h, color=RED, sw=4, z=None):
    """Liseré (contour seul) posé exactement sur une pilule : le contour « rougit » en fondu (piste opacity)."""
    z = z if z is not None else kit.S.ents[parent]["z"] + 0.1
    return kit.shape(id, [0, 0], kind="round", w=w, h=h, r=h / 2, fill="none", stroke=color, sw=sw, shadow=0, z=z,
                     parent=parent, opacity=0)


def capsule(kit, id, pos, text, size=32, weight=700, h=54, fill=PAPER, z=13, parent=None, shadow=3, scale=0):
    """Pilule composée (pistes `stroke` et `fill` en hex : encre sur papier, puis cyan pâle « à revoir ») : shape round
    + texte enfant `id`_mot centré. Renvoie (id, largeur)."""
    w = round(text_width(text, size, weight) + 48)
    kit.shape(id, list(pos), kind="round", w=w, h=h, r=h / 2, fill=fill, stroke=INK, sw=4, shadow=shadow, z=z,
              parent=parent, scale=scale)
    kit.S.set(id, stroke=INK, fill=fill)        # hex : PAPER -> LIGHT en fondu
    kit.text(f"{id}_mot", [0, 0], text, size=size, weight=weight, z=z + 0.1, parent=id)
    return id, w


def png(S, id, name, w, pos, z=5, contact=True, parent=None, scale=0, opacity=1):
    """Illustration générique (verre, alpha strict), largeur w, rapport gardé."""
    m = S.png(name)
    h = round(w * m["h"] / m["w"])
    p = dict(contact=dict(w=round(w * 0.7), h=22, dy=4, blur=10, alpha=0.2)) if contact else {}
    S.add(id, "png", z=z, parent=parent, src=m["src"], w=w, h=h, **p)
    S.set(id, pos=list(pos), scale=scale, opacity=opacity, rot=0)
    return id


def star_pts(r_out=13, r_in=5.5):
    """Étoile à 5 branches (poly fermée), pointe en haut."""
    pts = []
    for k in range(10):
        a = math.radians(-90 + 36 * k)
        r = r_out if k % 2 == 0 else r_in
        pts.append([round(r * math.cos(a), 2), round(r * math.sin(a), 2)])
    return pts


def heart_halves(k):
    """Deux moitiés de cœur (gauche, droite) au bord commun en zigzag, centrées sur l'origine (147 x 133 à k 4,6)."""
    def h(t):
        return (16 * math.sin(t) ** 3 * k, -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t)
                                             - math.cos(4 * t)) * k - 11.7 * k / 4.6)
    top, bot = h(0)[1], h(math.pi)[1]
    zig = [[(7 if j % 2 else -7) if 0 < j < 6 else 0, round(top + (bot - top) * j / 6, 1)] for j in range(7)]
    right = [[round(x, 1), round(y, 1)] for x, y in (h(math.pi * j / 24) for j in range(25))] + zig[::-1][1:-1]
    left = [[round(x, 1), round(y, 1)] for x, y in (h(math.pi + math.pi * j / 24) for j in range(25))] + zig[1:-1]
    return left, right


def bubble_params(w, h, tip_world, center, base=(-30, 10), sw=5, shadow=6):
    shape = dict(w=w, h=h, r=26, q=56, qx=0, px=0, ps=0, sw=sw, shadow=shadow, gs=4)
    return dict(big=shape, small=dict(shape), tail=[round(tip_world[0] - center[0], 1),
                                                     round(tip_world[1] - center[1], 1)], tailBase=list(base))


def children(S, id):
    return [k for k, e in S.ents.items() if e.get("parent") == id]


def set_z(kit, id, f, z, kids=True):
    """Change de calque à l'image f (et ses enfants, z global : chacun garde son écart au parent)."""
    S = kit.S
    z0 = S.val(id, "z", f - 1, S.ents[id]["z"]) if "z" in S.ents[id]["t"] else S.ents[id]["z"]
    kit.ensure(id, "z", S.ents[id]["z"])
    S.key(id, "z", f, z)
    if kids:
        for c in children(S, id):
            zc = S.ents[c]["z"]
            kit.ensure(c, "z", zc)
            S.key(c, "z", f, round(z + (zc - S.ents[id]["z"]), 2))
    return z0


def fondre(kit, ids, f, step=2, d=8):
    """Les éléments d'un processus fini se résorbent SUR PLACE (dans la vie, sans traverser l'image ni le texte du
    conseil), l'un après l'autre ; le conseil bat une fois : il les a repris. -> image qui suit."""
    for k, id in enumerate(ids):
        kit.vanish(id, f + step * k, d=d)
    kit.pulse("conseil", f + 4, peak=1.1, step=3)
    return f + step * (len(ids) - 1) + d


def pile_push(kit, stack, pid, f, from_pt, d=16):
    """La pile grandit PAR LE BAS : la nouvelle pilule sort du conseil et se pose dans la case du bas (son trajet ne
    croise aucune pilule), pendant que les autres montent d'une case. `stack` : ids du bas vers le haut (modifié)."""
    for k, other in enumerate(stack):
        kit.move(other, f, (PILE_X, PILE_YS[k + 1]), d=d, e="inOut")
    kit.pop(pid, f, from_pt=from_pt, to=[PILE_X, PILE_YS[0]])
    kit.S.key(pid, "pos", f, [PILE_X, PILE_YS[0]], d, "out")
    stack.insert(0, pid)
    return f + d


def rows_state(S, kit, f, red=None, review=(), d=6):
    """Rouge seulement sur la rangée `red` (scène en cours) ; les rangées `review` passent à « à revoir » : encre sur
    aplat cyan pâle (fiche_hl 1, capsule beige effacée)."""
    for i in range(5):
        lid = f"fiche_L{i + 1}"
        r_now = S.val(lid, "red", f - 1, 0)
        if red == i and r_now < 1:
            S.key(lid, "red", f, 1, 3, "out")
        # contrôle muet : une rangée que la vie a rendue fausse RESTE rouge jusqu'à la mise à jour (S21) ; l'effacer
        # se lisait « la ligne est réglée »
    for i in review:
        if S.val(f"fiche_hl{i + 1}", "opacity", f - 1) < 1:
            S.key(f"fiche_hl{i + 1}", "opacity", f, 1, d, "out")
            S.key(f"fiche_L{i + 1}", "slotFill", f, 0, d, "out")


# ---------- raccords (contrat des parties ; couleurs en hex minuscule : S.val rend du minuscule) ----------
def _lo(c):
    return c.lower()


_OFF = lambda *ids: {i: {"scale": 0} for i in ids}   # noqa: E731
_ROWS = [f"fiche_L{i + 1}" for i in range(5)]
_HL = [f"fiche_hl{i + 1}" for i in range(5)]
BADGE_IDS = ["badge_rings", "badge_cradle", "badge_travail", "badge_token", "badge_globe"]


def _rows(red, hl):
    """État des 5 rangées : red = indices rouges, hl = indices surlignés (capsule beige effacée sous l'aplat light)."""
    st = {}
    for i in range(5):
        st[_ROWS[i]] = {"red": 1 if i in red else 0, "slotFill": 0 if i in hl else 1, "pulse": 0, "flash": 0,
                        "fall": 0}
        st[_HL[i]] = {"opacity": 1 if i in hl else 0}
    return st


_COMMON = {   # S07 -> S20 : la photo datée et le conseil inadapté ne changent pas
    "fiche": {"pos": list(FICHE_C), "scale": 1},
    "cadre": {"pos": list(CADRE_C), "scale": 1, "draw": 1, "stroke": _lo(INK)},
    "punaise": {"pos": list(PUNAISE_C), "scale": 1},
    "pastille": {"pos": list(PASTILLE_PHOTO), "scale": 1, "text": T_MARS},
    "pastille_rouge": {"opacity": 1},
    "conseil": {"pos": list(CONSEIL_C), "scale": 1, "rot": CONSEIL_TILT, "fill": _lo(LIGHT)},
    "conseil_rouge": {"opacity": 1},
    "conseil_fil": {"draw": 1, "sag": 60, "from": 0, "opacity": 1},
    "conseil_fil2": {"draw": 0},
    **_OFF("info", "bulle1", "question", "vie_disque1", "vie_disque2", "vie_disque3", "refus"),
    "fil_vie1": {"draw": 0}, "fil_vie2": {"draw": 0}, "fil_vie3": {"draw": 0},
}

ENTRY_P2 = {   # fin de S08 = etat_initial de S09 (image 822)
    **_COMMON,
    **_rows(red=[], hl=[0, 1]),
    "vie": {"pos": list(VIE_C), "scale": 1, "text": T_NOV},
    "marqueur": {"pos": [MARKER_CX, MARKER_Y], "scale": 1, "on": 1, "active": 0, "done0": 0, "done1": 0, "done2": 0},
    "evt_disque": {"pos": list(EVT_C), "scale": 1},
    **{f"q_ligne{i + 1}": {"scale": 1} for i in range(5)},
    "eclat_evt": {"p": 0},
    **_OFF(*(pid for pid, _ in PILE), "evt_rings", "ring_g", "ring_d", "evt_cradle", *BADGE_IDS, "ou_famille",
           "separation", "mini_rings", "mini_cradle", "coeur_g", "coeur_d", "fois2", "vente_fleche",
           "vente_piece"),
}
ENTRY_P3 = {   # fin de S14 = etat_initial de S15 (image 1771)
    **_COMMON,
    **_rows(red=[0, 1, 2], hl=[0, 1, 2]),        # contrôle muet : les rangées touchées RESTENT rouges
    "vie": {"scale": 0},
    "marqueur": {"pos": [MARKER_CX, MARKER_Y], "scale": 1, "on": 1, "active": 1, "done0": 0, "done1": 0, "done2": 0},
    **{bid: {"pos": list(BADGES[i]), "scale": 1} for i, bid in enumerate(BADGE_IDS[:3])},
    **_OFF(*BADGE_IDS[3:]),
    "conseil": {"pos": list(CONSEIL_PULL), "scale": 1, "rot": CONSEIL_TILT, "fill": _lo(LIGHT)},
    **{j[0]: {"pos": [JAUGE_CX, j[4]], "scale": 1, "value": j[3]} for j in JAUGES},
    **{f"{j[0]}_mot": {"scale": 1} for j in JAUGES},
    **{f"{j[0]}_fl": {"scale": 1} for j in JAUGES},
    "fil_jauge1": {"draw": 1}, "fil_jauge2": {"draw": 1}, "fil_jauge3": {"draw": 1},
    **_OFF(*(pid for pid, _ in PILE), "evt_disque", *(f"q_ligne{i + 1}" for i in range(5)), "evt_rings", "ring_g",
           "ring_d", "evt_cradle", "ou_famille", "separation", *(t[0] for t in TRAVAIL), "ou_travail",
           "mini_rings", "mini_cradle", "coeur_g", "coeur_d", "fois2", "vente_fleche", "vente_piece"),
}


def cast(S, kit):
    """Toute la distribution, à son état de l'image 0. Ce qui arrive plus tard : scale=0 (ou draw=0, chars=0,
    opacity=0). Seuls `fin` et son bouton naissent dans kit.outro (p3)."""

    # --- le cadre-photo (derrière la fiche, tracé en S04), sa punaise, l'éclair et le flash (S05) ---
    kit.shape("cadre", list(CADRE_C), kind="round", w=CADRE_W, h=CADRE_H, r=18, fill=PAPER, stroke=INK, sw=4,
              shadow=8, z=6, draw=0)
    S.set("cadre", stroke=INK)                  # hex : clignote en deep (S05)
    kit.shape("punaise", list(PUNAISE_C), kind="circle", w=2 * PUNAISE_R, fill=CYAN, stroke=INK, sw=4, shadow=4,
              z=8.8, scale=0)
    kit.shape("punaise_reflet", [-7, -7], kind="circle", w=12, fill=PAPER, stroke="none", sw=0, shadow=0, z=8.9,
              parent="punaise")
    kit.shape("flash", list(CADRE_C), kind="round", w=CADRE_W, h=CADRE_H, r=18, fill=PAPER, stroke="none", sw=0,
              shadow=0, z=10.8, opacity=0)

    # --- la fiche client : 5 rangées écrites dès l'image 0 ---
    rows = SHEET.add(kit, "fiche", LINES, pos=list(FICHE_C), title=T_FICHE, z=8, typed=False)
    S.set("fiche", rot=0)
    for i, lid in enumerate(rows):
        S.set(lid, grow=1)                      # capsule pleine (60 px), texte centré sur la rangée
        # surligneur (S08, S12, S15) et état « à revoir » : aplat light sous la rangée ; la capsule beige s'efface
        kit.shape(f"fiche_hl{i + 1}", [round((SHEET.x["slot0"] + SHEET.x["slot1"]) / 2, 1), SHEET.rows[i]],
                  kind="round", w=round(SHEET.x["slot1"] - SHEET.x["slot0"]), h=SHEET.slot_h, r=12, fill=LIGHT,
                  stroke="none", sw=0, shadow=0, z=8.5, parent="fiche", opacity=0)
        # nouvelle valeur (S21) : deep Bold, ancrée à droite, tapée après la chute de l'ancienne
        kit.text(f"fiche_v{i + 1}", [SHEET.x["value"], SHEET.rows[i]], NEW_VALUES[i], size=32, weight=700,
                 color=DEEP, anchor="end", z=9.5, parent="fiche", typed=True)
        # S08 : « ? » devant chaque rangée
        S.add(f"q_ligne{i + 1}", "qmark", z=10, parent="fiche")
        S.set(f"q_ligne{i + 1}", pos=[QLIGNE_LOCAL_X, SHEET.rows[i]], scale=0, opacity=1, gs=44)
    S.add("eclair", "sheen", z=10.5, parent="fiche", w=SHEET.w, h=SHEET.h)
    S.set("eclair", pos=[0, 0], p=0)

    # --- la pastille « mars 2023 » (objet du fil) et son liseré rouge ---
    pill(S, "pastille", PASTILLE_HEAD, T_MARS, size=34, fill=CYAN, h=PASTILLE_H, w=PASTILLE_W, z=12,
         scale=PASTILLE_HEAD_K, icon="cal")
    S.set("pastille", text=T_MARS, rot=0, textOp=1)
    outline(kit, "pastille_rouge", "pastille", PASTILLE_W, PASTILLE_H)

    # --- « Toi » (encre, nommé dès l'image 0), le client (papier, entre en S01), le conjoint (S09, à gauche) ---
    toi = Figure(kit, "toi", pos=TOI_HOME, variant="ink", side="left")
    pill(S, "nom_toi", NOM_LOCAL, T_TOI, size=34, fill=LIGHT, h=NOM_H, w=NOM_TOI_W, z=15.8, parent="toi", scale=1)
    client = Figure(kit, "client", pos=CLIENT_C, variant="paper", side="right", tool=False, show=False)
    pill(S, "nom_client", NOM_LOCAL, T_CLIENT, size=34, fill=LIGHT, h=NOM_H, w=NOM_CLIENT_W, z=15.8,
         parent="client", scale=1)
    kit.ensure("client", "look", 0)
    conjoint = Figure(kit, "conjoint", pos=CONJOINT_IN, scale=CONJOINT_K, variant="paper", side="right", tool=False,
                      show=False, z=14.5)
    kit.ensure("conjoint", "look", 0)

    # --- la pilule « Info » (S01-S02) : capsule cyan, étoile, mot ; anneau deep ; éclats ---
    kit.shape("info", list(INFO_C0), kind="round", w=INFO_W, h=INFO_H, r=INFO_H / 2, fill=CYAN, stroke=INK, sw=4,
              shadow=6, z=12, scale=0)
    S.set("info", rot=0)
    kit.shape("info_etoile", [-44, 0], kind="poly", pts=star_pts(), fill=INK, stroke=INK, sw=2, shadow=0, z=12.1,
              parent="info")
    kit.text("info_mot", [16, 0], T_INFO, size=34, weight=700, z=12.1, parent="info")
    kit.shape("info_anneau", [0, 0], kind="round", w=INFO_W + 22, h=INFO_H + 22, r=(INFO_H + 22) / 2, fill="none",
              stroke=DEEP, sw=5, shadow=0, z=11.9, parent="info", draw=0)
    S.add("eclat_info", "burst", z=11.8, r0=50, r1=100, n=8, sw=6, color=DEEP)
    S.set("eclat_info", pos=list(INFO_C0), p=0)
    S.add("eclat_refus", "burst", z=12.5, r0=24, r1=96, n=8, sw=9, color=RED, a0=22.5)   # S01 : la fiche refuse
    # grand « × » rouge au point de contact (S01 « dossier. », S04 « problème, ») : la fiche refuse
    kit.shape("refus", list(REFUS_S01), kind="poly", pts=[[-REFUS_A, -REFUS_A], [REFUS_A, REFUS_A]], closed=False,
              fill="none", stroke=RED, sw=13, shadow=0, z=12.7, scale=0)
    kit.shape("refus_b", [0, 0], kind="poly", pts=[[-REFUS_A, REFUS_A], [REFUS_A, -REFUS_A]], closed=False,
              fill="none", stroke=RED, sw=13, shadow=0, z=12.7, parent="refus")
    S.set("eclat_refus", pos=[FICHE_C[0] - SHEET.w / 2, INFO_BUMP[1]], p=0)

    # --- les trois disques de la vie (S02-S08) et leurs fils tiretés, arrêtés avant L1, L3, L4 ---
    for k, (name, row) in enumerate(zip(("person", "building", "euro"), DISQUES_ROWS)):
        did = f"vie_disque{k + 1}"
        kit.icon(did, list(INFO_CLIENT), name, disc=DISQUE_R, fill=CYAN, shadow=3, z=12.5, scale=0)
        S.add(f"fil_vie{k + 1}", "wire", z=8.8, a={"id": did, "at": [0, 0]},
              b={"id": f"fiche_L{row + 1}", "at": [FIL_VIE_STOP, 0]}, color=DEEP, sw=4, dash=[14, 9])
        S.set(f"fil_vie{k + 1}", draw=0, sag=0, opacity=1)
        S.set(f"fil_vie{k + 1}", **{"from": 0})

    # --- le repère 1-2-3 : seule la légende de l'étape active (naît des disques en S08) ---
    kit.steps_marker(MARKER_LABELS, y=MARKER_Y, cx=MARKER_CX, gap=MARKER_GAP, z=20)
    S.ents["marqueur"]["p"].update(moveBlank=True, labelSize=32, labelShow="active")
    S.set("marqueur", scale=0, on=0, done0=0, done1=0, done2=0)
    # S21 « plus » (p3) : le disque actif garde son chiffre par-dessus done2 : pastille cochée posée dessus (comme V10)
    kit.shape("marqueur_fait3", [MARKER_XS[2], MARKER_Y], kind="circle", w=2 * GEOM["MARKER"]["r"], fill=LIGHT,
              stroke=INK, sw=4, shadow=0, z=20.6, scale=0)
    kit.tick("marqueur_fait3_coche", [0, 1], DEEP, size=26, sw=6, z=20.7, parent="marqueur_fait3", draw=0)

    # --- l'événement familial (S08 : copie du disque 1) et son éclat ---
    kit.icon("evt_disque", list(EVT_C), "person", disc=44, fill=CYAN, shadow=3, z=12.5, scale=0)
    S.add("eclat_evt", "burst", z=12.4, r0=50, r1=120, n=8, sw=6, color=DEEP)
    S.set("eclat_evt", pos=list(EVT_C), p=0)

    # --- la pilule de la vie (S06-S08 ; revient en S21 dans la réponse du client) ---
    pill(S, "vie", VIE_C, T_MARS, size=34, fill=CYAN, h=PASTILLE_H, w=PASTILLE_W, z=12, scale=0, icon="cal")
    S.set("vie", text=T_MARS, textOp=1)

    # --- le conseil (S07-S21) : pill light, liseré rouge, fil vers le bas du cadre ; fil neuf (S21) ---
    pill(S, "conseil", CONSEIL_C, T_CONSEIL, size=34, fill=LIGHT, h=CONSEIL_H, w=CONSEIL_W, z=11, scale=0,
         icon="chat")
    S.set("conseil", rot=0, fill=LIGHT)         # hex : LIGHT -> CYAN (S21)
    outline(kit, "conseil_rouge", "conseil", CONSEIL_W, CONSEIL_H)
    for fid in ("conseil_fil", "conseil_fil2"):
        S.add(fid, "wire", z=10.5, a={"id": "conseil", "at": list(CONSEIL_TOP_LOCAL)},
              b={"id": "cadre", "at": list(CADRE_FIL_LOCAL)}, color=DEEP, sw=4)
        S.set(fid, draw=0, sag=0, opacity=1)
        S.set(fid, **{"from": 0})

    # --- la pile des sujets à revoir (S10, S11, S19) : encre sur papier ---
    pile_w = {}
    for pid, txt in PILE:
        pile_w[pid] = capsule(kit, pid, (PILE_X, PILE_YS[0]), txt, size=32, h=PILE_H, z=13)[1]

    # --- famille : alliances (et leurs deux anneaux), « ou », « Séparation », berceau ---
    png(S, "evt_rings", "RINGS", RINGS_W, RINGS_C, z=5)
    for rid, c in zip(("ring_g", "ring_d"), RINGS_SPLIT[0]):
        kit.shape(rid, list(c), kind="circle", w=2 * RING_R, fill="none", stroke=DEEP, sw=9, shadow=0, z=5.2, scale=0)
    kit.text("ou_famille", list(OU_FAMILLE_C), T_OU, size=56, weight=800, color=DEEP, z=5.5, scale=0)
    pill(S, "separation", SEPARATION_C, T_SEPARATION, size=34, fill=PAPER, h=54, z=5.5, scale=0, shadow=3)
    png(S, "evt_cradle", "CRADLE", CRADLE_W, CRADLE_C, z=5, opacity=0)
    # S09 « sépare » : le cœur qui se brise (deux moitiés, bord commun en zigzag)
    for cid, pts in zip(("coeur_g", "coeur_d"), heart_halves(COEUR_K)):
        kit.shape(cid, list(COEUR_C), kind="poly", pts=pts, fill=CYAN, stroke=INK, sw=5, shadow=5, z=5.2, scale=0)
        S.set(cid, rot=0)

    # --- les badges : disques cyan au pictogramme de leur rangée, au-dessus de la tête du client ---
    for bid, c, ico in zip(BADGE_IDS, BADGES, BADGE_ICONS):
        kit.icon(bid, list(c), ico, disc=BADGE_R, fill=CYAN, shadow=3, z=6, scale=0)
    # S11 : la clause touchée par les deux événements : les pictogrammes famille et enfants posés sur ses bouts
    for mid, ico in (("mini_rings", "person"), ("mini_cradle", "plus")):
        kit.icon(mid, [PILE_X, PILE_YS[3] + MINI_DY], ico, disc=MINI_R, fill=CYAN, shadow=3, z=13.5, scale=0)
    kit.text("fois2", [PILE_X, PILE_YS[3] + FOIS2_DY], "×2", size=52, weight=800, color=DEEP, z=13.5, scale=0)

    # --- travail : un cas à la fois (disque + pictogramme + étiquette), « ou » deep ---
    for tid, txt, icon, rot in TRAVAIL:
        kit.shape(tid, list(CASE_C), kind="circle", w=2 * CASE_R, fill=CYAN, stroke=INK, sw=5, shadow=6, z=5.5,
                  scale=0)
        kit.icon(f"{tid}_ico", [0, 0], icon, s=96, sw=7, z=5.6, parent=tid, rot=rot or None)
        pill(S, f"{tid}_mot", (0, CASE_LBL_DY), txt, size=34, fill=PAPER, h=58, z=5.7, parent=tid, scale=1, shadow=3)
    kit.text("ou_travail", list(OU_TRAVAIL_C), T_OU, size=56, weight=800, color=DEEP, z=5.5, scale=0)

    # --- S14 : les trois barres, leurs légendes, flèches de sens, traits d'avant ; fils vers le conseil ---
    for k, (jid, leg, old, new, y, sens) in enumerate(JAUGES):
        kit.gauge(jid, [JAUGE_CX, y], value=old, w=JAUGE_W, h=JAUGE_H, dir="right", fill=CYAN, empty=PAPER, sw=4,
                  shadow=6, z=12, scale=0)
        kit.text(f"{jid}_mot", [JAUGE_LEG_X, y + JAUGE_LEG_DY], leg, size=JAUGE_LEG_SIZE, weight=700,
                 anchor="start", z=12, scale=0)
        tw = text_width(leg, JAUGE_LEG_SIZE, 700)
        kit.icon(f"{jid}_fl", [round(JAUGE_LEG_X + tw + 32, 1), y + JAUGE_LEG_DY], "arrow", s=52, sw=7,
                 color=RED if sens < 0 else DEEP, z=12, scale=0, rot=90 if sens < 0 else -90)
        x_old = round(-JAUGE_W / 2 + JAUGE_W * old, 1)
        kit.shape(f"{jid}_trait", [x_old, 0], kind="poly", pts=[[0, -30], [0, 30]], closed=False, fill="none",
                  stroke=GHOST, sw=4, dash=[7, 5], shadow=0, z=12.2, parent=jid)
        S.add(f"fil_jauge{k + 1}", "wire", z=11.5, a={"id": jid, "at": [JAUGE_W / 2, 0]},
              b={"id": "conseil", "at": [CONSEIL_FIL_XS[k], -CONSEIL_H / 2]}, color=INK, sw=FIL_JAUGE_SW)
        S.set(f"fil_jauge{k + 1}", draw=0, sag=0, opacity=1)
        S.set(f"fil_jauge{k + 1}", **{"from": 0})

    # --- patrimoine : titre, bloc « Épargne » / « Maison », barre « − Crédit » (rouge : la dette), la pièce ---
    kit.text("patrimoine_titre", list(PATRIMOINE_TITRE_C), T_PATRIMOINE, size=34, weight=700, z=12, typed=True)
    kit.shape("bloc_epargne", list(BLOC_C), kind="round", w=BLOC_W, h=BLOC_H, r=16, fill=CYAN, stroke=INK, sw=4,
              shadow=6, z=12, scale=0)
    tw_e = text_width(T_EPARGNE, 32, 700)
    kit.icon("bloc_epargne_ico", [round(-(44 + tw_e) / 2 + 20, 1), 0], "euro", disc=20, fill=PAPER, shadow=0,
             z=12.2, parent="bloc_epargne")
    kit.text("bloc_epargne_mot", [round(-(44 + tw_e) / 2 + 44 + tw_e / 2, 1), 0], T_EPARGNE, size=32, weight=700,
             z=12.2, parent="bloc_epargne")
    tw_m = text_width(T_MAISON, 32, 700)
    kit.shape("bloc_maison", [MAISON_RECOMP[0], BLOC_C[1]], kind="round", w=MAISON_RECOMP[1], h=BLOC_H, r=16,
              fill=LIGHT, stroke=INK, sw=4, shadow=6, z=12.1, scale=0)
    kit.icon("bloc_maison_ico", [round(-(34 + tw_m) / 2 + 13, 1), 0], "house", s=28, z=12.3, parent="bloc_maison")
    kit.text("bloc_maison_mot", [round(-(34 + tw_m) / 2 + 34 + tw_m / 2, 1), 0], T_MAISON, size=32, weight=700,
             z=12.3, parent="bloc_maison")
    kit.gauge("credit", list(CREDIT_C), value=0, w=CREDIT_W, h=CREDIT_H, dir="right", fill=RED, empty=PAPER, sw=4,
              shadow=6, z=12, scale=0)
    kit.text("credit_mot", [-CREDIT_W / 2 - 12, 0], T_CREDIT, size=32, weight=700, anchor="end", z=12.2,
             parent="credit")
    kit.shape("credit_trait", [round(-CREDIT_W / 2 + CREDIT_W * 0.35, 1), 0], kind="poly", pts=[[0, -28], [0, 28]],
              closed=False, fill="none", stroke=GHOST, sw=4, dash=[7, 5], shadow=0, z=12.2, parent="credit",
              opacity=0)
    kit.icon("piece", [MAISON_RECOMP[0], BLOC_C[1]], "coin", disc=PIECE_R, fill=CYAN, shadow=4, z=12.6, scale=0)
    png(S, "evt_token", "TOKEN", TOKEN_W, TOKEN_C, z=5, opacity=0)
    # S16 « vend » : la maison -> une pièce (vendre refait de l'argent disponible) ; rime avec la pièce de S17
    kit.icon("vente_fleche", list(VENTE_FLECHE), "arrow", s=52, sw=8, color=INK, z=5.5, scale=0, rot=VENTE_ROT)
    kit.icon("vente_piece", list(VENTE_PIECE), "coin", disc=32, fill=CYAN, shadow=4, z=5.5, scale=0)

    # --- étranger : camion, globe ---
    png(S, "evt_truck", "TRUCK", TRUCK_W, TRUCK_C, z=5)
    png(S, "evt_globe", "GLOBE", GLOBE_W, GLOBE_C, z=5, opacity=0)

    # --- la question de « Toi » : « ? » (qmark), petite bulle (S03), grande bulle (S20-S21) et son texte ---
    S.add("question", "qmark", z=17)
    S.set("question", pos=list(Q_S03), scale=0, opacity=1, gs=Q_GS_S03)
    S.add("bulle1", "bubble", z=16, **bubble_params(BULLE1_W, BULLE1_H, Q_S03, BULLE1_C, base=(30, 62)))
    S.set("bulle1", pos=list(BULLE1_C), scale=0, s=0, q=0, glyph=0, pulse=0, opacity=1, rot=0)
    S.add("bulle2", "bubble", z=16, **bubble_params(BULLE2_W, BULLE2_H, BULLE2_TIP, BULLE2_C, base=(90, 150)))
    S.set("bulle2", pos=bulle2_pos(BULLE2_K0), scale=0, s=0, q=0, glyph=0, pulse=0, opacity=1, rot=0)
    kit.text("question_texte", list(QUESTION_TXT), T_QUESTION, size=32, weight=700, anchor="start", z=16.5,
             typed=True)
    # --- S21 : la réponse du client (petite bulle papier, « … ») ---
    S.add("bulle3", "bubble", z=16.2, **bubble_params(BULLE3_W, BULLE3_H, BULLE3_TIP, BULLE3_C, base=(-50, -18),
                                                       sw=4, shadow=4))
    S.set("bulle3", pos=list(BULLE3_C), scale=0, s=0, q=0, glyph=0, pulse=0, opacity=1, rot=0)
    kit.text("bulle3_mot", [0, -8], T_DOTS, size=48, weight=800, z=16.3, parent="bulle3")

    return SimpleNamespace(toi=toi, client=client, conjoint=conjoint, sheet=SHEET, rows=rows, pile_w=pile_w)


def build(S):
    kit = Kit(S)
    c = cast(S, kit)
    only = [p for p in os.environ.get("WTH_PARTS", "").split(",") if p]   # WTH_PARTS=p2 : cette partie seule
    for name in PARTS:
        if not only or name in only:
            importlib.import_module(f".{name}", __name__).part(S, kit, c)
