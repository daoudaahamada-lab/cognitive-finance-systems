# Guide de rédaction du contenu

Ce guide fixe le format et le style de chaque niveau du jeu. Il sert à écrire les 100 premières questions et à en ajouter d'autres plus tard.

## L'examen visé

**Claude Certified Architect – Professional (CCAR-P)** : 63 questions, 120 minutes, QCM à réponse unique ou multiple, questions indépendantes (pas de scénario partagé), score de réussite 720/1000.

Le guide d'examen officiel est distribué via l'Anthropic Partner Academy. La répartition par domaine ci-dessous provient de plusieurs reproductions publiques concordantes. **Le contenu technique, lui, doit toujours être vérifié dans la documentation officielle** :

- https://platform.claude.com/docs/en/... (API, outils, évaluations, garde-fous, administration). Ajouter `.md` à l'URL pour lire la page en Markdown. L'index complet est à https://platform.claude.com/llms.txt
- https://code.claude.com/docs/en/... (Claude Code). L'index est à https://code.claude.com/docs/llms.txt
- https://www.anthropic.com/engineering/... (articles d'ingénierie, par ex. *Building effective agents*)

| Code | Domaine | Poids | Questions sur 100 |
|---|---|---|---|
| D1 | Solution Design & Architecture | 17 % | 17 |
| D2 | Claude Models, Prompting & Context Engineering | 13 % | 13 |
| D3 | Integration | 19 % | 19 |
| D4 | Evaluation, Testing & Optimization | 16 % | 16 |
| D5 | Governance, Safety & Risk Management | 14 % | 14 |
| D6 | Stakeholder Communication & Lifecycle Management | 14 % | 14 |
| D7 | Developer Productivity & Operational Enablement | 7 % | 7 |

## Plan des 10 niveaux

| Niveau | Thème | Boss (anti-pattern à vaincre) | Répartition des 10 questions du boss |
|---|---|---|---|
| 1 | Modèles, prompting et contexte | L'Ambigu (l'instruction floue) | D2 ×9, D1 ×1 |
| 2 | Conception de solution | Le Sur-Ingénieur | D1 ×10 |
| 3 | Intégration I : API, tool use, sorties structurées, agents | Le Schéma Brisé | D3 ×10 |
| 4 | Intégration II : MCP, RAG, données d'entreprise, clouds | L'Hydre des Connecteurs | D3 ×7, D2 ×3 |
| 5 | Évaluation et tests | Le Vibe-Checker | D4 ×10 |
| 6 | Optimisation : coût, latence, passage à l'échelle | Le Gouffre à Tokens | D4 ×5, D1 ×4, D6 ×1 |
| 7 | Gouvernance, sécurité et risques | L'Injecteur | D5 ×10 |
| 8 | Parties prenantes et cycle de vie | La Promesse à 99,9 % | D6 ×10 |
| 9 | Productivité des développeurs et opérations | Le Chaos Ops | D7 ×6, D6 ×2, D5 ×2 |
| 10 | Simulation finale, tous domaines | L'Examinateur | D1 ×2, D2 ×1, D3 ×2, D4 ×1, D5 ×2, D6 ×1, D7 ×1 |

## Format d'un fichier de niveau (`content/level-XX.json`)

```json
{
  "id": 1,
  "title": "La Forge des Prompts",
  "theme": "Modèles, prompting et contexte",
  "intro": "2 à 3 phrases en français : ce que couvre le niveau et pourquoi c'est important à l'examen.",
  "boss": {
    "name": "L'Ambigu",
    "epithet": "Seigneur des instructions floues",
    "taunt": "Phrase d'entrée du boss, en français, une ligne.",
    "defeat": "Phrase quand le boss est vaincu, en français, une ligne.",
    "victory": "Phrase quand le joueur perd, en français, une ligne."
  },
  "cards": [
    {
      "term": "Terme en anglais tel qu'il apparaît à l'examen",
      "fr": "Explication en français, 2 à 4 phrases, concrète.",
      "trap": "Le piège classique à l'examen sur ce sujet, en français, 1 à 2 phrases.",
      "source": { "title": "Titre de la page officielle", "url": "https://platform.claude.com/docs/en/..." }
    }
  ],
  "warmup": [
    {
      "statement": "An English true/false statement about a concept from the cards.",
      "answer": true,
      "fr": "Explication en français, 1 à 3 phrases."
    }
  ],
  "questions": [
    {
      "id": "L01-Q01",
      "domain": "D2",
      "type": "single",
      "stem": "English scenario, 50 to 130 words, ending with the precise ask.",
      "options": [
        { "text": "English option", "why": "En français : pourquoi c'est juste ou faux." },
        { "text": "...", "why": "..." },
        { "text": "...", "why": "..." },
        { "text": "...", "why": "..." }
      ],
      "answer": [2],
      "explanation": "En français, 2 à 4 phrases : le principe qui fait gagner la question.",
      "tip": "Réflexe examen en une phrase, en français.",
      "source": { "title": "Titre de la page officielle", "url": "https://platform.claude.com/docs/en/..." }
    }
  ]
}
```

Règles de structure (vérifiées par `node scripts/validate.mjs`) :

- `cards` : exactement 6 fiches. `warmup` : exactement 5 affirmations vrai/faux, avec au moins 2 vraies et 2 fausses.
- `questions` : exactement 10, avec la répartition par domaine du plan ci-dessus.
- `type: "single"` : 4 options, `answer` contient 1 index. `type: "multi"` : 5 options, `answer` contient exactement 2 index, et la question finit par « (Select TWO.) ». Prévoir 2 questions `multi` par niveau.
- Les index de `answer` commencent à 0. Le jeu mélange l'ordre des options à l'affichage. Varier quand même la position de la bonne réponse dans le fichier.
- `id` : `LXX-QYY`, unique.
- Chaque `source.url` pointe vers une page officielle qui existe (vérifiée avec `curl`).
- Les guillemets doubles à l'intérieur d'un texte s'écrivent « » en français et ‘ ’ ou \" en anglais.

## Style des questions (le plus important)

Les questions doivent ressembler à celles d'un examen professionnel d'architecte :

1. **Un scénario d'entreprise concret** : un secteur (banque, assurance, santé, distribution, industrie, secteur public…), une contrainte chiffrée (volumes, latence, budget, SLA, réglementation), un problème observé. Pas de question de définition pure.
2. **Une demande précise** à la fin : *Which approach BEST…*, *What should the architect do FIRST?*, *Which design MOST effectively…*, *What is the MOST likely cause…*, *Which TWO actions… (Select TWO.)*
3. **Quatre options plausibles** de longueur et de ton similaires. Les mauvaises réponses reprennent les erreurs réelles des équipes :
   - consigne dans le prompt alors qu'il faut un contrôle déterministe (code, hook, permission, validation de schéma) ;
   - fine-tuning ou modèle plus gros alors que le vrai problème est le contexte, la récupération ou l'évaluation ;
   - système multi-agents là où un workflow simple suffit ;
   - optimisation avant d'avoir mesuré ;
   - promesse aux parties prenantes non soutenue par les évaluations ;
   - accès trop larges, secrets dans les prompts, absence d'humain dans la boucle pour les décisions à fort impact.
4. **Pas d'indice gratuit** : éviter « always/never » dans les seules mauvaises réponses. La longueur ne doit pas trahir la réponse : la bonne option fait au plus 1,3 fois la longueur moyenne des mauvaises (et au moins 0,75 fois), et elle n'est l'option la plus longue que dans 4 questions sur 10 au maximum. Le validateur le vérifie. Pour y arriver, donner aux mauvaises réponses des détails concrets et une justification plausible (« …because… », « …so that… »), et écrire la bonne réponse de façon dense.
5. **Indépendant des versions** : ne pas faire dépendre la réponse d'un numéro de modèle, d'un prix exact ou d'une limite susceptible de changer. Parler de « the most capable model », « a smaller, faster model such as Haiku ». Les mécanismes stables (prompt caching, Message Batches API, structured outputs, tool use, MCP, extended/adaptive thinking, citations, Files API, hooks, CLAUDE.md, subagents, skills, permissions, ZDR, etc.) peuvent être cités par leur nom.
6. **Vérifier chaque fait technique** dans la doc officielle avant de l'écrire. En cas de doute, reformuler pour que la réponse repose sur un principe d'architecture solide plutôt que sur un détail de produit.
7. **Contenu original** : ne pas recopier de questions de sites de préparation tiers.

## Explications en français

- `why` de chaque option : pourquoi elle est juste, ou l'erreur précise qu'elle commet.
- `explanation` : le principe général à retenir.
- `tip` : un réflexe court pour reconnaître ce type de question le jour J.
- Garder les termes techniques en anglais quand c'est ainsi qu'ils apparaissent à l'examen (prompt caching, tool use, eval set, guardrails…).
