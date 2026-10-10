import { TEST_DATABASE_URL } from "./global-setup";

// Must run before anything imports the Prisma client.
process.env.DATABASE_URL = TEST_DATABASE_URL;
process.env.TIME_SCALE = "1";
