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
        # Add your ANSI palette implementation here
        pass

    def truecolor_palette(self):
        # Add your Truecolor palette implementation here
        pass

    def closest_color(self, tile_np, invert=False):
        
        if np.min(tile_np[:, :, 3]) < 128:  # Tile has transparency
            return None
        tile_color = np.mean(tile_np[:, :, :3], axis=(0, 1))
        if invert:
            tile_color = 255 - tile_color
        min_color_index = self.palette_tree.query(tile_color)[1]
        return self.palette[min_color_index]

    def xterm256_color_code(self, color):
        
        r, g, b = color
        if r == g and g == b:
            if r < 8:
                return "\033[38;5;16m"
            if r > 248:
                return "\033[38;5;231m"
            return f"\033[38;5;{232 + (r - 8) // 10}m"
        return f"\033[38;5;{16 + (r // 51) * 36 + (g // 51) * 6 + (b // 51)}m"