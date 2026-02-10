import os
import cv2
import numpy as np
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== TensorFlow Lite Runtime (Much lighter than full TensorFlow) =====
try:
    # Try tflite_runtime first (lighter, for deployment)
    from tflite_runtime.interpreter import Interpreter
    logger.info("Using tflite_runtime")
except ImportError:
    # Fall back to full TensorFlow's lite interpreter
    import tensorflow as tf
    Interpreter = tf.lite.Interpreter
    logger.info("Using tensorflow.lite")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "deepfake_model.tflite")

# Load face detection cascade
FACE_CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
logger.info("Face detection cascade loaded")

# Load TFLite model once at startup
logger.info(f"Loading TFLite model from: {MODEL_PATH}")
try:
    interpreter = Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    
    # Get input and output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    logger.info("TFLite model loaded successfully!")
    logger.info(f"Input shape: {input_details[0]['shape']}")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    interpreter = None
    input_details = None
    output_details = None


def detect_and_crop_face(img):
    """
    Detect face in image and crop it.
    Returns cropped face or original image if no face detected.
    """
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(30, 30)
        )
        
        if len(faces) > 0:
            # Get the largest face
            largest_face = max(faces, key=lambda f: f[2] * f[3])
            x, y, w, h = largest_face
            
            # Add padding around the face (20%)
            padding = int(0.2 * max(w, h))
            x = max(0, x - padding)
            y = max(0, y - padding)
            w = min(img.shape[1] - x, w + 2 * padding)
            h = min(img.shape[0] - y, h + 2 * padding)
            
            face_crop = img[y:y+h, x:x+w]
            logger.info(f"Face detected and cropped: {w}x{h}")
            return face_crop, True
        else:
            logger.info("No face detected, using full image")
            return img, False
    except Exception as e:
        logger.warning(f"Face detection failed: {e}, using full image")
        return img, False


def predict_image(img_path):
    """
    Predict if an image is REAL or FAKE using TFLite
    Returns: (result, confidence_percentage)
    """
    try:
        # Check if model loaded
        if interpreter is None:
            logger.error("Model not loaded!")
            return "MODEL_ERROR", 0.0
        
        # Read image
        img = cv2.imread(img_path)
        
        if img is None:
            logger.error(f"Failed to read image: {img_path}")
            return "READ_ERROR", 0.0
        
        # Check if image is too small
        if img.shape[0] < 50 or img.shape[1] < 50:
            logger.error(f"Image too small: {img.shape}")
            return "SIZE_ERROR", 0.0
        
        # Detect and crop face (improves accuracy)
        face_img, face_detected = detect_and_crop_face(img)
        
        # Preprocess: resize, normalize, reshape
        processed_img = cv2.resize(face_img, (128, 128))
        processed_img = processed_img.astype(np.float32) / 255.0
        processed_img = np.expand_dims(processed_img, axis=0)  # Shape: (1, 128, 128, 3)

        # Run inference
        interpreter.set_tensor(input_details[0]['index'], processed_img)
        interpreter.invoke()
        prediction = interpreter.get_tensor(output_details[0]['index'])[0][0]
        
        # Calculate confidence
        if prediction > 0.5:
            result = "FAKE"
            confidence = float(prediction) * 100
        else:
            result = "REAL"
            confidence = (1 - float(prediction)) * 100
        
        face_status = "face_detected" if face_detected else "full_image"
        logger.info(f"Prediction: {result} | Confidence: {confidence:.2f}% | {face_status} | File: {os.path.basename(img_path)}")
        
        return result, confidence
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        import traceback
        traceback.print_exc()
        return "ERROR", 0.0
