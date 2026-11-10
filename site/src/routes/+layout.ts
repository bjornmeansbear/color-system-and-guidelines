// Most pages are built once, ahead of time. /results and /api/vote opt out:
// they read the vote database on every request.
export const prerender = true;
