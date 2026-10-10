import { ArrowLeft, Inbox, TriangleAlert } from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";
import { LabeledBadge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/form";
import { Avatar, EmptyState, PageHeader } from "@/components/ui/misc";
import { cn } from "@/lib/cn";
import { formatDateTime, formatRelative } from "@/lib/format";
import { CONVERSATION_STATUS, INTENTS, STAGE_LABELS } from "@/lib/labels";
import { requireContext } from "@/server/auth/context";
import { INBOX_TABS, getThread, inboxCounts, listConversations, type InboxTab } from "@/server/services/inbox";
import { Composer, ConversationButtons, DraftCard } from "./thread-controls";

export const metadata: Metadata = { title: "Boîte de réception" };

const TAB_LABELS: Record<InboxTab, string> = { todo: "À traiter", drafts: "Brouillons", ai: "IA", all: "Toutes" };
const AUTHOR_LABELS: Record<string, string> = { SEQUENCE: "Séquence", AI: "Setter IA", HUMAN: "Vous", PROSPECT: "" };

export default async function InboxPage({ searchParams }: { searchParams: Promise<{ tab?: string; c?: string; q?: string; sent?: string }> }) {
  const { workspace } = await requireContext();
  const sp = await searchParams;
  const tab: InboxTab = INBOX_TABS.includes(sp.tab as InboxTab) ? (sp.tab as InboxTab) : "todo";
  const [counts, conversations, thread] = await Promise.all([
    inboxCounts(workspace.id),
    listConversations(workspace.id, tab, sp.q),
    sp.c ? getThread(workspace.id, sp.c) : Promise.resolve(null),
  ]);
  const link = (patch: Record<string, string | undefined>) => {
    const params = new URLSearchParams(Object.entries({ tab, q: sp.q, c: sp.c, ...patch, sent: undefined }).filter(([, v]) => v) as [string, string][]);
    return `/inbox?${params.toString()}`;
  };

  return (
    <>
      <PageHeader title="Boîte de réception" description="Les réponses de vos prospects. Le setter traite ce qu'il peut et vous signale le reste." />
      <Card className="grid overflow-hidden lg:h-[calc(100vh-12rem)] lg:min-h-[560px] lg:grid-cols-[360px_minmax(0,1fr)]">
        <div className={cn("flex min-h-0 min-w-0 flex-col border-line lg:border-r", thread && "hidden lg:flex")}>
          <nav className="flex gap-1 overflow-x-auto border-b border-line p-2" aria-label="Filtres">
            {INBOX_TABS.map((t) => (
              <Link
                key={t}
                href={link({ tab: t, c: undefined })}
                aria-current={t === tab ? "page" : undefined}
                className={cn("flex items-center gap-1 whitespace-nowrap rounded-lg px-2 py-1.5 text-[13px]", t === tab ? "bg-canvas font-medium text-ink" : "text-muted hover:text-ink")}
              >
                {TAB_LABELS[t]}
                <span className={cn("rounded-full px-1.5 text-[11px] tabular-nums", t === "todo" && counts.todo > 0 ? "bg-red-600 text-white" : "bg-zinc-100 text-muted")}>{counts[t]}</span>
              </Link>
            ))}
          </nav>
          <form action="/inbox" className="border-b border-line p-2">
            <input type="hidden" name="tab" value={tab} />
            <Input name="q" defaultValue={sp.q} placeholder="Rechercher un prospect…" aria-label="Rechercher une conversation" />
          </form>
          {conversations.length === 0 ? (
            <EmptyState icon={<Inbox className="size-5" />} title={tab === "todo" ? "Rien à traiter" : "Aucune conversation"} description={tab === "todo" ? "Le setter s'occupe du reste. Revenez quand il vous signale quelque chose." : undefined} />
          ) : (
            <ul className="flex-1 divide-y divide-line overflow-y-auto">
              {conversations.map((c) => {
                const last = c.messages[0];
                return (
                  <li key={c.id}>
                    <Link href={link({ c: c.id })} className={cn("flex gap-3 px-4 py-3 hover:bg-canvas", c.id === sp.c && "bg-brand-50/70")}>
                      <Avatar first={c.prospect.firstName} last={c.prospect.lastName} size="sm" />
                      <div className="min-w-0 flex-1">
                        <div className="flex items-center justify-between gap-2">
                          <p className={cn("truncate text-sm", c.unread ? "font-semibold" : "font-medium")}>
                            {c.prospect.firstName} {c.prospect.lastName}
                          </p>
                          <span className="shrink-0 text-[11px] text-muted">{formatRelative(c.lastMessageAt)}</span>
                        </div>
                        <p className="truncate text-xs text-muted">{c.prospect.company}</p>
                        <p className="mt-1 line-clamp-1 text-xs">
                          {last?.direction === "OUTBOUND" ? <span className="text-muted">{AUTHOR_LABELS[last.author]} : </span> : null}
                          {last?.body}
                        </p>
                        <div className="mt-1.5 flex flex-wrap gap-1">
                          {c.status !== "AI_ACTIVE" ? <LabeledBadge map={CONVERSATION_STATUS} value={c.status} /> : null}
                          {c.drafts.length > 0 ? <LabeledBadge map={{ x: { label: "Brouillon", tone: "indigo" } }} value="x" /> : null}
                          {c.prospect.stage === "MEETING_BOOKED" ? <LabeledBadge map={STAGE_LABELS} value="MEETING_BOOKED" /> : null}
                        </div>
                      </div>
                    </Link>
                  </li>
                );
              })}
            </ul>
          )}
        </div>

        <div className={cn("min-h-0 min-w-0 flex-col", thread ? "flex" : "hidden lg:flex")}>
          {!thread ? (
            <EmptyState title="Sélectionnez une conversation" description="Choisissez un fil à gauche pour lire l'échange et répondre." />
          ) : (
            <>
              <header className="flex flex-wrap items-start justify-between gap-3 border-b border-line px-5 py-4">
                <div className="flex min-w-0 items-center gap-3">
                  <Link href={link({ c: undefined })} className="lg:hidden" aria-label="Retour à la liste"><ArrowLeft className="size-5" /></Link>
                  <Avatar first={thread.prospect.firstName} last={thread.prospect.lastName} />
                  <div className="min-w-0">
                    <Link href={`/prospects/${thread.prospect.id}`} className="block truncate font-semibold hover:underline">
                      {thread.prospect.firstName} {thread.prospect.lastName}
                    </Link>
                    <p className="truncate text-xs text-muted">
                      {thread.prospect.title} · {thread.prospect.company} · {thread.prospect.campaign.name}
                    </p>
                  </div>
                </div>
                <div className="flex flex-wrap items-center gap-2">
                  {thread.lastIntent ? <span className="text-xs text-muted">Intention : {INTENTS[thread.lastIntent] ?? thread.lastIntent}</span> : null}
                  <LabeledBadge map={STAGE_LABELS} value={thread.prospect.stage} />
                  <LabeledBadge map={CONVERSATION_STATUS} value={thread.status} />
                </div>
              </header>

              {sp.sent ? (
                <div role="status" className="border-b border-emerald-200 bg-emerald-50 px-5 py-2.5 text-sm text-emerald-900">
                  Réponse envoyée.
                </div>
              ) : null}
              {thread.status === "NEEDS_HUMAN" && thread.escalationReason ? (
                <div className="flex items-start gap-2 border-b border-amber-200 bg-amber-50 px-5 py-3 text-sm text-amber-900">
                  <TriangleAlert className="mt-0.5 size-4 shrink-0" aria-hidden />
                  <span><strong className="font-semibold">Le setter vous passe la main.</strong> {thread.escalationReason}</span>
                </div>
              ) : null}
              {thread.prospect.meetings[0] ? (
                <div className="border-b border-emerald-200 bg-emerald-50 px-5 py-3 text-sm text-emerald-900">
                  Rendez-vous réservé pour le <strong className="font-semibold">{formatDateTime(thread.prospect.meetings[0].startsAt)}</strong>.
                </div>
              ) : null}

              <ol className="flex-1 space-y-4 overflow-y-auto bg-canvas/50 px-5 py-6" aria-label="Messages">
                {thread.messages.map((m) => {
                  const outbound = m.direction === "OUTBOUND";
                  return (
                    <li key={m.id} className={cn("flex flex-col", outbound ? "items-end" : "items-start")}>
                      <div className={cn("max-w-[85%] whitespace-pre-line rounded-2xl px-4 py-2.5 text-sm shadow-sm", outbound ? "rounded-br-sm bg-brand-600 text-white" : "rounded-bl-sm border border-line bg-surface")}>
                        {m.body}
                      </div>
                      <span className="mt-1 text-[11px] text-muted">
                        {outbound ? `${AUTHOR_LABELS[m.author]} · ` : ""}
                        {formatDateTime(m.sentAt)}
                      </span>
                    </li>
                  );
                })}
              </ol>

              <div className="max-h-[55%] space-y-4 overflow-y-auto border-t border-line px-5 py-4">
                {thread.drafts[0] ? <DraftCard draft={thread.drafts[0]} /> : null}
                <Composer conversationId={thread.id} status={thread.status} />
                <ConversationButtons conversationId={thread.id} prospectId={thread.prospect.id} status={thread.status} unread={thread.unread} stage={thread.prospect.stage} />
              </div>
            </>
          )}
        </div>
      </Card>
    </>
  );
}
