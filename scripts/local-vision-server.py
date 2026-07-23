#!/usr/bin/env python3
"""
本地视觉API服务器 — Qwen2.5-VL-3B-Instruct
OpenAI-compatible /v1/chat/completions 端点
供 Hermes vision_analyze 使用
"""

import os, sys, base64, io, json, time, logging
from pathlib import Path
from PIL import Image
import torch

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# ── 路径 ──
MODEL_DIR = Path("D:/llama-b9851-bin-win-cuda-12.4-x64/modes/Qwen2.5-VL-3B-Instruct")
os.environ["HF_HOME"] = "D:/llama-b9851-bin-win-cuda-12.4-x64/modes/hf_cache"
os.environ["HF_HUB_CACHE"] = "D:/llama-b9851-bin-win-cuda-12.4-x64/modes/hf_cache"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# ── 模型加载 ──
log.info("正在加载 Qwen2.5-VL-3B-Instruct …")
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from transformers import BitsAndBytesConfig

quant = BitsAndBytesConfig(
    load_in_8bit=True,
    bnb_8bit_compute_dtype=torch.float16,
)

model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    MODEL_DIR,
    quantization_config=quant,
    device_map="auto",
    torch_dtype=torch.float16,
)
processor = AutoProcessor.from_pretrained(MODEL_DIR)
log.info(f"✅ 模型已加载，device_map={model.device}")

# ── FastAPI ──
app = FastAPI(title="本地视觉API")

def decode_image(url: str) -> Image.Image:
    """从各种 URL 格式解析图片"""
    if url.startswith("data:image"):
        _, b64 = url.split(",", 1)
        raw = base64.b64decode(b64)
        return Image.open(io.BytesIO(raw)).convert("RGB")
    elif url.startswith("http"):
        from urllib.request import urlopen
        return Image.open(urlopen(url)).convert("RGB")
    else:
        return Image.open(url).convert("RGB")

class ChatRequest(BaseModel):
    model: str = "qwen2.5-vl-3b"
    messages: List[Dict[str, Any]]
    max_tokens: int = 512
    temperature: float = 0.7

    model_config = {"extra": "allow"}

@app.post("/v1/chat/completions")
async def chat_completions(req: ChatRequest):
    t0 = time.time()

    # 转换 OpenAI 格式 → Qwen 格式 (processor.apply_chat_template)
    images = []
    qwen_messages = []

    for msg in req.messages:
        role = msg["role"]
        content = msg.get("content", "")

        if isinstance(content, str):
            qwen_messages.append({"role": role, "content": content})
        elif isinstance(content, list):
            # 多模态格式: text + image_url
            parts = []
            for item in content:
                if item.get("type") == "text":
                    parts.append({"type": "text", "text": item["text"]})
                elif item.get("type") == "image_url":
                    img_url = item["image_url"]["url"]
                    pil_img = decode_image(img_url)
                    images.append(pil_img)
                    # Qwen 的 image token 由 apply_chat_template 自动插入
                    parts.append({"type": "image", "image": pil_img})
            qwen_messages.append({"role": role, "content": parts})

    if not qwen_messages:
        return JSONResponse({"error": "empty messages"}, status_code=400)

    # apply_chat_template 生成带 image token 的文本
    text = processor.apply_chat_template(
        qwen_messages, tokenize=False, add_generation_prompt=True
    )

    # 处理: 传 text 和 images
    inputs = processor(
        text=[text],
        images=images if images else None,
        padding=True,
        return_tensors="pt",
    ).to(model.device)

    # 生成
    with torch.no_grad():
        generated_ids = model.generate(
            **inputs,
            max_new_tokens=req.max_tokens,
            temperature=req.temperature,
            do_sample=req.temperature > 0,
            pad_token_id=processor.tokenizer.pad_token_id,
        )

    input_len = inputs["input_ids"].shape[1]
    output_ids = generated_ids[0][input_len:]
    response_text = processor.tokenizer.decode(output_ids, skip_special_tokens=True)

    elapsed = time.time() - t0
    log.info(f"✅ 生成完成 ({elapsed:.1f}s): {len(response_text)} 字符")

    return {
        "id": "chatcmpl-local",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "qwen2.5-vl-3b",
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": response_text},
            "finish_reason": "stop",
        }],
        "usage": {
            "prompt_tokens": input_len,
            "completion_tokens": len(output_ids),
            "total_tokens": input_len + len(output_ids),
        },
    }

@app.get("/health")
async def health():
    return {"status": "ok", "model": "qwen2.5-vl-3b", "device": str(model.device)}

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    log.info(f"启动服务器于 http://localhost:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
