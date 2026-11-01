"""V12, partie 1 : S01-S08, images 0-969 (36 temps forts, 32,3 s). Le solde immobile et le panier qui perd un
article, l'inflation nommée et chiffrée (100 € -> 102 €), le relevé muet, l'exemple sur 10 ans (dérive 882-956).

ÉTAT D'ENTRÉE : l'image 0 du film = l'état de distribution (cast) : carte « Solde » (COMPTE_C) et pilule « 10 000 € »
(CASH_C) à droite ; panier plein de 10 articles (PANIER_C) à gauche ; rien d'autre (toi déclaré show=False). Pas
d'épingle (la partie commence à l'image 0).
SORTIE : ENTRY_P2 à l'image 969 (voir __init__.py). Tout ce que cette partie commence finit avant 970 (la dérive de S08
finit à 956).

Ids : compte (+ compte_ico, compte_mot, compte_filet, interets), cash, panier (+ panier_anse, panier_roue1-2), b1-b10,
vide4, vide5, hausse1-5, hausse_grande, lien, toi (Figure c.toi), nom_toi, regard, question, cible, mission,
mission_pointe, etiquette (+ etiq_prix, etiq_taux), ficelle_taux, ficelle_panier, taux, un_an, pouvoir_titre,
pouvoir_val, mention (+ mention_ico), temps, temps_auj, temps_10.
Helpers du paquet : drop_in, taux_under, ring, scene_f0 ; constantes : voir __init__.py.

TOUR DE REVUE 1 (prime sur le brief ci-dessous quand ils diffèrent) : S01-S03 panier et carte à ×1,15 plus bas
(HOOK), remis en place sur « Dans » ; « si. » : flèche ↑ de 64 px qui bat AVANT que b5 rougisse, b5 passe par-dessus
le bord puis tombe (500 ms) ; regard = cône translucide deep (pop / vanish au visage) en S03, S07, S10 ; « même » et
« aucun » : la place vide bat puis tremble hors du cône ; S05 : la flèche de la mission rentre en 150 ms, la cible se
range dans le solde, l'étiquette tombe 3 images plus tard ; flèches 48 / 110 px ; S06 : fantôme « 100 € » en tirets,
« + 1 an » sur une flèche fantôme -> étiquette, l'étiquette monte de 20 px à chaque pas du compteur ; S07 : pas de
stylo (rangé jusqu'en S11), le « ? » naît au-dessus de la tête ; S08 : « aujourd'hui » n'est plus affiché, la pilule
garde « inflation : 2 % / an », la face dit « +2 % », la place de b5 vire aux tirets rouges à mi-dérive.

BRIEF, scène par scène (images = round(t × 30), avant calage acoustique) :
- S01 (0-51) « euros » (8) : kit.pulse("cash", f, times=2, step=3, peak=1.1). « pas. » (26) : kit.hold (rien ne
  bouge). Image 0 déjà lisible, sans mouvement.
- S02 (52-114) « Leur » (52) : kit.draw("lien", f, DRAW) (de la pilule au coin haut droit de la corbeille).
  « d’achat, » (70) : kit.pulse("panier", f, times=2, step=2, peak=1.06) (articles, roues, anse suivent : enfants).
  « si. » (90) : kit.pop("hausse5", f, d=6) au-dessus de b5 ; b5 fill LIGHT -> RED (hex, 3 images) puis
  kit.drop("b5", f + 4, out=True, h=160, rot=12) ; kit.draw("vide5", f + 6, 6) ; la flèche reste, la pilule ne bouge
  pas. Fin : panier de 9 articles, place b5 en tirets rouges sous sa flèche.
- S03 (115-169) « tu » (120) : c.toi.enter(f, at=TOI_P1) puis bras baissé et stylo rangé (c.toi.stow juste après
  l'entrée, puis c.toi.lower) ; kit.pop("nom_toi", f) (enfant de toi, pilule « Toi » au-dessus de la tête).
  « vois » (130) : kit.draw("regard", f, DRAW) (tête -> bas de la carte). « même » (138) :
  kit.pulse("vide5", f, times=2, step=2, peak=1.12) ; le regard ne va pas vers le panier.
- S04 (170-353) « Dans » (170) : kit.draw("regard", f, 6, to=0) ; kit.vanish("nom_toi", f, into="toi").
  « l’inflation » (226) : kit.pop("taux", f) en TAUX_C0 (pilule « inflation ») ; kit.pulse hausse5 et vide5
  (times=2, step=2, peak=1.15) ; kit.shake("panier", f, amp=6). « comment » (286) : drop_in(kit, "cible", f) en
  CIBLE_C (ne pas montrer la cible avant le mot). « mission » (312) : kit.draw("mission", f, DRAW) puis
  kit.pop("mission_pointe", f + DRAW - 2, d=4) à MISSION_B. « cash. » (332) : kit.pulse("cash", f, times=2, step=3,
  peak=1.1). Fin : cible reliée au solde ; « inflation » au-dessus du panier entamé.
- S05 (354-431) « L’inflation, » (354) : relais : kit.vanish cible, mission_pointe, et mission draw -> 0 (from ou draw)
  ; drop_in(kit, "etiquette", f) en ETIQ_DROP (compteur « 100 € » sur sa face, etiq_prix opacité 1) ;
  kit.move("taux", f, taux_under(ETIQ_DROP), arc=60) puis kit.draw("ficelle_taux", f + MOVE, 6).
  « hausse » (382) : kit.move etiquette -> ETIQ_UP et taux -> taux_under(ETIQ_UP) (même clé, MOVE inOut) ;
  kit.pop("hausse_grande", f). « prix. » (407) : kit.stagger(HAUSSE[:4], f, 2, kit.pop) (à côté de hausse5).
- S06 (432-628) « Quand » (432) : les 6 flèches kit.vanish(…, into="etiquette") ; etiquette -> ETIQ_LEFT, taux ->
  taux_under(ETIQ_LEFT) (MOVE). « 2 % » (456) : taux text -> T_INFL_TAUX et w W_INFL -> W_INFL_TAUX (POP, out ; la
  bascule de texte au début du segment). « coûtait » (519) : kit.pulse("etiq_prix", f, times=2, step=3, peak=1.15).
  « coûte » (554) : etiquette -> ETIQ_RIGHT, taux -> taux_under(ETIQ_RIGHT) (MOVE ; pilule x 547-893).
  « 102 € » (564) : S.key("etiq_prix", "value", f, PRIX_1, 9, "out"). « un » (577) : kit.pop("un_an", f) en UN_AN_C.
- S07 (629-773) « Pourquoi » (629) : kit.fade("un_an", f, to=0) (puis scale 0) ; c.toi.unstow(f) et
  c.toi.reach(f, PEN_S07, d=9) ; kit.pop("question", f + 6, from_pt=c.toi.tip(f + 5), to=QUESTION_S07) (le « ? » né
  de la pointe, à gauche du futur regard). « perte » (703) : kit.pulse("vide5", f, times=2, step=2, peak=1.15).
  « n’apparaît » (716) : kit.draw("regard", f, DRAW) (il lit son relevé). « aucun » (738) : vide5 rebat (idem),
  hors du regard. « relevé. » (750) : kit.pulse("cash", f, step=2, peak=1.08) seule sur la carte ; tenue ensuite.
  Rien n'est rouge sur la carte.
- S08 (774-969) « Imagine » (774) : kit.pop("mention", f) en MENTION_C (« ◀◀ exemple », mention_ico visible) ; b5 :
  fill RED -> LIGHT (d=0 à f - 1), opacité 1, échelle 1, value 1, rot 0, posé 160 px plus bas à f - 1 puis
  kit.move vers sa place ART_LOCAL[4] (repère du panier) ; kit.draw("vide5", f, 6, to=0) : on rejoue l'exemple.
  « 10 000 € » (789) : kit.pop pouvoir_titre et pouvoir_val (value POUVOIR_0) ; kit.pulse("cash", f, step=2,
  peak=1.1) : même somme des deux côtés. « laissés » (813) : regard draw -> 0 ; kit.vanish("question", f,
  into=c.toi.tip(f)) ; c.toi.stow(f + 2) puis c.toi.lower(f + 6). « intérêt » (831) : kit.type("interets", f, rate=2).
  « pendant » (844) : kit.draw("ficelle_taux", f, 4, to=0) ; etiquette vole (kit.move, arc 80) vers ETIQ_PANIER à
  l'échelle ETIQ_PANIER_K ; etiq_prix opacité 1 -> 0 (FADE) puis etiq_taux 0 -> 1 (FADE) : « + 2 % / an » ; taux text
  -> T_INFL, w -> W_INFL et move vers TAUX_PANIER (MORPH) ; kit.draw("ficelle_panier", f + MOVE, 6) (trou de
  l'étiquette -> coin haut gauche de la corbeille). « 10 ans, » (857) : « temps » pop en largeur depuis la gauche
  (scale 1 à f - 1 avec w 0 et pos x 340, puis w -> TEMPS_W et pos -> TEMPS_C en STRETCH 6 images) ; kit.fade
  temps_auj et temps_10 vers 1. « avec » (882) -> 956 (dérive linéaire, d = 956 - 882 = 74 images) :
  S.key("temps", "value", f, 1, 74, "linear") ; S.key("pouvoir_val", "value", f, POUVOIR_1, 74, "linear") ; b5 value
  1 -> 0 en 41 images (5,5 cases), puis b4 value 1 -> 0.2 en 33 images ; à chaque case (toutes les 7,4 images)
  kit.pulse("etiquette", …, step=2, peak=1.08) en évitant de recouvrir deux pulses (4 images chacun). « 2 % » (904) :
  kit.pulse("etiq_taux", f, step=2, peak=1.15) (piste du texte, pas de l'étiquette : la dérive continue).
  « d’inflation » (916) : kit.pulse("taux", f, step=2, peak=1.1). La pilule « 10 000 € » ne bouge pas.

RACCORD vers p2 : l'image 969 doit valoir ENTRY_P2 (barre pleine, b5 vide (value 0, light), b4 à 0,2, compteur
8 200 €, « + 2 % / an » sur l'étiquette accrochée, pilule « inflation » au-dessus, « ◀◀ exemple », « intérêts : 0 € »
écrit, regard et « ? » rentrés ; « Toi » en TOI_P1, stylo rangé, bras baissé).
"""
from . import *  # noqa: F401,F403
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, SCALE, STRETCH, TILT  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401


def part(S, kit, c):
    toi = c.toi

    # Image 0 = distribution (cast). Épingle de principe à -1 : l'état de S01, identique au cast (aucun saut).
    # Tour 1 : S01-S03, panier et carte à ×1,15, plus bas (PANIER_HOOK, COMPTE_HOOK) ; retour en place sur « Dans ».
    kit.pin(0 - 1, {"compte": {"pos": list(COMPTE_HOOK), "scale": HOOK_K},
                    "cash": {"pos": list(CASH_HOOK), "scale": HOOK_K},
                    "panier": {"pos": list(PANIER_HOOK), "scale": HOOK_K}, **{b: {"value": 1} for b in ARTICLES}})
    for b in ARTICLES:                           # même couleur, posée par une clé : S.val la rend alors en hex
        S.key(b, "fill", 0, ART_FILL)            # minuscule, comme ENTRY_P2 (pas de « (saut) » au raccord p2)

    # ================= S01 « Tes euros ne bougent pas. » =================
    f = kit.at("S01", "euros", "la pilule « 10 000 € » bat deux fois (×1,1) ; rien d'autre ne bouge")
    kit.pulse("cash", f, times=2, step=3, peak=round(HOOK_K * 1.1, 3))
    kit.hold("S01", "pas.", "tenue : le solde « 10 000 € » et le panier plein de 10 articles, immobiles")

    # ================= S02 « Leur pouvoir d’achat, si. » =================
    f = kit.at("S02", "Leur", "un fil deep se trace de la pilule « 10 000 € » au coin haut droit du panier")
    kit.draw("lien", f, DRAW)
    f = kit.at("S02", "d’achat,", "le panier entier (corbeille, roues, 10 articles) bat (×1,06)")
    kit.pulse("panier", f, times=2, step=2, peak=round(HOOK_K * 1.06, 3))
    f = kit.at("S02", "si.", "une grande flèche ↑ surgit au-dessus de l'article b5 et bat ; puis b5 rougit, passe "
                             "par-dessus le bord et tombe hors du panier ; sa place reste en tirets rouges")
    kit.pop("hausse5", f, d=6)                   # la cause d'abord : la flèche monte, bat, puis l'article rougit
    kit.pulse("hausse5", f + 6, peak=1.2, step=2)
    S.key("b5", "fill", f + 7, RED, 3, "out")
    lift = kit.move("b5", f + 10, [ART_LOCAL[4][0] + 70, ART_LOCAL[4][1] - 50], d=5, arc=30)   # par-dessus le bord
    kit.drop("b5", lift, out=True, h=160, rot=12, d=15)
    kit.draw("vide5", lift + 2, 6)

    # ================= S03 « Et tu ne le vois même pas. » =================
    f = kit.at("S03", "tu", "« Toi » surgit en bas à droite, bras baissé, sans stylo ; sa pilule « Toi » au-dessus "
                            "de sa tête")
    toi.stow(f - 5, d=4)                         # stylo caché : il n'apparaît qu'en S11, où il sert
    toi.enter(f, at=TOI_P1)
    toi.lower(f + 1, d=POP - 1)                  # le bras paraît (f + 2) en train de se baisser
    kit.pop("nom_toi", f)
    f = kit.at("S03", "vois", "un cône de regard translucide va de la tête de « Toi » à la carte « Solde »")
    kit.pop("regard", f)
    f = kit.at("S03", "même", "la place vide rouge du panier bat deux fois puis tremble, hors du cône du regard")
    g = kit.pulse("vide5", f, times=2, step=2, peak=1.12)
    kit.shake("vide5", g, amp=6)

    # ================= S04 « Dans cette vidéo… mission à ton cash. » =================
    f = kit.at("S04", "Dans", "le panier et la carte reprennent leur place ; le cône rentre dans la tête, la pilule "
                              "« Toi » aussi ; puis la place vide rouge bat")
    kit.vanish("regard", f, d=6)
    kit.vanish("nom_toi", f, into="toi")
    kit.move("panier", f, list(PANIER_C), scale=1)
    kit.move("compte", f, list(COMPTE_C), scale=1)
    kit.move("cash", f, list(CASH_C), scale=1)
    kit.pulse("vide5", f + MOVE + 2, step=3, peak=1.15)
    f = kit.at("S04", "l’inflation", "la pilule « inflation » surgit au-dessus de la flèche ↑ ; la flèche et la "
                                     "place vide battent, le panier tremble")
    kit.pop("taux", f)
    for hid in ("hausse5", "vide5"):
        kit.pulse(hid, f, times=2, step=2, peak=1.15)
    kit.shake("panier", f, amp=6)
    kit.pulse("cash", S.word_after("argent.", f), step=2, peak=1.08)    # « à ton argent » : le solde (tenue coupée)
    f = kit.at("S04", "comment", "une cible tombe en haut au centre")
    drop_in(kit, "cible", f, h=90)                # chute courte : le haut de la cible reste sous y 160
    f = kit.at("S04", "mission", "une flèche deep se trace du haut de la carte « Solde » jusqu'à la cible")
    kit.draw("mission", f, DRAW)
    kit.pop("mission_pointe", f + DRAW - 2, d=4)
    f = kit.at("S04", "cash.", "la pilule « 10 000 € » bat deux fois : c'est elle qui reçoit une mission")
    kit.pulse("cash", f, times=2, step=3, peak=1.1)

    # ================= S05 « L’inflation, c’est la hausse générale des prix. » =================
    f = kit.at("S05", "L’inflation,", "la flèche de la mission rentre dans la carte et la cible se range dans le "
                                      "solde ; l'étiquette « 100 € » tombe à sa place et la pilule « inflation » vole "
                                      "se pendre dessous par une ficelle")
    kit.draw("mission", f, 5, to=0)              # 150 ms : partie avant que l'étiquette ne croise son bout
    kit.vanish("mission_pointe", f, into="cash", d=5)
    kit.vanish("cible", f, into="cash")          # la mission reste attachée au solde
    drop_in(kit, "etiquette", f + 3, h=90)        # chute courte : rien dans les 160 px du haut
    kit.move("taux", f + 3, taux_under(ETIQ_DROP), arc=60)
    kit.draw("ficelle_taux", f + 3 + MOVE, 6)
    f = kit.at("S05", "hausse", "l'étiquette et sa pilule montent ; une grande flèche ↑ surgit à droite de "
                                "l'étiquette")
    kit.move("etiquette", f, ETIQ_UP)
    kit.move("taux", f, taux_under(ETIQ_UP))
    kit.pop("hausse_grande", f)
    f = kit.at("S05", "prix.", "quatre flèches ↑ surgissent au-dessus des colonnes du panier, à côté de celle de b5 : "
                               "tout augmente")
    kit.stagger(HAUSSE[:4], f, 2, kit.pop)

    # ================= S06 « Quand elle est de 2 % par an… 102 € un an plus tard. » =================
    f = kit.at("S06", "Quand", "les six flèches ↑ rentrent dans l'étiquette, qui glisse à gauche avec sa pilule")
    kit.move("etiquette", f, ETIQ_LEFT)
    kit.move("taux", f, taux_under(ETIQ_LEFT))
    for hid in HAUSSE + ["hausse_grande"]:
        kit.vanish(hid, f, into="etiquette")
    f = kit.at("S06", "2 %", "la pilule s'allonge : « inflation : 2 % / an »")
    S.key("taux", "text", f, T_INFL_TAUX)
    S.key("taux", "w", f, W_INFL_TAUX, POP, "out")
    f = kit.at("S06", "coûtait", "le prix « 100 € » de l'étiquette bat deux fois : le prix d'aujourd'hui")
    kit.pulse("etiq_prix", f, times=2, step=3, peak=1.15)
    f = kit.at("S06", "coûte", "l'étiquette et sa pilule glissent vers la droite ; sa place reste marquée « 100 € » "
                               "en tirets")
    kit.move("etiquette", f, ETIQ_RIGHT, d=8)
    kit.move("taux", f, taux_under(ETIQ_RIGHT), d=8)
    S.key("fantome", "scale", f - 1, 1)          # cadre en tirets (invisible tant que draw = 0)
    kit.draw("fantome", f, 8)
    kit.fade("fantome_prix", f + 3)
    f = kit.at("S06", "102 €", "le prix passe de « 100 € » à « 101 € » puis « 102 € » ; à chaque pas l'étiquette "
                               "monte de 20 px")
    S.key("etiq_prix", "value", f, PRIX_0 + 1, 4, "out")
    S.key("etiq_prix", "value", f + 4, PRIX_1, 4, "out")
    for k in range(2):
        y = ETIQ_RIGHT[1] - 20 * (k + 1)
        kit.move("etiquette", f + 4 * k, [ETIQ_RIGHT[0], y], d=4, e="out")
        kit.move("taux", f + 4 * k, taux_under([ETIQ_RIGHT[0], y]), d=4, e="out")
    f = kit.at("S06", "un", "« + 1 an » surgit sur une flèche qui va de la place « 100 € » à l'étiquette « 102 € »")
    kit.draw("fleche_an", f, 6)
    kit.pop("fleche_an_pointe", f + 4, d=4)
    kit.pop("un_an", f)

    # ================= S07 « Pourquoi partir d’un exemple ? … sur aucun relevé. » =================
    f = kit.at("S07", "Pourquoi", "« + 1 an », sa flèche et la place « 100 € » s'effacent ; un « ? » naît au-dessus "
                                  "de la tête de « Toi »")
    g = kit.fade("un_an", f, to=0)
    S.key("un_an", "scale", g, 0)
    kit.draw("fleche_an", f, 5, to=0)
    kit.vanish("fleche_an_pointe", f, d=5)
    kit.vanish("fantome", f)
    S.key("fantome_prix", "scale", f + POP, 0)
    head = [TOI_P1[0], TOI_P1[1] + HEAD_DY - HEAD_R]
    kit.pop("question", f + 2, from_pt=head, to=QUESTION_S07)
    kit.pulse("question", S.word_after("exemple", f), peak=1.12)   # la question reste posée (tenue coupée)
    f = kit.at("S07", "perte", "la place vide rouge du panier bat deux fois, toujours vide")
    kit.pulse("vide5", f, times=2, step=2, peak=1.15)
    f = kit.at("S07", "n’apparaît", "« Toi » lit sa carte : un cône de regard translucide va de sa tête à la carte "
                                    "« Solde »")
    kit.pop("regard", f)
    f = kit.at("S07", "aucun", "la place vide rouge bat puis tremble, hors du cône ; la carte ne bouge pas")
    g = kit.pulse("vide5", f, times=2, step=2, peak=1.15)
    kit.shake("vide5", g, amp=6)
    f = kit.at("S07", "relevé.", "seule la pilule « 10 000 € » bat sur la carte : aucune ligne de perte ne s'y "
                                 "ajoute")
    kit.pulse("cash", f, times=1, step=4, peak=1.08)

    # ================= S08 « Imagine 10 000 € … avec 2 % d’inflation par an. » =================
    f = kit.at("S08", "Imagine", "la pilule « ◀◀ exemple » surgit sous le panier ; b5 remonte à sa place, plein ; "
                                 "la place vide rouge s'efface : on rejoue l'exemple")
    kit.pop("mention", f)
    b5_home = list(ART_LOCAL[4])
    S.key("b5", "fill", f - 1, ART_FILL)
    S.key("b5", "rot", f - 1, 0)
    S.key("b5", "value", f - 1, 1)
    S.key("b5", "pos", f - 1, [b5_home[0], b5_home[1] + 160])
    S.key("b5", "scale", f - 1, 0)
    S.key("b5", "opacity", f, 1)
    S.key("b5", "scale", f, 1, POP, "out")
    kit.move("b5", f, b5_home)
    kit.draw("vide5", f, 6, to=0)
    f = kit.at("S08", "10 000 €", "« pouvoir d'achat 10 000 € » surgit sous le panier ; la pilule du solde bat : "
                                  "même somme des deux côtés")
    kit.pop("pouvoir_titre", f)
    kit.pop("pouvoir_val", f)
    kit.pulse("cash", f, times=1, step=4, peak=1.1)
    f = kit.at("S08", "laissés", "le cône du regard et le « ? » rentrent dans la tête de « Toi »")
    head = [TOI_P1[0], TOI_P1[1] + HEAD_DY - HEAD_R]
    kit.vanish("regard", f, d=6)
    kit.vanish("question", f, into=head, d=6)
    f = kit.at("S08", "intérêt", "« intérêts : 0 € » s'écrit sur la carte, sous la pilule")
    kit.type("interets", f, rate=2)
    f = kit.at("S08", "pendant", "l'étiquette vole s'accrocher au panier ; sa face passe à « +2 % » ; la pilule "
                                 "« inflation : 2 % / an » se pose au-dessus ; une ficelle la relie au panier")
    kit.draw("ficelle_taux", f, 4, to=0)
    kit.move("etiquette", f, ETIQ_PANIER, arc=80, scale=ETIQ_PANIER_K)
    g = kit.fade("etiq_prix", f, to=0)
    kit.fade("etiq_taux", g, to=1)
    kit.move("taux", f, TAUX_PANIER)                # même vol que l'étiquette : ils se posent ensemble
    kit.draw("ficelle_panier", f + MOVE, 6)
    f = kit.at("S08", "10 ans,", "la barre des 10 ans s'étire depuis la gauche en haut ; « 10 ans » paraît à son "
                                 "bout")
    x0 = TEMPS_C[0] - TEMPS_W / 2
    kit.ensure("temps", "w", 0)
    S.key("temps", "w", f - 1, 0)
    S.key("temps", "pos", f - 1, [x0, TEMPS_C[1]])
    S.key("temps", "scale", f, 1)
    S.key("temps", "w", f, TEMPS_W, STRETCH, "out")
    S.key("temps", "pos", f, list(TEMPS_C), STRETCH, "out")
    kit.fade("temps_10", f)                      # tour 1 : « aujourd'hui » n'est plus affiché (moins de textes)
    f = kit.at("S08", "avec", "dérive linéaire : les cases de la barre se remplissent ; à chaque case l'étiquette "
                              "bat ; b5 se vide et sa place passe en tirets rouges, puis b4 se vide ; le compteur "
                              "descend à 8 200 € ; le solde ne bouge pas")
    end = S.word_after("À", f) - 14             # fin de la dérive juste après « par an. »
    D = end - f
    S.key("temps", "value", f, 1, D, "linear")
    S.key("pouvoir_val", "value", f, POUVOIR_1, D, "linear")
    d5 = round(D * 0.55)                         # b5 : 5,5 cases sur 10
    S.key("b5", "value", f, 0, d5, "linear")
    kit.draw("vide5", f + d5 // 2, 8)            # à mi-chemin, le vide se marque en tirets rouges
    S.key("b4", "value", f + d5, 0.2, D - d5, "linear")
    for k in range(1, 11):                       # un battement par case remplie (4 images ; 7,4 images entre deux)
        kit.pulse("etiquette", round(f + D * k / 10) - 2, step=2, peak=1.08)
    f = kit.at("S08", "2 %", "la face « +2 % » de l'étiquette bat ; la dérive continue")
    kit.pulse("etiq_taux", f, step=2, peak=1.15)
    f = kit.at("S08", "d’inflation", "la pilule « inflation : 2 % / an » bat ; la dérive continue")
    kit.pulse("taux", f, step=2, peak=1.1)
