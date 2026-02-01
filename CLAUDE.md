# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Static website for Privanon LLC (www.privanon.com), a defense communications company. Vanilla HTML/CSS/JS with Python-based article generation and automated publishing via GitHub Actions.

## Commands

```bash
# Set up Python environment (first time)
cd scripts
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Generate article locally (uses claude-sonnet-4-20250514)
cd scripts && source venv/bin/activate
python generate_article.py   # Creates insight-*.html, writes scripts/latest_article.json
python update_insights.py    # Prepends card to insights.html, deletes JSON

# Deploy via Hostinger MCP
tar -czvf site.tar.gz -C . .  # Archive with files at root level
# Then: mcp__hostinger-mcp__hosting_deployStaticWebsite(domain="privanon.com", archivePath="site.tar.gz")
```

## Architecture

**Static Site** — No build step. Edit HTML/CSS/JS directly, preview in browser.
- `styles.css` — CSS custom properties in `:root` for theming, CSS Grid layouts
- `script.js` — Mobile menu, navbar scroll effect, Intersection Observer fade-in animations, simulated contact form

**Article Generation Pipeline:**
1. `generate_article.py` — Selects random topic from hardcoded `TOPICS` list, calls Claude API, creates `insight-{slug}.html` (slug truncated at 50 chars), saves metadata to `scripts/latest_article.json`
2. `update_insights.py` — Reads JSON, prepends article card to `insights.html` grid via regex, deletes JSON

**Credentials** — Store in `scripts/.env` (gitignored), loaded via `python-dotenv`:
- `ANTHROPIC_API_KEY` — Required for article generation
- `X_API_KEY`, `X_API_SECRET`, `X_ACCESS_TOKEN`, `X_ACCESS_TOKEN_SECRET` — For X/Twitter posting

## GitHub Actions

`auto-post.yml` runs twice daily (9 AM & 3 PM HST):
1. Generate article via Claude API
2. Update insights.html
3. Post to X with article link
4. Commit and push
5. FTP deploy to Hostinger

Required secrets: `ANTHROPIC_API_KEY`, `X_API_KEY`, `X_API_SECRET`, `X_ACCESS_TOKEN`, `X_ACCESS_TOKEN_SECRET`, `FTP_HOST`, `FTP_USERNAME`, `FTP_PASSWORD`

## Constraints

- 2-space indentation in HTML/CSS/JS
- Test responsive breakpoints: 480px, 768px, 1024px
- Contact form is simulated (no backend)—submission shows success message but doesn't send
