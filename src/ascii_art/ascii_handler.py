import os
import cv2
import numpy as np
from ascii_art.color_manager import ColorManager, ColorPalettes
from skimage import exposure
from skimage.filters import threshold_local
from colorama import Fore, Back, Style

DENSITY_MAP_256 = ' _,.`;\':-~"|!\/<()L>+J^=c*[{}]zirj1?syulvCIZt7oTx2Yng3pSqaeU5fVwEFOQXGmd9hHbD6PAk4%WB8K&N$#R0M@'
DENSITY_MAP_16 = ' ,;"<[?IneEhABR@'
CHARACTER_ASPECT_RATIO = 0.4897959183673469

class AsciiHandler:
    def __init__(self, img, width, palette=ColorPalettes.xterm256, density_map=DENSITY_MAP_256):
        if width <= 0:
            raise ValueError("Width should be greater than 0.")
        self.img = img
        self.width = width
        self.density_map = density_map
        self.color_manager = ColorManager(palette)

    @staticmethod
    def equalize_luminosity(image_np):
        
        ycrcb = cv2.cvtColor(image_np, cv2.COLOR_RGB2YCrCb)
        ycrcb[..., 0] = cv2.equalizeHist(ycrcb[..., 0])
        return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2RGB)

    def perform_contrast_stretching(self, image_np):
        lab = cv2.cvtColor(image_np, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        return cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)

    def perform_gamma_correction(self, image_np, gamma=1.5):
        inv_gamma = 1.0 / gamma
        lut = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)], dtype="uint8")
        return cv2.LUT(image_np, lut)

    def preprocess_image(self, image_np, contrast_stretching=False, gamma_correction=False):
        if contrast_stretching:
            image_np = self.perform_contrast_stretching(image_np)
        if gamma_correction:
            image_np = self.perform_gamma_correction(image_np)
        return image_np

    def image_to_ascii(self, contrast_stretching=False, gamma_correction=False, invert=False):
        
        img_np = self.img.copy()
        img_np[:, :, :3] = self.equalize_luminosity(img_np[:, :, :3])

        img_np = self.preprocess_image(img_np, contrast_stretching=contrast_stretching, gamma_correction=gamma_correction)

        img_height, img_width, _ = img_np.shape
        num_columns = self.width

        # Calculate the number of rows considering the pixel aspect ratio
        num_rows = int(img_height * (num_columns / img_width) * CHARACTER_ASPECT_RATIO)

        column_step = img_width // num_columns
        row_step = img_height // num_rows

        ascii_map, color_map = self.generate_ascii_map_and_color_map(img_np, num_rows, num_columns, row_step, column_step, invert)

        return ascii_map, color_map
    
    def select_character(self, tile_np):
        try:
            alpha = np.mean(tile_np[:, :, 3])
        except IndexError:
            alpha = 255
        alphathreshold = 10  # Threshold below which alpha values are considered transparent
        if alpha < alphathreshold:  # Completely transparent
            return ' '

        tile_gray = cv2.cvtColor(tile_np[:, :, :3], cv2.COLOR_RGB2GRAY)
        block_size = 5
        adaptive_thresh = threshold_local(tile_gray, block_size, offset=10)
        binary_image = tile_gray > adaptive_thresh
        intensity = np.mean(binary_image)
        index = int(intensity * (len(self.density_map) - 1))
        return self.density_map[index]

    def generate_ascii_map_and_color_map(self, img_np, num_rows, num_columns, row_step, column_step, invert):
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

    def print_monochrome_ascii(self, ascii_map):
        
        for row in ascii_map:
            for char in row:
                print(char, end="")
            print()

    def print_colored_ascii(self, ascii_map, color_map):
        
        reset_color = Style.RESET_ALL
        for row, color_row in zip(ascii_map, color_map):
            for char, color in zip(row, color_row):
                if color is None:
                    print(reset_color + ' ', end="")
                else:
                    foreground_color = self.color_manager.xterm256_color_code(color)
                    print(foreground_color + char, end="")
            print(reset_color)  # Reset colors at the end of the row

    def print_ascii(self, ascii_map, color_map, monochrome=False):
        if monochrome:
            self.print_monochrome_ascii(ascii_map)
        else:
            self.print_colored_ascii(ascii_map, color_map)