import { redirect } from "next/navigation";
import { cache } from "react";
import { db } from "@/server/db";
import { currentUser } from "./session";

/** The signed-in user and their workspace; redirects to /login otherwise. Cached per request. */
export const requireContext = cache(async () => {
  const user = await currentUser();
  if (!user) redirect("/login");
  const membership = await db.membership.findFirst({
    where: { userId: user.id },
    include: { workspace: true },
    orderBy: { createdAt: "asc" },
  });
  if (!membership) redirect("/login");
  return { user, workspace: membership.workspace, role: membership.role };
});

export type AppContext = Awaited<ReturnType<typeof requireContext>>;
