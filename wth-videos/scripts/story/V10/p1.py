"""V10, partie 1 : S01-S07, images 0-867 (accroche, annonce, contexte, premier geste sur le temps). 29 temps forts,
Revue 1 du film : écarts d'exécution listés dans scripts/storyboards/V10.md (« Écarts de mise en scène »), le
code ci-dessous fait foi là où le brief qui suit diffère (S04 points rouges, S05 heurt, case de vérification…).
28,9 s.

ÉTAT D'ENTRÉE (etat_initial de S01, image 0 : c'est l'état de la distribution, rien à épingler) : ivoire quadrillé ;
« Toi » en P2 (628, 1135), bras baissé, nommé par `nom_toi` ; la pastille cyan « Ton argent » en PASTILLE_S01
(760, 700). Tout le reste à l'échelle 0 (offre, barre, interlocuteur…) : la moitié gauche est vide.

Temps forts (image du mot, calage acoustique compris) :
S01  « Offre@8  jusqu’à@36  minuit. »@58
S02  Tu@89  pression@102  monter ?@113
S03  C’est@141  moment@151  ralentir.@163
S04  pièges@242  éviter@256  urgente.@297  vérifier@342  minutes.@379
S05  Pourquoi@405  l’urgence ?@416  pression@457  t’empêche@485  l’offre@515  interlocuteur.@543
S06  numéro@599  arnaques@631  pousse@686  agir@697  réfléchir.@719
S07  réflexe,@764  reprendre@809  main@830  temps.@845

BRIEF, scène par scène (constantes et helpers : `from . import *` des noms de __init__ ; ids entre {}) :
- S01 « Offre » : kit.drop("offre", f) ({offre_titre}, {bouton} déjà dessus). « jusqu’à » : kit.type("offre_ligne",
  f, rate=1). « minuit. » : {compte_rebours} sx 0 -> 1 (STRETCH) ; {cr_maintenant}, {cr_minuit} kit.fade 1 ;
  kit.pop("horloge_cr") ; puis dérive value 1 -> 0,82 linéaire jusqu'à l'image 138 (la fonte continue en S02).
- S02 « Tu » : kit.draw("crochet", f, 9) puis kit.pop("crochet_j", f + 7, d=4) et kit.shake("pastille", f + 9, 5).
  « pression » : S.key crochet sag 0 ; kit.move("pastille", f, PASTILLE_TIRE1, d=12) ; c.toi.lean_to(f, -6, TILT)
  (penché vers l'offre ; vérifier le signe sur une image fixe). « monter ? » : kit.move pastille -> PASTILLE_TIRE2
  (9) ; value perd un bloc (0,88 -> 0,74, 9 images) puis reprend la fonte lente (-> ≈ 0,72 à 141).
- S03 « C’est » : lean_to 0 ; c.toi.reach(f, BAR_END, 9). « moment » : hit = c.toi.tap(f - TAP + 1, BAR_END) (contact
  SUR le mot) ; au contact : value figée (clé instantanée sur sa valeur), kit.pop("pause", hit), ring d'impact
  facultatif. « ralentir. » : crochet sag 0 -> 90 (14, out) ; kit.move pastille -> PASTILLE_S01 (21 images, plus lent
  que MOVE) ; lower(c.toi, f + 6).
- S04 « pièges » : kit.stagger(c.pieges, f, 4, kit.pop, from_pt=PIEGES_FROM) puis chacun kit.move vers
  (MARKER_XS[k], MARKER_Y) (MOVE, arc 80). « éviter » : relais en place : kit.morph(c.pieges, [], f) + marqueur
  scale 1 à f (on 0) et S.key marqueur lbl 0 -> 1 (FADE) : les disques rouges DEVIENNENT le repère. « urgente. » :
  kit.pulse("offre", f, peak=1.05) ; offre stroke INK -> RED -> INK (hex, 2 x 5 images). « vérifier » :
  c.toi.reach(f, SPAWN_S04, 9) ; kit.pop("horloge", f + 9, from_pt=pointe) puis kit.move -> HORLOGE_S04 ;
  kit.pop("horloge_verifier", f + 14) (texte : pop ou fade) ; lower. « minutes. » : horloge value 0 -> 3
  (12, linear) ; kit.fade("horloge_minutes") (scale 1 posé avant).
- S05 « Pourquoi » : kit.vanish de {horloge}, {horloge_verifier}, {horloge_minutes} into = pointe du stylo
  (c.toi.tip(f)) : le stylo garde l'outil. « l’urgence ? » : kit.shake("offre", f, 6) ; kit.pulse("bouton", f,
  peak=1.1) ; kit.drop("pause", f + 2, out=True, rot=15) : c'est l'offre qui relance le temps. « pression » : dérive
  value 0,72 -> 0,45 linéaire jusqu'à l'image 580 ; crochet sag 90 -> 0 (9) ; kit.move pastille -> PASTILLE_TIRE1.
  « t’empêche » : c.toi.reach(f, BAR_BUMP, 6) puis reach vers BAR_BUMP + (40 px vers « Toi ») en 9 « out » (la pointe
  bute et rebondit) ; kit.shake("compte_rebours", f + 6) ; lower. « l’offre » : kit.draw("case_offre", f, 9) : elle
  reste vide. « interlocuteur. » : c.inter.enter(f, at=INTER_POS, frm=INTER_FROM_X, d=16) ; kit.pop("nom_inter", f,
  from_pt=(300, 470)) puis kit.move vers NOM_INTER_LOCAL (14, arc 60) : le nom sort du titre de l'offre.
- S06 « numéro » : kit.move("horloge_cr", f, HORLOGE_CR_N1_LOCAL, d=9, scale=HORLOGE_CR_N1_K) ; kit.pop("n1", f,
  from_pt=BAR_C). « arnaques » : kit.pop("n1_mot") ; kit.pulse("compte_rebours", f, peak=1.05). « pousse » :
  inclinaison de l'interlocuteur (piste lean de la figurine papier, 10° vers « Toi », TILT : c.inter.lean_to) ;
  kit.move pastille -> PASTILLE_S06A (12). « agir » : kit.move pastille -> PASTILLE_S06B (6) ; {bouton} pos +BOUTON_PRESS
  (4 images) et stroke INK -> RED (6). « réfléchir. » (0,7 s APRÈS le bouton) : kit.pop("question", f) en Q_TETE_P2
  avec gs Q_GS_S06, kit.shake rot ±8° ; c.inter.lean_to(f, 0).
- S07 « réflexe, » : kit.vanish("n1", into=BAR_C), kit.vanish("n1_mot", into=BAR_C) ; kit.move horloge_cr ->
  HORLOGE_CR_LOCAL (9, scale 1) ; question gs 96 -> 80. « reprendre » : c.toi.reach(f, BAR_END, 12). « main » :
  hit = c.toi.tap(f - TAP + 1, BAR_END) (la pointe RESTE sur BAR_END : pas de relève, finir par un reach(…, BAR_END, 3)
  si tap relève) ; au contact : value figée (≈ 0,5), kit.pop("pause"), crochet sag 0 -> 60 (12), kit.move pastille ->
  PASTILLE_S07 (12), {bouton} remonte (pos BOUTON_LOCAL) et stroke -> INK : c'est le geste de « Toi » qui annule
  l'appui. « temps. » : drag(c.toi, f, 12, BAR_END, RALLONGE_MID) ; MÊMES images : kit.ensure + {rallonge} scale 1
  à f et S.key("rallonge", "value", f, 0.5, 12, "inOut") : le cyan naît sous la pointe ; kit.move("question", f,
  Q_TETE_S07, d=12) (le « ? » suit « Toi »).

FIN DE PARTIE (= ENTRY_P2, image 867) : « Toi » en P_S07 (754), pointe POSÉE sur RALLONGE_MID (654, 900) ; rallonge
value 0,5 ; pause visible ; crochet mou (sag 60) ; pastille en PASTILLE_S07 ; bouton remonté, encre ; « ? » en
Q_TETE_S07 (gs 80) ; repère on 0, légende visible ; interlocuteur droit en INTER_POS. Rien ne bouge après 860.

"""
import math

from . import *  # noqa: F401,F403
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, STRETCH, TILT  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401

LIFT = 14                                       # pointe au-dessus de la cible avant le contact (comme Figure.tap)
SAG_PRISE = 35                                  # S02 « Tu » : le fil planté est encore un peu mou, puis se tend
CLOCK_DX = -30                                  # S04 : horloge et légendes 30 px plus à gauche que HORLOGE_S04 (air
HORLOGE_P1 = (HORLOGE_S04[0] + CLOCK_DX, HORLOGE_S04[1])   # entre « Quelques minutes » et le buste de « Toi »)
VERIFIER_P1 = (VERIFIER_C[0] + CLOCK_DX, VERIFIER_C[1])
MINUTES_P1 = (MINUTES_C[0] + CLOCK_DX, MINUTES_C[1])
N1_DX = 20                                      # S06 : « n° 1 des arnaques » 20 px à droite de N1_C (storyboard : 330 /
N1_P1 = (N1_C[0] + N1_DX, N1_C[1])              # 445) : de l'air entre l'horloge agrandie et le « n »
ARNAQUES_P1 = (ARNAQUES_C[0] + N1_DX, ARNAQUES_C[1])


def hover_pt(fig, n, target, lift=LIFT):
    """Point à `lift` px de `target`, sur la droite épaule -> cible (image n) : d'où part le coup."""
    A = fig._shoulder(n)
    u = [target[0] - A[0], target[1] - A[1]]
    k = lift / max(1e-6, math.hypot(*u))
    return [round(target[0] - u[0] * k, 2), round(target[1] - u[1] * k, 2)]


def press(fig, f, contact, target, d=None, stay=False):
    """La pointe va au-dessus de `target` dès f (reach en d images, par défaut jusqu'à contact - 3), tient, puis frappe
    en 3 images : contact SUR l'image `contact`. stay=False : relève de LIFT px en 5 images ; stay=True : la pointe
    reste posée (saisie). -> contact."""
    hov = hover_pt(fig, contact, target)
    d = d or (contact - 2 - f)
    fig.reach(f, hov, d)
    fig._tip_line(contact - 2, 3, hov, list(target), "in")
    if not stay:
        fig._tip_line(contact + 1, 5, list(target), hov, "out")
    return contact


def lean_low(fig, f, deg, d=TILT, e="out"):
    """Incline la figurine, bras baissé qui suit (Figure.lean_to remettrait la main au repos, stylo levé). -> f + d."""
    fig.kit.ensure(fig.id, "lean", 0)
    fig.S.key(fig.id, "lean", f, deg, d, e)
    hold_low(fig, f, f + d)
    return f + d


def freeze(S, id, f):
    """La jauge s'arrête net à l'image f (clé instantanée sur sa valeur de f - 1 : la fonte en cours est coupée)."""
    v = round(S.val(id, "value", f - 1), 4)
    S.key(id, "value", f, v)
    return v


def part(S, kit, c):
    toi, inter = c.toi, c.inter

    # ---------- état d'entrée (image 0 = distribution) : épinglé à -1 ----------
    kit.pin(0 - 1, {
        "offre": {"pos": list(OFFRE_C), "scale": 0, "stroke": INK},
        "offre_ligne": {"chars": 0},
        "bouton": {"pos": list(BOUTON_LOCAL), "stroke": INK},
        "compte_rebours": {"sx": 0, "value": 1},
        "cr_maintenant": {"opacity": 0}, "cr_minuit": {"opacity": 0},
        "horloge_cr": {"pos": list(HORLOGE_CR_LOCAL), "scale": 0},
        "pause": {"pos": list(PAUSE_LOCAL), "scale": 0},
        "case_offre": {"scale": 0}, "case_x": {"scale": 0}, "n1_lien": {"draw": 0},
        "crochet": {"draw": 0, "sag": 0},
        "crochet_j": {"scale": 0},
        "pastille": {"pos": list(PASTILLE_S01), "scale": 1},
        "marqueur": {"pos": [MARKER_CX, MARKER_Y], "scale": 0, "on": 0, "active": 0, "lbl": 0},
        "horloge": {"scale": 0, "value": 0},
        "horloge_verifier": {"scale": 0}, "horloge_minutes": {"scale": 0},
        "n1": {"pos": list(N1_C), "scale": 0}, "n1_mot": {"pos": list(ARNAQUES_C), "scale": 0},
        "question": {"pos": list(Q_TETE_P2), "scale": 0, "gs": Q_GS},
        "rallonge": {"scale": 0, "value": 0},
        **{p: {"pos": list(PIEGES_FROM), "scale": 0} for p in PIEGES},
    })
    if S.val(toi.id, "scale", -1) == 0:          # garde-fou (figurine absente) : sans effet, « Toi » est là dès l'image 0
        toi.enter(0, at=list(P2))

    assert_reach(P2[0], BAR_END, "S03/S07 bout de la barre")
    assert_reach(P2[0], BLOCK_S05, "S05 heurt sous la barre")
    assert_reach(P2[0], SPAWN_S04, "S04 horloge au bout du stylo")

    # ================= S01 : « Offre réservée jusqu’à ce soir minuit. » =================
    f = kit.at("S01", "« Offre", "la carte papier « Offre réservée » (bouton « J’investis ») tombe du haut dans la "
                                 "moitié gauche, en face de « Toi » et de sa pastille « Ton argent »")
    drop_in(kit, "offre", f, h=240)      # départ y 170 : hors du bandeau haut (160 px) ; visible sur le mot même

    f = kit.at("S01", "jusqu’à", "« jusqu’à ce soir minuit » s'écrit sous le titre de l'offre")
    kit.type("offre_ligne", f, rate=1)

    f = kit.at("S01", "minuit. »", "sous la carte, la barre rouge du compte à rebours s'étire entre « maintenant » et "
                                   "« minuit », une horloge surgit à son bout gauche ; la barre commence à fondre "
                                   "vers « minuit »")
    S.key("compte_rebours", "sx", f, 1, STRETCH, "out")
    kit.fade("cr_maintenant", f)
    kit.fade("cr_minuit", f)
    kit.pop("horloge_cr", f)
    melt_end = scene_f0(S, "S03") - 3                    # fonte lente jusqu'à S03 (-> S02 « monter ? »)
    S.key("compte_rebours", "value", f + STRETCH, 0.82, melt_end - (f + STRETCH), "linear")

    # ================= S02 : « Tu sens la pression monter ? » =================
    f = kit.at("S02", "Tu", "un fil rouge part du bord droit de l'offre et plante son crochet en J dans la pastille "
                            "« Ton argent », qui tremble : elle est prise")
    S.key("crochet", "sag", f - 1, SAG_PRISE)
    kit.draw("crochet", f, DRAW)
    kit.pop("crochet_j", f + 7, d=4)
    kit.shake("pastille", f + 9, 5)

    f = kit.at("S02", "pression", "le fil rouge se tend et tire la pastille vers l'offre ; « Toi » se penche vers elle "
                                  "malgré lui")
    S.key("crochet", "sag", f, 0, 6, "out")
    kit.move("pastille", f, PASTILLE_TIRE1, d=12)
    lean_low(toi, f, -6, TILT)

    f = kit.at("S02", "monter ?", "second coup de fil : la pastille colle presque au bord de la carte ; la barre rouge "
                                  "perd d'un coup un bloc")
    kit.move("pastille", f, PASTILLE_TIRE2, d=9, e="out")
    S.key("compte_rebours", "value", f, 0.74, 9, "out")
    S.key("compte_rebours", "value", f + 9, 0.66, 50, "linear")      # reprend la fonte lente (coupée au contact)

    # ================= S03 : « C’est le moment de ralentir. » =================
    f = kit.at("S03", "C’est", "« Toi » se redresse et tend le stylo vers le bout droit de la barre rouge")
    fm = S.word_after("moment", f)
    toi.lean_to(f, 0, 9, "out")                  # par le rig (le geste qui suit re-pose le bras)
    hit = press(toi, f, fm, BAR_END)
    kit.at("S03", "moment", "la pointe du stylo touche le bout de la barre : la fonte s'arrête net et un signe "
                            "« pause » se pose au-dessus du bout")
    v_pause = freeze(S, "compte_rebours", hit)
    kit.pop("pause", hit)

    f = kit.at("S03", "ralentir.", "le fil rouge se relâche et pend ; la pastille « Ton argent » revient lentement près "
                                   "de « Toi », qui baisse le bras")
    S.key("crochet", "sag", f, 90, 14, "out")
    kit.move("pastille", f, PASTILLE_S01, d=30, e="inOut")    # revient lentement : se pose vers le début de S04
    lower(toi, f + 6)

    # ================= S04 : « Dans cette vidéo, on va voir les pièges à éviter … vérifier en quelques minutes. » =====
    fv = S.word_after("vidéo", scene_f0(S, "S04"))         # gestes secondaires : pas d'image figée de 2 s
    kit.pulse("offre", fv, peak=1.04)                       # « vidéo » : la carte qui va lâcher les pièges respire
    fw = S.word_after("voir", fv)                           # « voir » : trois petits points rouges sur la carte
    for k, pid in enumerate(PIEGES):
        S.key(pid, "pos", fw - 1, [PIEGES_FROM[0] - 44 + 44 * k, PIEGES_FROM[1]])
        S.key(pid, "scale", fw + 2 * k, 0.3, 6, "out")

    f = kit.at("S04", "pièges", "les trois points rouges grandissent en disques 1, 2, 3 et montent en arc en haut de "
                                "l'image")
    for k, pid in enumerate(PIEGES):
        fk = f + 2 * k
        S.key(pid, "scale", fk, 1, POP, "out")
        kit.move(pid, fk, [MARKER_XS[k], MARKER_Y], d=10, arc=80)

    f = kit.at("S04", "éviter", "les trois disques rouges deviennent le repère 1-2-3 ; sa légende « Délai · Registres "
                                "· Apparence » paraît sous les disques")
    S.key("marqueur", "scale", f, 1)
    kit.morph(PIEGES, [], f)
    S.key("marqueur", "lbl", f + 4, 1, FADE, "out")

    f = kit.at("S04", "urgente.", "l'offre bat une fois et son contour passe au rouge puis revient : les pièges "
                                  "sortaient d'elle")
    kit.pulse("offre", f, peak=1.05)
    S.key("offre", "stroke", f, RED, 5, "out")
    S.key("offre", "stroke", f + 5, INK, 5, "inOut")

    f = kit.at("S04", "vérifier", "« Toi » lève le stylo : à sa pointe naît une horloge deep qui se pose devant lui, "
                                  "en bas à gauche, légendée « Vérifier »")
    S.key("horloge_verifier", "pos", f, list(VERIFIER_P1))     # places de p1 (encore invisibles, échelle 0)
    S.key("horloge_minutes", "pos", f, list(MINUTES_P1))
    g = toi.reach(f - 8, SPAWN_S04, 9)                     # le stylo est levé sur le mot même
    tip = toi.tip(g - 1)
    arr = kit.pop("horloge", f, from_pt=tip, to=HORLOGE_P1, d=MOVE)
    lower(toi, f + 3)
    kit.pop("horloge_verifier", arr - 2)

    f = kit.at("S04", "minutes.", "le secteur deep de l'horloge se remplit de 3 unités ; « Quelques minutes » paraît "
                                  "sous « Vérifier »")
    S.key("horloge", "value", f, 3, 12, "linear")
    S.key("horloge_minutes", "opacity", f - 1, 0)
    S.key("horloge_minutes", "scale", f - 1, 1)
    kit.fade("horloge_minutes", f)

    # ================= S05 : « Pourquoi l’urgence ? Parce que la pression du temps t’empêche … interlocuteur. » ======
    f = kit.at("S05", "Pourquoi", "l'horloge et ses deux légendes se réduisent et rentrent dans la pointe du stylo de "
                                  "« Toi »")
    tip = toi.tip(f - 1)
    for hid in ("horloge", "horloge_verifier", "horloge_minutes"):
        kit.vanish(hid, f, into=tip, d=MORPH)

    f = kit.at("S05", "l’urgence ?", "l'offre secoue sa carte, son bouton « J’investis » bat : la « pause » saute du "
                                     "bout de la barre et tombe")
    kit.shake("offre", f, 6)
    kit.pulse("bouton", f, peak=1.1)
    g = kit.drop("pause", f + 2, out=True, rot=15)
    gone = f + 2 + DROP // 2 + 6                     # fin du fondu de la chute : la « pause » est rangée, invisible
    S.keys("pause", gone, scale=0, pos=list(PAUSE_LOCAL), rot=0)
    S.key("pause", "opacity", gone + 1, 1)

    f = kit.at("S05", "pression", "la barre rouge repart et fond plus vite ; le fil se retend et tire de nouveau la "
                                  "pastille vers l'offre")
    f06, fmain = scene_f0(S, "S06"), S.word_after("main", scene_f0(S, "S07"))
    S.key("compte_rebours", "value", f, 0.57, f06 - f, "linear")
    S.key("compte_rebours", "value", f06, 0.5, fmain - f06, "linear")   # fonte lente jusqu'à la saisie (S07 « main »)
    S.key("crochet", "sag", f, 0, 9, "out")
    kit.move("pastille", f, PASTILLE_TIRE1)

    f = kit.at("S05", "t’empêche", "« Toi » pousse le stylo en diagonale vers l'offre : la barre rouge descend dans sa "
                                   "course et se dresse comme un mur ; choc (anneau), la pointe recule de 60 px, la "
                                   "barre tremble fort")
    C = BLOCK_S05
    toi.reach(f - 5, C, 6, e="in")                           # la pointe arrive sur la barre à l'image du mot
    bar0 = [BAR_LOCAL[0], BAR_LOCAL[1] + 30]
    S.key("compte_rebours", "pos", f - 4, bar0, 4, "out")    # la barre glisse de 30 px dans la course du stylo
    S.key("compte_rebours", "sy", f, 1.6, 3, "out")          # et se dresse (x 1,6)
    S.key("compte_rebours", "sy", f + 9, 1, 6, "inOut")
    for k, dx in enumerate((8, -8, 8, -6, 4, 0)):            # secousse 3 x 8 px
        S.key("compte_rebours", "pos", f + k, [bar0[0] + dx, bar0[1]])
    S.key("compte_rebours", "pos", f + 12, list(BAR_LOCAL), 6, "inOut")
    impact(S, f, C)
    for lid in ("cr_maintenant", "cr_minuit"):              # la barre dressée couvre ses légendes : elles s'effacent
        S.key(lid, "opacity", f - 4, 0, 3, "linear")
        S.key(lid, "opacity", f + 18, 1, FADE, "out")
    A = toi._shoulder(f)
    u = [A[0] - C[0], A[1] - C[1]]
    k = 60 / math.hypot(*u)
    back = [round(C[0] + u[0] * k, 2), round(C[1] + u[1] * k, 2)]
    h = toi.reach(f + 1, back, 9, e="out")                   # recul de 60 px, ease-out 300 ms
    lower(toi, h + 3)

    f = kit.at("S05", "l’offre", "au coin haut droit de l'offre surgit une grande case de vérification (loupe) ; elle "
                                 "tremble, rougit et un grand ✕ rouge s'y trace, puis elle redevient vide")
    kit.pop("case_offre", f)
    case_block(S, kit, f + 10, hold=15)

    f = kit.at("S05", "interlocuteur.", "l'interlocuteur (figurine papier) entre par la gauche face à « Toi » ; son nom "
                                        "« Invest Minuit » sort du titre de l'offre et se pose au-dessus de sa tête")
    walk_d = 16
    inter.enter(f, at=list(INTER_POS), frm=INTER_FROM_X, d=walk_d)
    S.key("nom_inter", "pos", f - 1, [round(v, 3) for v in S.parent_space("nom_inter", [300, 470], f - 1)])
    kit.pop("nom_inter", f)
    S.fly("nom_inter", f, walk_d, "inOut", to=[INTER_POS[0] + NOM_INTER_LOCAL[0], INTER_POS[1] + NOM_INTER_LOCAL[1]],
          arc=60)
    S.key("nom_inter", "pos", f + walk_d, list(NOM_INTER_LOCAL))

    # ================= S06 : « C’est l’arme numéro un des arnaques financières. Elle te pousse à agir … » =========
    f = kit.at("S06", "numéro", "l'horloge du compte à rebours saute au-dessus de la barre et grossit ; un grand "
                                "« n° 1 » rouge surgit de la barre à côté d'elle")
    kit.move("horloge_cr", f, HORLOGE_CR_N1_LOCAL, d=9, scale=HORLOGE_CR_N1_K)
    kit.pop("n1", f, from_pt=BAR_C, to=N1_P1)
    kit.draw("n1_lien", f + 7, 5)                            # trait rouge : l'horloge EST le n° 1

    f = kit.at("S06", "arnaques", "« des arnaques » paraît en rouge à droite du « n° 1 » ; la barre rouge bat une fois")
    S.key("n1_mot", "pos", f - 1, list(ARNAQUES_P1))
    kit.pop("n1_mot", f)
    kit.pulse("compte_rebours", f, peak=1.05)

    f = kit.at("S06", "pousse", "l'interlocuteur se penche vers « Toi » ; le fil rouge tire la pastille contre le bord "
                                "droit de l'offre")
    inter.lean_to(f, 10, TILT)
    kit.move("pastille", f, PASTILLE_S06A, d=12)

    f = kit.at("S06", "agir", "la pastille glisse encore sur le bord de la carte ; le bouton « J’investis » s'enfonce "
                              "et son contour passe au rouge : l'argent part")
    kit.move("pastille", f, PASTILLE_S06B, d=6)
    S.key("bouton", "pos", f, [BOUTON_LOCAL[0], BOUTON_LOCAL[1] + BOUTON_PRESS], 4, "out")
    S.key("bouton", "stroke", f, RED, 6, "out")
    S.key("bouton", "fill", f, RED, 4, "out")                # vraiment enfoncé : plein rouge, libellé papier
    S.key("bouton_mot", "color", f, PAPER, 4, "out")

    f = kit.at("S06", "réfléchir.", "0,7 s après le bouton, un gros « ? » surgit à côté de la tête de « Toi » et "
                                    "tremble : il réfléchit trop tard ; l'interlocuteur se redresse")
    S.key("question", "gs", f - 1, Q_GS_S06)
    g = kit.pop("question", f)
    for t, v, dd in ((g, 8, 2), (g + 2, -8, 3), (g + 5, 5, 3), (g + 8, 0, 3)):
        S.key("question", "rot", t, v, dd, "inOut")
    inter.lean_to(f, 0, TILT)

    # ================= S07 : « Le premier réflexe, c’est donc de reprendre la main sur le temps. » =================
    f = kit.at("S07", "réflexe,", "« n° 1 des arnaques » rentre dans la barre ; l'horloge reprend sa place à son bout "
                                  "gauche ; le « ? » se réduit un peu")
    kit.vanish("n1", f, into=list(BAR_C))
    kit.vanish("n1_mot", f, into=list(BAR_C))
    kit.vanish("n1_lien", f, into=list(BAR_C))
    kit.move("horloge_cr", f, HORLOGE_CR_LOCAL, d=9, scale=1)
    S.key("question", "gs", f, Q_GS, 9, "inOut")

    f = kit.at("S07", "reprendre", "« Toi » tend le stylo vers le bout droit de la barre rouge")
    fm = S.word_after("main", f)
    hit = press(toi, f, fm, BAR_END, d=12, stay=True)
    kit.at("S07", "main", "la pointe saisit le bout de la barre et y reste : la fonte s'arrête, la « pause » "
                          "ressurgit, le fil se relâche, la pastille décolle et le bouton « J’investis » remonte à "
                          "l'encre")
    freeze(S, "compte_rebours", hit)
    S.key("compte_rebours", "value", hit, 0.5)
    kit.pop("pause", hit)
    S.key("crochet", "sag", hit, 60, 12, "out")
    kit.move("pastille", hit, PASTILLE_S07, d=12)
    S.key("bouton", "pos", hit, list(BOUTON_LOCAL), 4, "out")
    S.key("bouton", "stroke", hit, INK, 6, "out")
    S.key("bouton", "fill", hit, PAPER, 6, "out")
    S.key("bouton_mot", "color", hit, INK, 6, "out")

    f = kit.at("S07", "temps.", "« Toi » tire le bout de la barre vers la droite en reculant : au-delà de « minuit », "
                                "la barre s'allonge d'un net morceau cyan ; le « ? » le suit")
    # la rallonge naît sous la pointe : plein cyan qui s'allonge (bord gauche fixe en x 528), sans case vide ; même
    # convention que p2 (pistes w / pos, value 1)
    x0, half = RALLONGE_C[0] - RALLONGE_W / 2, RALLONGE_W / 2
    kit.ensure("rallonge", "w", RALLONGE_W)
    S.key("rallonge", "value", f - 1, 1)
    S.key("rallonge", "w", f - 1, 4)
    S.key("rallonge", "pos", f - 1, [x0 + 2, RALLONGE_C[1]])
    S.key("rallonge", "scale", f, 1)
    S.key("rallonge", "w", f, half, 12, "inOut")
    S.key("rallonge", "pos", f, [x0 + half / 2, RALLONGE_C[1]], 12, "inOut")
    drag(toi, f, 12, BAR_END, RALLONGE_MID)
    kit.move("question", f, Q_TETE_S07, d=12)
    del v_pause
