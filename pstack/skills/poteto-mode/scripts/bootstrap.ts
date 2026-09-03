import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import { join } from "node:path";

const scriptsDirectory = import.meta.dirname;
const nodeModulesDirectory = join(scriptsDirectory, "node_modules");
const commanderPackagePath = join(
  nodeModulesDirectory,
  "commander",
  "package.json"
);
export function ensureDependenciesInstalled(): void {
  if (existsSync(commanderPackagePath)) return;

  const npm = process.platform === "win32" ? "npm.cmd" : "npm";
  const result = spawnSync(
    npm,
    ["install", "--ignore-scripts", "--no-audit", "--no-fund", "--package-lock=false"],
    { cwd: scriptsDirectory, encoding: "utf8" }
  );
  if (result.status !== 0) {
    process.stdout.write(result.stdout ?? "");
    process.stderr.write(result.stderr ?? "");
    throw new Error(
      `npm install exited with status ${result.status ?? "unknown"}`
    );
  }
  if (!existsSync(commanderPackagePath)) {
    throw new Error(
      "npm install completed without installing commander"
    );
  }

}
