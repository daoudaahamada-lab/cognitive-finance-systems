import { Plug } from "lucide-react";
import type { Metadata } from "next";
import { Badge, LabeledBadge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Avatar, EmptyState, Meter, PageHeader } from "@/components/ui/misc";
import { formatRelative } from "@/lib/format";
import { ACCOUNT_STATUS, ACCOUNT_TYPES } from "@/lib/labels";
import { requireContext } from "@/server/auth/context";
import { listAccounts } from "@/server/services/accounts";
import { AccountSettingsForm, ConnectAccountForm } from "./account-forms";
import { setAccountStatusAction } from "./actions";

export const metadata: Metadata = { title: "Comptes LinkedIn" };

export default async function AccountsPage() {
  const { workspace } = await requireContext();
  const accounts = await listAccounts(workspace.id);

  return (
    <>
      <PageHeader
        title="Comptes LinkedIn"
        description="Le moteur agit au nom de ces comptes, dans leurs horaires d'envoi et sous les plafonds de sécurité (100 invitations par semaine sur un compte gratuit, 200 sur Premium, 40 par jour au maximum)."
      />

      {accounts.length === 0 ? (
        <Card className="mb-6">
          <EmptyState icon={<Plug className="size-5" />} title="Aucun compte connecté" description="Connectez un compte LinkedIn pour que le moteur puisse prospecter." />
        </Card>
      ) : (
        <div className="mb-6 space-y-6">
          {accounts.map((a) => (
            <Card key={a.id}>
              <CardHeader
                title={
                  <span className="flex items-center gap-3">
                    <Avatar first={a.fullName.split(" ")[0] ?? a.fullName} last={a.fullName.split(" ")[1]} />
                    <span>
                      <span className="block">{a.fullName}</span>
                      <span className="block text-xs font-normal text-muted">{a.headline || "—"}</span>
                    </span>
                  </span>
                }
                actions={
                  <>
                    <Badge tone="gray">{ACCOUNT_TYPES[a.accountType]}</Badge>
                    <Badge tone="violet">{a.provider === "simulator" ? "Simulateur" : a.provider}</Badge>
                    <LabeledBadge map={ACCOUNT_STATUS} value={a.status} />
                  </>
                }
              />
              <CardBody className="grid gap-8 lg:grid-cols-[1fr_2fr]">
                <div className="space-y-4">
                  <Meter label="Invitations (24 h)" value={a.quota.usage.invitesLast24h} max={a.quota.limits.dailyInvites} />
                  <Meter label="Invitations (7 jours)" value={a.quota.usage.invitesLast7d} max={a.quota.limits.weeklyInvites} />
                  <Meter label="Messages (24 h)" value={a.quota.usage.messagesLast24h} max={a.quota.limits.dailyMessages} />
                  <p className="text-xs text-muted">
                    {a._count.campaigns} campagne{a._count.campaigns > 1 ? "s" : ""} active{a._count.campaigns > 1 ? "s" : ""} · dernière synchro {formatRelative(a.lastSyncedAt)}
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {a.status === "ACTIVE" ? (
                      <form action={setAccountStatusAction.bind(null, a.id, "PAUSED")}>
                        <Button type="submit" variant="secondary" size="sm">Mettre en pause</Button>
                      </form>
                    ) : (
                      <form action={setAccountStatusAction.bind(null, a.id, "ACTIVE")}>
                        <Button type="submit" variant="secondary" size="sm">Réactiver</Button>
                      </form>
                    )}
                    <form action={setAccountStatusAction.bind(null, a.id, "DISCONNECTED")}>
                      <Button type="submit" variant="danger" size="sm">Déconnecter</Button>
                    </form>
                  </div>
                </div>
                <AccountSettingsForm account={a} />
              </CardBody>
            </Card>
          ))}
        </div>
      )}

      <Card>
        <CardHeader title="Connecter un compte" description="Chaque compte a ses propres horaires et plafonds." />
        <CardBody>
          <ConnectAccountForm />
        </CardBody>
      </Card>
    </>
  );
}
