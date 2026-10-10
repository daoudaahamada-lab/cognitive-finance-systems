import type { ReactNode } from "react";
import { Logo } from "@/components/layout/logo";
import { BRAND } from "@/lib/brand";

export default function AuthLayout({ children }: { children: ReactNode }) {
  return (
    <main className="grid min-h-screen lg:grid-cols-2">
      <div className="flex flex-col justify-center px-4 py-12 sm:px-12">
        <div className="mx-auto w-full max-w-sm">
          <Logo />
          <div className="mt-10">{children}</div>
        </div>
      </div>
      <aside className="hidden flex-col justify-center bg-brand-900 px-14 text-white lg:flex">
        <p className="text-sm font-medium uppercase tracking-widest text-brand-200">{BRAND.tagline}</p>
        <h2 className="mt-4 max-w-md text-3xl font-semibold leading-tight">
          Il trouve vos prospects, lance la conversation et réserve les rendez-vous.
        </h2>
        <ul className="mt-8 space-y-3 text-sm text-brand-100">
          <li>• Ciblage par critères, signaux d&apos;achat et engagement</li>
          <li>• Invitations et relances dans les limites de sécurité LinkedIn</li>
          <li>• Setter qui répond, gère les objections et vous passe la main</li>
        </ul>
      </aside>
    </main>
  );
}
