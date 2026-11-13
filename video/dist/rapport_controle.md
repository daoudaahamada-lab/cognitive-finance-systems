# Rapport de contrôle : « On audite un cabinet de gestion de patrimoine »

Version locale à relire, non publiée. Contrôles exécutés sur le MP4 final (`tools/qc.py`, ffprobe, ffmpeg, Whisper local).

## Fichiers

Tous sous `/home/user/cognitive-finance-systems/video/` :

| Livrable | Chemin |
|---|---|
| Vidéo finale | `dist/agentic-wealth_audit-cgp_fr.mp4` (56,5 Mo) |
| Sous-titres SRT | `dist/agentic-wealth_audit-cgp.fr.srt` |
| Texte définitif de la voix off | `dist/voix_off_texte_definitif.txt` |
| Conducteur scène par scène | `dist/conducteur.md` |
| Captures de contrôle (19) | `dist/frames/` |
| Projet source | `script/`, `tools/`, `web/`, `build.sh`, `README.md` |

## Mesures techniques (ffprobe / ffmpeg sur le MP4 final)

| Critère | Résultat |
|---|---|
| Durée réelle | **1 008,2 s = 16 min 48 s** (minimum demandé : 10 min 30 s) |
| Vidéo | H.264, **1920 × 1080**, 25 i/s |
| Audio | **piste présente** : AAC, 48 kHz, stéréo, 192 kb/s |
| Loudness intégrée | -16,0 LUFS |
| Silences > 2,5 s (sous -45 dB) | aucun |
| Plus longue pause entre deux phrases | 1,79 s (fin de l'accroche, transition volontaire) |
| Mots prononcés | **2 595** (≈ 154 mots/min, pauses comprises) |
| Sous-titres | 323 blocs, 2 lignes maximum, 42 caractères maximum par ligne, incrustés dans l'image et fournis en SRT |
| Tirets cadratin / demi-cadratin | 0 dans la voix, 0 dans le SRT, 0 dans les textes à l'écran |

**Synchronisation.** Les sous-titres et les animations sont calculés à partir des horodatages réels de chaque phrase
synthétisée, donc synchrones par construction. Contrôle indépendant : transcription Whisper du MP4 final, décalage
médian de 0,14 s entre les segments reconnus et la timeline (127 segments appariés). L'imprécision vient surtout de
l'horodatage de Whisper.

**Intelligibilité.** Whisper retrouve 86,6 % des mots du script à l'identique. La plupart des écarts sont des
normalisations (« vingt-quatre » transcrit « 24 ») ou des accords de pluriel inaudibles en français. Pour les phrases
à mots difficiles, plusieurs prises sont synthétisées et la mieux reconnue est conservée (journal :
`build/tts_bestof.log`).

## Calculs vérifiés

- 8 + 9 + 7 = **24** h (avant)
- 4 + 6 + 4 = **14** h (après visé)
- gains cibles 4 + 3 + 3 = **10** h
- 10 × 46 = **460** h de capacité potentielle
- 460 × 60 € = **27 600** € de capacité théorique (illustration)
- note : 13 + 6 + 7 + 9 + 10 = **45** / 100

Les chiffres sont identiques dans la voix, à l'écran et dans les sous-titres.

## Captures inspectées (extraites du MP4)

Toutes lisibles, sans débordement ni texte coupé :

- accroche (00:24)
- titre (01:09)
- cabinet (02:28)
- audit et note (04:11)
- 5 domaines (04:51)
- agent 1 : sources (05:43), brief (06:48), compte rendu (07:35), tâches (07:53)
- agent 2 : tableau (09:12), décision humaine (09:35)
- agent 3 : brouillon (11:32), cockpit (12:25)
- données (13:05)
- bilan (14:42 et 15:10)
- planning (16:09)
- appel à l'action (16:37)
- carton final (16:47)

## Relecture indépendante du fond

Un relecteur séparé a relu le script et tous les textes à l'écran. Il a relevé un point bloquant, désormais corrigé :
la première phrase présentait les 24 h comme un fait. Elle devient « Prenons un cabinet de gestion de patrimoine
fictif », avec la mention « simulation » à côté du 24 h. Également corrigé :

- « capacité potentielle » ;
- « heures visées » ;
- « notre hypothèse » pour le bloc 3 ;
- « revue arbitrée » au lieu de « revue validée » ;
- incohérences entre écrans : client et prospect, horloge 15:31, foyer du cockpit.

Après correction, les critères sont respectés :

- aucune conformité garantie ;
- aucun résultat client présenté comme réel ;
- aucun envoi par l'agent seul : l'agent n'a que « Préparer », et Sophie ou Karim « Vérifier et envoyer » ;
- aucun conseil patrimonial automatisé ;
- capacité théorique, économies et chiffre d'affaires distingués explicitement.

## Écarts par rapport à la demande

- **Durée : 16 min 48 s**, soit 48 s au-dessus de la cible indicative de 13 à 16 min. Le minimum de 10 min 30 s est
  largement dépassé. Le texte a déjà été resserré de 3 034 à 2 595 mots. Raccourcir encore aurait obligé à retirer des
  éléments demandés.
- **Formulation réglementaire modifiée** par rapport au script d'origine. « Déclaration d'adéquation remise après le
  conseil » devient « remise au client avant la réalisation de l'opération conseillée », sur l'avis du relecteur. À
  confirmer par un juriste.
- **Voix de synthèse** : Piper, voix française « siwis », exécutée localement et gratuitement. Elle est intelligible
  mais reste reconnaissable comme une voix de synthèse : ce n'est pas une voix humaine.
- **Musique** : nappe discrète générée par calcul (`tools/mix_audio.py`), aucune banque sonore.
- **Identité visuelle** : aucun logo ni charte Agentic Wealth n'existait dans le projet. J'ai utilisé un simple
  wordmark texte, sans inventer de logo. Les tableaux Miro n'étaient pas accessibles ici : les cinq domaines suivent le
  script.

## Points à valider par une personne avant publication

1. **Mentions réglementaires** : repère AMF (informations à recueillir, déclaration d'adéquation et moment de sa
   remise), vigilance « pour les professionnels assujettis » et « approche fondée sur les risques », points d'attention
   « rappelés par la CNIL ». Ce sont des formulations générales, sans source citée à l'écran.
2. **Écoute intégrale de la voix**, en particulier sur ces mots :
   - « Léa », que Whisper confond parfois avec « l'IA » ;
   - « Aix-en-Provence » ;
   - « chatbot » ;
   - « onze étapes » ;
   - « Agentic Wealth », prononcé à la française.
3. **Chiffres affichés** : vérifier que les mentions « simulation », « hypothèse », « gain cible », « capacité
   théorique » et « valorisation interne illustrative » vous conviennent. La valeur de 60 € de l'heure est
   illustrative.
4. **Données fictives** :
   - initiales (Camille R., Mme D., M. B., foyers G., H., P., T.) ;
   - adresse « 12, rue fictive » ;
   - document de démonstration flouté ;
   - nom « Horizon Patrimoine ». Vérifier qu'aucun cabinet réel ne porte ce nom dans votre zone.
5. **Planning de mission et appel à l'action** (« Montrez-nous un dossier et une semaine réelle ») : vérifier qu'ils
   correspondent à votre offre réelle.
6. **Licence de la voix** : CC BY 4.0 (corpus SIWIS). L'attribution figure sur le carton final ; vérifier qu'elle suffit
   pour votre canal de diffusion.
7. **Sous-titres incrustés** : ils sont gravés dans l'image. Si la plateforme affiche aussi le SRT, désactiver l'un des
   deux.
