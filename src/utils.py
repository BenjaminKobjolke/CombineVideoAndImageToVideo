import os
from typing import List, Optional, Tuple

from .config import FILE_EXTENSIONS


def get_file_type(path: str) -> Optional[str]:
    """Determine if a file is an image or video based on extension.

    Returns:
        'image', 'video', or None if unknown type
    """
    ext = os.path.splitext(path)[1].lower()
    if ext in FILE_EXTENSIONS.IMAGE:
        return 'image'
    elif ext in FILE_EXTENSIONS.VIDEO:
        return 'video'
    return None


def discover_assets(folder_path: str) -> List[Tuple[str, str]]:
    """Discover and sort media files in a folder.

    Returns:
        List of tuples (file_path, file_type) sorted by filename.
        file_type is either 'image' or 'video'.
    """
    if not os.path.isdir(folder_path):
        raise ValueError(f"Not a valid directory: {folder_path}")

    assets = []
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if not os.path.isfile(filepath):
            continue

        file_type = get_file_type(filepath)
        if file_type is not None:
            assets.append((filepath, file_type))

    # Sort by filename
    assets.sort(key=lambda x: os.path.basename(x[0]).lower())

    return assets
