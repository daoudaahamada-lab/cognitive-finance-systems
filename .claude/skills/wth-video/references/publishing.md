# Livraison et publication

À lire pour livrer une vidéo finie, proposer les dates, l'envoyer sur Cloudinary ou la programmer dans Metricool.
L'utilisateur a choisi la route suivante : je livre les MP4 ; il les dépose dans un dossier Drive partagé ; je les
envoie sur Cloudinary depuis le Drive ; je les programme dans Metricool une fois les dates validées.

Pourquoi cette route : `api.cloudinary.com` n'est pas joignable depuis la machine, donc `make upload` et
`make publish` ne marchent pas ici. Les connecteurs Cloudinary et Metricool, eux, fonctionnent, mais le connecteur
Cloudinary ne lit qu'une URL publique, pas un fichier de la machine. Le Drive partagé fournit cette URL sans rendre
les vidéos publiques sur GitHub avant leur date.

## 0. Conditions

- La vidéo est finie : `output/qa/Vxx.json` dit `ok: true` en mode `story`, et le contrôle sans son est réussi
  (`status.py show Vxx` : `qa` et `mute_verify` à `done`). La QA est le garde-fou de `pipeline/upload.py` ; on le
  respecte aussi à la main.
- **Rien n'est programmé sans l'accord de l'utilisateur sur les dates** (point de validation
  `publication_dates_approved`).
- Avant la première publication, pose deux questions et note les réponses dans le point de validation
  `publication_questions` :
  - la licence Remotion : gratuite pour un particulier ou une entreprise de 3 personnes au plus, licence entreprise
    au-delà ; le MP4 porte « Made with Remotion » ;
  - la déclaration de contenu généré par l'IA, à cause de la voix de synthèse : `isAigc` (TikTok) et
    `isAiGenerated` (Instagram).

## 1. Livrer (chaque vidéo dès qu'elle est prête)

1. Envoie le film avec `SendUserFile` : `wth-videos/output/WTH-Vxx.mp4`. Pour V01, et chaque fois que l'utilisateur
   veut juger son critère, ajoute `wth-videos/build/Vxx/story/film_sans_sous_titres.mp4`.
2. Donne dans la légende du fichier, ou juste après, le texte prêt à coller : `legende`, une ligne vide, puis les
   `hashtags` séparés par des espaces (champs de `scripts/scripts.json`) :
   ```bash
   cd wth-videos && python3 -c "import json;s={x['id']:x for x in json.load(open('scripts/scripts.json'))}['V07'];print(s['titre']);print();print(s['legende']+'\n\n'+' '.join(s['hashtags']))"
   ```
3. `status.py set Vxx delivered done --note "envoyée le <date>"`.

## 2. Proposer les dates

Règle choisie par l'utilisateur : **une vidéo tous les 2 jours à 17:00 (Europe/Paris)**, dans l'ordre V01 → V15,
décalée par rapport au plan d'origine (`config/videos.csv` : V01 le 20/10, V15 le 17/11), qui est déjà dépassé.

1. Première date : le premier jour libre après la livraison de la dernière vidéo à programmer, ou la date que
   l'utilisateur donne.
2. Regarde ce qui est déjà programmé : `getScheduledPosts` de Metricool sur la période. Les carrousels occupent
   08:00, 13:00 et 19:30 ; 17:00 est l'heure des vidéos (`config.yaml` `planning.heure`).
3. Présente un tableau Vxx → date et heure, et attends son accord.
4. Après l'accord :
   - écris les dates dans `config/videos.csv` et dans le champ `date` de `scripts/scripts.json`. Ne touche à rien
     d'autre : la clé de la voix ne dépend que du texte et des réglages, pas de la date ;
   - `status.py checkpoint publication_dates_approved done --note "V01 <date> … tous les 2 jours à 17:00"`.

Fuseau : l'heure d'été finit le dernier dimanche d'octobre (2026-10-25). Avant cette date, 17:00 à Paris s'écrit
`+02:00` ; après, `+01:00`. Calcule le décalage, ne le devine pas :
```bash
python3 -c "from datetime import datetime;from zoneinfo import ZoneInfo;print(datetime(2026,10,28,17,0,tzinfo=ZoneInfo('Europe/Paris')).isoformat())"
```

## 3. Drive, puis Cloudinary

1. L'utilisateur dépose les MP4 dans un dossier Drive partagé en « tous les utilisateurs disposant du lien »
   (lecteur). Retrouve chaque fichier avec le connecteur Google Drive : `search_files` sur le nom `WTH-Vxx.mp4`, ou
   le lien du dossier qu'il donne.
2. Vérifie le partage avec `get_file_permissions` : il faut une permission `anyone` en lecture. Sinon, demande à
   l'utilisateur de partager le dossier. Cloudinary recevrait une page de connexion au lieu de la vidéo.
3. Envoie sur Cloudinary avec `upload-asset` :
   ```json
   {"resource_type": "video",
    "upload_request": {"file": "https://drive.google.com/uc?export=download&id=<fileId>",
                       "public_id": "WTH-V07", "asset_folder": "WTH-V2/videos", "display_name": "WTH-V07",
                       "overwrite": false, "tags": ["WTH-V2", "video", "V07"]}}
   ```
   `public_id` et dossier viennent de `config.yaml` (`cloudinary.public_id_pattern`, `cloudinary.folder`).
4. Contrôle la réponse :
   - `resource_type` vaut `video`, `format` vaut `mp4`, et la taille est de 1080 × 1920 ;
   - `duration` est égale à la durée de la QA, à 0,1 s près ;
   - `bytes` est égal à la taille locale (`stat -c %s wth-videos/output/WTH-V07.mp4`).

   Un écart signale en général un fichier Drive qui n'est pas le bon, ou une page HTML reçue à la place de la
   vidéo.
5. `existing: true` : un fichier portait déjà ce `public_id`, et `overwrite: false` l'a laissé en place. Compare
   `bytes` et `duration`. S'ils diffèrent, demande à l'utilisateur avant de relancer avec `overwrite: true`.

## 4. `output/uploads.json`, puis `make planning`

`uploads.json` a le format qu'écrit `pipeline/upload.py`, une entrée par vidéo :
```bash
cd wth-videos && python3 - <<'EOF'
import json, pathlib
from datetime import datetime, timezone
p = pathlib.Path("output/uploads.json")
u = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
u["V07"] = {"public_id": "WTH-V07", "asset_id": "<asset_id>", "secure_url": "<secure_url>", "version": 0,
            "bytes": 0, "duration": 0.0, "existing": False,
            "uploaded_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
p.write_text(json.dumps(u, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
EOF
make planning      # -> output/planning_videos.csv : id, date, heure, URL Cloudinary, légende, hashtags
```
Remplace chaque valeur par celle de la réponse de Cloudinary. Commite `output/uploads.json` et
`output/planning_videos.csv`.

## 5. Metricool

Conditions : les dates sont validées, `uploads.json` a la `secure_url` de la vidéo, et l'utilisateur a répondu sur
la déclaration IA.

Fais un appel `createScheduledPost` **par réseau** (tiktok, instagram, facebook), comme pour les carrousels
(`pipeline/carousel_jobs.py`). Un échec sur un réseau se reprend alors seul, sans doublon sur les autres, et chaque
post a son identifiant à vérifier.

- `blogId` : `"6791889"`.
- `date` : ISO 8601 avec le décalage de Paris, ex. `"2026-10-28T17:00:00+01:00"` (voir « Fuseau »).
- `info` : une chaîne JSON.
  ```json
  {"autoPublish": true, "draft": false, "descendants": [], "firstCommentText": "", "hasNotReadNotes": false,
   "providers": [{"network": "instagram"}],
   "publicationDate": {"dateTime": "2026-10-28T17:00:00", "timezone": "Europe/Paris"},
   "shortener": false, "smartLinkData": {"ids": []},
   "text": "<legende>\n\n<hashtags séparés par des espaces>",
   "media": ["<secure_url Cloudinary>"], "mediaAltText": [],
   "instagramData": {"type": "REEL", "showReelOnFeed": true, "isAiGenerated": false}}
  ```
- Donnée propre à chaque réseau, la seule partie qui change :
  - TikTok : `"tiktokData": {"privacyOption": "PUBLIC_TO_EVERYONE", "title": "<titre>", "autoAddMusic": false,
    "disableComment": false, "disableDuet": false, "disableStitch": false, "isAigc": false}`.
    `autoAddMusic` reste à `false` : la vidéo a sa voix, alors que les carrousels photo ajoutaient une musique.
  - Instagram : `"instagramData": {"type": "REEL", "showReelOnFeed": true, "isAiGenerated": false}`.
  - Facebook : `"facebookData": {"type": "REEL", "title": "<titre>"}`.
  - `isAigc` et `isAiGenerated` prennent la valeur que l'utilisateur a choisie (`false` n'est qu'un exemple).
- Média : la vidéo MP4 H.264 servie par Cloudinary convient aux trois réseaux. Leçon des carrousels : TikTok
  refusait le PNG pour les posts photo, d'où le JPEG converti par Cloudinary ; pour une vidéo, ce problème ne se pose
  pas.
- Couverture : par défaut, la première image. `videoCoverMilliseconds` choisit une autre image, seulement si
  l'utilisateur le demande.

Vérifie ensuite avec `getScheduledPosts` sur la date : trois posts à 17:00, réseaux corrects, `autoPublish: true`,
`draft: false`, média `mp4`. Puis note-le :
`status.py set Vxx published done scheduled_at='"2026-10-28T17:00+01:00"' metricool='{"tiktok": "<id>", "instagram": "<id>", "facebook": "<id>"}'`.

## Ce qui ne marche pas ici

| Voie | Pourquoi |
|---|---|
| `make upload`, `make publish` | `api.cloudinary.com` bloqué depuis la machine ; pas de `CLOUDINARY_URL` |
| `upload-asset` avec un chemin local (`file://…`) | le connecteur ne voit pas les fichiers de la machine |
| `sign-upload` + POST depuis la machine | même blocage réseau vers l'API Cloudinary |
| une URL GitHub (branche temporaire) | dépôt public : les vidéos seraient visibles avant leur date |
