import os
import subprocess
import urllib.request
import zipfile
import shutil
import time
import stat

def download_ffmpeg():
    """Download and extract FFmpeg version 7.1 temporarily."""
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = "ffmpeg.zip"
    extract_path = "ffmpeg"

    # Remove existing FFmpeg directory if it exists
    if os.path.exists(extract_path):
        shutil.rmtree(extract_path)

    # Download the FFmpeg zip file
    print("Downloading FFmpeg...")
    urllib.request.urlretrieve(url, zip_path)

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

def get_video_files(directory, extension='.mp4'):
    """Get a list of video file paths with the specified extension in the given directory."""
    try:
        return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(extension)]
    except FileNotFoundError as fnf_error:
        print(f"❌❌❌ Directory not found: {str(fnf_error)}")
        return []
    except Exception as e:
        print(f"❌❌❌ Unexpected error: {str(e)}")
        return []

def create_input_file(video_files, input_filename='input.txt'):
    """Create a text file containing a list of input video files for FFmpeg."""
    try:
        with open(input_filename, 'w') as input_file:
            for video_file in video_files:
                input_file.write(f"file '{video_file}'\n")
    except FileNotFoundError as fnf_error:
        print(f"❌❌❌ File not found error: {str(fnf_error)}")
    except Exception as e:
        print(f"❌❌❌ Unexpected error: {str(e)}")

def concatenate_videos(ffmpeg_path, input_filename='input.txt', output_filename='final.mp4'):
    """Concatenate video clips using FFmpeg with progress display and ignoring warnings."""
    ffmpeg_command = [
        ffmpeg_path, '-f', 'concat', '-safe', '0', '-i', input_filename,
        '-c:v', 'copy', '-c:a', 'copy', '-v', 'warning', '-progress', 'pipe:1', output_filename
    ]

    try:
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
    except FileNotFoundError as fnf_error:
        print(f"❌❌❌ FFmpeg not found: {str(fnf_error)}. Please ensure FFmpeg is installed and added to your PATH.")
        return False
    except Exception as e:
        print(f"❌❌❌ Error during video concatenation: {str(e)}")
        return False
    return True

def remove_readonly(func, path, excinfo):
    """Clear the readonly bit and reattempt the removal."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def main():
    downloads_dir = 'downloads'
    input_filename = 'input.txt'
    output_filename = 'final.mp4'

    # Check if the output file already exists
    if os.path.exists(output_filename):
        overwrite = input(f"'{output_filename}' already exists. Do you want to overwrite it? (Y/N): ").strip().lower()
        if overwrite != 'y':
            print("Operation cancelled.")
            # Clean up FFmpeg files if the user chooses not to overwrite
            if os.path.exists('ffmpeg'):
                shutil.rmtree('ffmpeg', onerror=remove_readonly)
            return

    # Get the list of video files
    video_files = get_video_files(downloads_dir)

    if not video_files:
        print("No video files found in the 'downloads' directory.")
        return

    # Create the input file for FFmpeg
    create_input_file(video_files, input_filename)

    # Download and extract FFmpeg
    ffmpeg_path, ffmpeg_dir = download_ffmpeg()

    # Concatenate the videos
    if concatenate_videos(ffmpeg_path, input_filename, output_filename):
        # Remove the temporary input file
        try:
            os.remove(input_filename)
        except FileNotFoundError as fnf_error:
            print(f"❌❌❌ Temporary input file not found: {str(fnf_error)}")
        except Exception as e:
            print(f"❌❌❌ Error removing temporary input file: {str(e)}")

        print(f"Merged all videos into '{output_filename}'.")

        # Close FFmpeg process and wait before deleting
        print("Waiting for 2 seconds before cleaning up FFmpeg files...")
        time.sleep(2)
        try:
            shutil.rmtree(ffmpeg_dir, onerror=remove_readonly)
        except Exception as e:
            print(f"❌❌❌ Failed to delete FFmpeg directory: {str(e)}")
    else:
        print("❌❌❌ Failed to merge videos.")
        # Clean up FFmpeg files if the merge fails
        if os.path.exists(ffmpeg_dir):
            try:
                shutil.rmtree(ffmpeg_dir, onerror=remove_readonly)
            except Exception as e:
                print(f"❌❌❌ Failed to delete FFmpeg directory: {str(e)}")

if __name__ == "__main__":
    main()
