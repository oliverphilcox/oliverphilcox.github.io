#!/usr/bin/env python3
"""Generate the website Research page (_pages/research.md) from INSPIRE-HEP.

The thematic prose and images are human-curated in research_config.yaml; only
the per-theme "Key papers" lists are auto-generated from INSPIRE. For each theme
we take the union of its pinned arXiv ids and any papers whose title matches the
theme keywords, then render the most recent `max_per_theme`.

Usage:
    python3 generate_research.py --config research_config.yaml
    python3 generate_research.py --config research_config.yaml --dry-run
"""

import argparse
import os
import sys
import time

import requests
import yaml


def fetch_papers_json(query, size=250):
    """Fetch papers from INSPIRE JSON API with retries."""
    url = "https://inspirehep.net/api/literature"
    params = {"q": f"a {query}", "size": size, "sort": "mostrecent"}
    fields = "texkeys,titles.title,earliest_date,arxiv_eprints.value,authors.full_name"
    params["fields"] = fields
    for attempt in range(3):
        try:
            resp = requests.get(url, params=params, timeout=60)
            resp.raise_for_status()
            return resp.json()["hits"]["hits"]
        except Exception as e:
            print(f"  Attempt {attempt + 1} failed: {e}", file=sys.stderr)
            if attempt < 2:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


def load_config(path):
    with open(path) as f:
        return yaml.safe_load(f)


def arxiv_id(meta):
    eps = meta.get("arxiv_eprints") or []
    return eps[0].get("value", "") if eps else ""


def title_of(meta):
    titles = meta.get("titles") or []
    return titles[0].get("title", "") if titles else ""


def surnames(meta):
    return [a["full_name"].split(",")[0].strip() for a in meta.get("authors", [])]


def author_label(meta):
    """'Philcox'; 'A & B'; 'A, B & C'; 'A, B, C, D'; 'A, B, C et al.' (>4)."""
    names = surnames(meta)
    if not names:
        return ""
    if len(names) > 4:
        return ", ".join(names[:3]) + " et al."
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + " & " + names[-1]


def paper_entry(meta):
    """Build a '[Label YEAR](arXiv url)' markdown link for one paper."""
    year = (meta.get("earliest_date") or "")[:4]
    aid = arxiv_id(meta)
    label = author_label(meta)
    if year:
        label = f"{label} {year}"
    return f"[{label}](https://arxiv.org/abs/{aid})"


def keyword_score(theme, meta):
    """Number of the theme's keywords that appear in the paper title."""
    t = title_of(meta).lower()
    return sum(1 for kw in theme.get("keywords", []) if kw.lower() in t)


def classify(config, papers_by_arxiv, pinned_anywhere, max_authors, global_exclude):
    """Assign each non-pinned paper to its single best-matching theme.

    Returns {theme_key: [metas]} of keyword-classified (non-pinned) papers.
    Ties broken by theme order in the config (earlier wins). Oversized
    collaboration papers and globally excluded ids are skipped.
    """
    by_theme = {t["key"]: [] for t in config["themes"]}
    for aid, meta in papers_by_arxiv.items():
        if aid in pinned_anywhere or aid in global_exclude:
            continue
        if len(meta.get("authors", [])) > max_authors:
            continue
        best_key, best_score = None, 0
        for theme in config["themes"]:  # config order = tie-break priority
            s = keyword_score(theme, meta)
            if s > best_score:
                best_key, best_score = theme["key"], s
        if best_key is not None:
            by_theme[best_key].append(meta)
    return by_theme


def select_for_theme(theme, papers_by_arxiv, classified, global_exclude):
    """Chosen papers (most recent first): the pinned baseline, plus at most the
    single newest classified paper that is strictly newer than every pin.

    Pins guarantee the curated selection; capping the auto-additions at one
    genuinely-newer paper bounds churn to a single swap per rebuild.
    """
    max_n = theme.get("_max_per_theme", 3)
    pins = [p for p in (theme.get("pin") or []) if p not in global_exclude]
    pin_metas = [papers_by_arxiv[a] for a in pins if a in papers_by_arxiv]
    newest_pin_date = max((m.get("earliest_date", "") for m in pin_metas), default="")

    newer = [m for m in classified.get(theme["key"], [])
             if m.get("earliest_date", "") > newest_pin_date]
    newer.sort(key=lambda m: m.get("earliest_date", ""), reverse=True)
    extras = newer[:1]  # at most one auto-addition per rebuild

    candidates = pin_metas + extras
    candidates.sort(key=lambda m: m.get("earliest_date", ""), reverse=True)
    return candidates[:max_n]


FRONT_MATTER = """---
layout: page
permalink: /research/
title: Research
description: An overview of my research interests and key results.
keywords: galaxy clustering bispectrum power spectrum CMB primordial non-Gaussianity inflation parity violation Hubble constant dark energy simulation-based inference BOSS DESI Planck cosmological collider neutrino masses trispectrum perturbation theory EFT large-scale structure
nav: true
nav_order: 5
---"""

IMG_STYLE = (
    "float: right; margin: 0 0 1em 1.5em; width: 260px; border-radius: 4px; "
    "box-shadow: 0 2px 6px rgba(0,0,0,0.15);"
)


def render(config, papers):
    papers_by_arxiv = {}
    for h in papers:
        meta = h["metadata"]
        aid = arxiv_id(meta)
        if aid and aid not in papers_by_arxiv:
            papers_by_arxiv[aid] = meta

    pinned_anywhere = set()
    for theme in config["themes"]:
        pinned_anywhere.update(theme.get("pin", []) or [])

    max_per_theme = config.get("max_per_theme", 3)
    max_authors = config.get("max_authors", 12)
    global_exclude = set(config.get("exclude", []) or [])

    classified = classify(
        config, papers_by_arxiv, pinned_anywhere, max_authors, global_exclude
    )

    lines = [FRONT_MATTER, ""]
    lines.append(
        f"*Auto-generated from recent publications. See "
        f"[InspireHEP](https://inspirehep.net/authors/{config['author_id']}) "
        f"for a full list of papers.*"
    )
    lines.append("")

    for theme in config["themes"]:
        theme["_max_per_theme"] = max_per_theme
        chosen = select_for_theme(theme, papers_by_arxiv, classified, global_exclude)
        if not chosen:
            print(f"  WARNING: no papers selected for theme '{theme['key']}'",
                  file=sys.stderr)

        lines.append(f"## {theme['title']}")
        lines.append("")
        lines.append(
            f'<img src="{theme["image"]}" alt="{theme["alt"]}" style="{IMG_STYLE}">'
        )
        lines.append("")
        # Collapse the folded YAML blurb into a single clean paragraph.
        lines.append(" ".join(theme["blurb"].split()))
        lines.append("")
        entries = ", ".join(paper_entry(m) for m in chosen)
        lines.append(f"Key papers: {entries}")
        lines.append("")
        lines.append('<div style="clear: both;"></div>')
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate research.md from INSPIRE-HEP")
    parser.add_argument("--config", required=True)
    parser.add_argument("--dry-run", action="store_true",
                        help="Print output instead of writing the file")
    parser.add_argument("--output", default="../_pages/research.md",
                        help="Output path, relative to the config file directory")
    args = parser.parse_args()

    config = load_config(args.config)
    config_dir = os.path.dirname(os.path.abspath(args.config))

    print("Fetching papers from INSPIRE JSON API...")
    papers = fetch_papers_json(config.get("author_query", "Oliver.H.E.Philcox.1"))
    print(f"  Fetched {len(papers)} papers")

    content = render(config, papers)

    if args.dry_run:
        print("\n" + content)
        return

    out = os.path.normpath(os.path.join(config_dir, args.output))
    with open(out, "w") as f:
        f.write(content)
    print(f"  Wrote {out}")
    print("Done.")


if __name__ == "__main__":
    main()
