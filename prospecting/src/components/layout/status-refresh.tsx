"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";

/**
 * Layouts do not re-render on navigation: refresh the route every minute so the header
 * (engine state, inbox count, account banners) follows the worker. Skipped while the tab
 * is hidden or the user is typing.
 */
export function StatusRefresh({ intervalMs = 60_000 }: { intervalMs?: number }) {
  const router = useRouter();
  useEffect(() => {
    const timer = setInterval(() => {
      const el = document.activeElement;
      const typing = el instanceof HTMLElement && (el.isContentEditable || ["INPUT", "TEXTAREA", "SELECT"].includes(el.tagName));
      if (document.visibilityState === "visible" && !typing) router.refresh();
    }, intervalMs);
    return () => clearInterval(timer);
  }, [router, intervalMs]);
  return null;
}
