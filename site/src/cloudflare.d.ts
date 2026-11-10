// The Cloudflare bindings this site uses, from wrangler.jsonc. Server code
// reads them with: import { env } from 'cloudflare:workers';
declare module 'cloudflare:workers' {
	export const env: {
		DB: import('@cloudflare/workers-types').D1Database;
	};
}
