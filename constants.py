#!/usr/bin/env python3

"""constants.py - Constants used by video_download.py

Author: Josh Buchbinder
"""

__author__ = "Josh Buchbinder"
__copyright__ = "Copyright 2024, Josh Buchbinder"


class AppConst:
    """Various strings
    """
    # Monospace font name used for status window text
    MONOSPACE_FONT_NAME = "Monospace"
    # URL for format string help
    FORMAT_STRING_HELP_URL = "https://github.com/yt-dlp/yt-dlp/blob/"\
        "master/README.md#format-selection"
    # Regex to strip color codes from string
    REGEX_COLORSTRIP = r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]'
    # URL list file extensions
    URLLIST_EXTENSIONS = ["html", "txt"]


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
    SETTINGS_VAL_OVERWRITE = "Overwrite"
    SETTINGS_VAL_KEEPVIDEO = "KeepVideo"
    SETTINGS_VAL_CONSOLEOUTPUT = "ConsoleOutput"
    SETTINGS_VAL_PREFERFREEFORMATS = "PreferFreeFormats"
    SETTINGS_VAL_SUBTITLEFORMAT = "SubtitleFormat"
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
    SETTINGS_VAL_WINDOWWIDTH = "WindowWidth"
    SETTINGS_VAL_WINDOWHEIGHT = "WindowHeight"


class ComboBoxConst:
    """String lists to populate combo boxes and their indexes
    """
    URL_TYPE_LABELS = ["Single URL:", "URL List:"]
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
    TTT_OVERWRITE_CHECK = "Overwrite video files if they exist when " \
        "downloading"
    TTT_KEEPVIDEO_CHECK = "Keep media files after post processing"
    TTT_PREFERFREEFORMATS_CHECK = "Whether to prefer video formats with " \
        "free containers over non-free ones of same quality"
    TTT_CONSOLEOUTPUT_CHECK = "The yt_dlp library will output to the " \
        "console that launched this program.\nUseful for debugging."
    TTT_GENERATEDSUBS_CHECK = "Download auto-generated caption text.\nIf" \
        "unchecked, actual subtitles will be downloaded."
    TTT_SUBS_LANG_COMBO = "The languages of subtitles to download.\nThe " \
        "languages must be available from the server."
    TTT_SUBS_CLEAR_BUTTON = "Clears all checked subtitle languages."
    TTT_SUBS_FORMAT_COMBO = "The destination subtitle format.\nSome formats " \
        "will be converted."
    TTT_SUBS_DELAY_SPIN = "The delay in seconds between subtitle " \
        "retrieval.\nIf too many download requests happen too quickly,\n" \
        "some sites will abort the activity."
    TTT_LIST_SUBS_BUTTON = "Attempt to retrieve a list of available " \
        "subtitles from the server."
    TTT_FORMAT_TYPE_COMBO = "Select which method of format selection to use"
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
    TTT_STATUS_TEXT = "This window shows status text.\nYou can pinch and " \
        "zoom the text in this window or\nhold ctrl and use the mouse wheel " \
        "to change the zoom factor,\nand copy text by dragging and then " \
        "pressing CTRL-C.\nClicking on a blue link will select that format " \
        "in the format selection options."
    TTT_CLOSE_BUTTON = "Close this window"
    TTT_DOWNLOAD_BUTTON = "Begin downloading and processing video " \
        "files"


class LinkIds:
    """String constants for link IDs
    """
    LINKID_FORMATID = "formatid"
    LINKID_FILEEXT = "vidextension"
    LINKID_AUDIOCODEC = "audiocodec"
    LINKID_VIDEOCODEC = "videocodec"
    LINKID_SUBLANGUAGE = "sublanguage"
    LINKID_SUBEXTENSION = "subextension"
    LINKID_RESOLUTION = "resolution"
