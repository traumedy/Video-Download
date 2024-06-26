#!/usr/bin/env python3

"""doc_table.py - Class containing QTextDocument and QTextTable
"""

__author__ = "Josh Buchbinder"
__copyright__ = "Copyright 2024, Josh Buchbinder"

from PySide6.QtGui import QFont, QBrush, QColor
from PySide6.QtGui import QTextCursor, QTextDocument, QTextTableFormat


class DocTable(QTextDocument):
    """Helper class encapsulation QTextDocument and QTextTable
    """
    def __init__(self, title, headers):
        super().__init__()
        self.table_format = QTextTableFormat()
        self.table_format.setCellPadding(len(headers))
        self.table_format.setCellSpacing(0)
        cursor = QTextCursor(self)
        self.table = cursor.insertTable(1, len(headers), self.table_format)
        self.add_row([(title, None)], True)
        self.table.appendRows(1)
        tuple_list = [(header, None) for header in headers]
        self.add_row(tuple_list, True)

    def add_row(self, fields, header=False):
        """Adds a row to a QTextTable

        Args:
            fields ([(str, str)]): List of fiends to add (text, link)
            header (bool): True if this is the header (Default: False)
        """
        cursor = QTextCursor()
        if not header:
            self.table.appendRows(1)
        row = self.table.rows() - 1
        for idx, field in enumerate(fields):
            cell = self.table.cellAt(row, idx)
            cursor = cell.firstCursorPosition()
            if header:
                fmt = cell.format()
                fmt.setFontWeight(QFont.Weight.Bold)
                fmt.setForeground(QBrush(QColor.fromRgb(200, 100, 50)))
                cell.setFormat(fmt)
            if field[0]:
                if field[1]:
                    # Link
                    txt_fmt = cursor.charFormat()
                    txt_fmt.setAnchor(True)
                    txt_fmt.setAnchorHref(field[1])
                    # txt_fmt.setAnchorNames([str(field[0])])
                    # txt_fmt.setToolTip("TEST")
                    cursor.insertText(str(field[0]), txt_fmt)
                else:
                    # Plain text
                    cursor.insertText(str(field[0]))

    def to_html(self):
        """Returns the QTextDocument as HTML

        Returns:
            str: Document in HTML form
        """
        return self.toHtml()
