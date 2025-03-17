# video_download.py  

Description: GUI for downloading video URLs using `yt_dlp` library.  

Author: Josh Buchbinder  
Copyright 2025, Josh Buchbinder  

## General usage  

`video_download` is a PySide6 (Qt) GUI wrapper around the `yt_dlp`
Python library that can parse a text file containing a list of URLs
or an HTML file of bookmarks exported from a browser and attempt to
download the video in each URL. It can also download a single video
URL and list the formats available for that URL.  

See `yt-dlp` documentation to see which video sites are
[supported](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

## Setup  

After cloning this repository of code and entering the directory,
follow these steps:  

1. Ensure you have a recent version of Python 3 installed, between
versions 3.10 and 3.12.  

2. Optionally create and activate a venv virtual environment to contain
the packages for this program:  

```bash
python -m venv venv
```

On Windows:  

```bash
venv\Scripts\activate
```

On *nix or Mac:  

```bash
source venv/bin/activate
```

3. Install requirements.txt:  

```bash
pip3 install -r requirements.txt
```

4. On some platforms, there may be additional dependencies required. On
Ubuntu 22 for instance `xcb-cursor0` is required for Qt:  

```bash
sudo apt install libxcb-cursor0
```

## Usage  

To run the program, either launch Python 3 with the script as the argument or
on some systems you may be able to run the program directly:  

```bash
python ./video_download.py
```

```bash
./video_download.py
```

A single URL or a list of URLs can be specified. The URL list can either be
a text file (.txt) with a list of URLs (blank lines and lines beginning with #
are ignored) or an HTML file (.html) of bookmarks exported from a browser.  

Google "`export bookmarks <browser name>`" for detail on how to export
bookmarks from your browser. Most browsers except for Safari (thanks Apple)
use a common HTML file format so unlisted browsers are likely to be
supported.  

When processing an HTML file of bookmarks, if there are folders you will be
allowed to choose which folder of URLs to download.  

URL lists (html or txt files) can be dragged and dropped onto the window
instead of typing or browsing for their their paths.  

If `Specify format` is not checked, the best quality file that has audio
and video will be downloaded. If no such format exists, the best audio only
file will be merged with the best video only file. Checking this box and
selecting `Merge formats` and selecting `Best audio` and `Best video` will
result in the highest quality file available.  

The "List formats" button can be used to list the available formats for a
single URL. In `Format selection` you can specify `Raw format string` and
enter the `ID` shown for a format to download that specific format. Blue
links in the format list can be clicked on to select those formats in the
format selection settings.  

## Notes  

`ffmpeg` is only required if you select format options that require post
processing such as `Merge formats`.  

Some sites do not include a video identifier in the page URL. Right
click on the video window and there may be an option to
`Copy video URL`.  

HTML bookmarks export tested with browsers:  
. Brave (Windows)  
. Chrome (Windows)  
. DuckDuckGo (Windows)  
. Edge (Windows)  
. Firefox (Windows)  
. Opera (Windows)  
. Safari (MacOS)  
. Vivaldi (Windows)  

All settings in the GUI are stored between executions including the window
size.  

Every site has a limited selection of file types, audio and video codecs. Use
the `List formats` button available when `Single URL` is selected at the top
to view the available formats for a site based on any video URL.  
