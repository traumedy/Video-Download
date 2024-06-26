#!/usr/bin/env python3

"""comboboxext.py - Subclass of QComboBox with additional features
"""

__author__ = "Josh Buchbinder"
__copyright__ = "Copyright 2024, Josh Buchbinder"

from overrides import override
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QComboBox


class ComboBoxExt(QComboBox):
    """Subclass of QComboBox with extended functionality
    """
    def __init__(self, checkboxes=False):
        super().__init__()
        self.checkboxes = checkboxes
        self._changed = False
        if checkboxes:
            self.view().pressed.connect(self.item_pressed)
            self.setModel(QStandardItemModel(self))

    def flags(self, index):
        """Returns flags for widget

        Args:
            index (int): Index of ?

        Returns:
            int: Qt.ItemFlag
        """
        if self.checkboxes:
            return Qt.ItemIsUserCheckable | Qt.ItemIsSelectable \
                | Qt.ItemIsEnabled
        else:
            return super().flags(index)

    def has_checkboxes(self):
        """Returns True if combobox has checkboxes

        Returns:
            bool: True if combobox has checkboxes
        """
        return self.checkboxes

    @override
    def addItem(self, label, data=None):
        """Override of QCombmBox.addItem() that sets initial checkbox state

        Args:
            label (str): Text for combobox item
            data (Any, optional): data associated with combobox item.
                Defaults to None.

        Returns:
            QStandardItem - The newly added item
        """
        super().addItem(label, data)
        item = self.model().item(self.count() - 1, 0)
        if self.checkboxes:
            # Uncheck item to make checkbox appear
            item.setCheckState(Qt.Unchecked)
        return item

    @override
    def hidePopup(self):
        """Override of hidePopup() to allow combobox staying expanded
           when items are chcecked/unchecked
        """
        if not self._changed:
            super().hidePopup()
        self._changed = False

    def item_pressed(self, index):
        """Callback function for whan an item is pressed

        Args:
            index (int): Index of pressed item
        """
        item = self.model().itemFromIndex(index)
        state = Qt.Checked if item.checkState() == Qt.Unchecked \
            else Qt.Unchecked
        item.setCheckState(state)
        self._changed = True

    def set_current_data(self, data):
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

    def set_current_data_lte(self, val):
        """Sets the current index to the item who's data is nearest to val
           without going over (less than or equal to)

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

    def items_text(self):
        """Returns the text of the items of the combobox as a list

        Returns:
            [str]: List of all items' text
        """
        return [self.itemText(i) for i in range(0, self.count())]

    def items_data(self):
        """Returns the data of the items of the combobox as a list

        Returns:
            [Any]: List of all items' data
        """
        return [self.itemData(i) for i in range(0, self.count())]

    def checked_items_text(self):
        """Returns a list of the text of checked items

        Returns:
            [str]: List of checked items' text
        """
        return [self.itemText(i) for i in range(0, self.count())
                if self.model().item(i, 0).checkState() == Qt.Checked]

    def checked_items_data(self):
        """Returns a list of the data of checked items

        Returns:
            [Any]: List of checked items' data
        """
        return [self.itemData(i) for i in range(0, self.count())
                if self.model().item(i, 0).checkState() == Qt.Checked]

    def check_item_by_index(self, index, checked):
        """Checks an item identified by its index

        Args:
            index (int): Index of item to check
            checked (bool): True if item is to be checked

        Returns:
            bool: True if item is found
        """
        item = self.model().item(index, 0)
        if item:
            state = Qt.Checked if checked else Qt.Unchecked
            item.setCheckState(state)
            return True
        return False

    def check_item_by_text(self, text, checked):
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
            return True
        return False

    def check_item_by_data(self, data, checked):
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
            return True
        return False

    def check_items_by_text(self, text_list, checked):
        """Checks multiple items identified by their text

        Args:
            text_list ([str]): List of strings identifying items to check
            checked (bool): True if items are to be checked
        """
        for text in text_list:
            self.check_item_by_text(text, checked)

    def check_items_by_data(self, data_list, checked):
        """Checks multiple items identified by their data

        Args:
            data_list ([Any]): List of data values identifying items to check
            checked (bool): True if items are to be checked
        """
        for data in data_list:
            self.check_item_by_data(data, checked)

    def check_all(self, checked):
        """Checks or unchecks all items in list

        Args:
            checked (bool): True if items are to be checked
        """
        for i in range(0, self.count()):
            self.check_item_by_index(i, checked)

