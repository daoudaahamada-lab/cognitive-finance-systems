"""V14, partie 1 : S01-S07, images 0-855 (28 temps forts, 28,5 s). Accroche (la question envoyée, la réponse d'aplomb
à case « Source » vide, le doute, la pensée « Je ne sais pas », la cible du test), contexte (pensée ravalée,
rembobinage, case « Source » détachée, boule de cristal, valeurs inventées), point 1 : les pièces de « Toi » reliées
à la réponse.

TOUR DE REVUE 1 : pastille plus grande (x 1,3) et arc haut en S01 ; faisceaux de l'IA épais (7 px, gris encre) ; S03
coupé de gestes secondaires sur « IA », « financière », « doit », « savoir » ; pensée à trois ronds (r 12/18/26) ; cible
de S03 avec sa pilule vide (le test annoncé) ; S06 : la branche reste plantée ~12 images dans la case vide (case qui
tremble ±10, contour et livre dessiné qui clignotent en rouge) ; valeurs écrites au bout des traits de la boule,
recoches étalées ; S07 : départ léger (regard, pastille qui bat sur « grave »). Bras de « Toi » BAISSÉ au repos.

ÉTAT D'ENTRÉE : l'image 0 du film = l'état de distribution (cast). Ivoire presque vide : « Toi » en TOI_REST (870, 1144),
VISIBLE (Figure show=True, échelle 0,9), étiquette « Toi » (pill encre, enfant) au-dessus ; pastille « Question
fiscale ? » (630, 1060) échelle 1 ; IA (AI.png 170 px, (165, 1110)) et « Ton IA » (165, 995). Rien d'autre. Pas
d'épingle (la partie commence à l'image 0). Image 0 lisible et immobile : bras baissé dès l'image 0
(c.toi.lower(0, d=1) ou équivalent), sans mouvement visible.
SORTIE : ENTRY_P2 à l'image 855 (voir __init__.py). Tout ce que cette partie commence finit avant 856. Faisceaux
f_lit, f_carte, f_case, f_boule1-3 : draw 0 ET from 0 (clés instantanées une fois invisibles). reflet p = 1 (fin d'un
balayage). « Toi » en TOI_REST, bras baissé, look 0. La cible est rangée dans « Toi » (scale 0).

Ids : toi (c.toi), nom_toi ; ia, nom_ia, eclat_ia ; pastille ; f_lit, f_carte, f_case, f_boule1-3 ; reponse (+ reponse_L1-3,
reponse_ia1-3, reflet) ; source (+ source_livre, source_livre_dos), source_mot ; doute ; pensee (+ pensee_txt),
pensee_rond1-2 ; cible ; rembobiner ; boule ; pile (+ piece1-4, piece4_euro), fil_jetons.
Constantes et aides : __init__.py (head_pt, card_pt, toi_head, look, ring, drop_in, scene_f0 ; SHEET_A, VALUE_END_A…).

BRIEF, scène par scène (images = round(t × 30), avant calage acoustique ; poser CHAQUE temps fort par kit.at / kit.hold
avec un `what` qui dit ce qu'on voit) :
- S01 (0-82) « poses » (7) : c.toi.tap(…, PASTILLE_TAP) avec contact SUR le mot (tap(f - TAP + 1, …)) ; kit.pulse
  ("pastille", contact, step=3, peak=1.1) ; bras qui revient bas. « fiscale » (29) : kit.move("pastille", f,
  PASTILLE_IA, arc=160) (550 ms). « IA. » (61) : kit.draw("f_lit", f, 9) ; kit.pulse("pastille", fin du tracé,
  peak=1.08). Résultat : la question devant l'IA, reliée par le faisceau pointillé.
- S02 (83-165) « répond » (88) : eclat_ia p 0 -> 1 (9 images) ; la carte sort de la tête : S.key reponse pos
  CARD_A_FROM et scale CARD_A_FROM_K à f - 1, puis -> CARD_C / 1 en MORPH ; source et source_mot naissent avec elle
  (kit.pop from_pt près de CARD_A_FROM, même d, à SOURCE_SMALL_C / SOURCE_MOT_SMALL) ; pastille -> head_pt("reponse")
  (kit.move 11 images, échelle 0,8) ; f_lit : rétraction (from). « avec » (100) : les 3 lignes s'écrivent ensemble
  (kit.type rate=3 chacune, valeurs incluses). « aplomb. » (110) : kit.draw des coches reponse_ia1-3 (5 images,
  décalées de 2) ; reflet p 0 -> 1 (12 images). « Et » (132) : kit.hold (rien ne bouge). « faux ? » (151) : la case
  « Source » seule : kit.pulse("source", f, times=2, step=3) ; S.key("source", "stroke", f, RED, 3) ; coches et puces
  immobiles ; 6 images plus tard kit.pop("doute", f + 6, from_pt=toi_head()) (bulle « ? », queue vers la tête).
- S03 (166-398) « Dans » (166) : la bulle devient l'autocollant : S.key("doute", "s", f, 1, MORPH) + kit.move vers
  STICKER_C (même clé). « pourquoi » (220) : kit.pulse("doute", f, track="pulse", step=3). « dire » (304) : pensée :
  kit.pop pensee_rond1, pensee_rond2 (+2), pensee (+4). « « je » (322) : kit.type("pensee_txt", f, rate=1) ; la carte
  reste cochée au-dessus (l'IA affiche le contraire). « tester » (364) : kit.pop("cible", f, scale=CIBLE_S03_K,
  from_pt=poitrine de « Toi » (toi_head() + (0, 40)), to=CIBLE_S03) ; look(S, "toi", f, -1) puis 0 plus tard.
- S04 (399-471) « réflexe » (403) : kit.vanish pensee_txt / pensee into IA_HEAD, puis pensee_rond2, pensee_rond1 (+2,
  +4) : les petits ronds en dernier. « IA, » (422) : kit.pop("rembobiner", f). « c’est » (438) : chars des 3 lignes
  -> 0 (6 images, linéaire) ; coches reponse_ia draw -> 0 (5 images) ; source stroke RED -> DEEP (6 images) ; puis
  kit.vanish("rembobiner", fin + 1). Pastille, autocollant, case et rangées vides restent.
- S05 (472-599) « Une » (472) : kit.vanish("cible", f, into=poitrine de « Toi »). « générative » (496) : eclat_ia
  p 0 -> 1 (relancer depuis 0) ; kit.draw("f_carte", f, 9). « conçue » (525) : la case se détache : kit.move("source",
  f, SOURCE_BIG_C, d=MORPH) + S.key w/h -> 180 x 160 (même clé) + kit.move("source_livre", f, [0, 0],
  scale=SILH_BIG_K) ; kit.move("source_mot", f, SOURCE_MOT_BIG, scale=SOURCE_MOT_BIG_K). « produire » (548) :
  kit.type(Li, f, n=len(clé), rate=2) pour les 3 lignes (intitulés seuls). « réponse. » (570) : kit.draw("f_case",
  f, 9) jusqu'au bord droit de la case (SOURCE_EDGE_RIGHT).
- S06 (600-724) « sans » (608) : S.key f_case pb -> SOURCE_BIG_C (6 images) ; kit.shake("source", fin, axis="x") ;
  puis sag -> 40 et from -> 1 (9 images) : la branche pend et retombe. f_carte se rétracte aussi (from). « peut »
  (648) : kit.pop("boule", f, from_pt=IA_HEAD, to=BOULE_TETE). « fabriquer » (659) : kit.draw f_boule1-3 (6 images,
  décalés de 2), puis kit.type(Li, …, rate=2) de la clé jusqu'au bout (n = clé + valeur) au bout de chaque trait.
  « paraît » (689) : f_boule1-3 from -> 1 ; reflet : S.key p 0 à f - 1 puis -> 1 (12 images) ; coches reponse_ia1-3
  draw -> 1 (5 images, décalées de 2). La boule reste près de l'IA.
- S07 (725-855) « finance ? » (762) : la pile tombe à côté de « Toi » : S.set ou clé pile scale 1 à f - 1, kit.drop
  piece1-4 décalées de 2 images (ou drop_in("pile", f) puis rien) : 4 pièces, « € » sur la pièce du dessus.
  « jamais » (821) : kit.draw("fil_jetons", f, 9) (tirets encre, bas de la carte -> haut de la pile). « théorique. »
  (830) : S.key("pile", "rot", f, -6, 7, "out") puis -> 0 (7 images) : la pile vacille vers la carte (pivot = sol).
PASSATION vers p2 : à 855, la carte d'aplomb pleine (3 lignes écrites, cochées par l'IA, autocollant « ? »), la case
« Source » vide à gauche (deep), la boule en BOULE_TETE, la pile de 4 reliée par le fil encre ; « Toi » au repos.
"""
from . import *  # noqa: F401,F403
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP  # noqa: F401


def part(S, kit, c):
    toi = c.toi
    rows, ticks = c.rep_a, c.ticks_a
    keys = [len(k) for k, _, _ in LINES_A]
    full = [len(k) + len(v) for k, v, _ in LINES_A]

    # Image 0 = distribution (cast). Épingle de principe à -1 : l'état de S01, identique au cast (aucun saut).
    kit.pin(0 - 1, {"pastille": {"pos": list(PASTILLE_C0), "scale": PASTILLE_K0}, "reponse": {"scale": 0},
                    "source": {"scale": 0}, "doute": {"scale": 0}, "pile": {"scale": 0}, "boule": {"scale": 0}})
    if S.val("toi", "scale", 0 - 1) == 0:        # garde-fou (toi est visible dès le cast : sans effet)
        toi.enter(0, at=list(TOI_REST))
    toi.lower(0, d=1)                            # image 0 lisible et immobile : bras baissé, stylo vers le sol

    def chest(n):
        return S.to_world("toi", list(TOI_CHEST), n)

    def reset_beam(id, n):
        """Faisceau invisible (from 1) : draw 0 et from 0 en clés instantanées (contrat ENTRY_P2)."""
        S.key(id, "draw", n, 0)
        S.key(id, "from", n, 0)
        if "sag" in S.ents[id]["t"]:
            S.key(id, "sag", n, 0)

    # ================= S01 « Tu poses une question fiscale à ton IA. » =================
    f = kit.at("S01", "poses", "« Toi » touche du stylo sa grande pastille « Question fiscale ? » : elle bat ; le "
                               "bras redescend")
    hit = toi.tap(f - 6, list(PASTILLE_TAP), d=7)        # contact sur le mot ; approche dès l'image 1
    kit.pulse("pastille", hit, peak=round(PASTILLE_K0 * 1.08, 4), step=3)
    toi.lower(hit + 5, d=8)
    f = kit.at("S01", "fiscale", "la pastille « Question fiscale ? » monte en grand arc et redescend devant le front "
                                 "de l'IA")
    kit.move("pastille", f, list(PASTILLE_IA), arc=260, scale=PASTILLE_IA_K)
    f = kit.at("S01", "IA.", "un faisceau pointillé épais part du front de l'IA et touche le bout gauche de la "
                             "pastille ; la pastille bat une fois : l'IA lit la question")
    g = kit.draw("f_lit", f, DRAW)
    kit.pulse("pastille", g, peak=round(PASTILLE_IA_K * 1.08, 4), step=3)

    # ================= S02 « Elle répond avec aplomb. Et si c’était faux ? » =================
    f = kit.at("S02", "répond", "un éclat jaillit du cerveau de l'IA ; la carte « Réponse » sort de sa tête et "
                                "grandit au centre, avec au pied le mot « Source » et une case en tirets vide (livre "
                                "dessiné, sans livre) ; la pastille se pose sur l'en-tête ; le faisceau se retire")
    S.key("eclat_ia", "p", f, 1, POP, "out")
    kit.pop("reponse", f, scale=1, from_pt=list(CARD_A_FROM), to=list(CARD_C), d=MORPH)
    kit.pop("source", f, scale=1, from_pt=list(CARD_A_FROM), to=list(SOURCE_SMALL_C), d=MORPH)
    kit.pop("source_mot", f, scale=1, from_pt=list(CARD_A_FROM), to=list(SOURCE_MOT_SMALL), d=MORPH)
    hp, hk = head_pt("reponse")
    kit.move("pastille", f, hp, d=MORPH, scale=hk)
    S.key("pastille", "w", f, PASTILLE_DOCK_W, MORPH, "inOut")
    S.key("f_lit", "from", f, 1, 6, "in")
    reset_beam("f_lit", f + 6)
    f = kit.at("S02", "avec", "les trois lignes s'écrivent ensemble, d'un trait : « Règle : déductible », "
                              "« Plafond : aucun », « Date : fin du mois »")
    for r in rows:
        kit.type(r, f, rate=3)
    f = kit.at("S02", "aplomb.", "l'IA coche ses trois lignes en pointillés (coches « ai ») ; un reflet blanc "
                                 "balaie la carte")
    for i, t in enumerate(ticks):
        kit.draw(t, f + 2 * i, 5)
    S.key("reflet", "p", f, 1, 12, "inOut")
    kit.hold("S02", "Et", "tenue : la réponse nette, cochée par l'IA, case « Source » vide au pied ; rien ne bouge")
    f = kit.at("S02", "faux ?", "seule la case « Source » vide bat deux fois et son contour rougit ; puis une "
                                "bulle « ? » sort de la tête de « Toi »")
    kit.pulse("source", f, times=2, step=3)
    S.key("source", "stroke", f, RED, 3, "out")
    kit.pop("doute", f + 6, from_pt=list(toi_head()), to=list(DOUTE_C), d=7)   # posée avant « Dans » (165)

    # ================= S03 « Dans cette vidéo… Et comment tester la tienne. » =================
    f = kit.at("S03", "Dans", "la bulle « ? » de « Toi » se réduit en autocollant cyan « ? » et se colle au coin "
                              "bas droit de la carte")
    S.key("doute", "s", f, 1, MORPH, "inOut")
    kit.move("doute", f, list(STICKER_C), d=MORPH)
    f = kit.at("S03", "pourquoi", "l'autocollant « ? » bat deux fois (+25 %)")
    kit.pulse("doute", f, track="pulse", peak=1.25, times=2, step=3)
    g = S.word_after("IA", f)                    # gestes secondaires (aucun temps fort déplacé) : la tenue se coupe
    for i, t in enumerate(ticks):                # les coches d'aplomb de l'IA battent l'une après l'autre
        kit.pulse(t, g + 3 * i, peak=1.25, step=3)
    g = S.word_after("on", scene_f0(S, "S03"))   # la réponse d'aplomb garde son air sûr : un reflet la balaie
    S.key("reflet", "p", g - 1, 0)
    S.key("reflet", "p", g, 1, 12, "inOut")
    g = S.word_after("financière", f)
    kit.pulse("pastille", g, peak=round(PASTILLE_HEAD_K * 1.08, 4), step=3)
    g = S.word_after("doit", f)                  # la case « Source » vide, rouge, rebat
    kit.pulse("source", g, peak=1.12, step=3)
    g = S.word_after("savoir", f)                # éclat du cerveau de l'IA, juste avant la pensée
    S.key("eclat_ia", "p", g - 1, 0)
    S.key("eclat_ia", "p", g, 1, POP, "out")
    f = kit.at("S03", "dire", "l'IA pense : trois ronds pointillés de plus en plus grands montent de sa tête, puis "
                              "une bulle de pensée pointillée s'ouvre au bout")
    for k in range(3):
        kit.pop(f"pensee_rond{k + 1}", f + 2 * k, d=7)
    kit.pop("pensee", f + 6)
    f = kit.at("S03", "« je", "« Je ne sais pas » s'écrit dans la bulle de pensée, sous la carte qui affiche "
                              "toujours sa réponse cochée")
    kit.type("pensee_txt", f, rate=1)
    f = kit.at("S03", "tester", "une cible sort de la poitrine de « Toi » et se pose au-dessus de son étiquette, une "
                                "pilule vide au centre : un test à venir")
    kit.pop("cible", f, scale=CIBLE_K03, from_pt=chest(f - 1), to=list(CIBLE_S03))
    look(S, "toi", f, -1)

    # ================= S04 « Le réflexe des IA, c’est de répondre. » =================
    f = kit.at("S04", "réflexe", "la pensée « Je ne sais pas » se réduit et redescend dans la tête de l'IA, les "
                                 "ronds en dernier")
    kit.vanish("pensee", f, into=list(IA_HEAD))
    for k, dd in ((3, 3), (2, 5), (1, 7)):
        kit.vanish(f"pensee_rond{k}", f + dd, into=list(IA_HEAD))
    f = kit.at("S04", "IA,", "un pictogramme ◀◀ (rembobiner) paraît au-dessus de la carte")
    kit.pop("rembobiner", f)
    f = kit.at("S04", "c’est", "les trois lignes s'effacent de droite à gauche, les coches pointillées se "
                               "dé-tracent, le contour de la case « Source » repasse au bleu ; puis le ◀◀ se retire : "
                               "carte vierge")
    for r in rows:
        S.key(r, "chars", f, 0, 6, "linear")
    for t in ticks:
        S.key(t, "draw", f, 0, 5, "in")
    S.key("source", "stroke", f, DEEP, 6, "out")
    kit.vanish("rembobiner", f + 7, d=5)
    S.key("rembobiner", "opacity", f + 9, 0, 3, "linear")

    # ================= S05 « Une IA générative est conçue pour produire une réponse. » =================
    f = kit.at("S05", "Une", "la cible se réduit et rentre dans la poitrine de « Toi », qui regarde de nouveau "
                             "devant lui")
    kit.vanish("cible", f, into=chest(f))
    look(S, "toi", f, 0)
    f = kit.at("S05", "générative", "un éclat jaillit du cerveau de l'IA ; un faisceau pointillé part de sa tête "
                                    "vers le bord gauche de la carte")
    S.key("eclat_ia", "p", f - 1, 0)
    S.key("eclat_ia", "p", f, 1, POP, "out")
    kit.draw("f_carte", f, DRAW)
    S.key("eclat_ia", "scale", f + POP, 0)      # éclat fini (p = 1, invisible) : rangé (contrat ENTRY_P2)
    f = kit.at("S05", "conçue", "la case « Source » vide quitte le pied de la carte et glisse à gauche en "
                                "grandissant, le mot « Source » au-dessus, le livre dessiné dedans")
    kit.move("source", f, list(SOURCE_BIG_C), d=MORPH)
    S.key("source", "w", f, SOURCE_BIG_W, MORPH, "inOut")
    S.key("source", "h", f, SOURCE_BIG_H, MORPH, "inOut")
    kit.move("source_livre", f, [0, 0], d=MORPH, scale=SILH_BIG_K)
    kit.move("source_mot", f, list(SOURCE_MOT_BIG), d=MORPH, scale=SOURCE_MOT_BIG_K)
    f = kit.at("S05", "produire", "l'IA n'écrit que la forme : « Règle : », « Plafond : », « Date : », sans "
                                  "valeurs")
    for r, n in zip(rows, keys):
        kit.type(r, f, n=n, rate=2)
    f = kit.at("S05", "réponse.", "une branche du faisceau de l'IA se tend vers le coin bas droit de la case "
                                  "« Source » et s'y arrête")
    kit.draw("f_case", f, DRAW)

    # ================= S06 « Même sans l’information, … paraît crédible. » =================
    f = kit.at("S06", "sans", "la branche entre dans la case « Source » et y reste plantée : vide ; la case tremble, "
                              "son contour et le livre dessiné clignotent en rouge ; puis la branche pend et se "
                              "retire, le faisceau de la carte aussi")
    g = f + 6
    S.key("f_case", "pb", f, list(SOURCE_BIG_C), 6, "out")
    kit.shake("source", g, amp=10, axis="x")
    S.key("source", "stroke", g, RED, 2, "out")
    S.key("source", "stroke", g + 8, DEEP, 4, "inOut")
    for t, col in ((g, RED), (g + 4, DEEP), (g + 7, RED), (g + 11, DEEP)):
        S.key("source_livre", "stroke", t, col)
    h = g + 13                                   # ~12 images plantée dans la case vide
    S.key("f_case", "sag", h, 60, 13, "in")
    S.key("f_case", "from", h + 1, 1, 13, "in")
    S.key("f_carte", "from", h + 1, 1, 13, "in")
    reset_beam("f_case", h + 14)
    reset_beam("f_carte", h + 14)
    f = kit.at("S06", "peut", "une boule de cristal sort de la tête de l'IA et se pose à sa droite")
    kit.pop("boule", f, scale=1, from_pt=list(IA_HEAD), to=list(BOULE_TETE))
    f = kit.at("S06", "fabriquer", "trois traits pointillés partent de la boule ; chaque valeur s'écrit au bout de son "
                                   "trait : « déductible », « aucun », « fin du mois »")
    for i, (r, n) in enumerate(zip(rows, full)):
        g = kit.draw(f"f_boule{i + 1}", f + 2 * i, 6)
        S.key(r, "chars", g, n, 8, "linear")
    f = kit.at("S06", "paraît", "les traits pointillés se retirent ; un reflet balaie la carte et l'IA recoche ses "
                                "trois lignes en pointillés, une à une : la même réponse d'aplomb")
    for i in range(3):
        S.key(f"f_boule{i + 1}", "from", f, 1, 6, "in")
        reset_beam(f"f_boule{i + 1}", f + 6)
    S.key("reflet", "p", f - 1, 0)
    S.key("reflet", "p", f, 1, 12, "inOut")
    for i, t in enumerate(ticks):
        kit.draw(t, f + 6 + 4 * i, 6)

    # ================= S07 « Pourquoi c’est grave en finance ? … jamais théorique. » =================
    g = S.word_after("Pourquoi", scene_f0(S, "S07"))     # départ léger de la scène (aucun temps fort déplacé)
    look(S, "toi", g, -1)
    g = S.word_after("grave", g)
    look(S, "toi", g, 0)
    kit.pulse("pastille", g, peak=round(PASTILLE_HEAD_K * 1.08, 4), step=3)
    f = kit.at("S07", "finance ?", "une pile de quatre pièces (« € » sur la dernière) tombe à côté de « Toi » : "
                                   "son argent")
    S.key("pile", "scale", f - 1, 1)
    for k in range(4):
        S.key(f"piece{k + 1}", "opacity", f - 1, 0)
        drop_in(kit, f"piece{k + 1}", f + 2 * k)
    f = kit.at("S07", "jamais", "un fil en tirets encre descend du bas de la carte jusqu'à la pièce du dessus")
    S.key("fil_jetons", "color", f, INK)        # même encre, posée en clé (hex minuscule au raccord ENTRY_P2)
    kit.draw("fil_jetons", f, DRAW)
    f = kit.at("S07", "théorique.", "la pile vacille vers la carte (6°) puis revient")
    S.key("pile", "rot", f, -6, 7, "out")
    S.key("pile", "rot", f + 7, 0, 7, "inOut")
