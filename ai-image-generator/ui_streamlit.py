import streamlit as st
from PIL import Image
from time import time
from app.pipelines import load_pipeline, generate
from app.prompts import engineer_prompt, combine_negative
from app.filters import is_prompt_allowed
from app.watermark import add_watermark
from app.storage import session_dir, save_image, save_metadata
from app.config import DEFAULTS, DEFAULT_MODEL

st.set_page_config(page_title="AI Image Generator", page_icon="🎨", layout="wide")

st.title("AI-Powered Image Generator (Local, Open-Source)")
with st.sidebar:
    st.markdown("### Settings")
    model_id = st.selectbox("Model", [DEFAULT_MODEL, "stabilityai/stable-diffusion-xl-base-1.0"])
    style = st.selectbox("Style guidance", ["photorealistic", "artistic", "cartoon", "van_gogh"])
    num_images = st.slider("Number of images", 1, 6, DEFAULTS["num_images"])
    steps = st.slider("Steps", 10, 75, DEFAULTS["num_inference_steps"])
    guidance = st.slider("Guidance scale", 1.0, 15.0, DEFAULTS["guidance_scale"])
    width = st.selectbox("Width", [512, 640, 768, 1024], index=0)
    height = st.selectbox("Height", [512, 640, 768, 1024], index=0)
    seed = st.number_input("Seed (optional)", value=0, min_value=0, step=1)
    use_seed = st.checkbox("Use seed", value=False)
    negative_user = st.text_input("Negative prompt", DEFAULTS["negative_prompt"])
    add_wm = st.checkbox("Add watermark", value=True)
    fmt = st.selectbox("Export format", ["PNG", "JPEG"], index=0)

prompt = st.text_input("Enter your prompt", "a futuristic city at sunset, dramatic sky")
go = st.button("Generate")

status = st.empty()
progress_bar = st.progress(0)
eta_text = st.empty()

if go:
    if not is_prompt_allowed(prompt):
        st.error("Prompt appears to contain disallowed content. Please revise.")
    else:
        status.info("Loading model...")
        pipe = load_pipeline(model_id)
        status.success("Model ready.")

        full_prompt = engineer_prompt(prompt, style)
        negative_prompt = combine_negative(negative_user)

        st.write(f"Prompt: {full_prompt}")
        st.write(f"Negative: {negative_prompt}")

        t0 = time()

        def cb(step, timestep, latents):
            progress = int((step / steps) * 100)
            progress_bar.progress(min(progress, 100))
            elapsed = time() - t0
            if progress > 0:
                eta = elapsed / (progress/100) * (1 - progress/100)
                eta_text.info(f"Estimated time remaining: {int(eta)}s")

        images = generate(
            pipe=pipe, prompt=full_prompt, negative_prompt=negative_prompt,
            num_images=num_images, steps=steps, guidance=guidance,
            height=height, width=width, seed=(seed if use_seed else None),
            progress_cb=cb
        )

        out_dir = session_dir()
        meta = {
            "prompt": prompt,
            "engineered_prompt": full_prompt,
            "negative_prompt": negative_prompt,
            "model": model_id,
            "params": {
                "num_images": num_images, "steps": steps, "guidance": guidance,
                "height": height, "width": width, "seed": (seed if use_seed else None)
            },
            "timestamp": int(time())
        }

        cols = st.columns(len(images))
        for i, img in enumerate(images):
            if add_wm:
                img = add_watermark(img, text="AI-Generated")
            fname = f"image_{i+1}"
            path = save_image(img, out_dir, fname, fmt)
            cols[i].image(img, caption=str(path), use_column_width=True)
            cols[i].download_button("Download", data=open(path, "rb").read(), file_name=path.name)

        save_metadata(out_dir, meta)
        status.success(f"Finished in {int(time()-t0)}s. Saved to {out_dir}")
        eta_text.empty()
        progress_bar.empty()