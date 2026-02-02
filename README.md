# Deepfake Detection System

A full-stack application for detecting deepfakes in images using deep learning. The system provides a user-friendly React-based frontend for image upload, a Flask backend serving a MobileNetV2-based binary classifier, and an admin dashboard to monitor all image predictions.

## Project Overview

- **Upload an image:** Get real-time predictions (REAL or FAKE) powered by a deep learning model.
- **Admin dashboard:** View the full history of uploaded images and their classification results.
- **Persistent history:** All predictions are stored in a local SQLite database, accessible via a built-in web dashboard.

## Project Structure

```
DeepFake-Detection/
├── backend/
│   ├── app.py             # Flask backend server with prediction & admin API
│   ├── database.py        # SQLite database logic for uploads and results
├── model/
│   └── deepfake_model.h5  # Trained Keras model file (generated after training)
├── dataset/
│   ├── train/
│   │   ├── real/
│   ���   └── fake/
│   └── test/
│       ├── real/
│       └── fake/
├── predict.py             # Model inference logic
├── train_model.py         # Model training script
├── templates/
│   ├── index.html         # Frontend UI (if using Flask templates)
│   └── admin.html         # Admin dashboard HTML
├── uploads/               # Folder for uploaded images
├── frontend/
│   ├── public/
│   │   └── index.html     # React static template
│   ├── src/
│   │   ├── App.js         # Main React app
│   │   └── ...
│   └── package.json
├── README.md
└── uploads.db             # SQLite database file (auto-generated)
```

## Features

- 🧠 **Deep learning:** Transfer learning with MobileNetV2 for robust deepfake detection.
- 📤 **Image upload:** Simple, intuitive upload UI—supports drag-and-drop or file selection.
- 🔮 **Binary predictions:** Classifies input as either "REAL" or "FAKE".
- 📊 **Admin dashboard:** Check upload history and prediction results visually at `/admin`.
- 🗃️ **Database:** Automatically logs every upload and model result (filename, result, timestamp).
- 🌐 **REST API:** Flask backend exposes API endpoints for prediction and file handling.
- ⚛️ **Frontend:** Built in React—easy to extend or customize.
- 🚀 **Easy deployment:** Run backend and frontend locally with minimal configuration.

## Setup Instructions

### 1. Prepare Dataset

- Place real images in:
  - `dataset/train/real/`
  - `dataset/test/real/`
- Place fake images in:
  - `dataset/train/fake/`
  - `dataset/test/fake/`

### 2. Install Python Dependencies

```bash
pip install tensorflow opencv-python numpy flask flask-cors
```

### 3. Train the Model

```bash
python train_model.py
# Generates 'model/deepfake_model.h5'
```

### 4. Run the Backend Server

```bash
cd backend
python app.py
```
- The prediction API runs at: `POST /predict_api`
- The admin dashboard is accessible at: [http://localhost:5000/admin](http://localhost:5000/admin)

### 5. Run the Frontend

```bash
cd frontend
npm install
npm start
```
- Visit [http://localhost:3000](http://localhost:3000) in your browser.

## Usage

1. Open the frontend.
2. Select or drag-and-drop an image file.
3. Click "Check" to submit for prediction.
4. View the result—either **REAL** or **FAKE**.
5. For history/analytics, visit `/admin` on the backend.

## Technologies Used

- **Model/Inference:** TensorFlow, MobileNetV2, OpenCV
- **Backend:** Python, Flask, SQLite
- **Frontend:** React, Axios, HTML/CSS
- **Database:** SQLite (automatic, no setup required)

## Admin Dashboard

- `/admin`: Visualize all uploads—image previews, filenames, predictions, and timestamps.
- Table-driven UI for reviewer convenience.

---

> **Note:** Make sure to train the model or download a pre-trained model to `model/deepfake_model.h5` before running the full end-to-end pipeline.

---

**License:** MIT
