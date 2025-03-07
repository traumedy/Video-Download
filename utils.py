#!/usr/bin/env python3

"""utils.py - Utility functions
"""

__author__ = "Josh Buchbinder"
__copyright__ = "Copyright 2024, Josh Buchbinder"

import shutil
from typing import Any
from PySide6.QtCore import QFileInfo, QDir, QStandardPaths


def value_to_bool(value: Any) -> bool:
    """Helper function to convert QSettings.value() to bool

    Args:
        value (Any): Converts Any to bool

    Returns:
        bool: Evaluated bool value
    """
    return value.lower() == 'true'\
        if isinstance(value, str)\
        else bool(value)


def normalize_path(path: str) -> str:
    """Returns paths with the correct slash for the operating system

    Args:
        path (str): Path to correct

    Returns:
        str: Corrected path
    """
    path = path.replace("/", QDir.separator())
    path = path.replace("\\", QDir.separator())
    return path


def get_ffmpeg_bin_path() -> str:
    """Returns the path to ffmpeg binaries

    Returns:
        str: Path to ffmpeg binaries
    """
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        # If ffmpeg found
        ffmpeg_info = QFileInfo(ffmpeg_path)
        ffmpeg_path = ffmpeg_info.dir().path()
    else:
        # ffmpeg executable not found in path
        ffmpeg_path = ""
    ffmpeg_path = normalize_path(ffmpeg_path)
    return ffmpeg_path


def get_videos_path() -> str:
    """Returns the path to a place to store video files

    Returns:
        str: Path to directory where videos might be stored
    """
    videos_paths = QStandardPaths.standardLocations(
        QStandardPaths.StandardLocation.MoviesLocation)
    if not videos_paths:
        return ""
    video_path = normalize_path(videos_paths[0])
    return video_path
