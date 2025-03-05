#!/usr/bin/env python3

"""video_download.py - Download videos or lists of videos
including bookmarks exported from browsers from video sites
like YouTube, Vimeo, Instagram, etc using the yt_dlp Python package.

Author: Josh Buchbinder
"""

__author__ = "Josh Buchbinder"
__copyright__ = "Copyright 2024, Josh Buchbinder"
__version__ = "1.0.0"

import sys
import argparse
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from constants import AppConst, ComboBoxConst, ToolTips, StringMaps
from main_window import MainWindow


def create_parserer() -> argparse.ArgumentParser:
    """ Creates and populates the argparse.ArgumentParser

    Returns:
        argparse.ArgumentParser: Populated parser object
    """

    # Build argparse.ArgumentParser
    parser = argparse.ArgumentParser(
        description=AppConst.HELP_DESCRIPTION, epilog=AppConst.HELP_EPILOG,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-v", "--version", action="version",
                        version=__version__)
    url_group = parser.add_mutually_exclusive_group()
    url_group.add_argument("--url", help=ToolTips.TTT_URL_TEXT)
    url_group.add_argument("--urllist", help=ToolTips.TTT_LIST_PATH_TEXT)
    parser.add_argument("--ffmpegpath", help=ToolTips.TTT_FFMPEG_PATH_TEXT)
    parser.add_argument("-u", "--username", help=ToolTips.TTT_USERNAME_TEXT)
    parser.add_argument("-p", "--password", help=ToolTips.TTT_PASSWORD_TEXT)
    format_group = parser.add_mutually_exclusive_group()
    format_group.add_argument("--format", action="store_true",
                              help=ToolTips.TTT_SPECIFYFORMAT_CHECK)
    format_group.add_argument("--noformat", action="store_true",
                              help="Do not specify format download options.")
    resolution_group = parser.add_mutually_exclusive_group()
    resolution_group.add_argument("--resolution", action="store_true",
                                  help=ToolTips.TTT_SPECIFYRES_CHECK)
    resolution_group.add_argument("--noresolution", action="store_true",
                                  help="Do not specify resolution options.")
    subtitles_group = parser.add_mutually_exclusive_group()
    subtitles_group.add_argument("--subtitles", action="store_true",
                                 help=ToolTips.TTT_DOWNLOADSUBS_CHECK)
    subtitles_group.add_argument("--nosubtitles", action="store_true",
                                 help="Do not download subtitles.")
    overwrite_group = parser.add_mutually_exclusive_group()
    overwrite_group.add_argument("-o", "--overwrite", action="store_true",
                                 help=ToolTips.TTT_OVERWRITE_CHECK)
    overwrite_group.add_argument("--nooverwrite", action="store_true",
                                 help="Do not overwrite existing files when "
                                 "downloading.")
    keepfiles_group = parser.add_mutually_exclusive_group()
    keepfiles_group.add_argument("-k", "--keepfiles", action="store_true",
                                 help=ToolTips.TTT_KEEPFILES_CHECK)
    keepfiles_group.add_argument("--nokeepfiles", action="store_true",
                                 help="Do not keep temporary files.")
    preferfree_group = parser.add_mutually_exclusive_group()
    preferfree_group.add_argument("--preferfree", action="store_true",
                                  help=ToolTips.TTT_PREFERFREEFORMATS_CHECK)
    preferfree_group.add_argument("--nopreferfree", action="store_true",
                                  help="Do not prefer free media formats.")
    consoleout_group = parser.add_mutually_exclusive_group()
    consoleout_group.add_argument("--consoleout", action="store_true",
                                  help=ToolTips.TTT_CONSOLEOUTPUT_CHECK)
    consoleout_group.add_argument("--noconsoleout", action="store_true",
                                  help="Do not output to console.")
    formattype_list = [item[2] for item in ComboBoxConst.FORMAT_TYPE_LIST]
    parser.add_argument("--formattype", choices=formattype_list,
                        help=ToolTips.TTT_FORMAT_TYPE_COMBO)
    max_quality = len(ComboBoxConst.FORMAT_LABELS_QUALITY_LIST)
    parser.add_argument("--quality", type=int,
                        choices=range(1, max_quality + 1),
                        help="Quality level, 1 is best 2 is second best, etc.")
    parser.add_argument("--videoextension",
                        choices=ComboBoxConst.FORMAT_EXT_VID_LIST,
                        help=ToolTips.TTT_FORMAT_VIDEXT_COMBO)
    parser.add_argument("--audioextension",
                        choices=ComboBoxConst.FORMAT_EXT_AUD_LIST,
                        help=ToolTips.TTT_FORMAT_AUDEXT_COMBO)
    vidcodec_list = [codec for _, codec in ComboBoxConst.FORMAT_CODEC_VID_LIST]
    parser.add_argument("--videocodec",
                        choices=vidcodec_list,
                        help=ToolTips.TTT_FORMAT_VIDCODEC_COMBO)
    parser.add_argument("--audiocodec",
                        choices=ComboBoxConst.FORMAT_CODEC_AUD_LIST,
                        help=ToolTips.TTT_FORMAT_AUDCODEC_COMBO)
    mergeaudio_list = [val for _, _, val in
                       ComboBoxConst.FORMAT_MERGE_AUD_LIST]
    parser.add_argument("--mergeaudio", choices=mergeaudio_list,
                        help=ToolTips.TTT_FORMAT_MERGE_AUDIO_COMBO)
    mergevideo_list = [val for _, _, val in
                       ComboBoxConst.FORMAT_MERGE_VID_LIST]
    parser.add_argument("--mergevideo", choices=mergevideo_list,
                        help=ToolTips.TTT_FORMAT_MERGE_VIDEO_COMBO)
    parser.add_argument("--mergecontainer",
                        choices=ComboBoxConst.FORMAT_MERGE_OUTPUT_LIST,
                        help=ToolTips.TTT_FORMAT_MARGE_CONTAINER_COMBO)
    parser.add_argument("--rawformatstring",
                        help=ToolTips.TTT_FORMAT_STRING_TEXT)
    resheight_list = [item[1] for item in ComboBoxConst.FORMAT_RESOLUTION_LIST]
    parser.add_argument("--maxheight", type=int, choices=resheight_list,
                        help=ToolTips.TTT_RESOLUTION_COMBO)
    subtype_group = parser.add_mutually_exclusive_group()
    subtype_group.add_argument("--subsgenerated", action="store_true",
                               help=ToolTips.TTT_SUBSGENERATED_CHECK)
    subtype_group.add_argument("--subssupplied", action="store_true",
                               help="Download user supplied subtitles.")
    submerge_group = parser.add_mutually_exclusive_group()
    submerge_group.add_argument("--subsmerge", action="store_true",
                                help=ToolTips.TTT_SUBS_MERGE_CHECK)
    submerge_group.add_argument("--nosubsmerge", action="store_true",
                                help="Do not merge subtitles into media file.")
    lang_codes = [item[1] for item in ComboBoxConst.SUBTITLES_LANGUAGES_LIST]
    parser.add_argument("--subslangs", nargs="+", default=[],
                        choices=lang_codes,
                        help="Language codes for subtitles to download.")
    parser.add_argument("--subsformat",
                        choices=ComboBoxConst.SUBTITLES_DOWNFMT_LIST,
                        help=ToolTips.TTT_SUBS_FORMAT_COMBO)
    subscvt_list = [item[1] for item in ComboBoxConst.SUBTITLES_CNVTFMT_LIST]
    parser.add_argument("--subsconvert", choices=subscvt_list,
                        help=ToolTips.TTT_SUBS_CONVERT_COMBO)
    parser.add_argument("--subsdelay", type=int,
                        help=ToolTips.TTT_SUBS_DELAY_SPIN)
    parser.add_argument("--noloadsettings", action="store_true",
                        help="Do not load stored settings at startup. "
                        "This will restore GUI settings to default.")
    parser.add_argument("--nosavesettings", action="store_true",
                        help="Do not save GUI settings on exit. "
                        "This will make this session's settings temporary.")
    parser.add_argument("--guistyle", default="fusion",
                        choices=["windows", "windowsvista", "fusion", "macos"],
                        help="Qt GUI style to use, default=fusion.")
    parser.add_argument("--qtarg", action="append", default=[],
                        help="Pass argument(s) to Qt engine. "
                        "Can be used more than once.")
    parser.add_argument("-d", "--download", action="store_true",
                        help=ToolTips.TTT_DOWNLOAD_BUTTON)
    parser.add_argument("-e", "--exitoncompletion", action="store_true",
                        help="Exit after download is attempted.")
    # parser.add_argument("--nogui", action="store_true",
    #                     help="Do not display GUI window.")
    return parser


def main(argv: list[str]) -> int:
    """ Main function entry point

    Args:
        argv (list[str]): Command line arguments

    Returns:
        int: exit() value
    """

    # Create argument parser
    parser = create_parserer()
    # Parse command line arguments
    args = parser.parse_args(argv[1:])

    # Create application
    app = QApplication(args.qtarg)

    # Use Fusion app style
    app.setStyle(args.guistyle)

    # Create window
    window = MainWindow(not args.noloadsettings, not args.nosavesettings)

    # Set arguments in GUI
    if args.url:
        window.url_type_combo.setCurrentIndex(ComboBoxConst.URL_TYPE_SINGLE)
        window.url_text.setText(args.url)
    elif args.urllist:
        window.url_type_combo.setCurrentIndex(ComboBoxConst.URL_TYPE_LIST)
        window.list_path_text.setText(args.urllist)
    if args.ffmpegpath:
        window.ffmpeg_path_text.setText(args.ffmpegpath)
    if args.username:
        window.username_text.setText(args.username)
    if args.password:
        window.password_text.setText(args.password)
    if args.format:
        window.specifyformat_check.setChecked(True)
    elif args.noformat:
        window.specifyformat_check.setChecked(False)
    if args.resolution:
        window.specifyres_check.setChecked(True)
    elif args.noresolution:
        window.specifyres_check.setChecked(False)
    if args.overwrite:
        window.overwrite_check.setChecked(True)
    elif args.nooverwrite:
        window.overwrite_check.setChecked(False)
    if args.keepfiles:
        window.keepfiles_check.setChecked(True)
    elif args.nokeepfiles:
        window.keepfiles_check.setChecked(False)
    if args.consoleout:
        window.consoleoutput_check.setChecked(True)
    elif args.noconsoleout:
        window.consoleoutput_check.setChecked(False)
    if args.formattype:
        window.format_type_combo.set_current_data(
            StringMaps.STRINGMAP_FORMATTYPE[args.formattype])
    if args.quality:
        window.format_quality_combo.setCurrentIndex(args.quality - 1)
    if args.videoextension:
        window.format_vidext_combo.set_current_data(args.videoextension)
    if args.audioextension:
        window.format_audext_combo.set_current_data(args.audioextension)
    if args.videocodec:
        window.format_vidcodec_combo.set_current_data(args.videocodec)
    if args.audiocodec:
        window.format_audcodec_combo.set_current_data(args.audiocodec)
    if args.mergeaudio:
        window.format_merge_audio_combo.set_current_data(
            StringMaps.STRINGMAP_MERGEAUDIO[args.mergeaudio])
    if args.mergevideo:
        window.format_merge_video_combo.set_current_data(
            StringMaps.STRINGMAP_MERGEVIDEO[args.mergevideo])
    if args.mergecontainer:
        window.format_marge_container_combo.setCurrentText(args.mergecontainer)
    if args.rawformatstring:
        window.format_string_text.setText(args.rawformatstring)
    if args.maxheight:
        window.resheight_combo.set_current_data(args.maxheight)
    if args.subsgenerated:
        window.subsgenerated_check.setChecked(True)
    elif args.subssupplied:
        window.subsgenerated_check.setChecked(False)
    if args.subsmerge:
        window.subs_merge_check.setChecked(True)
    elif args.nosubsmerge:
        window.subs_merge_check.setChecked(False)
    if args.subslangs:
        window.subs_lang_combo.check_all(False)
        window.subs_lang_combo.check_items_by_data(args.subslangs, True)
    if args.subsformat:
        window.subs_format_combo.set_current_text(args.subsformat)
    if args.subsconvert is not None:
        window.subs_cnvt_combo.set_current_data(args.subsconvert)
    if args.subsdelay is not None:
        window.subs_delay_spin.setValue(args.subsdelay)

    # Show the main window
    window.show()

    # Trigger the download
    if args.download:
        window.exit_on_completion = args.exitoncompletion
        QTimer.singleShot(0, window, window.download_button_clicked)

    # Execute event loop
    return app.exec()


# Entry point
if __name__ == "__main__":
    sys.exit(main(sys.argv))
