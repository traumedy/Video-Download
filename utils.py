#!/usr/bin/env python3

"""utils.py - Utility functions
"""

__author__ = "Josh Buchbinder"
__copyright__ = "Copyright 2024, Josh Buchbinder"

import shutil
from PySide6.QtCore import QFileInfo, QDir


def value_to_bool(value):
    """Helper function to convert QSettings.value() to bool

    Returns:
        bool: Evaluated bool value
    """
    return value.lower() == 'true'\
        if isinstance(value, str)\
        else bool(value)


def normalize_path(path):
    """Returns paths with the correct slash for the operating system

    Args:
        path (str): Path to correct

    Returns:
        str: Corrected path
    """
    path = path.replace("/", QDir.separator())
    path = path.replace("\\", QDir.separator())
    return path


def get_ffmpeg_bin_path():
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
