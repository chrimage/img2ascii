import sys
import cv2
import requests
import numpy as np
from io import BytesIO
from PIL import Image, ImageGrab
from skimage import io

class ImageHandler:
    def __init__(self, source_type, source):
        self.source_type = source_type
        self.source = source

    def load_image(self):
        if self.source_type == "url":
            return self.load_image_from_url(self.source)
        elif self.source_type == "file":
            return self.load_image_from_file(self.source)
        elif self.source_type == "webcam":
            return self.load_image_from_webcam()
        elif self.source_type == "clipboard":
            return self.load_image_from_clipboard()
        else:
            raise ValueError("Invalid source type")

    def load_image_from_url(self, url):
        response = requests.get(url)
        img = io.imread(BytesIO(response.content))
        return img

    def load_image_from_file(self, file_path):
        img = io.imread(file_path)
        return img
    
    def load_image_from_webcam(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        cv2.destroyAllWindows()
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img_np = np.array(img)
        return img_np

    def load_image_from_clipboard(self):
        if sys.platform not in ["win32", "darwin"]:
            raise OSError("ImageGrab.grabclipboard() is macOS and Windows only")
        image = ImageGrab.grabclipboard()
        if image is None:
            raise ValueError("No image data found in clipboard")
        return image