"""V07, partie 2 : S10-S15, images 1045-1948 (erreur 1 : les noms et le MSCI World ; erreur 2 : le poids). 29 temps
forts, 30,1 s. La partie la plus dense (lecture au stylo S11, panier -> balance S12, pesée S14) : moins de temps forts.

ÉTAT D'ENTRÉE (etat_initial de S10, à épingler à 1044 : `kit.pin(f0 - 1, ENTRY_P2)` avec f0 = scene_f0(S, "S10")) :
« Toi » en P1 (660, 1135), bras baissé, dos au livre (look +1) ; repère `marqueur` sur 1 (on 1, active 0) sous
`titre_erreurs` « 3 erreurs » ; `livre` « Indice » (souligné) en LIVRE_C relié par `ficelle` au `panier` OUVERT
(PANIER_C, 10 titres light : titre1..7, titre9, titre10, titre_neuf) ; `etiquette` en ETIQ_C.
Garde-fou figurine (partie construite seule) : `if S.val("toi", "scale", f0 - 1) == 0: c.toi.enter(f0 - 10,
at=list(P1))` ; puis `kit.ensure("toi", "look", 0)` : dans le film entier look vaut +1 à f0 - 1 (posé par p1), en
partie seule 0 ; la clé look -> 0 de « Monde » marche dans les deux cas.

Temps forts (image du mot) :
S10  «Monde»,@1045  «États-Unis»,@1069  «Tech»:@1098  derrière@1121  indice@1172  règles.@1193
S11  Le@1216  MSCI@1223  exemple,@1296  couvre@1318  développés,@1344  mais@1371  émergents.@1393
S12  Ça@1418  savoir@1465  pèse@1488  pays.@1503
S13  Deuxième@1531  croire@1567  «Monde»@1590  équilibré.@1622
S14  indices@1664  taille@1713  entreprises,@1724  États-Unis@1762  pèsent@1779  70 %.@1824
S15  Ton@1868  «Monde»@1882  américain.@1919

BRIEF, scène par scène :
- S10 « Monde » : look +1 -> 0 ; {nom_monde} naît de {etiquette} (pop from_pt « etiquette ») et monte en (190, 520)
  (move 550) ; {ficelle} se retire (piste `from` 0 -> 1 : c'est l'état attendu par p3) ; {livre} passe SOUS la pilule
  (z) et se réduit en LIVRE_S10 x0,6 (move 550). « États-Unis » : {nom_usa} pop SUR PLACE (450, 520) — aucun lien
  avec le panier. « Tech » : {nom_tech} pop sur place (720, 520). « derrière » : {livre}, puis {livre_usa}, puis
  {livre_tech} (x0,6) glissent de 130 px vers le bas jusqu'à LIVRES_S10_Y (move 350 out, 4 images d'écart ; les deux
  autres livres : scale 0 -> 0,6 au départ, position y 560) ; {fil_nom_monde/usa/tech} se tracent (draw).
  « indice » : les trois livres battent (stagger 3, x1,08). « règles. » : sur chaque livre {<livre>_regle1..3} se
  tracent (stagger 3 de kit.draw) et leurs {<livre>_puce1..3} pop. Le panier et « Toi » ne bougent pas.
- S11 « Le » : {nom_monde} rentre dans {etiquette} (vanish into) ; {nom_usa}, {nom_tech}, {livre_usa}, {livre_tech}
  et les trois fils se réduisent sur place (4 images d'écart ; fils : opacité 0 en fin, état attendu par p3) ;
  {livre} grandit en LIVRE_S11 x1 (move 550). « MSCI » (7 images après « Le ») : {livre_titre} s'efface (FADE) et
  {livre_msci} « MSCI World » s'écrit (kit.type rate 1). « exemple, » : {panier} -> PANIER_S11 x0,7 et {etiquette}
  -> ETIQ_S11 x0,7 avec les MÊMES clés (move 550) ; « Toi » reste en P1 (les règles sont placées pour P1).
  « couvre » : {fil_livre_regle} se trace ; « Toi » lit : `c.toi.trace(f, [(REGLE_MARK_X, REGLE_Y[0]),
  (REGLE_TRACE_END_X, REGLE_Y[0])])` pendant que {regle1} s'écrit et que {regle1_coche} se trace au départ (coche
  HUMAINE pleine deep). « développés, » : {fil_regle_titres} (deep) se trace vers les titres du panier réduit, qui
  battent en vague (stagger 2, x1,15). « mais » : même lecture sur la 2e ligne (REGLE_Y[1]) pendant que {regle2}
  s'écrit. `lower` après. « émergents. » : {emergent1..3} sortent du bout de {regle2} (x ≈ REGLE_X + 250), sautent en
  arc 120 vers le panier (stagger 3), rebondissent (shake x 8) et tombent à EMERGENTS_SOL (kit.drop) ; {regle2_croix}
  se trace (kit.draw). Avant chaque geste : assert_reach(P1[0], …) (vérifié : 440 -> 570 sur les deux lignes).
- S12 « Ça » : {livre} se réduit dans le disque 1 (vanish into DISQUE_PT[0], MORPH) et une coche se trace dans le
  disque (`done0` 0 -> 1, 9 images) ; {regle1}, {regle2}, {regle1_coche}, {regle2_croix}, {fil_livre_regle},
  {fil_regle_titres}, {emergent1..3} sortent (morph sortie groupée). « savoir » : walk_low vers P2 ; {panier} revient
  en PANIER_BAL_C x1 et {etiquette} en (400, 1050) x1 (mêmes clés). « pèse » : MORPH 350 ms : {panier} se réduit
  vers le pivot (vanish, échelle 0 en fin ; ses titres partent avec lui) pendant que {balance} grandit en BALANCE_C
  (pop) ; {poids1..10} sautent des places des titres (position monde des titres à f - 1, S.parent_space) vers
  seat(SEATS_S12[k], TITRE_R) (stagger 1, arc 40) ; {etiquette} glisse vers ETIQ_BAL pendant que {ficelle_etiq}
  s'efface (draw 1 -> 0) et que {ficelle_etiq_bal} se trace (draw 0 -> 1). « pays. » : {poids} CYAN_SEATS passent au
  cyan (piste fill hex, 9 images) ; {pil_usa} et {pil_autres} pop. La planche reste à plat (autant de chaque côté).
- S13 « Deuxième » : kit.step(f, 1) (le disque actif glisse de 1 à 2 « Poids » ; done0 reste 1). « croire » :
  {bulle2_rond1..3} montent de la tête de « Toi » en P2 (stagger 2 de pop), {bulle2} s'ouvre avec sa mini balance à
  plat ({bulle2_balance}, {bulle2_jeton1..4}, enfants : ils viennent avec elle). « Monde » : {etiquette} bat (x1,15).
  « équilibré. » : {bulle2_coche} se trace (coche pleine deep). La mini balance ne bouge pas.
- S14 « indices » : le disque 1 coché bat (pulse sur le marker impossible par disque : faire battre tout le marker à
  x1,08, ou rien de plus qu'un `done0` déjà posé — choisir le pulse du marker). « taille » : {poids} prennent leur
  taille (scale -> S14_R[k] / TITRE_R, SCALE 10 images ; y du siège : seat(x, r) en même temps). « entreprises, » :
  {poids} glissent par pays vers S14_X (move arc 30, 550 inOut). « États-Unis » : {pil_usa} bat (x1,15). « pèsent » :
  {balance} rot 0 -> TILTS["S14"] (TILT 14 images, out) ; dans les mêmes images {bulle2} et tout son contenu + ses
  ronds éclatent (vanish 300 ms). « 70 %. » : {compteur} pop en COMPTEUR_C et compte 0 -> 70 (15 images out).
- S15 « Ton » : {etiquette} bat (x1,15). « Monde » : {lien_rouge} se trace (draw, 9 images) de l'étiquette au géant
  {poids1}. « américain. » : les 5 {poids} cyan et {compteur} battent ensemble (x1,12) ; tenue jusqu'à 1948.

PASSAGE À p3 (image 1948 = ENTRY_P3 de __init__, exactement) : balance BALANCE_C rot -12, poids à seat(S14_X, S14_R)
et à leur échelle S14_R/26 (cyan / light en hex), panier échelle 0 en PANIER_BAL_C, livre échelle 0 en DISQUE_PT[0],
étiquette en ETIQ_BAL (ficelle_etiq draw 0, ficelle_etiq_bal draw 1), ficelle from 1, lien_rouge tracé, compteur
70 en COMPTEUR_C, pil_usa / pil_autres à leur place, marqueur active 1 / done0 1 / done1 0, fils de S10-S11 à
opacité 0, bulle2 et ronds à 0 ; « Toi » en P2, bras baissé, look 0.

Règles : bras baissé entre deux gestes ; « Toi » ne bouge que par walk_low / reach / tap / trace / lower ; rouge
uniquement pour {compteur} et {lien_rouge} ; aucun gris ; aucune coche variant « ai ».
"""
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP, SCALE, TILT  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401

from . import *  # noqa: F401,F403


def part(S, kit, c):
    pass
