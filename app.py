from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash
from admin import admin_bp
from upload import create_upload_bp

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)  # Create a Flask app
app.secret_key = os.getenv('SECRET_KEY')  # Set a secret key for the session

# Configure MySQL
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
mysql = MySQL(app)  # Initialize MySQL

# Configure Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)  # Initialize Flask-Mail

# Register the blueprints
app.register_blueprint(admin_bp)
upload_bp = create_upload_bp(mysql)  # Create the upload blueprint
app.register_blueprint(upload_bp)  # Register the upload blueprint

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT m.material_title, m.photo_path, m.description, m.pricing, u.id, u.username 
        FROM materials m 
        JOIN users u ON m.id = u.id
    """)
    materials = cur.fetchall()
    cur.close()

    if 'username' in session:
        username = session['username']
        return render_template('home.html', username=username, materials=materials)
    else:
        return render_template('home.html', materials=materials)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form['login_input']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s OR email = %s", (login_input, login_input))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[3], password):  # Adjust index based on your table structure
            session['username'] = user[1]  # Assuming username is at index 1
            session['id'] = user[0]  # Assuming id is at index 0
            
            # Send login email
            msg = Message(
                'Login Notification',
                sender=app.config['MAIL_DEFAULT_SENDER'],
                recipients=[user[2]],  # Assuming email is at index 2
                body='You have just logged in to ShareBuddy.'
            )
            mail.send(msg)
            
            return redirect(url_for('home'))
        
        return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        faculty = request.form['faculty']
        contact = request.form['contact']
        semester = request.form['semester']
        
        hashed_password = generate_password_hash(password)

        # Open a new cursor to execute the query
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO users (username, email, password, faculty, contact, semester)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (username, email, hashed_password, faculty, contact, semester))
        mysql.connection.commit()
        cur.close()

        # Send registration email
        msg = Message(
            'Welcome to ShareBuddy',
            recipients=[email],
            body='Thank you for registering with ShareBuddy!'
        )
        mail.send(msg)

        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)  # Remove 'username' from the session
    return redirect(url_for('home'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    if request.method == 'POST':
        bio = request.form['bio']
        
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE users
            SET bio = %s
            WHERE username = %s
        """, (bio, username))
        mysql.connection.commit()
        cur.close()

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT username, email, faculty, contact, semester, bio
        FROM users
        WHERE username = %s
    """, [username])
    user = cur.fetchone()
    cur.close()

    return render_template('profile.html', user=user)

@app.route('/browse')
def browse_materials():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT m.material_title, m.photo_path, m.description, m.pricing, u.id, u.username 
        FROM materials m 
        JOIN users u ON m.user_id = u.id
    """)
    materials = cur.fetchall()
    cur.close()

    # Debugging: Print the fetched materials
    print("Browse Materials:", materials)

    return render_template('browse.html', materials=materials)

@app.route('/my_materials')
def my_materials():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT material_title, photo_path, description, pricing 
        FROM materials 
        WHERE user_id = (SELECT id FROM users WHERE username = %s)
    """, (username,))
    materials = cur.fetchall()
    cur.close()

    # Debugging: Print the fetched materials
    print("My Materials:", materials)

    return render_template('my_materials.html', materials=materials)

@app.route('/view_profile/<int:id>')
def view_profile(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT username, email, faculty, contact, semester, bio FROM users WHERE id = %s", (id,))
    user = cur.fetchone()
    cur.close()

    if user:
        print(user)
        return render_template('view_profile.html', user=user)
    else:
        return "User not found", 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)