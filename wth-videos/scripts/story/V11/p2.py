"""V11, partie 2 : S09-S14, images 823-1771 (32 temps forts, 31,6 s). Famille (alliances, « ou » Séparation,
berceau, pile des sujets à revoir) et travail (quatre cas reliés par « ou », barres, conseil tiré mais encore rouge).

ÉTAT D'ENTRÉE : ENTRY_P2 épinglé à 822 (`kit.pin(f0 - 1, ENTRY_P2)`, f0 = scene_f0(S, "S09") = 823) : etat_initial de
S09 = résultat de S08 (repère en haut, étape 1 « Famille » active ; disque-événement cyan en EVT_C ; un « ? » devant
chacune des 5 rangées ; L1-L2 surlignées ; pastille « mars 2023 » cerclée de rouge sous la photo ; vie « nov. 2026 » ;
conseil rouge penché de 8° en CONSEIL_C, fil sag 30). Garde-fous de partie isolée (sans effet dans le film entier) :
`if S.val("client", "scale", f0 - 1) == 0: c.client.enter(f0 - 10, at=CLIENT_C)` ; « Toi » est visible dès l'image 0
(rien à faire), le mettre bras baissé (`c.toi.lower(f0 - 9)`).
SORTIE : ENTRY_P3 à l'image 1771 (voir __init__.py). Tout ce que cette partie commence finit avant 1772.

Ids : evt_disque, q_ligne1-5, evt_rings, conjoint, ou_famille, separation, fiche_L1-L3, fiche_hl1-3, pile_* (capsules :
piste stroke INK -> RED en hex ; texte `pile_*_mot`), conseil, conseil_rouge, evt_cradle, badge_rings, badge_cradle,
mini_rings, mini_cradle, marqueur, travail1-4 (capsules avec pictogramme), ou_travail1-3, badge_travail,
jauge_revenus / jauge_fiscalite / jauge_liquidites (+ `_mot`, `_trait`), fil_jauge1-3, toi, client.

BRIEF, scène par scène :
- S09 (823-910) « Ton » : q_ligne1-5 se réduisent (kit.vanish) ; kit.morph("evt_disque", "evt_rings") à EVT_C.
  « marie, » : c.conjoint.enter(at=CONJOINT_IN) ; client.lean_to(+5°) et conjoint.lean_to(-5°) l'un vers l'autre.
  « pacse » : L1 red 0 -> 1 (3 im.) et pulse x2 (kit.pulse(..., track="pulse", times=2, step=2)). « ou » : pop
  `ou_famille`. « sépare ? » : pop `separation` ; conjoint.hop(CONJOINT_OUT, 12, lean=-4) (recul, penché en arrière ;
  il ne touche pas le conseil, x 445) ; client.lean_to(0) ; L1 rebat x2.
- S10 (911-1101) « Régime » : c.conjoint.exit ; kit.fade ou_famille et separation vers 0 puis scale 0 ; `pile_regime`
  pop from_pt="conseil" et monte à (PILE_X, PILE_YS[0]) (POP + move 12 im.). « clause » : pile_clause -> PILE_YS[1].
  « donation, » : pile_donation -> PILE_YS[2]. « transmission : » : pile_transmission -> PILE_YS[3]. « revoir. » :
  stroke des 4 capsules -> RED (hex, 4 im.) et kit.shake 5 px, de bas en haut, 2 images d'écart.
- S11 (1102-1331) « Une » : regime, donation, transmission : kit.vanish(into="conseil") ; pile_clause glisse en
  (PILE_X, PILE_YS[3]) ; `mini_rings` pop en CLAUSE_MINI_L (suivre la pilule : poser sa place à l'arrivée) ;
  kit.morph("evt_rings", "badge_rings") vers BADGES[0] (relais : la PNG se réduit dans le badge). « naissance ? » :
  drop `evt_cradle` à EVT_C ; 8 images après l'impact L2 red -> 1 + pulse. « Nouvel » / « protection » /
  « prévoyance, » : pile_objectif / pile_protection / pile_prevoyance sortent du conseil vers PILE_YS[0..2] (stroke
  encore INK). « clause » : `mini_cradle` vole de EVT_C en arc 60 jusqu'à CLAUSE_MINI_R (MOVE) ; à l'arrivée
  pile_clause pulse x2 + shake : elle porte les deux événements. « jour. » : stroke des 3 nouvelles -> RED, de bas en
  haut, 2 images d'écart. Fin : « Clause bénéficiaire » en haut entre ses deux mini-badges.
- S12 (1332-1439) « La » : les 4 pilules et les 2 mini-badges rentrent dans le conseil (vanish into, décalés de 2) ;
  kit.morph("evt_cradle", "badge_cradle") vers BADGES[1]. « changer : » : L1 et L2 pulse une fois ensemble ;
  fiche_hl1-2 opacity -> 0 et slotFill -> 1. « travail. » : kit.step(f, 1) ; fiche_hl3 -> 1, L3 slotFill -> 0.
- S13 (1440-1602) « crée » : pop travail1 (x 225, TRAVAIL_YS[0]). « entreprise, » : L3 red -> 1 + pulse x2.
  « perd » : pop ou_travail1 puis, 4 images après, travail2 ; L3 pulse 1 fois. « promu » : ou_travail2 + travail3 ;
  L3 pulse. « retraite ? » : ou_travail3 + travail4 ; L3 pulse. Les « ou » disent « autre cas », pas « ensuite ».
- S14 (1603-1771) « Ses » : kit.morph(travail1-4 + ou_travail1-3, "badge_travail") vers BADGES[2] (pair=False : tout se
  réduit vers le badge). « revenus, » / « fiscalité » / « liquidités » : chaque jauge sort du conseil (pop from_pt=
  "conseil" puis move à (JAUGE_CX, y), avec sa légende `_mot` et son trait d'avant `_trait`), value = niveau
  d'avant (déclaré). « changent. » : S.key(value) des 3 jauges vers leur nouveau niveau, MOVE inOut, ensemble (les
  traits restent). « conseil » : c.toi.tap(f - TAP + 1, CONSEIL_TAP) (contact sur le mot) ; kit.shake("conseil", 5) ;
  kit.pulse("conseil_rouge", ...) (opacité ou scale) ; le bras se rebaisse ensuite. « suivre. » : kit.draw
  fil_jauge1-3 (décalés de 2) ; le conseil monte de 12 px et revient (MOVE 9 + 9) ; il RESTE rouge et penché, son
  fil vers le cadre reste accroché.

RACCORD vers p3 : l'image 1771 doit valoir ENTRY_P3 (barres aux nouveaux niveaux, traits d'avant visibles, fils encre
tracés ; badges alliances, berceau, immeuble en BADGES[0..2] ; L1-L3 rouges, L3 seule surlignée ; repère étape 2 ;
conseil en CONSEIL_C, rouge, penché ; pile et pilules de travail à l'échelle 0 ; « Toi » en TOI_HOME bras baissé).
"""
from . import *  # noqa: F401,F403
from pipeline.story import DROP, FADE, MORPH, MOVE, POP, SCALE, TILT  # noqa: F401
from pipeline.story_kit import TAP, r3  # noqa: F401


def part(S, kit, c):
    toi, client, conjoint = c.toi, c.client, c.conjoint
    f0 = scene_f0(S, "S09")                                   # 823
    entry = {id: dict(tr) for id, tr in ENTRY_P2.items()}     # etat_initial de S09 = résultat de S08
    for id, tr in entry.items():                              # couleur hex : même teinte, casse de la valeur en place
        for t, v in tr.items():
            if isinstance(v, str) and t in S.ents[id]["t"]:
                cur = S.val(id, t, f0 - 2)
                if isinstance(cur, str) and cur.lower() == v.lower():
                    tr[t] = cur
    kit.pin(f0 - 1, entry)
    if S.val("client", "scale", f0 - 1) == 0:                 # partie construite seule (WTH_PARTS=p2)
        client.enter(f0 - 10, at=CLIENT_C)
    toi.lower(f0 - 9)                                         # « Toi » bras baissé (sans effet s'il l'est déjà)

    def conseil_top(n):
        return S.to_world("conseil", list(CONSEIL_TOP_LOCAL), n)

    def sortir(pid, f, to, d=12):
        """Une pilule (ou une barre) sort du haut du conseil et monte à sa place (POP + glissé de 400 ms)."""
        kit.pop(pid, f, from_pt=conseil_top(f - 1), to=list(to))
        S.key(pid, "pos", f, r3(to), d, "out")
        return f + d

    def rougir(pid, f, d=4):
        S.key(pid, "stroke", f, RED, d, "out")

    # ================= S09 : se marie, se pacse ou se sépare ? =================
    f = kit.at("S09", "Ton", "les 5 « ? » rentrent dans leurs rangées ; le disque-événement devient les alliances")
    for i in range(5):
        kit.vanish(f"q_ligne{i + 1}", f)
    kit.morph("evt_disque", "evt_rings", f)

    f = kit.at("S09", "marie,", "le conjoint (figurine papier) entre face au client ; ils s'inclinent l'un vers "
                                "l'autre")
    conjoint.enter(f, at=CONJOINT_IN)
    client.lean_to(f + 3, 5, TILT)
    conjoint.lean_to(f + 3, -5, TILT)

    f = kit.at("S09", "pacse", "« Famille : célibataire » vire au rouge et sa puce bat deux fois")
    S.key("fiche_L1", "red", f, 1, 3, "out")
    kit.pulse("fiche_L1", f, times=2, step=2, track="pulse")

    f = kit.at("S09", "ou", "un grand « ou » s'écrit sous les alliances : un autre cas")
    kit.pop("ou_famille", f)

    f = kit.at("S09", "sépare ?", "« Séparation » surgit sous le « ou » ; le conjoint recule d'un bond, penché en "
                                  "arrière ; L1 rouge bat de nouveau")
    kit.pop("separation", f)
    conjoint.hop(f, CONJOINT_OUT, 12, lean=-4)
    client.lean_to(f, 0, TILT)
    kit.pulse("fiche_L1", f + 4, times=2, step=2, track="pulse")

    # ================= S10 : tout peut être à revoir =================
    f = kit.at("S10", "Régime", "le conjoint sort, « ou » et « Séparation » s'effacent ; « Régime matrimonial » sort "
                                "du conseil et monte au-dessus de lui")
    conjoint.exit(f)
    for tid in ("ou_famille", "separation"):
        kit.fade(tid, f, to=0)
        S.key(tid, "scale", f + FADE, 0)
    sortir("pile_regime", f, (PILE_X, PILE_YS[0]))
    for (pid, word), y in zip((("pile_clause", "clause"), ("pile_donation", "donation,"),
                               ("pile_transmission", "transmission :")), PILE_YS[1:]):
        nom = dict(PILE)[pid]
        f = kit.at("S10", word, f"« {nom} » sort du conseil et s'empile au-dessus")
        sortir(pid, f, (PILE_X, y))

    f = kit.at("S10", "revoir.", "les contours des 4 pilules virent au rouge et chacune tremble, de bas en haut")
    for k, pid in enumerate(("pile_regime", "pile_clause", "pile_donation", "pile_transmission")):
        rougir(pid, f + 2 * k)
        kit.shake(pid, f + 2 * k, 5)

    # ================= S11 : une naissance =================
    f = kit.at("S11", "Une", "régime, donation, transmission rentrent dans le conseil ; « Clause bénéficiaire » monte "
                             "en haut avec un mini-badge alliances ; les alliances se rangent en badge")
    for k, pid in enumerate(("pile_regime", "pile_donation", "pile_transmission")):
        kit.vanish(pid, f + k, into="conseil")
    kit.move("pile_clause", f, CLAUSE_TOP, d=12, e="out")        # en haut, elle s'élargit : place des deux badges
    kit.ensure("pile_clause", "w", c.pile_w["pile_clause"])
    S.key("pile_clause", "w", f, CLAUSE_TOP_W, 12, "out")
    left0 = PILE_X - c.pile_w["pile_clause"] / 2 + (CLAUSE_MINI_L[0] - (CLAUSE_TOP[0] - CLAUSE_TOP_W / 2))
    kit.pop("mini_rings", f, from_pt=(left0, PILE_YS[1]), to=list(CLAUSE_MINI_L), d=12)
    kit.morph("evt_rings", "badge_rings", f)

    f = kit.at("S11", "naissance ?", "un berceau tombe dans la vie du client ; « Enfants : aucun » vire au rouge et "
                                     "bat")
    impact = kit.drop("evt_cradle", f, h=170, to=list(EVT_C))
    S.key("fiche_L2", "red", impact + 8, 1, 3, "out")
    kit.pulse("fiche_L2", impact + 8, times=2, step=2, track="pulse")

    for (pid, word), y in zip((("pile_objectif", "Nouvel"), ("pile_protection", "protection"),
                               ("pile_prevoyance", "prévoyance,")), PILE_YS[:3]):
        nom = dict(PILE)[pid]
        f = kit.at("S11", word, f"« {nom} » sort du conseil et s'empile")
        sortir(pid, f, (PILE_X, y))

    f = kit.at("S11", "clause", "un mini-badge berceau vole du berceau au bout droit de « Clause bénéficiaire », qui "
                                "bat et tremble : elle porte les deux événements")
    kit.pop("mini_cradle", f, d=6)
    arr = kit.move("mini_cradle", f, list(CLAUSE_MINI_R), arc=60)
    kit.pulse("pile_clause", arr, times=2, step=3)
    kit.shake("pile_clause", arr + 12, 5)

    f = kit.at("S11", "jour.", "les contours des trois nouvelles pilules virent au rouge, de bas en haut")
    for k, pid in enumerate(("pile_objectif", "pile_protection", "pile_prevoyance")):
        rougir(pid, f + 2 * k)

    # ================= S12 : la famille n'est pas seule à changer =================
    f = kit.at("S12", "La", "la pile et ses deux mini-badges rentrent dans le conseil ; le berceau se range en badge")
    for k, ids in enumerate((["pile_objectif"], ["pile_protection"], ["pile_prevoyance"],
                             ["pile_clause", "mini_rings", "mini_cradle"])):
        for pid in ids:
            kit.vanish(pid, f + 2 * k, into="conseil")
    kit.morph("evt_cradle", "badge_cradle", f)

    f = kit.at("S12", "changer :", "les deux rangées rouges de la famille battent ensemble ; leur surlignage s'efface")
    for i in (0, 1):
        kit.pulse(f"fiche_L{i + 1}", f, times=1, step=3, track="pulse")
        S.key(f"fiche_hl{i + 1}", "opacity", f, 0, 9, "out")
        S.key(f"fiche_L{i + 1}", "slotFill", f, 1, 9, "out")

    f = kit.at("S12", "travail.", "le repère glisse sur l'étape 2 « Travail » ; la rangée « Travail : salarié » se "
                                  "surligne")
    kit.step(f, 1)
    S.key("fiche_hl3", "opacity", f, 1, 9, "out")
    S.key("fiche_L3", "slotFill", f, 0, 9, "out")

    # ================= S13 : quatre cas de travail, reliés par « ou » =================
    f = kit.at("S13", "crée", "la pilule « Entreprise » surgit dans la vie du client")
    kit.pop("travail1", f)

    f = kit.at("S13", "entreprise,", "« Travail : salarié » vire au rouge et sa puce bat deux fois")
    S.key("fiche_L3", "red", f, 1, 3, "out")
    kit.pulse("fiche_L3", f, times=2, step=2, track="pulse")

    for k, (word, nom) in enumerate((("perd", "Emploi perdu"), ("promu", "Promotion"), ("retraite ?", "Retraite"))):
        f = kit.at("S13", word, f"autre cas : un « ou », puis « {nom} » surgit dessous ; L3 bat une fois")
        kit.pop(f"ou_travail{k + 1}", f)
        kit.pop(f"travail{k + 2}", f + 4)
        kit.pulse("fiche_L3", f + 4, times=1, step=3, track="pulse")

    # ================= S14 : revenus, fiscalité, liquidités ; le conseil doit suivre =================
    f = kit.at("S14", "Ses", "les quatre pilules de travail et leurs « ou » se rassemblent en un badge immeuble")
    outs = [t[0] for t in TRAVAIL] + [f"ou_travail{k + 1}" for k in range(3)]
    for o in outs:
        kit.vanish(o, f, into=list(BADGES[2]), d=MORPH)
    kit.pop("badge_travail", f, d=MORPH)

    for (jid, leg, old, new, y), word in zip(JAUGES, ("revenus,", "fiscalité", "liquidités")):
        f = kit.at("S14", word, f"la barre « {leg} » sort du conseil, légendée, avec le trait de son niveau d'avant")
        sortir(jid, f, (JAUGE_CX, y))
        S.key(f"{jid}_trait", "scale", f, 1)
        kit.pop(f"{jid}_mot", f + 4)

    f = kit.at("S14", "changent.", "les trois niveaux bougent ensemble : revenus en baisse, fiscalité et liquidités en "
                                   "hausse ; les traits d'avant restent")
    for jid, leg, old, new, y in JAUGES:
        S.key(jid, "value", f, new, MOVE, "inOut")

    f = kit.at("S14", "conseil", "« Toi » touche du stylo le bout du conseil : il tremble et son contour rouge bat")
    hit = toi.tap(f - TAP + 1, list(CONSEIL_TAP))
    kit.shake("conseil", hit, 5)
    kit.pulse("conseil_rouge", hit, times=2, step=2)
    toi.lower(hit + 6)

    f = kit.at("S14", "suivre.", "trois fils encre se tracent des nouveaux niveaux au conseil et le tirent vers le "
                                 "haut ; il reste rouge, penché, accroché à la vieille fiche")
    for k in range(3):
        kit.draw(f"fil_jauge{k + 1}", f + 2 * k)
    S.key("conseil", "pos", f + 6, [CONSEIL_C[0], CONSEIL_C[1] - 12], 8, "out")
    S.key("conseil", "pos", f + 14, list(CONSEIL_C), 8, "inOut")
