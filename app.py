from flask import Flask, request, send_file, jsonify
from pypdf import PdfReader
import io

app = Flask(__name__)

@app.route('/')
def index():
    return "Flask app is running!"

@app.route('/hello')
def hello():
    return jsonify({"message": "Hello, world!"})

@app.route('/extract-images', methods=['POST'])
def extract_images():
    # Check if the request contains a file
    if 'pdf' not in request.files:
        return jsonify({"error": "No PDF file provided"}), 400

    pdf_file = request.files['pdf']
    reader = PdfReader(pdf_file)
    images = []

    # Extract images from each page of the PDF
    for page in reader.pages:
        for image in page.images:
            image_io = io.BytesIO()
            image_io.write(image.data)
            image_io.seek(0)
            images.append(image_io)

    # Check if we have at least two images
    if len(images) < 2:
        return jsonify({"error": "The PDF does not contain enough images"}), 400

    # Prepare the two images with the specific names
    photo_image = images[0]
    sign_image = images[1]

    # Send the images back as separate files in a single response
    return send_file(photo_image, mimetype='image/png', as_attachment=True, download_name='photo.png'), \
           send_file(sign_image, mimetype='image/png', as_attachment=True, download_name='sign.png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, debug=True)
