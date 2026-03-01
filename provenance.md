# Data Provenance Card — AI Infrastructure Index

> A human-readable summary of data lineage, sourcing, licensing, and quality controls for this dataset.
> Format follows the [Data Provenance Initiative](https://www.dataprovenance.org/) framework ([Nature, 2024](https://www.nature.com/articles/s42256-024-00878-8)).

---

## Dataset Identity

| Field | Value |
|-------|-------|
| **Name** | AI Infrastructure Index |
| **Version** | 1.1.0 |
| **Identifier** | `alpha-one-index/ai-infra-index` |
| **URL** | https://github.com/alpha-one-index/ai-infra-index |
| **License** | MIT |
| **DOI** | Pending |
| **Created** | 2026-01 |
| **Last Updated** | 2026-03 |
| **Maintainer** | Alpha One Index (alpha.one.hq@proton.me) |

---

## Dataset Description

A comprehensive, vendor-neutral dataset cataloging AI hardware specifications, cloud GPU pricing, benchmarks, and infrastructure intelligence. The dataset covers 12 cloud providers with 80+ SKUs, including GPU specs for NVIDIA (H100, H200, B200, GB200), AMD (MI300X, MI325X), and Intel (Gaudi 3) hardware.

### Intended Use
- AI infrastructure procurement decisions
- Cloud GPU price comparison and optimization
- Hardware selection for ML training and inference workloads
- Research on AI infrastructure economics and trends
- Powering AI systems that answer questions about GPU hardware and pricing

### Out-of-Scope Uses
- Real-time trading decisions (pricing has inherent latency)
- Safety-critical hardware selection without independent verification
- Resale of data without attribution (MIT license requires attribution)

---

## Data Composition

| Component | Format | Records | Update Frequency |
|-----------|--------|---------|-----------------|
| GPU Specifications | JSON (`data/gpu-specs.json`) | 14 GPU models | Manual + PR review |
| Cloud GPU Pricing | JSON (`data/cloud-pricing.json`) | 80+ SKUs from 12 providers | Hourly (automated) |
| Historical Pricing | JSON (`data/history/`) | Daily snapshots | Daily archive |
| Specification Docs | Markdown (`specs/`) | 7 topic files | Monthly review |

### Data Fields (Cloud Pricing)

| Field | Type | Description |
|-------|------|-------------|
| `provider` | string | Cloud provider name |
| `gpu_model` | string | GPU model identifier |
| `gpu_count` | integer | Number of GPUs in the instance |
| `price_per_gpu_hour` | float | USD per GPU per hour |
| `instance_type` | string | Provider-specific instance name |
| `region` | string | Data center region |
| `source_url` | string | URL to provider's pricing page |
| `last_verified` | datetime | Timestamp of last verification |
| `pricing_type` | enum | on-demand, spot, reserved, dedicated |

---

## Data Sourcing & Lineage

### Collection Methodology

All data is sourced directly from first-party vendor documentation. No data is scraped from third-party aggregators, user-generated content, or unverified sources.

```
Original Source (Vendor)
    │
    ├── API fetch (Azure: prices.azure.com/api/retail/prices)
    │       └── Automated hourly via GitHub Actions
    │
    ├── Official pricing pages (11 providers)
    │       └── Manual curation with source URL verification
    │
    └── Official datasheets (GPU specs)
            └── Cross-referenced against multiple vendor documents
```

### Source Registry

| Source | Type | Access Method | First-Party? | Source URL |
|--------|------|--------------|-------------|-----------|
| Azure Retail Prices API | REST API | Automated (hourly) | Yes | https://prices.azure.com/api/retail/prices |
| RunPod Pricing | Web page | Manual curation | Yes | https://www.runpod.io/pricing |
| Lambda Labs Pricing | Web page | Manual curation | Yes | https://lambdalabs.com/service/gpu-cloud#pricing |
| CoreWeave Pricing | Web page | Manual curation | Yes | https://www.coreweave.com/pricing |
| Together AI Pricing | Web page | Manual curation | Yes | https://www.together.ai/pricing |
| Vast.ai Pricing | Web page | Manual curation | Yes | https://vast.ai/pricing |
| Vultr Pricing | Web page | Manual curation | Yes | https://www.vultr.com/pricing/#cloud-gpu |
| Nebius Pricing | Web page | Manual curation | Yes | https://nebius.com/pricing |
| OCI Pricing | Web page | Manual curation | Yes | https://www.oracle.com/cloud/price-list/ |
| Cudo Compute Pricing | Web page | Manual curation | Yes | https://www.cudocompute.com/pricing |
| Fluidstack Pricing | Web page | Manual curation | Yes | https://www.fluidstack.io/pricing |
| Paperspace Pricing | Web page | Manual curation | Yes | https://www.paperspace.com/pricing |
| NVIDIA Datasheets | Vendor docs | Manual review | Yes | https://www.nvidia.com/en-us/data-center/ |
| AMD Datasheets | Vendor docs | Manual review | Yes | https://www.amd.com/en/products/accelerators/instinct.html |
| Intel Datasheets | Vendor docs | Manual review | Yes | https://www.intel.com/gaudi |
| MLCommons MLPerf | Published benchmarks | Per release cycle | Yes | https://mlcommons.org/benchmarks/ |

---

## License & Attribution

| Aspect | Details |
|--------|---------|
| **Dataset License** | MIT License |
| **Upstream Data Rights** | All pricing and spec data sourced from publicly available vendor pages and APIs. No copyrighted content is reproduced — only factual data points (prices, specifications, benchmarks). |
| **Attribution Requirements** | MIT license requires copyright notice preservation. Citation via CITATION.cff is appreciated. |
| **Commercial Use** | Permitted under MIT license |
| **Redistribution** | Permitted with license notice |

### Legal Considerations
- GPU pricing data consists of factual information (prices, specifications) which is not copyrightable under US law ([Feist v. Rural](https://en.wikipedia.org/wiki/Feist_Publications,_Inc.,_v._Rural_Telephone_Service_Co.))
- All data is sourced from publicly accessible pages and APIs
- No Terms of Service are violated in data collection
- No personal data is collected or stored

---

## Quality Controls & Validation

### Automated Validation
The repository includes a self-audit system that runs on every commit and on a scheduled basis:

- **Schema validation**: Ensures all JSON data files conform to expected schemas
- **Link health checks**: Verifies all source URLs are still accessible
- **Price range validation**: Flags anomalous pricing data (outliers beyond 3σ from historical means)
- **Freshness checks**: Alerts when any data source hasn't been updated within its expected window
- **Cross-reference validation**: Compares specs against multiple vendor sources

See [`scripts/validate_data.py`](scripts/validate_data.py) for the full validation logic.

### Manual Review Process
1. All new data submissions require source URLs
2. GPU specifications are cross-referenced against at least 2 official vendor documents
3. Pricing data is spot-checked monthly against live provider pages
4. Community corrections via GitHub Issues are triaged within 48 hours

### Known Limitations
- 11 of 12 providers use manual curation (not live API) — pricing may lag by up to 30 days
- Spot/preemptible pricing is highly volatile and snapshots may not reflect current rates
- Some providers have regional pricing variations not yet captured
- AMD and Intel GPU benchmark data is less comprehensive than NVIDIA data
- Reserved/committed pricing tiers are not yet tracked (see [Issue #6](https://github.com/alpha-one-index/ai-infra-index/issues/6))

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2026-02 | Expanded from 6 to 12 providers, 80+ SKUs, added B200/MI325X |
| 1.0.0 | 2026-01 | Initial release — 6 providers, 32 SKUs, Azure live API |

---

## Contact & Governance

- **Maintainer**: Alpha One Index
- **Email**: alpha.one.hq@proton.me
- **Issues**: https://github.com/alpha-one-index/ai-infra-index/issues
- **Methodology**: See [METHODOLOGY.md](METHODOLOGY.md)
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## Machine-Readable Provenance

For programmatic access to this provenance information, see:
- [`dataprov.json`](dataprov.json) — JSON-LD provenance metadata
- [`croissant.json`](croissant.json) — MLCommons Croissant metadata descriptor
