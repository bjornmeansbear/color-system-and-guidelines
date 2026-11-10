// The palette, read straight from the repo's kit.css, so the site can never
// drift from the kit. Shared by the pages and by the vote endpoint, which
// uses the same contrast rules to reject sets the voter could never show.
import kit from '../../../kit.css?raw';

export type RGB = [number, number, number];

export interface Color {
	/** Token name without the leading dashes: "pink-5", "wjerk-navy". */
	name: string;
	/** Scale name ("pink"), or "wjerk" for the original palette. */
	family: string;
	/** 0–9 on a scale, null for an original. */
	step: number | null;
	rgb: RGB;
	hex: string;
	/** WCAG relative luminance. */
	lum: number;
	/** OKLCH chroma and hue, for telling an accent from a neutral. */
	chroma: number;
	hue: number;
}

// Only the light-mode :root block holds literal colors.
const lightBlock = kit.split('/* ---- dark mode')[0];

function channel(v: number) {
	v /= 255;
	return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4;
}

function luminance([r, g, b]: RGB) {
	return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b);
}

function oklch([r, g, b]: RGB): { chroma: number; hue: number } {
	const [lr, lg, lb] = [r, g, b].map((v) => {
		v /= 255;
		return v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4;
	});
	const l = Math.cbrt(0.4122214708 * lr + 0.5363325363 * lg + 0.0514459929 * lb);
	const m = Math.cbrt(0.2119034982 * lr + 0.6806995451 * lg + 0.1073969566 * lb);
	const s = Math.cbrt(0.0883024619 * lr + 0.2817188376 * lg + 0.6299787005 * lb);
	const a = 1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s;
	const b2 = 0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s;
	return { chroma: Math.hypot(a, b2), hue: ((Math.atan2(b2, a) * 180) / Math.PI + 360) % 360 };
}

const toHex = (rgb: RGB) => '#' + rgb.map((v) => v.toString(16).padStart(2, '0')).join('').toUpperCase();

function make(name: string, family: string, step: number | null, rgb: RGB): Color {
	return { name, family, step, rgb, hex: toHex(rgb), lum: luminance(rgb), ...oklch(rgb) };
}

const colors: Color[] = [];

for (const [, family, step, r, g, b] of lightBlock.matchAll(
	/--([a-z-]+)-(\d):\s*rgb\((\d+),\s*(\d+),\s*(\d+)\)/g
)) {
	colors.push(make(`${family}-${step}`, family, Number(step), [Number(r), Number(g), Number(b)]));
}

for (const [, name, hex] of lightBlock.matchAll(/--(wjerk-[a-z-]+):\s*#([0-9A-Fa-f]{6})/g)) {
	const rgb = [0, 2, 4].map((i) => parseInt(hex.slice(i, i + 2), 16)) as RGB;
	colors.push(make(name, 'wjerk', null, rgb));
}

export const COLORS = colors;
export const BY_NAME = new Map(colors.map((c) => [c.name, c]));

/** Scales in spectrum order (by the hue of step 5), then the neutrals. */
const NEUTRALS = ['brown', 'gray', 'dark-gray', 'light-gray', 'purple-gray', 'white', 'black'];
const families = [...new Set(colors.filter((c) => c.step !== null).map((c) => c.family))];
const hueOf = (f: string) => BY_NAME.get(`${f}-5`)!.hue;
export const HUE_SCALES = families
	.filter((f) => !NEUTRALS.includes(f))
	.sort((a, b) => ((hueOf(a) + 330) % 360) - ((hueOf(b) + 330) % 360));
export const NEUTRAL_SCALES = NEUTRALS.filter((f) => families.includes(f));
export const ORIGINALS = colors.filter((c) => c.family === 'wjerk');

export function scale(family: string): Color[] {
	return colors.filter((c) => c.family === family).sort((a, b) => a.step! - b.step!);
}

/** WCAG 2 contrast ratio. Symmetric: which color is the text doesn't matter. */
export function contrast(a: Color, b: Color): number {
	const [hi, lo] = a.lum > b.lum ? [a.lum, b.lum] : [b.lum, a.lum];
	return (hi + 0.05) / (lo + 0.05);
}

export type Grade = 'AAA' | 'AA' | 'Large' | 'Fail';

export function grade(ratio: number): Grade {
	if (ratio >= 7) return 'AAA';
	if (ratio >= 4.5) return 'AA';
	if (ratio >= 3) return 'Large';
	return 'Fail';
}

/** A ground light type can sit on at AA: measured, not eyeballed. */
export const isDark = (c: Color) => c.lum <= 0.183;

/**
 * The step cheat sheet: for each pair of steps, the worst and best contrast
 * across every hue scale paired with every hue scale (white and black are
 * materials, not hues, so they're left out).
 */
export function stepMatrix(): { min: number; max: number }[][] {
	const hueScales = [...HUE_SCALES, ...NEUTRAL_SCALES.filter((f) => f !== 'white' && f !== 'black')];
	const byStep = Array.from({ length: 10 }, (_, s) =>
		hueScales.map((f) => BY_NAME.get(`${f}-${s}`)).filter(Boolean) as Color[]
	);
	return byStep.map((rowColors, i) =>
		byStep.map((colColors, j) => {
			let min = Infinity;
			let max = 0;
			if (i !== j) {
				for (const a of rowColors)
					for (const b of colColors) {
						const r = contrast(a, b);
						if (r < min) min = r;
						if (r > max) max = r;
					}
			}
			return { min: i === j ? 1 : min, max: i === j ? 1 : max };
		})
	);
}

// ---- sets of three, for the voter ----

export interface Trio {
	ground: Color;
	text: Color;
	accent: Color;
}

const ACCENT_CHROMA = 0.07;

function hueGap(a: number, b: number) {
	const d = Math.abs(a - b) % 360;
	return d > 180 ? 360 - d : d;
}

/**
 * The rules every voting card follows: text and accent each clear AA on the
 * ground, the accent is a real color (not a gray), and it reads as a
 * different color from the text.
 */
export function validTrio({ ground, text, accent }: Trio): boolean {
	if (contrast(text, ground) < 4.5) return false;
	if (contrast(accent, ground) < 4.5) return false;
	if (accent.chroma < ACCENT_CHROMA) return false;
	if (accent.name === text.name || accent.name === ground.name) return false;
	if (text.chroma >= 0.04 && hueGap(text.hue, accent.hue) < 30) return false;
	return true;
}

const pick = <T>(list: T[]) => list[Math.floor(Math.random() * list.length)];

export function randomTrio(): Trio {
	for (;;) {
		const ground = pick(colors);
		const texts = colors.filter((c) => contrast(c, ground) >= 4.5);
		if (!texts.length) continue;
		const text = pick(texts);
		const accents = colors.filter((c) => validTrio({ ground, text, accent: c }));
		if (!accents.length) continue;
		return { ground, text, accent: pick(accents) };
	}
}
