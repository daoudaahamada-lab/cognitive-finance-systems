"""V12, partie 3 : S15-S22, images 1863-2872 (35 temps forts, 33,7 s). Le panier du berceau qui se vide sur 10 puis
20 ans, la ligne des horizons, l'imprévu payé tout de suite, l'arbre qui fait grandir l'argent, la courbe et son creux,
le tableau rôle / durée, le billet rouge sans mission, la fin.

ÉTAT D'ENTRÉE : ENTRY_P3 épinglé à 1862 (`kit.pin(f0 - 1, ENTRY_P3)`, f0 = scene_f0(S, "S15") = 1863) : etat_initial
de S15 = résultat de S14 (berceau (BERCEAU_C) et ses 5 billets couchés, « z z z », pilule « ? » en tirets (ROLE_PROG_C) ;
bouée + billet1-3 « Imprévus », valise + billet4-5 « Projet » ; carte (COMPTE_LOW) et pilule (CASH_LOW) à 0,8 ; panier
et son monde éteints). Garde-fou de partie isolée (sans effet dans le film entier) :
`if S.val("toi", "scale", f0 - 1) == 0: c.toi.enter(f0 - 12, at=TOI_P2); c.toi.stow(f0 - 9, d=2); c.toi.lower(f0 - 8)`.
SORTIE : fin du film (image 2872, FILM_END = 2873) ; plus rien ne bouge après le toucher (≈ 2850).

Ids : panier, b6-b10, vide9, vide10, etiquette (+ etiq_taux), ficelle_panier (piste bAt), berceau, zzz1-3,
billet1-10, billet_arbre, billet_dort, temps_long, temps_auj, temps_10, temps_20, separateur, court, long, court_mot,
long_mot, bouee, valise, bouclier, imprevu, arbre, role_vide (+ _mot), role_progresser (+ _mot), role_imprevus,
role_projet, courbe, courbe_creux, duree1-3, role_dort (+ _mot), cash, compte, toi, fin_doigt, fin_onde1-2.

TOUR DE REVUE 1 (prime sur le brief ci-dessous quand ils diffèrent) : S15 étiquette ×0,8 et pilule « inflation »
au-dessus (masquée sur « progresser »), le panier s'enfonce de 24 px ; S17 la ligne croise la barre, chaque morceau bat
avec ses objets, stylo rangé ; S18 bouclier ressorti de la bouée, ⚠ r 50, billet en arc haut sous la pilule puis
au-dessus du disque, ⚠ rentre dans le billet ; S19 berceau -> arbre en un relais sur « cherche », panier plein qui bat
avec l'étiquette, relais panier -> courbe sur « acceptant » (tracée jusqu'au creux), « risque. » : point rouge puis la
courbe repart plus haut, la pile -30 puis +50 ; S20 « durée » : fils deep pile -> morceau de barre, puis pilules de
durée sous les rôles ; S21 berceau à cheval sur le bas de la ligne, coches deep sur « n'est », « Toi » pointe le billet
rouge ; S22 libellé changé à mi-morph.

BRIEF, scène par scène :
- S15 (1863-2035) « L’inflation » (1863) : le panier (× PANIER_LOW_K) sort du berceau : kit.pop("panier", f,
  scale=PANIER_LOW_K, from_pt=PILE_BERCEAU[0], to=PANIER_LOW, d=11) ; b6-b10 (pleins, light) apparaissent un à un,
  chacun quand un billet du berceau (billet6-10) bat (kit.stagger 3 images : pop de l'article + pulse du billet).
  « pèse » (1882) : etiquette posée à ETIQ_LOW, échelle ETIQ_LOW_K (face « + 2 % / an ») : drop_in ; ficelle_panier :
  bAt -> [170, -85] (d=0 avant) puis kit.draw(…, 6) ; le panier s'enfonce de 10 px puis remonte (move 6 + 8 images,
  out). Bouée et valise ne bougent pas. « longtemps, » (1966) : temps_long apparaît en largeur depuis la gauche
  (TEMPS_LONG_C0, w TEMPS_LONG_W0, STRETCH 6) ; temps_auj (ancre end) posé en (TEMPS_LONG_AUJ_END_X, 300) et
  temps_10 posé en TEMPS_LONG_10_C (ATTENTION : temps_10 est ancré « start » ; centre-le à la main, x 650 - largeur / 2)
  : scale 1 à f - 1, opacité 0 -> 1 (FADE). « immobile. » (2010) : kit.stagger(zzz1-3, f, 3, kit.pulse, peak=1.15) ;
  les billets restent couchés.
- S16 (2036-2141) « 10 » (2046) : S.key("temps_long", "value", f, 1, 9, "linear") ; kit.pulse("etiquette", f, step=2,
  peak=1.1) ; b10 value 1 -> 0.1 (9 images). « 20 ans, » (2055) : temps_long w -> TEMPS_LONG_W1 et pos ->
  TEMPS_LONG_C1 (même clé, 11 images) ; la valeur repart à 0.5 (10 cases pleines sur 20) à f - 1 PUIS dérive vers 1
  jusqu'à 2088 (69,6 s) ; kit.pop("temps_20", f) en TEMPS_LONG_20_C ; b10 0.1 -> 0 et b9 1 -> 0.37 sur la même
  dérive. « l’érosion » (2074) : kit.drop("b10", f, out=True, h=120, rot=12) ; kit.draw vide10 et vide9 (8 images).
  « importante. » (2106) : vide9/vide10 pulse (times=2, step=2, peak=1.15) ; kit.shake("panier", f, amp=6).
- S17 (2142-2216) « Alors » (2142) : c.toi.unstow(f) ; c.toi.reach(f, SEP_A, d=12). « sépare » (2162) :
  c.toi.trace(f, [SEP_A, SEP_PEN_B]) (la pointe monte de 65 px) et kit.draw("separateur", f, DRAW) : la ligne part
  de la pointe et file seule jusqu'en (530, 390). « horizons. » (2193) : la barre se fend en x 530 : relais
  kit.morph("temps_long", ["court", "long"], f, pair=False) À LA MÊME PLACE (court en COURT_CUT, long en LONG_CUT,
  barres pleines sans cases), puis kit.move court -> COURT_C, long -> LONG_C (MOVE) ; kit.fade temps_auj, temps_10,
  temps_20 vers 0 ; kit.pop court_mot et long_mot (f + 8) ; la main redescend (lower) après le trait.
- S18 (2217-2334) « court » (2222) : S.key("court", "fill", f, CYAN, 9) ; S.key("court_mot", "color", f, DEEP, 9) ;
  bouee et valise pulse (times=2, step=2, peak=1.06). « sécurité » (2260) : bouclier posé en BOUCLIER_S18 (pos d=0 à
  f - 1) puis kit.pop("bouclier", f, scale=BOUCLIER_S18_K). « et » (2284) : kit.pop("imprevu", f, d=6) en IMPREVU_C ;
  kit.shake("imprevu", f + 6, amp=4). « disponibilité. » (2294) : billet3 (haut de la pile) saute en arc sur l'imprévu
  (kit.move(…, IMPREVU_C, d=9, e="out", arc=50)) ; billet3 et imprevu pulse puis kit.vanish ensemble (9 images) : la
  bouée garde 2 billets.
- S19 (2335-2537) « long » (2340) : long fill -> CYAN, long_mot -> DEEP ; court fill -> LIGHT, court_mot -> INK (9).
  « cherche » (2366) : kit.vanish berceau et zzz1-3 (les 5 billets restent). « progresser » (2386) :
  kit.pop("arbre", f, scale=ARBRE_S19_K) en ARBRE_C ; billet6-10 -> PILE_ARBRE, échelle 1 (11 images) ; relais en
  fondu role_vide (+ _mot) -> role_progresser (opacity 1 -> 0 / scale 1 ; FADE). « argent » (2409) :
  kit.pop("billet_arbre", f, from_pt=BILLET_ARBRE_FROM) puis kit.drop vers BILLET_ARBRE_C (ou move 11 images, out).
  « aussi » (2437) : la pile (billet6-10 + billet_arbre) et l'étiquette battent ensemble (times=2, step=3, peak=1.1).
  « prix. » (2465) : b10 : scale 1, opacité 1, value 1, rot 0 et kit.drop("b10", f) à sa place (entrée) ; b9 value
  0.37 -> 1 (9 images) ; vide9/vide10 draw -> 0. « Mais » (2490) : kit.vanish panier (enfants avec lui), etiquette,
  ficelle_panier draw -> 0. « acceptant » (2499) : kit.draw("courbe", f, 20). « risque. » (2518) :
  kit.pop("courbe_creux", f) + pulse (times=2, step=2, peak=1.3) ; la pile des 6 billets descend de 30 px puis
  remonte (6 + 10 images).
- S20 (2538-2687) « Garder » (2538) : kit.vanish courbe, courbe_creux, bouclier ; piles bouée (billet1-2) et valise
  (billet4-5) pulse (times=2, step=2, peak=1.1). « utilité. » (2579) : kit.draw("role_imprevus_mot", f, 9,
  track="under") puis role_projet_mot à f + 4. « rôle » (2620) : kit.stagger([role_imprevus, role_projet,
  role_progresser], f, 4, kit.pulse, peak=1.12). « durée » (2645) : duree1-3 naissent des légendes (posées en
  COURT_MOT_C / LONG_MOT_C, échelle 1 à f - 1 ? non : pop depuis la légende, puis move vers leur place DUREES, 11
  images, kit.stagger 3).
- S21 (2688-2785) « problème » (2693) : berceau à BERCEAU_LOW, échelle BERCEAU_LOW_K, drop_in (vide). « n’est »
  (2707) : piles bouée et valise + role_imprevus / role_projet pulse ensemble (times=2, step=2, peak=1.1).
  « cash. » (2720) : kit.pop("billet_dort", f, from_pt="cash", to=BILLET_DORT_C, scale=BILLET_DORT_K, d=MOVE)
  (arc : kit.move). « C’est » (2738) : kit.draw("role_dort", f, 8) + role_dort_mot opacité 1 ; billet_dort fill
  CYAN -> RED, role_dort stroke INK -> RED, role_dort_mot color INK -> RED (5 images) ; kit.shake("billet_dort",
  f + 6, amp=5). Tenue jusqu'à 2785 (1,6 s).
- S22 (2786-2872) « Abonne-toi » (2786) : kit.outro("S22", outs=[tout sauf cash, toi], press="argent.",
  btn_at=…) ; c.toi.exit(f) ; la pilule « cash » quitte la carte (monde) : textOp 1 -> 0, text -> T_ABONNER,
  textOp -> 1 (FADE), move vers FIN_BUTTON et w / échelle jusqu'au bouton (380 x 112) ; relais par btn_at.
  S.set(out["cursor"], opacity=0) (pas de flèche de souris). « comprendre » (2811) : kit.pop("fin_doigt", f, to=FIN_TAP)
  (glisse vers le bas droit du bouton, hors du libellé). « argent. » (2834, clic de l'outro) : fin_doigt scale 0.8
  puis vanish ; ring(S, "fin_onde1"/"fin_onde2", fp + 4 k, d=14, s0=0.6, s1=2.1). Plus rien ne bouge ensuite.
"""
from . import *  # noqa: F401,F403
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, SCALE, STRETCH, TILT  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401


PANIER_SINK, SINK_BACK = 24, 14                # S15 « pèse » : le panier s'enfonce de 24 px, remonte en 450 ms
ETIQ_DROP_H = 150                               # S15 « pèse » : l'étiquette tombe de 150 px (et non 240 : elle
                                                # traverserait le berceau)
SPLIT = 6                                       # S17 « horizons. » : chaque morceau s'écarte de 6 px (fente de 12)
B10_DROP_H = 100                                # S19 « prix. » : b10 retombe de 100 px (repère du panier, x 0,8)
PILE_DIP, PILE_RISE = 30, 50                    # S19 « risque. » : la pile descend de 30 px puis remonte de 50
COURBE_CREUX_FRAC = 0.68                        # part de la longueur de la courbe jusqu'au creux
FIN_K = 112 / CASH_H                            # S22 : pilule 250 x 80 -> bouton 380 x 112 (x 1,4)
FIN_W = round(380 / FIN_K, 2)                   # largeur de pilule qui donne 380 px à l'échelle FIN_K
FIN_BSIZE = round(48 * FIN_K, 1)                # corps du libellé du bouton = celui de la pilule agrandie
# Écart de place (p3) : la pile de l'arbre monte de 11 px par billet (et non 6) depuis (700, 636) : à 6 px, les 6
# billets se lisaient comme un seul billet sur un socle noir ; le 6e se pose en (700, 581) (et non 590).
PILE_ARBRE_P3 = [(700, 636 - 11 * k) for k in range(5)]
BILLET_ARBRE_P3 = (700, 636 - 11 * 5)
# Écart de place (p3) : le libellé « S’abonner » du bouton (ExtraBold 67, x 370-710, y ≈ 884-932) couvrait FIN_TAP
# (684, 944) ; le doigt touche le bas du bouton, sous la fin du libellé.
FIN_TAP_P3 = (700, 962)
FIN_DOIGT_FROM = (FIN_TAP_P3[0] + 90, FIN_TAP_P3[1] + 90)
PEN_S21 = (598, 902)                            # S21 « C’est » : la pointe vise le billet rouge du berceau
assert_reach(TOI_P2[0], PEN_S21, "S21 pointe vers le billet rouge")
# S20 « durée » : un fil de chaque pile à son morceau de barre (Court : x 250-330 ; Long : x 540-860 ; bas y 320)
FILS_DUREE = [("fil_court1", (232, 598), (272, 322), "court", "duree1"),
              ("fil_court2", (398, 598), (312, 322), "court", "duree2"),
              ("fil_long", (742, 556), (742, 322), "long", "duree3")]


def part(S, kit, c):
    toi = c.toi
    f0 = scene_f0(S, "S15")                     # 1863
    kit.pin(f0 - 1, ENTRY_P3)                   # etat_initial de S15 = résultat de S14
    if S.val("toi", "scale", f0 - 1) == 0:      # partie construite seule (WTH_PARTS) : « Toi » n'est pas entré
        toi.enter(f0 - 12, at=TOI_P2)
        toi.stow(f0 - 9, d=2)
        toi.lower(f0 - 8)

    pile_berceau = BILLETS[5:10]                 # billet6-10 : l'argent qui dort (S14-S19)
    arts = ARTICLES[5:10]                        # b6-b10 : le panier qu'il achète

    # ================= S15 : l'inflation pèse sur l'argent qui dort longtemps =================
    f = kit.at("S15", "L’inflation", "un panier sort du berceau et se pose dessous ; ses 5 articles apparaissent un "
                                     "à un, chacun quand un billet du berceau bat")
    kit.pop("panier", f, scale=PANIER_LOW_K, from_pt=PILE_BERCEAU[0], to=list(PANIER_LOW), d=MORPH)
    for k, (b, a) in enumerate(zip(pile_berceau, arts)):
        g = f + 5 + 3 * k
        kit.pop(a, g, d=6)
        kit.pulse(b, g, peak=round(PILE_BERCEAU_K * 1.2, 3), step=3)

    f = kit.at("S15", "pèse", "l’étiquette des prix (« +2 % ») tombe accrochée au coin du panier, sa pilule "
                              "« inflation » au-dessus ; le panier s’enfonce nettement puis remonte lentement ; "
                              "l’étiquette bat")
    S.key("etiquette", "pos", f - 1, list(ETIQ_LOW))
    S.key("etiquette", "scale", f - 1, ETIQ_LOW_K)
    S.key("etiquette", "rot", f - 1, 0)
    drop_in(kit, "etiquette", f, h=ETIQ_DROP_H)
    S.key("ficelle_panier", "bAt", f - 1, [170, -85])
    kit.draw("ficelle_panier", f + 3, 7)
    S.key("taux", "pos", f - 1, list(TAUX_LOW))
    S.key("taux", "text", f - 1, T_INFL)
    S.key("taux", "w", f - 1, W_INFL)
    kit.pop("taux", f + 4)
    land = f + DROP                             # l'étiquette touche : le panier, elle et sa pilule plongent
    for id, p0 in (("panier", PANIER_LOW), ("etiquette", ETIQ_LOW), ("taux", TAUX_LOW)):
        S.key(id, "pos", land, [p0[0], p0[1] + PANIER_SINK], 6, "out")
        S.key(id, "pos", land + 6, list(p0), SINK_BACK, "inOut")
    kit.pulse("etiquette", land, peak=round(ETIQ_LOW_K * 1.15, 3), step=3)
    g = S.word_after("l’argent", f)             # « l’argent dont tu n’as pas besoin » : les billets qui dorment
    for k, b in enumerate(pile_berceau):
        kit.pulse(b, g + 2 * k, step=2, peak=round(PILE_BERCEAU_K * 1.15, 3))

    f = kit.at("S15", "longtemps,", "la barre du temps s’étire en haut (10 cases vides) ; « aujourd’hui » et "
                                    "« 10 ans » s’inscrivent à ses bouts")
    kit.ensure("temps_long", "w", TEMPS_LONG_W0)
    x0 = TEMPS_LONG_C0[0] - TEMPS_LONG_W0 / 2   # bord gauche de la barre (450)
    S.key("temps_long", "value", f - 1, 0)
    S.key("temps_long", "w", f - 1, 20)
    S.key("temps_long", "pos", f - 1, [x0 + 10, TEMPS_LONG_C0[1]])
    S.key("temps_long", "scale", f, 1)
    S.key("temps_long", "w", f, TEMPS_LONG_W0, STRETCH, "out")
    S.key("temps_long", "pos", f, list(TEMPS_LONG_C0), STRETCH, "out")
    S.key("temps_auj", "pos", f - 1, [TEMPS_LONG_AUJ_END_X, TEMPS_LONG_C0[1]])
    w10 = text_width(T_10ANS, 34, 700)
    S.key("temps_10", "pos", f - 1, [round(TEMPS_LONG_10_C[0] - w10 / 2, 1), TEMPS_LONG_10_C[1]])
    kit.ensure("temps_10", "under", 0)
    S.key("temps_10", "under", f - 1, 0)        # le soulignement de S09 ne revient pas
    for t in ("temps_auj", "temps_10"):
        S.key(t, "scale", f - 1, 1)
        S.key(t, "opacity", f - 1, 0)
        kit.fade(t, f + 2)

    f = kit.at("S15", "immobile.", "les trois « z » battent l’un après l’autre ; les billets restent couchés")
    kit.stagger([z[0] for z in ZZZ], f, 3, kit.pulse, peak=1.15)

    # ================= S16 : sur 10 puis 20 ans, le panier se vide =================
    f = kit.at("S16", "10", "les 10 cases se remplissent ; l’étiquette bat ; le dernier article se vide presque")
    S.key("temps_long", "value", f, 1, 9, "linear")
    kit.pulse("etiquette", f, peak=round(ETIQ_LOW_K * 1.1, 3), step=2)
    S.key("b10", "value", f, 0.1, 9, "linear")

    f = kit.at("S16", "20 ans,", "la barre s’allonge à 20 ans et continue de se remplir ; « 20 ans » surgit ; le "
                                 "dernier article se vide, l’avant-dernier aux deux tiers")
    drift_end = S.word_after("devient", f) - 5  # fin de la dérive juste avant « devient »
    kit.ensure("temps_long", "w", TEMPS_LONG_W0)
    S.key("temps_long", "w", f, TEMPS_LONG_W1, MORPH, "out")
    S.key("temps_long", "pos", f, list(TEMPS_LONG_C1), MORPH, "out")
    for n in range(f, drift_end + 1):           # cases pleines gardées pendant l'allongement, puis dérive linéaire
        drift = 0.5 + 0.5 * (n - f + 1) / (drift_end - f + 1)
        v = max(TEMPS_LONG_W0 / S.val("temps_long", "w", n), drift)
        S.key("temps_long", "value", n, round(min(v, 1), 4), 1, "linear")
    kit.pop("temps_20", f)
    S.key("b10", "value", f, 0, drift_end - f + 1, "linear")
    S.key("b9", "value", f, 0.37, drift_end - f + 1, "linear")

    f = kit.at("S16", "l’érosion", "le dernier article, vide, tombe hors du panier ; deux carrés en tirets rouges "
                                   "marquent sa place et l’avant-dernier")
    kit.drop("b10", f, out=True, h=120, rot=12)
    for v in ("vide10", "vide9"):
        S.key(v, "scale", f - 1, 1)
        kit.draw(v, f + 2, 8)

    f = kit.at("S16", "importante.", "les carrés rouges battent ; le panier tremble")
    kit.pulse("vide9", f, times=2, step=2, peak=1.15)
    kit.pulse("vide10", f, times=2, step=2, peak=1.15)
    kit.shake("panier", f, amp=6)

    # ================= S17 : « Toi » sépare les horizons =================
    f = kit.at("S17", "Alors", "« Toi » sort son stylo et en pose la pointe entre la carte et le panier")
    toi.unstow(f)
    toi.reach(f, SEP_A, d=12)

    f = kit.at("S17", "sépare", "« Toi » tire la pointe vers le haut : une ligne deep part du stylo et file jusqu’en "
                                "haut, à travers la barre du temps, entre la bouée / valise et le berceau / panier")
    hits = toi.trace(f + 1, [SEP_A, SEP_PEN_B])
    kit.draw("separateur", max(hits[0], f + 1), DRAW)

    f = kit.at("S17", "horizons.", "la barre du temps se fend là où la ligne la croise ; le petit morceau va à gauche "
                                   "(« Court »), le grand à droite (« Long ») ; chaque morceau bat avec ses objets ; "
                                   "« Toi » range son stylo")
    S.key("temps_long", "scale", f, 0)          # relais à la même place : deux barres pleines sans cases
    for gid, cut, dx, dest in (("court", COURT_CUT, -SPLIT, COURT_C), ("long", LONG_CUT, SPLIT, LONG_C)):
        S.key(gid, "pos", f - 1, list(cut))
        S.key(gid, "value", f - 1, 1)
        S.key(gid, "scale", f, 1)
        S.key(gid, "pos", f, [cut[0] + dx, cut[1]], 4, "out")
        kit.move(gid, f + 5, list(dest), d=10)
    for t in ("temps_auj", "temps_10", "temps_20"):
        kit.fade(t, f, to=0)
    kit.pop("court_mot", f + 8)
    kit.pop("long_mot", f + 8)
    g = f + 15                                  # les morceaux sont en place : la longueur de la barre = la durée
    for id in ["court", "bouee", "valise"] + BILLETS[0:5]:
        kit.pulse(id, g, step=2)
    for id in ["long", "berceau", "panier"] + pile_berceau:
        kit.pulse(id, g + 4, step=2)
    toi.lower(f + 2)
    toi.stow(f + 2)                             # stylo rangé : sa pointe ne touche plus les sous-titres

    # ================= S18 : court terme = sécurité et disponibilité =================
    f = kit.at("S18", "court", "le morceau « Court » devient cyan ; la bouée et la valise battent")
    S.key("court", "fill", f, CYAN, POP, "out")
    S.key("court_mot", "color", f, DEEP, POP, "out")
    kit.pulse("bouee", f, times=2, step=2, peak=1.06)
    kit.pulse("valise", f, times=2, step=2, peak=1.06)

    f = kit.at("S18", "sécurité", "le disque bouclier ressort de la bouée et se pose entre la bouée et la valise")
    S.key("bouclier", "rot", f - 1, 0)
    kit.pop("bouclier", f, scale=BOUCLIER_S18_K, from_pt="bouee", to=list(BOUCLIER_S18), d=MORPH)

    f = kit.at("S18", "et", "un grand disque « ⚠ » (imprévu) surgit sous « Imprévus » et tremble")
    S.key("imprevu", "pos", f - 1, list(IMPREVU_C))
    g = kit.pop("imprevu", f, d=6)
    kit.shake("imprevu", g, amp=6)

    f = kit.at("S18", "disponibilité.", "le billet du haut de la pile de la bouée saute en arc haut sur l’imprévu ; "
                                        "les deux battent, puis le « ⚠ » rentre dans le billet et ils disparaissent "
                                        "ensemble : la pile passe de 3 à 2 billets")
    kit.ensure("billet3", "z", S.ents["billet3"]["z"])
    S.key("billet3", "z", f, 10.9)              # passe SOUS la pilule « Imprévus »
    g = kit.move("billet3", f, list(IMPREVU_C), d=12, e="out", arc=120)
    up = next((n for n in range(f, g) if S.val("billet3", "pos", n)[1] > ROLE_IMPREVUS_C[1] + ROLE_H / 2 + 20), g)
    S.key("billet3", "z", up, 12.4)             # puis au-dessus du disque
    kit.pulse("billet3", g, peak=1.15, step=3)
    h = kit.pulse("imprevu", g, peak=1.15, step=3)
    kit.vanish("imprevu", h, into="billet3", d=9)
    kit.vanish("billet3", h, d=9)

    # ================= S19 : long terme = progresser, avec un risque =================
    f = kit.at("S19", "long", "le morceau « Long » devient cyan ; « Court » revient au bleu pâle")
    S.key("long", "fill", f, CYAN, POP, "out")
    S.key("long_mot", "color", f, DEEP, POP, "out")
    S.key("court", "fill", f, LIGHT, POP, "out")
    S.key("court_mot", "color", f, INK, POP, "out")

    f = kit.at("S19", "cherche", "le berceau se réduit pendant que l’arbre grandit à sa place (un seul relais) ; "
                                 "les « z z z » s’éteignent ; les 5 billets restent")
    kit.vanish("berceau", f, d=MORPH)
    S.key("arbre", "pos", f - 1, list(ARBRE_C))
    kit.pop("arbre", f, scale=ARBRE_S19_K, d=MORPH)
    for zid, _, _ in ZZZ:
        kit.vanish(zid, f)

    f = kit.at("S19", "progresser", "les 5 billets descendent aux racines de l’arbre et s’y empilent ; le « ? » "
                                    "devient « Progresser »")
    for b, p in zip(pile_berceau, PILE_ARBRE_P3):
        kit.move(b, f + 2, list(p), d=MORPH, scale=1)
        S.key(b, "rot", f + 2, 0, MORPH, "inOut")
    kit.fade("role_vide", f + 4, to=0)
    kit.vanish("taux", f + 4)                   # la pilule « inflation » libère la place de « Progresser »
    S.key("role_progresser", "scale", f + 3, 1)
    S.key("role_progresser", "opacity", f + 3, 0)
    kit.fade("role_progresser", f + 4)

    f = kit.at("S19", "argent", "un 6e billet sort du feuillage et tombe sur la pile : l’argent grandit")
    S.key("billet_arbre", "pos", f - 1, list(BILLET_ARBRE_FROM))
    g = kit.pop("billet_arbre", f, d=6)
    kit.move("billet_arbre", g, list(BILLET_ARBRE_P3), d=DROP, e="out")

    f = kit.at("S19", "aussi", "la pile de 6 billets et l’étiquette des prix battent ensemble, deux fois")
    pile6 = pile_berceau + ["billet_arbre"]
    for b in pile6:
        kit.pulse(b, f, times=2, step=3, peak=1.1)
    kit.pulse("etiquette", f, times=2, step=3, peak=round(ETIQ_LOW_K * 1.1, 3))

    f = kit.at("S19", "prix.", "l’avant-dernier article se remplit, puis le dernier retombe à sa place ; les tirets "
                               "rouges s’effacent ; le panier plein et son étiquette battent ensemble")
    S.key("b9", "value", f, 1, 9, "out")
    kit.draw("vide9", f, 6, to=0)
    S.key("vide9", "scale", f + 6, 0)
    g = f + 4
    S.key("b10", "rot", g - 1, 0)
    S.key("b10", "value", g - 1, 1)
    drop_in(kit, "b10", g, h=B10_DROP_H, to=list(ART_LOCAL[9]))
    kit.draw("vide10", g, 6, to=0)
    S.key("vide10", "scale", g + 6, 0)
    full = g + DROP
    kit.pulse("panier", full, step=3, peak=round(PANIER_LOW_K * 1.1, 3))
    kit.pulse("etiquette", full, step=3, peak=round(ETIQ_LOW_K * 1.1, 3))

    f = kit.at("S19", "Mais", "l’étiquette se réduit ; le panier plein reste encore un instant")
    kit.vanish("etiquette", f)
    kit.draw("ficelle_panier", f, 4, to=0)

    f = kit.at("S19", "acceptant", "relais : le panier se réduit pendant qu’une courbe deep monte en zigzag à sa place, "
                                   "jusqu’à un creux")
    kit.vanish("panier", f)
    S.key("courbe", "scale", f - 1, 1)
    S.key("courbe", "draw", f - 1, 0)
    kit.draw("courbe", f, 14, to=COURBE_CREUX_FRAC, e="linear")

    f = kit.at("S19", "risque.", "un point rouge se pose dans le creux et bat ; la pile de billets descend un instant ; "
                                 "puis la courbe repart au-dessus du creux et finit plus haut, et la pile remonte plus "
                                 "haut qu’avant")
    kit.pop("courbe_creux", f)
    kit.pulse("courbe_creux", f + POP, times=2, step=2, peak=1.3)
    kit.draw("courbe", f + 6, 10, e="out")
    for b in pile6:
        x, y = S.val(b, "pos", f - 1)
        S.key(b, "pos", f, [x, y + PILE_DIP], 6, "out")
        S.key(b, "pos", f + 6, [x, y + PILE_DIP - PILE_RISE], 12, "inOut")

    # ================= S20 : chaque paquet de cash a un rôle et une durée =================
    f = kit.at("S20", "Garder", "la courbe, son point rouge et le bouclier se réduisent ; les billets de la bouée et "
                                "de la valise battent")
    for id in ("courbe", "courbe_creux", "bouclier"):
        kit.vanish(id, f)
    for b in ("billet1", "billet2", "billet4", "billet5"):
        kit.pulse(b, f, times=2, step=2, peak=1.1)

    f = kit.at("S20", "utilité.", "« Imprévus » puis « Projet » se soulignent")
    kit.draw("role_imprevus_mot", f, POP, track="under")
    kit.draw("role_projet_mot", f + 4, POP, track="under")

    f = kit.at("S20", "rôle", "les trois pilules de rôle battent l’une après l’autre")
    kit.stagger(["role_imprevus", "role_projet", "role_progresser"], f, 4, kit.pulse, peak=1.12)

    f = kit.at("S20", "durée", "un fil deep se tire de chaque pile (bouée, valise, arbre) jusqu’à son morceau de "
                               "barre, qui bat ; puis une pilule « Court » ou « Long » se pose sous chaque rôle")
    dests = {did: dest for did, _, dest in DUREES}
    for k, (wid, a, b, piece, did) in enumerate(FILS_DUREE):
        g = f + 5 * k
        S.key(wid, "pa", g - 1, list(a))
        S.key(wid, "pb", g - 1, list(b))
        h = kit.draw(wid, g, DRAW)
        kit.pulse(piece, h, step=2, peak=1.15)
        S.key(did, "pos", h, list(dests[did]))  # la durée se pose sous le rôle, une fois le fil tiré
        kit.pop(did, h + 1)

    # ================= S21 : le cash sans mission =================
    f = kit.at("S21", "problème", "les fils se retirent ; le berceau revient, vide, à cheval sur le bas de la ligne, "
                                  "entre les deux colonnes")
    for wid, *_ in FILS_DUREE:
        kit.draw(wid, f, 6, to=0)
    kit.ensure("separateur", "z", S.ents["separateur"]["z"])
    S.key("separateur", "z", f, 4.9)            # la ligne passe derrière le berceau
    S.key("berceau", "pos", f - 1, list(BERCEAU_LOW))
    S.key("berceau", "scale", f - 1, BERCEAU_LOW_K)
    drop_in(kit, "berceau", f)

    f = kit.at("S21", "n’est", "une coche deep se trace à côté de chaque pile qui a un rôle ; les billets de la bouée "
                               "et de la valise battent avec « Imprévus » et « Projet »")
    for k, (cid, _) in enumerate(COCHES):
        kit.draw(cid, f + 3 * k, 6)
    for id in ("billet1", "billet2", "billet4", "billet5", "role_imprevus", "role_projet"):
        kit.pulse(id, f, times=2, step=2, peak=1.1)

    f = kit.at("S21", "cash.", "un billet sort de la pilule « 10 000 € » et vole se coucher dans le berceau")
    S.key("billet_dort", "pos", f - 1, list(CASH_LOW))
    kit.pop("billet_dort", f, scale=BILLET_DORT_K)
    kit.move("billet_dort", f, list(BILLET_DORT_C), arc=80)

    f = kit.at("S21", "C’est", "« Toi » sort son stylo et en pointe le billet ; un « ? » en tirets se trace à côté du "
                               "berceau ; le billet et le « ? » virent au rouge ; le billet tremble : un cash sans "
                               "mission")
    toi.unstow(f)
    toi.reach(f, PEN_S21, d=9)
    S.key("role_dort", "scale", f - 1, 1)
    kit.draw("role_dort", f, 8)
    kit.fade("role_dort_mot", f + 2)
    g = f + 6
    S.key("billet_dort", "fill", g, RED, 5, "out")
    S.key("role_dort", "stroke", g, RED, 5, "out")
    S.key("role_dort_mot", "color", g, RED, 5, "out")
    kit.shake("billet_dort", g + 6, amp=5)

    # ================= S22 : la pilule devient le bouton « S’abonner » =================
    fe = scene_f0(S, "S22")
    outs, wires = [], []
    for id, e in S.ents.items():                # tout ce qui est encore à l'écran, sauf la pilule et « Toi »
        if e.get("parent") or id == "cash" or id.startswith("toi") or id.startswith("fin"):
            continue
        if S.val(id, "scale", fe - 1) < 1e-3 or S.val(id, "opacity", fe - 1) < 1e-2:
            continue
        if e["type"] == "wire":
            if S.val(id, "draw", fe - 1, 0) > 0:
                wires.append(id)
            continue
        outs.append(id)
    out = kit.outro("S22", outs=outs, press="argent.", btn_at=MOVE, bsize=FIN_BSIZE)
    f = out["card"]
    toi.exit(f)
    for w_id in wires:
        S.key(w_id, "opacity", f, 0, FADE, "linear")
    kit.ensure("cash", "z", S.ents["cash"]["z"])
    S.key("cash", "z", f, 41)                   # au-dessus de la carte (z 40)
    S.key("cash", "textOp", f, 0, 3, "out")
    S.key("cash", "text", f + MOVE // 2, T_ABONNER)   # le libellé change quand la pilule est assez large
    S.key("cash", "textOp", f + MOVE // 2, 1, FADE, "out")
    S.key("cash", "w", f, FIN_W, MOVE, "inOut")
    kit.move("cash", f, list(FIN_BUTTON), scale=round(FIN_K, 4))
    S.key("cash", "opacity", f + MOVE, 0)       # relais : le bouton de la carte paraît dessous (btn_at)
    S.set(out["cursor"], opacity=0)             # pas de flèche de souris : un toucher au doigt

    g = kit.at("S22", "comprendre", "un doigt glisse jusqu’au coin bas droit du bouton « S’abonner »")
    S.key("fin_doigt", "pos", g - 1, list(FIN_DOIGT_FROM))
    kit.pop("fin_doigt", g, to=list(FIN_TAP_P3), d=MORPH)
    fp = out["press"]
    S.key("fin_doigt", "scale", fp, 0.8, 2, "out")
    kit.vanish("fin_doigt", fp + 5, d=5)
    for k in range(2):
        S.key(f"fin_onde{k + 1}", "pos", fp - 1, list(FIN_TAP_P3))
        ring(S, f"fin_onde{k + 1}", fp + 4 * k, d=14, s0=0.6, s1=2.1)
    assert fp + 4 + 14 < film_end(S), (fp, film_end(S))
