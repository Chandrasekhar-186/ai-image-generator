import re

BANNED = [
    r"\b(nsfw|explicit|sexual|gore|hate)\b",
]

def is_prompt_allowed(prompt: str) -> bool:
    text = prompt.lower()
    return not any(re.search(p, text) for p in BANNED)