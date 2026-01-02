"""Tests for src/combiner.py."""

import os
import tempfile

import cv2
import numpy as np
import pytest

from src.combiner import VideoCombiner


class TestVideoCombiner:
    """Tests for VideoCombiner class."""

    @pytest.fixture
    def temp_video(self) -> str:
        """Create a temporary test video."""
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(f.name, fourcc, 30.0, (320, 240))
            for _ in range(30):
                frame = np.zeros((240, 320, 3), dtype=np.uint8)
                frame[:, :] = [0, 255, 0]
                out.write(frame)
            out.release()
            yield f.name
        os.unlink(f.name)

    @pytest.fixture
    def temp_image(self) -> str:
        """Create a temporary test image."""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            img = np.zeros((100, 320, 3), dtype=np.uint8)
            img[:, :] = [255, 0, 0]
            cv2.imwrite(f.name, img)
            yield f.name
        os.unlink(f.name)

    def test_init_valid_constraint(self) -> None:
        """Test initialization with valid constraints."""
        combiner_width = VideoCombiner(constraint='width')
        assert combiner_width.constraint == 'width'

        combiner_height = VideoCombiner(constraint='height')
        assert combiner_height.constraint == 'height'

    def test_init_invalid_constraint(self) -> None:
        """Test initialization with invalid constraint."""
        with pytest.raises(ValueError, match='Invalid constraint'):
            VideoCombiner(constraint='invalid')

    def test_combine_single(self, temp_video: str, temp_image: str) -> None:
        """Test combining a single video with an image."""
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
            output_path = f.name

        try:
            combiner = VideoCombiner()
            combiner.combine_single(temp_video, temp_image, output_path)

            # Verify output exists and is valid
            assert os.path.exists(output_path)
            cap = cv2.VideoCapture(output_path)
            assert cap.isOpened()
            # Combined height should be video height + image height
            assert cap.get(cv2.CAP_PROP_FRAME_HEIGHT) == 240 + 100
            cap.release()
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_combine_single_image_top(self, temp_video: str, temp_image: str) -> None:
        """Test combining with image on top."""
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
            output_path = f.name

        try:
            combiner = VideoCombiner()
            combiner.combine_single(temp_video, temp_image, output_path, image_position='top')

            assert os.path.exists(output_path)
            cap = cv2.VideoCapture(output_path)
            assert cap.isOpened()
            cap.release()
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_combine_from_folder(self, temp_video: str, temp_image: str) -> None:
        """Test combining assets from a folder."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Copy files to temp folder
            import shutil
            shutil.copy(temp_video, os.path.join(tmpdir, '01_video.mp4'))
            shutil.copy(temp_image, os.path.join(tmpdir, '02_image.png'))

            output_path = os.path.join(tmpdir, 'output.mp4')

            combiner = VideoCombiner()
            combiner.combine_from_folder(tmpdir, output_path)

            assert os.path.exists(output_path)
            cap = cv2.VideoCapture(output_path)
            assert cap.isOpened()
            cap.release()

    def test_combine_from_folder_empty(self) -> None:
        """Test error handling for empty folder."""
        with tempfile.TemporaryDirectory() as tmpdir:
            combiner = VideoCombiner()
            with pytest.raises(ValueError, match='No media files found'):
                combiner.combine_from_folder(tmpdir, 'output.mp4')
