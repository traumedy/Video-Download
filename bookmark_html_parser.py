#!/usr/bin/env python3

"""bookmark_html_parser.py - Class for parsing HTML of exported
browser bookmarks to extract URLs.
"""

from html.parser import HTMLParser
from overrides import override
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout
from PySide6.QtWidgets import QLabel, QListWidget


class FolderSelectDialog(QDialog):
    """Simple dialog box allowing selection of an item from a list
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Select bookmark folder")
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.button_box = QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Select the folder of URLs or none for all folders")
        self.folder_listbox = QListWidget()
        self.layout.addWidget(message)
        self.layout.addWidget(self.folder_listbox)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def set_list(self, folder_list):
        """Sets string list for selection

        Args:
            folder_list ([str]): List of strings for selection
        """
        self.folder_listbox.insertItems(0, folder_list)

    def get_selected(self):
        """Returns string of selected item

        Returns:
            str: String of selected item or empty string if none selected
        """
        # List should be in single selection mode so return first item
        for item in self.folder_listbox.selectedItems():
            return item.text()
        return ""


class BookmarkHTMLParser(HTMLParser):
    """HTML parsing class derived from HTMLParser
    """
    # List of extracted URLs
    url_dict = {}
    # Current tag
    current_tag = ""
    # Flag for in H3 tag
    in_folder_title = False
    # Current folder name
    current_folder = ""
    # Parent window for dialog
    parent_widget = None

    def __init__(self, parent=None):
        super().__init__()
        # Store parent widget for folder dialog
        self.parent_widget = parent
        # Handle case of URLs before a folder name
        self.url_dict[""] = []

    @override
    def handle_decl(self, decl):
        """Overriden method, handles doctype decleration tags

        Args:
            decl (str): DOCTYPE string
        """
        # Beginning of document, clear dictionary
        self.url_dict[""] = []

    @override
    def handle_starttag(self, tag, attrs):
        """Overriden method, handles tag opening

        Args:
            tag (str): Tag name
            attrs (dict): Dictionary of attributes for start tag
        """
        if "h3" == tag:
            self.in_folder_title = True
        elif "a" == tag:
            # URLs are stored in href attribute of a tags
            for attr in attrs:
                if "href" == attr[0]:
                    self.url_dict[self.current_folder].append(attr[1])

    @override
    def handle_endtag(self, tag):
        """Overriden method, handles tag closing

        Args:
            tag (str): Tag name
        """
        if "h3" == tag:
            self.in_folder_title = False

    def handle_data(self, data):
        """Overriden method, handles data between tags

        Args:
            data (str): The data between tags
        """
        # Folder names are stored in data of H3 tags
        if self.in_folder_title:
            self.current_folder = data
            self.url_dict[self.current_folder] = []

    def get_url_list(self):
        """Returns list of URL strings

        Returns:
            [str]: Extracted URLs or empty list
        """
        # Make list of folder names that actually contain URLs
        folders = [key for key, val in self.url_dict.items() if val]
        if len(folders) == 1:
            # Only one folder, just return all the values
            return list(self.url_dict[folders[0]])
        if len(folders) > 1:
            dialog = FolderSelectDialog(self.parent_widget)
            dialog.set_list(folders)
            if dialog.exec():
                folder = dialog.get_selected()
                if folder:
                    # Just return the list in the dictionary
                    return self.url_dict[folder]
                # No folder selected, combine all the folder lists into one
                url_list = []
                for urls in list(self.url_dict.values()):
                    url_list.extend(urls)
                return url_list
        # Return empty URL list of no folders were found
        return []
