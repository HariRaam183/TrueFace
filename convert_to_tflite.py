# Run this script ONCE locally to convert the model to TensorFlow Lite
import tensorflow as tf
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "deepfake_model.h5")
TFLITE_PATH = os.path.join(BASE_DIR, "model", "deepfake_model.tflite")

print(f"Loading model from: {MODEL_PATH}")
model = tf.keras.models.load_model(MODEL_PATH)

print("Converting to TensorFlow Lite...")
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]  # Optimize for size
tflite_model = converter.convert()

print(f"Saving TFLite model to: {TFLITE_PATH}")
with open(TFLITE_PATH, 'wb') as f:
    f.write(tflite_model)

# Get file sizes for comparison
h5_size = os.path.getsize(MODEL_PATH) / (1024 * 1024)
tflite_size = os.path.getsize(TFLITE_PATH) / (1024 * 1024)

print(f"\n✅ Conversion complete!")
print(f"Original model size: {h5_size:.2f} MB")
print(f"TFLite model size: {tflite_size:.2f} MB")
print(f"Size reduction: {((h5_size - tflite_size) / h5_size * 100):.1f}%")
