# This script is a command-line tool for converting image formats.
# It requires the Pillow library, which can be installed with:
# pip install Pillow

import argparse
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
    parser = argparse.ArgumentParser(description="Convert image formats.")
    parser.add_argument("input_path", help="Path to the input image file.")
    parser.add_argument("output_format", help="Desired output format (e.g., png, jpg, webp, ico, pdf).")
    
    args = parser.parse_args()
    
    # Call the conversion function
    convert_image(args.input_path, args.output_format.lower())

if __name__ == "__main__":
    main()
