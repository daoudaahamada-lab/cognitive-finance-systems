# Suivi de production : `wth-videos/scripts/production_status.json`

À lire avant de modifier le suivi à la main, ou pour interpréter `status.py show` et `status.py next`.

Le fichier est versionné. Une session neuve, ou un workflow repris après une coupure, y lit où en est chaque vidéo
sans relire la conversation. Il ne remplace pas les fichiers eux-mêmes : en cas de doute, `preflight.py` vérifie ce
qui existe vraiment (voix en cache, storyboard, mise en scène, QA).

Modifie-le **par `status.py`**, qui valide les noms d'étapes et d'états, horodate chaque changement et prend un
verrou (`wth-videos/build/.status.lock`). Deux workflows peuvent écrire en même temps : le storyboard de la vidéo
suivante pendant la fabrication de la vidéo en cours.

## Forme

```json
{
  "version": 1,
  "updated_at": "2026-10-20T19:24:49+00:00",
  "checkpoints": {
    "v01_full_approved": {"state": "pending", "label": "…", "note": "…", "updated_at": "…"},
    "publication_dates_approved": {"state": "pending", "label": "…"},
    "elevenlabs_credits": {"state": "pending", "label": "…"},
    "publication_questions": {"state": "pending", "label": "…"}
  },
  "notes": ["…"],
  "videos": {
    "V03": {
      "title": "1 % de frais par an : ce que ça coûte",
      "source": "WTH-016",
      "date_initiale": "2026-10-24",
      "max_duration_s": 62.0,
      "stages": {
        "voice": {"state": "done", "take": "4GUyNlztRyg1DFD6Zq97", "duration_s": 60.6,
                  "cache_key": "e43c18019584620a96b6a204", "aligned": "139/139",
                  "note": "…", "updated_at": "…"},
        "storyboard": {"state": "pending"},
        "spec": {"state": "pending"}, "render": {"state": "pending"}, "review": {"state": "pending"},
        "mute_verify": {"state": "pending"}, "qa": {"state": "pending"},
        "delivered": {"state": "pending"}, "published": {"state": "pending"}
      },
      "open_issues": [],
      "notes": []
    }
  }
}
```

## Les étapes, dans l'ordre

| Clé | Étape | « done » veut dire | Détails utiles (clé=valeur) |
|---|---|---|---|
| `voice` | voix | voix en cache, commitée, `make voice` fait | `take`, `duration_s`, `cache_key`, `aligned` |
| `storyboard` | storyboard | `Vxx.json` et `.md` passent `--check`, test sans son fait, commit | `version` |
| `spec` | mise en scène | `scripts/story/Vxx/` couvre toutes les scènes (`make story-staging` OK) | — |
| `render` | rendu | `output/WTH-Vxx.mp4` et la version sans sous-titres, rendus des sources actuelles | — |
| `review` | revues | aucun problème bloquant ni majeur (`done`), ou tous corrigés (`fixed`) | — |
| `mute_verify` | contrôle sans son | ≥ 85 % des idées-clés GOT, aucune idée principale MISSED, « oui » au critère | `got` (« 8/9 »), `critere` |
| `qa` | QA | `output/qa/Vxx.json` OK en mode story | — |
| `delivered` | livrée | MP4 envoyé à l'utilisateur avec légende et hashtags | — |
| `published` | publiée | Cloudinary + programmée sur les 3 réseaux dans Metricool | `scheduled_at`, `metricool` |

`spec`, `render`, `review`, `mute_verify` et `qa` sont les clés de l'objet `status` que renvoie
`build-review.wf.js` : il se reporte tel quel avec `status.py merge`.

## Les états

| État | Sens | Laisse passer à l'étape suivante ? |
|---|---|---|
| `pending` | pas commencée | non |
| `in_progress` | en cours, ou en attente d'une décision (voir `pending`) | non |
| `partial` | faite en partie (V01 : mise en scène de S10-S14 seulement) | non |
| `done` | terminée | oui |
| `fixed` | des problèmes ont été trouvés, puis corrigés | oui |
| `open` | des problèmes majeurs restent après 2 tours : consignés dans `open_issues` et signalés à l'utilisateur ; on continue sans boucler | oui |
| `fail` | a échoué : lire `note` et `open_issues` | non |
| `blocked` | attend l'utilisateur (crédits, durée, décision) | non |
| `skipped` | volontairement sautée | oui |

Champs libres d'une étape :
- `note` : ce qui s'est passé ;
- `pending` : ce qui **reste à faire**, même sur une étape `done`. Exemple : V01, storyboard v2 fait, v3 à faire.
  `status.py next` s'arrête sur une étape qui a un `pending`. `set … done` sans `--pending` l'efface.

Une vidéo porte aussi `open_issues` (problèmes encore ouverts), `notes` (historique libre) et `max_duration_s`
(durée maximale approuvée par l'utilisateur, en miroir de `config.yaml` `qa.max_duration_by_video`).

Dans un `merge`, `open_issues` **remplace** la liste : c'est ce que donne un film refait ou revu en entier.
`open_issues_add` l'**allonge** sans doublon : c'est ce que donne une vérification seule (`build-review.wf.js` avec
`from: "verify"`), qui ne doit pas effacer les problèmes laissés ouverts par la revue. `status.py issues Vxx --clear`
vide la liste quand ils sont réglés.

`blocked` contre `in_progress` : une étape qui attend une réponse de l'utilisateur (crédits, choix de durée) est
`blocked`, avec la question dans `pending`. Une session neuve sait alors qu'il n'y a rien à lancer avant sa réponse.
Dès qu'il a répondu, repasse-la à `in_progress` (`--pending ""` efface la question).

Le suivi peut prendre du retard sur les fichiers (une voix commitée sans `status.py set`). `status.py next` et
`preflight.py` le signalent pour la voix (« voix DÉJÀ en cache », « ! suivi de la voix ») : enregistre-la, ne la
régénère pas.

## Les points de validation

| Nom | Passe à `done` quand |
|---|---|
| `v01_full_approved` | l'utilisateur a validé V01 complète, avec et sans sous-titres. Avant, aucune vidéo V02 à V15 ne passe au storyboard (`batch.wf.js` refuse, `status.py next` l'affiche). |
| `publication_dates_approved` | l'utilisateur a validé le tableau des dates. Avant, rien n'est programmé dans Metricool. |
| `elevenlabs_credits` | l'utilisateur a confirmé que son solde couvre le lot de voix suivant. Repasse à `pending` après chaque lot. |
| `publication_questions` | licence Remotion et déclaration « contenu IA » tranchées. |

## Commandes

```bash
ST=".claude/skills/wth-video/scripts/status.py"      # depuis la racine du dépôt
python3 $ST init                                      # crée le fichier, ajoute les vidéos de scripts.json qui manquent
python3 $ST show [V07 …] [--details] [--json]         # tableau, puis détail (notes, reste à faire, problèmes)
python3 $ST next [V07 …] [--json]                     # prochaine étape de chaque vidéo et le moyen de la faire
python3 $ST set V07 storyboard done version='"v1"' --note "écrit par storyboard.wf.js"
python3 $ST set V07 voice blocked --note "aucune prise ≤ 59,4 s" --pending "choix de l'utilisateur"
python3 $ST merge V07 - <<'EOF'
{"spec": "done", "render": "done", "review": "fixed", "qa": "done",
 "mute_verify": {"state": "done", "got": "8/9", "critere": "oui"}, "open_issues": []}
EOF
python3 $ST merge V07 - <<'EOF'
{"qa": "done", "open_issues_add": ["QA : …"]}
EOF
python3 $ST checkpoint v01_full_approved done --note "accord de l'utilisateur le 22/10"
python3 $ST issues V07 --clear
```

- Les valeurs `clé=valeur` sont lues en JSON quand c'est possible : `duration_s=57.7` est un nombre. Pour une
  chaîne qui ressemble à un nombre ou qui contient des espaces, entoure-la de guillemets JSON : `version='"v2 · retouche"'`.
- Un état ou une étape inconnus sont refusés (code 1). Le fichier n'est réécrit que s'il reste valide.
- Après chaque changement d'étape, commite `production_status.json` avec les sources de cette étape.
