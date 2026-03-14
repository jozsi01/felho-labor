import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

# Konfiguráció
app.config['SECRET_KEY'] = 'titkos-kulcs-ide' # Ez a munkamenetek (session) biztonságához kell
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
db_url = os.environ.get("DATABASE_URL")
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url or "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Login Menedzser beállítása
login_manager = LoginManager(app)
login_manager.login_view = 'login' # Ide irányít, ha bejelentkezés köteles oldalra mész
login_manager.login_message = "Kérlek, jelentkezz be az oldal megtekintéséhez."

# --- ADATBÁZIS MODELLEK ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    # Növeld meg 128-ról 256-ra vagy Text-re
    password_hash = db.Column(db.String(256), nullable=False) 
    photos = db.relationship('Photo', backref='uploader', lazy=True)

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) # Ezt is érdemes növelni
    filename = db.Column(db.String(255), nullable=False) # 120-ról 255-re
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

with app.app_context():
    db.create_all()
    # Feltöltési mappa létrehozása futásidőben
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- ÚTVONALAK (ROUTES) ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('Ez a felhasználónév már foglalt!')
            return redirect(url_for('register'))
            
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Sikeres regisztráció! Most már bejelentkezhetsz.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Hibás felhasználónév vagy jelszó!')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Csak bejelentkezett felhasználók tölthetnek fel képet!')
            return redirect(url_for('login'))
            
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        photo_name = request.form.get('name')

        if file.filename == '' or not photo_name:
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Itt rendeljük hozzá a feltöltőt (current_user.id) a képhez!
            new_photo = Photo(name=photo_name[:40], filename=filename, user_id=current_user.id)
            db.session.add(new_photo)
            db.session.commit()
            return redirect(url_for('index'))

    sort_by = request.args.get('sort', 'date_desc')
    if sort_by == 'name_asc':
        photos = Photo.query.order_by(Photo.name.asc()).all()
    elif sort_by == 'name_desc':
        photos = Photo.query.order_by(Photo.name.desc()).all()
    elif sort_by == 'date_asc':
        photos = Photo.query.order_by(Photo.upload_date.asc()).all()
    else:
        photos = Photo.query.order_by(Photo.upload_date.desc()).all()

    return render_template('index.html', photos=photos, current_sort=sort_by)

@app.route('/photo/<int:id>')
def view_photo(id):
    photo = Photo.query.get_or_404(id)
    return render_template('photo.html', photo=photo)

@app.route('/delete/<int:id>', methods=['POST'])
@login_required # Csak bejelentkezve lehet ide eljutni
def delete_photo(id):
    photo = Photo.query.get_or_404(id)
    
    # KULCSFONTOSSÁGÚ: Csak akkor törölhet, ha ő a tulajdonos!
    if photo.user_id != current_user.id:
        flash('Nincs jogosultságod törölni ezt a képet!')
        return redirect(url_for('index'))

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    db.session.delete(photo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)