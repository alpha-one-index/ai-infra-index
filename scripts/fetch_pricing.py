#!/usr/bin/env python3
"""fetch_pricing.py - Multi-provider GPU cloud pricing aggregator.

Fetches live pricing from Azure Retail Prices API, Vast.ai marketplace API,
RunPod GraphQL API, and Lambda Labs Cloud API. Combines with curated pricing
data from 8 additional providers including CoreWeave, Together AI, Vultr,
Nebius, OCI, Cudo Compute, Fluidstack, and Paperspace.

Outputs data/cloud-pricing.json with historical tracking.

Part of the AI Infrastructure Index
(https://alpha-one-index.github.io/ai-infra-index/)
"""
import json
import os
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timezone

# --- Configuration ---
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "cloud-pricing.json")
HISTORY_DIR = os.path.join(DATA_DIR, "history")
AZURE_API = "https://prices.azure.com/api/retail/prices"
VASTAI_API = "https://console.vast.ai/api/v0/search/asks/"
RUNPOD_API = "https://api.runpod.io/graphql"
LAMBDA_API = "https://cloud.lambda.ai/api/v1/instance-types"

# Optional API keys from environment (RunPod and Lambda require free keys)
RUNPOD_API_KEY = os.environ.get("RUNPOD_API_KEY", "")
LAMBDA_API_KEY = os.environ.get("LAMBDA_API_KEY", "")

# Pricing source URLs for transparency
PRICING_SOURCES = {
    "Azure": "https://prices.azure.com/api/retail/prices",
    "RunPod": "https://api.runpod.io/graphql",
    "Lambda": "https://cloud.lambda.ai/api/v1/instance-types",
    "Vast.ai": "https://console.vast.ai/api/v0/search/asks/",
    "CoreWeave": "https://www.coreweave.com/pricing",
    "Together AI": "https://www.together.ai/pricing",
    "Vultr": "https://www.vultr.com/pricing/#cloud-gpu",
    "Nebius": "https://nebius.com/pricing",
    "OCI": "https://www.oracle.com/cloud/price-list/",
    "Cudo Compute": "https://www.cudocompute.com/pricing",
    "Fluidstack": "https://www.fluidstack.io/pricing",
    "Paperspace": "https://www.paperspace.com/pricing",
}

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

# GPU name normalization for Vast.ai marketplace
VASTAI_GPU_NORMALIZE = {
    "RTX 4090": "RTX 4090",
    "RTX 3090": "RTX 3090",
    "A100_SXM4": "A100 SXM",
    "A100_PCIE": "A100 PCIe",
    "A100 SXM": "A100 SXM",
    "A100 80GB": "A100 SXM",
    "H100_SXM5": "H100 SXM",
    "H100 SXM": "H100 SXM",
    "H100_PCIE": "H100 PCIe",
    "H100 80GB": "H100 SXM",
    "H200": "H200",
    "L40S": "L40S",
    "L40": "L40",
    "RTX A6000": "RTX A6000",
    "RTX A5000": "RTX A5000",
    "RTX A4000": "RTX A4000",
}

# GPU VRAM lookup (GB)
GPU_VRAM = {
    "H100 SXM": 80, "H100 PCIe": 80, "H200": 141, "B200": 192,
    "A100 SXM": 80, "A100 PCIe": 40, "A100 SXM 40GB": 40,
    "A10": 24, "A16": 64, "L40S": 48, "L40": 48,
    "RTX 4090": 24, "RTX 3090": 24, "RTX A6000": 48,
    "RTX A5000": 24, "RTX A4000": 16, "MI300X": 192, "MI325X": 256,
    "H200 SXM": 141,
}

# --- Curated pricing: CoreWeave (last verified Feb 2026) ---
# Source: https://www.coreweave.com/pricing
COREWEAVE_PRICING = [
    {"gpu": "H100 SXM", "mem": 80, "on_demand": 2.23},
    {"gpu": "H200", "mem": 141, "on_demand": 3.35},
    {"gpu": "A100 SXM", "mem": 80, "on_demand": 1.21},
    {"gpu": "A100 PCIe", "mem": 40, "on_demand": 0.76},
    {"gpu": "L40S", "mem": 48, "on_demand": 0.74},
    {"gpu": "RTX A6000", "mem": 48, "on_demand": 0.62},
    {"gpu": "RTX A5000", "mem": 24, "on_demand": 0.34},
]

# --- Curated pricing: Together AI Dedicated (last verified Feb 2026) ---
# Source: https://www.together.ai/pricing
TOGETHER_PRICING = [
    {"gpu": "H100 SXM", "mem": 80, "on_demand": 2.50},
    {"gpu": "H200", "mem": 141, "on_demand": 3.30},
    {"gpu": "A100 SXM", "mem": 80, "on_demand": 1.25},
]

# --- Curated pricing: Vultr (last verified Feb 2026) ---
# Source: https://www.vultr.com/pricing/#cloud-gpu
VULTR_PRICING = [
    {"gpu": "H100 SXM", "mem": 80, "on_demand": 2.99},
    {"gpu": "B200", "mem": 192, "on_demand": 2.99},
    {"gpu": "A100 SXM", "mem": 80, "on_demand": 2.60},
    {"gpu": "A100 PCIe", "mem": 40, "on_demand": 1.29},
    {"gpu": "L40S", "mem": 48, "on_demand": 1.67},
    {"gpu": "MI300X", "mem": 192, "on_demand": 1.85},
    {"gpu": "MI325X", "mem": 256, "on_demand": 2.00},
    {"gpu": "A16", "mem": 64, "on_demand": 0.51},
]

# --- Curated pricing: Nebius (last verified Feb 2026) ---
# Source: https://nebius.com/pricing
NEBIUS_PRICING = [
    {"gpu": "H100 SXM", "mem": 80, "on_demand": 2.00},
    {"gpu": "H200 SXM", "mem": 141, "on_demand": 2.30},
]

# --- Curated pricing: Oracle Cloud Infrastructure (last verified Feb 2026) ---
# Source: https://www.oracle.com/cloud/price-list/
OCI_PRICING = [
    {"gpu": "H100 SXM", "mem": 80, "on_demand": 4.10},
    {"gpu": "A100 SXM", "mem": 80, "on_demand": 2.95},
    {"gpu": "A100 SXM 40GB", "mem": 40, "on_demand": 2.95},
    {"gpu": "L40S", "mem": 48, "on_demand": 2.39},
    {"gpu": "A10", "mem": 24, "on_demand": 1.50},
]

# --- Curated pricing: Cudo Compute (last verified Feb 2026) ---
# Source: https://www.cudocompute.com/pricing
CUDO_PRICING = [
    {"gpu": "H100 SXM", "mem": 80, "on_demand": 2.50},
    {"gpu": "A100 SXM", "mem": 80, "on_demand": 1.20},
    {"gpu": "RTX 4090", "mem": 24, "on_demand": 0.35},
]

# --- Curated pricing: Fluidstack (last verified Feb 2026) ---
# Source: https://www.fluidstack.io/pricing
FLUIDSTACK_PRICING = [
    {"gpu": "H100 SXM", "mem": 80, "on_demand": 2.21},
    {"gpu": "A100 SXM", "mem": 80, "on_demand": 1.15},
    {"gpu": "A100 PCIe", "mem": 40, "on_demand": 0.80},
    {"gpu": "L40S", "mem": 48, "on_demand": 0.59},
]

# --- Curated pricing: Paperspace by DigitalOcean (last verified Feb 2026) ---
# Source: https://www.paperspace.com/pricing
PAPERSPACE_PRICING = [
    {"gpu": "H100 SXM", "mem": 80, "on_demand": 3.09},
    {"gpu": "A100 SXM", "mem": 80, "on_demand": 1.89},
    {"gpu": "RTX A4000", "mem": 16, "on_demand": 0.56},
]


def fetch_url(url, timeout=30, headers=None):
    """Fetch URL and return parsed JSON, or None on error."""
    try:
        hdrs = {"User-Agent": "ai-infra-index/2.0"}
        if headers:
            hdrs.update(headers)
        req = urllib.request.Request(url, headers=hdrs)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"    WARN: {e}")
        return None


def post_json(url, payload, timeout=30, headers=None):
    """POST JSON payload and return parsed response, or None on error."""
    try:
        hdrs = {
            "User-Agent": "ai-infra-index/2.0",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if headers:
            hdrs.update(headers)
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=hdrs, method="PUT")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"    WARN: {e}")
        return None


def post_graphql(url, query, timeout=30, headers=None):
    """POST a GraphQL query and return parsed response, or None on error."""
    try:
        hdrs = {
            "User-Agent": "ai-infra-index/2.0",
            "Content-Type": "application/json",
        }
        if headers:
            hdrs.update(headers)
        data = json.dumps({"query": query}).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=hdrs)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"    WARN: {e}")
        return None


def fetch_azure():
    """Fetch GPU VM pricing from Azure Retail Prices API (LIVE)."""
    print("[LIVE] Fetching Azure pricing...")
    skus = list(AZURE_GPU_MAP.keys())
    filters = " or ".join(f"armSkuName eq '{s}'" for s in skus)
    query = f"$filter=serviceName eq 'Virtual Machines' and priceType eq 'Consumption' and ({filters})"
    url = f"{AZURE_API}?" + urllib.parse.quote(query, safe="=&$'()")
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
    print(f"    Azure: {len(out)} SKUs (from {len(results)} regional prices)")
    return out


def fetch_vastai():
    """Fetch GPU pricing from Vast.ai marketplace API (LIVE).

    Vast.ai is a marketplace where hosts set their own prices,
    so prices fluctuate in real-time based on supply and demand.
    We compute median on-demand and spot prices per GPU type.
    """
    print("[LIVE] Fetching Vast.ai marketplace pricing...")
    payload = {
        "q": {
            "verified": {"eq": True},
            "rentable": {"eq": True},
            "num_gpus": {"eq": 1},
            "type": "on-demand",
        },
        "sort": [["dph_total", "asc"]],
        "limit": 500,
    }
    data = post_json(VASTAI_API, payload)
    if not data or "offers" not in data:
        print("    Vast.ai: API returned no offers, using fallback")
        return None

    # Group prices by normalized GPU name
    gpu_prices = {}  # gpu_name -> [price, ...]
    for offer in data["offers"]:
        gpu_name_raw = offer.get("gpu_name", "")
        # Try to normalize
        normalized = None
        for key, val in VASTAI_GPU_NORMALIZE.items():
            if key.lower() in gpu_name_raw.lower():
                normalized = val
                break
        if not normalized:
            continue
        price = offer.get("dph_total", 0)
        if price <= 0 or price > 50:  # sanity check
            continue
        if normalized not in gpu_prices:
            gpu_prices[normalized] = []
        gpu_prices[normalized].append(price)

    # Compute median price per GPU
    results = []
    for gpu_name, prices in sorted(gpu_prices.items()):
        prices.sort()
        mid = len(prices) // 2
        median = prices[mid] if len(prices) % 2 else (prices[mid - 1] + prices[mid]) / 2
        mem = GPU_VRAM.get(gpu_name, 0)
        item = {
            "gpu": gpu_name,
            "cnt": 1,
            "mem": mem,
            "on_demand": round(median, 2),
            "offers_sampled": len(prices),
            "price_min": round(prices[0], 2),
            "price_max": round(prices[-1], 2),
        }
        results.append(item)

    print(f"    Vast.ai: {len(results)} GPU types (from {len(data['offers'])} marketplace offers)")
    return results if results else None


def fetch_runpod():
    """Fetch GPU pricing from RunPod GraphQL API (LIVE).

    Queries community and secure cloud pricing with spot rates.
    Requires RUNPOD_API_KEY environment variable.
    """
    if not RUNPOD_API_KEY:
        print("[LIVE] RunPod: No API key set (RUNPOD_API_KEY), skipping live fetch")
        return None

    print("[LIVE] Fetching RunPod pricing...")
    query = """
    query {
        gpuTypes {
            id
            displayName
            memoryInGb
            secureCloud
            communityCloud
            securePrice
            communityPrice
            secureSpotPrice
            communitySpotPrice
            lowestPrice(input: {gpuCount: 1}) {
                minimumBidPrice
                uninterruptablePrice
            }
        }
    }
    """
    url = f"{RUNPOD_API}?api_key={RUNPOD_API_KEY}"
    data = post_graphql(url, query)
    if not data or "data" not in data or "gpuTypes" not in data["data"]:
        print("    RunPod: API returned no data, skipping")
        return None

    results = []
    for gpu in data["data"]["gpuTypes"]:
        name = gpu.get("displayName", "")
        mem = gpu.get("memoryInGb", 0)
        # Use community price (cheaper) or secure price
        community = gpu.get("communityPrice")
        secure = gpu.get("securePrice")
        spot_community = gpu.get("communitySpotPrice")
        lowest = gpu.get("lowestPrice", {})
        on_demand = community or secure
        if not on_demand or on_demand <= 0:
            continue
        item = {
            "gpu": name,
            "cnt": 1,
            "mem": mem,
            "on_demand": round(on_demand, 2),
        }
        if secure and secure > 0:
            item["secure_price"] = round(secure, 2)
        if spot_community and spot_community > 0:
            item["spot"] = round(spot_community, 2)
        if lowest and lowest.get("minimumBidPrice"):
            item["min_bid"] = round(lowest["minimumBidPrice"], 2)
        results.append(item)

    print(f"    RunPod: {len(results)} GPU types")
    return results if results else None


def fetch_lambda():
    """Fetch GPU instance pricing from Lambda Labs Cloud API (LIVE).

    Returns available instance types with current pricing.
    Requires LAMBDA_API_KEY environment variable.
    """
    if not LAMBDA_API_KEY:
        print("[LIVE] Lambda: No API key set (LAMBDA_API_KEY), skipping live fetch")
        return None

    print("[LIVE] Fetching Lambda Labs pricing...")
    data = fetch_url(LAMBDA_API, headers={"Authorization": f"Bearer {LAMBDA_API_KEY}"})
    if not data or "data" not in data:
        print("    Lambda: API returned no data, skipping")
        return None

    results = []
    for instance_type, info in data["data"].items():
        specs = info.get("instance_type", {})
        price = specs.get("price_cents_per_hour", 0)
        if price <= 0:
            continue
        price_hr = price / 100.0
        gpu_desc = specs.get("description", instance_type)
        gpu_count = specs.get("specs", {}).get("gpus", 1)
        gpu_name = specs.get("gpu_description", gpu_desc)
        mem_gb = specs.get("specs", {}).get("memory_gib", 0)
        # Extract per-GPU price
        per_gpu = round(price_hr / max(gpu_count, 1), 2)
        item = {
            "gpu": gpu_name,
            "cnt": gpu_count,
            "mem": mem_gb,
            "on_demand": round(price_hr, 2),
            "per_gpu": per_gpu,
            "instance_type": instance_type,
        }
        results.append(item)

    print(f"    Lambda: {len(results)} instance types")
    return results if results else None


def build_manual_providers():
    """Build provider entries from curated pricing data."""
    providers = {}
    sources = {
        "CoreWeave": COREWEAVE_PRICING,
        "Together AI": TOGETHER_PRICING,
        "Vultr": VULTR_PRICING,
        "Nebius": NEBIUS_PRICING,
        "OCI": OCI_PRICING,
        "Cudo Compute": CUDO_PRICING,
        "Fluidstack": FLUIDSTACK_PRICING,
        "Paperspace": PAPERSPACE_PRICING,
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
        print(f"    {name}: {len(items)} SKUs")
    return providers


def main():
    """Main entry point: fetch all pricing and write JSON."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"AI Infra Index - Pricing Update ({ts})")
    print("=" * 50)

    # Ensure directories exist
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(HISTORY_DIR, exist_ok=True)

    # Track which providers are live vs curated
    live_providers = []
    curated_providers = []

    # --- Live API providers ---
    providers = {}

    # 1. Azure (live, no key needed)
    azure_skus = fetch_azure()
    if azure_skus:
        providers["Azure"] = azure_skus
        live_providers.append("Azure")

    # 2. Vast.ai (live, no key needed)
    vastai_skus = fetch_vastai()
    if vastai_skus:
        providers["Vast.ai"] = vastai_skus
        live_providers.append("Vast.ai")

    # 3. RunPod (live, requires free API key)
    runpod_skus = fetch_runpod()
    if runpod_skus:
        providers["RunPod"] = runpod_skus
        live_providers.append("RunPod")

    # 4. Lambda Labs (live, requires free API key)
    lambda_skus = fetch_lambda()
    if lambda_skus:
        providers["Lambda"] = lambda_skus
        live_providers.append("Lambda")

    # --- Curated providers ---
    print("Loading curated provider pricing...")
    manual = build_manual_providers()
    for name, items in manual.items():
        providers[name] = items
        curated_providers.append(name)

    # Build output
    output = {
        "metadata": {
            "updated": ts,
            "source": "AI Infrastructure Index",
            "url": "https://alpha-one-index.github.io/ai-infra-index/",
            "providers_count": len(providers),
            "total_skus": sum(len(v) for v in providers.values()),
            "live_providers": live_providers,
            "curated_providers": curated_providers,
            "methodology": f"{len(live_providers)} providers via live API; {len(curated_providers)} curated monthly from official pricing pages",
            "last_curated": "2026-02",
            "pricing_sources": PRICING_SOURCES,
        },
        "providers": providers,
    }

    # Write main output
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nWrote {OUTPUT_FILE}")
    print(f"  {output['metadata']['providers_count']} providers, {output['metadata']['total_skus']} total SKUs")
    print(f"  Live API: {', '.join(live_providers) if live_providers else 'none'}")
    print(f"  Curated:  {', '.join(curated_providers)}")

    # Archive historical snapshot
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    hist_file = os.path.join(HISTORY_DIR, f"pricing-{date_str}.json")
    with open(hist_file, "w") as f:
        json.dump(output, f, indent=2)
    print(f"  Archived to {hist_file}")


if __name__ == "__main__":
    main()
