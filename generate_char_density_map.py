import numpy as np
from PIL import Image, ImageDraw, ImageFont
from sklearn.cluster import KMeans

ASCII_CHARS = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
FULL_BLOCK_CHAR = "█"

def get_full_block_char_dimensions(font_path, base_font_size=40):
    font = ImageFont.truetype(font_path, base_font_size)
    return font.getmask(FULL_BLOCK_CHAR).size

def render_single_char_image(char, font_path, block_dimensions):
    w, h = block_dimensions
    img = Image.new('L', (w, h), color=0)  # Black background
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, h)
    draw.text((0, 0), char, font=font, fill=255)  # White text
    return img

def calculate_pixel_density(img):
    return np.mean(np.array(img))

def create_font_char_density_map(font_path, chars=ASCII_CHARS):
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
    ideal_chars += [min(remaining_densities, key=lambda x: abs(x[1] - centroid[0]))[0] for centroid in sorted(kmeans.cluster_centers_, key=lambda x: x[0])]
    ideal_chars.append(max_density_char[0]) # Add the lightest character
    
    return ideal_chars

def main():
    noto_sans_mono_font_path = "/usr/share/fonts/google-noto/NotoSansMono-Regular.ttf"
    density_map, block_dimensions = create_font_char_density_map(noto_sans_mono_font_path)
    
    full_density_chars = ''.join([char for char, _ in density_map])
    gradient_chars = select_gradient_chars_kmeans(density_map)
    
    aspect_ratio = block_dimensions[0] / block_dimensions[1]
    
    print(f"DENSITY_MAP_256 = '{full_density_chars}'")
    print(f"DENSITY_MAP_16 = '{''.join(gradient_chars)}'")
    print(f"CHARACTER_ASPECT_RATIO = '{aspect_ratio}'")

if __name__ == '__main__':
    main()