#!/usr/bin/env python3
"""Free-first video generator: tries each backend that has a key in the environment.

Backends (first available wins, override with --backend):
  pollinations  POLLINATIONS_KEY   wan-2.2-fast etc. via gen.pollinations.ai
  hf            HF_TOKEN           Hugging Face ZeroGPU Space (LTX-Video distilled)
  hf-anon       (none)             same Space, shared anonymous quota (often exhausted)

Usage: generate.py "prompt" OUT.mp4 [--seconds 8] [--backend NAME] [--model MODEL]
"""
import argparse
import os
import shutil
import sys
import urllib.parse
import urllib.request

NEG = "worst quality, cartoon, text, watermark, distorted, jittery, extra limbs"


def pollinations(prompt, out, seconds, model):
    key = os.environ["POLLINATIONS_KEY"]
    q = urllib.parse.urlencode({"model": model or "alibaba/wan-2.2-fast",
                                "duration": seconds, "aspectRatio": "9:16"})
    url = f"https://gen.pollinations.ai/image/{urllib.parse.quote(prompt)}?{q}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=600) as r, open(out, "wb") as f:
        if "video" not in r.headers.get("Content-Type", ""):
            raise RuntimeError(f"pollinations returned {r.headers.get('Content-Type')}: {r.read(300)!r}")
        shutil.copyfileobj(r, f)


def hf(prompt, out, seconds, model, token=None):
    from gradio_client import Client
    space = model or "Lightricks/ltx-video-distilled"
    c = Client(space, token=token) if token else Client(space)
    r = c.predict(prompt=prompt, negative_prompt=NEG, input_image_filepath=None,
                  input_video_filepath=None, height_ui=1024, width_ui=576,
                  mode="text-to-video", duration_ui=min(seconds, 8), ui_frames_to_use=9,
                  seed_ui=42, randomize_seed=True, ui_guidance_scale=1,
                  improve_texture_flag=True, api_name="/text_to_video")
    shutil.copy(r[0]["video"], out)


BACKENDS = {
    "pollinations": (lambda: "POLLINATIONS_KEY" in os.environ, pollinations),
    "hf": (lambda: "HF_TOKEN" in os.environ,
           lambda p, o, s, m: hf(p, o, s, m, os.environ["HF_TOKEN"])),
    "hf-anon": (lambda: True, hf),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("out")
    ap.add_argument("--seconds", type=int, default=8)
    ap.add_argument("--backend")
    ap.add_argument("--model")
    a = ap.parse_args()
    names = [a.backend] if a.backend else [n for n, (ok, _) in BACKENDS.items() if ok()]
    for name in names:
        try:
            BACKENDS[name][1](a.prompt, a.out, a.seconds, a.model)
            print(f"ok {name} -> {a.out}")
            return
        except Exception as e:
            print(f"{name} failed: {e}", file=sys.stderr)
    sys.exit("no backend succeeded")


if __name__ == "__main__":
    main()
