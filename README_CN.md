[English](README_NEW.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md)

<div align="center">

# 🔥 FireRedASR2S

**SOTA 工业级全能语音识别系统 — Docker 一键部署，UI + API + MCP 三合一**

[![Docker](https://img.shields.io/badge/Docker-neosun%2Ffirered--asr2s-blue?logo=docker)](https://hub.docker.com/r/neosun/firered-asr2s)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/neosun100/FireRedASR2S?style=social)](https://github.com/neosun100/FireRedASR2S)

🌐 [在线演示](https://firered-asr.aws.xin) · 📄 [API 文档](https://firered-asr.aws.xin/docs) · 🤗 [原始模型](https://huggingface.co/FireRedTeam)

</div>

---

## ✨ 功能特性

- 🎯 **SOTA 语音识别**: 普通话 2.89% CER，超越豆包ASR、Qwen3-ASR、FunASR
- 🌍 **多语言支持**: 中文（普通话 + 20+ 方言）、英文、中英混合、歌词识别
- 🔊 **语音活动检测 (VAD)**: F1 97.57%，支持 100+ 语言
- 🌐 **语种识别 (LID)**: 准确率 97.18%，支持 100+ 语言和 20+ 中文方言
- 📝 **标点预测**: 自动添加标点，F1 78.90%
- ⏱️ **字级时间戳**: 精确到每个字/词的起止时间和置信度
- 🖥️ **Web 界面**: 现代暗色主题，支持中/英/繁/日四语言
- 🔌 **REST API**: 完整 Swagger 文档，访问 `/docs`
- 🤖 **MCP 服务器**: 支持 AI 助手集成
- 🐳 **All-in-One Docker**: 零配置部署，模型内嵌
- 🎮 **GPU 管理**: 自动选择空闲 GPU，超时自动释放显存

## 🚀 快速开始

### Docker 部署（推荐）

```bash
# 拉取并运行（需要 GPU，约 15GB 显存）
docker run -d --name firered-asr2s \
  --gpus '"device=0"' \
  -p 8350:8300 -p 8351:8301 \
  -v /tmp/firered-asr2s:/tmp/firered-asr2s \
  --shm-size=4g \
  --restart unless-stopped \
  neosun/firered-asr2s:latest

# 或使用 docker-compose
git clone https://github.com/neosun100/FireRedASR2S.git
cd FireRedASR2S
bash start.sh  # 自动选择最空闲的 GPU
```

访问地址：
- 🌐 界面: http://localhost:8350
- 📄 API 文档: http://localhost:8350/docs
- 🔌 MCP: 端口 8351

### 直接运行（不使用 Docker）

```bash
conda create --name fireredasr2s python=3.10
conda activate fireredasr2s
pip install -r requirements.txt
pip install fastapi uvicorn python-multipart fastmcp

# 下载模型
python3 -c "from huggingface_hub import snapshot_download; \
  snapshot_download('FireRedTeam/FireRedASR2-AED', local_dir='pretrained_models/FireRedASR2-AED'); \
  snapshot_download('FireRedTeam/FireRedVAD', local_dir='pretrained_models/FireRedVAD'); \
  snapshot_download('FireRedTeam/FireRedLID', local_dir='pretrained_models/FireRedLID'); \
  snapshot_download('FireRedTeam/FireRedPunc', local_dir='pretrained_models/FireRedPunc')"

export PYTHONPATH=$PWD:$PYTHONPATH
cd app && python3 -m uvicorn server:app --host 0.0.0.0 --port 8300
```

## 📡 API 使用

```bash
# 语音识别
curl -X POST http://localhost:8350/api/transcribe -F "file=@audio.wav"

# 健康检查
curl http://localhost:8350/health

# 释放 GPU
curl -X POST http://localhost:8350/api/gpu-offload
```

## 🤖 MCP 集成

详见 [MCP_GUIDE.md](MCP_GUIDE.md)

## ⚙️ 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `PORT` | 8300 | API 端口 |
| `MCP_PORT` | 8301 | MCP 端口 |
| `GPU_IDLE_TIMEOUT` | 600 | GPU 空闲超时（秒） |

## 📊 性能指标

| 模块 | 指标 | 得分 |
|------|------|------|
| ASR（普通话） | CER | 3.05% |
| ASR（方言） | CER | 11.67% |
| VAD | F1 | 97.57% |
| LID | 准确率 | 97.18% |
| 标点 | F1 | 78.90% |

## 📄 许可证

Apache License 2.0。基于 [FireRedASR2S](https://github.com/FireRedTeam/FireRedASR2S)（小红书 FireRedTeam）。

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=neosun100/FireRedASR2S&type=Date)](https://star-history.com/#neosun100/FireRedASR2S)

## 📱 关注公众号

![公众号](https://img.aws.xin/uPic/扫码_搜索联合传播样式-标准色版.png)
