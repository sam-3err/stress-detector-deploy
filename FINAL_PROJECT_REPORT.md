# Academic Project Report: Deep Neural Emotion & Stress Analysis System

---

## 1. Project Information & Overview

### A. Objectives
The **AI Stress Detector** is a real-time computer vision and deep learning web application designed to detect and quantify human stress levels using facial expression analysis. The system supports:
1. **Real-time Live Webcam Analysis**: Continuous facial capturing and frame-by-frame emotion processing.
2. **Static Photo Uploads**: Direct browser-based portrait uploads for instant stress evaluation.
3. **Dynamic Dashboard Metrics**: Real-time stress gauges, historical trends (via Chart.js), and exact probability breakdowns of 7 major facial expressions.

### B. Core System Logic
Rather than treating stress as a simple binary (yes/no), this project maps the **7 human facial emotions** to a custom **weighted stress index heuristic**. Each predicted emotion has a stress weight ranging from `0.0` (no stress) to `1.0` (extreme stress).

---

## 2. The Training Dataset (FER2013)

The underlying "AI Brain" (a Mini-XCEPTION Convolutional Neural Network) was trained on the world-renowned **FER2013 (Facial Expression Recognition 2013)** dataset.

### A. Key Facts & Dimensions
* **Data Dimensions**: All images are standardized to $48 \times 48$ pixels, grayscale (1-channel).
* **Data volume**: **35,887 human facial images** in total.
  * **Training Set**: `28,709 images` (used for neural weight adjustments).
  * **Public Validation Set**: `3,589 images` (used for parameter checking during training).
  * **Private Test Set**: `3,589 images` (used for final accuracy scoring).
* **Size on Disk**: Zipped at **58.4 MB** (approx. **96 MB** unzipped in CSV format containing raw pixel vectors).

### B. Emotion Class Distribution
The dataset is split across 7 distinct human expressions. The exact distribution of images is as follows:

| Class ID | Emotion Label | Stress Weight | Approximate Image Count |
| :---: | :--- | :---: | :--- |
| **0** | 😡 **Angry** | `1.0` (Very High) | ~4,953 images |
| **1** | 🤢 **Disgust** | `0.8` (High) | ~547 images *(Rarest class)* |
| **2** | 😨 **Scared** | `1.0` (Very High) | ~5,121 images |
| **3** | 😄 **Happy** | `0.0` (No Stress) | ~8,989 images *(Most abundant)* |
| **4** | 😢 **Sad** | `0.8` (High) | ~6,077 images |
| **5** | 😲 **Surprised** | `0.4` (Moderate) | ~4,002 images |
| **6** | 😐 **Neutral** | `0.1` (Minimal) | ~6,198 images |

---

## 3. Step-by-Step Project Flow & Tech Stack

Here is the exact step-by-step pipeline mapping how a photo gets uploaded, processed, evaluated, and rendered back to the user, alongside the technology used at each point:

```
[User Uploads Image]
         │ (Tech: HTML5 & JavaScript Fetch POST)
         ▼
[Server Receives & Resizes Image]
         │ (Tech: Flask Backend & OpenCV Resize)
         ▼
[Grayscale Conversion & Face Detection]
         │ (Tech: OpenCV Haar Cascade Classifier + Thread Lock)
         ▼
[Face Bounding Box & Fallback Logic]
         │ (Tech: Python Clip Coordinate boundaries)
         ▼
[Neural Network Inference]
         │ (Tech: TensorFlow, Keras Mini-XCEPTION model + Thread Lock)
         ▼
[Stress Score Math Calculation]
         │ (Tech: Python Weighted Heuristic)
         ▼
[JSON Packaging & Base64 Image Conversion]
         │ (Tech: Base64 string encoding)
         ▼
[UI Gauge & Trend Chart Update]
         │ (Tech: JS, HTML, Chart.js)
```

---

### Step 1: The Upload
* **Action**: The user opens the web app in Chrome/Firefox, clicks the **Upload Picture** button, and selects a portrait image from their desktop.
* **Tech Stack**: **HTML5** (File Input Element) & **JavaScript (ES6)**.
* **How It Works**: JavaScript intercepts the file select event, bundles the raw image inside a virtual `FormData` envelope, and initiates a background network call (`fetch('/upload_image')`) without freezing or reloading the web page.

### Step 2: Receiving & Standardizing
* **Action**: The Flask backend receives the raw file stream in a child thread and prepares it for vision scanning.
* **Tech Stack**: **Flask (Python Framework)** & **OpenCV (`cv2`)**.
* **How It Works**: Flask takes the request files. OpenCV converts the raw file stream into a NumPy color matrix (`cv2.imdecode`) and resizes the image to a standardized maximum width of `500 pixels` (using `imutils.resize`). 
  > **Why?**: Resizing standardizes inputs, increases processing speeds by 10x, and completely prevents OpenCV out-of-bound C++ vector subscript errors on high-resolution photos.

### Step 3: Finding the Face
* **Action**: The server converts the standardized image to black-and-white and detects the face coordinates.
* **Tech Stack**: **OpenCV Grayscale Conversion** & **Haar Cascade Face Classifier** (`haarcascade_frontalface_default.xml`).
* **How It Works**: 
  1. The image is converted to grayscale (`cv2.cvtColor`) since color is irrelevant for matching spatial facial details (eyes, nose, mouth lines).
  2. To prevent concurrent threading conflicts between the active webcam feed thread and the upload request thread, a global **`cascade_lock = threading.Lock()`** is acquired. 
  3. Under mutual exclusion, the Haar Cascade scans the grayscale image and returns bounding box coordinates `(x, y, w, h)` for any human faces found.

### Step 4: Robust Coordinate Fallback
* **Action**: The system clips the bounding box coordinates to ensure they are inside the image borders.
* **Tech Stack**: **Python Bounds Clipping Logic**.
* **How It Works**: 
  1. Coordinates are bounded using `max` and `min` checks to prevent negative values or coordinates exceeding image dimensions.
  2. **Fallback**: If no face is detected (due to lighting or angle), the system treats the **entire image** as the face region, drawing a yellow bounding box. This guarantees the upload **always** gives a successful stress evaluation and never crashes.

### Step 5: Deep Learning Expression Recognition
* **Action**: The face region is fed into the deep learning model.
* **Tech Stack**: **TensorFlow & Keras**, **Mini-XCEPTION model**, and **Grayscale Normalization**.
* **How It Works**: 
  1. The cropped face ROI is resized to $64 \times 64$ pixels, normalized to $[0.0, 1.0]$, converted to a float array, and reshaped into a $4\text{D}$ tensor of shape `(1, 64, 64, 1)`.
  2. A global **`model_lock = threading.Lock()`** is acquired.
  3. The Mini-XCEPTION model (`.predict`) executes forward propagation to produce a softmax array containing the probability values for all 7 emotions.

### Step 6: Stress Score Calculation
* **Action**: The predicted emotion array is mapped to a stress index score.
* **Tech Stack**: **Python Math Logic**.
* **How It Works**: The system calculates the stress score using a weighted mathematical sum:
  $$\text{Stress Score} = \sum (\text{Probability}_i \times \text{Weight}_i)$$
  *(Refer to Section 2-B for the exact weight mappings).*

### Step 7: Packaging & Transmission
* **Action**: The server compiles all results and sends them back to the browser.
* **Tech Stack**: **Base64 Encoding** & **JSON**.
* **How It Works**:
  1. OpenCV draws a bounding box outline (green for face, yellow for fallback) around the detected face region.
  2. The processed image is converted into a standard JPG byte buffer and encoded into a standard **Base64 ASCII string**.
  3. Flask packs the Base64 image string and the calculated stress dictionary into a clean JSON packet and returns it with a `200 OK` status.

### Step 8: Frontend Dashboard Rendering
* **Action**: The dashboard dynamically updates to display the results.
* **Tech Stack**: **JavaScript** & **Chart.js**.
* **How It Works**:
  1. JavaScript parses the JSON response.
  2. The live webcam stream is hidden, and the canvas displays the uploaded analyzed photo.
  3. The stress level border color adjusts instantly (Red for High, Orange for Moderate, Green for Low).
  4. The 7 emotion breakdown progress bars dynamically fill, and the numerical stress gauge rises to show the exact percentage.

---

## 4. Easy-to-Understand Flowchart

Here is a simplified flowchart of the system architecture you can walk through with Ma'am:

```
                  ┌──────────────────────────────┐
                  │    User's Web Browser        │
                  │  (HTML5, JS, CSS, Chart.js)  │
                  └──────────────┬───────────────┘
                                 │
                                 │ HTTP POST File Upload (Fetch API)
                                 ▼
                  ┌──────────────────────────────┐
                  │      Flask Backend           │
                  │        (app.py)              │
                  └──────────────┬───────────────┘
                                 │
                                 │ Standardizes size to width = 500px
                                 ▼
                  ┌──────────────────────────────┐
                  │      OpenCV Pipeline         │
                  │   Grayscale Conversion       │
                  └──────────────┬───────────────┘
                                 │
                                 │ Thread-Locked Face Detection (cascade_lock)
                                 ▼
                  ┌──────────────────────────────┐
                  │    Haar Cascade Classifier   │
                  │  (Finds face coordinates)    │
                  └──────────────┬───────────────┘
                                 │
                                 │ Cropped face region resized to 64x64
                                 ▼
                  ┌──────────────────────────────┐
                  │  Mini-XCEPTION AI Model      │
                  │ (Thread-Locked tensorflow)   │
                  └──────────────┬───────────────┘
                                 │
                                 │ Calculates Weighted Stress Index
                                 ▼
                  ┌──────────────────────────────┐
                  │   JSON & Base64 Response     │
                  │  (Sent back to Browser)      │
                  └──────────────┬───────────────┘
                                 │
                                 │ Dynamic Dashboard update (No page reload)
                                 ▼
                  ┌──────────────────────────────┐
                  │      Updated Dashboard       │
                  │   (Gauges, Trends & Charts)  │
                  └──────────────────────────────┘
```

---
*Report prepared on 2026-05-17. Ready for submission.*
