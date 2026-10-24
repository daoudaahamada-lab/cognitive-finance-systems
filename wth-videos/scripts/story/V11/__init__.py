"""V11 « La meilleure info n’est pas dans le dossier » : mise en scène Story, en paquet (une partie par fichier).

Storyboard : scripts/storyboards/V11.json (v1, révisé après le test sans son, 22 scènes, 93 temps forts, 93,015 s),
version lisible scripts/storyboards/V11.md. Voix : build/V11/words.json (film : images 0-2790, FILM_END = 2791).
Fil : la pastille cyan « mars 2023 » (`pastille`, pill 250 x 62, pictogramme cal, Bold 34) : sur l'en-tête de la fiche
dès l'image 0 (échelle 0,76), légende de la photo (S05), engendre la pilule de la vie (S06), cerclée de rouge (S07-S20),
mise à jour « nov. 2026 » par le stylo de « Toi » (S21), bouton « S’abonner » de la carte de fin (S22).
Parti pris « la photo et la vie » : à droite la fiche du client (une photo épinglée, datée), à gauche sa vie (une date
qui avance, des événements qui tombent au-dessus de lui) ; la question de « Toi » est le seul pont.

Parties (scènes contiguës, coupées sur un changement de composition) :
- p1 : S01-S08, images 0-822 (27 temps forts, 27,4 s). Accroche, contexte (photo datée, vie, conseil rouge), étape 1.
- p2 : S09-S14, images 823-1771 (32 temps forts, 31,6 s). Famille (alliances, berceau, pile) et travail (barres).
- p3 : S15-S22, images 1772-2790 (34 temps forts, 33,9 s). Patrimoine, déménagement, question, mise à jour, fin.
ENTRY_P2 et ENTRY_P3 sont le contrat des raccords (kit.pin(f0 - 1, …)). Les figurines n'y sont jamais.

Aucune entité nouvelle : tout se compose avec le catalogue.
- Contour qui rougit (pastille, conseil) : la pill n'a pas de piste `stroke` ; un liseré rouge enfant (`*_rouge`,
  shape round fill none, même taille) passe en fondu (opacity 0 -> 1, puis 1 -> 0 en S21).
- Pilules « à revoir », pilules de travail : capsules = shape round (piste `stroke` en hex) + texte enfant (+ pictogramme
  sur disque) : `capsule()`.
- Surligneur des rangées : la line n'a pas de piste `mark` ; un aplat light (`fiche_hlN`, sous la rangée) paraît pendant
  que la capsule beige de la rangée s'efface (slotFill 1 -> 0), et l'inverse.
- Nouvelle valeur de rangée (S21) : texte deep enfant de la fiche (`fiche_vN`, ancré à droite, tapé) ; l'ancienne valeur
  tombe (piste `fall` de la line).
- Pilule « Info » : capsule cyan + étoile en polygone (pas de pictogramme étoile) + anneau deep (shape, draw).

ÉCARTS DE PLACE (raisons de mise en page, aucun sens changé) :
- conseil (580, 1195), 270 de large (x 445-715) au lieu de (550, 1195) x 300 : le conjoint (S09) tient entre le client
  et le conseil sans collision (entrée x 340, recul x 380) ; « Toi » le touche en (715, 1195) (S14) ;
- bloc « Patrimoine » 460 de large (x 320-780) : « Épargne » + pictogramme tiennent dans la part réduite (220 px) ;
- S20 : « Toi » s'arrête en x 700 (et non 690) ; S21 « dernier » : la pastille descend de 30 px (690, 868) en battant
  (repli prévu au storyboard) : sa pointe gauche (592, 870) est alors à portée (d 261 px, côté sûr) ;
- S22 : « Toi » touche le bouton en (615, 975), sous la droite du libellé (une cible à droite de son épaule ferait
  passer le bras par la tête).
"""
import importlib
import math
import os
from types import SimpleNamespace

from pipeline.story import GEOM, STYLE, text_width
from pipeline.story_kit import Figure, Kit, Sheet

PARTS = ["p1", "p2", "p3"]                      # S01-S08, S09-S14, S15-S22
NBSP = " "                                 # espace insécable (avant « : », « ? », dans les guillemets)
ALERT_WORDS = {"dépassée", "inadapté"}          # karaoké en rouge : ce que la vie a rendu faux (S07)
ACOUSTIC_SNAP = {"gap": 0.2, "window": 0.08}    # temps fort après un silence : calé sur l'attaque audible
# découpes imposées : sans elles, « dossier | client », « situation | dépassée », « clause | bénéficiaire »,
# « objectif | d’épargne » et « a | changé » étaient coupés
CAPTION_GROUPS = [
    ["Un dossier client", "est une photo", "prise à une date"],
    ["Et un conseil", "fondé sur", "une situation dépassée", "peut devenir inadapté"],
    ["Nouvel", "objectif d’épargne", "protection du foyer", "prévoyance", "et clause bénéficiaire", "à mettre à jour"],
    ["Qu’est-ce qui", "a changé depuis", "notre dernier échange"],
]

FILM_END = 2791                                 # images 0-2790 (93,015 s)

# ---------- couleurs ----------
INK, CYAN, DEEP, LIGHT = STYLE["ink"], STYLE["cyan"], STYLE["deep"], STYLE["light"]
PAPER, RED, GREY, BG = STYLE["paper"], STYLE["red"], STYLE["grey"], STYLE["bg"]

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
TRAVAIL = [  # S13 : (id, texte, pictogramme, rotation du pictogramme)
    ("travail1", "Entreprise", "building", 0), ("travail2", "Emploi perdu", "minus", 0),
    ("travail3", "Promotion", "arrow", -90), ("travail4", "Retraite", "hourglass", 0),
]
JAUGES = [  # S14 : (id, légende, niveau d'avant, nouveau niveau, y)
    ("jauge_revenus", "Revenus", 0.6, 0.25, 945), ("jauge_fiscalite", "Fiscalité", 0.4, 0.75, 1025),
    ("jauge_liquidites", "Liquidités", 0.3, 0.85, 1105),
]
T_PATRIMOINE, T_EPARGNE, T_MAISON, T_CREDIT = "Patrimoine", "Épargne", "Maison", "Crédit"
T_QUESTION = f"«{NBSP}Qu’est-ce qui\na changé depuis\nnotre dernier\néchange{NBSP}?{NBSP}»"

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
TOI_RDV = fig_pos(700)                          # (700, 1135) S20-S22 (« rendez-vous ») ; épaule (670, 1119)
CLIENT_C = fig_pos(220)                         # (220, 1135), tourné vers « Toi » (side « right »)
CLIENT_FROM_X = 40                              # S01 « client » : entre en marchant depuis le bord gauche
CONJOINT_K = 0.95
CONJOINT_IN = fig_pos(340, s=CONJOINT_K)        # (340, 1140) S09 « marie » (x 284-396 : entre client et conseil)
CONJOINT_OUT = fig_pos(380, s=CONJOINT_K)       # (380, 1140) S09 « sépare » : recule, penché en arrière
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
PUNAISE_C, PUNAISE_R = (690, 330), 16
CADRE_FIL_LOCAL = (-110, CADRE_H / 2)           # bas du cadre (580, 875) : là où s'accroche le fil du conseil
PASTILLE_W, PASTILLE_H = 250, 62
PASTILLE_HEAD, PASTILLE_HEAD_K = (566, 365), 0.76  # S01-S05 : en-tête (x 471-661 ; « Fiche client » de 684 à 889)
PASTILLE_PHOTO = (690, 838)                     # S05-S21 : marge basse du cadre (x 565-815)
PASTILLE_LOW = (690, 868)                       # S21 « dernier » : descend de 30 px (à portée de « Toi » en x 700)
PASTILLE_TAP = (592, 870)                       # S21 « C’est » : contact (bout gauche de la pastille)

# --- la vie du client ---
INFO_C0, INFO_W, INFO_H = (330, 640), 150, 62   # S01 « meilleure »
INFO_BUMP = (390, 640)                          # S01 « dans » : bord gauche contre la fiche (465)
INFO_BACK = (355, 640)                          # S01 « dossier. » : rebond
INFO_CLIENT = (220, 870)                        # S01 « Elle » : au-dessus du client
VIE_C = (220, 915)                              # la pilule de la vie (date du client)
DISQUE_R = 36
DISQUES_S02 = [(95, 560), (220, 560), (345, 560)]   # personne, immeuble, euro
DISQUES_S03 = [(410, 445), (410, 605), (410, 685)]  # au bord gauche de la fiche, à côté de L1, L3, L4
DISQUES_S04 = [(95, 430), (220, 430), (345, 430)]   # repoussés au-dessus du client
DISQUES_ROWS = [0, 2, 3]                        # rangées reliées (L1, L3, L4)
EVT_C = (225, 650)                              # centre de la colonne de la vie : les événements tombent ici
BADGES = [(75, 430), (155, 430), (235, 430), (315, 430), (395, 430)]   # alliances, berceau, immeuble, maison, globe
BADGE_R, BADGE_PNG = 36, 52
MINI_R, MINI_PNG = 22, 32

# --- le repère 1-2-3 (en haut) ---
MARKER_Y, MARKER_CX, MARKER_GAP = 200, 540, 200   # disques x 340, 540, 740 ; légende Bold 32 à y 262
MARKER_XS = [MARKER_CX - MARKER_GAP, MARKER_CX, MARKER_CX + MARKER_GAP]

# --- le conseil (au sol entre les deux personnages) et la pile des sujets à revoir ---
CONSEIL_C, CONSEIL_W, CONSEIL_H = (580, 1195), 270, 64        # x 445-715, y 1163-1227
CONSEIL_RDV = (450, 1195)                       # S20 : glisse entre les deux personnages (x 315-585)
CONSEIL_TILT = 8                                # penché (S07-S21)
CONSEIL_TOP_LOCAL = (0, -CONSEIL_H / 2)
CONSEIL_TAP = (715, 1195)                       # S14 « conseil » : bout droit
CONSEIL_SPAWN = (660, 1175)                     # S07 « conseil » : sous la pointe du stylo
PILE_X, PILE_YS, PILE_H = 550, [1103, 1041, 979, 917], 54     # de bas en haut
CLAUSE_MINI_L, CLAUSE_MINI_R = (395, 917), (785, 917)         # S11 : mini-badges aux bouts de « Clause bénéficiaire »
CLAUSE_TOP, CLAUSE_TOP_W = (590, 917), 441      # S11 (p2) : en haut, la pilule s'élargit (x 370-811) : badges hors du texte

# --- S09 (famille) et S13 (travail) : cas reliés par « ou » ---
OU_FAMILLE_C, SEPARATION_C = (225, 785), (225, 845)
TRAVAIL_YS, OU_TRAVAIL_YS, TRAVAIL_H = [500, 610, 720, 830], [555, 665, 775], 60

# --- S14 : les barres du travail (x 510-740) ---
JAUGE_CX, JAUGE_W, JAUGE_H, JAUGE_LEG_X = 625, 230, 44, 498   # x 510-740 (p2) : « Revenus » libre de la pilule vie
CONSEIL_FIL_XS = [-60, 0, 60]                   # arrivée des trois fils encre en haut du conseil (local)

# --- S15-S17 : le patrimoine ---
BLOC_C, BLOC_W, BLOC_H = (550, 1000), 460, 70   # x 320-780
PATRIMOINE_TITRE_C = (550, 920)
EPARGNE_RECOMP = (430, 220)                     # S17 « recompose » : (centre x, largeur) x 320-540
MAISON_RECOMP = (662.5, 235)                    # x 545-780
EPARGNE_FIN = (460, 280)                        # S17 « apparaître » : x 320-600
MAISON_FIN = (692.5, 175)                       # x 605-780
CREDIT_C, CREDIT_W, CREDIT_H = (550, 1100), 460, 44
PIECE_R = 26

# --- les illustrations (une seule à la fois dans la vie du client) ---
PNG_W = {"RINGS": 240, "CRADLE": 250, "TOKEN": 220, "TRUCK": 280, "GLOBE": 220}
TRUCK_C, TRUCK_FROM = (225, 660), (-140, 660)
GLOBE_C = (225, 640)

# --- la question de « Toi » (S03 : petite bulle ; S20-S21 : grande bulle) ---
Q_GS_S03, Q_GS_S20, Q_GS_COIN = 64, 64, 40
BULLE1_C, BULLE1_W, BULLE1_H = (650, 975), 150, 110
BULLE1_TIP = (788, 1050)                        # S03 : queue vers la tête de « Toi » (820, 1071)
BULLE2_C, BULLE2_W, BULLE2_H = (260, 760), 400, 220   # x 60-460, y 650-870
BULLE2_TIP = (665, 1048)                        # S20 : queue vers la tête de « Toi » en TOI_RDV (700, 1071)
BULLE2_K0 = 0.65                                # S20 « pose » : 260 x 150, puis « ouverte. » : 1 (queue fixe, voir
                                                # bulle2_pos)
Q_COIN = (95, 685)                              # S20 « ouverte. » : le « ? » dans le coin haut gauche
QUESTION_TXT = (95, 715)                        # S21 : 4 lignes, ancre start
FIN_BTN_TAP = (615, 975)                        # S22 « comprendre » : sous la droite du libellé du bouton


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


for _x, _pt, _what in [(TOI_HOME[0], (705, 1000), "S03 « ? » à la pointe"), (TOI_HOME[0], CONSEIL_SPAWN, "S07"),
                       (TOI_HOME[0], CONSEIL_TAP, "S14 conseil"), (TOI_RDV[0], PASTILLE_TAP, "S21 pastille"),
                       (TOI_RDV[0], FIN_BTN_TAP, "S22 bouton")]:
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


def capsule(kit, id, pos, text, size=32, weight=700, h=54, fill=PAPER, icon=None, icon_rot=0, z=13, parent=None,
            shadow=3, scale=0):
    """Pilule composée (piste `stroke` disponible, hex) : shape round + pictogramme sur disque cyan (facultatif) +
    texte enfant `id`_mot (ancre start avec pictogramme, sinon centré). Renvoie (id, largeur)."""
    tw = text_width(text, size, weight)
    if icon:
        w = round(24 + 40 + 12 + tw + 24)
    else:
        w = round(tw + 48)
    kit.shape(id, list(pos), kind="round", w=w, h=h, r=h / 2, fill=fill, stroke=INK, sw=4, shadow=shadow, z=z,
              parent=parent, scale=scale)
    kit.S.set(id, stroke=INK)                   # hex : INK -> RED en fondu
    if icon:
        kit.icon(f"{id}_ico", [-w / 2 + 44, 0], icon, disc=20, fill=CYAN, shadow=0, z=z + 0.1, parent=id,
                 rot=icon_rot or None)
        kit.text(f"{id}_mot", [-w / 2 + 76, 0], text, size=size, weight=weight, anchor="start", z=z + 0.1, parent=id)
    else:
        kit.text(f"{id}_mot", [0, 0], text, size=size, weight=weight, z=z + 0.1, parent=id)
    return id, w


def png(S, id, name, w, pos, z=5, contact=True, parent=None, scale=0):
    """Illustration générique (verre, alpha strict), largeur w, rapport gardé."""
    m = S.png(name)
    h = round(w * m["h"] / m["w"])
    p = dict(contact=dict(w=round(w * 0.7), h=22, dy=4, blur=10, alpha=0.2)) if contact else {}
    S.add(id, "png", z=z, parent=parent, src=m["src"], w=w, h=h, **p)
    S.set(id, pos=list(pos), scale=scale, opacity=1, rot=0)
    return id


def badge(kit, id, pos, name=None, icon=None, r=BADGE_R, png_w=BADGE_PNG, z=6, scale=0):
    """Badge d'un événement : disque papier contour encre + PNG (ou pictogramme) ; enfant `id`_png."""
    S = kit.S
    if icon:
        kit.icon(id, list(pos), icon, disc=r, fill=PAPER, shadow=3, z=z, scale=scale)
        return id
    kit.shape(id, list(pos), kind="circle", w=2 * r, fill=PAPER, stroke=INK, sw=4 if r > 30 else 3, shadow=3, z=z,
              scale=scale)
    png(S, f"{id}_png", name, png_w, [0, 0], z=z + 0.1, contact=False, parent=id, scale=1)
    return id


def star_pts(r_out=13, r_in=5.5):
    """Étoile à 5 branches (poly fermée), pointe en haut."""
    pts = []
    for k in range(10):
        a = math.radians(-90 + 36 * k)
        r = r_out if k % 2 == 0 else r_in
        pts.append([round(r * math.cos(a), 2), round(r * math.sin(a), 2)])
    return pts


def bubble_params(w, h, tip_world, center, base=(-30, 10), q=0):
    shape = dict(w=w, h=h, r=26, q=56, qx=0, px=0, ps=0, sw=5, shadow=6, gs=4)
    return dict(big=shape, small=dict(shape), tail=[round(tip_world[0] - center[0], 1),
                                                     round(tip_world[1] - center[1], 1)], tailBase=list(base))


# ---------- raccords (contrat des parties ; couleurs en hex minuscule : S.val rend du minuscule) ----------
def _lo(c):
    return c.lower()


_OFF = lambda *ids: {i: {"scale": 0} for i in ids}   # noqa: E731
_ROWS = [f"fiche_L{i + 1}" for i in range(5)]
_HL = [f"fiche_hl{i + 1}" for i in range(5)]


def _rows(red, hl):
    """État des 5 rangées : red = indices rouges, hl = indices surlignés (capsule beige effacée sous l'aplat light)."""
    st = {}
    for i in range(5):
        st[_ROWS[i]] = {"red": 1 if i in red else 0, "slotFill": 0 if i in hl else 1, "pulse": 0, "flash": 0,
                        "fall": 0}
        st[_HL[i]] = {"opacity": 1 if i in hl else 0}
    return st


_COMMON = {   # S07 -> S21 : la photo datée et le conseil inadapté ne changent pas
    "fiche": {"pos": list(FICHE_C), "scale": 1},
    "cadre": {"pos": list(CADRE_C), "scale": 1, "draw": 1, "stroke": _lo(INK)},
    "punaise": {"pos": list(PUNAISE_C), "scale": 1},
    "pastille": {"pos": list(PASTILLE_PHOTO), "scale": 1, "text": T_MARS},
    "pastille_rouge": {"opacity": 1},
    "vie": {"pos": list(VIE_C), "scale": 1, "text": T_NOV},
    "conseil": {"pos": list(CONSEIL_C), "scale": 1, "rot": CONSEIL_TILT, "fill": _lo(LIGHT)},
    "conseil_rouge": {"opacity": 1},
    "conseil_fil": {"draw": 1, "sag": 30, "from": 0, "opacity": 1},
    "conseil_fil2": {"draw": 0},
    **_OFF("info", "bulle1", "question", "vie_disque1", "vie_disque2", "vie_disque3"),
    "fil_vie1": {"draw": 0}, "fil_vie2": {"draw": 0}, "fil_vie3": {"draw": 0},
}

ENTRY_P2 = {   # fin de S08 = etat_initial de S09 (image 822)
    **_COMMON,
    **_rows(red=[], hl=[0, 1]),
    "marqueur": {"pos": [MARKER_CX, MARKER_Y], "scale": 1, "on": 1, "active": 0, "done0": 0, "done1": 0, "done2": 0},
    "evt_disque": {"pos": list(EVT_C), "scale": 1},
    **{f"q_ligne{i + 1}": {"scale": 1} for i in range(5)},
    "eclat_evt": {"p": 0},
    **_OFF(*(pid for pid, _ in PILE), "evt_rings", "badge_rings", "mini_rings", "evt_cradle", "badge_cradle",
           "mini_cradle", "ou_famille", "separation"),
}
ENTRY_P3 = {   # fin de S14 = etat_initial de S15 (image 1771)
    **_COMMON,
    **_rows(red=[0, 1, 2], hl=[2]),
    "marqueur": {"pos": [MARKER_CX, MARKER_Y], "scale": 1, "on": 1, "active": 1, "done0": 0, "done1": 0, "done2": 0},
    "badge_rings": {"pos": list(BADGES[0]), "scale": 1},
    "badge_cradle": {"pos": list(BADGES[1]), "scale": 1},
    "badge_travail": {"pos": list(BADGES[2]), "scale": 1},
    **{jid: {"pos": [JAUGE_CX, y], "scale": 1, "value": new} for jid, _, _, new, y in JAUGES},
    **{f"{jid}_mot": {"scale": 1} for jid, *_ in JAUGES},
    **{f"{jid}_trait": {"scale": 1} for jid, *_ in JAUGES},
    "fil_jauge1": {"draw": 1}, "fil_jauge2": {"draw": 1}, "fil_jauge3": {"draw": 1},
    **_OFF(*(pid for pid, _ in PILE), "evt_disque", *(f"q_ligne{i + 1}" for i in range(5)), "evt_rings",
           "mini_rings", "evt_cradle", "mini_cradle", "ou_famille", "separation", *(t[0] for t in TRAVAIL),
           "ou_travail1", "ou_travail2", "ou_travail3"),
}


def cast(S, kit):
    """Toute la distribution, à son état de l'image 0. Ce qui arrive plus tard : scale=0 (ou draw=0, chars=0,
    opacity=0). Seuls `fin` et son bouton naissent dans kit.outro (p3)."""

    # --- le cadre-photo (derrière la fiche, tracé en S04), sa punaise, l'éclair (S05) ---
    kit.shape("cadre", list(CADRE_C), kind="round", w=CADRE_W, h=CADRE_H, r=18, fill=PAPER, stroke=INK, sw=4,
              shadow=8, z=6, draw=0)
    S.set("cadre", stroke=INK)                  # hex : clignote en deep (S05)
    kit.shape("punaise", list(PUNAISE_C), kind="circle", w=2 * PUNAISE_R, fill=CYAN, stroke=INK, sw=3, shadow=3,
              z=8.8, scale=0)

    # --- la fiche client : 5 rangées écrites dès l'image 0 ---
    rows = SHEET.add(kit, "fiche", LINES, pos=list(FICHE_C), title=T_FICHE, z=8, typed=False)
    S.set("fiche", rot=0)
    for i, lid in enumerate(rows):
        S.set(lid, grow=1)                      # capsule pleine (60 px), texte centré sur la rangée
        # surligneur (S08, S12, S15) : aplat light sous la rangée ; la capsule beige s'efface (slotFill) en même temps
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

    # --- « Toi » (encre, nommé dès l'image 0) et le client (papier, entre en S01) ---
    toi = Figure(kit, "toi", pos=TOI_HOME, variant="ink", side="left")
    pill(S, "nom_toi", NOM_LOCAL, T_TOI, size=34, fill=LIGHT, h=NOM_H, w=NOM_TOI_W, z=15.8, parent="toi", scale=1)
    client = Figure(kit, "client", pos=CLIENT_C, variant="paper", side="right", tool=False, show=False)
    pill(S, "nom_client", NOM_LOCAL, T_CLIENT, size=34, fill=LIGHT, h=NOM_H, w=NOM_CLIENT_W, z=15.8,
         parent="client", scale=1)
    kit.ensure("client", "look", 0)
    conjoint = Figure(kit, "conjoint", pos=CONJOINT_IN, scale=CONJOINT_K, variant="paper", side="left", tool=False,
                      show=False, z=14.5)

    # --- la pilule « Info » (S01-S02) : capsule cyan, étoile, mot ; anneau deep ; éclat ---
    kit.shape("info", list(INFO_C0), kind="round", w=INFO_W, h=INFO_H, r=INFO_H / 2, fill=CYAN, stroke=INK, sw=4,
              shadow=6, z=12, scale=0)
    kit.shape("info_etoile", [-44, 0], kind="poly", pts=star_pts(), fill=INK, stroke=INK, sw=2, shadow=0, z=12.1,
              parent="info")
    kit.text("info_mot", [16, 0], T_INFO, size=34, weight=700, z=12.1, parent="info")
    kit.shape("info_anneau", [0, 0], kind="round", w=INFO_W + 22, h=INFO_H + 22, r=(INFO_H + 22) / 2, fill="none",
              stroke=DEEP, sw=5, shadow=0, z=11.9, parent="info", draw=0)
    S.add("eclat_info", "burst", z=11.8, r0=50, r1=100, n=8, sw=6, color=DEEP)
    S.set("eclat_info", pos=list(INFO_C0), p=0)

    # --- les trois disques de la vie (S02-S08) et leurs fils vers L1, L3, L4 ---
    for k, (name, row) in enumerate(zip(("person", "building", "euro"), DISQUES_ROWS)):
        did = f"vie_disque{k + 1}"
        kit.icon(did, list(INFO_CLIENT), name, disc=DISQUE_R, fill=CYAN, shadow=3, z=12.5, scale=0)
        S.add(f"fil_vie{k + 1}", "wire", z=8.8, a={"id": did, "at": [0, 0]},
              b={"id": f"fiche_L{row + 1}", "at": [SHEET.x["bullet"], 0]}, color=DEEP, sw=3)
        S.set(f"fil_vie{k + 1}", draw=0, sag=0, opacity=1)
        S.set(f"fil_vie{k + 1}", **{"from": 0})

    # --- le repère 1-2-3 légendé (naît des disques en S08) ---
    kit.steps_marker(MARKER_LABELS, y=MARKER_Y, cx=MARKER_CX, gap=MARKER_GAP, z=20)
    S.ents["marqueur"]["p"].update(moveBlank=True, labelSize=32)
    S.set("marqueur", scale=0, on=0, done0=0, done1=0, done2=0)
    # S21 « plus » (p3) : le disque actif garde son chiffre par-dessus done2 : pastille cochée posée dessus (comme V10)
    kit.shape("marqueur_fait3", [MARKER_XS[2], MARKER_Y], kind="circle", w=2 * GEOM["MARKER"]["r"], fill=LIGHT,
              stroke=INK, sw=4, shadow=0, z=20.6, scale=0)
    kit.tick("marqueur_fait3_coche", [0, 1], DEEP, size=26, sw=6, z=20.7, parent="marqueur_fait3", draw=0)

    # --- l'événement familial (S08 : copie du disque 1) et son éclat ---
    kit.icon("evt_disque", list(EVT_C), "person", disc=44, fill=CYAN, shadow=3, z=12.5, scale=0)
    S.add("eclat_evt", "burst", z=12.4, r0=50, r1=120, n=8, sw=6, color=DEEP)
    S.set("eclat_evt", pos=list(EVT_C), p=0)

    # --- la pilule de la vie (S06-S21) ---
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

    # --- la pile des sujets à revoir (S10, S11, S19) ---
    pile_w = {}
    for pid, txt in PILE:
        pile_w[pid] = capsule(kit, pid, (PILE_X, PILE_YS[0]), txt, size=32, h=PILE_H, z=13)[1]

    # --- famille : alliances, « ou », « Séparation », berceau ; badges et mini-badges ---
    png(S, "evt_rings", "RINGS", PNG_W["RINGS"], EVT_C, z=5)
    kit.text("ou_famille", list(OU_FAMILLE_C), T_OU, size=40, weight=800, z=5.5, scale=0)
    pill(S, "separation", SEPARATION_C, T_SEPARATION, size=34, fill=PAPER, h=54, z=5.5, scale=0, shadow=3)
    png(S, "evt_cradle", "CRADLE", PNG_W["CRADLE"], EVT_C, z=5)
    badge(kit, "badge_rings", BADGES[0], "RINGS")
    badge(kit, "badge_cradle", BADGES[1], "CRADLE")
    badge(kit, "mini_rings", CLAUSE_MINI_L, "RINGS", r=MINI_R, png_w=MINI_PNG, z=13.5)
    badge(kit, "mini_cradle", EVT_C, "CRADLE", r=MINI_R, png_w=MINI_PNG, z=13.5)

    # --- travail : quatre cas reliés par « ou », badge immeuble ; les trois barres ---
    for (tid, txt, icon, rot), y in zip(TRAVAIL, TRAVAIL_YS):
        capsule(kit, tid, (EVT_C[0], y), txt, size=34, h=TRAVAIL_H, icon=icon, icon_rot=rot, z=5.5)
    for k, y in enumerate(OU_TRAVAIL_YS):
        kit.text(f"ou_travail{k + 1}", [EVT_C[0], y], T_OU, size=34, weight=800, z=5.5, scale=0)
    badge(kit, "badge_travail", BADGES[2], icon="building")
    for k, (jid, leg, old, new, y) in enumerate(JAUGES):
        kit.gauge(jid, [JAUGE_CX, y], value=old, w=JAUGE_W, h=JAUGE_H, dir="right", fill=CYAN, empty=PAPER, sw=4,
                  shadow=6, z=12, scale=0)
        kit.text(f"{jid}_mot", [JAUGE_LEG_X, y], leg, size=34, weight=700, anchor="end", z=12, scale=0)
        x_old = round(-JAUGE_W / 2 + JAUGE_W * old, 1)
        kit.shape(f"{jid}_trait", [x_old, 0], kind="poly", pts=[[0, -32], [0, 32]], closed=False, fill="none",
                  stroke=INK, sw=4, shadow=0, z=12.2, parent=jid, scale=0)
        x_new = round(-JAUGE_W / 2 + JAUGE_W * new, 1)
        S.add(f"fil_jauge{k + 1}", "wire", z=11.5, a={"id": jid, "at": [x_new, JAUGE_H / 2]},
              b={"id": "conseil", "at": [CONSEIL_FIL_XS[k], -CONSEIL_H / 2]}, color=INK, sw=3)
        S.set(f"fil_jauge{k + 1}", draw=0, sag=0, opacity=1)
        S.set(f"fil_jauge{k + 1}", **{"from": 0})

    # --- patrimoine : titre, bloc « Épargne » / « Maison », barre « Crédit », trois pièces ; maison, badge ---
    kit.text("patrimoine_titre", list(PATRIMOINE_TITRE_C), T_PATRIMOINE, size=34, weight=700, z=12, typed=True)
    kit.shape("bloc_epargne", list(BLOC_C), kind="round", w=BLOC_W, h=BLOC_H, r=16, fill=CYAN, stroke=INK, sw=4,
              shadow=6, z=12, scale=0)
    kit.icon("bloc_epargne_ico", [-44 - text_width(T_EPARGNE, 34, 700) / 2, 0], "euro", disc=22, fill=PAPER,
             shadow=0, z=12.2, parent="bloc_epargne")
    kit.text("bloc_epargne_mot", [16, 0], T_EPARGNE, size=34, weight=700, z=12.2, parent="bloc_epargne")
    kit.shape("bloc_maison", [MAISON_RECOMP[0], BLOC_C[1]], kind="round", w=MAISON_RECOMP[1], h=BLOC_H, r=16,
              fill=LIGHT, stroke=INK, sw=4, shadow=6, z=12.1, scale=0)
    kit.icon("bloc_maison_ico", [-40 - text_width(T_MAISON, 34, 700) / 2, 0], "house", s=30, z=12.3,
             parent="bloc_maison")
    kit.text("bloc_maison_mot", [14, 0], T_MAISON, size=34, weight=700, z=12.3, parent="bloc_maison")
    kit.gauge("credit", list(CREDIT_C), value=0, w=CREDIT_W, h=CREDIT_H, dir="right", fill=GREY, empty=PAPER, sw=4,
              shadow=6, z=12, scale=0)
    kit.text("credit_mot", [-CREDIT_W / 2 + 20, 0], T_CREDIT, size=34, weight=700, anchor="start", z=12.2,
             parent="credit")
    for k in range(3):
        kit.icon(f"piece{k + 1}", [MAISON_RECOMP[0], BLOC_C[1]], "coin", disc=PIECE_R, fill=CYAN, shadow=3,
                 z=12.6, scale=0)
    png(S, "evt_token", "TOKEN", PNG_W["TOKEN"], EVT_C, z=5)
    badge(kit, "badge_token", BADGES[3], "TOKEN")

    # --- étranger : camion, globe, badge ---
    png(S, "evt_truck", "TRUCK", PNG_W["TRUCK"], TRUCK_C, z=5)
    png(S, "evt_globe", "GLOBE", PNG_W["GLOBE"], GLOBE_C, z=5)
    badge(kit, "badge_globe", BADGES[4], "GLOBE")

    # --- la question de « Toi » : « ? » (qmark), petite bulle (S03), grande bulle (S20-S21) et son texte ---
    S.add("question", "qmark", z=17)
    S.set("question", pos=[705, 1000], scale=0, opacity=1, gs=Q_GS_S03)
    S.add("bulle1", "bubble", z=16, **bubble_params(BULLE1_W, BULLE1_H, BULLE1_TIP, BULLE1_C, base=(20, 50)))
    S.set("bulle1", pos=list(BULLE1_C), scale=0, s=0, q=0, glyph=0, pulse=0, opacity=1, rot=0)
    S.add("bulle2", "bubble", z=16, **bubble_params(BULLE2_W, BULLE2_H, BULLE2_TIP, BULLE2_C, base=(90, 150)))
    S.set("bulle2", pos=bulle2_pos(BULLE2_K0), scale=0, s=0, q=0, glyph=0, pulse=0, opacity=1, rot=0)
    kit.text("question_texte", list(QUESTION_TXT), T_QUESTION, size=32, weight=700, anchor="start", z=16.5,
             typed=True)

    return SimpleNamespace(toi=toi, client=client, conjoint=conjoint, sheet=SHEET, rows=rows, pile_w=pile_w)


def build(S):
    kit = Kit(S)
    c = cast(S, kit)
    only = [p for p in os.environ.get("WTH_PARTS", "").split(",") if p]   # WTH_PARTS=p2 : cette partie seule
    for name in PARTS:
        if not only or name in only:
            importlib.import_module(f".{name}", __name__).part(S, kit, c)
