import type { Campaign, LinkedInAccount, Prospect, Workspace } from "@prisma/client";
import type { TemplateVars } from "@/server/domain/templates";

export function templateVars(
  prospect: Pick<Prospect, "firstName" | "lastName" | "company" | "title" | "industry" | "location">,
  account: Pick<LinkedInAccount, "fullName">,
  campaign: Pick<Campaign, "bookingUrl">,
  workspace: Pick<Workspace, "bookingUrl">,
): TemplateVars {
  return {
    firstName: prospect.firstName,
    lastName: prospect.lastName,
    company: prospect.company,
    title: prospect.title,
    industry: prospect.industry,
    location: prospect.location,
    senderFirstName: account.fullName.split(" ")[0] ?? account.fullName,
    bookingUrl: campaign.bookingUrl || workspace.bookingUrl,
  };
}
