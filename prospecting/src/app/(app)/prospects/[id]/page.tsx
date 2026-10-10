import { ExternalLink, MessageSquare } from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import type { ReactNode } from "react";
import { Badge, LabeledBadge } from "@/components/ui/badge";
import { Button, ButtonLink } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Avatar, PageHeader, ScorePill } from "@/components/ui/misc";
import { formatDateTime } from "@/lib/format";
import { ACTIVITY_LABELS, CONVERSATION_STATUS, MEETING_STATUS, SIGNALS, SOURCES, STAGE_LABELS } from "@/lib/labels";
import { requireContext } from "@/server/auth/context";
import type { ScoreReason } from "@/server/agents/scorer";
import { getProspect } from "@/server/services/prospects";
import { snoozeAction } from "../actions";
import { MeetingForm, NotesForm, StageButtons } from "./prospect-actions";

export const metadata: Metadata = { title: "Prospect" };

export default async function ProspectPage({ params }: { params: Promise<{ id: string }> }) {
  const { workspace } = await requireContext();
  const { id } = await params;
  const p = await getProspect(workspace.id, id);
  if (!p) notFound();
  const reasons = (p.scoreReasons ?? []) as ScoreReason[];
  const snoozed = p.snoozedUntil && p.snoozedUntil > new Date();

  return (
    <>
      <PageHeader
        title={
          <span className="flex items-center gap-4">
            <Avatar first={p.firstName} last={p.lastName} size="lg" />
            <span>
              <span className="block">{p.firstName} {p.lastName}</span>
              <span className="block text-sm font-normal text-muted">{p.headline}</span>
            </span>
          </span>
        }
        actions={
          <>
            {p.conversation ? <ButtonLink href={`/inbox?c=${p.conversation.id}`} variant="secondary"><MessageSquare className="size-4" /> Conversation</ButtonLink> : null}
            <a href={p.profileUrl} target="_blank" rel="noreferrer" className="inline-flex h-9 items-center gap-2 rounded-lg px-3 text-sm text-muted hover:bg-surface hover:text-ink">
              Profil LinkedIn <ExternalLink className="size-3.5" />
            </a>
          </>
        }
      />

      <div className="grid gap-6 xl:grid-cols-3">
        <div className="space-y-6 xl:col-span-2">
          <Card>
            <CardHeader title="Profil" actions={<><ScorePill score={p.score} /><LabeledBadge map={STAGE_LABELS} value={p.stage} /></>} />
            <CardBody className="grid gap-4 text-sm sm:grid-cols-3">
              <Info label="Poste">{p.title || "—"}</Info>
              <Info label="Entreprise">{p.company} <span className="text-muted">({p.companySize} sal.)</span></Info>
              <Info label="Secteur">{p.industry}</Info>
              <Info label="Zone">{p.location}</Info>
              <Info label="Origine">{SOURCES[p.source]?.label}</Info>
              <Info label="Signal">{p.signal ? <Badge tone="amber">{SIGNALS[p.signal] ?? p.signal}</Badge> : "—"}{p.signalDetail ? <span className="mt-1 block text-xs text-muted">{p.signalDetail}</span> : null}</Info>
              <Info label="Campagne"><Link href={`/campaigns/${p.campaign.id}`} className="hover:underline">{p.campaign.name}</Link></Info>
              <Info label="Compte">{p.account.fullName}</Info>
              <Info label="Relances envoyées">{p.followUpsSent}</Info>
            </CardBody>
          </Card>

          <Card>
            <CardHeader
              title="Pourquoi ce score"
              description={`Minimum de la campagne : ${p.campaign.minScore}/100${p.disqualifiedReason ? ` · ${p.disqualifiedReason}` : ""}`}
              actions={p.scoredBy ? <Badge tone={p.scoredBy === "claude" ? "indigo" : "gray"}>{p.scoredBy === "claude" ? "Évalué par Claude" : "Évalué par règles"}</Badge> : null}
            />
            <CardBody>
              {p.scoreSummary ? <p className="mb-3 rounded-lg bg-canvas px-3 py-2 text-sm">{p.scoreSummary}</p> : null}
              {reasons.length === 0 ? (
                <p className="text-sm text-muted">Pas encore évalué.</p>
              ) : (
                <ul className="divide-y divide-line text-sm">
                  {reasons.map((r) => (
                    <li key={r.label} className="flex items-center justify-between gap-3 py-2">
                      <span className={r.points === 0 ? "text-muted" : undefined}>{r.label}</span>
                      {r.max ? (
                        <span className="tabular-nums text-muted">{r.points} / {r.max}</span>
                      ) : (
                        <span className={r.points > 0 ? "text-emerald-700" : "text-muted"}>{r.points > 0 ? "Favorable" : "Défavorable"}</span>
                      )}
                    </li>
                  ))}
                </ul>
              )}
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Historique" />
            <CardBody>
              <ol className="relative space-y-4 border-l border-line pl-5">
                {p.activities.map((a) => {
                  const data = (a.data ?? {}) as Record<string, unknown>;
                  return (
                    <li key={a.id} className="relative">
                      <span className="absolute -left-[25px] top-1.5 size-2 rounded-full bg-brand-500 ring-4 ring-surface" aria-hidden />
                      <p className="text-sm font-medium">{ACTIVITY_LABELS[a.type] ?? a.type}</p>
                      <p className="text-xs text-muted">
                        {formatDateTime(a.createdAt)}
                        {typeof data.reason === "string" ? ` · ${data.reason}` : ""}
                        {typeof data.score === "number" ? ` · score ${data.score}` : ""}
                      </p>
                      {typeof data.note === "string" ? <p className="mt-1 rounded-lg bg-canvas px-3 py-2 text-xs">{data.note}</p> : null}
                    </li>
                  );
                })}
              </ol>
            </CardBody>
          </Card>
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader title="Actions" />
            <CardBody className="space-y-5">
              <StageButtons prospectId={p.id} stage={p.stage} />
              <div>
                <p className="mb-2 text-sm font-medium">Mettre en veille</p>
                {snoozed ? <p className="mb-2 text-xs text-muted">En veille jusqu&apos;au {formatDateTime(p.snoozedUntil)}</p> : null}
                <div className="flex flex-wrap gap-2">
                  {[3, 7, 30].map((d) => (
                    <form key={d} action={snoozeAction.bind(null, p.id, d)}>
                      <Button type="submit" variant="secondary" size="sm">{d} jours</Button>
                    </form>
                  ))}
                  {snoozed ? (
                    <form action={snoozeAction.bind(null, p.id, 0)}>
                      <Button type="submit" variant="ghost" size="sm">Réveiller</Button>
                    </form>
                  ) : null}
                </div>
              </div>
              {p.stage !== "MEETING_BOOKED" ? <MeetingForm prospectId={p.id} /> : null}
            </CardBody>
          </Card>

          {p.conversation ? (
            <Card>
              <CardHeader title="Conversation" actions={<LabeledBadge map={CONVERSATION_STATUS} value={p.conversation.status} />} />
              <CardBody>
                <ButtonLink href={`/inbox?c=${p.conversation.id}`} variant="secondary" size="sm">Ouvrir dans la boîte</ButtonLink>
              </CardBody>
            </Card>
          ) : null}

          {p.meetings.length > 0 ? (
            <Card>
              <CardHeader title="Rendez-vous" />
              <CardBody className="space-y-2">
                {p.meetings.map((m) => (
                  <div key={m.id} className="flex items-center justify-between text-sm">
                    <span>{formatDateTime(m.startsAt)}</span>
                    <LabeledBadge map={MEETING_STATUS} value={m.status} />
                  </div>
                ))}
              </CardBody>
            </Card>
          ) : null}

          <Card>
            <CardHeader title="Notes" />
            <CardBody>
              <NotesForm prospectId={p.id} notes={p.notes} />
            </CardBody>
          </Card>
        </div>
      </div>
    </>
  );
}

function Info({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div>
      <p className="text-xs text-muted">{label}</p>
      <div className="mt-0.5">{children}</div>
    </div>
  );
}
