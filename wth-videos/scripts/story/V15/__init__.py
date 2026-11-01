"""V15 « Pas besoin de tout réorganiser ce soir » : mise en scène Story, en paquet (une partie par fichier).

Storyboard : scripts/storyboards/V15.json (v1, révisé après le test sans son, 22 scènes, 82 temps forts, 81,684 s),
version lisible scripts/storyboards/V15.md. Voix : build/V15/words.json (film : images 0-2450, FILM_END = 2451).
Fil : la pilule cyan « Ton argent » (`pastille`, pill euro, 256 x 64, Bold 34), l'argent de « Toi » : au sol devant
lui à l'image 0 (640, 1198) ; au bout de son stylo (S01) ; lâchée, au sol (460, 1198) (S02) ; au sommet de la tour du
grand plan (460, 798 ; 758 puis 718 en S09) ; au sommet de l'escalier (170, 798) (S10-S18) ; remontée sur la tour
(S19) ; de nouveau au sommet de l'escalier (S20) ; au bout du stylo de « Toi » debout sur la marche 1 (560, 880) (S21) ;
devient le bouton « S’abonner » (S22). Entité MONDE : quand la tour ou l'escalier bouge, la déplacer avec la même clé
(même f, d, e) que le bloc du sommet.
Parti pris : « la tour devient un escalier ». Les 4 blocs du grand plan (`bloc1`-`bloc4` : Budget, Épargne,
Placements, Papiers) poussent sous la pastille en une tour (x 300-620) ; « Toi » tire le bloc du bas et la même tour
s'étale en 4 marches basses calées à gauche (x 45-790 / 625 / 460 / 295). Deux instruments : la pilule-calendrier en
haut à gauche, la jauge « Énergie » en haut à droite. Une horloge (`cadran`) : un week-end entier (tour complet) contre
10 min (1/6 de tour). Aucune IA (le script n'en parle pas) : « Toi » est le seul acteur, trait plein deep.

Parties (scènes contiguës ; poids : temps forts et secondes) :
- p1 : S01-S08, images 0-899 (29 temps forts, 30,0 s). Accroche (argent ramassé, lâché ; la tour du grand plan pousse,
  « Toi » s'y cogne ; la petite marche « 1 » annoncée) ; contexte (la tour ravale la petite marche, ses 4 chantiers
  nommés ; un week-end entier sur l'horloge, abandon) ; point 1 (l'argent hors de portée, l'énergie pleine, la poussée
  qui la vide, la nuée de « ? »).
- p2 : S09-S16, images 900-1745 (30 temps forts, 28,2 s). La tour grandit, « Toi » recule, « Plus tard » ; il tire le
  bloc du bas et la tour s'étale en escalier ; marche 1 choisie, montée, « 2 » noté ; l'abonnement barré en 10 min,
  coche ; les trois autres petites actions ; le premier segment d'énergie ; point 3 : marche 2 cochée, « 3 » noté,
  bond éclair sur la marche 3.
- p3 : S17-S22, images 1746-2450 (23 temps forts, 23,5 s). « 3 ✓ » face à la tour fantôme « 0 ✓ » ; la règle et la
  barre des 52 semaines ; ◀◀ Avant (rembobinage en tour, attente) ; Maintenant (escalier, une marche cochée) ; l'argent
  revient dans la main de « Toi », marches suivantes notées en tirets ; fin.
Les coupes tombent sur des débuts de scène où l'action repart : S09 (« Et » : la nuée de « ? » rentre dans la tour,
qui se met à grandir ; le passage tour -> escalier de S10 reste dans la même partie que la croissance qui le prépare)
et S17 (le bilan : « 3 ✓ » contre la tour fantôme). ENTRY_P2 et ENTRY_P3 sont le contrat des raccords
(kit.pin(f0 - 1, …)) ; les figurines n'y sont jamais (placées par walk / hop / enter seulement).

Entités nouvelles : AUCUN nouveau type, aucun changement du code partagé. Compositions (catalogue) :
- bloc / marche = shape round (pistes pos, w, h, fill hex) + pictogramme sur disque cyan (icon, enfant) + nom (text,
  enfant, ancre start) ; les enfants restent à -w/2 + 35 et -w/2 + 67 du centre : quand w change, leurs pos changent
  avec la même clé (block_children) ;
- accolade « Grand plan » = shape poly ouverte deep (origine au pied (270, 1230), piste draw ; s'allonge par la piste
  sy, pied fixe) + text « Grand\\nplan » ;
- tour fantôme = 4 shape round en tirets encre + pictogrammes encre sans disque (enfants) + text + « 0 » (text rouge)
  et coche rouge (tick) ;
- numéro noté = shape circle deep (draw : tracé sous le stylo) + chiffre (text, enfant, typed) ; numéro « à faire » =
  même dessin en tirets [8, 6] (entités distinctes : dash est un paramètre fixe) ;
- « Plus tard » en rouge, texte papier : la pilule passe au rouge (piste fill) et son libellé encre s'efface (piste
  textOp) sous un texte papier enfant (`cal_alerte`) : la couleur du texte d'une pilule est un paramètre fixe ;
- ◀◀ de « Avant » : disque light (enfant, `cal_rewind`) qui couvre le pictogramme cal de la pilule + icon rewind
  (enfant) ; à poser en (-w/2 + 30, 0) de la pilule (place du pictogramme, PillP) ;
- segment d'énergie = shape round cyan 75 x 44 (`elan1`-`elan3`) ;
- abonnement = carte plate (shape round papier, contour encre) + pictogramme repeat sur disque cyan + « Abonnement /
  inutile » + « −9,99 € / mois » (deep) + trait (shape poly ouverte, enfant, draw, Figure.strike track="draw").

REVUE 1 (corrections) : pictogramme `repeat` ajouté au kit (nouveau nom, rien d'autre ne change) ; « Toi » = sous-classe
Toi de Figure (bras baissé : stylo couché en travers du corps, pointe à 24 px au-dessus des pieds) ; accroche plus haute
(argent levé à y 900, calendrier dans la colonne d'action puis rangé sur « grand ») ; rangée des instruments à y 360 ;
S09 : la tour passe de 400 à 500 puis 600 px d'un coup (SCALE), « Toi » recule d'un bond de 80 puis 70 px ; cartes de
S14 garées au-dessus de leur marche avec un fil tireté ; segment d'énergie 2 x en vol avec traînée ; tour fantôme à
l'échelle réelle (S17) ; ◀◀ / ▶▶ géants et voile du rembobinage (S19-S20) ; macros cal_swap, marks, stepped, elan_fly,
count_rings ; découpes de sous-titres imposées (CAPTION_GROUPS).

CONTRÔLE SANS SON (tour ciblé) : pictogramme `bolt` ajouté au kit (nouveau nom, opt-in) pour l'éclair de la jauge ;
Toi.stretch / Toi.tip_on (méthodes de Figure seulement) ; entité `ecart` (S09) ; constantes TOI_CHOC, POUSSE_*, SAUT_*,
PASTILLE_FLECHIE*, CAL_HOOK_K, CADRAN_ATTENTE, BILAN_DX ; détails dans les docstrings des parties.

ÉCARTS DE PLACE (mise en page ou allonge, aucun sens changé) :
- carte de l'abonnement en (560, 840), trait en DIAGONALE de (680, 782) à (460, 868) : il barre les deux lignes et le
  prix et reste à portée de « Toi » sur la marche 1 (265 px < 267) ;
- les signes de penché du storyboard (« +10° en avant ») sont « vers l'argent, à gauche » : sur la piste lean de la
  figurine (rotation horaire autour du pied), c'est une valeur NÉGATIVE (« Toi » regarde à gauche, side="left").
"""
import importlib
import math
import os
from types import SimpleNamespace

from pipeline.story import GEOM, STYLE, text_width
from pipeline.story_kit import Figure, Kit, ang_lerp, frames, lerp, r3

PARTS = ["p1", "p2", "p3"]                      # S01-S08, S09-S16, S17-S22
NBSP = " "                                 # espace insécable
ALERT_WORDS = {"lâché", "échoue", "abandonne", "trop", "repousse"}   # karaoké en rouge (style du storyboard)
ACOUSTIC_SNAP = {"gap": 0.2, "window": 0.08}    # temps fort après un silence : calé sur l'attaque audible
# découpes imposées (revue 1) : « grand plan » et « la marche » jamais coupés ; pas de mot seul éclair (« parce »)
CAPTION_GROUPS = [
    ["Dans cette vidéo", "on va voir", "pourquoi le", "grand plan échoue"],
    ["Un week-end entier", "Et le lundi", "on abandonne", "parce que c’était trop"],
    ["Et plus", "la marche est haute", "plus on repousse", "le départ"],
]

# ---------- couleurs ----------
INK, CYAN, DEEP, LIGHT = STYLE["ink"], STYLE["cyan"], STYLE["deep"], STYLE["light"]
PAPER, RED, BG = STYLE["paper"], STYLE["red"], STYLE["bg"]

# ---------- textes à l'écran (typographie française) ----------
T_ARGENT = "Ton argent"
T_ABONNER = "S’abonner"
T_TOI = "Toi"
T_BLOCS = ["Budget", "Épargne", "Placements", "Papiers"]            # bloc1 (bas) ... bloc4 (haut)
ICO_BLOCS = ["cart", "coin", "bars", "mail"]
T_GRAND_PLAN = "Grand\nplan"
T_CAL = {"weekend": "Week-end", "lundi": "Lundi", "tard": "Plus tard", "s1": "Semaine 1", "s2": "Semaine 2",
         "s3": "Semaine 3", "regle": "1 décision / semaine", "avant": "Avant", "maintenant": "Maintenant"}
T_ENERGIE = "Énergie"
T_DIX = "10 min"
T_ABO = "Abonnement\ninutile"
T_ABO_PRIX = "−9,99" + NBSP + "€ / mois"
T_WEEKEND = "week-end"
T_OPTIONS = [("opt_virement", "Virement\nd’épargne", "bank", "2"),   # (id, texte, pictogramme, numéro de sa marche)
             ("opt_frais", "Vérifier\nles frais", "percent", "3"),
             ("opt_projet", "Dater\nun projet", "cal", "4")]
T_SEMAINE1, T_FIN_ANNEE, T_DECISIONS = "Semaine 1", "Fin d’année", "décisions"

# ---------- mise en page (1080 x 1920) ----------
X_MIN, X_MAX, Y_MIN, Y_MAX = 40, 930, 160, 1270  # zone d'action ; on descend jusqu'à y ≈ 1250 ; rien à droite de 930
GROUND = 1230                                   # pied des figurines, bas des blocs, bas de la pastille
SOL_Y, SOL_X0, SOL_X1 = 1232, 45, 915           # trait encre du sol (4 px)
FIG_S = 1.0                                     # « Toi » à l'échelle 1
FIG_BASE = GEOM["FIGURE"]["base"]               # 95
HEAD_DY, HEAD_R = GEOM["FIGURE"]["head"]["cy"], GEOM["FIGURE"]["head"]["r"]     # -64, 32
SHOULDER = GEOM["FIGURE"]["shoulder"]           # [-30, -16] (côté gauche)
REACH_OK, REACH_MIN = 267 * FIG_S, 63 * FIG_S   # allonge confortable / minimale (pointe du stylo)

# --- « Toi » : places (centre de la figurine ; pied = y + 95) ---
TOI_P0 = (862, 1135)                            # au sol, en bas à droite (repos, attente)
TOI_BUTE = (706, 1135)                          # S03 : contre la tour : la pointe du stylo levé touche sa face (x 618)
TOI_PIED_TOUR = (740, 1135)                     # S06 : au pied de la tour ; sauts sur place, le stylo frappe sa face
TOI_TEND = (840, 1135)                          # S07 : tend le stylo vers l'argent, sans l'atteindre
TOI_CHOC = (684, 1135)                          # S03 (contrôle sans son) : le corps heurte la face de la tour (x 620)
POUSSE_CONTACT = (622, 1030)                    # S08 : la pointe au milieu de la tour (joint Épargne / Placements)
POUSSE_PAS = 8                                  # S08 : un coup toutes les 8 images, un quart d'énergie par coup
SAUT_VISE, SAUT_DIST = (636, 858), 205          # S06 : sauts stylo tendu vers l'argent ; à l'apogée la pointe reste à côté, sous la pastille
TOI_POUSSE = (720, 1135)                        # S08 : pousse la tour (penché de 22°, la tête reste hors de la tour)
TOI_RECUL = (730, 1135)                         # S08 -> S09 : les pieds ont glissé de 10 px en arrière ; affaissé
TOI_RECUL2 = (810, 1135)                        # S09 : premier bond en arrière (80 px)
TOI_RECUL3 = (880, 1135)                        # S09 : second bond en arrière (70 px)
TOI_TIRE = (790, 1135)                          # S10 : saisit le bord droit du bloc du bas
TOI_M1, TOI_M2, TOI_M3 = (708, 1035), (543, 935), (378, 835)   # debout sur les marches 1, 2, 3
LEAN_AFFAISSE = -10                             # « penché en avant, tête basse » (vers la gauche : lean négatif)
LEAN_VERS = -6                                  # S04 : se penche vers la tour
LEAN_POUSSE = -14                               # S08 : tête encore plus basse (nuée de « ? »)
LEAN_PRESSE = -22                               # S08 « demande » : penché de tout son poids dans la tour
TOI_LOW_GRIP, TOI_LOW_ROT = (50, -12), 80       # bras BAISSÉ : prise à la hanche ; le stylo pend vers l'avant
PEN_CLEAR = 24                                  # pointe du stylo baissé : au moins 24 px au-dessus des pieds (revue 1)
NOM_SOL = (0, -136)                             # étiquette « Toi » (enfant) : au-dessus de la tête, au sol
NOM_MARCHE = (100, -70)                         # sur les marches : à droite de la tête
NOM_W, NOM_H = 100, 56


class Toi(Figure):
    """« Toi » (V15) : la Figure du kit, bras baissé redessiné (revue 1 : la pointe du stylo baissé passait sous le sol
    ou dans la marche). Bras baissé = prise à la hanche (low_grip), stylo couché en travers du corps vers l'arrière,
    pointe à PEN_CLEAR px au-dessus des pieds : il ne touche ni le sol, ni une marche, ni la tour devant lui. Tout le
    reste est la Figure du kit (aucun code partagé ne change)."""

    def low_pose(self, n):
        G, _ = super().low_pose(n)
        s = self._scale(n)
        foot = self.S.val(self.id, "pos", n)[1] + FIG_BASE * s
        L = self.pen_len * s
        k = max(-1.0, min(1.0, (foot - PEN_CLEAR * s - G[1]) / L))
        a = math.degrees(math.asin(k))               # sous l'horizontale, vers l'arrière (côté droit : +x)
        return G, (a if self.m < 0 else 180 - a)

    def stretch(self, fa, fb, pt, dist=255, ramp=3):
        """Contrôle sans son : images [fa, fb), le bras se tend vers `pt` (monde), la pointe à `dist` px de l'épaule
        dans sa direction, image par image (le corps peut sauter : la pointe suit l'épaule et reste toujours à
        portée). La pose part de celle de fa - 1 en `ramp` images. Méthodes de Figure seulement (aucun code partagé
        ne change). Renvoie fb."""
        rel0, r0 = self._start(fa)
        for k, n in enumerate(range(fa, fb)):
            A, s = self._shoulder(n), self._scale(n)
            L = math.hypot(pt[0] - A[0], pt[1] - A[1])
            T = [A[0] + (pt[0] - A[0]) * dist / L, A[1] + (pt[1] - A[1]) * dist / L]
            G, rot = self._tip_pose(A, T, s)
            p = min(1.0, (k + 1) / ramp)
            self._pose(n, lerp([A[0] + rel0[0], A[1] + rel0[1]], G, p), ang_lerp(r0, rot, p))
        return fb

    def tip_on(self, fa, fb, pt):
        """Images [fa, fb) : la pointe reste sur `pt` (monde) pendant que le corps penche (poussée de S08)."""
        for n in range(fa, fb):
            G, rot = self._tip_pose(self._shoulder(n), list(pt), self._scale(n))
            self._pose(n, G, rot)
        return fb


def fig_pos(x, feet=GROUND, s=FIG_S):
    return [x, round(feet - FIG_BASE * s, 1)]


def _toward(fig, pt, dist):
    """Point à `dist` px de l'épaule de « Toi » (en fig), dans la direction de `pt` (monde)."""
    sx, sy = fig[0] + SHOULDER[0] * FIG_S, fig[1] + SHOULDER[1] * FIG_S
    L = math.hypot(pt[0] - sx, pt[1] - sy)
    return (round(sx + (pt[0] - sx) * dist / L, 1), round(sy + (pt[1] - sy) * dist / L, 1))


# S07 « bloque ? » : la pointe s'arrête à bout de bras (260 px de l'épaule) dans la direction du bas de la pastille
# (585, 798), soit vers (661, 906) : 76 px sous l'argent. reach(f, TEND_TIP, step=False) ne prévient pas (cible à
# portée) ; viser la pastille même ferait un « attention (kit) » (hors d'atteinte).
TEND_TIP = _toward(TOI_TEND, (585, 798), 260)


# --- la pastille « Ton argent » (objet du fil, monde) ---
PASTILLE_SIZE, PASTILLE_H = 34, 64
PASTILLE_W = round(text_width(T_ARGENT, PASTILLE_SIZE, 700) + 48 + 30)   # 256 (pictogramme euro compris)
PASTILLE_SOL0 = (640, 1198)                     # image 0 : posée au sol devant « Toi »
PASTILLE_TAP0 = (740, 1198)                     # S01 « promis » : bout droit, touché du stylo
PASTILLE_MAIN = (640, 900)                      # S01 « reprendre » : levée à bout de bras, au-dessus de la tête
PASTILLE_MAIN_TIP = (765, 900)                  # pointe du stylo sur le bout droit (y reste)
PASTILLE_FLECHIE = (640, 960)                   # S02 « lundi, » : le bras fléchit, l'argent redescend de 60 px
PASTILLE_FLECHIE_TIP = (765, 960)
PASTILLE_TOMBEE = (460, 1198)                   # S02 : lâchée, entière à quelques pas
PASTILLE_TOUR = {100: (460, 798), 125: (460, 698), 150: (460, 598)}      # sommet de la tour (hauteur de bloc)
PASTILLE_ESCALIER = (170, 798)                  # sommet de l'escalier (marche 4)
PASTILLE_RETOUR = (540, 800)                    # S21 : levée à bout de bras par « Toi » sur la marche 1 (pose de S01)
PASTILLE_RETOUR_TIP = (665, 800)                # S21 : la pointe touche le bout droit

# --- les 4 blocs : tour, puis escalier ---
BLOC_IDS = [f"bloc{i + 1}" for i in range(4)]
BLOC_ICO = [f"{b}_ico" for b in BLOC_IDS]       # pictogramme sur disque cyan r 22 (enfant)
BLOC_NOM = [f"{b}_nom" for b in BLOC_IDS]       # nom Bold 34, ancre start (enfant, typed : écrit en S05)
TOWER_X, TOWER_W = 460, 320                     # x 300-620
STAIRS_RIGHT = [790, 625, 460, 295]             # bord droit des marches (bord gauche 45)
STAIRS_LEFT = 45
ICO_DX, NOM_DX = 35, 67                         # depuis le bord gauche du bloc (tour : 335 / 367 ; escalier : 80 / 112)


def tower(i, bh=100):
    """(centre, w, h) du bloc i (0 = bas) de la tour, blocs de hauteur bh empilés sur le sol."""
    return [TOWER_X, GROUND - bh * (i + 0.5)], TOWER_W, bh


def stairs(i):
    """(centre, w, h) de la marche i (0 = bas) de l'escalier (marches de 100, calées à gauche à x 45)."""
    x1 = STAIRS_RIGHT[i]
    return [round((STAIRS_LEFT + x1) / 2, 1), GROUND - 100 * (i + 0.5)], x1 - STAIRS_LEFT, 100


def block_children(w):
    """pos locales (pictogramme, nom) d'un bloc de largeur w : constantes depuis son bord gauche."""
    return [round(-w / 2 + ICO_DX, 1), 0], [round(-w / 2 + NOM_DX, 1), 0]


def block_top(i, geom):
    """Haut (y monde) du bloc i d'une géométrie (centre, w, h)."""
    c, _, h = geom
    return c[1] - h / 2


# --- la petite marche « 1 » de l'annonce (S04-S05) ---
APERCU_C, APERCU_W, APERCU_H = (702, 1180), 165, 100   # x 620-785, au sol contre le bloc Budget
APERCU_CACHE = (460, 1180)                      # départ caché derrière B1

# --- l'accolade « Grand plan » (origine au pied, s'allonge par sy) ---
ACCOLADE_O = (270, 1230)
ACCOLADE_PTS = [(-20, 0), (0, 0), (0, -400), (-20, -400)]   # tracée de bas en haut (draw)
ACCOLADE_SY = {100: 1.0, 125: 1.25, 150: 1.5}   # tour de 400 / 500 / 600 px
GP_NOM_C = {100: (150, 1030), 125: (150, 980), 150: (150, 930)}   # « Grand » / « plan », milieu de l'accolade

# --- la pilule-calendrier ---
CAL_C, CAL_K = (210, 360), 1.0                  # rangée des instruments à y 360 (revue 1 : moins de vide en haut)
CAL_HOOK_K = 1.5                                # accroche : pilule grande (« Week-end » / « Lundi » lisibles)
CAL_HOOK_C = (560, 760)                         # S01-S02 : dans la colonne d'action, au-dessus de l'argent
CAL_TARD_DX = 40                                # S09 « départ. » : « Plus tard » glisse de 40 px vers la droite
CAL_REGLE_C, CAL_REGLE_K = (540, 330), 1.25     # S18 : « 1 décision / semaine » au centre


def cal_w(text):
    """Largeur de la pilule-calendrier pour `text` (pictogramme compris)."""
    return round(text_width(text, 34, 700) + 48 + 30)


def cal_icon_x(text):
    """x local du pictogramme de la pilule (là où se pose le ◀◀ de « Avant »)."""
    return round(-cal_w(text) / 2 + 30, 1)


# --- l'horloge ---
CADRAN_R = 70
CADRAN_CAL = (210, 530)                         # sous la pilule (S06, S19)
CADRAN_TOI = (820, 580)                         # S13 : près de « Toi » (« 10 min » dessous, (820, 690))
CADRAN_TXT_LOCAL = (0, 110)
CADRAN_WE_R = 96                                # S13 : tour complet fantôme (le week-end) autour de l'horloge
CADRAN_WE_TXT = (820, 455)                      # « week-end » au-dessus
CHRONO_R = 50                                   # petite horloge de chaque montée (S12 / S15 / S16)

# --- la jauge « Énergie » (4 quarts : 595-670, 670-745, 745-820, 820-895) ---
ENERGIE_C, ENERGIE_W, ENERGIE_H = (745, 360), 300, 44
ENERGIE_NOM = (505, 362)                        # ancré à droite (contrôle sans son : l'éclair entre lui et la jauge)
ENERGIE_BOLT_LOCAL, ENERGIE_BOLT_R = (-178, 0), 24   # éclair sur disque cyan, enfant de la jauge : « énergie » dès sa naissance
ENERGIE_QUARTS = [(632, 360), (707, 360), (782, 360), (857, 360)]
ENERGIE_SORTIE = (840, 1045)                    # S07 : sort de la tête de « Toi » (en TOI_TEND)
ENERGIE_GRAND_C, ENERGIE_GRAND_K = (745, 640), 1.2   # S07 « manque » : grande, au-dessus de « Toi » (contrôle sans son : détachée de la tour)

# --- les « ? » ---
GRAND_Q_C, GRAND_Q_GS = (380, 630), 120         # S07 : au-dessus de la pastille
Q_IDS = [f"q{k + 1}" for k in range(8)]         # S08 : deux par bloc (q1-q2 : bloc1 ... q7-q8 : bloc4)
Q_NUEE = [(650, 940), (645, 860), (690, 790), (770, 770), (845, 810), (860, 900), (720, 880), (800, 900)]
Q_SIZE = 56

# --- numéros et coches sur les marches ---
NUM_PTS = [(755, 1180), (590, 1080), (425, 980), (270, 880)]    # « 1 » ... « 4 » (le « 4 », r 20 : 13 px après
#                                                                 « Papiers », qui finit à x 237)
NUM_R, NUM4_R = 26, 20
COCHE_PTS = [(685, 1180), (520, 1080), (355, 980)]
COCHE_SIZE = 48
BILAN_SIZE, BILAN_TICK, BILAN_DX = 120, 80, 46   # « 3 ✓ » et « 0 ✓ » : même corps (ExtraBold 120), même hauteur
BILAN3_C = (245, 560)                           # « 3 ✓ » au-dessus de l'escalier et de l'argent
ZERO_C = (780, 560)                             # « 0 ✓ » au-dessus de la tour fantôme, à la même hauteur

# --- l'abonnement : carte plate du kit (revue 1 : le TAG.png se lisait « bouteille » ou « étiquette de prix ») ---
ABO_W, ABO_H = 340, 170
ABO_C = (560, 840)                              # x 390-730, y 755-925 : au-dessus de la tête de « Toi » (939)
ABO_FROM = (80, 1180)                           # S13 : sort du disque cart de la marche B1
ABO_ICO_LOCAL = (-122, -36)                     # disque cyan, pictogramme repeat (paiement récurrent)
ABO_TXT_LOCAL = (-82, -36)                      # « Abonnement / inutile », Bold 34, ancré à gauche
ABO_PRIX_LOCAL = (0, 50)                        # « −9,99 € / mois », Bold 32, deep
ABO_STRIKE = [(680, 782), (460, 868)]           # S13 « résilier » : diagonale, droite -> gauche (monde)

# --- les trois autres petites actions (cartes en tirets), chacune garée au-dessus de SA marche (revue 1) ---
OPT_W, OPT_H = 200, 104
OPT_C = {"opt_virement": (640, 875), "opt_frais": (470, 760), "opt_projet": (300, 645)}   # escalier de tâches
OPT_FROM = {"opt_virement": NUM_PTS[1], "opt_frais": NUM_PTS[2], "opt_projet": NUM_PTS[3]}
OPT_NUM_LOCAL = {"opt_virement": (-70, 52), "opt_frais": (-70, 52), "opt_projet": (70, 52)}   # sur le bord bas
OPT_TXT_LOCAL = (0, 0)                          # texte Bold 34 sur deux lignes (plus de pictogramme : moins chargé)

ECART_Y, ECART_X0 = 1256, 622                   # S09 : l'écart tour -> « Toi », au sol (contrôle sans son)
ECART_TOE = 59                                  # du centre de « Toi » au bord avant de son pied
DROP_OUT = 13                                   # S13 : la carte barrée tombe hors champ (ease-in)

# --- le segment d'énergie (en vol : 2 x, 150 x 88 ; il se réduit à 75 x 44 en s'emboîtant) ---
ELAN_W, ELAN_H = 75, 44
ELAN_FLY_K = 2.0
ELAN_TRAIL_OP = (0.5, 0.32, 0.18)
ELAN_TRAIL_LAG = (2, 4, 6)

# --- la tour fantôme (S17-S18) : à l'échelle de la vraie tour (revue 1), en l'air à droite de l'escalier ---
FANTOME_X, FANTOME_W, FANTOME_BOT = 780, 280, 1025  # x 640-920, y 625-1025 (posée plus bas : face aux marches)
FANTOME_IDS = [f"fantome{i + 1}" for i in range(4)]
FANTOME_NOM_C = (780, 1062)                     # « Grand plan » sous la tour fantôme
FANTOME_SLOT_LOCAL = (60, 0)                    # case de coche vide, en tirets, sur chaque bloc
FANTOME_FROM = (790, 1180)                      # sort du bout droit du bloc B1 (et y rentre en S18)


def fantome_c(i):
    return [FANTOME_X, FANTOME_BOT - 100 * (i + 0.5)]

# --- la barre de l'année (S18) ---
ANNEE_C, ANNEE_W, ANNEE_H = (540, 560), 720, 44  # x 180-900
ANNEE_S1, ANNEE_FIN = (180, 614), (900, 614)     # légendes (ancres start / end)
COMPTEUR_C, DECISIONS_C = (520, 455), (540, 466)  # compteur ancré à droite ; « décisions » ancré à gauche
ANNEE_CASES = [(round(180 + ANNEE_W / 52 * (k + 0.5), 1), 560) for k in range(3)]   # 3 premières cases

REMBOBINE_C = (560, 660)                        # S19-S20 : ◀◀ / ▶▶ géants, au centre de l'action
CADRAN_ATTENTE = (830, 770)                     # S19 : l'horloge tourne au-dessus de « Toi » qui attend

# --- la fin (kit.outro) : carte (540, 760) ; toucher au stylo, pas de souris (modèle : V14 p3) ---
FIN_C = (540, 760)
FIN_TAP = (700, 955)                            # dans le bouton (x 350-730, y 852-964), hors du libellé


def scene_f0(S, sid):
    return round(next(s for s in S.sb["scenes"] if s["id"] == sid)["t_start"] * S.fps)


def film_end(S):
    """Première image après le film (fin de la dernière scène du storyboard)."""
    return round(S.sb["scenes"][-1]["t_end"] * S.fps)


# ---------- l'allonge de « Toi » (bras gauche, échelle 1) ----------
def arm_dist(fig, pt):
    sx, sy = fig[0] + SHOULDER[0] * FIG_S, fig[1] + SHOULDER[1] * FIG_S
    return round(math.hypot(pt[0] - sx, pt[1] - sy), 1)


def assert_reach(fig, pt, what):
    d = arm_dist(fig, pt)
    assert REACH_MIN <= d <= REACH_OK, f"{what} : hors d'allonge depuis {fig} : {d} px"


for _fig, _pt, _what in [(TOI_P0, PASTILLE_TAP0, "S01 toucher la pastille"),
                         (TOI_P0, PASTILLE_MAIN_TIP, "S01 tenir la pastille au bout du stylo"),
                         (TOI_POUSSE, (622, 1030), "S08 pousser la tour"),
                         (TOI_P0, PASTILLE_FLECHIE_TIP, "S02 bras fléchi"),
                         (TOI_TIRE, (622, 1170), "S10 saisir le bord de B1"),
                         (TOI_P0, (790, 1170), "S10 bord de B1 tiré jusqu'aux pieds"),
                         (TOI_P0, NUM_PTS[0], "S11 écrire « 1 »"),
                         (TOI_M1, NUM_PTS[1], "S12 écrire « 2 »"),
                         (TOI_M1, ABO_STRIKE[0], "S13 barrer (départ)"),
                         (TOI_M1, ABO_STRIKE[1], "S13 barrer (fin)"),
                         (TOI_M1, COCHE_PTS[0], "S13 / S20 cocher la marche 1"),
                         (TOI_M1, NUM_PTS[0], "S20 réécrire « 1 »"),
                         (TOI_M2, COCHE_PTS[1], "S16 cocher la marche 2"),
                         (TOI_M2, NUM_PTS[2], "S16 écrire « 3 »"),
                         (TOI_M3, COCHE_PTS[2], "S17 cocher la marche 3"),
                         (TOI_M1, PASTILLE_RETOUR_TIP, "S21 recevoir l'argent"),
                         (TOI_P0, FIN_TAP, "S22 toucher le bouton")]:
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
         shadow=6, **p):
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


def set_blocks(S, f, d, e, geoms, children=True):
    """Pose les 4 blocs sur `geoms` (liste de (centre, w, h)) avec la même clé (f, d, e), enfants compris."""
    for i, (c, w, h) in enumerate(geoms):
        S.keys(BLOC_IDS[i], f, d, e, pos=list(c), w=w, h=h)
        if children:
            ico, nom = block_children(w)
            S.key(BLOC_ICO[i], "pos", f, ico, d, e)
            S.key(BLOC_NOM[i], "pos", f, nom, d, e)
    return f + d


# ---------- revue 1 : petites macros de la série V15 (pistes et entités de la distribution seulement) ----------
def cal_swap(S, kit, f, text, d_w=6, pulse=True, extra_w=0):
    """La pilule-calendrier bascule sur `text` SANS image vide ni débordement : l'ancien libellé s'efface en 2 images
    pendant que la largeur part vers celle du nouveau (d_w images, ease-out) ; le nouveau libellé paraît à f + 2 et
    revient à pleine opacité en 4 images, quand la largeur est presque atteinte. Bat x1,1 (pulse)."""
    kit.ensure("calendrier", "textOp", 1)
    S.key("calendrier", "textOp", f, 0, 2, "out")
    S.key("calendrier", "w", f, cal_w(text) + extra_w, d_w, "out")
    S.key("calendrier", "text", f + 2, text)
    S.key("calendrier", "textOp", f + 2, 1, 4, "out")
    if pulse:
        kit.pulse("calendrier", f, peak=1.1, step=3)
    return f + max(d_w, 6)


def marks(S, f, segs, hold=4, d=2):
    """Traits courts encre (vitesse, impact, poussière) : `segs` = [(point monde, angle°), ...] (3 au plus, entités
    vite1-3) ; ils se tracent en d images à f, restent `hold` images, puis se rétractent en 3 images. -> fin."""
    for k, (pt, ang) in enumerate(segs):
        id = f"vite{k + 1}"
        S.key(id, "pos", f - 1, r3(pt))
        S.key(id, "rot", f - 1, ang)
        S.key(id, "draw", f - 1, 0)
        S.key(id, "draw", f, 1, d, "out")
        S.key(id, "draw", f + d + hold, 0, 3, "in")
    return f + d + hold + 3


def stepped(S, id, track, f, d, to, e="inOut", step=2):
    """Comme S.key(id, track, f, to, d, e) mais par paliers de `step` images (cadence de rembobinage)."""
    v0 = S.val(id, track, f - 1)
    for n, p in frames(f, d, e):
        if (n - f) % step == step - 1 or n == f + d - 1:
            v = [round(lerp(a, b, p), 3) for a, b in zip(v0, to)] if isinstance(to, (list, tuple)) else \
                round(v0 + (to - v0) * p, 4)
            S.key(id, track, n, list(v) if isinstance(v, list) else v)
    return f + d


def elan_fly(S, kit, id, f, frm, quart, value, d=13, arc=120):
    """Le segment d'énergie (revue 1 : 2 x plus grand en vol, traînée de 3 fantômes) : la coche bat x1,3 au départ ; le
    segment naît sur elle à 2 x (pop 4 images), vole en arc s'emboîter dans son quart de jauge en d images en se
    réduisant à sa taille (75 x 44) ; la jauge monte d'un quart au contact et le segment s'y fond. -> arrivée."""
    S.key(id, "pos", f - 1, list(frm))
    kit.pop(id, f, scale=ELAN_FLY_K, d=4)
    arr = kit.move(id, f + 1, list(quart), d, "inOut", arc=arc, scale=1)
    S.key("energie", "value", arr, value, 4, "out")
    kit.pulse("energie", arr, peak=1.12, step=3)   # contrôle sans son : la jauge bat quand le segment s'emboîte
    S.key(id, "scale", arr + 2, 0, 2, "in")
    S.key(id, "opacity", arr + 4, 0)
    for g, lag in enumerate(ELAN_TRAIL_LAG):    # traînée : la même course, en retard de 2 / 4 / 6 images
        tid = f"{id}_t{g + 1}"
        for n in range(f - 1, arr + lag + 1):
            m = min(n - lag, arr)
            S.key(tid, "pos", n, r3(S.val(id, "pos", m)))
            S.key(tid, "scale", n, round(S.val(id, "scale", m) if f + lag <= n < arr + lag else 0, 4))
    return arr


def count_rings(S, kit, f, k):
    """Une coche compte (S17 « avancé », S18 « décision ») : une onde deep part de la coche k et la marche k bat."""
    ring(S, f"coche_onde{k + 1}", f, d=12, s0=0.6, s1=2.0)
    kit.pulse(BLOC_IDS[k], f, peak=1.06)
    return f + 12


def number(kit, id, pos, digit, dashed=False, r=NUM_R, size=36, z=7.5, parent=None):
    """Numéro cerclé deep : cercle (draw 0 -> 1 si plein ; tirets [8, 6] et scale 0 si « à faire ») + chiffre enfant
    (typed)."""
    if dashed:
        kit.shape(id, list(pos), kind="circle", w=2 * r, fill="none", stroke=DEEP, sw=4, dash=[8, 6], shadow=0, z=z,
                  parent=parent, scale=0)
        kit.text(f"{id}_txt", [0, 1], digit, size=size, weight=800, color=DEEP, z=z + 0.05, parent=id)
    else:
        kit.shape(id, list(pos), kind="circle", w=2 * r, fill="none", stroke=DEEP, sw=4, shadow=0, z=z, parent=parent,
                  draw=0)
        kit.text(f"{id}_txt", [0, 1], digit, size=size, weight=800, color=DEEP, z=z + 0.05, parent=id, typed=True)
    return id


# ---------- raccords (contrat des parties ; couleurs en hex minuscule : S.val rend du minuscule) ----------
def _lo(c):
    return c.lower()


_OFF = lambda *ids: {i: {"scale": 0} for i in ids}   # noqa: E731
_TOWER100 = [tower(i, 100) for i in range(4)]
_STAIRS = [stairs(i) for i in range(4)]


def _blocks_state(geoms, fills):
    st = {}
    for i, (c, w, h) in enumerate(geoms):
        ico, nom = block_children(w)
        st[BLOC_IDS[i]] = {"pos": list(c), "w": w, "h": h, "scale": 1, "fill": _lo(fills[i])}
        st[BLOC_ICO[i]] = {"pos": ico, "scale": 1}
        st[BLOC_NOM[i]] = {"pos": nom, "chars": len(T_BLOCS[i])}
    return st


ENTRY_P2 = {   # fin de S08 = etat_initial de S09 (image 899)
    "pastille": {"pos": list(PASTILLE_TOUR[100]), "scale": 1, "rot": 0, "text": T_ARGENT, "w": PASTILLE_W},
    **_blocks_state(_TOWER100, [PAPER] * 4),
    "accolade": {"pos": list(ACCOLADE_O), "draw": 1, "sy": 1, "scale": 1},
    "gp_nom": {"pos": list(GP_NOM_C[100]), "chars": len(T_GRAND_PLAN.replace("\n", "")), "scale": 1},
    **{q: {"pos": list(Q_NUEE[k]), "scale": 1} for k, q in enumerate(Q_IDS)},
    "energie": {"pos": list(ENERGIE_C), "scale": 1, "value": 0, "fill": _lo(RED)},
    "energie_nom": {"opacity": 1},
    "calendrier": {"pos": list(CAL_C), "scale": CAL_K, "text": T_CAL["lundi"], "w": cal_w(T_CAL["lundi"]),
                   "fill": _lo(LIGHT), "textOp": 1},
    "cal_alerte": {"opacity": 0}, "cal_rewind": {"scale": 0},
    "cadran": {"scale": 0},                     # valeur et place : posées par la partie qui le ressort (f - 1)
    **_OFF("apercu", "grand_q", "ecart"),
    "nom_toi": {"pos": list(NOM_SOL)},
}

ENTRY_P3 = {   # fin de S16 = etat_initial de S17 (image 1745)
    "pastille": {"pos": list(PASTILLE_ESCALIER), "scale": 1, "rot": 0, "text": T_ARGENT, "w": PASTILLE_W},
    **_blocks_state(_STAIRS, [LIGHT, PAPER, PAPER, PAPER]),
    "accolade": {"scale": 0}, "gp_nom": {"scale": 0},
    **{n: {"scale": 1, "draw": 1} for n in ("num1", "num2", "num3")},
    **{f"{n}_txt": {"chars": 1} for n in ("num1", "num2", "num3")},
    "coche1": {"draw": 1}, "coche2": {"draw": 1}, "coche3": {"draw": 0},
    "energie": {"pos": list(ENERGIE_C), "scale": 1, "value": 0.5, "fill": _lo(CYAN)},
    "energie_nom": {"opacity": 1},
    "calendrier": {"pos": list(CAL_C), "scale": CAL_K, "text": T_CAL["s2"], "w": cal_w(T_CAL["s2"]),
                   "fill": _lo(LIGHT), "textOp": 1},
    "cal_alerte": {"opacity": 0}, "cal_rewind": {"scale": 0},
    "cadran": {"scale": 0}, "cadran_txt": {"scale": 0},
    **_OFF("elan1", "elan2", "elan3", "abonnement", "opt_virement", "opt_frais", "opt_projet", "apercu", "grand_q",
           "numt2", "numt3", "numt4", *Q_IDS, "chrono", "cadran_we", "cadran_we_txt", "ecart",
           *[f"elan{k}_t{g}" for k in (1, 2) for g in (1, 2, 3)]),
    **{f"{o}_lien": {"draw": 0} for o in ("opt_virement", "opt_frais", "opt_projet")},
    "nom_toi": {"pos": list(NOM_MARCHE)},
}


def cast(S, kit):
    """Toute la distribution, à son état de l'image 0. Ce qui arrive plus tard : scale=0 (ou draw=0, chars=0,
    opacity=0). Seuls `fin` et son curseur naissent dans kit.outro (p3)."""

    # --- le sol ---
    kit.shape("sol", [(SOL_X0 + SOL_X1) / 2, SOL_Y], kind="round", w=SOL_X1 - SOL_X0, h=4, r=2, fill=INK,
              stroke="none", sw=0, shadow=0, z=2)

    # --- « Toi » (encre, échelle 1, visible dès l'image 0) et son étiquette (enfant) ; bras baissé au repos ---
    toi = Toi(kit, "toi", pos=list(TOI_P0), scale=FIG_S, variant="ink", side="left", show=True)
    toi.low_grip, toi.low_rot = TOI_LOW_GRIP, TOI_LOW_ROT
    kit.ensure("toi", "look", 0)
    pill(S, "nom_toi", NOM_SOL, T_TOI, size=34, fill=LIGHT, h=NOM_H, w=NOM_W, z=15.8, parent="toi", scale=1, sw=3,
         shadow=4)

    # --- la pastille « Ton argent » (objet du fil, monde) ---
    pill(S, "pastille", PASTILLE_SOL0, T_ARGENT, size=PASTILLE_SIZE, fill=CYAN, h=PASTILLE_H, w=PASTILLE_W, z=12.5,
         scale=1, icon="euro")
    S.set("pastille", rot=0)

    # --- les 4 blocs du grand plan (cachés ; ils poussent du sol en S03 : h 0 -> 100 avec pos) ---
    for i in range(4):
        c, w, h = tower(i, 100)
        kit.shape(BLOC_IDS[i], c, kind="round", w=w, h=h, r=14, fill=PAPER, stroke=INK, sw=4, shadow=6,
                  z=round(6 + 0.01 * i, 2), scale=0)
        S.set(BLOC_IDS[i], w=w, h=h, fill=PAPER)        # hex : PAPER <-> LIGHT (marche choisie)
        ico, nom = block_children(w)
        kit.icon(BLOC_ICO[i], ico, ICO_BLOCS[i], disc=22, fill=CYAN, color=INK, shadow=3, z=round(6.1 + 0.01 * i, 2),
                 parent=BLOC_IDS[i], scale=0)
        kit.text(BLOC_NOM[i], nom, T_BLOCS[i], size=34, weight=700, anchor="start", z=round(6.15 + 0.01 * i, 2),
                 parent=BLOC_IDS[i], typed=True)

    # --- la petite marche « 1 » de l'annonce (derrière B1, cachée) ---
    kit.shape("apercu", list(APERCU_C), kind="round", w=APERCU_W, h=APERCU_H, r=14, fill=LIGHT, stroke=DEEP, sw=4,
              dash=[14, 10], shadow=0, z=5.9, scale=0)
    kit.text("apercu_txt", [0, 2], "1", size=56, weight=800, color=DEEP, z=5.95, parent="apercu")

    # --- l'accolade « Grand plan » ---
    line(kit, "accolade", ACCOLADE_PTS, color=DEEP, sw=5, z=6.5, pos=ACCOLADE_O)
    S.set("accolade", sy=1)
    kit.text("gp_nom", list(GP_NOM_C[100]), T_GRAND_PLAN, size=40, weight=700, z=6.5, typed=True, lh=1.1)

    # --- la pilule-calendrier (cachée ; tombe en S01), son libellé d'alerte, son ◀◀ ---
    pill(S, "calendrier", CAL_C, T_CAL["weekend"], size=34, fill=LIGHT, h=64, z=20, scale=0, icon="cal",
         w=cal_w(T_CAL["weekend"]))
    S.set("calendrier", fill=LIGHT)                 # hex : LIGHT -> RED (« Plus tard ») -> LIGHT
    kit.text("cal_alerte", [15, 0], T_CAL["tard"], size=34, weight=700, color=PAPER, z=20.3, parent="calendrier",
             opacity=0)
    kit.shape("cal_rewind", [cal_icon_x(T_CAL["avant"]), 0], kind="circle", w=34, fill=LIGHT, stroke="none", sw=0,
              shadow=0, z=20.1, parent="calendrier", scale=0)
    kit.icon("cal_rewind_ico", [0, 0], "rewind", s=26, color=INK, z=20.2, parent="cal_rewind")

    # --- l'horloge (secteur deep, aiguille) et sa légende ---
    kit.sector("cadran", list(CADRAN_CAL), start=0, value=0, r=CADRAN_R, unit=60, face=PAPER, fill=DEEP, ticks=12,
               hand=True, sw=5, shadow=6, z=19, scale=0)
    kit.text("cadran_txt", list(CADRAN_TXT_LOCAL), T_DIX, size=34, weight=700, color=DEEP, z=19.1, parent="cadran",
             scale=0)

    # --- la jauge « Énergie » (pleine, cachée ; sort de la tête de « Toi » en S07) ---
    kit.gauge("energie", list(ENERGIE_C), value=1, w=ENERGIE_W, h=ENERGIE_H, segments=4, fill=CYAN, empty=PAPER,
              sw=4, shadow=6, z=20, scale=0)
    S.set("energie", fill=CYAN)                     # hex : CYAN -> RED en se vidant (S08) ; CYAN de nouveau (S15)
    kit.text("energie_nom", list(ENERGIE_NOM), T_ENERGIE, size=34, weight=700, anchor="end", z=20, opacity=0)
    kit.icon("energie_bolt", list(ENERGIE_BOLT_LOCAL), "bolt", disc=ENERGIE_BOLT_R, fill=CYAN, color=INK, shadow=3,
             z=20.05, parent="energie")

    # --- S09 : l'écart au sol entre la tour et « Toi » (trait encre et deux butées) ---
    kit.shape("ecart", [ECART_X0 + 25, ECART_Y], kind="round", w=50, h=8, r=4, fill=INK, stroke="none", sw=0,
              shadow=0, z=3, scale=0)
    S.set("ecart", w=50)
    for k, sg in enumerate((-1, 1)):
        kit.shape(f"ecart_{'gd'[k]}", [sg * 25, 0], kind="round", w=8, h=32, r=4, fill=INK, stroke="none", sw=0,
                  shadow=0, z=3.05, parent="ecart")

    # --- les « ? » : le grand (S07), les huit petits (S08, au centre de leur bloc, deux par bloc) ---
    S.add("grand_q", "qmark", z=13)
    S.set("grand_q", pos=list(GRAND_Q_C), scale=0, opacity=1, gs=GRAND_Q_GS)
    for k, q in enumerate(Q_IDS):
        c = tower(k // 2, 100)[0]
        kit.text(q, [c[0] + (-40 if k % 2 == 0 else 40), c[1]], "?", size=Q_SIZE, weight=800, z=13.1, scale=0)

    # --- numéros sur les marches : notés (plein, tracés au stylo) et « à faire » (tirets) ---
    for k in range(3):
        number(kit, f"num{k + 1}", NUM_PTS[k], str(k + 1))
    for k in range(1, 4):
        number(kit, f"numt{k + 1}", NUM_PTS[k], str(k + 1), dashed=True, **({"r": NUM4_R, "size": 30} if k == 3 else {}))

    # --- coches de « Toi » (pleines, deep) et le bilan « 3 ✓ » ---
    for k in range(3):
        kit.tick(f"coche{k + 1}", list(COCHE_PTS[k]), DEEP, size=COCHE_SIZE, sw=8, z=7.6)
    kit.text("bilan3", [BILAN3_C[0] - BILAN_DX, BILAN3_C[1]], "3", size=BILAN_SIZE, weight=800, color=DEEP, z=13, scale=0)
    kit.tick("bilan3_coche", [BILAN3_C[0] + BILAN_DX, BILAN3_C[1]], DEEP, size=BILAN_TICK, sw=10, z=13.05, draw=1)
    S.set("bilan3_coche", scale=0)
    for k in range(3):                              # S17 / S18 : une onde part de chaque coche quand elle compte
        kit.shape(f"coche_onde{k + 1}", list(COCHE_PTS[k]), kind="circle", w=60, fill="none", stroke=DEEP, sw=5,
                  shadow=0, z=7.7, opacity=0)
    for k in range(3):                              # S18 : un double de chaque coche vole remplir une case de l'année
        kit.tick(f"coche_double{k + 1}", list(COCHE_PTS[k]), DEEP, size=COCHE_SIZE, sw=8, z=22, draw=1)
        S.set(f"coche_double{k + 1}", scale=0)

    # --- les segments d'énergie (un par marche cochée) ---
    for k in range(3):
        kit.shape(f"elan{k + 1}", list(COCHE_PTS[k]), kind="round", w=ELAN_W, h=ELAN_H, r=6, fill=CYAN, stroke=INK,
                  sw=4, shadow=3, z=21, scale=0)
        for g, op in enumerate(ELAN_TRAIL_OP):      # traînée : 3 fantômes cyan qui suivent le segment en vol
            kit.shape(f"elan{k + 1}_t{g + 1}", list(COCHE_PTS[k]), kind="round", w=ELAN_W, h=ELAN_H, r=6, fill=CYAN,
                      stroke="none", sw=0, shadow=0, z=20.9 - 0.01 * g, scale=0, opacity=op)

    # --- l'abonnement inutile : carte plate (papier, contour encre), pictogramme repeat, prix, trait (enfants) ---
    kit.shape("abonnement", list(ABO_C), kind="round", w=ABO_W, h=ABO_H, r=18, fill=PAPER, stroke=INK, sw=4, shadow=6,
              z=14, scale=0)
    kit.icon("abonnement_ico", list(ABO_ICO_LOCAL), "repeat", disc=28, fill=CYAN, color=INK, shadow=3, z=14.05,
             parent="abonnement")
    kit.text("abonnement_txt", list(ABO_TXT_LOCAL), T_ABO, size=34, weight=700, anchor="start", z=14.1,
             parent="abonnement", lh=1.15)
    kit.text("abonnement_prix", list(ABO_PRIX_LOCAL), T_ABO_PRIX, size=32, weight=700, color=DEEP, z=14.1,
             parent="abonnement")
    line(kit, "abonnement_trait", [(ABO_STRIKE[0][0] - ABO_C[0], ABO_STRIKE[0][1] - ABO_C[1]),
                                   (ABO_STRIKE[1][0] - ABO_C[0], ABO_STRIKE[1][1] - ABO_C[1])],
         color=INK, sw=7, z=14.2, parent="abonnement")
    abo = None

    # --- les trois autres petites actions (cartes en tirets, numérotées comme leur marche) ---
    for oid, txt, ico, digit in T_OPTIONS:
        kit.shape(oid, list(OPT_C[oid]), kind="round", w=OPT_W, h=OPT_H, r=16, fill=PAPER, stroke=DEEP, sw=4,
                  dash=[14, 10], shadow=0, z=12.2, scale=0)          # sous la pastille (12,5) : en redescendant
        kit.text(f"{oid}_txt", list(OPT_TXT_LOCAL), txt, size=34, weight=700, z=12.25, parent=oid, lh=1.1)
        kit.shape(f"{oid}_num", list(OPT_NUM_LOCAL[oid]), kind="circle", w=44, fill=PAPER, stroke=DEEP, sw=4,
                  dash=[8, 6], shadow=0, z=12.3, parent=oid)
        kit.text(f"{oid}_num_txt", [0, 1], digit, size=30, weight=800, color=DEEP, z=12.35, parent=f"{oid}_num")
        a = [OPT_C[oid][0] + OPT_NUM_LOCAL[oid][0], OPT_C[oid][1] + OPT_NUM_LOCAL[oid][1]]   # fil : badge -> marche
        b = OPT_FROM[oid]
        line(kit, f"{oid}_lien", [(0, 0), (b[0] - a[0], b[1] - a[1])], color=DEEP, sw=3, z=12.1, pos=a, dash=[8, 7])

    # --- la tour fantôme du grand plan, son nom, « 0 ✓ » rouge (S17-S18) ---
    for i in range(4):
        fid = FANTOME_IDS[i]
        kit.shape(fid, fantome_c(i), kind="round", w=FANTOME_W, h=100, r=14, fill="none", stroke=INK, sw=5,
                  dash=[12, 10], shadow=0, z=6, scale=0)
        kit.icon(f"{fid}_ico", [round(-FANTOME_W / 2 + ICO_DX, 1), 0], ICO_BLOCS[i], s=40, color=INK, z=6.05,
                 parent=fid)
        kit.shape(f"{fid}_case", list(FANTOME_SLOT_LOCAL), kind="round", w=50, h=50, r=8, fill="none", stroke=INK,
                  sw=4, dash=[8, 7], shadow=0, z=6.06, parent=fid)
    kit.text("fantome_nom", list(FANTOME_NOM_C), T_GRAND_PLAN.replace("\n", " "), size=34, weight=700, z=6.1,
             scale=0)
    kit.text("zero", [ZERO_C[0] - BILAN_DX, ZERO_C[1]], "0", size=BILAN_SIZE, weight=800, color=RED, z=13, scale=0)
    kit.tick("zero_coche", [ZERO_C[0] + BILAN_DX, ZERO_C[1]], INK, size=BILAN_TICK, sw=10, z=13.05, draw=1)
    S.set("zero_coche", scale=0)

    # --- la barre de l'année, ses légendes, le compteur, « décisions » (S18) ---
    kit.gauge("annee", list(ANNEE_C), value=0, w=ANNEE_W, h=ANNEE_H, segments=13, fill=CYAN, empty=PAPER, sw=4,
              shadow=6, z=21, scale=0)
    kit.text("annee_s1", list(ANNEE_S1), T_SEMAINE1, size=34, weight=700, anchor="start", z=21, typed=True)
    kit.text("annee_fin", list(ANNEE_FIN), T_FIN_ANNEE, size=34, weight=700, anchor="end", z=21, typed=True)
    kit.counter("compteur", list(COMPTEUR_C), value=3, size=110, weight=800, color=DEEP, anchor="end", z=21, scale=0)
    kit.text("decisions", list(DECISIONS_C), T_DECISIONS, size=44, weight=700, anchor="start", z=21, typed=True)

    # --- revue 1 : traînée de la jauge (S07), traits de vitesse / d'impact / de poussière (réutilisés), petite
    #     horloge des montées, tour complet fantôme du week-end (S13), ◀◀ / ▶▶ géants (S19-S20), voile du rembobinage ---
    line(kit, "energie_trace", [(0, 0), (ENERGIE_C[0] - ENERGIE_GRAND_C[0], ENERGIE_C[1] - ENERGIE_GRAND_C[1])],
         color=DEEP, sw=4, z=19.5, pos=ENERGIE_GRAND_C, dash=[10, 9])
    for k in range(3):
        line(kit, f"vite{k + 1}", [(-18, 0), (18, 0)], color=INK, sw=6, z=16.5)
    kit.sector("chrono", [0, 0], start=0, value=0, r=CHRONO_R, unit=60, face=PAPER, fill=DEEP, ticks=4, hand=True,
               sw=4, shadow=3, z=19, scale=0)
    kit.shape("cadran_we", list(CADRAN_TOI), kind="circle", w=2 * CADRAN_WE_R, fill="none", stroke=INK, sw=4,
              dash=[10, 9], shadow=0, z=18.9, scale=0, opacity=0.45)
    kit.text("cadran_we_txt", list(CADRAN_WE_TXT), T_WEEKEND, size=32, weight=700, z=18.9, scale=0)
    kit.icon("rembobine", list(REMBOBINE_C), "rewind", s=170, color=INK, z=30, scale=0)
    kit.icon("avance", list(REMBOBINE_C), "rewind", s=170, color=INK, z=30, scale=0)
    S.set("avance", rot=180)                        # ▶▶ : le même pictogramme retourné
    kit.shape("voile", [540, 960], kind="rect", w=1080, h=1920, fill=INK, stroke="none", sw=0, shadow=0, z=1.5,
              opacity=0)

    # --- la fin : ondes du toucher du stylo (le curseur de kit.outro reste invisible) ---
    for k in range(2):
        kit.shape(f"fin_onde{k + 1}", list(FIN_TAP), kind="circle", w=60, fill="none", stroke=DEEP, sw=5, shadow=0,
                  z=41.9, opacity=0)

    return SimpleNamespace(toi=toi, abo=abo, blocs=BLOC_IDS, bloc_ico=BLOC_ICO, bloc_nom=BLOC_NOM, q=Q_IDS,
                           fantome=FANTOME_IDS, options=[o[0] for o in T_OPTIONS])


def build(S):
    kit = Kit(S)
    c = cast(S, kit)
    only = [p for p in os.environ.get("WTH_PARTS", "").split(",") if p]   # WTH_PARTS=p2 : cette partie seule
    for name in PARTS:
        if not only or name in only:
            importlib.import_module(f".{name}", __name__).part(S, kit, c)
