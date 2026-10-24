"""V13, partie 3 : S16-S22, images 1916-2767 (36 temps forts, 28,4 s). Point 3 « Limites » : « Patrimoine net » ressort
de la grille avec un signe d'attention, six pastilles montrent ce qu'il mélange, deux restent (liquidité, risques),
un point « repère » commence une courbe de mesures (deux creux, écart premier / dernier point) ; chute : l'équation
complète, « Toi » barre son regard rouge vers le solde et regarde le Patrimoine net ; fin : la pilule du solde devient
le bouton « S’abonner ».

ÉTAT D'ENTRÉE : ENTRY_P3 épinglé à 1915 (`kit.pin(f0 - 1, ENTRY_P3)`, f0 = scene_f0(S, "S16") = 1916) : etat_initial
de S16 = résultat de S15 (grille réduite GRILLE_SMALL complète, case « Immobilier » avec son cercle en tirets ; pilule
du solde SOLDE_CELL_SMALL ; jeton JETON_P2 (×JETON_P2_K) ; étiquette ETIQ_P2 « Valeur actuelle · 250 000 € » ; barre
courte BARRE_SHORT_C ; « ≈ 70 000 € nets » RESULTAT_C ; calcul écrit ; part grise rentrée dans le disque 2 ; repère
étape 2, done0). « Toi » en P1 (visible dès l'image 0 : ne pas l'épingler, ne pas le faire entrer).
SORTIE : fin du film (image 2767, FILM_END = 2768) ; plus rien ne bouge après le toucher (≈ 2740) : la QA dispense
la dernière scène du contrôle d'image figée.

Ids : grille, cases (CASE_IDS, case_immo_place), compte, solde, marqueur, jeton, etiquette (+ enfants), ficelle_jeton,
barre, resultat, calc_a, calc_b, net (+ net_trait, ne plus le tracer), alerte, fil_net, past_disponible / past_bloque /
past_sur / past_risque / past_estime / past_reel (+ _ico, _mot ; past_estime_approx), axes, axe_y_pointe,
axe_x_pointe, axe_y_mot, axe_auj, grad1-3 (+ _mot), point1-8, courbe, graphe_freq, axe_onde, ecart_h, ecart_v,
ecart_haut, ecart_bas, dettes (+ enfants : revenir à la forme carte DETTES_W x DETTES_H, dettes_mot T_DOIS_CARTE en
DETTES_MOT_CARD, dettes_ico DETTES_ICO_CARD échelle 1, dettes_val échelle 0), moins, egal, regard, regard_barre,
regard_net, leg_possedes, leg_dois, leg_limites, toi (c.toi), nom_toi, fin_doigt, fin_onde1-2.

BRIEF, scène par scène (images = round(t × 30), avant calage acoustique) :
- S16 (1916-2025) « Dernier » (1916) : kit.step(f, 2) ; S.key("marqueur", "done1", f, 1, DRAW). « point, » (1928) :
  kit.stagger(["calc_b", "calc_a", "resultat", "barre", "etiquette"], f, 2, kit.vanish, into="jeton") (ficelle_jeton
  rétractée, draw 0) ; puis le jeton revient dans sa case : kit.move("jeton", …, JETON_SMALL, scale=JETON_SMALL_K)
  (MOVE) ; case_immo_place s'efface à l'arrivée. « moindre : » (1957) : net : échelle 0.85 ; kit.pop("net", f,
  scale=NET_P3_K, from_pt=NET_FROM_GRID) puis kit.move vers NET_P3 (MOVE) (le total de toute la grille) ; net_trait
  reste à draw 0. « chiffre » (1984) : kit.pulse("net", f, step=3, peak=1.1 × 0.85). « limites. » (2002) :
  kit.pop("alerte", f) en ALERTE_C (encre, jamais rouge) ; au même moment la légende 3 « Limites » du repère bat (pas de
  piste de légende : kit.pulse("marqueur", …) ferait battre tout le repère ; préférer un `text` « Limites » posé
  exactement sur la légende 3 (MARKER_LEGENDS[2], Bold 34) qui bat, ou tout le repère avec peak 1.05 : à décider sur
  image fixe).
- S17 (2026-2190) « mélange » (2032) : kit.draw("fil_net", f, 9). Puis chaque pastille sort de sa case sur son mot
  (pop from_pt de l'origine monde : cell_world(i, True) ; -1 = SOLDE_CELL_SMALL ; 6 = JETON_SMALL) et va à sa place
  PASTILLES[id][2] (kit.move 13 images, arc 60) : « disponible » (2046), « bloqué, » (2075), « sûr » (2096),
  « risqué, » (2115), « l’estimé » (2136), « réel. » (2166) ; puis tenue. Toujours une seule pastille en mouvement.
- S18 (2191-2313) « Utilise-le » (2191) : sûr, bloqué, réel, estimé rentrent dans leur case (kit.vanish into, décalés
  de 2 images) ; disponible et risqué -> PAST_GARDE (MOVE) ; kit.draw("fil_net", f, 6, track="from") puis draw / from
  à 0. « comme » (2210) : kit.draw("axes", f, 9) ; pointes d'axe pop à la fin ; axe_y_mot, axe_auj, grad1-3, grad1-3_mot
  en fondu (FADE). « repère, » (2216) : point1 posé en NET_P3 (bas de la pilule) échelle 0 à f - 1, kit.pop puis
  kit.move vers POINTS[0] (MOVE, arc 60) : le repère tombe de la pilule. « liquidité » (2261) :
  kit.pulse("past_disponible", f, step=3, peak=1.08) ; S.key("past_disponible_mot", "under", f, 1, 9). « risques. »
  (2294) : idem pour past_risque.
- S19 (2314-2432) « calcule-le » (2319) : c.toi.unstow ; hit = c.toi.tap(f, AXE_TAP) ; ring(S, "axe_onde", hit).
  « une » (2339) : kit.pop("graphe_freq", f) en FREQ_C (écart : voir __init__). « fois » (2352) :
  kit.stagger(point2-8, f, 3, kit.pop) ; c.toi.lower. « évolution » (2395) : kit.draw("courbe", f, 18, e="linear")
  (par les 8 points, deux creux). « compte. » (2414) : kit.pulse point1 et point8 ensemble (peak 1.4, step 3) ;
  kit.draw("ecart_h", f + 6, 6) ; kit.draw("ecart_v", f + 12, 9) ; ecart_haut / ecart_bas pop à la fin du trait.
- S20 (2433-2525) « Retiens » (2433) : graphe (axes, pointes, légendes, graduations, points, courbe, graphe_freq,
  écart), past_disponible, past_risque et alerte : kit.vanish(into="net") ; net -> NET_CHUTE échelle 1 (MOVE) ;
  dettes : forme carte (w/h DETTES_W x DETTES_H, enfants remis) posée en DISQUE2 à f - 1, kit.pop puis kit.move vers
  DETTES_C ; kit.pop("moins", f + 3) en MOINS_C ; egal posé en EGAL_CHUTE puis kit.pop(f + 6). « patrimoine, » (2462) :
  kit.pulse("net", f, step=3, peak=1.1). « n’est » (2488) : kit.move("solde", f, SOLDE_OUT, scale=SOLDE_OUT_K) (MOVE,
  inOut) : la pilule sort de sa case vers « Toi ». « pas » (2495) : regard : pa REGARD_EYE_S20, pb REGARD_SOLDE_S20,
  color INK, draw 0 / from 0 à f - 1, kit.draw("regard", f, 8). « solde. » (2507) : S.key("regard", "color", f, RED,
  3) (hex) ; kit.shake("regard", f + 3, amp=4) (piste pos du fil : sinon secouer pb).
- S21 (2526-2684) « C’est » (2526) : c.toi.unstow ; c.toi.strike(f, *REGARD_BARRE, line="regard_barre",
  track="draw") ; puis le regard rouge se détend et rentre (sag 0 -> 30 en 6 images, puis kit.draw("regard", …, 9,
  track="from")) ; regard_barre s'efface (FADE). « possèdes » (2546) : kit.move("solde", f, SOLDE_CELL_SMALL,
  scale=round(SOLDE_CELL_K * GRILLE_SMALL_K, 4)) (retour dans sa case) ; kit.type("leg_possedes", f, rate=3) puis
  under. « moins » (2565) : kit.type("leg_dois", f, rate=3) + under ; kit.pulse("moins", f, step=3, peak=1.1).
  « dois. » (2592) : kit.draw("regard_net", f, 9) (plein deep, tête -> bas droit de la pilule) ; kit.move("net", f,
  NET_CHUTE, d=10, scale=NET_CHUTE_K, e="out"). « Simple, » (2613) : alerte : pop from_pt net vers ALERTE_CHUTE échelle
  ALERTE_CHUTE_K ; kit.type("leg_limites", f + 4, rate=3) + under. « pourtant » (2638) : S.key("marqueur", "done2", f,
  1, DRAW) ; c.toi.lower(f) ; tenue jusqu'à 2684.
- S22 (2685-2767) « Abonne-toi » (2685) : c.toi.exit(f) ; out = kit.outro("S22", outs=[tout ce qui est à l'écran sauf
  solde et toi : grille, jeton, dettes, net, moins, egal, leg_*, regard_net, alerte, marqueur, nom_toi s'il ne suit pas
  toi], press="argent.", btn_at=MOVE, clear=None ou "fade") ; la pilule `solde` vole jusqu'au bouton (S.fly vers
  FIN_BUTTON, échelle et piste w jusqu'à la taille du bouton, 380 x 112), textOp 1 -> 0 (3 images), text ->
  T_ABONNER, textOp -> 1 : elle devient le bouton (relais btn_at, comme V12) ; S.set(out["cursor"], opacity=0) (pas
  de flèche de souris). « comprendre » (2710) : kit.pop("fin_doigt", f, to=FIN_TAP) (bas droit du bouton, hors du
  libellé). « argent. » (2732) : toucher : fin_doigt scale 0.8 (2 images) ; ring fin_onde1-2 décalés de 3 images ;
  puis plus rien ne bouge.
"""
from pipeline.story import STYLE  # noqa: F401


def part(S, kit, c):
    pass
