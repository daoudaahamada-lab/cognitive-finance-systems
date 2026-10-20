# Rapport qualité — vidéos WealthTech Horizon

| Vidéo | Source | Résultat | Durée | Synchro | Loudness | Contrôlée le |
|---|---|---|---|---|---|---|
| V01 | WTH-003 | ✅ OK | 58.17 s | 19 ms | -14.1 LUFS | 2026-10-20T10:44:33+00:00 |
| V02 | WTH-002 | ✅ OK | 55.97 s | 38 ms | -14.3 LUFS | 2026-10-18T17:51:57+00:00 |

## V01 (WTH-003) — OK

| Contrôle | Résultat | Valeur | Attendu | Détail |
|---|---|---|---|---|
| Durée | ✔ | 58.17 s | 45 à 60 s |  |
| Format | ✔ | h264 1080x1920 30/1 yuv420p + aac, profil High, tv/bt709, audio 48000 Hz, 190 kb/s | h264 1080x1920 30/1 yuv420p + aac, BT.709 plage tv |  |
| Rendu motion à jour | ✔ | 1745 images, empreintes identiques | 1745 images (motion.json), empreintes props + plan du rendu = fichiers actuels | props b4ae75e7e1, plan a9b05416a4 |
| Synchro sous-titres | ✔ | 19 ms | < 150 ms | sous-titres (motion.json)/alignement + image : 16 ms ; décalage audio MP4 : 3 ms ; alignement scribe vérifié sur 21 pauses mesurées, aucun conflit |
| Aucun mot coupé | ✔ | ok | tous les mots, entiers, dans la largeur | 147 mots, groupe le plus large 730/760 px (Inter ExtraBold 66 px, rendu motion) |
| Accents et caractères | ✔ | ok | UTF-8 NFC, glyphes présents, aucun mojibake | mots hors dictionnaire à relire : brief, info |
| Pas de saturation | ✔ | true peak -2.3 dBTP, 0 échantillon(s) écrêté(s) | ≤ -1.0 dBTP, 0 écrêtage |  |
| Loudness | ✔ | -14.1 LUFS | -14 ± 1 LUFS |  |
| Scène jamais vide | ✔ | 3.8% au pire (image 253, chapitre 1) | ≥ 3% de pixels allumés dans la bande visuelle à chaque passage et carte de chapitre | 21 fenêtres ; médiane de toute la vidéo 19.2%, minimum 3.8% (image 253) |
| Passages sans creux | ✔ | 0.80 au pire (image 486) | ≥ 0.78 (luminance du passage / plan le moins lumineux des deux) | 21 passages, médiane 1.08 |
| Rangée d'étapes dégagée | ✔ | ok | aucun rouge dans la boîte du héros pendant ses premières images après une carte de chapitre | 15 images contrôlées |
| Surbrillance à l'image près | ✔ | 146/146 changements à l'image exacte | le mot rouge change à l'image du début du mot, pas avant ; toujours un mot rouge à l'écran | mesuré sur la ligne de sous-titres décodée |

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
