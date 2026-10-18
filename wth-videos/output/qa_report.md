# Rapport qualité — vidéos WealthTech Horizon

| Vidéo | Source | Résultat | Durée | Synchro | Loudness | Contrôlée le |
|---|---|---|---|---|---|---|
| V01 | WTH-003 | ✅ OK | 58.23 s | 38 ms | -14.1 LUFS | 2026-10-18T17:51:26+00:00 |
| V02 | WTH-002 | ✅ OK | 55.97 s | 38 ms | -14.3 LUFS | 2026-10-18T17:51:57+00:00 |

## V01 (WTH-003) — OK

| Contrôle | Résultat | Valeur | Attendu | Détail |
|---|---|---|---|---|
| Durée | ✔ | 58.23 s | 45 à 60 s |  |
| Format | ✔ | h264 1080x1920 30/1 yuv420p + aac | h264 1080x1920 30/1 yuv420p + aac |  |
| Synchro sous-titres | ✔ | 38 ms | < 150 ms | sous-titres/alignement + image : 35 ms ; décalage audio MP4 : 3 ms ; alignement scribe vérifié sur 21 pauses mesurées, aucun conflit |
| Aucun mot coupé | ✔ | ok | tous les mots, entiers, dans la largeur | 147 mots, groupe le plus large 722/860 px |
| Accents et caractères | ✔ | ok | UTF-8 NFC, glyphes présents, aucun mojibake | mots hors dictionnaire à relire : brief, info |
| Pas de saturation | ✔ | true peak -2.3 dBTP, 0 échantillon(s) écrêté(s) | ≤ -1.0 dBTP, 0 écrêtage |  |
| Loudness | ✔ | -14.1 LUFS | -14 ± 1 LUFS |  |

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
