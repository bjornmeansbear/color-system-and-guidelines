<script lang="ts">
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();
</script>

<svelte:head>
	<title>Rules — Wjavelength</title>
</svelte:head>

<h1>Rules</h1>
<p class="lede">
	The reasoning behind the kit: why pink, why rules instead of shadows, why steps instead of colors.
	A working document, kept as decisions get made.
</p>

<div class="layout">
	<nav aria-label="Sections" class="toc">
		<h2>Sections</h2>
		<ol>
			{#each data.toc as item}
				<li><a href="#{item.id}">{item.text}</a></li>
			{/each}
		</ol>
	</nav>

	<article class="prose">
		{@html data.html}
	</article>
</div>

<style>
	.layout {
		display: grid;
		grid-template-columns: minmax(0, 1fr);
		gap: 2.25rem;
		margin-top: 2.25rem;
	}

	@media (min-width: 55rem) {
		.layout {
			grid-template-columns: 16rem minmax(0, 1fr);
			align-items: start;
		}

		.toc {
			position: sticky;
			top: 1.5rem;
			max-height: calc(100vh - 3rem);
			overflow-y: auto;
		}
	}

	.toc {
		border-top: 2px solid var(--color-border);
		padding-top: 0.75rem;
	}

	.toc h2 {
		font-size: var(--text-sm);
		line-height: var(--leading-sm);
		text-transform: uppercase;
		letter-spacing: 0.08em;
		margin-bottom: 0.5rem;
	}

	.toc ol {
		list-style: none;
		margin: 0;
		padding: 0;
		font-size: var(--text-sm);
		line-height: var(--leading-sm);
	}

	.toc li {
		padding: 0.25rem 0;
	}

	.toc a {
		text-decoration-color: transparent;
	}

	.toc a:hover,
	.toc a:focus-visible {
		text-decoration-color: var(--color-accent);
	}

	/* Markdown content: sizes from the kit's type scale. */
	.prose {
		max-width: 42rem;
	}

	.prose :global(h2) {
		font-size: var(--text-xl);
		line-height: var(--leading-xl);
		border-top: 2px solid var(--color-border);
		padding-top: 1.125rem;
		margin-top: 3rem;
		scroll-margin-top: 1.5rem;
	}

	.prose :global(h2:first-child) {
		margin-top: 0;
	}

	.prose :global(h3) {
		font-size: var(--text-lg);
		line-height: var(--leading-lg);
		margin-top: 2.25rem;
	}

	.prose :global(h4) {
		font-size: var(--text-md);
		line-height: var(--leading-md);
	}

	.prose :global(ul),
	.prose :global(ol) {
		margin: 0 0 1.5rem;
		padding-left: 1.5rem;
	}

	.prose :global(li) {
		margin-bottom: 0.375rem;
	}

	.prose :global(pre) {
		overflow-x: auto;
		border: 1px solid var(--color-border);
		padding: 0.75rem 1rem;
		margin: 0 0 1.5rem;
		font-size: var(--text-sm);
		line-height: var(--leading-sm);
	}

	.prose :global(table) {
		display: block;
		overflow-x: auto;
		border-collapse: collapse;
		margin: 0 0 1.5rem;
		font-size: var(--text-sm);
		line-height: var(--leading-sm);
	}

	.prose :global(th),
	.prose :global(td) {
		border-bottom: 1px solid var(--color-border);
		padding: 0.375rem 0.75rem 0.375rem 0;
		text-align: left;
		vertical-align: top;
	}

	.prose :global(blockquote) {
		margin: 0 0 1.5rem;
		padding-left: 1rem;
		border-left: 2px solid var(--color-accent);
	}
</style>
