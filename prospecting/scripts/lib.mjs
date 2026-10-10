// Helpers shared by `npm run setup` and `npm run local` (plain Node: they run before any dependency is installed).
import { spawnSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import net from "node:net";

export const windows = process.platform === "win32";

/** Runs a command in this terminal; npm, npx and docker are .cmd/.exe wrappers on Windows. */
export function run(command, args, { quiet = false } = {}) {
  return spawnSync(command, args, { stdio: quiet ? "ignore" : "inherit", shell: windows }).status === 0;
}

export function fail(message) {
  console.error(`\n✗ ${message}\n`);
  process.exit(1);
}

/** A setting from the environment or from .env. */
export function setting(name) {
  if (process.env[name]) return process.env[name];
  const env = existsSync(".env") ? readFileSync(".env", "utf8") : "";
  return new RegExp(`^${name}\\s*=\\s*"?([^"\\n]*)"?`, "m").exec(env)?.[1] || undefined;
}

/** Host and port of DATABASE_URL (the docker compose database by default). */
export function databaseAddress() {
  const url = setting("DATABASE_URL") ?? "postgresql://vela:vela@localhost:5432/vela";
  try {
    const { hostname, port } = new URL(url);
    return { host: hostname || "localhost", port: Number(port || 5432) };
  } catch {
    return { host: "localhost", port: 5432 };
  }
}

export function reachable({ host, port }, timeoutMs = 1500) {
  return new Promise((resolve) => {
    const socket = net.connect({ host, port });
    const done = (ok) => {
      socket.destroy();
      resolve(ok);
    };
    socket.setTimeout(timeoutMs, () => done(false));
    socket.once("connect", () => done(true));
    socket.once("error", () => done(false));
  });
}

/** Uses a database that is already running, or starts the docker compose one. */
export async function ensureDatabase() {
  const address = databaseAddress();
  if (await reachable(address)) return;
  if (!run("docker", ["info"], { quiet: true })) {
    fail(
      "La base de données ne tourne pas et Docker ne répond pas.\n" +
        "  Installez Docker Desktop (https://www.docker.com/products/docker-desktop/), ouvrez-le,\n" +
        "  attendez qu'il indique « Engine running », puis relancez cette commande.",
    );
  }
  if (!run("docker", ["compose", "up", "-d"])) fail("Docker n'a pas pu démarrer la base de données (voir le message ci-dessus).");
  for (let i = 0; i < 60; i++) {
    if (await reachable(address)) return;
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }
  fail(`La base de données ne répond pas sur ${address.host}:${address.port}.`);
}
