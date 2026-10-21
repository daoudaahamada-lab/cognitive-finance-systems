"""V02, partie 2 : S08-S14, images 923-1801 (31 temps forts, 29,3 s). Erreur 1 « Codes » (bulle de pensée « Mot de
passe », clé touchée à la banque, appli qui réclame les codes, barrée puis rouge) et erreur 2 « Société » (la société
derrière l'appli, son badge en tirets, le registre REGAFI de l'ACPR, le badge prouvé et coché).

État d'entrée, épinglé à l'image 922 : kit.pin(922, ENTRY_P2) (etat_initial de S08 : clé rangée dans la banque en
CLE_HOME à l'échelle 0,8, câble par la porte DSP2, interrupteur « Accès » sur ON, repère visible sans étape active ;
l'espace sous la porte est vide). Figurines : `toi` en P2 (garde-fou : if S.val("toi", "scale", 922) == 0:
c.toi.enter(913, at=P2)) ; `societe` à l'échelle 0, cachée en SOC_HIDDEN derrière le téléphone (z 3 < 4).

Temps forts (image du film = round(t x 30), avant calage acoustique ; kit.at donne l'image exacte) :
S08  Première=923  croire=957  l’appli=974  passe.=1012
S09  t’identifies=1074  banque,=1103  pas=1122  l’appli.=1133
S10  Une=1155  demande=1175  directement=1189  codes=1217  Méfiance.=1250
S11  Ça=1275  connexion=1310  société=1361  face.=1379
S12  Deuxième=1404  vérifier=1443  qui=1463  derrière=1472  l’appli.=1484
S13  France,=1516  enregistrés=1567  l’ACPR.=1613
S14  vérifier=1655  gratuitement=1669  REGAFI,=1714  tapant=1744  nom=1758  société.=1770

Brief, scène par scène (ids de __init__.py) :
- S08 « Première » : le repère s'allume sur 1 : S.key("marqueur", "on", f, 1, MOVE, "out") (active reste 0) ;
  « Codes » passe à l'encre. « croire » : bulle_rond1-3 pop un à un depuis la tête de « Toi » (décalés de 3 images),
  puis kit.pop("bulle", f + 9, from_pt=tête). « l’appli » : kit.pop("bulle_tel"), kit.type("bulle_txt"),
  kit.pop("bulle_fleche") : « Mot de passe -> téléphone ». « passe. » : kit.pulse("cle", peak 1.08 x échelle) sans
  bouger ; kit.pulse("bulle") ; tenue (la bulle reste vide de toute clé).
- S09 « t’identifies » : toi.tap(CLE_HOME) contact sur le mot ; kit.draw("cle_coche", contact, 6). « banque, » : une
  pastille sort des comptes, passe le tourniquet et file jusqu'au bouton (along "cable" t 1 -> 0, 650 ms) ; la clé ne
  bouge pas. « pas » : la pastille se fond dans le bouton ; kit.shake("bulle"). « l’appli. » : la bulle et ses ronds
  éclatent (vanish, ronds décalés de 2 images). Fini avant 1155.
- S10 « Une » : douteuse : pin pos DOUTEUSE_START + scale 1 à f - 1, kit.move vers DOUTEUSE_C (550 ms). « demande » :
  kit.type("douteuse_txt", f, rate=1) ; kit.pop("douteuse_champ"). « directement » : kit.draw("douteuse_fil1", f, 5)
  puis kit.draw("douteuse_fil2", f + 5, 5) : un fil en tirets, droit, du champ vers la capsule, à droite de la porte
  sans la traverser. « codes » : le bout du fil touche la capsule et recule de 10 px (S.key "douteuse_fil2" "pb") ;
  kit.shake("cle"). « Méfiance. » : toi.strike(f, a, b) en travers de DOUTEUSE_FIL_MID (le stylo barre le fil) ; à
  la fin du trait les deux moitiés pendent (pb de fil1 et pa de fil2 descendent, sag) ; À L'IMAGE SUIVANTE seulement :
  S.key("douteuse", "stroke", …, RED, 9) et S.key("douteuse_txt", "color", …, RED, 9), kit.shake("douteuse").
  Toi.strike exige un pas ? place_for avant (toi.walk) : jamais de pas automatique pendant le trait.
- S11 « Ça » : kit.drop("douteuse", f, out=True) et les deux moitiés du fil avec elle (draw -> 0 ou opacity). Fini
  avant « connexion ». « connexion » : une pastille part de la banque, franchit la porte et rejoint le bouton (along).
  « société » : la société sort de derrière le téléphone : c.societe.enter(f - POP - 1, at=SOC_HIDDEN) (cachée, z 3),
  puis c.societe.hop(f, SOCIETE_C, MOVE) ; le badge (vide, en tirets, pictogramme d'immeuble) arrive avec elle :
  kit.pop("badge", …) sur sa poitrine à l'arrivée (BADGE_ON_SOC), ou suivi en même temps (z 16 : au-dessus du
  téléphone, donc ne le montrer qu'à la sortie du téléphone). « face. » : c.societe.lean_to(f, 5) vers « Toi ».
- S12 « Deuxième » : kit.step(f, 1) (le disque actif glisse sur 2, « Société » à l'encre). « vérifier » :
  kit.pop("question2", f, from_pt=toi.tip(f)) puis kit.move vers QUESTION2_C en arc. « qui » : kit.pulse("badge_fond",
  times=2) (contour seul si possible, sinon le badge entier) ; il reste vide. « derrière » : kit.type("badge_nom",
  rate=1) ; le contour reste en tirets. « l’appli. » : kit.pulse("question2", times=2, step=3) ; tenue.
- S13 « France, » : le registre monte du bas : kit.pop("registre", f, from_pt=[480, 1200]). « enregistrés » :
  registre_tel1-3 tombent dans leurs rangées (kit.drop, décalés de 4 images) et registre_trait1-3 se tracent
  (kit.draw) : des applis inscrites. « l’ACPR. » : registre_acpr tombe d'en haut de l'image (kit.drop h grand, comme
  la directive) sur la page de droite.
- S14 « vérifier » : kit.pop("champ", f) ; toi.reach(f, CHAMP_TAP) (stylo levé vers le champ). « gratuitement » :
  kit.pop("gratuit", f) collé au bout du champ. « REGAFI, » : kit.type("registre_titre", f, rate=1). « tapant » :
  toi.tap(CHAMP_TAP) contact sur le mot ; kit.type("champ_nom", contact, rate=1). « nom » : le nom tapé quitte le
  champ et descend sur la rangée du milieu (S.fly("champ_nom", …, to=monde de registre_nom) puis relais instantané :
  champ_nom opacity 0, registre_nom chars plein) ; registre_trait2 vanish ; kit.draw("registre_nom", …, track="mark").
  « société. » : toi.tap(registre_nom) contact sur le mot ; kit.draw("registre_coche") ; S.set/S.key("preuve", pa =
  monde du nom, pb = bord droit du badge) puis kit.draw("preuve", 9) ; à l'arrivée kit.draw("badge_plein", 6) (le
  contour devient plein deep), kit.draw("badge_coche", 6), vanish("question2"). Tout fini avant 1802.

Raccord vers p3 : à l'image 1801, l'état est exactement ENTRY_P3 (registre en REGISTRE_C avec titre, inscriptions, nom
surligné et coché, ACPR ; champ vide (champ_nom chars 0, opacité 0) ; « gratuit » ; fil `preuve` tracé ; badge en
BADGE_ON_SOC plein et coché ; question2, bulle, douteuse à l'échelle 0 ; repère active 1, on 1 ; clé cochée) ;
« Toi » arrêté en P2, stylo au repos ; société posée en SOCIETE_C.
"""
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401

from . import (BADGE_ON_SOC, CHAMP_TAP, CLE_HOME, DOUTEUSE_C, DOUTEUSE_FIL_MID, DOUTEUSE_START, ENTRY_P2,  # noqa: F401
               P2, QUESTION2_C, RED, REGISTRE_C, SOC_HIDDEN, SOCIETE_C, along, scene_f0, vanish)


def part(S, kit, c):
    pass
