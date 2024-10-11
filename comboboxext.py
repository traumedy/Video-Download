#!/usr/bin/env python3

"""comboboxext.py - Subclass of QComboBox with additional features
"""

__author__ = "Josh Buchbinder"
__copyright__ = "Copyright 2024, Josh Buchbinder"

from typing import Any
from overrides import override
from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QComboBox, QLineEdit


class ComboBoxExt(QComboBox):
    """Subclass of QComboBox with extended functionality
    """
    checkboxes: bool
    changed: bool
    line_edit: QLineEdit
    mdl: QStandardItemModel

    def __init__(self, checkboxes: bool = False) -> None:
        """Initializer for ComboBoxExt

        Args:
            checkboxes (bool, optional): True if clickable combobox.
                Defaults to False.
        """
        super().__init__()
        self.checkboxes = checkboxes
        self.changed = False
        if checkboxes:
            self.view().pressed.connect(self.item_pressed)
            self.mdl = QStandardItemModel(self)
            self.setModel(self.mdl)
            self.line_edit = QLineEdit()
            self.line_edit.setReadOnly(True)
            self.setLineEdit(self.line_edit)
            self.update_edit_text()
            self.currentTextChanged.connect(
                lambda _: self.update_edit_text())

    def has_checkboxes(self) -> bool:
        """Returns True if combobox has checkboxes

        Returns:
            bool: True if combobox has checkboxes
        """
        return self.checkboxes

    def add_check_item(self, text: str, user_data: Any = None) -> None:
        """Like QCombmBox.addItem() but sets initial checkbox state

        Args:
            label (str): Text for combobox item
            user_dat (Any, optional): data associated with combobox item.
                Defaults to None.
        """
        super().addItem(text, user_data)
        item = self.mdl.item(self.count() - 1, 0)
        # Uncheck item to make checkbox appear
        item.setCheckState(Qt.CheckState.Unchecked)

    @override
    def hidePopup(self) -> None:
        """Override of hidePopup() to allow combobox staying expanded
           when items are chcecked/unchecked
        """
        if not self.changed:
            super().hidePopup()
        self.changed = False

    def set_current_text(self, text: str) -> bool:
        """Like setCurrentText but returns True if item is found

        Args:
            text (str): Text to find

        Returns:
            bool: True if item is found
        """
        index = self.findText(text)
        if index != -1:
            self.setCurrentIndex(index)
            return True
        return False

    def item_pressed(self, index: QModelIndex) -> None:
        """Callback function for whan an item is pressed

        Args:
            index (QModelIndex): Index of pressed item
        """
        item = self.mdl.itemFromIndex(index)
        state = Qt.CheckState.Checked
        if item.checkState() == Qt.CheckState.Checked:
            state = Qt.CheckState.Unchecked
        item.setCheckState(state)
        self.changed = True
        self.update_edit_text()

    def set_current_data(self, data: Any) -> bool:
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

    def set_current_data_lte(self, val: int) -> bool:
        """Sets the current index to the item who's data is nearest to val
           without going over (less than or equal to)

        Args:
            val (int): Value to compare to

        Returns:
            bool: True if item is found
        """
        datalist = [(index, self.itemData(index))
                    for index in range(self.count())]
        closest = (-1, 0)
        for index, data in datalist:
            if val <= data and (closest[0] == -1 or data < closest[1]):
                closest = (index, data)

        if closest[0] != -1:
            self.setCurrentIndex(closest[0])
            return True
        return False

    def items_text(self) -> list[str]:
        """Returns the text of the items of the combobox as a list

        Returns:
            list[str]: List of all items' text
        """
        return [self.itemText(i) for i in range(self.count())]

    def items_data(self) -> list[Any]:
        """Returns the data of the items of the combobox as a list

        Returns:
            list[Any]: List of all items' data
        """
        return [self.itemData(i) for i in range(self.count())]

    def checked_items_text(self) -> list[str]:
        """Returns a list of the text of checked items

        Returns:
            list[str]: List of checked items' text
        """
        return [self.itemText(i) for i in range(self.count())
                if self.mdl.item(i, 0).checkState() == Qt.CheckState.Checked]

    def checked_items_data(self) -> list[Any]:
        """Returns a list of the data of checked items

        Returns:
            list[Any]: List of checked items' data
        """
        return [self.itemData(i) for i in range(self.count())
                if self.mdl.item(i, 0).checkState() == Qt.CheckState.Checked]

    def check_item_by_index(self, index: int, checked: bool) -> bool:
        """Checks an item identified by its index

        Args:
            index (int): Index of item to check
            checked (bool): True if item is to be checked

        Returns:
            bool: True if item is found
        """
        item = self.mdl.item(index, 0)
        if item:
            state = Qt.CheckState.Unchecked
            if checked:
                state = Qt.CheckState.Checked
            item.setCheckState(state)
            self.update_edit_text()
            return True
        return False

    def check_item_by_text(self, text: str, checked: bool) -> bool:
        """Checks an item identified by its text

        Args:
            text (str): Text of item to check
            checked (bool): True if item is to be checked

        Returns:
            bool: True if item is found
        """
        item_index = self.findText(text)
        if item_index != -1:
            self.check_item_by_index(item_index, checked)
            self.update_edit_text()
            return True
        return False

    def check_item_by_data(self, data: Any, checked: bool) -> bool:
        """Checks an item identified by its data

        Args:
            data (Any): Data of item to check
            checked (bool): True if item is to be checked

        Returns:
            bool: True if item is found
        """
        item_index = self.findData(data)
        if item_index != -1:
            self.check_item_by_index(item_index, checked)
            self.update_edit_text()
            return True
        return False

    def check_items_by_text(self, text_list: list[str], checked: bool) -> None:
        """Checks multiple items identified by their text

        Args:
            text_list (list[str]): List of strings identifying items to check
            checked (bool): True if items are to be checked
        """
        for text in text_list:
            self.check_item_by_text(text, checked)

    def check_items_by_data(self, data_list: list[Any], checked: bool) -> None:
        """Checks multiple items identified by their data

        Args:
            data_list (list[Any]): List of data values identifying
                items to check
            checked (bool): True if items are to be checked
        """
        for data in data_list:
            self.check_item_by_data(data, checked)

    def check_all(self, checked: bool) -> None:
        """Checks or unchecks all items in list

        Args:
            checked (bool): True if items are to be checked
        """
        for i in range(0, self.count()):
            self.check_item_by_index(i, checked)

    def is_item_checked(self, index: int) -> bool:
        """Returns True if an item at an index exists and is checked

        Args:
            index (int): Index of item

        Returns:
            bool: True if item is checked
        """
        item = self.mdl.item(index, 0)
        return item is not None and item.checkState() == Qt.CheckState.Checked

    def checked_count(self) -> int:
        """Returns the number of checked items

        Returns:
            int: The count of checked items
        """
        return sum(self.is_item_checked(i) for i in range(self.count()))

    def update_edit_text(self) -> None:
        """Updates the edit text to display the selected count
        """
        count = self.checked_count()
        text = f"{count} item{"" if count == 1 else "s"} selected"
        self.line_edit.setText(text)
