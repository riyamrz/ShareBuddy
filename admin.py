from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_mysqldb import MySQL

admin_bp = Blueprint('admin', __name__)

# Initialize MySQL
mysql = MySQL()

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