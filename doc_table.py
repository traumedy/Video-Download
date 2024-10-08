#!/usr/bin/env python3

"""doc_table.py - DocTable class encapsulating QTextDocument and QTextTable
"""

__author__ = "Josh Buchbinder"
__copyright__ = "Copyright 2024, Josh Buchbinder"

from PySide6.QtGui import QFont, QBrush, QColor
from PySide6.QtGui import QTextCursor, QTextDocument, QTextTableFormat
from constants import LinkIds


class DocTable(QTextDocument):
    """Subclass of QTextDocument that encapsulates the document and a table
    """
    def __init__(self, title: str, headers: list[str]) -> None:
        """Initializer for DocTable

        Args:
            title (str): Table title
            headers (list[str]): Headers for table
        """
        super().__init__()
        self.table_format = QTextTableFormat()
        self.table_format.setCellPadding(len(headers))
        self.table_format.setCellSpacing(0)
        cursor = QTextCursor(self)
        self.table = cursor.insertTable(1, len(headers), self.table_format)
        self.add_headers([title])
        self.table.appendRows(1)
        self.add_headers(headers)

    def add_headers(self, headers: list[str]) -> None:
        """Adds a row of headers

        Args:
            headers (list[str]): List of headers text
        """
        row = self.table.rows() - 1
        for idx, header in enumerate(headers):
            cell = self.table.cellAt(row, idx)
            cursor = cell.firstCursorPosition()
            fmt = cell.format()
            fmt.setFontWeight(QFont.Weight.Bold)
            fmt.setForeground(QBrush(QColor.fromRgb(200, 100, 50)))
            cell.setFormat(fmt)
            # fmt_orig = cursor.charFormat()
            cursor.insertText(header)

    def add_row(self, fields:
                list[tuple[str | list[str], str | None]]) -> None:
        """Adds a row to a QTextTable
        Args:

            fields (list[tuple[tuple[str | list[str], str | None]]): List of
                tuples of fields and links to add (text, link). If link is
                None it is not a link. if text is a list the text is formed
                from the list making links for each.
        """
        # TODO - Simplify this somehow
        row = self.table.rows()
        self.table.appendRows(1)
        for idx, field in enumerate(fields):
            cell = self.table.cellAt(row, idx)
            cursor = cell.firstCursorPosition()
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

    def to_html(self) -> str:
        """Returns the QTextDocument as HTML

        Returns:
            str: Document in HTML form
        """
        return self.toHtml()
