import sys
from colorama import init
import argparse
from image_handler import ImageHandler
from ascii_converter import AsciiConverter

def handle_arguments():
    parser = argparse.ArgumentParser(description="Convert an image to ASCII art.")
    parser.add_argument("-u", "--url", help="URL of the image to convert (optional)", default=None)
    parser.add_argument("--cats", action="store_true", help="Display a random cat image")
    parser.add_argument("--dogs", action="store_true", help="Display a random dog image")
    parser.add_argument("-w", "--width", type=int, default=100, help="Width of the ASCII art in characters")
    args = parser.parse_args()

    if args.cats and args.dogs:
        parser.error("You can only choose one option: --cats or --dogs")

    if args.url is None:
        if args.cats:
            # Use The Cat API for a random cat image
            args.url = "http://thecatapi.com/api/images/get?format=src&type=jpg"
        elif args.dogs:
            # Use Dog API for a random dog image
            args.url = "https://dog.ceo/api/breeds/image/random"
        else:
            # Use Lorem Picsum for a random image with a width of 800 pixels and a height of 600 pixels
            args.url = "https://picsum.photos/800/600"

    return args

def main():
    args = handle_arguments()
    init()
    
    try:
        img_handler = ImageHandler(args.url)
        img = img_handler.download_image()
        ascii_converter = AsciiConverter(img, args.width)
        ascii_map, color_map = ascii_converter.image_to_ascii()
        ascii_converter.print_colored_ascii(ascii_map, color_map)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
