// CPU-only render of the Jugnu cast v3: per character 8 transparent 1200x2000 PNGs + <id>_sheet.png, and cast_lineup.png.
// usage: npx tsx scripts/render-cast.ts [id,id,...]   (default: all)
import { createCanvas, loadImage } from "@napi-rs/canvas";
import fs from "node:fs"; import path from "node:path";
import { drawChar, POSES, CharId, Pose } from "./jugnucast";
const IDS: CharId[] = ["tinku", "bholu", "ira", "titli", "daroga", "dadi", "mummy", "chacha", "jugnu"];
// output folder/file names in channels/jugnu-stories/characters/ (code ids stay short)
const OUT: Record<CharId, string> = { tinku: "tinku", bholu: "bholu", ira: "ira", titli: "titli", daroga: "daroga_singh", dadi: "kesar_dadi", mummy: "tinku_mummy", chacha: "lon_chacha", jugnu: "jugnu" };
const NAMES: Record<CharId, string> = { tinku: "Tinku", bholu: "Bholu", ira: "Ira", titli: "Titli", daroga: "Daroga Singh", dadi: "Kesar Dadi", mummy: "Tinku ki mummy", chacha: "Lon Chacha", jugnu: "Jugnu (firefly)" };
const JUGNU_LABEL: Record<Pose, string> = { stand: "hover (side)", walk: "flying", point: "top view", think: "perched, dim", happy: "happy glow", surprised: "surprised", scared: "scared, dim", laugh: "laughing glow" };
const want = (process.argv[2]?.split(",") as CharId[]) ?? IDS;
const ROOT = path.resolve(import.meta.dirname, "..");
for (const id of want) {
  const dir = path.join(ROOT, OUT[id]); fs.mkdirSync(dir, { recursive: true });
  for (const pose of POSES) {
    const c = createCanvas(1200, 2000), g = c.getContext("2d") as any;
    g.scale(2, 2); drawChar(g, id, pose); // 600 x 1000 design canvas -> 1200 x 2000, transparent
    fs.writeFileSync(path.join(dir, `${OUT[id]}_${pose}.png`), c.toBuffer("image/png"));
  }
  // contact sheet 4 x 2
  const TW = 480, TH = 800, GAP = 24, LAB = 44, cols = 4, rows = 2;
  const sheet = createCanvas(cols * TW + (cols + 1) * GAP, rows * (TH + LAB) + (rows + 1) * GAP + 56), s = sheet.getContext("2d");
  s.fillStyle = "#efe7d6"; s.fillRect(0, 0, sheet.width, sheet.height);
  s.fillStyle = "#241726"; s.font = "bold 34px DejaVu Sans"; s.textAlign = "left"; s.fillText(NAMES[id], GAP, 42);
  for (let i = 0; i < POSES.length; i++) {
    const x = GAP + (i % cols) * (TW + GAP), y = 56 + GAP + Math.floor(i / cols) * (TH + LAB + GAP);
    s.fillStyle = "#faf5ea"; s.fillRect(x, y, TW, TH + LAB);
    s.drawImage(await loadImage(path.join(dir, `${OUT[id]}_${POSES[i]}.png`)), x, y, TW, TH);
    s.fillStyle = "#241726"; s.font = "26px DejaVu Sans"; s.textAlign = "center";
    s.fillText(id === "jugnu" ? JUGNU_LABEL[POSES[i]] : `${i < 4 ? "pose" : "expression"}: ${POSES[i]}`, x + TW / 2, y + TH + 32);
  }
  fs.writeFileSync(path.join(dir, `${OUT[id]}_sheet.png`), sheet.toBuffer("image/png"));
  console.log("wrote", id);
}
// lineup of all characters (stand pose), same canvas scale so heights compare
const LW = 340, LH = 567, G = 20, all = IDS.filter((i) => fs.existsSync(path.join(ROOT, OUT[i], `${OUT[i]}_stand.png`)));
const lu = createCanvas(all.length * (LW + G) + G, LH + 2 * G + 40), l = lu.getContext("2d");
l.fillStyle = "#efe7d6"; l.fillRect(0, 0, lu.width, lu.height);
for (let i = 0; i < all.length; i++) {
  const x = G + i * (LW + G); l.fillStyle = "#faf5ea"; l.fillRect(x, G, LW, LH + 40);
  l.drawImage(await loadImage(path.join(ROOT, OUT[all[i]], `${OUT[all[i]]}_stand.png`)), x, G, LW, LH);
  l.fillStyle = "#241726"; l.font = "22px DejaVu Sans"; l.textAlign = "center"; l.fillText(NAMES[all[i]], x + LW / 2, G + LH + 28);
}
fs.writeFileSync(path.join(ROOT, "cast_lineup.png"), lu.toBuffer("image/png"));
console.log("wrote cast_lineup.png", lu.width + "x" + lu.height);
