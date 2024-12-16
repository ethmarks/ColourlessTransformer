import streamlit as st
from PIL import Image
import io

# Title and Description
st.title("ColourlessTransformer")
st.markdown("""
**ColourlessTransformer** is an interface for the Paint Transformer neural network, which performs feed-forward neural painting with stroke prediction.
""")

# File uploader for image input
uploaded_file = st.file_uploader("Drag and drop your image here", type=["png", "jpg", "jpeg"])

# Generate Button
if st.button("Generate"):
    if uploaded_file is not None:
        # Open the image
        image = Image.open(uploaded_file)

        # Display the uploaded image
        st.image(image, caption="Uploaded Image", use_container_width=True)

        # Dummy Processing Logic
        st.write("Processing your image...")
        # Placeholder for static image generation
        processed_result = Image.new("RGB", image.size, (0, 255, 0))  # Dummy green frame
        st.image(processed_result, caption="Generated Static Image", use_container_width=True)

    else:
        st.error("Please upload an image before clicking Generate.")
