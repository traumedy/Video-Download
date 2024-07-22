#!/usr/bin/env python3

"""doc_table.py - DocTable class encapsulating QTextDocument and QTextTable
"""

__author__ = "Josh Buchbinder"
__copyright__ = "Copyright 2024, Josh Buchbinder"

from PySide6.QtGui import QFont, QBrush, QColor
from PySide6.QtGui import QTextCursor, QTextDocument, QTextTableFormat
from constants import LinkIds


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
            fields ([(str|[str], str)]): List of string tuples of fields and
                links to add (text, link) or list of tuples with multiple
                strings using the same link prefix ([texts], link_prefix)
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
                fmt_orig = cursor.charFormat()
                if field[1]:
                    # Link
                    fmt = fmt_orig
                    fmt.setAnchor(True)
                    if isinstance(field[0], list):
                        # A list of link strings
                        for s in field[0]:
                            link = field[1] + LinkIds.LINKID_SEP + s
                            fmt.setAnchorHref(link)
                            fmt.setToolTip("ToolTipTest")
                            cursor.insertText(s, fmt)
                            cursor.insertText(" ", fmt_orig)
                    else:
                        fmt.setAnchorHref(field[1])
                        cursor.insertText(str(field[0]), fmt)
                    # Restore original format
                    cursor.setCharFormat(fmt_orig)
                else:
                    # Plain text
                    cursor.insertText(str(field[0]))

    def to_html(self):
        """Returns the QTextDocument as HTML

        Returns:
            str: Document in HTML form
        """
        return self.toHtml()
