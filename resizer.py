import cv2
from PIL import Image

class ImageResizer:
    def __init__(self):
        self.sizes = [
            (1080, 1080),  # Size 1
            (2000, 365),   # Size 2
            (600, 348)     # Size 3
        ]
        self.ppi = 300  # Desired PPI

    # Function to resize image while maintaining quality
    def resize_image(self, image_path):
        # Read the image using OpenCV
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

        if image is None:
            raise ValueError(f"Could not load image from {image_path}")

        # Convert BGR (OpenCV) to RGB (Pillow compatible)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # List to store resized images
        resized_images = []

        # Resize the image for each size
        for size in self.sizes:
            resized = cv2.resize(image_rgb, size, interpolation=cv2.INTER_LANCZOS4)
            resized_images.append(self.convert_to_pil_and_set_ppi(resized, size))

        return resized_images

    # Function to convert OpenCV image to PIL and set the PPI
    def convert_to_pil_and_set_ppi(self, cv_image, size):
        # Convert OpenCV image (NumPy array) to PIL image
        pil_image = Image.fromarray(cv_image)
        
        # Set PPI (Resolution in DPI)
        pil_image.info['dpi'] = (self.ppi, self.ppi)

        # Ensure RGB color mode
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')

        return pil_image

    # Function to save the resized images to disk
    def save_images(self, resized_images, output_paths):
        for i, img in enumerate(resized_images):
            img.save(output_paths[i], dpi=(self.ppi, self.ppi), quality=100)