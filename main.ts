import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Entry point for the news-image-20261118 bounty.
// The poster itself is the file entry.png next to this script.
// This program only copies that file into the output directory,
// so it needs no network and produces identical bytes every run.

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });

if (!existsSync(source)) {
  console.error(`entry.png not found next to main.ts at ${source}`);
  process.exit(1);
}

const destination = join(outDir, "entry.png");
copyFileSync(source, destination);

// The copy must be exact: same byte count in, same byte count out.
if (statSync(source).size !== statSync(destination).size) {
  console.error(`copy mismatch: ${source} and ${destination} differ in size`);
  process.exit(1);
}
console.log(`Wrote ${destination} (${statSync(destination).size} bytes)`);
