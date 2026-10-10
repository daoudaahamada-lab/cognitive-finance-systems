import { z } from "zod";
import { db } from "@/server/db";
import { TRIAL_DAYS } from "@/server/domain/plans";
import { DAY } from "@/server/domain/time";
import { hashPassword, verifyPassword } from "@/server/auth/password";
import { UserError } from "./errors";

export const signupSchema = z.object({
  name: z.string().trim().min(1, "Indiquez votre nom").max(100),
  email: z.email("Email invalide").transform((e) => e.toLowerCase()),
  password: z.string().min(8, "8 caractères minimum").max(200),
  company: z.string().trim().min(1, "Indiquez le nom de votre entreprise").max(100),
});

export async function signup(input: z.infer<typeof signupSchema>) {
  const existing = await db.user.findUnique({ where: { email: input.email } });
  if (existing) throw new UserError("Un compte existe déjà avec cet email.");
  const passwordHash = await hashPassword(input.password);
  return db.user.create({
    data: {
      email: input.email,
      name: input.name,
      passwordHash,
      memberships: {
        create: {
          role: "OWNER",
          workspace: {
            create: { name: input.company, plan: "PRO", trialEndsAt: new Date(Date.now() + TRIAL_DAYS * DAY) },
          },
        },
      },
    },
  });
}

export const loginSchema = z.object({
  email: z.email("Email invalide").transform((e) => e.toLowerCase()),
  password: z.string().min(1, "Mot de passe requis"),
});

let dummyHash: Promise<string> | null = null;

export async function login(input: z.infer<typeof loginSchema>) {
  const user = await db.user.findUnique({ where: { email: input.email } });
  // Hash even for unknown emails so response time does not reveal which accounts exist.
  dummyHash ??= hashPassword("not-a-real-password");
  const valid = await verifyPassword(input.password, user?.passwordHash ?? (await dummyHash));
  if (!user || !valid) throw new UserError("Email ou mot de passe incorrect.");
  return user;
}
