from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, session
from predict import predict_image
from database import init_db, save_upload, get_all_uploads, register_user, login_user, get_user_by_id, get_user_uploads
from werkzeug.utils import secure_filename
from functools import wraps
import os
import uuid

# ========== CONFIGURATION ==========
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_FOLDER = os.path.join(BASE_DIR, "templates")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed file extensions (security)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB max

# Admin usernames (add your admin username here)
ADMIN_USERS = ['admin', 'hariram']

app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
app.secret_key = os.environ.get('SECRET_KEY', 'deepfake_secret_key_2026')
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Initialize DB
init_db()

# ========== HELPER FUNCTIONS ==========

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        if session.get("username") not in ADMIN_USERS:
            return render_template("error.html", message="Access Denied! Admin only."), 403
        return f(*args, **kwargs)
    return decorated_function

def generate_unique_filename(filename):
    """Generate unique filename to prevent overwrites"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'jpg'
    return f"{uuid.uuid4().hex}.{ext}"

# ========== AUTH ROUTES ==========

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("home"))
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        success, user = login_user(username, password)
        
        if success:
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid username or password!")
    
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "user_id" in session:
        return redirect(url_for("home"))
    
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        
        if password != confirm_password:
            return render_template("signup.html", error="Passwords do not match!")
        
        if len(password) < 6:
            return render_template("signup.html", error="Password must be at least 6 characters!")
        
        success, message = register_user(username, email, password)
        
        if success:
            return redirect(url_for("login"))
        else:
            return render_template("signup.html", error=message)
    
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ========== MAIN ROUTES ==========

@app.route("/")
@login_required
def home():
    return render_template("index.html", username=session.get("username"))

# Serve uploaded images (protected)
@app.route("/uploads/<filename>")
@login_required
def uploaded_file(filename):
    # Secure: only serve files that exist, prevent directory traversal
    filename = secure_filename(filename)
    return send_from_directory(UPLOAD_FOLDER, filename)

# Prediction API
@app.route("/predict_api", methods=["POST"])
@login_required
def predict_api():
    # Check if file exists
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    
    # Validate file type
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Allowed: PNG, JPG, JPEG, GIF, WEBP"}), 400
    
    # Generate unique filename (security + prevent overwrites)
    unique_filename = generate_unique_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    file.save(file_path)

    # Get prediction with confidence
    result, confidence = predict_image(file_path)

    # Save in database with user_id
    save_upload(unique_filename, result, confidence, session.get("user_id"))

    return jsonify({
        "result": result,
        "confidence": f"{confidence:.2f}%"
    })

# User's history
@app.route("/history")
@login_required
def history():
    uploads = get_user_uploads(session["user_id"])
    return render_template("history.html", uploads=uploads, username=session.get("username"))

# Admin dashboard (PROTECTED - admin only)
@app.route("/admin")
@admin_required
def admin():
    uploads = get_all_uploads()
    return render_template("admin.html", uploads=uploads, username=session.get("username"))

# Error handlers
@app.errorhandler(413)
def file_too_large(e):
    return jsonify({"error": "File too large. Maximum size is 10MB"}), 413

@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", message="Page not found!"), 404

if __name__ == "__main__":
    app.run(debug=True)
