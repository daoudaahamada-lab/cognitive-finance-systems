import type { Metadata } from "next";
import { BRAND } from "@/lib/brand";
import { LegalPage } from "../legal";

export const metadata: Metadata = { title: "Politique de confidentialité" };

export default function PrivacyPage() {
  return (
    <LegalPage title="Politique de confidentialité" updated="[date]">
      <section>
        <h2>Responsable du traitement</h2>
        <p>[Raison sociale], [adresse], joignable à {BRAND.supportEmail}, est responsable des traitements liés à votre compte {BRAND.name}.</p>
        <p>
          Pour les données des prospects que vous traitez avec le service, vous êtes responsable du traitement et {BRAND.name} agit comme sous-traitant, dans le cadre d&apos;un accord de
          traitement des données (article 28 du RGPD).
        </p>
      </section>
      <section>
        <h2>Données traitées</h2>
        <ul>
          <li>Votre compte : nom, adresse e-mail, mot de passe chiffré, paramètres de votre espace.</li>
          <li>Les profils professionnels de vos prospects : nom, poste, entreprise, secteur, zone, URL de profil.</li>
          <li>Les messages échangés avec vos prospects et l&apos;historique des actions.</li>
        </ul>
      </section>
      <section>
        <h2>Finalités et bases légales</h2>
        <ul>
          <li>Fournir le service (exécution du contrat).</li>
          <li>Prospecter des professionnels pour le compte de nos clients (intérêt légitime du client, qui doit informer les personnes et respecter leur droit d&apos;opposition).</li>
          <li>Sécuriser et améliorer le service (intérêt légitime).</li>
        </ul>
      </section>
      <section>
        <h2>Sous-traitants</h2>
        <p>
          [Hébergeur] pour l&apos;hébergement. Anthropic, pour l&apos;analyse des profils et la rédaction des messages par Claude lorsque cette fonction est active : les données nécessaires
          à chaque requête lui sont transmises. [Fournisseur d&apos;accès LinkedIn], pour l&apos;envoi des invitations et des messages. [Liste à compléter, avec les garanties en cas de
          transfert hors de l&apos;Union européenne.]
        </p>
      </section>
      <section>
        <h2>Durées de conservation</h2>
        <p>[À préciser : durée de conservation des comptes, des prospects et des conversations, et suppression à la fermeture du compte.]</p>
      </section>
      <section>
        <h2>Vos droits</h2>
        <p>
          Vous pouvez accéder à vos données, les rectifier, les effacer, en limiter le traitement, vous y opposer et demander leur portabilité en écrivant à {BRAND.supportEmail}. Vous pouvez
          aussi saisir la CNIL. Lorsqu&apos;un prospect demande l&apos;arrêt des messages ou la suppression de ses données, le setter ne lui répond jamais automatiquement : la demande est
          transmise au client.
        </p>
      </section>
    </LegalPage>
  );
}
