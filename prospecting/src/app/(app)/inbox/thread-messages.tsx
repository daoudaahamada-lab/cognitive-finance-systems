"use client";

import { useLayoutEffect, useRef, type ReactNode } from "react";
import { cn } from "@/lib/cn";

/** The scrolling message list of a thread: opens on the latest message, and follows new ones. */
export function ThreadMessages({ threadId, count, className, children }: { threadId: string; count: number; className?: string; children: ReactNode }) {
  const list = useRef<HTMLOListElement>(null);
  useLayoutEffect(() => {
    const el = list.current;
    if (el) el.scrollTop = el.scrollHeight;
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
