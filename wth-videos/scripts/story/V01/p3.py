"""V01, partie 3 : S15-S22, images 1936-2796 (64,539 -> 93,201 s, fin du film). 32 temps forts.

Entrée (épinglée à l'image 1935 : kit.pin(1935, ENTRY_P3), etat_initial de S15) : page à gauche (300, 780) x 0,95,
« Brief · 1 page », pastille sur l'en-tête (pastille_fiche) ; L1-L5 en rangées cochées par l'IA, puce de L5 cerclée de
rouge ; 4 fils vers les 4 sources compactes dans case1-4, dates (source1-4, tagged 0) sous les valeurs ; case5 vide
en face de L5 ; conseiller (870, 800) ; IA rangée (60, 1200) x 0,42 ; repère sur 2 ; horloge-badge (830, 300).
Garde-fou figurine : `if S.val("toi", "scale", 1935) == 0: c.toi.enter(1926, at=list(ADV_S13))`.

Sortie : fin du film (image 2796) ; la carte de fin `fin` et son pointeur sont déclarés par kit.outro.

Brief, scène par scène :
- S15 « Une » : morph : chaque source compacte remonte son fil jusqu'à sa date (S.along_wire) et s'y fond (doc tag
  0 -> 1, puis la date devient étiquette : source tagged 0 -> 1) ; les fils se rétractent ; case1-4 s'effacent ; case5
  reste. Le conseiller redescend au pied de la page (ADV_S15, x 1,1 : toi.scale_to + walk). « sans » : [surligneur]
  passe sous L5 ; [fil5] se trace vers case5 : il touche un contour vide, se casse en tirets (dashed) et retombe (sag) ;
  case5 tremble (shake x) et reste vide. Tenue ≈ 1,6 s. « C’est » : toi.tap sur « 5 ans » (contact calé sur le mot :
  tap(f - TAP + 1, …)) ; sous la pointe, L5 vire au rouge (red) et casse (crack 0 -> 1, 300 ms) : c'est le STYLO qui la
  fait casser (règle 2 de la planche de référence). [coche_ia5] reste ; l'IA ne bouge pas. « question » : [question]
  sort de la valeur fendue (kit.pop(from_pt=valeur)), monte en arc au-dessus du conseiller ; [bulle] grandit autour
  (BUBBLE_AT), queue vers sa tête ; fil5 et case5 s'effacent. « client » : [client] naît du pictogramme de
  pastille_fiche (pop sur place puis hop) et descend se poser face au conseiller (CLIENT_S15) ; il s'incline de 4°
  vers lui (lean_to) et reste immobile.
- S16 « Reste » : [bulle] se replie en autocollant (s 0 -> 1) et vole attendre en STICKER_S16, hors de la page, sans
  couvrir la valeur fendue (relais par [autocollant] enfant de la fiche quand il s'y pose en S17). « décision » :
  [tampon_ferme] sort de la poitrine dans sa main (toi.stow du stylo, pop du tampon, tenu en STAMP_HOLD : S.path qui
  suit la main) ; 8 images plus tard, [empreinte] (contour en tirets 380 x 84, -6°) se trace sur la bande libre du bas
  de la page. « délègue » : [faisceau_tampon] part de l'IA, passe sous la page (via ≈ (380, 1200)) et touche le socle
  du tampon : le tampon ne bouge pas ; le faisceau se rétracte ; l'empreinte reste vide ; aucun rouge.
- S17 « Troisième » : kit.step(f, 2) ; [chapitre] (« 3 ») grandit et revient ; le client rentre dans le pictogramme
  de pastille_fiche (vanish into) ; le conseiller range le tampon (tampon_ferme vanish into toi, toi.unstow) et monte à
  droite de la page (ADV_S17, x 1,1, toi.place_for sur la colonne des coches). « relis » : toi.trace descend la
  colonne des coches ; sur L1-L4 : [surligneur] le temps du passage, [cocheN] (pleine, 64 px) se trace sur
  [coche_iaN], qui s'efface sous elle (opacity -> 0) ; [sourceN] s'allume (lit 0 -> 1). La pointe s'arrête sur L5
  sans cocher. « corriges » : d'un même trait, la pointe chasse [coche_ia5] (kit.drop out, h 52, 35°) et barre
  « 5 ans » (toi.strike(…, line="L5")) ; la valeur tombe (fall 0 -> 1) ; la fente se referme (crack 1 -> 0), la ligne
  repasse à l'encre (red 0) ; [autocollant] glisse à la place de la valeur : « Horizon : ? » ; [source5] « à poser au
  RDV » surgit dessous. « décides » : toi.stamp(f, "tampon", shake="fiche") s'abat dans [empreinte] (qui disparaît
  sous l'empreinte) : « PRÊT POUR LE RDV » et « + 1 question » (subOn 0 -> 1 au contact) ; l'autocollant bat au
  contact. Jamais « VALIDÉ ».
- S18 « L’IA » : morph : [marqueur] et les légendes se réduisent ; [planche] (seesaw) naît à leur place et descend
  (PLANK_AT) ; la fiche se réduit (PAGE_S18, x 0,45, lite 0 -> 1 sous 0,5) et se pose sur le bout gauche ; [ia]
  regrandit en IA_S18 (x 1,0). « prépare » : le conseiller marche sur le bout droit (ADV_S18, x 1,1) ;
  [faisceau_passe] pousse la fiche le long de la planche jusqu'à lui (≈ (790, 800)). « Toi » : [toi_pill] surgit au-
  dessus de sa tête ; l'IA descend calmement au sol (IA_FLOOR, x 0,7, arc 30), toujours visible. « conseil » :
  [conseil] ressort de sa poitrine (pop depuis le buste) et devient [jeton1] posé sur son bout de planche (relais) ;
  la planche penche de 4° (S.key rot, TILT). « l’adéquation » : [jeton2] naît de la pointe du stylo, empilé ; 8°.
  « responsabilité » : [jeton3] ; 12°, arrêt net ; le conseiller reste droit, pointe posée sur ses jetons.
- S19 « Dix » : morph : la planche revient à plat, se réduit et [chemin] naît à sa place (PATH_C) ; jetons rentrés
  dans la poitrine ; toi_pill s'efface ; le conseiller se pose sur le chemin (ADV_S19), la fiche devant lui
  (PAGE_S19, x 0,45) ; l'IA au départ du chemin (IA_S19, x 0,45) ; [horloge] quitte le badge et descend grandir au-
  dessus de lui (CLOCK_S19, x 0,66). « relecture » : [secteur] value 0 -> 10 (linéaire, 600 ms) pendant que toi.trace
  descend la fiche ; [dix_min] compte 0 -> 10 ; à la fin [coche_relue] se trace. « valent » : [fauteuils] surgissent
  seuls (CHAIRS_S19) ; puis la fiche glisse jusqu'à leur table (TABLE_S19). « erreur » : [brouillon] (x 0,4) sort de la
  tête de l'IA et file sur le chemin vers la droite (linéaire) ; le conseiller abaisse son stylo en travers du chemin
  (pointe ≈ (520, 1150)). « devant » : le brouillon bute sur la pointe ([impact_brouillon]), s'écrase (sx 0,86),
  colle 6 images, puis relais par [moitie1-2] qui tombent sous le chemin (kit.drop out) ; [bande_rouge] reste sous le
  chemin. « client » : [client] renaît de pastille_fiche et s'assoit dans le fauteuil droit (CLIENT_S19).
- S20 « Avant » : [separateur] se trace (draw) ; [avant] surgit ; fauteuils, client et fiche glissent dans la moitié
  droite (CHAIRS_S20 x 0,75) ; chemin, éclats, bande rouge et IA se réduisent en points (un seul PNG sort à la fois :
  l'IA) ; le conseiller marche dans la moitié gauche (ADV_S20, x 0,9 : scale_to + walk). « tu » : [toi_pill] surgit ;
  l'horloge glisse et se réduit au-dessus de lui (CLOCK_S20, x 0,4). « arrives » : la vieille pile (doc1-4 rendus
  visibles : tag 0, compact 0, x 0,5, ±12°, bandeaux visibles) tombe de travers dans ses bras (drop, décalés de
  2 images) ; à droite, la fiche se replie dans sa pastille (relais pastille_fiche -> [pastille], fiche scale 0), qui
  saute par-dessus le séparateur jusqu'à PASTILLE_S20 (arc 80). « cherché » : doc3 (Mail) glisse et tombe (drop out,
  h 80, 25°) ; le conseiller se penche en arrière de 4°.
- S21 « Après » : [apres] surgit ; la pastille saute par-dessus le séparateur jusqu'à la table (700, 800, arc 120) ;
  la fiche se redéplie sous elle (FICHE_S21, x 0,35, tamponnée ; relais pastille -> pastille_fiche). « arrives » :
  [toi2] entre depuis x 520 jusqu'à ADV_S21 (enter frm) ; [toi_pill] -> relais [toi_pill_vol] qui saute le séparateur
  (arc 100) -> [toi2_pill] au-dessus de toi2. « compris » : l'autocollant quitte L5 et vole au client dans [bulle]
  partie de toi2 ; le client renvoie [reponse] (pastille cyan) qui remplit la puce vide de L5 ; les deux figurines
  s'inclinent de 4° l'une vers l'autre. À gauche, rien ne bouge.
- S22 « Abonne-toi » : out = kit.outro("S22", outs=[séparateur, pilules, horloge, pile, fauteuils, fiche…],
  press="argent.") ; la pastille passe à « S’abonner » (piste text) et rejoint le bouton (ou s'efface sous lui) ;
  toi.exit / toi2.exit / client.exit(out["card"]) ; un PNG à la fois (fauteuils puis horloge). Puis immobile.

Recyclage : git show 6962c86:wth-videos/scripts/story/V01/p2.py (S13-S14 : rature, tampon) et p3.py (S15-S20 :
planche, jetons, chemin, brouillon, Avant / Après, fin).

Mise en scène réalisée (écarts au brief ; places propres à p3 en tête de module) :
- Raccord : kit.pin(1935, ENTRY_P3) plus l'ancre aAt des fils 1-4 (bout de la valeur, posée par p2) ; fil5 part aussi
  du bout de la valeur (S.set). Empreinte et tampon en [0, 300] à -4° (STAMP_LOCAL [0, 314] à -6° dépassait le bas de
  la page) ; coche_relue à cheval sur le coin haut droit de la fiche (sur le titre, elle le masquait).
- S16 « décision » : il fait un pas à droite (680) et tient le tampon en (560, 1075), devant lui, entre l'empreinte et
  sa tête, sous l'autocollant (STAMP_HOLD (720, 1040) est derrière lui : son bras est du côté gauche). La main est
  posée par toi.reach sur une pointe virtuelle (stylo rangé) ; le tampon suit la main image par image.
- S17 : il relit depuis (632, 812) (d'ici la pointe atteint L1 et la rature) ; sur « décides » il descend au pied de
  la page (458, 1125) en 12 images, tamponne, puis s'écarte en (720, 1125), à droite du futur pivot.
- S18 : l'IA debout SUR le bout gauche (y 795 : IA_S18 la plantait dans la planche) ; jetons à largeur mesurée
  (200 / 262 / 311), alignés à droite et décalés vers le pivot : à 12° la pile est d'aplomb, à côté de lui. La fiche
  reçue est tenue levée à sa gauche, puis rangée contre lui (vanish into toi) 10 images après « Toi » : les poids ont
  la place ; elle ressort de lui sur « Dix », posée devant (PAGE_S19). Il suit son bout de planche image par image
  (hop + reach à chaque image), la pointe posée au bout de la pile.
- S19 : brouillon x 0,3 (au lieu de 0,4 : il a la place de filer avant le stylo), bande rouge x 0,75 en proportion ;
  pointe du stylo en travers du chemin en (380, 1150), à SA gauche, côté IA ((520, 1150) est derrière lui). Client
  assis x 0,75.
- S20 : il range le stylo sur « arrives » (bras pleins) ; pile en (140, 1125), sous sa pilule.
- S21 : fiche x 0,26 en (703, 961), debout sur la table (x 0,35 recouvrait la tête du client) ; toi2 en (575, 1144).
- S22 : press = l'image du mot « argent. » (kit.outro n'accepte en mot que les temps forts de la scène) ; la fiche
  monte au centre et s'efface dans la carte ; la pastille devient « S’abonner », glisse sur le bouton et s'y fond ;
  horloge sortie après les fauteuils (un PNG à la fois).
"""
import math

# Tour de revue 1 (corrections) :
# - S15 : [bande5] et [nuage5] (posés par p2 sur « fausse ») s'effacent au coup de stylo ; S17 « corriges » : [anneau5]
#   s'efface, la puce revient à sa taille.
# - S16 : le conseiller se tient à x 700 (l'autocollant « ? » en (585, 940) n'est plus sa pensée) ; « délègue » : le
#   faisceau casse net sur le tampon tenu (éclats, traits d'impact), puis recule visiblement.
# - S17 : chaque coche pointillée de l'IA rentre dans l'IA quand la coche pleine se trace ; celle de L5 est chassée
#   loin hors de la page ; la marche vers la page passe à droite de l'autocollant.
# - S18 : la fiche ne disparaît plus : portée par le faisceau jusqu'à lui, tenue contre sa poitrine (z relevés entre
#   le corps et le bras), elle suit ses pas et repart sur « Dix » vers PAGE_S19 (même entité) ; l'IA descend, devant la
#   planche, sur une petite marche à côté du pivot, tournée vers lui, et ils se saluent d'un signe de tête ; chaque
#   poids est cherché devant sa poitrine au bout du stylo, porté et posé, la planche penche à la pose ; les pilules
#   restent horizontales.
# - S19 : « Dix » décalé (fiche + 2, horloge + 4, IA + 6) ; fiche vers la table en arc bas (60) ; brouillon x 0,4 à
#   contour pointillé épais et ombre, tenue de 8 images sur la pointe (éclats), moitiés et bande rouge qui tombent de
#   32 px et s'effacent ensemble (rien de rouge ne reste) ; client né à x 0,25.
# - S20 : l'horloge (x 0,55) part sur « Avant », le séparateur se trace 9 images plus tard ; pile en éventail (± 18°) ;
#   « cherché » : Mail puis PDF tombent lentement au sol et y restent (traits de vitesse), il se penche de 8°.
# - S21 : fiche x 0,46 au-dessus de la table ; « ? » de 56 px en arc jusqu'au client ; le client répond par une bulle de
#   parole avec une pastille cyan pleine de 56 px ([reponse], disque, plus le pictogramme de personne qui se lisait
#   « cadenas »), qui passe sous les rangées 1-4 et remplit la puce de L5 ([reponse5]) ; coche pleine [coche5],
#   surlignage cyan pâle.
# - S22 : la fiche devient la carte (S.fly + sx / sy jusqu'au cadre de la carte, kit.outro card_at) et la pastille
#   devient le bouton (relais sans pictogramme [pastille_btn] en vol, kit.outro btn_at) ; carte centrée en y 800,
#   sous-titre 34 px ; les sortants s'effacent (clear="fade").

from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, SCALE, line_crack_point, text_width
from pipeline.story_kit import TAP, frames, lerp

from . import (ADV_S13, ADV_S15, ADV_S15_S, ADV_S18, ADV_S18_S, ADV_S19, ADV_S20, ADV_S20_S, ADV_S21, BUBBLE_AT,
               CHAIRS_S19, CHAIRS_S20, CHAIRS_S20_S, CLIENT_S15, CLIENT_S19, CLOCK_S19, CLOCK_S19_S, CLOCK_S20,
               CLOCK_S20_S, ENTRY_P3, FIG_BASE, IA_FLOOR, IA_FLOOR_S, IA_S18, IA_S18_S, IA_S19, IA_S19_S,
               MARKER_XS, PAGE_S18, PAGE_S18_S, PAGE_S19, PAGE_S19_S, PASTILLE_S20, PATH_TOP, PILL_TEXT, PILL_W,
               PLANK_AT, PLANK_H, STICKER_S16, TABLE_S19, TOI_PILL_DY, TOKEN_H, TOKEN_SIZE, TOKENS, morph_out,
               STEP_C, STEP_H, IA_W, seam, scene_f0, vanish)

# ---------- places propres à p3 (repère monde sauf mention) ----------
ICON_LOCAL = [-PILL_W / 2 + 30, 0]            # pictogramme de personne de la pastille (repère de la pilule)
HANG_DY = 78                                  # S15 « sans » : le fil 5 retombe de 78 px sous la case vide
TAMPON_HOLD = (560, 1075)                     # S16 : tampon fermé tenu devant lui, entre l'empreinte et sa tête
#                                               (STAMP_HOLD (720, 1040) est derrière lui : son bras est à gauche)
TAMPON_GRIP = [0, -54]                        # poignée du tampon fermé (repère du tampon)
BEAM_VIA = (380, 1200)                        # S16 : le faisceau de l'IA passe sous la page
ADV_S17_P3 = (632, 812)                       # S17 : à droite de la page ; d'ici la pointe atteint L1 et la rature
STAMP_SPOT = (458, 1125.5)                    # S17 « décides » : au pied de la page, la main sur la poignée
ADV_S16 = (700, 1125.5)                       # S16 : à droite, à 40 px au moins de l'autocollant (585, 940)
ADV_S17_END = (720, 1125.5)                   # S17 : il s'écarte du tampon, à droite du futur pivot (x 470-590)
STAMP_AT, STAMP_ROT = [0, 300], -4            # empreinte et tampon dans la bande libre du bas de la page, sans
#                                               dépasser son bord (STAMP_LOCAL [0, 314] à -6° débordait de 15 px)
PLANK_LX = ADV_S18[0] - PLANK_AT[0]           # 340 : ses pieds sur la planche (repère de la planche)
IA_S18_P3 = (IA_S18[0], round(PLANK_AT[1] - PLANK_H - 127, 1))   # l'IA debout SUR le bout gauche (pieds y 922)
CHEST_OFF = (-4, 18)                          # S18 : la fiche tenue contre sa poitrine (décalage du corps), x 0,2
HOLD_S = 0.2
CH_OFF = (-98, 2)                             # S18 : la pointe va chercher chaque poids devant sa poitrine
IA_STEP = (STEP_C[0], round(STEP_C[1] - STEP_H / 2 - 254 * 0.55 / 2, 1))   # l'IA debout sur sa marche, x 0,55
IA_STEP_S = 0.55
CARRY = 8                                     # S18 : images du transport d'un poids, de la poitrine à la pile
TOKEN_RIGHT = 245                             # bord droit du jeton du bas (repère de la planche) : avant son buste
TOKEN_LEAN = 12.8                             # chaque jeton décalé vers le pivot : à 12° la pile est d'aplomb, sans
#                                               toucher le conseiller
TOKEN_WS = [round(text_width(t, TOKEN_SIZE, 600) + 84) for t, _ in TOKENS]   # 200 / 262 / 311
TILTS = [4, 8, 12]
BROUILLON_P3 = 0.4                            # brouillon x 0,4 (200 x 288), plus lent, contour pointillé lisible
PEN_BAR = (380, 1150)                         # S19 « erreur » : pointe du stylo en travers du chemin, à SA gauche
#                                               (côté IA ; (520, 1150) est à sa droite, derrière lui)
CLIENT_S19_S = 0.75                           # assis : la tête au dossier du fauteuil
PILE_AT = (140, 1125)                         # S20 : centre de la pile dans ses bras, sous sa pilule « Toi »
PILE_REL = [(-10, 10, -18), (8, -6, 14), (-4, -16, -8), (12, 6, 18)]   # (dx, dy, rot) de doc1-4 : pile en éventail
FALLEN = {"doc3": ((105, 1180), -80), "doc1": ((392, 1182), 84)}       # S20 « cherché » : cartes tombées au sol
TABLE_S20_TOP = 1092                          # S20-S21 : dessus de la table (fauteuils x 0,75)
FICHE_S21_P3_S = 0.46                         # S21 : x 0,46, levée au-dessus de la table, entre les deux têtes
ADV_S21_P3 = (575, ADV_S21[1])                # S21 : devant le fauteuil gauche, sa pilule hors de la fiche
FICHE_S21_P3 = (705, 815)                     # bas de la fiche y 981 : au-dessus des têtes (client 1011, lui 1058)
CARD_C, CARD_W, CARD_H = (540, 800), 640, 560   # carte de fin (kit.outro) : centrée plus bas, bouton y 968
BTN_S22 = (CARD_C[0], CARD_C[1] + CARD_H / 2 - 112 / 2 - 56)
BTN_K = 1.75                                  # la pastille (60 px) devient le bouton (112 px de haut à peu près)
BTN_SIZE = 56                                 # libellé du bouton : 32 x 1,75


def _r(p):
    return [round(p[0], 2), round(p[1], 2)]


def _descends(S, i, root):
    """L'entité i descend-elle de root (parent, grand-parent…) ?"""
    p = S.ents[i].get("parent")
    while p:
        if p == root:
            return True
        p = S.ents[p].get("parent")
    return False


def part(S, kit, c):
    toi, toi2, client, sheet = c.toi, c.toi2, c.client, c.sheet
    rows, X, ty, ly = sheet.rows, sheet.x, sheet.ty, sheet.ly
    ai_h = c.ai_h
    p5 = sheet.lines[4][1]
    f0 = seam(S, "S15") + 1                                       # 1936 (« Une » calé à 1937 : début de scène)

    # ---------- raccord : etat_initial de S15 (ENTRY_P3), plus l'ancre des fils posée par p2 ----------
    S.set("fil5", aAt=[X["value"] + 6, rows[4] + ty])           # fil5 part, lui aussi, du bout de la valeur
    kit.pin(f0 - 1, {**ENTRY_P3, **{f"fil{i + 1}": {"draw": 1, "aAt": [X["value"] + 6, rows[i] + ty]}
                                    for i in range(4)}})
    if S.val("toi", "scale", f0 - 1) == 0:                        # partie construite seule : figurine absente
        toi.enter(f0 - 10, at=list(ADV_S13))

    S.set("empreinte", pos=list(STAMP_AT), rot=STAMP_ROT)
    S.set("tampon", pos=list(STAMP_AT), rot=STAMP_ROT)
    S.set("coche_relue", pos=[sheet.w / 2 - 6, -sheet.h / 2 - 6])  # S19 : à cheval sur le coin, hors du titre
    # la fiche elle-même n'est pas allégée : son titre vide deviendrait une barre encre (« Brief · ▬ », revue 1) ;
    # l'en-tête garde « Brief · 1 page » et la pastille
    lite_ids = ["tampon"] + [f"L{i + 1}" for i in range(5)] + [f"source{i + 1}" for i in range(5)]
    for id in lite_ids:
        kit.ensure(id, "lite", 0)

    def fw(pt, n):
        """Point local de la fiche -> monde à l'image n."""
        return _r(S.to_world("fiche", pt, n))

    def icon_w(n):
        return _r(S.to_world("pastille_fiche", ICON_LOCAL, n))

    # =================== S15 « Une info sans source n’est pas une certitude. C’est une question à poser au client. »
    f = kit.at("S15", "Une", "chaque source compacte remonte son fil jusqu'à sa date et s'y fond : la date devient une "
               "étiquette-source (pictogramme du document + date) ; les fils et les cases 1 à 4 s'effacent, la case 5 "
               "reste vide ; le conseiller redescend au pied de la page (x 1,1)")
    for i in range(4):
        d_id, src, fil = f"doc{i + 1}", f"source{i + 1}", f"fil{i + 1}"
        dst = S.to_world(src, [0, 0], f - 1)
        S.key(d_id, "z", f, 12.5 + 0.01 * i)                       # sous l'étiquette qu'il rejoint
        S.fly(d_id, f, MORPH, "inOut", to=_r(dst), scale=round(S.world_scale(src, f - 1), 4))
        S.key(d_id, "tag", f, 1, MORPH, "inOut")                   # la carte compacte se réduit en étiquette
        arr = f + MORPH
        S.key(fil, "opacity", arr - 3, 0, 3, "linear")             # le fil rentre avec elle (ancre b = la source)
        S.key(fil, "draw", arr, 0)
        S.key(d_id, "opacity", arr, 0)
        S.key(src, "tagged", arr - 1, 1)                           # la date devient l'étiquette-source
        S.key(src, "flash", arr, 1, 2, "out")
        S.key(src, "flash", arr + 2, 0, 3, "inOut")
        vanish(kit, f"case{i + 1}", f + 2, d=MORPH)
    toi.scale_to(f, ADV_S15_S, d=14)
    toi.walk(f, list(ADV_S15), d=14)

    f = kit.at("S15", "sans", "test de la ligne 5 : un surligneur cyan pâle passe sous « Horizon 5 ans » ; elle lance "
               "le même fil vers la case 5 : il touche un contour vide, se casse en tirets et retombe ; la case tremble "
               "et reste vide ; puis tenue de 1,6 s, rien ne bouge")
    sl_w = X["slot1"] - X["slot0"]
    sl_y = rows[4] + ty
    S.set("surligneur", w=sl_w)
    S.keys("surligneur", f - 1, w=0, pos=[X["slot0"], sl_y], scale=1)
    S.keys("surligneur", f, FADE, "out", w=sl_w, pos=[round((X["slot0"] + X["slot1"]) / 2, 1), sl_y])
    S.key("L5", "slotFill", f, 0, FADE, "out")
    kit.draw("fil5", f + 3, 7)
    touch = f + 10
    kit.shake("case5", touch, amp=6)
    S.key("fil5", "dashed", touch, 1)
    pb0 = S.val("fil5", "pb", touch - 1)
    S.key("fil5", "pb", touch + 1, [pb0[0] - 30, pb0[1] + HANG_DY], 9, "inOutSine")
    S.key("fil5", "sag", touch + 1, 34, 9, "inOutSine")

    f = kit.at("S15", "C’est", "le stylo du conseiller tape « 5 ans » : sous la pointe, la ligne 5 vire au rouge et se "
               "fend, sa moitié droite s'affaisse ; la coche pointillée de l'IA reste ; l'IA ne bouge pas")
    val_c = [X["value"] - p5["valueW"] / 2, ty]
    hit = toi.tap(f - TAP + 1, S.to_world("L5", val_c, f - 1))
    S.key("L5", "red", hit, 1, 3, "out")
    S.key("L5", "crack", hit, 1, POP, "out")
    S.key("L5", "slotFill", hit, 1, 3, "out")                     # le surligneur s'éteint sous la capsule rouge
    S.key("surligneur", "scale", hit + 3, 0)
    S.key("bande5", "opacity", hit, 0, 4, "linear")              # la capsule rouge de la ligne prend le relais
    vanish(kit, "nuage5", hit, d=4)

    f = kit.at("S15", "question", "un grand « ? » sort de la valeur fendue, puis monte en arc au-dessus du conseiller ; "
               "une bulle grandit autour, queue vers sa tête ; le fil retombé et la case 5 s'effacent")
    q_from = S.to_world("L5", line_crack_point(p5, val_c, 1.0), f - 1)
    S.key("question", "pos", f - 1, _r(q_from))
    kit.pop("question", f, scale=0.7)
    S.key("question", "pos", f + POP, list(BUBBLE_AT), MOVE, "inOut", arc=60)
    S.key("question", "scale", f + POP, 1, MOVE, "inOut")
    kit.pop("bulle", f + POP + 4, d=POP)
    arr = f + POP + MOVE
    S.key("bulle", "q", arr, 1)
    S.key("question", "scale", arr, 0)
    S.key("question", "opacity", arr, 0)
    vanish(kit, "case5", f, d=POP)
    S.key("fil5", "opacity", f, 0, POP, "linear")
    S.key("fil5", "draw", f + POP, 0)
    toi.rest(f + 2, 8)

    f = kit.at("S15", "client", "le client (figurine papier) naît du pictogramme de la pastille sur l'en-tête, fait le tour "
               "par la droite de la bulle et se pose face au conseiller ; il s'incline de 4° vers lui, immobile")
    kit.pulse("pastille_fiche", f, step=3)
    born = icon_w(f - 1)
    client.size = 0.3
    client.enter(f, at=born, d=5)
    route = [born, [born[0] + 130, born[1] - 40], [620, 470], [850, 640], [850, 900], list(CLIENT_S15)]   # x ≤ 850 (QA x > 940)
    client.scale_to(f + 3, 1.0, d=17, e="inOut")
    client.run(f + 3, route, 17)
    client.lean_to(f + 20, -4, d=5)

    # =================== S16 « Reste le plus important : la décision finale ne se délègue pas. » ===================
    f = kit.at("S16", "Reste", "la bulle se replie en autocollant « ? » (disque cyan 72 px) qui vole attendre à droite de "
               "la ligne 5, hors de la page ; le client reste immobile")
    S.key("bulle", "s", f, 1, 6, "out")
    S.key("bulle", "pos", f + 2, list(STICKER_S16), MOVE, "inOut", arc=30)
    toi.walk(f + 4, list(ADV_S16), d=10)                          # un pas à droite : l'autocollant n'est pas sa pensée

    f = kit.at("S16", "décision", "le conseiller range son stylo et sort de sa poitrine le tampon fermé (socle cyan "
               "profond, poignée encre, aucun texte), qu'il tient levé devant lui ; 8 images plus tard, le contour vide "
               "de l'empreinte se trace en tirets sur la bande libre du bas de la page")
    toi.walk(f, list(ADV_S16), d=8)
    toi.stow(f, d=4)
    f = f + 6
    sh = toi._shoulder(f - 1)
    rr = math.radians(-6)
    grip = [TAMPON_HOLD[0] - TAMPON_GRIP[1] * math.sin(rr), TAMPON_HOLD[1] + TAMPON_GRIP[1] * math.cos(rr)]
    dv = [grip[0] - sh[0], grip[1] - sh[1]]
    dl = math.hypot(*dv)
    pen_l = toi.pen_len * S.world_scale("toi", f - 1)
    virt_tip = [sh[0] + dv[0] / dl * (dl + pen_l), sh[1] + dv[1] / dl * (dl + pen_l)]   # stylo rangé : la main en grip
    toi.reach(f, virt_tip, d=8, step=False)
    off = [TAMPON_HOLD[0] - grip[0], TAMPON_HOLD[1] - grip[1]]
    for n, p in frames(f, 8, "out"):
        g = S.val(toi.pen, "pos", n)
        S.key("tampon_ferme", "pos", n, _r([g[0] + off[0], g[1] + off[1]]), 1, "linear")
        S.key("tampon_ferme", "scale", n, round(p, 4), 1, "linear")
    kit.draw("empreinte", f + 8, DRAW)

    f = kit.at("S16", "délègue", "un court faisceau pointillé de l'IA passe sous la page et touche le socle du tampon : "
               "le tampon ne bouge pas, tenu par sa main ; le faisceau se rétracte ; l'empreinte reste vide ; aucun rouge")
    socle = [TAMPON_HOLD[0] - 40, TAMPON_HOLD[1] + 22]           # coin gauche du socle, côté IA
    S.keys("faisceau_tampon", f - 1, pb=_r(socle), via=list(BEAM_VIA), draw=0, opacity=1)
    kit.draw("faisceau_tampon", f, 8, e="in")
    hit = f + 8                                                   # il casse net sur le tampon tenu
    S.key("impact_cadre", "pos", hit - 1, _r([socle[0] - 4, socle[1]]))
    kit.pop("impact_cadre", hit, d=3)
    S.key("eclat", "pos", hit - 1, _r(socle))
    S.key("eclat", "scale", hit - 1, 1.1)
    S.key("eclat", "p", hit - 1, 0)
    S.key("eclat", "p", hit, 1, 9, "out")
    S.key("eclat", "p", hit + 9, 0)
    vanish(kit, "impact_cadre", hit + 10, d=6)
    S.key("faisceau_tampon", "draw", hit + 8, 0, 10, "inOut")      # il recule, visiblement ; le tampon n'a pas bougé
    S.key("faisceau_tampon", "opacity", hit + 18, 0)

    # =================== S17 « Troisième étape : tu relis, tu corriges, tu décides. » ===================
    f = kit.at("S17", "Troisième", "le repère passe à « 3 · Relire » (le disque grandit puis revient) ; le client rentre "
               "dans le pictogramme de la pastille ; le conseiller range le tampon dans sa poitrine et monte à droite "
               "de la page, stylo vers la colonne des coches")
    arr = kit.step(f, 2)
    S.key("legende2", "under", f, 0, FADE, "inOut")
    kit.draw("legende3", f + 4, DRAW, track="under")
    S.key("chapitre", "pos", f - 1, [MARKER_XS[2], S.val("chapitre", "pos", f - 1)[1]])
    S.key("chapitre_txt", "text", f - 1, "3")
    S.key("chapitre", "scale", arr, 1)
    S.key("chapitre", "scale", arr + 1, 1.6, SCALE, "out")
    S.key("chapitre", "scale", arr + 11, 1, SCALE, "inOut")
    S.key("chapitre", "scale", arr + 21, 0)
    home = icon_w(f + 13)
    c0 = S.val("client", "pos", f - 1)
    client.lean_to(f, 0, d=3)
    client.scale_to(f, 0.25, d=14, e="inOut")
    client.run(f, [c0, [850, 900], [850, 640], [620, 470], home], 14)   # x ≤ 850 : rien sous la colonne x > 940
    client.exit(f + 14, d=3)
    kit.pulse("pastille_fiche", f + 15, step=3)
    chest = [S.val("toi", "pos", f - 1)[0], S.val("toi", "pos", f - 1)[1] - 10]
    vanish(kit, "tampon_ferme", f, into=chest, d=6)
    toi.walk(f + 2, [710, ADV_S17_P3[1]], d=10)                   # il monte à droite de l'autocollant « ? »,
    toi.walk(f + 12, list(ADV_S17_P3), d=5)                       # puis se place contre la page
    toi.unstow(f + 10)
    ticks = [sheet.world(S, i, "tick", n=f + 16) for i in range(5)]
    toi.reach(f + 17, [ticks[0][0] + 12, ticks[0][1] + 4], d=8, step=False)   # pointe en attente sur L1

    f = kit.at("S17", "relis", "la pointe descend la colonne des coches ; sur chaque ligne 1 à 4 la rangée se surligne le "
               "temps du passage, la coche pleine du conseiller (plus grande) se trace sur la coche pointillée de l'IA, "
               "qui s'efface sous elle, et l'étiquette-source s'allume ; la pointe s'arrête sur L5 sans cocher")
    hits = toi.trace(f, ticks, step=False)
    S.key("surligneur", "scale", hits[0] - 2, 1)
    for i in range(4):
        h = max(hits[i], f)
        S.key("surligneur", "pos", h - 1, [round((X["slot0"] + X["slot1"]) / 2, 1), rows[i] + ty])
        S.key(f"L{i + 1}", "slotFill", h - 1, 0, 2, "out")
        S.key(f"L{i + 1}", "slotFill", h + 4, 1, 3, "inOut")
        kit.draw(f"coche{i + 1}", h, 5)
        vanish(kit, f"coche_ia{i + 1}", h, into=_r(S.to_world("ia", c.brain_front, h + POP)), d=POP)
        S.key(f"source{i + 1}", "lit", h, 1, 4, "out")
    S.key("surligneur", "scale", max(hits[3], f) + 8, 0)

    f = kit.at("S17", "corriges", "d'un même trait, la pointe chasse la coche pointillée de l'IA de la ligne 5 et barre "
               "« 5 ans », qui tombe hors de la page ; la fente se referme, la ligne repasse à l'encre ; l'autocollant "
               "« ? » prend la place de la valeur, et « à poser au RDV » surgit dessous")
    kit.drop("coche_ia5", f + 1, out=True, h=130, dx=46, rot=55)   # chassée d'un coup de stylo, hors de la page
    a = S.to_world("L5", line_crack_point(p5, [X["value"] + 8, ty], 1.0), f - 1)
    b = S.to_world("L5", line_crack_point(p5, [X["value"] - p5["valueW"] - 8, ty], 1.0), f - 1)
    g = toi.strike(f, a, b, d=6, lead=3, line="L5")
    S.key("L5", "fall", g, 1, 7, "in")
    S.key("L5", "crack", g, 0, 8, "inOut")
    S.key("L5", "red", g, 0, 4, "out")
    S.key("L5", "alarm", g, 0, 4, "out")
    S.key("L5", "pulse", g, 0, 4, "out")
    vanish(kit, "anneau5", g, d=6)
    spot = S.to_world("autocollant", [0, 0], g + 1)
    S.fly("bulle", g + 1, 7, "inOut", to=_r(spot), scale=round(S.world_scale("autocollant", g + 1), 4), arc=24)
    S.key("bulle", "scale", g + 8, 0)
    S.key("bulle", "opacity", g + 8, 0)
    S.key("autocollant", "opacity", g + 8, 1)
    kit.pop("source5", g + 3, d=POP)

    f_dec = kit.at("S17", "décides", "le conseiller descend au pied de la page et abat le tampon dans le contour marqué : "
                   "« PRÊT POUR LE RDV » et « + 1 question » ; la page tremble, l'autocollant « ? » bat au contact ; "
                   "jamais « VALIDÉ »")
    w0 = g + 1
    toi.walk(w0, list(STAMP_SPOT), d=max(8, f_dec - w0))
    hit = toi.stamp(f_dec, "tampon", shake="fiche", step=False)
    S.key("tampon", "subOn", hit, 1, 3, "out")
    S.key("empreinte", "opacity", hit, 0)
    kit.pulse("autocollant", hit, peak=1.15, step=3)
    toi.walk(hit + 8, list(ADV_S17_END), d=12)                       # il s'écarte : le tampon se lit en entier

    # =================== S18 « L’IA prépare. Toi, tu gardes le conseil, l’adéquation et la responsabilité. » ======
    f = kit.at("S18", "L’IA", "le fil du repère descend et devient une planche sur un pivot ; disques et légendes "
               "s'effacent ; la fiche se réduit (allégée) sur le bout gauche ; l'IA regrandit à côté d'elle, debout "
               "sur la planche")
    kit.morph(["marqueur"], ["planche"], f)
    for k in range(3):
        S.key(f"legende{k + 1}", "opacity", f, 0, FADE, "out")
        S.key(f"legende{k + 1}", "scale", f + FADE, 0)
    S.keys("fiche", f, MORPH, "inOut", pos=list(PAGE_S18), scale=PAGE_S18_S)
    for id in lite_ids:
        S.key(id, "lite", f + 3, 1, 6, "inOut")
    S.keys("ia", f, MORPH, "inOut", pos=list(IA_S18_P3), scale=IA_S18_S)
    S.keys("ia_pill", f, MORPH, "inOut", pos=[0, -round(ai_h / 2 + 34, 1)], scale=1)
    for k in range(3):                                            # jetons calibrés : bord droit aligné, avant lui
        S.set(f"jeton{k + 1}", w=TOKEN_WS[k],
              pos=[round(TOKEN_RIGHT - TOKEN_LEAN * k - TOKEN_WS[k] / 2, 1),
                   round(-PLANK_H - TOKEN_H / 2 - (TOKEN_H + 4) * k, 1)])

    f = kit.at("S18", "prépare", "le conseiller monte sur le bout droit ; le faisceau pointillé de l'IA pousse la fiche "
               "le long de la planche et la porte jusqu'à lui, sans jamais la lâcher ; il la prend contre sa poitrine ; "
               "la planche reste à plat")
    toi.walk(f, list(ADV_S18), d=MOVE)
    slide = [660, PAGE_S18[1]]
    S.key("fiche", "pos", f, slide, 12, "inOut")
    chest = [ADV_S18[0] + CHEST_OFF[0], ADV_S18[1] + CHEST_OFF[1]]
    S.keys("fiche", f + 12, 8, "inOut", pos=list(chest), scale=HOLD_S)
    taken = f + 20                                                # la fiche est dans ses mains
    # la fiche passe DEVANT lui (contre sa poitrine) mais sous son bras : toute la fiche entre en z 15,05-15,35
    fiche_ids = [i for i, e in S.ents.items() if i == "fiche" or _descends(S, i, "fiche")]
    for i in fiche_ids:
        z0 = S.ents[i]["z"]
        kit.ensure(i, "z", z0)
        S.key(i, "z", f + 12, round(15.05 + (z0 - 8) * 0.05, 3))
    S.keys("faisceau_passe", f - 1, draw=0, opacity=1, **{"from": 0})
    kit.draw("faisceau_passe", f, 4)
    for n in range(f - 1, taken + 1):                             # le faisceau la tient jusqu'à ses mains
        S.key("faisceau_passe", "pb", n, fw([-250, 60], n), 1, "linear")
    S.key("faisceau_passe", "draw", taken + 1, 0, 6, "out")
    S.key("faisceau_passe", "opacity", taken + 7, 0)

    f = kit.at("S18", "Toi", "la pilule « Toi » surgit au-dessus de sa tête ; une petite marche surgit à côté du pivot ; "
               "l'IA en descend lentement et s'y pose, à hauteur, tournée vers lui ; ils échangent un petit signe de tête")
    kit.pop("toi_pill", f)
    kit.pop("marche", f, d=POP)
    kit.ensure("ia", "z", S.ents["ia"]["z"])
    S.key("ia", "z", f + 2, 6.6)                                  # elle descend DEVANT la planche, pas au travers
    kit.ensure("ia_pill", "z", S.ents["ia_pill"]["z"])
    S.key("ia_pill", "z", f + 2, 6.7)
    S.keys("ia", f + 2, 20, "inOut", arc=24, pos=list(IA_STEP), scale=IA_STEP_S)
    pill_x = -(IA_W / 2 * IA_STEP_S + 12 + 46) / IA_STEP_S         # pilule « IA » à sa gauche, hors de la marche
    S.keys("ia_pill", f + 2, 20, "inOut", pos=[round(pill_x, 1), 0], scale=round(1 / IA_STEP_S, 4))
    kit.ensure("ia", "rot", 0)
    nod = f + 18
    S.key("ia", "rot", nod, 7, 4, "out")                          # l'IA salue…
    S.key("ia", "rot", nod + 4, 0, 4, "inOut")
    toi.lean_to(nod + 3, -5, d=4)                                 # … il répond
    toi.lean_to(nod + 7, 0, d=4)

    # « conseil », « l’adéquation », « responsabilité » : la pointe va chercher chaque poids devant sa poitrine, le
    # porte, le pose sur la pile ; la planche penche à chaque pose ; les pilules restent horizontales
    f_c = kit.at("S18", "conseil", "sa pointe va chercher devant sa poitrine la pilule « Conseil » (cochée en S05), la "
                 "porte et la pose sur son bout de planche, où elle devient le premier poids ; la planche penche de 4°")
    f_a = kit.at("S18", "l’adéquation", "même geste : le poids « Adéquation » sort devant sa poitrine au bout du stylo, "
                 "est porté et posé sur le premier ; la planche penche à 8°")
    f_r = kit.at("S18", "responsabilité", "même geste : « Responsabilité » posé en haut de la pile ; la planche penche "
                 "à 12° et s'arrête net ; il reste droit, la fiche contre lui, la pointe sur ses poids ; l'IA, sur sa "
                 "marche, reste visible")
    f_dix = scene_f0(S, "S19")
    beats = [f_c, f_a, f_r]
    lands = [b + 8 + CARRY for b in beats]
    seats = [S.val(f"jeton{k + 1}", "pos", f_c) for k in range(3)]   # places sur la planche (repère de la planche)
    grips = [[seats[k][0] + TOKEN_WS[k] / 2 - 20, seats[k][1]] for k in range(3)]   # la pointe tient le bout droit
    s18 = ADV_S18_S
    kit.ensure("conseil", "z", S.ents["conseil"]["z"])
    S.keys("conseil", f_c + 5, pos=[0, 0], z=15.8, opacity=1, scale=0)
    for k in range(3):
        kit.ensure(f"jeton{k + 1}", "rot", 0)

    def body_at(n):
        if n < lands[0]:
            return list(ADV_S18)
        feet = S.to_world("planche", [PLANK_LX, -PLANK_H], n)
        return _r([feet[0], feet[1] - FIG_BASE * s18])

    def ease(t):
        t = min(1.0, max(0.0, t))
        return t * t * (3 - 2 * t)

    rest_tip = toi.tip(f_c - 1)
    for n in range(f_c, f_dix):
        for k, L in enumerate(lands):                             # la planche penche à la pose
            if n == L:
                S.key("planche", "rot", L, TILTS[k], 12 if k == 0 else 14, "out")
        prot = S.val("planche", "rot", n)
        body = body_at(n)
        ch = [body[0] + CH_OFF[0] * s18, body[1] + CH_OFF[1] * s18]
        k = max(i for i, b in enumerate(beats) if b <= n)
        b, L = beats[k], lands[k]
        prev = rest_tip if k == 0 else S.to_world("planche", grips[k - 1], n)
        seat_tip = S.to_world("planche", grips[k], n)
        if n < b + 6:
            tip = lerp(prev, ch, ease((n - b + 1) / 6))
        elif n < b + 8:
            tip = ch
        elif n < L:
            tip = lerp(ch, seat_tip, ease((n - b - 7) / CARRY))
        else:
            tip = seat_tip
        tip = _r(tip)
        toi.hop(n, body, 1, h=0, lean=0)
        toi.reach(n, tip, d=1, step=False)
        S.key("fiche", "pos", n, _r([body[0] + CHEST_OFF[0], body[1] + CHEST_OFF[1]]), 1, "linear")
        tok = "conseil" if k == 0 else f"jeton{k + 1}"
        if b + 6 <= n < L:                                       # le poids, au bout du stylo
            center = [tip[0] - (TOKEN_WS[k] / 2 - 20), tip[1]]
            if n == b + 6:
                S.key(tok, "scale", n, 1, 4, "out")
            if k == 0:
                S.key(tok, "pos", n, _r(center), 1, "linear")
            else:
                S.key(tok, "pos", n, _r(S.to_local("planche", center, n)), 1, "linear")
                S.key(tok, "rot", n, round(-prot, 2), 1, "linear")
        if n == L:                                                # posé : relais (Conseil -> jeton1), à sa place
            if k == 0:
                S.key("conseil", "scale", n, 0)
                S.key("conseil", "opacity", n, 0)
                S.key("jeton1", "scale", n, 1)
            S.key(f"jeton{k + 1}", "pos", n, [round(v, 1) for v in seats[k]])
        for j in range(3):                                        # les poids posés restent horizontaux
            if n >= lands[j]:
                S.key(f"jeton{j + 1}", "rot", n, round(-prot, 2), 1, "linear")

    # =================== S19 « Dix minutes de relecture valent mieux qu’une erreur devant le client. » ===========
    f = kit.at("S19", "Dix", "la planche revient à plat et devient le chemin ; les jetons rentrent dans sa poitrine, la "
               "pilule « Toi » s'efface ; il se pose sur le chemin, la fiche devant lui ; l'IA au départ du chemin ; "
               "l'horloge quitte le badge et grandit au-dessus de lui")
    toi.scale_to(f, 1.0, d=MOVE)
    toi.walk(f, list(ADV_S19), d=MOVE)
    for k in range(3):                                            # les jetons rentrent dans sa poitrine…
        vanish(kit, f"jeton{k + 1}", f + k, into="toi", d=6)
    vanish(kit, "toi_pill", f, d=POP)
    S.key("planche", "rot", f, 0, 8, "out")                       # … pendant que la planche revient à plat,
    kit.morph(["planche"], ["chemin"], f + 6)                     # puis s'étire en chemin
    S.keys("fiche", f + 2, MOVE - 2, "inOut", pos=list(PAGE_S19), scale=PAGE_S19_S)   # la même fiche, posée devant
    morph_out(kit, ["marche"], f + 6)
    S.keys("ia", f + 6, MOVE, "inOut", pos=list(IA_S19), scale=IA_S19_S)          # décalés : l'IA à + 6,
    S.key("ia", "z", f + 6 + MOVE, S.ents["ia"]["z"])
    S.key("ia_pill", "z", f + 6 + MOVE, S.ents["ia_pill"]["z"])
    S.keys("ia_pill", f + 6, MOVE, "inOut", pos=[0, -round((ai_h * IA_S19_S / 2 + 30) / IA_S19_S, 1)],
           scale=round(1 / IA_S19_S, 4))
    S.keys("horloge", f + 4, MOVE, "inOut", pos=list(CLOCK_S19), scale=CLOCK_S19_S)   # l'horloge à + 4

    f = kit.at("S19", "relecture", "sa pointe descend la fiche pendant qu'un secteur de dix minutes se remplit sur le "
               "cadran, au même rythme ; « 10 min » compte de 0 à 10 ; à la fin, une coche pleine se trace sur le coin "
               "de la fiche")
    pts = [sheet.world(S, i, "tick", n=f) for i in range(5)]
    toi.trace(f - 4, pts, d=18, lead=4, step=False)
    S.key("secteur", "value", f, 10, 18, "linear")
    kit.pop("dix_min", f, d=6)
    S.key("dix_min", "value", f, 10, 18, "linear")
    done = f + 18
    kit.draw("coche_relue", done, 6)
    kit.pulse("secteur", done, peak=1.12, step=2)
    toi.rest(done, 8)

    f = kit.at("S19", "valent", "les fauteuils du rendez-vous surgissent seuls au bout du chemin ; puis la fiche relue file "
               "au-dessus de lui jusqu'à leur table")
    kit.pop("fauteuils", f)
    S.key("fiche", "pos", f + 6, list(TABLE_S19), MOVE, "inOut", arc=60)        # arc bas, le long du chemin
    S.key("fiche", "scale", f + 6, 0.2, MOVE, "inOut")

    f = kit.at("S19", "erreur", "de la tête de l'IA sort son brouillon non relu (contour et coches pointillés, ligne 5 "
               "en rouge) qui file sur le chemin vers la droite ; le conseiller abaisse son stylo en travers du chemin")
    f_dev = S.word_after("devant", f)
    toi.reach(f, list(PEN_BAR), d=6, step=False)
    bh = 720 * BROUILLON_P3
    bump = [PEN_BAR[0] - 250 * BROUILLON_P3 - 2, PATH_TOP - bh / 2]
    head = S.to_world("ia", c.brain_front, f - 1)
    S.keys("brouillon", f - 1, pos=_r(head), scale=0, opacity=1)
    S.key("brouillon", "scale", f, BROUILLON_P3, 5, "out")
    S.key("brouillon", "pos", f, _r(bump), f_dev - f, "linear")

    f = kit.at("S19", "devant", "le brouillon bute sur la pointe du stylo (traits d'impact), s'écrase un peu, y reste "
               "collé, puis se fend en deux moitiés qui tombent sous le chemin ; sa bande rouge reste sous le chemin")
    tip = toi.tip(f)
    S.key("impact_brouillon", "pos", f - 1, _r([tip[0] - 4, tip[1]]))
    kit.pop("impact_brouillon", f, d=2)
    S.key("eclat", "pos", f - 1, _r(tip))
    S.key("eclat", "scale", f - 1, 1.2)
    S.key("eclat", "p", f - 1, 0)
    S.key("eclat", "p", f, 1, 9, "out")
    S.key("eclat", "p", f + 9, 0)
    vanish(kit, "impact_brouillon", f + 10, d=5)
    kit.ensure("brouillon", "sx", 1)
    S.key("brouillon", "sx", f, 0.84, 2, "out")
    S.key("brouillon", "pos", f, _r([bump[0] + 250 * BROUILLON_P3 * 0.16, bump[1]]), 2, "out")   # bord droit collé
    brk = f + 9                                                   # tenue de 8 images contre la pointe
    bp = S.val("brouillon", "pos", brk - 1)
    S.key("brouillon", "scale", brk, 0)
    S.key("brouillon", "opacity", brk, 0)
    for k, (dx, rot) in enumerate(((-30, -16), (26, 14))):        # les moitiés tombent peu, et s'effacent (y < 1250)
        m = f"moitie{k + 1}"
        S.keys(m, brk - 1, pos=_r(bp), scale=round(BROUILLON_P3 * 0.84, 4), opacity=1)
        kit.drop(m, brk, out=True, h=32, dx=dx, rot=rot)
        vanish(kit, m, brk + DROP - 4, d=6)
    band = [bp[0] + (X["slot0"] + X["slot1"]) / 2 * BROUILLON_P3 * 0.84, bp[1] + rows[4] * BROUILLON_P3]
    S.keys("bande_rouge", brk - 1, pos=_r(band), scale=round(BROUILLON_P3 * 0.84 / 0.4, 4), opacity=1)
    S.key("bande_rouge", "pos", brk, [round(band[0], 1), round(band[1] + 32, 1)], DROP, "in")
    vanish(kit, "bande_rouge", brk + DROP - 4, d=6)               # la bande rouge s'efface avec le papier

    f = kit.at("S19", "client", "le client naît du pictogramme de la pastille, sur la fiche posée sur la table, et "
               "s'assoit dans le fauteuil droit, tourné vers la gauche")
    born = icon_w(f - 1)
    client.size = 0.25
    client.enter(f, at=born, d=4)
    client.scale_to(f + 2, CLIENT_S19_S, d=16, e="inOut")
    client.run(f + 2, [born, [born[0] + 70, born[1] - 70], list(CLIENT_S19)], 16)
    toi.rest(f, 8)

    # =================== S20 « Avant, tu arrives en ayant cherché. » ===================
    f = kit.at("S20", "Avant", "un trait vertical partage l'écran ; « Avant » surgit à gauche ; le rendez-vous (fauteuils, "
               "client, fiche) se range dans la moitié droite ; chemin, bande rouge, compteur et IA se réduisent en "
               "points ; le conseiller marche dans la moitié gauche (x 0,9)")
    kit.draw("separateur", f + 9, DRAW)                           # l'horloge part d'abord : le trait ne la coupe pas
    kit.pop("avant", f)
    S.keys("horloge", f, MOVE, "inOut", pos=list(CLOCK_S20), scale=CLOCK_S20_S)   # l'horloge de 9 h, au-dessus de lui

    def chairs_map(pt):
        return _r([CHAIRS_S20[0] + (pt[0] - CHAIRS_S19[0]) * CHAIRS_S20_S,
                   CHAIRS_S20[1] + (pt[1] - CHAIRS_S19[1]) * CHAIRS_S20_S])
    S.keys("fauteuils", f, MOVE, "inOut", pos=list(CHAIRS_S20), scale=CHAIRS_S20_S)
    S.keys("fiche", f, MOVE, "inOut", pos=chairs_map(TABLE_S19), scale=round(0.2 * CHAIRS_S20_S, 4))
    client.scale_to(f, round(CLIENT_S19_S * CHAIRS_S20_S, 4), d=MOVE)
    client.hop(f, chairs_map(CLIENT_S19), MOVE, h=0, lean=0)
    morph_out(kit, ["chemin", "bande_rouge", "ia", "dix_min"], f)
    S.key("secteur", "value", f, 0, 6, "out")
    toi.scale_to(f, ADV_S20_S, d=MOVE)
    toi.walk(f, list(ADV_S20), d=MOVE)

    f = kit.at("S20", "tu", "sa pilule « Toi » surgit au-dessus de sa tête ; l'horloge glisse dans la moitié gauche et se "
               "réduit au-dessus de lui : l'image du début")
    kit.pop("toi_pill", f)

    f = kit.at("S20", "arrives", "la vieille pile des 4 sources tombe de travers dans ses bras ; à droite, la fiche se "
               "replie dans sa pastille, qui saute par-dessus le séparateur et attend au-dessus de lui : la table du "
               "rendez-vous est vide")
    toi.stow(f, d=4)                                              # les bras pleins : plus de stylo
    for i, (dx, dy, rot) in enumerate(PILE_REL):
        d_id, fi = f"doc{i + 1}", f + 2 * i
        z = round(15.2 + 0.03 * i, 2)
        S.keys(d_id, fi - 1, compact=0, tag=0, txt=1, sh=6, lit=0, scale=0.5, rot=rot, z=z, opacity=0)
        for ch, dz in ((f"{d_id}_bandeau", 0.01), (f"{d_id}_bandeau_txt", 0.015)):
            kit.ensure(ch, "z", S.ents[ch]["z"])
            S.key(ch, "z", fi - 1, round(z + dz, 3))
        S.key(f"{d_id}_bandeau", "opacity", fi - 1, 1)
        kit.drop(d_id, fi, h=220, to=[PILE_AT[0] + dx, PILE_AT[1] + dy])
    pf = S.to_world("pastille_fiche", [0, 0], f - 1)
    S.keys("pastille", f - 1, pos=_r(pf), scale=round(S.world_scale("pastille_fiche", f - 1), 4), opacity=1,
           text=PILL_TEXT)
    S.key("pastille_fiche", "opacity", f, 0)
    vanish(kit, "fiche", f, into=_r(pf), d=MORPH)
    S.key("pastille", "pos", f + 2, list(PASTILLE_S20), MOVE, "inOut", arc=80)
    S.key("pastille", "scale", f + 2, 1, MOVE, "inOut")

    f = kit.at("S20", "cherché", "deux cartes (« Mail », puis « PDF ») glissent de la pile et tombent lentement au sol, "
               "où elles restent ; traits de vitesse ; le conseiller, débordé, se penche en arrière")
    for k, d_id in enumerate(("doc3", "doc1")):
        g = f + 3 * k
        to, rot = FALLEN[d_id]
        x0, y0 = S.val(d_id, "pos", g - 1)
        S.key(d_id, "pos", g, list(to), DROP + 5, "in", arc=40)
        S.key(d_id, "rot", g, rot, DROP + 5, "inOut")
        v = f"{d_id}_vitesse"                                     # traits de vitesse, au-dessus de la carte qui tombe
        trail = math.degrees(math.atan2(y0 - to[1], x0 - to[0]))
        S.key(v, "rot", g + 1, round(trail - S.val(d_id, "rot", g + 3), 2))
        for j in range(3):
            S.key(f"{v}{j + 1}", "z", g + 1, 15.1)
        kit.pop(v, g + 3, d=3)
        vanish(kit, v, g + 10, d=5)
    toi.lean_to(f, 8, d=9)

    # =================== S21 « Après, tu arrives en ayant compris. » ===================
    f = kit.at("S21", "Après", "« Après » surgit en cyan à droite ; la pastille saute par-dessus le séparateur jusqu'à la "
               "table et la fiche relue se redéplie sous elle, debout sur la table, tamponnée")
    kit.pop("apres", f)
    S.keys("fiche", f + 3, pos=list(FICHE_S21_P3), scale=0, opacity=1)
    kit.pop("fiche", f + 6, scale=FICHE_S21_P3_S, d=MORPH)
    arr = f + MOVE
    head_pt = S.to_world("pastille_fiche", [0, 0], arr)
    S.key("pastille", "pos", f, _r(head_pt), MOVE, "inOut", arc=120)
    S.key("pastille", "scale", f, round(S.world_scale("pastille_fiche", arr), 4), MOVE, "inOut")
    S.key("pastille", "scale", arr, 0)
    S.key("pastille", "opacity", arr, 0)
    S.key("pastille_fiche", "opacity", arr, 1)

    f = kit.at("S21", "arrives", "le conseiller entre à droite et se place devant le fauteuil gauche, face au client ; la "
               "pilule « Toi » quitte celui de gauche, saute le séparateur et se pose sur lui : c'est le même, après")
    start = [545, ADV_S21[1]]                                      # juste à droite du séparateur
    toi2.enter(f, at=start, d=6)
    toi2.walk(f + 6, list(ADV_S21_P3), d=10)
    pv = S.to_world("toi_pill", [0, 0], f - 1)
    S.keys("toi_pill_vol", f - 1, pos=_r(pv), scale=round(S.world_scale("toi_pill", f - 1), 4), opacity=1)
    S.key("toi_pill", "scale", f, 0)
    S.key("toi_pill", "opacity", f, 0)
    dest = [ADV_S21_P3[0], ADV_S21_P3[1] + TOI_PILL_DY * ADV_S20_S]
    S.key("toi_pill_vol", "pos", f, _r(dest), MOVE, "inOut", arc=100)
    S.key("toi_pill_vol", "scale", f, ADV_S20_S, MOVE, "inOut")
    arr = f + MOVE
    S.key("toi_pill_vol", "scale", arr, 0)
    S.key("toi_pill_vol", "opacity", arr, 0)
    S.key("toi2_pill", "scale", arr, 1)

    f = kit.at("S21", "compris", "l'autocollant « ? » quitte la ligne 5, grossit et vole en arc jusqu'à la tête du "
               "client ; le client répond par une bulle de parole d'où part une pastille cyan pleine, qui vole remplir la "
               "puce vide de la ligne 5 ; la ligne bat, se surligne, et reçoit la coche pleine ; à gauche, rien ne bouge")
    st = S.to_world("autocollant", [0, 0], f - 1)
    S.keys("bulle", f - 1, pos=_r(st), scale=round(S.world_scale("autocollant", f - 1), 4), s=1, q=1, glyph=0,
           opacity=1, rot=0)
    S.key("autocollant", "opacity", f, 0)
    chead = S.to_world("client", [0, -96], f - 1)
    S.key("bulle", "pos", f, _r([chead[0] - 6, chead[1] - 40]), 6, "inOut", arc=70)
    S.key("bulle", "scale", f, 0.8, 6, "inOut")                   # « ? » de 56 px environ
    vanish(kit, "bulle", f + 6, into=_r(chead), d=4)
    mouth = S.to_world("client", [-22, -60], f + 6)
    bub = _r([mouth[0] - 46, mouth[1] - 44])
    S.key("reponse_bulle", "pos", f + 5, bub)
    kit.pop("reponse_bulle", f + 6, d=4)                          # il répond : une bulle de parole…
    S.key("reponse", "pos", f + 6, bub)
    kit.pop("reponse", f + 7, d=4)                                # … qui contient une pastille cyan pleine (56 px)
    land = f + 19
    bullet = S.to_world("fiche", [X["bullet"], rows[4] + ty], land)
    S.key("reponse", "pos", f + 11, _r(bullet), 8, "inOut", arc=-40)   # sous les rangées 1-4, jamais à travers
    S.key("reponse", "scale", f + 15, round(44 / 56 * S.world_scale("fiche", land), 4), 4, "in")
    vanish(kit, "reponse_bulle", f + 13, d=5)
    S.key("reponse", "scale", land, 0)
    S.key("reponse", "opacity", land, 0)
    S.key("reponse5", "scale", land, 1)                           # la puce de L5 est remplie (relais, sur la fiche)
    kit.pulse("reponse5", land + 1, peak=1.35, step=2)
    kit.draw("coche5", land, 4)                                   # le « ? » de la ligne devient une coche pleine
    sl_c = [round((X["slot0"] + X["slot1"]) / 2, 1), rows[4] + ty]
    S.keys("surligneur", land - 1, pos=sl_c, w=X["slot1"] - X["slot0"], scale=1, opacity=1)
    S.key("surligneur", "opacity", land + 6, 0, 3, "linear")
    toi2.lean_to(f + 12, 4, d=6)
    client.lean_to(f + 12, -4, d=6)

    # =================== S22 « Abonne-toi pour comprendre ton argent. » ===================
    # la fiche relue devient la carte de fin ; la pastille du fil devient le bouton « S’abonner » (relais exacts :
    # kit.outro card_at / btn_at, aucune carte ni bouton générique ne surgit)
    f_end = S.word_after("argent", scene_f0(S, "S22"))
    card = scene_f0(S, "S22")
    outs = ["separateur", "avant", "apres", "doc1", "doc2", "doc3", "doc4", "fauteuils"]
    out = kit.outro("S22", outs=outs, press=f_end - card, pos=CARD_C, w=CARD_W, h=CARD_H, clear="fade",
                    card_at=MORPH, btn_at=MOVE + 1, labelSize=34, bsize=BTN_SIZE)
    card = out["card"]
    toi.exit(card)
    toi2.exit(card)
    client.exit(card)
    vanish(kit, "horloge", card + MORPH, d=POP)                  # un PNG à la fois : fauteuils, puis horloge
    # la fiche monte au centre et s'élargit exactement en carte ; son contenu s'efface en fin de trajet
    S.fly("fiche", card, MORPH, "inOut", to=list(CARD_C), scale=1)
    kit.ensure("fiche", "sx", 1)
    kit.ensure("fiche", "sy", 1)
    S.key("fiche", "sx", card, round(CARD_W / 500, 4), MORPH, "inOut")
    S.key("fiche", "sy", card, round(CARD_H / 720, 4), MORPH, "inOut")
    content = [i for i in S.ents if _descends(S, i, "fiche") and i != "pastille_fiche"]
    for i in content:
        S.key(i, "opacity", card + 6, 0, 5, "linear")
    S.key("fiche", "opacity", card + MORPH, 0)                    # relais : la carte de fin, à la même place
    S.key("fiche", "scale", card + MORPH + 1, 0)
    hp = S.to_world("pastille_fiche", [0, 0], card - 1)
    kit.ensure("pastille", "z", S.ents["pastille"]["z"])
    S.keys("pastille", card - 1, pos=_r(hp), scale=round(S.world_scale("pastille_fiche", card - 1), 4), opacity=1,
           z=41, w=PILL_W)
    S.key("pastille_fiche", "opacity", card, 0)
    S.keys("pastille_btn", card - 1, pos=_r(hp), scale=round(S.world_scale("pastille_fiche", card - 1), 4), w=PILL_W)
    for pid in ("pastille", "pastille_btn"):                      # même trajet : la pastille devient le bouton
        S.keys(pid, card + 1, MOVE, "inOut", pos=list(BTN_S22), scale=BTN_K, w=round(380 / BTN_K, 1))
    sw = card + 8                                                 # en vol, son texte devient « S’abonner » et son
    S.key("pastille", "opacity", sw, 0)                           # pictogramme s'efface (relais à la même place)
    S.key("pastille_btn", "opacity", sw, 1)
    btn = card + MOVE + 1                                         # relais : le bouton de la carte, à la même place
    S.key("pastille_btn", "scale", btn, 0)
    S.key("pastille_btn", "opacity", btn, 0)
