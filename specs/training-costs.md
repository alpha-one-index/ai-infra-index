# AI Model Training Cost Index

> Comprehensive cost analysis for training and fine-tuning AI models at scale. Includes compute, energy, storage, and total cost of ownership estimates.

## Foundation Model Training Costs (Historical)

| Model | Org | Year | GPUs | GPU-Hours | Compute Cost |
|-------|-----|------|------|-----------|-------------|
| GPT-3 175B | OpenAI | 2020 | 10K A100s | ~3.1M | ~$4.6M |
| GPT-4 (est.) | OpenAI | 2023 | ~25K A100s | ~50M | ~$63M |
| LLaMA 2 70B | Meta | 2023 | 2K A100s | ~1.7M | ~$2.1M |
| LLaMA 3 70B | Meta | 2024 | 16K H100s | ~6.4M | ~$7.7M |
| LLaMA 3 405B | Meta | 2024 | 16K H100s | ~30.8M | ~$37M |
| Falcon 180B | TII | 2023 | 4K A100s | ~7.5M | ~$9M |
| Mistral 7B | Mistral | 2023 | 512 H100s | ~200K | ~$240K |
| Mixtral 8x7B | Mistral | 2023 | 512 H100s | ~600K | ~$720K |
| Claude 3 Opus (est.) | Anthropic | 2024 | ~30K H100s | ~60M | ~$72M |
| Gemini Ultra (est.) | Google | 2023 | ~32K TPUv4 | ~80M | ~$200M |
| DeepSeek V3 | DeepSeek | 2024 | 2K H800s | ~2.7M | ~$5.5M |
| DeepSeek R1 | DeepSeek | 2025 | 2K H800s | ~2.7M | ~$5.5M |

> Note: Costs are estimates based on public disclosures and compute estimates. Actual costs vary significantly based on negotiated contracts, energy costs, and cluster efficiency.

## Training Cost Calculator

### Formula

```
Total Compute Cost = GPU_Hours x Hourly_GPU_Rate

GPU_Hours = (6 x Parameters x Tokens) / (GPU_FLOPS x MFU x 3600)

Where:
  Parameters = model parameter count
  Tokens     = training tokens
  GPU_FLOPS  = GPU peak FLOPS (BF16)
  MFU        = Model FLOP Utilization (typically 0.35-0.55)
  3600       = seconds per hour
```

### Reference GPU FLOPS (BF16 Tensor Core)

| GPU | BF16 TFLOPS | Typical MFU |
|-----|------------|-------------|
| NVIDIA H100 SXM | 989 | 0.45-0.55 |
| NVIDIA H200 SXM | 989 | 0.45-0.55 |
| NVIDIA B200 SXM | 2,250 | 0.50-0.60 |
| NVIDIA A100 80GB SXM | 312 | 0.35-0.45 |
| NVIDIA A100 40GB SXM | 312 | 0.35-0.45 |
| AMD MI300X | 1,307 | 0.40-0.50 |
| Intel Gaudi 3 | 1,835 | 0.35-0.45 |

### Example Calculations

**Training a 7B model on 1T tokens with H100s:**
```
GPU_Hours = (6 x 7e9 x 1e12) / (989e12 x 0.45 x 3600)
          = 42e21 / (1,600,038e12)
          = 26,249 GPU-Hours

With 256 H100s: 26,249 / 256 = 102 hours (~4.3 days)
Cost at $98.32/hr (AWS p5): 256 x 102 x $98.32 = ~$2.57M
```

**Fine-tuning LLaMA 3 8B on 10B tokens:**
```
GPU_Hours = (6 x 8e9 x 10e9) / (989e12 x 0.45 x 3600)
          = 480e18 / (1,600,038e12)
          = 300 GPU-Hours

With 8 H100s: 300 / 8 = 37.5 hours (~1.6 days)
Cost at $98.32/hr (AWS p5): 8 x 37.5 x $98.32 = ~$29.5K
```

## Training Run Estimates by Scale

### Small Scale (Research / Startup)

| Model Size | Tokens | GPUs | Duration | Cost (H100 on-demand) |
|-----------|--------|------|----------|----------------------|
| 1B | 100B | 8 | ~8 hrs | ~$6.3K |
| 7B | 200B | 32 | ~2.5 days | ~$197K |
| 7B | 1T | 64 | ~10 days | ~$1.5M |
| 13B | 500B | 64 | ~5.5 days | ~$1.7M |

### Mid Scale (Well-funded Startup / Enterprise)

| Model Size | Tokens | GPUs | Duration | Cost (H100 reserved 1yr) |
|-----------|--------|------|----------|-------------------------|
| 34B | 1T | 256 | ~11 days | ~$5.3M |
| 70B | 1T | 512 | ~14 days | ~$13.4M |
| 70B | 2T | 512 | ~28 days | ~$26.7M |
| 120B | 1T | 512 | ~23 days | ~$22M |

### Large Scale (Hyperscaler / Major AI Lab)

| Model Size | Tokens | GPUs | Duration | Estimated Total Cost |
|-----------|--------|------|----------|--------------------|
| 175B | 1T | 2,048 | ~20 days | ~$50M |
| 405B | 15T | 16,384 | ~25 days | ~$400M |
| 1T+ | 15T+ | 32,768+ | ~60 days | ~$1B+ |

## Fine-Tuning Cost Guide

### Instruction Tuning

| Base Model | Dataset Size | Method | GPUs | Duration | Cost |
|-----------|-------------|--------|------|----------|------|
| LLaMA 3 8B | 50K examples | Full FT | 8x H100 | ~3 hrs | ~$2.4K |
| LLaMA 3 8B | 1M examples | Full FT | 8x H100 | ~2 days | ~$38K |
| LLaMA 3 70B | 50K examples | Full FT | 64x H100 | ~4 hrs | ~$25K |
| LLaMA 3 70B | 1M examples | Full FT | 64x H100 | ~3 days | ~$450K |
| LLaMA 3 405B | 50K examples | Full FT | 256x H100 | ~8 hrs | ~$200K |

### RLHF / DPO Training

| Base Model | Comparison Pairs | Method | GPUs | Duration | Cost |
|-----------|-----------------|--------|------|----------|------|
| 7B | 100K | DPO | 8x H100 | ~12 hrs | ~$9.4K |
| 7B | 100K | PPO | 16x H100 | ~2 days | ~$75K |
| 70B | 100K | DPO | 32x H100 | ~1.5 days | ~$150K |
| 70B | 100K | PPO | 64x H100 | ~5 days | ~$990K |

### Parameter-Efficient Fine-Tuning (PEFT)

| Base Model | Dataset | Method | GPUs | Duration | Cost |
|-----------|---------|--------|------|----------|------|
| LLaMA 3 8B | 50K examples | QLoRA | 1x A100 40GB | ~6 hrs | ~$9.7 |
| LLaMA 3 8B | 1M examples | QLoRA | 2x A100 80GB | ~18 hrs | ~$58 |
| LLaMA 3 70B | 50K examples | QLoRA | 2x H100 80GB | ~8 hrs | ~$196 |
| LLaMA 3 70B | 1M examples | QLoRA | 4x H100 80GB | ~3 days | ~$3.5K |

## Total Cost of Ownership (TCO)

### Beyond Compute: Full Cost Breakdown

| Category | % of Total Cost | Notes |
|----------|----------------|-------|
| GPU Compute | 60-75% | Largest cost driver |
| Data collection & cleaning | 10-20% | Often underestimated |
| Energy (on-prem) | 5-10% | $0.06-0.12/kWh typical |
| Engineering labor | 5-15% | ML engineers, infra |
| Storage & networking | 2-5% | Checkpoints, datasets |
| Evaluation & iteration | 5-10% | Multiple training runs |

### Energy Consumption

| GPU | TDP (W) | 8-GPU Node TDP | 1K GPU Hours Energy |
|-----|---------|----------------|--------------------|
| H100 SXM | 700W | ~8 kW | ~8 MWh |
| H200 SXM | 700W | ~8 kW | ~8 MWh |
| B200 SXM | 1,000W | ~11 kW | ~11 MWh |
| A100 SXM | 400W | ~4.5 kW | ~4.5 MWh |
| MI300X | 750W | ~8.5 kW | ~8.5 MWh |

**Energy cost for 1M H100 GPU-hours:**
- Energy consumed: ~700 MWh
- At $0.08/kWh: ~$56,000 (electricity only)
- Note: Represents ~1-5% of total on-demand compute cost

## Cloud vs On-Premise Breakeven Analysis

### Assumptions
- H100 SXM server (8-GPU): $300,000 purchase
- 3-year amortization
- Power: $0.08/kWh, PUE: 1.3
- 85% utilization
- Staff: 0.5 FTE per rack

| GPUs | Monthly Cloud (on-demand) | Monthly Cloud (reserved) | Monthly On-Prem TCO | Breakeven (on-prem vs reserved) |
|------|--------------------------|--------------------------|--------------------|---------------------------------|
| 8 | ~$57,000 | ~$35,000 | ~$12,000 | ~3 months |
| 64 | ~$455,000 | ~$282,000 | ~$78,000 | ~3.5 months |
| 512 | ~$3.64M | ~$2.25M | ~$580,000 | ~4 months |
| 4,096 | ~$29M | ~$18M | ~$4.3M | ~4 months |

> On-premise is significantly cheaper at scale (>64 GPUs) if utilization stays above 70%. Cloud wins for variable workloads and getting started.

## Price Trends

### H100 Training Cost per Token (1T token training run)

| Date | H100 On-Demand $/hr | Approx Cost/1B tokens |
|------|---------------------|----------------------|
| Q1 2023 | $40+ (scarce) | ~$5,200 |
| Q3 2023 | $32-$36 | ~$4,200 |
| Q1 2024 | $28-$32 | ~$3,700 |
| Q3 2024 | $26-$30 | ~$3,300 |
| Q1 2025 | $24-$27 | ~$3,000 |
| Q1 2026 | $22-$25 | ~$2,700 |

> Trend: H100 prices have fallen ~40% from peak scarcity pricing, driven by increased supply and B200/H200 availability.

---

*Last updated: February 2026*
*Methodology: Compute estimates use Chinchilla scaling law GPU-hour formula. Cloud prices from public APIs. On-prem TCO from industry benchmarks.*
*See [model-gpu-sizing.md](model-gpu-sizing.md) for memory requirements and [cloud-gpu-pricing.md](cloud-gpu-pricing.md) for current pricing.*
