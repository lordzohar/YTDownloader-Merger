import os
import subprocess

def get_video_files(directory, extension='.mp4'):
    """Get a list of video file paths with the specified extension in the given directory."""
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(extension)]

def create_input_file(video_files, input_filename='input.txt'):
    """Create a text file containing a list of input video files for FFmpeg."""
    with open(input_filename, 'w') as input_file:
        for video_file in video_files:
            input_file.write(f"file '{video_file}'\n")

def concatenate_videos(input_filename='input.txt', output_filename='final.mp4'):
    """Concatenate video clips using FFmpeg with progress display and ignoring warnings."""
    ffmpeg_command = [
        'ffmpeg', '-f', 'concat', '-safe', '0', '-i', input_filename,
        '-c:v', 'copy', '-c:a', 'copy', '-v', 'warning', '-progress', 'pipe:1', output_filename
    ]

    ffmpeg_process = subprocess.Popen(
        ffmpeg_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    for line in ffmpeg_process.stdout:
        if "time=" in line:
            print(line.strip())

    ffmpeg_process.communicate()

def main():
    downloads_dir = 'downloads'
    input_filename = 'input.txt'
    output_filename = 'final.mp4'

    # Get the list of video files
    video_files = get_video_files(downloads_dir)

    if not video_files:
        print("No video files found in the 'downloads' directory.")
        return

    # Create the input file for FFmpeg
    create_input_file(video_files, input_filename)

    # Concatenate the videos
    concatenate_videos(input_filename, output_filename)

    # Remove the temporary input file
    os.remove(input_filename)

    print(f"Merged all videos into '{output_filename}'.")

if __name__ == "__main__":
    main()
