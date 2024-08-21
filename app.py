from flask import Flask, request, jsonify, render_template_string
from pypdf import PdfReader
import io
import base64
from PIL import Image

app = Flask(__name__)

def get_image_format(image_data):
    image = Image.open(io.BytesIO(image_data))
    return image.format.lower()


@app.route('/')
def home():
    html = '''
    <html>
    <head>
        <meta http-equiv="refresh" content="5;url=https://puffin24.xyz">
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                text-align: center;
            }
            .container {
                background: #fff;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                max-width: 500px;
                width: 100%;
            }
            h1 {
                font-size: 24px;
                color: #333;
                margin-bottom: 20px;
            }
            p {
                font-size: 16px;
                color: #555;
                margin: 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Proudly Served with Pie IT.</h1>
            <p>You will be redirected shortly...</p>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)



@app.route('/check-json')
def check_json():
    return jsonify({"status": "success", "message": "Flask app is running!"})

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
            image_format = get_image_format(image.data)
            image_base64 = base64.b64encode(image_io.getvalue()).decode('utf-8')
            images.append(f"data:image/{image_format};base64,{image_base64}")

    if len(images) < 2:
        return jsonify({"error": "The PDF does not contain enough images"}), 400

    # Prepare the images for the response
    response = {
        "photo": images[0],
        "sign": images[1]
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, debug=True)
