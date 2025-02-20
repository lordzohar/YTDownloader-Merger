import os
from pytube import Playlist
from pytube.exceptions import PytubeError
from yt_dlp import YoutubeDL

def create_directory(directory):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def download_video(video_url, index):
    """Download a video using yt-dlp."""
    try:
        ydl_opts = {
            'outtmpl': f'downloads/video_{index}.%(ext)s',
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"✅✅✅ Downloaded video {index}")
    except Exception as e:
        print(f"❌❌❌ Error downloading video {index}: {str(e)}")

def main():
    playlist_url = input("Playlist URL: ")

    # Create a directory to save the downloaded videos if it doesn't exist
    create_directory('downloads')

    # Create a Playlist object
    try:
        playlist = Playlist(playlist_url)
    except PytubeError as e:
        print(f"❌❌❌ Error creating playlist: {str(e)}")
        return

    # Loop through the videos in the playlist and download them
    for index, video in enumerate(playlist.video_urls, start=1):
        download_video(video, index)

    print("✅✅✅ Downloaded all available videos in the playlist to 'downloads' directory in .mp4 format")

if __name__ == "__main__":
    main()
