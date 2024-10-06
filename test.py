from resizer import ImageResizer

# Initialize the resizer
resizer = ImageResizer()

# Path to the original image
image_path = 'test.png'

# Resize the image
resized_images = resizer.resize_image(image_path)

# Paths to save resized images
output_paths = ['resized_1080x1080.png', 'resized_2000x365.png', 'resized_600x348.png']

# Save resized images to disk
resizer.save_images(resized_images, output_paths)