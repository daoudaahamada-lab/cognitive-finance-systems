import type { Metadata } from "next";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { formatRelative } from "@/lib/format";
import { PageHeader } from "@/components/ui/misc";
import { agentMode } from "@/server/agents";
import { CLAUDE_MODEL } from "@/server/agents/claude/client";
import { requireContext } from "@/server/auth/context";
import { listTokens } from "@/server/services/tokens";
import { publicBaseUrl } from "@/server/url";
import { revokeTokenAction } from "./actions";
import { CreateTokenForm } from "./mcp-access";
import { WorkspaceForm } from "./workspace-form";

export const metadata: Metadata = { title: "Réglages" };

export default async function SettingsPage() {
  const { workspace, user } = await requireContext();
  const [tokens, endpoint] = await Promise.all([listTokens(workspace.id), publicBaseUrl().then((base) => `${base}/api/mcp`)]);

  return (
    <>
      <PageHeader title="Réglages" description="Votre offre, votre lien de réservation et vos agents." />
      <div className="grid gap-6 xl:grid-cols-[minmax(0,3fr)_minmax(0,2fr)]">
        <Card>
          <CardHeader title="Espace de travail" />
          <CardBody>
            <WorkspaceForm workspace={workspace} />
          </CardBody>
        </Card>

        <div className="space-y-6">
          <Card>
            <CardHeader
              title="Agents IA"
              actions={<Badge tone={agentMode() === "claude" ? "indigo" : "gray"}>{agentMode() === "claude" ? "Claude actif" : "Règles"}</Badge>}
            />
            <CardBody className="space-y-3 text-sm">
              {agentMode() === "claude" ? (
                <p>
                  Modèle : <code className="rounded bg-canvas px-1">{CLAUDE_MODEL}</code>. Claude note les prospects par rapport à votre offre et votre client idéal, personnalise
                  les messages des campagnes qui l&apos;activent et répond aux prospects selon le mode du setter.
                </p>
              ) : (
                <p>
                  Les agents à base de règles sont actifs : scoring par critères, modèles de messages, réponses types. Pour activer Claude, définissez{" "}
                  <code className="rounded bg-canvas px-1">ANTHROPIC_API_KEY</code> dans l&apos;environnement du serveur et du worker.
                </p>
              )}
              <ul className="space-y-1 text-muted">
                <li>• Les exclusions, les demandes RGPD ou d&apos;arrêt et les prospects déjà en rendez-vous restent gérés par des règles fixes.</li>
                <li>• Une réponse avec un lien autre que votre lien de réservation n&apos;est jamais envoyée.</li>
                <li>• Si Claude ne répond pas ou décline, les règles prennent le relais.</li>
              </ul>
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Accès MCP" description="Pilotez Vela depuis Claude Code, Cursor ou tout client MCP." />
            <CardBody className="space-y-4 text-sm">
              <p className="text-muted">
                Point d&apos;accès : <code className="rounded bg-canvas px-1">{endpoint}</code>. Chaque jeton donne accès à cet espace : vue d&apos;ensemble, conversations, brouillons,
                prospects, campagnes et rendez-vous. Votre assistant vous demandera confirmation avant d&apos;envoyer un message.
              </p>
              <CreateTokenForm endpoint={endpoint} />
              {tokens.length > 0 ? (
                <ul className="divide-y divide-line rounded-lg border border-line">
                  {tokens.map((t) => (
                    <li key={t.id} className="flex items-center justify-between gap-3 px-3 py-2.5">
                      <span className="min-w-0">
                        <span className="block truncate font-medium">{t.name}</span>
                        <span className="block text-xs text-muted">
                          <code>{t.prefix}…</code> · créé {formatRelative(t.createdAt)} · {t.lastUsedAt ? `utilisé ${formatRelative(t.lastUsedAt)}` : "jamais utilisé"}
                        </span>
                      </span>
                      <form action={revokeTokenAction.bind(null, t.id)}>
                        <Button type="submit" variant="danger" size="sm">Révoquer</Button>
                      </form>
                    </li>
                  ))}
                </ul>
              ) : null}
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Profil" />
            <CardBody className="space-y-1 text-sm">
              <p className="font-medium">{user.name}</p>
              <p className="text-muted">{user.email}</p>
            </CardBody>
          </Card>
        </div>
      </div>
    </>
  );
}
