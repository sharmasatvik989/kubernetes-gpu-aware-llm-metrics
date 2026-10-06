from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field

from .planner import MODELS, catalog, deployment_plan

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
ASSETS = {"app.js", "styles.css", "workspace.css", "visual-refresh.css", "product-v2.css"}

app = FastAPI(title="GPU-Aware LLM Router", version="1.0.0")


class PlanRequest(BaseModel):
    model: str
    tokens: int = Field(default=1024, ge=32, le=8192)
    incoming_rps: int = Field(default=1000, ge=1, le=1_000_000)
    latency_slo_ms: int = Field(default=500, ge=50, le=10000)
    processing_mode: str = Field(default="hybrid", pattern="^(synchronous|asynchronous|hybrid)$")
    gateway_threads: int = Field(default=20, ge=1, le=128)
    cache_hit_percent: int = Field(default=20, ge=0, le=95)
    batch_size: int = Field(default=8, ge=1, le=64)
    max_gpu_pods: int = Field(default=38, ge=1, le=200)
    queue_capacity: int = Field(default=100_000, ge=0, le=1_000_000)


@app.get("/")
def home():
    html = (PUBLIC / "index.html").read_text()
    css = "\n".join((PUBLIC / name).read_text() for name in
                    ("styles.css", "workspace.css", "visual-refresh.css", "product-v2.css"))
    javascript = (PUBLIC / "app.js").read_text()
    for name in ("styles.css", "workspace.css", "visual-refresh.css", "product-v2.css"):
        html = html.replace(f'<link rel="stylesheet" href="/{name}?v=4">', "")
    html = html.replace("</head>", f"<style>{css}</style></head>")
    html = html.replace('<script src="/app.js?v=4" defer></script>', f"<script>{javascript}</script>")
    return HTMLResponse(html, headers={"Cache-Control": "no-store"})


@app.get("/assets/{name}", include_in_schema=False)
def asset(name: str):
    if name not in ASSETS:
        raise HTTPException(status_code=404, detail="Not found")
    return FileResponse(PUBLIC / name, headers={"Cache-Control": "no-store"})


@app.get("/{name}", include_in_schema=False)
def root_asset(name: str):
    """Match Vercel's public-directory URLs during local development."""
    if name not in ASSETS:
        raise HTTPException(status_code=404, detail="Not found")
    return FileResponse(PUBLIC / name, headers={"Cache-Control": "no-store"})


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "gpu-aware-router"}


@app.get("/api/catalog")
def model_catalog():
    return catalog()


@app.post("/api/plan")
def plan_request(request: PlanRequest):
    if request.model not in MODELS:
        raise HTTPException(status_code=400, detail="Unsupported model")
    return deployment_plan(request.model, request.tokens, request.incoming_rps, request.latency_slo_ms,
                           request.processing_mode, request.gateway_threads, request.cache_hit_percent,
                           request.batch_size, request.max_gpu_pods, request.queue_capacity)
