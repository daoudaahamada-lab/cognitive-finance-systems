"""V01, partie 1 : S01-S07, images 0-889 (0,000 -> 29,651 s). 29 temps forts.

Entrée (image 0, pas d'épingle : c'est l'état de cast) : fond ivoire ; horloge WTH-003-01 (540, 500), 400 px ; pile
nette des 4 documents (doc1 dessus, décalés de 6 px, centre (540, 1020)) ; pastille « Client · 9 h » sous le pied de
l'horloge (540, 745). Ni personnage, ni barre, ni repère.

Sortie (image 889) = ENTRY_P2 (etat_initial de S08) : horloge-badge (830, 300) x 0,5 ; repère posé (disque 1 actif,
on = 1) et ses 3 légendes écrites ; barre2 vide (contour seul, value 0) ; blocs, barre, conseil, avance à 0 ; doc1-4
aux places DOC_S07 (rot 0), bandeau et date visibles ; info1-4 sur le coin de leur carte ; pastille (540, 865) ; rond
vide (540, 935) ; IA rangée (60, 1200) x 0,42 avec sa pilule ; conseiller au sol (540, 1135) (non épinglé : p2 le
replace par walk / enter).

Brief, scène par scène (ids de la distribution entre crochets ; places : constantes de __init__) :
- S01 « 9 » : un seul geste. [pastille] tombe de PASTILLE_S01 à PASTILLE_PILE (kit.drop, 370 ms) et bat une fois
  (x 1,15). Pile et horloge immobiles.
- S02 « Et » : [horloge] glisse et se réduit en badge (CLOCK_BADGE, x 0,5) ; [barre] (3 blocs) s'étire de son pied vers
  la gauche (piste w 0 -> 580 depuis le bord droit, ou pop) ; [toi] entre en marchant depuis x 930 jusqu'à ADV_S02
  (toi.enter(f, at=ADV_S02, frm=930)). « tu » : [toi_pill] surgit au-dessus de sa tête. « fouilles » : toi.tap sur le
  coin bas droit de la pile (≈ (635, 1135)) ; au contact, doc1-4 glissent vers DOC_SPREAD (x, y, rot ; décalés de
  2 images) ; la pastille reste seule à (540, 865). « dossier » : bond (toi.hop / walk + place_for) à côté de doc3,
  pointe sur son bord droit ; au contact, [bloc1] se détache de la barre (la barre perd un segment : value 1 -> 2/3)
  et vole en arc dans doc3 en s'y réduisant, CYAN. « préparer » : idem doc2, [bloc2] ; il reste un bloc contre
  l'horloge. « conseil » : [conseil] surgit du pied de l'horloge et se pose sous le badge (CONSEIL_S02), vide ; le
  conseiller ne se tourne pas vers elle.
- S03 « Dans » : [avance] (▶▶) surgit en AVANCE_AT et y reste jusqu'à S05 ; le conseiller redescend au repos
  (ADV_REST), sa pilule avec lui. « l’IA » : [ia] surgit en IA_S03 (x 0,8), [ia_pill] dessous. « prépare » :
  [faisceau1-4] (pointillés, pb = chaque document) se tracent ; les documents se redressent et s'empilent un à un en
  PILE_S03 (décalés de 3 images) ; la pastille se clipse sur la pile (PASTILLE_S03) ; les faisceaux s'éteignent
  (piste from). « rendez-vous » : bloc1 et bloc2 ressortent de la pile, cyan, et remontent à leur place (arc 60) : la
  barre est pleine (value 1). « contrôle » : un pas vers (720, 1135), toi.tap sur PILE_TICK_S03 : [coche_pile] se trace
  au contact (coche pleine deep, 60 px).
- S04 « Trois » : morph : bloc1-3 montent à y 300 et s'arrondissent en disques de 40 px (pistes w, h, r ; x MARKER_XS,
  décalés de 2 images) ; [barre] s'efface en fil (relais par [marqueur], scale 0 -> 1, on = 0 : 3 disques inactifs) ;
  toi_pill et ia_pill s'effacent (fondu). « limiter » : marqueur on 0 -> 1 sur l'étape 0 (S.key "on") ; [legende1]
  s'écrit (kit.type, 1 caractère / image) et se souligne (under). « exiger » : kit.step(f, 1) ; [legende2] s'écrit ;
  legende1 reste à l'encre. « relire » : kit.step(f, 2) ; [legende3] ; 15 images plus tard, le disque actif revient sur
  le 1 (kit.step(f + 15, 0)). Les soulignements suivent l'étape active. Rien d'autre ne bouge.
- S05 « Le » : [avance] pivote de 180° (▶▶ -> ◀◀, rot 0 -> 180, 300 ms) ; en 550 ms tout repart à reculons :
  coche_pile s'efface (draw 1 -> 0), [ia] glisse et se réduit en IA_CORNER x 0,42 (toujours visible, pilule rendue
  à 1 et posée à sa droite), les documents repartent vers DOC_SPREAD avec leurs traits de vitesse
  ([docN_vitesse] : groupe à orienter à l'opposé du trajet, pop puis vanish), la pastille revient en PASTILLE_PILE,
  le conseiller recule en ADV_REST ; [barre2] (5 blocs) s'étire du pied de l'horloge ; puis [avance] se réduit.
  Les blocs 1-3 devenus disques restent le repère (aucun bloc ne revient). « conseil » : [conseil] descend devant le
  conseiller (760, 1000) ; toi.tap : [conseil_coche] se trace au contact et la pilule passe en cyan clair (fill PAPER
  -> LIGHT, hex) ; 10 images plus tard elle glisse contre sa poitrine et y rentre (kit.vanish(into=toi), même geste
  que le tampon en S16-S17). « recherche » : bond à côté de doc1, pointe sur son bord droit ; [bloc4] quitte barre2
  (value 1 -> 4/5) et entre dans doc1, cyan.
- S06 « bilan » : la pointe touche le pictogramme de doc1 ; [info1] (enfant de doc1) en sort et se pose sur le coin
  (INFO_CORNER). « contrats » / « décisions » / « promesses » : bond à côté de doc2 / doc3 / doc4, pointe sur le bord,
  [info2-4] sortent, et [bloc5-7] partent de barre2 dans chaque document (value 3/5, 2/5, 1/5). « événements » : bond
  dans le blanc entre doc1 et doc2 (≈ (560, 640), toi.place_for), la pointe touche l'ivoire : [rond] naît sous la
  pointe (pop), tremble (kit.shake x, 6), reste vide ; aucun bloc ne part ; 12 images plus tard il glisse en ROND_S06
  sous la pastille et s'y accroche ; la pastille bat (x 1,2) : ce qui manque concerne le client.
- S07 « dispersé » : doc1-4 glissent vers DOC_S07 (rot 0, avec leur info) ; le rond reste sous la pastille ; le
  conseiller retombe au sol en ADV_S07 (hop 8 images). « CRM » : sur doc2, [doc2_bandeau] tombe (opacity 1 + drop
  local) et [doc2_date] s'inscrit (fondu) ; la carte bat (x 1,1). « mails » : doc3. « PDF » : doc1. « notes » : doc4 ;
  [bloc8] (le dernier) part de barre2 en arc dans la carte Notes : barre2 n'est plus qu'un contour vide (value 0).

Raccord vers p2 : tout ce qui est commencé finit avant l'image 890 ; état final = ENTRY_P2 exactement (kit.pin de p2
signale tout écart).
Mise en scène précédente à recycler (même rig, autres mots) : git show 6962c86:wth-videos/scripts/story/V01/p1.py
(sauts du conseiller S04, rembobinage S03, cadre S05).

Mise en œuvre (écarts au brief) : le conseiller entre depuis x 880 (et non 930 : sa base de ± 59 px mordait sur la
colonne réservée x > 940) en 8 images, arrivé sur « fouilles » ; les gestes « bond + pointe » partent sur le mot et
touchent 10 à 13 images plus tard (contacts sur le mot quand il est déjà en place : « bilan ») ; places du conseiller
(P_DOC1-4, P_BLANC) à côté des cartes, à mi-hauteur pour doc1 / doc2 (hors d'atteinte depuis le sol) ; en S03
« contrôle » il va en (760, 1135) (à 720, la pile était trop près de l'épaule pour le stylo) ; la pilule « Conseil » est
cochée en (650, 940), au-dessus de doc4 ; au retour du repère sur le 1 (S04, image 426-440) les soulignements sont tous
effacés : p2 souligne « Limiter » sur « Pourquoi » ; S07 : bandeaux de 64 px (piste h) qui couvrent le pictogramme.
"""
import math

from pipeline.story import FADE, MORPH, MOVE, POP, STRETCH

from . import (ADV_REST, ADV_S02, ADV_S07, BAR_C, BAR_H, BAR_W, BAR_X0, BAR_Y, CLOCK_BADGE, CLOCK_BADGE_S, CLOCK_S01,
               DOC_S07, DOC_SPREAD, ENTRY_P2, IA_CORNER, IA_CORNER_S, IA_S03_S, IA_W, INFO_CORNER, LIGHT, MARKER_XS,
               MARKER_Y, PAPER, PASTILLE_PILE, PASTILLE_S01, PASTILLE_S03, PILE_S01, PILE_S03, PILE_STEP,
               PILE_TICK_S03, ROND_S06, LEGEND_Y, MARKER_CX, block_c, seam, vanish)

DOCS_ = ["doc1", "doc2", "doc3", "doc4"]
BAR_RIGHT = BAR_X0 + BAR_W                       # 720 : pied gauche du badge-horloge, d'où sortent les barres
CLOCK_FOOT = (CLOCK_BADGE[0], 386)               # bas du badge (horloge 342 px de haut x 0,5, centre y 300)
ENTER_X = 880                                    # entrée par la droite : la figurine (± 59 px à la base) reste sous
#                                                  x 940 ; ADV_ENTER_X = 930 débordait sur la colonne réservée x > 940
# places du conseiller (centre de la figurine, échelle 1) : à côté de la carte fouillée, jamais dessus
P_DOC3 = [470, 1135]                             # au sol entre doc3 et doc4 : pointe sur le bord droit de doc3
P_DOC2 = [840, 1010]                             # sous doc2 (pilule « Toi » sous son bord bas) : pointe sur son bas
P_DOC4 = list(ADV_REST)                          # au sol à droite de doc4 : pointe sur son bord droit
P_DOC1 = [495, 720]                              # à droite de doc1, entre la carte et la pastille
P_BLANC = [620, 730]                             # dans le blanc entre doc1 et doc2
P_S03 = [760, 1135]                              # S03 « contrôle » : un pas vers la pile
CONSEIL_TAP = (650, 940)                         # S05 : la pilule « Conseil » devant lui, au-dessus de doc4
TOUCH = {"doc1": [100, 0], "doc2": [-60, 125], "doc3": [100, -10], "doc4": [100, 0]}   # bord touché (repère carte)
PICTO = [-56, -80]                               # pictogramme de la carte (pastille r 22 en (-64, -85))
BLANC_PT = [545, 625]                            # la pointe touche l'ivoire : naissance du rond vide
IA_PILL_RIGHT = [round((IA_W / 2 * IA_CORNER_S + 50) / IA_CORNER_S, 1), 0]   # pilule « IA » 10 px à droite de la tête
IA_PILL_K = round(1 / IA_CORNER_S, 4)            # pilule à l'échelle monde 1 (texte 32 px) contre l'IA x 0,42
BLOCK_IN = [0, 20]                               # le bloc entre au milieu de la carte
BANNER_H2 = 64                                   # S07 : bandeau de 64 px (au lieu de 48) : il couvre tout le
BANNER_Y2 = -125 + BANNER_H2 / 2                 # pictogramme (r 20 en y -85), qui dépassait en demi-lune dessous
# S04 : le repère naît en grand au centre (x 1,5, centre (540, 640)) : les 3 étapes, idée principale, se lisent en
# légendes de 48 px ; après « relire », il se range à sa place de badge (x 1, y 300) en 12 images
MK_C, MK_S = (540, 640), 1.5
MK_XS = [round(MK_C[0] + (x - MARKER_CX) * MK_S, 1) for x in MARKER_XS]
MK_LEG_Y = round(MK_C[1] + (LEGEND_Y - MARKER_Y) * MK_S, 1)
AVANCE_S04 = (540, 540)                          # le ▶▶ remonte de 20 px : le disque actif agrandi passe dessous


def _pt(p):
    return [round(p[0], 2), round(p[1], 2)]


def _pile(c, i):
    return [c[0] + PILE_STEP * (i - 1.5), c[1] + PILE_STEP * (i - 1.5)]


def _check_entry_p2(S, kit, n):
    """Raccord : l'état à l'image n doit être exactement ENTRY_P2 (sinon : avertissement)."""
    for id, tracks in ENTRY_P2.items():
        for track, v in tracks.items():
            cur = S.val(id, track, n, None if track == "pos" else 0)
            if isinstance(v, (list, tuple)):
                bad = cur is None or max(abs(a - b) for a, b in zip(cur, v)) > 0.5
            else:
                bad = abs((cur or 0) - v) > 1e-3
            if bad:
                kit.warn(f"raccord p1 -> p2 : {id}.{track} vaut {cur} à l'image {n}, ENTRY_P2 attend {v}")


def part(S, kit, c):
    toi = c.toi

    def block_fly(b, f, doc, gauge, value, d=11):
        """Le bloc b se détache de la jauge (value instantanée), vole en arc et entre dans `doc`, cyan, en s'y
        réduisant. Renvoie l'image où il a disparu."""
        S.key(gauge, "value", f, round(value, 4))              # le segment quitte la barre au contact (image f)
        S.key(b, "scale", f, 1)                                 # et le bloc, identique, prend sa place
        S.key(b, "opacity", f, 1)
        kit.ensure(b, "z", 5.6)
        S.key(b, "z", f, 12.6)
        f1, arr = f + 1, f + 1 + d                              # puis il vole
        land = S.to_world(doc, BLOCK_IN, arr)
        S.key(b, "pos", f1, _pt(land), d, "inOut", arc=90)
        S.key(b, "rot", f1, S.val(doc, "rot", arr), d, "out")
        S.key(b, "scale", f1, 0.35, d, "in")
        return vanish(kit, b, arr, d=3)

    def info_out(i, f):
        """Pastille d'information i : sort du pictogramme de sa carte et se pose sur son coin."""
        d = DOCS_[i]
        kit.pop(f"info{i + 1}", f, from_pt=S.to_world(d, PICTO, f - 1), to=INFO_CORNER, d=12)

    def touch(doc, f):
        return _pt(S.to_world(doc, TOUCH[doc], f))

    # État d'entrée = distribution (image 0) : l'épingle ne fait que le redire.
    kit.pin(-1, {"horloge": {"pos": list(CLOCK_S01), "scale": 1}, "pastille": {"pos": list(PASTILLE_S01), "scale": 1},
                 **{d: {"pos": _pile(PILE_S01, i), "rot": 0, "scale": 1} for i, d in enumerate(DOCS_)}})

    # ============================== S01 « Client à 9 heures ? » ==============================
    f = kit.at("S01", "9", "la pastille « Client · 9 h » quitte le pied de l'horloge, tombe sur la pile de 4 documents "
                           "et la coiffe (540, 865), puis bat une fois ; pile et horloge immobiles")
    g = kit.drop("pastille", f, h=PASTILLE_PILE[1] - PASTILLE_S01[1], to=PASTILLE_PILE)
    S.key("pastille", "scale", g, 1.15, 3, "out")
    S.key("pastille", "scale", g + 3, 1, 6, "inOut")

    # ============================== S02 « Et tu fouilles encore son dossier… » ==============================
    f = kit.at("S02", "Et", "l'horloge se range en badge en haut à droite ; de son pied, la barre de temps (3 blocs "
                            "cyan) s'étire vers la gauche ; le conseiller entre par la droite en marchant")
    kit.move("horloge", f, CLOCK_BADGE, d=MORPH, e="inOut", scale=CLOCK_BADGE_S)
    gb = f + 5                                                   # la barre sort quand le badge arrive
    S.key("barre", "pos", gb - 1, [BAR_RIGHT, BAR_Y])
    S.key("barre", "w", gb - 1, 0)
    S.key("barre", "scale", gb, 1)
    S.key("barre", "w", gb, BAR_W, STRETCH, "out")
    S.key("barre", "pos", gb, list(BAR_C), STRETCH, "out")
    toi.enter(f, at=ADV_S02, frm=ENTER_X, d=8)                   # en marchant, arrivé sur « fouilles »

    f = kit.at("S02", "tu", "la pilule « Toi » surgit au-dessus de la tête du conseiller et le suit")
    kit.pop("toi_pill", f)

    f = kit.at("S02", "fouilles", "son stylo tape le coin bas droit de la pile : au contact, les 4 documents s'étalent "
                                  "vers 4 places éloignées ; la pastille reste seule au centre")
    hit = toi.tap(f, [635, 1135], d=6)
    for i, d in enumerate(DOCS_):
        x, y, r = DOC_SPREAD[i]
        S.keys(d, hit + 1 + 2 * i, MOVE, "inOut", pos=[x, y], rot=r)

    f = kit.at("S02", "dossier", "il bondit entre doc3 et doc4, sa pointe touche le bord droit de doc3 : le bloc gauche "
                                 "de la barre se détache, vole en arc et entre dans doc3, cyan")
    g = toi.hop(f, P_DOC3, 8, h=40)
    hit = toi.tap(g, touch("doc3", g), d=6)
    block_fly("bloc1", hit, "doc3", "barre", 2 / 3)

    f = kit.at("S02", "préparer", "il bondit sous doc2, sa pointe touche son bord bas : le 2e bloc vole et entre dans "
                                  "doc2 ; il ne reste qu'un bloc cyan contre l'horloge")
    g = toi.hop(f, P_DOC2, 8, h=30)
    hit = toi.tap(g, touch("doc2", g), d=5)
    block_fly("bloc2", hit, "doc2", "barre", 1 / 3, d=9)

    f = kit.at("S02", "conseil", "une pilule « Conseil » vide sort du pied du badge-horloge et se pose dessous ; le "
                                 "conseiller, penché sur doc2, ne se tourne pas vers elle")
    kit.pop("conseil", f, from_pt=list(CLOCK_FOOT))

    # ============================== S03 « Dans cette vidéo… » ==============================
    f = kit.at("S03", "Dans", "un « ▶▶ » surgit au-dessus des papiers et y reste ; le conseiller redescend à sa place "
                              "de repos, sa pilule « Toi » avec lui")
    kit.pop("avance", f)
    toi.hop(f, list(ADV_REST), 12, h=0)

    f = kit.at("S03", "l’IA", "l'IA (tête de verre) surgit dans la marge gauche, sa pilule « IA » dessous")
    kit.pop("ia", f, scale=IA_S03_S)

    f = kit.at("S03", "prépare", "4 faisceaux pointillés gris partent de la tête de l'IA vers les documents ; ils se "
                                 "redressent et s'empilent un à un au centre ; la pastille se clipse sur la pile ; les "
                                 "faisceaux s'éteignent")
    for i, d in enumerate(DOCS_):
        w = f"faisceau{i + 1}"
        S.key(w, "pb", f - 1, _pt(S.val(d, "pos", f - 1)))
        kit.draw(w, f, 8)
    for k, i in enumerate([3, 2, 1, 0]):                         # du dessous (doc4) au dessus (doc1)
        d, w, g = DOCS_[i], f"faisceau{i + 1}", f + 4 + 2 * k
        S.keys(d, g, 12, "inOut", pos=_pile(PILE_S03, i), rot=0)
        S.key(w, "pb", g, _pile(PILE_S03, i), 12, "inOut")
    kit.move("pastille", f + 8, PASTILLE_S03, d=10, e="out")
    off = f + 17
    for i in range(4):                                           # éteints, puis remis à zéro (p2 les retrace)
        w = f"faisceau{i + 1}"
        S.key(w, "from", off, 1, 6, "inOut")
        S.key(w, "draw", off + 7, 0)
        S.key(w, "from", off + 8, 0)

    f = kit.at("S03", "rendez-vous", "les 2 blocs ressortent de la pile, cyan, et remontent à leur place dans la "
                                     "barre : elle est pleine")
    for k, (b, slot, val) in enumerate((("bloc2", 1, 2 / 3), ("bloc1", 0, 1.0))):
        g = f + 2 * k
        kit.ensure(b, "z", 5.6)
        S.key(b, "z", g - 1, 12.6)
        S.key(b, "rot", g - 1, 0)
        S.key(b, "opacity", g - 1, 1)
        S.key(b, "pos", g - 1, _pt(PILE_S03))
        S.key(b, "scale", g, 1, POP, "out")
        S.key(b, "pos", g, block_c(slot, 3), MOVE, "inOut", arc=60)
        arr = g + MOVE
        S.key("barre", "value", arr, round(val, 4))
        S.key(b, "scale", arr, 0)
        S.key(b, "z", arr, 5.6)

    f = kit.at("S03", "contrôle", "le conseiller fait un pas vers la pile ; son stylo tape son coin bas droit : une "
                                  "coche pleine cyan profond s'y trace")
    toi.walk(f, P_S03, d=8)
    hit = toi.tap(f + 2, list(PILE_TICK_S03), d=8)
    kit.draw("coche_pile", hit, 6)
    toi.rest(hit + 8, d=8)

    # ============================== S04 « Trois étapes : limiter, exiger, relire. » ==============================
    f = kit.at("S04", "Trois", "les 3 blocs de la barre montent et s'arrondissent en 3 disques ; la barre s'amincit en "
                               "un fil : le repère 1-2-3 ; les pilules « IA » et « Toi » s'effacent")
    for k in range(3):
        b = f"bloc{k + 1}"
        S.key(b, "pos", f - 1, block_c(k, 3))
        S.key(b, "scale", f - 1, 1)
        S.key(b, "opacity", f - 1, 1)
        S.key(b, "rot", f - 1, 0)
        kit.ensure(b, "z", 5.6)
        S.key(b, "z", f - 1, 5.6)
    S.key("barre", "value", f, 0)
    dk = round(40 * MK_S)
    for k in range(3):
        b, g = f"bloc{k + 1}", f + 2 * k
        S.key(b, "pos", g, [MK_XS[k], MK_C[1]], MORPH, "inOut")
        S.keys(b, g, MORPH, "inOut", w=dk, h=dk, r=dk / 2)
        S.key(b, "fill", g, PAPER, MORPH, "inOut")
    kit.ensure("barre", "h", BAR_H)
    S.key("barre", "pos", f, list(MK_C), MORPH + 4, "inOut")
    S.keys("barre", f, MORPH + 4, "inOut", w=MK_XS[2] - MK_XS[0], h=round(4 * MK_S, 1))
    kit.move("avance", f + 4, AVANCE_S04, d=10)
    relay = f + 4 + MORPH                                        # le repère prend le relais des disques, en grand
    S.key("marqueur", "pos", relay - 1, list(MK_C))
    S.key("marqueur", "scale", relay - 1, 0)
    S.key("marqueur", "scale", relay, MK_S)
    for k in range(3):                                           # légendes sous les disques agrandis, 48 px
        S.keys(f"legende{k + 1}", relay - 1, pos=[MK_XS[k], MK_LEG_Y], scale=MK_S)
    for k in range(3):
        S.key(f"bloc{k + 1}", "scale", relay, 0)
    S.key("barre", "scale", relay, 0)
    for p in ("toi_pill", "ia_pill"):
        kit.fade(p, f, 0)
    S.key("toi_pill", "scale", f + FADE, 0)

    f = kit.at("S04", "limiter", "le disque 1 grandit et devient cyan ; « Limiter » s'écrit dessous et se souligne")
    S.key("marqueur", "on", f, 1, 10, "out")
    g = kit.type("legende1", f, rate=1)
    kit.draw("legende1", g, 6, track="under")

    f = kit.at("S04", "exiger", "le disque actif glisse sur le 2 ; « Exiger » s'écrit et se souligne ; « Limiter » reste "
                                "lisible, à l'encre")
    kit.step(f, 1)
    S.key("legende1", "under", f, 0, 6, "inOut")
    g = kit.type("legende2", f, rate=1)
    kit.draw("legende2", g, 6, track="under")

    f = kit.at("S04", "relire", "le disque actif glisse sur le 3 ; « Relire » s'écrit ; puis le disque actif revient sur "
                                "le 1 et y reste")
    kit.step(f, 2, d=12)
    S.key("legende2", "under", f, 0, 6, "inOut")
    g = kit.type("legende3", f, rate=1)
    kit.draw("legende3", g, 6, track="under")
    back = f + 14
    kit.step(back, 0, d=14)                                      # arrivé sur le 1 à l'image 440 (« Le »)
    S.key("legende3", "under", back, 0, 6, "inOut")
    S.keys("marqueur", back, 12, "inOut", pos=[MARKER_CX, MARKER_Y], scale=1)   # il se range en badge
    for k in range(3):
        S.keys(f"legende{k + 1}", back, 12, "inOut", pos=[MARKER_XS[k], LEGEND_Y], scale=1)

    # ============================== S05 « Le vrai problème… C'est la recherche. » ==============================
    f = kit.at("S05", "Le", "le « ▶▶ » pivote en « ◀◀ » ; tout repart à reculons : la coche s'efface, l'IA se range "
                            "petite dans le coin bas gauche, les documents filent (traits de vitesse) vers leurs places "
                            "éparpillées, la pastille revient au centre, le conseiller recule ; une barre pleine de 5 "
                            "blocs sort du pied de l'horloge")
    S.key("avance", "rot", f, 180, POP, "inOut")
    r0 = f + 6
    S.key("coche_pile", "draw", r0, 0, 10, "inOut")
    kit.move("ia", r0, IA_CORNER, d=MOVE, scale=IA_CORNER_S)
    for i, d in enumerate(DOCS_):
        x, y, rot = DOC_SPREAD[i]
        x0, y0 = S.val(d, "pos", r0 - 1)
        S.keys(d, r0, MOVE, "inOut", pos=[x, y], rot=rot)
        trail = math.degrees(math.atan2(y0 - y, x0 - x))         # traits derrière la carte, à l'opposé du trajet
        v = f"{d}_vitesse"
        S.key(v, "rot", r0 - 1, round(trail - rot, 2))
        for j in range(3):                                       # sous toutes les cartes : jamais sur une voisine
            kit.ensure(f"{v}{j + 1}", "z", S.ents[f"{v}{j + 1}"]["z"])
            S.key(f"{v}{j + 1}", "z", r0 - 1, 11.0)
        kit.pop(v, r0 + 3, d=3)                                  # une fois les cartes décollées de la pile
        vanish(kit, v, r0 + 11, d=5)
    kit.move("pastille", r0, PASTILLE_PILE, d=MOVE)
    toi.hop(r0, list(ADV_REST), MOVE, h=0, lean=-4)
    gb = r0 + 6
    S.key("barre2", "pos", gb - 1, [BAR_RIGHT, BAR_Y])
    S.key("barre2", "w", gb - 1, 0)
    S.key("barre2", "scale", gb, 1)
    S.key("barre2", "w", gb, BAR_W, STRETCH, "out")
    S.key("barre2", "pos", gb, list(BAR_C), STRETCH, "out")
    done = r0 + MOVE
    vanish(kit, "avance", done, d=POP)
    S.key("ia_pill", "pos", done - 1, IA_PILL_RIGHT)
    S.key("ia_pill", "scale", done - 1, IA_PILL_K)
    kit.fade("ia_pill", done, 1)

    f = kit.at("S05", "conseil", "la pilule « Conseil » descend devant le conseiller ; son stylo y trace une coche "
                                 "pleine et elle se remplit de cyan clair ; puis elle rentre dans sa poitrine")
    g = kit.move("conseil", f, CONSEIL_TAP, d=10)
    tick = S.to_world("conseil_coche", [0, 0], g)
    hit = toi.tap(g - 5, _pt(tick), d=6)
    kit.draw("conseil_coche", hit, 6)
    S.key("conseil", "fill", hit, LIGHT, 9, "out")
    chest = S.to_world("toi", [0, -15], hit + 10)
    vanish(kit, "conseil", hit + 10, into=_pt(chest), d=POP)
    toi.rest(hit + 4, d=8)

    f = kit.at("S05", "recherche", "il bondit à côté de doc1, sa pointe touche son bord droit : le bloc gauche de la "
                                   "nouvelle barre vole et entre dans doc1, cyan")
    g = toi.hop(f, P_DOC1, 8, h=40)
    hit = toi.tap(g, touch("doc1", g), d=6)
    block_fly("bloc4", hit, "doc1", "barre2", 4 / 5)

    # ============================== S06 « Dernier bilan, contrats… événements de vie. » ==============================
    f = kit.at("S06", "bilan", "la pointe touche le pictogramme de doc1 : il en sort en pastille d'information, qui se "
                               "pose sur son coin")
    hit = toi.tap(f - 5, _pt(S.to_world("doc1", PICTO, f)), d=6)
    info_out(0, hit)
    toi.rest(hit + 6, d=8)

    for k, (word, doc, place, what) in enumerate((
            ("contrats", "doc2", P_DOC2, "bond sous doc2, pointe sur son bord : la pastille bouclier sort du "
                                         "pictogramme et se pose sur son coin ; un bloc de la barre entre dans doc2"),
            ("décisions", "doc3", P_DOC3, "bond à côté de doc3, pointe sur son bord : la pastille coche se pose sur "
                                          "son coin ; un bloc entre dans doc3"),
            ("promesses", "doc4", P_DOC4, "bond à côté de doc4 : la pastille calendrier se pose sur son coin ; un "
                                          "bloc entre dans doc4 ; il ne reste qu'un bloc contre l'horloge"))):
        f = kit.at("S06", word, what)
        g = toi.hop(f, place, 8, h=40)
        hit = toi.tap(g, touch(doc, g), d=5)
        i = DOCS_.index(doc)
        info_out(i, hit)
        block_fly(f"bloc{5 + k}", hit, doc, "barre2", (3 - k) / 5)

    f = kit.at("S06", "événements", "bond dans le blanc entre les documents ; la pointe touche l'ivoire : un rond vide "
                                    "naît, tremble et reste vide ; aucun bloc ne part ; puis il glisse sous la pastille "
                                    "du client et s'y accroche ; la pastille bat")
    g = toi.hop(f, P_BLANC, 8, h=40)
    hit = toi.tap(g, BLANC_PT, d=5)
    S.key("rond", "pos", hit - 1, list(BLANC_PT))
    g = kit.pop("rond", hit)
    g = kit.shake("rond", g, amp=6, axis="x")
    toi.rest(hit + 6, d=8)
    g = kit.move("rond", g + 4, ROND_S06, d=14)
    kit.pulse("pastille", g, peak=1.2, step=3)

    # ============================== S07 « Tout est dispersé entre le CRM, les mails… » ==============================
    f = kit.at("S07", "dispersé", "les 4 documents s'écartent vers 4 places, chacun avec sa pastille d'information ; le "
                                  "rond vide reste sous la pastille ; le conseiller retombe au sol au centre")
    for i, d in enumerate(DOCS_):
        S.keys(d, f + 2 * i, MOVE, "inOut", pos=list(DOC_S07[i]), rot=0)
    toi.hop(f, list(ADV_S07), 8, h=20)

    words = [("CRM", "doc2", "un bandeau « CRM » tombe sur le haut de doc2 et « déc. 2025 » s'inscrit en bas ; la "
                             "carte bat"),
             ("mails", "doc3", "bandeau « Mail » sur doc3 et « sept. 2025 » ; la carte bat"),
             ("PDF", "doc1", "bandeau « PDF » sur doc1 et « mars 2026 » ; la carte bat"),
             ("notes", "doc4", "bandeau « Notes » sur doc4 et « févr. 2026 » ; la carte bat ; le dernier bloc de temps "
                               "vole dans la carte Notes : la barre n'est plus qu'un contour vide")]
    for word, doc, what in words:
        f = kit.at("S07", word, what)
        kit.ensure(f"{doc}_bandeau", "h", 48)
        S.key(f"{doc}_bandeau", "h", f - 1, BANNER_H2)
        g = kit.drop(f"{doc}_bandeau", f, h=70, to=[0, BANNER_Y2])
        kit.fade(f"{doc}_date", f + 2, 1)
        kit.pulse(doc, g - 3, peak=1.1, step=3)
        if word == "notes":
            block_fly("bloc8", f, doc, "barre2", 0)

    _check_entry_p2(S, kit, seam(S, "S08"))
