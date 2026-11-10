import { Marked, type Tokens } from 'marked';
import rules from '../../../../RULES.md?raw';
import type { PageServerLoad } from './$types';

// Built once, at build time, from the repo's RULES.md.
export const prerender = true;

const slug = (text: string) =>
	text
		.toLowerCase()
		.replace(/<[^>]+>/g, '')
		.replace(/&[a-z#0-9]+;/g, '')
		.replace(/[^a-z0-9]+/g, '-')
		.replace(/^-|-$/g, '');

// RULES.md is a working document. Local file paths on the author's machine
// mean nothing on the web, so "~/Code/chair-ness" becomes "chair-ness".
const publicText = rules.replace(/~\/Code\//g, '');

export const load: PageServerLoad = () => {
	const toc: { id: string; text: string }[] = [];

	const marked = new Marked({
		renderer: {
			heading(this: { parser: { parseInline: (t: Tokens.Generic[]) => string } }, { tokens, depth, text }: Tokens.Heading) {
				const id = slug(text);
				if (depth === 2) toc.push({ id, text });
				// The page's own h1 is "Rules", so the document's levels shift down one.
				const level = Math.min(depth + 1, 6);
				return `<h${level} id="${id}">${this.parser.parseInline(tokens)}</h${level}>\n`;
			}
		}
	});

	// Drop the document's own top-level title; the page supplies one.
	const body = publicText.replace(/^# .*\n/, '');
	const html = marked.parse(body, { async: false }) as string;

	return { html, toc };
};
