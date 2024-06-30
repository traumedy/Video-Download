#!/usr/bin/env python3

"""status_widow.py - Subclass of QTextEdit with additional features
"""

__author__ = "Josh Buchbinder"
__copyright__ = "Copyright 2024, Josh Buchbinder"

from overrides import override
import re
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QTextCursor
from PySide6.QtWidgets import QTextEdit
from constants import AppConst


class StatusWindow(QTextEdit):
    """Subclass of QTextEdit allowing clickable links
    """
    def __init__(self, link_click_callback):
        super().__init__()
        self.anchor = None
        self.link_click_callback = link_click_callback
        # Set font to monospace black
        self.font = QFont(AppConst.MONOSPACE_FONT_NAME)
        self.font.setStyleHint(QFont.StyleHint.TypeWriter)
        self.font.setWeight(QFont.Weight.Black)
        self.setFont(self.font)
        # Set status text box to read only for status logs
        self.setReadOnly(True)
        # Set status window to not wrap text
        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        # Set to accept rich text
        self.setAcceptRichText(True)
        self.autoscroll = True

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
                self.link_click_callback(self.anchor)
                self.anchor = None
        super().mouseReleaseEvent(e)

    def scroll_to_end(self):
        """Scrolls window to bottom of text
        """
        self.verticalScrollBar().setValue(
            self.verticalScrollBar().maximum())

    def strip_color_codes(self, message):
        """Removes console color escape codes from string

        Args:
            message (str): Message with possible color codes

        Returns:
            str: message with color escape codes removed
        """
        regex = re.compile(AppConst.REGEX_COLORSTRIP)
        return regex.sub("", message)

    def append_text(self, text):
        """Appends to TextEdit without affecting the char format
        and scrolls to the end.

        Args:
            text (str): Text to append
        """
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(self.strip_color_codes(text) + "\n")
        if self.autoscroll:
            self.scroll_to_end()

    def append_html(self, text):
        """Simple text append, allows html

        Args:
            text (str): Text to append
        """
        self.append(text)
        if self.autoscroll:
            self.scroll_to_end()

    def set_autoscroll(self, flag):
        """Sets auto-scroll to bottom of text flag and scrolls if set

        Args:
            set (bool): New flag value
        """
        self.autoscroll = flag
        if flag:
            self.scroll_to_end()
