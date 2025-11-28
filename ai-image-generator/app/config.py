import torch

DEFAULT_MODEL = "runwayml/stable-diffusion-v1-5"
OPTIONAL_MODEL_SDXL = "stabilityai/stable-diffusion-xl-base-1.0"

# Generation defaults
DEFAULTS = {
    "num_inference_steps": 30,
    "guidance_scale": 7.5,
    "height": 512,
    "width": 512,
    "num_images": 1,
    "style": "photorealistic",
    "negative_prompt": "low quality, blurry, deformed, nsfw, watermark, text",
    "seed": None,
}

def device():
    return "cuda" if torch.cuda.is_available() else "cpu"