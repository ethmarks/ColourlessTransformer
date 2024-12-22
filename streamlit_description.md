# Colourless Transformer

Created by **Ethan Marks** ([@ColourlessSpearmint](https://github.com/ColourlessSpearmint)).

**ColourlessTransformer** is an interface for the Paint Transformer neural network, which performs feed-forward neural painting with stroke prediction.

## Usage

### **Upload an Image**

Use the file uploader to drag and drop an image or select it from your file system. Supported formats: .png, .jpg, .jpeg.

The app will automatically resize the image to a maximum of 512 pixels. This will drastically decrease processing time for large images without significantly affecting output quality. 

### **Choose Output Format**

Animation Toggle: Enable the checkbox to generate an animation (GIF) instead of a static image.

### **Generate Results**

Click the Generate button to process your uploaded image. Depending on your hardware, the processing should take between a few seconds and a few minutes.

### **View Results**

Once processing is complete, view the result in the right column. You can download the result by right-clicking and selecting "Save Image As..."