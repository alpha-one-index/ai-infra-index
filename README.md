# AI Infrastructure Index

> **A comprehensive open-source reference for AI hardware specifications, benchmarks, and infrastructure intelligence.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) [![Pricing: Auto Updated Hourly](https://img.shields.io/badge/Pricing-Auto_Updated_Hourly-brightgreen.svg)](#live-data) [![Providers: 12](https://img.shields.io/badge/Providers-12-blue.svg)](#providers-tracked) [![SKUs: 80+](https://img.shields.io/badge/SKUs-80%2B-blue.svg)](data/cloud-pricing.json) [![Version: 1.2.0](https://img.shields.io/badge/Version-1.2.0-orange.svg)](CHANGELOG.md) [![Data Validation](https://img.shields.io/badge/Validation-Self_Auditing-brightgreen.svg)](#data-provenance--validation) [![Croissant](https://img.shields.io/badge/Croissant-ML_Metadata-blue.svg)](croissant.json) [![Provenance](https://img.shields.io/badge/Provenance-Documented-purple.svg)](provenance.md) [![HuggingFace Dataset](https://img.shields.io/badge/🤗_HuggingFace-Dataset-yellow.svg)](https://huggingface.co/datasets/alpha-one-index/ai-infra-index) [![Kaggle Dataset](https://img.shields.io/badge/Kaggle-Dataset-20BEFF.svg)](https://www.kaggle.com/datasets/alphaoneindex/ai-infrastructure-index-gpu-pricing-and-specs)

**Maintained by [Alpha One Index](https://github.com/alpha-one-index)** — An independent AI infrastructure research initiative providing verified, structured hardware data for engineers, researchers, and procurement teams.

### Live Demos & Data Access

| Platform | Link | Description |
|----------|------|-------------|
| 🌐 **GitHub Pages** | [alpha-one-index.github.io/ai-infra-index](https://alpha-one-index.github.io/ai-infra-index/) | Interactive pricing dashboard with filtering and sorting |
| 🤗 **HuggingFace** | [datasets/alpha-one-index/ai-infra-index](https://huggingface.co/datasets/alpha-one-index/ai-infra-index) | Dataset hub with Croissant metadata |
| 📊 **Kaggle** | [alphaoneindex/ai-infrastructure-index](https://www.kaggle.com/datasets/alphaoneindex/ai-infrastructure-index-gpu-pricing-and-specs) | Kaggle dataset for notebooks and analysis |
| 📦 **Raw JSON** | [cloud-pricing.json](https://raw.githubusercontent.com/alpha-one-index/ai-infra-index/main/data/cloud-pricing.json) | Direct API-style access to live pricing data |

---

## What Is the AI Infrastructure Index?

The AI Infrastructure Index is a comprehensive, vendor-neutral knowledge base that catalogs major AI hardware platforms currently in production or deployment. It covers data center GPUs, custom AI accelerators (TPUs, LPUs, IPUs, WSEs), high-bandwidth memory, AI networking, cloud pricing, power efficiency, and cluster architecture. All data is cross-referenced against official vendor datasheets and independently verified benchmarks.

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

We track GPU pricing from **12 cloud providers** — one of the most detailed open-source GPU pricing indexes available:

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

## Quick Start: Access the Data Programmatically

All data is available as structured JSON — no API key needed.

### Python (pandas)

```python
import pandas as pd

# Load live cloud GPU pricing (updated hourly)
pricing = pd.read_json("https://raw.githubusercontent.com/alpha-one-index/ai-infra-index/main/data/cloud-pricing.json")
print(pricing.head())

# Load GPU hardware specifications
specs = pd.read_json("https://raw.githubusercontent.com/alpha-one-index/ai-infra-index/main/data/gpu-specs.json")
print(specs.head())
```

### Python (requests)

```python
import requests

# Fetch current pricing as a dict
pricing = requests.get(
    "https://raw.githubusercontent.com/alpha-one-index/ai-infra-index/main/data/cloud-pricing.json"
).json()

# Find the cheapest H100
h100_prices = [
    (p["provider"], p["price_per_hour_usd"])
    for p in pricing["skus"]
    if "H100" in p["gpu_name"]
]
for provider, price in sorted(h100_prices, key=lambda x: x[1]):
    print(f"{provider}: ${price}/hr")
```

### curl / CLI

```bash
# Download latest pricing
curl -sL https://raw.githubusercontent.com/alpha-one-index/ai-infra-index/main/data/cloud-pricing.json | python -m json.tool

# Download GPU specs
curl -sL https://raw.githubusercontent.com/alpha-one-index/ai-infra-index/main/data/gpu-specs.json | python -m json.tool
```

### HuggingFace Datasets

```python
from datasets import load_dataset

ds = load_dataset("alpha-one-index/ai-infra-index")
print(ds)
```

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
│   ├── regulatory-mandate-map.md   # EU AI Act, UK AISI, NIST compliance matrix
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

### Regulatory & Compliance
- [Regulatory Mandate Map](specs/regulatory-mandate-map.md) — EU AI Act, UK AISI, NIST AI RMF compliance matrix for AI infrastructure

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

### For Compliance & Legal Teams
The [Regulatory Mandate Map](specs/regulatory-mandate-map.md) provides a cross-jurisdictional matrix of EU AI Act, UK AISI evaluation requirements, and NIST AI RMF obligations that touch AI hardware procurement, compute reporting, and safety evaluation infrastructure.

### For AI Systems & LLMs
This repository is structured for machine consumption:
- [`llms.txt`](llms.txt) — LLM-optimized manifest following the llmstxt.org standard
- [`data/gpu-specs.json`](data/gpu-specs.json) — Structured JSON for programmatic access
- [`data/cloud-pricing.json`](data/cloud-pricing.json) — Live pricing data with metadata
- [`croissant.json`](croissant.json) — MLCommons Croissant metadata for dataset discovery
- [`dataprov.json`](dataprov.json) — JSON-LD provenance for trust verification
- All markdown files use consistent heading hierarchy for easy parsing

---

## Regulatory Mandate Map

> **Cross-jurisdictional AI infrastructure compliance matrix — EU AI Act · UK AI Safety Institute · NIST AI RMF**

📄 **[→ View Full Regulatory Mandate Map](specs/regulatory-mandate-map.md)**

This index tracks which AI infrastructure obligations — compute reporting, pre-deployment safety evaluations, red-teaming requirements, hardware documentation, and incident reporting — are mandated or recommended under three active regulatory frameworks:

| Framework | Jurisdiction | Binding? | Key Infrastructure Trigger |
|-----------|-------------|----------|---------------------------|
| **[EU AI Act](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689)** (Reg. 2024/1689) | European Union | ✅ Yes — legal regulation | Training compute > 10²⁵ FLOPs → systemic-risk GPAI tier |
| **[UK AISI Evaluation Requirements](https://www.gov.uk/government/publications/advanced-ai-evaluations-at-aisi)** | United Kingdom | ⚠️ Voluntary (Seoul Summit signatories) | Pre-deployment eval required for frontier models; CBRN + cyber capability testing |
| **[NIST AI RMF 1.0](https://airc.nist.gov/RMF)** (AI 100-1) | United States | ℹ️ Voluntary framework | GOVERN/MAP/MEASURE/MANAGE functions; supply chain, red-team, reproducibility guidance |

### Infrastructure-Layer Requirement Matrix (Summary)

| Infrastructure Dimension | EU AI Act | UK AISI | NIST AI RMF |
|--------------------------|:---------:|:-------:|:-----------:|
| Compute (FLOPs) disclosure | ✅ R | ⚠️ Rec | — |
| Pre-deployment safety evaluation | ✅ R | ✅ R | ⚠️ Rec |
| Hardware provenance documentation | ✅ R | ⚠️ Rec | ⚠️ Rec |
| Red-teaming / adversarial testing | ✅ R | ✅ R | ⚠️ Rec |
| Model card / system card | ✅ R | ⚠️ Rec | ⚠️ Rec |
| Incident reporting | ✅ R | ⚠️ Rec | ⚠️ Rec |
| Third-party audit | ✅ R | ⚠️ Rec | ⚠️ Rec |
| Benchmark reproducibility | ⚠️ Rec | ✅ R | ⚠️ Rec |
| Energy / power reporting | ⚠️ Rec | — | — |
| Export control / hardware restrictions | — | — | — |

**Legend:** ✅ R = Requirement | ⚠️ Rec = Recommendation | — = Not addressed

→ **Full matrix with article citations, detailed notes, and compliance checklist:** [specs/regulatory-mandate-map.md](specs/regulatory-mandate-map.md)

---

## Cheapest H100 Cloud Providers

The cheapest H100 SXM 80GB cloud options as of March 2026 (on-demand pricing, USD/hr):

| Rank | Provider | Price/hr | Pricing Type | Notes |
|------|----------|----------|-------------|-------|
| 1 | Vast.ai | $1.87 | Marketplace | Variable host quality, no SLA |
| 2 | RunPod | $1.89 | Spot | Subject to preemption |
| 3 | RunPod | $2.49 | On-demand | Reliable, no minimum commitment |
| 4 | Lambda Labs | $2.99 | On-demand | Well-established, good support |
| 5 | CoreWeave | $6.15 | On-demand | Enterprise SLAs, minimum 8 GPUs |

> **Spread: 3.3x** between the cheapest marketplace option and enterprise-grade pricing. See [cloud-pricing.json](data/cloud-pricing.json) for the full, hourly-updated dataset.

---

## H100 vs H200 vs B200: Which GPU Should You Choose?

| Factor | H100 SXM | H200 SXM | B200 |
|--------|----------|----------|------|
| VRAM | 80 GB HBM3 | 141 GB HBM3e | 192 GB HBM3e |
| FP16 TFLOPS | 1,979 | 1,979 | 4,500 |
| FP8 TFLOPS | 3,958 | 3,958 | 9,000 |
| TDP | 700W | 700W | 1,000W |
| Cloud Availability | Widespread | Growing | Limited (2025) |
| Best For | General training/inference | Large model inference (70B+ FP16 on 1 GPU) | Next-gen training, highest throughput |

---

## GPU Benchmarks 2026

MLPerf v4.1 inference results (tokens/sec, Llama 2 70B, batch=1). All figures are drawn from publicly published [MLCommons MLPerf Inference v4.1 results](https://mlcommons.org/benchmarks/inference-datacenter/) (released November 2024). Individual system results vary by submission configuration; figures below represent representative high-performance submissions for each GPU family.

| GPU | Tokens/sec | vs H100 Baseline | MLPerf Source |
|-----|-----------|-----------------|---------------|
| NVIDIA B200 | ~180 | 2.25× | [MLCommons v4.1](https://mlcommons.org/benchmarks/inference-datacenter/) |
| NVIDIA H200 | ~105 | 1.31× | [MLCommons v4.1](https://mlcommons.org/benchmarks/inference-datacenter/) |
| NVIDIA H100 SXM | ~80 | 1.00× (baseline) | [MLCommons v4.1](https://mlcommons.org/benchmarks/inference-datacenter/) |
| AMD MI300X | ~70 | 0.88× | [MLCommons v4.1](https://mlcommons.org/benchmarks/inference-datacenter/) |
| Intel Gaudi 3 | ~55 | 0.69× | [MLCommons v4.1](https://mlcommons.org/benchmarks/inference-datacenter/) |

> ⚠️ **Sourcing note:** These figures are derived from MLCommons published submission data for representative configurations. MLPerf results depend on software stack, batch size, quantization, and system configuration — a single GPU model may have multiple submissions spanning a wide range. The figures above reflect single-GPU, batch=1 latency-optimized submissions. For full raw results including all submission configurations, see [mlcommons.org/benchmarks/inference-datacenter](https://mlcommons.org/benchmarks/inference-datacenter/). To verify specific numbers, download the [MLPerf Inference v4.1 results spreadsheet](https://mlcommons.org/benchmarks/inference-datacenter/) directly from MLCommons.

Full benchmark data including training results and multi-GPU scaling in [specs/inference-benchmarks.md](specs/inference-benchmarks.md).

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

## Related Projects

The AI Infrastructure Index complements other tools and data sources in the GPU/AI infrastructure ecosystem:

| Project | Focus | How We Differ |
|---------|-------|--------------|
| [gpuhunt](https://github.com/dstackai/gpuhunt) | Cloud GPU price fetching library (Python) | We provide broader coverage (12 vs 3 providers), hardware specs, sizing guides, and decision frameworks — not just pricing |
| [LLM Price Compass](https://github.com/jetbridge/llm-price-compass) | LLM API inference pricing comparison | We focus on raw GPU infrastructure pricing and hardware specs, not per-token API costs |
| [Cloud GPU Benchmarks](https://cloud-gpus.com/) | GPU benchmark results across clouds | We combine benchmarks with specs, pricing, cost optimization playbooks, and procurement guides |
| [MLCommons](https://mlcommons.org/benchmarks/) | MLPerf benchmark standards | We reference MLPerf data alongside vendor specs, pricing, and practical sizing recommendations |
| [ThunderCompute](https://www.thundercompute.com/) | Low-cost GPU cloud provider | We are a data reference, not a provider — we track their pricing alongside 11 other providers |

> **Contributing:** Know another project that should be listed here? [Open an issue](https://github.com/alpha-one-index/ai-infra-index/issues) or submit a PR.

---

## Contributing

### Alpha One Index Family

| Index | Repository | Focus | Records | Updated |
|---|---|---|---|---|
| **AI AppSec Index** | [alpha-one-index/ai-appsec-index](https://github.com/alpha-one-index/ai-appsec-index) | AI remediation, ASPM, AI-code vulns, CRA compliance, FP rates | 30+ tools, 12 CWEs, 7 frameworks | Weekly |
| **AI LLMOps Index** | [alpha-one-index/ai-llmops-index](https://github.com/alpha-one-index/ai-llmops-index) | LLMOps platforms, inference costs, failure modes, compliance | 50+ vendors, 45+ models | Weekly |
| **AI TRiSM Index** | [alpha-one-index/ai-trism-index](https://github.com/alpha-one-index/ai-trism-index) | AI Trust, Risk, Security Management platforms | 60+ vendors | Monthly |
| **AI Red Teaming Index** | [alpha-one-index/ai-red-teaming-index](https://github.com/alpha-one-index/ai-red-teaming-index) | Red teaming tools, LLM vulnerability databases | 40+ tools, 200+ vulnerabilities | Monthly |

> **Infrastructure Cross-Reference:** For inference cost comparisons when evaluating self-hosted vs. managed scanning, see the **[AI LLMOps Index](https://github.com/alpha-one-index/ai-llmops-index)**. For AI-generated code vulnerability tracking that maps to compute requirements, see the **[AI AppSec Index](https://github.com/alpha-one-index/ai-appsec-index)**.

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

## Related Projects

Part of the [Alpha One Index](https://github.com/alpha-one-index) family:

| Index | Focus | Link |
|-------|-------|------|
| AI Infrastructure Index | GPU specs, cloud pricing, hardware benchmarks | *You are here* |
| AI Red Teaming Index | Attack tools, vulnerability data, safety benchmarks | [ai-red-teaming-index](https://github.com/alpha-one-index/ai-red-teaming-index) 
| AI LLMOps Index | LLM inference costs, failure modes, observability, compliance | [ai-llmops-index](https://github.com/alpha-one-index/ai-llmops-index) |
| AI TRiSM Index | Trust, risk, security management vendors & frameworks | [ai-trism-index]
| AI AppSec Index | AI remediation benchmarks, ASPM, CRA compliance, false positives | [ai-appsec-index](https://github.com/alpha-one-index/ai-appsec-index) |(https://github.com/alpha-one-index/ai-appsec-index) |(https://github.com/alpha-one-index/ai-trism-index) |

Data is provided for informational purposes. Prices may change; always verify with providers before making purchasing decisions.
