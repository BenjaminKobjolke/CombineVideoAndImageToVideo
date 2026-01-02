"""Environment-driven settings."""

import os
from dataclasses import dataclass

from .constants import DEFAULTS


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""

    default_video: str = os.getenv('DEFAULT_VIDEO', DEFAULTS.VIDEO_PATH)
    default_image: str = os.getenv('DEFAULT_IMAGE', DEFAULTS.IMAGE_PATH)
    default_output: str = os.getenv('DEFAULT_OUTPUT', DEFAULTS.OUTPUT_PATH)
    default_constraint: str = os.getenv('DEFAULT_CONSTRAINT', DEFAULTS.CONSTRAINT)
    default_image_position: str = os.getenv('DEFAULT_IMAGE_POSITION', DEFAULTS.IMAGE_POSITION)
    default_crop_bottom: int = int(os.getenv('DEFAULT_CROP_BOTTOM', str(DEFAULTS.CROP_BOTTOM)))


SETTINGS = Settings()
