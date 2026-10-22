import { PurgeCSS } from "purgecss";
import fs from "node:fs";
const cfg = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const [r] = await new PurgeCSS().purge(cfg);
fs.writeFileSync(cfg.output, r.css);
