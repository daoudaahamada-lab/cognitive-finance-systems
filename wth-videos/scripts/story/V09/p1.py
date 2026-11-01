"""V09, partie 1 : S01-S07, images 0-905 (accroche : l'étiquette des trois promesses, le reflet, le repère 1-2-3,
les « ? », la signature ; contexte : coche / astérisques, la sangle rouge qui recopie la coche, coupée par « Toi »,
les promesses rangées ; étape 1 ouverte : carte collée sur la boîte, pièces versées, bouclier). 28 temps forts, 30,2 s.

ÉTAT D'ENTRÉE (image 0 = distribution) : ivoire quadrillé ; au centre l'`etiquette` (560 x 380) et sa ficelle vers
la boîte `produit` (étiquette « Produit » sur son devant) ; sur la carte les trois pilules cyan VIDES (pictogrammes
46 px visibles) ; « Toi » en P1, bras baissé, nommé ; sa pile de 5 pièces (PILE, 60 px plus à gauche qu'au tour 0 :
le stylo baissé ne la touche plus).

Temps forts (image du mot ; `beat(kit, "S01", i, what)`) :
S01  « Capital@6  rendement@38  5 %,@56  disponible@87
S02  papier,@156  parfaite.@188
S03  vidéo,@227  promesses@289  réalités@327
S04  questions@385  avant@415  signer.@428
S05  Une@454  vraie@484  conditionnelle@525  autres.@561
S06  piège,@589  croire@618  ensemble.@664  sépare,@708  une@734  par@740
S07  Pourquoi@767  commencer@780  garantie ?@807  Parce@835  rassure@868  plus.@881

Tour de revue 1 :
- S01 « moment » : le pictogramme horloge de « Disponible » bat (plus d'image figée de 1,8 s dans l'accroche).
- S02 « parfaite. » : deux éclats aux coins de l'étiquette, la pile de pièces se soulève vers l'offre, « Toi »
  avance d'un pas (P1 -> P2) et penche.
- S03 « promesses » : chaque pilule bat (x 1,15) et un pointillé deep la relie à la légende de son étape ;
  « pourquoi » : le repère bat (plus d'image figée).
- S04 « signer. » : le geste part tout de suite (reach e="out"), par-dessus la pile.
- S05 « Une » : le rond « Signature » et son mot rentrent (ils renaîtront au départ de la barre, S10) : le nœud de
  la sangle (S06) ne peut plus se lire comme une signature.
- S06 : la sangle enserre aussi la pastille « 5 % » (qui passe au-dessus d'elle) ; chaque pilule se range dans
  son disque par une réduction uniforme (x 0,15, en arc au-dessus du repère) et son pictogramme reste dans le disque.
- S07 « Pourquoi » : le disque 1 s'allume en montrant le bouclier rangé ; « commencer » : la carte collée (x 0,42)
  ne garde qu'un grand « * » ; l'étiquette « Produit » rentre ; « garantie ? » : la pilule ressort du disque en arc
  au-dessus de la légende, le pictogramme quitte le disque.
"""
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, STYLE  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401

from . import *  # noqa: F401,F403
from . import (DISQUES, ECLATS, ENTRY_P2, ETIQ_C, ETIQ_COLLEE, ETIQ_COLLEE_K, FAUSSES_COCHES, FENTE, LIENS, P1, P2,
               P3, PIECES, PILE, PILE_HAUT, PRODUIT_C, PROMESSE_POINT, PROMESSES, PROMESSES_ECARTEES, PROMESSES_ETIQ,
               Q_ETAPES, SANGLE_NOEUD, SIGNATURE_TIP, TOI_TETE, assert_reach, beat, hold_low, lower, scene_f0,
               walk_low)

LEAN_ATTIRE = -4             # S02 « parfaite. » : penché de 4° vers l'étiquette
Q_TOI = (790, 915)           # S04 : le grand « ? » au-dessus de « Toi » (P2)
RANGE_K = 0.15               # S06 : réduction uniforme des pilules jusqu'à leur disque
RANGE_ARC = [170, 220, 290]  # S06 : arcs qui passent au-dessus du repère (y < 270), jamais sur les légendes
PIECE_AU_DESSUS = (300, 992)
NOEUD_K = 0.85
ECARTEES = [(500, 555), PROMESSES_ECARTEES[1], (500, 790)]
SIGNE_PASSAGE = (720, 1030)  # S04 : la pointe passe d'abord ici (au-dessus de la pile), puis va au rond


def _w(S, id, n, pt=(0, 0)):
    return [round(v, 3) for v in S.to_world(id, list(pt), n)]


def _range(S, kit, pid, f, k, extra=()):
    """La pilule k (et ses `extra` : la pastille) se réduit uniformément en arc jusqu'au disque k ; son pictogramme
    paraît dans le disque à l'arrivée. -> image d'arrivée."""
    disc = list(DISQUES[k])
    p0, s0 = S.val(pid, "pos", f - 1), S.val(pid, "scale", f - 1)
    g = kit.move(pid, f, disc, arc=RANGE_ARC[k], scale=round(s0 * RANGE_K, 4))
    for x in extra:
        q0, k0 = S.val(x, "pos", f - 1), S.val(x, "scale", f - 1)
        off = [(q0[0] - p0[0]) * RANGE_K, (q0[1] - p0[1]) * RANGE_K]
        kit.move(x, f, [disc[0] + off[0], disc[1] + off[1]], arc=RANGE_ARC[k], scale=round(k0 * RANGE_K, 4))
        kit.vanish(x, g, into=disc, d=4)
    kit.vanish(pid, g, into=disc, d=4)
    S.key("marqueur", f"icon{k}", g, 1, 5, "out")
    return g


def part(S, kit, c):
    toi = c.toi
    f0 = scene_f0(S, "S01")
    last = scene_f0(S, "S08") - 1             # dernière image de la partie (p2 commence à S08)
    kit.pin(f0 - 1, {
        "etiquette": {"pos": list(ETIQ_C), "scale": 1},
        "produit": {"pos": list(PRODUIT_C), "scale": 1},
        **{p: {"pos": list(PROMESSES_ETIQ[k]), "scale": 1} for k, p in enumerate(PROMESSES)},
        **{f"{p}_mot": {"chars": 0} for p in PROMESSES},
        "marqueur": {"scale": 0, "on": 0, "lbl": 0},
        "pastille": {"scale": 0},
    })
    if S.val("toi", "scale", f0 - 1) == 0:     # partie construite seule : sans effet ici
        toi.enter(f0 - 10, at=list(P1))
        lower(toi, f0 - 1, d=1)

    # ================= S01 : l'étiquette des trois promesses s'écrit =================
    f = beat(kit, "S01", 0, "« Capital garanti » s'écrit dans la pilule 1 ; son pictogramme bouclier bat une fois")
    kit.type("promesse1_mot", f, rate=1)
    kit.pulse("promesse1_icone", f)

    f = beat(kit, "S01", 1, "« Rendement » s'écrit dans la pilule 2")
    kit.type("promesse2_mot", f, rate=1)

    f = beat(kit, "S01", 2, "la pastille cyan « 5 % » surgit, inclinée, au bout de la pilule 2, à cheval sur le "
                            "bord de l'étiquette")
    kit.pop("pastille", f)

    f = beat(kit, "S01", 3, "« Disponible » s'écrit dans la pilule 3 ; son pictogramme horloge bat à la fin du mot")
    g = kit.type("promesse3_mot", f, rate=1)
    kit.pulse("promesse3_icone", g)
    kit.pulse("promesse3_icone", max(g + 8, S.word("moment", near=3.7)), peak=1.2)   # « à tout moment »

    # ================= S02 : l'offre brille, « Toi » est attiré =================
    f = beat(kit, "S02", 0, "un reflet blanc balaie l'étiquette en diagonale, sous les mots des pilules")
    S.key("reflet", "p", f, 1, 12, "inOut")
    S.key("reflet_promesses", "p", f, 1, 12, "inOut")

    f = beat(kit, "S02", 1, "deux éclats jaillissent aux coins de l'étiquette ; la pile de pièces se soulève vers "
                            "l'offre ; « Toi » avance d'un pas vers elle (P1 -> P2), bras baissé, et penche")
    for k, eid in enumerate(ECLATS):
        S.key(eid, "p", f + 2 * k, 1, 14, "out")
    for k, pid in enumerate(PIECES):
        x, y = PILE[k]
        S.key(pid, "pos", f + k, [x - 4, y - 12], 6, "out")
        S.key(pid, "pos", f + k + 6, [x, y], 7, "inOut")
    g = walk_low(toi, f, P2[0], d=10)
    g2 = toi.lean_to(g, LEAN_ATTIRE)
    hold_low(toi, g, g2)

    # ================= S03 : le repère 1-2-3, une étape par promesse =================
    f = beat(kit, "S03", 0, "le repère 1-2-3 surgit en haut (trois grands disques papier) ; « Toi » se redresse")
    kit.pop("marqueur", f)
    g = toi.lean_to(f, 0)
    hold_low(toi, f, g)
    kit.pulse("marqueur", S.word("pourquoi", near=8.8), peak=1.06)

    f = beat(kit, "S03", 1, "les légendes « Garantie », « Rendement », « Disponible » paraissent ; les trois pilules "
                            "battent l'une après l'autre et un pointillé relie chacune à la légende de son étape")
    S.key("marqueur", "lbl", f, 1, FADE, "out")
    for k, (pid, lid) in enumerate(zip(PROMESSES, LIENS)):
        g = f + 4 * k
        kit.pulse(pid, g, peak=1.15)
        S.key("reflet_promesses", "p", f - 1, 0)
        kit.draw(lid, g, 6)
        S.key(lid, "from", g + 12, 1, 6, "in")
    S.key("reflet_promesses", "p", f, 1, 14, "inOut")

    f = beat(kit, "S03", 2, "un « ? » surgit sous chaque légende (penchés -10°, 0, +10°) : trois questions "
                            "différentes")
    kit.stagger(Q_ETAPES, f, 3, kit.pop)

    # ================= S04 : les questions, avant de signer =================
    f = beat(kit, "S04", 0, "les trois « ? » volent en arc jusqu'au-dessus de « Toi » et s'y fondent en un "
                            "grand « ? »")
    ends = kit.stagger(Q_ETAPES, f, 3, kit.move, list(Q_TOI), arc=90)
    kit.morph(Q_ETAPES, ["q_toi"], ends[-1] - 2, pair=False)

    f = beat(kit, "S04", 1, "un rond de signature surgit sous le coin de l'étiquette ; « Signature » s'écrit à "
                            "sa gauche")
    kit.pop("signature", f)
    kit.type("mot_signature", f + 2, rate=2)

    f = beat(kit, "S04", 2, "« Toi » tend aussitôt son stylo vers le rond, par-dessus la pile, et s'arrête juste "
                            "avant : il ne signe pas ; le grand « ? » bat")
    assert_reach(P2[0], SIGNATURE_TIP, "S04 signature")
    g = toi.reach(f, list(SIGNE_PASSAGE), d=4, e="out")
    g = toi.reach(g, list(SIGNATURE_TIP), d=7, e="inOut")
    kit.pulse("q_toi", g, peak=1.12)

    # ================= S05 : vraie sur un point, conditionnelle sur les autres =================
    f = beat(kit, "S05", 0, "le grand « ? » rentre dans la tête de « Toi » ; son bras redescend ; le rond "
                            "« Signature » et son mot rentrent (pas de signature)")
    kit.vanish("q_toi", f, into=list(TOI_TETE["P2"]))
    lower(toi, f, 8)
    kit.vanish("signature", f + 2)
    S.key("mot_signature", "opacity", f + 2, 0, FADE, "linear")
    S.key("mot_signature", "scale", f + 2 + FADE, 0)

    f = beat(kit, "S05", 1, "une coche ronde imprimée surgit au bout de la pilule « Capital garanti »")
    kit.pop("coche_ronde", f)

    f = beat(kit, "S05", 2, "un astérisque surgit au bout de la pilule 2, puis de la pilule 3")
    kit.pop("ast2", f)
    kit.pop("ast3", f + 4)

    f = beat(kit, "S05", 3, "« * sous conditions » s'écrit en petit en bas de l'étiquette")
    kit.type("sous_conditions", f, rate=2)

    # ================= S06 : le piège de la sangle, coupée par « Toi » =================
    f = beat(kit, "S06", 0, "une sangle rouge se trace autour des trois pilules et de la pastille « 5 % »")
    kit.draw("sangle", f, DRAW)

    f = beat(kit, "S06", 1, "la coche ronde se recopie deux fois : deux coches cerclées de rouge glissent sur les "
                            "astérisques et les cachent (les trois semblent cochées)")
    src = _w(S, "coche_ronde", f - 1)
    for k, (fid, ast) in enumerate(zip(FAUSSES_COCHES, ("ast2", "ast3"))):
        g = f + 3 * k
        kit.pop(fid, g, from_pt=src, to=_w(S, ast, g - 1, (0, -8)), d=10)

    f = beat(kit, "S06", 2, "un nœud rouge surgit au coin bas droit de la sangle ; les trois pilules et la pastille "
                            "battent d'un seul bloc")
    kit.pop("noeud", f, scale=NOEUD_K)
    for id in [*PROMESSES, "pastille"]:
        kit.pulse(id, f, peak=round(1.06 * S.val(id, "scale", f - 1), 4))

    f = beat(kit, "S06", 3, "« Toi » touche le nœud du stylo : la sangle se rompt, ses deux moitiés tombent en "
                            "emportant le nœud et les fausses coches ; les astérisques reparaissent et les pilules "
                            "s'écartent")
    assert_reach(P2[0], SANGLE_NOEUD, "S06 nœud")
    hit = toi.tap(f - TAP + 1, list(SANGLE_NOEUD))
    S.key("sangle", "scale", hit, 0)
    S.key("sangle_g", "scale", hit, 1)
    S.key("sangle_d", "scale", hit, 1)
    kit.drop("sangle_g", hit, out=True, h=60, rot=-20)
    kit.drop("sangle_d", hit, out=True, h=60, rot=20)
    kit.drop("noeud", hit, out=True, h=60, dx=10, rot=20)
    for k, fid in enumerate(FAUSSES_COCHES):
        kit.drop(fid, hit, out=True, h=60, dx=12 + 6 * k, rot=25)
    gone = hit + DROP + 1
    for id in ("sangle_g", "sangle_d", "noeud", *FAUSSES_COCHES):
        S.key(id, "scale", gone, 0)
    for k, pid in enumerate(PROMESSES):
        kit.move(pid, hit + 2, list(ECARTEES[k]))
    lower(toi, hit + 6, 8)

    f = beat(kit, "S06", 4, "la pilule « Capital garanti » (avec sa coche) rapetisse en arc au-dessus du repère et "
                            "se range dans le disque 1, qui garde son pictogramme bouclier")
    _range(S, kit, "promesse1", f, 0)

    f = beat(kit, "S06", 5, "la pilule « Rendement » et sa pastille « 5 % » se rangent dans le disque 2, puis "
                            "« Disponible » dans le disque 3 (pictogrammes % et horloge) : l'étiquette est vide")
    _range(S, kit, "promesse2", f, 1, extra=("pastille",))
    _range(S, kit, "promesse3", f + 8, 2)

    # ================= S07 : étape 1, la garantie ; l'argent de « Toi » dans la boîte =================
    f = beat(kit, "S07", 0, "le disque 1 du repère grandit en disque cyan qui montre le bouclier rangé : étape "
                            "« Garantie »")
    S.key("marqueur", "on", f, 1, POP, "out")

    f = beat(kit, "S07", 1, "la carte vide de l'étiquette se réduit le long de sa ficelle et se colle sur le devant "
                            "de la boîte, où il ne reste qu'un grand « * » ; « Produit » rentre ; la ficelle se "
                            "rétracte")
    g = kit.move("etiquette", f, list(ETIQ_COLLEE), scale=ETIQ_COLLEE_K)
    S.key("ficelle_etiquette", "from", f, 1, MOVE, "inOut")
    S.key("sous_conditions", "opacity", f + 6, 0, FADE, "linear")
    kit.pop("etiq_ast", g - 4)
    kit.vanish("produit_nom", f + 4)

    f = beat(kit, "S07", 2, "la pilule « Capital garanti » (avec sa coche) ressort du disque 1 (le bouclier quitte le "
                            "disque) et descend en arc se poser sous le repère")
    S.key("promesse1", "pos", f - 1, list(DISQUES[0]))
    S.key("promesse1", "opacity", f, 1)
    kit.pop("promesse1", f, scale=1, d=MOVE)
    kit.move("promesse1", f, list(PROMESSE_POINT), arc=110)
    S.key("marqueur", "icon0", f, 0, 6, "out")

    f = beat(kit, "S07", 3, "« Toi » touche sa pile du stylo : ses 5 pièces sautent une à une en arc dans la "
                            "fente de la boîte")
    assert_reach(P2[0], PILE_HAUT, "S07 pile")
    hit = toi.tap(f - TAP + 1, list(PILE_HAUT))
    order = ["piece5", "piece4", "piece3", "piece2", "piece1"]
    assert sorted(order) == sorted(PIECES)
    for k, pid in enumerate(order):
        g = kit.move(pid, hit + 3 * k, list(PIECE_AU_DESSUS), arc=120)
        kit.vanish(pid, g, into=list(FENTE), d=5)
    lower(toi, hit + 6, 8)

    f = beat(kit, "S07", 4, "un grand bouclier cyan sort du pictogramme de la pilule 1, descend en grandissant et "
                            "se pose sur la boîte, par-dessus l'étiquette")
    icone = _w(S, "promesse1_icone", f - 1)
    S.key("bouclier", "pos", f - 1, icone)
    kit.pop("bouclier", f, scale=1, d=MOVE)
    kit.move("bouclier", f, list(ENTRY_P2["bouclier"]["pos"]), arc=60)

    f = beat(kit, "S07", 5, "« Toi » avance vers la boîte (P2 -> P3), bras baissé, et se redresse : rassuré")
    end = walk_low(toi, f, P3[0], d=12)
    assert end <= last + 1, end
