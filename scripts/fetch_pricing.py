#!/usr/bin/env python3
"""fetch_pricing.py - Multi-provider GPU cloud pricing aggregator.

Fetches live pricing from Azure Retail Prices API and combines with
curated pricing data from RunPod, Lambda, CoreWeave, Together AI,
and Vast.ai. Outputs data/cloud-pricing.json with historical tracking.

Part of the AI Infrastructure Index (https://alpha-one-index.github.io/ai-infra-index/)
"""

import json
import os
import urllib.request
import urllib.error
from datetime import datetime, timezone

# --- Configuration ---
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "cloud-pricing.json")
HISTORY_DIR = os.path.join(DATA_DIR, "history")
AZURE_API = "https://prices.azure.com/api/retail/prices"

# Azure VM SKU -> GPU mapping
AZURE_GPU_MAP = {
    "Standard_NC40ads_H100_v5": {"gpu": "H100 SXM", "cnt": 1, "mem": 80},
    "Standard_NC80adis_H100_v5": {"gpu": "H100 SXM", "cnt": 2, "mem": 160},
    "Standard_ND96isr_H100_v5": {"gpu": "H100 SXM", "cnt": 8, "mem": 640},
    "Standard_ND96is_H200_v5": {"gpu": "H200", "cnt": 8, "mem": 1128},
    "Standard_NC24ads_A100_v4": {"gpu": "A100 SXM", "cnt": 1, "mem": 80},
    "Standard_NC48ads_A100_v4": {"gpu": "A100 SXM", "cnt": 2, "mem": 160},
    "Standard_NC96ads_A100_v4": {"gpu": "A100 SXM", "cnt": 4, "mem": 320},
    "Standard_ND96asr_v4": {"gpu": "A100 SXM", "cnt": 8, "mem": 640},
    "Standard_NV36ads_A10_v5": {"gpu": "A10", "cnt": 1, "mem": 24},
    "Standard_NV72ads_A10_v5": {"gpu": "A10", "cnt": 2, "mem": 48},
}

# --- Curated pricing: RunPod (Feb 2026) ---
RUNPOD_PRICING = [
    {"gpu": "H100 SXM", "mem": 80, "on_demand": 2.49, "spot": 1.89},
    {"gpu": "H200", "mem": 141, "on_demand": 3.59, "spot": None},
    {"gpu": "B200", "mem": 192, "on_demand": 5.98, "spot": None},
    {"gpu": "A100 SXM", "mem": 80, "on_demand": 1.39, "spot": 0.79},
    {"gpu": "A100 PCIe", "mem": 40, "on_demand": 1.19, "spot": 0.60},
    {"gpu": "L40S", "mem": 48, "on_demand": 0.79, "spot": 0.40},
    {"gpu": "L40", "mem": 48, "on_demand": 0.69, "spot": None},
    {"gpu": "RTX 4090", "mem": 24, "on_demand": 0.34, "spot": 0.20},
    {"gpu": "RTX A6000", "mem": 48, "on_demand": 0.33, "spot": 0.25},
    {"gpu": "RTX 3090", "mem": 24, "on_demand": 0.22, "spot": 0.11},
]

# --- Curated pricing: Lambda Labs (Feb 2026) ---
LAMBDA_PRICING = [
    {"gpu": "H100 SXM", "cnt": 8, "mem": 640, "on_demand": 23.84},
    {"gpu": "H100 SXM", "cnt": 1, "mem": 80, "on_demand": 2.98},
    {"gpu": "H200", "cnt": 8, "mem": 1128, "on_demand": 27.92},
    {"gpu": "A100 SXM", "cnt": 8, "mem": 640, "on_demand": 10.80},
    {"gpu": "A100 SXM", "cnt": 1, "mem": 80, "on_demand": 1.35},
    {"gpu": "A10", "cnt": 1, "mem": 24, "on_demand": 0.60},
]

# --- Curated pricing: CoreWeave (Feb 2026) ---
COREWEAVE_PRICING = [
    {"gpu": "H100 SXM", "mem": 80, "on_demand": 2.23},
    {"gpu": "H200", "mem": 141, "on_demand": 3.35},
    {"gpu": "A100 SXM", "mem": 80, "on_demand": 1.21},
    {"gpu": "A100 PCIe", "mem": 40, "on_demand": 0.76},
    {"gpu": "L40S", "mem": 48, "on_demand": 0.74},
    {"gpu": "RTX A6000", "mem": 48, "on_demand": 0.62},
    {"gpu": "RTX A5000", "mem": 24, "on_demand": 0.34},
]

# --- Curated pricing: Together AI Dedicated (Feb 2026) ---
TOGETHER_PRICING = [
    {"gpu": "H100 SXM", "mem": 80, "on_demand": 2.50},
    {"gpu": "H200", "mem": 141, "on_demand": 3.30},
    {"gpu": "A100 SXM", "mem": 80, "on_demand": 1.25},
]

# --- Curated pricing: Vast.ai market median (Feb 2026) ---
VASTAI_PRICING = [
    {"gpu": "H100 SXM", "mem": 80, "on_demand": 2.45, "spot": 1.80},
    {"gpu": "A100 SXM", "mem": 80, "on_demand": 1.15, "spot": 0.70},
    {"gpu": "A100 PCIe", "mem": 40, "on_demand": 0.85, "spot": 0.50},
    {"gpu": "L40S", "mem": 48, "on_demand": 0.65, "spot": 0.35},
    {"gpu": "RTX 4090", "mem": 24, "on_demand": 0.28, "spot": 0.16},
    {"gpu": "RTX 3090", "mem": 24, "on_demand": 0.15, "spot": 0.08},
]


def fetch_url(url, timeout=30):
    """Fetch URL and return parsed JSON, or None on error."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ai-infra-index/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"  WARN: {e}")
        return None


def fetch_azure():
    """Fetch GPU VM pricing from Azure Retail Prices API."""
    print("Fetching Azure pricing...")
    skus = list(AZURE_GPU_MAP.keys())
    filters = " or ".join(f"armSkuName eq '{s}'" for s in skus)
    query = f"$filter=serviceName eq 'Virtual Machines' and priceType eq 'Consumption' and ({filters})"
    url = f"{AZURE_API}?{query}"
    results = []
    page = 0
    while url:
        page += 1
        data = fetch_url(url)
        if not data:
            break
        for item in data.get("Items", []):
            sku = item.get("armSkuName", "")
            if sku not in AZURE_GPU_MAP:
                continue
            if "Spot" in item.get("skuName", "") or "spot" in item.get("meterName", "").lower():
                continue
            info = AZURE_GPU_MAP[sku]
            region = item.get("armRegionName", "unknown")
            price_hr = item.get("unitPrice", 0)
            if price_hr <= 0:
                continue
            results.append({
                "gpu": info["gpu"],
                "cnt": info.get("cnt", 1),
                "mem": info["mem"],
                "on_demand": round(price_hr, 2),
                "region": region,
                "sku": sku,
            })
        url = data.get("NextPageLink")
    # Deduplicate: keep cheapest per GPU+cnt combo
    best = {}
    for r in results:
        key = (r["gpu"], r["cnt"])
        if key not in best or r["on_demand"] < best[key]["on_demand"]:
            best[key] = r
    out = list(best.values())
    print(f"  Azure: {len(out)} SKUs (from {len(results)} regional prices)")
    return out


def build_manual_providers():
    """Build provider entries from curated pricing data."""
    providers = {}
    sources = {
        "RunPod": RUNPOD_PRICING,
        "Lambda": LAMBDA_PRICING,
        "CoreWeave": COREWEAVE_PRICING,
        "Together AI": TOGETHER_PRICING,
        "Vast.ai": VASTAI_PRICING,
    }
    for name, entries in sources.items():
        items = []
        for e in entries:
            item = {
                "gpu": e["gpu"],
                "cnt": e.get("cnt", 1),
                "mem": e["mem"],
                "on_demand": e["on_demand"],
            }
            if e.get("spot") is not None:
                item["spot"] = e["spot"]
            items.append(item)
        providers[name] = items
        print(f"  {name}: {len(items)} SKUs")
    return providers


def main():
    """Main entry point: fetch all pricing and write JSON."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"AI Infra Index - Pricing Update ({ts})")
    print("=" * 50)

    # Ensure directories exist
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(HISTORY_DIR, exist_ok=True)

    # Fetch Azure (live API)
    azure_skus = fetch_azure()

    # Build manual provider data
    print("Loading curated provider pricing...")
    providers = build_manual_providers()

    # Add Azure
    if azure_skus:
        providers["Azure"] = azure_skus

    # Build output
    output = {
        "metadata": {
            "updated": ts,
            "source": "AI Infrastructure Index",
            "url": "https://alpha-one-index.github.io/ai-infra-index/",
            "providers_count": len(providers),
            "total_skus": sum(len(v) for v in providers.values()),
            "methodology": "Azure via Retail Prices API; others curated monthly",
        },
        "providers": providers,
    }

    # Write main output
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nWrote {OUTPUT_FILE}")
    print(f"  {output['metadata']['providers_count']} providers, {output['metadata']['total_skus']} total SKUs")

    # Archive historical snapshot
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    hist_file = os.path.join(HISTORY_DIR, f"pricing-{date_str}.json")
    with open(hist_file, "w") as f:
        json.dump(output, f, indent=2)
    print(f"  Archived to {hist_file}")


if __name__ == "__main__":
    main()
