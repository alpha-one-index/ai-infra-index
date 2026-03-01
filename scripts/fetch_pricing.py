#!/usr/bin/env python3
"""
fetch_pricing.py - Automated GPU cloud pricing fetcher
Runs hourly via GitHub Actions to update data/cloud-pricing.json

Sources:
- Azure Retail Prices API (public, no auth required)
- Lambda Labs API (public instance-types endpoint)

Note: AWS and GCP bulk pricing APIs require large downloads or auth.
We fetch from Azure and Lambda directly, and maintain manual data for
AWS/GCP/CoreWeave/Together AI from their published pricing pages.
"""

import json
import sys
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# Config
DATA_DIR = Path(__file__).parent.parent / "data"
PRICING_FILE = DATA_DIR / "cloud-pricing.json"

# Azure VM SKUs to query - maps SKU name to GPU info
AZURE_SKUS = {
    "Standard_ND96isr_H100_v5": {
        "gpu_model": "NVIDIA H100 SXM",
        "gpu_count": 8,
        "gpu_memory_gb": 640,
    },
    "Standard_ND96amsr_A100_v4": {
        "gpu_model": "NVIDIA A100 80GB",
        "gpu_count": 8,
        "gpu_memory_gb": 640,
    },
    "Standard_ND96asr_v4": {
        "gpu_model": "NVIDIA A100 40GB",
        "gpu_count": 8,
        "gpu_memory_gb": 320,
    },
}


def fetch_url(url, timeout=30):
    """Fetch URL content with error handling."""
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "ai-infra-index/1.0"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"  WARNING: Failed to fetch {url}: {e}")
        return None


def fetch_azure_pricing():
    """Fetch GPU VM pricing from Azure Retail Prices API."""
    print("Fetching Azure pricing...")
    results = []

    for sku_name, gpu_info in AZURE_SKUS.items():
        # Build filter with proper URL encoding
        odata_filter = (
            f"serviceName eq 'Virtual Machines' "
            f"and armSkuName eq '{sku_name}' "
            f"and armRegionName eq 'eastus' "
            f"and priceType eq 'Consumption'"
        )
        params = urllib.parse.urlencode({
            "api-version": "2023-01-01-preview",
            "$filter": odata_filter,
        })
        url = f"https://prices.azure.com/api/retail/prices?{params}"
        data = fetch_url(url)

        if data and data.get("Items"):
            for item in data["Items"]:
                if item.get("type") == "Consumption" and "Spot" not in item.get("skuName", "") and "Low" not in item.get("skuName", ""):
                    results.append({
                        "provider": "azure",
                        "instance_type": sku_name,
                        "gpu_model": gpu_info["gpu_model"],
                        "gpu_count": gpu_info["gpu_count"],
                        "gpu_memory_gb": gpu_info["gpu_memory_gb"],
                        "price_per_hour_usd": item["retailPrice"],
                        "region": item.get("armRegionName", "eastus"),
                        "currency": item.get("currencyCode", "USD"),
                        "meter": item.get("meterName", ""),
                        "source_url": "https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/",
                    })
                    break  # Take first matching non-spot price

    print(f"  Azure: {len(results)} instances fetched")
    return results


def fetch_lambda_pricing():
    """Fetch GPU instance pricing from Lambda Labs API."""
    print("Fetching Lambda Labs pricing...")
    results = []

    url = "https://cloud.lambdalabs.com/api/v1/instance-types"
    data = fetch_url(url)

    if data and isinstance(data, dict) and "data" in data:
        for instance_id, info in data["data"].items():
            specs = info.get("instance_type", {})
            price = specs.get("price_cents_per_hour")
            if price is not None:
                gpu_desc = specs.get("description", instance_id)
                gpu_count = specs.get("specs", {}).get("gpus", 0)
                results.append({
                    "provider": "lambda",
                    "instance_type": instance_id,
                    "gpu_model": gpu_desc,
                    "gpu_count": gpu_count,
                    "price_per_hour_usd": round(price / 100, 2),
                    "region": "us-east-1",
                    "currency": "USD",
                    "source_url": "https://lambdalabs.com/service/gpu-cloud#pricing",
                })
    elif data and isinstance(data, dict):
        # Try alternate response format
        for key, val in data.items():
            if isinstance(val, dict) and "price_cents_per_hour" in val:
                results.append({
                    "provider": "lambda",
                    "instance_type": key,
                    "gpu_model": val.get("description", key),
                    "gpu_count": val.get("specs", {}).get("gpus", 0),
                    "price_per_hour_usd": round(val["price_cents_per_hour"] / 100, 2),
                    "region": "us-east-1",
                    "currency": "USD",
                    "source_url": "https://lambdalabs.com/service/gpu-cloud#pricing",
                })

    print(f"  Lambda: {len(results)} instances fetched")
    return results


def main():
    now = datetime.now(timezone.utc).isoformat()
    print(f"Starting pricing fetch at {now}")
    print(f"Data directory: {DATA_DIR}")
    print(f"Pricing file: {PRICING_FILE}")

    # Load existing pricing data
    if PRICING_FILE.exists():
        with open(PRICING_FILE) as f:
            pricing_data = json.load(f)
    else:
        pricing_data = {
            "metadata": {"description": "Live GPU cloud pricing data"},
            "providers": {},
        }

    # Fetch from all sources
    azure_instances = fetch_azure_pricing()
    lambda_instances = fetch_lambda_pricing()

    total_fetched = len(azure_instances) + len(lambda_instances)
    print(f"\nFetched {total_fetched} live instance pricing records")

    providers_updated = []

    # Update Azure
    if azure_instances:
        pricing_data["providers"]["azure"] = {
            "name": "Microsoft Azure",
            "last_api_fetch": now,
            "fetch_method": "azure_retail_prices_api",
            "instances": azure_instances,
        }
        providers_updated.append("azure")

    # Update Lambda
    if lambda_instances:
        pricing_data["providers"]["lambda"] = {
            "name": "Lambda Labs",
            "last_api_fetch": now,
            "fetch_method": "lambda_api_v1",
            "instances": lambda_instances,
        }
        providers_updated.append("lambda")

    # Update metadata
    pricing_data["metadata"]["last_updated"] = now
    pricing_data["metadata"]["update_frequency"] = "hourly"
    pricing_data["metadata"]["sources_fetched"] = total_fetched
    pricing_data["metadata"]["providers_with_live_data"] = providers_updated

    print(f"Providers updated: {providers_updated}")

    # Write updated data
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(PRICING_FILE, "w") as f:
        json.dump(pricing_data, f, indent=2)
    print(f"Updated {PRICING_FILE}")

    print(f"\nDone in {datetime.now(timezone.utc).isoformat()}")


if __name__ == "__main__":
    main()
