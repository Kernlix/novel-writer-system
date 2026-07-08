"""
Reranker API server — Qwen3-Reranker-0.6B via sentence-transformers CrossEncoder.

Endpoints:
  GET  /health          → {"status": "ok", "model": "..."}
  POST /v1/rerank       → {"results": [{"index": int, "relevance_score": float}, ...]}

Usage:
  python server_reranker.py [--port 8081] [--model Qwen/Qwen3-Reranker-0.6B]
"""

import argparse
import json
import logging
import os
import sys
import time
from typing import Optional

import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel

# Offline mode — use cached model only
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("reranker")

app = FastAPI(title="Novel Reranker", version="1.0.0")

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class RerankRequest(BaseModel):
    query: str
    documents: list[str]
    top_n: Optional[int] = None

class RerankResult(BaseModel):
    index: int
    relevance_score: float

class RerankResponse(BaseModel):
    results: list[RerankResult]

# ---------------------------------------------------------------------------
# Model global (lazy-loaded)
# ---------------------------------------------------------------------------

_model = None
_model_name: str = ""

def get_model(model_name: str):
    """Lazy-load cross-encoder model."""
    global _model, _model_name
    if _model is None:
        logger.info(f"Loading CrossEncoder model from {model_name} ...")
        t0 = time.time()
        from sentence_transformers import CrossEncoder
        _model = CrossEncoder(model_name, device="cpu")
        _model_name = model_name
        elapsed = time.time() - t0
        logger.info(f"Model loaded in {elapsed:.1f}s on cpu")
    return _model

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/health")
async def health():
    status = "loaded" if _model is not None else "ready"
    return {"status": status, "model": _model_name}

@app.post("/v1/rerank", response_model=RerankResponse)
async def rerank(req: RerankRequest):
    model = get_model(_model_name or "Qwen/Qwen3-Reranker-0.6B")

    pairs = [[req.query, doc] for doc in req.documents]
    scores = model.predict(pairs, show_progress_bar=False)

    # scores can be a list or numpy array
    if hasattr(scores, "tolist"):
        scores = scores.tolist()

    results = [
        RerankResult(index=i, relevance_score=float(s))
        for i, s in enumerate(scores)
    ]

    # Sort by score descending
    results.sort(key=lambda r: r.relevance_score, reverse=True)

    if req.top_n is not None and req.top_n > 0:
        results = results[: req.top_n]

    return RerankResponse(results=results)

# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Start reranker API server")
    ap.add_argument("--port", type=int, default=8081, help="Server port")
    ap.add_argument("--host", default="0.0.0.0", help="Bind address")
    ap.add_argument(
        "--model",
        default="Qwen/Qwen3-Reranker-0.6B",
        help="CrossEncoder model name or path",
    )
    args = ap.parse_args()

    global _model_name
    _model_name = args.model

    logger.info(
        f"Starting reranker server — model={args.model} "
        f"on {args.host}:{args.port}"
    )

    # Preload model before accepting requests
    get_model(args.model)

    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()
