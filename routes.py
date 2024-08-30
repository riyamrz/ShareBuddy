from flask import render_template, request, redirect, url_for, session
from app import app

@app.route('/')
def home():
    # Debugging line
    print(f"Session data: {session}")
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')