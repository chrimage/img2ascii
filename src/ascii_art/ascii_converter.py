import os
import cv2
import numpy as np
import html
from color_manager import ColorManager
from skimage import exposure
from colorama import Fore, Back, Style

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
    
    @staticmethod
    def canny_edge_detection(img_np, low_threshold=50, high_threshold=200):
        """Applies Canny edge detection to the input image."""
        img_gray = cv2.cvtColor(img_np, cv2.COLOR_RGBA2GRAY)
        edges = cv2.Canny(img_gray, low_threshold, high_threshold)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2RGBA)

    def apply_feature_extraction(self, img_np, num_keypoints=500):
        """Applies feature extraction using SIFT keypoint detector on the input image."""
        sift = cv2.SIFT_create(nfeatures=num_keypoints)
        keypoints, _ = sift.detectAndCompute(cv2.cvtColor(img_np, cv2.COLOR_RGBA2GRAY), None)

        # Create a black image of the same size as the input image
        feature_img = np.zeros_like(img_np)

        # Draw the keypoints on the black image
        feature_img = cv2.drawKeypoints(feature_img, keypoints, None, color=(255, 255, 255), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        return feature_img

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
    
    def canny_edge_detection(self, img_np, low_threshold=50, high_threshold=200):
        """Applies Canny edge detection to the input image."""
        img_gray = cv2.cvtColor(img_np, cv2.COLOR_RGBA2GRAY)
        edges = cv2.Canny(img_gray, low_threshold, high_threshold)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2RGBA)
    
    def apply_feature_extraction(self, img_np, num_keypoints=500):
        """Applies feature extraction using ORB keypoint detector on the input image."""
        orb = cv2.ORB_create(nfeatures=num_keypoints)
        keypoints = orb.detect(cv2.cvtColor(img_np, cv2.COLOR_RGBA2GRAY), None)
        keypoints, _ = orb.compute(img_np, keypoints)

        # Create a black image of the same size as the input image
        feature_img = np.zeros_like(img_np)

        # Draw the keypoints on the black image
        feature_img = cv2.drawKeypoints(feature_img, keypoints, None, color=(255, 255, 255), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        return feature_img

    def print_monochrome_ascii(self, ascii_map):
        """Prints the ASCII art in monochrome (grayscale) without colors."""
        for row in ascii_map:
            for char in row:
                print(char, end="")
            print()
            
    def print_colored_ascii(self, ascii_map, color_map):
        """Prints the ASCII art with color."""

        reset_color = Style.RESET_ALL

        for row, color_row in zip(ascii_map, color_map):
            for char, color in zip(row, color_row):
                if color is None:
                    print(reset_color + ' ', end="")
                else:
                    background_color = Back.RGB(color[0], color[1], color[2])
                    print(background_color + char, end="")
            print(reset_color)  # Reset colors at the end of the row

