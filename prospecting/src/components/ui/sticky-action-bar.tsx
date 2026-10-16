import type { ReactNode } from "react";
import { cn } from "@/lib/cn";

/**
 * Bar that stays at the bottom of the viewport while its form scrolls, above the mobile tab bar.
 * Place it as the last child of a form that sits directly in <main> (it bleeds into main's padding).
 */
export function StickyActionBar({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <div
      className={cn(
        "sticky bottom-(--mobile-nav-h) z-20 -mx-4 mt-6 flex flex-wrap items-center justify-end gap-3 border-t border-line bg-surface/95 px-4 py-3 backdrop-blur sm:-mx-8 sm:px-8 lg:bottom-0",
        className,
      )}
    >
      {children}
    </div>
  );
}
