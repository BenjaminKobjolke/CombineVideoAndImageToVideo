# Video and Image Combiner

This Python script combines a video with an image, placing the video on top and the image below it. It supports cropping the bottom portion of the video and provides various command-line options for customization.

## Requirements

- Python 3.x
- Windows OS

## Installation

1. Clone or download this repository
2. Run `install.bat` to:
   - Create a Python virtual environment
   - Install required dependencies

## Usage

1. Prepare your files:

   - Place your video in the `input` folder as `video.mp4`
   - Place your image in the `input` folder as `image.png`
   - Or use custom paths with command-line arguments

2. Activate the virtual environment:

   ```batch
   activate_environment.bat
   ```

3. Run the script:

   ```batch
   # Basic usage with default paths
   python combine_video_image.py

   # Crop 50 pixels from bottom of video
   python combine_video_image.py --crop-bottom 50

   # Custom input/output paths
   python combine_video_image.py --video custom_video.mp4 --image custom_image.png --output output/custom_output.mp4
   ```

## Command Line Arguments

- `--video`: Path to input video file (default: 'input/video.mp4')
- `--image`: Path to input image file (default: 'input/image.png')
- `--output`: Path to output video file (default: 'output/output.mp4')
- `--crop-bottom`: Number of pixels to crop from bottom of video (default: 0)

## Project Structure

```
├── input/              # Input files directory
│   ├── video.mp4      # Your input video
│   └── image.png      # Your input image
├── output/            # Output directory for combined videos
├── venv/              # Python virtual environment (created by install.bat)


├── .gitignore         # Git ignore file
├── activate_environment.bat  # Script to activate virtual environment
├── combine_video_image.py   # Main Python script
├── install.bat        # Installation script
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Example Output

![output](https://github.com/user-attachments/assets/a8b24a88-ad10-4299-893b-71c41aab39a9)

This example demonstrates how the script combines a video with an image, placing the video on top and the image below it.

## Notes

- The script will automatically create the output directory if it doesn't exist
- Input and output directories are ignored by git to avoid committing large media files
