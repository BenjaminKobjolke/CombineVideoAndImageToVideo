"""Tests for src/utils.py."""

import os
import tempfile
from typing import Generator

import pytest

from src.utils import discover_assets, get_file_type


class TestGetFileType:
    """Tests for get_file_type function."""

    @pytest.mark.parametrize(
        'filename,expected',
        [
            ('video.mp4', 'video'),
            ('video.avi', 'video'),
            ('video.mov', 'video'),
            ('video.mkv', 'video'),
            ('video.webm', 'video'),
            ('video.wmv', 'video'),
            ('VIDEO.MP4', 'video'),
            ('image.jpg', 'image'),
            ('image.jpeg', 'image'),
            ('image.png', 'image'),
            ('image.gif', 'image'),
            ('image.bmp', 'image'),
            ('image.webp', 'image'),
            ('IMAGE.PNG', 'image'),
            ('document.pdf', None),
            ('script.py', None),
            ('no_extension', None),
        ],
    )
    def test_file_type_detection(self, filename: str, expected: str | None) -> None:
        """Test file type detection for various extensions."""
        assert get_file_type(filename) == expected


class TestDiscoverAssets:
    """Tests for discover_assets function."""

    @pytest.fixture
    def temp_folder(self) -> Generator[str, None, None]:
        """Create a temporary folder for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_empty_folder(self, temp_folder: str) -> None:
        """Test discovering assets in an empty folder."""
        result = discover_assets(temp_folder)
        assert result == []

    def test_discover_mixed_assets(self, temp_folder: str) -> None:
        """Test discovering mixed image and video assets."""
        # Create test files
        open(os.path.join(temp_folder, 'video.mp4'), 'w').close()
        open(os.path.join(temp_folder, 'image.png'), 'w').close()
        open(os.path.join(temp_folder, 'document.txt'), 'w').close()

        result = discover_assets(temp_folder)

        assert len(result) == 2
        assert any(path.endswith('image.png') and ftype == 'image' for path, ftype in result)
        assert any(path.endswith('video.mp4') and ftype == 'video' for path, ftype in result)

    def test_sorted_by_filename(self, temp_folder: str) -> None:
        """Test that assets are sorted by filename."""
        open(os.path.join(temp_folder, 'z_video.mp4'), 'w').close()
        open(os.path.join(temp_folder, 'a_image.png'), 'w').close()
        open(os.path.join(temp_folder, 'm_video.avi'), 'w').close()

        result = discover_assets(temp_folder)

        filenames = [os.path.basename(path) for path, _ in result]
        assert filenames == ['a_image.png', 'm_video.avi', 'z_video.mp4']

    def test_invalid_directory(self) -> None:
        """Test error handling for invalid directory."""
        with pytest.raises(ValueError, match='Not a valid directory'):
            discover_assets('/nonexistent/path')
