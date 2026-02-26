# FireRedASR2S MCP Guide

## Overview
FireRedASR2S provides an MCP (Model Context Protocol) server for programmatic access from AI assistants and automation tools.

## Available Tools

### `transcribe`
Transcribe audio file using the full ASR pipeline (VAD → LID → ASR → Punc).

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| audio_path | string | Yes | Path to audio file (accessible from container) |

**Returns:** `{status, text, sentences, words, vad_segments_ms, duration_seconds, process_time}`

### `get_status`
Get service status including GPU info and loaded model state.

**Returns:** `{model_loaded, idle_seconds, idle_timeout, gpu: {id, name, memory_used_mb, ...}}`

### `gpu_offload`
Release GPU memory by unloading all models.

**Returns:** `{status: "offloaded"}`

## Configuration

```json
{
  "mcpServers": {
    "firered-asr2s": {
      "command": "docker",
      "args": ["exec", "-i", "firered-asr2s", "python3", "/workspace/app/mcp_server.py"],
      "env": {
        "GPU_IDLE_TIMEOUT": "600"
      }
    }
  }
}
```

## Usage Example

```python
result = await mcp_client.call_tool("transcribe", {"audio_path": "/tmp/firered-asr2s/test.wav"})
# Returns: {"status": "success", "text": "你好世界。", "sentences": [...], ...}
```

## Notes
- Audio files must be accessible from inside the container. Mount volumes via docker-compose.
- The MCP server shares the same GPU manager as the API/UI — models are loaded once and shared.
- Models auto-offload after `GPU_IDLE_TIMEOUT` seconds of inactivity.
