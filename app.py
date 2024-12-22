import streamlit as st
from PIL import Image
from inference.inference import main
import glob
import os
import tempfile

# Set page config to wide mode
st.set_page_config(layout="wide")


# Function to read markdown from a file
def load_markdown(file_path):
    with open(file_path, "r") as file:
        return file.read()


# Load markdown description from a file
markdown_path = "streamlit_description.md"
markdown_content = load_markdown(markdown_path)
st.markdown(markdown_content)

# Initialize session state variables if not already set
if "generated_result" not in st.session_state:
    st.session_state["generated_result"] = None
if "generated_result_type" not in st.session_state:
    st.session_state["generated_result_type"] = None

# File uploader for image input
uploaded_file = st.file_uploader(
    "Drag and drop your image here", type=["png", "jpg", "jpeg"]
)

# Create two columns for side-by-side display
col1, col2 = st.columns(2)

# Checkbox to toggle animation
animation = st.checkbox("Animation")

# Check if a file has been uploaded
if uploaded_file is not None:
    # Open the image
    image = Image.open(uploaded_file)

    # Check if the image dimensions exceed 512px
    max_dimension = 512
    if image.width > max_dimension or image.height > max_dimension:
        # Calculate the new size while maintaining the aspect ratio
        resize_ratio = min(max_dimension / image.width, max_dimension / image.height)
        new_size = (int(image.width * resize_ratio), int(image.height * resize_ratio))

        # Resize the image
        image = image.resize(new_size, Image.LANCZOS)

    # Display the uploaded image in the first column
    with col1:
        st.image(image, caption="Uploaded Image", use_container_width=True)

# Generate Button
if st.button("Generate"):
    if uploaded_file is not None:
        # Save the uploaded file to a temporary path
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_path = temp_file.name
            image.save(temp_path)

        # Simulate a processing delay
        with st.spinner("Processing your image..."):
            output_dir = "inference/output/"
            os.makedirs(output_dir, exist_ok=True)

            # Run the PaintTransformer inference function
            main(
                input_path=temp_path,
                model_path="inference/model.pth",
                output_dir=output_dir,
                need_animation=animation,
                serial=animation,
            )

            # Handle the results
            if animation:
                # Create gif from generated output images
                filename = os.path.splitext(os.path.basename(temp_path))[0]
                in_dir = os.path.join(output_dir, filename, "*.jpg")
                out_path = f"{output_dir}/animation.gif"
                img, *imgs = [Image.open(f) for f in sorted(glob.glob(in_dir))]
                img.save(
                    fp=out_path,
                    format="GIF",
                    append_images=imgs,
                    save_all=True,
                    duration=100,
                    loop=0,
                )

                # Update session state with the GIF path
                st.session_state["generated_result"] = out_path
                st.session_state["generated_result_type"] = "gif"
            else:
                # Get the last generated image
                final_image_path = os.path.join(
                    output_dir, os.path.basename(temp_file.name)
                )

                # Update session state with the static image path
                st.session_state["generated_result"] = final_image_path
                st.session_state["generated_result_type"] = "static"
    else:
        st.error("Please upload an image before clicking Generate.")

# Display the generated result from session state
if st.session_state["generated_result"]:
    with col2:
        if st.session_state["generated_result_type"] == "gif":
            st.image(
                st.session_state["generated_result"],
                caption="Generated Animation",
                use_container_width=True,
            )
        else:
            st.image(
                st.session_state["generated_result"],
                caption="Generated Static Image",
                use_container_width=True,
            )

# Button to clear all image files from output directory
if st.button("Clear Output Directory"):
    output_dir = "inference/output/"
    # Get all image files in the output directory
    image_files = (
        glob.glob(os.path.join(output_dir, "*.png"))
        + glob.glob(os.path.join(output_dir, "*.jpg"))
        + glob.glob(os.path.join(output_dir, "*.jpeg"))
    )

    # Delete all the files
    for file in image_files:
        os.remove(file)

    st.success("All generated images have been cleared.")
