from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_mysqldb import MySQL

admin_bp = Blueprint('admin', __name__)

# Initialize MySQL
mysql = MySQL()

@admin_bp.route('/admin')
def admin_dashboard():
    if 'username' in session:
        username = session['username']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT is_admin FROM users WHERE username = %s", (username,))
        is_admin = cursor.fetchone()[0]
        if is_admin:
            return render_template('admin.html', username=username)
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@admin_bp.route('/admin/manage_users')
def manage_users():
    if 'username' in session and session.get('is_admin'):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return render_template('manage_users.html', users=users)
    else:
        return redirect(url_for('login'))

@admin_bp.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'username' in session and session.get('is_admin'):
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        mysql.connection.commit()
        return redirect(url_for('admin.manage_users'))
    else:
        return redirect(url_for('login'))

@admin_bp.route('/admin/update_user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    if 'username' in session and session.get('is_admin'):
        cursor = mysql.connection.cursor()
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            faculty = request.form['faculty']
            contact = request.form['contact']
            semester = request.form['semester']
            cursor.execute("""
                UPDATE users
                SET username = %s, email = %s, faculty = %s, contact = %s, semester = %s
                WHERE id = %s
            """, (username, email, faculty, contact, semester, user_id))
            mysql.connection.commit()
            return redirect(url_for('admin.manage_users'))
        else:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            return render_template('update_user.html', user=user)
    else:
        return redirect(url_for('login'))