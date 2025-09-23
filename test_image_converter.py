import os
import pytest
from unittest.mock import patch, MagicMock
from image_converter import convert_image
from PIL import UnidentifiedImageError

# Define a temporary directory for test output
@pytest.fixture
def temp_output_dir(tmp_path):
    return tmp_path

# Test successful conversion
def test_convert_image_success(temp_output_dir):
    mock_image = MagicMock()
    mock_image.save.return_value = None

    with patch('PIL.Image.open', return_value=mock_image) as mock_image_open:
        with patch('builtins.print') as mock_print:
            input_path = "/path/to/test.png"
            output_format = "jpg"
            convert_image(input_path, output_format)
            
            mock_image_open.assert_called_once_with(input_path)
            mock_image.save.assert_called_once_with("test.jpg", format="JPEG")
            mock_print.assert_called_once_with(f"Success! Converted '{input_path}' to 'test.jpg'.")

# Test FileNotFoundError
def test_convert_image_file_not_found():
    with patch('os.path.exists', return_value=False):
        with patch('builtins.print') as mock_print:
            input_path = "/path/to/nonexistent.png"
            output_format = "jpg"
            convert_image(input_path, output_format)
            mock_print.assert_called_once_with(f"Error: The input file '{input_path}' was not found.")

# Test UnidentifiedImageError
def test_convert_image_unidentified_image_error():
    with patch('os.path.exists', return_value=True):
        with patch('PIL.Image.open', side_effect=UnidentifiedImageError):
            with patch('builtins.print') as mock_print:
                input_path = "/path/to/corrupt.txt"
                output_format = "jpg"
                convert_image(input_path, output_format)
                mock_print.assert_called_once_with(f"Error: Could not identify image file '{input_path}'. It might be corrupt or an unsupported format.")

# Test OSError during save (e.g., unsupported conversion)
def test_convert_image_os_error_on_save():
    mock_image = MagicMock()
    mock_image.save.side_effect = OSError("cannot write mode P as JPEG")

    with patch('os.path.exists', return_value=True):
        with patch('PIL.Image.open', return_value=mock_image):
            with patch('builtins.print') as mock_print:
                input_path = "/path/to/test.png"
                output_format = "jpg"
                convert_image(input_path, output_format)
                mock_print.assert_called_once_with(f"Error: Failed to save image to 'test.jpg'. This might be due to an unsupported output format for the given image data, or a permissions issue. Details: cannot write mode P as JPEG")

# Test generic Exception
def test_convert_image_generic_exception():
    mock_image = MagicMock()
    mock_image.save.side_effect = Exception("Something unexpected happened")

    with patch('os.path.exists', return_value=True):
        with patch('PIL.Image.open', return_value=mock_image):
            with patch('builtins.print') as mock_print:
                input_path = "/path/to/test.png"
                output_format = "jpg"
                convert_image(input_path, output_format)
                mock_print.assert_called_once_with(f"An unexpected error occurred during conversion: Something unexpected happened")
