# Vela : setter IA pour la prospection LinkedIn

> **Vela** est un nom de code provisoire. Pour renommer le produit, modifiez `src/lib/brand.ts`.

Un SaaS de prospection B2B sur LinkedIn, inspiré des fonctionnalités publiques de [mimikflow.com](https://mimikflow.com).
Le moteur trouve les prospects, les note, les invite, lance la conversation, relance, puis laisse le **setter** répondre et réserver le rendez-vous. Vous gardez la main sur les cas sensibles.

C'est une **réimplémentation indépendante** (« clean room ») : aucun code, texte, logo ou nom de MimikFlow n'est repris, seulement des fonctionnalités décrites publiquement.

## Ce que contient cette itération

| Domaine | Ce qui marche |
| --- | --- |
| **Compte** | Instance personnelle : le premier compte créé en devient propriétaire, puis les inscriptions se ferment (`ALLOW_SIGNUP=true` pour les rouvrir). Toutes les fonctionnalités sont disponibles, sans facturation |
| **Comptes LinkedIn** | Votre vrai compte, piloté dans un navigateur automatisé (cookie `li_at` ou connexion manuelle), ou le simulateur pour tester. Type de compte, horaires et jours d'envoi, fuseau horaire, plafonds personnalisables (uniquement à la baisse) |
| **Campagnes** | Sources (recherche ou URL de recherche LinkedIn, signaux d'achat, engagement sur des posts, visiteurs de profil, import), ciblage (postes, secteurs, zones, tailles, mots-clés), exclusions, score minimum, séquence (note d'invitation, premier message, jusqu'à 8 relances), variables `{{firstName}}` et variantes `{Bonjour\|Hello}` avec aperçu en direct |
| **Moteur** | Sourcing, scoring expliqué point par point, invitations, premier message après acceptation, relances arrêtées dès la première réponse, reprise après un « absent » |
| **Setter** | Trois modes : automatique, validation, désactivé. Il classe l'intention (intéressé, question, objection, refus, absent, sensible), répond ou rédige un brouillon, envoie le lien de réservation, et passe la main sur les cas sensibles (RGPD, tarifs, réponse non reconnue, trop d'échanges) |
| **Agents IA (Claude)** | Scoring par rapport à l'offre et au client idéal, personnalisation de chaque message, setter qui lit la conversation et répond. Garde-fous déterministes et repli automatique sur les règles (voir plus bas) |
| **Boîte de réception** | Onglets À traiter / Brouillons / IA / Toutes. Validation ou modification des brouillons, réponse manuelle, prise de main, retour au setter |
| **Prospects** | Liste filtrable, vue pipeline (Kanban), fiche avec score détaillé, historique, notes, mise en veille, exclusion, RDV manuel |
| **Rendez-vous** | À venir et passés, statut (effectué, absent, annulé) |
| **Tableau de bord** | Indicateurs clés, entonnoir, activité quotidienne, quotas par compte, liste de démarrage |
| **Serveur MCP** | `/api/mcp` (Streamable HTTP), 25 outils pour piloter Vela depuis Claude Code, Cursor ou tout client MCP, avec des jetons personnels créés dans les réglages |
| **Site vitrine** | Accueil (`/`), mentions légales, confidentialité, CGU, sitemap et robots.txt |

**Pas encore inclus** : recherches Sales Navigator, signaux d'achat sur un vrai compte (simulateur uniquement), synchronisation d'agenda (un rendez-vous pris via le lien de réservation se saisit sur la fiche du prospect).

## Sécurité des comptes LinkedIn

LinkedIn ne publie pas de limites officielles. Le moteur applique les seuils observés couramment, sur des **fenêtres glissantes en temps réel** :

| Type de compte | Invitations / 7 jours | Invitations / 24 h | Messages / 24 h |
| --- | --- | --- | --- |
| Gratuit | 100 | 40 | 100 |
| Premium, Sales Navigator, Recruiter | 200 | 40 | 100 |

D'autres règles s'ajoutent :
- Aucune action n'est envoyée hors des horaires du compte.
- Chaque passage du moteur envoie au plus 3 invitations et 5 messages par compte.
- Sur un vrai compte, invitations et messages de séquence partent un par un, étalés sur la plage horaire. Avec 40 invitations par jour de 9 h à 18 h, cela fait une invitation toutes les 13 minutes environ ; un plafond abaissé espace encore plus les envois. Les réponses du setter, elles, ne sont pas retardées.
- Une personne déjà connue de l'espace n'est jamais recontactée depuis une autre campagne.
- Un verrou par compte empêche les doubles envois quand deux passages du moteur se chevauchent.

Sur un vrai compte, le navigateur ajoute des pauses humaines entre chaque action. Si LinkedIn affiche l'avertissement de limite d'invitations, les invitations du compte s'arrêtent 24 h. Si la session expire ou si LinkedIn demande une vérification, le compte se met en pause avec la raison affichée.

> ⚠️ Les conditions d'utilisation de LinkedIn interdisent les outils d'automatisation tiers. Même avec ces limites, un compte peut être restreint. Le simulateur, lui, ne contacte personne.

## Démarrage

### Sur votre ordinateur, en deux commandes

Prérequis : [Node.js](https://nodejs.org) 22 ou plus récent, et [Docker Desktop](https://www.docker.com/products/docker-desktop/) ouvert (ou un PostgreSQL déjà installé). Dans un terminal ouvert dans le dossier `prospecting` :

```bash
npm run setup     # une seule fois : dépendances, réglages (.env), base de données, navigateur pour LinkedIn
npm run local     # à chaque utilisation : base, app et worker ensemble ; Ctrl+C arrête tout
```

Ouvrez ensuite http://localhost:3000/signup pour créer votre compte : le premier compte créé devient propriétaire de l'instance.

### Démo et développement

Prérequis : Node.js 22 ou plus récent, et PostgreSQL 16 (ou Docker).

```bash
cd prospecting
npm install
docker compose up -d          # Postgres sur localhost:5432 (vela / vela)
cp .env.example .env
npm run db:migrate            # applique les migrations
npm run db:seed               # données de démo (environ 30 s)
npx playwright-core install chromium   # seulement pour piloter votre vrai compte LinkedIn
npm run dev                   # site : http://localhost:3000, app : /login
npm run worker                # dans un 2e terminal : le moteur tourne toutes les 10 s
```

Connectez-vous avec **demo@vela.local / demo1234**.

Pour utiliser votre vrai compte LinkedIn, sautez `npm run db:seed` (ou utilisez `npm run setup`) et créez votre compte sur `/signup` : le premier compte créé devient propriétaire de l'instance.

Le script de démo rejoue le vrai moteur et le simulateur sur trois semaines passées. Tous les chiffres affichés sont donc cohérents. Le compte de démo envoie 24 h/24, 7 j/7 pour que le worker ait toujours du travail.

Avec `TIME_SCALE=720` (la valeur de `.env.example`), une journée d'attente dure 2 minutes : délais de relance, réactions simulées des prospects. Cette accélération ne s'applique qu'aux comptes simulés : **un vrai compte LinkedIn attend toujours en temps réel, et les quotas restent en temps réel pour tous.** Le bouton **Synchroniser maintenant**, en haut de l'app, exécute un passage immédiatement.

### Site vitrine

Les pages publiques vivent dans `src/app/(marketing)/` et sont générées en statique.
- **Pages légales** : ce sont des modèles. Les champs entre crochets (raison sociale, SIREN, hébergeur, durées de conservation…) sont à compléter et à faire relire avant la mise en ligne.
- **URL publique** : définissez `SITE_URL` pour que le sitemap et le robots.txt l'utilisent.

### Variables d'environnement

| Variable | Rôle |
| --- | --- |
| `DATABASE_URL` | Connexion PostgreSQL |
| `TIME_SCALE` | Accélère les attentes des comptes simulés, pour les démos (`1` = temps réel). Sans effet sur un vrai compte |
| `WORKER_INTERVAL_SECONDS` | Fréquence du worker (10 s par défaut) |
| `ANTHROPIC_API_KEY` | Active les agents Claude (sans clé : agents à base de règles) |
| `AGENTS` | Force `claude` ou `rules` (par défaut : `claude` dès qu'une clé est définie) |
| `ANTHROPIC_MODEL` | Modèle des agents (`claude-opus-5-5` par défaut) |
| `ALLOW_SIGNUP` | `true` pour autoriser d'autres inscriptions après le premier compte |
| `SITE_URL` | URL publique du site (sitemap, robots.txt) |
| `ENGINE_TICK_SECRET` | Active `POST /api/engine/tick` (en-tête `Authorization: Bearer …`) pour un cron externe, à utiliser à la place du worker (simulateur uniquement : le navigateur vit dans le worker) |
| `LINKEDIN_PROFILES_DIR` | Dossier des profils Chromium, un par compte (`.linkedin-profiles` par défaut). Contient vos sessions : à garder privé |
| `LINKEDIN_HEADLESS` | `false` pour voir la fenêtre du navigateur |
| `LINKEDIN_CHROMIUM_PATH` | Chrome ou Chromium déjà installé, à la place de celui de Playwright |
| `LINKEDIN_PACE` | Multiplie les pauses humaines (`1` par défaut ; ne descendez pas en dessous sur un vrai compte) |
| `LINKEDIN_EVENTS_INTERVAL_MINUTES` | Écart minimum entre deux lectures des nouvelles connexions et des messages (15 min par défaut) |
| `LINKEDIN_BRIDGE_PORT`, `LINKEDIN_BRIDGE_SECRET` | Passerelle locale entre l'app et le worker (`4319` ; secret dérivé de `DATABASE_URL` par défaut) |

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
    linkedin/             contrat LinkedInProvider, simulateur, navigateur (Playwright), passerelle app ↔ worker
    domain/               quotas, horaires, modèles de messages, temps
    auth/                 mots de passe (scrypt), sessions (cookie httpOnly, jeton haché en base)
    mcp/                  serveur MCP (outils au-dessus des services)
worker/                   boucle qui exécute le moteur ; seul processus à ouvrir Chromium
scripts/                  linkedin:login (connexion manuelle), linkedin:check (diagnostic sans envoi)
prisma/                   schéma, migrations, données de démo
tests/                    tests unitaires + intégration (moteur sur 3 semaines simulées)
```

Un passage du moteur (`runTick`) traite chaque compte actif, sous verrou, en cinq étapes :
1. Il récupère les événements LinkedIn : acceptations, réponses, rendez-vous.
2. Il trouve de nouveaux prospects, dans la limite de l'objectif hebdomadaire et d'une file d'attente maximale.
3. Il note les nouveaux prospects.
4. Il envoie les invitations, par meilleur score d'abord.
5. Il envoie les premiers messages et les relances dus, et marque « sans réponse » les séquences terminées.

## Connecter votre compte LinkedIn

Le fournisseur « Mon compte LinkedIn » (`src/server/linkedin/browser/`) pilote votre propre session dans un Chromium automatisé, à un rythme humain. Il ne passe par aucune API ni aucun service tiers.

**Mise en place**
1. Installez Vela avec `npm run setup` : il télécharge aussi le navigateur (sinon : `npx playwright-core install chromium`).
2. Lancez Vela avec `npm run local`, ou démarrez le worker vous-même (`npm run worker`). C'est lui qui ouvre Chromium, avec un profil persistant par compte. L'app web lui transmet ses actions par une passerelle locale (`127.0.0.1:4319`).
3. Dans **Comptes LinkedIn**, choisissez **Mon compte LinkedIn**, puis l'une des deux options :
   - **Cookie `li_at`** : collez-le depuis votre navigateur (Outils de développement → Application → Cookies → linkedin.com ; l'aide est sur la page). Vela vérifie la session, puis lit votre nom et votre titre.
   - **Connexion manuelle** : laissez le cookie vide ; le compte est créé en pause. Arrêtez le worker, lancez `npm run linkedin:login -- --account <id>` sur une machine avec écran, connectez-vous (mot de passe, double authentification), puis relancez le worker.
4. **Avant d'activer une campagne**, cliquez sur **Vérifier la connexion LinkedIn** sur la fiche du compte. Ce diagnostic n'envoie rien : il vérifie la session, une recherche, les boutons d'un profil, vos relations et vos messages, puis signale chaque point en échec. En ligne de commande, worker arrêté : `npm run linkedin:check -- --account <id>` (sans `--account`, il liste les comptes).

Faites tourner Vela sur l'ordinateur et la connexion internet d'où vous utilisez LinkedIn d'habitude : une session qui apparaît soudain ailleurs déclenche souvent une vérification de sécurité.

**Premier test conseillé**
1. Sur le compte, baissez les plafonds à 5 invitations et 10 messages par jour, et vérifiez les jours et horaires d'envoi.
2. Mettez `LINKEDIN_HEADLESS=false` dans `.env` pour voir chaque action dans la fenêtre du navigateur.
3. Créez une campagne sans source (tout décoché), avec le setter en mode **Validation**. Sur la page de la campagne, importez 2 ou 3 URL de profils de personnes prévenues (collègues, amis), dont au moins une hors de votre réseau.
4. Lancez la campagne. Les invitations partent une par une, espacées ; pour un profil importé, Vela lit d'abord le profil afin que la note utilise le vrai prénom.
5. Demandez à une personne d'accepter. L'acceptation est repérée en 15 minutes environ, et le premier message part 4 heures plus tard, pendant vos horaires d'envoi.
6. Demandez-lui de répondre. Le brouillon du setter apparaît dans la boîte de réception : modifiez-le si besoin, puis validez-le.
7. Ensuite seulement, passez à une campagne de recherche, en gardant des plafonds bas la première semaine.

**Ce que fait le navigateur**

| Étape | Sur LinkedIn |
| --- | --- |
| Sourcing | Recherche de personnes : l'URL collée dans la campagne, ou une recherche construite à partir des postes et mots-clés. Il lit aussi les visiteurs de votre profil et les réactions à un post |
| Invitation | Ouvre le profil, clique sur Se connecter (ou Plus → Se connecter), ajoute la note et l'envoie. Il détecte une invitation déjà envoyée, une connexion existante ou une adresse e-mail exigée |
| Message | Ouvre la messagerie depuis le profil, tape le texte avec des pauses, l'envoie, puis vérifie que le champ s'est vidé |
| Événements | Lit vos nouvelles connexions et les conversations modifiées. Un message du prospect resté sans réponse de votre part devient une réponse à traiter |

**Limites**
- Les sélecteurs suivent l'interface de LinkedIn en français et en anglais. Ils ont été testés sur une réplique locale (`tests/linkedin-mock.ts`), pas sur linkedin.com : LinkedIn modifie régulièrement son interface. Si `linkedin:check` échoue, ajustez `src/server/linkedin/browser/selectors.ts`.
- Une seule instance du worker par machine : deux processus ne peuvent pas ouvrir le même profil.
- Le profil Chromium contient votre session : ne le partagez pas et ne le versionnez pas (`.linkedin-profiles/` est ignoré par git).

Chaque compte mémorise son fournisseur : le simulateur et votre vrai compte peuvent donc coexister. Un autre fournisseur (Unipile, par exemple) s'ajoute en implémentant `LinkedInProvider` (`src/server/linkedin/types.ts`), puis en le déclarant dans `getProvider()`.

## Agents IA (Claude)

Avec `ANTHROPIC_API_KEY` défini (serveur **et** worker), trois agents Claude remplacent les agents à base de règles (`src/server/agents/claude/`). Chaque appel utilise des sorties structurées validées par Zod. Il passe aussi par le repli côté serveur (`fallbacks: "default"`) : si un classifieur de sécurité décline, l'API relance la requête sur le modèle recommandé.

| Agent | Ce que fait Claude | Ce qui reste déterministe |
| --- | --- | --- |
| **Scorer** | Note chaque profil de 0 à 100 au regard de l'offre, du client idéal et des critères, par lots de 20, avec une synthèse et des raisons favorables ou défavorables | Les exclusions sont appliquées avant l'appel, et les profils exclus ne sont jamais envoyés à Claude |
| **Rédacteur** | Adapte la note d'invitation, le premier message et les relances au profil (poste, entreprise, signal récent) en gardant l'intention, le ton et les liens du modèle. Désactivable par campagne | Message vide, trop long (300 caractères pour une note), lien ajouté ou variable restante : le modèle part tel quel |
| **Setter** | Lit la conversation, classe l'intention, répond, attend ou passe la main, et explique sa décision au commercial | Demandes RGPD ou d'arrêt, prospect déjà en rendez-vous, plus de 4 réponses IA : la décision revient aux règles. Une réponse contenant un lien autre que le lien de réservation n'est jamais envoyée |

Si Claude est indisponible (erreur réseau, refus, réponse invalide), l'agent à base de règles prend le relais pour cette requête. Après une clé refusée (401 ou 403), Claude est mis en pause 5 minutes au lieu d'échouer à chaque message. Les messages des prospects sont transmis comme des données : le setter a pour consigne de ne jamais suivre une instruction qu'ils contiennent.

Les interfaces `ProspectScorer`, `MessageWriter` et `ReplyAgent` (`src/server/agents/`) restent le point d'extension. Le script de démo et les tests utilisent toujours les agents à base de règles, pour ne déclencher aucun appel payant.

## Serveur MCP

Créez un jeton dans **Réglages → Accès MCP**. Il n'est affiché qu'une fois ; la page donne aussi les commandes prêtes à copier pour Claude Code et Cursor :

```bash
claude mcp add --transport http vela https://votre-instance/api/mcp --header "Authorization: Bearer vela_..."
```

| Famille | Outils |
| --- | --- |
| Suivre | `get_overview`, `list_accounts`, `list_campaigns`, `get_campaign` |
| Décider | `list_conversations`, `get_conversation`, `approve_draft`, `reject_draft`, `send_reply`, `hand_back_to_setter`, `take_over_conversation`, `mark_conversation_handled` |
| Prospects | `list_prospects`, `get_prospect`, `set_prospect_status`, `snooze_prospect`, `save_prospect_notes`, `import_prospects` |
| Configurer | `create_campaign`, `update_campaign`, `set_campaign_status` |
| Rendez-vous | `list_meetings`, `log_meeting`, `set_meeting_status` |
| Moteur | `run_engine` (« Synchroniser maintenant ») |

Comment ça fonctionne :
- **Une instance par requête.** Le serveur est sans état : chaque requête crée une instance liée à l'espace du jeton, et tout passe par la même couche de services que l'interface (`src/server/mcp/server.ts`).
- **Limites intactes.** Les outils ne peuvent ni lire un autre espace, ni dépasser les quotas ou les horaires d'envoi.
- **Confirmation avant envoi.** Les outils qui envoient de vrais messages (`approve_draft`, `send_reply`, `hand_back_to_setter`) sont annotés comme tels, et les instructions du serveur demandent à l'assistant d'obtenir votre accord avant de les appeler.
- **Jetons.** Seule leur empreinte SHA-256 est stockée. Un jeton donne accès à tout l'espace : servez l'instance en HTTPS et révoquez les jetons inutilisés.

## Tests

```bash
createdb vela_test            # ou via Docker : docker compose exec postgres createdb -U vela vela_test
npm test                      # environ 1 min 30, sans appel à l'API Anthropic
npm run typecheck && npm run lint
```

Les tests du fournisseur navigateur lancent un vrai Chromium contre une réplique locale de LinkedIn (`tests/linkedin-mock.ts`). Ils sont ignorés si aucun Chromium n'est disponible : installez-le avec `npx playwright-core install chromium` ou indiquez-le via `LINKEDIN_CHROMIUM_PATH`.

La base de test doit s'appeler `*_test` (variable `TEST_DATABASE_URL`, `postgresql://vela:vela@localhost:5432/vela_test` par défaut). Les tests refusent de vider toute autre base.

Le test principal fait tourner le moteur heure par heure sur trois semaines simulées. Il vérifie que :
- les quotas ne sont jamais dépassés sur aucune fenêtre glissante ;
- seuls les prospects qualifiés sont invités ;
- chacun n'est invité qu'une fois ;
- les relances respectent les délais ;
- personne n'est relancé après un refus ;
- deux passages simultanés n'envoient rien en double.
