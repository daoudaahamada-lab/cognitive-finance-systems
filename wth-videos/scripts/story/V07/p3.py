"""V07, partie 3 : S16-S22, images 1949-2967 (erreur 3 : les doublons ; la chute : 3 questions, avant / après ; fin).
30 temps forts, 33,9 s.

ÉTAT D'ENTRÉE (etat_initial de S16, à épingler à 1948 : `kit.pin(f0 - 1, ENTRY_P3)` avec f0 = scene_f0(S, "S16")) :
`balance` à -12° côté États-Unis, ses `poids` rangés par pays (3 géants cyan r 32, 2 cyan r 18 à gauche ; 5 light
r 17 à droite), `lien_rouge` de l'`etiquette` (ETIQ_BAL, pendue au pivot par `ficelle_etiq_bal`) au géant `poids1`,
`compteur` « ≈ 70 % » rouge en COMPTEUR_C au-dessus de `pil_usa`, `pil_autres` à droite ; repère sur 2 (done0 1) ;
« Toi » en P2 (860, 1135), bras baissé. Garde-fou figurine : `if S.val("toi", "scale", f0 - 1) == 0:
c.toi.enter(f0 - 10, at=list(P2))`.

Temps forts (image du mot) :
S16  Et@1949  voulant@1974  corriger@1983  aggrave@2010  choses.@2023
S17  Troisième@2046  empiler@2085  ETF@2108  ressemblent.@2138
S18  Monde,@2197  S&P@2252  Nasdaq ?@2337
S19  plusieurs@2381  mêmes@2403  lignes,@2463  pas@2489  diversification.@2504
S20  Le@2544  réflexe@2556  trois@2586  questions.@2593  indice ?@2629  dedans ?@2685  coûte@2723
S21  nom@2761  suffit@2769  composition,@2839  si.@2862
S22  Abonne-toi@2883  argent.@2929   (film : dernière image 2967)

BRIEF, scène par scène :
- S16 « Et » : {lien_rouge} se retire (`from` 0 -> 1, 9 images) ; {pil_usa} -> PIL_USA_HAUT et {compteur} ->
  COMPTEUR_HAUT, x HAUT_K (move 550). « voulant » : c.toi.reach vers PB_NEE (assert_reach(P2[0], PB_NEE, …)).
  « corriger » : {pb1} (enfant de la balance, ouvert, titres cyan {pb1_geant1..3}, {pb1_petit1..2} déjà dedans) naît
  de la pointe (pop from_pt = PB_NEE, échelle PB_K) puis se pose en PB_POSE (drop). `lower`. « aggrave » : {pb1}
  glisse le long de la planche vers PB1_SEAT (move 550 « in ») ; {balance} -12 -> TILTS["S16"] (TILT). « choses. » :
  {compteur} et {pil_usa} battent (x1,15) ; tenue.
- S17 « Troisième » : kit.step(f, 2) et `done1` 0 -> 1. « empiler » : {pb2} naît de la pointe (même geste) et tombe
  sur {pb1} en PB2_SEAT (drop) ; {balance} -> TILTS["S17"]. « ETF » : {pb1} puis {pb2} battent (stagger 4, x1,1).
  « ressemblent. » : {poids} géants (GEANTS) + {pb1_geant*} + {pb2_geant*} battent sur la même image (x1,2).
- S18 « Monde, » : {etiquette} bat (x1,15). « S&P » : {etiq_sp} sort de {pb1} (pop from_pt « pb1 ») vers ETIQ_SP_C
  (move 350), {ficelle_etiq_sp} se trace. « Nasdaq ? » : idem {etiq_nq} -> ETIQ_NQ_C, {ficelle_etiq_nq} ; 8 images
  après, {etiq_sp}, {etiq_nq} et {pil_usa} battent ensemble (x1,1).
- S19 « plusieurs » : les géants battent en trois temps : planche, puis {pb1}, puis {pb2} (stagger 5, x1,25).
  « mêmes » : {fois3} « ×3 » rouge pop en FOIS3_C. « lignes, » : {ficelle_etiq_bal}, {ficelle_etiq_sp},
  {ficelle_etiq_nq} se retirent (`from` -> 1) ; {etiquette}, {etiq_sp}, {etiq_nq} se rangent en ETIQ_LISTE (stagger 4
  de move 450 ; l'étiquette 240 px, les sœurs 260 : aligner leurs bords gauches si besoin) ; {liste_titre} « 3 ETF »
  pop en LISTE_TITRE_C. « pas » : c.toi.reach vers (690, 990) (le groupe « autres pays »). « diversification. » :
  {place_vide} (enfant de la balance, au bout droit de la planche) pop, son contour bat deux fois (pulse), elle
  RESTE vide ; `lower`.
- S20 « Le » : {pb1}, {pb2}, {etiq_sp}, {etiq_nq}, {fois3}, {liste_titre}, {place_vide}, {pil_autres} sortent
  (morph sortie groupée) ; {etiquette} revient pendre sous le pivot en ETIQ_BAL (move 450) avec {ficelle_etiq_bal}
  retracée (from 1 -> 0 ou draw) ; {balance} revient à plat (rot 0, TILT). « réflexe » : MORPH : {balance} se réduit
  pendant que {panier} renaît en PANIER_BAL_C puis va en PANIER_C (sans couvercle) ; les {titre*} (titre1..7, 9, 10,
  titre_neuf) reparaissent derrière le rebord AVEC leurs couleurs et tailles (poser fill / scale pendant qu'ils sont à
  0 : 5 cyan dont 3 géants x32/26, 5 light x17/26 ; garder des places sans chevauchement), les {poids} se réduisent ;
  {pil_usa} et {compteur} rentrent dans un titre cyan (vanish into) ; {etiquette} remonte en ETIQ_C et {ficelle_etiq}
  se retrace ; walk_low vers P1. « trois » : relais {marqueur} -> {marqueur2} et {titre_erreurs} -> {titre_questions}
  (kit.morph pair, mêmes places ; marqueur2 on 0). « questions. » (7 images après) : {fiche} tombe (kit.drop, échelle
  FICHE_K ; lignes vides, {fiche_tirets1..3} en tirets). « indice ? » : {marqueur2} on 0 -> 1 (étape 1) ; {livre}
  ressort du disque 1 (pop from_pt DISQUE_PT[0], petit : x0,3) et file vers la puce de {fiche_L1}
  (c.sheet.world(S, 0, "bullet", n=f)), s'y réduit (vanish into) ; {fiche_tirets1} s'efface, `bulletOn` 1 et
  kit.type(fiche_L1, flash=True). « dedans ? » : kit.step(f, 1, id="marqueur2") ; {saut_geant} (copie d'un géant du
  panier : l'original reste) saute en arc 80 vers la puce de {fiche_L2}, s'y réduit ; type L2. « coûte » : step 2 ;
  {frais_etf} ressort de {etiquette} (pop from_pt « etiquette ») et file vers la puce de {fiche_L3} ; type L3.
- S21 « nom » : {panier_couvercle} retombe (drop) en COUVERCLE_LOCAL (enfant du panier) ; les titres se cachent
  sous lui sur la même image (échelle 0 à l'image du contact). « suffit » : tap ETIQ_TAP (assert_reach(P1[0], …)) ;
  {etiquette} tremble (shake x 8), rien n'en sort. « composition, » : tap COUVERCLE_TAP ; le couvercle s'envole en
  arc vers le haut à gauche et se réduit ; les titres colorés reparaissent (pop) ; {fiche} bat (x1,06).
  « si. » : tap REBORD_TAP ; {panier_coche} se trace au contact (coche pleine deep 48) ; `lower` ; tenue.
- S22 « Abonne-toi » : fin standard comme V06 p3 : `kit.outro("S22", outs=[], btn_at=MOVE, press="argent.",
  pos=FIN_C, …)` ; tout ce qui reste ({panier} et parts, titres, {fiche}, {marqueur2}, {titre_questions}) s'efface
  (vanish into FIN_C ou clear "fade") ; S.set(out["cursor"], opacity=0) (aucun pointeur) ; {etiquette} : `textOp`
  1 -> 0, texte « S’abonner » (T_ABONNER), textOp -> 1, z au-dessus de la carte (kit.ensure z puis clé 41), w -> 380
  et move vers FIN_BUTTON (scale BTN_H/ETIQ_H en hauteur : h 60 -> 112, ou garder h et laisser le bouton relayer à
  btn_at), opacité 0 à btn_at (relais exact) ; walk_low vers P_FIN pendant le morph ; c.toi.set_z(…, tool_z=44) ;
  « argent. » : tap FIN_TAP (contact = image du clic `out["press"]`), {fin_onde1..2} (ring) ; `lower`. Puis plus rien
  ne bouge jusqu'à 2967.

Règles : jamais de VALIDÉ ; la place vide reste vide ; rouge seulement {compteur}, {fois3} (et {lien_rouge} qui se
retire) ; pas de gris ; « Toi » seul tient le stylo, bras baissé entre deux gestes ; tout ce qui est visible à la
dernière image ne se chevauche pas.
"""
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, SCALE, TILT  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401

from . import *  # noqa: F401,F403


def part(S, kit, c):
    pass
