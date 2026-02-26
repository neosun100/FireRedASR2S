"""GPU resource manager with auto-offload for FireRedASR2S models."""
import os, gc, time, asyncio, subprocess
from typing import Optional, Dict, Any

IDLE_TIMEOUT = int(os.environ.get("GPU_IDLE_TIMEOUT", "600"))


class GPUManager:
    def __init__(self):
        self.asr_system = None
        self.lock = asyncio.Lock()
        self.last_used: float = 0
        self._auto_task = None

    async def get_model(self, config_overrides: dict = None):
        async with self.lock:
            if self.asr_system:
                self.last_used = time.time()
                return self.asr_system
            # lazy load
            import torch
            from fireredasr2s import FireRedAsr2System, FireRedAsr2SystemConfig
            from fireredasr2s.fireredasr2 import FireRedAsr2Config
            from fireredasr2s.fireredlid import FireRedLidConfig
            from fireredasr2s.fireredpunc import FireRedPuncConfig
            from fireredasr2s.fireredvad import FireRedVadConfig

            vad_dir = os.environ.get("VAD_MODEL_DIR", "pretrained_models/FireRedVAD/VAD")
            lid_dir = os.environ.get("LID_MODEL_DIR", "pretrained_models/FireRedLID")
            asr_type = os.environ.get("ASR_TYPE", "aed")
            asr_dir = os.environ.get("ASR_MODEL_DIR", "pretrained_models/FireRedASR2-AED")
            punc_dir = os.environ.get("PUNC_MODEL_DIR", "pretrained_models/FireRedPunc")

            co = config_overrides or {}
            vad_config = FireRedVadConfig(
                use_gpu=False,
                smooth_window_size=int(co.get("smooth_window_size", 5)),
                speech_threshold=float(co.get("speech_threshold", 0.2)),
                min_speech_frame=int(co.get("min_speech_frame", 20)),
                max_speech_frame=int(co.get("max_speech_frame", 1000)),
                min_silence_frame=int(co.get("min_silence_frame", 10)),
                merge_silence_frame=int(co.get("merge_silence_frame", 50)),
                extend_speech_frame=int(co.get("extend_speech_frame", 10)),
                chunk_max_frame=int(co.get("vad_chunk_max_frame", 30000)),
            )
            lid_config = FireRedLidConfig(use_gpu=True, use_half=False)
            asr_config = FireRedAsr2Config(
                use_gpu=True,
                use_half=False,
                beam_size=int(co.get("beam_size", 3)),
                nbest=1,
                decode_max_len=0,
                softmax_smoothing=float(co.get("softmax_smoothing", 1.25)),
                aed_length_penalty=float(co.get("aed_length_penalty", 0.6)),
                eos_penalty=float(co.get("eos_penalty", 1.0)),
                return_timestamp=True,
            )
            punc_config = FireRedPuncConfig(use_gpu=True)

            cfg = FireRedAsr2SystemConfig(
                vad_dir, lid_dir, asr_type, asr_dir, punc_dir,
                vad_config, lid_config, asr_config, punc_config,
                asr_batch_size=1, punc_batch_size=1,
                enable_vad=True, enable_lid=True, enable_punc=True,
            )
            self.asr_system = FireRedAsr2System(cfg)
            self.last_used = time.time()
            return self.asr_system

    async def offload(self):
        async with self.lock:
            return await self._offload_unlocked()

    async def _offload_unlocked(self):
        if self.asr_system:
            del self.asr_system
            self.asr_system = None
            gc.collect()
            try:
                import torch
                torch.cuda.empty_cache()
            except Exception:
                pass
        return True

    def get_status(self) -> Dict[str, Any]:
        status = {
            "model_loaded": self.asr_system is not None,
            "idle_seconds": int(time.time() - self.last_used) if self.last_used else 0,
            "idle_timeout": IDLE_TIMEOUT,
        }
        try:
            r = subprocess.run(
                ["nvidia-smi", "--query-gpu=index,name,memory.used,memory.total,utilization.gpu,temperature.gpu",
                 "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=5)
            if r.returncode == 0:
                for line in r.stdout.strip().split("\n"):
                    p = [x.strip() for x in line.split(",")]
                    if len(p) >= 6:
                        status["gpu"] = {
                            "id": int(p[0]), "name": p[1],
                            "memory_used_mb": int(p[2]), "memory_total_mb": int(p[3]),
                            "utilization_percent": int(p[4]), "temperature_c": int(p[5]),
                        }
                        break
        except Exception:
            pass
        return status

    async def auto_offload_loop(self):
        while True:
            await asyncio.sleep(60)
            if self.asr_system and self.last_used and (time.time() - self.last_used) > IDLE_TIMEOUT:
                await self.offload()


gpu_manager = GPUManager()
