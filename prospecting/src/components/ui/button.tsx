import Link from "next/link";
import type { ComponentProps } from "react";
import { cn } from "@/lib/cn";

const VARIANTS = {
  primary: "bg-brand-600 text-white hover:bg-brand-700 shadow-sm disabled:bg-brand-600/60",
  secondary: "bg-surface text-ink border border-line hover:bg-canvas shadow-sm",
  ghost: "text-muted hover:text-ink hover:bg-canvas",
  danger: "bg-surface text-red-700 border border-red-200 hover:bg-red-50",
  success: "bg-emerald-600 text-white hover:bg-emerald-700 shadow-sm",
} as const;

const SIZES = {
  sm: "h-8 px-3 text-xs gap-1.5",
  md: "h-9 px-4 text-sm gap-2",
} as const;

type Style = { variant?: keyof typeof VARIANTS; size?: keyof typeof SIZES };

export function buttonClass({ variant = "primary", size = "md" }: Style = {}, className?: string) {
  return cn(
    "inline-flex items-center justify-center whitespace-nowrap rounded-lg font-medium transition-colors",
    "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-500 disabled:cursor-not-allowed",
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
