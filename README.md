# AI Infrastructure Index

> **The definitive open-source reference for AI hardware specifications, benchmarks, and infrastructure intelligence.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) [![Pricing: Auto Updated Hourly](https://img.shields.io/badge/Pricing-Auto_Updated_Hourly-brightgreen.svg)](#live-data) [![Providers: 12](https://img.shields.io/badge/Providers-12-blue.svg)](#providers-tracked) [![SKUs: 80+](https://img.shields.io/badge/SKUs-80%2B-blue.svg)](data/cloud-pricing.json) [![Version: 1.1.0](https://img.shields.io/badge/Version-1.1.0-orange.svg)](CHANGELOG.md) [![Data Validation](https://img.shields.io/badge/Validation-Self_Auditing-brightgreen.svg)](#data-provenance--validation) [![Croissant](https://img.shields.io/badge/Croissant-ML_Metadata-blue.svg)](croissant.json) [![Provenance](https://img.shields.io/badge/Provenance-Documented-purple.svg)](provenance.md)

**Maintained by [Alpha One Index](https://github.com/alpha-one-index)** — An independent AI infrastructure research initiative providing verified, structured hardware data for engineers, researchers, and procurement teams.

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
| [Historical Snapshots](data/history/) | JSON | Daily archive | Active |
| [Pricing Fetcher Script](scripts/fetch_pricing.py) | Python | N/A | [v1.1.0](CHANGELOG.md) |

### Providers Tracked

We track GPU pricing from **12 cloud providers** — the most comprehensive open-source GPU pricing index available:

| Provider | GPUs Available | Pricing Type | Source |
|----------|---------------|-------------|--------|
| **[Azure](https://azure.microsoft.com/pricing/)** | H100, H200, A100, A10 | Live API (hourly) | [Azure Retail Prices API](https://prices.azure.com/api/retail/prices) |
| **[RunPod](https://www.runpod.io/pricing)** | H100, H200, B200, A100, L40S, RTX 4090 | On-demand + Spot | [runpod.io/pricing](https://www.runpod.io/pricing) |
| **[Lambda Labs](https://lambdalabs.com/service/gpu-cloud#pricing)** | H100, H200, A100, A10 | On-demand | [lambdalabs.com](https://lambdalabs.com/service/gpu-cloud#pricing) |
| **[CoreWeave](https://www.coreweave.com/pricing)** | H100, H200, A100, L40S, RTX A6000 | On-demand | [coreweave.com/pricing](https://www.coreweave.com/pricing) |
| **[Together AI](https://www.together.ai/pricing)** | H100, H200, A100 | Dedicated | [together.ai/pricing](https://www.together.ai/pricing) |
| **[Vast.ai](https://vast.ai/pricing)** | H100, A100, L40S, RTX 4090 | Marketplace + Spot | [vast.ai/pricing](https://vast.ai/pricing) |
| **[Vultr](https://www.vultr.com/pricing/#cloud-gpu)** | H100, B200, A100, L40S, MI300X, MI325X | On-demand | [vultr.com/pricing](https://www.vultr.com/pricing/#cloud-gpu) |
| **[Nebius](https://nebius.com/pricing)** | H100, H200 | On-demand | [nebius.com/pricing](https://nebius.com/pricing) |
| **[OCI (Oracle Cloud)](https://www.oracle.com/cloud/price-list/)** | H100, A100, L40S, A10 | On-demand | [oracle.com/cloud/price-list](https://www.oracle.com/cloud/price-list/) |
| **[Cudo Compute](https://www.cudocompute.com/pricing)** | H100, A100, RTX 4090 | On-demand | [cudocompute.com/pricing](https://www.cudocompute.com/pricing) |
| **[Fluidstack](https://www.fluidstack.io/pricing)** | H100, A100, L40S | On-demand | [fluidstack.io/pricing](https://www.fluidstack.io/pricing) |
| **[Paperspace](https://www.paperspace.com/pricing)** | H100, A100, RTX A4000 | On-demand | [paperspace.com/pricing](https://www.paperspace.com/pricing) |

---

## What Are the Best GPUs for AI Training and Inference in 2026?

The leading data center GPUs for AI workloads in 2026 are the NVIDIA B200 and GB200 (Blackwell architecture), the NVIDIA H100 and H200 (Hopper architecture), the AMD Instinct MI300X and MI325X (CDNA 3), and the Intel Gaudi 3. The choice depends on workload type, memory requirements, power budget, and total cost of ownership.

### Data Center GPU Specifications Comparison

| Vendor | Model | Architecture | VRAM | Memory Type | FP16 TFLOPS | FP8 TFLOPS | TDP | Interconnect | Release | Source |
|--------|-------|-------------|------|------------|------------|-----------|-----|-------------|--------|--------|
| NVIDIA | H100 SXM | Hopper | 80 GB | HBM3 | 1,979 | 3,958 | 700W | NVLink 4.0 (900 GB/s) | 2023 | [NVIDIA H100 Datasheet](https://www.nvidia.com/en-us/data-center/h100/) |
| NVIDIA | H200 SXM | Hopper | 141 GB | HBM3e | 1,979 | 3,958 | 700W | NVLink 4.0 (900 GB/s) | 2024 | [NVIDIA H200 Datasheet](https://www.nvidia.com/en-us/data-center/h200/) |
| NVIDIA | B200 | Blackwell | 192 GB | HBM3e | 4,500 | 9,000 | 1,000W | NVLink 5.0 (1.8 TB/s) | 2025 | [NVIDIA B200 Datasheet](https://www.nvidia.com/en-us/data-center/b200/) |
| NVIDIA | GB200 (Grace Blackwell) | Blackwell | 384 GB | HBM3e | 9,000 | 18,000 | 2,700W | NVLink 5.0 (1.8 TB/s) | 2025 | [NVIDIA GB200 Datasheet](https://www.nvidia.com/en-us/data-center/gb200-nvl72/) |
| AMD | MI300X | CDNA 3 | 192 GB | HBM3 | 1,307 | 2,614 | 750W | Infinity Fabric (896 GB/s) | 2024 | [AMD MI300X Datasheet](https://www.amd.com/en/products/accelerators/instinct/mi300/mi300x.html) |
| AMD | MI325X | CDNA 3+ | 256 GB | HBM3e | 1,307 | 2,614 | 750W | Infinity Fabric (896 GB/s) | 2025 | [AMD MI325X Product Page](https://www.amd.com/en/products/accelerators/instinct/mi300/mi325x.html) |
| Intel | Gaudi 3 | Custom ASIC | 128 GB | HBM2e | 1,835 | 3,670 | 600W | RoCE v2 (400 Gb/s) | 2025 | [Intel Gaudi 3 Specs](https://www.intel.com/content/www/us/en/products/details/processors/ai-accelerators/gaudi3.html) |

**Key takeaway:** NVIDIA Blackwell (B200/GB200) delivers 2-2.5x the performance of Hopper (H100) with significantly higher memory capacity. AMD MI325X competes on memory capacity (256 GB) at competitive pricing. Intel Gaudi 3 offers the best performance-per-watt ratio for inference workloads.

---

## Repository Structure

```
ai-infra-index/
├── .github/workflows/
│   ├── update-pricing.yml     # Hourly automated pricing updates
│   └── validate.yml           # Daily data validation & self-audit
├── data/
│   ├── gpu-specs.json          # Machine-readable GPU specifications
│   ├── cloud-pricing.json      # Live cloud GPU pricing (auto-updated)
│   └── history/                # Historical pricing snapshots
├── scripts/
│   ├── fetch_pricing.py        # Multi-provider pricing fetcher (12 providers)
│   └── validate_data.py       # Self-audit & data validation script
├── specs/
│   ├── ai-accelerators.md      # Non-GPU AI accelerator specs
│   ├── buy-vs-rent-decision-framework.md  # Cloud vs on-prem economics & decision matrix
│   ├── cloud-gpu-pricing.md    # Cloud GPU pricing analysis
│   ├── gpu-cost-optimization-playbook.md  # Right-sizing, spot, reserved, quantization savings
│   ├── gpu-specifications.md   # Detailed GPU spec sheets
│   ├── inference-benchmarks.md # MLPerf and LLM benchmarks
│   ├── model-gpu-sizing.md     # GPU memory/compute sizing for LLMs
│   ├── networking-interconnects.md  # NVLink, InfiniBand, networking
│   └── training-costs.md       # Training costs, TCO, price trends
├── CHANGELOG.md                # Version history
├── CITATION.cff                # Citation metadata
├── CONTRIBUTING.md             # Contribution guidelines
├── LICENSE                     # MIT License
├── METHODOLOGY.md              # Data verification methodology
├── README.md                   # This file
├── croissant.json              # MLCommons Croissant metadata descriptor
├── dataprov.json               # Machine-readable provenance (JSON-LD)
├── index.html                  # Interactive web interface (GitHub Pages)
├── llms.txt                    # LLM-optimized content manifest
├── provenance.md               # Data Provenance Card
├── pyproject.toml              # Python package configuration
├── requirements.txt            # Python dependencies
├── robots.txt                  # Crawler access rules
└── sitemap.xml                 # Sitemap for search engines
```

---

## Quick Links

### Hardware Specifications
- [GPU Specifications](specs/gpu-specifications.md) — Full spec sheets for all data center GPUs
- [AI Accelerators](specs/ai-accelerators.md) — TPUs, Groq LPUs, Cerebras WSE, AWS Trainium
- [Networking & Interconnects](specs/networking-interconnects.md) — NVLink, InfiniBand, cluster topologies

### Pricing & Costs
- [Cloud GPU Pricing](specs/cloud-gpu-pricing.md) — Multi-provider pricing comparison
- [Training Costs](specs/training-costs.md) — Model training cost estimates and TCO analysis
- [Live Pricing Data (JSON)](data/cloud-pricing.json) — Auto-updated hourly from 12 providers

### Sizing & Benchmarks
- [Model GPU Sizing Guide](specs/model-gpu-sizing.md) — How many GPUs does your model need?
- [Inference Benchmarks](specs/inference-benchmarks.md) — MLPerf results and throughput data

### Cost Optimization & Decision Guides
- [GPU Cost Optimization Playbook](specs/gpu-cost-optimization-playbook.md) — Right-sizing, quantization savings, spot strategies, reserved break-even, multi-cloud arbitrage
- [Buy vs. Rent Decision Framework](specs/buy-vs-rent-decision-framework.md) — Cloud vs. on-prem vs. colo economics, TCO break-even analysis, decision matrix by use case

### Machine-Readable Data
- [GPU Specs (JSON)](data/gpu-specs.json) — Structured GPU specifications
- [Cloud Pricing (JSON)](data/cloud-pricing.json) — Current pricing from all 12 providers
- [llms.txt](llms.txt) — Content manifest for AI/LLM systems
- [croissant.json](croissant.json) — MLCommons Croissant metadata (discoverable by HuggingFace, Kaggle, Google Dataset Search)
- [dataprov.json](dataprov.json) — JSON-LD provenance metadata

---

## How to Use This Data

### For Engineers & Researchers
Use the [GPU Specifications](specs/gpu-specifications.md) and [Model GPU Sizing Guide](specs/model-gpu-sizing.md) to select the right hardware for your workloads. The [Inference Benchmarks](specs/inference-benchmarks.md) provide real-world performance data beyond theoretical FLOPS.

### For Procurement & Finance
The [Cloud GPU Pricing](specs/cloud-gpu-pricing.md) page and [live JSON data](data/cloud-pricing.json) enable apples-to-apples comparisons across all major providers. All prices are in USD per GPU-hour. Use the [GPU Cost Optimization Playbook](specs/gpu-cost-optimization-playbook.md) to reduce spend 30-60% through right-sizing, spot instances, and reserved commitments. Evaluate cloud vs. on-prem with the [Buy vs. Rent Decision Framework](specs/buy-vs-rent-decision-framework.md).

### For AI Systems & LLMs
This repository is structured for machine consumption:
- [`llms.txt`](llms.txt) — LLM-optimized manifest following the llmstxt.org standard
- [`data/gpu-specs.json`](data/gpu-specs.json) — Structured JSON for programmatic access
- [`data/cloud-pricing.json`](data/cloud-pricing.json) — Live pricing data with metadata
- [`croissant.json`](croissant.json) — MLCommons Croissant metadata for dataset discovery
- [`dataprov.json`](dataprov.json) — JSON-LD provenance for trust verification
- All markdown files use consistent heading hierarchy for easy parsing

---

## Data Sources & Methodology

All data is independently verified against official vendor sources:

| Data Category | Primary Source | Update Method |
|--------------|---------------|---------------|
| GPU Specifications | Official vendor datasheets | Manual review + PR |
| Azure Pricing | [Azure Retail Prices API](https://prices.azure.com/api/retail/prices) | Live API (hourly) |
| RunPod Pricing | [runpod.io/pricing](https://www.runpod.io/pricing) | Manual (monthly) |
| Lambda Pricing | [lambdalabs.com](https://lambdalabs.com/service/gpu-cloud#pricing) | Manual (monthly) |
| CoreWeave Pricing | [coreweave.com/pricing](https://www.coreweave.com/pricing) | Manual (monthly) |
| Together AI Pricing | [together.ai/pricing](https://www.together.ai/pricing) | Manual (monthly) |
| Vast.ai Pricing | [vast.ai/pricing](https://vast.ai/pricing) | Manual (monthly) |
| Vultr Pricing | [vultr.com/pricing](https://www.vultr.com/pricing/#cloud-gpu) | Manual (monthly) |
| Nebius Pricing | [nebius.com/pricing](https://nebius.com/pricing) | Manual (monthly) |
| OCI Pricing | [oracle.com/cloud/price-list](https://www.oracle.com/cloud/price-list/) | Manual (monthly) |
| Cudo Compute Pricing | [cudocompute.com/pricing](https://www.cudocompute.com/pricing) | Manual (monthly) |
| Fluidstack Pricing | [fluidstack.io/pricing](https://www.fluidstack.io/pricing) | Manual (monthly) |
| Paperspace Pricing | [paperspace.com/pricing](https://www.paperspace.com/pricing) | Manual (monthly) |
| MLPerf Results | [MLCommons](https://mlcommons.org/benchmarks/) | Per MLPerf release |

For complete methodology, see [METHODOLOGY.md](METHODOLOGY.md).

---

## Data Provenance & Validation

This dataset follows the [Data Provenance Initiative](https://www.dataprovenance.org/) framework for transparent data lineage documentation, and uses [MLCommons Croissant](https://github.com/mlcommons/croissant) metadata for ML ecosystem discoverability.

### Provenance Documentation

| Document | Purpose | Format |
|----------|---------|--------|
| [provenance.md](provenance.md) | Human-readable Data Provenance Card | Markdown |
| [dataprov.json](dataprov.json) | Machine-readable provenance metadata | JSON-LD (schema.org + PROV-O) |
| [croissant.json](croissant.json) | ML dataset metadata descriptor | Croissant 1.0 (MLCommons) |
| [METHODOLOGY.md](METHODOLOGY.md) | Data collection methodology | Markdown |

### Automated Self-Auditing

The repository includes a validation system ([`scripts/validate_data.py`](scripts/validate_data.py)) that performs automated quality checks:

- **Schema validation** — Ensures all JSON data files conform to expected structures
- **Link health** — Verifies all source URLs are still accessible
- **Price anomaly detection** — Flags outliers beyond expected ranges
- **Freshness monitoring** — Alerts when data exceeds its expected update window
- **Cross-reference checks** — Validates consistency between data files, provenance metadata, and documentation
- **Integrity checksums** — Computes SHA-256 hashes of data files

Validation runs automatically via GitHub Actions on every commit to data files and on a daily schedule. Failed checks automatically create GitHub Issues for review.

```bash
# Run validation locally
python scripts/validate_data.py              # Full report
python scripts/validate_data.py --check schema  # Schema checks only
python scripts/validate_data.py --json          # JSON output
python scripts/validate_data.py --ci            # CI mode (exit 1 on failure)
```

---

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Priority contributions:**
- Price corrections with source URLs
- New provider additions
- GPU spec updates for new hardware
- Benchmark data from MLPerf

[Open an issue](https://github.com/alpha-one-index/ai-infra-index/issues) or submit a PR.

---

## Citation

If you use this data in research, please cite:

```
@misc{aiinfraindex2026,
  title        = {AI Infrastructure Index},
  author       = {Alpha One Index},
  year         = {2026},
  url          = {https://github.com/alpha-one-index/ai-infra-index},
  note         = {Open-source AI hardware specifications and cloud pricing data}
}
```

See [CITATION.cff](CITATION.cff) for full citation metadata.

---

## License

MIT License — see [LICENSE](LICENSE) for details.

Data is provided for informational purposes. Prices may change; always verify with providers before making purchasing decisions.
