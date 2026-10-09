# Kubernetes GPU-Aware LLM Routing Platform

## Visitor analytics

The production site includes Vercel Web Analytics for privacy-safe page views and unique visitor reporting. Enable **Web Analytics** from the Vercel project dashboard and redeploy after enabling it. Visitor data is available under the project's **Analytics** tab.

An interactive Kubernetes capacity planner for model inference workloads. It translates use case, model, token volume, request rate, and latency SLO into pods, GPU allocation, memory, network demand, and autoscaling boundaries.

## Version 1

- Select text generation, speech-to-text, embeddings, or classification.
- Adjust token volume, requests per second, and latency SLO interactively.
- Watch pods and GPU allocations scale with demand.
- Inspect memory, projected latency, network load, throughput, and autoscaling limits.
- Model up to one million incoming requests per second without assuming unlimited GPU pods.
- Separate async gateway capacity from bounded inference capacity.
- Apply cache hits, dynamic batching, queue limits, and admission control.
- Report admitted, queued, and rejected traffic when demand exceeds the cluster.
- Explain why every part of the orchestration plan is required.
- Ship a Kubernetes deployment and service definition for the routing API.

The web demo exercises deterministic capacity-planning formulas and clearly presents their assumptions. It does not claim to allocate physical GPUs or send production inference traffic. A production implementation would replace planning assumptions with benchmark profiles, Kubernetes informers, NVIDIA DCGM metrics, and inference-runtime telemetry.

## Planning model

The planner reserves capacity at a 68% target GPU utilization, spreads pods over three zones, estimates model and runtime memory, and calculates projected compute plus network latency. Gateway threads model I/O concurrency only. Cache hits are removed before inference, batching improves effective GPU throughput, and the GPU pool is capped by the configured cluster limit. Excess traffic is admitted, queued, or rejected explicitly instead of generating unlimited pods. These estimates must be replaced with workload benchmarks before production use.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt pytest
uvicorn index:app --reload --port 8081
```

Open `http://127.0.0.1:8081`.

## Next infrastructure iteration

1. Watch GPU nodes, pods, and model deployments through Kubernetes informers.
2. Ingest DCGM utilization and memory metrics from Prometheus.
3. Add Triton/vLLM queue and token-throughput telemetry.
4. Reserve capacity through extended resources and NVIDIA device-plugin labels.
5. Apply load-aware routing through an Envoy or Kubernetes Gateway API integration.
