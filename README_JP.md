[English](README_NEW.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md)

<div align="center">

# 🔥 FireRedASR2S

**SOTA 産業グレード オールインワン音声認識システム — Docker デプロイ、UI + API + MCP**

[![Docker](https://img.shields.io/badge/Docker-neosun%2Ffirered--asr2s-blue?logo=docker)](https://hub.docker.com/r/neosun/firered-asr2s)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)

🌐 [デモ](https://firered-asr.aws.xin) · 📄 [API ドキュメント](https://firered-asr.aws.xin/docs)

</div>

---

## ✨ 機能

- 🎯 **SOTA 音声認識**: 中国語標準語 CER 2.89%
- 🌍 **多言語対応**: 中国語（標準語 + 20以上の方言）、英語、コードスイッチング、歌詞認識
- 🔊 **VAD**: 音声活動検出 F1 97.57%（100以上の言語）
- 🌐 **LID**: 言語識別 精度 97.18%
- 📝 **句読点予測**: 自動句読点 F1 78.90%
- ⏱️ **単語タイムスタンプ**: 文字/単語レベルのタイミング
- 🖥️ **Web UI**: ダークテーマ、4言語対応
- 🔌 **REST API**: Swagger ドキュメント付き
- 🤖 **MCP サーバー**: AI アシスタント統合
- 🐳 **All-in-One Docker**: ゼロ設定デプロイ

## 🚀 クイックスタート

```bash
docker run -d --name firered-asr2s \
  --gpus '"device=0"' \
  -p 8350:8300 -p 8351:8301 \
  -v /tmp/firered-asr2s:/tmp/firered-asr2s \
  --shm-size=4g \
  neosun/firered-asr2s:latest
```

- 🌐 UI: http://localhost:8350
- 📄 API ドキュメント: http://localhost:8350/docs

## 📡 API 使用方法

```bash
curl -X POST http://localhost:8350/api/transcribe -F "file=@audio.wav"
```

## 📄 ライセンス

Apache License 2.0。[FireRedASR2S](https://github.com/FireRedTeam/FireRedASR2S)（小紅書 FireRedTeam）に基づく。

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=neosun100/FireRedASR2S&type=Date)](https://star-history.com/#neosun100/FireRedASR2S)

## 📱 公式アカウント

![公式アカウント](https://img.aws.xin/uPic/扫码_搜索联合传播样式-标准色版.png)
