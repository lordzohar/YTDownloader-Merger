import os
import subprocess
import urllib.request
import zipfile
import shutil
import time
import stat
from yt_dlp import YoutubeDL


def create_directory(directory):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def download_with_progress(url, filename):
    """Download a file with a simple progress display."""
    response = urllib.request.urlopen(url)
    total_size = int(response.getheader('Content-Length').strip())
    block_size = 1024  # 1 KiB
    downloaded_size = 0

    with open(filename, 'wb') as f:
        while True:
            buffer = response.read(block_size)
            if not buffer:
                break
            f.write(buffer)
            downloaded_size += len(buffer)
            percent = (downloaded_size / total_size) * 100
            print(f"\rDownloading {filename}: {percent:.2f}%", end='')

    print()  # Newline after the download is complete
    if downloaded_size != total_size:
        raise Exception("Error: Download incomplete")


def download_ffmpeg():
    """Check if FFmpeg exists; if not, download and extract it."""
    extract_path = "ffmpeg"
    if os.path.exists(extract_path):
        print("FFmpeg is already downloaded. Skipping download.")
        version_folder = next(os.walk(extract_path))[1][0]
        ffmpeg_executable = os.path.join(extract_path, version_folder, 'bin', 'ffmpeg.exe')
        return ffmpeg_executable, extract_path

    print("FFmpeg not found. Downloading now...")
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = "ffmpeg.zip"

    # Download FFmpeg zip with progress
    download_with_progress(url, zip_path)

    # Extract the zip file
    print("Extracting FFmpeg...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    # Clean up the zip file
    os.remove(zip_path)

    # Get the version folder inside the extracted path
    version_folder = next(os.walk(extract_path))[1][0]
    ffmpeg_executable = os.path.join(extract_path, version_folder, 'bin', 'ffmpeg.exe')

    return ffmpeg_executable, extract_path


def download_video_or_playlist(url):
    """Download a single video or a playlist using yt-dlp."""
    options = {
        'format': 'bestvideo+bestaudio/best',  # Download best quality video + audio
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save to 'downloads' directory
        'merge_output_format': 'mp4',  # Merge video and audio into MP4 format
    }

    # Create the downloads directory if it doesn't exist
    create_directory('downloads')

    with YoutubeDL(options) as ydl:
        try:
            ydl.download([url])
            print("✅ Download successful.")
        except Exception as e:
            print(f"❌ Error downloading: {e}")


def remove_readonly(func, path, excinfo):
    """Clear the readonly bit and reattempt the removal."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def main():
    """Main function to handle video/playlist downloading."""
    url = input("Enter YouTube video or playlist URL: ")

    # Download and setup FFmpeg
    ffmpeg_executable, ffmpeg_dir = download_ffmpeg()
    os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_executable)

    try:
        # Download the video or playlist
        print("Starting download...")
        download_video_or_playlist(url)

        # Ask the user if they want to merge the downloaded files
        merge_videos = input("\nDo you want to merge all downloaded files into a single video? (Y/N): ").strip().lower()
        if merge_videos == 'y':
            print("Calling merger script to merge downloaded files...")
            subprocess.run(["python", "merger.py"])
        else:
            print("Merging skipped.")
    finally:
        # Clean up FFmpeg files
        print("Waiting for 2 seconds before cleaning up FFmpeg temporary files...")
        time.sleep(2)
        try:
	    if not os.path.exists(ffmpeg_dir):
                 shutil.rmtree(ffmpeg_dir, onerror=remove_readonly)
                 print("✅✅✅ Cleaned up FFmpeg temporary files.")
        except Exception as e:
            print(f"❌❌❌ Failed to delete FFmpeg directory: {str(e)}")


if __name__ == "__main__":
    main()
