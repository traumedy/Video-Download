# Video-Download.py

Description: GUI for downloading lists of video URLs using yt-dlp library.
Author: Josh Buchbinder

## General usage

`Video-Download` is a PySide6 (Qt) GUI wrapper around the `yt-dlp`
python library that will parse a text file containing a list of URLs
or an HTML file of bookmarks exported from a browser and attempt to
download the video in each URL. See `yt-dlp` documentation to see
what type of video sites are
[supported](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

## Setup

After downloading this directory of code, install the required pythin libraries:

```text
pip3 install -r requirements.txt
```

`ffmpeg` may be required to perform post processing.

### Usage

URL list can either be a text file (.txt) with a list of URLs (lines beginning
with # are ignored) or an HTML file (.html) of bookmarks exported from a browser.
Google "`export bookmarks <browser>`" for detail on how to export bookmarks from
your browser. Most browsers except for Safari (thanks Apple) use a common HTML
file format so unlisted browsers are likely to be supported.  

Tested with browsers:  
. Safari (MacOS)  
. Brave (Windows)  
. Chrome (Windows)  
. Firefox (Windows)  
. Opera (Windows)  
. DuckDuckGo (Windows)  
. Vivaldi (Windows)  

