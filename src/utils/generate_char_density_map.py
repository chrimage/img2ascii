import sys
import argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from sklearn.cluster import KMeans
import fontconfig

ASCII_CHARS = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
FULL_BLOCK_CHAR = "█"

def get_full_block_char_dimensions(font_path, base_font_size=40):
    """
    Calculate the dimensions of a full block character.

    :param font_path: str, path to the font file
    :param base_font_size: int, optional font size (default: 40)
    :return: tuple of width and height dimensions
    """
    font = ImageFont.truetype(font_path, base_font_size)
    return font.getmask(FULL_BLOCK_CHAR).size

def render_single_char_image(char, font_path, block_dimensions):
    """
    Render an image of a single character using the provided font.

    :param char: str, character to render
    :param font_path: str, path to the font file
    :param block_dimensions: tuple, dimensions of the character block
    :return: PIL.Image.Image
    """
    w, h = block_dimensions
    img = Image.new('L', (w, h), color=0)  # Black background
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, h)
    draw.text((0, 0), char, font=font, fill=255)  # White text
    return img

def calculate_pixel_density(img):
    """
    Calculate the average pixel density of an image.

    :param img: PIL.Image.Image, input image
    :return: float, average pixel density
    """
    return np.mean(np.asarray(img))

def create_font_char_density_map(font_path, chars=ASCII_CHARS):
    """
    Create a character density map for the provided font and characters.

    :param font_path: str, path to the font file
    :param chars: str, optional string of characters to include in the density map (default: ASCII_CHARS)
    :return: tuple of the density map (list of char-density tuples) and block dimensions (tuple)
    """
    block_dimensions = get_full_block_char_dimensions(font_path)
    densities = [(char, calculate_pixel_density(render_single_char_image(char, font_path, block_dimensions))) for char in chars]
    densities.sort(key=lambda x: x[1])
    return densities, block_dimensions

def select_gradient_chars_kmeans(density_map, num_chars=16):
    min_density_char, max_density_char = density_map[0], density_map[-1]
    remaining_densities = density_map[1:-1]
    densities = np.array([density for _, density in remaining_densities]).reshape(-1, 1)
    kmeans = KMeans(n_clusters=num_chars - 2, random_state=0)
    kmeans.fit(densities)
    ideal_chars = [min_density_char[0]]  # Add the darkest character
    # Sort cluster centers and labels
    sorted_indices = np.argsort(kmeans.cluster_centers_, axis=0).flatten()
    cluster_centers_sorted = kmeans.cluster_centers_[sorted_indices]
    cluster_labels_sorted = np.argsort(sorted_indices)
    for i, centroid in enumerate(cluster_centers_sorted):
        # Find the closest character in density to the cluster center
        ideal_char = min(
            [(idx, x) for idx, x in enumerate(remaining_densities) if cluster_labels_sorted[kmeans.labels_[idx]] == i],
            key=lambda ix: abs(ix[1][1] - centroid[0])
        )[1][0]
        ideal_chars.append(ideal_char)
    ideal_chars.append(max_density_char[0])  # Add the lightest character
    return ideal_chars

def find_font_by_name(name_pattern):
    """
    Find a font file by a name pattern.
    :param name_pattern: str, pattern to match the desired font
    :return: str, path to the font file or None if not found
    """
    fonts = fontconfig.query(family=name_pattern, lang='en')
    if fonts:
        return fonts[0].file
    else:
        return None

def main():
    parser = argparse.ArgumentParser(description='Generate a character density map using K-Means clustering.')
    parser.add_argument('--font', type=str, default='NotoSansMono', help='Font name (default: NotoSansMono)')
    parser.add_argument('--num_chars', type=int, default=16, help='Number of gradient characters (default: 16)')
    args = parser.parse_args()

    noto_sans_mono_font_path = find_font_by_name(args.font)

    if not(notfound:= noto_sans_mono_font_path is None):
        density_map, block_dimensions = create_font_char_density_map(noto_sans_mono_font_path)
    else:
        print(f'Font not found: {args.font}')
        sys.exit(1)

    full_density_chars = ''.join([char for char, _ in density_map])
    gradient_chars = select_gradient_chars_kmeans(density_map, args.num_chars)
    aspect_ratio = block_dimensions[0] / block_dimensions[1]
    print(f"DENSITY_MAP_256 = '{full_density_chars}'")
    print(f"DENSITY_MAP_{args.num_chars} = '{''.join(gradient_chars)}'")
    print(f"CHARACTER_ASPECT_RATIO = '{aspect_ratio}'")

    # Print the K clusters
    num_chars = args.num_chars
    min_density_char, max_density_char = density_map[0], density_map[-1]
    remaining_densities = density_map[1:-1]
    densities = np.array([density for _, density in remaining_densities]).reshape(-1, 1)
    kmeans = KMeans(n_clusters=num_chars - 2, random_state=0)
    kmeans.fit(densities)
    cluster_labels = kmeans.labels_
    print("\nK clusters:")
    for i in range(num_chars - 2):
        cluster_chars = [char for (char, _), label in zip(remaining_densities, cluster_labels) if label == i]
        print(f"Cluster {i + 1}: {', '.join(cluster_chars)}")

if __name__ == '__main__':
    main()