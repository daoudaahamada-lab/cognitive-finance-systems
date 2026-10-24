"""V10 « Offre urgente : le moment de ralentir » : mise en scène Story, en paquet (une partie par fichier).

Storyboard : scripts/storyboards/V10.json (v1, révisé après le test sans son, 22 scènes, 96 temps forts, 94,966 s),
version lisible scripts/storyboards/V10.md. Voix : build/V10/words.json (film : images 0-2848, FILM_END = 2849).
Fil : la pastille cyan « Ton argent » (`pastille`, pill 300 x 84, pictogramme euro, ExtraBold 40), à côté de « Toi »
dès l'image 0 ; accrochée par le crochet rouge de l'offre (S02, S05-S07), retenue dans le coin avec l'offre (S12),
libérée quand le crochet casse (S15), reprise par le crochet du téléphone (S16-S17), relâchée quand la façade tombe
(S18), gardée en grand (S21), bouton « S’abonner » (S22).
Parti pris : le compte à rebours rouge qu'on reprend en main (pause, rallonge cyan « Quelques jours ») ; ce délai
devient le champ de recherche qui consulte les registres ; puis la façade qu'on arrache.

Parties (scènes contiguës ; p2/p3 coupées sur un morph, p1/p2 sur l'entrée du piège 1 où le repère s'allume) :
- p1 : S01-S07, images 0-867 (29 temps forts, 28,9 s). Accroche, annonce, contexte, premier geste sur le temps.
- p2 : S08-S15, images 868-1850 (32 temps forts, 32,8 s). Piège 1 (délai) et piège 2 (registres, liste noire).
- p3 : S16-S22, images 1851-2848 (35 temps forts, 33,3 s). Piège 3 (façade), alertes, bouée, chute, fin.
ENTRY_P2 et ENTRY_P3 sont le contrat des raccords (kit.pin(f0 - 1, …)). Les figurines n'y sont jamais.

GÉOMÉTRIE DE « Toi » (raison de la mise en page, vérifiée par assert_reach) : bras gauche, épaule à (x − 30, 1119).
Il ne touche proprement qu'une cible à sa gauche (|dx| >= 0,3 x dy) à 267 px au plus, sinon le bras passe par la
tête. La barre (y 900) est donc décalée à gauche du storyboard (x 128-528 au lieu de 200-640) et la rallonge va de
528 à 780 : « Toi » la TIRE en reculant (`drag`, corps et pointe glissent ensemble, pointe à 70 px de l'épaule) :
P2 628 (S01-S07, au bout de la barre) -> P_S07 754 (rallonge à mi-course) -> P_FAR 880 (S09-S15, rallonge au bout) ;
S16 « Mais » : walk_low vers P3 650 (S16-S22). Entre deux gestes, son bras est BAISSÉ (`lower`, `walk_low`).
L'interlocuteur : figurine papier sans outil (Figure tool=False, side « right », il regarde « Toi ») en (190, 1135),
entré en S05 ; son nom `nom_inter`, son étiquette `verdict` et la pilule `conseiller` sont ses enfants (ils sortent
avec lui en S21).
Rouge : le compte à rebours et ses crochets, « n° 1 des arnaques », le bouton enfoncé, l'accolade, « Délai refusé »,
« Absent », le verdict, le vrai nom, les alertes, la case qui refuse (S21) ; karaoké : ALERT_WORDS. Aucun gris.
Pas d'IA dans V10. Aucune entité nouvelle : tout se compose avec le catalogue (voir chaque bloc de cast).
"""
import importlib
import math
import os
from types import SimpleNamespace

from pipeline.story import GEOM, STYLE, text_width
from pipeline.story_kit import WALK_LEAN, Figure, Kit, ang_lerp, frames, lerp, solve_ik

PARTS = ["p1", "p2", "p3"]                      # S01-S07, S08-S15, S16-S22
NBSP = " "                                 # espace insécable
ALERT_WORDS = {"arnaques", "refuse", "noires"}  # karaoké en rouge : l'arme n° 1 (S06), le refus (S10, S21), la liste noire (S14)
ACOUSTIC_SNAP = {"gap": 0.2, "window": 0.08}    # temps fort après un silence : calé sur l'attaque audible
# découpes imposées (revue 1) : pas de locution, de négation ni de nom de service coupés ; pas de mot seul éclair
CAPTION_GROUPS = [
    ["Parce que", "la pression du temps", "t’empêche", "de vérifier l’offre", "et ton interlocuteur"],
    ["C’est l’arme", "numéro un", "des arnaques", "financières"],
    ["Le premier réflexe", "c’est donc", "de reprendre la main", "sur le temps"],
    ["Premier piège", "décider dans la journée"],
    ["Une vraie opportunité", "supporte", "quelques jours", "de réflexion"],
    ["Si on te refuse", "ce délai"],
    ["Pour un", "établissement financier", "consulte le registre", "REGAFI"],
    ["Regarde aussi", "les listes noires", "de l’AMF"],
    ["Un paiement", "en crypto", "ou vers un compte", "à l’étranger"],
    ["Au moindre doute", "contacte", "Assurance Banque", "Épargne Info Service"],
    ["Et retiens", "une opportunité", "qui refuse", "la vérification", "ne mérite pas", "ton argent"],
]

FILM_END = 2849                                 # images 0-2848 (94,966 s)

# ---------- couleurs ----------
INK, CYAN, DEEP, LIGHT = STYLE["ink"], STYLE["cyan"], STYLE["deep"], STYLE["light"]
PAPER, RED, BG = STYLE["paper"], STYLE["red"], STYLE["bg"]

# ---------- textes à l'écran (typographie française : insécable avant ? et dans « n° 1 », apostrophe ’) ----------
T_TOI, T_ARGENT, T_ABONNER = "Toi", "Ton argent", "S’abonner"
T_OFFRE, T_OFFRE_LIGNE, T_INVESTIS = "Offre réservée", "jusqu’à ce soir minuit", "J’investis"
T_MAINTENANT, T_MINUIT = "maintenant", "minuit"
T_N1, T_ARNAQUES = f"n°{NBSP}1", "des arnaques"
T_VERIFIER, T_MINUTES = "Vérifier", "Quelques minutes"
T_JOURNEE, T_JOURS, T_REFUS = "Dans la journée", "Quelques jours", "Délai refusé"
T_INTER = "Invest Minuit"                       # nom fictif
T_AUTORISE_Q, T_NON_AUTORISE = f"Autorisé{NBSP}?", "Non autorisé"
T_REGAFI, T_REGAFI_SOUS = "REGAFI", "Établissement financier"
T_ORIAS, T_ORIAS_SOUS = "ORIAS", "Intermédiaire"
T_ABSENT, T_LISTE, T_AMF = "Absent", "Liste noire", "AMF"
T_CONSEILLER, T_BANQUE_NAT = "Conseiller", "Banque\nNationalis"   # nom inventé (aucun établissement réel)
T_ALERTES = [("Rendement", "élevé", "garanti"), ("Contact", "non sollicité", None), ("Paiement", "en crypto", None),
             ("Compte", "à l’étranger", None)]
T_BOUEE1, T_BOUEE2 = "Assurance Banque", "Épargne Info Service"
MARKER_LABELS = ["Délai", "Registres", "Apparence"]

# ---------- mise en page (1080 x 1920) ----------
X_MIN, X_MAX, Y_MIN, Y_MAX = 40, 940, 160, 1270
GROUND = 1230                                   # pieds de « Toi » et de l'interlocuteur
FIG_BASE = GEOM["FIGURE"]["base"]
HEAD_DY = GEOM["FIGURE"]["head"]["cy"]          # -64 : centre de la tête
HEAD_R = GEOM["FIGURE"]["head"]["r"]
SHOULDER_DX, SHOULDER_DY = abs(GEOM["FIGURE"]["shoulder"][0]), GEOM["FIGURE"]["shoulder"][1]   # 30, -16
REACH_OK = 267
TOI_SCALE = 1.0


def fig_pos(x, feet=GROUND, s=TOI_SCALE):
    return [x, round(feet - FIG_BASE * s, 2)]


DRAG_K = 70                                     # recul de la pointe : pointe à 70 px à gauche de l'épaule
P2 = fig_pos(628)                               # (628, 1135) S01-S07 : bout de la barre (528, 900) à 230 px, côté sûr
P_S07 = fig_pos(754)                            # après le tirage de S07 (pointe sur RALLONGE_MID)
P_FAR = fig_pos(880)                            # S09-S15 : après le tirage de S09 (pointe sur RALLONGE_END)
P3 = fig_pos(650)                               # S16-S22 (walk_low sur « Mais »)
NOM_TOI_LOCAL, NOM_TOI_W, NOM_TOI_H = (0, -135), 96, 54   # pilule « Toi » au-dessus de la tête (monde y 1000)
INTER_POS = fig_pos(190)                        # (190, 1135) : l'interlocuteur, face à « Toi »
INTER_FROM_X = -120                             # S05 : entre en marchant depuis la gauche
NOM_INTER_LOCAL, NOM_INTER_W, NOM_INTER_H = (0, -125), 275, 56    # monde (190, 1010)
VERDICT_LOCAL, VERDICT_W, VERDICT_H = (0, -190), 250, 60          # monde (190, 945)
CONSEILLER_W, CONSEILLER_H = 250, 64
SOURIRE_LOCAL, SOURIRE_W, SOURIRE_H = (0, -305), 130, 90          # monde (190, 830)

# --- le repère 1-2-3 légendé (en haut) ---
MARKER_Y, MARKER_CX, MARKER_GAP = 280, 540, 193  # disques x 347, 540, 733 ; légende Bold 32
MARKER_LABEL_SIZE = 32
MARKER_XS = [MARKER_CX - MARKER_GAP, MARKER_CX, MARKER_CX + MARKER_GAP]

# --- la pastille (objet du fil) ---
PASTILLE_W, PASTILLE_H = 300, 84
PASTILLE_S01 = (760, 700)                       # image 0 -> S01, S03-S05 (revenue)
PASTILLE_TIRE1, PASTILLE_TIRE2 = (700, 675), (665, 650)   # S02 « pression », « monter ? » ; S05 : TIRE1
PASTILLE_S06A, PASTILLE_S06B = (640, 640), (620, 640)     # S06 « pousse », « agir » (contre le bord de la carte)
PASTILLE_S07 = (730, 670)                       # S07 « main » : décollée du bouton, retenue par le fil mou (-> S11)
PASTILLE_COIN, PASTILLE_COIN_K = (490, 462), 0.7   # S12-S15 : suit l'offre réduite (fil de 84 px visible)
PASTILLE_S15 = (660, 965)                       # S15 « perdre. » : libérée, revient du côté de « Toi »
PASTILLE_LIBRE = (765, 420)                     # S15 libérée ; S18-S21 attend en haut à droite
PASTILLE_TEL = (765, 428)                       # S16-S17 : reprise par le crochet du téléphone
PASTILLE_FIN, PASTILLE_FIN_K = (480, 760), 1.5  # S21 « argent. » : en grand à côté de « Toi » (x 255-705)
PASTILLE_HOOK_LOCAL = (-150, 0)                 # bout gauche : là où se plante le crochet

# --- l'offre (carte papier) et ses enfants (repère local de `offre`, centre (300, 560)) ---
OFFRE_C, OFFRE_W, OFFRE_H = (300, 560), 420, 300   # x 90-510, y 410-710
OFFRE_COIN, OFFRE_COIN_K = (175, 462), 0.6      # S12-S20 : réduite en haut à gauche (carte x 49-301, barre y 649-683)
# enfants cachés dans le coin (textes à 20 px illisibles) : restent le titre, le bouton et la barre rouge
COIN_HIDE = ["offre_ligne", "cr_maintenant", "cr_minuit", "accolade_mot", "accolade_jour", "horloge_cr",
             "case_offre"]                      # le bouton « J’investis » reste (la carte n'est pas vide)
TITRE_LOCAL, LIGNE_LOCAL = (0, -90), (0, -25)   # monde y 470, 535
BOUTON_LOCAL, BOUTON_W, BOUTON_H = (0, 80), 220, 64   # monde (300, 640)
BOUTON_PRESS = 6                                # S06 « agir » : le bouton descend de 6 px sur son ombre fixe
CASE_LOCAL, CASE_S = (222, -110), 90            # monde (522, 450) : case de vérification (haut 410, sous le repère)
CROCHET_A_LOCAL = (210, 0)                      # bord droit de la carte (monde 510, 560)

# --- le compte à rebours (gauge rouge, dir left, enfant de l'offre) ---
BAR_C, BAR_W, BAR_H = (328, 900), 400, 56       # monde : x 128-528, y 872-928
BAR_LOCAL = (BAR_C[0] - OFFRE_C[0], BAR_C[1] - OFFRE_C[1])   # (28, 340)
BAR_END = (528, 900)                            # le bout droit (côté « minuit ») : pause, saisie, tirage
BLOCK_S05 = (465, 975)                          # S05 : la pointe (en route vers l'offre) heurte la barre baissée et dressée
LEG_MAINTENANT_LOCAL = (128 - OFFRE_C[0], 960 - OFFRE_C[1])  # ancre start, monde (128, 960)
LEG_MINUIT_LOCAL = (528 - OFFRE_C[0], 960 - OFFRE_C[1])      # ancre end, monde (528, 960)
HORLOGE_CR_LOCAL, HORLOGE_CR_R = (95 - OFFRE_C[0], 900 - OFFRE_C[1]), 24    # monde (95, 900)
HORLOGE_CR_N1_LOCAL, HORLOGE_CR_N1_K = (170 - OFFRE_C[0], 800 - OFFRE_C[1]), 1.4   # S06 : à côté du « n° 1 »
PAUSE_LOCAL, PAUSE_R = (528 - OFFRE_C[0], 845 - OFFRE_C[1]), 30    # monde (528, 845), au-dessus du bout
ACCOLADE_LOCAL = (BAR_C[0] - OFFRE_C[0], 858 - OFFRE_C[1])   # monde (328, 858)
ACCOLADE_PTS = [[-200, 10], [-200, 0], [200, 0], [200, 10]]  # de « maintenant » à « minuit »
ACCOLADE_MOT_LOCAL = (BAR_C[0] - OFFRE_C[0], 825 - OFFRE_C[1])   # monde (328, 825)
BAR_DROP = 50                                   # S21 « refuse » : la barre glisse de 50 px vers le bas (bloque)
TRAIT_PTS = [[200, -22], [140, 40]]             # S21 : trait deep de « Toi » (repère de la barre ; enfant de la barre)

# --- la rallonge cyan (gauge dir right, monde) et « Délai refusé » ---
RALLONGE_C, RALLONGE_W = (654, 900), 252        # x 528-780 (« Quelques jours » Bold 32 : 236 px, dedans)
RALLONGE_MID, RALLONGE_END = (654, 900), (780, 900)   # bout à value 0,5 (S07) et 1 (S09)
RESPRING_TAP = (712, 900)                       # S11 « Ce » : depuis P_FAR, « Toi » touche la place du délai
REFUS_C, REFUS_W, REFUS_H = (656, 900), 250, 60  # x 531-781 : contre le bout de la barre
BLOCK_S10 = (705, 960)                          # S10 « éviter » : depuis P_FAR, la pointe bute sur « Délai refusé » baissé

# --- les 3 disques rouges (S04), le « n° 1 » (S06) ---
PIEGE_R, PIEGES_FROM = 28, OFFRE_C
N1_C, ARNAQUES_C = (310, 800), (425, 815)       # « n° 1 » ExtraBold 110 ; « des arnaques » ancre start

# --- l'horloge de la vérification (sector, outil du stylo) ---
HORLOGE_R, HORLOGE_UNIT = 60, 10
HORLOGE_S04 = (180, 1090)                       # S04 (x 120-240) ; légendes ancre start x 258 (jusqu'à 559)
VERIFIER_C, MINUTES_C = (258, 1068), (258, 1113)
SPAWN_S04 = (520, 1020)                         # S04 « vérifier » : la pointe levée d'où naît l'horloge
HORLOGE_S15, DEUX_MIN_C = (862, 700), (862, 810)  # S15 : à droite de la liste, au-dessus de « Toi » (P_FAR)

# --- le « ? » de « Toi » (qmark) ---
Q_GS, Q_GS_S06, Q_GS_CHAMP = 80, 96, 48
Q_TETE_P2 = (720, 995)                          # à droite de la tête, « Toi » en P2
Q_TETE_S07 = (846, 995)                         # « Toi » en P_S07 (suit le tirage de S07)
Q_TETE_FAR = (884, 905)                         # « Toi » en P_FAR : au-dessus de sa tête (plus de place à droite)
Q_TETE_P3 = (742, 995)                          # « Toi » en P3 (S20)
Q_CYAN = (654, 815)                             # S09 « réflexion. » : au-dessus des jours gagnés
Q_CHAMP = (620, 1080)                           # S11-S14 : au bout droit du champ

# --- le champ de recherche (né de la rallonge, S11) et le fil de recherche ---
CHAMP_C, CHAMP_W, CHAMP_H = (470, 1080), 360, 64    # x 290-650, y 1048-1112
LOUPE_LOCAL, LOUPE_R = (-150, -4), 13
CHAMP_MOT_LOCAL = (-125, 0)                     # « Invest Minuit » ancre start (monde x 345)
CHAMP_TAP = (630, 1080)                         # S11 « savoir », S13 « consulte » (le « ? » en 620)
CHAMP_LEFT = (295, 1080)                        # départ du fil vers le nom (S11)
CHAMP_TOP = (470, 1050)                         # départ du fil vers le registre / la liste (S13-S14)
NOM_INTER_PT = (300, 1010)                      # bout droit de la pilule « Invest Minuit »
CHAMP_SPAWN, CHAMP_S11 = (660, 1000), (645, 1012)   # S11 « Ce » : le champ sort de la pointe, sous « Délai refusé »
FIL_COUPE_A = (340, 1048)                       # S15 : le fil qui coupe le crochet part du haut gauche du champ
CHAMP_S21, CHAMP_S21_K = (415, 1095), 1.0       # S21 : ressort du stylo, à pleine taille (x 235-595)

# --- le registre (S13-S14) : page dessinée en code ---
# page de registre dessinée en code (revue 1 : la place vide et « Absent » sur la page même, pas sur le pli du PNG)
REGISTRE_C, REGISTRE_W, REGISTRE_H = (565, 750), 460, 360   # x 335-795, y 570-930
REG_ENTETE_LOCAL, REG_ENTETE_H = (0, -132), 96  # bandeau light, monde y 570-666
REG_SCEAU_LOCAL, REG_SCEAU_R = (-185, -132), 30   # le sceau officiel (bank sur disque cyan), le même sur la liste noire
REG_TITRE_LOCAL, REG_SOUS_LOCAL = (-145, -152), (-145, -108)   # ancre start : ExtraBold 44 / Bold 30
REG_ROWS_Y = [-50, 0, 50, 100]                  # 4 noms inscrits (monde y 700, 750, 800, 850)
REG_ICO_X, REG_TRAIT_X0 = -190, -160            # disque immeuble ; trait encre depuis x -160 (ancre gauche)
REG_TRAIT_W = [[230, 180, 250, 200], [190, 240, 170, 220]]   # longueurs des noms : REGAFI, puis ORIAS
REG_VIDE_LOCAL, REG_VIDE_W, REG_VIDE_H = (-10, 150), 400, 48   # la place vide (monde y 900), là où pointe le fil
REG_X_LOCAL, REG_ABSENT_LOCAL = (-170, 150), (-130, 150)       # grand ✕ rouge, puis « Absent » (ancre start)

# --- la liste noire de l'AMF (S14-S15) ---
LISTE_C, LISTE_W, LISTE_H = (565, 750), 420, 330     # x 355-775, y 585-915
LN_ENTETE_LOCAL, LN_ENTETE_H = (0, -130), 70    # monde y 575-645 (encre ; sx 0 -> 1)
LN_TITRE_LOCAL = (-140, 0)                      # « Liste noire » ancre start, papier (repère de ln_entete)
LN_SCEAU_LOCAL = (-178, 0)                      # le même sceau que le registre
LN_AMF_LOCAL, AMF_W, AMF_H = (140, -130), 110, 52    # monde (680, 610)
LN_ROWS_Y = [-60, -5, 50, 105]                  # monde y 680, 735, 790, 845
LN_DISC_X, LN_TRAIT_X, LN_TRAIT_W = -165, -20, 220   # disque light r 20 (x 375) ; trait encre (x 410-630)
LN_NOM_LOCAL = (-135, 105)                      # « Invest Minuit » ancre start (monde x 405)

# --- le téléphone de l'escroc (S16-S20) ---
TEL_C, TEL_W, TEL_H = (470, 670), 300, 480      # x 320-620, y 430-910 (à droite de la barre réduite, x <= 312)
ECRAN_W, ECRAN_H = 260, 400                     # repère du téléphone : y -200 .. 200
CROCHET_TEL_A_LOCAL = (150, -80)                # bord droit du téléphone (monde 600, 590)
SITE_BANDEAU_LOCAL, SITE_BANDEAU_H = (0, -155), 90
SITE_ROWS_Y = [-60, 10, 80]                     # blocs puis avis (monde y 610, 680, 750)
AVIS_CHAT_X, ETOILES_X = -100, [-55, -20, 15, 50, 85]
VRAI_NOM_LOCAL = (0, -155)                      # sous la façade : « Invest Minuit » rouge
ALERTE_TEL_LOCAL, ALERTE_TEL_R = (0, 10), 40    # warning sur disque rouge (monde 450, 680)
PHONE_TAP, PHONE_PULL = (540, 895), (540, 960)  # S18 : « Toi » (P3) accroche le bas de l'écran et tire vers le bas

# --- les quatre cartes d'alerte (S18-S20) ---
ALERTE_C = [(778, 530), (778, 645), (778, 760), (778, 875)]   # x 628-928 (+ ombre 6 : 934 < 940) ; téléphone x <= 620
ALERTE_W, ALERTE_H = 300, 100
ALERTE_ICO_LOCAL, ALERTE_ICO_R, ALERTE_TXT_X = (-112, 0), 34, -68   # pictogramme d'abord : disque 68 px anneau rouge

# --- la bouée (S20) : appel par ondes (pas de fil), nom sous la bouée en 40 px, à droite des ondes ---
BOUEE_C, BOUEE_W = (430, 600), 220              # h ≈ 144 : x 320-540, y ≈ 528-672
BOUEE_TEL_C, BOUEE_TEL_R = (492, 742), 22       # pictogramme téléphone devant le nom
BOUEE_NOM1_C, BOUEE_NOM2_C = (528, 742), (528, 794)   # ancre start, deep, Bold 40 (jusqu'à x 934)
AMF_BOUEE_C = (520, 540)                        # même pilule que sur la liste noire, posée sur la bouée
AMF_LISTE_W = (LISTE_C[0] + 140, LISTE_C[1] - 130)   # (705, 620) : d'où elle part (place qu'elle avait sur la liste)
COCHE_BOUEE_C = (430, 600)                      # le « ? » y devient une coche deep (size 60)
COMBINE_C, COMBINE_R = (400, 975), 34           # S20 « contacte » : sous la pointe (depuis P3)
ONDES_C = [(410, 905), (418, 840), (425, 775)]  # trois arcs d'appel du combiné vers la bouée
ONDES_W = [44, 64, 84]

# --- S22 : fin (kit.outro, pos (540, 760), 620 x 520 : bouton ≈ (540, 908), x 350-730, y 852-964) ---
FIN_C, FIN_BUTTON = (540, 720), (540, 868)     # 40 px plus haut : la carte ne touche plus la tête de « Toi »
FIN_TAP = (560, 930)                            # bord bas du bouton, sous le libellé (depuis P3 : côté sûr)
BTN_W, BTN_H = 380, 112
BTN_K = BTN_H / PASTILLE_H                      # relais pastille -> bouton (w = BTN_W / BTN_K, échelle BTN_K)

# ---------- identifiants ----------
PIEGES = ["piege1", "piege2", "piege3"]         # disques rouges (enfants : piege1_num…)
LN_DISCS = ["ln_disc1", "ln_disc2", "ln_disc3", "ln_disc4"]
LN_TRAITS = ["ln_trait1", "ln_trait2", "ln_trait3"]
REG_NOMS = ["reg_nom1", "reg_nom2", "reg_nom3", "reg_nom4"]
ONDES = ["onde1", "onde2", "onde3"]
SITE_BLOCS = ["site_bloc1", "site_bloc2", "site_bloc3"]
SITE_AVIS = ["site_avis1", "site_avis2", "site_avis3"]
SITE_ETOILES = [[f"site_etoile{i + 1}_{j + 1}" for j in range(5)] for i in range(3)]
ALERTES = ["alerte1", "alerte2", "alerte3", "alerte4"]
FIN_ONDES = ["fin_onde1", "fin_onde2"]


def scene_f0(S, sid):
    return round(next(s for s in S.sb["scenes"] if s["id"] == sid)["t_start"] * S.fps)


# ---------- l'allonge de « Toi » (bras gauche) ----------
def arm_check(fig_x, pt, side="left", fig_y=P2[1]):
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


def assert_reach(fig_x, pt, what, side="left", fig_y=P2[1]):
    d, safe, clear = arm_check(fig_x, pt, side, fig_y)
    assert 63 <= d <= REACH_OK and safe and clear >= HEAD_R + 8, \
        f"{what} : hors d'allonge depuis x {fig_x} ({side}) : {d} px, côté sûr {safe}, tête {clear} px"


# ---------- bras baissé (pose de repos de V06-V08) ----------
LOW_GRIP = (52, 15)          # prise du stylo, repère de la figurine : à la hanche (pointe au repos y <= 1262)
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


def drag(fig, f, d, a, b, e="inOut", lean=WALK_LEAN):
    """« Toi » TIRE : la pointe du stylo va de a à b (points monde) pendant que le corps recule du même dx, penché
    en arrière (lean > 0 en reculant vers la droite), sans saut. La pointe doit déjà être sur a à f - 1 (tap ou reach
    juste avant). Le bout de la jauge suit la pointe : S.key(gauge, "value", f, v, d, e) sur les MÊMES (f, d, e).
    -> f + d."""
    S = fig.S
    p0 = S.val(fig.id, "pos", f - 1)
    to = [round(p0[0] + b[0] - a[0], 2), p0[1]]
    fig._move_body(f, d, to, e, hop=0, lean=lean)
    for n, p in frames(f, d, e):
        G, rot = fig._tip_pose(fig._shoulder(n), lerp(list(a), list(b), p), fig._scale(n))
        fig._pose(n, G, rot)
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


def impact(S, f, pt, d=10):
    """Anneau d'impact encre au point monde `pt` : paraît à f, grandit et s'efface (le stylo bloqué, la coupe)."""
    S.key("choc", "pos", f - 1, [round(v, 2) for v in pt])
    return ring(S, "choc", f, d=d, s0=0.5, s1=1.7)


def drop_in(kit, id, f, **kw):
    """kit.drop d'entrée, invisible jusqu'à l'image du mot (opacité 0 à f - 1 : kit.drop la remet à 1 sur f)."""
    kit.S.key(id, "opacity", f - 1, 0)
    return kit.drop(id, f, **kw)


def case_block(S, kit, f, hold=15, stay=False):
    """La case de vérification refuse : elle tremble, son contour rougit et un grand ✕ rouge s'y trace sur l'image f ;
    hold images plus tard elle redevient vide et deep (stay=True : elle reste rouge, ✕ compris). -> f + hold."""
    kit.shake("case_offre", f, 7)
    S.key("case_offre", "stroke", f, RED, 3, "out")
    S.key("case_x", "scale", f - 1, 0)
    S.key("case_x", "scale", f, 1, 4, "out")
    if not stay:
        S.key("case_x", "scale", f + hold, 0, 4, "in")
        S.key("case_offre", "stroke", f + hold, DEEP, 6, "inOut")
    return f + hold


def star_pts(r_out=13, r_in=5.5):
    """Étoile à 5 branches (poly fermée), pointe en haut."""
    pts = []
    for k in range(10):
        a = math.radians(-90 + 36 * k)
        r = r_out if k % 2 == 0 else r_in
        pts.append([round(r * math.cos(a), 2), round(r * math.sin(a), 2)])
    return pts


# J du crochet (poly ouverte rouge 7 px, x 1,8 : 47 x 61), origine = bout du fil, planté dans le bord gauche de la pastille
HOOK_PTS = [[round(1.8 * x, 1), round(1.8 * y, 1)] for x, y in
            [[0, -8], [0, 14], [-3, 22], [-11, 26], [-19, 22], [-21, 13]]]
CROCHET_SW = 8


# ---------- raccords (contrat des parties ; couleurs en hex minuscule : S.val rend du minuscule) ----------
def _lo(c):
    return c.lower()


_OFF = lambda *ids: {i: {"scale": 0} for i in ids}   # noqa: E731

ENTRY_P2 = {   # fin de S07 = etat_initial de S08 (image 867)
    "offre": {"pos": list(OFFRE_C), "scale": 1, "stroke": _lo(INK)},
    "offre_ligne": {"chars": len(T_OFFRE_LIGNE)},
    "bouton": {"pos": list(BOUTON_LOCAL), "stroke": _lo(INK), "fill": _lo(PAPER)}, "bouton_mot": {"color": _lo(INK)},
    "compte_rebours": {"sx": 1, "value": 0.5},
    "cr_maintenant": {"opacity": 1}, "cr_minuit": {"opacity": 1},
    "horloge_cr": {"pos": list(HORLOGE_CR_LOCAL), "scale": 1},
    "pause": {"scale": 1, "opacity": 1},
    "case_offre": {"scale": 1, "stroke": _lo(DEEP)}, "case_x": {"scale": 0},
    "rallonge": {"value": 1, "scale": 1},          # plein cyan, largeur 126 (pistes w / pos : x 528-654)
    "rallonge_mot": {"chars": 0},
    "crochet": {"draw": 1, "sag": 60, "dashed": 0, "opacity": 1},
    "crochet_j": {"scale": 1},
    "pastille": {"pos": list(PASTILLE_S07), "scale": 1},
    "nom_inter": {"scale": 1},
    "question": {"pos": list(Q_TETE_S07), "scale": 1, "gs": Q_GS},
    "marqueur": {"pos": [MARKER_CX, MARKER_Y], "scale": 1, "on": 0, "active": 0, "lbl": 1,
                 "done0": 0, "done1": 0, "done2": 0},
    **_OFF("n1", "n1_mot", "horloge", "horloge_verifier", "horloge_minutes", *PIEGES, "refus", "champ"),
    "accolade_jour": {"draw": 0}, "accolade_mot": {"scale": 0},
}
ENTRY_P3 = {   # fin de S15 = etat_initial de S16 (image 1850)
    "offre": {"pos": list(OFFRE_COIN), "scale": OFFRE_COIN_K},
    **_OFF(*COIN_HIDE),
    "crochet": {"opacity": 0}, "crochet_j": {"scale": 0}, "crochet_h1": {"draw": 0}, "crochet_h2": {"draw": 0},
    "fil_coupe": {"draw": 0},
    "pastille": {"pos": list(PASTILLE_S15), "scale": 1},
    "champ": {"pos": list(CHAMP_C), "scale": 1}, "champ_mot": {"chars": len(T_INTER)},
    "fil_recherche": {"draw": 1, "dashed": 0, "color": _lo(RED)},
    "liste_noire": {"pos": list(LISTE_C), "scale": 1}, "ln_entete": {"sx": 1}, "amf_liste": {"scale": 1},
    "ln_titre": {"scale": 1}, "ln_sceau": {"scale": 1},
    "ln_nom": {"chars": len(T_INTER), "color": _lo(RED)},
    "horloge": {"pos": list(HORLOGE_S15), "scale": 1, "value": 2},
    "horloge_2min": {"scale": 1, "value": 2},
    "verdict": {"scale": 1}, "verdict_tirets": {"scale": 0}, "verdict_plein": {"scale": 1},
    "verdict_mot": {"text": T_NON_AUTORISE, "color": _lo(RED)},
    "nom_inter": {"scale": 1},
    "marqueur": {"pos": [MARKER_CX, MARKER_Y], "scale": 1, "on": 1, "active": 1, "done0": 1, "done1": 0,
                 "done2": 0, "lbl": 1},
    **_OFF("question", "registre", "rallonge", "refus", "n1", "n1_mot", "pause", "horloge_verifier",
           "horloge_minutes", "telephone", "conseiller", "sourire"),
}


def cast(S, kit):
    """Toute la distribution, à son état de l'image 0. Ce qui arrive plus tard : scale=0 (ou draw=0, chars=0, sx=0,
    opacity=0). Seuls `fin` et `fin_curseur` naissent dans kit.outro (p3)."""

    # --- l'offre : carte papier (tombe en S01) ; titre, ligne tapée, bouton « J’investis » (forme + ombre fixe :
    #     le bouton s'enfonce en descendant de BOUTON_PRESS px ; contour en hex pour passer au rouge) ---
    kit.shape("offre", list(OFFRE_C), kind="round", w=OFFRE_W, h=OFFRE_H, r=18, fill=PAPER, stroke=INK, sw=4,
              shadow=6, z=5, scale=0)
    S.set("offre", stroke=INK)
    kit.text("offre_titre", list(TITRE_LOCAL), T_OFFRE, size=44, weight=800, z=5.2, parent="offre")
    kit.text("offre_ligne", list(LIGNE_LOCAL), T_OFFRE_LIGNE, size=34, weight=700, z=5.2, parent="offre", typed=True)
    kit.shape("bouton_ombre", [BOUTON_LOCAL[0] + 6, BOUTON_LOCAL[1] + 6], kind="round", w=BOUTON_W, h=BOUTON_H,
              r=BOUTON_H / 2, fill=INK, stroke=INK, sw=0, shadow=0, z=5.25, parent="offre")
    kit.shape("bouton", list(BOUTON_LOCAL), kind="round", w=BOUTON_W, h=BOUTON_H, r=BOUTON_H / 2, fill=PAPER,
              stroke=INK, sw=4, shadow=0, z=5.3, parent="offre")
    S.set("bouton", stroke=INK, fill=PAPER)     # S06 « agir » : enfoncé, plein rouge (hex)
    kit.text("bouton_mot", [0, 0], T_INVESTIS, size=34, weight=700, z=5.35, parent="bouton")
    S.set("bouton_mot", color=INK)
    # la case de vérification (revue 1) : 90 px, trait plein deep, loupe à 40 % dans le coin haut gauche ; chaque fois
    # que le stylo est bloqué (S05, S10, S21), elle tremble, rougit et un grand ✕ rouge s'y trace
    kit.shape("case_offre", list(CASE_LOCAL), kind="round", w=CASE_S, h=CASE_S, r=14, fill=PAPER, stroke=DEEP,
              sw=5, shadow=3, z=5.5, parent="offre", scale=0)
    S.set("case_offre", stroke=DEEP)            # DEEP -> RED (hex)
    kit.shape("case_loupe", [-22, -22], kind="circle", w=22, fill="none", stroke=DEEP, sw=4, shadow=0, z=5.55,
              parent="case_offre", opacity=0.4)
    kit.shape("case_manche", [-8, -8], kind="poly", pts=[[0, 0], [9, 9]], closed=False, fill="none", stroke=DEEP,
              sw=5, shadow=0, z=5.55, parent="case_offre", opacity=0.4)
    group(kit, "case_x", [0, 6], z=5.6, parent="case_offre", scale=0)
    for k, pts in enumerate(([[-24, -24], [24, 24]], [[24, -24], [-24, 24]])):
        kit.shape(f"case_x{k + 1}", [0, 0], kind="poly", pts=pts, closed=False, fill="none", stroke=RED, sw=9,
                  shadow=0, z=5.6, parent="case_x")

    # --- le compte à rebours (enfant de l'offre) : jauge rouge dir left (STRETCH sx 0 -> 1), légendes, horloge,
    #     « pause », accolade « Dans la journée », trait de refus de « Toi » (S21, enfant de la barre) ---
    kit.gauge("compte_rebours", list(BAR_LOCAL), value=1, w=BAR_W, h=BAR_H, dir="left", fill=RED, empty=PAPER,
              sw=4, shadow=6, z=6, parent="offre")
    S.set("compte_rebours", sx=0)
    kit.text("cr_maintenant", list(LEG_MAINTENANT_LOCAL), T_MAINTENANT, size=32, weight=700, anchor="start",
             z=6.1, parent="offre", opacity=0)
    kit.text("cr_minuit", list(LEG_MINUIT_LOCAL), T_MINUIT, size=32, weight=700, anchor="end", z=6.1,
             parent="offre", opacity=0)
    kit.icon("horloge_cr", list(HORLOGE_CR_LOCAL), "clock", disc=HORLOGE_CR_R, fill=PAPER, shadow=3, z=6.2,
             parent="offre", scale=0)
    kit.icon("pause", list(PAUSE_LOCAL), "pause", disc=PAUSE_R, fill=PAPER, shadow=3, z=6.4, parent="offre",
             scale=0)
    kit.shape("accolade_jour", list(ACCOLADE_LOCAL), kind="poly", pts=ACCOLADE_PTS, closed=False, fill="none",
              stroke=RED, sw=6, shadow=0, z=6.2, parent="offre", draw=0)
    kit.text("accolade_mot", list(ACCOLADE_MOT_LOCAL), T_JOURNEE, size=34, weight=700, color=RED, z=6.2,
             parent="offre", scale=0)
    kit.shape("trait_refus", [0, 0], kind="poly", pts=TRAIT_PTS, closed=False, fill="none", stroke=DEEP, sw=6,
              shadow=0, z=6.5, parent="compte_rebours", draw=0)

    # --- la rallonge cyan (monde) et son mot ; « Délai refusé » ---
    kit.gauge("rallonge", list(RALLONGE_C), value=0, w=RALLONGE_W, h=BAR_H, dir="right", fill=CYAN, empty=PAPER,
              sw=4, shadow=6, z=6, scale=0)
    kit.text("rallonge_mot", [0, 0], T_JOURS, size=32, weight=600, z=6.1, parent="rallonge", typed=True)
    pill(S, "refus", REFUS_C, T_REFUS, size=34, fill=PAPER, h=REFUS_H, w=REFUS_W, z=7, stroke=RED, color=RED,
         shadow=3)

    # --- la pastille « Ton argent » (objet du fil), son crochet en J, le fil de l'offre, le fil du téléphone ---
    pill(S, "pastille", PASTILLE_S01, T_ARGENT, size=40, weight=800, fill=CYAN, h=PASTILLE_H, w=PASTILLE_W, z=12,
         scale=1, icon="euro")
    S.set("pastille", rot=0, text=T_ARGENT, textOp=1)
    kit.shape("crochet_j", list(PASTILLE_HOOK_LOCAL), kind="poly", pts=HOOK_PTS, closed=False, fill="none",
              stroke=RED, sw=7, shadow=0, z=12.2, parent="pastille", scale=0)
    S.add("crochet", "wire", z=11.8, a={"id": "offre", "at": list(CROCHET_A_LOCAL)},
          b={"id": "pastille", "at": list(PASTILLE_HOOK_LOCAL)}, color=RED, sw=CROCHET_SW, dashAlt=[14, 11])
    S.set("crochet", draw=0, sag=0, dashed=0, opacity=1)
    for hid in ("crochet_h1", "crochet_h2"):    # S15 : les deux moitiés du fil coupé (extrémités libres pa / pb)
        S.add(hid, "wire", z=11.8, color=RED, sw=CROCHET_SW)
        S.set(hid, pa=[0, 0], pb=[0, 0], draw=0, sag=0, opacity=1)
        S.set(hid, **{"from": 0})
    S.add("crochet_tel", "wire", z=11.8, a={"id": "telephone", "at": list(CROCHET_TEL_A_LOCAL)},
          b={"id": "pastille", "at": list(PASTILLE_HOOK_LOCAL)}, color=RED, sw=CROCHET_SW, dashAlt=[14, 11])
    S.set("crochet_tel", draw=0, sag=0, dashed=0, opacity=1)
    # S10 : le fil rouge de l'interlocuteur qui saisit la rallonge et la ramène ; S15 : le fil deep de la recherche
    # qui coupe le crochet ; anneau d'impact (le stylo bloqué, la coupe)
    S.add("fil_refus", "wire", z=11.6, a={"id": "interlocuteur", "at": [38, -40]}, color=RED, sw=7)
    S.set("fil_refus", pb=list(RALLONGE_END), draw=0, sag=0, opacity=1)
    S.set("fil_refus", **{"from": 0})
    S.add("fil_coupe", "wire", z=11.9, color=DEEP, sw=6)
    S.set("fil_coupe", pa=[340, 1048], pb=[340, 460], draw=0, sag=0)
    S.set("fil_coupe", **{"from": 0})
    kit.shape("choc", [0, 0], kind="circle", w=64, fill="none", stroke=INK, sw=6, shadow=0, z=16.8, opacity=0)

    # --- S04 : les 3 disques rouges (sortent de l'offre, deviennent le repère) ---
    for k, pid in enumerate(PIEGES):
        kit.shape(pid, list(PIEGES_FROM), kind="circle", w=2 * PIEGE_R, fill=PAPER, stroke=RED, sw=4, shadow=3,
                  z=21, scale=0)
        kit.text(f"{pid}_num", [0, 0], str(k + 1), size=30, weight=800, color=RED, z=21.1, parent=pid)

    # --- le repère 1-2-3 légendé (aucun gris : doneStyle « kept » ; inactif on 0 jusqu'à S08) ---
    kit.steps_marker(MARKER_LABELS, y=MARKER_Y, cx=MARKER_CX, gap=MARKER_GAP, z=20)
    S.ents["marqueur"]["p"].update(moveBlank=True, labelSize=MARKER_LABEL_SIZE, doneStyle="kept")
    S.set("marqueur", scale=0, on=0, done0=0, done1=0, done2=0, lbl=0)
    # S21 « retiens : » : le disque 3 se coche (le disque actif garde son chiffre : pastille cochée posée dessus, p3)
    kit.shape("marqueur_fait3", [MARKER_XS[2], MARKER_Y], kind="circle", w=2 * GEOM["MARKER"]["r"], fill=LIGHT,
              stroke=INK, sw=4, shadow=0, z=20.6, scale=0)
    kit.tick("marqueur_fait3_coche", [0, 1], DEEP, size=26, sw=6, z=20.7, parent="marqueur_fait3", draw=0)

    # --- l'horloge de la vérification (sector), ses légendes, « 2 min » ---
    kit.sector("horloge", list(HORLOGE_S04), start=0, value=0, r=HORLOGE_R, unit=HORLOGE_UNIT, face="paper",
               fill=DEEP, sw=5, shadow=6, z=9, scale=0)
    kit.text("horloge_verifier", list(VERIFIER_C), T_VERIFIER, size=34, weight=700, color=DEEP, anchor="start",
             z=9, scale=0)
    kit.text("horloge_minutes", list(MINUTES_C), T_MINUTES, size=34, weight=700, color=DEEP, anchor="start", z=9,
             scale=0)
    kit.counter("horloge_2min", list(DEUX_MIN_C), value=0, size=56, weight=800, color=DEEP, suffix=" min", z=9,
                scale=0)

    # --- « n° 1 des arnaques » (S06) ---
    kit.text("n1", list(N1_C), T_N1, size=110, weight=800, color=RED, z=9, scale=0)
    kit.text("n1_mot", list(ARNAQUES_C), T_ARNAQUES, size=34, weight=700, color=RED, anchor="start", z=9, scale=0)
    # trait rouge de l'horloge agrandie (S06, x 170 r 34) au « n° 1 » : c'est le compte à rebours qui est n° 1
    kit.shape("n1_lien", [0, 0], kind="poly", pts=[[205, 800], [236, 800]], closed=False, fill="none", stroke=RED,
              sw=7, shadow=0, z=9, draw=0)

    # --- le « ? » de « Toi » ---
    S.add("question", "qmark", z=17)
    S.set("question", pos=list(Q_TETE_P2), scale=0, opacity=1, gs=Q_GS)

    # --- le champ de recherche (S11, né de la rallonge) : forme light, loupe en code, nom tapé ; le fil ---
    kit.shape("champ", list(CHAMP_C), kind="round", w=CHAMP_W, h=CHAMP_H, r=CHAMP_H / 2, fill=LIGHT, stroke=DEEP,
              sw=4, shadow=6, z=9, scale=0)
    kit.shape("champ_loupe", list(LOUPE_LOCAL), kind="circle", w=2 * LOUPE_R, fill=LIGHT, stroke=DEEP, sw=4,
              shadow=0, z=9.2, parent="champ")
    kit.shape("champ_manche", [LOUPE_LOCAL[0] + 10, LOUPE_LOCAL[1] + 10], kind="poly", pts=[[0, 0], [9, 9]],
              closed=False, fill="none", stroke=DEEP, sw=6, shadow=0, z=9.1, parent="champ")
    kit.text("champ_mot", list(CHAMP_MOT_LOCAL), T_INTER, size=34, weight=700, anchor="start", z=9.2,
             parent="champ", typed=True)
    S.add("fil_recherche", "wire", z=8.5, color=DEEP, sw=5, dashAlt=[14, 11])   # dashAlt : piste dashed (S13)
    S.set("fil_recherche", pa=list(CHAMP_LEFT), pb=list(NOM_INTER_PT), draw=0, sag=0, dashed=0, color=DEEP)
    S.set("fil_recherche", **{"from": 0})

    # --- le registre (S13-S14) : page papier dessinée en code ; bandeau light (sceau officiel, titre, sous-titre) ;
    #     4 noms inscrits ; la place vide en tirets où pointe le fil (-> rouge, grand ✕, « Absent ») ; la page tourne
    #     (piste sx de la carte) de REGAFI à ORIAS ---
    kit.shape("registre", list(REGISTRE_C), kind="round", w=REGISTRE_W, h=REGISTRE_H, r=18, fill=PAPER, stroke=INK,
              sw=4, shadow=6, z=4, scale=0)
    kit.shape("reg_entete", list(REG_ENTETE_LOCAL), kind="round", w=REGISTRE_W - 8, h=REG_ENTETE_H, r=14, fill=LIGHT,
              stroke="none", sw=0, shadow=0, z=4.05, parent="registre")
    kit.icon("registre_sceau", list(REG_SCEAU_LOCAL), "bank", disc=REG_SCEAU_R, fill=CYAN, shadow=3, z=4.4,
             parent="registre")
    kit.text("registre_titre", list(REG_TITRE_LOCAL), T_REGAFI, size=44, weight=800, anchor="start", z=4.3,
             parent="registre")
    S.set("registre_titre", text=T_REGAFI)
    kit.text("registre_sous_titre", list(REG_SOUS_LOCAL), T_REGAFI_SOUS, size=30, weight=700, anchor="start", z=4.3,
             parent="registre")
    S.set("registre_sous_titre", text=T_REGAFI_SOUS)
    for k, nid in enumerate(REG_NOMS):
        y, w = REG_ROWS_Y[k], REG_TRAIT_W[0][k]
        kit.icon(f"{nid}_ico", [REG_ICO_X, y], "building", disc=16, fill=LIGHT, shadow=0, z=4.2, parent="registre")
        kit.shape(nid, [REG_TRAIT_X0 + w / 2, y], kind="rect", w=w, h=12, fill=INK, stroke=INK, sw=0, shadow=0,
                  z=4.2, parent="registre")
    kit.shape("reg_vide", list(REG_VIDE_LOCAL), kind="round", w=REG_VIDE_W, h=REG_VIDE_H, r=10, fill="none",
              stroke=INK, sw=4, dash=[12, 8], shadow=0, z=4.2, parent="registre")
    S.set("reg_vide", stroke=INK)               # ne rien trouver : INK -> RED (hex)
    group(kit, "reg_x", REG_X_LOCAL, z=4.35, parent="registre", scale=0)
    for k, pts in enumerate(([[-17, -17], [17, 17]], [[17, -17], [-17, 17]])):
        kit.shape(f"reg_x{k + 1}", [0, 0], kind="poly", pts=pts, closed=False, fill="none", stroke=RED, sw=8,
                  shadow=0, z=4.35, parent="reg_x")
    kit.text("reg_absent", list(REG_ABSENT_LOCAL), T_ABSENT, size=34, weight=700, color=RED, anchor="start",
             z=4.3, parent="registre", typed=True)

    # --- la liste noire de l'AMF (S14-S15) : carte, en-tête encre (sx), « Liste noire », pilule AMF, 4 lignes ---
    kit.shape("liste_noire", list(LISTE_C), kind="round", w=LISTE_W, h=LISTE_H, r=18, fill=PAPER, stroke=INK, sw=4,
              shadow=6, z=4, scale=0)
    kit.shape("ln_entete", list(LN_ENTETE_LOCAL), kind="rect", w=LISTE_W, h=LN_ENTETE_H, fill=INK, stroke=INK, sw=0,
              shadow=0, z=4.1, parent="liste_noire")
    S.set("ln_entete", sx=0)
    kit.text("ln_titre", list(LN_TITRE_LOCAL), T_LISTE, size=34, weight=700, color=PAPER, anchor="start", z=4.2,
             parent="ln_entete", scale=0)
    kit.icon("ln_sceau", list(LN_SCEAU_LOCAL), "bank", disc=24, fill=CYAN, shadow=0, z=4.25, parent="ln_entete",
             scale=0)
    pill(S, "amf_liste", LN_AMF_LOCAL, T_AMF, size=34, weight=800, fill=PAPER, h=AMF_H, w=AMF_W, z=4.3,
         parent="liste_noire", shadow=3)
    for k, did in enumerate(LN_DISCS):
        kit.shape(did, [LN_DISC_X, LN_ROWS_Y[k]], kind="circle", w=40, fill=LIGHT, stroke=INK, sw=3, shadow=3,
                  z=4.2, parent="liste_noire", scale=0)
        S.set(did, fill=LIGHT)                  # la ligne trouvée : LIGHT -> RED (hex)
        if k < 2:                               # sites : petite fenêtre de navigateur dessinée en code
            kit.shape(f"{did}_fen", [0, 0], kind="round", w=24, h=20, r=3, fill=PAPER, stroke=INK, sw=3, shadow=0,
                      z=4.3, parent=did)
            kit.shape(f"{did}_barre", [0, -6], kind="rect", w=24, h=6, fill=INK, stroke=INK, sw=0, shadow=0, z=4.35,
                      parent=did)
        else:                                   # acteurs : immeuble
            kit.icon(f"{did}_ico", [0, 0], "building", s=26, z=4.3, parent=did)
    for k, tid in enumerate(LN_TRAITS):
        kit.shape(tid, [LN_TRAIT_X, LN_ROWS_Y[k]], kind="rect", w=LN_TRAIT_W, h=12, fill=INK, stroke=INK, sw=0,
                  shadow=0, z=4.2, parent="liste_noire", scale=0)
    kit.text("ln_nom", list(LN_NOM_LOCAL), T_INTER, size=34, weight=700, anchor="start", z=4.2,
             parent="liste_noire", typed=True)
    S.set("ln_nom", color=INK)                  # trouvé : INK -> RED (hex)

    # --- le téléphone (S16-S20) : coque, écran, encoche ; façade `site` (groupe arrachable) ; dessous : vrai nom
    #     rouge et alerte ; reflet ---
    kit.shape("telephone", list(TEL_C), kind="round", w=TEL_W, h=TEL_H, r=36, fill=PAPER, stroke=INK, sw=5,
              shadow=6, z=4, scale=0)
    S.set("telephone", stroke=INK)              # S16 « l'image. » : bat en rouge (hex)
    kit.shape("tel_ecran", [0, 0], kind="round", w=ECRAN_W, h=ECRAN_H, r=20, fill=LIGHT, stroke=INK, sw=3,
              shadow=0, z=4.1, parent="telephone")
    kit.shape("tel_encoche", [0, -TEL_H / 2 + 14], kind="round", w=60, h=10, r=5, fill=INK, stroke=INK, sw=0,
              shadow=0, z=4.15, parent="telephone")
    kit.text("tel_vrai_nom", list(VRAI_NOM_LOCAL), T_INTER, size=34, weight=700, color=RED, z=4.2,
             parent="telephone", scale=0)
    kit.icon("tel_alerte", list(ALERTE_TEL_LOCAL), "warning", disc=ALERTE_TEL_R, fill=RED, color=PAPER, shadow=4,
             z=4.2, parent="telephone", scale=0)
    group(kit, "site", [0, 0], z=4.3, parent="telephone")
    kit.shape("site_bandeau", list(SITE_BANDEAU_LOCAL), kind="round", w=ECRAN_W, h=SITE_BANDEAU_H, r=14, fill=CYAN,
              stroke=INK, sw=3, shadow=0, z=4.4, parent="site", scale=0)
    kit.text("site_nom", [0, 0], T_INTER, size=34, weight=700, z=4.45, parent="site_bandeau")
    for k, bid in enumerate(SITE_BLOCS):
        kit.shape(bid, [0, SITE_ROWS_Y[k]], kind="round", w=220, h=40, r=10, fill=PAPER, stroke=INK, sw=3,
                  shadow=0, z=4.4, parent="site", scale=0)
    for k, aid in enumerate(SITE_AVIS):
        group(kit, aid, [0, SITE_ROWS_Y[k]], z=4.4, parent="site", scale=0)
        kit.icon(f"{aid}_chat", [AVIS_CHAT_X, 0], "chat", disc=22, fill=LIGHT, shadow=3, z=4.45, parent=aid)
        for j, sid in enumerate(SITE_ETOILES[k]):
            kit.shape(sid, [ETOILES_X[j], 0], kind="poly", pts=star_pts(), fill=CYAN, stroke=INK, sw=2, shadow=0,
                      z=4.45, parent=aid, scale=0)
    kit.shape("site_banque", list(SITE_BANDEAU_LOCAL), kind="round", w=236, h=SITE_BANDEAU_H, r=12, fill=LIGHT,
              stroke=INK, sw=3, shadow=3, z=4.6, parent="site", scale=0)
    kit.icon("site_banque_ico", [-84, 0], "bank", disc=22, fill=PAPER, shadow=3, z=4.65, parent="site_banque")
    kit.text("site_banque_mot", [24, 0], T_BANQUE_NAT, size=34, weight=700, z=4.65, parent="site_banque")
    S.add("tel_reflet", "sheen", z=4.7, parent="telephone", w=ECRAN_W, h=ECRAN_H)
    S.set("tel_reflet", pos=[0, 0], p=0)

    # --- les quatre cartes d'alerte (S18-S20) : pictogramme D'ABORD (disque papier 68 px, anneau rouge, dessin rouge
    #     en code), puis deux lignes Bold 34 ; « garanti » soulignable (piste under). 1 flèche vers le haut + cadenas
    #     (garanti) ; 2 téléphone qui sonne, traits vers « Toi » ; 3 pièce ₿ ; 4 globe et flèche qui sort ---
    for k, aid in enumerate(ALERTES):
        kit.shape(aid, list(ALERTE_C[k]), kind="round", w=ALERTE_W, h=ALERTE_H, r=16, fill=PAPER, stroke=RED, sw=4,
                  shadow=6, z=10, scale=0)
        ico = f"{aid}_ico"
        kit.shape(ico, list(ALERTE_ICO_LOCAL), kind="circle", w=2 * ALERTE_ICO_R, fill=PAPER, stroke=RED, sw=5,
                  shadow=3, z=10.2, parent=aid)
        if k == 0:
            kit.icon(f"{aid}_g1", [-4, -2], "arrow", s=48, color=RED, sw=5, z=10.3, parent=ico, rot=-58)
            kit.icon(f"{aid}_g2", [15, 14], "lock", disc=13, fill=PAPER, color=RED, shadow=0, z=10.35, parent=ico)
        elif k == 1:
            kit.icon(f"{aid}_g1", [5, -5], "phone", s=40, color=RED, sw=4, z=10.3, parent=ico)
            for j, pts in enumerate(([[-12, 8], [-20, 16]], [[-4, 15], [-9, 24]], [[-17, 0], [-27, 4]])):
                kit.shape(f"{aid}_t{j + 1}", [0, 0], kind="poly", pts=pts, closed=False, fill="none", stroke=RED,
                          sw=4, shadow=0, z=10.3, parent=ico)
        elif k == 2:
            kit.shape(f"{aid}_g1", [0, 0], kind="circle", w=48, fill="none", stroke=RED, sw=4, shadow=0, z=10.3,
                      parent=ico)
            kit.text(f"{aid}_g2", [0, 1], "₿", size=36, weight=800, color=RED, z=10.35, parent=ico)
        else:
            kit.shape(f"{aid}_g1", [-6, 2], kind="circle", w=40, fill="none", stroke=RED, sw=4, shadow=0, z=10.3,
                      parent=ico)
            kit.shape(f"{aid}_g2", [-6, 2], kind="ellipse", w=18, h=40, fill="none", stroke=RED, sw=3, shadow=0,
                      z=10.3, parent=ico)
            kit.shape(f"{aid}_g3", [0, 0], kind="poly", pts=[[-26, 2], [14, 2]], closed=False, fill="none",
                      stroke=RED, sw=3, shadow=0, z=10.3, parent=ico)
            kit.icon(f"{aid}_g4", [18, -14], "arrow", s=26, color=RED, sw=4, z=10.35, parent=ico, rot=-20)
        l1, l2, l3 = T_ALERTES[k]
        kit.text(f"{aid}_l1", [ALERTE_TXT_X, -20], l1, size=34, weight=700, anchor="start", z=10.2, parent=aid)
        kit.text(f"{aid}_l2", [ALERTE_TXT_X, 20], l2, size=34, weight=700, anchor="start", z=10.2, parent=aid)
        if l3:
            x3 = ALERTE_TXT_X + text_width(l2 + " ", 34, 700)
            kit.text(f"{aid}_l3", [round(x3, 1), 20], l3, size=34, weight=700, anchor="start", underColor=RED,
                     z=10.2, parent=aid)
            S.set(f"{aid}_l3", under=0)
    # chaque signal vise l'argent : une flèche rouge part de la carte vers la pastille « Ton argent » (S18-S19)
    kit.icon("fleche_argent", [0, 0], "arrow", s=52, color=RED, sw=6, z=12.5, scale=0)

    # --- la bouée (S20) : BUOY ; appel par trois ondes cyan (pas de fil) ; nom deep 40 px sous la bouée, précédé
    #     d'un téléphone ; le sceau « AMF » (celui de la liste noire) ; coche ; combiné ---
    buoy = S.png("BUOY")
    S.add("bouee", "png", z=4, src=buoy["src"], w=BOUEE_W, h=round(BOUEE_W * buoy["h"] / buoy["w"]),
          contact=dict(w=round(BOUEE_W * 0.75), h=20, dy=4, blur=10, alpha=0.18))
    S.set("bouee", pos=list(BOUEE_C), scale=0, opacity=1)
    kit.icon("bouee_tel", list(BOUEE_TEL_C), "phone", disc=BOUEE_TEL_R, fill=CYAN, shadow=3, z=9, scale=0)
    kit.text("bouee_nom1", list(BOUEE_NOM1_C), T_BOUEE1, size=40, weight=700, color=DEEP, anchor="start", z=9,
             typed=True)
    kit.text("bouee_nom2", list(BOUEE_NOM2_C), T_BOUEE2, size=40, weight=700, color=DEEP, anchor="start", z=9,
             typed=True)
    pill(S, "amf_bouee", AMF_LISTE_W, T_AMF, size=34, weight=800, fill=PAPER, h=AMF_H, w=AMF_W, z=9.5, shadow=3)
    pill(S, "amf_trace", AMF_LISTE_W, T_AMF, size=34, weight=800, fill=PAPER, h=AMF_H, w=AMF_W, z=9.4, shadow=0)
    S.set("amf_trace", opacity=0.35)
    kit.tick("coche_bouee", list(COCHE_BOUEE_C), DEEP, size=60, sw=8, z=9.6, draw=1)
    S.set("coche_bouee", scale=0)
    kit.icon("combine", list(COMBINE_C), "phone", disc=COMBINE_R, fill=CYAN, shadow=3, z=16.5, scale=0)
    for k, oid in enumerate(ONDES):
        w = ONDES_W[k]
        kit.curve(oid, list(ONDES_C[k]), [[-w / 2, 10], [0, -8], [w / 2, 10]], draw=1, color=CYAN, sw=7, dot=False,
                  z=9, scale=0)

    # --- S22 : ondes du toucher du stylo sur le bouton (pas de pointeur de souris) ---
    for oid in FIN_ONDES:
        kit.shape(oid, list(FIN_TAP), kind="circle", w=70, fill="none", stroke=DEEP, sw=6, shadow=0, z=43.5,
                  opacity=0)

    # --- « Toi » (bras gauche), bras baissé dès l'image 0, et son nom (enfant : il le suit) ---
    toi = Figure(kit, "toi", pos=list(P2), scale=TOI_SCALE, side="left", z=15)
    S.set("toi", look=0)
    G, rot = low_pose(toi, 0)
    S.set(toi.pen, pos=[round(G[0], 3), round(G[1], 3)], rot=round(rot, 3))
    S.set(toi.arm, elbow=[round(v, 3) for v in solve_ik(toi._shoulder(0), G, toi.l1, toi.l2, toi.bend)[0]])
    pill(S, "nom_toi", NOM_TOI_LOCAL, T_TOI, size=34, fill=LIGHT, h=NOM_TOI_H, w=NOM_TOI_W, z=15.2, parent="toi",
         scale=1, shadow=3)

    # --- l'interlocuteur (figurine papier sans outil, entre en S05) et ses enfants : nom, verdict, façade
    #     « Conseiller », bulle souriante ---
    inter = Figure(kit, "interlocuteur", pos=list(INTER_POS), scale=1.0, variant="paper", side="right", tool=False,
                   z=14, show=False)
    S.set("interlocuteur", look=0)
    pill(S, "nom_inter", NOM_INTER_LOCAL, T_INTER, size=34, fill=PAPER, h=NOM_INTER_H, w=NOM_INTER_W, z=14.2,
         parent="interlocuteur", shadow=3)
    group(kit, "verdict", VERDICT_LOCAL, z=14.3, parent="interlocuteur", scale=0)
    kit.shape("verdict_tirets", [0, 0], kind="round", w=VERDICT_W, h=VERDICT_H, r=VERDICT_H / 2, fill=PAPER,
              stroke=RED, sw=4, dash=[12, 8], shadow=3, z=14.3, parent="verdict")
    kit.shape("verdict_plein", [0, 0], kind="round", w=VERDICT_W, h=VERDICT_H, r=VERDICT_H / 2, fill=PAPER,
              stroke=RED, sw=4, shadow=3, z=14.31, parent="verdict", scale=0)
    kit.text("verdict_mot", [0, 0], T_AUTORISE_Q, size=34, weight=700, z=14.35, parent="verdict")
    S.set("verdict_mot", text=T_AUTORISE_Q, color=INK)   # S14 « autorisés. » : T_NON_AUTORISE, INK -> RED
    pill(S, "conseiller", VERDICT_LOCAL, T_CONSEILLER, size=34, fill=LIGHT, h=CONSEILLER_H, w=CONSEILLER_W,
         z=14.6, parent="interlocuteur", shadow=3)
    kit.shape("sourire", list(SOURIRE_LOCAL), kind="round", w=SOURIRE_W, h=SOURIRE_H, r=22, fill=LIGHT,
              stroke=INK, sw=4, shadow=3, z=14.4, parent="interlocuteur", scale=0)
    kit.shape("sourire_queue", [30, 40], kind="poly", pts=[[-12, 0], [24, 22], [10, 0]], closed=True, fill=LIGHT,
              stroke=INK, sw=4, shadow=0, z=14.39, parent="sourire")
    kit.shape("sourire_oeil1", [-20, -12], kind="circle", w=12, fill=INK, stroke=INK, sw=0, shadow=0, z=14.45,
              parent="sourire")
    kit.shape("sourire_oeil2", [20, -12], kind="circle", w=12, fill=INK, stroke=INK, sw=0, shadow=0, z=14.45,
              parent="sourire")
    kit.curve("sourire_bouche", [0, 12], [[-26, 0], [0, 16], [26, 0]], draw=1, color=INK, sw=5, dot=False,
              z=14.45, parent="sourire")

    return SimpleNamespace(toi=toi, inter=inter, pieges=PIEGES, ln_discs=LN_DISCS, ln_traits=LN_TRAITS,
                           reg_noms=REG_NOMS, site_blocs=SITE_BLOCS, site_avis=SITE_AVIS, site_etoiles=SITE_ETOILES,
                           alertes=ALERTES, fin_ondes=FIN_ONDES)


def build(S):
    kit = Kit(S)
    c = cast(S, kit)
    only = [p for p in os.environ.get("WTH_PARTS", "").split(",") if p]   # WTH_PARTS=p2 : cette partie seule
    for name in PARTS:
        if not only or name in only:
            importlib.import_module(f".{name}", __name__).part(S, kit, c)
