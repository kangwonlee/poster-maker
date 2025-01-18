import configparser
import pathlib
import sys


from PIL import Image


class ImageCombiner:
    """
    Combines multiple PNG images into a single larger image based on a configuration file.
    """

    def __init__(self, config_file):
        """
        Initializes the ImageCombiner with the path to the configuration file.

        Args:
            config_file (pathlib.Path): Path to the configuration file (e.g., 'poster.cfg').
        """
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        self.image_paths = self._get_image_paths()
        self.rows = len(self.image_paths)
        self.cols = len(self.image_paths[0]) if self.rows > 0 else 0
        self.output_filename = self.config.get('output', 'filename', fallback='combined_image.png')
        self.background_color = self._get_background_color()

    def _get_image_paths(self):
        """
        Parses the configuration file and returns a 2D list of image paths.

        Returns:
            list[list[str]]: A 2D list where each inner list represents a row of image paths.
        """
        image_paths = []
        for row_index in range(self.config.getint('layout', 'rows', fallback=0)):
            row_key = f'row{row_index}'
            if row_key in self.config['images']:
                row_paths = [
                    path.strip() for path in self.config['images'][row_key].split(',')
                ]
                image_paths.append(row_paths)
            else:
                print(f"Warning: Row '{row_key}' not found in the configuration file.")
        return image_paths

    def _get_background_color(self):
        """
        Retrieves the background color from the configuration file.

        Returns:
            tuple: The background color as an RGB tuple (e.g., (255, 255, 255)).
                   Defaults to white (255, 255, 255) if not specified.
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

        # Determine individual image dimensions (assuming all images have the same size)
        try:
            first_image = Image.open(self.image_paths[0][0])
        except FileNotFoundError:
            print(f"Error: Image file not found: {self.image_paths[0][0]}")
            return
        except Exception as e:
            print(f"Error: An unexpected error occurred while opening the image: {e}")
            return

        width, height = first_image.size
        first_image.close()

        # Create a new image with the calculated dimensions and background color
        combined_width = width * self.cols
        combined_height = height * self.rows
        combined_image = Image.new('RGBA', (combined_width, combined_height), self.background_color)

        # Paste each image into the combined image
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

        # Save the combined image
        combined_image.save(self.output_filename)
        print(f"Combined image saved as {self.output_filename}")
        combined_image.close()


def main(argv):
        # Example usage:
        if len(argv) > 1:
            config_fname = argv[1]
        else:
            config_fname = 'poster.cfg'  # Path to your configuration file

        config_file = pathlib.Path(config_fname).resolve()

        # Create a dummy config file if it doesn't exist
        if not config_file.exists(config_file):
            config_file.write_text(
                    '[layout]\n'
                    'rows = 3\n'
                    '\n'
                    '[images]\n'
                    'row0 = image1.png, image2.png, image3.png\n'
                    'row1 = image4.png, image5.png, image6.png\n'
                    'row2 = image7.png, image8.png, image9.png, image10.png\n'
                    '\n'
                    '[output]\n'
                    'filename = output.png\n'
                    'background_color = 255,255,255\n'
            )

            # Create dummy image files for testing
            for i in range(1, 11):
                img = Image.new('RGB', (100, 100), color=(i * 25, i * 10, i * 5))  # Example colors
                img.save(f'image{i}.png')

        combiner = ImageCombiner(config_file)
        combiner.combine_images()    


if __name__ == "__main__":
    main(sys.argv)
