"""V05 « Ton agent IA a inventé une info » : mise en scène Story, en paquet (une partie par fichier).

Storyboard : scripts/storyboards/V05.json (v1, révisé après le test sans son, 22 scènes, 89 temps forts, 89,44 s),
version lisible scripts/storyboards/V05.md. Voix : build/V05/words.json (film : images 0-2684).
Fil : le brief du rendez-vous de 10 h. objet_fil = `pastille` (pilule cyan « Client · 10 h », pictogramme de
personne), posée sur l'en-tête du brief dès l'image 0 (enfant de la fiche : elle suit le brief dans tous ses états,
réduite en S13, à gauche en S17) ; en S19 « client. » elle quitte l'en-tête (relais `pastille_client`, même place
monde) et se pose au-dessus du client ; en S22 elle devient le bouton « S’abonner » (relais `pastille_btn`, sans
pictogramme ; kit.outro(..., btn_at=…)).

Parties (scènes contiguës, coupées sur un changement de composition) :
- p1 : S01-S08, images 0-952. L'IA écrit le brief depuis le dossier et comble les vides depuis son nuage (accroche),
  « Toi », le repère des 4 erreurs, la parade, le rembobinage (trois dates, choix au jugé), « 250 000 € » avec aplomb,
  la maison, l'alerte, les vides et leur origine (nuage), « 1 · Vides » : les fausses cartes bouchent les places.
- p2 : S09-S14, images 953-1751. « Toi » touche : les fausses cartes s'émiettent, les valeurs cassent ; « 2 · Source » :
  les fils (trois tendus, deux tombent) ; L5 surlignée et soulignée ; « 3 · Hypothèse » : morph, carte A, « Fait »,
  carte B, « ≠ », « Fait » -> « Hypothèse ».
- p3 : S15-S22, images 1752-2684. Morph retour, « 4 · Diagonale », coche hâtive ; relecture lente, « 12 000 € » sous
  « 120 000 € » ; correction, rangement, parade ; la rubrique « Informations non confirmées » ; les questions ; le
  client ; la réponse « sept. 2028 » ; fin standard, bouton touché du stylo.
ENTRY_P2 et ENTRY_P3 (plus bas) sont le contrat des raccords : la partie précédente finit exactement dans cet état,
la suivante l'épingle à seam(S, "S09") / seam(S, "S15") (kit.pin). Les figurines n'y sont jamais (walk / enter).

Distribution : TOUT est déclaré ici (cast), à son état de l'image 0 ; ce qui arrive plus tard a scale=0 (ou draw=0,
opacity=0, chars=0), les figurines show=False. Exception : la carte de fin `fin`, que kit.outro déclare (p3). Une
partie qui aurait besoin d'un élément de plus, utilisé dans elle seule, le déclare en tête de partie sous un id préfixé
(`p2_…`) et l'a fait disparaître avant sa dernière image.

Aucun type nouveau : les pilules en tirets (« Fait » / « Hypothèse ») et à texte sur deux lignes (la rubrique) sont
des shape round + text ; les cartes du dossier sont des shape + icon + text ; les valeurs tombées au sol sont des
entités `line` seules (même dessin rouge fissuré que dans le brief).

Grammaire propre à V05 (storyboard, style) :
- pointillés ai_tick = l'IA (faisceaux, traits d'extraction, coches variant « ai », nuage, puces, fausses cartes) ;
  trait plein deep = « Toi » ou la preuve (fils, coches pleines, soulignements, cadre de la rubrique).
- Une coche pleine de « Toi » se pose à la place de la coche de l'IA (colonne des coches, x 200 du brief) : au contact,
  la coche de l'IA de cette ligne est chassée (kit.drop out, h 52, dx 18, rot 35) ; sur les lignes cassées (L2, L4),
  les coches de l'IA restent jusqu'à ce que les lignes deviennent des questions (S19).
- Rouge : cadres autour des valeurs inventées (S02, S06), valeurs fissurées (S09 -> S21), « 120 000 € » et son zéro
  (S16 -> S17), disque d'alerte (S06 -> S07). Jamais sur l'IA, le dossier, les places vides ou le client.
- Dates en clair (« mars 2027 », « sept. 2028 ») ; nombres « 120 000 € » : U+202F entre les milliers, U+00A0 avant €.
"""
import importlib
import math
import os
from types import SimpleNamespace

from pipeline.story import GEOM, MORPH, POP, STYLE, text_width
from pipeline.story_kit import Figure, Kit, Sheet

PARTS = ["p1", "p2", "p3"]                      # S01-S08, S09-S14, S15-S22
ALERT_WORDS = {"inventée", "risque", "erreur", "erreurs", "fabriqué"}   # karaoké en rouge (storyboard, style ROUGE)
ACOUSTIC_SNAP = {"gap": 0.2, "window": 0.08}    # temps fort après un silence : calé sur l'attaque audible
CAPTION_GROUPS = [["chiffres dates", "noms montants"],   # S16 : « dates » puis « noms » seuls, centrés, de même
                  # largeur, se lisaient comme une surbrillance en retard (QA, image 2015)
                  ["Quand une donnée", "manque elle peut"], ["c’est un vrai risque"], ["Ça ne suffit pas"],
                  ["Une IA générative", "est conçue", "pour produire"], ["à éviter avant", "ton rendez-vous client"],
                  ["et il pourrait vendre"]]          # revue 1 : groupes d'un mot trop brefs, coupes du français

# ---------- couleurs (storyboard « style » = pipeline.story.STYLE) ----------
INK, CYAN, DEEP, LIGHT = STYLE["ink"], STYLE["cyan"], STYLE["deep"], STYLE["light"]
PAPER, RED, BG, AI_TICK = STYLE["paper"], STYLE["red"], STYLE["bg"], STYLE["ai_tick"]

# ---------- typographie française ----------
NBSP, NNBSP = " ", " "                 # insécable (avant « : », « € », dans « » ) ; fine (milliers)


def euros(n):
    """« 120 000 € » : milliers en espace fine insécable, espace insécable avant €."""
    return f"{n:,}".replace(",", NNBSP) + NBSP + "€"


def cle(mot):
    """« Vente : » (insécable avant les deux-points)."""
    return f"{mot}{NBSP}:"


def guil(t):
    """« t » avec insécables."""
    return f"«{NBSP}{t}{NBSP}»"


T_120, T_12, T_250 = euros(120000), euros(12000), euros(250000)
T_MARS, T_JUIN, T_JANV, T_SEPT = "mars 2027", "juin 2026", "janv. 2028", "sept. 2028"
PILL_TEXT = f"Client · 10{NBSP}h"               # « Client · 10 h » (comme le storyboard)
T_ABONNER = "S’abonner"
T_TITRE = "4 erreurs"
T_RUBRIQUE = f"«{NBSP}Informations\nnon confirmées{NBSP}»"   # deux lignes, Bold 34
QUESTIONS = ["Date de vente ?", "Montant du contrat ?", "Projet de vente ?"]   # L2, L4, L5 dans la rubrique
QUESTIONS = [q.replace(" ?", f"{NBSP}?") for q in QUESTIONS]
T_REPONSE_L2 = f"{cle('Vente')} {T_SEPT}"       # S21 : la première question devient « Vente : sept. 2028 »
T_VENDRE_Q = f"Vendre{NBSP}?"                   # S15 : L5 revient « Vendre ? »
T_CARTE_A0 = f"{cle('Projet')} vendre"          # S13 : la carte A naît de L5
T_CARTE_A = f"«{NBSP}Le client prévoit\nde vendre{NBSP}»"   # S14 (Bold 34, deux lignes)
T_CARTE_B = f"«{NBSP}il pourrait\nvendre{NBSP}»"
T_BULLE = f"Date de\nvente{NBSP}?"              # S21 : la question dans la bulle de « Toi » (Bold 28)
MARKER_LABELS = ["Vides", "Source", "Hypothèse", "Diagonale"]
TEXT_MIN = 32                                   # corps minimal d'un texte lu à l'échelle 1 (libellés : 26 au moins)

# ---------- mise en page (1080 x 1920) ----------
# Action entre x 40-940 et y 160-1270 ; composition de y ≈ 280 à y ≈ 1240 ; sous-titres 1280-1380.
X_MIN, X_MAX, Y_MIN, Y_MAX = 40, 940, 160, 1270
CX = 540                                        # axe de l'écran (repère, titre, carte de fin)
GROUND = 1230                                   # ligne de sol : pieds de « Toi » et du client
FIG_S = 0.9                                     # échelle des deux figurines
FIG_BASE = GEOM["FIGURE"]["base"]               # 95
FIG_TOP = GEOM["FIGURE"]["top"]                 # -96
PEN_LEN = 90                                    # stylo de 90 px (storyboard)


def fig_pos(x, feet=GROUND, s=FIG_S):
    """Centre d'une figurine d'échelle s dont les pieds sont sur y = feet."""
    return [x, round(feet - FIG_BASE * s, 2)]


def scene_f0(S, sid):
    """Première image de la scène sid (round(t_start x 30))."""
    return round(next(s for s in S.sb["scenes"] if s["id"] == sid)["t_start"] * S.fps)


def seam(S, sid):
    """Image d'épingle du raccord qui ouvre la scène sid : la plus tôt de son début et de son premier temps fort (calé
    sur l'attaque audible, il peut tomber avant le début de la scène), moins 1. Le temps fort n'est pas enregistré."""
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
    """kit.morph(outs, [], f) avec le fondu des 3 dernières images."""
    end = kit.morph(outs, [], f, d=d)
    for o in outs:
        kit.S.key(o, "opacity", end - 3, 0, 3, "linear")
    return end


def cloud_pts(w, h, bumps=9, amp=0.11, n=90):
    """Contour d'un nuage de pensée (shape poly) : ellipse w x h festonnée de `bumps` bosses."""
    pts = []
    for k in range(n):
        t = 2 * math.pi * k / n
        s = 1 - amp + amp * abs(math.sin(bumps * t / 2))
        pts.append([round(w / 2 * s * math.cos(t), 1), round(h / 2 * s * math.sin(t), 1)])
    return pts


def short_pen(fig, S, length=PEN_LEN):
    """Stylo de 90 px au lieu de GEOM.PEN.len : paramètre `len` du pen et longueur utilisée par le rig."""
    fig.pen_len = length
    S.ents[fig.pen]["p"]["len"] = length


def ring(S, id, f, d=18, s0=0.6, s1=1.6):
    """Onde d'impact : un cercle grandit de s0 à s1 en s'effaçant (d images). -> f + d."""
    S.key(id, "scale", f - 1, s0)
    S.key(id, "opacity", f - 1, 0)
    S.key(id, "opacity", f, 1)
    S.key(id, "scale", f, s1, d, "out")
    S.key(id, "opacity", f + 3, 0, d - 3, "linear")
    return f + d


# ---------- le brief (fiche) : Sheet(5), 500 x 720, rangées locales -224, -120, -16, 88, 192 ----------
SHEET = Sheet(n=5)
ROWS, TY = SHEET.rows, SHEET.ty                 # TY = -22 : ligne de texte d'une rangée (repère de la ligne)
X = SHEET.x                                     # bullet -248, text -206, value 150 (bord droit), tick 200
FICHE_C, FICHE_S = (560, 750), 0.95             # S01-S12, S15-S16 : x 322-798, y 408-1092 ; rangées monde y 537 …
FICHE_S13, FICHE_S13_S = (600, 975), 0.75      # S13-S14 : reculé en bas (x 412-788, y 705-1245)
FICHE_S17 = (380, 750)                          # S17-S22 : à gauche (x 142-618)
LINES = [(cle("Épargne"), T_120, "bars"), (cle("Vente"), T_MARS, "cal"), (cle("Notaire"), "Me Roux", "mail"),
         (cle("Contrat"), T_250, "shield"), (cle("Projet"), "vendre", "person")]   # pictogramme = source (S17)
LINE_IDS = [f"L{i + 1}" for i in range(5)]
VALUE_W = [round(text_width(v, 32, 600), 1) for _, v, _ in LINES]
VALUE_CX = [round(X["value"] - w / 2, 1) for w in VALUE_W]   # centre de la valeur (repère de la ligne)
VALUE_PT = [[cx, TY] for cx in VALUE_CX]        # point de la valeur (repère de la ligne : pos de la ligne = [0, row])
TICK_PT = [X["tick"], TY]                       # colonne des coches (repère de la ligne)
WIRE_X = X["text"] - 15                         # -221 : départ des fils, juste avant le texte (monde x ≈ 350)
WIRE_DY = 4                                     # … sous la puce et la ligne de texte (repère de la rangée)
CASE_VAL_W, CASE_VAL_H = 170, 44                # case de valeur vide en tirets (L2, L4), bord droit = bord de la valeur
CASE_VAL_PT = [X["value"] - CASE_VAL_W / 2, TY]
CADRE_W, CADRE_H = 190, 52                      # cadre rouge autour d'une valeur (L2, L4)
PASTILLE_LOCAL = [-90, round(-SHEET.h / 2 + SHEET.head / 2 + 2, 1)]    # en-tête, à gauche (monde (475, 448))
PASTILLE_LOCAL_S = round(1 / FICHE_S, 4)        # x 1 à l'écran sur la fiche x 0,95 (texte 32 px)
PILL_W, PILL_H, PILL_SIZE = 290, 60, TEXT_MIN
# S16 : le zéro de trop de « 120 000 € » (3e caractère, repère de la ligne L1) et la copie « 12 000 € » posée dessous,
# alignée à gauche (Bold 30), à mi-chemin entre L1 et L2
L1_LEFT = round(X["value"] - VALUE_W[0], 1)
ZERO_PT = [round(L1_LEFT + text_width("12", 32, 600) + text_width("0", 32, 600) / 2, 1), TY]
ZERO_R = 46                                     # diamètre du cercle rouge (lisible au téléphone)
COPIE_PT = [L1_LEFT, TY + 52]                   # ancre « start » de la copie (repère de L1) ; monde y ≈ 566
COPIE_SIZE = 32
COPIE_W = round(text_width(T_12, COPIE_SIZE, 700) + 28)
COPIE_C = [round(L1_LEFT + text_width(T_12, COPIE_SIZE, 700) / 2, 1), TY + 54]   # centre (texte aligné à gauche)
LOUPE_C, LOUPE_W, LOUPE_H, LOUPE_SIZE = (560, 1176), 470, 140, 52   # S16 : loupe de L1 (x 325-795, y 1106-1246)
# S18-S19 : la rallonge de page (enfant de la fiche, cachée dessous à l'image 0) ; le bas du brief descend à y 1240
RALLONGE_W, RALLONGE_H = 500, 158
RALLONGE_IN = [0, SHEET.h / 2 - RALLONGE_H / 2 - 4]          # cachée sous la page
RALLONGE_OUT = [0, round(SHEET.h / 2 + RALLONGE_H / 2 - 2, 1)]   # sortie : bas de la page monde 1240 (fiche en S17)
# S19-S21 : questions (enfants de L2, L4, L5, ligne de texte) et cases réponse (colonne des coches : monde x 592)
Q_PT = [X["text"], TY]
REP_PT = TICK_PT
REP_W = 36
RUBRIQUE_LINES_Y = [830, 905, 980]              # monde, S19 (fiche à (400, 750)) : L2, L4, L5 dans la rubrique
L3_S19_ROW = ROWS[1]                            # L3 remonte au rang 2 (S19)

# ---------- le dossier (chemise à gauche) : 5 places alignées sur les rangées du brief ----------
DOSSIER_C, DOSSIER_W, DOSSIER_H = (170, 745), 236, 540     # x 52-288, y 475-1015
DOSSIER_S13, DOSSIER_S13_S = (300, 1010), 0.6     # (revue 1 : le dossier se retire en S13-S14)
ONGLET_LOCAL = (-42, -275)                      # onglet « Dossier » (monde (128, 470))
ROW_WORLD = [round(FICHE_C[1] + r * FICHE_S, 1) for r in ROWS]   # 537, 636, 735, 834, 932
CARD_W, CARD_H = 206, 84                        # textes 32 px, 12 px de marge
CARD_LOCAL = [[0, round(y - DOSSIER_C[1], 1)] for y in ROW_WORLD]   # centres des places (repère du dossier)
CARD_IDS = ["doc_releve", "place_vente", "doc_mail", "place_contrat", "doc_cr"]   # dans l'ordre des rangées
CARD_WIRE_AT = [CARD_W / 2, round(WIRE_DY * FICHE_S, 1)]     # bord droit, à hauteur du départ des fils
DOCS = {"doc_releve": ("Relevé", "bars", T_12), "doc_mail": ("Mail", "mail", None),
        "doc_cr": ("Compte\nrendu", "person", None)}
PLACES = {"place_vente": ("Vente", "cal"), "place_contrat": ("Contrat", "shield")}
FANTOMES = {"fantome_vente": (T_MARS, -8, "place_vente"), "fantome_contrat": (T_250, 8, "place_contrat")}
FANTOME_W, FANTOME_H = 244, 84                  # fausses cartes : plus larges que les places, de travers (bourrées)
MAISON_LOCAL = (40, -335)                       # maison (pictogramme sur disque) sur le haut de la chemise (210, 410)
MAISON_VENTE = (98, -109)                       # S06 « c’est » : posée sur le bord droit de la place « Vente »

# ---------- l'IA (AI.png 130 px, de profil vers la droite), son nuage, ses puces ----------
IA_C, IA_W = (115, 1145), 130
IA_S17, IA_S17_S = (90, 1180), 0.6
NUAGE_C, NUAGE_W, NUAGE_H = (330, 1165), 210, 124
NUAGE_S04_C = (330, 1135)                       # S04 : le nuage agrandi monte (bas à 1230, loin des sous-titres)
NUAGE_S04_K = (270 / 210, 196 / 124)            # S04 : le nuage grandit à 270 x 196 (sx, sy)
PUCE_W, PUCE_H, PUCE_SIZE = 176, 44, 30
PUCES = {"puce_vente": T_MARS, "puce_contrat": T_250, "puce_date1": T_JUIN, "puce_date3": T_JANV}
PUCE_S02 = {"puce_vente": (330, 1140), "puce_contrat": (330, 1190)}   # dans le nuage (S02)
PUCE_DATES_S04 = [(330, 1076), (330, 1135), (330, 1194)]   # juin 2026, mars 2027 (= puce_vente), janv. 2028
REMBOBINER_C = (215, 1060)                      # ◀◀ (S04) : à gauche du brief, au-dessus du nuage
ALERTE_C = (875, 735)                           # S06 : disque d'alerte (72 px) à droite du brief, entre L2 et L4

TRACE_VIA = [(336, 700), (352, 890)]            # S07 : passage des traits dans la marge gauche du brief
MIETTES = 7                                     # S09 : miettes d'une fausse carte

# ---------- repère des 4 erreurs ----------
MARKER_Y = 300
TITRE_C = (CX, 222)

# ---------- « Toi » et le client ----------
TOI_REST = fig_pos(860)                         # (860, 1144.5) : repos, pieds sur y 1230 (bord droit < 940)
TOI_S09 = [885, 760]                            # S09-S11 : à droite du brief (place_for pour le placement exact)
TOI_S12 = [885, 880]                            # S12 : à hauteur de L5
TOI_S13 = [885, 670]                            # S13-S16
TOI_S19 = [790, 870]                            # S19 : s'approche de la rubrique
TOI_S19_REST = fig_pos(870)                     # S19-S22 : face au client (bord droit < 920)
TOI_PILL_LOCAL = [0, -150]                      # pilule « Toi » au-dessus de la tête (repère de la figurine)
CLIENT_C = fig_pos(712)                         # (712, 1144.5) : face à « Toi »
PASTILLE_CLIENT = (745, 1000)                   # S19-S22 : la pastille au-dessus de la tête du client (bord g. 629)
PASTILLE_CLIENT_S = 0.8

# ---------- S13-S15 : les deux formulations ----------
CARTE_W, CARTE_H = 540, 110
CARTE_A_C, CARTE_B_C = (470, 445), (470, 610)
NEQ_C = (470, 528)
CARTE_B_S12 = (470, 1168)                       # S12 : le compte rendu agrandi dans la bande basse (sa phrase)
CARTE_B_PARK, CARTE_B_PARK_S = (205, 880), 0.6  # S13 : rangé à gauche, à la place du dossier qui se retire
CARTE_TXT_X = -245                              # texte des cartes, ancré à gauche (repère de la carte)
CARTE_B_TXT_X = -195                            # carte B : pictogramme du compte rendu à gauche
LIGNE1_Y = round(-34 * 1.18 / 2, 1)             # première ligne d'un texte Bold 34 sur deux lignes
FAIT_C = (840, 445)
FAIT_W, HYP_W, PILL2_H = 156, 210, 56


def word_span(prefix, word, x0, size=34, weight=700):
    """(centre x, largeur) du mot `word` écrit après `prefix`, texte ancré à gauche en x0."""
    a = text_width(prefix, size, weight)
    w = text_width(word, size, weight)
    return round(x0 + a + w / 2, 1), round(w, 1)


PREVOIT = word_span(f"«{NBSP}Le client ", "prévoit", CARTE_TXT_X)
POURRAIT = word_span(f"«{NBSP}il ", "pourrait", CARTE_B_TXT_X)

# ---------- S15 : la diagonale ----------
DIAG_A, DIAG_B = (660, 500), (790, 800)

# ---------- S17-S21 : la parade, la rubrique, la bulle, la réponse ----------
PARADE_S03, PARADE_S17 = (560, 1045), (380, 1045)
PARADE_W, PARADE_H = 230, 60
BANDEAU_W, BANDEAU_H = 436, 96
BANDEAU_S18, BANDEAU_S19 = (380, 1056), (380, 738)
CADRE_RUB_S18 = ((380, 1122), 440, 228)         # (centre, w, h) : x 160-600, y 1008-1236
CADRE_RUB_S19 = ((380, 855), 436, 340)          # x 162-598, y 685-1025
SOL_VENTE, SOL_CONTRAT = (280, 1200), (460, 1205)   # S19 : valeurs cassées au sol (centre de la valeur)
BULLE_C = (830, 700)                            # S21 : dans la colonne libre à droite du brief (x 730-930)
BULLE_BIG = dict(w=200, h=120, r=36, q=60, qx=0, px=60, ps=40, sw=5, shadow=6, gs=3)
BULLE_SMALL = dict(w=72, h=72, r=36, q=40, qx=0, px=27, ps=30, sw=4, shadow=4, gs=3)
REPONSE_C = (712, 1120)
REPONSE_UP = (730, 870)                         # S21 : la réponse monte du client dans la colonne libre
REPONSE_W, REPONSE_H = 204, 54

# ---------- S22 : fin ----------
FIN_C = (CX, 760)
FIN_TAP = (690, 965)                            # coin bas droit du bouton : le stylo de « Toi » le touche

# ---------- raccords ----------
_OFF = lambda *ids: {i: {"scale": 0} for i in ids}   # noqa: E731
_FULL = [len(k) + len(v) for k, v, _ in LINES]

ENTRY_P2 = {   # fin de S08 = etat_initial de S09
    "fiche": {"pos": list(FICHE_C), "scale": FICHE_S, "opacity": 1},
    "pastille": {"pos": PASTILLE_LOCAL, "scale": PASTILLE_LOCAL_S, "opacity": 1},
    **{lid: {"pos": [0, ROWS[i]], "scale": 1, "opacity": 1, "chars": _FULL[i], "red": 0, "crack": 0, "bulletOn": 0}
       for i, lid in enumerate(LINE_IDS)},
    "L2_case": {"opacity": 0}, "L4_case": {"opacity": 0},
    "L2_cadre": {"draw": 1, "opacity": 1}, "L4_cadre": {"draw": 1, "opacity": 1},
    **{f"coche_ia{i + 1}": {"draw": 1, "opacity": 1} for i in range(5)},
    "dossier": {"pos": list(DOSSIER_C), "scale": 1, "opacity": 1},
    "maison": {"scale": 0},
    "fantome_vente": {"scale": 1, "rot": -8, "opacity": 1}, "fantome_contrat": {"scale": 1, "rot": 8, "opacity": 1},
    "toi_pill": {"scale": 1, "opacity": 1},
    "ia": {"pos": list(IA_C), "scale": 1, "opacity": 1},
    "marqueur": {"pos": [CX, MARKER_Y], "scale": 1, "on": 1, "active": 0},
    "titre_erreurs": {"scale": 1, "opacity": 1},
    "reflet": {"p": 0},
    **{w: {"draw": 0} for w in ("faisceau", "faisceau_contrat", "extrait1", "extrait3", "extrait5", "trace_vente",
                                "trace_contrat")},
    **{f"fil{i + 1}": {"draw": 0} for i in range(5)},
    **{w: {"draw": 0} for w in ("lien_vente", "lien_contrat", "eclair_vente", "eclair_contrat")},
    **_OFF("nuage", "bulle_rond1", "bulle_rond2", "bulle_rond3", "puce_vente", "puce_contrat", "puce_date1",
           "puce_date3", "cadre_choix", "rembobiner", "alerte", "parade", "picto1", "picto3", "picto5", "L2_vide",
           "L4_vide"),
}
ENTRY_P3 = {   # fin de S14 = etat_initial de S15 : brief et dossier réduits en bas, cartes A et B, « ≠ », Hypothèse
    "fiche": {"pos": list(FICHE_S13), "scale": FICHE_S13_S, "opacity": 1},
    "pastille": {"pos": PASTILLE_LOCAL, "scale": PASTILLE_LOCAL_S, "opacity": 1},
    "L1": {"chars": _FULL[0], "red": 0, "crack": 0, "bulletOn": 1}, "L3": {"chars": _FULL[2], "red": 0, "crack": 0,
                                                                         "bulletOn": 1},
    "L2": {"chars": _FULL[1], "red": 0, "crack": 1}, "L4": {"chars": _FULL[3], "red": 0, "crack": 1},
    "L5": {"chars": 0, "red": 0, "crack": 0, "bulletOn": 1},
    "L2_vide": {"scale": 1}, "L4_vide": {"scale": 1},
    "L2_cadre": {"opacity": 0}, "L4_cadre": {"opacity": 0},
    **{f"coche_ia{i + 1}": {"draw": 1, "opacity": 1} for i in range(5)},
    "L5_surligne": {"scale": 0}, "L5_souligne": {"draw": 0},
    "dossier": {"pos": list(DOSSIER_C), "scale": 0},
    "fil1": {"draw": 0}, "fil3": {"draw": 0}, "fil5": {"draw": 0},
    "fil2": {"opacity": 0}, "fil4": {"opacity": 0},
    "fantome_vente": {"scale": 0}, "fantome_contrat": {"scale": 0},
    "ia": {"pos": list(IA_C), "scale": 1, "opacity": 1},
    "marqueur": {"pos": [CX, MARKER_Y], "scale": 1, "on": 1, "active": 2},
    "titre_erreurs": {"scale": 1, "opacity": 1},
    "carteA": {"pos": list(CARTE_A_C), "scale": 1, "opacity": 1},
    "carteA_txt": {"text": T_CARTE_A, "chars": len(T_CARTE_A.replace("\n", ""))},
    "carteA_surligne": {"scale": 1}, "carteA_souligne": {"opacity": 0}, "carteA_souligne_t": {"opacity": 1},
    "carteA_tirets": {"opacity": 0}, "carteA_coche": {"draw": 0}, "carteA_q": {"scale": 1}, "carteB_q": {"scale": 1},
    "carteB": {"pos": list(CARTE_B_C), "scale": 1, "opacity": 1},
    "carteB_txt": {"chars": len(T_CARTE_B.replace("\n", ""))},
    "carteB_surligne": {"scale": 1}, "carteB_souligne": {"opacity": 1},
    "different": {"pos": list(NEQ_C), "scale": 1, "opacity": 1},
    "hypothese": {"pos": list(FAIT_C), "scale": 1, "opacity": 1},
    **_OFF("fait", "nuage", "alerte", "parade", "toi_pill", "L5_hyp", "maison"),
}


# ---------- distribution ----------

def cast(S, kit):
    """Toute la distribution, à son état de l'image 0 (S01) : le dossier à gauche (3 cartes, 2 places vides), le
    brief vierge au centre-droit avec la pastille sur son en-tête, l'IA en bas à gauche. Ce qui arrive plus tard est
    déclaré à sa première place avec scale=0 (draw=0, chars=0) ; les figurines show=False."""

    # --- le dossier : chemise, onglet, 3 cartes et 2 places vides alignées sur les rangées ; la maison ---
    kit.shape("dossier", list(DOSSIER_C), kind="round", w=DOSSIER_W, h=DOSSIER_H, r=18, fill=PAPER, stroke=INK, sw=4,
              shadow=6, z=3)
    S.add("dossier_onglet", "pill", z=3.2, parent="dossier", text="Dossier",
          w=round(text_width("Dossier", TEXT_MIN, 700) + 36), h=48, size=TEXT_MIN, weight=700, fill=LIGHT, shadow=4)
    S.set("dossier_onglet", pos=list(ONGLET_LOCAL), scale=1, opacity=1)
    tx = -CARD_W / 2 + 56                        # début des textes d'une carte (après le bandeau du pictogramme)
    for cid, at in zip(CARD_IDS, CARD_LOCAL):
        if cid in DOCS:                          # vraie carte : papier, bandeau light à pictogramme, titre (+ valeur)
            title, icon, val = DOCS[cid]
            kit.shape(cid, at, kind="round", w=CARD_W, h=CARD_H, r=12, fill=PAPER, stroke=INK, sw=4, shadow=5, z=3.4,
                      parent="dossier")
            kit.shape(f"{cid}_bandeau", [-CARD_W / 2 + 24, 0], kind="round", w=44, h=CARD_H - 4, r=10, fill=LIGHT,
                      stroke="none", sw=0, shadow=0, z=3.42, parent=cid)
            kit.icon(f"{cid}_ico", [-CARD_W / 2 + 24, 0], icon, s=30, color=INK, z=3.44, parent=cid)
            if val:
                kit.text(f"{cid}_txt", [tx, -18], title, size=TEXT_MIN, weight=600, anchor="start", z=3.44,
                         parent=cid)
                kit.text(f"{cid}_val", [tx, 19], val, size=TEXT_MIN, weight=700, anchor="start", z=3.44,
                         parent=cid)
            else:
                kit.text(f"{cid}_txt", [tx, 0], title, size=TEXT_MIN, weight=600, anchor="start", z=3.44,
                         parent=cid, lh=1.0)
        else:                                    # place vide : tirets encre épais, pictogramme et nom de ce qui manque
            title, icon = PLACES[cid]
            kit.shape(cid, at, kind="round", w=CARD_W, h=CARD_H, r=12, fill="none", stroke=INK, sw=5, dash=[12, 9],
                      shadow=0, z=3.4, parent="dossier")
            kit.shape(f"{cid}_hi", [0, 0], kind="round", w=CARD_W, h=CARD_H, r=12, fill="none", stroke=INK, sw=9,
                      dash=[12, 9], shadow=0, z=3.41, parent=cid, opacity=0)      # S07 : le contour s'épaissit
            kit.icon(f"{cid}_ico", [-CARD_W / 2 + 24, 0], icon, s=30, color=INK, z=3.44, parent=cid)
            kit.text(f"{cid}_txt", [tx, 0], title, size=TEXT_MIN, weight=600, anchor="start", z=3.44,
                     parent=cid)
    # la maison du client (S06) : pictogramme encre sur disque papier, posé sur la chemise, puis sur la place « Vente »
    kit.icon("maison", list(MAISON_LOCAL), "house", disc=42, s=54, fill=PAPER, color=INK, shadow=5, z=3.6,
             parent="dossier", scale=0)

    # --- les fausses cartes de l'IA (S08-S09) : papier opaque, tirets pointillés ai_tick épais, de travers, valeur à
    #     l'encre ; la coche pointillée de l'IA à la place du pictogramme d'un vrai document ---
    for fid, (txt, rot, place) in FANTOMES.items():
        at = CARD_LOCAL[CARD_IDS.index(place)]
        kit.shape(fid, [DOSSIER_C[0] + at[0] + 8, DOSSIER_C[1] + at[1]], kind="round", w=FANTOME_W, h=FANTOME_H,
                  r=12, fill=PAPER, stroke=AI_TICK, sw=5, dash=[0.01, 10], shadow=4, z=3.7, scale=0)
        S.set(fid, rot=rot)
        # contrôle sans son : la coche se lisait « document » ; un petit nuage pointillé (celui de l'IA) dit d'où
        # vient la carte, à la place du pictogramme d'un vrai document
        kit.shape(f"{fid}_bandeau", [-FANTOME_W / 2 + 28, 0], kind="round", w=48, h=FANTOME_H - 8, r=10,
                  fill=STYLE["grey"], stroke="none", sw=0, shadow=0, z=3.71, parent=fid)
        kit.shape(f"{fid}_ia", [-FANTOME_W / 2 + 28, 1], kind="poly", pts=cloud_pts(42, 32, bumps=7, amp=0.2),
                  fill=AI_TICK, stroke="none", sw=0, shadow=0, z=3.72, parent=fid)
        kit.text(f"{fid}_txt", [-FANTOME_W / 2 + 60, 1], txt, size=TEXT_MIN, weight=700, anchor="start", z=3.75,
                 parent=fid)

    # --- le brief : page, reflet (sous les textes), pastille, 5 rangées vides ---
    def sheen(dx, dy):
        return {"id": "reflet", "dx": dx, "dy": dy, "w": SHEET.w, "h": SHEET.h}
    S.add("reflet", "sheen", z=10, w=SHEET.w, h=SHEET.h, under=True)
    S.set("reflet", p=0)
    S.add("fiche", "fiche", z=8, w=SHEET.w, h=SHEET.h, title="Brief", headerH=SHEET.head, tabs=[], tabX=X["bullet"],
          sheen=sheen(0, 0))
    S.set("fiche", pos=list(FICHE_C), scale=FICHE_S, opacity=1, lite=0)
    SHEET.id, SHEET.lines = "fiche", []
    for i, (k, v, icon) in enumerate(LINES):
        lid = LINE_IDS[i]
        p = SHEET.line_params(k, v, icon, sheen=sheen(0, ROWS[i]), keyW=round(text_width(k, 32, 600), 1))
        S.add(lid, "line", z=9, parent="fiche", **p)
        S.set(lid, pos=[0, ROWS[i]], scale=1, chars=0, red=0, crack=0, flash=0, pulse=0, alarm=0, strike=0, fall=0,
              grow=0, dimValue=0, slotFill=1, bulletOn=0, opacity=1, lite=0)
        SHEET.lines.append((lid, p))
    S.add("pastille", "pill", z=12.5, parent="fiche", text=PILL_TEXT, w=PILL_W, h=PILL_H, size=PILL_SIZE, weight=700,
          fill=CYAN, icon="person", sheen=sheen(*PASTILLE_LOCAL))
    S.set("pastille", pos=list(PASTILLE_LOCAL), scale=PASTILLE_LOCAL_S, opacity=1, text=PILL_TEXT)
    kit.shape("rallonge", list(RALLONGE_IN), kind="round", w=RALLONGE_W, h=RALLONGE_H, r=16, fill=PAPER, stroke=INK,
              sw=4, shadow=8, z=7.9, parent="fiche", scale=0)

    # --- dans les rangées (enfants des lignes : ils suivent la ligne jusque dans la rubrique) ---
    for i, lid in enumerate(LINE_IDS):
        # coche de l'IA (pointillés dans un carré tireté) ; coche pleine de « Toi » (L1, L3)
        kit.tick(f"coche_ia{i + 1}", TICK_PT, AI_TICK, size=40, sw=8, variant="ai", z=11.5, parent=lid, draw=0,
                 thin=6, boxSw=3.5, boxFill=PAPER)
    kit.tick("coche_hate", [TICK_PT[0] + 10, TICK_PT[1] - 4], DEEP, size=48, sw=8, z=11.6, parent="L1", draw=0)
    S.set("coche_hate", rot=-15)                 # S15 : coche trop rapide, grande, de travers, qui déborde
    kit.tick("coche1", TICK_PT, DEEP, size=40, sw=8, z=11.6, parent="L1", draw=0)        # S17 : L1 corrigée
    kit.tick("coche3", TICK_PT, DEEP, size=40, sw=8, z=11.6, parent="L3", draw=0)        # S16 : « noms, »
    for i in (1, 3):                             # L2, L4 : case de valeur vide en tirets ; cadre rouge
        lid = LINE_IDS[i]
        kit.shape(f"{lid}_case", list(CASE_VAL_PT), kind="round", w=CASE_VAL_W, h=CASE_VAL_H, r=8, fill="none",
                  stroke=INK, sw=3, dash=[10, 8], shadow=0, z=9.2, parent=lid, opacity=0)
        kit.shape(f"{lid}_cadre", list(VALUE_PT[i]), kind="round", w=CADRE_W, h=CADRE_H, r=3, fill="none",
                  stroke=RED, sw=3, shadow=0, z=9.3, parent=lid, draw=0)
        # S11 : pas de document -> case de pictogramme vide en tirets, à la place de la puce
        kit.shape(f"{lid}_vide", [X["bullet"], TY], kind="round", w=42, h=42, r=9, fill=PAPER, stroke=INK, sw=4,
                  dash=[8, 6], shadow=0, z=9.3, parent=lid, scale=0)
    for i in (1, 2, 3):                          # S16 : surligneur light sous la valeur (L2 dates, L3 noms, L4 montants)
        lid = LINE_IDS[i]
        kit.shape(f"{lid}_surligne", list(VALUE_PT[i]), kind="round", w=round(VALUE_W[i] + 16), h=40, r=8,
                  fill=LIGHT, stroke="none", sw=0, shadow=0, z=8.95, parent=lid, scale=0)
    # S12 : L5 surlignée (toute la ligne) puis soulignée (trait plein deep 4 px)
    l5_x0, l5_x1 = X["text"] - 8, X["value"] + 8
    kit.shape("L5_surligne", [round((l5_x0 + l5_x1) / 2, 1), TY], kind="round", w=round(l5_x1 - l5_x0), h=44, r=10,
              fill=LIGHT, stroke="none", sw=0, shadow=0, z=8.95, parent="L5", scale=0)
    v5_x0 = round(X["value"] - VALUE_W[4] - 2, 1)          # « vendre » seul : le stylo l'atteint de la droite
    kit.shape("L5_souligne", [0, TY + 24], kind="poly", pts=[[v5_x0, 0], [l5_x1, 0]], closed=False, fill="none",
              stroke=DEEP, sw=5, shadow=0, z=9.4, parent="L5", draw=0)
    # S15 : « Vendre ? » garde le soulignement en tirets de l'hypothèse
    vq_w = round(text_width(T_VENDRE_Q, 32, 600), 1)
    kit.shape("L5_tirets", [0, TY + 24], kind="poly", pts=[[Q_PT[0], 0], [round(Q_PT[0] + vq_w, 1), 0]],
              closed=False, fill="none", stroke=DEEP, sw=5, dash=[10, 8], shadow=0, z=9.4, parent="L5", opacity=0)
    # S15 : L5 revient « Vendre ? » + petite pilule « Hypothèse » en tirets dans la colonne des valeurs
    kit.text("L5_vendre", list(Q_PT), T_VENDRE_Q, size=32, weight=600, anchor="start", z=9.5, parent="L5", typed=True)
    hyp_w = round(text_width("Hypothèse", TEXT_MIN, 700) + 28)
    kit.shape("L5_hyp", [round(X["value"] - hyp_w / 2 - 2, 1), TY], kind="round", w=hyp_w, h=46, r=23, fill=PAPER,
              stroke=DEEP, sw=4, dash=[8, 6], shadow=0, z=9.6, parent="L5", scale=0)
    kit.text("L5_hyp_txt", [0, 1], "Hypothèse", size=TEXT_MIN, weight=700, z=9.65, parent="L5_hyp")
    # S16 : cercle rouge autour du zéro de trop ; copie « 12 000 € » du relevé (glisse le long de fil1, enfant de L1)
    kit.shape("cercle_zero", list(ZERO_PT), kind="circle", w=ZERO_R, fill="none", stroke=RED, sw=5, shadow=0,
              z=9.7, parent="L1", draw=0)
    # la copie « 12 000 € » voyage sur une pastille papier (au-dessus des fils) ; à l'arrivée la pastille s'efface et
    # le texte devient la valeur de L1
    kit.shape("copie_releve", list(COPIE_C), kind="round", w=COPIE_W, h=46, r=23, fill=PAPER, stroke=INK, sw=3,
              shadow=3, z=11.2, parent="L1", scale=0, draw=1)
    S.set("copie_releve", fillOp=1)
    kit.text("copie_releve_txt", [0, 1], T_12, size=COPIE_SIZE, weight=700, z=11.25, parent="copie_releve")
    # S16 : la loupe de L1 dans la bande basse : « 120 000 € » au-dessus de « 12 000 € » (relevé), chiffres alignés
    kit.shape("loupe", list(LOUPE_C), kind="round", w=LOUPE_W, h=LOUPE_H, r=18, fill=PAPER, stroke=INK, sw=4,
              shadow=6, z=12.2, scale=0)
    lx = -LOUPE_W / 2 + 92
    kit.text("loupe_haut", [lx, -32], T_120, size=LOUPE_SIZE, weight=700, anchor="start", z=12.3, parent="loupe")
    kit.text("loupe_bas", [lx, 34], T_12, size=LOUPE_SIZE, weight=700, anchor="start", color=DEEP, z=12.3,
             parent="loupe")
    kit.icon("loupe_ico_bas", [-LOUPE_W / 2 + 46, 34], "bars", disc=22, s=26, fill=CYAN, color=INK, shadow=0,
             z=12.3, parent="loupe")
    zx = lx + text_width("12", LOUPE_SIZE, 700) + text_width("0", LOUPE_SIZE, 700) / 2
    kit.shape("loupe_zero", [round(zx, 1), -32], kind="circle", w=64, fill="none", stroke=RED, sw=6, shadow=0,
              z=12.4, parent="loupe", draw=0)
    # S19-S21 : les questions (même ligne de texte) et leurs cases réponse
    for lid, q in zip(("L2", "L4", "L5"), QUESTIONS):
        kit.text(f"{lid}_q", list(Q_PT), q, size=32, weight=700, anchor="start", z=9.5, parent=lid, typed=True,
                 markColor=LIGHT)
        S.set(f"{lid}_q", mark=0, text=q)
        kit.shape(f"{lid}_rep", list(REP_PT), kind="rect", w=REP_W, h=REP_W, fill=PAPER, stroke=DEEP, sw=4, shadow=0,
                  z=9.6, parent=lid, scale=0)
        S.set(f"{lid}_rep", fill=PAPER)          # hex : la case se remplit de cyan en fondu (S21)

    # --- les valeurs cassées tombées au sol (S19-S21) : lignes seules, rouges et fissurées, inclinées ---
    for sid, (cx, cy), (k, v, _) in (("sol_vente", SOL_VENTE, LINES[1]), ("sol_contrat", SOL_CONTRAT, LINES[3])):
        p = SHEET.line_params("", v, "none")
        S.add(sid, "line", z=12, **p)                # au-dessus de la page : la chute se voit
        S.set(sid, pos=[round(cx - (X["value"] - p["valueW"] / 2), 1), round(cy - TY, 1)], scale=0, rot=8, chars=len(v),
              red=1, crack=1, flash=0, pulse=0, alarm=0, strike=0, fall=0, grow=0, dimValue=0, slotFill=0, bulletOn=0,
              opacity=1, lite=0)

    # --- les fils de source (deep, plein, point à chaque bout) : du début de la ligne vers sa carte / sa place ---
    for i in range(5):
        a = {"id": "fiche", "at": [WIRE_X, ROWS[i] + WIRE_DY]}
        b = {"id": CARD_IDS[i], "at": list(CARD_WIRE_AT)}
        S.add(f"fil{i + 1}", "wire", z=11, a=a, b=b, color=DEEP, sw=5, dots=True)
        S.set(f"fil{i + 1}", draw=0, sag=0, opacity=1, aAt=list(a["at"]), bAt=list(b["at"]), **{"from": 0})
        if i in (0, 2, 4):                       # S12 : les fils sourcés « s'épaississent » (doublon épais qui bat)
            S.add(f"fil{i + 1}_halo", "wire", z=10.9, a=a, b=b, color=DEEP, sw=9)
            S.set(f"fil{i + 1}_halo", draw=1, sag=0, opacity=0, **{"from": 0})
            # S11 : le pictogramme du document revient le long du fil jusqu'à la puce de la rangée (cyan, comme elle)
            kit.icon(f"picto{i + 1}", [0, 0], LINES[i][2], disc=22, s=28, fill=CYAN, color=INK, shadow=3, z=11.4,
                     scale=0)
    # S09 : la seule « preuve » de la valeur inventée est la fausse carte (pointillés de l'IA, sous le texte de la
    # rangée) ; au toucher du stylo, un éclair plein deep file de la valeur à la place vide
    for k, (lid, fid, place) in enumerate((("L2", "fantome_vente", "place_vente"),
                                           ("L4", "fantome_contrat", "place_contrat"))):
        i = LINE_IDS.index(lid)
        S.add(("lien_vente", "lien_contrat")[k], "wire", z=11, a={"id": lid, "at": [round(VALUE_CX[i] - VALUE_W[i] / 2 - 6, 1), 12]},
              b={"id": fid, "at": [FANTOME_W / 2 - 4, 0]}, color=AI_TICK, sw=5, dash=[0.01, 11], dots=True)
        S.set(("lien_vente", "lien_contrat")[k], draw=0, sag=0, opacity=1, **{"from": 0})
        S.add(("eclair_vente", "eclair_contrat")[k], "wire", z=11.1, a={"id": lid, "at": [X["value"] - 14, 12]},
              b={"id": place, "at": [CARD_W / 2, 0]}, color=DEEP, sw=6, dots=True)
        S.set(("eclair_vente", "eclair_contrat")[k], draw=0, sag=0, opacity=1, **{"from": 0})
    # S02 « info » : l'IA cherche la preuve de « mars 2027 » : un faisceau pointillé file de la valeur à la place
    #     « Vente », la trouve vide et rentre bredouille
    S.add("p1_cherche", "wire", z=11, a={"id": "L2", "at": [round(VALUE_CX[1] - VALUE_W[1] / 2 - 6, 1), 12]},
          b={"id": "place_vente", "at": [CARD_W / 2 - 6, 0]}, color=AI_TICK, sw=5, dash=[0.01, 11], dots=True)
    S.set("p1_cherche", draw=0, sag=0, opacity=1, **{"from": 0})
    # S09 : les miettes de la fausse carte (papier, contour pointillé de l'IA) qui tombent jusqu'au sol
    for fid in FANTOMES:
        for k in range(MIETTES):
            kit.shape(f"{fid}_m{k}", [0, 0], kind="round", w=34 + 6 * (k % 3), h=24 + 4 * (k % 2), r=4, fill=PAPER,
                      stroke=AI_TICK, sw=3, dash=[0.01, 7], shadow=0, z=3.8, scale=0)

    # --- l'IA : AI.png, pilule « IA », faisceaux et traits pointillés, coches, nuage, puces ---
    ai = S.png("AI", keep_largest=True)
    ai_h = round(IA_W * ai["h"] / ai["w"])
    brain_front = [round(0.2 * IA_W, 1), round(-0.28 * ai_h, 1)]     # avant du cerveau de verre (repère de l'IA)
    S.add("ia", "png", z=4, src=ai["src"], w=IA_W, h=ai_h, saturate=0.85,
          contact=dict(w=round(IA_W * 0.72), h=24, dy=4, blur=10, alpha=0.2))
    S.set("ia", pos=list(IA_C), scale=1, opacity=1)
    S.add("ia_pill", "pill", z=4.1, parent="ia", text="IA", w=round(text_width("IA", 32, 600) + 44), h=50, size=32,
          weight=600, fill=PAPER, sw=4, shadow=4)
    S.set("ia_pill", pos=[0, round(-ai_h / 2 - 30, 1)], scale=1, opacity=1)
    beam = dict(color=AI_TICK, sw=6, dash=[0.01, 14], dots=True)
    S.add("faisceau", "wire", z=13, a={"id": "ia", "at": brain_front}, **beam)            # S01 : lit le dossier
    S.set("faisceau", draw=0, pb=[DOSSIER_C[0] + DOSSIER_W / 2 + 4, DOSSIER_C[1]], via=[306, 1010], sag=0, opacity=1,
          **{"from": 0})                         # touche le bord droit de la chemise sans traverser les cartes
    S.add("faisceau_contrat", "wire", z=13, a={"id": "ia", "at": brain_front}, **beam)    # S05 : cherche le contrat
    S.set("faisceau_contrat", draw=0, pb=[DOSSIER_C[0] + 40, ROW_WORLD[3]], sag=0, opacity=1, **{"from": 0})
    for i in (0, 2, 4):                          # S01 : traits d'extraction carte -> rangée (sur la ligne de texte)
        S.add(f"extrait{i + 1}", "wire", z=13, a={"id": CARD_IDS[i], "at": list(CARD_WIRE_AT)},
              b={"id": "fiche", "at": [WIRE_X, ROWS[i] + TY]}, color=AI_TICK, sw=5, dash=[0.01, 11], dots=True)
        S.set(f"extrait{i + 1}", draw=0, sag=0, opacity=1, **{"from": 0})
    head = [IA_C[0] + brain_front[0], IA_C[1] + brain_front[1]]
    left = [NUAGE_C[0] - NUAGE_W / 2 + 6, NUAGE_C[1] - 10]
    for k, r in enumerate((6, 9, 12)):           # bulles de pensée : de la tête de l'IA vers le nuage
        t = 0.2 + 0.3 * k
        kit.shape(f"bulle_rond{k + 1}", [round(head[0] + (left[0] - head[0]) * t, 1),
                                         round(head[1] + (left[1] - head[1]) * t, 1)], kind="circle", w=2 * r,
                  fill=PAPER, stroke=AI_TICK, sw=3, dash=[0.01, 6], shadow=0, z=13.04, scale=0)
    kit.shape("nuage", list(NUAGE_C), kind="poly", pts=cloud_pts(NUAGE_W, NUAGE_H), fill=PAPER, stroke=AI_TICK, sw=4,
              dash=[0.01, 10], shadow=0, z=13.05, scale=0)
    for pid, txt in PUCES.items():               # puces de valeur (papier, contour pointillé) ; monde
        pos = PUCE_S02.get(pid, PUCE_DATES_S04[0] if pid == "puce_date1" else PUCE_DATES_S04[2])
        kit.shape(pid, list(pos), kind="round", w=PUCE_W, h=PUCE_H, r=PUCE_H / 2, fill=PAPER, stroke=AI_TICK, sw=3,
                  dash=[0.01, 8], shadow=0, z=13.2, scale=0)
        kit.text(f"{pid}_txt", [0, 1], txt, size=PUCE_SIZE, weight=600, z=13.25, parent=pid)
    kit.shape("cadre_choix", list(PUCE_DATES_S04[0]), kind="round", w=PUCE_W + 14, h=PUCE_H + 14, r=14,
              fill="none", stroke=AI_TICK, sw=5, dash=[0.01, 8], shadow=0, z=13.3, scale=0)   # S04 : saute de date en date
    for pid in ("puce_date1", "puce_date3"):     # S04 : la date essayée puis lâchée est barrée (trait fin de l'IA)
        kit.shape(f"{pid}_barre", [0, 0], kind="poly", pts=[[-PUCE_W / 2 + 14, 1], [PUCE_W / 2 - 14, 1]],
                  closed=False, fill="none", stroke=AI_TICK, sw=4, shadow=0, z=13.27, parent=pid, draw=0)
    for k, i in enumerate((1, 3)):               # S07 : pointillés du nuage vers les deux valeurs inventées, le long
        #                                          de la marge gauche du brief, puis sous le texte jusqu'au cadre rouge
        S.add(("trace_vente", "trace_contrat")[k], "wire", z=13, a={"id": "nuage", "at": [-30 + 26 * k, -NUAGE_H / 2 + 8]},
              b={"id": LINE_IDS[i], "at": [round(VALUE_CX[i] - CADRE_W / 2 - 4, 1), 12]}, color=INK, sw=4,
              dash=[0.01, 10], dots=True)
        S.set(("trace_vente", "trace_contrat")[k], draw=0, sag=0, opacity=0.7, via=list(TRACE_VIA[k]), **{"from": 0})
    kit.icon("rembobiner", list(REMBOBINER_C), "rewind", disc=30, s=34, fill=LIGHT, shadow=4, z=13.4, scale=0)
    kit.icon("alerte", list(ALERTE_C), "warning", disc=36, s=44, fill=PAPER, color=RED, shadow=5, z=12, scale=0)
    kit.text("p1_vide", [0, 0], "?", size=44, weight=800, color=AI_TICK, z=13.3, scale=0)   # S05 : retour bredouille

    # --- le repère des 4 erreurs et son titre ---
    gap = round(max(text_width(t, TEXT_MIN, 700) for t in MARKER_LABELS) + 30)   # légendes en 32 px : deux légendes
    #                                              voisines qui se croisent en fondu (kit.step) ne se touchent pas
    kit.steps_marker(MARKER_LABELS, id="marqueur", y=MARKER_Y, cx=CX, gap=gap, z=20)
    S.ents["marqueur"]["p"].update(moveBlank=True, labelShow="active", labelSize=TEXT_MIN)   # seule l'étape active
    #                                              est légendée, à l'encre, en 32 px (revue 1 : légendes grises illisibles)
    S.set("marqueur", scale=0, on=0)
    kit.text("titre_erreurs", list(TITRE_C), T_TITRE, size=34, weight=700, z=20, scale=0)

    # --- la parade (pilule « Parade » au bouclier) -> bandeau de la rubrique (S18) ; cadre ; la rubrique ---
    kit.shape("parade", list(PARADE_S03), kind="round", w=PARADE_W, h=PARADE_H, r=PARADE_H / 2, fill=LIGHT,
              stroke=INK, sw=4, shadow=6, z=12, scale=0)
    S.set("parade", w=PARADE_W, h=PARADE_H, r=PARADE_H / 2, stroke=INK)     # hex : contour encre -> deep (S18)
    kit.icon("parade_ico", [-72, 0], "shield", s=30, color=INK, z=12.1, parent="parade")
    kit.text("parade_txt", [20, 2], "Parade", size=32, weight=700, z=12.1, parent="parade")
    kit.text("rubrique_titre", [24, 2], T_RUBRIQUE, size=34, weight=700, z=12.1, parent="parade", typed=True, lh=1.1)
    (rc, rw, rh) = CADRE_RUB_S18
    kit.shape("rubrique_cadre", list(rc), kind="round", w=rw, h=rh, r=16, fill="none", stroke=DEEP, sw=4, shadow=0,
              z=11.8, draw=0)
    S.set("rubrique_cadre", w=rw, h=rh)

    # --- S13-S15 : les deux formulations, « ≠ », « Fait » -> « Hypothèse ». Code du trait : plein = affirmé (carte A,
    #     bord encre plein, « prévoit » souligné plein) ; tirets = incertain (carte B, bord et « pourrait » en tirets) ---
    kit.shape("carteA", list(CARTE_A_C), kind="round", w=CARTE_W, h=CARTE_H, r=16, fill=PAPER, stroke=INK, sw=5,
              shadow=6, z=14, scale=0)
    S.set("carteA", stroke=INK)                  # hex : le bord plein s'efface sous les tirets (S14 « même »)
    kit.shape("carteA_tirets", [0, 0], kind="round", w=CARTE_W, h=CARTE_H, r=16, fill="none", stroke=INK, sw=5,
              dash=[14, 10], shadow=0, z=14.02, parent="carteA", opacity=0)
    kit.shape("carteA_surligne", [PREVOIT[0], LIGNE1_Y], kind="round", w=round(PREVOIT[1] + 12), h=42, r=8,
              fill=LIGHT, stroke="none", sw=0, shadow=0, z=14.05, parent="carteA", scale=0)
    kit.text("carteA_txt", [CARTE_TXT_X, 0], T_CARTE_A0, size=34, weight=700, anchor="start", z=14.1,
             parent="carteA", lh=1.18)
    S.set("carteA_txt", text=T_CARTE_A0, chars=len(T_CARTE_A0))
    und_a = [[PREVOIT[0] - PREVOIT[1] / 2, LIGNE1_Y + 23], [PREVOIT[0] + PREVOIT[1] / 2, LIGNE1_Y + 23]]
    kit.shape("carteA_souligne", [0, 0], kind="poly", pts=und_a, closed=False, fill="none", stroke=DEEP, sw=5,
              shadow=0, z=14.15, parent="carteA", draw=0)
    kit.shape("carteA_souligne_t", [0, 0], kind="poly", pts=und_a, closed=False, fill="none", stroke=DEEP, sw=5,
              dash=[10, 8], shadow=0, z=14.15, parent="carteA", opacity=0)
    kit.tick("carteA_coche", [CARTE_W / 2 - 40, 0], AI_TICK, size=40, sw=8, variant="ai", z=14.2, parent="carteA",
             draw=0, thin=6, boxSw=3.5, boxFill=PAPER)
    # contrôle sans son : la certitude se lit sans les mots : coche (carte A) au-dessus de « ? » (carte B) ; au
    # reclassement (S14 « même »), la coche de la carte A devient le même « ? »
    kit.text("carteA_q", [CARTE_W / 2 - 40, 2], "?", size=64, weight=800, color=DEEP, z=14.2, parent="carteA",
             scale=0)
    kit.shape("carteB", list(CARTE_B_C), kind="round", w=CARTE_W, h=CARTE_H, r=16, fill=PAPER, stroke=INK, sw=5,
              dash=[14, 10], shadow=6, z=14, scale=0)
    S.add("carteB_tete", "figure", z=14.1, parent="carteB", variant="paper")       # le client : « ce qu'il a dit »
    S.set("carteB_tete", pos=[-CARTE_W / 2 + 42, 6], scale=0.36, lean=0)
    kit.shape("carteB_surligne", [POURRAIT[0], LIGNE1_Y], kind="round", w=round(POURRAIT[1] + 12), h=42, r=8,
              fill=LIGHT, stroke="none", sw=0, shadow=0, z=14.05, parent="carteB", scale=0)
    kit.text("carteB_txt", [CARTE_B_TXT_X, 0], T_CARTE_B, size=34, weight=700, anchor="start", z=14.1,
             parent="carteB", lh=1.18, typed=True)
    kit.shape("carteB_souligne", [0, 0], kind="poly",
              pts=[[POURRAIT[0] - POURRAIT[1] / 2, LIGNE1_Y + 23], [POURRAIT[0] + POURRAIT[1] / 2, LIGNE1_Y + 23]],
              closed=False, fill="none", stroke=DEEP, sw=5, dash=[10, 8], shadow=0, z=14.15, parent="carteB",
              opacity=0)
    kit.text("carteB_q", [CARTE_W / 2 - 40, 2], "?", size=64, weight=800, color=DEEP, z=14.2, parent="carteB",
             scale=0)
    kit.text("different", list(NEQ_C), "≠", size=100, weight=800, z=14.3, scale=0)
    kit.shape("fait", list(FAIT_C), kind="round", w=FAIT_W, h=PILL2_H, r=PILL2_H / 2, fill=LIGHT, stroke=DEEP, sw=4,
              shadow=5, z=14.4, scale=0)
    kit.tick("fait_coche", [-44, 1], AI_TICK, size=24, sw=6, variant="ai", z=14.45, parent="fait", draw=1, thin=5,
             boxSw=3, boxFill=PAPER)                       # la certitude affirmée par l'IA (pas une coche de « Toi »)
    kit.text("fait_txt", [16, 2], "Fait", size=TEXT_MIN, weight=700, z=14.45, parent="fait")
    kit.shape("hypothese", list(FAIT_C), kind="round", w=HYP_W, h=PILL2_H, r=PILL2_H / 2, fill=PAPER, stroke=DEEP,
              sw=4, dash=[10, 8], shadow=5, z=14.4, scale=0)
    kit.text("hypothese_txt", [0, 2], "Hypothèse", size=TEXT_MIN, weight=700, z=14.45, parent="hypothese")

    # --- S15 : la traînée de la diagonale ---
    kit.shape("trainee", [0, 0], kind="poly", pts=[list(DIAG_A), list(DIAG_B)], closed=False, fill="none", stroke=DEEP,
              sw=3, shadow=0, z=16.4, draw=0)

    # --- « Toi » (figurine encre, stylo 90 px, bras côté gauche de l'écran) ; sa pilule ; le client ---
    toi = Figure(kit, "toi", pos=list(TOI_REST), scale=FIG_S, show=False, z=15)          # entre sur « Dans » (S03)
    short_pen(toi, S)
    S.add("toi_pill", "pill", z=16.5, parent="toi", text="Toi", w=round(text_width("Toi", 32, 600) + 48), h=52,
          size=32, weight=600, fill=INK, color=BG, stroke=INK, shadow=4)
    S.set("toi_pill", pos=list(TOI_PILL_LOCAL), scale=0, opacity=1)
    client = Figure(kit, "client", pos=list(CLIENT_C), scale=FIG_S, variant="paper", tool=False, show=False, z=14.8)

    # --- la pastille au-dessus du client (S19-S22) et le bouton (S22, sans pictogramme) ---
    S.add("pastille_client", "pill", z=16, text=PILL_TEXT, w=PILL_W, h=PILL_H, size=PILL_SIZE, weight=700, fill=CYAN,
          icon="person")
    S.set("pastille_client", pos=list(PASTILLE_CLIENT), scale=PASTILLE_CLIENT_S, opacity=0, text=PILL_TEXT)
    S.add("pastille_btn", "pill", z=41, text=T_ABONNER, w=PILL_W, h=PILL_H, size=PILL_SIZE, weight=700, fill=CYAN)
    S.set("pastille_btn", pos=list(PASTILLE_CLIENT), scale=PASTILLE_CLIENT_S, opacity=0, w=PILL_W, text=T_ABONNER)

    # --- S21 : la bulle de « Toi » (sans « ? » ni mini-figurine), la question dedans ; la réponse du client ---
    tip = [TOI_S19_REST[0] + 20, round(TOI_S19_REST[1] + FIG_TOP * FIG_S + 14, 1)]  # côté droit de sa tête (repos
    #                                              S19) : la queue passe à droite de la pastille du client
    S.add("bulle", "bubble", z=17.5, big=BULLE_BIG, small=BULLE_SMALL,
          tail=[tip[0] - BULLE_C[0], tip[1] - BULLE_C[1]], tailBase=[10, 60])
    S.set("bulle", pos=list(BULLE_C), scale=0, s=0, q=0, glyph=0, pulse=0, opacity=1, rot=0)
    kit.text("bulle_txt", [0, 0], T_BULLE, size=TEXT_MIN, weight=700, z=17.6, parent="bulle", lh=1.1)
    S.add("reponse", "pill", z=22, text=T_SEPT, w=REPONSE_W, h=REPONSE_H, size=TEXT_MIN, weight=700, fill=CYAN)
    S.set("reponse", pos=list(REPONSE_C), scale=0, opacity=1, text=T_SEPT)

    # --- S22 : ondes du toucher du stylo sur le bouton ---
    for k in range(2):
        kit.shape(f"fin_onde{k + 1}", list(FIN_TAP), kind="circle", w=60, fill="none", stroke=DEEP, sw=5, shadow=0,
                  z=43.5, opacity=0)

    return SimpleNamespace(toi=toi, client=client, sheet=SHEET, ai_h=ai_h, brain_front=brain_front,
                           lines=LINE_IDS, cards=CARD_IDS)


def build(S):
    kit = Kit(S)
    c = cast(S, kit)
    only = [p for p in os.environ.get("WTH_PARTS", "").split(",") if p]   # WTH_PARTS=p2 : cette partie seule
    for name in PARTS:
        if not only or name in only:
            importlib.import_module(f".{name}", __name__).part(S, kit, c)
