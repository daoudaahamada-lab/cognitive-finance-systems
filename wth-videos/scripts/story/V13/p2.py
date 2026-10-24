"""V13, partie 2 : S09-S15, images 987-1915 (36 temps forts, 31,0 s). Fin du point 1 (immobilier, véhicule, parts de
société ; l'étiquette « Prix d’achat » barrée devient « Valeur actuelle ») ; point 2 « Dois » : la barre de
l'appartement recouverte par la part grise « Ce que tu dois », capital restant dû (pas la mensualité), 250 000 € /
180 000 €, « 250 000 € » rouge barré, part grise retirée, ≈ 70 000 € nets.

ÉTAT D'ENTRÉE : ENTRY_P2 épinglé à 986 (`kit.pin(f0 - 1, ENTRY_P2)`, f0 = scene_f0(S, "S09") = 987) : etat_initial de
S09 = résultat de S08 (grille pleine GRILLE_FULL ; case « Comptes » + pilule (SOLDE_CELL_FULL, ×0,62) ; Livrets,
Assurance-vie, PEA, Épargne salariale, PER nommées ; trois « ? » en bas ; repère étape 1). Garde-fou de partie isolée
(sans effet dans le film entier ; « Toi » est visible dès l'image 0, il est donc déjà là) : ne pas épingler la figurine.
SORTIE : ENTRY_P3 à l'image 1915. Tout ce que cette partie commence finit avant 1916 ; en particulier le calcul de
« nets. » (1896) s'écrit à rate 2 au moins (32 caractères -> 16 images). Fins exigées par le contrat : etiq_achat en
opacité 0 (tombé), ficelle en draw 0 (relayée par ficelle_jeton en S11), brut / mensualite / mensualite_mot en
opacité 0, accolade et restant à l'échelle 0 (vanish), dettes à l'échelle 0 (rentrée dans le disque 2), regard
draw 0 / from 0, « Toi » en P1 stylo baissé.

CODE PARTAGÉ (cette partie seulement) : ajouter le pictogramme `car` (voiture de profil dans la boîte 24 x 24 : caisse
basse à capot et coffre, toit à deux vitres, deux roues pleines ; traits arrondis, `color`, `sw` comme les autres) dans
motion/src/story/draw.tsx (IconName, ICON_NAMES, switch de Icon), le documenter dans
.claude/skills/wth-story-build/references/entities.md (§ pictogrammes), puis `make story-check`. Opt-in : aucun dessin
existant ne change. Vérifier sur une image fixe de S09 (case « Véhicule »).

Ids : grille, q_immo / q_vehicule / q_societe (+ _mot), case_immo, case_vehicule, case_societe (+ _ico, _mot ;
case_societe_pct ; case_immo_place), compte, solde, marqueur, toi (c.toi), nom_toi, jeton (c.tok : meta du PNG ;
c.jeton_bottom), etiquette (+ etiq_oeillet, etiq_achat, etiq_achat_barre, etiq_valeur, etiq_montant), ficelle,
ficelle_jeton, barre, dettes (+ dettes_ico, dettes_mot, dettes_val), mensualite, mensualite_mot (+ mensualite_barre),
accolade, restant, brut (+ brut_barre), resultat, calc_a, calc_b.

BRIEF, scène par scène (images = round(t × 30), avant calage acoustique) :
- S09 (987-1096) « l’immobilier, » (998) : kit.morph(q_immo, case_immo, f) ; drop_in(kit, "jeton", f + 11) en
  JETON_CELL (×1, 120 px) ; kit.type("case_immo_mot", f + 4, rate=3). « véhicule, » (1033) : morph q_vehicule ->
  case_vehicule (pictogramme car) + type. « parts » (1060) : morph q_societe -> case_societe (bâtiment + petit disque %)
  + type. « société. » (1070) : c.toi.walk(f, TOI_P3[0]) ; nom_toi -> NOM_RIGHT (même durée). Plus aucun « ? ».
- S10 (1097-1185) « note » (1103) : drop_in(kit, "etiquette", f) en ETIQ_S10 ; kit.draw("ficelle", f + DROP - 2, 6)
  (du bas de la case « Immobilier » à l'œillet) ; « Prix d’achat » rouge visible dès la chute. « valeur » (1114) :
  c.toi.strike(f, *ACHAT_STRIKE, line="etiq_achat_barre", track="draw") (depuis P3 : assert_reach l'a vérifié).
  « actuelle, » (1123) : kit.drop("etiq_achat", f, out=True, h=110, rot=-8) (le texte barré tombe et s'efface) ;
  kit.type("etiq_valeur", f + 2, rate=3). « pas » (1145) : kit.pulse("etiquette", f, step=3, peak=1.06) ;
  c.toi.lower(f).
- S11 (1186-1315) « Ça » (1186) : move_with_grid(kit, f, small=True) ; case_immo_place pop (le cercle en tirets à la
  place du jeton) ; jeton -> JETON_P2 échelle JETON_P2_K (kit.move, arc 80) ; etiquette -> ETIQ_P2 (même clé) ;
  ficelle draw -> 0 (4 images) et ficelle_jeton draw 0 -> 1 à l'arrivée ; c.toi.walk(f, TOI_P1[0], low=True) ; nom_toi
  -> NOM_ABOVE. « posséder » (1220) : barre : S.key w 0 -> à f - 1 ; kit.pop("barre", f, from_pt=jeton bas
  (735, 600), to=BARRE_C, d=9) puis S.key("barre", "w", …) STRETCH 6 jusqu'à BARRE_W (entièrement cyan). « bien »
  (1239) : kit.pulse("jeton", f, step=3, peak=1.08). « toi » (1282) : c.toi.lean_to(f, 6, d=14). « entier. » (1293) :
  la carte grise ressort du disque 2 : dettes posée en DISQUE2 (pos, w DETTES_W, h DETTES_H, d=0 à f - 1), kit.pop
  puis kit.move vers GRISE_C avec w GRISE_W et h GRISE_H (MOVE) ; dettes_ico -> GRISE_ICO (s 40 : échelle 40/44),
  dettes_mot : text -> T_DOIS_BARRE et pos -> centre (ancre start : x = GRISE_MOT[0] - largeur / 2) ; elle recouvre
  72 % de la barre ; c.toi.lean_to(f + 6, 0).
- S12 (1316-1423) « Ensuite, » (1316) : kit.step(f, 1) ; S.key("marqueur", "done0", f, 1, DRAW). « retire » (1338) :
  hit = c.toi.tap(f, GRISE_TAP) ; kit.shake("dettes", hit, amp=6) ; kit.move("dettes", hit + 3, GRISE_GAP_C, d=9,
  e="out") (liseré ivoire de 12 px). « capital » (1353) : dettes_mot fade 3 images, text -> T_CRD, pos -> GRISE_MOT2,
  kit.type (rate 3). « crédits. » (1402) : kit.pulse("dettes_ico", f, times=2, step=3, peak=1.2) ; c.toi.lower(f).
- S13 (1424-1528) « Pas » (1424) : c.toi.walk(f, TOI_P2[0], low=True) (590 : écart) ; nom_toi -> NOM_RIGHT.
  « mensualités, » (1434) : kit.draw("mensualite", f, 8) (contour rouge sur le bord gauche de la part grise, qui ne
  bouge pas) ; kit.type("mensualite_mot", f + 2, rate=3). « mais » (1461) : c.toi.strike(f, *MENS_STRIKE,
  line="mensualite_barre", track="draw"). « montant » (1474) : kit.fade("mensualite", f, 0) et
  kit.fade("mensualite_mot", f, 0) (FADE, sur place : rien ne tombe) ; kit.draw("accolade", f, 9). « restant »
  (1486) : kit.type("restant", f, rate=3). « rembourser. » (1500) : S.key("dettes", "stroke", f, DEEP, 6) (hex) ;
  kit.pulse("dettes", f, step=3, peak=1.04) ; c.toi.lower(f).
- S14 (1529-1732) « Imagine » (1529) : kit.vanish("accolade", f) et kit.vanish("restant", f) ; c.toi.walk(f,
  TOI_P1[0], low=True) ; nom_toi -> NOM_ABOVE. « appartement » (1546) : kit.pulse("jeton", f, step=3, peak=1.1).
  « estimé » (1567) : kit.pulse("etiquette", f, step=3, peak=1.06). « 250 000 €, » (1582) : kit.pop("etiq_montant", f,
  d=4) ; S.key("etiq_montant", "value", f, V_250, 18, "linear"). « 180 000 € » (1645) : kit.pop("dettes_val", f, d=4) ;
  S.key("dettes_val", "value", f, V_180, 18, "linear"). « crédit » (1698) : kit.pulse("dettes_ico", f, step=3,
  peak=1.2). (Le mot « 250 000 € » revient en S15 : S.beat prend celui de la scène, aucun conflit.)
- S15 (1733-1915) « représente » (1742) : brut posé en BRUT_FROM échelle 0.5 à f - 1, kit.pop("brut", f) puis
  kit.move("brut", f, BRUT_C, d=MOVE, arc=60, scale=1) (copie rouge de la valeur entière, sous la part grise).
  « 250 000 € » (1769) : kit.shake("brut", f, amp=6) ; kit.pulse("dettes", f, step=3, peak=1.04). « patrimoine, »
  (1818) : c.toi.unstow / reach puis c.toi.strike(f, *BRUT_STRIKE, line="brut_barre", track="draw") depuis P1.
  « mais » (1842) : kit.drop("brut", f, out=True, h=120, rot=10) ; hit = c.toi.tap(f, GRISE_TAP) (préparer le tap
  pour que le contact tombe sur f + 4 au plus tard). « environ » (1847) : la pointe tire la part grise : kit.move
  ("dettes", f, …, arc vers la droite) puis kit.vanish("dettes", …, into=DISQUE2) ; la barre cyan reste seule
  (S.key barre w -> BARRE_SHORT_W et pos -> BARRE_SHORT_C, même clé : elle ne garde que sa part cyan x 140-319) ;
  c.toi.lower. « 70 000 € » (1863) : kit.pop("resultat", f, from_pt=BARRE_SHORT_C, to=RESULTAT_C). « nets. » (1896) :
  kit.type("calc_a", f, rate=2.5) puis kit.type("calc_b", fin, rate=2.5) (fini avant 1916).

PASSAGE À p3 : grille réduite complète (case « Immobilier » : libellé + cercle en tirets), jeton à droite (×JETON_P2_K)
avec l'étiquette « Valeur actuelle · 250 000 € », courte barre cyan, « ≈ 70 000 € nets » et le calcul ; part grise
dans le disque 2 ; repère étape 2 (done0) ; « Toi » en P1 stylo baissé (ENTRY_P3).
"""
from pipeline.story import STYLE  # noqa: F401


def part(S, kit, c):
    pass
