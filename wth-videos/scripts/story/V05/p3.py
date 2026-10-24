"""V05, partie 3 : S15-S22, images 1752-2684 (33 temps forts, 31,0 s). Erreur 4 (diagonale), la parade, le client, fin.

Revue 1 (prime sur le détail ci-dessous) : S15 cartes effacées avant le retour, « Hypothèse » surgit sur place, L5
soulignée en tirets ; diagonale en 7 images avec traits de vitesse ; « bien » : les coches de l'IA battent (plus de
reflet) ; coche hâtive grande et de travers ; S16 : la pointe la tapote, elle bascule et tombe au sol ; copie
« 12 000 € » sur pastille au-dessus du fil (posée à f + 13), loupe de L1 dans la bande basse ; S17 : remplacement sur
place, fil du relevé allumé ; dossier qui s'efface d'un bloc ; « Toi » au repos sur « parade » ; S19 : valeurs au sol
en z 12 ; S20 : anneau autour de la case, surligné + souligné, « mars 2027 » se soulève et retombe ; S21 : question
sur pastille par la droite du brief, bulle et réponse dans la colonne libre ; S22 : sorties en points, une à une.

Temps forts (image = round(t x 30), avant calage acoustique) :
S15  Quatrième@1752  relire@1785  diagonale.@1800  bien@1847  confiance.@1882
S16  C’est@1910  ralentir :@1947  chiffres,@1976  dates,@1997  noms,@2015  montants.@2029
S17  Comment@2058  tout@2080  Avec@2138  parade@2151
S18  Ajoute@2178  rubrique@2207  « Informations@2243
S19  Tout@2307  va,@2335  forme@2352  question@2365  poser@2381  client.@2393
S20  case@2420  mieux@2439  fabriqué.@2454
S21  client@2484  pardonnera@2497  question,@2516  pas@2536
S22  Abonne-toi@2594  argent.@2646

État d'entrée (etat_initial de S15) : kit.pin(seam(S, "S15"), ENTRY_P3). Cartes A et B, « ≠ », pilule `hypothese`
(840, 515) ; brief (600, 1010) et dossier (300, 1010) réduits x 0,6 ; repère sur 3 ; « Toi » à TOI_S13 (garde-fou :
entrée à TOI_S13 si la partie est construite seule).

Mise en scène (ce qui est implémenté) :
- S15 : morph de retour (cartes rentrées dans L5 / le compte rendu, L5 « Vendre ? » + « Hypothèse »), repère sur 4 ;
  « Toi » se place à droite du brief (TOI_S15), lève le stylo en DIAG_A, file en diagonale jusqu'à DIAG_B (traînée),
  reflet, puis coche hâtive sur L1 (la coche de l'IA est chassée).
- S16 : la coche hâtive tombe ; « Toi » remonte à hauteur de L1 (TOI_L1), relit lentement « 120 000 € » ; la copie
  « 12 000 € » sort de la carte Relevé, longe le fil 1 et se pose dessous ; le zéro de trop se cercle de rouge, L1
  rougit. « Toi » descend (TOI_L34) : « mars 2027 », « Me Roux » (coche pleine, fil 3 qui bat), « 250 000 € » se
  surlignent sous la pointe ; les surlignés s'effacent et « Toi » remonte à hauteur de L1.
- S17 : barre et chute de « 120 000 € » (et du cercle) ; « 12 000 € » monte à sa place, coche pleine de L1 ; rangement
  (cartes -> puces de L1 / L3 / L5, dossier, places, maison et fils repliés, IA dans le coin) ; brief à gauche,
  pilule « Parade ».
- S18 : la pilule s'étire en bandeau, la rallonge sort ; le cadre de la rubrique se trace ; le titre s'écrit.
- S19 : L2, L4, L5 descendent dans la rubrique, L3 remonte ; la rubrique remonte sous les faits ; « Toi » s'approche et
  sa pointe descend la colonne des coches : « mars 2027 » et « 250 000 € » tombent au sol, « Hypothèse » rentre ;
  questions et cases vides ; « Toi » redescend ; le client arrive, la pastille vole au-dessus de lui.
- S20 : la case bat ; la question se surligne ; au sol, « mars 2027 » tremble et bat.
- S21 : « Toi » se penche, la question vole dans sa bulle ; le client se penche, « sept. 2028 » surgit, vole dans la
  ligne qui devient « Vente : sept. 2028 », la case se remplit de cyan, la bulle rentre ; les valeurs au sol tombent et
  s'effacent ; tenue immobile 1,6 s.
- S22 : kit.outro (clear="fade") : la pastille devient « S’abonner », vole et grandit jusqu'au bouton (btn_at) ; le
  client sort ; « Toi » passe au-dessus de la carte (calque) et touche le bouton du stylo sur « argent. » : presse et
  deux ondes ; pas de pointeur ; immobile jusqu'à 2684.
"""
import math

from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, STRETCH, STYLE, TILT, line_crack_point, text_width  # noqa: F401
from pipeline.story_kit import REACH, TAP

from . import (AI_TICK, BANDEAU_H, BANDEAU_S18, BANDEAU_S19, BANDEAU_W, BULLE_C, CADRE_RUB_S18, CADRE_RUB_S19,  # noqa: F401
               CLIENT_C, COPIE_C, CYAN, DEEP, DIAG_A, DIAG_B, DOSSIER_C, ENTRY_P3, FICHE_C, FICHE_S, FICHE_S17,
               FIN_TAP, IA_S17, IA_S17_S, LINES, LOUPE_C, PARADE_S17, PASTILLE_CLIENT, PASTILLE_CLIENT_S, PILL_H,
               PILL_SIZE, PILL_W, Q_PT, QUESTIONS, RALLONGE_IN, RALLONGE_OUT, REP_W, REPONSE_C, REPONSE_UP, ROWS,
               RUBRIQUE_LINES_Y, SOL_CONTRAT, SOL_VENTE, T_12, T_REPONSE_L2, T_VENDRE_Q, TEXT_MIN, TICK_PT, TOI_REST,
               TOI_S13, TOI_S19, TOI_S19_REST, TY, VALUE_PT, VALUE_W, X, ZERO_PT, fig_pos, ring, seam, vanish)

L_KEY = [len(k) for k, _, _ in LINES]
TOI_S15 = [850, 630]          # S15 : à droite du brief, DIAG_A, DIAG_B et la coche de L1 à portée
TOI_L1 = [820, 600]           # S16-S17 : sous l'en-tête, L1 à portée (relecture de « 120 000 € », coche de L1)
TOI_L34 = [820, 728]          # S16 : épaule à hauteur de L3 (L2, L3, L4 à portée)
UNDER = 17                    # S16 : la pointe souligne à 17 px sous la ligne de texte (repère de la ligne)
RUB18_Y = [1126, 1168, 1210]  # S19 « Tout » : lignes de texte (monde) des 3 lignes dans la rubrique S18 (sous le bandeau)
RUB18_S = 0.8                 # … à l'échelle 0,8 (la rubrique S18 fait 228 px de haut)
BTN_K = 112 / PILL_H          # S22 : la pastille (h 60) grandit jusqu'au bouton de la carte (h 112)
BTN_C = (540, 908)            # centre du bouton de kit.outro (pos (540, 760), h 520, bh 112)
BTN_AT = FADE + MOVE          # relais pastille -> bouton (images après « Abonne-toi »)
FLOOR = 1250                  # sol (y monde) : la coche hâtive y tombe
# S19-S22 : le client à droite du brief (bord 618) ; sa pastille x 0,85 au-dessus de sa tête, bord gauche >= 634
CLIENT_P3 = list(CLIENT_C)
PASTILLE_P3, PASTILLE_P3_S = (PASTILLE_CLIENT[0], PASTILLE_CLIENT[1]), PASTILLE_CLIENT_S
REPONSE_P3 = tuple(REPONSE_C)                       # sa réponse surgit devant lui, puis monte dans la colonne libre
# S19-S21 : valeurs au sol (centre de la valeur, inclinaison) : loin de l'IA réduite, au-dessus de la bande des
# sous-titres
SOL_P3 = {"sol_vente": ((300, 1173), 8), "sol_contrat": ((535, 1170), -7)}
INK, PAPER, RED, LIGHT = STYLE["ink"], STYLE["paper"], STYLE["red"], STYLE["light"]


def part(S, kit, c):
    toi, client = c.toi, c.client
    f0 = seam(S, "S15") + 1
    kit.pin(f0 - 1, ENTRY_P3)
    if S.val("toi", "scale", f0 - 1) == 0:      # partie construite seule : « Toi » n'est pas entré
        toi.enter(f0 - 10, at=list(TOI_S13))

    # éléments propres à cette partie (déclarés ici, effacés avant la fin)
    for k, off in enumerate((-30, 26, 52)):      # S15 : traits de vitesse de part et d'autre de la pointe
        n = [0.92, -0.39]                         # normale à la diagonale DIAG_A -> DIAG_B
        a = [DIAG_A[0] + n[0] * off, DIAG_A[1] + n[1] * off]
        b = [DIAG_B[0] + n[0] * off, DIAG_B[1] + n[1] * off]
        kit.shape(f"p3_vitesse{k}", [0, 0], kind="poly", pts=[a, b], closed=False, fill="none", stroke=DEEP, sw=4,
                  shadow=0, z=16.3, draw=0)
    S.add("p3_anneau", "shape", z=9.7, parent="L2", kind="circle", w=round(REP_W * 1.9), fill="none", stroke=DEEP,
          sw=5, shadow=0)                        # S20 : anneau plein autour de la case vide gardée
    S.set("p3_anneau", pos=list(TICK_PT), scale=1, opacity=1, draw=0)
    qw = text_width(QUESTIONS[0], 32, 700)
    kit.shape("p3_question", [0, 0], kind="round", w=round(qw + 28), h=50, r=25, fill=PAPER, stroke=INK, sw=3,
              shadow=3, z=22, scale=0)            # S21 : la question vole sur une pastille papier
    kit.text("p3_question_txt", [0, 1], QUESTIONS[0], size=32, weight=700, z=22.1, parent="p3_question")

    def W(id, pt, n):
        return S.to_world(id, list(pt), n)

    def lp(lid):
        return S.ents[lid]["p"]

    def crack_pt(lid, pt):
        """Point local `pt` de la partie droite (valeur) d'une ligne fissurée (crack 1)."""
        return line_crack_point(lp(lid), pt, 1.0)

    def sh_at(body):
        """Épaule monde de « Toi » si son centre est en `body` (penché 0)."""
        s = S.world_scale("toi", f0)
        return [body[0] + toi.shoulder[0] * s, body[1] + toi.shoulder[1] * s]

    def reach_r():
        return 0.97 * REACH * toi.reach_max(f0)

    def x_min(body, y):
        """x monde le plus à gauche que la pointe atteint, depuis `body`, à la hauteur y (portée confortable)."""
        a = sh_at(body)
        dy = y - a[1]
        return a[0] - math.sqrt(max(0.0, reach_r() ** 2 - dy * dy))

    def check_reach(body, pts, what):
        a = sh_at(body)
        for q in pts:
            assert math.dist(a, q) <= REACH * toi.reach_max(f0), (what, body, q, math.dist(a, q))

    def sweep(sid, f, d, rot=0.0, center=None):
        """Surligneur (shape) tiré de gauche à droite en d images : largeur 16 -> pleine, centre glissé d'autant."""
        p = S.ents[sid]["p"]
        full = p["w"]
        cx, cy = center if center is not None else S.val(sid, "pos", f - 1)
        u = (math.cos(math.radians(rot)), math.sin(math.radians(rot)))
        k0 = -(full - 16) / 2
        kit.ensure(sid, "w", full)
        S.key(sid, "rot", f - 1, rot)
        S.key(sid, "w", f - 1, 16)
        S.key(sid, "pos", f - 1, [round(cx + u[0] * k0, 2), round(cy + u[1] * k0, 2)])
        S.key(sid, "scale", f - 1, 1)
        S.key(sid, "opacity", f - 1, 0)
        S.key(sid, "opacity", f, 1)
        S.key(sid, "w", f, full, d, "out")
        S.key(sid, "pos", f, [round(cx, 2), round(cy, 2)], d, "out")
        return f + d

    def fade_out(id, f, d=6):
        """Sortie en opacité (d images) puis échelle 0 : pas de bouillie de formes pendant un morph."""
        S.key(id, "opacity", f, 0, d, "linear")
        S.key(id, "scale", f + d, 0)
        S.key(id, "opacity", f + d + 1, 1)

    # ======================= S15 : 4 · Diagonale ; relire en survolant ; coche trop rapide =======================
    f = kit.at("S15", "Quatrième", "le repère passe sur 4 « Diagonale » ; les cartes et le « ≠ » s'effacent, puis "
                                   "brief et dossier reprennent leur taille et leur place ; L5 s'écrit « Vendre ? », "
                                   "soulignée en tirets, et la pilule « Hypothèse » surgit sur place ; les fils "
                                   "reviennent")
    kit.step(f, 3)
    for k, cid in enumerate(("carteA", "carteB", "different", "hypothese")):
        fade_out(cid, f + (k % 2))
    g = f + 4
    kit.move("fiche", g, list(FICHE_C), MORPH, "out", scale=FICHE_S)
    kit.move("dossier", g, list(DOSSIER_C), MORPH, "out", scale=1)
    for lid in ("L2", "L4"):
        S.key(lid, "red", g, 1, MORPH, "out")
    for k in (1, 3, 5):
        kit.draw(f"fil{k}", g + MORPH, 6)
    kit.pop("L5_hyp", g + MORPH)
    kit.type("L5_vendre", g + 3, rate=2)
    kit.fade("L5_tirets", g + 8, to=1, d=8)
    toi.walk(f + 2, list(TOI_S15))
    check_reach(TOI_S15, [DIAG_A, DIAG_B], "S15 diagonale")

    f = kit.at("S15", "relire", "« Toi » lève le stylo et en porte la pointe en haut de la colonne des valeurs")
    toi.reach(f, list(DIAG_A), d=9)

    f = kit.at("S15", "diagonale.", "la pointe file d'un trait en diagonale jusqu'en bas du brief, très vite, trois "
                                    "traits de vitesse derrière elle ; elle ne touche aucune valeur")
    toi.trace(f, [list(DIAG_A), list(DIAG_B)], d=7, step=False)
    kit.draw("trainee", f, 7, e="linear")
    S.key("trainee", "opacity", f + 7, 0, FADE, "linear")
    for k in range(3):
        kit.draw(f"p3_vitesse{k}", f + 1 + k % 2, 6, e="linear")
        kit.draw(f"p3_vitesse{k}", f + 3 + k % 2, 6, track="from", e="linear")
        S.key(f"p3_vitesse{k}", "opacity", f + 11 + k, 0)
    toi.rest(f + 8, 8)

    f = kit.at("S15", "bien", "les coches pointillées de l'IA battent ensemble : tout a l'air vérifié")
    for i in range(5):
        kit.pulse(f"coche_ia{i + 1}", f + i, peak=1.25, step=3)

    m = kit.at("S15", "confiance.", "« Toi » plaque d'un geste une grosse coche pleine, de travers, qui déborde de L1 "
                                     "à côté de « 120 000 € » et chasse la coche pointillée de l'IA ; la pointe repart "
                                     "aussitôt")
    tick1 = W("L1", TICK_PT, m - TAP)
    check_reach(TOI_S15, [tick1], "S15 coche")
    hit = toi.tap(m - TAP + 1, tick1)
    kit.draw("coche_hate", hit, 3, e="linear")
    kit.drop("coche_ia1", hit, out=True, h=52, dx=18, rot=35)
    toi.rest(hit + 4, 6)

    # ======================= S16 : ralentir ; 12 000 € sous 120 000 € ; dates, noms, montants ======================
    f = kit.at("S16", "C’est", "la pointe tapote la coche trop rapide : elle bascule et tombe jusqu'au sol ; « Toi » "
                               "remonte à hauteur de L1")
    tick_w = W("coche_hate", [0, 0], f - TAP)
    hit = toi.tap(f - TAP + 1, [round(tick_w[0] + 6, 2), round(tick_w[1] - 4, 2)])
    p0 = S.val("coche_hate", "pos", hit)
    land = S.parent_space("coche_hate", [tick_w[0] + 40, FLOOR], hit)
    S.key("coche_hate", "rot", hit + 1, S.val("coche_hate", "rot", hit) + 90, 14, "in")
    S.key("coche_hate", "pos", hit + 1, [round(land[0], 2), round(land[1], 2)], 14, "in")
    S.key("coche_hate", "opacity", hit + 16, 0, 5, "linear")
    S.key("coche_hate", "draw", hit + 21, 0)
    S.key("coche_hate", "pos", hit + 21, p0)
    toi.walk(hit + 3, list(TOI_L1), d=10)

    y1 = W("L1", [0, TY + UNDER], f)[1]
    l1_left = W("L1", [X["value"] - VALUE_W[0], TY], f)[0]
    l1_right = W("L1", [X["value"], TY], f)[0]
    p_start = [round(max(l1_left + 4, x_min(TOI_L1, y1) + 2), 1), round(y1, 1)]
    p_end = [round(l1_right + 2, 1), round(y1, 1)]
    check_reach(TOI_L1, [p_start, p_end, tick1], "S16 L1")

    f = kit.at("S16", "ralentir :", "la pointe revient lentement sous le début de « 120 000 € »")
    toi.reach(f, p_start, d=MOVE)

    f = kit.at("S16", "chiffres,", "la pointe souligne lentement « 120 000 € » ; une copie de « 12 000 € » sort de la "
                                   "carte Relevé sur une pastille, longe le fil au-dessus de lui et se pose juste "
                                   "dessous ; dans le bas de l'image, une loupe aligne « 120 000 € » sur « 12 000 € » "
                                   "chiffre à chiffre ; le zéro en trop se cercle de rouge, L1 vire au rouge")
    toi.trace(f, [p_start, p_end], d=12, step=False)
    val0 = W("doc_releve_val", [text_width(T_12, 32, 700) / 2, 0], f - 1)
    S.key("copie_releve", "pos", f - 1, S.parent_space("copie_releve", val0, f - 1))
    kit.pop("copie_releve", f, d=3)
    wire = S.wire_cubic("fil1", f)
    lift = 26                                                           # la pastille passe AU-DESSUS du fil
    S.fly("copie_releve", f + 3, 2, "inOut", to=[wire[3][0], wire[3][1] - lift])
    S.along_wire("copie_releve", "fil1", f + 5, 4, "linear", 1, 0, f + 5, offset=(0, -lift))
    S.fly("copie_releve", f + 9, 4, "out", to=W("L1", COPIE_C, f + 9))
    g = f + 13                                                          # la copie est posée
    kit.draw("cercle_zero", g, 4)
    S.key("L1", "red", g, 1, 3, "out")
    kit.pop("loupe", f + 6, from_pt=W("L1", VALUE_PT[0], f + 5), to=list(LOUPE_C), d=7)
    kit.draw("loupe_zero", g, 4)

    # TOI_L34 : L2, L3, L4 à portée
    f = kit.at("S16", "dates,", "« Toi » descend ; sa pointe souligne « mars 2027 » (fissurée), qui se surligne")
    toi.walk(f, list(TOI_L34), d=5)
    g = f + 5
    sl = {}
    for lid in ("L2", "L3", "L4"):
        sl[lid] = S.val(lid, "slotFill", g - 1, 1)
    c2 = crack_pt("L2", VALUE_PT[1])
    tilt = lp("L2")["tilt"]
    a2 = W("L2", crack_pt("L2", [X["value"] - VALUE_W[1] + 8, TY + UNDER]), g)
    b2 = W("L2", crack_pt("L2", [X["value"] + 2, TY + UNDER]), g)
    a2 = [max(a2[0], x_min(TOI_L34, a2[1]) + 2), a2[1] + (max(a2[0], x_min(TOI_L34, a2[1]) + 2) - a2[0]) *
          math.tan(math.radians(tilt))]
    check_reach(TOI_L34, [a2, b2], "S16 L2")
    toi.trace(g, [a2, b2], d=8, lead=2, step=False)
    kit.ensure("L2", "slotFill", 1)
    S.key("L2", "slotFill", g + 2, 0, 4, "out")
    sweep("L2_surligne", g + 2, 8, rot=tilt, center=c2)

    f = kit.at("S16", "noms,", "la pointe souligne « Me Roux », qui se surligne ; le fil vers la carte Mail bat ; "
                               "la coche pleine de « Toi » se trace au bout de L3 et chasse celle de l'IA")
    y3 = W("L3", [0, TY + UNDER], f)[1]
    a3 = [max(W("L3", [X["value"] - VALUE_W[2], TY], f)[0] + 4, x_min(TOI_L34, y3) + 2), y3]
    b3 = [W("L3", [X["value"] + 2, TY], f)[0], y3]
    t3 = W("L3", TICK_PT, f)
    check_reach(TOI_L34, [a3, b3, t3], "S16 L3")
    hits = toi.trace(f, [a3, b3, t3], d=9, lead=4, step=False)
    kit.ensure("L3", "slotFill", 1)
    S.key("L3", "slotFill", hits[0] + 1, 0, 4, "out")
    sweep("L3_surligne", hits[0] + 1, hits[1] - hits[0])
    S.key("fil3_halo", "opacity", hits[0] + 1, 1, 3, "out")
    S.key("fil3_halo", "opacity", hits[0] + 4, 0, 4, "inOut")
    kit.draw("coche3", hits[2], 5)
    kit.drop("coche_ia3", hits[2], out=True, h=52, dx=18, rot=35)

    f = kit.at("S16", "montants.", "la pointe descend sous « 250 000 € » (fissurée), qui se surligne")
    tilt4 = lp("L4")["tilt"]
    a4 = W("L4", crack_pt("L4", [X["value"] - VALUE_W[3] + 8, TY + UNDER]), f)
    b4 = W("L4", crack_pt("L4", [X["value"] + 2, TY + UNDER]), f)
    xa = max(a4[0], x_min(TOI_L34, a4[1]) + 2)
    a4 = [xa, a4[1] + (xa - a4[0]) * math.tan(math.radians(tilt4))]
    check_reach(TOI_L34, [a4, b4], "S16 L4")
    toi.trace(f, [a4, b4], d=8, lead=4, step=False)
    kit.ensure("L4", "slotFill", 1)
    S.key("L4", "slotFill", f + 4, 0, 4, "out")
    sweep("L4_surligne", f + 4, 8, rot=tilt4, center=crack_pt("L4", VALUE_PT[3]))
    # fin de S16 : les surlignés s'effacent, les bandes beiges reviennent ; « Toi » remonte à hauteur de L1
    e = f + 16
    for lid in ("L2", "L3", "L4"):
        kit.fade(f"{lid}_surligne", e, to=0)
        S.key(lid, "slotFill", e + 2, sl[lid], FADE, "out")
    toi.walk(e, list(TOI_L1), d=12)

    # ======================= S17 : corriger depuis la source ; ranger ; la parade =======================
    f = kit.at("S17", "Comment", "« Toi » barre « 120 000 € » ; la valeur barrée s'enfonce un peu et s'efface sur "
                                 "place avec son cercle rouge ; la loupe rentre dans L1 ; « 12 000 € » reste dessous")
    lp("L1")["fallPx"] = 14                                         # la valeur barrée s'efface sur place
    ra, la = (W("fiche", q, f - 1) for q in c.sheet.value_span(0))   # repère de la fiche
    end = toi.strike(f, ra, la, line="L1", lead=3)
    kit.ensure("L1", "fall", 0)
    S.key("L1", "fall", end, 1, DROP, "in")
    kit.drop("cercle_zero", end, out=True, h=14, rot=0)
    vanish(kit, "loupe", f + 2)

    f = kit.at("S17", "tout", "le fil du relevé s'allume et la carte Relevé bat pendant que « 12 000 € » monte à la "
                              "place de la valeur de L1 ; sa pastille s'efface, L1 redevient encre ; « Toi » coche L1")
    tw = text_width(T_12, 32, 700)
    kit.move("copie_releve", f, [round(X["value"] - tw / 2, 1), TY], 10, "inOut")
    S.key("copie_releve", "draw", f + 6, 0, 5, "linear")
    kit.ensure("copie_releve", "fillOp", 1)
    S.key("copie_releve", "fillOp", f + 6, 0, 5, "linear")
    S.key("L1", "red", f, 0, 6, "out")
    S.key("fil1_halo", "opacity", f, 1, 3, "out")
    S.key("fil1_halo", "opacity", f + 14, 0, 6, "inOut")
    kit.pulse("doc_releve", f, times=2, peak=1.12, step=3)
    toi.walk(f, list(TOI_L1), d=8)
    tick1 = W("L1", TICK_PT, f)
    hit = toi.tap(f + 6, tick1)
    kit.draw("coche1", hit, 5)
    toi.rest(hit + 6, 8)

    f = kit.at("S17", "Avec", "tout se range : le dossier se réduit et s'efface d'un bloc, ses fils se replient ; les "
                              "pictogrammes des sources restent au début de L1, L3 et L5 ; l'IA se range, réduite, "
                              "dans le coin bas gauche")
    S.key("dossier", "scale", f, 0.5, MORPH, "in")
    S.key("dossier", "opacity", f, 0, MORPH, "linear")
    for k in (1, 3, 5):
        S.key(f"fil{k}", "from", f, 1, MORPH, "out")
        S.key(f"fil{k}", "draw", f + MORPH + 2, 0)
        S.key(f"fil{k}", "from", f + MORPH + 2, 0)
    for lid in ("L1", "L3", "L5"):
        kit.ensure(lid, "flash", 0)
        S.key(lid, "flash", f + 4, 1, 3, "out")
        S.key(lid, "flash", f + 7, 0, 4, "inOut")
    kit.move("ia", f, list(IA_S17), MORPH + 4, "inOut", scale=IA_S17_S)
    S.key("ia_pill", "scale", f, round(1 / IA_S17_S, 4), MORPH + 4, "inOut")     # la pilule « IA » garde sa taille

    f = kit.at("S17", "parade", "le brief glisse à gauche ; la pilule « Parade » au bouclier ressurgit dans sa marge "
                                "basse ; « Toi » redescend au repos, en bas à droite")
    kit.move("fiche", f, list(FICHE_S17), MOVE)
    S.key("parade", "pos", f - 1, list(PARADE_S17))
    kit.pop("parade", f + 6)
    toi.walk(f + 4, list(TOI_REST), d=14)

    # ======================= S18 : la rubrique « Informations non confirmées » =======================
    f = kit.at("S18", "Ajoute", "la pilule « Parade » s'étire en bandeau, bouclier et mot compris ; une rallonge de "
                                "page sort sous le brief")
    S.keys("parade", f, 8, "inOut", w=BANDEAU_W, h=BANDEAU_H, r=20, pos=list(BANDEAU_S18))
    S.key("parade", "stroke", f, DEEP, 8, "inOut")
    kit.move("parade_ico", f, [-BANDEAU_W / 2 + 34, 0], 8)
    S.key("rallonge", "scale", f - 1, 1)
    S.key("rallonge", "pos", f, list(RALLONGE_OUT), 10, "out")

    f = kit.at("S18", "rubrique", "un cadre cyan foncé se trace autour de l'espace vide de la rallonge : une rubrique")
    kit.draw("rubrique_cadre", f, 10)

    f = kit.at("S18", "« Informations", "le mot « Parade » s'efface et le titre s'écrit dans le bandeau : "
                                        "« Informations non confirmées »")
    kit.fade("parade_txt", f, to=0, d=4)
    kit.type("rubrique_titre", f + 1, rate=3.5)

    # ======================= S19 : tout ce qui manque devient une question ; le client =======================
    f = kit.at("S19", "Tout", "L2, L4 et L5 quittent le haut du brief et descendent dans la rubrique, une à une ; L3 "
                              "remonte sous L1")
    fx = S.val("fiche", "pos", f)[0]
    for k, (lid, y) in enumerate(zip(("L2", "L4", "L5"), RUB18_Y)):
        loc = S.to_local("fiche", [fx, y - TY * 0.95 * RUB18_S], f)
        kit.move(lid, f + 4 * k, [0, round(loc[1], 2)], MOVE, scale=RUB18_S)
    kit.move("L3", f + 8, [0, ROWS[1]], MOVE)

    f = kit.at("S19", "va,", "la rubrique remonte sous les faits et la page reprend sa taille ; « Toi » s'approche "
                             "de la rubrique")
    (c19, w19, h19) = CADRE_RUB_S19
    kit.move("parade", f, list(BANDEAU_S19), MOVE)
    S.keys("rubrique_cadre", f, MOVE, "inOut", pos=list(c19), w=w19, h=h19)
    kit.move("rallonge", f, list(RALLONGE_IN), MOVE)
    S.key("rallonge", "scale", f + MOVE, 0)
    for lid, y in zip(("L2", "L4", "L5"), RUBRIQUE_LINES_Y):
        loc = S.to_local("fiche", [fx, y - TY * 0.95], f)
        kit.move(lid, f, [0, round(loc[1], 2)], MOVE, scale=1)
    # place de « Toi » : la colonne des coches de la rubrique à portée (y de TOI_S19)
    col = [[fx + X["tick"] * 0.95, y] for y in RUBRIQUE_LINES_Y]
    lo, hi = -math.inf, math.inf
    for q in col:
        a = sh_at([0, TOI_S19[1]])
        dy = q[1] - a[1]
        w = math.sqrt(reach_r() ** 2 - dy * dy)
        lo, hi = max(lo, q[0] - w - (a[0])), min(hi, q[0] + w - a[0])
    toi19 = [round(min(max(TOI_S19[0], lo), hi), 1), TOI_S19[1]]
    check_reach(toi19, col, "S19 rubrique")
    toi.walk(f + 2, toi19, d=16)

    f = kit.at("S19", "forme", "la pointe descend la colonne des trois lignes : sous elle, « mars 2027 » et "
                               "« 250 000 € » quittent leurs lignes et tombent, visibles tout du long, sur le sol sous "
                               "le brief, rouges et fissurés ; la pilule « Hypothèse » rentre dans L5")
    hits = toi.trace(f, col, d=9, lead=3, step=False)
    for sid in ("sol_vente", "sol_contrat"):          # au sol : seule la partie droite (la valeur) reste visible ; la
        sp = lp(sid)                                    # capsule vide de la clé (x0 -> crackX) dessinait un cadre rouge
        sp["x0"] = sp["crackX"]                         # jusqu'au bord gauche de l'image (paramètre propre à p3)
        sp["x1"] = round(sp["valueX"] + 16, 1)          # capsule serrée sur la valeur
    for (lid, i, sid), h in zip((("L2", 1, "sol_vente"), ("L4", 3, "sol_contrat")), hits[:2]):
        goal, rot1 = SOL_P3[sid]
        vp = lp(sid)
        vc = [X["value"] - vp["valueW"] / 2, TY]                 # centre de la valeur (repère de la ligne au sol)
        src = W(lid, crack_pt(lid, VALUE_PT[i]), h - 1)
        s0 = S.world_scale(lid, h - 1)
        r0 = lp(lid)["tilt"]

        def origin(center, s, rot):
            t = math.radians(rot)
            return [round(center[0] - s * (vc[0] * math.cos(t) - vc[1] * math.sin(t)), 2),
                    round(center[1] - s * (vc[0] * math.sin(t) + vc[1] * math.cos(t)), 2)]
        S.key(sid, "pos", h - 1, origin(src, s0, r0))
        S.key(sid, "scale", h - 1, round(s0, 4))
        S.key(sid, "rot", h - 1, r0)
        S.key(sid, "pos", h, origin(goal, 1, rot1), DROP, "in")
        S.key(sid, "scale", h, 1, DROP, "in")
        S.key(sid, "rot", h, rot1, DROP, "in")
        S.key(lid, "chars", h, L_KEY[i])
        S.key(lid, "crack", h, 0)
        S.key(lid, "red", h, 0, 4, "out")
    vanish(kit, "L5_hyp", hits[2], d=POP)
    S.key("L5_tirets", "opacity", hits[2], 0, 4, "linear")

    f = kit.at("S19", "question", "les trois lignes se réécrivent « Date de vente ? », « Montant du contrat ? », "
                                  "« Projet de vente ? » ; au bout de chacune surgit une case réponse vide ; les "
                                  "coches de l'IA disparaissent")
    for lid in ("L2", "L4"):
        S.key(lid, "chars", f, 0, 2, "linear")
    S.key("L5_vendre", "chars", f, 0, 2, "linear")
    for k, lid in enumerate(("L2", "L4", "L5")):
        kit.type(f"{lid}_q", f + 2, rate=4)
        kit.vanish(f"coche_ia{lid[1]}", f, d=6)
        kit.pop(f"{lid}_rep", f + 3 + 2 * k)
    toi.rest(f + 2, 8)

    f = kit.at("S19", "poser", "« Toi » redescend au repos, en bas à droite")
    toi.walk(f, list(TOI_S19_REST), d=12)

    f = kit.at("S19", "client.", "le client apparaît face à « Toi » et se penche vers lui ; la pastille « Client · "
                                 "10 h » quitte l'en-tête du brief et vient se poser au-dessus de sa tête")
    client.enter(f, at=list(CLIENT_P3))
    client.lean_to(f + POP, 5, d=POP)
    pw = W("pastille", [0, 0], f - 1)
    S.key("pastille_client", "pos", f - 1, [round(pw[0], 2), round(pw[1], 2)])
    S.key("pastille_client", "scale", f - 1, round(S.world_scale("pastille", f - 1), 4))
    S.key("pastille_client", "opacity", f, 1)
    S.key("pastille", "opacity", f, 0)
    kit.move("pastille_client", f + 1, list(PASTILLE_P3), MOVE, scale=PASTILLE_P3_S)

    # ======================= S20 : une case vide vaut mieux qu'un fait fabriqué =======================
    f = kit.at("S20", "case", "la case vide de « Date de vente ? » grossit et bat ; un anneau plein cyan foncé se "
                              "trace autour d'elle : elle est gardée vide")
    kit.pulse("L2_rep", f, times=2, peak=1.3, step=3)
    kit.draw("p3_anneau", f, 9)

    f = kit.at("S20", "mieux", "« Date de vente ? » se surligne en bleu clair et se souligne d'un trait plein : la "
                               "question est gardée")
    kit.ensure("L2", "slotFill", 1)
    S.key("L2", "slotFill", f, 0, 4, "out")
    kit.draw("L2_q", f, 9, track="mark")
    kit.draw("L2_q", f + 3, 9, track="under")

    f = kit.at("S20", "fabriqué.", "au sol, « mars 2027 » se soulève vers la case gardée, tremble et bat en rouge, "
                                   "puis retombe : la valeur fabriquée ne prend pas la place")
    p0 = S.val("sol_vente", "pos", f - 1)
    S.key("sol_vente", "pos", f, [p0[0], p0[1] - 30], 6, "out")
    for k, dx in enumerate([10, -8, 6, -4, 0]):
        S.key("sol_vente", "pos", f + 6 + k, [p0[0] + dx, p0[1] - 30])
    kit.pulse("sol_vente", f + 3, peak=1.2, step=4)
    S.key("sol_vente", "pos", f + 12, p0, 8, "in")

    # ======================= S21 : le client répond « sept. 2028 » ; les valeurs inventées disparaissent ===========
    f = kit.at("S21", "client", "« Toi » se penche vers le client ; une bulle grandit dans la colonne libre au-dessus "
                                "de lui et « Date de vente ? », sur une pastille, quitte la rubrique par la droite pour "
                                "y entrer : c'est lui qui demande")
    toi.lean_to(f, -5, d=POP)
    kit.pop("bulle", f)
    S.key("bulle_txt", "opacity", f - 1, 0)
    q0 = W("L2_q", [qw / 2 + 8, -6], f - 1)                         # décalée : ne double pas la question
    S.key("p3_question", "pos", f, [round(q0[0], 2), round(q0[1], 2)])
    kit.pop("p3_question", f + 1, d=3)
    out_x = 700
    pts = [q0, [out_x, q0[1]], [out_x, BULLE_C[1] + 70], list(BULLE_C)]

    def route(p):
        """Polyligne q0 -> à droite du brief -> en haut -> la bulle (longueur parcourue proportionnelle à p)."""
        seg = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
        t = p * sum(seg)
        for (a, b), L in zip(zip(pts, pts[1:]), seg):
            if t <= L or L == seg[-1] and b == pts[-1]:
                u = min(1.0, t / L) if L else 1.0
                return [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u]
            t -= L
        return list(pts[-1])
    S.path("p3_question", f + 4, MOVE, "inOut", route)
    arr = f + 4 + MOVE
    S.key("p3_question", "scale", arr, 0)                            # coupe : la bulle prend la question
    S.key("bulle_txt", "opacity", arr, 1)

    f = kit.at("S21", "pardonnera", "le client se penche vers « Toi » ; sa réponse surgit devant lui et monte dans la "
                                    "colonne libre : « sept. 2028 »")
    client.lean_to(f, 6, d=TILT)
    S.key("reponse", "pos", f - 1, list(REPONSE_P3))
    kit.pop("reponse", f)
    kit.move("reponse", f + 4, list(REPONSE_UP), 10, "out")

    f = kit.at("S21", "question,", "la réponse vole jusqu'à la question et s'y fond : la ligne devient « Vente : sept. "
                                   "2028 » et sa case se remplit de cyan ; la bulle rentre dans « Toi »")
    tgt = W("L2_q", [qw / 2, 0], f)
    S.fly("reponse", f, MOVE, "inOut", to=tgt, scale=0.8, arc=40)
    arr = f + MOVE
    S.key("reponse", "scale", arr, 0, 3, "in")
    S.key("reponse", "opacity", arr + 3, 0)
    S.key("L2_q", "text", arr, T_REPONSE_L2)
    S.key("L2_q", "chars", arr, len(T_REPONSE_L2))
    S.key("L2_q", "mark", arr, 0, FADE, "out")
    S.key("L2_q", "under", arr, 0, FADE, "out")
    S.key("L2", "slotFill", arr, 1, FADE, "out")
    S.key("L2_rep", "fill", arr, CYAN, 6, "out")
    kit.pulse("L2_rep", arr, peak=1.15, step=3)
    S.key("p3_anneau", "opacity", arr + 6, 0, FADE, "linear")
    head = W("toi", [0, -64], f + 4 + POP)
    vanish(kit, "bulle", f + 4, into=head, d=POP)
    toi.lean_to(f + 6, 0, d=POP)
    client.lean_to(arr, 0, d=POP)

    f = kit.at("S21", "pas", "« mars 2027 » et « 250 000 € » tombent du sol et s'effacent ; puis plus rien ne bouge")
    kit.drop("sol_vente", f, out=True, h=70, dx=-10, rot=-10)
    kit.drop("sol_contrat", f + 2, out=True, h=70, dx=10, rot=10)

    # ======================= S22 : fin standard ; le bouton touché du stylo =======================
    outs = ["fiche", "parade", "rubrique_cadre", "ia", "marqueur", "titre_erreurs"]
    out = kit.outro("S22", outs=(), press="argent.", clear="fade", btn_at=BTN_AT, bsize=round(PILL_SIZE * BTN_K, 1))
    S.set(out["cursor"], opacity=0)                             # pas de pointeur de souris : le stylo de « Toi »
    f, fp = out["card"], out["press"]
    for k, o in enumerate(outs):                                # sortie en points, un à un (2 images d'écart)
        vanish(kit, o, f + 2 * k, d=POP)
    for bt in S.beats:
        if bt["scene"] == "S22" and bt["frame"] == f:
            bt["what"] = ("le brief, l'IA et le repère se réduisent en points un à un, la carte de fin surgit ; le "
                          "client sort ; sa pastille devient « S’abonner », vole au bas de la carte et grandit : "
                          "c'est son bouton ; « Toi » reste sous la carte")
        elif bt["scene"] == "S22" and bt["frame"] == fp:
            bt["what"] = ("le stylo de « Toi » touche le coin bas droit du bouton « S’abonner » : il s'enfonce, deux "
                          "ondes partent du point touché ; puis plus rien ne bouge")
    client.exit(f)
    pc = S.val("pastille_client", "pos", f - 1)
    S.key("pastille_btn", "pos", f - 1, list(pc))
    S.key("pastille_btn", "scale", f - 1, S.val("pastille_client", "scale", f - 1))
    S.key("pastille_client", "opacity", f, 0, FADE, "linear")
    S.key("pastille_btn", "opacity", f, 1, FADE, "linear")
    kit.ensure("pastille_btn", "w", PILL_W)
    kit.move("pastille_btn", f + FADE, list(BTN_C), MOVE, scale=round(BTN_K, 4))
    S.key("pastille_btn", "w", f + FADE, round(380 / BTN_K, 1), MOVE, "inOut")
    S.key("pastille_btn", "opacity", f + BTN_AT, 0)
    S.key("pastille_client", "scale", f + FADE, 0)
    toi.set_z(f, 42, tool_z=42.5)
    spot = toi.place_for([list(FIN_TAP)], f - 1)
    toi.walk(f + 4, spot, d=8)
    hit = toi.tap(fp - TAP + 1, list(FIN_TAP))
    assert hit == fp, (hit, fp)
    for k in range(2):
        S.key(f"fin_onde{k + 1}", "pos", hit - 1, list(FIN_TAP))
    ring(S, "fin_onde1", hit, d=18)
    last = ring(S, "fin_onde2", hit + 4, d=18)
    n_frames = math.ceil(S.sb["scenes"][-1]["t_end"] * S.fps)    # longueur du film (fin de la dernière scène)
    assert last < n_frames, (last, n_frames)
