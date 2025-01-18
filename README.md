[![Poster Maker CI/CD](https://github.com/kangwonlee/poster-maker/actions/workflows/poster-maker.yaml/badge.svg)](https://github.com/kangwonlee/poster-maker/actions/workflows/poster-maker.yaml)
# Poster Maker

This Python script helps you create a single, well-structured image file for your poster presentations by combining multiple PNG images based on a simple configuration file. It's designed to assist researchers, academics, and students in preparing their posters for conferences, symposia, or any event where visual presentation of data is required.

**Important Note:** This tool helps generate a single image file that you can then integrate into your poster layout using presentation software like PowerPoint, Keynote, or LaTeX. It does **not** handle the entire poster layout process (e.g., text, titles, headers). You will need to use a separate tool to create the final poster design.

## Features

-   **Configurable Layout:** Define the number of rows and the images to be included in each row through a simple configuration file.
-   **Single Image Folder:** Specify a single folder containing all the images (figures, charts, etc.) you want to include in your poster.
-   **Customizable Output:** Set the output filename and background color.
-   **Automatic Resizing:** If images have different dimensions, they are automatically resized to match the dimensions of the first image, ensuring uniformity in your poster components.
-   **Error Handling:** Includes warnings for missing images or folders and error messages for file access or processing issues.
-   **Default Configuration and Images:** Generates a default configuration file and sample images if no configuration file is provided, to get you started quickly.

## Requirements

-   Python 3.x
-   Pillow (PIL Fork)

## Installation

1.  Clone the repository:

    ```zsh
    git clone [repository-url]
    cd poster-maker
    ```
    Replace `[repository-url]` with the GitHub repository url.

2.  Install the required library (Pillow):

    ```zsh
    pip install Pillow
    ```

## Usage

1.  **Prepare your images:** Place all the PNG images (figures, charts, results) you want to include in your poster in a single folder.
2.  **Create a configuration file (or use the default):**

    -   If you run the script without a configuration file, it will create a default `poster.cfg` file and a folder named `images` with some sample images.
    -   You can modify the `poster.cfg` file to specify your images, layout, and output settings.

    Here's an example `poster.cfg` file:

    ```cfg
    [layout]
    rows = 3

    [image_folder]
    path = ./images

    [images]
    row0 = figure1.png, figure2.png
    row1 = results_chart.png
    row2 = diagram1.png, diagram2.png, diagram3.png

    [output]
    filename = output/combined_figures.png
    background_color = 255,255,255
    ```

    -   **`layout` section:**
        -   `rows`: Specifies the number of rows in the output image. This helps you organize your figures and results logically.
    -   **`image_folder` section:**
        -   `path`: Specifies the path to the folder containing your images. This can be a relative or absolute path. It also supports the use of `~` to represent the user's home directory (e.g., `~/my_poster_images`).
    -   **`images` section:**
        -   `row0`, `row1`, `row2`, etc.: Defines the images for each row. List the filenames separated by commas. The script will automatically create columns based on the number of images in each row.
    -   **`output` section:**
        -   `filename`: The name of the output file (the combined image). The script will create necessary directories if they don't exist.
        -   `background_color`: The background color of the output image in RGB format (e.g., `255,255,255` for white).

3.  **Run the script:**

    ```zsh
    python poster_maker.py
    ```

    Or, if you want to use a custom configuration file name:

    ```zsh
    python poster_maker.py my_config.cfg
    ```

4.  **Integrate into your poster:** The script will generate a single image file (e.g., `combined_figures.png`) containing your combined figures. You can now insert this image into your poster layout using presentation software like PowerPoint, Keynote, or LaTeX.

## Important Considerations for Poster Presentations

- **Set up in advance:** Attach your poster to the poster board in your session room at least 10 minutes before the session starts.
- **Be present:** Remain with your poster throughout the poster session to answer questions and discuss your work.
- **Elucidate:** Be prepared to present and explain your research and results to the audience.
- **Remove promptly:** Remove your poster immediately after the session finishes.
- **Poster Size:** Consult the specific conference or event guidelines for poster size requirements. This tool does not automatically resize the final output to specific poster dimensions. You will need to ensure your combined image and overall poster design fit within the allowed size.

## Example

Let's say you have five images (`figure1.png`, `figure2.png`, `results_chart.png`, `diagram1.png`, `diagram2.png`) in a folder named `images`, and you want to organize them into a logical layout for your poster.

1.  Your `poster.cfg` file might look like this:

    ```cfg
    [layout]
    rows = 3

    [image_folder]
    path = ./images

    [images]
    row0 = figure1.png, figure2.png
    row1 = results_chart.png
    row2 = diagram1.png, diagram2.png

    [output]
    filename = output/combined_figures.png
    background_color = 255,255,255
    ```

2.  After running the script, you'll find the `combined_figures.png` image in the `output` folder. You can then insert this image into your poster layout using your preferred presentation software.

## Contributing

Feel free to open issues or submit pull requests for bug fixes, new features, or improvements.

## Acknowledgments

The development of this repository was significantly aided by the assistance of Gemini Advanced, a large language model from Google AI.

## License

Please see the [LICENSE](LICENSE) file for details.
