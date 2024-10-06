from model import ImageResizerDB

# Initialize the database object
db = ImageResizerDB()

# Insert a new image record
with open('test.jpg', 'rb') as f:
    original_image = f.read()
db.insert_image(original_image)

# Read an image record by ID
image_data = db.read_image_by_id(1)  # Read image with ID 1
if image_data:
    original, size1, size2, size3 = image_data
    print("Original image and resized images retrieved!")

# Update resized images
with open('test.jpg', 'rb') as f:
    resized_image1 = f.read()
db.update_image(1, size1=resized_image1)
