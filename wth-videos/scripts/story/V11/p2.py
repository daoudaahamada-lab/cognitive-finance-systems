"""V11, partie 2 : S09-S14, images 823-1771 (32 temps forts, 31,6 s). Famille (alliances, « ou » Séparation,
berceau, pile des sujets à revoir) et travail (un cas à la fois relié par « ou », barres, conseil tiré mais encore
rouge).

ÉTAT D'ENTRÉE : ENTRY_P2 épinglé à 822 (`kit.pin(f0 - 1, ENTRY_P2)`, f0 = scene_f0(S, "S09") = 823) : etat_initial de
S09 = résultat de S08. Garde-fous de partie isolée (sans effet dans le film entier) : client entré, « Toi » bras baissé.
SORTIE : ENTRY_P3 à l'image 1771 (voir __init__.py). Tout ce que cette partie commence finit avant 1772.

Tour de revue 1 :
- la pilule de la vie (« nov. 2026 ») se retire sur « Ton » (S09) ; elle revient en S21 dans la réponse du client ;
- S09 : le conjoint entre à GAUCHE du client ; « ou » deep 56 px ; « sépare ? » : il se détourne et sort du champ,
  les alliances deviennent deux anneaux qui s'écartent de 120 px ;
- S10-S11 : la pile se dresse dans la colonne de la vie (x 240, pas de 80 : 26 px entre deux pilules) et grandit PAR
  LE BAS (pile_push) : chaque pilule sort du conseil vers la case du bas, les autres montent d'une case ; aucun trajet
  ne croise une pilule posée ; « revoir. » / « jour. » : encre sur papier -> cyan pâle (« à revoir »), aucun rouge ;
  les alliances se rangent en badge dès « Régime » ; S11 « Une » : seules les trois pilules disparaissent (4 images),
  la clause monte en haut de la colonne et reçoit le pictogramme « famille » sur son bout gauche ; « Nouvel » : le
  berceau se range en badge ; « clause » : le pictogramme « enfants » se pose sur son bout droit (la même clause porte
  les deux événements) ; S12 « La » : la pile se résorbe sur place, le conseil bat ;
- rangées : rouge seulement sur celle de la scène en cours ; les autres passent à « à revoir » (aplat cyan pâle) ;
- S13 : un cas à la fois, grand disque + pictogramme + étiquette, au-dessus du client ; « ou » deep 56 px ;
- S14 : barres dans la colonne de la vie, légende au-dessus, flèche ↓ rouge / ↑ deep, trait d'avant tireté gris ;
  « conseil » : vrai geste de « Toi » vers le bout du conseil ; « suivre. » : trois fils encre (8 px) partent du bout
  de chaque barre et descendent au conseil sans se croiser, qui est tiré vers les barres et y reste (CONSEIL_PULL)
  jusqu'à S15 « décisions », toujours rouge et penché.
Contrôle sans son (tour ciblé) : cœur qui se brise sur « sépare » ; pictogrammes famille / enfants qui volent de
leurs badges jusqu'à la clause, puis « ×2 » ; rangées rouges cumulées ; « Besoin de liquidités ».
"""
from . import *  # noqa: F401,F403
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, SCALE, TILT  # noqa: F401
from pipeline.story_kit import TAP, r3  # noqa: F401

SORTIR_D = MOVE                                 # une pilule ou une barre monte du conseil à sa place


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

    def sortir(pid, f, to, d=SORTIR_D):
        """Une pilule (ou une barre) sort du haut du conseil et monte à sa place, dans la vie (POP + MOVE out)."""
        kit.pop(pid, f, from_pt=conseil_top(f - 1), to=list(to))
        S.key(pid, "pos", f, r3(to), d, "out")
        return f + d

    def a_revoir(pid, f, d=5):
        S.key(pid, "fill", f, LIGHT, d, "out")

    # ================= S09 : se marie, se pacse ou se sépare ? =================
    f = kit.at("S09", "Ton", "les 5 « ? » rentrent dans leurs rangées ; le disque-événement devient les alliances ; "
                             "la date de la vie se retire")
    for i in range(5):
        kit.vanish(f"q_ligne{i + 1}", f)
    kit.morph("evt_disque", "evt_rings", f)
    kit.vanish("vie", f, d=6)

    f = kit.at("S09", "marie,", "le conjoint (figurine papier) entre à gauche du client ; ils s'inclinent l'un vers "
                                "l'autre")
    conjoint.enter(f, at=CONJOINT_IN)
    client.lean_to(f + 3, -4, TILT)
    conjoint.lean_to(f + 3, 4, TILT)

    f = kit.at("S09", "pacse", "« Famille : célibataire » vire au rouge et sa puce bat deux fois")
    rows_state(S, kit, f, red=0)
    kit.pulse("fiche_L1", f, times=2, step=2, track="pulse")

    f = kit.at("S09", "ou", "un grand « ou » deep s'écrit sous les alliances : un autre cas")
    kit.pop("ou_famille", f)

    f = kit.at("S09", "sépare ?", "« Séparation » surgit sous le « ou » ; le conjoint se détourne et sort du champ par "
                                  "la gauche ; les alliances deviennent un cœur cyan qui se brise : ses deux moitiés "
                                  "s'écartent et penchent ; L1 rebat")
    kit.pop("separation", f)
    S.key("conjoint", "look", f, -1, 3, "out")
    conjoint.lean_to(f, 0, 4)
    client.lean_to(f, 0, TILT)
    g = conjoint.walk(f + 2, CONJOINT_OUT_X, d=20, e="in")
    S.key("conjoint", "scale", g, 0)
    kit.vanish("evt_rings", f, d=5)
    for cid, dx, rot in zip(("coeur_g", "coeur_d"), COEUR_SPLIT, (-14, 14)):
        kit.pop(cid, f, d=5)
        kit.move(cid, f + 8, [COEUR_C[0] + dx, COEUR_C[1] + 6], d=12, e="out")
        S.key(cid, "rot", f + 8, rot, 12, "out")
    kit.pulse("fiche_L1", f + 4, times=2, step=2, track="pulse")

    # ================= S10 : tout peut être à revoir =================
    f = kit.at("S10", "Régime", "« ou » et « Séparation » se réduisent ; les deux anneaux se rangent en badge "
                                "« famille » au-dessus du client ; « Régime matrimonial » sort du conseil et monte "
                                "dans la vie")
    for tid in ("ou_famille", "separation"):
        S.key(tid, "scale", f, 0, 6, "in")
        S.key(tid, "opacity", f + 6, 0)
    for cid in ("coeur_g", "coeur_d"):
        kit.vanish(cid, f, into=list(BADGES[0]), d=MORPH)
    kit.pop("badge_rings", f + 2, from_pt=RINGS_C, to=list(BADGES[0]), d=MORPH)
    pile = []                                                 # du bas vers le haut
    pile_push(kit, pile, "pile_regime", f, conseil_top(f - 1))
    for pid, word in (("pile_clause", "clause"), ("pile_donation", "donation,"),
                      ("pile_transmission", "transmission :")):
        nom = dict(PILE)[pid]
        f = kit.at("S10", word, f"« {nom} » sort du conseil et se pose en bas de la pile, qui monte d'une case")
        pile_push(kit, pile, pid, f, conseil_top(f - 1))

    f = kit.at("S10", "revoir.", "les 4 pilules passent au cyan pâle, « à revoir », et chacune tremble, de bas en haut")
    for k, pid in enumerate(pile):
        a_revoir(pid, f + 2 * k)
        kit.shake(pid, f + 2 * k, 5)

    # ================= S11 : une naissance =================
    w_cl = c.pile_w["pile_clause"]
    mini_l = (PILE_X - w_cl / 2 + 30, PILE_YS[3] + MINI_DY)
    mini_r = (PILE_X + w_cl / 2 - 30, PILE_YS[3] + MINI_DY)
    f = kit.at("S11", "Une", "régime, donation et transmission disparaissent ; « Clause bénéficiaire » monte en haut "
                             "de la colonne ; le pictogramme « famille » se pose sur son bout gauche, son badge bat")
    for pid in ("pile_regime", "pile_donation", "pile_transmission"):
        kit.vanish(pid, f, d=4)
    g = kit.move("pile_clause", f + 1, (PILE_X, PILE_YS[3]), d=8, e="inOut")
    # contrôle muet (« pourquoi celle-là ? ») : le pictogramme famille VOLE de son badge jusqu'au bout de la clause
    kit.pulse("badge_rings", f, peak=1.25, step=3)
    kit.pop("mini_rings", g, from_pt=list(BADGES[0]), to=list(mini_l), d=14)

    f = kit.at("S11", "naissance ?", "un berceau tombe dans la vie du client, sous la clause ; « Enfants : aucun » vire "
                                     "au rouge et bat ; « Famille » passe à « à revoir »")
    impact = kit.drop("evt_cradle", f, h=150, to=list(CRADLE_C))
    rows_state(S, kit, impact + 8, red=1)
    kit.pulse("fiche_L2", impact + 8, times=2, step=2, track="pulse")

    pile = []
    for pid, word in (("pile_objectif", "Nouvel"), ("pile_protection", "protection"),
                      ("pile_prevoyance", "prévoyance,")):
        nom = dict(PILE)[pid]
        f = kit.at("S11", word, f"« {nom} » sort du conseil et se pose en bas de la colonne, qui monte d'une case" +
                   (" ; le berceau se range en badge « enfants » au-dessus du client" if word == "Nouvel" else ""))
        if word == "Nouvel":
            kit.vanish("evt_cradle", f, into=list(BADGES[1]), d=MORPH)
            kit.pop("badge_cradle", f + 2, from_pt=CRADLE_C, to=list(BADGES[1]), d=MORPH)
            pile_push(kit, pile, pid, f + 4, conseil_top(f + 3))
        else:
            pile_push(kit, pile, pid, f, conseil_top(f - 1))

    f = kit.at("S11", "clause", "le badge « enfants » bat et son pictogramme se pose sur le bout droit de « Clause "
                                "bénéficiaire », qui bat et tremble : la même clause est touchée par le mariage ET la "
                                "naissance")
    kit.pulse("badge_cradle", f, peak=1.25, step=3)
    arr = kit.pop("mini_cradle", f, from_pt=list(BADGES[1]), to=list(mini_r), d=14)
    kit.pulse("pile_clause", arr, times=2, step=3)
    kit.shake("pile_clause", arr + 12, 5)
    kit.pop("fois2", arr)                         # « ×2 » entre les deux pictogrammes, tenu jusqu'à S12 « La »
    kit.pulse("mini_rings", arr, peak=1.2, step=3)

    f = kit.at("S11", "jour.", "les trois nouvelles pilules passent au cyan pâle, « à revoir », de bas en haut")
    for k, pid in enumerate(pile):
        a_revoir(pid, f + 2 * k)

    # ================= S12 : la famille n'est pas seule à changer =================
    f = kit.at("S12", "La", "la pile et ses deux pictogrammes se résorbent sur place, de haut en bas ; le conseil bat")
    fondre(kit, ["fois2", "mini_rings", "mini_cradle", "pile_clause"] + pile[::-1], f, step=2)

    f = kit.at("S12", "changer :", "les deux rangées de la famille battent ensemble ; « Enfants » passe à « à revoir »")
    for i in (0, 1):
        kit.pulse(f"fiche_L{i + 1}", f, times=1, step=3, track="pulse")
    rows_state(S, kit, f, red=None)

    f = kit.at("S12", "travail.", "le repère glisse sur l'étape 2, légendée « Travail » ; la rangée « Travail : "
                                  "salarié » se surligne")
    kit.step(f, 1)
    S.key("fiche_hl3", "opacity", f, 1, 9, "out")
    S.key("fiche_L3", "slotFill", f, 0, 9, "out")

    # ================= S13 : quatre cas de travail, un à la fois, reliés par « ou » =================
    f = kit.at("S13", "crée", "un grand disque « Entreprise » (immeuble) surgit dans la vie du client")
    kit.pop("travail1", f)

    f = kit.at("S13", "entreprise,", "« Travail : salarié » vire au rouge et sa puce bat deux fois")
    rows_state(S, kit, f, red=2)
    kit.pulse("fiche_L3", f, times=2, step=2, track="pulse")

    for k, (word, nom) in enumerate((("perd", "Emploi perdu"), ("promu", "Promotion"), ("retraite ?", "Retraite"))):
        f = kit.at("S13", word, f"autre cas : un grand « ou » deep bat, le cas précédent se retire et « {nom} » "
                                f"prend sa place ; « Travail » bat une fois")
        if k == 0:
            kit.pop("ou_travail", f)
        else:
            kit.pulse("ou_travail", f, peak=1.25, step=3)
        kit.vanish(f"travail{k + 1}", f, d=6)
        kit.pop(f"travail{k + 2}", f + 4)
        kit.pulse("fiche_L3", f + 4, times=1, step=3, track="pulse")

    # ================= S14 : revenus, fiscalité, liquidités ; le conseil doit suivre =================
    f = kit.at("S14", "Ses", "le dernier cas et le « ou » se rangent en badge « travail » au-dessus du client")
    kit.vanish("travail4", f, into=list(BADGES[2]), d=MORPH)
    kit.vanish("ou_travail", f, d=6)
    kit.pop("badge_travail", f + 2, from_pt=CASE_C, to=list(BADGES[2]), d=MORPH)

    for (jid, leg, old, new, y, sens), word in zip(JAUGES, ("revenus,", "fiscalité", "liquidités")):
        fl = "↓" if sens < 0 else "↑"
        f = kit.at("S14", word, f"la barre « {leg} » sort du conseil et se pose dans la vie, légendée, avec le trait "
                                f"tireté de son niveau d'avant et une flèche {fl}")
        sortir(jid, f, (JAUGE_CX, y))
        kit.pop(f"{jid}_mot", f + 6)
        kit.pop(f"{jid}_fl", f + 8)

    f = kit.at("S14", "changent.", "les trois niveaux bougent ensemble dans le sens de leur flèche : revenus en baisse, "
                                   "fiscalité et liquidités en hausse ; les traits d'avant restent")
    for jid, leg, old, new, y, sens in JAUGES:
        S.key(jid, "value", f, new, MOVE, "inOut")
        kit.pulse(f"{jid}_fl", f, peak=1.3, step=4)

    f = kit.at("S14", "conseil", "« Toi » tend le bras et touche du stylo le bout du conseil : il tremble et son "
                                 "contour rouge bat")
    hit = toi.tap(f - TAP + 1, list(CONSEIL_TAP))
    kit.shake("conseil", hit, 6)
    kit.pulse("conseil_rouge", hit, times=2, step=2)
    toi.lower(hit + 6, 8)

    f = kit.at("S14", "suivre.", "trois fils encre se tracent du bout de chaque barre jusqu'au conseil et le tirent "
                                 "vers les nouveaux niveaux ; il est traîné vers elles et y reste, encore rouge et penché")
    for k in range(3):
        kit.draw(f"fil_jauge{k + 1}", f + 2 * k, 7)
    # contrôle muet (« les jauges tirent-elles le conseil ? ») : fils épais, traction franche, et le conseil RESTE
    # tiré vers les barres (encore rouge et penché) jusqu'à S15 « décisions »
    jerk = (CONSEIL_PULL[0] - 12, CONSEIL_PULL[1] - 14)
    S.key("conseil", "pos", f + 4, list(jerk), 8, "out")
    S.key("conseil", "pos", f + 12, list(CONSEIL_PULL), 8, "inOut")
