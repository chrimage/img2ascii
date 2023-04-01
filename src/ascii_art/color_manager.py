import numpy as np
from scipy.spatial import KDTree

class ColorManager:
    def __init__(self):
        self.palette = self.xterm256_palette()
        self.palette_tree = KDTree(self.palette)

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

    def closest_color(self, tile_np, invert=False):
        """Finds the closest color in the color palette for a given tile."""
        if np.min(tile_np[:, :, 3]) < 128:  # Tile has transparency
            return None
        tile_color = np.mean(tile_np[:, :, :3], axis=(0, 1))
        if invert:
            tile_color = 255 - tile_color
        min_color_index = self.palette_tree.query(tile_color)[1]
        return self.palette[min_color_index]

    def xterm256_color_code(self, color):
        """Generates the xterm256 color code for a given color."""
        r, g, b = color
        if r == g and g == b:
            if r < 8:
                return "\033[38;5;16m"
            if r > 248:
                return "\033[38;5;231m"
            return f"\033[38;5;{232 + (r - 8) // 10}m"
        return f"\033[38;5;{16 + (r // 51) * 36 + (g // 51) * 6 + (b // 51)}m"