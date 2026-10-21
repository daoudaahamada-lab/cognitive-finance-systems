# Rapport qualité — vidéos WealthTech Horizon

| Vidéo | Source | Résultat | Durée | Synchro | Loudness | Contrôlée le |
|---|---|---|---|---|---|---|
| V01 | WTH-003 | ✅ OK | 93.23 s | 89 ms | -14.2 LUFS | 2026-10-21T18:00:23+00:00 |
| V02 | WTH-002 | ✅ OK | 89.27 s | 76 ms | -14.2 LUFS | 2026-10-21T17:58:55+00:00 |

## V01 (WTH-003) — OK

| Contrôle | Résultat | Valeur | Attendu | Détail |
|---|---|---|---|---|
| Durée | ✔ | 93.23 s | 45 à 180 s |  |
| Format | ✔ | h264 1080x1920 30/1 yuv420p + aac, profil High, tv/bt709, audio 48000 Hz, 190 kb/s | h264 1080x1920 30/1 yuv420p + aac, BT.709 plage tv |  |
| Rendu Story à jour | ✔ | 2797 images, empreintes identiques | 2797 images (props), empreintes props + storyboard + mise en scène du rendu = fichiers actuels, version sans sous-titres du même rendu | props b363732a09, storyboard 0b19fdde73, mise en scène 52fa221933 |
| Mise en scène complète | ✔ | 22 scènes mises en scène, tous les temps forts posés | chaque scène du storyboard mise en scène, chaque temps fort avec son événement, pas de rendu partiel | mise en scène scripts/story/V01/__init__.py, storyboard scripts/storyboards/V01.json |
| Synchro sous-titres | ✔ | 89 ms | < 150 ms | sous-titres (props Story)/alignement + image : 86 ms ; décalage audio MP4 : 3 ms ; alignement scribe vérifié sur 28 pauses mesurées, aucun conflit |
| Aucun mot coupé | ✔ | ok | tous les mots, entiers, dans la largeur | 239 mots, groupe le plus large 717/760 px (Inter Bold 64 px, film Story) |
| Accents et caractères | ✔ | ok | UTF-8 NFC, glyphes présents, aucun mojibake | mots hors dictionnaire à relire : Brief, Mail, brief, déc, févr, info, mails |
| Pas de saturation | ✔ | true peak -1.6 dBTP, 0 échantillon(s) écrêté(s) | ≤ -1.0 dBTP, 0 écrêtage |  |
| Loudness | ✔ | -14.2 LUFS | -14 ± 1 LUFS |  |
| Surbrillance à l'image près | ✔ | 238/238 changements à l'image exacte | le mot surligné change à l'image du début du mot, pas avant ; toujours un mot surligné à l'écran | mesuré sur la ligne de sous-titres décodée |
| Zones réservées dégagées | ✔ | haut 0.00% (image 0); bas 0.00% (image 0); droite 0.27% (image 996) | ≤ 0.3% de pixels hors fond dans les 160 px du haut, les 380 px du bas et à droite de x = 940 (version sans sous-titres) | interface TikTok / Reels : rien d'important sous les bandeaux ni sous la colonne d'icônes |
| Jamais d'image figée | ✔ | tenue la plus longue 1.6 s (images 171-219) | aucune image figée plus de 3.5 s, hors carte de fin (dès l'image 2718) | 12 tenues ≥ 0,5 s (au moins 12 px à mi-résolution qui changent de plus de 16 niveaux = mouvement) |
| Version sans sous-titres conforme | ✔ | PSNR 46.9 dB au pire (image 2725), 2797 / 2797 images | ≥ 40 dB au-dessus de y = 1270, 2797 images dans les deux versions | médiane 99.0 dB |
| Bande d'action jamais vide | ✔ | 4.9% au pire (image 2730) | ≥ 1% de pixels hors fond entre y = 160 et 1270, à chaque image | médiane 11.7% |

## V02 (WTH-002) — OK

| Contrôle | Résultat | Valeur | Attendu | Détail |
|---|---|---|---|---|
| Durée | ✔ | 89.27 s | 45 à 180 s |  |
| Format | ✔ | h264 1080x1920 30/1 yuv420p + aac, profil High, tv/bt709, audio 48000 Hz, 190 kb/s | h264 1080x1920 30/1 yuv420p + aac, BT.709 plage tv |  |
| Rendu Story à jour | ✔ | 2678 images, empreintes identiques | 2678 images (props), empreintes props + storyboard + mise en scène du rendu = fichiers actuels, version sans sous-titres du même rendu | props 842105fb5b, storyboard c161705e70, mise en scène c0d4c512eb |
| Mise en scène complète | ✔ | 22 scènes mises en scène, tous les temps forts posés | chaque scène du storyboard mise en scène, chaque temps fort avec son événement, pas de rendu partiel | mise en scène scripts/story/V02/__init__.py, storyboard scripts/storyboards/V02.json |
| Synchro sous-titres | ✔ | 76 ms | < 150 ms | sous-titres (props Story)/alignement + image : 73 ms ; décalage audio MP4 : 3 ms ; alignement scribe vérifié sur 28 pauses mesurées, aucun conflit |
| Aucun mot coupé | ✔ | ok | tous les mots, entiers, dans la largeur | 250 mots, groupe le plus large 702/760 px (Inter Bold 64 px, film Story) |
| Accents et caractères | ✔ | ok | UTF-8 NFC, glyphes présents, aucun mojibake | mots hors dictionnaire à relire : Appli, appli, cliquais, cliqué |
| Pas de saturation | ✔ | true peak -2.2 dBTP, 0 échantillon(s) écrêté(s) | ≤ -1.0 dBTP, 0 écrêtage |  |
| Loudness | ✔ | -14.2 LUFS | -14 ± 1 LUFS |  |
| Surbrillance à l'image près | ✔ | 249/249 changements à l'image exacte | le mot surligné change à l'image du début du mot, pas avant ; toujours un mot surligné à l'écran | mesuré sur la ligne de sous-titres décodée |
| Zones réservées dégagées | ✔ | haut 0.00% (image 0); bas 0.00% (image 0); droite 0.06% (image 1970) | ≤ 0.3% de pixels hors fond dans les 160 px du haut, les 380 px du bas et à droite de x = 940 (version sans sous-titres) | interface TikTok / Reels : rien d'important sous les bandeaux ni sous la colonne d'icônes |
| Jamais d'image figée | ✔ | tenue la plus longue 1.2 s (images 1677-1713) | aucune image figée plus de 3.5 s, hors carte de fin (dès l'image 2589) | 36 tenues ≥ 0,5 s (au moins 12 px à mi-résolution qui changent de plus de 16 niveaux = mouvement) |
| Version sans sous-titres conforme | ✔ | PSNR 46.3 dB au pire (image 2592), 2678 / 2678 images | ≥ 40 dB au-dessus de y = 1270, 2678 images dans les deux versions | médiane 99.0 dB |
| Bande d'action jamais vide | ✔ | 5.8% au pire (image 10) | ≥ 1% de pixels hors fond entre y = 160 et 1270, à chaque image | médiane 17.4% |
