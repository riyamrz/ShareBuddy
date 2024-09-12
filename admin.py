from flask import Blueprint, render_template, session, redirect, url_for
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