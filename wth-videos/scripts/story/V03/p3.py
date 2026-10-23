"""V03, partie 3 : S16-S21, images 2088-2926 (33 temps forts, 27,9 s). La liste des frais pendue à l'étiquette, le
document d'informations clés qui la range, l'intermédiaire qui remet à « Toi » son relevé en € et en %, la vague du
marché qui monte et plonge seule pendant que « Toi » prend la ficelle de l'étiquette, le panneau « Rendement affiché »
barré, l'étiquette qui devient le bouton de la carte de fin.

État d'entrée, épinglé à l'image 2087 : kit.pin(2087, ENTRY_P3) (etat_initial de S16). « Toi » en P_TOI, stylo au
repos (jamais épinglé) ; `intermediaire` à l'échelle 0.

Temps forts (image du film, round(t x 30) ; ACOUSTIC_SNAP peut décaler d'une image) :
S16  Et@2088  produit,@2105  s’allonger :@2138  arbitrage,@2168  sortie,@2205  transaction,@2231  change,@2259
     droits@2278
S17  Alors,@2314  retrouver ?@2340  Demande@2369  clés@2419  détail@2440
S18  intermédiaire@2482  doit@2502  communiquer@2513  euros@2575  pourcentage.@2597
S19  Tu@2628  ne@2633  pas@2649  marchés.@2657  contrôles@2687  frais.@2705
S20  Et@2726  rendement@2736  affiché@2750  sans@2769  frais@2781  n’est@2794
S21  Abonne-toi@2835  comprendre@2868  argent.@2889      (dernière image du film : 2926)

Tour de revue 1 :
- S16 : le disque 2 se coche (fait) ; pendant que la liste se construit, la légende du repère et « Frais : »
  s'effacent (les disques restent). Liste en deux colonnes (corps 32, 5 rangées au plus avec l'étiquette) : gestion,
  entrée, arbitrage, sortie en A ; en B, chaque nouvelle étiquette naît sous l'étiquette du fil et pousse les autres
  d'un cran AVANT d'arriver : aucune étiquette n'en recouvre une autre. Plus de kit.drop (il montrait l'objet à f − 1).
- S17 : la colonne réduite reste à 0,7 (« 10 000 € » à 39 px) ; le livre PNG devient un document papier plat (carte
  ivoire, traits encre), titré en clair « Document d’informations clés » avec « DIC » dessous (44 px) ; le « ? » de
  « Toi » attend à sa place et se pose sur lui avant que les étiquettes n'y volent.
- S18 : le relevé sort du document dans la main de l'intermédiaire (« doit »), qui fait un pas vers « Toi » et le pose
  à portée de son stylo (« communiquer ») ; « obligatoire » (pilule claire, texte encre) est tamponné sur le relevé à
  la remise ; « Toi » touche le relevé (« euros ») avant que les lignes ne s'écrivent, « sur 10 000 € » sous
  « 100 € / an », puis il le coche. « ton intermédiaire » au-dessus de sa tête, hors du buste.
- S19 : le repère se réduit avec l'intermédiaire et le document. La vague plate se trace (« ne ») pendant que « Toi »
  tourne la tête vers elle sans bouger le stylo ; elle monte de 200 px en basculant de −10° (« pas », flèche deep vers
  le haut à côté de « marché »), puis plonge de 260 px à +10° (« marchés. », flèche vers le bas).
- S20 : panneau élargi (420), textes centrés, colonne remontée à 0,8 à sa gauche (40 px d'ivoire) ; l'étiquette bute
  sur le bord haut du panneau et se pose 28 px au-dessus ; « Toi » barre le 5 % depuis x 620.
- S21 : l'étiquette, seule sur l'ivoire, va et s'élargit en bouton en 14 images en gardant « 1 % / an », bat, puis
  devient « S’abonner » ; la carte (titre, marque, ligne à 36 px) n'entre qu'ensuite, et son bouton prend le relais.
"""
from pipeline.story import DRAW, FADE, MORPH, MOVE, POP
from pipeline.story_kit import TAP

from . import (DIC_C, ENTRY_P3, EPARGNE_MINI, EPARGNE_MINI_K, EPARGNE_S16, EPARGNE_S20, EPARGNE_S20_K, ETIQ_BTN_SCALE,
               ETIQ_BUTE, ETIQ_LISTE, ETIQ_POSEE, ETIQ_S20, ETIQ_SIZE, ETIQ_TAP, ETIQ_TIRE, ETIQ_TOI, FIN_BUTTON,
               FIN_TAP, INTERM_FROM, INTERM_NOM, INTERM_NOM_PAS, LISTE_B_X, LISTE_FIL_B, LISTE_ROWS, LISTE_SLOTS,
               P_INTERM, P_INTERM_PAS, P_TOI, P_TOI_S20, PANNEAU_TAUX, QUESTION_COIN, QUESTION_DIC,
               QUESTION_NEE, RELEVE_C, RELEVE_COCHE, RELEVE_FROM, RELEVE_MAIN, RELEVE_MAIN_K, RELEVE_TAP,
               VAGUE_FLECHE_S19, VAGUE_MARCHE_S19, VAGUE_S19, VAGUE_S19_DOWN, VAGUE_S19_UP, fig_pos, ring, scene_f0)

F_START, F_END = 2088, 2926
TIP_TIENT = (770, 990)                     # S19 « frais. » : la pointe recule à gauche de la tête, la ficelle tendue
P_TOI_APPROCHE = fig_pos(720)              # S20 « rendement » : « Toi » s'approche ; stylo au repos hors du panneau
P_TOI_RECUL = fig_pos(770)                 # S20 après la rature : il recule, « 5 % / an » et « 4 % net » dégagés
FIN_TAP_S21 = (FIN_TAP[0] + 32, FIN_TAP[1] - 4)   # S21 : bout droit du bouton, hors de « S’abonner » (corps 60, x ≤ 691)
FIN_DOIGT_FROM = (FIN_TAP_S21[0] + 90, FIN_TAP_S21[1] + 90)   # S21 « comprendre » : le doigt arrive du bas droit
B_TOP = (LISTE_FIL_B[0][0], LISTE_FIL_B[0][1])   # S16 : les étiquettes de B naissent sous l'étiquette du fil
BOUTON = 14                                # S21 : images du trajet de l'étiquette jusqu'au bouton
CARTE = BOUTON + 2                         # S21 : la carte n'entre qu'une fois l'étiquette posée


def part(S, kit, c):
    toi, interm = c.toi, c.interm
    f0 = scene_f0(S, "S16")
    assert f0 == F_START, f0
    kit.pin(f0 - 1, ENTRY_P3)
    if S.val("toi", "scale", f0 - 1) == 0:     # partie construite seule : « Toi » n'est pas entré
        toi.enter(f0 - 10, at=list(P_TOI))

    # ================= S16 « Et selon le produit, la liste peut s’allonger : … droits de garde. » =================
    f = kit.at("S16", "Et", "repère : le disque actif glisse sur 3 « Autres » ; le disque 2 se coche (fait)")
    kit.step(f, 2)
    S.key("marqueur", "done1", f + 4, 1, 8, "out")

    f = kit.at("S16", "produit,", "rangement : l'étiquette « 1 % / an » monte en haut à droite (sa ficelle vers la "
                                  "colonne rentre) ; la pile se réduit dans l'étiquette et « gestion » devient "
                                  "l'étiquette bleu clair « gestion » ; le jeton de 30 € devient l'étiquette « entrée » ; "
                                  "le bac se réduit ; la colonne glisse à gauche")
    kit.draw("ficelle", f, 8, track="from")
    kit.move("etiquette", f, list(ETIQ_LISTE), MOVE)
    kit.move("epargne", f, list(EPARGNE_S16), MOVE)
    kit.vanish("pile", f + 1, into=list(ETIQ_LISTE), d=MOVE - 2)
    kit.morph(["etiquette_gestion"], ["liste1"], f + 2, d=MOVE - 2)
    kit.morph(["jeton_entree"], ["liste2"], f + 4, d=MOVE - 2)
    for o in ("jeton_entree_txt", "etiquette_entree"):
        kit.vanish(o, f + 4, into=list(LISTE_SLOTS[1]), d=MOVE - 4)
    kit.vanish("bac", f + 4, d=MORPH)
    kit.fade("pile_repere", f, to=0)

    f = kit.at("S16", "s’allonger :", "deux ficelles deep se tracent vers le bas sous l'étiquette : la liste s'allonge, "
                                      "vide ; la légende du repère s'efface (les disques restent)")
    kit.draw("liste_fil", f, 12, e="out")
    kit.draw("liste_fil2", f + 3, 10, e="out")
    kit.fade("frais_label", f, to=0)
    S.key("marqueur", "lbl", f, 0, FADE, "out")

    b_col = []                                  # étiquettes de la colonne B, de haut en bas

    def push_b(f):
        """Les étiquettes déjà en B descendent d'un cran (8 images) : la place du haut se libère."""
        for k, lid in enumerate(b_col):
            S.key(lid, "pos", f, [LISTE_B_X, LISTE_ROWS[k + 1]], 8, "inOut")

    for k, mot in enumerate(["arbitrage,", "sortie,", "transaction,", "change,", "droits"]):
        lid = f"liste{k + 3}"
        label = S.ents[lid]["p"]["text"]
        if k < 2:       # colonne A : elle naît à sa place, en glissant de 20 px le long de la ficelle
            f = kit.at("S16", mot, f"l'étiquette papier « {label} » arrive sur la ficelle de gauche, sous les précédentes")
            x, y = LISTE_SLOTS[k + 2]
            kit.pop(lid, f, from_pt=[x, y - 20], to=[x, y])
        else:           # colonne B : les autres descendent d'abord, la nouvelle naît sous l'étiquette du fil
            f = kit.at("S16", mot, f"les étiquettes de droite descendent d'un cran ; « {label} » naît en haut de la "
                       "ficelle de droite" + (" ; tenue : 7 frais pendent sous l'étiquette" if k == 4 else ""))
            if b_col:
                push_b(f)
            kit.pop(lid, f + (3 if b_col else 0), from_pt=list(B_TOP), to=[LISTE_B_X, LISTE_ROWS[0]])
            b_col.insert(0, lid)

    # ================= S17 « Alors, comment tout retrouver ? Demande le document d’informations clés … » ==========
    f = kit.at("S17", "Alors,", "la colonne se réduit (0,7) et glisse en bas à gauche")
    kit.move("epargne", f, list(EPARGNE_MINI), MOVE, scale=EPARGNE_MINI_K)

    f = kit.at("S17", "retrouver ?", "un « ? » naît sous la pointe du stylo de « Toi » et vole se poser à gauche, à la "
                                     "place vide du futur document")
    tip = toi.tip(f - 1)
    kit.pop("question", f, from_pt=tip, to=list(QUESTION_NEE))
    kit.move("question", f + POP, list(QUESTION_DIC), MOVE, arc=40)

    f = kit.at("S17", "Demande", "un document papier tombe à la place du « ? », qui se pose sur son coin haut droit")
    S.key("dic", "opacity", f - 1, 0)
    kit.drop("dic", f, h=240, to=list(DIC_C))
    kit.move("question", f, list(QUESTION_COIN), MOVE)

    f = kit.at("S17", "clés", "le titre « Document d’informations clés » s'inscrit sur le document ; « DIC » surgit "
                              "dessous")
    kit.fade("dic_titre1", f)
    kit.fade("dic_titre2", f + 3)
    kit.pop("dic_sigle", f + 6)

    f = kit.at("S17", "détail", "le « ? » se pose dans le document ; puis les 7 étiquettes y volent une à une et "
                                "deviennent 7 traits encre ; les ficelles rentrent. Tenue : l'étiquette « 1 % / an » "
                                "reste seule en haut à droite")
    kit.vanish("question", f, into=list(DIC_C), d=6)
    for k in range(7):
        kit.morph([f"liste{k + 1}"], [f"dic_ligne{k + 1}"], f + 4 + 2 * k, d=13)
    kit.draw("liste_fil", f + 10, 12, to=0, e="inOut")
    kit.draw("liste_fil2", f + 10, 12, to=0, e="inOut")
    kit.fade("frais_label", f + 24)
    S.key("marqueur", "lbl", f + 24, 1, FADE, "out")

    # ================= S18 « Ton intermédiaire doit te communiquer les coûts et frais, en euros et en pourcentage. » ==
    f = kit.at("S18", "intermédiaire", "une figurine papier entre en marchant par la gauche et se tourne vers « Toi » ; "
                                       "« ton intermédiaire » surgit au-dessus de sa tête")
    arrive = interm.enter(f, at=list(P_INTERM), frm=INTERM_FROM, d=MOVE)
    S.key("intermediaire", "look", arrive - 2, 1, 4, "out")
    kit.pop("interm_nom", arrive - 2, to=list(INTERM_NOM))

    f = kit.at("S18", "doit", "le relevé « Coûts et frais » sort du document et arrive dans la main de "
                              "l'intermédiaire")
    kit.pop("releve", f, scale=RELEVE_MAIN_K, from_pt=list(RELEVE_FROM), to=list(RELEVE_MAIN), d=12)

    f = kit.at("S18", "communiquer", "l'intermédiaire fait un pas vers « Toi » et lui tend le relevé, qui se pose à "
                                     "portée de son stylo ; « obligatoire » est tamponné dessus ; le titre se souligne")
    interm.walk(f, list(P_INTERM_PAS), d=10)
    kit.move("interm_nom", f, list(INTERM_NOM_PAS), d=10)
    g = kit.move("releve", f, list(RELEVE_C), MOVE, arc=40, scale=1)
    S.key("interm_oblig", "scale", g - 1, 0)
    S.key("interm_oblig", "scale", g, 1.35)
    S.key("interm_oblig", "scale", g + 1, 1, 5, "out")
    kit.shake("releve", g + 1, amp=4, axis="xy")
    kit.draw("releve_titre", g + 2, 8, track="under")

    f = kit.at("S18", "euros", "« Toi » touche le relevé du stylo ; la ligne « en € : 100 € / an » s'écrit (clé en deep), "
                               "« sur 10 000 € » dessous")
    hit = toi.tap(f - TAP + 1, list(RELEVE_TAP))
    assert hit == f, (hit, f)
    g = kit.type("releve_cle1", f + 1, rate=2)
    g = kit.type("releve_val1", g, rate=2)
    kit.type("releve_sur", g, rate=3)
    toi.rest(hit + 5, 8)

    f = kit.at("S18", "pourcentage.", "la ligne « en % : 1 % / an » s'écrit dessous ; « Toi » coche le relevé. Tenue : "
                                      "l'intermédiaire reste face à « Toi »")
    g = kit.type("releve_cle2", f, rate=2)
    g = kit.type("releve_val2", g, rate=2)
    pt = S.to_world("releve", list(RELEVE_COCHE), g)
    hit = toi.tap(g, pt)
    kit.draw("releve_coche", hit, 6)
    toi.rest(hit + 5, 8)

    # ================= S19 « Tu ne contrôles pas les marchés. Tu contrôles les frais. » =================
    f = kit.at("S19", "Tu", "l'intermédiaire et sa pilule se réduisent et sortent ; le document, le relevé et le repère "
                            "se réduisent ; l'étiquette « 1 % / an » descend devant « Toi »")
    interm.exit(f)
    for o in ("interm_nom", "dic", "releve", "marqueur"):
        kit.vanish(o, f, d=MORPH if o == "marqueur" else POP)
    kit.fade("frais_label", f, to=0)
    kit.move("etiquette", f, list(ETIQ_TOI), MOVE)

    f = kit.at("S19", "ne", "la vague du marché se trace à gauche, « marché » dessous ; « Toi » tourne la tête vers "
                            "elle, stylo baissé")
    S.keys("vague", f - 1, pos=list(VAGUE_S19), scale=1, rot=0, opacity=0, draw=0)
    S.key("vague", "opacity", f, 1)
    kit.draw("vague", f, 10, e="out")
    S.keys("vague_marche", f - 1, pos=list(VAGUE_MARCHE_S19), opacity=1)
    kit.pop("vague_marche", f + 3)
    S.key("toi", "look", f, -1, 5, "out")

    f = kit.at("S19", "pas", "la vague monte de 200 px en basculant ; une flèche deep vers le haut surgit à côté de "
                             "« marché » ; « Toi » ne bouge pas")
    up = [VAGUE_S19[0], VAGUE_S19[1] + VAGUE_S19_UP]
    S.key("vague", "pos", f, up, 8, "out")
    S.key("vague", "rot", f, -10, 8, "out")
    kit.pop("vague_fleche", f)

    f = kit.at("S19", "marchés.", "la vague plonge de 260 px en basculant de l'autre côté ; la flèche pivote vers le "
                                  "bas ; « Toi » ne bouge toujours pas")
    S.key("vague", "pos", f, [up[0], up[1] + VAGUE_S19_DOWN], 12, "inOut")
    S.key("vague", "rot", f, 10, 12, "inOut")
    S.key("vague_fleche", "rot", f, 90, 8, "inOut")

    f = kit.at("S19", "contrôles", "« Toi » se retourne et touche l'étiquette « 1 % / an » de la pointe du stylo")
    S.key("toi", "look", f - 8, 0, 5, "inOut")
    hit = toi.tap(f - TAP + 1, list(ETIQ_TAP))
    assert hit == f, (hit, f)
    kit.pulse("etiquette", hit, peak=1.08)

    f = kit.at("S19", "frais.", "une ficelle se tire de l'étiquette jusqu'à la pointe du stylo ; « Toi » ramène la "
                                "pointe vers lui et l'étiquette suit : il la tient, la vague non. Tenue")
    kit.draw("ficelle_toi", f, DRAW)
    toi.reach(f, list(TIP_TIENT), 12)
    kit.move("etiquette", f + 1, list(ETIQ_TIRE), 12)

    # ================= S20 « Et un rendement affiché sans les frais n’est pas ton rendement. » =================
    f = kit.at("S20", "Et", "la vague se change en panneau papier « Rendement affiché » ; « marché » et la flèche "
                            "s'effacent ; la colonne remonte à côté du panneau")
    kit.morph(["vague"], ["panneau"], f)
    for o in ("vague_marche", "vague_fleche"):
        kit.vanish(o, f)
    kit.move("epargne", f, list(EPARGNE_S20), MOVE, scale=EPARGNE_S20_K)

    f = kit.at("S20", "rendement", "« Toi » marche vers le panneau ; l'étiquette suit au bout de la ficelle")
    d = toi.walk(f, list(P_TOI_APPROCHE)) - f
    kit.move("etiquette", f, list(ETIQ_S20), d)

    f = kit.at("S20", "affiché", "« 5 % / an » surgit en grand au centre du panneau")
    kit.pop("panneau_taux", f)

    f = kit.at("S20", "sans", "« Toi » lâche la ficelle ; l'étiquette des frais glisse et bute sur le bord haut du "
                              "panneau, qui tremble, puis se pose juste au-dessus")
    kit.draw("ficelle_toi", f, 8, track="from", e="inOut")
    g = kit.move("etiquette", f + 1, list(ETIQ_BUTE), 8, e="in")
    kit.shake("panneau", g, amp=6, axis="y")
    kit.move("etiquette", g, list(ETIQ_POSEE), 6, e="out")
    toi.walk(f + 2, list(P_TOI_S20), 10)                         # il s'avance sous le panneau, à portée du 5 %

    f = kit.at("S20", "frais", "« Toi » barre « 5 % / an » d'un trait, de droite à gauche")
    a = S.to_world("panneau", [PANNEAU_TAUX[0] + 103, PANNEAU_TAUX[1]], f - 1)
    b = S.to_world("panneau", [PANNEAU_TAUX[0] - 103, PANNEAU_TAUX[1]], f - 1)
    end = toi.strike(f, a, b, line="panneau_barre", track="draw")
    toi.walk(end + 1, list(P_TOI_RECUL))                          # il recule : le chiffre barré et « 4 % net » dégagés

    f = kit.at("S20", "n’est", "« 4 % net » surgit en deep sous le chiffre barré ; la pilule « ton rendement » surgit "
                               "sous le panneau, à côté de la colonne. Tenue")
    kit.pop("panneau_net", f)
    kit.pop("panneau_ton", f + 3)

    # ================= S21 « Abonne-toi pour comprendre ton argent. » =================
    outs = ["panneau", "panneau_ton", "epargne"]
    bsize = round(ETIQ_SIZE * ETIQ_BTN_SCALE, 1)
    out = kit.outro("S21", outs=outs, press="argent.", clear="fade", bsize=bsize, btn_at=CARTE + MORPH,
                    labelSize=36)
    f = out["card"]
    toi.exit(f)
    # l'étiquette reste seule sur l'ivoire : elle va et s'élargit en bouton en gardant « 1 % / an », bat, puis le
    # libellé devient « S’abonner » ; la carte n'entre qu'après (relais du bouton quand la carte est entière)
    kit.ensure("etiquette", "z", S.ents["etiquette"]["z"])
    S.key("etiquette", "z", f, 41)                               # au-dessus de la carte (z 40)
    kit.ensure("etiquette", "w", S.ents["etiquette"]["p"]["w"])
    S.key("etiquette", "w", f, round(380 / ETIQ_BTN_SCALE, 2), BOUTON, "inOut")
    kit.move("etiquette", f, list(FIN_BUTTON), BOUTON, e="inOut", scale=ETIQ_BTN_SCALE)
    S.key("etiquette", "text", f + BOUTON, "S’abonner")
    kit.pulse("etiquette", f + BOUTON, peak=round(ETIQ_BTN_SCALE * 1.08, 3), step=3)
    S.key(out["id"], "scale", f, 0)                              # la carte attend que l'étiquette soit posée
    kit.pop(out["id"], f + CARTE, d=MORPH)
    S.key(out["id"], "title", f + 4, 0)
    S.key(out["id"], "title", f + CARTE + 4, 1, FADE, "out")
    S.key("etiquette", "opacity", f + CARTE + MORPH, 0)          # le bouton de la carte est entier dessous

    g = kit.at("S21", "comprendre", "un doigt (point d'appui) glisse jusqu'au coin bas droit du bouton « S’abonner »")
    S.key("fin_doigt", "pos", g - 1, list(FIN_DOIGT_FROM))
    kit.pop("fin_doigt", g, to=list(FIN_TAP_S21), d=MORPH)
    S.set(out["cursor"], opacity=0)                              # pas de pointeur de souris : un toucher au doigt
    fp = out["press"]
    S.key("fin_doigt", "scale", fp, 0.8, 2, "out")
    kit.vanish("fin_doigt", fp + 5, d=5)
    for k in range(2):
        S.key(f"fin_onde{k + 1}", "pos", fp - 1, list(FIN_TAP_S21))
        ring(S, f"fin_onde{k + 1}", fp + 4 * k, d=14, s0=0.6, s1=2.1)
    assert f + CARTE + MORPH < g and fp + 4 + 14 < F_END, (f, g, fp, F_END)
