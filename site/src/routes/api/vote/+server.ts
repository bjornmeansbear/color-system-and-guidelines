import { error, json } from '@sveltejs/kit';
import { env } from 'cloudflare:workers';
import { BY_NAME, validTrio } from '#lib/palette.ts';
import type { RequestHandler } from './$types';

export const prerender = false;

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export const POST: RequestHandler = async ({ request }) => {
	const db = env.DB;
	if (!db) error(503, 'No database connected');

	let body: Record<string, unknown>;
	try {
		body = await request.json();
	} catch {
		error(400, 'Expected JSON');
	}

	const { ground, text, accent, liked, voter } = body;
	const g = BY_NAME.get(String(ground));
	const t = BY_NAME.get(String(text));
	const a = BY_NAME.get(String(accent));

	// Only sets the voter could actually have shown are counted.
	if (!g || !t || !a || !validTrio({ ground: g, text: t, accent: a })) {
		error(400, 'Not a set the voter makes');
	}
	if (typeof liked !== 'boolean') error(400, 'liked must be true or false');
	if (typeof voter !== 'string' || !UUID.test(voter)) error(400, 'Bad voter id');

	// One vote per person per set: voting on the same set again replaces it.
	await db
		.prepare(
			`INSERT INTO votes (ground, text, accent, liked, voter) VALUES (?1, ?2, ?3, ?4, ?5)
			 ON CONFLICT (voter, ground, text, accent) DO UPDATE SET liked = excluded.liked, created_at = datetime('now')`
		)
		.bind(g.name, t.name, a.name, liked ? 1 : 0, voter)
		.run();

	return json({ ok: true });
};
