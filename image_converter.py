# This script is a command-line tool for converting image formats.
# It requires the Pillow library, which can be installed with:
# pip install Pillow

import sys
import os
from PIL import Image

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
        # This case is handled by the initial check, but it's good practice to keep it.
        print(f"Error: The file '{input_path}' was not found.")
    except Exception as e:
        # Catch any other potential errors during conversion (e.g., invalid format)
        print(f"An error occurred during conversion: {e}")

def main():
    """
    The main function to handle command-line arguments.
    """
    # Check if the correct number of arguments were provided
    if len(sys.argv) < 3:
        print("Usage: python image_converter.py <input_image_path> <output_format>")
        print("Example: python image_converter.py my_photo.jpg png")
        print("Supported formats depend on Pillow, but common ones include jpg, png, webp, bmp, gif, ico, pdf.")
        return

    # Get the input file path from the first argument
    input_file = sys.argv[1]
    
    # Get the desired output format from the second argument
    # Convert it to lowercase for standardization
    output_format = sys.argv[2].lower()

    # Call the conversion function
    convert_image(input_file, output_format)

if __name__ == "__main__":
    main()
