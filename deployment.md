# NewsFlow AI — Deployment Guide

This project has two parts that can be deployed independently:
1. **Backend pipeline** — Python script that fetches RSS, processes articles with OpenAI, and saves an archive.
2. **Website** — React Vite app that serves as a frontend for the archive.

---

## 1. Backend Pipeline Deployment

### Option A: One‑off / Cron Job

```bash
# Set the environment variable before running
export OPENAI_API_KEY=sk-proj-...   # or set in your CI/env system

# Run manually
python backend/main.py
```

**For cron / scheduled runs** (e.g., daily at 6am):

```bash
# Add to crontab (run as user with OPENAI_API_KEY available)
0 6 * * * cd /path/to/newsflow-ai && python backend/main.py >> logs/newsflow-$(date +\%Y\%m\%d).log 2>&1
```

**CI / GitHub Actions** — see the example workflow below.

### Option B: Production Checklist

- [ ] **`OPENAI_API_KEY`** is set as a secret in your hosting environment (never hard‑code it).
- [ ] **`requirements.txt`** packages are installed in the production Python environment.
- [ ] **`data/`** directory is writable by the process (the pipeline creates `news_archive.json` there).
- [ ] **RSS feed accessibility** — ensure outbound HTTP/HTTPS is allowed (feeds from BBC/DW).
- [ ] **OpenAI quota** — the pipeline sends up to 15 articles per run. Verify your plan can handle that volume.
- [ ] **Archive rotation** — `data/news_archive.json` grows daily. Consider adding retention logic or external storage if long‑term storage is needed.

### Option C: Docker (optional, not currently configured)

No `Dockerfile` exists yet. If you containerize, mount `.env` at runtime and expose no ports (the pipeline is CLI‑only). The website can also be served from the same container via Vite’s preview build.

---

## 2. Website Deployment

### Static Hosting (recommended)

The Vite build produces static assets in `website/dist/`.

```bash
# From repository root
cd website
npm install          # Install deps
npm run build         # Creates website/dist/
```

**Deploy `website/dist/`** to any static host (Netlify, Vercel, Cloudflare Pages, GitHub Pages, etc.).

**Build environment variables**: No special env vars are required for the static build. The React app only renders UI; it does not call OpenAI directly. If your host requires a `_redirects` file for SPA routing, add `public/_redirects` with content `/   /   200`.

**Alternative: Serve from Same Python Process**

You can also serve the built website from the same host as the Python pipeline, e.g.:

```bash
# In one terminal
python backend/main.py

# In another terminal, from website/
npx serve -s dist        # or use any static file server
```

### SPA Routing Consideration

If you deploy to a host that serves a single `index.html` for all routes (e.g., Netlify redirect rules), you may need a basic `404.html` fallback or a rewrite rule that points to `index.html`. The current React app uses client‑side routing (HashRouter or BrowserRouter), so ensure your host supports SPA conventions.

### Alternative: Sync Archive for Static Deployment

After building the website, copy the latest archive so the frontend can display it:

```bash
# From repository root
python backend/sync_archive.py
```

This copies `data/news_archive.json` into `website/public/data/news_archive.json`, which the React app reads from `/data/news_archive.json` at runtime.

Then deploy `website/dist/` (the Vite build output) to your chosen static host.

---

## 3. Full‑Stack Deployment Example (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install Python deps
        run: |
          python -m venv .venv
          source .venv/bin/activate
          pip install -r requirements.txt

      - name: Run pipeline
        # OPENAI_API_KEY must be available as a secret
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          source .venv/bin/activate
          python backend/main.py

      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install Node deps
        run: cd website && npm ci

      - name: Build website
        run: cd website && npm run build

      - name: Deploy website
        # Example using Netlify action
        uses: netlify/actions/cli@v1
        with:
          args: publish website/dist/ --distribute-on-cdntier
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

**Secrets needed** in your CI system:
- `OPENAI_API_KEY` — for the Python pipeline
- `NETLIFY_AUTH_TOKEN` / `NETLIFY_SITE_ID` — if deploying the website via Netlify

---

## 4. Post‑Deployment Verification

After the first run:

1. **Check the archive**: `data/news_archive.json` should exist and contain today's date key.
2. **Inspect statistics**: Open the JSON and verify `statistics.{articles_collected, duplicates_removed, total_articles}` are reasonable.
3. **Website**: Visit the deployed URL and confirm the archive data is visible (once UI components are implemented).
4. **Logs**: Review any console output for warnings (e.g., RSS feed bozo warnings, OpenAI errors).

---

## 5. What NOT to Deploy

- **`.env`** — already gitignored, contains real API key.
- **`__pycache__/`** — Python bytecode cache, not needed at runtime.
- **`website/node_modules/`** — committed to repo? No, it's gitignored. Install via `npm ci` or `npm install` in the target environment.
- **`data/news_archive.json`** — this is generated output; you may want to exclude it from backups or rotate it depending on your policy.