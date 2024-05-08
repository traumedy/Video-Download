#!/usr/bin/env python3

"""video_download.py - Download videos or lists of videos
including bookmarks exported from browsers from video sites
like YouTube, Vimeo, Instagram, etc using the yt_dlp Python package.

Author: Josh Buchbinder
"""

__author__ = "Josh Buchbinder"
__copyright__ = "Copyright 2024, Josh Buchbinder"
__version__ = "0.1.0"

import sys
import shutil
import re
from overrides import override
from PySide6.QtCore import Qt, QFileInfo, QDir, QUrl, QSettings
from PySide6.QtGui import QDesktopServices, QFont, QBrush, QColor
from PySide6.QtGui import QTextDocument, QTextTable, QTextTableFormat
from PySide6.QtGui import QTextTableCell, QTextCursor
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox
from PySide6.QtWidgets import QFormLayout, QHBoxLayout, QTextEdit
from PySide6.QtWidgets import QLineEdit, QPushButton, QLabel, QFileDialog
from PySide6.QtWidgets import QProgressBar, QDialogButtonBox, QSpinBox
from PySide6.QtWidgets import QCheckBox, QComboBox, QStyle
from PySide6.QtWidgets import QSizePolicy, QStackedWidget
from yt_dlp import YoutubeDL, utils

from constants import AppConst, SettingsConst, ComboBoxConst, ToolTips
from bookmark_html_parser import BookmarkHTMLParser
from utils import table_add_row, table_create


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
    downloadsubs_check: QCheckBox
    consoleoutput_check: QCheckBox
    subtitles_layout: QHBoxLayout
    generatedsubs_check: QCheckBox
    subs_lang_combo: QComboBox
    subs_format_combo: QComboBox
    subs_delay_spin: QSpinBox
    list_subs_button: QPushButton
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
        self.settings = QSettings(SettingsConst.SETTINGS_COMPANYNAME,
                                  SettingsConst.SETTINGS_APPNAME)
        # Used to store downloaded filenames from progress hook callback
        self.download_filenames = []

        # Set minimum window size
        size = self.size()
        self.setMinimumSize(size)

        # Load persistent settings including stored window size
        self.load_settings()

        # Possibly hide subtitles row
        visible = self.downloadsubs_check.isChecked()
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
        self.downloadsubs_check = QCheckBox("Download subtitles")
        self.consoleoutput_check = QCheckBox("Console output")
        self.generatedsubs_check = QCheckBox("Auto-generated subtitles")
        self.subs_lang_combo = QComboBox()
        self.subs_format_combo = QComboBox()
        self.subs_delay_spin = QSpinBox()
        self.list_subs_button = QPushButton("List subtitles")
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
        for label in ComboBoxConst.URL_TYPE_LABELS:
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
        widgets = [self.subs_lang_combo, self.subs_format_combo,
                   self.list_subs_button, self.format_type_combo,
                   self.format_quality_combo, self.format_audext_combo,
                   self.format_vidext_combo, self.format_audcodec_combo,
                   self.format_vidcodec_combo, self.format_merge_audio_combo,
                   self.format_merge_video_combo, self.subs_delay_spin]
        for widget in widgets:
            widget.setSizePolicy(QSizePolicy.Policy.Fixed,
                                 QSizePolicy.Policy.Fixed)
        # Set status QTextEdit to read only for status logs
        self.status_text.setReadOnly(True)
        # Set status to fix font family
        font = QFont(AppConst.MONOSPACE_FONT_NAME)
        font.setStyleHint(QFont.StyleHint.TypeWriter)
        font.setWeight(QFont.Weight.Black)
        self.status_text.setFont(font)
        # Set status window to not wrap text
        self.status_text.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        # Set to accept rich text
        self.status_text.setAcceptRichText(True)

        # Populate subtitles combo boxes
        for lang, lang_code in ComboBoxConst.SUBTITLES_LANGUAGES_LIST:
            self.subs_lang_combo.addItem(lang, lang_code)
        for label, built_in in ComboBoxConst.SUBTITLES_FORMAT_LIST:
            self.subs_format_combo.addItem(label, built_in)

        # Populate format selection combo boxes
        for label, idx in ComboBoxConst.FORMAT_TYPE_LIST:
            self.format_type_combo.addItem(label, idx)
        for idx, label in enumerate(ComboBoxConst.FORMAT_LABELS_QUALITY_LIST):
            self.format_quality_combo.addItem(label, "." + str(idx + 1))
        for ext in ComboBoxConst.FORMAT_EXT_AUD_LIST:
            self.format_audext_combo.addItem(ext, ext)
        for ext in ComboBoxConst.FORMAT_EXT_VID_LIST:
            self.format_vidext_combo.addItem(ext, ext)
        for codec in ComboBoxConst.FORMAT_CODEC_AUD_LIST:
            self.format_audcodec_combo.addItem(codec, codec)
        for label, codec in ComboBoxConst.FORMAT_CODEC_VID_LIST:
            self.format_vidcodec_combo.addItem(label, codec)
        for label, fstr in ComboBoxConst.FORMAT_MERGE_AUD_LIST:
            self.format_merge_audio_combo.addItem(label, fstr)
        for label, fstr in ComboBoxConst.FORMAT_MERGE_VID_LIST:
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
        # switches_layout.addWidget(self.downloadsubs_check)
        switches_layout.addWidget(self.consoleoutput_check)
        self.subtitles_layout = QHBoxLayout()
        self.subtitles_layout.addWidget(self.generatedsubs_check)
        self.subtitles_layout.addWidget(QLabel("Language:",
                                        alignment=Qt.AlignmentFlag.AlignRight))
        self.subtitles_layout.addWidget(self.subs_lang_combo)
        self.subtitles_layout.addWidget(QLabel("Format:",
                                        alignment=Qt.AlignmentFlag.AlignRight))
        self.subtitles_layout.addWidget(self.subs_format_combo)
        self.subtitles_layout.addWidget(QLabel("Delay:",
                                        alignment=Qt.AlignmentFlag.AlignRight))
        self.subtitles_layout.addWidget(self.subs_delay_spin)
        self.subtitles_layout.addWidget(self.list_subs_button)
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
        self.downloadsubs_check.checkStateChanged.connect(
            lambda checked: self.main_layout.setRowVisible(
                self.subtitles_layout, checked == Qt.CheckState.Checked))
        self.list_subs_button.clicked.connect(
            lambda: self.download_subtitle_formats(self.url_text.text()))
        self.format_type_combo.currentIndexChanged.connect(
            self.format_type_combo_changed)
        self.format_string_help_button.clicked.connect(
            lambda: QDesktopServices.openUrl(AppConst.FORMAT_STRING_HELP_URL))
        self.close_button.clicked.connect(
            self.close)
        self.download_button.clicked.connect(
            self.download_button_clicked)

    def create_mainwindow_tooltips(self):
        """Sets tooltips for main window widgets
        """
        # Set widget tooltips
        self.url_type_combo.setToolTip(ToolTips.TTT_URL_TYPE_COMBO)
        self.url_text.setToolTip(ToolTips.TTT_URL_TEXT)
        self.list_formats_button.setToolTip(ToolTips.TTT_LIST_PATH_TEXT)
        self.list_path_text.setToolTip(ToolTips.TTT_LIST_PATH_TEXT)
        self.list_path_browse_button.setToolTip(
            ToolTips.TTT_LIST_PATH_BROSE_BUTTON)
        self.download_path_text.setToolTip(ToolTips.TTT_DOWNLOAD_PATH_TEXT)
        self.download_path_browse_button.setToolTip(
            ToolTips.TTT_DOWNLOAD_PATH_BROWSE_BUTTON)
        self.ffmpeg_path_text.setToolTip(ToolTips.TTT_FFMPEG_PATH_TEXT)
        self.ffmpeg_path_browse_button.setToolTip(
            ToolTips.TTT_FFMPEG_PATH_BROWSE_BUTTON)
        self.username_text.setToolTip(ToolTips.TTT_USERNAME_TEXT)
        self.password_text.setToolTip(ToolTips.TTT_PASSWORD_TEXT)
        self.overwrite_check.setToolTip(ToolTips.TTT_OVERWRITE_CHECK)
        self.keepvideo_check.setToolTip(ToolTips.TTT_KEEPVIDEO_CHECK)
        self.preferfreeformats_check.setToolTip(
            ToolTips.TTT_PREFERFREEFORMATS_CHECK)
        self.downloadsubs_check.setToolTip(ToolTips.TTT_DOWNLOADSUBS_CHECK)
        self.consoleoutput_check.setToolTip(ToolTips.TTT_CONSOLEOUTPUT_CHECK)
        self.generatedsubs_check.setToolTip(ToolTips.TTT_GENERATEDSUBS_CHECK)
        self.subs_lang_combo.setToolTip(ToolTips.TTT_SUBS_LANG_COMBO)
        self.subs_format_combo.setToolTip(ToolTips.TTT_SUBS_FORMAT_COMBO)
        self.subs_delay_spin.setToolTip(ToolTips.TTT_SUBS_DELAY_SPIN)
        self.list_subs_button.setToolTip(ToolTips.TTT_LIST_SUBS_BUTTON)
        self.format_type_combo.setToolTip(ToolTips.TTT_FORMAT_TYPE_COMBO)
        self.format_quality_combo.setToolTip(ToolTips.TTT_FORMAT_QUALITY_COMBO)
        self.format_audext_combo.setToolTip(ToolTips.TTT_FORMAT_AUDEXT_COMBO)
        self.format_vidext_combo.setToolTip(ToolTips.TTT_FORMAT_VIDEXT_COMBO)
        self.format_audcodec_combo.setToolTip(
            ToolTips.TTT_FORMAT_AUDCODEC_COMBO)
        self.format_vidcodec_combo.setToolTip(
            ToolTips.TTT_FORMAT_VIDCODEC_COMBO)
        self.format_merge_audio_combo.setToolTip(
            ToolTips.TTT_FORMAT_MERGE_AUDIO_COMBO)
        self.format_merge_video_combo.setToolTip(
            ToolTips.TTT_FORMAT_MERGE_VIDIO_COMBO)
        self.format_string_text.setToolTip(ToolTips.TTT_FORMAT_STRING_TEXT)
        self.format_string_help_button.setToolTip(
            ToolTips.TTT_FORMAT_STRING_HELP_BUTTON)
        self.status_text.setToolTip(ToolTips.TTT_STATUS_TEXT)
        self.close_button.setToolTip(ToolTips.TTT_CLOSE_BUTTON)
        self.download_button.setToolTip(ToolTips.TTT_DOWNLOAD_BUTTON)

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
            if suffix in AppConst.URLLIST_EXTENSIONS:
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

    def get_settings_widgets(self):
        """Returns list of widgets and their associated settings key string
            and their default values

        Returns:
            [(QWidget, str)]: [(Widget, settings key, default)]
        """
        # Default to ffmpeg in path
        ffmpeg_path = shutil.which("ffmpeg")
        if ffmpeg_path:
            # If ffmpeg found
            ffmpeg_info = QFileInfo(ffmpeg_path)
            ffmpeg_path = ffmpeg_info.dir().path()
        else:
            # ffmpeg executable not found in path
            ffmpeg_path = ""

        return [
            (self.url_type_combo, SettingsConst.SETTINGS_VAL_URLTYPE, ""),
            (self.url_text, SettingsConst.SETTINGS_VAL_URLTEXT, ""),
            (self.list_path_text, SettingsConst.SETTINGS_VAL_URLLIST, ""),
            (self.download_path_text,
                SettingsConst.SETTINGS_VAL_DOWNLOADPATH, ""),
            (self.ffmpeg_path_text,
                SettingsConst.SETTINGS_VAL_FFMPEGPATH, ffmpeg_path),
            (self.username_text, SettingsConst.SETTINGS_VAL_USERNAME, ""),
            (self.password_text, SettingsConst.SETTINGS_VAL_PASSWORD, ""),
            (self.overwrite_check, SettingsConst.SETTINGS_VAL_OVERWRITE, ""),
            (self.keepvideo_check, SettingsConst.SETTINGS_VAL_KEEPVIDEO, ""),
            (self.preferfreeformats_check,
                SettingsConst.SETTINGS_VAL_PREFERFREEFORMATS, ""),
            (self.downloadsubs_check,
                SettingsConst.SETTINGS_VAL_DOWNLOADSUBTITLES, ""),
            (self.consoleoutput_check,
                SettingsConst.SETTINGS_VAL_CONSOLEOUTPUT, ""),
            (self.generatedsubs_check,
                SettingsConst.SETTINGS_VAL_AUTOGENSUBS, ""),
            (self.subs_lang_combo,
                SettingsConst.SETTINGS_VAL_SUBTITLELANGUAGE, ""),
            (self.subs_format_combo,
                SettingsConst.SETTINGS_VAL_SUBTITLEFORMAT, ""),
            (self.subs_delay_spin,
                SettingsConst.SETTINGS_VAL_SUBTITLEDELAY, 0),
            (self.format_type_combo,
                SettingsConst.SETTINGS_VAL_FORMATTYPE, ""),
            (self.format_quality_combo,
                SettingsConst.SETTINGS_VAL_FORMATQUALITY, ""),
            (self.format_audext_combo,
                SettingsConst.SETTINGS_VAL_FORMATAUDEXT, ""),
            (self.format_vidext_combo,
                SettingsConst.SETTINGS_VAL_FORMATVIDEXT, ""),
            (self.format_audcodec_combo,
                SettingsConst.SETTINGS_VAL_FORMATAUDCODEC, ""),
            (self.format_vidcodec_combo,
                SettingsConst.SETTINGS_VAL_FORMATVIDCODEC, ""),
            (self.format_merge_audio_combo,
                SettingsConst.SETTINGS_VAL_FORMATMERGEAUD, ""),
            (self.format_merge_video_combo,
                SettingsConst.SETTINGS_VAL_FORMATMERGEVID, ""),
            (self.format_string_text,
                SettingsConst.SETTINGS_VAL_FORMATSTRING, "")]

    def load_settings(self):
        """Loads persistent settings
        """
        widgets = self.get_settings_widgets()
        for widget, settings_key, default in widgets:
            if isinstance(widget, QLineEdit):
                widget.setText(self.settings.value(settings_key, default))
            elif isinstance(widget, QComboBox):
                widget.setCurrentText(self.settings.value(settings_key,
                                                          default))
            elif isinstance(widget, QCheckBox):
                widget.setChecked(self.value_to_bool(
                                  self.settings.value(settings_key)))
            elif isinstance(widget, QSpinBox):
                widget.setValue(self.settings.value(settings_key,
                                                    default))
        # Restore widow size
        size = self.size()
        width = int(self.settings.value(SettingsConst.SETTINGS_VAL_WINDOWWIDTH,
                                        size.width()))
        height = int(self.settings.value(
            SettingsConst.SETTINGS_VAL_WINDOWHEIGHT, size.height()))
        self.resize(width, height)

    def save_settings(self):
        """Save persistent settingss
        """
        widgets = self.get_settings_widgets()
        for widget, settings_key, _ in widgets:
            if isinstance(widget, QLineEdit):
                self.settings.setValue(settings_key, widget.text())
            elif isinstance(widget, QComboBox):
                self.settings.setValue(settings_key, widget.currentText())
            elif isinstance(widget, QCheckBox):
                self.settings.setValue(settings_key, widget.isChecked())
            elif isinstance(widget, QSpinBox):
                self.settings.setValue(settings_key, widget.value())
        # Save size of main window
        self.settings.setValue(SettingsConst.SETTINGS_VAL_WINDOWWIDTH,
                               self.width())
        self.settings.setValue(SettingsConst.SETTINGS_VAL_WINDOWHEIGHT,
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
        if type_id in [ComboBoxConst.FORMAT_TYPE_AUDVID_BY_QUA,
                       ComboBoxConst.FORMAT_TYPE_AUD_BY_QUA,
                       ComboBoxConst.FORMAT_TYPE_VID_BY_QUA]:
            self.format_stacked_widget.setCurrentWidget(
                self.format_quality_combo)
        elif type_id == ComboBoxConst.FORMAT_TYPE_AUD_BY_EXT:
            self.format_stacked_widget.setCurrentWidget(
                self.format_audext_combo)
        elif type_id in [ComboBoxConst.FORMAT_TYPE_VID_BY_EXT,
                         ComboBoxConst.FORMAT_TYPE_AUDVID_BY_EXT]:
            self.format_stacked_widget.setCurrentWidget(
                self.format_vidext_combo)
        elif type_id == ComboBoxConst.FORMAT_TYPE_AUD_BY_CODEC:
            self.format_stacked_widget.setCurrentWidget(
                self.format_audcodec_combo)
        elif type_id == ComboBoxConst.FORMAT_TYPE_VID_BY_CODEC:
            self.format_stacked_widget.setCurrentWidget(
                self.format_vidcodec_combo)
        elif type_id == ComboBoxConst.FORMAT_TYPE_MERGE:
            self.format_stacked_widget.setCurrentWidget(
                self.format_merge_layout_widget)
        elif type_id == ComboBoxConst.FORMAT_TYPE_RAWSTRING:
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
        if url_type_index == ComboBoxConst.URL_TYPE_SINGLE:
            url = self.url_text.text()
            if not url:
                QMessageBox.warning(self, "Missing download URL",
                                    "Enter a valid URL to be downloaded",
                                    QMessageBox.StandardButton.Ok)
                return
            url_list = [url]
        elif url_type_index == ComboBoxConst.URL_TYPE_LIST:
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
        if self.downloadsubs_check.isChecked():
            if self.generatedsubs_check.isChecked():
                ydl_opts["writeautomaticsub"] = True
            else:
                ydl_opts["writesubtitles"] = True
            subs_language = self.subs_lang_combo.currentData()
            ydl_opts["subtitleslangs"] = [subs_language]
            subs_format = self.subs_format_combo.currentText()
            if self.subs_format_combo.currentData():
                ydl_opts["subtitlesformat"] = subs_format
            else:
                ydl_opts["convertsubtitles"] = subs_format
            sleep_interval = self.subs_delay_spin.value()
            ydl_opts["sleep_interval_subtitles"] = sleep_interval

        # Create format string
        format_str = ""
        type_id = self.format_type_combo.currentData()
        if type_id in [ComboBoxConst.FORMAT_TYPE_AUDVID_BY_QUA,
                       ComboBoxConst.FORMAT_TYPE_AUD_BY_QUA,
                       ComboBoxConst.FORMAT_TYPE_VID_BY_QUA]:
            quality_str = self.format_quality_combo.currentData()
            if type_id == ComboBoxConst.FORMAT_TYPE_AUDVID_BY_QUA:
                format_str = "best" + quality_str
            elif type_id == ComboBoxConst.FORMAT_TYPE_AUD_BY_QUA:
                format_str = "bestaudio" + quality_str
            elif type_id == ComboBoxConst.FORMAT_TYPE_VID_BY_QUA:
                format_str = "bestvideo" + quality_str
        elif type_id == ComboBoxConst.FORMAT_TYPE_AUDVID_BY_EXT:
            ext = self.format_vidext_combo.currentData()
            format_str = ext
        elif type_id == ComboBoxConst.FORMAT_TYPE_AUD_BY_EXT:
            ext = self.format_audext_combo.currentData()
            format_str = f"bestaudio[ext={ext}]"
        elif type_id == ComboBoxConst.FORMAT_TYPE_VID_BY_EXT:
            ext = self.format_vidext_combo.currentData()
            format_str = f"bestvideo[ext={ext}]"
        elif type_id == ComboBoxConst.FORMAT_TYPE_AUD_BY_CODEC:
            codec = self.format_audcodec_combo.currentData()
            format_str = f"bestaudio[acodec^={codec}]"
        elif type_id == ComboBoxConst.FORMAT_TYPE_VID_BY_CODEC:
            codec = self.format_vidcodec_combo.currentData()
            format_str = f"bestvideo[vcodec^={codec}]"
        elif type_id == ComboBoxConst.FORMAT_TYPE_MERGE:
            audtype = self.format_merge_audio_combo.currentData()
            vidtype = self.format_merge_video_combo.currentData()
            format_str = f"{audtype}+{vidtype}"
            ydl_opts["allow_multiple_audio_streams"] = True
            ydl_opts["allow_multiple_video_streams"] = True
        elif type_id == ComboBoxConst.FORMAT_TYPE_RAWSTRING:
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
            text_doc, table = table_create("File formats", headers)

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
                table_add_row(table, fields)
            # Add table to status window
            self.status_text.append(text_doc.toHtml())

        # Reenable widgets that would interfere with processing
        self.enable_active_buttons(True)

    def download_subtitle_formats(self, url):
        """Downloads and displays subtitles available from url

        Args:
            url (str): URL of video
        """
        self.enable_active_buttons(False)
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
                self.enable_active_buttons(True)
                return

            def parse_subs(self, key, name):
                if key not in meta or not isinstance(meta[key],
                                                     dict):
                    self.add_status_message("This video seems to contain no "
                                            "{name}.")
                else:
                    subtitles_list = meta[key]
                    headers = ["Code", "Name", "Format"]
                    text_doc, table = table_create(name, headers)
                    for key, value in subtitles_list.items():
                        for sub in value:
                            fields = []
                            fields.append(key)
                            fields.append(sub["name"] if "name" in sub else "")
                            fields.append(sub["ext"] if "ext" in sub else "")
                            table_add_row(table, fields)
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
        regex = re.compile(AppConst.REGEX_COLORSTRIP)
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
        widgets = [self.list_formats_button, self.list_subs_button,
                   self.bottom_buttonbox]
        for widget in widgets:
            widget.setEnabled(enable)


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
