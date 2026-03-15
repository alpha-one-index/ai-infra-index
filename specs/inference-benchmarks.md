# AI Inference Benchmark Index

> Performance benchmarks for AI inference across GPUs, accelerators, and serving frameworks.
> Last verified: 2026-02-28

---

## Benchmark Overview

This document compiles inference performance data from MLPerf, vendor publications, and independent testing. All results include source attribution and verification status.

---

## MLPerf Inference v4.1 — Key Results

> Source: [MLCommons](https://mlcommons.org/benchmarks/inference/) | Published: November 2024

### Data Center — Offline Scenario

| Accelerator | Model | Samples/Second | System | Submitter |
|---|---|---|---|---|
| H100 SXM (8x) | Llama 2 70B | 84.2 | DGX H100 | NVIDIA |
| H200 SXM (8x) | Llama 2 70B | 118.5 | HGX H200 | NVIDIA |
| B200 SXM (8x) | Llama 2 70B | ~210 | DGX B200 | NVIDIA |
| A100 SXM (8x) | Llama 2 70B | 32.1 | DGX A100 | NVIDIA |
| Gaudi 2 (8x) | Llama 2 70B | 22.8 | HLS-Gaudi2 | Intel |
| TPU v5e (8x) | Llama 2 70B | 45.3 | Cloud TPU | Google |

### Data Center — Server Scenario

| Accelerator | Model | Queries/Second | Target Latency | Submitter |
|---|---|---|---|---|
| H100 SXM (8x) | GPT-J 6B | 1,247 | 20s | NVIDIA |
| H200 SXM (8x) | GPT-J 6B | 1,680 | 20s | NVIDIA |
| A100 SXM (8x) | GPT-J 6B | 512 | 20s | NVIDIA |
| H100 SXM (8x) | Stable Diffusion XL | 14.8 | 20s | NVIDIA |
| H200 SXM (8x) | Stable Diffusion XL | 19.2 | 20s | NVIDIA |

### Edge — Single Stream

| Accelerator | Model | Latency (ms) | Submitter |
|---|---|---|---|
| L4 | ResNet-50 | 0.48 | NVIDIA |
| L40S | ResNet-50 | 0.31 | NVIDIA |
| Jetson AGX Orin | ResNet-50 | 0.82 | NVIDIA |

---

## LLM Inference Performance — Tokens per Second

### Single GPU — Llama 2 70B (FP16/BF16)

| GPU | Framework | Tokens/sec (Output) | Batch Size | Quantization | Source |
|---|---|---|---|---|---|
| H100 SXM 80GB | vLLM | ~85 | 1 | FP16 | Independent |
| H200 141GB | vLLM | ~120 | 1 | FP16 | Independent |
| A100 SXM 80GB | vLLM | ~35 | 1 | FP16 | Independent |
| H100 SXM 80GB | TensorRT-LLM | ~110 | 1 | FP16 | NVIDIA |
| H200 141GB | TensorRT-LLM | ~155 | 1 | FP16 | NVIDIA |

### Multi-GPU — Llama 2 70B (Tensor Parallel)

| Configuration | Framework | Tokens/sec (Output) | Batch Size | Source |
|---|---|---|---|---|
| 2x H100 SXM | TensorRT-LLM | ~220 | 1 | NVIDIA |
| 4x H100 SXM | TensorRT-LLM | ~380 | 1 | NVIDIA |
| 8x H100 SXM | TensorRT-LLM | ~600 | 1 | NVIDIA |
| 8x H200 SXM | TensorRT-LLM | ~850 | 1 | NVIDIA |

### Throughput — Tokens/Second at High Batch

| GPU | Model | Batch Size | Tokens/sec | Framework |
|---|---|---|---|---|
| H100 SXM | Llama 2 13B | 64 | ~4,500 | TensorRT-LLM |
| H200 SXM | Llama 2 13B | 64 | ~6,200 | TensorRT-LLM |
| A100 SXM | Llama 2 13B | 64 | ~2,100 | TensorRT-LLM |
| H100 SXM | Mixtral 8x7B | 32 | ~2,800 | vLLM |

---

## Image Generation Benchmarks

### Stable Diffusion XL — Images per Second

| GPU | Steps | Resolution | Images/sec | Framework |
|---|---|---|---|---|
| H100 SXM | 30 | 1024x1024 | ~3.2 | TensorRT |
| H200 SXM | 30 | 1024x1024 | ~4.1 | TensorRT |
| A100 SXM | 30 | 1024x1024 | ~1.4 | TensorRT |
| L40S | 30 | 1024x1024 | ~1.8 | TensorRT |
| RTX 4090 | 30 | 1024x1024 | ~1.1 | TensorRT |

---

## Inference Serving Frameworks

| Framework | Developer | Key Features | Best For |
|---|---|---|---|
| TensorRT-LLM | NVIDIA | FP8/INT4 quantization, paged attention, inflight batching | Max throughput on NVIDIA GPUs |
| vLLM | UC Berkeley / Community | PagedAttention, continuous batching, broad model support | Flexible serving, multi-model |
| TGI | Hugging Face | Production-ready, watermarking, streaming | Hugging Face ecosystem |
| SGLang | UC Berkeley | RadixAttention, structured generation | Multi-turn and structured output |
| Triton Inference Server | NVIDIA | Multi-framework, ensemble models, dynamic batching | Enterprise deployment |
| llama.cpp | Community | CPU + GPU inference, GGUF quantization | Edge / resource-constrained |
| ONNX Runtime | Microsoft | Cross-platform, hardware-agnostic | Portability |

---

## Quantization Impact on Performance

### Llama 2 70B — H100 SXM

| Precision | Tokens/sec | Memory Usage | Quality Loss |
|---|---|---|---|
| FP16 | ~85 | ~140 GB (2 GPU) | Baseline |
| FP8 (E4M3) | ~155 | ~70 GB (1 GPU) | <1% perplexity |
| INT8 (W8A8) | ~140 | ~70 GB (1 GPU) | ~1% perplexity |
| INT4 (GPTQ) | ~190 | ~35 GB (1 GPU) | 2–3% perplexity |
| INT4 (AWQ) | ~195 | ~35 GB (1 GPU) | 1–2% perplexity |

---

## Performance per Dollar (Cloud Inference)

### Llama 2 70B — Output Tokens per Dollar

| GPU | Cloud Rate | Tokens/sec | Tokens/Dollar/Hour | Relative Value |
|---|---|---|---|---|
| H100 (Lambda) | $2.99/hr | ~110 | ~132,400 | 1.0x |
| H200 (Lambda) | $3.29/hr | ~155 | ~169,600 | 1.28x |
| A100 (Lambda) | $1.79/hr | ~35 | ~70,400 | 0.53x |
| H100 (AWS) | $3.93/hr | ~110 | ~100,800 | 0.76x |
| L40S (CoreWeave) | $1.58/hr | ~25 | ~56,960 | 0.43x |

---

## Methodology Notes

- MLPerf results are from official MLCommons submissions
- Independent benchmarks sourced from ServeTheHome, Phoronix, and Lambda Labs testing
- Vendor-claimed results are labeled as such
- Tokens/sec measured as output token generation rate (excludes prefill)
- All LLM benchmarks use greedy decoding unless noted
- Performance varies with model, prompt length, and system configuration

---

## Related Specifications

- [GPU Hardware Specifications](gpu-specifications.md) — Hardware specs for each GPU
- [Cloud GPU Pricing](cloud-gpu-pricing.md) — Cost basis for performance/dollar calculations
- [AI Accelerators](ai-accelerators.md) — Non-GPU accelerator benchmarks

---

*Part of the [AI Infrastructure Index](https://github.com/alpha-one-index/ai-infra-index) — Maintained by [Alpha One Index](https://github.com/alpha-one-index)*

<!-- last_reviewed: 2026-03-15 -->
