from flask import Flask, render_template, jsonify, request
from .test import process_image_array
import cv2
import numpy as np
import base64
import os
import traceback

app = Flask(__name__, template_folder='templates')


# ==========================================
# HOME PAGE
# ==========================================

@app.route('/')
def index():
    return render_template('index.html')


# ==========================================
# REALTIME FRAME ANALYSIS
# ==========================================

@app.route('/analyze_frame', methods=['POST'])
def analyze_frame():

    try:

        payload = request.get_json(silent=True) or {}
        data = payload.get('image')

        if not data or ',' not in data:
            return jsonify({
                "emotion": "No Frame",
                "stress_value": 0,
                "stress_label": "Waiting for camera",
                "emotion_probs": {}
            })

        # Remove base64 header
        encoded_data = data.split(',')[1]

        # Decode image
        np_arr = np.frombuffer(
            base64.b64decode(encoded_data),
            np.uint8
        )

        frame = cv2.imdecode(
            np_arr,
            cv2.IMREAD_COLOR
        )

        if frame is None:
            return jsonify({
                "emotion": "No Frame",
                "stress_value": 0,
                "stress_label": "Waiting for camera",
                "emotion_probs": {}
            })

        # Process image using AI model
        _, info = process_image_array(frame)

        return jsonify(info)

    except Exception as e:

        print("ANALYZE FRAME ERROR:", e)
        traceback.print_exc()

        return jsonify({
            "emotion": "Error",
            "stress_value": 0,
            "stress_label": "Error",
            "emotion_probs": {}
        }), 500


# ==========================================
# IMAGE UPLOAD ANALYSIS
# ==========================================

@app.route('/upload_image', methods=['POST'])
def upload_image():

    try:

        if 'image' not in request.files:

            return jsonify({
                'error': 'No image uploaded'
            })

        file = request.files['image']

        # Read image
        npimg = np.frombuffer(
            file.read(),
            np.uint8
        )

        img = cv2.imdecode(
            npimg,
            cv2.IMREAD_COLOR
        )

        if img is None:

            return jsonify({
                'error': 'Invalid image'
            })

        # Process image
        processed_img, info = process_image_array(img)

        # Convert processed image back to base64
        _, buffer = cv2.imencode('.jpg', processed_img)

        img_b64 = base64.b64encode(buffer).decode('utf-8')

        return jsonify({

            'image':
                'data:image/jpeg;base64,' + img_b64,

            'info':
                info
        })

    except Exception as e:

        print("UPLOAD ERROR:", e)
        traceback.print_exc()

        return jsonify({
            'error': str(e)
        }), 500


# ==========================================
# RUN FLASK APP
# ==========================================

if __name__ == '__main__':

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
