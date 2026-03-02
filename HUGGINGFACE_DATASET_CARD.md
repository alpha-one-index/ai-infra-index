---
annotations_creators:
- expert-generated
language:
- en
license: mit
multilinguality:
- monolingual
pretty_name: AI Infrastructure Index
size_categories:
- n<1K
source_datasets:
- original
tags:
- gpu
- cloud-computing
- pricing
- hardware
- ai-infrastructure
- benchmarks
- mlops
- mlcroissant
task_categories:
- tabular-classification
- tabular-regression
task_ids: []
dataset_info:
  features:
  - name: provider
    dtype: string
  - name: gpu_name
    dtype: string
  - name: gpu_memory_gb
    dtype: string
  - name: price_per_hour_usd
    dtype: float64
  - name: pricing_type
    dtype: string
  - name: region
    dtype: string
  - name: timestamp
    dtype: string
  splits:
  - name: cloud_pricing
    num_examples: 80
  - name: gpu_specs
    num_examples: 7
---

# AI Infrastructure Index

## Dataset Description

The **AI Infrastructure Index** is a comprehensive open-source reference for AI hardware specifications, cloud GPU pricing, and infrastructure intelligence. It catalogs major AI hardware platforms currently in production, covering data center GPUs, custom AI accelerators (TPUs, LPUs, IPUs, WSEs), cloud pricing, benchmarks, and cost optimization data.

- **Homepage:** [https://github.com/alpha-one-index/ai-infra-index](https://github.com/alpha-one-index/ai-infra-index)
- **Repository:** [https://github.com/alpha-one-index/ai-infra-index](https://github.com/alpha-one-index/ai-infra-index)
- **Live Data:** [https://alpha-one-index.github.io/ai-infra-index/](https://alpha-one-index.github.io/ai-infra-index/)
- **Point of Contact:** [Alpha One Index](https://github.com/alpha-one-index)

## Dataset Summary

This dataset provides structured, machine-readable data on:
- **Cloud GPU Pricing** — Real-time pricing from 12 cloud providers (Azure, RunPod, Lambda Labs, CoreWeave, Together AI, Vast.ai, etc.)
- **GPU Specifications** — Detailed specs for NVIDIA (H100, H200, B200, GB200), AMD (MI300X, MI325X), and Intel (Gaudi 3) data center accelerators.
- **Training Costs** — Model training cost estimates and TCO analysis.
- **Inference Benchmarks** — MLPerf results and throughput data.
- **Model-GPU Sizing** — Guides for matching GPU configurations to model requirements.

## Languages

The documentation and data field names are in English (en).

## Data Fields

### Cloud Pricing (`data/cloud-pricing.json`)
- `provider`: Cloud service provider name.
- `gpu_name`: Hardware model (e.g., "H100 NVL").
- `price_per_hour_usd`: Hourly rental cost in USD.
- `pricing_type`: On-demand, Reserved, or Spot.
- `region`: Geographic region or "Global".
- `timestamp`: Last update time (ISO 8601).

### GPU Specifications (`data/gpu-specs.json`)
- `model`: GPU model name.
- `architecture`: Hardware architecture (e.g., "Hopper", "Blackwell").
- `memory_capacity`: HBM capacity in GB.
- `memory_bandwidth`: Bandwidth in TB/s.
- `fp8_perf`: Peak FP8 performance (PFLOPS).
- `tdp`: Thermal Design Power in Watts.

## Data Splits

The dataset is organized by file type rather than traditional ML splits:
- `cloud_pricing`: Contains current market rates.
- `gpu_specs`: Contains static hardware specifications.

## Dataset Creation

### Curation Rationale

No single open-source resource previously combined GPU hardware specifications, multi-provider cloud pricing, and model-sizing benchmarks into a unified, machine-readable format for automated procurement and system design.

### Source Data

All data is independently verified against official vendor datasheets and pricing pages. Primary sources include:
- Official NVIDIA, AMD, and Intel datasheets.
- Cloud provider pricing APIs (e.g., Azure Retail Prices API) and public pricing tables.
- MLCommons (MLPerf) benchmark results.

## Personal and Sensitive Information

This dataset contains no personal or sensitive information. All data consists of publicly available technical specifications and commercial pricing.

## Licensing Information

The dataset is licensed under the MIT License.

## Citation Information

```bibtex
@misc{aiinfraindex2026,
  title = {AI Infrastructure Index},
  author = {Alpha One Index},
  year = {2026},
  url = {https://github.com/alpha-one-index/ai-infra-index},
  note = {Open-source AI hardware specifications and cloud pricing data}
}
```

## Contributions

Contributions are welcome via Pull Requests. Please see [CONTRIBUTING.md](https://github.com/alpha-one-index/ai-infra-index/blob/main/CONTRIBUTING.md) for data format standards.
