from PIL import Image, ImageEnhance
import os
import numpy as np

def adjust_all_thumbnails(thumbnail_dir: str) -> None:
    for filename in os.listdir(thumbnail_dir):
        if filename.lower().endswith(".png"):
            thumbnail_path = os.path.join(thumbnail_dir, filename)
            adjust_brightness(thumbnail_path, 0.75)

def adjust_brightness(image_path, factor):
    """
    Adjust image brightness using gamma correction.

    factor < 1.0: Brighten, lifting shadows more than highlights.
    factor = 1.0: No change.
    factor > 1.0: Darken, suppressing shadows more than highlights.
    """
    with Image.open(image_path) as img:
        # Preserve transparency if present
        has_alpha = img.mode in ("RGBA", "LA") or "transparency" in img.info
        img = img.convert("RGBA" if has_alpha else "RGB")

        arr = np.asarray(img).copy()
        rgb = arr[..., :3].astype(np.float32) / 255.0

        # Gamma < 1 brightens; gamma > 1 darkens
        gamma = factor
        adjusted = np.power(rgb, gamma)

        arr[..., :3] = np.clip(adjusted * 255, 0, 255).astype(np.uint8)

        result = Image.fromarray(arr, mode=img.mode)
        result.save(image_path, format="PNG")
        
      
if __name__ == "__main__":
    adjust_all_thumbnails("spell_thumbnails")
