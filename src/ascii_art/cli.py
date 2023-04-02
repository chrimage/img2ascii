import argparse
from ascii_art.ascii_handler import DENSITY_MAP_16, DENSITY_MAP_256
from ascii_art.color_manager import ColorPalettes

def get_cli_arguments():
    parser = argparse.ArgumentParser(description="Convert images to ASCII art.")
    
    # Image source
    source_group = parser.add_mutually_exclusive_group()
    source_group.add_argument("-u", "--url", help="URL of the image to convert")
    source_group.add_argument("-f", "--file", help="Path to the image file to convert")
    source_group.add_argument("--webcam", action="store_true", help="Capture an image using the webcam")
    source_group.add_argument("--clipboard", action="store_true", help="Load image from the clipboard")
    
    # Preprocessing
    preprocess_group = parser.add_argument_group("preprocessing")
    preprocess_group.add_argument("--contrast-stretching", action="store_true", help="Perform contrast stretching on the image")
    preprocess_group.add_argument("--gamma-correction", action="store_true", help="Perform gamma correction on the image")
    
    # Output style
    style_group = parser.add_argument_group("style")
    style_group.add_argument("--mono", action="store_true", help="Print the ASCII art in monochrome (grayscale)")
    style_group.add_argument("--palette", choices=list(ColorPalettes), default=ColorPalettes.xterm256, help="Choose a color palette for the ASCII art")
    style_group.add_argument("--density-map", default=DENSITY_MAP_16, help="Specify a custom density map for the ASCII art")
    style_group.add_argument("--invert", action="store_true", help="Invert colors of the ASCII art")
    style_group.add_argument("-w", "--width", type=int, default=100, help="Width of the ASCII art in characters (default: 100)")
    
    # Fun examples
    fun_group = parser.add_argument_group("fun")
    fun_group.add_argument("--cats", action="store_true", help="Display a random cat image")
    fun_group.add_argument("--dogs", action="store_true", help="Display a random dog image")
    
    # Saving output
    output_group = parser.add_argument_group("output")
    output_group.add_argument("-o", "--output", help="Output monochrome ASCII art to a text file")
    output_group.add_argument("--html", help="Output colored ASCII art to an HTML file")
    
    return parser.parse_args()