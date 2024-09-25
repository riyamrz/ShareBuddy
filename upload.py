from flask import Blueprint, request, redirect, url_for, session, render_template
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
import os

def create_upload_bp(mysql, mail):
    upload_bp = Blueprint('upload', __name__)

    @upload_bp.route('/upload', methods=['GET', 'POST'])
    def upload():
        if 'username' not in session:
            return redirect(url_for('login'))

        if request.method == 'POST':
            title = request.form['material_title']
            description = request.form['description']
            pricing = request.form['pricing']
            file = request.files['photo_path']
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join('static/uploads', filename))

                user_id = session['id']  # Get the user ID from the session

                cur = mysql.connection.cursor()
                cur.execute("SELECT email FROM users WHERE id = %s", (user_id,))
                user_email = cur.fetchone()[0]

                cur.execute("""
                    INSERT INTO materials (material_title, photo_path, description, pricing, user_id)
                    VALUES (%s, %s, %s, %s, %s)
                """, (title, filename, description, pricing, user_id))
                mysql.connection.commit()
                cur.close()

                # Send email notification to admin
                admin_email = 'admin@example.com'  # Replace with the admin's email address
                msg = Message(
                    'New Material Uploaded',
                    recipients=[admin_email],
                    body=f'New material "{title}" has been uploaded by user with email {user_email}.'
                )
                mail.send(msg)

                return redirect(url_for('my_materials'))

        return render_template('upload.html')

    return upload_bp