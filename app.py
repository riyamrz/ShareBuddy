from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # Create a Flask app
app.secret_key = 'your_secret_key'  # Set a secret key for the session

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://phpmyadmin:3850@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
