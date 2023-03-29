import requests
from io import BytesIO
from PIL import Image

class ImageHandler:
    def __init__(self, url):
        self.url = url

    def download_image(self):
        """Downloads an image from a URL and returns it as a PIL.Image instance."""
        if "dog.ceo" in self.url:  # Dog API returns JSON
            response = requests.get(self.url).json()
            self.url = response["message"]
        return Image.open(BytesIO(requests.get(self.url).content))