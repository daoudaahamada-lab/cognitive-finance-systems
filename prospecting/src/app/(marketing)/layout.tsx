import Link from "next/link";
import type { ReactNode } from "react";
import { Logo } from "@/components/layout/logo";
import { ButtonLink } from "@/components/ui/button";
import { BRAND } from "@/lib/brand";

const NAV = [
  { href: "/#fonctionnement", label: "Fonctionnement" },
  { href: "/#setter", label: "Setter IA" },
  { href: "/#securite", label: "Sécurité" },
  { href: "/tarifs", label: "Tarifs" },
  { href: "/#faq", label: "FAQ" },
];

export default function MarketingLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-surface">
      <header className="sticky top-0 z-20 border-b border-line/70 bg-surface/85 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3 sm:px-6">
          <Link href="/" aria-label={`${BRAND.name}, accueil`}>
            <Logo />
          </Link>
          <nav aria-label="Navigation du site" className="hidden items-center gap-6 text-sm text-muted md:flex">
            {NAV.map((item) => (
              <Link key={item.href} href={item.href} className="hover:text-ink">
                {item.label}
              </Link>
            ))}
          </nav>
          <div className="flex items-center gap-2">
            <Link href="/login" className="hidden px-2 text-sm font-medium text-muted hover:text-ink sm:inline">
              Se connecter
            </Link>
            <ButtonLink href="/signup" size="sm">Essai gratuit</ButtonLink>
          </div>
        </div>
      </header>

      <main>{children}</main>

      <footer className="border-t border-line bg-canvas">
        <div className="mx-auto grid max-w-6xl gap-8 px-4 py-12 sm:px-6 md:grid-cols-[2fr_1fr_1fr]">
          <div className="space-y-3">
            <Logo />
            <p className="max-w-sm text-sm text-muted">{BRAND.tagline}. Il trouve vos prospects, lance la conversation et réserve vos rendez-vous.</p>
            <p className="text-xs text-muted">{BRAND.name} n&apos;est ni affilié à LinkedIn, ni approuvé par LinkedIn.</p>
          </div>
          <FooterColumn title="Produit" links={[["/#fonctionnement", "Fonctionnement"], ["/#setter", "Setter IA"], ["/tarifs", "Tarifs"], ["/signup", "Essai gratuit"]]} />
          <FooterColumn title="Légal" links={[["/mentions-legales", "Mentions légales"], ["/confidentialite", "Confidentialité"], ["/cgu", "Conditions d'utilisation"]]} />
        </div>
        <p className="border-t border-line py-4 text-center text-xs text-muted">© {new Date().getFullYear()} {BRAND.name}</p>
      </footer>
    </div>
  );
}

function FooterColumn({ title, links }: { title: string; links: [string, string][] }) {
  return (
    <div>
      <p className="text-sm font-semibold">{title}</p>
      <ul className="mt-3 space-y-2 text-sm text-muted">
        {links.map(([href, label]) => (
          <li key={href}>
            <Link href={href} className="hover:text-ink">{label}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
