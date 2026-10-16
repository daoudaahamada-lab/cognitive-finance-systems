import {
  Ban, CalendarCheck, Circle, Clock, Hand, MessageCircle, PenLine, Repeat, Reply, Search, Send, Sparkles, Star,
  ThumbsDown, TriangleAlert, UserCheck, UserPlus, X, type LucideIcon,
} from "lucide-react";
import type { ReactNode } from "react";
import { cn } from "@/lib/cn";
import { ACTIVITY_VISUALS, type ActivityIconName, type SemanticTone, type Tone } from "@/lib/labels";
import { toneClasses } from "@/lib/tones";

export const ACTIVITY_ICONS: Record<ActivityIconName, LucideIcon> = {
  search: Search,
  star: Star,
  ban: Ban,
  "user-plus": UserPlus,
  "user-check": UserCheck,
  send: Send,
  repeat: Repeat,
  "message-circle": MessageCircle,
  sparkles: Sparkles,
  reply: Reply,
  "pen-line": PenLine,
  x: X,
  hand: Hand,
  "calendar-check": CalendarCheck,
  "thumbs-down": ThumbsDown,
  clock: Clock,
  alert: TriangleAlert,
};

/** Icon component and tone for an ActivityType (ACTIVITY_VISUALS in lib/labels). */
export function activityVisual(type: string): { icon: LucideIcon; tone: SemanticTone } {
  const visual = ACTIVITY_VISUALS[type];
  return visual ? { icon: ACTIVITY_ICONS[visual.icon], tone: visual.tone } : { icon: Circle, tone: "neutral" };
}

export type TimelineItem = {
  /** React key; defaults to the position. */
  id?: string;
  icon: LucideIcon;
  tone?: Tone;
  title: ReactNode;
  meta?: ReactNode;
  body?: ReactNode;
};

/** Vertical history: 24px tone circles joined by a line. */
export function Timeline({ items, className }: { items: TimelineItem[]; className?: string }) {
  return (
    <ol className={cn("min-w-0", className)}>
      {items.map((item, i) => {
        const Icon = item.icon;
        return (
          <li key={item.id ?? i} className="relative flex gap-3 pb-4 last:pb-0">
            {i < items.length - 1 ? <span aria-hidden className="absolute bottom-0 left-3 top-6 w-px -translate-x-1/2 bg-line" /> : null}
            <span className={cn("relative flex size-6 shrink-0 items-center justify-center rounded-full ring-2 ring-surface", toneClasses(item.tone ?? "neutral").soft)}>
              <Icon className="size-3.5" aria-hidden />
            </span>
            <div className="min-w-0 flex-1 pt-0.5">
              <p className="text-sm text-ink">{item.title}</p>
              {item.meta ? <p className="text-xs text-muted">{item.meta}</p> : null}
              {item.body ? <div className="mt-1 text-sm text-ink-2">{item.body}</div> : null}
            </div>
          </li>
        );
      })}
    </ol>
  );
}
