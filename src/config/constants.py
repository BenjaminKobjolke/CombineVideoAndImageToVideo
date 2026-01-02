"""String constants for the application."""

from dataclasses import dataclass


@dataclass(frozen=True)
class FileExtensions:
    """Supported file extensions for media types."""

    IMAGE: frozenset[str] = frozenset({'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'})
    VIDEO: frozenset[str] = frozenset({'.mp4', '.avi', '.mov', '.mkv', '.webm', '.wmv'})


@dataclass(frozen=True)
class Defaults:
    """Default paths and values."""

    VIDEO_PATH: str = 'input/video.mp4'
    IMAGE_PATH: str = 'input/image.png'
    OUTPUT_PATH: str = 'output/output.mp4'
    CONSTRAINT: str = 'width'
    IMAGE_POSITION: str = 'bottom'
    CROP_BOTTOM: int = 0


@dataclass(frozen=True)
class VideoCodec:
    """Video codec constants."""

    MP4V: str = 'mp4v'


FILE_EXTENSIONS = FileExtensions()
DEFAULTS = Defaults()
VIDEO_CODEC = VideoCodec()
