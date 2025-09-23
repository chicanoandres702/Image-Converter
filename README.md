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