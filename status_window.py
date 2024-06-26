#!/usr/bin/env python3

"""status_widow.py - Subclass of QTextEdit with additional features
"""

__author__ = "Josh Buchbinder"
__copyright__ = "Copyright 2024, Josh Buchbinder"

from overrides import override
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTextEdit


class StatusWindow(QTextEdit):
    """Subclass of QTextEdit allowing clickable links
    """
    def __init__(self, callback):
        super().__init__()
        self.anchor = None
        self.callback = callback

    @override
    def mouseMoveEvent(self, e):
        """Override of mouseMoveEvent

        Args:
            e (QMouseEvent): _description_
        """
        anchor = self.anchorAt(e.pos())
        if anchor:
            self.viewport().setCursor(Qt.PointingHandCursor)
        else:
            self.viewport().setCursor(Qt.IBeamCursor)
        super().mouseMoveEvent(e)

    @override
    def mousePressEvent(self, e):
        """Override of mousePressEvent

        Args:
            e (QMouseEvent): The mouse event
        """
        self.anchor = self.anchorAt(e.pos())
        super().mousePressEvent(e)

    @override
    def mouseReleaseEvent(self, e):
        """Override of mouseReleaseEvent

        Args:
            e (QMouseEvent): The mouse event
        """
        if self.anchor:
            anchor = self.anchorAt(e.pos())
            if anchor == self.anchor:
                self.callback(self.anchor)
                self.anchor = None
        super().mouseReleaseEvent(e)

    def append_safe(self, text):
        """Appends to TextEdit without affecting the char format
        and scrolls to the end.

        Args:
            text (str): Text to append
        """
        fmt = self.currentCharFormat()
        self.append(text)
        self.setCurrentCharFormat(fmt)
        self.verticalScrollBar().setValue(
            self.verticalScrollBar().maximum())
