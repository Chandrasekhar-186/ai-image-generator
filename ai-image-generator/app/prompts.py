STYLE_PRESETS = {
    "photorealistic": [
        "highly detailed", "4K", "sharp focus", "professional photography",
        "global illumination", "volumetric lighting"
    ],
    "artistic": [
        "concept art", "intricate", "golden ratio", "rich color grading",
        "digital painting"
    ],
    "cartoon": [
        "cel shading", "bold outlines", "vibrant colors", "clean line art",
        "studio quality"
    ],
    "van_gogh": ["in the style of Vincent van Gogh", "impasto", "swirling brushstrokes"]
}

def engineer_prompt(user_prompt: str, style: str):
    boosters = STYLE_PRESETS.get(style, STYLE_PRESETS["photorealistic"])
    return f"{user_prompt}, " + ", ".join(boosters)

def combine_negative(user_negative: str):
    base = "low quality, blurry, deformed, extra limbs, nsfw, text, artifacts"
    if user_negative and user_negative.strip():
        return f"{base}, {user_negative.strip()}"
    return base