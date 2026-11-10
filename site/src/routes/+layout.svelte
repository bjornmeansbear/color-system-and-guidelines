<script lang="ts">
	import '../../../kit.css';
	import '#lib/site.css';
	import { page } from '$app/state';
	import type { LayoutProps } from './$types';

	let { children }: LayoutProps = $props();

	const nav = [
		{ href: '/palette', label: 'Palette' },
		{ href: '/contrast', label: 'Contrast' },
		{ href: '/vote', label: 'Vote' },
		{ href: '/results', label: 'Results' },
		{ href: '/rules', label: 'Rules' }
	];
</script>

<a class="skip" href="#main">Skip to content</a>

<header>
	<div class="wrap bar">
		<a class="wordmark" href="/" aria-current={page.url.pathname === '/' ? 'page' : undefined}
			>Wjavelength</a
		>
		<nav aria-label="Site">
			<ul>
				{#each nav as item}
					<li>
						<a
							href={item.href}
							aria-current={page.url.pathname.startsWith(item.href) ? 'page' : undefined}
							>{item.label}</a
						>
					</li>
				{/each}
				<li><a href="/kit.css" download>kit.css</a></li>
			</ul>
		</nav>
	</div>
</header>

<main id="main" class="wrap">
	{@render children()}
</main>

<footer>
	<div class="wrap">
		<p>
			Wjavelength is the Wjerk color system: the palette, the reasoning behind it, and a place to
			vote on what it makes. Public domain. A <a href="https://a.wjerk.shop/">Wjerk</a> project.
		</p>
	</div>
</footer>

<style>
	header {
		border-bottom: 2px solid var(--color-border);
	}

	.bar {
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		justify-content: space-between;
		gap: 0.75rem 1.5rem;
		padding-top: 1.125rem;
		padding-bottom: 1.125rem;
	}

	.wordmark {
		font-weight: bold;
		font-size: var(--text-lg);
		line-height: var(--leading-lg);
		text-decoration: none;
		letter-spacing: -0.01em;
	}

	ul {
		display: flex;
		flex-wrap: wrap;
		gap: 0.25rem 1.25rem;
		list-style: none;
		margin: 0;
		padding: 0;
	}

	nav a {
		text-decoration-color: transparent;
	}

	nav a[aria-current='page'] {
		text-decoration-color: var(--color-accent);
		font-weight: bold;
	}

	footer {
		border-top: 2px solid var(--color-border);
		padding: 1.5rem 0 3rem;
	}

	footer p {
		font-size: var(--text-sm);
		line-height: var(--leading-sm);
		color: var(--color-text-muted);
		max-width: 40rem;
		margin: 0;
	}
</style>
