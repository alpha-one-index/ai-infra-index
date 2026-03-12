#!/usr/bin/env python3
"""generate_price_index.py - GPU Cloud Price Index Generator.

Computes a proprietary GPU Cloud Price Index (GCPI) from daily pricing
snapshots. Produces time-series data showing price trends per GPU model
across all tracked providers - a derived dataset no competitor offers.

The GCPI is analogous to a stock market index but for cloud GPU compute:
- Tracks median $/hr per GPU model across providers over time
- Computes index values normalized to base date (first snapshot = 100)
- Generates per-provider price competitiveness scores
- Identifies price movers (biggest drops/increases)

Outputs data/gpu-price-index.json with historical tracking.

Part of the AI Infrastructure Index
(https://alpha-one-index.github.io/ai-infra-index/)
"""
import json
import os
import glob
from datetime import datetime, timezone
from statistics import median, mean

# --- Configuration ---
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
HISTORY_DIR = os.path.join(DATA_DIR, "history")
OUTPUT_FILE = os.path.join(DATA_DIR, "gpu-price-index.json")

# GPU models to track in the index (high-demand AI/ML GPUs)
INDEX_GPUS = [
    "H100 SXM", "H100", "A100 SXM", "A100",
    "A10", "L40S", "L4", "RTX 4090", "RTX 3090",
    "A6000", "H200"
]


def load_snapshot(filepath):
    """Load a daily pricing snapshot and extract per-GPU prices."""
    with open(filepath, "r") as f:
        data = json.load(f)

    date_str = os.path.basename(filepath).replace("pricing-", "").replace(".json", "")
    gpu_prices = {}  # gpu_model -> [prices]
    provider_prices = {}  # provider -> gpu_model -> [prices]

    providers = data.get("providers", {})
    for provider, skus in providers.items():
        if not isinstance(skus, list):
            continue
        for sku in skus:
            gpu = sku.get("gpu", "")
            price = sku.get("on_demand")
            cnt = sku.get("cnt", 1)
            if not gpu or not price or price <= 0:
                continue
            # Normalize to per-GPU price
            per_gpu_price = price / cnt if cnt > 0 else price

            if gpu not in gpu_prices:
                gpu_prices[gpu] = []
            gpu_prices[gpu].append(per_gpu_price)

            if provider not in provider_prices:
                provider_prices[provider] = {}
            if gpu not in provider_prices[provider]:
                provider_prices[provider][gpu] = []
            provider_prices[provider][gpu].append(per_gpu_price)

    return {
        "date": date_str,
        "gpu_prices": gpu_prices,
        "provider_prices": provider_prices
    }


def compute_daily_index(snapshot, base_medians=None):
    """Compute index values for a single day."""
    daily = {
        "date": snapshot["date"],
        "gpu_medians": {},
        "gpu_mins": {},
        "gpu_maxs": {},
        "gpu_index": {},
        "provider_cheapest": {},
        "composite_index": None,
        "num_gpus_tracked": 0,
        "num_skus": 0
    }

    total_skus = 0
    index_values = []

    for gpu in INDEX_GPUS:
        prices = snapshot["gpu_prices"].get(gpu, [])
        if not prices:
            continue

        med = round(median(prices), 4)
        daily["gpu_medians"][gpu] = med
        daily["gpu_mins"][gpu] = round(min(prices), 4)
        daily["gpu_maxs"][gpu] = round(max(prices), 4)
        daily["num_gpus_tracked"] += 1
        total_skus += len(prices)

        # Compute index relative to base
        if base_medians and gpu in base_medians and base_medians[gpu] > 0:
            idx = round((med / base_medians[gpu]) * 100, 2)
            daily["gpu_index"][gpu] = idx
            index_values.append(idx)

        # Find cheapest provider for this GPU
        cheapest_provider = None
        cheapest_price = float("inf")
        for provider, gpu_map in snapshot["provider_prices"].items():
            if gpu in gpu_map:
                pmin = min(gpu_map[gpu])
                if pmin < cheapest_price:
                    cheapest_price = pmin
                    cheapest_provider = provider
        if cheapest_provider:
            daily["provider_cheapest"][gpu] = {
                "provider": cheapest_provider,
                "price": round(cheapest_price, 4)
            }

    daily["num_skus"] = total_skus
    if index_values:
        daily["composite_index"] = round(mean(index_values), 2)

    return daily


def compute_provider_scores(snapshots):
    """Compute provider competitiveness scores from latest snapshot."""
    if not snapshots:
        return {}

    latest = snapshots[-1]
    scores = {}

    for provider, gpu_map in latest["provider_prices"].items():
        wins = 0
        total = 0
        for gpu in INDEX_GPUS:
            all_prices = latest["gpu_prices"].get(gpu, [])
            provider_gpu_prices = gpu_map.get(gpu, [])
            if not all_prices or not provider_gpu_prices:
                continue
            total += 1
            provider_min = min(provider_gpu_prices)
            global_min = min(all_prices)
            # Win if within 10% of cheapest
            if global_min > 0 and provider_min <= global_min * 1.10:
                wins += 1

        if total > 0:
            scores[provider] = {
                "competitive_wins": wins,
                "gpus_offered": total,
                "competitiveness_pct": round((wins / total) * 100, 1)
            }

    return dict(sorted(scores.items(), key=lambda x: x[1]["competitiveness_pct"], reverse=True))


def compute_movers(daily_indices):
    """Identify biggest price movers between first and last snapshot."""
    if len(daily_indices) < 2:
        return {"biggest_drops": [], "biggest_increases": []}

    first = daily_indices[0]
    last = daily_indices[-1]
    changes = []

    for gpu in INDEX_GPUS:
        if gpu in first["gpu_medians"] and gpu in last["gpu_medians"]:
            old = first["gpu_medians"][gpu]
            new = last["gpu_medians"][gpu]
            if old > 0:
                pct = round(((new - old) / old) * 100, 2)
                changes.append({"gpu": gpu, "change_pct": pct, "old": old, "new": new})

    changes.sort(key=lambda x: x["change_pct"])
    return {
        "biggest_drops": changes[:3],
        "biggest_increases": list(reversed(changes[-3:]))
    }


def main():
    # Load all daily snapshots
    files = sorted(glob.glob(os.path.join(HISTORY_DIR, "pricing-*.json")))
    if not files:
        print("No pricing snapshots found.")
        return

    print(f"Processing {len(files)} daily snapshots...")
    snapshots = []
    for f in files:
        try:
            snapshots.append(load_snapshot(f))
        except Exception as e:
            print(f"  Skipping {f}: {e}")

    if not snapshots:
        print("No valid snapshots.")
        return

    # Compute base medians from first snapshot
    first_day = compute_daily_index(snapshots[0])
    base_medians = first_day["gpu_medians"]

    # Compute daily index for all snapshots
    daily_indices = []
    for snap in snapshots:
        daily = compute_daily_index(snap, base_medians)
        daily_indices.append(daily)

    # Compute derived analytics
    provider_scores = compute_provider_scores(snapshots)
    movers = compute_movers(daily_indices)

    # Build output
    output = {
        "metadata": {
            "name": "GPU Cloud Price Index (GCPI)",
            "description": "Proprietary price index tracking cloud GPU costs across providers over time. Base index = 100 on first tracking date.",
            "version": "1.0.0",
            "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source": "AI Infrastructure Index",
            "url": "https://alpha-one-index.github.io/ai-infra-index/",
            "methodology": "Median per-GPU-hour price across all providers and regions, normalized to base date index of 100",
            "base_date": snapshots[0]["date"],
            "latest_date": snapshots[-1]["date"],
            "total_snapshots": len(daily_indices),
            "tracked_gpus": INDEX_GPUS,
            "license": "MIT - cite as: Alpha One Index. GPU Cloud Price Index (GCPI). https://github.com/alpha-one-index/ai-infra-index"
        },
        "latest_composite_index": daily_indices[-1]["composite_index"],
        "latest_summary": {
            "date": daily_indices[-1]["date"],
            "gpu_medians": daily_indices[-1]["gpu_medians"],
            "cheapest_per_gpu": daily_indices[-1]["provider_cheapest"]
        },
        "provider_competitiveness": provider_scores,
        "price_movers": movers,
        "time_series": [
            {
                "date": d["date"],
                "composite_index": d["composite_index"],
                "gpu_index": d["gpu_index"],
                "gpu_medians": d["gpu_medians"],
                "num_gpus_tracked": d["num_gpus_tracked"],
                "num_skus": d["num_skus"]
            }
            for d in daily_indices
        ]
    }

    # Write output
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"GPU Price Index generated: {OUTPUT_FILE}")
    print(f"  Snapshots: {len(daily_indices)}")
    print(f"  Date range: {snapshots[0]['date']} to {snapshots[-1]['date']}")
    print(f"  Composite index: {daily_indices[-1]['composite_index']}")
    print(f"  GPUs tracked: {daily_indices[-1]['num_gpus_tracked']}")


if __name__ == "__main__":
    main()
