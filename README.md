# Video and Image Combiner

This Python script combines a video with an image vertically. You can choose whether to place the image above or below the video. It supports cropping the bottom portion of the video and provides various command-line options for customization.

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Windows OS

## Installation

1. Clone or download this repository
2. Run `install.bat` to install dependencies with uv

## Usage

### Using start.bat (recommended)

```batch
# Show help
start.bat --help

# Basic usage with default paths (image below video)
start.bat

# Place image on top of video
start.bat --image-position top

# Crop 50 pixels from bottom of video
start.bat --crop-bottom 50

# Custom input/output paths
start.bat --video custom_video.mp4 --image custom_image.png --output output/custom_output.mp4

# Folder mode - combine all assets in a folder
start.bat --input folder_path --constraint width
```

### Using uv directly

```batch
uv run python combine_video_image.py --help
```

## Command Line Arguments

- `--input`: Path to folder containing media files (folder mode)
- `--video`: Path to input video file (default: 'input/video.mp4')
- `--image`: Path to input image file (default: 'input/image.png')
- `--output`: Path to output video file (default: 'output/output.mp4')
- `--constraint`: Scaling constraint: 'width' or 'height' (folder mode)
- `--crop-bottom`: Number of pixels to crop from bottom of video (default: 0)
- `--image-position`: Position of image relative to video, either 'top' or 'bottom' (default: 'bottom')

## Project Structure

```
├── input/                  # Input files directory
│   ├── video.mp4          # Your input video
│   └── image.png          # Your input image
├── output/                 # Output directory for combined videos
├── src/                    # Source code package
│   ├── config/            # Configuration module
│   │   ├── constants.py   # String constants
│   │   └── settings.py    # Environment settings
│   ├── asset.py           # Asset classes (ImageAsset, VideoAsset)
│   ├── cli.py             # Command-line argument parsing
│   ├── combiner.py        # Video combining logic
│   └── utils.py           # Utility functions
├── tests/                  # Pytest test suite
├── tools/                  # Development tools
│   └── tests.bat          # Run test suite
├── .gitignore
├── combine_video_image.py  # Main entry point
├── install.bat             # Installation script (uses uv)
├── pyproject.toml          # Project configuration
├── start.bat               # Run the application
└── README.md
```

## Development

### Running Tests

```batch
tools\tests.bat
```

Or directly:

```batch
uv run pytest tests/ -v
```

## Example Output

![output](https://github.com/user-attachments/assets/a8b24a88-ad10-4299-893b-71c41aab39a9)

This example demonstrates how the script combines a video with an image. Use `--image-position top` to place the image above the video, or `--image-position bottom` (default) to place it below.

## Notes

- The script will automatically create the output directory if it doesn't exist
- Input and output directories are ignored by git to avoid committing large media files
- Environment variables can override default paths (see `src/config/settings.py`)
