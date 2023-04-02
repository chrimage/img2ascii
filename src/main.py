import sys
from colorama import init
from ascii_art import get_cli_arguments, ImageHandler, AsciiHandler, ColorPalettes

def generate_default_url(args):
    if args.cats:
        return "http://thecatapi.com/api/images/get?format=src&type=jpg"
    elif args.dogs:
        return "https://dog.ceo/api/breeds/image/random"
    else:
        return "https://picsum.photos/800/600"

def main():
    args = get_cli_arguments()
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
        elif args.clipboard:
            img_handler = ImageHandler("clipboard", None)
        else:
            img_url = generate_default_url(args)
            img_handler = ImageHandler("url", img_url)

        img = img_handler.load_image()

        ascii_handler = AsciiHandler(img, args.width, palette=ColorPalettes(args.palette), density_map=args.density_map)
        ascii_map, color_map = ascii_handler.image_to_ascii(
            adaptive_hist_eq=True,
            invert=args.invert
        )

        if args.output:
            ascii_handler.save_monochrome_ascii(ascii_map, args.output)
        elif args.html:
            ascii_handler.save_colored_ascii_html(ascii_map, color_map, args.html)
        else:
            ascii_handler.print_ascii(ascii_map, color_map, monochrome=args.mono)

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()