"""
ColourlessTransformer - Neural Network Paint Transformer Interface

This module provides a Python interface for Paint Transformer, a neural network that performs
feed-forward neural painting with stroke prediction. It can process images to create painterly
transformations, either as static images or animated sequences showing the painting process.

The module can be used both as a command-line tool and as a Python library.

Command Line Usage:
    python colourlesstransformer.py <image_path> [--animation] [--no-resize]

Python API Usage:
    from colourlesstransformer import process_image_complete

    result_path, result_type = process_image_complete(
        input_path="image.jpg",
        animation=False,
        resize=True
    )

Dependencies:
    - numpy
    - pillow
    - torch
    - torchvision

Author: Ethan Marks (@ethmarks)
Based on Paint Transformer by Songhua Liu et al.
"""

import sys
import os
import tempfile
import glob
from PIL import Image
from inference.inference import main


def resize_image(input_path, max_dim=512):
    """
    Resize the image to fit within the maximum dimension while maintaining the aspect ratio.

    Args:
        input_path (str): Path to the input image file
        max_dim (int): Maximum dimension (width or height) for the resized image. Defaults to 512.

    Returns:
        str: Path to the temporary file containing the resized image

    Note:
        The resized image is saved to a temporary file that should be cleaned up after use.
        The aspect ratio is preserved during resizing.
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


def copy_image_to_temp(input_path):
    """
    Copy the image to a temporary file without resizing.

    Args:
        input_path (str): Path to the input image file

    Returns:
        str: Path to the temporary file containing the copied image

    Note:
        This function is used when processing images at their original size.
        The temporary file should be cleaned up after use.
    """
    image = Image.open(input_path)
    temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    image.save(temp_file.name)
    return temp_file.name


def create_animation_gif(temp_file_path, output_dir="inference/output/"):
    """
    Create a GIF animation from the generated frame sequence.

    Args:
        temp_file_path (str): Path to the temporary file used for processing
        output_dir (str): Directory containing the generated animation frames.
                         Defaults to "inference/output/"

    Returns:
        str or None: Path to the created GIF file, or None if no frames were found

    Note:
        This function looks for .jpg files in a subdirectory named after the temp file
        and combines them into an animated GIF with 100ms frame duration.
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
    Clear all image files and subdirectories from the output directory.

    Args:
        output_dir (str): Directory to clear. Defaults to "inference/output/"

    Note:
        This function removes all image files (.png, .jpg, .jpeg, .gif) and
        subdirectories containing animation frames from the specified directory.
        Use with caution as this permanently deletes files.
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
    Run the neural network inference process on the image and save the result.

    Args:
        temp_file (str): Path to the temporary image file to process
        output_path (str, optional): Desired output path. If None, saves to output directory.
        need_animation (bool): Whether to generate animation frames. Defaults to False.
        serial (bool): Whether to process frames serially. Defaults to False.

    Returns:
        str or None: Path to the processed image, or None if processing failed

    Note:
        This function calls the main inference routine from the inference module.
        The model file is expected to be at "inference/model.pth".
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


def process_image_complete(input_path, animation=False, output_path=None, resize=True):
    """
    Complete image processing workflow: optionally resize, process, and optionally create animation.

    This is the main function for processing images with Paint Transformer. It handles the complete
    workflow from input to output, including optional resizing, neural network inference, and
    animation generation.

    Args:
        input_path (str): Path to the input image file. Supports common formats (jpg, png, etc.)
        animation (bool, optional): If True, generates an animated GIF showing the painting process.
                                   If False, generates a static paint-transformed image.
                                   Defaults to False.
        output_path (str, optional): Custom path for the output file. If None, saves to the same
                                    directory as input with '_painttransformed' suffix.
                                    Defaults to None.
        resize (bool, optional): If True, resizes the image to fit within 512px maximum dimension
                                while maintaining aspect ratio. If False, processes at original size.
                                Larger images may take significantly longer to process.
                                Defaults to True.

    Returns:
        tuple: A tuple containing (result_path, result_type) where:
            - result_path (str): Full path to the generated output file
            - result_type (str): Type of output created, either 'static' or 'gif'

    Raises:
        FileNotFoundError: If the input image file doesn't exist
        PIL.UnidentifiedImageError: If the input file is not a valid image
        Exception: If the neural network inference fails

    Example:
        >>> # Process image with default settings
        >>> result_path, result_type = process_image_complete("photo.jpg")
        >>> print(f"Created {result_type} at: {result_path}")

        >>> # Generate animation at original size
        >>> result_path, result_type = process_image_complete(
        ...     "photo.jpg",
        ...     animation=True,
        ...     resize=False
        ... )
    """
    # Resize or copy the image
    if resize:
        processed_path = resize_image(input_path)
    else:
        processed_path = copy_image_to_temp(input_path)

    try:
        # Process the image
        result_path = process_image(
            processed_path,
            output_path=output_path,
            need_animation=animation,
            serial=animation
        )

        if animation:
            # Create GIF from animation frames
            gif_path = create_animation_gif(processed_path)
            if gif_path:
                return gif_path, "gif"
            else:
                # Fallback to static image if GIF creation fails
                return result_path, "static"
        else:
            return result_path, "static"

    finally:
        # Clean up temporary processed file
        if os.path.exists(processed_path):
            os.unlink(processed_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python colourlesstransformer.py <image_path> [--animation] [--no-resize]")
        sys.exit(1)

    input_file = sys.argv[1]
    animation = "--animation" in sys.argv
    resize = "--no-resize" not in sys.argv

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
    if resize:
        print("Resizing image to 512px maximum dimension")
    else:
        print("Processing image at original size")

    result_path, result_type = process_image_complete(input_file, animation, output_file, resize)

    if result_path:
        print(f"Successfully created {result_type}: {result_path}")
    else:
        print("Processing failed")
        sys.exit(1)
