"""V04, partie 1 : S01-S08, images 0-853. Accroche (8 pièces nées de « 800 € » ; elles partent et la pilule décompte
jusqu'à « 0 € », puis « À découvert »), rembobinage (la pilule recompte), « Solde » ≠ « Budget » (cadre à calendrier),
les trois alertes devenues le repère, le panier qui part vers le téléphone et s'arrête sur « ≠ », les factures, photo
(flash, viseur) contre film (le cadre prend un fond et deux bandes perforées, puis défile), le bac et ses fils (chaque
facture se branche seule sur SES deux pièces) pendant que « Toi » se retourne, le volet qui cache les factures.

Temps forts (image du film) :
S01  800 €.@27  sens@71  l’aise…@86
S02  pourtant,@108  finis@126  découvert ?@146
S03  Dans@175  vidéo,@187  solde@243  budget.@275
S04  trois@303  éviter@324  dépenser.@348
S05  problème,@383  chiffre@418  sortir@465
S06  photo.@533  film.@586
S07  Pourquoi@610  prélèvements ?@644  partent@681  penses.@737
S08  Premier@759  oublier@790  venir.@826

Raccord vers p2 : à l'image 853, l'état est exactement ENTRY_P2 (volet fermé, factures enfoncées, six fils tendus,
8 pièces en place, repère sur 1) ; « Toi » retourné (`toi_dos` visible, `toi` caché) en P1.
"""
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP  # noqa: F401

from . import (ALERTES_C, APPLI_C, BAC_H, BUDGET_C, CASES, COIN_PLACES, COINS, CYAN, FACT_BAC, FACT_BAC_SUNK,
               FACT_IDS, FACT_K, FILS, FIN_MOIS_S02, HEAD_DY, MARKER_DISC, NEQ_C, PANIER_C, PANIER_S04, PANIER_STOP,
               REACH_S04, RED, REMBOBINER_C, SOLDE_BOTTOM, SOLDE_C, T_800, VISEUR, VOLET_H, FILM_DRIFT, bulle_ronds,
               euros, scene_f0, turn)

VISEUR_OPEN = 1.14         # S06 : les équerres partent 14 % plus loin du centre du téléphone, puis se referment
BULLE_S01, BULLE_S01_WH = (745, 905), (190, 96)


def part(S, kit, c):
    toi, dos = c.toi, c.dos
    kit.pin(0 - 1, {"solde": {"pos": list(SOLDE_C), "scale": 1, "opacity": 1},
                    "solde_alerte": {"opacity": 0}, "solde_titre": {"under": 0},
                    "marqueur": {"scale": 0, "on": 0}, "bulle_coche": {"draw": 0}})

    # ================= S01 : 800 € = 8 pièces ; « Toi » se détend, bulle cochée =================
    f = kit.at("S01", "800 €.", "huit pièces jaillissent une à une du bas de la pilule « 800 € » et tombent dans "
                                "les quatre rangées de deux de l'écran du téléphone")
    for i, cid in enumerate(COINS):
        kit.pop(cid, f + 2 * i, from_pt=list(SOLDE_BOTTOM), to=list(COIN_PLACES[i]), d=POP)

    f = kit.at("S01", "sens", "« Toi » s'incline, détendu, et range son stylo")
    toi.lean_to(f, -8, d=14)
    toi.stow(f)

    f = kit.at("S01", "l’aise…", "trois petits ronds en tirets sortent de la tête de « Toi », puis une bulle de "
                                 "pensée ; une coche pleine s'y trace : tout va bien")
    head = toi._body_pt([0, HEAD_DY], f - 1)
    corner = [BULLE_S01[0], BULLE_S01[1] + BULLE_S01_WH[1] / 2]
    for k, pt in enumerate(bulle_ronds(head, corner)):
        S.key(f"bulle_rond{k + 1}", "pos", f - 1, pt)
        kit.pop(f"bulle_rond{k + 1}", f + 2 * k, d=6)
    g = kit.pop("bulle", f + 4)
    kit.draw("bulle_coche", g - 1, DRAW)

    # ================= S02 : les pièces partent, la pilule décompte ; « À découvert » =================
    f = kit.at("S02", "pourtant,", "les pièces tombent une à une hors du téléphone ; à chaque départ la pilule "
                                   "décompte 100 € (700 €, 600 €… 0 €) et une place vide en tirets reste")
    for i, cid in enumerate(reversed(COINS)):
        g = f + 4 * i
        kit.drop(cid, g, out=True, h=260)
        kit.fade(CASES[7 - i], g, to=1, d=6)
        S.key("solde", "text", g + 2, euros(700 - 100 * i))

    f = kit.at("S02", "finis", "une pilule « fin du mois » à calendrier surgit au-dessus du téléphone, pendant que "
                               "les dernières pièces tombent")
    kit.pop("fin_du_mois", f, to=list(FIN_MOIS_S02))

    f = kit.at("S02", "découvert ?", "la pilule, à « 0 € », vire au rouge et affiche « À découvert », elle tremble ; "
                                     "la bulle cochée de « Toi » éclate et il se redresse")
    S.key("solde", "fill", f, RED.lower(), 9, "out")
    S.key("solde", "text", f, "")
    kit.fade("solde_alerte", f, to=1, d=FADE)
    kit.shake("solde", f + 9, amp=8)
    kit.vanish("bulle", f, style="burst", n=7, spread=36)
    for k in range(3):
        kit.vanish(f"bulle_rond{2 - k + 1}", f + k, d=6)
    S.key("bulle_coche", "draw", f + 6, 0)
    toi.lean_to(f, 0)

    # ================= S03 : rembobinage ; « Solde » ≠ « Budget » =================
    f = kit.at("S03", "Dans", "un grand ◀◀ surgit au-dessus du téléphone et la pilule « fin du mois » rentre dedans ; "
                              "« Toi » ressort son stylo")
    kit.pop("rembobiner", f)
    kit.vanish("fin_du_mois", f + 3, into=list(REMBOBINER_C))
    toi.unstow(f)

    f = kit.at("S03", "vidéo,", "tout se rembobine : les 8 pièces remontent dans leurs places et la pilule, redevenue "
                                "cyan, recompte jusqu'à « 800 € » ; le ◀◀ disparaît")
    kit.fade("solde_alerte", f + 1, to=0, d=4)
    S.key("solde", "fill", f, CYAN.lower(), 9, "out")
    S.key("solde", "text", f + 2, euros(0))
    for i, cid in enumerate(COINS):
        g = f + 2 * i
        S.key(cid, "opacity", g, 1)
        kit.move(cid, g, list(COIN_PLACES[i]), d=12, e="out")
        S.key(CASES[i], "opacity", g + 9, 0)
        S.key("solde", "text", g + 9, euros(100 * (i + 1)))
    assert S.val("solde", "text", f + 30) == T_800
    kit.vanish("rembobiner", f + 12)

    f = kit.at("S03", "solde", "un trait cyan profond se tire sous « Solde »")
    kit.draw("solde_titre", f, DRAW, track="under")

    f = kit.at("S03", "budget.", "« ≠ » surgit à droite du téléphone ; un cadre vide en tirets surgit, titré "
                                 "« Budget » avec un calendrier")
    kit.pop("neq", f)
    kit.pop("budget", f)
    kit.fade("budget_titre", f + 3)
    kit.fade("budget_cal", f + 3)

    # ================= S04 : trois pièges -> repère 1-2-3 ; le panier arrêté par « ≠ » =================
    f = kit.at("S04", "trois", "trois alertes sortent du centre du cadre « Budget » et s'alignent dedans")
    for k in range(3):
        kit.pop(f"alerte{k + 1}", f + 3 * k, from_pt=list(BUDGET_C), to=list(ALERTES_C[k]))

    f = kit.at("S04", "éviter", "les trois alertes montent en haut et deviennent les disques du repère 1-2-3 "
                                "légendé « Échéances », « Différés », « Virements » (aucun disque actif)")
    for k in range(3):
        kit.move(f"alerte{k + 1}", f, list(MARKER_DISC[k]), d=10, e="inOut", scale=20 / 34)
    kit.pop("marqueur", f + 7)
    for k in range(3):
        kit.vanish(f"alerte{k + 1}", f + 10, d=6)
    assert f + 16 <= S.word_after("dépenser", f), f

    f = kit.at("S04", "dépenser.", "un panier naît de la pointe du stylo de « Toi » et part vers le téléphone ; il "
                                   "bute sous « ≠ », tremble et s'arrête ; « ≠ » bat")
    g = kit.pop("panier", f, from_pt=toi.tip(f - 1), to=list(PANIER_S04))
    toi.reach(f + 3, list(REACH_S04), step=False)
    g = kit.move("panier", g, list(PANIER_STOP), d=10, e="out")
    kit.shake("panier", g, amp=7)
    kit.pulse("neq", g, peak=1.25)
    assert g + 10 <= S.word_after("problème", f), g

    # ================= S05 : le chiffre ne dit rien des factures à venir =================
    f = kit.at("S05", "problème,", "« ≠ » bat deux fois ; « Toi » ramène son stylo et le panier rentre dans sa "
                                   "pointe")
    kit.pulse("neq", f, times=2, peak=1.2)
    g = toi.rest(f, 8)
    kit.vanish("panier", f, into=toi.tip(f + 9))
    S.key("panier", "pos", g + 2, list(PANIER_C))

    f = kit.at("S05", "chiffre", "la pilule « 800 € » bat deux fois : c'est ce chiffre-là")
    kit.pulse("solde", f, times=2, peak=1.15)

    f = kit.at("S05", "sortir", "trois factures tombent dans le cadre « Budget » : Loyer, Forfait, Assurance ; la "
                                "pilule ne bouge pas")
    for k, fid in enumerate(FACT_IDS):
        kit.drop(fid, f + 4 * k, h=140)

    # ================= S06 : le solde est une photo, le budget un film =================
    f = kit.at("S06", "photo.", "flash blanc sur le téléphone, et quatre coins de viseur se referment sur lui : une "
                                "photo figée")
    S.key("flash", "opacity", f, 0.85)
    S.key("flash", "opacity", f + 1, 0, 4, "linear")
    ax, ay = APPLI_C
    for k, (pos, _pts) in enumerate(VISEUR):
        v = f"viseur{k + 1}"
        S.key(v, "pos", f - 1, [round(ax + VISEUR_OPEN * (pos[0] - ax), 2), round(ay + VISEUR_OPEN * (pos[1] - ay), 2)])
        S.key(v, "scale", f, 1.25)
        S.key(v, "scale", f + 1, 1, 9, "out")
        S.key(v, "pos", f + 1, list(pos), 9, "out")

    f = kit.at("S06", "film.", "le cadre « Budget » prend un fond et deux bandes perforées : une pellicule ; puis la "
                               "bande et ses trois factures défilent vers le bas")
    kit.ensure("budget", "fillOp", 0)
    S.key("budget", "fillOp", f, 1, DRAW, "out")
    for k in range(2):
        kit.ensure(f"bande{k + 1}", "sy", 0)
        S.key(f"bande{k + 1}", "sy", f + 2, 1, DRAW, "out")
    g0 = f + 11
    f7 = scene_f0(S, "S07")
    d = f7 - 1 - g0                                       # défile jusqu'à la veille de « Pourquoi », puis s'arrête
    assert d >= 8, d
    for k in range(2):
        S.key(f"perf{k + 1}", "pos", g0, [0, FILM_DRIFT], d, "linear")
    for fid in FACT_IDS:
        x, y = S.val(fid, "pos", g0 - 1)
        S.key(fid, "pos", g0, [x, y + FILM_DRIFT], d, "linear")

    # ================= S07 : les prélèvements partent tout seuls =================
    f = kit.at("S07", "Pourquoi", "la pellicule, le viseur, « ≠ » et « Budget » se réduisent ; les trois factures "
                                  "restent")
    for x in ["budget", "viseur1", "viseur2", "viseur3", "viseur4", "neq", "budget_titre", "budget_cal"]:
        kit.vanish(x, f)

    f = kit.at("S07", "prélèvements ?", "un bac surgit à droite ; les factures y tombent, une par rangée de pièces")
    kit.pop("bac", f)
    for k, fid in enumerate(FACT_IDS):
        kit.move(fid, f + 2 * k, list(FACT_BAC[k]), d=DROP, e="out", scale=FACT_K)

    f = kit.at("S07", "partent", "de chaque facture partent tout seuls deux fils, jusqu'à ses deux pièces du "
                                 "téléphone (3 factures, 6 pièces) ; « Toi » ne bouge pas")
    for k in range(3):
        kit.draw(f"fil_mandat{k + 1}a", f + 4 * k, DRAW)
        kit.draw(f"fil_mandat{k + 1}b", f + 4 * k + 2, DRAW)

    f = kit.at("S07", "penses.", "« Toi » se retourne en entier vers la droite, dos au téléphone et au bac (son stylo "
                                 "passe de l'autre côté) et s'y tient")
    g = turn(S, toi, dos, f)
    dos.lean_to(g, 6)

    # ================= S08 : premier piège, oublier les prélèvements à venir =================
    f = kit.at("S08", "Premier", "le disque 1 du repère s'allume en cyan, « Échéances » passe en gras")
    S.key("marqueur", "on", f, 1, POP, "out")

    f = kit.at("S08", "oublier", "un volet monte sur le bac et cache les trois factures (seul le bord de « Loyer » "
                                 "dépasse) ; les six fils restent accrochés aux pièces")
    vb = BAC_H / 2 - 6
    S.keys("bac_volet", f, MOVE, "out", sy=1, pos=[0, vb - VOLET_H / 2])
    for k, fid in enumerate(FACT_IDS):
        kit.move(fid, f, list(FACT_BAC_SUNK[k]), d=MOVE, e="out")

    f = kit.at("S08", "venir.", "les six fils battent deux fois et les six pièces accrochées penchent deux fois vers "
                                "le bac : elles sont tenues")
    for w in FILS:
        g = kit.pulse(f"{w}_halo", f, times=2, peak=1, step=3, track="opacity")
    for cid in COINS[:6]:
        x, y = S.val(cid, "pos", f - 1)
        for t in range(2):
            S.keys(cid, f + 6 * t, 3, "out", pos=[x + 8, y], rot=8)
            S.keys(cid, f + 6 * t + 3, 3, "inOut", pos=[x, y], rot=0)
    assert g <= scene_f0(S, "S09") - 1, g
