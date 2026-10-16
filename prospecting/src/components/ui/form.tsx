import { ChevronDown } from "lucide-react";
import { Fragment, cloneElement, isValidElement, type ComponentProps, type ReactElement, type ReactNode } from "react";
import { cn } from "@/lib/cn";

/** 16px text below sm so iOS Safari does not zoom on focus. Heights follow buttons: 44px on phones and touch screens. */
const control =
  "block w-full rounded-control border border-line bg-surface px-3 text-base text-ink placeholder:text-muted sm:text-sm " +
  "focus:border-brand-600 focus:outline-none focus:ring-2 focus:ring-brand-600/50 disabled:bg-canvas disabled:text-muted " +
  "aria-[invalid=true]:border-danger";

/** Native checkbox and radio styling. */
export const checkbox = "size-4 shrink-0 accent-brand-600 pointer-coarse:size-5";

export function Input({ className, ...props }: ComponentProps<"input">) {
  return <input className={cn(control, "h-11 sm:h-9 sm:pointer-coarse:h-11", className)} {...props} />;
}

export function Textarea({ className, ...props }: ComponentProps<"textarea">) {
  return <textarea className={cn(control, "py-2 leading-relaxed", className)} {...props} />;
}

/** `className` styles the wrapper (width, margins); every other prop goes to the <select>. */
export function Select({ className, ...props }: ComponentProps<"select">) {
  return (
    <span className={cn("relative block w-full", className)}>
      <select className={cn(control, "h-11 appearance-none pr-9 sm:h-9 sm:pointer-coarse:h-11")} {...props} />
      <ChevronDown className="pointer-events-none absolute right-3 top-1/2 size-4 -translate-y-1/2 text-muted" aria-hidden />
    </span>
  );
}

type Describable = { "aria-describedby"?: string; "aria-invalid"?: boolean | "true" | "false" };

export function Field({
  label,
  htmlFor,
  hint,
  error,
  children,
  className,
}: {
  label: ReactNode;
  htmlFor?: string;
  hint?: ReactNode;
  error?: string;
  children: ReactNode;
  className?: string;
}) {
  const description = error || hint ? (htmlFor ? `${htmlFor}-desc` : undefined) : undefined;
  const input =
    isValidElement<Describable>(children) && children.type !== Fragment && (description || error)
      ? cloneElement(children as ReactElement<Describable>, {
          "aria-describedby": [children.props["aria-describedby"], description].filter(Boolean).join(" ") || undefined,
          "aria-invalid": error ? true : children.props["aria-invalid"],
        })
      : children;
  return (
    <div className={cn("space-y-1.5", className)}>
      <label htmlFor={htmlFor} className="block text-sm font-medium text-ink">
        {label}
      </label>
      {input}
      {error ? (
        <p id={description} className="text-xs text-danger">
          {error}
        </p>
      ) : hint ? (
        <p id={description} className="text-xs text-muted">
          {hint}
        </p>
      ) : null}
    </div>
  );
}

export function FormMessage({ state }: { state: { error?: string; message?: string } | null }) {
  if (!state) return null;
  if (state.error) return <p role="alert" className="rounded-control border border-danger-line bg-danger-soft px-3 py-2 text-sm text-danger">{state.error}</p>;
  if (state.message) return <p role="status" className="rounded-control border border-success-line bg-success-soft px-3 py-2 text-sm text-success">{state.message}</p>;
  return null;
}
