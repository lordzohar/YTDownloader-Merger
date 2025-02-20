import os
from pytube import Playlist
from pytube.exceptions import PytubeError
from yt_dlp import YoutubeDL

# Replace with your playlist URL
playlist_url = input("Playlist URL: ")

# Create a directory to save the downloaded videos if it doesn't exist
if not os.path.exists('downloads'):
    os.makedirs('downloads')

# Create a Playlist object
playlist = Playlist(playlist_url)

# Function to download a video
def download_video(video_url, index):
    try:
        ydl_opts = {
            'outtmpl': f'downloads/video_{index}.%(ext)s',
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"✅✅✅ Downloaded video {index}")
    except Exception as e:
        print(f"❌❌❌ Error downloading video {index}: {str(e)}")

# Loop through the videos in the playlist and download them
for index, video in enumerate(playlist.video_urls, start=1):
    download_video(video, index)

print("✅✅✅ Downloaded all available videos in the playlist to 'downloads' directory in .mp4 format")
