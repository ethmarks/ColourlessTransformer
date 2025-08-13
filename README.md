# ColourlessTransformer

ColourlessTransformer is a simple interface for Paint Transformer, a neural network that performs *Feed Forward Neural Painting with Stroke Prediction*.

## Demo
| Original                   | ![A photo of a walkway with rose bushes](images/walkway.jpg)                            |
|----------------------------|-----------------------------------------------------------------------------------------|
| PaintTransformer           | ![A painterly image of a walkway with rose bushes](images/walkway_painttransformer.jpg) |
| PaintTransformer Animation | ![An animation of the a painterly image of a walkway](images/walkway.gif)               |

## Authors

Interface by Ethan Marks ([@ColourlessSpearmint](https://github.com/ColourlessSpearmint)).

PyTorch implementation by [@Huage001](https://github.com/Huage001).

Original paper by Songhua Liu, Tianwei Lin, Dongliang He, Fu Li, Ruifeng Deng, Xin Li, Errui Ding, and Hao Wang.

## Prerequisites

- Python 3
- Git

## Dependencies

- numpy>=2.3.2
- pillow>=11.3.0
- streamlit>=1.48.1
- torch>=2.8.0
- torchvision>=0.23.0

## Installation

1. Clone the repository

```bash
git clone https://github.com/ColourlessSpearmint/ColourlessTransformer.git
```

2. Navigate into project directory

```bash
cd ColourlessTransformer
```

3. Install the required dependencies

Installing the dependencies can be done with pip...

```bash
python -m venv
pip install .
```

...or with [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Usage

### Streamlit

You can run the Streamlit interface by running `main.py` with Python...

```bash
python main.py
```

...or with the `streamlit` command.

```bash
streamlit run app.py
```

### Drag-Drop (Windows only)

If you're on Windows, you can process images by dragging them onto painttransformer.bat. Your images will be processed automatically and saved to the directory of the input files.

## License

ColourlessTransformer is licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).
