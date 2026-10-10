import type { Metadata } from "next";
import { BRAND } from "@/lib/brand";
import { LegalPage } from "../legal";

export const metadata: Metadata = { title: "Mentions légales" };

export default function LegalNoticePage() {
  return (
    <LegalPage title="Mentions légales" updated="[date]">
      <section>
        <h2>Éditeur</h2>
        <p>
          Le service {BRAND.name} est édité par [raison sociale], [forme juridique] au capital de [montant] €, immatriculée au RCS de [ville] sous le numéro [SIREN], dont le siège est situé
          [adresse]. Numéro de TVA intracommunautaire : [numéro].
        </p>
        <p>Directeur de la publication : [nom]. Contact : {BRAND.supportEmail}.</p>
      </section>
      <section>
        <h2>Hébergement</h2>
        <p>Le service est hébergé par [hébergeur], [adresse], [téléphone].</p>
      </section>
      <section>
        <h2>Marques</h2>
        <p>
          LinkedIn est une marque de LinkedIn Corporation. {BRAND.name} n&apos;est ni affilié à LinkedIn, ni approuvé par LinkedIn. Claude est une marque d&apos;Anthropic.
        </p>
      </section>
    </LegalPage>
  );
}
