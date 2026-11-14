# laraborowsky-site

Source for laraborowsky.com. Plain HTML, no build step. Vercel publishes every push to `main`.

## Layout
- `index.html`: home page
- `lavalou/`: the Lavalou section (lavalou.fun redirects here)
  - `cluck-quest/`: Cluck Quest 1 (math) and its guides
  - `cluck-quest-2/`: Cluck Quest 2 (spelling) and its guides
- `vercel.json`: clean URLs and the lavalou.fun redirect

## Updating a game
Replace `lavalou/cluck-quest/index.html` (or `cluck-quest-2/index.html`) with the new single-file build, then commit and push.
Saved progress is stored per web address, so it carries over as long as the URL stays the same.

## Hosting
- Domains: Cloudflare (DNS only, no proxy)
- Hosting: Vercel, connected to this GitHub repo
