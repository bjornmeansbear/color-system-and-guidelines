<script lang="ts">
	import { BY_NAME } from '#lib/palette.ts';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	const pct = (x: number) => `${Math.round(x * 100)}%`;
	const color = (name: string) => BY_NAME.get(name)!;
</script>

<svelte:head>
	<title>Results — Wjavelength</title>
</svelte:head>

<h1>Results</h1>

{#if !data.connected}
	<p class="lede">The vote database isn't connected here, so there's nothing to show yet.</p>
{:else if data.totals.votes === 0}
	<p class="lede">No votes yet. <a href="/vote">Be the first.</a></p>
{:else}
	<p class="lede">
		{data.totals.votes.toLocaleString()} votes from {data.totals.voters.toLocaleString()}
		{data.totals.voters === 1 ? 'person' : 'people'}. {pct(data.totals.yes / data.totals.votes)} were
		yes. <a href="/vote">Add yours.</a>
	</p>
	<p class="muted">
		With thousands of possible sets, most get only a vote or two. Sets are ranked by how sure the
		votes make us, not by raw share, so one lucky yes doesn't top the list. A set needs 3 votes to
		appear.
	</p>

	{#snippet sets(list: typeof data.best, empty: string)}
		{#if list.length}
			<ol class="sets">
				{#each list as s}
					{@const g = color(s.ground)}
					{@const t = color(s.text)}
					{@const a = color(s.accent)}
					<li>
						<div class="mini" style="background: {g.hex}; color: {t.hex}" aria-hidden="true">
							<span class="aa">Aa</span>
							<em style="color: {a.hex}">accent</em>
						</div>
						<p class="mono">{s.ground} · {s.text} · {s.accent}</p>
						<p>{s.yes} of {s.n} said yes</p>
					</li>
				{/each}
			</ol>
		{:else}
			<p class="muted">{empty}</p>
		{/if}
	{/snippet}

	{#snippet bars(rows: typeof data.groundFamilies, caption: string)}
		<table>
			<caption class="visually-hidden">{caption}</caption>
			<thead>
				<tr><th scope="col">Group</th><th scope="col">Yes</th><th scope="col">Votes</th></tr>
			</thead>
			<tbody>
				{#each rows as r}
					<tr>
						<th scope="row" class="mono">{r.key}</th>
						<td>
							<span class="share">
								<span class="track" aria-hidden="true"><span class="bar" style="width: {pct(r.share)}"></span></span>
								<span class="num">{pct(r.share)}</span>
							</span>
						</td>
						<td class="num">{r.n}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	{/snippet}

	<section class="section">
		<h2>Most liked</h2>
		{@render sets(data.best, 'No set has 3 votes yet.')}
	</section>

	<section class="section">
		<h2>Least liked</h2>
		{@render sets(data.worst, 'Nothing with 3 or more votes is mostly disliked yet.')}
	</section>

	<section class="section">
		<h2>Light or dark grounds</h2>
		{@render bars(data.lightDark, 'Share of yes votes by ground lightness')}
		<p class="muted note">
			"Dark" is measured: a ground the kit's paper white reads on at 4.5:1 or more.
		</p>
	</section>

	<div class="two">
		<section class="section">
			<h2>By ground</h2>
			{@render bars(data.groundFamilies, 'Share of yes votes by ground scale')}
		</section>
		<section class="section">
			<h2>By accent</h2>
			{@render bars(data.accentFamilies, 'Share of yes votes by accent scale')}
		</section>
	</div>
	<p class="muted note">Groups are ordered by how sure the votes make us, highest first.</p>
{/if}

<style>
	.sets {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(13rem, 1fr));
		gap: 1.5rem;
	}

	.sets p {
		margin: 0.375rem 0 0;
		font-size: var(--text-sm);
		line-height: var(--leading-sm);
	}

	.mini {
		border: 1px solid var(--color-border);
		padding: 0.75rem 1rem;
		display: flex;
		align-items: baseline;
		gap: 0.75rem;
		min-height: 6rem;
	}

	.aa {
		font-weight: bold;
		font-size: var(--text-2xl);
		line-height: var(--leading-2xl);
	}

	.mini em {
		font-weight: bold;
	}

	table {
		width: 100%;
		border-collapse: collapse;
		font-variant-numeric: tabular-nums;
	}

	th,
	td {
		text-align: left;
		padding: 0.375rem 0.5rem 0.375rem 0;
		border-bottom: 1px solid var(--color-border);
		font-size: var(--text-sm);
		line-height: var(--leading-sm);
	}

	thead th {
		font-weight: bold;
	}

	tbody th {
		font-weight: normal;
	}

	.share {
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}

	td:nth-child(2) {
		width: 60%;
	}

	.track {
		flex: 1;
		height: 0.75rem;
		border: 1px solid var(--color-border);
	}

	.bar {
		display: block;
		height: 100%;
		background: var(--color-text);
	}

	.num {
		min-width: 3rem;
		text-align: right;
	}

	.two {
		display: grid;
		gap: 0 2rem;
	}

	@media (min-width: 55rem) {
		.two {
			grid-template-columns: 1fr 1fr;
		}
	}

	.note {
		font-size: var(--text-sm);
		line-height: var(--leading-sm);
		margin-top: 0.75rem;
	}
</style>
