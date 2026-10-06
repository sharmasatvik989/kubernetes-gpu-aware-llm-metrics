from app.planner import deployment_plan


def test_capacity_scales_with_demand():
    low = deployment_plan("mistral-7b-instruct", 512, 2, 1000)
    high = deployment_plan("mistral-7b-instruct", 512, 20, 1000)
    assert high["plan"]["replicas"] > low["plan"]["replicas"]
    assert high["plan"]["total_memory_gb"] > low["plan"]["total_memory_gb"]


def test_plan_explains_resources():
    result = deployment_plan("whisper-small", 512, 10, 800)
    assert result["pods"]
    assert result["plan"]["max_replicas"] > result["plan"]["min_replicas"]
    assert len(result["why"]) == 4


def test_cluster_limit_applies_admission_control():
    result = deployment_plan("all-minilm-l6-v2", 512, 1_000_000, 1000,
                             "hybrid", 20, 70, 32, 38, 100_000)
    assert result["plan"]["replicas"] == 38
    assert result["plan"]["required_pods"] > 38
    assert result["traffic"]["admitted_rps"] < result["traffic"]["inference_rps"]
    assert result["traffic"]["queued_rps"] == 100_000
    assert result["traffic"]["rejected_rps"] > 0
