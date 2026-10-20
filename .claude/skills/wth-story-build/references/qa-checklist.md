# QA d'un film Story (`make qa ID=Vxx`)

Ce que `pipeline/qa.py` vérifie sur un film Story, ce qui fait échouer chaque contrôle et comment le corriger. Plus
les vérifications que la machine ne fait pas.

## Lancer

```bash
make qa ID=V07          # environ 2 min ; écrit output/qa/V07.json et réécrit output/qa_report.md
make story ID=V07       # rend le film PUIS lance la même QA (code 1 si elle échoue, le film est pourtant rendu)
```

- **Mode.** Il est lu dans le MP4 : balise `wth_mode=story`, avant le commentaire « Made with Remotion ». Pour le
  forcer : `python3 -m pipeline.qa V07 --mode story`.
- **Entrées.** `output/WTH-V07.mp4`, sa fiche `build/V07/story_render.json` (props, empreintes, version sans
  sous-titres), `build/V07/tts.json` et `words.json`, `scripts/scripts.json`.
- **Seuils.** Ils sont dans `config.yaml`, section `qa`. Ne les change jamais pour faire passer un film : une durée
  maximale propre à une vidéo (`max_duration_by_video`, ex. V03 : 62 s) demande l'accord de l'utilisateur.
- **Publication.** `make upload` refuse une vidéo dont la QA a échoué.

## Les 14 contrôles, dans l'ordre du rapport

| # | Contrôle | Réussi si | Causes d'échec et remèdes |
|---|---|---|---|
| 1 | Durée | 45 à 60 s (ou `qa.max_duration_by_video`) | La voix est trop longue : ce n'est pas un problème de mise en scène. Demande à l'utilisateur (accélérer de 4 % au plus, allonger la limite, raccourcir le texte). |
| 2 | Format | h264 1080 × 1920, 30 i/s, yuv420p, AAC ; couleur BT.709, plage tv | Le MP4 n'a pas été rendu par `make story`. Ne réencode jamais à la main. |
| 3 | Rendu Story à jour | empreintes des props, du storyboard et de la mise en scène (balises du MP4) = fichiers actuels ; nombre d'images = props ; version sans sous-titres présente et inchangée | Un fichier source a changé après le rendu (storyboard, une partie du paquet, props reconstruites). Relance `make story`. Ne modifie rien entre le rendu et la QA. |
| 4 | Mise en scène complète | pas de balise `wth_partial`, film entier, aucune scène ni aucun temps fort sans événement, rien de non mis en scène au début | Rendu de travail (`ALLOW_PARTIAL=1`) ou mise en scène incomplète. Termine les scènes (`make story-props` doit passer sans `ALLOW_PARTIAL`). |
| 5 | Synchro sous-titres | < 150 ms : écart image / début du mot, plus le décalage de la piste audio du MP4 (corrélation avec la voix), et aucun conflit avec les pauses mesurées | Presque jamais la mise en scène. Un décalage audio fort indique une coupe audio fausse : vérifie `build/Vxx/audio.wav` (refait par `make voice`). |
| 6 | Aucun mot coupé | les mots surlignés = les mots du texte ; groupe le plus large ≤ 760 px (Inter Bold 64) ; un sous-titre à chaque image depuis le premier mot ; alignement complet ; fin d'audio silencieuse ; vidéo pas coupée avant la fin du dernier mot | Groupe trop large : `CAPTION_GROUPS` dans le paquet (4 mots au plus). Alignement incomplet ou fin d'audio : voix à refaire (skill `wth-video`). |
| 7 | Accents et caractères | texte NFC, aucun mojibake (texte lu et textes affichés), glyphes présents dans Inter, `words.json` aligné sur le texte du script | Glyphe absent : remplace le caractère (flèche, symbole rare) par un pictogramme `icon`. Les « mots hors dictionnaire » du détail ne font pas échouer : relis-les, une coquille à l'écran est un défaut. |
| 8 | Pas de saturation | true peak ≤ −1 dBTP, aucun échantillon écrêté | Vient de la voix normalisée. Supprime `build/Vxx/audio.wav`, refais `make voice ID=Vxx`, puis `make story`. |
| 9 | Loudness | −14 ± 1 LUFS intégrés | Même remède que le contrôle 8. |
| 10 | Surbrillance à l'image près | sur la ligne de sous-titres décodée, le mot surligné (cyan profond ou rouge) change à l'image exacte du début de chaque mot, jamais avant, et un mot est toujours surligné | Regarde les images citées (« en retard », « en avance », « sans mot »). Causes : un élément de la mise en scène qui entre dans la bande 1280-1380 différemment avec et sans sous-titres ; deux mots sur la même image ; un `ALERT_WORDS` mal écrit. |
| 11 | Zones réservées dégagées | sur la version sans sous-titres, au plus 0,3 % de pixels hors fond dans les 160 px du haut, les 380 px du bas et à droite de x = 940 | Un élément, son ombre ou une entrée depuis le hors-champ passe sous l'interface TikTok ou Reels. Rapproche-le, réduis-le, fais-le naître sur place (`pop`) ou entrer par la gauche (`Figure.enter(frm=…)` évite x > 940). |
| 12 | Jamais d'image figée | aucune tenue de plus de 3,5 s, hors carte de fin (de la dernière scène à la fin) | Une scène sans événement pendant longtemps. Ajoute un temps fort ou un geste discret (`pulse`, reflet, petit glissement), sans casser « tenir puis éclater ». `build/Vxx/review/film/holds.json` donne les tenues. |
| 13 | Version sans sous-titres conforme | même nombre d'images que les props dans les deux versions ; PSNR ≥ 40 dB au-dessus de y = 1270 | Les deux versions ne viennent pas du même `make story`, ou une entité dépend de l'affichage des sous-titres. Refais `make story`. |
| 14 | Bande d'action jamais vide | au moins 1 % de pixels hors fond entre y = 160 et 1270, à chaque image | Scène vidée entre deux compositions. Passe par `kit.morph` : les sortants se réduisent pendant que les entrants grandissent. |

Les contrôles 10 à 14 décodent les deux MP4 à demi-résolution.

## Ce que la QA ne vérifie pas

Ces points sont à vérifier à l'œil, sur les planches, ou par les revues :
- **Critère de l'utilisateur.** Le contrôle sans son (`mute-verify.wf.js`) doit réussir : 85 % des `idees_cles` en
  GOT, aucune idée principale manquée, « oui » au critère.
- **Revues.** Aucun problème bloquant ni majeur ne reste ouvert.
- **Lisibilité.** À taille téléphone (`build/Vxx/review/film/phone/`), sans collision sur la dernière image de chaque
  scène.
- **Couleurs.** Rouge seulement pour l'élément d'alerte ; IA et humain distincts par la forme.
- **Dates.** Écrites en clair.
- **Fin.** La carte standard (`kit.outro`) avec le bouton « S’abonner ».
- **Orthographe à l'écran.** Relis les « mots hors dictionnaire » du contrôle 7.

## Après une QA verte

- Commite `output/qa/Vxx.json`, `output/qa_report.md` et les sources (jamais le MP4 ni `build/`).
- Mets à jour l'état de la vidéo (`qa: done`).
