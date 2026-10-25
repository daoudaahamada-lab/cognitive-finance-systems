"""V15, partie 1 : S01-S08, images 0-899 (29 temps forts, 30,0 s). Accroche, contexte, début du point 1.

ÉTAT D'ENTRÉE (image 0 = état de distribution, rien à épingler) : ivoire, `sol` (y 1232) ; « Toi » au sol en TOI_P0
(862, 1135), bras BAISSÉ (toi.hold_low(0, f_premier_geste) : jamais le stylo levé à l'image 0), étiquette `nom_toi`
au-dessus de la tête (NOM_SOL) ; la `pastille` « Ton argent » posée au sol en PASTILLE_SOL0 (640, 1198). Rien d'autre.

RÈGLES DE LA PARTIE
- « Toi » ne bouge que par Figure (walk / hop / tap / reach / lean_to / lower / hold_low / rest). lean_to et hop
  remettent la main au repos (stylo levé) : quand le bras doit rester baissé (affaissé, ballant), appeler APRÈS eux
  toi.hold_low(fa, fb) (la dernière méthode appelée gagne sur les images communes) ; walk(..., low=True).
- Penché « en avant » = vers la gauche = lean NÉGATIF (LEAN_AFFAISSE -10, LEAN_VERS -6, LEAN_POUSSE -14).
- La tour : blocs bloc1-4 (shape round, pistes pos / w / h / fill), enfants bloc*_ico / bloc*_nom (block_children) ;
  la pastille au sommet bouge avec la MÊME clé que le bloc du haut.
- Rouge : seulement la jauge qui se vide (S08).

SCÈNE PAR SCÈNE (ids de la distribution)
- S01 (0-109) « promis » : contact sur le mot (hit = toi.tap(f - TAP + 1, PASTILLE_TAP0)) ; kit.pulse("pastille", hit,
  peak 1,1). « reprendre » : kit.move("pastille", f, PASTILLE_MAIN, arc=80) et toi.reach(f, PASTILLE_MAIN_TIP) dans
  les mêmes images ; la pointe reste sur le bout droit. « week-end. » : drop_in(kit, "calendrier", f, h=100) (texte
  Week-end, scale 1). Résultat : argent au bout du stylo, « Week-end ».
- S02 (110-168) « lundi, » : calendrier text Lundi, w cal_w("Lundi") en 6 images, pulse 1,1. « lâché ? » : la
  pastille quitte la pointe et tombe à y 1198 (DROP, e « in », rot 8), puis glisse à PASTILLE_TOMBEE (460, 1198) en
  MOVE e « out », rot 0, ENTIÈRE ; en même temps toi.lean_to(f, LEAN_AFFAISSE) puis toi.lower / hold_low : affaissé,
  tête basse, bras ballant, qu'il garde.
- S03 (169-264) « grand » : les 4 blocs poussent du sol sous la pastille, l'un après l'autre (scale 1 + h 0 à f-1 au
  sol, puis h 100 et pos centre en 5 images e « out », décalés de 4 images) : tower(i, 100) ; à chaque bloc la pastille
  monte de 100 px jusqu'à PASTILLE_TOUR[100] ; « Toi » se redresse (lean 0, bras baissé). « plan » : kit.draw
  ("accolade", f, 9) de bas en haut, kit.type("gp_nom", f, rate=2). « échoue. » : walk(low) vers TOI_BUTE en 8 images,
  au contact kit.shake des 4 blocs + pastille (amp 6, mêmes images), puis toi.hop(…, TOI_P0, 12) à reculons. Résultat
  : la tour « Grand plan » (x 300-620, y 830-1230), l'argent au sommet (460, 798), « Toi » repoussé.
- S04 (265-350) « avancer » : toi.lean_to(f, LEAN_VERS), bras baissé. « seule » : `apercu` (petite marche « 1 » en
  tirets) scale 1 en APERCU_CACHE derrière B1 (z 5,9) puis kit.move vers APERCU_C (702, 1180) en MORPH e « out ».
  Le storyboard dit « Toi se redresse » ici MAIS l'état initial de S05 le veut encore penché : garder LEAN_VERS
  jusqu'à « piège ».
- S05 (351-549) « piège » : apercu glisse vers APERCU_CACHE puis disparaît dans B1 (scale 0 à l'arrivée) ;
  kit.pulse("gp_nom", …, 1,12) ; kit.shake des blocs (amp 4) ; « Toi » se redresse (lean 0). « tout » : les 4 blocs
  battent ensemble x1,04 (6 images), la pastille aussi. « budget, » / « épargne, » / « placements, » / « papiers. » :
  kit.pop(bloc_i_ico, f) + kit.type(bloc_i_nom, f, rate=2), de bas en haut.
- S06 (550-678) « week-end » : walk(low) vers TOI_PIED_TOUR en 14 images ; calendrier -> Week-end (texte, w), pulse.
  « entier. » : `cadran` à CADRAN_CAL (start 0, value 0 à f-1), kit.pop(from_pt=CAL_C) ; S.key value 60 en 30 images
  linéaire (tour complet de l'aiguille) ; pendant ce temps deux hop (h 60) vers TOI_SAUT_TOUR et retour (2 x 12), la
  tour tremble à chaque contact (amp 3). « lundi, » : calendrier -> Lundi. « abandonne, » : walk(low) à reculons vers
  TOI_P0 (16 images) puis lean_to(LEAN_AFFAISSE) + hold_low : la pose de S02. « trop. » : les 4 blocs battent x1,05 ;
  l'horloge pleine reste.
- S07 (679-770) « Pourquoi » : kit.vanish("cadran", f, into=CAL_C) ; kit.pop("grand_q", f) ; lean 0. « bloque ? » :
  walk vers TOI_TEND (6 images) ; toi.reach(…, TEND_TIP, step=False) : la pointe s'arrête 76 px sous l'argent, tenue
  0,4 s ; puis bras qui retombe (lower) ; kit.pulse("grand_q", peak 1,15). « manque » : jauge `energie` (value 1, fill
  CYAN) kit.pop(from_pt=ENERGIE_SORTIE) qui monte se poser en ENERGIE_C (prendre d=MOVE pour que le trajet se lise) ;
  kit.fade("energie_nom", …) : c'est SON énergie. « volonté. » : deux hop sur place (h 30, 2 x 8) ; pulse énergie 1,08.
- S08 (771-899) « Tout » : kit.vanish("grand_q", f, into=centre de bloc4) ; les 4 blocs battent. « demande » : walk
  vers TOI_POUSSE (8 images) ; lean_to(LEAN_POUSSE) PUIS toi.reach(…, (622, 1080)) (le reach après le lean) ; la
  tour tremble à peine (amp 2). « d’énergie » : energie value 1 -> 0 en 30 images linéaire et fill CYAN -> RED (hex)
  dans les mêmes images ; aussitôt après, lower, walk(low) vers TOI_RECUL (8 images), lean_to(LEAN_AFFAISSE) +
  hold_low. « décisions. » : q1-q8 (2 par bloc, déclarés au centre de leur bloc) kit.stagger 2 images : pop puis
  kit.move vers Q_NUEE[k] (MORPH) ; lean_to(LEAN_POUSSE) (tête encore plus basse) + hold_low.

CONTRÔLE SANS SON (tour ciblé, 3/9 GOT) : S01-S02 pilule-calendrier x1,5 dans l'accroche, « Lundi » bat deux fois,
le bras fléchit (argent de y 900 à 960) avant de lâcher ; S03 chaque bloc naît avec son pictogramme, « Toi » heurte la
tour du CORPS (TOI_CHOC, traits d'impact, rejeté en arrière) ; S05 le bloc Budget aspire la petite marche, « Toi » ne la
touche pas (il sursautait le stylo tendu : « il repousse le petit pas ») ; noms écrits sur les mots, pictogrammes qui
battent ; S06 trois sauts stylo tendu vers l'argent, la pointe reste dessous (Toi.stretch) ; S07 la jauge pleine porte
un éclair (pictogramme bolt), reste au-dessus de lui (ENERGIE_GRAND_C) et bat à chaque saut ; S08 quatre coups sur la
tour entière (POUSSE_CONTACT, au milieu) : à chaque coup les quatre pictogrammes battent et la jauge, au-dessus de lui,
perd un quart ; vide, il s'affaisse et la jauge se range en haut à droite ; « ? » plus grands (56).

PASSAGE À p2 (ENTRY_P2, épinglé par p2 à l'image 899) : tout ce qui commence ici finit avant l'image 900. Fin exacte
attendue : pastille PASTILLE_TOUR[100] ; blocs tower(i, 100) fill PAPER, pictogrammes et noms écrits ; accolade draw 1
sy 1, gp_nom écrit en GP_NOM_C[100] ; q1-q8 scale 1 en Q_NUEE ; grand_q 0 ; energie value 0, fill RED ; energie_nom
opacité 1 ; calendrier « Lundi » (w cal_w, fill LIGHT) ; cadran 0 ; apercu 0 ; nom_toi en NOM_SOL. « Toi » en
TOI_RECUL (780, 1135), affaissé (lean LEAN_POUSSE), bras baissé.

REVUE 1 : S01 l'argent levé à bout de bras (640, 900), calendrier tombé au-dessus (CAL_HOOK_C) puis rangé sur « grand » ;
S02 la glissade finit sur « vidéo », il s'affaisse encore, l'argent bat sur « pourquoi » ; S03 il tend le stylo vers
l'argent qui monte, et c'est la pointe du stylo levé qui heurte la tour ; S05 la marche « 1 » est ravalée en 550 ms,
il tend le stylo dans le vide ; S06 deux sauts sur place, la pointe frappe Épargne puis Placements ; S07 bras tendu
gardé, jauge grande au-dessus de lui, puis rangée avec un trajet en tirets ; trois sauts h 60 ; S08 poussée penchée de
22°, pieds qui glissent de 10 px, traits d'impact, jauge rouge d'un coup ; les « ? » partent des pictogrammes (cyan à
la naissance). Pinces de fin : assert sur scene_f0(S, "S08") et scene_f0(S, "S09").
"""
from . import *  # noqa: F401,F403
from . import _toward
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, SCALE  # noqa: F401
from pipeline.story_kit import TAP


def part(S, kit, c):
    toi = c.toi
    blocs, icos, noms = c.blocs, c.bloc_ico, c.bloc_nom
    tower_ids = blocs + ["pastille"]

    # Image 0 = distribution (cast) : épingle de principe à -1 (identique au cast, aucun saut).
    kit.pin(0 - 1, {"pastille": {"pos": list(PASTILLE_SOL0), "scale": 1, "rot": 0},
                    "calendrier": {"scale": 0}, "apercu": {"scale": 0}, "cadran": {"scale": 0},
                    "energie": {"scale": 0}, "grand_q": {"scale": 0}, "accolade": {"draw": 0},
                    **{b: {"scale": 0} for b in blocs}})
    if S.val("toi", "scale", 0 - 1) == 0:        # garde-fou (toi est visible dès le cast : sans effet)
        toi.enter(0, at=list(TOI_P0))
    for b in blocs:                              # même couleur, en hex minuscule (contrat ENTRY_P2 : S.val compare
        S.key(b, "fill", 0, PAPER.lower())       # les chaînes telles quelles)
    S.key("calendrier", "fill", 0, LIGHT.lower())
    S.key("calendrier", "pos", 0, list(CAL_HOOK_C))   # accroche : la pilule tombe dans la colonne d'action

    def cal_to(f, key):
        """La pilule-calendrier bascule sur T_CAL[key] (sans image vide ni débordement) et bat x1,1."""
        cal_swap(S, kit, f, T_CAL[key])

    def beat_tower(f, peak, with_pastille=True):
        for b in (tower_ids if with_pastille else blocs):
            kit.pulse(b, f, peak=peak, step=3)

    def shake_tower(f, amp):
        for b in tower_ids:
            kit.shake(b, f, amp=amp, axis="x")

    # ================= S01 « Tu t’étais promis de reprendre ton argent en main ce week-end. » =================
    f = kit.at("S01", "promis", "« Toi » touche du stylo le bout droit de sa pastille cyan « Ton argent », posée au "
                                "sol : elle bat")
    t0 = f - TAP + 1
    toi.hold_low(0, t0)                          # image 0 lisible et immobile : bras baissé
    hit = toi.tap(t0, list(PASTILLE_TAP0))
    kit.pulse("pastille", hit, peak=1.1, step=3)
    f = kit.at("S01", "reprendre", "« Toi » lève la pastille à bout de bras, au-dessus de sa tête ; la pointe du stylo "
                                   "reste sur son bout droit")
    kit.move("pastille", f, list(PASTILLE_MAIN), arc=80)
    toi.reach(f, list(PASTILLE_MAIN_TIP), d=MOVE)
    f = kit.at("S01", "week-end.", "une pilule-calendrier « Week-end » tombe juste au-dessus de l'argent levé")
    drop_in(kit, "calendrier", f, h=100)
    S.key("calendrier", "scale", f, CAL_HOOK_K)  # contrôle sans son : « Week-end » / « Lundi » lisibles au téléphone

    # ================= S02 « Et lundi, tu as tout lâché ? » =================
    f = kit.at("S02", "lundi,", "la pilule-calendrier passe de « Week-end » à « Lundi » et bat")
    cal_swap(S, kit, f, T_CAL["lundi"], pulse=False)   # pilule à l'échelle CAL_HOOK_K : battement relatif
    kit.pulse("calendrier", f, peak=round(CAL_HOOK_K * 1.1, 3), step=3)
    kit.pulse("calendrier", f + 7, peak=round(CAL_HOOK_K * 1.1, 3), step=3)   # le lundi bat deux fois
    # contrôle sans son : dès « lundi », le bras fléchit et l'argent levé redescend (l'élan retombe) avant d'être lâché
    kit.move("pastille", f + 4, list(PASTILLE_FLECHIE), 14, "inOut")
    toi.reach(f + 4, list(PASTILLE_FLECHIE_TIP), 14)
    toi.lean_to(f + 4, -5, 14, "inOut")
    toi.tip_on(f + 18, f + 30, PASTILLE_FLECHIE_TIP)
    f = kit.at("S02", "lâché ?", "la pastille quitte la pointe du stylo, tombe au sol en tournant et glisse à "
                                 "gauche, entière ; « Toi » laisse retomber son bras et s'affaisse, tête basse")
    w_video = S.word_after("vidéo", f)           # revue 1 : la glissade s'achève sur « vidéo » (pas d'image figée)
    S.key("pastille", "pos", f, [PASTILLE_FLECHIE[0], PASTILLE_SOL0[1]], DROP + 2, "in")
    S.key("pastille", "rot", f, 8, DROP + 2, "in")
    g = f + DROP + 2
    S.key("pastille", "pos", g, list(PASTILLE_TOMBEE), w_video - g, "out")
    S.key("pastille", "rot", g, 0, w_video - g, "out")
    toi.lean_to(f, LEAN_AFFAISSE, d=POP)
    toi.lower(f, d=8)
    toi.hold_low(f + 8, f + POP + 1)
    # secondaire (sans temps fort) : « vidéo » il s'affaisse encore ; « pourquoi » l'argent tombé bat
    toi.lean_to(w_video, LEAN_POUSSE, d=SCALE, e="inOut")
    toi.hold_low(w_video, w_video + SCALE + 1)
    kit.pulse("pastille", S.word_after("pourquoi", w_video), peak=1.08, step=3)

    # ================= S03 « Dans cette vidéo, on va voir pourquoi le grand plan échoue. » =================
    f = kit.at("S03", "grand", "quatre blocs papier poussent du sol l'un sur l'autre sous la pastille et l'emportent "
                               "au sommet d'une tour ; « Toi » se redresse et tend le stylo vers elle, trop tard ; le "
                               "calendrier remonte à sa place")
    for i, b in enumerate(blocs):
        fi = f + 4 * i
        (cx, cy), w, h = tower(i, 100)
        S.key(b, "pos", fi - 1, [cx, GROUND - 100 * i])
        S.key(b, "h", fi - 1, 0)
        S.key(b, "scale", fi, 1)
        S.key(b, "pos", fi, [cx, cy], 5, "out")
        S.key(b, "h", fi, 100, 5, "out")
        S.key("pastille", "pos", fi, [PASTILLE_TOMBEE[0], GROUND - 100 * (i + 1) - PASTILLE_H / 2], 5, "out")
        kit.pop(icos[i], fi + 3, d=6)            # contrôle sans son : chaque bloc naît avec son pictogramme (pas de
        #                                          blocs vides pendant 7 s) ; les noms s'écrivent en S05
    kit.move("calendrier", f, list(CAL_C), MOVE, scale=CAL_K)
    toi.lean_to(f, 0, d=POP)
    toi.reach(f, list(_toward(TOI_P0, (588, 800), 255)), d=14, step=False)   # la main tend vers l'argent qui monte
    f = kit.at("S03", "plan", "une accolade se trace de bas en haut à gauche de la tour et « Grand plan » s'écrit à "
                              "côté")
    kit.draw("accolade", f, DRAW)
    kit.type("gp_nom", f, rate=2)
    f = kit.at("S03", "échoue.", "« Toi » fonce dans la tour et s'y cogne de tout le corps : traits d'impact, la tour "
                                 "et l'argent tremblent fort ; il est rejeté en arrière et revient à sa place")
    hit = toi.walk(f, list(TOI_CHOC), d=8, low=True)   # contrôle sans son : le CORPS heurte la face (x 620)
    shake_tower(hit, 9)
    marks(S, hit, [([TOWER_X + TOWER_W / 2 - 22, 1098], 35), ([TOWER_X + TOWER_W / 2 - 28, 1130], 0),
                   ([TOWER_X + TOWER_W / 2 - 22, 1162], -35)], hold=8)
    g = toi.hop(hit, list(TOI_P0), 11, h=24, lean=10)   # rejeté en arrière (lean > 0 : loin de la tour)
    toi.hold_low(hit, g)
    toi.lower(g, 8)

    # ================= S04 « Et comment avancer avec une seule décision à la fois. » =================
    f = kit.at("S04", "avancer", "« Toi » se penche vers la tour, bras baissé")
    toi.lean_to(f, LEAN_VERS, d=POP)
    toi.hold_low(f, f + POP + 1)
    f = kit.at("S04", "seule", "une petite marche « 1 » en tirets sort de derrière le bloc du bas et se pose au sol, "
                               "devant « Toi »")
    S.key("apercu", "pos", f - 1, list(APERCU_CACHE))
    S.key("apercu", "scale", f - 1, 1)
    kit.move("apercu", f, list(APERCU_C), d=MORPH, e="out")

    # ================= S05 « C’est le piège du grand plan… budget, épargne, placements, papiers. » =================
    f = kit.at("S05", "piège", "la tour ravale la petite marche « 1 » : elle glisse dans le bloc du bas ; « Toi » "
                               "tend le stylo vers elle et ne rattrape que du vide ; « Grand plan » bat, la tour "
                               "tremble")
    # contrôle sans son (S04 se lisait « il repousse la petite marche ») : le bloc Budget bat et ASPIRE la marche,
    # « Toi » ne la touche pas ; il sursaute en arrière, bras baissé
    kit.pulse("bloc1", f, peak=1.06, step=3)
    g = kit.move("apercu", f + 3, list(APERCU_CACHE), d=10, e="in")
    S.key("apercu", "scale", g, 0)
    kit.pulse("gp_nom", g, peak=1.15, step=3)
    shake_tower(g, 5)
    toi.lean_to(f + 3, 8, d=6)
    toi.lean_to(f + 9, 0, d=POP, e="inOut")
    toi.hold_low(f, f + 9 + POP + 1)
    f = kit.at("S05", "tout", "les quatre blocs battent ensemble, d'un seul coup ; l'argent au sommet aussi")
    beat_tower(f, 1.04)
    for i, mot in enumerate(["budget,", "épargne,", "placements,", "papiers."]):
        f = kit.at("S05", mot, f"le bloc {i + 1} reçoit son pictogramme et son nom : « {T_BLOCS[i]} »")
        kit.pulse(icos[i], f, peak=1.35, step=3)   # le pictogramme (né en S03) bat ; le nom s'écrit
        kit.type(noms[i], f, rate=2)

    # ================= S06 « Un week-end entier. Et le lundi, on abandonne, parce que c’était trop. » ==========
    f = kit.at("S06", "week-end", "« Toi » va au pied de la tour ; le calendrier repasse à « Week-end »")
    toi.walk(f, list(TOI_PIED_TOUR), d=14, low=True)
    cal_to(f, "weekend")
    f = kit.at("S06", "entier.", "une horloge sort du calendrier : son aiguille fait un tour complet et son secteur "
                                 "se remplit ; « Toi » saute deux fois contre la tour et la frappe du stylo : elle "
                                 "tremble à peine")
    kit.pop("cadran", f, from_pt=list(CAL_C))
    S.key("cadran", "value", f, 60, 30, "linear")
    # contrôle sans son : pendant le tour d'horloge, trois sauts, le stylo tendu vers l'argent : la pointe reste
    # sous la pastille, il ne l'atteint jamais (échec visible)
    hs = f
    for k in range(3):
        hs = toi.hop(hs, list(TOI_PIED_TOUR), 10, h=70, lean=0)
    toi.stretch(f, hs, SAUT_VISE, dist=SAUT_DIST, ramp=4)
    toi.lower(hs, 8)
    f = kit.at("S06", "lundi,", "le calendrier passe à « Lundi » ; l'horloge pleine reste")
    cal_to(f, "lundi")
    f = kit.at("S06", "abandonne,", "« Toi » repart à reculons à sa place et s'affaisse, tête basse, bras ballant")
    g = toi.walk(f, list(TOI_P0), d=16, low=True)
    toi.lean_to(g, LEAN_AFFAISSE, d=POP)
    toi.hold_low(g, g + POP + 1)
    f = kit.at("S06", "trop.", "la tour bat, lourde ; l'horloge pleine reste sous « Lundi »")
    beat_tower(f, 1.05)

    # ================= S07 « Pourquoi ça bloque ? Ce n’est pas un manque de volonté. » =================
    f = kit.at("S07", "Pourquoi", "l'horloge rentre dans le calendrier ; un grand « ? » paraît au-dessus de l'argent ; "
                                  "« Toi » se redresse")
    kit.vanish("cadran", f, into=list(CAL_C))
    kit.pop("grand_q", f)
    toi.lean_to(f, 0, d=POP)
    toi.hold_low(f, f + POP + 1)
    f = kit.at("S07", "bloque ?", "« Toi » fait un pas et tend le stylo droit vers l'argent de tout son bras : la "
                                  "pointe s'arrête bien en dessous ; il garde le bras tendu ; le « ? » bat")
    g = toi.walk(f, list(TOI_TEND), d=6)         # main au repos (stylo levé) : le geste part vers le haut
    g = toi.reach(g, list(TEND_TIP), d=12, step=False)
    kit.pulse("grand_q", g, peak=1.15, step=3)
    f = kit.at("S07", "manque", "une grande jauge pleine marquée d'un éclair (son énergie) sort de la tête de « Toi » "
                                "et reste au-dessus de lui")
    S.key("energie", "pos", f - 1, list(ENERGIE_SORTIE))
    g = kit.pop("energie", f, to=list(ENERGIE_GRAND_C), scale=ENERGIE_GRAND_K)
    f = kit.at("S07", "volonté.", "« Toi » saute trois fois sur place, haut, le stylo levé, plein d'envie ; la jauge "
                                  "pleine au-dessus de lui bat à chaque réception")
    # contrôle sans son : la jauge pleine (éclair) RESTE au-dessus de lui et bat à chaque réception : l'envie est là
    lands, h = [], f
    for k in range(3):
        h = toi.hop(h, list(TOI_TEND), 8, h=75, lean=0)
        lands.append(h)
        kit.pulse("energie", h, peak=round(ENERGIE_GRAND_K * 1.08, 3), step=2)
    assert lands[-1] <= scene_f0(S, "S08") + 2, "p1 : S07 déborde sur S08"

    # ================= S08 « Tout réorganiser d’un coup demande trop d’énergie et trop de décisions. » ==========
    f = kit.at("S08", "Tout", "le grand « ? » se réduit sur place ; les quatre blocs battent ensemble")
    kit.vanish("grand_q", f)
    beat_tower(f, 1.04)
    toi.lower(f, 8)
    f = kit.at("S08", "demande", "« Toi » s'avance et pousse la tour de tout son poids, penché, les pieds qui "
                                 "glissent en arrière : trois traits d'impact au contact ; la tour ne bouge pas")
    g = toi.walk(f, list(TOI_POUSSE), d=8, low=True)
    toi.lean_to(g, LEAN_PRESSE, d=POP)
    toi.hop(g, list(TOI_RECUL), POP, h=0, lean=0)   # les pieds glissent de 10 px en arrière pendant la poussée
    contact = list(POUSSE_CONTACT)               # contrôle sans son : au milieu de la tour (joint Épargne / Placements)
    hit = toi.reach(g, contact, d=POP) - 1
    f = kit.at("S08", "d’énergie", "il pousse quatre fois la tour entière : à chaque coup, les quatre chantiers battent "
                                   "ensemble, la tour tremble à peine, et la jauge rouge au-dessus de lui perd un quart ; "
                                   "vide, il lâche et s'affaisse ; la jauge vide se range en haut à droite")
    S.key("energie", "fill", f, RED)             # rouge d'un coup, sur l'image du mot : jamais de gris violacé
    for k in range(4):                           # un coup = un quart d'énergie perdu
        fk = f + POUSSE_PAS * k
        S.key("toi", "lean", fk, LEAN_PRESSE - 6, 3, "out")
        S.key("toi", "lean", fk + 3, LEAN_PRESSE, 4, "inOut")
        shake_tower(fk + 2, 3)
        for ic in icos:
            kit.pulse(ic, fk + 2, peak=1.3, step=2)
        marks(S, fk + 2, [([contact[0] - 26, contact[1] - 32], 35), ([contact[0] - 32, contact[1]], 0),
                          ([contact[0] - 26, contact[1] + 32], -35)], hold=2)
        S.key("energie", "value", fk + 2, round(0.75 - 0.25 * k, 2), 4, "out")
    toi.tip_on(hit + 1, f + 4 * POUSSE_PAS, contact)   # la pointe reste sur la tour pendant les coups (APRÈS les clés lean)
    g = f + 4 * POUSSE_PAS
    toi.lean_to(g, LEAN_AFFAISSE, d=POP)
    toi.lower(g, 8)
    toi.hold_low(g + 8, g + POP + 1)
    arr = kit.move("energie", g + 2, list(ENERGIE_C), MORPH, "inOut", scale=1)   # la jauge vide se range
    S.key("energie_trace", "draw", g + 2, 1)
    S.key("energie_trace", "opacity", arr - 2, 0, FADE, "linear")
    kit.fade("energie_nom", arr - 2, frm=0)
    f = kit.at("S08", "décisions.", "chaque bloc lance ses deux « ? » depuis son pictogramme, qui bat : huit « ? » "
                                    "cyan à la naissance, qui s'agglutinent au-dessus de la tête de « Toi », qui "
                                    "baisse encore la tête")
    for i in range(4):
        fi = f + 4 * i
        kit.pulse(icos[i], fi, peak=1.35, step=3)
        src = S.to_world(icos[i], [0, 0], fi)
        for j in range(2):
            k = 2 * i + j
            q = c.q[k]
            kit.ensure(q, "color", INK)
            S.key(q, "color", fi - 1, CYAN)
            S.key(q, "color", fi + MORPH, INK, 4, "out")
            kit.pop(q, fi + j, from_pt=src, to=list(Q_NUEE[k]), d=MORPH)
    toi.lean_to(f, LEAN_POUSSE, d=POP)
    toi.hold_low(f, f + POP + 1)
    assert f + 4 * 3 + 1 + MORPH + 4 <= scene_f0(S, "S09"), "p1 : la nuée de « ? » finit après la fin de S08"
