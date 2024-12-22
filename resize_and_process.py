import sys
import os
from PIL import Image
from inference.inference import main

def resize_image(input_path, output_path, max_dim=512):
    """
    Resize the image to fit within the maximum dimension while maintaining aspect ratio.
    """
    image = Image.open(input_path)
    resize_ratio = min(max_dim / image.width, max_dim / image.height) if image.width > max_dim or image.height > max_dim else 1
    new_size = (int(image.width * resize_ratio), int(image.height * resize_ratio))
    image.resize(new_size, Image.LANCZOS).save(output_path)
    print(f"Resized image saved to {output_path}")

def process_image(resized_path):
    """
    Call the `main` function from the inference module to process the image.
    """
    output_dir = "inference/output/"
    os.makedirs(output_dir, exist_ok=True)
    main(input_path=resized_path, model_path="inference/model.pth", output_dir=output_dir, need_animation=False, serial=False)
    print(f"Processed image saved to {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python resize_and_process.py <image_path>")
        sys.exit(1)

    input_file = sys.argv[1]
    temp_resized = "temp_resized.png"

    try:
        print(f"Resizing image: {input_file}")
        resize_image(input_file, temp_resized)

        print("Running inference...")
        process_image(temp_resized)
    finally:
        if os.path.exists(temp_resized):
            os.remove(temp_resized)
            print("Temporary resized file deleted.")
