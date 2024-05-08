#!/usr/bin/env python3

"""video_download.py - Download videos or lists of videos
including bookmarks exported from browsers from video sites
like YouTube, Vimeo, Instagram, etc using the yt_dlp Python package.

Author: Josh Buchbinder
"""

import sys
import shutil
import re
from html.parser import HTMLParser
from PySide6.QtCore import Qt, QFileInfo, QDir, QUrl, QSettings
from PySide6.QtGui import QDesktopServices, QFont, QBrush, QColor
from PySide6.QtGui import QTextDocument, QTextTable, QTextTableFormat
from PySide6.QtGui import QTextTableCell, QTextCursor
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox
from PySide6.QtWidgets import QFormLayout, QHBoxLayout, QVBoxLayout, QTextEdit
from PySide6.QtWidgets import QLineEdit, QPushButton, QLabel, QFileDialog
from PySide6.QtWidgets import QProgressBar, QDialog, QDialogButtonBox, QSpinBox
from PySide6.QtWidgets import QListWidget, QCheckBox, QComboBox, QStyle
from PySide6.QtWidgets import QSizePolicy, QStackedWidget
from yt_dlp import YoutubeDL, utils
from overrides import override

# Monospace font name used for status window text
MONOSPACE_FONT_NAME = "Monospace"

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
SETTINGS_VAL_CONSOLEOUTPUT = "ConsoleOutput"
SETTINGS_VAL_PREFERFREEFORMATS = "PreferFreeFormats"
SETTINGS_VAL_DOWNLOADSUBTITLES = "DownloadSubtitles"
SETTINGS_VAL_SUBTITLEFORMAT = "SubtitleFormat"
SETTINGS_VAL_SUBTITLESGENERATED = "SubtitlesGenerated"
SETTINGS_VAL_SUBTITLELANGUAGE = "SubtitleLanguage"
SETTINGS_VAL_SUBTITLEDELAY = "SubtitleDelay"
SETTINGS_VAL_FORMATTYPE = "FormatType"
SETTINGS_VAL_FORMATQUALITY = "FormatQuality"
SETTINGS_VAL_FORMATAUDEXT = "FormatAudExt"
SETTINGS_VAL_FORMATVIDEXT = "FormatVidExt"
SETTINGS_VAL_FORMATAUDCODEC = "FormatAudCodec"
SETTINGS_VAL_FORMATVIDCODEC = "FormatVidCodec"
SETTINGS_VAL_FORMATMERGEAUD = "FormatMergeAud"
SETTINGS_VAL_FORMATMERGEVID = "FormatMergeVid"
SETTINGS_VAL_FORMATSTRING = "FormatString"
SETTINGS_VAL_WINDOWWIDTH = "WindowWidth"
SETTINGS_VAL_WINDOWHEIGHT = "WindowHeight"

url_type_labels = ["Single URL:", "URL List:"]

URL_TYPE_SINGLE = 0
URL_TYPE_LIST = 1

SUBTITLES_FORMAT_LIST = [("vtt", True), ("ttml", True), ("srv3", True),
                         ("srv2", True), ("srv1", True), ("json3", True),
                         ("ass", False), ("lrc", False), ("srt", False)]
SUBTITLES_LANGUAGES_LIST = [("Afrikaans", "af"), ("Akan", "ak"),
                            ("Albanian", "sq"), ("Amharic", "am"),
                            ("Arabic", "ar"), ("Armenian", "hy"),
                            ("Assamese", "as"), ("Aymara", "ay"),
                            ("Azerbaijani", "az"), ("Bangla", "bn"),
                            ("Basque", "eu"), ("Belarusian", "be"),
                            ("Bhojpuri", "bho"), ("Bosnian", "bs"),
                            ("Bulgarian", "bg"), ("Burmese", "my"),
                            ("Catalan", "ca"), ("Cebuano", "ceb"),
                            ("Chinese (Simplified)", "zh-Hans"),
                            ("Chinese (Traditional)", "zh-Hant"),
                            ("Corsican", "co"), ("Croatian", "hr"),
                            ("Czech", "cs"), ("Danish", "da"),
                            ("Divehi", "dv"), ("Dutch", "nl"),
                            ("English (Original)", "en-orig"),
                            ("English", "en"),
                            ("Esperanto", "eo"), ("Estonian", "et"),
                            ("Ewe", "ee"), ("Filipino", "fil"),
                            ("Finnish", "fi"), ("French", "fr"),
                            ("Galician", "gl"), ("Ganda", "lg"),
                            ("Georgian", "ka"), ("German", "de"),
                            ("Greek", "el"), ("Guarani", "gn"),
                            ("Gujarati", "gu"), ("Haitian Creole", "ht"),
                            ("Hausa", "ha"), ("Hawaiian", "haw"),
                            ("Hebrew", "iw"), ("Hindi", "hi"),
                            ("Hmong", "hmn"), ("Hungarian", "hu"),
                            ("Icelandic", "is"), ("Igbo", "ig"),
                            ("Indonesian", "id"), ("Irish", "ga"),
                            ("Italian", "it"), ("Japanese", "ja"),
                            ("Javanese", "jv"), ("Kannada", "kn"),
                            ("Kazakh", "kk"), ("Khmer", "km"),
                            ("Kinyarwanda", "rw"), ("Korean", "ko"),
                            ("Krio", "kri"), ("Kurdish", "ku"),
                            ("Kyrgyz", "ky"), ("Lao", "lo"),
                            ("Latin", "la"), ("Latvian", "lv"),
                            ("Lingala", "ln"), ("Lithuanian", "lt"),
                            ("Luxembourgish", "lb"), ("Macedonian", "mk"),
                            ("Malagasy", "mg"), ("Malay", "ms"),
                            ("Malayalam", "ml"), ("Maltese", "mt"),
                            ("Māori", "mi"), ("Marathi", "mr"),
                            ("Mongolian", "mn"), ("Nepali", "ne"),
                            ("Northern Sotho", "nso"), ("Norwegian", "no"),
                            ("Nyanja", "ny"), ("Odia", "or"),
                            ("Oromo", "om"), ("Pashto", "ps"),
                            ("Persian", "fa"), ("Polish", "pl"),
                            ("Portuguese", "pt"), ("Punjabi", "pa"),
                            ("Quechua", "qu"), ("Romanian", "ro"),
                            ("Russian", "ru"), ("Samoan", "sm"),
                            ("Sanskrit", "sa"), ("Scottish Gaelic", "gd"),
                            ("Serbian", "sr"), ("Shona", "sn"),
                            ("Sindhi", "sd"), ("Sinhala", "si"),
                            ("Slovak", "sk"), ("Slovenian", "sl"),
                            ("Somali", "so"), ("Southern Sotho", "st"),
                            ("Spanish", "es"), ("Sundanese", "su"),
                            ("Swahili", "sw"), ("Swedish", "sv"),
                            ("Tajik", "tg"), ("Tamil", "ta"),
                            ("Tatar", "tt"), ("Telugu", "te"),
                            ("Thai", "th"), ("Tigrinya", "ti"),
                            ("Tsonga", "ts"), ("Turkish", "tr"),
                            ("Turkmen", "tk"), ("Ukrainian", "uk"),
                            ("Urdu", "ur"), ("Uyghur", "ug"),
                            ("Uzbek", "uz"), ("Vietnamese", "vi"),
                            ("Welsh", "cy"), ("Western Frisian", "fy"),
                            ("Xhosa", "xh"), ("Yiddish", "yi"),
                            ("Yoruba", "yo"), ("Zulu", "zu")]

FORMAT_TYPE_AUDVID_BY_QUA = 0
FORMAT_TYPE_AUD_BY_QUA = 1
FORMAT_TYPE_VID_BY_QUA = 2
FORMAT_TYPE_AUDVID_BY_EXT = 3
FORMAT_TYPE_AUD_BY_EXT = 4
FORMAT_TYPE_VID_BY_EXT = 5
FORMAT_TYPE_AUD_BY_CODEC = 6
FORMAT_TYPE_VID_BY_CODEC = 7
FORMAT_TYPE_MERGE = 8
FORMAT_TYPE_RAWSTRING = 9

FORMAT_TYPE_LIST = [
    ("Audio+Video by quality", FORMAT_TYPE_AUDVID_BY_QUA),
    ("Audio only by quality", FORMAT_TYPE_AUD_BY_QUA),
    ("Video only by quality", FORMAT_TYPE_VID_BY_QUA),
    ("Audio+Video by extension", FORMAT_TYPE_AUDVID_BY_EXT),
    ("Audio only by extension", FORMAT_TYPE_AUD_BY_EXT),
    ("Video only by extension", FORMAT_TYPE_VID_BY_EXT),
    ("Audio only by codec", FORMAT_TYPE_AUD_BY_CODEC),
    ("Video only by codec", FORMAT_TYPE_VID_BY_CODEC),
    ("Merge formats", FORMAT_TYPE_MERGE),
    ("Raw format string", FORMAT_TYPE_RAWSTRING)
]

FORMAT_LABELS_QUALITY_LIST = ["Best quality", "Second best quality",
                              "Third best quality", "Fourth best quality"]

# Output container formats
FORMAT_EXT_LIST = ["3gp", "aac", "flv", "m4a", "mp3", "mp4", "ogg", "wav",
                   "webm"]
FORMAT_EXT_AUD_LIST = ["m4a", "aac", "mp3", "ogg", "opus", "webm"]
FORMAT_EXT_VID_LIST = ["mp4", "mov", "webm", "flv", "3gp"]
# Audio and video Codecs
FORMAT_CODEC_AUD_LIST = ["flac", "alac", "wav", "aiff", "opus", "vorbis",
                         "aac", "mp4a", "mp3", "ac4", "eac3", "ac3", "dts"]
FORMAT_CODEC_VID_LIST = [("av01", "av01"), ("vp9.2", "vp09.2"),
                         ("vp9", "vp09"), ("avc1/h264", "avc1"),
                         ("hevc/h265", "h265"),
                         ("vp8", "vp08"), ("h263", "h263"),
                         ("theora", "theora")]
# Merge options
FORMAT_MERGE_AUD_LIST = [("Best audio", "bestaudio"),
                         ("All audio only", "mergeall[vcodec=none]"),
                         ("Codec flac", "ba[acodec~=flac]"),
                         ("Codec alac", "ba[acodec~=alac]"),
                         ("Codec wav", "ba[acodec~=wav]"),
                         ("Codec aiff", "ba[acodec~=aiff]"),
                         ("Codec opus", "ba[acodec~=opus]"),
                         ("Codec vorbis", "ba[acodec~=vorbis]"),
                         ("Codec aac", "ba[acodec~=aac]"),
                         ("Codec mp4a", "ba[acodec~=mp4a]"),
                         ("Codec mp3", "ba[acodec~=mp3]"),
                         ("Codec ac4", "ba[acodec~=ac4]"),
                         ("Codec eac3", "ba[acodec~=eac3]"),
                         ("Codec ac3", "ba[acodec~=ac3]"),
                         ("Codec dts", "ba[acodec~=dts]"),
                         ("Extension m4a", "be[ext=m4a]"),
                         ("Extension aac", "be[ext=aac]"),
                         ("Extension mp3", "be[ext=mp3]"),
                         ("Extension ogg", "be[ext=ogg]"),
                         ("Extension opus", "be[ext=opus]"),
                         ("Extension webm", "be[ext=webm]")]
FORMAT_MERGE_VID_LIST = [("Best video", "bestvideo"),
                         ("All video only", "mergeall[acodec=none"),
                         ("Codec av01", "bv*[vcodec~=av01]"),
                         ("Codec vp9.2", "bv*[vcodec~=vp09.2]"),
                         ("Codec vp9", "bv*[vcodec~=vp09]"),
                         ("Codec hevc/h265", "bv*[vcodec~=h265]"),
                         ("Codec avc1/h264", "bv*[vcodec~=avc1]"),
                         ("Codec vp8", "bv*[vcodec~=vp08]"),
                         ("Codec h263", "bv*[vcodec~=h263]"),
                         ("Codec theora", "bv*[vcodec~=theora]"),
                         ("Extension mp4", "bv*[ext=mp4]"),
                         ("Extension mov", "bv*[ext=mov]"),
                         ("Extension webm", "bv*[ext=webm]"),
                         ("Extension flv", "bv*[ext=flv]"),
                         ("Extension 3gp", "bv*[ext=3gp]")]

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
    main_layout: QFormLayout
    url_type_combo: QComboBox
    url_stacked_widget: QStackedWidget
    url_text_layout_widget: QWidget
    url_text: QLineEdit
    list_formats_button: QPushButton
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
    downloadsubtitles_check: QCheckBox
    consoleoutput_check: QCheckBox
    subtitles_layout: QHBoxLayout
    subtitles_generated: QCheckBox
    subtitles_format_combo: QComboBox
    subtitles_languages_combo: QComboBox
    subtitles_delay_spin: QSpinBox
    list_subtitles_button: QPushButton
    format_stacked_widget: QStackedWidget
    format_type_combo: QComboBox
    format_quality_combo: QComboBox
    format_audext_combo: QComboBox
    format_vidext_combo: QComboBox
    format_audcodec_combo: QComboBox
    format_vidcodec_combo: QComboBox
    format_merge_layout_widget: QWidget
    format_merge_audio_combo: QComboBox
    format_merge_video_combo: QComboBox
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

        # Possibly hide subtitles row
        visible = self.downloadsubtitles_check.isChecked()
        self.main_layout.setRowVisible(self.subtitles_layout, visible)

    def create_mainwindow_widgets(self):
        """Create widgets for window
        """
        self.url_stacked_widget = QStackedWidget()
        self.url_type_combo = QComboBox()
        self.url_text_layout_widget = QWidget()
        self.url_text = QLineEdit()
        self.list_formats_button = QPushButton("List formats")
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
        self.downloadsubtitles_check = QCheckBox("Download subtitles")
        self.consoleoutput_check = QCheckBox("Console output")
        self.subtitles_generated = QCheckBox("Auto-generated subtitles")
        self.subtitles_format_combo = QComboBox()
        self.subtitles_languages_combo = QComboBox()
        self.subtitles_delay_spin = QSpinBox()
        self.list_subtitles_button = QPushButton("List subtitles")
        self.subtitles_layout = QHBoxLayout()
        self.format_stacked_widget = QStackedWidget()
        self.format_type_combo = QComboBox()
        self.format_quality_combo = QComboBox()
        self.format_audext_combo = QComboBox()
        self.format_vidext_combo = QComboBox()
        self.format_audcodec_combo = QComboBox()
        self.format_vidcodec_combo = QComboBox()
        self.format_merge_layout_widget = QWidget()
        self.format_merge_audio_combo = QComboBox()
        self.format_merge_video_combo = QComboBox()
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

        # Prevent QStackedWidgets from expanding vertically
        self.url_stacked_widget.setSizePolicy(QSizePolicy.Policy.Expanding,
                                              QSizePolicy.Policy.Fixed)
        self.format_stacked_widget.setSizePolicy(QSizePolicy.Policy.Expanding,
                                                 QSizePolicy.Policy.Fixed)
        # Prevent various other widgets from expanding (some of these don't
        # work)
        widgets = [self.subtitles_format_combo, self.subtitles_languages_combo,
                   self.list_subtitles_button, self.format_type_combo,
                   self.format_quality_combo, self.format_audext_combo,
                   self.format_vidext_combo, self.format_audcodec_combo,
                   self.format_vidcodec_combo, self.format_merge_audio_combo,
                   self.format_merge_video_combo, self.subtitles_delay_spin]
        for widget in widgets:
            widget.setSizePolicy(QSizePolicy.Policy.Fixed,
                                 QSizePolicy.Policy.Fixed)
        # Set status QTextEdit to read only for status logs
        self.status_text.setReadOnly(True)
        # Set status to fix font family
        font = QFont(MONOSPACE_FONT_NAME)
        font.setStyleHint(QFont.StyleHint.TypeWriter)
        font.setWeight(QFont.Weight.Black)
        self.status_text.setFont(font)
        # Set status window to not wrap text
        self.status_text.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        # Set to accept rich text
        self.status_text.setAcceptRichText(True)

        # Populate subtitles combo boxes
        for label, built_in in SUBTITLES_FORMAT_LIST:
            self.subtitles_format_combo.addItem(label, built_in)
        self.subtitles_languages_combo.addItem("All languages", "all")
        for lang, lang_code in SUBTITLES_LANGUAGES_LIST:
            self.subtitles_languages_combo.addItem(lang, lang_code)

        # Populate format selection combo boxes
        for label, idx in FORMAT_TYPE_LIST:
            self.format_type_combo.addItem(label, idx)
        for idx, label in enumerate(FORMAT_LABELS_QUALITY_LIST):
            self.format_quality_combo.addItem(label, "." + str(idx + 1))
        for ext in FORMAT_EXT_AUD_LIST:
            self.format_audext_combo.addItem(ext, ext)
        for ext in FORMAT_EXT_VID_LIST:
            self.format_vidext_combo.addItem(ext, ext)
        for codec in FORMAT_CODEC_AUD_LIST:
            self.format_audcodec_combo.addItem(codec, codec)
        for label, codec in FORMAT_CODEC_VID_LIST:
            self.format_vidcodec_combo.addItem(label, codec)
        for label, fstr in FORMAT_MERGE_AUD_LIST:
            self.format_merge_audio_combo.addItem(label, fstr)
        for label, fstr in FORMAT_MERGE_VID_LIST:
            self.format_merge_video_combo.addItem(label, fstr)

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

        url_layout = QHBoxLayout(self.url_text_layout_widget)
        url_layout.addWidget(self.url_text)
        url_layout.addWidget(self.list_formats_button)
        list_path_layout = QHBoxLayout(self.list_path_layout_widget)
        list_path_layout.addWidget(self.list_path_text)
        list_path_layout.addWidget(self.list_path_browse_button, 0,
                                   Qt.AlignmentFlag.AlignRight)
        self.url_stacked_widget.addWidget(self.url_text_layout_widget)
        self.url_stacked_widget.addWidget(self.list_path_layout_widget)
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
        # switches_layout.addWidget(self.downloadsubtitles_check)
        switches_layout.addWidget(self.consoleoutput_check)
        self.subtitles_layout = QHBoxLayout()
        self.subtitles_layout.addWidget(self.subtitles_generated)
        self.subtitles_layout.addWidget(QLabel("Format:",
                                        alignment=Qt.AlignmentFlag.AlignRight))
        self.subtitles_layout.addWidget(self.subtitles_format_combo)
        self.subtitles_layout.addWidget(QLabel("Language:",
                                        alignment=Qt.AlignmentFlag.AlignRight))
        self.subtitles_layout.addWidget(self.subtitles_languages_combo)
        self.subtitles_layout.addWidget(QLabel("Delay:",
                                        alignment=Qt.AlignmentFlag.AlignRight))
        self.subtitles_layout.addWidget(self.subtitles_delay_spin)
        self.subtitles_layout.addWidget(self.list_subtitles_button)
        format_string_layout = QHBoxLayout(
            self.format_string_layout_widget)
        format_string_layout.addWidget(QLabel("Format string:"))
        format_string_layout.addWidget(self.format_string_text)
        format_string_layout.addWidget(self.format_string_help_button, 0,
                                       Qt.AlignmentFlag.AlignRight)
        format_merge_layout = QHBoxLayout(
            self.format_merge_layout_widget)
        format_merge_layout.addWidget(QLabel("Audio:"),
                                      alignment=Qt.AlignmentFlag.AlignRight)
        format_merge_layout.addWidget(self.format_merge_audio_combo)
        format_merge_layout.addWidget(QLabel("Video:"),
                                      alignment=Qt.AlignmentFlag.AlignRight)
        format_merge_layout.addWidget(self.format_merge_video_combo)
        self.format_stacked_widget.addWidget(self.format_quality_combo)
        self.format_stacked_widget.addWidget(self.format_audext_combo)
        self.format_stacked_widget.addWidget(self.format_vidext_combo)
        self.format_stacked_widget.addWidget(self.format_audcodec_combo)
        self.format_stacked_widget.addWidget(self.format_vidcodec_combo)
        self.format_stacked_widget.addWidget(self.format_merge_layout_widget)
        self.format_stacked_widget.addWidget(self.format_string_layout_widget)
        format_type_layout = QHBoxLayout()
        format_type_layout.addWidget(self.format_type_combo)
        format_type_layout.addWidget(self.format_stacked_widget)

        # By default the layout is too tall for the QStackedWidget
        url_layout.setContentsMargins(0, 0, 0, 0)
        list_path_layout.setContentsMargins(0, 0, 0, 0)
        format_string_layout.setContentsMargins(0, 0, 0, 0)
        format_merge_layout.setContentsMargins(0, 0, 0, 0)

        # Use Form Layout for window
        self.main_layout = QFormLayout()

        # Add widgets to window layout
        self.main_layout.addRow(self.url_type_combo, self.url_stacked_widget)
        self.main_layout.addRow("Download path:", download_path_layout)
        self.main_layout.addRow("FFMPEG path:", ffmpeg_layout)
        self.main_layout.addRow("Authentication:", auth_layout)
        self.main_layout.addRow("Switches:", switches_layout)
        self.main_layout.addRow("Subtitles:", self.subtitles_layout)
        self.main_layout.addRow("Format selection:", format_type_layout)
        self.main_layout.addRow(self.status_text)
        self.main_layout.addRow("File progress", self.file_progress)
        self.main_layout.addRow("Total progress", self.total_progress)
        self.main_layout.addRow(QLabel(""))
        self.main_layout.addRow(self.bottom_buttonbox)

        return self.main_layout

    def connect_mainwindow_signals(self):
        """Connects main window signals to slots
        """
        self.url_type_combo.currentIndexChanged.connect(
            self.url_stacked_widget.setCurrentIndex)
        self.list_formats_button.clicked.connect(
            self.list_formats_button_clicked)
        self.list_path_browse_button.clicked.connect(
            self.list_browse_button_clicked)
        self.download_path_browse_button.clicked.connect(
            self.download_browse_button_clicked)
        self.ffmpeg_path_browse_button.clicked.connect(
            self.ffmpeg_browse_button_clicked)
        self.downloadsubtitles_check.checkStateChanged.connect(
            lambda checked: self.main_layout.setRowVisible(
                self.subtitles_layout, checked == Qt.CheckState.Checked))
        self.list_subtitles_button.clicked.connect(
            lambda: self.download_subtitle_formats(self.url_text.text()))
        self.format_type_combo.currentIndexChanged.connect(
            self.format_type_combo_changed)
        self.format_string_help_button.clicked.connect(
            lambda: QDesktopServices.openUrl(FORMAT_STRING_HELP_URL))
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
        self.list_formats_button.setToolTip(
            "Retrieve the list of video and audio formats available for "
            "this URL.")
        self.list_path_text.setToolTip(
            "The path to the list of URLs to download")
        self.list_path_browse_button.setToolTip(
            "Use dialog to browse to URL list path")
        self.download_path_text.setToolTip(
            "The path to the directory to download videos to")
        self.download_path_browse_button.setToolTip(
            "Use dialog to browse to download directory")
        self.ffmpeg_path_text.setToolTip(
            "Path to directory containing ffmpeg and ffprobe binaries. "
            "ffmpeg is only required if you select format options that "
            "require post processing.")
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
        self.downloadsubtitles_check.setToolTip(
            "Download subtitles with video. More options will be revealed "
            "when checked.")
        self.consoleoutput_check.setToolTip(
            "The yt_dlp library will output to the console that launched this "
            "program. Useful for debugging.")
        self.subtitles_generated.setToolTip(
            "Download auto-generated caption text. If unchecked, actual "
            "subtitles will be downloaded.")
        self.subtitles_format_combo.setToolTip(
            "The destination subtitle format. Some formats will be converted.")
        self.subtitles_languages_combo.setToolTip(
            "The languages of subtitles to download. The languages must be "
            "available from the server.")
        self.subtitles_delay_spin.setToolTip(
            "The delay in seconds between subtitle retrieval. If too many "
            "download requests happen too quickly, some sites will abort the "
            "activity.")
        self.list_subtitles_button.setToolTip(
            "Attempt to retrieve a list of available subtitles from the "
            "server.")
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
        self.format_merge_audio_combo.setToolTip(
            "The audio format or formats to be combined into the output file. "
            "ffmpeg is required.")
        self.format_merge_video_combo.setToolTip(
            "The video format or formats to be combined into the output file. "
            "ffmpeg is required.")
        self.format_string_text.setToolTip(
            "Enter the string representing the format to download. Click "
            "the Help button for more information.")
        self.format_string_help_button.setToolTip(
            "Launches a browser directed to detailed information about "
            "creating yt-dlp format strings.")
        self.status_text.setToolTip(
            "This window shows status text. You can pinch and zoom the text "
            "in this window or hold ctrl and use the mouse wheel to change "
            "the zoom factor, and copy text by dragging and then pressing "
            "ctrl-c.")
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
        self.downloadsubtitles_check.setChecked(self.value_to_bool(
            self.settings.value(SETTINGS_VAL_DOWNLOADSUBTITLES)))
        self.subtitles_generated.setChecked(self.value_to_bool(
            self.settings.value(SETTINGS_VAL_SUBTITLESGENERATED)))
        self.subtitles_format_combo.setCurrentText(
            self.settings.value(SETTINGS_VAL_SUBTITLEFORMAT))
        self.subtitles_languages_combo.setCurrentText(
            self.settings.value(SETTINGS_VAL_SUBTITLELANGUAGE))
        self.subtitles_delay_spin.setValue(
            self.settings.value(SETTINGS_VAL_SUBTITLEDELAY, 0))
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
        self.format_merge_audio_combo.setCurrentText(
            self.settings.value(SETTINGS_VAL_FORMATMERGEAUD, ""))
        self.format_merge_video_combo.setCurrentText(
            self.settings.value(SETTINGS_VAL_FORMATMERGEVID, ""))
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
        self.settings.setValue(SETTINGS_VAL_DOWNLOADSUBTITLES,
                               self.downloadsubtitles_check.isChecked())
        self.settings.setValue(SETTINGS_VAL_CONSOLEOUTPUT,
                               self.consoleoutput_check.isChecked())
        self.settings.setValue(SETTINGS_VAL_SUBTITLESGENERATED,
                               self.subtitles_generated.isChecked())
        self.settings.setValue(SETTINGS_VAL_SUBTITLEFORMAT,
                               self.subtitles_format_combo.currentText())
        self.settings.setValue(SETTINGS_VAL_SUBTITLELANGUAGE,
                               self.subtitles_languages_combo.currentText())
        self.settings.setValue(SETTINGS_VAL_SUBTITLEDELAY,
                               self.subtitles_delay_spin.value())
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
        self.settings.setValue(SETTINGS_VAL_FORMATMERGEAUD,
                               self.format_merge_audio_combo.currentText())
        self.settings.setValue(SETTINGS_VAL_FORMATMERGEVID,
                               self.format_merge_video_combo.currentText())
        self.settings.setValue(SETTINGS_VAL_FORMATSTRING,
                               self.format_string_text.text())
        self.settings.setValue(SETTINGS_VAL_WINDOWWIDTH,
                               self.width())
        self.settings.setValue(SETTINGS_VAL_WINDOWHEIGHT,
                               self.height())

    def list_formats_button_clicked(self):
        """Called when list formats button is clicked
        """
        url = self.url_text.text()
        if not url:
            QMessageBox.warning(self, "Missing download URL",
                                "Enter a valid URL for format listing",
                                QMessageBox.StandardButton.Ok)
            return
        self.download_url_formats(url)

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
            self.format_stacked_widget.setCurrentWidget(
                self.format_quality_combo)
        elif type_id == FORMAT_TYPE_AUD_BY_EXT:
            self.format_stacked_widget.setCurrentWidget(
                self.format_audext_combo)
        elif type_id in [FORMAT_TYPE_VID_BY_EXT, FORMAT_TYPE_AUDVID_BY_EXT]:
            self.format_stacked_widget.setCurrentWidget(
                self.format_vidext_combo)
        elif type_id == FORMAT_TYPE_AUD_BY_CODEC:
            self.format_stacked_widget.setCurrentWidget(
                self.format_audcodec_combo)
        elif type_id == FORMAT_TYPE_VID_BY_CODEC:
            self.format_stacked_widget.setCurrentWidget(
                self.format_vidcodec_combo)
        elif type_id == FORMAT_TYPE_MERGE:
            self.format_stacked_widget.setCurrentWidget(
                self.format_merge_layout_widget)
        elif type_id == FORMAT_TYPE_RAWSTRING:
            self.format_stacked_widget.setCurrentWidget(
                self.format_string_layout_widget)

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

    def create_ydl_quiet_options(self):
        """Returns a YouTubeDL Options map preset to quiet settings

        Returns:
            {}: Options map
        """
        ydl_opts = {}
        if self.consoleoutput_check.isChecked():
            ydl_opts["quiet"] = False
            ydl_opts["verbose"] = True
            ydl_opts["no_warnings"] = False
        else:
            ydl_opts["quiet"] = True
            ydl_opts["verbose"] = False
            ydl_opts["no_warnings"] = True
        ydl_opts["noprogress"] = True
        return ydl_opts

    def create_ydl_download_options(self):
        """Creates the dictionary of options to pass to yt_dlp.YoutubeDL
        built from UI values and set some default values

        Returns:
            dict: Dictionary of options for yt_dlp.YoutubeDL constructor
        """
        # Set options for yt_dlp.YoutubeDL
        ydl_opts = self.create_ydl_quiet_options()
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
        if self.downloadsubtitles_check.isChecked():
            if self.subtitles_generated.isChecked():
                ydl_opts["writeautomaticsub"] = True
            else:
                ydl_opts["writesubtitles"] = True
            subs_format = self.subtitles_format_combo.currentText()
            if self.subtitles_format_combo.currentData():
                ydl_opts["subtitlesformat"] = subs_format
            else:
                ydl_opts["convertsubtitles"] = subs_format
            subs_language = self.subtitles_languages_combo.currentData()
            ydl_opts["subtitleslangs"] = [subs_language]
            sleep_interval = self.subtitles_delay_spin.value()
            ydl_opts["sleep_interval_subtitles"] = sleep_interval

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
            format_str = f"bestaudio[acodec^={codec}]"
        elif type_id == FORMAT_TYPE_VID_BY_CODEC:
            codec = self.format_vidcodec_combo.currentData()
            format_str = f"bestvideo[vcodec^={codec}]"
        elif type_id == FORMAT_TYPE_MERGE:
            audtype = self.format_merge_audio_combo.currentData()
            vidtype = self.format_merge_video_combo.currentData()
            format_str = f"{audtype}+{vidtype}"
            ydl_opts["allow_multiple_audio_streams"] = True
            ydl_opts["allow_multiple_video_streams"] = True
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
        ydl_opts = self.create_ydl_download_options()

        # Perform downloads
        with YoutubeDL(ydl_opts) as ydl:
            self.file_progress.setValue(0)
            ydl.add_progress_hook(self.ydl_download_progress_hook)
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

    def ydl_download_progress_hook(self, progress_dict):
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
            if file_bytes is not None and file_total:
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

    def table_add_row(self, table, fields, header=False):
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

    def table_create(self, name, headers):
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
        self.table_add_row(table, [name], True)
        table.appendRows(1)
        self.table_add_row(table, headers, True)
        return text_doc, table

    def download_url_formats(self, url):
        """Download and display the formats avilable at url

        Args:
            url (str): URL to download format list from
        """

        message = f"Trying to retrieve format list for URL {url}"
        self.add_status_message(message)

        # Disable widgets that would interfere with processing
        self.enable_active_buttons(False)

        ydl_opts = self.create_ydl_quiet_options()
        ydl_opts["simulate"] = True

        # Perform data retrieval
        with YoutubeDL(ydl_opts) as ydl:
            try:
                meta = ydl.extract_info(url, download=False)
                format_list = meta.get('formats', [meta])
            except utils.DownloadError as e:
                error_message = str(e)
                message = f"Download error: {error_message}"
                self.add_status_message(message)
                # Reenable widgets that would interfere with processing
                self.enable_active_buttons(True)
                return

            headers = ["ID", "Extension", "Audio codec", "Video codec",
                       "Resolution", "Bitrate", "Size", "Note"]
            text_doc, table = self.table_create("File formats", headers)

            for fmt in format_list:
                # Tupple is key, is_numeric, suffix
                keys = [("format_id", False, ""),
                        ("ext", False, ""),
                        ("acodec", False, ""),
                        ("vcodec", False, ""),
                        ("resolution", False, ""),
                        ("tbr", True, " K/s"),
                        ("filesize", True, " bytes"),
                        ("format_note", False, "")]
                fields = []
                for key, is_numeric, suffix in keys:
                    text = ""
                    if key in fmt and fmt[key]:
                        if is_numeric:
                            text = format(fmt[key], ',')
                        else:
                            text = fmt[key]
                        text += suffix
                    fields.append(text)
                # Add fields to table
                self.table_add_row(table, fields)
            # Add table to status window
            self.status_text.append(text_doc.toHtml())

        # Reenable widgets that would interfere with processing
        self.enable_active_buttons(True)

    def download_subtitle_formats(self, url):
        """Downloads and displays subtitles available from url

        Args:
            url (str): URL of video
        """
        message = f"Trying to retrieve subtitle list for URL {url}"
        self.add_status_message(message)

        ydl_opts = self.create_ydl_quiet_options()
        ydl_opts["simulate"] = True

        with YoutubeDL(ydl_opts) as ydl:
            try:
                meta = ydl.extract_info(url, download=False)
            except utils.DownloadError as e:
                error_message = str(e)
                message = f"Download error: {error_message}"
                self.add_status_message(message)
                return

            def parse_subs(self, key, name):
                if key not in meta or not isinstance(meta[key],
                                                     dict):
                    self.add_status_message("This video seems to contain no "
                                            "{name}.")
                else:
                    subtitles_list = meta[key]
                    headers = ["Code", "Name", "Format"]
                    text_doc, table = self.table_create(name, headers)
                    for key, value in subtitles_list.items():
                        for sub in value:
                            fields = []
                            fields.append(key)
                            fields.append(sub["name"] if "name" in sub else "")
                            fields.append(sub["ext"] if "ext" in sub else "")
                            self.table_add_row(table, fields)
                    # Add table to status window
                    self.status_text.append(text_doc.toHtml())

            parse_subs(self, "automatic_captions", "Auto-generated captions")
            parse_subs(self, "subtitles", "Subtitles")

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
        self.list_formats_button.setEnabled(enable)
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
