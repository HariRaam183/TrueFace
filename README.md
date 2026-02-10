# 🛡️ TrueFace - AI Deepfake Detection System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/TensorFlow-2.20-orange?logo=tensorflow" alt="TensorFlow">
  <img src="https://img.shields.io/badge/Flask-2.x-green?logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/Docker-Ready-blue?logo=docker" alt="Docker">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
</p>

A production-ready, full-stack AI-powered deepfake detection web application that uses deep learning to identify manipulated or AI-generated images.

## 🎯 Live Demo

🌐 **[Try it live on Render](https://trueface.onrender.com)** _(if deployed)_

---

## ✨ Features

| Feature                    | Description                                        |
| -------------------------- | -------------------------------------------------- |
| 🧠 **AI Detection**        | MobileNetV2-based CNN model with 90%+ accuracy     |
| 📊 **Confidence Score**    | Shows prediction confidence (e.g., "FAKE - 87.3%") |
| 👤 **Face Detection**      | Auto-detects and crops faces for better accuracy   |
| 🔒 **User Authentication** | Secure login/signup with password hashing          |
| 👑 **Admin Dashboard**     | View all uploads, stats, and user activity         |
| 📱 **Responsive UI**       | Works on desktop and mobile devices                |
| ⚡ **Loading States**      | Professional UX with spinners and disabled buttons |
| 🐳 **Docker Ready**        | One-command deployment with Docker Compose         |

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│   Frontend      │────▶│   Flask API     │────▶│   TFLite Model  │
│   (HTML/JS)     │     │   (Backend)     │     │   (AI/ML)       │
│                 │     │                 │     │                 │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │   SQLite DB     │
                        │   (Users/Logs)  │
                        └─────────────────┘
```

---

## 📁 Project Structure

```
TrueFace/
├── backend/
│   ├── app.py              # Flask application & routes
│   ├── predict.py          # AI inference with face detection
│   └── database.py         # SQLite database operations
├── model/
│   ├── deepfake_model.h5   # Original Keras model
│   └── deepfake_model.tflite # Optimized TFLite model
├── templates/
│   ├── index.html          # Main detection page
│   ├── login.html          # User login
│   ├── signup.html         # User registration
│   ├── history.html        # User's prediction history
│   ├── admin.html          # Admin dashboard
│   └── error.html          # Error page
├── dataset/
│   ├── train/real/         # Training real images
│   ├── train/fake/         # Training fake images
│   ├── test/real/          # Test real images
│   └── test/fake/          # Test fake images
├── uploads/                # User uploaded images
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
├── requirements.txt        # Python dependencies
├── Procfile               # Render/Heroku deployment
└── train_model.py         # Model training script
```

---

## 🚀 Quick Start

### Option 1: Local Development

```bash
# 1. Clone the repository
git clone https://github.com/HariRaam183/TrueFace.git
cd TrueFace

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
cd backend
python app.py
```

🌐 Open: **http://localhost:5000**

### Option 2: Docker (Recommended for Production)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t trueface .
docker run -p 5000:5000 trueface
```

---

## 🔧 Configuration

### Environment Variables

| Variable               | Description          | Default                    |
| ---------------------- | -------------------- | -------------------------- |
| `SECRET_KEY`           | Flask session secret | `deepfake_secret_key_2026` |
| `TF_CPP_MIN_LOG_LEVEL` | TensorFlow log level | `2`                        |

### Admin Users

Edit `backend/app.py` to add admin usernames:

```python
ADMIN_USERS = ['admin', 'your_username']
```

---

## 📊 Model Information

| Property         | Value                           |
| ---------------- | ------------------------------- |
| **Architecture** | MobileNetV2 (Transfer Learning) |
| **Input Size**   | 128x128x3 (RGB)                 |
| **Output**       | Binary (Real/Fake)              |
| **Format**       | TensorFlow Lite (.tflite)       |
| **Size**         | ~2.4 MB (optimized)             |

### Training Your Own Model

```bash
# 1. Add images to dataset folders
#    dataset/train/real/  - Real face images
#    dataset/train/fake/  - Deepfake images

# 2. Train the model
python train_model.py

# 3. Convert to TFLite (optional, for smaller size)
python convert_to_tflite.py
```

---

## 🔒 Security Features

- ✅ Password hashing with Werkzeug
- ✅ Session-based authentication
- ✅ Admin-only protected routes
- ✅ File type validation (JPG, PNG, WEBP only)
- ✅ File size limits (5MB max)
- ✅ Secure filename handling
- ✅ CSRF protection via Flask sessions

---

## ⚠️ Limitations

1. **Face-focused**: Works best with clear, frontal face images
2. **Still images only**: Does not support video input
3. **Training data dependent**: Accuracy depends on training dataset quality
4. **Not foolproof**: Sophisticated deepfakes may evade detection

---

## 🛣️ Roadmap

- [ ] Video deepfake detection
- [ ] API rate limiting
- [ ] Batch image upload
- [ ] Export reports as PDF
- [ ] Multi-language support

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Hari Raam**

- GitHub: [@HariRaam183](https://github.com/HariRaam183)

---

<p align="center">
  Made with ❤️ for fighting misinformation
</p>
