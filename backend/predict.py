import os

# ===== FORCE CPU ONLY (for Render/Heroku deployment) =====
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TF warnings

import tensorflow as tf

# Disable GPU explicitly
tf.config.set_visible_devices([], 'GPU')

# Limit memory growth for stability
tf.config.threading.set_intra_op_parallelism_threads(1)
tf.config.threading.set_inter_op_parallelism_threads(1)

import cv2
import numpy as np
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "deepfake_model.h5")

# Load model once at startup
logger.info(f"Loading model from: {MODEL_PATH}")
try:
    model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    logger.info("Model loaded successfully!")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    model = None

def predict_image(img_path):
    """
    Predict if an image is REAL or FAKE
    Returns: (result, confidence_percentage)
    """
    try:
        # Check if model loaded
        if model is None:
            logger.error("Model not loaded!")
            return "ERROR", 0.0
        
        # Read and preprocess image
        img = cv2.imread(img_path)
        
        if img is None:
            logger.error(f"Failed to read image: {img_path}")
            return "ERROR", 0.0
        
        img = cv2.resize(img, (128, 128))
        img = img.astype('float32') / 255.0
        img = np.reshape(img, (1, 128, 128, 3))

        # Get prediction
        prediction = model.predict(img, verbose=0)[0][0]
        
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
