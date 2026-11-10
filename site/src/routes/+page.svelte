<script lang="ts">
	import { HUE_SCALES, NEUTRAL_SCALES, ORIGINALS, scale } from '#lib/palette.ts';

	// The spectrum: hue scales in hue order, then the neutrals that share the
	// grid. White and black are papers and inks, not steps on it.
	const columns = [...HUE_SCALES, ...NEUTRAL_SCALES.filter((f) => f !== 'white' && f !== 'black')];
	const steps = Array.from({ length: 10 }, (_, i) => i);
	const scaleCount = HUE_SCALES.length + NEUTRAL_SCALES.length;
</script>

<svelte:head>
	<title>Wjavelength — the Wjerk color system</title>
	<meta
		name="description"
		content="The Wjerk color system: {scaleCount} scales on one lightness grid, the rules behind them, and a place to vote on the color sets they make."
	/>
</svelte:head>

<h1>Wjavelength</h1>
<p class="lede">
	The Wjerk color system. {scaleCount} scales of ten steps, every hue on one lightness grid, so contrast
	comes from the step numbers. Pick steps, not colors.
</p>

<figure class="spectrum">
	<div class="grid" style="--cols: {columns.length}" aria-hidden="true">
		{#each steps as s}
			{#each columns as f}
				{@const c = scale(f)[s]}
				<div class="cell" style="background: {c.hex}" title="{c.name} {c.hex}"></div>
			{/each}
		{/each}
	</div>
	<figcaption class="muted">
		Every hue and neutral scale, step 0 (top) to step 9 (bottom). Each row is one step: same
		lightness, different hue. <a href="/palette">See every value.</a>
	</figcaption>
</figure>

<div class="cards">
	<section>
		<h2>Pick steps, not colors</h2>
		<p>
			Steps 0–1 on steps 7–9 pass AAA in any hue, on any hue. Two step numbers tell you the contrast
			before you choose a color.
		</p>
		<p><a href="/contrast">The step cheat sheet</a></p>
	</section>
	<section>
		<h2>Readable isn't the same as good</h2>
		<p>
			Thousands of sets pass AA. Which ones do people want to look at? Vote yes or no on random
			sets of ground, text and accent.
		</p>
		<p><a href="/vote">Start voting</a></p>
	</section>
	<section>
		<h2>Use it</h2>
		<p>
			One file, no build step. Copy <code>kit.css</code> into a project and link it. Dark mode, the
			type scale and the focus ring come with it.
		</p>
		<p><a href="/kit.css" download>Download kit.css</a> · <a href="/rules">Read the rules</a></p>
	</section>
</div>

<section class="section">
	<h2>The originals</h2>
	<p class="lede">
		The scales grew out of these {ORIGINALS.length} colors. They're kept at their exact values, for when
		the color is the identity.
	</p>
	<ul class="originals">
		{#each ORIGINALS as c}
			<li>
				<span class="chip" style="background: {c.hex}" aria-hidden="true"></span>
				<span class="mono">{c.name.replace('wjerk-', '')}</span>
			</li>
		{/each}
	</ul>
</section>

<style>
	h1 {
		font-size: var(--text-3xl);
		line-height: var(--leading-3xl);
		margin-bottom: 0.75rem;
	}

	@media (min-width: 55rem) {
		h1 {
			font-size: 6rem;
			line-height: 6rem;
			letter-spacing: -0.02em;
		}
	}

	.spectrum {
		margin: 2.25rem 0 0;
	}

	.grid {
		display: grid;
		grid-template-columns: repeat(var(--cols), 1fr);
		border: 2px solid var(--color-border);
	}

	.cell {
		aspect-ratio: 2 / 1;
	}

	figcaption {
		font-size: var(--text-sm);
		line-height: var(--leading-sm);
		margin-top: 0.75rem;
	}

	.cards {
		display: grid;
		gap: 0 2rem;
		margin-top: 3rem;
	}

	.cards section {
		border-top: 2px solid var(--color-border);
		padding-top: 1.125rem;
	}

	.cards h2 {
		font-size: var(--text-lg);
		line-height: var(--leading-lg);
		margin-bottom: 0.75rem;
	}

	@media (min-width: 55rem) {
		.cards {
			grid-template-columns: repeat(3, 1fr);
		}
	}

	.originals {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(11rem, 1fr));
		gap: 0.75rem 1.5rem;
	}

	.originals li {
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}

	.chip {
		width: 2.25rem;
		height: 2.25rem;
		border: 1px solid var(--color-border);
		flex: none;
	}
</style>
