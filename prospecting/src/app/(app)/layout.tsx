import { RefreshCw } from "lucide-react";
import type { ReactNode } from "react";
import { Logo } from "@/components/layout/logo";
import { Nav } from "@/components/layout/nav";
import { Avatar } from "@/components/ui/misc";
import { SubmitButton } from "@/components/ui/submit-button";
import { agentLabel } from "@/server/agents";
import { requireContext } from "@/server/auth/context";
import { inboxCounts } from "@/server/services/inbox";
import { logoutAction } from "../(auth)/actions";
import { runEngineNow } from "./engine-actions";

export default async function AppLayout({ children }: { children: ReactNode }) {
  const { user, workspace } = await requireContext();
  const counts = await inboxCounts(workspace.id);

  return (
    <div className="min-h-screen lg:grid lg:grid-cols-[240px_minmax(0,1fr)]">
      <aside className="hidden border-r border-line bg-surface lg:flex lg:h-screen lg:flex-col lg:sticky lg:top-0">
        <div className="px-5 py-5">
          <Logo />
        </div>
        <div className="flex-1 overflow-y-auto px-3">
          <Nav inboxCount={counts.todo} orientation="vertical" />
        </div>
        <div className="space-y-3 border-t border-line p-4">
          <div className="rounded-lg bg-canvas px-3 py-2 text-xs">
            <p className="font-medium text-ink">{workspace.name}</p>
          </div>
          <div className="flex items-center gap-2">
            <Avatar first={user.name.split(" ")[0] ?? user.name} last={user.name.split(" ")[1]} size="sm" />
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-medium">{user.name}</p>
              <p className="truncate text-xs text-muted">{user.email}</p>
            </div>
          </div>
          <form action={logoutAction}>
            <button type="submit" className="text-xs text-muted hover:text-ink">
              Se déconnecter
            </button>
          </form>
        </div>
      </aside>

      <div className="min-w-0">
        <div className="sticky top-0 z-10 border-b border-line bg-surface/90 backdrop-blur">
          <div className="flex items-center justify-between gap-3 px-4 py-3 sm:px-8">
            <div className="lg:hidden">
              <Logo />
            </div>
            <p className="hidden text-xs text-muted lg:block">
              LinkedIn : <span className="font-medium text-ink">simulateur</span> · Agents : <span className="font-medium text-ink">{agentLabel()}</span> · le moteur tourne en continu via le worker
            </p>
            <form action={runEngineNow}>
              <SubmitButton variant="secondary" size="sm" pendingLabel="Moteur en cours…">
                <RefreshCw className="size-3.5" aria-hidden /> Lancer le moteur
              </SubmitButton>
            </form>
          </div>
          <div className="px-3 pb-2 lg:hidden">
            <Nav inboxCount={counts.todo} orientation="horizontal" />
          </div>
        </div>
        <main className="mx-auto max-w-7xl px-4 py-8 sm:px-8">{children}</main>
      </div>
    </div>
  );
}
