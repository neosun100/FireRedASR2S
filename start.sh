#!/bin/bash
set -e

echo "🔥 FireRedASR2S — Starting..."

# Check nvidia-docker
if ! command -v nvidia-smi &>/dev/null; then
    echo "❌ nvidia-smi not found. Please install NVIDIA drivers."
    exit 1
fi
if ! docker info 2>/dev/null | grep -q "Runtimes.*nvidia"; then
    echo "⚠️  nvidia-docker runtime not detected, trying deploy.resources.reservations approach..."
fi

# Auto-select GPU with most free memory
GPU_ID=$(nvidia-smi --query-gpu=index,memory.free --format=csv,noheader,nounits | sort -t',' -k2 -rn | head -1 | cut -d',' -f1 | tr -d ' ')
export GPU_ID=${GPU_ID:-2}
echo "🎮 Using GPU $GPU_ID (most free memory)"

# Write .env
cp .env.example .env 2>/dev/null || true
sed -i "s/^GPU_ID=.*/GPU_ID=$GPU_ID/" .env

# Create tmp dir
mkdir -p /tmp/firered-asr2s

# Build and start
docker compose up -d --build

echo ""
echo "✅ FireRedASR2S running!"
echo "   🌐 UI:       http://0.0.0.0:8300"
echo "   📄 API Docs: http://0.0.0.0:8300/docs"
echo "   🔌 MCP:      port 8301"
echo "   🎮 GPU:      $GPU_ID"
