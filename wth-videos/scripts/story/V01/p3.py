"""V01, partie 3 : S15-S20, images 1239-1747 (24 temps forts, 16,9 s dont la tenue finale). L'IA passe son brouillon
et se met en retrait ; le poids du conseil, de l'adéquation et de la responsabilité penche du côté du conseiller ; dix
minutes de relecture laissent passer la fiche et arrêtent le brouillon ; Avant / Après ; la pastille devient le bouton.

État d'entrée, épinglé à l'image 1238 : kit.pin(1238, ENTRY_P3) (etat_initial de S15), plus `horloge` (échelle 0) et
`pastille` (opacité 0). Figurines (jamais épinglées) : `toi` à droite de la page (ADV_END de p2), `client` debout en
bas à droite. Partie construite seule (WTH_PARTS=p3) : gardes d'entrée, sans effet dans le film entier.

Temps forts (image du film, calés par kit.at ; « mot n » = début du mot quand l'attaque audible le devance) :
S15  L’IA=1239  prépare.=1259
S16  Toi,=1287 (mot 1286)  tu=1300  gardes=1306  conseil,=1317  l’adéquation=1337  responsabilité.=1373
S17  Dix=1422  minutes=1429  relecture=1442  valent=1461  erreur=1481  devant=1491  client.=1502
S18  Avant,=1532 (mot 1531)  arrives=1552  cherché.=1573
S19  Après,=1594  arrives=1612  compris.=1633
S20  Abonne-toi=1659 (mot 1658)  comprendre=1688  argent.=1711 ; dernière image du film : 1746 (1747 images)

Scène par scène (tour de revue 1) :
- S15 « L’IA » : le client rentre dans le pictogramme de la pastille et le trait du repère tombe en planche (pivot à
  y 1240, planche de 790 px) ; 4 images plus tard, la fiche se réduit (x 0,45) sur le bout gauche et REDEVIENT le
  brouillon de l'IA : tampon, coches pleines, étiquettes et autocollant s'effacent, « 5 ans » et la coche pointillée
  de L5 reviennent ; l'IA regrandit (280 px) sur le bout gauche ; les cercles 1-2-3 se posent et leur chiffre s'efface
  sous le pictogramme de leur jeton ; le conseiller marche au bout droit et grandit (x 1,3). « prépare. » : il range
  son stylo ; le faisceau de l'IA pousse le brouillon en arc jusque dans ses bras (x 0,3, bras derrière la fiche) ; à
  l'arrivée, ses coches, ses étiquettes, l'autocollant et son tampon reviennent : il la reçoit et la fait sienne.
- S16 « Toi, » : pilule « Toi ». « tu » : l'IA descend calmement (300 ms) au sol juste à gauche du pivot, derrière la
  planche, x 0,85, pilule à taille réelle ; son faisceau reste relié à la fiche 0,5 s, pâle, puis s'éteint ; la
  planche reste à plat. « gardes » : il serre la fiche (planche toujours à plat). « conseil, » / « l’adéquation » /
  « responsabilité. » : chaque cercle roule et devient son jeton (34 px) ; la planche penche quand le jeton se pose
  (4°, 8°, 12°) : 19 images immobiles entre l'IA posée et la première bascule.
- S17 « Dix » : la planche devient le chemin (y 1150) ; jetons et « Toi » se réduisent ; l'IA, x 0,55, reste au départ
  du chemin ; le conseiller garde la fiche dans ses bras et revient à x 1 ; fauteuils (x 0,43) au bout. « minutes » :
  l'horloge (352 px) grandit au-dessus de la fiche, qu'il pose sur le chemin devant lui (x 0,45). « relecture » : le
  stylo descend la colonne pendant que le secteur ET l'aiguille des minutes vont de :50 à :00 ; coche sur le coin de
  la fiche. « valent » : la fiche glisse à la table. « erreur » : il tend le stylo en travers du chemin ; le brouillon
  de l'IA sort de sa tête par un faisceau pointillé et fonce. « devant » : il bute sur le stylo (3 traits d'impact, il
  tremble, sa ligne rouge bat) puis repart et rentre dans l'IA : rien ne se brise. « client. » : coche sur la fiche.
- S18 « Avant, » : tout se réduit, l'IA comprise ; fauteuils au centre ; « Avant ». « arrives » : il entre, déjà dans
  l'image, la pile de travers ; pastille x 1, à gauche de sa tête. « cherché. » : un document tombe.
- S19 « Après, » : « Après » ; les 4 documents volent devant la table et fusionnent en la fiche (x 0,6) ; le conseiller
  va s'asseoir dans le fauteuil gauche, face au client. « arrives » : l'autocollant « ? » de L5 devient sa bulle,
  entre eux, queue sur SA tête : il pose la question. « compris. » : le client répond par sa propre bulle, avec la
  pastille cyan à silhouette, qui tombe dans la puce de L5 et bat ; « à poser au RDV » devient la source « RDV 9 h »
  (pictogramme du client) ; ils se penchent de 5° l'un vers l'autre.
- S20 « Abonne-toi » (1659, image du temps fort calé) : la pastille devient « S’abonner » et descend au bouton (fondu
  enchaîné de 3 images avec lui) ; carte de fin 620 x 760 (bas à y 1240), titre 56 px, ligne 36 px, en fondu à
  l'arrivée de la pastille. « comprendre », « argent. » : pointeur, clic.
"""
import math

from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, STRETCH, TILT, _ease
from pipeline.story_kit import frames, lerp

from . import (ADV_PLANK_SCALE, ADV_S14, ADV_S17, AVANT_AT, BROUILLON_SCALE, CHAIRS_S17, CHAIRS_S17_SCALE,
               CHAIRS_S18, CIRCLE_X, CLIENT_S13, CLOCK_S17, CLOCK_S17_SCALE, CX, CYAN, ENTRY_P3, FIG_BASE, GROUND,
               IA_CORNER, IA_GROUND, IA_GROUND_SCALE, IA_PLANK_SCALE, IA_PLANK_X, IA_S17, IA_S17_SCALE, MARKER_GAP,
               MARKER_Y, PAGE_PLANK_SCALE, PAGE_S17, PAGE_S17_SCALE, PATH_C, PATH_TOP, PATH_W, PILL_ICON, PILL_TEXT,
               PILL_W, PLANK_AT, PLANK_H, PLANK_W, TOKEN_H, TOKEN_W, TOKEN_X, TOKENS, fig_pos, morph_out, vanish)

# ---------- places propres à p3 ----------
PLANK_TOP = PLANK_AT[1] - PLANK_H                 # 1164 : dessus de la planche à plat
PAGE_H, PAGE_W = 720, 500                         # fiche de V01 : 500 x 720
PAGE_ON = (480, PLANK_TOP - 2 - PAGE_PLANK_SCALE * PAGE_H / 2)   # sur la planche, devant l'IA (son visage dégagé)
ADV_LX = 328                                      # pieds du conseiller sur la planche (x local) : x monde 863
ARMS_SCALE = 0.30                                 # la fiche dans ses bras : 150 x 216
ARMS_DX = (-50, -8)                               # centre de la fiche / pieds : à l'arrivée, puis serrée (« gardes »)
ARMS_LIFT = 2                                     # bas de la fiche au-dessus du dessus de la planche (+ pente)
TOI_PILL_DY = FIG_BASE + 30                       # « Toi » sous la planche (repère de la figurine, x 1,3)
LV = [-PLANK_H - TOKEN_H / 2 - (TOKEN_H + 4) * k for k in range(3)]   # niveaux de la pile de jetons
ROLL_X = TOKEN_X + TOKEN_W / 2 - 36               # bout droit de la pile : là où le cercle s'étire en jeton
CHAIRS_PNG_H = 306
TABLE = (-5, 8)                                   # dessus de la table de verre, repère des fauteuils à x 1
CLIENT_SEAT = (200, -62)                          # client assis dans le fauteuil droit (repère des fauteuils, x 1)
ADV_SEAT = (-200, -62)                            # le conseiller, au RDV, dans le fauteuil gauche (S19)
FICHE17_TABLE = 0.16                              # fiche posée sur la petite table (S17)
BARRIER = (410, 1066)                             # S17 « erreur » : la pointe du stylo en travers du chemin
TOI18 = fig_pos(400, GROUND)                      # S18 : debout au premier plan, la pile dans les bras
CARD_SCALE = 0.6                                  # cartes de la pile (120 x 150)
PILE_REL = {"doc4": (-96, -22, 10, 11.0), "doc3": (-126, -18, -9, 11.1), "carte_grise2": (-150, 8, -16, None),
            "carte_grise1": (-118, 14, 7, None), "doc2": (-100, 30, -3, 11.7), "doc1": (-134, 38, 6, 11.8)}
PILL_REL = (-135, -112)                           # pastille x 1, sur la pile, à gauche de la tête (tête visible)
FLOOR_DOC = (545, GROUND - 58)                    # doc1 glisse en avant et tombe à plat devant lui
FICHE19, FICHE19_SCALE = (540, 1050), 0.6         # S19 : la fiche devant la table, « Horizon : ? » lisible
ANSWER_SCALE = 1.3                                # la réponse du client : pastille de 57 px
CARD_POS, CARD_H = (540, 860), 760                # carte de fin : bas à y 1240
BTN = (540, CARD_POS[1] + CARD_H / 2 - 56 - 56)   # bouton de la carte de fin


def _catmull(pts, n=24):
    """Points denses d'une courbe de Catmull-Rom passant par `pts`, et leurs abscisses curvilignes."""
    P = [pts[0]] + [list(p) for p in pts] + [pts[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            out.append([0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                               + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in (0, 1)])
    out.append(list(pts[-1]))
    acc = [0.0]
    for a, b in zip(out, out[1:]):
        acc.append(acc[-1] + math.dist(a, b))
    return out, acc


def _at_length(curve, frac):
    out, acc = curve
    target = max(0.0, min(1.0, frac)) * acc[-1]
    for i in range(1, len(out)):
        if acc[i] >= target:
            t = (target - acc[i - 1]) / max(1e-9, acc[i] - acc[i - 1])
            return lerp(out[i - 1], out[i], t)
    return out[-1]


def r2(pt):
    return [round(pt[0], 2), round(pt[1], 2)]


def part(S, kit, c):
    toi, client, sheet = c.toi, c.client, c.sheet
    rows, X, ty = sheet.rows, sheet.x, sheet.ty
    ai_h = c.ai_h
    f0 = round(next(s for s in S.sb["scenes"] if s["id"] == "S15")["t_start"] * S.fps)   # 1239

    kit.pin(f0 - 1, {**ENTRY_P3, "horloge": {"scale": 0}, "pastille": {"opacity": 0}})   # etat_initial de S15
    if S.val("toi", "scale", f0 - 1) == 0:                  # partie construite seule : figurines absentes
        toi.enter(f0 - 10, at=list(ADV_S14))
    if S.val("client", "scale", f0 - 1) == 0:
        kit.pop("client", f0 - 10, to=list(CLIENT_S13))
    if S.val("L1", "chars", f0 - 1) == 0:                   # partie seule : les rangées que p2 écrit (S11)
        kit.pin(f0 - 1, {lid: {"chars": len(p["key"]) + len(p["value"])} for lid, p in sheet.lines})

    # ---------- utilitaires ----------
    def plank_feet(n):
        """Pieds du conseiller sur la planche (point monde du dessus, x local ADV_LX) à l'image n."""
        return S.to_world("planche", [ADV_LX, -PLANK_H], n)

    def ride(fa, fb, feet_at, s=ADV_PLANK_SCALE):
        """Le conseiller suit feet_at(n) image par image, sans saut ni penché (walk d = 1 : le bras suit)."""
        for n in range(fa, fb):
            ft = feet_at(n)
            toi.walk(n, r2([ft[0], ft[1] - FIG_BASE * s]), d=1)

    def arms_pos(feet, dx, rot):
        """Centre de la fiche serrée contre le buste : bas au-dessus de la planche, même penchée."""
        h = ARMS_SCALE * PAGE_H
        lift = ARMS_LIFT + (ARMS_SCALE * PAGE_W / 2 - dx) * math.tan(math.radians(rot)) if rot else ARMS_LIFT
        return [feet[0] + dx, feet[1] - lift - h / 2]

    def chairs_pt(pos, s, local):
        return [pos[0] + local[0] * s, pos[1] + local[1] * s]

    reviewed = ["tampon", "autocollant"] + [f"coche{i + 1}" for i in range(4)] + [f"source{i + 1}" for i in range(5)]

    # =================== S15 « L’IA prépare. » ===================
    f = kit.at("S15", "L’IA", "le client rentre dans le pictogramme de la pastille ; le trait du repère tombe et devient "
               "une planche ; puis la fiche se réduit sur le bout gauche et redevient le brouillon de l'IA (tampon, coches "
               "pleines, étiquettes effacés) ; l'IA regrandit derrière elle ; le conseiller marche au bout droit")
    # le trait du repère se détache et tombe : la planche naît à sa place (même longueur, même épaisseur)
    mk_w = 2 * MARKER_GAP
    kit.fade("marqueur", f, to=0)
    S.key("marqueur", "scale", f + FADE, 0)
    S.key("planche", "pos", f - 1, [CX, MARKER_Y + PLANK_H / 2])
    S.key("planche", "sx", f - 1, round(mk_w / PLANK_W, 4))
    S.key("planche", "sy", f - 1, round(4 / PLANK_H, 4))
    S.key("planche", "scale", f, 1)
    S.key("planche", "pos", f, list(PLANK_AT), DROP, "in")
    S.keys("planche", f, STRETCH, "out", sx=1, sy=1)
    for k in range(3):
        cid = f"cercle{k + 1}"
        S.key(cid, "pos", f - 1, [CIRCLE_X[k], LV[0] + (TOKEN_H - 72) / 2])
        g = kit.pop(cid, f + STRETCH + k, d=6)
        kit.fade(f"{cid}_ico", g + 4, 1, d=FADE)                # le chiffre s'efface sous le pictogramme
    # 4 images plus tard : la fiche se réduit sur la planche et redevient le brouillon de l'IA
    g = f + 4
    S.keys("fiche", g, MOVE, "inOut", pos=r2(PAGE_ON), scale=PAGE_PLANK_SCALE)
    # le client remonte, se réduit et rentre dans le pictogramme de la pastille (qui suit la fiche), image par image
    dc = 12
    c0 = S.val("client", "pos", f - 1)
    s0 = S.val("client", "scale", f - 1)
    start = S.to_world("pastille_fiche", PILL_ICON, f - 1)
    route = _catmull([c0, [c0[0] - 40, 760], [560, 560], start])
    for n, p in frames(f, dc, "inOut"):
        icon = S.to_world("pastille_fiche", PILL_ICON, n)
        pt = _at_length(route, p)
        pt = [pt[0] + (icon[0] - start[0]) * p, pt[1] + (icon[1] - start[1]) * p]
        S.key("client", "pos", n, r2(pt), 1, "linear")
        S.key("client", "scale", n, round(max(0.05, s0 * (1 - 1.15 * p)) if p < 0.999 else 0.05, 4), 1, "linear")
    S.key("client", "scale", f + dc, 0)
    S.key("client", "opacity", f + dc, 0)
    for id in reviewed:
        kit.fade(id, g, 0, d=6)
    S.key("L5", "fall", g, 0, 6, "out")                       # « 5 ans » revient, sans rature
    S.key("L5", "strike", g, 0, 6, "out")
    S.key("coche_ia5", "draw", g, 1, 6, "out")                # la coche pointillée de L5 aussi
    # l'IA regrandit sur le bout gauche, socle sur la planche ; sa pilule sous la planche, à l'échelle 1
    ia_on = [IA_PLANK_X, PLANK_TOP - IA_PLANK_SCALE * ai_h / 2]
    pill_low = [0, round((PLANK_AT[1] + 8 + 35 - ia_on[1]) / IA_PLANK_SCALE, 1)]
    S.keys("ia", g, MOVE, "inOut", pos=r2(ia_on), scale=IA_PLANK_SCALE)
    S.keys("ia_pill", g, MOVE, "inOut", pos=pill_low, scale=1)
    # le conseiller marche jusqu'au bout droit et grandit (x 1,3)
    adv_on = plank_feet(f + DROP + 2)                         # planche posée, à plat
    to = r2([adv_on[0], adv_on[1] - FIG_BASE * ADV_PLANK_SCALE])
    toi.walk(g, to, d=MOVE)
    toi.scale_to(g, ADV_PLANK_SCALE, d=MOVE)

    f = kit.at("S15", "prépare.", "le conseiller range son stylo ; le faisceau pointillé de l'IA pousse le brouillon en "
               "arc jusque dans ses bras ; à l'arrivée, ses coches pleines, ses étiquettes, l'autocollant « ? » et son "
               "tampon reviennent : il le reçoit et le fait sien")
    toi.stow(f)
    toi.set_z(f, 7.9, tool_z=7.8)                             # la fiche devant le buste ET devant le bras
    g = f + 2
    feet = plank_feet(g)
    S.fly("fiche", g, MOVE, "inOut", to=r2(arms_pos(feet, ARMS_DX[0], 0)), scale=ARMS_SCALE, arc=150)
    for n in range(f - 1, g + MOVE):
        S.key("faisceau_passe", "pb", n, r2(S.to_world("fiche", [-PAGE_W / 2, 0], n)), 1, "linear")
    kit.draw("faisceau_passe", f, 3)
    S.key("faisceau_passe", "from", g + MOVE, 1, 6, "in")
    S.key("faisceau_passe", "draw", g + MOVE + 6, 0)
    S.key("faisceau_passe", "from", g + MOVE + 6, 0)
    land = g + MOVE
    S.key("L5", "fall", land, 1, 6, "out")                    # sa relecture revient avec la fiche
    S.key("L5", "strike", land, 1)
    S.key("coche_ia5", "draw", land, 0.5)
    for id in reviewed:
        if id != "tampon":
            kit.fade(id, land, 1, d=6)
    S.key("tampon", "scale", land, 1.4)                       # le tampon s'abat de nouveau : il la fait sienne
    S.key("tampon", "opacity", land, 1)
    S.key("tampon", "scale", land + 1, 1, 6, "out")

    # =================== S16 « Toi, tu gardes le conseil, l’adéquation et la responsabilité. » ===================
    f = kit.at("S16", "Toi,", "la pilule « Toi » surgit sous le conseiller")
    S.key("toi_pill", "pos", f - 1, [0, TOI_PILL_DY])
    kit.pop("toi_pill", f)

    f = kit.at("S16", "tu", "l'IA descend calmement de la planche au sol, juste à gauche du pivot, derrière la planche, "
               "face au conseiller, sa pilule à taille réelle ; son faisceau reste relié à la fiche un instant, pâle, "
               "puis s'éteint ; la planche reste à plat")
    d_ia = POP
    S.key("ia", "z", f + d_ia - 1, 6.5)                      # au sol, devant la planche : elle ne la traverse pas
    S.key("ia_pill", "z", f + d_ia - 1, 6.6)
    S.keys("ia", f, d_ia, "inOut", pos=list(IA_GROUND), scale=IA_GROUND_SCALE)
    S.keys("ia_pill", f, d_ia, "inOut", pos=[-150, -10], scale=round(1 / IA_GROUND_SCALE, 4))
    g = f + d_ia                                              # posée à 1309
    kit.ensure("faisceau_passe", "opacity", 1)
    S.key("faisceau_passe", "opacity", g - 1, 0.55)
    for n in range(g - 1, g + 16):
        S.key("faisceau_passe", "pb", n, r2(S.to_world("fiche", [-PAGE_W / 2, 0], n)), 1, "linear")
    kit.draw("faisceau_passe", g, 3)
    S.key("faisceau_passe", "from", g + 12, 1, 4, "in")
    S.key("faisceau_passe", "draw", g + 16, 0)
    S.key("faisceau_passe", "from", g + 16, 0)
    S.key("faisceau_passe", "opacity", g + 16, 1)

    fg = kit.at("S16", "gardes", "il serre la fiche contre lui ; la planche reste à plat")

    def to_token(k, fk, arc):
        """Le cercle k roule (360°) jusqu'au bout de la pile et s'étire en jeton k (relais) ; ceux qui attendent
        montent sur le nouveau jeton ; au moment où le jeton se pose, la planche penche de 4° de plus."""
        cid, jid = f"cercle{k + 1}", f"jeton{k + 1}"
        S.key(cid, "pos", fk, [ROLL_X, LV[k]], DROP, "inOut", arc=arc)
        S.key(cid, "rot", fk, 360, DROP, "inOut")
        r = fk + DROP
        S.key(jid, "pos", r - 1, [ROLL_X, LV[k]])
        S.key(jid, "w", r - 1, TOKEN_H)
        S.key(jid, "text", r - 1, "")                         # le pictogramme seul, comme le cercle
        S.key(jid, "scale", r, 1)
        S.key(cid, "scale", r, 0)
        S.key(cid, "opacity", r, 0)
        S.keys(jid, r, STRETCH, "out", w=TOKEN_W, pos=[TOKEN_X, LV[k]])
        S.key(jid, "text", r + 3, TOKENS[k][0])
        for m in range(k + 1, 3):
            S.key(f"cercle{m + 1}", "pos", r - 2, [CIRCLE_X[m], LV[k + 1]], 4, "out")
        S.key("planche", "rot", r, 4 * (k + 1), TILT, "out")
        return r

    f = kit.at("S16", "conseil,", "le cercle 1 roule jusqu'au conseiller et s'étire en jeton « Conseil » ; quand il se "
               "pose, la planche penche de son côté (4°)")
    to_token(0, f, 75)
    f = kit.at("S16", "l’adéquation", "le cercle 2 roule et devient « Adéquation », empilé sur le premier ; 8°")
    to_token(1, f, 75)
    f = kit.at("S16", "responsabilité.", "le cercle 3 roule et devient « Responsabilité », en haut de la pile ; 12° ; "
               "l'IA reste au sol, à côté, visible")
    r3 = to_token(2, f, 0)
    f_end = r3 + TILT

    # le conseiller et la fiche suivent le bout de la planche, image par image (sans saut)
    def dx_at(n):
        return lerp(ARMS_DX[0], ARMS_DX[1], _ease("out", min(1.0, max(0.0, (n - fg + 1) / 9))))
    ride(fg, f_end, plank_feet)
    for n in range(fg, f_end):
        S.key("fiche", "pos", n, r2(arms_pos(plank_feet(n), dx_at(n), S.val("planche", "rot", n))), 1, "linear")

    # =================== S17 « Dix minutes de relecture valent mieux qu’une erreur devant le client. » =============
    f = kit.at("S17", "Dix", "la planche se remet à plat et devient un chemin ; jetons et « Toi » se réduisent ; l'IA "
               "reste, petite, au départ du chemin ; le conseiller garde la fiche dans ses bras et va au milieu du "
               "chemin ; les fauteuils apparaissent au bout, le client assis à droite")
    S.keys("planche", f, MORPH, "out", pos=[PATH_C[0], PATH_C[1] + PLANK_H / 2], rot=0,
           sx=round(PATH_W / PLANK_W, 4))
    S.key("chemin", "pos", f - 1, list(PATH_C))
    S.key("chemin", "scale", f + MORPH, 1)                  # même trait, même place : relais invisible
    vanish(kit, "planche", f + MORPH, d=6)                  # le pivot rentre dans le chemin
    morph_out(kit, ["jeton1", "jeton2", "jeton3", "toi_pill"], f)
    ia17 = [IA_S17, PATH_TOP - IA_S17_SCALE * ai_h / 2]
    S.keys("ia", f, MOVE, "inOut", pos=r2(ia17), scale=IA_S17_SCALE)
    S.keys("ia_pill", f, MOVE, "inOut", pos=[0, -175], scale=round(1 / IA_S17_SCALE, 4))   # au-dessus de sa tête
    a = S.val("toi", "pos", f - 1)
    a_feet = [a[0], a[1] + FIG_BASE * ADV_PLANK_SCALE]
    b_feet = [ADV_S17[0], ADV_S17[1] + FIG_BASE]
    for n in range(f, f + MOVE):                              # il quitte vite le bout de la planche, en revenant à x 1
        p = _ease("out", (n - f + 1) / MOVE)
        s = lerp(ADV_PLANK_SCALE, 1.0, p)
        ft = lerp(a_feet, b_feet, p)
        toi.walk(n, r2([ft[0], ft[1] - FIG_BASE * s]), d=1)
    toi.scale_to(f, 1.0, d=MOVE, e="out")
    for n in range(f, f + MOVE):                              # la fiche reste dans ses bras
        tp, s = S.val("toi", "pos", n), S.val("toi", "scale", n)
        S.key("fiche", "pos", n, r2([tp[0] + ARMS_DX[1] * s / ADV_PLANK_SCALE,
                                     tp[1] + FIG_BASE * s - ARMS_LIFT - ARMS_SCALE * PAGE_H / 2]), 1, "linear")
    toi.set_z(f + MORPH, 15, tool_z=15.5)
    toi.unstow(f + MOVE)
    fc = f + 4                                              # le conseiller a quitté le bout du chemin
    S.key("fauteuils", "pos", fc - 1, list(CHAIRS_S17))
    kit.pop("fauteuils", fc, scale=CHAIRS_S17_SCALE, d=6)
    S.key("client", "pos", fc - 1, r2(chairs_pt(CHAIRS_S17, CHAIRS_S17_SCALE, CLIENT_SEAT)))
    kit.pop("client", fc, scale=CHAIRS_S17_SCALE, d=6)

    f = kit.at("S17", "minutes", "l'horloge de 9 h grandit au-dessus de la fiche ; il pose la fiche sur le chemin, "
               "devant lui")
    S.key("horloge", "pos", f - 1, list(CLOCK_S17))
    S.key("secteur", "value", f - 1, 0)
    kit.pop("horloge", f, scale=CLOCK_S17_SCALE, d=10)
    S.key("aiguille", "scale", f, 1)
    S.fly("fiche", f + 1, 9, "inOut", to=r2(PAGE_S17), scale=PAGE_S17_SCALE)

    f = kit.at("S17", "relecture", "le stylo descend la fiche ligne par ligne pendant que le secteur cyan et l'aiguille "
               "des minutes vont de :50 à :00, au même rythme ; puis une coche pleine se trace sur son coin")
    pts = [S.to_world("fiche", sheet.pt(i, "tick"), f) for i in range(5)]
    hits = toi.trace(f - 4, pts, d=18, lead=4)
    S.key("secteur", "value", hits[0] + 1, 10, hits[-1] - hits[0], "linear")
    S.key("aiguille", "rot", hits[0] + 1, 0, hits[-1] - hits[0], "linear")
    corner = S.to_world("fiche", [PAGE_W / 2 - 6, -PAGE_H / 2 - 4], f)
    S.key("coche_relue", "pos", f - 1, r2(corner))
    S.key("coche_relue", "scale", f - 1, 1)
    kit.draw("coche_relue", hits[-1] + 1, 6)
    toi.rest(hits[-1] + 2, 8)

    f = kit.at("S17", "valent", "la fiche relue, avec sa coche, glisse jusqu'à la table entre les fauteuils ; il garde "
               "son stylo levé")
    tbl = chairs_pt(CHAIRS_S17, CHAIRS_S17_SCALE, TABLE)
    on_table = [tbl[0], tbl[1] - 2 - FICHE17_TABLE * PAGE_H / 2]
    S.keys("fiche", f, MOVE, "inOut", pos=r2(on_table), scale=FICHE17_TABLE)
    k17 = FICHE17_TABLE / PAGE_S17_SCALE
    corner_t = [on_table[0] + (PAGE_W / 2 - 6) * FICHE17_TABLE, on_table[1] + (-PAGE_H / 2 - 4) * FICHE17_TABLE]
    S.keys("coche_relue", f, MOVE, "inOut", pos=r2(corner_t), scale=round(max(0.5, k17), 3))

    f = kit.at("S17", "erreur", "le conseiller tend son stylo en travers du chemin ; le brouillon de l'IA (contour "
               "tireté, coches pointillées, ligne rouge) sort de sa tête par un faisceau pointillé et fonce vers lui")
    toi.reach(f, list(BARRIER), d=6, step=False)
    head = S.to_world("ia", c.brain_front, f - 1)
    bump = [BARRIER[0] - BROUILLON_SCALE * PAGE_W / 2 - 4, PATH_TOP - BROUILLON_SCALE * PAGE_H / 2]
    S.key("brouillon", "pos", f - 1, r2(head))
    S.key("brouillon", "scale", f - 1, 0)
    S.key("brouillon", "scale", f, 0.08)
    S.key("brouillon", "scale", f + 1, BROUILLON_SCALE, 8, "out")
    S.key("brouillon", "pos", f + 1, r2(bump), 9, "in")
    for n in range(f - 1, f + 11):
        S.key("faisceau_passe", "pb", n, r2(S.to_world("brouillon", [-PAGE_W / 2, 0], n)), 1, "linear")
    kit.draw("faisceau_passe", f, 3)

    f = kit.at("S17", "devant", "le brouillon bute sur le stylo levé : 3 traits d'impact, il tremble, sa ligne rouge "
               "bat ; puis il repart en arrière et rentre dans la tête de l'IA ; rien ne se brise")
    tip = toi.tip(f)
    S.key("impact3", "pos", f - 1, r2([tip[0] - 4, tip[1]]))
    kit.pop("impact3", f, d=2)
    kit.shake("brouillon", f + 1, amp=10, axis="x")
    kit.pulse("brouillon_L5", f, times=2, peak=1.12, step=2)
    vanish(kit, "impact3", f + 8, d=5)
    back = f + 9
    head2 = S.to_world("ia", c.brain_front, back)
    S.key("brouillon", "pos", back, r2(head2), 12, "inOut")
    S.key("brouillon", "scale", back, 0, 12, "in")
    S.key("brouillon", "opacity", back + 12, 0)
    S.key("faisceau_passe", "from", back, 1, 10, "in")       # le faisceau rentre avec lui
    S.key("faisceau_passe", "draw", back + 10, 0)
    S.key("faisceau_passe", "from", back + 10, 0)

    f = kit.at("S17", "client.", "une coche cyan se trace sur le coin de la fiche relue, posée sur la table")
    S.key("coche_table", "pos", f - 1, r2([corner_t[0] + 18, corner_t[1] - 14]))
    kit.draw("coche_table", f, POP)
    toi.rest(f, 8)

    # =================== S18 « Avant, tu arrives en ayant cherché. » ===================
    f = kit.at("S18", "Avant,", "chemin, horloge, fiche, coches et l'IA se réduisent, le conseiller sort ; les fauteuils "
               "glissent au centre et grandissent, le client assis à droite ; l'étiquette « Avant » surgit")
    morph_out(kit, ["chemin", "horloge", "fiche", "coche_relue", "coche_table", "ia"], f)
    toi.exit(f)
    S.keys("fauteuils", f, MOVE, "inOut", pos=list(CHAIRS_S18), scale=1)
    S.keys("client", f, MOVE, "inOut", pos=r2(chairs_pt(CHAIRS_S18, 1, CLIENT_SEAT)), scale=1)
    S.key("avant", "pos", f - 1, list(AVANT_AT))
    kit.pop("avant", f)

    f = kit.at("S18", "arrives", "le conseiller entre par la gauche, déjà dans l'image, les bras chargés d'une pile de "
               "travers (4 documents, 2 cartes « Client · 14 h »), la pastille « Client · 9 h » dessus, à gauche de sa "
               "tête")
    toi.set_z(f - 1, 10.9)                                   # la pile devant son buste, le bras devant la pile
    toi.enter(f, at=list(TOI18), frm=30, d=MOVE)
    toi.stow(f - 1, d=1)
    kit.ensure("pastille", "z", 13.5)
    S.key("pastille_fiche", "opacity", f - 1, 0)             # le relais repassera par la pastille du monde (S19)
    S.keys("pastille", f - 1, scale=1, opacity=1, text=PILL_TEXT, w=PILL_W)
    for cid, (_, _, rot, z) in PILE_REL.items():
        if cid.startswith("doc"):
            S.keys(cid, f - 1, compact=0, tag=0, txt=1, read=0, sh=6, opacity=1, z=z)
        S.keys(cid, f - 1, scale=CARD_SCALE, rot=rot)
    for n in range(f - 1, f + MOVE):
        tp = S.val("toi", "pos", n)
        for cid, (dx, dy, _, _) in PILE_REL.items():
            S.key(cid, "pos", n, r2([tp[0] + dx, tp[1] + dy]), 1, "linear")
        S.key("pastille", "pos", n, r2([tp[0] + PILL_REL[0], tp[1] + PILL_REL[1]]), 1, "linear")

    f = kit.at("S18", "cherché.", "un document glisse de la pile et tombe au sol en tournant")
    S.key("doc1", "pos", f, list(FLOOR_DOC), DROP, "in")
    S.key("doc1", "rot", f, 96, DROP, "in")

    # =================== S19 « Après, tu arrives en ayant compris. » ===================
    f = kit.at("S19", "Après,", "l'étiquette se remplit de cyan et devient « Après » ; les cartes grises se réduisent ; "
               "les 4 documents volent devant la table et fusionnent en la fiche tamponnée (x 0,6) ; le conseiller va "
               "s'asseoir dans le fauteuil gauche, face au client ; la pastille reprend sa place sur l'en-tête")
    S.key("avant", "text", f, "Après")
    S.key("avant", "fill", f, CYAN, POP, "out")
    vanish(kit, "carte_grise1", f)
    vanish(kit, "carte_grise2", f)
    merge = list(FICHE19)
    for i in range(4):
        d_id = f"doc{i + 1}"
        S.fly(d_id, f + i, MORPH - 2, "in", to=r2(merge), scale=0.2)
        S.key(d_id, "opacity", f + i + MORPH - 2, 0)
    S.key("fiche", "pos", f - 1, r2(merge))
    kit.pop("fiche", f + 6, scale=FICHE19_SCALE, d=MORPH)
    seat = chairs_pt(CHAIRS_S18, 1, ADV_SEAT)
    toi.set_z(f, 15)
    toi.walk(f, r2(seat), d=MOVE)
    arr = f + 6 + MORPH
    head = S.to_world("pastille_fiche", [0, 0], arr)
    S.fly("pastille", f, MOVE, "inOut", to=r2(head), scale=FICHE19_SCALE, arc=60)
    S.key("pastille", "opacity", f + MOVE, 0)
    S.key("pastille_fiche", "opacity", f + MOVE, 1)

    f = kit.at("S19", "arrives", "l'autocollant « ? » quitte la fiche et devient une bulle entre les deux figurines, "
               "queue sur la tête du conseiller : c'est lui qui pose la question")
    st = S.to_world("autocollant", [0, 0], f - 1)
    adv_head = [seat[0] + 4, seat[1] + toi.size * (-96 - 6)]
    tail = S.ents["bulle"]["p"]["tail"]
    b_at = [adv_head[0] - tail[0], adv_head[1] - tail[1]]   # la pointe de la queue sur sa tête (bulle à x 1)
    S.keys("bulle", f - 1, pos=r2(st), scale=round(S.world_scale("autocollant", f - 1), 4), s=1, q=1, glyph=0,
           opacity=1, rot=0)
    S.key("autocollant", "opacity", f, 0)
    S.fly("bulle", f, 12, "inOut", to=r2(b_at), scale=1, arc=60)
    S.key("bulle", "s", f + 4, 0, 8, "inOut")               # l'autocollant redevient sa bulle

    f = kit.at("S19", "compris.", "le client répond par sa propre bulle, où la pastille cyan à silhouette tombe dans "
               "la puce vide de la ligne 5 et bat ; « à poser au RDV » devient la source « RDV 9 h » ; les deux "
               "figurines se penchent l'une vers l'autre")
    vanish(kit, "bulle", f, d=6)
    kit.pop("bulle_client", f, d=6)
    bc = S.val("bulle_client", "pos", f)
    S.key("reponse", "pos", f - 1, r2(bc))
    kit.pop("reponse", f, scale=ANSWER_SCALE, d=5)
    bullet = S.to_world("fiche", [X["bullet"], rows[4] + ty], f + 5)
    S.fly("reponse", f + 5, 8, "inOut", to=r2(bullet), scale=ANSWER_SCALE, arc=40)
    land = f + 13
    kit.pulse("reponse", land, peak=ANSWER_SCALE * 1.3, step=3)
    vanish(kit, "bulle_client", f + 8, d=6)
    vanish(kit, "source5", land, d=4)                       # la question a sa réponse : elle devient sa source
    kit.pop("source5b", land + 1, d=6)
    S.key("source5b", "flash", land + 7, 1, 2, "out")
    S.key("source5b", "flash", land + 9, 0, 3, "inOut")
    toi.lean_to(f, 5, d=POP)
    S.key("client", "lean", f, -5, POP, "out")

    # =================== S20 « Abonne-toi pour comprendre ton argent. » ===================
    out = kit.outro("S20", outs=["fauteuils", "fiche", "reponse", "avant"], press="argent.", h=CARD_H,
                    pos=CARD_POS)
    S.ents["fin"]["p"].update(titleSize=56, labelSize=36, titleY=-60)   # titre au centre de la carte
    card = g0 = out["card"]                                  # image du temps fort calé (1659), pas scene_f0
    hp = S.to_world("pastille_fiche", [0, 0], g0 - 1)
    S.keys("pastille", g0, pos=r2(hp), scale=round(S.world_scale("pastille_fiche", g0 - 1), 4), opacity=1, z=40.5,
           text="S’abonner")
    S.key("pastille_fiche", "opacity", g0, 0)
    for o in ("fauteuils", "fiche", "reponse", "avant"):
        S.key(o, "opacity", card + MORPH - 3, 0, 3, "linear")
    toi.exit(card)
    client.exit(card)
    S.keys("pastille", card, MOVE, "inOut", pos=list(BTN), scale=2, w=190)
    land = card + MOVE
    S.key("fin", "title", card + 4, 0)                      # titre et ligne en fondu à l'arrivée de la pastille
    S.key("fin", "title", land - 2, 1, FADE, "out")
    S.key("fin", "btn", card + 6, 0)                        # le bouton naît du relais, en fondu enchaîné
    S.key("fin", "btn", land - 2, 1, 3, "out")
    S.key("pastille", "opacity", land - 2, 0, 3, "linear")
    S.key("pastille", "scale", land + 1, 0)

    f = kit.at("S20", "comprendre", "le pointeur surgit en bas à droite et glisse jusqu'au bas du bouton S’abonner")
    cur = out["cursor"]
    aim = S.val(cur, "pos", out["press"])
    kit.pop(cur, f, d=6)
    S.key(cur, "pos", f + 2, r2(aim), 7, "inOut")
