# Img2Ascii

Img2Ascii is a Python application that converts images to ASCII art. The
application accepts images from various sources, including local files, URLs,
webcams, and clipboard, and generates colored ASCII representations that can be
viewed in the terminal or saved as an HTML file.

## Requirements

- Python 3.6+
- Pillow library
- Colorama library
- NumPy library
- OpenCV library (required for webcam support)
- scikit-image library
- clipboard library

## Installation

1. Clone the repository or download the source code.
2. Install the required packages with the following command:

```
pip install -r requirements.txt
```

## Usage

To run the application, navigate to the project directory and execute the
following command:

```
python src/main.py
```

By default, the application will generate ASCII art for a random image with 100
characters width. You can customize the output with various command-line
options:

- `-u` or `--url`: Specify a URL of the image to convert (optional)
- `-f` or `--file`: Specify a path to the image file to convert (optional)
- `--webcam`: Take a photo using the webcam to convert into ASCII art
- `--clipboard`: Load an image from the clipboard to convert into ASCII art
- `--mono`: Print the ASCII art in monochrome (grayscale) without colors
- `--cats`: Display a random cat image
- `--dogs`: Display a random dog image
- `--invert`: Invert colors of the ASCII art
- `-w` or `--width`: Specify the width of the ASCII art in characters
  (default: 100)

For saving the ASCII art output to a file, use the following options:

- `-o` or `--output`: Output monochrome ASCII art to a text file (e.g.,
  `-o output.txt`)
- `--html`: Output colored ASCII art to an HTML file (e.g.,
  `--html output.html`)

For a complete list of options and their descriptions, use
`python src/main.py -h` to display the command-line argument help.

## Examples

Convert an image from a URL:

```
python src/main.py -u "https://example.com/image.jpg"
```

Convert an image file from the local filesystem:

```
python src/main.py -f "path/to/image.jpg"
```

Take a photo with the webcam and convert it to ASCII art:

```
python src/main.py --webcam
```

Load an image from the clipboard and convert it to ASCII art:

```
python src/main.py --clipboard
```

Display a random cat image in inverted monochrome ASCII art with a width of 150
characters:

```
python src/main.py --cats --mono --invert -w 150
```

Save colored ASCII art as an HTML file with a dark background, centered and
automatically resized based on the browser window size:

```
python src/main.py --html output.html
```
