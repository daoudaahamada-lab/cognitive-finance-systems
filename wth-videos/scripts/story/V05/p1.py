"""V05, partie 1 : S01-S08, images 0-952 (29 temps forts, 31,8 s). L'accroche, l'annonce, le contexte, la 1re erreur.

Revue 1 (ce qui prime sur le détail ci-dessous) : preuves « vide » renforcées (S02 « info » : faisceau de l'IA de
« mars 2027 » à la place « Vente », qui tremble 12 px / 6 images et bat x 1,15 ; S05 « manque, » : même refus, le
faisceau rentre avec un « ? » gris) ; S04 : cadre de choix épais, trois sauts juin -> janv. -> mars, dates lâchées
barrées ; S06 : maison = pictogramme sur disque, glisse sur la place « Vente » à « c’est », sort en S07 « Pourquoi » ;
S07 : la pilule « Toi » reste, les places battent 3 fois (contour épaissi), traits du nuage dès « l’IA » (marge gauche
du brief) ; S08 : fausses cartes (papier, gros pointillés, coche de l'IA) qui tombent (kit.drop) dans les places.

Temps forts (image = round(t x 30), avant calage acoustique) :
S01  agent@8  préparé@39  brief.@55
S02  Il@77  fluide,@87  complet…@105  info@141  inventée.@164
S03  Dans@193  quatre@242  rendez-vous@307  parade@353
S04  Pourquoi@381  générative@440  produire@482  plausible.@510
S05  donnée@549  manque,@558  compléter@588  aplomb.@612
S06  patrimonial,@656  c’est@685  risque.@701
S07  Pourquoi@721  vides@760  l’IA@820  invente.@836
S08  Première@864  combler@921

État d'entrée : l'état de distribution (image 0) ; rien à épingler. Dossier (170, 745) avec Relevé, place « Vente »,
Mail, place « Contrat », Compte rendu ; brief vierge (560, 750) x 0,95, 5 rangées vides (bandes beiges), pastille
sur l'en-tête ; IA (115, 1145) et sa pilule. Ni « Toi », ni repère, ni maison.

Brief, scène par scène (ids de __init__) :
- S01 « agent » : `faisceau` (pb déjà sur la chemise) se trace (DRAW). « préparé » : `extrait1/3/5` se tracent
  (200 ms), puis L1, L3, L5 s'écrivent ensemble (kit.type, chars complets) ; L2 et L4 s'écrivent jusqu'au bout de la
  clé seulement (chars = len(clé)) et `L2_case` / `L4_case` paraissent (opacity 1, ou pop) ; `faisceau` s'efface
  (piste from 0 -> 1). « brief. » : `coche_ia1/3/5` se tracent (draw, décalées de 2 images), les extraits s'effacent.
- S02 « Il » : `bulle_rond1-3` puis `nuage` surgissent ; `puce_vente`, `puce_contrat` dedans (pop). « fluide, » : les
  deux puces volent en arc (S.fly, arc 80) jusqu'à la valeur de L2 / L4 (S.to_world(Lx, VALUE_PT[i], f)) et s'y
  fondent (vanish) pendant que L2 / L4 tapent leur valeur ; `L2_case` / `L4_case` s'effacent sous la valeur.
  « complet… » : `coche_ia2/4` ; `reflet` p 0 -> 1 (400 ms) ; nuage et bulles vanish dans la tête (into « ia »).
  « info » : kit.shake(`place_vente`) (enfant du dossier : shake x 6). « inventée. » : `L2_cadre` draw 0 -> 1 puis
  pulse x 1,08. L'IA ne bouge jamais quand elle se trompe.
- S03 « Dans » : toi.enter(f, at=TOI_REST) ; `toi_pill` pop. « quatre » : `titre_erreurs` pop, `marqueur` pop (on reste
  0 : aucun disque actif). « rendez-vous » : kit.pulse(`pastille`, times=2). « parade » : `parade` pop en PARADE_S03.
- S04 « Pourquoi » : `parade` vanish ; `rembobiner` pop ; `L2_cadre` fade ; L2 / L4 chars -> len(clé) pendant que
  `puce_vente` / `puce_contrat` (posées à f-1 sur les valeurs, pop) redescendent en arc dans le `nuage` qui ressurgit ;
  `coche_ia2/4` draw 1 -> 0 ; `L2_case` / `L4_case` reparaissent. « générative » : nuage sx/sy -> NUAGE_S04_K ;
  `puce_contrat` se range dans un coin (scale 0,7) ; `puce_date1`, `puce_vente` (milieu), `puce_date3` aux
  PUCE_DATES_S04. « produire » : `cadre_choix` saute (clés instantanées, 4 images par saut) juin -> mars -> janv. ->
  mars, s'arrête ; `puce_vente` x 1,2 ; dates 1 et 3 vanish ; RIEN ne s'allume dans le dossier. « plausible. » :
  `puce_vente` vole dans L2, L2 retape sa valeur, `coche_ia2` se retrace, `rembobiner` vanish, `L2_case` s'efface.
- S05 « donnée » : `faisceau_contrat` se trace jusqu'à la place « Contrat ». « manque, » : shake(`place_contrat`) ;
  le faisceau se rétracte (from 0 -> 1). « compléter » : `puce_contrat` (bulles visibles, nuage reformé à sa taille
  S02) vole jusqu'à la valeur de L4. « aplomb. » : L4 tape d'un coup sa valeur (rate élevé) ; un `p1_…` texte
  ExtraBold relais x 1,25 -> 1 si besoin ; `coche_ia4` ; nuage et bulles vanish dans l'IA ; `L4_case` s'efface.
- S06 « patrimonial, » : kit.drop(`maison`) sur la chemise. « c’est » : pulse x 1,08 de `place_vente` (2 fois).
  « risque. » : `L2_cadre` et `L4_cadre` draw 1 (L2 déjà tracé : seulement L4 se trace, L2 bat) ; `alerte` pop.
- S07 « Pourquoi » : `alerte` et `toi_pill` vanish (les cadres restent). « vides » : `place_vente`, `place_contrat`
  battent 2 fois (x 1,08, step 4). « l’IA » : bulles + `nuage` ressortent, vide. « invente. » : `trace_vente`,
  `trace_contrat` se tracent du nuage vers les valeurs (DRAW).
- S08 « Première » : S.key("marqueur", "on", f, 1, POP) (le disque 1 « Vides » grandit). « combler » : les traces se
  rétractent (from 0 -> 1) ; `fantome_vente` / `fantome_contrat` sortent du nuage (pop depuis NUAGE_C, puis vol
  jusqu'à leur place, rot -6 / +5 déjà posée, décalées de 3 images) ; nuage et bulles vanish dans l'IA.

Raccord vers p2 : à la dernière image (952), l'état est exactement ENTRY_P2 (__init__.py) : valeurs écrites et
cochées par l'IA, cadres rouges tracés sur L2 et L4, fausses cartes dans les places, repère « on » sur 1, titre,
pastille ; nuage, puces, alerte, parade, pilule « Toi », faisceaux et traces à 0. « Toi » au repos (TOI_REST).
"""
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, SCALE, STYLE  # noqa: F401

from . import (CASE_VAL_PT, ENTRY_P2, LINES, MAISON_VENTE, NUAGE_C, NUAGE_S04_C, NUAGE_S04_K, PARADE_S03,  # noqa: F401
               PUCE_DATES_S04, PUCE_S02, T_250, TOI_REST, VALUE_PT, scene_f0, seam, vanish)

L_KEY = [len(k) for k, _, _ in LINES]                 # chars d'une ligne qui n'a que sa clé
L_FULL = [len(k) + len(v) for k, v, _ in LINES]
CONTRAT_COIN = (565, 1150)                            # S04 : « 250 000 € » rangée à droite du nuage agrandi (32 px)
SHAKE_BIG = [12, -10, 8, -6, 3, 0]                    # revue 1 : preuve « vide » aussi forte que le verdict (6 images)


def shake_big(S, id, f):
    """Secousse x de 12 px sur 6 images (clés instantanées). -> f + 6."""
    x, y = S.val(id, "pos", f - 1)
    for k, dx in enumerate(SHAKE_BIG):
        S.key(id, "pos", f + k, [round(x + dx, 2), y])
    return f + len(SHAKE_BIG)


def proof_empty(S, kit, place, f):
    """Une place vide refuse : secousse 12 px / 6 images, et elle bat deux fois x 1,15 (contour et pictogramme)."""
    shake_big(S, place, f)
    return kit.pulse(place, f, times=2, peak=1.15, step=3)
AI_RATE = 3.5                                         # vitesse d'écriture de l'IA (car. par image)


def part(S, kit, c):
    toi = c.toi
    kit.pin(0 - 1, {"fiche": {"opacity": 1}})         # état de distribution : rien à imposer

    def head(n):
        """Avant du cerveau de verre de l'IA (monde) : d'où partent et où rentrent nuage et bulles."""
        return S.to_world("ia", c.brain_front, n)

    def value_w(i, n):
        """Centre monde de la valeur de la ligne i (ligne de texte)."""
        return S.to_world(c.lines[i], VALUE_PT[i], n)

    def type_value(i, f, rate=AI_RATE):
        """La ligne i passe de sa clé seule à clé + valeur (l'IA écrit la valeur). -> image de fin."""
        n = L_FULL[i] - L_KEY[i]
        S.key(c.lines[i], "chars", f, L_FULL[i], n / rate, "linear")
        return round(f + n / rate)

    home = {x: S.val(x, "pos", 0) for x in ("nuage", "bulle_rond1", "bulle_rond2", "bulle_rond3")}

    def cloud_in(f):
        """Les trois petites bulles montent de la tête de l'IA, puis le nuage surgit. -> fin du pop du nuage."""
        for k in range(3):
            b = f"bulle_rond{k + 1}"
            kit.pop(b, f + k, from_pt=head(f + k - 1), to=home[b], d=6)
        return kit.pop("nuage", f + 1, from_pt=head(f), to=home["nuage"])

    def cloud_out(f):
        """Nuage et bulles se réduisent dans la tête de l'IA. -> fin."""
        end = vanish(kit, "nuage", f, into=head(f), d=POP)
        for k in range(3):
            end = max(end, vanish(kit, f"bulle_rond{3 - k}", f + k, into=head(f), d=6))
        return end

    # relais « avec aplomb » (S05) : la valeur de L4 en ExtraBold, qui grossit puis se pose ; rendu à L4 avant S06
    kit.text("p1_aplomb", list(VALUE_PT[3]), T_250, size=32, weight=800, z=9.6, parent="L4", scale=0)

    # ================= S01 : l'IA lit le dossier et écrit le brief ; deux lignes sans valeur =================
    f = kit.at("S01", "agent", "un faisceau pointillé gris part de la tête de l'IA et se pose au milieu du dossier")
    kit.draw("faisceau", f, DRAW)

    f = kit.at("S01", "préparé", "de Relevé, Mail et Compte rendu part un petit trait pointillé vers sa rangée ; "
                                 "L1, L3, L5 s'écrivent ; L2 « Vente : » et L4 « Contrat : » n'ont que leur clé "
                                 "et une case de valeur vide en tirets ; le faisceau rentre dans le dossier")
    for k, i in enumerate((0, 2, 4)):
        kit.draw(f"extrait{i + 1}", f, 6)
    for i in (0, 2, 4):
        kit.type(c.lines[i], f + 4, rate=AI_RATE)
    for i in (1, 3):
        kit.type(c.lines[i], f + 4, n=L_KEY[i], rate=AI_RATE)
        kit.fade(f"{c.lines[i]}_case", f + 6, to=1)
    kit.draw("faisceau", f + 4, DRAW, track="from")
    S.key("faisceau", "draw", f + 14, 0)
    S.key("faisceau", "from", f + 14, 0)

    f = kit.at("S01", "brief.", "la coche pointillée de l'IA se trace au bout de L1, L3 et L5 ; les petits traits "
                                "rentrent dans les rangées")
    for k, i in enumerate((0, 2, 4)):
        kit.draw(f"coche_ia{i + 1}", f + 2 * k, 5)
        kit.draw(f"extrait{i + 1}", f, 6, track="from")
        S.key(f"extrait{i + 1}", "draw", f + 7, 0)
        S.key(f"extrait{i + 1}", "from", f + 7, 0)

    # ================= S02 : le nuage comble les deux vides ; tout est coché ; « mars 2027 » cerclé =================
    f = kit.at("S02", "Il", "trois petites bulles montent de la tête de l'IA et un nuage pointillé surgit à sa "
                            "droite, avec « mars 2027 » et « 250 000 € » dedans")
    cloud_in(f)
    for k, pid in enumerate(("puce_vente", "puce_contrat")):
        kit.pop(pid, f + 3 + k, d=7)

    f = kit.at("S02", "fluide,", "les deux puces quittent le nuage et montent en arc jusqu'aux cases vides de L2 et "
                                 "L4 ; L2 et L4 s'écrivent « mars 2027 » et « 250 000 € », les cases disparaissent")
    for pid, i in (("puce_vente", 1), ("puce_contrat", 3)):
        S.fly(pid, f, MOVE, "inOut", to=value_w(i, f), arc=80)
        type_value(i, f + 12)
        kit.fade(f"{c.lines[i]}_case", f + 12, to=0)
        vanish(kit, pid, f + 13, d=5)

    f = kit.at("S02", "complet…", "la coche pointillée de l'IA se trace au bout de L2 et L4 ; un reflet blanc "
                                  "balaie la page ; le nuage rentre dans la tête de l'IA")
    kit.draw("coche_ia2", f, 5)
    kit.draw("coche_ia4", f + 2, 5)
    S.key("reflet", "p", f, 1, 12, "linear")
    S.key("reflet", "p", f + 13, 0)
    cloud_out(f + 4)

    f = kit.at("S02", "info", "un faisceau pointillé de l'IA file de « mars 2027 » à la place en tirets « Vente » du "
                              "dossier : vide, elle tremble fort et bat deux fois ; le faisceau rentre bredouille")
    g = kit.draw("p1_cherche", f, 6)
    proof_empty(S, kit, "place_vente", g - 1)
    kit.draw("p1_cherche", g + 5, 8, track="from", e="inOut")
    S.key("p1_cherche", "draw", g + 13, 0)
    S.key("p1_cherche", "from", g + 13, 0)

    f = kit.at("S02", "inventée.", "un cadre rouge se trace autour de « mars 2027 » et bat une fois")
    g = kit.draw("L2_cadre", f, DRAW)
    kit.pulse("L2_cadre", g, peak=1.08)

    # ================= S03 : « Toi », les 4 erreurs, le rendez-vous, la parade =================
    f = kit.at("S03", "Dans", "« Toi », la figurine encre, surgit au repos en bas à droite avec sa pilule « Toi »")
    toi.enter(f, at=list(TOI_REST))
    kit.pop("toi_pill", f + 3)

    f = kit.at("S03", "quatre", "le titre « 4 erreurs » surgit en haut, puis le repère à 4 disques légendés "
                                "(Vides, Source, Hypothèse, Diagonale), aucun disque actif")
    kit.pop("titre_erreurs", f)
    kit.pop("marqueur", f + 3)

    f = kit.at("S03", "rendez-vous", "la pastille « Client · 10 h » bat deux fois sur l'en-tête du brief")
    kit.pulse("pastille", f, times=2)

    f = kit.at("S03", "parade", "une pilule « Parade » au bouclier surgit dans la marge basse du brief")
    kit.pop("parade", f)

    # ================= S04 : rembobinage ; trois dates ; choix au jugé ; « mars 2027 » réécrite =================
    f = kit.at("S04", "Pourquoi", "la Parade se réduit, un ◀◀ surgit ; le cadre rouge s'efface ; « mars 2027 » et "
                                  "« 250 000 € » quittent L2 et L4 et redescendent dans le nuage qui ressurgit ; "
                                  "les coches de L2 et L4 se rétractent, les cases vides reviennent")
    vanish(kit, "parade", f)
    kit.pop("rembobiner", f)
    kit.fade("L2_cadre", f, to=0)
    cloud_in(f)
    for pid, i in (("puce_vente", 1), ("puce_contrat", 3)):
        S.key(c.lines[i], "chars", f, L_KEY[i], 3, "linear")
        kit.pop(pid, f, d=6)
        S.key(f"coche_ia{i + 1}", "draw", f, 0, 6, "in")
        kit.fade(f"{c.lines[i]}_case", f + 3, to=1)
    for pid in ("puce_vente", "puce_contrat"):
        S.fly(pid, f + 6, MOVE, "inOut", to=list(PUCE_S02[pid]), arc=40)

    f = kit.at("S04", "générative", "le nuage grandit ; « 250 000 € » se range à son bord ; trois dates y surgissent "
                                    "l'une sous l'autre : « juin 2026 », « mars 2027 », « janv. 2028 »")
    kx, ky = NUAGE_S04_K
    S.keys("nuage", f, SCALE, "out", sx=round(kx, 4), sy=round(ky, 4))
    kit.move("nuage", f, list(NUAGE_S04_C), d=SCALE, e="out")           # il grandit vers le haut (sous-titres)
    kit.move("puce_contrat", f, list(CONTRAT_COIN), d=SCALE, e="out", arc=30)
    kit.move("puce_vente", f + 2, list(PUCE_DATES_S04[1]), d=SCALE, e="out")
    kit.pop("puce_date1", f + 4)
    kit.pulse("puce_vente", f + 7, peak=1.08)
    kit.pop("puce_date3", f + 10)

    f = kit.at("S04", "produire", "un épais cadre pointillé de l'IA saute de date en date : « juin 2026 » (barrée en "
                                  "le quittant), « janv. 2028 » (barrée), puis s'arrête sur « mars 2027 », qui "
                                  "grandit ; les dates barrées disparaissent ; rien ne s'allume dans le dossier")
    hop = 7                                                             # trois atterrissages, trois battements
    kit.pop("cadre_choix", f, d=3)
    kit.pulse("puce_date1", f + 1, peak=1.08, step=2)
    S.key("cadre_choix", "pos", f + hop, list(PUCE_DATES_S04[2]))
    kit.pulse("cadre_choix", f + hop, peak=1.08, step=2)
    kit.pulse("puce_date3", f + hop, peak=1.08, step=2)
    kit.draw("puce_date1_barre", f + hop, 4)
    S.key("cadre_choix", "pos", f + 2 * hop, list(PUCE_DATES_S04[1]))
    kit.pulse("puce_vente", f + 2 * hop, peak=1.08, step=2)
    kit.draw("puce_date3_barre", f + 2 * hop, 4)
    g = f + 2 * hop + 3
    S.key("puce_vente", "scale", g, 1.2, 8, "out")
    S.key("cadre_choix", "scale", g, 1.2, 8, "out")
    vanish(kit, "puce_date1", g + 4, d=6)
    vanish(kit, "puce_date3", g + 4, d=6)

    f = kit.at("S04", "plausible.", "« mars 2027 » quitte le nuage et remonte en arc dans L2, qui la réécrit, et "
                                    "la coche pointillée de l'IA se retrace ; le ◀◀ se réduit")
    vanish(kit, "cadre_choix", f, d=6)
    S.fly("puce_vente", f, MOVE, "inOut", to=value_w(1, f), arc=80)
    S.key("puce_vente", "scale", f, 1, 12, "inOut")
    vanish(kit, "rembobiner", f + 2)
    S.keys("nuage", f + 6, SCALE, "inOut", sx=1, sy=1)                  # le nuage reprend sa taille (S05)
    kit.move("nuage", f + 6, list(NUAGE_C), d=SCALE, e="inOut")
    kit.move("puce_contrat", f + 6, list(NUAGE_C), d=SCALE, e="inOut", arc=30)
    type_value(1, f + 12)
    kit.fade("L2_case", f + 12, to=0)
    vanish(kit, "puce_vente", f + 13, d=5)
    kit.draw("coche_ia2", f + 17, 5)

    # ================= S05 : le faisceau cherche le contrat ; la place est vide ; « 250 000 € » avec aplomb ======
    f = kit.at("S05", "donnée", "un faisceau pointillé part de la tête de l'IA et monte se poser sur la place vide "
                                "« Contrat » du dossier")
    kit.draw("faisceau_contrat", f, DRAW)

    f = kit.at("S05", "manque,", "la place « Contrat » tremble fort et bat deux fois, vide ; le faisceau se rétracte "
                                 "depuis la place et ramène un « ? » gris jusqu'à la tête de l'IA : bredouille")
    proof_empty(S, kit, "place_contrat", f)
    r0 = f + 6
    S.key("faisceau_contrat", "draw", r0, 0, 10, "inOut")
    S.key("p1_vide", "pos", r0 - 4, [round(v, 2) for v in S.wire_cubic("faisceau_contrat", r0 - 1)[3]])
    kit.pop("p1_vide", r0 - 3, d=3)
    S.along_wire("p1_vide", "faisceau_contrat", r0, 10, "inOut", 1, 0, r0 - 1)
    kit.pulse("p1_vide", r0 + 10, peak=1.3, step=3)
    vanish(kit, "p1_vide", r0 + 17, into=head(r0 + 17), d=6)

    f = kit.at("S05", "compléter", "« 250 000 € » sort du nuage, encore relié à la tête de l'IA par les bulles, et "
                                   "monte en arc jusqu'à la case vide de L4")
    S.fly("puce_contrat", f, MOVE, "inOut", to=value_w(3, f), arc=80)

    f = kit.at("S05", "aplomb.", "L4 s'écrit d'un coup « 250 000 € » en gras, qui grossit puis se pose ; la coche "
                                 "pointillée de l'IA se trace ; le nuage rentre dans la tête de l'IA")
    vanish(kit, "puce_contrat", f, d=4)
    kit.fade("L4_case", f, to=0, d=3)
    S.key("p1_aplomb", "scale", f, 1.25)
    S.key("p1_aplomb", "scale", f + 1, 1, SCALE, "out")
    kit.draw("coche_ia4", f + 6, 5)
    cloud_out(f + 10)
    sw = f + 16                                                         # relais rendu à la ligne L4
    S.key("L4", "chars", sw, L_FULL[3])
    kit.fade("p1_aplomb", sw, to=0, d=4)
    S.key("p1_aplomb", "scale", sw + 4, 0)

    # ================= S06 : la maison du client ; la vente non datée ; le risque =================
    f = kit.at("S06", "patrimonial,", "une maison (pictogramme encre sur disque) tombe sur le haut du dossier")
    kit.drop("maison", f, h=150)

    f = kit.at("S06", "c’est", "la maison glisse et se pose sur le coin de la place vide « Vente » ; la place tremble "
                               "fort et bat deux fois : cette vente n'a pas de date")
    g = kit.move("maison", f, list(MAISON_VENTE), d=8, e="inOut")
    shake_big(S, "place_vente", g - 2)
    kit.pulse("place_vente", g - 2, times=2, peak=1.15, step=2)

    f = kit.at("S06", "risque.", "un cadre rouge se trace autour de « mars 2027 » et de « 250 000 € », puis les "
                                 "deux battent ; un grand disque d'alerte rouge surgit à droite du brief")
    S.key("L2_cadre", "draw", f - 1, 0)
    S.key("L2_cadre", "opacity", f - 1, 1)
    g = kit.draw("L2_cadre", f, DRAW)
    kit.draw("L4_cadre", f, DRAW)
    kit.pulse("L2_cadre", g, peak=1.08)
    kit.pulse("L4_cadre", g, peak=1.08)
    kit.pop("alerte", f + 3)

    # ================= S07 : les vides du dossier ; c'est là que l'IA invente =================
    f = kit.at("S07", "Pourquoi", "le disque d'alerte et la maison se réduisent ; les cadres rouges restent")
    vanish(kit, "alerte", f)
    vanish(kit, "maison", f + 2)

    f = kit.at("S07", "vides", "les places vides « Vente » et « Contrat » battent trois fois (x 1,15), leur contour en "
                               "tirets s'épaissit à chaque battement ; elles restent vides")
    for pid in ("place_vente", "place_contrat"):
        kit.pulse(pid, f, times=3, peak=1.15, step=5)
        kit.pulse(f"{pid}_hi", f, times=3, peak=1, step=5, track="opacity")

    f = kit.at("S07", "l’IA", "les petites bulles puis le nuage ressortent de la tête de l'IA, vide ; deux traits "
                              "pointillés en partent, longent la marge du brief et se tracent jusqu'à « mars 2027 » et "
                              "« 250 000 € »")
    g = cloud_in(f)
    kit.draw("trace_vente", g - 2, DRAW + 3)
    kit.draw("trace_contrat", g, DRAW + 3)

    f = kit.at("S07", "invente.", "les deux cadres rouges battent fort, au bout des traits venus du nuage")
    kit.pulse("L2_cadre", f, peak=1.15, step=3)
    kit.pulse("L4_cadre", f + 1, peak=1.15, step=3)

    # ================= S08 : 1 · Vides : de fausses cartes bouchent les trous du dossier =================
    f = kit.at("S08", "Première", "le disque 1 « Vides » du repère grandit et se remplit de cyan ; sa légende paraît")
    S.key("marqueur", "on", f, 1, POP, "out")

    f = kit.at("S08", "combler", "les traits pointillés rentrent dans le nuage ; deux fausses cartes (papier, gros "
                                 "pointillés de l'IA, sa coche à la place du pictogramme) en sortent, volent en arc et "
                                 "tombent de travers dans les places « Vente » et « Contrat », qui encaissent le choc ; "
                                 "le nuage rentre dans la tête de l'IA")
    for wid in ("trace_vente", "trace_contrat"):
        S.key(wid, "draw", f, 0, 6, "in")
    for k, (fid, place) in enumerate((("fantome_vente", "place_vente"), ("fantome_contrat", "place_contrat"))):
        g = f + 2 + 3 * k
        at = S.val(fid, "pos", g - 1)
        S.key(fid, "pos", g - 1, list(NUAGE_C))
        S.key(fid, "scale", g - 1, 0)
        S.key(fid, "scale", g, 1, POP, "out")
        S.key(fid, "pos", g, [at[0], at[1] - 70], 12, "inOut", 70)
        land = kit.drop(fid, g + 12, h=70, to=list(at))
        kit.shake(place, land - 3, amp=5, axis="y")
    end = cloud_out(f + 17)
    assert end <= seam(S, "S09"), end
