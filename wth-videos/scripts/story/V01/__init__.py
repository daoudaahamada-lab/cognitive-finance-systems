"""V01 « Préparer ton entretien client avec l’IA » : mise en scène Story, en paquet (une partie par fichier).

Storyboard : scripts/storyboards/V01.json (v3.2), version lisible scripts/storyboards/V01.md. Fil : un seul dossier,
celui du client de 9 h. objet_fil = `pastille` (pilule cyan « Client · 9 h » à pictogramme de personne) : elle est
toujours posée sur ce qui contient le dossier (pile, cadre, fenêtre, en-tête de la fiche), le client naît de son
pictogramme (S04, S13) et y rentre (S05, S15), puis elle devient le bouton « S’abonner » (S20).

Parties (scènes contiguës, coupées sur un changement de composition) :
- p1 : S01-S08, images 0-609. Le dossier dispersé, le temps qui fond, « 1 · Limiter » : cadre, outil scellé, mur.
- p2 : S09-S14, images 610-1238. Le mur des règles, « 2 · Exiger » (la fiche, la ligne inventée, les preuves),
  « 3 · Relire » (relecture, rature, question gardée, tampon).
- p3 : S15-S20, images 1239-1747. Passation et poids (planche), dix minutes de relecture, Avant / Après, fin.
ENTRY_P2 et ENTRY_P3 (plus bas) sont le contrat des raccords : la partie précédente finit exactement dans cet état,
la suivante l'épingle à first_frame - 1.

Ce fichier déclare TOUTE la distribution à son état de l'image 0 (cast) et les places communes ; chaque partie pose
ses temps forts (pN.py, def part(S, kit, c)). Exceptions : la carte de fin `fin` et son pointeur `fin_curseur`, que
kit.outro déclare lui-même (p3).

Tour de revue 1 (corrections) : composition S05-S09 agrandie et descendue (cadre x 150-800, y 410-1190 ; documents à
l'échelle 1 ; fenêtre de S08 à x 0,88 jusqu'à y 1205) ; le conseiller reste à l'écran de S05 à S09 (le curseur part
de son stylo, relié par un fil) ; IA grand public en verre gris cerné d'encre, tournée vers la fenêtre ; coches de
l'IA plus sombres et plus grandes ; planche, chemin et rendez-vous agrandis jusqu'à y ≈ 1250.

Ajouts au code partagé que cette mise en scène suppose (tous facultatifs, défauts inchangés) :
- pictogrammes `hourglass`, `clock9`, `chat`, `target`, `sign` ;
- window : pistes `bar`, `sealOn` / `sealDy`, `lockOn` / `lockDy`, paramètre `sealK` (sceau agrandi) ;
- doc : paramètres `fw`, `fh`, `fts`, `fdate` et piste `read` ;
- png : paramètres `tint` ('mono'), `outline`, `flip` (l'IA grand public) ;
- label : `tag.icon2` (« à poser au RDV » : mini-horloge + pictogramme du client) ;
- Figure : méthodes `hop`, `run`, `lean_to`, `scale_to`, `stow`, `unstow`, `set_z`.
"""
import importlib
import os
from types import SimpleNamespace

from pipeline.story import GEOM, POP, STYLE, text_width
from pipeline.story_kit import Figure, Kit, Sheet

PARTS = ["p1", "p2", "p3"]                      # S01-S08, S09-S14, S15-S20
ALERT_WORDS = {"fausse", "erreur"}              # karaoké en rouge (storyboard, typographie)
ACOUSTIC_SNAP = {"gap": 0.2, "window": 0.08}    # temps fort après un silence : calé sur l'attaque audible
# Découpes : aucun groupe qui ne dure qu'un éclair (« pas dans ») ni qui coupe une locution (« politique / interne »,
# « valent / mieux ») ; 4 mots au plus (« et à une date » : exception admise), tous sous 760 px.
CAPTION_GROUPS = [["pas dans le conseil"], ["et ta politique interne", "s’appliquent"],
                  ["Exige", "que chaque ligne", "renvoie à un document", "et à une date"],
                  ["c’est une question", "à poser au client"],
                  ["Dix minutes", "de relecture", "valent mieux", "qu’une erreur", "devant le client"]]

# ---------- couleurs (storyboard « style » = pipeline.story.STYLE) ----------
INK, CYAN, DEEP, LIGHT = STYLE["ink"], STYLE["cyan"], STYLE["deep"], STYLE["light"]
PAPER, GREY, RED, AI_TICK, BG = STYLE["paper"], STYLE["grey"], STYLE["red"], STYLE["ai_tick"], STYLE["bg"]


def mix(a, b, t):
    """Couleur hex à t de a vers b (t = 0 : a)."""
    ca, cb = (tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) for h in (a, b))
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(ca, cb))


INK_40 = mix(BG, INK, 0.40)       # contour des cartes de l'autre client
INK_25 = mix(BG, INK, 0.25)       # blocs de temps perdus (S04)
AI_INK = mix(BG, INK, 0.62)       # coches de l'IA : gris encre, 100 % (le gris ai_tick se lisait « case pâle »)

# ---------- mise en page (1080 x 1920) ----------
# Action entre x 40-940 et y 160-1270 ; sous-titres 1280-1380 ; haut 160 px et colonne x > 940 réservés à TikTok.
X_MIN, X_MAX, Y_MIN, Y_MAX = 40, 940, 160, 1270
CX = 540                    # axe de la colonne d'action
GROUND = 1230               # ligne de sol : pieds des figurines debout
MARKER_Y = 300              # repère 1-2-3 (S05-S15), et la barre de temps avant lui (S03-S04)
MARKER_LABEL, MARKER_DY, MARKER_GAP = 34, 68, 180   # légende 34 px (règle des 32 px), 6 px plus bas, disques à 180 px
FIG_BASE = GEOM["FIGURE"]["base"]   # 95 : du centre de la figurine à ses pieds (x échelle)


def fig_pos(x, feet=GROUND, s=1.0):
    """Centre d'une figurine d'échelle s dont les pieds sont sur la ligne y = feet (place à donner à walk / enter)."""
    return [x, round(feet - FIG_BASE * s, 2)]


def scene_f0(S, sid):
    """Première image de la scène sid (round(t_start x 30))."""
    return round(next(s for s in S.sb["scenes"] if s["id"] == sid)["t_start"] * S.fps)


def win_map(pt, pos, s, frame=None):
    """Point de la composition du cadre (S05-S07, centre FRAME_C, échelle 1) quand la fenêtre est en `pos` à l'échelle
    `s` (S08-S09 : WIN_S08) : ce qui est dans l'outil le suit."""
    c = frame or FRAME_C
    return [round(pos[0] + (pt[0] - c[0]) * s, 2), round(pos[1] + (pt[1] - c[1]) * s, 2)]


def vanish(kit, id, f, into=None, d=POP):
    """kit.vanish, plus un fondu d'opacité sur ses 3 dernières images : pas de point résiduel à taille téléphone."""
    end = kit.vanish(id, f, into=into, d=d)
    kit.S.key(id, "opacity", end - 3, 0, 3, "linear")
    return end


def morph_out(kit, outs, f, d=None):
    """kit.morph(outs, [], f) avec le fondu des 3 dernières images (aucun point résiduel)."""
    from pipeline.story import MORPH
    d = d or MORPH
    end = kit.morph(outs, [], f, d=d)
    for o in outs:
        kit.S.key(o, "opacity", end - 3, 0, 3, "linear")
    return end


# Pastille « Client · 9 h » (objet du fil)
PILL_TEXT, PILL_W, PILL_H = "Client · 9 h", 260, 56
PILL_ICON = [-PILL_W / 2 + 30, 0]           # pictogramme de personne de la pastille (repère de la pilule)
PASTILLE_S01 = (540, 890)                   # coiffe la pile (S01)

# Horloge de 9 h (WTH-003-01) : 440 px en S01, badge de 170 px (S02-S04), 352 px en S17
CLOCK_W = 440
CLOCK_S01 = (540, 560)
CLOCK_BADGE, CLOCK_BADGE_SCALE = (850, 300), 170 / CLOCK_W      # bout droit de la barre de temps
CLOCK_S17, CLOCK_S17_SCALE = (290, 660), 352 / CLOCK_W          # au-dessus de la fiche relue (S17)
DIAL = dict(cx=0.575, cy=0.375, rx=0.20, ry=0.245)              # cadran dans la boîte du PNG

# Documents du dossier : (titre, pictogramme, date en clair). Carte complète 200 x 250 ; compacte 150 x 80 (S11-S13).
DOCS = [("Avis d’impôt", "euro", "sept. 2025"), ("Relevé PEA", "bars", "mars 2026"),
        ("Mail client", "mail", "févr. 2026"), ("Assurance-vie", "shield", "déc. 2025")]
DOC_W, DOC_H, DOC_TITLE = 200, 250, 24
DOC_CW, DOC_CH = 150, 80
PILE_S01 = (540, 1010)                       # pile nette sous la pastille (S01)
DOC_SPOTS = [(160, 800), (825, 870), (160, 1080), (545, 1080)]  # 4 places (S01 « heures ? », S03 rembobinage)
DOC_TILTS = [-8, 6, -5, 7]
PILE_S02 = (540, 900)                        # pile rangée par l'IA (S02)
IA_S02, IA_S02_SCALE = (200, 1050), 1.1      # l'IA (200 px à l'échelle 1) entre par la gauche
ADV_S02 = fig_pos(745, 1200)                 # le conseiller surgit en bas à droite, pile à portée de stylo
PILE_TICK_S02 = (603, 972)                   # coin bas droit de la pile, à portée du stylo (S02 « décides. »)
# cartes « Client · 14 h » glissées ENTRE les documents, un coin sur l'un d'eux (storyboard : x 380 / 720, x 680 / 1000)
GREY_SPOTS = [(330, 740), (700, 660)]        # un coin sous doc1, un coin sous doc2 ; loin du conseiller (S02-S04)
GREY_Z = [11.95, 11.85]                      # entre les documents : sous doc1, sous doc2
GREY_PILL = dict(w=round(text_width("Client · 14 h", 34, 700) + 92), h=60, size=34)
GREY_EDGE_S05, GREY_EDGE_SCALE = [(872, 610), (872, 890)], 0.55   # bord droit, hors du cadre, x <= 940 (S05-S07)
DOC_GRID_S05, DOC_GRID_SCALE = [(475, 565), (685, 565), (475, 825), (685, 825)], 1.0   # 2 x 2 dans le cadre
PILE_S06, DOC_PILE_SCALE = (470, 760), 1.0   # pile décalée dans le cadre (S06-S09), à l'échelle 1
PILE_SLOT = [1, 2, 0, 3]                     # place de doc i dans la pile : « Mail client » dessus (S06-S12)


def pile_pt(c, slot, step=6):
    """Place `slot` d'une pile décalée centrée sur c (slot 0 dessus, en haut à gauche)."""
    return [c[0] - 1.5 * step + step * slot, c[1] - 1.5 * step + step * slot]


def pile_z(slot):
    return round(12 - 0.1 * slot, 2)


# Barre de temps (S03-S04) : 580 x 40, de x 180 à 760, fond par la gauche ; blocs de 22 %
BAR_X0, BAR_W, BAR_H = 180, 580, 40
BAR_C = (BAR_X0 + BAR_W / 2, MARKER_Y)
BLOCK = 0.22
BAR_STUB = 0.12                               # bout cyan restant contre l'horloge (S04)
CLIENT_S04, CLIENT_S04_SCALE = (795, 430), 0.7   # le client sous le bout cyan (S04 « conseil. »)
# sauts (S04) : au-dessus de doc2 (le plus proche), au-dessus de doc1, à droite de doc3, contre carte_grise2
S04_HOPS = [(870, 650), (160, 580), (335, 1110), (530, 650)]
ADV_RECOIL = (520, 740)                       # recul de 95 px, penché en arrière : mauvais dossier (pilules dégagées)

# Cadre puis fenêtre de l'outil (S05-S07) : x 150-800, y 410-1190 ; coin libre en bas à gauche pour l'IA
FRAME_C, FRAME_W, FRAME_H = (475, 800), 650, 780
FRAME_X0, FRAME_X1 = FRAME_C[0] - FRAME_W / 2, FRAME_C[0] + FRAME_W / 2
FRAME_TOP, FRAME_Y1 = FRAME_C[1] - FRAME_H / 2, FRAME_C[1] + FRAME_H / 2
TITLE_H = 64                                  # barre de titre (64 px : sceau agrandi)
SEAL_K = 1.25                                 # sceau x 1,25 : disque de 55 px, « Cabinet » à 32 px
SEAL_W = round(68 * SEAL_K + text_width("Cabinet", 26 * SEAL_K, 700) + 16 * SEAL_K)
IA_S05 = (262, 1000)                          # l'IA dans le coin libre, dans le cadre, pilule comprise
ADV_OUT = fig_pos(880)                        # conseiller dehors, en bas à droite (S05-S07)
TITLE_S07 = (FRAME_X0 + 90 + PILL_W / 2, FRAME_TOP + TITLE_H / 2)   # titre : la pastille, avant le cadenas
SEAL_S07 = (680, 1010)                        # le grand sceau tombe là, dans la fenêtre (libre), puis vole au titre
SEAL_SLOT = (FRAME_X1 - 12 - 23 * SEAL_K, FRAME_TOP + TITLE_H / 2)   # sceau fermé au bout de la barre (S07)
# S08-S09 : la fenêtre et son contenu se rangent à gauche (x 40 -> 612, échelle 0,88) ; tout ce qui est dedans suit
WIN_S08_POS, WIN_S08_SCALE = (326, 862), 0.88
WALL_X = round(WIN_S08_POS[0] + FRAME_W / 2 * WIN_S08_SCALE, 1)   # mur droit de la fenêtre (≈ 612)
MAIL_S08 = win_map(pile_pt(PILE_S06, 0), WIN_S08_POS, WIN_S08_SCALE)   # « Mail client », dessus de la pile
CHOC = (WALL_X, MAIL_S08[1])                   # le mail bute sur le mur (S08 « non ») ; les briques s'y posent (S09)
ADV_S08 = fig_pos(790)                         # conseiller dehors, en bas à droite de la fenêtre (S08-S09)
IA_PUB, IA_PUB_W, IA_PUB_SCALE = (820, 700), 180, 1.1   # IA grand public, hors de la fenêtre
# foule grise au-dessus de la tête, jamais sur le trajet des briques (x 507-717, y >= 578) ni au-delà de x 917
FOULE = dict(n=6, h=56, pts=[[-110, -150], [-60, -178], [-5, -190], [50, -180], [84, -140], [86, -80]])
BRICK_W, BRICK_H = 210, 96
BRICKS = [("RGPD", (WALL_X, CHOC[1])), ("Politique\ninterne", (WALL_X, CHOC[1] - BRICK_H))]

# S10 : la fenêtre s'élargit (x 80 -> 770, y 420 -> 1060) ; pile en haut à gauche, IA en bas à gauche, page vide
WIN_S10 = dict(pos=(490, 740), w=820, h=640)
PILE_S10, PILE_S10_SCALE = (260, 600), 0.8
IA_S10 = (240, 940)
PAGE_S10, PAGE_S10_SCALE = (640, 740), 0.6     # la commande : page vide 300 x 432 posée par le conseiller
ADV_REST = fig_pos(880)                        # coin de repos du conseiller : dehors, en bas à droite (S10-S11)

# Fiche (S11-S14) : 500 x 720, jamais sous l'échelle 0,85 tant qu'on la lit
PAGE_S11 = (540, 780)                          # au centre, échelle 1 : y 420-1140
PAGE_S12, PAGE_S12_SCALE = (320, 780), 0.95    # à gauche : les sources à droite (S12-S14)
BADGE = dict(pos=(170, 330), w=240, h=170, scale=0.55)   # la fenêtre en badge, en haut à gauche (S11-S12)
IA_S11 = (160, 1110)                           # l'IA en bas à gauche pendant qu'elle écrit (S11)
# l'IA rangée, petite et visible (S12-S14) : pilule à droite de la tête, à l'échelle 1 (contre-échelle)
IA_CORNER, IA_CORNER_SCALE = (104, 1190), 0.55
IA_PILL_CORNER = [130, 40]                     # pilule « IA » à droite de la tête (repère de l'IA)
ADV_S12 = (870, 760)                           # prise en main : à droite de la page, à mi-hauteur (centre)
CASE_X = 690                                   # colonne des cases-sources (S12-S13)
CASE_W, CASE_H = 150, 80
ADV_S13 = fig_pos(560)                         # à gauche de la colonne des sources : sous la case 5, l'ivoire reste vide
CLIENT_S13 = fig_pos(874)                      # face au conseiller, sous le côté ouvert de la bulle
BUBBLE_AT = (760, 860)                         # bulle « ? » décalée vers le client, queue sur la tête du conseiller
ADV_S14, ADV_S14_SCALE = (640, 860), 1.1

FICHE_LINES = [("Revenus 2024", "82 k€", "euro"), ("PEA", "46 k€", "bars"), ("Retraite", "à 62 ans", "hourglass"),
               ("Assurance-vie", "120 k€", "shield"), ("Horizon", "5 ans", "none")]   # L5 : née de la tête de l'IA
RDV_TEXT = "à poser au RDV"
TICK_AI = 46                                   # coche de l'IA : pointillés dans un carré tireté de 60 px
TICK_AI_THIN = 6.5                             # points de 6,5 px (gris encre plein)
TICK_HUMAN = round(0.78 * TICK_AI, 2)          # coche pleine du conseiller : exactement sur les pointillés de l'IA
TAG_SIZE, TAG_H = 30, 50                       # dates et étiquettes-sources : page cornée, 30 px
TAG_W = round(GEOM["TAG"]["textX"] + max(text_width(d[2], TAG_SIZE, 600) for d in DOCS) + 14)
TAG_ICON2 = 2 * GEOM["TAG"]["discR"] + 4       # second pictogramme d'une étiquette (tag.icon2)
TAG5_W = round(GEOM["TAG"]["textX"] + TAG_ICON2 + text_width(RDV_TEXT, TAG_SIZE, 600) + 14)
RDV9_TEXT = "RDV 9 h"                          # S19 : la source de L5 devient le rendez-vous (pictogramme du client)
TAG5B_W = round(GEOM["TAG"]["textX"] + text_width(RDV9_TEXT, TAG_SIZE, 600) + 14)
STAMP_TEXT, STAMP_W, STAMP_H, STAMP_SIZE = "PRÊT POUR LE RDV", 370, 66, 30
BUBBLE_BIG = dict(w=236, h=136, r=40, q=100, qx=0, px=60, ps=64, sw=5, shadow=6, gs=4)    # « ? » seul (glyph = 0)
BUBBLE_SMALL = dict(w=72, h=72, r=36, q=48, qx=0, px=27, ps=36, sw=4, shadow=4, gs=3)     # autocollant de 72 px

# S15-S16 : planche (trait du repère) agrandie, posée bas ; jetons, cercles
PLANK_AT, PLANK_W, PLANK_H = (535, 1140), 790, 16   # origine = haut du pivot ; dessus de la planche à y 1124 ;
# à 12°, le bout droit descend de 68 px : « Toi » reste au-dessus des sous-titres
IA_PLANK_X, IA_PLANK_SCALE = 230, 1.4          # l'IA sur le bout gauche : 280 px, son visage dégagé de la fiche
PAGE_PLANK_SCALE = 0.45
ADV_PLANK_SCALE = 1.3                           # le conseiller sur le bout droit
IA_GROUND, IA_GROUND_SCALE = (260, 1092), 0.85  # S16 « tu » : descend au sol, à gauche du pivot, derrière la planche
CIRCLE_X = [20, 100, 180]                       # cercles 1-2-3 posés à droite du pivot (repère local de la planche)
CIRCLE_D, CIRCLE_SIZE = 72, 34
TOKENS = [("Conseil", "chat"), ("Adéquation", "target"), ("Responsabilité", "sign")]
TOKEN_SIZE, TOKEN_H = 32, 72
TOKEN_W = round(text_width("Responsabilité", TOKEN_SIZE, 600) + 92)
TOKEN_X = 40                                    # centre de la pile de jetons (x local), à gauche du conseiller

# S17 : chemin, conseiller, fiche relue, fauteuils, brouillon
PATH_C, PATH_W = (510, 1150), 800              # chemin x 110 -> 910, dessus à y 1142
PATH_TOP = PATH_C[1] - 8
ADV_S17 = fig_pos(520, PATH_TOP)
IA_S17, IA_S17_SCALE = 115, 0.55               # l'IA reste au départ du chemin
PAGE_S17, PAGE_S17_SCALE = (300, PATH_TOP - 2 - 0.45 * 360), 0.45   # posée sur le chemin devant lui
CHAIRS_W = 800
CHAIRS_S17, CHAIRS_S17_SCALE = (765, PATH_TOP - 0.43 * 153), 0.43   # pieds sur le chemin, x 593-937
BROUILLON_SCALE = 0.4
CHAIRS_S18 = (540, 810)
AVANT_AT = (540, 290)                           # au-dessus de la bulle de la question (S19)

# ---------- raccords : état épinglé au début de p2 (image 609) et de p3 (image 1238) ----------
# Figurines exclues (jamais épinglées) : p2 et p3 les replacent par walk / enter, avec le garde-fou de SKILL.md.
_DOC_S08 = [win_map(pile_pt(PILE_S06, PILE_SLOT[i]), WIN_S08_POS, WIN_S08_SCALE) for i in range(4)]
ENTRY_P2 = {   # fin de S08 = etat_initial de S09 : fenêtre à gauche, mail revenu sur la pile, IA grand public entière
    "marqueur": {"pos": [CX, MARKER_Y], "scale": 1, "active": 0},
    "outil": {"pos": list(WIN_S08_POS), "scale": WIN_S08_SCALE, "w": FRAME_W, "h": FRAME_H, "opacity": 1,
              "bar": 1, "seal": 1, "sealOn": 1, "sealDy": 0, "lockOn": 0, "lockDy": 0, "lock": 0},
    **{f"doc{i + 1}": {"pos": _DOC_S08[i], "scale": round(DOC_PILE_SCALE * WIN_S08_SCALE, 4), "rot": 0,
                       "compact": 0, "read": 1, "opacity": 1} for i in range(4)},
    "pastille": {"pos": win_map(TITLE_S07, WIN_S08_POS, WIN_S08_SCALE), "scale": WIN_S08_SCALE, "opacity": 1},
    "ia": {"pos": win_map(IA_S05, WIN_S08_POS, WIN_S08_SCALE), "scale": WIN_S08_SCALE, "opacity": 1},
    "ia_pub": {"pos": list(IA_PUB), "scale": IA_PUB_SCALE, "opacity": 1},
    "impact2": {"scale": 1}, "mur_choc": {"scale": 0}, "attache": {"draw": 0},
    "horloge": {"scale": 0}, "barre": {"scale": 0}, "cadre": {"scale": 0}, "curseur": {"scale": 0},
    "carte_grise1": {"scale": 0}, "carte_grise2": {"scale": 0}, "sceau": {"scale": 0},
}
ENTRY_P3 = {   # fin de S14 = etat_initial de S15 : fiche tamponnée à gauche, IA petite dans le coin, repère sur 3
    "marqueur": {"pos": [CX, MARKER_Y], "scale": 1, "active": 2},
    "fiche": {"pos": list(PAGE_S12), "scale": PAGE_S12_SCALE, "opacity": 1},
    "pastille_fiche": {"opacity": 1},
    "L5": {"strike": 1, "fall": 1, "crack": 0, "red": 0, "alarm": 0, "bulletOn": 1},
    **{f"source{i + 1}": {"scale": 1, "tagged": 1, "lit": 1} for i in range(4)},
    "source5": {"scale": 1, "tagged": 1},
    **{f"coche{i + 1}": {"draw": 1} for i in range(4)},
    **{f"coche_ia{i + 1}": {"draw": 1, "opacity": 1} for i in range(4)},
    "coche_ia5": {"draw": 0.5},
    "autocollant": {"opacity": 1, "s": 1},
    "tampon": {"scale": 1, "opacity": 1, "handle": 0},
    "ia": {"pos": list(IA_CORNER), "scale": IA_CORNER_SCALE, "opacity": 1},
    "outil": {"scale": 0}, "bulle": {"scale": 0}, "question": {"scale": 0}, "surligneur": {"scale": 0},
    "puce5_alerte": {"opacity": 0}, "cadre5": {"opacity": 0},
    **{f"doc{i + 1}": {"opacity": 0} for i in range(4)},
}


def tag_geom(text, w=TAG_W, icon2=None):
    """Géométrie d'une page cornée (label tagged, doc.tag) : texte en clair, 30 px ; icon2 : second pictogramme."""
    return {"w": w, "h": TAG_H, "date": text, "size": TAG_SIZE, **({"icon2": icon2} if icon2 else {})}


def card_pts(w, h, fold):
    """Contour d'une carte au coin haut droit plié (shape poly)."""
    return [[-w / 2, -h / 2], [w / 2 - fold, -h / 2], [w / 2, -h / 2 + fold], [w / 2, h / 2], [-w / 2, h / 2]]


def short_pen(fig, S, length=90):
    """Stylo de ≈ 90 px (storyboard v3) au lieu de GEOM.PEN.len : paramètre `len` de l'entité pen (entities.md) et
    longueur que le rig utilise pour la pointe et l'allonge (Figure.pen_len). À appeler juste après Figure(...)."""
    fig.pen_len = length
    S.ents[fig.pen]["p"]["len"] = length


def impact_marks(kit, id, at, z=13.8, side=1, length=40, sw=6, color=INK):
    """3 traits d'impact encre de ≈ `length` px, en éventail du côté `side` (+1 : vers la droite) d'un point de choc ;
    un groupe (parent invisible) qui surgit d'un coup (pop) et peut rester comme une marque."""
    kit.shape(id, at, kind="circle", w=2, fill="none", stroke="none", sw=0, shadow=0, z=z, scale=0)
    for k, (a, b) in enumerate((([8, -14], [8 + length * 0.8, -14 - length * 0.6]), ([10, 0], [10 + length, 0]),
                                 ([8, 14], [8 + length * 0.8, 14 + length * 0.6]))):
        kit.shape(f"{id}_{k + 1}", [0, 0], kind="poly", pts=[[a[0] * side, a[1]], [b[0] * side, b[1]]], closed=False,
                  fill="none", stroke=color, sw=sw, shadow=0, z=z, parent=id)


# ---------- distribution ----------

def cast(S, kit):
    """Toute la distribution, à son état de l'image 0 : S01 montre seulement l'horloge de 9 h et la pile coiffée de
    la pastille. Ce qui arrive plus tard est déclaré à sa première place avec scale=0 (figurines : show=False)."""
    sheet = Sheet(n=5)                                   # fiche de V01 : 500 x 720, rangées -224 … 192
    rows, ty, ly, X = sheet.rows, sheet.ty, sheet.ly, sheet.x

    # --- repère 1-2-3 légendé (S05-S15) : naît de la barre de temps ; légende 34 px ---
    kit.steps_marker(["Limiter", "Exiger", "Relire"], id="marqueur", y=MARKER_Y, cx=CX, z=20, gap=MARKER_GAP)
    S.ents["marqueur"]["p"].update(labelSize=MARKER_LABEL, labelDy=MARKER_DY)
    S.set("marqueur", scale=0)

    # --- horloge de 9 h (PNG), secteur de 10 minutes et aiguille des minutes calés sur son cadran (S17) ---
    clk = S.png("WTH-003-01")
    clk_h = round(CLOCK_W * clk["h"] / clk["w"])
    S.add("horloge", "png", z=3, src=clk["src"], w=CLOCK_W, h=clk_h)
    S.set("horloge", pos=list(CLOCK_S01), scale=1, opacity=1)
    dial_c = [round((DIAL["cx"] - 0.5) * CLOCK_W, 1), round((DIAL["cy"] - 0.5) * clk_h, 1)]
    dial_r = round(DIAL["rx"] * CLOCK_W, 1)
    S.add("secteur", "sector", z=3.1, parent="horloge", r=dial_r, unit=60, face="none", fill=DEEP)
    S.set("secteur", pos=dial_c, sy=round(DIAL["ry"] * clk_h / (DIAL["rx"] * CLOCK_W), 4), start=50, value=0)
    # aiguille des minutes cyan profond : de :50 (rot -60°) à :00 (0°) avec le secteur ; cachée hors S17
    kit.shape("aiguille", dial_c, kind="poly", pts=[[0, 6], [0, -round(dial_r * 0.92, 1)]], closed=False, fill="none",
              stroke=DEEP, sw=7, shadow=0, z=3.2, parent="horloge", scale=0, rot=-60)

    # --- les 4 documents : pile nette sous la pastille (doc1 dessus) ---
    for i, (title, icon, date) in enumerate(DOCS):
        d = f"doc{i + 1}"
        S.add(d, "doc", z=12 - 0.1 * i, title=title, icon=icon, date=date, cw=DOC_CW, ch=DOC_CH, titleSize=26,
              tag=tag_geom(date), fw=DOC_W, fh=DOC_H, fts=DOC_TITLE, fdate=True)
        S.set(d, pos=pile_pt(PILE_S01, i), scale=1, rot=0, compact=0, tag=0, txt=1, read=0, sh=6 if i == 3 else 0,
              z=12 - 0.1 * i, opacity=1)
        # traits de vitesse du rembobinage (S03), du côté opposé au trajet vers sa place
        ux, uy = DOC_SPOTS[i][0] - PILE_S02[0], DOC_SPOTS[i][1] - PILE_S02[1]
        n = max(1e-6, (ux * ux + uy * uy) ** 0.5)
        ux, uy = ux / n, uy / n
        for j, off in enumerate((-16, 0, 16)):
            a = [round(-ux * 118 - uy * off, 1), round(-uy * 140 + ux * off, 1)]
            b = [round(a[0] - ux * 48, 1), round(a[1] - uy * 48, 1)]
            kit.shape(f"vitesse{i + 1}_{j + 1}", [0, 0], kind="poly", pts=[a, b], closed=False, fill="none",
                      stroke=INK, sw=4, shadow=0, z=11.9, parent=d, scale=0)

    # --- pastille « Client · 9 h » (monde : S01-S11, S18, S20) et son double posé sur l'en-tête de la fiche ---
    S.add("pastille", "pill", z=13.5, text=PILL_TEXT, w=PILL_W, h=PILL_H, size=28, weight=700, fill=CYAN, icon="person")
    S.set("pastille", pos=list(PASTILLE_S01), scale=1, opacity=1, text=PILL_TEXT, fill=CYAN, w=PILL_W)

    # --- cartes de l'autre client (S03-S07, S18-S19) : grises, sans pictogramme, pilule grise « Client · 14 h » ---
    for k, spot in enumerate(GREY_SPOTS):
        g = f"carte_grise{k + 1}"
        kit.shape(g, spot, kind="poly", pts=card_pts(DOC_W, DOC_H, 22), fill=GREY, stroke=INK_40, sw=4, shadow=6,
                  z=GREY_Z[k], scale=0)
        S.set(g, z=GREY_Z[k])
        S.add(f"{g}_pill", "pill", z=GREY_Z[k] + 0.01, parent=g, text="Client · 14 h", w=GREY_PILL["w"],
              h=GREY_PILL["h"], size=GREY_PILL["size"], weight=700, fill=GREY, stroke=INK_40, icon="person")
        S.set(f"{g}_pill", pos=[0, -DOC_H / 2], scale=1, opacity=1, z=GREY_Z[k] + 0.01)

    # --- l'IA (AI.png) : sa pilule, son éclat ; ses faisceaux en pointillés ---
    ai = S.png("AI", keep_largest=True)
    ia_w = 200
    ai_h = round(ia_w * ai["h"] / ai["w"])
    brain_top, brain_front = [-6, round(-0.44 * ai_h, 1)], [40, round(-0.28 * ai_h, 1)]   # cerveau de verre
    S.add("ia", "png", z=4, src=ai["src"], w=ia_w, h=ai_h, saturate=0.85,
          contact=dict(w=round(ia_w * 0.72), h=28, dy=4, blur=10, alpha=0.2))
    S.set("ia", pos=list(IA_S02), scale=0, opacity=1, z=4)                # entre par la gauche (S02, x 1,1 = 220 px)
    S.add("ia_pill", "pill", z=4.1, parent="ia", text="IA", w=round(text_width("IA", 30, 600) + 48), h=50, size=30,
          weight=600, fill=PAPER, sw=4, shadow=5)
    S.set("ia_pill", pos=[0, round(ai_h / 2 + 28, 1)], scale=1, opacity=1, z=4.1)
    S.add("ia_eclat", "burst", z=4.2, parent="ia", r0=26, r1=70, n=8, sw=6, color=DEEP, a0=-90)
    S.set("ia_eclat", pos=list(brain_front), p=0)
    beam = dict(color=DEEP, sw=7, dash=[0.01, 17])
    # S02 (range la pile), S06 (rayon qui bute), S10-S11 (lit, écrit), S15-S17 (pousse le brief, le brouillon)
    for wid in ("faisceau_range", "rayon", "faisceau_tete", "faisceau_passe"):
        S.add(wid, "wire", z=13, a={"id": "ia", "at": brain_front}, **beam)
        S.set(wid, draw=0, pb=[0, 0], via=[], sag=0, **{"from": 0})
    S.add("faisceau_lit", "wire", z=13, a={"id": "ia", "at": brain_top}, b={"id": "outil", "at": [-80, 85]}, **beam)
    S.set("faisceau_lit", draw=0, sag=0, **{"from": 0})
    S.add("faisceau", "wire", z=13, a={"id": "outil", "at": [80, 85]}, **beam)    # badge -> puce de la ligne (S11)
    S.set("faisceau", draw=0, pb=[0, 0], via=[], sag=0, **{"from": 0})
    # cône de lecture (S05-S06) : de la tête de l'IA vers les 4 documents, coupé net par le haut et la droite du cadre
    apex = [IA_S05[0] + brain_front[0], IA_S05[1] + brain_front[1]]
    fy0, fx1 = FRAME_TOP + 4, FRAME_X1 - 4
    cone = [[0, 0], [round(365 - apex[0], 1), round(fy0 - apex[1], 1)], [round(fx1 - apex[0], 1),
            round(fy0 - apex[1], 1)], [round(fx1 - apex[0], 1), round(960 - apex[1], 1)]]
    kit.shape("cone", apex, kind="poly", pts=cone, fill=LIGHT, stroke=DEEP, sw=4, dash=[0.01, 12], shadow=0, z=1.5,
              scale=0)
    S.set("cone", fillOp=0.7)

    # --- l'IA grand public (S08-S09) : AI.png en verre GRIS cerné d'encre, tournée vers la fenêtre ; foule reliée ---
    pub_h = round(IA_PUB_W * ai["h"] / ai["w"])
    S.add("ia_pub", "png", z=4, src=ai["src"], w=IA_PUB_W, h=pub_h, tint="mono", outline=3, flip=True,
          contact=dict(w=round(IA_PUB_W * 0.72), h=26, dy=4, blur=10, alpha=0.2))
    S.set("ia_pub", pos=list(IA_PUB), scale=0, opacity=1)
    kit.crowd("foule", [0, 0], show=0, link=0, z=3.9, parent="ia_pub", tone=INK_40, linkColor="ai_tick", **FOULE)
    pub_head = [0, round(-0.22 * pub_h, 1)]
    for k, pt in enumerate(FOULE["pts"]):       # chaque figurine envoie une carte grise dans la tête (S08 « IA »)
        kit.shape(f"colis{k + 1}", pt, kind="rect", w=24, h=30, fill=GREY, stroke=INK_40, sw=3, shadow=0, z=3.95,
                  parent="ia_pub", scale=0)
    S.add("ia_pub_pill", "pill", z=4.1, parent="ia_pub", text="IA grand public",
          w=round(text_width("IA grand public", 28, 600) + 44), h=50, size=28, weight=600, fill=GREY, sw=4, shadow=5)
    S.set("ia_pub_pill", pos=[-22, 190], scale=1, opacity=1)

    # --- le conseiller (« toi » : figurine encre, bras à longueur fixe, stylo de 90 px) et le client (papier) ---
    toi = Figure(kit, "toi", pos=fig_pos(940, 1200), show=False)          # entre par la droite en S02, pieds y 1200
    short_pen(toi, S)
    S.add("toi_pill", "pill", z=16.5, parent="toi", text="Toi", w=round(text_width("Toi", 30, 600) + 48), h=50,
          size=30, weight=600, fill=INK, color=PAPER, stroke=INK, shadow=5)
    S.set("toi_pill", pos=[0, FIG_BASE + 30], scale=0, opacity=1)       # sous ses pieds (S02, S16)
    client = Figure(kit, "client", pos=list(CLIENT_S04), variant="paper", tool=False, show=False)

    # --- S02-S04 : coche pleine sur la pile, rembobinage, barre de temps et ses blocs, traînées ---
    kit.tick("coche_pile", PILE_TICK_S02, DEEP, size=40, sw=8, z=13.6, draw=0)
    kit.icon("rembobine", (CX, 690), "rewind", disc=34, fill=INK, color=PAPER, s=40, z=21, scale=0)
    kit.gauge("barre", BAR_C, value=1, w=BAR_W, h=BAR_H, dir="left", z=5.5, scale=0)
    S.set("barre", fill=CYAN, w=BAR_W)                                  # hex : fondus possibles
    bw = BLOCK * BAR_W
    for k in range(4):
        kit.shape(f"bloc{k + 1}", [BAR_X0 + bw * (k + 0.5), MARKER_Y], kind="rect", w=round(bw, 1), h=BAR_H, fill=CYAN,
                  stroke=INK, sw=4, shadow=0, z=5.6, scale=0)
        S.set(f"bloc{k + 1}", fill=CYAN)                                  # cyan pendant la chute -> INK_25 à l'arrivée
        # traînée de chute du bloc : de sa place dans la barre à la carte fouillée (tirets cyan profond)
        S.add(f"chute{k + 1}", "wire", z=5.55, color=DEEP, sw=4, dash=[10, 9])
        S.set(f"chute{k + 1}", draw=0, pa=[0, 0], pb=[0, 0], sag=0, opacity=1, **{"from": 0})
    # bout cyan de 12 % contre l'horloge (S04 « pas ») : il devient le disque « 1 » du repère (S05)
    kit.shape("bout", [BAR_X0 + BAR_W * (1 - BAR_STUB / 2), MARKER_Y], kind="rect", w=round(BAR_STUB * BAR_W, 1),
              h=BAR_H, fill=CYAN, stroke=INK, sw=4, shadow=0, z=5.7, scale=0)
    # traînée du saut en cours seulement (tirets encre, pas les pointillés de l'IA), effacée au saut suivant
    hop_from = [list(ADV_S02)] + [list(p) for p in S04_HOPS[:-1]]
    for k, (a, b) in enumerate(zip(hop_from, S04_HOPS)):
        mid = [(a[0] + b[0]) / 2, min(a[1], b[1]) - 60]
        kit.curve(f"traine{k + 1}", [0, 0], [a, mid, list(b)], draw=0, color=INK, sw=4, dash=[12, 10], dot=False,
                  z=6.5)

    # --- S05-S07 : cadre en tirets ouvert par le stylo du conseiller, fenêtre de l'outil, sceau, impacts ---
    # le contour part du coin bas droit (stylo) et remonte : déclaré couché (w <-> h), tourné de -90° et retourné
    # (sy = -1), son tracé va bas droit -> haut droit -> haut gauche -> bas gauche -> bas droit ; la fin (coin bas
    # gauche) reste ouverte jusqu'à ce que l'IA y passe
    S.add("cadre", "case", z=1, w=FRAME_H, h=FRAME_W)
    S.set("cadre", pos=list(FRAME_C), scale=1, rot=-90, sy=-1, draw=0, opacity=1)
    S.add("outil", "window", z=1, titleH=TITLE_H, r=24, sealW=SEAL_W, sealText="Cabinet", sealK=SEAL_K)
    S.set("outil", pos=list(FRAME_C), w=FRAME_W, h=FRAME_H, scale=0, opacity=1, seal=0, lock=0,
          bar=0, sealOn=0, sealDy=0, lockOn=0, lockDy=0)                  # bar/seal*/lock* : variante opt-in
    # le grand sceau du cabinet (S07) : disque cyan de 96 px au bâtiment, coché en ivoire, puis rangé dans la barre
    kit.icon("sceau", SEAL_S07, "building", disc=48, fill=CYAN, color=INK, z=13.7, scale=0)
    kit.tick("coche_sceau", [8, 8], PAPER, size=34, sw=7, z=13.75, parent="sceau", draw=0)
    impact_marks(kit, "impact1", [FRAME_X1, 900])                          # rayon contre le cadre (S06)
    kit.shape("bosse", [FRAME_X1, 900], kind="poly", pts=[[0, -70], [12, 0], [0, 70]], closed=False, fill="none",
              stroke=DEEP, sw=6, shadow=0, z=1.2, scale=0)                # le bord encaisse : il se creuse de 12 px
    impact_marks(kit, "impact2", list(CHOC))                               # mail contre le mur (S08), reste marqué
    kit.shape("mur_choc", list(CHOC), kind="rect", w=12, h=150, fill=DEEP, stroke=DEEP, sw=0, shadow=0, z=13.6,
              scale=0)                                                    # le mur s'épaissit sous le choc

    # --- S08-S09 : curseur (la main du conseiller à l'écran) relié à son stylo, briques du mur ---
    kit.cursor("curseur", (700, 1040), z=30, scale=0)
    S.add("attache", "wire", z=29.5, a={"id": toi.pen, "at": [toi.pen_len, 0]}, b={"id": "curseur", "at": [0, 0]},
          color=INK, sw=3)
    S.set("attache", draw=0, sag=0, opacity=1, **{"from": 0})
    for k, (txt, at) in enumerate(BRICKS):
        b = f"brique{k + 1}"
        kit.shape(b, at, kind="round", w=BRICK_W, h=BRICK_H, r=8, fill=INK, stroke=INK, sw=4, shadow=6, z=18, scale=0)
        kit.text(f"{b}_txt", [28, 0], txt, size=28, weight=600, color=PAPER, z=18.1, parent=b, opacity=0, lh=1.05)
    # pictogrammes des règles : bouclier-cadenas (RGPD), bâtiment à colonnes du sceau « ✓ Cabinet » (politique interne)
    kit.icon("brique1_ico", [-62, 0], "shield", s=46, color=PAPER, sw=2.6, z=18.1, parent="brique1", opacity=0)
    kit.icon("brique1_cad", [-62, 4], "lock", s=20, color=PAPER, sw=2.4, z=18.15, parent="brique1", opacity=0)
    kit.icon("brique2_ico", [-70, 0], "building", s=44, color=PAPER, sw=2.6, z=18.1, parent="brique2", opacity=0)

    # --- S10 : pastilles d'information (une par document), la puce vide née de la tête de l'IA et sa traînée ---
    for i in range(4):
        S.add(f"puce{i + 1}", "bullet", z=13.2, icon=FICHE_LINES[i][2], r=GEOM["BULLET"]["r"])
        S.set(f"puce{i + 1}", pos=pile_pt(PILE_S10, PILE_SLOT[i]), scale=0, opacity=1)
    S.add("puce5", "bullet", z=13.2, icon="none", r=GEOM["BULLET"]["r"])
    S.set("puce5", pos=[IA_S10[0], 800], scale=0, opacity=1, alarm=0)
    for k, w in enumerate((12, 16, 20)):                 # bulles de pensée : de la tête de l'IA à la puce vide
        kit.shape(f"pensee{k + 1}", [0, 0], kind="circle", w=w, fill=PAPER, stroke=DEEP, sw=3, dash=[4, 4], shadow=0,
                  z=13.1, scale=0)

    # --- la fiche (page de commande S10 -> brief S11-S17 -> fiche du RDV S19 -> carte de fin S20) ---
    def sheen(dx, dy):
        return {"id": "reflet", "dx": dx, "dy": dy, "w": sheet.w, "h": sheet.h}
    S.add("reflet", "sheen", z=10, w=sheet.w, h=sheet.h, under=True)     # porteur du reflet « fluide… » (S11)
    S.set("reflet", p=0)
    S.add("fiche", "fiche", z=8, w=sheet.w, h=sheet.h, title="Brief", headerH=sheet.head,
          tabs=[r + ty for r in rows], tabX=X["bullet"], sheen=sheen(0, 0))
    S.set("fiche", pos=list(PAGE_S10), scale=0, opacity=1, **{f"tab{i}": 1 for i in range(5)})
    sheet.id, sheet.lines = "fiche", []
    for i, (k, v, icon) in enumerate(FICHE_LINES):
        lid = f"L{i + 1}"
        p = sheet.line_params(k, v, icon, sheen=sheen(0, rows[i]))
        S.add(lid, "line", z=9, parent="fiche", **p)
        S.set(lid, pos=[0, rows[i]], chars=0, red=0, crack=0, flash=0, pulse=0, alarm=0, strike=0, fall=0, grow=0,
              dimValue=0, slotFill=1, bulletOn=0, opacity=1)
        sheet.lines.append((lid, p))
    header_pill = [round(-sheet.w / 2 + 24 + PILL_W / 2, 1), round(-sheet.h / 2 + sheet.head / 2, 1)]
    S.add("pastille_fiche", "pill", z=12.5, parent="fiche", text=PILL_TEXT, w=PILL_W, h=PILL_H, size=28, weight=700,
          fill=CYAN, icon="person", sheen=sheen(*header_pill))
    S.set("pastille_fiche", pos=header_pill, scale=1, opacity=0, text=PILL_TEXT, fill=CYAN, w=PILL_W)
    slot_w = X["slot1"] - X["slot0"]
    kit.shape("surligneur", [round((X["slot0"] + X["slot1"]) / 2, 1), rows[4] + ty], kind="round", w=slot_w, h=48,
              r=12, fill=LIGHT, stroke=LIGHT, sw=0, shadow=0, z=8.5, parent="fiche", scale=0)
    S.set("surligneur", w=slot_w)
    for i in range(5):                       # coches de l'IA : pointillés gris encre dans un carré tireté (« ai »)
        kit.tick(f"coche_ia{i + 1}", sheet.pt(i, "tick"), AI_INK, size=TICK_AI, sw=8, variant="ai", z=11,
                 parent="fiche", draw=0, thin=TICK_AI_THIN, boxSw=3.5)
    for i in range(4):                       # coches pleines du conseiller, tracées sur celles de l'IA (S14)
        kit.tick(f"coche{i + 1}", sheet.pt(i, "tick"), DEEP, size=TICK_HUMAN, sw=8, z=11.2, parent="fiche", draw=0)
    # la coche pointillée de L5 chassée par le stylo (S14) : sans son carré, qui reste vide ; elle repart vers l'IA
    kit.tick("coche_ia5_vol", sheet.pt(4, "tick"), AI_INK, size=round(TICK_AI * 0.78, 2), sw=TICK_AI_THIN, z=11.1,
             parent="fiche", draw=1, dots=round(TICK_AI_THIN * 1.5, 2))
    S.set("coche_ia5_vol", opacity=0, z=11.1)
    # S11 « produire » : le pictogramme de chaque document voyage, par le faisceau, jusqu'à la puce de sa ligne
    for i in range(4):
        S.add(f"copie{i + 1}", "bullet", z=13.3, icon=FICHE_LINES[i][2], r=GEOM["BULLET"]["r"])
        S.set(f"copie{i + 1}", pos=[0, 0], scale=0, opacity=1)
    # S11 « fausse. » : la puce vide de L5 (relais, enfant de la fiche), ses ondes rouges, le contour rouge de la rangée
    bullet5 = [X["bullet"], rows[4] + ty]
    S.add("puce5_alerte", "bullet", z=9.6, parent="fiche", icon="none", r=GEOM["BULLET"]["r"])
    S.set("puce5_alerte", pos=bullet5, scale=1, opacity=0, alarm=0)
    for k in range(2):
        kit.shape(f"onde{k + 1}", bullet5, kind="circle", w=44, fill="none", stroke=RED, sw=5, shadow=0, z=9.55,
                  parent="fiche", scale=0)
    kit.shape("anneau5", bullet5, kind="circle", w=44, fill="none", stroke=RED, sw=5, shadow=0, z=9.62,
              parent="fiche", scale=0)                   # anneau rouge plein, x 1,3 : la puce suspecte
    kit.shape("cadre5", [round((X["slot0"] + X["slot1"]) / 2 + 2, 1), rows[4]], kind="round", w=slot_w + 52,
              h=sheet.slot_h + 8, r=18, fill="none", stroke=RED, sw=4, dash=[12, 8], shadow=0, z=9.5, parent="fiche",
              draw=0)
    S.set("cadre5", opacity=1)

    # --- preuves (S12-S14) : cases-sources, fils pleins, dates / étiquettes-sources, « à poser au RDV » ---
    def case_y(i):
        return round(PAGE_S12[1] + (rows[i] + ty) * PAGE_S12_SCALE, 1)
    for i in range(5):
        S.add(f"case{i + 1}", "case", z=5, w=CASE_W, h=CASE_H)
        S.set(f"case{i + 1}", pos=[CASE_X, case_y(i)], scale=1, draw=0, opacity=1)
    wire_a = [[X["value"] + 10, rows[i] + ty] for i in range(5)]          # le fil part du texte qu'il prouve
    for i in range(4):
        S.add(f"fil{i + 1}", "wire", z=11, a={"id": "fiche", "at": wire_a[i]}, b={"id": f"doc{i + 1}", "at": [0, 0]},
              color=DEEP, sw=5, dots=True)
        S.set(f"fil{i + 1}", draw=0, aAt=wire_a[i], sag=0, opacity=1, **{"from": 0})
    S.add("fil5", "wire", z=11, a={"id": "fiche", "at": wire_a[4]}, color=DEEP, sw=5, dots=True, dashAlt=[14, 11])
    S.set("fil5", draw=0, pb=[CASE_X - CASE_W / 2 + 2, case_y(4)], sag=0, dashed=0, opacity=1, **{"from": 0})
    tag_cx = round(X["value"] - TAG_W / 2, 1)
    for i in range(4):                       # page cornée datée en clair (tagged = 1 : jamais de calendrier)
        S.add(f"source{i + 1}", "label", z=12.6, parent="fiche", icon=DOCS[i][1], tag=tag_geom(DOCS[i][2]))
        S.set(f"source{i + 1}", pos=[tag_cx, rows[i] + ly], scale=0, pop=1, lit=0, tagged=1, flash=0, opacity=1)
    # « à poser au RDV » : mini-horloge sur 9 h + pictogramme du client (à ce client, à 9 h), puis « RDV 9 h » (S19)
    S.add("source5", "label", z=12.6, parent="fiche", icon="clock9", tag=tag_geom(RDV_TEXT, TAG5_W, icon2="person"))
    S.set("source5", pos=[round(X["value"] - TAG5_W / 2, 1), rows[4] + ly], scale=0, pop=1, lit=0, tagged=1, flash=0,
          opacity=1)
    S.add("source5b", "label", z=12.65, parent="fiche", icon="person", tag=tag_geom(RDV9_TEXT, TAG5B_W))
    S.set("source5b", pos=[round(X["value"] - TAG5B_W / 2, 1), rows[4] + ly], scale=0, pop=1, lit=1, tagged=1,
          flash=0, opacity=1)

    # --- la question : « ? », bulle du conseiller, autocollant ; tampon PRÊT POUR LE RDV ---
    S.add("question", "qmark", z=17)
    S.set("question", pos=list(BUBBLE_AT), scale=0, gs=110, opacity=1)
    head = [ADV_S13[0] + 4, ADV_S13[1] + GEOM["FIGURE"]["top"] - 6]      # haut de la tête du conseiller (S13)
    bubble_p = dict(big=BUBBLE_BIG, small=BUBBLE_SMALL, tail=[head[0] - BUBBLE_AT[0], head[1] - BUBBLE_AT[1]],
                    tailBase=[-96, -50])
    S.add("bulle", "bubble", z=14, **bubble_p)                            # aussi la question posée au RDV (S19)
    S.set("bulle", pos=list(BUBBLE_AT), scale=0, s=0, q=0, glyph=0, pulse=0, opacity=1, rot=0)
    S.add("autocollant", "bubble", z=11.6, parent="fiche", **bubble_p)    # posé sur la fiche (S14-S19)
    S.set("autocollant", pos=[X["bullet"] + 32, rows[4] + ly + 24], scale=1, s=1, q=1, glyph=0, pulse=0, opacity=0)
    S.add("tampon", "stamp", z=11.8, parent="fiche", text=STAMP_TEXT, w=STAMP_W, h=STAMP_H, size=STAMP_SIZE)
    S.set("tampon", pos=[20, 300], rot=-6, scale=0, handle=1, opacity=0)  # bas de la page, sous « à poser au RDV »

    # --- S15-S17 : planche (trait du repère), cercles -> jetons, chemin, fauteuils, horloge, brouillon ---
    kit.seesaw("planche", PLANK_AT, w=PLANK_W, h=PLANK_H, fill=INK, base=INK, baseW=70, baseH=60, ground=0, z=6,
               scale=0)
    for k in range(3):
        S.add(f"cercle{k + 1}", "pill", z=7, parent="planche", text=str(k + 1), w=CIRCLE_D, h=CIRCLE_D,
              size=CIRCLE_SIZE, weight=800, fill=PAPER)
        S.set(f"cercle{k + 1}", pos=kit.seat("planche", CIRCLE_X[k], CIRCLE_D), scale=0, opacity=1, fill=PAPER,
              text=str(k + 1))
        label, icon = TOKENS[k]
        # posé sur la planche, le chiffre s'efface sous le pictogramme du jeton (bulle, cible, signature)
        kit.icon(f"cercle{k + 1}_ico", [0, 0], icon, disc=round(CIRCLE_D / 2 - 4), fill=PAPER, color=DEEP, sw=2.6,
                 s=40, shadow=0, z=7.05, parent=f"cercle{k + 1}", opacity=0)
        S.add(f"jeton{k + 1}", "pill", z=7.1 + 0.01 * k, parent="planche", text=label, w=TOKEN_W, h=TOKEN_H,
              size=TOKEN_SIZE, weight=600, fill=LIGHT, icon=icon, iconColor=DEEP)
        x, y = kit.seat("planche", TOKEN_X, TOKEN_H)
        S.set(f"jeton{k + 1}", pos=[x, y - (TOKEN_H + 4) * k], scale=0, opacity=1, w=TOKEN_W, text=label)
    kit.shape("chemin", PATH_C, kind="round", w=PATH_W, h=16, r=8, fill=INK, stroke=INK, sw=4, shadow=6, z=6, scale=0)
    ch = S.png("WTH-003-08")
    S.add("fauteuils", "png", z=3.5, src=ch["src"], w=CHAIRS_W, h=round(CHAIRS_W * ch["h"] / ch["w"]), shadow=0.22)
    S.set("fauteuils", pos=list(CHAIRS_S17), scale=0, opacity=1)
    kit.tick("coche_relue", [PAGE_S17[0], PAGE_S17[1] - 150], DEEP, size=56, sw=9, z=13.6, draw=0)
    kit.tick("coche_table", [CHAIRS_S17[0], CHAIRS_S17[1] - 120], DEEP, size=56, sw=9, z=13.6, draw=0)
    # brouillon non relu de l'IA (S17) : la fiche de S11, contour tireté cyan 4 px, coches de l'IA, bande L5 rouge
    kit.shape("brouillon", [IA_S17, PATH_TOP - 120], kind="round", w=sheet.w, h=sheet.h, r=16, fill=PAPER,
              stroke=DEEP, sw=10, dash=[22, 14], shadow=0, z=14, scale=0)
    for i, (k, v, icon) in enumerate(FICHE_LINES):
        b = f"brouillon_L{i + 1}"
        S.add(b, "line", z=14.1, parent="brouillon", **sheet.line_params(k, v, icon))
        S.set(b, pos=[0, rows[i]], chars=len(k) + len(v), red=1 if i == 4 else 0, crack=1 if i == 4 else 0,
              alarm=1 if i == 4 else 0, flash=0, pulse=0, strike=0, fall=0, grow=0, dimValue=0, slotFill=1,
              bulletOn=1, opacity=1)
        kit.tick(f"brouillon_coche{i + 1}", sheet.pt(i, "tick"), AI_INK, size=TICK_AI, sw=8, variant="ai", z=14.2,
                 parent="brouillon", draw=1, thin=TICK_AI_THIN, boxSw=3.5)
    impact_marks(kit, "impact3", [0, 0], z=14.6, side=-1, length=44, sw=7)   # brouillon contre le stylo levé (S17)

    # --- S18-S19 : étiquette Avant -> Après, question posée, réponse du client dans sa bulle ---
    S.add("avant", "pill", z=21, text="Avant", w=200, h=72, size=40, weight=600, fill=PAPER)
    S.set("avant", pos=list(AVANT_AT), scale=0, opacity=1, text="Avant", fill=PAPER)   # -> « Après », fond cyan
    S.add("bulle_client", "bubble", z=21.5, big=dict(w=150, h=124, r=40, q=0, qx=0, px=0, ps=0, sw=5, shadow=6, gs=4),
          small=BUBBLE_SMALL, tail=[110, 150], tailBase=[20, 52])
    S.set("bulle_client", pos=[640, 500], scale=0, s=0, q=0, glyph=0, pulse=0, opacity=1)
    S.add("reponse", "bullet", z=22, icon="person", r=GEOM["BULLET"]["r"])
    S.set("reponse", pos=list(CHAIRS_S18), scale=0, opacity=1)

    return SimpleNamespace(toi=toi, client=client, sheet=sheet, ai_h=ai_h, pub_h=pub_h, clock_h=clk_h,
                           brain_top=brain_top, brain_front=brain_front, header_pill=header_pill, case_y=case_y,
                           wire_a=wire_a, tag_cx=tag_cx, pub_head=pub_head, bullet5=bullet5, dial_r=dial_r)


def build(S):
    kit = Kit(S)
    c = cast(S, kit)
    only = [p for p in os.environ.get("WTH_PARTS", "").split(",") if p]   # WTH_PARTS=p2 : cette partie seule
    for name in PARTS:
        if not only or name in only:
            importlib.import_module(f".{name}", __name__).part(S, kit, c)
