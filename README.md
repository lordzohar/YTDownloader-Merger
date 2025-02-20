# YTDownloader-Merger
YTDownloader-Merger is a Python script that allows you to download videos from a YouTube playlist and merge them into a single file. This tool leverages `pytube` for playlist handling and `yt-dlp` for downloading videos.

## Features

- Download all videos from a YouTube playlist.
- Save videos in a specified directory.
- Merge downloaded videos into a single file (optional).

## Requirements

- Python 3.6+
- `pytube`
- `yt-dlp`

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/lordzohar/YTDownloader-Merger.git
    cd YTDownloader-Merger
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Download Videos

To download videos from a YouTube playlist, run the `playlist_downloader.py` script:

```sh
python playlist_downloader.py
# Follow the on-screen prompt to provide the playlist URL and download the videos. The downloaded videos will be saved in the 'downloads' directory within the project folder. Please note URL should include a Youtube playlist id.

# Merge Videos
# After downloading the videos, combine them into a single video
python merger.py
# The script will display the progress of the video merging process and create a final combined video named 'final.mp4'.
```
### Find the Merged Video
You can find the merged video in the project directory.

### Contributing
Feel free to contribute! Please open an issue or bug fixes.

###  Support
If you find this project helpful, consider supporting me:

<a href="https://www.buymeacoffee.com/dailymeme" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

### License
This project is licensed under the GNU License. See the LICENSE file for details.

Acknowledgements
- pytube
- yt-dlp
