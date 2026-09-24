# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Academic personal website for Oliver Philcox (Stanford Physics). Built with Jekyll using the AcademicPages template (fork of Minimal Mistakes theme). Deployed to GitHub Pages at https://oliverphilcox.github.io.

## Development Commands

Note: the system Ruby at `/usr/bin` (2.6) can't satisfy `Gemfile.lock`'s pinned bundler — use the Homebrew Ruby instead: `export PATH="/opt/homebrew/opt/ruby/bin:$PATH"` before running any `bundle`/`jekyll` command.

```bash
# Install dependencies
bundle install

# Local development server (with live reload)
bundle exec jekyll serve

# Local dev with development config overrides (disables analytics, expands CSS)
bundle exec jekyll serve --config _config.yml,_config.dev.yml

# Build static site to _site/
bundle exec jekyll build

# Rebuild minified JS (only needed if editing JS assets)
npm run uglify
```

Note: `_config.yml` is NOT auto-reloaded by `jekyll serve` — restart the server after config changes.

## Architecture

**Static site generator:** Jekyll with Liquid templates, Kramdown markdown, SCSS stylesheets.

**Layout hierarchy:** `_layouts/compress.html` → `default.html` → `single.html` / `talk.html` / `archive.html`

**Key directories:**
- `_config.yml` — site settings, author info, collection definitions, plugin config
- `_pages/` — static pages (about, research, talks, cv, code, etc.) with YAML front matter
- `_data/navigation.yml` — main menu links
- `_includes/` — reusable Liquid partials (author-profile, head, footer, masthead, etc.)
- `_sass/` — SCSS partials; entry point is `assets/css/main.scss`
- `images/` — site images; `files/` — PDFs (CV, talk slides)
- `markdown_generator/` — Python/Jupyter scripts that convert TSV data files into Jekyll collection markdown

**Collections** (defined in `_config.yml`): `talks`, `publications`, `teaching`, `portfolio` — each outputs pages at `/:collection/:path/`.

**Content pipeline for talks/publications:** Edit TSV files in `markdown_generator/`, run the corresponding Python script or Jupyter notebook to regenerate markdown files in `_talks/` or `_publications/`.
