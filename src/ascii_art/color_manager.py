import numpy as np
from scipy.spatial import KDTree
from enum import Enum


class ColorPalettes(Enum):
    xterm256 = "xterm256"
    ansi = "ansi"
    truecolor = "truecolor"


class ColorManager:
    def __init__(self, palette: ColorPalettes = ColorPalettes.xterm256):
        self.palette = self.get_palette_for(palette)
        self.palette_tree = KDTree(self.palette)

    def get_palette_for(self, palette: ColorPalettes):
        if palette == ColorPalettes.xterm256:
            return self.xterm256_palette()
        elif palette == ColorPalettes.ansi:
            return self.ansi_palette()
        elif palette == ColorPalettes.truecolor:
            return self.truecolor_palette()
        else:
            raise ValueError(f"Invalid color palette: {palette}")

    def basic_colors(self):
        return [
            (0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0),
            (0, 0, 128), (128, 0, 128), (0, 128, 128), (192, 192, 192)
        ]

    def rgb_colors(self):
        return [(r, g, b) for r in (0, 95, 135, 175, 215, 255) for g in (0, 95, 135, 175, 215, 255) for b in (0, 95, 135, 175, 215, 255)]

    def grayscale_colors(self):
        return [(i, i, i) for i in range(8, 248, 10)]

    def xterm256_palette(self):
        return self.basic_colors() + self.rgb_colors() + self.grayscale_colors()

    def ansi_palette(self):
        return [
            (0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0),
            (0, 0, 128), (128, 0, 128), (0, 128, 128), (192, 192, 192),
            (128, 128, 128), (255, 0, 0), (0, 255, 0), (255, 255, 0),
            (0, 0, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255)
        ]

    def truecolor_palette(self):
        return [(r, g, b) for r in range(256) for g in range(256) for b in range(256)]

    def closest_color(self, tile_color, invert=False):
        if invert:
            tile_color = 255 - tile_color

        min_color_index = self.palette_tree.query(tile_color[:3])[1]
        return self.palette[min_color_index]

    def xterm256_color(self, text, color_code):
        return f"\x1b[38;5;{color_code}m{text}\x1b[0m"

    def xterm256_color_code(self, r, g, b):
        r = int(round(r / 255 * 5))
        g = int(round(g / 255 * 5))
        b = int(round(b / 255 * 5))
        return 16 + 36 * r + 6 * g + b

