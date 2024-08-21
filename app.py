from flask import Flask, request, jsonify
from pypdf import PdfReader
import io
import base64

app = Flask(__name__)

# Route for checking if the application is running
@app.route('/')
def home():
    return "Flask app is running!"

# Route for checking a simple JSON response
@app.route('/check-json')
def check_json():
    return jsonify({"status": "success", "message": "Flask app is running!"})

# Route for extracting images from a PDF
@app.route('/extract-images', methods=['POST'])
def extract_images():
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
            image_base64 = base64.b64encode(image_io.getvalue()).decode('utf-8')
            images.append(image_base64)

    if len(images) < 2:
        return jsonify({"error": "The PDF does not contain enough images"}), 400

    # Send the first two images as Base64 encoded strings
    response = {
        "photo": images[0],
        "sign": images[1]
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, debug=True)
