# AI Networking & Interconnect Specifications

> Technical reference for GPU-to-GPU, node-to-node, and cluster-scale networking in AI infrastructure.
> Last verified: 2026-02-28

---

## GPU Interconnects

### NVLink Generations

| Generation | Bandwidth (Bidirectional) | Links per GPU | Total GPU BW | First Available | GPUs Supported |
|---|---|---|---|---|---|
| NVLink 1.0 | 40 GB/s per link | 4 | 160 GB/s | 2016 | P100 |
| NVLink 2.0 | 50 GB/s per link | 6 | 300 GB/s | 2017 | V100 |
| NVLink 3.0 | 50 GB/s per link | 12 | 600 GB/s | 2020 | A100 |
| NVLink 4.0 | 50 GB/s per link | 18 | 900 GB/s | 2022 | H100, H200 |
| NVLink 5.0 | 50 GB/s per link | 18 | 900 GB/s | 2024 | B100, B200, GB200 |

### NVSwitch Generations

| Generation | Ports | Per-Port BW | Total Switch BW | GPU Topology |
|---|---|---|---|---|
| NVSwitch 1.0 | 18 | 50 GB/s | 900 GB/s | DGX-2 (16 V100) |
| NVSwitch 2.0 | 36 | 50 GB/s | 1.8 TB/s | DGX A100 (8 A100) |
| NVSwitch 3.0 | 64 | 50 GB/s | 3.2 TB/s | DGX H100 (8 H100) |
| NVSwitch 4.0 | 64 | 100 GB/s | 6.4 TB/s | DGX B200, GB200 NVL72 |

### NVLink Topologies

| Platform | GPUs | NVLink Gen | All-to-All BW | NVSwitch |
|---|---|---|---|---|
| DGX H100 | 8x H100 | 4.0 | 900 GB/s per GPU | NVSwitch 3.0 |
| HGX H200 | 8x H200 | 4.0 | 900 GB/s per GPU | NVSwitch 3.0 |
| DGX B200 | 8x B200 | 5.0 | 900 GB/s per GPU | NVSwitch 4.0 |
| GB200 NVL72 | 72x B200 | 5.0 | 1.8 TB/s per GPU | NVSwitch 4.0 (2nd gen) |
| DGX GH200 | 256x GH200 | 4.0 (NVLink-C2C) | 900 GB/s per GPU | NVLink Switch |

---

## PCIe Interconnects

| Generation | Per-Lane BW | x16 Bandwidth | Encoding | First Available |
|---|---|---|---|---|
| PCIe 3.0 | 1 GB/s | 16 GB/s | 128b/130b | 2010 |
| PCIe 4.0 | 2 GB/s | 32 GB/s | 128b/130b | 2017 |
| PCIe 5.0 | 4 GB/s | 64 GB/s | 128b/130b | 2021 |
| PCIe 6.0 | 8 GB/s | 128 GB/s | PAM-4/1b/1b FLIT | 2024 |

### GPU PCIe Interface by Model

| GPU | PCIe Version | Max PCIe BW | Primary Interconnect |
|---|---|---|---|
| A100 PCIe | PCIe 4.0 x16 | 64 GB/s | PCIe |
| A100 SXM | PCIe 4.0 x16 | 64 GB/s | NVLink 3.0 (600 GB/s) |
| H100 PCIe | PCIe 5.0 x16 | 128 GB/s | PCIe |
| H100 SXM | PCIe 5.0 x16 | 128 GB/s | NVLink 4.0 (900 GB/s) |
| L40S | PCIe 4.0 x16 | 64 GB/s | PCIe only |

---

## Network Fabric — InfiniBand

### InfiniBand Data Rates

| Standard | Per-Lane Rate | 4x (Typical) | Effective BW (4x, bidirectional) | Year |
|---|---|---|---|---|
| SDR | 2.5 Gb/s | 10 Gb/s | 2 GB/s | 2004 |
| DDR | 5 Gb/s | 20 Gb/s | 4 GB/s | 2005 |
| QDR | 10 Gb/s | 40 Gb/s | 8 GB/s | 2008 |
| FDR | 14 Gb/s | 56 Gb/s | ~11 GB/s | 2011 |
| EDR | 25 Gb/s | 100 Gb/s | 24 GB/s | 2014 |
| HDR | 50 Gb/s | 200 Gb/s | 48 GB/s | 2018 |
| NDR | 100 Gb/s | 400 Gb/s | 96 GB/s | 2022 |
| XDR | 200 Gb/s | 800 Gb/s | 192 GB/s | 2025 |

### NVIDIA InfiniBand Products

| Product | Generation | Ports | Total Switch BW | Use Case |
|---|---|---|---|---|
| ConnectX-6 | HDR (200 Gb/s) | 1–2 | 200–400 Gb/s | A100 clusters |
| ConnectX-7 | NDR (400 Gb/s) | 1–2 | 400–800 Gb/s | H100/H200 clusters |
| ConnectX-8 | XDR (800 Gb/s) | 1–2 | 800–1600 Gb/s | B200/GB200 clusters |
| Quantum-2 (QM9700) | NDR | 64 | 51.2 Tb/s | Spine/leaf switches |
| Quantum-3 (QM9790) | XDR | 64 | 102.4 Tb/s | Next-gen fabric |

---

## Network Fabric — Ethernet

### RoCE (RDMA over Converged Ethernet)

| Speed | Standard | Typical Use |
|---|---|---|
| 100 GbE | 802.3ck | A100-era clusters |
| 200 GbE | 802.3ck | H100-era clusters |
| 400 GbE | 802.3bs/802.3ck | H100/H200 clusters |
| 800 GbE | 802.3df | B200/GB200 clusters |

### NVIDIA Ethernet Products (Spectrum)

| Product | Speed | Ports | Total Switch BW |
|---|---|---|---|
| Spectrum-3 (SN4000) | 400 GbE | 32 | 25.6 Tb/s |
| Spectrum-4 (SN5000) | 400/800 GbE | 64 | 51.2 Tb/s |

---

## Cluster Networking Topologies

### Typical AI Cluster Network Design

| Cluster Size | Intra-Node | Inter-Node Fabric | Topology | Total Bisection BW |
|---|---|---|---|---|
| 8 GPUs (1 node) | NVLink + NVSwitch | N/A | Fully connected | 7.2 TB/s (H100) |
| 64 GPUs (8 nodes) | NVLink + NVSwitch | 400G IB NDR | Fat-tree | ~25.6 TB/s |
| 256 GPUs (32 nodes) | NVLink + NVSwitch | 400G IB NDR | 2-tier fat-tree | ~51.2 TB/s |
| 1024 GPUs (128 nodes) | NVLink + NVSwitch | 400G IB NDR | 3-tier fat-tree | ~204.8 TB/s |
| 4096 GPUs (512 nodes) | NVLink + NVSwitch | 800G IB XDR | 3-tier fat-tree | ~819 TB/s |

### DGX SuperPOD Configurations

| Configuration | GPUs | Nodes | Network Fabric | Compute Performance |
|---|---|---|---|---|
| DGX H100 SuperPOD | 256 | 32 | NDR 400G IB | ~256 PFLOPS FP8 |
| DGX B200 SuperPOD | 576 | 72 (NVL72) | XDR 800G IB | ~1.4 EFLOPS FP4 |
| DGX GB200 NVL72 | 72 B200 + 36 Grace | 36 | NVLink 5.0 + XDR IB | ~720 PFLOPS FP4 |

---

## Scale-Up vs Scale-Out Comparison

| Aspect | Scale-Up (NVLink) | Scale-Out (IB/Ethernet) |
|---|---|---|
| Bandwidth | 900 GB/s per GPU | 50–100 GB/s per GPU |
| Latency | ~1–5 µs | ~1–5 µs (RDMA) |
| Max GPUs | 8 (HGX) / 72 (NVL72) | Thousands |
| Use Case | Tensor parallelism | Data/pipeline parallelism |
| Cost/GPU | Included in server | $2K–$5K additional |

---

## Memory Bandwidth vs Interconnect Bandwidth

| Component | Bandwidth | Relative to HBM3e |
|---|---|---|
| HBM3e (H200) | 4.8 TB/s | 1.0x |
| NVLink 4.0 (H100) | 900 GB/s | 0.19x |
| PCIe 5.0 x16 | 128 GB/s | 0.027x |
| NDR InfiniBand (400G) | 50 GB/s | 0.010x |
| 100 GbE | 12.5 GB/s | 0.003x |

This hierarchy illustrates why GPU memory bandwidth, NVLink, and high-speed fabric each play distinct roles in AI workload performance.

---

## Related Specifications

- [GPU Hardware Specifications](gpu-specifications.md) — Full GPU specs including memory bandwidth
- [AI Accelerators](ai-accelerators.md) — Non-GPU AI hardware with interconnect details
- [Cloud GPU Pricing](cloud-gpu-pricing.md) — Pricing across cloud providers

---

*Part of the [AI Infrastructure Index](https://github.com/alpha-one-index/ai-infra-index) — Maintained by [Alpha One Index](https://github.com/alpha-one-index)*
