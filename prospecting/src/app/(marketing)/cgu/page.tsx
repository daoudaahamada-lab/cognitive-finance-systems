import type { Metadata } from "next";
import { BRAND } from "@/lib/brand";
import { PRICING } from "@/lib/pricing";
import { LegalPage } from "../legal";

export const metadata: Metadata = { title: "Conditions d'utilisation" };

export default function TermsPage() {
  return (
    <LegalPage title="Conditions générales d'utilisation" updated="[date]">
      <section>
        <h2>Objet</h2>
        <p>
          Les présentes conditions encadrent l&apos;utilisation du service {BRAND.name}, logiciel de prospection commerciale sur LinkedIn, édité par [raison sociale].
        </p>
      </section>
      <section>
        <h2>Essai et abonnement</h2>
        <p>
          L&apos;essai gratuit dure {PRICING.trialDays} jours, sans moyen de paiement. Les abonnements sont mensuels ou annuels, aux prix affichés sur la page Tarifs. [Conditions de
          renouvellement, de résiliation et de remboursement à préciser.]
        </p>
      </section>
      <section>
        <h2>Utilisation de LinkedIn</h2>
        <p>
          Les conditions d&apos;utilisation de LinkedIn interdisent l&apos;usage d&apos;outils d&apos;automatisation tiers. Le client utilise le service sous sa responsabilité et reconnaît
          qu&apos;un compte LinkedIn peut être restreint malgré les limites de sécurité appliquées par le service.
        </p>
      </section>
      <section>
        <h2>Obligations du client</h2>
        <ul>
          <li>Prospecter dans le respect du RGPD et des règles applicables à la prospection B2B.</li>
          <li>Ne pas envoyer de contenu illicite, trompeur ou non sollicité de manière abusive.</li>
          <li>Relire les paramètres du setter et en rester responsable : en mode automatique, les réponses sont envoyées en son nom.</li>
        </ul>
      </section>
      <section>
        <h2>Responsabilité</h2>
        <p>[Limites de responsabilité, disponibilité du service, droit applicable et juridiction compétente à préciser.]</p>
      </section>
    </LegalPage>
  );
}
