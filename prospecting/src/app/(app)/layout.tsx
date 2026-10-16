import { LogOut } from "lucide-react";
import Link from "next/link";
import type { ReactNode } from "react";
import { EngineButton } from "@/components/layout/engine-button";
import { AccountAlerts, EngineStatusChips } from "@/components/layout/engine-status";
import { Logo } from "@/components/layout/logo";
import { BottomNav, Nav } from "@/components/layout/nav";
import { StatusRefresh } from "@/components/layout/status-refresh";
import { Button } from "@/components/ui/button";
import { Avatar } from "@/components/ui/misc";
import { BRAND } from "@/lib/brand";
import { requireContext } from "@/server/auth/context";
import { engineStatus } from "@/server/services/engine-status";
import { inboxCounts } from "@/server/services/inbox";
import { logoutAction } from "../(auth)/actions";

const homeLabel = `${BRAND.name}, tableau de bord`;

export default async function AppLayout({ children }: { children: ReactNode }) {
  const { user, workspace } = await requireContext();
  const [counts, status] = await Promise.all([inboxCounts(workspace.id), engineStatus(workspace.id)]);
  const [first = user.name, last] = user.name.split(" ");

  return (
    <div className="min-h-screen lg:grid lg:grid-cols-[240px_minmax(0,1fr)]">
      <a
        href="#contenu"
        className="sr-only rounded-control bg-surface text-sm font-medium text-ink shadow-pop focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:px-4 focus:py-2 focus:outline-2 focus:outline-brand-600"
      >
        Aller au contenu
      </a>
      <aside className="hidden border-r border-line bg-surface lg:sticky lg:top-0 lg:flex lg:h-screen lg:flex-col">
        <div className="px-5 py-5">
          <Link href="/dashboard" aria-label={homeLabel} className="rounded-control focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-brand-600">
            <Logo />
          </Link>
        </div>
        <div className="flex-1 overflow-y-auto px-3">
          <Nav inboxCount={counts.todo} />
        </div>
        <div className="flex items-center gap-2.5 border-t border-line p-4">
          <Avatar first={first} last={last} size="sm" />
          <div className="min-w-0 flex-1">
            <p className="truncate text-sm font-medium text-ink">{user.name}</p>
            <p className="truncate text-xs text-muted">{workspace.name}</p>
          </div>
          <form action={logoutAction}>
            <Button type="submit" variant="ghost" size="icon" aria-label="Se déconnecter" title="Se déconnecter">
              <LogOut className="size-4" aria-hidden />
            </Button>
          </form>
        </div>
      </aside>

      <div className="min-w-0">
        <header className="sticky top-0 z-20 h-(--app-header-h) border-b border-line bg-surface/90 backdrop-blur">
          <div className="flex h-full items-center justify-between gap-3 px-4 sm:px-8">
            <Link href="/dashboard" aria-label={homeLabel} className="rounded-control focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-brand-600 lg:hidden">
              <Logo />
            </Link>
            <div className="ml-auto flex min-w-0 items-center lg:ml-0 lg:flex-1">
              <EngineStatusChips status={status} />
            </div>
            <EngineButton />
          </div>
        </header>
        <AccountAlerts status={status} />
        <main id="contenu" tabIndex={-1} className="mx-auto max-w-7xl px-4 pt-8 pb-[calc(var(--mobile-nav-h)+2.5rem)] focus:outline-none sm:px-8 lg:pb-8">
          {children}
        </main>
      </div>
      <BottomNav inboxCount={counts.todo} />
      <StatusRefresh />
    </div>
  );
}
