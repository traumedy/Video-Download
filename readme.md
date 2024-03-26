# Video-Download.py

Description: Downloads lists of video URLs using yt-dlp library
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

```
pip3 install -r requirements.txt
```

`ffmpeg` may be required to perform post processing.
