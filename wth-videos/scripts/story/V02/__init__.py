"""V02 « Connecter ta banque : les erreurs à éviter » : mise en scène Story, en paquet (une partie par fichier).

Storyboard : scripts/storyboards/V02.json (v1, révisé après le test sans son), version lisible
scripts/storyboards/V02.md. Fil : une seule connexion bancaire. objet_fil = `bouton` (bouton cyan « Connecter / ma
banque » en bas de l'écran du téléphone) : cliqué, il tire le câble (S01) ; il donne naissance au « ? » (S02), à
l'étiquette « open banking » (S04) et à l'interrupteur « Accès » (S05) ; il reçoit chaque pastille qui franchit la
porte ; il est recliqué au rembobinage (S19) ; il devient le bouton « S’abonner » de la carte de fin (S22).

Parties (scènes contiguës ; coupes aux changements de composition) :
- p1 : S01-S07, images 0-922. Le clic, le câble, le « ? » qui devient le repère 1-2-3, « open banking », la directive
  DSP2 qui devient la porte, l'interrupteur « Accès », le cadenas sur le mur, la clé qui ouvre les comptes.
- p2 : S08-S14, images 923-1801. Erreur 1 (bulle « Mot de passe » : un mini « Mon budget » avec une clé fantôme en
  tirets, clé touchée à la banque, appli douteuse dont le fil contourne la porte), erreur 2 (la société qui sort de
  derrière le téléphone, son badge relié au téléphone, le registre REGAFI au sceau de l'autorité).
- p3 : S15-S22, images 1802-2677. Erreur 3 (appli testée branchée À TRAVERS la porte, cadran des mois, coupure des
  deux côtés), Avant / Maintenant sur le même montage (alertes numérotées -> coches de « Toi »), carte de fin.
ENTRY_P2 et ENTRY_P3 (plus bas) sont le contrat des raccords : la partie précédente finit exactement dans cet état,
la suivante l'épingle à first_frame - 1 (kit.pin). Les figurines n'y sont jamais.

Mise en page (revue 1) : la scène principale est descendue et agrandie (câble à y 860, porte de 260 px, clé de 150 px
à l'échelle 1, téléphone 300 x 416, banque 240 x 376) ; les accessoires de passage vivent dans la bande basse
y 980-1250 (bulle, appli douteuse, société, registre, appli testée, panneau « Espace client ») ; « Toi » est à
l'échelle 1,1, pieds sur y 1238, et se place TOUJOURS à droite de ce qu'il touche (bras côté gauche : jamais de bras
en travers du buste). Textes des objets à 32 px au moins.

Pas d'IA dans V02. « Toi » (figurine encre) est seul à toucher, basculer, barrer, taper et cocher (coches pleines
cyan profond). Tirets encre = ce qui n'est pas réel ou pas prouvé (bulle de pensée, clé fantôme, fil qui réclame les
codes, badge et attache avant preuve) ; trait plein = connexion réelle, preuve, geste de « Toi ». Rouge : l'appli qui
réclame les codes, après le geste de « Toi » (S10) jusqu'à sa chute (S11), rien d'autre.

Code partagé que cette mise en scène suppose (facultatif, défaut inchangé) : marker, pistes `on` et `done0..2` (étape
faite : légende à l'encre, coche dans le disque) ; piste `look` de la figure
(profil) ; kit.vanish style="burst" (éclats en tirets de la bulle, S09 et S20) ; kit.outro clear="fade".

Écarts d'exécution assumés par rapport au storyboard (places et tailles seulement, aucun sens changé) :
- bouton sur deux lignes « Connecter / ma banque » (32 px) : sur une ligne, il faudrait 380 px ;
- câble de l'appli testée branché au tourniquet de la porte (il descend de la porte vers l'appli) : toutes les données
  passent par la porte ; les pastilles de S17 la traversent ;
- S06 « pirate » : une pastille d'intrusion venue du téléphone rebondit sur le mur avant que le cadenas s'y pose ;
- S08 : la bulle est grande (380 x 270) et basse ; le mini « Mon budget » montre la clé fantôme DANS son écran,
  étiquetée « Mot de passe » (pas de flèche) ; S09 « l’appli. » : le stylo barre la clé fantôme avant l'éclatement ;
- S13-S14 : registre PNG à 300 px ; inscriptions sur une feuille papier (code) posée sur la page de droite ;
  « REGAFI » sur un bandeau au-dessus du livre ; champ et « gratuit » (à gauche du champ) au-dessus du livre ;
- S18 : le panneau « Espace client » s'ouvre dans la carte de la banque, avec deux lignes ON ;
- S20 « vérifies » : une pilule « REGAFI » (le registre en raccourci) tombe d'en haut, au lieu du livre réduit ;
- badge vérifié accroché sous le téléphone ; les alertes résolues retournent à leur disque du repère ;
- le bouton s'enfonce par une ombre séparée (`bouton_ombre`, enfant).
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
CAPTION_GROUPS = [["Mais tu sais", "ce que tu as", "autorisé"],
                  ["Parce que", "ce sont les clés"], ["Et le bon réflexe", "pour chacune"],
                  ["enregistrés", "auprès de l’ACPR"], ["gratuitement", "sur le registre REGAFI"],
                  ["Coupe-le", "dans les réglages"], ["Et tous les", "6 mois", "tu fais le tri."],
                  ["Tu peux le vérifier"], ["en tapant le nom"],
                  ["croire que", "l’appli connaît", "ton mot de passe."],
                  ["Une appli te demande", "directement", "tes codes bancaires"],
                  ["Ça ne suffit pas"],
                  ["que tu n’utilises plus."],
                  ["qui est derrière l’appli."],
                  ["dans ton espace client", "aussi."],
                  ]

# ---------- couleurs (storyboard « style » = pipeline.story.STYLE) ----------
INK, CYAN, DEEP, LIGHT = STYLE["ink"], STYLE["cyan"], STYLE["deep"], STYLE["light"]
PAPER, GREY, RED, BG, RULE = STYLE["paper"], STYLE["grey"], STYLE["red"], STYLE["bg"], STYLE["rule"]
NBSP = " "

# ---------- mise en page (1080 x 1920) ----------
# Action entre x 40-940 et y 160-1270 ; bande basse jusqu'à y ≈ 1250 ; sous-titres 1280-1380.
X_MIN, X_MAX, Y_MIN, Y_MAX = 40, 940, 160, 1270
CX = 540
GROUND = 1238                              # ligne de sol : pieds des figurines
FIG_BASE = GEOM["FIGURE"]["base"]          # 95 : du centre de la figurine à ses pieds (x échelle)
TOI_SCALE = 1.1


def fig_pos(x, feet=GROUND, s=TOI_SCALE):
    """Centre d'une figurine d'échelle s dont les pieds sont sur la ligne y = feet."""
    return [x, round(feet - FIG_BASE * s, 2)]


P1 = fig_pos(370)                          # « Toi » à droite du téléphone : bouton, interrupteur « Accès »
P2 = fig_pos(770)                          # « Toi » sous la banque, à droite de tout ce qu'il touche
P_BACK = fig_pos(450)                      # S19 : « Toi » recule (rembobinage) avant le bond vers P1
HEAD_DY = GEOM["FIGURE"]["head"]["cy"]     # -64 : centre de la tête (repère de la figurine, x échelle)

# Repère 1-2-3 légendé (S03 -> S22), sans étape active jusqu'à « Première » (piste on)
MARKER_Y, MARKER_GAP, MARKER_LABEL, MARKER_DY = 270, 150, 32, 66
MARKER_XS = [CX - MARKER_GAP, CX, CX + MARKER_GAP]          # 390, 540, 690
MARKER_LABELS = ["Codes", "Société", "Accès"]

# Téléphone « Mon budget » (à gauche)
PHONE_C, PHONE_W, PHONE_H, PHONE_R = (200, 768), 300, 416, 36          # x 50-350, y 560-976
PHONE_TITLE_DY, PHONE_RULE_DY = -168, -133                             # en-tête (y 600) et filet (y 635)
RELEVE_DY, RELEVE_W, RELEVE_H = [-96, -58, -20], 228, 30               # lignes de relevé de l'écran (y 672-748)
BOUTON_C, BOUTON_W, BOUTON_H, BOUTON_SIZE = (200, 840), 250, 96, 32    # objet du fil, deux lignes (y 792-888)
BOUTON_TEXT = "Connecter\nma banque"
BOUTON_SHADOW = 6
BOUTON_TAP = (292, 846)                                                # bout droit : à portée depuis P1
SWITCH_C, SWITCH_W, SWITCH_H = (290, 932), 92, 46                      # interrupteur « Accès » (x 244-336)
SWITCH_LABEL_X = -62                                                   # « Accès » finit à x 228 (ancre end)

# Banque (à droite)
BANK_C, BANK_W, BANK_H = (800, 788), 240, 376                          # x 680-920, y 600-976
BANK_ICON_DY, BANK_TITLE_DY = -140, -84
COMPTES_DY = [-34, 8]                                                  # barres de comptes (y 754, 796)
COMPTE_W, COMPTE_H = 190, 34
BANK_BOTTOM = (800, 976)
COMPTES_MID = (BANK_C[0], BANK_C[1] + (COMPTES_DY[0] + COMPTES_DY[1]) / 2 - 1)   # entre les deux barres (800, 774)

# Câble principal : bord droit du téléphone -> bord gauche de la banque ; via par le tourniquet dès S05
CABLE_A, CABLE_B = (350, 860), (680, 860)
CABLE_VIA_FLAT = [515, 860]
PORTE_VIA = [515, 864]

# Porte DSP2 (PNG WTH-002-02), directive, barrière tant que l'accès est sur OFF
PORTE_C, PORTE_W = (515, 820), 260         # x 385-645, y 727-913
PORTE_DSP2_C = (515, 696)                  # pilule « DSP2 » sur le linteau
PORTE_UE_C, PORTE_UE_R = (422, 700), 26    # couronne d'étoiles de la directive, gardée sur l'arche (S05 -> S22)
BARRIERE_C, BARRIERE_W, BARRIERE_H = (612, 862), 18, 110   # barre encre en travers du câble, côté banque (S05-S06)
INTER_RING = (290, 932)                    # S06 : anneau cyan profond autour de l'interrupteur OFF quand on bute
DIRECTIVE_C, DIRECTIVE_W, DIRECTIVE_H = (515, 470), 300, 170           # x 365-665, y 385-555 : au-dessus de tout
DIRECTIVE_TEXT_Y = -38
DIRECTIVE_CROWN, DIRECTIVE_CROWN_R = (-86, 42), 28
DIRECTIVE_DSP2 = (44, 42)
OPEN_BANKING_C = (515, 762)
CADENAS_C = (680, 700)                     # S06 : sur le mur gauche de la banque, au point du choc (au-dessus du câble)
MUR_C, MUR_H = (680, 730), 150             # S06 : trait du mur gauche (y 655-805)
QUESTION_C = (515, 735)
ALERTES_CABLE = [(430, 860), (515, 860), (600, 860)]
ALERTE_R, ALERTE_NUM = 36, 34
ALERTES_S19 = [(92, 1222), (100, 1070), (557, 955)]   # bord bas gauche de la bulle, sous le bout gauche du badge,
                                                       # câble de l'appli testée : jamais sur un texte
FIN_BUTTON = (540, 908)                                # bouton de la carte de fin (kit.outro : 380 x 112)

# Clé (PNG WTH-002-03) et carte d'identifiants
CLE_W = 150                                # échelle 1 : capsule 150 x 80, clé plate cyan profond par-dessus
CLE_HOME = (775, 920)                      # sous le câble, dans la banque (x 700-850, y 880-960)
CLE_TICK = (885, 920)
COMPTES_KEY = (800, 786)                   # S07 : la clé tourne dans les comptes (debout, échelle 0,9)
CARTE_ID_C = (560, 1062)                   # x 440-680, y 1007-1117 : à gauche de la tête de « Toi » en P2

# Bulle de pensée (S08-S09 ; S19-S20) : un mini « Mon budget » dont l'écran montre une clé fantôme en tirets,
# étiquetée « Mot de passe » ; dans la bande basse (x 310-690, y 973-1243)
BULLE_C, BULLE_W, BULLE_H = (482, 1108), 380, 270
BULLE_S19, BULLE_S19_K = (178, 1176), 0.5              # S19 : en bas à gauche, réduite (l'appli testée occupe le centre)
BULLE_RONDS_R = [5, 7, 9]
BULLE_TEL_W, BULLE_TEL_H = 240, 222
GHOST_KEY = (6, -20)                       # clé fantôme : dans l'écran du mini-téléphone (repère de la bulle)

# Appli qui réclame les codes (S10-S11) : en bas à gauche, en-tête encre au loup (masque), contour épais, pas de cyan
DOUTEUSE_C, DOUTEUSE_W, DOUTEUSE_H = (190, 1158), 210, 168            # x 85-295, y 1074-1242
DOUTEUSE_START = (-95, 1158)
DOUTEUSE_FIL_A = (296, 1150)               # bord droit de l'appli
DOUTEUSE_FIL_MID = (525, 1060)             # loin sous la porte (70 px d'air au moins) ; le stylo coupe ici
DOUTEUSE_FIL_B = (660, 975)                # la pince bute sur le trait du mur, juste devant la clé : jamais dedans
MUR_BAS_C, MUR_BAS_H = (680, 935), 84      # S10 : trait du mur devant la clé (y 893-977), cadenas posé dessus
CADENAS_BAS = (680, 920)

# Société (figurine papier, échelle 1) et son badge ; attache en tirets vers le téléphone
SOC_SCALE = 1.05                           # figurine papier devant une tour de bureaux (enfant soc_tour)
SOCIETE_C = fig_pos(190, s=SOC_SCALE)      # [190, 1138] : tour jusqu'à y 994
SOC_HIDDEN = (215, 862)                    # cachée derrière le téléphone (z 3 < 4)
TOUR_W, TOUR_H, TOUR_CY = 200, 232, -21   # tour de bureaux derrière la société (repère de la figurine : y -137..95)
TOUR_WINDOWS = ([(x, -112) for x in (-72, -36, 0, 36, 72)]                       # rangée haute (de part et d'autre de la tête)
                + [(x, y) for y in (-70, -30, 10, 50) for x in (-82, 82)])    # colonnes latérales, hors du buste
BADGE_W, BADGE_H = 270, 56
BADGE_ICON_S = 44                          # immeuble agrandi (x 1,5) dès l'apparition
BADGE_CASE_X = BADGE_W / 2 - 26            # case de coche (vide, en tirets, S12) puis coche (S14)
BADGE_ON_SOC = (190, 1168)                 # sur la poitrine (x 55-325)
BADGE_UNDER_PHONE = (190, 1006)            # S15 -> S22 : accroché sous le téléphone (x 55-325, y 978-1034)
QUESTION2_C = (340, 1030)                  # S12 : le « ? » de « Toi », à droite de la tour de la société

# Registre REGAFI (PNG BOOK, 300 px) : sceau de l'autorité et « ACPR » sur la page de gauche ; une feuille papier
# plate (code) posée sur la page de droite porte les inscriptions ; « REGAFI » sur un bandeau au-dessus du livre
REGISTRE_C, REGISTRE_W = (480, 1150), 300  # x 330-630, y 1050-1250
REG_SHEET, REG_SHEET_W, REG_SHEET_H = (70, -4), 220, 150   # feuille (repère du livre) : monde x 440-660, y 1071-1221
REG_PAGE_ROT = -3
REG_ROWS = [-46, 0, 46]                    # rangées (repère de la feuille)
REG_PHONE_X, REG_TRAIT_X = -78, -6
REG_NAME_X, REG_TICK_X = -92, 78           # nom (ancre start) et coche de la rangée du milieu, dans la feuille
REG_DOT_X = -102                           # bout gauche de la rangée : départ du fil de preuve
REG_BANDEAU = (0, -100)                    # bandeau « REGAFI » à cheval sur le haut du livre (repère du livre)
REG_SEAL = (-85, -52)                      # sceau rond (étoiles + colonne), 64 px
REG_ACPR = (-88, -8)                       # « ACPR » tamponnée sous le sceau
CHAMP_C, CHAMP_W, CHAMP_H = (530, 1000), 210, 48        # x 425-635, y 976-1024 : au-dessus du livre
CHAMP_TAP = (600, 1002)
GRATUIT_C = (343, 1000)                    # À GAUCHE du champ : le bras de « Toi » (à droite) ne le couvre jamais
REGAFI_PILL_C = (262, 1166)                # S20 : le registre en raccourci tombe là où était la bulle
P_REG = fig_pos(450)                       # S20 : « Toi » à portée de la pilule « REGAFI »

# Cadran des mois, étiquette Avant / Maintenant (bande haute) ; S21 : cadran plus bas, cerné d'une flèche de boucle
CADRAN_C, CADRAN_R = (440, 508), 62
CADRAN_S21 = (440, 524)
BOUCLE_R = 80
ROUTINE_TXT = (540, 528)                   # « tous les 6 mois » ancré à la pointe de la flèche de boucle
CADRE_C, CADRE_W, CADRE_H = (490, 812), 876, 892       # S19-S21 : cadre du montage (x 52-928, y 366-1258) : x < 940
CADRAN_TXT = (524, 508)                    # « 6 mois » / « tous les 6 mois » à droite du cadran (ancre start)
ETIQUETTE_C = (540, 402)

# Appli testée (bas-centre, à gauche de « Toi » en P2), son câble par la porte, panneau « Espace client »
TESTEE_C, TESTEE_W, TESTEE_H = (610, 1145), 170, 200   # x 525-695, y 1045-1245
TESTEE_SWITCH_DY = 70
TESTEE_SWITCH = (610, 1215)
TESTEE_TOP = (600, 1047)
CABLE_T_A, CABLE_T_B = (515, 864), (600, 1047)          # du tourniquet de la porte au haut de l'appli testée
CABLE_LOOSE = [578, 1004]                  # S18 : bout côté appli débranché, pendu sous la porte
FICHE_C = (534, 905)                       # S18 : fiche cyan du câble, côté porte (sortie du tourniquet)
# Panneau « Espace client » : une fenêtre de la banque, posée DANS sa carte (sur les comptes), deux lignes ON
ESPACE_C, ESPACE_W, ESPACE_H = (795, 812), 270, 160    # x 660-930, y 732-892 (ombre comprise : x < 940)
ESPACE_ROWS = [-6, 44]                                 # « Mon budget », « Appli testée » (repère du panneau)
ESPACE_SWITCH_X, ESPACE_LABEL_X = -100, -62
COUPE_COCHE1 = (497, 1212)                 # S18 : coche de « Toi » après la coupure dans l'appli (à gauche de son
COUPE_COCHE2 = (550, 985)                  # interrupteur), puis à la sortie de la porte, où la fiche a sauté

# Interrupteurs : id -> (rond, course du rond depuis le centre)
SWITCHES = {"interrupteur": ("interrupteur_rond", (SWITCH_W - SWITCH_H) / 2),
            "testee_inter": ("testee_rond", 20), "espace_inter1": ("espace_rond1", 14),
            "espace_inter2": ("espace_rond2", 14)}

N_PERLES = 3                               # pastilles de données, réutilisées d'une scène à l'autre
PERLE_R = 16


def scene_f0(S, sid):
    """Première image de la scène sid (round(t_start x 30))."""
    return round(next(s for s in S.sb["scenes"] if s["id"] == sid)["t_start"] * S.fps)


# ---------- aides de mouvement communes ----------

def wire_point(S, wid, frac, n):
    """Point monde à la fraction `frac` de la longueur du fil `wid` à l'image n, piste `via` comprise (copie de
    timeline.ts wirePath : S-cubique de A à via, puis segment droit via -> B). Fils sans ancres : pistes pa / pb."""
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


def t_at_x(S, wid, x, n):
    """Fraction du fil `wid` (monotone en x, croissant de pa vers pb) dont le point a l'abscisse x."""
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if wire_point(S, wid, mid, n)[0] < x:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def along(S, id, wid, f, d, t0=0.0, t1=1.0, at=None, e="linear"):
    """L'entité `id` glisse le long du fil `wid` (via compris) de la fraction t0 à t1, en d images. -> f + d."""
    at = f if at is None else at
    S.path(id, f, d, e, lambda p: wire_point(S, wid, t0 + (t1 - t0) * p, at))
    return f + d


def polyline_at(pts):
    """Point à la fraction p de la longueur d'une polyligne (points monde)."""
    acc = [0.0]
    for a, b in zip(pts, pts[1:]):
        acc.append(acc[-1] + math.dist(a, b))

    def at(p):
        s = max(0.0, min(1.0, p)) * acc[-1]
        i = next((j for j in range(1, len(acc)) if acc[j] >= s - 1e-9), len(acc) - 1)
        t = (s - acc[i - 1]) / max(1e-9, acc[i] - acc[i - 1])
        return [pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * t, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * t]
    return at


def perle_in(S, id, f, pt):
    """La pastille `id` naît en `pt` (monde) à l'image f : posée à l'échelle 0 en f - 1, grandit en 4 images."""
    S.key(id, "pos", f - 1, [round(c, 3) for c in pt])
    S.key(id, "scale", f - 1, 0)
    S.key(id, "opacity", f, 1)
    S.key(id, "scale", f, 1, 4, "out")


def perle_route(S, id, f, d, route):
    """La pastille `id` naît au premier point de `route` et la parcourt à vitesse constante en d images. -> f + d."""
    perle_in(S, id, f, route[0])
    S.path(id, f, d, "linear", polyline_at(route))
    return f + d


def cable_route(S, n, t0=1.0, t1=0.0, k=32):
    """Points du câble principal de la fraction t0 à t1 (via compris) à l'image n."""
    return [wire_point(S, "cable", t0 + (t1 - t0) * i / k, n) for i in range(k + 1)]


def press(S, f, depth=BOUTON_SHADOW, d_in=3, d_out=4):
    """Le bouton s'enfonce dans son ombre (`depth` px vers le bas-droite) puis remonte ; l'ombre (enfant) reste en
    place. -> f + d_in + d_out."""
    p = S.val("bouton", "pos", f - 1)
    S.key("bouton", "pos", f, [p[0] + depth, p[1] + depth], d_in, "out")
    S.key("bouton_ombre", "pos", f, [BOUTON_SHADOW - depth, BOUTON_SHADOW - depth], d_in, "out")
    S.key("bouton", "pos", f + d_in, list(p), d_out, "inOut")
    S.key("bouton_ombre", "pos", f + d_in, [BOUTON_SHADOW, BOUTON_SHADOW], d_out, "inOut")
    return f + d_in + d_out


def toggle(S, sw, f, on, d=6):
    """Bascule l'interrupteur `sw` : le rond glisse (droite = ON), la piste passe au cyan (ON) ou au papier (OFF)."""
    knob, travel = SWITCHES[sw]
    S.key(knob, "pos", f, [travel if on else -travel, 0], d, "out")
    S.key(sw, "fill", f, CYAN if on else PAPER, d, "out")
    return f + d


def vanish(kit, id, f, into=None, d=POP):
    """kit.vanish, plus un fondu d'opacité sur ses 3 dernières images : pas de point résiduel à taille téléphone."""
    end = kit.vanish(id, f, into=into, d=d)
    kit.S.key(id, "opacity", end - 3, 0, 3, "linear")
    return end


def ring(S, id, f, d=8, s0=0.8, s1=1.35):
    """Anneau qui s'élargit et s'efface (le « ping » d'un objet qui compte). -> f + d."""
    S.key(id, "scale", f - 1, s0)
    S.key(id, "opacity", f - 1, 0)
    S.key(id, "opacity", f, 1)
    S.key(id, "scale", f, s1, d, "out")
    S.key(id, "opacity", f + 2, 0, d - 2, "linear")
    return f + d


def bulle_ronds(head_c, corner, radii=BULLE_RONDS_R, head_r=35):
    """Places des 3 petits ronds de pensée, de la tête (centre head_c) vers le coin `corner` de la bulle."""
    hx, hy = head_c
    vx, vy = corner[0] - hx, corner[1] - hy
    L = math.hypot(vx, vy)
    ux, uy = vx / L, vy / L
    start, end = head_r + 4, L - 4
    return [[round(hx + ux * (start + (end - start) * (0.12 + 0.36 * k)), 1),
             round(hy + uy * (start + (end - start) * (0.12 + 0.36 * k)), 1)] for k in range(len(radii))]


def star_pts(r_out=8.0, r_in=3.4):
    """Étoile à 5 branches (pointe en haut), centrée sur l'origine."""
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        r = r_out if k % 2 == 0 else r_in
        pts.append([round(r * math.cos(a), 2), round(r * math.sin(a), 2)])
    return pts


# ---------- raccords : état épinglé au début de p2 (image 922) et de p3 (image 1801) ----------
_PERLES_OFF = {f"perle{i + 1}": {"scale": 0} for i in range(N_PERLES)}
_CONNEXION = {   # le montage établi en S05-S07, inchangé jusqu'à la carte de fin
    "appli": {"pos": list(PHONE_C), "scale": 1, "opacity": 1},
    "bouton": {"pos": list(BOUTON_C), "scale": 1, "opacity": 1},
    "bouton_ombre": {"pos": [BOUTON_SHADOW, BOUTON_SHADOW]},
    "interrupteur": {"pos": list(SWITCH_C), "scale": 1, "fill": CYAN.lower()},
    "interrupteur_rond": {"pos": [SWITCHES["interrupteur"][1], 0]},
    "cable": {"draw": 1, "from": 0, "via": list(PORTE_VIA), "pa": list(CABLE_A), "pb": list(CABLE_B), "sag": 0},
    "porte": {"pos": list(PORTE_C), "scale": 1, "opacity": 1},
    "porte_dsp2": {"pos": list(PORTE_DSP2_C), "scale": 1, "opacity": 1},
    "porte_ue": {"pos": list(PORTE_UE_C), "scale": 1, "opacity": 1},
    "banque": {"pos": list(BANK_C), "scale": 1, "opacity": 1},
    "cle": {"pos": list(CLE_HOME), "scale": 1, "rot": 0, "opacity": 1},
    **{f"releve{k + 1}": {"scale": 1} for k in range(3)},
    "directive": {"scale": 0}, "open_banking": {"scale": 0}, "cadenas": {"scale": 0}, "mur": {"scale": 0},
    "barriere": {"scale": 0}, "question": {"scale": 0}, "carte_id": {"scale": 0}, "mur_bas": {"scale": 0},
    **{f"alerte{i + 1}": {"scale": 0} for i in range(3)},
    **_PERLES_OFF,
}
ENTRY_P2 = {   # fin de S07 = etat_initial de S08 : clé rangée dans la banque, repère sans étape active
    **_CONNEXION,
    "marqueur": {"pos": [CX, MARKER_Y], "scale": 1, "active": 0, "on": 0},
    "cle_coche": {"draw": 0},
    "bulle": {"scale": 0}, **{f"bulle_rond{i + 1}": {"scale": 0} for i in range(3)},
    "douteuse": {"scale": 0}, "douteuse_fil1": {"draw": 0}, "douteuse_fil2": {"draw": 0},
    "douteuse_pince": {"scale": 0}, "bulle_barre": {"draw": 0},
    "badge": {"scale": 0}, "badge_case": {"scale": 0}, "question2": {"scale": 0}, "registre": {"scale": 0},
    "champ": {"scale": 0},
    "gratuit": {"scale": 0}, "preuve": {"draw": 0}, "attache": {"draw": 0}, "attache_pleine": {"draw": 0},
}
ENTRY_P3 = {   # fin de S14 = etat_initial de S15 : société trouvée au registre, badge plein coché relié par le fil
    **_CONNEXION,
    "marqueur": {"pos": [CX, MARKER_Y], "scale": 1, "active": 1, "on": 1, "done0": 1, "done1": 0, "done2": 0},
    "cle_coche": {"draw": 1},
    "bulle": {"scale": 0}, **{f"bulle_rond{i + 1}": {"scale": 0} for i in range(3)},
    "douteuse": {"scale": 0}, "douteuse_fil1": {"draw": 0}, "douteuse_fil2": {"draw": 0},
    "douteuse_pince": {"scale": 0}, "bulle_barre": {"opacity": 0},
    "badge": {"pos": list(BADGE_ON_SOC), "scale": 1, "opacity": 1}, "badge_case": {"scale": 0},
    "badge_plein": {"draw": 1}, "badge_nom": {"chars": len("Société X")}, "badge_coche": {"draw": 1},
    "question2": {"scale": 0},
    "registre": {"pos": list(REGISTRE_C), "scale": 1, "opacity": 1},
    "registre_nom": {"chars": len("Société X"), "mark": 1}, "registre_coche": {"draw": 1},
    "registre_titre": {"chars": len("REGAFI")},
    "registre_acpr": {"scale": 1},
    "champ": {"scale": 0}, "gratuit": {"scale": 0},
    "preuve": {"draw": 1}, "attache": {"draw": 1}, "attache_pleine": {"draw": 1},
    "cadran": {"scale": 0, "value": 0}, "testee": {"scale": 0}, "cable_testee": {"draw": 0},
    "espace_client": {"scale": 0}, "fiche": {"scale": 0}, "testee_veille": {"scale": 0},
    "coupe_coche1": {"draw": 0}, "coupe_coche2": {"draw": 0},
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


def key_glyph(kit, prefix, parent, pos, k=1.0, color=DEEP, z=7, dash=None, sw=None):
    """Clé plate (anneau, tige, deux dents), ~70 x 30 px à k = 1, centrée sur `pos` (repère du parent). Pleine
    (cyan profond, sur la capsule) ou en tirets (`dash` : la clé fantôme de la bulle). Renvoie l'id du groupe."""
    g = f"{prefix}"
    kit.shape(g, list(pos), kind="circle", w=2, fill="none", stroke="none", sw=0, shadow=0, z=z, parent=parent)
    lw = sw if sw is not None else 6 * k
    fill = "none" if dash else color
    kit.shape(f"{g}_anneau", [-24 * k, 0], kind="circle", w=26 * k, fill="none", stroke=color, sw=lw, shadow=0,
              z=z + 0.01, parent=g, **({"dash": dash} if dash else {}))
    kit.shape(f"{g}_tige", [10 * k, 0], kind="rect", w=44 * k, h=8 * k, fill=fill, stroke=color,
              sw=(lw * 0.5 if dash else 0), shadow=0, z=z + 0.01, parent=g, **({"dash": dash} if dash else {}))
    for j, x in enumerate((20, 30)):
        kit.shape(f"{g}_dent{j + 1}", [x * k, 8 * k], kind="rect", w=6 * k, h=10 * k, fill=fill, stroke=color,
                  sw=(lw * 0.5 if dash else 0), shadow=0, z=z + 0.01, parent=g, **({"dash": dash} if dash else {}))
    return g


def cast(S, kit):
    """Toute la distribution, à son état de l'image 0 : S01 montre le téléphone « Mon budget » et son bouton cyan,
    « Toi » en P1. Ce qui arrive plus tard est déclaré à sa première place avec scale=0 (figurines : show=False)."""

    # --- repère 1-2-3 légendé (S03 -> S22) : sans étape active jusqu'à « Première » (S08) ---
    kit.steps_marker(MARKER_LABELS, id="marqueur", y=MARKER_Y, cx=CX, gap=MARKER_GAP, z=20)
    S.ents["marqueur"]["p"].update(labelSize=MARKER_LABEL, labelDy=MARKER_DY, moveBlank=True)
    S.set("marqueur", scale=0, on=0, done0=0, done1=0, done2=0)

    # --- téléphone « Mon budget », lignes de relevé de l'écran, bouton (objet du fil), interrupteur « Accès » ---
    kit.shape("appli", PHONE_C, kind="round", w=PHONE_W, h=PHONE_H, r=PHONE_R, fill=PAPER, stroke=INK, sw=5,
              shadow=6, z=4)
    kit.text("appli_titre", [0, PHONE_TITLE_DY], "Mon budget", size=32, weight=600, z=4.1, parent="appli")
    kit.shape("appli_filet", [0, PHONE_RULE_DY], kind="rect", w=PHONE_W - 40, h=3, fill=RULE, stroke=RULE, sw=0,
              shadow=0, z=4.1, parent="appli")
    for k, dy in enumerate(RELEVE_DY):
        rid = f"releve{k + 1}"
        kit.shape(rid, [0, dy], kind="round", w=RELEVE_W, h=RELEVE_H, r=9, fill=LIGHT, stroke=INK, sw=3, shadow=0,
                  z=4.2, parent="appli", scale=0)
        kit.icon(f"{rid}_ic", [-RELEVE_W / 2 + 20, 0], "bars", s=22, z=4.3, parent=rid)
        kit.shape(f"{rid}_trait", [18, 0], kind="round", w=120 - 26 * k, h=8, r=4, fill=INK, stroke=INK, sw=0,
                  shadow=0, z=4.3, parent=rid)
    kit.shape("bouton", BOUTON_C, kind="round", w=BOUTON_W, h=BOUTON_H, r=30, fill=CYAN, stroke=INK, sw=4, shadow=0,
              z=6)
    kit.text("bouton_txt", [0, 0], BOUTON_TEXT, size=BOUTON_SIZE, weight=700, lh=1.05, z=6.1, parent="bouton")
    kit.shape("bouton_ombre", [BOUTON_SHADOW, BOUTON_SHADOW], kind="round", w=BOUTON_W, h=BOUTON_H, r=30, fill=INK,
              stroke=INK, sw=4, shadow=0, z=5.9, parent="bouton")
    _switch(kit, "interrupteur", SWITCH_C, SWITCH_W, SWITCH_H, 36, on=False, z=6.2, scale=0)
    kit.text("interrupteur_txt", [SWITCH_LABEL_X, 0], "Accès", size=32, weight=600, anchor="end", z=6.3,
             parent="interrupteur")

    # --- la banque : carte, disque cyan au temple, « Ta banque », deux barres de comptes (et leurs copies) ---
    kit.shape("banque", BANK_C, kind="round", w=BANK_W, h=BANK_H, r=30, fill=PAPER, stroke=INK, sw=5, shadow=6, z=4,
              scale=0)
    kit.icon("banque_icone", [0, BANK_ICON_DY], "bank", disc=34, fill=CYAN, z=4.1, parent="banque")
    kit.text("banque_titre", [0, BANK_TITLE_DY], "Ta banque", size=32, weight=700, z=4.1, parent="banque")
    for k, dy in enumerate(COMPTES_DY):
        cid = f"compte{k + 1}"
        kit.shape(cid, [0, dy], kind="round", w=COMPTE_W, h=COMPTE_H, r=10, fill=LIGHT, stroke=INK, sw=3, shadow=0,
                  z=4.2, parent="banque")
        kit.icon(f"{cid}_euro", [-COMPTE_W / 2 + 22, 0], "euro", s=24, z=4.3, parent=cid)
        # copie en tirets qui se détache de la barre (S02 : des données COPIÉES, la barre reste pleine)
        kit.shape(f"{cid}_copie", [0, dy], kind="round", w=COMPTE_W, h=COMPTE_H, r=10, fill="none", stroke=DEEP,
                  sw=3, dash=[8, 6], shadow=0, z=4.4, parent="banque", scale=0)

    # --- le câble de la connexion (pa / pb : extrémités monde ; via sur la droite tant qu'il n'y a pas de porte) ---
    S.add("cable", "wire", z=3, color=DEEP, sw=8, dots=True, tension=0.45)
    S.set("cable", pa=list(CABLE_A), pb=list(CABLE_B), via=list(CABLE_VIA_FLAT), sag=0, draw=0, opacity=1,
          color=DEEP)
    S.set("cable", **{"from": 0})

    # --- pastilles de données (pictogramme « lignes de relevé », jamais euro), réutilisées ---
    for i in range(N_PERLES):
        S.add(f"perle{i + 1}", "bullet", z=13, icon="bars", r=PERLE_R)
        S.set(f"perle{i + 1}", pos=list(BANK_C), scale=0, opacity=1)

    # --- le « ? » (S02-S03) et les trois alertes (S03 ; S19-S21, avec numéros, guides et coches) ---
    S.add("question", "qmark", z=12)
    S.set("question", pos=list(BOUTON_C), scale=0, opacity=1, gs=110)
    for i in range(3):
        a = f"alerte{i + 1}"
        S.add(f"guide{i + 1}", "wire", z=17.5, color=INK, sw=3, dash=[9, 7], tension=0)
        S.set(f"guide{i + 1}", pa=[MARKER_XS[i], MARKER_Y], pb=[MARKER_XS[i], MARKER_Y], sag=0, draw=0, opacity=1)
        kit.icon(a, ALERTES_CABLE[i], "warning", disc=ALERTE_R, fill=PAPER, shadow=4, z=18, scale=0)
        kit.text(f"{a}_num", [ALERTE_R + 14, -ALERTE_R + 8], str(i + 1), size=ALERTE_NUM, weight=800, z=18.1,
                 parent=a, opacity=0)
        kit.shape(f"{a}_ok", ALERTES_CABLE[i], kind="circle", w=2 * ALERTE_R, fill=PAPER, stroke=INK, sw=4, shadow=4,
                  z=18, scale=0)
        kit.tick(f"{a}_ok_coche", [0, 0], DEEP, size=40, sw=8, z=18.1, parent=f"{a}_ok", draw=0)

    # --- étiquette « open banking » (S04-S05) ---
    S.add("open_banking", "pill", z=9, text="open banking", w=round(text_width("open banking", 32, 700) + 40), h=60,
          size=32, weight=700, fill=LIGHT)
    S.set("open_banking", pos=list(OPEN_BANKING_C), scale=0, opacity=1)

    # --- la directive DSP2 (S05) : carte, couronne de 12 étoiles, « Directive / européenne », « DSP2 » souligné ---
    kit.shape("directive", DIRECTIVE_C, kind="round", w=DIRECTIVE_W, h=DIRECTIVE_H, r=18, fill=PAPER, stroke=INK,
              sw=4, shadow=6, z=9, scale=0)
    for k in range(12):
        a = -math.pi / 2 + k * math.pi / 6
        kit.shape(f"etoile{k + 1}", [round(DIRECTIVE_CROWN[0] + DIRECTIVE_CROWN_R * math.cos(a), 1),
                                     round(DIRECTIVE_CROWN[1] + DIRECTIVE_CROWN_R * math.sin(a), 1)],
                  kind="poly", pts=star_pts(7.4, 3.1), fill=INK, stroke=INK, sw=0, shadow=0, z=9.1,
                  parent="directive")
    kit.text("directive_txt", [0, DIRECTIVE_TEXT_Y], "Directive\neuropéenne", size=32, weight=600, lh=1.05, z=9.1,
             parent="directive")
    kit.text("directive_dsp2", list(DIRECTIVE_DSP2), "DSP2", size=46, weight=800, z=9.1, parent="directive")
    dsp2_w = text_width("DSP2", 46, 800)
    kit.shape("directive_trait", [DIRECTIVE_DSP2[0] - dsp2_w / 2, DIRECTIVE_DSP2[1] + 30], kind="round", w=0, h=9,
              r=4.5, fill=DEEP, stroke=DEEP, sw=0, shadow=0, z=9.2, parent="directive")
    S.set("directive_trait", w=0)

    # --- la porte officielle (PNG WTH-002-02), sa pilule « DSP2 », la barrière tant que l'accès est OFF ---
    gate = S.png("WTH-002-02")
    porte_h = round(PORTE_W * gate["h"] / gate["w"])
    S.add("porte", "png", z=7, src=gate["src"], w=PORTE_W, h=porte_h, saturate=0.85,   # verre un peu calmé
          contact=dict(w=round(PORTE_W * 0.62), h=16, dy=2, blur=5, alpha=0.22))      # ombre de contact serrée
    S.set("porte", pos=list(PORTE_C), scale=0, opacity=1, rot=0)
    S.add("porte_dsp2", "pill", z=7.5, text="DSP2", w=round(text_width("DSP2", 32, 700) + 40), h=52, size=32,
          weight=700, fill=LIGHT)
    S.set("porte_dsp2", pos=list(PORTE_DSP2_C), scale=0, opacity=1)
    kit.shape("barriere", BARRIERE_C, kind="round", w=BARRIERE_W, h=BARRIERE_H, r=BARRIERE_W / 2, fill=INK,
              stroke=INK, sw=0, shadow=3, z=7.6, scale=0)
    kit.shape("porte_ue", PORTE_UE_C, kind="circle", w=2 * PORTE_UE_R + 26, fill=PAPER, stroke=INK, sw=3, shadow=3,
              z=7.55, scale=0)
    for k in range(12):
        a = -math.pi / 2 + k * math.pi / 6
        kit.shape(f"porte_ue{k + 1}", [round(PORTE_UE_R * math.cos(a), 1), round(PORTE_UE_R * math.sin(a), 1)],
                  kind="poly", pts=star_pts(6.0, 2.6), fill=INK, stroke=INK, sw=0, shadow=0, z=7.56, parent="porte_ue")
    kit.shape("inter_anneau", INTER_RING, kind="ellipse", w=150, h=86, fill="none", stroke=DEEP, sw=6, shadow=0,
              z=6.25, opacity=0)

    # --- le mur fermé de la banque et son cadenas (S06-S07 ; reparaît en S10) ---
    kit.shape("mur", MUR_C, kind="round", w=14, h=MUR_H, r=7, fill=INK, stroke=INK, sw=0, shadow=0, z=7.9, scale=0)
    kit.icon("cadenas", CADENAS_C, "lock", disc=32, fill=PAPER, shadow=4, z=8, scale=0)
    kit.shape("mur_bas", MUR_BAS_C, kind="round", w=14, h=MUR_BAS_H, r=7, fill=INK, stroke=INK, sw=0, shadow=0,
              z=7.9, scale=0)

    # --- la carte d'identifiants (S07) puis la clé (PNG WTH-002-03 + clé plate), son anneau et sa coche ---
    kit.shape("carte_id", CARTE_ID_C, kind="round", w=240, h=110, r=16, fill=PAPER, stroke=INK, sw=4, shadow=6,
              z=13, scale=0)
    kit.text("carte_id_txt", [0, -22], "Identifiant", size=32, weight=600, z=13.1, parent="carte_id")
    kit.text("carte_id_mdp", [0, 24], "••••••", size=34, weight=700, z=13.1, parent="carte_id")
    key = S.png("WTH-002-03")
    cle_h = round(CLE_W * key["h"] / key["w"])
    S.add("cle", "png", z=6.5, src=key["src"], w=CLE_W, h=cle_h,
          contact=dict(w=round(CLE_W * 0.7), h=16, dy=2, blur=8, alpha=0.18))
    S.set("cle", pos=list(CARTE_ID_C), scale=0, opacity=1, rot=0)
    key_glyph(kit, "cle_plate", "cle", [-4, 2], k=1.0, color=DEEP, z=6.6)
    kit.tick("cle_coche", CLE_TICK, DEEP, size=40, sw=8, z=6.7, draw=0)
    kit.shape("cle_anneau", CLE_HOME, kind="ellipse", w=180, h=110, fill="none", stroke=DEEP, sw=6, shadow=0, z=6.8,
              opacity=0)

    # --- la bulle de pensée (S08-S09, S19-S20) : un mini « Mon budget » dont l'écran montre une clé fantôme en
    #     tirets, étiquetée « Mot de passe » (pas de flèche : la clé est DANS l'appli, c'est la croyance) ---
    kit.shape("bulle", BULLE_C, kind="round", w=BULLE_W, h=BULLE_H, r=44, fill=PAPER, stroke=INK, sw=4,
              dash=[14, 10], shadow=0, z=17, scale=0)
    kit.shape("bulle_tel", [0, 0], kind="round", w=BULLE_TEL_W, h=BULLE_TEL_H, r=26, fill=PAPER, stroke=INK, sw=4,
              shadow=3, z=17.1, parent="bulle", scale=0)
    kit.text("bulle_tel_titre", [0, -82], "Mon budget", size=32, weight=600, z=17.2, parent="bulle_tel")
    kit.shape("bulle_tel_filet", [0, -58], kind="rect", w=BULLE_TEL_W - 36, h=3, fill=RULE, stroke=RULE, sw=0,
              shadow=0, z=17.2, parent="bulle_tel")
    kit.shape("bulle_tel_bouton", [0, 84], kind="round", w=130, h=26, r=13, fill=CYAN, stroke=INK, sw=3, shadow=0,
              z=17.2, parent="bulle_tel")
    key_glyph(kit, "bulle_cle", "bulle_tel", list(GHOST_KEY), k=1.8, color=INK, z=17.3, dash=[8, 6], sw=5)
    kit.text("bulle_txt", [0, 40], "Mot de passe", size=32, weight=600, z=17.3, parent="bulle_tel", typed=True)
    for k in range(3):
        kit.shape(f"bulle_rond{k + 1}", BULLE_C, kind="circle", w=2 * BULLE_RONDS_R[k], fill=PAPER, stroke=INK,
                  sw=3, dash=[5, 4], shadow=0, z=17, scale=0)
    S.add("bulle_barre", "wire", z=17.6, color=INK, sw=7, tension=0)       # S09 : le stylo barre la clé fantôme
    S.set("bulle_barre", pa=list(BULLE_C), pb=list(BULLE_C), sag=0, draw=0, opacity=1)
    S.add("bulle_guide", "wire", z=16.5, color=INK, sw=4, dash=[10, 8], tension=0)    # clé fantôme -> vraie clé
    S.set("bulle_guide", pa=list(BULLE_C), pb=list(CLE_HOME), sag=0, draw=0, opacity=1)

    # --- l'appli qui réclame les codes (S10-S11) : en-tête encre et crochet, contour épais ; texte en hex (rouge) ---
    kit.shape("douteuse", DOUTEUSE_C, kind="round", w=DOUTEUSE_W, h=DOUTEUSE_H, r=26, fill=PAPER, stroke=INK, sw=7,
              shadow=6, z=10, scale=0)
    S.set("douteuse", stroke=INK)
    kit.shape("douteuse_tete", [0, -DOUTEUSE_H / 2 + 24], kind="round", w=DOUTEUSE_W - 8, h=44, r=20, fill=INK,
              stroke=INK, sw=0, shadow=0, z=10.05, parent="douteuse")
    S.set("douteuse_tete", fill=INK)             # hex : l'en-tête vire au rouge en fondu après le geste (S10)
    # loup de voleur (bandeau papier, deux yeux encre) : impossible à lire comme une lettre
    kit.shape("douteuse_loup", [0, -DOUTEUSE_H / 2 + 24], kind="round", w=86, h=30, r=15, fill=PAPER, stroke=PAPER,
              sw=0, shadow=0, z=10.1, parent="douteuse")
    for k, dx in enumerate((-20, 20)):
        kit.shape(f"douteuse_oeil{k + 1}", [dx, 1], kind="ellipse", w=24, h=12, fill=INK, stroke=INK, sw=0,
                  shadow=0, z=10.12, parent="douteuse_loup")
    kit.text("douteuse_txt", [0, -6], "Tes codes ?", size=32, weight=700, z=10.1, parent="douteuse", typed=True)
    S.set("douteuse_txt", color=INK)
    kit.shape("douteuse_champ", [0, 46], kind="round", w=160, h=44, r=10, fill=PAPER, stroke=INK, sw=3, shadow=0,
              z=10.1, parent="douteuse", scale=0)
    kit.shape("douteuse_curseur", [-60, 0], kind="rect", w=3, h=26, fill=INK, stroke=INK, sw=0, shadow=0, z=10.2,
              parent="douteuse_champ")
    for k, (a, b) in enumerate(((DOUTEUSE_FIL_A, DOUTEUSE_FIL_MID), (DOUTEUSE_FIL_MID, DOUTEUSE_FIL_B))):
        wid = f"douteuse_fil{k + 1}"   # deux moitiés d'un même fil (tension 0) : il se sépare au trait du stylo
        S.add(wid, "wire", z=9.5, color=INK, sw=7, dash=[18, 11], tension=0)
        S.set(wid, pa=list(a), pb=list(b), sag=0, draw=0, opacity=1, color=INK)
    # pince ouverte au bout du fil, tournée vers la clé (repère : la pointe du fil, axe = direction du fil)
    kit.shape("douteuse_pince", list(DOUTEUSE_FIL_B), kind="circle", w=2, fill="none", stroke="none", sw=0, shadow=0,
              z=9.6, scale=0, rot=round(math.degrees(math.atan2(DOUTEUSE_FIL_B[1] - DOUTEUSE_FIL_MID[1],
                                                                 DOUTEUSE_FIL_B[0] - DOUTEUSE_FIL_MID[0])), 2))
    for k, sy in enumerate((-1, 1)):
        kit.shape(f"douteuse_machoire{k + 1}", [0, 0], kind="poly", pts=[[-6, 0], [6, 7 * sy], [18, 13 * sy]],
                  closed=False, fill="none", stroke=INK, sw=6, shadow=0, z=9.61, parent="douteuse_pince")
    S.add("coupure", "burst", z=16, r0=12, r1=58, n=10, sw=7, color=INK)             # éclair au point de coupe
    S.set("coupure", pos=list(DOUTEUSE_FIL_MID), p=0)

    # --- la société derrière l'appli (figurine papier, sans outil), son badge, l'attache vers le téléphone ---
    # tour de bureaux derrière la figurine (enfant, calque 2,9 sous la figurine et le téléphone) : une entreprise,
    # pas un temple (le temple est l'icône de la banque) ; contrôle sans son : « on peut le prendre pour une deuxième
    # banque »
    societe = Figure(kit, "societe", pos=list(SOC_HIDDEN), scale=SOC_SCALE, variant="paper", tool=False, z=3,
                     show=False)
    kit.shape("soc_tour", [0, TOUR_CY], kind="round", w=TOUR_W, h=TOUR_H, r=8, fill=PAPER, stroke=INK, sw=5,
              shadow=6, z=2.9, parent="societe")
    for k, (wx, wy) in enumerate(TOUR_WINDOWS):
        kit.shape(f"soc_fenetre{k + 1}", [wx, wy], kind="rect", w=20, h=22, fill=LIGHT, stroke=INK, sw=3, shadow=0,
                  z=2.95, parent="soc_tour")
    kit.shape("badge", BADGE_ON_SOC, kind="circle", w=2, fill="none", stroke="none", sw=0, shadow=0, z=16, scale=0)
    kit.shape("badge_fond", [0, 0], kind="round", w=BADGE_W, h=BADGE_H, r=BADGE_H / 2, fill=PAPER, stroke=INK, sw=4,
              dash=[12, 8], shadow=0, z=16, parent="badge")
    kit.shape("badge_plein", [0, 0], kind="round", w=BADGE_W, h=BADGE_H, r=BADGE_H / 2, fill="none", stroke=DEEP,
              sw=5, shadow=0, z=16.1, parent="badge", draw=0)
    # mini tour de bureaux (même dessin que la tour de la société), pas le temple de la banque
    kit.shape("badge_icone", [-BADGE_W / 2 + 32, -1], kind="round", w=26, h=38, r=3, fill=PAPER, stroke=INK, sw=3.5,
              shadow=0, z=16.2, parent="badge")
    for k, (wx, wy) in enumerate([(-5, -10), (5, -10), (-5, 0), (5, 0), (-5, 10), (5, 10)]):
        kit.shape(f"badge_fenetre{k + 1}", [wx, wy], kind="rect", w=5, h=5, fill=INK, stroke=INK, sw=0, shadow=0,
                  z=16.25, parent="badge_icone")
    kit.text("badge_nom", [2, 0], "Société X", size=32, weight=700, z=16.2, parent="badge", typed=True)
    kit.shape("badge_case", [BADGE_CASE_X, 0], kind="round", w=30, h=30, r=6, fill=PAPER, stroke=INK, sw=3,
              dash=[6, 4], shadow=0, z=16.2, parent="badge", scale=0)     # case vide : nommée, pas vérifiée
    kit.tick("badge_coche", [BADGE_CASE_X, 0], DEEP, size=30, sw=7, z=16.25, parent="badge", draw=0)
    for wid, col, dash, z in (("attache", INK, [9, 7], 15.6), ("attache_pleine", DEEP, None, 15.7)):
        S.add(wid, "wire", z=z, color=col, sw=4 if dash else 5, tension=0.3,
              a={"id": "appli", "at": [-110, PHONE_H / 2 + 2]},
              b={"id": "badge", "at": [-BADGE_W / 2 + 24, -BADGE_H / 2]}, **({"dash": dash} if dash else {}))
        S.set(wid, sag=0, draw=0, opacity=1)
    S.add("question2", "qmark", z=17)
    S.set("question2", pos=list(QUESTION2_C), scale=0, opacity=1, gs=90)

    # --- le registre REGAFI (PNG BOOK) : sceau de l'autorité, « REGAFI », « ACPR », inscriptions ; champ, « gratuit » ---
    book = S.png("BOOK")
    book_h = round(REGISTRE_W * book["h"] / book["w"])
    S.add("registre", "png", z=11, src=book["src"], w=REGISTRE_W, h=book_h,
          contact=dict(w=round(REGISTRE_W * 0.8), h=22, dy=4, blur=10, alpha=0.18))
    S.set("registre", pos=list(REGISTRE_C), scale=0, opacity=1)
    kit.shape("registre_sceau", list(REG_SEAL), kind="circle", w=64, fill=PAPER, stroke=INK, sw=4, shadow=3,
              z=11.2, parent="registre")
    for k in range(12):
        a = -math.pi / 2 + k * math.pi / 6
        kit.shape(f"sceau_etoile{k + 1}", [round(22 * math.cos(a), 1), round(22 * math.sin(a), 1)], kind="poly",
                  pts=star_pts(3.6, 1.5), fill=INK, stroke=INK, sw=0, shadow=0, z=11.3, parent="registre_sceau")
    kit.shape("sceau_colonne", [0, 0], kind="rect", w=8, h=18, fill=INK, stroke=INK, sw=0, shadow=0, z=11.3,
              parent="registre_sceau")
    kit.shape("sceau_chapiteau", [0, -10], kind="rect", w=16, h=4, fill=INK, stroke=INK, sw=0, shadow=0, z=11.3,
              parent="registre_sceau")
    kit.shape("sceau_socle", [0, 10], kind="rect", w=16, h=4, fill=INK, stroke=INK, sw=0, shadow=0, z=11.3,
              parent="registre_sceau")
    S.add("registre_acpr", "pill", z=11.4, parent="registre", text="ACPR", w=round(text_width("ACPR", 32, 800) + 32),
          h=50, size=32, weight=800, fill=PAPER, stroke=DEEP, color=DEEP, shadow=4)
    S.set("registre_acpr", pos=list(REG_ACPR), scale=0, opacity=1, rot=REG_PAGE_ROT)
    kit.shape("registre_page", list(REG_SHEET), kind="round", w=REG_SHEET_W, h=REG_SHEET_H, r=8, fill=PAPER,
              stroke=INK, sw=3, shadow=3, z=11.1, parent="registre", rot=REG_PAGE_ROT)
    kit.shape("registre_bandeau", list(REG_BANDEAU), kind="round", w=170, h=46, r=10, fill=PAPER, stroke=INK, sw=3,
              shadow=3, z=11.3, parent="registre")
    kit.text("registre_titre", [0, 0], "REGAFI", size=32, weight=800, z=11.35, parent="registre_bandeau",
             typed=True)
    for k, dy in enumerate(REG_ROWS):
        kit.icon(f"registre_tel{k + 1}", [REG_PHONE_X, dy], "phone", s=34, z=11.15, parent="registre_page",
                 scale=0)
        kit.shape(f"registre_trait{k + 1}", [REG_TRAIT_X, dy], kind="round", w=70, h=8, r=4, fill=INK, stroke=INK,
                  sw=0, shadow=0, z=11.15, parent="registre_page", draw=0)
    kit.text("registre_nom", [REG_NAME_X, REG_ROWS[1]], "Société X", size=30, weight=700, anchor="start", z=11.25,
             parent="registre_page", typed=True, markColor=LIGHT)
    S.set("registre_nom", mark=0)
    kit.tick("registre_coche", [REG_TICK_X, REG_ROWS[1]], DEEP, size=28, sw=7, z=11.3, parent="registre_page",
             draw=0)
    kit.shape("champ", CHAMP_C, kind="round", w=CHAMP_W, h=CHAMP_H, r=12, fill=PAPER, stroke=DEEP, sw=4, shadow=0,
              z=12, scale=0)
    kit.shape("champ_curseur", [-CHAMP_W / 2 + 16, 0], kind="rect", w=3, h=30, fill=INK, stroke=INK, sw=0, shadow=0,
              z=12.2, parent="champ")
    kit.text("champ_nom", [0, 0], "Société X", size=32, weight=700, z=12.1, parent="champ", typed=True)
    S.add("gratuit", "pill", z=12, text="gratuit", w=round(text_width("gratuit", 32, 700) + 36), h=CHAMP_H, size=32,
          weight=700, fill=LIGHT)
    S.set("gratuit", pos=list(GRATUIT_C), scale=0, opacity=1)
    S.add("preuve", "wire", z=15.8, color=DEEP, sw=6, dots=True, tension=0.45)    # sous le badge (z 16)
    S.set("preuve", pa=list(REGISTRE_C), pb=list(BADGE_ON_SOC), sag=0, draw=0, opacity=1)
    S.add("regafi", "pill", z=12, text="REGAFI", w=round(text_width("REGAFI", 32, 800) + 40), h=54, size=32,
          weight=800, fill=PAPER, stroke=DEEP, color=DEEP, shadow=4)
    S.set("regafi", pos=list(REGAFI_PILL_C), scale=0, opacity=1)

    # --- cadran des mois (S15-S17, S21) et ses textes ---
    kit.sector("cadran", CADRAN_C, start=0, value=0, r=CADRAN_R, unit=12, face=PAPER, fill=DEEP, ticks=12, sw=5,
               z=9, scale=0)
    kit.text("cadran_txt", CADRAN_TXT, f"6{NBSP}mois", size=44, weight=800, anchor="start", z=9, scale=0)
    kit.text("cadran_routine", ROUTINE_TXT, f"tous les 6{NBSP}mois", size=34, weight=700, anchor="start", z=9,
             typed=True)
    a0, a1 = 12, 344                                        # flèche de boucle : un tour presque complet, sens horaire
    arc = [[round(BOUCLE_R * math.cos(math.radians(a0 + (a1 - a0) * i / 24)), 1),
            round(BOUCLE_R * math.sin(math.radians(a0 + (a1 - a0) * i / 24)), 1)] for i in range(25)]
    kit.curve("cadran_boucle", CADRAN_S21, arc, draw=0, z=9.1, color=INK, sw=6, smooth=False)
    tip = math.radians(a1)
    ux, uy = -math.sin(tip), math.cos(tip)                  # tangente (sens horaire, y vers le bas)
    nx, ny = math.cos(tip), math.sin(tip)
    hx, hy = BOUCLE_R * math.cos(tip), BOUCLE_R * math.sin(tip)
    kit.shape("cadran_pointe", [round(CADRAN_S21[0] + hx, 1), round(CADRAN_S21[1] + hy, 1)], kind="poly",
              pts=[[round(16 * ux, 1), round(16 * uy, 1)], [round(-6 * ux + 13 * nx, 1), round(-6 * uy + 13 * ny, 1)],
                   [round(-6 * ux - 13 * nx, 1), round(-6 * uy - 13 * ny, 1)]],
              fill=INK, stroke=INK, sw=2, shadow=0, z=9.15, scale=0)

    # --- appli testée (S15-S22), son interrupteur, sa lune, ses relevés ; son câble ; panneau « Espace client » ---
    kit.shape("testee", TESTEE_C, kind="round", w=TESTEE_W, h=TESTEE_H, r=26, fill=PAPER, stroke=INK, sw=5,
              shadow=6, z=10, scale=0)
    S.set("testee", fill=PAPER, stroke=INK)      # hex : le contour plein s'efface quand elle s'endort (S16)
    kit.text("testee_titre", [0, -60], "Appli\ntestée", size=32, weight=600, lh=1.0, z=10.1, parent="testee")
    kit.icon("testee_lune", [-36, 14], "moon", s=62, z=10.1, parent="testee", scale=0)
    for k in range(3):
        kit.shape(f"testee_l{k + 1}", [36, -4 + 15 * k], kind="round", w=56, h=8, r=4, fill=INK, stroke=INK, sw=0,
                  shadow=0, z=10.1, parent="testee", scale=0)
    _switch(kit, "testee_inter", [0, TESTEE_SWITCH_DY], 80, 40, 30, on=False, z=10.2, parent="testee", shadow=3)
    kit.shape("testee_veille", [0, 0], kind="round", w=TESTEE_W + 20, h=TESTEE_H + 20, r=34, fill="none", stroke=INK,
              sw=4, dash=[12, 9], shadow=0, z=10.15, parent="testee", scale=0)   # en veille : contour en tirets
    S.add("cable_testee", "wire", z=3.5, color=DEEP, sw=7, dots=True, tension=0.45)
    S.set("cable_testee", pa=list(CABLE_T_A), pb=list(CABLE_T_B), sag=0, draw=0, opacity=1)
    kit.shape("fiche", FICHE_C, kind="round", w=30, h=20, r=6, fill=CYAN, stroke=INK, sw=3, shadow=2, z=7.8,
              scale=0, rot=65)                                        # fiche du câble, côté porte (S18)
    kit.shape("espace_client", ESPACE_C, kind="round", w=ESPACE_W, h=ESPACE_H, r=18, fill=PAPER, stroke=INK, sw=4,
              shadow=6, z=8, scale=0)
    kit.text("espace_txt", [0, -ESPACE_H / 2 + 28], "Espace client", size=30, weight=700, z=8.1,
             parent="espace_client")
    kit.shape("espace_filet", [0, -ESPACE_H / 2 + 52], kind="rect", w=ESPACE_W - 30, h=3, fill=RULE, stroke=RULE,
              sw=0, shadow=0, z=8.1, parent="espace_client")
    for k, (dy, lab) in enumerate(zip(ESPACE_ROWS, ("Mon budget", "Appli testée"))):
        _switch(kit, f"espace_inter{k + 1}", [ESPACE_SWITCH_X, dy], 60, 32, 24, on=True, z=8.2,
                parent="espace_client", shadow=2)
        kit.text(f"espace_lab{k + 1}", [ESPACE_LABEL_X, dy], lab, size=30, weight=600, anchor="start", z=8.1,
                 parent="espace_client")

    # --- S18 : les deux coupures sont deux gestes faits (coches pleines de « Toi ») ---
    for k, pt in enumerate((COUPE_COCHE1, COUPE_COCHE2)):
        kit.tick(f"coupe_coche{k + 1}", list(pt), DEEP, size=44, sw=9, z=10.4, draw=0)

    # --- S21 : le disque 3 du repère se coche (le disque actif garde son chiffre : pastille posée par-dessus) ---
    kit.shape("marqueur_fait3", [MARKER_XS[2], MARKER_Y], kind="circle", w=2 * GEOM["MARKER"]["r"], fill=PAPER,
              stroke=INK, sw=4, shadow=0, z=20.6, scale=0)
    kit.tick("marqueur_fait3_coche", [0, 1], DEEP, size=26, sw=6, z=20.7, parent="marqueur_fait3", draw=0)

    # --- S19-S21 : cadre du montage (en tirets = avant, plein = maintenant) et barre de rembobinage ---
    for cid, dash in (("cadre_avant", [18, 12]), ("cadre_plein", None)):
        kit.shape(cid, CADRE_C, kind="round", w=CADRE_W, h=CADRE_H, r=30, fill="none", stroke=INK, sw=4, shadow=0,
                  z=2, draw=0, **({"dash": dash} if dash else {}))
    kit.shape("balayage", [CADRE_C[0] + CADRE_W / 2 - 20, CADRE_C[1]], kind="round", w=10, h=CADRE_H - 40, r=5,
              fill=DEEP, stroke=DEEP, sw=0, shadow=0, z=19, scale=0)

    # --- étiquettes « ◀◀ Avant » puis « Maintenant » (S19-S22) ---
    S.add("etiquette_avant", "pill", z=21, text="Avant", icon="rewind", w=300, h=70, size=34, weight=800, fill=LIGHT)
    S.set("etiquette_avant", pos=list(ETIQUETTE_C), scale=0, opacity=1)
    S.add("etiquette_maint", "pill", z=21, text="Maintenant", w=300, h=70, size=34, weight=800, fill=LIGHT)
    S.set("etiquette_maint", pos=list(ETIQUETTE_C), scale=0, opacity=1)

    # --- « Toi » : en P1 dès l'image 0, stylo levé (bras côté gauche : il fait face à ce qu'il touche) ---
    toi = Figure(kit, "toi", pos=list(P1), scale=TOI_SCALE, z=15)

    return SimpleNamespace(toi=toi, societe=societe, book_h=book_h, porte_h=porte_h, cle_h=cle_h)


def build(S):
    kit = Kit(S)
    c = cast(S, kit)
    only = [p for p in os.environ.get("WTH_PARTS", "").split(",") if p]   # WTH_PARTS=p2 : cette partie seule
    for name in PARTS:
        if not only or name in only:
            importlib.import_module(f".{name}", __name__).part(S, kit, c)
