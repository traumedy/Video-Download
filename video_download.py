#!/usr/bin/env python3

"""video_download.py - Parses bookmarks file and downloads videos
using the yt_dlp Python package.

Author: Josh Buchbinder
"""

import sys
import shutil
from html.parser import HTMLParser
from PySide6.QtCore import Qt, QFileInfo, QDir, QSettings
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox
from PySide6.QtWidgets import QFormLayout, QHBoxLayout, QVBoxLayout, QTextEdit
from PySide6.QtWidgets import QLineEdit, QPushButton, QLabel, QFileDialog
from PySide6.QtWidgets import QProgressBar, QDialog, QDialogButtonBox
from PySide6.QtWidgets import QListWidget, QCheckBox, QComboBox
from PySide6.QtWidgets import QAbstractItemView
from yt_dlp import YoutubeDL, utils
from overrides import override

# App name string used for settings
SETTINGS_COMPANYNAME = "MySoft"
SETTINGS_APPNAME = "Youtube-Download"
SETTINGS_VAL_URLLIST = "UrlList"
SETTINGS_VAL_DOWNLOADPATH = "DownloadPath"
SETTINGS_VAL_FFMPEGPATH = "FfmpegPath"
SETTINGS_VAL_USERNAME = "Username"
SETTINGS_VAL_PASSWORD = "Password"
SETTINGS_VAL_OVERWRITE = "Overwrite"
SETTINGS_VAL_KEEPVIDEO = "KeepVideo"
SETTINGS_VAL_FORMATEXT = "FormatExt"
SETTINGS_VAL_WINDOWWIDTH = "WindowWidth"
SETTINGS_VAL_WINDOWHEIGHT = "WindowHeight"

# Output container formats
format_ext_list = ["3gp", "aac", "flv", "m4a", "mp3", "mp4", "ogg", "wav",
                   "webm"]

# HTML Document types, not really used
DOCTYPE_UNKNOWN = 0
DOCTYPE_NETSCAPE = 1
DOCTYPE_SAFARI = 2


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
        self.folder_listbox.setCurrentItem(None)

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

    def handle_decl(self, decl):
        self.url_dict = {}
        if decl == "DOCTYPE NETSCAPE-Bookmark-file-1":
            self.doctype = DOCTYPE_NETSCAPE

    def handle_starttag(self, tag, attrs):
        if "h3" == tag:
            self.in_folder_title = True
        elif "a" == tag:
            # URLs are stored in href attribute of a tags
            for attr in attrs:
                if "href" == attr[0]:
                    self.url_dict[self.current_folder].append(attr[1])

    def handle_endtag(self, tag):
        if "h3" == tag:
            self.in_folder_title = False

    def handle_data(self, data):
        # Folder names are stored in data of H3 tags
        if self.in_folder_title:
            self.current_folder = data
            self.url_dict[self.current_folder] = []

    def set_parent(self, window):
        """Sets the parent window

        Args:
            window (QWidget): Parent window
        """
        self.parent_window = window

    def get_url_list(self):
        """Returns list of URL strings

        Returns:
            [str]: Extracted URLs or empty list
        """
        folders = list(self.url_dict.keys())
        if len(folders) == 1:
            # Only one folder, just return all the values
            return list(self.url_dict[folders[0]])
        if len(folders) > 1:
            dialog = FolderSelectDialog(self.parent_window)
            dialog.set_list(folders)
            if dialog.exec():
                folder = dialog.get_selected()
                if folder:
                    # Just return the list in the dictionary
                    return self.url_dict[folder]
                # Combine all the folder lists into one
                url_list = []
                for urls in list(self.url_dict.values()):
                    url_list.extend(urls)
                return url_list
        # Return empty URL list of no folders were found
        return []

    # List of extracted URLs
    url_dict = {}
    # Current document type
    doctype = DOCTYPE_UNKNOWN
    # Current tag
    current_tag = ""
    # Flag for in H3 tag
    in_folder_title = False
    # Current folder name
    current_folder = ""
    # Parent window for dialog
    parent_window = None


class MainWindow(QMainWindow):
    """Main application window class derived from QMainWindow
    """
    list_path_text: QLineEdit
    list_path_browse_button: QPushButton
    download_path_text: QLineEdit
    download_path_browse_button: QPushButton
    ffmpeg_path_text: QLineEdit
    ffmpeg_path_browse_button: QPushButton
    username_text: QLineEdit
    password_text: QLineEdit
    overwrite_check: QCheckBox
    keepvideo_check: QCheckBox
    format_ext_combo: QComboBox
    status_text: QTextEdit
    file_progress: QProgressBar
    total_progress: QProgressBar
    close_button: QPushButton
    download_button: QPushButton
    settings: QSettings

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video URL downloader")

        # Create widgets for window
        self.create_mainwindow_widgets()

        # Set widget tooltips
        self.create_mainwindow_tooltips()

        # Connect widget signals
        self.connect_mainwindow_signals()

        # Create central widget
        central_widget = QWidget()
        # Create window layout
        layout = self.create_mainwindow_layout()
        # Set the layout for the widget
        central_widget.setLayout(layout)
        # Set widget as main window central widget
        self.setCentralWidget(central_widget)

        # Persistent settings object
        self.settings = QSettings(SETTINGS_COMPANYNAME, SETTINGS_APPNAME)
        # Used to store downloaded filenames from progress hook callback
        self.download_filenames = []

        # Set minimum window size
        size = self.size()
        self.setMinimumSize(size)

        # Load persistent settings including stored window size
        self.load_settings()

    def create_mainwindow_widgets(self):
        """Create widgets for window
        """
        self.list_path_text = QLineEdit()
        self.list_path_browse_button = QPushButton("Browse...")
        self.download_path_text = QLineEdit()
        self.download_path_browse_button = QPushButton("Browse...")
        self.ffmpeg_path_text = QLineEdit()
        self.ffmpeg_path_browse_button = QPushButton("Browse...")
        self.username_text = QLineEdit()
        self.password_text = QLineEdit()
        self.overwrite_check = QCheckBox("Overwrite")
        self.keepvideo_check = QCheckBox("Keep video")
        self.format_ext_combo = QComboBox()
        self.status_text = QTextEdit()
        self.file_progress = QProgressBar()
        self.total_progress = QProgressBar()
        self.close_button = QPushButton("Cancel")
        self.download_button = QPushButton("Download videos")

        # Set widget properties
        self.status_text.setReadOnly(True)
        self.format_ext_combo.addItem("[Best quality]", "")
        for ext in format_ext_list:
            self.format_ext_combo.addItem(ext, ext)

    def create_mainwindow_layout(self):
        """Creates layout for main window

        Returns:
            QLayout: Layout for main window
        """
        # Create horizontal layouts to stack browse buttons next to paths
        list_path_layout = QHBoxLayout()
        list_path_layout.addWidget(self.list_path_text)
        list_path_layout.addWidget(self.list_path_browse_button)
        download_path_layout = QHBoxLayout()
        download_path_layout.addWidget(self.download_path_text)
        download_path_layout.addWidget(self.download_path_browse_button)
        ffmpeg_layout = QHBoxLayout()
        ffmpeg_layout.addWidget(self.ffmpeg_path_text)
        ffmpeg_layout.addWidget(self.ffmpeg_path_browse_button)
        auth_layout = QHBoxLayout()
        auth_layout.addWidget(QLabel("Username:"))
        auth_layout.addWidget(self.username_text)
        auth_layout.addWidget(QLabel("Password:"))
        auth_layout.addWidget(self.password_text)
        switches_layout = QHBoxLayout()
        switches_layout.addWidget(self.overwrite_check)
        switches_layout.addWidget(self.keepvideo_check)

        # Use Form Layout for window
        layout = QFormLayout()

        # Add widgets to window layout
        layout.addRow(QLabel("URL list:"), list_path_layout)
        layout.addRow(QLabel("Download path:"), download_path_layout)
        layout.addRow(QLabel("FFMPEG path:"), ffmpeg_layout)
        layout.addRow(auth_layout)
        layout.addRow(switches_layout)
        layout.addRow(QLabel("Download extension:"), self.format_ext_combo)
        layout.addRow(self.status_text)
        layout.addRow(QLabel("File progress"), self.file_progress)
        layout.addRow(QLabel("Total progress"), self.total_progress)
        layout.addRow(self.close_button, self.download_button)

        return layout

    def connect_mainwindow_signals(self):
        """Connects mainwindow signals to slots
        """
        self.list_path_browse_button.clicked.connect(
            self.list_browse_button_clicked)
        self.download_path_browse_button.clicked.connect(
            self.download_browse_button_clicked)
        self.ffmpeg_path_browse_button.clicked.connect(
            self.ffmpeg_browse_button_clicked)
        self.close_button.clicked.connect(self.close)
        self.download_button.clicked.connect(self.download_button_clicked)

    def create_mainwindow_tooltips(self):
        """Sets tooltips for main window widgets
        """
        # Set widget tooltips
        self.list_path_text.setToolTip(
            "The path to the list of URLs to download")
        self.list_path_browse_button.setToolTip(
            "Use dialog to browse to URL list path")
        self.download_path_text.setToolTip(
            "The path to the directory to download videos to")
        self.download_path_browse_button.setToolTip(
            "Use dialog to browse to download directory")
        self.ffmpeg_path_text.setToolTip(
            "Path to directory containing ffmpeg and ffprobe binaries")
        self.ffmpeg_path_browse_button.setToolTip(
            "Use fialog to browse to ffmpeg directory")
        self.username_text.setToolTip(
            "Username for authentication")
        self.password_text.setToolTip(
            "Password for authentication")
        self.overwrite_check.setToolTip(
            "Overwrite video files if they exist when downloading")
        self.keepvideo_check.setToolTip(
            "Keep video files after post processing")
        self.format_ext_combo.setToolTip(
            "Extension of the container format to download")
        self.status_text.setToolTip(
            "Status window")
        self.close_button.setToolTip(
            "Close this window")
        self.download_button.setToolTip(
            "Begin processing URL list and downloading video files")

    @override
    def closeEvent(self, event):
        """Overridden method

        Args:
            event (PySide6.QtGui.QCloseEvent): Event type
        """
        self.save_settings()
        event.accept()

    @staticmethod
    def value_to_bool(value):
        """Helper function to convert QSettings.value() to bool
        """
        return value.lower() == 'true'\
            if isinstance(value, str)\
            else bool(value)

    def load_settings(self):
        """Loads persistent settings
        """
        self.list_path_text.setText(
            self.settings.value(SETTINGS_VAL_URLLIST, ""))
        self.download_path_text.setText(
            self.settings.value(SETTINGS_VAL_DOWNLOADPATH, ""))
        # Default to ffmpeg in path
        ffmpeg_path = shutil.which("ffmpeg")
        if ffmpeg_path:
            # If ffmpeg found
            ffmpeg_info = QFileInfo(ffmpeg_path)
            ffmpeg_path = ffmpeg_info.dir().path()
        else:
            # ffmpeg executable not found in path
            ffmpeg_path = ""
        self.ffmpeg_path_text.setText(
            self.settings.value(SETTINGS_VAL_FFMPEGPATH,
                                ffmpeg_path))
        self.username_text.setText(
            self.settings.value(SETTINGS_VAL_USERNAME, ""))
        self.password_text.setText(
            self.settings.value(SETTINGS_VAL_PASSWORD, ""))
        self.overwrite_check.setChecked(self.value_to_bool(
            self.settings.value(SETTINGS_VAL_OVERWRITE)))
        self.keepvideo_check.setChecked(self.value_to_bool(
            self.settings.value(SETTINGS_VAL_KEEPVIDEO)))
        self.format_ext_combo.setCurrentText(
            self.settings.value(SETTINGS_VAL_FORMATEXT, ""))

        # Restore widow size
        size = self.size()
        width = int(self.settings.value(SETTINGS_VAL_WINDOWWIDTH,
                                        size.width()))
        height = int(self.settings.value(SETTINGS_VAL_WINDOWHEIGHT,
                                         size.height()))
        self.resize(width, height)

    def save_settings(self):
        """Save persistent settingss
        """
        self.settings.setValue(SETTINGS_VAL_URLLIST,
                               self.list_path_text.text())
        self.settings.setValue(SETTINGS_VAL_DOWNLOADPATH,
                               self.download_path_text.text())
        self.settings.setValue(SETTINGS_VAL_FFMPEGPATH,
                               self.ffmpeg_path_text.text())
        self.settings.setValue(SETTINGS_VAL_USERNAME,
                               self.username_text.text())
        self.settings.setValue(SETTINGS_VAL_PASSWORD,
                               self.password_text.text())
        self.settings.setValue(SETTINGS_VAL_OVERWRITE,
                               self.overwrite_check.isChecked())
        self.settings.setValue(SETTINGS_VAL_KEEPVIDEO,
                               self.keepvideo_check.isChecked())
        self.settings.setValue(SETTINGS_VAL_FORMATEXT,
                               self.format_ext_combo.currentText())
        self.settings.setValue(SETTINGS_VAL_WINDOWWIDTH,
                               self.width())
        self.settings.setValue(SETTINGS_VAL_WINDOWHEIGHT,
                               self.height())

    def list_browse_button_clicked(self):
        """Called when video list browse button is clicked
        """
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Browse for URL list...")
        # Set initial directory if present
        file_info = QFileInfo(self.list_path_text.text())
        if file_info.exists():
            file_dialog.setDirectory(file_info.dir())
        filters = ["HTML files (*.html)", "Text files (*.txt)"]
        file_dialog.setNameFilters(filters)
        file_dialog.selectNameFilter(filters[0])
        if file_dialog.exec():
            # Fill in text box
            selected_files = file_dialog.selectedFiles()
            self.list_path_text.setText(selected_files[0])

    def download_browse_button_clicked(self):
        """Called when download path browse button is clicked
        """
        # For initial directory
        dir_info = QFileInfo(self.download_path_text.text())
        # Simple dialog
        path = QFileDialog.getExistingDirectory(
            self,
            "Save videos to directory...",
            dir_info.filePath(),
            QFileDialog.ShowDirsOnly
            | QFileDialog.DontResolveSymlinks)
        if path:
            self.download_path_text.setText(path)

    def ffmpeg_browse_button_clicked(self):
        """Called when ffmpeg browse button is clicked
        """
        # For initial directory
        dir_info = QFileInfo(self.ffmpeg_path_text.text())
        # Simple dialog
        path = QFileDialog.getExistingDirectory(
            self,
            "FFMPEG location directory...",
            dir_info.filePath(),
            QFileDialog.ShowDirsOnly
            | QFileDialog.DontResolveSymlinks)
        if path:
            self.ffmpeg_path_text.setText(path)

    def download_button_clicked(self):
        """Called when download button is clicked
        """
        file_info = QFileInfo(self.list_path_text.text())
        dir_info = QFileInfo(self.download_path_text.text())
        if not file_info.exists():
            QMessageBox.warning(self, "Missing URL list",
                                "Enter the path to a valid list of URLs",
                                QMessageBox.StandardButton.Ok)
        elif not dir_info.isDir():
            QMessageBox.warning(self, "Missing download directory",
                                "Enter a valid directory for files to be "
                                "downloaded to",
                                QMessageBox.StandardButton.Ok)
        else:
            message = f"Processing URL list {file_info.absoluteFilePath()}"
            self.status_text.append(message)
            ext = file_info.completeSuffix().lower()
            url_list = []
            if ext == "txt":
                url_list = self.parse_txt_file(file_info.absoluteFilePath())
            elif ext == "html":
                url_list = self.parse_html_file(file_info.absoluteFilePath())
            else:
                QMessageBox.warning(self, "Unsupported file type",
                                    "Valid file types are HTML, TXT",
                                    QMessageBox.StandardButton.Ok)
            if url_list:
                # Store the current diretory to return after processing
                current_path = QDir.currentPath()
                # Change path to download directory
                QDir.setCurrent(dir_info.absoluteFilePath())
                # Download URLs
                self.download_url_list(url_list)
                # Return to current directory
                QDir.setCurrent(current_path)

    def parse_txt_file(self, file_path):
        """Parses a simple text file and builds a list of entries

        Args:
            file_path (str): Path to file to parse

        Returns:
            [str]: List of lines extracted from file
        """
        url_list = [line.strip('\n') for line in open(file_path, 'r',
                                                      encoding="utf-8")
                    .readlines() if line[0] != '#']
        # Remove blank lines
        url_list = [x for x in url_list if x]
        return url_list

    def parse_html_file(self, file_path):
        """Parses a HTML bookmark file and builds a list of entries.
        These files are exported from Chrome and Firefox

        Args:
            file_path (str): Path to file to parse

        Returns:
            [str]: List of lines extracted from file
        """
        # Use our custom HTML parser
        parser = BookmarkHTMLParser()
        parser.set_parent(self)
        # Feed file into parser
        with open(file_path, 'r', encoding="utf-8") as f:
            parser.feed(f.read())
        # Get URL list from parser
        return parser.get_url_list()

    def download_url_list(self, url_list):
        """Performs the downloading of URLs

        Args:
            url_list ([str]): List of URLs to download
        """
        # Reset progress bars
        self.file_progress.setRange(0, 100)
        self.file_progress.setValue(0)
        self.total_progress.setRange(0, len(url_list))
        self.total_progress.setValue(0)

        errors = []
        self.download_filenames = []
        count = 0

        # Set options for YoutubeDL
        ydl_opts = {}
        ydl_opts["quiet"] = True
        ydl_opts["verbose"] = False
        ydl_opts["no_warnings"] = True
        ffmpeg_path = self.ffmpeg_path_text.text()
        if ffmpeg_path:
            ydl_opts["ffmpeg_location"] = ffmpeg_path
        username = self.username_text.text()
        if username:
            ydl_opts["username"] = username
        password = self.password_text.text()
        if password:
            ydl_opts["password"] = password
        if self.overwrite_check.isChecked():
            ydl_opts["overwrites"] = True
        if self.keepvideo_check.isChecked():
            ydl_opts["keepvideo"] = True
        format_ext = self.format_ext_combo.currentData()
        if format_ext:
            ydl_opts["format"] = format_ext

        # Perform downloads
        with YoutubeDL(ydl_opts) as ydl:
            self.file_progress.setValue(0)
            ydl.add_progress_hook(self.ydl_progress_hook)
            for url in url_list:
                message = f"Trying download of URL {url}"
                self.status_text.append(message)
                try:
                    ydl.download(url)
                except utils.DownloadError as e:
                    errors.append(str(e))
                count += 1
                self.total_progress.setValue(count)

        message = f"{len(self.download_filenames)} downloads complete"
        if errors:
            message += f"\n{len(errors)} errors encountered"
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Download complete")
        dlg.setText(message)
        dlg.exec()

    def ydl_progress_hook(self, progress_dict):
        """Callback function for download progress

        Args:
            progress_dict ({str:str}): progress dictionary
        """
        status = ""
        if "status" in progress_dict:
            status = progress_dict["status"]

        if "downloaded_bytes" in progress_dict and\
                "total_bytes" in progress_dict and\
                "downloading" == status:
            file_bytes = progress_dict["downloaded_bytes"]
            file_total = progress_dict["total_bytes"]
            value = int(100 * file_bytes / file_total)
            self.file_progress.setValue(value)
        if "filename" in progress_dict:
            filename = progress_dict["filename"]
            if filename not in self.download_filenames:
                self.download_filenames.append(filename)
                message = f"Downloading file {filename}"
                self.status_text.append(message)
            if "finished" == status:
                message = f"Finished with file {filename}"
                self.status_text.append(message)
            elif "error" == status:
                message = f"Error with file {filename}"
                self.status_text.append(message)

        # Drive message loop
        QApplication.processEvents()


def main(argv):
    """ Main function entry point

    Args:
        argv ([str]): Command line arguments

    Returns:
        int: ERRNO value
    """

    # Create application
    app = QApplication(argv)

    # Create window
    window = MainWindow()
    window.show()

    # Start event loop
    app.exec()


# Entry point
if __name__ == "__main__":
    main(sys.argv)
    exit(0)
