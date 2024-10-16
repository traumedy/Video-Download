#!/usr/bin/env python3

"""video_download.py - Download videos or lists of videos
including bookmarks exported from browsers from video sites
like YouTube, Vimeo, Instagram, etc using the yt_dlp Python package.

Author: Josh Buchbinder
"""

__author__ = "Josh Buchbinder"
__copyright__ = "Copyright 2024, Josh Buchbinder"
__version__ = "0.6.0"

import sys
from PySide6.QtWidgets import QApplication

from main_window import MainWindow


def main(argv: list[str]) -> int:
    """ Main function entry point

    Args:
        argv (list[str]): Command line arguments

    Returns:
        int: exit() value
    """

    # Create application
    app = QApplication(argv)
    # Use Fusion app style
    app.setStyle('Fusion')

    # Create window
    window = MainWindow()
    window.show()

    # Start event loop
    return app.exec()


# Entry point
if __name__ == "__main__":
    sys.exit(main(sys.argv))
