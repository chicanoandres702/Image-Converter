import argparse
import os
import sys
import subprocess

# --- Global Configuration ---

# Determine if running as a PyInstaller bundled executable
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # Running in a PyInstaller bundle
    BUNDLE_DIR = sys._MEIPASS
else:
    # Running as a normal Python script
    BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to ffmpeg.exe and ffprobe.exe (assuming they are bundled in the same directory as the executable)
FFMPEG_PATH = os.path.join(BUNDLE_DIR, "ffmpeg.exe")
FFPROBE_PATH = os.path.join(BUNDLE_DIR, "ffprobe.exe")

def _verify_ffmpeg_executables():
    """Verifies that ffmpeg.exe and ffprobe.exe exist and are executable."""
    if not os.path.exists(FFMPEG_PATH):
        raise EnvironmentError(f"ffmpeg.exe not found at {FFMPEG_PATH}. Please ensure it's bundled correctly.")
    if not os.path.isfile(FFMPEG_PATH):
        raise EnvironmentError(f"ffmpeg.exe at {FFMPEG_PATH} is not a file.")
    if not os.access(FFMPEG_PATH, os.X_OK):
        raise EnvironmentError(f"ffmpeg.exe at {FFMPEG_PATH} is not executable.")

    if not os.path.exists(FFPROBE_PATH):
        raise EnvironmentError(f"ffprobe.exe not found at {FFPROBE_PATH}. Please ensure it's bundled correctly.")
    if not os.path.isfile(FFPROBE_PATH):
        raise EnvironmentError(f"ffprobe.exe at {FFPROBE_PATH} is not a file.")
    if not os.access(FFPROBE_PATH, os.X_OK):
        raise EnvironmentError(f"ffprobe.exe at {FFPROBE_PATH} is not executable.")

try:
    _verify_ffmpeg_executables()
    print("DEBUG: ffmpeg and ffprobe executables verified.")
except EnvironmentError as e:
    print(f"ERROR: FFmpeg/FFprobe verification failed: {e}")

# Supported output formats for audio conversion
SUPPORTED_OUTPUT_FORMATS = ['mp3', 'wav', 'flac', 'ogg', 'aac']

def convert_audio(input_path, output_format):
    """
    Converts an audio file from the input_path to the specified output_format.
    The new file is saved with the same base name in the original directory.
    """
    try:
        if not os.path.exists(input_path):
            print(f"Error: The input file '{input_path}' was not found.")
            return

        base_name = os.path.splitext(os.path.basename(input_path))[0]
        input_directory = os.path.dirname(input_path)
        output_path = os.path.join(input_directory, f"{base_name}.{output_format}")
        
        command = [FFMPEG_PATH, "-i", input_path, output_path]
        
        result = subprocess.run(command, capture_output=True, text=True, check=False)

        if result.returncode == 0:
            print(f"Success! Converted '{input_path}' to '{output_path}'.")
        else:
            print(f"Error converting '{input_path}':")
            print(result.stderr)

    except FileNotFoundError:
        print(f"Error: ffmpeg command not found. Please ensure ffmpeg is installed and in your PATH.")
    except Exception as e:
        print(f"An unexpected error occurred during conversion: {e}")

def run_conversion_logic(input_path, output_format, recursive):
    if os.path.isdir(input_path):
        audio_extensions = ('.mp3', '.wav', '.flac', '.ogg', '.aac', '.m4a', '.wma') # Add more as needed
        for root, _, files in os.walk(input_path):
            for file in files:
                if file.lower().endswith(audio_extensions):
                    current_input_file_path = os.path.join(root, file)
                    convert_audio(current_input_file_path, output_format)
            if not recursive:
                break
    elif os.path.isfile(input_path):
        convert_audio(input_path, output_format)
    else:
        print(f"Error: The provided path '{input_path}' is neither a file nor a directory.")

def main():
    parser = argparse.ArgumentParser(description="Convert audio formats.")

    parser.add_argument("input_path", help="Path to the input audio file or a directory containing audio files.")
    parser.add_argument("output_format", help=f"Desired output format ({', '.join(SUPPORTED_OUTPUT_FORMATS)}).")
    parser.add_argument("-r", "--recursive", action="store_true", help="Recursively search for audio files in subdirectories when input_path is a directory.")
    
    args = parser.parse_args()

    output_format = args.output_format.lower()
    if output_format not in SUPPORTED_OUTPUT_FORMATS:
        print(f"Error: Unsupported output format '{output_format}'. Supported formats are: {', '.join(SUPPORTED_OUTPUT_FORMATS)}")
        sys.exit(1)

    run_conversion_logic(args.input_path, output_format, args.recursive)

if __name__ == "__main__":
    main()