import { ArrowLeft, ChevronLeft, ChevronRight, CircleCheck, Inbox, MessageSquare, Search, Sparkles, TriangleAlert } from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";
import type { ReactNode } from "react";
import { Badge, LabeledBadge } from "@/components/ui/badge";
import { ButtonLink, buttonClass } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/form";
import { Avatar, EmptyState, PageHeader } from "@/components/ui/misc";
import { SegmentedControl } from "@/components/ui/segmented-control";
import { cn } from "@/lib/cn";
import { formatNumber } from "@/lib/format";
import { CONVERSATION_STATUS, INTENTS, INTENT_TONES, STAGE_LABELS } from "@/lib/labels";
import { requireContext } from "@/server/auth/context";
import { INBOX_TABS, getThread, hasLaunchedCampaign, inboxCounts, listConversations, oldestConversationId, type InboxTab } from "@/server/services/inbox";
import { formatCompactTime, formatFullTime, formatMessageTime } from "./format";
import { doneMessage, foldSequence, parseTab, threadNavigation } from "./navigation";
import { ReplyBox, ThreadToolbar } from "./thread-controls";
import { ThreadMessages } from "./thread-messages";

export const metadata: Metadata = { title: "Boîte de réception" };

const TAB_LABELS: Record<InboxTab, string> = { todo: "À traiter", drafts: "À valider", ai: "Setter", all: "Toutes" };
/** Caption under outbound bubbles, and prefix of the last message in the list. */
const AUTHOR_LABELS: Record<string, string> = { SEQUENCE: "Séquence", AI: "Setter", HUMAN: "Vous" };

type Conversation = Awaited<ReturnType<typeof listConversations>>[number];
type Thread = NonNullable<Awaited<ReturnType<typeof getThread>>>;
type Message = Thread["messages"][number];

function IntentChip({ intent }: { intent: string | null }) {
  if (!intent) return null;
  return <Badge tone={INTENT_TONES[intent] ?? "neutral"}>{INTENTS[intent] ?? intent}</Badge>;
}

/** The one line telling what a conversation waits for. */
function ActionLine({ c, muted }: { c: Conversation; muted: string }) {
  if (c.drafts.length > 0) {
    return (
      <span className="inline-flex min-w-0 items-center gap-1 text-ai">
        <Sparkles className="size-3 shrink-0" aria-hidden />
        <span className="truncate">Réponse proposée prête</span>
      </span>
    );
  }
  if (c.prospect.stage === "MEETING_BOOKED") return <span className="truncate text-success">Rendez-vous pris</span>;
  const text =
    c.escalationReason ||
    { HUMAN: "Vous avez la main", NEEDS_HUMAN: "À vous de répondre", AI_ACTIVE: "Le setter s'en occupe", CLOSED: "Terminée" }[c.status] ||
    "";
  return <span className={cn("min-w-0 truncate", muted)}>{text}</span>;
}

function ConversationRow({ c, href, selected, showProposal, now, timeZone }: { c: Conversation; href: string; selected: boolean; showProposal: boolean; now: Date; timeZone: string }) {
  const last = c.messages[0];
  // text-muted is too faint on brand-50: the selected row uses ink-2.
  const muted = selected ? "text-ink-2" : "text-muted";
  return (
    <li>
      <Link
        href={href}
        aria-current={selected ? "page" : undefined}
        className={cn(
          "flex gap-3 border-l-[3px] py-3 pr-4 pl-[13px] transition-colors",
          "focus-visible:outline-2 focus-visible:-outline-offset-2 focus-visible:outline-brand-600",
          selected ? "border-brand-600 bg-brand-50" : "border-transparent hover:bg-surface-2",
        )}
      >
        <Avatar first={c.prospect.firstName} last={c.prospect.lastName} size="sm" />
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-2">
            {c.unread ? (
              <>
                <span className="size-1.5 shrink-0 rounded-full bg-brand-600" aria-hidden />
                <span className="sr-only">Non lu : </span>
              </>
            ) : null}
            <p className={cn("min-w-0 flex-1 truncate text-sm text-ink", c.unread ? "font-semibold" : "font-medium")}>
              {c.prospect.firstName} {c.prospect.lastName}
            </p>
            {c.lastMessageAt ? (
              <time dateTime={c.lastMessageAt.toISOString()} title={formatFullTime(c.lastMessageAt, timeZone)} className={cn("shrink-0 text-2xs tabular-nums", muted)}>
                {formatCompactTime(c.lastMessageAt, now, timeZone)}
              </time>
            ) : null}
          </div>
          {c.prospect.company ? <p className={cn("truncate text-xs", muted)}>{c.prospect.company}</p> : null}
          {last ? (
            <p className="mt-1 line-clamp-1 text-xs text-ink-2">
              {last.direction === "OUTBOUND" ? <span className={muted}>{AUTHOR_LABELS[last.author] ?? "Vous"} : </span> : null}
              {last.body}
            </p>
          ) : null}
          {showProposal && c.drafts[0] ? (
            <p className="mt-1.5 line-clamp-2 border-l-2 border-ai-line pl-2 text-xs text-ink-2">
              <span className="font-medium text-ai">Réponse proposée : </span>
              {c.drafts[0].body}
            </p>
          ) : null}
          <div className="mt-1.5 flex min-w-0 items-center gap-2 text-xs">
            <IntentChip intent={c.lastIntent} />
            <ActionLine c={c} muted={muted} />
          </div>
        </div>
      </Link>
    </li>
  );
}

function Bubble({ m, firstName, timeZone }: { m: Message; firstName: string; timeZone: string }) {
  const outbound = m.direction === "OUTBOUND";
  const caption = outbound ? (AUTHOR_LABELS[m.author] ?? "Vous") : firstName;
  return (
    <li className={cn("flex flex-col", outbound ? "items-end" : "items-start")}>
      <div
        className={cn(
          "max-w-[85%] rounded-2xl px-4 py-2.5 text-sm whitespace-pre-line break-words",
          !outbound && "rounded-bl-sm border border-line bg-surface text-ink shadow-card",
          m.author === "SEQUENCE" && "rounded-br-sm border border-line bg-surface-2 text-ink-2",
          m.author === "AI" && "rounded-br-sm border border-ai-line bg-ai-soft text-ai",
          m.author === "HUMAN" && "rounded-br-sm bg-brand-600 text-white shadow-card",
        )}
      >
        {m.body}
      </div>
      <span className={cn("mt-1 inline-flex items-center gap-1 text-2xs text-muted", m.author === "AI" && "text-ai")}>
        {m.author === "AI" ? <Sparkles className="size-3" aria-hidden /> : null}
        <span className="font-medium">{caption}</span>
        <span aria-hidden>·</span>
        <time dateTime={m.sentAt.toISOString()}>{formatMessageTime(m.sentAt, timeZone)}</time>
      </span>
    </li>
  );
}

function Banner({ tone, icon, children }: { tone: "success" | "warning"; icon: ReactNode; children: ReactNode }) {
  return (
    <div
      role={tone === "success" ? "status" : undefined}
      className={cn(
        "flex items-start gap-2 border-b px-4 py-2.5 text-sm sm:px-5",
        tone === "success" ? "border-success-line bg-success-soft text-success" : "border-warning-line bg-warning-soft text-warning",
      )}
    >
      <span className="mt-0.5 shrink-0">{icon}</span>
      <span className="min-w-0">{children}</span>
    </div>
  );
}

export default async function InboxPage({ searchParams }: { searchParams: Promise<{ tab?: string; c?: string; q?: string; done?: string; did?: string }> }) {
  const { workspace } = await requireContext();
  const sp = await searchParams;
  const tab = parseTab(sp.tab);
  const q = sp.q?.trim() ?? "";
  const [counts, conversations, thread] = await Promise.all([
    inboxCounts(workspace.id),
    listConversations(workspace.id, tab, q),
    sp.c ? getThread(workspace.id, sp.c) : Promise.resolve(null),
  ]);
  const [oldestTodoId, launched] = await Promise.all([
    thread ? Promise.resolve(null) : oldestConversationId(workspace.id, "todo"),
    conversations.length === 0 && counts.all === 0 ? hasLaunchedCampaign(workspace.id) : Promise.resolve(true),
  ]);
  const now = new Date();
  const timeZone = workspace.timezone;

  const link = (patch: Record<string, string | undefined>) => {
    const params = new URLSearchParams(Object.entries({ tab, q: q || undefined, c: thread?.id, ...patch }).filter(([, v]) => v) as [string, string][]);
    return `/inbox?${params.toString()}`;
  };

  const ids = conversations.map((c) => c.id);
  const position = threadNavigation(ids, thread?.id);
  const total = q ? ids.length : Math.max(counts[tab], ids.length);
  const doneName = sp.done?.trim().slice(0, 60);
  const done = doneName ? doneMessage(sp.did, doneName) : null;
  const listEmpty = conversations.length === 0;
  const doneBanner = (suffix?: string) =>
    done ? (
      <Banner tone="success" icon={<CircleCheck className="size-4" aria-hidden />}>
        {suffix ? `${done} · ${suffix}` : `${done}.`}
      </Banner>
    ) : null;

  const empty: { title: string; description?: string; action?: ReactNode } = (() => {
    if (q) return { title: "Aucun résultat", description: `Aucune conversation ne correspond à « ${q} ».` };
    if (counts.all === 0) {
      return launched
        ? { title: "Vos campagnes tournent", description: "Premières réponses en général sous 2 à 5 jours." }
        : {
            title: "Pas encore de conversation",
            description: "Les réponses arrivent ici dès qu'un prospect accepte votre invitation et répond au premier message.",
            action: <ButtonLink href="/campaigns" size="sm">Lancer une campagne</ButtonLink>,
          };
    }
    switch (tab) {
      case "todo":
        return { title: "Rien à traiter", description: "Le setter s'occupe du reste. Revenez quand il vous signale quelque chose." };
      case "drafts":
        return { title: "Aucune réponse à valider", description: "Les réponses proposées par le setter attendent ici votre accord." };
      case "ai":
        return { title: "Aucune conversation au setter", description: "Les conversations que le setter mène seul apparaissent ici." };
      default:
        return { title: "Aucune conversation" };
    }
  })();

  const draft = thread?.drafts[0] ?? null;
  const fold = thread ? foldSequence(thread.messages) : null;

  return (
    <>
      {/* On phones an open thread starts with its own header. */}
      <div className={cn(thread && "max-lg:hidden")}>
        <PageHeader title="Boîte de réception" description="Les réponses de vos prospects. Le setter traite ce qu'il peut et vous signale le reste." />
      </div>
      <Card
        className={cn(
          // overflow-clip (not hidden) keeps the rounded corners without breaking the sticky bars inside.
          "grid grid-rows-[minmax(0,1fr)] overflow-clip lg:h-[calc(100dvh-12rem)] lg:min-h-[560px] lg:grid-cols-[380px_minmax(0,1fr)]",
          thread && "max-lg:h-[calc(100dvh-var(--app-header-h)-var(--mobile-nav-h)-3rem)] max-lg:min-h-[30rem]",
        )}
      >
        <div className={cn("flex min-h-0 min-w-0 flex-col border-line lg:border-r", thread && "hidden lg:flex")}>
          <div className="sticky top-(--app-header-h) z-10 space-y-2 border-b border-line bg-surface p-2 lg:static">
            <SegmentedControl
              label="Filtrer les conversations"
              value={tab}
              fill
              stacked
              items={INBOX_TABS.map((t) => ({ href: link({ tab: t, c: undefined }), value: t, label: TAB_LABELS[t], count: counts[t] }))}
            />
            <form action="/inbox" role="search" className="relative">
              <input type="hidden" name="tab" value={tab} />
              <Search className="pointer-events-none absolute left-2.5 top-1/2 size-4 -translate-y-1/2 text-muted" aria-hidden />
              <Input type="search" name="q" defaultValue={q} placeholder="Rechercher un prospect…" aria-label="Rechercher une conversation" className="pl-8" />
            </form>
          </div>
          {!thread ? <div className="lg:hidden">{doneBanner(listEmpty ? "Tout est traité" : undefined)}</div> : null}
          {conversations.length === 0 ? (
            <EmptyState icon={<Inbox className="size-5" aria-hidden />} title={empty.title} description={empty.description} action={empty.action} />
          ) : (
            <ul className="min-h-0 flex-1 divide-y divide-line overflow-y-auto" aria-label={`Conversations : ${TAB_LABELS[tab]}`}>
              {conversations.map((c) => (
                <ConversationRow key={c.id} c={c} href={link({ c: c.id })} selected={c.id === thread?.id} showProposal={tab === "drafts"} now={now} timeZone={timeZone} />
              ))}
            </ul>
          )}
        </div>

        <div className={cn("min-h-0 min-w-0 flex-col", thread ? "flex" : "hidden lg:flex")}>
          {!thread ? (
            <>
              {doneBanner()}
              <div className="flex flex-1 items-center justify-center">
                <EmptyState
                  icon={listEmpty && !q ? <CircleCheck className="size-5" aria-hidden /> : <MessageSquare className="size-5" aria-hidden />}
                  title={!listEmpty ? "Sélectionnez une conversation" : q ? "Aucun résultat" : counts.all > 0 ? "Tout est traité" : "Aucune conversation pour l'instant"}
                  description={`${formatNumber(counts.todo)} à traiter · ${formatNumber(counts.drafts)} à valider`}
                  action={oldestTodoId ? <ButtonLink href={`/inbox?tab=todo&c=${encodeURIComponent(oldestTodoId)}`}>Traiter le plus ancien</ButtonLink> : undefined}
                />
              </div>
            </>
          ) : (
            <>
              <header className="border-b border-line px-4 py-3 sm:px-5">
                <div className="flex items-center gap-3">
                  <ButtonLink href={link({ c: undefined })} variant="ghost" size="icon" className="-ml-2 size-11 lg:hidden" aria-label="Retour à la liste">
                    <ArrowLeft className="size-5" aria-hidden />
                  </ButtonLink>
                  <span className="flex shrink-0 max-sm:hidden">
                    <Avatar first={thread.prospect.firstName} last={thread.prospect.lastName} />
                  </span>
                  <div className="min-w-0 flex-1">
                    <div className="flex flex-wrap items-center gap-x-2 gap-y-1">
                      <Link href={`/prospects/${thread.prospect.id}`} className="min-w-0 truncate font-semibold text-ink hover:underline">
                        {thread.prospect.firstName} {thread.prospect.lastName}
                      </Link>
                      <IntentChip intent={thread.lastIntent} />
                      {thread.prospect.stage !== "REPLIED" ? <LabeledBadge map={STAGE_LABELS} value={thread.prospect.stage} /> : null}
                      <LabeledBadge map={CONVERSATION_STATUS} value={thread.status} />
                    </div>
                    <p className="truncate text-xs text-muted">
                      {[thread.prospect.title, thread.prospect.company, thread.prospect.campaign.name].filter(Boolean).join(" · ")}
                    </p>
                  </div>
                  {position.position > 0 ? (
                    <nav aria-label="Parcourir les conversations" className="flex shrink-0 items-center gap-0.5">
                      <span className="mr-1 text-xs text-muted tabular-nums">
                        <span aria-hidden>
                          {formatNumber(position.position)} / {formatNumber(total)}
                        </span>
                        <span className="sr-only">
                          Conversation {formatNumber(position.position)} sur {formatNumber(total)}
                        </span>
                      </span>
                      <PagerLink href={position.prevId ? link({ c: position.prevId }) : null} label="Conversation précédente">
                        <ChevronLeft className="size-4" aria-hidden />
                      </PagerLink>
                      <PagerLink href={position.nextId ? link({ c: position.nextId }) : null} label="Conversation suivante">
                        <ChevronRight className="size-4" aria-hidden />
                      </PagerLink>
                    </nav>
                  ) : null}
                </div>
                <ThreadToolbar
                  key={thread.id}
                  conversationId={thread.id}
                  prospectId={thread.prospect.id}
                  status={thread.status}
                  unread={thread.unread}
                  stage={thread.prospect.stage}
                  hasDraft={draft !== null}
                  nav={{ tab, q, next: position.afterId ?? "", name: thread.prospect.firstName }}
                />
              </header>

              {doneBanner("fil suivant")}
              {thread.status === "NEEDS_HUMAN" && thread.escalationReason ? (
                <Banner tone="warning" icon={<TriangleAlert className="size-4" aria-hidden />}>
                  <strong className="font-semibold">Le setter vous passe la main.</strong> {thread.escalationReason}
                </Banner>
              ) : null}
              {thread.prospect.meetings[0] ? (
                <Banner tone="success" icon={<CircleCheck className="size-4" aria-hidden />}>
                  Rendez-vous réservé pour le <strong className="font-semibold">{formatFullTime(thread.prospect.meetings[0].startsAt, timeZone)}</strong>.
                </Banner>
              ) : null}

              <ThreadMessages threadId={thread.id} count={thread.messages.length} className="min-h-0 flex-1 space-y-4 overflow-y-auto bg-canvas px-4 py-5 sm:px-5">
                {fold && fold.folded.length > 0 ? (
                  <li>
                    <details className="group">
                      <summary className="mx-auto flex w-fit cursor-pointer list-none items-center gap-1 rounded-full border border-line bg-surface px-3 py-1 text-xs font-medium text-ink-2 hover:bg-surface-2 pointer-coarse:min-h-11 [&::-webkit-details-marker]:hidden">
                        {formatNumber(fold.folded.length)} messages de séquence · <span className="text-brand-700 group-open:hidden">afficher</span>
                        <span className="hidden text-brand-700 group-open:inline">masquer</span>
                      </summary>
                      <ol className="mt-4 space-y-4">
                        {fold.folded.map((m) => (
                          <Bubble key={m.id} m={m} firstName={thread.prospect.firstName} timeZone={timeZone} />
                        ))}
                      </ol>
                    </details>
                  </li>
                ) : null}
                {(fold?.visible ?? thread.messages).map((m) => (
                  <Bubble key={m.id} m={m} firstName={thread.prospect.firstName} timeZone={timeZone} />
                ))}
              </ThreadMessages>

              {/* The reply box stays pinned above the mobile tab bar; on desktop it closes the flex column. */}
              <div className="z-10 border-t border-line bg-surface px-4 py-3 max-lg:sticky max-lg:bottom-(--mobile-nav-h) sm:px-5 lg:max-h-[55%] lg:overflow-y-auto">
                <ReplyBox
                  key={`${thread.id}:${draft?.id ?? "reply"}`}
                  conversationId={thread.id}
                  status={thread.status}
                  draft={draft ? { id: draft.id, body: draft.body, intent: draft.intent, rationale: draft.rationale, author: draft.author } : null}
                  bookingUrl={thread.bookingUrl}
                  firstName={thread.prospect.firstName}
                  nav={{ tab, q, next: position.afterId ?? "", name: thread.prospect.firstName }}
                />
              </div>
            </>
          )}
        </div>
      </Card>
    </>
  );
}

function PagerLink({ href, label, children }: { href: string | null; label: string; children: ReactNode }) {
  if (!href) {
    // Nothing before or after: keep the slot so the pager does not jump, but out of the tab order.
    return (
      <span aria-hidden className={buttonClass({ variant: "ghost", size: "icon" }, "pointer-events-none opacity-40")}>
        {children}
      </span>
    );
  }
  return (
    <Link href={href} aria-label={label} className={buttonClass({ variant: "ghost", size: "icon" })}>
      {children}
    </Link>
  );
}
