import sys
sys.path.insert(0, 'c:\\pip_packages')

import traceback

try:
    import cv2
    print("[1] cv2 imported OK")

    cap = cv2.VideoCapture(0)
    print("[2] VideoCapture(0) opened:", cap.isOpened())

    ret, frame = cap.read()
    print("[3] cap.read() ret:", ret, "frame is None:", frame is None)

    if ret and frame is not None:
        print("[4] Frame shape:", frame.shape)
        import imutils
        frame = cv2.flip(frame, 1)
        frame = imutils.resize(frame, width=500, height=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        print("[5] Gray shape:", gray.shape)

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        print("[6] Faces detected:", len(faces))

        from keras.models import load_model
        from keras.preprocessing.image import img_to_array
        import numpy as np
        emotion_classifier = load_model("_mini_XCEPTION.102-0.66.hdf5", compile=False)
        print("[7] Emotion model loaded OK")

        _, jpeg = cv2.imencode('.jpg', frame)
        print("[8] JPEG encode OK, size:", len(jpeg.tobytes()), "bytes")
    else:
        print("[ERROR] Camera failed to read a frame!")

    cap.release()
    print("[9] Camera released OK")

except Exception as e:
    print("[EXCEPTION]", e)
    traceback.print_exc()
