from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)  # Create a Flask app
app.secret_key = 'your_secret_key'  # Set a secret key for the session

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'phpmyadmin'
app.config['MYSQL_PASSWORD'] = '3850'
app.config['MYSQL_DB'] = 'flask'
mysql = MySQL(app)  # Initialize MySQL

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        
        # Open a new cursor to execute the query
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        user = cur.fetchone()
        cur.close()

        # Check if the user exists and the password matches
        if user and pwd == user[1]:  # Adjust index based on your table structure
            session['username'] = user[0]  # Store the username in the session
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']

        # Open a new cursor to execute the query
        cur = mysql.connection.cursor()
        # Use parameterized queries to prevent SQL injection
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, pwd))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove 'username' from the session
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
