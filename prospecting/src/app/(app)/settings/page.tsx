import { Check } from "lucide-react";
import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { PageHeader } from "@/components/ui/misc";
import { cn } from "@/lib/cn";
import { formatDate } from "@/lib/format";
import { requireContext } from "@/server/auth/context";
import { PLANS } from "@/server/domain/plans";
import { changePlanAction } from "./actions";
import { WorkspaceForm } from "./workspace-form";

export const metadata: Metadata = { title: "Réglages" };

export default async function SettingsPage() {
  const { workspace, user, role } = await requireContext();

  return (
    <>
      <PageHeader title="Réglages" description="Votre offre, votre lien de réservation et votre plan." />
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
              title="Plan"
              description={workspace.trialEndsAt ? `Essai jusqu'au ${formatDate(workspace.trialEndsAt)}` : undefined}
              actions={<Badge tone="amber">Facturation non branchée</Badge>}
            />
            <CardBody className="space-y-3">
              {(Object.keys(PLANS) as (keyof typeof PLANS)[]).map((key) => {
                const plan = PLANS[key];
                const current = workspace.plan === key;
                return (
                  <div key={key} className={cn("rounded-lg border p-4", current ? "border-brand-500 bg-brand-50/50" : "border-line")}>
                    <div className="flex items-center justify-between gap-2">
                      <p className="font-semibold">{plan.label}</p>
                      {current ? (
                        <Badge tone="indigo">Plan actuel</Badge>
                      ) : role === "OWNER" ? (
                        <form action={changePlanAction.bind(null, key)}>
                          <Button type="submit" size="sm" variant="secondary">Choisir</Button>
                        </form>
                      ) : null}
                    </div>
                    <ul className="mt-2 space-y-1 text-sm text-muted">
                      <PlanLine>{plan.maxAccounts === 1 ? "1 compte LinkedIn" : `${plan.includedAccounts} comptes inclus, jusqu'à ${plan.maxAccounts}`}</PlanLine>
                      <PlanLine>{plan.weeklyProspects ? `${plan.weeklyProspects} prospects par semaine et par campagne` : "Prospects illimités (dans les quotas LinkedIn)"}</PlanLine>
                      <PlanLine>{plan.maxFollowUps} relances automatiques</PlanLine>
                      <PlanLine off={!plan.setter}>Setter IA (réponses et prise de RDV)</PlanLine>
                      <PlanLine off={!plan.listImport}>Import de listes de prospects</PlanLine>
                    </ul>
                  </div>
                );
              })}
              <p className="text-xs text-muted">Le changement de plan est immédiat et sans paiement tant que la facturation n&apos;est pas branchée.</p>
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

function PlanLine({ children, off }: { children: ReactNode; off?: boolean }) {
  return (
    <li className={cn("flex items-start gap-2", off && "text-muted/60 line-through")}>
      <Check className={cn("mt-0.5 size-3.5 shrink-0", off ? "opacity-0" : "text-emerald-600")} aria-hidden />
      {children}
    </li>
  );
}
