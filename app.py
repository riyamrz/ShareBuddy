from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash

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

@app.route('/')
def home():
    if 'username' in session:
        username = session['username']
        return render_template('home.html', username=username)
    else:
        return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form['login_input']
        password = request.form['password']
        
        # Open a new cursor to execute the query
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s OR email = %s", (login_input, login_input))
        user = cur.fetchone()
        cur.close()

        # Check if the user exists and the password matches
        if user and check_password_hash(user[3], password):  # Adjust index based on your table structure
            session['username'] = user[1]  # Assuming username is at index 1
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

        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)  # Remove 'username' from the session
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
