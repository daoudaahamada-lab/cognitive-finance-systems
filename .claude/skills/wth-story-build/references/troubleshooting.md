# Dépannage : erreurs connues et remèdes

Messages tels qu'ils s'affichent (`pipeline/story.py`, `story_kit.py`, `story_review.py`, `qa.py`, Makefile), avec
leur cause et le remède. Lis la section de l'étape qui a échoué. Commandes lancées depuis `wth-videos/`.

## Sommaire

1. Entrées : voix, storyboard, illustrations
2. Construction des props : temps forts, scènes, pistes
3. Kit et figurine
4. Sous-titres
5. Images fixes et rendu
6. Revue
7. QA
8. Disque, verrou et machine
9. Rendu qui semble faux sans erreur

## 1. Entrées : voix, storyboard, illustrations

| Message | Cause | Remède |
|---|---|---|
| `build/Vxx/tts.json absent (make tts ID=…)` ou `words.json absent` | voix pas importée ou pas préparée | `make voice ID=Vxx` (aucun appel réseau si la voix est en cache). Sans voix en cache : skill `wth-video`, recette de la voix. |
| `Storyboard absent : scripts/storyboards/Vxx.json` | storyboard pas écrit | skill `wth-storyboard` |
| `storyboard REFUSÉ` (`make storyboard-check`) | champs, scènes non contiguës, début de scène hors début de mot, temps fort introuvable, texte ≠ script, `idees_cles` absentes | Corrige le storyboard (skill `wth-storyboard`). Le texte des scènes doit être celui de `scripts.json` (NFC). |
| `Mise en scène absente : scripts/story/Vxx.py` | pas de mise en scène | crée le paquet `scripts/story/Vxx/` (SKILL.md, étape 1) |
| `Deux mises en scène pour Vxx` | `Vxx.py` et `Vxx/` coexistent | garde le paquet : `git mv scripts/story/Vxx.py scripts/story/Vxx/<partie>.py`, puis adapte |
| `Illustration absente : …/assets/illustrations/X.png` | illustrations non versionnées (gitignore) | Télécharge-les depuis le Drive (identifiants dans `data/illustrations_manifest.tsv`) : skill `wth-video`, `references/environment.md`. |
| `(carrousel WTH-00x) : illustration … d'un autre carrousel de la série` | règle de la série | Seulement le carrousel de la vidéo (`source` dans `scripts.json`) et les 20 génériques. Dessine l'objet en entités sinon. |

## 2. Construction des props : temps forts, scènes, pistes

| Message | Cause | Remède |
|---|---|---|
| `Sxx « mot » (t s) : mot introuvable à ce temps dans words.json` | le `t` du storyboard est à plus de 30 ms du début du mot, le mot diffère (casse, orthographe), ou la voix a changé après le storyboard | `make storyboard-check ID=Vxx` montre l'écart. Corrige `t` et `mot` d'après `build/Vxx/words.json`. Casse exacte ; ponctuation libre ; nombres comme « 4 600 € ». |
| `Sxx : pas de temps fort sur « mot » dans le storyboard` | `kit.at` sur un mot qui n'est pas un temps fort de cette scène | Prends le mot du storyboard, ou `S.word_after(mot, f)` pour un geste secondaire. |
| `Scène Sxx absente du storyboard` | id de scène faux | Ids exacts du storyboard (`S01`…). |
| `Mot « x » absent de words.json` (`S.word`, `word_after`) | mot mal écrit ou absent après l'image donnée | Vérifie dans `words.json` (casse, apostrophe ’ ou '). |
| `film entier refusé, mise en scène incomplète` | scènes sans aucun temps fort, temps forts sans événement, ou rien de mis en scène au début | Chaque temps fort du storyboard doit être posé (`kit.at`, ou `kit.hold` pour une tenue). `ALLOW_PARTIAL=1` seulement pour un rendu de travail. |
| Second temps fort sur le même mot dans une scène, jamais déclenché | `S.beat` ne trouve que le premier temps fort de ce mot dans la scène | `S.word(mot, near=t)` pour le second ; mieux : le storyboard le déplace sur un mot voisin. |
| `id.piste : valeur initiale manquante (Story.set)` | `S.key` sur une piste sans valeur initiale | `S.set(id, piste=…)` à la déclaration (les macros du kit le font pour leurs pistes). |
| `Entité « x » déjà déclarée` | deux `add` du même id, souvent dans deux parties | Déclare tout dans `cast` (`__init__.py`), une seule fois. |
| `x : parent « p » à déclarer avant` | ordre de déclaration | Déclare le parent d'abord. |
| `id.piste : assouplissement « … » inconnu` | nom d'easing | `linear`, `out`, `in`, `inOut`, `outQuad`, `inOutSine`. |
| `matrice non inversible (entité réduite à un point)` | `to_local` / `parent_space` / `fly` sur un parent à l'échelle 0 à cette image | Calcule à une image où le parent est visible, ou fais voler l'objet avant que le parent ne disparaisse. |
| `attention : temps forts hors début de mot : [...]` | un temps fort a été déplacé à la main | Utilise l'image renvoyée par `kit.at` telle quelle. |
| `ModuleNotFoundError` / `SyntaxError` dans `pN.py` | partie en cours d'écriture | Corrige ; en attendant, isole ta partie : `WTH_PARTS=p2 make story-props ID=Vxx ALLOW_PARTIAL=1`. |
| `KeyError` sur `text_width` | graisse non prise en charge | 600, 700 ou 800 seulement. |

## 3. Kit et figurine

Un avertissement du kit (`attention (kit) : …`) n'arrête rien, mais une mise en scène terminée n'en a aucun : chacun
correspond à un défaut visible.

| Message | Cause | Remède |
|---|---|---|
| `pin N : id.piste vaut X à l'image N−1, imposé Y (saut)` | l'état de fin de la partie précédente ≠ l'état d'entrée de la suivante | En film entier, aligne la fin de la partie précédente sur l'épingle. Avec `WTH_PARTS` (partie isolée), c'est normal. |
| L'épingle ne change rien au premier mouvement | `kit.pin(f)` et un mouvement qui commence sur f : il part de la valeur de f − 1 | Épingle à f − 1. |
| `id image N : prise hors d'atteinte de X px (la figurine doit s'approcher : walk / place_for)` | la cible est trop loin pour un bras à longueur fixe | `fig.walk(f, fig.place_for(cibles, f - 1))` avant le geste. |
| `pas automatique de X px en N images (saccadé)` | le rig a dû faire un pas pendant un geste court | Place la figurine avant (`walk` + `place_for`). |
| `cible … hors d'atteinte (… px) : rapproche la figurine en hauteur` | cible trop haute ou trop basse pour l'épaule | Change le y de la figurine, ou son échelle. |
| `cibles trop écartées pour un seul emplacement` | `place_for` sur des points trop éloignés | Coupe la séquence en deux emplacements, ou rapproche les cibles. |
| `cible à X px de l'épaule, trop près pour le stylo` | figurine collée à la cible | Éloigne la figurine (`walk`). |
| `figurine sans bras ni stylo (tool=False)` | geste demandé au client | Seul « toi » (encre) tient un outil : c'est une règle de la série. |
| Bras qui se détache ou s'étire | clé manuelle, `kit.move` ou `kit.pin` sur la figurine, son bras ou son stylo | Seulement les méthodes de `Figure`. |
| `Fiche id : N rangées pour M places (Sheet(n=…))` | `Sheet(n)` trop petit | `Sheet(n=len(lines))`. |
| `outro : scène Sxx absente du storyboard` | id de la dernière scène | Utilise l'id réel. |

## 4. Sous-titres

| Message | Cause | Remède |
|---|---|---|
| `Découpe imposée de plus de 4 mots : « … »` | groupe de `CAPTION_GROUPS` trop long | 4 mots au plus ; 2-3 de préférence. |
| `Découpe de sous-titres imposée introuvable dans le texte : [...]` | les mots ne se suivent pas ainsi dans `words.json` (casse, apostrophe, ponctuation) | Recopie les mots tels qu'ils sont dans `words.json` (sans ponctuation). |
| QA « Aucun mot coupé » : `groupe trop large : N px` | groupe > 760 px en Inter Bold 64 | Coupe-le avec `CAPTION_GROUPS`. |
| Un mot d'alerte n'est pas rouge | absent de `ALERT_WORDS`, ou écrit autrement | Écris-le sans ponctuation, comme dans `words.json`. |

## 5. Images fixes et rendu

| Message | Cause | Remède |
|---|---|---|
| `FROM et TO vont ensemble` | un seul des deux donné à `make story` | Les deux pour un extrait, aucun pour le film entier. |
| `Précise les images : make story-stills ID=… FRAMES="0 120 480"` | `FRAMES` manquant | Numéros d'image du film. |
| `motion/node_modules absent : lance « npm ci » dans motion/.` | dépendances Remotion absentes | `make motion-setup` |
| `Rendering browser not found: …` | navigateur de `motion/browser.json` absent | Vérifie le chemin (`/opt/pw-browsers/…`) ou mets `REMOTION_BROWSER_EXECUTABLE`. |
| `Story: no component for entity type "x"` (au rendu ou aux images fixes) | type déclaré en Python mais pas enregistré en TSX | Ajoute le composant à `KIT` (`entities_kit.tsx`), puis `make story-check`. |
| `Rendu Remotion en échec (N)` ou `Images fixes en échec` | erreur affichée juste au-dessus (4 000 derniers caractères) : disque plein, `delayRender` dépassé (PNG manquant ou énorme), erreur TSX, mémoire | Lis l'erreur. Vérifie `df -h .`, puis `make clean-tmp` et `make story-check`. Relance une fois ; si ça échoue encore, ne boucle pas : rapporte l'erreur. |
| `… : en attente de build/.render.lock (tenu par pid …)` | un autre rendu tourne (un seul à la fois) | Attends. Le texte du fichier peut nommer un ancien pid : c'est sans effet, seul le verrou système compte. Ne supprime jamais ce fichier. |
| `make story` sort en code 1 alors que le MP4 existe | la QA lancée après le rendu a échoué | Lis le tableau de QA (section 7). Le film est bien rendu. |
| `output/WTH-Vxx.mp4 (rendu motion) rangé dans build/Vxx/archive/` | premier film Story de la vidéo | Information : l'ancien film est archivé, pas perdu. |
| `make video` ou `make motion` refuse d'écraser le film | garde-fou : un film Story n'est jamais écrasé par un autre rendu | Voulu. `FORCE=1` seulement sur demande explicite. |
| `Fenêtre vide : a -> b s` | extrait hors de la voix | Corrige `FROM` / `TO` (débuts de mots). |

## 6. Revue

| Message | Cause | Remède |
|---|---|---|
| `build/Vxx/story_render.json absent : rendre d'abord le film (make story ID=…), ou --src <mp4>` | pas de film entier complet | Rends le film, ou relis un rendu de travail : `REVIEW="--src build/Vxx/story/film_partiel.mp4"`. |
| `… : props introuvables (balises wth_props / wth_scenes) : préciser --props` | MP4 d'un autre outil, ou props reconstruites depuis | `REVIEW="--src <mp4> --props build/Vxx/story/props_….json"` |
| Planches d'une ancienne version | sheets pas refaites après un rendu | `make story` refait les planches du film avec sous-titres ; refais celles sans sous-titres (`REVIEW="--nocap --sheets --phone"`). |
| Une image fixe montre la partie d'un autre auteur | deux auteurs partagent `props_film_partiel.json` | Relance l'appel. |

## 7. QA

Chaque contrôle et son remède : `qa-checklist.md`. Les échecs les plus fréquents :
- **« Rendu Story à jour » : empreintes DIFFÉRENTES.** Une source a changé après le rendu (storyboard, partie,
  `make story-props` d'une autre version). Relance `make story`.
- **« Mise en scène complète » : `rendu de travail (--allow-partial)`.** Le film livré doit venir de `make story`
  sans `ALLOW_PARTIAL`.
- **« Jamais d'image figée » : tenue de plus de 3,5 s.** Voir `build/Vxx/review/film/holds.json`. Ajoute un temps
  fort ou un geste discret.
- **« Zones réservées dégagées ».** Une ombre ou une entrée depuis le bord droit (x > 940), le haut (< 160) ou le bas
  (> 1540) suffit à échouer.
- **`story_render.json absent : le film Story n'a pas été rendu par pipeline.story`.** `output/WTH-Vxx.mp4` vient
  d'un autre rendu. Lance `make story`.

## 8. Disque, verrou et machine

- **Disque.** `df -h .` doit montrer au moins 4 Go libres. Sinon, dans cet ordre :
  1. `make clean-tmp` : dossiers temporaires de Remotion, sous le verrou ;
  2. `make clean-tmp ID=<vidéo terminée>` : bandes, images téléphone, images extraites ;
  3. `rm -f build/Vxx/story/stills/*.png build/Vxx/story/muet_*.mp4` : images fixes, rendus muets intermédiaires ;
  4. anciennes archives `build/Vxx/archive/` d'une vidéo livrée.

  Ne supprime jamais `output/*.mp4`, `cache/` ni `assets/`.
- **Dossiers `/tmp/remotion-*`.** Les rendus passés par `make` nettoient les leurs ; `make clean-tmp` supprime ceux
  d'un rendu tué. Il ne touche à rien si un rendu tourne (`pgrep -af "remotion render|stills.mjs"`).
- **Lenteur.** 4 cœurs : un seul rendu Remotion à la fois (4 workers) et 2 agents par workflow. Ordres de grandeur :
  - film entier : environ 4 min pour les deux versions, plus 2 min de QA ;
  - planches de revue : 1 à 2 min ;
  - images fixes : environ 30 s de préparation, puis 1 à 3 s par image.
- **Workflow interrompu.** Relance avec `resumeFromRunId` : les étapes terminées sont reprises du cache.

## 9. Rendu qui semble faux sans erreur

| Symptôme | Cause | Remède |
|---|---|---|
| Halo sombre ou sarcelle autour d'un PNG sur l'ivoire | halo cuit pour fond noir | Passe toujours par `S.png` (alpha strict). Préfère `contact={…}` (ombre sous l'objet) à l'ombre portée autour de la silhouette ; `keep_largest=True` retire une pièce détachée. Si la recette change, incrémente `PNG_VERSION`. |
| PNG trop coloré à côté du cyan | couleurs du verre | `saturate=0.85` sur l'entité `png`. |
| Élément visible dans le coin haut gauche au début | `add` sans `set(pos, scale=0)` | Déclare-le à sa place, `scale=0`. |
| Clignotement juste avant une apparition | élément visible avant un `pop` (qui le remet à 0 à f − 1) | Déclare-le avec `scale=0`. |
| Couleur qui saute au lieu d'un fondu | nom de palette au lieu d'un hex | `S.set(id, fill=STYLE["cyan"])`, puis clé en hex. |
| Un élément passe sous un autre alors que son parent est au-dessus | `z` global, pas relatif au parent | Donne-lui un `z` supérieur, ou une piste `z`. |
| Un `morph` réduit un repère 1-2-3 vers le coin de l'écran | repère déclaré avec des `xs` absolus | `kit.steps_marker` (repère local centré). |
| Mouvement coupé net | deux macros sur la même piste qui se recouvrent : la dernière posée gagne | Enchaîne sur la valeur de retour de la macro précédente. |
| Le fil part d'un espace vide | ancre du fil hors du texte | Ancre-le sur la valeur (`a: {id: rangée, at: point de la valeur}`). |
| Texte illisible sur téléphone | corps < 32 px à l'échelle 1, ou fiche trop réduite | Agrandis ; enlève des éléments plutôt que de réduire. |
| Bas de l'image vide | composition trop haute | Descends l'action jusqu'à y ≈ 1250 (ligne de sol vers 1230). |
| Extrait validé de V01 modifié après une retouche du code partagé | défaut d'un type existant changé | Rends le nouveau comportement optionnel ; rends l'extrait (`make story ID=V01 FROM=25.612 TO=41.309`) et compare-le à `build/V01/baseline/` (PSNR ≥ 45 dB par image). |
