import kit from '../../../../kit.css?raw';

// The kit itself, served as a file to download. Prerendered, so it's the
// kit.css that was in the repo when the site was built.
export const prerender = true;

export const GET = () =>
	new Response(kit, { headers: { 'content-type': 'text/css; charset=utf-8' } });
