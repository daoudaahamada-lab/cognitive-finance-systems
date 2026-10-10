import { TEST_DATABASE_URL } from "./global-setup";

// Must run before anything imports the Prisma client.
process.env.DATABASE_URL = TEST_DATABASE_URL;
process.env.TIME_SCALE = "1";
// Tests never call the real API, even if a key is configured on the machine.
process.env.AGENTS = "rules";
