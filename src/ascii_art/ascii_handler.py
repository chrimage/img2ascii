import cv2
import numpy as np
from ascii_art.color_manager import ColorManager, ColorPalettes
from skimage import exposure
from skimage.filters import threshold_local
from colorama import Fore, Back, Style
import itertools

DENSITY_MAP_256 = ' _,.`;\':-~"|!\/<()L>+J^=c*[{}]zirj1?syulvCIZt7oTx2Yng3pSqaeU5fVwEFOQXGmd9hHbD6PAk4%WB8K&N$#R0M@'
DENSITY_MAP_16 = ' .,:"<+[?e=E*%#@'
CHARACTER_ASPECT_RATIO = 0.4897959183673469


class AsciiHandler:
    def __init__(self, img, width, palette=ColorPalettes.xterm256, density_map=DENSITY_MAP_16):
        if width <= 0:
            raise ValueError("Width should be greater than 0.")
        self.img = img
        self.width = width
        self.density_map = density_map
        self.color_manager = ColorManager(palette)

    def adaptive_histogram_equalization(self, image_np):
        lab = cv2.cvtColor(image_np, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        return cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)

    def preprocess_image(self, image_np, adaptive_hist_eq=False):
        if adaptive_hist_eq:
            image_np = self.adaptive_histogram_equalization(image_np)
        return image_np

    def image_to_ascii(self, adaptive_hist_eq=False, invert=False):
        img_np = self.img.copy()

        img_np = self.preprocess_image(
            img_np, adaptive_hist_eq=adaptive_hist_eq)

        img_height, img_width, _ = img_np.shape
        num_columns = self.width

        # Calculate the number of rows considering the pixel aspect ratio
        num_rows = int(img_height * (num_columns / img_width)
                       * CHARACTER_ASPECT_RATIO)

        column_step = img_width // num_columns
        row_step = img_height // num_rows

        ascii_map, color_map = self.generate_ascii_and_color_maps(
            img_np, num_rows, num_columns, row_step, column_step, invert)

        return ascii_map, color_map

    def select_character(self, tile_np):
        alpha = 1 if tile_np.shape[2] < 4 else np.mean(tile_np[:, :, 3]) / 255
        alphathreshold = 10 / 255

        if alpha < alphathreshold:  # Completely transparent
            return ' '

        mean_color = np.mean(tile_np[:, :, :3], axis=(0, 1))
        # Apply weighted sum to convert the average color to grayscale
        intensity = np.dot(mean_color, [0.2989, 0.5870, 0.1140]) / 255

        index = int(intensity * (len(self.density_map) - 1))
        return self.density_map[index]


    def generate_ascii_and_color_maps(self, img_np, num_rows, num_columns, row_step, column_step, invert):
        # Resize the input image to have dimensions (num_rows * row_step, num_columns * column_step, 3)
        img_np_resized = cv2.resize(img_np, (num_columns * column_step, num_rows * row_step))
        
        # Reshape the resized image to have dimensions (num_rows, num_columns, row_step, column_step, 3)
        img_np_reshaped = img_np_resized.reshape(num_rows, row_step, num_columns, column_step, -1)
        
        # Calculate the means per tile and reshape the color_map_as_array to dimensions (num_rows, num_columns, 3)
        color_map_as_array = np.mean(img_np_reshaped, axis=(1, 3))
        
        if invert:
            color_map_as_array = 255 - color_map_as_array

        # Create color_map by iterating through color_map_as_array and applying the closest_color function
        color_map = []
        for row in color_map_as_array:
            color_row = []
            for color in row:
                color_row.append(self.color_manager.closest_color(color[:3], invert))
            color_map.append(color_row)
        color_map = np.array(color_map)

        # Calculate the grayscale intensities for each tile
        intensities = np.dot(color_map_as_array[:, :, :3], [0.2989, 0.5870, 0.1140]) / 255
    
        indices = (intensities * (len(self.density_map) - 1)).astype(int)
        
        index_pairs = list(itertools.product(range(num_rows), range(num_columns)))

        # Create the ASCII map using the grayscale intensities
        ascii_map = [[self.density_map[indices[i, j]] for j in range(num_columns)] for i in range(num_rows)]
        
        return ascii_map, color_map


    def print_monochrome_ascii(self, ascii_map):
        for row in ascii_map:
            print(''.join(row))

    def print_colored_ascii(self, ascii_map, color_map):
        for i, row in enumerate(ascii_map):
            for j, char in enumerate(row):
                color_code = self.color_manager.xterm256_color_code(*color_map[i][j])
                print(self.color_manager.xterm256_color(char, color_code), end="")
            print()

    def print_ascii(self, ascii_map, color_map, monochrome=False):
        if monochrome:
            self.print_monochrome_ascii(ascii_map)
        else:
            self.print_colored_ascii(ascii_map, color_map)
