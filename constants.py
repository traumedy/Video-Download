#!/usr/bin/env python3

"""constants.py - Constants used by video_download.py

Author: Josh Buchbinder
"""

from enum import Enum

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
SETTINGS_VAL_DOWNLOADSUBTITLES = "DownloadSubtitls"
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
# DOCTYPE_SAFARI = 2

# Regex to strip color codes from string
REGEX_COLORSTRIP = r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]'


