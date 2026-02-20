#!/usr/bin/env python3
"""Generate CV publications (pubs.tex) and website bibliography (papers.bib)
from INSPIRE-HEP API data.

Usage:
    python3 generate_pubs.py --config pubs_config.yaml
    python3 generate_pubs.py --config pubs_config.yaml --bibtex-only
    python3 generate_pubs.py --config pubs_config.yaml --pubstex-only
    python3 generate_pubs.py --config pubs_config.yaml --dry-run
"""

import argparse
import os
import re
import sys
import time

import requests
import yaml

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PHILCOX_BOLD = r"\textbf{Philcox, O.\,H.\,E.}"

# Unicode -> LaTeX for author names
UNICODE_TO_LATEX = {
    "\u00e4": '\\"a',  # ä
    "\u00eb": '\\"e',  # ë
    "\u00ef": '\\"\\i',  # ï
    "\u00f6": '\\"o',  # ö
    "\u00fc": '\\"u',  # ü
    "\u00c4": '\\"A',  # Ä
    "\u00d6": '\\"O',  # Ö
    "\u00dc": '\\"U',  # Ü
    "\u00e9": "\\'e",  # é
    "\u00e8": "\\`e",  # è
    "\u00e1": "\\'a",  # á
    "\u00e0": "\\`a",  # à
    "\u00ed": "\\'\\i",  # í
    "\u00f3": "\\'o",  # ó
    "\u00fa": "\\'u",  # ú
    "\u0107": "\\'c",  # ć
    "\u010d": "\\v{c}",  # č
    "\u0161": "\\v{s}",  # š
    "\u017e": "\\v{z}",  # ž
    "\u0159": "\\v{r}",  # ř
    "\u00f1": "\\~n",  # ñ
    "\u00f8": "{\\o}",  # ø
    "\u0142": "{\\l}",  # ł
    "\u00e6": "{\\ae}",  # æ
}

# Journals where page ranges should use $start-end$ (math-mode dash)
PAGE_RANGE_JOURNALS = {
    "Mon.Not.Roy.Astron.Soc.",
    "JHEAp",
}

# Journals that use issue-number style formatting (volume pages, no bold vol)
JCAP_STYLE_JOURNALS = {"JCAP"}

# Journals where the issue number should be used as pages
ISSUE_AS_PAGES_JOURNALS = {
    "Proc.Nat.Acad.Sci.",
    "Proc.Roy.Soc.Lond.A",
}

# Maximum number of authors before truncating in contributing-author section
CONTRIB_AUTHOR_TRUNCATE = 6

# If Philcox is within first N authors, list up to and including Philcox
CONTRIB_PHILCOX_CUTOFF = 6


# ---------------------------------------------------------------------------
# Data fetching
# ---------------------------------------------------------------------------


def fetch_papers_json(query, size=250):
    """Fetch papers from INSPIRE JSON API with retries."""
    url = "https://inspirehep.net/api/literature"
    params = {
        "q": f"a {query}",
        "size": size,
        "sort": "mostrecent",
    }
    for attempt in range(3):
        try:
            resp = requests.get(url, params=params, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            return data["hits"]["hits"]
        except Exception as e:
            print(f"  Attempt {attempt + 1} failed: {e}", file=sys.stderr)
            if attempt < 2:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


def fetch_bibtex(query, size=250):
    """Fetch raw BibTeX string from INSPIRE."""
    url = "https://inspirehep.net/api/literature"
    params = {
        "q": f"a {query}",
        "size": size,
        "sort": "mostrecent",
        "format": "bibtex",
    }
    for attempt in range(3):
        try:
            resp = requests.get(url, params=params, timeout=60)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            print(f"  BibTeX attempt {attempt + 1} failed: {e}", file=sys.stderr)
            if attempt < 2:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------


def load_config(path):
    with open(path) as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# Paper metadata helpers
# ---------------------------------------------------------------------------


def get_texkey(paper):
    keys = paper.get("texkeys", [])
    return keys[0] if keys else ""


def get_arxiv_id(paper, config=None):
    texkey = get_texkey(paper)
    # Check override first
    if config:
        ovr = config.get("overrides", {}).get(texkey, {})
        if "arxiv_id" in ovr:
            return ovr["arxiv_id"]
    eprints = paper.get("arxiv_eprints", [])
    if eprints:
        return eprints[0].get("value", "")
    return ""


def get_doi(paper):
    dois = paper.get("dois", [])
    if dois:
        return dois[0].get("value", "")
    return ""


def is_philcox_author(full_name):
    return "Philcox" in full_name


# ---------------------------------------------------------------------------
# Author name formatting
# ---------------------------------------------------------------------------


def unicode_to_latex(text):
    for char, latex in UNICODE_TO_LATEX.items():
        text = text.replace(char, latex)
    return text


def format_author_name(full_name, author_overrides=None):
    """Convert INSPIRE 'Last, First Middle' to 'Last, F.\\,M.' format."""
    if is_philcox_author(full_name):
        return PHILCOX_BOLD

    # Check for explicit override
    if author_overrides and full_name in author_overrides:
        return author_overrides[full_name]

    parts = full_name.split(",", 1)
    if len(parts) != 2:
        return unicode_to_latex(full_name)

    last_name = unicode_to_latex(parts[0].strip())
    first_names_str = parts[1].strip()

    # Split first names on whitespace
    name_tokens = first_names_str.split()
    initials = []
    for token in name_tokens:
        if "-" in token:
            # Hyphenated: "Shi-Fan" -> "S.-F."
            hyph_parts = token.split("-")
            hyph_inits = []
            for hp in hyph_parts:
                if hp:
                    hyph_inits.append(hp[0] + ".")
            initials.append("-".join(hyph_inits))
        elif len(token) <= 2 and token.endswith("."):
            # Already an initial like "M."
            initials.append(token)
        else:
            initials.append(token[0] + ".")

    formatted = "\\,".join(initials)
    return f"{last_name}, {formatted}"


# ---------------------------------------------------------------------------
# Alphabetization detection
# ---------------------------------------------------------------------------


def detect_alphabetized(authors):
    """Check if author last names are approximately alphabetically sorted."""
    if len(authors) <= 1:
        return False
    last_names = []
    for a in authors:
        name = a.get("full_name", "")
        ln = name.split(",")[0].strip().lower()
        last_names.append(ln)
    n = len(last_names)
    if n <= 20:
        return last_names == sorted(last_names)
    else:
        sorted_pairs = sum(
            1 for i in range(n - 1) if last_names[i] <= last_names[i + 1]
        )
        return sorted_pairs >= 0.8 * (n - 1)


# ---------------------------------------------------------------------------
# Paper classification
# ---------------------------------------------------------------------------


def classify_paper(texkey, config):
    """Return 'major', 'contributing', or 'exclude'."""
    if texkey in config.get("exclude", []):
        return "exclude"
    if texkey in config.get("contributing_author", []):
        return "contributing"
    return "major"


# ---------------------------------------------------------------------------
# Title formatting
# ---------------------------------------------------------------------------


def _mathml_to_latex(text):
    """Convert simple MathML fragments in INSPIRE titles to LaTeX."""

    def _convert_math(m):
        inner = m.group(1)
        # Handle subscripts: <msub><mi>f</mi><mrow><mi>NL</mi></mrow></msub>
        inner = re.sub(
            r"<msub>\s*<mi>([^<]*)</mi>\s*<mrow>\s*<mi>([^<]*)</mi>\s*</mrow>\s*</msub>",
            r"\1_{\\rm \2}",
            inner,
        )
        inner = re.sub(
            r"<msub>\s*<mi>([^<]*)</mi>\s*<mn>([^<]*)</mn>\s*</msub>",
            r"\1_{\2}",
            inner,
        )
        # Strip all remaining tags
        inner = re.sub(r"<[^>]+>", "", inner)
        inner = inner.strip()
        # If the result is just a word (no math operators), use \textit
        if re.match(r"^[A-Za-z]+$", inner) and len(inner) > 2:
            return f"\\textit{{{inner}}}"
        return f"${inner}$"

    text = re.sub(
        r"<math[^>]*>(.*?)</math>", _convert_math, text, flags=re.DOTALL
    )
    return text


def _fix_title_unicode(title):
    """Fix unicode characters in titles that should be LaTeX."""
    title = title.replace("\u039b", "\\Lambda")  # Λ
    title = title.replace("\u03b1", "$\\alpha$")  # α
    title = title.replace("\u03b2", "$\\beta$")  # β
    title = title.replace("\u03b3", "$\\gamma$")  # γ
    title = title.replace("\u2013", "--")  # en-dash
    title = title.replace("\u2014", "---")  # em-dash
    title = title.replace("\u2019", "'")  # right single quote
    title = title.replace("\u2018", "`")  # left single quote
    title = title.replace("\u201c", "``")  # left double quote
    title = title.replace("\u201d", "''")  # right double quote
    # Escape bare % but avoid double-escaping already-escaped \%
    title = re.sub(r"(?<!\\)%", r"\\%", title)
    # Fix bare \LambdaCDM -> $\Lambda$CDM
    title = title.replace("\\LambdaCDM", "$\\Lambda$CDM")
    return title


def _get_arxiv_title(paper):
    """Get the arXiv-source title if available."""
    for t in paper.get("titles", []):
        if t.get("source", "").lower() == "arxiv":
            return t.get("title", "")
    return None


def get_title(paper, config):
    texkey = get_texkey(paper)
    overrides = config.get("title_overrides", {}) or {}
    if texkey in overrides:
        return overrides[texkey]
    titles = paper.get("titles", [])
    if not titles:
        return ""

    # Strategy: use journal (first) title for published papers,
    # arXiv title for submitted/unpublished (title-cased, author's original).
    pub_infos = paper.get("publication_info", [])
    has_journal = bool(pub_infos and pub_infos[0].get("journal_title"))

    if has_journal:
        # Published: use default (journal) title
        title = titles[0].get("title", "")
    else:
        # Not published: prefer arXiv title (title-cased)
        title = _get_arxiv_title(paper) or titles[0].get("title", "")

    # Strip outer braces from INSPIRE
    if title.startswith("{") and title.endswith("}"):
        title = title[1:-1]
    # Convert MathML fragments to LaTeX
    title = _mathml_to_latex(title)
    # Fix unicode
    title = _fix_title_unicode(title)
    # Replace {\&} or bare & with \&
    title = title.replace("{\\&}", "\\&")
    title = re.sub(r"(?<!\\)&", r"\\&", title)
    return title


# ---------------------------------------------------------------------------
# Publication info
# ---------------------------------------------------------------------------


def get_pub_info(paper, config):
    """Get publication info, preferring INSPIRE data over config overrides.

    Returns dict with: status, journal, volume, pages, year, doi, inspire_journal
    """
    texkey = get_texkey(paper)
    override = config.get("overrides", {}).get(texkey, {})
    doi = get_doi(paper)
    if override.get("doi"):
        doi = override["doi"]

    # Check INSPIRE publication_info first
    pub_infos = paper.get("publication_info", [])
    pi = pub_infos[0] if pub_infos else {}
    inspire_journal = pi.get("journal_title", "")

    if inspire_journal:
        journal_latex = config.get("journal_map", {}).get(
            inspire_journal, inspire_journal
        )
        volume = pi.get("journal_volume", "")
        year = str(pi.get("year", ""))
        page_start = pi.get("page_start", "")
        page_end = pi.get("page_end", "")
        artid = pi.get("artid", "")
        journal_issue = pi.get("journal_issue", "")

        # Determine pages string
        if inspire_journal in ISSUE_AS_PAGES_JOURNALS and journal_issue:
            pages = journal_issue
        elif page_start and page_end and page_start != page_end:
            if inspire_journal in PAGE_RANGE_JOURNALS:
                # Check for letter-pages (e.g. L42-L45)
                if page_start[0].isalpha():
                    pages = f"{page_start}-{page_end}"
                else:
                    pages = f"${page_start}-{page_end}$"
            else:
                pages = page_start  # APS-style: just use page_start as article ID
        elif artid:
            pages = artid
        elif page_start:
            pages = page_start
        else:
            pages = ""

        return {
            "status": "published",
            "journal": journal_latex,
            "volume": volume,
            "pages": pages,
            "year": year,
            "doi": doi,
            "inspire_journal": inspire_journal,
        }

    # No INSPIRE publication info -> check overrides
    if override:
        status = override.get("status", "")
        if status == "published":
            return {
                "status": "published",
                "journal": override.get("journal", ""),
                "volume": override.get("volume", ""),
                "pages": override.get("pages", ""),
                "year": override.get("year", ""),
                "doi": doi,
                "inspire_journal": "",
            }
        elif status == "submitted":
            return {"status": "submitted", "journal": override.get("journal", ""), "doi": doi}
        elif status == "accepted":
            return {"status": "accepted", "journal": override.get("journal", ""), "doi": doi}
        elif status == "book_chapter":
            return {
                "status": "book_chapter",
                "verbatim_ref": override.get("verbatim_ref", ""),
                "doi": doi,
            }
        elif status == "white_paper":
            return {
                "status": "white_paper",
                "verbatim_ref": override.get("verbatim_ref", ""),
                "doi": doi,
            }

    return {"status": "unpublished", "doi": doi}


# ---------------------------------------------------------------------------
# Reference formatting
# ---------------------------------------------------------------------------


def format_reference(paper, config):
    """Format the journal/status + arXiv link portion of an item."""
    pub = get_pub_info(paper, config)
    arxiv_id = get_arxiv_id(paper, config)

    arxiv_part = ""
    if arxiv_id:
        arxiv_part = f"(\\href{{https://arxiv.org/abs/{arxiv_id}}}{{arXiv}})"

    if pub["status"] == "published":
        doi_url = f'https://doi.org/{pub["doi"]}' if pub.get("doi") else ""
        journal = pub["journal"]
        volume = pub["volume"]
        pages = pub["pages"]
        year = pub["year"]
        inspire_j = pub.get("inspire_journal", "")

        # Build journal reference
        if doi_url:
            ref = f"\\href{{{doi_url}}}{{\\textit{{{journal}}}}}"
        else:
            ref = f"\\textit{{{journal}}}"

        if inspire_j in JCAP_STYLE_JOURNALS:
            # JCAP: no bold volume, just "volume pages (year)"
            if volume:
                ref += f" {volume}"
            if pages:
                ref += f" {pages}"
        else:
            if volume:
                ref += f" \\textbf{{{volume}}}"
            if pages:
                ref += f", {pages}"

        ref += f" ({year})"
        if arxiv_part:
            ref += f" {arxiv_part}"
        return ref

    elif pub["status"] == "submitted":
        ref = f'\\textit{{submitted to {pub["journal"]}}}'
        if arxiv_part:
            ref += f" {arxiv_part}"
        return ref

    elif pub["status"] == "accepted":
        ref = f'\\textit{{accepted by {pub["journal"]}}}'
        if arxiv_part:
            ref += f" {arxiv_part}"
        return ref

    elif pub["status"] in ("book_chapter", "white_paper"):
        ref = pub.get("verbatim_ref", "")
        if arxiv_part:
            ref += f" {arxiv_part}"
        return ref

    else:  # unpublished
        return arxiv_part


# ---------------------------------------------------------------------------
# Author list formatting
# ---------------------------------------------------------------------------


def format_author_list_major(paper, config):
    """Format author list for Major Author papers: list all authors."""
    authors = paper.get("authors", [])
    author_overrides = config.get("author_name_overrides", {}) or {}
    parts = []
    for a in authors:
        parts.append(format_author_name(a.get("full_name", ""), author_overrides))
    return ", ".join(parts)


def _find_philcox_position(authors):
    for i, a in enumerate(authors):
        if is_philcox_author(a.get("full_name", "")):
            return i
    return None


def format_author_list_contributing(paper, config):
    """Format author list for Contributing Author papers.

    - <=6 authors: list all
    - >6 authors with Philcox in first 6: list up to Philcox, then et al.
    - >6 authors with Philcox later: first author + et al. (inc. Philcox)
    """
    authors = paper.get("authors", [])
    n = len(authors)

    if n <= CONTRIB_AUTHOR_TRUNCATE:
        return format_author_list_major(paper, config)

    author_overrides = config.get("author_name_overrides", {}) or {}
    pos = _find_philcox_position(authors)

    if pos is not None and pos < CONTRIB_PHILCOX_CUTOFF:
        # Show authors up to and including Philcox, then et al.
        parts = []
        for a in authors[: pos + 1]:
            parts.append(format_author_name(a.get("full_name", ""), author_overrides))
        return ", ".join(parts) + r", \textit{et al.}"
    else:
        # First author + et al. (inc. Philcox)
        first = format_author_name(authors[0].get("full_name", ""), author_overrides)
        return first + r", \textit{et al.} (inc.\,\," + PHILCOX_BOLD + ")"


# ---------------------------------------------------------------------------
# Item formatting
# ---------------------------------------------------------------------------


def format_item(paper, config, is_contributing=False):
    """Format a single \\item line for pubs.tex."""
    authors = paper.get("authors", [])
    is_alpha = detect_alphabetized(authors)
    star = "*" if is_alpha else ""

    if is_contributing:
        author_str = format_author_list_contributing(paper, config)
    else:
        author_str = format_author_list_major(paper, config)

    title = get_title(paper, config)
    ref = format_reference(paper, config)

    # Build the line
    line = f"    \\item {star}{author_str}, ``{title}'', {ref}."

    # Clean up any double periods at the end
    line = re.sub(r"\.\.$", ".", line)

    return line


# ---------------------------------------------------------------------------
# Full pubs.tex generation
# ---------------------------------------------------------------------------


def generate_pubstex(papers, config):
    """Generate the full pubs.tex content."""
    major = []
    contributing = []

    for paper in papers:
        texkey = get_texkey(paper)
        cat = classify_paper(texkey, config)
        if cat == "exclude":
            continue
        elif cat == "contributing":
            contributing.append(paper)
        else:
            major.append(paper)

    lines = []

    # --- Major Author ---
    lines.append(r"\textit{\textbf{Major Author}}")
    lines.append(r"\begin{enumerate}")
    for paper in major:
        lines.append(format_item(paper, config, is_contributing=False))
    # Append any extra major-author items not in INSPIRE
    for extra in config.get("extra_major_author", []):
        lines.append(extra.rstrip())
    lines.append(r"\end{enumerate}")
    lines.append("")
    lines.append(r"\vskip 4 pt ")
    lines.append("")

    # --- Contributing Author ---
    lines.append(r"\textit{\textbf{Contributing Author}}")
    lines.append("")
    lines.append(r"\begin{enumerate}[resume]")
    for paper in contributing:
        lines.append(format_item(paper, config, is_contributing=True))
    lines.append(r"\end{enumerate}")
    lines.append("")
    lines.append(r"\vskip 4 pt ")
    lines.append("")

    # --- Other Works ---
    lines.append(r"\textit{\textbf{Other Works}}")
    lines.append(r"\begin{enumerate}[resume]")
    other_works = config.get("other_works", "")
    lines.append(other_works.rstrip())
    lines.append(r"\end{enumerate}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# BibTeX generation
# ---------------------------------------------------------------------------


def generate_bibtex(raw_bib, config):
    """Process raw BibTeX: inject selected flags, remove excluded entries."""
    excluded = set(config.get("exclude", []))
    selected = set(config.get("selected_papers", []))

    # Split into individual entries (split on blank-line-then-@)
    entries = re.split(r"\n(?=@)", raw_bib.lstrip())
    result = []

    for entry in entries:
        if not entry.strip():
            continue

        # Extract texkey
        m = re.match(r"@\w+\{([^,]+),", entry)
        if not m:
            result.append(entry)
            continue
        texkey = m.group(1).strip()

        if texkey in excluded:
            continue

        # Inject selected/bibtex_show for selected papers (if not already present)
        if texkey in selected and "selected" not in entry:
            first_nl = entry.index("\n")
            entry = (
                entry[: first_nl + 1]
                + "    selected = {true},\n"
                + "    bibtex_show = {true},\n"
                + entry[first_nl + 1 :]
            )

        result.append(entry)

    return "\n".join(result)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Generate CV publications from INSPIRE-HEP"
    )
    parser.add_argument("--config", required=True, help="Path to YAML config file")
    parser.add_argument(
        "--dry-run", action="store_true", help="Print output instead of writing files"
    )
    parser.add_argument(
        "--bibtex-only", action="store_true", help="Only generate papers.bib"
    )
    parser.add_argument(
        "--pubstex-only", action="store_true", help="Only generate pubs.tex"
    )
    args = parser.parse_args()

    config = load_config(args.config)
    query = config.get("author_query", "Oliver.H.E.Philcox.1")
    config_dir = os.path.dirname(os.path.abspath(args.config))

    if not args.bibtex_only:
        print("Fetching papers from INSPIRE JSON API...")
        papers_raw = fetch_papers_json(query)
        papers = [p["metadata"] for p in papers_raw]
        print(f"  Fetched {len(papers)} papers")

        pubstex = generate_pubstex(papers, config)

        # Write to all configured output paths
        out_keys = ["output_pubstex", "output_pubstex_ci"]
        if args.dry_run:
            print("\n=== pubs.tex ===")
            print(pubstex)
        else:
            for key in out_keys:
                path = config.get(key)
                if not path:
                    continue
                out = os.path.normpath(os.path.join(config_dir, path))
                os.makedirs(os.path.dirname(out), exist_ok=True)
                with open(out, "w") as f:
                    f.write(pubstex)
                print(f"  Wrote {out}")

    if not args.pubstex_only:
        print("Fetching BibTeX from INSPIRE...")
        raw_bib = fetch_bibtex(query)
        print(f"  Fetched BibTeX ({len(raw_bib)} bytes)")

        bibtex = generate_bibtex(raw_bib, config)

        out = os.path.normpath(
            os.path.join(
                config_dir, config.get("output_bibtex", "../_bibliography/papers.bib")
            )
        )
        if args.dry_run:
            print("\n=== papers.bib (first 3000 chars) ===")
            print(bibtex[:3000])
        else:
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with open(out, "w") as f:
                f.write(bibtex)
            print(f"  Wrote {out}")

    print("Done.")


if __name__ == "__main__":
    main()
