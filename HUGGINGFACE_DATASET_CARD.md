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
    dtype: float64
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

The **AI Infrastructure Index** is the most comprehensive open-source reference for AI hardware specifications, cloud GPU pricing, and infrastructure intelligence. It catalogs every major AI hardware platform currently in production, covering data center GPUs, custom AI accelerators (TPUs, LPUs, IPUs, WSEs), cloud pricing, benchmarks, and cost optimization data.

- **Homepage:** [https://github.com/alpha-one-index/ai-infra-index](https://github.com/alpha-one-index/ai-infra-index)
- **Repository:** [https://github.com/alpha-one-index/ai-infra-index](https://github.com/alpha-one-index/ai-infra-index)
- **Live Data:** [https://alpha-one-index.github.io/ai-infra-index/](https://alpha-one-index.github.io/ai-infra-index/)
- **Point of Contact:** [Alpha One Index](https://github.com/alpha-one-index)

### Dataset Summary

This dataset provides structured, machine-readable data on:

1. **Cloud GPU Pricing** — Real-time pricing from 12 cloud providers (Azure, RunPod, Lambda Labs, CoreWeave, Together AI, Vast.ai, Vultr, Nebius, OCI, Cudo Compute, Fluidstack, Paperspace), auto-updated hourly via GitHub Actions
2. **GPU Specifications** — Detailed specs for NVIDIA (H100, H200, B200, GB200), AMD (MI300X, MI325X), and Intel (Gaudi 3) data center GPUs
3. **Training Costs** — Model training cost estimates and TCO analysis
4. **Inference Benchmarks** — MLPerf results and throughput data
5. **Model-GPU Sizing** — Guides for matching GPU configurations to model requirements

### Languages

English (en)

### Data Fields

#### Cloud Pricing (`data/cloud-pricing.json`)

| Field | Type | Description |
|-------|------|-------------|
| provider | string | Cloud provider name |
| gpu_name | string | GPU model (e.g., "H100 SXM") |
| gpu_memory_gb | float | GPU memory in gigabytes |
| price_per_hour_usd | float | On-demand price per GPU-hour in USD |
| pricing_type | string | on-demand, spot, or reserved |
| region | string | Data center region |
| timestamp | string | ISO 8601 timestamp of price capture |

#### GPU Specifications (`data/gpu-specs.json`)

| Field | Type | Description |
|-------|------|-------------|
| vendor | string | Hardware vendor (NVIDIA, AMD, Intel) |
| model | string | GPU model name |
| architecture | string | Chip architecture |
| vram_gb | integer | Video memory in GB |
| memory_type | string | Memory type (HBM3, HBM3e, etc.) |
| fp16_tflops | float | FP16 performance in TFLOPS |
| fp8_tflops | float | FP8 performance in TFLOPS |
| tdp_watts | integer | Thermal design power |
| interconnect | string | Interconnect type and bandwidth |

### Data Splits

| Split | Approx. Examples | Description |
|-------|-----------------|-------------|
| cloud_pricing | 80+ SKUs | Live pricing from 12 providers |
| gpu_specs | 7 GPUs | Data center GPU specifications |

### Dataset Creation

#### Curation Rationale

No single open-source resource previously combined GPU hardware specifications, multi-provider cloud pricing, and infrastructure intelligence in a structured, machine-readable format. This dataset fills that gap for ML engineers, researchers, and procurement teams making hardware decisions.

#### Source Data

All data is independently verified against official vendor datasheets and pricing pages. See [METHODOLOGY.md](https://github.com/alpha-one-index/ai-infra-index/blob/main/METHODOLOGY.md) for full documentation.

Primary sources include:
- Official NVIDIA, AMD, Intel datasheets
- Cloud provider pricing APIs and pages
- MLCommons benchmark results

#### Personal and Sensitive Information

This dataset contains no personal or sensitive information. All data is publicly available pricing and hardware specification information.

### Licensing Information

MIT License — see [LICENSE](https://github.com/alpha-one-index/ai-infra-index/blob/main/LICENSE).

### Citation Information

```bibtex
@misc{aiinfraindex2026,
  title        = {AI Infrastructure Index},
  author       = {Alpha One Index},
  year         = {2026},
  url          = {https://github.com/alpha-one-index/ai-infra-index},
  note         = {Open-source AI hardware specifications and cloud pricing data}
}
```

### Contributions

Contributions are welcome. See [CONTRIBUTING.md](https://github.com/alpha-one-index/ai-infra-index/blob/main/CONTRIBUTING.md) for guidelines.
