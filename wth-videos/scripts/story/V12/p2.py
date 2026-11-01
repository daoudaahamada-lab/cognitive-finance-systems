"""V12, partie 2 : S09-S14, images 970-1862 (30 temps forts, 29,8 s). ≈ 8 200 € en euros d'aujourd'hui, « toujours »
10 000 € (la perte invisible), grand relais vers les billets (S11), bouée / valise, bascule, berceau.

ÉTAT D'ENTRÉE : ENTRY_P2 épinglé à 969 (`kit.pin(f0 - 1, ENTRY_P2)`, f0 = scene_f0(S, "S09") = 970) : etat_initial
de S09 = résultat de S08 (barre des 10 ans pleine ; b5 vide, b4 au cinquième ; « pouvoir d’achat 8 200 € » ;
« ◀◀ exemple » ; étiquette « + 2 % / an » et pilule « inflation » au-dessus du panier ; carte « Solde » « 10 000 € » et
« intérêts : 0 € » ; fil deep tendu). Garde-fou de partie isolée (sans effet dans le film entier) :
`if S.val("toi", "scale", f0 - 1) == 0: c.toi.enter(f0 - 12, at=TOI_P1); c.toi.stow(f0 - 9, d=2); c.toi.lower(f0 - 8)`.
SORTIE : ENTRY_P3 à l'image 1862 (voir __init__.py). Tout ce que cette partie commence finit avant 1863.

Ids : temps, temps_10 (under), panier, b1-b10, vide4, vide5, pouvoir_val, pouvoir_approx, pouvoir_note, mention
(+ mention_ico), regard, cash, cercle, toujours, compte, interets, lien, etiquette, taux, ficelle_panier, temps_auj,
pouvoir_titre, billet1-10, arbre, question, toi, bouee, valise, role_imprevus (+ _mot), role_projet (+ _mot),
bascule, bouclier, pourcent, stabilite, rendement, berceau, zzz1-3, role_vide (+ role_vide_mot).

TOUR DE REVUE 1 (prime sur le brief ci-dessous quand ils diffèrent) : S10 cône du regard, « exemple illustratif » se
range sur « Pourtant », « toujours » : mini-barre de 10 ans sous la carte + solde qui roule 9 999 -> 10 000 €,
« invisible. » : la perte rebat hors du cône ; S11 « Face » : panier, étiquette et pilule rentrent dans la pilule du
solde, « intérêts : 0 € » se range, « Solde » garde 34 px ; « placer. » : pilule « tout » avec les billets ; « Non. » :
contact du stylo sur le mot, « tout » barré, billets arrêtés net (shake) puis retour ; S12 : billets un à un, piles en
escalier, vaguelette sous la bouée, pilule de rôle à l'arrivée ; S13 : bouclier ×1,5 cyan, % ×0,8, bascule -20° puis
-18°, sur « rendement. » bouée, valise et bouclier battent et deux fils deep relient le bouclier aux deux rôles ;
S14 : le bouclier rentre dans la bouée, billets du berceau en éventail, tout posé avant « raison. ».

BRIEF, scène par scène :
- S09 (970-1190) « fin, » (979) : kit.pulse("temps", f, step=2, peak=1.2) n'agrandit que la barre : préférer un
  battement de la dernière case (petit carré light posé sur la case 10, ou pulse de la barre entière à 1,05) ;
  kit.draw("temps_10", f, 9, track="under"). « achètent » (1000) : kit.drop("b5", f, out=True, h=160, rot=12) ;
  kit.draw("vide5", f + 2, 8) et kit.draw("vide4", f + 2, 8). « l’équivalent » (1016) : les 8 articles pleins
  (b1-b3, b6-b10) puis b4 battent l'un après l'autre (kit.stagger(…, f, 2, kit.pulse, peak=1.12, step=2)).
  « 8 200 € » (1055) : kit.pop("pouvoir_approx", f) ; kit.pulse("pouvoir_val", f, times=2, step=3, peak=1.15).
  « d’aujourd’hui. » (1082) : kit.fade("pouvoir_note", f). « exemple » (1143) : kit.vanish("mention_ico", f, d=6) ;
  mention text -> T_EXEMPLE_ILL et w -> W_EXEMPLE_ILL (POP, out).
- S10 (1191-1345) « Pourtant, » (1191) : kit.draw("regard", f, DRAW). « solde » (1217) : kit.pulse("cash", f,
  times=2, step=3, peak=1.1). « toujours » (1240) : kit.draw("cercle", f, DRAW) ; kit.type("toujours", f, rate=2).
  « perte » (1298) : kit.pulse vide4 et vide5 (times=2, step=2, peak=1.15), pouvoir_val (peak=1.1) ;
  kit.shake("panier", f, amp=5). « invisible. » (1315) : kit.hold ; rien ne bouge sur la carte.
  Pas de rouge sur la carte ; l'ellipse est à l'encre (pas deep : « bonne nouvelle » refusé par le test sans son).
- S11 (1346-1489) « Face » (1346) : kit.morph([panier, etiquette, taux, pouvoir_titre, pouvoir_val, pouvoir_approx,
  pouvoir_note, mention, temps, temps_auj, temps_10, cercle, toujours], [], f, pair=False) ; lien et regard
  draw -> 0 (from ou draw), ficelle_panier draw -> 0 ; carte : kit.move("compte", f, COMPTE_LOW,
  scale=COMPTE_LOW_K) et kit.move("cash", f, CASH_LOW, scale=COMPTE_LOW_K) (même clé). Pendant que le panier est caché
  (après f + MORPH) : b1-b10 scale 0, value 1, fill LIGHT, opacité 1 ; vide4/vide5 scale 0 ; etiq_prix opacité 0 /
  etiq_taux 1 (déjà) : c'est ENTRY_P3. « envie » (1377) : 10 billets naissent de la pilule et se rangent en
  BILLET_ROWS (kit.stagger(BILLETS, f, 2, kit.pop, from_pt="cash") avec `to` = leur place, ou pop puis move 350 ms).
  « placer. » (1396) : drop_in(kit, "arbre", f) en ARBRE_C ; tous les billets glissent ensemble vers ARBRE_ROWS
  (MOVE inOut). « Mais » (1424) : c.toi.walk(f, TOI_P2[0]) (≈ 22 images). « cash ? » (1455) : c.toi.unstow(f - 6) puis
  c.toi.reach vers la pilule ; kit.pop("question", f, from_pt=c.toi.tip(f - 1), to=QUESTION_S11).
  « Non. » (1469) : contact sur le mot : c.toi.tap(f - TAP + 1, CASH_TAP) ; kit.vanish("question", f, d=6) ; les 10
  billets reviennent en BILLET_ROWS (MOVE, arc 60) ; l'arbre ne bouge pas. Bras ensuite baissé (lower).
- S12 (1490-1651) « L’argent » (1490) : les 10 billets battent ensemble (pulse peak=1.1, times=2, step=2).
  « faire » (1549) : drop_in(kit, "bouee", f) en BOUEE_C. « imprévus, » (1571) : billet1-3 volent en arc vers
  PILE_BOUEE (kit.stagger 3 images, MOVE, arc 60 ; billet3 en haut de la pile) ; kit.pop("role_imprevus", f + 6).
  « financer » (1600) : drop_in(kit, "valise", f) en VALISE_C. « projet » (1618) : billet4-5 -> PILE_VALISE (idem) ;
  kit.pop("role_projet", f + 6). Restent billet6-10 en rangée y 935 ; l'arbre reste, vide.
- S13 (1652-1755) « Pour » (1652) : kit.pop("bascule", f) (à plat, pivot BASCULE_C) ; « bouclier » naît de la bouée
  (kit.pop(…, from_pt=BOUEE_C, to=BOUCLIER_SEAT, d=MOVE)) ; kit.pop("stabilite", f + 6). « ça, » (1660) : « pourcent »
  naît de l'arbre (from_pt=ARBRE_C, to=POURCENT_SEAT) ; kit.pop("rendement", f + 6). « stabilité » (1674) :
  S.key("bouclier", "scale", f, 1.25, 10, "out") puis kit.pulse. « compte » (1695) : S.key("bascule", "rot", f,
  BASCULE_TILT, TILT, "out") ; les disques et leurs légendes (entités monde) suivent la planche par
  S.path(id, f, TILT, "out", lambda p: rotate_about(seat, BASCULE_TILT * p, BASCULE_C)) (rotate_about de
  pipeline.story_kit ; même assouplissement que la clé rot) ; « rendement » finit vers (830, 686). Tenue.
- S14 (1756-1862) « sujet, » (1767) : kit.vanish bascule, bouclier, pourcent, stabilite, rendement, arbre (relais,
  300 ms) ; billet6-10 battent (pulse peak=1.12, times=2, step=2). « l’argent » (1805) : drop_in(kit, "berceau", f) en
  BERCEAU_C. « dort » (1824) : billet6-10 volent en arc dans le berceau, PILE_BERCEAU, échelle PILE_BERCEAU_K
  (kit.stagger 2 images, MOVE) ; zzz1-3 montent (kit.stagger 3 images : pop 20 px plus bas que ZZZ puis move vers
  leur place). « raison. » (1836) : kit.draw("role_vide", f, DRAW) ; kit.fade("role_vide_mot", f + 4) (« ? »).

RACCORD vers p3 : l'image 1862 doit valoir ENTRY_P3 (berceau, ses 5 billets couchés, « z z z », pilule « ? » en
tirets ; bouée + 3 billets « Imprévus », valise + 2 billets « Projet » ; carte et pilule en bas à gauche à 0,8 ; tout le
monde du panier éteint (scale 0, values remises à 1) ; arbre, bascule et disques à 0 ; « Toi » en TOI_P2, bras baissé).
"""
from . import *  # noqa: F401,F403
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, SCALE, STRETCH, TILT  # noqa: F401
from pipeline.story_kit import TAP, rotate_about  # noqa: F401


PEN_S11 = (610, 990)                            # S11 « cash ? » : stylo levé (même geste que PEN_S07, depuis x 700)
ZZZ_RISE = 20                                   # S14 « dort » : les « z » montent de 20 px


def _tilt(S, id, f, base):
    """S13 « compte » : l'entité monde `id` suit la planche (rotation autour du pivot, mêmes assouplissements) :
    0 -> BASCULE_OVER en TILT images, puis -> BASCULE_TILT en 6 (amorti)."""
    S.path(id, f, TILT, "out", lambda p: rotate_about(base, BASCULE_OVER * p, BASCULE_C))
    S.path(id, f + TILT, 6, "inOut",
           lambda p: rotate_about(base, BASCULE_OVER + (BASCULE_TILT - BASCULE_OVER) * p, BASCULE_C))


def part(S, kit, c):
    toi = c.toi
    f0 = scene_f0(S, "S09")
    kit.pin(f0 - 1, ENTRY_P2)
    if S.val("toi", "scale", f0 - 1) == 0:      # partie construite seule (WTH_PARTS) : « Toi » n'est pas entré
        toi.enter(f0 - 12, at=TOI_P1)
        toi.stow(f0 - 9, d=2)
        toi.lower(f0 - 8)

    # ================= S09 : ≈ 8 200 € en euros d'aujourd'hui =================
    f = kit.at("S09", "fin,", "la dernière case de la barre des 10 ans bat ; « 10 ans » se souligne")
    S.key("temps_case10", "scale", f - 1, 1)
    kit.pulse("temps_case10", f, peak=1.2, step=2)
    S.key("temps_case10", "scale", f + 4, 0)
    kit.draw("temps_10", f, DRAW, track="under")

    f = kit.at("S09", "achètent", "b5, vide, passe par-dessus le bord et tombe hors du panier ; sa place reste en "
                                  "tirets rouges ; un second carré rouge cerne le haut de b4")
    lift = kit.move("b5", f, [ART_LOCAL[4][0] + 70, ART_LOCAL[4][1] - 50], d=5, arc=30)
    kit.drop("b5", lift, out=True, h=160, rot=12)
    kit.draw("vide4", f + 2, 8)

    f = kit.at("S09", "l’équivalent", "on compte : les 8 articles pleins, puis le cinquième de b4, battent un à un")
    for k, b in enumerate(["b1", "b2", "b3", "b6", "b7", "b8", "b9", "b10", "b4"]):
        kit.pulse(b, f + 2 * k, peak=1.12, step=2)

    f = kit.at("S09", "8 200 €", "« ≈ » surgit devant « 8 200 € », qui bat deux fois")
    kit.pop("pouvoir_approx", f)
    kit.pulse("pouvoir_val", f, times=2, step=3, peak=1.15)

    f = kit.at("S09", "d’aujourd’hui.", "« en euros d’aujourd’hui » s’écrit en fondu sous le compteur")
    kit.fade("pouvoir_note", f)

    f = kit.at("S09", "exemple", "la pilule « ◀◀ exemple » perd son ◀◀ et devient « exemple illustratif »")
    kit.vanish("mention_ico", f, d=6)
    S.key("mention", "w", f, W_EXEMPLE_ILL, POP, "out")
    S.key("mention", "text", f + 3, T_EXEMPLE_ILL)

    # ================= S10 : « toujours » 10 000 € ; la perte est invisible =================
    f = kit.at("S10", "Pourtant,", "« Toi » regarde à nouveau son solde : le cône du regard va de sa tête à la "
                                   "carte ; « exemple illustratif » se range")
    kit.pop("regard", f)
    kit.vanish("mention", f)

    f = kit.at("S10", "solde", "la pilule « 10 000 € » bat deux fois")
    kit.pulse("cash", f, times=2, step=3, peak=1.1)

    f = kit.at("S10", "toujours", "une ellipse encre cercle « 10 000 € » ; « toujours » s’écrit au-dessus ; sous la "
                                  "carte une mini-barre de 10 ans se remplit pendant que le solde roule à « 9 999 € » "
                                  "et retombe sur « 10 000 € »")
    kit.draw("cercle", f, DRAW)
    kit.type("toujours", f, rate=2)
    kit.pop("temps_mini", f, d=4)
    S.key("temps_mini", "value", f + 2, 1, 12, "linear")
    S.key("cash", "text", f + 5, T_CASH_ROLL)
    S.key("cash", "text", f + 10, T_CASH)

    f = kit.at("S10", "perte", "les places en tirets rouges et « ≈ 8 200 € » battent ; le panier tremble ; la carte "
                               "ne bouge pas")
    kit.pulse("vide4", f, times=2, step=2, peak=1.15)
    kit.pulse("vide5", f, times=2, step=2, peak=1.15)
    kit.pulse("pouvoir_val", f, times=2, step=2, peak=1.1)
    kit.shake("panier", f, amp=5)

    f = kit.at("S10", "invisible.", "le cône reste sur la carte ; hors du cône, les deux places rouges et "
                                    "« ≈ 8 200 € » battent une seconde fois")
    kit.pulse("vide4", f, step=3, peak=1.15)
    kit.pulse("vide5", f, step=3, peak=1.15)
    kit.pulse("pouvoir_val", f, step=3, peak=1.1)
    kit.pulse("pouvoir_approx", f, step=3, peak=1.1)

    # ================= S11 : tout placer ? Non =================
    f = kit.at("S11", "Face", "relais : le panier, l’étiquette et sa pilule se rangent dans le solde ; les chiffres, "
                              "la barre, l’ellipse, le regard et « intérêts : 0 € » se réduisent ; la carte descend "
                              "en bas à gauche")
    kit.morph(["pouvoir_titre", "pouvoir_val", "pouvoir_approx", "pouvoir_note", "temps", "temps_auj", "temps_10", "cercle",
               "toujours", "temps_mini"], [], f, pair=False)
    for id in ("panier", "etiquette", "taux"):  # l'argent qui a perdu sa valeur rentre dans la pilule
        kit.vanish(id, f, into="cash")
    kit.vanish("regard", f, d=6)
    kit.vanish("interets", f)
    for w_id in ("lien", "ficelle_panier"):
        kit.draw(w_id, f, 6, to=0)
    kit.move("compte", f, COMPTE_LOW, scale=COMPTE_LOW_K)
    kit.move("cash", f, CASH_LOW, scale=COMPTE_LOW_K)
    for t in ("compte_mot", "compte_ico"):      # « Solde » garde 34 px une fois la carte à 0,8
        S.key(t, "scale", f, COMPTE_TXT_LOW_K, MOVE, "inOut")
    g = f + MORPH + 1                           # panier caché : son monde revient à l'état de ENTRY_P3
    for i, b in enumerate(ARTICLES):
        S.key(b, "scale", g, 0)
        S.key(b, "value", g, 1)
        S.key(b, "fill", g, ART_FILL.lower())
        S.key(b, "opacity", g, 1)
        S.key(b, "rot", g, 0)
        S.key(b, "pos", g, list(ART_LOCAL[i]))
    for v in ("vide4", "vide5", "vide9", "vide10", "courbe"):   # vide9/10, courbe : sans trait, mis à 0 (ENTRY_P3)
        S.key(v, "scale", g, 0)

    f = kit.at("S11", "envie", "10 billets cyan sortent de la pilule « 10 000 € » et se rangent en deux rangées "
                               "au-dessus de la carte")
    for i, b in enumerate(BILLETS):
        kit.pop(b, f + i, from_pt="cash", to=BILLET_ROWS[i], d=7)

    f = kit.at("S11", "placer.", "un arbre de verre tombe en haut à droite ; les 10 billets glissent tous à son pied, "
                                 "avec la pilule « tout » au-dessus d’eux")
    drop_in(kit, "arbre", f)
    kit.pop("tout", f + 6, d=6)
    kit.move("tout", f + 8, list(TOUT_TREE))
    for b, p in zip(BILLETS, ARBRE_ROWS):
        kit.move(b, f + 8, p)

    f = kit.at("S11", "Mais", "« Toi » marche vers la carte, jusqu’en x 700")
    toi.walk(f, TOI_P2[0], low=True)

    f = kit.at("S11", "cash ?", "« Toi » sort son stylo et le lève : un « ? » en sort et monte au-dessus de lui")
    toi.unstow(f)
    toi.reach(f, PEN_S11, d=6)
    kit.pop("question", f + 4, from_pt=toi.tip(f + 3), to=QUESTION_S11)

    f = kit.at("S11", "Non.", "le stylo de « Toi » frappe la pilule : au contact « tout » est barré, les billets "
                              "s’arrêtent net, le « ? » rentre dans la pointe ; les 10 billets reviennent au-dessus "
                              "de la carte ; l’arbre reste")
    hit = toi.tap(f - 5, CASH_TAP, d=6)           # contact sur le mot
    kit.draw("tout_barre", hit, 4)
    kit.vanish("question", hit, into=toi.tip(hit), d=6)
    kit.shake("tout", hit, amp=8)
    for b, p in zip(BILLETS, BILLET_ROWS):
        kit.shake(b, hit, amp=8)
        kit.move(b, hit + 3, p, arc=60)
    toi.stow(hit + 7)
    toi.lower(hit + 7)

    # ================= S12 : un rôle pour l'argent disponible =================
    f = kit.at("S12", "L’argent", "les 10 billets battent ensemble au-dessus de la carte ; « tout » barré se range ; "
                                  "l’arbre reste en place")
    for b in BILLETS:
        kit.pulse(b, f, times=2, step=2, peak=1.1)
    kit.vanish("tout", f)
    S.key("tout_barre", "draw", f + POP + 1, 0)

    f = kit.at("S12", "faire", "une bouée tombe en haut à gauche")
    drop_in(kit, "bouee", f)

    f = kit.at("S12", "imprévus,", "3 billets volent un à un sous la bouée et s’y empilent en escalier ; une "
                                   "vaguelette passe sous la bouée ; la pile bat et « Imprévus » se pose dessous")
    lands = [kit.move(b, f + 4 * k, p, d=12, arc=60) for k, (b, p) in enumerate(zip(BILLETS[0:3], PILE_BOUEE))]
    kit.draw("vague", lands[0], 6)
    kit.draw("vague", lands[0] + 8, 6, to=0)
    for b in BILLETS[0:3]:
        kit.pulse(b, lands[-1], step=2, peak=1.12)
    kit.pop("role_imprevus", lands[-1])

    f = kit.at("S12", "financer", "une valise tombe à côté de la bouée")
    drop_in(kit, "valise", f)

    f = kit.at("S12", "projet", "2 billets volent un à un sous la valise et s’y empilent en escalier ; la pile bat "
                                "et « Projet » se pose dessous")
    lands = [kit.move(b, f + 4 * k, p, d=12, arc=60) for k, (b, p) in enumerate(zip(BILLETS[3:5], PILE_VALISE))]
    for b in BILLETS[3:5]:
        kit.pulse(b, lands[-1], step=2, peak=1.12)
    kit.pop("role_projet", lands[-1])

    # ================= S13 : la stabilité pèse plus que le rendement =================
    f = kit.at("S13", "Pour", "une bascule surgit à plat sous l’arbre ; un disque bouclier sort de la bouée et se pose "
                              "sur son bout gauche ; « stabilité » paraît quand il s’y pose")
    kit.pop("bascule", f)
    S.key("bouclier", "pos", f - 1, list(BOUEE_C))        # naît sur la bouée, puis vole en arc (sous les pilules)
    kit.pop("bouclier", f)
    g = kit.move("bouclier", f + 2, BOUCLIER_SEAT, d=8, arc=110)
    kit.pop("stabilite", g)

    f = kit.at("S13", "ça,", "un disque % sort de l’arbre et se pose sur le bout droit ; « rendement » paraît quand il "
                             "s’y pose")
    g = kit.pop("pourcent", f, from_pt=ARBRE_C, to=POURCENT_SEAT, d=12)
    kit.pop("rendement", g)

    f = kit.at("S13", "stabilité", "le disque bouclier grossit (×1,5) et se remplit de cyan, le disque % rapetisse "
                                   "(×0,8) : le poids se voit")
    S.key("bouclier", "scale", f, BOUCLIER_BIG_K, SCALE, "out")
    S.key("bouclier", "fill", f, CYAN, SCALE, "out")
    S.key("bouclier", "pos", f, list(BOUCLIER_BIG_SEAT), SCALE, "out")
    S.key("stabilite", "pos", f, list(STABILITE_UP), SCALE, "out")    # la légende cède la place
    S.key("pourcent", "scale", f, POURCENT_SMALL_K, SCALE, "out")
    kit.pulse("bouclier", f + SCALE, peak=round(BOUCLIER_BIG_K * 1.1, 3), step=3)

    f = kit.at("S13", "compte", "la bascule penche nettement à gauche (−20° puis −18°), côté « stabilité » ; le % et "
                                "« rendement » restent en l’air")
    S.key("bascule", "rot", f, BASCULE_OVER, TILT, "out")
    S.key("bascule", "rot", f + TILT, BASCULE_TILT, 6, "inOut")
    for id in ("bouclier", "pourcent", "stabilite", "rendement"):
        _tilt(S, id, f, S.val(id, "pos", f - 1))
    g = S.word_after("rendement", f)
    for id, pk in (("bouee", 1.1), ("valise", 1.1), ("bouclier", round(BOUCLIER_BIG_K * 1.1, 3))):
        kit.pulse(id, g, step=3, peak=pk)
    for w_id in ("fil_bouee", "fil_valise"):    # l'argent des deux paquets choisit la stabilité
        kit.draw(w_id, g, DRAW)

    # ================= S14 : l'argent qui dort sans raison =================
    f = kit.at("S14", "sujet,", "la bascule, le % et l’arbre se réduisent ; le bouclier rentre dans la bouée ; les 5 "
                                "billets restés au-dessus de la carte battent")
    for id in ("bascule", "pourcent", "stabilite", "rendement", "arbre"):
        kit.vanish(id, f)
    kit.vanish("bouclier", f, into="bouee")
    for w_id in ("fil_bouee", "fil_valise"):
        kit.draw(w_id, f, 6, to=0)
    for b in BILLETS[5:10]:
        kit.pulse(b, f, times=2, step=2, peak=1.12)

    f = kit.at("S14", "l’argent", "un berceau tombe à droite")
    drop_in(kit, "berceau", f)

    f = kit.at("S14", "dort", "les 5 billets volent dans le berceau et s’y couchent en éventail ; trois « z » montent")
    for k, (b, p, r) in enumerate(zip(BILLETS[5:10], PILE_BERCEAU, PILE_BERCEAU_ROT)):
        kit.move(b, f + k, p, d=8, arc=60, scale=PILE_BERCEAU_K)
        S.key(b, "rot", f + k, r, 8, "inOut")
    for k, (zid, p, _) in enumerate(ZZZ):
        kit.pop(zid, f + 2 + 2 * k, from_pt=[p[0], p[1] + ZZZ_RISE], to=list(p), d=6)

    f = kit.at("S14", "raison.", "une pilule en tirets marquée « ? » se trace sous le berceau : pas de rôle")
    S.key("role_vide", "scale", f - 1, 1)
    kit.draw("role_vide", f, DRAW)
    kit.fade("role_vide_mot", f + 4)
