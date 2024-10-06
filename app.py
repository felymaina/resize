import os
from flask import Flask, request, jsonify, render_template
from model import ImageResizerDB
from resizer import ImageResizer

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Initialize database
db = ImageResizerDB()
db.create_table()  # Create table if it doesn't exist

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route to render the upload form and gallery
@app.route('/')
def home():
    return render_template('form.html')

# Route to upload an image and create a new record
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Create uploads directory if it doesn't exist
        file.save(filepath)

        # Use the resizer class to resize the image
        resizer = ImageResizer()
        resized_images = resizer.resize_image(filepath)

        # Insert original and resized images into the database
        with open(filepath, 'rb') as original_file:
            original_data = original_file.read()
        
        # Save resized images to bytes
        resized_bytes = [img.tobytes() for img in resized_images]

        db.insert_image(original_data, resized_bytes[0], resized_bytes[1], resized_bytes[2])

        original_url = f"/{filepath}"
        resized_urls = [
            f"/uploads/resized_1080x1080.jpg",
            f"/uploads/resized_2000x365.jpg",
            f"/uploads/resized_600x348.jpg"
        ]

        return jsonify({
            'message': 'Image uploaded and resized successfully!',
            'original_url': original_url,
            'resized_urls': resized_urls
        }), 201

    return jsonify({'error': 'File type not allowed'}), 400

# Route to get all images for the gallery
@app.route('/images', methods=['GET'])
def get_images():
    images = db.get_all_images()
    return jsonify(images), 200

# HTML Form and Gallery
@app.route('/gallery', methods=['GET'])
def gallery():
    images = db.get_all_images()
    return render_template('gallery.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)
