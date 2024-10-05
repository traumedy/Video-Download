#!/usr/bin/env python3

"""status_widow.py - Subclass of QTextEdit with additional features
"""

__author__ = "Josh Buchbinder"
__copyright__ = "Copyright 2024, Josh Buchbinder"

import re
from typing import cast
from collections.abc import Callable
from overrides import override
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QFont, QTextCursor, QMouseEvent, QHelpEvent
from PySide6.QtWidgets import QTextEdit, QToolTip
from constants import AppConst, LinkIds, StringMaps


class StatusWindow(QTextEdit):
    """Subclass of QTextEdit allowing clickable links
    """
    def __init__(self, link_click_callback: Callable[[str], None]) -> None:
        """Initializer for StatusWindow

        Args:
            link_click_callback (Callable[[str], None]): Callback functions for
                clicked links
        """
        super().__init__()
        self.anchor = None
        self.link_click_callback = link_click_callback
        # Set font to monospace black
        self.text_font = QFont(AppConst.MONOSPACE_FONT_NAME)
        self.text_font.setStyleHint(QFont.StyleHint.TypeWriter)
        self.text_font.setWeight(QFont.Weight.Black)
        self.setFont(self.text_font)
        # Set status text box to read only for status logs
        self.setReadOnly(True)
        # Set status window to not wrap text
        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        # Set to accept rich text
        self.setAcceptRichText(True)
        self.autoscroll = True

    @override
    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        """Override of mouseMoveEvent

        Args:
            e (QMouseEvent): Mouse event
        """
        anchor = self.anchorAt(e.pos())
        if anchor:
            self.viewport().setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.viewport().setCursor(Qt.CursorShape.IBeamCursor)
        super().mouseMoveEvent(e)

    @override
    def mousePressEvent(self, e: QMouseEvent) -> None:
        """Override of mousePressEvent

        Args:
            e (QMouseEvent): The mouse event
        """
        self.anchor = self.anchorAt(e.pos())
        super().mousePressEvent(e)

    @override
    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
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

    @override
    def event(self, e: QEvent) -> bool:
        """Override of event handler in parent class

        Args:
            e (QEvent): Event to handle

        Returns:
            bool: True if handled
        """
        if e.type() == QEvent.Type.ToolTip:
            help_event = cast(QHelpEvent, e)
            anchor = self.anchorAt(help_event.pos())
            if anchor:
                QToolTip.showText(help_event.globalPos(),
                                  self.tooltip_from_anchor(anchor))
                return True

        return super().event(e)

    def tooltip_from_anchor(self, anchor: str) -> str:
        """Returns tooltip text for an anchor text

        Args:
            anchor (str): Anchor text

        Returns:
            str: Tooltip text
        """
        sep_pos = anchor.find(LinkIds.LINKID_SEP)
        if sep_pos != -1:
            link_id = anchor[0:sep_pos]
            if link_id in StringMaps.STRINGMAP_LINKID_TOOLTIP:
                return StringMaps.STRINGMAP_LINKID_TOOLTIP[link_id]
        return ""

    def scroll_to_end(self) -> None:
        """Scrolls window to bottom of text
        """
        self.verticalScrollBar().setValue(
            self.verticalScrollBar().maximum())

    def strip_color_codes(self, message: str) -> str:
        """Removes console color escape codes from string

        Args:
            message (str): Message with possible color codes

        Returns:
            str: message with color escape codes removed
        """
        regex = re.compile(AppConst.REGEX_COLORSTRIP)
        return regex.sub("", message)

    def append_text(self, text: str) -> None:
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

    def append_console_text(self, text: str) -> None:
        """Add console text with color escape sequences converted
        to change the text color

        Args:
            text (str): Text to add
        """
        # TODO
        self.append_text(text)

    def append_html(self, text: str) -> None:
        """Simple text append, allows html

        Args:
            text (str): Text to append
        """
        self.append(text)
        if self.autoscroll:
            self.scroll_to_end()

    def set_autoscroll(self, flag: bool) -> None:
        """Sets auto-scroll to bottom of text and scrolls if flag is set

        Args:
            set (bool): New flag value
        """
        self.autoscroll = flag
        if flag:
            self.scroll_to_end()
