from flask import Blueprint, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os

def create_upload_bp(mysql):
    upload_bp = Blueprint('upload', __name__)

    @upload_bp.route('/upload', methods=['GET', 'POST'])
    def upload():
        if 'username' not in session:
            return redirect(url_for('login'))

        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            pricing = request.form['pricing']
            file = request.files['file']
            filename = secure_filename(file.filename)
            file.save(os.path.join('static/uploads', filename))

            user_id = session['id']  # Get the user ID from the session

            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO materials (material_title, photo_path, description, pricing, user_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (title, filename, description, pricing, user_id))
            mysql.connection.commit()
            cur.close()

            return redirect(url_for('my_materials'))

        return render_template('upload.html')

    return upload_bp