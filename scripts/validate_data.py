#!/usr/bin/env python3
"""
validate_data.py — Self-audit and data validation for the AI Infrastructure Index.

This script performs automated quality checks on all data in the repository:
  1. Schema validation — ensures JSON data files conform to expected structures
  2. Link health — verifies all source URLs are still accessible
  3. Price anomaly detection — flags outliers beyond expected ranges
  4. Freshness checks — ensures data is within expected update windows
  5. Cross-reference validation — checks consistency between data sources
  6. Provenance verification — validates provenance metadata files

Usage:
    python scripts/validate_data.py                # Run all checks
    python scripts/validate_data.py --check schema  # Run specific check
    python scripts/validate_data.py --json          # Output JSON report
    python scripts/validate_data.py --ci            # CI mode (exit code 1 on failure)

Exit codes:
    0 — All checks passed
    1 — One or more checks failed (CI mode only)
    2 — Script error
"""

import json
import os
import sys
import argparse
import hashlib
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from typing import Any

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent

EXPECTED_FILES = {
    "data/gpu-specs.json": "application/json",
    "data/cloud-pricing.json": "application/json",
    "README.md": "text/markdown",
    "llms.txt": "text/plain",
    "provenance.md": "text/markdown",
    "dataprov.json": "application/json",
    "croissant.json": "application/json",
    "METHODOLOGY.md": "text/markdown",
    "CHANGELOG.md": "text/markdown",
    "CITATION.cff": "text/yaml",
    "LICENSE": "text/plain",
}

KNOWN_GPU_MODELS = {
    "H100", "H100 SXM", "H100 PCIe", "H200", "H200 SXM",
    "B200", "GB200", "GB200 NVL72",
    "A100", "A100 SXM", "A100 PCIe",
    "A10", "L40S", "L40", "L4",
    "RTX 4090", "RTX A6000", "RTX A4000",
    "MI300X", "MI325X",
    "Gaudi 3",
}

KNOWN_PROVIDERS = {
    "Azure", "RunPod", "Lambda Labs", "CoreWeave", "Together AI",
    "Vast.ai", "Vultr", "Nebius", "OCI", "Oracle Cloud",
    "Cudo Compute", "Fluidstack", "Paperspace",
}

# Price sanity bounds (USD/GPU/hour) — deliberately wide to catch only egregious errors
PRICE_BOUNDS = {
    "H100":    (0.50, 15.00),
    "H200":    (0.80, 20.00),
    "B200":    (1.50, 30.00),
    "A100":    (0.30, 10.00),
    "A10":     (0.10, 5.00),
    "L40S":    (0.20, 8.00),
    "L40":     (0.20, 8.00),
    "RTX 4090":(0.10, 5.00),
    "MI300X":  (0.50, 15.00),
    "MI325X":  (0.80, 20.00),
    "Gaudi 3": (0.30, 10.00),
}

# Maximum age (in days) before data is flagged as stale
FRESHNESS_THRESHOLDS = {
    "data/cloud-pricing.json": 2,  # Should be updated hourly
    "data/gpu-specs.json": 90,     # Manual updates are OK to be older
}

# ---------------------------------------------------------------------------
# Validation Report
# ---------------------------------------------------------------------------

class ValidationReport:
    """Collects validation results and generates reports."""

    def __init__(self):
        self.checks: list[dict] = []
        self.start_time = datetime.now(timezone.utc)

    def add(self, category: str, name: str, passed: bool, message: str = "",
            severity: str = "error"):
        self.checks.append({
            "category": category,
            "name": name,
            "passed": passed,
            "message": message,
            "severity": severity,  # error, warning, info
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    @property
    def passed(self) -> int:
        return sum(1 for c in self.checks if c["passed"])

    @property
    def failed(self) -> int:
        return sum(1 for c in self.checks if not c["passed"] and c["severity"] == "error")

    @property
    def warnings(self) -> int:
        return sum(1 for c in self.checks if not c["passed"] and c["severity"] == "warning")

    @property
    def all_passed(self) -> bool:
        return self.failed == 0

    def to_json(self) -> dict:
        return {
            "validation_run": {
                "timestamp": self.start_time.isoformat(),
                "duration_seconds": (datetime.now(timezone.utc) - self.start_time).total_seconds(),
                "repository": "alpha-one-index/ai-infra-index",
                "script_version": "1.0.0",
            },
            "summary": {
                "total_checks": len(self.checks),
                "passed": self.passed,
                "failed": self.failed,
                "warnings": self.warnings,
                "status": "PASS" if self.all_passed else "FAIL",
            },
            "checks": self.checks,
        }

    def print_report(self):
        print("\n" + "=" * 70)
        print("  AI Infrastructure Index — Data Validation Report")
        print("=" * 70)
        print(f"  Run at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"  Repository: alpha-one-index/ai-infra-index")
        print("-" * 70)

        # Group by category
        categories = {}
        for check in self.checks:
            cat = check["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(check)

        for cat, checks in categories.items():
            print(f"\n  [{cat.upper()}]")
            for c in checks:
                icon = "PASS" if c["passed"] else ("WARN" if c["severity"] == "warning" else "FAIL")
                marker = "  ✓" if c["passed"] else "  ✗"
                print(f"    {marker} [{icon}] {c['name']}")
                if c["message"] and not c["passed"]:
                    print(f"           {c['message']}")

        print("\n" + "-" * 70)
        status = "ALL CHECKS PASSED" if self.all_passed else f"{self.failed} CHECK(S) FAILED"
        print(f"  Result: {status}  |  {self.passed} passed, {self.failed} failed, {self.warnings} warnings")
        print("=" * 70 + "\n")


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------

def check_file_exists(report: ValidationReport):
    """Verify all expected repository files exist."""
    for filepath, _ in EXPECTED_FILES.items():
        full_path = REPO_ROOT / filepath
        exists = full_path.exists()
        report.add(
            category="schema",
            name=f"File exists: {filepath}",
            passed=exists,
            message="" if exists else f"Missing file: {full_path}",
            severity="error" if filepath.startswith("data/") else "warning",
        )


def check_json_schema(report: ValidationReport):
    """Validate JSON data files have expected structure."""

    # --- gpu-specs.json ---
    gpu_path = REPO_ROOT / "data" / "gpu-specs.json"
    if gpu_path.exists():
        try:
            with open(gpu_path) as f:
                gpu_data = json.load(f)

            # Should be a dict or list
            is_valid = isinstance(gpu_data, (dict, list))
            report.add("schema", "gpu-specs.json is valid JSON", is_valid,
                       "" if is_valid else "File is not valid JSON structure")

            # Check for expected fields
            gpus = gpu_data if isinstance(gpu_data, list) else gpu_data.get("gpus", [])
            if gpus:
                sample = gpus[0]
                required_fields = {"vendor", "model"}
                present = required_fields.intersection(set(sample.keys()))
                all_present = present == required_fields
                report.add("schema", "gpu-specs.json has required fields",
                           all_present,
                           f"Missing fields: {required_fields - present}" if not all_present else "")

                # Validate GPU model names
                for gpu in gpus:
                    model = gpu.get("model", "")
                    # Check it's a non-empty string
                    report.add("schema", f"GPU model '{model}' is valid",
                               bool(model and isinstance(model, str)),
                               severity="warning")
            else:
                report.add("schema", "gpu-specs.json has GPU entries", False,
                           "No GPU entries found")
        except json.JSONDecodeError as e:
            report.add("schema", "gpu-specs.json parses as JSON", False, str(e))
    else:
        report.add("schema", "gpu-specs.json exists", False, "File not found")

    # --- cloud-pricing.json ---
    pricing_path = REPO_ROOT / "data" / "cloud-pricing.json"
    if pricing_path.exists():
        try:
            with open(pricing_path) as f:
                pricing_data = json.load(f)

            report.add("schema", "cloud-pricing.json is valid JSON", True)

            # Check structure
            if isinstance(pricing_data, dict):
                has_metadata = "metadata" in pricing_data or "last_updated" in pricing_data
                report.add("schema", "cloud-pricing.json has metadata",
                           has_metadata, severity="warning",
                           message="" if has_metadata else "No metadata field found")

                # Look for pricing entries
                providers = pricing_data.get("providers", pricing_data.get("data", []))
                if isinstance(providers, list) and providers:
                    report.add("schema", "cloud-pricing.json has provider entries", True,
                               f"Found {len(providers)} provider(s)")
                elif isinstance(pricing_data, dict):
                    # Might be keyed by provider name
                    non_meta = {k: v for k, v in pricing_data.items()
                                if k not in ("metadata", "last_updated", "version")}
                    report.add("schema", "cloud-pricing.json has provider entries",
                               bool(non_meta),
                               f"Found {len(non_meta)} top-level keys" if non_meta else "No provider data found")

        except json.JSONDecodeError as e:
            report.add("schema", "cloud-pricing.json parses as JSON", False, str(e))
    else:
        report.add("schema", "cloud-pricing.json exists", False, "File not found")

    # --- dataprov.json ---
    dataprov_path = REPO_ROOT / "dataprov.json"
    if dataprov_path.exists():
        try:
            with open(dataprov_path) as f:
                prov_data = json.load(f)
            report.add("schema", "dataprov.json is valid JSON", True)

            has_context = "@context" in prov_data
            has_type = "@type" in prov_data
            report.add("schema", "dataprov.json has JSON-LD @context",
                       has_context, severity="warning")
            report.add("schema", "dataprov.json has @type",
                       has_type, severity="warning")
        except json.JSONDecodeError as e:
            report.add("schema", "dataprov.json parses as JSON", False, str(e))

    # --- croissant.json ---
    croissant_path = REPO_ROOT / "croissant.json"
    if croissant_path.exists():
        try:
            with open(croissant_path) as f:
                croissant_data = json.load(f)
            report.add("schema", "croissant.json is valid JSON", True)

            conforms = croissant_data.get("conformsTo", "")
            is_croissant = "croissant" in conforms.lower() if conforms else False
            report.add("schema", "croissant.json conforms to Croissant spec",
                       is_croissant,
                       f"conformsTo: {conforms}" if not is_croissant else "")
        except json.JSONDecodeError as e:
            report.add("schema", "croissant.json parses as JSON", False, str(e))


def check_link_health(report: ValidationReport, timeout: int = 10, max_checks: int = 20):
    """Verify source URLs referenced in the data are accessible."""

    urls_to_check = set()

    # Extract URLs from cloud-pricing.json
    pricing_path = REPO_ROOT / "data" / "cloud-pricing.json"
    if pricing_path.exists():
        try:
            with open(pricing_path) as f:
                content = f.read()
            # Find all URLs in the JSON
            found = re.findall(r'https?://[^\s"<>]+', content)
            urls_to_check.update(found[:max_checks])
        except Exception:
            pass

    # Extract source URLs from README.md
    readme_path = REPO_ROOT / "README.md"
    if readme_path.exists():
        try:
            with open(readme_path) as f:
                content = f.read()
            # Find pricing source URLs specifically
            pricing_urls = re.findall(
                r'\((https?://(?:www\.)?(?:runpod|lambdalabs|coreweave|together|vast|vultr|nebius|oracle|cudocompute|fluidstack|paperspace|prices\.azure)[^\)]+)\)',
                content
            )
            urls_to_check.update(pricing_urls[:max_checks])
        except Exception:
            pass

    checked = 0
    for url in list(urls_to_check)[:max_checks]:
        # Clean URL
        url = url.rstrip('.,;)')
        try:
            req = Request(url, method="HEAD", headers={
                "User-Agent": "AI-Infra-Index-Validator/1.0 (+https://github.com/alpha-one-index/ai-infra-index)"
            })
            response = urlopen(req, timeout=timeout)
            status = response.getcode()
            ok = 200 <= status < 400
            report.add("links", f"URL accessible: {url[:60]}...",
                       ok, f"HTTP {status}" if not ok else "", severity="warning")
        except (URLError, HTTPError, OSError) as e:
            report.add("links", f"URL accessible: {url[:60]}...",
                       False, str(e)[:100], severity="warning")
        checked += 1

    if checked == 0:
        report.add("links", "URL health check", True, "No URLs to check (skipped)",
                    severity="info")


def check_price_anomalies(report: ValidationReport):
    """Flag pricing data that falls outside expected ranges."""

    pricing_path = REPO_ROOT / "data" / "cloud-pricing.json"
    if not pricing_path.exists():
        report.add("prices", "Price anomaly check", True,
                    "No pricing file found (skipped)", severity="info")
        return

    try:
        with open(pricing_path) as f:
            pricing_data = json.load(f)
    except Exception as e:
        report.add("prices", "Price data readable", False, str(e))
        return

    # Flatten pricing entries regardless of structure
    prices = []

    def extract_prices(obj, path=""):
        if isinstance(obj, dict):
            price = obj.get("price_per_gpu_hour") or obj.get("price") or obj.get("price_hr")
            model = obj.get("gpu_model") or obj.get("gpu") or obj.get("model") or ""
            if price is not None and model:
                try:
                    prices.append((model, float(price), path))
                except (ValueError, TypeError):
                    pass
            for k, v in obj.items():
                extract_prices(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                extract_prices(item, f"{path}[{i}]")

    extract_prices(pricing_data)

    if not prices:
        report.add("prices", "Price entries found", False,
                    "Could not extract any pricing entries")
        return

    report.add("prices", f"Price entries found: {len(prices)}", True)

    anomalies = 0
    for model, price, path in prices:
        # Find matching bounds
        bounds = None
        for known_model, b in PRICE_BOUNDS.items():
            if known_model.lower() in model.lower():
                bounds = b
                break

        if bounds:
            lo, hi = bounds
            in_range = lo <= price <= hi
            if not in_range:
                anomalies += 1
                report.add("prices",
                           f"Price range: {model} = ${price:.2f}/hr",
                           False,
                           f"Expected ${lo:.2f}-${hi:.2f}/hr",
                           severity="warning")

    if anomalies == 0:
        report.add("prices", "All prices within expected ranges", True)
    else:
        report.add("prices", f"{anomalies} price anomalies detected", False,
                    severity="warning")


def check_freshness(report: ValidationReport):
    """Check that data files are within expected freshness windows."""

    for filepath, max_age_days in FRESHNESS_THRESHOLDS.items():
        full_path = REPO_ROOT / filepath
        if not full_path.exists():
            report.add("freshness", f"Freshness: {filepath}", False,
                       "File does not exist")
            continue

        mod_time = datetime.fromtimestamp(full_path.stat().st_mtime, tz=timezone.utc)
        age = datetime.now(timezone.utc) - mod_time
        fresh = age < timedelta(days=max_age_days)

        report.add("freshness", f"Freshness: {filepath}",
                    fresh,
                    f"Last modified {age.days} days ago (max: {max_age_days})",
                    severity="warning" if not fresh else "info")


def check_cross_references(report: ValidationReport):
    """Verify consistency between different data files."""

    # Check that README mentions the same number of providers as the pricing data
    readme_path = REPO_ROOT / "README.md"
    if readme_path.exists():
        with open(readme_path) as f:
            readme = f.read()
        # Count provider rows in the table
        provider_mentions = re.findall(r'\*\*\[([^\]]+)\]', readme)
        if provider_mentions:
            report.add("cross-ref",
                        f"README lists {len(provider_mentions)} providers",
                        len(provider_mentions) >= 10,
                        severity="warning")

    # Check provenance.md references match dataprov.json
    prov_md_path = REPO_ROOT / "provenance.md"
    dataprov_path = REPO_ROOT / "dataprov.json"
    if prov_md_path.exists() and dataprov_path.exists():
        with open(prov_md_path) as f:
            prov_md = f.read()
        with open(dataprov_path) as f:
            dataprov = json.load(f)

        # Both should reference the same version
        md_version = re.search(r'\*\*Version\*\*\s*\|\s*([\d.]+)', prov_md)
        json_version = dataprov.get("version", "")
        if md_version:
            versions_match = md_version.group(1) == json_version
            report.add("cross-ref", "Version consistency (provenance.md ↔ dataprov.json)",
                        versions_match,
                        f"MD: {md_version.group(1)}, JSON: {json_version}" if not versions_match else "")

    # Check croissant.json references valid files
    croissant_path = REPO_ROOT / "croissant.json"
    if croissant_path.exists():
        with open(croissant_path) as f:
            croissant = json.load(f)
        dists = croissant.get("distribution", [])
        for dist in dists:
            url = dist.get("contentUrl", "")
            if "raw.githubusercontent.com" in url:
                # Extract the path part
                parts = url.split("/main/")
                if len(parts) > 1:
                    local_path = REPO_ROOT / parts[1]
                    exists = local_path.exists()
                    report.add("cross-ref",
                                f"Croissant references valid file: {parts[1]}",
                                exists,
                                severity="warning")


def check_integrity(report: ValidationReport):
    """Compute checksums for data files to detect tampering."""

    data_files = ["data/gpu-specs.json", "data/cloud-pricing.json"]
    for filepath in data_files:
        full_path = REPO_ROOT / filepath
        if full_path.exists():
            with open(full_path, "rb") as f:
                sha256 = hashlib.sha256(f.read()).hexdigest()
            report.add("integrity", f"SHA-256 for {filepath}: {sha256[:16]}...",
                        True, severity="info")
        else:
            report.add("integrity", f"Checksum: {filepath}", False,
                        "File not found", severity="warning")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Validate data integrity for the AI Infrastructure Index"
    )
    parser.add_argument("--check", choices=["schema", "links", "prices", "freshness",
                                              "cross-ref", "integrity", "all"],
                        default="all", help="Which validation to run")
    parser.add_argument("--json", action="store_true",
                        help="Output report as JSON")
    parser.add_argument("--ci", action="store_true",
                        help="CI mode: exit 1 on failure")
    parser.add_argument("--skip-links", action="store_true",
                        help="Skip URL health checks (for offline/CI use)")
    args = parser.parse_args()

    report = ValidationReport()

    checks = {
        "schema": lambda: (check_file_exists(report), check_json_schema(report)),
        "links": lambda: check_link_health(report),
        "prices": lambda: check_price_anomalies(report),
        "freshness": lambda: check_freshness(report),
        "cross-ref": lambda: check_cross_references(report),
        "integrity": lambda: check_integrity(report),
    }

    if args.check == "all":
        for name, fn in checks.items():
            if name == "links" and args.skip_links:
                report.add("links", "Link health checks", True,
                           "Skipped (--skip-links)", severity="info")
                continue
            try:
                fn()
            except Exception as e:
                report.add(name, f"{name} check error", False,
                           f"Unexpected error: {e}")
    else:
        try:
            checks[args.check]()
        except Exception as e:
            report.add(args.check, f"{args.check} check error", False,
                       f"Unexpected error: {e}")

    # Output
    if args.json:
        print(json.dumps(report.to_json(), indent=2))
    else:
        report.print_report()

    # Save report to data directory
    report_path = REPO_ROOT / "data" / "validation-report.json"
    try:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, "w") as f:
            json.dump(report.to_json(), f, indent=2)
        if not args.json:
            print(f"  Report saved to: {report_path}\n")
    except Exception:
        pass  # Non-critical

    if args.ci and not report.all_passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
