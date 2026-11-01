// Jugnu Stories cast v3 (locked 2026-10-30, my-tubes log.md) drawn with the toon.ts Pen API: 600 x 1000 design canvas, soles at y = 975.
// Tinku (hero), Bholu, Ira, Titli, Daroga Singh, Kesar Dadi, Tinku ki mummy + Jugnu (real firefly beetle).
// Style = cartoon-3d-short: bean heads, plum variable-width outline, deadpan dot eyes, no blush, no catchlights in the eyes.
// Limbs are filled tubes with an ink rim (healthy, not sticks). Designs follow characters/_v3_free/_cast_final.jpg only
// for look (colours, outfit, props); the drawing is our own.
import { Pen, INK, blobPts, headBlob, thickAngle, mix, mul } from "./toon";

type P2 = [number, number];
const rad = (d: number) => (d * Math.PI) / 180;
const clamp = (x: number, a: number, b: number) => Math.max(a, Math.min(b, x));
const rnd = (seed: number, k: number) => { const x = Math.sin(seed * 127.1 + k * 311.7) * 43758.5453; return x - Math.floor(x); };
const lerp2 = (a: P2, b: P2, t: number): P2 => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t];
const rotAbout = (q: P2, a: number, c: P2): P2 => [c[0] + (q[0] - c[0]) * Math.cos(a) - (q[1] - c[1]) * Math.sin(a), c[1] + (q[0] - c[0]) * Math.sin(a) + (q[1] - c[1]) * Math.cos(a)];
const curve = (a: P2, k: P2, b: P2, n = 10): P2[] => {
  const c: P2 = [2 * k[0] - (a[0] + b[0]) / 2, 2 * k[1] - (a[1] + b[1]) / 2], out: P2[] = [];
  for (let i = 0; i <= n; i++) { const t = i / n, s = 1 - t; out.push([s * s * a[0] + 2 * s * t * c[0] + t * t * b[0], s * s * a[1] + 2 * s * t * c[1] + t * t * b[1]]); }
  return out;
};
const WHITE = "#ffffff", MOUTH = "#5a1e28", TONGUE = "#e86e78", SWEAT = "#9fd4ff";
const SH_SKIN: [number, number, number] = [0.96, 0.86, 0.84], SH_CLOTH: [number, number, number] = [0.64, 0.66, 0.74];
const LIGHT = rad(-120);

export type Pose = "stand" | "walk" | "point" | "think" | "happy" | "surprised" | "scared" | "laugh";
export type CharId = "tinku" | "bholu" | "ira" | "titli" | "daroga" | "dadi" | "mummy" | "jugnu";
export const POSES: Pose[] = ["stand", "walk", "point", "think", "happy", "surprised", "scared", "laugh"];
type Expr = "smile" | "happy" | "surprised" | "scared" | "laugh" | "think";
type Layer = "back" | "mid" | "top";
// rel = hand target from the shoulder as a fraction of the arm reach (x outward-positive, y down); abs = design-canvas point
type ArmSpec = { rel?: P2; abs?: P2; layer?: Layer; finger?: boolean; elbow?: "out" | "down" };
type PoseSpec = { expr: Expr; lean?: number; headTilt?: number; facing?: -1 | 0 | 1; legL?: [number, number]; legR?: [number, number]; armL: ArmSpec; armR: ArmSpec };
const HANG: P2 = [0.12, 0.96];
const BASE: Record<Pose, PoseSpec> = {
  stand: { expr: "smile", armL: { rel: HANG }, armR: { rel: HANG } },
  walk: { expr: "smile", lean: 2, headTilt: -2, legL: [0, 1], legR: [22, 6], armL: { rel: [0.15, 0.86], layer: "mid", elbow: "out" }, armR: { rel: [0.12, 0.96] } },
  point: { expr: "happy", facing: 1, lean: -1, headTilt: 3, armL: { rel: HANG }, armR: { rel: [0.95, -0.36], finger: true, layer: "top" } },
  think: { expr: "think", lean: 1, headTilt: 7, facing: 1, armL: { rel: HANG }, armR: { layer: "top", elbow: "down" } },
  happy: { expr: "happy", armL: { rel: [0.42, -0.36], layer: "back" }, armR: { rel: [0.42, -0.36], layer: "back" } },
  surprised: { expr: "surprised", lean: -2, legL: [0, 2], legR: [0, 2], armL: { rel: [0.58, 0.0], layer: "back" }, armR: { rel: [0.58, 0.0], layer: "back" } },
  scared: { expr: "scared", lean: 3, headTilt: -3, legL: [0, -2], legR: [0, -2], armL: { layer: "top" }, armR: { layer: "top" } },
  laugh: { expr: "laugh", lean: -4, headTilt: -7, armL: { layer: "mid", elbow: "down" }, armR: { layer: "mid", elbow: "down" } },
};

// ---------------- character sheet data ----------------
type HairK = { kind: "neat" | "spiky" | "smooth" | "grey" | "sides" | "none"; color: string; hi?: string; tuft: number; period: number; fringe: number; slope: number; jag: number; grow?: number; part?: boolean };
type BackHair = { kind: "bob" | "pigtails" | "bun" | "long"; color: string; clips?: [string, string] };
type PropK = { kind: "guava" | "notebook" | "pinwheel" | "magnifier" | "biscuit" | "cane" | "plate"; hand?: "L" | "R"; poses: Pose[] };
type Spec = {
  A: number; skin: string; torsoK: number; legK: number; tw: number; egg: number; limb: number; legW: number; armK: number;
  hair: HairK; back?: BackHair; glasses?: boolean; moustache?: boolean; cap?: boolean; bindi?: boolean; lashes?: boolean; wrinkles?: boolean;
  earrings?: string; necklace?: boolean; braid?: boolean; bag?: boolean; smileDefault?: Expr;
  top: { kind: "polo" | "tee" | "tunic" | "saree" | "uniform"; color: string; trim?: string; trim2?: string; sleeve: number; cuff?: string; hem?: number };
  bottom: { kind: "shorts" | "pants" | "none"; color: string; len?: number; hem?: string };
  shoe: "sandal" | "croc" | "shoe" | "bare" | "chappal"; shoeColor: string; props: PropK[]; over?: Partial<Record<Pose, Partial<PoseSpec>>>; hang?: number;
};
const SPECS: Record<Exclude<CharId, "jugnu">, Spec> = {
  tinku: { A: 108, skin: "#efbf98", torsoK: 1.0, legK: 1.35, tw: 0.31, egg: 0.1, limb: 8.2, legW: 10.4, armK: 0.5, glasses: true, bag: true,
    hair: { kind: "neat", color: "#1a1620", hi: "#3d3247", tuft: 0.02, period: 7, fringe: 27, slope: 7, jag: 2, grow: 1.06 },
    top: { kind: "polo", color: "#27324f", trim: "#1a2238", sleeve: 0.4 }, bottom: { kind: "shorts", color: "#c4b08a", len: 0.62, hem: "#a8946c" },
    shoe: "sandal", shoeColor: "#6d4528", props: [] },
  bholu: { A: 118, skin: "#f0bd96", torsoK: 0.95, legK: 1.0, tw: 0.41, egg: 0.2, limb: 10, legW: 12.5, armK: 0.44, smileDefault: "happy",
    hair: { kind: "spiky", color: "#17131a", hi: "#3a3042", tuft: 0.13, period: 5, fringe: 25, slope: 4, jag: 8, grow: 1.07 },
    top: { kind: "tee", color: "#cc3f2f", trim: "#a82f22", sleeve: 0.4 }, bottom: { kind: "shorts", color: "#7a5a30", len: 0.5, hem: "#5c4223" },
    shoe: "croc", shoeColor: "#3b6fc0", props: [{ kind: "guava", hand: "R", poses: ["stand", "walk", "happy", "surprised", "scared"] }] },
  ira: { A: 104, skin: "#f0c4a0", torsoK: 1.0, legK: 1.45, tw: 0.27, egg: 0.06, limb: 7, legW: 8.6, armK: 0.5, lashes: true,
    hair: { kind: "smooth", color: "#17131a", hi: "#3a3042", tuft: 0, period: 9, fringe: 24, slope: 8, jag: 0, grow: 1.05 }, back: { kind: "bob", color: "#17131a" },
    top: { kind: "tunic", color: "#a58ccf", trim: "#e3d9f3", sleeve: 1.0, hem: 0.62 }, bottom: { kind: "pants", color: "#f4f1ea" },
    shoe: "sandal", shoeColor: "#6d4528", props: [{ kind: "notebook", hand: "R", poses: ["stand", "walk", "happy", "surprised", "scared"] }] },
  titli: { A: 108, skin: "#efbf98", torsoK: 0.9, legK: 1.15, tw: 0.26, egg: 0.1, limb: 7.6, legW: 9.6, armK: 0.44, lashes: true, smileDefault: "happy",
    hair: { kind: "smooth", color: "#2d2020", hi: "#54403c", tuft: 0, period: 9, fringe: 25, slope: 3, jag: 0, grow: 1.05, part: true }, back: { kind: "pigtails", color: "#2d2020", clips: ["#7ec8f0", "#f08ab8"] },
    top: { kind: "tunic", color: "#f4a3c0", trim: "#f4dc8a", sleeve: 0.34, cuff: "#f4dc8a", hem: 0.5 }, bottom: { kind: "none", color: "#f4a3c0" },
    shoe: "bare", shoeColor: "#efbf98", props: [{ kind: "pinwheel", hand: "R", poses: ["stand", "walk", "happy", "surprised", "scared"] }] },
  daroga: { A: 104, skin: "#f0b890", torsoK: 1.15, legK: 1.12, tw: 0.5, egg: 0.26, limb: 10.4, legW: 13.5, armK: 0.5, moustache: true, cap: true,
    hair: { kind: "sides", color: "#17131a", hi: "#3a3042", tuft: 0, period: 9, fringe: 0, slope: 0, jag: 0, grow: 1.04 },
    top: { kind: "uniform", color: "#b9b27e", trim: "#9a9366", trim2: "#4a2f20", sleeve: 0.4 }, bottom: { kind: "pants", color: "#aaa56f" },
    shoe: "shoe", shoeColor: "#4a3326", props: [{ kind: "magnifier", hand: "R", poses: ["stand", "walk", "happy", "surprised", "scared", "laugh"] }, { kind: "biscuit", hand: "L", poses: ["stand", "walk", "happy", "surprised", "scared"] }],
    over: { stand: { armR: { rel: [0.5, -0.1], elbow: "out" }, armL: { rel: [0.46, 0.12], elbow: "out" } } } },
  dadi: { A: 100, skin: "#efc9a8", torsoK: 1.0, legK: 1.5, tw: 0.27, egg: 0.08, limb: 7, legW: 8, armK: 0.5, bindi: true, lashes: true, wrinkles: true, earrings: "#e0b04a",
    hair: { kind: "grey", color: "#d6d6de", hi: "#f3f3f8", tuft: 0, period: 9, fringe: 25, slope: 0, jag: 0, grow: 1.04, part: true }, back: { kind: "bun", color: "#d6d6de" },
    top: { kind: "saree", color: "#e9962a", trim: "#7d2038", trim2: "#f3ecdc", sleeve: 0.34, hem: 0 }, bottom: { kind: "none", color: "#e9962a" },
    shoe: "chappal", shoeColor: "#8a6a44", props: [{ kind: "cane", hand: "L", poses: ["stand", "walk", "surprised", "scared"] }],
    over: { walk: { lean: 0 } } },
  mummy: { A: 102, skin: "#e6ae80", torsoK: 1.05, legK: 1.5, tw: 0.3, egg: 0.1, limb: 7.6, legW: 8.6, armK: 0.5, bindi: true, lashes: true, earrings: "#e0b04a", necklace: true, braid: true,
    hair: { kind: "smooth", color: "#14101a", hi: "#3a3042", tuft: 0, period: 9, fringe: 24, slope: 0, jag: 0, grow: 1.05, part: true }, back: { kind: "long", color: "#14101a" },
    top: { kind: "saree", color: "#1f8a78", trim: "#d8b04a", trim2: "#1f8a78", sleeve: 0.34, hem: 0 }, bottom: { kind: "none", color: "#1f8a78" },
    shoe: "chappal", shoeColor: "#8a6a44", props: [{ kind: "plate", poses: ["stand", "walk", "happy"] }],
    over: { stand: { armL: { abs: [0, 0], layer: "mid", elbow: "down" }, armR: { abs: [0, 0], layer: "mid", elbow: "down" } },
      walk: { armL: { abs: [0, 0], layer: "mid", elbow: "down" }, armR: { abs: [0, 0], layer: "mid", elbow: "down" } },
      happy: { armL: { abs: [0, 0], layer: "mid", elbow: "down" }, armR: { abs: [0, 0], layer: "mid", elbow: "down" } } } },
};
const SKIN_DEEP = (c: string) => mul(c, SH_SKIN);

// ---------------- face ----------------
type EyeK = "dot" | "dotUp" | "happy" | "squeeze" | "wide" | "scared";
type MouthK = "smile" | "grin" | "laugh" | "O" | "teeth" | "skew";
type Face = { eye: EyeK; mouth: MouthK; brow: [number, number, number, number]; sweat?: boolean };
const FACES: Record<Expr, Face> = {
  smile: { eye: "dot", mouth: "smile", brow: [0, -1, 0, -1] },
  happy: { eye: "happy", mouth: "grin", brow: [-3, -3, -3, -3] },
  surprised: { eye: "wide", mouth: "O", brow: [-8, -9, -8, -9] },
  scared: { eye: "scared", mouth: "teeth", brow: [-8, 3, -8, 3], sweat: true },
  laugh: { eye: "squeeze", mouth: "laugh", brow: [-5, -5, -5, -5] },
  think: { eye: "dotUp", mouth: "skew", brow: [-9, -10, 3, 1] },
};
const taper = (p: Pen, a: P2, b: P2, wa: number, wb: number, col = INK) => {
  const dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1, nx = -dy / l, ny = dx / l;
  p.poly([[a[0] + nx * wa / 2, a[1] + ny * wa / 2], [b[0] + nx * wb / 2, b[1] + ny * wb / 2], [b[0] - nx * wb / 2, b[1] - ny * wb / 2], [a[0] - nx * wa / 2, a[1] - ny * wa / 2]], col, 0);
  p.dot(a[0], a[1], wa / 2, col); p.dot(b[0], b[1], wb / 2, col);
};
const dmouth = (p: Pen, mx: number, y: number, rx: number, ry: number, u: number, tongue = false) => {
  p.ell(mx, y, rx, ry, MOUTH, 0, 0, 180);
  p.clip([[mx - rx, y], [mx + rx, y], [mx + rx, y + 3.2 * u], [mx - rx, y + 3.2 * u]], () => p.ell(mx, y, rx, ry, WHITE, 0, 0, 180));
  if (tongue) p.ell(mx + 2 * u, y + 0.62 * ry, 0.42 * rx, 0.3 * ry, TONGUE, 0);
  p.ell(mx, y, rx, ry, null, 3 * u, 0, 180);
};
const face = (p: Pen, cx: number, hc: number, u: number, F: Face, facing: number, earX: number, sp: Spec, skin: string) => {
  const fx = cx + 5 * u * facing, ex = (sp.glasses ? 15.8 : 14) * u, ey = hc + (sp.glasses ? 3 : 4) * u, R = 14.5 * u, lw = 3.6 * u;
  for (const side of [-1, 1]) {
    const x = fx + side * ex, es = sp.glasses ? 1 : 1.12;
    switch (F.eye) {
      case "dot": p.ell(x, ey + u, 3.8 * u * es, 5.4 * u * es, INK, 0); break;
      case "dotUp": p.ell(x + 3.5 * u, ey - 3 * u, 3.8 * u * es, 5.4 * u * es, INK, 0); break;
      case "happy": p.arc(x, ey + 4 * u, 8 * u, 6.5 * u, 200, 340, lw); break;
      case "squeeze": p.stroke([[x + 6.5 * u * side, ey - 5.5 * u], [x - 6.5 * u * side, ey], [x + 6.5 * u * side, ey + 5.5 * u]], lw); break;
      case "wide": p.ell(x, ey, 9.6 * u, 9.6 * u, WHITE, 2.4 * u); p.dot(x - side * u, ey + u, 3.4 * u); break;
      case "scared": p.ell(x, ey, 9 * u, 9 * u, WHITE, 2.4 * u); p.dot(x + u * facing, ey + 1.2 * u, 2.3 * u); break;
    }
    if (sp.lashes && F.eye !== "squeeze") p.stroke([[x + side * 5 * u, ey - 3 * u], [x + side * 9.5 * u, ey - 6.5 * u]], 2 * u);
    if (sp.glasses) {
      p.ell(x, ey, R, R, "rgba(255,255,255,0.20)", 0);
      p.arc(x, ey, R * 0.74, R * 0.74, 205, 250, 2 * u, "rgba(255,255,255,0.85)");
      p.ell(x, ey, R, R, null, 2.5 * u);
      p.stroke([[x + side * R, ey - u], [cx + side * earX, ey + 1.5 * u]], 2.2 * u);
    }
  }
  if (sp.glasses) p.stroke([[fx - 2.4 * u, ey - 3.5 * u], [fx + 2.4 * u, ey - 3.5 * u]], 2.6 * u);
  for (const [k, side] of [[0, -1], [2, 1]] as const) {
    const x = fx + side * ex, by = ey - (sp.glasses ? 22.5 : 15.5) * u;
    taper(p, [x - side * 9 * u, by + F.brow[k] * u], [x + side * 9 * u, by + F.brow[k + 1] * u], 5 * u, 2.6 * u, sp.hair.kind === "grey" ? "#8d8d98" : INK);
  }
  if (sp.wrinkles) for (const side of [-1, 1]) { p.arc(fx + side * (ex + 8 * u), ey + 2 * u, 5 * u, 7 * u, side > 0 ? -50 : 130, side > 0 ? 50 : 230, 1.4 * u, SKIN_DEEP(skin)); p.stroke([[fx + side * 6 * u, hc - 26 * u], [fx + side * 18 * u, hc - 25 * u]], 1.2 * u, SKIN_DEEP(skin)); }
  const mx = fx + u * facing, my = hc + (sp.glasses ? 29 : sp.moustache ? 28 : 27) * u;
  if (sp.moustache) {
    p.ell(fx, hc + 12 * u, 6.5 * u, 5.5 * u, mix(skin, "#d2706a", 0.4), 2 * u); // round nose under the moustache
  }
  switch (F.mouth) {
    case "smile": p.arc(mx, my - 3.5 * u, 9 * u, 5.5 * u, 20, 160, 3.7 * u); break;
    case "grin": dmouth(p, mx, my - 1.5 * u, 13.5 * u, 9.5 * u, u); break;
    case "laugh": dmouth(p, mx, my - 1 * u, 17.5 * u, 12.5 * u, u, true); break;
    case "O": p.ell(mx, my + 3 * u, 7 * u, 9.5 * u, MOUTH, 3.1 * u); break;
    case "teeth":
      p.poly([[mx - 12 * u, my - 3 * u], [mx + 12 * u, my - 3 * u], [mx + 11 * u, my + 5 * u], [mx - 11 * u, my + 5 * u]], WHITE, 3 * u);
      for (const j of [-1, 0, 1]) p.stroke([[mx + j * 6 * u, my - 3 * u], [mx + j * 6 * u, my + 5 * u]], 1.5 * u);
      break;
    case "skew": p.stroke([[mx - 7 * u, my + 2.5 * u], [mx, my + 0.5 * u], [mx + 8 * u, my - 3 * u]], 3.6 * u); break;
  }
  if (sp.moustache) for (const s of [-1, 1]) {
    p.poly([[fx + s * 1 * u, hc + 15.5 * u], [fx + s * 12 * u, hc + 13 * u], [fx + s * 21 * u, hc + 17 * u], [fx + s * 22 * u, hc + 12 * u], [fx + s * 25 * u, hc + 18 * u], [fx + s * 14 * u, hc + 22.5 * u], [fx + s * 2 * u, hc + 21 * u]], "#17131a", 1.6 * u);
  }
  if (sp.bindi) p.ell(fx, hc - 19 * u, 2.8 * u, 2.8 * u, "#c0262e", 0);
  if (F.sweat) p.poly([[cx + 41 * u, hc - 8 * u], [cx + 46 * u, hc + 2 * u], [cx + 41 * u, hc + 8 * u], [cx + 36 * u, hc + 2 * u]], SWEAT, 2.2 * u);
};

/** upper head cap of hair (tufts, fringe) */
const hairPoly = (hp: P2[], cx: number, hc: number, H: { b: number }, u: number, h: HairK): P2[] => {
  const n = hp.length, yc = hc - (h.kind === "sides" ? 0.1 : 0.3) * H.b, keep = (q: P2) => q[1] < yc;
  const s0 = Math.max(0, hp.findIndex((q, i) => keep(q) && !keep(hp[(i + n - 1) % n])));
  const arc = [...hp.slice(s0), ...hp.slice(0, s0)].filter(keep);
  const out: P2[] = arc.map(([x, y], j) => {
    const on = h.period > 0 && j % h.period === 2, tuft = on ? h.tuft * (0.5 + 0.5 * rnd(7, j)) : h.tuft > 0.05 && j % h.period === 3 ? h.tuft * 0.4 : 0;
    const s = (h.grow ?? 1.06) + tuft, sk = on ? (rnd(7, j + 40) - 0.5) * h.tuft * 40 * u : 0;
    return [cx + (x - cx) * s + sk, hc + (y - hc) * s] as P2;
  });
  if (h.kind === "sides") return [...out, ...out.slice().reverse().map(([x, y]) => [cx + (x - cx) * 0.9, hc + (y - hc) * 0.9 + 6 * u] as P2)];
  const xr = out[out.length - 1][0], xl = out[0][0], fr: P2[] = [];
  for (let i = 1; i < 9; i++) {
    const t = i / 9, x = xr + (xl - xr) * t, edge = Math.min(i, 9 - i) <= 1;
    const sl = h.slope * (0.5 - t) * 2 * u, jag = (i % 2 ? (0.5 + 0.5 * rnd(7, 60 + i)) * h.jag * u : 0), vpart = h.part ? Math.abs(t - 0.5) * 16 * u : 0;
    fr.push([x, hc - (edge ? h.fringe * 0.62 : h.fringe) * u + sl + jag + (edge ? 0 : vpart) - (h.part ? 4 * u : 0)]);
  }
  return [...out, ...fr];
};

// ---------------- the character ----------------
export const drawChar = (g: CanvasRenderingContext2D, id: CharId, pose: Pose) => {
  if (id === "jugnu") return drawJugnu(g, pose);
  const sp = SPECS[id], base = BASE[pose], S: PoseSpec = { ...base, ...(sp.over?.[pose] ?? {}) };
  const F = FACES[sp.smileDefault && S.expr === "smile" ? sp.smileDefault : S.expr], p = new Pen(g);
  const A = sp.A, facing = S.facing ?? 0, seed = 7, skin = sp.skin, col = sp.top, bot = sp.bottom;
  const H = { ...headBlob(seed, A, 0), asym: 0.035 * (facing || 1), rot: rad(1.5), noise: 0.005 };
  const W = 2 * A, HH = 2 * H.b, u = W / 100, sole = 975;
  const torsoBot = sole - sp.legK * HH, chin = torsoBot - sp.torsoK * HH, hc = chin - H.b, hipY = torsoBot - 0.12 * HH;
  const thick = thickAngle(LIGHT), ow = 5 * u, limb = 2.6 * u;
  const T = { a: sp.tw * W, b: 0.5 * (torsoBot - (chin - 0.25 * HH)), nTop: 2.2, nBot: 2.6, egg: sp.egg, rot: 0, asym: 0, noise: 0.005, seed: seed + 7 };
  const tcx = 300, tcy = torsoBot - T.b, lean = S.lean ?? 0;
  const gown = col.kind === "tunic" || col.kind === "saree";
  const hemY = gown ? (col.kind === "saree" ? sole - 12 * u : torsoBot + (col.hem ?? 0.5) * HH) : torsoBot;
  const clothShade = (c: string) => mul(c, SH_CLOTH);

  // ---- legs + shoes (unrotated) ----
  p.rot = null; p.ol = limb;
  const spread = Math.max(14, sp.tw * 46) * u, legCol = bot.kind === "pants" ? bot.color : skin;
  const hidden = col.kind === "saree";
  for (const [side, L] of [[-1, S.legL ?? [0, 0]], [1, S.legR ?? [0, 0]]] as const) {
    const up = Math.min(L[0], hidden ? 5 : 99) * u, out = L[1] * u, hx = 300 + side * spread * 0.9, hy = (gown ? hemY - 0.2 * HH : bot.kind === "pants" ? torsoBot - 0.02 * HH : torsoBot + 0.3 * HH);
    const ank: P2 = [300 + side * (spread * 1.3 + 4 * u) + side * out, sole - 8 * u - up];
    if (!hidden) {
      const knee: P2 = [(hx + ank[0]) / 2 + side * (2 * u + up * 0.28), (hy + ank[1]) / 2 - up * 0.55];
      p.line(curve([hx, hy], knee, ank), legCol, sp.legW * u);
    }
    const fx = ank[0] + side * 3 * u, fy = ank[1];
    switch (sp.shoe) {
      case "croc": p.ell(fx + side * 4 * u, fy + 3 * u, 15 * u, 8.2 * u, sp.shoeColor, 2.2 * u); for (const k of [-1, 0, 1]) p.dot(fx + side * (4 + k * 5) * u, fy + 1 * u, 1.3 * u, mul(sp.shoeColor, [0.7, 0.7, 0.7])); break;
      case "shoe": p.ell(fx + side * 5 * u, fy + 3 * u, 15 * u, 8 * u, sp.shoeColor, 2.4 * u); p.arc(fx + side * 6 * u, fy, 8 * u, 4 * u, 190, 350, 1.6 * u, mul(sp.shoeColor, [1.6, 1.6, 1.6])); break;
      case "bare": p.ell(fx + side * 4 * u, fy + 3 * u, 12 * u, 5.6 * u, skin, 2 * u); break;
      case "chappal": p.ell(fx + side * 4 * u, fy + 5 * u, 11 * u, 3.2 * u, sp.shoeColor, 1.8 * u); p.ell(fx + side * 4 * u, fy + 2 * u, 9 * u, 4.4 * u, skin, 1.8 * u); p.stroke([[fx - 2 * u, fy - 2 * u], [fx + side * 8 * u, fy + 1 * u]], 2 * u, mul(sp.shoeColor, [0.7, 0.7, 0.7])); break;
      default: p.ell(fx + side * 5 * u, fy + 5.5 * u, 12.5 * u, 3.8 * u, sp.shoeColor, 2 * u); p.ell(fx + side * 4.5 * u, fy + 1.5 * u, 9.5 * u, 4.8 * u, skin, 2 * u); p.stroke([[fx - side * 3 * u, fy - 2.5 * u], [fx + side * 5 * u, fy + 1 * u]], 2.6 * u, "#4f2f1c");
    }
  }

  // ---- arms ----
  const Lu = sp.armK * HH, Lf = sp.armK * HH, reachU = (Lu + Lf) / u;
  const shoulder = (side: number): P2 => [tcx + side * 0.85 * T.a, chin + 0.12 * HH];
  const joints = (side: number, a: ArmSpec): [P2, P2, P2] => {
    const Sh = shoulder(side);
    let hd: P2 = a.abs && (a.abs[0] || a.abs[1]) ? a.abs : [Sh[0] + side * (a.rel ?? HANG)[0] * reachU * u, Sh[1] + (a.rel ?? HANG)[1] * reachU * u];
    const dx = hd[0] - Sh[0], dy = hd[1] - Sh[1], d = Math.max(1, Math.hypot(dx, dy)), reach = Lu + Lf - 0.5, dd = Math.min(d, reach);
    hd = [Sh[0] + (dx / d) * dd, Sh[1] + (dy / d) * dd];
    const aa = Math.acos(clamp((Lu * Lu + dd * dd - Lf * Lf) / (2 * Lu * dd), -1, 1)), b0 = Math.atan2(hd[1] - Sh[1], hd[0] - Sh[0]);
    const c1: P2 = [Sh[0] + Lu * Math.cos(b0 + aa), Sh[1] + Lu * Math.sin(b0 + aa)], c2: P2 = [Sh[0] + Lu * Math.cos(b0 - aa), Sh[1] + Lu * Math.sin(b0 - aa)];
    const score = (e: P2) => (a.elbow === "down" ? e[1] + 0.2 * side * (e[0] - tcx) : side * (e[0] - tcx) + 0.6 * e[1]);
    return [Sh, score(c1) >= score(c2) ? c1 : c2, hd];
  };
  const specR: ArmSpec = { ...S.armR }, specL: ArmSpec = { ...S.armL };
  const plateOn = sp.props.some((q) => q.kind === "plate" && q.poses.includes(pose));
  if (pose === "think") specR.abs = [tcx + 15 * u, chin - 2 * u];
  else if (pose === "scared") { const sx2 = 0.85 * T.a + 18; specL.abs = [tcx - sx2, chin + 10 * u]; specR.abs = [tcx + sx2, chin + 10 * u]; }
  else if (pose === "laugh") { specR.abs = [tcx + 12 * u, chin + 0.68 * HH]; specL.abs = [tcx - 12 * u, chin + 0.6 * HH]; }
  if (plateOn) { const py = chin + 0.74 * HH; specL.abs = [tcx - 33 * u, py]; specR.abs = [tcx + 33 * u, py]; specL.elbow = specR.elbow = "out"; }
  const armSet = [[-1, specL] as const, [1, specR] as const].map(([side, spec]) => ({ side, spec, j: joints(side, spec) }));
  const sleeveCol = col.kind === "saree" ? col.color : col.color;
  const props = sp.props.filter((q) => q.poses.includes(pose) && q.kind !== "plate");
  const drawProp = (q: PropK, Hd: P2, E: P2) => {
    const [x, y] = Hd;
    switch (q.kind) {
      case "guava": p.ell(x + 2 * u, y - 7 * u, 10.5 * u, 10 * u, "#9ec23a", 2 * u); p.ell(x + 2 * u, y - 7 * u, 6 * u, 5.4 * u, "#f0e48a", 0); p.dot(x + 1 * u, y - 7 * u, 1.2 * u, "#8a7a30"); break;
      case "notebook": p.poly([[x - 13 * u, y - 24 * u], [x + 11 * u, y - 24 * u], [x + 11 * u, y + 6 * u], [x - 13 * u, y + 6 * u]], "#c9a878", 2.2 * u); p.stroke([[x - 9 * u, y - 24 * u], [x - 9 * u, y + 6 * u]], 1.6 * u, "#8a6a40"); p.line([[x + 6 * u, y - 30 * u], [x + 12 * u, y - 14 * u]], "#f0c030", 2.6 * u); break;
      case "pinwheel": {
        p.line([[x, y + 8 * u], [x + 2 * u, y - 52 * u]], "#9a6a3a", 2.6 * u);
        const cx = x + 2 * u, cy = y - 54 * u, cols = ["#e8453c", "#f4c030", "#3c9ae8", "#58b848"];
        cols.forEach((c, k) => { const a = rad(k * 90 + 20); p.poly([[cx, cy], [cx + Math.cos(a) * 24 * u, cy + Math.sin(a) * 24 * u], [cx + Math.cos(a + 1.1) * 15 * u, cy + Math.sin(a + 1.1) * 15 * u]], c, 1.8 * u); });
        p.dot(cx, cy, 3.2 * u, WHITE); break;
      }
      case "magnifier": {
        p.line([[x - 4 * u, y + 14 * u], [x + 2 * u, y - 22 * u]], "#5a3a22", 4.4 * u);
        p.ell(x + 8 * u, y - 44 * u, 19 * u, 22 * u, "rgba(190,225,240,0.55)", 3.4 * u); p.arc(x + 8 * u, y - 44 * u, 12 * u, 15 * u, 205, 250, 2 * u, "rgba(255,255,255,0.9)"); break;
      }
      case "biscuit": p.ell(x + 2 * u, y - 8 * u, 9.5 * u, 9 * u, "#b88a50", 2.2 * u); for (const [dx, dy] of [[-3, -10], [3, -6], [0, -3]]) p.dot(x + dx * u, y + dy * u, 1 * u, "#7a5a30"); break;
      case "cane": p.line([[x, y + 2 * u], [x + 3 * u, sole - 2 * u]], "#6a4a2a", 4.2 * u); break;
    }
    void E;
  };
  const drawArm = (side: number, spec: ArmSpec, [Sh, E, Hd]: [P2, P2, P2]) => {
    p.ol = limb;
    const pts = curve(Sh, E, Hd, 14);
    p.line(pts, skin, sp.limb * u);
    const n = Math.max(2, Math.round(col.sleeve * (pts.length - 1)));
    const slv = pts.slice(0, n + 1);
    if (col.sleeve > 0.01) p.line(slv, sleeveCol, sp.limb * u + 4.2 * u);
    if (col.cuff) { const a = slv[slv.length - 1], b = slv[Math.max(0, slv.length - 3)]; p.line([b, a], col.cuff, sp.limb * u + 4.2 * u); }
    if (col.kind === "tunic" && col.trim && col.sleeve > 0.9) p.line(pts.slice(pts.length - 4, pts.length - 2), col.trim, sp.limb * u + 4.4 * u);
    if (spec.finger) {
      const ex = Hd[0] - E[0], ey = Hd[1] - E[1], el = Math.hypot(ex, ey) || 1;
      p.line([Hd, [Hd[0] + (ex / el) * 17 * u, Hd[1] + (ey / el) * 17 * u]], skin, 3.6 * u);
    }
    for (const q of props) if ((q.hand ?? "R") === (side > 0 ? "R" : "L")) drawProp(q, Hd, E);
    p.ell(Hd[0], Hd[1], 6 * u, 6 * u, skin, 2 * u);
  };
  const layerArms = (ly: Layer) => armSet.filter((a) => (a.spec.layer ?? "back") === ly).forEach((a) => drawArm(a.side, a.spec, a.j));

  // ---- body (rotates about the hips) ----
  p.rot = lean ? [rad(lean), 300, hipY] : null;
  layerArms("back");
  const sx = (x: number) => 300 + x;
  if (bot.kind === "pants") { // hips + leg tops in the trouser colour so the legs join the body
    const hips = blobPts(300, torsoBot - 0.05 * HH, { a: T.a * 1.02, b: 0.2 * HH, nTop: 2.2, nBot: 2.6, egg: 0, rot: 0, asym: 0, noise: 0.004, seed: 3 });
    p.gradFill(hips, bot.color, clothShade(bot.color), LIGHT); p.inkRing(hips, ow * 0.85, thick);
  }
  if (bot.kind === "shorts") {
    const wh = T.a * 0.95, yb = torsoBot + (bot.len ?? 0.5) * HH, w2 = 3 * u;
    const shorts: P2[] = [[sx(-wh), torsoBot - 0.24 * HH], [sx(wh), torsoBot - 0.24 * HH], [sx(wh + w2), yb], [sx(4 * u), yb], [sx(0), yb - 0.22 * HH], [sx(-4 * u), yb], [sx(-wh - w2), yb]];
    p.gradFill(shorts, bot.color, clothShade(bot.color), LIGHT);
    if (bot.hem) { p.stroke([[sx(-wh - w2 + u), yb - 6 * u], [sx(-4.5 * u), yb - 6 * u]], 2.4 * u, bot.hem); p.stroke([[sx(wh + w2 - u), yb - 6 * u], [sx(4.5 * u), yb - 6 * u]], 2.4 * u, bot.hem); }
    p.poly(shorts, null, ow * 0.85);
  }
  // upper garment
  const tp = blobPts(tcx, tcy, T);
  if (gown) {
    const hemW = col.kind === "saree" ? 1.3 : 1.55, sh = chin + 0.04 * HH;
    const R: P2[] = [], L: P2[] = [];
    for (let i = 0; i <= 12; i++) { const t = i / 12, y = sh + (hemY - sh) * t, w = T.a * (0.9 + (hemW - 0.9) * Math.pow(Math.max(0, (t - 0.28) / 0.72), 1.15)) * (1 + 0.04 * Math.sin(t * 3)); R.push([tcx + w, y]); L.push([tcx - w, y]); }
    const hemPts: P2[] = []; for (let i = 1; i < 10; i++) { const t = i / 10, w = T.a * hemW; hemPts.push([tcx + w - 2 * w * t, hemY + 3 * u * Math.sin(Math.PI * t)]); }
    const poly = [...R, ...hemPts, ...L.slice().reverse()];
    p.gradFill(poly, col.color, clothShade(col.color), LIGHT);
    if (col.kind === "tunic" && col.trim) { // embroidery: dotted hem band + neck line
      p.clip(poly, () => { for (let k = 0; k < 2; k++) p.stroke([[tcx - T.a * hemW, hemY - (7 + k * 6) * u], [tcx + T.a * hemW, hemY - (7 + k * 6) * u]], 1.8 * u, col.trim!); });
      if (col.cuff) p.clip(poly, () => p.stroke([[tcx - T.a * hemW, hemY - 8 * u], [tcx + T.a * hemW, hemY - 8 * u]], 7 * u, col.cuff!));
      if (id === "ira") for (let k = -3; k <= 3; k++) p.dot(tcx + k * 9 * u, hemY - 22 * u + 3 * u * (k % 2), 2 * u, col.trim);
    }
    p.inkRing(poly, ow, thick);
    if (col.kind === "tunic" && col.trim && id === "ira") { p.stroke([[tcx, chin + 0.1 * HH], [tcx, chin + 0.3 * HH]], 2 * u, col.trim); for (let k = 0; k < 4; k++) p.dot(tcx + (k % 2 ? 3 : -3) * u, chin + (0.12 + k * 0.05) * HH, 1.4 * u, col.trim); }
    if (col.kind === "tunic" && id === "titli") { p.arc(tcx, chin + 0.04 * HH, 0.14 * W, 0.07 * HH, 15, 165, 3.6 * u, col.trim!); for (let k = 0; k < 9; k++) p.dot(tcx + (rnd(5, k) - 0.5) * 1.6 * T.a, chin + (0.25 + rnd(5, k + 9) * 0.7) * HH, 1.8 * u, "#f7c27a"); }
    if (col.kind === "saree") { // blouse + pallu drape
      const blouseCol = id === "mummy" ? "#1f8a78" : "#e9962a", bl = blobPts(tcx, tcy - 0.12 * HH, { ...T, b: T.b * 0.72, egg: 0.04 });
      p.gradFill(bl, blouseCol, clothShade(blouseCol), LIGHT); p.inkRing(bl, ow * 0.9, thick);
      const sd = id === "mummy" ? -1 : 1, pal: P2[] = [[tcx - sd * 0.8 * T.a, chin + 0.05 * HH], [tcx - sd * 0.1 * T.a, chin + 0.0 * HH], [tcx + sd * 0.95 * T.a, chin + 0.55 * HH], [tcx + sd * 1.4 * T.a, torsoBot + 0.5 * HH], [tcx + sd * 1.3 * T.a, torsoBot + 0.95 * HH], [tcx + sd * 0.25 * T.a, torsoBot + 0.95 * HH], [tcx - sd * 0.05 * T.a, torsoBot - 0.05 * HH]];
      const palCol = id === "mummy" ? "#2aa592" : col.trim2!;
      p.gradFill(pal, palCol, clothShade(palCol), LIGHT);
      p.stroke([pal[0], pal[6]], 5 * u, col.trim!); p.stroke([pal[3], pal[4], pal[5]], 5 * u, col.trim!);
      p.poly(pal, null, ow * 0.8);
      if (id === "mummy") { p.stroke([[tcx - 1.0 * T.a, torsoBot + 0.1 * HH], [tcx + 1.2 * T.a, torsoBot + 0.1 * HH]], 6 * u, "#d8b04a"); for (let k = 0; k < 14; k++) p.dot(tcx + (rnd(9, k) - 0.5) * 2.4 * T.a, torsoBot + (0.2 + rnd(9, k + 20) * 0.7) * HH, 1.5 * u, "#e8f4ee"); }
    }
  } else {
    const shirtCol = col.color;
    p.gradFill(tp, shirtCol, clothShade(shirtCol), LIGHT);
    if (col.kind === "uniform") p.clip(tp, () => {
      p.stroke([[tcx - 1.2 * T.a, torsoBot - 0.14 * HH], [tcx + 1.2 * T.a, torsoBot - 0.14 * HH]], 0.1 * HH, col.trim2!); // belt
      p.poly([[tcx - 6 * u, torsoBot - 0.14 * HH - 6 * u], [tcx + 6 * u, torsoBot - 0.14 * HH - 6 * u], [tcx + 6 * u, torsoBot - 0.14 * HH + 6 * u], [tcx - 6 * u, torsoBot - 0.14 * HH + 6 * u]], "#d9b84a", 1.6 * u);
      for (const s of [-1, 1]) { const px = tcx + s * 0.5 * T.a, py = chin + 0.28 * HH; p.poly([[px - 9 * u, py], [px + 9 * u, py], [px + 9 * u, py + 15 * u], [px, py + 19 * u], [px - 9 * u, py + 15 * u]], mul(shirtCol, [0.94, 0.94, 0.94]), 1.6 * u); p.stroke([[px - 9 * u, py + 5 * u], [px + 9 * u, py + 5 * u]], 1.3 * u); }
      p.stroke([[tcx, chin + 0.1 * HH], [tcx, torsoBot - 0.2 * HH]], 1.6 * u, col.trim!); for (let k = 0; k < 4; k++) p.dot(tcx, chin + (0.2 + k * 0.17) * HH, 1.8 * u, "#d9b84a");
    });
    if (id === "tinku") p.clip(tp, () => { p.stroke([[tcx - 0.7 * T.a, chin + 0.02 * HH], [tcx + 0.9 * T.a, torsoBot - 0.05 * HH]], 6.5 * u, "#7a5030"); });
    p.inkRing(tp, ow, thick);
    if (col.kind === "polo") { // collar + placket + chest pocket with pens
      for (const s of [-1, 1]) p.poly([[tcx + s * 2 * u, chin + 0.02 * HH], [tcx + s * 17 * u, chin - 0.02 * HH], [tcx + s * 13 * u, chin + 0.13 * HH]], col.trim!, 1.8 * u);
      p.stroke([[tcx, chin + 0.04 * HH], [tcx, chin + 0.3 * HH]], 1.8 * u, col.trim!);
      const px = tcx + 0.4 * T.a, py = chin + 0.38 * HH; p.poly([[px - 8 * u, py], [px + 8 * u, py], [px + 8 * u, py + 14 * u], [px - 8 * u, py + 14 * u]], mul(col.color, [1.1, 1.1, 1.1]), 1.5 * u);
      for (const k of [-4, 0, 4]) p.stroke([[px + k * u, py - 4 * u], [px + k * u, py + 3 * u]], 1.3 * u, ["#e8c040", "#e8e8f0", "#c0262e"][k / 4 + 1]);
    }
    if (col.kind === "tee") { p.arc(tcx, chin + 0.04 * HH, 0.13 * W, 0.06 * HH, 15, 165, 3.2 * u, col.trim!); p.arc(tcx + 2 * u, tcy + 0.2 * HH, 3 * u, 2 * u, 20, 160, 1.4 * u, col.trim!); }
    if (col.kind === "uniform") for (const s of [-1, 1]) { p.poly([[tcx + s * 2 * u, chin + 0.0 * HH], [tcx + s * 20 * u, chin - 0.02 * HH], [tcx + s * 15 * u, chin + 0.16 * HH]], col.trim!, 1.8 * u); p.poly([[tcx + s * 0.62 * T.a, chin + 0.07 * HH], [tcx + s * 1.0 * T.a, chin + 0.12 * HH], [tcx + s * 0.95 * T.a, chin + 0.2 * HH], [tcx + s * 0.62 * T.a, chin + 0.15 * HH]], col.trim!, 1.5 * u); }
  }
  if (plateOn) { const py = chin + 0.72 * HH; p.ell(tcx, py, 46 * u, 9 * u, "#c8ccd4", 2.4 * u); for (let k = 0; k < 3; k++) p.ell(tcx + (k - 1) * 9 * u, py - (3 + k * 3) * u, 24 * u, 7 * u, "#e3b878", 2 * u, 0, 360, (k - 1) * 6); }
  if (sp.braid) { const bx = (k: number): P2 => [tcx - 0.85 * T.a + k * 1.5 * u, chin + 0.12 * HH + k * 0.12 * HH]; for (let k = 0; k < 7; k++) p.ell(bx(k)[0], bx(k)[1], 9 * u, 7.5 * u, k % 2 ? "#14101a" : "#2a2230", 2 * u, 0, 360, k % 2 ? 25 : -25); }
  if (sp.bag) { const bx = tcx + 1.02 * T.a, by = torsoBot - 0.05 * HH; p.poly([[bx - 12 * u, by], [bx + 12 * u, by], [bx + 12 * u, by + 26 * u], [bx - 12 * u, by + 26 * u]], "#8a6038", 2.2 * u); p.poly([[bx - 12 * u, by], [bx + 12 * u, by], [bx + 10 * u, by + 12 * u], [bx - 10 * u, by + 12 * u]], "#6d4a28", 2 * u); p.dot(bx, by + 13 * u, 2 * u, "#d9b84a"); }
  layerArms("mid");

  // ---- head ----
  const A2 = lean + (S.headTilt ?? 0), [cpx, cpy] = rotAbout([300, chin], rad(lean), [300, hipY]);
  p.rot = A2 ? [rad(A2), 300, chin, cpx - 300, cpy - chin] : null;
  const b = sp.back;
  if (b) {
    if (b.kind === "bob") p.poly(blobPts(300, hc + 0.14 * H.b, { ...H, a: A * 1.16, b: H.b * 1.0, egg: 0.0, asym: 0, nBot: 2.6 }), b.color, ow * 0.85);
    if (b.kind === "long") p.poly(blobPts(300, hc + 0.04 * H.b, { ...H, a: A * 1.07, b: H.b * 1.02, egg: 0.0, asym: 0 }), b.color, ow * 0.85);
    if (b.kind === "bun") p.ell(300, hc - 1.0 * H.b, 0.32 * A, 0.27 * H.b, b.color, ow * 0.85);
    if (b.kind === "pigtails") for (const s of [-1, 1]) {
      p.ell(300 + s * 1.22 * A, hc - 0.34 * H.b, 0.34 * A, 0.7 * H.b, b.color, ow * 0.85, 0, 360, -s * 22);
      p.ell(300 + s * 0.98 * A, hc - 0.74 * H.b, 5.5 * u, 4 * u, b.clips![0], 1.6 * u, 0, 360, -s * 30); p.ell(300 + s * 0.98 * A + s * 6 * u, hc - 0.74 * H.b - 2 * u, 5.5 * u, 4 * u, b.clips![1], 1.6 * u, 0, 360, s * 30);
    }
  }
  if (!sp.hair || sp.hair.kind !== "none") for (const side of [-1, 1]) p.ell(300 + side * A * 0.97, hc + 0.1 * H.b, 8 * u, 11 * u, skin, ow * 0.8); // ears
  if (sp.earrings) for (const side of [-1, 1]) p.ell(300 + side * A * 0.99, hc + 0.3 * H.b, 3.4 * u, 3.4 * u, sp.earrings, 1.4 * u);
  const hp = blobPts(300, hc, H);
  p.shadedFill(hp, skin, mul(skin, SH_SKIN), LIGHT, H.a); p.inkRing(hp, ow, thick);
  const hr = sp.hair;
  if (hr.kind !== "none") {
    const poly = hairPoly(hp, 300, hc, H, u, hr);
    p.poly(poly, hr.color, ow * 0.8);
    if (hr.hi) for (const [a, k, c] of [[[-34, -36], [-16, -46], [4, -44]], [[10, -42], [24, -40], [34, -33]]] as [P2, P2, P2][])
      if (hr.kind !== "sides") p.stroke(curve([300 + a[0] * u, hc + a[1] * u], [300 + k[0] * u, hc + k[1] * u], [300 + c[0] * u, hc + c[1] * u]), 2.2 * u, hr.hi);
    if (hr.part) p.stroke([[300, hc - 0.98 * H.b], [300 + 3 * u, hc - 24 * u]], 2 * u, mul(hr.color, [0.55, 0.55, 0.6]));
  }
  if (sp.cap) { // peaked khaki cap with badge
    const capC = "#b9b27e", band = "#5a4228", yb = hc - 0.28 * H.b, yt = hc - 1.3 * H.b;
    const body: P2[] = [[300 - 0.82 * A, yb], [300 - 0.9 * A, yt + 12 * u], [300 - 0.55 * A, yt], [300 + 0.55 * A, yt], [300 + 0.9 * A, yt + 12 * u], [300 + 0.82 * A, yb]];
    p.gradFill(body, capC, mul(capC, SH_CLOTH), LIGHT); p.poly(body, null, ow * 0.85);
    p.poly([[300 - 0.84 * A, yb - 0.26 * H.b], [300 + 0.84 * A, yb - 0.26 * H.b], [300 + 0.82 * A, yb], [300 - 0.82 * A, yb]], band, 2 * u);
    p.ell(300, yb + 1 * u, 0.62 * A, 0.12 * H.b, band, ow * 0.7, 0, 180);
    p.ell(300, yb - 0.13 * H.b, 6 * u, 6 * u, "#d9b84a", 1.6 * u);
  }
  face(p, 300, hc, u, F, facing, A * 0.97, sp, skin);
  if (sp.necklace) p.arc(300, chin + 0.02 * HH, 0.2 * W, 0.2 * HH, 25, 155, 2.8 * u, "#14101a");
  if (id === "ira") { for (let k = 0; k < 5; k++) { const a = rad(k * 72); p.ell(300 + 0.72 * A + Math.cos(a) * 4 * u, hc - 12 * u + Math.sin(a) * 4 * u, 3.2 * u, 3.2 * u, WHITE, 1.2 * u); } p.dot(300 + 0.72 * A, hc - 12 * u, 2 * u, "#f0c030"); }
  layerArms("top");
  p.rot = null;
};

// ---------------- Jugnu: a real firefly beetle (not human-like) ----------------
const GLOWY = "#d8f066";
export const drawJugnu = (g: CanvasRenderingContext2D, pose: Pose) => {
  const p = new Pen(g); p.rot = null; p.ol = 3.6;
  type V = { top?: boolean; wing: number; glow: number; ant: number; tilt: number; eye: "dot" | "wide" | "happy" | "squeeze"; rays?: boolean; tuck?: boolean; sweat?: boolean; perched?: boolean };
  const V: Record<Pose, V> = {
    stand: { wing: 30, glow: 0.8, ant: 0, tilt: -6, eye: "dot" },
    walk: { wing: 55, glow: 0.8, ant: 6, tilt: -16, eye: "dot" },
    point: { top: true, wing: 38, glow: 0.7, ant: 0, tilt: 0, eye: "dot" },
    think: { wing: 8, glow: 0.35, ant: -16, tilt: 0, eye: "dot", perched: true, tuck: true },
    happy: { wing: 44, glow: 1, ant: 18, tilt: -10, eye: "happy", rays: true },
    surprised: { wing: 72, glow: 0.9, ant: 34, tilt: 4, eye: "wide" },
    scared: { wing: 5, glow: 0.15, ant: -26, tilt: 10, eye: "wide", tuck: true, sweat: true },
    laugh: { wing: 60, glow: 1, ant: 12, tilt: -14, eye: "squeeze", rays: true },
  };
  const v = V[pose], cx = 300, cy = 520, lamp = (x: number, y: number, r: number, a: number) => {
    const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, `rgba(235,255,120,${0.95 * a})`); gr.addColorStop(0.45, `rgba(200,240,90,${0.45 * a})`); gr.addColorStop(1, "rgba(200,240,90,0)");
    g.fillStyle = gr; g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill();
  };
  p.rot = [rad(v.tilt), cx, cy];
  if (v.top) { // dorsal view, facing up
    lamp(cx, cy + 150, 180, v.glow);
    for (const s of [-1, 1]) {
      p.ell(cx + s * 120, cy - 20, 125, 46, "rgba(240,246,255,0.55)", 3.4, 0, 360, s * (-62 + v.wing * 0.4));
      p.stroke([[cx + s * 40, cy - 50], [cx + s * 190, cy - 130]], 1.6, "rgba(36,23,38,0.5)");
    }
    p.ell(cx, cy + 40, 66, 150, "#25222a", 4); p.stroke([[cx, cy - 100], [cx, cy + 185]], 2.4, "#e8dcc0");
    p.ell(cx, cy + 190, 40, 28, GLOWY, 3.4);
    p.ell(cx, cy - 118, 60, 52, "#c8782e", 4); for (const [dx, dy] of [[-22, -8], [22, -8], [0, 14]]) p.dot(cx + dx, cy - 118 + dy, 6, "#8a4a1a");
    p.ell(cx, cy - 172, 30, 26, "#2a2420", 3.4); for (const s of [-1, 1]) { p.dot(cx + s * 14, cy - 178, 6, WHITE); p.dot(cx + s * 14, cy - 177, 3.2); p.line(curve([cx + s * 12, cy - 190], [cx + s * 40, cy - 235], [cx + s * (50 + v.ant * 0.5), cy - 255]), "#1a1620", 3, false); }
    p.rot = null; return;
  }
  const per = !!v.perched;
  lamp(cx + 120, cy + 70, 200, v.glow);
  if (v.rays) for (let k = 0; k < 9; k++) { const a = rad(-30 + k * 26 + 8), r0 = 120, r1 = 165; p.stroke([[cx + 120 + Math.cos(a) * r0, cy + 70 + Math.sin(a) * r0], [cx + 120 + Math.cos(a) * r1, cy + 70 + Math.sin(a) * r1]], 5, "#e8f58a"); }
  // legs (short, under the body)
  const legY = cy + (per ? 108 : 78);
  for (const [x0, dx, kn] of [[cx - 70, -26, 40], [cx + 0, 8, 46], [cx + 70, 30, 40]] as const) p.line(curve([x0, legY - 12], [x0 + dx * 0.4 + (v.tuck ? 8 : 0), legY + kn * 0.5], [x0 + dx, legY + kn + (per ? 6 : (v.tuck ? -6 : 0))]), "#3a2a20", 7);
  // wings (behind the body, hinge on the back)
  for (const [k, ang, len, al] of [[0, -62 + v.wing * 0.5, 215, 0.55], [1, -38 + v.wing * 0.4, 190, 0.45]] as const) {
    const a = rad(ang); const ex = cx + 20 + Math.cos(a) * len * 0.5, ey = cy - 55 + Math.sin(a) * len * 0.5;
    if (v.tuck) p.ell(cx + 70 - k * 10, cy - 52 + k * 8, 150, 20, `rgba(240,246,255,${al})`, 3, 0, 360, 6);
    else { p.ell(ex, ey, len * 0.5, 40 - k * 6, `rgba(240,246,255,${al})`, 3.4, 0, 360, ang); p.stroke([[cx + 20, cy - 55], [cx + 20 + Math.cos(a) * len * 0.92, cy - 55 + Math.sin(a) * len * 0.92]], 1.6, "rgba(36,23,38,0.55)"); }
  }
  // abdomen glow tip, elytra, pronotum, head
  p.ell(cx + 120, cy + 62, 72, 44, GLOWY, 3.6, 0, 360, 14);
  p.ell(cx + 45, cy + 20, 160, 82, "#25222a", 4.4, 0, 360, 10);
  p.clip(blobEll(cx + 45, cy + 20, 160, 82, 10), () => { p.stroke([[cx - 110, cy + 2], [cx + 220, cy + 56]], 3, "#e8dcc0"); p.arc(cx + 45, cy + 20, 150, 74, 188, 262, 3.2, "rgba(255,255,255,0.28)"); });
  p.ell(cx - 112, cy - 4, 74, 66, "#c8782e", 4.4); for (const [dx, dy] of [[-22, -14], [14, -22], [20, 14], [-14, 18]]) p.dot(cx - 112 + dx, cy - 4 + dy, 6.5, "#8a4a1a");
  p.arc(cx - 112, cy - 4, 56, 50, 200, 255, 3, "rgba(255,255,255,0.35)");
  p.ell(cx - 168, cy + 52, 38, 33, "#2a2420", 3.6);
  const ex = cx - 178, ey = cy + 46;
  switch (v.eye) {
    case "dot": p.ell(ex, ey, 11, 12, WHITE, 2.4); p.dot(ex - 2, ey + 1, 5.2); break;
    case "wide": p.ell(ex, ey, 14, 14, WHITE, 2.6); p.dot(ex - 1, ey + 1, 4.2); break;
    case "happy": p.arc(ex, ey + 4, 12, 9, 200, 340, 4); break;
    case "squeeze": p.stroke([[ex + 8, ey - 8], [ex - 8, ey], [ex + 8, ey + 8]], 4); break;
  }
  p.arc(cx - 178, cy + 66, 11, 7, 20, 160, 3);
  for (const k of [0, 1]) { const a = k ? 24 : -4; p.line(curve([cx - 190, cy + 36], [cx - 232, cy - 20 - v.ant], [cx - 262 + k * 12, cy - 50 - v.ant * 1.5 - a]), "#1a1620", 3.4, false); p.dot(cx - 262 + k * 12, cy - 50 - v.ant * 1.5 - a, 5.2, "#1a1620"); }
  if (v.sweat) p.poly([[cx - 120, cy - 100], [cx - 112, cy - 84], [cx - 120, cy - 74], [cx - 128, cy - 84]], SWEAT, 2.4);
  p.rot = null;
};
const blobEll = (cx: number, cy: number, rx: number, ry: number, rot: number): P2[] => {
  const r = rad(rot), pts: P2[] = [];
  for (let i = 0; i < 48; i++) { const a = (i / 48) * Math.PI * 2, x = rx * Math.cos(a), y = ry * Math.sin(a); pts.push([cx + x * Math.cos(r) - y * Math.sin(r), cy + x * Math.sin(r) + y * Math.cos(r)]); }
  return pts;
};
