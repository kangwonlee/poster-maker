import os
import pathlib

import pytest
from PIL import Image

from poster_maker import ImageCombiner, write_default_cfg_file, write_default_img_files


def test_combine_images_valid_config(valid_config_file, temp_test_dir):
    """
    Test image combination with a valid configuration file.
    """
    combiner = ImageCombiner(pathlib.Path(valid_config_file))
    combiner.combine_images()
    output_image_path = pathlib.Path(temp_test_dir) / 'output' / 'combined.png'
    assert output_image_path.is_file()
    # You can add more assertions here to check the dimensions, etc. of the output image
    # For example, to check the dimensions:
    with Image.open(output_image_path) as img:
        width, height = img.size
    assert width == 200  # 2 images of width 100 each in a row
    assert height == 200  # 2 rows of height 100 each


def test_write_default_cfg_file(temp_test_dir):
    """
    Test the creation of a default configuration file.
    """
    config_file_path = os.path.join(temp_test_dir, "default.cfg")
    write_default_cfg_file(pathlib.Path(config_file_path))
    assert os.path.isfile(config_file_path)
    # Add more assertions to check the content of the default config file


def test_write_default_img_files(temp_test_dir):
    """
    Test the creation of default image files.
    """
    images_dir = os.path.join(temp_test_dir, "images")
    write_default_img_files(pathlib.Path(images_dir))
    assert os.path.isdir(images_dir)
    # Assert that 4 images have been created
    for i in range(1, 5):
        assert os.path.isfile(os.path.join(images_dir, f"image{i}.png"))


def test_invalid_config_missing_rows(invalid_config_missing_rows, temp_test_dir, capsys):
    """
    Test behavior with a configuration file missing the 'rows' entry.
    """
    combiner = ImageCombiner(pathlib.Path(invalid_config_missing_rows))
    combiner.combine_images()
    captured = capsys.readouterr()  # Capture stdout/stderr
    assert "Error: No image paths found in the configuration file." in captured.out


def test_invalid_config_missing_image_folder(invalid_config_missing_image_folder, temp_test_dir, capsys):
    """
    Test behavior with a configuration file missing the 'image_folder' section.
    """
    combiner = ImageCombiner(pathlib.Path(invalid_config_missing_image_folder))
    combiner.combine_images()
    captured = capsys.readouterr()
    assert "Error: No image paths found in the configuration file." in captured.out


if "__main__" == __name__:
    pytest.main(['-vv', __file__])
