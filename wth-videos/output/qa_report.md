# Rapport qualité — vidéos WealthTech Horizon

| Vidéo | Source | Résultat | Durée | Synchro | Loudness | Contrôlée le |
|---|---|---|---|---|---|---|
| V01 | WTH-003 | ✅ OK | 93.23 s | 89 ms | -14.2 LUFS | 2026-10-21T19:49:43+00:00 |
| V02 | WTH-002 | ✅ OK | 89.27 s | 76 ms | -14.2 LUFS | 2026-10-23T13:14:08+00:00 |
| V03 | WTH-016 | ✅ OK | 97.53 s | 80 ms | -14.2 LUFS | 2026-10-23T20:07:14+00:00 |
| V04 | WTH-006 | ✅ OK | 89.00 s | 62 ms | -14.1 LUFS | 2026-10-23T19:38:11+00:00 |
| V05 | WTH-009 | ✅ OK | 89.47 s | 85 ms | -14.1 LUFS | 2026-10-24T08:35:28+00:00 |
| V06 | WTH-025 | ✅ OK | 89.33 s | 84 ms | -14.2 LUFS | 2026-10-24T07:28:11+00:00 |
| V07 | WTH-014 | ✅ OK | 98.93 s | 70 ms | -14.2 LUFS | 2026-10-24T11:20:43+00:00 |
| V08 | WTH-004 | ✅ OK | 95.73 s | 80 ms | -14.3 LUFS | 2026-10-24T11:24:25+00:00 |
| V09 | WTH-019 | ✅ OK | 90.80 s | 60 ms | -14.1 LUFS | 2026-10-24T16:13:55+00:00 |
| V10 | WTH-064 | ✅ OK | 94.97 s | 95 ms | -14.2 LUFS | 2026-10-24T16:43:00+00:00 |
| V11 | WTH-021 | ✅ OK | 93.03 s | 78 ms | -14.3 LUFS | 2026-10-24T22:06:06+00:00 |
| V12 | WTH-049 | ✅ OK | 95.77 s | 86 ms | -14.3 LUFS | 2026-10-24T21:31:48+00:00 |

## V01 (WTH-003) — OK

| Contrôle | Résultat | Valeur | Attendu | Détail |
|---|---|---|---|---|
| Durée | ✔ | 93.23 s | 45 à 180 s |  |
| Format | ✔ | h264 1080x1920 30/1 yuv420p + aac, profil High, tv/bt709, audio 48000 Hz, 190 kb/s | h264 1080x1920 30/1 yuv420p + aac, BT.709 plage tv |  |
| Rendu Story à jour | ✔ | 2797 images, empreintes identiques | 2797 images (props), empreintes props + storyboard + mise en scène du rendu = fichiers actuels, version sans sous-titres du même rendu | props 75bc29d3cd, storyboard 0b19fdde73, mise en scène 597b73309a |
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
| Rendu Story à jour | ✔ | 2678 images, empreintes identiques | 2678 images (props), empreintes props + storyboard + mise en scène du rendu = fichiers actuels, version sans sous-titres du même rendu | props 0e5ccee90c, storyboard c161705e70, mise en scène 251097b006 |
| Mise en scène complète | ✔ | 22 scènes mises en scène, tous les temps forts posés | chaque scène du storyboard mise en scène, chaque temps fort avec son événement, pas de rendu partiel | mise en scène scripts/story/V02/__init__.py, storyboard scripts/storyboards/V02.json |
| Synchro sous-titres | ✔ | 76 ms | < 150 ms | sous-titres (props Story)/alignement + image : 73 ms ; décalage audio MP4 : 3 ms ; alignement scribe vérifié sur 28 pauses mesurées, aucun conflit |
| Aucun mot coupé | ✔ | ok | tous les mots, entiers, dans la largeur | 250 mots, groupe le plus large 702/760 px (Inter Bold 64 px, film Story) |
| Accents et caractères | ✔ | ok | UTF-8 NFC, glyphes présents, aucun mojibake | mots hors dictionnaire à relire : Appli, appli, cliquais, cliqué |
| Pas de saturation | ✔ | true peak -2.2 dBTP, 0 échantillon(s) écrêté(s) | ≤ -1.0 dBTP, 0 écrêtage |  |
| Loudness | ✔ | -14.2 LUFS | -14 ± 1 LUFS |  |
| Surbrillance à l'image près | ✔ | 249/249 changements à l'image exacte | le mot surligné change à l'image du début du mot, pas avant ; toujours un mot surligné à l'écran | mesuré sur la ligne de sous-titres décodée |
| Zones réservées dégagées | ✔ | haut 0.00% (image 0); bas 0.00% (image 0); droite 0.06% (image 1970) | ≤ 0.3% de pixels hors fond dans les 160 px du haut, les 380 px du bas et à droite de x = 940 (version sans sous-titres) | interface TikTok / Reels : rien d'important sous les bandeaux ni sous la colonne d'icônes |
| Jamais d'image figée | ✔ | tenue la plus longue 1.2 s (images 1677-1713) | aucune image figée plus de 3.5 s, hors carte de fin (dès l'image 2589) | 33 tenues ≥ 0,5 s (au moins 12 px à mi-résolution qui changent de plus de 16 niveaux = mouvement) |
| Version sans sous-titres conforme | ✔ | PSNR 49.5 dB au pire (image 2619), 2678 / 2678 images | ≥ 40 dB au-dessus de y = 1270, 2678 images dans les deux versions | médiane 99.0 dB |
| Bande d'action jamais vide | ✔ | 6.0% au pire (image 2639) | ≥ 1% de pixels hors fond entre y = 160 et 1270, à chaque image | médiane 19.3% |

## V03 (WTH-016) — OK

| Contrôle | Résultat | Valeur | Attendu | Détail |
|---|---|---|---|---|
| Durée | ✔ | 97.53 s | 45 à 180 s |  |
| Format | ✔ | h264 1080x1920 30/1 yuv420p + aac, profil High, tv/bt709, audio 48000 Hz, 190 kb/s | h264 1080x1920 30/1 yuv420p + aac, BT.709 plage tv |  |
| Rendu Story à jour | ✔ | 2926 images, empreintes identiques | 2926 images (props), empreintes props + storyboard + mise en scène du rendu = fichiers actuels, version sans sous-titres du même rendu | props 87390e8212, storyboard cc24fcdd03, mise en scène 1f63ebd6fb |
| Mise en scène complète | ✔ | 21 scènes mises en scène, tous les temps forts posés | chaque scène du storyboard mise en scène, chaque temps fort avec son événement, pas de rendu partiel | mise en scène scripts/story/V03/__init__.py, storyboard scripts/storyboards/V03.json |
| Synchro sous-titres | ✔ | 80 ms | < 150 ms | sous-titres (props Story)/alignement + image : 77 ms ; décalage audio MP4 : 3 ms ; alignement scribe vérifié sur 26 pauses mesurées, aucun conflit |
| Aucun mot coupé | ✔ | ok | tous les mots, entiers, dans la largeur | 235 mots, groupe le plus large 742/760 px (Inter Bold 64 px, film Story) |
| Accents et caractères | ✔ | ok | UTF-8 NFC, glyphes présents, aucun mojibake | aucun mot hors dictionnaire |
| Pas de saturation | ✔ | true peak -2.1 dBTP, 0 échantillon(s) écrêté(s) | ≤ -1.0 dBTP, 0 écrêtage |  |
| Loudness | ✔ | -14.2 LUFS | -14 ± 1 LUFS |  |
| Surbrillance à l'image près | ✔ | 234/234 changements à l'image exacte | le mot surligné change à l'image du début du mot, pas avant ; toujours un mot surligné à l'écran | mesuré sur la ligne de sous-titres décodée |
| Zones réservées dégagées | ✔ | haut 0.00% (image 0); bas 0.00% (image 0); droite 0.04% (image 2288) | ≤ 0.3% de pixels hors fond dans les 160 px du haut, les 380 px du bas et à droite de x = 940 (version sans sous-titres) | interface TikTok / Reels : rien d'important sous les bandeaux ni sous la colonne d'icônes |
| Jamais d'image figée | ✔ | tenue la plus longue 1.7 s (images 1159-1208) | aucune image figée plus de 3.5 s, hors carte de fin (dès l'image 2835) | 46 tenues ≥ 0,5 s (au moins 12 px à mi-résolution qui changent de plus de 16 niveaux = mouvement) |
| Version sans sous-titres conforme | ✔ | PSNR 50.7 dB au pire (image 2838), 2926 / 2926 images | ≥ 40 dB au-dessus de y = 1270, 2926 images dans les deux versions | médiane 99.0 dB |
| Bande d'action jamais vide | ✔ | 2.0% au pire (image 2841) | ≥ 1% de pixels hors fond entre y = 160 et 1270, à chaque image | médiane 13.5% |

## V04 (WTH-006) — OK

| Contrôle | Résultat | Valeur | Attendu | Détail |
|---|---|---|---|---|
| Durée | ✔ | 89.00 s | 45 à 180 s |  |
| Format | ✔ | h264 1080x1920 30/1 yuv420p + aac, profil High, tv/bt709, audio 48000 Hz, 190 kb/s | h264 1080x1920 30/1 yuv420p + aac, BT.709 plage tv |  |
| Rendu Story à jour | ✔ | 2670 images, empreintes identiques | 2670 images (props), empreintes props + storyboard + mise en scène du rendu = fichiers actuels, version sans sous-titres du même rendu | props bc0e8f36ca, storyboard a939800938, mise en scène 688be4cab3 |
| Mise en scène complète | ✔ | 21 scènes mises en scène, tous les temps forts posés | chaque scène du storyboard mise en scène, chaque temps fort avec son événement, pas de rendu partiel | mise en scène scripts/story/V04/__init__.py, storyboard scripts/storyboards/V04.json |
| Synchro sous-titres | ✔ | 62 ms | < 150 ms | sous-titres (props Story)/alignement + image : 59 ms ; décalage audio MP4 : 3 ms ; alignement scribe vérifié sur 27 pauses mesurées, aucun conflit |
| Aucun mot coupé | ✔ | ok | tous les mots, entiers, dans la largeur | 244 mots, groupe le plus large 673/760 px (Inter Bold 64 px, film Story) |
| Accents et caractères | ✔ | ok | UTF-8 NFC, glyphes présents, aucun mojibake | mots hors dictionnaire à relire : appli |
| Pas de saturation | ✔ | true peak -2.0 dBTP, 0 échantillon(s) écrêté(s) | ≤ -1.0 dBTP, 0 écrêtage |  |
| Loudness | ✔ | -14.1 LUFS | -14 ± 1 LUFS |  |
| Surbrillance à l'image près | ✔ | 243/243 changements à l'image exacte | le mot surligné change à l'image du début du mot, pas avant ; toujours un mot surligné à l'écran | mesuré sur la ligne de sous-titres décodée |
| Zones réservées dégagées | ✔ | haut 0.00% (image 0); bas 0.00% (image 0); droite 0.09% (image 652) | ≤ 0.3% de pixels hors fond dans les 160 px du haut, les 380 px du bas et à droite de x = 940 (version sans sous-titres) | interface TikTok / Reels : rien d'important sous les bandeaux ni sous la colonne d'icônes |
| Jamais d'image figée | ✔ | tenue la plus longue 1.6 s (images 1985-2032) | aucune image figée plus de 3.5 s, hors carte de fin (dès l'image 2579) | 38 tenues ≥ 0,5 s (au moins 12 px à mi-résolution qui changent de plus de 16 niveaux = mouvement) |
| Version sans sous-titres conforme | ✔ | PSNR 54.4 dB au pire (image 2583), 2670 / 2670 images | ≥ 40 dB au-dessus de y = 1270, 2670 images dans les deux versions | médiane 99.0 dB |
| Bande d'action jamais vide | ✔ | 4.2% au pire (image 2585) | ≥ 1% de pixels hors fond entre y = 160 et 1270, à chaque image | médiane 9.7% |

## V05 (WTH-009) — OK

| Contrôle | Résultat | Valeur | Attendu | Détail |
|---|---|---|---|---|
| Durée | ✔ | 89.47 s | 45 à 180 s |  |
| Format | ✔ | h264 1080x1920 30/1 yuv420p + aac, profil High, tv/bt709, audio 48000 Hz, 190 kb/s | h264 1080x1920 30/1 yuv420p + aac, BT.709 plage tv |  |
| Rendu Story à jour | ✔ | 2684 images, empreintes identiques | 2684 images (props), empreintes props + storyboard + mise en scène du rendu = fichiers actuels, version sans sous-titres du même rendu | props 10e5529f95, storyboard 38992e8c46, mise en scène 60d2af8300 |
| Mise en scène complète | ✔ | 22 scènes mises en scène, tous les temps forts posés | chaque scène du storyboard mise en scène, chaque temps fort avec son événement, pas de rendu partiel | mise en scène scripts/story/V05/__init__.py, storyboard scripts/storyboards/V05.json |
| Synchro sous-titres | ✔ | 85 ms | < 150 ms | sous-titres (props Story)/alignement + image : 82 ms ; décalage audio MP4 : 3 ms ; alignement scribe vérifié sur 29 pauses mesurées, aucun conflit |
| Aucun mot coupé | ✔ | ok | tous les mots, entiers, dans la largeur | 243 mots, groupe le plus large 704/760 px (Inter Bold 64 px, film Story) |
| Accents et caractères | ✔ | ok | UTF-8 NFC, glyphes présents, aucun mojibake | mots hors dictionnaire à relire : Brief, Mail, brief, info, janv, mail, sourcé |
| Pas de saturation | ✔ | true peak -1.6 dBTP, 0 échantillon(s) écrêté(s) | ≤ -1.0 dBTP, 0 écrêtage |  |
| Loudness | ✔ | -14.1 LUFS | -14 ± 1 LUFS |  |
| Surbrillance à l'image près | ✔ | 242/242 changements à l'image exacte | le mot surligné change à l'image du début du mot, pas avant ; toujours un mot surligné à l'écran | mesuré sur la ligne de sous-titres décodée |
| Zones réservées dégagées | ✔ | haut 0.00% (image 0); bas 0.00% (image 0); droite 0.26% (image 1727) | ≤ 0.3% de pixels hors fond dans les 160 px du haut, les 380 px du bas et à droite de x = 940 (version sans sous-titres) | interface TikTok / Reels : rien d'important sous les bandeaux ni sous la colonne d'icônes |
| Jamais d'image figée | ✔ | tenue la plus longue 1.9 s (images 2251-2308) | aucune image figée plus de 3.5 s, hors carte de fin (dès l'image 2594) | 36 tenues ≥ 0,5 s (au moins 12 px à mi-résolution qui changent de plus de 16 niveaux = mouvement) |
| Version sans sous-titres conforme | ✔ | PSNR 52.1 dB au pire (image 2602), 2684 / 2684 images | ≥ 40 dB au-dessus de y = 1270, 2684 images dans les deux versions | médiane 99.0 dB |
| Bande d'action jamais vide | ✔ | 5.3% au pire (image 2605) | ≥ 1% de pixels hors fond entre y = 160 et 1270, à chaque image | médiane 13.6% |

## V06 (WTH-025) — OK

| Contrôle | Résultat | Valeur | Attendu | Détail |
|---|---|---|---|---|
| Durée | ✔ | 89.33 s | 45 à 180 s |  |
| Format | ✔ | h264 1080x1920 30/1 yuv420p + aac, profil High, tv/bt709, audio 48000 Hz, 190 kb/s | h264 1080x1920 30/1 yuv420p + aac, BT.709 plage tv |  |
| Rendu Story à jour | ✔ | 2680 images, empreintes identiques | 2680 images (props), empreintes props + storyboard + mise en scène du rendu = fichiers actuels, version sans sous-titres du même rendu | props 72cd799896, storyboard 02b8a3e72a, mise en scène bf190212e7 |
| Mise en scène complète | ✔ | 22 scènes mises en scène, tous les temps forts posés | chaque scène du storyboard mise en scène, chaque temps fort avec son événement, pas de rendu partiel | mise en scène scripts/story/V06/__init__.py, storyboard scripts/storyboards/V06.json |
| Synchro sous-titres | ✔ | 84 ms | < 150 ms | sous-titres (props Story)/alignement + image : 81 ms ; décalage audio MP4 : 3 ms ; alignement scribe vérifié sur 30 pauses mesurées, aucun conflit |
| Aucun mot coupé | ✔ | ok | tous les mots, entiers, dans la largeur | 234 mots, groupe le plus large 745/760 px (Inter Bold 64 px, film Story) |
| Accents et caractères | ✔ | ok | UTF-8 NFC, glyphes présents, aucun mojibake | mots hors dictionnaire à relire : max |
| Pas de saturation | ✔ | true peak -2.2 dBTP, 0 échantillon(s) écrêté(s) | ≤ -1.0 dBTP, 0 écrêtage |  |
| Loudness | ✔ | -14.2 LUFS | -14 ± 1 LUFS |  |
| Surbrillance à l'image près | ✔ | 233/233 changements à l'image exacte | le mot surligné change à l'image du début du mot, pas avant ; toujours un mot surligné à l'écran | mesuré sur la ligne de sous-titres décodée |
| Zones réservées dégagées | ✔ | haut 0.00% (image 0); bas 0.00% (image 0); droite 0.02% (image 1166) | ≤ 0.3% de pixels hors fond dans les 160 px du haut, les 380 px du bas et à droite de x = 940 (version sans sous-titres) | interface TikTok / Reels : rien d'important sous les bandeaux ni sous la colonne d'icônes |
| Jamais d'image figée | ✔ | tenue la plus longue 1.8 s (images 801-853) | aucune image figée plus de 3.5 s, hors carte de fin (dès l'image 2592) | 37 tenues ≥ 0,5 s (au moins 12 px à mi-résolution qui changent de plus de 16 niveaux = mouvement) |
| Version sans sous-titres conforme | ✔ | PSNR 54.1 dB au pire (image 1259), 2680 / 2680 images | ≥ 40 dB au-dessus de y = 1270, 2680 images dans les deux versions | médiane 99.0 dB |
| Bande d'action jamais vide | ✔ | 4.1% au pire (image 2595) | ≥ 1% de pixels hors fond entre y = 160 et 1270, à chaque image | médiane 10.6% |

## V07 (WTH-014) — OK

| Contrôle | Résultat | Valeur | Attendu | Détail |
|---|---|---|---|---|
| Durée | ✔ | 98.93 s | 45 à 180 s |  |
| Format | ✔ | h264 1080x1920 30/1 yuv420p + aac, profil High, tv/bt709, audio 48000 Hz, 190 kb/s | h264 1080x1920 30/1 yuv420p + aac, BT.709 plage tv |  |
| Rendu Story à jour | ✔ | 2968 images, empreintes identiques | 2968 images (props), empreintes props + storyboard + mise en scène du rendu = fichiers actuels, version sans sous-titres du même rendu | props d8856a3304, storyboard d48cb570c4, mise en scène c1a4238720 |
| Mise en scène complète | ✔ | 22 scènes mises en scène, tous les temps forts posés | chaque scène du storyboard mise en scène, chaque temps fort avec son événement, pas de rendu partiel | mise en scène scripts/story/V07/__init__.py, storyboard scripts/storyboards/V07.json |
| Synchro sous-titres | ✔ | 70 ms | < 150 ms | sous-titres (props Story)/alignement + image : 67 ms ; décalage audio MP4 : 3 ms ; alignement scribe vérifié sur 33 pauses mesurées, aucun conflit |
| Aucun mot coupé | ✔ | ok | tous les mots, entiers, dans la largeur | 255 mots, groupe le plus large 670/760 px (Inter Bold 64 px, film Story) |
| Accents et caractères | ✔ | ok | UTF-8 NFC, glyphes présents, aucun mojibake | mots hors dictionnaire à relire : Tech |
| Pas de saturation | ✔ | true peak -2.3 dBTP, 0 échantillon(s) écrêté(s) | ≤ -1.0 dBTP, 0 écrêtage |  |
| Loudness | ✔ | -14.2 LUFS | -14 ± 1 LUFS |  |
| Surbrillance à l'image près | ✔ | 255/255 changements à l'image exacte | le mot surligné change à l'image du début du mot, pas avant ; toujours un mot surligné à l'écran | mesuré sur la ligne de sous-titres décodée |
| Zones réservées dégagées | ✔ | haut 0.00% (image 0); bas 0.00% (image 0); droite 0.10% (image 773) | ≤ 0.3% de pixels hors fond dans les 160 px du haut, les 380 px du bas et à droite de x = 940 (version sans sous-titres) | interface TikTok / Reels : rien d'important sous les bandeaux ni sous la colonne d'icônes |
| Jamais d'image figée | ✔ | tenue la plus longue 1.8 s (images 2143-2196) | aucune image figée plus de 3.5 s, hors carte de fin (dès l'image 2883) | 39 tenues ≥ 0,5 s (au moins 12 px à mi-résolution qui changent de plus de 16 niveaux = mouvement) |
| Version sans sous-titres conforme | ✔ | PSNR 52.6 dB au pire (image 2893), 2968 / 2968 images | ≥ 40 dB au-dessus de y = 1270, 2968 images dans les deux versions | médiane 99.0 dB |
| Bande d'action jamais vide | ✔ | 4.3% au pire (image 2886) | ≥ 1% de pixels hors fond entre y = 160 et 1270, à chaque image | médiane 11.8% |

## V08 (WTH-004) — OK

| Contrôle | Résultat | Valeur | Attendu | Détail |
|---|---|---|---|---|
| Durée | ✔ | 95.73 s | 45 à 180 s |  |
| Format | ✔ | h264 1080x1920 30/1 yuv420p + aac, profil High, tv/bt709, audio 48000 Hz, 190 kb/s | h264 1080x1920 30/1 yuv420p + aac, BT.709 plage tv |  |
| Rendu Story à jour | ✔ | 2872 images, empreintes identiques | 2872 images (props), empreintes props + storyboard + mise en scène du rendu = fichiers actuels, version sans sous-titres du même rendu | props 52d242a563, storyboard 5c095075ef, mise en scène 47726bfdba |
| Mise en scène complète | ✔ | 22 scènes mises en scène, tous les temps forts posés | chaque scène du storyboard mise en scène, chaque temps fort avec son événement, pas de rendu partiel | mise en scène scripts/story/V08/__init__.py, storyboard scripts/storyboards/V08.json |
| Synchro sous-titres | ✔ | 80 ms | < 150 ms | sous-titres (props Story)/alignement + image : 77 ms ; décalage audio MP4 : 3 ms ; alignement scribe vérifié sur 24 pauses mesurées, aucun conflit |
| Aucun mot coupé | ✔ | ok | tous les mots, entiers, dans la largeur | 250 mots, groupe le plus large 725/760 px (Inter Bold 64 px, film Story) |
| Accents et caractères | ✔ | ok | UTF-8 NFC, glyphes présents, aucun mojibake | aucun mot hors dictionnaire |
| Pas de saturation | ✔ | true peak -1.6 dBTP, 0 échantillon(s) écrêté(s) | ≤ -1.0 dBTP, 0 écrêtage |  |
| Loudness | ✔ | -14.3 LUFS | -14 ± 1 LUFS |  |
| Surbrillance à l'image près | ✔ | 249/249 changements à l'image exacte | le mot surligné change à l'image du début du mot, pas avant ; toujours un mot surligné à l'écran | mesuré sur la ligne de sous-titres décodée |
| Zones réservées dégagées | ✔ | haut 0.00% (image 0); bas 0.00% (image 0); droite 0.00% (image 0) | ≤ 0.3% de pixels hors fond dans les 160 px du haut, les 380 px du bas et à droite de x = 940 (version sans sous-titres) | interface TikTok / Reels : rien d'important sous les bandeaux ni sous la colonne d'icônes |
| Jamais d'image figée | ✔ | tenue la plus longue 2.0 s (images 150-209) | aucune image figée plus de 3.5 s, hors carte de fin (dès l'image 2790) | 54 tenues ≥ 0,5 s (au moins 12 px à mi-résolution qui changent de plus de 16 niveaux = mouvement) |
| Version sans sous-titres conforme | ✔ | PSNR 51.1 dB au pire (image 2796), 2872 / 2872 images | ≥ 40 dB au-dessus de y = 1270, 2872 images dans les deux versions | médiane 99.0 dB |
| Bande d'action jamais vide | ✔ | 5.1% au pire (image 13) | ≥ 1% de pixels hors fond entre y = 160 et 1270, à chaque image | médiane 18.4% |

## V09 (WTH-019) — OK

| Contrôle | Résultat | Valeur | Attendu | Détail |
|---|---|---|---|---|
| Durée | ✔ | 90.80 s | 45 à 180 s |  |
| Format | ✔ | h264 1080x1920 30/1 yuv420p + aac, profil High, tv/bt709, audio 48000 Hz, 190 kb/s | h264 1080x1920 30/1 yuv420p + aac, BT.709 plage tv |  |
| Rendu Story à jour | ✔ | 2724 images, empreintes identiques | 2724 images (props), empreintes props + storyboard + mise en scène du rendu = fichiers actuels, version sans sous-titres du même rendu | props 89c5c52f61, storyboard ca453fffab, mise en scène d1af430cec |
| Mise en scène complète | ✔ | 22 scènes mises en scène, tous les temps forts posés | chaque scène du storyboard mise en scène, chaque temps fort avec son événement, pas de rendu partiel | mise en scène scripts/story/V09/__init__.py, storyboard scripts/storyboards/V09.json |
| Synchro sous-titres | ✔ | 60 ms | < 150 ms | sous-titres (props Story)/alignement + image : 57 ms ; décalage audio MP4 : 3 ms ; alignement scribe vérifié sur 27 pauses mesurées, aucun conflit |
| Aucun mot coupé | ✔ | ok | tous les mots, entiers, dans la largeur | 246 mots, groupe le plus large 744/760 px (Inter Bold 64 px, film Story) |
| Accents et caractères | ✔ | ok | UTF-8 NFC, glyphes présents, aucun mojibake | mots hors dictionnaire à relire : boosté, œil |
| Pas de saturation | ✔ | true peak -1.7 dBTP, 0 échantillon(s) écrêté(s) | ≤ -1.0 dBTP, 0 écrêtage |  |
| Loudness | ✔ | -14.1 LUFS | -14 ± 1 LUFS |  |
| Surbrillance à l'image près | ✔ | 246/246 changements à l'image exacte | le mot surligné change à l'image du début du mot, pas avant ; toujours un mot surligné à l'écran | mesuré sur la ligne de sous-titres décodée |
| Zones réservées dégagées | ✔ | haut 0.00% (image 0); bas 0.00% (image 0); droite 0.00% (image 0) | ≤ 0.3% de pixels hors fond dans les 160 px du haut, les 380 px du bas et à droite de x = 940 (version sans sous-titres) | interface TikTok / Reels : rien d'important sous les bandeaux ni sous la colonne d'icônes |
| Jamais d'image figée | ✔ | tenue la plus longue 1.5 s (images 341-384) | aucune image figée plus de 3.5 s, hors carte de fin (dès l'image 2643) | 30 tenues ≥ 0,5 s (au moins 12 px à mi-résolution qui changent de plus de 16 niveaux = mouvement) |
| Version sans sous-titres conforme | ✔ | PSNR 50.7 dB au pire (image 2647), 2724 / 2724 images | ≥ 40 dB au-dessus de y = 1270, 2724 images dans les deux versions | médiane 99.0 dB |
| Bande d'action jamais vide | ✔ | 5.9% au pire (image 790) | ≥ 1% de pixels hors fond entre y = 160 et 1270, à chaque image | médiane 11.9% |

## V10 (WTH-064) — OK

| Contrôle | Résultat | Valeur | Attendu | Détail |
|---|---|---|---|---|
| Durée | ✔ | 94.97 s | 45 à 180 s |  |
| Format | ✔ | h264 1080x1920 30/1 yuv420p + aac, profil High, tv/bt709, audio 48000 Hz, 190 kb/s | h264 1080x1920 30/1 yuv420p + aac, BT.709 plage tv |  |
| Rendu Story à jour | ✔ | 2849 images, empreintes identiques | 2849 images (props), empreintes props + storyboard + mise en scène du rendu = fichiers actuels, version sans sous-titres du même rendu | props b32d118c44, storyboard 8dd401ae24, mise en scène 91d5dd3185 |
| Mise en scène complète | ✔ | 22 scènes mises en scène, tous les temps forts posés | chaque scène du storyboard mise en scène, chaque temps fort avec son événement, pas de rendu partiel | mise en scène scripts/story/V10/__init__.py, storyboard scripts/storyboards/V10.json |
| Synchro sous-titres | ✔ | 95 ms | < 150 ms | sous-titres (props Story)/alignement + image : 92 ms ; décalage audio MP4 : 3 ms ; alignement scribe vérifié sur 25 pauses mesurées, aucun conflit |
| Aucun mot coupé | ✔ | ok | tous les mots, entiers, dans la largeur | 237 mots, groupe le plus large 757/760 px (Inter Bold 64 px, film Story) |
| Accents et caractères | ✔ | ok | UTF-8 NFC, glyphes présents, aucun mojibake | mots hors dictionnaire à relire : Info, Invest, Nationalis, crypto |
| Pas de saturation | ✔ | true peak -2.1 dBTP, 0 échantillon(s) écrêté(s) | ≤ -1.0 dBTP, 0 écrêtage |  |
| Loudness | ✔ | -14.2 LUFS | -14 ± 1 LUFS |  |
| Surbrillance à l'image près | ✔ | 237/237 changements à l'image exacte | le mot surligné change à l'image du début du mot, pas avant ; toujours un mot surligné à l'écran | mesuré sur la ligne de sous-titres décodée |
| Zones réservées dégagées | ✔ | haut 0.00% (image 0); bas 0.00% (image 0); droite 0.10% (image 1001) | ≤ 0.3% de pixels hors fond dans les 160 px du haut, les 380 px du bas et à droite de x = 940 (version sans sous-titres) | interface TikTok / Reels : rien d'important sous les bandeaux ni sous la colonne d'icônes |
| Jamais d'image figée | ✔ | tenue la plus longue 1.6 s (images 639-685) | aucune image figée plus de 3.5 s, hors carte de fin (dès l'image 2764) | 40 tenues ≥ 0,5 s (au moins 12 px à mi-résolution qui changent de plus de 16 niveaux = mouvement) |
| Version sans sous-titres conforme | ✔ | PSNR 54.9 dB au pire (image 2659), 2849 / 2849 images | ≥ 40 dB au-dessus de y = 1270, 2849 images dans les deux versions | médiane 99.0 dB |
| Bande d'action jamais vide | ✔ | 4.6% au pire (image 7) | ≥ 1% de pixels hors fond entre y = 160 et 1270, à chaque image | médiane 12.0% |

## V11 (WTH-021) — OK

| Contrôle | Résultat | Valeur | Attendu | Détail |
|---|---|---|---|---|
| Durée | ✔ | 93.03 s | 45 à 180 s |  |
| Format | ✔ | h264 1080x1920 30/1 yuv420p + aac, profil High, tv/bt709, audio 48000 Hz, 190 kb/s | h264 1080x1920 30/1 yuv420p + aac, BT.709 plage tv |  |
| Rendu Story à jour | ✔ | 2791 images, empreintes identiques | 2791 images (props), empreintes props + storyboard + mise en scène du rendu = fichiers actuels, version sans sous-titres du même rendu | props b75ba40aeb, storyboard 387fc40c45, mise en scène e26cdcf1bd |
| Mise en scène complète | ✔ | 22 scènes mises en scène, tous les temps forts posés | chaque scène du storyboard mise en scène, chaque temps fort avec son événement, pas de rendu partiel | mise en scène scripts/story/V11/__init__.py, storyboard scripts/storyboards/V11.json |
| Synchro sous-titres | ✔ | 78 ms | < 150 ms | sous-titres (props Story)/alignement + image : 75 ms ; décalage audio MP4 : 3 ms ; alignement scribe vérifié sur 25 pauses mesurées, aucun conflit |
| Aucun mot coupé | ✔ | ok | tous les mots, entiers, dans la largeur | 241 mots, groupe le plus large 752/760 px (Inter Bold 64 px, film Story) |
| Accents et caractères | ✔ | ok | UTF-8 NFC, glyphes présents, aucun mojibake | mots hors dictionnaire à relire : Info, info, nov, pacse |
| Pas de saturation | ✔ | true peak -2.1 dBTP, 0 échantillon(s) écrêté(s) | ≤ -1.0 dBTP, 0 écrêtage |  |
| Loudness | ✔ | -14.3 LUFS | -14 ± 1 LUFS |  |
| Surbrillance à l'image près | ✔ | 240/240 changements à l'image exacte | le mot surligné change à l'image du début du mot, pas avant ; toujours un mot surligné à l'écran | mesuré sur la ligne de sous-titres décodée |
| Zones réservées dégagées | ✔ | haut 0.09% (image 358); bas 0.00% (image 0); droite 0.00% (image 0) | ≤ 0.3% de pixels hors fond dans les 160 px du haut, les 380 px du bas et à droite de x = 940 (version sans sous-titres) | interface TikTok / Reels : rien d'important sous les bandeaux ni sous la colonne d'icônes |
| Jamais d'image figée | ✔ | tenue la plus longue 1.8 s (images 1859-1913) | aucune image figée plus de 3.5 s, hors carte de fin (dès l'image 2697) | 38 tenues ≥ 0,5 s (au moins 12 px à mi-résolution qui changent de plus de 16 niveaux = mouvement) |
| Version sans sous-titres conforme | ✔ | PSNR 53.2 dB au pire (image 2702), 2791 / 2791 images | ≥ 40 dB au-dessus de y = 1270, 2791 images dans les deux versions | médiane 99.0 dB |
| Bande d'action jamais vide | ✔ | 3.7% au pire (image 2703) | ≥ 1% de pixels hors fond entre y = 160 et 1270, à chaque image | médiane 19.4% |

## V12 (WTH-049) — OK

| Contrôle | Résultat | Valeur | Attendu | Détail |
|---|---|---|---|---|
| Durée | ✔ | 95.77 s | 45 à 180 s |  |
| Format | ✔ | h264 1080x1920 30/1 yuv420p + aac, profil High, tv/bt709, audio 48000 Hz, 190 kb/s | h264 1080x1920 30/1 yuv420p + aac, BT.709 plage tv |  |
| Rendu Story à jour | ✔ | 2873 images, empreintes identiques | 2873 images (props), empreintes props + storyboard + mise en scène du rendu = fichiers actuels, version sans sous-titres du même rendu | props 29301101cc, storyboard 015dcd2364, mise en scène 12504f5451 |
| Mise en scène complète | ✔ | 22 scènes mises en scène, tous les temps forts posés | chaque scène du storyboard mise en scène, chaque temps fort avec son événement, pas de rendu partiel | mise en scène scripts/story/V12/__init__.py, storyboard scripts/storyboards/V12.json |
| Synchro sous-titres | ✔ | 86 ms | < 150 ms | sous-titres (props Story)/alignement + image : 83 ms ; décalage audio MP4 : 3 ms ; alignement scribe vérifié sur 30 pauses mesurées, aucun conflit |
| Aucun mot coupé | ✔ | ok | tous les mots, entiers, dans la largeur | 241 mots, groupe le plus large 679/760 px (Inter Bold 64 px, film Story) |
| Accents et caractères | ✔ | ok | UTF-8 NFC, glyphes présents, aucun mojibake | mots hors dictionnaire à relire : cash, illustratif, z |
| Pas de saturation | ✔ | true peak -2.3 dBTP, 0 échantillon(s) écrêté(s) | ≤ -1.0 dBTP, 0 écrêtage |  |
| Loudness | ✔ | -14.3 LUFS | -14 ± 1 LUFS |  |
| Surbrillance à l'image près | ✔ | 240/240 changements à l'image exacte | le mot surligné change à l'image du début du mot, pas avant ; toujours un mot surligné à l'écran | mesuré sur la ligne de sous-titres décodée |
| Zones réservées dégagées | ✔ | haut 0.00% (image 0); bas 0.00% (image 0); droite 0.10% (image 1895) | ≤ 0.3% de pixels hors fond dans les 160 px du haut, les 380 px du bas et à droite de x = 940 (version sans sous-titres) | interface TikTok / Reels : rien d'important sous les bandeaux ni sous la colonne d'icônes |
| Jamais d'image figée | ✔ | tenue la plus longue 1.9 s (images 1085-1142) | aucune image figée plus de 3.5 s, hors carte de fin (dès l'image 2786) | 43 tenues ≥ 0,5 s (au moins 12 px à mi-résolution qui changent de plus de 16 niveaux = mouvement) |
| Version sans sous-titres conforme | ✔ | PSNR 53.1 dB au pire (image 2793), 2873 / 2873 images | ≥ 40 dB au-dessus de y = 1270, 2873 images dans les deux versions | médiane 99.0 dB |
| Bande d'action jamais vide | ✔ | 3.1% au pire (image 2790) | ≥ 1% de pixels hors fond entre y = 160 et 1270, à chaque image | médiane 12.0% |
