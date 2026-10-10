import { ButtonLink } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/misc";

export default function NotFound() {
  return (
    <Card>
      <EmptyState title="Introuvable" description="Cette page n'existe pas ou n'appartient pas à votre espace." action={<ButtonLink href="/dashboard">Retour au tableau de bord</ButtonLink>} />
    </Card>
  );
}
