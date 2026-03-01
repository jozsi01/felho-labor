import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Konfiguráció
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max 16MB fájlméret
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///photos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Adatbázis Modell
class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False) # Max 40 karakter
    filename = db.Column(db.String(120), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.now)

# Adatbázis létrehozása az első indításkor
with app.app_context():
    db.create_all()

# Segédfüggvény a fájlkiterjesztések ellenőrzéséhez
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Főoldal: Listázás és Feltöltés
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fájl feltöltés kezelése
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        photo_name = request.form.get('name')

        if file.filename == '' or not photo_name:
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Fájl mentése az 'uploads' mappába
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Adatbázis bejegyzés létrehozása
            new_photo = Photo(name=photo_name[:40], filename=filename) # Biztosítjuk a max 40 karaktert
            db.session.add(new_photo)
            db.session.commit()
            return redirect(url_for('index'))

    # Rendezés paraméter lekérése (alapértelmezett: dátum szerint csökkenő)
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

# Kép megtekintése
@app.route('/photo/<int:id>')
def view_photo(id):
    photo = Photo.query.get_or_404(id)
    return render_template('photo.html', photo=photo)

# Kép törlése
@app.route('/delete/<int:id>', methods=['POST'])
def delete_photo(id):
    photo = Photo.query.get_or_404(id)
    # Fájl törlése a lemezről
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    # Bejegyzés törlése az adatbázisból
    db.session.delete(photo)
    db.session.commit()
    return redirect(url_for('index'))

# Fájlok kiszolgálása a böngészőnek
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # Biztosítjuk, hogy az uploads mappa létezik
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)