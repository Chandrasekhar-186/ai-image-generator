import json, os, time
from pathlib import Path
from PIL import Image

def session_dir(base="outputs"):
    sid = time.strftime("%Y%m%d_%H%M%S")
    p = Path(base) / sid
    p.mkdir(parents=True, exist_ok=True)
    return p

def save_image(img: Image.Image, dir: Path, filename: str, fmt: str):
    path = dir / f"{filename}.{fmt.lower()}"
    img.save(path, format=fmt.upper())
    return path

def save_metadata(dir: Path, meta: dict):
    with open(dir / "metadata.json", "w") as f:
        json.dump(meta, f, indent=2)