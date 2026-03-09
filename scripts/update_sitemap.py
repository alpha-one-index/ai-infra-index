#!/usr/bin/env python3
"""Rebuild sitemap.xml from all content directories.

Scans specs/, specs/gpu/, providers/, comparisons/, snapshots/,
usecases/, glossary/, and landing/ for .md and .html files,
then writes a valid sitemap.xml with proper lastmod, priority,
and changefreq values.
"""

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://alpha-one-index.github.io/ai-infra-index"
SITEMAP_PATH = ROOT / "sitemap.xml"

# Directories to scan and their priority/changefreq
CONTENT_CONFIG = {
    "specs": {"priority": "0.8", "changefreq": "weekly"},
    "specs/gpu": {"priority": "0.8", "changefreq": "weekly"},
    "providers": {"priority": "0.7", "changefreq": "weekly"},
    "comparisons": {"priority": "0.7", "changefreq": "weekly"},
    "snapshots": {"priority": "0.6", "changefreq": "weekly"},
    "usecases": {"priority": "0.7", "changefreq": "monthly"},
    "glossary": {"priority": "0.6", "changefreq": "monthly"},
    "landing": {"priority": "0.9", "changefreq": "daily"},
    "data": {"priority": "0.5", "changefreq": "hourly"},
}

# Top-level files to include
TOP_LEVEL_FILES = [
    "index.html",
    "README.md",
]


def git_last_modified(filepath: str) -> str:
    """Get the last git commit date for a file."""
    try:
        ts = subprocess.check_output(
            ["git", "log", "-1", "--format=%aI", "--", filepath],
            text=True,
        ).strip()
        if ts:
            return ts[:10]  # YYYY-MM-DD
    except subprocess.CalledProcessError:
        pass
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def collect_urls() -> list[dict]:
    """Collect all content URLs with metadata."""
    urls = []

    # Top-level pages
    for fname in TOP_LEVEL_FILES:
        fpath = ROOT / fname
        if fpath.exists():
            url_path = fname.replace(".md", "").replace("README", "")
            if url_path == "":
                url_path = "/"
            urls.append({
                "loc": f"{BASE_URL}/{url_path}" if url_path != "/" else f"{BASE_URL}/",
                "lastmod": git_last_modified(str(fpath)),
                "priority": "1.0",
                "changefreq": "daily",
            })

    # Content directories
    for dir_name, config in CONTENT_CONFIG.items():
        dir_path = ROOT / dir_name
        if not dir_path.is_dir():
            continue
        for fpath in sorted(dir_path.glob("*")):
            if fpath.suffix not in (".md", ".html", ".json"):
                continue
            if fpath.name.startswith(".") or fpath.name.startswith("_"):
                continue
            rel = fpath.relative_to(ROOT)
            # Build URL path
            url_path = str(rel)
            urls.append({
                "loc": f"{BASE_URL}/{url_path}",
                "lastmod": git_last_modified(str(fpath)),
                "priority": config["priority"],
                "changefreq": config["changefreq"],
            })

    return urls


def build_sitemap(urls: list[dict]) -> str:
    """Build sitemap XML string."""
    urlset = Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

    for entry in urls:
        url_el = SubElement(urlset, "url")
        SubElement(url_el, "loc").text = entry["loc"]
        SubElement(url_el, "lastmod").text = entry["lastmod"]
        SubElement(url_el, "changefreq").text = entry["changefreq"]
        SubElement(url_el, "priority").text = entry["priority"]

    raw = tostring(urlset, encoding="unicode")
    pretty = parseString(raw).toprettyxml(indent="  ")
    # Remove extra XML declaration line from minidom
    lines = pretty.split("\n")
    if lines[0].startswith("<?xml"):
        lines[0] = '<?xml version="1.0" encoding="UTF-8"?>'
    return "\n".join(lines)


def main():
    urls = collect_urls()
    sitemap = build_sitemap(urls)
    SITEMAP_PATH.write_text(sitemap, encoding="utf-8")
    print(f"Sitemap updated: {len(urls)} URLs written to {SITEMAP_PATH}")


if __name__ == "__main__":
    main()
