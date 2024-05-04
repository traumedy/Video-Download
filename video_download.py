#!/usr/bin/env python3

"""video_download.py - Parses bookmarks file and downloads videos
using the yt_dlp Python package.

Author: Josh Buchbinder
"""

import sys
import shutil
import re
from html.parser import HTMLParser
from PySide6.QtCore import Qt, QFileInfo, QDir, QUrl, QSettings
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox
from PySide6.QtWidgets import QFormLayout, QHBoxLayout, QVBoxLayout, QTextEdit
from PySide6.QtWidgets import QLineEdit, QPushButton, QLabel, QFileDialog
from PySide6.QtWidgets import QProgressBar, QDialog, QDialogButtonBox
from PySide6.QtWidgets import QListWidget, QCheckBox, QComboBox, QStyle
from PySide6.QtWidgets import QSizePolicy, QStackedLayout
from yt_dlp import YoutubeDL, utils
from overrides import override

# App name string used for settings
SETTINGS_COMPANYNAME = "MySoft"
SETTINGS_APPNAME = "Youtube-Download"
SETTINGS_VAL_URLTYPE = "UrlType"
SETTINGS_VAL_URLTEXT = "UrlText"
SETTINGS_VAL_URLLIST = "UrlList"
SETTINGS_VAL_DOWNLOADPATH = "DownloadPath"
SETTINGS_VAL_FFMPEGPATH = "FfmpegPath"
SETTINGS_VAL_USERNAME = "Username"
SETTINGS_VAL_PASSWORD = "Password"
SETTINGS_VAL_OVERWRITE = "Overwrite"
SETTINGS_VAL_KEEPVIDEO = "KeepVideo"
SETTINGS_VAL_PREFERFREEFORMATS = "PreferFreeFormats"
SETTINGS_VAL_FORMATTYPE = "FormatType"
SETTINGS_VAL_FORMATQUALITY = "FormatQuality"
SETTINGS_VAL_FORMATAUDEXT = "FormatAudExt"
SETTINGS_VAL_FORMATVIDEXT = "FormatVidExt"
SETTINGS_VAL_FORMATAUDCODEC = "FormatAudCodec"
SETTINGS_VAL_FORMATVIDCODEC = "FormatVidCodec"
SETTINGS_VAL_FORMATSTRING = "FormatString"
SETTINGS_VAL_WINDOWWIDTH = "WindowWidth"
SETTINGS_VAL_WINDOWHEIGHT = "WindowHeight"

url_type_labels = ["Single URL:", "URL List:"]

URL_TYPE_SINGLE = 0
URL_TYPE_LIST = 1

FORMAT_TYPE_AUDVID_BY_QUA = 0
FORMAT_TYPE_AUD_BY_QUA = 1
FORMAT_TYPE_VID_BY_QUA = 2
FORMAT_TYPE_AUDVID_BY_EXT = 3
FORMAT_TYPE_AUD_BY_EXT = 4
FORMAT_TYPE_VID_BY_EXT = 5
FORMAT_TYPE_AUD_BY_CODEC = 6
FORMAT_TYPE_VID_BY_CODEC = 7
FORMAT_TYPE_RAWSTRING = 8

format_type_list = [
    ("Audio+Video by quality", FORMAT_TYPE_AUDVID_BY_QUA),
    ("Audio only by quality", FORMAT_TYPE_AUD_BY_QUA),
    ("Video only by quality", FORMAT_TYPE_VID_BY_QUA),
    ("Audio+Video by extension", FORMAT_TYPE_AUDVID_BY_EXT),
    ("Audio only by extension", FORMAT_TYPE_AUD_BY_EXT),
    ("Video only by extension", FORMAT_TYPE_VID_BY_EXT),
    ("Audio only by codec", FORMAT_TYPE_AUD_BY_CODEC),
    ("Video only by codec", FORMAT_TYPE_VID_BY_CODEC),
    ("Raw format string", FORMAT_TYPE_RAWSTRING)
]

format_labels_quality_list = ["Best quality", "Second best quality",
                              "Third best quality", "Fourth best quality"]

# Output container formats
format_ext_list = ["3gp", "aac", "flv", "m4a", "mp3", "mp4", "ogg", "wav",
                   "webm"]
format_ext_aud_list = ["m4a", "aac", "mp3", "ogg", "opus", "webm"]
format_ext_vid_list = ["mp4", "mov", "webm", "flv", "3gp"]
# Audio and video Codecs
format_codec_aud_list = ["flac", "alac", "wav", "aiff", "opus", "vorbis",
                         "aac", "mp4a", "mp3", "ac4", "eac3", "ac3", "dts"]
format_codec_vid_list = [("av01", "av01"), ("vp9.2", "vp09.2"),
                         ("vp9", "vp09"), ("avc1", "avc1"),
                         ("h265", "h265"), ("h264", "h265"),
                         ("vp8", "vp08"), ("h263", "h263"),
                         ("theora", "theora")]

# URL list file extensions
URLLIST_EXTENSIONS = ["html", "txt"]

# URL for format string help
FORMAT_STRING_HELP_URL = "https://github.com/yt-dlp/yt-dlp/blob/"\
    "master/README.md#format-selection"

# HTML Document types, not really used
DOCTYPE_UNKNOWN = 0
DOCTYPE_NETSCAPE = 1
DOCTYPE_SAFARI = 2

# Regex to strip color codes from string
REGEX_COLORSTRIP = r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]'


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
    # Current document type
    doctype = DOCTYPE_UNKNOWN
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
        if decl == "DOCTYPE NETSCAPE-Bookmark-file-1":
            self.doctype = DOCTYPE_NETSCAPE

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


class MainWindow(QMainWindow):
    """Main application window class derived from QMainWindow
    """
    url_type_combo: QComboBox
    url_stacked_layout: QStackedLayout
    url_text: QLineEdit
    list_path_layout_widget: QWidget
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
    preferfreeformats_check: QCheckBox
    format_stacked_layout: QStackedLayout
    format_type_combo: QComboBox
    format_quality_combo: QComboBox
    format_audext_combo: QComboBox
    format_vidext_combo: QComboBox
    format_audcodec_combo: QComboBox
    format_vidcodec_combo: QComboBox
    format_string_layout_widget: QWidget
    format_string_text: QLineEdit
    format_string_help_button: QPushButton
    status_text: QTextEdit
    file_progress: QProgressBar
    total_progress: QProgressBar
    close_button: QPushButton
    download_button: QPushButton
    bottom_buttonbox: QDialogButtonBox
    settings: QSettings

    def __init__(self):
        super().__init__()
        # Set title text for window
        self.setWindowTitle("Video URL downloader")

        # Set an icon for our window
        pixmapi = QStyle.StandardPixmap.SP_DialogSaveButton
        icon = self.style().standardIcon(pixmapi)
        self.setWindowIcon(icon)

        # Create widgets for window
        self.create_mainwindow_widgets()
        # Create central widget
        central_widget = QWidget()
        # Create window layout
        layout = self.create_mainwindow_layout()
        # Set the layout for the widget
        central_widget.setLayout(layout)
        # Set widget as main window central widget
        self.setCentralWidget(central_widget)
        # Connect widget signals
        self.connect_mainwindow_signals()
        # Set widget tooltips
        self.create_mainwindow_tooltips()

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
        self.url_type_combo = QComboBox()
        self.url_text = QLineEdit()
        self.list_path_layout_widget = QWidget()
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
        self.preferfreeformats_check = QCheckBox("Prefer free formats")
        self.format_type_combo = QComboBox()
        self.format_quality_combo = QComboBox()
        self.format_audext_combo = QComboBox()
        self.format_vidext_combo = QComboBox()
        self.format_audcodec_combo = QComboBox()
        self.format_vidcodec_combo = QComboBox()
        self.format_string_layout_widget = QWidget()
        self.format_string_text = QLineEdit()
        self.format_string_help_button = QPushButton("Help")
        self.status_text = QTextEdit()
        self.file_progress = QProgressBar()
        self.total_progress = QProgressBar()
        self.close_button = QPushButton("Close")
        self.download_button = QPushButton("Download videos")
        self.bottom_buttonbox = QDialogButtonBox()

        # Set widget properties

        # Populate url type listbox
        for label in url_type_labels:
            self.url_type_combo.addItem(label)
        # These Expanding policies seem necessary for Mac to get the
        #  QLineEdit fields to expand to fill
        self.list_path_text.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum)
        self.list_path_browse_button.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Minimum)
        self.download_path_text.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Maximum)
        self.download_path_browse_button.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Minimum)
        self.ffmpeg_path_text.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Maximum)
        self.ffmpeg_path_browse_button.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Minimum)
        # Set status QTextEdit to read only for status logs
        self.status_text.setReadOnly(True)
        # Populate format selection combo boxes
        for label, idx in format_type_list:
            self.format_type_combo.addItem(label, idx)
        for idx, label in enumerate(format_labels_quality_list):
            self.format_quality_combo.addItem(label, "." + str(idx + 1))
        for ext in format_ext_aud_list:
            self.format_audext_combo.addItem(ext, ext)
        for ext in format_ext_vid_list:
            self.format_vidext_combo.addItem(ext, ext)
        for codec in format_codec_aud_list:
            self.format_audcodec_combo.addItem(codec, codec)
        for codec, cstr in format_codec_vid_list:
            self.format_vidcodec_combo.addItem(codec, cstr)

        # Populate dialog button box
        self.bottom_buttonbox.addButton(self.close_button,
                                        QDialogButtonBox.ButtonRole.RejectRole)
        self.bottom_buttonbox.addButton(self.download_button,
                                        QDialogButtonBox.ButtonRole.AcceptRole)

    def create_mainwindow_layout(self):
        """Creates layout for main window

        Returns:
            QLayout: Layout for main window
        """
        # Create horizontal layouts to stack browse buttons next to paths

        list_path_layout = QHBoxLayout(self.list_path_layout_widget)
        list_path_layout.addWidget(self.list_path_text)
        list_path_layout.addWidget(self.list_path_browse_button, 0,
                                   Qt.AlignmentFlag.AlignRight)
        self.url_stacked_layout = QStackedLayout()
        self.url_stacked_layout.addWidget(self.url_text)
        self.url_stacked_layout.addWidget(self.list_path_layout_widget)

        download_path_layout = QHBoxLayout()
        download_path_layout.addWidget(self.download_path_text)
        download_path_layout.addWidget(self.download_path_browse_button, 0,
                                       Qt.AlignmentFlag.AlignRight)
        ffmpeg_layout = QHBoxLayout()
        ffmpeg_layout.addWidget(self.ffmpeg_path_text)
        ffmpeg_layout.addWidget(self.ffmpeg_path_browse_button, 0,
                                Qt.AlignmentFlag.AlignRight)
        auth_layout = QHBoxLayout()
        auth_layout.addWidget(QLabel("Username:"))
        auth_layout.addWidget(self.username_text)
        auth_layout.addWidget(QLabel("Password:"))
        auth_layout.addWidget(self.password_text)
        switches_layout = QHBoxLayout()
        switches_layout.addWidget(self.overwrite_check)
        switches_layout.addWidget(self.keepvideo_check)
        switches_layout.addWidget(self.preferfreeformats_check)
        self.format_stacked_layout = QStackedLayout()
        self.format_stacked_layout.addWidget(self.format_quality_combo)
        self.format_stacked_layout.addWidget(self.format_audext_combo)
        self.format_stacked_layout.addWidget(self.format_vidext_combo)
        self.format_stacked_layout.addWidget(self.format_audcodec_combo)
        self.format_stacked_layout.addWidget(self.format_vidcodec_combo)
        format_string_layout = QHBoxLayout(
            self.format_string_layout_widget)
        format_string_layout.addWidget(QLabel("Format string:"))
        format_string_layout.addWidget(self.format_string_text)
        format_string_layout.addWidget(self.format_string_help_button)
        self.format_stacked_layout.addWidget(self.format_string_layout_widget)
        format_type_layout = QHBoxLayout()
        format_type_layout.addWidget(QLabel("Format selection:"))
        format_type_layout.addWidget(self.format_type_combo)
        format_type_layout.addLayout(self.format_stacked_layout)

        # By default the layout is too tall for the QStackedLayout
        format_string_layout.setContentsMargins(0, 0, 0, 0)
        list_path_layout.setContentsMargins(0, 0, 0, 0)

        # Use Form Layout for window
        layout = QFormLayout()

        # Add widgets to window layout
        layout.addRow(self.url_type_combo, self.url_stacked_layout)
        layout.addRow(QLabel("Download path:"), download_path_layout)
        layout.addRow(QLabel("FFMPEG path:"), ffmpeg_layout)
        layout.addRow(auth_layout)
        layout.addRow(switches_layout)
        layout.addRow(format_type_layout)
        layout.addRow(self.status_text)
        layout.addRow(QLabel("File progress"), self.file_progress)
        layout.addRow(QLabel("Total progress"), self.total_progress)
        layout.addRow(QLabel(""))
        layout.addRow(self.bottom_buttonbox)

        return layout

    def connect_mainwindow_signals(self):
        """Connects main window signals to slots
        """
        self.url_type_combo.currentIndexChanged.connect(
            self.url_stacked_layout.setCurrentIndex)
        self.list_path_browse_button.clicked.connect(
            self.list_browse_button_clicked)
        self.download_path_browse_button.clicked.connect(
            self.download_browse_button_clicked)
        self.ffmpeg_path_browse_button.clicked.connect(
            self.ffmpeg_browse_button_clicked)
        self.format_type_combo.currentIndexChanged.connect(
            self.format_type_combo_changed)
        self.format_string_help_button.clicked.connect(
            self.format_string_help_button_clicked)
        self.close_button.clicked.connect(
            self.close)
        self.download_button.clicked.connect(
            self.download_button_clicked)

    def create_mainwindow_tooltips(self):
        """Sets tooltips for main window widgets
        """
        # Set widget tooltips
        self.url_type_combo.setToolTip(
            "Select either a single URL to download or a URL list")
        self.url_text.setToolTip(
            "The URL of a page with a video to download")
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
        self.preferfreeformats_check.setToolTip(
            "Whether to prefer video formats with free containers over "
            "non-free ones of same quality")
        self.format_type_combo.setToolTip(
            "Select which method of format selection to use")
        self.format_quality_combo.setToolTip(
            "Select the quality level to download. "
            "Different quality levels may result in different file types. "
            "Not all quality levels may be available.")
        self.format_audext_combo.setToolTip(
            "Select the audio file extension to download. "
            "This does not guarantee a specific codec."
            "Different sites will have different file types available and "
            "may not offer all types.")
        self.format_vidext_combo.setToolTip(
            "Select the video file extension to download. "
            "This does not guarantee a specific codec. "
            "Different sites will have different file types available and "
            "may not offer all types.")
        self.format_audcodec_combo.setToolTip(
            "Select the audio codec to download."
            "Different sites will have different audio codecs available and "
            "may not offer all types.")
        self.format_vidcodec_combo.setToolTip(
            "Select the video codec to download."
            "Different sites will have different video codecs available and "
            "may not offer all types.")
        self.format_string_text.setToolTip(
            "Enter the string representing the format to download. Click "
            "the Help button for more information.")
        self.format_string_help_button.setToolTip(
            "Launches a browser directed to detailed information about "
            "creating yt-dlp format strings.")
        self.status_text.setToolTip(
            "Status window")
        self.close_button.setToolTip(
            "Close this window")
        self.download_button.setToolTip(
            "Begin processing URL list and downloading video files")

    @override
    def closeEvent(self, event):
        """Overridden method, called when window is closing

        Args:
            event (PySide6.QtGui.QCloseEvent): Event type
        """
        self.save_settings()
        event.accept()

    @override
    def dragEnterEvent(self, event):
        """Overriden method, called when a file is dragged over window

        Args:
            event (QDragEnterEvent): Event info
        """
        drag_url = QUrl(event.mimeData().text())
        if drag_url.isLocalFile():
            drag_file = QFileInfo(drag_url.toLocalFile())
            suffix = drag_file.suffix().lower()
            if suffix in URLLIST_EXTENSIONS:
                event.accept()
                return
        event.ignore()

    @override
    def dropEvent(self, event):
        """Overriden method, called when a file is dropped on window

        Args:
            event (QDragEvent): Event info
        """
        drag_url = QUrl(event.mimeData().text())
        if drag_url.isLocalFile():
            drag_file = QFileInfo(drag_url.toLocalFile())
            self.list_path_text.setText(drag_file.filePath())
            event.accept()
            return
        event.ignore()

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
        self.url_type_combo.setCurrentText(
            self.settings.value(SETTINGS_VAL_URLTYPE, ""))
        self.url_text.setText(
            self.settings.value(SETTINGS_VAL_URLTEXT, ""))
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
        self.preferfreeformats_check.setChecked(self.value_to_bool(
            self.settings.value(SETTINGS_VAL_PREFERFREEFORMATS)))
        self.format_type_combo.setCurrentText(
            self.settings.value(SETTINGS_VAL_FORMATTYPE, ""))
        self.format_quality_combo.setCurrentText(
            self.settings.value(SETTINGS_VAL_FORMATQUALITY, ""))
        self.format_audext_combo.setCurrentText(
            self.settings.value(SETTINGS_VAL_FORMATAUDEXT, ""))
        self.format_vidext_combo.setCurrentText(
            self.settings.value(SETTINGS_VAL_FORMATVIDEXT, ""))
        self.format_audcodec_combo.setCurrentText(
            self.settings.value(SETTINGS_VAL_FORMATAUDCODEC, ""))
        self.format_vidcodec_combo.setCurrentText(
            self.settings.value(SETTINGS_VAL_FORMATVIDCODEC, ""))
        self.format_string_text.setText(
            self.settings.value(SETTINGS_VAL_FORMATSTRING, ""))

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
        self.settings.setValue(SETTINGS_VAL_URLTYPE,
                               self.url_type_combo.currentText())
        self.settings.setValue(SETTINGS_VAL_URLTEXT,
                               self.url_text.text())
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
        self.settings.setValue(SETTINGS_VAL_PREFERFREEFORMATS,
                               self.preferfreeformats_check.isChecked())
        self.settings.setValue(SETTINGS_VAL_FORMATTYPE,
                               self.format_type_combo.currentText())
        self.settings.setValue(SETTINGS_VAL_FORMATQUALITY,
                               self.format_quality_combo.currentText())
        self.settings.setValue(SETTINGS_VAL_FORMATAUDEXT,
                               self.format_audext_combo.currentText())
        self.settings.setValue(SETTINGS_VAL_FORMATVIDEXT,
                               self.format_vidext_combo.currentText())
        self.settings.setValue(SETTINGS_VAL_FORMATAUDCODEC,
                               self.format_audcodec_combo.currentText())
        self.settings.setValue(SETTINGS_VAL_FORMATVIDCODEC,
                               self.format_vidcodec_combo.currentText())
        self.settings.setValue(SETTINGS_VAL_FORMATSTRING,
                               self.format_string_text.text())
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

    def format_type_combo_changed(self, new_index):
        """Called when format type combo changes

        Args:
            new_index (int): Index of newly selected item
        """
        type_id = self.format_type_combo.itemData(new_index)
        if type_id in [FORMAT_TYPE_AUDVID_BY_QUA,
                       FORMAT_TYPE_AUD_BY_QUA,
                       FORMAT_TYPE_VID_BY_QUA]:
            self.format_stacked_layout.setCurrentWidget(
                self.format_quality_combo)
        elif type_id == FORMAT_TYPE_AUD_BY_EXT:
            self.format_stacked_layout.setCurrentWidget(
                self.format_audext_combo)
        elif type_id in [FORMAT_TYPE_VID_BY_EXT, FORMAT_TYPE_AUDVID_BY_EXT]:
            self.format_stacked_layout.setCurrentWidget(
                self.format_vidext_combo)
        elif type_id == FORMAT_TYPE_AUD_BY_CODEC:
            self.format_stacked_layout.setCurrentWidget(
                self.format_audcodec_combo)
        elif type_id == FORMAT_TYPE_VID_BY_CODEC:
            self.format_stacked_layout.setCurrentWidget(
                self.format_vidcodec_combo)
        elif type_id == FORMAT_TYPE_RAWSTRING:
            self.format_stacked_layout.setCurrentWidget(
                self.format_string_layout_widget)

    def format_string_help_button_clicked(self):
        """Called when string help button is clicked
        """
        QDesktopServices.openUrl(FORMAT_STRING_HELP_URL)

    def download_button_clicked(self):
        """Called when download button is clicked
        """
        dir_info = QFileInfo(self.download_path_text.text())
        if not dir_info.isDir():
            QMessageBox.warning(self, "Missing download directory",
                                "Enter a valid directory for files to be "
                                "downloaded to",
                                QMessageBox.StandardButton.Ok)
            return
        url_list = []
        url_type_index = self.url_type_combo.currentIndex()
        if url_type_index == URL_TYPE_SINGLE:
            url = self.url_text.text()
            if not url:
                QMessageBox.warning(self, "Missing download URL",
                                    "Enter a valid URL to be downloaded",
                                    QMessageBox.StandardButton.Ok)
                return

            url_list = [url]
        elif url_type_index == URL_TYPE_LIST:
            file_info = QFileInfo(self.list_path_text.text())
            if not file_info.exists():
                QMessageBox.warning(self, "Missing URL list",
                                    "Enter the path to a valid list of URLs",
                                    QMessageBox.StandardButton.Ok)
            else:
                message = f"Processing URL list {file_info.absoluteFilePath()}"
                self.add_status_message(message)
                ext = file_info.completeSuffix().lower()
                url_list = []
                if ext == "txt":
                    url_list = self.parse_txt_file(
                        file_info.absoluteFilePath())
                elif ext == "html":
                    url_list = self.parse_html_file(
                        file_info.absoluteFilePath())
                else:
                    QMessageBox.warning(self, "Unsupported file type",
                                        "Valid file types are HTML, TXT",
                                        QMessageBox.StandardButton.Ok)
        # Process URLs
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
        parser = BookmarkHTMLParser(self)
        # Feed file into parser
        with open(file_path, 'r', encoding="utf-8") as f:
            parser.feed(f.read())
        # Get URL list from parser
        return parser.get_url_list()

    def create_ydl_options(self):
        """Creates the dictionary of options to pass to YoutubeDL
        built from UI values and set some default values

        Returns:
            dict: Dictionary of options for yt_dlp.YoutubeDL constructor
        """
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
        if self.preferfreeformats_check.isChecked():
            ydl_opts["prefer_free_formats"] = True

        # Create format string
        format_str = ""
        type_id = self.format_type_combo.currentData()
        if type_id in [FORMAT_TYPE_AUDVID_BY_QUA,
                       FORMAT_TYPE_AUD_BY_QUA,
                       FORMAT_TYPE_VID_BY_QUA]:
            quality_str = self.format_quality_combo.currentData()
            if type_id == FORMAT_TYPE_AUDVID_BY_QUA:
                format_str = "best" + quality_str
            elif type_id == FORMAT_TYPE_AUD_BY_QUA:
                format_str = "bestaudio" + quality_str
            elif type_id == FORMAT_TYPE_VID_BY_QUA:
                format_str = "bestvideo" + quality_str
        elif type_id == FORMAT_TYPE_AUDVID_BY_EXT:
            ext = self.format_vidext_combo.currentData()
            format_str = ext
        elif type_id == FORMAT_TYPE_AUD_BY_EXT:
            ext = self.format_audext_combo.currentData()
            format_str = f"bestaudio[ext={ext}]"
        elif type_id == FORMAT_TYPE_VID_BY_EXT:
            ext = self.format_vidext_combo.currentData()
            format_str = f"bestvideo[ext={ext}]"
        elif type_id == FORMAT_TYPE_AUD_BY_CODEC:
            codec = self.format_audcodec_combo.currentData()
            format_str = f"ba[acodec^={codec}]"
        elif type_id == FORMAT_TYPE_VID_BY_CODEC:
            codec = self.format_vidcodec_combo.currentData()
            format_str = f"bv[vcodec^={codec}]"
        elif type_id == FORMAT_TYPE_RAWSTRING:
            format_str = self.format_string_text.text()
        if format_str:
            message = f"Using format string: {format_str}"
            self.add_status_message(message)
            ydl_opts["format"] = format_str
        return ydl_opts

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

        # Disable widgets that would interfere with processing
        self.enable_active_buttons(False)

        errors = []
        self.download_filenames = []
        count = 0
        ydl_opts = self.create_ydl_options()

        # Perform downloads
        with YoutubeDL(ydl_opts) as ydl:
            self.file_progress.setValue(0)
            ydl.add_progress_hook(self.ydl_progress_hook)
            for url in url_list:
                message = f"Trying download of URL {url}"
                self.add_status_message(message)
                try:
                    ydl.download(url)
                except utils.DownloadError as e:
                    error_message = str(e)
                    errors.append(error_message)
                    message = f"Download error: {error_message}"
                    self.add_status_message(message)
                count += 1
                self.total_progress.setValue(count)

        # Reenable widgets
        self.enable_active_buttons(True)

        # Display summary message box
        message = f"{len(url_list)} URLs processed"
        message += f"\n{len(self.download_filenames)} downloads complete"
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
                self.add_status_message(message)
            if "finished" == status:
                message = f"Finished with file {filename}"
                self.add_status_message(message)
            elif "error" == status:
                message = f"Error with file {filename}"
                self.add_status_message(message)

        # Drive message loop
        QApplication.processEvents()

    def strip_color_codes(self, message):
        """Removes console color escape codes from string

        Args:
            message (str): Message with possible color codes

        Returns:
            str: message with color escape codes removed
        """
        regex = re.compile(REGEX_COLORSTRIP)
        return regex.sub("", message)

    def add_status_message(self, message):
        """Adds text to the status window and scrolls to the bottom

        Args:
            message (str): Message text to add
        """
        self.status_text.append(self.strip_color_codes(message))
        self.status_text.verticalScrollBar().setValue(
            self.status_text.verticalScrollBar().maximum())
        # Drive message loop
        QApplication.processEvents()

    def enable_active_buttons(self, enable):
        """Enables or disables widgets while downloading is in progress

        Args:
            enable (bool): Enable widgets flag
        """
        self.bottom_buttonbox.setEnabled(enable)


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
