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
        self.source_methods = {
            'url': self.download_image,
            'file': self.load_local_image,
            'webcam': self.capture_webcam,
            'clipboard': self.load_image_from_clipboard
        }

    def load_image(self):
        """
        Load image based on the specified source type and value.
        Raises:
            ValueError: If the source type is invalid.
            Exception: If there is an error loading the image.
        Returns:
            PIL.Image.Image: Loaded image.
        """
        if self.source_type not in self.source_methods:
            raise ValueError("Invalid source type")

        return self.source_methods[self.source_type]()

    def download_image(self):
        url = self.source_value
        response = requests.get(url)
        response.raise_for_status()

        try:
            return Image.open(BytesIO(response.content))
        except Exception as e:
            raise Exception(f"Error loading image from URL: {e}")

    def load_local_image(self):
        try:
            return Image.open(self.source_value)
        except Exception as e:
            raise Exception(f"Error loading image from file: {e}")

    def load_image_from_clipboard(self):
        if platform.system() == "Linux":
            return self.load_image_from_clipboard_linux()
        else:
            return self.load_image_from_clipboard_generic()

    def load_image_from_clipboard_linux(self):
        try:
            from PIL import ImageGrab
        except ImportError:
            raise ImportError("ImageGrab module not found. To use clipboard functionality on Linux, you need to install 'xclip' and 'pillow' packages.")

        return self.load_image_from_clipboard_generic()

    def load_image_from_clipboard_generic(self):
        try:
            img = ImageGrab.grabclipboard()
            if img is None:
                raise ValueError("No image found in the clipboard.")
            return img
        except Exception as e:
            raise Exception(f"Error loading image from clipboard: {e}")

    def capture_webcam(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if ret:
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            return img
        else:
            raise Exception("Could not capture image from the webcam")