import configparser
import os
import shutil
import tempfile

import pytest
from PIL import Image


@pytest.fixture(scope="session")
def temp_test_dir():
    """
    Creates a temporary directory for testing.

    This fixture is session-scoped, meaning it will be set up once
    before the first test starts and torn down once after the last test ends.
    """
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def test_image_folder(temp_test_dir):
    """
    Creates a temporary folder with sample test images.
    """
    img_folder = os.path.join(temp_test_dir, "test_images")
    os.makedirs(img_folder, exist_ok=True)
    for i in range(1, 5):
        img = Image.new('RGB', (100, 100), color=(i * 25, i * 10, i * 5))
        img.save(os.path.join(img_folder, f'image{i}.png'))
    return img_folder


@pytest.fixture
def valid_config_file(temp_test_dir, test_image_folder):
    """
    Creates a temporary valid configuration file.
    """
    config_path = os.path.join(temp_test_dir, "test_config.cfg")
    config = configparser.ConfigParser()
    config['layout'] = {'rows': '2'}
    config['image_folder'] = {'path': test_image_folder}
    config['images'] = {
        'row0': 'image1.png, image2.png',
        'row1': 'image3.png, image4.png'
    }
    config['output'] = {
        'filename': os.path.join(temp_test_dir, 'output', 'combined.png'),
        'background_color': '255,255,255'
    }
    with open(config_path, 'w') as f:
        config.write(f)
    return config_path


@pytest.fixture
def invalid_config_missing_rows(temp_test_dir, test_image_folder):
    """
    Creates a temporary invalid configuration file (missing rows).
    """
    config_path = os.path.join(temp_test_dir, "missing_rows.cfg")
    config = configparser.ConfigParser()
    config['image_folder'] = {'path': test_image_folder}
    config['images'] = {
        'row0': 'image1.png, image2.png',
        'row1': 'image3.png, image4.png'
    }
    config['output'] = {
        'filename': os.path.join(temp_test_dir, 'output', 'combined.png'),
        'background_color': '255,255,255'
    }
    with open(config_path, 'w') as f:
        config.write(f)
    return config_path


@pytest.fixture
def invalid_config_missing_image_folder(temp_test_dir):
    """
    Creates a temporary invalid configuration file (missing image folder).
    """
    config_path = os.path.join(temp_test_dir, "missing_image_folder.cfg")
    config = configparser.ConfigParser()
    config['layout'] = {'rows': '2'}
    config['images'] = {
        'row0': 'image1.png, image2.png',
        'row1': 'image3.png, image4.png'
    }
    config['output'] = {
        'filename': os.path.join(temp_test_dir, 'output', 'combined.png'),
        'background_color': '255,255,255'
    }
    with open(config_path, 'w') as f:
        config.write(f)
    return config_path
