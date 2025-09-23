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

To use the image converter, run the `image_converter.py` script from your terminal, providing the input image path and the desired output format as arguments.

```bash
python image_converter.py <input_image_path> <output_format>
```

**Arguments:**

*   `<input_image_path>`: The path to the image file you want to convert.
*   `<output_format>`: The desired format for the output image (e.g., `png`, `jpg`, `webp`, `ico`, `pdf`).

### Examples

1.  **Convert a JPG image to PNG:**

    ```bash
    python image_converter.py my_photo.jpg png
    ```

2.  **Convert a PNG image to ICO:**

    ```bash
    python image_converter.py icon.png ico
    ```

3.  **Convert a TIFF image to PDF:**

    ```bash
    python image_converter.py document.tiff pdf
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