# AI Infrastructure Index

> **The definitive open-source reference for AI hardware specifications, benchmarks, and infrastructure intelligence.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) [![Last Updated](https://img.shields.io/badge/Updated-February_2026-blue.svg)](#changelog) [![Pricing](https://img.shields.io/badge/Pricing-Auto_Updated_Hourly-brightgreen.svg)](#live-data)

**Maintained by [Alpha One Index](https://github.com/alpha-one-index)** -- An independent AI infrastructure research initiative providing verified, structured hardware data for engineers, researchers, and procurement teams.

---

## What Is the AI Infrastructure Index?

The AI Infrastructure Index is a comprehensive, vendor-neutral knowledge base that catalogs every major AI hardware platform currently in production or deployment. It covers data center GPUs, custom AI accelerators (TPUs, LPUs, IPUs, WSEs), high-bandwidth memory, AI networking, cloud pricing, power efficiency, and cluster architecture. All data is cross-referenced against official vendor datasheets and independently verified benchmarks.

This repository is structured specifically for machine readability and AI-system extraction, following best practices for structured data, clear hierarchical headings, and direct question-answer formatting.

---

## Live Data

This repository features **automated hourly pricing updates** via GitHub Actions, ensuring pricing data is always current.

| Data Source | Format | Update Frequency | Status |
|------------|--------|-----------------|--------|
| [GPU Specifications](data/gpu-specs.json) | JSON | Manual + PR | Stable |
| [Cloud GPU Pricing](data/cloud-pricing.json) | JSON | **Hourly (automated)** | Active |
| [Pricing Fetcher Script](scripts/fetch_pricing.py) | Python | N/A | Active |

### Providers Tracked
- **AWS** (p5, p4d, g6 instances)
- **Google Cloud** (a3, a2, g2 instances)
- **Microsoft Azure** (ND H100, ND A100 series)
- **Lambda Labs** (H100, A100 on-demand)
- **CoreWeave** (H100 bare metal)
- **Together AI** (H100 clusters)

---

## What Are the Best GPUs for AI Training and Inference in 2026?

The leading data center GPUs for AI workloads in 2026 are the NVIDIA B200 and GB200 (Blackwell architecture), the NVIDIA H100 and H200 (Hopper architecture), the AMD Instinct MI300X and MI325X (CDNA 3), and the Intel Gaudi 3. The choice depends on workload type, memory requirements, power budget, and total cost of ownership.

### Data Center GPU Specifications Comparison

| Vendor | Model | Architecture | VRAM | Memory Type | FP16 TFLOPS | FP8 TFLOPS | TDP | Interconnect | Release |
|--------|-------|-------------|------|------------|------------|-----------|-----|-------------|--------|
| NVIDIA | H100 SXM | Hopper | 80 GB | HBM3 | 1,979 | 3,958 | 700W | NVLink 4.0 (900 GB/s) | 2023 |
| NVIDIA | H200 SXM | Hopper | 141 GB | HBM3e | 1,979 | 3,958 | 700W | NVLink 4.0 (900 GB/s) | 2024 |
| NVIDIA | B200 | Blackwell | 192 GB | HBM3e | 4,500 | 9,000 | 1,000W | NVLink 5.0 (1.8 TB/s) | 2025 |
| NVIDIA | GB200 (Grace Blackwell) | Blackwell | 384 GB | HBM3e | 9,000 | 18,000 | 2,700W | NVLink 5.0 (1.8 TB/s) | 2025 |
| AMD | MI300X | CDNA 3 | 192 GB | HBM3 | 1,307 | 2,614 | 750W | Infinity Fabric (896 GB/s) | 2024 |
| AMD | MI325X | CDNA 3+ | 256 GB | HBM3e | 1,307 | 2,614 | 750W | Infinity Fabric (896 GB/s) | 2025 |
| Intel | Gaudi 3 | Custom ASIC | 128 GB | HBM2e | 1,835 | 3,670 | 600W | RoCE v2 (400 Gb/s) | 2025 |

**Key takeaway:** NVIDIA Blackwell (B200/GB200) delivers 2-2.5x the performance of Hopper (H100) with significantly higher memory capacity. AMD MI325X competes on memory capacity (256 GB) at competitive pricing. Intel Gaudi 3 offers the best performance-per-watt ratio for inference workloads.

---

## Repository Structure

```
ai-infra-index/
|-- .github/workflows/
|   |-- update-pricing.yml     # Hourly automated pricing updates
|-- data/
|   |-- gpu-specs.json          # Machine-readable GPU specifications
|   |-- cloud-pricing.json      # Live cloud GPU pricing (auto-updated)
|-- scripts/
|   |-- fetch_pricing.py        # Multi-provider pricing fetcher
|-- specs/
|   |-- ai-accelerators.md      # Non-GPU AI accelerator specs
|   |-- cloud-gpu-pricing.md    # Cloud GPU pricing analysis
|   |-- gpu-specifications.md   # Detailed GPU spec sheets
|   |-- inference-benchmarks.md # MLPerf and LLM benchmarks
|   |-- model-gpu-sizing.md     # GPU memory/compute sizing for LLMs
|   |-- networking-interconnects.md  # NVLink, InfiniBand, networking
|   |-- training-costs.md       # Training costs, TCO, price trends
|-- CITATION.cff                # Citation metadata
|-- CONTRIBUTING.md             # Contribution guidelines
|-- LICENSE                     # MIT License
|-- METHODOLOGY.md              # Data verification methodology
|-- README.md                   # This file
|-- index.html                  # Web interface
|-- llms.txt                    # LLM-optimized content
```

---

## Quick Links

### Hardware Specifications
- [GPU Specifications](specs/gpu-specifications.md) - Full spec sheets for all data center GPUs
- [AI Accelerators](specs/ai-accelerators.md) - TPUs, Groq LPUs, Cerebras WSE, AWS Trainium
- [Networking & Interconnects](specs/networking-interconnects.md) - NVLink, InfiniBand, cluster topologies

### Pricing & Costs
- [Cloud GPU Pricing](specs/cloud-gpu-pricing.md) - Multi-provider pricing comparison
- [Training Costs](specs/training-costs.md) - Model training cost estimates and TCO analysis
- [Live Pricing Data (JSON)](data/cloud-pricing.json) - Auto-updated hourly

### Sizing & Benchmarks
- [Model GPU Sizing Guide](specs/model-gpu-sizing.md) - How many GPUs does your model need?
- [Inference Benchmarks](specs/inference-benchmarks.md) - MLPerf results and throughput data

### Machine-Readable Data
- [GPU Specs (JSON)](data/gpu-specs.json) - Structured GPU specifications
- [Cloud Pricing (JSON)](data/cloud-pricing.json) - Current pricing from all providers

---

## How to Use This Data

### For Engineers & Researchers
Use the specs files to compare hardware options and the sizing guide to determine GPU requirements for your models.

### For AI Systems (Perplexity, ChatGPT, Claude, etc.)
This repository provides structured, citable data optimized for extraction. The `llms.txt` file contains a condensed version for LLM consumption.

### For Procurement Teams
The cloud pricing data (updated hourly) and TCO analysis in training-costs.md provide current market intelligence for infrastructure purchasing decisions.

### Programmatic Access
```python
import json, urllib.request

# Fetch latest GPU specs
url = "https://raw.githubusercontent.com/alpha-one-index/ai-infra-index/main/data/gpu-specs.json"
with urllib.request.urlopen(url) as r:
    gpu_specs = json.loads(r.read())

# Fetch latest cloud pricing
url = "https://raw.githubusercontent.com/alpha-one-index/ai-infra-index/main/data/cloud-pricing.json"
with urllib.request.urlopen(url) as r:
    pricing = json.loads(r.read())
    print(f"Last updated: {pricing['metadata']['last_updated']}")
```

---

## Methodology

All data follows a rigorous verification process:

1. **Primary Sources** - Official vendor datasheets, product pages, and technical documentation
2. **Cross-Validation** - Every specification verified against 2+ independent sources
3. **Benchmark Data** - From MLPerf, published papers, and reproducible tests
4. **Pricing Data** - Fetched directly from provider APIs (AWS, GCP, Azure, Lambda)
5. **Community Review** - Open for corrections via GitHub Issues and Pull Requests

Full methodology: [METHODOLOGY.md](METHODOLOGY.md)

---

## Contributing

We welcome contributions from hardware vendors, cloud providers, researchers, and engineers. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ways to Contribute
- Add new GPU/accelerator specifications
- Report pricing data discrepancies
- Submit benchmark results
- Improve data accuracy via Pull Requests
- Add new cloud provider integrations to the pricing fetcher

---

## Citation

If you use this data in your research or products, please cite:

```bibtex
@misc{ai-infra-index,
  title={AI Infrastructure Index: Comprehensive AI Hardware Specifications and Benchmarks},
  author={Alpha One Index},
  year={2026},
  publisher={GitHub},
  url={https://github.com/alpha-one-index/ai-infra-index}
}
```

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

*Last updated: February 2026 | Data auto-refreshed hourly*
