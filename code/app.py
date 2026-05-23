from flask import Flask, render_template, Response, jsonify, request
from .test import VideoCamera, process_image_array
import test
import cv2
import numpy as np
import base64
from flask import request, jsonify
app = Flask(__name__, template_folder='templates')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json['image']

    encoded = data.split(",")[1]
    img_data = base64.b64decode(encoded)

    np_arr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    result = process_image_array(frame)

    return jsonify(result)
@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):

    while True:

        try:

            frame = camera.get_frame()

            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' +
                frame +
                b'\r\n'
            )

        except Exception as e:

            print("STREAM ERROR:", e)
            break

@app.route('/predict')
def predict():

    return Response(
        gen(VideoCamera()),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/status')
def status():
    return jsonify(test.latest_stress_info)

@app.route('/analyze_frame', methods=['POST'])
def analyze_frame():

    data = request.json['image']

    encoded_data = data.split(',')[1]

    np_arr = np.frombuffer(
        base64.b64decode(encoded_data),
        np.uint8
    )

    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    result = process_image_array(frame)

    return jsonify(result)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'})
        
        file = request.files['image']
        # Read the image array using frombuffer (modern alternative to fromstring)
        npimg = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({'error': 'Invalid image file or format'})

        # Process
        processed_img, info = process_image_array(img)
        
        # Encode back to base64
        _, buffer = cv2.imencode('.jpg', processed_img)
        img_b64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            'image': 'data:image/jpeg;base64,' + img_b64,
            'info': info
        })
    except Exception as e:
        import traceback
        print("UPLOAD ERROR TRACEBACK:")
        traceback.print_exc()
        return jsonify({'error': f"Internal Server Error: {str(e)}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)