from PIL import Image
import os


def make_thumbnail(image_file: str) -> Image.Image:
    with Image.open(image_file) as img:
        width, height = img.size

        # Crop to centered square if needed
        if width != height:
            side = min(width, height)
            left = (width - side) // 2
            top = (height - side) // 2
            right = left + side
            bottom = top + side
            img = img.crop((left, top, right, bottom))

        # Resize to 254x254
        img = img.resize((254, 254), Image.Resampling.LANCZOS)

        return img.copy()  # return a standalone image


def save_thumbnail(thumbnail_image: Image.Image, thumbnail_path: str) -> None:
    os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)
    thumbnail_image.save(thumbnail_path)


def make_all_thumbnails(input_dir: str, output_dir: str) -> None:
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".png"):
            image_path = os.path.join(input_dir, filename)
            thumbnail_image = make_thumbnail(image_path)

            name, _ = os.path.splitext(filename)
            thumbnail_path = os.path.join(output_dir, f"{name}.png")

            save_thumbnail(thumbnail_image, thumbnail_path)


if __name__ == "__main__":
    make_all_thumbnails("spell_images", "spell_thumbnails")
