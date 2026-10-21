"""V02 « Connecter ta banque : les erreurs à éviter » : mise en scène Story, en paquet (une partie par fichier).

Storyboard : scripts/storyboards/V02.json (v1, révisé après le test sans son), version lisible
scripts/storyboards/V02.md. Fil : une seule connexion bancaire. objet_fil = `bouton` (pilule cyan « Connecter ma
banque » en bas de l'écran du téléphone) : cliqué, il tire le câble (S01) ; il donne naissance au « ? » (S02), à
l'étiquette « open banking » (S04) et à l'interrupteur « Accès » (S05) ; il reçoit chaque pastille qui franchit la
porte ; il est recliqué au rembobinage (S19) ; il devient le bouton « S’abonner » de la carte de fin (S22).

Parties (scènes contiguës ; coupes aux changements de composition) :
- p1 : S01-S07, images 0-922 (24 temps forts, 30,8 s). Le clic, le câble, le « ? » qui devient le repère 1-2-3,
  « open banking », la directive DSP2 qui devient la porte, l'interrupteur « Accès », le cadenas, la clé.
- p2 : S08-S14, images 923-1801 (31 temps forts, 29,3 s). Erreur 1 (bulle « Mot de passe », clé touchée, appli qui
  réclame les codes), erreur 2 (la société, son badge, le registre REGAFI de l'ACPR).
- p3 : S15-S22, images 1802-2677 (33 temps forts, 29,2 s). Erreur 3 (appli testée, cadran des mois, coupure des
  deux côtés), Avant / Maintenant, carte de fin.
ENTRY_P2 et ENTRY_P3 (plus bas) sont le contrat des raccords : la partie précédente finit exactement dans cet état,
la suivante l'épingle à first_frame - 1 (kit.pin). Les figurines n'y sont jamais : `toi` est en P2 à l'entrée de p2
et de p3 ; `societe` est à l'échelle 0 à l'entrée de p2 et posée en SOCIETE_C (badge coché) à l'entrée de p3.

Ce fichier déclare TOUTE la distribution à son état de l'image 0 (cast) et les places communes ; chaque partie pose
ses temps forts (pN.py, def part(S, kit, c)). Exception : la carte de fin `fin` et son pointeur `fin_curseur`, que
kit.outro déclare lui-même (p3).

Pas d'IA dans V02 : aucune coche ni faisceau pointillé de l'IA. « Toi » (figurine encre) est seul à toucher, basculer,
barrer, taper et cocher (coches pleines cyan profond). Tirets encre = ce qui n'est pas réel ou pas prouvé (bulle de
pensée, fil qui réclame les codes, badge avant preuve) ; trait plein = connexion réelle, preuve, geste de « Toi ».
Rouge : l'appli qui réclame les codes, après le geste de « Toi » (S10) jusqu'à sa chute (S11), rien d'autre.

Ajout au code partagé que cette mise en scène suppose (facultatif, défaut inchangé) : marker, piste `on` (0 = aucune
étape active : le disque actif est dessiné comme un disque inactif, légendes grises ; 0 -> 1 le fait grandir en
disque cyan). Le repère naît en S03 sans étape active et s'allume sur « Première » (S08).

Écarts d'exécution assumés par rapport au storyboard (places et tailles seulement, aucun sens changé) :
- téléphone 340 x 480 (x 70-410, y 520-1000) et bouton 318 x 66 en 27 px : le libellé tient avec une marge ;
- textes des objets à 28 px au moins (le storyboard en donnait 24-26 ; règle de la série : 32 px visés) ;
- pastilles de données de 32 px (r 16) : le pictogramme « lignes » se lit à taille téléphone ;
- bulle de pensée 230 x 110 en (525, 960) : « Mot de passe » à 28 px tient, loin du mur de la banque ;
- appli douteuse 200 x 230 en (517, 1115) : elle ne touche plus le coin du téléphone ;
- société en x 160 (badge 236 x 50, x 42-278) et registre de 320 px en (480, 1112) : rien ne se chevauche ;
- panneau « Espace client » 320 x 64 : plus large que la banque, il SORT d'elle par un pop (from_pt bas de la
  banque) au lieu d'y être caché ;
- le bouton s'enfonce par une ombre séparée (`bouton_ombre`, enfant) : la pilule n'a pas de piste `press`.
"""
import importlib
import math
import os
from types import SimpleNamespace

from pipeline.story import GEOM, POP, STYLE, text_width
from pipeline.story_kit import Figure, Kit

PARTS = ["p1", "p2", "p3"]                      # S01-S07, S08-S14, S15-S22
ALERT_WORDS = {"Méfiance"}                      # karaoké en rouge : le seul élément rouge (l'appli douteuse, S10)
ACOUSTIC_SNAP = {"gap": 0.2, "window": 0.08}    # temps fort après un silence : calé sur l'attaque audible

# ---------- couleurs (storyboard « style » = pipeline.story.STYLE) ----------
INK, CYAN, DEEP, LIGHT = STYLE["ink"], STYLE["cyan"], STYLE["deep"], STYLE["light"]
PAPER, GREY, RED, BG, RULE = STYLE["paper"], STYLE["grey"], STYLE["red"], STYLE["bg"], STYLE["rule"]
NBSP = " "

# ---------- mise en page (1080 x 1920) ----------
# Action entre x 40-940 et y 160-1270 ; on descend jusqu'à y ≈ 1250 ; sous-titres 1280-1380.
X_MIN, X_MAX, Y_MIN, Y_MAX = 40, 940, 160, 1270
CX = 540                                   # axe de la colonne d'action
GROUND = 1230                              # ligne de sol : pieds des figurines debout
FIG_BASE = GEOM["FIGURE"]["base"]          # 95 : du centre de la figurine à ses pieds (x échelle)


def fig_pos(x, feet=GROUND, s=1.0):
    """Centre d'une figurine d'échelle s dont les pieds sont sur la ligne y = feet (place à donner à walk / enter)."""
    return [x, round(feet - FIG_BASE * s, 2)]


P1 = fig_pos(500)                          # « Toi » près du téléphone : bouton, interrupteur « Accès »
P2 = fig_pos(690)                          # « Toi » sous la banque : clé, fil douteux, registre, appli testée, panneau

# Repère 1-2-3 légendé (S03 -> S22), sans étape active jusqu'à « Première » (piste on)
MARKER_Y, MARKER_GAP, MARKER_LABEL, MARKER_DY = 300, 150, 32, 66
MARKER_XS = [CX - MARKER_GAP, CX, CX + MARKER_GAP]          # 390, 540, 690 (monde)
MARKER_LABELS = ["Codes", "Société", "Accès"]

# Téléphone « Mon budget » (à gauche, toujours là)
PHONE_C, PHONE_W, PHONE_H, PHONE_R = (240, 760), 340, 480, 36          # x 70-410, y 520-1000
PHONE_TITLE_DY, PHONE_RULE_DY = -180, -145                             # en-tête (y 580) et filet (y 615)
BOUTON_C, BOUTON_W, BOUTON_H, BOUTON_SIZE = (240, 890), 318, 66, 27    # objet du fil (x 81-399)
BOUTON_TEXT = "Connecter ma banque"
BOUTON_SHADOW = 6                                                      # ombre dure séparée (enfant `bouton_ombre`)
BOUTON_TAP = (365, 893)                                                # moitié droite : à portée depuis P1
SWITCH_C, SWITCH_W, SWITCH_H = (335, 955), 92, 46                      # interrupteur « Accès » (x 289-381)
SWITCH_LABEL_X = -62                                                   # « Accès » finit à x 273 (ancre end)

# Banque (à droite)
BANK_C, BANK_W, BANK_H = (780, 760), 250, 360                          # x 655-905, y 580-940
BANK_ICON_DY, BANK_TITLE_DY = -120, -58
COMPTES_DY = [-2, 42]                                                  # barres de comptes (y 758, 802)
COMPTE_W, COMPTE_H = 180, 34
BANK_BOTTOM = (780, 940)

# Câble principal : du bord droit du téléphone au bord gauche de la banque ; `via` sur la droite au départ (câble
# droit), puis abaissé dans le tourniquet de la porte (S05 « ouvrir »)
CABLE_A, CABLE_B = (410, 790), (655, 790)
CABLE_VIA_FLAT = [520, 790]                # point de passage sur la droite : même tracé qu'un câble sans via
PORTE_VIA = [520, 830]                     # S05 : le câble passe par le tourniquet

# Porte DSP2 (PNG WTH-002-02) et directive
PORTE_C, PORTE_W = (528, 800), 200
PORTE_DSP2_C = (528, 705)                  # pilule « DSP2 » sur le linteau
DIRECTIVE_C, DIRECTIVE_W, DIRECTIVE_H = (528, 560), 250, 160          # x 403-653 : ne touche pas la banque
DIRECTIVE_CROWN = (-78, 0)                 # couronne de 12 étoiles (repère de la directive), rayon 28
DIRECTIVE_TEXT_X = 45
OPEN_BANKING_C = (528, 735)
CADENAS_C = (655, 650)                     # sur le mur gauche de la banque, au-dessus de la porte
QUESTION_C = (528, 650)                    # « ? » de S02 au-dessus du câble (110 px)
ALERTES_CABLE = [(466, 790), (528, 790), (590, 790)]                   # S03 : posées sur le câble
ALERTE_R = 26
ALERTES_S19 = [(240, 662), (140, 1032), (868, 988)]    # S19 : écran du téléphone, à gauche du badge, câble testé
ALERTE_OK_S21 = (905, 1050)                            # S21 : la coche 3 glisse sur le coin haut de l'appli testée
FIN_BUTTON = (540, 908)                                # bouton de la carte de fin (kit.outro : 380 x 112)

# Clé (PNG WTH-002-03) et carte d'identifiants
CLE_W = 150                                # largeur déclarée ; rangée dans la banque à l'échelle CLE_SMALL (120 px)
CLE_SMALL = 0.8
CLE_HOME = (735, 880)                      # sous les comptes, dans la banque
CLE_TICK = (850, 880)                      # coche de « Toi » à droite de la capsule
COMPTES_EDGE = (880, 780)                  # S07 : la clé tourne au bord droit des barres de comptes
CARTE_ID_C = (550, 985)

# Bulle de pensée « Mot de passe » (S08-S09, S19-S20)
BULLE_C, BULLE_W, BULLE_H = (525, 960), 230, 110       # x 410-640, y 905-1015
BULLE_S19 = (525, 945)                                 # S19 : « Toi » en P1, juste dessous : 15 px plus haut
BULLE_RONDS_R = [5, 7, 9]

# Appli qui réclame les codes (S10-S11)
DOUTEUSE_C, DOUTEUSE_W, DOUTEUSE_H = (517, 1115), 200, 230            # x 417-617, y 1000-1230
DOUTEUSE_START = (-110, 1115)                                          # entre par le bord gauche
DOUTEUSE_TEXT_DY, DOUTEUSE_CHAMP_DY = -55, 13
DOUTEUSE_FIL_A = (592, 1128)               # bout droit du champ
DOUTEUSE_FIL_B = (690, 905)                # contre la capsule de la clé
DOUTEUSE_FIL_MID = (641, 1016)             # milieu : le stylo barre ici, le fil s'y sépare

# Société (figurine papier) et son badge
SOC_SCALE = 0.9
SOCIETE_C = fig_pos(160, s=SOC_SCALE)      # pieds sur le sol, x 107-213
SOC_HIDDEN = (160, 880)                    # cachée derrière le téléphone (z sous lui) avant S11 « société »
BADGE_W, BADGE_H = 236, 50
BADGE_ON_SOC = (160, 1178)                 # sur la poitrine (x 42-278)
BADGE_UNDER_PHONE = (290, 1032)            # S15 -> S22 : accroché sous le bord bas du téléphone
QUESTION2_C = (245, 1078)                  # S12 : le « ? » de « Toi » (90 px), à droite de la tête de la société

# Registre REGAFI (PNG BOOK), champ de recherche, « gratuit »
REGISTRE_C, REGISTRE_W = (480, 1112), 320  # x 320-640
REGISTRE_S20, REGISTRE_S20_SCALE = (480, 1150), 0.8
REG_ROWS = [-26, 6, 38]                    # rangées de la page de gauche (repère du livre)
REG_PHONE_X, REG_TRAIT_X, REG_NAME_X = -118, -70, -102
REG_TITLE_DY = -62
REG_ACPR = (72, 6)                         # pilule « ACPR » sur la page de droite
CHAMP_C, CHAMP_W, CHAMP_H = (530, 962), 230, 52        # x 415-645 : au-dessus du livre, sous la porte
CHAMP_TAP = (600, 962)
GRATUIT_C = (712, 968)

# Cadran des mois, étiquette Avant / Maintenant
CADRAN_C, CADRAN_R = (528, 530), 62
CADRAN_TXT_C = (528, 625)
ETIQUETTE_C = (540, 425)

# Appli testée (en bas à droite), son câble et le panneau « Espace client »
TESTEE_C, TESTEE_W, TESTEE_H = (850, 1135), 160, 200   # x 770-930, y 1035-1235
TESTEE_SWITCH_DY = 65                                   # interrupteur en (850, 1200)
TESTEE_SWITCH = (850, 1200)
CABLE_T_A, CABLE_T_B = (875, 940), (860, 1035)          # du bas de la banque au haut de l'appli testée
ESPACE_C, ESPACE_W, ESPACE_H = (690, 985), 320, 64      # x 530-850, y 953-1017
ESPACE_SWITCH_X = 112                                   # interrupteur du panneau en (802, 985)
ESPACE_SWITCH = (802, 985)

# Interrupteurs : id -> (rond, course du rond depuis le centre)
SWITCHES = {"interrupteur": ("interrupteur_rond", (SWITCH_W - SWITCH_H) / 2),
            "testee_inter": ("testee_rond", 20), "espace_inter": ("espace_rond", 15)}

N_PERLES = 3                               # pastilles de données, réutilisées d'une scène à l'autre


def scene_f0(S, sid):
    """Première image de la scène sid (round(t_start x 30))."""
    return round(next(s for s in S.sb["scenes"] if s["id"] == sid)["t_start"] * S.fps)


# ---------- aides de mouvement communes ----------

def wire_point(S, wid, frac, n):
    """Point monde à la fraction `frac` de la longueur du fil `wid` à l'image n, piste `via` comprise (copie de
    timeline.ts wirePath : S-cubique de A à via, puis segment droit via -> B). Les fils de V02 n'ont pas d'ancres :
    extrémités `pa` / `pb`."""
    from pipeline.story import cubic_at, wire_cubic
    A, B = S.val(wid, "pa", n), S.val(wid, "pb", n)
    via = S.val(wid, "via", n, [])
    via = via if via and len(via) == 2 else None
    cub = wire_cubic(A, via or B, S.val(wid, "sag", n, 0), S.ents[wid]["p"].get("tension", 0.45))
    pts = [cubic_at(cub, i / 32) for i in range(33)] + ([list(B)] if via else [])
    acc = [0.0]
    for i in range(1, len(pts)):
        acc.append(acc[-1] + math.dist(pts[i], pts[i - 1]))
    target = max(0.0, min(1.0, frac)) * acc[-1]
    for i in range(1, len(pts)):
        if acc[i] >= target:
            t = (target - acc[i - 1]) / max(1e-6, acc[i] - acc[i - 1])
            return [pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * t, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * t]
    return pts[-1]


def along(S, id, wid, f, d, t0=0.0, t1=1.0, at=None, e="linear"):
    """L'entité `id` glisse le long du fil `wid` (via compris) de la fraction t0 à t1, en d images (géométrie du fil
    figée à l'image `at`, f par défaut). Remplace S.along_wire, qui ignore `via`. -> f + d."""
    at = f if at is None else at
    S.path(id, f, d, e, lambda p: wire_point(S, wid, t0 + (t1 - t0) * p, at))
    return f + d


def press(S, f, depth=BOUTON_SHADOW, d_in=3, d_out=4):
    """Le bouton s'enfonce dans son ombre (`depth` px vers le bas-droite, d_in images) puis remonte (d_out images) ;
    l'ombre (enfant) reste en place. -> f + d_in + d_out."""
    p = S.val("bouton", "pos", f - 1)
    S.key("bouton", "pos", f, [p[0] + depth, p[1] + depth], d_in, "out")
    S.key("bouton_ombre", "pos", f, [BOUTON_SHADOW - depth, BOUTON_SHADOW - depth], d_in, "out")
    S.key("bouton", "pos", f + d_in, list(p), d_out, "inOut")
    S.key("bouton_ombre", "pos", f + d_in, [BOUTON_SHADOW, BOUTON_SHADOW], d_out, "inOut")
    return f + d_in + d_out


def toggle(S, sw, f, on, d=6):
    """Bascule l'interrupteur `sw` (clé de SWITCHES) : le rond glisse (droite = ON) et la piste passe au cyan (ON) ou
    au papier (OFF), en d images. -> f + d."""
    knob, travel = SWITCHES[sw]
    S.key(knob, "pos", f, [travel if on else -travel, 0], d, "out")
    S.key(sw, "fill", f, CYAN if on else PAPER, d, "out")
    return f + d


def vanish(kit, id, f, into=None, d=POP):
    """kit.vanish, plus un fondu d'opacité sur ses 3 dernières images : pas de point résiduel à taille téléphone."""
    end = kit.vanish(id, f, into=into, d=d)
    kit.S.key(id, "opacity", end - 3, 0, 3, "linear")
    return end


def bulle_ronds(head_c, corner, radii=BULLE_RONDS_R):
    """Places des 3 petits ronds de pensée, de la tête (centre head_c, r 32) vers le coin `corner` de la bulle."""
    hx, hy = head_c
    vx, vy = corner[0] - hx, corner[1] - hy
    L = math.hypot(vx, vy)
    ux, uy = vx / L, vy / L
    start, end = 32 + 4, L - 4
    out = []
    for k, r in enumerate(radii):
        s = start + (end - start) * (0.15 + 0.35 * k)
        out.append([round(hx + ux * s, 1), round(hy + uy * s, 1)])
    return out


def star_pts(r_out=8.0, r_in=3.4):
    """Étoile à 5 branches (pointe en haut), centrée sur l'origine."""
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        r = r_out if k % 2 == 0 else r_in
        pts.append([round(r * math.cos(a), 2), round(r * math.sin(a), 2)])
    return pts


HEAD_DY = GEOM["FIGURE"]["head"]["cy"]     # -64 : centre de la tête (repère de la figurine)

# ---------- raccords : état épinglé au début de p2 (image 922) et de p3 (image 1801) ----------
# Figurines exclues (jamais épinglées) : p2 et p3 les replacent par walk / enter, avec le garde-fou de SKILL.md.
_PERLES_OFF = {f"perle{i + 1}": {"scale": 0} for i in range(N_PERLES)}
_CONNEXION = {   # le montage établi en S05-S07, inchangé jusqu'à la carte de fin
    "appli": {"pos": list(PHONE_C), "scale": 1, "opacity": 1},
    "bouton": {"pos": list(BOUTON_C), "scale": 1, "opacity": 1, "text": BOUTON_TEXT},
    "bouton_ombre": {"pos": [BOUTON_SHADOW, BOUTON_SHADOW]},
    "interrupteur": {"pos": list(SWITCH_C), "scale": 1, "fill": CYAN},
    "interrupteur_rond": {"pos": [SWITCHES["interrupteur"][1], 0]},
    "interrupteur_txt": {"opacity": 1},
    "cable": {"draw": 1, "from": 0, "via": list(PORTE_VIA), "pa": list(CABLE_A), "pb": list(CABLE_B), "sag": 0},
    "porte": {"pos": list(PORTE_C), "scale": 1, "opacity": 1},
    "porte_dsp2": {"pos": list(PORTE_DSP2_C), "scale": 1, "opacity": 1},
    "banque": {"pos": list(BANK_C), "scale": 1, "opacity": 1},
    "cle": {"pos": list(CLE_HOME), "scale": CLE_SMALL, "rot": 0, "opacity": 1},
    "directive": {"scale": 0}, "open_banking": {"scale": 0}, "cadenas": {"scale": 0}, "question": {"scale": 0},
    "carte_id": {"scale": 0},
    **{f"alerte{i + 1}": {"scale": 0} for i in range(3)},
    **_PERLES_OFF,
}
ENTRY_P2 = {   # fin de S07 = etat_initial de S08 : clé rangée dans la banque, repère sans étape active
    **_CONNEXION,
    "marqueur": {"pos": [CX, MARKER_Y], "scale": 1, "active": 0, "on": 0},
    "cle_coche": {"draw": 0},
    "bulle": {"scale": 0}, **{f"bulle_rond{i + 1}": {"scale": 0} for i in range(3)},
    "douteuse": {"scale": 0}, "douteuse_fil1": {"draw": 0}, "douteuse_fil2": {"draw": 0},
    "badge": {"scale": 0}, "question2": {"scale": 0}, "registre": {"scale": 0}, "champ": {"scale": 0},
    "gratuit": {"scale": 0}, "preuve": {"draw": 0},
}
ENTRY_P3 = {   # fin de S14 = etat_initial de S15 : société trouvée au registre, badge plein coché relié par le fil
    **_CONNEXION,
    "marqueur": {"pos": [CX, MARKER_Y], "scale": 1, "active": 1, "on": 1},
    "cle_coche": {"draw": 1},
    "bulle": {"scale": 0}, **{f"bulle_rond{i + 1}": {"scale": 0} for i in range(3)},
    "douteuse": {"scale": 0}, "douteuse_fil1": {"draw": 0}, "douteuse_fil2": {"draw": 0},
    "badge": {"pos": list(BADGE_ON_SOC), "scale": 1, "opacity": 1},
    "badge_plein": {"draw": 1}, "badge_nom": {"chars": len("Société X")}, "badge_coche": {"draw": 1},
    "question2": {"scale": 0},
    "registre": {"pos": list(REGISTRE_C), "scale": 1, "opacity": 1},
    "registre_titre": {"chars": len("REGAFI")},
    **{f"registre_tel{i + 1}": {"scale": 1} for i in range(3)},
    "registre_trait1": {"draw": 1}, "registre_trait2": {"scale": 0}, "registre_trait3": {"draw": 1},
    "registre_nom": {"chars": len("Société X"), "mark": 1}, "registre_coche": {"draw": 1},
    "registre_acpr": {"scale": 1},
    "champ": {"pos": list(CHAMP_C), "scale": 1, "opacity": 1}, "champ_nom": {"chars": 0, "opacity": 0},
    "gratuit": {"pos": list(GRATUIT_C), "scale": 1, "opacity": 1},
    "preuve": {"draw": 1},
    "cadran": {"scale": 0, "value": 0}, "testee": {"scale": 0}, "cable_testee": {"draw": 0},
    "espace_client": {"scale": 0},
}


# ---------- distribution ----------

def _switch(kit, id, pos, w, h, knob_d, on, z, parent=None, scale=1, shadow=4):
    """Interrupteur : piste arrondie (fill papier OFF / cyan ON, hex pour le fondu) + rond encre enfant."""
    S = kit.S
    kit.shape(id, pos, kind="round", w=w, h=h, r=h / 2, fill=CYAN if on else PAPER, stroke=INK, sw=4, shadow=shadow,
              z=z, parent=parent, scale=scale)
    S.set(id, fill=CYAN if on else PAPER)
    knob, travel = SWITCHES[id]
    kit.shape(knob, [travel if on else -travel, 0], kind="circle", w=knob_d, fill=INK, stroke=INK, sw=2, shadow=0,
              z=z + 0.05, parent=id)


def cast(S, kit):
    """Toute la distribution, à son état de l'image 0 : S01 montre le téléphone « Mon budget » et son bouton cyan,
    « Toi » en P1. Ce qui arrive plus tard est déclaré à sa première place avec scale=0 (figurines : show=False)."""

    # --- repère 1-2-3 légendé (S03 -> S22) : sans étape active jusqu'à « Première » (S08) ---
    kit.steps_marker(MARKER_LABELS, id="marqueur", y=MARKER_Y, cx=CX, gap=MARKER_GAP, z=20)
    S.ents["marqueur"]["p"].update(labelSize=MARKER_LABEL, labelDy=MARKER_DY, moveBlank=True)
    S.set("marqueur", scale=0, on=0)

    # --- téléphone « Mon budget », bouton (objet du fil) et son ombre, interrupteur « Accès » ---
    kit.shape("appli", PHONE_C, kind="round", w=PHONE_W, h=PHONE_H, r=PHONE_R, fill=PAPER, stroke=INK, sw=5,
              shadow=6, z=4)
    kit.text("appli_titre", [0, PHONE_TITLE_DY], "Mon budget", size=32, weight=600, z=4.1, parent="appli")
    kit.shape("appli_filet", [0, PHONE_RULE_DY], kind="rect", w=PHONE_W - 40, h=3, fill=RULE, stroke=RULE, sw=0,
              shadow=0, z=4.1, parent="appli")
    S.add("bouton", "pill", z=6, text=BOUTON_TEXT, w=BOUTON_W, h=BOUTON_H, size=BOUTON_SIZE, weight=700, fill=CYAN,
          shadow=0)
    S.set("bouton", pos=list(BOUTON_C), scale=1, opacity=1, text=BOUTON_TEXT, w=BOUTON_W)
    kit.shape("bouton_ombre", [BOUTON_SHADOW, BOUTON_SHADOW], kind="round", w=BOUTON_W, h=BOUTON_H, r=BOUTON_H / 2,
              fill=INK, stroke=INK, sw=4, shadow=0, z=5.9, parent="bouton")
    _switch(kit, "interrupteur", SWITCH_C, SWITCH_W, SWITCH_H, 36, on=False, z=6.2, scale=0)
    kit.text("interrupteur_txt", [SWITCH_LABEL_X, 0], "Accès", size=28, weight=600, anchor="end", z=6.3,
             parent="interrupteur", opacity=0)

    # --- la banque : carte, disque cyan au temple, « Ta banque », deux barres de comptes (euro) ---
    kit.shape("banque", BANK_C, kind="round", w=BANK_W, h=BANK_H, r=30, fill=PAPER, stroke=INK, sw=5, shadow=6, z=4,
              scale=0)
    kit.icon("banque_icone", [0, BANK_ICON_DY], "bank", disc=36, fill=CYAN, z=4.1, parent="banque")
    kit.text("banque_titre", [0, BANK_TITLE_DY], "Ta banque", size=30, weight=700, z=4.1, parent="banque")
    for k, dy in enumerate(COMPTES_DY):
        cid = f"compte{k + 1}"
        kit.shape(cid, [0, dy], kind="round", w=COMPTE_W, h=COMPTE_H, r=10, fill=LIGHT, stroke=INK, sw=3, shadow=0,
                  z=4.2, parent="banque")
        kit.icon(f"{cid}_euro", [-COMPTE_W / 2 + 22, 0], "euro", s=24, z=4.3, parent=cid)

    # --- le câble de la connexion (pa / pb : extrémités monde ; via sur la droite tant qu'il n'y a pas de porte) ---
    S.add("cable", "wire", z=3, color=DEEP, sw=8, dots=True, tension=0.45)
    S.set("cable", pa=list(CABLE_A), pb=list(CABLE_B), via=list(CABLE_VIA_FLAT), sag=0, draw=0, opacity=1)
    S.set("cable", **{"from": 0})

    # --- pastilles de données (pictogramme « lignes de relevé », jamais euro), réutilisées ---
    for i in range(N_PERLES):
        S.add(f"perle{i + 1}", "bullet", z=13, icon="bars", r=16)
        S.set(f"perle{i + 1}", pos=list(BANK_C), scale=0, opacity=1)

    # --- le « ? » (S02-S03) et les trois alertes (S03 ; S19-S21, avec numéros et coches) ---
    S.add("question", "qmark", z=12)
    S.set("question", pos=list(BOUTON_C), scale=0, opacity=1, gs=110)
    for i in range(3):
        a = f"alerte{i + 1}"
        kit.icon(a, ALERTES_CABLE[i], "warning", disc=ALERTE_R, fill=PAPER, shadow=4, z=14, scale=0)
        kit.text(f"{a}_num", [ALERTE_R + 16, -ALERTE_R + 4], str(i + 1), size=26, weight=800, z=14.1, parent=a,
                 opacity=0)
        kit.shape(f"{a}_ok", ALERTES_CABLE[i], kind="circle", w=2 * ALERTE_R, fill=PAPER, stroke=INK, sw=4, shadow=4,
                  z=14, scale=0)
        kit.tick(f"{a}_ok_coche", [0, 0], DEEP, size=30, sw=7, z=14.1, parent=f"{a}_ok", draw=0)

    # --- étiquette « open banking » (S04-S05) ---
    S.add("open_banking", "pill", z=9, text="open banking", w=round(text_width("open banking", 28, 700) + 40), h=56,
          size=28, weight=700, fill=LIGHT)
    S.set("open_banking", pos=list(OPEN_BANKING_C), scale=0, opacity=1)

    # --- la directive DSP2 (S05) : carte, couronne de 12 étoiles encre, « Directive / européenne », « DSP2 » ---
    kit.shape("directive", DIRECTIVE_C, kind="round", w=DIRECTIVE_W, h=DIRECTIVE_H, r=18, fill=PAPER, stroke=INK,
              sw=4, shadow=6, z=9, scale=0)
    for k in range(12):
        a = -math.pi / 2 + k * math.pi / 6
        kit.shape(f"etoile{k + 1}", [round(DIRECTIVE_CROWN[0] + 28 * math.cos(a), 1),
                                     round(DIRECTIVE_CROWN[1] + 28 * math.sin(a), 1)],
                  kind="poly", pts=star_pts(), fill=INK, stroke=INK, sw=0, shadow=0, z=9.1, parent="directive")
    kit.text("directive_txt", [DIRECTIVE_TEXT_X, -24], "Directive\neuropéenne", size=26, weight=600, lh=1.1, z=9.1,
             parent="directive")
    kit.text("directive_dsp2", [DIRECTIVE_TEXT_X, 42], "DSP2", size=40, weight=800, z=9.1, parent="directive",
             underColor=DEEP)
    S.set("directive_dsp2", under=0)

    # --- la porte officielle (PNG WTH-002-02) et sa pilule « DSP2 » ---
    gate = S.png("WTH-002-02")
    S.add("porte", "png", z=7, src=gate["src"], w=PORTE_W, h=round(PORTE_W * gate["h"] / gate["w"]),
          contact=dict(w=round(PORTE_W * 0.8), h=22, dy=4, blur=10, alpha=0.2))
    S.set("porte", pos=list(PORTE_C), scale=0, opacity=1)
    S.add("porte_dsp2", "pill", z=7.5, text="DSP2", w=round(text_width("DSP2", 28, 700) + 36), h=46, size=28,
          weight=700, fill=LIGHT)
    S.set("porte_dsp2", pos=list(PORTE_DSP2_C), scale=0, opacity=1)

    # --- le cadenas du mur de la banque (S06-S07) ---
    kit.icon("cadenas", CADENAS_C, "lock", disc=30, fill=PAPER, shadow=4, z=8, scale=0)

    # --- la carte d'identifiants (S07) puis la clé (PNG WTH-002-03) et sa coche ---
    kit.shape("carte_id", CARTE_ID_C, kind="round", w=220, h=100, r=16, fill=PAPER, stroke=INK, sw=4, shadow=6,
              z=13, scale=0)
    kit.text("carte_id_txt", [0, -20], "Identifiant", size=28, weight=600, z=13.1, parent="carte_id")
    kit.text("carte_id_mdp", [0, 24], "••••••", size=32, weight=700, z=13.1, parent="carte_id")
    key = S.png("WTH-002-03")
    S.add("cle", "png", z=6.5, src=key["src"], w=CLE_W, h=round(CLE_W * key["h"] / key["w"]),
          contact=dict(w=round(CLE_W * 0.7), h=16, dy=2, blur=8, alpha=0.18))
    S.set("cle", pos=list(CARTE_ID_C), scale=0, opacity=1, rot=0)
    kit.tick("cle_coche", CLE_TICK, DEEP, size=40, sw=8, z=6.6, draw=0)

    # --- la bulle de pensée « Mot de passe » (S08-S09, S19-S20) : tirets encre, sans remplissage ---
    kit.shape("bulle", BULLE_C, kind="round", w=BULLE_W, h=BULLE_H, r=30, fill="none", stroke=INK, sw=4,
              dash=[14, 10], shadow=0, z=17, scale=0)
    kit.text("bulle_txt", [0, -22], "Mot de passe", size=28, weight=600, z=17.1, parent="bulle", typed=True)
    kit.icon("bulle_fleche", [-22, 26], "arrow", s=28, z=17.1, parent="bulle", scale=0)
    kit.icon("bulle_tel", [30, 26], "phone", s=36, z=17.1, parent="bulle", scale=0)
    head_p2 = [P2[0], P2[1] + HEAD_DY]
    corner = [BULLE_C[0] + BULLE_W / 2 - 18, BULLE_C[1] + BULLE_H / 2 - 12]
    for k, (pt, r) in enumerate(zip(bulle_ronds(head_p2, corner), BULLE_RONDS_R)):
        kit.shape(f"bulle_rond{k + 1}", pt, kind="circle", w=2 * r, fill="none", stroke=INK, sw=3, dash=[5, 4],
                  shadow=0, z=17, scale=0)

    # --- l'appli qui réclame les codes (S10-S11) : sans en-tête ni bouton cyan ; contour et texte en hex (rouge) ---
    kit.shape("douteuse", DOUTEUSE_C, kind="round", w=DOUTEUSE_W, h=DOUTEUSE_H, r=28, fill=PAPER, stroke=INK, sw=5,
              shadow=6, z=10, scale=0)
    S.set("douteuse", stroke=INK)
    kit.text("douteuse_txt", [0, DOUTEUSE_TEXT_DY], "Tes codes ?", size=28, weight=700, z=10.1, parent="douteuse",
             typed=True)
    S.set("douteuse_txt", color=INK)
    kit.shape("douteuse_champ", [0, DOUTEUSE_CHAMP_DY], kind="round", w=150, h=44, r=10, fill=PAPER, stroke=INK,
              sw=3, shadow=0, z=10.1, parent="douteuse", scale=0)
    kit.shape("douteuse_curseur", [-56, 0], kind="rect", w=3, h=26, fill=INK, stroke=INK, sw=0, shadow=0, z=10.2,
              parent="douteuse_champ")
    for k, (a, b) in enumerate(((DOUTEUSE_FIL_A, DOUTEUSE_FIL_MID), (DOUTEUSE_FIL_MID, DOUTEUSE_FIL_B))):
        wid = f"douteuse_fil{k + 1}"   # deux moitiés d'un même fil droit (tension 0) : il se sépare au trait du stylo
        S.add(wid, "wire", z=9.5, color=INK, sw=4, dash=[16, 10], tension=0)
        S.set(wid, pa=list(a), pb=list(b), sag=0, draw=0, opacity=1, color=INK)

    # --- la société derrière l'appli (figurine papier, sans outil) et son badge (groupe invisible + enfants) ---
    societe = Figure(kit, "societe", pos=list(SOC_HIDDEN), scale=SOC_SCALE, variant="paper", tool=False, z=3,
                     show=False)
    kit.shape("badge", BADGE_ON_SOC, kind="circle", w=2, fill="none", stroke="none", sw=0, shadow=0, z=16, scale=0)
    kit.shape("badge_fond", [0, 0], kind="round", w=BADGE_W, h=BADGE_H, r=BADGE_H / 2, fill=PAPER, stroke=INK, sw=4,
              dash=[12, 8], shadow=0, z=16, parent="badge")
    kit.shape("badge_plein", [0, 0], kind="round", w=BADGE_W, h=BADGE_H, r=BADGE_H / 2, fill="none", stroke=DEEP,
              sw=5, shadow=0, z=16.1, parent="badge", draw=0)
    kit.icon("badge_icone", [-BADGE_W / 2 + 28, 0], "building", s=28, z=16.2, parent="badge")
    kit.text("badge_nom", [-6, 0], "Société X", size=28, weight=700, z=16.2, parent="badge", typed=True)
    kit.tick("badge_coche", [BADGE_W / 2 - 28, 0], DEEP, size=30, sw=7, z=16.2, parent="badge", draw=0)
    S.add("question2", "qmark", z=17)
    S.set("question2", pos=list(QUESTION2_C), scale=0, opacity=1, gs=90)

    # --- le registre REGAFI (PNG BOOK), ses inscriptions, « ACPR », le champ de recherche, « gratuit », la preuve ---
    book = S.png("BOOK")
    book_h = round(REGISTRE_W * book["h"] / book["w"])
    S.add("registre", "png", z=11, src=book["src"], w=REGISTRE_W, h=book_h,
          contact=dict(w=round(REGISTRE_W * 0.8), h=22, dy=4, blur=10, alpha=0.18))
    S.set("registre", pos=list(REGISTRE_C), scale=0, opacity=1)
    kit.text("registre_titre", [0, REG_TITLE_DY], "REGAFI", size=32, weight=800, z=11.2, parent="registre",
             typed=True)
    for k, dy in enumerate(REG_ROWS):
        kit.icon(f"registre_tel{k + 1}", [REG_PHONE_X, dy], "phone", s=26, z=11.1, parent="registre", scale=0)
        kit.shape(f"registre_trait{k + 1}", [REG_TRAIT_X, dy], kind="round", w=60, h=8, r=4, fill=INK, stroke=INK,
                  sw=0, shadow=0, z=11.1, parent="registre", draw=0)
    kit.text("registre_nom", [REG_NAME_X, REG_ROWS[1]], "Société X", size=24, weight=700, anchor="start", z=11.2,
             parent="registre", typed=True, markColor=LIGHT)
    S.set("registre_nom", mark=0)
    kit.tick("registre_coche", [REG_NAME_X + text_width("Société X", 24, 700) + 22, REG_ROWS[1]], DEEP, size=28,
             sw=7, z=11.3, parent="registre", draw=0)
    S.add("registre_acpr", "pill", z=11.2, parent="registre", text="ACPR", w=round(text_width("ACPR", 28, 800) + 30),
          h=46, size=28, weight=800, fill=PAPER, stroke=DEEP, color=DEEP, shadow=4)
    S.set("registre_acpr", pos=list(REG_ACPR), scale=0, opacity=1)
    kit.shape("champ", CHAMP_C, kind="round", w=CHAMP_W, h=CHAMP_H, r=12, fill=PAPER, stroke=DEEP, sw=3, shadow=0,
              z=12, scale=0)
    kit.shape("champ_curseur", [-CHAMP_W / 2 + 18, 0], kind="rect", w=3, h=30, fill=INK, stroke=INK, sw=0, shadow=0,
              z=12.2, parent="champ")
    kit.text("champ_nom", [0, 0], "Société X", size=28, weight=700, z=12.1, parent="champ", typed=True)
    S.add("gratuit", "pill", z=12, text="gratuit", w=round(text_width("gratuit", 28, 700) + 36), h=48, size=28,
          weight=700, fill=LIGHT)
    S.set("gratuit", pos=list(GRATUIT_C), scale=0, opacity=1)
    S.add("preuve", "wire", z=15.8, color=DEEP, sw=5, dots=True, tension=0.45)   # sous le badge, au-dessus du livre
    S.set("preuve", pa=list(REGISTRE_C), pb=list(BADGE_ON_SOC), sag=0, draw=0, opacity=1)

    # --- cadran des mois (S15-S17, S21) et ses textes ---
    kit.sector("cadran", CADRAN_C, start=0, value=0, r=CADRAN_R, unit=12, face=PAPER, fill=DEEP, ticks=12, sw=5,
               z=9, scale=0)
    kit.text("cadran_txt", CADRAN_TXT_C, f"6{NBSP}mois", size=40, weight=800, z=9, scale=0)
    kit.text("cadran_routine", CADRAN_TXT_C, f"tous les 6{NBSP}mois", size=28, weight=700, z=9, typed=True)

    # --- appli testée (S15-S22), son interrupteur, sa lune, son câble ; panneau « Espace client » (S18-S19) ---
    kit.shape("testee", TESTEE_C, kind="round", w=TESTEE_W, h=TESTEE_H, r=26, fill=PAPER, stroke=INK, sw=5,
              shadow=6, z=10, scale=0)
    S.set("testee", fill=PAPER)                  # hex : fondu vers GREY quand elle s'éteint (S16)
    kit.text("testee_titre", [0, -52], "Appli\ntestée", size=28, weight=600, lh=1.1, z=10.1, parent="testee")
    kit.icon("testee_lune", [0, 12], "moon", s=44, z=10.1, parent="testee", scale=0)
    _switch(kit, "testee_inter", [0, TESTEE_SWITCH_DY], 80, 40, 30, on=False, z=10.2, parent="testee", shadow=3)
    S.add("cable_testee", "wire", z=9.5, color=DEEP, sw=6, dots=True, tension=0.45)
    S.set("cable_testee", pa=list(CABLE_T_A), pb=list(CABLE_T_B), sag=0, draw=0, opacity=1)
    kit.shape("espace_client", ESPACE_C, kind="round", w=ESPACE_W, h=ESPACE_H, r=18, fill=PAPER, stroke=INK, sw=4,
              shadow=6, z=8, scale=0)
    kit.icon("espace_icone", [-ESPACE_W / 2 + 26, 0], "bank", s=28, z=8.1, parent="espace_client")
    kit.text("espace_txt", [-18, 0], "Espace client", size=28, weight=600, z=8.1, parent="espace_client")
    _switch(kit, "espace_inter", [ESPACE_SWITCH_X, 0], 64, 34, 26, on=True, z=8.2, parent="espace_client", shadow=3)

    # --- étiquettes « ◀◀ Avant » puis « Maintenant » (S19-S22) ---
    S.add("etiquette_avant", "pill", z=21, text="Avant", icon="rewind", w=round(text_width("Avant", 30, 700) + 84),
          h=56, size=30, weight=700, fill=LIGHT)
    S.set("etiquette_avant", pos=list(ETIQUETTE_C), scale=0, opacity=1)
    S.add("etiquette_maint", "pill", z=21, text="Maintenant", w=round(text_width("Maintenant", 30, 700) + 48), h=56,
          size=30, weight=700, fill=LIGHT)
    S.set("etiquette_maint", pos=list(ETIQUETTE_C), scale=0, opacity=1)

    # --- « Toi » : en P1 dès l'image 0, stylo levé (côté gauche : il fait face au téléphone) ---
    toi = Figure(kit, "toi", pos=list(P1), z=15)

    return SimpleNamespace(toi=toi, societe=societe, book_h=book_h, porte_h=round(PORTE_W * gate["h"] / gate["w"]),
                           cle_h=round(CLE_W * key["h"] / key["w"]))


def build(S):
    kit = Kit(S)
    c = cast(S, kit)
    only = [p for p in os.environ.get("WTH_PARTS", "").split(",") if p]   # WTH_PARTS=p2 : cette partie seule
    for name in PARTS:
        if not only or name in only:
            importlib.import_module(f".{name}", __name__).part(S, kit, c)
