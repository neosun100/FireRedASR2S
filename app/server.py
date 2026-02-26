"""FastAPI server for FireRedASR2S — UI + REST API."""
import os, sys, time, uuid, asyncio, json, subprocess
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from contextlib import asynccontextmanager
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

from gpu_manager import gpu_manager

SUPPORTED_LANGUAGES = [
    "Chinese (Mandarin)", "English", "Cantonese (Hong Kong)", "Cantonese (Guangdong)",
    "Sichuan", "Shanghai", "Wu", "Minnan", "Anhui", "Fujian", "Gansu", "Guizhou",
    "Hebei", "Henan", "Hubei", "Hunan", "Jiangxi", "Liaoning", "Ningxia",
    "Shaanxi", "Shanxi", "Shandong", "Tianjin", "Yunnan",
]


@asynccontextmanager
async def lifespan(app):
    task = asyncio.create_task(gpu_manager.auto_offload_loop())
    yield
    task.cancel()


app = FastAPI(
    title="FireRedASR2S",
    description="SOTA Industrial-Grade All-in-One ASR System with ASR, VAD, LID, and Punc",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.get("/", response_class=HTMLResponse)
async def index():
    p = Path(__file__).parent / "templates" / "index.html"
    return p.read_text(encoding="utf-8") if p.exists() else "<h1>FireRedASR2S</h1><p><a href='/docs'>API Docs</a></p>"


@app.get("/health")
async def health():
    s = gpu_manager.get_status()
    return {"status": "healthy", "version": "1.0.0", "model_loaded": s["model_loaded"], **s}


@app.get("/api/status")
async def api_status():
    s = gpu_manager.get_status()
    return {**s, "supported_languages": SUPPORTED_LANGUAGES}


@app.post("/api/transcribe")
async def api_transcribe(
    file: UploadFile = File(...),
    enable_vad: bool = Form(True),
    enable_lid: bool = Form(True),
    enable_punc: bool = Form(True),
    beam_size: int = Form(3),
    speech_threshold: float = Form(0.2),
    softmax_smoothing: float = Form(1.25),
    aed_length_penalty: float = Form(0.6),
    eos_penalty: float = Form(1.0),
):
    t0 = time.time()
    tmp = f"/tmp/firered_asr_{uuid.uuid4()}.wav"
    tmp_converted = f"/tmp/firered_asr_{uuid.uuid4()}_16k.wav"
    try:
        content = await file.read()
        if len(content) > 200 * 1024 * 1024:
            return JSONResponse({"error": "File too large (max 200MB)"}, status_code=413)
        with open(tmp, "wb") as f:
            f.write(content)

        # Convert to 16kHz 16-bit mono PCM
        ret = subprocess.run(
            ["ffmpeg", "-y", "-i", tmp, "-ar", "16000", "-ac", "1", "-acodec", "pcm_s16le", "-f", "wav", tmp_converted],
            capture_output=True, timeout=120,
        )
        if ret.returncode != 0:
            return JSONResponse({"error": "Audio conversion failed. Please upload a valid audio file."}, status_code=400)

        asr_system = await gpu_manager.get_model()

        t_proc_start = time.time()
        result = asr_system.process(tmp_converted)
        t_proc = time.time() - t_proc_start

        t_total = time.time() - t0
        resp = {
            "text": result["text"],
            "sentences": result["sentences"],
            "vad_segments_ms": result["vad_segments_ms"],
            "words": result["words"],
            "duration_seconds": round(result["dur_s"], 2),
            "process_time_seconds": round(t_proc, 3),
            "rtf": round(t_proc / result["dur_s"], 4) if result["dur_s"] > 0 else 0,
        }
        headers = {
            "X-Time-Process": f"{t_proc:.3f}",
            "X-Time-Total": f"{t_total:.3f}",
        }
        return JSONResponse(resp, headers=headers)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)
    finally:
        for p in [tmp, tmp_converted]:
            if os.path.exists(p):
                os.remove(p)


@app.post("/api/gpu-offload")
async def gpu_offload():
    await gpu_manager.offload()
    return {"status": "offloaded", **gpu_manager.get_status()}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8300"))
    uvicorn.run("server:app", host="0.0.0.0", port=port, workers=1)
