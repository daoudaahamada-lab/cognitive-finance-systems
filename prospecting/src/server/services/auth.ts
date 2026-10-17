import { z } from "zod";
import { db } from "@/server/db";
import { hashPassword, verifyPassword } from "@/server/auth/password";
import { UserError } from "./errors";

export const signupSchema = z.object({
  name: z.string().trim().min(1, "Indiquez votre nom").max(100),
  email: z.email("Adresse e-mail invalide").transform((e) => e.toLowerCase()),
  password: z.string().min(8, "8 caractères minimum").max(200),
  company: z.string().trim().min(1, "Indiquez le nom de votre entreprise").max(100),
});

/**
 * Personal instance: whoever opens it first creates the account, then signup closes
 * (otherwise anyone finding the URL could use your LinkedIn sessions and Anthropic key).
 * ALLOW_SIGNUP=true reopens it.
 */
export async function signupOpen(): Promise<boolean> {
  if (process.env.ALLOW_SIGNUP === "true") return true;
  return (await db.user.count()) === 0;
}

export async function signup(input: z.infer<typeof signupSchema>) {
  if (!(await signupOpen())) throw new UserError("Les inscriptions sont fermées sur cette instance.");
  const existing = await db.user.findUnique({ where: { email: input.email } });
  if (existing) throw new UserError("Un compte existe déjà avec cette adresse e-mail.");
  const passwordHash = await hashPassword(input.password);
  return db.user.create({
    data: {
      email: input.email,
      name: input.name,
      passwordHash,
      memberships: {
        create: {
          role: "OWNER",
          workspace: { create: { name: input.company } },
        },
      },
    },
  });
}

export const loginSchema = z.object({
  email: z.email("Adresse e-mail invalide").transform((e) => e.toLowerCase()),
  password: z.string().min(1, "Mot de passe requis"),
});

let dummyHash: Promise<string> | null = null;

export async function login(input: z.infer<typeof loginSchema>) {
  const user = await db.user.findUnique({ where: { email: input.email } });
  // Hash even for unknown emails so response time does not reveal which accounts exist.
  dummyHash ??= hashPassword("not-a-real-password");
  const valid = await verifyPassword(input.password, user?.passwordHash ?? (await dummyHash));
  if (!user || !valid) throw new UserError("Adresse e-mail ou mot de passe incorrect.");
  return user;
}
