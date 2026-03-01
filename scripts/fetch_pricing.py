#!/usr/bin/env python3
"""
fetch_pricing.py - Automated GPU cloud pricing fetcher
Runs hourly via GitHub Actions to update data/cloud-pricing.json

Sources:
- Azure Retail Prices API (public, no auth required)
- Lambda Labs API (public instance-types endpoint)
"""

import json
import sys
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
PRICING_FILE = DATA_DIR / "cloud-pricing.json"

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
    """Fetch JSON from URL with error handling."""
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
                sku = item.get("skuName", "")
                if item.get("type") == "Consumption" and "Spot" not in sku and "Low" not in sku:
                    results.append({
                        "provider": "azure",
                        "instance_type": sku_name,
                        "gpu_model": gpu_info["gpu_model"],
                        "gpu_count": gpu_info["gpu_count"],
                        "gpu_memory_gb": gpu_info["gpu_memory_gb"],
                        "price_per_hour_usd": item["retailPrice"],
                        "region": item.get("armRegionName", "eastus"),
                        "currency": item.get("currencyCode", "USD"),
                        "source_url": "https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/",
                    })
                    break

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
                gpu_count = specs.get("specs", {}).get("gpus", 0)
                results.append({
                    "provider": "lambda",
                    "instance_type": instance_id,
                    "gpu_model": specs.get("description", instance_id),
                    "gpu_count": gpu_count,
                    "price_per_hour_usd": round(price / 100, 2),
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

    # Fetch from all sources
    azure_instances = fetch_azure_pricing()
    lambda_instances = fetch_lambda_pricing()

    total = len(azure_instances) + len(lambda_instances)
    print(f"\nFetched {total} live instance pricing records")

    providers_updated = []

    # Build fresh providers dict from fetched data
    providers = {}

    if azure_instances:
        providers["azure"] = {
            "name": "Microsoft Azure",
            "last_api_fetch": now,
            "fetch_method": "azure_retail_prices_api",
            "instances": azure_instances,
        }
        providers_updated.append("azure")

    if lambda_instances:
        providers["lambda"] = {
            "name": "Lambda Labs",
            "last_api_fetch": now,
            "fetch_method": "lambda_api_v1",
            "instances": lambda_instances,
        }
        providers_updated.append("lambda")

    # Build output structure (always fresh to avoid schema conflicts)
    pricing_data = {
        "metadata": {
            "description": "Live GPU cloud pricing - updated hourly via GitHub Actions",
            "last_updated": now,
            "update_frequency": "hourly",
            "sources_fetched": total,
            "providers_with_live_data": providers_updated,
            "repository": "https://github.com/alpha-one-index/ai-infra-index",
        },
        "providers": providers,
    }

    print(f"Providers updated: {providers_updated}")

    # Write updated data
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(PRICING_FILE, "w") as f:
        json.dump(pricing_data, f, indent=2)
    print(f"Updated {PRICING_FILE}")
    print(f"Done at {datetime.now(timezone.utc).isoformat()}")


if __name__ == "__main__":
    main()
