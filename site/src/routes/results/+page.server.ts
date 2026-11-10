import { env } from 'cloudflare:workers';
import { BY_NAME, isDark } from '#lib/palette.ts';
import type { PageServerLoad } from './$types';

export const prerender = false;

interface Row {
	n: number;
	yes: number;
}

/**
 * Wilson score bounds for a yes-share: how sure we can be, given how few
 * votes there are. Ranking by the lower bound keeps a set with 1 yes from 1
 * vote from outranking one with 40 from 45.
 */
function wilson(yes: number, n: number, z = 1.96) {
	if (n === 0) return { low: 0, high: 1 };
	const p = yes / n;
	const denom = 1 + (z * z) / n;
	const centre = p + (z * z) / (2 * n);
	const spread = z * Math.sqrt((p * (1 - p)) / n + (z * z) / (4 * n * n));
	return { low: (centre - spread) / denom, high: (centre + spread) / denom };
}

const familyOf = (name: string) => {
	const c = BY_NAME.get(name);
	return !c ? name : c.family === 'wjerk' ? 'originals' : c.family;
};

function tally(rows: (Row & { key: string })[]) {
	const out = new Map<string, Row>();
	for (const r of rows) {
		const t = out.get(r.key) ?? { n: 0, yes: 0 };
		t.n += r.n;
		t.yes += r.yes;
		out.set(r.key, t);
	}
	return [...out]
		.map(([key, t]) => ({ key, ...t, share: t.yes / t.n, ...wilson(t.yes, t.n) }))
		.sort((a, b) => b.low - a.low);
}

export const load: PageServerLoad = async () => {
	const db = env.DB;
	if (!db) return { connected: false as const };

	const [totals, sets, grounds, accents] = await Promise.all([
		db
			.prepare('SELECT COUNT(*) AS votes, COUNT(DISTINCT voter) AS voters, COALESCE(SUM(liked), 0) AS yes FROM votes')
			.first<{ votes: number; voters: number; yes: number }>(),
		db
			.prepare(
				`SELECT ground, text, accent, COUNT(*) AS n, SUM(liked) AS yes
				 FROM votes GROUP BY ground, text, accent HAVING n >= 3`
			)
			.all<{ ground: string; text: string; accent: string } & Row>(),
		db.prepare('SELECT ground AS name, COUNT(*) AS n, SUM(liked) AS yes FROM votes GROUP BY ground').all<{ name: string } & Row>(),
		db.prepare('SELECT accent AS name, COUNT(*) AS n, SUM(liked) AS yes FROM votes GROUP BY accent').all<{ name: string } & Row>()
	]);

	const ranked = sets.results
		.filter((s) => BY_NAME.has(s.ground) && BY_NAME.has(s.text) && BY_NAME.has(s.accent))
		.map((s) => ({ ...s, share: s.yes / s.n, ...wilson(s.yes, s.n) }));

	// A set lands on one list or the other, never both.
	const best = ranked.filter((s) => s.share >= 0.5).sort((a, b) => b.low - a.low).slice(0, 8);
	const worst = ranked.filter((s) => s.share < 0.5).sort((a, b) => a.high - b.high).slice(0, 8);

	return {
		connected: true as const,
		totals: totals ?? { votes: 0, voters: 0, yes: 0 },
		best,
		worst,
		groundFamilies: tally(grounds.results.map((r) => ({ ...r, key: familyOf(r.name) }))),
		accentFamilies: tally(accents.results.map((r) => ({ ...r, key: familyOf(r.name) }))),
		lightDark: tally(
			grounds.results.map((r) => {
				const c = BY_NAME.get(r.name);
				return { ...r, key: c && isDark(c) ? 'Dark grounds' : 'Light grounds' };
			})
		)
	};
};
