import type { Metadata } from "next";
import { Badge } from "@/components/ui/badge";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { PageHeader } from "@/components/ui/misc";
import { agentMode } from "@/server/agents";
import { CLAUDE_MODEL } from "@/server/agents/claude/client";
import { requireContext } from "@/server/auth/context";
import { WorkspaceForm } from "./workspace-form";

export const metadata: Metadata = { title: "Réglages" };

export default async function SettingsPage() {
  const { workspace, user } = await requireContext();

  return (
    <>
      <PageHeader title="Réglages" description="Votre offre, votre lien de réservation et vos agents." />
      <div className="grid gap-6 xl:grid-cols-[3fr_2fr]">
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
