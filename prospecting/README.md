# Vela : setter IA pour la prospection LinkedIn

> **Vela** est un nom de code provisoire. Pour renommer le produit, modifiez `src/lib/brand.ts`.

Un SaaS de prospection B2B sur LinkedIn, inspiré des fonctionnalités publiques de [mimikflow.com](https://mimikflow.com).
Le moteur trouve les prospects, les note, les invite, lance la conversation, relance, puis laisse le **setter** répondre et réserver le rendez-vous. Vous gardez la main sur les cas sensibles.

C'est une **réimplémentation indépendante** (« clean room ») : aucun code, texte, logo ou nom de MimikFlow n'est repris, seulement des fonctionnalités décrites publiquement.

## Ce que contient cette itération

| Domaine | Ce qui marche |
| --- | --- |
| **Comptes** | Inscription, connexion, espace de travail, essai Pro de 14 jours, plans Starter / Pro / Agency avec leurs limites (la facturation n'est pas branchée) |
| **Comptes LinkedIn** | Connexion via le simulateur, type de compte, horaires et jours d'envoi, fuseau horaire, plafonds personnalisables (uniquement à la baisse) |
| **Campagnes** | Sources (recherche, signaux d'achat, engagement sur des posts, visiteurs de profil, import), ciblage (postes, secteurs, zones, tailles, mots-clés), exclusions, score minimum, séquence (note d'invitation, premier message, jusqu'à 8 relances), variables `{{firstName}}` et variantes `{Bonjour\|Hello}` avec aperçu en direct |
| **Moteur** | Sourcing, scoring expliqué point par point, invitations, premier message après acceptation, relances arrêtées dès la première réponse, reprise après un « absent » |
| **Setter** | Trois modes : automatique, validation, désactivé. Il classe l'intention (intéressé, question, objection, refus, absent, sensible), répond ou rédige un brouillon, envoie le lien de réservation, et passe la main sur les cas sensibles (RGPD, tarifs, réponse non reconnue, trop d'échanges) |
| **Boîte de réception** | Onglets À traiter / Brouillons / IA / Toutes. Validation ou modification des brouillons, réponse manuelle, prise de main, retour au setter |
| **Prospects** | Liste filtrable, vue pipeline (Kanban), fiche avec score détaillé, historique, notes, mise en veille, exclusion, RDV manuel |
| **Rendez-vous** | À venir et passés, statut (effectué, absent, annulé) |
| **Tableau de bord** | Indicateurs clés, entonnoir, activité quotidienne, quotas par compte, liste de démarrage |

**Pas encore inclus** (prochaines itérations) :
- agents LLM ;
- serveur MCP ;
- site vitrine et facturation Stripe ;
- fournisseur LinkedIn réel.

## Sécurité des comptes LinkedIn

LinkedIn ne publie pas de limites officielles. Le moteur applique les seuils observés couramment, sur des **fenêtres glissantes en temps réel** :

| Type de compte | Invitations / 7 jours | Invitations / 24 h | Messages / 24 h |
| --- | --- | --- | --- |
| Gratuit | 100 | 40 | 100 |
| Premium, Sales Navigator, Recruiter | 200 | 40 | 100 |

D'autres règles s'ajoutent :
- Aucune action n'est envoyée hors des horaires du compte.
- Chaque passage du moteur envoie au plus 3 invitations et 5 messages par compte.
- Une personne déjà connue de l'espace n'est jamais recontactée depuis une autre campagne.
- Un verrou par compte empêche les doubles envois quand deux passages du moteur se chevauchent.

> ⚠️ Les conditions d'utilisation de LinkedIn interdisent les outils d'automatisation tiers. Même avec ces limites, un compte peut être restreint. Le simulateur, lui, ne contacte personne.

## Démarrage

Prérequis : Node.js 22 ou plus récent, et PostgreSQL 16 (ou Docker).

```bash
cd prospecting
npm install
docker compose up -d          # Postgres sur localhost:5432 (vela / vela)
cp .env.example .env
npm run db:migrate            # applique les migrations
npm run db:seed               # données de démo (environ 30 s)
npm run dev                   # http://localhost:3000
npm run worker                # dans un 2e terminal : le moteur tourne toutes les 10 s
```

Connectez-vous avec **demo@vela.local / demo1234**.

Le script de démo rejoue le vrai moteur et le simulateur sur trois semaines passées. Tous les chiffres affichés sont donc cohérents. Le compte de démo envoie 24 h/24, 7 j/7 pour que le worker ait toujours du travail.

Avec `TIME_SCALE=720` (la valeur de `.env.example`), une journée d'attente dure 2 minutes : délais de relance, réactions simulées des prospects. **Les quotas, eux, restent en temps réel.** Le bouton **Lancer le moteur**, en haut de l'app, exécute un passage immédiatement.

### Variables d'environnement

| Variable | Rôle |
| --- | --- |
| `DATABASE_URL` | Connexion PostgreSQL |
| `LINKEDIN_PROVIDER` | `simulator` (le seul fourni pour l'instant) |
| `TIME_SCALE` | Accélère les attentes pour les démos (`1` = temps réel) |
| `WORKER_INTERVAL_SECONDS` | Fréquence du worker (10 s par défaut) |
| `ENGINE_TICK_SECRET` | Active `POST /api/engine/tick` (en-tête `Authorization: Bearer …`) pour un cron externe, à utiliser à la place du worker |

## Architecture

```
src/
  app/                    Next.js (App Router) : pages, server actions
    (auth)/               inscription, connexion
    (app)/                tableau de bord, boîte, campagnes, prospects, RDV, comptes, réglages
    api/engine/tick/      déclenchement du moteur par cron
  server/
    services/             logique métier appelée par l'UI (et demain par le serveur MCP)
    engine/               le moteur : events → sourcing → scoring → invitations → messages → setter
    agents/               scorer, rédacteur, setter : à base de règles, derrière des interfaces
    linkedin/             contrat LinkedInProvider + simulateur
    domain/               plans, quotas, horaires, modèles de messages, temps
    auth/                 mots de passe (scrypt), sessions (cookie httpOnly, jeton haché en base)
worker/                   boucle qui exécute le moteur
prisma/                   schéma, migrations, données de démo
tests/                    tests unitaires + intégration (moteur sur 3 semaines simulées)
```

Un passage du moteur (`runTick`) traite chaque compte actif, sous verrou, en cinq étapes :
1. Il récupère les événements LinkedIn : acceptations, réponses, rendez-vous.
2. Il trouve de nouveaux prospects, dans la limite de l'objectif hebdomadaire et d'une file d'attente maximale.
3. Il note les nouveaux prospects.
4. Il envoie les invitations, par meilleur score d'abord.
5. Il envoie les premiers messages et les relances dus, et marque « sans réponse » les séquences terminées.

### Brancher un vrai LinkedIn

1. Implémentez `LinkedInProvider` (`src/server/linkedin/types.ts`) : connexion du compte, recherche, recherche par URL, invitation, message et récupération des événements. Un fournisseur comme Unipile s'y prête bien : ses webhooks alimentent `fetchEvents`.
2. Déclarez-le dans `getProvider()` (`src/server/linkedin/index.ts`).
3. Choisissez-le via `LINKEDIN_PROVIDER`.

Chaque compte mémorise son fournisseur : le simulateur et un fournisseur réel peuvent donc coexister.

### Brancher les agents IA

Le scoring, la rédaction et le setter passent par trois interfaces : `ProspectScorer`, `MessageWriter` et `ReplyAgent` (`src/server/agents/`). Une version LLM remplace la version à base de règles dans `defaultAgents()`, sans toucher au moteur. Les tests d'intégration servent alors de filet de sécurité.

## Tests

```bash
createdb vela_test            # ou via Docker : docker compose exec postgres createdb -U vela vela_test
npm test                      # environ 1 min 30
npm run typecheck && npm run lint
```

La base de test doit s'appeler `*_test` (variable `TEST_DATABASE_URL`, `postgresql://vela:vela@localhost:5432/vela_test` par défaut). Les tests refusent de vider toute autre base.

Le test principal fait tourner le moteur heure par heure sur trois semaines simulées. Il vérifie que :
- les quotas ne sont jamais dépassés sur aucune fenêtre glissante ;
- seuls les prospects qualifiés sont invités ;
- chacun n'est invité qu'une fois ;
- les relances respectent les délais ;
- personne n'est relancé après un refus ;
- deux passages simultanés n'envoient rien en double.
