#!/usr/bin/env python3

"""utils.py - Utilities for manipulating QTextTable
"""

__author__ = "Josh Buchbinder"
__copyright__ = "Copyright 2024, Josh Buchbinder"

from PySide6.QtGui import QTextTableCell, QTextCursor
from PySide6.QtGui import QFont, QBrush, QColor
from PySide6.QtGui import QTextDocument, QTextTable, QTextTableFormat


def table_add_row(table, fields, header=False):
    """Adds a row to a QTextTable

    Args:
        table (QTextTable): Table to be modified
        fields ([str]): List of fiends to add
        header (bool): True if this is the header (Default: False)
    """
    cursor = QTextCursor()
    if not header:
        table.appendRows(1)
    row = table.rows() - 1
    for idx, field in enumerate(fields):
        cell = table.cellAt(row, idx)
        cursor = cell.firstCursorPosition()
        if header:
            fmt = cell.format()
            fmt.setFontWeight(QFont.Weight.Bold)
            fmt.setForeground(QBrush(QColor.fromRgb(200, 100, 50)))
            cell.setFormat(fmt)
        if field:
            cursor.insertText(str(field))


def table_create(name, headers):
    """Creates a QTextDocument and a QTextTable with headers

    Args:
        name (str): Name of table for display
        headers ([str]): Headers for table, also definess number of columns

    Returns:
        (QTextDocument, QTextTable): Document and table
    """
    text_doc = QTextDocument()
    table_format = QTextTableFormat()
    table_format.setCellPadding(len(headers))
    table_format.setCellSpacing(0)
    cursor = QTextCursor(text_doc)
    table = cursor.insertTable(1, len(headers), table_format)
    table_add_row(table, [name], True)
    table.appendRows(1)
    table_add_row(table, headers, True)
    return text_doc, table


def value_to_bool(value):
    """Helper function to convert QSettings.value() to bool
    """
    return value.lower() == 'true'\
        if isinstance(value, str)\
        else bool(value)
