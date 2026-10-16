import Link from "next/link";
import type { ComponentProps } from "react";
import { cn } from "@/lib/cn";

const VARIANTS = {
  primary: "bg-brand-600 text-white hover:bg-brand-700 shadow-card disabled:bg-brand-600/60",
  secondary: "bg-surface text-ink border border-line hover:border-line-strong hover:bg-surface-2",
  ghost: "text-muted hover:text-ink hover:bg-canvas",
  danger: "bg-surface text-danger border border-danger-line hover:bg-danger-soft",
  success: "bg-success text-white hover:bg-success/90 shadow-card disabled:bg-success/60",
} as const;

const SIZES = {
  sm: "h-8 px-3 text-xs gap-1.5 pointer-coarse:h-11",
  md: "h-9 px-4 text-sm gap-2 pointer-coarse:h-11",
  lg: "h-11 px-5 text-base gap-2",
  /** Square icon button: give it an aria-label. */
  icon: "size-9 shrink-0 pointer-coarse:size-11",
} as const;

export type ButtonVariant = keyof typeof VARIANTS;
export type ButtonSize = keyof typeof SIZES;
type Style = { variant?: ButtonVariant; size?: ButtonSize };

export function buttonClass({ variant = "primary", size = "md" }: Style = {}, className?: string) {
  return cn(
    "inline-flex items-center justify-center whitespace-nowrap rounded-control font-medium transition-colors",
    "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-600 disabled:cursor-not-allowed",
    VARIANTS[variant],
    SIZES[size],
    className,
  );
}

export function Button({ variant, size, className, type = "button", ...props }: ComponentProps<"button"> & Style) {
  return <button type={type} className={buttonClass({ variant, size }, className)} {...props} />;
}

export function ButtonLink({ variant, size, className, ...props }: ComponentProps<typeof Link> & Style) {
  return <Link className={buttonClass({ variant, size }, className)} {...props} />;
}
