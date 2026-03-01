# Methodology

> How the AI Infrastructure Index verifies and maintains its data.

---

## Verification Framework

All data in this repository follows a structured verification process designed to ensure accuracy, traceability, and currency. Every specification, benchmark, and pricing data point is verified before publication.

---

## Tier 1: Primary Source Verification

Every data point is traced to its primary source:

- **Hardware specifications** are verified against official vendor datasheets and product pages
- **Each entry includes a direct URL** to the primary source document
- **Specifications are recorded exactly** as published by the vendor, with no interpolation or estimation
- **Discrepancies between sources** are noted with all conflicting values listed

### Accepted Primary Sources

| Data Type | Primary Sources |
|---|---|
| GPU Specifications | NVIDIA, AMD, Intel official datasheets |
| ASIC Specifications | Google (TPU), AWS (Trainium), vendor datasheets |
| Cloud Pricing | Provider pricing pages (AWS, GCP, Azure, etc.) |
| Server Specifications | Supermicro, Dell, HPE, Lenovo product pages |
| Memory Standards | JEDEC published specifications |
| Interconnect Specs | NVIDIA (NVLink), Mellanox/NVIDIA (InfiniBand), IEEE (Ethernet) |

---

## Tier 2: Cross-Reference Validation

- All performance claims are **cross-referenced against at least two independent sources**
- Benchmark data must **match MLPerf published results** or be explicitly flagged as vendor-claimed
- Memory bandwidth figures are **verified against JEDEC specifications** where applicable
- Where vendor claims differ from independent measurements, both values are recorded

---

## Tier 3: Independent Testing

- Where available, independent benchmark results from **ServeTheHome, Phoronix, Chips and Cheese, and Lambda Labs** are compared against vendor claims
- Discrepancies between vendor claims and independent testing are documented
- Independent results are labeled with their source and testing methodology

---

## Tier 4: Pricing Verification

- Cloud pricing is **verified monthly** against live provider pricing pages
- On-premise pricing is sourced from **authorized distributors and published price lists**
- All pricing includes a **last-verified date**
- Historical pricing trends are maintained for longitudinal analysis

---

## Data Currency

### Update Schedule

| Data Type | Update Frequency | Trigger |
|---|---|---|
| Cloud GPU Pricing | Monthly | Provider price changes |
| Hardware Specifications | Per-event | New product launches |
| Benchmark Results | Quarterly | MLPerf submissions, new independent tests |
| Interconnect Specifications | Per-event | New standard ratification |
| Market Intelligence | Weekly | News, announcements |

### Staleness Policy

- Data older than **90 days** without re-verification is flagged
- Pricing data older than **30 days** triggers a re-verification cycle
- All data includes a `Last Verified` date for transparency

---

## Error Handling

### Correction Process

1. Errors reported via GitHub Issues are triaged within 48 hours
2. Corrections are verified against primary sources before publication
3. All corrections are documented in commit messages with source attribution
4. Material corrections are noted in the changelog

### Disputed Data

When data points are disputed:
- All claimed values are listed with their respective sources
- The most conservative (vendor-published) figure is used as the default
- Independent measurements are provided as supplementary data
- Disputed status is clearly labeled

---

## Scope & Limitations

### What This Index Covers
- AI-specific GPUs and accelerators currently in production or deployment
- Cloud GPU pricing from providers with verified availability
- Networking and interconnect specifications for AI infrastructure
- Performance benchmarks from MLPerf and independent sources

### What This Index Does NOT Cover
- Consumer GPUs (gaming-focused products)
- Pre-release or unannounced products (until officially launched)
- Hyperscaler proprietary infrastructure not available to external customers
- Investment or purchasing recommendations

---

## Citation

If you use data from this index, please cite:

```
Alpha One Index. (2026). AI Infrastructure Index.
https://github.com/alpha-one-index/ai-infra-index
```

See [CITATION.cff](CITATION.cff) for machine-readable citation metadata.

---

*Part of the [AI Infrastructure Index](https://github.com/alpha-one-index/ai-infra-index) — Maintained by [Alpha One Index](https://github.com/alpha-one-index)*
