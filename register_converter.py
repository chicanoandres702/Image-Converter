import winreg
import os
import sys
import argparse

# Get the absolute path to the image_converter.py script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_CONVERTER_PATH = os.path.join(SCRIPT_DIR, "image_converter.py")
PYTHON_EXE = sys.executable

# Supported output formats for the context menu
SUPPORTED_OUTPUT_FORMATS = ['bmp', 'gif', 'ico', 'jpeg', 'png', 'pdf', 'tiff', 'webp']

# Common image file extensions to add context menu for
IMAGE_EXTENSIONS = [
    '.bmp', '.dib', '.eps', '.gif', '.icns', '.ico', '.im', '.jpeg', '.jpg', '.jpe',
    '.jp2', '.msp', '.pcx', '.png', '.pbm', '.pgm', '.ppm', '.psd', '.sgi', '.spi',
    '.tga', '.tiff', '.tif', '.webp', '.xbm', '.xpm'
]

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

def is_admin():
    try:
        return os.getuid() == 0 # For Unix-like systems
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() # For Windows

def main():
    if not is_admin():
        print("This script needs to be run with administrator privileges to modify the registry.")
        print("Please right-click on your terminal/command prompt and select 'Run as administrator'.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Add or remove 'Convert To' context menu entries for image files and directories.")
    parser.add_argument("action", nargs='?', default=None, choices=["add", "remove"], help="Action to perform: 'add' to add entries, 'remove' to remove them. If omitted, toggles the entries.")
    
    args = parser.parse_args()

    if args.action == "add":
        # Add context menu for all image files (using SystemFileAssociations\image)
        main_menu_name = "Convert Image(s) To"
        
        # For individual image files
        image_file_type = r"SystemFileAssociations\image"
        main_key_path_image = add_main_context_menu_entry_with_subcommands(image_file_type, main_menu_name)
        if main_key_path_image:
            for output_format in SUPPORTED_OUTPUT_FORMATS:
                command = f'"{PYTHON_EXE}" "{IMAGE_CONVERTER_PATH}" "%1" {output_format}'
                add_subcommand_entry(main_key_path_image, output_format.upper(), command)

        # For directories (when right-clicking on a folder)
        directory_file_type = "Directory"
        main_key_path_directory = add_main_context_menu_entry_with_subcommands(directory_file_type, main_menu_name)
        if main_key_path_directory:
            for output_format in SUPPORTED_OUTPUT_FORMATS:
                command = f'"{PYTHON_EXE}" "{IMAGE_CONVERTER_PATH}" "%1" {output_format} -r'
                add_subcommand_entry(main_key_path_directory, output_format.upper(), command)

        # For directory background (when right-clicking in an empty space within a folder)
        directory_background_file_type = r"Directory\Background"
        main_key_path_directory_bg = add_main_context_menu_entry_with_subcommands(directory_background_file_type, main_menu_name)
        if main_key_path_directory_bg:
            for output_format in SUPPORTED_OUTPUT_FORMATS:
                command = f'"{PYTHON_EXE}" "{IMAGE_CONVERTER_PATH}" "%V" {output_format} -r'
                add_subcommand_entry(main_key_path_directory_bg, output_format.upper(), command)
        
        print("Context menu entries added successfully. You might need to restart Explorer or your computer for changes to take effect.")

    elif args.action == "remove":
        main_menu_name = "Convert Image(s) To"

        # Remove for individual image files
        image_file_type = r"SystemFileAssociations\image"
        main_key_path_image = rf"Software\Classes\{image_file_type}\shell\{main_menu_name}"
        for output_format in SUPPORTED_OUTPUT_FORMATS:
            remove_subcommand_entry(main_key_path_image, output_format.upper())
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, main_key_path_image)
            print(f"Removed main '{main_menu_name}' menu for image files.")
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error removing main '{main_menu_name}' menu for image files: {{e}}")

        # Remove for directories
        directory_file_type = "Directory"
        main_key_path_directory = rf"Software\Classes\{directory_file_type}\shell\{main_menu_name}"
        for output_format in SUPPORTED_OUTPUT_FORMATS:
            remove_subcommand_entry(main_key_path_directory, output_format.upper())
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, main_key_path_directory)
            print(f"Removed main '{main_menu_name}' menu for directories.")
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error removing main '{main_menu_name}' menu for directories: {{e}}")

        # Remove for directory background
        directory_background_file_type = r"Directory\Background"
        main_key_path_directory_bg = rf"Software\Classes\{directory_background_file_type}\shell\{main_menu_name}"
        for output_format in SUPPORTED_OUTPUT_FORMATS:
            remove_subcommand_entry(main_key_path_directory_bg, output_format.upper())
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, main_key_path_directory_bg)
            print(f"Removed main '{main_menu_name}' menu for directory background.")
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error removing main '{main_menu_name}' menu for directory background: {{e}}")

        print("Context menu entries removed successfully. You might need to restart Explorer or your computer for changes to take effect.")

if __name__ == "__main__":
    main()
