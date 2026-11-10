<script lang="ts">
	import {
		BY_NAME,
		COLORS,
		HUE_SCALES,
		NEUTRAL_SCALES,
		contrast,
		grade,
		scale,
		stepMatrix
	} from '#lib/palette.ts';

	const matrix = stepMatrix();
	const steps = Array.from({ length: 10 }, (_, i) => i);

	const optionGroups = [
		...[...HUE_SCALES, ...NEUTRAL_SCALES].map((f) => ({ label: f, colors: scale(f) })),
		{ label: 'originals', colors: COLORS.filter((c) => c.family === 'wjerk') }
	];

	let textName = $state('pink-2');
	let groundName = $state('cornflower-7');

	const text = $derived(BY_NAME.get(textName)!);
	const ground = $derived(BY_NAME.get(groundName)!);
	const ratio = $derived(contrast(text, ground));

	// The dark twin: the same two hues with their step numbers traded.
	// The kit's dark mode is this move on the brown scale (0 and 9 swap).
	const twin = $derived.by(() => {
		if (text.step === null || ground.step === null) return null;
		const t = BY_NAME.get(`${text.family}-${ground.step}`);
		const g = BY_NAME.get(`${ground.family}-${text.step}`);
		return t && g ? { text: t, ground: g, ratio: contrast(t, g) } : null;
	});

	function swap() {
		[textName, groundName] = [groundName, textName];
	}
</script>

<svelte:head>
	<title>Contrast — Wjavelength</title>
</svelte:head>

<h1>Contrast</h1>
<p class="lede">
	Every scale shares one lightness grid, so the step numbers decide the contrast, whatever the hues.
	Pick two steps from the table and you know the worst case before you pick a color.
</p>

<section class="section">
	<h2>The step cheat sheet</h2>
	<p class="muted">
		Each cell is the lowest contrast between those two steps across every hue and neutral scale,
		paired with every other, mixing hues included. The highest is in brackets. Paper and ink (white,
		black) aren't on the grid, so they're left out.
	</p>
	<!-- A scrollable region must be focusable so keyboard users can scroll it. -->
	<!-- svelte-ignore a11y_no_noninteractive_tabindex -->
	<div class="scroll" role="region" aria-label="Step contrast table" tabindex="0">
		<table>
			<caption class="visually-hidden">Worst-case contrast between any two kit steps</caption>
			<thead>
				<tr>
					<th scope="col"><span class="visually-hidden">Step</span></th>
					{#each steps as s}<th scope="col">{s}</th>{/each}
				</tr>
			</thead>
			<tbody>
				{#each steps as i}
					<tr>
						<th scope="row">{i}</th>
						{#each steps as j}
							{@const cell = matrix[i][j]}
							{@const g = i === j ? null : grade(cell.min)}
							<td data-grade={g}>
								{#if g}
									<span class="num">{cell.min.toFixed(1)}</span>
									<span class="max">({cell.max.toFixed(1)})</span>
									<span class="visually-hidden">{g}</span>
								{:else}
									<span aria-label="same step">·</span>
								{/if}
							</td>
						{/each}
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
	<ul class="key">
		<li><span class="swatch" data-grade="AAA"></span> AAA, 7:1 and up: any text</li>
		<li><span class="swatch" data-grade="AA"></span> AA, 4.5:1: body text</li>
		<li><span class="swatch" data-grade="Large"></span> 3:1: large text and graphics only</li>
		<li><span class="swatch" data-grade="Fail"></span> Under 3:1: not for text</li>
	</ul>
</section>

<section class="section">
	<h2>Check a pair</h2>
	<p class="muted">
		Contrast is the same whichever color is the text, so a pair that passes also passes flipped. Its
		dark twin keeps both hues and trades their step numbers.
	</p>

	<div class="picker">
		<label>
			Text
			<select bind:value={textName}>
				{#each optionGroups as group}
					<optgroup label={group.label}>
						{#each group.colors as c}<option value={c.name}>{c.name}</option>{/each}
					</optgroup>
				{/each}
			</select>
		</label>
		<button type="button" class="btn" onclick={swap}>Flip</button>
		<label>
			Ground
			<select bind:value={groundName}>
				{#each optionGroups as group}
					<optgroup label={group.label}>
						{#each group.colors as c}<option value={c.name}>{c.name}</option>{/each}
					</optgroup>
				{/each}
			</select>
		</label>
	</div>

	<div class="pairs">
		<figure>
			<div class="sample" style="background: {ground.hex}; color: {text.hex}">
				<p class="big">Pick steps, not colors.</p>
				<p>Body text at the normal size, the kind that needs 4.5:1 to pass AA.</p>
			</div>
			<figcaption>
				<span class="mono">{text.name} on {ground.name}</span>
				<strong>{ratio.toFixed(2)}:1</strong>
				<span class="badge" data-grade={grade(ratio)}>{grade(ratio)}</span>
			</figcaption>
		</figure>

		{#if twin}
			<figure>
				<div class="sample" style="background: {twin.ground.hex}; color: {twin.text.hex}">
					<p class="big">Pick steps, not colors.</p>
					<p>Body text at the normal size, the kind that needs 4.5:1 to pass AA.</p>
				</div>
				<figcaption>
					<span class="mono">Twin: {twin.text.name} on {twin.ground.name}</span>
					<strong>{twin.ratio.toFixed(2)}:1</strong>
					<span class="badge" data-grade={grade(twin.ratio)}>{grade(twin.ratio)}</span>
				</figcaption>
			</figure>
		{:else}
			<p class="muted">Originals have no step number, so they have no twin.</p>
		{/if}
	</div>
	<p class="muted note">
		The numbers are symmetric; the eye isn't. Light text on a dark ground reads heavier and can
		bloom, so a dark twin may want a lighter weight or a little more letter-spacing.
	</p>
</section>

<style>
	.scroll {
		overflow-x: auto;
		margin-top: 1.125rem;
	}

	table {
		border-collapse: collapse;
		min-width: 40rem;
		width: 100%;
		font-variant-numeric: tabular-nums;
	}

	th,
	td {
		border: 1px solid var(--color-border);
		padding: 0.375rem;
		text-align: center;
		font-size: var(--text-sm);
		line-height: var(--leading-sm);
	}

	th {
		font-weight: bold;
	}

	/* The grade is carried by fill and by a hidden text label, not by color
	   alone: ink fill for AAA, a heavy inset rule for AA, plain for the rest. */
	td[data-grade='AAA'] {
		background: var(--color-text);
		color: var(--color-bg);
	}

	td[data-grade='AA'] {
		box-shadow: inset 0 0 0 3px var(--color-text);
		font-weight: bold;
	}

	td[data-grade='Fail'] {
		color: var(--color-text-muted);
	}

	.max {
		display: block;
		font-size: var(--text-2xs);
		line-height: var(--leading-2xs);
	}

	.key {
		list-style: none;
		padding: 0;
		margin: 1.125rem 0 0;
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem 1.5rem;
		font-size: var(--text-sm);
		line-height: var(--leading-sm);
	}

	.key li {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.key .swatch {
		width: 1.5rem;
		height: 1.125rem;
		border: 1px solid var(--color-border);
	}

	.key .swatch[data-grade='AAA'] {
		background: var(--color-text);
	}

	.key .swatch[data-grade='AA'] {
		box-shadow: inset 0 0 0 3px var(--color-text);
	}

	.picker {
		display: flex;
		flex-wrap: wrap;
		align-items: end;
		gap: 0.75rem 1rem;
		margin: 1.5rem 0;
	}

	label {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
		font-weight: bold;
		font-size: var(--text-sm);
		line-height: var(--leading-sm);
	}

	select {
		font: inherit;
		font-weight: normal;
		font-size: var(--text-base);
		min-height: 2.75rem;
		padding: 0 0.5rem;
		border: 1px solid var(--color-border);
		background: var(--color-bg);
		color: var(--color-text);
	}

	.pairs {
		display: grid;
		gap: 1.5rem;
	}

	@media (min-width: 55rem) {
		.pairs {
			grid-template-columns: 1fr 1fr;
		}
	}

	figure {
		margin: 0;
	}

	.sample {
		border: 1px solid var(--color-border);
		padding: 1.5rem;
	}

	.sample p {
		margin: 0;
	}

	.sample .big {
		font-weight: bold;
		font-size: var(--text-xl);
		line-height: var(--leading-xl);
		margin-bottom: 0.75rem;
	}

	figcaption {
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		gap: 0.5rem 0.75rem;
		margin-top: 0.5rem;
	}

	.note {
		margin-top: 1.5rem;
		font-size: var(--text-sm);
		line-height: var(--leading-sm);
	}
</style>
