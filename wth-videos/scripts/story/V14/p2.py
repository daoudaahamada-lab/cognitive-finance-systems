"""V14, partie 2 : S08-S15, images 856-1746 (30 temps forts, 29,7 s). Point 1 : trois lignes cassées au stylo de
« Toi », deux pièces perdues ; point 2 : la réponse fausse rangée dans la boule, la carte neuve à 4 lignes, le livre
dans la case « Source », la citation, l'empreinte reliée à « ton cas », où vérifier, la coche de « Toi » ; point 3 :
le faisceau de l'IA qui retombe avant l'empreinte, le conseiller.

TOUR DE REVUE 1 (le brief ci-dessous est celui de la v1 ; le code fait foi) : S08 la preuve avant le verdict (au
toucher, un trait plein deep va de la valeur à la case « Source » vide, qui bat et rougit, puis la ligne casse) ; bras de
« Toi » baissé après chaque saut ; S10 les 2 pièces rentrent dans « Toi » (reviennent en S16) ; carte prudente plus haute
(CARD_B_C) ; S11 la case repasse au rouge puis vire au cyan sous le livre, le mot « Source » s'efface ; S12 bulle PARLÉE,
empreinte de 130 px tenue contre « Toi » puis posée au sol, fil 7 px ; S13 « Toi » saute près du livre et le touche :
cadre et coche sur la ligne « Source » ; S14 vrai choix : deux cases vides, le stylo hésite sur celle de la boule et
coche la carte, la boule rentre dans la tête de l'IA ; S15 le faisceau s'arrête 180 px avant l'empreinte, tremble,
tombe ; le conseiller arrive en marchant.

ÉTAT D'ENTRÉE (etat_initial de S08) : kit.pin(855, ENTRY_P2) en tête de partie (f0 = scene_f0(S, "S08") = 856). Carte
d'aplomb au centre (rangées y 520 / 624 / 728, valeurs finissant à x 700), cochée par l'IA, autocollant « ? » en
STICKER_C ; case « Source » vide à gauche (150, 700) ; boule en BOULE_TETE ; pile de 4 en PILE_C reliée par fil_jetons ;
« Toi » en TOI_REST (jamais épinglé).
SORTIE : ENTRY_P3 à l'image 1746. Tout ce que cette partie commence finit avant 1747 (le conseiller entré et penché
compris). Faisceaux f_question, f_ecrit, f_empreinte : draw 0 ET from 0. « Toi » en TOI_REST, look 0.

Ids : toi (c.toi), conseiller (c.conseiller), nom_conseiller ; reponse (+ reponse_L1-3, reponse_ia1-3, reflet), doute ;
pile, piece1-4, piece2_euro, fil_jetons, fil_jetons_rouge ; boule, eclat_boule ; pastille ; eclat_ia ; bonne_reponse
(+ bonne_reponse_L1-4, coche_toi, surligne_L4) ; source, source_livre, source_mot ; livre, cadre_livre, fil_source,
fil_source_gras, point_source ; citation (+ citation_pointe, cit_l1, cit_l2a, cit_l2b, cit_l3a, cit_l3b, cit_l3c) ;
empreinte, fil_empreinte ; f_question, f_ecrit, f_empreinte.

BRIEF, scène par scène (images = round(t × 30), avant calage acoustique) :
- S08 (856-992) « Une » (856) : c.toi.hop(f, TOI_HIGH, 10) (l'étiquette suit, enfant) ; look(S, "toi", f, -1) puis
  look 0 à f + 8 : il regarde d'abord la case « Source » vide. « inventée, » (887) : contact du stylo SUR le mot
  (c.toi.tap(f - TAP + 1, VALUE_END_A[0])) ; au contact : reponse_L1 red -> 1 (3 images), crack -> 1 (9 images,
  out). La coche de l'IA reste, l'IA ne bouge pas. « erroné, » (934) : même geste sur VALUE_END_A[1] / reponse_L2.
  « fausse. » (971) : même geste sur VALUE_END_A[2] / reponse_L3. (Défaut V01 n° 2 : c'est le stylo qui casse.)
- S09 (993-1096) « Dite » (993) : c.toi.hop(f, TOI_REST, 10). « assurance, » (1013) : reflet p 0 (f - 1) -> 1
  (12 images) sur la carte cassée. « erreur » (1045) : fil_jetons_rouge opacity 0 -> 1 et fil_jetons opacity 1 -> 0
  (9 images) : le fil devient rouge et épais. « coûter » (1064) : kit.drop("piece4", f, out=True, h=200, dx=30,
  rot=25) puis piece3 à f + 4 (le « € » tombe avec piece4) ; piece2_euro opacity 0 -> 1 (FADE) ; kit.shake piece1 et
  piece2 (axe x) : moitié moins haute.
- S10 (1097-1173) « Alors, » (1097) : kit.vanish("reponse", f, into="boule", d=MORPH) et kit.vanish("doute", f,
  into="boule", d=MORPH) ; fil_jetons_rouge et fil_jetons : from -> 1 (9 images) puis draw / from à 0 (instantané,
  invisibles) ; la pastille ne bouge pas. « quoi » (1120) : kit.move("boule", f, BOULE_SOL, scale=BOULE_SOL_K). Les 2
  pièces restent au sol. « bonne » (1142) : kit.draw("f_question", f, 8) ; eclat_ia p 0 -> 1 ; la carte neuve sort
  de la tête : bonne_reponse pos CARD_A_FROM / scale 0,1 à f - 1, puis -> CARD_C / 1 (MORPH) ; à son arrivée,
  kit.move("pastille", f + MORPH, head_pt("bonne_reponse")[0], d=9) ; f_question se rétracte.
- S11 (1174-1289) « réponse, » (1192) : kit.draw("f_ecrit", f, 8) ; kit.type("bonne_reponse_L1", f, rate=2) +
  bulletOn -> 1 (puce pleine chat). « source, » (1219) : drop_in(kit, "livre", f) (exactement dans la silhouette, à
  SOURCE_BIG_C) ; source et source_livre(_dos) s'effacent sous lui (opacity -> 0, 6 images) ; source_mot reste au-dessus ;
  kit.type L2 + bulletOn ; au bout de la chute, kit.draw("fil_source", f + DROP, 9) (puce de L2 -> bord du livre).
  « date » (1243) : L3. « limites. » (1263) : L4 ; f_ecrit se rétracte.
- S12 (1290-1442) « Par » (1290) : kit.pop("citation", f, from_pt=IA_MOUTH, to=CITATION_C) : bulle parlée, pointe vers
  la bouche. « « Cette » (1322) : kit.type("cit_l1", f, rate=2). « général, » (1361) : kit.type cit_l2a puis cit_l2b ;
  kit.draw("cit_l2a", fin de cit_l2a, 9, track="mark"). « situation ». » (1406) : kit.type cit_l3a, cit_l3b, cit_l3c ;
  kit.draw("cit_l3b", …, 9, track="under") ; kit.pulse("bonne_reponse_L4", f, track="flash", step=3) ; l'empreinte
  sort de « Toi » : kit.pop("empreinte", f, from_pt=poitrine, to=EMPREINTE_C, d=MORPH) ; à son arrivée,
  kit.draw("fil_empreinte", f + MORPH, 9) (« ton cas » -> empreinte).
- S13 (1443-1547) « Une » (1443) : kit.vanish("citation", f, into="bonne_reponse_L1") ; kit.pulse L1 track="flash".
  « prudente » (1461) : le surligneur de L4 : S.key surligne_L4 w -> SURL_L4_W et pos -> SURL_L4_C (même clé, 9
  images) ; bonne_reponse_L4 slotFill -> 0 dans les mêmes images. « sourcée » (1482) : fil_source_gras opacity 0 -> 1
  (9 images) ; kit.pulse("livre", f, peak=1.1 × l'échelle). « vérifier. » (1518) : point_source : S.key scale 1 à f,
  puis S.along_wire("point_source", "fil_source", f, 12, "inOut", 0, 1, f) (le fil n'a pas de via : trajet exact) ;
  à l'arrivée, kit.draw("cadre_livre", …, 9) ; look(S, "toi", f, -1).
- S14 (1548-1630) « C’est » (1548) : kit.move("boule", f, BOULE_HAUT, d=12, scale=BOULE_HAUT_K) ; cadre_livre et
  fil_empreinte s'effacent (opacity -> 0, 6 images, puis draw 0) ; look 0 ; c.toi.hop(f, TOI_MID, 10) (écart :
  coche hors d'allonge depuis le repos). « utile » (1573) : hit = c.toi.tap(f - TAP + 1, card_pt("b",
  COCHE_TOI_LOCAL)) ; kit.draw("coche_toi", hit, 6). « certitude » (1589) : kit.pulse("boule", f, peak=1.12 ×) ;
  eclat_boule p 0 -> 1 (9 images) ; puis (≈ 53,5 s, image 1605) kit.move("boule", 1605, BOULE_SOL, d=12,
  scale=BOULE_SOL_K), sans coche ; c.toi.hop(…, TOI_REST, 10) après la coche.
- S15 (1631-1746) « Et » (1631) : MORPH 11 images : bonne_reponse -> B_SMALL_C / B_SMALL_K, lite 0 -> 1 (fiche et
  L1-4) ; livre -> LIVRE_SMALL_C / LIVRE_SMALL_K ; pastille -> head_pt("bonne_reponse", B_SMALL_C, B_SMALL_K) (même
  clé) ; fil_source_gras opacity -> 0 (le fil revient à 5 px) ; source_mot vanish ; la coche reste (enfant).
  « aucune » (1652) : kit.draw("f_empreinte", f, 18, e="linear") (le faisceau avance). « suffit : » (1677) :
  f_empreinte s'arrête court (pb (520, 1165) : 70 px avant l'empreinte), sag -> 50 et from -> 1 (9 images) ;
  kit.shake("empreinte", f). « humain. » (1724) : c.conseiller.enter(f, at=CONSEILLER_C) (l'étiquette « Conseiller »,
  enfant, entre avec lui) ; S.key("conseiller", "look", f, 1, 4) ; c.conseiller.lean_to(f + POP, 5) : face à « Toi »,
  l'empreinte et les 2 pièces entre eux.
PASSATION vers p3 : à 1746, carte prudente réduite en haut à droite (cochée, lignes en barres), livre à sa gauche relié
à L2, conseiller face à « Toi », empreinte et 2 pièces au sol entre eux, boule au sol ; plus de citation ni de case.
"""
from pipeline.story import DRAW, DROP, FADE, MORPH, POP  # noqa: F401
from pipeline.story_kit import TAP

from . import *  # noqa: F401,F403
from . import ENTRY_P2

PIECE2_TOP_LOCAL = [0, round(PIECE_LOCAL[1][1] - PIECE_H / 2, 1)]   # haut de la pièce 2 (pile de 2 pièces)


def _reset_beam(S, id, f):
    """Faisceau invisible (from 1) : draw / from / sag remis à 0 d'un coup à l'image f (aucun saut visible)."""
    S.key(id, "draw", f, 0)
    S.key(id, "from", f, 0)
    if "sag" in S.ents[id]["t"]:
        S.key(id, "sag", f, 0)


def _retract(S, id, f, d=9):
    """Le faisceau rentre vers son bout (from -> 1), puis remis à 0 invisible. -> f + d + 1."""
    S.key(id, "from", f, 1, d, "out")
    _reset_beam(S, id, f + d)
    return f + d + 1


def _fade_line(S, id, f, d=6):
    """Trait (shape poly) qui s'efface, puis remis à draw 0 (invisible) et opacité 1."""
    S.key(id, "opacity", f, 0, d, "linear")
    S.key(id, "draw", f + d, 0)
    S.key(id, "opacity", f + d + 1, 1)
    return f + d + 1


def part(S, kit, c):
    toi, rep_a, rep_b = c.toi, c.rep_a, c.rep_b
    f0 = scene_f0(S, "S08")                      # 856
    kit.pin(f0 - 1, ENTRY_P2)
    if S.val("toi", "scale", f0 - 1) == 0:       # partie isolée seulement (« Toi » est visible dès l'image 0)
        toi.enter(f0 - 10, at=list(TOI_REST))
        toi.lower(f0 - 10, 9)

    def chest(n):
        return S.to_world("toi", list(TOI_CHEST), n)

    # ================= S08 : le stylo de « Toi » vérifie, la case « Source » est vide, la ligne casse =================
    f = kit.at("S08", "Une", "« Toi » saute à côté de la carte, bras baissé, son étiquette avec lui ; la case « Source » "
               "vide bat : rien ne prouve ces lignes")
    hop_low(toi, f, TOI_HIGH, 10)
    look(S, "toi", f, -1)
    look(S, "toi", f + 14, 0)
    kit.pulse("source", f + 10, peak=1.1, step=3)

    for i, (mot, what) in enumerate((
            ("inventée,", "la pointe touche la fin de « déductible » ; un trait plein part de la valeur jusqu'à la case "
                          "« Source » : vide, elle bat et rougit ; la ligne vire au rouge et se fend ; la coche "
                          "pointillée de l'IA reste"),
            ("erroné,", "même vérification sur « aucun » : trait vers la case vide, qui rougit ; « Plafond : aucun » "
                        "vire au rouge et se fend"),
            ("fausse.", "même vérification sur « fin du mois » : la case vide rougit ; « Date : fin du mois » casse ; "
                        "les trois coches de l'IA restent sur les trois lignes cassées"))):
        f = kit.at("S08", mot, what)
        hit = toi.tap(f - TAP + 1, list(VALUE_END_A[i]))     # contact SUR le mot : c'est le stylo qui vérifie
        g = kit.draw(f"sonde{i + 1}", hit, 5)                # la preuve cherchée : la valeur -> la case « Source »
        kit.pulse("source", g, peak=1.12, step=3)            # vide : elle bat et rougit
        S.key("source", "stroke", g, RED, 2, "out")
        S.key("source", "stroke", g + 6, DEEP, 4, "inOut")
        S.key(rep_a[i], "red", g + 2, 1, 3, "out")            # le verdict, après la preuve
        S.key(rep_a[i], "crack", g + 2, 1, 9, "out")
        _fade_line(S, f"sonde{i + 1}", g + 4)
    toi.lower(hit + 6, 8)

    # ================= S09 : dite avec aplomb, l'erreur coûte deux pièces =================
    f = kit.at("S09", "Dite", "« Toi » redescend au repos, bras baissé, son étiquette avec lui")
    hop_low(toi, f, TOI_REST, 10)

    f = kit.at("S09", "assurance,", "un reflet blanc balaie encore la carte cassée : elle garde son air sûr")
    S.key("reflet", "p", f - 1, 0)
    S.key("reflet", "p", f, 1, 12, "inOut")

    f = kit.at("S09", "erreur", "le fil en tirets vers les pièces devient rouge et épais")
    S.key("fil_jetons_rouge", "opacity", f, 1, 9, "out")
    S.key("fil_jetons", "opacity", f, 0, 9, "out")

    f = kit.at("S09", "coûter", "la pièce du dessus (« € ») puis la suivante tombent de la pile et sortent ; le « € » "
               "passe sur la pièce 2 ; les deux pièces restantes tremblent")
    kit.drop("piece4", f, out=True, h=80, dx=40, rot=25)
    kit.drop("piece3", f + 4, out=True, h=80, dx=-36, rot=-20)
    kit.ensure("fil_jetons_rouge", "bAt", list(PILE_TOP_LOCAL))
    S.key("fil_jetons_rouge", "bAt", f + 4, PIECE2_TOP_LOCAL, 9, "out")   # le fil suit le haut de la pile
    kit.fade("piece2_euro", f + 6, 1, d=FADE)
    for k, g in enumerate((f + 8, f + 12)):
        kit.shake("piece1", g, amp=5 - k)
        kit.shake("piece2", g, amp=5 - k)

    # ================= S10 : la réponse fausse rangée, une carte neuve =================
    f = kit.at("S10", "Alors,", "la carte cassée (lignes, coches, autocollant « ? ») se réduit et rentre dans la boule "
               "de cristal ; le fil rouge se retire ; les 2 pièces rentrent dans « Toi » (son argent, gardé)")
    kit.vanish("reponse", f, into="boule", d=MORPH)
    kit.vanish("doute", f, into="boule", d=MORPH)
    S.key("fil_jetons_rouge", "from", f, 1, 9, "out")
    S.key("fil_jetons_rouge", "opacity", f + 9, 0)
    S.key("fil_jetons_rouge", "draw", f + 9, 0)
    S.key("fil_jetons_rouge", "from", f + 9, 0)
    S.key("fil_jetons", "draw", f + 9, 0)
    S.key("fil_jetons", "from", f + 9, 0)
    S.key("fil_jetons", "opacity", f + 10, 1)    # draw 0 : invisible
    kit.vanish("pile", f + 6, into=chest(f + 6 + POP), d=POP)

    f = kit.at("S10", "quoi", "la boule de cristal descend au sol, entre l'IA et « Toi »")
    kit.move("boule", f, list(BOULE_SOL), scale=BOULE_SOL_K)

    f = kit.at("S10", "bonne", "le faisceau pointillé de l'IA touche la question ; éclat du cerveau ; une carte "
               "« Réponse » neuve à 4 rangées vides sort de sa tête et grandit au centre ; la question se pose sur son "
               "en-tête")
    kit.draw("f_question", f, 8)
    S.key("eclat_ia", "scale", f - 1, 1)
    S.key("eclat_ia", "p", f - 1, 0)
    S.key("eclat_ia", "p", f, 1, 9, "out")
    S.key("eclat_ia", "scale", f + 10, 0)        # p = 1 : invisible
    S.key("bonne_reponse", "pos", f - 1, list(CARD_A_FROM))
    S.key("bonne_reponse", "scale", f, CARD_A_FROM_K)
    S.key("bonne_reponse", "pos", f + 1, list(CARD_B_C), MORPH, "out")
    S.key("bonne_reponse", "scale", f + 1, 1, MORPH, "out")
    arr = f + 1 + MORPH
    hp, hk = head_pt("bonne_reponse")
    kit.move("pastille", arr, hp, d=9, scale=hk, e="out")
    _retract(S, "f_question", arr - 2)

    # ================= S11 : réponse, source, date, limites =================
    f = kit.at("S11", "réponse,", "un faisceau pointillé de l'IA touche le bord gauche de la carte ; L1 « Réponse : en "
               "général » s'écrit, puce bulle de dialogue")
    kit.draw("f_ecrit", f, 8)
    S.key(rep_b[0], "bulletOn", f, 1)
    kit.type(rep_b[0], f, rate=2, flash=True)

    f = kit.at("S11", "source,", "la case « Source » vide repasse au rouge (le manque de S02) ; le livre tombe dedans, "
               "exactement dans sa silhouette, et le rouge vire au cyan ; le mot « Source » s'efface ; L2 « Source : "
               "site officiel » s'écrit ; un fil plein relie sa puce au livre")
    S.key("source", "stroke", f, RED, 2, "out")
    S.key("source_livre", "stroke", f, RED, 2, "out")
    land = drop_in(kit, "livre", f + 4, h=110)
    S.key("source", "stroke", land - 3, CYAN, 3, "out")
    S.key("source_livre", "stroke", land - 3, CYAN, 3, "out")
    S.key("source", "opacity", land, 0, 6, "linear")
    kit.vanish("source_mot", land, d=POP)
    S.key(rep_b[1], "bulletOn", f, 1)
    kit.type(rep_b[1], f, rate=2, flash=True)
    kit.draw("fil_source", land, 9)

    f = kit.at("S11", "date", "L3 « Date : à jour » s'écrit, puce calendrier")
    S.key(rep_b[2], "bulletOn", f, 1)
    kit.type(rep_b[2], f, rate=2, flash=True)

    f = kit.at("S11", "limites.", "L4 « Limites : ton cas » s'écrit, puce personne ; le faisceau de l'IA s'éteint")
    S.key(rep_b[3], "bulletOn", f, 1)
    end = kit.type(rep_b[3], f, rate=2, flash=True)
    _retract(S, "f_ecrit", end)

    # ================= S12 : la citation, « ta situation » reliée à l'empreinte =================
    f = kit.at("S12", "Par", "une bulle PARLÉE (contour plein, pointe pleine vers la bouche) sort de la bouche de "
               "l'IA, sous la carte")
    kit.pop("citation", f, from_pt=list(IA_MOUTH), to=list(CITATION_C))

    f = kit.at("S12", "« Cette", "1re ligne de la bulle : « « Cette règle s’applique »")
    kit.type("cit_l1", f, rate=2)

    f = kit.at("S12", "général,", "2e ligne « en général, mais dépend » ; « en général » se surligne")
    g = kit.type("cit_l2a", f, rate=2)
    kit.type("cit_l2b", g, rate=2)
    kit.draw("cit_l2a", g, 9, track="mark")

    f = kit.at("S12", "situation ».", "3e ligne « de ta situation » » ; « ta situation » se souligne ; une grande "
               "empreinte digitale sort lentement de la poitrine de « Toi », qui la regarde, contre lui ; elle se pose "
               "au sol ; un fil plein épais relie « ton cas » à l'empreinte ; la puce de « Limites » et l'empreinte "
               "battent ensemble")
    g = kit.type("cit_l3a", f, rate=2)
    h = kit.type("cit_l3b", g, rate=2)
    kit.type("cit_l3c", h, rate=2)
    kit.draw("cit_l3b", h, 9, track="under")
    arr = kit.pop("empreinte", f, scale=1, from_pt=chest(f - 1), to=list(EMPREINTE_TOI), d=12)
    look(S, "toi", f, -1)
    down = kit.move("empreinte", arr + 2, list(EMPREINTE_C), d=10)
    look(S, "toi", down, 0)
    g = kit.draw("fil_empreinte", down, 8)
    kit.pop("fil_empreinte_pt", g - 2, d=5)
    kit.pulse(rep_b[3], g, track="flash", step=3)
    kit.pulse("empreinte", g, peak=1.1, step=3)

    # ================= S13 : prudente, sourcée, où vérifier =================
    f = kit.at("S13", "Une", "la bulle de citation se réduit et rentre dans L1 « Réponse : en général », qui bat")
    end = kit.vanish("citation", f, into=rep_b[0])
    kit.pulse(rep_b[0], end - 3, track="flash", step=3)

    f = kit.at("S13", "prudente", "la ligne « Limites : ton cas » se surligne en bleu clair : la réponse est prudente")
    S.key("surligne_L4", "w", f, SURL_L4_W, 9, "out")
    S.key("surligne_L4", "pos", f, list(SURL_L4_C), 9, "out")
    S.key(rep_b[3], "slotFill", f, 0, 9, "out")

    f = kit.at("S13", "sourcée", "le fil de « Source » vers le livre s'épaissit ; le livre bat : la réponse est "
               "sourcée ; « Toi » saute près du livre, sous la carte")
    S.key("fil_source_gras", "opacity", f, 1, 9, "out")
    kit.pulse("livre", f, peak=round(S.val("livre", "scale", f - 1) * 1.1, 4))
    g = S.word_after("te", f)
    hop_low(toi, g, TOI_LIVRE, 12)
    S.key("nom_toi", "opacity", g, 0, 4, "linear")      # l'étiquette ne se pose pas sur la carte (S13)

    f = kit.at("S13", "vérifier.", "« Toi » touche le livre du stylo : le livre bat, un cadre deep l'entoure et une "
               "coche pleine se trace au bout de la ligne « Source » : vérifié dans le livre")
    hit = toi.tap(f - TAP + 1, list(LIVRE_TAP))
    kit.pulse("livre", hit, peak=round(S.val("livre", "scale", hit - 1) * 1.12, 4), step=3)
    S.key("onde_livre", "pos", hit - 1, list(LIVRE_TAP))
    ring(S, "onde_livre", hit, d=10)
    kit.draw("cadre_livre", hit, 8)
    kit.draw("coche_source", hit + 3, 6)
    toi.lower(hit + 6, 6)

    # ================= S14 : la coche va à l'utile, pas à la certitude =================
    f = kit.at("S14", "C’est", "la boule de cristal se relève sous la carte ; deux cases de coche vides en tirets "
               "paraissent : une à côté de la boule, une sur la carte ; le cadre du livre et le fil vers l'empreinte "
               "s'effacent ; « Toi » remonte à côté de la carte")
    kit.move("boule", f, list(BOULE_CHOIX), d=12, scale=1)
    kit.pop("case_boule", f + 8)
    kit.pop("case_carte", f + 8)
    for id in ("cadre_livre", "fil_empreinte"):
        S.key(id, "opacity", f, 0, 6, "linear")
        S.key(id, "draw", f + 6, 0)
        S.key(id, "opacity", f + 7, 1)           # draw 0 : invisible
    kit.vanish("fil_empreinte_pt", f, d=6)
    hop_low(toi, f, TOI_MID, 14)
    S.key("nom_toi", "opacity", f + 10, 1, FADE, "out")

    f = kit.at("S14", "utile", "le stylo de « Toi » passe d'abord au-dessus de la case de la boule et hésite, puis va "
               "cocher la case de la carte prudente : grande coche pleine")
    look(S, "toi", f, -1)
    toi.reach(f, [CASE_BOULE[0], CASE_BOULE[1] - 14], d=5)
    hit = toi.tap(f + 6, card_pt("b", COCHE_TOI_LOCAL))
    look(S, "toi", hit - 4, 0)
    kit.draw("coche_toi", hit, 6)
    S.key("case_carte", "opacity", hit + 2, 0, 5, "linear")
    S.key("case_carte", "scale", hit + 8, 0)
    toi.lower(hit + 5, 8)

    f = kit.at("S14", "certitude", "la boule de cristal bat et jaillit d'un éclat clair ; sa case reste vide et "
               "s'efface ; puis la boule rentre dans la tête de l'IA et « Toi » redescend au repos")
    kit.pulse("boule", f, peak=1.12)
    S.key("eclat_boule", "scale", f - 1, 1)
    S.key("eclat_boule", "p", f - 1, 0)
    S.key("eclat_boule", "p", f, 1, 9, "out")
    S.key("eclat_boule", "scale", f + 10, 0)     # p = 1 : invisible
    S.key("case_boule", "opacity", f + 8, 0, 6, "linear")
    S.key("case_boule", "scale", f + 14, 0)
    down = S.word_after("affichée", f)
    kit.vanish("boule", down, into=list(IA_HEAD), d=12)
    hop_low(toi, down, TOI_REST, 10)

    # ================= S15 : le faisceau de l'IA retombe ; un humain =================
    f = kit.at("S15", "Et", "la carte cochée se réduit et monte en haut à droite (lignes en barres), la question avec "
               "elle ; le livre la suit à sa gauche, fil compris")
    kit.move("bonne_reponse", f, list(B_SMALL_C), d=MORPH, scale=B_SMALL_K, e="out")
    for id in ["bonne_reponse"] + rep_b:
        S.key(id, "lite", f, 1, MORPH, "out")
    kit.move("livre", f, list(LIVRE_SMALL_C), d=MORPH, scale=LIVRE_SMALL_K, e="out")
    hp, hk = head_pt("bonne_reponse", B_SMALL_C, B_SMALL_K)
    kit.move("pastille", f, hp, d=MORPH, scale=hk, e="out")
    S.key("pastille", "textOp", f, 0, 4, "linear")     # pastille réduite : la pilule cyan seule, sans libellé
    S.key("fil_source_gras", "opacity", f, 0, MORPH, "out")

    f = kit.at("S15", "aucune", "un faisceau pointillé épais part du front de l'IA vers l'empreinte de « Toi » et "
               "avance")
    kit.draw("f_empreinte", f, 18, e="linear")

    f = kit.at("S15", "suffit :", "le faisceau s'arrête net, loin avant l'empreinte : son bout tremble, l'empreinte "
               "tremble ; puis il pend, son bout tombe au sol et il s'efface")
    pb = S.val("f_empreinte", "pb", f - 1)
    for k, dy in enumerate((-6, 5, -5, 4, -3, 0)):
        S.key("f_empreinte", "pb", f + 2 * k, [pb[0] + (3 if k % 2 else -3), pb[1] + dy])
    kit.shake("empreinte", f, amp=10, axis="x")
    kit.shake("empreinte", f + 5, amp=8, axis="x")
    g = f + 12
    S.key("f_empreinte", "sag", g, 80, 14, "in")
    S.key("f_empreinte", "pb", g, [pb[0] + 10, GROUND - 8], 14, "in")
    S.key("f_empreinte", "from", g + 2, 1, 13, "in")
    _reset_beam(S, "f_empreinte", g + 15)
    S.key("f_empreinte", "pb", g + 15, list(pb))

    f = kit.at("S15", "humain.", "un conseiller (figurine papier, étiquette « Conseiller ») arrive en marchant depuis "
               "l'IA et s'arrête là où le faisceau est retombé, face à « Toi », l'empreinte entre eux ; il se penche "
               "vers elle")
    c.conseiller.enter(f, at=list(CONSEILLER_C), frm=CONSEILLER_FROM, d=14)
    S.key("conseiller", "scale", f - 1, 0)       # il grandit en se mettant en marche (pas d'apparition d'un coup)
    S.key("conseiller", "scale", f, FIG_S, 5, "out")
    look(S, "conseiller", f, 1)
    c.conseiller.lean_to(f + 14, 5, d=7)
