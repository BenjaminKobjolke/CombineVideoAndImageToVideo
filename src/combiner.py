import cv2
import numpy as np
import os
from typing import List, Optional

from .asset import Asset, ImageAsset, VideoAsset
from .config import VIDEO_CODEC
from .utils import discover_assets


class VideoCombiner:
    """Combines multiple assets into a single video by stacking them spatially."""

    def __init__(self, constraint: str = 'width'):
        """Initialize the combiner.

        Args:
            constraint: 'width' to scale all to same width,
                       'height' to scale images to match video height
        """
        if constraint not in ('width', 'height'):
            raise ValueError(f"Invalid constraint: {constraint}. Must be 'width' or 'height'")
        self.constraint = constraint

    def combine_from_folder(self, folder_path: str, output_path: str) -> None:
        """Combine all assets from a folder into a single video.

        Args:
            folder_path: Path to folder containing media files
            output_path: Path for output video file
        """
        asset_info = discover_assets(folder_path)
        if not asset_info:
            raise ValueError(f"No media files found in: {folder_path}")

        # Load all assets
        assets: List[Asset] = []
        for path, file_type in asset_info:
            if file_type == 'image':
                assets.append(ImageAsset(path))
            else:
                assets.append(VideoAsset(path))

        try:
            self._combine_assets(assets, output_path)
        finally:
            for asset in assets:
                asset.release()

    def combine_single(self, video_path: str, image_path: str, output_path: str,
                       crop_bottom: int = 0, image_position: str = 'bottom') -> None:
        """Combine a single video with a single image (legacy mode).

        Args:
            video_path: Path to input video
            image_path: Path to input image
            output_path: Path for output video
            crop_bottom: Pixels to crop from bottom of video
            image_position: 'top' or 'bottom' for image placement
        """
        video = VideoAsset(video_path)
        image = ImageAsset(image_path)

        try:
            self._combine_video_and_image(video, image, output_path, crop_bottom, image_position)
        finally:
            video.release()
            image.release()

    def _combine_video_and_image(self, video: VideoAsset, image: ImageAsset,
                                  output_path: str, crop_bottom: int,
                                  image_position: str) -> None:
        """Internal method to combine a video with an image."""
        video_width = video.width
        video_height = video.height - crop_bottom

        # Scale image to match video width
        aspect_ratio = image.width / image.height
        image_height = int(video_width / aspect_ratio)
        scaled_image = cv2.resize(image.image, (video_width, image_height))

        # Create video writer
        combined_height = video_height + image_height
        fourcc = cv2.VideoWriter_fourcc(*VIDEO_CODEC.MP4V)
        out = cv2.VideoWriter(output_path, fourcc, video.fps, (video_width, combined_height))

        # Process each frame
        for frame in video.frames():
            if crop_bottom > 0:
                frame = frame[0:video_height, :]

            if image_position == 'top':
                combined = np.vstack((scaled_image, frame))
            else:
                combined = np.vstack((frame, scaled_image))
            out.write(combined)

        out.release()

    def _combine_assets(self, assets: List[Asset], output_path: str) -> None:
        """Combine multiple assets into a single video by stacking spatially."""
        # Find the first video to get FPS and reference dimensions
        video_asset: Optional[VideoAsset] = None
        for asset in assets:
            if isinstance(asset, VideoAsset):
                video_asset = asset
                break

        if video_asset is None:
            raise ValueError("At least one video asset is required")

        fps = video_asset.fps
        frame_count = video_asset.frame_count
        ref_width = video_asset.width
        ref_height = video_asset.height

        # Calculate scaled dimensions for each asset
        scaled_assets = []
        total_height = 0

        for asset in assets:
            if self.constraint == 'width':
                # Scale all to same width
                if isinstance(asset, ImageAsset):
                    aspect_ratio = asset.width / asset.height
                    new_height = int(ref_width / aspect_ratio)
                    scaled_assets.append({
                        'asset': asset,
                        'width': ref_width,
                        'height': new_height
                    })
                    total_height += new_height
                else:
                    # Video - use as is (it's the reference)
                    scaled_assets.append({
                        'asset': asset,
                        'width': ref_width,
                        'height': ref_height
                    })
                    total_height += ref_height
            else:
                # constraint == 'height': scale images to video height
                if isinstance(asset, ImageAsset):
                    aspect_ratio = asset.width / asset.height
                    new_width = int(ref_height * aspect_ratio)
                    # For height constraint, we still need same width for vstack
                    # So we use ref_width but scale based on height
                    new_height = ref_height
                    scaled_assets.append({
                        'asset': asset,
                        'width': ref_width,
                        'height': new_height
                    })
                    total_height += new_height
                else:
                    scaled_assets.append({
                        'asset': asset,
                        'width': ref_width,
                        'height': ref_height
                    })
                    total_height += ref_height

        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*VIDEO_CODEC.MP4V)
        out = cv2.VideoWriter(output_path, fourcc, fps, (ref_width, total_height))

        # Pre-scale all images
        scaled_images = {}
        for i, info in enumerate(scaled_assets):
            if isinstance(info['asset'], ImageAsset):
                scaled_images[i] = cv2.resize(
                    info['asset'].image,
                    (info['width'], info['height'])
                )

        # Reset all videos
        for asset in assets:
            asset.reset()

        # Process frame by frame
        for _ in range(frame_count):
            frames = []
            for i, info in enumerate(scaled_assets):
                asset = info['asset']
                if isinstance(asset, ImageAsset):
                    frames.append(scaled_images[i])
                else:
                    frame = asset.get_frame()
                    if frame is None:
                        # Video ended, use black frame
                        frame = np.zeros((info['height'], info['width'], 3), dtype=np.uint8)
                    elif frame.shape[1] != info['width'] or frame.shape[0] != info['height']:
                        frame = cv2.resize(frame, (info['width'], info['height']))
                    frames.append(frame)

            combined = np.vstack(frames)
            out.write(combined)

        out.release()
