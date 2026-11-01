"""V08, partie 3 : S15-S22, images 1806-2872 (étape 3 : face à face et soustraction, 850 € / mois, ≈ 28 € / jour ;
chute : la banque et la mensualité, « ? € / jour » ; fin). 34 temps forts, 35,5 s.

ÉTAT D'ENTRÉE (etat_initial de S15, à épingler à 1805 : `kit.pin(f0 - 1, ENTRY_P3)` avec f0 = scene_f0(S, "S15")) :
pile `charges` au centre en PILE_S10 (`loyer`, `factures`, `credits`, `abonnements`, y 726-1180 ; `coche1..3`
tracées ; `mot_charges` au pied) ; colonne `revenus` rangée en COL_RANGE x0,4 (billets, `allocations`, `autres`,
`socle`, « Salaire net », `mot_revenus`) ; `pastille` « ? € » en PASTILLE_ATTENTE x0,85 ; `marqueur` sur 2
(done0 1) ; « Toi » en P2 (790, 1135), bras baissé. Garde-fou figurine : `if S.val("toi", "scale", f0 - 1) == 0:
c.toi.enter(f0 - 10, at=list(P2))`.

Temps forts (image du mot) :
S15  Il@1806  mettre@1837  face@1863  Troisième@1901  soustraction.@1948
S16  2 200 €@2005  moins@2062  1 350 €@2072  charges@2120  fixes.@2130
S17  reste@2162  850 €@2173  par@2185  mois.@2214
S18  Soit@2235  environ@2244  28 €@2259  courses,@2341  loisirs,@2361  imprévus,@2380  épargne.@2407
S19  Pour@2436  crédit,@2447  banque@2475  taux@2499
S20  regarde@2546  reste@2588  mensualité@2647  payée.@2666
S21  Alors,@2689  jour,@2744  connais ?@2767
S22  Abonne-toi@2790  argent.@2834   (film : dernière image 2872)

BRIEF, scène par scène :
- S15 « Il » : walk_low vers P1_R. « mettre » (morph 350 + MOVE 550) : {revenus} x0,4 -> x1 en COL_S15 ; {charges}
  -> PILE_S15 ; leurs mots du pied suivent (enfants). « face » : {ligne_niveau} se trace de x 770 vers x 140 (draw 9,
  y 726). « Troisième » : kit.step(f, 2) et `done1` 0 -> 1. « soustraction. » : c.toi.tap(f - TAP + 1,
  CHARGES_TAP_S15) (assert_reach(P1_R[0], …)) ; {moins} « − » naît du contact (pop from_pt) et se pose en
  MOINS_PIED (move 12) : « Revenus − Charges ». `lower`.
- S16 « 2 200 € » : {compteur_2200} naît du haut des revenus (pop from_pt (290, 440)) et glisse en COMPTEUR_2200_C
  (move 550) en comptant 0 -> 2200 (`value`, 14 images). « moins » : {moins} -> MOINS_CALCUL (move 550, arc 60).
  « 1 350 € » : {compteur_1350} naît du haut des charges (620, 726) et glisse en COMPTEUR_1350_C en comptant
  0 -> 1350. « charges » : c.toi.tap(…, CHARGES_TAP_S15) ; au contact {charges} -> PILE_S16 (move 550 : la pile
  glisse et couvre le bas des revenus, z 7 > 5) ; {mot_charges} se réduit ; {coche1..3} s'effacent (draw 1 -> 0 ou
  vanish) ; `lower`. « fixes. » : {total} sx 0 -> 1 (STRETCH).
- S17 « reste » : {reste} (enfant de revenus) : `h`/`pos` posés sur RESTE_S17 avec h 0 à f - 1, puis se remplit
  (h et pos ensemble, 10 images) ; {legende_reste} (couleur INK, chars complets, pos LEGENDE_S17) pop dessus.
  « 850 € » : {pastille} -> PASTILLE_S17 x1 (move 550) ; à l'arrivée `text` T_850 (textOp 0 -> bascule -> 1).
  « par » : `text` T_850_MOIS, `w` 260 -> PASTILLE_W_MOIS (STRETCH). « mois. » : {fil_pastille} se trace (draw 9).
- S18 « Soit » (morph) : {compteur_2200}, {compteur_1350}, {moins}, {total}, {fil_pastille}, {ligne_niveau}
  se réduisent ; {legende_reste} se réduit (elle renaîtra en S19) ; {revenus} ET {charges} (MÊMES clés : même pos,
  même scale) -> COL_RANGE x0,4 ; {pastille} -> PASTILLE_S18 (move 550). « environ » : {page} pop en PAGE_C ;
  {jour1..30} naissent de la pastille (pop from_pt « pastille », stagger 1) et se posent en JOURS_C. « 28 € » :
  {jour1} vanish into « pastille » ; au contact `text` T_28_JOUR et `w` -> PASTILLE_W_JOUR ; sa place reste vide.
  « courses, » : {jour2..30} puis {page} se réduisent (stagger 1) ; {panier_png} sort de la pastille (pop from_pt)
  en (330, 650) ; {mot_courses} pop. « loisirs, » : {valise}, {mot_loisirs}. « imprévus, » : {bouee},
  {mot_imprevus}. « épargne. » : {epargne1..3} tombent l'une sur l'autre (drop, stagger 3) en EPARGNE_C ;
  {mot_epargne} pop.
- S19 « Pour » (morph) : les 3 PNG, les 3 pièces et les 4 mots rentrent dans la pastille (vanish into, stagger 3) ;
  {marqueur} se réduit ; {revenus} et {charges} -> COL_S19 x1 (MÊMES clés) ; {reste} reste RESTE_S17 ;
  {legende_reste} renaît en LEGENDE_S19 ; {pastille} -> PASTILLE_S19 (garder ≥ 12 px sous y 348). « crédit, » :
  {bulle_credit} pop depuis la tête de « Toi » (from_pt) en BULLE_C (queue vers la tête). « banque » :
  c.banque.enter(f, at=list(BANQUE_POS)) ({banque_nom} enfant suit). « taux » : c.banque.lean_to(f, 6) (vers la
  colonne : vérifier le signe sur image fixe) ; {regard} se trace (draw 9) de BANQUE_TETE à CREDITS_REGARD ;
  {credits} `stroke` INK -> DEEP et pulse x1,05, puis 4 images après {revenus} pulse x1,03 (et {charges}
  identique) ; {legende_taux} pop en TAUX_C.
- S20 « regarde » : c.banque.lean_to vers le haut (autre angle) ; {regard} `pb` -> RESTE_REGARD (move 550).
  « reste » : {reste} et {legende_reste} battent (x1,05). « mensualité » : {bulle_credit} se change en
  {mensualite} (kit.morph relais, 350 ms) qui tombe en MENSUALITE_C (drop) ; {reste} rétrécit vers RESTE_S20 (h et
  pos ensemble) ; {legende_reste} -> LEGENDE_S20. « payée. » : {regard} `pb` -> RESTE_REGARD_APRES (9) ; sur la même
  image {pastille} `w` PASTILLE_W_JOUR -> PASTILLE_W_Q_JOUR et `text` T_Q_JOUR ; {pastille_28} paraît sur la
  pastille (pos PASTILLE_S19 + (PASTILLE_28_DX, 0), scale 1 à l'image du contact) et tombe à droite (drop out,
  dx +60, x 600-700 : ne traverse ni la légende ni le regard).
- S21 « Alors, » : c.banque.exit(f) ; {regard} et {legende_taux} se réduisent. « jour, » : {pastille} et
  {nom_toi} battent sur la même image (pulse x1,12, times 2, step 3). « connais ? » : {question} pop en QUESTION_C.
- S22 « Abonne-toi » : fin standard comme V07 p3 : `kit.outro("S22", outs=[], btn_at=…, press="argent.",
  pos=FIN_C, clear="fade", …)` ; s'effacent : {revenus}, {charges}, {mensualite}, {reste}, {legende_reste},
  {question}, {nom_toi} ; S.set(out["cursor"], opacity=0) (aucun pointeur) ; {pastille} : textOp 1 -> 0, `text`
  T_ABONNER, textOp -> 1, z au-dessus de la carte (kit.ensure z puis clé 41), `w` -> BTN_W et move vers FIN_BUTTON,
  opacité 0 à btn_at (relais exact du bouton) ; « Toi » reste en P1_R ; c.toi.set_z(…, tool_z=44). « argent. » :
  tap FIN_TAP (contact = image du clic out["press"]) ; {fin_onde1..2} (ring) ; `lower`. Puis plus rien ne bouge
  jusqu’à 2872.

ÉCARTS DE MISE EN SCÈNE (vérifiés sur images fixes) : le point touché des charges (S15, S16) est CHARGES_TAP_P3
(770, 1062), même bord droit, 38 px plus haut que CHARGES_TAP_S15 (l'approche du tapotement tombait sous le minimum
du stylo depuis P1_R) ; {ligne_niveau} s'efface dès « reste » (S17) : sinon la pastille « 850 € / mois » se poserait
sur sa moitié droite, et le bord bas du cyan prend le relais ; la pastille descend en 12 images (et non 16) pour
que « 850 € » soit écrit avant « par » ; S20 « mensualité » : {legende_reste} remonte dès le mot, le relais pose
{mensualite} 60 px au-dessus de sa place puis il tombe (8 images « in », arrivée sur « payée. ») et le cyan prend
RESTE_S20 sous le bloc posé (aucune bande claire pendant la chute) ; {legende_taux} en (165, 740) et non TAUX_C
(le regard vers le cyan touchait le bout de « d’endettement ») ; « ? € / jour » paraît 6 images après le contact,
quand le morceau « ≈ 28 € » a quitté la pastille ; S22 : la pastille prend l'échelle du bouton (x 112/84, w 285) et
le bouton de la carte son corps de texte (bsize 58,7) : relais exact, sans saut de hauteur.

Règles : seuls « 2 200 € », « − 1 350 € », « 850 € / mois », « ≈ 28 € / jour » s'affichent comme montants (aucun
montant par bloc, aucun « 30 ») ; le regard de la banque est un trait PLEIN encre (les pointillés sont l'IA) ; la
banque ne tient rien et ne touche rien ; pas de gris ; « Toi » seul tient le stylo, bras baissé entre deux gestes ;
la dernière image ne montre aucune collision.
"""
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, SCALE, STRETCH, TILT  # noqa: F401
from pipeline.story_kit import TAP, rotate_about  # noqa: F401

from . import *  # noqa: F401,F403
from . import (BANQUE_NOM_LOCAL, BANQUE_POS, BANQUE_TETE, BULLE_C, COL_RANGE, COL_RANGE_K,
               COL_S15, COL_S19, COMPTEUR_1350_C, COMPTEUR_2200_C, CREDITS_REGARD, DEEP, ENTRY_P3, EPARGNE,
               EPARGNE_C, FIG_BASE, FIN_BUTTON, FIN_C, FIN_TAP, HEAD_DY, INK, JOURS, JOURS_C, LEGENDE_S17,
               LEGENDE_S19, LEGENDE_S20, MENSUALITE_C, MOINS_CALCUL, MOINS_PIED, P1_R, P2, PASTILLE_28_DX,
               PASTILLE_S17, PASTILLE_S18, PASTILLE_S19, PASTILLE_W_JOUR, PASTILLE_W_MOIS, PASTILLE_W_Q_JOUR,
               PILE_S15, PILE_S16, QUESTION_C, RESTE_REGARD, RESTE_REGARD_APRES, RESTE_S17, RESTE_S20, T_28_JOUR,
               T_850, T_850_MOIS, T_ABONNER, T_Q_JOUR, T_RESTE, USAGE_MOTS, USAGE_PNG, assert_reach,
               lower, reste_pos, ring, scene_f0, walk_low)

FILM_END = 2872
PH = 84                                          # hauteur de la pastille
BTN_K = round(112 / PH, 4)                       # S22 : la pastille (h 84) à l'échelle du bouton (h 112)
DEPART_2200 = (290, 440)                         # S16 : le haut des revenus (colonne en COL_S15)
DEPART_1350 = (620, 726)                         # S16 : le haut des charges (pile en PILE_S15)
LEAN_TAUX, LEAN_RESTE = 6, 10                    # S19 / S20 : la banque se penche vers la colonne (lean > 0 : à droite)
# S15-S16 : CHARGES_TAP_S15 (772, 1100) n'est qu'à 71 px de l'épaule en P1_R : l'approche du tapotement (14 px au-dessus)
# tomberait à 57 px, sous le minimum du stylo (63). On touche le même bord droit des charges, 38 px plus haut (90 px).
CHARGES_TAP_P3 = (770, 1062)
MENS_HAUT = 60                                   # S20 : la mensualité arrive 60 px au-dessus de sa place, puis tombe
# S19-S20 : « taux d’endettement » un peu plus haut et à gauche que TAUX_C (170, 770) : le regard de la banque vers le
# cyan (S20) passe alors à 10 px du bout de « d’endettement » au lieu de le toucher.
LEGENDE_TAUX_C = (165, 740)


def _r(pt):
    return [round(pt[0], 3), round(pt[1], 3)]


def _head_pt(lean):
    """Bord droit de la tête de la banque (départ du regard), penchée de `lean`° autour du pied."""
    pivot = (BANQUE_POS[0], BANQUE_POS[1] + FIG_BASE)
    return _r(rotate_about(BANQUE_TETE, lean, pivot))


def _reste(S, f, bottom, h, d, e="out"):
    """La partie cyan `reste` : pistes h et pos ensemble, le bas reste fixe. -> f + d."""
    S.key("reste", "h", f, h, d, e)
    S.key("reste", "pos", f, reste_pos(bottom, h), d, e)
    return f + d


def _pill_text(S, id, f, text, out=4, w=None, dw=STRETCH):
    """Le libellé de la pilule s'efface (out images), le texte bascule, il revient (FADE) ; w en même temps."""
    S.key(id, "textOp", f, 0, out, "in")
    S.key(id, "text", f + out, text)
    S.key(id, "textOp", f + out, 1, FADE, "out")
    if w is not None:
        S.key(id, "w", f + out, w, dw, "out")
    return f + out + FADE


def part(S, kit, c):
    toi, banque = c.toi, c.banque
    f0 = scene_f0(S, "S15")
    kit.pin(f0 - 1, {**ENTRY_P3,
                     "pastille": {**ENTRY_P3["pastille"], "textOp": 1},
                     "marqueur": {**ENTRY_P3["marqueur"], "lbl": 1},
                     "legende_reste": {"scale": 0, "chars": len(T_RESTE), "color": INK.lower()},   # pos : posée avant le pop (S17)
                     "enveloppe": {"scale": 0}, "maison": {"scale": 0}, "panier": {"scale": 0}})
    if S.val("toi", "scale", f0 - 1) == 0:      # partie construite seule : la figurine n'est pas entrée
        toi.enter(f0 - 10, at=list(P2))
        lower(toi, f0 - 1, d=1)

    assert_reach(P1_R[0], CHARGES_TAP_P3, "S15-S16 bord droit des charges")
    assert_reach(P1_R[0], FIN_TAP, "S22 bouton")

    # ================= S15 « Il ne reste plus qu’à mettre les deux face à face. Troisième étape … » =================
    f = kit.at("S15", "Il", "« Toi » s'écarte à droite, bras baissé : la place se libère")
    walk_low(toi, f, P1_R[0])

    f = kit.at("S15", "mettre", "face à face : la colonne « Revenus » grandit et se pose à gauche, la pile "
                                "« Charges » glisse à droite ; leurs mots du pied suivent")
    kit.move("revenus", f, list(COL_S15), scale=1)
    kit.move("charges", f, list(PILE_S15))

    f = kit.at("S15", "face", "un trait en tirets part du haut des charges et traverse la colonne des revenus : "
                              "le haut des revenus dépasse")
    kit.draw("ligne_niveau", f, DRAW)

    f = kit.at("S15", "Troisième", "repère : le disque actif glisse sur 3 « Soustraire » ; le 2 se coche")
    kit.step(f, 2)
    S.key("marqueur", "done1", f + 4, 1, DRAW, "out")

    f = kit.at("S15", "soustraction.", "« Toi » touche le bord droit des charges : un grand « − » en sort et se pose "
                                       "entre les deux mots du pied : « Revenus − Charges »")
    hit = toi.tap(f - TAP + 1, list(CHARGES_TAP_P3))
    kit.pop("moins", hit, from_pt=list(CHARGES_TAP_P3), to=list(MOINS_PIED), d=12)
    lower(toi, hit + 6)

    # ================= S16 « Exemple : 2 200 € de revenus, moins 1 350 € de charges fixes. » =================
    f = kit.at("S16", "2 200 €", "« 2 200 € » sort du haut des revenus et glisse à droite en comptant de 0 à 2 200")
    S.key("compteur_2200", "pos", f - 1, list(DEPART_2200))
    kit.pop("compteur_2200", f)
    kit.move("compteur_2200", f, list(COMPTEUR_2200_C))
    S.key("compteur_2200", "value", f, 2200, 14, "out")

    f = kit.at("S16", "moins", "le « − » quitte le pied et monte en arc devant la ligne suivante")
    kit.move("moins", f, list(MOINS_CALCUL), arc=60)

    f = kit.at("S16", "1 350 €", "« 1 350 € » sort du haut des charges et glisse à côté du « − » en comptant : "
                                 "on lit « − 1 350 € »")
    S.key("compteur_1350", "pos", f - 1, list(DEPART_1350))
    kit.pop("compteur_1350", f)
    kit.move("compteur_1350", f, list(COMPTEUR_1350_C))
    S.key("compteur_1350", "value", f, 1350, 14, "out")

    f = kit.at("S16", "charges", "« Toi » pousse les charges du stylo : la pile glisse sur le bas de la colonne des "
                                 "revenus et le couvre ; « Charges » et les coches s'effacent ; le haut reste découvert")
    hit = toi.tap(f - TAP + 1, list(CHARGES_TAP_P3))
    kit.move("charges", hit, list(PILE_S16))
    kit.vanish("mot_charges", hit, d=POP)
    for cid in c.coches:
        kit.vanish(cid, hit, d=6)
    lower(toi, hit + 6)

    f = kit.at("S16", "fixes.", "un trait de total s'étire sous « − 1 350 € »")
    S.key("total", "sx", f, 1, STRETCH, "out")

    # ================= S17 « Il te reste 850 € par mois. » =================
    f = kit.at("S17", "reste", "la partie libre du haut de la colonne se remplit de cyan, de bas en haut ; « reste à "
                               "vivre » surgit dessus ; le trait de niveau s'efface, le bord du cyan le remplace")
    b, h = RESTE_S17["bottom"], RESTE_S17["h"]
    S.key("reste", "h", f - 1, 0)
    S.key("reste", "pos", f - 1, reste_pos(b, 0))
    S.key("reste", "scale", f, 1)
    S.key("reste", "opacity", f, 1)              # le morph de S07 l'avait laissée à opacité 0
    _reste(S, f, b, h, 10)
    S.key("legende_reste", "pos", f + 3, list(LEGENDE_S17))   # invisible (échelle 0) : se place avant de naître
    kit.pop("legende_reste", f + 4)
    kit.vanish("ligne_niveau", f, d=POP)

    f = kit.at("S17", "850 €", "la pastille « ? € » descend sous le trait de total et devient « 850 € »")
    kit.move("pastille", f, list(PASTILLE_S17), d=12, scale=1)
    _pill_text(S, "pastille", f, T_850)

    f = kit.at("S17", "par", "la pastille s'allonge : « 850 € / mois »")
    _pill_text(S, "pastille", f, T_850_MOIS, out=2, w=PASTILLE_W_MOIS)

    f = kit.at("S17", "mois.", "un fil deep se trace du bord de la partie cyan à la pastille : ce chiffre, c'est elle")
    kit.draw("fil_pastille", f, DRAW)

    # ================= S18 « Soit environ 28 € par jour, pour tout le reste : … » =================
    f = kit.at("S18", "Soit", "la soustraction et le fil s'effacent ; la colonne (cyan, charges, socle) se range en "
                              "petit en bas à gauche ; la pastille monte au centre")
    kit.morph(["compteur_2200", "compteur_1350", "moins", "total", "legende_reste"], [], f)
    S.key("fil_pastille", "from", f, 1, 6, "in")
    S.key("fil_pastille", "opacity", f + 6, 0)
    for g in ("revenus", "charges"):               # mêmes clés : la pile reste collée sur la colonne
        kit.move(g, f, list(COL_RANGE), scale=COL_RANGE_K)
    kit.move("pastille", f, list(PASTILLE_S18))

    f = kit.at("S18", "environ", "une page de calendrier surgit sous la pastille ; 30 cases cyan sortent de la "
                                 "pastille l'une après l'autre et s'y rangent : les jours du mois")
    kit.pop("page", f)
    for k, jid in enumerate(JOURS):
        kit.pop(jid, f + k, from_pt="pastille", to=list(JOURS_C[k]), d=12)

    f = kit.at("S18", "28 €", "la première case remonte dans la pastille, qui devient « ≈ 28 € / jour » ; sa place "
                              "reste vide")
    hit = kit.vanish("jour1", f, into="pastille", d=POP)
    _pill_text(S, "pastille", hit - 4, T_28_JOUR, w=PASTILLE_W_JOUR)

    f = kit.at("S18", "courses,", "les autres cases puis la page se réduisent ; un panier de courses sort de la "
                                  "pastille et se pose à gauche, « courses » dessous")
    for k, jid in enumerate(JOURS[1:]):
        kit.vanish(jid, f + k // 3, d=6)
    kit.vanish("page", f + 6, d=POP)
    usages = [u[0] for u in USAGE_PNG]
    kit.pop(usages[0], f, from_pt="pastille", to=list(USAGE_PNG[0][3]), d=12)
    kit.pop(USAGE_MOTS[0], f + 8)

    f = kit.at("S18", "loisirs,", "une valise sort de la pastille et se pose à droite, « loisirs » dessous")
    kit.pop(usages[1], f, from_pt="pastille", to=list(USAGE_PNG[1][3]), d=12)
    kit.pop(USAGE_MOTS[1], f + 8)

    f = kit.at("S18", "imprévus,", "une bouée sort de la pastille et se pose en bas à gauche, « imprévus » dessous")
    kit.pop(usages[2], f, from_pt="pastille", to=list(USAGE_PNG[2][3]), d=12)
    kit.pop(USAGE_MOTS[2], f + 8)

    f = kit.at("S18", "épargne.", "trois pièces sortent de la pastille l'une après l'autre et tombent en pile en bas à "
                                  "droite, « épargne » dessous : de l'argent mis de côté")
    for k, eid in enumerate(EPARGNE):
        kit.pop(eid, f + 3 * k, from_pt="pastille", to=list(EPARGNE_C[k]), d=DROP + 1, e="in")
    kit.pop(USAGE_MOTS[3], f + 8)

    # ================= S19 « Pour un crédit, ta banque regarde ton taux d’endettement. » =================
    f = kit.at("S19", "Pour", "les quatre objets et leurs mots rentrent dans la pastille ; le repère sort ; la colonne "
                              "revient en grand au centre, haut cyan ; la pastille se pose au-dessus ; « reste à "
                              "vivre » revient sur le cyan")
    kit.move("pastille", f, list(PASTILLE_S19))
    groups = [[usages[0], USAGE_MOTS[0]], [usages[1], USAGE_MOTS[1]], [usages[2], USAGE_MOTS[2]],
              [*EPARGNE, USAGE_MOTS[3]]]
    for k, grp in enumerate(groups):
        for x in grp:
            kit.vanish(x, f + 3 * k, into="pastille", d=MORPH)
    kit.vanish("marqueur", f, d=MORPH)
    for g in ("revenus", "charges"):
        kit.move(g, f, list(COL_S19), scale=1)
    S.key("legende_reste", "pos", f + 9, list(LEGENDE_S19))
    kit.pop("legende_reste", f + 10)

    f = kit.at("S19", "crédit,", "une bulle « Un crédit ? » sort de la tête de « Toi »")
    head = _r(S.to_world("toi", [0, HEAD_DY], f - 1))
    kit.pop("bulle_credit", f, from_pt=head, to=list(BULLE_C))

    f = kit.at("S19", "banque", "la banque entre à gauche, face à « Toi », la colonne entre eux ; « Banque » au-dessus "
                                "d'elle")
    kit.ensure("banque", "look", 0)
    S.key("banque", "look", f, 1)
    banque.enter(f, at=list(BANQUE_POS))

    f = kit.at("S19", "taux", "la banque se penche vers la colonne ; un trait part de sa tête jusqu'au bloc "
                              "« Crédits », qui passe au deep et bat, puis toute la colonne bat ; « taux "
                              "d’endettement » surgit à gauche")
    banque.lean_to(f, LEAN_TAUX)
    S.key("regard", "pa", f - 1, _head_pt(0))
    S.key("regard", "pa", f, _head_pt(LEAN_TAUX), POP, "out")
    kit.draw("regard", f, DRAW)
    S.key("credits", "stroke", f + 6, DEEP, 9, "out")
    kit.pulse("credits", f + 6, peak=1.05)
    for g in ("revenus", "charges"):
        kit.pulse(g, f + 10, peak=1.03)
    S.key("legende_taux", "pos", f + 3, list(LEGENDE_TAUX_C))
    kit.pop("legende_taux", f + 4)

    # ================= S20 « Mais elle regarde aussi ce qu’il te reste pour vivre, … » =================
    f = kit.at("S20", "regarde", "la banque se penche davantage ; le bout de son trait glisse du bloc « Crédits » "
                                 "jusqu'à la partie cyan")
    banque.lean_to(f, LEAN_RESTE)
    S.key("regard", "pa", f, _head_pt(LEAN_RESTE), POP, "out")
    S.key("regard", "pb", f, list(RESTE_REGARD), MOVE, "inOut")

    f = kit.at("S20", "reste", "la partie cyan et « reste à vivre » battent ensemble")
    kit.pulse("reste", f, peak=1.05)
    kit.pulse("legende_reste", f, peak=1.05)

    f = kit.at("S20", "mensualité", "la bulle « Un crédit ? » devient un bloc « Mensualité » qui tombe sur les charges ; "
                                    "la partie cyan rétrécit, « reste à vivre » remonte")
    above = [MENSUALITE_C[0], MENSUALITE_C[1] - MENS_HAUT]
    kit.move("legende_reste", f, list(LEGENDE_S20), d=8, e="out")     # cède la place au bloc qui arrive
    S.key("mensualite", "pos", f - 1, above)                          # le relais l'amène juste au-dessus des charges
    kit.morph(["bulle_credit"], ["mensualite"], f)
    land = kit.move("mensualite", f + MORPH, list(MENSUALITE_C), d=8, e="in")
    rb, rh = RESTE_S20["bottom"], RESTE_S20["h"]
    _reste(S, land - 1, rb, rh, 0)       # sous le bloc posé : le cyan découvert s'arrête net au bord de la mensualité

    f = kit.at("S20", "payée.", "le trait de la banque suit le cyan restant ; la pastille rétrécit et son « ≈ 28 € » se "
                                "détache et tombe : il reste « ? € / jour »")
    assert land <= f + 1, (land, f)
    S.key("regard", "pb", f, list(RESTE_REGARD_APRES), DRAW, "out")
    S.key("pastille_28", "pos", f - 1, [PASTILLE_S19[0] + PASTILLE_28_DX, PASTILLE_S19[1]])
    S.key("pastille_28", "scale", f, 1)
    S.key("pastille", "textOp", f, 0)
    S.key("pastille", "text", f + 6, T_Q_JOUR)            # le morceau tombé a quitté la pastille
    S.key("pastille", "textOp", f + 6, 1, FADE, "out")
    S.key("pastille", "w", f, PASTILLE_W_Q_JOUR, DRAW, "out")
    kit.drop("pastille_28", f + 1, out=True, h=60, dx=60, rot=15)

    # ================= S21 « Alors, ton reste à vivre par jour, tu le connais ? » =================
    f = kit.at("S21", "Alors,", "la banque sort avec sa pilule ; son trait et « taux d’endettement » se réduisent")
    banque.exit(f)
    S.key("regard", "from", f, 1, 6, "in")
    S.key("regard", "opacity", f + 6, 0)
    kit.vanish("legende_taux", f)

    f = kit.at("S21", "jour,", "la pastille « ? € / jour » et la pilule « Toi » battent ensemble : ce chiffre est le "
                               "sien")
    kit.pulse("pastille", f, times=2, peak=1.12)
    kit.pulse("nom_toi", f, times=2, peak=1.12)

    f = kit.at("S21", "connais ?", "un grand « ? » surgit au-dessus de « Toi »")
    kit.pop("question", f)

    # ================= S22 « Abonne-toi pour comprendre ton argent. » =================
    glide = MOVE
    outs = ["revenus", "charges", "mensualite", "legende_reste", "question", "nom_toi"]   # `reste` suit `revenus`
    out = kit.outro("S22", outs=outs, btn_at=glide, press="argent.", pos=FIN_C, clear="fade",
                    bsize=round(44 * BTN_K, 1))
    f = out["card"]
    S.set(out["cursor"], opacity=0)                      # pas de pointeur de souris : le stylo de « Toi » touche
    kit.ensure("pastille", "z", S.ents["pastille"]["z"])
    S.key("pastille", "z", f, 41)                        # au-dessus de la carte (z 40)
    S.key("pastille", "textOp", f, 0, 4, "out")
    S.key("pastille", "text", f + 4, T_ABONNER)
    S.key("pastille", "textOp", f + 4, 1, FADE, "out")
    S.key("pastille", "w", f, round(380 / BTN_K, 2), glide, "inOut")
    kit.move("pastille", f, list(FIN_BUTTON), d=glide, e="inOut", scale=BTN_K)
    S.key("pastille", "opacity", f + glide, 0)           # relais exact : le bouton de la carte paraît dessous

    fp = out["press"]
    toi.set_z(fp - TAP - 12, S.ents[toi.id]["z"], tool_z=44)    # bras et stylo au-dessus de la carte
    hit = toi.tap(fp - TAP + 1, list(FIN_TAP))
    for k in range(2):
        ring(S, f"fin_onde{k + 1}", hit + 4 * k, d=14, s0=0.6, s1=2.0)
    end = lower(toi, hit + 6, 8)
    assert hit == fp and end < FILM_END and hit + 4 + 14 < FILM_END, (hit, fp, end)
