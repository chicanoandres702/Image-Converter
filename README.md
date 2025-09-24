# Image Converter

This is a simple command-line tool written in Python for converting image files from one format to another. It leverages the powerful Pillow library to handle various image types and ensures a straightforward conversion process.

## Features

*   **Versatile Conversion:** Convert images between a wide range of formats supported by Pillow (e.g., JPG, PNG, WEBP, BMP, GIF, ICO, PDF).
*   **Command-Line Interface:** Easy to use directly from your terminal.
*   **Automatic Naming:** Converted files are saved with the same base name as the input file, with the new extension, in the current directory.
*   **Error Handling:** Includes basic error handling for file not found issues and other conversion problems.

## Requirements

This script requires the `Pillow` library. If you don't have it installed, you can do so using pip:

```bash
pip install Pillow
```

## Usage

To use the image converter, run the `image_converter.py` script from your terminal. The script will automatically detect if the provided `input_path` is a single file or a directory.

```bash
python image_converter.py <input_path> <output_format> [-r]
```

**Arguments:**

*   `<input_path>`: The path to the input image file (for single conversion) OR the path to a directory containing image files (for batch conversion).
*   `<output_format>`: The desired format for the output image(s) (e.g., `png`, `jpg`, `webp`, `ico`, `pdf`).
*   `-r`, `--recursive` (optional): When `<input_path>` is a directory, this flag will make the script recursively search for images in subdirectories.

### Examples

1.  **Convert a single JPG image to PNG:**

    ```bash
    python image_converter.py my_photo.jpg png
    ```

2.  **Convert all supported images in a directory to JPG:**

    ```bash
    python image_converter.py my_images jpg
    ```

3.  **Convert all supported images in a directory and its subdirectories to PNG (recursive):**

    ```bash
    python image_converter.py my_images png -r
    ```

## Supported Formats

The script supports most image formats that the Pillow library can handle. Common supported formats include:

*   JPEG (`jpg`, `jpeg`)
*   PNG (`png`)
*   WEBP (`webp`)
*   BMP (`bmp`)
*   GIF (`gif`)
*   ICO (`ico`)
*   PDF (`pdf`)

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

For Windows users, this project provides a utility script (`register_converter.py`) to integrate the image conversion functionality directly into your right-click context menu for image files and directories.

### How it Works

The `register_converter.py` script adds "Convert To" submenus to the context menu:

*   **For Image Files:** When you right-click on a supported image file, a "Convert To" submenu will appear, offering various output formats (e.g., BMP, ICO, JPEG, PNG, PDF). Selecting an option will convert the image to that format.
*   **For Directories:** When you right-click on a directory, a "Convert All Images To" submenu will appear. Selecting an option will convert all supported image files within that directory (and its subdirectories if the recursive option is enabled in the command) to the chosen format.

### Usage

**Important:** You must run `register_converter.py` with **administrator privileges** for it to modify the Windows Registry. Right-click on your terminal/command prompt and select "Run as administrator".

1.  **Add Context Menu Entries:**

    Navigate to the project directory in an **administrator** command prompt and run:

    ```bash
    python register_converter.py add
    ```

    You might need to restart Windows Explorer (or your computer) for the changes to take effect.

2.  **Remove Context Menu Entries:**

    If you wish to remove the context menu entries, run the script with the `remove` action:

    ```bash
    python register_converter.py remove
    ```

    Again, a restart of Windows Explorer or your computer might be necessary.
