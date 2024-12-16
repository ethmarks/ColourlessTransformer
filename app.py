import streamlit as st
from PIL import Image
import io

# Set page config to wide mode
st.set_page_config(layout="wide")

# Function to read markdown from a file
def load_markdown(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Title and Description
st.title("ColourlessTransformer")

# Load markdown from a file
markdown_path = "streamlit_description.md"
markdown_content = load_markdown(markdown_path)
st.markdown(markdown_content)

# File uploader for image input
uploaded_file = st.file_uploader("Drag and drop your image here", type=["png", "jpg", "jpeg"])

# Create two columns for side-by-side display
col1, col2 = st.columns(2)

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
        # Dummy Processing Logic
        st.write("Processing your image...")
        # Placeholder for static image generation
        processed_result = Image.new("RGB", image.size, (0, 255, 0))  # Dummy green frame

        # Display the generated image in the second column
        with col2:
            st.image(processed_result, caption="Generated Static Image", use_container_width=True)

    else:
        st.error("Please upload an image before clicking Generate.")
