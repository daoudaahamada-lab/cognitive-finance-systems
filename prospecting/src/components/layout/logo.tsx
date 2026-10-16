import { BRAND } from "@/lib/brand";
import { cn } from "@/lib/cn";

/** Sail glyph, alone or with the product name. */
export function LogoMark({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" className={cn("size-6 shrink-0 text-brand-600", className)} aria-hidden>
      <path d="M11 2.5V16H3.5z" fill="currentColor" />
      <path d="M13 6v10h6.5z" fill="currentColor" opacity="0.55" />
      <path d="M3 18h18l-2.2 3.5H5.2z" fill="currentColor" />
    </svg>
  );
}

export function Logo() {
  return (
    <span className="inline-flex items-center gap-2 font-semibold tracking-tight text-ink">
      <LogoMark />
      {BRAND.name}
    </span>
  );
}
