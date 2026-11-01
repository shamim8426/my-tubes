// Props in the cast v3 ink style (same Pen API): Lon Chacha's rocket (with / without flame) and a floating guava.
// usage: npx tsx render-props.ts   -> characters/_props/<name>.png (transparent)
import { createCanvas } from "@napi-rs/canvas";
import fs from "node:fs"; import path from "node:path";
import { Pen, INK, mul } from "./toon";

type P2 = [number, number];
const OUT = path.resolve(import.meta.dirname, "..", "_props");
fs.mkdirSync(OUT, { recursive: true });
const SH: [number, number, number] = [0.72, 0.74, 0.82], LIGHT = (-120 * Math.PI) / 180;

const rocket = (flame: boolean) => {
  const c = createCanvas(800, 1600), g = c.getContext("2d") as any, p = new Pen(g);
  const cx = 400, top = 120, bot = 1130, W = 190;
  // body outline: pointed ogive nose, straight sides, slight taper at the base
  const half = (y: number) => { const t = (y - top) / (bot - top); return t < 0.42 ? W * Math.sqrt(t / 0.42) * (0.25 + 0.75 * Math.sin((t / 0.42) * Math.PI / 2)) : W * (1 - 0.12 * Math.max(0, (t - 0.8) / 0.2)); };
  const R: P2[] = [], L: P2[] = [];
  for (let i = 0; i <= 40; i++) { const y = top + (bot - top) * (i / 40); R.push([cx + half(y), y]); L.push([cx - half(y), y]); }
  const body = [...R, ...L.reverse()];
  if (flame) { // flame behind the nozzle: outer orange, inner yellow, white core
    const f = (k: number, col: string) => p.poly([[cx - 95 * k, bot + 40], [cx + 95 * k, bot + 40], [cx + 40 * k, bot + 40 + 330 * k], [cx, bot + 40 + 420 * k], [cx - 40 * k, bot + 40 + 330 * k]], col, k === 1 ? 5 : 0);
    f(1, "#f07a2a"); f(0.72, "#f6c638"); f(0.4, "#fff6d0");
  }
  // fins (behind the body)
  for (const s of [-1, 1]) p.poly([[cx + s * (W - 10), bot - 330], [cx + s * (W + 150), bot - 40], [cx + s * (W + 150), bot + 70], [cx + s * (W - 30), bot - 20]], "#d8453a", 6);
  p.poly([[cx - 22, bot - 200], [cx + 22, bot - 200], [cx + 30, bot + 70], [cx - 30, bot + 70]], mul("#d8453a", SH), 6);
  // nozzle
  p.poly([[cx - 110, bot - 10], [cx + 110, bot - 10], [cx + 135, bot + 50], [cx - 135, bot + 50]], "#6a6f7c", 6);
  // body + red nose cap
  p.gradFill(body, "#f4ead6", mul("#f4ead6", SH), LIGHT);
  p.clip(body, () => {
    p.poly([[0, 0], [800, 0], [800, top + 300], [0, top + 300]], "#d8453a", 0);
    p.stroke([[0, top + 300], [800, top + 300]], 10, INK);
    for (const y of [bot - 200, bot - 170]) p.stroke([[0, y], [800, y]], 12, y === bot - 200 ? "#d8453a" : "#f0b43a");
  });
  p.inkRing(body, 9, 0.6);
  // porthole window with a glass shine
  p.ell(cx, 560, 92, 92, "#7a7f8c", 8);
  p.ell(cx, 560, 70, 70, "#6fb8e8", 6);
  p.arc(cx, 560, 50, 50, 200, 260, 9, "rgba(255,255,255,0.85)");
  for (let k = 0; k < 8; k++) { const a = (k * Math.PI) / 4; p.dot(cx + Math.cos(a) * 81, 560 + Math.sin(a) * 81, 5, "#4a4f5c"); }
  // door outline + handle, rivet line
  p.poly([[cx - 70, 760], [cx + 70, 760], [cx + 70, 940], [cx - 70, 940]], null, 5);
  p.dot(cx + 48, 850, 8, "#f0b43a");
  for (let k = 0; k < 7; k++) p.dot(cx - 150 + k * 50, 700, 4.5, "#b8ad98");
  fs.writeFileSync(path.join(OUT, flame ? "rocket_flame.png" : "rocket.png"), c.toBuffer("image/png"));
};

const guava = () => {
  const c = createCanvas(240, 240), g = c.getContext("2d") as any, p = new Pen(g);
  p.ell(120, 128, 82, 78, "#9ec23a", 8); p.ell(120, 128, 48, 42, "#f0e48a", 0); p.dot(112, 126, 9, "#8a7a30");
  p.line([[120, 52], [128, 26]], "#6a4a2a", 9); p.ell(150, 34, 26, 12, "#58a838", 4, 0, 360, -20);
  fs.writeFileSync(path.join(OUT, "guava.png"), c.toBuffer("image/png"));
};

rocket(false); rocket(true); guava();
console.log("wrote props to", OUT);
