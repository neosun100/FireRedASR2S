[English](README_NEW.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md)

<div align="center">

# 🔥 FireRedASR2S

**SOTA 工業級全能語音識別系統 — Docker 一鍵部署，UI + API + MCP 三合一**

[![Docker](https://img.shields.io/badge/Docker-neosun%2Ffirered--asr2s-blue?logo=docker)](https://hub.docker.com/r/neosun/firered-asr2s)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)

🌐 [線上演示](https://firered-asr.aws.xin) · 📄 [API 文檔](https://firered-asr.aws.xin/docs)

</div>

---

## ✨ 功能特性

- 🎯 **SOTA 語音識別**: 普通話 2.89% CER，超越豆包ASR、Qwen3-ASR、FunASR
- 🌍 **多語言支持**: 中文（普通話 + 20+ 方言）、英文、中英混合、歌詞識別
- 🔊 **語音活動檢測 (VAD)**: F1 97.57%，支持 100+ 語言
- 🌐 **語種識別 (LID)**: 準確率 97.18%
- 📝 **標點預測**: 自動添加標點，F1 78.90%
- ⏱️ **字級時間戳**: 精確到每個字/詞的起止時間
- 🖥️ **Web 介面**: 現代暗色主題，支持中/英/繁/日四語言
- 🔌 **REST API**: 完整 Swagger 文檔
- 🤖 **MCP 伺服器**: 支持 AI 助手整合
- 🐳 **All-in-One Docker**: 零配置部署

## 🚀 快速開始

```bash
docker run -d --name firered-asr2s \
  --gpus '"device=0"' \
  -p 8350:8300 -p 8351:8301 \
  -v /tmp/firered-asr2s:/tmp/firered-asr2s \
  --shm-size=4g \
  neosun/firered-asr2s:latest
```

- 🌐 介面: http://localhost:8350
- 📄 API 文檔: http://localhost:8350/docs

## 📡 API 使用

```bash
curl -X POST http://localhost:8350/api/transcribe -F "file=@audio.wav"
```

## 📄 授權

Apache License 2.0。基於 [FireRedASR2S](https://github.com/FireRedTeam/FireRedASR2S)（小紅書 FireRedTeam）。

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=neosun100/FireRedASR2S&type=Date)](https://star-history.com/#neosun100/FireRedASR2S)

## 📱 關注公眾號

![公眾號](https://img.aws.xin/uPic/扫码_搜索联合传播样式-标准色版.png)
