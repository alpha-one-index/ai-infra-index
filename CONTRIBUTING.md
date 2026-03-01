# Contributing to the AI Infrastructure Index

Thank you for your interest in contributing to the AI Infrastructure Index. This project aims to be the most accurate and comprehensive open-source reference for AI hardware specifications, benchmarks, and infrastructure data.

---

## How to Contribute

### Report an Error or Outdated Data

The most valuable contributions are corrections and updates:

1. **Open an Issue** with the label `data-correction` or `outdated-data`
2. Include:
   - The specific file and data point that needs correction
   - The correct value with a link to the primary source
   - The date you verified the information

### Suggest New Data

1. **Open an Issue** with the label `new-data`
2. Include:
   - What data you'd like to see added
   - Why it's relevant to AI infrastructure
   - At least one primary source URL

### Submit a Pull Request

1. Fork the repository
2. Create a feature branch (`git checkout -b update/h200-pricing`)
3. Make your changes following the data format standards below
4. Include source URLs for all data points
5. Submit a pull request with a clear description

---

## Data Format Standards

### Specification Tables

All hardware specification tables must follow this format:

```markdown
| Parameter | Value | Source | Last Verified |
|---|---|---|---|
| Memory | 80 GB HBM3 | [NVIDIA Datasheet](url) | 2026-02-28 |
```

### Pricing Tables

```markdown
| Provider | Instance Type | Per-GPU-Hour | Region | Last Verified |
|---|---|---|---|---|
| AWS | p5.48xlarge | $3.93 | us-east-1 | 2026-02-28 |
```

### Requirements for All Data

- Every data point must have a **primary source URL**
- All dates use **ISO 8601 format** (YYYY-MM-DD)
- Prices are in **USD** unless otherwise noted
- Performance metrics must specify the **benchmark, configuration, and precision**
- Vendor-claimed vs independently-verified data must be clearly labeled

---

## Verification Requirements

Before submitting, ensure your data meets our [Methodology](METHODOLOGY.md) standards:

- [ ] Data sourced from official vendor documentation or reputable independent testing
- [ ] Source URL included and accessible
- [ ] Cross-referenced against at least one additional source where possible
- [ ] Last-verified date included
- [ ] No interpolated or estimated values (unless clearly labeled)

---

## Scope Guidelines

### In Scope
- AI training and inference GPUs (data center grade)
- AI-specific accelerators (TPUs, Trainium, Gaudi, etc.)
- Cloud GPU pricing from providers with verified availability
- Networking and interconnect specifications for AI clusters
- MLPerf and other standardized benchmark results

### Out of Scope
- Consumer GPUs (gaming products)
- Unannounced or pre-release products
- Investment advice or purchasing recommendations
- Proprietary benchmarks that cannot be independently verified

---

## Code of Conduct

- Be respectful and constructive
- Focus on data accuracy, not vendor advocacy
- Disclose any conflicts of interest (e.g., if you work for a vendor whose data you're submitting)
- Do not submit marketing materials as technical data

---

## Recognition

All contributors are recognized in our commit history. Significant contributors may be listed in the README.

---

*Questions? Open an issue or reach out via GitHub Discussions.*
