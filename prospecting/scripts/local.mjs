// Starts everything on your own computer: database, app (http://localhost:3000) and the LinkedIn worker.
//   npm run local        Ctrl+C stops everything.
import { spawn, spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import { ensureDatabase, fail, windows } from "./lib.mjs";

if (!existsSync("node_modules") || !existsSync(".env")) fail("Vela n'est pas encore installé : lancez d'abord « npm run setup ».");
await ensureDatabase();

let appUrl = "http://localhost:3000";

const processes = [
  { name: "app", args: ["run", "dev"] },
  { name: "worker", args: ["run", "worker"] },
].map(({ name, args }) => {
  // Own process group on Mac/Linux, so stopping it also stops what npm started.
  const child = spawn("npm", args, { shell: windows, detached: !windows, stdio: ["ignore", "pipe", "pipe"] });
  for (const stream of [child.stdout, child.stderr]) {
    let pending = "";
    stream.setEncoding("utf8");
    stream.on("data", (chunk) => {
      pending += chunk;
      const lines = pending.split(/\r?\n/);
      pending = lines.pop() ?? "";
      for (const line of lines) {
        if (line.trim()) console.log(`[${name}] ${line}`);
        // Next.js picks another port when 3000 is taken: show the one it chose.
        appUrl = /Local:\s+(https?:\/\/\S+)/.exec(line)?.[1] ?? appUrl;
        if (name === "app" && /Ready in/.test(line)) console.log(`\n→ Vela est prêt : ouvrez ${appUrl} dans votre navigateur.\n`);
      }
    });
  }
  return { name, child };
});

let stopping = false;
function stopAll(code) {
  if (stopping) return;
  stopping = true;
  for (const { child } of processes) {
    if (child.exitCode !== null) continue;
    try {
      if (windows) spawnSync("taskkill", ["/pid", String(child.pid), "/T", "/F"], { stdio: "ignore" });
      else process.kill(-child.pid, "SIGTERM");
    } catch {
      // Already gone.
    }
  }
  // Wait until every process npm started is gone (the worker closes its browsers first),
  // so a restart finds the ports and browser profiles free. taskkill already waited on Windows.
  const deadline = Date.now() + 15_000;
  const running = ({ child }) => {
    try {
      process.kill(-child.pid, 0);
      return true;
    } catch {
      return false;
    }
  };
  const check = () => {
    if (windows || !processes.some(running) || Date.now() > deadline) process.exit(code);
    setTimeout(check, 200);
  };
  check();
}

for (const { name, child } of processes) {
  child.on("exit", (code) => {
    if (stopping) return;
    console.error(`\n✗ ${name === "app" ? "L'application" : "Le worker LinkedIn"} s'est arrêté (code ${code}) : arrêt de Vela.`);
    stopAll(code ?? 1);
  });
}
process.on("SIGINT", () => stopAll(0));
process.on("SIGTERM", () => stopAll(0));

console.log("Démarrage de Vela (Ctrl+C pour tout arrêter)…");
