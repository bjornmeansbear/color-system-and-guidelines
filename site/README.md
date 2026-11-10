# Wjavelength

The website for the Wjerk color system: the palette, the step contrast cheat
sheet, the rules, a `kit.css` download, and a voter where people say yes or no
to random sets of ground, text and accent that all pass AA.

It reads `../kit.css` and `../RULES.md` at build time, so it can't drift from
the kit. The kit itself stays a plain file with no build step; only this
folder has one.

Live at https://wjavelength.wjerk.shop/. SvelteKit on Cloudflare Workers
(OOKB account), with votes in a D1 database.

## Run it locally

```sh
npm install
npm run db:migrate:local   # makes the local vote table, once
npm run build
npx wrangler dev           # http://localhost:8787, with a local vote database
```

`npm run dev` also works for editing pages; voting needs the database, so
test the vote and results pages under `wrangler dev`.

## Deploy

```sh
npm run build && npx wrangler deploy
```

The database and the `wjavelength.wjerk.shop` domain are already set up in
`wrangler.jsonc`. A new migration in `migrations/` goes live with
`npx wrangler d1 migrations apply wjavelength --remote` before deploying.

Redeploy after changing `kit.css` or `RULES.md`, too: the site reads them at
build time.

## How it fits together

- `src/lib/palette.ts` parses `kit.css`, does the WCAG math, and makes the
  random sets. The vote endpoint re-checks every set with the same rules, so
  only sets the voter could have shown are counted.
- `src/routes/rules` renders `RULES.md`, with local file paths stripped.
  `NOTES.md` is never published.
- `migrations/` holds the vote table. Each browser keeps a random id so a
  person's vote on a set counts once; it identifies nobody.
- Results rank sets by the Wilson lower bound, so a set with one yes doesn't
  outrank one with forty.
