<script lang="ts">
	import { onMount } from 'svelte';
	import { contrast, grade, randomTrio, type Trio } from '#lib/palette.ts';
	import endings from '#lib/endings.json';

	const pick = <T,>(list: T[]) => list[Math.floor(Math.random() * list.length)];

	let trio = $state<Trio | null>(null);
	let ending = $state('');
	let last = $state<{ trio: Trio; liked: boolean } | null>(null);
	let count = $state(0);
	let error = $state('');
	let voter = '';

	function next() {
		trio = randomTrio();
		ending = pick(endings as string[]);
	}

	// A random id this browser keeps, so one person's votes count once per
	// set. It identifies nobody. If storage is blocked, a fresh id per visit.
	function voterId() {
		try {
			let id = localStorage.getItem('wjavelength-voter');
			if (!id) {
				id = crypto.randomUUID();
				localStorage.setItem('wjavelength-voter', id);
			}
			return id;
		} catch {
			return crypto.randomUUID();
		}
	}

	async function vote(liked: boolean) {
		if (!trio) return;
		const voted = trio;
		last = { trio: voted, liked };
		count += 1;
		next();
		try {
			const res = await fetch('/api/vote', {
				method: 'POST',
				headers: { 'content-type': 'application/json' },
				body: JSON.stringify({
					ground: voted.ground.name,
					text: voted.text.name,
					accent: voted.accent.name,
					liked,
					voter
				})
			});
			error = res.ok ? '' : "That vote didn't save. The next ones might.";
		} catch {
			error = "That vote didn't save. Are you offline?";
		}
	}

	function onkey(e: KeyboardEvent) {
		if (e.metaKey || e.ctrlKey || e.altKey) return;
		if (e.key === 'y' || e.key === 'ArrowRight') vote(true);
		else if (e.key === 'n' || e.key === 'ArrowLeft') vote(false);
		else if (e.key === 's') next();
	}

	onMount(() => {
		voter = voterId();
		next();
	});
</script>

<svelte:head>
	<title>Vote — Wjavelength</title>
</svelte:head>

<svelte:window onkeydown={onkey} />

<h1>Vote</h1>
<p class="lede">
	Every set below passes AA: the text and the accent each clear 4.5:1 on the ground. That makes it
	readable. Is it any good? Yes or no, go with your gut.
</p>

{#if trio}
	<section class="card" style="background: {trio.ground.hex}; color: {trio.text.hex}" aria-label="Color set to vote on">
		<p class="poster">
			To really appreciate design you
			<em style="color: {trio.accent.hex}">{ending}</em>
		</p>
		<p class="body">
			Body text in the same ink, at the size people actually read. A
			<span class="link" style="color: {trio.accent.hex}; text-decoration-color: {trio.accent.hex}">link in the accent</span>
			sits in the middle of it.
		</p>
	</section>

	<div class="actions">
		<button type="button" class="btn no" onclick={() => vote(false)}>No <kbd>N</kbd></button>
		<button type="button" class="btn yes" onclick={() => vote(true)}>Yes <kbd>Y</kbd></button>
		<button type="button" class="skip-btn" onclick={next}>Skip <kbd>S</kbd></button>
	</div>
{:else}
	<p class="muted">Mixing a set…</p>
	<noscript><p>The voter needs JavaScript.</p></noscript>
{/if}

<div aria-live="polite">
	{#if error}<p class="error">{error}</p>{/if}

	{#if last}
		{@const t = last.trio}
		<section class="last">
			<h2>You said {last.liked ? 'yes' : 'no'} to</h2>
			<ul>
				{#each [['Ground', t.ground], ['Text', t.text], ['Accent', t.accent]] as const as [role, c]}
					<li>
						<span class="chip" style="background: {c.hex}" aria-hidden="true"></span>
						<span>
							<span class="role">{role}</span>
							<span class="mono">{c.name}</span>
							{#if role !== 'Ground'}
								{@const r = contrast(c, t.ground)}
								<span class="mono">{r.toFixed(2)}:1</span>
								<span class="badge" data-grade={grade(r)}>{grade(r)}</span>
							{/if}
						</span>
					</li>
				{/each}
			</ul>
			<p class="muted">
				{count} {count === 1 ? 'vote' : 'votes'} this visit. <a href="/results">See what everyone thinks.</a>
			</p>
		</section>
	{/if}
</div>

<style>
	.card {
		border: 2px solid var(--color-border);
		padding: 1.5rem;
		min-height: 18rem;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		gap: 1.5rem;
	}

	@media (min-width: 40rem) {
		.card {
			padding: 3rem;
			min-height: 24rem;
		}
	}

	.poster {
		font-family: var(--font-display);
		font-weight: bold;
		font-size: var(--text-2xl);
		line-height: var(--leading-2xl);
		margin: 0;
		text-wrap: balance;
	}

	.poster em {
		display: block;
	}

	@media (min-width: 55rem) {
		.poster {
			font-size: 3.5rem;
			line-height: 3.75rem;
		}
	}

	.body {
		margin: 0;
		max-width: 32rem;
	}

	.link {
		text-decoration: underline;
		text-decoration-thickness: 2px;
		text-underline-offset: 0.2em;
	}

	.actions {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.75rem;
		margin-top: 1.125rem;
	}

	.actions .btn {
		min-width: 8rem;
		font-weight: bold;
	}

	.yes {
		background: var(--color-text);
		color: var(--color-bg);
	}

	.yes:hover {
		background: var(--color-accent) !important;
		border-color: var(--color-accent);
	}

	kbd {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		font-weight: normal;
		opacity: 0.8;
		margin-left: 0.375rem;
	}

	.skip-btn {
		font: inherit;
		background: none;
		border: 0;
		color: var(--color-text);
		text-decoration: underline;
		text-decoration-color: var(--color-accent);
		text-underline-offset: 0.2em;
		min-height: 2.75rem;
		padding: 0 0.75rem;
		cursor: pointer;
	}

	.error {
		margin-top: 1.125rem;
		font-weight: bold;
	}

	.last {
		margin-top: 2.25rem;
		border-top: 2px solid var(--color-border);
		padding-top: 1.125rem;
	}

	.last h2 {
		font-size: var(--text-lg);
		line-height: var(--leading-lg);
		margin-bottom: 0.75rem;
	}

	.last ul {
		list-style: none;
		margin: 0 0 1.125rem;
		padding: 0;
		display: grid;
		gap: 0.5rem;
	}

	.last li {
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}

	.last li > span:last-child {
		display: flex;
		flex-wrap: wrap;
		gap: 0.25rem 0.75rem;
		align-items: baseline;
	}

	.role {
		font-weight: bold;
		min-width: 4rem;
	}

	.chip {
		width: 2.25rem;
		height: 2.25rem;
		border: 1px solid var(--color-border);
		flex: none;
	}
</style>
