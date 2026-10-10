import { execSync } from "node:child_process";

export const TEST_DATABASE_URL = process.env.TEST_DATABASE_URL ?? "postgresql://vela:vela@localhost:5432/vela_test";

/** Syncs the test schema once per run (non-destructive; tests truncate their own data). */
export default function setup() {
  assertTestDatabase(TEST_DATABASE_URL);
  execSync("npx prisma db push --skip-generate", {
    env: { ...process.env, DATABASE_URL: TEST_DATABASE_URL },
    stdio: "pipe",
  });
}

/** Tests wipe tables: refuse to touch anything that is not clearly a test database. */
export function assertTestDatabase(url: string) {
  const name = new URL(url).pathname.replace(/^\//, "");
  if (!name.endsWith("_test")) {
    throw new Error(`Refusing to run tests against "${name}": the database name must end with "_test".`);
  }
}
