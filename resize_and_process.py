import sys
import os
import tempfile
from PIL import Image
from inference.inference import main

def resize_image(input_path, max_dim=512):
    """
    Resize the image to fit within the maximum dimension while maintaining the aspect ratio.
    Returns a BytesIO object containing the resized image.
    """
    image = Image.open(input_path)
    resize_ratio = min(max_dim / image.width, max_dim / image.height) if image.width > max_dim or image.height > max_dim else 1
    new_size = (int(image.width * resize_ratio), int(image.height * resize_ratio))
    resized_image = image.resize(new_size, Image.LANCZOS)

    temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    resized_image.save(temp_file.name)
    return temp_file.name

def process_image(temp_file, output_path):
    """
    Run the inference process on the resized image and save the result.
    """
    temp_output_dir = "inference/output/"
    os.makedirs(temp_output_dir, exist_ok=True)

    # Run inference on the resized image
    main(input_path=temp_file, model_path="inference/model.pth", output_dir=temp_output_dir, need_animation=False, serial=False)

    # Move the final output image to the desired location
    processed_image_path = os.path.join(temp_output_dir, os.path.basename(temp_file))
    if os.path.exists(processed_image_path):
        os.rename(processed_image_path, output_path)
        print(f"Processed image saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python resize_and_process.py <image_path>")
        sys.exit(1)

    input_file = sys.argv[1]
    file_dir, file_name = os.path.split(input_file)
    file_base, file_ext = os.path.splitext(file_name)

    # Final output file with "paint-transformed" appended
    output_file = os.path.join(file_dir, f"{file_base}_painttransformed{file_ext}")

    print(f"Resizing image: {input_file}")
    with tempfile.NamedTemporaryFile(suffix=".png", delete=True) as temp_resized:
        resized_path = resize_image(input_file)
        
        print("Running inference...")
        process_image(resized_path, output_file)
