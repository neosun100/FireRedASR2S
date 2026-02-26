[English](README_NEW.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md)

<div align="center">

# 🔥 FireRedASR2S

**SOTA Industrial-Grade All-in-One ASR System — Dockerized with UI + API + MCP**

[![Docker](https://img.shields.io/badge/Docker-neosun%2Ffirered--asr2s-blue?logo=docker)](https://hub.docker.com/r/neosun/firered-asr2s)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/neosun100/FireRedASR2S?style=social)](https://github.com/neosun100/FireRedASR2S)

🌐 [Live Demo](https://firered-asr.aws.xin) · 📄 [API Docs](https://firered-asr.aws.xin/docs) · 🤗 [Original Models](https://huggingface.co/FireRedTeam)

</div>

---

## ✨ Features

- 🎯 **SOTA ASR**: 2.89% CER on Mandarin, outperforming Doubao-ASR, Qwen3-ASR, FunASR
- 🌍 **Multi-language**: Chinese (Mandarin + 20+ dialects), English, code-switching, singing lyrics
- 🔊 **VAD**: Voice Activity Detection with 97.57% F1 score (100+ languages)
- 🌐 **LID**: Language Identification with 97.18% accuracy (100+ languages)
- 📝 **Punctuation**: Auto punctuation prediction (78.90% F1)
- ⏱️ **Word Timestamps**: Character/word-level timing with confidence scores
- 🖥️ **Web UI**: Modern dark-theme interface with 4-language support
- 🔌 **REST API**: Full Swagger documentation at `/docs`
- 🤖 **MCP Server**: Model Context Protocol for AI assistant integration
- 🐳 **All-in-One Docker**: Zero-config deployment with embedded models
- 🎮 **GPU Management**: Auto-select idle GPU, auto-offload after timeout

## 🚀 Quick Start

### Docker (Recommended)

```bash
# Pull and run (GPU required, ~15GB VRAM)
docker run -d --name firered-asr2s \
  --gpus '"device=0"' \
  -p 8350:8300 -p 8351:8301 \
  -v /tmp/firered-asr2s:/tmp/firered-asr2s \
  --shm-size=4g \
  --restart unless-stopped \
  neosun/firered-asr2s:latest

# Or use docker-compose
git clone https://github.com/neosun100/FireRedASR2S.git
cd FireRedASR2S
bash start.sh
```

Access:
- 🌐 UI: http://localhost:8350
- 📄 API Docs: http://localhost:8350/docs
- 🔌 MCP: port 8351

### One-Click Start Script

```bash
bash start.sh
# Auto-selects GPU with most free memory
# Builds and starts docker-compose
```

### Direct Run (Without Docker)

```bash
conda create --name fireredasr2s python=3.10
conda activate fireredasr2s
pip install -r requirements.txt
pip install fastapi uvicorn python-multipart fastmcp

# Download models
python3 -c "from huggingface_hub import snapshot_download; \
  snapshot_download('FireRedTeam/FireRedASR2-AED', local_dir='pretrained_models/FireRedASR2-AED'); \
  snapshot_download('FireRedTeam/FireRedVAD', local_dir='pretrained_models/FireRedVAD'); \
  snapshot_download('FireRedTeam/FireRedLID', local_dir='pretrained_models/FireRedLID'); \
  snapshot_download('FireRedTeam/FireRedPunc', local_dir='pretrained_models/FireRedPunc')"

export PYTHONPATH=$PWD:$PYTHONPATH
cd app && python3 -m uvicorn server:app --host 0.0.0.0 --port 8300
```

## 📡 API Usage

### Transcribe Audio

```bash
curl -X POST http://localhost:8350/api/transcribe \
  -F "file=@audio.wav"
```

Response:
```json
{
  "text": "你好世界。",
  "sentences": [{"start_ms": 310, "end_ms": 1840, "text": "你好世界。", "lang": "zh mandarin", "asr_confidence": 0.875}],
  "words": [{"start_ms": 490, "end_ms": 690, "text": "你"}, ...],
  "duration_seconds": 2.32,
  "process_time_seconds": 0.35,
  "rtf": 0.15
}
```

### Health Check

```bash
curl http://localhost:8350/health
```

### GPU Offload

```bash
curl -X POST http://localhost:8350/api/gpu-offload
```

## 🤖 MCP Integration

See [MCP_GUIDE.md](MCP_GUIDE.md) for full details.

```json
{
  "mcpServers": {
    "firered-asr2s": {
      "command": "docker",
      "args": ["exec", "-i", "firered-asr2s", "python3", "/workspace/app/mcp_server.py"]
    }
  }
}
```

## ⚙️ Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `PORT` | 8300 | API server port |
| `MCP_PORT` | 8301 | MCP server port |
| `GPU_IDLE_TIMEOUT` | 600 | Auto-offload timeout (seconds) |
| `ASR_TYPE` | aed | ASR model type (aed/llm) |

## 🏗️ Tech Stack

- **ASR Engine**: FireRedASR2S (PyTorch + CUDA 11.8)
- **Web Framework**: FastAPI + Uvicorn
- **MCP**: FastMCP
- **Frontend**: Vanilla HTML/CSS/JS (dark theme)
- **Container**: Docker + NVIDIA Container Toolkit

## 📊 Benchmarks

| Module | Metric | Score |
|--------|--------|-------|
| ASR (Mandarin) | CER | 3.05% |
| ASR (Dialects) | CER | 11.67% |
| VAD | F1 | 97.57% |
| LID | Accuracy | 97.18% |
| Punctuation | F1 | 78.90% |

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Pull Request

## 📝 Changelog

- **v1.0.0** (2026-02-26): Initial release with Docker, UI, API, MCP

## 📄 License

This project is licensed under the Apache License 2.0 - see [LICENSE](LICENSE) for details.

Based on [FireRedASR2S](https://github.com/FireRedTeam/FireRedASR2S) by Xiaohongshu FireRedTeam.

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=neosun100/FireRedASR2S&type=Date)](https://star-history.com/#neosun100/FireRedASR2S)

## 📱 关注公众号

![公众号](https://img.aws.xin/uPic/扫码_搜索联合传播样式-标准色版.png)
