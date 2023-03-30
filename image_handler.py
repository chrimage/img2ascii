import cv2
import requests
from io import BytesIO
from PIL import Image, ImageGrab
import clipboard
import platform

class ImageHandler:

    def __init__(self, source_type, source_value):
        self.source_type = source_type.lower()
        self.source_value = source_value

    def load_image(self):
        if self.source_type == 'url':
            return self.download_image(self.source_value)
        elif self.source_type == 'file':
            return self.load_local_image(self.source_value)
        elif self.source_type == 'webcam':
            return self.capture_webcam()
        elif self.source_type == 'clipboard':
            return self.load_image_from_clipboard()
        else:
            raise ValueError("Invalid source type")

    def download_image(self, url):
        if "dog.ceo" in url:  # Dog API returns JSON
            response = requests.get(url)
            response.raise_for_status()
            url = response.json()["message"]
        response = requests.get(url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))

    def load_local_image(self, path):
        return Image.open(path)

    def load_image_from_clipboard(self):
        if platform.system() == "Linux":
            try:
                from PIL import ImageGrab
            except ImportError:
                raise ImportError("ImageGrab module not found. To use clipboard functionality on Linux, you need to install 'xclip' and 'pillow' packages.")
        try:
            return ImageGrab.grabclipboard()
        except Exception as e:
            raise Exception("Error loading image from clipboard: " + str(e))

    def capture_webcam(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if ret:
            return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        else:
            raise Exception("Could not capture image from the webcam")