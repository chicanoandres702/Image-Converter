# Media Converter

This is a versatile command-line tool and GUI application written in Python for converting various media files (images, audio, and video) from one format to another. It leverages the powerful Pillow library for images and FFmpeg for audio and video, ensuring a comprehensive and straightforward conversion process.

## Features

*   **Versatile Image Conversion:** Convert images between a wide range of formats supported by Pillow (e.g., JPG, PNG, WEBP, BMP, GIF, ICO, PDF).
*   **Audio Conversion:** Convert audio files between various formats (e.g., MP3, WAV, FLAC, OGG, AAC) using FFmpeg.
*   **Video Conversion:** Convert video files between various formats (e.g., MP4, AVI, MOV, MKV, FLV, WEBM) using FFmpeg.
*   **Command-Line Interface:** Easy to use directly from your terminal.
*   **Graphical User Interface (GUI):** A user-friendly GUI for interactive conversions.
*   **Automatic Naming:** Converted files are saved with the same base name as the input file, with the new extension, in the current directory.
*   **Error Handling:** Includes basic error handling for file not found issues and other conversion problems.

## Requirements

This project requires the `Pillow` library for image manipulation and `FFmpeg` for audio/video conversions. If you don't have them installed, you can do so using pip for Pillow and by downloading FFmpeg.

*   **Pillow:**
    ```bash
    pip install Pillow
    ```
*   **FFmpeg:**
    Download FFmpeg from its official website: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html). Ensure `ffmpeg.exe` and `ffprobe.exe` are placed in the same directory as `main_converter.py` or are accessible via your system's PATH.

## Usage

This project can be used either via its Graphical User Interface (GUI) or through the command-line interface (CLI). The main script for both functionalities is `main_converter.py`.

### Graphical User Interface (GUI)

To launch the GUI, simply run `main_converter.py` without any command-line arguments:

```bash
python main_converter.py
```

### Command-Line Interface (CLI)

To use the CLI, run `main_converter.py` with specific arguments for the type of conversion you want to perform.

#### General Options

*   `--register`: Register context menu entries (requires administrator privileges).
*   `--unregister`: Unregister context menu entries (requires administrator privileges).

#### Image Conversion

```bash
python main_converter.py --image <input_path> <output_format> [-ir]
```

**Arguments:**

*   `--image`: Flag to indicate image conversion.
*   `<input_path>`: The path to the input image file (for single conversion) OR the path to a directory containing image files (for batch conversion).
*   `<output_format>`: The desired format for the output image(s) (e.g., `png`, `jpg`, `webp`, `ico`, `pdf`).
*   `-ir`, `--image-recursive` (optional): When `<input_path>` is a directory, this flag will make the script recursively search for images in subdirectories.

**Image Examples:**

1.  **Convert a single JPG image to PNG:**

    ```bash
    python main_converter.py --image my_photo.jpg png
    ```

2.  **Convert all supported images in a directory to JPG:**

    ```bash
    python main_converter.py --image my_images jpg
    ```

3.  **Convert all supported images in a directory and its subdirectories to PNG (recursive):**

    ```bash
    python main_converter.py --image my_images png -ir
    ```

#### Audio Conversion

```bash
python main_converter.py --audio -ai <input_path> -o <output_format> [-ar]
```

**Arguments:**

*   `--audio`: Flag to indicate audio conversion.
*   `-ai`, `--audio-input`: Path to the input audio file or a directory containing audio files.
*   `-o`, `--audio-output`: Desired audio output format (e.g., `mp3`, `wav`, `flac`, `ogg`, `aac`).
*   `-ar`, `--audio-recursive` (optional): Recursively search for audio files in subdirectories when input path is a directory.

**Audio Examples:**

1.  **Convert a single WAV audio file to MP3:**

    ```bash
    python main_converter.py --audio -ai my_song.wav -o mp3
    ```

2.  **Convert all supported audio files in a directory to FLAC:**

    ```bash
    python main_converter.py --audio -ai my_music_folder -o flac
    ```

3.  **Convert all supported audio files in a directory and its subdirectories to OGG (recursive):**

    ```bash
    python main_converter.py --audio -ai my_music_library -o ogg -ar
    ```

#### Video Conversion

```bash
python main_converter.py --video -vi <input_path> -vo <output_format> [-vr]
```

**Arguments:**

*   `--video`: Flag to indicate video conversion.
*   `-vi`, `--video-input`: Path to the input video file or a directory containing video files.
*   `-vo`, `--video-output`: Desired video output format (e.g., `mp4`, `avi`, `mov`, `mkv`, `flv`, `webm`).
*   `-vr`, `--video-recursive` (optional): Recursively search for video files in subdirectories when input path is a directory.

**Video Examples:**

1.  **Convert a single MOV video file to MP4:**

    ```bash
    python main_converter.py --video -vi my_movie.mov -vo mp4
    ```

2.  **Convert all supported video files in a directory to AVI:**

    ```bash
    python main_converter.py --video -vi my_videos -vo avi
    ```

3.  **Convert all supported video files in a directory and its subdirectories to MKV (recursive):**

    ```bash
    python main_converter.py --video -vi my_video_library -vo mkv -vr
    ```

## Supported Formats

### Image Formats

The script supports most image formats that the Pillow library can handle. Common supported formats include:

*   JPEG (`jpg`, `jpeg`)
*   PNG (`png`)
*   WEBP (`webp`)
*   BMP (`bmp`)
*   GIF (`gif`)
*   ICO (`ico`)
*   PDF (`pdf`)

### Audio Formats

The script supports various audio formats for conversion using FFmpeg. Common supported formats include:

*   MP3 (`mp3`)
*   WAV (`wav`)
*   FLAC (`flac`)
*   OGG (`ogg`)
*   AAC (`aac`)

### Video Formats

The script supports various video formats for conversion using FFmpeg. Common supported formats include:

*   MP4 (`mp4`)
*   AVI (`avi`)
*   MOV (`mov`)
*   MKV (`mkv`)
*   FLV (`flv`)
*   WEBM (`webm`)

## Error Handling

The script provides informative error messages if:

*   The input file does not exist.
*   An invalid output format is specified or an issue occurs during the conversion process.

## License

This project is open-source and available under the [MIT License](LICENSE).

## Troubleshooting

Here are some common issues you might encounter and how to resolve them:

### 1. Pillow Library Not Found

If you see an error message like `ModuleNotFoundError: No module named 'PIL'`, it means the Pillow library is not installed.

**Solution:** Install Pillow using pip:
```bash
pip install Pillow
```

### 2. Input File Not Found

If the script reports `Error: The input file '<path>' was not found.`, it means the specified input image file does not exist or the path is incorrect.

**Solution:**
*   Double-check the file path for typos.
*   Ensure the file is in the specified location.
*   If the file is in a different directory, provide the full absolute path to the file.

### 3. Unsupported Output Format or Conversion Error

If you encounter an error during conversion, such as `An error occurred during conversion: cannot write mode P as JPEG` or similar, it might be due to:

*   **Unsupported Format:** The desired output format is not supported by Pillow or the input image cannot be converted to that specific format (e.g., trying to save a transparent PNG as a JPG, which doesn't support transparency).
*   **Corrupt Image:** The input image file might be corrupt or malformed.

**Solution:**
*   Verify that the output format you specified is a common image format supported by Pillow (e.g., `png`, `jpg`, `webp`, `ico`, `pdf`).
*   Try converting to a different, more common format (e.g., `png` or `jpg`) to see if the issue persists.
*   Check if the input image file can be opened by other image viewers or editors.

### 4. Permissions Error

If you get an error related to file writing permissions, it means the script does not have the necessary rights to create a new file in the current directory.

**Solution:**
*   Run the script from a directory where you have write permissions.
*   Change the permissions of the target directory if necessary (consult your operating system's documentation for how to do this).

## Windows Context Menu Integration

For Windows users, this project provides functionality to integrate media conversion directly into your right-click context menu for various file types and directories. This is handled by the `main_converter.py` script itself.

### How it Works

The `main_converter.py` script, when run with the `--register` argument, adds "Convert Media To" submenus to the context menu:

*   **For Image Files:** When you right-click on a supported image file, a "Convert Media To" submenu will appear, offering various image output formats (e.g., BMP, ICO, JPEG, PNG, PDF).
*   **For Audio Files:** When you right-click on a supported audio file, a "Convert Media To" submenu will appear, offering various audio output formats (e.g., MP3, WAV, FLAC, OGG, AAC).
*   **For Video Files:** When you right-click on a supported video file, a "Convert Media To" submenu will appear, offering various video output formats (e.g., MP4, AVI, MOV, MKV, FLV, WEBM).
*   **For Directories:** When you right-click on a directory, a "Convert Media To" submenu will appear, offering options to convert all supported image, audio, or video files within that directory (and its subdirectories if recursive options are used).

Selecting an option will convert the media file(s) to the chosen format.

### Usage

**Important:** You must run `main_converter.py` with **administrator privileges** for it to modify the Windows Registry. Right-click on your terminal/command prompt and select "Run as administrator".

1.  **Add Context Menu Entries:**

    Navigate to the project directory in an **administrator** command prompt and run:

    ```bash
    python main_converter.py --register
    ```

    You might need to restart Windows Explorer (or your computer) for the changes to take effect.

2.  **Remove Context Menu Entries:**

    If you wish to remove the context menu entries, run the script with the `--unregister` argument:

    ```bash
    python main_converter.py --unregister
    ```

    Again, a restart of Windows Explorer or your computer might be necessary.
