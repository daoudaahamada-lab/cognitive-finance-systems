import { BRAND } from "@/lib/brand";

export function Logo() {
  return (
    <span className="inline-flex items-center gap-2 font-semibold tracking-tight text-ink">
      <svg viewBox="0 0 24 24" className="size-6" aria-hidden>
        <rect width="24" height="24" rx="7" className="fill-brand-600" />
        <path d="M7 7.5l5 9 5-9" fill="none" stroke="white" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
      {BRAND.name}
    </span>
  );
}
