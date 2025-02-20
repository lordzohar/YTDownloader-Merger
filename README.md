# YTDownloader-Merger

YTDownloader-Merger is a Python-based tool that allows you to download videos from YouTube (single videos or playlists) and optionally merge the downloaded files into a single video. This tool leverages `yt-dlp` for robust downloading and FFmpeg for video merging.

## Features

- 📥 Download individual videos or all videos from a YouTube playlist.
- 📂 Save videos in a dedicated `downloads` directory.
- 🎬 Option to merge all downloaded videos into a single file (`final.mp4`).
- 🔄 Automatically handle FFmpeg download and setup if it's not already available.
- 🛠 User-friendly prompts for merging and overwriting options.

## Requirements

- Python 3.6+
- `yt-dlp`
- FFmpeg (automatically downloaded by the script if not present).

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/lordzohar/YTDownloader-Merger.git
    cd YTDownloader-Merger
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Download Videos

To download videos from a YouTube playlist or a single YouTube video, run the `playlist_downloader.py` script:

```bash
python playlist_downloader.py
```
- Enter the YouTube URL (either a playlist or a single video) when prompted.
- The videos will be downloaded to the downloads directory in the project folder.

## Merge Videos

After downloading the videos, the script will prompt you:
```plain text
    Do you want to merge all downloaded files into a single video? (Y/N):

    - If you press Y, the script will automatically call merger.py to combine all videos into a single file named final.mp4.
    - If you press N, the merging step will be skipped.
```
## Find the Merged Video

The merged video (final.mp4) will be available in the project directory after successful merging.
Example Workflow

Run the playlist downloader:
```bash
python playlist_downloader.py
```
Enter a YouTube playlist or video URL when prompted.

Merge videos (optional): At the end of the download process, choose whether to merge the videos by pressing Y or N.

### Contributing
Feel free to contribute! Please open an issue or bug fixes.

###  Support
If you find this project helpful, consider supporting me:

<a href="https://www.buymeacoffee.com/dailymeme" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

### License
This project is licensed under the GNU License. See the LICENSE file for details.

Acknowledgements
- yt-dlp
