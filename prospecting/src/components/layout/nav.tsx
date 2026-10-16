"use client";

import { CalendarCheck, Ellipsis, Inbox, LayoutDashboard, LogOut, Megaphone, Plug, Settings, Users, type LucideIcon } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useRef, type KeyboardEvent } from "react";
import { logoutAction } from "@/app/(auth)/actions";
import { cn } from "@/lib/cn";
import { formatNumber } from "@/lib/format";

type NavItem = { href: string; label: string; short: string; icon: LucideIcon; badge?: "inbox" };

const ITEMS: NavItem[] = [
  { href: "/dashboard", label: "Tableau de bord", short: "Accueil", icon: LayoutDashboard },
  { href: "/inbox", label: "Boîte de réception", short: "Boîte", icon: Inbox, badge: "inbox" },
  { href: "/campaigns", label: "Campagnes", short: "Campagnes", icon: Megaphone },
  { href: "/prospects", label: "Prospects", short: "Prospects", icon: Users },
  { href: "/meetings", label: "Rendez-vous", short: "Rendez-vous", icon: CalendarCheck },
  { href: "/accounts", label: "Comptes LinkedIn", short: "Comptes", icon: Plug },
  { href: "/settings", label: "Réglages", short: "Réglages", icon: Settings },
];

/** Tabs of the mobile bar; the other sections live under "Plus". */
const TAB_COUNT = 4;

const isActive = (pathname: string, href: string) => pathname === href || pathname.startsWith(`${href}/`);

function CountPill({ count, className }: { count: number; className?: string }) {
  return (
    <span className={cn("rounded-full bg-brand-600 px-1.5 py-0.5 text-2xs font-semibold leading-none text-white tabular-nums", className)}>
      {formatNumber(count)}
      <span className="sr-only"> à traiter</span>
    </span>
  );
}

/** Sidebar navigation (lg and up). */
export function Nav({ inboxCount, orientation = "vertical" }: { inboxCount: number; orientation?: "vertical" | "horizontal" }) {
  const pathname = usePathname();
  return (
    <nav aria-label="Navigation principale" className={cn(orientation === "vertical" ? "space-y-0.5" : "flex gap-1 overflow-x-auto")}>
      {ITEMS.map(({ href, label, icon: Icon, badge }) => {
        const active = isActive(pathname, href);
        return (
          <Link
            key={href}
            href={href}
            aria-current={active ? "page" : undefined}
            className={cn(
              "flex items-center gap-2.5 rounded-control px-3 py-2 text-sm font-medium whitespace-nowrap transition-colors",
              active ? "bg-brand-50 text-brand-700" : "text-muted hover:bg-canvas hover:text-ink",
            )}
          >
            <Icon className="size-4 shrink-0" aria-hidden />
            <span className="flex-1">{label}</span>
            {badge === "inbox" && inboxCount > 0 ? <CountPill count={inboxCount} /> : null}
          </Link>
        );
      })}
    </nav>
  );
}

const tabClass = (active: boolean) =>
  cn(
    "relative flex min-h-14 w-full flex-col items-center justify-center gap-0.5 text-2xs font-medium transition-colors",
    "focus-visible:outline-2 focus-visible:-outline-offset-2 focus-visible:outline-brand-600",
    active ? "text-brand-700" : "text-muted hover:text-ink",
  );

/** Fixed bottom tab bar below lg: four sections, the rest and logout under "Plus". */
export function BottomNav({ inboxCount }: { inboxCount: number }) {
  const pathname = usePathname();
  const more = useRef<HTMLDetailsElement>(null);
  const tabs = ITEMS.slice(0, TAB_COUNT);
  const extra = ITEMS.slice(TAB_COUNT);
  const moreActive = extra.some((item) => isActive(pathname, item.href));

  // Close the sheet once a link inside it has been followed.
  useEffect(() => {
    if (more.current) more.current.open = false;
  }, [pathname]);

  const close = () => {
    if (more.current) more.current.open = false;
  };
  const onKeyDown = (e: KeyboardEvent<HTMLDetailsElement>) => {
    if (e.key === "Escape" && more.current?.open) {
      close();
      more.current.querySelector("summary")?.focus();
    }
  };

  return (
    <nav aria-label="Navigation principale" className="fixed inset-x-0 bottom-0 z-30 border-t border-line bg-surface pr-[env(safe-area-inset-right)] pb-[env(safe-area-inset-bottom)] pl-[env(safe-area-inset-left)] lg:hidden">
      <ul className="grid grid-cols-5">
        {tabs.map(({ href, short, icon: Icon, badge }) => {
          const active = isActive(pathname, href);
          return (
            <li key={href}>
              <Link href={href} aria-current={active ? "page" : undefined} className={tabClass(active)}>
                <span className="relative">
                  <Icon className="size-5" aria-hidden />
                  {badge === "inbox" && inboxCount > 0 ? <CountPill count={inboxCount} className="absolute -right-3 -top-1.5 ring-2 ring-surface" /> : null}
                </span>
                {short}
              </Link>
            </li>
          );
        })}
        <li>
          <details ref={more} onKeyDown={onKeyDown}>
            <summary className={cn(tabClass(moreActive), "cursor-pointer list-none [&::-webkit-details-marker]:hidden")}>
              <Ellipsis className="size-5" aria-hidden />
              Plus
            </summary>
            <div aria-hidden className="fixed inset-0 bottom-(--mobile-nav-h) bg-ink/20" onClick={close} />
            <div className="fixed right-[max(0.75rem,env(safe-area-inset-right))] bottom-[calc(var(--mobile-nav-h)+0.5rem)] left-[max(0.75rem,env(safe-area-inset-left))] rounded-card border border-line bg-surface p-1.5 shadow-pop">
              <ul>
                {extra.map(({ href, label, icon: Icon }) => {
                  const active = isActive(pathname, href);
                  return (
                    <li key={href}>
                      <Link
                        href={href}
                        onClick={close}
                        aria-current={active ? "page" : undefined}
                        className={cn(
                          "flex min-h-12 items-center gap-3 rounded-control px-3 text-base font-medium",
                          active ? "bg-brand-50 text-brand-700" : "text-ink hover:bg-canvas",
                        )}
                      >
                        <Icon className="size-5 shrink-0" aria-hidden />
                        {label}
                      </Link>
                    </li>
                  );
                })}
                <li className="mt-1 border-t border-line pt-1">
                  <form action={logoutAction}>
                    <button type="submit" className="flex min-h-12 w-full items-center gap-3 rounded-control px-3 text-base font-medium text-ink hover:bg-canvas">
                      <LogOut className="size-5 shrink-0 text-muted" aria-hidden />
                      Se déconnecter
                    </button>
                  </form>
                </li>
              </ul>
            </div>
          </details>
        </li>
      </ul>
    </nav>
  );
}
