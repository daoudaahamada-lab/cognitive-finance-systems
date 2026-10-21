"""V01, partie 3 : S15-S20, images 1239-1746 (24 temps forts, 16,9 s dont la tenue finale). L'IA passe le brief relu ;
le poids du conseil, de l'adéquation et de la responsabilité penche du côté du conseiller, l'IA reste en retrait à côté
de la balance ; dix minutes de relecture laissent passer la fiche et arrêtent le brouillon ; Avant / Après ; la
pastille devient le bouton.

État d'entrée, épinglé à l'image 1238 : kit.pin(1238, ENTRY_P3) (etat_initial de S15), plus `horloge` (échelle 0) et
`pastille` (opacité 0). Figurines (jamais épinglées) : `toi` entre la fiche et le client (ADV_END, x 1, fin de p2),
`client` debout en CLIENT_S13. Partie construite seule (WTH_PARTS=p3) : gardes d'entrée, sans effet dans le film.

Temps forts (image du film, calés par kit.at ; « mot n » = début du mot quand l'attaque audible le devance) :
S15  L’IA=1239  prépare.=1259
S16  Toi,=1287 (mot 1286)  tu=1300  gardes=1306  conseil,=1317  l’adéquation=1337  responsabilité.=1373
S17  Dix=1422  minutes=1429  relecture=1442  valent=1461  erreur=1481  devant=1491  client.=1502
S18  Avant,=1532 (mot 1531)  arrives=1552  cherché.=1573
S19  Après,=1594  arrives=1612  compris.=1633
S20  Abonne-toi=1659 (mot 1658)  comprendre=1688  argent.=1711 ; dernière image du film : 1746 (1747 images)

Scène par scène (tour de revue 4) :
- S15 « L’IA » : l'IA d'abord : elle quitte son coin et regrandit sur le bout gauche de la future planche ; le fil du
  « ? » rentre ; le client revole dans le pictogramme de la pastille de l'en-tête. +3 : le trait du repère tombe en
  planche (pivot compris) et ses 3 disques descendent avec elle, à droite du pivot ; la fiche se réduit (allégée)
  devant l'IA. +6 : le conseiller monte sur le bout droit. Tout est posé à 1254. « prépare. » : passation isolée : la
  fiche monte au bout du faisceau de l'IA, y tient 6 images, puis glisse 550 ms vers le conseiller, qui se penche vers
  elle et la ramène contre lui ; rien d'autre ne bouge.
- S16 « Toi, » : pilule « Toi ». « tu » : l'IA descend au sol, À CÔTÉ de la balance (x 15-155, hors de la planche),
  x 0,7 ; son faisceau reste sur la fiche. « gardes » : il serre la fiche ; la planche penche à 5°. « conseil, »,
  « l’adéquation », « responsabilité. » : le cercle prend son pictogramme (56 px), roule dans la pile devant lui et y
  reste comme pictogramme de son jeton, dont le libellé (30 px) s'étire à droite ; jetons pile l'un sur l'autre ; à
  chaque jeton, la planche plonge de +2° puis se pose (10°, 15°, 20°) et le conseiller fléchit (x 0,97) : il porte le
  poids. Sur « responsabilité. », le faisceau de l'IA s'éteint.
- S17 « Dix » : la planche devient le chemin ; jetons, cercles et « Toi » s'effacent ; l'IA, petite, au départ du
  chemin ; le conseiller (x 1) descend sur le chemin et pose la fiche (allégée) devant lui. Rien d'autre : ni
  fauteuils ni client. « minutes » : l'horloge au-dessus de lui (aiguille sur :50) ; la fiche vient à lui.
  « relecture » : le stylo descend la colonne des coches pendant que le secteur se remplit de :50 à :00 au même pas ;
  coche sur le coin de la fiche, le secteur et la coche battent ensemble. « valent » : les fauteuils et le client
  surgissent (200 ms) au bout du chemin ; la fiche relue y vole. « erreur » : il tend son stylo en travers du chemin ;
  le brouillon de l'IA (x 0,4) naît devant sa tête et fonce à vitesse constante. « devant » : il bute, reste collé 4
  images contre le stylo, puis se brise : 6 éclats dérivent 0,6 s et s'effacent, sa bande rouge tombe sous le chemin
  et y reste jusqu'à « client. ».
- S18 « Avant, » : composition du rendez-vous ; « Avant » en haut. « arrives » : il entre avec une grosse pile en
  éventail (6 cartes x 0,8, ±12°, « Mail client » dessus), la pastille x 1,3 dessus, penché en arrière sous la
  charge. « cherché. » : le « Mail client » glisse du haut et tombe en arc au sol devant la table ; la pile vacille.
- S19 « Après, » : « Après » cyan, juste au-dessus de la fiche ; les documents (celui tombé compris) fusionnent en la
  fiche (x 0,8), debout sur la table ; il se tient devant la table, à 30 px du client. « arrives » : l'autocollant
  « ? » quitte la ligne 5 et s'arrête devant la tête du client. « compris. » : la bulle du client s'ouvre sur sa
  réponse (pastille à silhouette), qui descend dans la puce vide de L5 ; le stylo trace la 5e coche dans le carré
  tireté resté vide ; « 9 h » devient « Client · 9 h » ; ils s'inclinent l'un vers l'autre ; tout est immobile de 1652
  à 1658 (fiche complète tenue).
- S20 : fin standard ; la pastille devient le bouton « S’abonner ».
"""
import math

from pipeline.story import DROP, FADE, MORPH, MOVE, POP, TILT, _ease, text_width
from pipeline.story_kit import frames, lerp

from . import (ADV_PLANK_SCALE, ADV_PLANK_X, ADV_S17, ADV_S17_SCALE, ADV_S19, APRES_AT, AVANT_AT, BROUILLON_SCALE, BUBBLE19,
               CHAIRS_S17, CHAIRS_S17_SCALE, CHAIRS_S18, CIRCLE_D, CIRCLE_X, CLIENT_S13, CLOCK_S17, CLOCK_S17_SCALE,
               CX, CYAN, ENTRY_P3, FICHE19, FICHE19_SCALE, FIG_BASE, GROUND, IA_CORNER_SCALE, IA_FLOOR, IA_FLOOR_SCALE,
               IA_PILL_CORNER, IA_PLANK_SCALE, IA_PLANK_X, IA_S17, IA_S17_SCALE, LIGHT, MARKER_GAP, MARKER_Y,
               MINI_PILL, PAGE_PLANK_SCALE, PAGE_PLANK_X, PAGE_S14_SCALE, PAGE_S17, PAGE_S17_SCALE, PAPER, PATH_C, PIVOT_H,
               PATH_TOP, PATH_W, PILL_ICON, PILL_SIZE, PILL_TEXT, PILL_W, PLANK_AT, PLANK_H, PLANK_W, Q19, TOKEN_H,
               TOKEN_WS, TOKEN_X0, TOKENS, fig_pos, morph_out, scene_f0, vanish)

# ---------- places propres à p3 ----------
PAGE_W, PAGE_H = 500, 720                       # fiche de V01
PLANK_TOP = PLANK_AT[1] - PLANK_H               # 918 : dessus de la planche à plat
ARMS_SCALE = 0.2                                # la fiche dans ses bras : 100 x 144, à son côté, au-dessus des jetons
ARMS_OFF = (-22, -12)                            # centre de la fiche / centre de la figurine (x échelle)
ARMS_FROM = (-32, -24)                          # « prépare. » : elle arrive 40 px plus loin ; « gardes » la ramène
TOI_PILL_Y, TOI_PILL_SCALE = FIG_BASE + 52, 0.8   # « Toi » sous la planche (repère de la figurine)
LV = [-PLANK_H - TOKEN_H / 2 - (TOKEN_H + 4) * k for k in range(3)]   # niveaux de la pile (repère de la planche)
CIRCLE_Y = -PLANK_H - CIRCLE_D / 2              # cercles posés sur la planche
TILT_K = [5, 10, 15, 20]                         # « gardes », puis chaque jeton (tour 4 : bascule nette)
TABLE = (-5, 8)                                 # dessus de la table de verre (repère des fauteuils à x 1)
CLIENT_SEAT = (200, -62)                        # assis dans le fauteuil droit (repère des fauteuils à x 1)
PAGE_DIX = (PAGE_S17[0] - 28, PAGE_S17[1])      # S17 « Dix » : la fiche posée, 28 px avant sa place de relecture
FICHE_TABLE_SCALE = 0.2                         # S17 : la fiche relue posée sur la petite table
BARRIER = (-60, 46)                             # S17 « erreur » : pointe du stylo / épaule, en travers du chemin
BAND_FLOOR_Y = 1250                             # S17 « devant » : la bande rouge tombée sous le chemin
TOI18 = fig_pos(390, GROUND)                    # S18 : il arrive au fauteuil gauche, la pile dans les bras
CARD_SCALE = 0.8                                # tour 4 : cartes de la pile (184 x 200), pile en éventail ≈ 310 x 340
PILE_C = (-150, -30)                            # centre de la pile / centre de la figurine : à sa gauche (côté du bras),
#                                                 à hauteur de poitrine, sa tête reste visible
# (dx, dy, rot, z) : éventail de ±12°, pas de 22 px ; le « Mail client » (doc3) dessus, d'où il glissera (S18)
PILE_REL = {"carte_grise2": (-80, 16, -12, 11.0), "doc4": (-58, 10, -7, 11.1), "carte_grise1": (-36, 4, -2, 11.2),
            "doc2": (-14, -2, 3, 11.3), "doc1": (8, -8, 8, 11.4), "doc3": (30, -14, 12, 11.5)}
PILL_REL, PILL18_SCALE = (-150, -160), 1.3      # pastille sur la pile, x 1,3
LEAN_LOAD = 8                                   # S18 : penché en arrière sous la charge
FLOOR_CARD = (575, 1140)                        # « cherché. » : le « Mail client » au sol devant la table (bas ≈ 1250)
ANSWER_PX = 96                                  # S19 : la réponse du client, 96 px (puce de 44 px x 2,18)
CARD_POS, CARD_H = (540, 860), 560              # carte de fin, x 230-850, y 580-1140
BTN = (CARD_POS[0], CARD_POS[1] + CARD_H / 2 - 56 - 56)   # centre du bouton de la carte
BTN_SCALE = 1.6
BTN_W = round(text_width("S’abonner", PILL_SIZE, 700) + 92)
# contrôle sans son (S16) : l'IA descend au sol JUSTE À CÔTÉ du pivot, sous le bras gauche de la planche (x 273-417,
# tête à y 947 sous la planche à plat à 930), au même sol que la balance (base du pivot, y 1130)
PIVOT_BASE_Y = PLANK_AT[1] + PIVOT_H
IA_STANDBY, IA_STANDBY_SCALE = (345, PIVOT_BASE_Y), 0.72


def r2(pt):
    return [round(pt[0], 2), round(pt[1], 2)]


def part(S, kit, c):
    toi, client, sheet = c.toi, c.client, c.sheet
    rows, X, ty, ly = sheet.rows, sheet.x, sheet.ty, sheet.ly
    ai_h = c.ai_h
    f0 = scene_f0(S, "S15")                                   # 1239

    kit.pin(f0 - 1, {**ENTRY_P3, "horloge": {"scale": 0}, "pastille": {"opacity": 0}})   # etat_initial de S15
    if S.val("toi", "scale", f0 - 1) == 0:                   # partie construite seule : figurines absentes
        toi.size = 1.0
        toi.enter(f0 - 10, at=[716, 1075])
    if S.val("client", "scale", f0 - 1) == 0:
        client.size = 1.0
        client.enter(f0 - 10, at=list(CLIENT_S13))
    if S.val("L1", "chars", f0 - 1) == 0:                    # partie seule : ce que p2 a écrit et posé sur la fiche
        kit.pin(f0 - 1, {**{lid: {"chars": len(p["key"]) + len(p["value"])} for lid, p in sheet.lines},
                         "L5": {"slotFill": 0}, "autocollant": {"pos": [X["value"] - 46, rows[4] + ty - 10],
                                                                "scale": round(96 / 72 / PAGE_S14_SCALE, 4)},
                         "tampon": {"pos": [0, 300], "rot": -4}, "carre5": {"opacity": 1},
                         "pastille_mini": {"pos": [-189.0, rows[4] + ly + 6]},
                         "ia_pill": {"pos": list(IA_PILL_CORNER), "scale": round(1 / IA_CORNER_SCALE, 4)}})

    # ---------- utilitaires ----------
    def plank_feet(n):
        """Pieds du conseiller sur la planche (point monde du dessus, x local ADV_PLANK_X, 3 px d'ivoire entre ses
        pieds et la planche) à l'image n."""
        return S.to_world("planche", [ADV_PLANK_X, -PLANK_H - 3], n)

    def body_at(feet, s):
        return r2([feet[0], feet[1] - FIG_BASE * s])

    def arms_at(n, off):
        """Centre de la fiche tenue à son côté (off : décalage dans le repère de la figurine) à l'image n."""
        p, s = S.val("toi", "pos", n), S.val("toi", "scale", n)
        return r2([p[0] + off[0] * s, p[1] + off[1] * s])

    def chairs_pt(pos, s, local):
        return r2([pos[0] + local[0] * s, pos[1] + local[1] * s])

    def beam_on_fiche(fa, fb):
        """Le faisceau de l'IA suit le bord gauche de la fiche, image par image, sur [fa, fb)."""
        for n in range(fa, fb):
            S.key("faisceau_passe", "pb", n, r2(S.to_world("fiche", [-PAGE_W / 2, 0], n)), 1, "linear")

    # =================== S15 « L’IA prépare. » ===================
    f = kit.at("S15", "L’IA", "l'IA d'abord : elle quitte son coin et regrandit sur le bout gauche de la future "
               "planche ; le fil du « ? » rentre ; le client revole dans le pictogramme de la pastille. +3 : le trait "
               "du repère tombe en planche, ses 3 disques descendent avec elle à droite du pivot ; la fiche se réduit "
               "devant l'IA. +6 : le conseiller monte sur le bout droit ; tout est posé à +15")
    S.key("fil_q", "from", f, 1, 4, "in")
    S.key("fil_q", "draw", f + 4, 0)
    # C : l'IA (le sujet du mot) bouge la première
    ia_on = [PLANK_AT[0] + IA_PLANK_X, PLANK_TOP - IA_PLANK_SCALE * ai_h / 2]
    pill_low = [0, round((PLANK_AT[1] + 12 + 25 - ia_on[1]) / IA_PLANK_SCALE, 1)]
    S.key("ia", "z", f, 8.6)                                 # devant la fiche encore grande : on la voit monter
    S.key("ia_pill", "z", f, 8.7)
    S.keys("ia", f, 9, "inOut", pos=r2(ia_on), scale=IA_PLANK_SCALE)
    S.keys("ia_pill", f, 9, "inOut", pos=pill_low, scale=1)
    # la fiche se réduit (allégée) à sa place devant l'IA, sur la future planche
    page_on = [PLANK_AT[0] + PAGE_PLANK_X, PLANK_TOP - 2 - PAGE_PLANK_SCALE * PAGE_H / 2]
    S.keys("fiche", f + 3, MORPH, "inOut", pos=r2(page_on), scale=PAGE_PLANK_SCALE)
    lite_ids = ["fiche", "tampon", "source5"] + [lid for lid, _ in sheet.lines] + [f"source{i + 1}" for i in range(4)]
    for id in lite_ids:
        S.key(id, "lite", f + 5, 1, 6, "inOut")
    # A : le client revole jusqu'au pictogramme de la pastille de l'en-tête et y rentre (taille 1 jusqu'au bout)
    dc = 9
    c0 = S.val("client", "pos", f - 1)
    tgt = S.to_world("pastille_fiche", PILL_ICON, f + dc - 1)
    mid = [(c0[0] + tgt[0]) / 2 + 40, min(c0[1], tgt[1]) - 200]
    arc = [r2([(1 - q) ** 2 * c0[0] + 2 * (1 - q) * q * mid[0] + q * q * tgt[0],
               (1 - q) ** 2 * c0[1] + 2 * (1 - q) * q * mid[1] + q * q * tgt[1]]) for q in [k / 9 for k in range(10)]]
    client.run(f, arc, dc)
    client.scale_to(f + dc - 3, 0.05, d=3, e="in")
    client.exit(f + dc, d=1)
    kit.pulse("pastille_fiche", f + dc, peak=1.12, step=3)
    # B (+3) : le trait du repère (360 px) devient la planche (même échelle partout : ses enfants ne se déforment pas),
    # qui tombe en grandissant ; ses 3 disques deviennent les 3 cercles, qui descendent avec elle à droite du pivot
    fb = f + 3
    kit.fade("marqueur", fb, to=0, d=4)
    S.key("marqueur", "scale", fb + 4, 0)
    s0 = round(2 * MARKER_GAP / PLANK_W, 4)
    S.key("planche", "pos", fb - 1, [CX, MARKER_Y + 2])
    S.key("planche", "scale", fb, s0)
    S.key("planche", "scale", fb + 1, 1, DROP - 1, "out")
    for n, p in frames(fb, DROP, "in"):
        S.key("planche", "pos", n, r2([lerp(CX, PLANK_AT[0], p), lerp(MARKER_Y + 2, PLANK_AT[1], p)]), 1, "linear")
    xs = S.ents["marqueur"]["p"]["xs"]
    for k in range(3):
        cid = f"cercle{k + 1}"
        S.keys(cid, fb - 1, pos=[round(xs[k] / s0, 1), CIRCLE_Y], text=str(k + 1), fill=PAPER)
        S.key(cid, "scale", fb, 1)
        S.key(cid, "pos", fb, [CIRCLE_X[k], CIRCLE_Y], DROP, "out")
    landed = fb + DROP
    # C' (+6) : le conseiller monte sur le bout droit (x 1,1)
    fc = f + 6
    adv_on = body_at(S.to_world("planche", [ADV_PLANK_X, -PLANK_H - 3], landed), ADV_PLANK_SCALE)
    toi.scale_to(fc, ADV_PLANK_SCALE, d=9)
    toi.walk(fc, adv_on, d=9)

    f = kit.at("S15", "prépare.", "passation, seule : le faisceau pointillé de l'IA part de sa tête, la fiche monte à son "
               "bout et y tient 6 images, puis glisse 550 ms en arc vers le conseiller, qui se penche vers elle et la "
               "ramène contre lui ; rien d'autre ne bouge ; la planche reste à plat")
    toi.stow(f - 2)
    toi.set_z(f, 7.9, tool_z=7.95)
    lift = [page_on[0], page_on[1] - 60]
    S.key("fiche", "pos", f, r2(lift), 5, "out")              # elle monte au bout du faisceau
    held = f + 11                                             # tenue de 6 images (f + 5 .. f + 10)
    arrive = [adv_on[0] + (ARMS_OFF[0] + ARMS_FROM[0]) * ADV_PLANK_SCALE,
              adv_on[1] + (ARMS_OFF[1] + ARMS_FROM[1]) * ADV_PLANK_SCALE]
    S.fly("fiche", held, MOVE, "inOut", to=r2(arrive), scale=ARMS_SCALE, arc=120)
    land = held + MOVE
    toi.lean_to(held + 6, -7, d=6)                           # il se penche vers elle
    toi.lean_to(land - 4, 0, d=6, e="inOut")                 # et la ramène contre lui
    beam_on_fiche(f - 1, land)
    kit.draw("faisceau_passe", f, 3)

    # =================== S16 « Toi, tu gardes le conseil, l’adéquation et la responsabilité. » ===================
    f = kit.at("S16", "Toi,", "la pilule « Toi » surgit sous le conseiller")
    beam_on_fiche(land, f)
    S.key("toi_pill", "pos", f - 1, [0, TOI_PILL_Y])
    kit.pop("toi_pill", f, scale=TOI_PILL_SCALE)

    f_tu = kit.at("S16", "tu", "l'IA, son travail passé, descend d'elle-même de la planche par un petit saut et se pose "
                  "au sol JUSTE À CÔTÉ du pivot, sous le bras gauche (x 0,72, tournée vers lui, au même sol que la "
                  "balance) ; elle rentre son faisceau : elle reste là, près de lui, en retrait")
    beam_on_fiche(f, f_tu)
    # contrôle sans son (« l'IA semble éjectée ») : plus de glissade rapetissante vers le coin de l'écran. Elle descend
    # en douceur (16 images, petit saut) et se tient debout sur le sol du pivot, à 70 px de lui, à hauteur lisible ;
    # le bras gauche de la planche remonte au-dessus d'elle quand le poids passe du côté du conseiller
    d_ia = 16
    stand = [IA_STANDBY[0], PIVOT_BASE_Y - IA_STANDBY_SCALE * ai_h / 2]
    S.keys("ia", f_tu, d_ia, "inOut", arc=50, pos=r2(stand), scale=IA_STANDBY_SCALE)
    S.keys("ia_pill", f_tu, d_ia, "inOut", pos=[0, round(ai_h / 2 + 30, 1)], scale=round(1 / IA_STANDBY_SCALE, 4))
    S.key("faisceau_passe", "from", f_tu + 2, 1, 8, "in")   # elle rentre son faisceau (la passation est faite)
    S.key("faisceau_passe", "draw", f_tu + 10, 0)
    S.key("faisceau_passe", "from", f_tu + 10, 0)

    fg = kit.at("S16", "gardes", "il serre la fiche contre lui ; la planche penche à 5° de son côté")
    S.key("planche", "rot", fg, TILT_K[0], TILT, "out")

    def to_token(k, fk):
        """Sur son mot, le cercle k prend son pictogramme, roule dans la pile devant lui (colonne TOKEN_X0, niveau k) et
        y reste comme pictogramme de son jeton, dont la capsule et le libellé s'étirent à droite ; posé, la planche
        plonge de +2° puis se pose à 5 x (k + 2)° et le conseiller fléchit (x 0,97). Renvoie l'image d'arrivée."""
        cid, jid = f"cercle{k + 1}", f"jeton{k + 1}"
        kit.fade(f"{cid}_ico", fk, 1, d=3)                   # le chiffre s'efface sous le pictogramme du geste
        roll = 7
        S.key(cid, "pos", fk, [TOKEN_X0, LV[k]], roll, "out", arc=(LV[0] - LV[k]) + 24)
        S.key(cid, "rot", fk, -360, roll, "out")              # il roule vers la gauche, dans la pile
        S.key(cid, "fill", fk, LIGHT, roll, "out")
        r = fk + roll
        S.key(jid, "scale", r - 1, 1)
        S.keys(jid, r, 5, "out", w=TOKEN_WS[k], pos=[round(TOKEN_X0 - 36 + TOKEN_WS[k] / 2, 1), LV[k]])
        kit.fade(f"{jid}_txt", r + 3, 1, d=4)
        tgt = TILT_K[k + 1]
        S.key("planche", "rot", r, tgt + 2, 6, "out")         # le poids : la planche plonge…
        S.key("planche", "rot", r + 6, tgt, 8, "inOut")       # … puis se pose
        toi.scale_to(r, round(ADV_PLANK_SCALE * 0.97, 4), d=3, e="out")   # il fléchit : il porte le poids
        toi.scale_to(r + 3, ADV_PLANK_SCALE, d=4, e="inOut")
        return r

    f = kit.at("S16", "conseil,", "le cercle 1 prend la bulle de dialogue, roule dans la pile devant lui et devient le "
               "jeton « Conseil » ; la planche plonge puis se pose à 10° ; il fléchit")
    to_token(0, f)
    f = kit.at("S16", "l’adéquation", "le cercle 2 prend la cible, roule sur le premier jeton (même colonne) et devient "
               "« Adéquation » ; 15°")
    to_token(1, f)
    f = kit.at("S16", "responsabilité.", "le cercle 3 prend la signature et devient « Responsabilité », en haut de la "
               "pile ; 20° ; au sol juste à côté du pivot, l'IA reste visible, immobile, en retrait")
    f_end = to_token(2, f) + 14

    # le conseiller suit le bout de la planche image par image (à son échelle de l'image : il fléchit) ; la fiche suit
    # son côté ; le faisceau suit la fiche
    for n in range(fg, f_end):
        toi.walk(n, body_at(plank_feet(n), S.val("toi", "scale", n)), d=1)
        toi.rest(n, 1)                                       # bras re-posé à chaque image (main au repos)
    for n in range(fg, f_end):
        p = _ease("out", min(1.0, (n - fg + 1) / POP))
        off = lerp([ARMS_OFF[0] + ARMS_FROM[0], ARMS_OFF[1] + ARMS_FROM[1]], list(ARMS_OFF), p)
        S.key("fiche", "pos", n, arms_at(n, off), 1, "linear")
    beam_on_fiche(f_tu, f_tu + 10)                            # le faisceau suit la fiche pendant qu'il rentre

    # =================== S17 « Dix minutes de relecture valent mieux qu’une erreur devant le client. » =============
    f = kit.at("S17", "Dix", "la planche se remet à plat et devient le chemin ; jetons, cercles et « Toi » s'effacent ; "
               "l'IA, petite, va au départ du chemin ; le conseiller (x 1) descend sur le chemin et pose la fiche "
               "(allégée) devant lui ; rien d'autre à l'écran")
    mid = S.to_world("planche", [0, -PLANK_H / 2], f - 1)
    S.set("chemin", w=PATH_W)
    S.keys("chemin", f - 1, pos=r2(mid), rot=S.val("planche", "rot", f - 1), w=PLANK_W)
    S.key("chemin", "scale", f, 1)
    S.keys("chemin", f, MORPH, "out", pos=list(PATH_C), rot=0, w=PATH_W)
    S.keys("planche", f, MORPH, "out", pos=[PATH_C[0], PATH_C[1] + PLANK_H / 2], rot=0)
    S.key("planche", "opacity", f, 0, 4, "linear")
    S.key("planche", "scale", f + MORPH, 0)
    morph_out(kit, ["jeton1", "jeton2", "jeton3", "cercle1", "cercle2", "cercle3", "toi_pill"], f)
    ia17 = [IA_S17, PATH_TOP - IA_S17_SCALE * ai_h / 2]
    S.key("ia", "z", f, 14.6)                               # le brouillon (S17) sortira devant sa tête
    S.key("ia_pill", "z", f, 14.7)
    S.keys("ia", f, MORPH, "inOut", pos=r2(ia17), scale=IA_S17_SCALE)
    S.keys("ia_pill", f, MORPH, "inOut", pos=[0, -round(ai_h / 2 + 52, 1)], scale=round(1 / IA_S17_SCALE, 4))
    # le conseiller descend sur le chemin (même assouplissement « out » que la planche)
    a = S.val("toi", "pos", f - 1)
    a_s = S.val("toi", "scale", f - 1)
    a_feet = [a[0], a[1] + FIG_BASE * a_s]
    b_feet = [ADV_S17[0], ADV_S17[1] + FIG_BASE * ADV_S17_SCALE]
    toi.scale_to(f, ADV_S17_SCALE, d=MORPH, e="out")
    for n in range(f, f + MORPH):
        p = _ease("out", (n - f + 1) / MORPH)
        toi.walk(n, body_at(lerp(a_feet, b_feet, p), S.val("toi", "scale", n)), d=1)
        toi.rest(n, 1)
    toi.set_z(f, 15, tool_z=15.5)
    S.fly("fiche", f, MORPH, "inOut", to=r2(PAGE_DIX), scale=PAGE_S17_SCALE)

    f = kit.at("S17", "minutes", "l'horloge de 9 h grandit au-dessus de lui, aiguille des minutes sur :50 ; la fiche, "
               "posée sur le chemin, vient jusqu'à lui ; il reprend son stylo")
    S.key("horloge", "pos", f - 1, list(CLOCK_S17))
    S.key("secteur", "value", f - 1, 0)
    S.key("aiguille", "rot", f - 1, -60)
    S.key("aiguille", "scale", f - 1, 1)
    kit.pop("horloge", f, scale=CLOCK_S17_SCALE, d=10)
    S.key("dix_min", "scale", f + 6, 1)                      # contrôle sans son : « 0 min » à droite du cadran
    kit.fade("dix_min", f + 6, 1, d=FADE, frm=0)
    S.key("fiche", "pos", f + 4, r2(PAGE_S17), POP, "out")
    toi.unstow(f + 2)

    f = kit.at("S17", "relecture", "le stylo descend la colonne des coches de la fiche pendant que le secteur se remplit "
               "sur le cadran de :50 à :00, au même pas ; une coche pleine sur son coin ; le secteur et la coche battent "
               "ensemble : ces dix minutes produisent la coche")
    pts = [S.to_world("fiche", sheet.pt(i, "tick"), f) for i in range(5)]
    hits = toi.trace(f - 4, pts, d=14, lead=4)
    t0, dur = hits[0] + 1, hits[-1] - hits[0]
    S.key("secteur", "value", t0, 10, dur, "linear")
    S.key("aiguille", "rot", t0, 0, dur, "linear")
    S.key("dix_min", "value", t0, 10, dur, "linear")          # 0 -> 10 min, au pas du stylo et du secteur
    corner_l = [PAGE_W / 2 - 10, -PAGE_H / 2 + 6]            # coin haut droit, hors du texte
    S.key("coche_relue", "pos", f - 1, r2(S.to_world("fiche", corner_l, f)))
    done = hits[-1] + 1
    kit.draw("coche_relue", done, 4)
    kit.pulse("secteur", done, peak=1.15, step=2)            # même image : le temps passé produit la coche
    kit.pulse("dix_min", done, peak=1.15, step=2)
    kit.pulse("coche_relue", done + 2, peak=round(S.val("coche_relue", "scale", done) * 1.25, 4), step=2)
    toi.rest(done, 8)

    f = kit.at("S17", "valent", "les fauteuils et le client surgissent au bout du chemin (200 ms) ; la fiche relue, avec "
               "sa coche, passe au-dessus de lui jusqu'à la table ; il garde son stylo levé")
    S.key("fauteuils", "pos", f - 1, list(CHAIRS_S17))
    kit.pop("fauteuils", f, scale=CHAIRS_S17_SCALE, d=6)
    client.size = CHAIRS_S17_SCALE
    client.enter(f, at=chairs_pt(CHAIRS_S17, CHAIRS_S17_SCALE, CLIENT_SEAT), d=6)
    tbl = chairs_pt(CHAIRS_S17, CHAIRS_S17_SCALE, TABLE)
    on_table = [tbl[0], tbl[1] - 2 - FICHE_TABLE_SCALE * PAGE_H / 2]
    S.key("fiche", "pos", f, r2(on_table), MOVE, "inOut", arc=220)
    S.key("fiche", "scale", f, FICHE_TABLE_SCALE, MOVE, "inOut")
    k0 = S.val("coche_relue", "scale", f - 1)
    for n in range(f, f + MOVE):
        S.key("coche_relue", "pos", n, r2(S.to_world("fiche", corner_l, n)), 1, "linear")
        S.key("coche_relue", "scale", n, round(k0 * max(0.6, S.val("fiche", "scale", n) / PAGE_S17_SCALE), 4), 1,
              "linear")

    f = kit.at("S17", "erreur", "il tend son stylo en travers du chemin ; le brouillon de l'IA (tirets cyan, coches "
               "pointillées, une bande rouge) naît devant sa tête et fonce à vitesse constante sur le chemin")
    f_dev = S.word_after("devant", f)                        # il heurte le stylo sur « devant »
    sh = toi._shoulder(f - 1)
    barrier = [sh[0] + BARRIER[0], sh[1] + BARRIER[1]]
    toi.reach(f, barrier, d=6, step=False)
    head = S.to_world("ia", c.brain_front, f - 1)
    b_h = BROUILLON_SCALE * PAGE_H
    b_w = BROUILLON_SCALE * PAGE_W
    born = [head[0] + 70, PATH_TOP - b_h / 2]                # devant son visage, pas dessus
    bump = [barrier[0] - b_w / 2 - 2, PATH_TOP - b_h / 2]
    S.keys("brouillon", f - 1, pos=r2(born), scale=0, opacity=1)
    S.key("brouillon", "scale", f, 0.1)
    S.key("brouillon", "scale", f + 1, BROUILLON_SCALE, 3, "out")
    S.key("brouillon", "pos", f, r2(bump), f_dev - f, "linear")   # vitesse constante, sans s'arrêter
    for n in range(f - 1, f + 4):
        S.key("faisceau_passe", "pb", n, r2(S.to_world("brouillon", [-PAGE_W / 2, 0], n)), 1, "linear")
    S.key("faisceau_passe", "opacity", f - 1, 1)
    kit.draw("faisceau_passe", f, 2)
    S.key("faisceau_passe", "from", f + 3, 1, 4, "in")      # le faisceau rentre : le brouillon file seul
    S.key("faisceau_passe", "draw", f + 7, 0)
    S.key("faisceau_passe", "from", f + 7, 0)

    f = kit.at("S17", "devant", "il bute sur le stylo levé : 3 traits d'impact, il s'écrase un peu contre la pointe et "
               "y reste collé 6 images ; puis il bascule en arrière et tombe du chemin, sa ligne rouge avec lui, et "
               "s'efface : arrêté avant le client ; rien ne repart vers l'IA")
    # contrôle sans son : plus d'éclats (ils se lisaient comme des confettis) ; le brouillon est ARRÊTÉ net par le
    # stylo, puis rejeté hors du chemin, du côté de l'IA, loin du client
    tip = toi.tip(f)
    S.key("impact3", "pos", f - 1, r2([tip[0] - 4, tip[1]]))
    kit.pop("impact3", f, d=2)
    vanish(kit, "impact3", f + 12, d=5)
    kit.ensure("brouillon", "sx", 1)
    S.key("brouillon", "sx", f, 0.86, 2, "out")              # il s'écrase contre la pointe…
    S.key("brouillon", "sx", f + 2, 1, 4, "inOut")
    brk = f + 6                                              # … collé contre le stylo de f à f + 5
    kit.drop("brouillon", brk, out=True, h=70, dx=-60, rot=-24)
    S.key("brouillon", "scale", brk + 12, 0)

    f = kit.at("S17", "client.", "la coche pleine de la fiche relue, posée sur la table, bat ; le client aussi")
    kit.pulse("coche_relue", f, peak=round(S.val("coche_relue", "scale", f - 1) * 1.15, 4), step=3)
    cs = S.val("client", "scale", f - 1)
    client.scale_to(f, round(cs * 1.12, 4), d=3, e="out")
    client.scale_to(f + 3, cs, d=4, e="inOut")
    toi.rest(f, 8)

    # =================== S18 « Avant, tu arrives en ayant cherché. » ===================
    f = kit.at("S18", "Avant,", "chemin, horloge, fiche, coche et IA se réduisent, le conseiller sort ; les fauteuils "
               "glissent au centre et grandissent, le client y reste assis ; l'étiquette « Avant » surgit")
    morph_out(kit, ["chemin", "horloge", "dix_min", "fiche", "coche_relue", "ia"], f)
    toi.exit(f)
    S.keys("fauteuils", f, MOVE, "inOut", pos=list(CHAIRS_S18), scale=1)
    client.hop(f, chairs_pt(CHAIRS_S18, 1, CLIENT_SEAT), MOVE, h=0, lean=0)
    client.scale_to(f, 1.0, d=MOVE, e="inOut")
    S.key("avant", "pos", f - 1, list(AVANT_AT))
    kit.pop("avant", f)

    f = kit.at("S18", "arrives", "le conseiller entre par la gauche jusqu'au fauteuil gauche, les bras chargés d'une "
               "grosse pile en éventail (6 cartes de travers : 4 documents, 2 papiers gris, le « Mail client » dessus), "
               "la pastille « Client · 9 h » x 1,3 dessus ; il se penche en arrière sous la charge")
    toi.set_z(f - 1, 10.9, tool_z=12.9)
    toi.stow(f - 2, d=1)
    toi.size = 1.0
    toi.enter(f, at=list(TOI18), frm=-60, d=MOVE)
    toi.lean_to(f + MOVE, LEAN_LOAD, d=6)                    # débordé : penché en arrière
    kit.ensure("pastille", "z", 13.5)
    S.key("pastille_fiche", "opacity", f - 1, 0)
    S.keys("pastille", f - 1, scale=PILL18_SCALE, opacity=1, text=PILL_TEXT, w=PILL_W, z=13.5)
    for cid, (_, _, rot, z) in PILE_REL.items():
        if cid.startswith("doc"):
            S.keys(cid, f - 1, compact=0, tag=0, txt=1, read=0, sh=6, opacity=1, lit=0)
        else:
            S.keys(cid, f - 1, opacity=1)
        S.keys(cid, f - 1, scale=CARD_SCALE, rot=rot, z=z)
        if cid.startswith("carte"):                          # leurs lignes grises suivent leur calque (z global)
            for j in range(3):
                S.key(f"{cid}_l{j + 1}", "z", f - 1, round(z + 0.005, 3))
    S.key("carte_grise1_pill", "opacity", f - 1, 0)
    S.key("carte_grise2_pill", "opacity", f - 1, 0)
    for n in range(f - 1, f + MOVE):
        tp = S.val("toi", "pos", n)
        for cid, (dx, dy, _, _) in PILE_REL.items():
            S.key(cid, "pos", n, r2([tp[0] + PILE_C[0] + dx, tp[1] + PILE_C[1] + dy]), 1, "linear")
        S.key("pastille", "pos", n, r2([tp[0] + PILL_REL[0], tp[1] + PILL_REL[1]]), 1, "linear")

    f = kit.at("S18", "cherché.", "le « Mail client » glisse du haut de la pile et tombe en arc au sol, devant la table, "
               "en tournant ; la pile vacille")
    S.fly("doc3", f, DROP, "in", to=list(FLOOR_CARD), arc=60)
    S.key("doc3", "rot", f, 110, DROP, "out")
    for cid, (_, _, rot, _) in PILE_REL.items():             # la pile vacille (±4°)
        if cid != "doc3":
            S.key(cid, "rot", f + 1, rot + 4, 3, "out")
            S.key(cid, "rot", f + 4, rot - 3, 3, "inOut")
            S.key(cid, "rot", f + 7, rot, 4, "inOut")

    # =================== S19 « Après, tu arrives en ayant compris. » ===================
    f = kit.at("S19", "Après,", "l'étiquette se remplit de cyan, devient « Après » et se pose juste au-dessus de la "
               "fiche ; les papiers gris se réduisent ; les 4 documents (celui tombé compris) convergent et fusionnent "
               "en la fiche relue, debout sur la table ; la pastille vole à son en-tête ; le conseiller se redresse et se "
               "tient devant la table, à 30 px du client")
    S.key("avant", "text", f, "Après")
    S.key("avant", "fill", f, CYAN, POP, "out")
    S.key("avant", "pos", f, list(APRES_AT), MOVE, "inOut")
    vanish(kit, "carte_grise1", f)
    vanish(kit, "carte_grise2", f)
    for i in range(4):
        d_id = f"doc{i + 1}"
        S.fly(d_id, f + i, MORPH - 2, "in", to=r2(FICHE19), scale=0.3)
        S.key(d_id, "opacity", f + i + MORPH - 2, 0)
    S.keys("fiche", f + 5, pos=r2(FICHE19), rot=0, opacity=1)
    for id in lite_ids:                                      # en grand : la fiche complète, textes lisibles
        S.key(id, "lite", f + 5, 0)
    kit.pop("fiche", f + 6, scale=FICHE19_SCALE, d=MORPH)
    arr = f + 6 + MORPH
    toi.set_z(f, 15, tool_z=15.5)
    toi.lean_to(f, 0, d=6)
    toi.walk(f, list(ADV_S19), d=MOVE)
    header = S.to_world("pastille_fiche", [0, 0], arr)
    S.fly("pastille", f, arr - f, "inOut", to=r2(header), scale=FICHE19_SCALE, arc=80)
    S.key("pastille", "opacity", arr, 0)
    S.key("pastille_fiche", "opacity", arr, 1)

    f = kit.at("S19", "arrives", "l'autocollant « ? » (96 px) quitte la ligne 5 de la fiche et monte en arc jusque "
               "devant la tête du client, où il s'arrête")
    st = S.to_world("autocollant", [0, 0], f - 1)
    S.keys("bulle", f - 1, pos=r2(st), scale=round(S.world_scale("autocollant", f - 1), 4), s=1, q=1, glyph=0,
           opacity=1, rot=0)
    S.key("autocollant", "opacity", f, 0)
    fly = 10
    S.fly("bulle", f, fly, "inOut", to=list(Q19), scale=1.3, arc=90)
    toi.unstow(f + 4)

    f = kit.at("S19", "compris.", "la bulle du client s'ouvre au-dessus de lui sur sa réponse, une pastille cyan à "
               "silhouette ; le « ? » rentre dans sa tête ; la réponse descend dans la puce vide de la ligne 5 ; au "
               "même instant le stylo du conseiller trace la 5e coche pleine dans le carré tireté resté vide ; la "
               "réplique « 9 h » devient « Client · 9 h », la source de la ligne ; ils s'inclinent l'un vers l'autre ; "
               "puis tout tient")
    k_ans = ANSWER_PX / 44
    kit.pop("bulle_client", f, d=4)
    vanish(kit, "bulle", f, into="client", d=4)
    S.key("reponse", "pos", f - 1, list(BUBBLE19))
    kit.pop("reponse", f, scale=round(k_ans * 1.5, 3), d=3)
    bullet = S.to_world("fiche", [X["bullet"], rows[4] + ty], f + 3)
    S.fly("reponse", f + 3, 6, "inOut", to=r2(bullet), scale=round(FICHE19_SCALE, 3), arc=70)
    vanish(kit, "bulle_client", f + 4, d=4)
    landed = f + 9
    tick5 = S.to_world("fiche", sheet.pt(4, "tick"), landed)
    hit = toi.tap(landed - 4, tick5, d=5)                    # contact sur l'arrivée de la réponse
    kit.draw("coche5", hit, 5)                               # dans le carré tireté, qui reste visible
    vanish(kit, "source5", hit, d=4)                         # la question a sa réponse ; sa source : ce client, 9 h
    S.keys("pastille_mini", hit + 1, 4, "inOut", text="Client · 9 h",
           w=round(text_width("Client · 9 h", MINI_PILL["size"], 700) + 84),
           pos=[round(-PAGE_W / 2 + 6 + (text_width("Client · 9 h", MINI_PILL["size"], 700) + 84) / 2, 1),
                rows[4] + ly + 6])
    lean_end = toi.lean_to(hit + 5, 5, d=5)
    client.lean_to(hit + 5, -5, d=5)

    # =================== S20 « Abonne-toi pour comprendre ton argent. » ===================
    out = kit.outro("S20", outs=["fauteuils", "avant", "reponse"], press="argent.", h=CARD_H, pos=CARD_POS)
    S.ents["fin"]["p"].update(titleSize=56, labelSize=36)
    card = out["card"]                                       # image du temps fort calé (1659)
    if lean_end > card - 6:
        kit.warn(f"p3 S19 : la fiche complète ne tient que {card - lean_end} images avant la fin ({lean_end} -> {card})")
    S.key("pastille_fiche", "text", card, "S’abonner")      # sur le mot, avant que la pastille ne bouge
    toi.exit(card)
    client.exit(card)
    for o in ("fauteuils", "avant", "reponse"):             # aucun point résiduel à la fin du morph
        S.key(o, "opacity", card + MORPH - 3, 0, 3, "linear")
    # la fiche s'efface sur une carte blanche de même taille, puis la carte monte au centre et s'élargit
    fw = S.world_scale("fiche", card - 1)
    S.set("fin", w=round(PAGE_W * fw, 1), h=round(PAGE_H * fw, 1), z=7.9)
    S.keys("fin", card - 1, pos=r2(S.val("fiche", "pos", card - 1)), scale=1)
    S.key("fiche", "opacity", card, 0, FADE, "linear")
    S.key("fiche", "scale", card + FADE, 0)
    grow = card + FADE - 2
    S.keys("fin", grow, MORPH, "inOut", pos=list(CARD_POS), w=620, h=CARD_H)
    S.key("fin", "z", grow, 40)
    S.key("fin", "title", card + 4, 0)
    S.key("fin", "title", grow + MORPH - 2, 1, FADE, "out")
    # la pastille quitte l'en-tête (relais) et descend au bas de la carte en grandissant : elle EST le bouton (une
    # seule pilule, un seul libellé, son pictogramme gardé) ; le bouton dessiné par la carte reste caché
    hp = S.to_world("pastille_fiche", [0, 0], card - 1)
    S.keys("pastille", card, pos=r2(hp), scale=round(S.world_scale("pastille_fiche", card - 1), 4), opacity=1,
           z=40.5, text="S’abonner", w=PILL_W)
    S.key("pastille_fiche", "opacity", card, 0)
    S.keys("pastille", card + 2, MOVE, "inOut", pos=list(BTN), scale=BTN_SCALE, w=BTN_W)
    S.key("fin", "btn", card + 6, 0)

    f = kit.at("S20", "comprendre", "le pointeur surgit en bas à droite et glisse jusqu'au bas du bouton S’abonner")
    cur = out["cursor"]
    aim = S.val(cur, "pos", out["press"])
    kit.pop(cur, f, d=4)
    S.key(cur, "pos", f + 2, r2(aim), 10, "inOut")
    press = out["press"]                                     # clic : le bouton (la pastille) s'enfonce puis remonte
    S.key("pastille", "pos", press, [BTN[0], BTN[1] + 7], 2, "out")
    S.key("pastille", "pos", press + 5, list(BTN), 4, "out")
