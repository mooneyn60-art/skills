#!/usr/bin/env python3
"""Self-hosted text-to-video on CPU: LTX-Video 2B distilled, no GPU, no API key.

Memory plan (15 GB box): encode the prompt with T5-XXL (bf16, ~9.5 GB), free it,
then load the 2B transformer + VAE to denoise and decode.

Usage: gen_cpu.py "prompt" OUT.mp4 [--w 288 --h 512 --frames 41 --steps 8 --fps 12]
Models dir defaults to $MODELS or the session scratchpad models folder.
"""
import argparse
import gc
import os
import time

import torch
from diffusers import AutoencoderKLLTXVideo, FlowMatchEulerDiscreteScheduler, LTXPipeline, LTXVideoTransformer3DModel
from diffusers.utils import export_to_video
from transformers import T5EncoderModel, T5TokenizerFast

DEFAULT_MODELS = "/tmp/claude-0/-home-user/f2581a8c-fe42-5876-b5f9-d941a863a7fa/scratchpad/models"
NEG = "worst quality, cartoon, text, watermark, inconsistent motion, blurry, jittery, distorted"


def encode(models, prompt):
    tok = T5TokenizerFast.from_pretrained(f"{models}/ltx/tokenizer")
    enc = T5EncoderModel.from_pretrained(f"{models}/t5", torch_dtype=torch.bfloat16, low_cpu_mem_usage=True)
    out = []
    with torch.no_grad():
        for text in (prompt, NEG):
            t = tok(text, padding="max_length", max_length=128, truncation=True, return_tensors="pt")
            emb = enc(t.input_ids, attention_mask=t.attention_mask)[0].float()
            out += [emb, t.attention_mask]
    del enc
    gc.collect()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("out")
    ap.add_argument("--w", type=int, default=288)
    ap.add_argument("--h", type=int, default=512)
    ap.add_argument("--frames", type=int, default=41)
    ap.add_argument("--steps", type=int, default=8)
    ap.add_argument("--fps", type=int, default=12)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--models", default=os.environ.get("MODELS", DEFAULT_MODELS))
    a = ap.parse_args()
    torch.set_num_threads(os.cpu_count())
    t0 = time.time()
    pe, pm, ne, nm = encode(a.models, a.prompt)
    print(f"encoded in {time.time() - t0:.0f}s", flush=True)

    ckpt = f"{a.models}/ltxv-2b-0.9.6-distilled-04-25.safetensors"
    transformer = LTXVideoTransformer3DModel.from_single_file(ckpt, torch_dtype=torch.float32)
    vae = AutoencoderKLLTXVideo.from_single_file(ckpt, torch_dtype=torch.float32)
    sched = FlowMatchEulerDiscreteScheduler.from_pretrained(f"{a.models}/ltx/scheduler")
    pipe = LTXPipeline(scheduler=sched, vae=vae, text_encoder=None, tokenizer=None, transformer=transformer)
    vae.enable_tiling()

    t1 = time.time()
    latents = pipe(prompt_embeds=pe, prompt_attention_mask=pm,
                   negative_prompt_embeds=ne, negative_prompt_attention_mask=nm,
                   width=a.w, height=a.h, num_frames=a.frames, num_inference_steps=a.steps,
                   guidance_scale=1.0, output_type="latent",
                   generator=torch.Generator().manual_seed(a.seed)).frames
    print(f"denoised in {time.time() - t1:.0f}s", flush=True)

    # Decoding next to the 2B transformer OOMs a 15 GB box; free it first.
    sp, tp = transformer.config.patch_size, transformer.config.patch_size_t
    pipe.transformer = None
    del transformer
    gc.collect()
    lf = (a.frames - 1) // pipe.vae_temporal_compression_ratio + 1
    lh, lw = a.h // pipe.vae_spatial_compression_ratio, a.w // pipe.vae_spatial_compression_ratio
    lat = pipe._unpack_latents(latents, lf, lh, lw, sp, tp)
    lat = pipe._denormalize_latents(lat, vae.latents_mean, vae.latents_std, vae.config.scaling_factor)
    ts = torch.tensor([0.05]) if vae.config.timestep_conditioning else None
    if ts is not None:
        lat = 0.975 * lat + 0.025 * torch.randn_like(lat)
    with torch.no_grad():
        frames = vae.decode(lat, ts, return_dict=False)[0]
    video = pipe.video_processor.postprocess_video(frames, output_type="pil")[0]
    export_to_video(video, a.out, fps=a.fps)
    print(f"ok {a.out} denoise+decode {time.time() - t1:.0f}s total {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
