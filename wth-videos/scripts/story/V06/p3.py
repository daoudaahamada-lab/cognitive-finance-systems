"""V06, partie 3 : S15-S22, images 1767-2680 (fin du point 2, point 3, chute, fin). 33 temps forts, 30,4 s.

ÉTAT D'ENTRÉE (etat_initial de S15, kit.pin(1766, ENTRY_P3)) : trois pièces de tailles différentes (x1,5, x0,6, x1)
dans la caisse ; sur la scène, les actions (400, 880) avec « Actions, fonds », « vite » et la courbe ; la frise
(280-920) et la petite horloge à son bout ; l'échelle : appartement, livret, assurance-vie avec leurs délais ; la
feuille et la pilule rangées en haut à droite ; « Toi » (`toi`, bras droit, baissé) en P1.

Temps forts (image du mot) :
S15  plan@1772  reste@1834  bloqué@1843  jusqu’à@1854  déblocage@1902  anticipé.@1920
S16  l’épargne@1961  bloquée@2004  5 ans,@2022  exceptions.@2058
S17  Comment@2090  retrouver ?@2103  faisant@2131  liste.@2154
S18  Pour@2172  note@2206  combien@2223  temps@2238
S19  Puis@2287  frais.@2312  Et@2335  risque@2354  prix.@2374
S20  La@2394  vraie@2399  combien@2447  possèdes.@2462
S21  C’est@2485  récupères@2506  argent,@2526  demain.@2573
S22  Abonne-toi@2592  argent.@2643

Tour 1 de revue :
- S15-S16 : mur de briques (50 x 200) en x 640, PER puis épargne salariale seuls sur la scène en x 820 (élan de 91 px).
  Les pièces partent du bord gauche du disque, en file sur le rail, cognent le mur (il tremble, son cadenas aussi) et
  reviennent dans le disque. La porte est un événement : porte deep 5 px (64 x 110) qui déborde du mur, qui pivote
  sur sa charnière (sx 1 -> 0,15) et laisse un passage ; UNE pièce cerclée de cyan, marquée « ×1 », passe ; la
  porte se referme, le cadenas bat ; en S15 deux pièces cognent la porte refermée.
- S17 : la feuille descend et grandit en « Ma liste » (892 x 600, x 44-936, y 420-1020) PAR-DESSUS l'échelle ;
  frise, mur et horloge se rangent (rail rétracté vers la caisse, mur dans son cadenas, horloge dans l'appartement) ;
  la caisse monte en haut à gauche (x1, 60-280 x 172-412) ; « liste. » : les disques glissent dans les lignes
  (stagger 1, 8 images), trois cases en tirets par ligne (Délai · Frais · Risque, sous les disques du repère).
- S18-S19 : délais écrits DANS les cases délai (32 px) ; S19 « prix. » : toutes les cases restées vides battent
  ensemble : à remplir.
- S20 : la liste ne bouge pas (lisible) ; la facture rouge retombe à droite de la caisse, « demain » collé dessus ;
  la pilule s'y écrase (tenue 300 ms), tremble, son bord s'allume en rouge, la facture tremble deux fois, revient.
- S21 : « Toi » touche la case délai du bas : la ligne de l'appartement est barrée ; le surligneur monte à « vite »,
  le « ? » des actions bat et leur ligne est barrée ; il monte à « quelques jours », l'anneau entoure la ligne
  (12 px à l'intérieur de la carte), puis seulement trois pièces en sortent et paient la facture (recette de S05).
  Écart assumé : l'anneau n'est pas tracé par le stylo (la ligne 1, y 543, est à 576 px de l'épaule : hors
  d'atteinte, 267 px) ; c'est le geste de « Toi » en bas de la colonne qui lance le surligneur.
- S22 : carte de fin plus haut (pos 540, 720 ; le bas à 980, la tête de « Toi » à 1039), sous-titre 34 px ; les
  éléments se réduisent (morph) sans fondu gris.
"""
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401

from . import *  # noqa: F401,F403
from . import (AXE_Y, BULLE_RONDS_R, CAISSE_HAUT, CAISSE_PLACES, CELL_H, COINS, COL_DELAI, COL_DISC, COL_FRAIS,
               COL_RISQUE, CYAN, DELAI_OF, DELAIS, DISC_ID, DROP_FROM_Y, ENTRY_P3, FACTURE_HAUT, FIN_BUTTON, FIN_C,
               FIN_TAP, HEAD_DY, INK, LAD_NOMS, LAD_ORDER, LIGHT, LIGNES, LIST_C, LIST_DISC_K, LIST_H, LIST_HEAD,
               LIST_W, MARKER_XS, MARKER_Y, MUR_C, MUR_CADENAS_LOCAL, MUR_CONTACT_X, NOMS, P1, P2, P_FIN, P_FRAIS,
               PASTILLE_H, PASTILLE_LISTE, PASTILLE_LISTE_K, PLACEMENTS, RAIL_B, RED, ROWS_Y, STAGE_C, T_ABONNER,
               assert_reach, bulle_ronds, hold_low, list_local, lower, ring, row_pt, scene_f0, turn, walk_low)
from .p1 import pay
from .p2 import file_away

# ---------- constantes propres à la partie 3 ----------
BULLE_P3, BULLE_P3_W, BULLE_P3_H = (440, 1140), 160, 90       # S17 : à gauche et sous la tête de « Toi » en P2
HEADER_LOCAL = [0, -LIST_H / 2 + 4 + (LIST_HEAD - 8) / 2]       # bandeau-en-tête : (0, -260), 884 x 72
HEADER_W = [LIST_C[0], LIST_C[1] + HEADER_LOCAL[1]]
PASTILLE_HIT = (510 + 155, FACTURE_HAUT[1])     # S20 : bord gauche de la pilule (x1) contre le bord droit de la facture
BTN_K = round(112 / PASTILLE_H, 4)              # S22 : la pilule (h 90) à l'échelle du bouton (h 112)
DELAI_TAP = (COL_DELAI, ROWS_Y[5] + 22)         # bas de la case délai de l'appartement
FRAIS_TAP = (COL_FRAIS, ROWS_Y[5] + 22)
RISQUE_TAP = (COL_RISQUE, ROWS_Y[5] + 22)


def part(S, kit, c):
    toi, toi_g = c.toi, c.toi_g
    f0 = scene_f0(S, "S15")                       # 1767
    film_end = round(S.sb["scenes"][-1]["t_end"] * S.fps)

    # ---------- état d'entrée : etat_initial de S15 ----------
    kit.pin(f0 - 1, ENTRY_P3)
    if S.val(toi.id, "scale", f0 - 1) == 0:      # partie construite seule : sans effet dans le film entier
        toi.enter(f0 - 10, at=list(P1))

    assert_reach(P2[0], DELAI_TAP, "S18 case délai", "left", fig_y=P2[1])
    assert_reach(P_FRAIS[0], FRAIS_TAP, "S19 case frais", "right", fig_y=P2[1])
    assert_reach(P_FIN[0], RISQUE_TAP, "S19 case risque", "right", fig_y=P2[1])
    assert_reach(P_FIN[0], DELAI_TAP, "S21 case délai", "left", fig_y=P2[1])
    assert_reach(P_FIN[0], FIN_TAP, "S22 bouton", "right", fig_y=P2[1])

    def bump(src, ids, f, stagger=3, go=8, back=9, amp=8):
        """Les pièces sortent du bord gauche de `src`, filent en file sur le rail vers la caisse, cognent le mur (son
        cadenas tremble avec lui) et reculent dans `src`. -> images des chocs."""
        sx = S.to_world(src, [0, 0], f - 1)[0] - 38
        hits = []
        for k, cid in enumerate(ids):
            t = f + k * stagger
            S.key(cid, "rot", t - 1, 0)
            S.key(cid, "scale", t - 1, 0)
            g = kit.pop(cid, t, scale=1, from_pt=[sx + 20, AXE_Y], to=[sx, AXE_Y], d=3)
            h = kit.move(cid, g, [MUR_CONTACT_X, AXE_Y], d=go, e="in")
            kit.shake("mur", h, amp=amp)
            kit.vanish(cid, h, into=src, d=back)
            hits.append(h)
        return hits

    def door(f, cid, src, dest, close_at):
        """La porte du mur s'ouvre (pivote sur sa charnière), UNE pièce cerclée « ×1 » sort de `src`, passe et file
        jusqu'à `dest` ; la porte se referme à close_at. -> arrivée de la pièce."""
        S.key("mur_charniere", "sx", f, 0.15, 6, "out")
        S.key("mur_trou", "opacity", f + 1, 1)
        sx = S.to_world(src, [0, 0], f - 1)[0] - 38
        S.key(cid, "rot", f - 1, 0)
        g = kit.pop(cid, f + 1, scale=1, from_pt=[sx + 20, AXE_Y], to=[sx, AXE_Y], d=4)
        kit.pop(f"{cid}_anneau", f + 2, d=6)
        kit.pop(f"{cid}_un", f + 4, d=6)
        arr = kit.move(cid, g, list(dest), d=20, e="inOut")
        kit.vanish(f"{cid}_anneau", arr - 2, d=6)
        kit.vanish(f"{cid}_un", arr - 2, d=6)
        S.key("mur_charniere", "sx", close_at, 1, 6, "in")
        S.key("mur_trou", "opacity", close_at + 5, 0)
        return arr

    # ================= S15 « Le plan d’épargne retraite, lui, reste bloqué … sauf déblocage anticipé. » ==========
    f = kit.at("S15", "plan", "les trois pièces des actions s'enfoncent dans la caisse ; les actions montent se ranger "
                              "dans l'échelle avec « vite » (la courbe rentre en elles) ; le PER (sablier) tombe loin "
                              "à droite sur la frise, « PER » juste au-dessus")
    for cid in COINS["s14"]:
        kit.vanish(cid, f, into="caisse")
    kit.pulse("caisse", f + 6, peak=1.05)
    S.key("place2", "stroke", f, INK, 4)
    S.key("place2", "sw", f, 3, 4)
    kit.vanish("courbe", f, into="actions", d=6)
    file_away(S, kit, "actions", f)
    g = kit.drop("per", f + 10, h=STAGE_C["per"][1] - DROP_FROM_Y)
    kit.pop(NOMS["per"][0], g - 4)

    f = kit.at("S15", "reste", "un mur de briques à cadenas tombe sur la frise entre la caisse et le PER")
    kit.drop("mur", f, h=MUR_C[1] - DROP_FROM_Y)

    f = kit.at("S15", "bloqué", "trois pièces sortent du PER, filent vers la caisse et cognent le mur, qui tremble avec "
                                "son cadenas ; elles reculent dans le PER")
    bump("per", COINS["s15"], f)

    f = kit.at("S15", "jusqu’à", "« à la retraite » (sablier) surgit juste sous le PER")
    kit.pop("delai_retraite", f)

    f = kit.at("S15", "déblocage", "une porte deep surgit dans le mur et s'ouvre sur sa charnière ; UNE pièce sort du "
                                   "PER, cerclée de cyan et marquée « ×1 », passe la porte et file jusqu'à la caisse")
    kit.pop("mur_charniere", f, d=5)
    f_ant = kit.at("S15", "anticipé.", "le cadenas du mur bat ; la porte se referme derrière la pièce ; deux autres "
                                       "pièces sortent du PER et cognent la porte fermée, le mur tremble ; elles "
                                       "reculent")
    door(f + 3, COINS["s15"][0], "per", CAISSE_PLACES[0], f_ant + 6)
    kit.pulse("mur_cadenas", f_ant, peak=1.3)
    hits = bump("per", COINS["s15"][1:], f_ant + 14, stagger=3)
    kit.pulse("mur_cadenas", hits[0], peak=1.2)

    # ================= S16 « Et l’épargne salariale est souvent bloquée 5 ans, sauf exceptions. » =================
    f = kit.at("S16", "l’épargne", "la pièce passée s'enfonce dans la caisse ; le PER monte se ranger dans l'échelle "
                                   "avec « à la retraite » ; l'épargne salariale (une personne) tombe derrière le mur, "
                                   "« Épargne salariale » juste au-dessus")
    kit.vanish(COINS["s15"][0], f, into="caisse")
    kit.pulse("caisse", f + 6, peak=1.05)
    file_away(S, kit, "per", f)
    g = kit.drop("epargne_salariale", f + 10, h=STAGE_C["epargne_salariale"][1] - DROP_FROM_Y)
    kit.pop(NOMS["epargne_salariale"][0], g - 4)

    f = kit.at("S16", "bloquée", "trois pièces sortent de l'épargne salariale, cognent le mur, qui tremble avec son "
                                 "cadenas ; elles reculent")
    bump("epargne_salariale", COINS["s16"], f)

    f = kit.at("S16", "5 ans,", "« 5 ans » (calendrier) surgit juste sous l'épargne salariale")
    kit.pop("delai_5ans", f)

    f = kit.at("S16", "exceptions.", "la porte s'ouvre une seule fois : une seule pièce, cerclée « ×1 », la passe et "
                                     "file à la caisse ; la porte se referme et le cadenas bat")
    door(f, COINS["s16"][0], "epargne_salariale", CAISSE_PLACES[0], f + 18)
    kit.pulse("mur_cadenas", f + 18, peak=1.3)

    # ================= S17 « Comment t’y retrouver ? En faisant ta propre liste. » =================
    f = kit.at("S17", "Comment", "la pièce passée s'enfonce dans la caisse ; « Toi » se déplace à droite")
    kit.vanish(COINS["s16"][0], f, into="caisse")
    kit.pulse("caisse", f + 6, peak=1.05)
    walk_low(toi, f, P2[0], d=10)

    f = kit.at("S17", "retrouver ?", "trois petits ronds puis une bulle de pensée en tirets avec un « ? » sortent de la "
                                     "tête de « Toi »")
    head = (P2[0], P2[1] + HEAD_DY)
    ronds = bulle_ronds(head, (BULLE_P3[0] + BULLE_P3_W / 2, BULLE_P3[1]))
    S.keys("bulle", f - 1, pos=list(BULLE_P3), w=BULLE_P3_W, h=BULLE_P3_H, scale=0)
    S.key("bulle_pilule", "scale", f - 1, 0)
    S.key("bulle_q", "scale", f - 1, 1)
    for k, pt in enumerate(ronds):
        S.key(f"bulle_rond{k + 1}", "pos", f - 1, pt)
        kit.pop(f"bulle_rond{k + 1}", f + 2 * k, d=6)
    kit.pop("bulle", f + 5)

    f = kit.at("S17", "faisant", "la feuille du haut descend et grandit en liste par-dessus l'échelle ; son bandeau "
                                 "devient l'en-tête « Ma liste », la pilule « 200 000 € » s'y pose ; les noms et les "
                                 "délais rentrent dans leurs disques ; le rail se rétracte vers la caisse, le mur dans "
                                 "son cadenas, l'horloge dans l'appartement ; la caisse monte en haut à gauche")
    kit.move("feuille", f, list(LIST_C), scale=1)
    S.key("feuille", "w", f, LIST_W, MOVE, "inOut")
    S.key("feuille", "h", f, LIST_H, MOVE, "inOut")
    S.key("feuille_bandeau", "pos", f, HEADER_LOCAL, MOVE, "inOut")
    S.key("feuille_bandeau", "w", f, LIST_W - 8, MOVE, "inOut")
    S.key("feuille_bandeau", "h", f, LIST_HEAD - 8, MOVE, "inOut")
    kit.fade("feuille_titre", f, to=0)
    kit.vanish("feuille_icone", f, d=6)
    f_liste = S.word_after("liste", f)
    kit.pop("liste_titre", f_liste + 3)        # après le départ des disques de l'échelle, qui le couvraient
    kit.move("pastille", f, list(PASTILLE_LISTE), scale=PASTILLE_LISTE_K)
    S.key("pastille", "fill", f, CYAN, 8)
    S.key("rail", "pa", f, list(RAIL_B), DRAW, "in")
    S.key("rail", "draw", f + DRAW, 0)
    kit.vanish("rail_fleche", f + DRAW - 2, into="caisse", d=6)
    kit.vanish("mur", f, into=S.to_world("mur", list(MUR_CADENAS_LOCAL), f - 1))
    kit.vanish("horloge", f, into=DISC_ID["maison"])
    for i in ("bulle", "bulle_rond1", "bulle_rond2", "bulle_rond3"):
        kit.vanish(i, f, d=6)
    kit.vanish(NOMS["epargne_salariale"][0], f, into="epargne_salariale", d=6)
    for k, pid in enumerate(LAD_ORDER):
        did = DELAI_OF[pid]
        kit.vanish(did, f + k, into=DISC_ID[pid], d=7)
        if pid != "epargne_salariale":
            kit.vanish(LAD_NOMS[pid], f + k, into=DISC_ID[pid], d=7)
    kit.move("caisse", f_liste + 6, list(CAISSE_HAUT))   # passe DERRIÈRE la liste (z 4), après le départ de l'échelle

    f = kit.at("S17", "liste.", "les six placements glissent chacun sur une ligne de la liste, du plus rapide au plus "
                                "lent, l'appartement en dernier ; leur nom s'écrit à côté ; trois cases en tirets "
                                "surgissent sur chaque ligne, sous Délai · Frais · Risque")
    for i, (pid, lid) in enumerate(zip(PLACEMENTS, LIGNES)):
        t = f + i
        g = kit.move(DISC_ID[pid], t, row_pt(i, COL_DISC), d=7, scale=LIST_DISC_K)
        kit.type(f"{lid}_nom", g - 5, rate=8)
        for j, suf in enumerate(("cdelai", "frais", "risque")):
            kit.pop(f"{lid}_{suf}", g - 5 + j, d=5)
    last = f + 5 + 7 - 5 + 2 + 5                 # dernière case posée : au moins 3 images de repos avant S18
    assert last <= scene_f0(S, "S18") - 3, (last, scene_f0(S, "S18"))

    # ================= S18 « Pour chaque placement, note en combien de temps tu récupères l’argent. » =============
    f = kit.at("S18", "Pour", "l'horloge, une pièce et le « ? » ressortent de l'appartement et montent en arc ; ils "
                              "deviennent les trois disques du repère « Délai · Frais · Risque », au-dessus des "
                              "colonnes")
    kit.ensure("horloge", "z", S.ents["horloge"]["z"])
    S.key("horloge", "z", f - 1, 12.5)
    born = S.to_world(DISC_ID["maison"], [0, 0], f - 1)
    arrive = []
    for k, (oid, s) in enumerate((("horloge", 0.45), ("piece_s10_1", 0.85), ("doute", 0.6))):
        t = f + 3 * k
        S.key(oid, "pos", t - 1, [round(born[0], 2), round(born[1], 2)])
        S.key(oid, "rot", t - 1, 0)
        kit.pop(oid, t, scale=s, d=6)
        arrive.append(kit.move(oid, t, [MARKER_XS[k], MARKER_Y], d=14, arc=90))
    kit.morph(["horloge", "piece_s10_1", "doute"], ["marqueur"], max(arrive), pair=False)

    f = kit.at("S18", "note", "le disque 1 « Délai » s'allume en cyan ; « Toi » change de bras, vers la colonne délai")
    S.key("marqueur", "on", f, 1, POP, "out")
    turn(S, toi, toi_g, f)

    f = kit.at("S18", "combien", "« Toi » touche la case délai de l'appartement : « plusieurs mois » s'y écrit")
    hit = toi_g.tap(f - TAP + 1, list(DELAI_TAP))
    kit.type("ligne6_delai", hit, rate=5)
    lower(toi_g, hit + 6, 8)

    f = kit.at("S18", "temps", "les cinq autres délais s'écrivent dans leurs cases, de haut en bas : quelques jours, "
                               "vite, 2 mois max., à la retraite, 5 ans")
    kit.stagger([f"{lid}_delai" for lid in LIGNES[:5]], f, 4, kit.type, rate=5)

    # ================= S19 « Puis avec quels frais. Et avec quel risque sur le prix. » =================
    f = kit.at("S19", "Puis", "le disque actif glisse sur 2 « Frais » et une coche se trace dans le disque 1 ; "
                              "« Toi » se retourne et s'avance")
    kit.step(f, 1)
    S.key("marqueur", "done0", f, 1, POP, "out")
    g = turn(S, toi_g, toi, f)
    walk_low(toi, g, P_FRAIS[0])

    f = kit.at("S19", "frais.", "« Toi » touche la case frais de l'appartement : un « − » et une pièce s'y posent")
    hit = toi.tap(f - TAP + 1, list(FRAIS_TAP))
    kit.pop("ligne6_moins", hit)
    kit.pop("piece_s19", hit + 1)
    lower(toi, hit + 6, 8)

    f = kit.at("S19", "Et", "le disque actif glisse sur 3 « Risque » et une coche se trace dans le disque 2 ; « Toi » "
                            "s'avance")
    kit.step(f, 2)
    S.key("marqueur", "done1", f, 1, POP, "out")
    walk_low(toi, f, P_FIN[0])

    f = kit.at("S19", "risque", "« Toi » touche la case risque de l'appartement : un « ? » s'y pose")
    hit = toi.tap(f - TAP + 1, list(RISQUE_TAP))
    kit.pop("ligne6_q", hit)
    lower(toi, hit + 6, 8)

    f = kit.at("S19", "prix.", "la courbe en dents de scie ressort du disque des actions et se change en « ? » dans "
                               "leur case risque ; « sans perte » sort du livret et s'écrit dans sa case risque ; "
                               "puis toutes les cases restées vides battent ensemble : à remplir")
    a2 = row_pt(1, COL_RISQUE)
    S.key("courbe", "draw", f - 1, 1)
    g = kit.pop("courbe", f, scale=0.6, from_pt="actions", to=[a2[0] - 70, a2[1]], d=7)
    kit.morph("courbe", "ligne2_q", g)
    kit.pop("ligne1_sans_perte", f + 3, from_pt="livret")
    kit.type("ligne1_sans_perte", f + 5, rate=4)
    empty = [f"{lid}_frais" for lid in LIGNES[:5]] + [f"{lid}_risque" for lid in LIGNES[2:5]]
    for cid in empty:
        kit.pulse(cid, f + 14, peak=1.12, step=4)

    # ================= S20 « La vraie question, ce n’est pas combien tu possèdes. » =================
    f = kit.at("S20", "La", "une coche se trace dans le disque 3, puis le repère se range dans l'en-tête de la liste ; "
                            "la liste reste en place, lisible")
    S.key("marqueur", "done2", f, 1, 6, "out")
    kit.vanish("marqueur", f + 3, into=HEADER_W)
    turn(S, toi, toi_g, f + 8)

    f = kit.at("S20", "vraie", "la facture « 3 000 € » rouge retombe à droite de la caisse vide, « demain » collé sur "
                               "son bord haut ; la facture tremble")
    S.key("facture_coche", "scale", f - 1, 0)
    S.key("facture_montant", "color", f - 1, RED)
    S.key("facture", "rot", f - 1, 0)
    S.key("facture", "opacity", f - 2, 0)
    g = kit.drop("facture", f, h=50, to=list(FACTURE_HAUT))   # chute courte : jamais sous l'interface du haut
    kit.pop("demain", f + 6)
    kit.shake("facture", g, amp=8)

    f = kit.at("S20", "combien", "la pilule « 200 000 € » bondit de l'en-tête, reprend sa taille et vole jusqu'à la "
                                 "facture ; elle s'écrase contre son bord droit")
    S.key("pastille", "scale", f, 1, 5, "out")
    lift = [PASTILLE_LISTE[0] - 20, PASTILLE_LISTE[1] - 50]
    g = kit.move("pastille", f, lift, d=4, e="out")
    hit = kit.move("pastille", g, list(PASTILLE_HIT), d=8, e="in")
    kit.shake("facture", hit, amp=6)

    f = kit.at("S20", "possèdes.", "la pilule, toujours collée à la facture, tremble et son bord s'allume en rouge ; "
                                   "la facture tremble deux fois, « 3 000 € » reste rouge ; puis la pilule recule et "
                                   "revient sur l'en-tête de la liste")
    kit.shake("pastille", f, amp=8)
    S.key("pastille_alerte", "opacity", f, 1)
    S.key("pastille_alerte", "opacity", f + 8, 0, 3, "linear")
    kit.shake("facture", f, amp=9)
    kit.shake("facture", f + 4, amp=9)
    kit.move("pastille", f + 7, list(PASTILLE_LISTE), d=14, e="out", scale=PASTILLE_LISTE_K)
    assert f + 7 + 14 <= scene_f0(S, "S21") - 1

    # ================= S21 « C’est comment tu récupères ton argent, si tu en as besoin demain. » =================
    f = kit.at("S21", "C’est", "« Toi » touche la case délai du bas : la ligne de l'appartement (plusieurs mois, « ? ») "
                               "est barrée ; un surligneur monte la colonne jusqu'à « vite » : le « ? » des actions "
                               "bat et leur ligne est barrée à son tour")
    hit = toi_g.tap(f - TAP + 1, list(DELAI_TAP))
    g = kit.pop("surligneur", hit, d=4)
    kit.pulse("ligne6_q", hit, peak=1.3)
    kit.draw("ligne6_barre", hit + 2, 6, e="inOut")
    g = kit.move("surligneur", hit + 4, list_local(COL_DELAI, ROWS_Y[1]), d=8, e="inOut")
    kit.pulse("ligne2_q", g - 1, peak=1.35, step=2)
    kit.draw("ligne2_barre", g + 2, 6, e="inOut")
    lower(toi_g, hit + 6, 8)

    f = kit.at("S21", "récupères", "le surligneur monte jusqu'à « quelques jours » et un anneau entoure toute la ligne "
                                   "« Comptes, livrets » ; anneau fermé, trois pièces sortent du livret")
    kit.move("surligneur", f, list_local(COL_DELAI, ROWS_Y[0]), d=5, e="out")
    closed = kit.draw("anneau", f + 1, 7)
    f_arg = kit.at("S21", "argent,", "les trois pièces entrent dans la facture, sous le montant : « 3 000 € » passe "
                                     "au deep et la grande coche surgit : payée")
    jump = 10
    start = f_arg - jump - 1
    assert start >= closed + 1, (start, closed)
    src = S.to_world("livret", [0, 0], closed)
    for k, cid in enumerate(COINS["s21"]):
        S.key(cid, "rot", closed - 1, 0)
        kit.pop(cid, closed + k, scale=0.8, from_pt=src, to=src, d=3)
    arr = pay(S, kit, COINS["s21"], start, jump=jump, arc=40)
    assert arr == f_arg, (arr, f_arg)
    turn(S, toi_g, toi, f_arg + 20)              # « Toi » reprend le bras droit (vers le bouton de la fin)

    f = kit.at("S21", "demain.", "« demain » bat une fois ; la facture payée est tenue")
    kit.pulse("demain", f, peak=1.12)

    # ================= S22 « Abonne-toi pour comprendre ton argent. » =================
    outs = ["feuille", *[DISC_ID[p] for p in PLACEMENTS], "caisse", "facture", *COINS["s21"], "demain"]
    glide = MOVE
    f22 = S.word("Abonne-toi") + 1                      # = le temps fort (calé sur l'attaque), posé par kit.outro
    for o in outs:                                       # tout converge vers la carte (ni éclats ni points résiduels)
        kit.vanish(o, f22, into=list(FIN_C), d=MORPH)
    out = kit.outro("S22", outs=[], btn_at=glide, press="argent.", pos=FIN_C, bsize=round(52 * BTN_K, 1),
                    labelSize=34)
    f = out["card"]
    S.set(out["cursor"], opacity=0)                      # pas de pointeur de souris : le stylo de « Toi » touche
    kit.ensure("pastille", "z", S.ents["pastille"]["z"])
    S.key("pastille", "z", f, 41)                        # au-dessus de la carte (z 40)
    kit.ensure("pastille", "textOp", 1)
    S.key("pastille", "textOp", f, 0, 4, "out")
    S.key("pastille", "text", f + 4, T_ABONNER)
    S.key("pastille", "textOp", f + 4, 1, FADE, "out")
    S.key("pastille", "w", f, round(380 / BTN_K, 2), glide, "inOut")
    kit.move("pastille", f, list(FIN_BUTTON), d=glide, e="inOut", scale=BTN_K)
    S.key("pastille", "opacity", f + glide, 0)          # relais exact : le bouton de la carte paraît dessous

    fp = out["press"]
    toi.set_z(fp - TAP - 12, S.ents[toi.id]["z"], tool_z=44)    # bras et stylo au-dessus de la carte
    toi.reach(fp - TAP - 10, [FIN_TAP[0] + 10, FIN_TAP[1] + 40], d=10)
    hit = toi.tap(fp - TAP + 1, list(FIN_TAP))
    for k in range(2):
        ring(S, f"fin_onde{k + 1}", hit + 4 * k, d=14, s0=0.6, s1=2.0)
    end = lower(toi, hit + 6, 8)
    assert hit == fp and end < film_end and hit + 4 + 14 < film_end, (hit, fp, end, film_end)
