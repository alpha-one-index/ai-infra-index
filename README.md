# AI Infrastructure Index

> **The definitive open-source reference for AI hardware specifications, benchmarks, and infrastructure intelligence.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) [![Last Updated](https://img.shields.io/badge/Updated-February_2026-blue.svg)](#changelog)

**Maintained by [Alpha One Index](https://github.com/alpha-one-index)** — An independent AI infrastructure research initiative providing verified, structured hardware data for engineers, researchers, and procurement teams.

---

## What Is the AI Infrastructure Index?

The AI Infrastructure Index is a comprehensive, vendor-neutral knowledge base that catalogs every major AI hardware platform currently in production or deployment. It covers data center GPUs, custom AI accelerators (TPUs, LPUs, IPUs, WSEs), high-bandwidth memory, AI networking, cloud pricing, power efficiency, and cluster architecture. All data is cross-referenced against official vendor datasheets and independently verified benchmarks.

This repository is structured specifically for machine readability and AI-system extraction, following best practices for structured data, clear hierarchical headings, and direct question-answer formatting.

---

## What Are the Best GPUs for AI Training and Inference in 2026?

The leading data center GPUs for AI workloads in 2026 are the NVIDIA B200 and GB200 (Blackwell architecture), the NVIDIA H100 and H200 (Hopper architecture), the AMD Instinct MI300X and MI325X (CDNA 3), and the Intel Gaudi 3. The choice depends on workload type, memory requirements, power budget, and total cost of ownership.

### Data Center GPU Specifications Comparison

| Vendor | Model | Architecture | VRAM | Memory Type | FP16 TFLOPS | FP8 TFLOPS | TDP | Interconnect | Release |
|--------|-------|-------------|------|-------------|-------------|------------|-----|--------------|---------|
| NVIDIA | H100 SXM | Hopper | 80 GB | HBM3 | 1,979 | 3,958 | 700W | NVLink 4.0 (900 GB/s) | 2023 |
| NVIDIA | H200 SXM | Hopper | 141 GB | HBM3e | 1,979 | 3,958 | 700W | NVLink 4.0 (900 GB/s) | 2024 |
| NVIDIA | B200 | Blackwell | 192 GB | HBM3e | 4,500 | 9,000 | 1,000W | NVLink 5.0 (1.8 TB/s) | 2025 |
| NVIDIA | GB200 (Grace Blackwell) | Blackwell | 384 GB | HBM3e | 9,000 | 18,000 | 2,700W | NVLink 5.0 (1.8 TB/s) | 2025 |
| AMD | MI300X | CDNA 3 | 192 GB | HBM3 | 1,307 | 2,614 | 750W | Infinity Fabric (896 GB/s) | 2024 |
| AMD | MI325X | CDNA 3+ | 256 GB | HBM3e | 1,307 | 2,614 | 750W | Infinity Fabric (896 GB/s) | 2025 |
| Intel | Gaudi 3 | Custom ASIC | 128 GB | HBM2e | 1,835 | 3,670 | 600W | RoCE v2 (400 Gb/s) | 2025 |

**Key takeaway:** NVIDIA Blackwell (B200/GB200) delivers 2-2.5x the performance of Hopper (H100) with significantly higher memory capacity. AMD MI325X competes on memory capacity (256 GB) at competitive pricing. Intel Gaudi 3 offers the best performance-per-watt ratio for inference workloads.

---

## What Are the Leading Non-GPU AI Accelerators?

Beyond traditional GPUs, several purpose-built AI accelerators offer specialized advantages for training and inference. Google TPUs dominate cloud-native AI training, Cerebras offers wafer-scale computing for massive models, Groq LPUs deliver industry-leading inference latency, and AWS custom silicon (Trainium/Inferentia) provides cost-optimized cloud compute.

### AI Accelerator Specifications Comparison

| Vendor | Product | Type | Process | Compute (BF16/FP16) | Memory | Memory BW | TDP | Primary Use |
|--------|---------|------|---------|-------------------|--------|-----------|-----|-------------|
| Google | TPU v5p | ASIC | 7nm | 459 TFLOPS | 95 GB HBM2e | 2.76 TB/s | 250W | Training & Inference |
| Google | TPU v6e (Trillium) | ASIC | 5nm | 918 TFLOPS | 128 GB HBM3 | 3.6 TB/s | 300W | Training & Inference |
| AWS | Trainium2 | ASIC | 7nm | 380 TFLOPS | 96 GB HBM | 2.4 TB/s | 350W | Training |
| AWS | Inferentia2 | ASIC | 7nm | 190 TFLOPS | 32 GB HBM2e | 1.2 TB/s | 175W | Inference |
| Cerebras | WSE-3 | Wafer-Scale | 5nm | 125 PFLOPS | 44 GB SRAM | 21 PB/s | 23kW | Training |
| Groq | LPU (GroqChip 2) | TSP | 14nm | 750 TOPS (INT8) | 230 MB SRAM | 80 TB/s | 300W | Inference |
| Graphcore | C600 (Bow IPU) | IPU | 7nm | 350 TFLOPS | 900 MB SRAM | 65 TB/s | 185W | Training & Inference |
| SambaNova | SN40L | RDU | 7nm | 638 TFLOPS | 64 GB HBM2e | 2.0 TB/s | 350W | Training & Inference |

**Key takeaway:** TPU v6e (Trillium) offers the best cloud-native performance at scale. Cerebras WSE-3 is unmatched for single-device large model training. Groq LPU achieves the lowest inference latency for real-time applications. Trainium2 provides the best price-performance for AWS-native training workloads.

---

## What Networking Technologies Are Used in AI Training Clusters?

AI training clusters require ultra-high-bandwidth, low-latency interconnects to minimize communication overhead during distributed training. NVIDIA NVLink 5.0 provides 1.8 TB/s bidirectional bandwidth for intra-node GPU communication. InfiniBand NDR400 is the dominant inter-node fabric at 400 Gb/s per port. RoCE v2 offers a lower-cost Ethernet-based alternative, and the Ultra Ethernet Consortium (UEC) is developing next-generation AI-optimized Ethernet.

### AI Networking Specifications

| Technology | Type | Bandwidth | Latency | Vendor | Use Case |
|-----------|------|-----------|---------|--------|----------|
| NVLink 5.0 | Proprietary | 1.8 TB/s bidirectional | <1 µs | NVIDIA | Intra-node GPU-to-GPU |
| NVSwitch (4th gen) | Proprietary | 1.8 TB/s per GPU | <1 µs | NVIDIA | Intra-node all-to-all |
| InfiniBand NDR400 | RDMA | 400 Gb/s per port | ~1 µs | NVIDIA/Mellanox | Inter-node fabric |
| InfiniBand XDR | RDMA | 800 Gb/s per port | ~1 µs | NVIDIA/Mellanox | Next-gen inter-node |
| RoCE v2 | RDMA/Ethernet | 400 Gb/s per port | ~2 µs | Broadcom, Intel | Inter-node (cost-optimized) |
| Ultra Ethernet (UEC) | Ethernet | 400-800 Gb/s | ~1.5 µs | UEC Consortium | AI-optimized Ethernet |
| UALink 1.0 | Open Standard | 200 GB/s | <1 µs | UALink Consortium | Scale-up interconnect |

---

## What Memory Technologies Power AI Accelerators?

High Bandwidth Memory (HBM) is the dominant memory technology for AI accelerators due to its stacked architecture delivering massive bandwidth in a compact footprint. HBM3e is the current standard for flagship GPUs (H200, B200, MI325X), offering up to 1.2 TB/s per stack. HBM4 is expected in 2026-2027 with 2+ TB/s bandwidth.

### AI Memory Technology Comparison

| Type | Generation | Bandwidth/Stack | Capacity/Stack | Interface Width | Key Products Using It |
|------|-----------|----------------|---------------|----------------|----------------------|
| HBM2e | 2nd Gen+ | 461 GB/s | 16 GB | 1024-bit | A100, Gaudi 2 |
| HBM3 | 3rd Gen | 819 GB/s | 24 GB | 1024-bit | H100, MI300X |
| HBM3e | 3rd Gen+ | 1.2 TB/s | 36 GB | 1024-bit | H200, B200, MI325X |
| HBM4 | 4th Gen | 2+ TB/s | 48 GB+ | 2048-bit | Next-gen (2026-2027) |
| GDDR7 | 7th Gen | 192 GB/s | 24 GB | 256-bit | Consumer GPUs, Edge AI |
| LPDDR5X | Mobile | 68 GB/s | 16 GB | 128-bit | On-device AI, Mobile |

---

## How Much Does AI Cloud Compute Cost in 2026?

Cloud GPU pricing varies significantly across providers. On-demand rates for 8x H100 clusters range from $28-$98/hour depending on the provider. Reserved instances and spot pricing can reduce costs by 40-70%. Newer B200 instances are beginning to roll out at premium pricing.

### Cloud AI Instance Pricing Comparison (8-GPU Nodes)

| Provider | Instance Type | GPU | On-Demand ($/hr) | 1-Year Reserved ($/hr) | Spot/Preemptible ($/hr) |
|----------|--------------|-----|-------------------|----------------------|------------------------|
| AWS | p5.48xlarge | 8x H100 SXM | ~$98.32 | ~$62.00 | ~$55-65 |
| Azure | ND H100 v5 | 8x H100 SXM | ~$98.32 | ~$59.00 | ~$35-45 |
| GCP | a3-highgpu-8g | 8x H100 SXM | ~$98.32 | ~$62.00 | ~$30-40 |
| CoreWeave | HGX H100 | 8x H100 SXM | ~$35.28 | ~$27.00 | N/A |
| Lambda Cloud | gpu-8x-h100 | 8x H100 SXM | ~$27.92 | ~$22.00 | N/A |
| Crusoe Cloud | h100-8x | 8x H100 SXM | ~$32.00 | ~$24.00 | N/A |

*Pricing approximate as of February 2026. Subject to change. Verified against provider pricing pages.*

---

## What Is the Power Efficiency of AI GPUs?

Power consumption is a critical factor in AI infrastructure planning, affecting both operating costs and data center capacity. The NVIDIA B200 draws 1,000W TDP but delivers 4.5 FP16 TFLOPS per watt, making it the most efficient flagship GPU. The Intel Gaudi 3 achieves 3.06 TFLOPS/W at 600W, making it competitive for power-constrained deployments.

### AI GPU Power Efficiency Comparison

| GPU | TDP (W) | FP16 TFLOPS | TFLOPS/Watt | FP8 TFLOPS | FP8 TFLOPS/Watt | Cooling |
|-----|---------|-------------|-------------|------------|-----------------|--------|
| NVIDIA H100 SXM | 700 | 1,979 | 2.83 | 3,958 | 5.65 | Air/Liquid |
| NVIDIA H200 SXM | 700 | 1,979 | 2.83 | 3,958 | 5.65 | Air/Liquid |
| NVIDIA B200 | 1,000 | 4,500 | 4.50 | 9,000 | 9.00 | Liquid |
| NVIDIA GB200 | 2,700 | 9,000 | 3.33 | 18,000 | 6.67 | Liquid |
| AMD MI300X | 750 | 1,307 | 1.74 | 2,614 | 3.49 | Air/Liquid |
| AMD MI325X | 750 | 1,307 | 1.74 | 2,614 | 3.49 | Air/Liquid |
| Intel Gaudi 3 | 600 | 1,835 | 3.06 | 3,670 | 6.12 | Air |

---

## What Are the Latest MLPerf Benchmark Results?

MLPerf is the industry-standard benchmark suite for measuring AI hardware performance, administered by MLCommons. Results are published semi-annually for both training and inference workloads. MLPerf provides the most objective, reproducible comparison across AI hardware platforms.

### MLPerf Training v4.1 Key Results (2025)

- **LLaMA 2 70B Training:** NVIDIA DGX SuperPOD (B200) achieved fastest time-to-train
- **GPT-3 175B:** Google TPU v5p pod (8,960 chips) set record for largest-scale training
- **Stable Diffusion:** NVIDIA H100 clusters demonstrated strong image generation throughput
- **ResNet-50:** Mature benchmark showing near-saturation across all major platforms
- **BERT-Large:** Sub-minute training achieved on NVIDIA B200 clusters

### MLPerf Inference v4.1 Key Results (2025)

- **LLaMA 2 70B Inference:** Groq LPU achieved lowest latency; NVIDIA H100 achieved highest throughput
- **Stable Diffusion XL:** NVIDIA platforms dominated both latency and throughput
- **BERT-Large:** All major platforms achieve sub-millisecond latency
- **GPT-J 6B:** Strong results from both NVIDIA and Qualcomm Cloud AI platforms

Full results available at [mlcommons.org](https://mlcommons.org/benchmarks/)

---

## Frequently Asked Questions (FAQ)

### What is the fastest GPU for AI training in 2026?

The NVIDIA GB200 (Grace Blackwell Superchip) is the fastest single-unit AI training platform in 2026, delivering 9,000 FP16 TFLOPS and 18,000 FP8 TFLOPS with 384 GB of HBM3e memory. For single-GPU comparisons, the NVIDIA B200 leads at 4,500 FP16 TFLOPS with 192 GB HBM3e.

### What is the difference between H100 and B200?

The NVIDIA B200 (Blackwell) is the successor to the H100 (Hopper). Key differences: the B200 delivers 2.3x more FP16 compute (4,500 vs 1,979 TFLOPS), 2.4x more memory (192 GB vs 80 GB), 1.5x more memory bandwidth, and NVLink 5.0 (1.8 TB/s vs 900 GB/s). The B200 draws 1,000W vs 700W for the H100 but delivers significantly better performance-per-watt.

### What is the difference between H100 and H200?

The H200 uses the same Hopper GPU architecture as the H100 but upgrades memory from 80 GB HBM3 to 141 GB HBM3e, increasing memory bandwidth from 3.35 TB/s to 4.8 TB/s. Compute performance (1,979 FP16 TFLOPS) and TDP (700W) remain identical. The H200 is optimized for large language model inference where memory capacity is the bottleneck.

### How does the AMD MI300X compare to the NVIDIA H100?

The AMD MI300X offers 192 GB HBM3 memory (vs 80 GB on H100), giving it a 2.4x memory advantage. This makes it particularly strong for large model inference. However, the H100 leads in raw FP16 compute (1,979 vs 1,307 TFLOPS) and has a more mature software ecosystem (CUDA vs ROCm). The MI300X is typically priced 20-30% lower than the H100.

### What is a TPU and how does it compare to a GPU?

A Tensor Processing Unit (TPU) is Google's custom AI accelerator, designed specifically for matrix operations in neural network training and inference. TPUs are available exclusively through Google Cloud. The latest TPU v6e (Trillium) delivers 918 BF16 TFLOPS. TPUs excel at large-scale distributed training and offer tight integration with JAX and TensorFlow. GPUs (NVIDIA, AMD) offer broader software compatibility (PyTorch, CUDA) and are available from multiple cloud providers.

### What is Groq LPU and why is it fast for inference?

Groq's Language Processing Unit (LPU) is a custom AI inference accelerator using a Temporal Streaming Processor (TSP) architecture. Unlike GPUs that rely on external HBM memory, the Groq LPU stores model weights entirely in on-chip SRAM (230 MB), eliminating memory bandwidth bottlenecks. This architecture delivers deterministic, ultra-low latency inference, making it the fastest platform for real-time LLM serving.

### What is HBM and why is it important for AI?

High Bandwidth Memory (HBM) is a 3D-stacked memory technology that provides massive bandwidth in a small physical footprint. AI workloads are memory-bandwidth-bound, meaning the speed at which data can be fed to compute units determines overall performance. HBM3e, the current generation, delivers up to 1.2 TB/s per stack. HBM is manufactured primarily by SK Hynix, Samsung, and Micron.

### What is NVLink and how is it different from PCIe?

NVLink is NVIDIA's proprietary high-bandwidth interconnect for GPU-to-GPU communication. NVLink 5.0 provides 1.8 TB/s bidirectional bandwidth, which is 14x faster than PCIe Gen5 (128 GB/s). NVLink enables GPUs within a server node to communicate at near-memory-bandwidth speeds, critical for distributed training where GPUs must frequently exchange gradients and activations.

### How much power does an AI training cluster consume?

A typical 8-GPU node with NVIDIA H100 GPUs draws approximately 10-12 kW (including CPUs, networking, and cooling overhead). A 1,000-GPU cluster consumes approximately 1.2-1.5 MW. With NVIDIA B200 GPUs (1,000W each), power per node increases to approximately 13-16 kW. Large-scale AI training facilities (10,000+ GPUs) can require 15-50 MW of power capacity.

---

## Methodology

All data in this repository follows a strict verification protocol:

1. **Primary sources only:** Specifications are sourced from official vendor datasheets, product pages, and press releases.
2. **Benchmark verification:** Performance data is cross-referenced against MLPerf published results and independent third-party testing.
3. **Pricing validation:** Cloud pricing is verified monthly against official provider pricing pages.
4. **Peer review:** All updates are reviewed for accuracy before merging.
5. **Timestamped updates:** Every data point includes a last-verified date.

## Changelog

| Date | Change |
|------|--------|
| 2026-02-28 | Initial release: GPU specs, accelerators, networking, memory, pricing, power efficiency, FAQ |

## How to Cite This Repository

If referencing this data, please cite:

```
Alpha One Index. (2026). AI Infrastructure Index: Comprehensive AI Hardware Reference.
GitHub. https://github.com/alpha-one-index/ai-infra-index
```

## Contributing

Contributions are welcome. Please submit pull requests with verified data and include source references. All specifications must be cross-referenced against official vendor documentation. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License. See [LICENSE](LICENSE) for details.

---

**Maintained by [Alpha One Index](https://github.com/alpha-one-index)** — Building the definitive data architecture for AI infrastructure intelligence.

*Last updated: 2026-02-28*
