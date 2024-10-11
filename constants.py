#!/usr/bin/env python3

"""constants.py - Constants used by video_download.py

Author: Josh Buchbinder
"""

__author__ = "Josh Buchbinder"
__copyright__ = "Copyright 2024, Josh Buchbinder"

from typing import Any, TYPE_CHECKING
from PySide6.QtWidgets import QWidget
if TYPE_CHECKING:
    from video_download import MainWindow


class AppConst:
    """Various strings
    """
    # Monospace font name used for status window text
    FONT_NAME_STATUSWINDOW = "Monospace"
    # URL for format string help
    URL_HELP_FORMATSELECTION = "https://github.com/yt-dlp/yt-dlp/blob/"\
        "master/README.md#format-selection"
    # Regex to strip color codes from string
    REGEX_COLORSTRIP = r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]'
    # Regex for escape sequences
    REGEX_ESCAPESEQ = r"(\x1B\[([\d;]+)m)"
    # URL list file extensions
    EXTENSIONS_URLLIST = ["html", "txt"]
    # Format string for file progress bar
    FORMATSTR_FILEPROGRESS = "%vMb/%mMb %p%"
    # Format string for total progress bar
    FORMATSTR_TOTALPROGRESS = "%v/%m"


class SettingsConst:
    """Keys for loading/saving settings
    """
    SETTINGS_COMPANYNAME = "MySoft"
    SETTINGS_APPNAME = "Youtube-Download"
    SETTINGS_VAL_URLTYPE = "UrlType"
    SETTINGS_VAL_URLTEXT = "UrlText"
    SETTINGS_VAL_URLLIST = "UrlList"
    SETTINGS_VAL_DOWNLOADPATH = "DownloadPath"
    SETTINGS_VAL_FFMPEGPATH = "FfmpegPath"
    SETTINGS_VAL_USERNAME = "Username"
    SETTINGS_VAL_PASSWORD = "Password"
    SETTINGS_VAL_SPECIFYFORMAT = "SpecifyFormat"
    SETTINGS_VAL_SPECIFYRES = "SpecifyResolution"
    SETTINGS_VAL_DOWNLOADSUBTITLES = "DownloadSubtitles"
    SETTINGS_VAL_AUTOSCROLLSTATUS = "AutoScrollStatus"
    SETTINGS_VAL_OVERWRITE = "Overwrite"
    SETTINGS_VAL_KEEPFILES = "KeepFiles"
    SETTINGS_VAL_CONSOLEOUTPUT = "ConsoleOutput"
    SETTINGS_VAL_PREFERFREEFORMATS = "PreferFreeFormats"
    SETTINGS_VAL_SUBTITLEFORMAT = "SubtitleFormat"
    SETTINGS_VAL_SUBTITLECONVERT = "SubtitleConvert"
    SETTINGS_VAL_SUBTITLEMERGE = "SubtitleMerge"
    SETTINGS_VAL_AUTOGENSUBS = "SubtitlesGenerated"
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
    SETTINGS_VAL_FORMATMERGECONTAINER = "FormatMergeContainer"
    SETTINGS_VAL_FORMATSTRING = "FormatString"
    SETTINGS_VAL_RESHEIGHT = "ResolutionHeight"
    SETTINGS_VAL_WINDOWSTATE = "WindowState"
    SETTINGS_VAL_WINDOWWIDTH = "WindowWidth"
    SETTINGS_VAL_WINDOWHEIGHT = "WindowHeight"

    @staticmethod
    def get_mainwindow_widgets_vals(mainwindow: 'MainWindow') -> list[
            tuple[QWidget, str, Any]]:
        """Returns list of widgets and their associated settings key string
            and their default values

        Returns:
            list[tuple[QWidget, str, Any]]: [(Widget, settings key, default)]
        """

        return [
            (mainwindow.url_type_combo,
                SettingsConst.SETTINGS_VAL_URLTYPE, ""),
            (mainwindow.url_text,
                SettingsConst.SETTINGS_VAL_URLTEXT, ""),
            (mainwindow.list_path_text,
                SettingsConst.SETTINGS_VAL_URLLIST, ""),
            (mainwindow.download_path_text,
                SettingsConst.SETTINGS_VAL_DOWNLOADPATH, ""),
            (mainwindow.ffmpeg_path_text,
                SettingsConst.SETTINGS_VAL_FFMPEGPATH, ""),
            (mainwindow.username_text,
                SettingsConst.SETTINGS_VAL_USERNAME, ""),
            (mainwindow.password_text,
                SettingsConst.SETTINGS_VAL_PASSWORD, ""),
            (mainwindow.specifyformat_check,
                SettingsConst.SETTINGS_VAL_SPECIFYFORMAT, False),
            (mainwindow.specifyres_check,
                SettingsConst.SETTINGS_VAL_SPECIFYRES, False),
            (mainwindow.resolution_combo,
                SettingsConst.SETTINGS_VAL_RESHEIGHT, ""),
            (mainwindow.downloadsubs_check,
                SettingsConst.SETTINGS_VAL_DOWNLOADSUBTITLES, False),
            (mainwindow.autoscroll_check,
                SettingsConst.SETTINGS_VAL_AUTOSCROLLSTATUS, True),
            (mainwindow.overwrite_check,
                SettingsConst.SETTINGS_VAL_OVERWRITE, False),
            (mainwindow.keepfiles_check,
                SettingsConst.SETTINGS_VAL_KEEPFILES, False),
            (mainwindow.preferfreeformats_check,
                SettingsConst.SETTINGS_VAL_PREFERFREEFORMATS, False),
            (mainwindow.consoleoutput_check,
                SettingsConst.SETTINGS_VAL_CONSOLEOUTPUT, False),
            (mainwindow.generatedsubs_check,
                SettingsConst.SETTINGS_VAL_AUTOGENSUBS, False),
            (mainwindow.subs_lang_combo,
                SettingsConst.SETTINGS_VAL_SUBTITLELANGUAGE, ""),
            (mainwindow.subs_cnvt_combo,
                SettingsConst.SETTINGS_VAL_SUBTITLECONVERT, ""),
            (mainwindow.subs_merge_check,
                SettingsConst.SETTINGS_VAL_SUBTITLEMERGE, False),
            (mainwindow.subs_format_combo,
                SettingsConst.SETTINGS_VAL_SUBTITLEFORMAT, ""),
            (mainwindow.subs_delay_spin,
                SettingsConst.SETTINGS_VAL_SUBTITLEDELAY, 0),
            (mainwindow.format_type_combo,
                SettingsConst.SETTINGS_VAL_FORMATTYPE, ""),
            (mainwindow.format_quality_combo,
                SettingsConst.SETTINGS_VAL_FORMATQUALITY, ""),
            (mainwindow.format_audext_combo,
                SettingsConst.SETTINGS_VAL_FORMATAUDEXT, ""),
            (mainwindow.format_vidext_combo,
                SettingsConst.SETTINGS_VAL_FORMATVIDEXT, ""),
            (mainwindow.format_audcodec_combo,
                SettingsConst.SETTINGS_VAL_FORMATAUDCODEC, ""),
            (mainwindow.format_vidcodec_combo,
                SettingsConst.SETTINGS_VAL_FORMATVIDCODEC, ""),
            (mainwindow.format_merge_audio_combo,
                SettingsConst.SETTINGS_VAL_FORMATMERGEAUD, ""),
            (mainwindow.format_merge_video_combo,
                SettingsConst.SETTINGS_VAL_FORMATMERGEVID, ""),
            (mainwindow.format_marge_container_combo,
                SettingsConst.SETTINGS_VAL_FORMATMERGECONTAINER, ""),
            (mainwindow.format_string_text,
                SettingsConst.SETTINGS_VAL_FORMATSTRING, "")]


class ComboBoxConst:
    """String lists to populate combo boxes and their indexes
    """
    URL_TYPE_LABELS = ["Single URL:", "URL List:"]
    URL_TYPE_SINGLE = 0
    URL_TYPE_LIST = 1

    SUBTITLES_DOWNFMT_LIST = ["vtt", "ttml", "srv3", "srv2", "srv1", "json3"]
    SUBTITLES_CNVTFMT_LIST = [
        ("None", ""),
        ("ASS (Advanced SSA)", "ass"),
        ("HDMV Text", "hdmv_text_subtitle"),
        ("LRC Lyrics", "lrc"),
        ("SRT SubRip", "srt"),
        ("SSA (SubStation Alpha)", "ssa")]
    SUBTITLES_LANGUAGES_LIST = [
        ("Afrikaans (af)", "af"), ("Akan (ak)", "ak"), ("Albanian (sq)", "sq"),
        ("Amharic (am)", "am"), ("Arabic (ar)", "ar"), ("Armenian (hy)", "hy"),
        ("Assamese (as)", "as"), ("Aymara (ay)", "ay"),
        ("Azerbaijani (az)", "az"), ("Bangla (bn)", "bn"),
        ("Basque (eu)", "eu"), ("Belarusian (be)", "be"),
        ("Bhojpuri (bho)", "bho"), ("Bosnian (bs)", "bs"),
        ("Bulgarian (bg)", "bg"), ("Burmese (my)", "my"),
        ("Catalan (ca)", "ca"), ("Cebuano (ceb)", "ceb"),
        ("Chinese (Simplified) (zh-Hans)", "zh-Hans"),
        ("Chinese (Traditional) (zh-Hant)", "zh-Hant"),
        ("Corsican (co)", "co"), ("Croatian (hr)", "hr"), ("Czech (cs)", "cs"),
        ("Danish (da)", "da"), ("Divehi (dv)", "dv"), ("Dutch (nl)", "nl"),
        ("English (Original) (en-orig)", "en-orig"), ("English (en)", "en"),
        ("English (United States)", "en-US"),
        ("Esperanto (eo)", "eo"), ("Estonian (et)", "et"), ("Ewe (ee)", "ee"),
        ("Filipino (fil)", "fil"), ("Finnish (fi)", "fi"),
        ("French (fr)", "fr"), ("Galician (gl)", "gl"), ("Ganda (lg)", "lg"),
        ("Georgian (ka)", "ka"), ("German (de)", "de"), ("Greek (el)", "el"),
        ("Guarani (gn)", "gn"), ("Gujarati (gu)", "gu"),
        ("Haitian Creole (ht)", "ht"), ("Hausa (ha)", "ha"),
        ("Hawaiian (haw)", "haw"), ("Hebrew (iw)", "iw"),
        ("Hindi (hi)", "hi"), ("Hmong (hmn)", "hmn"),
        ("Hungarian (hu)", "hu"), ("Icelandic (is)", "is"),
        ("Igbo (ig)", "ig"), ("Indonesian (id)", "id"), ("Irish (ga)", "ga"),
        ("Italian (it)", "it"), ("Japanese (ja)", "ja"),
        ("Javanese (jv)", "jv"), ("Kannada (kn)", "kn"),
        ("Kazakh (kk)", "kk"), ("Khmer (km)", "km"),
        ("Kinyarwanda (rw)", "rw"), ("Korean (ko)", "ko"),
        ("Krio (kri)", "kri"), ("Kurdish (ku)", "ku"), ("Kyrgyz (ky)", "ky"),
        ("Lao (lo)", "lo"), ("Latin (la)", "la"), ("Latvian (lv)", "lv"),
        ("Lingala (ln)", "ln"), ("Lithuanian (lt)", "lt"),
        ("Luxembourgish (lb)", "lb"), ("Macedonian (mk)", "mk"),
        ("Malagasy (mg)", "mg"), ("Malay (ms)", "ms"),
        ("Malayalam (ml)", "ml"), ("Maltese (mt)", "mt"), ("Māori (mi)", "mi"),
        ("Marathi (mr)", "mr"), ("Mongolian (mn)", "mn"),
        ("Nepali (ne)", "ne"), ("Northern Sotho (nso)", "nso"),
        ("Norwegian (no)", "no"), ("Nyanja (ny)", "ny"), ("Odia (or)", "or"),
        ("Oromo (om)", "om"), ("Pashto (ps)", "ps"), ("Persian (fa)", "fa"),
        ("Polish (pl)", "pl"), ("Portuguese (pt)", "pt"),
        ("Punjabi (pa)", "pa"), ("Quechua (qu)", "qu"),
        ("Romanian (ro)", "ro"), ("Russian (ru)", "ru"),
        ("Samoan (sm)", "sm"), ("Sanskrit (sa)", "sa"),
        ("Scottish Gaelic (gd)", "gd"), ("Serbian (sr)", "sr"),
        ("Shona (sn)", "sn"), ("Sindhi (sd)", "sd"), ("Sinhala (si)", "si"),
        ("Slovak (sk)", "sk"), ("Slovenian (sl)", "sl"),
        ("Somali (so)", "so"), ("Southern Sotho (st)", "st"),
        ("Spanish (es)", "es"), ("Sundanese (su)", "su"),
        ("Swahili (sw)", "sw"), ("Swedish (sv)", "sv"),
        ("Tajik (tg)", "tg"), ("Tamil (ta)", "ta"), ("Tatar (tt)", "tt"),
        ("Telugu (te)", "te"), ("Thai (th)", "th"), ("Tigrinya (ti)", "ti"),
        ("Tsonga (ts)", "ts"), ("Turkish (tr)", "tr"),
        ("Turkmen (tk)", "tk"), ("Ukrainian (uk)", "uk"), ("Urdu (ur)", "ur"),
        ("Uyghur (ug)", "ug"), ("Uzbek (uz)", "uz"),
        ("Vietnamese (vi)", "vi"), ("Welsh (cy)", "cy"),
        ("Western Frisian (fy)", "fy"), ("Xhosa (xh)", "xh"),
        ("Yiddish (yi)", "yi"), ("Yoruba (yo)", "yo"), ("Zulu (zu)", "zu")]

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
    FORMAT_MERGE_OUTPUT_LIST = ["mkv", "mp4", "webm"]

    FORMAT_RESOLUTION_LIST = [("8K (4320)", 4320),
                              ("UHD (2160)", 2160),
                              ("QHD (1440)", 1440),
                              ("FHD (1080)", 1080),
                              ("HD (720)", 720),
                              ("SD (480)", 480),
                              ("360", 360),
                              ("240", 240),
                              ("144", 144)]


class ToolTips:
    """Strings for widgt tooltips
    """
    # ToolTip text for widgets
    TTT_URL_TYPE_COMBO = "Select either a single URL to download or a URL list"
    TTT_URL_TEXT = "The URL of a page with a video to download"
    TTT_LIST_FORMATS_BUTTON = "Retrieve the list of video and audio formats " \
        "available for this URL."
    TTT_LIST_PATH_TEXT = "The path to the list of URLs to download"
    TTT_LIST_PATH_BROSE_BUTTON = "Use dialog to browse to URL list path"
    TTT_DOWNLOAD_PATH_TEXT = "The path to the directory to download videos " \
        "into"
    TTT_DOWNLOAD_PATH_BROWSE_BUTTON = "Use dialog to browse to download " \
        "directory"
    TTT_FFMPEG_PATH_TEXT = "Path to directory containing ffmpeg and ffprobe " \
        "binaries.\nffmpeg is only required if you select format options " \
        "that require post processing."
    TTT_FFMPEG_PATH_BROWSE_BUTTON = "Use dialog to browse to ffmpeg directory"
    TTT_USERNAME_TEXT = "User name for authentication"
    TTT_PASSWORD_TEXT = "Password for authentication"
    TTT_SPECIFYFORMAT_CHECK = "Specify the format(s) to download and " \
        "optionally merge.\nIf unchecked the highest quality format with " \
        "audio and video will be downloaded.\nThis might not be as high " \
        "quality as specifying to merge\nthe best audio only and video only " \
        "formats."
    TTT_SPECIFYRES_CHECK = "Specify the maximum video resolution height " \
        "to download.\nIf not checked, the highest resolution video will " \
        "be downloaded."
    TTT_RESOLUTION_COMBO = "Select the highest resolution to download.\n" \
        "The highest resolution below or equal to this will be downloaded."
    TTT_DOWNLOADSUBS_CHECK = "Download subtitles with video.\nMore options " \
        "will be revealed when checked."
    TTT_AUTOSCROLL_CHECK = "When checked, status window automatically " \
        "scrolls to the bottom when new text is added."
    TTT_OVERWRITE_CHECK = "Overwrite video files if they exist when " \
        "downloading."
    TTT_KEEPFILES_CHECK = "Keep media files after post processing."
    TTT_PREFERFREEFORMATS_CHECK = "Whether to prefer video formats with " \
        "free containers over non-free ones of same quality."
    TTT_CONSOLEOUTPUT_CHECK = "The yt_dlp library will output to the " \
        "console that launched this program.\nUseful for debugging."
    TTT_GENERATEDSUBS_CHECK = "Download automatically generated caption " \
        "text.\nIf unchecked, user supplied subtitles will be downloaded " \
        "if available."
    TTT_SUBS_LANG_COMBO = "The languages of subtitles to download.\nThe " \
        "languages must be available from the server."
    TTT_SUBS_CLEAR_BUTTON = "Clears all checked subtitle languages."
    TTT_SUBS_FORMAT_COMBO = "The destination subtitle format.\nSome formats " \
        "will be converted."
    TTT_SUBS_CONVERT_COMBO = "The optional format to convert the downloaded " \
        "subtitles to."
    TTT_SUBS_MERGE_CHECK = "Merge subtitles into output video file."
    TTT_SUBS_DELAY_SPIN = "The delay in seconds between subtitle " \
        "retrievals.\nIf too many download requests happen too quickly, \n" \
        "some sites will abort the activity."
    TTT_LIST_SUBS_BUTTON = "Attempt to retrieve a list of available " \
        "subtitles from the server."
    TTT_FORMAT_TYPE_COMBO = "Select which method of format selection to use."
    TTT_FORMAT_QUALITY_COMBO = "Select the quality level to download.\n" \
        "Different quality levels may result in different file types.\n" \
        "Not all quality levels may be available."
    TTT_FORMAT_AUDEXT_COMBO = "Select the audio file extension to " \
        "download. This does not guarantee a specific codec.\nDifferent " \
        "sites will have different file types\navailable and may not offer " \
        "all types."
    TTT_FORMAT_VIDEXT_COMBO = "Select the video file extension to " \
        "download.\nThis does not guarantee a specific codec.\n" \
        "Different sites will have different file types available " \
        "and may not offer all types."
    TTT_FORMAT_AUDCODEC_COMBO = "Select the audio codec to download.\n" \
        "Different sites will have different audio codecs available and " \
        "may not offer all types."
    TTT_FORMAT_VIDCODEC_COMBO = "Select the video codec to download.\n" \
        "Different sites will have different video codecs available and " \
        "may not offer all types."
    TTT_FORMAT_MERGE_AUDIO_COMBO = "The audio format or formats to be " \
        "combined into the output file.\nffmpeg is required."
    TTT_FORMAT_MERGE_VIDIO_COMBO = "The video format or formats to be " \
        "combined into the output file.\nffmpeg is required."
    TTT_FORMAT_MARGE_CONTAINER_COMBO = "The output format for the merged " \
        "video file.\nffmpeg is required."
    TTT_FORMAT_STRING_TEXT = "Enter the string representing the format to " \
        "download.\nClick the Help button for more information on format " \
        "strings.\nYou can also use the `List format` button and specify " \
        "the ID of a specific format listed in the table."
    TTT_FORMAT_STRING_HELP_BUTTON = "Launches a browser directed to " \
        "detailed information about creating yt-dlp format strings."
    TTT_STATUSWINDOW_TEXT = "This window shows status text.\nYou can " \
        "pinch and zoom the text in this window or\nhold ctrl and use the " \
        "mouse wheel to change the zoom factor,\nand copy text by dragging " \
        "and then pressing CTRL-C.\nClicking on a blue link will change " \
        "download options."
    TTT_CLOSE_BUTTON = "Close this window."
    TTT_DOWNLOAD_BUTTON = "Begin downloading and processing " \
        "files."
    # ToolTip text for links in the status window
    TTT_LINK_STATUSWINDOW_FMTID = "Click here to change format selection " \
        "options to\ndownload this specific format ID."
    TTT_LINK_STATUSWINDOW_FILEEXT = "Click here to change format selection " \
        "options to\nAudio+Video by extension and to download this file " \
        "extension."
    TTT_LINK_STATUSWINDOW_AUDIOCODEC = ""
    TTT_LINK_STATUSWINDOW_VIDEOCODEC = ""
    TTT_LINK_STATUSWINDOW_SUBLANGUAGE = "Click here to check this language " \
        "\nin the languages list of subtitles options."
    TTT_LINK_STATUSWINDOW_SUBEXTENSION = "Click here to change the the " \
        "download format\nin the subtitles options."
    TTT_LINK_STATUSWINDOW_RESOLUTION = "Click here to change Max resolution " \
        "option to\ndownload no higher than this resolution."


class LinkIds:
    """String constants for link IDs
    """
    LINKID_SEP = ":"
    LINKID_FORMATID = "formatid"
    LINKID_FILEEXT = "vidextension"
    LINKID_AUDIOCODEC = "audiocodec"
    LINKID_VIDEOCODEC = "videocodec"
    LINKID_SUBLANGUAGE = "sublanguage"
    LINKID_SUBEXTENSION = "subextension"
    LINKID_RESOLUTION = "resolution"


class StringMaps:
    """String maps
    """
    # Map of link IDs to their tooltips in the status window
    STRINGMAP_LINKID_TOOLTIP = {
        LinkIds.LINKID_FORMATID: ToolTips.TTT_LINK_STATUSWINDOW_FMTID,
        LinkIds.LINKID_FILEEXT: ToolTips.TTT_LINK_STATUSWINDOW_FILEEXT,
        LinkIds.LINKID_AUDIOCODEC: ToolTips.TTT_LINK_STATUSWINDOW_AUDIOCODEC,
        LinkIds.LINKID_VIDEOCODEC: ToolTips.TTT_LINK_STATUSWINDOW_VIDEOCODEC,
        LinkIds.LINKID_SUBLANGUAGE: ToolTips.TTT_LINK_STATUSWINDOW_SUBLANGUAGE,
        LinkIds.LINKID_SUBEXTENSION:
        ToolTips.TTT_LINK_STATUSWINDOW_SUBEXTENSION,
        LinkIds.LINKID_RESOLUTION: ToolTips.TTT_LINK_STATUSWINDOW_RESOLUTION}
