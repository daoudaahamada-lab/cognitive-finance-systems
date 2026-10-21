"""V01 « Préparer ton entretien client avec l’IA » : mise en scène Story, en paquet (une partie par fichier).

Storyboard : scripts/storyboards/V01.json (v1 « révisé après le test sans son », 22 scènes, 93 temps forts, 93,20 s),
version lisible scripts/storyboards/V01.md. Voix : build/V01/words.json (film : images 0-2796).
Fil : un seul dossier, celui du client de 9 h. objet_fil = `pastille` (pilule cyan « Client · 9 h » à pictogramme de
personne) : posée sous l'horloge à l'image 0, elle coiffe la pile (S01), reste au centre des papiers, porte le rond
vide (S06-S11), devient le titre de la fenêtre puis du badge, se pose sur l'en-tête du brief (S14, relais
`pastille_fiche`), le client naît de son pictogramme (S15, S19) et y rentre (S17), la fiche se replie en elle (S20),
elle saute le séparateur (S21) et devient le bouton « S’abonner » (S22).

Parties (scènes contiguës, coupées sur un changement de composition) :
- p1 : S01-S07, images 0-889. L'accroche (pile, horloge, barre de temps qui fond), la promesse en avance rapide
  (▶▶, IA, coche), le repère 1-2-3, le rembobinage (◀◀), la fouille (infos, rond vide), les 4 sources.
- p2 : S08-S14, images 890-1935. « 1 · Limiter » (faisceaux cassés, cadre, outil scellé, mur RGPD), « 2 · Exiger »
  (la page « Réponse », « 5 ans » sorti du nuage, cases-sources, brief relié aux documents datés).
- p3 : S15-S22, images 1936-2796. La ligne cassée devient question, le tampon gardé en main, « 3 · Relire »
  (coches, rature, tampon), la planche, dix minutes de relecture, Avant / Après, fin.
ENTRY_P2 et ENTRY_P3 (plus bas) sont le contrat des raccords : la partie précédente finit exactement dans cet état,
la suivante l'épingle à first_frame - 1 (kit.pin), figurines exceptées (walk / enter, garde-fou de SKILL.md).

Ce fichier déclare TOUTE la distribution à son état de l'image 0 (cast) et les places communes ; chaque partie pose
ses temps forts (pN.py, def part(S, kit, c)). Exceptions : la carte de fin `fin` et son pointeur `fin_curseur`, que
kit.outro déclare lui-même (p3). Une partie qui aurait besoin d'un élément de plus, utilisé dans elle seule, le
déclare en tête de partie sous un id préfixé (`p2_…`) et l'a fait disparaître (scale 0) avant sa dernière image.

Seul ajout au code partagé que cette mise en scène suppose (storyboard, « entites_nouvelles ») : le type stamp reçoit
un paramètre facultatif `sub` (seconde ligne « + 1 question », précédée d'un « ? » cerclé) et sa piste `subOn` ; sans
`sub`, le tampon reste dessiné au pixel près. Il est déclaré ici (`tampon`) ; codé (entities.tsx, GEOM.STAMP_SUB,
Kit.stamp, `sub` dans STORY_TEXT_KEYS de qa.py) : p3 pose subOn 0 -> 1 au contact (hit = toi.stamp(...)).

Mise en scène précédente (storyboard v3.2, voix de 58 s, S01-S20) : `git show 6962c86:wth-videos/scripts/story/V01/pN.py`
(N = 1, 2, 3). Ses gestes réussis (tour du cadre, mur et briques, page écrite par l'IA, fils et dates, rature, tampon,
planche, chemin, brouillon) sont à reprendre en les recalant sur les nouveaux mots et les places ci-dessous.
"""
import importlib
import math
import os
from types import SimpleNamespace

from pipeline.story import GEOM, MORPH, POP, STYLE, text_width
from pipeline.story_kit import Figure, Kit, Sheet

PARTS = ["p1", "p2", "p3"]                      # S01-S07, S08-S14, S15-S22
ALERT_WORDS = {"fausse", "erreur"}              # karaoké en rouge (storyboard, style)
ACOUSTIC_SNAP = {"gap": 0.2, "window": 0.08}    # temps fort après un silence : calé sur l'attaque audible
# Découpes imposées : la découpe automatique coupait des groupes nominaux ou verbaux (« Client / à 9 heures »,
# « au lieu / de préparer », « ce n’est / pas le conseil », « une / IA », « et à / une date », « Une info / sans
# source n’est », « finale ne / se délègue pas », « politique / interne ») ou laissait un éclair (« Ça » 0,2 s,
# « Reste » 0,3 s). 4 mots au plus, tous sous 760 px (Inter Bold 64).
CAPTION_GROUPS = [["Client à 9 heures"], ["au lieu de préparer", "ton conseil"], ["ce n’est pas", "le conseil"],
                  ["Parce qu’avant", "de gagner du temps"], ["dans un outil", "validé par ton cabinet"],
                  ["Le RGPD", "et ta politique interne", "s’appliquent"], ["Ça ne suffit pas"],
                  ["une IA peut produire"], ["Un brief structuré", "d’une page"], ["et à une date"],
                  ["Une info sans source", "n’est pas une certitude"], ["C’est une question", "à poser au client"],
                  ["Reste le plus important"], ["la décision finale", "ne se délègue pas"],
                  ["Toi tu gardes", "le conseil"], ["Avant tu arrives", "en ayant cherché"],
                  ["Après tu arrives", "en ayant compris"]]

# ---------- couleurs (storyboard « style » = pipeline.story.STYLE) ----------
INK, CYAN, DEEP, LIGHT = STYLE["ink"], STYLE["cyan"], STYLE["deep"], STYLE["light"]
PAPER, GREY, RED, AI_TICK, BG = STYLE["paper"], STYLE["grey"], STYLE["red"], STYLE["ai_tick"], STYLE["bg"]


def mix(a, b, t):
    """Couleur hex à t de a vers b (t = 0 : a)."""
    ca, cb = (tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) for h in (a, b))
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(ca, cb))


AI_INK = mix(BG, INK, 0.62)       # pointillés de l'IA (faisceaux, coches, nuage) : gris encre lisible au téléphone

# ---------- mise en page (1080 x 1920) ----------
# Action entre x 40-940 et y 160-1270 (descendre jusqu'à y ≈ 1250) ; sous-titres 1280-1380 ; haut 160 px et bande
# x > 940 réservés à l'interface TikTok / Reels.
X_MIN, X_MAX, Y_MIN, Y_MAX = 40, 940, 160, 1270
CX = 540                            # axe de la colonne d'action
GROUND = 1230                       # ligne de sol : pieds des figurines debout
FIG_BASE = GEOM["FIGURE"]["base"]   # 95 : du centre de la figurine à ses pieds (x échelle)
FIG_TOP = GEOM["FIGURE"]["top"]     # -96 : du centre au haut de la tête (x échelle)
TEXT_MIN = 32                       # corps minimal d'un texte à l'échelle 1 (SKILL.md, grammaire)


def fig_pos(x, feet=GROUND, s=1.0):
    """Centre d'une figurine d'échelle s dont les pieds sont sur la ligne y = feet (place à donner à walk / enter)."""
    return [x, round(feet - FIG_BASE * s, 2)]


def scene_f0(S, sid):
    """Première image de la scène sid (round(t_start x 30))."""
    return round(next(s for s in S.sb["scenes"] if s["id"] == sid)["t_start"] * S.fps)


def seam(S, sid):
    """Image d'épingle du raccord qui ouvre la scène sid : la plus tôt de son début et de son premier temps fort
    (calé sur l'attaque audible, il peut tomber avant le début de la scène), moins 1. Le temps fort n'est pas
    enregistré ici (la partie suivante le pose elle-même avec kit.at)."""
    sc = next(s for s in S.sb["scenes"] if s["id"] == sid)
    n = len(S.beats)
    f = S.beat(sid, sc["beats"][0]["mot"])
    del S.beats[n:]
    return min(scene_f0(S, sid), f) - 1


def vanish(kit, id, f, into=None, d=POP):
    """kit.vanish, plus un fondu d'opacité sur ses 3 dernières images : pas de point résiduel à taille téléphone."""
    end = kit.vanish(id, f, into=into, d=d)
    kit.S.key(id, "opacity", end - 3, 0, 3, "linear")
    return end


def morph_out(kit, outs, f, d=MORPH):
    """kit.morph(outs, [], f) avec le fondu des 3 dernières images (aucun point résiduel)."""
    end = kit.morph(outs, [], f, d=d)
    for o in outs:
        kit.S.key(o, "opacity", end - 3, 0, 3, "linear")
    return end


def card_pts(w, h, fold):
    """Contour d'une carte au coin haut droit plié (shape poly)."""
    return [[-w / 2, -h / 2], [w / 2 - fold, -h / 2], [w / 2, -h / 2 + fold], [w / 2, h / 2], [-w / 2, h / 2]]


def cloud_pts(w, h, bumps=9, amp=0.11, n=90):
    """Contour d'un nuage de pensée (shape poly) : ellipse w x h festonnée de `bumps` bosses."""
    pts = []
    for k in range(n):
        t = 2 * math.pi * k / n
        s = 1 - amp + amp * abs(math.sin(bumps * t / 2))
        pts.append([round(w / 2 * s * math.cos(t), 1), round(h / 2 * s * math.sin(t), 1)])
    return pts


def short_pen(fig, S, length=90):
    """Stylo de 90 px (storyboard) au lieu de GEOM.PEN.len : paramètre `len` du pen et longueur utilisée par le rig."""
    fig.pen_len = length
    S.ents[fig.pen]["p"]["len"] = length


def impact_marks(kit, id, at, z=13.8, side=1, length=40, sw=6, color=INK, spread=14):
    """3 traits d'impact encre en éventail du côté `side` (+1 : droite) d'un point de choc : un groupe (parent
    invisible, scale 0) qui surgit d'un coup (kit.pop) et s'efface (vanish)."""
    kit.shape(id, at, kind="circle", w=2, fill="none", stroke="none", sw=0, shadow=0, z=z, scale=0)
    for k, (a, b) in enumerate((([8, -spread], [8 + length * 0.8, -spread - length * 0.6]), ([10, 0], [10 + length, 0]),
                                 ([8, spread], [8 + length * 0.8, spread + length * 0.6]))):
        kit.shape(f"{id}_{k + 1}", [0, 0], kind="poly", pts=[[a[0] * side, a[1]], [b[0] * side, b[1]]], closed=False,
                  fill="none", stroke=color, sw=sw, shadow=0, z=z, parent=id)


# ---------- places communes (storyboard, « style » MISE EN PAGE et scènes) ----------
# Pastille « Client · 9 h » (objet du fil) : 290 x 60, texte Bold 32 px, pictogramme de personne à gauche
PILL_TEXT, PILL_W, PILL_H, PILL_SIZE = "Client · 9 h", 290, 60, 32
PASTILLE_S01 = (540, 745)            # image 0 : sous le pied de l'horloge
PASTILLE_PILE = (540, 865)           # S01 « 9 » : coiffe la pile ; S02-S07 : seule au centre
PASTILLE_S03 = (540, 805)            # S03 : clipsée sur la pile rangée par l'IA
ROND_S06 = (540, 935)                # le rond vide accroché sous la pastille (S06-S07)

# Horloge de 9 h (WTH-003-01) : 400 px (S01), badge 200 px au bout du repère (S02-S18), 264 px (S19), 160 px (S20)
CLOCK_W = 400
CLOCK_S01 = (540, 500)
CLOCK_BADGE, CLOCK_BADGE_S = (830, 300), 0.5
CLOCK_S19, CLOCK_S19_S = (475, 700), 0.66
CLOCK_S20, CLOCK_S20_S = (255, 590), 0.55        # S20 : l'horloge de 9 h, agrandie au-dessus de lui
DIAL = dict(cx=0.575, cy=0.375, rx=0.20, ry=0.245)   # cadran dans la boîte du PNG (mesuré pour V01 v3)

# Barre de temps (S02-S09) : 580 x 40, x 140 -> 720, y 440 ; 3 blocs (barre, S02-S04) puis 5 (barre2, S05-S09)
BAR_X0, BAR_W, BAR_H, BAR_Y = 140, 580, 40, 440
BAR_C = (BAR_X0 + BAR_W / 2, BAR_Y)


def block_c(k, n):
    """Centre monde du bloc k (0 = le plus à gauche) d'une barre de n blocs."""
    return [round(BAR_X0 + BAR_W * (k + 0.5) / n, 1), BAR_Y]


# Repère 1-2-3 : disques x 320 / 470 / 620, y 300 ; légendes (texte à part, jamais grises) dessous
MARKER_Y, MARKER_CX, MARKER_GAP = 300, 470, 150
MARKER_XS = [MARKER_CX + (k - 1) * MARKER_GAP for k in range(3)]
LEGENDS = ["Limiter", "Exiger", "Relire"]
LEGEND_Y, LEGEND_SIZE = 362, TEXT_MIN

# Pilule « Conseil » (S02-S05) : 200 x 56, sous le badge ; ▶▶ / ◀◀ au-dessus des papiers (S03-S05)
CONSEIL_S02 = (830, 480)
AVANCE_AT = (540, 560)

# Documents : carte 200 x 250 au coin plié, pictogramme cyan, deux traits gris ; bandeau de source (S07) et date
# en clair (S07) ; compact 150 x 80 (S14). (bandeau, date, pictogramme)
DOCS = [("PDF", "mars 2026", "bars"), ("CRM", "déc. 2025", "shield"), ("Mail", "sept. 2025", "check"),
        ("Notes", "févr. 2026", "cal")]
DOC_W, DOC_H, DOC_CW, DOC_CH = 200, 250, 150, 80
BANNER_H, BANNER_SIZE, DOC_DATE_SIZE = 48, TEXT_MIN, TEXT_MIN
PILE_S01 = (540, 1020)                          # pile nette (doc1 dessus), décalée de PILE_STEP
PILE_STEP = 10                                  # décalage visible : on lit une pile de 4 papiers
DOC_SPREAD = [(330, 620, -8), (790, 700, 4), (300, 1040, -5), (620, 1110, 7)]   # S02 « fouilles » et S05 (x, y, rot)
PILE_S03 = (540, 960)                           # pile rangée par l'IA (S03)
PILE_TICK_S03 = (640, 1085)                     # coin bas droit de la pile : la coche du conseiller (S03)
DOC_S07 = [(170, 610), (810, 600), (330, 1080), (750, 1080)]   # S07 « dispersé » (doc1 sous barre2 : coin et info libres)
DOC_GRID_S08, DOC_GRID_S = [(330, 600), (570, 600), (330, 880), (570, 880)], 0.85   # S08 « client » : 2 x 2
PASTILLE_S08, ROND_S08 = (450, 740), (640, 740)  # dans l'allée du groupe (S08)
INFO_R = 28                                     # pastilles d'information : disques de 56 px (puces : 44)
INFO_CORNER = [80, -110]                        # coin haut droit d'une carte (repère du document)
INFO_ICONS = ["bars", "shield", "check", "cal"]

# Dossiers des autres clients (S08-S10) : cartes grises 110 x 140, pilule grise « 14 h » / « 16 h »
GREY_TIMES = ["14 h", "16 h"]
GREY_W, GREY_H = 110, 140
GREY_S08 = [(760, 850), (878, 850)]
GREY_EDGE, GREY_EDGE_S = [(870, 640), (870, 900)], 0.55
# pilule grise de même facture que la pastille du client (60 px de haut, Bold 32 px, pictogramme de personne) : la
# ressemblance dit « un autre client » sans lire l'heure
GREY_PILL_W = round(text_width("16 h", PILL_SIZE, 700) + 100)
GREY_PILL_K = 1.1333                            # pilule x 0,85 sur une carte x 0,75 (repère de la carte)

# L'IA (AI.png, 200 px à l'échelle 1) ; rangée petite et visible dans le coin bas gauche
IA_W = 200
IA_S03, IA_S03_S = (110, 820), 0.8
IA_CORNER, IA_CORNER_S = (60, 1200), 0.42
IA_S08, IA_S08_S = (100, 862), 0.75
IA_S09, IA_S09_S = (300, 1090), 0.8
IA_S12, IA_S12_S = (130, 1110), 0.8
IA_S18, IA_S18_S = (230, 822), 1.0
IA_FLOOR, IA_FLOOR_S = (85, 1185), 0.7
IA_S19, IA_S19_S = (85, 1150), 0.45

# Le conseiller (« Toi ») : repos en bas à droite, pieds sur la ligne de sol
ADV_ENTER_X = 930
ADV_S02 = fig_pos(760)
ADV_REST = fig_pos(840)
ADV_S07 = fig_pos(540)
ADV_S08 = fig_pos(870)
TOI_PILL_DY = -145                              # pilule « Toi » au-dessus de la tête (repère de la figurine)

# Cadre -> fenêtre de l'outil (S09-S11) : x 200 -> 780, y 410 -> 1190 ; coin bas gauche libre pour l'IA
FRAME_C, FRAME_W, FRAME_H = (490, 800), 580, 780
FRAME_X0, FRAME_X1 = FRAME_C[0] - FRAME_W / 2, FRAME_C[0] + FRAME_W / 2
FRAME_TOP, FRAME_Y1 = FRAME_C[1] - FRAME_H / 2, FRAME_C[1] + FRAME_H / 2
TITLE_H = 64
SEAL_K = 1.25
SEAL_W = round(68 * SEAL_K + text_width("Cabinet", 26 * SEAL_K, 700) + 16 * SEAL_K)
FAN_S10 = (490, 720)                            # éventail des 4 sources dans la fenêtre (S10)
TITLE_S10, TITLE_S10_S = (330, 442), 0.85       # la pastille, titre de la fenêtre
RONDE_S10 = (330, 505)                          # le rond vide sous elle
SEAL_DROP = (690, 560)                          # le sceau tombe là, puis s'ouvre au bout de la barre (680, 442)
WIN_S11, WIN_S11_S = (300, 862), 0.88           # fenêtre rangée à gauche : x 45 -> 555, mur droit x 555
WALL_X = round(WIN_S11[0] + FRAME_W / 2 * WIN_S11_S, 1)
CHOC = (WALL_X, 830)                            # le mail bute sur le mur ; la brique « RGPD » s'y encastre
BRICKS = [("RGPD", (WALL_X, 830), 220, 76), ("Politique\ninterne", (WALL_X, 742), 220, 100)]
IA_PUB, IA_PUB_W = (800, 820), 180
FOULE = dict(n=6, h=48, pts=[[-110, -140], [-60, -160], [-5, -168], [50, -160], [84, -128], [92, -76]])
BADGE_C, BADGE_S = (150, 470), 0.3              # la fenêtre réduite en badge (S12-S14)

# La page : « Réponse » (S12) -> brief (S13-S17) -> fiche du RDV (S18-S21) -> carte de fin (S22)
FICHE_LINES = [("Bilan", "profil prudent", "bars"), ("Contrat", "PER", "shield"), ("Décision", "ouvrir PEA", "check"),
               ("Promis", "point fiscal", "cal"), ("Horizon", "5 ans", "none")]
PAGE_S12, PAGE_S12_S = (560, 825), 1.0          # au bout du faisceau de l'IA
PAGE_S13, PAGE_S13_S = (300, 780), 0.95         # à gauche (x 62 -> 538) : la colonne des sources est à droite
HEAD_TITLE_SIZE = 30                            # « Brief · 1 page » tient à droite de la pastille de l'en-tête
PASTILLE_HEAD_S = 0.85
CLOUD_C, CLOUD_W, CLOUD_H = (175, 760), 230, 170
CASE_X, CASE_W, CASE_H = 730, 150, 80
ADV_S13 = (870, 800)                            # S13 : à droite de la page, stylo vers elle
ADV_S15_S = 1.1
ADV_S15 = fig_pos(640, s=ADV_S15_S)             # S15-S16 : au pied de la page
CLIENT_S15 = fig_pos(858)                       # face au conseiller
BUBBLE_AT = (760, 860)                          # bulle « ? » au-dessus du conseiller (S15)
STICKER_S16 = (585, 940)                        # autocollant « ? » contre le bord droit de la page, à hauteur de L5
STAMP_HOLD = (720, 1040)                        # S16 : le tampon fermé tenu levé devant lui
ADV_S17 = (680, 820)                            # S17 : à droite de la page, x 1,1 (fig.place_for)
TICK_AI, TICK_AI_THIN = 48, 6                   # coche de l'IA : pointillés dans un carré tireté (variant ai)
TICK_HUMAN = 64                                 # coche pleine du conseiller à la relecture (S17)
RDV_TEXT = "à poser au RDV"
TAG_SIZE, TAG_H = 34, 54                        # dates et étiquettes-sources (page cornée), 34 px
TAG5_SIZE = TEXT_MIN                            # « à poser au RDV »
TAG_W = round(GEOM["TAG"]["textX"] + max(text_width(d[1], TAG_SIZE, 600) for d in DOCS) + 14)
TAG5_W = round(GEOM["TAG"]["textX"] + text_width(RDV_TEXT, TAG5_SIZE, 600) + 14)
STAMP_TEXT, STAMP_SUB, STAMP_W, STAMP_H, STAMP_SIZE = "PRÊT POUR LE RDV", "+ 1 question", 380, 84, 30
STAMP_LOCAL = [0, 314]                          # bande libre du bas de la page (repère de la fiche) ; incliné de -6°
BUBBLE_BIG = dict(w=236, h=136, r=40, q=110, qx=0, px=60, ps=64, sw=5, shadow=6, gs=4)    # « ? » seul (glyph = 0)
BUBBLE_SMALL = dict(w=72, h=72, r=36, q=48, qx=0, px=27, ps=36, sw=4, shadow=4, gs=3)     # autocollant 72 px

# Planche (S18) : 780 x 16, x 140 -> 920, dessus y 922, pivot encre x 530, base y 1130
PLANK_AT, PLANK_W, PLANK_H = (530, 938), 780, 16
PIVOT_W, PIVOT_H = 120, 192
PAGE_S18, PAGE_S18_S = (440, 760), 0.45
ADV_S18_S = 1.1
ADV_S18 = fig_pos(870, 922, ADV_S18_S)          # sur le bout droit de la planche
TOKENS = [("Conseil", "chat"), ("Adéquation", "target"), ("Responsabilité", "sign")]
TOKEN_H, TOKEN_SIZE = 56, TEXT_MIN
TOKEN_W = round(max(text_width(t, TOKEN_SIZE, 600) for t, _ in TOKENS) + 84)

# Chemin et rendez-vous (S19) : chemin x 100 -> 900, dessus y 1214
PATH_C, PATH_W, PATH_H = (500, 1222), 800, 16
PATH_TOP = PATH_C[1] - PATH_H / 2
ADV_S19 = fig_pos(475, PATH_TOP)
PAGE_S19, PAGE_S19_S = (300, 1052), 0.45
CHAIRS_W = 400
CHAIRS_S19 = (740, 1137)
TABLE_S19 = (720, 1060)                         # la fiche relue sur la table
CLIENT_S19 = (840, 1090)                        # assis dans le fauteuil droit
BROUILLON_S = 0.4
STEP_C, STEP_W, STEP_H = (365, 1155), 150, 150  # S18 : la petite marche de l'IA, à côté du pivot (dessus y 1080)

# Écran partagé (S20-S21) : séparateur x 490 (gauche 40-470 « Avant », droite 510-940 « Après »)
SEP_X, SEP_Y0, SEP_Y1 = 490, 250, 1250
AVANT_AT, APRES_AT = (255, 330), (725, 330)
ADV_S20_S = 0.9
ADV_S20 = fig_pos(255, s=ADV_S20_S)
CHAIRS_S20, CHAIRS_S20_S = (725, 1100), 0.75
PASTILLE_S20 = (255, 860)
FICHE_S21, FICHE_S21_S = (700, 930), 0.35
ADV_S21 = fig_pos(585, s=ADV_S20_S)

# ---------- raccords : état épinglé au début de p2 (image 889) et de p3 (image 1935) ----------
# Figurines exclues (jamais épinglées) : p2 et p3 les replacent par walk / enter, avec le garde-fou de SKILL.md.
ENTRY_P2 = {   # fin de S07 = etat_initial de S08
    "horloge": {"pos": list(CLOCK_BADGE), "scale": CLOCK_BADGE_S, "opacity": 1},
    "marqueur": {"pos": [MARKER_CX, MARKER_Y], "scale": 1, "active": 0, "on": 1},
    **{f"legende{k + 1}": {"scale": 1, "opacity": 1, "chars": len(LEGENDS[k])} for k in range(3)},
    "barre": {"scale": 0}, "barre2": {"pos": list(BAR_C), "scale": 1, "value": 0, "w": BAR_W},
    **{f"bloc{k + 1}": {"scale": 0} for k in range(8)},
    "conseil": {"scale": 0}, "avance": {"scale": 0},
    **{f"doc{i + 1}": {"pos": list(DOC_S07[i]), "scale": 1, "rot": 0, "compact": 0, "tag": 0, "opacity": 1}
       for i in range(4)},
    **{f"doc{i + 1}_bandeau": {"opacity": 1} for i in range(4)},
    **{f"doc{i + 1}_date": {"opacity": 1} for i in range(4)},
    **{f"info{i + 1}": {"pos": list(INFO_CORNER), "scale": 1} for i in range(4)},
    "pastille": {"pos": list(PASTILLE_PILE), "scale": 1, "opacity": 1},
    "rond": {"pos": list(ROND_S06), "scale": 1, "alarm": 0},
    "ia": {"pos": list(IA_CORNER), "scale": IA_CORNER_S, "opacity": 1},
    "carte_grise1": {"scale": 0}, "carte_grise2": {"scale": 0},
}
ENTRY_P3 = {   # fin de S14 = etat_initial de S15
    "horloge": {"pos": list(CLOCK_BADGE), "scale": CLOCK_BADGE_S, "opacity": 1},
    "marqueur": {"pos": [MARKER_CX, MARKER_Y], "scale": 1, "active": 1, "on": 1},
    **{f"legende{k + 1}": {"scale": 1, "opacity": 1, "chars": len(LEGENDS[k])} for k in range(3)},
    "barre2": {"scale": 0}, "outil": {"scale": 0}, "cadre": {"scale": 0}, "pastille": {"scale": 0},
    "ia": {"pos": list(IA_CORNER), "scale": IA_CORNER_S, "opacity": 1},
    "fiche": {"pos": list(PAGE_S13), "scale": PAGE_S13_S, "opacity": 1, "lite": 0},
    "fiche_titre1": {"opacity": 0}, "fiche_titre2": {"opacity": 1}, "pastille_fiche": {"opacity": 1},
    **{f"L{i + 1}": {"chars": len(FICHE_LINES[i][0]) + len(FICHE_LINES[i][1]), "grow": 1, "bulletOn": 1}
       for i in range(5)},
    "L5": {"chars": len("Horizon") + len("5 ans"), "grow": 1, "bulletOn": 1, "alarm": 1, "red": 0, "crack": 0},
    **{f"coche_ia{i + 1}": {"draw": 1} for i in range(5)},
    **{f"case{i + 1}": {"scale": 1, "draw": 1} for i in range(5)},
    **{f"doc{i + 1}": {"scale": 1, "compact": 1, "rot": 0, "opacity": 1} for i in range(4)},
    **{f"fil{i + 1}": {"draw": 1} for i in range(4)}, "fil5": {"draw": 0},
    **{f"source{i + 1}": {"scale": 1, "tagged": 0} for i in range(4)},
    "nuage": {"scale": 0}, "rond": {"scale": 0}, **{f"info{i + 1}": {"scale": 0} for i in range(4)},
}


def tag_geom(text, w=TAG_W, size=TAG_SIZE):
    """Géométrie d'une page cornée (label tagged, doc.tag) : texte en clair."""
    return {"w": w, "h": TAG_H, "date": text, "size": size}


def case_y(i):
    """y monde de la case-source i (en face de la rangée i de la page en S13-S15)."""
    return round(PAGE_S13[1] + Sheet(n=5).rows[i] * PAGE_S13_S, 1)


# ---------- distribution ----------

def cast(S, kit):
    """Toute la distribution, à son état de l'image 0 : S01 montre seulement l'horloge de 9 h, la pile nette des 4
    documents et, sous le pied de l'horloge, la pastille. Ce qui arrive plus tard est déclaré à sa première place
    avec scale=0 (figurines : show=False)."""
    sheet = Sheet(n=5)                                   # 500 x 720, rangées -224, -120, -16, 88, 192
    rows, ty, ly, X = sheet.rows, sheet.ty, sheet.ly, sheet.x

    # --- horloge de 9 h (PNG) ; secteur des 10 minutes calé sur son cadran et « 10 min » (S19) ---
    clk = S.png("WTH-003-01")
    clock_h = round(CLOCK_W * clk["h"] / clk["w"])
    S.add("horloge", "png", z=3, src=clk["src"], w=CLOCK_W, h=clock_h,
          contact=dict(w=round(CLOCK_W * 0.6), h=26, dy=4, blur=10, alpha=0.18))
    S.set("horloge", pos=list(CLOCK_S01), scale=1, opacity=1)
    dial_c = [round((DIAL["cx"] - 0.5) * CLOCK_W, 1), round((DIAL["cy"] - 0.5) * clock_h, 1)]
    dial_r = round(DIAL["rx"] * CLOCK_W, 1)
    S.add("secteur", "sector", z=3.1, parent="horloge", r=dial_r, unit=60, face="none", fill=DEEP)
    S.set("secteur", pos=dial_c, sy=round(DIAL["ry"] * clock_h / (DIAL["rx"] * CLOCK_W), 4), start=50, value=0)
    kit.counter("dix_min", [CLOCK_S19[0] + 175, CLOCK_S19[1]], value=0, size=44, weight=800, color=INK,
                suffix=" min", anchor="start", z=3.3, scale=0)

    # --- barre de temps (S02-S04 : 3 blocs ; S05-S09 : 5 blocs) et blocs qui partent dans les papiers ---
    kit.gauge("barre", BAR_C, value=1, w=BAR_W, h=BAR_H, dir="left", segments=3, z=5.5, scale=0)
    kit.gauge("barre2", BAR_C, value=1, w=BAR_W, h=BAR_H, dir="left", segments=5, z=5.5, scale=0)
    for g in ("barre", "barre2"):
        S.set(g, fill=CYAN, w=BAR_W)                     # hex : fondus possibles ; w : rétraction dans l'horloge (S09)
    # bloc1-3 : les 3 blocs de la barre (S02 : 1 et 2 partent dans doc3 et doc2 ; S03 : reviennent ; S04 : montent et
    # s'arrondissent en disques, pistes w / h / r) ; bloc4-8 : les 5 blocs de barre2 (S05-S07)
    for k in range(8):
        n, j = (3, k) if k < 3 else (5, k - 3)
        bw = round(BAR_W / n, 1)
        kit.shape(f"bloc{k + 1}", block_c(j, n), kind="round", w=bw, h=BAR_H, r=4, fill=CYAN, stroke=INK, sw=4, shadow=0,
                  z=5.6, scale=0)
        S.set(f"bloc{k + 1}", w=bw, h=BAR_H, r=4, fill=CYAN)

    # --- repère 1-2-3 (S04-S18) ; légendes à part, à l'encre (jamais grises), écrites mot à mot (S04) ---
    kit.steps_marker(None, n=3, id="marqueur", y=MARKER_Y, cx=MARKER_CX, gap=MARKER_GAP, z=20)
    S.ents["marqueur"]["p"].update(moveBlank=True)
    S.set("marqueur", scale=0, on=0)
    for k, lab in enumerate(LEGENDS):
        kit.text(f"legende{k + 1}", [MARKER_XS[k], LEGEND_Y], lab, size=LEGEND_SIZE, weight=600, color=INK, z=20.5,
                 typed=True, underColor=DEEP)
        S.set(f"legende{k + 1}", under=0)
    # disque de chapitre (S09 « Première », S13 « Deuxième », S17 « Troisième ») : grandit x 1,6 sur le disque actif
    kit.shape("chapitre", [MARKER_XS[0], MARKER_Y], kind="circle", w=64, fill=CYAN, stroke=INK, sw=4, shadow=6, z=21,
              scale=0)
    kit.text("chapitre_txt", [0, 2], "1", size=34, weight=800, color=INK, z=21.1, parent="chapitre")
    S.set("chapitre_txt", text="1")

    # --- pilule « Conseil » (S02-S05) et sa coche ; « ▶▶ » -> « ◀◀ » (S03-S05) ---
    S.add("conseil", "pill", z=13.4, text="Conseil", w=round(text_width("Conseil", TEXT_MIN, 600) + 92), h=56,
          size=TEXT_MIN, weight=600, fill=PAPER, icon="chat", iconColor=DEEP)
    S.set("conseil", pos=list(CONSEIL_S02), scale=0, opacity=1, fill=PAPER)
    kit.tick("conseil_coche", [round(text_width("Conseil", TEXT_MIN, 600) / 2 + 40, 1), -2], DEEP, size=40, sw=8,
             z=13.45, parent="conseil", draw=0)
    kit.shape("avance", AVANCE_AT, kind="round", w=120, h=60, r=30, fill=INK, stroke=INK, sw=4, shadow=6, z=21,
              scale=0)
    kit.icon("avance_ico", [0, 0], "rewind", s=44, color=PAPER, z=21.1, parent="avance", rot=180)

    # --- les 4 documents : pile nette sous la pastille (doc1 dessus) ; bandeau de source et date (S07) ---
    for i, (src, date, icon) in enumerate(DOCS):
        d = f"doc{i + 1}"
        z = round(12 - 0.1 * i, 2)
        S.add(d, "doc", z=z, title="", icon=icon, date=date, cw=DOC_CW, ch=DOC_CH, titleSize=26,
              tag=tag_geom(date), fw=DOC_W, fh=DOC_H, fts=26)
        S.set(d, pos=[PILE_S01[0] + PILE_STEP * (i - 1.5), PILE_S01[1] + PILE_STEP * (i - 1.5)], scale=1, rot=0,
              compact=0, tag=0, txt=1, read=0, sh=6, lit=0, z=z, opacity=1)
        kit.shape(f"{d}_bandeau", [0, round(-DOC_H / 2 + BANNER_H / 2, 1)], kind="rect", w=DOC_W, h=BANNER_H,
                  fill=LIGHT, stroke=INK, sw=4, shadow=0, z=z + 0.02, parent=d, opacity=0)
        kit.text(f"{d}_bandeau_txt", [0, 2], src, size=BANNER_SIZE, weight=700, color=INK, z=z + 0.03,
                 parent=f"{d}_bandeau")
        kit.shape(f"{d}_date", [0, round(DOC_H / 2 - 34, 1)], kind="rect", w=DOC_W - 16, h=36, fill=PAPER,
                  stroke="none", sw=0, shadow=0, z=z + 0.02, parent=d, opacity=0)      # masque le 2e trait gris
        kit.text(f"{d}_date_txt", [-DOC_W / 2 + 16, 2], date, size=DOC_DATE_SIZE,
                 weight=600, color=DEEP, anchor="start", z=z + 0.03, parent=f"{d}_date")
        # traits de vitesse du rembobinage (S05), à orienter par la partie (rot du groupe)
        kit.shape(f"{d}_vitesse", [0, 0], kind="circle", w=2, fill="none", stroke="none", sw=0, shadow=0,
                  z=z - 0.05, parent=d, scale=0)
        for j, off in enumerate((-40, 0, 40)):
            kit.shape(f"{d}_vitesse{j + 1}", [0, 0], kind="poly", pts=[[118, off], [198, off]], closed=False,
                      fill="none", stroke=INK, sw=4, shadow=0, z=z - 0.05, parent=f"{d}_vitesse")
        # pastille d'information (S06) : sort du pictogramme sous la pointe et se pose sur le coin de la carte
        S.add(f"info{i + 1}", "bullet", z=12.5, parent=d, icon=INFO_ICONS[i], r=INFO_R)
        S.set(f"info{i + 1}", pos=list(INFO_CORNER), scale=0, opacity=1)
    kit.tick("coche_pile", PILE_TICK_S03, DEEP, size=60, sw=8, z=13.6, draw=0)

    # --- le rond vide (S06-S12) : la vie du client, écrite nulle part ---
    S.add("rond", "bullet", z=13.2, icon="none", r=INFO_R)
    S.set("rond", pos=[560, 640], scale=0, opacity=1, alarm=0)

    # --- pastille « Client · 9 h » (objet du fil) ---
    S.add("pastille", "pill", z=13.5, text=PILL_TEXT, w=PILL_W, h=PILL_H, size=PILL_SIZE, weight=700, fill=CYAN,
          icon="person")
    S.set("pastille", pos=list(PASTILLE_S01), scale=1, opacity=1, text=PILL_TEXT, fill=CYAN, w=PILL_W)
    S.add("pastille_btn", "pill", z=41, text="S’abonner", w=PILL_W, h=PILL_H, size=PILL_SIZE, weight=700, fill=CYAN)
    S.set("pastille_btn", pos=list(PASTILLE_S01), scale=1, opacity=0, w=PILL_W)   # S22 : la pastille sans pictogramme

    # --- dossiers des autres clients (S08-S10) : carte grise + pilule grise de même forme que la pastille ---
    for k, t in enumerate(GREY_TIMES):
        g = f"carte_grise{k + 1}"
        kit.shape(g, DOC_S07[1], kind="poly", pts=card_pts(GREY_W, GREY_H, 14), fill=GREY, stroke=INK, sw=4, shadow=6,
                  z=11.9 - 0.01 * k, scale=0)
        S.add(f"{g}_pill", "pill", z=11.95 - 0.01 * k, parent=g, text=t, w=GREY_PILL_W, h=PILL_H, size=PILL_SIZE,
              weight=700, fill=GREY, icon="person")
        S.set(f"{g}_pill", pos=[0, -GREY_H / 2], scale=GREY_PILL_K, opacity=1, text=t)

    # --- l'IA (AI.png, tournée vers la droite) : pilule, faisceaux pointillés, cône de lecture ---
    ai = S.png("AI", keep_largest=True)
    ai_h = round(IA_W * ai["h"] / ai["w"])
    brain_top, brain_front = [-6, round(-0.44 * ai_h, 1)], [40, round(-0.28 * ai_h, 1)]   # cerveau de verre
    S.add("ia", "png", z=4, src=ai["src"], w=IA_W, h=ai_h, saturate=0.85,
          contact=dict(w=round(IA_W * 0.72), h=28, dy=4, blur=10, alpha=0.2))
    S.set("ia", pos=list(IA_S03), scale=0, opacity=1)
    S.add("ia_pill", "pill", z=4.1, parent="ia", text="IA", w=round(text_width("IA", TEXT_MIN, 600) + 48), h=52,
          size=TEXT_MIN, weight=600, fill=PAPER, sw=4, shadow=5)
    S.set("ia_pill", pos=[0, round(ai_h / 2 + 30, 1)], scale=1, opacity=1)
    beam = dict(color=AI_INK, sw=7, dash=[0.01, 17], dots=True)
    # faisceau1-4 : vers les 4 documents (S03 range la pile, S08 vise les sources) ; faisceau5-6 : vers les dossiers
    # des autres clients (S08) ; rayon (S10) ; faisceau_lit (S12 : vers le badge) ; faisceau_page (S12 : écrit la
    # page) ; faisceau_tampon (S16 : touche le tampon, via sous la page) ; faisceau_passe (S18 : pousse la fiche)
    for wid in [f"faisceau{k + 1}" for k in range(6)] + ["rayon", "faisceau_lit", "faisceau_page", "faisceau_tampon",
                                                         "faisceau_passe"]:
        S.add(wid, "wire", z=13, a={"id": "ia", "at": brain_front}, **beam)
        S.set(wid, draw=0, pb=[0, 0], via=[], sag=0, opacity=1, **{"from": 0})
    kit.shape("cone", [0, 0], kind="poly", pts=[[0, 0], [10, 0], [0, 10]], fill=LIGHT, stroke=AI_INK, sw=4,
              dash=[0.01, 12], shadow=0, z=1.5, scale=0)   # sommets à poser par p2 (S09 : coupé net par le cadre)
    S.set("cone", fillOp=0.2)
    for k, w in enumerate((12, 16, 22)):                 # bulles de pensée : de la tête de l'IA vers le nuage (S12)
        kit.shape(f"pensee{k + 1}", [0, 0], kind="circle", w=w, fill=PAPER, stroke=AI_INK, sw=3, dash=[4, 4],
                  shadow=0, z=13.04, scale=0)
    kit.shape("nuage", list(CLOUD_C), kind="poly", pts=cloud_pts(CLOUD_W, CLOUD_H), fill=PAPER, stroke=AI_INK, sw=5,
              dash=[12, 9], shadow=0, z=13.05, scale=0)
    kit.text("nuage_val", list(CLOUD_C), "5 ans", size=34, weight=600, color=INK, z=13.15, scale=0)

    # --- l'IA grand public (S11) : AI.png en verre gris cerné d'encre, tournée vers la fenêtre ; foule ; trait ---
    pub_h = round(IA_PUB_W * ai["h"] / ai["w"])
    S.add("ia_pub", "png", z=4, src=ai["src"], w=IA_PUB_W, h=pub_h, tint="mono", outline=3, flip=True,
          contact=dict(w=round(IA_PUB_W * 0.72), h=26, dy=4, blur=10, alpha=0.2))
    S.set("ia_pub", pos=list(IA_PUB), scale=0, opacity=1)
    kit.crowd("foule", [0, 0], show=0, link=0, z=3.9, parent="ia_pub", tone=AI_INK, linkColor="ai_tick", **FOULE)
    pub_head = [0, round(-0.22 * pub_h, 1)]
    S.add("ia_pub_pill", "pill", z=18.5, parent="ia_pub", text="IA grand public",
          w=round(text_width("IA grand public", TEXT_MIN, 600) + 44), h=54, size=TEXT_MIN, weight=600, fill=GREY, sw=4,
          shadow=5)
    S.set("ia_pub_pill", pos=[-10, 130], scale=1, opacity=1)
    for k in range(4):     # S11 : chaque petite figurine de la foule verse sa carte dans la même IA (entonnoir commun)
        kit.shape(f"carte_pub{k + 1}", list(IA_PUB), kind="poly", pts=card_pts(46, 58, 12), fill=GREY, stroke=INK,
                  sw=3, shadow=0, z=4.05, scale=0)
    S.add("trait_pub", "wire", z=13, a={"id": "ia_pub", "at": pub_head}, color=AI_INK, sw=4)
    S.set("trait_pub", draw=0, pb=list(CHOC), via=[], sag=0, opacity=1, **{"from": 0})

    # --- le conseiller (« toi ») : figurine encre, bras à longueur fixe, stylo de 90 px ; pilule « Toi » ---
    toi = Figure(kit, "toi", pos=fig_pos(ADV_ENTER_X), show=False)     # entre par la droite sur « Et » (S02)
    short_pen(toi, S)
    toi_pill = dict(text="Toi", w=round(text_width("Toi", TEXT_MIN, 600) + 56), h=52, size=TEXT_MIN, weight=600,
                    fill=INK, color=PAPER, stroke=INK, shadow=5)
    S.add("toi_pill", "pill", z=16.5, parent="toi", **toi_pill)
    S.set("toi_pill", pos=[0, TOI_PILL_DY], scale=0, opacity=1)
    # S21 : le même conseiller, « après », à droite ; la pilule « Toi » saute le séparateur (relais toi_pill_vol)
    toi2 = Figure(kit, "toi2", pos=list(ADV_S21), scale=ADV_S20_S, show=False)
    short_pen(toi2, S)
    S.add("toi2_pill", "pill", z=16.5, parent="toi2", **toi_pill)
    S.set("toi2_pill", pos=[0, TOI_PILL_DY], scale=0, opacity=1)
    S.add("toi_pill_vol", "pill", z=21.5, **toi_pill)
    S.set("toi_pill_vol", pos=list(AVANT_AT), scale=0, opacity=1)
    # le tampon fermé (S16 ; S17 « décides ») : socle deep 120 x 40 et poignée encre, face cachée, aucun texte
    kit.shape("tampon_ferme", list(STAMP_HOLD), kind="round", w=120, h=40, r=10, fill=DEEP, stroke=INK, sw=4, shadow=6,
              z=16.2, scale=0, rot=-6)
    kit.shape("tampon_ferme_cou", [0, -32], kind="rect", w=22, h=26, fill=INK, stroke=INK, sw=0, shadow=0, z=16.15,
              parent="tampon_ferme")
    kit.shape("tampon_ferme_poignee", [0, -54], kind="round", w=50, h=26, r=13, fill=INK, stroke=INK, sw=0, shadow=0,
              z=16.18, parent="tampon_ferme")
    impact_marks(kit, "impact_stylo", [700, 850], z=16.8, side=1, length=56, sw=7, spread=18)   # S08 : faisceaux cassés
    impact_marks(kit, "impact_cadre", [FRAME_X1, 660], z=13.8, side=-1, length=60, sw=7, spread=20)   # S10, S16
    impact_marks(kit, "impact_mur", list(CHOC), z=13.8, side=1, length=60, sw=7, spread=32)  # S11 : le mail bute
    impact_marks(kit, "impact_brouillon", [520, 1150], z=16.8, side=-1, length=60, sw=8, spread=20)   # S19 : stylo
    # éclats d'un choc (rayons encre) : un seul jeu, reposé à chaque choc (S08, S10 x 2, S11, S16, S19)
    S.add("eclat", "burst", z=17.2, r0=16, r1=52, n=8, sw=6, color=INK)
    S.set("eclat", pos=[0, 0], scale=1, opacity=1, p=0)

    # --- le client : figurine papier, sans outil ni étiquette ---
    client = Figure(kit, "client", pos=list(CLIENT_S15), variant="paper", tool=False, show=False, z=14.8)

    # --- cadre (S09) -> fenêtre de l'outil scellé (S10-S11) -> badge (S12-S14) ; sceau, briques, cadenas ---
    S.add("cadre", "case", z=1, w=FRAME_W, h=FRAME_H)
    S.set("cadre", pos=list(FRAME_C), scale=1, rot=180, draw=0, opacity=1)   # rot 180 : le tracé part du bas droit
    S.add("outil", "window", z=1, titleH=TITLE_H, r=24, sealW=SEAL_W, sealText="Cabinet", sealK=SEAL_K)
    S.set("outil", pos=list(FRAME_C), w=FRAME_W, h=FRAME_H, scale=0, opacity=1, seal=0, lock=0, bar=0, sealOn=0,
          sealDy=0, lockOn=0, lockDy=0, lockDx=0, lockK=1)
    # S11 : le mur droit de la fenêtre, épais et encré (enfant de la fenêtre : il la suit jusqu'au badge)
    kit.shape("mur", [FRAME_W / 2, 0], kind="rect", w=14, h=FRAME_H, fill=INK, stroke=INK, sw=0, shadow=0, z=13.2,
              parent="outil", scale=0)
    kit.shape("cadre_flash", list(FRAME_C), kind="round", w=FRAME_W, h=FRAME_H, r=24, fill="none", stroke=CYAN, sw=10,
              shadow=0, z=1.15, opacity=0)
    kit.icon("sceau", list(SEAL_DROP), "building", disc=48, fill=CYAN, color=INK, s=62, z=13.7, scale=0)
    kit.tick("coche_sceau", [27, 24], PAPER, size=30, sw=7, z=13.75, parent="sceau", draw=0)
    for k, (txt, at, w, h) in enumerate(BRICKS):
        b = f"brique{k + 1}"
        kit.shape(b, at, kind="round", w=w, h=h, r=8, fill=INK, stroke=INK, sw=4, shadow=6, z=18, scale=0)
        kit.text(f"{b}_txt", [0, 2], txt, size=TEXT_MIN if k == 0 else 30, weight=600, color=PAPER, z=18.1, parent=b,
                 lh=1.0)

    # --- la page : « Réponse » -> « Brief · 1 page » -> fiche du RDV ---
    def sheen(dx, dy):
        return {"id": "reflet", "dx": dx, "dy": dy, "w": sheet.w, "h": sheet.h}
    S.add("reflet", "sheen", z=10, w=sheet.w, h=sheet.h, under=True)
    S.set("reflet", p=0)
    S.add("fiche", "fiche", z=8, w=sheet.w, h=sheet.h, title="", headerH=sheet.head,
          tabs=[r + ty for r in rows], tabX=X["bullet"], sheen=sheen(0, 0))
    S.set("fiche", pos=list(PAGE_S12), scale=0, opacity=1, lite=0, **{f"tab{i}": 0 for i in range(5)})
    head_y = round(-sheet.h / 2 + sheet.head / 2 + 2, 1)
    for k, t in enumerate(("Réponse", "Brief · 1 page")):   # le titre change sur « structuré » (fondu enchaîné)
        kit.text(f"fiche_titre{k + 1}", [sheet.w / 2 - 26, head_y], t, size=36 if k == 0 else HEAD_TITLE_SIZE,
                 weight=800, color=INK, anchor="end", z=8.6, parent="fiche", opacity=1 if k == 0 else 0)
    sheet.id, sheet.lines = "fiche", []
    for i, (k, v, icon) in enumerate(FICHE_LINES):
        lid = f"L{i + 1}"
        p = sheet.line_params(k, v, icon, sheen=sheen(0, rows[i]), keyW=round(text_width(k, 32, 600), 1))
        S.add(lid, "line", z=9, parent="fiche", **p)
        S.set(lid, pos=[0, rows[i]], chars=0, red=0, crack=0, flash=0, pulse=0, alarm=0, strike=0, fall=0, grow=0,
              dimValue=0, slotFill=1, bulletOn=0, opacity=1, lite=0)
        sheet.lines.append((lid, p))
    head_pill = [round(-sheet.w / 2 + 18 + PILL_W * PASTILLE_HEAD_S / 2, 1), head_y - 2]
    S.add("pastille_fiche", "pill", z=12.5, parent="fiche", text=PILL_TEXT, w=PILL_W, h=PILL_H, size=PILL_SIZE,
          weight=700, fill=CYAN, icon="person", sheen=sheen(*head_pill))
    S.set("pastille_fiche", pos=head_pill, scale=PASTILLE_HEAD_S, opacity=0, text=PILL_TEXT)
    slot_w = X["slot1"] - X["slot0"]
    kit.shape("surligneur", [round((X["slot0"] + X["slot1"]) / 2, 1), rows[4] + ty], kind="round", w=slot_w, h=48,
              r=12, fill=LIGHT, stroke=LIGHT, sw=0, shadow=0, z=8.5, parent="fiche", scale=0)
    for i in range(5):     # coches de l'IA (pointillés dans un carré tireté) puis coches pleines du conseiller (S17)
        kit.tick(f"coche_ia{i + 1}", sheet.pt(i, "tick"), AI_INK, size=TICK_AI, sw=8, variant="ai", z=11.5,
                 parent="fiche", draw=0, thin=TICK_AI_THIN, boxSw=3.5, boxFill=PAPER)
    for i in range(4):
        kit.tick(f"coche{i + 1}", sheet.pt(i, "tick"), DEEP, size=TICK_HUMAN, sw=8, z=11.6, parent="fiche", draw=0)
    kit.tick("coche5", sheet.pt(4, "tick"), DEEP, size=TICK_HUMAN, sw=8, z=11.6, parent="fiche", draw=0)   # S21
    # S12 « fausse » : la ligne 5 suspecte (surlignage rouge clair à contour rouge en tirets, anneau rouge autour de la
    # puce, onde rouge qui part d'elle) ; « 5 ans » garde le contour pointillé du nuage d'où il vient (nuage5)
    b5 = [X["bullet"], rows[4] + ty]
    kit.shape("bande5", [-46, rows[4] + ty], kind="round", w=456, h=68, r=16, fill="#F8DDE1", stroke=RED, sw=4,
              dash=[12, 8], shadow=0, z=8.45, parent="fiche", opacity=0)
    kit.shape("onde5", b5, kind="circle", w=50, fill="none", stroke=RED, sw=4, shadow=0, z=9.55, parent="fiche",
              scale=0)
    kit.shape("anneau5", b5, kind="circle", w=74, fill="none", stroke=RED, sw=4, dash=[8, 6], shadow=0, z=9.55,
              parent="fiche", scale=0)
    p5 = sheet.lines[4][1]
    kit.shape("nuage5", [round(X["value"] - p5["valueW"] / 2, 1), rows[4] + ty], kind="poly",
              pts=cloud_pts(round(p5["valueW"] + 48), 62, bumps=7, amp=0.12), fill="none", stroke=AI_INK, sw=4,
              dash=[7, 7], shadow=0, z=9.6, parent="fiche", scale=0)
    kit.shape("reponse5", b5, kind="circle", w=44, fill=CYAN, stroke=INK, sw=4, shadow=0, z=9.7, parent="fiche",
              scale=0)                                                       # S21 : la puce de L5 remplie
    kit.tick("coche_relue", [round(sheet.w / 2 - 40, 1), round(-sheet.h / 2 + 40, 1)], DEEP, size=TICK_HUMAN, sw=10,
             z=11.6, parent="fiche", draw=0)                                 # S19 : coin de la fiche relue

    # --- preuves (S13-S17) : cases-sources, fils pleins, dates -> étiquettes-sources, « à poser au RDV » ---
    for i in range(5):
        c = f"case{i + 1}"
        S.add(c, "case", z=5, w=CASE_W, h=CASE_H)
        S.set(c, pos=[CASE_X, case_y(i)], scale=1, draw=0, opacity=1)
        for j, y in enumerate((-CASE_H / 2 + 22, CASE_H / 2 - 20)):         # bandeau vide en haut, date vide en bas
            kit.shape(f"{c}_l{j + 1}", [0, 0], kind="poly", pts=[[-CASE_W / 2 + 6, y], [CASE_W / 2 - 6, y]],
                      closed=False, fill="none", stroke=DEEP, sw=3, dash=[10, 8], shadow=0, z=5.05, parent=c, draw=0)
    wire_a = [[round(X["value"] - p["valueW"] / 2, 1), rows[i] + ty] for i, (_, p) in enumerate(sheet.lines)]
    for i in range(4):
        S.add(f"fil{i + 1}", "wire", z=11, a={"id": "fiche", "at": wire_a[i]}, b={"id": f"doc{i + 1}", "at": [0, 0]},
              color=DEEP, sw=5, dots=True)
        S.set(f"fil{i + 1}", draw=0, sag=0, opacity=1, **{"from": 0})
    S.add("fil5", "wire", z=11, a={"id": "fiche", "at": wire_a[4]}, color=DEEP, sw=5, dots=True, dashAlt=[14, 11])
    S.set("fil5", draw=0, pb=[CASE_X - CASE_W / 2 + 2, case_y(4)], sag=0, dashed=0, opacity=1, **{"from": 0})
    tag_cx = round(X["value"] - TAG_W / 2, 1)
    for i in range(4):     # S14 : la date glisse le long du fil ; S15 : la source s'y fond (tagged 1 : étiquette)
        S.add(f"source{i + 1}", "label", z=12.6, parent="fiche", icon=DOCS[i][2], tag=tag_geom(DOCS[i][1]))
        S.set(f"source{i + 1}", pos=[tag_cx, rows[i] + ly], scale=0, pop=1, lit=0, tagged=0, flash=0, opacity=1,
              lite=0)
    S.add("source5", "label", z=12.6, parent="fiche", icon="clock9", tag=tag_geom(RDV_TEXT, TAG5_W, TAG5_SIZE))
    S.set("source5", pos=[round(X["value"] - TAG5_W / 2, 1), rows[4] + ly + 4], scale=0, pop=1, lit=0, tagged=1,
          flash=0, opacity=1, lite=0)

    # --- la question : « ? », bulle du conseiller, autocollant ; place de l'empreinte ; tampon ---
    S.add("question", "qmark", z=17)
    S.set("question", pos=list(BUBBLE_AT), scale=0, gs=110, opacity=1)
    head = [ADV_S15[0] + 4, ADV_S15[1] + FIG_TOP * ADV_S15_S - 6]          # haut de sa tête (S15)
    bubble_p = dict(big=BUBBLE_BIG, small=BUBBLE_SMALL, tail=[head[0] - BUBBLE_AT[0], head[1] - BUBBLE_AT[1]],
                    tailBase=[-96, -50])
    S.add("bulle", "bubble", z=17.5, **bubble_p)                           # aussi la petite bulle du RDV (S21)
    S.set("bulle", pos=list(BUBBLE_AT), scale=0, s=0, q=0, glyph=0, pulse=0, opacity=1, rot=0)
    S.add("autocollant", "bubble", z=11.7, parent="fiche", **bubble_p)     # sur la fiche (S16-S21)
    S.set("autocollant", pos=[round(X["value"] - 40, 1), rows[4] + ty], scale=1, s=1, q=1, glyph=0, pulse=0, opacity=0)
    S.add("empreinte", "case", z=11.7, parent="fiche", w=STAMP_W, h=STAMP_H)   # S16 : la place de la décision
    S.set("empreinte", pos=list(STAMP_LOCAL), rot=-6, scale=1, draw=0, opacity=1)
    # NOUVEAU (opt-in, storyboard « entites_nouvelles ») : stamp `sub` + piste `subOn`
    S.add("tampon", "stamp", z=11.8, parent="fiche", text=STAMP_TEXT, sub=STAMP_SUB, w=STAMP_W, h=STAMP_H,
          size=STAMP_SIZE)
    S.set("tampon", pos=list(STAMP_LOCAL), rot=-6, scale=0, handle=1, opacity=0, lite=0, subOn=0)

    # --- planche (S18) ; jetons Conseil / Adéquation / Responsabilité ---
    kit.seesaw("planche", PLANK_AT, w=PLANK_W, h=PLANK_H, fill=INK, base=INK, baseW=PIVOT_W, baseH=PIVOT_H, ground=0,
               z=6, scale=0)
    for k, (label, icon) in enumerate(TOKENS):
        j = f"jeton{k + 1}"
        S.add(j, "pill", z=6.5 + 0.01 * k, parent="planche", text=label, w=TOKEN_W, h=TOKEN_H, size=TOKEN_SIZE,
              weight=600, fill=LIGHT, icon=icon, iconColor=DEEP)
        S.set(j, pos=kit.seat("planche", 250, TOKEN_H + (TOKEN_H + 4) * 2 * k), scale=0, opacity=1, text=label)

    kit.shape("marche", list(STEP_C), kind="rect", w=STEP_W, h=STEP_H, fill=PAPER, stroke=INK, sw=4, shadow=6, z=3.8,
              scale=0)                                                      # S18 : la marche de l'IA
    # --- chemin, fauteuils, brouillon de l'IA (S19) ---
    kit.shape("chemin", list(PATH_C), kind="round", w=PATH_W, h=PATH_H, r=8, fill=INK, stroke=INK, sw=4, shadow=6, z=6,
              scale=0)
    ch = S.png("WTH-003-08")
    S.add("fauteuils", "png", z=3.5, src=ch["src"], w=CHAIRS_W, h=round(CHAIRS_W * ch["h"] / ch["w"]), shadow=0.22)
    S.set("fauteuils", pos=list(CHAIRS_S19), scale=0, opacity=1)
    kit.shape("brouillon", [IA_S19[0], IA_S19[1] - 80], kind="round", w=sheet.w, h=sheet.h, r=16, fill=PAPER,
              stroke=AI_INK, sw=12, dash=[0.01, 22], shadow=12, z=14, scale=0)    # contour pointillé + ombre
    for i, (k, v, icon) in enumerate(FICHE_LINES):
        b = f"brouillon_L{i + 1}"
        S.add(b, "line", z=14.1, parent="brouillon", **sheet.line_params(k, v, icon, keyW=round(text_width(k, 32, 600), 1)))
        S.set(b, pos=[0, rows[i]], chars=len(k) + len(v), red=1 if i == 4 else 0, crack=1 if i == 4 else 0,
              alarm=1 if i == 4 else 0, flash=0, pulse=0, strike=0, fall=0, grow=1, dimValue=0, slotFill=1,
              bulletOn=1, opacity=1, lite=1)
        kit.tick(f"brouillon_coche{i + 1}", sheet.pt(i, "tick"), AI_INK, size=100, sw=12, variant="ai", z=14.2,
                 parent="brouillon", draw=1, thin=12, boxSw=6)                # 40 px à l'échelle 0,4
    kit.shape("brouillon_bande", [round((X["slot0"] + X["slot1"]) / 2, 1), rows[4]], kind="round",
              w=X["slot1"] - X["slot0"] + 30, h=sheet.slot_h + 10, r=16, fill="none", stroke=RED, sw=16, shadow=0,
              z=14.15, parent="brouillon")
    for k, side in enumerate((-1, 1)):    # les deux moitiés du brouillon fendu, qui tombent sous le chemin (S19)
        kit.shape(f"moitie{k + 1}", [0, 0], kind="poly",
                  pts=[[0, -sheet.h / 2], [side * sheet.w / 2, -sheet.h / 2], [side * sheet.w / 2, sheet.h / 2],
                       [0, sheet.h / 2], [side * 24, 120], [-side * 18, 0], [side * 20, -140]],
                  fill=PAPER, stroke=AI_INK, sw=12, dash=[0.01, 22], shadow=12, z=14.3, scale=0)
    kit.shape("bande_rouge", [0, 0], kind="round", w=round((X["slot1"] - X["slot0"] + 30) * BROUILLON_S, 1),
              h=round((sheet.slot_h + 10) * BROUILLON_S, 1), r=8, fill="none", stroke=RED, sw=6, shadow=0, z=14.4,
              scale=0)

    # --- écran partagé (S20-S21) : séparateur, « Avant », « Après » ; réponse du client ---
    kit.shape("separateur", [0, 0], kind="poly", pts=[[SEP_X, SEP_Y0], [SEP_X, SEP_Y1]], closed=False, fill="none",
              stroke=INK, sw=4, shadow=0, z=20, draw=0)
    S.add("avant", "pill", z=21, text="Avant", w=round(text_width("Avant", 40, 600) + 56), h=72, size=40, weight=600,
          fill=PAPER)
    S.set("avant", pos=list(AVANT_AT), scale=0, opacity=1, text="Avant")
    S.add("apres", "pill", z=21, text="Après", w=round(text_width("Après", 40, 600) + 56), h=72, size=40, weight=600,
          fill=CYAN)
    S.set("apres", pos=list(APRES_AT), scale=0, opacity=1, text="Après")
    kit.shape("reponse_bulle", list(CLIENT_S19), kind="round", w=96, h=80, r=34, fill=PAPER, stroke=INK, sw=4, shadow=5,
              z=21.8, scale=0)                                              # S21 : la réponse du client, bulle de parole
    kit.shape("reponse", list(CLIENT_S19), kind="circle", w=56, fill=CYAN, stroke=INK, sw=4, shadow=0, z=22, scale=0)

    return SimpleNamespace(toi=toi, toi2=toi2, client=client, sheet=sheet, ai_h=ai_h, pub_h=pub_h, clock_h=clock_h,
                           dial_c=dial_c, dial_r=dial_r, brain_top=brain_top, brain_front=brain_front,
                           pub_head=pub_head, head_pill=head_pill, wire_a=wire_a, tag_cx=tag_cx, case_y=case_y,
                           bubble_p=bubble_p)


def build(S):
    kit = Kit(S)
    c = cast(S, kit)
    only = [p for p in os.environ.get("WTH_PARTS", "").split(",") if p]   # WTH_PARTS=p2 : cette partie seule
    for name in PARTS:
        if not only or name in only:
            importlib.import_module(f".{name}", __name__).part(S, kit, c)
