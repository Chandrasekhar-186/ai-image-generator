import torch
from diffusers import StableDiffusionPipeline, DiffusionPipeline
from app.config import DEFAULT_MODEL, OPTIONAL_MODEL_SDXL, device

def load_pipeline(model_id: str = DEFAULT_MODEL):
    dev = device()
    if "sdxl" in model_id.lower():
        pipe = DiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16 if dev=="cuda" else torch.float32)
    else:
        pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16 if dev=="cuda" else torch.float32)

    if dev == "cuda":
        pipe = pipe.to(dev)
        pipe.enable_xformers_memory_efficient_attention()
    else:
        # CPU safety: disable features that require CUDA
        pass

    # Safety checker can be kept or replaced with a simple filter in filters.py
    return pipe

def generate(pipe, prompt, negative_prompt, num_images, steps, guidance, height, width, seed=None, progress_cb=None):
    g = None
    if seed is not None:
        g = torch.Generator(device=device())
        g.manual_seed(seed)

    images = []
    for i in range(num_images):
        out = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=steps,
            guidance_scale=guidance,
            height=height,
            width=width,
            generator=g,
            callback=progress_cb,
            callback_steps=max(1, steps//10),
        )
        images.append(out.images[0])
    return images