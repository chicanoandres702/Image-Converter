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

def main():
    """
    The main function to handle command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Convert image formats.")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("input_path", nargs='?', help="Path to the input image file (for single file conversion).")
    group.add_argument("-d", "--directory", help="Path to a directory containing image files to convert.")

    parser.add_argument("output_format", help="Desired output format (e.g., png, jpg, webp, ico, pdf).")
    parser.add_argument("-r", "--recursive", action="store_true", help="Recursively search for images in subdirectories when using --directory.")
    
    args = parser.parse_args()
    
    if args.input_path:
        # Single file conversion
        convert_image(args.input_path, args.output_format.lower())
    elif args.directory:
        # Directory conversion
        if not os.path.isdir(args.directory):
            print(f"Error: Directory '{args.directory}' not found.")
            return

        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tiff', '.ico') # Add more as needed
        
        for root, _, files in os.walk(args.directory):
            for file in files:
                if file.lower().endswith(image_extensions):
                    input_file_path = os.path.join(root, file)
                    convert_image(input_file_path, args.output_format.lower())
            if not args.recursive:
                break # Only process the top-level directory if not recursive

if __name__ == "__main__":
    main()
