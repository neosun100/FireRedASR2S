#!/usr/bin/env python3
"""FireRedASR2S MCP Server — fastmcp based."""
import os, sys, time, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from typing import Optional
from fastmcp import FastMCP
from gpu_manager import gpu_manager

mcp = FastMCP("firered-asr2s")


def _get_loop():
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop


@mcp.tool()
def transcribe(audio_path: str) -> dict:
    """Transcribe audio file using FireRedASR2S (ASR+VAD+LID+Punc).
    Supports Chinese (Mandarin + 20+ dialects), English, code-switching, and singing.
    Audio must be accessible from the container filesystem.

    Args:
        audio_path: Path to audio file (16kHz 16-bit mono PCM wav recommended)

    Returns:
        dict with text, sentences, vad_segments_ms, words, duration
    """
    if not os.path.exists(audio_path):
        return {"status": "error", "error": f"File not found: {audio_path}"}
    try:
        import subprocess
        converted = f"/tmp/firered_mcp_{int(time.time()*1000)}.wav"
        subprocess.run(
            ["ffmpeg", "-y", "-i", audio_path, "-ar", "16000", "-ac", "1", "-acodec", "pcm_s16le", "-f", "wav", converted],
            capture_output=True, timeout=120, check=True,
        )
        loop = _get_loop()
        asr = loop.run_until_complete(gpu_manager.get_model())
        t0 = time.time()
        result = asr.process(converted)
        t1 = time.time()
        os.remove(converted)
        return {
            "status": "success",
            "text": result["text"],
            "sentences": result["sentences"],
            "words": result["words"],
            "vad_segments_ms": result["vad_segments_ms"],
            "duration_seconds": round(result["dur_s"], 2),
            "process_time": round(t1 - t0, 3),
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


@mcp.tool()
def get_status() -> dict:
    """Get service status including GPU info and loaded model."""
    return gpu_manager.get_status()


@mcp.tool()
def gpu_offload() -> dict:
    """Release GPU memory by unloading all models."""
    loop = _get_loop()
    loop.run_until_complete(gpu_manager.offload())
    return {"status": "offloaded"}


if __name__ == "__main__":
    mcp.run()
