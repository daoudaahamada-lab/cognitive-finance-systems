"""V10, partie 3 : S16-S22, images 1851-2848 (piège 3 : la façade ; les signaux d'alerte ; la bouée ; la chute ;
la fin standard). 35 temps forts, 33,3 s. FILM_END = 2849.

ÉTAT D'ENTRÉE (etat_initial de S16, à épingler à 1850 : `kit.pin(f0 - 1, ENTRY_P3)` avec f0 = scene_f0(S, "S16")) :
liste noire au centre (ligne « Invest Minuit » rouge), horloge « 2 min » à droite, champ « Invest Minuit » devant
« Toi », fil rouge vers le verdict ; « Non autorisé » rouge au-dessus de l'interlocuteur ; offre réduite en haut à
gauche ; pastille libre en PASTILLE_LIBRE (780, 420) ; repère sur 2 (1 coché) ; « Toi » en P_FAR (880), bras
baissé. Garde-fous figurines (partie isolée seulement) : `if S.val("interlocuteur", "scale", f0 - 1) == 0:
c.inter.enter(f0 - 10, at=INTER_POS)` ; `if abs(S.val("toi", "pos", f0 - 1)[0] - P_FAR[0]) > 1:
walk_low(c.toi, f0 - 40, P_FAR[0], d=30)`.

Temps forts (image du mot, calage acoustique compris ; « Site » tombe 1 image avant S17) :
S16  Mais@1851  soignent@1902  apparences.@1919  Troisième@1952  l’image.@2007
S17  Site@2033  soigné,@2047  faux@2072  institution@2133  conseiller@2172
S18  Fie-toi@2226  plutôt@2236  signaux@2252  d’alerte.@2262  rendement@2288  garanti.@2320
S19  contact@2348  paiement@2405  compte@2456  l’étranger.@2467
S20  Au@2496  doute,@2513  contacte@2532  Assurance@2547  Banque@2563  Info@2591  Service.@2602
S21  Et@2629  retiens :@2632  opportunité@2659  refuse@2684  mérite@2724  argent.@2743
S22  Abonne-toi@2765  argent.@2810

BRIEF, scène par scène (constantes et helpers de __init__ ; ids entre {}) :
- S16 « Mais » : kit.morph(["liste_noire", "horloge", "horloge_2min"], [], f) (décalés de 2 images) ; fil_recherche
  from 0 -> 1 (9) ; kit.vanish("champ", f, into=pointe) ; walk_low(c.toi, f, P3[0]) (880 -> 650, ≈ 33 images ; le
  champ rentre dans le stylo pendant la marche : into = c.toi.tip(f + POP)). « soignent » : kit.pop("telephone", f)
  (écran vide). « apparences. » : kit.drop("conseiller", f) : il couvre « Non autorisé » (enfant de l'interlocuteur,
  même place). « Troisième » : kit.step(f, 2) ; done1 0 -> 1. « l’image. » : c.toi.lean_to(f, -8, TILT) (vers le
  téléphone) ; MÊME image : kit.draw("crochet_tel", f, 9), kit.pop("crochet_j", f + 7, d=4) (opacity 1 : il était
  tombé en S15), kit.move("pastille", f + 9, PASTILLE_TEL, d=9) ; telephone stroke INK -> RED -> INK (2 x 5).
- S17 « Site » : kit.pop("site_bandeau", f) puis kit.stagger(c.site_blocs, f + 2, 2, kit.pop). « soigné, » :
  tel_reflet p 0 -> 1 (12, linear). « faux » : kit.morph(c.site_blocs, c.site_avis, f) puis les étoiles :
  kit.stagger(sum(c.site_etoiles, []), f + 6, 1, kit.pop, d=6). « institution » : kit.drop("site_banque", f, h=120)
  (collée PAR-DESSUS « Invest Minuit ») ; MÊME image kit.pulse("nom_inter", f, peak=1.1) : c'est toujours lui.
  « conseiller » : kit.pop("sourire", f, from_pt=tête de l'interlocuteur) ; c.inter.lean_to(f, 8, TILT).
- S18 « Fie-toi » : c.toi.lean_to(f, 0) (se redresse). « plutôt » : hit = c.toi.tap(f - TAP + 1, PHONE_TAP) (contact
  sur le mot) ; drag(c.toi, hit + 1, 9, PHONE_TAP, PHONE_PULL)… NON : ici la pointe tire vers le BAS, le corps ne
  bouge pas : c.toi.trace(hit + 1, [PHONE_TAP, PHONE_PULL], speed=8) ; « site » suit la pointe (kit.move 60 px vers le
  bas, mêmes images) puis kit.drop("site", fin, out=True, h=200, rot=10) (le masque tombe) ; au même moment
  kit.pop("tel_vrai_nom") : le vrai nom, rouge. « signaux » : kit.vanish("sourire") ; c.inter.lean_to(f, 0) ;
  kit.drop("conseiller", f, out=True) : « Non autorisé » réapparaît. « d’alerte. » : crochet_tel dashed 1 puis
  kit.drop out ; kit.drop("crochet_j", f, out=True) ; kit.move("pastille", f, PASTILLE_LIBRE, d=12) +
  kit.pulse(peak=1.08) ; kit.pop("tel_alerte", f). lower(c.toi). « rendement » : kit.pop("alerte1", f, from_pt=TEL_C)
  + glisse vers ALERTE_C[0] (MOVE). « garanti. » : kit.draw("alerte1_l3", f, 8, track="under") ; kit.pulse alerte1.
- S19 « contact » : alerte2 comme alerte1 (vers ALERTE_C[1]) ; kit.shake rot ±12° de alerte2_ico (sonnerie, 3 fois).
  « paiement » : alerte3. « compte » : alerte4. « l’étranger. » : kit.stagger(c.alertes, f, 2, kit.pulse,
  peak=1.05). Puis plus rien ne bouge jusqu'à S20 (≈ 0,9 s).
- S20 « Au » : kit.stagger(["telephone"] + c.alertes, f, 2, kit.vanish, into=(MARKER_XS[2], MARKER_Y)).
  « doute, » : kit.pop("question", f) en Q_TETE_P3 (gs Q_GS ; scale 0 avant). « contacte » : hit =
  c.toi.tap(f - TAP + 1, COMBINE_C) ; kit.pop("combine", hit) ; fil_appel draw 0 -> 1 (9). « Assurance » :
  kit.drop("bouee", f) (au bout du fil). « Banque » : kit.type("bouee_nom1", f, rate=3), kit.type("bouee_nom2", …
  à la suite). « Info » : kit.drop("amf_bouee", f) : le sceau officiel. « Service. » : kit.move("question", f,
  COCHE_BOUEE_C, d=14, arc=80) puis à l'arrivée question scale 0 et kit.draw("coche_bouee", arrivée, 6). lower.
- S21 « Et » : kit.morph(["bouee", "bouee_nom1", "bouee_nom2", "amf_bouee", "coche_bouee", "combine", "fil_appel"],
  [], f) (fil : draw 1 -> 0 ou opacity). « retiens : » : marqueur done2 0 -> 1 (stagger 4 images avec un battement des
  coches déjà faites ; pas de nouveau glissement). « opportunité » : kit.move("offre", f, OFFRE_C, scale=1) (MOVE) ;
  la barre reprend sa fonte. « refuse » : kit.pop("champ", f, from_pt=pointe, to=CHAMP_S21, scale=CHAMP_S21_K) puis
  il monte vers la case de l'offre ; {compte_rebours} glisse de BAR_DROP px vers le bas (6) devant lui : le champ
  rebondit de 60 px (9, out) ; case_offre stroke DEEP -> RED (6) + kit.pulse : c'est l'offre qui bloque.
  « mérite » : end = c.toi.strike(f, a, b, line="trait_refus", track="draw") avec a, b = points monde de TRAIT_PTS
  (S.to_world("compte_rebours", pt, f)) ; puis kit.drop("offre", end, out=True, h=900, rot=-20, d=18) (tout tombe,
  trait compris) ; c.inter.exit(end) (nom, verdict, conseiller : ses enfants) ; kit.vanish("champ", end,
  into=pointe). « argent. » : kit.move("pastille", f, PASTILLE_FIN, d=21, scale=PASTILLE_FIN_K) puis kit.pulse ;
  lower(c.toi).
- S22 « Abonne-toi » : fin standard comme V08 p3 : `out = kit.outro("S22", outs=["marqueur", "nom_toi"],
  btn_at=MOVE, press="argent.", pos=FIN_C, clear="fade")` ; S.set(out["cursor"], opacity=0) (aucun pointeur) ;
  pastille z 41, textOp 0 -> « S’abonner » -> 1, w -> BTN_W / BTN_K, kit.move vers FIN_BUTTON (scale BTN_K), opacity 0
  à l'arrivée (relais exact du bouton). « argent. » : c.toi.set_z(…, tool_z=44) ; hit = c.toi.tap(press - TAP + 1,
  FIN_TAP) (== out["press"]) ; ring(S, oid, hit + 4 k, d=14, s0=0.6, s1=2.0) pour c.fin_ondes ; lower. Puis plus rien
  ne bouge jusqu'à 2848 (assert : tout fini avant FILM_END).

ÉCARTS (revue 1) : « Toi » reste en P_FAR pendant S16-S17 et marche vers P3 sur « l'image. » (il se fie à l'image :
il va vers le téléphone, et le crochet reprend l'argent) ; la façade suit la pointe puis tombe, le bras ne redescend
qu'après ; chaque carte d'alerte (pictogramme d'abord) lance une flèche rouge sur la pastille avant de se ranger ;
S20 : appel par ondes (pas de fil), « ? » qui suit les ondes et devient la coche, sceau « AMF » venu de la place qu'il
avait sur la liste noire ; S21 : l'interlocuteur sort à pied sur « retiens : » (ses étiquettes croisaient la barre),
l'offre revient à l'échelle 1 avec ses enfants (sauf les légendes, que la barre baissée couvrirait), le champ à pleine
taille monte vers la case, la barre descend dans sa course et le repousse (choc), la case rougit (✕) ; 0,6 s plus
tard « Toi » barre la barre, l'offre sort entière par la gauche ; S22 : carte 40 px plus haut.
"""
import math

from . import *  # noqa: F401,F403
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, STRETCH, TILT  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401

MARK3 = (MARKER_XS[2], MARKER_Y)                 # disque « 3 » du repère : le piège 3 s'y range (S20)
PHONE_HOVER = (PHONE_TAP[0] + 8, PHONE_TAP[1] + 20)   # S18 « Fie-toi » : le stylo se lève vers le bas de l'écran
PEN_DOWN = (560, 1180)                           # S18 : la pointe redescend le long du corps (pas de balayage)
FIELD_TIP = (560, 1040)                          # S21 « refuse » : le champ sort de la pointe
BAR_BOTTOM = OFFRE_C[1] + BAR_LOCAL[1] + BAR_H / 2 + BAR_DROP     # 978 : bas de la barre baissée
CHAMP_HIT_Y = round(BAR_BOTTOM + CHAMP_H / 2)    # 1010 : le champ bute sur la barre baissée
CHAMP_BACK_Y = CHAMP_HIT_Y + 80                  # puis rebondit de 80 px
INTER_OUT_X = -150                               # S21 : l'interlocuteur sort à pied par la gauche
OFFRE_OUT = (-560, 940)                         # S21 : l'offre barrée sort entière par la gauche
COIN_BACK = ["offre_ligne", "case_offre", "horloge_cr"]   # S21 : ce qui revient


def rnd(p):
    return [round(v, 2) for v in p]


def part(S, kit, c):
    toi, inter = c.toi, c.inter
    f0 = scene_f0(S, "S16")
    kit.pin(f0 - 1, ENTRY_P3)
    # garde-fous (partie construite seule) : sans effet dans le film entier
    if S.val("interlocuteur", "scale", f0 - 1) == 0:
        inter.enter(f0 - 10, at=INTER_POS)
    if abs(S.val("toi", "pos", f0 - 1)[0] - P_FAR[0]) > 1:
        walk_low(toi, f0 - 40, P_FAR[0], d=30)
    if S.val("compte_rebours", "sx", f0 - 1) == 0:       # offre telle que p1 la laisse (barre, légendes, horloge)
        kit.pin(f0 - 1, {"compte_rebours": {"sx": 1, "value": 0.35}, "offre_ligne": {"chars": len(T_OFFRE_LIGNE)},
                         "cr_maintenant": {"opacity": 1}, "cr_minuit": {"opacity": 1}})
    for pt, what in ((PHONE_TAP, "bas de l'écran"), (PHONE_PULL, "façade tirée"), (COMBINE_C, "combiné"),
                     (FIN_TAP, "bouton de fin"), (FIELD_TIP, "champ S21"), ((528, 928), "bout de la barre baissée")):
        assert_reach(P3[0], pt, what)

    # ---------------- S16 « Mais les escrocs le savent… Troisième piège : te fier à l’image. » ----------------
    f = kit.at("S16", "Mais", "la liste noire, l'horloge et « 2 min » se réduisent, le fil rouge rentre ; le champ "
                              "rentre dans la pointe du stylo de « Toi »")
    for k, oid in enumerate(["liste_noire", "horloge", "horloge_2min"]):
        kit.vanish(oid, f + 2 * k, d=MORPH)
    g = kit.draw("fil_recherche", f, 9, track="from")
    S.key("fil_recherche", "draw", g, 0)
    S.key("fil_recherche", "from", g, 0)
    kit.vanish("champ", f, into=rnd(toi.tip(f - 1)))

    f = kit.at("S16", "soignent", "un grand téléphone surgit à côté de l'interlocuteur ; le bandeau cyan « Invest "
                                  "Minuit » s'affiche aussitôt sur l'écran")
    g = kit.pop("telephone", f)
    kit.pop("site_bandeau", g - 3)

    f = kit.at("S16", "apparences.", "une pilule « Conseiller » tombe sur « Non autorisé » et le cache")
    drop_in(kit, "conseiller", f, h=160)

    f = kit.at("S16", "Troisième", "repère : le disque actif glisse sur « 3 · Apparence », l'étape 2 se coche")
    kit.step(f, 2)
    S.key("marqueur", "done1", f, 1, 9, "out")

    f = kit.at("S16", "l’image.", "« Toi » marche vers le téléphone ; un crochet rouge part du téléphone, se plante "
                                  "dans la pastille « Ton argent » et la tire contre l'écran ; le téléphone bat en rouge")
    walk_low(toi, f, P3[0])
    kit.draw("crochet_tel", f, 9)
    S.key("crochet_j", "pos", f - 1, list(PASTILLE_HOOK_LOCAL))
    S.key("crochet_j", "rot", f - 1, 0)
    kit.pop("crochet_j", f + 7, d=4)
    g = kit.move("pastille", f + 9, list(PASTILLE_TEL), d=14)
    kit.shake("pastille", g, amp=-5)                         # la pastille, tirée, tressaute au bout du crochet
    kit.pulse("crochet_j", g, peak=1.25)                     # le crochet mord : battement rouge
    S.key("telephone", "stroke", f, RED, 5)
    S.key("telephone", "stroke", f + 5, INK, 5)

    # ---------------- S17 « Site soigné, faux témoignages, nom proche d’une institution… » ----------------
    f = kit.at("S17", "Site", "sous le bandeau « Invest Minuit », trois blocs du site s'affichent un à un")
    kit.pulse("site_bandeau", f, peak=1.06)
    kit.stagger(c.site_blocs, f + 2, 2, kit.pop)

    f = kit.at("S17", "soigné,", "un reflet blanc balaie l'écran en diagonale")
    S.key("tel_reflet", "p", f, 1, 12, "linear")

    f = kit.at("S17", "faux", "les blocs deviennent trois avis ; cinq étoiles cyan se posent une à une sur chacun")
    kit.morph(c.site_blocs, c.site_avis, f)
    kit.stagger(sum(c.site_etoiles, []), f + 6, 1, kit.pop, d=6)

    f = kit.at("S17", "institution", "une étiquette « Banque Nationalis » tombe par-dessus « Invest Minuit » sur le "
                                     "site ; au même moment la pilule « Invest Minuit » de l'interlocuteur bat")
    drop_in(kit, "site_banque", f, h=120)
    kit.pulse("nom_inter", f, peak=1.1)

    f = kit.at("S17", "conseiller", "une bulle souriante sort de l'interlocuteur, qui se penche aimablement vers "
                                    "« Toi »")
    kit.pop("sourire", f, from_pt=rnd(S.to_world("interlocuteur", [0, HEAD_DY], f - 1)),
            to=[SOURIRE_LOCAL[0] - 30, SOURIRE_LOCAL[1]])
    inter.lean_to(f, 8, TILT)

    # ---------------- S18 « Fie-toi plutôt aux signaux d’alerte. Un rendement élevé garanti. » ----------------
    f = kit.at("S18", "Fie-toi", "« Toi » lève le stylo vers le bas de l'écran du téléphone")
    toi.reach(f, list(PHONE_HOVER), 9)
    f = kit.at("S18", "plutôt", "le stylo de « Toi » accroche le bas de l'écran et tire vers le bas : la façade "
                                "(étiquette, avis, étoiles) suit la pointe puis tombe comme un masque ; dessous, le "
                                "vrai nom « Invest Minuit » paraît en rouge")
    hit = toi.tap(f - TAP + 1, list(PHONE_TAP))
    pull = 9
    toi.trace(hit + 1, [list(PHONE_TAP), list(PHONE_PULL)], d=pull, e="inOut")
    kit.move("site", hit + 1, [0, PHONE_PULL[1] - PHONE_TAP[1]], d=pull, e="inOut")   # collée à la pointe
    kit.pop("tel_vrai_nom", hit + 2, d=6)
    fall = hit + 1 + pull
    g = kit.drop("site", fall, out=True, h=200, rot=10, d=14)
    toi.reach(g, list(PEN_DOWN), 8)                          # après la chute : la pointe descend le long du corps
    lower(toi, g + 8, 6)

    f = kit.at("S18", "signaux", "la bulle souriante disparaît, l'interlocuteur se redresse ; « Conseiller » glisse "
                                 "et tombe : « Non autorisé » réapparaît, rouge")
    kit.vanish("sourire", f)
    inter.lean_to(f, 0, TILT)
    kit.drop("conseiller", f, out=True, h=70, dx=-20, rot=-12)

    f = kit.at("S18", "d’alerte.", "le crochet du téléphone casse et tombe ; la pastille revient en haut à droite "
                                   "et bat ; une alerte rouge s'allume au centre de l'écran vide")
    S.key("crochet_tel", "dashed", f, 1)
    S.key("crochet_tel", "sag", f, 90, 9, "out")
    kit.drop("crochet_tel", f + 3, out=True)
    kit.drop("crochet_j", f, out=True, rot=30)
    g = kit.move("pastille", f, list(PASTILLE_LIBRE), d=12)
    kit.pulse("pastille", g, peak=1.08)
    kit.pop("tel_alerte", f)

    money = list(PASTILLE_LIBRE)

    def alerte_out(k, f):
        """La carte k sort du centre de l'écran (pop) ; une flèche rouge en part et frappe la pastille « Ton argent »
        (qui bat et tremble) ; puis la carte se range dans la colonne de droite. -> arrivée de la carte."""
        aid = c.alertes[k]
        S.key(aid, "pos", f - 1, list(TEL_C))
        kit.pop(aid, f)
        a = [TEL_C[0] + 70, TEL_C[1] - 40]
        ang = math.degrees(math.atan2(money[1] - a[1], money[0] - a[0]))
        S.keys("fleche_argent", f + 2, pos=a, rot=round(ang, 2), opacity=1)
        S.key("fleche_argent", "scale", f + 2, 1, 3, "out")
        hit = kit.move("fleche_argent", f + 4, [money[0] - 90, money[1] + 12], d=8, e="in")
        S.key("fleche_argent", "scale", hit, 0, 3, "in")
        kit.pulse("pastille", hit, peak=1.1)
        kit.shake("pastille", hit, amp=3)
        return kit.move(aid, hit + 1, list(ALERTE_C[k]))

    f = kit.at("S18", "rendement", "la carte d'alerte 1 (flèche qui monte, cadenas) sort du téléphone, tire une "
                                   "flèche rouge sur « Ton argent », puis se range à droite : « Rendement élevé "
                                   "garanti »")
    alerte_out(0, f)
    f = kit.at("S18", "garanti.", "« garanti » se souligne de rouge ; la carte bat")
    kit.draw("alerte1_l3", f, 8, track="under")
    kit.pulse("alerte1", f, peak=1.06)

    # ---------------- S19 « Un contact non sollicité. Un paiement en crypto, ou vers un compte à l’étranger. » ------
    f = kit.at("S19", "contact", "la carte 2 (téléphone qui sonne vers « Toi ») sort du téléphone, frappe l'argent "
                                 "et se range ; son téléphone sonne (tremble)")
    g = alerte_out(1, f)
    for k, v in enumerate((14, -14, 12, -12, 8, 0)):
        S.key("alerte2_ico", "rot", g + 2 * k, v, 2, "inOut")
    f = kit.at("S19", "paiement", "la carte 3 (pièce ₿) sort du téléphone, frappe l'argent et se range")
    alerte_out(2, f)
    f = kit.at("S19", "compte", "la carte 4 (globe, flèche qui sort) sort du téléphone, frappe l'argent et se range")
    g4 = alerte_out(3, f)
    f = kit.at("S19", "l’étranger.", "les cartes d'alerte battent ensemble ; puis tout se tient")
    kit.stagger(c.alertes[:3], f, 2, kit.pulse, peak=1.05)
    kit.pulse("alerte4", g4, peak=1.05)

    # ---------------- S20 « Au moindre doute, contacte Assurance Banque Épargne Info Service. » ----------------
    f = kit.at("S20", "Au", "le téléphone et les quatre cartes d'alerte se réduisent et filent dans le disque « 3 » "
                            "du repère")
    kit.stagger(["telephone"] + c.alertes, f, 2, kit.vanish, into=list(MARK3), d=MORPH)

    f = kit.at("S20", "doute,", "un « ? » surgit à côté de la tête de « Toi »")
    S.key("question", "pos", f - 1, list(Q_TETE_P3))
    S.key("question", "gs", f - 1, Q_GS)
    S.key("question", "rot", f - 1, 0)
    kit.pop("question", f)

    f = kit.at("S20", "contacte", "« Toi » touche l'air devant lui : un combiné cyan surgit sous la pointe et trois "
                                  "ondes d'appel cyan battent vers le haut")
    hit = toi.tap(f - TAP + 1, list(COMBINE_C))
    kit.pop("combine", hit)
    lower(toi, hit + 6, 8)
    g = kit.stagger(ONDES, hit + 3, 3, kit.pop)[-1]
    for cyc in range(2):
        kit.stagger(ONDES, g + 2 + 12 * cyc, 3, kit.pulse, peak=1.25)

    f = kit.at("S20", "Assurance", "une bouée tombe au bout des ondes")
    drop_in(kit, "bouee", f, h=110)

    f = kit.at("S20", "Banque", "sous la bouée, un téléphone et le nom en deux lignes : « Assurance Banque » / "
                                "« Épargne Info Service »")
    kit.pop("bouee_tel", f)
    g = kit.type("bouee_nom1", f + 2, rate=3)
    kit.type("bouee_nom2", g, rate=3)

    f = kit.at("S20", "Info", "le sceau « AMF » de la liste noire revient de sa place sur la liste et se pose sur la "
                              "bouée (avec une traînée)")
    kit.pop("amf_bouee", f, d=4)
    kit.move("amf_bouee", f + 2, list(AMF_BOUEE_C), d=12)
    S.key("amf_trace", "scale", f + 3, 1, 3, "out")
    kit.move("amf_trace", f + 6, list(AMF_BOUEE_C), d=12)
    S.key("amf_trace", "scale", f + 17, 0, 3, "in")

    f = kit.at("S20", "Service.", "le « ? » quitte la tête de « Toi », suit les ondes jusqu'à la bouée et s'y change "
                                  "en coche deep")
    g = kit.move("question", f, [ONDES_C[0][0] + 10, ONDES_C[0][1] + 20], d=7, e="in")
    g = kit.move("question", g, list(COCHE_BOUEE_C), d=7, e="out")
    S.key("question", "gs", f, 64, 14, "inOut")
    kit.morph(["question"], ["coche_bouee"], g)

    # ---------------- S21 « Et retiens : une opportunité qui refuse la vérification ne mérite pas ton argent. » -----
    f = kit.at("S21", "Et", "le combiné, les ondes et le nom se réduisent ; la bouée cochée reste un instant")
    kit.morph(["combine", "bouee_tel", "bouee_nom1", "bouee_nom2"] + ONDES, [], f)

    f = kit.at("S21", "retiens :", "repère : le disque « 3 » se coche à son tour : Délai ✓ · Registres ✓ · "
                                   "Apparence ✓ ; l'interlocuteur sort à pied par la gauche ; la bouée cochée se réduit")
    S.key("marqueur", "done2", f, 1, 6, "out")
    S.key("marqueur", "on", f, 0, 4, "out")
    kit.pop("marqueur_fait3", f + 3, d=5)
    kit.draw("marqueur_fait3_coche", f + 5, 6)
    out = inter.walk(f + 2, INTER_OUT_X, d=MOVE)
    S.key("interlocuteur", "scale", out, 0)
    kit.morph(["bouee", "amf_bouee", "coche_bouee"], [], f + 13)

    f = kit.at("S21", "opportunité", "l'offre revient en grand avec son bouton, sa case de vérification et son "
                                     "compte à rebours rouge, qui recommence à fondre")
    kit.move("offre", f, list(OFFRE_C), scale=1)
    for cid in COIN_BACK:
        kit.pop(cid, f + 8)
    v0 = S.val("compte_rebours", "value", f - 1)
    mer = S.word_after("mérite", f)
    S.key("compte_rebours", "value", f, round(max(0.08, v0 - 0.12), 3), mer - f, "linear")

    f = kit.at("S21", "refuse", "« Toi » sort son champ de recherche du stylo, à pleine taille ; il monte vers la case "
                                "de l'offre : la barre rouge descend dans sa course, choc, le champ est repoussé et "
                                "tremble ; la case rougit, un grand ✕ s'y trace et bat")
    toi.reach(f - 6, list(FIELD_TIP), 6)
    up = kit.pop("champ", f, scale=CHAMP_S21_K, from_pt=list(FIELD_TIP), to=list(CHAMP_S21)) - 5
    lower(toi, f + 2, 8)
    rise = 12
    S.key("champ", "pos", up, [CHAMP_S21[0], CHAMP_HIT_Y], rise, "in")
    hitb = up + rise - 1                                     # le champ touche la barre baissée
    S.key("compte_rebours", "pos", hitb - 4, [BAR_LOCAL[0], BAR_LOCAL[1] + BAR_DROP], 4, "out")
    impact(S, hitb, [CHAMP_S21[0], BAR_BOTTOM])
    S.key("champ", "pos", hitb + 1, [CHAMP_S21[0], CHAMP_BACK_Y], 6, "out")   # repoussé de 80 px (200 ms)
    kit.shake("champ", hitb + 7, amp=8)
    kit.shake("compte_rebours", hitb + 1, amp=5, axis="y")
    case_block(S, kit, hitb, stay=True)
    kit.pulse("case_offre", hitb + 4, peak=1.2)

    f = kit.at("S21", "mérite", "« Toi » barre le bout de la barre rouge d'un trait deep : l'offre bascule et sort "
                                "entière par la gauche ; le champ rentre dans le stylo")
    assert f - 6 - hitb >= 12, (f, hitb)                     # la cause se lit avant le geste (≥ 0,6 s jusqu'au trait)
    a, b = (rnd(S.to_world("compte_rebours", pt, f - 7)) for pt in TRAIT_PTS)
    end = toi.strike(f - 6, a, b, lead=6, line="trait_refus", track="draw")
    gone = kit.move("offre", end, list(OFFRE_OUT), d=14, e="in")
    S.key("offre", "rot", end, -25, 14, "in")
    S.key("offre", "scale", gone, 0)                         # hors champ : rangée
    kit.vanish("champ", end, into=rnd(toi.tip(end + POP - 1)))
    lower(toi, end + 1, 8)

    f = kit.at("S21", "argent.", "la pastille « Ton argent » descend au centre et grandit à côté de « Toi », puis bat")
    g = kit.move("pastille", f, list(PASTILLE_FIN), d=21, scale=PASTILLE_FIN_K)
    kit.pulse("pastille", g, peak=PASTILLE_FIN_K * 1.06)

    # ---------------- S22 « Abonne-toi pour comprendre ton argent. » ----------------
    glide = 10                                               # la pastille quitte vite le sous-titre de la carte
    out = kit.outro("S22", outs=["marqueur", "marqueur_fait3", "nom_toi"], btn_at=glide, press="argent.",
                    pos=FIN_C, clear="fade", bsize=round(40 * BTN_K, 1))
    f = out["card"]
    S.set(out["cursor"], opacity=0)                          # pas de pointeur : le stylo de « Toi » touche
    kit.ensure("pastille", "z", S.ents["pastille"]["z"])
    S.key("pastille", "z", f, 41)                            # au-dessus de la carte (z 40)
    kit.ensure("pastille", "textOp", 1)
    S.key("pastille", "textOp", f, 0, 4, "out")
    S.key("pastille", "text", f + 4, T_ABONNER)
    S.key("pastille", "textOp", f + 4, 1, FADE, "out")
    S.key("pastille", "w", f, round(BTN_W / BTN_K, 2), glide, "out")
    kit.move("pastille", f, list(FIN_BUTTON), d=glide, e="out", scale=BTN_K)
    S.key("pastille", "opacity", f + glide, 0)               # relais exact : le bouton de la carte paraît dessous

    fp = out["press"]
    toi.set_z(fp - TAP - 12, S.ents[toi.id]["z"], tool_z=44)  # bras et stylo au-dessus de la carte
    hit = toi.tap(fp - TAP + 1, list(FIN_TAP))
    for k, oid in enumerate(c.fin_ondes):
        ring(S, oid, hit + 4 * k, d=14, s0=0.6, s1=1.2)
    end = lower(toi, hit + 6, 8)
    assert hit == fp and end < FILM_END and hit + 4 + 14 < FILM_END, (hit, fp, end)
