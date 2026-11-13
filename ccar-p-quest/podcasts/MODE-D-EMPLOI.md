# Podcasts « La Tour de l'Architecte » : mode d'emploi

Dix scripts de podcast pour préparer la certification Claude Certified Architect – Professional. Chaque épisode dure environ 5 minutes et raconte deux histoires : une situation en entreprise, des pistes sur la table, une pause pour réfléchir, puis la décision de Nora, l'architecte, et la raison pour laquelle les autres pistes échouent.

Les scripts sont écrits à deux voix (`NARRATEUR` et `NORA`), en français, avec les termes techniques en anglais comme à l'examen.

## Les dix épisodes

Chaque épisode suit un étage du jeu. La première histoire reprend une question du jeu, la seconde est une situation inédite sur une autre notion du même étage.

| Épisode | Fichier | Histoire reprise du jeu | Histoire inédite |
|---|---|---|---|
| 1 | `episode-01-la-forge-des-prompts.txt` | L'assistant téléphonique et sa liste d'interdits | La mutuelle et le plafond inventé (hallucinations) |
| 2 | `episode-02-le-bureau-d-etudes.txt` | Deux équipes veulent du multi-agents | Les notes de frais : workflow ou agent |
| 3 | `episode-03-l-atelier-des-outils.txt` | Le JSON presque toujours valide | L'agent de réservation qui choisit le mauvais outil |
| 4 | `episode-04-le-reseau-des-connecteurs.txt` | Cent quarante outils MCP | La conformité veut des sources vérifiables |
| 5 | `episode-05-le-banc-d-essai.txt` | 98 % en test, des erreurs en production | Le juge LLM instable |
| 6 | `episode-06-la-salle-des-machines.txt` | Le cache qui ne sert jamais | Les archives de presse à traiter chaque nuit |
| 7 | `episode-07-la-citadelle-des-garde-fous.txt` | L'e-mail qui donne des ordres | La grille de remises dans le prompt |
| 8 | `episode-08-le-conseil-des-parties-prenantes.txt` | Le SLA à 99,9 % | Les courriers qui changent tout seuls |
| 9 | `episode-09-le-poste-de-controle.txt` | La consigne en gras ignorée | Le traitement de nuit qui varie selon la machine |
| 10 | `episode-10-le-sommet.txt` | Deux dirigeants, deux demandes opposées | Le cabinet d'avocats et sa muraille de Chine |

## Avec NotebookLM

NotebookLM ne lit pas un texte mot pour mot : ses deux voix le racontent à leur façon. La consigne ci-dessous lui demande de coller au script, sans garantie qu'il le fasse complètement.

1. Crée un notebook par épisode et ajoute le fichier de l'épisode comme **seule** source. Avec plusieurs sources, les voix mélangent les épisodes.
2. Dans les paramètres, choisis le français comme langue de sortie.
3. Ouvre le résumé audio, puis « Personnaliser ». Garde le format à deux voix. Si le choix de la longueur est proposé, prends la plus courte.
4. Colle la consigne dans le champ d'instructions, puis lance la génération.

Consigne à coller (elle tient en moins de 500 caractères, au cas où le champ serait limité) :

```
Ce document est le script d'un podcast à deux voix. Jouez-le tel quel, en français, sans le résumer ni le commenter. Une voix est le narrateur, l'autre est Nora, qui parle à la première personne. Gardez l'ordre, les chiffres, les termes anglais et les phrases « À retenir ». N'ajoutez aucune information absente du script. Ne dites pas que vous lisez un document. Court silence après chaque question à l'auditeur. Durée : 5 minutes.
```

Les noms des boutons peuvent différer selon la version de l'application.

## Si NotebookLM s'écarte trop du script : Google AI Studio

La synthèse vocale de Google AI Studio lit le texte tel quel, avec deux voix au maximum.

1. Ouvre la génération de parole (text-to-speech) et choisis le mode à deux voix.
2. Nomme les deux voix exactement `NARRATEUR` et `NORA` : les noms réglés dans l'outil doivent correspondre à ceux du script.
3. Colle le script de l'épisode.
4. Consigne de style possible : « Lis ce script en français, sur un ton de podcast narratif, posé et chaleureux. Marque une courte pause après chaque question posée à l'auditeur. »

## À savoir

- Les scripts n'ont été testés ni dans NotebookLM ni dans AI Studio. Écoute le premier épisode avec le script sous les yeux et vérifie que les chiffres et les termes techniques sont restés exacts avant de générer les neuf autres.
- La durée de 5 minutes vaut pour une lecture mot pour mot (750 à 780 mots par épisode). Avec NotebookLM, c'est lui qui choisit la durée.
- Chaque épisode contient deux histoires. Trois ne tiennent pas en 5 minutes avec la pause et l'explication des mauvaises pistes.
- Les entreprises et les personnages sont fictifs. Les notions viennent du contenu du jeu, lui-même rédigé à partir de la documentation officielle d'Anthropic. Ce ne sont pas des questions officielles de l'examen.
