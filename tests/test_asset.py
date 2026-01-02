"""Tests for src/asset.py."""

import os
import tempfile

import cv2
import numpy as np
import pytest

from src.asset import ImageAsset, VideoAsset


class TestImageAsset:
    """Tests for ImageAsset class."""

    @pytest.fixture
    def temp_image(self) -> str:
        """Create a temporary test image."""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            # Create a simple test image
            img = np.zeros((100, 200, 3), dtype=np.uint8)
            img[:, :] = [255, 0, 0]  # Blue image (BGR)
            cv2.imwrite(f.name, img)
            yield f.name
        os.unlink(f.name)

    def test_load_image(self, temp_image: str) -> None:
        """Test loading an image asset."""
        asset = ImageAsset(temp_image)
        assert asset.width == 200
        assert asset.height == 100
        asset.release()

    def test_get_frame(self, temp_image: str) -> None:
        """Test getting a frame from image asset."""
        asset = ImageAsset(temp_image)
        frame = asset.get_frame()
        assert frame is not None
        assert frame.shape == (100, 200, 3)
        asset.release()

    def test_get_scaled(self, temp_image: str) -> None:
        """Test getting a scaled version of the image."""
        asset = ImageAsset(temp_image)
        scaled = asset.get_scaled(target_width=400)
        assert scaled is not None
        assert scaled.shape[1] == 400
        assert scaled.shape[0] == 200  # Aspect ratio preserved
        asset.release()

    def test_invalid_image_path(self) -> None:
        """Test error handling for invalid image path."""
        with pytest.raises(ValueError, match='Error loading image'):
            ImageAsset('/nonexistent/image.png')


class TestVideoAsset:
    """Tests for VideoAsset class."""

    @pytest.fixture
    def temp_video(self) -> str:
        """Create a temporary test video."""
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
            # Create a simple test video
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(f.name, fourcc, 30.0, (320, 240))
            for _ in range(30):  # 1 second of video
                frame = np.zeros((240, 320, 3), dtype=np.uint8)
                frame[:, :] = [0, 255, 0]  # Green frame (BGR)
                out.write(frame)
            out.release()
            yield f.name
        os.unlink(f.name)

    def test_load_video(self, temp_video: str) -> None:
        """Test loading a video asset."""
        asset = VideoAsset(temp_video)
        assert asset.width == 320
        assert asset.height == 240
        assert asset.fps == 30.0
        assert asset.frame_count == 30
        asset.release()

    def test_get_frame(self, temp_video: str) -> None:
        """Test getting a frame from video asset."""
        asset = VideoAsset(temp_video)
        frame = asset.get_frame()
        assert frame is not None
        assert frame.shape == (240, 320, 3)
        asset.release()

    def test_frames_iterator(self, temp_video: str) -> None:
        """Test iterating through video frames."""
        asset = VideoAsset(temp_video)
        frames = list(asset.frames())
        assert len(frames) == 30
        asset.release()

    def test_reset(self, temp_video: str) -> None:
        """Test resetting video to beginning."""
        asset = VideoAsset(temp_video)
        asset.get_frame()
        asset.get_frame()
        asset.reset()
        frame = asset.get_frame()
        assert frame is not None
        asset.release()

    def test_invalid_video_path(self) -> None:
        """Test error handling for invalid video path."""
        with pytest.raises(ValueError, match='Error opening video'):
            VideoAsset('/nonexistent/video.mp4')
