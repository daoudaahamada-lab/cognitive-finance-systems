# Rapport qualité — vidéos WealthTech Horizon

| Vidéo | Source | Résultat | Durée | Synchro | Loudness | Contrôlée le |
|---|---|---|---|---|---|---|
| V01 | WTH-003 | ✅ OK | 58.23 s | 72 ms | -14.1 LUFS | 2026-10-21T00:57:10+00:00 |
| V02 | WTH-002 | ✅ OK | 55.97 s | 38 ms | -14.3 LUFS | 2026-10-18T17:51:57+00:00 |

## V01 (WTH-003) — OK

| Contrôle | Résultat | Valeur | Attendu | Détail |
|---|---|---|---|---|
| Durée | ✔ | 58.23 s | 45 à 60 s |  |
| Format | ✔ | h264 1080x1920 30/1 yuv420p + aac, profil High, tv/bt709, audio 48000 Hz, 190 kb/s | h264 1080x1920 30/1 yuv420p + aac, BT.709 plage tv |  |
| Rendu Story à jour | ✔ | 1747 images, empreintes identiques | 1747 images (props), empreintes props + storyboard + mise en scène du rendu = fichiers actuels, version sans sous-titres du même rendu | props f70cd56b0f, storyboard 81d0c89847, mise en scène c1ee87c01d |
| Mise en scène complète | ✔ | 20 scènes mises en scène, tous les temps forts posés | chaque scène du storyboard mise en scène, chaque temps fort avec son événement, pas de rendu partiel | mise en scène scripts/story/V01/__init__.py, storyboard scripts/storyboards/V01.json |
| Synchro sous-titres | ✔ | 72 ms | < 150 ms | sous-titres (props Story)/alignement + image : 69 ms ; décalage audio MP4 : 3 ms ; alignement scribe vérifié sur 21 pauses mesurées, aucun conflit |
| Aucun mot coupé | ✔ | ok | tous les mots, entiers, dans la largeur | 147 mots, groupe le plus large 713/760 px (Inter Bold 64 px, film Story) |
| Accents et caractères | ✔ | ok | UTF-8 NFC, glyphes présents, aucun mojibake | mots hors dictionnaire à relire : Brief, Mail, brief, déc, févr, info |
| Pas de saturation | ✔ | true peak -2.2 dBTP, 0 échantillon(s) écrêté(s) | ≤ -1.0 dBTP, 0 écrêtage |  |
| Loudness | ✔ | -14.1 LUFS | -14 ± 1 LUFS |  |
| Surbrillance à l'image près | ✔ | 146/146 changements à l'image exacte | le mot surligné change à l'image du début du mot, pas avant ; toujours un mot surligné à l'écran | mesuré sur la ligne de sous-titres décodée |
| Zones réservées dégagées | ✔ | haut 0.00% (image 0); bas 0.00% (image 0); droite 0.21% (image 1329) | ≤ 0.3% de pixels hors fond dans les 160 px du haut, les 380 px du bas et à droite de x = 940 (version sans sous-titres) | interface TikTok / Reels : rien d'important sous les bandeaux ni sous la colonne d'icônes |
| Jamais d'image figée | ✔ | tenue la plus longue 0.9 s (images 627-653) | aucune image figée plus de 3.5 s, hors carte de fin (dès l'image 1658) | 15 tenues ≥ 0,5 s (au moins 12 px à mi-résolution qui changent de plus de 16 niveaux = mouvement) |
| Version sans sous-titres conforme | ✔ | PSNR 51.9 dB au pire (image 1255), 1747 / 1747 images | ≥ 40 dB au-dessus de y = 1270, 1747 images dans les deux versions | médiane 99.0 dB |
| Bande d'action jamais vide | ✔ | 2.0% au pire (image 1662) | ≥ 1% de pixels hors fond entre y = 160 et 1270, à chaque image | médiane 11.4% |

## V02 (WTH-002) — OK

| Contrôle | Résultat | Valeur | Attendu | Détail |
|---|---|---|---|---|
| Durée | ✔ | 55.97 s | 45 à 60 s |  |
| Format | ✔ | h264 1080x1920 30/1 yuv420p + aac | h264 1080x1920 30/1 yuv420p + aac |  |
| Synchro sous-titres | ✔ | 38 ms | < 150 ms | sous-titres/alignement + image : 35 ms ; décalage audio MP4 : 3 ms ; alignement scribe vérifié sur 14 pauses mesurées, aucun conflit |
| Aucun mot coupé | ✔ | ok | tous les mots, entiers, dans la largeur | 149 mots, groupe le plus large 724/860 px |
| Accents et caractères | ✔ | ok | UTF-8 NFC, glyphes présents, aucun mojibake | mots hors dictionnaire à relire : Appli, appli |
| Pas de saturation | ✔ | true peak -1.9 dBTP, 0 échantillon(s) écrêté(s) | ≤ -1.0 dBTP, 0 écrêtage |  |
| Loudness | ✔ | -14.3 LUFS | -14 ± 1 LUFS |  |
