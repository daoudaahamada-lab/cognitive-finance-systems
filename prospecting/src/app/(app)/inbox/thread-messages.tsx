"use client";

import { useLayoutEffect, useRef, type ReactNode } from "react";
import { cn } from "@/lib/cn";

/** Below lg (Tailwind's 64rem) the thread flows in the page instead of scrolling inside the card. */
const FLOWING = "(max-width: 63.99rem)";

/**
 * The message list of a thread: opens on the latest message, and follows new ones.
 * From lg it is its own scroll area; below lg the page scrolls, so the latest message lands right above the pinned reply box.
 */
export function ThreadMessages({ threadId, count, className, children }: { threadId: string; count: number; className?: string; children: ReactNode }) {
  const list = useRef<HTMLOListElement>(null);
  useLayoutEffect(() => {
    const el = list.current;
    if (!el) return;
    el.scrollTop = el.scrollHeight;
    if (!window.matchMedia(FLOWING).matches) return;
    // Next.js restores the top of the page after this effect on navigation: scroll on the next frame, still before paint.
    const frame = requestAnimationFrame(() => window.scrollTo({ top: document.documentElement.scrollHeight, behavior: "instant" }));
    return () => cancelAnimationFrame(frame);
  }, [threadId, count]);
  return (
    <ol
      ref={list}
      // Focusable so keyboard users can scroll the history.
      tabIndex={0}
      aria-label="Messages"
      className={cn("focus-visible:outline-2 focus-visible:-outline-offset-2 focus-visible:outline-brand-600", className)}
    >
      {children}
    </ol>
  );
}
