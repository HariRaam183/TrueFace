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


def predict_image(img_path):
    """
    Predict if an image is REAL or FAKE using TFLite
    Returns: (result, confidence_percentage)
    """
    try:
        # Check if model loaded
        if interpreter is None:
            logger.error("Model not loaded!")
            return "ERROR", 0.0
        
        # Read and preprocess image
        img = cv2.imread(img_path)
        
        if img is None:
            logger.error(f"Failed to read image: {img_path}")
            return "ERROR", 0.0
        
        # Preprocess: resize, normalize, reshape
        img = cv2.resize(img, (128, 128))
        img = img.astype(np.float32) / 255.0
        img = np.expand_dims(img, axis=0)  # Shape: (1, 128, 128, 3)

        # Run inference
        interpreter.set_tensor(input_details[0]['index'], img)
        interpreter.invoke()
        prediction = interpreter.get_tensor(output_details[0]['index'])[0][0]
        
        # Calculate confidence
        if prediction > 0.5:
            result = "FAKE"
            confidence = float(prediction) * 100
        else:
            result = "REAL"
            confidence = (1 - float(prediction)) * 100
        
        logger.info(f"Prediction: {result} | Confidence: {confidence:.2f}% | File: {os.path.basename(img_path)}")
        
        return result, confidence
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        import traceback
        traceback.print_exc()
        return "ERROR", 0.0
