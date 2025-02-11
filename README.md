# ImageFlow

A simple command-line tool for batch image processing.

## Features
- Resize images with aspect ratio preservation
- Convert between formats (PNG, JPG, WebP, etc.)
- Batch processing for entire directories
- Smart format handling (RGB conversion for JPEG)

## Installation
```bash
pip install -r requirements.txt
```

## Usage

### Resize an image
```bash
python imageflow.py resize image.jpg --width 800
python imageflow.py resize image.jpg --height 600
python imageflow.py resize image.jpg --width 800 --height 600 --output resized.jpg
```

### Convert image format
```bash
python imageflow.py convert image.png --format jpg
python imageflow.py convert image.jpg --format webp --output converted.webp
```

### Batch processing
```bash
# Resize all images in directory
python imageflow.py batch ./images --width 800

# Convert all JPGs to PNG
python imageflow.py batch ./images --pattern "*.jpg" --format png

# Resize and convert with output directory
python imageflow.py batch ./images --width 600 --format webp --output-dir ./processed
```

### Get help
```bash
python imageflow.py --help
python imageflow.py resize --help
python imageflow.py convert --help
python imageflow.py batch --help
```