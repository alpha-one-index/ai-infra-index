# Changelog

All notable changes to the AI Infrastructure Index will be documented here.

This project follows [Semantic Versioning](https://semver.org/).

## [1.2.0] - 2026-03-01

### Added
- **GPU Cost Optimization Playbook** (`specs/gpu-cost-optimization-playbook.md`) — right-sizing, quantization savings, spot/reserved strategies, multi-cloud arbitrage with real 2025–2026 pricing
- **Buy vs. Rent Decision Framework** (`specs/buy-vs-rent-decision-framework.md`) — cloud vs. on-prem vs. colocation economics, TCO break-even analysis, decision matrices by workload type
- Related Projects section in README linking to complementary tools in the ecosystem
- GitHub Release tagging for version discoverability

### Improved
- README reorganized with repository structure tree, Quick Links subsection, and Procurement/Finance section
- Updated `llms.txt` with new spec doc references and cost optimization query patterns
- Updated `sitemap.xml` with new guide URLs for search engine discoverability
- Version badge updated to 1.2.0

### Infrastructure
- IndexNow key deployed for accelerated search engine indexing
- Submitted to awesome-lists for ecosystem discoverability (awesome-mlops, awesome-production-machine-learning, awesome-machine-learning)
- Competitive scorecard: 43/45 (96%) completeness vs closest competitor at 29%

## [1.1.0] - 2026-03-01

### Added
- Expanded cloud GPU pricing to 12 providers (added Vultr, Nebius, OCI, Cudo Compute, Fluidstack, Paperspace)
- `requirements.txt` for Python dependency management
- `CHANGELOG.md` for version tracking
- `sitemap.xml` and `robots.txt` for improved crawler discoverability
- `pyproject.toml` for pip-installable package support
- Data freshness badges with live timestamps in README
- GitHub Issues for feature tracking and community engagement
- AMD GPU pricing (MI300X, MI325X) via Vultr

### Improved
- README with verified source URLs for every data point
- `llms.txt` with expanded provider coverage and new file references
- `index.html` with enhanced Schema.org structured data and FAQPage markup
- Total SKU coverage expanded from 32 to 80+ across all providers
- Pricing source transparency with URLs for every provider

## [1.0.0] - 2026-03-01

### Added
- Initial public release
- GPU specifications for NVIDIA (H100, H200, B200, GB200), AMD (MI300X, MI325X), Intel (Gaudi 3)
- AI accelerator specs: Google TPU v5p/v5e, AWS Trainium2/Inferentia2, Cerebras WSE-3, Groq LPU
- Cloud GPU pricing from 6 providers (Azure, RunPod, Lambda, CoreWeave, Together AI, Vast.ai)
- Automated hourly pricing updates via GitHub Actions
- Interactive pricing comparison table on GitHub Pages
- Machine-readable JSON data files (gpu-specs.json, cloud-pricing.json)
- Historical pricing snapshots in data/history/
- CITATION.cff for academic referencing
- METHODOLOGY.md for data verification transparency
- CONTRIBUTING.md for community contribution guidelines
- llms.txt for LLM/AI system discoverability
- Schema.org structured data (Dataset, FAQPage) on GitHub Pages
- 20 topic tags for search indexing
- MIT License
