import argparse
import os
import sys
import ctypes
import winreg
import tkinter as tk
import threading
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, UnidentifiedImageError
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

# Temporarily add BUNDLE_DIR to PATH to ensure pydub finds ffmpeg/ffprobe
# This is crucial when running from a PyInstaller executable


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

# Debug prints to verify paths
print(f"DEBUG: BUNDLE_DIR = {BUNDLE_DIR}")
print(f"DEBUG: FFMPEG_PATH = {FFMPEG_PATH}")
print(f"DEBUG: FFPROBE_PATH = {FFPROBE_PATH}")
print(f"DEBUG: ffmpeg.exe exists at FFMPEG_PATH: {os.path.exists(FFMPEG_PATH)}")
print(f"DEBUG: ffprobe.exe exists at FFPROBE_PATH: {os.path.exists(FFPROBE_PATH)}")
print(f"DEBUG: PATH contains BUNDLE_DIR: {BUNDLE_DIR in os.environ["PATH"]}")

try:
    _verify_ffmpeg_executables()
    print("DEBUG: ffmpeg and ffprobe executables verified.")
except EnvironmentError as e:
    print(f"ERROR: FFmpeg/FFprobe verification failed: {e}")
    # Depending on severity, you might want to exit or disable audio features here
    # For now, we'll let the audio conversion attempt and fail gracefully there.

# Get the absolute path to the current executable for context menu registration
CURRENT_EXECUTABLE_PATH = sys.argv[0]

# Supported output formats
SUPPORTED_IMAGE_FORMATS = ["bmp", "gif", "ico", "jpeg", "png", "pdf", "tiff", "webp"]
SUPPORTED_AUDIO_FORMATS = ["mp3", "wav", "flac", "ogg", "aac"]
SUPPORTED_VIDEO_FORMATS = ["mp4", "avi", "mov", "mkv", "flv", "webm"]

# Common audio file extensions to add context menu for
AUDIO_EXTENSIONS = [".mp3", ".wav", ".flac", ".ogg", ".aac", ".m4a", ".wma"]
VIDEO_EXTENSIONS = [".mp4", ".avi", ".mov", ".mkv", ".flv", ".webm"]

# --- Image Conversion Functions ---

def convert_image(input_path, output_format):
    """
    Converts an image from the input_path to the specified output_format.
    The new file is saved with the same base name in the original directory.
    """
    try:
        if not os.path.exists(input_path):
            print(f"Error: The input file '{input_path}' was not found.")
            return

        image = Image.open(input_path)
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        input_directory = os.path.dirname(input_path)
        output_path = os.path.join(input_directory, f"{base_name}.{output_format}")
        
        pillow_formats = {
            "jpg": "JPEG",
            "jpeg": "JPEG",
            "ico": "ICO",
            "pdf": "PDF"
        }
        pillow_format = pillow_formats.get(output_format, output_format.upper())
        
        image.save(output_path, format=pillow_format)
        
        print(f"Success! Converted '{input_path}' to '{output_path}'.")

    except FileNotFoundError:
        print(f"Error: The input file '{input_path}' was not found.")
    except UnidentifiedImageError:
        print(f"Error: Could not identify image file '{input_path}'. It might be corrupt or an unsupported format.")
    except OSError as e:
        print(f"Error: Failed to save image to '{output_path}'. This might be due to an unsupported output format for the given image data, or a permissions issue. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during image conversion: {e}")

def run_conversion_logic_image(input_path, output_format, recursive):
    if os.path.isdir(input_path):
        image_extensions = (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tiff", ".ico")
        for root, _, files in os.walk(input_path):
            for file in files:
                if file.lower().endswith(image_extensions):
                    current_input_file_path = os.path.join(root, file)
                    convert_image(current_input_file_path, output_format)
            if not recursive:
                break
    elif os.path.isfile(input_path):
        convert_image(input_path, output_format)
    else:
        print(f"Error: The provided path '{input_path}' is neither a file nor a directory.")

# --- Audio Conversion Functions ---

def convert_audio(input_path, output_format):
    """
    Converts an audio file from the input_path to the specified output_format using ffmpeg.
    The new file is saved with the same base name in the original directory.
    """
    try:
        if not os.path.exists(input_path):
            print(f"Error: The input file '{input_path}' was not found.")
            return

        base_name = os.path.splitext(os.path.basename(input_path))[0]
        input_directory = os.path.dirname(input_path)
        output_path = os.path.join(input_directory, f"{base_name}.{output_format}")

        command = [
            FFMPEG_PATH,
            "-i", input_path,
            output_path
        ]

        # Run ffmpeg command
        if sys.platform == "win32":
            creationflags = subprocess.CREATE_NO_WINDOW
        else:
            creationflags = 0
        result = subprocess.run(command, capture_output=True, text=True, check=True, creationflags=creationflags)

        print(f"Success! Converted '{input_path}' to '{output_path}'.")
        print("FFmpeg stdout:", result.stdout)
        if result.stderr:
            print("FFmpeg stderr:", result.stderr)

    except FileNotFoundError:
        print(f"Error: The input file '{input_path}' was not found.")
    except subprocess.CalledProcessError as e:
        print(f"Error during audio conversion with ffmpeg: {e}")
        print("FFmpeg stdout:", e.stdout)
        print("FFmpeg stderr:", e.stderr)
    except EnvironmentError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during audio conversion: {e}")

def run_conversion_logic_audio(input_path, output_format, recursive):
    if os.path.isdir(input_path):
        audio_extensions = (".mp3", ".wav", ".flac", ".ogg", ".aac", ".m4a", ".wma")
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

# --- Video Conversion Functions ---

def convert_video(input_path, output_format):
    """
    Converts a video file from the input_path to the specified output_format using ffmpeg.
    The new file is saved with the same base name in the original directory.
    """
    try:
        if not os.path.exists(input_path):
            print(f"Error: The input file '{input_path}' was not found.")
            return

        base_name = os.path.splitext(os.path.basename(input_path))[0]
        input_directory = os.path.dirname(input_path)
        output_path = os.path.join(input_directory, f"{base_name}.{output_format}")

        command = [
            FFMPEG_PATH,
            "-i", input_path,
            output_path
        ]

        # Run ffmpeg command
        if sys.platform == "win32":
            creationflags = subprocess.CREATE_NO_WINDOW
        else:
            creationflags = 0
        result = subprocess.run(command, capture_output=True, text=True, check=True, creationflags=creationflags)

        print(f"Success! Converted '{input_path}' to '{output_path}'.")
        print("FFmpeg stdout:", result.stdout)
        if result.stderr:
            print("FFmpeg stderr:", result.stderr)

    except FileNotFoundError:
        print(f"Error: The input file '{input_path}' was not found.")
    except subprocess.CalledProcessError as e:
        print(f"Error during video conversion with ffmpeg: {e}")
        print("FFmpeg stdout:", e.stdout)
        print("FFmpeg stderr:", e.stderr)
    except EnvironmentError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during video conversion: {e}")

def run_conversion_logic_video(input_path, output_format, recursive):
    if os.path.isdir(input_path):
        for root, _, files in os.walk(input_path):
            for file in files:
                if file.lower().endswith(tuple(VIDEO_EXTENSIONS)):
                    current_input_file_path = os.path.join(root, file)
                    convert_video(current_input_file_path, output_format)
            if not recursive:
                break
    elif os.path.isfile(input_path):
        convert_video(input_path, output_format)
    else:
        print(f"Error: The provided path '{input_path}' is neither a file nor a directory.")

# --- Registry Management Functions ---

def add_context_menu_entry(file_type, menu_name, command, icon_path=None):
    try:
        key_path = rf"Software\Classes\{file_type}\shell\{menu_name}"
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
        if icon_path:
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, icon_path)
        winreg.CloseKey(key)

        command_key_path = rf"{key_path}\command"
        command_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, command_key_path)
        winreg.SetValueEx(command_key, None, 0, winreg.REG_SZ, command)
        winreg.CloseKey(command_key)
        print(f"Added context menu for {file_type}: {menu_name}")
    except Exception as e:
        print(f"Error adding context menu for {file_type}: {menu_name} - {e}")

def add_subcommand_entry(parent_key_path, submenu_name, command):
    try:
        submenu_key_path = rf"{parent_key_path}\shell\{submenu_name}"
        submenu_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, submenu_key_path)
        winreg.CloseKey(submenu_key)

        command_key_path = rf"{submenu_key_path}\command"
        command_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, command_key_path)
        winreg.SetValueEx(command_key, None, 0, winreg.REG_SZ, command)
        winreg.CloseKey(command_key)
        print(f"Added subcommand: {submenu_name}")
    except Exception as e:
        print(f"Error adding subcommand {submenu_name} - {e}")

def remove_context_menu_entry(file_type, menu_name):
    try:
        key_path = rf"Software\Classes\{file_type}\shell\{menu_name}"
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path + r'\command')
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
        print(f"Removed context menu for {file_type}: {menu_name}")
    except FileNotFoundError:
        print(f"Context menu for {file_type}: {menu_name} not found, skipping removal.")
    except Exception as e:
        print(f"Error removing context menu for {file_type}: {menu_name} - {e}")

def add_main_context_menu_entry_with_subcommands(file_type, main_menu_name, icon_path=None):
    try:
        key_path = rf"Software\Classes\{file_type}\shell\{main_menu_name}"
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
        winreg.SetValueEx(key, "SubCommands", 0, winreg.REG_SZ, "")
        if icon_path:
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, icon_path)
        winreg.CloseKey(key)
        print(f"Added main context menu with subcommands for {file_type}: {main_menu_name}")
        return key_path
    except Exception as e:
        print(f"Error adding main context menu with subcommands for {file_type}: {main_menu_name} - {e}")
        return None

def remove_subcommand_entry(parent_key_path, submenu_name):
    try:
        submenu_key_path = rf"{parent_key_path}\shell\{submenu_name}"
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, submenu_key_path + r'\command')
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, submenu_key_path)
        print(f"Removed subcommand: {submenu_name}")
    except FileNotFoundError:
        print(f"Subcommand {submenu_name} not found, skipping removal.")
    except Exception as e:
        print(f"Error removing subcommand {submenu_name} - {e}")

def delete_key_recursive(hkey, subkey):
    try:
        reg_key = winreg.OpenKey(hkey, subkey, 0, winreg.KEY_ALL_ACCESS)
        while True:
            try:
                sub = winreg.EnumKey(reg_key, 0)
                delete_key_recursive(reg_key, sub)
            except OSError:
                break
        winreg.CloseKey(reg_key)
        winreg.DeleteKey(hkey, subkey)
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Error deleting key recursively {subkey}: {e}")

def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin()

def check_if_entries_exist():
    main_menu_name = "Convert Media To"
    image_file_type = r"SystemFileAssociations\image"
    key_path = rf"Software\Classes\{image_file_type}\shell\{main_menu_name}"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"Error checking for existing entries: {e}")
        return False

def register_context_menu():
    if not is_admin():
        print("This script needs to be run with administrator privileges to modify the registry.")
        print("Please right-click on your terminal/command prompt and select 'Run as administrator'.")
        return

    main_menu_name = "Convert Media To"
    
    # For individual image files
    image_file_type = r"SystemFileAssociations\image"
    main_key_path_image = add_main_context_menu_entry_with_subcommands(image_file_type, main_menu_name)
    if main_key_path_image:
        for output_format in SUPPORTED_IMAGE_FORMATS:
            command = f'\"{CURRENT_EXECUTABLE_PATH}\" --image \"%1\" {output_format}'
            add_subcommand_entry(main_key_path_image, output_format.upper(), command)

    # For individual audio files
    for ext in AUDIO_EXTENSIONS:
        audio_file_type = rf"SystemFileAssociations\{ext}"
        main_key_path_audio = add_main_context_menu_entry_with_subcommands(audio_file_type, main_menu_name)
        if main_key_path_audio:
            for output_format in SUPPORTED_AUDIO_FORMATS:
                command = f'"{CURRENT_EXECUTABLE_PATH}" --audio -ai "%1" -o {output_format}'
                add_subcommand_entry(main_key_path_audio, output_format.upper(), command)

    # For individual video files
    for ext in VIDEO_EXTENSIONS:
        video_file_type = rf"SystemFileAssociations\{ext}"
        main_key_path_video = add_main_context_menu_entry_with_subcommands(video_file_type, main_menu_name)
        if main_key_path_video:
            for output_format in SUPPORTED_VIDEO_FORMATS:
                command = f'"{CURRENT_EXECUTABLE_PATH}" --video -vi "%1" -vo {output_format}'
                add_subcommand_entry(main_key_path_video, output_format.upper(), command)

    # For directories (when right-clicking on a folder)
    directory_file_type = "Directory"
    main_key_path_directory = add_main_context_menu_entry_with_subcommands(directory_file_type, main_menu_name)
    if main_key_path_directory:
        # Offer both image and audio conversion for directories
        for output_format in SUPPORTED_IMAGE_FORMATS:
            command = f'\"{CURRENT_EXECUTABLE_PATH}\" --image \"%1\" {output_format} -r'
            add_subcommand_entry(main_key_path_directory, f"IMAGE_TO_{output_format.upper()}", command)
        for output_format in SUPPORTED_AUDIO_FORMATS:
            command = f'"{CURRENT_EXECUTABLE_PATH}" --audio -ai "%1" -o {output_format} -ar'
            add_subcommand_entry(main_key_path_directory, f"AUDIO_TO_{output_format.upper()}", command)
        # Offer video conversion for directories
        for output_format in SUPPORTED_VIDEO_FORMATS:
            command = f'"{CURRENT_EXECUTABLE_PATH}" --video -vi "%1" -vo {output_format} -vr'
            add_subcommand_entry(main_key_path_directory, f"VIDEO_TO_{output_format.upper()}", command)

    # For directory background (when right-clicking in an empty space within a folder)
    directory_background_file_type = r"Directory\Background"
    main_key_path_directory_bg = add_main_context_menu_entry_with_subcommands(directory_background_file_type, main_menu_name)
    if main_key_path_directory_bg:
        # Offer both image and audio conversion for directory background
        for output_format in SUPPORTED_IMAGE_FORMATS:
            command = f'"{CURRENT_EXECUTABLE_PATH}" --image "%V" {output_format} -r'
            add_subcommand_entry(main_key_path_directory_bg, f"IMAGE_TO_{output_format.upper()}", command)
        for output_format in SUPPORTED_AUDIO_FORMATS:
            command = f'"{CURRENT_EXECUTABLE_PATH}" --audio -ai "%V" -o {output_format} -ar'
            add_subcommand_entry(main_key_path_directory_bg, f"AUDIO_TO_{output_format.upper()}", command)
        # Offer video conversion for directory background
        for output_format in SUPPORTED_VIDEO_FORMATS:
            command = f'"{CURRENT_EXECUTABLE_PATH}" --video -vi "%V" -vo {output_format} -vr'
            add_subcommand_entry(main_key_path_directory_bg, f"VIDEO_TO_{output_format.upper()}", command)
    
    print("Context menu entries added successfully. You might need to restart Explorer or your computer for changes to take effect.")

def unregister_context_menu():
    if not is_admin():
        print("This script needs to be run with administrator privileges to modify the registry.")
        print("Please right-click on your terminal/command prompt and select 'Run as administrator'.")
        return

    main_menu_name = "Convert Media To"
    old_image_menu_name = "Convert Image(s) To" # Old menu name to remove

    # Remove for individual image files (new menu name)
    image_file_type = r"SystemFileAssociations\image"
    main_key_path_image = rf"Software\Classes\{image_file_type}\shell\{main_menu_name}"
    for output_format in SUPPORTED_IMAGE_FORMATS:
        remove_subcommand_entry(main_key_path_image, output_format.upper())
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, main_key_path_image, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, "SubCommands")
        winreg.CloseKey(key)
        delete_key_recursive(winreg.HKEY_CURRENT_USER, main_key_path_image)
        print(f"Removed main '{main_menu_name}' menu for image files.")
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Error removing main '{main_menu_name}' menu for image files: {e}")

    # Remove for individual image files (old menu name)
    old_main_key_path_image = rf"Software\Classes\{image_file_type}\shell\{old_image_menu_name}"
    for output_format in SUPPORTED_IMAGE_FORMATS:
        remove_subcommand_entry(old_main_key_path_image, output_format.upper())
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, old_main_key_path_image, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, "SubCommands")
        winreg.CloseKey(key)
        delete_key_recursive(winreg.HKEY_CURRENT_USER, old_main_key_path_image)
        print(f"Removed old main '{old_image_menu_name}' menu for image files.")
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Error removing old main '{old_image_menu_name}' menu for image files: {e}")

    # Remove for individual audio files
    for ext in AUDIO_EXTENSIONS:
        audio_file_type = rf"SystemFileAssociations\{ext}"
        main_key_path_audio = rf"Software\Classes\{audio_file_type}\shell\{main_menu_name}"
        for output_format in SUPPORTED_AUDIO_FORMATS:
            remove_subcommand_entry(main_key_path_audio, output_format.upper())
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, main_key_path_audio, 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, "SubCommands")
            winreg.CloseKey(key)
            delete_key_recursive(winreg.HKEY_CURRENT_USER, main_key_path_audio)
            print(f"Removed main '{main_menu_name}' menu for audio files with extension {ext}.")
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error removing main '{main_menu_name}' menu for audio files with extension {ext}: {e}")

    # Remove for individual video files
    for ext in VIDEO_EXTENSIONS:
        video_file_type = rf"SystemFileAssociations\{ext}"
        main_key_path_video = rf"Software\Classes\{video_file_type}\shell\{main_menu_name}"
        for output_format in SUPPORTED_VIDEO_FORMATS:
            remove_subcommand_entry(main_key_path_video, output_format.upper())
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, main_key_path_video, 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, "SubCommands")
            winreg.CloseKey(key)
            delete_key_recursive(winreg.HKEY_CURRENT_USER, main_key_path_video)
            print(f"Removed main '{main_menu_name}' menu for video files with extension {ext}.")
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error removing main '{main_menu_name}' menu for video files with extension {ext}: {e}")

    # Remove for directories
    directory_file_type = "Directory"
    main_key_path_directory = rf"Software\Classes\{directory_file_type}\shell\{main_menu_name}"
    for output_format in SUPPORTED_IMAGE_FORMATS:
        remove_subcommand_entry(main_key_path_directory, f"IMAGE_TO_{output_format.upper()}")
    for output_format in SUPPORTED_AUDIO_FORMATS:
        remove_subcommand_entry(main_key_path_directory, f"AUDIO_TO_{output_format.upper()}")
    for output_format in SUPPORTED_VIDEO_FORMATS:
        remove_subcommand_entry(main_key_path_directory, f"VIDEO_TO_{output_format.upper()}")
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, main_key_path_directory, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, "SubCommands")
        winreg.CloseKey(key)
        delete_key_recursive(winreg.HKEY_CURRENT_USER, main_key_path_directory)
        print(f"Removed main '{main_menu_name}' menu for directories.")
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Error removing main '{main_menu_name}' menu for directories: {e}")

    # Remove for directory background
    directory_background_file_type = r"Directory\Background"
    main_key_path_directory_bg = rf"Software\Classes\{directory_background_file_type}\shell\{main_menu_name}"
    for output_format in SUPPORTED_IMAGE_FORMATS:
        remove_subcommand_entry(main_key_path_directory_bg, f"IMAGE_TO_{output_format.upper()}")
    for output_format in SUPPORTED_AUDIO_FORMATS:
        remove_subcommand_entry(main_key_path_directory_bg, f"AUDIO_TO_{output_format.upper()}")
    for output_format in SUPPORTED_VIDEO_FORMATS:
        remove_subcommand_entry(main_key_path_directory_bg, f"VIDEO_TO_{output_format.upper()}")
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, main_key_path_directory_bg, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, "SubCommands")
        winreg.CloseKey(key)
        delete_key_recursive(winreg.HKEY_CURRENT_USER, main_key_path_directory_bg)
        print(f"Removed main '{main_menu_name}' menu for directory background.")
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Error removing main '{main_menu_name}' menu for directory background: {e}")

    print("Context menu entries removed successfully. You might need to restart Explorer or your computer for changes to take effect.")

# --- GUI Implementation ---

class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state='normal')
        self.widget.insert(tk.END, str, (self.tag,))
        self.widget.see(tk.END)
        self.widget.configure(state='disabled')

    def flush(self):
        pass

class MediaConverterGUI:
    def __init__(self, master):
        self.master = master
        master.title("Media Converter")

        # --- Image Conversion Section ---
        image_frame = tk.LabelFrame(master, text="Image Conversion", padx=10, pady=10)
        image_frame.pack(padx=10, pady=5, fill="x")

        self.image_input_path = tk.StringVar()
        self.image_output_format = tk.StringVar(value=SUPPORTED_IMAGE_FORMATS[0])
        self.image_recursive = tk.BooleanVar(value=False)

        tk.Label(image_frame, text="Image File/Folder:").pack(side="left")
        tk.Entry(image_frame, textvariable=self.image_input_path, width=40).pack(side="left", expand=True, fill="x", padx=5)
        tk.Button(image_frame, text="Browse", command=self.browse_image_input).pack(side="left")

        image_options_frame = tk.Frame(image_frame)
        image_options_frame.pack(fill="x", pady=5)
        tk.Label(image_options_frame, text="Output Format:").pack(side="left")
        tk.OptionMenu(image_options_frame, self.image_output_format, *SUPPORTED_IMAGE_FORMATS).pack(side="left", padx=5)
        tk.Checkbutton(image_options_frame, text="Recursive", variable=self.image_recursive).pack(side="left", padx=10)
        tk.Button(image_options_frame, text="Convert Image", command=self.convert_image_action).pack(side="right", padx=5)

        # --- Audio Conversion Section ---
        audio_frame = tk.LabelFrame(master, text="Audio Conversion", padx=10, pady=10)
        audio_frame.pack(padx=10, pady=5, fill="x")

        self.audio_input_path = tk.StringVar()
        self.audio_output_format = tk.StringVar(value=SUPPORTED_AUDIO_FORMATS[0])
        self.audio_recursive = tk.BooleanVar(value=False)

        tk.Label(audio_frame, text="Audio File/Folder:").pack(side="left")
        tk.Entry(audio_frame, textvariable=self.audio_input_path, width=40).pack(side="left", expand=True, fill="x", padx=5)
        tk.Button(audio_frame, text="Browse", command=self.browse_audio_input).pack(side="left")

        audio_options_frame = tk.Frame(audio_frame)
        audio_options_frame.pack(fill="x", pady=5)
        tk.Label(audio_options_frame, text="Output Format:").pack(side="left")
        tk.OptionMenu(audio_options_frame, self.audio_output_format, *SUPPORTED_AUDIO_FORMATS).pack(side="left", padx=5)
        tk.Checkbutton(audio_options_frame, text="Recursive", variable=self.audio_recursive).pack(side="left", padx=10)
        tk.Button(audio_options_frame, text="Convert Audio", command=self.convert_audio_action).pack(side="right", padx=5)

        # --- Video Conversion Section ---
        video_frame = tk.LabelFrame(master, text="Video Conversion", padx=10, pady=10)
        video_frame.pack(padx=10, pady=5, fill="x")

        self.video_input_path = tk.StringVar()
        self.video_output_format = tk.StringVar(value=SUPPORTED_VIDEO_FORMATS[0])
        self.video_recursive = tk.BooleanVar(value=False)

        tk.Label(video_frame, text="Video File/Folder:").pack(side="left")
        tk.Entry(video_frame, textvariable=self.video_input_path, width=40).pack(side="left", expand=True, fill="x", padx=5)
        tk.Button(video_frame, text="Browse", command=self.browse_video_input).pack(side="left")

        video_options_frame = tk.Frame(video_frame)
        video_options_frame.pack(fill="x", pady=5)
        tk.Label(video_options_frame, text="Output Format:").pack(side="left")
        tk.OptionMenu(video_options_frame, self.video_output_format, *SUPPORTED_VIDEO_FORMATS).pack(side="left", padx=5)
        tk.Checkbutton(video_options_frame, text="Recursive", variable=self.video_recursive).pack(side="left", padx=10)
        tk.Button(video_options_frame, text="Convert Video", command=self.convert_video_action).pack(side="right", padx=5)

        # --- Context Menu Management ---
        context_menu_frame = tk.LabelFrame(master, text="Context Menu Management", padx=10, pady=10)
        context_menu_frame.pack(padx=10, pady=5, fill="x")

        tk.Button(context_menu_frame, text="Register Context Menu", command=self.register_action).pack(side="left", expand=True, fill="x", padx=5)
        tk.Button(context_menu_frame, text="Unregister Context Menu", command=self.unregister_action).pack(side="left", expand=True, fill="x", padx=5)

        # --- Log Area ---
        log_frame = tk.LabelFrame(master, text="Log", padx=10, pady=10)
        log_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.log_text = scrolledtext.ScrolledText(log_frame, state='disabled', height=10)
        self.log_text.pack(fill="both", expand=True)
        sys.stdout = TextRedirector(self.log_text, "stdout")
        sys.stderr = TextRedirector(self.log_text, "stderr")

    def browse_image_input(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", ".png .jpg .jpeg .gif .bmp .webp .tiff .ico"), ("All files", ".*")])
        if not path:
            path = filedialog.askdirectory()
        self.image_input_path.set(path)

    def convert_image_action(self):
        input_path = self.image_input_path.get()
        output_format = self.image_output_format.get().lower()
        recursive = self.image_recursive.get()
        if input_path:
            print(f"Starting image conversion for {input_path} to {output_format} (recursive: {recursive})...")
            # Run conversion in a separate thread
            conversion_thread = threading.Thread(target=run_conversion_logic_image, args=(input_path, output_format, recursive))
            conversion_thread.daemon = True  # Allow the main program to exit even if thread is still running
            conversion_thread.start()
        else:
            messagebox.showwarning("Input Missing", "Please select an image input file or folder.")

    def browse_audio_input(self):
        path = filedialog.askopenfilename(filetypes=[("Audio files", ".mp3 .wav .flac .ogg .aac .m4a .wma"), ("All files", ".*")])
        if not path:
            path = filedialog.askdirectory()
        self.audio_input_path.set(path)

    def convert_audio_action(self):
        input_path = self.audio_input_path.get()
        output_format = self.audio_output_format.get().lower()
        recursive = self.audio_recursive.get()
        if input_path:
            print(f"Starting audio conversion for {input_path} to {output_format} (recursive: {recursive})...")
            # Run conversion in a separate thread
            conversion_thread = threading.Thread(target=run_conversion_logic_audio, args=(input_path, output_format, recursive))
            conversion_thread.daemon = True
            conversion_thread.start()
        else:
            messagebox.showwarning("Input Missing", "Please select an audio input file or folder.")

    def browse_video_input(self):
        path = filedialog.askopenfilename(filetypes=[("Video files", ".mp4 .avi .mov .mkv .flv .webm"), ("All files", ".*")])
        if not path:
            path = filedialog.askdirectory()
        self.video_input_path.set(path)

    def convert_video_action(self):
        input_path = self.video_input_path.get()
        output_format = self.video_output_format.get().lower()
        recursive = self.video_recursive.get()
        if input_path:
            print(f"Starting video conversion for {input_path} to {output_format} (recursive: {recursive})...")
            # Run conversion in a separate thread
            conversion_thread = threading.Thread(target=run_conversion_logic_video, args=(input_path, output_format, recursive))
            conversion_thread.daemon = True
            conversion_thread.start()
        else:
            messagebox.showwarning("Input Missing", "Please select a video input file or folder.")

    def register_action(self):
        register_context_menu()

    def unregister_action(self):
        unregister_context_menu()

# --- Main Entry Point ---

def cli_main():
    parser = argparse.ArgumentParser(description="Convert media formats and manage context menu entries.")

    parser.add_argument("--register", action="store_true", help="Register context menu entries.")
    parser.add_argument("--unregister", action="store_true", help="Unregister context menu entries.")

    # Image conversion arguments
    image_group = parser.add_argument_group('Image Conversion')
    image_group.add_argument("--image", action="store_true", help="Perform image conversion.")
    image_group.add_argument("image_input_path", nargs='?', help="Path to the input image file or a directory containing images.")
    image_group.add_argument("image_output_format", nargs='?', help=f"Desired image output format ({','.join(SUPPORTED_IMAGE_FORMATS)}).")
    image_group.add_argument("-ir", "--image-recursive", action="store_true", help="Recursively search for images in subdirectories when image_input_path is a directory.")

    # Audio conversion arguments
    audio_group = parser.add_argument_group('Audio Conversion')
    audio_group.add_argument("--audio", action="store_true", help="Perform audio conversion.")
    audio_group.add_argument("-ai", "--audio-input", help="Path to the input audio file or a directory containing audio files.")
    audio_group.add_argument("-o", "--audio-output", help=f"Desired audio output format ({','.join(SUPPORTED_AUDIO_FORMATS)}).")
    audio_group.add_argument("-ar", "--audio-recursive", action="store_true", help="Recursively search for audio files in subdirectories when audio_input_path is a directory.")

    # Video conversion arguments
    video_group = parser.add_argument_group('Video Conversion')
    video_group.add_argument("--video", action="store_true", help="Perform video conversion.")
    video_group.add_argument("-vi", "--video-input", help="Path to the input video file or a directory containing video files.")
    video_group.add_argument("-vo", "--video-output", help=f"Desired video output format ({','.join(SUPPORTED_VIDEO_FORMATS)}).")
    video_group.add_argument("-vr", "--video-recursive", action="store_true", help="Recursively search for video files in subdirectories when video_input_path is a directory.")
    
    args = parser.parse_args()

    if args.register:
        register_context_menu()
    elif args.unregister:
        unregister_context_menu()
    elif args.image:
        if args.image_input_path and args.image_output_format:
            image_output_format = args.image_output_format.lower()
            if image_output_format not in SUPPORTED_IMAGE_FORMATS:
                print(f"Error: Unsupported image output format '{image_output_format}'. Supported formats are: {','.join(SUPPORTED_IMAGE_FORMATS)}")
                sys.exit(1)
            run_conversion_logic_image(args.image_input_path, image_output_format, args.image_recursive)
        else:
            parser.print_help()
    elif args.audio:
        if args.audio_input and args.audio_output:
            audio_output_format = args.audio_output.lower()
            if audio_output_format not in SUPPORTED_AUDIO_FORMATS:
                print(f"Error: Unsupported audio output format '{audio_output_format}'. Supported formats are: {','.join(SUPPORTED_AUDIO_FORMATS)}")
                sys.exit(1)
            run_conversion_logic_audio(args.audio_input, audio_output_format, args.audio_recursive)
        else:
            parser.print_help()
    elif args.video:
        if args.video_input and args.video_output:
            video_output_format = args.video_output.lower()
            if video_output_format not in SUPPORTED_VIDEO_FORMATS:
                print(f"Error: Unsupported video output format '{video_output_format}'. Supported formats are: {','.join(SUPPORTED_VIDEO_FORMATS)}")
                sys.exit(1)
            run_conversion_logic_video(args.video_input, video_output_format, args.video_recursive)
        else:
            parser.print_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    if len(sys.argv) > 1: # Check if any command-line arguments are provided
        cli_main()
    else:
        root = tk.Tk()
        app = MediaConverterGUI(root)
        root.mainloop()
