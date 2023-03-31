import os
import cv2
import numpy as np
from color_manager import ColorManager
from skimage import exposure

CHARACTER_ASPECT_RATIO = 2.2  # Assuming 1:2.2 aspect ratio for the font
CHARS_BY_DENSITY = ' ,-._:;`\'=~"cs<>uv\/zJLx!+a)|r(oie1wn}[]{^y*tCl?IZj27mT3gYpqS5XGV4fEFUk6AbOhd&KD98$HPQRB%W0N#@M'

class AsciiConverter:
    def __init__(self, img, width):
        self.img = img
        self.width = width
        self.density_map = CHARS_BY_DENSITY
        self.color_manager = ColorManager()

    def equalize_luminosity(self, image_np):
        """Equalize the luminosity of the image using histogram equalization."""
        ycrcb = cv2.cvtColor(image_np, cv2.COLOR_RGB2YCrCb)
        ycrcb[..., 0] = cv2.equalizeHist(ycrcb[..., 0])
        return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2RGB)
    
    def select_character(self, tile_np):
        """Selects an ASCII character that represents the intensity of a tile."""
        alpha = np.mean(tile_np[:, :, 3])
        alphathreshold = 10  # Threshold below which alpha values are considered transparent

        if alpha < alphathreshold:  # Completely transparent
            return ' '

        tile_yuv = np.dot(tile_np[:, :, :3], [0.299, 0.587, 0.114])
        intensity = np.mean(tile_yuv) / 255.0 * (alpha / 255.0)

        index = int(intensity * (len(self.density_map) - 1))
        return self.density_map[index]
        # Implement additional preprocessing functions here:
    # ...

    def print_monochrome_ascii(self, ascii_map):
        """Prints the ASCII art in monochrome (grayscale) without colors."""
        for row in ascii_map:
            for char in row:
                print(char, end="")
            print()

    def image_to_ascii(self, canny=False, feature_extraction=False, invert=False):
        """Converts the input image to ASCII art."""
        img_color = self.img.convert("RGBA")
        img_np = np.array(img_color)
        img_np[:, :, :3] = self.equalize_luminosity(img_np[:, :, :3])

        # Apply additional preprocessing techniques, if required
        # ...

        img_width, img_height = img_color.size
        num_columns = self.width
        num_rows = int(img_height * (self.width / img_width) / CHARACTER_ASPECT_RATIO)

        column_step = img_width // num_columns
        row_step = img_height // num_rows

        ascii_map = []
        color_map = []

        for y in range(num_rows):
            row_ascii = []
            row_color = []
            for x in range(num_columns):
                tile_x = x * column_step
                tile_y = y * row_step
                tile_np = img_np[tile_y:tile_y + row_step, tile_x:tile_x + column_step]

                row_ascii.append(self.select_character(tile_np))
                row_color.append(self.color_manager.closest_color(tile_np, invert=invert))

            ascii_map.append(row_ascii)
            color_map.append(row_color)

        return ascii_map, color_map

    def print_colored_ascii(self, ascii_map, color_map):
        """Prints the ASCII art with color."""
        for row, color_row in zip(ascii_map, color_map):
            for char, color in zip(row, color_row):
                if color is None:
                    print("\033[0m ", end="")
                else:
                    print(self.color_manager.xterm256_color_code(color) + char, end="")
            print("\033[0m")  # Reset colors at the end of the row
    
    def save_monochrome_ascii(self, ascii_map, output_path):
        with open(output_path, "w") as file:
            for row in ascii_map:
                for char in row:
                    file.write(char)
                file.write(os.linesep)

    def save_colored_ascii_html(self, ascii_map, color_map, output_path):
        with open(output_path, "w") as file:
            file.write('<html><head><style>pre {font-family: Courier; font-size: 10pt;}</style></head><body><pre>')
            for row, color_row in zip(ascii_map, color_map):
                for char, color in zip(row, color_row):
                    if color is None:
                        file.write(" ")
                    else:
                        file.write(f'<span style="background-color: rgb{color};">{char}</span>')
                file.write(os.linesep)
            file.write('</pre></body></html>')