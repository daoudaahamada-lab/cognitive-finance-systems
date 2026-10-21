"""V02, partie 1 : S01-S07, images 0-922 (24 temps forts, 30,8 s). Le clic, le câble, le « ? » qui devient le repère
1-2-3, « open banking », la directive DSP2 qui devient la porte, l'interrupteur « Accès », le cadenas, la clé.

État d'entrée : l'image 0 de la distribution (cast), etat_initial de S01 : téléphone « Mon budget » (240, 760) et
bouton cyan (240, 890) ; « Toi » en P1 (500, 1135), stylo levé ; moitié droite vide. Rien à épingler.

Temps forts (image du film = round(t x 30), avant calage acoustique ; kit.at donne l'image exacte) :
S01  cliqué=9  « Connecter=32  banque »=49
S02  ce=109  autorisé ?=124
S03  trois=203  connectes=254  réflexe=310
S04  bouton,=359  l’open=385  banking.=394
S05  directive=434  DSP2,=470  ouvrir=520  comptes=559  autorisés.=594
S06  seulement=636  accord.=660  pirate=698  passe=734
S07  Pourquoi=790  identifiants ?=831  clés=886  compte.=902

Brief, scène par scène (ids de __init__.py ; aides : press, toggle, along, wire_point, vanish, bulle_ronds) :
- S01 « cliqué » : toi.tap(BOUTON_TAP), contact sur le mot (tap(f - TAP + 1, …)) ; press(S, contact) : le bouton
  s'enfonce dans son ombre. « Connecter » : kit.draw("cable", f) (300 ms) du téléphone vers la droite ; le bout libre
  s'arrête en CABLE_B. « banque » : kit.pop("banque", f) au bout du câble (le câble s'y accroche : rien à faire, pb est
  déjà sur son bord). Aucune autre forme.
- S02 « ce » : perle1 et perle2 naissent des barres de comptes (kit.pop from_pt compte1 / compte2), les barres ne
  bougent pas ; elles glissent le long du câble jusqu'au téléphone (along(S, "perleN", "cable", f, 15, 1, 0),
  décalées de 6 images) et s'y fondent (vanish). « autorisé ? » : kit.pop("question", f, from_pt=BOUTON_C) puis
  kit.move vers QUESTION_C en arc. Tenue.
- S03 « trois » : le « ? » se divise en alerte1-3 (kit.morph("question", [...]) puis kit.drop sur ALERTES_CABLE,
  décalées de 4 images) : on les compte. « connectes » : une pastille sort du bouton et parcourt le câble jusqu'à la
  banque, sous les alertes (along t 0 -> 1). « réflexe » : chaque alerte monte en arc sur son disque du repère
  (MARKER_XS, y 300) et s'y réduit pendant que le repère grandit (kit.morph(alertes, ["marqueur"], pair=False) ou
  vanish into le disque + kit.pop("marqueur")) ; la légende vient avec le repère ; AUCUN disque actif (piste on = 0).
- S04 « bouton, » : toi.tap(BOUTON_TAP) + press. « l’open » : kit.pop("open_banking", f, from_pt=BOUTON_C) puis
  kit.move vers OPEN_BANKING_C. « banking. » : une pastille sort du bouton et parcourt tout le câble jusqu'aux comptes.
- S05 « directive » : vanish("open_banking", into=[528, 790]) pendant que kit.drop("directive", f) tombe d'en haut
  sur DIRECTIVE_C (loin de la banque). « DSP2, » : kit.draw("directive_dsp2", f, 6, track="under"). « ouvrir » : la
  directive descend sur le câble et se change en porte (kit.move puis kit.morph(["directive"], ["porte"]) apparié) ;
  porte_dsp2 pop sur le linteau ; le câble plonge dans le tourniquet : S.key("cable", "via", f, PORTE_VIA, MORPH).
  « comptes » : kit.pulse(compte1/compte2, peak 1.1) ; une pastille sort des comptes et glisse jusqu'au tourniquet
  (along t 1 -> ~0.62, côté banque) où elle s'arrête. « autorisés. » : kit.pop("interrupteur", f, from_pt=BOUTON_C)
  (OFF) puis kit.fade("interrupteur_txt", f + 6). La pastille reste arrêtée.
- S06 « seulement » : la pastille avance de 14 px contre le tourniquet, bute et recule (path / key pos) ; kit.shake
  ("porte", f) ; l'interrupteur reste OFF. « accord. » : toi.tap(SWITCH_C) contact sur le mot, toggle(S,
  "interrupteur", contact, True) ; à contact + 1 la pastille franchit la porte jusqu'au téléphone (along), vanish.
  « pirate » : kit.pop("cadenas", f) sur le mur gauche de la banque ; rien ne s'en approche. « passe » : une pastille
  sort des comptes, passe le tourniquet et file jusqu'au bouton (along 700 ms) ; porte et porte_dsp2 battent au
  passage (kit.pulse peak 1.05) ; tenue.
- S07 « Pourquoi » : vanish("cadenas", into=mur) ; toi.walk(f, P2) (28 images). « identifiants ? » : kit.pop
  ("carte_id", f, from_pt=toi.tip(f)) se pose en CARTE_ID_C. « clés » : kit.morph(["carte_id"], ["cle"], f) apparié
  (la clé naît sur la carte). « compte. » : la clé monte en arc à COMPTES_EDGE (kit.move 12 images), y tourne d'un
  quart de tour (S.key rot 90, 6 images), compte1/2 battent (pulse 1.08), puis elle redescend en CLE_HOME à l'échelle
  CLE_SMALL en revenant droite (rot 0) ; tout fini avant l'image 922.

Raccord vers p2 : à l'image 922, l'état est exactement ENTRY_P2 (clé rangée en CLE_HOME à l'échelle 0,8, câble par la
porte, interrupteur ON, repère visible sans étape active, cadenas, alertes, « ? », carte, pastilles à l'échelle 0) ;
« Toi » arrêté en P2, stylo au repos. p2 épingle ENTRY_P2 à 922.
"""
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401

from . import (ALERTES_CABLE, BOUTON_C, BOUTON_TAP, CABLE_B, CARTE_ID_C, CLE_HOME, CLE_SMALL, COMPTES_EDGE,  # noqa: F401
               DIRECTIVE_C, MARKER_XS, MARKER_Y, OPEN_BANKING_C, P2, PORTE_VIA, QUESTION_C, SWITCH_C, along, press,
               scene_f0, toggle, vanish, wire_point)


def part(S, kit, c):
    pass
