import sys
from colorama import init
import argparse
from ascii_art.image_handler import ImageHandler
from ascii_art.ascii_converter import AsciiConverter

def generate_default_url(args):
    if args.cats:
        return "http://thecatapi.com/api/images/get?format=src&type=jpg"
    elif args.dogs:
        return "https://dog.ceo/api/breeds/image/random"
    else:
        return "https://picsum.photos/800/600"

def handle_arguments():
    parser = argparse.ArgumentParser(description="Convert an image to ASCII art.")
    parser.add_argument("-u", "--url", help="URL of the image to convert (optional)", default=None, type=str)
    parser.add_argument("-f", "--file", help="Path to the image file to convert (optional)", default=None, type=str)
    parser.add_argument("--webcam", action="store_true", help="Take a photo using the webcam")
    parser.add_argument("--clipboard", action="store_true", help="Load an image from the clipboard")
    parser.add_argument("--canny", action="store_true", help="Use Canny edge detection for preprocessing (outputs in monochrome)")
    parser.add_argument("--feature-extraction", action="store_true", help="Use feature extraction for preprocessing (outputs in monochrome)")
    parser.add_argument("--mono", action="store_true", help="Print the ASCII art in monochrome (grayscale) without colors")
    parser.add_argument("--cats", action="store_true", help="Display a random cat image")
    parser.add_argument("--dogs", action="store_true", help="Display a random dog image")
    parser.add_argument("--invert", action="store_true", help="Invert colors of the ASCII art")
    parser.add_argument("-w", "--width", type=int, default=100, help="Width of the ASCII art in characters")
    parser.add_argument("-o", "--output", help="Output monochrome ASCII art to a text file", default=None, type=str)
    parser.add_argument("--html", help="Output colored ASCII art to an HTML file", default=None, type=str)

    args = parser.parse_args()

    if args.url is None and args.file is None and not args.webcam and not args.clipboard:
        args.url = generate_default_url(args)

    return args

def main():
    args = handle_arguments()
    if args.width <= 0:
        print("Width should be greater than 0.")
        sys.exit(1)
    init()

    try:
        if args.url:
            img_handler = ImageHandler("url", args.url)
        elif args.file:
            img_handler = ImageHandler("file", args.file)
        elif args.webcam:
            img_handler = ImageHandler("webcam", None)
        else:
            img_handler = ImageHandler("clipboard", None)

        img = img_handler.load_image()

        ascii_converter = AsciiConverter(img, args.width)
        ascii_map, color_map = ascii_converter.image_to_ascii(args.canny, args.feature_extraction, args.invert)
        if args.output:
            ascii_converter.save_monochrome_ascii(ascii_map, args.output)
        elif args.html:
            ascii_converter.save_colored_ascii_html(ascii_map, color_map, args.html)
        else:
            if args.mono or args.canny:
                ascii_converter.print_monochrome_ascii(ascii_map)
            else:
                ascii_converter.print_colored_ascii(ascii_map, color_map)

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()