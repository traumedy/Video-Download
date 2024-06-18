#!/usr/bin/env python3

"""custom_widgets.py - Subclassed widgets
"""

__author__ = "Josh Buchbinder"
__copyright__ = "Copyright 2024, Josh Buchbinder"

from overrides import override
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTextEdit, QComboBox


class ClickableTextEdit(QTextEdit):
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


class ComboBoxExt(QComboBox):
    """Subclass of QComboBox with extended functionality
    """
    def setCurrentData(self, data):
        """Select item by data

        Args:
            data (Any): Data to earch for

        Returns:
            bool: True if data is found
        """
        index = self.findData(data)
        if index != -1:
            self.setCurrentIndex(index)
            return True
        return False

    def setCurrentNearestData(self, val):
        """Sets the current index to the item who's data
        is nearest to val without going over

        Args:
            val (int): Value to compare to

        Returns:
            bool: True if item is found
        """
        datalist = [(index, self.itemData(index))
                    for index in range(0, self.count())]
        closest = (-1, 0)
        for index, data in datalist:
            if val <= data and (closest[0] == -1 or data < closest[1]):
                closest = (index, data)

        if closest[0] != -1:
            self.setCurrentIndex(closest[0])
            return True
        return False

    def itemsText(self):
        """Returns the text of the items of the combobox as a list

        Returns:
            [str]: List of items' text
        """
        return [self.itemText(i) for i in range(0, self.count())]

    def itemsData(self):
        """Returns the data of the items of the combobox as a list

        Returns:
            [Any]: List of items' data
        """
        return [self.itemData(i) for i in range(0, self.count())]
