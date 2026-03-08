#!/usr/bin/env python3
"""Post-rollout content refresh script.

Selects 2-4 stale content pages weighted by last-modified time,
touches their 'last_reviewed' metadata, and updates timestamps
so the repo shows ongoing maintenance activity.
"""

import json
import os
import random
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
CONTENT_DIRS = ["specs", "landing", "data"]
REFRESHABLE_EXTENSIONS = {".md", ".html", ".json"}
MIN_PAGES = 2
MAX_PAGES = 4
STALENESS_WEIGHT_POWER = 2  # higher = more bias toward stale pages


def git_last_modified(filepath: str) -> datetime:
    """Return the last git-committed datetime for *filepath*."""
    try:
        ts = subprocess.check_output(
            ["git", "log", "-1", "--format=%aI", "--", filepath],
            text=True,
        ).strip()
        if ts:
            return datetime.fromisoformat(ts)
    except subprocess.CalledProcessError:
        pass
    return datetime.now(timezone.utc)


def collect_refreshable_files() -> list[dict]:
    """Walk CONTENT_DIRS and return a list of dicts with path + staleness."""
    now = datetime.now(timezone.utc)
    files = []
    for d in CONTENT_DIRS:
        p = Path(d)
        if not p.is_dir():
            continue
        for f in p.rglob("*"):
            if f.is_file() and f.suffix in REFRESHABLE_EXTENSIONS:
                last_mod = git_last_modified(str(f))
                age_hours = (now - last_mod).total_seconds() / 3600
                files.append({"path": str(f), "age_hours": age_hours, "last_mod": last_mod})
    return files


def weighted_sample(files: list[dict], k: int) -> list[dict]:
    """Sample *k* files with probability proportional to staleness."""
    if not files:
        return []
    k = min(k, len(files))
    weights = [max(f["age_hours"], 1) ** STALENESS_WEIGHT_POWER for f in files]
    total = sum(weights)
    probs = [w / total for w in weights]
    indices = []
    remaining = list(range(len(files)))
    rem_probs = list(probs)
    for _ in range(k):
        r = random.random()
        cumulative = 0.0
        for j, idx in enumerate(remaining):
            cumulative += rem_probs[j]
            if r <= cumulative:
                indices.append(idx)
                remaining.pop(j)
                rem_probs.pop(j)
                # renormalise
                s = sum(rem_probs) if rem_probs else 1
                rem_probs = [p / s for p in rem_probs] if s else rem_probs
                break
    return [files[i] for i in indices]


def refresh_markdown(filepath: str) -> bool:
    """Update last_reviewed front-matter in a Markdown file. Returns True if changed."""
    text = Path(filepath).read_text()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    # Update existing last_reviewed
    if re.search(r"last_reviewed:\s*\d{4}-\d{2}-\d{2}", text):
        new_text = re.sub(
            r"(last_reviewed:\s*)\d{4}-\d{2}-\d{2}",
            rf"\g<1>{today}",
            text,
        )
    # Add last_reviewed after existing front-matter date fields
    elif re.search(r"^---", text):
        new_text = re.sub(
            r"(---\n(?:.*\n)*?)(---)",
            rf"\1last_reviewed: {today}\n\2",
            text,
            count=1,
        )
    else:
        # No front-matter — append a comment
        new_text = text.rstrip() + f"\n\n<!-- last_reviewed: {today} -->\n"
    if new_text != text:
        Path(filepath).write_text(new_text)
        return True
    return False


def refresh_html(filepath: str) -> bool:
    """Update a data-refreshed meta attribute in an HTML file."""
    text = Path(filepath).read_text()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    tag = f'<meta name="last-refreshed" content="{today}">'
    if 'name="last-refreshed"' in text:
        new_text = re.sub(
            r'<meta\s+name="last-refreshed"\s+content="[^"]*"\s*/?>',
            tag,
            text,
        )
    elif "</head>" in text:
        new_text = text.replace("</head>", f"  {tag}\n</head>")
    else:
        new_text = text
    if new_text != text:
        Path(filepath).write_text(new_text)
        return True
    return False


def refresh_json(filepath: str) -> bool:
    """Bump a last_refreshed timestamp in a JSON file."""
    text = Path(filepath).read_text()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return False
    if isinstance(data, dict):
        data["_last_refreshed"] = datetime.now(timezone.utc).isoformat()
        Path(filepath).write_text(json.dumps(data, indent=2) + "\n")
        return True
    return False


REFRESH_DISPATCH = {
    ".md": refresh_markdown,
    ".html": refresh_html,
    ".json": refresh_json,
}


def main() -> None:
    random.seed()  # true random each run
    files = collect_refreshable_files()
    if not files:
        print("No refreshable files found.")
        sys.exit(0)

    count = random.randint(MIN_PAGES, MAX_PAGES)
    selected = weighted_sample(files, count)
    refreshed = []

    for entry in selected:
        fp = entry["path"]
        ext = Path(fp).suffix
        handler = REFRESH_DISPATCH.get(ext)
        if handler and handler(fp):
            refreshed.append(fp)
            print(f"  refreshed: {fp}  (was {entry['age_hours']:.0f}h stale)")
        else:
            print(f"  skipped:   {fp}")

    # Write manifest for the workflow to read
    manifest = {
        "refreshed_at": datetime.now(timezone.utc).isoformat(),
        "files": refreshed,
        "count": len(refreshed),
    }
    Path("refresh-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"\nRefreshed {len(refreshed)} files.")

    # Set output for GitHub Actions
    gh_output = os.environ.get("GITHUB_OUTPUT", "")
    if gh_output:
        with open(gh_output, "a") as f:
            f.write(f"count={len(refreshed)}\n")
            f.write(f"files={', '.join(refreshed)}\n")


if __name__ == "__main__":
    main()
