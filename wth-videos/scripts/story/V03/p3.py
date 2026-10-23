"""V03, partie 3 : S16-S21, images 2088-2926 (33 temps forts, 27,9 s). La liste des frais pendue à l'étiquette, le
DIC qui la range, l'intermédiaire « obligatoire » et son relevé en € et en %, la vague du marché qui bouge seule
pendant que « Toi » prend la ficelle de l'étiquette, le panneau « Rendement affiché » barré, la carte de fin.

État d'entrée, épinglé à l'image 2087 : kit.pin(2087, ENTRY_P3) (etat_initial de S16 : colonne en EPARGNE_C à
0,60, étiquette en ETIQ_LOW avec sa ficelle, pile « gestion » très haute et jeton « entrée 3 % » dans le bac,
disque 2 actif, « Frais : »). « Toi » en P_TOI, stylo au repos (jamais épinglé) ; `intermediaire` à l'échelle 0.

Temps forts (image du film, round(t x 30) ; ACOUSTIC_SNAP peut décaler d'une image) :
S16  Et@2088  produit,@2105  s’allonger :@2138  arbitrage,@2168  sortie,@2205  transaction,@2231  change,@2259
     droits@2278
S17  Alors,@2314  retrouver ?@2340  Demande@2369  clés@2419  détail@2440
S18  intermédiaire@2482  doit@2502  communiquer@2513  euros@2575  pourcentage.@2597
S19  Tu@2628  ne@2633  pas@2649  marchés.@2657  contrôles@2687  frais.@2705
S20  Et@2726  rendement@2736  affiché@2750  sans@2769  frais@2781  n’est@2794
S21  Abonne-toi@2835  comprendre@2868  argent.@2889      (dernière image du film : 2926)

Brief, scène par scène (ids de la distribution, places = constantes du paquet) :
- S16. « Et » : kit.step(f, 2). « produit, » (morph 11) : l'étiquette monte en ETIQ_LISTE (sa `ficelle` se retire) ;
  `pile` + `etiquette_gestion` -> `liste1` « gestion » (relais) ; `jeton_entree` + `jeton_entree_txt` +
  `etiquette_entree` -> `liste2` « entrée » ; `bac` s'efface ; `epargne` glisse en EPARGNE_S16 (MOVE).
  « s’allonger : » : `liste_fil` se trace (12 images, out), vide. « arbitrage, », « sortie, », « transaction, »,
  « change, », « droits » : `liste3`…`liste7` (papier : nouvelles) tombent une à une sur la ficelle (kit.drop).
  Tenue.
- S17. « Alors, » : `epargne` va en EPARGNE_MINI à l'échelle EPARGNE_MINI_K (MOVE). « retrouver ? » : `question`
  naît sous la pointe du stylo (pop from_pt) et vole en QUESTION_LIVRE. « Demande » : `livre` tombe en LIVRE_C
  (kit.drop), `question` remonte en QUESTION_COIN. « clés » : `livre_dic` pop ; `livre_legende1/2` en fondu.
  « détail » : kit.morph([liste1..7], [livre_ligne1..7]) décalé de 2 images (relais apparié : chaque étiquette se
  réduit dans un trait des pages) ; `liste_fil` se retire ; à f + 14, `question` se réduit dans le livre. Tenue :
  l'étiquette du fil reste seule en ETIQ_LISTE.
- S18. « intermédiaire » : `livre_legende1/2` s'effacent (FADE) ; c.interm.enter(f, at=P_INTERM, frm=INTERM_FROM)
  (il arrive en marchant), puis piste `look` -> 1 (il fait face à « Toi ») ; `interm_nom` pop. « doit » :
  `interm_oblig` pop. « communiquer » : `releve` naît du livre (RELEVE_FROM), passe par RELEVE_VIA et glisse en
  RELEVE_C (S.path ou deux MOVE, arc) ; `releve_titre` se souligne (piste under). « euros » : `releve_cle1` puis
  `releve_val1` s'écrivent (kit.type rate 2). « pourcentage. » : ligne 2. Tenue : l'intermédiaire reste ≥ 4 s.
- S19. « Tu » : c.interm.exit(f) (ou walk vers INTERM_FROM) avec `interm_nom`, `interm_oblig` (vanish) ; `livre`
  et `releve` se réduisent (kit.vanish) ; l'étiquette descend en ETIQ_TOI (MOVE). « ne » (5 images après !) :
  `vague` (échelle 1) tombe en VAGUE_S19 avec `vague_marche`. « pas » : elle monte de 70 px (8 images, out) ;
  « marchés. » : elle descend de 140 px (12 images). « Toi » NE BOUGE PAS (stylo baissé) avant le toucher.
  « contrôles » : c.toi.tap au contact sur le mot, sur ETIQ_TAP. « frais. » : `ficelle_toi` se trace (draw 9) de la
  pointe du stylo à l'étiquette ; c.toi.reach vers un point 30 px plus près de lui pendant que l'étiquette va en
  ETIQ_TIRE (même durée) : il la tient, la vague non. Tenue.
- S20. « Et » : kit.morph(["vague"], ["panneau"]) (`vague_marche` se réduit avec elle). « rendement » :
  c.toi.walk(f, P_TOI_S20) ; l'étiquette suit au bout de la ficelle. « affiché » : `panneau_taux` pop. « sans » :
  `ficelle_toi` se retire (from 0 -> 1) ; l'étiquette glisse en ETIQ_BUTE, le panneau tremble (kit.shake). « frais » :
  c.toi.strike(f, a, b, line="panneau_barre", track="draw"), a et b = extrémités monde de `panneau_barre`
  (S.to_world("panneau", …)) : la rature, de droite à gauche. « n’est » : `panneau_net` pop, `panneau_ton` pop.
  Tenue jusqu'à « Abonne-toi » (1,4 s).
- S21. « Abonne-toi » : kit.outro("S21", mot="Abonne-toi", outs=[panneau, panneau_ton, epargne, marqueur,
  frais_label, …], press="argent.", clear="fade", btn_at=…) ; l'étiquette (z > 40) perd son texte (T_ETIQ ->
  « S’abonner », piste text, après un fondu de 3 images) et va en FIN_BUTTON à l'échelle ETIQ_BTN_SCALE (relais du
  bouton : opacité 0 quand le bouton de la carte est entier dessous) ; c.toi.exit(f). « comprendre » : rien de neuf
  (le toucher approche). « argent. » : toucher au doigt `fin_doigt` + `fin_onde1/2` (ring) sur FIN_TAP, le pointeur
  de l'outro reste invisible (S.set(out["cursor"], opacity=0)), comme V02 p3. Puis plus rien ne bouge jusqu'à 2926.
"""
from pipeline.story import DRAW, DROP, FADE, MORPH, MOVE, POP  # noqa: F401
from pipeline.story_kit import TAP  # noqa: F401

from . import (ENTRY_P3, EPARGNE_MINI, EPARGNE_MINI_K, EPARGNE_S16, ETIQ_BTN_SCALE, ETIQ_BUTE, ETIQ_LISTE,  # noqa: F401
               ETIQ_TAP, ETIQ_TIRE, ETIQ_TOI, FIN_BUTTON, FIN_TAP, INTERM_FROM, LIVRE_C, P_INTERM, P_TOI_S20,
               QUESTION_COIN, QUESTION_LIVRE, RELEVE_C, RELEVE_FROM, RELEVE_VIA, VAGUE_S19, ring, scene_f0)

F_START, F_END = 2088, 2926


def part(S, kit, c):
    pass
