"use client";

import { CalendarCheck, Inbox, LayoutDashboard, Megaphone, Plug, Settings, Users } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/cn";

const ITEMS = [
  { href: "/dashboard", label: "Tableau de bord", icon: LayoutDashboard },
  { href: "/inbox", label: "Boîte de réception", icon: Inbox, badge: "inbox" as const },
  { href: "/campaigns", label: "Campagnes", icon: Megaphone },
  { href: "/prospects", label: "Prospects", icon: Users },
  { href: "/meetings", label: "Rendez-vous", icon: CalendarCheck },
  { href: "/accounts", label: "Comptes LinkedIn", icon: Plug },
  { href: "/settings", label: "Réglages", icon: Settings },
];

export function Nav({ inboxCount, orientation }: { inboxCount: number; orientation: "vertical" | "horizontal" }) {
  const pathname = usePathname();
  return (
    <nav aria-label="Navigation principale" className={cn(orientation === "vertical" ? "space-y-0.5" : "flex gap-1 overflow-x-auto")}>
      {ITEMS.map(({ href, label, icon: Icon, badge }) => {
        const active = pathname === href || pathname.startsWith(`${href}/`);
        return (
          <Link
            key={href}
            href={href}
            aria-current={active ? "page" : undefined}
            className={cn(
              "flex items-center gap-2.5 rounded-lg px-3 py-2 text-sm font-medium whitespace-nowrap transition-colors",
              active ? "bg-brand-50 text-brand-700" : "text-muted hover:bg-canvas hover:text-ink",
            )}
          >
            <Icon className="size-4 shrink-0" aria-hidden />
            <span className="flex-1">{label}</span>
            {badge === "inbox" && inboxCount > 0 ? (
              <span className="rounded-full bg-red-600 px-1.5 py-0.5 text-[10px] font-semibold leading-none text-white tabular-nums">{inboxCount}</span>
            ) : null}
          </Link>
        );
      })}
    </nav>
  );
}
