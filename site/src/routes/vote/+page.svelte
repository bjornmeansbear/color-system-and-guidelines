<script lang="ts">
	import { onMount } from 'svelte';
	import { contrast, grade, randomTrio, type Trio } from '#lib/palette.ts';
	import endings from '#lib/endings.json';

	// One card per set. The front card is the one being voted on; the two
	// behind it are the sets coming next, so their grounds show at the edges.
	type Card = { id: number; trio: Trio; ending: string; tilt: number };
	type Ghost = Card & { liked: boolean };

	const PILE = 3;
	let serial = 0;

	const pick = <T,>(list: T[]) => list[Math.floor(Math.random() * list.length)];

	// Pile tilt per RULES.md "rotation as an accent": 1.5–4deg, random,
	// alternating sides, fixed for the card's life.
	function deal(): Card {
		serial += 1;
		const side = serial % 2 ? 1 : -1;
		return {
			id: serial,
			trio: randomTrio(),
			ending: pick(endings as string[]),
			tilt: side * (1.5 + Math.random() * 2.5)
		};
	}

	let pile = $state<Card[]>([]);
	let ghost = $state<Ghost | null>(null);
	let last = $state<{ trio: Trio; liked: boolean } | null>(null);
	let count = $state(0);
	let error = $state('');
	let voter = '';
	let ghostTimer: ReturnType<typeof setTimeout> | undefined;

	const front = $derived(pile[0]);

	function advance() {
		pile = [...pile.slice(1), deal()];
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
		if (!front) return;
		const card = front;
		last = { trio: card.trio, liked };
		count += 1;

		// The voted card stays on top for a moment as a ghost: the stamp lands,
		// then it leaves toward the side of the answer. The pile has already
		// moved on underneath, so the next vote can come straight away.
		ghost = { ...card, liked };
		clearTimeout(ghostTimer);
		ghostTimer = setTimeout(() => (ghost = null), 900);
		advance();

		try {
			const res = await fetch('/api/vote', {
				method: 'POST',
				headers: { 'content-type': 'application/json' },
				body: JSON.stringify({
					ground: card.trio.ground.name,
					text: card.trio.text.name,
					accent: card.trio.accent.name,
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
		const target = e.target as HTMLElement | null;
		if (target?.closest('input, select, textarea')) return;
		if (e.key === 'y' || e.key === 'ArrowRight') vote(true);
		else if (e.key === 'n' || e.key === 'ArrowLeft') vote(false);
		else if (e.key === 's') advance();
	}

	onMount(() => {
		voter = voterId();
		pile = Array.from({ length: PILE }, deal);
		return () => clearTimeout(ghostTimer);
	});
</script>

<svelte:head>
	<title>Vote — Wjavelength</title>
</svelte:head>

<svelte:window onkeydown={onkey} />

<div class="intro">
	<h1>Vote</h1>
	<p>Every set passes AA. Is it any good? Go with your gut.</p>
</div>

{#if front}
	<div class="table">
		<!-- The sets coming next, back to front. Only their grounds show. -->
		{#each [...pile.slice(1)].reverse() as card (card.id)}
			<div
				class="card behind"
				style="background: {card.trio.ground.hex}; --tilt: {card.tilt}deg"
				aria-hidden="true"
			></div>
		{/each}

		<section
			class="card"
			style="background: {front.trio.ground.hex}; color: {front.trio.text.hex}; --tilt: {front.tilt / 3}deg"
			aria-label="Color set to vote on"
		>
			<p class="poster">
				To really appreciate design you
				<em style="color: {front.trio.accent.hex}">{front.ending}</em>
			</p>
			<p class="body">
				Body text in the same ink, at the size people actually read. A
				<span class="link" style="color: {front.trio.accent.hex}">link in the accent</span>
				sits in the middle of it.
			</p>
		</section>

		{#if ghost}
			{#key ghost.id}
				<div
					class="card ghost"
					class:yes={ghost.liked}
					style="background: {ghost.trio.ground.hex}; color: {ghost.trio.text.hex}; --tilt: {ghost.tilt /
						3}deg"
					aria-hidden="true"
				>
					<p class="poster">
						To really appreciate design you
						<em style="color: {ghost.trio.accent.hex}">{ghost.ending}</em>
					</p>
					<p class="body">
						Body text in the same ink, at the size people actually read. A
						<span class="link" style="color: {ghost.trio.accent.hex}">link in the accent</span>
						sits in the middle of it.
					</p>
					<!-- The stamp is the set's own accent on its own ground, which
					     every set already clears at 4.5:1 or more. -->
					<span
						class="stamp"
						style="color: {ghost.trio.accent.hex}; background: {ghost.trio.ground.hex}"
						>{ghost.liked ? 'Yes' : 'No'}</span
					>
				</div>
			{/key}
		{/if}
	</div>

	<div class="actions">
		<button type="button" class="btn no" onclick={() => vote(false)}>No <kbd>N</kbd></button>
		<button type="button" class="btn yes" onclick={() => vote(true)}>Yes <kbd>Y</kbd></button>
		<button type="button" class="skip-btn" onclick={advance}>Skip <kbd>S</kbd></button>
	</div>
{:else}
	<p class="muted">Mixing a set…</p>
	<noscript><p>The voter needs JavaScript.</p></noscript>
{/if}

<!-- One line after each vote: the answer, and the numbers the set was hiding. -->
<div class="after" aria-live="polite">
	{#if error}<p class="error">{error}</p>{/if}
	{#if last}
		{@const t = last.trio}
		{@const rt = contrast(t.text, t.ground)}
		{@const ra = contrast(t.accent, t.ground)}
		<p>
			You said {last.liked ? 'yes' : 'no'}. Text
			<span class="mono">{rt.toFixed(2)}:1</span>
			<span class="badge" data-grade={grade(rt)}>{grade(rt)}</span>, accent
			<span class="mono">{ra.toFixed(2)}:1</span>
			<span class="badge" data-grade={grade(ra)}>{grade(ra)}</span>.
			{count}
			{count === 1 ? 'vote' : 'votes'} so far. <a href="/results">See the results.</a>
		</p>
	{/if}
</div>

<style>
	.intro {
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		gap: 0 1.5rem;
		margin-bottom: 1.5rem;
	}

	.intro h1 {
		font-size: var(--text-xl);
		line-height: var(--leading-xl);
		margin: 0;
	}

	.intro p {
		margin: 0;
	}

	/* Every card sits in the same grid cell, so the pile stacks without
	   absolute positioning and takes the front card's height. */
	.table {
		display: grid;
		padding: 0.75rem 0;
	}

	.card {
		grid-area: 1 / 1;
		border: 2px solid var(--color-border);
		padding: 1.5rem;
		min-height: max(20rem, 60svh);
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		gap: 1.5rem;
		transform: rotate(var(--tilt));
		position: relative;
	}

	@media (min-width: 40rem) {
		.card {
			padding: 3rem;
		}
	}

	/* Basteleur (Velvetyne, OFL), the face oblique set its cards in. Fluid
	   between rem endpoints, per RULES.md "Fluid type is an allowed trade".
	   The type never changes from card to card: the vote is about color. */
	.poster {
		font-family: 'Basteleur', var(--font-display);
		font-weight: bold;
		font-size: clamp(2.25rem, 0.75rem + 6vw, 6rem);
		line-height: 1.1;
		margin: 0;
		max-width: none;
		text-wrap: balance;
		overflow-wrap: break-word;
	}

	.poster em {
		display: block;
		font-style: normal;
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

	.ghost {
		pointer-events: none;
		animation: leave-left 900ms ease-in forwards;
	}

	.ghost.yes {
		animation-name: leave-right;
	}

	/* The accent tilt, 8deg, for the one loud thing (RULES.md). */
	.stamp {
		position: absolute;
		top: 1.5rem;
		left: 1.5rem;
		font-family: 'Basteleur', var(--font-display);
		font-weight: bold;
		font-size: clamp(2.25rem, 1rem + 5vw, 5rem);
		line-height: 1;
		text-transform: uppercase;
		padding: 0.15em 0.3em 0.05em;
		border: 0.08em solid currentColor;
		transform: rotate(-8deg);
		animation: stamp 150ms ease-out;
	}

	.ghost.yes .stamp {
		left: auto;
		right: 1.5rem;
		transform: rotate(8deg);
	}

	@keyframes stamp {
		from {
			opacity: 0;
			scale: 1.6;
		}
	}

	@keyframes leave-right {
		0%,
		45% {
			transform: rotate(var(--tilt));
		}
		100% {
			transform: translateX(110vw) rotate(10deg);
		}
	}

	@keyframes leave-left {
		0%,
		45% {
			transform: rotate(var(--tilt));
		}
		100% {
			transform: translateX(-110vw) rotate(-10deg);
		}
	}

	/* Reduced motion: the stamp still shows, then the card simply goes. */
	@media (prefers-reduced-motion: reduce) {
		.ghost,
		.stamp {
			animation: none;
		}
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

	.actions .yes {
		background: var(--color-text);
		color: var(--color-bg);
	}

	@media (hover: hover) {
		.actions .yes:hover {
			background: var(--color-accent) !important;
			border-color: var(--color-accent);
		}
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

	.after {
		margin-top: 1.125rem;
	}

	.after p {
		margin: 0 0 0.75rem;
	}

	.error {
		font-weight: bold;
	}
</style>
