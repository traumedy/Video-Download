# video_download.py  

Description: GUI for downloading lists of video URLs using yt-dlp library.
Author: Josh Buchbinder

## General usage  

`video_download` is a PySide6 (Qt) GUI wrapper around the `yt-dlp`
python library that will parse a text file containing a list of URLs
or an HTML file of bookmarks exported from a browser and attempt to
download the video in each URL. See `yt-dlp` documentation to see
what type of video sites are
[supported](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

## Setup  

After cloning this repo of code, follow these steps:  

1. Ensure you have a recent version of Python 3 installed, at least
version 3.10.

2. Install requirements.txt:  

```bash
pip3 install -r requirements.txt
```

3. On non Windows platforms, make the Python script executable:  

```bash
chmod u+x ./video_download.py
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

The URL list can either be a text file (.txt) with a list of URLs (lines
beginning with # are ignored) or an HTML file (.html) of bookmarks exported
from a browser.
Google "`export bookmarks <browser name>`" for detail on how to export
bookmarks from your browser. Most browsers except for Safari (thanks Apple)
use a common HTML file format so unlisted browsers are likely to be
supported.  

Tested with browsers:  
. Brave (Windows)  
. Chrome (Windows)  
. DuckDuckGo (Windows)  
. Edge (Windows)  
. Firefox (Windows)  
. Opera (Windows)  
. Safari (MacOS)  
. Vivaldi (Windows)  

When processing an HTML file of bookmarks, if there are folders you will be
allowed to choose which folder of URLs to download.  

## Notes  

All settings in the GUI are stored between executions including the window size.  

Currently when selecting a container file extension, the requested format will
attempt to be downloaded from the server _if it is available_. If none is selected,
the 'best quality' format will be downloaded.  

## Todo  

More format selection options and post processing options will be added.  
