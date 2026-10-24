"""V05, partie 2 : S09-S14, images 953-1751 (27 temps forts, 26,6 s). Erreurs 1 (vides), 2 (source), 3 (hypothèse).

Revue 1 (prime sur le détail ci-dessous) : S09 trait pointillé valeur -> fausse carte (« date », « montant »), éclair
plein deep au toucher, la fausse carte s'émiette jusqu'au sol ; S10 : le départ de fil naît sous la pointe (x 702) et
file sous la rangée jusqu'à x 350 (piste aAt) ; S11 : « Toi » (TOI_P11) touche la coche de chaque rangée, le fil part,
le pictogramme du document revient le long du fil jusqu'à la puce ; fil sans document : case de pictogramme vide, le
bout libre se détache, pend puis tombe au sol ; S12 : « Toi » à droite du brief (TOI_P12), souligne « vendre » seul ;
la carte B (compte rendu, « pourrait » en tirets) s'agrandit dans la bande basse ; S13 : brief x 0,75 en (600, 975),
dossier et fils retirés, carte B rangée à gauche, L2 / L4 sans rouge ; S14 : carte B remonte, carte A passe en tirets.

Temps forts (image du film, après calage acoustique) :
S09  date@958  montant@989  intention@1032  S’ils@1075  absents@1088  dossier,@1102  ce@1124  faits.@1147
S10  Deuxième@1167  exiger@1203
S11  Relevé,@1242  contrat,@1262  compte@1281  mail :@1306  pas@1327  certitude.@1360
S12  sourcé,@1424  tromper@1467  formulation.@1491
S13  Troisième@1526  mélanger@1556  faits@1572
S14  « Le@1614  prévoit@1628  « il@1673  ce@1701  même@1720

État d'entrée (etat_initial de S09) : kit.pin(seam(S, "S09") = 952, ENTRY_P2). « Toi » au repos (TOI_REST) ; partie
construite seule : il entre à 943 (garde-fou).

Placements de « Toi » (stylo de 90 px, figurine x 0,9 : allonge confortable 215 px depuis l'épaule) :
- S09-S11 : (870, 690) puis (870, 830). À (885, 760) (storyboard), « 250 000 € » et « mars 2027 » sont à portée,
  mais pas la colonne entière (L1 à 230 px au-dessus de l'épaule) : il monte un peu plus haut (870, 690) pour toucher
  L2 / L4, et glisse jusqu'à (870, 830) pendant que la pointe descend la colonne (S10).
- S12 : sous le coin droit du brief (800, 1060), tête dans le pied de page vide du brief : il touche « vendre » vers le
  haut à gauche, puis souligne L5 de droite à gauche en glissant jusqu'à (445, 1060) (la ligne entière, 353 px, n'est
  pas à portée depuis la droite du brief ; de droite à gauche, le bras ne croise jamais la tête).
- S13-S14 : TOI_S13 (885, 700).

Raccord vers p3 : à l'image 1751, l'état est exactement ENTRY_P3 ; « Toi » à TOI_S13, main au repos.
"""
import math

from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, STYLE, cubic_at  # noqa: F401
from pipeline.story_kit import REACH, TAP  # noqa: F401

from . import (AI_TICK, CARD_W, CARTE_A_C, CARTE_B_C, CARTE_B_PARK, CARTE_B_PARK_S, CARTE_B_S12, DOSSIER_C,  # noqa: F401
               ENTRY_P2, ENTRY_P3, FAIT_C, FAIT_W, FICHE_S13, FICHE_S13_S, HYP_W, MIETTES, NEQ_C, PREVOIT, POURRAIT,
               ROWS, T_CARTE_A, T_CARTE_B, TOI_REST, TOI_S13, TY, VALUE_W, WIRE_DY, WIRE_X, X, seam, vanish)

TOI_P9 = [870, 690]              # S09 : touche L2 et L4 ; S10 : départ de la relecture
TOI_P10 = [870, 830]             # S10 : fin de la relecture (glisse pendant la descente de la pointe)
TOI_P11 = [850, 727]             # S11 : toutes les coches à portée : la pointe touche la rangée dont le fil part
TOI_P12 = [838, 950]             # S12 : à droite du brief (corps hors de la page), « vendre » à portée
TAP_X = X["value"] - 14          # pointe sur la fin de la valeur (repère de la ligne)
L5_X0, L5_X1 = X["text"] - 8, X["value"] + 8     # étendue du surligneur de L5 (cast)
V5_X0 = X["value"] - VALUE_W[4] - 2              # soulignement : « vendre » seul (cast)
STUB = 34                        # S10 : départ de fil de 34 px
FIL_IDS = [f"fil{i + 1}" for i in range(5)]
FLOOR = 1250                     # sol : y monde où tombent miettes et fils pendants
INK, PAPER = STYLE["ink"], STYLE["paper"]


def _wire_len(S, wid, n):
    c = S.wire_cubic(wid, n)
    pts = [cubic_at(c, k / 64) for k in range(65)]
    return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))


def _check_reach(toi, body, targets, n, label):
    """Toutes les cibles à portée confortable depuis le corps en `body` (même calcul que place_for)."""
    s = toi.size
    sh = [body[0] + toi.shoulder[0] * s, body[1] + toi.shoulder[1] * s]
    R = REACH * toi.reach_max(n)
    for t in targets:
        if math.dist(sh, t) > R + 0.5:
            raise SystemExit(f"p2 {label} : cible {t} à {math.dist(sh, t):.0f} px de l'épaule (> {R:.0f})")


def _sweep(S, id, f, d, w, e="out"):
    """Surligneur tiré de gauche à droite : sx 0 -> 1 pendant que le centre glisse du bord gauche à sa place (le bord
    gauche reste fixe). L'élément était à l'échelle 0. -> f + d."""
    c = S.val(id, "pos", f - 1)
    S.key(id, "scale", f - 1, 1)
    S.key(id, "sx", f - 1, 0)
    S.key(id, "pos", f - 1, [round(c[0] - w / 2, 2), c[1]])
    S.key(id, "sx", f, 1, d, e)
    S.key(id, "pos", f, c, d, e)
    return f + d


def _tap_pt(S, lid, n):
    return [round(v, 2) for v in S.to_world(lid, [TAP_X, TY], n)]


def _crumble(S, kit, fid, f, d=15):
    """La fausse carte s'émiette : elle disparaît en 2 images pendant que MIETTES miettes (papier, pointillés de l'IA)
    partent de son empreinte et tombent jusqu'au sol (FLOOR), en tournant, puis s'effacent. -> fin."""
    c = S.to_world(fid, [0, 0], f - 1)
    rot = math.radians(S.val(fid, "rot", f - 1))
    w, h = S.ents[fid]["p"]["w"], S.ents[fid]["p"]["h"]
    S.key(fid, "scale", f, 0, 2, "in")
    S.key(fid, "opacity", f + 2, 0)
    end = f
    for k in range(MIETTES):
        u = (k % 4 - 1.5) / 4 * w
        v = (k // 4 - 0.5) / 2 * h
        p0 = [c[0] + u * math.cos(rot) - v * math.sin(rot), c[1] + u * math.sin(rot) + v * math.cos(rot)]
        mid = f"{fid}_m{k}"
        g = f + k % 3
        dd = d + (k * 5) % 4
        S.key(mid, "pos", g - 1, [round(p0[0], 1), round(p0[1], 1)])
        S.key(mid, "rot", g - 1, round(math.degrees(rot), 1))
        S.key(mid, "scale", g - 1, 1)
        S.key(mid, "pos", g, [round(p0[0] + (k - 3) * 9, 1), FLOOR - 8 * (k % 3)], dd, "in")
        S.key(mid, "rot", g, round(math.degrees(rot) + (-1) ** k * (40 + 15 * k), 1), dd, "linear")
        S.key(mid, "opacity", g + dd, 0, 5, "linear")
        S.key(mid, "scale", g + dd + 5, 0)
        end = max(end, g + dd + 5)
    return end


def part(S, kit, c):
    toi = c.toi
    f0 = seam(S, "S09") + 1                                     # 953
    kit.pin(f0 - 1, ENTRY_P2)
    if S.val("toi", "scale", f0 - 1) == 0:                      # partie seule : « Toi » n'est pas entré (p1)
        toi.enter(f0 - 10, at=list(TOI_REST))

    # ================= S09 : les vides n'ont qu'une fausse carte ; « Toi » les touche, elles s'émiettent =================
    f = kit.at("S09", "date", "un trait pointillé gris de l'IA relie « mars 2027 » (L2) à la fausse carte de la place "
                              "« Vente » : sa seule preuve est une fausse carte ; la carte bat")
    g = kit.draw("lien_vente", f, 8)
    kit.pulse("fantome_vente", g - 2, peak=1.12)

    f = kit.at("S09", "montant", "même trait de « 250 000 € » (L4) à la fausse carte de la place « Contrat », qui bat")
    g = kit.draw("lien_contrat", f, 8)
    kit.pulse("fantome_contrat", g - 2, peak=1.12)

    f = kit.at("S09", "intention", "« vendre » (L5) et, en face, la vraie carte Compte rendu battent ensemble")
    kit.pulse("L5", f, peak=1.12)
    kit.pulse("doc_cr", f, peak=1.12)

    f = kit.at("S09", "S’ils", "« Toi » monte à droite du brief, à hauteur des valeurs, stylo levé ; sa pilule rentre")
    _check_reach(toi, TOI_P9, [_tap_pt(S, "L2", f), _tap_pt(S, "L4", f)], f, "S09")
    g = toi.walk(f, TOI_P9, d=8)
    vanish(kit, "toi_pill", f, d=6)

    def touch(lien, eclair, fid, place, hit):
        """Au contact : un éclair plein deep file de la valeur à la place (3 images), tient 2, rentre ; la fausse carte
        s'émiette quand il arrive ; le trait pointillé de l'IA s'efface ; la place vide tremble."""
        kit.draw(eclair, hit, 3, e="linear")
        kit.draw(eclair, hit + 5, 3, track="from", e="in")
        S.key(eclair, "draw", hit + 8, 0)
        S.key(eclair, "from", hit + 8, 0)
        _crumble(S, kit, fid, hit + 3)
        S.key(lien, "draw", hit + 3, 0, 5, "in")
        kit.shake(place, hit + 4, amp=8)

    f = kit.at("S09", "absents", "la pointe touche « mars 2027 » : un éclair plein file jusqu'à la place « Vente » ; "
                                 "la fausse carte s'émiette et ses miettes tombent au sol ; la place vide tremble")
    hit = toi.tap(g, _tap_pt(S, "L2", g), d=f - g + 1)          # contact sur « absents »
    touch("lien_vente", "eclair_vente", "fantome_vente", "place_vente", hit)

    f = kit.at("S09", "dossier,", "même geste sur « 250 000 € » : éclair jusqu'à la place « Contrat », la fausse carte "
                                  "s'émiette et tombe ; la place vide tremble")
    hit = toi.tap(f - TAP + 1, _tap_pt(S, "L4", f - TAP))
    touch("lien_contrat", "eclair_contrat", "fantome_contrat", "place_contrat", hit)

    f = kit.at("S09", "ce", "la pointe retouche « mars 2027 » : la valeur vire au rouge et casse ; son cadre s’efface ; "
                            "la coche pointillée de l’IA reste")
    hit = toi.tap(f - TAP + 1, _tap_pt(S, "L2", f - TAP))
    S.key("L2", "red", hit, 1, 3, "out")
    S.key("L2", "crack", hit, 1, 9, "out")
    kit.fade("L2_cadre", hit, to=0)

    f = kit.at("S09", "faits.", "la pointe touche « 250 000 € » : rouge, fissurée ; son cadre s’efface ; les coches de "
                                "l’IA restent, l’IA ne bouge pas")
    hit = toi.tap(f - TAP + 1, _tap_pt(S, "L4", f - TAP))
    S.key("L4", "red", hit, 1, 3, "out")
    S.key("L4", "crack", hit, 1, 9, "out")
    kit.fade("L4_cadre", hit, to=0)
    toi.rest(hit + 6)                                           # stylo levé, au repos

    # ================= S10 : « 2 · Source » ; la pointe tire un départ de fil de chaque ligne =================
    f = kit.at("S10", "Deuxième", "le disque actif du repère glisse de 1 à 2 « Source »")
    kit.step(f, 1)

    f = kit.at("S10", "exiger", "la pointe descend le bout des valeurs ; à chaque ligne, un départ de fil plein sort "
                                "sous la pointe et file sous la ligne jusqu'à son début, tourné vers le dossier")
    lead, d = 6, 12
    pts = [[702, round(S.to_world(f"L{i + 1}", [0, TY], f)[1], 2)] for i in range(5)]
    for k in range(d):                                          # contrôle : chaque pointe à portée du corps qui glisse
        p = (k + 1) / d
        body = [TOI_P9[0], TOI_P9[1] + (TOI_P10[1] - TOI_P9[1]) * p]
        tip = [pts[0][0], pts[0][1] + (pts[-1][1] - pts[0][1]) * p]
        _check_reach(toi, body, [tip], f, "S10")
    toi.hop(f + lead, TOI_P10, d, h=0, lean=0)                  # le corps descend avec la pointe
    hits = toi.trace(f, pts, d=d, lead=lead, step=False)
    slide = 10
    for i, (wid, h) in enumerate(zip(FIL_IDS, hits)):
        y = ROWS[i] + WIRE_DY
        xa = X["value"] - 6                                     # sous la pointe, au bout de la valeur
        for k in range(slide + 1):
            q = k / slide
            q = q * q * (3 - 2 * q)
            S.key(wid, "aAt", h + k, [round(xa + (WIRE_X - xa) * q, 2), y])
            S.key(wid, "draw", h + k, round(STUB / _wire_len(S, wid, h + k), 4))
    toi.rest(hits[-1] + 2)

    # ================= S11 : trois fils trouvent un document, deux ne trouvent rien et tombent =================
    t11 = kit.at("S11", "Relevé,", "la pointe touche L1 ; son fil rejoint la carte Relevé, qui bat ; le pictogramme "
                                   "du relevé revient le long du fil et s'allume au début de L1")
    toi.walk(t11 - TAP - 8, TOI_P11, d=8)

    def tap_row(i, f):
        pt = [round(v, 2) for v in S.to_world(f"L{i + 1}", [X["tick"], TY], f - TAP)]   # la coche de l'IA : « preuve ? »
        _check_reach(toi, TOI_P11, [pt], f, f"S11 L{i + 1}")
        return toi.tap(f - TAP + 1, pt)

    def link(i, f):
        wid, doc, pic, lid = f"fil{i + 1}", c.cards[i], f"picto{i + 1}", f"L{i + 1}"
        hit = tap_row(i, f)
        arr = kit.draw(wid, hit, DRAW) - 1
        kit.pulse(doc, arr, peak=1.1)
        S.key(pic, "pos", arr - 1, [round(v, 2) for v in S.wire_cubic(wid, arr)[3]])
        kit.pop(pic, arr, d=4)
        S.along_wire(pic, wid, arr + 4, 8, "inOut", 1, 0, arr)
        bullet = S.to_world(lid, [X["bullet"], TY], arr + 12)
        S.fly(pic, arr + 12, 3, "out", to=bullet)
        kit.ensure(lid, "bulletOn", 0)
        S.key(lid, "bulletOn", arr + 15, 1)
        kit.ensure(lid, "flash", 0)
        S.key(lid, "flash", arr + 15, 1, 3, "out")
        S.key(lid, "flash", arr + 18, 0, 4, "inOut")
        S.key(pic, "scale", arr + 15, 0)

    def dangle(i, f):
        wid, place, lid = f"fil{i + 1}", c.cards[i], f"L{i + 1}"
        hit = tap_row(i, f)
        arr = kit.draw(wid, hit, DRAW) - 1
        proof = S.val(wid, "bAt", arr)
        S.key(place, "pos", arr, S.val(place, "pos", arr - 1))
        for k, dx in enumerate([12, -10, 8, -6, 3, 0]):          # la place vide refuse, fort
            p0 = S.val(place, "pos", arr - 1)
            S.key(place, "pos", arr + k, [round(p0[0] + dx, 2), p0[1]])
        kit.pop(f"{lid}_vide", arr + 2)                        # pas de document : case de pictogramme vide
        S.key(wid, "bAt", arr + 4, [proof[0] + 16, proof[1] + 120], 8, "in")   # le bout libre se détache et pend
        S.key(wid, "sag", arr + 4, 60, 8, "out")

    link(0, t11)
    f = kit.at("S11", "contrat,", "la pointe touche L4 ; son fil file vers la place « Contrat » : vide, elle tremble ; "
                                  "une case de pictogramme vide paraît au début de L4 ; le bout du fil se détache et pend")
    dangle(3, f)
    f = kit.at("S11", "compte", "la pointe touche L5 ; son fil rejoint la carte Compte rendu, qui bat ; son pictogramme "
                                "revient le long du fil et s'allume au début de L5")
    link(4, f)
    f = kit.at("S11", "mail :", "la pointe touche L3 ; son fil rejoint la carte Mail, qui bat ; son pictogramme revient "
                                "et s'allume au début de L3")
    link(2, f)
    f = kit.at("S11", "pas", "la pointe touche L2 ; son fil file vers la place « Vente » : vide, elle tremble ; case de "
                             "pictogramme vide au début de L2 ; le bout du fil se détache et pend")
    dangle(1, f)
    toi.rest(f + 10)
    f = kit.at("S11", "certitude.", "les bouts des deux fils pendants (L2, L4) tombent jusqu'au sol et s’effacent ; "
                                    "« mars 2027 » et « 250 000 € », rouges, tremblent")
    for k, (wid, place) in enumerate((("fil2", "place_vente"), ("fil4", "place_contrat"))):
        g = f + 2 * k
        b0 = S.val(wid, "bAt", g - 1)
        py = S.to_world(place, [0, 0], g)[1]
        S.key(wid, "bAt", g, [b0[0] + 10, round(FLOOR - py, 1)], DROP, "in")
        S.key(wid, "sag", g, 30, DROP, "inOut")
        S.key(wid, "opacity", g + DROP, 0, 5, "linear")
    kit.shake("L2", f, amp=8)
    kit.shake("L4", f, amp=8)

    # ================= S12 : sourcée, mais mal formulée : le compte rendu dit « pourrait » =================
    f = kit.at("S12", "sourcé,", "les trois fils pleins (L1, L3, L5) s’épaississent ensemble, deux fois")
    for wid in ("fil1_halo", "fil3_halo", "fil5_halo"):
        kit.pulse(wid, f, times=2, peak=1, step=3, track="opacity")
    t12 = kit.at("S12", "tromper", "la pointe touche « vendre » : la ligne L5 se surligne ; la carte Compte rendu "
                                   "s'agrandit dans le bas de l'image : « il pourrait vendre », bord en tirets, avec la "
                                   "tête du client")
    vendre = [round(v, 2) for v in S.to_world("L5", [X["value"] - 40, TY], t12)]
    _check_reach(toi, TOI_P12, [vendre], t12, "S12 tap")
    toi.walk(f + 14, TOI_P12, d=12)                             # dans la tenue après « sourcé, »
    hit = toi.tap(t12 - TAP + 1, vendre)
    _sweep(S, "L5_surligne", hit, 8, L5_X1 - L5_X0)
    kit.ensure("L5", "slotFill", 1)
    S.key("L5", "slotFill", hit, 0, 8, "out")
    kit.pop("carteB", t12, from_pt="doc_cr", to=list(CARTE_B_S12), d=MOVE)
    kit.type("carteB_txt", t12 + 6, n=len(T_CARTE_B.replace("\n", "")), rate=4)

    f = kit.at("S12", "formulation.", "la pointe souligne « vendre » d'un trait plein ; en même temps « pourrait » se "
                                      "souligne en tirets dans le compte rendu : deux traits différents sur un même fil")
    a = [round(v, 2) for v in S.to_world("L5", [L5_X1 + 2, TY + 26], f)]
    b = [round(v, 2) for v in S.to_world("L5", [V5_X0, TY + 26], f)]
    _check_reach(toi, TOI_P12, [a, b], f, "S12 souligne")
    lead, d = 4, 10
    hits = toi.trace(f, [a, b], d=d, lead=lead, e="inOut", step=False)
    g = hits[0] + 1                                             # premier pas du tracé
    p0 = S.val("L5_souligne", "pos", g - 1)
    S.key("L5_souligne", "draw", g - 1, 1)                      # tracé de droite à gauche, sous la pointe : bord droit
    S.key("L5_souligne", "sx", g - 1, 0)                        # fixe (pos.x = x1 (1 - sx))
    S.key("L5_souligne", "pos", g - 1, [L5_X1, p0[1]])
    S.key("L5_souligne", "sx", g, 1, d, "inOut")
    S.key("L5_souligne", "pos", g, p0, d, "inOut")
    _sweep(S, "carteB_surligne", g, d, POURRAIT[1] + 12)
    kit.fade("carteB_souligne", g + 2, to=1, d=d - 2)
    toi.rest(hits[-1] + 2)

    # ================= S13 : « 3 · Hypothèse » ; L5 sort du brief en carte A, « Fait » =================
    f = kit.at("S13", "Troisième", "le disque actif du repère glisse de 2 à 3 « Hypothèse »")
    kit.step(f, 2)

    f = kit.at("S13", "mélanger", "le brief recule en bas, grand ; le dossier et ses fils se retirent ; le compte rendu "
                                  "se range à gauche ; L5 sort du brief et grandit en carte « Projet : vendre » cochée par "
                                  "l’IA ; « Toi » monte à droite, hors de la page")
    l5_at = S.to_world("L5", [0, TY], f - 1)
    kit.move("fiche", f, FICHE_S13, d=MORPH, e="out", scale=FICHE_S13_S)
    S.key("dossier", "scale", f, 0.6, MORPH, "in")
    S.key("dossier", "opacity", f + 3, 0, MORPH - 3, "linear")
    S.key("dossier", "scale", f + MORPH, 0)
    S.key("dossier", "opacity", f + MORPH + 1, 1)
    for k in (1, 3, 5):
        S.key(f"fil{k}", "draw", f, 0, 6, "in")
    for lid in ("L2", "L4"):                                    # les erreurs 1 restent fendues, sans rouge vif
        S.key(lid, "red", f, 0, MORPH, "out")
    S.key("L5", "chars", f, 0, 6, "linear")
    S.key("L5_surligne", "scale", f, 0, 6, "out")
    S.key("L5_souligne", "draw", f, 0, 6, "out")
    S.key("L5", "slotFill", f + 4, 1, FADE, "out")              # la rangée vide redevient une bande beige
    kit.move("carteB", f, list(CARTE_B_PARK), d=MORPH + 4, e="inOut", scale=CARTE_B_PARK_S)
    kit.fade("carteB_surligne", f, to=0, d=FADE)
    g = kit.pop("carteA", f, from_pt=l5_at, to=CARTE_A_C, d=MORPH)
    kit.draw("carteA_coche", g, 6)
    toi.walk(f + 2, TOI_S13, d=16)                              # tout droit vers le haut, x 850 -> 885

    f = kit.at("S13", "faits", "une pilule « Fait » surgit au bout de la carte A, avec la coche pointillée de l'IA")
    kit.pop("fait", f)

    # ================= S14 : « prévoit » (plein) ≠ « pourrait » (tirets) ; « Fait » devient « Hypothèse » =================
    f = kit.at("S14", "« Le", "la carte A s’écrit « Le client prévoit de vendre »")
    S.key("carteA_txt", "text", f, T_CARTE_A)
    S.key("carteA_txt", "chars", f, 0)
    kit.type("carteA_txt", f + 1, n=len(T_CARTE_A.replace("\n", "")))

    f = kit.at("S14", "prévoit", "« prévoit » se surligne et se souligne d’un trait plein : affirmé (bord plein)")
    _sweep(S, "carteA_surligne", f, 8, PREVOIT[1] + 12)
    kit.draw("carteA_souligne", f + 2, 8)

    f = kit.at("S14", "« il", "le compte rendu rangé à gauche remonte sous la carte A et reprend sa taille : « il "
                              "pourrait vendre », tête du client, bord et soulignement en tirets : incertain ; "
                              "« pourrait » se surligne")
    kit.move("carteB", f, list(CARTE_B_C), d=MOVE, e="inOut", scale=1, arc=60)
    S.key("carteB_surligne", "opacity", f + MOVE - 1, 1)
    _sweep(S, "carteB_surligne", f + MOVE, 8, POURRAIT[1] + 12)

    f = kit.at("S14", "ce", "un grand « ≠ » surgit entre les deux cartes")
    kit.pop("different", f)

    f = kit.at("S14", "même", "« Toi » touche la coche de « Fait » : elle se retire et la pilule devient « Hypothèse », "
                              "en tirets ; dans les mêmes images, le bord et le soulignement de la carte A passent en "
                              "tirets")
    target = [FAIT_C[0] - 44, FAIT_C[1] + 8]                    # la coche de la pilule
    hit = toi.tap(f - TAP + 1, target)
    S.key("fait_coche", "draw", hit, 0, 4, "in")
    g = hit + 3
    k = round(HYP_W / FAIT_W, 4)
    S.key("hypothese", "sx", g - 1, round(1 / k, 4))
    S.key("hypothese", "scale", g - 1, 1)
    S.key("hypothese", "opacity", g - 1, 0)
    S.key("hypothese", "opacity", g, 1, FADE, "out")
    S.key("hypothese", "sx", g, 1, FADE, "out")
    S.key("fait", "opacity", g, 0, FADE, "out")
    S.key("fait", "sx", g, k, FADE, "out")
    S.key("fait", "scale", g + FADE, 0)
    S.key("fait", "sx", g + FADE, 1)
    S.key("carteA", "stroke", g, PAPER, 8, "inOut")             # le bord plein s'efface sous les tirets
    kit.fade("carteA_tirets", g, to=1, d=8)
    kit.fade("carteA_souligne", g, to=0, d=8)
    kit.fade("carteA_souligne_t", g, to=1, d=8)
    end = toi.rest(hit + 6)
    last = seam(S, "S15")
    assert end <= last, end

    # contrôle du raccord (sans clé) : l'état de l'image `last` est celui d'ENTRY_P3
    for id, tracks in ENTRY_P3.items():
        for track, v in tracks.items():
            cur = S.val(id, track, last, None)
            if cur is None:
                continue
            if isinstance(v, str) or isinstance(cur, str):
                bad = cur != v
            elif isinstance(v, list):
                bad = any(abs(a - b) > 0.5 for a, b in zip(cur, v))
            else:
                bad = abs(cur - v) > 0.01
            if bad:
                kit.warn(f"raccord p3 : {id}.{track} vaut {cur} à {last}, attendu {v}")
    tp = S.val("toi", "pos", last)
    if math.dist(tp, TOI_S13) > 0.5:
        kit.warn(f"raccord p3 : « Toi » à {tp}, attendu {TOI_S13}")
