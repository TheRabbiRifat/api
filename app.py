from flask import Flask, request, send_file, jsonify, make_response
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
    if 'pdf' not in request.files:
        return jsonify({"error": "No PDF file provided"}), 400

    pdf_file = request.files['pdf']
    reader = PdfReader(pdf_file)
    images = []

    # Extract images from the PDF
    for page in reader.pages:
        for image in page.images:
            image_io = io.BytesIO()
            image_io.write(image.data)
            image_io.seek(0)
            images.append(image_io)

    if len(images) < 2:
        return jsonify({"error": "The PDF does not contain enough images"}), 400

    # Prepare response with both images
    photo_image = images[0]
    sign_image = images[1]

    response = make_response()
    response.headers["Content-Type"] = "multipart/mixed"

    with io.BytesIO() as combined:
        combined.write(photo_image.read())
        combined.write(sign_image.read())
        combined.seek(0)
        response.data = combined.read()

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, debug=True)
