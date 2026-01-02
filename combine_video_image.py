#!/usr/bin/env python3
"""Combine video and image assets into a single video.

Usage:
    Folder mode (new):
        python combine_video_image.py --input test/ --constraint width

    Legacy mode:
        python combine_video_image.py --video input/video.mp4 --image input/image.png
"""

import os
import sys

from src.cli import parse_args, get_mode
from src.combiner import VideoCombiner
from src.config import SETTINGS


def main() -> None:
    args = parse_args()
    mode, error = get_mode(args)

    if mode == 'error':
        print(f"Error: {error}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    combiner = VideoCombiner(constraint=args.constraint)

    try:
        if mode == 'folder':
            print(f"Combining assets from folder: {args.input}")
            combiner.combine_from_folder(args.input, args.output)
        elif mode == 'legacy':
            print(f"Combining video and image (legacy mode)")
            combiner.combine_single(
                args.video,
                args.image,
                args.output,
                args.crop_bottom,
                args.image_position
            )
        else:
            # legacy_default - use default paths
            video_path = SETTINGS.default_video
            image_path = SETTINGS.default_image
            print(f"Combining video and image (legacy mode with defaults)")
            combiner.combine_single(
                video_path,
                image_path,
                args.output,
                args.crop_bottom,
                args.image_position
            )

        print(f"Video processing completed successfully!")
        print(f"Output saved to: {args.output}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
