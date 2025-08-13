import streamlit as st
from PIL import Image
from colourlesstransformer import process_image_complete, clear_output_directory
import tempfile
import os

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
            try:
                # Process the image using comprehensive function
                result_path, result_type = process_image_complete(temp_path, animation)

                # Update session state with the result
                st.session_state["generated_result"] = result_path
                st.session_state["generated_result_type"] = result_type

            finally:
                # Clean up temporary input file
                if temp_path and os.path.exists(temp_path):
                    os.unlink(temp_path)
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
    clear_output_directory()
    st.success("All generated images have been cleared.")
