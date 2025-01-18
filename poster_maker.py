import configparser
import pathlib
import sys
from typing import List, Tuple

from PIL import Image


class ImageCombiner:
    """
    Combines multiple PNG images into a single larger image based on a configuration file.
    """

    def __init__(self, config_file:pathlib.Path):
        """
        Initializes the ImageCombiner with the path to the configuration file.

        Args:
            config_file (pathlib.Path): Path to the configuration file.
        """
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        self.image_folder = self._get_image_folder()  # Get the single image folder
        self.image_paths = self._get_image_paths()
        self.rows = len(self.image_paths)
        self.cols = len(self.image_paths[0]) if self.rows > 0 else 0
        self.output_filename = pathlib.Path(self.config.get('output', 'filename', fallback='combined_image.png'))
        self.background_color = self._get_background_color()

    def _get_image_folder(self):
        """
        Parses the configuration file for the single image folder path.

        Returns:
            pathlib.Path: A Path object representing the image folder.
        """
        if 'image_folder' in self.config:
            folder_path = pathlib.Path(self.config['image_folder']['path']).expanduser()
            if folder_path.is_dir():
                return folder_path
            else:
                print(f"Warning: Image folder '{folder_path}' not found.")
        return None

    def _get_image_paths(self) -> List[List[pathlib.Path]]:
        """
        Parses the configuration file and returns a 2D list of image paths
        within the specified single image folder.

        Returns:
            list[list[pathlib.Path]]: A 2D list where each inner list represents a row of image paths.
        """
        image_paths = []
        if self.image_folder:
            for row_index in range(self.config.getint('layout', 'rows', fallback=0)):
                row_key = f'row{row_index}'
                if row_key in self.config['images']:
                    row_paths = []
                    for image_file in self.config['images'][row_key].split(','):
                        image_file = image_file.strip()
                        image_path = self.image_folder / image_file
                        if image_path.is_file():
                            row_paths.append(image_path)
                        else:
                            print(f"Warning: Image '{image_file}' not found in folder '{self.image_folder}'.")
                    image_paths.append(row_paths)
                else:
                    print(f"Warning: Row '{row_key}' not found in the configuration file.")
        return image_paths

    def _get_background_color(self) -> Tuple[int, int, int]:
        """
        Retrieves the background color from the configuration file.

        Returns:
            tuple: The background color as an RGB tuple.
        """
        color_str = self.config.get('output', 'background_color', fallback='255,255,255')
        try:
            return tuple(map(int, color_str.split(',')))
        except ValueError:
            print("Warning: Invalid background color format. Using white (255, 255, 255).")
            return (255, 255, 255)

    def combine_images(self):
        """
        Combines the images according to the configuration and saves the result.
        """
        if not self.image_paths:
            print("Error: No image paths found in the configuration file.")
            return

        try:
            first_image = Image.open(self.image_paths[0][0])
            width, height = first_image.size
            first_image.close()
        except (FileNotFoundError, UnboundLocalError):
            print(f"Error: Image file not found: {self.image_paths[0][0]}")
            return
        except Exception as e:
            print(f"Error: An unexpected error occurred while opening the image: {e}")
            return

        combined_width = width * self.cols
        combined_height = height * self.rows
        combined_image = Image.new('RGBA', (combined_width, combined_height), self.background_color)

        y_offset = 0
        for row_paths in self.image_paths:
            x_offset = 0
            for image_path in row_paths:
                try:
                    img = Image.open(image_path)
                    if img.size != (width, height):
                        print(f"Warning: Image '{image_path}' has different dimensions. Resizing to {width}x{height}.")
                        img = img.resize((width, height))

                    combined_image.paste(img, (x_offset, y_offset))
                    x_offset += width
                    img.close()
                except FileNotFoundError:
                    print(f"Error: Image file not found: {image_path}")
                except Exception as e:
                    print(f"Error: An unexpected error occurred while processing '{image_path}': {e}")

            y_offset += height

        # Ensure the parent directory of the output file exists
        self.output_filename.parent.mkdir(parents=True, exist_ok=True)

        combined_image.save(self.output_filename)
        print(f"Combined image saved as {self.output_filename}")
        combined_image.close()


def write_default_cfg_file(config_file:pathlib.Path) -> int:
    return config_file.write_text(
        '[layout]\n'
        'rows = 2\n'
        '\n'
        '[image_folder]\n'  # Use singular 'image_folder'
        'path = ./images\n'  # Specify the single folder path
        '\n'
        '[images]\n'
        'row0 = image1.png, image2.png\n'
        'row1 = image3.png, image4.png\n'
        '\n'
        '[output]\n'
        'filename = output/combined.png\n'
        'background_color = 255,255,255\n'
    )


def write_default_img_files(default_folder:pathlib.Path):
    default_folder.mkdir(parents=True, exist_ok=True)
    for i in range(1, 5):  # Create 4 images
        img = Image.new('RGB', (100, 100), color=(i * 25, i * 10, i * 5))
        img.save(default_folder / f'image{i}.png')


def main(argv:List[str]):
    if len(argv) > 1:
        config_fname = argv[1]
    else:
        config_fname = 'poster.cfg'

    config_file = pathlib.Path(config_fname).resolve()

    if not config_file.exists():
        # Create a dummy config file and images in the specified folder
        default_folder = pathlib.Path('./images').resolve()

        write_default_cfg_file(config_file, default_folder)

        # Create a dummy image folder and files
        write_default_img_files(default_folder)

    combiner = ImageCombiner(config_file)
    combiner.combine_images()


if __name__ == "__main__":
    main(sys.argv)
