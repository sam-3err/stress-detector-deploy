<h1 align="center">🧠 Stress Detector AI</h1>

<p align="center">
  <strong>Real-Time Facial Emotion & Stress Analysis using Deep Learning, CNN and Flask</strong>
</p>

<p align="center">
  <img src="Images_output/Stress_High.png" alt="Stress High Example" width="300"/>
  &nbsp;&nbsp;&nbsp;
  <img src="Images_output/Stress_Low.png" alt="Stress Low Example" width="300"/>
</p>

---

## 📌 Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [System Architecture & Flow](#system-architecture--flow)
4. [The Dataset (FER2013)](#the-dataset-fer2013)
5. [Emotion-to-Stress Mapping](#emotion-to-stress-mapping)
6. [Tech Stack](#tech-stack)
7. [Project Structure](#project-structure)
8. [Setup & Installation](#setup--installation)
9. [Running the Application](#running-the-application)
10. [API Endpoints](#api-endpoints)
11. [Sample Output](#sample-output)
12. [License](#license)

---

## Project Overview

The **AI Stress Detector** is a real-time computer vision and deep learning web application that detects and quantifies human stress levels through facial expression analysis.

Rather than treating stress as a simple binary (yes/no), this system maps **7 human facial emotions** to a custom **weighted stress index heuristic**, giving users a precise percentage-based stress score.

The application supports two modes:
1. **Live Webcam Analysis** — Continuous real-time emotion detection from your camera.
2. **Static Image Upload** — Upload any portrait photo for instant stress evaluation.

---

## Features

- 🎥 **Real-Time Webcam Streaming** — Live frame-by-frame emotion processing via Flask multipart streaming.
- 📸 **Photo Upload & Analysis** — Drag-and-drop or click-to-upload portrait analysis.
- 📊 **Dynamic Dashboard** — Live stress gauges, trend charts (Chart.js), and emotion probability bars.
- 🤖 **7-Emotion Recognition** — Detects: Angry, Disgust, Scared, Happy, Sad, Surprised, Neutral.
- 🔒 **Thread-Safe Inference** — Mutex locks (`cascade_lock`, `model_lock`) prevent race conditions.
- 🟡 **Fallback Face Detection** — If no face is found, the full image is analyzed (no crashes).

---

## System Architecture & Flow

### Step-by-Step Pipeline

```
[User Uploads Image / Opens Camera]
         │ (Tech: HTML5 & JavaScript Fetch POST)
         ▼
[Server Receives & Resizes Image]
         │ (Tech: Flask Backend & OpenCV — max width 500px)
         ▼
[Grayscale Conversion & Face Detection]
         │ (Tech: OpenCV Haar Cascade Classifier + Thread Lock)
         ▼
[Face Bounding Box & Fallback Logic]
         │ (Tech: Python Clip Coordinate boundaries)
         ▼
[Neural Network Inference]
         │ (Tech: TensorFlow/Keras Mini-XCEPTION model + Thread Lock)
         ▼
[Stress Score Math Calculation]
         │ (Tech: Python Weighted Heuristic  →  Score = Σ(Pᵢ × Wᵢ))
         ▼
[JSON Packaging & Base64 Image Conversion]
         │ (Tech: Base64 string encoding + Flask jsonify)
         ▼
[UI Gauge & Trend Chart Update]
         │ (Tech: JavaScript & Chart.js — no page reload)
         ▼
[Updated Dashboard with Gauges, Trends & Charts]
```

### Detailed System Flowchart

```
              ┌──────────────────────────────┐
              │    User's Web Browser        │
              │  (HTML5, JS, CSS, Chart.js)  │
              └──────────────┬───────────────┘
                             │ HTTP POST File Upload (Fetch API)
                             ▼
              ┌──────────────────────────────┐
              │      Flask Backend           │
              │        (app.py)              │
              └──────────────┬───────────────┘
                             │ Standardizes size to width = 500px
                             ▼
              ┌──────────────────────────────┐
              │      OpenCV Pipeline         │
              │   Grayscale Conversion       │
              └──────────────┬───────────────┘
                             │ Thread-Locked Face Detection (cascade_lock)
                             ▼
              ┌──────────────────────────────┐
              │    Haar Cascade Classifier   │
              │  (Finds face coordinates)    │
              └──────────────┬───────────────┘
                             │ Cropped face region resized to 64×64
                             ▼
              ┌──────────────────────────────┐
              │  Mini-XCEPTION AI Model      │
              │ (Thread-Locked TensorFlow)   │
              └──────────────┬───────────────┘
                             │ Calculates Weighted Stress Index
                             ▼
              ┌──────────────────────────────┐
              │   JSON & Base64 Response     │
              │  (Sent back to Browser)      │
              └──────────────┬───────────────┘
                             │ Dynamic Dashboard update (No page reload)
                             ▼
              ┌──────────────────────────────┐
              │      Updated Dashboard       │
              │   (Gauges, Trends & Charts)  │
              └──────────────────────────────┘
```

### How Each Step Works

| Step | Action | Technology |
|------|---------|------------|
| **1. Upload** | User selects image via browser. JS bundles it in `FormData` and sends a background `fetch('/upload_image')` call — no page reload. | HTML5 File Input, JavaScript ES6, Fetch API |
| **2. Receive & Standardize** | Flask receives file stream. OpenCV decodes it into a NumPy color matrix and resizes to max 500px width. | Flask, OpenCV (`cv2.imdecode`, `imutils.resize`) |
| **3. Face Detection** | Image is converted to grayscale. A thread-safe `cascade_lock` is acquired before Haar Cascade runs, returning bounding box `(x, y, w, h)`. | OpenCV Haar Cascade, `threading.Lock()` |
| **4. Fallback Logic** | Bounding box is clipped to image boundaries. If no face found, the entire image is used as the face region. | Python bounds clipping (`max`/`min`) |
| **5. Neural Inference** | Cropped face is resized to 64×64, normalized to [0.0, 1.0], reshaped to `(1, 64, 64, 1)`. A `model_lock` is acquired, then `.predict()` runs to produce 7 emotion probabilities. | TensorFlow, Keras, Mini-XCEPTION |
| **6. Stress Calculation** | `Stress Score = Σ(Probabilityᵢ × Weightᵢ)` using the emotion-to-weight mapping table below. | Python math |
| **7. Response Packaging** | OpenCV draws green (face found) or yellow (fallback) bounding box. Image is JPEG-encoded and Base64-converted. Result is returned as JSON. | Base64, Flask `jsonify` |
| **8. Dashboard Update** | JS parses JSON, updates the stress gauge, fills emotion progress bars, adjusts border color (Red/Orange/Green), and appends to the trend chart. | JavaScript, Chart.js |

---

## The Dataset (FER2013)

The underlying AI model is a **Mini-XCEPTION Convolutional Neural Network** trained on the world-renowned **FER2013 (Facial Expression Recognition 2013)** dataset.

| Property | Value |
|----------|-------|
| **Image Size** | 48 × 48 pixels, Grayscale (1-channel) |
| **Total Images** | 35,887 |
| **Training Set** | 28,709 images |
| **Validation Set** | 3,589 images |
| **Test Set** | 3,589 images |
| **Dataset Size** | ~58.4 MB (zipped) / ~96 MB (unzipped CSV) |

---

## Emotion-to-Stress Mapping

The system maps each predicted emotion to a stress weight:

| Class ID | Emotion | Stress Weight | Stress Level | ~Image Count |
|:---:|:---|:---:|:---|:---|
| **0** | 😡 **Angry** | `1.0` | Very High | ~4,953 |
| **1** | 🤢 **Disgust** | `0.8` | High | ~547 *(Rarest)* |
| **2** | 😨 **Scared** | `1.0` | Very High | ~5,121 |
| **3** | 😄 **Happy** | `0.0` | No Stress | ~8,989 *(Most)* |
| **4** | 😢 **Sad** | `0.8` | High | ~6,077 |
| **5** | 😲 **Surprised** | `0.4` | Moderate | ~4,002 |
| **6** | 😐 **Neutral** | `0.1` | Minimal | ~6,198 |

**Formula:**
```
Stress Score (%) = Σ (Emotion_Probability_i × Stress_Weight_i) × 100
```

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | HTML5, CSS3, JavaScript (ES6), Chart.js |
| **Backend** | Python 3, Flask |
| **Computer Vision** | OpenCV (`cv2`), Haar Cascade Classifier |
| **Deep Learning** | TensorFlow 2.x, Keras |
| **AI Model** | Mini-XCEPTION CNN (trained on FER2013) |
| **Model Files** | `fer.h5` (model weights), `fer.json` (model architecture) |
| **Image Encoding** | Base64 + NumPy |
| **Threading** | Python `threading.Lock()` for safe concurrent requests |

---

## Project Structure

```
Stress_Detector/
│
├── code/                          # 🚀 Core Application
│   ├── app.py                     # Flask server — routes & API endpoints
│   ├── test.py                    # VideoCamera class, AI inference logic
│   ├── fer.h5                     # Trained model weights (Keras HDF5)
│   ├── fer.json                   # Model architecture (JSON)
│   ├── _mini_XCEPTION.102-0.66.hdf5  # Alternate mini model checkpoint
│   └── templates/
│       └── index.html             # Frontend UI (dashboard, camera, upload)
│
├── Images_output/                 # 📸 Sample output screenshots
│   ├── Stress_High.png            # Example: High stress detection
│   └── Stress_Low.png             # Example: Low stress detection
│
├── venv/                          # 🐍 Python virtual environment (not tracked)
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
├── LICENSE.md                     # MIT License
└── README.md                      # This file
```

---

## Setup & Installation

### Prerequisites
- Python 3.8 or higher
- A working webcam (for live mode)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/NamrataSancheti/stress_detector_AI.git
cd stress_detector_AI
```

### 2. Create & Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
# Make sure virtual environment is active first
.\venv\Scripts\activate

# Navigate to the code folder
cd code

# Run the Flask server
python app.py
```

Then open your browser and go to:
```
http://127.0.0.1:5000
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Renders the main dashboard UI |
| `GET` | `/predict` | Starts the live webcam MJPEG stream |
| `GET` | `/status` | Returns the latest stress info as JSON |
| `POST` | `/upload_image` | Accepts an image file, returns stress analysis + annotated image as JSON |

### `/upload_image` Response Format
```json
{
  "image": "data:image/jpeg;base64,<encoded_string>",
  "info": {
    "emotion": "Sad",
    "stress_score": 0.78,
    "emotion_probabilities": {
      "Angry": 0.12,
      "Happy": 0.05,
      "Sad": 0.72,
      ...
    }
  }
}
```

---

<p align="center">Made with ❤️ | Deep Learning Final Project | 2026</p>
