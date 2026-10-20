"""V01 « Préparer ton entretien client avec l’IA » — mise en scène Story (graphe de scène), fin de S10 puis S11 à S14.

Source : scripts/storyboards/V01.json (fil, distribution, style, temps forts). Chaque temps fort est posé avec
story.beat(scène, mot) : l'image de début de ce mot dans words.json (ou son attaque audible, ACOUSTIC_SNAP). Les durées
sont celles de la référence (pipeline.story : POP, MORPH, MOVE...). Le temps est celui du film.

Extrait (revue 2) : 25,612 -> 41,309 s (make story ID=V01 FROM=25.612 TO=41.309). Il s'ouvre sur le dernier temps fort
de S10, « page. » (amorce de 0,77 s, l'étiquette reste S11-S14) : la 5e pastille, VIDE, sort de la tête de l'IA et se
pose sur la 5e ligne. L'état reconstitué à l'image 0 est donc celui de S10 juste avant « page. » (fenêtre verrouillée et
scellée avec la pile et l'IA, page à 4 puces et un onglet vide, conseiller dehors en bas à droite, marqueur sur « 2 »).

Un seul objet suivi : la fiche du client de 9 h.
- S11 : l'IA l'écrit (L1-L4 par le badge des documents ; pour L5 le badge s'éteint, son cerveau s'allume et la copie de
  la puce vide descend le faisceau de sa tête) et coche tout d'une coche grise. Reflet sous les textes, immobilité. Sur
  « fausse. », la puce vide bat deux fois, L5 rougit et se FEND entre « Horizon » et « 5 ans » : la moitié droite tombe
  sous la coche grise de l'IA, qui ne bouge pas (l'IA ne fait rien).
- S12 : l'IA sort, les coches grises pâlissent, les rangées perdent leur fond ; le conseiller (stylo) trace 5 cases ;
  les documents reviennent du badge avec leur date, se relient par un fil qui part du bout de la valeur ; la date
  quitte le document et glisse le long du fil jusqu'à sa ligne.
- S13 : chaque document remonte son fil et se réduit en sa pastille, posée sur le calendrier de la date : l'étiquette-
  source. L5 lance son fil vers la case 5 vide, il casse, retombe et rentre. Le stylo touche « 5 ans » : un grand « ? »
  en sort, monte dans la bulle du conseiller (« ? » + mini-figurine du client) ; le client apparaît en face, penché.
- S14 : le client se fond dans la bulle, qui devient l'autocollant et attend sous L5. Le conseiller relit : sa coche
  cyan chasse la coche grise de chaque ligne prouvée ; sur L5 il chasse la coche de l'IA, barre « 5 ans », qui tombe
  de la fiche ; l'autocollant prend sa place (« Horizon : ? ») ; il abat le tampon VALIDÉ, l'autocollant bat.
"""
import math

from pipeline.story import (DRAW, DROP, FADE, LEAD, MORPH, MOVE, POP, SCALE, STYLE, TILT, _ease, cubic_at,
                            line_crack_point, point_at_length, text_width, wire_cubic)

# ---------- couleurs (storyboard, section « style » = pipeline.story.STYLE) ----------
INK, CYAN, DEEP, PAPER, RED, AI_TICK = (STYLE[k] for k in ("ink", "cyan", "deep", "paper", "red", "ai_tick"))
ALERT_WORDS = {"fausse", "erreur"}          # sous-titres en rouge (storyboard, typographie)

# ---------- la fiche (coordonnées locales, origine au centre de la page) ----------
W, H, HEAD = 500, 720, 84
ROWS = [-H / 2 + HEAD + 52 + 104 * i for i in range(5)]   # centres des 5 rangées : -224, -120, -16, 88, 192
TY, LY = -22, 23                                           # ligne de texte / ligne de la date, dans la rangée
SLOT_X0, SLOT_X1, SLOT_H, SLOT_STRIP = -W / 2 + 18, W / 2 - 78, 92, 48
BULLET_X, TEXT_X, VALUE_X, TICK_X = -W / 2 + 2, -W / 2 + 44, W / 2 - 100, W / 2 - 50
TICK_SIZE, TICK_SW = 40, 8                                  # coches (IA grise, conseiller cyan) : 40 px, trait 8 px
WIRE_X0, WIRE_X1 = VALUE_X + 12, VALUE_X + 4                # fil de preuve : bout de la valeur, puis bout de la date
L5_VALUE_W = round(text_width("5 ans", 32, 600), 1)
CRACK_X, CRACK_GAP = round(VALUE_X - L5_VALUE_W - 20, 1), 14   # L5 se fend entre « Horizon » et « 5 ans »
TILT_DEG, DROP_PX = 5, 14                                   # storyboard : la moitié droite tombe de 14 px, pivote de 5°
HEADER_PILL = (-W / 2 + 24 + 115, -H / 2 + HEAD / 2)       # place de la pastille dans l'en-tête
STAMP_AT = (70, 305)                                        # tampon : bas de la page, sa poignée reste sous L5
STICKER_PARK = (-50, 292)                                   # l'autocollant attend sous « Horizon », dans la page

# (clé, valeur, pictogramme, titre court du document, date du document MM/AAAA)
LINES = [
    ("Revenus 2024", "82 k€", "euro", "Impôt", "09/2025"),
    ("PEA", "46 k€", "bars", "PEA", "03/2026"),
    ("Retraite", "à 62 ans", "mail", "Mail", "02/2026"),
    ("Assurance-vie", "120 k€", "shield", "Assurance", "12/2025"),
    ("Horizon", "5 ans", "none", None, None),          # L5 : née dans la tête de l'IA, aucun document
]

# Puce-date / étiquette-source (entities.tsx TAG : pictogramme à 24 px du bord gauche, texte à 46 px) et document
# compact = [bande de la date | pastille du pictogramme] (entities.tsx Doc, DOC_DISC).
TAG_SIZE, TAG_H, TAG_ICON_X = 28, 42, 24
TAG_W = round(46 + max(text_width(l[4], TAG_SIZE, 600) for l in LINES[:4]) + 14)
TAG_CX = VALUE_X - TAG_W / 2                               # la date finit au bout de la valeur, sur la 2e ligne
DOC_CW, DOC_CH, DOC_TITLE = TAG_W + 70, 64, 30
DOC_CHIP_X = -DOC_CW / 2 + 8 + TAG_W / 2                   # la date posée sur la bande gauche du document

WRITE_RATE = 3.5      # caractères par image (L1-L4 finissent avant la bascule vers la tête de l'IA)

# Temps forts après un silence (>= 0,2 s) calés sur l'attaque audible de la voix (±80 ms) : relis, décide, Exige...
# Le karaoké suit le même calage (pipeline.story.caption_track, `snapped`).
ACOUSTIC_SNAP = {"gap": 0.2, "window": 0.08}

# Sous-titres : découpes imposées (la découpe automatique isolerait « et à » ou « à poser », 0,3 s). « et à une date »
# fait 4 mots : exception assumée à la règle des 2-3 mots (pipeline.story.OVERRIDE_MAX_WORDS).
CAPTION_GROUPS = [["à un document", "et à une date"], ["c’est une", "question à poser", "au client"]]

# ---------- places à l'écran (1080 x 1920 ; action entre x 40-940 et y 250-1180) ----------
PAGE_S10, PAGE_S10_SCALE = (640, 740), 0.6     # page de commande dans la fenêtre (S10)
PAGE_S11 = (540, 740)                          # au centre, échelle 1 : texte 32 px
PAGE_S12, PAGE_SCALE = (310, 740), 0.95        # à gauche, 0,95 (pastille 28 px -> 26,6 px) : les sources à droite
PAGE_S14 = (420, 740)                          # recentrée pour la relecture (même échelle)
WIN_S10 = dict(pos=[490, 740], w=820, h=640)   # fenêtre de l'outil : x 80-900, y 420-1060
BADGE = dict(pos=[170, 330], w=240, h=170, scale=0.7)   # storyboard : badge en haut à GAUCHE (x 170, y 330)
CASE_X = 800                                   # colonne des cases-sources (monde), bord droit < 930
CASE_W, CASE_H = round(DOC_CW * PAGE_SCALE + 14), round(DOC_CH * PAGE_SCALE + 12)
CORRIDOR_Y = 366                               # couloir des documents au-dessus de la page
MARKER = dict(xs=[440, 540, 640], y=300)
ADV_S10 = ([880, 1100], 0.8)                   # conseiller dehors, en bas à droite (S10)
ADV_S12 = [870, 1080]                          # coin de repos (storyboard x 870, y 1070)
ADV_S13 = [640, 1090]                          # storyboard x 660 : face au client, à 28 px de la page
ADV_S14, ADV_S14_SCALE = [770, 820], 1.1       # à droite de la page, à mi-hauteur : seul le bras descend
CLIENT_S13 = [874, 1090]                       # face au conseiller : 120 px d'ivoire entre eux, ombre x <= 940
IA_S10 = ([230, 880], 0.9)
IA_S11 = [150, 1020]
BUBBLE = [698, 880]                            # bulle du conseiller : au-dessus de lui, déborde vers le client

# Conseiller : bras (épaule -> prise du stylo), stylo de 120 px tenu par sa prise.
SHOULDER = [-30, -16]
HAND = [-58, -6]
PEN_LEN = 120
REST_ROT = 218                                 # stylo tenu pour écrire : pointe en haut à gauche
REST_UP = 255                                  # stylo levé au repos (ne pointe sur rien)
REST_DOWN = 110                                # stylo baissé le long du corps (S13 : il parle, il ne pointe plus)
STAMP_GRIP = [0, -(72 / 2 + 14 + 10)]          # prise du tampon (entities.tsx STAMP_HANDLE), repère du tampon
STAMP_ELBOW = [702, 1004]                      # coude du bras pendant le coup de tampon (monde, hors de la page)

# Bulle (S13) et autocollant (S14) : « ? » ExtraBold + mini-figurine du client (entities.tsx Bubble, ClientGlyph).
BIG = dict(w=236, h=136, r=30, q=100, qx=-52, px=60, ps=64, sw=5, shadow=6, gs=4)
SMALL = dict(w=112, h=60, r=30, q=44, qx=-26, px=27, ps=36, sw=4, shadow=4, gs=3)
FIGURE_H = 191                                 # figurine : tête (-96) -> base (95)


def hand_of(fig, s=1.0):
    return [fig[0] + HAND[0] * s, fig[1] + HAND[1] * s]


def shoulder_of(fig, s=1.0):
    return [fig[0] + SHOULDER[0] * s, fig[1] + SHOULDER[1] * s]


def tip_of(grip, rot):
    r = math.radians(rot)
    return [grip[0] + PEN_LEN * math.cos(r), grip[1] + PEN_LEN * math.sin(r)]


def grip_for_tip(tip, rot):
    r = math.radians(rot)
    return [tip[0] - PEN_LEN * math.cos(r), tip[1] - PEN_LEN * math.sin(r)]


def lerp(a, b, p):
    if isinstance(a, (int, float)):
        return a + (b - a) * p
    return [a[k] + (b[k] - a[k]) * p for k in range(len(a))]


def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return [u ** 3 * p0[k] + 3 * u * u * t * p1[k] + 3 * u * t * t * p2[k] + t ** 3 * p3[k] for k in (0, 1)]


def frames(f, d, e):
    """(image, progression assouplie) d'un segment de d images commençant en f (LEAD : l'image f montre le pas 1/d)."""
    for k in range(int(math.ceil(d))):
        yield f + k, _ease(e, min(1.0, (k + LEAD) / d))


def via_path_point(a, b, via, frac, sag=0.0, tension=0.45):
    """Point à la fraction `frac` de la longueur d'un faisceau routé par `via` (timeline.ts wirePath)."""
    cub = wire_cubic(a, via, sag, tension)
    pts = [cubic_at(cub, i / 32) for i in range(33)] + [list(b)]
    acc = [0.0]
    for i in range(1, len(pts)):
        acc.append(acc[-1] + math.dist(pts[i], pts[i - 1]))
    target = max(0.0, min(1.0, frac)) * acc[-1]
    for i in range(1, len(pts)):
        if acc[i] >= target:
            t = (target - acc[i - 1]) / max(1e-6, acc[i] - acc[i - 1])
            return lerp(pts[i - 1], pts[i], t)
    return pts[-1]


def build(story):
    S = story
    beat = S.beat
    page_pt = lambda local, n: S.to_world("fiche", local, n)   # noqa: E731

    def l5_pt(x, n, crack=1.0):
        """Point (x, ligne de texte) de la moitié droite de L5 cassée, en coordonnées monde à l'image n."""
        q = line_crack_point(line_p[4], [x, TY], crack)
        return page_pt([q[0], ROWS[4] + q[1]], n)

    def pen_at(n, grip, rot=None):
        """Image n : la prise du stylo en `grip` (monde), le stylo orienté à `rot` ; le bras suit (limb)."""
        S.key("stylo", "pos", n, [round(c, 3) for c in grip], 1, "linear")
        if rot is not None:
            S.key("stylo", "rot", n, round(rot, 3), 1, "linear")

    def point(n, tip, fig, s=1.0):
        """Image n : bras et stylo dans le prolongement l'un de l'autre, de l'épaule à la pointe `tip` (monde)."""
        sh = shoulder_of(fig, s)
        rot = math.degrees(math.atan2(tip[1] - sh[1], tip[0] - sh[0])) % 360
        pen_at(n, grip_for_tip(tip, rot), rot)
        return rot

    def knock(tick, g):
        """La coche grise de l'IA est chassée par le stylo : elle tombe en pivotant (370 ms) puis s'efface."""
        x, y = S.val(tick, "pos", g - 1)
        S.key(tick, "pos", g, [x + 18, y + 52], DROP, "out")
        S.key(tick, "rot", g, 35, DROP, "out")
        S.key(tick, "opacity", g + 5, 0, 6, "linear")

    # ======================= distribution : état de S10 juste avant « page. » =======================
    S.add("marqueur", "marker", z=20, **MARKER)
    S.set("marqueur", active=1)                                    # sur « 2 »

    seal_w = round(12 + 24 + 10 + 18 + 4 + text_width("Cabinet", 26, 700) + 16)
    S.add("outil", "window", z=1, sealW=seal_w, sealText="Cabinet")
    S.set("outil", pos=WIN_S10["pos"], w=WIN_S10["w"], h=WIN_S10["h"], scale=1, seal=1, lock=1, opacity=1)

    # La pile du dossier dans la fenêtre : feuilles décalées de 6 px, ombre dure sous la feuille du dessous seulement.
    tag_geom = lambda date: {"w": TAG_W, "h": TAG_H, "date": date, "size": TAG_SIZE}   # noqa: E731
    for i, (_, _, icon, title, date) in enumerate(LINES[:4]):
        d = f"doc{i + 1}"
        S.add(d, "doc", z=12 - 0.1 * i, title=title, icon=icon, date=date, cw=DOC_CW, ch=DOC_CH, titleSize=DOC_TITLE,
              tag=tag_geom(date))
        S.set(d, pos=[252 + 6 * i, 592 + 6 * i], scale=1, compact=0, tag=0, txt=1, sh=6 if i == 3 else 0,
              z=1.5 - 0.01 * i, opacity=1)

    ai = S.png("AI", keep_largest=True)                            # la tête seule (le cube détaché est retiré)
    ai_w = 170                                                    # jamais plus grande que le conseiller
    ai_h = round(ai_w * ai["h"] / ai["w"])
    brain_top, brain_front = [-5, -0.44 * ai_h], [34, -0.28 * ai_h]   # cerveau de verre (repères dans AI.png)
    # Ombre de contact sous le buste seulement ; cubes un peu désaturés (le cyan de la marque reste sur la fiche).
    S.add("ia", "png", z=4, src=ai["src"], w=ai_w, h=ai_h, saturate=0.85,
          contact=dict(w=round(ai_w * 0.72), h=26, dy=4, blur=10, alpha=0.2))
    S.set("ia", pos=IA_S10[0], scale=IA_S10[1])
    S.add("ia_pill", "pill", z=4.1, parent="ia", text="IA", w=round(text_width("IA", 30, 600) + 48), h=50,
          size=30, weight=600, fill=PAPER, sw=4, shadow=5)
    S.set("ia_pill", pos=[0, ai_h / 2 + 22])
    S.add("eclat", "burst", z=4.2, parent="ia", r0=26, r1=70, n=8, sw=6, color=DEEP, a0=-90)
    S.set("eclat", pos=list(brain_front), p=0)

    # La fiche (page de commande) : 5 rangées ; le reflet (« fluide… ») passe SOUS les textes de la page, des rangées
    # et de la pastille (porteur : l'entité « reflet », piste p).
    sheen = lambda dx, dy: {"id": "reflet", "dx": dx, "dy": dy, "w": W, "h": H}   # noqa: E731
    S.add("reflet", "sheen", z=10, parent=None, w=W, h=H, under=True)
    S.set("reflet", p=0)
    S.add("fiche", "fiche", z=8, w=W, h=H, title="Brief", headerH=HEAD, tabs=[r + TY for r in ROWS], tabX=BULLET_X,
          sheen=sheen(0, 0))
    S.set("fiche", pos=list(PAGE_S10), scale=PAGE_S10_SCALE, tab0=0, tab1=0, tab2=0, tab3=0, tab4=1)
    line_p = {}
    for i, (k, v, icon, _, _) in enumerate(LINES):
        p = dict(key=k, value=v, icon=icon, x0=SLOT_X0, x1=SLOT_X1, h=SLOT_H, hStrip=SLOT_STRIP, ty=TY,
                 bulletX=BULLET_X, textX=TEXT_X, valueX=VALUE_X, valueW=round(text_width(v, 32, 600), 1),
                 crackX=CRACK_X, gap=CRACK_GAP, tilt=TILT_DEG, drop=DROP_PX, fallPx=240, strikeW=7,
                 sheen=sheen(0, ROWS[i]))
        line_p[i] = p
        S.add(f"L{i + 1}", "line", z=9, parent="fiche", **p)
        S.set(f"L{i + 1}", pos=[0, ROWS[i]], chars=0, red=0, crack=0, flash=0, pulse=0, alarm=0, strike=0, fall=0,
              grow=0, dimValue=0, slotFill=1, bulletOn=0 if i == 4 else 1, opacity=1)

    # Pastille « Client · 9 h » : titre de la fenêtre. Enfant de la fiche dès le départ (elle s'y posera).
    S.add("pastille", "pill", z=12.5, parent="fiche", text="Client · 9 h", w=230, h=56, size=28, weight=700, fill=CYAN,
          sheen=sheen(*HEADER_PILL))
    title_pt = [WIN_S10["pos"][0], WIN_S10["pos"][1] - WIN_S10["h"] / 2 + 28]
    S.set("pastille", pos=S.to_local("fiche", title_pt, 0), scale=1 / PAGE_S10_SCALE)

    # La 5e pastille, vide (le trait pointillé de l'IA) : elle naîtra de la tête de l'IA (S10 puis S11).
    S.add("pastille5", "bullet", z=13, icon="none", r=22)
    S.set("pastille5", pos=[0, 0], scale=0, opacity=1)

    # Conseiller, son bras et son stylo (le bras va de l'épaule à la prise du stylo ; ils n'entrent qu'avec lui).
    S.add("conseiller", "figure", z=15, variant="ink")
    S.set("conseiller", pos=ADV_S10[0], scale=ADV_S10[1], lean=0)
    S.add("bras", "limb", z=15.5, a={"id": "conseiller", "at": SHOULDER}, b={"id": "stylo", "at": [0, 0]}, sw=13,
          pivot=[0, 95], pivotTrack="lean")
    S.set("bras", opacity=0, bend=0, elbow=[0, 0])
    S.add("stylo", "pen", z=16, len=PEN_LEN)
    S.set("stylo", pos=hand_of(ADV_S12), rot=REST_ROT, scale=0, opacity=1)
    S.add("client", "figure", z=15, variant="paper")
    S.set("client", pos=CLIENT_S13, scale=0, lean=0, opacity=1)

    # Faisceaux de l'IA (pointillés) : tête -> badge (lecture), badge -> ligne (écriture), tête -> L5 (sans document).
    beam = dict(color=DEEP, sw=7, dash=[0.01, 17])
    S.add("faisceau_lit", "wire", z=13, a={"id": "ia", "at": brain_top}, b={"id": "outil", "at": [-80, 85]}, **beam)
    S.set("faisceau_lit", draw=0)
    S.add("faisceau", "wire", z=13, a={"id": "outil", "at": [80, 85]}, **beam)
    S.set("faisceau", draw=0, pb=[0, 0], via=[0, 0])
    S.add("faisceau_tete", "wire", z=13, a={"id": "ia", "at": brain_front}, **beam)
    S.set("faisceau_tete", draw=0, pb=[0, 0], via=[0, 0])

    for i in range(5):   # coche de l'IA : une coche grise simple (encre ~50 %), même taille que celle du conseiller
        S.add(f"coche_ia{i + 1}", "tick", z=11, parent="fiche", color=AI_TICK, sw=TICK_SW, size=TICK_SIZE)
        S.set(f"coche_ia{i + 1}", pos=[TICK_X, ROWS[i] + TY], draw=0, scale=1, rot=0, opacity=1)
    for i in range(4):
        S.add(f"coche{i + 1}", "tick", z=11.2, parent="fiche", color=DEEP, sw=TICK_SW, size=TICK_SIZE)
        S.set(f"coche{i + 1}", pos=[TICK_X, ROWS[i] + TY], draw=0)
    for i in range(5):
        S.add(f"case{i + 1}", "case", z=5, w=CASE_W, h=CASE_H)
        S.set(f"case{i + 1}", pos=[0, 0], scale=0, draw=1, opacity=1)
    for i in range(4):
        S.add(f"fil{i + 1}", "wire", z=11, a={"id": "fiche", "at": [WIRE_X0, ROWS[i] + TY]},
              b={"id": f"doc{i + 1}", "at": [0, 0]}, color=DEEP, sw=5, dots=True, endDot=False)
        S.set(f"fil{i + 1}", draw=0, aAt=[WIRE_X0, ROWS[i] + TY], opacity=1)
        # la date du document (puce-date), puis l'étiquette-source de la ligne : au-dessus des documents
        S.add(f"source{i + 1}", "label", z=12.6, parent="fiche", icon=LINES[i][2], tag=tag_geom(LINES[i][4]))
        S.set(f"source{i + 1}", pos=[TAG_CX, ROWS[i] + LY], scale=0, pop=1, lit=0, tagged=0, flash=0, opacity=0)
    # Fil d'essai de L5 : le même fil plein que L1-L4, accroché au bout de la valeur de la moitié tombée.
    l5_end = line_crack_point(line_p[4], [WIRE_X0, TY], 1.0)
    S.add("fil5", "wire", z=11, a={"id": "fiche", "at": [round(l5_end[0], 2), round(ROWS[4] + l5_end[1], 2)]},
          color=DEEP, sw=5, dots=True, dashAlt=[14, 11])
    S.set("fil5", draw=0, pb=[0, 0], sag=0, dashed=0, **{"from": 0})

    tail_tip = [ADV_S13[0] - BUBBLE[0], ADV_S13[1] - 96 - 4 - BUBBLE[1]]   # sur la tête du conseiller
    bubble_p = dict(big=BIG, small=SMALL, tail=tail_tip, tailBase=[-74, -40])
    S.add("question", "qmark", z=17)
    S.set("question", pos=[0, 0], scale=0, gs=110, opacity=1)
    S.add("bulle", "bubble", z=14, **bubble_p)
    S.set("bulle", pos=BUBBLE, scale=0, s=0, q=0, pulse=0, opacity=1)
    # L'autocollant posé sur la page (enfant de la fiche) : il prend le relais de la bulle à son arrivée.
    S.add("autocollant", "bubble", z=11.6, parent="fiche", **bubble_p)
    S.set("autocollant", pos=list(STICKER_PARK), scale=1, s=1, q=1, pulse=0, opacity=0)
    S.add("tampon", "stamp", z=11.8, parent="fiche", text="VALIDÉ", w=230, h=72, size=40)
    S.set("tampon", pos=list(STAMP_AT), rot=-8, scale=0, handle=1, opacity=0)

    # ======================= S10 « … d’une page. » (amorce de l'extrait) =======================
    f = beat("S10", "page.", "une 5e pastille, vide, sort du cerveau de verre de l'IA (éclat, pop 250 ms) et tombe sur "
             "l'onglet 5 (400 ms) ; puis tout s'immobilise")
    brain0 = S.to_world("ia", brain_front, f)
    S.key("pastille5", "pos", f - 1, [round(c, 2) for c in brain0])
    S.key("pastille5", "scale", f, 1.0, 7, "out")
    S.key("eclat", "p", f, 1, 9, "linear")
    tab5 = page_pt([BULLET_X, ROWS[4] + TY], f)
    S.fly("pastille5", f + 7, 12, "inOut", to=tab5, scale=PAGE_S10_SCALE, arc=70)
    landed = f + 7 + 12
    S.key("pastille5", "opacity", landed, 0)
    S.key("fiche", "tab4", landed, 0)
    S.key("L5", "bulletOn", landed, 1)

    # ======================= S11 « Mais une IA peut produire une réponse fluide… et fausse. » =======================
    f = beat("S11", "Mais", "la fenêtre se réduit en badge (en haut à gauche) avec la pile, la page vient au centre, "
             "la pastille se pose sur son en-tête ; l'IA glisse à gauche avec la page ; le conseiller se réduit en point")
    S.keys("fiche", f, MORPH, "out", pos=list(PAGE_S11), scale=1)
    S.keys("outil", f, MORPH, "out", pos=BADGE["pos"], w=BADGE["w"], h=BADGE["h"], scale=BADGE["scale"], seal=0)
    for i in range(4):   # pile miniature : cartes compactes, ombre sous celle du dessous
        S.keys(f"doc{i + 1}", f, MORPH, "out", pos=[BADGE["pos"][0] - 8 + 5 * i, BADGE["pos"][1] + 12 + 5 * i],
               scale=0.55, compact=1, txt=0)
    S.keys("ia", f, MORPH, "out", pos=IA_S11, scale=1)            # même assouplissement que la page : jamais dessus
    S.key("conseiller", "scale", f, 0, SCALE, "out")
    head_end = [PAGE_S11[0] + HEADER_PILL[0], PAGE_S11[1] + HEADER_PILL[1]]
    start = S.to_world("pastille", [0, 0], f - 1)
    S.path("pastille", f, 17, "inOut", lambda p: [start[0] + (head_end[0] - start[0]) * p,
                                                  start[1] + (head_end[1] - start[1]) * p - 40 * 4 * p * (1 - p)],
           lambda p: 1.0)

    # Écriture : le faisceau descend la marge gauche (hors de la colonne des puces) et entre dans la puce de la ligne
    # par la gauche ; le texte sort de la puce. Il ne passe jamais sur le texte.
    via_x = PAGE_S11[0] + BULLET_X - 22 - 26          # 26 px à gauche de la colonne des puces
    row_y = [PAGE_S11[1] + r + TY for r in ROWS]
    plug = lambda i: [via_x + 24, row_y[i]]           # noqa: E731  bord gauche de la puce i
    bullet5 = [PAGE_S11[0] + BULLET_X, row_y[4]]

    f = beat("S11", "IA", "faisceau pointillé de la tête de l'IA au badge des documents, puis du badge vers la puce de L1")
    S.key("faisceau_lit", "draw", f, 1, DRAW, "out")
    S.set("faisceau", via=[via_x, row_y[0]], pb=plug(0))
    S.key("faisceau", "draw", f + 4, 1, DRAW, "out")

    f = beat("S11", "produire", "L1-L4 s'écrivent par le badge (3,5 car./image) et l'IA coche chacune en gris ; puis "
             "bascule (8 images) : le badge s'éteint, le cerveau s'allume, la copie de la puce vide descend le faisceau "
             "de la tête jusqu'à L5, qui s'écrit")
    starts, t = [], f
    for i, (k, v, *_r) in enumerate(LINES[:4]):
        starts.append(t)
        t += (len(k) + len(v)) / WRITE_RATE
    gap0 = math.ceil(t)                                   # première image après L4
    for i, (k, v, *_r) in enumerate(LINES[:4]):
        n = len(k) + len(v)
        s = starts[i]
        S.key(f"L{i + 1}", "chars", s, n, n / WRITE_RATE, "linear")
        S.key(f"L{i + 1}", "flash", s, 1, 2, "out")
        S.key(f"L{i + 1}", "flash", s + 2, 0, 3, "inOut")
        S.key(f"coche_ia{i + 1}", "draw", math.ceil(s + n / WRITE_RATE), 1, 4, "out")
        if i > 0:                                          # le bout du faisceau saute à la puce suivante
            g = math.ceil(s - 1e-6)
            S.key("faisceau", "pb", g, plug(i), 1, "linear")
            S.key("faisceau", "via", g, [via_x, row_y[i]], 1, "linear")
    # Bascule : le faisceau du badge se retire et le badge s'éteint (40 %) ; le cerveau de l'IA s'allume ; un faisceau
    # part de sa tête et la copie de la puce vide le descend jusqu'à la puce de L5.
    S.key("faisceau", "draw", gap0, 0, 3, "in")
    S.key("faisceau_lit", "draw", gap0, 0, 3, "in")
    S.key("outil", "opacity", gap0, 0.4, 6, "out")
    for i in range(4):
        S.key(f"doc{i + 1}", "opacity", gap0, 0.4, 6, "out")
    S.key("eclat", "p", gap0 + 1, 0)
    S.key("eclat", "p", gap0 + 2, 1, 8, "linear")
    S.set("faisceau_tete", via=[via_x, row_y[4]], pb=plug(4))
    S.key("faisceau_tete", "draw", gap0 + 2, 1, 4, "out")
    brain1 = S.to_world("ia", brain_front, gap0)
    S.key("pastille5", "pos", gap0 + 1, [round(c, 2) for c in brain1])
    S.key("pastille5", "scale", gap0 + 1, 0)
    S.key("pastille5", "opacity", gap0 + 1, 1)
    S.key("pastille5", "scale", gap0 + 2, 1, 3, "out")
    # le long du faisceau de la tête (cubique jusqu'au point de passage, puis droit dans la puce de L5)
    S.path("pastille5", gap0 + 3, 5, "inOut", lambda p: via_path_point(brain1, bullet5, [via_x, row_y[4]], p))
    l5_start = gap0 + 8
    S.key("pastille5", "opacity", l5_start, 0)
    n5 = len(LINES[4][0]) + len(LINES[4][1])
    S.key("L5", "chars", l5_start, n5, n5 / WRITE_RATE, "linear")
    S.key("L5", "flash", l5_start, 1, 2, "out")
    S.key("L5", "flash", l5_start + 2, 0, 3, "inOut")
    end5 = math.ceil(l5_start + n5 / WRITE_RATE)
    S.key("coche_ia5", "draw", end5, 1, 4, "out")
    S.key("faisceau_tete", "draw", end5, 0, 3, "in")

    f = beat("S11", "fluide…", "un reflet cyan pâle large de 110 px traverse la page en diagonale SOUS les textes "
             "(400 ms), puis immobilité totale jusqu'à « fausse »")
    S.key("reflet", "p", f, 1, 12, "linear")

    beat("S11", "et", "tenue : rien ne bouge")

    f = beat("S11", "fausse.", "la puce vide de L5 bat deux fois (x1,6), les 4 autres puces immobiles ; L5 rougit ; elle "
             "se fend entre « Horizon » et « 5 ans » (fente de 14 px) et la moitié droite tombe de 14 px en pivotant de "
             "5° (300 ms) ; la coche grise de l'IA reste où elle était : l'IA ne fait rien")
    for dt, v in ((0, 1), (2, 0), (4, 1), (6, 0)):
        S.key("L5", "pulse", f + dt, v, 2, "out" if v else "inOut")
    S.key("L5", "alarm", f + 6, 1, 3, "out")
    S.key("L5", "red", f + 6, 1, 3, "out")
    S.key("L5", "crack", f + 8, 1, 9, "out")

    # ======================= S12 « Exige que chaque ligne renvoie à un document et à une date. » =======================
    f_exige = f = beat("S12", "Exige", "l'IA sort par la gauche ; ses coches grises pâlissent (25 %) et les rangées "
                       "perdent leur fond ; la page glisse à gauche (0,95) ; le conseiller apparaît en bas à droite, stylo "
                       "en main (pop 300 ms)")
    S.key("ia", "pos", f, [-190, IA_S11[1]], MOVE, "inOut")
    S.keys("fiche", f, 12, "inOut", pos=list(PAGE_S12), scale=PAGE_SCALE)
    for i in range(5):
        S.key(f"coche_ia{i + 1}", "opacity", f, 0.25, FADE, "out")
    for i in range(4):
        S.key(f"L{i + 1}", "slotFill", f, 0, FADE, "out")
    S.key("conseiller", "pos", f - 1, list(ADV_S12))
    for n, p in frames(f, POP, "out"):
        S.key("conseiller", "scale", n, round(p, 5), 1, "linear")
        pen_at(n, hand_of(ADV_S12, p))
        S.key("stylo", "scale", n, round(p, 5), 1, "linear")
    S.key("bras", "opacity", f + 2, 1, 3, "out")

    # « que » (premier « que » après Exige, mot hors temps fort du storyboard) : 5 cases vides jaillissent de la
    # pointe du stylo, de la plus proche (L5) à la plus haute ; elles sont prêtes avant l'arrivée des documents.
    f = S.word_after("que", f_exige)
    tip12 = tip_of(hand_of(ADV_S12), REST_ROT)
    case_y = [PAGE_S12[1] + r * PAGE_SCALE for r in ROWS]
    for i in range(5):
        g = f + (4 - i)
        S.key(f"case{i + 1}", "pos", g - 1, [round(c, 2) for c in tip12])
        S.keys(f"case{i + 1}", g, 6, "out", pos=[CASE_X, round(case_y[i], 2)], scale=1)
    S.key("stylo", "rot", f, REST_ROT - 14, 4, "out")
    S.key("stylo", "rot", f + 4, REST_ROT, 6, "inOut")

    f = beat("S12", "chaque", "les 4 documents sortent du badge, de L1 à L4, par le couloir au-dessus de la page, avec "
             "leur pictogramme et leur date, et se logent dans leur case, qui s'efface ; la case 5 reste vide ; le "
             "badge vide se réduit en point avant « renvoie »")
    land = {}
    for i in range(4):
        d, src = f"doc{i + 1}", f"source{i + 1}"
        g = f + 2 * i
        p0 = S.to_world(d, [0, 0], g - 1)
        s0 = S.world_scale(d, g - 1)
        p3 = [CASE_X, case_y[i]]
        p1, p2 = [560, CORRIDOR_Y], [CASE_X, CORRIDOR_Y]
        S.key(d, "z", g, 12 + 0.1 * i)                   # le suivant passe devant ceux déjà posés
        S.key(d, "sh", g, 5)
        S.key(d, "opacity", g, 1, 3, "out")
        S.path(d, g, 13, "inOut", lambda p, p0=p0, p3=p3: cubic(p0, p1, p2, p3, p),
               lambda p, s0=s0: s0 + (PAGE_SCALE - s0) * min(1.0, 1.6 * p))
        land[i] = g + 12
        # la date voyage posée sur la bande gauche du document (même échelle que lui)
        S.key(src, "opacity", g - 1, 0)
        S.key(src, "opacity", g, 1, 3, "out")
        for n in range(g, land[i] + 1):
            S.key(src, "pos", n, [round(c, 3) for c in S.to_local("fiche", S.to_world(d, [DOC_CHIP_X, 0], n), n)], 1,
                  "linear")
            S.key(src, "scale", n, round(S.world_scale(d, n) / S.world_scale("fiche", n), 5), 1, "linear")
        S.key(f"case{i + 1}", "opacity", land[i] - 2, 0, 4, "out")   # la case s'efface sous le document qui s'y pose
    S.key("outil", "scale", f + 2 * 3 + 2, 0, 8, "out")

    f = beat("S12", "renvoie", "fil plein du bout de « 82 k€ » jusqu'au document de L1")
    S.key("fil1", "draw", f, 1, DRAW, "out")
    f = beat("S12", "document", "fils de L2, L3, L4 vers leur document")
    for i in (1, 2, 3):
        S.key(f"fil{i + 1}", "draw", f + 3 * (i - 1), 1, DRAW, "out")

    f = beat("S12", "date.", "la date de chaque document (calendrier) quitte sa bande et glisse le long du fil jusque "
             "sous sa valeur ; le bout du fil descend avec elle (400 ms)")
    for i in range(4):
        g = f + 2 * i
        src, fil = f"source{i + 1}", f"fil{i + 1}"
        S.key(fil, "aAt", g, [WIRE_X1, ROWS[i] + LY], 12, "inOut")
        on_doc = DOC_CHIP_X * PAGE_SCALE
        at_line = -(TAG_W / 2 + (WIRE_X1 - VALUE_X)) * PAGE_SCALE
        S.along_wire(src, fil, g, 12, "inOut", 1.0, 0.0, at_frame=g + 12,
                     offset=lambda p, a=on_doc, b=at_line: (a + (b - a) * p, 0))

    # ======================= S13 « Une info sans source, c’est une question à poser au client. » =======================
    f = beat("S13", "Une", "chaque document remonte son fil (qui rentre derrière lui) et se réduit en sa pastille, qui "
             "se pose sur le calendrier de sa date : la puce-date devient l'étiquette-source (350 ms)")
    for i in range(4):
        d, src, fil = f"doc{i + 1}", f"source{i + 1}", f"fil{i + 1}"
        dur = 11
        S.key(d, "z", f, 12.8 + 0.01 * i)                 # au-dessus de la date qu'il va rejoindre
        target = page_pt([TAG_CX - TAG_W / 2 + TAG_ICON_X, ROWS[i] + LY], f)
        cub = S.wire_cubic(fil, f - 1)                    # du bout de la date (A) au centre du document (B)

        def along(p, cub=cub, target=target):
            q = point_at_length(cub, 1 - p)
            return [q[0] + (target[0] - cub[0][0]) * p, q[1] + (target[1] - cub[0][1]) * p]
        S.path(d, f, dur, "inOut", along)
        S.key(d, "tag", f, 1, dur, "inOut")
        arrive = f + dur - 1
        S.key(fil, "opacity", arrive - 2, 0, 2, "linear")
        S.key(d, "opacity", arrive + 1, 0)
        S.key(src, "tagged", arrive + 1, 1)
        S.key(src, "flash", arrive + 1, 1, 1, "out")
        S.key(src, "flash", arrive + 2, 0, 2, "inOut")

    f = beat("S13", "sans", "lignes prouvées à 50 % ; L5 lance le même fil plein vers la case 5 : elle est vide, elle "
             "tremble, le fil casse en tirets, retombe dans la page puis rentre dans L5 ; la case s'efface")
    for i in range(4):
        for e in (f"L{i + 1}", f"source{i + 1}"):
            S.key(e, "opacity", f, 0.5, FADE, "out")
    case5 = [CASE_X, round(case_y[4], 2)]
    S.set("fil5", pb=[case5[0] - CASE_W / 2 + 2, case5[1]])
    S.key("fil5", "draw", f, 1, DRAW, "out")
    hit = f + DRAW
    for dt, dx in ((0, 6), (1, -5), (2, 0)):
        S.key("case5", "pos", hit + dt, [case5[0] + dx, case5[1]])
    S.key("fil5", "dashed", hit + 2, 1)
    hang = page_pt([WIRE_X0 + 50, ROWS[4] + 110], hit)          # retombe DANS la page, sous la ligne
    S.key("fil5", "pb", hit + 3, [round(c, 2) for c in hang], DROP, "out")
    S.key("fil5", "sag", hit + 3, 30, DROP, "out")
    S.key("fil5", "draw", hit + 14, 0, 7, "in")                  # le fil mort rentre dans L5
    S.key("case5", "opacity", hit + 14, 0, FADE, "out")

    f = beat("S13", "c’est", "le conseiller s'avance (x 640, 400 ms) et pose la pointe de son stylo sur « 5 ans »")
    vc = l5_pt(VALUE_X - L5_VALUE_W / 2, f)
    a0 = S.to_world("conseiller", [0, 0], f - 1)
    grip0 = S.val("stylo", "pos", f - 1)
    rot0 = S.val("stylo", "rot", f - 1)
    sh1 = shoulder_of(ADV_S13)
    rot1 = math.degrees(math.atan2(vc[1] - sh1[1], vc[0] - sh1[0])) % 360
    tip0 = tip_of(grip0, rot0)
    for n, p in frames(f, 12, "inOut"):
        S.key("conseiller", "pos", n, [round(c, 3) for c in lerp(a0, ADV_S13, p)], 1, "linear")
        rot = rot0 + (rot1 - rot0) * p
        pen_at(n, grip_for_tip(lerp(tip0, vc, p), rot), rot)

    f = beat("S13", "question", "un grand « ? » encre (110 px) sort de « 5 ans » sous la pointe du stylo (pop 300 ms) "
             "et se pose juste dessous, dans la page ; il y reste 6 images")
    q_at = [vc[0], vc[1] + 93]
    S.key("question", "pos", f - 1, [round(c, 2) for c in vc])
    S.path("question", f, POP, "out", lambda p: lerp(vc, q_at, p), lambda p: max(0.001, p))

    f = beat("S13", "poser", "la bulle du conseiller grandit depuis sa tête (« ? » vide + mini-figurine du client, du "
             "côté du client) ; le « ? » y monte en arc ; le stylo se relève")
    tip_w = [BUBBLE[0] + tail_tip[0], BUBBLE[1] + tail_tip[1]]
    S.key("bulle", "pos", f - 1, tip_w)
    S.keys("bulle", f, POP, "out", pos=BUBBLE, scale=1)
    slot = [BUBBLE[0] + BIG["qx"], BUBBLE[1]]
    S.fly("question", f, 10, "inOut", to=slot, scale=BIG["q"] / 110, arc=50)
    S.key("question", "opacity", f + 10, 0)
    S.key("bulle", "q", f + 10, 1)
    g0, r0 = S.val("stylo", "pos", f - 1), S.val("stylo", "rot", f - 1)
    g1 = hand_of(ADV_S13)
    for n, p in frames(f, 10, "inOut"):
        pen_at(n, lerp(g0, g1, p), r0 + (REST_DOWN - r0) * p)

    f = beat("S13", "client.", "le client apparaît face au conseiller (x 874, pop 300 ms), 120 px d'ivoire entre eux, et "
             "s'incline de 5° vers lui")
    S.key("client", "scale", f, 1, POP, "out")
    S.key("client", "lean", f + 3, -5, TILT, "out")

    # ======================= S14 « Dernière étape : relis, corrige, décide. » =======================
    f = beat("S14", "Dernière", "marqueur sur « 3 » ; le client se fond dans sa mini-figurine de la bulle, puis la bulle "
             "se réduit en autocollant « ? » + client et se pose sous « Horizon », dans la page")
    S.key("marqueur", "active", f, 2, MOVE, "inOut")
    b0 = list(BUBBLE)
    fly0, fly_d = f + 2, 10
    park_w = page_pt(list(STICKER_PARK), fly0 + fly_d - 1)
    S.path("bulle", fly0, fly_d, "inOut", lambda p: lerp(b0, park_w, p), lambda p: 1 + (PAGE_SCALE - 1) * p)
    S.key("bulle", "s", fly0, 1, fly_d, "inOut")
    arrive = fly0 + fly_d - 1
    S.key("bulle", "opacity", arrive + 1, 0)
    S.key("autocollant", "opacity", arrive + 1, 1)
    c0 = list(CLIENT_S13)
    for n, p in frames(f, 9, "inOut"):
        sb = S.val("bulle", "s", n)
        bs = S.world_scale("bulle", n)
        gx = BIG["px"] + (SMALL["px"] - BIG["px"]) * sb
        gh = BIG["ps"] + (SMALL["ps"] - BIG["ps"]) * sb
        tgt = S.to_world("bulle", [gx, 0], n)
        S.key("client", "pos", n, [round(c, 3) for c in lerp(c0, tgt, p)], 1, "linear")
        S.key("client", "scale", n, round(1 + (gh * bs / FIGURE_H - 1) * p, 5), 1, "linear")
    S.key("client", "lean", f, 0, 6, "out")
    S.key("client", "opacity", f + 9, 0)

    f = beat("S14", "étape :", "la page se recentre (350 ms) ; le conseiller se place à sa droite, à mi-hauteur, stylo "
             "sur la coche de L1 ; toutes les lignes et les coches grises à 100 %")
    S.keys("fiche", f, MORPH, "inOut", pos=list(PAGE_S14))
    tick_w = lambda i, n: page_pt([TICK_X, ROWS[i] + TY], n)   # noqa: E731
    l1 = tick_w(0, f + MORPH)
    a0 = S.to_world("conseiller", [0, 0], f - 1)
    g0, r0 = S.val("stylo", "pos", f - 1), S.val("stylo", "rot", f - 1)
    sh14 = shoulder_of(ADV_S14, ADV_S14_SCALE)
    rot_l1 = math.degrees(math.atan2(l1[1] - sh14[1], l1[0] - sh14[0])) % 360
    g1 = grip_for_tip(l1, rot_l1)
    for n, p in frames(f, MORPH, "inOut"):
        S.key("conseiller", "pos", n, [round(c, 3) for c in lerp(a0, ADV_S14, p)], 1, "linear")
        S.key("conseiller", "scale", n, round(1 + (ADV_S14_SCALE - 1) * p, 5), 1, "linear")
        pen_at(n, lerp(g0, g1, p), r0 + (rot_l1 - r0) * p)       # le stylo garde 120 px
    for i in range(4):
        for e in (f"L{i + 1}", f"source{i + 1}"):
            S.key(e, "opacity", f, 1, FADE, "out")
    for i in range(5):
        S.key(f"coche_ia{i + 1}", "opacity", f, 1, FADE, "out")

    f = beat("S14", "relis,", "seul le bras descend : la pointe du stylo descend la colonne des coches à vitesse "
             "constante (600 ms) ; sur L1-L4 elle chasse la coche grise de l'IA, qui tombe, et trace la coche cyan ; "
             "chaque étiquette s'allume ; arrêt sur la coche grise de L5")
    run = 18
    t1, t5 = tick_w(0, f), tick_w(4, f)
    for n, p in frames(f, run, "linear"):
        point(n, lerp(t1, t5, p), ADV_S14, ADV_S14_SCALE)
    for i in range(4):
        g = f + round(run * (ROWS[i] - ROWS[0]) / (ROWS[4] - ROWS[0]))   # image où la pointe passe sur la coche i
        knock(f"coche_ia{i + 1}", g)
        S.key(f"coche{i + 1}", "draw", g + 1, 1, FADE, "out")
        S.key(f"source{i + 1}", "lit", g + 1, 1, 4, "out")

    f = beat("S14", "corrige,", "le stylo chasse la coche grise de L5 ; il barre « 5 ans » d'un trait encre (200 ms, "
             "7 px), L5 repasse à l'encre ; « 5 ans » barré se détache et tombe de la fiche (370 ms) ; la fente se "
             "referme ; l'autocollant glisse à la place de la valeur : « Horizon : ? »")
    knock("coche_ia5", f)
    s0w = l5_pt(VALUE_X + 8, f)
    s1w = l5_pt(VALUE_X - L5_VALUE_W - 8, f)
    tipA = t5
    for n, p in frames(f, 3, "inOut"):
        point(n, lerp(tipA, s0w, p), ADV_S14, ADV_S14_SCALE)
    for n, p in frames(f + 3, 6, "inOut"):
        rot_s1 = point(n, lerp(s0w, s1w, p), ADV_S14, ADV_S14_SCALE)
    S.key("L5", "strike", f + 3, 1, 6, "inOut")
    S.key("L5", "red", f, 0, 4, "out")            # le stylo du conseiller prend L5 : le rouge finit sur « corrige »
    S.key("L5", "alarm", f, 0, 4, "out")
    S.key("L5", "fall", f + 9, 1, 10, "out")
    S.key("L5", "crack", f + 10, 0, 8, "inOut")
    S.key("L5", "slotFill", f + 10, 0, FADE, "out")
    S.key("autocollant", "pos", f + 11, [VALUE_X - SMALL["w"] / 2, ROWS[4] + TY], 8, "inOut")
    rest14 = hand_of(ADV_S14, ADV_S14_SCALE)
    g0 = grip_for_tip(s1w, rot_s1)
    for n, p in frames(f + 9, 8, "inOut"):
        pen_at(n, lerp(g0, rest14, p), rot_s1 + (REST_UP - rot_s1) * p)

    f = beat("S14", "décide.", "le conseiller abat le tampon VALIDÉ, tenu par son poignée au bout de son bras, sur la "
             "bande vide sous L5 (1,4 -> 1 en 200 ms ease-out, -8°, secousse de 2 images) ; il plonge de 6 px ; "
             "l'autocollant « ? » bat x1,3 : validé, une question gardée")
    S.key("tampon", "scale", f - 1, 1.4)
    S.key("tampon", "opacity", f, 1)
    S.key("tampon", "scale", f, 1.0, 6, "out")
    hit = f + 5                                        # première image à l'échelle 1
    S.key("stylo", "opacity", f, 0)
    S.key("stylo", "rot", f, REST_UP)
    for dt, dxy in ((1, (4, -3)), (2, (-3, 2)), (3, (0, 0))):
        S.key("fiche", "pos", hit + dt, [PAGE_S14[0] + dxy[0], PAGE_S14[1] + dxy[1]])
    for n in range(f, hit + 4):
        pen_at(n, S.to_world("tampon", STAMP_GRIP, n))
    # le bras descend hors de la page puis entre sous L5 (coude) : il ne passe ni sur L5 ni sur l'autocollant
    S.key("bras", "elbow", f - 1, list(STAMP_ELBOW))
    S.key("bras", "bend", f, 1)
    S.key("conseiller", "pos", hit, [ADV_S14[0], ADV_S14[1] + 6], 3, "out")
    S.key("conseiller", "pos", hit + 3, list(ADV_S14), 4, "inOut")
    S.key("conseiller", "lean", hit, -6, 3, "out")
    S.key("conseiller", "lean", hit + 3, 2, 3, "inOut")
    S.key("conseiller", "lean", hit + 6, 0, 3, "inOut")
    S.key("tampon", "handle", hit + 3, 0, 3, "linear")
    S.key("stylo", "opacity", hit + 4, 1)
    gS = S.to_world("tampon", STAMP_GRIP, hit + 3)
    for n, p in frames(hit + 4, 6, "inOut"):
        pen_at(n, lerp(gS, rest14, p))
    S.key("bras", "bend", hit + 4, 0, 6, "inOut")
    S.key("autocollant", "pulse", hit + 2, 1.2, 3, "out")
    S.key("autocollant", "pulse", hit + 5, 0, 4, "inOut")
