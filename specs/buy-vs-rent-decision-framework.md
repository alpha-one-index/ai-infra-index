# Buy vs. Rent GPU Infrastructure: Decision Framework for AI Teams

> **The only open-source buy vs. rent GPU decision framework with real 2025–2026 TCO data.** No other repository provides this analysis.
>
> Part of the [AI Infrastructure Index](../README.md) — an independent, vendor-neutral reference maintained by [Alpha One Index](https://github.com/alpha-one-index).
>
> **Last updated:** March 2026 | **Applies to:** H100/H200 generation and forward  
> **Cross-references:** [`gpu-cost-optimization-playbook.md`](./gpu-cost-optimization-playbook.md) · [`cloud-gpu-pricing.md`](./cloud-gpu-pricing.md) · [`model-gpu-sizing.md`](./model-gpu-sizing.md) · [`training-costs.md`](./training-costs.md)

---

## Table of Contents

1. [The Decision Framework Overview](#1-the-decision-framework-overview)
2. [Cloud GPU Economics (Rent)](#2-cloud-gpu-economics-rent)
3. [On-Premise Economics (Buy)](#3-on-premise-economics-buy)
4. [Colocation Economics (Middle Ground)](#4-colocation-economics-middle-ground)
5. [Break-Even Analysis](#5-break-even-analysis)
6. [Decision Matrix by Use Case](#6-decision-matrix-by-use-case)
7. [Migration Triggers](#7-migration-triggers)
8. [5-Minute Decision Checklist](#8-5-minute-decision-checklist)

---

## 1. The Decision Framework Overview

### Should I Buy or Rent GPUs for AI Training?

The honest answer: **it depends on utilization, time horizon, and team maturity** — but the math strongly favors on-premise at sustained high utilization and strongly favors cloud at low or unpredictable utilization. The threshold is sharper than most teams expect.

This framework gives you the tools to run the calculation for your specific situation, grounded in real 2025–2026 market data.

### What Are the Three Infrastructure Paths?

| Path | Description | Best for |
|------|-------------|----------|
| **Cloud (Rent)** | Pay per GPU-hour with no capital outlay | Variable workloads, early-stage teams, burst capacity |
| **On-Premise (Buy)** | Own the hardware, run in your own data center or office | High utilization (>60%), large teams, data-sensitive workloads |
| **Colocation (Hybrid)** | Own the hardware, rent the facility | Predictable workloads, no facility expertise, cost optimization without cloud markup |

### Decision Tree

```
Is your GPU utilization predictable and sustained?
├── NO → Cloud (on-demand or spot)
└── YES → Will you need this for 12+ months?
    ├── NO → Cloud (reserved instances)
    └── YES → Do you have >60% average daily utilization?
        ├── NO → Cloud reserved or colocation
        └── YES → Do you have data sovereignty or compliance requirements?
            ├── YES → On-premise or colocation
            └── NO → Do you have facility infrastructure + ops team?
                ├── YES → On-premise
                └── NO → Colocation
```

### Key Variables That Drive the Decision

These six variables determine the outcome of your build-vs-buy analysis. Rank yourself on each before proceeding:

| Variable | Favors Cloud | Favors On-Prem |
|----------|-------------|----------------|
| **Daily GPU utilization** | < 50% | > 70% |
| **Planning horizon** | < 12 months | > 24 months |
| **Workload predictability** | Highly variable / bursty | Steady and predictable |
| **Team infrastructure maturity** | No dedicated infra team | Experienced ML platform team |
| **Data sensitivity** | Low (public data) | High (PII, proprietary, regulated) |
| **Capital availability** | Capital-constrained | Capital available for CapEx |

### Quick Reference: When to Choose Each Path

**Choose Cloud when:**
- You're running experiments, R&D, or proof-of-concept work
- GPU utilization is below 50% on average
- You need to scale up/down rapidly (e.g., new model training runs, product launches)
- Your team has fewer than 5 people working on ML infrastructure
- You need access to the latest hardware (H200, B200) before on-prem procurement is viable
- You're in the first 12–18 months of building an AI product

**Choose On-Premise when:**
- GPU utilization consistently exceeds 70%
- You have a 24+ month planning horizon with predictable workloads
- Data sovereignty, latency, or compliance requirements rule out cloud
- You're running large-scale pretraining with 50B+ parameter models continuously
- Your annual cloud GPU bill exceeds $1M and is growing predictably

**Choose Colocation when:**
- You want on-prem economics without building out your own facility
- You're in a leased office or building without data-center-grade power/cooling
- You want to own hardware but keep capital in compute, not facilities
- Your team can manage hardware remotely (most modern server vendors support IPMI/BMC)

---

## 2. Cloud GPU Economics (Rent)

### What Does It Actually Cost to Rent an H100 in 2025–2026?

The GPU cloud market went through a fundamental repricing cycle in 2025. After peak scarcity pricing hit $8–$10/hr in late 2024, [AWS cut H100 prices by ~44% in June 2025](https://www.datacenterdynamics.com/), and the entry of 300+ new cloud providers drove market-rate H100 pricing to $2.85–$3.50/hr on-demand by Q3–Q4 2025, with a provider profitability floor estimated at ~$1.65/hr. Prices are expected to stabilize at $2.75–$3.25/hr through 2026 before Blackwell-era GPU supply further pressures H100 rates.

**H100 Price Timeline:**

| Period | On-Demand Price/GPU-hr | Notes |
|--------|----------------------|-------|
| Q4 2024 | $8.00–$10.00 | Peak scarcity; major providers, limited supply |
| Q1 2025 | $5.50–$7.00 | Initial supply improvements |
| Q2 2025 | $3.50–$4.50 | AWS 44% price cut triggers market-wide repricing |
| Q3–Q4 2025 | $2.85–$3.50 | Market stabilization; 300+ providers competing |
| 2026 projected | $2.75–$3.25 | Stabilization; upward pressure from DRAM shortage |

Sources: [Introl GPU Cloud Price Collapse report (Jan 2026)](https://introl.com/blog/gpu-cloud-price-collapse-h100-market-december-2025), [Intuition Labs H100 Rental Comparison (Nov 2025)](https://intuitionlabs.ai/pdfs/h100-rental-prices-a-cloud-cost-comparison-nov-2025.pdf), [Jarvislabs H100 Price Guide (Jan 2026)](https://docs.jarvislabs.ai/blog/h100-price)

### On-Demand vs. Spot vs. Reserved: Full Pricing Comparison

**Per-GPU-Hour Rates (H100 80GB SXM), Q4 2025:**

| Provider | On-Demand | Spot / Preemptible | 1-yr Reserved | Notes |
|----------|-----------|-------------------|---------------|-------|
| AWS EC2 (p5.48xlarge) | ~$3.90–$4.10 | ~$2.50 | ~$2.80–$3.00 | After June 2025 price cut; 8-GPU instance = $33–$34/hr total |
| Google Cloud (A3-highgpu) | ~$3.00 | ~$2.25 | ~$2.10–$2.40 | GCP spot often cheapest among hyperscalers |
| Microsoft Azure (ND H100 v5) | ~$3.50–$5.00 | ~$2.00–$2.50 | ~$2.50–$3.50 | Pricing less transparent; varies by region |
| Oracle Cloud (OCI) | Competitive | N/A | Aggressive (bulk) | Aggressive pricing; primary DGX Cloud host |
| CoreWeave | ~$1.50–$3.50 | ~$1.50–$2.00 | ~$1.50–$2.00 | GPU-dense clusters; best for AI/ML-only workloads |
| Lambda Labs | ~$2.40–$2.99 | ~$1.70–$2.00 | ~$1.85–$1.89 | Transparent pricing; research-friendly |
| RunPod (Community) | ~$2.30 | ~$1.70–$1.99 | ~$2.00–$2.30 | Community cloud; lower SLA |
| DataCrunch | ~$1.99 | Dynamic pricing | ~$1.80 | Dynamic spot model; strong value |

Sources: [ComputePrices.com market share report (Dec 2025)](https://computeprices.com/blog/cloud-gpu-providers-market-share), [Intuition Labs pricing guide (Nov 2025)](https://intuitionlabs.ai/pdfs/h100-rental-prices-a-cloud-cost-comparison-nov-2025.pdf), [GMI Cloud comparison (2025)](https://www.gmicloud.ai/blog/2025-gpu-cloud-cost-comparison)

**Key pricing dynamics:**
- **Spot/preemptible** instances are 40–60% cheaper but can be interrupted with little notice; suitable for checkpointed training jobs
- **1-year reserved** locks in ~30–40% discount vs. on-demand; requires predictable demand
- **3-year reserved** extends that to ~45–55% off but introduces significant technology risk as new GPU generations arrive every 18–24 months
- **Provider profitability floor** is estimated at ~$1.65/hr for H100 ([Introl, Jan 2026](https://introl.com/blog/gpu-cloud-price-collapse-h100-market-december-2025)); prices below this are promotional or loss-leaders

### Total Cloud Cost Formula

The sticker GPU price is only part of your cloud bill. Calculate your true cloud cost as:

```
Total Monthly Cloud Cost =
  (GPU-hrs/month × on-demand $/hr)
  + (storage_GB × $0.023/GB/month)       # S3/GCS standard storage
  + (egress_GB × $0.085–$0.12/GB)        # internet egress
  + (inter-region transfer × $0.02/GB)   # cross-region data movement
  + (managed services overhead × 10–20%) # if using SageMaker, Vertex AI, etc.
```

**Egress pricing by hyperscaler (2025):**

| Provider | First 10 TB/month | 10–50 TB/month | Notes |
|----------|------------------|----------------|-------|
| AWS | $0.09/GB | $0.085/GB | First 100 GB free |
| Azure | $0.087/GB | $0.083/GB | First 100 GB free |
| GCP | $0.12/GB | $0.11/GB | Calculated in GiB |
| Oracle Cloud | $0.0085/GB | $0.0085/GB | 10 TB free tier |

Sources: [US Signal egress pricing guide (Jun 2025)](https://ussignal.com/blog/understanding-egress-charges/), [WZ-IT egress comparison (Dec 2025)](https://wz-it.com/en/blog/public-internet-egress-costs-comparison-aws-azure-gcp-hetzner/)

> **Warning:** [Gartner estimates egress fees represent 10–15% of total cloud costs](https://www.cloudoptimo.com/blog/the-true-cost-of-cloud-data-egress-and-how-to-manage-it/) for compute-heavy organizations. For AI teams transferring large model checkpoints and datasets, this can exceed $10K/month at scale.

**Hidden cost example — 8x H100 training cluster running 16 hrs/day:**

| Cost Component | Monthly | Annualized |
|----------------|---------|------------|
| GPU compute (on-demand, $3.10/hr) | $36,024 | $432,288 |
| Storage: 100TB training data (S3) | $2,300 | $27,600 |
| Egress: 50TB model/checkpoint transfers | $4,250 | $51,000 |
| Managed service overhead (10%) | $3,602 | $43,226 |
| **Total** | **$46,176** | **$554,114** |

### Cloud Advantages

- **Zero CapEx:** No upfront hardware cost; expense is fully OpEx
- **Instant scaling:** Provision additional GPUs in minutes; pay only for what you use
- **No maintenance burden:** Hardware failures, firmware updates, and cooling are the provider's problem
- **Technology flexibility:** Switch to H200 or Blackwell B200 without a procurement cycle
- **Global reach:** Deploy close to users or data sources in any region
- **Built-in redundancy:** Enterprise SLAs with 99.9%+ uptime

---

## 3. On-Premise Economics (Buy)

### What Does a Full On-Prem 8x H100 Setup Actually Cost?

The Lenovo 2025 TCO study provides the most authoritative public reference point: a [ThinkSystem SR675 V3 with 8x H100 NVL 94GB PCIe Gen5 GPUs carries a total system cost of ~$833,806 (no sales discounts)](https://lenovopress.lenovo.com/lp2225.pdf). This is the full server system price — it does not include facility costs, networking, storage, or the operations team.

**Complete Hardware Cost Breakdown — 8x H100 Cluster:**

| Component | Low Estimate | High Estimate | Notes |
|-----------|-------------|---------------|-------|
| 8x H100 80GB SXM GPUs | $216,000 | $320,000 | $27K–$40K per GPU; SXM5 commands premium |
| Server chassis + CPUs + RAM | $40,000 | $80,000 | Dual AMD EPYC or Intel Xeon; 512GB–2TB RAM |
| NVMe storage (local, fast) | $15,000 | $40,000 | 20–100TB NVMe for training data/checkpoints |
| High-speed networking (InfiniBand/400GbE) | $20,000 | $50,000 | InfiniBand HDR/NDR per node; switch shared |
| Power infrastructure (PDUs, UPS) | $10,000 | $30,000 | Per rack; amortized across cluster |
| Rack and cabling | $5,000 | $10,000 | Per rack |
| **Total Hardware (8x H100 node)** | **~$306,000** | **~$530,000** | Lenovo SR675 V3 list: ~$834K with full config |

Sources: [GMI Cloud H100 cost analysis (2025)](https://www.gmicloud.ai/blog/nvidia-h100-gpu-cost-2025-buy-vs-rent-for-data-centers), [Intuition Labs pricing guide (Feb 2026)](https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide), [Lenovo TCO study (May 2025)](https://lenovopress.lenovo.com/lp2225.pdf)

### Operating Cost Formula: Power

Power is the largest ongoing operational cost. Use this formula:

```
Hourly Power Cost =
  (GPU_count × GPU_TDP_kW × PUE × electricity_rate_$/kWh)
  + (server_overhead_kW × PUE × electricity_rate_$/kWh)

For 8x H100 at 700W TDP each, PUE 1.4, $0.10/kWh:
  = (8 × 0.7 × 1.4 × 0.10) + (2.0 × 1.4 × 0.10)
  = $0.784/hr + $0.280/hr
  = ~$1.06/hr (full server power)
```

**PUE explained:** Power Usage Effectiveness = total facility power / IT equipment power. A PUE of 1.0 is perfect; real data centers range from 1.2 (modern hyperscale) to 1.6 (older facilities). Typical enterprise/colo facilities run 1.3–1.5.

**Electricity cost by region (commercial rates, 2025):**

| Region | $/kWh | Impact on 8x H100 node (annual, 24/7) |
|--------|-------|---------------------------------------|
| Pacific Northwest (hydro) | $0.04–$0.06 | ~$16,000–$24,000/yr |
| Texas (ERCOT) | $0.06–$0.09 | ~$24,000–$36,000/yr |
| US National Average | $0.08–$0.12 | ~$32,000–$48,000/yr |
| Northeast US / California | $0.12–$0.18 | ~$48,000–$72,000/yr |
| Europe (varies) | $0.10–$0.30 | ~$40,000–$120,000/yr |

Source: [Aterio data center power analysis (Jan 2025)](https://www.aterio.io/blog/how-much-power-would-a-data-center-with-30-000-gpus-consume-in-a-year), [TRG Datacenters H100 power guide (Jan 2026)](https://www.trgdatacenters.com/resource/nvidia-h100-power-consumption/)

### Complete 3-Year and 5-Year TCO Model (8x H100 Node)

Based on [Lenovo's 2025 TCO study](https://lenovopress.lenovo.com/lp2225.pdf), with on-prem hourly operational cost of **~$0.87/hr** (power + cooling + maintenance at $0.15/kWh):

| Cost Item | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
|-----------|--------|--------|--------|--------|--------|
| Hardware (amortized) | $250,000 | — | — | — | — |
| Power & cooling ($0.87/hr × 8,760 hrs) | $7,621 | $7,621 | $7,621 | $7,621 | $7,621 |
| Maintenance contracts (1% HW/yr) | $3,000 | $5,000 | $5,000 | $5,000 | $5,000 |
| IT staff allocation (0.25 FTE @ $200K) | $50,000 | $50,000 | $50,000 | $50,000 | $50,000 |
| Network/storage operating costs | $8,000 | $8,000 | $8,000 | $8,000 | $8,000 |
| **Annual Total** | **$318,621** | **$70,621** | **$70,621** | **$70,621** | **$70,621** |
| **Cumulative Total** | $318,621 | $389,242 | $459,863 | $530,484 | $601,105 |

> **Note:** Lenovo's full SR675 V3 system cost is $833,806. The figures above use a conservative all-in hardware estimate of $250K for a single 8-GPU node with power infrastructure. Teams building multi-node clusters achieve some per-node economies of scale on networking and facility costs.

**Cloud equivalent cost (AWS p5.48xlarge, on-demand at $98.32/hr, 24/7 operation):**

| Year | Cloud Cost | Cumulative |
|------|-----------|------------|
| Year 1 | $861,283 | $861,283 |
| Year 2 | $861,283 | $1,722,566 |
| Year 3 | $861,283 | $2,583,849 |
| Year 4 | $861,283 | $3,445,132 |
| Year 5 | $861,283 | $4,306,415 |

**5-year savings with on-prem vs. on-demand cloud: ~$3.7M per 8-GPU node at 100% utilization.** Even at 50% utilization and 1-year AWS reserved pricing ($77.43/hr), on-prem saves ~$1.5M over 5 years.

Source: [Lenovo GenAI TCO 2025 Edition](https://lenovopress.lenovo.com/lp2225.pdf)

### Depreciation Schedule (MACRS 5-Year for GPUs)

GPU servers are classified as **5-year property** under [IRS MACRS guidelines](https://www.irs.gov/faqs/sale-or-trade-of-business-depreciation-rentals/depreciation-recapture/depreciation-recapture) (computer hardware). The double-declining balance method front-loads deductions:

| Year | MACRS % | Deduction on $250K hardware | Cumulative Deducted |
|------|---------|----------------------------|---------------------|
| 1 | 20.00% | $50,000 | $50,000 |
| 2 | 32.00% | $80,000 | $130,000 |
| 3 | 19.20% | $48,000 | $178,000 |
| 4 | 11.52% | $28,800 | $206,800 |
| 5 | 11.52% | $28,800 | $235,600 |
| 6 | 5.76% | $14,400 | $250,000 |

> **Bonus depreciation (2025+):** Under the [Tax Cuts and Jobs Act as extended](https://www.irs.gov/faqs/sale-or-trade-of-business-depreciation-rentals/depreciation-recapture/depreciation-recapture), qualified property acquired after January 19, 2025 is eligible for **100% first-year bonus depreciation**. This means a $250K GPU server can generate a $250K deduction in Year 1. For a business in the 21% corporate tax bracket, that's a ~$52,500 immediate tax benefit — effectively reducing the net hardware cost.

### Residual Value Estimation

GPU hardware depreciates rapidly due to rapid technology cycles. Historical market data suggests:

| Age | Residual Value (% of purchase price) | Notes |
|-----|--------------------------------------|-------|
| 6 months | 75–85% | H100 market still liquid |
| 12 months | 60–70% | New generation announced |
| 18 months | 45–60% | Newer GPUs entering market |
| 24 months | 30–45% | Next gen widely available |
| 36 months | 20–35% | H100 becomes "previous gen" |
| 48–60 months | 10–20% | Book value only; limited resale |

Source: [Jarvislabs H100 price guide (Jan 2026)](https://docs.jarvislabs.ai/blog/h100-price), [GMI Cloud H100 analysis (2025)](https://www.gmicloud.ai/blog/how-much-does-the-nvidia-h100-gpu-cost-in-2025-buy-vs-rent-analysis)

> New GPU generations arrive every **18–24 months**. Plan your depreciation and refresh cycles around this reality. An H100 purchased in 2024 will compete against B200/B300 Blackwell GPUs by 2026–2027, significantly compressing residual value.

---

## 4. Colocation Economics (Middle Ground)

### When Does Colocation Make Sense?

Colocation — owning your hardware but housing it in a third-party data center — hits a cost sweet spot for teams that:
- Want on-prem economics but lack data-center-grade power, cooling, or physical space
- Run predictable workloads with high utilization (>60%)
- Have hardware procurement expertise but not facilities management expertise
- Are located in regions where commercial electricity is expensive (build out in a low-cost power region)

Colocation eliminates the 80–95% cloud markup you pay for managed infrastructure, while avoiding the multi-million-dollar capital expenditure of building or leasing your own facility.

### Colo Cost Structure

Your monthly colocation bill has four components:

```
Monthly Colo Cost =
  rack/cabinet space
  + power (kW committed × $/kW/month)
  + bandwidth (Mbps or 95th percentile)
  + remote hands / managed services (optional)
```

### Typical Colocation Pricing Tiers (2025)

| Tier | Space | Power | Monthly Cost | Best for |
|------|-------|-------|-------------|----------|
| Per-U (small) | 1–4U | 0.5–2 kW | $200–$600/mo | Single GPU server, dev/test |
| Half cabinet | 10–20U | 2–5 kW | $600–$1,200/mo | Small cluster (2–4 GPUs) |
| Full cabinet (standard) | 42U | 5–10 kW | $1,000–$2,500/mo | 1–2 GPU servers |
| Full cabinet (high-density) | 42U | 10–20 kW | $2,500–$5,000/mo | 4–8 GPU servers |
| Private cage | Custom | 20–100+ kW | $150–$300/kW/mo | Large clusters (16+ GPUs) |
| Wholesale (1MW+) | Full hall | 500kW–10MW | $80–$150/kW/mo | Hyperscale / infra companies |

> **Power pricing is the dominant variable.** An 8x H100 server draws ~6–8 kW under full load (8 × 700W GPU + ~800W system overhead). At a typical [colo rate of $150–$300/kW/month](https://cyfuture.cloud/kb/data-centers/get-the-real-data-center-colocation-pricing-in-2025-market), that's $900–$2,400/month just for power — on top of space charges.

**Typical monthly colo cost for one 8x H100 node:**

| Cost Item | Low | High | Notes |
|-----------|-----|------|-------|
| Cabinet space (shared, 10U) | $400 | $800 | Partial cabinet |
| Power (8 kW × $150–$300/kW) | $1,200 | $2,400 | Committed allocation |
| Bandwidth (1Gbps port, 10TB) | $200 | $500 | Metered or burstable |
| Remote hands (2 hrs/month) | $100 | $300 | Emergency intervention |
| **Total Monthly** | **~$1,900** | **~$4,000** | |
| **Annualized** | **~$22,800** | **~$48,000** | |

**Compare to cloud equivalent:**  
AWS p5.48xlarge (8x H100) at $98.32/hr × 8,760 hrs = **$861,283/year** at full utilization.  
Colo operating cost: **~$35,000/year** — a **96% reduction** in operating costs vs. hyperscaler on-demand.

Sources: [Reddit datacenter thread on GPU colo in Texas (Dec 2025)](https://www.reddit.com/r/datacenter/comments/1ppukd8/what_should_i_expect_to_pay_for_colocating_an_8x/), [Cyfuture colo pricing guide (Jan 2026)](https://cyfuture.cloud/kb/data-centers/get-the-real-data-center-colocation-pricing-in-2025-market), [LightWave Networks GPU colo guide (Jan 2026)](https://www.lightwavenetworks.com/blog/gpu-colocation/)

### Colo vs. Cloud vs. Full On-Prem: Quick Comparison

| Factor | Cloud | Colocation | Full On-Prem |
|--------|-------|------------|-------------|
| Upfront CapEx | $0 | $250K–$500K (hardware) | $250K–$1M+ (hardware + facility) |
| Monthly OpEx (8x H100, 24/7) | $70K–$85K | $2K–$4K | $600–$1,200 |
| Lead time to first GPU | Minutes | 4–8 weeks (procurement) | 4–8 months (procurement + facility) |
| Hardware ownership | No | Yes | Yes |
| Facility ownership | No | No | Yes |
| Scaling flexibility | High | Moderate (space/power limits) | Low (fixed capacity) |
| Data sovereignty | Provider-controlled | Full control | Full control |
| Infra team required | No | Partial (remote mgmt) | Yes (on-site or on-call) |

---

## 5. Break-Even Analysis

### When Does Buying GPUs Break Even With Renting?

The canonical reference point is the [Lenovo 2025 GenAI TCO study](https://lenovopress.lenovo.com/lp2225.pdf), which compares a ThinkSystem SR675 V3 (8x H100) against AWS p5.48xlarge at $98.32/hr:

```
Cloud hourly cost:     $98.32
On-prem hourly cost:   $0.87 (power + cooling + maintenance)
On-prem hardware:      $833,806

Break-even:
  98.32 × H = 0.87 × H + 833,806
  H = 833,806 / (98.32 - 0.87)
  H ≈ 8,556 hours  →  11.9 months at 100% utilization
```

**This is the most important number in this document.** At 100% utilization, owning an 8x H100 server breaks even with on-demand cloud in under 12 months. Every hour after that is pure savings.

> Note: The Lenovo study uses $98.32/hr for AWS p5.48xlarge (pre-June 2025 cut). Post-cut pricing is ~$33–$34/hr. The updated break-even at $33/hr is: 833,806 / (33 - 0.87) ≈ **25,942 hours or ~35 months** at 100% utilization. The right answer depends on your specific cloud pricing. Use the formula with your actual rates.

### Break-Even by Daily Usage Hours (Lenovo SR675 V3, 8x H100)

Using real-world cloud pricing at both on-demand ($98.32/hr, pre-cut) and current post-cut rates ($33/hr), with hardware at $833,806:

| Daily GPU Usage | Hours/Year | On-demand break-even | Post-cut ($33/hr) break-even |
|----------------|-----------|---------------------|------------------------------|
| 4 hrs/day | 1,460 | 5.9 years | Not reached in 5 years |
| 8 hrs/day | 2,920 | 2.9 years | Not reached in 5 years |
| 12 hrs/day | 4,380 | 1.96 years | ~4.8 years |
| 16 hrs/day | 5,840 | 1.47 years | ~3.6 years |
| 24 hrs/day (100%) | 8,760 | 11.9 months | ~2.9 years |

> **Key insight:** At current market rates (~$33/hr for 8x H100 on-demand), you need at least 12+ hours/day sustained utilization to break even within a 5-year hardware lifecycle. Cloud becomes more competitive as spot and reserved pricing compresses the on-demand rate — but on-prem still wins at high utilization.

**Lenovo study break-even variants by AWS pricing tier:**

| AWS Pricing | Hourly Rate | Break-even |
|-------------|------------|------------|
| On-demand | $98.32/hr | ~8,556 hours (~12 months) |
| 1-year reserved | $77.43/hr | ~10,890 hours (~15 months) |
| 3-year reserved | $53.95/hr | ~15,710 hours (~22 months) |

Source: [Lenovo GenAI TCO 2025 Edition](https://lenovopress.lenovo.com/lp2225.pdf)

### Sensitivity Analysis

How key variables shift the break-even point (holding other variables constant at baseline):

**Effect of electricity cost on annual on-prem operating cost (8x H100, 24/7):**

| Electricity Rate | Annual Power Cost | Impact vs. $0.10/kWh baseline |
|-----------------|------------------|-------------------------------|
| $0.05/kWh | $16,800 | −$9,100/yr |
| $0.08/kWh | $26,880 | −$0/yr (similar to baseline) |
| $0.10/kWh | $33,600 | Baseline |
| $0.12/kWh | $40,320 | +$6,720/yr |
| $0.15/kWh | $50,400 | +$16,800/yr |

Formula: `8 GPUs × 700W × PUE(1.4) × $/kWh × 8,760 hrs/yr`

**Effect of GPU utilization on effective hourly on-prem cost (hardware amortized over 3 years):**

| Utilization | Effective On-prem $/hr | Cloud on-demand break-even |
|-------------|----------------------|---------------------------|
| 30% | $10.70 | Never (cloud wins) |
| 50% | $6.42 | Marginal |
| 70% | $4.59 | Likely on-prem wins |
| 85% | $3.78 | On-prem wins |
| 100% | $3.21 | On-prem wins clearly |

*Effective on-prem $/hr = (hardware cost / (utilization × lifecycle hours)) + power & maintenance*

**Effect of cloud price changes:**

| Scenario | Cloud Rate | On-prem advantage |
|----------|-----------|-------------------|
| Cloud prices rise 20% (DRAM shortage) | $3.96/hr/GPU | Strengthened |
| Current market | $3.30/hr/GPU | Moderate |
| Cloud prices fall 30% | $2.31/hr/GPU | Weakened; re-evaluate |
| Cloud at provider floor | $1.65/hr/GPU | On-prem advantage minimal at <80% utilization |

> **Note:** A [2025 DRAM shortage triggered by OpenAI's wafer procurement](https://www.softwareseni.com/understanding-the-2025-dram-shortage-and-its-impact-on-cloud-infrastructure-costs/) has pushed server costs up 15–25%, and OVH Cloud CEO has predicted 5–10% cloud price increases between April–September 2026. This modestly favors on-prem purchases in 2025 vs. waiting.

### Cumulative Cost Trajectory: Cloud vs. On-Prem Over 36 Months

*8x H100 cluster at 100% utilization, on-demand $98.32/hr (Lenovo baseline):*

```
Month  Cloud ($98.32/hr)    On-Prem ($833K HW + $0.87/hr)
  1        $72,760               $834,452  ← Hardware purchase
  3       $218,279               $835,350
  6       $436,558               $836,899
 12       $873,115               $839,995
 18     $1,309,673               $843,091  ← Cross-over: cloud > on-prem
 24     $1,746,230               $846,188
 36     $2,619,346               $852,380

36-month savings with on-prem: ~$1.77M per 8-GPU node (at 100% utilization)
```

---

## 6. Decision Matrix by Use Case

### Which Workload Belongs Where?

| Workload Type | Recommended Infrastructure | Pricing Tier | Rationale |
|--------------|--------------------------|-------------|-----------|
| R&D / experimentation | Cloud on-demand | $2.85–$3.50/hr/GPU | Irregular; spin up/down; no commitment |
| Hyperparameter search | Cloud spot | $1.70–$2.50/hr/GPU | Checkpointable; interruption tolerant |
| Model fine-tuning (infrequent) | Cloud spot or reserved | $1.85–$2.50/hr/GPU | Predictable duration; cost-sensitive |
| LLM pretraining (large-scale) | On-prem or colocation | See Section 3/4 | High utilization; months-long runs |
| Production inference (steady traffic) | On-prem, colo, or reserved cloud | $1.90–$2.10/hr reserved | Predictable; 24/7; latency-sensitive |
| Burst inference (product launch) | Cloud on-demand | $2.85–$3.50/hr/GPU | Short duration; unpredictable |
| Data preprocessing / ETL | CPU cloud or on-prem CPU | Minimal GPU needed | GPUs often wasteful here |
| Multi-modal training (images + text) | On-prem or colo | — | Data I/O intensive; egress costly in cloud |
| Federated learning | On-prem per site | — | Data locality requirements |
| CI/CD model testing | Cloud spot | $1.70–$2.00/hr | Short jobs; interruption OK |

### Team Size and Maturity Considerations

| Team Profile | Recommended Path | Key Constraint |
|-------------|-----------------|----------------|
| ≤5 people, seed/Series A | Cloud only | No infra bandwidth |
| 5–20 people, Series B | Cloud + consider colo for steady workloads | Limited infra team |
| 20–50 people, Series C+ | Colo for baseline + cloud for burst | Justifiable capital |
| 50+ people, enterprise | On-prem for baseline + cloud for burst | Can support ops team |
| Research lab (university) | Cloud or colo (grant-funded, episodic) | CapEx restrictions |
| Enterprise ML platform | Hybrid (on-prem + cloud burst) | Multi-team coordination |

### Data Sovereignty and Compliance

| Requirement | Viable Paths | Notes |
|------------|-------------|-------|
| HIPAA (PHI data) | On-prem, colo, or compliant cloud (BAA required) | AWS/Azure/GCP offer HIPAA BAAs |
| SOC 2 Type II | All paths | Cloud providers certified; on-prem requires your own audit |
| GDPR (EU data residency) | EU-region cloud, EU colo, or EU on-prem | Data cannot leave EU |
| FedRAMP / GovCloud | AWS GovCloud, Azure Government, GCP FedRAMP only | Limited cloud options |
| Export controls (ITAR/EAR) | On-prem preferred; restricted cloud regions | Model weights may be controlled |
| Proprietary model weights | On-prem or colo strongly preferred | Cloud provider access risk |
| Air-gapped environment | On-prem only | No cloud path |

### Geographic Considerations

| Factor | Cloud Advantage | On-Prem / Colo Advantage |
|--------|----------------|--------------------------|
| Low-latency inference (global users) | Multi-region deployment | Single location, adds CDN complexity |
| Low electricity cost | Irrelevant (built in) | Sites in PNW, Texas, Iceland, Norway: $0.03–$0.07/kWh |
| Disaster recovery | Built-in multi-AZ | Requires second colo site |
| Talent proximity | N/A | Need local infra staff |
| Data residency | Regional cloud availability | Full control |

---

## 7. Migration Triggers

### When Should I Move from Cloud to On-Prem?

Treat these as threshold-based signals. If three or more are true simultaneously, initiate a migration evaluation:

**Green-light signals (move toward on-prem / colo):**
- [ ] GPU utilization consistently **>70%** over the past 90 days
- [ ] Cloud GPU spend **>$50K/month** and growing predictably
- [ ] Workloads are **predictable** with defined daily/weekly patterns
- [ ] Planning horizon is **12+ months** with no major architecture pivots expected
- [ ] You have or are building a **dedicated ML platform team** (2+ engineers)
- [ ] **Data egress costs** exceed $5K/month (large model checkpoints, dataset transfers)
- [ ] **Compliance or data sovereignty** requirements are creating cloud complexity
- [ ] Cloud provider **availability constraints** are delaying training runs

**Quantitative migration trigger:**  
When your **annualized cloud GPU bill exceeds the break-even-adjusted hardware cost by >20%**, migration economics are clearly favorable. Example: $1.2M cloud spend/year on 8x H100 capacity → hardware costs ~$834K → break-even in <12 months at your utilization level.

### When Should I Move from On-Prem to Cloud?

**Red-flag signals (move toward cloud):**
- [ ] GPU utilization drops **below 30%** consistently (paying for idle hardware)
- [ ] You need to **rapidly scale** from 8 to 64 GPUs in < 30 days (procurement delay)
- [ ] The **next GPU generation** (B200/B300) would provide a 3x+ performance advantage for your workload
- [ ] Your **infra team is leaving** and you can't backfill quickly
- [ ] **Facility lease expiration** or power constraint limits expansion
- [ ] A **business pivot** changes your GPU workload profile significantly
- [ ] On-prem hardware is **>3 years old** and failing at increasing rates

### Hybrid Architecture Patterns

Most mature AI teams end up at a hybrid model. Common architectures:

**Pattern 1: On-Prem Baseline + Cloud Burst**
- Run steady-state training and inference on owned hardware
- Burst to cloud for peak demand (model launches, research sprints)
- Trigger: on-prem queue wait time > 4 hours for a batch job
- Tools: Kubernetes federation, [Slurm](https://slurm.schedmd.com/) with cloud bursting plugins

**Pattern 2: Colo for Training + Cloud for Inference**
- Heavy pretraining on colo hardware (economics favor ownership)
- Serve inference in cloud (latency, global reach, auto-scaling)
- Model weights synchronized via object storage

**Pattern 3: Multi-Cloud for Resilience**
- Primary workloads on one cloud provider (negotiated reserved pricing)
- Secondary provider as failover + price hedge
- Prevents single-vendor rate lock after 1-year reserved commitments expire

**Pattern 4: Cloud for R&D + Colo for Production**
- Experimentation and team onboarding in cloud (no infra overhead)
- Proven workloads migrated to colo as they stabilize
- Clear migration criteria: 60+ days of consistent usage at >70% utilization

### Cost of Switching

Migration is not free. Budget these when evaluating a switch:

| Migration Type | One-Time Costs | Ongoing Changes |
|---------------|---------------|-----------------|
| Cloud → On-Prem | Data transfer egress ($0.085–$0.12/GB), hardware procurement (4–8 month lead time), facility buildout or colo contract | Infra team headcount (+1–2 FTE); reduced cloud bill |
| Cloud → Colo | Hardware procurement + egress transfer | Colo monthly fees; hardware maintenance |
| On-Prem → Cloud | Data transfer to cloud (ingress free; egress from old DC variable), re-architecture for cloud APIs, testing | Cloud subscription vs. hardware depreciation |
| Cloud A → Cloud B | Egress from source cloud ($0.085–$0.12/GB per provider), re-deployment and testing, reserved instance write-off | May negotiate reserved contract exit |

**Data transfer cost estimate:**  
Moving 1 PB of model weights and training data from AWS:  
`1,000,000 GB × $0.085 = $85,000` just in egress fees, plus transfer time and bandwidth

> Rule of thumb: **Budget 3–6 months of current cloud spend for migration costs** when switching from cloud to on-prem. The ROI is typically recovered within the first year of on-prem operation at >70% utilization.

---

## 8. 5-Minute Decision Checklist

Answer Yes/No to each question. Count your answers.

### Section A: Utilization and Duration

- [ ] **A1.** My GPU utilization will exceed 70% on average for the next 12+ months
- [ ] **A2.** My workloads are predictable in schedule and scale (not research/exploratory)
- [ ] **A3.** I have a defined workload running for 12+ months with no major architecture changes expected
- [ ] **A4.** I am spending or will spend >$50,000/month on cloud GPU compute

### Section B: Team and Organization

- [ ] **B1.** I have (or will hire) at least 1–2 dedicated infrastructure/ML platform engineers
- [ ] **B2.** My organization can commit capital expenditure of $500K–$1M+ without threatening other priorities
- [ ] **B3.** I have access to appropriate physical space, power (≥10kW available), and cooling

### Section C: Data and Compliance

- [ ] **C1.** My data has sovereignty, privacy, or regulatory requirements that restrict cloud placement
- [ ] **C2.** My model weights or training data are proprietary and I'm uncomfortable with third-party access risk
- [ ] **C3.** Data egress fees are a significant line item (>$5K/month) in my current cloud bill

### Section D: Technology and Risk

- [ ] **D1.** I do NOT need the absolute latest GPU generation immediately (I can work with H100/H200 for 2–3 years)
- [ ] **D2.** I have a disaster recovery plan that doesn't depend on cloud geographic redundancy
- [ ] **D3.** Hardware failures and maintenance windows are acceptable (with proper planning)

---

### How to Interpret Your Score

**Score: 10–13 YES answers → Strong case for On-Premise or Colocation**  
Run the break-even formula in Section 5 with your specific numbers. The math almost certainly favors ownership. Consider colocation if you answered NO to B3.

**Score: 6–9 YES answers → Evaluate Colocation or Hybrid**  
You have some on-prem-favorable signals but not a clean case for full ownership. Colocation likely hits the optimal cost point. Model the 3-year TCO from Section 3 with your actual utilization.

**Score: 3–5 YES answers → Cloud Reserved or Cloud + Colo**  
Commit to 1-year reserved instances for your baseline workload to capture 30–40% discounts. Evaluate colocation only for the most stable, high-utilization portion of your workload.

**Score: 0–2 YES answers → Cloud On-Demand or Spot**  
Your utilization pattern, team maturity, or planning horizon doesn't justify ownership. Optimize your cloud spend with spot instances for interruptible jobs and on-demand for production. Revisit this checklist in 6–12 months.

---

### Quick Formula for Your Situation

Before finalizing your decision, plug in your actual numbers:

```python
# GPU Buy vs. Rent Break-Even Calculator

# Your inputs
cloud_hourly_rate     = 3.10      # $/hr per GPU (on-demand or reserved)
gpu_count             = 8         # number of GPUs in cluster
hardware_cost         = 250000    # total hardware cost ($)
power_cost_per_hour   = 0.87      # $/hr (power + cooling + maintenance)
daily_usage_hours     = 16        # hours/day you'll actually use it

# Calculations
cloud_hourly_cluster  = cloud_hourly_rate * gpu_count
onprem_hourly         = power_cost_per_hour
annual_usage_hours    = daily_usage_hours * 365

# Break-even in hours
break_even_hours      = hardware_cost / (cloud_hourly_cluster - onprem_hourly)
break_even_months     = break_even_hours / annual_usage_hours * 12

print(f"Break-even: {break_even_hours:,.0f} hours = {break_even_months:.1f} months")
print(f"3-year cloud cost: ${cloud_hourly_cluster * annual_usage_hours * 3:,.0f}")
print(f"3-year on-prem cost: ${hardware_cost + onprem_hourly * annual_usage_hours * 3:,.0f}")
```

---

## Key Sources and Further Reading

| Resource | Description | Link |
|----------|-------------|------|
| Lenovo GenAI TCO 2025 Edition | Authoritative on-prem vs. cloud TCO study with H100/H200/L40S | [lenovopress.lenovo.com/lp2225.pdf](https://lenovopress.lenovo.com/lp2225.pdf) |
| Introl GPU Cloud Price Collapse | H100 cloud pricing history and provider floor analysis | [introl.com/blog](https://introl.com/blog/gpu-cloud-price-collapse-h100-market-december-2025) |
| Intuition Labs H100 Rental Comparison | Provider-by-provider pricing breakdown (Nov 2025) | [intuitionlabs.ai](https://intuitionlabs.ai/pdfs/h100-rental-prices-a-cloud-cost-comparison-nov-2025.pdf) |
| ComputePrices.com | Real-time H100 pricing across 31 providers | [computeprices.com](https://computeprices.com/blog/cloud-gpu-providers-market-share) |
| GMI Cloud H100 Cost Analysis | Buy vs. rent analysis with provider context | [gmicloud.ai](https://www.gmicloud.ai/blog/nvidia-h100-gpu-cost-2025-buy-vs-rent-for-data-centers) |
| TRG Datacenters H100 Power Guide | H100 TDP, cooling, and power infrastructure | [trgdatacenters.com](https://www.trgdatacenters.com/resource/nvidia-h100-power-consumption/) |
| IRS MACRS Depreciation | Computer hardware depreciation rules | [irs.gov](https://www.irs.gov/faqs/sale-or-trade-of-business-depreciation-rentals/depreciation-recapture/depreciation-recapture) |
| US Signal Egress Guide | Cloud egress pricing comparison (2025) | [ussignal.com](https://ussignal.com/blog/understanding-egress-charges/) |
| SoftwareSeni DRAM Shortage Analysis | Supply chain risk factors for 2026 cloud pricing | [softwareseni.com](https://www.softwareseni.com/understanding-the-2025-dram-shortage-and-its-impact-on-cloud-infrastructure-costs/) |

---

*This document is part of the [ai-infra-index](../README.md) open-source reference. Contributions and corrections welcome via pull request. Data reflects market conditions as of Q1 2026 and should be re-validated annually.*
