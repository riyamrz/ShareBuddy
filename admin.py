from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_mysqldb import MySQL
from flask_mail import Mail, Message

admin_bp = Blueprint('admin', __name__)

# Initialize MySQL
mysql = MySQL()

# Initialize Flask-Mail
mail = Mail()

@admin_bp.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        identifier = request.form.get('identifier')
        password = request.form.get('password')
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM admin WHERE username = %s OR email = %s", (identifier, identifier))
        admin = cursor.fetchone()
        if admin and admin[3] == password:  # Assuming the password is in the 4th column
            session['admin_username'] = admin[1]
            
            # Send email notification
            msg = Message('Admin Login Notification', recipients=[admin[2]])  # Assuming the email is in the 3rd column
            msg.body = f"Admin {admin[1]} has logged in."
            mail.send(msg)
            
            return redirect(url_for('admin.admin_dashboard'))
        else:
            return "Invalid credentials"
    return render_template('admin_login.html')

@admin_bp.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_username' in session:
        username = session['admin_username']
        return render_template('admin_dashboard.html', username=username)
    else:
        return redirect(url_for('admin.admin_login'))

@admin_bp.route('/admin/manage_users')
def manage_users():
    if 'admin_username' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.execute("SELECT id FROM admin")
        admin_ids = {row[0] for row in cursor.fetchall()}
        cursor.close()
        return render_template('manage_users.html', users=users, admin_ids=admin_ids)
    else:
        return redirect(url_for('admin.admin_login'))

@admin_bp.route('/delete_user', methods=['POST'])
def delete_user():
    if 'admin_username' in session:
        user_id = request.form['id']
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('admin.manage_users'))
    else:
        return redirect(url_for('admin.admin_login'))

@admin_bp.route('/update_user', methods=['GET', 'POST'])
def update_user():
    if 'admin_username' in session:
        if request.method == 'POST':
            user_id = request.form['id']
            username = request.form['username']
            email = request.form['email']
            faculty = request.form['faculty']
            contact = request.form['contact']
            semester = request.form['semester']
            cursor = mysql.connection.cursor()
            cursor.execute("""
                UPDATE users
                SET username = %s, email = %s, faculty = %s, contact = %s, semester = %s
                WHERE id = %s
            """, (username, email, faculty, contact, semester, user_id))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('admin.manage_users'))
        else:
            user_id = request.args.get('id')
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            cursor.close()
            return render_template('update_user.html', user=user)
    else:
        return redirect(url_for('admin.admin_login'))


# Routes for managing materials
@admin_bp.route('/admin/manage_materials')
def manage_materials():
    if 'admin_username' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM materials")
        materials = cursor.fetchall()
        cursor.close()
        return render_template('manage_materials.html', materials=materials)
    else:
        return redirect(url_for('admin.admin_login'))

@admin_bp.route('/delete_material', methods=['POST'])
def delete_material():
    if 'admin_username' in session:
        material_id = request.form['id']
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM materials WHERE id = %s", (material_id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('admin.manage_materials'))
    else:
        return redirect(url_for('admin.admin_login'))

@admin_bp.route('/update_material', methods=['GET', 'POST'])
def update_material():
    if 'admin_username' in session:
        if request.method == 'POST':
            material_id = request.form['id']
            title = request.form['title']
            description = request.form['description']
            pricing = request.form['pricing']
            cursor = mysql.connection.cursor()
            cursor.execute("""
                UPDATE materials
                SET material_title = %s, description = %s, pricing = %s
                WHERE id = %s
            """, (title, description, pricing, material_id))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('admin.manage_materials'))
        else:
            material_id = request.args.get('id')
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM materials WHERE id = %s", (material_id,))
            material = cursor.fetchone()
            cursor.close()
            return render_template('update_material.html', material=material)
    else:
        return redirect(url_for('admin.admin_login'))