import { Briefcase, Eye, Radio, ThumbsUp, UserPlus, Zap, type LucideIcon } from "lucide-react";
import { createElement } from "react";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/cn";
import { SIGNALS } from "@/lib/labels";

/** One icon per buying signal (the label stays the text; the icon helps scanning). */
const SIGNAL_ICONS: Record<string, LucideIcon> = {
  FUNDRAISING: Zap,
  HIRING: UserPlus,
  NEW_ROLE: Briefcase,
  POST_ENGAGEMENT: ThumbsUp,
  PROFILE_VISIT: Eye,
};

export function signalLabel(signal: string): string {
  return SIGNALS[signal] ?? signal;
}

/** The signal's icon, decorative (pair it with the label or SignalIcon's sr-only text). */
export function SignalGlyph({ signal, className }: { signal: string; className?: string }) {
  return createElement(SIGNAL_ICONS[signal] ?? Radio, { className: cn("shrink-0", className), "aria-hidden": true });
}

/** Neutral chip: a signal is context, not a warning. */
export function SignalBadge({ signal, className }: { signal: string; className?: string }) {
  return (
    <Badge tone="neutral" className={className}>
      <SignalGlyph signal={signal} className="size-3" />
      {signalLabel(signal)}
    </Badge>
  );
}

/** The icon alone (board cards), with its label for screen readers and on hover. */
export function SignalIcon({ signal, className }: { signal: string; className?: string }) {
  const label = signalLabel(signal);
  return (
    <span title={label} className={cn("inline-flex shrink-0 items-center text-muted", className)}>
      <SignalGlyph signal={signal} className="size-3.5" />
      <span className="sr-only">{label}</span>
    </span>
  );
}
