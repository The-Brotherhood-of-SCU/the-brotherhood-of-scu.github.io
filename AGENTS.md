# AGENTS.md

Official homepage of The Brotherhood of SCU（四川大学开源社区）— an Astro 7 + Tailwind CSS v4 static site, Chinese-language (`lang="zh-CN"`), deployed to GitHub Pages at https://scubro.dev. `README.md` covers contributor workflows (writing posts, syncing members) in Chinese.

## Commands

```bash
npm run dev            # dev server at http://localhost:4321
npm run build          # build to dist/ — also validates blog frontmatter against the zod schema
npm run preview        # serve the built dist/
npm run sync-members   # regenerate src/data/members.json (requires local gh CLI logged in with read:org)
```

No lint or test scripts are configured. There is no tailwind.config — Tailwind v4 runs via `@tailwindcss/vite` with all theme tokens in CSS. Verify changes with `npm run build`.

## Architecture

- `src/data/site.ts` — single source of truth for homepage copy: `SITE` (name, url, contacts), `CONCEPTS`, projects, etc. Edit copy here, not in pages.
- `src/data/members.json` — **generated** by `scripts/sync-members.mjs` from the GitHub org GraphQL API. Never hand-edit; re-run the script instead.
- `src/content/blog/*.md` — posts; filename is the URL slug. Schema (zod) lives in `src/content.config.ts`: `title` required, `date` coerced, `author`/`tags` optional. Post images go in `public/images/posts/<slug>/` and are referenced with absolute paths like `/images/posts/<slug>/x.avif`.
- `src/pages/` — routes: `/`, `/blog`, `/blog/[slug]`, `/projects`, `/members`, `/about`, `/404`, `/rss.xml`.
- `src/layouts/Base.astro` — owns the `<head>`: title format `X · The Brotherhood of SCU`, canonical/OG built from `Astro.site`, RSS link. New pages should use this layout.
- `src/components/` — Header, Footer, ProjectCard, PostRow, SectionHeader.

## Design system

"Aurora glass"（极光玻璃拟态），defined in `src/styles/global.css` via Tailwind v4 `@theme` — MiniMax-style neutral `paper`/`ink` neutrals + `crimson` #b5121b brand + high-saturation aurora accents (`aurora-red` #f52c6b / `aurora-gold` #ff7045 / `aurora-blue` #16a9f3 / `aurora-violet` #6f2cf5), Noto Serif SC headings, sans body. Reuse these tokens and the existing component classes (`.wrap`, `.kicker`, `.glass-card`, `.glass-lite`, `.glass-chip`, `.btn-primary`, `.btn-ghost`, `.text-gradient`, `.g-line`, `.u-link`, `.prose-book` for long-form blog typography) instead of introducing ad-hoc colors or fonts.

Dark mode（夜间模式）is class-based: `html.dark` toggled by the Header button, persisted in `localStorage` (`theme`), initialized before first paint by an inline script in `Base.astro` (falls back to `prefers-color-scheme`). `global.css` redefines the semantic `--color-*` tokens under `.dark` (plus dark body/glass/prose/aurora overrides), so token-based utilities adapt automatically — add new colors through tokens or `dark:` variants (enabled via `@custom-variant dark`), never hardcoded light values.

Motion lives in two places: the fixed `.aurora-scene` background layer in `Base.astro` (CSS keyframe drift), and the scroll-reveal system — add `data-reveal` (optionally `style="--reveal-delay: Nms"` for stagger) to any element; the IntersectionObserver script in `Base.astro` toggles `.is-revealed`. Stats use `data-count-to` for count-up. All motion is disabled under `prefers-reduced-motion`, and initial hidden state is gated on an `html.js` class so no-JS visitors see everything. `html` has `overflow-x: clip` — don't remove it.

## Gotchas

- `astro.config.mjs` `site` must stay in sync with `public/CNAME` (`scubro.dev`); canonical URLs, OG tags, sitemap, and RSS all derive from it. Don't delete `public/CNAME`.
- Every push to `main` auto-deploys via GitHub Actions (`.github/workflows/deploy.yml`, `withastro/action@v3`) — there is no staging environment.
- Pushes made with the built-in `GITHUB_TOKEN` do **not** trigger other workflows (GitHub's recursion guard), so `sync-members.yml` commits with `GITHUB_TOKEN` and then explicitly runs `gh workflow run deploy.yml` (needs `permissions.actions: write`). Don't switch that push back to a PAT or drop the dispatch — the member sync would silently stop deploying.
- Code blocks use Shiki dual themes `github-light`/`github-dark` (`defaultColor: 'light'`); the dark palette is applied by the `.dark` rule on `.astro-code` in `global.css`.
