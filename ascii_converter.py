import os
import cv2
import numpy as np
import html
from color_manager import ColorManager
from skimage import exposure

DENSITY_MAP_256 = ' _,.`;\':-~"|!\/<()L>+J^=c*[{}]zirj1?syulvCIZt7oTx2Yng3pSqaeU5fVwEFOQXGmd9hHbD6PAk4%WB8K&N$#R0M@'
DENSITY_MAP_16 = ' ,;"<[?IneEhABR@'
CHARACTER_ASPECT_RATIO = 0.4897959183673469


class AsciiConverter:
    def __init__(self, img, width, density_map=DENSITY_MAP_16):
        self.img = img
        self.width = width
        self.density_map = density_map
        self.color_manager = ColorManager()

    @staticmethod
    def equalize_luminosity(image_np):
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

    def image_to_ascii(self, canny=False, feature_extraction=False, invert=False):
        """Converts the input image to ASCII art."""
        img_color = self.img.convert("RGBA")
        img_np = np.array(img_color)
        img_np[:, :, :3] = self.equalize_luminosity(img_np[:, :, :3])

        img_width, img_height = img_color.size
        num_columns = self.width

        # Calculate the number of rows considering the pixel aspect ratio
        num_rows = int(img_height * (num_columns / img_width) * CHARACTER_ASPECT_RATIO)

        column_step = img_width // num_columns
        row_step = img_height // num_rows

        if canny:
            img_np = self.canny_edge_detection(img_np)

        if feature_extraction:
            img_np = self.apply_feature_extraction(img_np)

        ascii_map, color_map = self.generate_ascii_map_and_color_map(img_np, num_rows, num_columns, row_step, column_step, invert)

        return ascii_map, color_map

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