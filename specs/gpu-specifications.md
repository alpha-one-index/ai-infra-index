# AI Data Center GPU Specifications

> Comprehensive specifications for every major AI training and inference GPU currently in production. All data verified against official vendor datasheets.

*Last updated: February 2026 | Maintained by [Alpha One Index](https://github.com/alpha-one-index/ai-infra-index)*

---

## What Are the Best GPUs for AI Training?

The leading GPUs for AI training in 2025 are NVIDIA B200, NVIDIA H200, NVIDIA H100, and AMD MI300X. Selection depends on workload size, memory requirements, and budget constraints.

## NVIDIA Data Center GPUs

### What are NVIDIA B200 specifications?

| Specification | Value |
|---|---|
| GPU Architecture | Blackwell |
| Process Node | TSMC 4NP |
| GPU Memory | 192 GB HBM3e |
| Memory Bandwidth | 8 TB/s |
| FP64 Performance | 40 TFLOPS |
| FP32 Performance | 80 TFLOPS |
| FP16 / BF16 Performance | 2,250 TFLOPS |
| FP8 / FP4 Performance | 4,500 / 9,000 TFLOPS |
| TDP | 1,000W |
| Interconnect | NVLink 5.0 (1,800 GB/s) |
| Form Factor | SXM |
| Availability | 2025 |

### What are NVIDIA H200 specifications?

| Specification | Value |
|---|---|
| GPU Architecture | Hopper |
| Process Node | TSMC 4N |
| GPU Memory | 141 GB HBM3e |
| Memory Bandwidth | 4.8 TB/s |
| FP16 / BF16 Performance | 989 TFLOPS |
| FP8 Performance | 1,979 TFLOPS |
| TDP | 700W |
| Interconnect | NVLink 4.0 (900 GB/s) |
| Form Factor | SXM |

### What are NVIDIA H100 SXM specifications?

| Specification | Value |
|---|---|
| GPU Architecture | Hopper |
| Process Node | TSMC 4N |
| GPU Memory | 80 GB HBM3 |
| Memory Bandwidth | 3.35 TB/s |
| FP64 Performance | 34 TFLOPS |
| FP32 Performance | 67 TFLOPS |
| FP16 / BF16 Performance | 989 TFLOPS |
| FP8 Performance | 1,979 TFLOPS |
| TDP | 700W |
| Interconnect | NVLink 4.0 (900 GB/s) |
| PCIe | Gen 5.0 x16 |

### What are NVIDIA H100 PCIe specifications?

| Specification | Value |
|---|---|
| GPU Architecture | Hopper |
| GPU Memory | 80 GB HBM3 |
| Memory Bandwidth | 2.0 TB/s |
| FP16 / BF16 Performance | 756 TFLOPS |
| TDP | 350W |
| Interconnect | PCIe Gen 5.0 x16 |
| NVLink | Optional NVLink Bridge (600 GB/s) |

### What are NVIDIA A100 specifications?

| Specification | Value |
|---|---|
| GPU Architecture | Ampere |
| Process Node | TSMC 7N |
| GPU Memory | 80 GB HBM2e (SXM) / 40 or 80 GB (PCIe) |
| Memory Bandwidth | 2.0 TB/s (SXM) / 1.6-2.0 TB/s (PCIe) |
| FP16 / BF16 Performance | 312 TFLOPS |
| TF32 Performance | 156 TFLOPS |
| TDP | 400W (SXM) / 300W (PCIe) |
| Interconnect | NVLink 3.0 (600 GB/s) |

---

## AMD Data Center GPUs

### What are AMD MI300X specifications?

| Specification | Value |
|---|---|
| GPU Architecture | CDNA 3 |
| Process Node | TSMC 5nm + 6nm |
| GPU Memory | 192 GB HBM3 |
| Memory Bandwidth | 5.3 TB/s |
| FP16 Performance | 1,307 TFLOPS |
| FP8 Performance | 2,615 TFLOPS |
| TDP | 750W |
| Interconnect | Infinity Fabric (896 GB/s) |
| Chiplet Design | 8 XCDs + 4 IODs |

### What are AMD MI250X specifications?

| Specification | Value |
|---|---|
| GPU Architecture | CDNA 2 |
| GPU Memory | 128 GB HBM2e |
| Memory Bandwidth | 3.2 TB/s |
| FP16 Performance | 383 TFLOPS |
| TDP | 560W |
| Interconnect | Infinity Fabric |

---

## Intel Data Center GPUs

### What are Intel Gaudi 3 specifications?

| Specification | Value |
|---|---|
| Architecture | Gaudi 3 |
| Process Node | TSMC 5nm |
| Memory | 128 GB HBM2e |
| Memory Bandwidth | 3.7 TB/s |
| BF16 Performance | 1,835 TFLOPS |
| FP8 Performance | 3,670 TFLOPS |
| TDP | 900W |
| Networking | 24x 200GbE RoCE |

### What are Intel Gaudi 2 specifications?

| Specification | Value |
|---|---|
| Architecture | Gaudi 2 |
| Memory | 96 GB HBM2e |
| Memory Bandwidth | 2.45 TB/s |
| BF16 Performance | 432 TFLOPS |
| FP8 Performance | 865 TFLOPS |
| TDP | 600W |
| Networking | 24x 100GbE RoCE |

---

## GPU Comparison Table

| GPU | Memory | Bandwidth | FP16 TFLOPS | TDP | Interconnect |
|---|---|---|---|---|---|
| NVIDIA B200 | 192 GB HBM3e | 8 TB/s | 2,250 | 1,000W | NVLink 5.0 |
| NVIDIA H200 | 141 GB HBM3e | 4.8 TB/s | 989 | 700W | NVLink 4.0 |
| NVIDIA H100 SXM | 80 GB HBM3 | 3.35 TB/s | 989 | 700W | NVLink 4.0 |
| NVIDIA A100 SXM | 80 GB HBM2e | 2.0 TB/s | 312 | 400W | NVLink 3.0 |
| AMD MI300X | 192 GB HBM3 | 5.3 TB/s | 1,307 | 750W | Infinity Fabric |
| AMD MI250X | 128 GB HBM2e | 3.2 TB/s | 383 | 560W | Infinity Fabric |
| Intel Gaudi 3 | 128 GB HBM2e | 3.7 TB/s | 1,835 | 900W | RoCE |
| Intel Gaudi 2 | 96 GB HBM2e | 2.45 TB/s | 432 | 600W | RoCE |

---

## Frequently Asked Questions

### How much memory does NVIDIA H100 have?
NVIDIA H100 SXM has 80 GB of HBM3 memory with 3.35 TB/s bandwidth. The PCIe variant also has 80 GB HBM3 but with 2.0 TB/s bandwidth.

### Which GPU has the most memory for AI?
As of 2025, both NVIDIA B200 and AMD MI300X offer 192 GB of HBM memory, the highest among production AI GPUs.

### What is the difference between H100 SXM and H100 PCIe?
H100 SXM delivers higher memory bandwidth (3.35 vs 2.0 TB/s), higher FP16 performance (989 vs 756 TFLOPS), higher TDP (700W vs 350W), and includes NVLink 4.0 with 900 GB/s bandwidth.

### How does AMD MI300X compare to NVIDIA H100?
AMD MI300X offers 2.4x more memory (192 vs 80 GB), 1.58x more bandwidth (5.3 vs 3.35 TB/s), and 1.32x more FP16 performance (1,307 vs 989 TFLOPS) compared to H100 SXM.

---

*Data sourced from official vendor specifications. See the [AI Infrastructure Index](https://github.com/alpha-one-index/ai-infra-index) for complete data.*
