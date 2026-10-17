import { Plug, TriangleAlert } from "lucide-react";
import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Badge, LabeledBadge } from "@/components/ui/badge";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Avatar, EmptyState, Meter, PageHeader } from "@/components/ui/misc";
import { cn } from "@/lib/cn";
import { formatAgo, formatDateTime, formatRelative, plural } from "@/lib/format";
import { ACCOUNT_STATUS, ACCOUNT_TYPES, PROVIDER_LABELS } from "@/lib/labels";
import { requireContext } from "@/server/auth/context";
import { listAccounts, needsSession } from "@/server/services/accounts";
import { AccountActions, AccountSettingsForm, ConnectAccountForm } from "./account-forms";
import { SessionPanel } from "./session-panel";

export const metadata: Metadata = { title: "Comptes LinkedIn" };

function Notice({ tone, children }: { tone: "warning" | "danger"; children: ReactNode }) {
  return (
    <p
      className={cn(
        "flex items-start gap-2 border-b px-5 py-3 text-sm",
        tone === "danger" ? "border-danger-line bg-danger-soft text-danger" : "border-warning-line bg-warning-soft text-warning",
      )}
    >
      <TriangleAlert className="mt-0.5 size-4 shrink-0" aria-hidden />
      <span className="min-w-0 break-words">{children}</span>
    </p>
  );
}

export default async function AccountsPage() {
  const { workspace } = await requireContext();
  const accounts = await listAccounts(workspace.id);
  const now = new Date();

  return (
    <>
      <PageHeader
        title="Comptes LinkedIn"
        description="Vela agit au nom de ces comptes, dans leurs horaires d'envoi et sous les plafonds de sécurité : 100 invitations par semaine sur un compte gratuit, 200 sur Premium, 40 par jour au maximum."
      />

      {accounts.length === 0 ? (
        <Card className="mb-6">
          <EmptyState icon={<Plug className="size-5" />} title="Aucun compte connecté" description="Connectez votre compte LinkedIn pour que Vela puisse prospecter." />
        </Card>
      ) : (
        <div className="mb-6 space-y-6">
          {accounts.map((a) => {
            const sessionToOpen = needsSession(a);
            const [first = a.fullName, ...rest] = a.fullName.split(" ");
            return (
              // id: the header alerts and the dashboard link to /accounts#<id>.
              <Card key={a.id} id={a.id} aria-labelledby={`account-${a.id}`}>
                <CardHeader
                  title={
                    <span className="flex items-center gap-3">
                      <Avatar first={first} last={rest.join(" ") || undefined} />
                      <span className="min-w-0">
                        <span id={`account-${a.id}`} className="block break-words">
                          {a.fullName || "Compte LinkedIn"}
                        </span>
                        <span className="block text-xs font-normal text-muted">{a.headline || "—"}</span>
                      </span>
                    </span>
                  }
                  actions={
                    <>
                      <Badge tone="neutral">{ACCOUNT_TYPES[a.accountType]}</Badge>
                      <Badge tone={a.provider === "browser" ? "info" : "neutral"}>{PROVIDER_LABELS[a.provider] ?? a.provider}</Badge>
                      <LabeledBadge map={ACCOUNT_STATUS} value={a.status} />
                    </>
                  }
                />
                {/* A session to open is explained in the 'Session LinkedIn' block below. */}
                {a.statusReason && !sessionToOpen ? <Notice tone="warning">{a.statusReason}</Notice> : null}
                {a.status === "ACTIVE" && a.lastError ? (
                  <Notice tone="danger">
                    Dernière synchronisation échouée{a.lastErrorAt ? ` (${formatAgo(a.lastErrorAt, now)})` : ""} : {a.lastError}
                  </Notice>
                ) : null}
                {a.invitesPausedUntil && a.invitesPausedUntil > now ? (
                  <Notice tone="warning">
                    LinkedIn a signalé la limite d&apos;invitations : aucune invitation avant le {formatDateTime(a.invitesPausedUntil)}. Les messages continuent.
                  </Notice>
                ) : null}
                {a.provider === "browser" ? (
                  <div className="border-b border-line px-5 py-4">
                    <SessionPanel
                      now={now}
                      account={{
                        id: a.id,
                        needsSession: sessionToOpen,
                        statusReason: a.statusReason,
                        lastDiagnosedAt: a.lastDiagnosedAt,
                        lastDiagnosisOk: a.lastDiagnosisOk,
                      }}
                    />
                  </div>
                ) : null}
                <CardBody className="grid gap-8 lg:grid-cols-[minmax(0,1fr)_minmax(0,2fr)]">
                  <div className="space-y-4">
                    <Meter label="Invitations (24 h)" value={a.quota.usage.invitesLast24h} max={a.quota.limits.dailyInvites} />
                    <Meter label="Invitations (7 jours)" value={a.quota.usage.invitesLast7d} max={a.quota.limits.weeklyInvites} />
                    <Meter label="Messages (24 h)" value={a.quota.usage.messagesLast24h} max={a.quota.limits.dailyMessages} />
                    <p className="text-xs text-muted">
                      {plural(a._count.campaigns, "campagne active", "campagnes actives")} ·{" "}
                      {a.lastSyncedAt ? `dernière synchronisation ${formatRelative(a.lastSyncedAt, now)}` : "jamais synchronisé"}
                    </p>
                    <AccountActions
                      account={{
                        id: a.id,
                        fullName: a.fullName,
                        provider: a.provider,
                        status: a.status,
                        needsSession: sessionToOpen,
                        activeCampaigns: a._count.campaigns,
                      }}
                    />
                  </div>
                  <AccountSettingsForm account={a} />
                </CardBody>
              </Card>
            );
          })}
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
