"""V07, partie 3 : S16-S22, images 1949-2967 (erreur 3 : les doublons ; la chute : 3 questions, avant / après ; fin).
30 temps forts, 33,9 s.

ÉTAT D'ENTRÉE (etat_initial de S16, à épingler à 1948 : `kit.pin(f0 - 1, ENTRY_P3)` avec f0 = scene_f0(S, "S16")) :
`balance` à -12° côté États-Unis, ses `poids` rangés par pays (3 géants cyan r 32, 2 cyan r 18 à gauche ; 5 light
r 17 à droite), `lien_rouge` de l'`etiquette` (ETIQ_BAL, pendue au pivot par `ficelle_etiq_bal`) au géant `poids1`,
`compteur` « ≈ 70 % » rouge en COMPTEUR_C au-dessus de `pil_usa`, `pil_autres` à droite ; repère sur 2 (done0 1) ;
« Toi » en P2 (860, 1135), bras baissé. Garde-fou figurine : `if S.val("toi", "scale", f0 - 1) == 0:
c.toi.enter(f0 - 10, at=list(P2))`.

Temps forts (image du mot) :
S16  Et@1949  voulant@1974  corriger@1983  aggrave@2010  choses.@2023
S17  Troisième@2046  empiler@2085  ETF@2108  ressemblent.@2138
S18  Monde,@2197  S&P@2252  Nasdaq ?@2337
S19  plusieurs@2381  mêmes@2403  lignes,@2463  pas@2489  diversification.@2504
S20  Le@2544  réflexe@2556  trois@2586  questions.@2593  indice ?@2629  dedans ?@2685  coûte@2723
S21  nom@2761  suffit@2769  composition,@2839  si.@2862
S22  Abonne-toi@2883  argent.@2929   (film : dernière image 2967)

BRIEF, scène par scène :
- S16 « Et » : {lien_rouge} se retire (`from` 0 -> 1, 9 images) ; {pil_usa} -> PIL_USA_HAUT et {compteur} ->
  COMPTEUR_HAUT, x HAUT_K (move 550). « voulant » : c.toi.reach vers PB_NEE (assert_reach(P2[0], PB_NEE, …)).
  « corriger » : {pb1} (enfant de la balance, ouvert, titres cyan {pb1_geant1..3}, {pb1_petit1..2} déjà dedans) naît
  de la pointe (pop from_pt = PB_NEE, échelle PB_K) puis se pose en PB_POSE (drop). `lower`. « aggrave » : {pb1}
  glisse le long de la planche vers PB1_SEAT (move 550 « in ») ; {balance} -12 -> TILTS["S16"] (TILT). « choses. » :
  {compteur} et {pil_usa} battent (x1,15) ; tenue.
- S17 « Troisième » : kit.step(f, 2) et `done1` 0 -> 1. « empiler » : {pb2} naît de la pointe (même geste) et tombe
  sur {pb1} en PB2_SEAT (drop) ; {balance} -> TILTS["S17"]. « ETF » : {pb1} puis {pb2} battent (stagger 4, x1,1).
  « ressemblent. » : {poids} géants (GEANTS) + {pb1_geant*} + {pb2_geant*} battent sur la même image (x1,2).
- S18 « Monde, » : {etiquette} bat (x1,15). « S&P » : {etiq_sp} sort de {pb1} (pop from_pt « pb1 ») vers ETIQ_SP_C
  (move 350), {ficelle_etiq_sp} se trace. « Nasdaq ? » : idem {etiq_nq} -> ETIQ_NQ_C, {ficelle_etiq_nq} ; 8 images
  après, {etiq_sp}, {etiq_nq} et {pil_usa} battent ensemble (x1,1).
- S19 « plusieurs » : les géants battent en trois temps : planche, puis {pb1}, puis {pb2} (stagger 5, x1,25).
  « mêmes » : {fois3} « ×3 » rouge pop en FOIS3_C. « lignes, » : {ficelle_etiq_bal}, {ficelle_etiq_sp},
  {ficelle_etiq_nq} se retirent (`from` -> 1) ; {etiquette}, {etiq_sp}, {etiq_nq} se rangent en ETIQ_LISTE (stagger 4
  de move 450 ; l'étiquette 240 px, les sœurs 260 : aligner leurs bords gauches si besoin) ; {liste_titre} « 3 ETF »
  pop en LISTE_TITRE_C. « pas » : c.toi.reach vers (690, 990) (le groupe « autres pays »). « diversification. » :
  {place_vide} (enfant de la balance, au bout droit de la planche) pop, son contour bat deux fois (pulse), elle
  RESTE vide ; `lower`.
- S20 « Le » : {pb1}, {pb2}, {etiq_sp}, {etiq_nq}, {fois3}, {liste_titre}, {place_vide}, {pil_autres} sortent
  (morph sortie groupée) ; {etiquette} revient pendre sous le pivot en ETIQ_BAL (move 450) avec {ficelle_etiq_bal}
  retracée (from 1 -> 0 ou draw) ; {balance} revient à plat (rot 0, TILT). « réflexe » : MORPH : {balance} se réduit
  pendant que {panier} renaît en PANIER_BAL_C puis va en PANIER_C (sans couvercle) ; les {titre*} (titre1..7, 9, 10,
  titre_neuf) reparaissent derrière le rebord AVEC leurs couleurs et tailles (poser fill / scale pendant qu'ils sont à
  0 : 5 cyan dont 3 géants x32/26, 5 light x17/26 ; garder des places sans chevauchement), les {poids} se réduisent ;
  {pil_usa} et {compteur} rentrent dans un titre cyan (vanish into) ; {etiquette} remonte en ETIQ_C et {ficelle_etiq}
  se retrace ; walk_low vers P1. « trois » : relais {marqueur} -> {marqueur2} et {titre_erreurs} -> {titre_questions}
  (kit.morph pair, mêmes places ; marqueur2 on 0). « questions. » (7 images après) : {fiche} tombe (kit.drop, échelle
  FICHE_K ; lignes vides, {fiche_tirets1..3} en tirets). « indice ? » : {marqueur2} on 0 -> 1 (étape 1) ; {livre}
  ressort du disque 1 (pop from_pt DISQUE_PT[0], petit : x0,3) et file vers la puce de {fiche_L1}
  (c.sheet.world(S, 0, "bullet", n=f)), s'y réduit (vanish into) ; {fiche_tirets1} s'efface, `bulletOn` 1 et
  kit.type(fiche_L1, flash=True). « dedans ? » : kit.step(f, 1, id="marqueur2") ; {saut_geant} (copie d'un géant du
  panier : l'original reste) saute en arc 80 vers la puce de {fiche_L2}, s'y réduit ; type L2. « coûte » : step 2 ;
  {frais_etf} ressort de {etiquette} (pop from_pt « etiquette ») et file vers la puce de {fiche_L3} ; type L3.
- S21 « nom » : {panier_couvercle} retombe (drop) en COUVERCLE_LOCAL (enfant du panier) ; les titres se cachent
  sous lui sur la même image (échelle 0 à l'image du contact). « suffit » : tap ETIQ_TAP (assert_reach(P1[0], …)) ;
  {etiquette} tremble (shake x 8), rien n'en sort. « composition, » : tap COUVERCLE_TAP ; le couvercle s'envole en
  arc vers le haut à gauche et se réduit ; les titres colorés reparaissent (pop) ; {fiche} bat (x1,06).
  « si. » : tap REBORD_TAP ; {panier_coche} se trace au contact (coche pleine deep 48) ; `lower` ; tenue.
- S22 « Abonne-toi » : fin standard comme V06 p3 : `kit.outro("S22", outs=[], btn_at=MOVE, press="argent.",
  pos=FIN_C, …)` ; tout ce qui reste ({panier} et parts, titres, {fiche}, {marqueur2}, {titre_questions}) s'efface
  (vanish into FIN_C ou clear "fade") ; S.set(out["cursor"], opacity=0) (aucun pointeur) ; {etiquette} : `textOp`
  1 -> 0, texte « S’abonner » (T_ABONNER), textOp -> 1, z au-dessus de la carte (kit.ensure z puis clé 41), w -> 380
  et move vers FIN_BUTTON (scale BTN_H/ETIQ_H en hauteur : h 60 -> 112, ou garder h et laisser le bouton relayer à
  btn_at), opacité 0 à btn_at (relais exact) ; walk_low vers P_FIN pendant le morph ; c.toi.set_z(…, tool_z=44) ;
  « argent. » : tap FIN_TAP (contact = image du clic `out["press"]`), {fin_onde1..2} (ring) ; `lower`. Puis plus rien
  ne bouge jusqu'à 2967.

ÉCARTS DE MISE EN SCÈNE (lisibilité, vérifiés sur images fixes) : {pil_usa} monte à l'échelle 1 (texte 30 px ;
x0,7 le rendait illisible) ; {pil_autres} glisse en PIL_AUTRES_S16 (815, 880) sur « Et » (le petit panier se pose sur
sa place) ; « ETF Monde » revient sous le pivot sans retracer sa ficelle (12 images avant « réflexe ») ; S20-S22 :
panier en PANIER_S20 (340, 1090) et fiche à l'échelle 1 centrée en FICHE_S20 (540, 636) (texte des lignes 32 px,
bas du cadre occupé) ; les points touchés de S21 suivent le panier (+80 px en y).

Règles : jamais de VALIDÉ ; la place vide reste vide ; rouge seulement {compteur}, {fois3} (et {lien_rouge} qui se
retire) ; pas de gris ; « Toi » seul tient le stylo, bras baissé entre deux gestes ; tout ce qui est visible à la
dernière image ne se chevauche pas.
"""
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, SCALE, TILT  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401

from . import *  # noqa: F401,F403
from . import (COMPTEUR_HAUT, COUVERCLE_LOCAL, COUVERCLE_TAP, CYAN, DISQUE_PT, ENTRY_P3, ETIQ_BAL, ETIQ_C,
               ETIQ_H, ETIQ_LISTE, ETIQ_TAP, FIN_BUTTON, FIN_C, FIN_TAP, GEANTS, HAUT_K, LIGHT, P1, P2, P_FIN,
               PANIER_BAL_C, PANIER_C, PB1_SEAT, PB2_SEAT, PB_K, PB_NEE, PB_POSE, PIL_USA_HAUT, POIDS, REBORD_TAP,
               T_ABONNER, TILTS, TITRE_R, TITRE_TOMBE, TITRES, TITRES_LOCAL, assert_reach, lower, ring, scene_f0,
               walk_low)

FILM_END = 2967
BTN_K = round(112 / ETIQ_H, 4)                   # S22 : l'étiquette (h 60) à l'échelle du bouton (h 112)
ETIQ_LISTE_X0 = ETIQ_LISTE[0][0] - 10            # S19 : « ETF Monde » (240) aligné à gauche sur les sœurs (260)
PB_HAUT = 60                                     # S16 : le petit panier se pose de 60 px au-dessus de sa place
PB2_ARC = 100                                    # S17 : le second petit panier tombe en arc sur le premier
VIDE_PT = (690, 990)                             # S19 « pas » : la pointe sur le groupe « autres pays »
COUVERCLE_FUITE = (-200, -150)                   # S21 : le couvercle s'envole en haut à gauche (local panier ;
                                                 # monde 140, 940 : il reste dans le cadre en se réduisant)
# S20-S22 : le panier revient PLUS BAS que dans S01-S11 (bas du cadre utilisé jusqu'à y 1190) et la fiche, à
# l'échelle 1 (texte des lignes à 32 px), se centre sous le repère : x 290-790, y 380-892 ; titres du panier dès y 908.
PANIER_S20 = (PANIER_C[0], 1090)
ETIQ_S20 = (PANIER_S20[0], PANIER_S20[1] + (ETIQ_C[1] - PANIER_C[1]))           # (340, 1130)
PANIER_NEE_S20 = (PANIER_BAL_C[0], PANIER_S20[1])                               # (400, 1090) : sur le pivot
FICHE_S20, FICHE_S20_K = (540, 636), 1.0
_DY = PANIER_S20[1] - PANIER_C[1]
ETIQ_TAP_S21 = (ETIQ_TAP[0], ETIQ_TAP[1] + _DY)                                 # (455, 1130)
COUVERCLE_TAP_S21 = (COUVERCLE_TAP[0], COUVERCLE_TAP[1] + _DY)                  # (530, 972)
REBORD_TAP_S21 = (REBORD_TAP[0], REBORD_TAP[1] + _DY)                           # (520, 995)
LIVRE_VOL = (300, 430)                           # S20 « indice ? » : le livre sort du disque 1, à gauche de la fiche
PIL_AUTRES_S16 = (815, 880)                      # S16-S19 : « autres pays » à droite, bord droit ombre comprise < x 940 (QA) ; le petit panier se pose
                                                 # au bout haut de la planche, x 538-754)

# S20 : les 10 titres du panier, avec leurs couleurs et leurs tailles de la balance, sans chevauchement.
# Rangée arrière : 3 géants cyan (r 32) et 2 cyan (r 18), bas à y -118 ; rangée avant : 5 clairs (r 17), bas à y -95
# (le haut du rebord est à -103). Écarts vérifiés : géant / clair >= 50 px, cyan 18 / clair >= 40 px.
_VISIBLES = [t if k != TITRE_TOMBE else "titre_neuf" for k, t in enumerate(TITRES)]
_R = [32, 18, 32, 18, 32, 17, 17, 17, 17, 17]
TITRES_S20 = {t: {"pos": [TITRES_LOCAL[k][0], -118 - _R[k] if k < 5 else -95 - _R[k]],
                  "scale": round(_R[k] / TITRE_R, 4), "fill": CYAN if k < 5 else LIGHT}
              for k, t in enumerate(_VISIBLES)}
GEANT_SAUT = _VISIBLES[2]                        # le géant du milieu (x 0) : sa copie saute dans la fiche


def _r(pt):
    return [round(pt[0], 3), round(pt[1], 3)]


def part(S, kit, c):
    toi, sheet = c.toi, c.sheet
    f0 = scene_f0(S, "S16")
    def _same_hex(i, k, v):                    # même couleur que la fin de p2, à la casse près : la garder
        if isinstance(v, str) and v.startswith("#") and k in S.ents[i]["t"]:
            cur = S.val(i, k, f0 - 2)
            return cur if isinstance(cur, str) and cur.lower() == v.lower() else v
        return v
    entry = {i: {k: _same_hex(i, k, v) for k, v in tr.items()} for i, tr in ENTRY_P3.items()}
    kit.pin(f0 - 1, {**entry,
                     "panier_couvercle": {"scale": 0},
                     "titre_questions": {"scale": 0},
                     "marqueur2": {"scale": 0, "on": 0},
                     "fiche": {"scale": 0},
                     "toi_nom": {"opacity": 0}})
    if S.val("toi", "scale", f0 - 1) == 0:      # partie construite seule : la figurine n'est pas entrée
        toi.enter(f0 - 10, at=list(P2))
        lower(toi, f0 - 1, d=1)
    if abs(S.val("toi", "pos", f0 - 1)[0] - P2[0]) > 0.5:   # partie seule : « Toi » est resté en P1 (cast)
        walk_low(toi, f0 - 40, P2[0], d=30)
    kit.ensure("toi", "look", 0)

    assert_reach(P2[0], PB_NEE, "S16 pointe du petit panier", fig_y=P2[1])
    assert_reach(P2[0], VIDE_PT, "S19 autres pays", fig_y=P2[1])
    for pt, what in ((ETIQ_TAP_S21, "S21 étiquette"), (COUVERCLE_TAP_S21, "S21 couvercle"),
                     (REBORD_TAP_S21, "S21 rebord")):
        assert_reach(P1[0], pt, what)
    assert_reach(P_FIN[0], FIN_TAP, "S22 bouton", fig_y=P_FIN[1])

    # ================= S16 « Et c’est souvent en voulant corriger qu’on aggrave les choses. » =================
    f = kit.at("S16", "Et", "le fil rouge se retire ; « États-Unis » et « ≈ 70 % » montent en haut à gauche, plus "
                            "petits")
    S.key("lien_rouge", "from", f, 1, DRAW, "in")
    S.key("lien_rouge", "opacity", f + DRAW, 0)
    kit.move("pil_usa", f, list(PIL_USA_HAUT))           # échelle 1 : son texte (30 px) reste lisible
    kit.move("pil_autres", f, list(PIL_AUTRES_S16))      # cède le bout haut de la planche au petit panier
    kit.move("compteur", f, list(COMPTEUR_HAUT), scale=HAUT_K)

    f = kit.at("S16", "voulant", "« Toi » lève son stylo vers le bout haut de la planche")
    toi.reach(f, list(PB_NEE), d=POP)

    f = kit.at("S16", "corriger", "sous la pointe naît un petit panier ouvert plein de titres cyan ; il monte et se "
                                  "pose sur le bout haut de la planche, au-dessus des titres clairs")
    above = [PB_POSE[0], PB_POSE[1] - PB_HAUT]
    g = kit.pop("pb1", f, scale=PB_K, from_pt=list(PB_NEE), to=above)
    kit.drop("pb1", g, h=PB_HAUT, to=list(PB_POSE))
    lower(toi, f + 12)

    f = kit.at("S16", "aggrave", "le petit panier glisse le long de la pente et se pose sur les géants cyan, côté "
                                 "États-Unis ; la balance penche encore plus (-15°)")
    kit.move("pb1", f, list(PB1_SEAT), e="in")
    S.key("balance", "rot", f + 6, TILTS["S16"], TILT, "out")

    f = kit.at("S16", "choses.", "« ≈ 70 % » et « États-Unis » battent ensemble ; tenue")
    kit.pulse("compteur", f)
    kit.pulse("pil_usa", f)

    # ================= S17 « Troisième erreur : empiler des ETF qui se ressemblent. » =================
    f = kit.at("S17", "Troisième", "le repère passe au 3 « Doublons » ; le disque 2 se coche")
    kit.step(f, 2)
    S.key("marqueur", "done1", f + 4, 1, DRAW, "out")

    f = kit.at("S17", "empiler", "un second petit panier plein de titres cyan naît sous la pointe du stylo et tombe "
                                 "sur le premier : empilés ; la balance penche à -17°")
    toi.reach(f - POP, list(PB_NEE), d=POP)
    here = _r(S.parent_space("pb2", list(PB_NEE), f - 1))
    g = kit.pop("pb2", f, scale=PB_K, from_pt=list(PB_NEE), to=here)
    land = kit.move("pb2", g, list(PB2_SEAT), d=14, e="in", arc=PB2_ARC)
    S.key("balance", "rot", land - 2, TILTS["S17"], TILT, "out")
    lower(toi, g + 2)

    f = kit.at("S17", "ETF", "les deux petits paniers battent l'un après l'autre")
    kit.stagger(["pb1", "pb2"], f, 4, kit.pulse, peak=round(PB_K * 1.1, 4))

    f = kit.at("S17", "ressemblent.", "les 3 géants de la planche et ceux des deux petits paniers battent ensemble : "
                                      "les mêmes")
    planche_geants = [POIDS[k] for k in GEANTS]
    pb_geants = [f"{pb}_geant{k + 1}" for pb in ("pb1", "pb2") for k in range(3)]
    for gid in planche_geants + pb_geants:
        kit.pulse(gid, f, peak=round(S.val(gid, "scale", f - 1) * 1.2, 4))

    # ================= S18 « Un ETF Monde, un ETF S&P 500 et un ETF Nasdaq ? » =================
    f = kit.at("S18", "Monde,", "l'étiquette « ETF Monde » bat")
    kit.pulse("etiquette", f)

    f = kit.at("S18", "S&P", "l'étiquette « ETF S&P 500 » sort du petit panier du bas et pend à sa droite, reliée par "
                             "une ficelle")
    kit.pop("etiq_sp", f, from_pt="pb1", to=[420, 905], d=MORPH)
    kit.draw("ficelle_etiq_sp", f + 5)

    f = kit.at("S18", "Nasdaq ?", "l'étiquette « ETF Nasdaq » sort du petit panier du haut et pend à sa droite ; "
                                  "puis les deux étiquettes sœurs et « États-Unis » battent ensemble")
    kit.pop("etiq_nq", f, from_pt="pb2", to=[420, 820], d=MORPH)
    kit.draw("ficelle_etiq_nq", f + 5)
    for eid in ("etiq_sp", "etiq_nq", "pil_usa"):
        kit.pulse(eid, f + 8, peak=round(S.val(eid, "scale", f + 7) * 1.1, 4))

    # ================= S19 « Tu achètes plusieurs fois les mêmes grandes entreprises. Plus de lignes, … » =========
    f = kit.at("S19", "plusieurs", "les géants battent en trois temps : sur la planche, dans le petit panier du bas, "
                                   "dans celui du haut")
    for k, grp in enumerate((planche_geants, pb_geants[:3], pb_geants[3:])):
        for gid in grp:
            kit.pulse(gid, f + 5 * k, peak=round(S.val(gid, "scale", f - 1) * 1.25, 4))

    f = kit.at("S19", "mêmes", "« ×3 » rouge surgit à côté de la pile")
    kit.pop("fois3", f)

    f = kit.at("S19", "lignes,", "les ficelles se retirent ; les trois étiquettes se rangent en liste à droite, sous "
                                 "« 3 ETF » : les lignes d'un portefeuille")
    for wid in ("ficelle_etiq_bal", "ficelle_etiq_sp", "ficelle_etiq_nq"):
        S.key(wid, "from", f, 1, 6, "in")
        S.key(wid, "opacity", f + 6, 0)
    dests = [(ETIQ_LISTE_X0, ETIQ_LISTE[0][1]), ETIQ_LISTE[1], ETIQ_LISTE[2]]
    for k, (eid, to) in enumerate(zip(("etiquette", "etiq_sp", "etiq_nq"), dests)):
        kit.move(eid, f + 2 + 4 * k, list(to), d=14)
    kit.pop("liste_titre", f + 8)

    f = kit.at("S19", "pas", "« Toi » pointe son stylo vers le groupe « autres pays », au bout haut de la planche")
    toi.reach(f, list(VIDE_PT), d=POP)

    f = kit.at("S19", "diversification.", "au bout de la planche, une place ronde en tirets surgit et bat deux fois : "
                                          "elle reste vide")
    g = kit.pop("place_vide", f)
    g = kit.pulse("place_vide", g, times=2, peak=1.25)
    lower(toi, g)

    # ================= S20 « Le bon réflexe tient en trois questions. Quel indice ? … » =================
    f = kit.at("S20", "Le", "les petits paniers, les étiquettes sœurs, « ×3 », « 3 ETF », la place vide et "
                            "« autres pays » se réduisent ; « ETF Monde » revient sous le pivot ; la balance revient "
                            "à plat")
    kit.morph(["pb1", "pb2", "etiq_sp", "etiq_nq", "fois3", "liste_titre", "place_vide", "pil_autres"], [], f)
    kit.move("etiquette", f, list(ETIQ_BAL), d=12)
    S.key("balance", "rot", f, 0, TILT, "out")

    f = kit.at("S20", "réflexe", "la balance se replie en panier ouvert : ses titres y retombent avec leurs couleurs "
                                 "et leurs tailles ; « États-Unis » et « ≈ 70 % » rentrent dans les géants cyan ; "
                                 "l'étiquette remonte sur le devant du panier ; « Toi » revient à gauche")
    for t, st in TITRES_S20.items():               # posés pendant que le panier est à l'échelle 0
        S.key(t, "pos", f - 1, st["pos"])
        S.key(t, "scale", f - 1, st["scale"])
        S.key(t, "fill", f - 1, st["fill"])
        S.key(t, "opacity", f - 1, 1)
    kit.vanish("balance", f, d=MORPH)
    S.key("panier", "pos", f - 1, list(PANIER_NEE_S20))
    g = kit.pop("panier", f, scale=1, d=MORPH)
    arr = kit.move("panier", g, list(PANIER_S20))
    kit.vanish("pil_usa", f + 2, into=_VISIBLES[0], d=MORPH)
    kit.vanish("compteur", f + 2, into=_VISIBLES[2], d=MORPH)
    kit.move("etiquette", f, list(ETIQ_S20), d=arr - f)
    kit.draw("ficelle_etiq", arr - 6)
    walk_low(toi, f, P1[0], d=arr - f)

    f = kit.at("S20", "trois", "« 3 erreurs » devient « 3 questions » ; le repère prend les légendes Indice · Pays · "
                               "Frais")
    kit.morph(["marqueur", "titre_erreurs"], ["marqueur2", "titre_questions"], f)

    f = kit.at("S20", "questions.", "la fiche « Composition » à trois lignes vides descend de sous le repère")
    S.key("fiche", "scale", f - 1, FICHE_S20_K)
    kit.drop("fiche", f, h=160, to=list(FICHE_S20))
    fiche_ok = f + DROP

    def bullet(i):
        return _r(sheet.world(S, i, "bullet", n=fiche_ok))

    def answer(i, g, src):
        """`src` arrive sur la puce de la rangée i à l'image g : il s'y réduit, la puce vide s'efface, la puce
        pleine paraît et la ligne s'écrit. -> image où tout est écrit."""
        kit.vanish(src, g, into=bullet(i), d=5)
        kit.vanish(f"fiche_tirets{i + 1}", g, d=5)
        S.key(c.lignes[i], "bulletOn", g + 3, 1)
        return kit.type(c.lignes[i], g + 3, flash=True)

    f = kit.at("S20", "indice ?", "disque 1 allumé ; le livre de l'indice ressort du disque 1, file vers la 1re ligne "
                                  "et devient sa puce : « Indice : MSCI World » s'écrit")
    S.key("marqueur2", "on", f, 1, FADE, "out")
    for lid in ["livre"] + [i for i, e in S.ents.items() if e.get("parent") == "livre"]:
        z0 = S.ents[lid]["z"]                      # au-dessus de la fiche (z 8) pendant le vol
        kit.ensure(lid, "z", z0)
        S.key(lid, "z", f, z0 + 4)
    g = kit.pop("livre", f, scale=0.4, from_pt=list(DISQUE_PT[0]), to=list(LIVRE_VOL))
    g = kit.move("livre", g, bullet(0), d=12, scale=0.12)
    answer(0, g, "livre")

    f = kit.at("S20", "dedans ?", "disque 2 ; une copie d'un géant cyan saute du panier en arc jusqu'à la 2e ligne et "
                                  "devient sa puce : « États-Unis : ≈ 70 % » s'écrit")
    kit.step(f, 1, id="marqueur2")
    S.key("saut_geant", "pos", f - 1, _r(S.to_world(GEANT_SAUT, [0, 0], f - 1)))
    S.key("saut_geant", "scale", f - 1, round(S.world_scale(GEANT_SAUT, f - 1) * TITRE_R / 32, 4))   # disque r 32
    S.key("saut_geant", "opacity", f - 1, 1)
    g = kit.move("saut_geant", f, bullet(1), arc=80, scale=0.6)
    answer(1, g, "saut_geant")

    f = kit.at("S20", "coûte", "disque 3 ; la pièce cyan des frais ressort de l'étiquette et file vers la 3e ligne, "
                               "dont elle devient la puce : « Frais /an : bas » s'écrit")
    kit.step(f, 2, id="marqueur2")
    g = kit.pop("frais_etf", f, from_pt="etiquette", to=[ETIQ_S20[0] + 150, ETIQ_S20[1] - 60])
    g = kit.move("frais_etf", g, bullet(2), d=12, scale=0.8)
    answer(2, g, "frais_etf")

    # ================= S21 « Un nom ne suffit pas à savoir ce que tu achètes. La composition, si. » =============
    f = kit.at("S21", "nom", "le couvercle retombe sur le panier et cache les titres : on ne voit plus que "
                             "l'étiquette « ETF Monde »")
    kit.drop("panier_couvercle", f, h=70, d=7, to=list(COUVERCLE_LOCAL))
    for t in TITRES_S20:
        x, y = TITRES_S20[t]["pos"]
        S.key(t, "pos", f + 1, [x, y + 24], 4, "in")
        S.key(t, "scale", f + 1, 0, 4, "in")

    f = kit.at("S21", "suffit", "« Toi » touche l'étiquette : elle tremble, rien n'en sort")
    hit = toi.tap(f - TAP + 1, list(ETIQ_TAP_S21))
    kit.shake("etiquette", hit, amp=8)
    lower(toi, hit + 6)

    f = kit.at("S21", "composition,", "« Toi » touche le couvercle : il s'envole en haut à gauche ; les titres "
                                      "colorés réapparaissent et la fiche « Composition » bat")
    hit = toi.tap(f - TAP + 1, list(COUVERCLE_TAP_S21))
    kit.ensure("panier_couvercle", "z", S.ents["panier_couvercle"]["z"])
    kit.ensure("panier_bouton", "z", S.ents["panier_bouton"]["z"])
    S.key("panier_couvercle", "z", hit, 9)
    S.key("panier_bouton", "z", hit, 9.1)
    kit.move("panier_couvercle", hit, list(COUVERCLE_FUITE), d=MORPH, e="out", arc=60)
    kit.vanish("panier_couvercle", hit, d=MORPH)
    for k, (t, st) in enumerate(TITRES_S20.items()):
        S.key(t, "pos", hit + 1, st["pos"])
        kit.pop(t, hit + 1 + k // 3, scale=st["scale"])
    kit.pulse("fiche", hit + 4, peak=round(FICHE_S20_K * 1.03, 4))   # 1,03 : le haut reste sous la légende
    lower(toi, hit + 6)

    f = kit.at("S21", "si.", "« Toi » touche le rebord du panier : sa coche pleine s'y trace ; tenue")
    hit = toi.tap(f - TAP + 1, list(REBORD_TAP_S21))
    kit.draw("panier_coche", hit)
    lower(toi, hit + 6)

    # ================= S22 « Abonne-toi pour comprendre ton argent. » =================
    glide = MOVE
    out = kit.outro("S22", outs=[], btn_at=glide, press="argent.", pos=FIN_C, bsize=round(34 * BTN_K, 1),
                    labelSize=34)
    f = out["card"]
    S.set(out["cursor"], opacity=0)                      # pas de pointeur de souris : le stylo de « Toi » touche
    for o in ("panier", "fiche", "marqueur2", "titre_questions"):   # tout converge vers la carte
        kit.vanish(o, f, into=list(FIN_C), d=MORPH)
    S.key("ficelle_etiq", "draw", f, 0, 4, "in")
    kit.ensure("etiquette", "z", S.ents["etiquette"]["z"])
    S.key("etiquette", "z", f, 41)                       # au-dessus de la carte (z 40)
    kit.ensure("etiquette", "textOp", 1)
    S.key("etiquette", "textOp", f, 0, 4, "out")
    S.key("etiquette", "text", f + 4, T_ABONNER)
    S.key("etiquette", "textOp", f + 4, 1, FADE, "out")
    S.key("etiquette", "w", f, round(380 / BTN_K, 2), glide, "inOut")
    kit.move("etiquette", f, list(FIN_BUTTON), d=glide, e="inOut", scale=BTN_K)
    S.key("etiquette", "opacity", f + glide, 0)          # relais exact : le bouton de la carte paraît dessous
    walk_low(toi, f, P_FIN[0])

    fp = out["press"]
    toi.set_z(fp - TAP - 12, S.ents[toi.id]["z"], tool_z=44)    # bras et stylo au-dessus de la carte
    toi.reach(fp - TAP - 10, [FIN_TAP[0] + 10, FIN_TAP[1] + 40], d=10)
    hit = toi.tap(fp - TAP + 1, list(FIN_TAP))
    for k in range(2):
        ring(S, f"fin_onde{k + 1}", hit + 4 * k, d=14, s0=0.6, s1=2.0)
    end = lower(toi, hit + 6, 8)
    assert hit == fp and end < FILM_END and hit + 4 + 14 < FILM_END, (hit, fp, end)
