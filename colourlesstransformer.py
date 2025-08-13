import sys
import os
import tempfile
import glob
from PIL import Image
from inference.inference import main


def resize_image(input_path, max_dim=512):
    """
    Resize the image to fit within the maximum dimension while maintaining the aspect ratio.
    Returns a BytesIO object containing the resized image.
    """
    image = Image.open(input_path)
    resize_ratio = (
        min(max_dim / image.width, max_dim / image.height)
        if image.width > max_dim or image.height > max_dim
        else 1
    )
    new_size = (int(image.width * resize_ratio), int(image.height * resize_ratio))
    resized_image = image.resize(new_size, Image.LANCZOS)

    temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    resized_image.save(temp_file.name)
    return temp_file.name


def create_animation_gif(temp_file_path, output_dir="inference/output/"):
    """
    Create a GIF animation from the generated frame sequence.
    Returns the path to the created GIF file.
    """
    filename = os.path.splitext(os.path.basename(temp_file_path))[0]
    in_dir = os.path.join(output_dir, filename, "*.jpg")
    out_path = os.path.join(output_dir, "animation.gif")

    frame_files = sorted(glob.glob(in_dir))
    if not frame_files:
        return None

    img, *imgs = [Image.open(f) for f in frame_files]
    img.save(
        fp=out_path,
        format="GIF",
        append_images=imgs,
        save_all=True,
        duration=100,
        loop=0,
    )
    return out_path


def clear_output_directory(output_dir="inference/output/"):
    """
    Clear all image files from the output directory.
    """
    # Get all image files in the output directory
    image_files = (
        glob.glob(os.path.join(output_dir, "*.png"))
        + glob.glob(os.path.join(output_dir, "*.jpg"))
        + glob.glob(os.path.join(output_dir, "*.jpeg"))
        + glob.glob(os.path.join(output_dir, "*.gif"))
    )

    # Delete all the files
    for file in image_files:
        os.remove(file)

    # Also remove subdirectories with animation frames
    for item in os.listdir(output_dir):
        item_path = os.path.join(output_dir, item)
        if os.path.isdir(item_path):
            import shutil
            shutil.rmtree(item_path)


def process_image(temp_file, output_path=None, need_animation=False, serial=False):
    """
    Run the inference process on the resized image and save the result.
    If output_path is None, returns the path to the processed image in the output directory.
    """
    temp_output_dir = "inference/output/"
    os.makedirs(temp_output_dir, exist_ok=True)

    # Run inference on the resized image
    main(
        input_path=temp_file,
        model_path="inference/model.pth",
        output_dir=temp_output_dir,
        need_animation=need_animation,
        serial=serial,
    )

    # Handle the output
    processed_image_path = os.path.join(temp_output_dir, os.path.basename(temp_file))

    if output_path:
        # Move the final output image to the desired location
        if os.path.exists(processed_image_path):
            os.rename(processed_image_path, output_path)
            print(f"Processed image saved to {output_path}")
            return output_path
    else:
        # Return the path to the processed image
        return processed_image_path if os.path.exists(processed_image_path) else None


def process_image_complete(input_path, animation=False, output_path=None):
    """
    Complete image processing workflow: resize, process, and optionally create animation.
    Returns a tuple of (result_path, result_type) where result_type is 'static' or 'gif'.
    """
    # Resize the image
    resized_path = resize_image(input_path)

    try:
        # Process the image
        processed_path = process_image(
            resized_path,
            output_path=output_path,
            need_animation=animation,
            serial=animation
        )

        if animation:
            # Create GIF from animation frames
            gif_path = create_animation_gif(resized_path)
            if gif_path:
                return gif_path, "gif"
            else:
                # Fallback to static image if GIF creation fails
                return processed_path, "static"
        else:
            return processed_path, "static"

    finally:
        # Clean up temporary resized file
        if os.path.exists(resized_path):
            os.unlink(resized_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python colourlesstransformer.py <image_path> [--animation]")
        sys.exit(1)

    input_file = sys.argv[1]
    animation = "--animation" in sys.argv

    file_dir, file_name = os.path.split(input_file)
    file_base, file_ext = os.path.splitext(file_name)

    # Final output file with "paint-transformed" appended
    if animation:
        output_file = os.path.join(file_dir, f"{file_base}_painttransformed.gif")
    else:
        output_file = os.path.join(file_dir, f"{file_base}_painttransformed{file_ext}")

    print(f"Processing image: {input_file}")
    if animation:
        print("Animation mode enabled")

    result_path, result_type = process_image_complete(input_file, animation, output_file)

    if result_path:
        print(f"Successfully created {result_type}: {result_path}")
    else:
        print("Processing failed")
        sys.exit(1)
