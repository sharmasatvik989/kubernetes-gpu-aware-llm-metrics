import math


MODELS = {
    "mistral-7b-instruct": {
        "name": "Mistral 7B Instruct", "use_case": "text-generation", "task": "Text generation",
        "gpu": "NVIDIA L4 24 GB", "weight_memory_gb": 14.5, "tokens_per_second": 1450,
        "base_latency_ms": 95, "max_batch": 8, "gpu_fraction": 1.0,
    },
    "llama-3.1-8b-instruct": {
        "name": "Llama 3.1 8B Instruct", "use_case": "text-generation", "task": "Text generation",
        "gpu": "NVIDIA A10G 24 GB", "weight_memory_gb": 16.5, "tokens_per_second": 1320,
        "base_latency_ms": 108, "max_batch": 8, "gpu_fraction": 1.0,
    },
    "qwen2.5-3b-instruct": {
        "name": "Qwen 2.5 3B Instruct", "use_case": "text-generation", "task": "Text generation",
        "gpu": "NVIDIA L4 24 GB", "weight_memory_gb": 6.8, "tokens_per_second": 2650,
        "base_latency_ms": 64, "max_batch": 16, "gpu_fraction": .5,
    },
    "phi-3-mini-instruct": {
        "name": "Phi-3 Mini Instruct", "use_case": "text-generation", "task": "Text generation",
        "gpu": "NVIDIA T4 16 GB", "weight_memory_gb": 7.6, "tokens_per_second": 2100,
        "base_latency_ms": 71, "max_batch": 12, "gpu_fraction": .5,
    },
    "whisper-small": {
        "name": "Whisper Small", "use_case": "speech-to-text", "task": "Speech to text",
        "gpu": "NVIDIA L4 24 GB", "weight_memory_gb": 3.2, "tokens_per_second": 4200,
        "base_latency_ms": 72, "max_batch": 16, "gpu_fraction": .5,
    },
    "whisper-tiny": {
        "name": "Whisper Tiny", "use_case": "speech-to-text", "task": "Speech to text",
        "gpu": "NVIDIA T4 16 GB", "weight_memory_gb": .8, "tokens_per_second": 9200,
        "base_latency_ms": 38, "max_batch": 32, "gpu_fraction": .25,
    },
    "whisper-base": {
        "name": "Whisper Base", "use_case": "speech-to-text", "task": "Speech to text",
        "gpu": "NVIDIA T4 16 GB", "weight_memory_gb": 1.5, "tokens_per_second": 6800,
        "base_latency_ms": 51, "max_batch": 24, "gpu_fraction": .25,
    },
    "wav2vec2-base-960h": {
        "name": "Wav2Vec2 Base 960h", "use_case": "speech-to-text", "task": "Speech to text",
        "gpu": "NVIDIA T4 16 GB", "weight_memory_gb": 1.2, "tokens_per_second": 7600,
        "base_latency_ms": 44, "max_batch": 24, "gpu_fraction": .25,
    },
    "all-minilm-l6-v2": {
        "name": "all-MiniLM-L6-v2", "use_case": "embeddings", "task": "Embeddings",
        "gpu": "NVIDIA T4 16 GB", "weight_memory_gb": 1.1, "tokens_per_second": 12500,
        "base_latency_ms": 24, "max_batch": 64, "gpu_fraction": .25,
    },
    "bge-small-en-v1.5": {
        "name": "BGE Small EN v1.5", "use_case": "embeddings", "task": "Embeddings",
        "gpu": "NVIDIA T4 16 GB", "weight_memory_gb": 1.3, "tokens_per_second": 11200,
        "base_latency_ms": 27, "max_batch": 64, "gpu_fraction": .25,
    },
    "e5-base-v2": {
        "name": "E5 Base v2", "use_case": "embeddings", "task": "Embeddings",
        "gpu": "NVIDIA L4 24 GB", "weight_memory_gb": 2.2, "tokens_per_second": 8200,
        "base_latency_ms": 34, "max_batch": 48, "gpu_fraction": .25,
    },
    "gte-base-en-v1.5": {
        "name": "GTE Base EN v1.5", "use_case": "embeddings", "task": "Embeddings",
        "gpu": "NVIDIA L4 24 GB", "weight_memory_gb": 2.5, "tokens_per_second": 7900,
        "base_latency_ms": 36, "max_batch": 48, "gpu_fraction": .25,
    },
    "distilbert-sst2": {
        "name": "DistilBERT SST-2", "use_case": "classification", "task": "Classification",
        "gpu": "NVIDIA T4 16 GB", "weight_memory_gb": 1.4, "tokens_per_second": 9800,
        "base_latency_ms": 31, "max_batch": 48, "gpu_fraction": .25,
    },
    "roberta-go-emotions": {
        "name": "RoBERTa GoEmotions", "use_case": "classification", "task": "Classification",
        "gpu": "NVIDIA T4 16 GB", "weight_memory_gb": 1.8, "tokens_per_second": 7600,
        "base_latency_ms": 39, "max_batch": 40, "gpu_fraction": .25,
    },
    "finbert": {
        "name": "FinBERT", "use_case": "classification", "task": "Classification",
        "gpu": "NVIDIA T4 16 GB", "weight_memory_gb": 1.7, "tokens_per_second": 8100,
        "base_latency_ms": 36, "max_batch": 40, "gpu_fraction": .25,
    },
    "deberta-v3-base": {
        "name": "DeBERTa v3 Base", "use_case": "classification", "task": "Classification",
        "gpu": "NVIDIA L4 24 GB", "weight_memory_gb": 2.4, "tokens_per_second": 6500,
        "base_latency_ms": 47, "max_batch": 32, "gpu_fraction": .25,
    },
}


USE_CASES = [
    {"id": "text-generation", "name": "Text generation", "description": "Interactive generation and completion"},
    {"id": "speech-to-text", "name": "Speech to text", "description": "Audio transcription workloads"},
    {"id": "embeddings", "name": "Embeddings", "description": "Search and retrieval vectors"},
    {"id": "classification", "name": "Classification", "description": "Low-latency label prediction"},
]


def catalog() -> dict:
    return {"use_cases": USE_CASES, "models": [{"id": key, **value} for key, value in MODELS.items()]}


def deployment_plan(model_id: str, tokens: int, incoming_rps: int, latency_slo_ms: int,
                    processing_mode: str = "hybrid", gateway_threads: int = 20,
                    cache_hit_percent: int = 20, batch_size: int = 8,
                    max_gpu_pods: int = 38, queue_capacity: int = 100_000) -> dict:
    model = MODELS[model_id]
    target_utilization = .68
    cache_rps = math.floor(incoming_rps * cache_hit_percent / 100)
    inference_rps = max(0, incoming_rps - cache_rps)
    mode_efficiency = {"synchronous": 1.0, "asynchronous": 1.0 + min(batch_size, model["max_batch"]) ** .5 * .52,
                       "hybrid": 1.0 + min(batch_size, model["max_batch"]) ** .5 * .34}[processing_mode]
    usable_throughput = model["tokens_per_second"] * target_utilization * mode_efficiency
    required_pods = max(1, math.ceil(tokens * inference_rps / usable_throughput)) if inference_rps else 1
    min_available = 2 if processing_mode != "asynchronous" else 1
    provisioned_pods = min(max_gpu_pods, max(min_available, required_pods))
    sustainable_rps = max(1, math.floor(provisioned_pods * usable_throughput / tokens))
    admitted_rps = min(inference_rps, sustainable_rps)
    overflow_rps = max(0, inference_rps - admitted_rps)
    queued_rps = min(overflow_rps, queue_capacity) if processing_mode in {"asynchronous", "hybrid"} else 0
    rejected_rps = max(0, overflow_rps - queued_rps)
    gateway_capacity_per_instance = max(1, gateway_threads * 2500)
    gateway_instances = max(1, math.ceil(incoming_rps / gateway_capacity_per_instance))
    effective_batch = min(batch_size, model["max_batch"])
    kv_cache_gb = max(.4, tokens * effective_batch * .00011)
    memory_per_pod = round(model["weight_memory_gb"] + kv_cache_gb + 1.2, 1)
    total_memory = round(memory_per_pod * provisioned_pods, 1)
    gpu_utilization = min(96, round(tokens * admitted_rps / max(1, provisioned_pods * model["tokens_per_second"] * mode_efficiency) * 100))
    batch_wait_ms = {"synchronous": 0, "hybrid": 35, "asynchronous": 120}[processing_mode]
    queue_delay_ms = round(queued_rps / max(admitted_rps, 1) * 1000)
    network_latency_ms = round(10 + min(80, incoming_rps / max(gateway_instances, 1) / 2500))
    compute_ms = tokens / (model["tokens_per_second"] * mode_efficiency) * 1000
    projected_latency_ms = round(model["base_latency_ms"] + compute_ms + batch_wait_ms + network_latency_ms + min(queue_delay_ms, 30_000))
    network_mbps = round(incoming_rps * tokens * .0024, 1)
    capacity_deficit_percent = round(overflow_rps / max(inference_rps, 1) * 100, 1)
    slo_status = "within-slo" if projected_latency_ms <= latency_slo_ms and rejected_rps == 0 else "at-risk"
    pods = [{"name": f"{model_id[:18]}-{index + 1}", "zone": f"us-west-2{chr(97 + index % 3)}",
             "utilization": max(5, min(98, gpu_utilization + ((index % 3) - 1) * 5)), "memory_gb": memory_per_pod,
             "gpu_allocation": model["gpu_fraction"], "status": "ready"} for index in range(provisioned_pods)]
    why = [
        f"{incoming_rps:,} incoming RPS is handled by {gateway_instances} async gateway instance{'s' if gateway_instances != 1 else ''} using {gateway_threads} threads each; gateway concurrency does not increase GPU compute capacity.",
        f"The {cache_hit_percent}% cache-hit assumption serves {cache_rps:,} RPS before inference, leaving {inference_rps:,} RPS for the GPU pool.",
        f"{processing_mode.title()} processing with batches of {effective_batch} improves effective model throughput by {mode_efficiency:.2f}× and requires {required_pods:,} pods before the cluster limit is applied.",
        f"The cluster is capped at {max_gpu_pods} GPU pods, sustaining {sustainable_rps:,} inference RPS; {queued_rps:,} RPS is queued and {rejected_rps:,} RPS is rejected or redirected.",
    ]
    return {"model": {"id": model_id, **model}, "inputs": {"tokens": tokens, "incoming_rps": incoming_rps,
            "latency_slo_ms": latency_slo_ms, "processing_mode": processing_mode},
            "traffic": {"incoming_rps": incoming_rps, "cache_rps": cache_rps, "inference_rps": inference_rps,
                        "admitted_rps": admitted_rps, "queued_rps": queued_rps, "rejected_rps": rejected_rps},
            "plan": {"replicas": provisioned_pods, "required_pods": required_pods, "max_gpu_pods": max_gpu_pods,
                     "gateway_instances": gateway_instances, "gateway_threads": gateway_threads, "gpu_allocations": provisioned_pods,
                     "gpu": model["gpu"], "gpu_fraction_per_pod": model["gpu_fraction"], "memory_per_pod_gb": memory_per_pod,
                     "total_memory_gb": total_memory, "batch_size": effective_batch, "batch_efficiency": round(mode_efficiency, 2),
                     "projected_latency_ms": projected_latency_ms, "queue_delay_ms": queue_delay_ms,
                     "network_latency_ms": network_latency_ms, "network_mbps": network_mbps, "gpu_utilization": gpu_utilization,
                     "capacity_rps": sustainable_rps, "capacity_deficit_percent": capacity_deficit_percent, "slo_status": slo_status},
            "pods": pods, "why": why}
