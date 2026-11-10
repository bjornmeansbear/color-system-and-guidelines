<script lang="ts">
	import { BY_NAME, HUE_SCALES, NEUTRAL_SCALES, ORIGINALS, contrast, scale, type Color } from '#lib/palette.ts';

	const groups = [
		{ title: 'Hues', note: 'In spectrum order. Every one on the same lightness grid.', families: HUE_SCALES },
		{
			title: 'Neutrals',
			note: 'Warm and cool grays, and the browns that carry the line work. White and black are papers and inks: a material, not a ramp, so their steps sit close together.',
			families: NEUTRAL_SCALES
		}
	];

	// Which of the kit's ground and ink reads as text on this swatch.
	const white = BY_NAME.get('white-0')!;
	const black = BY_NAME.get('black-9')!;
	const labelInk = (c: Color) => (contrast(black, c) >= contrast(white, c) ? black : white);

	let copied = $state('');
	let timer: ReturnType<typeof setTimeout>;

	async function copy(c: Color) {
		const value = `var(--${c.name})`;
		try {
			await navigator.clipboard.writeText(value);
			copied = `Copied ${value}`;
		} catch {
			copied = `${value} (copy blocked by the browser)`;
		}
		clearTimeout(timer);
		timer = setTimeout(() => (copied = ''), 2500);
	}
</script>

<svelte:head>
	<title>Palette — Wjavelength</title>
</svelte:head>

<h1>Palette</h1>
<p class="lede">
	Every color in <code>kit.css</code>, read from the file itself. Press a swatch to copy its token.
	The label on each swatch is set in whichever of the kit's ink or paper reads better on it.
</p>
<p class="visually-hidden" aria-live="polite">{copied}</p>

{#each groups as group}
	<section class="section">
		<h2>{group.title}</h2>
		<p class="muted">{group.note}</p>
		{#each group.families as f}
			<div class="scale">
				<h3 class="mono">{f}</h3>
				<ol>
					{#each scale(f) as c}
						{@const ink = labelInk(c)}
						<li>
							<button
								type="button"
								class="swatch"
								style="background: {c.hex}; color: {ink.hex}"
								aria-label="{c.name}, {c.hex}. Copy token."
								onclick={() => copy(c)}
							>
								<span class="step">{c.step}</span>
								<span class="hex">{c.hex}</span>
							</button>
						</li>
					{/each}
				</ol>
			</div>
		{/each}
	</section>
{/each}

<section class="section">
	<h2>The originals</h2>
	<p class="muted">
		The Wjerk palette the scales were built from, at exact values. Use the original when the color is
		the identity; use a scale step for tints and guaranteed contrast.
	</p>
	<ol class="originals">
		{#each ORIGINALS as c}
			{@const ink = labelInk(c)}
			<li>
				<button
					type="button"
					class="swatch"
					style="background: {c.hex}; color: {ink.hex}"
					aria-label="{c.name}, {c.hex}. Copy token."
					onclick={() => copy(c)}
				>
					<span class="step">{c.name.replace('wjerk-', '')}</span>
					<span class="hex">{c.hex}</span>
				</button>
			</li>
		{/each}
	</ol>
</section>

<p class="toast" aria-hidden="true" class:on={copied}>{copied}</p>

<style>
	.scale {
		margin-top: 1.5rem;
	}

	h3 {
		margin: 0 0 0.375rem;
		font-weight: bold;
	}

	ol {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		grid-template-columns: repeat(5, 1fr);
		border: 1px solid var(--color-border);
	}

	@media (min-width: 40rem) {
		ol {
			grid-template-columns: repeat(10, 1fr);
		}
	}

	.originals {
		margin-top: 1.5rem;
		grid-template-columns: repeat(2, 1fr);
	}

	@media (min-width: 40rem) {
		.originals {
			grid-template-columns: repeat(4, 1fr);
		}
	}

	.swatch {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		width: 100%;
		min-height: 4.5rem;
		padding: 0.375rem 0.5rem;
		border: 0;
		font: inherit;
		text-align: left;
		cursor: copy;
	}

	.swatch:focus-visible {
		outline-offset: -0.25rem;
		outline-color: currentColor;
	}

	.step {
		font-weight: bold;
		font-size: var(--text-sm);
		line-height: var(--leading-sm);
	}

	.hex {
		font-family: var(--font-mono);
		font-size: var(--text-2xs);
		line-height: var(--leading-2xs);
	}

	.toast {
		position: fixed;
		left: 50%;
		bottom: 1.5rem;
		transform: translateX(-50%);
		margin: 0;
		padding: 0.5rem 1rem;
		background: var(--color-text);
		color: var(--color-bg);
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		line-height: var(--leading-sm);
		visibility: hidden;
	}

	.toast.on {
		visibility: visible;
	}
</style>
