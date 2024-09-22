from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os

def create_upload_bp(mysql):
    upload_bp = Blueprint('upload', __name__)

    @upload_bp.route('/upload', methods=['GET', 'POST'])
    def upload():
        if 'username' not in session or 'id' not in session:
            return redirect(url_for('login'))

        if request.method == 'POST':
            material_title = request.form['material_title']
            description = request.form['description']
            pricing = request.form['pricing']
            
            if 'photo' not in request.files:
                return "No photo part", 400
            
            photo = request.files['photo']
            if photo.filename == '':
                return "No selected file", 400
            
            filename = secure_filename(photo.filename)
            photo.save(os.path.join('static/uploads', filename))

            user_id = session['id']

            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO materials (material_title, description, pricing, photo_path, user_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (material_title, description, pricing, filename, user_id))
            mysql.connection.commit()
            cur.close()

            return redirect(url_for('home'))

        return render_template('upload.html')

    return upload_bp