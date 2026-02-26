FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 python3.10-dev python3.10-venv python3-pip \
    git wget ffmpeg libsndfile1 sox ca-certificates curl \
    && rm -rf /var/lib/apt/lists/* \
    && ln -sf /usr/bin/python3.10 /usr/bin/python3 \
    && ln -sf /usr/bin/python3.10 /usr/bin/python

WORKDIR /workspace

RUN pip3 install --no-cache-dir -U pip setuptools wheel

# Install PyTorch + deps
COPY requirements.txt /workspace/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Install web server deps
RUN pip3 install --no-cache-dir fastapi uvicorn python-multipart fastmcp

# Copy project code
COPY fireredasr2s/ /workspace/fireredasr2s/
COPY app/ /workspace/app/
COPY assets/ /workspace/assets/

# Download models (embedded in image)
RUN python3 -c "from huggingface_hub import snapshot_download; \
    snapshot_download('FireRedTeam/FireRedASR2-AED', local_dir='/workspace/pretrained_models/FireRedASR2-AED'); \
    snapshot_download('FireRedTeam/FireRedVAD', local_dir='/workspace/pretrained_models/FireRedVAD'); \
    snapshot_download('FireRedTeam/FireRedLID', local_dir='/workspace/pretrained_models/FireRedLID'); \
    snapshot_download('FireRedTeam/FireRedPunc', local_dir='/workspace/pretrained_models/FireRedPunc')"

ENV PYTHONPATH=/workspace
ENV PATH=/workspace/fireredasr2s:$PATH
ENV VAD_MODEL_DIR=/workspace/pretrained_models/FireRedVAD/VAD
ENV LID_MODEL_DIR=/workspace/pretrained_models/FireRedLID
ENV ASR_TYPE=aed
ENV ASR_MODEL_DIR=/workspace/pretrained_models/FireRedASR2-AED
ENV PUNC_MODEL_DIR=/workspace/pretrained_models/FireRedPunc
ENV PORT=8300
ENV MCP_PORT=8301
ENV GPU_IDLE_TIMEOUT=600

EXPOSE 8300 8301

WORKDIR /workspace/app
CMD ["sh", "-c", "python3 mcp_server.py & python3 -m uvicorn server:app --host 0.0.0.0 --port ${PORT}"]
