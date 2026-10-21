"""V02, partie 3 : S15-S22, images 1802-2677 (33 temps forts, 29,2 s). Erreur 3 « Accès » (l'appli testée branchée
par « Toi », le cadran des mois, l'appli oubliée qui reçoit encore des données, coupée des deux côtés), la chute
Avant / Maintenant sur le même montage (alertes numérotées -> coches de « Toi »), la carte de fin.

État d'entrée, épinglé à l'image 1801 : kit.pin(1801, ENTRY_P3) (etat_initial de S15 : fil de preuve tendu du
registre au badge coché ; champ vide, « gratuit », « ACPR » ; repère sur 2). Figurines : `toi` en P2 (garde-fou :
if S.val("toi", "scale", 1801) == 0: c.toi.enter(1792, at=P2)) ; `societe` en SOCIETE_C (garde-fou : si son échelle
vaut 0 à 1801, c.societe.enter(1792, at=SOCIETE_C)).

Temps forts (image du film = round(t x 30), avant calage acoustique ; kit.at donne l'image exacte) :
S15  Et=1802  s’arrête=1828  jour=1853  connectes.=1879
S16  Troisième=1910  oublier=1954  accès=1973  n’utilises=1996
S17  6=2073  encore=2095  actif.=2127
S18  Coupe-le=2152  réglages=2173  l’appli.=2189  propose,=2237  espace=2278  aussi.=2299
S19  Avant,=2325  tu=2345  cliquais=2350  sans=2362  réfléchir.=2369
S20  Maintenant,=2398  t’identifies=2430  banque=2461  vérifies=2487  REGAFI.=2507
S21  Et=2529  6=2542  tri.=2570
S22  Abonne-toi=2589  comprendre=2617  argent.=2638

Brief, scène par scène (ids de __init__.py) :
- S15 « Et » : un seul morph de rangement (350 ms) : registre, champ, gratuit et preuve se réduisent (kit.morph(...,
  [])), la société remonte derrière le téléphone (c.societe.hop vers SOC_HIDDEN, z 3 sous lui, puis c.societe.exit à
  l'arrivée), le badge (plein, coché) glisse en BADGE_UNDER_PHONE et y reste (kit.move). « s’arrête » :
  kit.pop("testee", f) en bas à droite, interrupteur OFF, aucun câble. « jour » : kit.pop("cadran", f) vide.
  « connectes. » : toi.tap(TESTEE_SWITCH) contact sur le mot (le bras croise le buste : toi.rim(…, True) avant, False
  avant que le bras se replie) ; toggle(S, "testee_inter", contact, True) ; à contact + 4 kit.draw("cable_testee", 9)
  depuis la banque ; dans les mêmes images S.key("cadran", "value", contact, 6, kit.at("S17", "6") - contact,
  "linear") : la seule dérive du film, jusqu'à « 6 » (S17).
- S16 « Troisième » : kit.step(f, 2). « oublier » : toi.stow(f) puis toi.walk vers P1 (26 images), dos à l'appli
  testée. « accès » : kit.pulse("testee_inter", times=2, step=3) (toujours ON). « n’utilises » : S.key("testee",
  "fill", f, GREY, 9) et kit.pop("testee_lune", f) : écran éteint, câble toujours branché.
- S17 « 6 » : le secteur arrive à 6 (fin de la clé posée en S15) ; kit.pop("cadran_txt", f) « 6 mois ». « encore » :
  perle1-3 sortent du bas de la banque et coulent le long de cable_testee jusque dans l'appli endormie (along(S,
  "perleN", "cable_testee", …), décalées de 6 images), la lune ne bouge pas. « actif. » :
  kit.pulse("testee_inter", times=2) pendant que la dernière pastille s'y fond.
- S18 « Coupe-le » : toi.unstow(f) et toi.walk vers P2 (20 images). « réglages » : toi.tap(TESTEE_SWITCH) contact sur
  le mot ; toggle(S, "testee_inter", contact, False). « l’appli. » : le bout du câble se détache et pend : S.key
  ("cable_testee", "pb", f, [860, 1075], 9, "out") et S.key(…, "sag", f, 50, 9). « propose, » :
  kit.pop("espace_client", f, from_pt=BANK_BOTTOM) : le panneau sort de la banque (interrupteur ON). « espace » :
  toi.tap(ESPACE_SWITCH) contact sur le mot ; toggle(S, "espace_inter", contact, False). « aussi. » : le câble pendant
  rentre dans la banque : kit.draw("cable_testee", f, 9, to=0).
- S19 « Avant, » : kit.pop("etiquette_avant", f) ; un seul mouvement visible : kit.draw("cable_testee", f, 12) (le
  câble ressort et se rebranche : remettre pb / sag à leur place AVANT, à f - 1) et toggle(S, "testee_inter", f,
  True) ; les petites pièces se réduisent ensemble (300 ms) : espace_client (vanish into BANK_BOTTOM), cadran et
  cadran_txt, cle_coche (draw -> 0), badge_plein et badge_coche (draw -> 0 : le badge repasse en tirets). « tu » :
  toi.hop(f, P1, 14). « cliquais » : toi.tap(BOUTON_TAP, d=6) contact sur le mot ; press(S, contact) ; une pastille
  file de la banque au bouton (along "cable" t 1 -> 0, 12 images). « sans » : bulle_rond1-3 puis bulle ressortent de
  la tête de « Toi » (P1) en BULLE_S19 (places des ronds : bulle_ronds(tête P1, coin de la bulle) ; kit.move les ronds
  à f - 1 en scale 0, puis kit.pop décalés de 3 images) ; bulle_txt, bulle_fleche, bulle_tel déjà pleins (S08).
  « réfléchir. » : de chaque disque du repère tombe une alerte numérotée (alerteN : pos au disque MARKER_XS[N], pop
  depuis le disque puis kit.drop vers ALERTES_S19, décalées de 8 images ; alerteN_num opacity 1 ; le marqueur bat à
  chaque départ) : 1 sur l'écran du téléphone, 2 à gauche du badge, 3 sur le câble de l'appli testée. Tenue.
- S20 « Maintenant, » : kit.morph(["etiquette_avant"], ["etiquette_maint"], f) ; toi.walk(f, P2, 24). « t’identifies »
  : toi.tap(CLE_HOME) contact sur le mot ; kit.draw("cle_coche", contact, 6). « banque » : la bulle tremble puis
  éclate (kit.shake, vanish, ronds avec elle) ; alerte1 -> alerte1_ok : kit.morph(["alerte1"], ["alerte1_ok"], f)
  apparié (pos alerte1_ok à ALERTES_S19[0] à f - 1) puis kit.draw("alerte1_ok_coche", f + MORPH, 6). « vérifies » :
  le registre revient plus petit : pos REGISTRE_S20, échelle REGISTRE_S20_SCALE (kit.pop from_pt [480, 1230]) avec
  titre, inscriptions et nom surligné déjà là (chars, mark à 1 ; registre_coche à 0 ; registre_acpr, registre_tel*
  à 1) ; toi.reach vers le nom. « REGAFI. » : toi.tap(nom du livre) contact sur le mot ; preuve : pa = nom (monde),
  pb = badge en BADGE_UNDER_PHONE, draw 0 -> 1 (9 images) ; à l'arrivée badge_plein et badge_coche se retracent ;
  alerte2 -> alerte2_ok (morph) et sa coche.
- S21 « Et » : vanish registre et preuve (vers le centre du livre) ; « Toi » reste en P2. « 6 » : kit.pop("cadran",
  f) puis S.key value 0 -> 6 (9 images, out), 6 -> 0 (2 images), 0 -> 6 (9 images) : la routine boucle ;
  kit.type("cadran_routine", f) « tous les 6 mois » sous le cadran. « tri. » : toi.tap(TESTEE_SWITCH) contact sur le
  mot ; toggle(S, "testee_inter", contact, False) ; kit.draw("cable_testee", contact + 2, 12, to=0) (le câble rentre
  dans la banque) ; alerte3 -> alerte3_ok (morph) qui glisse en ALERTE_OK_S21 et sa coche se trace. Tenue.
- S22 « Abonne-toi » : S.key("bouton", "text", f - 1, "S’abonner") (avant tout mouvement) ; out =
  kit.outro("S22", outs=[tout ce qui est à l'écran sauf le bouton et les figurines], press="argent.") ; toi.exit
  (out["card"]) ; le bouton (z à passer au-dessus de 40) descend et grandit jusqu'au bouton de la carte : centre
  (540, 760 + 260 - 56 - 56) = (540, 908), S.key("bouton", "w", …, 380 / 1.7) et scale 1.7 (≈ 380 x 112, texte
  ≈ 46 px) en 11 images ; puis relais instantané au moment où le bouton de la carte est entier (out["card"] + 6 +
  POP) : bouton et bouton_ombre opacity 0. Les câbles (wire, dessinés en monde) sortent par draw -> 0 ou opacity, pas
  par un vanish d'échelle. « comprendre » : tenue (le pointeur glisse, géré par kit.outro). « argent. » : clic (par
  kit.outro) ; plus rien ne bouge ensuite.
  Pour le décompte : kit.hold("S22", "comprendre", …) si outro ne pose pas ce temps fort.

Fin du film : image 2677 ; la carte reste immobile jusqu'au bout.
"""
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401

from . import (ALERTES_CABLE, BADGE_UNDER_PHONE, BANK_BOTTOM, BOUTON_TAP, BULLE_S19, CLE_HOME, ENTRY_P3,  # noqa: F401
               ESPACE_SWITCH, FIN_BUTTON, GREY, MARKER_XS, P1, P2, REGISTRE_S20, REGISTRE_S20_SCALE, SOC_HIDDEN,
               SOCIETE_C, ALERTES_S19, ALERTE_OK_S21,
               TESTEE_SWITCH, along, bulle_ronds, press, scene_f0, toggle, vanish)


def part(S, kit, c):
    pass
