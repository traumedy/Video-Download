#!/usr/bin/env python3

"""main_window.py - Main application window
"""

__author__ = "Josh Buchbinder"
__copyright__ = "Copyright 2024, Josh Buchbinder"


from typing import Any
from overrides import override
from PySide6.QtCore import Qt, QFileInfo, QDir, QUrl, QSettings
from PySide6.QtGui import QDesktopServices, QCloseEvent, QDragEnterEvent
from PySide6.QtGui import QDropEvent
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox
from PySide6.QtWidgets import QLayout, QFormLayout, QHBoxLayout, QGridLayout
from PySide6.QtWidgets import QLineEdit, QPushButton, QLabel, QFileDialog
from PySide6.QtWidgets import QProgressBar, QDialogButtonBox, QSpinBox
from PySide6.QtWidgets import QCheckBox, QStyle
from PySide6.QtWidgets import QSizePolicy, QStackedWidget
from yt_dlp import YoutubeDL, utils

from comboboxext import ComboBoxExt
from status_window import StatusWindow
from constants import AppConst, SettingsConst, ComboBoxConst, ToolTips, LinkIds
from bookmark_html_parser import BookmarkHTMLParser
from doc_table import DocTable
from utils import value_to_bool, normalize_path, get_ffmpeg_bin_path
from utils import get_videos_path


class MainWindow(QMainWindow):
    """Main application window class derived from QMainWindow
    """
    download_filenames: list[str]
    cancel_flag: bool
    settings: QSettings
    main_layout: QFormLayout
    url_type_combo: ComboBoxExt
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
    specifyformat_check: QCheckBox
    specifyres_check: QCheckBox
    downloadsubs_check: QCheckBox
    autoscroll_check: QCheckBox
    overwrite_check: QCheckBox
    keepfiles_check: QCheckBox
    preferfreeformats_check: QCheckBox
    consoleoutput_check: QCheckBox
    format_layout: QHBoxLayout
    format_stacked_widget: QStackedWidget
    format_type_combo: ComboBoxExt
    format_quality_layout_widget: QWidget
    format_quality_combo: ComboBoxExt
    format_audext_layout_widget: QWidget
    format_audext_combo: ComboBoxExt
    format_vidext_layout_widget: QWidget
    format_vidext_combo: ComboBoxExt
    format_audcodec_layout_widget: QWidget
    format_audcodec_combo: ComboBoxExt
    format_vidcodec_layout_widget: QWidget
    format_vidcodec_combo: ComboBoxExt
    format_merge_layout_widget: QWidget
    format_merge_audio_combo: ComboBoxExt
    format_merge_video_combo: ComboBoxExt
    format_marge_container_combo: ComboBoxExt
    format_string_layout_widget: QWidget
    format_string_text: QLineEdit
    format_string_help_button: QPushButton
    resolution_layout: QHBoxLayout
    resheight_combo: ComboBoxExt
    subtitles_layout: QGridLayout
    subsgenerated_check: QCheckBox
    subs_lang_combo: ComboBoxExt
    subs_all_button: QPushButton
    subs_clear_button: QPushButton
    subs_format_combo: ComboBoxExt
    subs_cnvt_combo: ComboBoxExt
    subs_merge_check: QCheckBox
    subs_delay_spin: QSpinBox
    list_subs_button: QPushButton
    status_text: StatusWindow
    file_progress: QProgressBar
    total_progress: QProgressBar
    close_button: QPushButton
    download_button: QPushButton
    bottom_buttonbox: QDialogButtonBox
    cancel_button: QPushButton
    settings_save: bool
    exit_on_completion: bool

    def __init__(self, settings_load: bool = True,
                 settings_save: bool = True) -> None:
        """Initializer for MainWindow
        """
        super().__init__()

        # Store for when we exit to allow not saving settings
        self.settings_save = settings_save

        # Set title text for window and include app version
        # Import here to avoid circular import
        # pylint: disable=import-outside-toplevel
        from video_download import __version__ as AppVersion
        self.setWindowTitle(f"Video URL downloader v{AppVersion}")

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

        # Used to detect cancel request
        self.cancel_flag = False
        # Used to cause application to exit after performing download
        self.exit_on_completion = False

        # Set minimum window size
        size = self.size()
        self.setMinimumSize(size.width() + 260, size.height())

        if settings_load:
            # Load persistent settings including stored window size
            self.load_settings()

        # Get a default place to store videos if output path is invalid
        download_path = self.download_path_text.text()
        if not download_path or not QFileInfo(download_path).isDir():
            self.download_path_text.setText(get_videos_path())

        # Try to find ffmpeg path if blank or not a directory
        ffmpeg_path = self.ffmpeg_path_text.text()
        if not ffmpeg_path or not QFileInfo(ffmpeg_path).isDir():
            self.ffmpeg_path_text.setText(get_ffmpeg_bin_path())

        # Set status window auto-scroll state
        self.status_text.set_autoscroll(self.autoscroll_check.isChecked())

        # Possibly hide formats and subtitles rows
        visible = self.downloadsubs_check.isChecked()
        self.main_layout.setRowVisible(self.subtitles_layout, visible)
        visible = self.specifyformat_check.isChecked()
        self.main_layout.setRowVisible(self.format_layout, visible)
        visible = self.specifyres_check.isChecked()
        self.main_layout.setRowVisible(self.resolution_layout, visible)

    def create_mainwindow_widgets(self) -> None:
        """Create widgets for window
        """
        self.url_stacked_widget = QStackedWidget()
        self.url_type_combo = ComboBoxExt()
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
        self.specifyformat_check = QCheckBox("Specify format")
        self.specifyres_check = QCheckBox("Specify resolution")
        self.downloadsubs_check = QCheckBox("Download subtitles")
        self.autoscroll_check = QCheckBox("Auto-scroll status window")
        self.overwrite_check = QCheckBox("Overwrite")
        self.keepfiles_check = QCheckBox("Keep files")
        self.preferfreeformats_check = QCheckBox("Prefer free formats")
        self.consoleoutput_check = QCheckBox("Console output")
        self.format_layout = QHBoxLayout()
        self.format_stacked_widget = QStackedWidget()
        self.format_type_combo = ComboBoxExt()
        self.format_quality_layout_widget = QWidget()
        self.format_quality_combo = ComboBoxExt()
        self.format_audext_layout_widget = QWidget()
        self.format_audext_combo = ComboBoxExt()
        self.format_vidext_layout_widget = QWidget()
        self.format_vidext_combo = ComboBoxExt()
        self.format_audcodec_layout_widget = QWidget()
        self.format_audcodec_combo = ComboBoxExt()
        self.format_vidcodec_layout_widget = QWidget()
        self.format_vidcodec_combo = ComboBoxExt()
        self.format_merge_layout_widget = QWidget()
        self.format_merge_audio_combo = ComboBoxExt()
        self.format_merge_video_combo = ComboBoxExt()
        self.format_marge_container_combo = ComboBoxExt()
        self.format_string_layout_widget = QWidget()
        self.format_string_text = QLineEdit()
        self.format_string_help_button = QPushButton("Help")
        self.resolution_layout = QHBoxLayout()
        self.resheight_combo = ComboBoxExt()
        self.subtitles_layout = QGridLayout()
        self.subsgenerated_check = QCheckBox("Auto-generated")
        self.subs_lang_combo = ComboBoxExt(checkboxes=True)
        self.subs_all_button = QPushButton("Check all languages")
        self.subs_clear_button = QPushButton("Uncheck all languages")
        self.subs_format_combo = ComboBoxExt()
        self.subs_cnvt_combo = ComboBoxExt()
        self.subs_merge_check = QCheckBox("Merge into video")
        self.subs_delay_spin = QSpinBox()
        self.list_subs_button = QPushButton("List subtitles")
        self.status_text = StatusWindow(self.status_click_callback)
        self.file_progress = QProgressBar()
        self.total_progress = QProgressBar()
        self.cancel_button = QPushButton("Cancel")
        self.close_button = QPushButton("Close")
        self.download_button = QPushButton("Start downloading")
        self.bottom_buttonbox = QDialogButtonBox()

        # Set widget properties

        # Populate url type listbox
        for label in ComboBoxConst.URL_TYPE_LABELS:
            self.url_type_combo.addItem(label)
        # These Expanding policies seem necessary for Mac to get the
        # QLineEdit fields to expand to fill
        widgets: list[QWidget] = [self.list_path_text, self.download_path_text,
                                  self.ffmpeg_path_text]
        for widget in widgets:
            widget.setSizePolicy(QSizePolicy.Policy.Expanding,
                                 QSizePolicy.Policy.Minimum)
        # Prevent QStackedWidgets from expanding vertically
        widgets = [self.url_stacked_widget, self.format_stacked_widget]
        for widget in widgets:
            widget.setSizePolicy(QSizePolicy.Policy.Expanding,
                                 QSizePolicy.Policy.Fixed)
        # Prevent various other widgets from expanding horizontally
        widgets = [self.list_path_browse_button,
                   self.download_path_browse_button,
                   self.ffmpeg_path_browse_button, self.subs_clear_button,
                   self.subs_all_button, self.list_subs_button,
                   self.resheight_combo]
        for widget in widgets:
            widget.setSizePolicy(QSizePolicy.Policy.Fixed,
                                 QSizePolicy.Policy.Fixed)

        # Populate subtitles combo boxes
        for lang, lang_code in ComboBoxConst.SUBTITLES_LANGUAGES_LIST:
            self.subs_lang_combo.add_check_item(lang, lang_code)
        for label in ComboBoxConst.SUBTITLES_DOWNFMT_LIST:
            self.subs_format_combo.addItem(label)
        for label, data in ComboBoxConst.SUBTITLES_CNVTFMT_LIST:
            self.subs_cnvt_combo.addItem(label, data)

        # Populate format selection combo boxes
        for label, idx, _ in ComboBoxConst.FORMAT_TYPE_LIST:
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
        for label, fstr, _ in ComboBoxConst.FORMAT_MERGE_AUD_LIST:
            self.format_merge_audio_combo.addItem(label, fstr)
        for label, fstr, _ in ComboBoxConst.FORMAT_MERGE_VID_LIST:
            self.format_merge_video_combo.addItem(label, fstr)
        for ext in ComboBoxConst.FORMAT_MERGE_OUTPUT_LIST:
            self.format_marge_container_combo.addItem(ext, ext)

        # Populate resolution combobox
        for label, res in ComboBoxConst.FORMAT_RESOLUTION_LIST:
            self.resheight_combo.addItem(label, res)

        # Set progress bars display text formats
        self.file_progress.setFormat(AppConst.FORMATSTR_FILEPROGRESS)
        self.total_progress.setFormat(AppConst.FORMATSTR_TOTALPROGRESS)

        # Hide cancel button
        self.cancel_button.setVisible(False)

        # Populate dialog button box
        self.bottom_buttonbox.addButton(self.close_button,
                                        QDialogButtonBox.ButtonRole.RejectRole)
        self.bottom_buttonbox.addButton(self.download_button,
                                        QDialogButtonBox.ButtonRole.AcceptRole)

    def create_mainwindow_layout(self) -> QLayout:
        """Creates layout for main window

        Returns:
            QLayout: Layout for main window
        """
        # Single URL layout
        url_layout = QHBoxLayout(self.url_text_layout_widget)
        url_layout.addWidget(self.url_text)
        url_layout.addWidget(self.list_formats_button)
        # URL list layout
        list_path_layout = QHBoxLayout(self.list_path_layout_widget)
        list_path_layout.addWidget(self.list_path_text)
        list_path_layout.addWidget(self.list_path_browse_button, 0,
                                   Qt.AlignmentFlag.AlignRight)
        # Stacked widget to hold single URL and URL list layouts
        self.url_stacked_widget.addWidget(self.url_text_layout_widget)
        self.url_stacked_widget.addWidget(self.list_path_layout_widget)
        # Download path layout
        download_path_layout = QHBoxLayout()
        download_path_layout.addWidget(self.download_path_text)
        download_path_layout.addWidget(self.download_path_browse_button, 0,
                                       Qt.AlignmentFlag.AlignRight)
        # FFMPEG path layout
        ffmpeg_layout = QHBoxLayout()
        ffmpeg_layout.addWidget(self.ffmpeg_path_text)
        ffmpeg_layout.addWidget(self.ffmpeg_path_browse_button, 0,
                                Qt.AlignmentFlag.AlignRight)
        # Username/password layout
        auth_layout = QHBoxLayout()
        auth_layout.addWidget(QLabel("Username:"))
        auth_layout.addWidget(self.username_text)
        auth_layout.addWidget(QLabel("Password:"))
        auth_layout.addWidget(self.password_text)
        # Switches (checkboxes) layout
        switches_layout = QGridLayout()
        switches_layout.addWidget(self.specifyformat_check, 1, 1)
        switches_layout.addWidget(self.specifyres_check, 2, 1)
        switches_layout.addWidget(self.downloadsubs_check, 1, 2)
        switches_layout.addWidget(self.autoscroll_check, 2, 2)
        switches_layout.addWidget(self.overwrite_check, 1, 3)
        switches_layout.addWidget(self.keepfiles_check, 2, 3)
        switches_layout.addWidget(self.preferfreeformats_check, 1, 4)
        switches_layout.addWidget(self.consoleoutput_check, 2, 4)
        # - Format selection layouts
        # Audio + video by quality layout
        format_quality_layout = QHBoxLayout(
            self.format_quality_layout_widget)
        format_quality_layout.addWidget(QLabel("Quality:"),
                                        alignment=Qt.AlignmentFlag.AlignRight)
        format_quality_layout.addWidget(self.format_quality_combo,
                                        alignment=Qt.AlignmentFlag.AlignLeft)
        format_quality_layout.addStretch()
        # Audio only by extension layout
        format_audext_layout = QHBoxLayout(self.format_audext_layout_widget)
        format_audext_layout.addWidget(QLabel("File extension:"),
                                       alignment=Qt.AlignmentFlag.AlignRight)
        format_audext_layout.addWidget(self.format_audext_combo,
                                       alignment=Qt.AlignmentFlag.AlignLeft)
        format_audext_layout.addStretch()
        # Video only by extension layout
        format_vidext_layout = QHBoxLayout(self.format_vidext_layout_widget)
        format_vidext_layout.addWidget(QLabel("Video extension:"),
                                       alignment=Qt.AlignmentFlag.AlignRight)
        format_vidext_layout.addWidget(self.format_vidext_combo,
                                       alignment=Qt.AlignmentFlag.AlignLeft)
        format_vidext_layout.addStretch()
        # Audio only by codec layout
        format_audcodec_layout = QHBoxLayout(
            self.format_audcodec_layout_widget)
        format_audcodec_layout.addWidget(QLabel("Audio codec:"),
                                         alignment=Qt.AlignmentFlag.AlignRight)
        format_audcodec_layout.addWidget(self.format_audcodec_combo,
                                         alignment=Qt.AlignmentFlag.AlignLeft)
        format_audcodec_layout.addStretch()
        # Video only by codec layout
        format_vidcodec_layout = QHBoxLayout(
            self.format_vidcodec_layout_widget)
        format_vidcodec_layout.addWidget(QLabel("Video codec:"),
                                         alignment=Qt.AlignmentFlag.AlignRight)
        format_vidcodec_layout.addWidget(self.format_vidcodec_combo,
                                         alignment=Qt.AlignmentFlag.AlignLeft)
        format_vidcodec_layout.addStretch()
        # Raw format string layout
        format_string_layout = QHBoxLayout(
            self.format_string_layout_widget)
        format_string_layout.addWidget(QLabel("Format string:"))
        format_string_layout.addWidget(self.format_string_text)
        format_string_layout.addWidget(self.format_string_help_button, 0,
                                       Qt.AlignmentFlag.AlignRight)
        # Merge formats layout
        format_merge_layout = QHBoxLayout(
            self.format_merge_layout_widget)
        format_merge_layout.addWidget(QLabel("Audio:"),
                                      alignment=Qt.AlignmentFlag.AlignRight)
        format_merge_layout.addWidget(self.format_merge_audio_combo)
        format_merge_layout.addWidget(QLabel("Video:"),
                                      alignment=Qt.AlignmentFlag.AlignRight)
        format_merge_layout.addWidget(self.format_merge_video_combo)
        format_merge_layout.addWidget(QLabel("Output format:"),
                                      alignment=Qt.AlignmentFlag.AlignRight)
        format_merge_layout.addWidget(self.format_marge_container_combo)
        # format_merge_layout.addStretch()
        # Stacked layout widget for format selection layouts
        self.format_stacked_widget.addWidget(self.format_quality_layout_widget)
        self.format_stacked_widget.addWidget(self.format_audext_layout_widget)
        self.format_stacked_widget.addWidget(self.format_vidext_layout_widget)
        self.format_stacked_widget.addWidget(
            self.format_audcodec_layout_widget)
        self.format_stacked_widget.addWidget(
            self.format_vidcodec_layout_widget)
        self.format_stacked_widget.addWidget(self.format_merge_layout_widget)
        self.format_stacked_widget.addWidget(self.format_string_layout_widget)
        # Main format selection layout
        self.format_layout.addWidget(self.format_type_combo)
        self.format_layout.addWidget(self.format_stacked_widget)
        # Resolution layout
        self.resolution_layout.addWidget(self.resheight_combo)
        self.resolution_layout.addStretch()
        # Subtitles layout
        self.subtitles_layout.addWidget(self.subsgenerated_check, 1, 1)
        self.subtitles_layout.addWidget(self.subs_merge_check, 2, 1)
        self.subtitles_layout.addWidget(QLabel("Languages:"), 1, 2,
                                        alignment=Qt.AlignmentFlag.AlignRight)
        self.subtitles_layout.addWidget(self.subs_lang_combo, 1, 3)
        self.subtitles_layout.addWidget(self.subs_all_button, 2, 2,
                                        alignment=Qt.AlignmentFlag.AlignRight)
        self.subtitles_layout.addWidget(self.subs_clear_button, 2, 3,
                                        alignment=Qt.AlignmentFlag.AlignLeft)
        self.subtitles_layout.addWidget(QLabel("Download format:"), 1, 4,
                                        alignment=Qt.AlignmentFlag.AlignRight)
        self.subtitles_layout.addWidget(self.subs_format_combo, 1, 5)
        self.subtitles_layout.addWidget(QLabel("Convert to format:"), 2, 4,
                                        alignment=Qt.AlignmentFlag.AlignRight)
        self.subtitles_layout.addWidget(self.subs_cnvt_combo, 2, 5)
        self.subtitles_layout.addWidget(QLabel("Download delay:"), 2, 6,
                                        alignment=Qt.AlignmentFlag.AlignRight)
        self.subtitles_layout.addWidget(self.list_subs_button, 1, 7)
        self.subtitles_layout.addWidget(self.subs_delay_spin, 2, 7)

        # By default the layout is too tall for the QStackedWidget
        layouts = [url_layout, list_path_layout, format_quality_layout,
                   format_audext_layout, format_vidext_layout,
                   format_audcodec_layout, format_vidcodec_layout,
                   format_merge_layout, format_string_layout]
        for layout in layouts:
            layout.setContentsMargins(0, 0, 0, 0)

        # Use Form Layout for window
        self.main_layout = QFormLayout()

        # Add widgets to window layout
        self.main_layout.addRow(self.url_type_combo, self.url_stacked_widget)
        self.main_layout.addRow("Download path:", download_path_layout)
        self.main_layout.addRow("FFMPEG path:", ffmpeg_layout)
        self.main_layout.addRow("Authentication:", auth_layout)
        self.main_layout.addRow("Switches:", switches_layout)
        self.main_layout.addRow("Format selection:", self.format_layout)
        self.main_layout.addRow("Max resolution:", self.resolution_layout)
        self.main_layout.addRow("Subtitles:", self.subtitles_layout)
        self.main_layout.addRow(self.status_text)
        self.main_layout.addRow("File progress", self.file_progress)
        self.main_layout.addRow("Total progress", self.total_progress)
        self.main_layout.addRow(QLabel(""))
        self.main_layout.addRow(self.cancel_button, self.bottom_buttonbox)

        return self.main_layout

    def connect_mainwindow_signals(self) -> None:
        """Connect main window signals
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
        self.specifyformat_check.checkStateChanged.connect(
            lambda checked: self.main_layout.setRowVisible(
                self.format_layout, checked == Qt.CheckState.Checked))
        self.specifyres_check.checkStateChanged.connect(
            lambda checked: self.main_layout.setRowVisible(
                self.resolution_layout, checked == Qt.CheckState.Checked))
        self.downloadsubs_check.checkStateChanged.connect(
            lambda checked: self.main_layout.setRowVisible(
                self.subtitles_layout, checked == Qt.CheckState.Checked))
        self.autoscroll_check.checkStateChanged.connect(
            lambda checked: self.status_text.set_autoscroll(
                checked == Qt.CheckState.Checked))
        self.subs_all_button.clicked.connect(
            lambda: self.subs_lang_combo.check_all(True))
        self.subs_clear_button.clicked.connect(
            lambda: self.subs_lang_combo.check_all(False))
        self.list_subs_button.clicked.connect(
            lambda: self.download_subtitle_formats(self.url_text.text()))
        self.format_type_combo.currentIndexChanged.connect(
            self.format_type_combo_changed)
        self.format_string_help_button.clicked.connect(
            lambda: QDesktopServices.openUrl(
                AppConst.URL_HELP_FORMATSELECTION))
        self.cancel_button.clicked.connect(self.cancel_button_clicked)
        self.close_button.clicked.connect(self.close)
        self.download_button.clicked.connect(self.download_button_clicked)

    def create_mainwindow_tooltips(self) -> None:
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
        self.specifyformat_check.setToolTip(ToolTips.TTT_SPECIFYFORMAT_CHECK)
        self.specifyres_check.setToolTip(ToolTips.TTT_SPECIFYRES_CHECK)
        self.downloadsubs_check.setToolTip(ToolTips.TTT_DOWNLOADSUBS_CHECK)
        self.autoscroll_check.setToolTip(ToolTips.TTT_AUTOSCROLL_CHECK)
        self.overwrite_check.setToolTip(ToolTips.TTT_OVERWRITE_CHECK)
        self.keepfiles_check.setToolTip(ToolTips.TTT_KEEPFILES_CHECK)
        self.preferfreeformats_check.setToolTip(
            ToolTips.TTT_PREFERFREEFORMATS_CHECK)
        self.consoleoutput_check.setToolTip(ToolTips.TTT_CONSOLEOUTPUT_CHECK)
        self.subsgenerated_check.setToolTip(ToolTips.TTT_SUBSGENERATED_CHECK)
        self.subs_lang_combo.setToolTip(ToolTips.TTT_SUBS_LANG_COMBO)
        self.subs_clear_button.setToolTip(ToolTips.TTT_SUBS_CLEAR_BUTTON)
        self.subs_format_combo.setToolTip(ToolTips.TTT_SUBS_FORMAT_COMBO)
        self.subs_cnvt_combo.setToolTip(ToolTips.TTT_SUBS_CONVERT_COMBO)
        self.subs_merge_check.setToolTip(ToolTips.TTT_SUBS_MERGE_CHECK)
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
            ToolTips.TTT_FORMAT_MERGE_VIDEO_COMBO)
        self.format_marge_container_combo.setToolTip(
            ToolTips.TTT_FORMAT_MARGE_CONTAINER_COMBO)
        self.format_string_text.setToolTip(ToolTips.TTT_FORMAT_STRING_TEXT)
        self.format_string_help_button.setToolTip(
            ToolTips.TTT_FORMAT_STRING_HELP_BUTTON)
        self.resheight_combo.setToolTip(ToolTips.TTT_RESOLUTION_COMBO)
        self.status_text.setToolTip(ToolTips.TTT_STATUSWINDOW_TEXT)
        self.close_button.setToolTip(ToolTips.TTT_CLOSE_BUTTON)
        self.download_button.setToolTip(ToolTips.TTT_DOWNLOAD_BUTTON)

    @override
    def closeEvent(self, event: QCloseEvent) -> None:
        """Overridden method, called when window is closing

        Args:
            event (PySide6.QtGui.QCloseEvent): Event type
        """
        self.cancel_flag = True
        if self.settings_save:
            self.save_settings()
        event.accept()

    @override
    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        """Overriden method, called when a file is dragged over window

        Args:
            event (PySide6.QtGui.QDragEnterEvent): Event info
        """
        drag_url = QUrl(event.mimeData().text())
        if drag_url.isLocalFile():
            drag_file = QFileInfo(drag_url.toLocalFile())
            suffix = drag_file.suffix().lower()
            if suffix in AppConst.EXTENSIONS_URLLIST:
                event.accept()
                return
        event.ignore()

    @override
    def dropEvent(self, event: QDropEvent) -> None:
        """Overriden method, called when a file is dropped on window

        Args:
            event (PySide6.QtGui.QDropEvent): Event info
        """
        drag_url = QUrl(event.mimeData().text())
        if drag_url.isLocalFile():
            drag_file = QFileInfo(drag_url.toLocalFile())
            self.list_path_text.setText(drag_file.filePath())
            event.accept()
            return
        event.ignore()

    def display_warning(self, title: str, message: str) -> None:
        """Displays a warning, possibly via message box or console

        Args:
            message (str): Message to display
        """
        if self.exit_on_completion or self.consoleoutput_check.isChecked():
            print(message)
            if self.exit_on_completion:
                self.close()
        elif not self.exit_on_completion:
            QMessageBox.warning(self, title, message,
                                QMessageBox.StandardButton.Ok)

    def status_click_callback(self, link: str) -> None:
        """Callback when a link is clicked in the status text widget

        Args:
            link (str): The anchor link
        """
        parts = link.split(':')
        if len(parts) == 2:
            ident = parts[0]
            value = parts[1]
            if ident == LinkIds.LINKID_FORMATID:
                self.format_type_combo.set_current_data(
                       ComboBoxConst.FORMAT_TYPE_RAWSTRING)
                self.specifyformat_check.setChecked(True)
                self.format_string_text.setText(value)
            elif ident == LinkIds.LINKID_FILEEXT:
                if value in ComboBoxConst.FORMAT_EXT_VID_LIST:
                    if self.format_vidext_combo.set_current_text(value):
                        self.format_type_combo.set_current_data(
                            ComboBoxConst.FORMAT_TYPE_AUDVID_BY_EXT)
                        self.specifyformat_check.setChecked(True)
                elif value in ComboBoxConst.FORMAT_EXT_AUD_LIST:
                    if self.format_audext_combo.set_current_text(value):
                        self.format_type_combo.set_current_data(
                            ComboBoxConst.FORMAT_TYPE_AUD_BY_EXT)
                        self.specifyformat_check.setChecked(True)
            elif ident == LinkIds.LINKID_AUDIOCODEC:
                dotpos = value.find(".")
                if dotpos != -1:
                    value = value[0:dotpos]
                # TODO
            elif ident == LinkIds.LINKID_VIDEOCODEC:
                dotpos = value.find(".")
                if dotpos != -1:
                    value = value[0:dotpos]
                # TODO
                # if self.format_vidcodec_combo.set_current_data(value):
                #     self.specifyformat_check.setChecked(True)
                #     self.format_type_combo.set_current_data(
                #        ComboBoxConst.FORMAT_TYPE_VID_BY_CODEC)
            elif ident == LinkIds.LINKID_SUBLANGUAGE:
                if self.subs_lang_combo.check_item_by_data(value, True):
                    self.downloadsubs_check.setChecked(True)
            elif ident == LinkIds.LINKID_SUBEXTENSION:
                if self.subs_format_combo.set_current_text(value):
                    self.downloadsubs_check.setChecked(True)
            elif ident == LinkIds.LINKID_RESOLUTION:
                xpos = value.find("x")
                if xpos != -1:
                    value = value[xpos + 1:]
                try:
                    if self.resheight_combo.set_current_data_lte(int(value)):
                        self.specifyres_check.setChecked(True)
                except ValueError:
                    pass

    def load_settings(self) -> None:
        """Loads persistent settings
        """
        widgets = SettingsConst.get_mainwindow_widgets_vals(self)
        for widget, settings_key, default in widgets:
            if isinstance(widget, QLineEdit):
                widget.setText(str(self.settings.value(settings_key, default)))
            elif isinstance(widget, ComboBoxExt):
                if widget.has_checkboxes():
                    checked_items = str(self.settings.value(
                        settings_key, default)).split("|")
                    widget.check_items_by_text(checked_items, True)
                else:
                    widget.setCurrentText(str(self.settings.value(settings_key,
                                                                  default)))
            elif isinstance(widget, QCheckBox):
                widget.setChecked(value_to_bool(
                                  self.settings.value(settings_key, default)))
            elif isinstance(widget, QSpinBox):
                widget.setValue(int(self.settings.value(settings_key,
                                default, int)))  # type: ignore
        # Restore widow size
        size = self.size()
        width = int(self.settings.value(SettingsConst.SETTINGS_VAL_WINDOWWIDTH,
                    size.width()))  # type: ignore
        height = int(self.settings.value(
                     SettingsConst.SETTINGS_VAL_WINDOWHEIGHT,
                     size.height(), int))  # type: ignore
        self.resize(width, height)
        state = self.settings.value(
                            SettingsConst.SETTINGS_VAL_WINDOWSTATE,
                            Qt.WindowState.WindowNoState, int)
        self.setWindowState(Qt.WindowState(state))

    def save_settings(self) -> None:
        """Save persistent settings
        """
        widgets = SettingsConst.get_mainwindow_widgets_vals(self)
        for widget, settings_key, _ in widgets:
            if isinstance(widget, QLineEdit):
                self.settings.setValue(settings_key, widget.text())
            elif isinstance(widget, ComboBoxExt):
                if widget.has_checkboxes():
                    checked_items = widget.checked_items_text()
                    self.settings.setValue(settings_key,
                                           "|".join(checked_items))
                else:
                    self.settings.setValue(settings_key, widget.currentText())
            elif isinstance(widget, QCheckBox):
                self.settings.setValue(settings_key, widget.isChecked())
            elif isinstance(widget, QSpinBox):
                self.settings.setValue(settings_key, widget.value())
        # Save size and state of main window
        state = self.windowState()
        if not state & Qt.WindowState.WindowMaximized:
            self.settings.setValue(SettingsConst.SETTINGS_VAL_WINDOWWIDTH,
                                   self.width())
            self.settings.setValue(SettingsConst.SETTINGS_VAL_WINDOWHEIGHT,
                                   self.height())
        self.settings.setValue(SettingsConst.SETTINGS_VAL_WINDOWSTATE,
                               state.value)

    def list_formats_button_clicked(self) -> None:
        """Called when list formats button is clicked
        """
        url = self.url_text.text()
        if not url:
            self.display_warning("Missing download URL",
                                 "Enter a valid URL for format listing")
            return
        self.download_url_formats(url)
        # Restore focus to clicked button which got disabled and lost focus
        self.list_formats_button.setFocus()

    def list_browse_button_clicked(self) -> None:
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
            path = normalize_path(selected_files[0])
            self.list_path_text.setText(path)

    def download_browse_button_clicked(self) -> None:
        """Called when download path browse button is clicked
        """
        # For initial directory
        dir_info = QFileInfo(self.download_path_text.text())
        # Simple dialog
        path = QFileDialog.getExistingDirectory(
            self,
            "Save videos to directory...",
            dir_info.filePath(),
            QFileDialog.Option.ShowDirsOnly
            | QFileDialog.Option.DontResolveSymlinks)
        if path:
            self.download_path_text.setText(normalize_path(path))

    def ffmpeg_browse_button_clicked(self) -> None:
        """Called when ffmpeg browse button is clicked
        """
        # For initial directory
        dir_info = QFileInfo(self.ffmpeg_path_text.text())
        # Simple dialog
        path = QFileDialog.getExistingDirectory(
            self,
            "FFMPEG location directory...",
            dir_info.filePath(),
            QFileDialog.Option.ShowDirsOnly
            | QFileDialog.Option.DontResolveSymlinks)
        if path:
            self.ffmpeg_path_text.setText(path)

    def format_type_combo_changed(self, new_index: int) -> None:
        """Called when format type combo changes

        Args:
            new_index (int): Index of newly selected item
        """
        type_id = self.format_type_combo.itemData(new_index)
        if type_id in [ComboBoxConst.FORMAT_TYPE_AUDVID_BY_QUA,
                       ComboBoxConst.FORMAT_TYPE_AUD_BY_QUA,
                       ComboBoxConst.FORMAT_TYPE_VID_BY_QUA]:
            self.format_stacked_widget.setCurrentWidget(
                self.format_quality_layout_widget)
        elif type_id == ComboBoxConst.FORMAT_TYPE_AUD_BY_EXT:
            self.format_stacked_widget.setCurrentWidget(
                self.format_audext_layout_widget)
        elif type_id in [ComboBoxConst.FORMAT_TYPE_VID_BY_EXT,
                         ComboBoxConst.FORMAT_TYPE_AUDVID_BY_EXT]:
            self.format_stacked_widget.setCurrentWidget(
                self.format_vidext_layout_widget)
        elif type_id == ComboBoxConst.FORMAT_TYPE_AUD_BY_CODEC:
            self.format_stacked_widget.setCurrentWidget(
                self.format_audcodec_layout_widget)
        elif type_id == ComboBoxConst.FORMAT_TYPE_VID_BY_CODEC:
            self.format_stacked_widget.setCurrentWidget(
                self.format_vidcodec_layout_widget)
        elif type_id == ComboBoxConst.FORMAT_TYPE_MERGE:
            self.format_stacked_widget.setCurrentWidget(
                self.format_merge_layout_widget)
        elif type_id == ComboBoxConst.FORMAT_TYPE_RAWSTRING:
            self.format_stacked_widget.setCurrentWidget(
                self.format_string_layout_widget)

    def cancel_button_clicked(self) -> None:
        """Called when cancel button is clicked
        """
        self.cancel_flag = True
        self.add_status_message("Canceling...")

    def download_button_clicked(self) -> None:
        """Called when download button is clicked
        """
        dir_info = QFileInfo(self.download_path_text.text())
        if not dir_info.isDir():
            self.display_warning("Missing download directory",
                                 "Enter a valid directory for files to be "
                                 "downloaded to")
            return
        url_list: list[str] = []
        url_type_index = self.url_type_combo.currentIndex()
        if url_type_index == ComboBoxConst.URL_TYPE_SINGLE:
            url = self.url_text.text()
            if not url:
                self.display_warning("Missing download URL",
                                     "Enter a valid URL to be downloaded")
                return
            url_list = [url]
        elif url_type_index == ComboBoxConst.URL_TYPE_LIST:
            file_info = QFileInfo(self.list_path_text.text())
            if not file_info.exists():
                self.display_warning("Missing URL list",
                                     "Enter the path to a valid list of URLs")
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
                    self.display_warning("Unsupported file type",
                                         "Valid file types are HTML, TXT")
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

    def parse_txt_file(self, file_path: str) -> list[str]:
        """Parses a simple text file and builds a list of entries

        Args:
            file_path (str): Path to file to parse

        Returns:
            list[str]: List of lines extracted from file
        """
        url_list = [line.strip('\n') for line in open(file_path, 'r',
                                                      encoding="utf-8")
                    .readlines() if line[0] != '#']
        # Remove blank lines
        url_list_clean = [x for x in url_list if x]
        return url_list_clean

    def parse_html_file(self, file_path: str) -> list[str]:
        """Parses a HTML bookmark file and builds a list of entries.
        These files are exported from Chrome and Firefox

        Args:
            file_path (str): Path to file to parse

        Returns:
            list[str]: List of lines extracted from file
        """
        # Use our custom HTML parser
        parser = BookmarkHTMLParser(self)
        # Feed file into parser
        with open(file_path, 'r', encoding="utf-8") as f:
            parser.feed(f.read())
        # Get URL list from parser
        return parser.get_url_list()

    def create_ydl_quiet_options(self, ydl_opts: dict[str, Any]) -> None:
        """Returns a YouTubeDL Options map preset to quiet settings

        Args:
            ydl_opts (dict[str, Any]): Dict of options for yt_dlp.YoutubeDL
                constructor
        """
        if self.consoleoutput_check.isChecked():
            ydl_opts["quiet"] = False
            ydl_opts["verbose"] = True
            ydl_opts["no_warnings"] = False
        else:
            ydl_opts["quiet"] = True
            ydl_opts["verbose"] = False
            ydl_opts["no_warnings"] = True
        ydl_opts["noprogress"] = True

    def create_ydl_auth_options(self, ydl_opts: dict[str, Any]) -> None:
        """Sets the dictionary values for authentication options

        Args:
            ydl_opts (dict[str, Any]): Dict of options for yt_dlp.YoutubeDL
                constructor
        """
        username = self.username_text.text()
        if username:
            ydl_opts["username"] = username
        password = self.password_text.text()
        if password:
            ydl_opts["password"] = password

    def create_ydl_switches_options(self, ydl_opts: dict[str, Any]) -> None:
        """Sets the dictionary values for various switch options

        Args:
            ydl_opts (dict[str, Any]): Dict of options for yt_dlp.YoutubeDL
                constructor
        """
        if self.overwrite_check.isChecked():
            ydl_opts["overwrites"] = True
        if self.keepfiles_check.isChecked():
            ydl_opts["keepvideo"] = True
        if self.preferfreeformats_check.isChecked():
            ydl_opts["prefer_free_formats"] = True

    def create_ydl_subtitle_options(self, ydl_opts: dict[str, Any]) -> None:
        """Sets the dictionary values for subtitle options

        Args:
            ydl_opts (dict[str, Any]): Dict of options for yt_dlp.YoutubeDL
                constructor
        """
        if self.downloadsubs_check.isChecked():
            if self.subsgenerated_check.isChecked():
                ydl_opts["writeautomaticsub"] = True
            else:
                ydl_opts["writesubtitles"] = True
            subs_languages = self.subs_lang_combo.checked_items_data()
            if subs_languages:
                ydl_opts["subtitleslangs"] = subs_languages
                message = "Downloading subtitle languages: " \
                    f"{','.join(subs_languages)}"
                self.add_status_message(message)
            subs_format = self.subs_format_combo.currentText()
            ydl_opts["subtitlesformat"] = subs_format
            sleep_interval = self.subs_delay_spin.value()
            if sleep_interval:
                ydl_opts["sleep_interval_subtitles"] = sleep_interval
            # Create post processors dictionary
            postprocessors_dict: list[dict[str, Any]] = []
            convert_format = self.subs_cnvt_combo.currentData()
            if convert_format:
                postprocessors_dict.append({"format": convert_format,
                                            'key': 'FFmpegSubtitlesConvertor',
                                            'when': 'before_dl'})
            if self.subs_merge_check.isChecked():
                postprocessors_dict.append({'already_have_subtitle': True,
                                            'key': 'FFmpegEmbedSubtitle'})
            if postprocessors_dict:
                ydl_opts["postprocessors"] = postprocessors_dict

    def create_ydl_format_options(self, ydl_opts: dict[str, Any]) -> None:
        """Sets the dictionary values for format options

        Args:
            ydl_opts (dict[str, Any]): Dict of options for yt_dlp.YoutubeDL
                constructor
        """
        format_str = ""
        if self.specifyformat_check.isChecked():
            # Create format string
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
                output_ext = self.format_marge_container_combo.currentData()
                format_str = f"{audtype}+{vidtype}"
                ydl_opts["merge_output_format"] = output_ext
                ydl_opts["allow_multiple_audio_streams"] = True
                ydl_opts["allow_multiple_video_streams"] = True
            elif type_id == ComboBoxConst.FORMAT_TYPE_RAWSTRING:
                format_str = self.format_string_text.text()
        if format_str:
            message = f"Using format string: {format_str}"
            self.add_status_message(message)
            ydl_opts["format"] = format_str
        if self.specifyres_check.isChecked():
            resdata = self.resheight_combo.currentData()
            if resdata:
                sort_str = f"height:{resdata}"
                ydl_opts["format_sort"] = [sort_str]
                message = f"Using format sort string: {sort_str}"
                self.add_status_message(message)

    def create_ydl_download_options(self) -> dict[str, Any]:
        """Creates the dictionary of options to pass to yt_dlp.YoutubeDL
        for downloading media files, built from UI values and some
        default values

        Returns:
            dict[str, Any]: Dictionary of options for yt_dlp.YoutubeDL
                constructor
        """
        # Set options for yt_dlp.YoutubeDL
        ydl_opts: dict[str, Any] = {}
        ydl_opts["postprocessor_hooks"] = [self.ydl_postprocessor_hook]
        ffmpeg_path = self.ffmpeg_path_text.text()
        if ffmpeg_path:
            ydl_opts["ffmpeg_location"] = ffmpeg_path
        self.create_ydl_quiet_options(ydl_opts)
        self.create_ydl_auth_options(ydl_opts)
        self.create_ydl_switches_options(ydl_opts)
        self.create_ydl_subtitle_options(ydl_opts)
        self.create_ydl_format_options(ydl_opts)
        return ydl_opts

    def download_url_list(self, url_list: list[str]) -> None:
        """Performs the downloading of URLs

        Args:
            url_list (list[str]): List of URLs to download
        """
        # Disable widgets that would interfere with processing
        self.enable_active_buttons(False)

        errors: list[str] = []
        self.download_filenames = []
        count = 0
        ydl_opts = self.create_ydl_download_options()

        # Reset total progress bar
        self.file_progress.setValue(0)
        self.file_progress.setTextVisible(False)
        self.total_progress.setRange(0, len(url_list))
        self.total_progress.setValue(0)

        # Unhide cancel button
        self.cancel_button.setVisible(True)

        # Perform downloads
        with YoutubeDL(ydl_opts) as ydl:
            ydl.add_progress_hook(self.ydl_download_progress_hook)
            for url in url_list:
                if self.cancel_flag:
                    break
                message = f"Trying download of URL {url}"
                self.add_status_message(message)
                try:
                    ydl.download(url)
                except utils.DownloadError as e:
                    error_message = str(e)
                    errors.append(error_message)
                    message = f"Download error: {error_message}"
                    self.add_status_message(message)
                except utils.DownloadCancelled as e:
                    error_message = str(e)
                    errors.append(error_message)
                    message = f"Download canceled: {error_message}"
                    self.add_status_message(message)
                count += 1
                self.total_progress.setValue(count)

        # Reenable widgets
        self.enable_active_buttons(True)
        self.cancel_flag = False
        self.cancel_button.setVisible(False)

        # Display summary message box
        message = f"{len(url_list)} URLs processed"
        message += f"\n{len(self.download_filenames)} downloads complete"
        if errors:
            message += f"\n{len(errors)} errors encountered"
        if self.exit_on_completion:
            print(message)
            self.close()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Download complete")
            dlg.setText(message)
            dlg.exec()

    def ydl_download_progress_hook(self, progress_dict:
                                   dict[str, Any]) -> None:
        """Callback function for download progress

        Args:
            progress_dict (dict[str:Any]): progress dictionary
        """
        # Drive message loop
        QApplication.processEvents()
        if self.cancel_flag:
            raise utils.DownloadCancelled("Aborted")
        status = progress_dict.get("status", None)
        file_bytes = progress_dict.get("downloaded_bytes", None)
        file_total = progress_dict.get("total_bytes", None)
        if not file_total:
            file_total = progress_dict.get("total_bytes_estimate", None)

        if "downloading" == status:
            if file_bytes is not None and file_total is not None:
                pos_value = file_bytes // 1024 // 1024
                pos_max = file_total // 1024 // 1024
                self.file_progress.setTextVisible(True)
                self.file_progress.setValue(pos_value)
                self.file_progress.setMaximum(pos_max)
        if "filename" in progress_dict:
            filename = progress_dict["filename"]
            if filename not in self.download_filenames:
                self.download_filenames.append(filename)
                message = f"Downloading file {filename}"
                self.add_status_message(message)
            if "finished" == status:
                message = f"Finished with file {filename}"
                self.add_status_message(message)
                if file_total:
                    pos_max = file_total // 1024 // 1024
                    self.file_progress.setMaximum(pos_max)
                    self.file_progress.setValue(pos_max)
            elif "error" == status:
                message = f"Error with file {filename}"
                self.add_status_message(message)

    def ydl_postprocessor_hook(self, hook_dict: dict[str, Any]) -> None:
        """Callback function for postprocessing progress info

        Args:
            hook_dict (dict[str, Any]): Info about callback and file info
        """
        status = hook_dict.get("status", None)
        info_dict = hook_dict.get("info_dict", {})
        filename = info_dict.get("filename", "[UNKNOWN]")
        message = ""
        if "started" == status:
            message = f"Starting postprocessing of {filename}"
        elif "finished" == status:
            message = f"Finished postprocessing of {filename}"
        if message:
            self.add_status_message(message)

    def download_url_formats(self, url: str) -> None:
        """Download and display the formats avilable at url

        Args:
            url (str): URL to download format list from
        """

        message = f"Trying to retrieve format list for URL {url}"
        self.add_status_message(message)

        # Disable widgets that would interfere with processing
        self.enable_active_buttons(False)
        ydl_opts: dict[str, Any] = {}
        self.create_ydl_quiet_options(ydl_opts)
        ydl_opts["simulate"] = True

        # Perform data retrieval
        with YoutubeDL(ydl_opts) as ydl:
            try:
                meta = ydl.extract_info(url, download=False)
                if isinstance(meta, dict):
                    format_list = meta.get('formats', [meta])
                else:
                    message = "Data error in ydl metedata"
                    self.add_status_message(message)
                    return
            except utils.DownloadError as e:
                error_message = str(e)
                message = f"Download error: {error_message}"
                self.add_status_message(message)
                # Reenable widgets that would interfere with processing
                self.enable_active_buttons(True)
                return

            headers = ["ID", "Extension", "Audio codec", "Video codec",
                       "Resolution", "Bitrate", "Size", "Note"]
            table = DocTable("File formats", headers)

            for fmt in format_list:
                # Tuple is (key, is_numeric, suffix, linkId)
                keys: list[tuple[str, bool, str, str]] = \
                        [("format_id", False, "", LinkIds.LINKID_FORMATID),
                         ("ext", False, "", LinkIds.LINKID_FILEEXT),
                         # TODO - Implement audio and video codec links
                         # ("acodec", False, "", LinkIds.LINKID_AUDIOCODEC),
                         # ("vcodec", False, "", LinkIds.LINKID_VIDEOCODEC),
                         ("acodec", False, "", ""),
                         ("vcodec", False, "", ""),
                         ("resolution", False, "", LinkIds.LINKID_RESOLUTION),
                         ("tbr", True, " K/s", ""),
                         ("filesize", True, " bytes", ""),
                         ("format_note", False, "", "")]
                fields: list[tuple[str | list[str], str]] = []
                for key, is_numeric, suffix, linkid in keys:
                    text: str = ""
                    link: str = ""
                    if key in fmt and fmt[key]:
                        if is_numeric:
                            text = format(fmt[key], ',')
                        else:
                            text = fmt[key]
                        text += suffix
                        if linkid:
                            link = linkid + LinkIds.LINKID_SEP + text
                    fields.append((text, link))
                # Add fields to table
                table.add_row(fields)
            # Add table to status window
            self.status_text.append_html(table.to_html())

        # Reenable widgets that would interfere with processing
        self.enable_active_buttons(True)

    def download_subtitle_formats(self, url: str) -> None:
        """Downloads and displays subtitles available from url

        Args:
            url (str): URL of video
        """
        self.enable_active_buttons(False)
        message = f"Trying to retrieve subtitle list for URL {url}"
        self.add_status_message(message)

        ydl_opts: dict[str, Any] = {}
        self.create_ydl_quiet_options(ydl_opts)
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

            def parse_subs(self: MainWindow, dict_key: str,
                           sub_name: str) -> None:
                """Parses subtitle metadata

                Args:
                    dict_key (str): Dictionary key in meta name to parse
                    sub_name (str): Description of this subtitle
                """
                if not isinstance(meta, dict)\
                        or dict_key not in meta\
                        or not isinstance(meta[dict_key], dict)\
                        or not meta[dict_key]:
                    self.add_status_message("This video seems to contain no "
                                            f"{sub_name}.")
                else:
                    subtitles_list = meta[dict_key]
                    headers = ["Code", "Name", "Format"]
                    table = DocTable(sub_name, headers)
                    for key, value in subtitles_list.items():
                        fields: list[tuple[str | list[str], str]] = []
                        link = LinkIds.LINKID_SUBLANGUAGE + \
                            LinkIds.LINKID_SEP + key
                        fields.append((key, link))
                        extensions = []
                        name = ""
                        for sub in value:
                            name = sub["name"] if "name" in sub else ""
                            extensions.append(sub["ext"]
                                              if "ext" in sub else "")
                        fields.append((name, ""))
                        fields.append((extensions,
                                       LinkIds.LINKID_SUBEXTENSION))
                        table.add_row(fields)
                    # Add table to status window
                    self.status_text.append_html(table.to_html())

            parse_subs(self, "automatic_captions", "Auto-generated captions")
            parse_subs(self, "subtitles", "Subtitles")
        self.enable_active_buttons(True)
        # Restore focus to clicked button which got disabled and lost focus
        self.list_subs_button.setFocus()

    def add_status_message(self, message: str) -> None:
        """Adds text to the status window and scrolls to the bottom

        Args:
            message (str): Message text to add
        """
        # Output to console
        if self.consoleoutput_check.isChecked():
            print(message)
        # Add text to status window
        self.status_text.append_text(message)
        # Drive message loop
        QApplication.processEvents()

    def enable_active_buttons(self, enable: bool) -> None:
        """Enables or disables widgets while downloading is in progress

        Args:
            enable (bool): Enable widgets flag
        """
        widgets: list[QWidget] = [self.list_formats_button,
                                  self.list_subs_button,
                                  self.bottom_buttonbox]
        for widget in widgets:
            widget.setEnabled(enable)
