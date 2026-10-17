import { Gauge, LogOut, MessageSquareText, ShieldCheck, Sparkles, UserRound } from "lucide-react";
import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { cn } from "@/lib/cn";
import { formatRelative } from "@/lib/format";
import { PageHeader } from "@/components/ui/misc";
import { agentMode } from "@/server/agents";
import { CLAUDE_MODEL } from "@/server/agents/claude/client";
import { requireContext } from "@/server/auth/context";
import { listTokens } from "@/server/services/tokens";
import { publicBaseUrl } from "@/server/url";
import { logoutAction } from "@/app/(auth)/actions";
import { revokeTokenAction } from "./actions";
import { CreateTokenForm } from "./mcp-access";
import { WorkspaceForm } from "./workspace-form";

export const metadata: Metadata = { title: "Réglages" };

/** One of the three jobs; the AI tint only when Claude really does it. */
function Role({ icon, title, claude, children }: { icon: ReactNode; title: string; claude: boolean; children: ReactNode }) {
  return (
    <li className="flex gap-3">
      <span className={cn("flex size-8 shrink-0 items-center justify-center rounded-full", claude ? "bg-ai-soft text-ai" : "bg-canvas text-ink-2")} aria-hidden>
        {icon}
      </span>
      <div className="min-w-0">
        <p className="font-medium text-ink">{title}</p>
        <p className="text-ink-2">{children}</p>
      </div>
    </li>
  );
}

function Guardrail({ children }: { children: ReactNode }) {
  return (
    <li className="flex gap-2">
      <ShieldCheck className="mt-0.5 size-4 shrink-0 text-success" aria-hidden />
      <span>{children}</span>
    </li>
  );
}

export default async function SettingsPage() {
  const { workspace, user } = await requireContext();
  const [tokens, endpoint] = await Promise.all([listTokens(workspace.id), publicBaseUrl().then((base) => `${base}/api/mcp`)]);
  const claude = agentMode() === "claude";
  // AGENTS=rules can switch Claude off even with a key: say so instead of asking for a key.
  const keyConfigured = Boolean(process.env.ANTHROPIC_API_KEY);

  return (
    <>
      <PageHeader title="Réglages" description="Votre offre, votre lien de réservation, l'intelligence artificielle et l'accès depuis vos assistants." />
      <div className="grid items-start gap-6 xl:grid-cols-[minmax(0,3fr)_minmax(0,2fr)]">
        <Card>
          <CardHeader title="Espace de travail" />
          <CardBody>
            <WorkspaceForm workspace={workspace} />
          </CardBody>
        </Card>

        <div className="min-w-0 space-y-6">
          <Card>
            <CardHeader
              title="Intelligence artificielle"
              actions={
                <Badge tone={claude ? "ai" : "neutral"}>
                  {claude ? <Sparkles className="size-3" aria-hidden /> : null}
                  {claude ? "Claude actif" : keyConfigured ? "Claude désactivé" : "Claude non configuré"}
                </Badge>
              }
            />
            <CardBody className="space-y-4 text-sm">
              {claude ? (
                <p className="text-ink-2">
                  Claude travaille sur vos prospects à partir de votre offre et de votre client idéal. <span className="text-muted">Modèle : {CLAUDE_MODEL}</span>
                </p>
              ) : keyConfigured ? (
                <p className="text-ink-2">
                  Claude est désactivé par le réglage AGENTS=rules du fichier .env. Vela note les profils avec des critères fixes, envoie vos messages tels quels et répond avec des
                  réponses types. Pour activer Claude, retirez ce réglage, puis relancez Vela.
                </p>
              ) : (
                <p className="text-ink-2">
                  Claude n&apos;est pas configuré. Vela note les profils avec des critères fixes, envoie vos messages tels quels et répond avec des réponses types. Pour activer
                  Claude, ajoutez votre clé <code className="rounded bg-canvas px-1 text-ink">ANTHROPIC_API_KEY</code> dans le fichier .env, puis relancez Vela.
                </p>
              )}
              <ul className="space-y-3">
                <Role icon={<Gauge className="size-4" />} title="Notation" claude={claude}>
                  {claude
                    ? "Claude note chaque profil sur 100 au regard de votre offre et de votre client idéal, et explique sa note."
                    : "Chaque profil reçoit une note sur 100 selon le poste, le secteur, la zone et la taille d'entreprise visés."}
                </Role>
                <Role icon={<MessageSquareText className="size-4" />} title="Rédaction" claude={claude}>
                  {claude
                    ? "Claude adapte vos messages à chaque profil dans les campagnes qui l'activent, sans inventer de faits."
                    : "Vos messages partent tels que vous les écrivez, avec leurs variables et leurs variantes."}
                </Role>
                <Role icon={<UserRound className="size-4" />} title="Setter" claude={claude}>
                  {claude
                    ? "Claude lit la conversation, répond aux prospects, propose votre lien de réservation et vous passe la main sur les cas sensibles."
                    : "Il reconnaît l'intention de la réponse, envoie une réponse type adaptée et vous passe la main sur tout le reste."}
                </Role>
              </ul>
              <div>
                <h3 className="text-xs font-semibold uppercase tracking-wide text-muted">Garde-fous</h3>
                <ul className="mt-2 space-y-1.5 text-ink-2">
                  <Guardrail>Les exclusions, les demandes RGPD ou d&apos;arrêt et les prospects déjà en rendez-vous restent gérés par des règles fixes.</Guardrail>
                  <Guardrail>Une réponse contenant un autre lien que votre lien de réservation n&apos;est jamais envoyée.</Guardrail>
                  {claude ? <Guardrail>Si Claude ne répond pas ou refuse, les règles prennent le relais.</Guardrail> : null}
                </ul>
              </div>
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Accès MCP" description="Pilotez Vela depuis Claude Code, Cursor ou tout autre assistant compatible MCP." />
            <CardBody className="space-y-4 text-sm">
              <p className="text-ink-2">
                Adresse : <code className="break-all rounded bg-canvas px-1 text-ink">{endpoint}</code>. Chaque jeton donne accès à cet espace : vue d&apos;ensemble,
                conversations, réponses proposées, prospects, campagnes et rendez-vous. Votre assistant vous demandera confirmation avant d&apos;envoyer un message.
              </p>
              <CreateTokenForm endpoint={endpoint} />
              {tokens.length > 0 ? (
                <ul className="divide-y divide-line rounded-control border border-line">
                  {tokens.map((t) => (
                    <li key={t.id} className="flex items-center justify-between gap-3 px-3 py-2.5">
                      <span className="min-w-0">
                        <span className="block truncate font-medium text-ink">{t.name}</span>
                        <span className="block text-xs text-muted">
                          <code>{t.prefix}…</code> · créé {formatRelative(t.createdAt)} · {t.lastUsedAt ? `utilisé ${formatRelative(t.lastUsedAt)}` : "jamais utilisé"}
                        </span>
                      </span>
                      <form action={revokeTokenAction.bind(null, t.id)}>
                        <Button type="submit" variant="danger" size="sm">
                          Révoquer
                        </Button>
                      </form>
                    </li>
                  ))}
                </ul>
              ) : null}
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Profil" />
            <CardBody className="flex flex-wrap items-center justify-between gap-3 text-sm">
              <div className="min-w-0">
                <p className="truncate font-medium text-ink">{user.name}</p>
                <p className="truncate text-muted">{user.email}</p>
              </div>
              <form action={logoutAction}>
                <Button type="submit" variant="secondary" size="sm">
                  <LogOut className="size-3.5" aria-hidden /> Se déconnecter
                </Button>
              </form>
            </CardBody>
          </Card>
        </div>
      </div>
    </>
  );
}
