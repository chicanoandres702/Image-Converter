# This script is a command-line tool for converting image formats.
# It requires the Pillow library, which can be installed with:
# pip install Pillow

import argparse
import os
from PIL import Image, UnidentifiedImageError

def convert_image(input_path, output_format):
    """
    Converts an image from the input_path to the specified output_format.
    The new file is saved with the same base name in the current directory.
    """
    try:
        # Check if the input file exists
        if not os.path.exists(input_path):
            print(f"Error: The input file '{input_path}' was not found.")
            return

        # Open the image file
        image = Image.open(input_path)
        
        # Get the base filename without the extension
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        
        # Construct the output file path using the desired format
        output_path = f"{base_name}.{output_format}"
        
        # Save the image in the new format. Pillow automatically handles the conversion.
        # It's important to use a lowercase extension for consistency.
        
        # Map common output formats to Pillow's expected format strings
        pillow_formats = {
            'jpg': 'JPEG',
            'jpeg': 'JPEG',
            'ico': 'ICO',
            'pdf': 'PDF'
        }
        
        # Get the Pillow-specific format, defaulting to the uppercase version of the input
        # if no specific mapping is found.
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
        print(f"An unexpected error occurred during conversion: {e}")

import winreg
import sys
import ctypes

# Get the absolute path to the current executable
CURRENT_EXECUTABLE_PATH = sys.argv[0]

# Supported output formats for the context menu
SUPPORTED_OUTPUT_FORMATS = ['bmp', 'gif', 'ico', 'jpeg', 'png', 'pdf', 'tiff', 'webp']

def add_context_menu_entry(file_type, menu_name, command, icon_path=None):
    try:
        # Create the main menu entry
        key_path = rf"Software\Classes\{file_type}\shell\{menu_name}"
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
        if icon_path:
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, icon_path)
        winreg.CloseKey(key)

        # Create the command sub-key
        command_key_path = rf"{key_path}\command"
        command_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, command_key_path)
        winreg.SetValueEx(command_key, None, 0, winreg.REG_SZ, command)
        winreg.CloseKey(command_key)
        print(f"Added context menu for {file_type}: {menu_name}")
    except Exception as e:
        print(f"Error adding context menu for {file_type}: {menu_name} - {e}")

def add_subcommand_entry(parent_key_path, submenu_name, command):
    try:
        # Create the submenu entry (e.g., "BMP")
        submenu_key_path = rf"{parent_key_path}\shell\{submenu_name}"
        submenu_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, submenu_key_path)
        winreg.CloseKey(submenu_key)

        # Create the command sub-key for the submenu
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
        winreg.SetValueEx(key, "SubCommands", 0, winreg.REG_SZ, "") # Indicate it's a submenu
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
                # Enumerate subkeys
                sub = winreg.EnumKey(reg_key, 0)
                delete_key_recursive(reg_key, sub)
            except OSError:
                # No more subkeys, break the loop
                break
        winreg.CloseKey(reg_key)
        winreg.DeleteKey(hkey, subkey)
    except FileNotFoundError:
        pass # Key already deleted or never existed
    except Exception as e:
        print(f"Error deleting key recursively {subkey}: {e}")

def is_admin():
    try:
        return os.getuid() == 0 # For Unix-like systems
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() # For Windows

def check_if_entries_exist():
    main_menu_name = "Convert Image(s) To"
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
        sys.exit(1)

    # Add context menu for all image files (using SystemFileAssociations\image)
    main_menu_name = "Convert Image(s) To"
    
    # For individual image files
    image_file_type = r"SystemFileAssociations\image"
    main_key_path_image = add_main_context_menu_entry_with_subcommands(image_file_type, main_menu_name)
    if main_key_path_image:
        for output_format in SUPPORTED_OUTPUT_FORMATS:
            command = f'\"{CURRENT_EXECUTABLE_PATH}\" \"%1\" {output_format}'
            add_subcommand_entry(main_key_path_image, output_format.upper(), command)

    # For directories (when right-clicking on a folder)
    directory_file_type = "Directory"
    main_key_path_directory = add_main_context_menu_entry_with_subcommands(directory_file_type, main_menu_name)
    if main_key_path_directory:
        for output_format in SUPPORTED_OUTPUT_FORMATS:
            command = f'\"{CURRENT_EXECUTABLE_PATH}\" \"%1\" {output_format} -r'
            add_subcommand_entry(main_key_path_directory, output_format.upper(), command)

    # For directory background (when right-clicking in an empty space within a folder)
    directory_background_file_type = r"Directory\Background"
    main_key_path_directory_bg = add_main_context_menu_entry_with_subcommands(directory_background_file_type, main_menu_name)
    if main_key_path_directory_bg:
        for output_format in SUPPORTED_OUTPUT_FORMATS:
            command = f'\"{CURRENT_EXECUTABLE_PATH}\" \"%V\" {output_format} -r'
            add_subcommand_entry(main_key_path_directory_bg, output_format.upper(), command)
    
    print("Context menu entries added successfully. You might need to restart Explorer or your computer for changes to take effect.")

def unregister_context_menu():
    if not is_admin():
        print("This script needs to be run with administrator privileges to modify the registry.")
        print("Please right-click on your terminal/command prompt and select 'Run as administrator'.")
        sys.exit(1)

    main_menu_name = "Convert Image(s) To"

    # Remove for individual image files
    image_file_type = r"SystemFileAssociations\image"
    main_key_path_image = rf"Software\Classes\{image_file_type}\shell\{main_menu_name}"
    for output_format in SUPPORTED_OUTPUT_FORMATS:
        remove_subcommand_entry(main_key_path_image, output_format.upper())
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, main_key_path_image, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, "SubCommands")
        winreg.CloseKey(key)
        # Recursively delete the main key
        delete_key_recursive(winreg.HKEY_CURRENT_USER, main_key_path_image)
        print(f"Removed main '{main_menu_name}' menu for image files.")
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Error removing main '{main_menu_name}' menu for image files: {e}")

    # Remove for directories
    directory_file_type = "Directory"
    main_key_path_directory = rf"Software\Classes\{directory_file_type}\shell\{main_menu_name}"
    for output_format in SUPPORTED_OUTPUT_FORMATS:
        remove_subcommand_entry(main_key_path_directory, output_format.upper())
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
    for output_format in SUPPORTED_OUTPUT_FORMATS:
        remove_subcommand_entry(main_key_path_directory_bg, output_format.upper())
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, main_key_path_directory_bg, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, "SubCommands")
        winreg.CloseKey(key)
        # Recursively delete the main key
        delete_key_recursive(winreg.HKEY_CURRENT_USER, main_key_path_directory_bg)
        print(f"Removed main '{main_menu_name}' menu for directory background.")
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Error removing main '{main_menu_name}' menu for directory background: {e}")

    print("Context menu entries removed successfully. You might need to restart Explorer or your computer for changes to take effect.")

def main():
    """
    The main function to handle command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Convert image formats and manage context menu entries.")

    parser.add_argument("--register", action="store_true", help="Register context menu entries.")
    parser.add_argument("--unregister", action="store_true", help="Unregister context menu entries.")
    parser.add_argument("input_path", nargs='?', help="Path to the input image file or a directory containing images.")
    parser.add_argument("output_format", nargs='?', help="Desired output format (e.g., png, jpg, webp, ico, pdf).")
    parser.add_argument("-r", "--recursive", action="store_true", help="Recursively search for images in subdirectories when input_path is a directory.")
    
    args = parser.parse_args()

    if args.register:
        register_context_menu()
    elif args.unregister:
        unregister_context_menu()
    elif args.input_path and args.output_format:
        input_path = args.input_path
        output_format = args.output_format.lower()

        if os.path.isdir(input_path):
            # Directory conversion
            image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tiff', '.ico') # Add more as needed
            
            for root, _, files in os.walk(input_path):
                for file in files:
                    if file.lower().endswith(image_extensions):
                        current_input_file_path = os.path.join(root, file)
                        convert_image(current_input_file_path, output_format)
                if not args.recursive:
                    break # Only process the top-level directory if not recursive
        elif os.path.isfile(input_path):
            # Single file conversion
            convert_image(input_path, output_format)
        else:
            print(f"Error: The provided path '{input_path}' is neither a file nor a directory.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
